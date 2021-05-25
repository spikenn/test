from rest_framework import parsers, renderers, status
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import AuthTokenSerializer, ExportConfigurationSerializer
from .models import Record, ExportConfiguration
from .services import export_csv, get_or_create_configuration, allowed_fields

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Test'})


class ConfigurationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_configuration = get_or_create_configuration(self.request.user)
        serializer = ExportConfigurationSerializer(user_configuration)
        return Response(serializer.data)
    
    def put(self, request, *args, **kwargs):
        user_configuration = get_or_create_configuration(self.request.user)
        serializer = ExportConfigurationSerializer(user_configuration, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecordsExportWithConfigurationView(APIView):
    """
    Экспорт рекордов с конфигурацией из модели ExportConfiguration
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_configuration = get_or_create_configuration(self.request.user)
        field_list = user_configuration.field_list.replace(' ', '').split(',')
        return export_csv(field_list, user_configuration.filename, self.request.user)


class RecordsExportView(APIView):
    """
    Экспорт рекордов (конфигурируется параметрами в url).
    Принимает параметры fields со списком полей для экспорта и filename.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_user = self.request.user

        fields = request.GET.get('fields')
        filename = request.GET.get('filename')
        field_list = []

        if fields:
            fields = fields.replace(' ', '').split(',')
            for field in fields:
                if field in allowed_fields:
                    field_list.append(field)

        if len(field_list) < 1:
            field_list = allowed_fields

        if not filename:
            filename = f'{current_user.pk}_{current_user.name}'

        return export_csv(field_list, filename, current_user)

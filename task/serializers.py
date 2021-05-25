from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import ExportConfiguration
from .services import allowed_fields


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ExportConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExportConfiguration
        fields = ('filename', 'field_list')
    
    def validate_filename(self, value):
        reserved_chars = ('<', '>', ':', '"', '/', '"\"', '|', '?', '*')
        for char in value:
            if char in reserved_chars:
                raise serializers.ValidationError(f'Название файла содержит недопустимый символ {char}')
        return value
    
    def validate_field_list(self, value):
        fields = value.replace(' ', '').split(',')
        for field in fields:
            if field not in allowed_fields:
                raise serializers.ValidationError(f'Поле не существует: {field}')
        return value

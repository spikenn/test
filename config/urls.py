from django.contrib import admin
from django.urls import path, include

from task.views import obtain_auth_token

urlpatterns = [
    path('api/v1/', include('task.urls')),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls'))
]

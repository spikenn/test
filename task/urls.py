from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('templates/configure/', ConfigurationView.as_view(), name='configuration'),
    path('records/export/', RecordsExportView.as_view(), name='records_export'),
    path('records/export-from-template/', RecordsExportWithConfigurationView.as_view(), name='records_export_conf'),
]

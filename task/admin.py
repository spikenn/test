from django.contrib import admin

from .models import ExportConfiguration, User, Record, Status


class RecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'status', 'created_at')
    list_filter = ('user', 'status', 'created_at')


admin.site.register(User)
admin.site.register(ExportConfiguration)
admin.site.register(Status)
admin.site.register(Record, RecordAdmin)

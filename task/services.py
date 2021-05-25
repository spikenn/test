import csv

from django.http import HttpResponse

from .models import ExportConfiguration, Record


allowed_fields = ['id', 'created_at', 'description', 'phone', 'status']


def get_or_create_configuration(user):
    try:
        return ExportConfiguration.objects.get(user=user)
    except ExportConfiguration.DoesNotExist:
        return ExportConfiguration.objects.create(
            user=user,
            filename=f'{user.pk}_{user.name}',
            field_list='id, created_at, description, phone, status'
        )

def export_csv(field_list, filename, user):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'

    writer = csv.writer(response)
    writer.writerow(field_list)

    for record in Record.objects.filter(user=user):
        row = []
        for attr in field_list:
            if attr == 'created_at':
                row.append(getattr(record, attr).strftime('%y-%m-%d'))
            elif attr == 'phone':
                row.append(record.phone_number)
            else:
                row.append(getattr(record, attr))

        writer.writerow(row)
    return response

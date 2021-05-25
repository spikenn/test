**python manage.py createsuperuser**

**python manage.py createrecords --user <id пользователя. Default: 1> --records <количество рекордов. Default: 100>** - сгенерировать рекорды

**api-token-auth/** - авторизация (email, password)\
**api/v1/templates/configure/** - настройка шаблона\
**api/v1/records/export/** - экспорт в csv (конфигурация из параметров в url)\
**api/v1/records/export-from-template/** - экспорт в csv (конфигурация из шаблона (модели ExportConfiguration))\

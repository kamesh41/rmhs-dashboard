  web: python manage.py collectstatic --noinput && python manage.py migrate && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell && gunicorn rmhs_dashboard.wsgi --log-file -

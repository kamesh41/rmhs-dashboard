release: python manage.py migrate --noinput
web: python manage.py collectstatic --noinput && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword123') if not User.objects.filter(username='admin').exists() else print('Superuser exists')" && gunicorn rmhs_dashboard.wsgi --log-file -

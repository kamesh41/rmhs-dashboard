from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),  # This should be your last migration
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE dashboard_operation RENAME COLUMN tonnage TO quantity;",
            reverse_sql="ALTER TABLE dashboard_operation RENAME COLUMN quantity TO tonnage;"
        ),
    ] 
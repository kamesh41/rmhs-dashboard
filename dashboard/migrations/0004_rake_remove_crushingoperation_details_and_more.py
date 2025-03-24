# Generated by Django 5.1.7 on 2025-03-22 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_operation_reported_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rake_id', models.CharField(help_text='Unique ID for the rake', max_length=50, unique=True)),
                ('tippler', models.CharField(choices=[('WT-1', 'Wagon Tippler 1'), ('WT-2', 'Wagon Tippler 2'), ('WT-3', 'Wagon Tippler 3'), ('WT-4', 'Wagon Tippler 4')], max_length=4)),
                ('rake_in_time', models.DateTimeField(help_text='Time when rake entered the system')),
                ('rake_completed_time', models.DateTimeField(blank=True, help_text='Time when rake processing was completed', null=True)),
                ('rake_status', models.CharField(choices=[('Pending', 'Pending'), ('Progress', 'In Progress'), ('Complete', 'Complete')], default='Pending', max_length=10)),
                ('rake_type', models.CharField(help_text='Type of rake (e.g., BOXN, BOY)', max_length=50)),
                ('rake_material', models.CharField(help_text='Material carried by the rake', max_length=100)),
                ('reported_by', models.CharField(blank=True, max_length=100, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-rake_in_time'],
            },
        ),
        migrations.RemoveField(
            model_name='crushingoperation',
            name='details',
        ),
        migrations.RemoveField(
            model_name='feedingoperation',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='receivingoperation',
            name='source',
        ),
        migrations.RemoveField(
            model_name='reclaimingoperation',
            name='source',
        ),
        migrations.RemoveField(
            model_name='stackingoperation',
            name='destination',
        ),
        migrations.AddField(
            model_name='crushingoperation',
            name='crushing_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='operation',
            name='destination',
            field=models.ForeignKey(blank=True, help_text='Required for Feeding, Reclaiming, and Crushing operations', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.destination'),
        ),
        migrations.AddField(
            model_name='operation',
            name='source',
            field=models.ForeignKey(blank=True, help_text='Required for Receiving operations', null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.source'),
        ),
    ]

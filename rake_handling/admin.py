from django.contrib import admin
from .models import Rake

@admin.register(Rake)
class RakeAdmin(admin.ModelAdmin):
    list_display = ('rake_id', 'tippler', 'rake_type', 'rake_material', 'rake_status', 'rake_in_time', 'rake_completed_time', 'reported_by')
    list_filter = ('tippler', 'rake_status', 'rake_type')
    search_fields = ('rake_id', 'rake_material', 'reported_by')
    date_hierarchy = 'rake_in_time'

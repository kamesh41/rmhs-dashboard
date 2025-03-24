from django.contrib import admin
from .models import (
    Material, Destination, Source, Operation,
    FeedingOperation, StackingOperation, ReclaimingOperation,
    ReceivingOperation, CrushingOperation
)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('operation_type', 'date', 'shift', 'area', 'material', 'quantity', 'created_at')
    list_filter = ('operation_type', 'date', 'shift', 'area')
    search_fields = ('remarks',)
    date_hierarchy = 'date'

@admin.register(FeedingOperation)
class FeedingOperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift', 'area', 'material', 'destination', 'quantity')
    list_filter = ('date', 'shift', 'area', 'material', 'destination')
    search_fields = ('remarks',)

@admin.register(StackingOperation)
class StackingOperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift', 'area', 'material', 'destination', 'quantity')
    list_filter = ('date', 'shift', 'area', 'material', 'destination')
    search_fields = ('remarks',)

@admin.register(ReclaimingOperation)
class ReclaimingOperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift', 'area', 'material', 'source', 'quantity')
    list_filter = ('date', 'shift', 'area', 'material', 'source')
    search_fields = ('remarks',)

@admin.register(ReceivingOperation)
class ReceivingOperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift', 'area', 'material', 'source', 'quantity')
    list_filter = ('date', 'shift', 'area', 'material', 'source')
    search_fields = ('remarks',)

@admin.register(CrushingOperation)
class CrushingOperationAdmin(admin.ModelAdmin):
    list_display = ('date', 'shift', 'area', 'material', 'quantity')
    list_filter = ('date', 'shift', 'area', 'material')
    search_fields = ('remarks', 'crushing_details')



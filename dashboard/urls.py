from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main dashboard
    path('', views.dashboard, name='dashboard'),
    path('daily-summary/', views.daily_summary, name='daily_summary'),
    path('operations/', views.operations_list, name='operations_list'),
    
    # Operation exports
    path('export/excel/', views.export_operations_excel, name='export_excel'),
    path('export/pdf/', views.export_operations_pdf, name='export_pdf'),
    
    # Feeding operations
    path('feeding/add/', views.add_feeding_operation, name='add_feeding'),
    path('feeding/edit/<int:pk>/', views.edit_feeding_operation, name='edit_feeding'),
    path('feeding/delete/<int:pk>/', views.delete_feeding_operation, name='delete_feeding'),
    
    # Stacking operations
    path('stacking/add/', views.add_stacking_operation, name='add_stacking'),
    path('stacking/edit/<int:pk>/', views.edit_stacking_operation, name='edit_stacking'),
    path('stacking/delete/<int:pk>/', views.delete_stacking_operation, name='delete_stacking'),
    
    # Reclaiming operations
    path('reclaiming/add/', views.add_reclaiming_operation, name='add_reclaiming'),
    path('reclaiming/edit/<int:pk>/', views.edit_reclaiming_operation, name='edit_reclaiming'),
    path('reclaiming/delete/<int:pk>/', views.delete_reclaiming_operation, name='delete_reclaiming'),
    
    # Receiving operations
    path('receiving/add/', views.add_receiving_operation, name='add_receiving'),
    path('receiving/edit/<int:pk>/', views.edit_receiving_operation, name='edit_receiving'),
    path('receiving/delete/<int:pk>/', views.delete_receiving_operation, name='delete_receiving'),
    
    # Crushing operations
    path('crushing/add/', views.add_crushing_operation, name='add_crushing'),
    path('crushing/edit/<int:pk>/', views.edit_crushing_operation, name='edit_crushing'),
    path('crushing/delete/<int:pk>/', views.delete_crushing_operation, name='delete_crushing'),
] 
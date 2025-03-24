from django.urls import path
from . import views
from .views import (
    RakeDashboardView, RakeListView, 
    RakeCreateView, RakeUpdateView, RakeDeleteView,
    export_rakes_excel,
    export_rakes_pdf
)

app_name = 'rake_handling'

urlpatterns = [
    # Dashboard view
    path('', RakeDashboardView.as_view(), name='rake_dashboard'),
    
    # List view
    path('list/', RakeListView.as_view(), name='rake_list'),
    
    # CRUD operations
    path('add/', RakeCreateView.as_view(), name='add_rake'),
    path('<int:pk>/edit/', RakeUpdateView.as_view(), name='edit_rake'),
    path('<int:pk>/delete/', RakeDeleteView.as_view(), name='delete_rake'),
    
    # Export operations
    path('export/excel/', export_rakes_excel, name='export_excel'),
    path('export/pdf/', export_rakes_pdf, name='export_pdf'),
] 
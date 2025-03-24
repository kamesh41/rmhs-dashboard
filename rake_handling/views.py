from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta, datetime
from django.contrib import messages

from dashboard.utils import export_to_excel, export_to_pdf
from .models import Rake, TIPPLER_CHOICES, RAKE_STATUS_CHOICES
from .forms import RakeForm, RakeFilterForm

class RakeDashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view for rake handling"""
    template_name = 'rake_handling/rake_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get counts by status using case-insensitive comparison
        pending_count = Rake.objects.filter(rake_status__iexact='pending').count()
        progress_count = Rake.objects.filter(rake_status__iexact='progress').count()
        complete_count = Rake.objects.filter(rake_status__iexact='complete').count()
        
        # Add status counts to context
        context['pending_count'] = pending_count
        context['progress_count'] = progress_count
        context['complete_count'] = complete_count
        context['total_count'] = pending_count + progress_count + complete_count
        
        # Get recent rakes - limit to 10 for better performance
        context['recent_rakes'] = Rake.objects.all().order_by('-rake_in_time')[:10]
        
        # Get today's date
        today = timezone.now().date()
        
        # Get today's rakes
        today_rakes = Rake.objects.filter(
            rake_in_time__date=today
        )
        
        # Get today's count by status
        context['today_pending'] = today_rakes.filter(rake_status__iexact='pending').count()
        context['today_progress'] = today_rakes.filter(rake_status__iexact='progress').count()
        context['today_complete'] = today_rakes.filter(rake_status__iexact='complete').count()
        context['today_total'] = context['today_pending'] + context['today_progress'] + context['today_complete']
        
        # Get material statistics
        material_stats = Rake.objects.values('rake_material').annotate(
            count=Count('rake_material')
        ).order_by('-count')[:5]  # Limit to top 5 materials
        
        context['material_stats'] = material_stats
        
        return context

class RakeListView(LoginRequiredMixin, ListView):
    """List view for all rakes"""
    model = Rake
    template_name = 'rake_handling/rake_list.html'
    context_object_name = 'rakes'
    
    def get_queryset(self):
        # Get filter parameters
        date_from = self.request.GET.get('date_from')
        date_to = self.request.GET.get('date_to')
        tippler = self.request.GET.get('tippler')
        status = self.request.GET.get('status')
        
        # Initial queryset - default to current day if no date filter specified
        queryset = Rake.objects.all()
        
        # If no date filter is applied, show only today's rakes
        if not date_from and not date_to:
            today = timezone.now().date()
            queryset = queryset.filter(rake_in_time__date=today)
        else:
            # Apply date filters if provided
            if date_from:
                queryset = queryset.filter(rake_in_time__date__gte=date_from)
            if date_to:
                queryset = queryset.filter(rake_in_time__date__lte=date_to)
        
        # Apply other filters
        if tippler:
            queryset = queryset.filter(tippler=tippler)
        if status:
            queryset = queryset.filter(rake_status__iexact=status)
        
        return queryset.order_by('-rake_in_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get filtered queryset
        queryset = self.get_queryset()
        
        # Get counts
        context['total_rakes'] = queryset.count()
        
        # Use case-insensitive filtering for status counts
        context['pending_count'] = queryset.filter(rake_status__iexact='pending').count()
        context['progress_count'] = queryset.filter(rake_status__iexact='progress').count()
        context['completed_count'] = queryset.filter(rake_status__iexact='complete').count()
        
        # Get material summary
        context['material_summary'] = (
            queryset
            .values('rake_material')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        return context

class RakeCreateView(LoginRequiredMixin, CreateView):
    """Create view for a new rake"""
    model = Rake
    form_class = RakeForm
    template_name = 'rake_handling/rake_form.html'
    
    def form_valid(self, form):
        # Set the reported_by field to the current user
        form.instance.reported_by = self.request.user.username
        messages.success(self.request, 'Rake successfully added.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('rake_handling:rake_list')

class RakeUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for an existing rake"""
    model = Rake
    form_class = RakeForm
    template_name = 'rake_handling/rake_form.html'
    context_object_name = 'rake'
    
    def form_valid(self, form):
        # Update reported_by field to show who made the update
        form.instance.reported_by = self.request.user.username
        messages.success(self.request, 'Rake successfully updated.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('rake_handling:rake_list')

class RakeDeleteView(LoginRequiredMixin, DeleteView):
    """Delete view for a rake"""
    model = Rake
    template_name = 'rake_handling/rake_confirm_delete.html'
    context_object_name = 'rake'
    
    def get_success_url(self):
        return reverse_lazy('rake_handling:rake_list')

@login_required
def export_rakes_excel(request):
    """Export rakes data to Excel file"""
    # Get filter parameters
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    rake_type = request.GET.get('rake_type', '')
    
    # Initialize queryset with all rakes
    rakes = Rake.objects.all().order_by('-rake_in_time')
    
    # If no date filter is applied, show only today's rakes
    if not date_from and not date_to:
        today = timezone.now().date()
        rakes = rakes.filter(rake_in_time__date=today)
        # Set date_from and date_to to today for filename
        date_from = today.strftime('%Y-%m-%d')
        date_to = date_from
    else:
        # Apply date filters if provided
        if date_from:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            rakes = rakes.filter(rake_in_time__date__gte=date_from_obj)
        if date_to:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            rakes = rakes.filter(rake_in_time__date__lte=date_to_obj)
    
    # Apply other filters
    if status:
        rakes = rakes.filter(rake_status__iexact=status)
    if rake_type:
        rakes = rakes.filter(rake_type=rake_type)
    
    # Generate filename based on filters
    filename = "Rakes_Report"
    if date_from and date_to and date_from == date_to:
        filename += f"_{date_from}"
    elif date_from and date_to:
        filename += f"_{date_from}_to_{date_to}"
    elif date_from:
        filename += f"_from_{date_from}"
    elif date_to:
        filename += f"_until_{date_to}"
    
    if status:
        filename += f"_{status.title()}"
    
    if rake_type:
        filename += f"_{rake_type}"
    
    # Generate title
    title = "Rakes Report"
    date_range = ""
    if date_from and date_to and date_from == date_to:
        date_range = f"for {date_from}"
    elif date_from and date_to:
        date_range = f"from {date_from} to {date_to}"
    elif date_from:
        date_range = f"from {date_from}"
    elif date_to:
        date_range = f"until {date_to}"
    
    if date_range:
        title += f" {date_range}"
    
    if status:
        title += f" - {status.title()} Rakes"
    
    if rake_type:
        title += f" - {rake_type}"
    
    # Define columns for Excel export
    columns = [
        'rake_id', 
        'rake_type', 
        'rake_material', 
        'rake_status',
        'rake_in_time', 
        'rake_completed_time',
        'time_taken',
    ]
    
    # Get material summary
    material_summary = Rake.objects.filter(
        id__in=rakes.values_list('id', flat=True)
    ).values('rake_material').annotate(count=Count('rake_material')).order_by('rake_material')
    
    # Export to Excel
    return export_to_excel(
        rakes, 
        filename, 
        columns, 
        title=title,
        material_summary=material_summary
    )

@login_required
def export_rakes_pdf(request):
    """Export rakes data to PDF file"""
    # Get filter parameters
    status = request.GET.get('status', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    rake_type = request.GET.get('rake_type', '')
    
    # Initialize queryset with all rakes
    rakes = Rake.objects.all().order_by('-rake_in_time')
    
    # If no date filter is applied, show only today's rakes
    if not date_from and not date_to:
        today = timezone.now().date()
        rakes = rakes.filter(rake_in_time__date=today)
        # Set date_from and date_to to today for filename
        date_from = today.strftime('%Y-%m-%d')
        date_to = date_from
    else:
        # Apply date filters if provided
        if date_from:
            date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            rakes = rakes.filter(rake_in_time__date__gte=date_from_obj)
        if date_to:
            date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            rakes = rakes.filter(rake_in_time__date__lte=date_to_obj)
    
    # Apply other filters
    if status:
        rakes = rakes.filter(rake_status__iexact=status)
    if rake_type:
        rakes = rakes.filter(rake_type=rake_type)
    
    # Generate filename based on filters
    filename = "Rakes_Report"
    if date_from and date_to and date_from == date_to:
        filename += f"_{date_from}"
    elif date_from and date_to:
        filename += f"_{date_from}_to_{date_to}"
    elif date_from:
        filename += f"_from_{date_from}"
    elif date_to:
        filename += f"_until_{date_to}"
    
    if status:
        filename += f"_{status.title()}"
    
    if rake_type:
        filename += f"_{rake_type}"
    
    # Generate title
    title = "Rakes Report"
    date_range = ""
    if date_from and date_to and date_from == date_to:
        date_range = f"for {date_from}"
    elif date_from and date_to:
        date_range = f"from {date_from} to {date_to}"
    elif date_from:
        date_range = f"from {date_from}"
    elif date_to:
        date_range = f"until {date_to}"
    
    if date_range:
        title += f" {date_range}"
    
    if status:
        title += f" - {status.title()} Rakes"
    
    if rake_type:
        title += f" - {rake_type}"
    
    # Define columns for PDF export
    columns = [
        'rake_id', 
        'rake_type', 
        'rake_material', 
        'rake_status',
        'rake_in_time', 
        'rake_completed_time',
        'time_taken',
    ]
    
    # Get material summary
    material_summary = Rake.objects.filter(
        id__in=rakes.values_list('id', flat=True)
    ).values('rake_material').annotate(count=Count('rake_material')).order_by('rake_material')
    
    # Export to PDF
    return export_to_pdf(
        rakes, 
        filename, 
        columns, 
        title=title,
        material_summary=material_summary
    )

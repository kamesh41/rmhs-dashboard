from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    Operation, FeedingOperation, StackingOperation, 
    ReclaimingOperation, ReceivingOperation, CrushingOperation,
    Material, Destination, Source,
    SHIFT_CHOICES, OPERATION_TYPES
)
from .forms import (
    FilterForm, FeedingOperationForm, StackingOperationForm,
    ReclaimingOperationForm, ReceivingOperationForm, CrushingOperationForm
)
from .filters import OperationFilter
from .utils import export_to_excel, export_to_pdf, get_tonnage_summary, get_material_summary

class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if there are any filters applied
        any_filters = any(self.request.GET.values())
        today = timezone.now().date().strftime('%Y-%m-%d')
        
        # Get filter parameters
        date = self.request.GET.get('date', today if not any_filters else None)
        shift = self.request.GET.get('shift')
        area = self.request.GET.get('area')
        operation_type = self.request.GET.get('operation_type')
        
        # Base queryset
        queryset = Operation.objects.all()
        
        # Apply filters
        filters = {}
        if date:
            filters['date'] = date
        if shift:
            filters['shift'] = shift
        if area:
            filters['area'] = area
        if operation_type:
            filters['operation_type'] = operation_type
        
        if filters:
            queryset = queryset.filter(**filters)
        
        # Get operation summaries
        context['feeding_total'] = queryset.filter(operation_type='Feeding').aggregate(total=Sum('tonnage'))['total'] or 0
        context['stacking_total'] = queryset.filter(operation_type='Stacking').aggregate(total=Sum('tonnage'))['total'] or 0
        context['reclaiming_total'] = queryset.filter(operation_type='Reclaiming').aggregate(total=Sum('tonnage'))['total'] or 0
        context['receiving_total'] = queryset.filter(operation_type='Receiving').aggregate(total=Sum('tonnage'))['total'] or 0
        context['crushing_total'] = queryset.filter(operation_type='Crushing').aggregate(total=Sum('tonnage'))['total'] or 0
        
        # Get material summary
        context['material_summary'] = get_material_summary(queryset)
        
        # Get recent activities (last 10 operations)
        context['recent_activities'] = queryset.order_by('-date', '-created_at')[:10]
        
        # Add filter to context
        form_initial = {}
        if not any_filters:
            form_initial = {'date': today}
        
        context['filter'] = OperationFilter(self.request.GET or form_initial, queryset=Operation.objects.all())
        context['today'] = today
        
        return context

class FeedingOperationCreateView(CreateView):
    model = FeedingOperation
    form_class = FeedingOperationForm
    template_name = 'dashboard/operation_form.html'
    success_url = reverse_lazy('dashboard:feeding_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Feeding Operation'
        context['operation_type'] = 'Feeding'
        context['recent_entries'] = FeedingOperation.objects.order_by('-date', '-created_at')[:5]
        return context
    
    def form_valid(self, form):
        # Handle manual entry for material and destination
        material_name = form.cleaned_data.get('material_name')
        destination_name = form.cleaned_data.get('destination_name')
        
        # Get or create material
        material, _ = Material.objects.get_or_create(name=material_name)
        
        # Get or create destination
        destination, _ = Destination.objects.get_or_create(name=destination_name)
        
        # Set the material and destination on the instance
        form.instance.material = material
        form.instance.destination = destination
        
        messages.success(self.request, 'Feeding operation added successfully!')
        return super().form_valid(form)

class StackingOperationCreateView(CreateView):
    model = StackingOperation
    form_class = StackingOperationForm
    template_name = 'dashboard/operation_form.html'
    success_url = reverse_lazy('dashboard:stacking_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Stacking Operation'
        context['operation_type'] = 'Stacking'
        context['recent_entries'] = StackingOperation.objects.order_by('-date', '-created_at')[:5]
        return context
    
    def form_valid(self, form):
        # Handle manual entry for material and destination
        material_name = form.cleaned_data.get('material_name')
        destination_name = form.cleaned_data.get('destination_name')
        
        # Get or create material
        material, _ = Material.objects.get_or_create(name=material_name)
        
        # Get or create destination
        destination, _ = Destination.objects.get_or_create(name=destination_name)
        
        # Set the material and destination on the instance
        form.instance.material = material
        form.instance.destination = destination
        
        messages.success(self.request, 'Stacking operation added successfully!')
        return super().form_valid(form)

class ReclaimingOperationCreateView(CreateView):
    model = ReclaimingOperation
    form_class = ReclaimingOperationForm
    template_name = 'dashboard/operation_form.html'
    success_url = reverse_lazy('dashboard:reclaiming_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Reclaiming Operation'
        context['operation_type'] = 'Reclaiming'
        context['recent_entries'] = ReclaimingOperation.objects.order_by('-date', '-created_at')[:5]
        return context
    
    def form_valid(self, form):
        # Handle manual entry for material and source
        material_name = form.cleaned_data.get('material_name')
        source_name = form.cleaned_data.get('source_name')
        
        # Get or create material
        material, _ = Material.objects.get_or_create(name=material_name)
        
        # Get or create source
        source, _ = Source.objects.get_or_create(name=source_name)
        
        # Set the material and source on the instance
        form.instance.material = material
        form.instance.source = source
        
        messages.success(self.request, 'Reclaiming operation added successfully!')
        return super().form_valid(form)

class ReceivingOperationCreateView(CreateView):
    model = ReceivingOperation
    form_class = ReceivingOperationForm
    template_name = 'dashboard/operation_form.html'
    success_url = reverse_lazy('dashboard:receiving_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Receiving Operation'
        context['operation_type'] = 'Receiving'
        context['recent_entries'] = ReceivingOperation.objects.order_by('-date', '-created_at')[:5]
        return context
    
    def form_valid(self, form):
        # Handle manual entry for material and source
        material_name = form.cleaned_data.get('material_name')
        source_name = form.cleaned_data.get('source_name')
        
        # Get or create material
        material, _ = Material.objects.get_or_create(name=material_name)
        
        # Get or create source
        source, _ = Source.objects.get_or_create(name=source_name)
        
        # Set the material and source on the instance
        form.instance.material = material
        form.instance.source = source
        
        messages.success(self.request, 'Receiving operation added successfully!')
        return super().form_valid(form)

class CrushingOperationCreateView(CreateView):
    model = CrushingOperation
    form_class = CrushingOperationForm
    template_name = 'dashboard/operation_form.html'
    success_url = reverse_lazy('dashboard:crushing_create')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Crushing Operation'
        context['operation_type'] = 'Crushing'
        context['recent_entries'] = CrushingOperation.objects.order_by('-date', '-created_at')[:5]
        return context
    
    def form_valid(self, form):
        # Handle manual entry for material
        material_name = form.cleaned_data.get('material_name')
        
        # Get or create material
        material, _ = Material.objects.get_or_create(name=material_name)
        
        # Set the material on the instance
        form.instance.material = material
        
        messages.success(self.request, 'Crushing operation added successfully!')
        return super().form_valid(form)

class OperationListView(ListView):
    model = Operation
    template_name = 'dashboard/operation_list.html'
    context_object_name = 'operations'
    paginate_by = 20
    
    def get_queryset(self):
        # Check if there are any filters applied
        any_filters = any(self.request.GET.values())
        today = timezone.now().date().strftime('%Y-%m-%d')
        
        # Use QueryDict to allow modification
        query_params = self.request.GET.copy()
        
        # Set default date if no filters are applied
        if not any_filters:
            query_params['date'] = today
        
        # Get queryset
        queryset = super().get_queryset()
        self.filterset = OperationFilter(query_params, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['today'] = timezone.now().date().strftime('%Y-%m-%d')
        return context

class DailySummaryView(TemplateView):
    template_name = 'dashboard/daily_summary.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if there are any filters applied
        any_filters = any(self.request.GET.values())
        today = timezone.now().date().strftime('%Y-%m-%d')
        
        # Get filter parameters
        date = self.request.GET.get('date', today if not any_filters else None)
        area = self.request.GET.get('area')
        operation_type = self.request.GET.get('operation_type')
        
        # Base queryset
        queryset = Operation.objects.all()
        
        # Apply filters
        filters = {}
        if date:
            filters['date'] = date
        if area:
            filters['area'] = area
        if operation_type:
            filters['operation_type'] = operation_type
        
        if filters:
            queryset = queryset.filter(**filters)
        
        # Get operation summaries
        context['operation_summary'] = get_tonnage_summary(queryset)
        
        # Get material summary
        context['material_summary'] = get_material_summary(queryset)
        
        # Add filter to context
        form_initial = {}
        if not any_filters:
            form_initial = {'date': today}
        
        context['filter'] = OperationFilter(self.request.GET or form_initial, queryset=Operation.objects.all())
        context['today'] = today
        
        return context

@login_required
def export_operations_excel(request):
    """Export operations to Excel file"""
    # Get filter parameters
    date_str = request.GET.get('date')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    shift = request.GET.get('shift')
    area = request.GET.get('area')
    operation_type = request.GET.get('operation_type')
    
    # Check if any date filter is applied
    any_date_filter = date_str or date_from_str or date_to_str
    
    # Parse dates
    date = None
    date_from = None
    date_to = None
    
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Base queryset
    queryset = Operation.objects.all()
    
    # If no date filter is applied, default to today's operations
    if not any_date_filter:
        today = timezone.now().date()
        queryset = queryset.filter(date=today)
        # Set today as the default date for filename
        date = today
    else:
        # Apply date filters
        if date:
            queryset = queryset.filter(date=date)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
    
    # Apply other filters
    if shift:
        queryset = queryset.filter(shift=shift)
    if area:
        queryset = queryset.filter(area=area)
    if operation_type:
        queryset = queryset.filter(operation_type__iexact=operation_type)
    
    # Get operation summary
    operation_summary = {}
    for op_type, _ in OPERATION_TYPES:
        total = queryset.filter(operation_type=op_type).aggregate(sum=Sum('quantity'))['sum'] or 0
        operation_summary[op_type] = total
    
    # Get material summary
    material_summary = (
        queryset
        .values('material__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    
    # Define columns to export
    columns = ['date', 'shift', 'area', 'operation_type', 'material', 'quantity']
    
    # Build filename with filters
    filename = 'RMHS_Operations'
    if date:
        filename += f'_{date}'
    elif date_from and date_to:
        filename += f'_{date_from}_to_{date_to}'
    elif date_from:
        filename += f'_from_{date_from}'
    elif date_to:
        filename += f'_to_{date_to}'
        
    if shift:
        filename += f'_Shift_{shift}'
    if area:
        filename += f'_{area}'
    if operation_type:
        filename += f'_{operation_type}'
    
    # Generate title based on filters
    title = "Operations Report"
    if date:
        title += f" for {date}"
    elif date_from and date_to:
        title += f" from {date_from} to {date_to}"
    elif date_from:
        title += f" from {date_from}"
    elif date_to:
        title += f" to {date_to}"
    
    if shift:
        title += f" - Shift {shift}"
    if area:
        title += f" - {area}"
    if operation_type:
        title += f" - {operation_type.title()}"
    
    # Export to Excel
    return export_to_excel(
        queryset, 
        filename, 
        columns, 
        title=title,
        material_summary=material_summary,
        operation_summary=operation_summary
    )

@login_required
def export_operations_pdf(request):
    """Export operations to PDF file"""
    # Get filter parameters
    date_str = request.GET.get('date')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    shift = request.GET.get('shift')
    area = request.GET.get('area')
    operation_type = request.GET.get('operation_type')
    
    # Check if any date filter is applied
    any_date_filter = date_str or date_from_str or date_to_str
    
    # Parse dates
    date = None
    date_from = None
    date_to = None
    
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            pass
            
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Base queryset
    queryset = Operation.objects.all()
    
    # If no date filter is applied, default to today's operations
    if not any_date_filter:
        today = timezone.now().date()
        queryset = queryset.filter(date=today)
        # Set today as the default date for filename
        date = today
    else:
        # Apply date filters
        if date:
            queryset = queryset.filter(date=date)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
    
    # Apply other filters
    if shift:
        queryset = queryset.filter(shift=shift)
    if area:
        queryset = queryset.filter(area=area)
    if operation_type:
        queryset = queryset.filter(operation_type__iexact=operation_type)
    
    # Get operation summary
    operation_summary = {}
    for op_type, _ in OPERATION_TYPES:
        total = queryset.filter(operation_type=op_type).aggregate(sum=Sum('quantity'))['sum'] or 0
        operation_summary[op_type] = total
    
    # Get material summary
    material_summary = (
        queryset
        .values('material__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    
    # Define columns to export
    columns = ['date', 'shift', 'area', 'operation_type', 'material', 'quantity']
    
    # Build filename with filters
    filename = 'RMHS_Operations'
    if date:
        filename += f'_{date}'
    elif date_from and date_to:
        filename += f'_{date_from}_to_{date_to}'
    elif date_from:
        filename += f'_from_{date_from}'
    elif date_to:
        filename += f'_to_{date_to}'
        
    if shift:
        filename += f'_Shift_{shift}'
    if area:
        filename += f'_{area}'
    if operation_type:
        filename += f'_{operation_type}'
    
    # Generate title based on filters
    title = "Operations Report"
    if date:
        title += f" for {date}"
    elif date_from and date_to:
        title += f" from {date_from} to {date_to}"
    elif date_from:
        title += f" from {date_from}"
    elif date_to:
        title += f" to {date_to}"
    
    if shift:
        title += f" - Shift {shift}"
    if area:
        title += f" - {area}"
    if operation_type:
        title += f" - {operation_type.title()}"
    
    # Export to PDF
    return export_to_pdf(
        queryset, 
        filename, 
        columns, 
        title=title,
        material_summary=material_summary,
        operation_summary=operation_summary
    )

@login_required
def dashboard(request):
    """Display the main dashboard page with summary of operations"""
    # Get filter parameters from request
    date_str = request.GET.get('date')
    shift = request.GET.get('shift')
    area = request.GET.get('area')
    operation_type = request.GET.get('operation_type')
    
    # Default to today if date not provided
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()
    
    # Create filter form with initial values
    form = FilterForm(request.GET or None, initial={
        'date': date,
        'shift': shift if shift else '',
        'area': area if area else '',
        'operation_type': operation_type if operation_type else '',
    })
    
    # Build base queryset with date filter
    operations = Operation.objects.filter(date=date)
    
    # Apply additional filters if provided
    if shift:
        operations = operations.filter(shift=shift)
    if area:
        operations = operations.filter(area=area)
    
    # Create a filtered operations queryset for specific operation type
    filtered_operations = operations
    if operation_type:
        # Make sure operation type filtering is case-insensitive
        filtered_operations = operations.filter(operation_type__iexact=operation_type)
        
    # Get operation summary by type - FIXED CALCULATION
    operation_summary = {}
    
    # Always calculate totals for all operation types to display in cards
    for op_type, _ in OPERATION_TYPES:
        # If filter is applied, only show amounts for the selected type
        if operation_type and op_type.lower() != operation_type.lower():
            operation_summary[op_type.lower()] = 0
        else:
            total = operations.filter(operation_type__iexact=op_type).aggregate(sum=Sum('quantity'))['sum'] or 0
            operation_summary[op_type.lower()] = total
    
    # Get material summary based on filtered operations
    material_summary = (
        filtered_operations
        .values('material__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    
    # Get recent activities based on filtered operations
    recent_operations = filtered_operations.order_by('-created_at')[:10]
    
    # Prepare context
    context = {
        'form': form,
        'date': date,
        'operations': filtered_operations,
        'operation_summary': operation_summary,
        'material_summary': material_summary,
        'recent_operations': recent_operations,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def daily_summary(request):
    """Function-based view for daily summary"""
    # Get filter parameters
    date_str = request.GET.get('date')
    area = request.GET.get('area')
    operation_type = request.GET.get('operation_type')
    
    # Default to today if date not provided
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date = timezone.now().date()
    else:
        date = timezone.now().date()
    
    # Create filter form with request data
    form = FilterForm(request.GET or None, initial={
        'date': date,
        'area': area if area else '',
        'operation_type': operation_type if operation_type else '',
    })
    
    # Base queryset
    queryset = Operation.objects.filter(date=date)
    
    # Apply filters
    if area:
        queryset = queryset.filter(area=area)
    if operation_type:
        queryset = queryset.filter(operation_type__iexact=operation_type)
    
    # Get operation summary by type
    operation_summary = {}
    for op_type, _ in OPERATION_TYPES:
        total = queryset.filter(operation_type=op_type).aggregate(sum=Sum('quantity'))['sum'] or 0
        operation_summary[op_type] = total
    
    # Get material summary
    material_summary = (
        queryset
        .values('material__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    
    # Prepare context
    context = {
        'form': form,
        'date': date,
        'operation_summary': operation_summary,
        'material_summary': material_summary,
    }
    
    return render(request, 'dashboard/daily_summary.html', context)

@login_required
def operations_list(request):
    """Function-based view for operations list"""
    # Get filter parameters
    date_str = request.GET.get('date')
    date_from_str = request.GET.get('date_from')
    date_to_str = request.GET.get('date_to')
    shift = request.GET.get('shift')
    area = request.GET.get('area')
    operation_type = request.GET.get('operation_type')
    
    # Check if any date filter is applied
    any_date_filter = date_str or date_from_str or date_to_str
    
    # Parse dates
    date = None
    date_from = None
    date_to = None
    
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if date_from_str:
        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    if date_to_str:
        try:
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        except ValueError:
            pass
    
    # Base queryset
    queryset = Operation.objects.all()
    
    # If no date filter is applied, default to today's operations
    if not any_date_filter:
        today = timezone.now().date()
        queryset = queryset.filter(date=today)
        # Set today as the default date for context
        date = today
    else:
        # Apply filters
        if date:
            queryset = queryset.filter(date=date)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
    
    # Apply other filters
    if shift:
        queryset = queryset.filter(shift=shift)
    if area:
        queryset = queryset.filter(area=area)
    if operation_type:
        queryset = queryset.filter(operation_type__iexact=operation_type)
    
    # Create filter form
    filter = OperationFilter(request.GET, queryset=queryset)
    queryset = filter.qs
    
    # Get operation summary
    operation_summary = {}
    for op_type, _ in OPERATION_TYPES:
        total = queryset.filter(operation_type=op_type).aggregate(sum=Sum('quantity'))['sum'] or 0
        operation_summary[op_type] = total
    
    # Get material summary
    material_summary = (
        queryset
        .values('material__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')
    )
    
    context = {
        'operations': queryset.order_by('-date', 'shift'),
        'filter': filter,
        'operation_summary': operation_summary,
        'material_summary': material_summary,
        'page_title': 'Operations List',
        'today': timezone.now().date().strftime('%Y-%m-%d'),
    }
    
    return render(request, 'dashboard/operation_list.html', context)

@login_required
def add_feeding_operation(request):
    """Add a new feeding operation"""
    if request.method == 'POST':
        form = FeedingOperationForm(request.POST)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create destination
            destination_name = form.cleaned_data.pop('destination_name', None)
            destination = None
            if destination_name:
                destination, created = Destination.objects.get_or_create(name=destination_name)
            
            # Create operation
            operation = form.save(commit=False)
            operation.material = material
            operation.destination = destination
            operation.save()
            
            messages.success(request, 'Feeding operation added successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = FeedingOperationForm(initial={
            'date': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'page_title': 'Add Feeding Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def edit_feeding_operation(request, pk):
    """Edit an existing feeding operation"""
    operation = get_object_or_404(FeedingOperation, pk=pk)
    
    if request.method == 'POST':
        form = FeedingOperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create destination
            destination_name = form.cleaned_data.pop('destination_name', None)
            destination = None
            if destination_name:
                destination, created = Destination.objects.get_or_create(name=destination_name)
            
            # Update operation
            operation = form.save(commit=False)
            operation.material = material
            operation.destination = destination
            operation.save()
            
            messages.success(request, 'Feeding operation updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = FeedingOperationForm(instance=operation, initial={
            'material_name': operation.material.name,
            'destination_name': operation.destination.name if operation.destination else '',
        })
    
    context = {
        'form': form,
        'operation': operation,
        'page_title': 'Edit Feeding Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def delete_feeding_operation(request, pk):
    """Delete a feeding operation"""
    operation = get_object_or_404(FeedingOperation, pk=pk)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Feeding operation deleted successfully.')
        return redirect('dashboard:dashboard')
    
    context = {
        'operation': operation,
        'page_title': 'Delete Feeding Operation',
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)

@login_required
def add_stacking_operation(request):
    """Add a new stacking operation"""
    if request.method == 'POST':
        form = StackingOperationForm(request.POST)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Create operation
            operation = form.save(commit=False)
            operation.material = material
            operation.save()
            
            messages.success(request, 'Stacking operation added successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = StackingOperationForm(initial={
            'date': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'page_title': 'Add Stacking Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def edit_stacking_operation(request, pk):
    """Edit an existing stacking operation"""
    operation = get_object_or_404(StackingOperation, pk=pk)
    
    if request.method == 'POST':
        form = StackingOperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Update operation
            operation = form.save(commit=False)
            operation.material = material
            operation.save()
            
            messages.success(request, 'Stacking operation updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = StackingOperationForm(instance=operation, initial={
            'material_name': operation.material.name,
        })
    
    context = {
        'form': form,
        'operation': operation,
        'page_title': 'Edit Stacking Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def delete_stacking_operation(request, pk):
    """Delete a stacking operation"""
    operation = get_object_or_404(StackingOperation, pk=pk)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Stacking operation deleted successfully.')
        return redirect('dashboard:dashboard')
    
    context = {
        'operation': operation,
        'page_title': 'Delete Stacking Operation',
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)

@login_required
def add_reclaiming_operation(request):
    """Add a new reclaiming operation"""
    if request.method == 'POST':
        form = ReclaimingOperationForm(request.POST)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create source
            source_name = form.cleaned_data.pop('source_name', None)
            source = None
            if source_name:
                source, created = Source.objects.get_or_create(name=source_name)
            
            # Create operation
            operation = form.save(commit=False)
            operation.material = material
            operation.source = source
            operation.save()
            
            messages.success(request, 'Reclaiming operation added successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = ReclaimingOperationForm(initial={
            'date': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'page_title': 'Add Reclaiming Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def edit_reclaiming_operation(request, pk):
    """Edit an existing reclaiming operation"""
    operation = get_object_or_404(ReclaimingOperation, pk=pk)
    
    if request.method == 'POST':
        form = ReclaimingOperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create source
            source_name = form.cleaned_data.pop('source_name', None)
            source = None
            if source_name:
                source, created = Source.objects.get_or_create(name=source_name)
            
            # Update operation
            operation = form.save(commit=False)
            operation.material = material
            operation.source = source
            operation.save()
            
            messages.success(request, 'Reclaiming operation updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = ReclaimingOperationForm(instance=operation, initial={
            'material_name': operation.material.name,
            'source_name': operation.source.name if operation.source else '',
        })
    
    context = {
        'form': form,
        'operation': operation,
        'page_title': 'Edit Reclaiming Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def delete_reclaiming_operation(request, pk):
    """Delete a reclaiming operation"""
    operation = get_object_or_404(ReclaimingOperation, pk=pk)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Reclaiming operation deleted successfully.')
        return redirect('dashboard:dashboard')
    
    context = {
        'operation': operation,
        'page_title': 'Delete Reclaiming Operation',
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)

@login_required
def add_receiving_operation(request):
    """Add a new receiving operation"""
    if request.method == 'POST':
        form = ReceivingOperationForm(request.POST)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create source
            source_name = form.cleaned_data.pop('source_name', None)
            source = None
            if source_name:
                source, created = Source.objects.get_or_create(name=source_name)
            
            # Create operation
            operation = form.save(commit=False)
            operation.material = material
            operation.source = source
            operation.save()
            
            messages.success(request, 'Receiving operation added successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = ReceivingOperationForm(initial={
            'date': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'page_title': 'Add Receiving Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def edit_receiving_operation(request, pk):
    """Edit an existing receiving operation"""
    operation = get_object_or_404(ReceivingOperation, pk=pk)
    
    if request.method == 'POST':
        form = ReceivingOperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Get or create source
            source_name = form.cleaned_data.pop('source_name', None)
            source = None
            if source_name:
                source, created = Source.objects.get_or_create(name=source_name)
            
            # Update operation
            operation = form.save(commit=False)
            operation.material = material
            operation.source = source
            operation.save()
            
            messages.success(request, 'Receiving operation updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = ReceivingOperationForm(instance=operation, initial={
            'material_name': operation.material.name,
            'source_name': operation.source.name if operation.source else '',
        })
    
    context = {
        'form': form,
        'operation': operation,
        'page_title': 'Edit Receiving Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def delete_receiving_operation(request, pk):
    """Delete a receiving operation"""
    operation = get_object_or_404(ReceivingOperation, pk=pk)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Receiving operation deleted successfully.')
        return redirect('dashboard:dashboard')
    
    context = {
        'operation': operation,
        'page_title': 'Delete Receiving Operation',
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)

@login_required
def add_crushing_operation(request):
    """Add a new crushing operation"""
    if request.method == 'POST':
        form = CrushingOperationForm(request.POST)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Create operation
            operation = form.save(commit=False)
            operation.material = material
            operation.save()
            
            messages.success(request, 'Crushing operation added successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = CrushingOperationForm(initial={
            'date': timezone.now().date(),
        })
    
    context = {
        'form': form,
        'page_title': 'Add Crushing Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def edit_crushing_operation(request, pk):
    """Edit an existing crushing operation"""
    operation = get_object_or_404(CrushingOperation, pk=pk)
    
    if request.method == 'POST':
        form = CrushingOperationForm(request.POST, instance=operation)
        if form.is_valid():
            # Get or create material
            material_name = form.cleaned_data.pop('material_name')
            material, created = Material.objects.get_or_create(name=material_name)
            
            # Update operation
            operation = form.save(commit=False)
            operation.material = material
            operation.save()
            
            messages.success(request, 'Crushing operation updated successfully.')
            return redirect('dashboard:dashboard')
    else:
        form = CrushingOperationForm(instance=operation, initial={
            'material_name': operation.material.name,
        })
    
    context = {
        'form': form,
        'operation': operation,
        'page_title': 'Edit Crushing Operation',
    }
    return render(request, 'dashboard/operation_form.html', context)

@login_required
def delete_crushing_operation(request, pk):
    """Delete a crushing operation"""
    operation = get_object_or_404(CrushingOperation, pk=pk)
    
    if request.method == 'POST':
        operation.delete()
        messages.success(request, 'Crushing operation deleted successfully.')
        return redirect('dashboard:dashboard')
    
    context = {
        'operation': operation,
        'page_title': 'Delete Crushing Operation',
    }
    return render(request, 'dashboard/operation_confirm_delete.html', context)

from django.db import models
from django.utils import timezone

# Area choices
AREA_CHOICES = [
    ('area-1', 'Area-1'),
    ('area-2&3', 'Area-2&3'),
]

# Shift choices
SHIFT_CHOICES = [
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
]

# Operation types
OPERATION_TYPES = [
    ('feeding', 'Feeding'),
    ('stacking', 'Stacking'),
    ('reclaiming', 'Reclaiming'),
    ('receiving', 'Receiving'),
    ('crushing', 'Crushing'),
]

class Material(models.Model):
    """Model to store material types"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Destination(models.Model):
    """Model to store destinations (Blast Furnace, Sinter Plant, SMS, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Source(models.Model):
    """Model to store sources for reclaiming operations"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Operation(models.Model):
    """Base model for all operations"""
    date = models.DateField(default=timezone.now)
    shift = models.CharField(max_length=1, choices=SHIFT_CHOICES)
    area = models.CharField(max_length=10, choices=AREA_CHOICES)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='operations')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES)
    source = models.ForeignKey(Source, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations')
    reported_by = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.operation_type.title()} - {self.material} ({self.quantity} MT) - {self.date} {self.shift}"

    class Meta:
        ordering = ['-date', 'shift']

class FeedingOperation(Operation):
    """Model for Feeding operations"""
    
    def save(self, *args, **kwargs):
        self.operation_type = 'feeding'
        super().save(*args, **kwargs)

class StackingOperation(Operation):
    """Model for Stacking operations"""
    
    def save(self, *args, **kwargs):
        self.operation_type = 'stacking'
        super().save(*args, **kwargs)

class ReclaimingOperation(Operation):
    """Model for Reclaiming operations"""
    
    def save(self, *args, **kwargs):
        self.operation_type = 'reclaiming'
        super().save(*args, **kwargs)

class ReceivingOperation(Operation):
    """Model for Receiving operations"""
    
    def save(self, *args, **kwargs):
        self.operation_type = 'receiving'
        super().save(*args, **kwargs)

class CrushingOperation(Operation):
    """Model for Crushing operations"""
    crushing_details = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.operation_type = 'crushing'
        super().save(*args, **kwargs)

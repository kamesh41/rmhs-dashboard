from django.db import models
from datetime import timedelta

# Choices for tipplers
TIPPLER_CHOICES = [
    ('WT-1', 'Wagon Tippler 1'),
    ('WT-2', 'Wagon Tippler 2'),
    ('WT-3', 'Wagon Tippler 3'),
    ('WT-4', 'Wagon Tippler 4'),
]

# Choices for rake status
RAKE_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('progress', 'In Progress'),
    ('complete', 'Completed'),
]

class Rake(models.Model):
    """Model for tracking wagon tipplers"""
    rake_id = models.CharField(max_length=50, unique=True, help_text="Unique ID for the rake")
    tippler = models.CharField(max_length=4, choices=TIPPLER_CHOICES)
    rake_in_time = models.DateTimeField(help_text="Time when rake entered the system")
    rake_completed_time = models.DateTimeField(null=True, blank=True, help_text="Time when rake processing was completed")
    rake_status = models.CharField(max_length=10, choices=RAKE_STATUS_CHOICES, default='pending')
    rake_type = models.CharField(max_length=50, help_text="Type of rake (e.g., BOXN, BOY)")
    rake_material = models.CharField(max_length=100, help_text="Material carried by the rake")
    reported_by = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.rake_id} - {self.tippler} - {self.rake_status}"
    
    @property
    def time_taken(self):
        """Calculate the time taken to process the rake"""
        if self.rake_completed_time and self.rake_in_time:
            time_diff = self.rake_completed_time - self.rake_in_time
            hours = time_diff.total_seconds() // 3600
            minutes = (time_diff.total_seconds() % 3600) // 60
            return f"{int(hours)}h {int(minutes)}m"
        return "-"
    
    class Meta:
        ordering = ['-rake_in_time']

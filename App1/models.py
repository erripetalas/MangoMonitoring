from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farms")

    def __str__(self):
        return self.name

class Pest(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Surveillance(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='surveillance_records')
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE, related_name='occurrences')
    date_observed = models.DateField()
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.farm.name} - {self.pest.name} ({self.date_observed})"


"""
Key changes:
Added owner field to Farm model to link each farm to a specific user
Added related_name attributes for more intuitive reverse lookups
Added SEVERITY_CHOICES to make the surveillance record's severity more meaningful
Fixed the string representation for Surveillance (changed self.date to self.date_observed)
"""


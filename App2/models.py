from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Farm(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="farms")
    total_plants = models.IntegerField(validators=[MinValueValidator(1)], help_text="Total number of mango plants on the property")
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Farm size in hectares")
    stocking_rate = models.DecimalField(max_digits=10, decimal_places=2, help_text="Plants per hectare", editable=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.farm_size > 0:
            self.stocking_rate = self.total_plants / self.farm_size
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"

    class Meta:
        ordering = ['name']


class PlantLocation(models.Model):
    """Specific locations within a farm for surveillance"""
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100, help_text="e.g., North Block, Section A")
    description = models.TextField(blank=True, help_text="Additional location details")
    number_of_plants = models.IntegerField(validators=[MinValueValidator(1)])
    
    def __str__(self):
        return f"{self.farm.name} - {self.name}"

    class Meta:
        unique_together = ['farm', 'name']


class Pest(models.Model):
    """User-identified pests during surveillance"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    reference_pest_id = models.IntegerField(null=True, blank=True,help_text="ID from reference pest database if identified")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.name


class Surveillance(models.Model):
    SEVERITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        (4, 'Critical'),
    ]
    
    PLANT_PART_CHOICES = [
        ('leaves', 'Leaves'),
        ('fruit', 'Fruit'),
        ('flowers', 'Flowers'),
        ('stem', 'Stem/Branches'),
        ('roots', 'Roots'),
        ('whole', 'Whole Plant'),
    ]
    
    # Core fields
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='surveillance_records')
    location = models.ForeignKey(PlantLocation, on_delete=models.SET_NULL, null=True,related_name='surveillance_records')
    date_observed = models.DateField()
    time_observed = models.TimeField()
    
    # Surveillance details
    plants_inspected = models.IntegerField(validators=[MinValueValidator(1)],help_text="Number of plants inspected in this surveillance")
    plant_part = models.CharField(max_length=20, choices=PLANT_PART_CHOICES)
    
    # Pest information
    pest = models.ForeignKey(Pest, on_delete=models.CASCADE, related_name='occurrences')
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    pest_count = models.IntegerField(default=0, help_text="Estimated number of pests found")
    
    # Additional information
    notes = models.TextField(blank=True)
    weather_conditions = models.CharField(max_length=100, blank=True, help_text="e.g., Sunny, Rainy, Humid")
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farm.name} - {self.pest.name} ({self.date_observed})"
    
    class Meta:
        ordering = ['-date_observed', '-time_observed']

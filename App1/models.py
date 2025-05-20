# from django.db import models

# class Farm(models.Model):
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=150)

#     def __str__(self):
#         return self.name

# class Pest(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class Surveillance(models.Model):
#     farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
#     pest = models.ForeignKey(Pest, on_delete=models.CASCADE)
#     date_observed = models.DateField()
#     severity = models.IntegerField()
#     notes = models.TextField(blank=True)

#     def __str__(self):
#         return f"{self.farm.name} - {self.pest.name} ({self.date})"

from django.db import models


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='fas fa-folder')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    department = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
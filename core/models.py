from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CITIZEN = 'C'
    STAFF = 'S'
    ADMIN = 'A'
    ROLE_CHOICES = [
        (CITIZEN, 'Citizen'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin')
    ]
    
    role = models.CharField(max_length=1, choices=ROLE_CHOICES, default=CITIZEN)
    id_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.username
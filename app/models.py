from django.db import models
from django.contrib.auth.models import AbstractUser


class DXVLUsers(AbstractUser):
    user_address = models.CharField(max_length=255, blank=True)
    user_mobile_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'dxvl_users'
        verbose_name = 'DXVL User'

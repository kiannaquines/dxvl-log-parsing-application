from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class DXVLUsers(AbstractUser):
    user_address = models.CharField(max_length=255, blank=True)
    user_mobile_number = models.CharField(max_length=15, blank=True)
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        db_table = 'dxvl_users'
        verbose_name = 'DXVL User'


class DXVLLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    date_aired = models.DateTimeField(auto_now=False,null=False, blank=False)
    artist = models.CharField(max_length=255, blank=True)
    advertisement = models.CharField(max_length=255, blank=True)
    added_by = models.ForeignKey(DXVLUsers, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.date_aired)
    
    class Meta:
        db_table = 'dxvl_aired_logs'
        verbose_name = 'DXVL Log'
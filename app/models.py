from django.db import models
from django.contrib.auth.models import AbstractUser

class DXVLUsers(AbstractUser):
    user_address = models.CharField(max_length=255, blank=True,null=True)
    user_mobile_number = models.CharField(max_length=15, blank=True,null=True)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        db_table = 'dxvl_users'
        verbose_name = 'DXVL User'


class DXVLLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    date_aired = models.DateTimeField(auto_now=False,null=False, blank=False)
    artist = models.CharField(max_length=255, blank=True)
    advertisement = models.CharField(max_length=255, blank=True)
    added_by = models.ForeignKey(DXVLUsers, on_delete=models.CASCADE,editable=False)
    status = models.BooleanField(default=True)
    remarks = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.date_aired)
    
    class Meta:
        db_table = 'dxvl_aired_logs'
        verbose_name = 'DXVL Log'

class DXVLLogNames(models.Model):
    file_name = models.CharField(max_length=255, blank=True)
    file_lines = models.IntegerField(default=0)
    file_state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.file_name
    
    class Meta:
        db_table = 'dxvl_log_filenames'
        verbose_name = 'DXVL Log File Name'

class DXVLAdvertisementPrices(models.Model):
    price = models.FloatField()
    advertisement = models.CharField(max_length=255, blank=True)


    def __str__(self) -> str:
        return f'Advertisement {self.advertisement} price: {self.price}'
    
    class Meta:
        db_table = 'dxvl_advertisement_prices'
        verbose_name = 'DXVL Advertisement Price'
from django.db import models
from django.contrib.auth.models import AbstractUser


class SearchKeyWords(models.Model):
    keyword = models.CharField(max_length=255, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Advertisement Search Keyword'
        verbose_name_plural = 'Advertisement Search Keywords'
        
    def __str__(self):
        return self.keyword


class DXVLUsers(AbstractUser):
    user_address = models.TextField(max_length=255, blank=True,null=True)
    user_mobile_number = models.CharField(max_length=15, blank=True,null=True)
    
    def __str__(self) -> str:
        return self.username
    
    class Meta:
        db_table = 'dxvl_users'
        verbose_name = 'DXVL User'

class DXVLLogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    date_aired = models.DateTimeField(auto_now=False,null=False, blank=False)
    artist = models.CharField(max_length=255, blank=True, db_index=True)
    advertisement = models.CharField(max_length=255, blank=True, db_index=True)
    added_by = models.ForeignKey(DXVLUsers, on_delete=models.CASCADE,editable=False)
    status = models.BooleanField(default=True)
    remarks = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self) -> str:
        return str(self.advertisement)
    
    class Meta:
        db_table = 'dxvl_aired_logs'
        verbose_name = 'DXVL Log'
        ordering = ['advertisement', 'date_aired']
        
class DXVLLogNames(models.Model):
    file_name = models.CharField(max_length=255, blank=True)
    file_lines = models.IntegerField(default=0)
    file_state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.file_name
    
    class Meta:
        db_table = 'dxvl_log_filenames'
        verbose_name = 'DXVL Log File Name'

class Advertisements(models.Model):
    advertisement_id = models.AutoField(primary_key=True,unique=True, editable=False)
    advertisement_name = models.CharField(max_length=255,unique=True,null=True,blank=True)
    advertisement_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.advertisement_name
    
    class Meta:
        db_table = 'dxvl_advertisements'
        verbose_name = 'DXVL Advertisement'
        verbose_name_plural = 'DXVL Advertisements'
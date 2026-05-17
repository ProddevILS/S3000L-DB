from django.db import models
class BackupLog(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    backup_file=models.CharField(max_length=500)
    status=models.CharField(max_length=30)
    message=models.TextField(blank=True)
    class Meta: ordering=['-created_at']
    def __str__(self): return f'{self.created_at:%Y-%m-%d %H:%M} {self.status}'

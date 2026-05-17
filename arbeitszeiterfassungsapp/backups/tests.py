from django.contrib.auth.models import User
from django.test import TestCase
from .models import BackupLog
class BackupTests(TestCase):
    def test_backup_creation(self):
        User.objects.create_user('u',password='pw'); self.client.login(username='u',password='pw')
        r=self.client.post('/backups/create/')
        self.assertEqual(r.status_code,302); self.assertTrue(BackupLog.objects.exists())

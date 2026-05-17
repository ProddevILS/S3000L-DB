import shutil
from pathlib import Path
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone
from .models import BackupLog
@login_required
def backup_home(request): return render(request,'backups/home.html',{'logs':BackupLog.objects.all()[:20]})
@login_required
def create_backup(request):
    folder=Path(settings.BASE_DIR)/'backups'; folder.mkdir(exist_ok=True)
    target=folder/f'db_backup_{timezone.now():%Y%m%d_%H%M%S}.sqlite3'
    try:
        shutil.copy2(settings.DATABASES['default']['NAME'], target); BackupLog.objects.create(backup_file=str(target),status='success',message='Backup erstellt')
    except Exception as exc:
        BackupLog.objects.create(backup_file=str(target),status='error',message=str(exc))
    return redirect('backups:home')

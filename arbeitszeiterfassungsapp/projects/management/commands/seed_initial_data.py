from django.core.management.base import BaseCommand
from arbeitszeiterfassungsapp.customers.models import Customer
from arbeitszeiterfassungsapp.projects.models import ActivityType, Project
class Command(BaseCommand):
    help='Legt initiale Tätigkeitsarten, Beispielkunde und Beispielprojekt an.'
    def handle(self,*args,**opts):
        names=[('Beratung',True),('Dokumentation',True),('Analyse',True),('Entwicklung',True),('Fahrzeit',True),('Interne Tätigkeit',False),('Pause',False),('Sonstiges',True)]
        for name,bill in names: ActivityType.objects.get_or_create(name=name,defaults={'billable_default':bill,'unit':'Stunde'})
        c,_=Customer.objects.get_or_create(short_name='DEMO',defaults={'name':'Beispielkunde'})
        Project.objects.get_or_create(customer=c,short_name='DEMO-P',defaults={'name':'Beispielprojekt','billable':True})
        self.stdout.write(self.style.SUCCESS('Seed-Daten erstellt.'))

import csv, io
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from arbeitszeiterfassungsapp.time_tracking.models import TimeEntry
from arbeitszeiterfassungsapp.time_tracking.services import employee_for_user

def filtered(request):
    qs=TimeEntry.objects.filter(employee=employee_for_user(request.user),status='completed').select_related('customer','project','activity_type')
    if request.GET.get('from'): qs=qs.filter(date__gte=request.GET['from'])
    if request.GET.get('to'): qs=qs.filter(date__lte=request.GET['to'])
    if request.GET.get('customer'): qs=qs.filter(customer_id=request.GET['customer'])
    if request.GET.get('project'): qs=qs.filter(project_id=request.GET['project'])
    if request.GET.get('activity_type'): qs=qs.filter(activity_type_id=request.GET['activity_type'])
    if request.GET.get('billable') in ['0','1']: qs=qs.filter(billable=request.GET['billable']=='1')
    return qs
@login_required
def exports_home(request): return render(request,'exports/home.html')
def rows(qs):
    for e in qs:
        yield [e.customer.name, e.project.name if e.project else '', e.date, e.start_datetime.strftime('%H:%M'), e.end_datetime.strftime('%H:%M') if e.end_datetime else '', f'{e.duration_hours:.2f}', e.activity_type.name, e.description, e.hourly_rate or 0, e.amount_net]
@login_required
def invoice_export(request, fmt):
    qs=filtered(request); headers=['Kunde','Projekt','Datum','Start','Ende','Dauer','Tätigkeit','Beschreibung','Stundensatz','Betrag netto']
    if fmt=='csv':
        resp=HttpResponse(content_type='text/csv'); resp['Content-Disposition']='attachment; filename="rechnungsanhang.csv"'; w=csv.writer(resp); w.writerow(headers); w.writerows(rows(qs)); return resp
    if fmt=='xlsx':
        wb=Workbook(); ws=wb.active; ws.title='Rechnungsanhang'; ws.append(headers)
        for r in rows(qs): ws.append(r)
        buf=io.BytesIO(); wb.save(buf); resp=HttpResponse(buf.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'); resp['Content-Disposition']='attachment; filename="rechnungsanhang.xlsx"'; return resp
    resp=HttpResponse(content_type='application/pdf'); resp['Content-Disposition']='attachment; filename="rechnungsanhang.pdf"'; p=canvas.Canvas(resp,pagesize=A4); y=800; p.drawString(40,y,'Rechnungsanhang / Leistungsnachweis'); y-=30
    total_h=Decimal('0'); total_a=Decimal('0')
    for e in qs:
        if y<80: p.showPage(); y=800
        p.drawString(40,y,f'{e.date} {e.customer.name} {e.project.name if e.project else ""} {e.duration_hours:.2f}h {e.activity_type.name} {e.amount_net} EUR'); y-=18; total_h+=e.duration_hours; total_a+=e.amount_net
    y-=20; p.drawString(40,y,f'Gesamt: {total_h:.2f} Stunden / {total_a:.2f} EUR netto'); y-=50; p.drawString(40,y,'Unterschrift / Freigabe: ______________________________'); p.showPage(); p.save(); return resp
@login_required
def lexware_csv(request):
    qs=filtered(request); resp=HttpResponse(content_type='text/csv'); resp['Content-Disposition']='attachment; filename="lexware_preparation.csv"'; w=csv.writer(resp); w.writerow(['Kunde','Projekt','Leistungsdatum','Beschreibung','Menge Stunden','Einzelpreis netto','Gesamtpreis netto','Tätigkeitsart','interne Referenz','Bemerkung'])
    for e in qs: w.writerow([e.customer.name,e.project.name if e.project else '',e.date,e.description,f'{e.duration_hours:.2f}',e.hourly_rate or 0,e.amount_net,e.activity_type.name,f'TE-{e.pk}','Vorbereitungsdatei, kein garantierter Direktimport'])
    return resp

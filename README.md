# arbeitszeiterfassungsapp

Lokale Django-Web-App als MVP zur Arbeitszeiterfassung, projektbezogenen Auswertung und Abrechnungsvorbereitung für zunächst eine Einzelperson. Die Daten bleiben lokal in SQLite; die Struktur ist auf spätere Mehr-Mitarbeiter-Nutzung vorbereitet.

## Funktionsumfang MVP

- Login/Logout über Django Auth und Mitarbeiterprofil (`Employee`) mit vorbereiteten Rollen Admin/Mitarbeiter.
- Kundenverwaltung mit Anlegen, Bearbeiten, Anzeigen und Deaktivieren statt Löschen.
- Projektverwaltung mit Kunde, Auftragsnummer, Standard-Stundensätzen, Fahrtzeit-Satz, Abrechenbarkeit und Aktiv-Status.
- Tätigkeitsarten inkl. Seed-Daten: Beratung, Dokumentation, Analyse, Entwicklung, Fahrzeit, Interne Tätigkeit, Pause, Sonstiges.
- Zeiterfassung per Start-/Stopp-Buttons, Pause starten/beenden und Projektwechsel.
- Manuelle Zeitbuchungen inkl. Validierung von Start/Ende, Projekt/Kunde und Überschneidungswarnung mit expliziter Bestätigung.
- Audit-Log bei Änderungen an Zeitbuchungen mit optionalem Änderungsgrund.
- Berechnung von Minuten, Dezimalstunden und Nettobetrag.
- Auswertungen für Tag, Woche, Monat sowie gefilterte Kunden-/Projektübersicht.
- Rechnungsanhang-Export als PDF, Excel und CSV.
- Lexware-Office-Vorbereitungsdatei `lexware_preparation.csv` ohne direkte API-Anbindung.
- Lokale SQLite-Backup-Funktion in den Ordner `backups/` inkl. `BackupLog`.
- Responsive Bootstrap-Oberfläche mit großen Buttons für mobile Bedienung und PWA-vorbereitenden Meta-Tags.

## Installation unter Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_initial_data
python manage.py runserver 0.0.0.0:8000
```

Danach lokal öffnen: <http://127.0.0.1:8000/>

## Zugriff vom Smartphone im lokalen Netzwerk

1. Linux-Rechner-IP ermitteln, z. B. `ip addr`.
2. Server mit `python manage.py runserver 0.0.0.0:8000` starten.
3. Smartphone im selben WLAN öffnen: `http://<IP-DES-RECHNERS>:8000/`.

## Backup-Hinweise

Über **Backup → Backup erstellen** wird die SQLite-Datei nach `backups/db_backup_<timestamp>.sqlite3` kopiert. Für automatische Backups kann ein Cronjob verwendet werden, z. B. täglich um 22:00 Uhr:

```cron
0 22 * * * cd /pfad/zur/arbeitszeiterfassungsapp && . .venv/bin/activate && python manage.py shell -c "from django.test import Client; print('Für Cron in einer späteren Version als Management Command ausbauen')"
```

Im MVP ist der Button der primäre Weg. Für produktive Nutzung sollte ein eigenes Management Command für Headless-Backups ergänzt werden.

## Export-Hinweise

Die Exportseite bietet:

- `rechnungsanhang.pdf`
- `rechnungsanhang.xlsx`
- `rechnungsanhang.csv`
- `lexware_preparation.csv`

Filter können als Query-Parameter genutzt werden: `from`, `to`, `customer`, `project`, `activity_type`, `billable`.

## Tests

```bash
python manage.py test
```

Abgedeckt sind Start/Stopp, Pause, Projektwechsel, manuelle Buchung, Dauer- und Stundensatzlogik, Exportfilter, Audit-Log und Backup-Erstellung.

## Bekannte Einschränkungen des MVP

- Keine komplexe Rechteverwaltung; Rollen sind im Datenmodell vorbereitet.
- Keine direkte Lexware-Office-API-Anbindung.
- PDF-Layout ist bewusst schlicht.
- Projektfilter in Formularen sind serverseitig validiert; dynamische abhängige Dropdowns können später ergänzt werden.
- Keine echte PWA-Installation; Oberfläche und Meta-Tags sind vorbereitet.
- Backup-Automatisierung ist dokumentiert, aber noch nicht als Management Command umgesetzt.

## Projektstruktur

Die gewünschte App-Struktur wurde umgesetzt:

- `accounts`
- `customers`
- `projects`
- `time_tracking`
- `reporting`
- `exports`
- `backups`

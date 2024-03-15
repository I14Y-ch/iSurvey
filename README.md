# iSurvey

Willkommen im iSurvey Repository! Dieses Repository bietet Ihnen die Werkzeuge, um Kataloge der I14Y-Interoperabilitätsplattform als Fragebogen-Sets in LimeSurvey zu verwenden.

## Überblick

iSurvey zielt darauf ab, die Erstellung und Verwaltung von Umfragen in LimeSurvey zu vereinfachen, indem es eine direkte Integration mit den Katalogen der I14Y-Interoperabilitätsplattform ermöglicht. Mit diesem Tool können Sie effizienter arbeiten, Fehler reduzieren und die Aktualisierung Ihrer Datenbestände optimieren.

## Setup
Passe die Anmeldedaten für den LimeSurvey Administrator in der docker-compose.yml an.
Um mit iSurvey zu beginnen, folgen Sie diesen Schritten:

1. Stellen Sie sicher, dass Docker auf Ihrem System installiert ist.
2. Klonen Sie dieses Repository auf Ihren lokalen Computer.
3. Starten Sie die Anwendung mit Docker-Compose:

```bash
docker-compose build
docker-compose up -d
```
## LimeSurvey
1. Gehe in den Admin-Bereich: http://localhost:8082/index.php/admin/index
2. @Todo aktivieren Plugin oder importiere die Datei Fooo unter Fiii.
3. Definiere alle Sprachen in Deiner Umfrage bevor Du importierte Antwort/Auswahl Sets benutzt.

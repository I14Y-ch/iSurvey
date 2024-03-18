# iSurvey -- die Brücke zwischen I14Y und Limesurvey
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/I14Y-ch/iSurvey)

Auf der [I14Y-Interoperabilitätsplattform](https://i14y.admin.ch) sind harmonisierte und standardisierte Codelisten der Schweizer Behörden erhältlich. Diese sollen in der quelloffenen Umfragesoftware [Limesurvey](https://limesurvey.org) auf einfache Weise genutzt werden können. Der Prototyp iSurvey versucht diese Brücke zu schlagen. Entwickelt wurde er im Rahmen des [GovTech-Hackathons 2024](https://www.bk.admin.ch/bk/de/home/digitale-transformation-ikt-lenkung/bundesarchitektur/api-architektur-bund/govtech-hackathon24.html).  

iSurvey ruft die öffentlich verfügbaren Codelisten von der I14Y-Interoperabilitätsplattform ab, so dass sich die Listen mit wenigen Klicks in eine Umfrage einbauen lassen. Dadurch können Umfragen rascher erstellt werden. Und es entstehen nachträglich weniger Probleme aufgrund abweichender Codierungen. 

iSurvey besteht aus einem [Plugin für Limesurvey](https://github.com/I14Y-ch/iSurvey/tree/main/I14Y%20LimeSurvey%20Plugin) und einigen Skripten, mit denen die Codelisten bezogen und aufbereitet werden. Dank Docker-Containern und einer detaillierten Anleitung lässt sich Limesurvey inklusive des Plugins iSurvey innert weniger Minuten installieren. 

## Installation 

### Öffnen in Github-Codespaces

Wer Limesurvey mit dem I14Y-Plugin kurz ausprobieren möchte, nutzt dazu am besten Github-Codespaces. Dazu genügt ein Klick auf den Knopf zuoberst in diesem Dokument oder auf den unstenstehenden Link. In wenigen Schritten wird ein virtueller Computer gestartet und die Sofware installiert. Bei der Nutzung von Codespaces fallen Kosten von derzeit 18 Cents pro Stunde an.

1. Starten Sie [Github-Codespaces](https://codespaces.new/I14Y-ch/iSurvey) mit dem I14Y-Plugin.
2. Installieren Sie die nötigen Docker-Container: ```docker-compose build```.
3. Starten Sie die installierte Software: ```docker-compose up -d```.
4. Klicken Sie auf den unten rechts eingeblendeten Link. Sie sehen nun die öffentliche Startseite von Limesurvey. Falls Sie den Admin-Bereich nutzen möchten, fügen Sie der URL ```/index.php/admin/index```an. Nutzen Sie fürs erste Einloggen ```admin``` mit ```password```. Ändern Sie das Passwort in der Administationsoberfläche anschliessend ab.
5. Installieren und nutzen Sie das I14Y-Plugin (siehe [unten](#plugin-zu-bestehender-installation-hinzufügen))

### Docker-Container installieren

Damit Limesurvey und iSurvey auf einfache Weise ausprobiert werden kann, wird hier eine auf Docker basierende Installationsmöglichkeit zur Verfügung gestellt. 

|:exclamation: Prototyp nicht für sensible Daten verwenden|
|-----------------------------------------|
|Ohne weitergehende Abklärungen sollte iSurvey nicht produktiv genutzt werden. Insbesondere dürfen damit keine schützenswerten Daten erhoben werden. Die Installation enthält einen [Limesurvey-Container](https://github.com/adamzammit/limesurvey-docker) von Adam Zammit, der für die Nichtregierungsorganisation Australian Consortium for Social and Political Research Incorporated arbeitet. Statt diese zu nutzen, kann auch eine selbst geprüfte Limesurvey-Version eingesetzt werden. Diese lässt sich mit dem [hier publizierten Plugin](https://github.com/I14Y-ch/iSurvey/tree/main/I14Y%20LimeSurvey%20Plugin) ergänzen. Die Interoperabilitätsstelle leistet keinen Support für das Plugin. Die Nutzung erfolgt auf eigenes Risiko.|

Um die Testversion auf dem lokalen Computer zu installieren, sind untenstehende Schritte auf der Kommandozeile nötig. Voraussetzung: Git, Docker und Docker-Compose müssen installiert sein.  

1. Auschecken des Repository mit ```git clone https://github.com/I14Y-ch/iSurvey.git```. Wechsel ins neu erstellte Verzeichnis: ```cd iSurvey```. 
2. Editieren der Anmeldedaten für den LimeSurvey-Administrator in der Datei __docker-compose.yml__ mit einem Texteditor.
3. Installieren der Applikation mit ```docker-compose build```.
4. Starten der Applikation mit ```docker-compose up -d```. Limesurvey ist nun unter http://localhost:8082/ (Nutzeroberfläche) beziehungsweise http://localhost:8082/index.php/admin/index (Admin-Bereich) erreichbar. 

### Plugin zu bestehender Installation hinzufügen
Das Plugin ist bereits auf dem Server vorhanden. Mit den folgenden vier Schritten kann es aktiviert werden. Nach der Aktivierung sind alle I14Y-Beschriftungssets verfügbar. Sobald das I14Y-Plugin aktiviert ist, werden die Beschriftungssets in LimeSurvey täglich automatisch aktualisiert.

1. Gehe zu Konfiguration>Plugins
2. Dateien Scannen
3. Beim Plugin I14Y klicke auf den Button Installieren
4. Gehe zum Plugin I14Y und klicke aktivieren

## Nutzung von Limesurvey mit dem I14Y-Plugin
1. Erstellen Sie eine neue Umfrage. Wählen Sie als Sprache Deutsch aus.
2. Erfassen Sie eine erste Frage. Wählen Sie rechts als Fragetipp zum Beispiel eine Einfachauswahl aus. 
3. Klicken Sie nun auf "Beschriftungsset laden". In der Liste sehen Sie nun alle Codelisten von I14Y. Wählen Sie die passende aus. Klicken Sie auf "Ersetzen". 

### Hinweise zur Nutzung
- Bei mehrsprachigen Umfragungen müssen die Sprachen ausgewählt werden, bevor die erste Codeliste einer Frage hinzugefügt wird. 
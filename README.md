# iSurvey -- die Brücke zwischen I14Y und Limesurvey
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/I14Y-ch/iSurvey)

Auf der [I14Y-Interoperabilitätsplattform](https://i14y.admin.ch) sind harmonisierte und standardisierte Codelisten der Schweizer Behörden erhältlich. Diese sollen in der quelloffenen Umfragesoftware [Limesurvey](https://limesurvey.org) auf einfache Weise genutzt werden können. Der Prototyp iSurvey versucht diese Brücke zu schlagen. Entwickelt wurde er im Rahmen des [GovTech-Hackathons 2024](https://www.bk.admin.ch/bk/de/home/digitale-transformation-ikt-lenkung/bundesarchitektur/api-architektur-bund/govtech-hackathon24.html).  

iSurvey ruft die öffentlich verfügbaren Codelisten von der I14Y-Interoperabilitätsplattform ab, so dass sich die Listen mit wenigen Klicks in eine Umfrage einbauen lassen. Dadurch können Umfragen rascher erstellt werden. Und es entstehen nachträglich weniger Probleme aufgrund abweichender Codierungen. 

iSurvey besteht aus einem Plugin für Limesurvey und einigen Skripten, mit denen die Codelisten bezogen und aufbereitet werden. Dank Docker-Containern und einer detaillierten Anleitung lässt sich Limesurvey inklusive des Plugins iSurvey innert weniger Minuten installieren. 

## Installation 

### Plugin zu bestehender Installation hinzufügen

Limesurvey ist eine webbasierte Software, mit der Befragungen durchgeführt werden können. Sie kann entweder kostenpflichtig als Software as a Service genutzt werden. Alternativ kann die quelloffene Software auch in der **Community Edition** auf einem eigenen Server installiert werden ([Downloads](https://community.limesurvey.org/downloads/), [Anleitung](https://manual.limesurvey.org/Installation_-_LimeSurvey_CE)). 

Sobald die Installation abgschlossen ist, wird das Plugin iSurvey hinzugefügt.  

### Docker-Container installieren

Damit Limesurvey und iSurvey auf einfache Weise ausprobiert werden kann, wird hier eine auf Docker basierende Installationsmöglichkeit zur Verfügung gestellt. 

| :exclamation:  Prototyp nicht für sensible Daten verwenden   |
|-----------------------------------------|
| Bei diesem Docker-Container handelt es sich um einen Prototyp. Er eignet sich für Tests. Ohne weitergehende Abklärungen sollte er nicht produktiv durch Behörden genutzt werden. Insbesondere dürfen damit keine schützenswerten Daten erhoben werden. Der Prototyp enthält einen Limesurvey-Container, der von einem privaten Nutzer angeboten wird. Empfohlen wird eine Installation einer geprüften Limesurvey-Version durch die zuständigen Behörde. Diese kann mit dem hier publizierten Plugin ergänzt werden. |

Um die Testversion auf dem lokalen Computer zu installieren, sind untenstehende Schritte auf der Kommandozeile nötig. Voraussetzungen: Git, Docker und Docker-Compose müssen installiert sein.  

1. Auschecken des Repository mit ```git clone https://github.com/I14Y-ch/iSurvey.git```. Wechsel ins neu erstellte Verzeichnis: ```cd iSurvey```. 
2. Editieren der Anmeldedaten für den LimeSurvey-Administrator in der Datei __docker-compose.yml__ mit einem Texteditor.
3. Installieren der Applikation mit ```docker-compose build```.
4. Starten der Applikation mit ```docker-compose up -d```. Limesurvey ist nun unter http://localhost:8082/ (Nutzeroberfläche) beziehungsweise http://localhost:8082/index.php/admin/index (Admin-Bereich) erreichbar. 

## Hinweise zur Nutzung
- Die Codelisten werden in der Regel einmal täglich aktualiert. 
- Bei mehrsprachigen Umfragungen müssen die Sprachen ausgewählt werden, bevor die erste Codeliste einer Frage hinzugefügt wird. 
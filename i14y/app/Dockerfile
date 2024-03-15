# Basierend auf einem offiziellen Python-Image
FROM python:3.9

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Installieren von Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren des restlichen Quellcodes in den Container
COPY . .

# Befehl, der beim Start des Containers ausgeführt wird
CMD ["python", "script.py"]

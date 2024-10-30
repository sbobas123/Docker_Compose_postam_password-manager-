# Usa un'immagine base di Python
FROM python:3.9

# Imposta la cartella di lavoro
WORKDIR /app

# Copia il file di requirements
COPY requirements.txt .

# Installa i pacchetti necessari
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY app/ .

# Espone la porta su cui Flask girerà all'interno del container
EXPOSE 5000

# Comando per avviare l'app
CMD ["python", "main.py"]


FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# On expose les deux ports : 8000 pour l'API, 8501 pour Streamlit
EXPOSE 8000
EXPOSE 8501

# On lance l'API en arrière-plan (&) puis Streamlit au premier plan
CMD uvicorn main:app --host 0.0.0.0 --port 8000 & streamlit run app.py --server.port 8501 --server.address 0.0.0.0
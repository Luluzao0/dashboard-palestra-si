FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copiar projeto
COPY . .

# Expor porta
EXPOSE 8501

# Saúde check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Executar Streamlit
CMD ["streamlit", "run", "SCRIPTS/dashboard_palestra.py", "--server.port=8501", "--server.address=0.0.0.0"]

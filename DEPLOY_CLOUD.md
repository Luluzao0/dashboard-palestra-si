# Deploy em Nuvem - Dashboard Palestra SI

## 🚀 Streamlit Cloud (Mais Rápido)

### Passo 1: Prepare o repositório
- ✓ `requirements.txt` está atualizado
- ✓ `SCRIPTS/dashboard_palestra.py` é o arquivo principal
- ✓ `.streamlit/config.toml` está configurado

### Passo 2: Push para GitHub
```bash
git add .
git commit -m "Deploy cloud setup"
git push origin main
```

### Passo 3: Deploy no Streamlit Cloud
1. Acesse: https://share.streamlit.io
2. Clique em "New app"
3. Conecte seu GitHub
4. Selecione: `Luluzao0/dashboard-palestra-si`
5. Main file path: `SCRIPTS/dashboard_palestra.py`
6. Python version: `3.11`
7. Clique "Deploy"

**Sua app estará em:** `https://dashboard-palestra-si.streamlit.app`

---

## 🐳 Alternativa: Docker + Render

### Passo 1: Criar Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "SCRIPTS/dashboard_palestra.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Passo 2: Push e Deploy
- Push no GitHub
- Acesse: https://render.com
- Create > Web Service
- Conecte GitHub
- Deploy

---

## 📦 Alternativa Rápida: Heroku

```bash
heroku login
heroku create seu-app-name
git push heroku main
```

---

**RECOMENDADO:** Streamlit Cloud (é grátis, fácil e rápido!)

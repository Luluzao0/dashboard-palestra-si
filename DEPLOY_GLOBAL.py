#!/usr/bin/env python3
"""
DEPLOY GLOBAL - Dashboard Palestra SI
Consolida dados, scripts e inicia dashboard direto
"""

import os
import sys
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Configurações
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SCRIPTS_DIR = os.path.join(BASE_DIR, 'SCRIPTS')
OUTPUTS_DIR = os.path.join(BASE_DIR, 'OUTPUTS')

# Criar diretórios se não existirem
os.makedirs(OUTPUTS_DIR, exist_ok=True)

print("=" * 60)
print("DEPLOY GLOBAL - Dashboard Palestra SI")
print("=" * 60)

# 1. CARREGAR DADOS
print("\n[1] Carregando dados...")
try:
    xlsx_file = os.path.join(DATA_DIR, 'palestra_desenvolvimento.xlsx')
    df = pd.read_excel(xlsx_file)
    print(f"✓ Dados carregados: {len(df)} registros, {len(df.columns)} colunas")
    
    # Salvar versão CSV
    csv_file = os.path.join(OUTPUTS_DIR, 'dados_processados.csv')
    df.to_csv(csv_file, index=False)
    print(f"✓ CSV exportado: {csv_file}")
except Exception as e:
    print(f"✗ Erro ao carregar dados: {e}")
    sys.exit(1)

# 2. NORMALIZAR DADOS
print("\n[2] Normalizando dados...")
try:
    # Limpeza básica
    df = df.dropna(how='all')
    df = df.fillna('N/A')
    
    # Análise rápida
    stats = {
        'total_registros': len(df),
        'colunas': list(df.columns),
        'tipos': df.dtypes.to_dict()
    }
    print(f"✓ Dados normalizados")
    print(f"  - Total: {stats['total_registros']} registros")
    print(f"  - Campos: {len(stats['colunas'])}")
except Exception as e:
    print(f"✗ Erro ao normalizar: {e}")
    sys.exit(1)

# 3. GERAR RELATÓRIO RÁPIDO
print("\n[3] Gerando relatório...")
try:
    relatorio = f"""
RELATÓRIO GLOBAL - Palestra SI
=====================================
Data: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M:%S')}

DADOS:
- Total de respostas: {len(df)}
- Campos: {len(df.columns)}
- Colunas: {', '.join(df.columns[:5])}...

STATUS: ✓ PRONTO PARA DEPLOY
"""
    
    rel_file = os.path.join(OUTPUTS_DIR, 'relatorio_deploy.txt')
    with open(rel_file, 'w', encoding='utf-8') as f:
        f.write(relatorio)
    
    print(relatorio)
    print(f"✓ Relatório salvo: {rel_file}")
except Exception as e:
    print(f"✗ Erro ao gerar relatório: {e}")

# 4. INICIAR DASHBOARD
print("\n[4] Iniciando Dashboard...")
print("=" * 60)
print("Dashboard será aberto em http://localhost:8501")
print("Pressione Ctrl+C para parar")
print("=" * 60 + "\n")

os.system(f'streamlit run {os.path.join(SCRIPTS_DIR, "dashboard_palestra.py")}')

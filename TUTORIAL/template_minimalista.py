"""
╔════════════════════════════════════════════════════════════════╗
║         TEMPLATE MINIMALISTA: Comece bem enxuto!              ║
║                                                                ║
║  Este é o código MAIS SIMPLES possível para um dashboard.    ║
║  Copie, mude os dados, e pronto!                              ║
║                                                                ║
║  Para executar:                                               ║
║  streamlit run template_minimalista.py                        ║
╚════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd

# ═══════════════════════════════════════════════════════════════
# PASSO 1: CONFIGURAR
# ═══════════════════════════════════════════════════════════════

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Meu Dashboard")

# ═══════════════════════════════════════════════════════════════
# PASSO 2: CRIAR DADOS (ou ler do arquivo)
# ═══════════════════════════════════════════════════════════════

# OPÇÃO A: Dados fictícios (para testar)
dados = {
    'Categoria': ['Vendas', 'Lucro', 'Custos', 'Margem'],
    'Valor': [10000, 3000, 7000, 30]
}
df = pd.DataFrame(dados)

# OPÇÃO B: Ler de um arquivo (descomente e mude o nome)
# df = pd.read_excel('seu_arquivo.xlsx')
# df = pd.read_csv('seu_arquivo.csv')

# ═══════════════════════════════════════════════════════════════
# PASSO 3: MOSTRAR FILTRO (opcional)
# ═══════════════════════════════════════════════════════════════

# Se seu arquivo tem uma coluna para filtrar:
# filtro = st.sidebar.selectbox("Escolha:", df['SuaColuna'].unique())
# df = df[df['SuaColuna'] == filtro]

# ═══════════════════════════════════════════════════════════════
# PASSO 4: MOSTRAR NÚMEROS IMPORTANTES
# ═══════════════════════════════════════════════════════════════

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total de Registros", len(df))

with col2:
    total = df['Valor'].sum()
    st.metric("Valor Total", f"R$ {total:,.2f}")

with col3:
    media = df['Valor'].mean()
    st.metric("Valor Médio", f"R$ {media:,.2f}")

# ═══════════════════════════════════════════════════════════════
# PASSO 5: MOSTRAR GRÁFICO
# ═══════════════════════════════════════════════════════════════

st.bar_chart(df.set_index('Categoria'))

# ═══════════════════════════════════════════════════════════════
# PASSO 6: MOSTRAR DADOS
# ═══════════════════════════════════════════════════════════════

st.dataframe(df)

# ═══════════════════════════════════════════════════════════════
# FIM!
# ═══════════════════════════════════════════════════════════════
# Está pronto! É assim de simples.
# Agora adapte conforme necessário.

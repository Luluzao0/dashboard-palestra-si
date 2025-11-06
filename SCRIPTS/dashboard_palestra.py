"""
DASHBOARD PROFISSIONAL ÚNICO - Palestra SI
Consolidação completa em uma única página
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard Palestra SI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================
# FUNÇÕES
# ============================================================================

@st.cache_data
def carregar_dados():
    """Carrega dados do arquivo Excel - compatível com qualquer caminho"""
    import os
    import glob
    
    # Tentar vários caminhos
    paths = [
        'data/palestra_desenvolvimento.xlsx',
        './data/palestra_desenvolvimento.xlsx',
        os.path.join('data', 'palestra_desenvolvimento.xlsx'),
    ]
    
    df = None
    for path in paths:
        try:
            if os.path.exists(path):
                df = pd.read_excel(path)
                break
        except:
            pass
    
    if df is None:
        # Busca recursiva como último recurso
        try:
            xlsx_files = glob.glob('**/palestra_desenvolvimento.xlsx', recursive=True)
            if xlsx_files:
                df = pd.read_excel(xlsx_files[0])
        except:
            pass
    
    if df is None:
        st.error("❌ Arquivo palestra_desenvolvimento.xlsx não encontrado")
        st.stop()
    
    # Limpar nomes de colunas
    df.columns = [col.strip() for col in df.columns]
    
    return df

# Tentar carregar dados
try:
    df = carregar_dados()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.markdown("""
    <style>
        .header-title {
            text-align: center;
            color: #1f77b4;
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .header-subtitle {
            text-align: center;
            color: #666;
            font-size: 1.1em;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='header-title'>📊 DASHBOARD - Palestra SI</div>", unsafe_allow_html=True)
st.markdown("<div class='header-subtitle'>Análise Completa de Avaliações - 14 a 15 de Outubro de 2025</div>", unsafe_allow_html=True)
st.divider()

# ============================================================================
# MÉTRICAS PRINCIPAIS
# ============================================================================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("📋 Total de Respostas", len(df))

with col2:
    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '
    st.metric("⭐ Nota Média", f"{df[nota_col].mean():.2f}/10")

with col3:
    st.metric("👥 Faixa Etária Dominante", df['Idade'].mode()[0] if not df['Idade'].mode().empty else 'N/A')

with col4:
    pesquisa_sim = len(df[df['Já participou de algum projeto de pesquisa ou extensão?  '].str.contains('Sim', case=False, na=False)])
    st.metric("🔬 Experiência em Pesquisa", f"{pesquisa_sim}")

with col5:
    st.metric("📅 Data do Evento", "14-15/10/2025")

st.divider()

# ============================================================================
# FILTROS SIDEBAR
# ============================================================================

st.sidebar.title("🎛️ FILTROS")

# Filtro por faixa etária
faixas_etarias = sorted(df['Idade'].unique().tolist())
faixas_selecionadas = st.sidebar.multiselect(
    "Faixa Etária",
    options=faixas_etarias,
    default=faixas_etarias,
    key="faixa_etaria"
)

# Filtro por experiência em pesquisa
pesquisa_opcoes = df['Já participou de algum projeto de pesquisa ou extensão?  '].unique().tolist()
pesquisa_selecionada = st.sidebar.multiselect(
    "Experiência em Pesquisa",
    options=pesquisa_opcoes,
    default=pesquisa_opcoes,
    key="pesquisa"
)

# Botão resetar
if st.sidebar.button("🔄 Resetar Filtros", use_container_width=True):
    st.rerun()

# Aplicar filtros
df_filtrado = df[
    (df['Idade'].isin(faixas_selecionadas)) &
    (df['Já participou de algum projeto de pesquisa ou extensão?  '].isin(pesquisa_selecionada))
]

st.sidebar.metric("📊 Registros Filtrados", len(df_filtrado))

# ============================================================================
# SEÇÃO 1: VISÃO GERAL
# ============================================================================

st.subheader("📈 1. VISÃO GERAL")

col1, col2 = st.columns(2)

with col1:
    # Distribuição por idade
    fig, ax = plt.subplots(figsize=(10, 5))
    idade_counts = df_filtrado['Idade'].value_counts().sort_index()
    idade_counts.plot(kind='bar', ax=ax, color='#667eea', edgecolor='black', alpha=0.7)
    ax.set_title('Distribuição por Faixa Etária', fontsize=14, fontweight='bold')
    ax.set_xlabel('Faixa Etária')
    ax.set_ylabel('Quantidade')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

with col2:
    # Avaliação geral
    fig, ax = plt.subplots(figsize=(10, 5))
    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '
    notas = df_filtrado[nota_col].value_counts().sort_index()
    notas.plot(kind='bar', ax=ax, color='#764ba2', edgecolor='black', alpha=0.7)
    ax.set_title('Avaliação Geral do Evento', fontsize=14, fontweight='bold')
    ax.set_xlabel('Nota (0-10)')
    ax.set_ylabel('Quantidade')
    ax.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=0)
    st.pyplot(fig)

# ============================================================================
# SEÇÃO 2: ANÁLISE TEMÁTICA
# ============================================================================

st.subheader("🎯 2. ANÁLISE TEMÁTICA")

# Colunas de avaliação
avaliacoes = [
    'O conteúdo apresentado foi claro e de fácil compreensão  ',
    'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).  ',
    'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.  ',
    'A interação entre os palestrantes e o público foi satisfatória.  ',
    'Após a palestra, você considera mais clara a importância da integração entre Administração e Engenharia da Computação para o desenvolvimento institucional?  ',
    'Você percebe potencial de aplicação dos sistemas apresentados em outras organizações públicas ou privadas?    ',
    'O evento despertou seu interesse em aprofundar conhecimentos sobre Sistemas de Informação Gerencial (SIG)?   '
]

# Preparar dados para heatmap
avaliacoes_resumidas = [
    'Conteúdo Claro',
    'Aplicabilidade Prática',
    'Gestão & Tecnologia',
    'Interação Palestrantes',
    'Integração Admin-Eng',
    'Potencial Aplicação',
    'Interesse em SIG'
]

# Contar respostas "Sim"
dados_avaliacoes = []
for i, av in enumerate(avaliacoes):
    if av in df_filtrado.columns:
        sim_count = len(df_filtrado[df_filtrado[av].str.contains('Sim', case=False, na=False)])
        taxa = (sim_count / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
        dados_avaliacoes.append(taxa)

# Gráfico de aprovação
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#2ecc71' if x >= 80 else '#f39c12' if x >= 60 else '#e74c3c' for x in dados_avaliacoes]
bars = ax.barh(avaliacoes_resumidas, dados_avaliacoes, color=colors, edgecolor='black', alpha=0.8)
ax.set_xlabel('Taxa de Aprovação (%)', fontsize=12, fontweight='bold')
ax.set_title('Taxa de Concordância por Tema', fontsize=14, fontweight='bold')
ax.set_xlim(0, 100)
ax.grid(axis='x', alpha=0.3)

# Adicionar valores nas barras
for i, (bar, val) in enumerate(zip(bars, dados_avaliacoes)):
    ax.text(val + 2, i, f'{val:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

# ============================================================================
# SEÇÃO 3: EXPERIÊNCIA EM PESQUISA
# ============================================================================

st.subheader("🔬 3. ANÁLISE POR EXPERIÊNCIA")

col1, col2 = st.columns(2)

with col1:
    # Experiência em pesquisa
    fig, ax = plt.subplots(figsize=(8, 5))
    pesquisa_counts = df_filtrado['Já participou de algum projeto de pesquisa ou extensão?  '].value_counts()
    colors_pesquisa = ['#3498db', '#e74c3c']
    pesquisa_counts.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=colors_pesquisa, startangle=90)
    ax.set_ylabel('')
    ax.set_title('Experiência em Pesquisa/Extensão', fontsize=14, fontweight='bold')
    st.pyplot(fig)

with col2:
    # Motivação para projetos
    fig, ax = plt.subplots(figsize=(8, 5))
    
    motivacao_col = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique. '
    if motivacao_col in df_filtrado.columns:
        motivacao_counts = df_filtrado[motivacao_col].str.contains('Sim', case=False, na=False).value_counts()
        colors_motiv = ['#2ecc71', '#95a5a6']
        labels_motiv = ['Motivado', 'Não Motivado/Indefinido']
        ax.pie(motivacao_counts.values, autopct='%1.1f%%', colors=colors_motiv, labels=labels_motiv, startangle=90)
        ax.set_title('Motivação para Pesquisa/Extensão', fontsize=14, fontweight='bold')
    
    st.pyplot(fig)

# ============================================================================
# SEÇÃO 4: RESPOSTAS ABERTAS
# ============================================================================

st.subheader("💬 4. RESPOSTAS ABERTAS")

tabs = st.tabs([
    "Tecnologia & Gestão",
    "Cooperação Admin-Eng",
    "Motivação para Projetos"
])

with tabs[0]:
    st.write("**Como soluções tecnológicas podem contribuir para gestão mais efetiva:**")
    col_gestao = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'
    if col_gestao in df_filtrado.columns:
        respostas = df_filtrado[col_gestao].dropna()
        for i, resp in enumerate(respostas, 1):
            if resp and resp.strip() != '':
                st.write(f"{i}. {resp}")
    else:
        st.info("Coluna não disponível")

with tabs[1]:
    st.write("**Como Admin pode se beneficiar da cooperação com Engenharia:**")
    col_coop = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação? '
    if col_coop in df_filtrado.columns:
        respostas = df_filtrado[col_coop].dropna()
        for i, resp in enumerate(respostas, 1):
            if resp and resp.strip() != '':
                st.write(f"{i}. {resp}")
    else:
        st.info("Coluna não disponível")

with tabs[2]:
    st.write("**Justificativas para participação em projetos:**")
    col_justif = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique. '
    if col_justif in df_filtrado.columns:
        respostas = df_filtrado[col_justif].dropna()
        for i, resp in enumerate(respostas, 1):
            if resp and resp.strip() != '':
                st.write(f"{i}. {resp}")
    else:
        st.info("Coluna não disponível")

# ============================================================================
# SEÇÃO 5: DADOS COMPLETOS
# ============================================================================

st.subheader("📋 5. DADOS COMPLETOS")

if st.checkbox("📥 Visualizar Tabela Completa", value=False):
    st.dataframe(df_filtrado, use_container_width=True)
    
    # Download CSV
    csv = df_filtrado.to_csv(index=False)
    st.download_button(
        label="⬇️ Baixar como CSV",
        data=csv,
        file_name="palestra_avaliacoes.csv",
        mime="text/csv"
    )

# ============================================================================
# RODAPÉ
# ============================================================================

st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9em; margin-top: 20px;'>
        <p>Dashboard desenvolvido com Streamlit | Palestra SI 2025</p>
        <p>Dados: 27 respostas | Período: 14-15 de outubro de 2025</p>
    </div>
""", unsafe_allow_html=True)

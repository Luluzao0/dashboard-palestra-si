""""""

DASHBOARD PROFISSIONAL ÚNICO - Palestra SIDASHBOARD PROFISSIONAL ÚNICO - Palestra SI

Funciona no Streamlit Cloud e LocalmenteConsolidação completa em uma única página

"""Versão para Streamlit Cloud - FUNCIONA EM QUALQUER LUGAR

"""

import streamlit as st

import pandas as pdimport streamlit as st

import matplotlib.pyplot as pltimport pandas as pd

import seaborn as snsimport matplotlib.pyplot as plt

import numpy as npimport seaborn as sns

import warningsimport numpy as np

import osfrom scipy import stats

import globimport warnings

import os

warnings.filterwarnings('ignore')import glob



st.set_page_config(page_title="Dashboard Palestra SI", page_icon="📊", layout="wide")warnings.filterwarnings('ignore')



sns.set_style("whitegrid")st.set_page_config(page_title="Dashboard Palestra SI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

plt.rcParams['figure.facecolor'] = 'white'

sns.set_style("whitegrid")

# ============================================================================plt.rcParams['figure.facecolor'] = 'white'

# CARREGAR DADOSplt.rcParams['figure.figsize'] = (12, 6)

# ============================================================================

# ============================================================================

@st.cache_data# CARREGAR DADOS - Compatível com qualquer estrutura

def carregar_dados():# ============================================================================

    """Carrega dados - funciona localmente e no Streamlit Cloud"""

    try:@st.cache_data

        # Tentar caminhos diferentesdef carregar_dados():

        paths = [    """Carrega dados - funciona localmente e no Streamlit Cloud"""

            'data/palestra_desenvolvimento.xlsx',    try:

            './data/palestra_desenvolvimento.xlsx',        # Tentar caminhos diferentes

            os.path.join(os.path.dirname(__file__), '../data/palestra_desenvolvimento.xlsx'),        paths = [

        ]            'data/palestra_desenvolvimento.xlsx',

                    './data/palestra_desenvolvimento.xlsx',

        df = None            os.path.join(os.path.dirname(__file__), '../data/palestra_desenvolvimento.xlsx'),

        for path in paths:            os.path.join(os.getcwd(), 'data/palestra_desenvolvimento.xlsx'),

            try:        ]

                if os.path.exists(path):        

                    df = pd.read_excel(path)        df = None

                    break        for path in paths:

            except:            try:

                pass                if os.path.exists(path):

                            df = pd.read_excel(path)

        if df is None:                    break

            xlsx_files = glob.glob('**/palestra_desenvolvimento.xlsx', recursive=True)            except:

            if xlsx_files:                pass

                df = pd.read_excel(xlsx_files[0])        

                if df is None:

        if df is None:            # Busca recursiva como último recurso

            st.error("❌ Arquivo não encontrado")            xlsx_files = glob.glob('**/palestra_desenvolvimento.xlsx', recursive=True)

            st.stop()            if xlsx_files:

                        df = pd.read_excel(xlsx_files[0])

        df.columns = [col.strip() for col in df.columns]        

        return df        if df is None:

                    st.error("❌ Arquivo palestra_desenvolvimento.xlsx não encontrado. Verifique a estrutura do projeto.")

    except Exception as e:            st.stop()

        st.error(f"❌ Erro: {str(e)}")        

        st.stop()        df.columns = [col.strip() for col in df.columns]

        return df

df = carregar_dados()        

    except Exception as e:

# ============================================================================        st.error(f"❌ Erro ao carregar dados: {str(e)}")

# HEADER        st.stop()

# ============================================================================

df = carregar_dados()

st.markdown("<h1 style='text-align: center; color: #1f77b4;'>📊 Dashboard - Palestra SI</h1>", unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #666;'>Análise de Avaliações | 14-15 de Outubro de 2025</p>", unsafe_allow_html=True)# ============================================================================

st.divider()# HEADER

# ============================================================================

# ============================================================================

# MÉTRICASst.markdown("""

# ============================================================================    <style>

        .header-title { text-align: center; color: #1f77b4; font-size: 2.5em; font-weight: bold; }

col1, col2, col3, col4, col5 = st.columns(5)    </style>

""", unsafe_allow_html=True)

with col1:

    st.metric("📋 Total", len(df))st.markdown("<div class='header-title'>📊 DASHBOARD - Palestra SI</div>", unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #666;'>Análise de Avaliações - 14-15 de Outubro de 2025</div>", unsafe_allow_html=True)

with col2:st.divider()

    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '

    media = df[nota_col].astype(float).mean() if nota_col in df.columns else 0# ============================================================================

    st.metric("⭐ Nota Média", f"{media:.2f}/10")# MÉTRICAS

# ============================================================================

with col3:

    st.metric("👥 Respostas", "27")col1, col2, col3, col4, col5 = st.columns(5)



with col4:with col1:

    st.metric("🎯 Status", "✓ OK")    st.metric("📋 Total", len(df))



with col5:with col2:

    st.metric("📅 Data", "Oct 2025")    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '

    media = df[nota_col].astype(float).mean() if nota_col in df.columns else 0

st.divider()    st.metric("⭐ Nota Média", f"{media:.2f}/10" if media else "N/A")



# ============================================================================with col3:

# FILTROS    st.metric("👥 Faixa Etária", "18-30")

# ============================================================================

with col4:

st.sidebar.title("🎛️ FILTROS")    st.metric("🔬 Pesquisa", "12")

idade_col = 'Idade'

with col5:

if idade_col in df.columns:    st.metric("📅 Data", "14-15/10")

    faixas = sorted(df[idade_col].unique().tolist())

    selecionadas = st.sidebar.multiselect("Faixa Etária", faixas, default=faixas)st.divider()

    df_filtrado = df[df[idade_col].isin(selecionadas)]

else:# ============================================================================

    df_filtrado = df# FILTROS

# ============================================================================

if st.sidebar.button("🔄 Resetar", use_container_width=True):

    st.rerun()st.sidebar.title("🎛️ FILTROS")

idade_col = 'Idade'

st.sidebar.metric("Registros", len(df_filtrado))if idade_col in df.columns:

    faixas = sorted(df[idade_col].unique().tolist())

# ============================================================================    selecionadas = st.sidebar.multiselect("Faixa Etária", faixas, default=faixas)

# SEÇÃO 1: VISÃO GERAL    df_filtrado = df[df[idade_col].isin(selecionadas)]

# ============================================================================else:

    df_filtrado = df

st.subheader("📈 1. VISÃO GERAL")

if st.sidebar.button("🔄 Resetar"):

col1, col2 = st.columns(2)    st.rerun()



with col1:st.sidebar.metric("Registros", len(df_filtrado))

    if 'Idade' in df_filtrado.columns:

        fig, ax = plt.subplots(figsize=(10, 5))# ============================================================================

        df_filtrado['Idade'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#667eea', alpha=0.7, edgecolor='black')# GRÁFICOS - VISÃO GERAL

        ax.set_title('Distribuição por Faixa Etária', fontsize=12, fontweight='bold')# ============================================================================

        ax.set_xlabel('Faixa Etária')

        ax.set_ylabel('Quantidade')st.subheader("📈 1. VISÃO GERAL")

        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()col1, col2 = st.columns(2)

        st.pyplot(fig)

with col1:

with col2:    if 'Idade' in df_filtrado.columns:

    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '        fig, ax = plt.subplots(figsize=(10, 5))

    if nota_col in df_filtrado.columns:        df_filtrado['Idade'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#667eea', alpha=0.7)

        fig, ax = plt.subplots(figsize=(10, 5))        ax.set_title('Distribuição por Faixa Etária', fontsize=12, fontweight='bold')

        df_filtrado[nota_col].astype(float).value_counts().sort_index().plot(kind='bar', ax=ax, color='#764ba2', alpha=0.7, edgecolor='black')        ax.set_xlabel('Faixa Etária')

        ax.set_title('Avaliação Geral do Evento', fontsize=12, fontweight='bold')        ax.set_ylabel('Quantidade')

        ax.set_xlabel('Nota (0-10)')        plt.xticks(rotation=45, ha='right')

        ax.set_ylabel('Quantidade')        st.pyplot(fig)

        plt.tight_layout()

        st.pyplot(fig)with col2:

    nota_col = 'Avaliação geral do evento (nota de 0 a 10): '

# ============================================================================    if nota_col in df_filtrado.columns:

# SEÇÃO 2: ANÁLISE TEMÁTICA        fig, ax = plt.subplots(figsize=(10, 5))

# ============================================================================        df_filtrado[nota_col].astype(float).value_counts().sort_index().plot(kind='bar', ax=ax, color='#764ba2', alpha=0.7)

        ax.set_title('Avaliação Geral do Evento', fontsize=12, fontweight='bold')

st.subheader("🎯 2. ANÁLISE TEMÁTICA")        ax.set_xlabel('Nota (0-10)')

        ax.set_ylabel('Quantidade')

avaliacoes = [        st.pyplot(fig)

    'O conteúdo apresentado foi claro e de fácil compreensão  ',

    'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).  ',# ============================================================================

    'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.  ',# ANÁLISE TEMÁTICA

    'A interação entre os palestrantes e o público foi satisfatória.  ',# ============================================================================

    'Após a palestra, você considera mais clara a importância da integração entre Administração e Engenharia da Computação para o desenvolvimento institucional?  ',

    'Você percebe potencial de aplicação dos sistemas apresentados em outras organizações públicas ou privadas?    ',st.subheader("🎯 2. ANÁLISE TEMÁTICA")

    'O evento despertou seu interesse em aprofundar conhecimentos sobre Sistemas de Informação Gerencial (SIG)?   '

]avaliacoes = [

    'O conteúdo apresentado foi claro e de fácil compreensão  ',

labels = ['Conteúdo Claro', 'Aplicabilidade', 'Gestão & Tech', 'Interação', 'Integração Admin-Eng', 'Potencial Aplicação', 'Interesse SIG']    'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).  ',

    'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.  ',

dados = []    'A interação entre os palestrantes e o público foi satisfatória.  ',

for av in avaliacoes:]

    if av in df_filtrado.columns:

        sim = len(df_filtrado[df_filtrado[av].astype(str).str.contains('Sim', case=False, na=False)])labels = ['Conteúdo Claro', 'Aplicabilidade', 'Gestão & Tech', 'Interação']

        taxa = (sim / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0

        dados.append(taxa)dados = []

for av in avaliacoes:

if dados:    if av in df_filtrado.columns:

    fig, ax = plt.subplots(figsize=(12, 6))        sim = len(df_filtrado[df_filtrado[av].astype(str).str.contains('Sim', case=False, na=False)])

    colors = ['#2ecc71' if x >= 80 else '#f39c12' if x >= 60 else '#e74c3c' for x in dados]        taxa = (sim / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0

    bars = ax.barh(labels, dados, color=colors, alpha=0.8, edgecolor='black')        dados.append(taxa)

    ax.set_xlabel('Taxa de Concordância (%)', fontsize=11, fontweight='bold')

    ax.set_title('Taxa de Aprovação por Tema', fontsize=12, fontweight='bold')if dados:

    ax.set_xlim(0, 100)    fig, ax = plt.subplots(figsize=(12, 5))

    for i, v in enumerate(dados):    colors = ['#2ecc71' if x >= 80 else '#f39c12' for x in dados]

        ax.text(v + 2, i, f'{v:.0f}%', va='center', fontweight='bold')    bars = ax.barh(labels, dados, color=colors, alpha=0.8)

    plt.tight_layout()    ax.set_xlabel('Taxa de Aprovação (%)')

    st.pyplot(fig)    ax.set_title('Concordância por Tema', fontsize=12, fontweight='bold')

    ax.set_xlim(0, 100)

# ============================================================================    for i, v in enumerate(dados):

# SEÇÃO 3: RESPOSTAS ABERTAS        ax.text(v + 2, i, f'{v:.0f}%', va='center', fontweight='bold')

# ============================================================================    st.pyplot(fig)



st.subheader("💬 3. RESPOSTAS ABERTAS")# ============================================================================

# RESPOSTAS ABERTAS

tabs = st.tabs(["Gestão & Tecnologia", "Cooperação Admin-Eng", "Motivação"])# ============================================================================



with tabs[0]:st.subheader("💬 3. RESPOSTAS ABERTAS")

    col_gestao = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'

    if col_gestao in df_filtrado.columns:tabs = st.tabs(["Gestão & Tecnologia", "Cooperação"])

        respostas = df_filtrado[col_gestao].dropna()

        for i, resp in enumerate(respostas, 1):with tabs[0]:

            if resp and str(resp).strip():    col_gestao = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'

                st.write(f"**{i}.** {resp}")    if col_gestao in df_filtrado.columns:

        respostas = df_filtrado[col_gestao].dropna()

with tabs[1]:        for i, resp in enumerate(respostas, 1):

    col_coop = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação? '            if resp and str(resp).strip():

    if col_coop in df_filtrado.columns:                st.write(f"**{i}.** {resp}")

        respostas = df_filtrado[col_coop].dropna()

        for i, resp in enumerate(respostas, 1):with tabs[1]:

            if resp and str(resp).strip():    col_coop = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação? '

                st.write(f"**{i}.** {resp}")    if col_coop in df_filtrado.columns:

        respostas = df_filtrado[col_coop].dropna()

with tabs[2]:        for i, resp in enumerate(respostas, 1):

    col_motiv = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique. '            if resp and str(resp).strip():

    if col_motiv in df_filtrado.columns:                st.write(f"**{i}.** {resp}")

        respostas = df_filtrado[col_motiv].dropna()

        for i, resp in enumerate(respostas, 1):# ============================================================================

            if resp and str(resp).strip():# DADOS

                st.write(f"**{i}.** {resp}")# ============================================================================



# ============================================================================st.subheader("📋 4. DADOS COMPLETOS")

# SEÇÃO 4: DADOS

# ============================================================================if st.checkbox("Visualizar Tabela"):

    st.dataframe(df_filtrado, use_container_width=True)

st.subheader("📋 4. DADOS COMPLETOS")    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')

    st.download_button("⬇️ Baixar CSV", csv, "dados.csv", "text/csv")

if st.checkbox("Visualizar Tabela Completa"):

    st.dataframe(df_filtrado, use_container_width=True)# Rodapé

    csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')st.divider()

    st.download_button("⬇️ Baixar como CSV", csv, "palestra_dados.csv", "text/csv")st.markdown("<p style='text-align:center; color:#666; font-size:0.9em;'>Dashboard Palestra SI 2025 | Streamlit</p>", unsafe_allow_html=True)



# Rodapétab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Análise Avançada", "💬 Respostas", "📋 Dados"])

st.divider()

st.markdown("<p style='text-align:center; color:#666; font-size:0.85em;'>Dashboard Palestra SI 2025 | Desenvolvido com Streamlit</p>", unsafe_allow_html=True)# ═════════════════════════════════════════════════════════════════════════

# ABA 1: VISÃO GERAL
# ═════════════════════════════════════════════════════════════════════════

with tab1:
    
    # Números principais
    st.subheader("Resumo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Respostas", len(df_filtrado))
    
    with col2:
        media = df_filtrado['avaliacao_geral'].mean()
        st.metric("Nota Média", f"{media:.2f}/10")
    
    with col3:
        pct = (df_filtrado['avaliacao_geral'] >= 8).sum() / len(df_filtrado) * 100 if len(df_filtrado) > 0 else 0
        st.metric("Satisfação (≥8)", f"{pct:.0f}%")
    
    with col4:
        interesse = (df_filtrado['interesse_sig'].str.contains('Sim', case=False, na=False)).sum()
        pct_interesse = (interesse / len(df_filtrado) * 100) if len(df_filtrado) > 0 else 0
        st.metric("Interesse SIG", f"{pct_interesse:.0f}%")
    
    # Avaliação geral
    st.subheader("Distribuição de Notas")
    
    fig, ax = plt.subplots(figsize=(12, 4))
    contagem = df_filtrado['avaliacao_geral'].value_counts().sort_index()
    ax.bar(contagem.index, contagem.values, color='#1f77b4', edgecolor='black', alpha=0.8)
    ax.axvline(df_filtrado['avaliacao_geral'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {df_filtrado["avaliacao_geral"].mean():.2f}')
    ax.set_xlabel('Nota')
    ax.set_ylabel('Quantidade')
    ax.set_xticks(range(0, 11))
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    
    # Aspectos avaliados
    st.subheader("Aspectos Avaliados")
    
    fig, ax = plt.subplots(figsize=(12, 4))
    aspectos = ['conteudo_claro', 'sistemas_aplicaveis', 'tecnologia_gestao', 'interacao_palestrantes']
    nomes = ['Conteúdo Claro', 'Sistemas Aplicáveis', 'Tecnologia e Gestão', 'Interação Palestrantes']
    medias = [df_filtrado[col].mean() for col in aspectos]
    
    bars = ax.bar(nomes, medias, color=['#2ca02c', '#1f77b4', '#ff7f0e', '#d62728'], edgecolor='black', alpha=0.8)
    ax.set_ylabel('Nota Média')
    ax.set_ylim(0, 10)
    ax.axhline(y=8, color='red', linestyle='--', alpha=0.3, label='Meta (8.0)')
    
    for bar, v in zip(bars, medias):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.2,
                f'{v:.2f}', ha='center', va='bottom', fontweight='bold')
    
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    
    # Respostas categóricas
    st.subheader("Respostas Categóricas")
    
    col_cat1, col_cat2 = st.columns(2)
    
    with col_cat1:
        st.write("**Já participou de pesquisa/extensão?**")
        contagem = df_filtrado['participou_pesquisa'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%', 
               colors=['#2ca02c', '#ff7f0e', '#d62728'][:len(contagem)])
        plt.tight_layout()
        st.pyplot(fig)
    
    with col_cat2:
        st.write("**Integração Adm × Engenharia clara?**")
        contagem = df_filtrado['integracao_clara'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%',
               colors=['#2ca02c', '#ff7f0e', '#d62728'][:len(contagem)])
        plt.tight_layout()
        st.pyplot(fig)
    
    # Por faixa etária
    st.subheader("Análise por Faixa Etária")
    
    fig, ax = plt.subplots(figsize=(12, 4))
    media_por_idade = df_filtrado.groupby('idade')['avaliacao_geral'].agg(['mean', 'count']).sort_values('mean', ascending=False)
    
    bars = ax.bar(range(len(media_por_idade)), media_por_idade['mean'], 
                   color='#1f77b4', edgecolor='black', alpha=0.8)
    ax.set_xticks(range(len(media_por_idade)))
    ax.set_xticklabels(media_por_idade.index, rotation=45, ha='right')
    ax.set_ylabel('Nota Média')
    ax.set_ylim(0, 10)
    
    for i, (bar, (idx, row)) in enumerate(zip(bars, media_por_idade.iterrows())):
        height = bar.get_height()
        ax.text(i, height + 0.2, f'{height:.2f}\n(n={int(row["count"])})', 
                ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    st.pyplot(fig)


# ═════════════════════════════════════════════════════════════════════════
# ABA 2: ANÁLISE AVANÇADA
# ═════════════════════════════════════════════════════════════════════════

with tab2:
    
    st.subheader("Matriz de Correlação")
    
    avaliacoes = ['conteudo_claro', 'sistemas_aplicaveis', 'tecnologia_gestao', 
                  'interacao_palestrantes', 'avaliacao_geral']
    
    correlacao = df_filtrado[avaliacoes].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlacao, annot=True, fmt='.2f', cmap='RdYlGn', center=0, 
                ax=ax, cbar_kws={'label': 'Correlação'}, vmin=-1, vmax=1)
    ax.set_title('Correlação entre Variáveis')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Correlações mais fortes
    st.write("**Correlações Mais Fortes:**")
    correlacoes_lista = []
    for i in range(len(correlacao.columns)):
        for j in range(i+1, len(correlacao.columns)):
            correlacoes_lista.append({
                'var1': correlacao.columns[i],
                'var2': correlacao.columns[j],
                'corr': correlacao.iloc[i, j]
            })
    
    correlacoes_lista = sorted(correlacoes_lista, key=lambda x: abs(x['corr']), reverse=True)
    for item in correlacoes_lista[:5]:
        st.write(f"• **{item['var1']}** ↔ **{item['var2']}**: {item['corr']:.3f}")
    
    st.divider()
    
    # Comparação: Com vs Sem experiência em pesquisa
    st.subheader("Comparativo: Com vs Sem Experiência em Pesquisa")
    
    com_pesquisa = df_filtrado[df_filtrado['participou_pesquisa'].str.contains('Sim', case=False, na=False)][avaliacoes]
    sem_pesquisa = df_filtrado[df_filtrado['participou_pesquisa'].str.contains('Não', case=False, na=False)][avaliacoes]
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        st.write(f"**Com experiência ({len(com_pesquisa)} pessoas):**")
        st.write(com_pesquisa.mean().round(2))
    
    with col_comp2:
        st.write(f"**Sem experiência ({len(sem_pesquisa)} pessoas):**")
        st.write(sem_pesquisa.mean().round(2))
    
    # Teste T
    st.write("**Teste T (diferença significativa?):**")
    for col in avaliacoes:
        if len(com_pesquisa) > 1 and len(sem_pesquisa) > 1:
            t_stat, p_valor = stats.ttest_ind(com_pesquisa[col].dropna(), sem_pesquisa[col].dropna())
            sig = "✓ Significativo (p < 0.05)" if p_valor < 0.05 else "✗ Não significativo (p ≥ 0.05)"
            st.write(f"• **{col}**: t={t_stat:.2f}, p={p_valor:.4f} {sig}")
    
    st.divider()
    
    # Box plot comparativo
    st.subheader("Box Plot - Comparação Pesquisa vs Sem Pesquisa")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    dados_com = [com_pesquisa[col].dropna().values for col in avaliacoes]
    dados_sem = [sem_pesquisa[col].dropna().values for col in avaliacoes]
    
    x_pos = np.arange(len(avaliacoes))
    width = 0.35
    
    bp1 = ax.boxplot([com_pesquisa[col].dropna().values for col in avaliacoes], 
                      positions=x_pos - width/2, widths=width, patch_artist=True,
                      boxprops=dict(facecolor='#2ca02c', alpha=0.7))
    
    bp2 = ax.boxplot([sem_pesquisa[col].dropna().values for col in avaliacoes],
                      positions=x_pos + width/2, widths=width, patch_artist=True,
                      boxprops=dict(facecolor='#1f77b4', alpha=0.7))
    
    ax.set_xticks(x_pos)
    ax.set_xticklabels([c.replace('_', ' ').title() for c in avaliacoes], rotation=45, ha='right')
    ax.set_ylabel('Nota')
    ax.set_ylim(0, 10)
    
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='#2ca02c', alpha=0.7, label='Com Pesquisa'),
                       Patch(facecolor='#1f77b4', alpha=0.7, label='Sem Pesquisa')]
    ax.legend(handles=legend_elements)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # Scatter: Idade vs Avaliação
    st.subheader("Relação: Idade vs Avaliação Geral")
    
    fig, ax = plt.subplots(figsize=(12, 5))
    scatter = ax.scatter(df_filtrado['idade_num'], df_filtrado['avaliacao_geral'], 
                        alpha=0.6, s=100, c=df_filtrado['avaliacao_geral'], cmap='RdYlGn')
    
    # Linha de tendência
    z = np.polyfit(df_filtrado['idade_num'], df_filtrado['avaliacao_geral'], 1)
    p = np.poly1d(z)
    ax.plot(df_filtrado['idade_num'].sort_values(), p(df_filtrado['idade_num'].sort_values()), 
            "r--", linewidth=2, label=f'Tendência: y={z[0]:.3f}x+{z[1]:.2f}')
    
    ax.set_xlabel('Idade')
    ax.set_ylabel('Avaliação Geral')
    ax.set_ylim(0, 10)
    ax.legend()
    plt.colorbar(scatter, ax=ax, label='Avaliação')
    plt.tight_layout()
    st.pyplot(fig)
    
    # Estatísticas
    corr_idade = df_filtrado['idade_num'].corr(df_filtrado['avaliacao_geral'])
    st.write(f"**Correlação Idade vs Avaliação:** {corr_idade:.3f}")

# ═════════════════════════════════════════════════════════════════════════
# ABA 3: RESPOSTAS ABERTAS
# ═════════════════════════════════════════════════════════════════════════

with tab3:
    
    st.subheader("Análise de Palavras-Chave")
    
    # Palavras-chave
    palavras_chave = {
        'Tecnologia': ['tecnologia', 'software', 'sistema', 'digital', 'dados'],
        'Gestão': ['gestão', 'decisão', 'planejamento', 'controle', 'efetiva'],
        'Colaboração': ['cooperação', 'trabalho', 'colaboração', 'integração', 'juntos'],
        'Inovação': ['inovação', 'novo', 'moderno', 'avançado', 'criatividade']
    }
    
    contagem_palavras = {}
    for tema, palavras in palavras_chave.items():
        count = 0
        for col in ['tecnologia_contribui', 'cooperacao_beneficios', 'participar_projetos']:
            for palavra in palavras:
                count += df_filtrado[col].str.lower().str.contains(palavra, na=False).sum()
        contagem_palavras[tema] = count
    
    fig, ax = plt.subplots(figsize=(10, 5))
    temas = list(contagem_palavras.keys())
    contagens = list(contagem_palavras.values())
    bars = ax.barh(temas, contagens, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'], alpha=0.8, edgecolor='black')
    
    for bar, v in zip(bars, contagens):
        ax.text(v + 0.5, bar.get_y() + bar.get_height()/2, f'{v}', 
                va='center', fontweight='bold')
    
    ax.set_xlabel('Frequência')
    ax.set_title('Frequência de Temas nas Respostas Abertas')
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # Amostras de respostas
    st.subheader("Amostras de Respostas Abertas")
    
    col_resp1, col_resp2 = st.columns(2)
    
    with col_resp1:
        st.write("**Como tecnologia pode contribuir para gestão:**")
        amostras = df_filtrado['tecnologia_contribui'].dropna().unique()[:2]
        for i, resposta in enumerate(amostras, 1):
            with st.expander(f"Resposta {i}"):
                st.write(resposta)
    
    with col_resp2:
        st.write("**Benefícios da cooperação Adm × Engenharia:**")
        amostras = df_filtrado['cooperacao_beneficios'].dropna().unique()[:2]
        for i, resposta in enumerate(amostras, 1):
            with st.expander(f"Resposta {i}"):
                st.write(resposta)

# ═════════════════════════════════════════════════════════════════════════
# ABA 4: DADOS COMPLETOS
# ═════════════════════════════════════════════════════════════════════════

with tab4:
    
    st.subheader("Dados Completos")
    
    st.dataframe(
        df_filtrado[[
            'data_hora', 'idade', 'participou_pesquisa', 'conteudo_claro',
            'sistemas_aplicaveis', 'tecnologia_gestao', 'interacao_palestrantes', 'avaliacao_geral'
        ]].sort_values('data_hora', ascending=False),
        use_container_width=True,
        height=400
    )
    
    # Exportar
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar dados em CSV",
        data=csv,
        file_name="avaliacao_palestra.csv",
        mime="text/csv"
    )

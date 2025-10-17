"""
╔═══════════════════════════════════════════════════════════════════════╗
║    LIÇÃO 4: DASHBOARD PROFISSIONAL - TUDO JUNTO!                     ║
║                                                                       ║
║  Esta é a lição final! Você combina tudo que aprendeu:               ║
║                                                                       ║
║  ✨ Dados de arquivo real                                            ║
║  ✨ Filtros interativos                                              ║
║  ✨ Gráficos profissionais                                           ║
║  ✨ Design limpo e organizado                                        ║
║  ✨ Código bem comentado para você adaptar                           ║
║                                                                       ║
║  Para executar:                                                      ║
║  streamlit run 04_dashboard_profissional.py                          ║
║                                                                       ║
║  🎯 IMPORTANTE: Este arquivo é feito para você COPIAR E ADAPTAR!    ║
║     Use como template para seus próprios dashboards!                ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta


# ═══════════════════════════════════════════════════════════════════════
# PARTE 1: CONFIGURAÇÃO INICIAL
# ═══════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Dashboard Profissional",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configurar o estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'


# ═══════════════════════════════════════════════════════════════════════
# PARTE 2: FUNÇÕES AUXILIARES
# ═══════════════════════════════════════════════════════════════════════

@st.cache_data
def carregar_dados():
    """
    Carrega os dados do dashboard.
    
    Se você quer usar seu próprio arquivo:
    1. Substitua 'df = pd.DataFrame(...)' por:
       df = pd.read_excel('seu_arquivo.xlsx')
       # ou
       df = pd.read_csv('seu_arquivo.csv')
    
    2. Verifique os nomes das colunas
    3. Pronto! Seu arquivo será carregado
    """
    
    # Para este exemplo, criamos dados fictícios
    dados = {
        'Data': pd.date_range(start='2024-10-01', periods=365, freq='D'),
        'Produto': np.random.choice(
            ['Produto Premium', 'Produto Standard', 'Produto Básico', 'Produto Especial'],
            365
        ),
        'Categoria': np.random.choice(
            ['Eletrônicos', 'Moda', 'Casa', 'Saúde'],
            365
        ),
        'Regiao': np.random.choice(
            ['Sul', 'Sudeste', 'Centro-Oeste', 'Nordeste', 'Norte'],
            365
        ),
        'Quantidade': np.random.randint(1, 100, 365),
        'Preco_Unitario': np.random.uniform(20, 1000, 365),
        'Vendedor': np.random.choice(
            ['Ana Silva', 'Bruno Santos', 'Carlos Oliveira', 'Diana Costa', 'Eduardo Ferreira'],
            365
        ),
        'Status': np.random.choice(['Concluída', 'Pendente', 'Cancelada'], 365, p=[0.75, 0.15, 0.10])
    }
    
    df = pd.DataFrame(dados)
    
    # Calcular coluna de valor total
    df['Valor_Total'] = (df['Quantidade'] * df['Preco_Unitario']).round(2)
    
    # Adicionar mês para análises
    df['Mes'] = df['Data'].dt.strftime('%B/%Y')
    df['Mes_Numero'] = df['Data'].dt.month
    df['Ano'] = df['Data'].dt.year
    
    return df


def formatar_moeda(valor):
    """Formata um valor em moeda brasileira"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')


def criar_grafico_vendas_por_categoria(df_filtrado):
    """Cria gráfico de vendas por categoria"""
    dados_categoria = df_filtrado[df_filtrado['Status'] == 'Concluída'].groupby('Categoria')['Valor_Total'].sum().sort_values(ascending=False)
    
    if len(dados_categoria) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 5))
    cores = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd'][:len(dados_categoria)]
    
    barras = ax.bar(dados_categoria.index, dados_categoria.values, color=cores, edgecolor='black', linewidth=1.5)
    
    # Adicionar valores nas barras
    for barra in barras:
        altura = barra.get_height()
        ax.text(
            barra.get_x() + barra.get_width()/2.,
            altura,
            f'{altura:,.0f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold'
        )
    
    ax.set_xlabel('Categoria', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valor Total (R$)', fontsize=11, fontweight='bold')
    ax.set_title('💰 Vendas por Categoria', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    return fig


def criar_grafico_evolucao_temporal(df_filtrado):
    """Cria gráfico de evolução ao longo do tempo"""
    dados_tempo = df_filtrado[df_filtrado['Status'] == 'Concluída'].groupby('Data')['Valor_Total'].sum()
    
    if len(dados_tempo) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(14, 5))
    
    # Linha principal
    ax.plot(dados_tempo.index, dados_tempo.values, linewidth=2.5, color='#1f77b4', label='Vendas Diárias')
    
    # Área preenchida
    ax.fill_between(dados_tempo.index, dados_tempo.values, alpha=0.3, color='#1f77b4')
    
    # Média móvel (suaviza a linha)
    media_movel = dados_tempo.rolling(window=7).mean()
    ax.plot(media_movel.index, media_movel.values, linewidth=2, color='red', linestyle='--', label='Média Móvel 7 dias', alpha=0.7)
    
    ax.set_xlabel('Data', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valor (R$)', fontsize=11, fontweight='bold')
    ax.set_title('📈 Evolução de Vendas ao Longo do Tempo', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig


def criar_grafico_desempenho_vendedor(df_filtrado):
    """Cria gráfico de desempenho por vendedor"""
    dados_vendedor = df_filtrado[df_filtrado['Status'] == 'Concluída'].groupby('Vendedor').agg({
        'Valor_Total': 'sum',
        'Quantidade': 'count'
    }).sort_values('Valor_Total', ascending=True)
    
    if len(dados_vendedor) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ax.barh(dados_vendedor.index, dados_vendedor['Valor_Total'], color='#ff7f0e', edgecolor='black', linewidth=1.5)
    
    # Adicionar valores
    for i, v in enumerate(dados_vendedor['Valor_Total'].values):
        ax.text(v + 1000, i, f'R$ {v:,.0f}', va='center', fontweight='bold', fontsize=10)
    
    ax.set_xlabel('Valor Total Vendido (R$)', fontsize=11, fontweight='bold')
    ax.set_title('👥 Desempenho dos Vendedores', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    
    return fig


def criar_grafico_pizza_regiao(df_filtrado):
    """Cria gráfico de pizza por região"""
    dados_regiao = df_filtrado[df_filtrado['Status'] == 'Concluída'].groupby('Regiao')['Valor_Total'].sum()
    
    if len(dados_regiao) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    cores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc'][:len(dados_regiao)]
    
    wedges, texts, autotexts = ax.pie(
        dados_regiao,
        labels=dados_regiao.index,
        autopct='%1.1f%%',
        colors=cores,
        startangle=90,
        explode=[0.05] * len(dados_regiao)
    )
    
    # Melhorar fonte
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title('🗺️ Distribuição de Vendas por Região', fontsize=13, fontweight='bold')
    
    plt.tight_layout()
    
    return fig


# ═══════════════════════════════════════════════════════════════════════
# PARTE 3: INTERFACE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════

st.title("💼 Dashboard de Vendas Profissional")
st.markdown("""
Este é um dashboard **completo** e **profissional** que você pode adaptar para seus dados.
Use os filtros da barra lateral para explorar os dados! 📊
""")


# ═══════════════════════════════════════════════════════════════════════
# PARTE 4: BARRA LATERAL COM FILTROS
# ═══════════════════════════════════════════════════════════════════════

st.sidebar.header("🔍 Filtros do Dashboard")

# Carregar dados (uma única vez)
df = carregar_dados()

# ---- Filtro: Período ----
st.sidebar.subheader("📅 Período")

data_inicio = st.sidebar.date_input(
    "Data Inicial",
    value=df['Data'].min(),
    min_value=df['Data'].min(),
    max_value=df['Data'].max()
)

data_fim = st.sidebar.date_input(
    "Data Final",
    value=df['Data'].max(),
    min_value=df['Data'].min(),
    max_value=df['Data'].max()
)

# ---- Filtro: Região ----
st.sidebar.subheader("🗺️ Região")

todas_regioes = df['Regiao'].unique().tolist()
regioes_selecionadas = st.sidebar.multiselect(
    "Selecione as regiões",
    options=todas_regioes,
    default=todas_regioes
)

# ---- Filtro: Categoria ----
st.sidebar.subheader("📂 Categoria")

todas_categorias = df['Categoria'].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as categorias",
    options=todas_categorias,
    default=todas_categorias
)

# ---- Filtro: Vendedor ----
st.sidebar.subheader("👤 Vendedor")

todos_vendedores = df['Vendedor'].unique().tolist()
vendedores_selecionados = st.sidebar.multiselect(
    "Selecione os vendedores",
    options=todos_vendedores,
    default=todos_vendedores
)

# ---- Filtro: Status ----
st.sidebar.subheader("✅ Status da Venda")

todos_status = df['Status'].unique().tolist()
status_selecionados = st.sidebar.multiselect(
    "Selecione os status",
    options=todos_status,
    default=todos_status
)

# ---- Botão de Reset ----
if st.sidebar.button("🔄 Resetar Todos os Filtros", use_container_width=True):
    st.rerun()

st.sidebar.divider()


# ═══════════════════════════════════════════════════════════════════════
# PARTE 5: APLICAR FILTROS
# ═══════════════════════════════════════════════════════════════════════

df_filtrado = df[
    (df['Data'] >= pd.Timestamp(data_inicio)) &
    (df['Data'] <= pd.Timestamp(data_fim)) &
    (df['Regiao'].isin(regioes_selecionadas)) &
    (df['Categoria'].isin(categorias_selecionadas)) &
    (df['Vendedor'].isin(vendedores_selecionados)) &
    (df['Status'].isin(status_selecionados))
]

# Mostrar quantidade de registros
st.sidebar.metric(
    label="📊 Registros",
    value=f"{len(df_filtrado)} de {len(df)}"
)


# ═══════════════════════════════════════════════════════════════════════
# PARTE 6: INDICADORES PRINCIPAIS (KPIs)
# ═══════════════════════════════════════════════════════════════════════

st.header("📊 Indicadores Principais")

# Calcular métricas apenas de vendas concluídas
df_concluidas = df_filtrado[df_filtrado['Status'] == 'Concluída']

valor_total = df_concluidas['Valor_Total'].sum() if len(df_concluidas) > 0 else 0
quantidade_vendas = len(df_concluidas)
ticket_medio = df_concluidas['Valor_Total'].mean() if len(df_concluidas) > 0 else 0
produto_mais_vendido = df_concluidas['Produto'].mode()[0] if len(df_concluidas) > 0 else 'N/A'

# Mostrar em 4 colunas
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric(
        label="💰 Valor Total",
        value=formatar_moeda(valor_total),
        delta="Vendas Concluídas"
    )

with col_kpi2:
    st.metric(
        label="📈 Quantidade de Vendas",
        value=f"{quantidade_vendas:,}",
        delta="Transações"
    )

with col_kpi3:
    st.metric(
        label="🎫 Ticket Médio",
        value=formatar_moeda(ticket_medio),
        delta="Valor Médio"
    )

with col_kpi4:
    st.metric(
        label="🏆 Produto Mais Vendido",
        value=produto_mais_vendido[:15] + "..." if len(produto_mais_vendido) > 15 else produto_mais_vendido,
        delta="Top Vendedor"
    )


# ═══════════════════════════════════════════════════════════════════════
# PARTE 7: GRÁFICOS PRINCIPAIS
# ═══════════════════════════════════════════════════════════════════════

st.header("📈 Análises Visuais")

# Linha 1: Dois gráficos lado a lado
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    fig1 = criar_grafico_vendas_por_categoria(df_filtrado)
    if fig1:
        st.pyplot(fig1)
    else:
        st.info("Sem dados para mostrar com os filtros selecionados")

with col_grafico2:
    fig2 = criar_grafico_pizza_regiao(df_filtrado)
    if fig2:
        st.pyplot(fig2)
    else:
        st.info("Sem dados para mostrar com os filtros selecionados")

# Gráfico em toda a largura: Evolução temporal
fig3 = criar_grafico_evolucao_temporal(df_filtrado)
if fig3:
    st.pyplot(fig3)
else:
    st.info("Sem dados para mostrar com os filtros selecionados")

# Gráfico: Desempenho do vendedor
fig4 = criar_grafico_desempenho_vendedor(df_filtrado)
if fig4:
    st.pyplot(fig4)
else:
    st.info("Sem dados para mostrar com os filtros selecionados")


# ═══════════════════════════════════════════════════════════════════════
# PARTE 8: DISTRIBUIÇÃO DE STATUS
# ═══════════════════════════════════════════════════════════════════════

st.header("✅ Status das Vendas")

col_status1, col_status2, col_status3 = st.columns(3)

vendas_concluidas = len(df_filtrado[df_filtrado['Status'] == 'Concluída'])
vendas_pendentes = len(df_filtrado[df_filtrado['Status'] == 'Pendente'])
vendas_canceladas = len(df_filtrado[df_filtrado['Status'] == 'Cancelada'])

with col_status1:
    st.metric(label="✅ Concluídas", value=vendas_concluidas, delta="Sucesso")

with col_status2:
    st.metric(label="⏳ Pendentes", value=vendas_pendentes, delta="Em Andamento")

with col_status3:
    st.metric(label="❌ Canceladas", value=vendas_canceladas, delta="Não Concluído")


# ═══════════════════════════════════════════════════════════════════════
# PARTE 9: TABELA DE DADOS DETALHADOS
# ═══════════════════════════════════════════════════════════════════════

st.header("📋 Dados Detalhados")

with st.expander("Clique para expandir a tabela completa"):
    if len(df_filtrado) > 0:
        # Colunas a mostrar
        colunas_mostrar = ['Data', 'Produto', 'Categoria', 'Regiao', 'Quantidade', 'Valor_Total', 'Vendedor', 'Status']
        
        st.dataframe(
            df_filtrado[colunas_mostrar].sort_values('Data', ascending=False),
            use_container_width=True,
            height=400
        )
    else:
        st.warning("Nenhum dado para mostrar com os filtros selecionados.")


# ═══════════════════════════════════════════════════════════════════════
# PARTE 10: RESUMO E PRÓXIMOS PASSOS
# ═══════════════════════════════════════════════════════════════════════

st.divider()

st.header("🎓 Como Adaptar Este Dashboard para Seus Dados")

with st.expander("📖 Clique para ler o guia completo"):
    st.write("""
    ### Passo 1: Prepare seu arquivo
    
    1. Salve seus dados em **Excel (.xlsx)** ou **CSV**
    2. Certifique-se de que tem cabeçalhos (nomes das colunas)
    3. Sem linhas vazias no meio
    4. Coloque na mesma pasta deste arquivo
    
    ### Passo 2: Modifique a função `carregar_dados()`
    
    Encontre esta parte do código (perto do início):
    
    ```python
    @st.cache_data
    def carregar_dados():
        df = pd.DataFrame(dados)
        ...
    ```
    
    E substitua por:
    
    ```python
    @st.cache_data
    def carregar_dados():
        # Para Excel
        df = pd.read_excel('seu_arquivo.xlsx')
        
        # OU para CSV
        df = pd.read_csv('seu_arquivo.csv')
        
        return df
    ```
    
    ### Passo 3: Mude os nomes das colunas
    
    Se suas colunas têm nomes diferentes, ajuste em todos os lugares onde aparecem.
    
    Por exemplo, se em vez de 'Produto' você tem 'Item':
    - Procure por `'Produto'` no código
    - Substitua por `'Item'` em todos os lugares
    
    ### Passo 4: Adicione/remova filtros
    
    Para adicionar um novo filtro, procure por:
    ```python
    st.sidebar.subheader("📂 Categoria")
    
    todas_categorias = df['Categoria'].unique().tolist()
    categorias_selecionadas = st.sidebar.multiselect(...)
    ```
    
    E copie este padrão para sua nova coluna.
    
    ### Exemplo: Adicionar filtro de "Cidade"
    
    ```python
    st.sidebar.subheader("🏙️ Cidade")
    
    todas_cidades = df['Cidade'].unique().tolist()
    cidades_selecionadas = st.sidebar.multiselect(
        "Selecione as cidades",
        options=todas_cidades,
        default=todas_cidades
    )
    ```
    
    E adicione ao filtro:
    ```python
    df_filtrado = df[
        ... outros filtros ...
        (df['Cidade'].isin(cidades_selecionadas)) &
    ]
    ```
    
    ### Passo 5: Teste!
    
    ```bash
    streamlit run 04_dashboard_profissional.py
    ```
    """)

st.success("""
### ✅ Parabéns!

Você completou as 4 lições de Streamlit!

**O que você sabe fazer agora:**
✔️ Criar dashboards simples
✔️ Ler dados de arquivos
✔️ Adicionar filtros interativos  
✔️ Criar gráficos profissionais
✔️ Adaptar para qualquer tipo de dado

**Próximos passos:**
1. Use este arquivo como template
2. Adapte para seus dados
3. Compartilhe com sua equipe
4. Melhore aos poucos conforme aprende

**Dúvidas?**
- Google: "streamlit [sua dúvida]"
- Documentação: https://docs.streamlit.io
- Stack Overflow: busque por sua pergunta

Boa sorte! 🚀
""")

"""
╔═══════════════════════════════════════════════════════════════════════╗
║         LIÇÃO 3: DASHBOARD INTERATIVO COM FILTROS                   ║
║                                                                       ║
║  Nesta lição você aprenderá:                                         ║
║  • Como adicionar filtros e seletores                                ║
║  • Como deixar o usuário escolher o que ver                          ║
║  • Como criar dashboards dinâmicos e responsivos                     ║
║  • Como usar a sidebar para melhor organização                       ║
║                                                                       ║
║  Para executar:                                                      ║
║  streamlit run 03_dashboard_interativo.py                            ║
║                                                                       ║
║  Esta é a lição mais importante! Aqui seu dashboard fica vivo!      ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


# CONFIGURAÇÃO DA PÁGINA
# ═══════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Dashboard Interativo",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# TÍTULO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════
st.title("🎛️ Dashboard Interativo com Filtros")
st.write("""
Bem-vindo ao dashboard **interativo**!

Aqui você aprenderá a criar dashboards que **respondem** aos cliques do usuário.
Explore os filtros da barra lateral e veja os gráficos mudarem em tempo real!
""")


# CRIAR DADOS DE EXEMPLO
# ═══════════════════════════════════════════════════════════════════════
@st.cache_data  # Isso faz Streamlit não recalcular toda vez que a página atualiza
def criar_dados_vendas():
    """
    Função que cria dados fictícios de vendas.
    O @st.cache_data melhora a performance!
    """
    
    # Criar 100 linhas de dados
    dados = {
        'Data': pd.date_range(start='2025-01-01', periods=100, freq='D'),
        'Produto': np.random.choice(['Produto A', 'Produto B', 'Produto C', 'Produto D'], 100),
        'Categoria': np.random.choice(['Eletrônicos', 'Roupas', 'Alimentos', 'Livros'], 100),
        'Regiao': np.random.choice(['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul'], 100),
        'Quantidade': np.random.randint(1, 50, 100),
        'Preco_Unitario': np.random.uniform(10, 500, 100),
        'Vendedor': np.random.choice(['João Silva', 'Maria Santos', 'Pedro Oliveira', 'Ana Costa'], 100),
        'Status_Venda': np.random.choice(['Concluída', 'Pendente', 'Cancelada'], 100, p=[0.7, 0.2, 0.1])
    }
    
    df = pd.DataFrame(dados)
    df['Valor_Total'] = (df['Quantidade'] * df['Preco_Unitario']).round(2)
    df['Data_Formatada'] = df['Data'].dt.strftime('%d/%m/%Y')
    
    return df

# Carregar os dados
df_vendas = criar_dados_vendas()


# SEÇÃO 1: CRIAR FILTROS NA BARRA LATERAL
# ═══════════════════════════════════════════════════════════════════════
st.sidebar.header("🔍 Filtros")
st.sidebar.write("Use estes filtros para personalizar seu dashboard!")

# Filtro 1: Período (Data)
st.sidebar.subheader("📅 Período")

data_inicio, data_fim = st.sidebar.date_input(
    label="Selecione o intervalo de datas",
    value=[df_vendas['Data'].min(), df_vendas['Data'].max()],
    min_value=df_vendas['Data'].min(),
    max_value=df_vendas['Data'].max()
)

# Filtro 2: Região
st.sidebar.subheader("🗺️ Região")

regioes_disponiveis = df_vendas['Regiao'].unique().tolist()
regioes_selecionadas = st.sidebar.multiselect(
    label="Escolha as regiões",
    options=regioes_disponiveis,
    default=regioes_disponiveis  # Por padrão, seleciona todas
)

# Filtro 3: Categoria
st.sidebar.subheader("📂 Categoria")

categorias_disponiveis = df_vendas['Categoria'].unique().tolist()
categorias_selecionadas = st.sidebar.multiselect(
    label="Escolha as categorias",
    options=categorias_disponiveis,
    default=categorias_disponiveis
)

# Filtro 4: Vendedor
st.sidebar.subheader("👤 Vendedor")

vendedores_disponiveis = df_vendas['Vendedor'].unique().tolist()
vendedores_selecionados = st.sidebar.multiselect(
    label="Escolha os vendedores",
    options=vendedores_disponiveis,
    default=vendedores_disponiveis
)

# Filtro 5: Status da Venda
st.sidebar.subheader("✅ Status da Venda")

status_disponiveis = df_vendas['Status_Venda'].unique().tolist()
status_selecionados = st.sidebar.multiselect(
    label="Escolha os status",
    options=status_disponiveis,
    default=status_disponiveis
)

# Botão para resetar todos os filtros
if st.sidebar.button("🔄 Resetar Todos os Filtros"):
    st.rerun()


# SEÇÃO 2: APLICAR OS FILTROS AOS DADOS
# ═══════════════════════════════════════════════════════════════════════
# Aqui filtramos os dados conforme o que o usuário escolheu

df_filtrado = df_vendas[
    (df_vendas['Data'] >= pd.Timestamp(data_inicio)) &
    (df_vendas['Data'] <= pd.Timestamp(data_fim)) &
    (df_vendas['Regiao'].isin(regioes_selecionadas)) &
    (df_vendas['Categoria'].isin(categorias_selecionadas)) &
    (df_vendas['Vendedor'].isin(vendedores_selecionados)) &
    (df_vendas['Status_Venda'].isin(status_selecionados))
]

st.sidebar.divider()
st.sidebar.write(f"📊 **Registros encontrados:** {len(df_filtrado)} de {len(df_vendas)}")


# SEÇÃO 3: MOSTRAR INDICADORES PRINCIPAIS (KPIs)
# ═══════════════════════════════════════════════════════════════════════
st.header("📊 Indicadores Principais")

# Calcular as métricas
valor_total_vendido = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída']['Valor_Total'].sum()
quantidade_vendas = len(df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'])
ticket_medio = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída']['Valor_Total'].mean()
quantidade_vendedores = df_filtrado['Vendedor'].nunique()

# Mostrar em 4 colunas
col_total, col_qtd, col_ticket, col_vendedores = st.columns(4)

with col_total:
    st.metric(
        label="💰 Valor Total Vendido",
        value=f"R$ {valor_total_vendido:,.2f}",
        help="Apenas vendas concluídas"
    )

with col_qtd:
    st.metric(
        label="📈 Quantidade de Vendas",
        value=quantidade_vendas,
        help="Quantas vendas foram completadas"
    )

with col_ticket:
    st.metric(
        label="🎫 Ticket Médio",
        value=f"R$ {ticket_medio:,.2f}",
        help="Valor médio por venda"
    )

with col_vendedores:
    st.metric(
        label="👥 Vendedores",
        value=quantidade_vendedores,
        help="Quantos vendedores nos dados filtrados"
    )


# SEÇÃO 4: VISUALIZAR OS DADOS FILTRADOS
# ═══════════════════════════════════════════════════════════════════════
st.header("📋 Dados Filtrados")

if len(df_filtrado) > 0:
    # Mostrar os dados em uma tabela
    st.dataframe(
        df_filtrado[['Data_Formatada', 'Produto', 'Categoria', 'Regiao', 
                     'Vendedor', 'Quantidade', 'Valor_Total', 'Status_Venda']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados. Tente ajustar os filtros!")


# SEÇÃO 5: GRÁFICOS INTERATIVOS (responde aos filtros)
# ═══════════════════════════════════════════════════════════════════════
st.header("📈 Análises Visuais")

if len(df_filtrado) > 0:
    
    # Dividir em 2 colunas para os gráficos
    col_grafico1, col_grafico2 = st.columns(2)
    
    with col_grafico1:
        st.subheader("Vendas por Região")
        
        vendas_regiao = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'].groupby('Regiao')['Valor_Total'].sum().sort_values(ascending=False)
        
        if len(vendas_regiao) > 0:
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            ax1.bar(vendas_regiao.index, vendas_regiao.values, color='#2ca02c')
            ax1.set_xlabel('Região', fontsize=11)
            ax1.set_ylabel('Valor Vendido (R$)', fontsize=11)
            ax1.set_title('Desempenho por Região', fontsize=12, fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='y')
            
            for i, v in enumerate(vendas_regiao.values):
                ax1.text(i, v + 100, f'R$ {v:.0f}', ha='center', fontweight='bold')
            
            st.pyplot(fig1)
        else:
            st.info("Sem dados para mostrar com os filtros selecionados")
    
    with col_grafico2:
        st.subheader("Vendas por Categoria")
        
        vendas_categoria = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'].groupby('Categoria')['Valor_Total'].sum().sort_values(ascending=False)
        
        if len(vendas_categoria) > 0:
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            cores = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
            ax2.pie(vendas_categoria, labels=vendas_categoria.index, autopct='%1.1f%%', colors=cores)
            ax2.set_title('Proporção por Categoria', fontsize=12, fontweight='bold')
            st.pyplot(fig2)
        else:
            st.info("Sem dados para mostrar com os filtros selecionados")
    
    # Gráfico de linha: Evolução temporal
    st.subheader("📅 Evolução de Vendas ao Longo do Tempo")
    
    vendas_diarias = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'].groupby('Data')['Valor_Total'].sum()
    
    if len(vendas_diarias) > 0:
        fig3, ax3 = plt.subplots(figsize=(14, 6))
        ax3.plot(vendas_diarias.index, vendas_diarias.values, marker='o', linewidth=2, markersize=6, color='#1f77b4')
        ax3.fill_between(vendas_diarias.index, vendas_diarias.values, alpha=0.3, color='#1f77b4')
        ax3.set_xlabel('Data', fontsize=11)
        ax3.set_ylabel('Vendas Diárias (R$)', fontsize=11)
        ax3.set_title('Evolução de Vendas', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        st.pyplot(fig3)
    else:
        st.info("Sem dados para mostrar com os filtros selecionados")
    
    # Gráfico: Performance por Vendedor
    st.subheader("👤 Desempenho dos Vendedores")
    
    vendas_vendedor = df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'].groupby('Vendedor')['Valor_Total'].sum().sort_values(ascending=True)
    
    if len(vendas_vendedor) > 0:
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.barh(vendas_vendedor.index, vendas_vendedor.values, color='#ff7f0e')
        ax4.set_xlabel('Valor Vendido (R$)', fontsize=11)
        ax4.set_title('Total Vendido por Vendedor', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3, axis='x')
        
        for i, v in enumerate(vendas_vendedor.values):
            ax4.text(v + 50, i, f'R$ {v:.2f}', va='center', fontweight='bold', fontsize=9)
        
        st.pyplot(fig4)
    else:
        st.info("Sem dados para mostrar com os filtros selecionados")


# SEÇÃO 6: RESUMO E DISTRIBUIÇÃO DE STATUS
# ═══════════════════════════════════════════════════════════════════════
st.header("✅ Status das Vendas")

col_status1, col_status2, col_status3 = st.columns(3)

vendas_concluidas = len(df_filtrado[df_filtrado['Status_Venda'] == 'Concluída'])
vendas_pendentes = len(df_filtrado[df_filtrado['Status_Venda'] == 'Pendente'])
vendas_canceladas = len(df_filtrado[df_filtrado['Status_Venda'] == 'Cancelada'])

with col_status1:
    st.metric(label="✅ Concluídas", value=vendas_concluidas)

with col_status2:
    st.metric(label="⏳ Pendentes", value=vendas_pendentes)

with col_status3:
    st.metric(label="❌ Canceladas", value=vendas_canceladas)


# SEÇÃO 7: PRÓXIMOS PASSOS
# ═══════════════════════════════════════════════════════════════════════
st.divider()

st.header("🎓 O Que Você Aprendeu")

with st.expander("Clique para ver o resumo"):
    st.write("""
    ✅ Como adicionar filtros interativos
    ✅ Como usar a sidebar para organizar filtros
    ✅ Como aplicar filtros aos dados
    ✅ Como criar gráficos que respondem aos filtros
    ✅ Como mostrar KPIs (indicadores principais)
    ✅ Como melhorar a experiência do usuário
    
    ### 💡 Dicas de Interatividade:
    
    1. **Sempre mostre quantos registros restaram** - As pessoas querem saber se os filtros funcionaram
    2. **Botão de reset** - Facilita voltar aos dados originais
    3. **Avisos quando não há dados** - Não deixe a página em branco
    4. **Carregue dados uma vez** - Use `@st.cache_data` para melhor performance
    5. **Atualize em tempo real** - Streamlit faz isso automaticamente!
    """)

st.success("""
### 🚀 Próximo Passo: Lição 4 - Dashboard Profissional Completo

A Lição 4 combina tudo que você aprendeu com:
✨ Melhor design
✨ Mais funcionalidades
✨ Exemplos práticos prontos para usar
✨ Dicas para adaptar aos seus dados

Execute: `streamlit run 04_dashboard_profissional.py`
""")

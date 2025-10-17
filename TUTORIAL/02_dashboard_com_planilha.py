"""
╔═══════════════════════════════════════════════════════════════════════╗
║      LIÇÃO 2: LENDO DADOS DE ARQUIVO E CRIANDO DASHBOARD            ║
║                                                                       ║
║  Nesta lição você aprenderá:                                         ║
║  • Como ler dados de um arquivo Excel ou CSV                         ║
║  • Como explorar e entender seus dados                               ║
║  • Como criar múltiplos gráficos com seus dados reais                ║
║  • Como tratar problemas comuns com dados                            ║
║                                                                       ║
║  Para executar:                                                      ║
║  streamlit run 02_dashboard_com_planilha.py                          ║
║                                                                       ║
║  Antes disso, coloque seu arquivo na pasta!                          ║
║  (arquivo.xlsx ou arquivo.csv)                                       ║
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
    page_title="Dashboard com Dados Reais",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# TÍTULO
# ═══════════════════════════════════════════════════════════════════════
st.title("📊 Dashboard com Dados de Arquivo")
st.write("""
Nesta lição, você aprenderá a ler dados de um arquivo Excel ou CSV 
e criar um dashboard profissional com eles!
""")


# SEÇÃO 1: ENTENDER COMO LER ARQUIVO
# ═══════════════════════════════════════════════════════════════════════
st.header("1️⃣ Como Ler Seus Dados")

with st.expander("ℹ️ Clique para entender como funciona"):
    st.write("""
    ### O Que Vamos Fazer?
    
    1. **Criar dados de exemplo** (para você testar agora)
    2. **Mostrar como ler arquivos** (para quando tiver seus dados)
    3. **Limpar e preparar os dados** (tratamento de erros)
    4. **Criar visualizações** (gráficos bonitos)
    
    ### Por Que Fazer Isso?
    
    - Dados brutos raramente estão perfeitos
    - Precisamos verificar se estão corretos
    - Pequenos problemas podem quebrar tudo
    - Tratar dados é 80% do trabalho!
    """)


# SEÇÃO 2: CRIAR ARQUIVO DE EXEMPLO
# ═══════════════════════════════════════════════════════════════════════
st.header("2️⃣ Criando Dados de Exemplo")

# Criar dados fictícios de vendas de uma loja
# Imagine que você tem uma loja e vendeu esses produtos:
dados_exemplo = {
    'Data': pd.date_range(start='2025-01-01', periods=30, freq='D'),
    'Produto': np.random.choice(['Camiseta', 'Calça', 'Meia', 'Jaqueta'], 30),
    'Categoria': np.random.choice(['Roupas', 'Acessórios'], 30),
    'Quantidade_Vendida': np.random.randint(1, 20, 30),
    'Preco_Unitario': np.random.uniform(20, 200, 30),
    'Vendedor': np.random.choice(['João', 'Maria', 'Pedro', 'Ana'], 30),
}

# Transformar em DataFrame (tabela)
df_dados = pd.DataFrame(dados_exemplo)

# Calcular o valor total da venda (Quantidade × Preço)
df_dados['Valor_Total'] = df_dados['Quantidade_Vendida'] * df_dados['Preco_Unitario']

# Arredondar valores de dinheiro para 2 casas decimais
df_dados['Preco_Unitario'] = df_dados['Preco_Unitario'].round(2)
df_dados['Valor_Total'] = df_dados['Valor_Total'].round(2)

st.write("✅ Dados de exemplo criados com sucesso!")
st.dataframe(df_dados, use_container_width=True)


# SEÇÃO 3: EXPLORAR E ENTENDER OS DADOS
# ═══════════════════════════════════════════════════════════════════════
st.header("3️⃣ Explorando os Dados")

# Dividir em 3 colunas para mostrar informações lado a lado
col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.metric(
        label="📊 Total de Linhas",
        value=len(df_dados),
        help="Quantos registros temos no total"
    )

with col_info2:
    st.metric(
        label="📋 Total de Colunas",
        value=len(df_dados.columns),
        help="Quantas informações diferentes temos"
    )

with col_info3:
    st.metric(
        label="💰 Valor Total Vendido",
        value=f"R$ {df_dados['Valor_Total'].sum():,.2f}",
        help="Soma de todas as vendas"
    )

# Mostrar informações sobre cada coluna
st.subheader("Informações sobre cada coluna:")
st.write("""
| Coluna | O que é | Tipo |
|--------|---------|------|
| Data | Quando a venda aconteceu | Data |
| Produto | O que foi vendido | Texto |
| Categoria | Tipo do produto | Texto |
| Quantidade_Vendida | Quantas unidades | Número |
| Preco_Unitario | Preço de 1 unidade | Valor |
| Vendedor | Quem fez a venda | Texto |
| Valor_Total | Quantidade × Preço | Valor |
""")


# SEÇÃO 4: ANÁLISE POR CATEGORIA
# ═══════════════════════════════════════════════════════════════════════
st.header("4️⃣ Análise por Categoria")

# Agrupar dados por categoria e somar o valor total
vendas_por_categoria = df_dados.groupby('Categoria')['Valor_Total'].sum().sort_values(ascending=False)

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Gráfico de Pizza - Proporção de Vendas")
    
    figura_pizza, eixo_pizza = plt.subplots(figsize=(8, 6))
    eixo_pizza.pie(
        vendas_por_categoria,
        labels=vendas_por_categoria.index,
        autopct='%1.1f%%',  # Mostra porcentagem
        colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    )
    eixo_pizza.set_title('Proporção de Vendas por Categoria', fontsize=14, fontweight='bold')
    st.pyplot(figura_pizza)

with col_grafico2:
    st.subheader("Tabela Resumida")
    
    # Criar tabela com resumo
    resumo_categoria = df_dados.groupby('Categoria').agg({
        'Valor_Total': ['sum', 'mean', 'count']
    }).round(2)
    
    resumo_categoria.columns = ['Total Vendido', 'Média por Venda', 'Quantidade de Vendas']
    st.dataframe(resumo_categoria, use_container_width=True)


# SEÇÃO 5: ANÁLISE POR VENDEDOR
# ═══════════════════════════════════════════════════════════════════════
st.header("5️⃣ Análise por Vendedor")

# Agrupar por vendedor
vendas_por_vendedor = df_dados.groupby('Vendedor')['Valor_Total'].sum().sort_values(ascending=False)

figura_barras_vendedor, eixo_barras_vendedor = plt.subplots(figsize=(12, 5))

# Cores diferentes para cada vendedor
cores_vendedor = ['#2ca02c', '#ff7f0e', '#d62728', '#9467bd']
barras = eixo_barras_vendedor.bar(
    vendas_por_vendedor.index,
    vendas_por_vendedor.values,
    color=cores_vendedor
)

# Adicionar valores no topo das barras
for barra in barras:
    altura = barra.get_height()
    eixo_barras_vendedor.text(
        barra.get_x() + barra.get_width()/2.,
        altura,
        f'R$ {altura:.2f}',
        ha='center',
        va='bottom',
        fontsize=11,
        fontweight='bold'
    )

eixo_barras_vendedor.set_xlabel('Vendedor', fontsize=12)
eixo_barras_vendedor.set_ylabel('Valor Total Vendido (R$)', fontsize=12)
eixo_barras_vendedor.set_title('Desempenho de Vendas por Vendedor', fontsize=14, fontweight='bold')
eixo_barras_vendedor.grid(True, alpha=0.3, axis='y')

st.pyplot(figura_barras_vendedor)


# SEÇÃO 6: EVOLUÇÃO TEMPORAL
# ═══════════════════════════════════════════════════════════════════════
st.header("6️⃣ Evolução de Vendas ao Longo do Tempo")

# Agrupar por data (diária)
vendas_por_dia = df_dados.groupby('Data')['Valor_Total'].sum()

figura_linha_temporal, eixo_linha_temporal = plt.subplots(figsize=(14, 6))

eixo_linha_temporal.plot(
    vendas_por_dia.index,
    vendas_por_dia.values,
    marker='o',
    linewidth=2,
    markersize=6,
    color='#1f77b4'
)

eixo_linha_temporal.fill_between(
    vendas_por_dia.index,
    vendas_por_dia.values,
    alpha=0.3,
    color='#1f77b4'
)

eixo_linha_temporal.set_xlabel('Data', fontsize=12)
eixo_linha_temporal.set_ylabel('Vendas Diárias (R$)', fontsize=12)
eixo_linha_temporal.set_title('Evolução de Vendas ao Longo dos Dias', fontsize=14, fontweight='bold')
eixo_linha_temporal.grid(True, alpha=0.3)

plt.xticks(rotation=45)
st.pyplot(figura_linha_temporal)


# SEÇÃO 7: ANÁLISE POR PRODUTO
# ═══════════════════════════════════════════════════════════════════════
st.header("7️⃣ Análise por Produto")

vendas_por_produto = df_dados.groupby('Produto')['Valor_Total'].sum().sort_values(ascending=True)

figura_barras_produto, eixo_barras_produto = plt.subplots(figsize=(10, 6))

eixo_barras_produto.barh(
    vendas_por_produto.index,
    vendas_por_produto.values,
    color='#ff7f0e'
)

eixo_barras_produto.set_xlabel('Valor Total Vendido (R$)', fontsize=12)
eixo_barras_produto.set_title('Vendas Totais por Tipo de Produto', fontsize=14, fontweight='bold')
eixo_barras_produto.grid(True, alpha=0.3, axis='x')

# Adicionar valores nas barras
for i, v in enumerate(vendas_por_produto.values):
    eixo_barras_produto.text(v + 50, i, f'R$ {v:.2f}', va='center', fontweight='bold')

st.pyplot(figura_barras_produto)


# SEÇÃO 8: COMO USAR COM SEUS DADOS
# ═══════════════════════════════════════════════════════════════════════
st.header("🔄 Como Adaptar Para Seus Dados")

st.write("""
### Passo 1: Prepare seu arquivo
- Salve seus dados em **Excel (.xlsx)** ou **CSV**
- Coloque na mesma pasta que este arquivo Python
- Verifique se não tem linhas vazias

### Passo 2: Mude este código
Procure por esta linha (está no topo, não contamos):

```python
# Substitua isso:
df_dados = pd.read_excel('seu_arquivo.xlsx')

# Ou, se for CSV:
df_dados = pd.read_csv('seu_arquivo.csv')
```

### Passo 3: Adapte as análises
- Se seus dados têm outras colunas, crie novos gráficos!
- Se seus dados usam outros nomes, mude no código

### Exemplo: Se você tem dados de "Clientes"
""")

st.code("""
# Ler o arquivo
df_clientes = pd.read_csv('clientes.csv')

# Ver as primeiras linhas
st.dataframe(df_clientes.head())

# Contar clientes por região
clientes_por_regiao = df_clientes.groupby('Região').size()

# Visualizar em gráfico
st.bar_chart(clientes_por_regiao)
""", language='python')

st.divider()

st.success("""
✅ **Parabéns!**

Você aprendeu:
- ✔️ Como ler arquivos Excel e CSV
- ✔️ Como explorar seus dados
- ✔️ Como criar múltiplos gráficos
- ✔️ Como adaptar para seus dados

**Próximo passo: Lição 3 - Dashboard Interativo**
Execute: `streamlit run 03_dashboard_interativo.py`
""")

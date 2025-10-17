"""
╔═══════════════════════════════════════════════════════════════════════╗
║         LIÇÃO 1: SEU PRIMEIRO DASHBOARD COM STREAMLIT               ║
║                                                                       ║
║  Nesta lição você aprenderá:                                         ║
║  • Como o Streamlit funciona (é bem simples!)                        ║
║  • Como escrever e executar seu primeiro código                      ║
║  • Como criar seu primeiro gráfico                                   ║
║                                                                       ║
║  Para executar este arquivo:                                         ║
║  1. Abra o terminal na pasta deste arquivo                           ║
║  2. Digite: streamlit run 01_primeiro_dashboard.py                   ║
║  3. Aperte Enter                                                     ║
║                                                                       ║
║  Sua página abrirá automaticamente no navegador!                     ║
╚═══════════════════════════════════════════════════════════════════════╝
"""

# PASSO 1: Importar as bibliotecas que vamos usar
# ═══════════════════════════════════════════════════════════════════════
# Streamlit é como um "pintor" que desenha na tela para você
import streamlit as st

# Pandas é para trabalhar com dados (imagina um Excel turbinado)
import pandas as pd

# Matplotlib é para fazer gráficos
import matplotlib.pyplot as plt

# Numpy é para fazer contas matemáticas
import numpy as np


# PASSO 2: Configurar a página (design, título, etc)
# ═══════════════════════════════════════════════════════════════════════
# st.set_page_config() configura como o Streamlit vai aparecer
st.set_page_config(
    page_title="Meu Primeiro Dashboard",  # Nome que aparece na aba do navegador
    page_icon="📊",                        # Emoji que aparece na aba
    layout="wide",                         # "wide" = usa toda a tela; "centered" = centralizado
    initial_sidebar_state="expanded"       # "expanded" = barra lateral aberta
)


# PASSO 3: Criar o título da página
# ═══════════════════════════════════════════════════════════════════════
st.title("🎯 Bem-vindo ao Seu Primeiro Dashboard!")

# st.write() é como print(), mas mostra na página
st.write("""
Parabéns! Você conseguiu executar seu primeiro dashboard com Streamlit!

Se você está vendo isto, significa que tudo está funcionando. 🎉

Vamos entender o básico:
""")


# PASSO 4: Criar dados fictícios simples
# ═══════════════════════════════════════════════════════════════════════
# Vamos criar alguns dados para demonstrar
# Imagine que você vendeu produtos durante a semana

dados_vendas_da_semana = {
    'Dia da Semana': ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'],
    'Vendas em Reais': [150, 200, 180, 220, 250, 300, 280]
}

# Transformar em um DataFrame (que é como uma tabela no Pandas)
df_vendas = pd.DataFrame(dados_vendas_da_semana)

st.subheader("📋 Os Dados Brutos")
st.write("""
Aqui estão os dados que vamos visualizar.
Perceba que são apenas números em forma de tabela:
""")
st.dataframe(df_vendas)


# PASSO 5: Mostrar algumas estatísticas simples
# ═══════════════════════════════════════════════════════════════════════
st.subheader("📈 Estatísticas Rápidas")

# Calcular totais
vendas_total = df_vendas['Vendas em Reais'].sum()
vendas_media = df_vendas['Vendas em Reais'].mean()
vendas_maxima = df_vendas['Vendas em Reais'].max()
vendas_minima = df_vendas['Vendas em Reais'].min()

# st.metric() cria aqueles "cards" bonitos que você vê em dashboards
# É ótimo para mostrar números importantes
col_venda_total, col_venda_media, col_venda_maxima, col_venda_minima = st.columns(4)

with col_venda_total:
    st.metric(
        label="💰 Vendas Total",
        value=f"R$ {vendas_total:.2f}"
    )

with col_venda_media:
    st.metric(
        label="📊 Média de Vendas",
        value=f"R$ {vendas_media:.2f}"
    )

with col_venda_maxima:
    st.metric(
        label="⬆️ Venda Máxima",
        value=f"R$ {vendas_maxima:.2f}"
    )

with col_venda_minima:
    st.metric(
        label="⬇️ Venda Mínima",
        value=f"R$ {vendas_minima:.2f}"
    )


# PASSO 6: Criar o primeiro gráfico
# ═══════════════════════════════════════════════════════════════════════
st.subheader("📈 Gráfico de Linha: Evolução das Vendas")

st.write("""
Este é um gráfico de linha que mostra como as vendas mudaram ao longo da semana.
Quanto mais alto a linha, maior foi a venda naquele dia.
""")

# Criar o gráfico usando matplotlib
figura_grafico_linha, eixo = plt.subplots(figsize=(12, 5))

# Desenhar a linha
eixo.plot(
    df_vendas['Dia da Semana'],
    df_vendas['Vendas em Reais'],
    marker='o',      # Adiciona bolinhas nos pontos
    linewidth=2,     # Espessura da linha
    markersize=8,    # Tamanho das bolinhas
    color='#1f77b4'  # Cor azul
)

# Adicionar rótulos
eixo.set_xlabel('Dias da Semana', fontsize=12)
eixo.set_ylabel('Vendas (R$)', fontsize=12)
eixo.set_title('Vendas por Dia da Semana', fontsize=14, fontweight='bold')
eixo.grid(True, alpha=0.3)  # Adiciona uma grade para facilitar leitura

# Mostrar o gráfico na página
st.pyplot(figura_grafico_linha)


# PASSO 7: Criar um gráfico de barras
# ═══════════════════════════════════════════════════════════════════════
st.subheader("📊 Gráfico de Barras: Vendas por Dia")

st.write("""
Este é um gráfico de barras. Ele mostra os mesmos dados, mas em formato de barras.
Ótimo para comparar valores entre diferentes categorias.
""")

figura_grafico_barras, eixo_barras = plt.subplots(figsize=(12, 5))

# Desenhar as barras
cores_barras = ['#ff7f0e' if venda < 250 else '#2ca02c' for venda in df_vendas['Vendas em Reais']]
eixo_barras.bar(
    df_vendas['Dia da Semana'],
    df_vendas['Vendas em Reais'],
    color=cores_barras  # Cores diferentes: laranja se <250, verde se >=250
)

# Adicionar rótulos
eixo_barras.set_xlabel('Dias da Semana', fontsize=12)
eixo_barras.set_ylabel('Vendas (R$)', fontsize=12)
eixo_barras.set_title('Comparação de Vendas por Dia', fontsize=14, fontweight='bold')
eixo_barras.grid(True, alpha=0.3, axis='y')  # Grade apenas no eixo Y

# Adicionar valores no topo das barras
for i, venda in enumerate(df_vendas['Vendas em Reais']):
    eixo_barras.text(i, venda + 5, f'R$ {venda}', ha='center', fontsize=10)

st.pyplot(figura_grafico_barras)


# PASSO 8: Resumo e próximos passos
# ═══════════════════════════════════════════════════════════════════════
st.divider()  # Adiciona uma linha divisória
st.subheader("✨ O Que Você Aprendeu")

st.write("""
Parabéns! Você criou seu primeiro dashboard com:

✅ Títulos e subtítulos
✅ Tabelas de dados
✅ Estatísticas em cards bonitos (metrics)
✅ Gráficos de linha
✅ Gráficos de barras com cores customizadas

### 🚀 Próximos Passos:

1. **Experimente**: Mude os dados, adicione mais dias, mude as cores
2. **Teste**: Rode `streamlit run 01_primeiro_dashboard.py` de novo e veja as mudanças
3. **Customize**: Mude o título, adicione seus dados
4. **Avance**: Quando estiver pronto, abra `02_dashboard_com_planilha.py`

### 💡 Dicas:

- Toda vez que salvar o arquivo (Ctrl+S), a página atualiza automaticamente
- Se der erro, leia a mensagem de erro com calma no terminal
- Google é seu amigo! Procure por "streamlit" + sua dúvida

---

**Quando estiver pronto, execute:**
```bash
streamlit run 02_dashboard_com_planilha.py
```
""")

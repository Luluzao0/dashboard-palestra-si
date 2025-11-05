# Dashboard de Avaliação - Palestra Desenvolvimento de SI

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Avaliação Palestra SI", page_icon="📊", layout="wide")

sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'

# Carregar dados normalizados
@st.cache_data
def carregar_dados():
    # Usar arquivo na pasta data
    df = pd.read_excel('data/palestra_desenvolvimento.xlsx')
    
    df['data_hora'] = pd.to_datetime(df['data_hora'])
    
    # Extrair idade numérica
    df['idade_num'] = df['idade'].str.extract(r'(\d+)').astype(int)
    
    return df

df = carregar_dados()

# Sidebar - Filtros
st.sidebar.title("Filtros")
faixas_etarias = df['idade'].unique().tolist()
faixas_selecionadas = st.sidebar.multiselect("Faixa Etária", options=faixas_etarias, default=faixas_etarias)

pesquisa_opcoes = df['participou_pesquisa'].unique().tolist()
pesquisa_selecionada = st.sidebar.multiselect("Participou de Pesquisa?", options=pesquisa_opcoes, default=pesquisa_opcoes)

if st.sidebar.button("🔄 Resetar", use_container_width=True):
    st.rerun()

df_filtrado = df[
    (df['idade'].isin(faixas_selecionadas)) &
    (df['participou_pesquisa'].isin(pesquisa_selecionada))
]

st.sidebar.metric("Total de Respostas", len(df_filtrado))

# Aba de seleção
st.title("Avaliação - Palestra Desenvolvimento de SI")
st.write(f"Total de respostas: {len(df_filtrado)} | Data: {df['data_hora'].dt.date.min()} a {df['data_hora'].dt.date.max()}")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Análise Avançada", "💬 Respostas", "📋 Dados"])

# ═════════════════════════════════════════════════════════════════════════
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

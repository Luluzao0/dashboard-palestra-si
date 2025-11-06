import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="📊 Dashboard Palestra SI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = '#ffffff'

@st.cache_data
def load_data():
    try:
        df = pd.read_excel("data/palestra_desenvolvimento.xlsx")
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

df = load_data()
if df is None:
    st.stop()

notas = pd.to_numeric(df.iloc[:, -1], errors='coerce')

st.markdown("<h1 style='text-align:center;color:#1f77b4'>📊 Dashboard Palestra SI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#666;font-size:14px'>Análise Completa & Profissional | PowerBI Style</p>", unsafe_allow_html=True)
st.divider()

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    st.metric("📋 Total", len(df))
with col2:
    st.metric("⭐ Média", f"{notas.mean():.2f}/10")
with col3:
    st.metric("👍 Excelente (≥9)", f"{(notas >= 9).sum()}")
with col4:
    st.metric("📊 Bom (7-8)", f"{((notas >= 7) & (notas < 9)).sum()}")
with col5:
    st.metric("📉 Desvio Padrão", f"{notas.std():.2f}")
with col6:
    st.metric("🎯 Mediana", f"{notas.median():.2f}")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Visão Geral",
    "🎯 Análise Temática",
    "👥 Demografia",
    "🔬 Pesquisa",
    "💬 Respostas",
    "📊 Dados"
])

with tab1:
    st.subheader("Distribuição de Notas")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        notas_clean = notas.dropna()
        counts = notas_clean.value_counts().sort_index()
        colors = ['#e74c3c' if x < 5 else '#f39c12' if x < 7 else '#2ecc71' if x < 9 else '#27ae60' for x in counts.index]
        ax.bar(counts.index, counts.values, color=colors, edgecolor='black', alpha=0.8)
        ax.set_title('Histograma de Notas', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nota (0-10)', fontsize=11)
        ax.set_ylabel('Frequência', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        faixas = ['0-3\n(Péssimo)', '4-6\n(Ruim)', '7-8\n(Bom)', '9-10\n(Excelente)']
        valores = [
            len(notas[(notas >= 0) & (notas < 4)]),
            len(notas[(notas >= 4) & (notas < 7)]),
            len(notas[(notas >= 7) & (notas < 9)]),
            len(notas[(notas >= 9) & (notas <= 10)])
        ]
        cores = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
        ax.pie(valores, labels=faixas, autopct='%1.1f%%', colors=cores, startangle=90)
        ax.set_title('Distribuição por Faixa', fontsize=14, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
    
    with col3:
        st.write("### Estatísticas")
        st.write(f"**Média:** {notas.mean():.2f}")
        st.write(f"**Mediana:** {notas.median():.2f}")
        st.write(f"**Desvio:** {notas.std():.2f}")
        st.write(f"**Min:** {notas.min():.0f}")
        st.write(f"**Max:** {notas.max():.0f}")
        st.write(f"**Q1:** {notas.quantile(0.25):.2f}")
        st.write(f"**Q3:** {notas.quantile(0.75):.2f}")

with tab2:
    st.subheader("Análise Temática - Concordância")
    
    temas = [
        ('Conteúdo Claro', 'O conteúdo apresentado foi claro e de fácil compreensão'),
        ('Aplicabilidade', 'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).'),
        ('Gestão & Tecnologia', 'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.'),
        ('Interação', 'A interação entre os palestrantes e o público foi satisfatória.'),
        ('Integração', 'Após a palestra, você considera mais clara a importância da integração entre Administração e Engenharia da Computação para o desenvolvimento institucional?'),
        ('Potencial Aplicação', 'Você percebe potencial de aplicação dos sistemas apresentados em outras organizações públicas ou privadas?'),
        ('Interesse SIG', 'O evento despertou seu interesse em aprofundar conhecimentos sobre Sistemas de Informação Gerencial (SIG)?')
    ]
    
    dados_temas = []
    for nome, col_name in temas:
        if col_name in df.columns:
            col_data = df[col_name]
            if pd.api.types.is_numeric_dtype(col_data):
                sim = (col_data == 1).sum()
                nao = (col_data == 0).sum()
            else:
                sim = len(col_data[col_data.astype(str).str.contains('Sim', case=False, na=False)])
                nao = len(col_data[col_data.astype(str).str.contains('Não', case=False, na=False)])
            
            total = sim + nao
            pct = (sim / total * 100) if total > 0 else 0
            dados_temas.append({'Tema': nome, 'Sim': sim, 'Não': nao, 'Taxa': pct})
    
    df_temas = pd.DataFrame(dados_temas)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 7))
        colors = ['#2ecc71' if x >= 90 else '#f39c12' if x >= 75 else '#e74c3c' for x in df_temas['Taxa']]
        ax.barh(df_temas['Tema'], df_temas['Taxa'], color=colors, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Taxa de Concordância (%)', fontsize=12, fontweight='bold')
        ax.set_title('Concordância por Tema', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        for i, v in enumerate(df_temas['Taxa']):
            ax.text(v + 1, i, f'{v:.1f}%', va='center', fontweight='bold')
        
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.write("### Resumo")
        st.dataframe(df_temas[['Tema', 'Taxa']], use_container_width=True, hide_index=True)
        st.metric("Média Geral", f"{df_temas['Taxa'].mean():.1f}%")
        st.metric("Maior", f"{df_temas.loc[df_temas['Taxa'].idxmax(), 'Tema']}")
        st.metric("Menor", f"{df_temas.loc[df_temas['Taxa'].idxmin(), 'Tema']}")

with tab3:
    st.subheader("Análise por Idade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        idade_counts = df['Idade'].value_counts()
        colors_idade = sns.color_palette("husl", len(idade_counts))
        ax.bar(range(len(idade_counts)), idade_counts.values, color=colors_idade, edgecolor='black', alpha=0.8)
        ax.set_xticks(range(len(idade_counts)))
        ax.set_xticklabels(idade_counts.index, rotation=45, ha='right')
        ax.set_ylabel('Quantidade', fontsize=11, fontweight='bold')
        ax.set_title('Respondentes por Faixa Etária', fontsize=12, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 5))
        media_idade = df.groupby('Idade')[df.columns[-1]].apply(lambda x: pd.to_numeric(x, errors='coerce')).mean().sort_values(ascending=False)
        colors_media = sns.color_palette("RdYlGn", len(media_idade))
        ax.barh(media_idade.index, media_idade.values, color=colors_media, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Nota Média', fontsize=11, fontweight='bold')
        ax.set_title('Avaliação por Faixa Etária', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 10)
        
        for i, v in enumerate(media_idade.values):
            ax.text(v + 0.2, i, f'{v:.2f}', va='center', fontweight='bold')
        
        st.pyplot(fig, use_container_width=True)

with tab4:
    st.subheader("Experiência em Pesquisa")
    
    pesq_col = 'Já participou de algum projeto de pesquisa ou extensão?'
    
    if pesq_col in df.columns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            pesq_counts = df[pesq_col].value_counts()
            ax.pie(pesq_counts.values, labels=pesq_counts.index, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'], startangle=90)
            ax.set_title('Experiência em Pesquisa/Extensão', fontsize=12, fontweight='bold')
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            com_pesq = df[df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            sem_pesq = df[~df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            
            notas_com = pd.to_numeric(com_pesq.iloc[:, -1], errors='coerce')
            notas_sem = pd.to_numeric(sem_pesq.iloc[:, -1], errors='coerce')
            
            st.write("### Com Experiência")
            st.write(f"**n:** {len(com_pesq)}")
            st.write(f"**Média:** {notas_com.mean():.2f}")
            st.write(f"**Desvio:** {notas_com.std():.2f}")
            
            st.write("### Sem Experiência")
            st.write(f"**n:** {len(sem_pesq)}")
            st.write(f"**Média:** {notas_sem.mean():.2f}")
            st.write(f"**Desvio:** {notas_sem.std():.2f}")
        
        with col3:
            if len(notas_com.dropna()) > 1 and len(notas_sem.dropna()) > 1:
                t_stat, p_valor = stats.ttest_ind(notas_com.dropna(), notas_sem.dropna())
                st.write("### Teste T")
                st.write(f"**t-statístico:** {t_stat:.4f}")
                st.write(f"**p-valor:** {p_valor:.4f}")
                
                if p_valor < 0.05:
                    st.success("✅ Diferença significativa! (p < 0.05)")
                else:
                    st.info("⚠️ Sem diferença significativa (p ≥ 0.05)")
                
                d = (notas_com.mean() - notas_sem.mean()) / np.sqrt((notas_com.std()**2 + notas_sem.std()**2) / 2)
                st.write(f"**Cohen's d:** {d:.3f}")

with tab5:
    st.subheader("Respostas Abertas")
    
    subtabs = st.tabs(["Tecnologia & Gestão", "Cooperação", "Motivação"])
    
    with subtabs[0]:
        col = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'
        if col in df.columns:
            st.write("### Contribuições de Tecnologia")
            respostas = df[col].dropna()
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[1]:
        col = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação?'
        if col in df.columns:
            st.write("### Benefícios da Cooperação")
            respostas = df[col].dropna()
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[2]:
        col = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique.'
        if col in df.columns:
            st.write("### Motivação")
            respostas = df[col].dropna()
            motiv_sim = len([r for r in respostas if 'Sim' in str(r)])
            st.metric("Taxa de Motivação", f"{motiv_sim / len(respostas) * 100:.1f}%")
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")

with tab6:
    st.subheader("Dataset Completo")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.write(f"**Registros:** {len(df)} | **Colunas:** {len(df.columns)}")
        st.dataframe(df, use_container_width=True, height=500)
    
    with col2:
        st.write("### Exportar")
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 CSV", csv, "palestra.csv", "text/csv", use_container_width=True)
    
    st.markdown("---")
    st.write("### Dicionário")
    dict_df = pd.DataFrame({
        'Coluna': df.columns,
        'Tipo': [str(df[col].dtype) for col in df.columns],
        'Não Nulos': [df[col].notna().sum() for col in df.columns],
        'Nulos': [df[col].isna().sum() for col in df.columns]
    })
    st.dataframe(dict_df, use_container_width=True, hide_index=True)

st.divider()
st.markdown("<p style='text-align:center;color:#666;font-size:12px'>Dashboard Profissional PowerBI Style | Palestra SI 2025</p>", unsafe_allow_html=True)

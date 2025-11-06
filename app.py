import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Palestra SI - Análise Completa", page_icon="📊", layout="wide")
sns.set_style("whitegrid")

@st.cache_data
def load_data():
    df = pd.read_excel("data/palestra_desenvolvimento.xlsx")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    st.stop()

st.markdown("<h1 style='text-align:center;color:#1f77b4'>📊 Análise Completa - Palestra SI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#666'>Avaliação Integral | 14-15 de Outubro 2025</p>", unsafe_allow_html=True)
st.divider()

notas = pd.to_numeric(df.iloc[:, -1], errors='coerce')

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("📋 Total", len(df))
c2.metric("⭐ Nota Média", f"{notas.mean():.2f}/10")
c3.metric("👥 Taxa >8", f"{(notas >= 8).sum() / len(notas) * 100:.0f}%")
c4.metric("📅 Período", "14-15 Out")
c5.metric("✅ Completos", f"{notas.notna().sum()}")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visão Geral", "🎯 Análise Temática", "🔬 Pesquisa", "💬 Respostas", "📊 Dados"])

with tab1:
    st.subheader("Avaliação Geral - Distribuição de Notas")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        notas_clean = notas.dropna()
        notas_clean.value_counts().sort_index().plot(kind='bar', ax=ax, color='#667eea', edgecolor='black', alpha=0.7)
        ax.set_title('Histograma de Notas', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nota (0-10)')
        ax.set_ylabel('Frequência')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.write("### Estatísticas Descritivas")
        st.write(f"**Média:** {notas.mean():.2f}")
        st.write(f"**Mediana:** {notas.median():.2f}")
        st.write(f"**Desvio Padrão:** {notas.std():.2f}")
        st.write(f"**Mínima:** {notas.min():.2f}")
        st.write(f"**Máxima:** {notas.max():.2f}")
        st.write(f"**Q1 (25%):** {notas.quantile(0.25):.2f}")
        st.write(f"**Q3 (75%):** {notas.quantile(0.75):.2f}")
    
    st.markdown("---")
    st.subheader("Análise por Faixa Etária")
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 5))
        df.groupby('Idade').size().plot(kind='bar', ax=ax, color='#764ba2', edgecolor='black', alpha=0.7)
        ax.set_title('Distribuição por Faixa Etária', fontsize=14, fontweight='bold')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Quantidade')
        plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)
    
    with col2:
        media_por_idade = df.groupby('Idade')[df.columns[-1]].apply(lambda x: pd.to_numeric(x, errors='coerce')).agg(['mean', 'count', 'std'])
        media_por_idade.columns = ['Nota Média', 'Respostas', 'Desvio Padrão']
        st.write("### Notas por Faixa Etária")
        st.dataframe(media_por_idade, use_container_width=True)

with tab2:
    st.subheader("Análise Temática - Taxa de Concordância")
    
    temas = [
        ('Conteúdo Claro', 'O conteúdo apresentado foi claro e de fácil compreensão  '),
        ('Aplicabilidade', 'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).  '),
        ('Gestão & Tecnologia', 'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.  '),
        ('Interação', 'A interação entre os palestrantes e o público foi satisfatória.  '),
        ('Integração', 'Após a palestra, você considera mais clara a importância da integração entre Administração e Engenharia da Computação para o desenvolvimento institucional?  '),
        ('Potencial Aplicação', 'Você percebe potencial de aplicação dos sistemas apresentados em outras organizações públicas ou privadas?    '),
        ('Interesse SIG', 'O evento despertou seu interesse em aprofundar conhecimentos sobre Sistemas de Informação Gerencial (SIG)?   ')
    ]
    
    dados_temas = []
    for nome, col_name in temas:
        if col_name in df.columns:
            sim_count = len(df[df[col_name].astype(str).str.contains('Sim', case=False, na=False)])
            nao_count = len(df[df[col_name].astype(str).str.contains('Não', case=False, na=False)])
            total = sim_count + nao_count
            pct = (sim_count / total * 100) if total > 0 else 0
            dados_temas.append({
                'Tema': nome,
                'Sim': sim_count,
                'Não': nao_count,
                'Taxa': pct
            })
    
    if dados_temas:
        df_temas = pd.DataFrame(dados_temas)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['#2ecc71' if x >= 80 else '#f39c12' if x >= 60 else '#e74c3c' for x in df_temas['Taxa']]
        ax.barh(df_temas['Tema'], df_temas['Taxa'], color=colors, edgecolor='black', alpha=0.8)
        ax.set_xlabel('Taxa de Concordância (%)', fontsize=12, fontweight='bold')
        ax.set_title('Concordância por Tema', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        for i, v in enumerate(df_temas['Taxa']):
            ax.text(v + 2, i, f'{v:.1f}%', va='center', fontweight='bold')
        
        st.pyplot(fig)
        st.write("### Resumo Temático")
        st.dataframe(df_temas, use_container_width=True)

with tab3:
    st.subheader("Análise: Experiência em Pesquisa")
    pesq_col = 'Já participou de algum projeto de pesquisa ou extensão?  '
    
    if pesq_col in df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            df[pesq_col].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=['#3498db', '#e74c3c'], startangle=90)
            ax.set_ylabel('')
            ax.set_title('Experiência em Pesquisa/Extensão', fontsize=12, fontweight='bold')
            st.pyplot(fig)
        
        with col2:
            st.write("### Análise por Experiência")
            com_pesq = df[df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            sem_pesq = df[~df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            
            notas_com = pd.to_numeric(com_pesq.iloc[:, -1], errors='coerce')
            notas_sem = pd.to_numeric(sem_pesq.iloc[:, -1], errors='coerce')
            
            st.write(f"**Com experiência:** {len(com_pesq)} pessoas")
            st.write(f"  - Nota média: {notas_com.mean():.2f}")
            st.write(f"**Sem experiência:** {len(sem_pesq)} pessoas")
            st.write(f"  - Nota média: {notas_sem.mean():.2f}")
            
            if len(notas_com.dropna()) > 1 and len(notas_sem.dropna()) > 1:
                t_stat, p_valor = stats.ttest_ind(notas_com.dropna(), notas_sem.dropna())
                st.write(f"**Teste T:** t={t_stat:.3f}, p={p_valor:.4f}")
                if p_valor < 0.05:
                    st.write("✅ Diferença estatisticamente significativa!")
                else:
                    st.write("⚠️ Sem diferença significativa")

with tab4:
    st.subheader("Respostas Abertas")
    subtabs = st.tabs(["Gestão & Tecnologia", "Cooperação", "Motivação"])
    
    with subtabs[0]:
        col = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'
        if col in df.columns:
            st.write("### Contribuições de Tecnologia para Gestão")
            respostas = df[col].dropna()
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[1]:
        col = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação? '
        if col in df.columns:
            st.write("### Benefícios da Cooperação")
            respostas = df[col].dropna()
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[2]:
        col = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique. '
        if col in df.columns:
            st.write("### Motivação para Participação")
            respostas = df[col].dropna()
            motiv_sim = len([r for r in respostas if 'Sim' in str(r)])
            st.write(f"**Taxa de motivação:** {motiv_sim / len(respostas) * 100:.1f}%")
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")

with tab5:
    st.subheader("Dataset Completo")
    st.write(f"**Total de registros:** {len(df)}")
    st.write(f"**Total de colunas:** {len(df.columns)}")
    st.dataframe(df, use_container_width=True, height=500)
    
    csv = df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button("📥 Baixar CSV", csv, "palestra_completa.csv", "text/csv")
    
    st.markdown("---")
    st.subheader("Dicionário de Dados")
    dict_data = {'Coluna': df.columns, 'Tipo': [str(df[col].dtype) for col in df.columns]}
    st.dataframe(pd.DataFrame(dict_data), use_container_width=True)

st.divider()
st.markdown("<p style='text-align:center;color:#666;font-size:0.85em;'>Dashboard Completo e Profissional | Análise Palestra SI 2025</p>", unsafe_allow_html=True)

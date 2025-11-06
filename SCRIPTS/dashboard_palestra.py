import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="📊 Dashboard Palestra SI - PowerBI", page_icon="📊", layout="wide", initial_sidebar_state="expanded")
sns.set_style("darkgrid")
plt.rcParams['figure.facecolor'] = 'white'

@st.cache_data
def load_data():
    df = pd.read_excel("data/palestra_desenvolvimento.xlsx")
    df.columns = [c.strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"❌ Erro ao carregar dados: {e}")
    st.stop()

notas = pd.to_numeric(df.iloc[:, -1], errors='coerce')

header_col1, header_col2, header_col3 = st.columns([2, 3, 1])
with header_col1:
    st.markdown("<h1 style='color:#1f77b4;margin:0'>📊 DASHBOARD PALESTRA SI</h1>", unsafe_allow_html=True)
with header_col2:
    st.markdown("<p style='color:#666;font-size:14px;margin-top:15px'>Análise Completa & Profissional | PowerBI Style</p>", unsafe_allow_html=True)
with header_col3:
    st.markdown(f"<div style='background:#667eea;color:white;padding:10px;border-radius:5px;text-align:center'><p style='margin:0;font-size:12px'>Atualizado</p><p style='margin:0;font-weight:bold'>{datetime.now().strftime('%d/%m')}</p></div>", unsafe_allow_html=True)

st.divider()

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>📋 TOTAL</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{len(df)}</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Respondentes</p>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #f093fb 0%, #f5576c 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>⭐ MÉDIA</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{notas.mean():.2f}</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Nota Geral /10</p>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    taxa_excelente = (notas >= 9).sum() / len(notas) * 100
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>⭐ EXCELENTE</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{taxa_excelente:.0f}%</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Nota ≥ 9</p>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    taxa_bom = ((notas >= 7) & (notas < 9)).sum() / len(notas) * 100
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>👍 BOM</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{taxa_bom:.0f}%</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Nota 7-8</p>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    std_val = notas.std()
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #fa709a 0%, #fee140 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>📊 DESVIO</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{std_val:.2f}</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Padrão</p>
    </div>
    """, unsafe_allow_html=True)

with kpi6:
    percentil_95 = notas.quantile(0.95)
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
    <p style='margin:0;font-size:12px;opacity:0.9'>📈 P95</p>
    <p style='margin:0;font-size:28px;font-weight:bold'>{percentil_95:.1f}</p>
    <p style='margin:0;font-size:11px;opacity:0.8'>Percentil</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 VISÃO GERAL",
    "🎯 ANÁLISE TEMÁTICA",
    "👥 DEMOGRAFIA",
    "🔬 PESQUISA",
    "💬 INSIGHTS",
    "📊 DADOS"
])

with tab1:
    st.subheader("📊 Distribuição de Avaliações")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(12, 6))
        notas_clean = notas.dropna()
        counts = notas_clean.value_counts().sort_index()
        bars = ax.bar(counts.index, counts.values, color=['#e74c3c' if x < 5 else '#f39c12' if x < 7 else '#2ecc71' if x < 9 else '#27ae60' for x in counts.index], edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_title('Histograma de Notas', fontsize=14, fontweight='bold')
        ax.set_xlabel('Nota (0-10)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Frequência', fontsize=11, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        fig, ax = plt.subplots(figsize=(10, 6))
        faixas = ['0-3 (Péssimo)', '4-6 (Ruim)', '7-8 (Bom)', '9-10 (Excelente)']
        valores = [
            len(notas[(notas >= 0) & (notas < 4)]),
            len(notas[(notas >= 4) & (notas < 7)]),
            len(notas[(notas >= 7) & (notas < 9)]),
            len(notas[(notas >= 9) & (notas <= 10)])
        ]
        cores = ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71']
        wedges, texts, autotexts = ax.pie(valores, labels=faixas, autopct='%1.1f%%', colors=cores, startangle=90, textprops={'fontsize': 10, 'weight': 'bold'})
        ax.set_title('Distribuição por Faixa', fontsize=14, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
    
    with col3:
        st.write("### 📈 Estatísticas Completas")
        stats_dict = {
            '📊 Média': f"{notas.mean():.2f}",
            '📌 Mediana': f"{notas.median():.2f}",
            '📍 Moda': f"{notas.mode().values[0]:.0f}" if len(notas.mode()) > 0 else "N/A",
            '📊 Desvio Padrão': f"{notas.std():.2f}",
            '⬇️ Mínima': f"{notas.min():.0f}",
            '⬆️ Máxima': f"{notas.max():.0f}",
            'Q1 (25%)': f"{notas.quantile(0.25):.2f}",
            'Q3 (75%)': f"{notas.quantile(0.75):.2f}",
            'IQR': f"{notas.quantile(0.75) - notas.quantile(0.25):.2f}",
            'CV (%)': f"{(notas.std() / notas.mean() * 100):.2f}"
        }
        for k, v in stats_dict.items():
            st.markdown(f"**{k}:** `{v}`")

with tab2:
    st.subheader("🎯 Análise por Tema de Concordância")
    
    temas_cols = [
        ('Conteúdo Claro', 'O conteúdo apresentado foi claro e de fácil compreensão'),
        ('Aplicabilidade', 'Os sistemas desenvolvidos pelos alunos de Engenharia da Computação demonstraram aplicabilidade prática às necessidades das instituições apresentadas (Aceite de navios, App IMESC, outros).'),
        ('Gestão & Tecnologia', 'A palestra contribuiu para compreender como a tecnologia pode apoiar a gestão e a tomada de decisão.'),
        ('Interação', 'A interação entre os palestrantes e o público foi satisfatória.'),
        ('Integração AD-EC', 'Após a palestra, você considera mais clara a importância da integração entre Administração e Engenharia da Computação para o desenvolvimento institucional?'),
        ('Potencial Aplicação', 'Você percebe potencial de aplicação dos sistemas apresentados em outras organizações públicas ou privadas?'),
        ('Interesse SIG', 'O evento despertou seu interesse em aprofundar conhecimentos sobre Sistemas de Informação Gerencial (SIG)?')
    ]
    
    dados_temas = []
    for nome, col_name in temas_cols:
        if col_name in df.columns:
            col_data = df[col_name]
            if col_data.dtype == 'int64':
                sim = (col_data == 1).sum()
                nao = (col_data == 0).sum()
                total = sim + nao
                pct = (sim / total * 100) if total > 0 else 0
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
        colors_tema = ['#2ecc71' if x >= 90 else '#f39c12' if x >= 75 else '#e74c3c' for x in df_temas['Taxa']]
        bars = ax.barh(df_temas['Tema'], df_temas['Taxa'], color=colors_tema, edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_xlabel('Taxa de Concordância (%)', fontsize=12, fontweight='bold')
        ax.set_title('Concordância por Tema - Escala 0-100%', fontsize=14, fontweight='bold')
        ax.set_xlim(0, 100)
        
        for i, (bar, v) in enumerate(zip(bars, df_temas['Taxa'])):
            ax.text(v + 1.5, i, f'{v:.1f}%', va='center', fontweight='bold', fontsize=10)
        
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.write("### 🎯 Resumo Temático")
        st.dataframe(df_temas[['Tema', 'Sim', 'Não', 'Taxa']], use_container_width=True, hide_index=True)
        
        st.write("### 📊 Indicadores")
        media_concordancia = df_temas['Taxa'].mean()
        st.metric("Média Geral de Concordância", f"{media_concordancia:.1f}%")
        st.metric("Tema Mais Forte", f"{df_temas.loc[df_temas['Taxa'].idxmax(), 'Tema']} ({df_temas['Taxa'].max():.1f}%)")
        st.metric("Tema com Menos Concordância", f"{df_temas.loc[df_temas['Taxa'].idxmin(), 'Tema']} ({df_temas['Taxa'].min():.1f}%)")

with tab3:
    st.subheader("👥 Análise Demográfica")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Distribuição por Idade")
        fig, ax = plt.subplots(figsize=(10, 5))
        idade_counts = df['Idade'].value_counts()
        colors_idade = sns.color_palette("husl", len(idade_counts))
        bars = ax.bar(range(len(idade_counts)), idade_counts.values, color=colors_idade, edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_xticks(range(len(idade_counts)))
        ax.set_xticklabels(idade_counts.index, rotation=45, ha='right')
        ax.set_ylabel('Quantidade', fontsize=11, fontweight='bold')
        ax.set_title('Respondentes por Faixa Etária', fontsize=12, fontweight='bold')
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        st.pyplot(fig, use_container_width=True)
    
    with col2:
        st.write("### Nota Média por Idade")
        media_idade = df.groupby('Idade')[df.columns[-1]].apply(lambda x: pd.to_numeric(x, errors='coerce')).agg(['mean', 'count', 'std'])
        media_idade.columns = ['Nota Média', 'Respostas', 'Desvio Padrão']
        media_idade = media_idade.sort_values('Nota Média', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(media_idade.index, media_idade['Nota Média'], color=sns.color_palette("RdYlGn", len(media_idade)), edgecolor='black', linewidth=1.5, alpha=0.8)
        ax.set_xlabel('Nota Média', fontsize=11, fontweight='bold')
        ax.set_title('Avaliação Média por Faixa Etária', fontsize=12, fontweight='bold')
        ax.set_xlim(0, 10)
        
        for i, v in enumerate(media_idade['Nota Média']):
            ax.text(v + 0.2, i, f'{v:.2f}', va='center', fontweight='bold')
        
        st.pyplot(fig, use_container_width=True)
    
    st.write("### 📊 Tabela Detalhada")
    st.dataframe(media_idade, use_container_width=True)

with tab4:
    st.subheader("🔬 Análise: Experiência em Pesquisa & Extensão")
    
    pesq_col = 'Já participou de algum projeto de pesquisa ou extensão?'
    
    if pesq_col in df.columns:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            pesq_counts = df[pesq_col].value_counts()
            colors_pesq = ['#2ecc71', '#e74c3c']
            wedges, texts, autotexts = ax.pie(pesq_counts.values, labels=pesq_counts.index, autopct='%1.1f%%', colors=colors_pesq[:len(pesq_counts)], startangle=90, textprops={'fontsize': 11, 'weight': 'bold'})
            ax.set_title('Experiência em Pesquisa/Extensão', fontsize=12, fontweight='bold')
            st.pyplot(fig, use_container_width=True)
        
        with col2:
            st.write("### 📈 Análise Comparativa")
            com_pesq = df[df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            sem_pesq = df[~df[pesq_col].astype(str).str.contains('Sim', case=False, na=False)]
            
            notas_com = pd.to_numeric(com_pesq.iloc[:, -1], errors='coerce')
            notas_sem = pd.to_numeric(sem_pesq.iloc[:, -1], errors='coerce')
            
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                st.metric("Com Experiência", f"n={len(com_pesq)}")
                st.metric("Nota Média", f"{notas_com.mean():.2f}")
                st.metric("Desvio Padrão", f"{notas_com.std():.2f}")
            
            with col_c2:
                st.metric("Sem Experiência", f"n={len(sem_pesq)}")
                st.metric("Nota Média", f"{notas_sem.mean():.2f}")
                st.metric("Desvio Padrão", f"{notas_sem.std():.2f}")
        
        with col3:
            if len(notas_com.dropna()) > 1 and len(notas_sem.dropna()) > 1:
                t_stat, p_valor = stats.ttest_ind(notas_com.dropna(), notas_sem.dropna())
                st.write("### 📊 Teste T de Student")
                st.write(f"**Estatística t:** {t_stat:.4f}")
                st.write(f"**p-valor:** {p_valor:.4f}")
                if p_valor < 0.05:
                    st.write("✅ **Diferença Significativa!** (p < 0.05)")
                    st.write(f"A diferença de {abs(notas_com.mean() - notas_sem.mean()):.2f} pontos é estatisticamente significativa.")
                else:
                    st.write("⚠️ **Sem Diferença Significativa** (p ≥ 0.05)")
                    st.write("As notas não diferem estatisticamente entre os grupos.")
                
                st.write("---")
                efeto = (notas_com.mean() - notas_sem.mean()) / np.sqrt((notas_com.std()**2 + notas_sem.std()**2) / 2)
                st.write(f"**Tamanho do Efeito (Cohen's d):** {efeto:.3f}")
        
        st.markdown("---")
        st.write("### 📊 Comparação Visual")
        
        fig, ax = plt.subplots(figsize=(12, 5))
        data_comp = [notas_com.dropna(), notas_sem.dropna()]
        bp = ax.boxplot(data_comp, labels=['Com Experiência', 'Sem Experiência'], patch_artist=True)
        
        for patch, color in zip(bp['boxes'], ['#2ecc71', '#e74c3c']):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_ylabel('Nota', fontsize=11, fontweight='bold')
        ax.set_title('Distribuição de Notas por Experiência em Pesquisa', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig, use_container_width=True)

with tab5:
    st.subheader("💬 Insights das Respostas Abertas")
    
    subtabs = st.tabs(["🤔 Tecnologia & Gestão", "🤝 Cooperação", "💡 Motivação"])
    
    with subtabs[0]:
        col = 'De que forma você acredita que soluções tecnológicas podem contribuir para uma gestão mais efetiva?'
        if col in df.columns:
            st.write("### Contribuições de Tecnologia para Gestão")
            respostas = df[col].dropna()
            st.write(f"**Total de respostas:** {len(respostas)}")
            st.markdown("---")
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[1]:
        col = 'Como os graduandos de Administração podem se beneficiar da cooperação com graduandos de Engenharia da Computação?'
        if col in df.columns:
            st.write("### Benefícios da Cooperação")
            respostas = df[col].dropna()
            st.write(f"**Total de respostas:** {len(respostas)}")
            st.markdown("---")
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")
    
    with subtabs[2]:
        col = 'Você se sentiria motivado(a) a participar de projetos de pesquisa ou extensão que envolvam o desenvolvimento de sistemas aplicados à Administração? Justifique.'
        if col in df.columns:
            st.write("### Motivação para Participação")
            respostas = df[col].dropna()
            motiv_sim = len([r for r in respostas if 'Sim' in str(r)])
            motiv_taxa = motiv_sim / len(respostas) * 100 if len(respostas) > 0 else 0
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Taxa de Motivação", f"{motiv_taxa:.1f}%")
            with col_m2:
                st.metric("Respostas Motivadas", f"{motiv_sim}/{len(respostas)}")
            
            st.markdown("---")
            for i, r in enumerate(respostas, 1):
                if str(r).strip():
                    st.write(f"**{i}.** {r}")

with tab6:
    st.subheader("📊 Dataset Completo & Exportação")
    
    col_d1, col_d2 = st.columns([3, 1])
    
    with col_d1:
        st.write(f"**Total de registros:** {len(df)} | **Total de colunas:** {len(df.columns)}")
        st.dataframe(df, use_container_width=True, height=500)
    
    with col_d2:
        st.write("### 📥 Exportar Dados")
        
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 CSV",
            data=csv,
            file_name="palestra_completa.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='openpyxl')
        df.to_excel(excel_buffer, sheet_name='Dados', index=False)
        excel_buffer.close()
        
        with open('temp.xlsx', 'rb') as f:
            excel_data = f.read()
        
        st.download_button(
            label="📊 Excel",
            data=excel_data,
            file_name="palestra_completa.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.markdown("---")
    st.subheader("📖 Dicionário de Dados")
    dict_data = {
        'Coluna': df.columns,
        'Tipo': [str(df[col].dtype) for col in df.columns],
        'Não Nulos': [df[col].notna().sum() for col in df.columns],
        'Nulos': [df[col].isna().sum() for col in df.columns]
    }
    st.dataframe(pd.DataFrame(dict_data), use_container_width=True, hide_index=True)

st.divider()
st.markdown("""
<div style='background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);color:white;padding:15px;border-radius:8px;text-align:center'>
<p style='margin:0;font-size:13px'>🎉 Dashboard Profissional PowerBI Style | Análise Palestra SI 2025</p>
<p style='margin:0;font-size:11px;opacity:0.9'>Desenvolvido com Streamlit | Última atualização: {}</p>
</div>
""".format(datetime.now().strftime('%d de %B de %Y às %H:%M')), unsafe_allow_html=True)

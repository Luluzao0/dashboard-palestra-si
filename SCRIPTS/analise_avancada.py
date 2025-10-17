import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Configurar estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Carregar dados
df = pd.read_excel('DADOS/Palestra_Dados_Normalizados.xlsx')

# Renomear colunas
df.columns = [
    'data_hora',
    'idade',
    'participou_pesquisa',
    'conteudo_claro',
    'sistemas_aplicaveis',
    'tecnologia_gestao',
    'interacao_palestrantes',
    'integracao_clara',
    'potencial_aplicacao',
    'interesse_sig',
    'tecnologia_contribui',
    'cooperacao_beneficios',
    'participar_projetos',
    'avaliacao_geral'
]

# Converter coluna de idade para numérica (extrair números)
df['idade_num'] = df['idade'].str.extract('(\d+)').astype(int)

# Colunas de avaliação
avaliacoes = [
    'conteudo_claro',
    'sistemas_aplicaveis',
    'tecnologia_gestao',
    'interacao_palestrantes',
    'avaliacao_geral'
]

print("\n" + "="*100)
print("ANÁLISE AVANÇADA - PALESTRA DESENVOLVIMENTO DE SI")
print("="*100)

# 1. ANÁLISE DESCRITIVA
print("\n" + "─"*100)
print("1. ANÁLISE DESCRITIVA DAS AVALIAÇÕES")
print("─"*100)

stats_avaliacoes = df[avaliacoes].describe().round(2)
print("\n", stats_avaliacoes)

print("\nMODO (Nota mais frequente):")
for col in avaliacoes:
    moda = df[col].mode()[0]
    freq = (df[col] == moda).sum()
    print(f"  • {col}: {moda} (frequência: {freq}x)")

# 2. CORRELAÇÃO ENTRE VARIÁVEIS
print("\n" + "─"*100)
print("2. MATRIZ DE CORRELAÇÃO (Pearson)")
print("─"*100)

correlacao = df[avaliacoes].corr().round(3)
print("\n", correlacao)

print("\nCORRELAÇÕES MAIS FORTES:")
correlacoes_lista = []
for i in range(len(correlacao.columns)):
    for j in range(i+1, len(correlacao.columns)):
        correlacoes_lista.append({
            'var1': correlacao.columns[i],
            'var2': correlacao.columns[j],
            'correlacao': correlacao.iloc[i, j]
        })

correlacoes_lista = sorted(correlacoes_lista, key=lambda x: abs(x['correlacao']), reverse=True)
for item in correlacoes_lista[:5]:
    print(f"  • {item['var1']} ↔ {item['var2']}: {item['correlacao']:.3f}")

# 3. ANÁLISE POR GRUPO (Pesquisa vs Sem Pesquisa)
print("\n" + "─"*100)
print("3. ANÁLISE COMPARATIVA: COM vs SEM EXPERIÊNCIA EM PESQUISA")
print("─"*100)

com_pesquisa = df[df['participou_pesquisa'].str.contains('Sim', case=False, na=False)][avaliacoes]
sem_pesquisa = df[df['participou_pesquisa'].str.contains('Não', case=False, na=False)][avaliacoes]

print(f"\nCom experiência em pesquisa ({len(com_pesquisa)} pessoas):")
print(com_pesquisa.mean().round(2))

print(f"\nSem experiência em pesquisa ({len(sem_pesquisa)} pessoas):")
print(sem_pesquisa.mean().round(2))

# Teste T
print("\nTeste T (diferença significativa?):")
for col in avaliacoes:
    if len(com_pesquisa) > 1 and len(sem_pesquisa) > 1:
        t_stat, p_valor = stats.ttest_ind(com_pesquisa[col], sem_pesquisa[col])
        sig = "✓ Significativo" if p_valor < 0.05 else "✗ Não significativo"
        print(f"  • {col}: t={t_stat:.2f}, p={p_valor:.4f} {sig}")

# 4. ANÁLISE DE INTERESSE EM SIG
print("\n" + "─"*100)
print("4. ANÁLISE: INTERESSE EM SISTEMAS DE INFORMAÇÃO GERENCIAL (SIG)")
print("─"*100)

interesse_contagem = df['interesse_sig'].str.strip().value_counts()
print("\nDistribuição:")
for resposta, count in interesse_contagem.items():
    pct = (count / len(df)) * 100
    print(f"  • {resposta}: {count} ({pct:.1f}%)")

# Correlação com avaliação geral
interesse_sim = df[df['interesse_sig'].str.contains('Sim', case=False, na=False)]['avaliacao_geral'].mean()
interesse_nao = df[df['interesse_sig'].str.contains('Não', case=False, na=False)]['avaliacao_geral'].mean()
print(f"\nAvaliação geral média:")
print(f"  • Interessados em SIG: {interesse_sim:.2f}")
print(f"  • Não interessados em SIG: {interesse_nao:.2f}")

# 5. ANÁLISE DE TEXTO (Respostas Abertas)
print("\n" + "─"*100)
print("5. ANÁLISE DE RESPOSTAS ABERTAS")
print("─"*100)

# Palavras-chave
palavras_chave = {
    'tecnologia': ['tecnologia', 'software', 'sistema', 'digital', 'dados'],
    'gestao': ['gestão', 'decisão', 'planejamento', 'controle', 'efetiva'],
    'colaboracao': ['cooperação', 'trabalho', 'colaboração', 'integração', 'juntos'],
    'inovacao': ['inovação', 'novo', 'moderno', 'avançado', 'criatividade']
}

print("\nFrequência de palavras-chave em respostas abertas:")
for tema, palavras in palavras_chave.items():
    count = 0
    for col in ['tecnologia_contribui', 'cooperacao_beneficios', 'motivacao_participar']:
        for palavra in palavras:
            count += df[col].str.lower().str.contains(palavra, na=False).sum()
    print(f"  • {tema.upper()}: {count} menções")

# 6. SATISFAÇÃO GERAL
print("\n" + "─"*100)
print("6. INDICADORES DE SATISFAÇÃO")
print("─"*100)

satisfacao_alta = (df['avaliacao_geral'] >= 8).sum()
satisfacao_media = ((df['avaliacao_geral'] >= 5) & (df['avaliacao_geral'] < 8)).sum()
satisfacao_baixa = (df['avaliacao_geral'] < 5).sum()

print(f"\nNota geral de satisfação:")
print(f"  • Alta (≥8): {satisfacao_alta} ({satisfacao_alta/len(df)*100:.1f}%)")
print(f"  • Média (5-7): {satisfacao_media} ({satisfacao_media/len(df)*100:.1f}%)")
print(f"  • Baixa (<5): {satisfacao_baixa} ({satisfacao_baixa/len(df)*100:.1f}%)")

print(f"\nNota média: {df['avaliacao_geral'].mean():.2f}/10")
print(f"Mediana: {df['avaliacao_geral'].median():.1f}/10")
print(f"Desvio padrão: {df['avaliacao_geral'].std():.2f}")

# 7. ANÁLISE POR FAIXA ETÁRIA
print("\n" + "─"*100)
print("7. ANÁLISE POR FAIXA ETÁRIA")
print("─"*100)

df['faixa_etaria'] = pd.cut(df['idade_num'], bins=[0, 20, 25, 30, 35, 50, 100],
                              labels=['Até 20', '21-25', '26-30', '31-35', '36+', '50+'])

print("\nAvaliação média por faixa etária:")
for faixa in df['faixa_etaria'].cat.categories:
    media_faixa = df[df['faixa_etaria'] == faixa]['avaliacao_geral'].mean()
    count_faixa = len(df[df['faixa_etaria'] == faixa])
    if count_faixa > 0:
        print(f"  • {faixa}: {media_faixa:.2f} (n={count_faixa})")

# 8. RESPOSTAS COM MÚLTIPLAS ANÁLISES
print("\n" + "─"*100)
print("8. ALGUMAS RESPOSTAS INTERESSANTES")
print("─"*100)

respostas_boas = df[df['avaliacao_geral'] >= 9]
print(f"\nRespostas com avaliação ≥9 ({len(respostas_boas)}):")
print("\nMais comum:")
print(f"  • Interesse em SIG: {respostas_boas['interesse_sig'].mode()[0]}")
print(f"  • Participou pesquisa: {respostas_boas['participou_pesquisa'].mode()[0]}")

# 9. GERAR GRÁFICOS
print("\n" + "─"*100)
print("9. GERANDO VISUALIZAÇÕES...")
print("─"*100)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Análise Avançada - Palestra Desenvolvimento de SI', fontsize=16, fontweight='bold')

# Gráfico 1: Distribuição de avaliações
ax = axes[0, 0]
df['avaliacao_geral'].hist(bins=11, ax=ax, color='skyblue', edgecolor='black')
ax.axvline(df['avaliacao_geral'].mean(), color='red', linestyle='--', linewidth=2, label=f'Média: {df["avaliacao_geral"].mean():.2f}')
ax.set_xlabel('Nota')
ax.set_ylabel('Frequência')
ax.set_title('Distribuição de Notas Gerais')
ax.legend()

# Gráfico 2: Box plot por variável
ax = axes[0, 1]
df[avaliacoes].boxplot(ax=ax)
ax.set_ylabel('Nota')
ax.set_title('Box Plot - Todas as Avaliações')
ax.tick_params(axis='x', rotation=45)

# Gráfico 3: Comparação pesquisa vs sem pesquisa
ax = axes[0, 2]
dados_comparacao = [com_pesquisa['avaliacao_geral'].values, sem_pesquisa['avaliacao_geral'].values]
bp = ax.boxplot(dados_comparacao, labels=['Com Pesquisa', 'Sem Pesquisa'])
ax.set_ylabel('Nota')
ax.set_title('Avaliação por Experiência em Pesquisa')

# Gráfico 4: Heatmap de correlação
ax = axes[1, 0]
sns.heatmap(correlacao, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax, cbar_kws={'label': 'Correlação'})
ax.set_title('Correlação entre Variáveis')

# Gráfico 5: Interesse em SIG
ax = axes[1, 1]
interesse_data = df['interesse_sig'].str.strip().value_counts()
cores = ['#2ecc71', '#e74c3c', '#95a5a6']
interesse_data.plot(kind='bar', ax=ax, color=cores[:len(interesse_data)])
ax.set_title('Interesse em SIG')
ax.set_ylabel('Quantidade')
ax.set_xlabel('')
ax.tick_params(axis='x', rotation=45)

# Gráfico 6: Scatter - Idade vs Avaliação
ax = axes[1, 2]
scatter = ax.scatter(df['idade_num'], df['avaliacao_geral'], alpha=0.6, s=100, c=df['avaliacao_geral'], cmap='RdYlGn')
z = np.polyfit(df['idade_num'], df['avaliacao_geral'], 1)
p = np.poly1d(z)
ax.plot(df['idade_num'], p(df['idade_num']), "r--", linewidth=2, label='Tendência')
ax.set_xlabel('Idade')
ax.set_ylabel('Avaliação Geral')
ax.set_title('Idade vs Avaliação (com tendência)')
ax.legend()
plt.colorbar(scatter, ax=ax)

plt.tight_layout()
plt.savefig('OUTPUTS/analise_avancada_graficos.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráficos salvos em: OUTPUTS/analise_avancada_graficos.png")

plt.show()

print("\n" + "="*100)
print("ANÁLISE CONCLUÍDA")
print("="*100 + "\n")

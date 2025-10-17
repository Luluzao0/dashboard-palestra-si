import pandas as pd
import numpy as np

# Carregar os dados
df = pd.read_excel('Palestra Desenvolvimento de SI (respostas).xlsx')

# Renomear colunas para nomes mais curtos
df.columns = [
    'data_hora',
    'idade',
    'participou_pesquisa',
    'conteudo_claro',
    'sistemas_aplicaveis',
    'tecnologia_apoiar_gestao',
    'interacao_satisfatoria',
    'integracao_clara',
    'potencial_aplicacao',
    'interesse_sig',
    'tecnologia_contribui',
    'cooperacao_beneficios',
    'motivacao_participar',
    'avaliacao_geral'
]

print("=" * 100)
print("DADOS COMPLETOS - PALESTRA DESENVOLVIMENTO DE SI")
print("=" * 100)
print()

for idx, row in df.iterrows():
    print(f"\n{'─' * 100}")
    print(f"RESPOSTA #{idx + 1}")
    print(f"{'─' * 100}")
    print(f"Data/Hora: {row['data_hora']}")
    print(f"Idade: {row['idade']}")
    print(f"Participou de pesquisa: {row['participou_pesquisa']}")
    print()
    print("AVALIAÇÕES (0-10):")
    print(f"  • Conteúdo claro: {row['conteudo_claro']}")
    print(f"  • Sistemas aplicáveis: {row['sistemas_aplicaveis']}")
    print(f"  • Tecnologia apoiar gestão: {row['tecnologia_apoiar_gestao']}")
    print(f"  • Interação satisfatória: {row['interacao_satisfatoria']}")
    print(f"  • Avaliação geral: {row['avaliacao_geral']}")
    print()
    print("RESPOSTAS SIM/NÃO:")
    print(f"  • Integração clara: {row['integracao_clara']}")
    print(f"  • Potencial de aplicação: {row['potencial_aplicacao']}")
    print(f"  • Interesse em SIG: {row['interesse_sig']}")
    print()
    print("RESPOSTAS ABERTAS:")
    print(f"  • Como tecnologia pode contribuir para gestão:")
    print(f"    {row['tecnologia_contribui']}")
    print()
    print(f"  • Benefícios da cooperação Adm × Engenharia:")
    print(f"    {row['cooperacao_beneficios']}")
    print()
    print(f"  • Motivação para participar de projetos:")
    print(f"    {row['motivacao_participar']}")

print(f"\n{'=' * 100}")
print(f"TOTAL: {len(df)} respostas")
print(f"{'=' * 100}")

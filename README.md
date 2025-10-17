# Dashboard Análise - Palestra SI

Dashboard interativo desenvolvido com Streamlit para análise de avaliações de palestra.

## Requisitos

- Python 3.10+
- pip

## Instalação

```bash
pip install -r requirements.txt
```

## Como Usar

```bash
python -m streamlit run SCRIPTS/dashboard_palestra.py
```

Acesse: http://localhost:8501

## Estrutura

```
├── DADOS/           # Arquivos de dados
├── SCRIPTS/         # Scripts Python
├── OUTPUTS/         # Saídas geradas
├── README.md
└── requirements.txt
```

## Dados

- Total de respostas: 27
- Nota média: 9.62/10
- Período: 14-15 de outubro de 2025

## Dashboard

O dashboard possui 4 abas:
1. **Visão Geral** - Métricas e gráficos principais
2. **Análise Avançada** - Correlações e testes estatísticos
3. **Respostas Abertas** - Análise de texto
4. **Dados** - Tabela completa e download CSV

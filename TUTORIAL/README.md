# 📊 Tutorial Completo: Criando Dashboards com Streamlit

Bem-vindo! Este tutorial foi criado para ajudar **qualquer pessoa** a criar dashboards profissionais, mesmo que você nunca tenha programado antes.

## 📚 Conteúdo do Tutorial

Este repositório possui 4 lições progressivas:

### 1️⃣ **Lição 1: O Primeiro Dashboard** (`01_primeiro_dashboard.py`)
   - Como instalar Streamlit
   - Criar seu primeiro gráfico
   - Entender o básico de como funciona

### 2️⃣ **Lição 2: Dashboard com Dados de Planilha** (`02_dashboard_com_planilha.py`)
   - Como ler um arquivo Excel ou CSV
   - Criar múltiplos gráficos
   - Organizar os dados de forma visual

### 3️⃣ **Lição 3: Dashboard Interativo** (`03_dashboard_interativo.py`)
   - Adicionar filtros e seletores
   - Criar dashboards dinâmicos
   - Permitir que o usuário escolha o que ver

### 4️⃣ **Lição 4: Dashboard Profissional Completo** (`04_dashboard_profissional.py`)
   - Combinar tudo que aprendeu
   - Dicas de design e layout
   - Como adaptar para diferentes planilhas

## 🚀 Como Começar

### Passo 1: Instalar Python
Se você não tem Python instalado:
1. Acesse: https://www.python.org/
2. Baixe a versão mais recente
3. Execute e **marque "Add Python to PATH"**

### Passo 2: Abrir o Terminal
- Windows: Aperte `Win + R`, digite `cmd` e aperte Enter
- Mac: Procure por "Terminal"
- Linux: Abra o Terminal normalmente

### Passo 3: Instalar Streamlit
Cole este comando no terminal:
```bash
pip install streamlit pandas openpyxl matplotlib seaborn
```

### Passo 4: Executar o Dashboard
Abra o terminal na pasta deste projeto e execute:
```bash
streamlit run 01_primeiro_dashboard.py
```

## 💡 Conceitos Importantes

### O que é um Dashboard?
Um dashboard é uma página web interativa que mostra dados de forma visual. Com Streamlit, você não precisa saber HTML, CSS ou JavaScript!

### Por que Streamlit?
- ✅ Fácil de aprender
- ✅ Sem necessidade de frontend/backend
- ✅ Funciona com Python puro
- ✅ Ótimo para apresentações e análises rápidas

### Como Funciona?
Streamlit lê seu código Python de cima para baixo:
1. Você escreve um script Python normal
2. Streamlit transforma isso em uma página web
3. Toda vez que você salva, a página atualiza automaticamente

## 📁 Estrutura de Arquivos

```
dashbord-adm/
├── README.md                          # Este arquivo
├── 01_primeiro_dashboard.py           # Lição 1: Básico
├── 02_dashboard_com_planilha.py       # Lição 2: Lendo dados
├── 03_dashboard_interativo.py         # Lição 3: Interatividade
├── 04_dashboard_profissional.py       # Lição 4: Completo
├── dados_exemplo.csv                  # Arquivo de dados para teste
└── dados_exemplo.xlsx                 # Mesmo dado em Excel
```

## 🎯 Pré-requisitos

- Um computador (Windows, Mac ou Linux)
- Python 3.7 ou superior
- Um editor de texto (recomendado: VS Code)
- Vontade de aprender!

## ⚠️ Dicas Importantes

1. **Sempre use a mesma pasta**: Todos os exemplos assumem que você está usando a pasta deste projeto
2. **Erros são normais**: Se der erro, leia a mensagem com calma
3. **Customize**: Adapte os códigos para seus dados
4. **Comunidade**: O Streamlit tem uma comunidade grande - procure no Google!

## 📞 Dúvidas Comuns

**P: Posso usar minha própria planilha?**
R: Sim! Veja a Lição 2 para aprender como.

**P: Como mudo as cores dos gráficos?**
R: Está explicado em cada lição. Procure por `color=` nos códigos.

**P: O Dashboard fica online?**
R: Não automaticamente, mas você pode fazer isso com Streamlit Cloud (grátis).

**P: Preciso saber inglês?**
R: Não, mas será útil para Google e Stack Overflow quando tiver dúvidas específicas.

---

**Pronto? Vamos começar! Abra o arquivo `01_primeiro_dashboard.py` 👇**

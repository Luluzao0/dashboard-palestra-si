# Upload para GitHub

Este repositório está pronto para ser enviado ao GitHub.

## Pré-requisitos

1. Ter uma conta no GitHub (https://github.com)
2. Ter o Git instalado
3. Ter SSH ou token de acesso configurado

## Passo 1: Criar um novo repositório no GitHub

1. Acesse https://github.com/new
2. Defina o nome do repositório (ex: `dashboard-palestra-si`)
3. Descrição: "Dashboard Streamlit para análise de avaliações de palestra"
4. Selecione "Public" ou "Private"
5. NÃO inicialize com README (já temos um)
6. Clique em "Create repository"

## Passo 2: Adicionar remote ao repositório local

Copie o comando SSH/HTTPS fornecido pelo GitHub e execute:

```bash
# Se usar HTTPS:
git remote add origin https://github.com/seu-usuario/dashboard-palestra-si.git

# Se usar SSH:
git remote add origin git@github.com:seu-usuario/dashboard-palestra-si.git
```

## Passo 3: Fazer push

```bash
git branch -M main
git push -u origin main
```

## Passo 4: Verificar

Acesse seu repositório no GitHub:
https://github.com/seu-usuario/dashboard-palestra-si

---

## Verificar status atual

Para verificar se tudo está pronto:

```bash
git status
git log
git remote -v
```

---

**Substitua `seu-usuario` com seu nome de usuário do GitHub.**

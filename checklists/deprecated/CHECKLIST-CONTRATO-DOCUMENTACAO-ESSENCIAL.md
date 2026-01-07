# Checklist - Contrato de Documentacao Essencial

**Contrato:** DOCUMENTACAO-ESSENCIAL
**Versao:** 1.0
**Arquivo YAML:** CHECKLIST-CONTRATO-DOCUMENTACAO-ESSENCIAL.yaml

---

## Arquivos de Saida (5 arquivos)

| Ordem | Arquivo | Baseado em | Proposito |
|-------|---------|------------|-----------|
| 1 | RFXXX.md | RF.md + Legado | Requisito Funcional |
| 2 | UC-RFXXX.md | UC.md + RF | Casos de Uso |
| 3 | MD-RFXXX.md | MD.md + RF | Modelo de Dados |
| 4 | WF-RFXXX.md | WF.md + UC | Wireframes |
| 5 | user-stories.yaml | TEMPLATE-USER-STORIES.yaml + RF | User Stories para Azure DevOps |

---

## Pre-requisitos (BLOQUEANTES)

Antes de iniciar, TODOS devem ser True:

- [ ] **Pasta do RF existe** - em documentacao/[Fase]/[EPIC]/
- [ ] **Legado acessivel** - D:/IC2/ic1_legado/
- [ ] **Modelo fisico acessivel** - D:\DocumentosIC2\modelo-fisico-bd.sql
- [ ] **Templates disponiveis** - templates/TEMPLATE-*.md

**PARAR se qualquer item for False.**

---

## Todo List

- [ ] **Todo list criada** - Antes de qualquer acao
- [ ] **Status atualizado** - Em tempo real durante execucao

---

## Workflow

### Preparacao Git

- [ ] Branch dev atualizado (`git checkout dev && git pull`)
- [ ] Branch criado (`git checkout -b docs/RFXXX-essential-docs`)

### Analise do Legado

- [ ] Webservices identificados em ic1_legado
- [ ] Telas ASPX analisadas
- [ ] Tabelas mapeadas no modelo fisico
- [ ] Stored Procedures listadas

### Extracao de Regras

- [ ] Codigo VB.NET dos webservices lido
- [ ] Validacoes SQL identificadas
- [ ] **10-15 regras documentadas em linguagem natural**
- [ ] **Nenhum codigo VB.NET ou SQL copiado** (BLOQUEANTE)

---

## Geracao dos 4 Arquivos

### RFXXX.md (Ordem 1)

- [ ] **RFXXX.md** criado baseado em RF.md
  - [ ] Secao 1: Visao Geral (max 300 palavras)
  - [ ] Secao 2: Funcionalidades (min 10 regras)
  - [ ] Secao 3: Referencias ao Legado
  - [ ] Secao 4: Impacto e Dependencias
  - [ ] Secao 5: Integracao com Central

### UC-RFXXX.md (Ordem 2)

- [ ] **UC-RFXXX.md** criado baseado em UC.md
  - [ ] UC00: Listar
  - [ ] UC01: Criar
  - [ ] UC02: Visualizar
  - [ ] UC03: Editar
  - [ ] UC04: Excluir
  - [ ] Todos UCs tem Fluxos Alternativos (FA-XX)
  - [ ] Todos UCs tem Fluxos de Excecao (FE-XX)
  - [ ] Todos UCs tem Regras de Negocio (RN-UC-XXX)

### MD-RFXXX.md (Ordem 3)

- [ ] **MD-RFXXX.md** criado baseado em MD.md
  - [ ] Diagrama ER (Mermaid)
  - [ ] DDL completo (CREATE TABLE)
  - [ ] Campos de auditoria (Created, CreatedBy, LastModified, LastModifiedBy)
  - [ ] Multi-tenancy (ClienteId, EmpresaId ou FornecedorId)
  - [ ] Constraints (PK, FK, UNIQUE, CHECK)
  - [ ] Indices sugeridos
  - [ ] Dados iniciais (Seed)

### WF-RFXXX.md (Ordem 4)

- [ ] **WF-RFXXX.md** criado baseado em WF.md
  - [ ] Tela de Listagem (Desktop + Mobile)
  - [ ] Tela de Criar/Editar
  - [ ] Tela de Visualizar
  - [ ] Modais (Confirmacao, Sucesso, Erro)
  - [ ] Estados (Loading, Vazio, Erro)
  - [ ] Componentes Fuse/Material

### user-stories.yaml (Ordem 5)

- [ ] **user-stories.yaml** criado baseado em TEMPLATE-USER-STORIES.yaml
  - [ ] Minimo 2 User Stories identificadas
  - [ ] Cada story tem codigo unico (US-RFXXX-NNN)
  - [ ] Todas stories tem description (Como... Quero... Para...)
  - [ ] Todas stories tem acceptance criteria (minimo 5)
  - [ ] Todas stories tem technical notes (backend, frontend)
  - [ ] Todas stories tem story points (Fibonacci)
  - [ ] Dependencies mapeadas
  - [ ] Summary calculado (total stories, points)
  - [ ] Validation flags preenchidos

---

## Atualizacao STATUS.yaml

- [ ] documentacao.rf = True
- [ ] documentacao.uc = True
- [ ] documentacao.md = True
- [ ] documentacao.wf = True
- [ ] documentacao.user_stories = True

---

## Finalizacao

### Git

- [ ] Arquivos adicionados (`git add RFXXX.md UC-RFXXX.md MD-RFXXX.md WF-RFXXX.md user-stories.yaml STATUS.yaml`)
- [ ] Commit realizado (`git commit -m "docs(RFXXX): documentacao essencial (5 arquivos)"`)
- [ ] Checkout para dev (`git checkout dev`)
- [ ] Pull atualizado (`git pull origin dev`)
- [ ] Merge executado (`git merge docs/RFXXX-essential-docs`)
- [ ] Push realizado (`git push origin dev`)
- [ ] Branch removida (`git branch -d docs/RFXXX-essential-docs`)

### Sincronizacao (ver D:\IC2\sincronizar-devops.txt)

- [ ] sync-rf.py executado (`python tools/devops-sync/sync-rf.py RFXXX`)
- [ ] RF moveu para coluna "Documentacao Testes"

---

## Zonas Permitidas

### Leitura

```
D:/IC2/ic1_legado/**
D:\DocumentosIC2\modelo-fisico-bd.sql
D:\DocumentosIC2\inteligencia-artificial\prompts\arquitetura.md
templates/TEMPLATE-RF.md
templates/TEMPLATE-UC.md
templates/TEMPLATE-MD.md
templates/TEMPLATE-WF.md
rf/**/STATUS.yaml
```

### Escrita (5 arquivos + STATUS)

```
rf/**/RFXXX.md
rf/**/UC-RFXXX.md
rf/**/MD-RFXXX.md
rf/**/WF-RFXXX.md
rf/**/user-stories.yaml
rf/**/STATUS.yaml (apenas secao documentacao)
```

---

## Zonas Proibidas

```
backend/**
frontend/**
*.spec.ts
*.test.ts
*Tests.cs
azure-pipelines.yml
rf/**/TC-*.md (outro contrato)
```

---

## Proximo Contrato

Apos conclusao: **CONTRATO DE DOCUMENTACAO-GOVERNADA-TESTES**

```
Conforme CONTRATO DE DOCUMENTACAO-GOVERNADA-TESTES para RFXXX.
Seguir D:\IC2\CLAUDE.md.
```

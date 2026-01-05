# Checklist - Contrato de Documentacao Governada de Testes

**Contrato:** DOCUMENTACAO-GOVERNADA-TESTES
**Versao:** 2.0
**Arquivo YAML:** CHECKLIST-CONTRATO-DOCUMENTACAO-TESTES.yaml

---

## Arquivos de Saida (4 arquivos separados)

| Arquivo | Executor | Proposito |
|---------|----------|-----------|
| TC-RFXXX-BACKEND.md | Desenvolvimento (TI) | Testes de API |
| TC-RFXXX-FRONTEND.md | Desenvolvimento (TI) | Testes de UI |
| TC-RFXXX-SEGURANCA.md | Desenvolvimento (TI) | Testes OWASP |
| TC-RFXXX-E2E.md | QA / Usuario Final | Testes fim-a-fim |

---

## Pre-requisitos (BLOQUEANTES)

Antes de iniciar, TODOS devem ser True:

- [ ] **RF.md existe** - documentacao.rf == True
- [ ] **UC-RFXXX.md existe** - documentacao.uc == True
- [ ] **MD-RFXXX.md existe** - documentacao.md == True
- [ ] **WF-RFXXX.md existe** - documentacao.wf == True

**PARAR se qualquer item for False.**

---

## Todo List

- [ ] **Todo list criada** - Antes de qualquer acao
- [ ] **Status atualizado** - Em tempo real durante execucao

---

## Workflow

### Preparacao Git

- [ ] Branch dev atualizado (`git checkout dev && git pull`)
- [ ] Branch criado (`git checkout -b docs/RFXXX-test-cases`)

### Extracao do UC

- [ ] UC-RFXXX.md lido completamente
- [ ] Fluxo Principal identificado (steps 1-N)
- [ ] Fluxos Alternativos identificados (FA-01, FA-02...)
- [ ] Fluxos de Excecao identificados (FE-01, FE-02...)
- [ ] Regras de Negocio identificadas (RN-UC-XXX-NNN)

### Geracao dos 4 Arquivos TC

- [ ] **TC-RFXXX-BACKEND.md** criado
  - [ ] TC-API-XX: Happy Path
  - [ ] TC-API-XX: Alternative Paths (FA-XX)
  - [ ] TC-API-XX: Unhappy Paths (FE-XX)
  - [ ] Matriz de Rastreabilidade

- [ ] **TC-RFXXX-FRONTEND.md** criado
  - [ ] TC-FE-XX: Componentes UI
  - [ ] TC-FE-XX: Validacoes de formulario
  - [ ] TC-FE-XX: Feedback visual
  - [ ] Matriz de Rastreabilidade

- [ ] **TC-RFXXX-SEGURANCA.md** criado
  - [ ] TC-SEC-01: Isolamento de Tenant
  - [ ] TC-SEC-02: SQL Injection
  - [ ] TC-SEC-XX: Outros testes OWASP
  - [ ] Matriz de Rastreabilidade

- [ ] **TC-RFXXX-E2E.md** criado
  - [ ] TC-E2E-01: Fluxo completo (Happy Path)
  - [ ] TC-E2E-XX: Fluxos alternativos principais
  - [ ] Scripts Playwright (referencia)
  - [ ] Matriz de Rastreabilidade

---

## Cobertura (BLOQUEANTES)

- [ ] **Fluxo Principal mapeado** - TC-API + TC-FE + TC-E2E
- [ ] **Todos FA-XX tem TC** - Em BACKEND e FRONTEND
- [ ] **Todos FE-XX tem TC** - Em BACKEND e FRONTEND
- [ ] **Todas RN-UC-XXX referenciadas** - Em criterios de aprovacao
- [ ] **Isolamento de Tenant** - Em SEGURANCA
- [ ] **SQL Injection** - Em SEGURANCA
- [ ] **Matriz de Rastreabilidade** - Em cada arquivo

**PARAR se qualquer item nao for atendido.**

---

## Atualizacao STATUS.yaml

- [ ] documentacao_testes.backend = True (TC-RFXXX-BACKEND.md)
- [ ] documentacao_testes.frontend = True (TC-RFXXX-FRONTEND.md)
- [ ] documentacao_testes.e2e = True (TC-RFXXX-E2E.md)
- [ ] documentacao_testes.seguranca = True (TC-RFXXX-SEGURANCA.md)

---

## Finalizacao

### Git

- [ ] Arquivos adicionados (`git add TC-RFXXX-*.md STATUS.yaml`)
- [ ] Commit realizado (`git commit -m "docs(RFXXX): casos de teste (4 arquivos)"`)
- [ ] Checkout para dev (`git checkout dev`)
- [ ] Pull atualizado (`git pull origin dev`)
- [ ] Merge executado (`git merge docs/RFXXX-test-cases`)
- [ ] Push realizado (`git push origin dev`)
- [ ] Branch removida (`git branch -d docs/RFXXX-test-cases`)

### Sincronizacao (ver D:\IC2\sincronizar-devops.txt)

- [ ] sync-rf.py executado (`python tools/devops-sync/sync-rf.py RFXXX`)
- [ ] RF moveu para coluna "Testes TI"

---

## Zonas Permitidas

### Leitura

```
rf/**/RF*.md
rf/**/UC-RF*.md
rf/**/MD-RF*.md
rf/**/WF-RF*.md
rf/**/STATUS.yaml
templates/TEMPLATE-TC.md
```

### Escrita (4 arquivos)

```
rf/**/TC-RFXXX-BACKEND.md
rf/**/TC-RFXXX-FRONTEND.md
rf/**/TC-RFXXX-SEGURANCA.md
rf/**/TC-RFXXX-E2E.md
rf/**/STATUS.yaml (apenas documentacao_testes)
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
rf/**/RF*.md (somente leitura)
rf/**/UC-*.md (somente leitura)
rf/**/MD-*.md (somente leitura)
rf/**/WF-*.md (somente leitura)
```

---

## Modo Lote

Quando processando multiplos RFs:

- [ ] Branch unico: `docs/batch-test-cases-YYYYMMDD`
- [ ] Cada RF gera 4 arquivos
- [ ] Se RF falhar: perguntar ao usuario
- [ ] Commit unico com todos os RFs
- [ ] Sync individual para cada RF

---

## Mapeamento de Executores

| Arquivo | Executor |
|---------|----------|
| TC-RFXXX-BACKEND.md | Desenvolvimento (TI) |
| TC-RFXXX-FRONTEND.md | Desenvolvimento (TI) |
| TC-RFXXX-SEGURANCA.md | Desenvolvimento (TI) |
| TC-RFXXX-E2E.md | QA / Usuario Final |

---

## Proximo Contrato

Apos conclusao: **CONTRATO DE EXECUCAO DE TESTES**

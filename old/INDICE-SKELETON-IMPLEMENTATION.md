# ÍNDICE DA IMPLEMENTAÇÃO: SUPORTE A SKELETON

Este documento índice lista todos os artefatos criados para suportar
o novo estado **Skeleton** (Base de Entidade) no projeto IControlIT.

---

## RESUMO EXECUTIVO

Foi implementado um novo contrato formal chamado **CONTRATO-BASE-DE-ENTIDADE**
que permite criar estruturas CRUD básicas (backend + frontend) sem implementação
completa de regras de negócio.

**Objetivo:** Validar entidade e navegação antes de implementar regras completas.

**Próximo passo obrigatório após Skeleton:**
CONTRATO DE REGULARIZAÇÃO DE BACKEND

---

## ARTEFATOS CRIADOS

### 1. CONTRATO FORMAL

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| `CONTRATO-BASE-DE-ENTIDADE.md` | `D:\IC2\docs\contracts\` | Contrato formal de execução do Skeleton |

**Conteúdo:**
- Identificação do agente
- Ativação do contrato
- TODO LIST obrigatória
- Workflow de branches
- Escopo técnico permitido/proibido
- Validações mínimas
- Critério de pronto
- Transição obrigatória
- Regra de STATUS.yaml

---

### 2. GOVERNANÇA E CLAUDE.MD

| Arquivo | Localização | Alteração |
|---------|-------------|-----------|
| `CLAUDE.md` | `D:\IC2\` | Seção "Contrato de Base de Entidade (Skeleton)" adicionada |

**Alterações:**
- Linha ~287-376: Nova seção explicando o contrato
- Linha ~1009-1031: Atualizada "Regra Automatica de Decisao de Contrato"
- Linha ~1380-1397: Atualizada segunda ocorrência da regra de decisão

**Regra de decisão adicionada:**
```
1. Criar estrutura basica sem regras completas:
   → CONTRATO DE BASE DE ENTIDADE
```

---

### 3. TEMPLATES E DOCUMENTAÇÃO

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| `STATUS-TEMPLATE-SKELETON.yaml` | `D:\IC2\docs\templates\` | Template de STATUS.yaml para fase Skeleton |
| `FLUXO-TRANSICAO-SKELETON.md` | `D:\IC2\docs\workflows\` | Documentação completa do fluxo de transição |

**STATUS-TEMPLATE-SKELETON.yaml:**
- Novo campo: `skeleton.criado`
- Novo campo: `skeleton.data_criacao`
- Novo campo: `skeleton.observacao`
- Status de desenvolvimento: `skeleton` (não `done`)
- Board column: `"Skeleton"`
- Próximo contrato: `"CONTRATO-REGULARIZACAO-BACKEND"`

**FLUXO-TRANSICAO-SKELETON.md:**
- Visão geral do fluxo completo
- 5 estados detalhados (Skeleton, Regularização, Validação, Frontend, Testes)
- Tabela de transições permitidas/proibidas
- Regras de bloqueio
- Exemplos de STATUS.yaml em cada estado

---

### 4. DEVOPS SYNC

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| `PATCH-SKELETON-SUPPORT.md` | `D:\IC2\tools\devops-sync\` | Patch com alterações nos scripts |

**Alterações necessárias:**
- Adicionar coluna "Skeleton" ao dicionário COLUMNS
- Atualizar função `determine_column` para detectar estado Skeleton
- Atualizar comentários do cabeçalho

**Arquivos afetados:**
- `sync-board.py`
- `sync-rf.py`

**Lógica de detecção:**
```python
if skeleton_criado or backend_skeleton or frontend_skeleton:
    return "Skeleton", "Active"
```

---

### 5. GUIAS E DOCUMENTAÇÃO DE USO

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| `GUIA-CONFIGURACAO-SKELETON-DEVOPS.md` | `D:\IC2\docs\guias\` | Guia passo a passo completo |

**Conteúdo do guia:**
- Passo 1: Criar coluna "Skeleton" no Azure DevOps Board
- Passo 2: Aplicar patch nos scripts de sincronização
- Passo 3: Testar a configuração
- Passo 4: Documentar o novo fluxo
- Passo 5: Validação final
- Troubleshooting

---

## FLUXO COMPLETO DE TRANSIÇÃO

```
┌──────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DO RF                           │
└──────────────────────────────────────────────────────────────────┘

1. CONTRATO DE BASE DE ENTIDADE
   ↓
   STATUS.yaml: skeleton.criado = True
   STATUS.yaml: desenvolvimento.backend.status = "skeleton"
   Board: coluna "Skeleton"

2. CONTRATO DE REGULARIZAÇÃO DE BACKEND
   ↓
   STATUS.yaml: desenvolvimento.backend.status = "in_progress"
   Board: coluna "Backend"

3. CONTRATO DE TESTER-BACKEND
   ↓
   STATUS.yaml: desenvolvimento.backend.status = "done"
   Board: coluna "Frontend"

4. CONTRATO DE EXECUÇÃO – FRONTEND (completo)
   ↓
   STATUS.yaml: desenvolvimento.frontend.status = "done"
   Board: coluna "Documentacao Testes"

5. CONTRATO DE EXECUÇÃO DE TESTES (E2E)
   ↓
   STATUS.yaml: testes.e2e = "pass"
   Board: coluna "Testes QA"
```

---

## COLUNAS DO AZURE DEVOPS BOARD

| Ordem | Coluna | State | Descrição | Critério de Entrada |
|-------|--------|-------|-----------|---------------------|
| 0 | Backlog | New | Estado inicial | RF criado |
| 1 | Documentação | Active | Documentação em andamento | RF.md existe |
| **2** | **Skeleton** | **Active** | **CRUD básico criado** | **skeleton.criado = True** |
| 3 | Backend | Active | Backend em regularização | Todos docs + backend in_progress |
| 4 | Frontend | Active | Frontend em desenvolvimento | backend.status = done |
| 5 | Documentacao Testes | Active | Criar TC docs | frontend.status = done |
| 6 | Testes TI | Active | Executar testes TI | Todos TC docs existem |
| 7 | Testes QA | Testing | Testes QA em andamento | Todos testes TI passaram |
| 8 | Resolvido | Resolved | Resolvido (manual) | Aprovação QA |
| 9 | Finalizado | Closed | Finalizado (manual) | Deploy produção |

---

## TRANSIÇÕES PERMITIDAS E PROIBIDAS

### ✅ Transições Permitidas

```
Skeleton → Regularização → Validado → Frontend Completo → Aprovado → Produção
```

### ❌ Transições PROIBIDAS

- **Skeleton → Validado** (pular Regularização)
- **Skeleton → Frontend Completo** (pular Regularização + Validação)
- **Skeleton → Aprovado** (pular todas as fases)
- **Regularização → Frontend Completo** (pular Validação)
- **Skeleton → Produção** (NUNCA)

---

## QUANDO USAR CONTRATO-BASE-DE-ENTIDADE

Este contrato DEVE ser utilizado quando:

- ✅ Você quer validar entidade e navegação básica
- ✅ O cliente precisa "ver algo" inicial
- ✅ O domínio é grande e precisa ser estruturado antes
- ✅ As regras são muitas e serão incrementadas depois
- ✅ O time é pequeno e precisa dividir em fases

Este contrato NÃO deve ser usado quando:

- ❌ As regras de negócio já estão claras e completas
- ❌ O RF é pequeno e pode ser implementado de uma vez
- ❌ O backend já existe e precisa apenas de ajustes

---

## PRÓXIMOS PASSOS PARA O USUÁRIO

### Imediato (Obrigatório)

1. **Configurar Azure DevOps:**
   - Seguir `GUIA-CONFIGURACAO-SKELETON-DEVOPS.md`
   - Criar coluna "Skeleton" no board
   - Posicionar entre "Documentação" e "Backend"

2. **Aplicar patch nos scripts:**
   - Fazer backup de `sync-board.py` e `sync-rf.py`
   - Aplicar alterações conforme `PATCH-SKELETON-SUPPORT.md`
   - Testar com RF de exemplo

3. **Validar configuração:**
   - Executar teste local (`test-determine-column.py`)
   - Sincronizar RF de teste
   - Verificar que work item move para coluna "Skeleton"

### Médio Prazo

4. **Identificar RFs que deveriam ser Skeleton:**
   - Revisar RFs atuais em estado "Backend"
   - Verificar quais são apenas estruturas básicas
   - Atualizar STATUS.yaml desses RFs

5. **Documentar processos internos:**
   - Criar runbook para equipe
   - Incluir Skeleton no onboarding
   - Atualizar templates de projeto

### Longo Prazo

6. **Monitorar e ajustar:**
   - Acompanhar primeiros usos
   - Coletar feedback da equipe
   - Ajustar documentação conforme necessário

---

## REFERÊNCIAS CRUZADAS

### Contratos Relacionados

- `CONTRATO-BASE-DE-ENTIDADE.md` → Define Skeleton
- `CONTRATO-REGULARIZACAO-BACKEND.md` → Próximo passo após Skeleton
- `CONTRATO-TESTER-BACKEND.md` → Validação de backend regularizado
- `CONTRATO-EXECUCAO-FRONTEND.md` → Frontend completo

### Documentação Técnica

- `ARCHITECTURE.md` → Padrões arquiteturais
- `CONVENTIONS.md` → Convenções de código
- `CLAUDE.md` → Governança superior

### Scripts e Tools

- `sync-board.py` → Sincronização de board
- `sync-rf.py` → Sincronização de RF individual
- `validate-transitions.py` → Validação de transições (futuro)

---

## SUPORTE E TROUBLESHOOTING

### Problemas Comuns

1. **Coluna Skeleton não aparece no Board**
   - Solução: Verificar Board Settings
   - Referência: Seção "Troubleshooting" do guia

2. **Script não detecta estado Skeleton**
   - Solução: Verificar STATUS.yaml
   - Referência: `PATCH-SKELETON-SUPPORT.md`

3. **Work item não move para Skeleton**
   - Solução: Verificar campo WEF
   - Referência: `GUIA-CONFIGURACAO-SKELETON-DEVOPS.md`

### Documentação de Suporte

- `GUIA-CONFIGURACAO-SKELETON-DEVOPS.md` → Seção "Troubleshooting"
- `PATCH-SKELETON-SUPPORT.md` → Seção "Teste Recomendado"
- `FLUXO-TRANSICAO-SKELETON.md` → Seção "Regras de Transição"

---

## HISTÓRICO DE ALTERAÇÕES

| Data | Versão | Descrição |
|------|--------|-----------|
| 2025-12-27 | 1.0 | Implementação inicial do suporte a Skeleton |

---

## RESUMO PARA EXECUÇÃO RÁPIDA

**3 passos essenciais:**

1. **Azure DevOps:** Criar coluna "Skeleton" no board
2. **Scripts:** Aplicar patch em `sync-board.py` e `sync-rf.py`
3. **Teste:** Executar sincronização e validar

**Documentos obrigatórios:**
- `GUIA-CONFIGURACAO-SKELETON-DEVOPS.md` (passo a passo)
- `PATCH-SKELETON-SUPPORT.md` (código)

**Tempo estimado:** 30-60 minutos

---

**FIM DO ÍNDICE**

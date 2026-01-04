# PATCH: SUPORTE A ESTADO SKELETON

Este documento descreve as alterações necessárias nos scripts de sincronização DevOps
para suportar o novo estado **Skeleton** (Base de Entidade).

---

## ALTERAÇÕES NECESSÁRIAS

### 1. Adicionar Coluna "Skeleton" ao Mapeamento

**Arquivo:** `sync-board.py` e `sync-rf.py`

**Linha:** ~35-45 (seção COLUMNS)

**Alteração:**

```python
# ANTES:
COLUMNS = {
    "Backlog": {"state": "New", "order": 0},
    "Documentação": {"state": "Active", "order": 1},
    "Backend": {"state": "Active", "order": 2},
    "Frontend": {"state": "Active", "order": 3},
    "Documentacao Testes": {"state": "Active", "order": 4},
    "Testes TI": {"state": "Active", "order": 5},
    "Testes QA": {"state": "Testing", "order": 6},
    "Resolvido": {"state": "Resolved", "order": 7},
    "Finalizado": {"state": "Closed", "order": 8},
}

# DEPOIS:
COLUMNS = {
    "Backlog": {"state": "New", "order": 0},
    "Documentação": {"state": "Active", "order": 1},
    "Skeleton": {"state": "Active", "order": 2},           # NOVO
    "Backend": {"state": "Active", "order": 3},             # order: 2 → 3
    "Frontend": {"state": "Active", "order": 4},            # order: 3 → 4
    "Documentacao Testes": {"state": "Active", "order": 5}, # order: 4 → 5
    "Testes TI": {"state": "Active", "order": 6},           # order: 5 → 6
    "Testes QA": {"state": "Testing", "order": 7},          # order: 6 → 7
    "Resolvido": {"state": "Resolved", "order": 8},         # order: 7 → 8
    "Finalizado": {"state": "Closed", "order": 9},          # order: 8 → 9
}
```

---

### 2. Atualizar Função `determine_column`

**Arquivo:** `sync-board.py`

**Linha:** ~113-191

**Alteração:**

```python
def determine_column(status_data):
    """
    Determina a coluna do Board baseado no STATUS.yaml.
    Retorna (coluna, state).

    NOVO FLUXO COM SKELETON:
    - Skeleton criado -> Skeleton (estrutura básica)
    - Backend done (pós-regularização) -> Frontend
    - Frontend done -> Documentacao Testes (criar TC docs)
    - Todos TC docs existem -> Testes TI (executar testes)
    - Todos testes TI passaram -> Testes QA
    """
    docs = status_data.get('documentacao', {})
    dev = status_data.get('desenvolvimento', {})

    # NOVO: Campo skeleton
    skeleton = status_data.get('skeleton', {})
    skeleton_criado = skeleton.get('criado', False)

    # Novo schema: documentacao_testes (TC files)
    doc_testes = status_data.get('documentacao_testes', {})

    # Novo schema: testes_ti com backend/frontend/e2e/seguranca
    testes_ti = status_data.get('testes_ti', {})

    # Status de desenvolvimento
    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')
    backend_done = backend_status == 'done'
    frontend_done = frontend_status == 'done'

    # NOVO: Detectar estado skeleton
    backend_skeleton = backend_status == 'skeleton'
    frontend_skeleton = frontend_status == 'skeleton'

    # Documentacao completa (RF, UC, MD, WF)
    all_docs = (
        docs.get('rf', False) and
        docs.get('uc', False) and
        docs.get('md', False) and
        docs.get('wf', False)
    )

    # Documentacao de Testes - todos os 4 TC docs existem
    all_tc_docs = (
        doc_testes.get('backend', False) and
        doc_testes.get('frontend', False) and
        doc_testes.get('e2e', False) and
        doc_testes.get('seguranca', False)
    )

    # Testes TI - todos os 4 testes passaram
    all_ti_passed = (
        testes_ti.get('backend', 'not_run') == 'pass' and
        testes_ti.get('frontend', 'not_run') == 'pass' and
        testes_ti.get('e2e', 'not_run') == 'pass' and
        testes_ti.get('seguranca', 'not_run') == 'pass'
    )

    # ========================================
    # LOGICA DE DETERMINACAO (mais avancado primeiro)
    # ========================================

    # 7. Testes QA - todos testes TI passaram
    if all_ti_passed and frontend_done and backend_done:
        return "Testes QA", "Testing"

    # 6. Testes TI - todos TC docs existem (executar testes)
    if all_tc_docs and frontend_done and backend_done:
        return "Testes TI", "Active"

    # 5. Documentacao Testes - frontend done (criar TC docs)
    if frontend_done and backend_done:
        return "Documentacao Testes", "Active"

    # 4. Frontend - backend done (pós-regularização)
    if backend_done and not frontend_done:
        return "Frontend", "Active"

    # 3. Backend - backend em regularização (in_progress) OU todos docs prontos
    if all_docs and (backend_status == 'in_progress' or (not backend_done and not backend_skeleton)):
        return "Backend", "Active"

    # 2.5 NOVO: Skeleton - skeleton criado OU backend/frontend = "skeleton"
    if skeleton_criado or backend_skeleton or frontend_skeleton:
        return "Skeleton", "Active"

    # 2. Documentação - RF.md existe mas falta algum doc
    if docs.get('rf', False) and not all_docs:
        return "Documentação", "Active"

    # 1. Backlog - nada iniciado
    return "Backlog", "New"
```

---

### 3. Atualizar Comentários do Cabeçalho

**Arquivo:** `sync-board.py`

**Linha:** ~8-19

**Alteração:**

```python
# ANTES:
"""
COLUNAS E REGRAS:
- Backlog (New): Estado inicial
- Documentacao (Active): RF.md existe
- Backend (Active): Todos docs existem (RF, UC, MD, WF)
- Frontend (Active): Backend done
- Documentacao Testes (Active): Frontend done (criar TC docs)
- Testes TI (Active): Todos TC docs existem (executar testes)
- Testes QA (Testing): Todos testes TI passaram
- Resolvido (Resolved): MANUAL
- Finalizado (Closed): MANUAL

FLUXO:
Frontend done -> Documentacao Testes -> Testes TI -> Testes QA
"""

# DEPOIS:
"""
COLUNAS E REGRAS:
- Backlog (New): Estado inicial
- Documentacao (Active): RF.md existe
- Skeleton (Active): CRUD básico criado (backend.status = "skeleton")
- Backend (Active): Todos docs existem + backend em regularização/completo
- Frontend (Active): Backend done (pós-regularização)
- Documentacao Testes (Active): Frontend done (criar TC docs)
- Testes TI (Active): Todos TC docs existem (executar testes)
- Testes QA (Testing): Todos testes TI passaram
- Resolvido (Resolved): MANUAL
- Finalizado (Closed): MANUAL

NOVO FLUXO COM SKELETON:
Documentacao -> Skeleton -> Backend (Regularização) -> Frontend -> Documentacao Testes -> Testes TI -> Testes QA
"""
```

---

## RESUMO DAS ALTERAÇÕES

### Arquivos Afetados

1. `sync-board.py` (principal)
2. `sync-rf.py` (mesmas alterações em COLUMNS e determine_column)

### Linhas Alteradas

- Linha ~35-45: Adicionar coluna "Skeleton" ao dicionário COLUMNS
- Linha ~8-19: Atualizar comentários do cabeçalho
- Linha ~113-191: Adicionar lógica para detectar estado Skeleton na função determine_column

### Teste Recomendado

Após aplicar as alterações:

```bash
# Testar sincronização de um RF em estado Skeleton
python tools/devops-sync/sync-rf.py RF046

# Verificar que:
# 1. Script detecta skeleton.criado = True
# 2. Determina coluna "Skeleton"
# 3. Atualiza work item no DevOps
```

---

## PRÓXIMOS PASSOS

Após aplicar este patch:

1. **Criar coluna "Skeleton" no Azure DevOps Board**
   - Acessar Azure DevOps → Boards → Board Settings
   - Adicionar coluna "Skeleton" entre "Documentação" e "Backend"
   - Associar à state "Active"

2. **Testar sincronização**
   - Criar um STATUS.yaml de teste com skeleton.criado = True
   - Executar sync-rf.py
   - Verificar que work item move para coluna "Skeleton"

3. **Atualizar documentação**
   - Atualizar `D:\IC2\docs\devops\BOARD-WORKFLOW.md` (se existir)
   - Incluir coluna "Skeleton" no fluxo visual

---

**FIM DO PATCH**

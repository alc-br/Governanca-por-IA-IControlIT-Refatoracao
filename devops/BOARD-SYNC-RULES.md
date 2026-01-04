# Regras de Sincronizacao Board <-> STATUS.yaml

Este documento define as regras de movimentacao automatica de itens no Azure DevOps Board
baseadas no STATUS.yaml de cada RF.

---

## Colunas do Board e Regras

| Coluna | State | Regra de Entrada | Automatico? |
|--------|-------|------------------|-------------|
| **Backlog** | New | Estado inicial | - |
| **Documentacao** | Active | RF.md existe | SIM |
| **Backend** | Active | Todos docs existem (RF, UC, MD, WF) | SIM |
| **Frontend** | Active | Backend status = done | SIM |
| **Documentacao Testes** | Active | Frontend status = done (criar TC docs) | SIM |
| **Testes TI** | Active | Todos TC docs existem (executar testes) | SIM |
| **Testes QA** | Testing | Todos testes TI passaram | SIM |
| **Resolvido** | Resolved | QA aprovado pelo usuario | NAO |
| **Finalizado** | Closed | Usuario fecha manualmente | NAO |

## Fluxo Principal

```
Frontend done -> Documentacao Testes -> Testes TI -> Testes QA
                 (criar TC docs)       (executar)    (QA valida)
```

---

## Mapeamento STATUS.yaml -> Coluna

### 1. Backlog (State: New)
```yaml
documentacao:
  rf: False  # RF.md NAO existe
```

### 2. Documentacao (State: Active, Column: Documentacao)
```yaml
documentacao:
  rf: True   # RF.md existe
  uc: False  # Falta algum doc obrigatorio
```

### 3. Backend (State: Active, Column: Backend)
```yaml
documentacao:
  rf: True
  uc: True
  md: True
  wf: True   # Todos docs completos
desenvolvimento:
  backend:
    status: not_started | in_progress
```

### 4. Frontend (State: Active, Column: Frontend)
```yaml
desenvolvimento:
  backend:
    status: done
  frontend:
    status: not_started | in_progress
```

### 5. Documentacao Testes (State: Active, Column: Documentacao Testes)
```yaml
desenvolvimento:
  backend:
    status: done
  frontend:
    status: done
documentacao_testes:
  backend: False    # TC-RFXXX-BACKEND.md nao existe
  frontend: False   # TC-RFXXX-FRONTEND.md nao existe
  e2e: False        # TC-RFXXX-E2E.md nao existe
  seguranca: False  # TC-RFXXX-SEGURANCA.md nao existe
```

### 6. Testes TI (State: Active, Column: Testes TI)
```yaml
documentacao_testes:
  backend: True     # Todos TC docs existem
  frontend: True
  e2e: True
  seguranca: True
testes_ti:
  backend: not_run  # Testes ainda nao executados
  frontend: not_run
  e2e: not_run
  seguranca: not_run
```

### 7. Testes QA (State: Testing, Column: Testes QA)
```yaml
testes_ti:
  backend: pass     # Todos testes TI passaram
  frontend: pass
  e2e: pass
  seguranca: pass
testes_qa:
  executado: False  # QA ainda nao executou
  aprovado: False
```

### 8. Resolvido (State: Resolved) - MANUAL
```yaml
testes_qa:
  executado: True
  aprovado: True    # Usuario aprovou
```

### 9. Finalizado (State: Closed) - MANUAL
Controlado exclusivamente pelo usuario.

---

## Schema STATUS.yaml

```yaml
# Documentacao de Testes (TC files)
documentacao_testes:
  backend: False     # TC-RFXXX-BACKEND.md existe
  frontend: False    # TC-RFXXX-FRONTEND.md existe
  e2e: False         # TC-RFXXX-E2E.md existe
  seguranca: False   # TC-RFXXX-SEGURANCA.md existe

# Testes de TI (pos-desenvolvimento)
testes_ti:
  backend: not_run   # not_run | pass | fail
  frontend: not_run
  e2e: not_run
  seguranca: not_run

# Testes de QA
testes_qa:
  executado: False   # True quando QA executou
  aprovado: False    # True quando usuario aprovou
```

---

## Logica de Determinacao de Coluna

```python
def determine_column(status):
    docs = status.get('documentacao', {})
    dev = status.get('desenvolvimento', {})
    doc_testes = status.get('documentacao_testes', {})
    testes_ti = status.get('testes_ti', {})

    backend_done = dev.get('backend', {}).get('status') == 'done'
    frontend_done = dev.get('frontend', {}).get('status') == 'done'
    all_docs = docs.get('rf') and docs.get('uc') and docs.get('md') and docs.get('wf')

    # Todos os 4 TC docs existem
    all_tc_docs = (
        doc_testes.get('backend') and doc_testes.get('frontend') and
        doc_testes.get('e2e') and doc_testes.get('seguranca')
    )

    # Todos os 4 testes TI passaram
    all_ti_passed = (
        testes_ti.get('backend') == 'pass' and testes_ti.get('frontend') == 'pass' and
        testes_ti.get('e2e') == 'pass' and testes_ti.get('seguranca') == 'pass'
    )

    # Ordem de verificacao (do mais avancado para o menos)

    # 6. Testes QA - todos testes TI passaram
    if all_ti_passed and frontend_done and backend_done:
        return "Testes QA", "Testing"

    # 5. Testes TI - todos TC docs existem
    if all_tc_docs and frontend_done and backend_done:
        return "Testes TI", "Active"

    # 4. Documentacao Testes - frontend done (criar TC docs)
    if frontend_done and backend_done:
        return "Documentacao Testes", "Active"

    # 3. Frontend - backend done
    if backend_done and not frontend_done:
        return "Frontend", "Active"

    # 2. Backend - todos docs prontos
    if all_docs and not backend_done:
        return "Backend", "Active"

    # 1. Documentacao - RF.md existe
    if docs.get('rf') and not all_docs:
        return "Documentacao", "Active"

    # 0. Backlog
    return "Backlog", "New"
```

---

## Estados Protegidos

A automacao NUNCA altera itens que estao em:
- **Testing** (apos entrada em Testes QA)
- **Resolved** (usuario resolveu)
- **Closed** (usuario finalizou)

Isso garante que decisoes humanas nao sejam sobrescritas.

---

## Execucao

A sincronizacao pode ser executada:

1. **Pipeline CI/CD**: Apos merge de PR
2. **Manual**: `python tools/devops-sync/sync-board.py`
3. **Agendada**: Job diario para consistencia

---

## Auditoria

Cada sincronizacao gera log em:
- Description do work item (HTML)
- last_sync no STATUS.yaml
- Console output com resumo

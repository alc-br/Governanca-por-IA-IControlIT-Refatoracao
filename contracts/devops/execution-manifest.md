# DEVOPS EXECUTION MANIFEST

Este arquivo declara **explicitamente**
a execucao de atividades sob o
**CONTRATO DE DEVOPS / GOVERNANCA**.

Este arquivo e **OBRIGATORIO**.

---

## CONTRATO

CONTRATO: DEVOPS

---

## TIPO DE OPERACAO

- Consulta
- Inclusao
- Edicao
- Exclusao (excepcional)

Selecionado: Inclusao

---

## ALVO DA ACAO

Azure Boards:
- Criacao de Epics faltantes
- Criacao de User Stories para todos os RFs listados em D:\DocumentosIC2\RF-TRACKER.md
- Area Path por fase (Fase-1 a Fase-5)

---

## CONTEXTO

- Projeto Azure DevOps: iControlIT 2.0
- Organizacao: https://dev.azure.com/IControlIT-v2
- Ambiente afetado: DEV

---

## JUSTIFICATIVA

Registrar todo o backlog existente no Azure Boards para rastreabilidade,
planejamento e governanca operacional alinhada ao RF-TRACKER.

---

## PLANO DE ROLLBACK

- Registrar IDs criados na evidencia final.
- Para reversao: alterar o State para Removed/Closed e manter historico (sem exclusao).
- Aplicar tag de rastreio para localizar rapidamente os itens criados.

---

## DECLARACAO

Declaro que:
- A mudanca segue o CONTRATO DE DEVOPS
- O impacto foi analisado
- O rollback e possivel
- Nenhuma acao fora do escopo foi executada

---

## RESPONSAVEL

- Executor: Claude Code
- Aprovador humano: Anderson
- Data: 2025-12-22

---

## STATUS ATUAL

**CONCLUIDO**

Data execucao: 2025-12-22
Executor: Claude Code

---

## RESULTADO DA SINCRONIZACAO

### Fase 1: Criacao de Estrutura
| Metrica | Quantidade |
|---------|------------|
| Epics existentes | 25 |
| Epics criados | 0 |
| Features (RFs) existentes | 114 |
| Features criados | 0 |

### Fase 2: Atualizacao de Status (via STATUS.yaml)
| Metrica | Quantidade |
|---------|------------|
| RFs atualizados | 114 |
| STATUS.yaml atualizados | 114 |
| Erros | 0 |

### Distribuicao por State
| State | Quantidade | Descricao |
|-------|------------|-----------|
| Closed | 24 | Backend e Frontend concluidos |
| Active | 27 | Em desenvolvimento |
| New | 63 | Nao iniciados |

### IDs Criados (para rollback)

Faixa de IDs: 232 a 345

### Pendencias

| Item | Status |
|------|--------|
| RF-083 | Script atualizado para criar Area Path automaticamente |

---

## EVIDENCIAS

- Script utilizado: tools/devops-sync/sync-all-rfs.py
- Tag de rastreio: sync-YYYY-MM-DD (data dinamica)
- Tipo de Work Item: Feature (vinculado ao Epic pai)

---

## ATUALIZACOES DO SCRIPT (2025-12-22)

1. Adicionado mapeamento para Fase-99-Dev e EPIC027-DEV
2. Funcao ensure_area_path_exists() para criar Area Paths automaticamente
3. Tag de sincronizacao dinamica (usa data atual)
4. RF-083 agora sera sincronizado na proxima execucao

## ATUALIZACOES DO SCRIPT (2025-12-23)

### NOVO: Sistema State + WorkflowStage

**Principio:** O script APENAS atualiza campos. O Board se ajusta sozinho.
Automacao so pode ir ate State=Active + WorkflowStage=TEST_TI.
Estados Testing, Resolved, Closed sao EXCLUSIVOS do usuario.

Tags deixaram de existir para controle de fluxo.
Apenas tag de sync (sync-YYYY-MM-DD) para rastreabilidade.

### Campos Controlados

- `System.State` - Estado do work item
- `Custom.WorkflowStage` - Fase do workflow (DOC_NOK, DOC_OK, BACKEND, FRONTEND, TEST_TI)
- `System.Description` - Descricao HTML com status

### Mapeamento Oficial de Workflow

| WorkflowStage | System.State | Coluna do Board | Controlado por |
|---------------|--------------|-----------------|----------------|
| DOC_NOK | Active | Documentacao | Automacao |
| DOC_OK | Active | Documentacao | Automacao |
| BACKEND | Active | Backend | Automacao |
| FRONTEND | Active | Frontend | Automacao |
| TEST_TI | Active | Aguardando QA | Automacao |
| TEST_QA | Testing | Em Testes | **Usuario** |
| - | Resolved | Pronto | **Usuario** |
| - | Closed | Concluido | **Usuario** |

### Fluxo Visual

```
Automacao controla:
  New -> DOC_NOK -> DOC_OK -> BACKEND -> FRONTEND -> TEST_TI
         (Active)   (Active)  (Active)   (Active)    (Active)
                                                        |
Usuario controla:                                       v
                                           Testing -> Resolved -> Closed
```

### Logica de Determinacao de Workflow (sync-all-rfs.py)

```python
# Inferido do STATUS.yaml
if backend_done and frontend_done:
    stage = "TEST_TI"  # Aguardando QA
elif frontend_done or frontend_in_progress:
    stage = "FRONTEND"
elif backend_done or backend_in_progress:
    stage = "BACKEND"
elif docs_done:
    stage = "DOC_OK"
elif docs_started:
    stage = "DOC_NOK"
else:
    state = "New"  # Nao iniciado
```

### Logica de Determinacao de Workflow (sync-rf.py)

```python
# Inferido do CONTRATO no EXECUTION-MANIFEST
CONTRACT_TO_WORKFLOW = {
    "DOCUMENTACAO": "DOC_NOK",
    "BACKEND": "BACKEND",
    "FRONTEND": "FRONTEND",
    "TESTES": "TEST_TI",
    "DEBUG": "BACKEND",
    "MANUTENCAO": "BACKEND"
}
```

### Protecao de Estados do Usuario

O script NUNCA altera work items que ja estao em:
- Testing
- Resolved
- Closed

Estes estados sao controlados EXCLUSIVAMENTE pelo usuario no Board.

### Fallback para WorkflowStage

Se o campo `Custom.WorkflowStage` nao existir no Azure DevOps,
o script atualiza apenas `System.State` e emite um aviso.

### Beneficios do Novo Sistema

- Separacao clara: automacao vs usuario
- Board como fonte unica de verdade
- Colunas mapeiam para State + WorkflowStage
- Nao depende de tags para workflow
- Usuario tem controle total apos TEST_TI

---

## COMO EXECUTAR

```powershell
# Configurar variaveis de ambiente
$env:AZDO_ORG_URL = "https://dev.azure.com/IControlIT-v2"
$env:AZDO_PROJECT = "iControlIT 2.0"
$env:AZDO_PAT = "<seu_pat_aqui>"

# Executar sincronizacao
python D:\IC2\tools\devops-sync\sync-all-rfs.py
```

---

## PLANO DE ROLLBACK (se necessario)

Para reverter:
1. Filtrar por tag "sync-YYYY-MM-DD" (data da sincronizacao)
2. Alterar State para "Removed" (nao excluir)
3. Ou usar query: `SELECT * FROM WorkItems WHERE [System.Tags] CONTAINS 'sync-YYYY-MM-DD'`

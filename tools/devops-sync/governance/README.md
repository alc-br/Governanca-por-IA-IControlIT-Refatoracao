# Scripts de Governança - DevOps Sync

Scripts para **transições de estado** e **rollback** conforme contratos de governança.

## Scripts Disponíveis

| Script | Descrição | Quando Usar |
|--------|-----------|-------------|
| **apply_rollback.py** | Reverte transição de estado | Quando deploy falha e precisa voltar |
| **apply_tests_to_deploy_transition.py** | Aplica transição Testes → Deploy | Após testes 100% PASS |
| **apply-transition.py** | Aplica transição genérica de estado | Transições customizadas |

## Uso

### Rollback de Deploy

Quando deploy falha em HOM ou PRD:

```bash
python tools/devops-sync/governance/apply_rollback.py RFXXX
```

**Efeito:**
- Reverte STATUS.yaml para estado anterior
- Move Work Item de volta para coluna anterior no board
- Registra rollback no EXECUTION-MANIFEST.md

### Transição Testes → Deploy

Após testes 100% PASS:

```bash
python tools/devops-sync/governance/apply_tests_to_deploy_transition.py RFXXX
```

**Efeito:**
- Valida que `validacao.tester_backend_aprovado = True`
- Atualiza STATUS.yaml para `deploy.homologacao = True`
- Move Work Item para coluna "Em Homologação"
- Registra transição no EXECUTION-MANIFEST.md

### Transição Genérica

Para transições customizadas:

```bash
python tools/devops-sync/governance/apply-transition.py RFXXX FROM_STATE TO_STATE
```

**Exemplo:**
```bash
python tools/devops-sync/governance/apply-transition.py RF027 TESTES DEPLOY
```

## Regras de Governança

### Transições Permitidas

```
DOCUMENTACAO → BACKEND
BACKEND → TESTER-BACKEND
TESTER-BACKEND → FRONTEND (somente se aprovado)
FRONTEND → TESTES
TESTES → DEPLOY-HOM (somente se 100% PASS)
DEPLOY-HOM → DEPLOY-PRD (somente se HOM OK)
```

### Transições Bloqueadas

- **BACKEND → FRONTEND** sem aprovação Tester-Backend
- **TESTES → DEPLOY** sem 100% PASS
- **DEPLOY-HOM → DEPLOY-PRD** sem validação HOM

### Rollback Obrigatório

Se deploy falha:
➡️ Rollback automático via `apply_rollback.py`
➡️ Registro no EXECUTION-MANIFEST.md
➡️ Work Item volta para estado anterior

## Integração com Contratos

| Script | Contrato Relacionado |
|--------|---------------------|
| apply_rollback.py | CONTRATO-DEPLOY-AZURE |
| apply_tests_to_deploy_transition.py | CONTRATO-EXECUCAO-TESTES → CONTRATO-DEPLOY-AZURE |
| apply-transition.py | CONTRATO-ORQUESTRACAO |

## Pré-requisitos

- Variável de ambiente `AZURE_DEVOPS_PAT` configurada
- STATUS.yaml atualizado
- EXECUTION-MANIFEST.md atualizado

## Resultado Esperado

- ✅ Transição aplicada corretamente
- ✅ STATUS.yaml atualizado
- ✅ Work Item movido para coluna correta
- ✅ EXECUTION-MANIFEST.md registrado
- ❌ Bloqueio se transição não é permitida

## Atenção

⚠️ **Scripts de governança são bloqueadores** - não permitem transições inválidas.

⚠️ **Rollback é obrigatório** em caso de falha de deploy.

⚠️ **Transições sem aprovação Tester-Backend são NEGADAS** automaticamente.

# FLUXO VISUAL DE CONTRATOS – GOVERNANÇA ICONTROLIT

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Propósito:** Visualização completa do fluxo de contratos desde documentação até deploy/rollback

---

## VISÃO GERAL

Este documento apresenta o fluxo visual completo de execução de contratos no IControlIT, demonstrando:
- A sequência obrigatória de contratos
- Pontos de decisão (APROVADO/REPROVADO)
- Gatilhos explícitos de transição
- Atualização de STATUS.yaml
- Registro em EXECUTION-MANIFEST

---

## FLUXO PRINCIPAL: BACKEND → TESTER → TESTES → DEPLOY

```
┌──────────────────────────────┐
│ RF + MD + UC + WF PRONTOS    │
│                              │
│ - RF completo (5 seções)     │
│ - UC completo (UC00-UC04)    │
│ - MD completo (DDL)          │
│ - WF completo (telas)        │
└──────────────┬───────────────┘
               │
               │ PRÉ-REQUISITO VALIDADO
               ▼
┌──────────────────────────────┐
│ CONTRATO-EXECUCAO-BACKEND    │
│ (Implementa código backend)  │
│                              │
│ Executor: Developer Agent    │
│ Tipo: OPERACIONAL            │
│                              │
│ Entregas:                    │
│ - Código backend (.NET)      │
│ - Migrations                 │
│ - Seeds                      │
│ - Permissões                 │
│ - Testes unitários mínimos   │
└──────────────┬───────────────┘
               │
               │ gera
               ▼
┌──────────────────────────────┐
│ EXECUTION-MANIFEST           │
│ Tipo: OPERACIONAL            │
│                              │
│ - Contrato: EXECUCAO-BACKEND │
│ - RF: RFXXX                  │
│ - Executor: Developer Agent  │
│ - Data: YYYY-MM-DD HH:MM:SS  │
└──────────────┬───────────────┘
               │
               │ GATILHO AUTOMÁTICO
               ▼
┌──────────────────────────────┐
│ CONTRATO-TESTER-BACKEND      │
│ (Valida contrato backend)    │
│                              │
│ Executor: Tester-Backend     │
│ Tipo: DECISÓRIA              │
│                              │
│ Validações:                  │
│ - Backend rejeita violações? │
│ - Erros estruturados?        │
│ - Permissões corretas?       │
│ - Multi-tenancy validado?    │
└──────────────┬───────────────┘
               │
               │ se APROVADO
               ▼
┌──────────────────────────────────────────────┐
│ EXECUTION-MANIFEST                            │
│ Tipo: DECISÓRIA                               │
│                                               │
│ decision:                                     │
│   resultado: APROVADO                         │
│   autoridade: Tester-Backend                  │
│   contrato: CONTRATO-EXECUCAO-TESTER-BACKEND  │
│   data: YYYY-MM-DD HH:MM:SS                   │
│                                               │
│ Atualização STATUS.yaml:                      │
│   contrato_validado: true                     │
│   contrato: CONTRATO-EXECUCAO-BACKEND         │
│   versao_contrato: v1.0                       │
└──────────────┬───────────────────────────────┘
               │
               │ (GATILHO EXPLÍCITO)
               │ Transição autorizada
               ▼
┌──────────────────────────────────────────────┐
│ CONTRATO-TRANSICAO-BACKEND-PARA-TESTES        │
│ (NÃO executa testes)                          │
│                                               │
│ Executor: DevOps Agent                        │
│ Tipo: DECISÓRIA                               │
│                                               │
│ Função:                                       │
│ - Validar aprovação do Tester-Backend         │
│ - Atualizar STATUS.yaml                       │
│ - Registrar transição no manifesto            │
│ - Sincronizar Azure DevOps                    │
└──────────────┬───────────────────────────────┘
               │
               │ aplica
               ▼
┌──────────────────────────────┐
│ STATUS.yaml ATUALIZADO       │
│                              │
│ governanca:                  │
│   contrato_ativo: TESTES     │
│                              │
│ devops:                      │
│   board_column:              │
│     "Pronto para Testes"     │
└──────────────┬───────────────┘
               │
               │ PRÓXIMA FASE
               ▼
┌──────────────────────────────┐
│ CONTRATO-EXECUCAO-TESTES     │
│ (QA / E2E / Validações)      │
│                              │
│ Executor: QA Agent / Tester  │
│ Tipo: DECISÓRIA              │
│                              │
│ Testes executados:           │
│ - Backend (unitários)        │
│ - Frontend (componentes)     │
│ - E2E (Playwright)           │
│ - Segurança (SQL, XSS, CSRF) │
│                              │
│ Critério de aprovação:       │
│ Taxa = 100% (sem exceções)   │
└──────────────┬───────────────┘
               │
               │ se APROVADO (taxa = 100%)
               ▼
┌──────────────────────────────────────────────┐
│ EXECUTION-MANIFEST                            │
│ Tipo: DECISÓRIA                               │
│                                               │
│ decision:                                     │
│   resultado: APROVADO                         │
│   autoridade: QA / Tester                     │
│   contrato: CONTRATO-EXECUCAO-TESTES          │
│   taxa_aprovacao: 100%                        │
│   data: YYYY-MM-DD HH:MM:SS                   │
│                                               │
│ Evidências:                                   │
│   - Screenshots de E2E                        │
│   - Logs de execução                          │
│   - Relatório de cobertura                    │
└──────────────┬───────────────────────────────┘
               │
               │ (GATILHO EXPLÍCITO)
               │ Transição autorizada
               ▼
┌──────────────────────────────────────────────┐
│ CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY         │
│ (NÃO executa deploy)                          │
│                                               │
│ Executor: DevOps Agent                        │
│ Tipo: DECISÓRIA                               │
│                                               │
│ Função:                                       │
│ - Validar taxa de aprovação = 100%            │
│ - Atualizar STATUS.yaml                       │
│ - Registrar transição no manifesto            │
│ - Sincronizar Azure DevOps                    │
└──────────────┬───────────────────────────────┘
               │
               │ aplica
               ▼
┌──────────────────────────────┐
│ STATUS.yaml ATUALIZADO       │
│                              │
│ governanca:                  │
│   contrato_ativo: DEPLOY     │
│                              │
│ devops:                      │
│   board_column:              │
│     "Pronto para Deploy"     │
└──────────────┬───────────────┘
               │
               │ PRÓXIMA FASE
               │ (Aguarda aprovação formal)
               ▼
┌──────────────────────────────┐
│ CONTRATO-EXECUCAO-DEPLOY     │
│ (Build + Deploy governado)   │
│                              │
│ Executor: DevOps Agent       │
│ Tipo: DECISÓRIA              │
│ Ambiente: HOM ou PRD         │
│                              │
│ Ações:                       │
│ - Executar build             │
│ - Executar deploy            │
│ - Executar smoke tests       │
│ - Registrar versão           │
│                              │
│ Smoke tests:                 │
│ - Backend health: OK?        │
│ - Frontend acessível: OK?    │
│ - Autenticação: OK?          │
└──────────────┬───────────────┘
               │
               ├─────────────────┐
               │                 │
               │ se PASS         │ se FAIL
               ▼                 ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ SUCESSO                      │ │ CONTRATO-ROLLBACK            │
│                              │ │ (Rollback auditável)         │
│ EXECUTION-MANIFEST:          │ │                              │
│ decision:                    │ │ Executor: DevOps Agent       │
│   resultado: APROVADO        │ │ Tipo: DECISÓRIA (CRÍTICA)    │
│   smoke_tests: PASS          │ │ Gatilho: AUTOMÁTICO          │
│   versao: X.Y.Z              │ │                              │
│   ambiente: HOM/PRD          │ │ Ações:                       │
│                              │ │ - Identificar versão anterior│
│ STATUS.yaml:                 │ │ - Reverter código            │
│   deployed_version: X.Y.Z    │ │ - Smoke tests pós-rollback   │
│   last_deploy: timestamp     │ │ - Registrar motivo           │
│   board_column: "Produção"   │ │                              │
│                              │ │ EXECUTION-MANIFEST:          │
│ FIM DO FLUXO                 │ │ decision:                    │
└──────────────────────────────┘ │   resultado: APROVADO        │
                                 │   motivo: Smoke test failed  │
                                 │   versao_revertida: X.Y.Z-1  │
                                 │                              │
                                 │ Próximo passo:               │
                                 │ - CONTRATO-DEBUG-CONTROLADO  │
                                 │ - Investigar causa raiz      │
                                 └──────────────────────────────┘
```

---

## PONTOS DE DECISÃO CRÍTICOS

### 1. TESTER-BACKEND (Aprovação de Contrato)

**Ponto de decisão:**
- Backend rejeita todas as violações?
- Erros são estruturados?
- Permissões estão corretas?

**Se APROVADO:**
- Atualiza STATUS.yaml com `contrato_validado: true`
- Permite transição para testes

**Se REPROVADO:**
- Backend retorna para Developer
- NÃO pode avançar para testes
- Deve corrigir e re-submeter

---

### 2. EXECUÇÃO DE TESTES (Aprovação de Qualidade)

**Ponto de decisão:**
- Taxa de aprovação = 100%?
- Todos os testes passaram?
- Evidências foram geradas?

**Se APROVADO:**
- Atualiza STATUS.yaml com `contrato_ativo: DEPLOY`
- Permite transição para deploy

**Se REPROVADO (taxa < 100%):**
- Identifica falhas
- Corrige código (backend ou frontend)
- Re-executa testes
- NÃO pode avançar até taxa = 100%

---

### 3. DEPLOY (Aprovação de Smoke Tests)

**Ponto de decisão:**
- Smoke tests passaram?
- Backend health OK?
- Frontend acessível?

**Se APROVADO:**
- Deploy bem-sucedido
- Versão registrada
- FIM DO FLUXO

**Se REPROVADO:**
- Rollback AUTOMÁTICO
- Versão anterior restaurada
- Investigação obrigatória

---

## FLUXOS ALTERNATIVOS

### Fluxo com Frontend

```
RF + MD + UC + WF PRONTOS
    │
    ▼
CONTRATO-EXECUCAO-BACKEND
    │
    ▼
CONTRATO-TESTER-BACKEND (APROVADO)
    │
    ▼
CONTRATO-TRANSICAO-BACKEND-PARA-TESTES
    │
    ▼
CONTRATO-EXECUCAO-FRONTEND ◄─── NOVO PASSO
    │
    ▼
CONTRATO-EXECUCAO-TESTES
    │
    ▼
CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
    │
    ▼
CONTRATO-EXECUCAO-DEPLOY
```

---

### Fluxo com Backend Legado

```
RF + MD + UC + WF PRONTOS
    │
    ▼
CONTRATO-REGULARIZACAO-BACKEND ◄─── SUBSTITUI EXECUCAO-BACKEND
    │
    ▼
CONTRATO-TESTER-BACKEND (APROVADO)
    │
    ▼
CONTRATO-TRANSICAO-BACKEND-PARA-TESTES
    │
    ▼
CONTRATO-EXECUCAO-TESTES
    │
    ▼
CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
    │
    ▼
CONTRATO-EXECUCAO-DEPLOY
```

---

### Fluxo de Correção de Bug

```
CONTRATO-DEBUG-CONTROLADO
    │
    │ identifica causa raiz
    ▼
CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA
    │
    ▼
CONTRATO-EXECUCAO-TESTES ◄─── RETORNA AO FLUXO PRINCIPAL
    │
    ▼
CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
    │
    ▼
CONTRATO-EXECUCAO-DEPLOY
```

---

## ATUALIZAÇÃO DE STATUS.yaml POR FASE

### Fase: Backend Implementado

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: false  # Ainda NÃO validado

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-BACKEND

devops:
  board_column: "Backend Implementado"
```

---

### Fase: Backend Aprovado pelo Tester

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true        # ✅ VALIDADO
    contrato: CONTRATO-EXECUCAO-BACKEND
    versao_contrato: v1.0

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-BACKEND

devops:
  board_column: "Backend Validado"
```

---

### Fase: Transição para Testes

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true
    contrato: CONTRATO-EXECUCAO-BACKEND
    versao_contrato: v1.0

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-TESTES  # ✅ MUDOU

devops:
  board_column: "Pronto para Testes"        # ✅ MUDOU
```

---

### Fase: Testes Aprovados

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true

  frontend:
    status: done

testes:
  backend: pass
  frontend: pass
  e2e: pass
  seguranca: pass

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-TESTES

devops:
  board_column: "Testes Aprovados"
```

---

### Fase: Transição para Deploy

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true

  frontend:
    status: done

testes:
  backend: pass
  frontend: pass
  e2e: pass
  seguranca: pass

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-DEPLOY  # ✅ MUDOU

devops:
  board_column: "Pronto para Deploy"        # ✅ MUDOU
```

---

### Fase: Deploy Bem-Sucedido

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true

  frontend:
    status: done

testes:
  backend: pass
  frontend: pass
  e2e: pass
  seguranca: pass

governanca:
  contrato_ativo: CONTRATO-EXECUCAO-DEPLOY

devops:
  board_column: "Produção"                   # ✅ MUDOU
  deployed_version: "1.2.0"
  deployed_commit: "abc123def456"
  last_deploy: "2025-12-26 14:30:00"
```

---

### Fase: Rollback Executado

```yaml
desenvolvimento:
  backend:
    status: done
    contrato_validado: true

  frontend:
    status: done

testes:
  backend: pass
  frontend: pass
  e2e: pass
  seguranca: pass

governanca:
  contrato_ativo: CONTRATO-ROLLBACK          # ✅ MUDOU

devops:
  board_column: "Rollback Executado"         # ✅ MUDOU
  deployed_version: "1.1.0"                  # Versão anterior
  deployed_commit: "xyz789abc123"
  last_deploy: "2025-12-25 10:00:00"
  last_rollback: "2025-12-26 14:35:00"       # ✅ NOVO
  rollback_reason: "Smoke tests failed"      # ✅ NOVO
```

---

## GATILHOS EXPLÍCITOS

### Gatilho 1: Backend Aprovado → Transição para Testes

**Condição:**
- EXECUTION-MANIFEST tem decisão APROVADA do Tester-Backend
- STATUS.yaml tem `contrato_validado: true`

**Ação:**
- Executar CONTRATO-TRANSICAO-BACKEND-PARA-TESTES
- Atualizar `contrato_ativo: CONTRATO-EXECUCAO-TESTES`
- Sincronizar Azure DevOps

---

### Gatilho 2: Testes Aprovados → Transição para Deploy

**Condição:**
- EXECUTION-MANIFEST tem decisão APROVADA de testes
- Taxa de aprovação = 100%

**Ação:**
- Executar CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- Atualizar `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`
- Sincronizar Azure DevOps

---

### Gatilho 3: Smoke Tests Falharam → Rollback Automático

**Condição:**
- Deploy executado
- Smoke tests retornaram FAIL

**Ação:**
- Executar CONTRATO-ROLLBACK (automático)
- Reverter para versão anterior
- Smoke tests pós-rollback
- Registrar motivo

---

## BLOQUEIOS AUTOMÁTICOS

### Bloqueio 1: Backend SEM validação de contrato

**Tentativa bloqueada:**
- Executar CONTRATO-EXECUCAO-TESTES sem `contrato_validado: true`

**Mensagem:**
```
[BLOQUEADO] Backend não foi validado pelo Tester-Backend
Execute primeiro: CONTRATO-EXECUCAO-TESTER-BACKEND
```

---

### Bloqueio 2: Testes com taxa < 100%

**Tentativa bloqueada:**
- Executar CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY com taxa < 100%

**Mensagem:**
```
[BLOQUEADO] Taxa de aprovação de testes: 85%
Critério mínimo: 100%
Corrija falhas e re-execute CONTRATO-EXECUCAO-TESTES
```

---

### Bloqueio 3: Deploy sem transição aprovada

**Tentativa bloqueada:**
- Executar CONTRATO-EXECUCAO-DEPLOY sem transição registrada

**Mensagem:**
```
[BLOQUEADO] Transição para deploy não foi aprovada
Execute primeiro: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
```

---

## VALIDAÇÃO DE FLUXO

Para validar se o RF está no contrato correto antes de executar próximo passo:

```bash
python d:/IC2tools/contract-validator/validate-transitions.py RFXXX PROXIMO-CONTRATO
```

**Exemplo de uso:**

```bash
# Verificar se RF046 pode ir para TESTES
python validate-transitions.py RF046 CONTRATO-EXECUCAO-TESTES

# Saída esperada (se válido):
[OK] Transição permitida
Estado atual do RF046: CONTRATO-EXECUCAO-BACKEND
Próximo contrato: CONTRATO-EXECUCAO-TESTES
Transição: PERMITIDA
```

```bash
# Verificar se RF046 pode ir para DEPLOY (sem passar por testes)
python validate-transitions.py RF046 CONTRATO-EXECUCAO-DEPLOY

# Saída esperada (se inválido):
[ERRO] Transição não permitida
Estado atual do RF046: CONTRATO-EXECUCAO-BACKEND
Próximo contrato: CONTRATO-EXECUCAO-DEPLOY
Motivo: Contratos intermediários obrigatórios: TESTER-BACKEND, TESTES, TRANSICAO-DEPLOY
```

---

## RASTREABILIDADE COMPLETA

Cada execução gera registro no EXECUTION-MANIFEST, permitindo rastrear:

1. **O QUE** foi alterado → RF identificado
2. **QUANDO** foi alterado → Timestamp em cada execução
3. **QUEM** autorizou → Autoridade no bloco `decision`
4. **POR QUE** foi alterado → Contrato ativo + motivo
5. **COMO** foi validado → Decisão APROVADA/REPROVADA + evidências

**Exemplo de rastreabilidade de RF046:**

```markdown
# EXECUTION-MANIFEST.md

## RF046 - Cadastro de Departamentos

### Execução 1: Backend Implementado
- ID: RF046-BACKEND-20251226-100000
- Contrato: CONTRATO-EXECUCAO-BACKEND
- Tipo: OPERACIONAL
- Executor: Developer Agent
- Data: 2025-12-26 10:00:00

### Execução 2: Backend Validado
- ID: RF046-TESTER-BACKEND-20251226-110000
- Contrato: CONTRATO-EXECUCAO-TESTER-BACKEND
- Tipo: DECISÓRIA
- Executor: Tester-Backend Agent
- Data: 2025-12-26 11:00:00
- Decisão: APROVADO

### Execução 3: Transição para Testes
- ID: RF046-TRANSITION-BACKEND-TO-TESTS-20251226-110500
- Contrato: CONTRATO-TRANSICAO-BACKEND-PARA-TESTES
- Tipo: DECISÓRIA
- Executor: DevOps Agent
- Data: 2025-12-26 11:05:00
- Decisão: APROVADO

### Execução 4: Testes Executados
- ID: RF046-TESTES-20251226-140000
- Contrato: CONTRATO-EXECUCAO-TESTES
- Tipo: DECISÓRIA
- Executor: QA Agent
- Data: 2025-12-26 14:00:00
- Taxa de aprovação: 100%
- Decisão: APROVADO

### Execução 5: Transição para Deploy
- ID: RF046-TRANSITION-TESTS-TO-DEPLOY-20251226-150000
- Contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- Tipo: DECISÓRIA
- Executor: DevOps Agent
- Data: 2025-12-26 15:00:00
- Decisão: APROVADO

### Execução 6: Deploy Realizado
- ID: RF046-DEPLOY-20251226-160000
- Contrato: CONTRATO-EXECUCAO-DEPLOY
- Tipo: DECISÓRIA
- Executor: DevOps Agent
- Data: 2025-12-26 16:00:00
- Ambiente: HOM
- Versão: 1.2.0
- Commit: abc123def456
- Smoke tests: PASS
- Decisão: APROVADO
```

---

## RESUMO VISUAL DE ESTADOS

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   BACKEND   │ ──► │   TESTER    │ ──► │   TESTES    │ ──► │   DEPLOY    │
│             │     │             │     │             │     │             │
│ Implementa  │     │  Valida     │     │  Executa    │     │  Deploya    │
│ código      │     │  contrato   │     │  100% taxa  │     │  + Smoke    │
└─────────────┘     └─────────────┘     └─────────────┘     └──────┬──────┘
                                                                    │
                    APROVADO        APROVADO        APROVADO        │
                        ✓               ✓               ✓           │
                                                                    │
                                                                    ▼
                                                            ┌───────────────┐
                                                            │ PASS ou FAIL? │
                                                            └───┬───────┬───┘
                                                                │       │
                                                             PASS       FAIL
                                                                │       │
                                                                ▼       ▼
                                                            ┌────┐  ┌─────────┐
                                                            │FIM │  │ROLLBACK │
                                                            └────┘  └─────────┘
```

---

**FIM DO DOCUMENTO**

# FLUXO DE TRANSIÇÃO – SKELETON → BACKEND COMPLETO

Este documento define o **fluxo obrigatório de transição** quando um RF
é criado inicialmente como Skeleton (Base de Entidade).

---

## VISÃO GERAL DO FLUXO

```
┌──────────────────────────────────────────────────────────────────┐
│                    CICLO DE VIDA DO RF                           │
└──────────────────────────────────────────────────────────────────┘

1. CONTRATO DE BASE DE ENTIDADE
   │
   ├─> Cria estrutura CRUD básica (backend + frontend)
   ├─> Valida navegação funcional
   ├─> STATUS.yaml: skeleton.criado = True
   ├─> STATUS.yaml: desenvolvimento.backend.status = "skeleton"
   ├─> STATUS.yaml: desenvolvimento.frontend.status = "skeleton"
   └─> Board: coluna "Skeleton"
   │
   │
2. CONTRATO DE REGULARIZAÇÃO DE BACKEND
   │
   ├─> Audita backend Skeleton
   ├─> Identifica gaps em relação ao RF/UC/MD
   ├─> Implementa regras de negócio faltantes
   ├─> Implementa validações completas
   ├─> Implementa estados e transições (se aplicável)
   ├─> STATUS.yaml: desenvolvimento.backend.status = "in_progress"
   └─> Preserva compatibilidade com frontend Skeleton
   │
   │
3. CONTRATO DE TESTER-BACKEND
   │
   ├─> Cria contrato de teste derivado
   ├─> Cria matriz de violação
   ├─> Implementa testes automatizados
   ├─> Valida que backend REJEITA payloads inválidos
   ├─> AUTORIDADE para bloquear merge se violações aceitas
   └─> STATUS.yaml: desenvolvimento.backend.status = "done"
   │
   │
4. CONTRATO DE EXECUÇÃO – FRONTEND (completo)
   │
   ├─> Implementa regras de negócio no frontend
   ├─> Implementa validações avançadas
   ├─> Implementa workflows visuais
   ├─> Implementa estados visuais
   ├─> STATUS.yaml: desenvolvimento.frontend.status = "in_progress"
   └─> STATUS.yaml: desenvolvimento.frontend.status = "done"
   │
   │
5. CONTRATO DE EXECUÇÃO DE TESTES (E2E)
   │
   ├─> Valida fluxo completo (backend + frontend)
   ├─> Testes E2E automatizados
   ├─> Testes de segurança
   └─> STATUS.yaml: testes.e2e = "pass"
```

---

## ESTADO 1: SKELETON (BASE DE ENTIDADE)

### Artefatos Criados

**Backend:**
- Entidade Domain básica
- Commands/Queries CRUD padrão
- Validators mínimos
- DTOs básicos
- Controller/Endpoints HTTP
- Seeds de permissões básicas

**Frontend:**
- Listagem básica
- Formulário básico
- Serviço HTTP CRUD
- Rota e navegação
- i18n mínimo

### STATUS.yaml

```yaml
skeleton:
  criado: True
  data_criacao: "2025-12-27"
  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."

desenvolvimento:
  backend:
    status: skeleton          # NÃO "done"
  frontend:
    status: skeleton          # NÃO "done"

governanca:
  contrato_ativo: "CONTRATO-BASE-DE-ENTIDADE"
  proximo_contrato: "CONTRATO-REGULARIZACAO-BACKEND"
```

### Proibições Absolutas

- ❌ Marcar `desenvolvimento.backend.status = "done"`
- ❌ Marcar `desenvolvimento.frontend.status = "done"`
- ❌ Executar CONTRATO DE TESTER-BACKEND
- ❌ Executar CONTRATO DE EXECUÇÃO DE TESTES
- ❌ Pular CONTRATO DE REGULARIZAÇÃO DE BACKEND

### Próximo Passo Obrigatório

**CONTRATO DE REGULARIZAÇÃO DE BACKEND**

---

## ESTADO 2: REGULARIZAÇÃO (EM PROGRESSO)

### Ações Permitidas

**Backend:**
- Implementar regras de negócio completas
- Implementar validações avançadas
- Implementar estados e transições
- Implementar workflows de aprovação
- Ajustar DTOs conforme RF/UC/MD
- Criar validações compostas
- Implementar auditoria customizada (se necessário)

**Frontend:**
- Preservar funcionalidade básica
- NÃO quebrar CRUD existente
- Ajustes mínimos se necessário

### STATUS.yaml

```yaml
skeleton:
  criado: True                # Mantém histórico
  data_criacao: "2025-12-27"
  data_regularizacao_inicio: "2025-12-28"

desenvolvimento:
  backend:
    status: in_progress       # Mudou de "skeleton" para "in_progress"
    branch: "feature/RFXXX-regularizacao-backend"
  frontend:
    status: skeleton          # Permanece "skeleton"

governanca:
  contrato_ativo: "CONTRATO-REGULARIZACAO-BACKEND"
  proximo_contrato: "CONTRATO-TESTER-BACKEND"
```

### Proibições

- ❌ Quebrar compatibilidade com frontend Skeleton
- ❌ Criar novas funcionalidades fora do RF
- ❌ Alterar payloads públicos sem necessidade
- ❌ Executar CONTRATO DE TESTER-BACKEND (ainda)

### Critério de Pronto

- ✅ Backend 100% aderente ao RF/UC/MD
- ✅ Regras de negócio implementadas
- ✅ Validações completas implementadas
- ✅ Estados e transições implementados (se aplicável)
- ✅ Build sem erros
- ✅ Seeds atualizados e idempotentes

### Próximo Passo Obrigatório

**CONTRATO DE TESTER-BACKEND**

---

## ESTADO 3: VALIDAÇÃO DE CONTRATO (TESTER-BACKEND)

### Ações Executadas

- Criar `backend.test.contract.yaml`
- Criar `violations.matrix.md`
- Implementar testes de violação
- Validar que backend REJEITA payloads inválidos
- Validar erros estruturados
- Validar códigos HTTP corretos

### STATUS.yaml

```yaml
skeleton:
  criado: True
  data_criacao: "2025-12-27"
  data_regularizacao_inicio: "2025-12-28"
  data_regularizacao_conclusao: "2025-12-29"
  data_validacao_inicio: "2025-12-29"

desenvolvimento:
  backend:
    status: done              # Mudou para "done" APÓS aprovação Tester
    branch: null              # Mergeado em dev
  frontend:
    status: skeleton          # Permanece "skeleton"

testes:
  backend: pass               # Testes de contrato passaram

governanca:
  contrato_ativo: "CONTRATO-TESTER-BACKEND"
  proximo_contrato: "CONTRATO-EXECUCAO-FRONTEND"
```

### Autoridade do Tester-Backend

O agente Tester-Backend TEM AUTORIDADE para:

- ✅ BLOQUEAR merge se backend aceita violações
- ✅ EXIGIR correções antes de aprovar
- ✅ NEGAR aprovação se erros não estruturados

### Critério de Aprovação

- ✅ Backend REJEITA todos os payloads inválidos
- ✅ Erros estruturados com códigos HTTP corretos
- ✅ 100% dos testes de violação passam
- ✅ Matriz de violação completa

### Próximo Passo Obrigatório

**CONTRATO DE EXECUÇÃO – FRONTEND (completo)**

---

## ESTADO 4: FRONTEND COMPLETO

### Ações Permitidas

**Frontend:**
- Implementar regras de negócio visuais
- Implementar validações avançadas
- Implementar workflows visuais
- Implementar estados visuais (aprovado, rejeitado, etc.)
- Implementar integrações com outros módulos
- Implementar dashboards/relatórios (se aplicável)

**Backend:**
- NÃO alterar (já aprovado pelo Tester)
- Apenas ajustes se necessário (sob CONTRATO DE MANUTENÇÃO)

### STATUS.yaml

```yaml
skeleton:
  criado: True
  data_criacao: "2025-12-27"
  data_regularizacao_conclusao: "2025-12-29"
  data_validacao_conclusao: "2025-12-29"
  data_frontend_inicio: "2025-12-30"

desenvolvimento:
  backend:
    status: done              # Permanece "done"
  frontend:
    status: in_progress       # Mudou de "skeleton" para "in_progress"
    branch: "feature/RFXXX-frontend-completo"

governanca:
  contrato_ativo: "CONTRATO-EXECUCAO-FRONTEND"
  proximo_contrato: "CONTRATO-EXECUCAO-TESTES"
```

### Critério de Pronto

- ✅ Frontend 100% aderente ao RF/UC/WF
- ✅ Regras de negócio visuais implementadas
- ✅ Validações avançadas implementadas
- ✅ Workflows visuais implementados
- ✅ i18n completo (100% das chaves)
- ✅ Permissões aplicadas em todos os elementos
- ✅ Build sem erros

### Próximo Passo Obrigatório

**CONTRATO DE EXECUÇÃO DE TESTES (E2E)**

---

## ESTADO 5: TESTES E2E

### Ações Executadas

- Validar dependências funcionais
- Executar testes E2E automatizados (Playwright)
- Executar testes de segurança
- Criar registro de evidência final

### STATUS.yaml

```yaml
desenvolvimento:
  backend:
    status: done
  frontend:
    status: done              # Mudou para "done" APÓS testes E2E passarem

testes:
  backend: pass
  frontend: pass
  e2e: pass                   # E2E aprovado
  seguranca: pass

testes_qa:
  executado: True
  aprovado: True

governanca:
  contrato_ativo: "CONTRATO-EXECUCAO-TESTES"
  proximo_contrato: "CONTRATO-DEPLOY-AZURE"
```

### Critério de Aprovação

- ✅ 100% dos testes E2E passam
- ✅ 100% dos testes de segurança passam
- ✅ Todas as dependências validadas
- ✅ Registro de evidência criado

---

## TABELA DE TRANSIÇÕES

| Estado Atual | Contrato Executado | Próximo Estado | STATUS.yaml: backend.status | STATUS.yaml: frontend.status |
|--------------|-------------------|----------------|----------------------------|------------------------------|
| Inicial | CONTRATO-BASE-DE-ENTIDADE | Skeleton | skeleton | skeleton |
| Skeleton | CONTRATO-REGULARIZACAO-BACKEND | Regularização | in_progress | skeleton |
| Regularização | CONTRATO-TESTER-BACKEND | Validado | done | skeleton |
| Validado | CONTRATO-EXECUCAO-FRONTEND | Frontend Completo | done | in_progress |
| Frontend Completo | CONTRATO-EXECUCAO-TESTES | Aprovado | done | done |
| Aprovado | CONTRATO-DEPLOY-AZURE | Produção | done | done |

---

## REGRAS DE TRANSIÇÃO

### Transições Permitidas

```
Skeleton → Regularização → Validado → Frontend Completo → Aprovado → Produção
```

### Transições PROIBIDAS

❌ **Skeleton → Validado** (pular Regularização)
❌ **Skeleton → Frontend Completo** (pular Regularização + Validação)
❌ **Skeleton → Aprovado** (pular todas as fases)
❌ **Regularização → Frontend Completo** (pular Validação)
❌ **Skeleton → Produção** (NUNCA)

### Regra de Bloqueio

Se o agente tentar executar uma transição proibida:

➡️ O agente DEVE PARAR
➡️ O agente DEVE AVISAR sobre a transição inválida
➡️ O agente DEVE informar o próximo contrato correto
➡️ Nenhuma ação parcial pode ser executada

---

## SCRIPT DE VALIDAÇÃO

Antes de executar qualquer contrato, validar a transição:

```bash
python tools/contract-validator/validate-transitions.py RFXXX PROXIMO-CONTRATO
```

Exemplo:

```bash
# Validar se pode executar Tester-Backend
python tools/contract-validator/validate-transitions.py RF046 CONTRATO-TESTER-BACKEND

# Saída esperada:
# ✅ Transição permitida: Skeleton → Regularização → Tester-Backend
# ✅ STATUS.yaml: desenvolvimento.backend.status = "in_progress"
# ✅ Contrato anterior: CONTRATO-REGULARIZACAO-BACKEND
```

---

## RESUMO EXECUTIVO

**Fluxo Obrigatório:**

1. **CONTRATO-BASE-DE-ENTIDADE** → Cria Skeleton
2. **CONTRATO-REGULARIZACAO-BACKEND** → Completa backend
3. **CONTRATO-TESTER-BACKEND** → Valida backend
4. **CONTRATO-EXECUCAO-FRONTEND** → Completa frontend
5. **CONTRATO-EXECUCAO-TESTES** → Valida E2E
6. **CONTRATO-DEPLOY-AZURE** → Deploy

**Transições Proibidas:**
- Pular qualquer fase
- Executar Tester-Backend sem Regularização
- Executar Frontend sem Backend validado
- Deploy sem testes E2E aprovados

**Governança:**
- STATUS.yaml rastreia toda a transição
- Campo `skeleton.criado` mantém histórico
- Campo `governanca.contrato_ativo` indica fase atual
- Campo `governanca.proximo_contrato` indica próximo passo

---

**FIM DO DOCUMENTO**

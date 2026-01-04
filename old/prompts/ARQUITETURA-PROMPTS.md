# ARQUITETURA DE PROMPTS - FLUXOGRAMA VISUAL

**Versão:** 2.1
**Data:** 2026-01-02
**Propósito:** Consulta rápida - bater o olho e saber qual prompt usar

---

## 🧭 CONSULTORIA E ORQUESTRAÇÃO (PROMPT MESTRE)

```
💡 MODO CONSULTORIA (Recomendado para começar)
   └─ \docs\prompts\consultoria.md

      O consultor irá:
      - Diagnosticar em que fase o RF está
      - Recomendar próximo passo correto
      - Validar pré-requisitos
      - Orientar correções quando necessário
      - Manter rastreabilidade via STATUS.yaml

      Use quando:
      - Não sabe qual o próximo passo
      - Quer validar se pode prosseguir
      - Precisa entender dependências
      - Quer orientação sobre correções
```

---

## 🔥 FLUXOGRAMA COMPLETO (COPIAR CAMINHOS)

```
┌─────────────────────────────────────────────────────────────────────┐
│ FASE 1: DOCUMENTAÇÃO INICIAL (3 prompts)                           │
└─────────────────────────────────────────────────────────────────────┘

1️⃣  UC (Casos de Uso)
    ├─ NOVO:    \docs\prompts\documentacao\execucao\uc-criacao.md
    └─ LEGADO:  \docs\prompts\documentacao\execucao\uc-adequacao.md
                ⬇️

2️⃣  WF (Workflow)
    └─          \docs\prompts\documentacao\execucao\wf-criacao.md
                ⬇️

3️⃣  MD (Modelo de Dados)
    └─          \docs\prompts\documentacao\execucao\md-criacao.md
                ⬇️


┌─────────────────────────────────────────────────────────────────────┐
│ FASE 2: BACKEND (2 prompts)                                        │
└─────────────────────────────────────────────────────────────────────┘

4️⃣  Backend (Implementação)
    ├─ NOVO:    \docs\prompts\desenvolvimento\execucao\backend-criacao.md
    └─ LEGADO:  \docs\prompts\desenvolvimento\execucao\backend-adequacao.md
                ⬇️

5️⃣  Validação Backend (100% OBRIGATÓRIO)
    └─          \docs\prompts\desenvolvimento\validacao\backend.md
                ⬇️ (só prossegue se APROVADO 100%)


┌─────────────────────────────────────────────────────────────────────┐
│ FASE 3: FRONTEND (2 prompts)                                       │
└─────────────────────────────────────────────────────────────────────┘

6️⃣  Frontend (Implementação)
    ├─ NOVO:    \docs\prompts\desenvolvimento\execucao\frontend-criacao.md
    └─ LEGADO:  \docs\prompts\desenvolvimento\execucao\frontend-adequacao.md
                ⬇️

7️⃣  Validação Frontend (100% OBRIGATÓRIO)
    └─          \docs\prompts\desenvolvimento\validacao\frontend.md
                ⬇️ (só prossegue se APROVADO 100%)


┌─────────────────────────────────────────────────────────────────────┐
│ FASE 4: DOCUMENTAÇÃO DE TESTES (2 prompts) ⚠️ CRITICO             │
└─────────────────────────────────────────────────────────────────────┘

8️⃣  MT + TC (Massa de Teste + Casos de Teste)
    └─          \docs\prompts\documentacao\execucao\mt-tc-criacao.md
                ⬇️

9️⃣  Validação MT + TC (100% OBRIGATÓRIO)
    └─          \docs\prompts\documentacao\validacao\mt-tc-validacao.md
                ⬇️ (só prossegue se APROVADO 100%)


┌─────────────────────────────────────────────────────────────────────┐
│ FASE 5: TESTES E2E (2 prompts)                                     │
└─────────────────────────────────────────────────────────────────────┘

🔟 Geração + Execução E2E Playwright
    └─          \docs\prompts\testes\geracao-e2e-playwright.md
                ⬇️

1️⃣1️⃣ Execução Completa (Backend + Frontend + E2E + Segurança)
    └─          \docs\prompts\testes\execucao.md
                ⬇️

                ┌─ ✅ 100% PASS → RFXXX PRONTO
                └─ ❌ < 100%    → FASE 6 (Correção)


┌─────────────────────────────────────────────────────────────────────┐
│ FASE 6: CORREÇÃO (se necessário)                                   │
└─────────────────────────────────────────────────────────────────────┘

🔧 Manutenção/Correção Controlada
    └─          \docs\prompts\desenvolvimento\execucao\manutencao-correcao-controlada.md
                ⬇️ (volta para validação ou testes)
```

---

## 📋 TABELA RÁPIDA (CTRL+F para buscar)

| Nº | Fase | Tipo | Caminho |
|---|---|---|---|
| 💡 | **META** | **Consultoria** | `\docs\prompts\consultoria.md` |
| 1️⃣ | DOC | UC Novo | `\docs\prompts\documentacao\execucao\uc-criacao.md` |
| 1️⃣ | DOC | UC Legado | `\docs\prompts\documentacao\execucao\uc-adequacao.md` |
| 2️⃣ | DOC | WF | `\docs\prompts\documentacao\execucao\wf-criacao.md` |
| 3️⃣ | DOC | MD | `\docs\prompts\documentacao\execucao\md-criacao.md` |
| 4️⃣ | DEV | Backend Novo | `\docs\prompts\desenvolvimento\execucao\backend-criacao.md` |
| 4️⃣ | DEV | Backend Legado | `\docs\prompts\desenvolvimento\execucao\backend-adequacao.md` |
| 5️⃣ | VAL | Validação Backend | `\docs\prompts\desenvolvimento\validacao\backend.md` |
| 6️⃣ | DEV | Frontend Novo | `\docs\prompts\desenvolvimento\execucao\frontend-criacao.md` |
| 6️⃣ | DEV | Frontend Legado | `\docs\prompts\desenvolvimento\execucao\frontend-adequacao.md` |
| 7️⃣ | VAL | Validação Frontend | `\docs\prompts\desenvolvimento\validacao\frontend.md` |
| 8️⃣ | DOC | MT+TC Criação | `\docs\prompts\documentacao\execucao\mt-tc-criacao.md` |
| 9️⃣ | VAL | MT+TC Validação | `\docs\prompts\documentacao\validacao\mt-tc-validacao.md` |
| 🔟 | TEST | E2E Playwright | `\docs\prompts\testes\geracao-e2e-playwright.md` |
| 1️⃣1️⃣ | TEST | Testes Completos | `\docs\prompts\testes\execucao.md` |
| 🔧 | FIX | Correção | `\docs\prompts\desenvolvimento\execucao\manutencao-correcao-controlada.md` |

---

## 🚀 EXEMPLO VISUAL - RF060 (LEGADO)

```
RF060 (tem UC, backend e frontend legado)

1️⃣  uc-adequacao.md          ✅ (adequar UC legado)
      ⬇️
2️⃣  wf-criacao.md            ✅ (criar workflow)
      ⬇️
3️⃣  md-criacao.md            ✅ (criar modelo de dados)
      ⬇️
4️⃣  backend-adequacao.md     ✅ (adequar backend legado)
      ⬇️
5️⃣  validacao-backend.md     ✅ (validar 100%)
      ⬇️
6️⃣  frontend-adequacao.md    ✅ (adequar frontend legado)
      ⬇️
7️⃣  validacao-frontend.md    ✅ (validar 100%)
      ⬇️
8️⃣  mt-tc-criacao.md         ✅ (criar MT e TC)
      ⬇️
9️⃣  mt-tc-validacao.md       ✅ (validar MT e TC 100%)
      ⬇️
🔟 geracao-e2e-playwright.md ✅ (gerar e executar E2E)
      ⬇️
1️⃣1️⃣ execucao-testes.md        ✅ (executar todas camadas)
      ⬇️
      ┌─ ✅ 100% → RF060 PRONTO
      └─ ❌ < 100% → manutencao-correcao-controlada.md
```

---

## 🆕 EXEMPLO VISUAL - RF070 (NOVO)

```
RF070 (não tem nada - criar do zero)

1️⃣  uc-criacao.md            ✅ (criar UC do zero)
      ⬇️
2️⃣  wf-criacao.md            ✅ (criar workflow)
      ⬇️
3️⃣  md-criacao.md            ✅ (criar modelo de dados)
      ⬇️
4️⃣  backend-criacao.md       ✅ (criar backend do zero)
      ⬇️
5️⃣  validacao-backend.md     ✅ (validar 100%)
      ⬇️
6️⃣  frontend-criacao.md      ✅ (criar frontend do zero)
      ⬇️
7️⃣  validacao-frontend.md    ✅ (validar 100%)
      ⬇️
8️⃣  mt-tc-criacao.md         ✅ (criar MT e TC)
      ⬇️
9️⃣  mt-tc-validacao.md       ✅ (validar MT e TC 100%)
      ⬇️
🔟 geracao-e2e-playwright.md ✅ (gerar e executar E2E)
      ⬇️
1️⃣1️⃣ execucao-testes.md        ✅ (executar todas camadas)
      ⬇️
      ✅ 100% → RF070 PRONTO
```

---

## 🎯 DECISÃO RÁPIDA

### Não sei qual o próximo passo?
- **USE** → `consultoria.md` (RECOMENDADO PARA COMEÇAR)

### Tenho UC legado?
- **SIM** → `uc-adequacao.md`
- **NÃO** → `uc-criacao.md`

### Tenho backend legado?
- **SIM** → `backend-adequacao.md`
- **NÃO** → `backend-criacao.md`

### Tenho frontend legado?
- **SIM** → `frontend-adequacao.md`
- **NÃO** → `frontend-criacao.md`

### Validação reprovou?
- **SIM** → `manutencao-correcao-controlada.md`
- **NÃO** → Prosseguir próxima fase

### Testes E2E falharam?
- **SIM** → `manutencao-correcao-controlada.md`
- **NÃO** → RFXXX PRONTO ✅

### Preciso entender dependências entre fases?
- **USE** → `consultoria.md`

---

## ⚠️ REGRAS DE OURO

```
❌ NUNCA pular etapas
❌ NUNCA aprovar com ressalvas
❌ NUNCA prosseguir se validação < 100%

✅ SEMPRE seguir ordem sequencial
✅ SEMPRE validar backend ANTES de frontend
✅ SEMPRE MT ANTES de TC
✅ SEMPRE testes E2E DEPOIS de validações

📋 PRÉ-REQUISITOS OBRIGATÓRIOS:
- Backend só inicia se UC existe + (MD existe OU md: false com justificativa)
- Frontend só inicia se backend 100% aprovado + (WF existe OU wf: false com justificativa)
- MT+TC só iniciam se backend E frontend 100% aprovados
- E2E só inicia se MT+TC validados 100%
```

---

## 📦 PACOTES PRONTOS (COPIAR TUDO)

### 📄 Documentação Inicial (3 prompts)
```
\docs\prompts\documentacao\execucao\uc-criacao.md
\docs\prompts\documentacao\execucao\wf-criacao.md
\docs\prompts\documentacao\execucao\md-criacao.md
```

### 🔧 Backend Completo (2 prompts)
```
\docs\prompts\desenvolvimento\execucao\backend-criacao.md
\docs\prompts\desenvolvimento\validacao\backend.md
```

### 🎨 Frontend Completo (2 prompts)
```
\docs\prompts\desenvolvimento\execucao\frontend-criacao.md
\docs\prompts\desenvolvimento\validacao\frontend.md
```

### 📋 Documentação de Testes (2 prompts) ⚠️ APÓS FRONTEND 100%
```
\docs\prompts\documentacao\execucao\mt-tc-criacao.md
\docs\prompts\documentacao\validacao\mt-tc-validacao.md
```

**IMPORTANTE:** MT e TC precisam de backend E frontend 100% aprovados porque:
- MT define payloads reais (precisa conhecer contratos de API)
- MT define estados reais (precisa conhecer estados do frontend)
- TC testa fluxos completos (precisa de backend + frontend juntos)

**ESTRUTURA DE ARQUIVOS:**
- MT-RF[XXX].yaml (exemplo: MT-RF006.yaml)
- TC-RF[XXX].yaml (exemplo: TC-RF006.yaml)
- Local: D:\IC2\docs\rf\[FASE]\[EPIC]\[RFXXX]\

### 🧪 Testes E2E Completo (2 prompts) ⚠️ APÓS MT+TC 100%
```
\docs\prompts\testes\geracao-e2e-playwright.md
\docs\prompts\testes\execucao.md
```

---

**FIM - VERSÃO VISUAL SIMPLIFICADA**

# MANUAL DO USUÁRIO - IControlIT 2.0

**Versão:** 1.0.0
**Data:** 2025-12-28
**Público:** Usuário humano (você que está lendo isso!)

---

## 📖 Como Usar Este Manual

Este manual mostra **exatamente o que VOCÊ deve fazer** para trabalhar com RFs no projeto IControlIT.

**O que você vai encontrar:**
- ✅ Qual prompt enviar
- ✅ Quando enviar
- ✅ O que esperar como resultado
- ✅ Como validar que deu certo

**O que NÃO está aqui:**
- ❌ Detalhes técnicos internos da IA
- ❌ Documentação de código
- ❌ Arquitetura interna

---

## 🎯 Regra de Ouro

**Antes de QUALQUER ação, decida:**

```
┌─────────────────────────────────────┐
│ O backend deste RF já existe?       │
└─────────────────────────────────────┘
           │
           ├─── NÃO ──→ FLUXO 1: RF NOVO
           │
           └─── SIM ──→ O backend está modernizado?
                        │
                        ├─── NÃO ──→ FLUXO 2: ADEQUAÇÃO
                        │
                        └─── SIM ──→ FLUXO 3: MANUTENÇÃO
```

---

## 📋 FLUXO 1: RF NOVO (Backend não existe)

**Quando usar:** Você quer criar um RF completamente novo, sem código backend existente.

### Passo 1: Preparar Ambiente

**Comando que VOCÊ digita:**
```
/start-rf
```

**IA perguntará:** Qual RF deseja iniciar?
**Você responde:** RF-XXX (exemplo: RF-028)

**O que a IA faz:**
- ✅ Valida que documentação existe
- ✅ Cria branch `feature/RF-XXX-backend`
- ✅ Verifica portas 5000 e 4200/8080 livres
- ✅ Cria checklist de próximos passos

**Como validar:**
- Branch criado: `git branch` deve mostrar `feature/RF-XXX-backend`
- Checklist aparece na resposta da IA

---

### Passo 2: Criar Documentação

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO-DOCUMENTACAO-ESSENCIAL para RF-XXX
```

**Substitua:** RF-XXX pelo número real (ex: RF-028)

**O que a IA faz:**
1. Lê código legado (se houver)
2. Cria 5 arquivos:
   - RF-XXX.md (requisito funcional)
   - UC-RF-XXX.md (casos de uso)
   - MD-RF-XXX.md (modelo de dados)
   - WF-RF-XXX.md (wireframes)
   - user-stories.yaml (user stories para Azure DevOps)
3. Atualiza STATUS.yaml (documentacao.* = True)
4. Faz commit e merge para `dev`

**Como validar:**
- Arquivos criados em `rf/Fase-X/EPIC-XXX/RF-XXX/`
- STATUS.yaml com `documentacao: { documentacao: True, uc: True, md: True, wf: True, user_stories: True }`

**Tempo estimado:** 30-60 minutos

---

### Passo 3: Implementar Backend

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE EXECUÇÃO – BACKEND para RF-XXX
```

**O que a IA faz:**
1. Cria branch `feature/RF-XXX-backend`
2. Implementa:
   - Entities (Domain)
   - Commands e Queries (Application)
   - Handlers (Application)
   - API Controllers (Web)
   - Seeds de dados
   - Permissões RBAC
3. Atualiza STATUS.yaml (desenvolvimento.backend.status = "done")
4. Faz commit e merge para `dev`

**Como validar:**
- Backend compilando: `cd backend && dotnet build` (0 erros)
- Seeds criados em `D:\IC2\backend\Web/Data/Seeds/`
- STATUS.yaml com `desenvolvimento.backend.status: "done"`

**Tempo estimado:** 2-4 horas

---

### Passo 4: Validar Backend (Tester-Backend)

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE EXECUÇÃO – TESTER-BACKEND para RF-XXX
```

**O que a IA faz:**
1. Lê RF, UC, MD
2. Cria contrato de teste derivado
3. Cria matriz de violação (payloads inválidos)
4. Implementa testes automatizados focados em VIOLAÇÃO
5. Executa testes (DEVE ter 100% PASS)
6. Aprova ou bloqueia merge

**Como validar:**
- Testes executados: `cd backend && dotnet test` (100% PASS)
- Arquivo `backend.test.contract.yaml` criado
- STATUS.yaml com `testes.backend: "pass"`

**Se algum teste falhar:**
- ❌ Backend NÃO pode avançar
- Volte ao Passo 3 para corrigir

**Tempo estimado:** 1-2 horas

---

### Passo 5: Implementar Frontend

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE EXECUÇÃO – FRONTEND para RF-XXX
```

**O que a IA faz:**
1. Cria branch `feature/RF-XXX-frontend`
2. Implementa:
   - Componentes Angular
   - Services
   - Rotas
   - Traduções i18n
3. Integra com backend
4. Atualiza STATUS.yaml (desenvolvimento.frontend.status = "done")
5. Faz commit e merge para `dev`

**Como validar:**
- Frontend compilando: `cd frontend/icontrolit-app && npm run build` (0 erros)
- Rotas acessíveis: `http://localhost:4200/admin/...`
- STATUS.yaml com `desenvolvimento.frontend.status: "done"`

**Tempo estimado:** 2-4 horas

---

### Passo 6: Executar Testes Completos

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE EXECUÇÃO DE TESTES para RF-XXX
```

**O que a IA faz:**
1. Executa Bateria Backend (API tests)
2. Executa Bateria Frontend (E2E Playwright)
3. Executa Bateria Outros (Segurança, Performance)
4. Atualiza STATUS.yaml (testes.* = "pass")

**Como validar:**
- Todos os testes passaram (100% PASS em cada bateria)
- STATUS.yaml com `testes: { backend: "pass", frontend: "pass", e2e: "pass", seguranca: "pass" }`

**Se algum teste falhar:**
- ❌ RF NÃO pode ser marcado como concluído
- Volte ao passo correspondente para corrigir

**Tempo estimado:** 1-2 horas

---

### Passo 7: Sincronizar com Azure DevOps

**Comando que VOCÊ digita:**
```
/sync-devops
```

**IA perguntará:** Sincronizar 1 RF ou todos?
**Você responde:** RF-XXX

**O que a IA faz:**
- Executa `python tools/devops-sync/core/sync-rf.py RF-XXX`
- Move work item para coluna correta no board
- Cria user stories (se houver user-stories.yaml)

**Como validar:**
- Abrir Azure DevOps Board: https://dev.azure.com/icontrolit/IControlIT%202.0/_boards/board
- Work item do RF-XXX na coluna correta (ex: "Testes QA" se testes passaram)

---

### Passo 8: Deploy para Homologação

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE DEPLOY – AZURE para RF-XXX em HOM
```

**O que a IA faz:**
1. Valida que testes passaram (100%)
2. Executa deploy para ambiente de homologação
3. Atualiza STATUS.yaml (deploy.homologacao = True)
4. Sincroniza DevOps

**Como validar:**
- Aplicação acessível em HOM
- STATUS.yaml com `deploy.homologacao: True`

**Tempo estimado:** 30 minutos

---

### Resumo do Fluxo 1 (RF Novo)

```
1. /start-rf
   ↓
2. CONTRATO-DOCUMENTACAO-ESSENCIAL
   ↓
3. CONTRATO DE EXECUÇÃO – BACKEND
   ↓
4. CONTRATO DE EXECUÇÃO – TESTER-BACKEND ← BLOQUEADOR (100% PASS obrigatório)
   ↓
5. CONTRATO DE EXECUÇÃO – FRONTEND
   ↓
6. CONTRATO DE EXECUÇÃO DE TESTES ← BLOQUEADOR (100% PASS obrigatório)
   ↓
7. /sync-devops
   ↓
8. CONTRATO DE DEPLOY – AZURE (HOM)
   ↓
9. (Após aprovação em HOM) CONTRATO DE DEPLOY – AZURE (PRD)
```

**Tempo total estimado:** 8-15 horas (distribuídas em 2-3 dias)

---

## 📋 FLUXO 2: ADEQUAÇÃO (Backend legado → modernizado)

**Quando usar:** Backend já existe, mas foi criado antes da governança atual (não está 100% aderente ao RF/UC/MD).

### Passo 1: Preparar Ambiente

**Comando que VOCÊ digita:**
```
/start-rf
```

(Mesmo comando do Fluxo 1)

---

### Passo 2: Regularizar Backend

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE REGULARIZAÇÃO DE BACKEND para RF-XXX
```

**O que a IA faz:**
1. Audita backend existente
2. Identifica divergências em relação ao RF
3. Corrige **apenas o necessário** para aderência
4. **NÃO quebra** compatibilidade com frontend existente
5. Atualiza STATUS.yaml
6. Faz commit

**Como validar:**
- Backend compilando: `dotnet build` (0 erros)
- Testes existentes ainda passando
- STATUS.yaml com `desenvolvimento.backend.status: "done"`

**Tempo estimado:** 2-4 horas

---

### Passo 3: Validar Backend (Tester-Backend)

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE EXECUÇÃO – TESTER-BACKEND para RF-XXX
```

(Mesmo do Fluxo 1 - Passo 4)

---

### Passo 4: Frontend

**Escolha:**

**4A. Frontend já existe e está OK:**
```
Conforme CONTRATO DE EXECUÇÃO – FRONTEND para RF-XXX (apenas validar)
```

**4B. Frontend precisa ser criado/atualizado:**
```
Conforme CONTRATO DE EXECUÇÃO – FRONTEND para RF-XXX
```

---

### Passos 5-8: Mesmos do Fluxo 1

- Passo 5: Testes completos
- Passo 6: Sincronizar DevOps
- Passo 7: Deploy HOM
- Passo 8: Deploy PRD

---

### Resumo do Fluxo 2 (Adequação)

```
1. /start-rf
   ↓
2. CONTRATO DE REGULARIZAÇÃO DE BACKEND ← DIFERENTE do Fluxo 1
   ↓
3. CONTRATO DE EXECUÇÃO – TESTER-BACKEND ← BLOQUEADOR
   ↓
4. CONTRATO DE EXECUÇÃO – FRONTEND (validar ou criar)
   ↓
5. CONTRATO DE EXECUÇÃO DE TESTES ← BLOQUEADOR
   ↓
6. /sync-devops
   ↓
7. CONTRATO DE DEPLOY – AZURE (HOM)
   ↓
8. CONTRATO DE DEPLOY – AZURE (PRD)
```

**Tempo total estimado:** 6-12 horas

---

## 📋 FLUXO 3: MANUTENÇÃO (Correção, Hotfix, Debug)

**Quando usar:** Backend e frontend já existem e estão modernizados. Você quer fazer uma correção rápida.

### Cenário 3A: Debug (Apenas Investigar)

**Quando usar:** Há um erro e você quer que a IA **investigue**, mas **NÃO corrija** ainda.

**Prompt que VOCÊ envia:**
```
Investigue o erro XYZ conforme CONTRATO DE DEBUG
```

**O que a IA faz:**
- ✅ Analisa código (read-only)
- ✅ Fornece análise técnica
- ✅ Lista hipóteses ordenadas
- ✅ Sugere plano de correção
- ❌ NÃO altera código
- ❌ NÃO cria commits

**Como validar:**
- IA fornece análise técnica
- Nenhum arquivo foi alterado: `git status` (working tree clean)

**Tempo estimado:** 15-30 minutos

---

### Cenário 3B: Correção Rápida

**Quando usar:** Correção pequena (typo, mensagem de erro, validação simples).

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE MANUTENÇÃO CURTO, corrigir [descrição do problema] no RF-XXX
```

**O que a IA faz:**
1. Corrige **apenas o problema descrito**
2. **NÃO adiciona funcionalidades**
3. **NÃO refatora código não relacionado**
4. Faz commit
5. Atualiza STATUS.yaml

**Como validar:**
- Apenas os arquivos relacionados ao problema foram alterados
- Build ainda passando: `dotnet build` ou `npm run build`

**Tempo estimado:** 15-30 minutos

---

### Cenário 3C: Manutenção de Backend

**Quando usar:** Melhorias internas de código backend sem alterar comportamento externo.

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE MANUTENÇÃO DE BACKEND, [descrição da melhoria] no RF-XXX
```

**Exemplos de uso:**
- Refatoração interna
- Otimização de queries
- Ajuste de logging
- Correção de code smells

**O que a IA PODE fazer:**
- ✅ Refatorar código interno
- ✅ Otimizar performance
- ✅ Melhorar logs

**O que a IA NÃO PODE fazer:**
- ❌ Alterar DTOs públicos
- ❌ Alterar APIs (endpoints, payloads)
- ❌ Adicionar funcionalidades
- ❌ Quebrar compatibilidade

**Como validar:**
- Build passando: `dotnet build`
- Testes passando: `dotnet test`
- APIs ainda funcionando: `curl http://localhost:5000/api/...`

**Tempo estimado:** 1-2 horas

---

### Resumo do Fluxo 3 (Manutenção)

```
Cenário A: Debug
  CONTRATO DE DEBUG → Análise (sem alterações)

Cenário B: Correção Rápida
  CONTRATO DE MANUTENÇÃO CURTO → Correção pontual

Cenário C: Manutenção Backend
  CONTRATO DE MANUTENÇÃO DE BACKEND → Melhorias internas
```

---

## 📋 FLUXO 4: DEPLOY

### Deploy para Homologação (HOM)

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE DEPLOY – AZURE para RF-XXX em HOM
```

**Pré-requisitos OBRIGATÓRIOS:**
- ✅ Testes 100% PASS
- ✅ Tester-Backend aprovado
- ✅ STATUS.yaml atualizado

**O que a IA faz:**
1. Valida pré-requisitos
2. Executa deploy para HOM
3. Atualiza STATUS.yaml (deploy.homologacao = True)
4. Sincroniza DevOps

**Como validar:**
- Aplicação acessível em HOM
- Work item no board movido para coluna "Em Homologação"

---

### Deploy para Produção (PRD)

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO DE DEPLOY – AZURE para RF-XXX em PRD
```

**Pré-requisitos OBRIGATÓRIOS:**
- ✅ Deploy em HOM concluído
- ✅ Aprovação de QA/usuário
- ✅ STATUS.yaml com deploy.homologacao = True

**O que a IA faz:**
1. Valida pré-requisitos
2. Executa deploy para PRD
3. Atualiza STATUS.yaml (deploy.producao = True)
4. Sincroniza DevOps

**Como validar:**
- Aplicação acessível em PRD
- Work item no board movido para coluna "Finalizado"

---

### Deploy HOM sem Validação (EXCEÇÃO)

**Quando usar:** Apresentações iniciais, demonstrações rápidas (USO EXCEPCIONAL).

**Prompt que VOCÊ envia:**
```
Conforme CONTRATO-DEPLOY-HOM-SEM-VALIDACAO para RF-XXX
```

**⚠️ ATENÇÃO:**
- Uso restrito a apresentações iniciais
- Risco explicitamente aceito
- Validação técnica dispensada
- **PROIBIDO para PRD**

---

## 📋 FLUXO 5: AUDITORIA

**Quando usar:** Verificar se implementação está conforme especificação.

### Auditar Backend

**Prompt que VOCÊ envia:**
```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA (escopo: Backend)
```

**O que a IA faz:**
1. Lê RF, UC, MD
2. Analisa código backend (read-only)
3. Identifica gaps (divergências)
4. Gera relatório em `relatorios/AAAA-MM-DD-RFXXX-BACKEND-Gaps.md`
5. Classifica gaps (CRÍTICO, IMPORTANTE, MENOR)

**Como validar:**
- Relatório criado em `relatorios/`
- IA **NÃO** alterou código (read-only)

---

### Auditar Frontend

**Prompt que VOCÊ envia:**
```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA (escopo: Frontend)
```

---

### Auditar Completo (Backend + Frontend)

**Prompt que VOCÊ envia:**
```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA (escopo: Completo)
```

**Tempo estimado:** 30-60 minutos

---

## 🔧 COMANDOS ÚTEIS (Atalhos)

Além dos fluxos acima, você tem comandos rápidos:

### /start-rf
Prepara ambiente para trabalhar em um RF.

**Uso:**
```
/start-rf
```

---

### /validate-rf
Valida que RF está completo e pronto para produção.

**Uso:**
```
/validate-rf
```

**IA perguntará:** Qual RF deseja validar?
**Você responde:** RF-XXX

**O que a IA faz:**
- ✅ Valida documentação (5/5)
- ✅ Valida STATUS.yaml
- ✅ Executa build backend
- ✅ Executa build frontend
- ✅ Executa testes backend
- ✅ Executa testes E2E
- ✅ Gera relatório de validação

---

### /audit-rf
Executa auditoria de conformidade.

**Uso:**
```
/audit-rf
```

**IA perguntará:** Qual RF? Qual escopo?
**Você responde:** RF-XXX, Completo

---

### /sync-devops
Sincroniza STATUS.yaml com Azure DevOps.

**Uso:**
```
/sync-devops
```

**IA perguntará:** Sincronizar 1 RF ou todos?
**Você responde:** RF-XXX (ou "todos")

---

### /fix-build
Corrige erros de compilação automaticamente.

**Uso:**
```
/fix-build
```

**O que a IA faz:**
- Detecta erros de build
- Adiciona imports faltantes
- Instala dependências ausentes
- Re-executa build

---

### /deploy-rf
Executa deploy para HOM ou PRD.

**Uso:**
```
/deploy-rf
```

**IA perguntará:** Qual RF? Qual ambiente?
**Você responde:** RF-XXX, HOM (ou PRD)

---

## 📊 FLUXO VISUAL COMPLETO

```
┌─────────────────────────────────────────────────────────────┐
│                    INÍCIO: Novo RF                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  /start-rf    │
                    └───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO-DOCUMENTACAO-        │
            │ ESSENCIAL                     │
            │ (RF, UC, MD, WF, user-stories)│
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO DE EXECUÇÃO –        │
            │ BACKEND                       │
            │ (Entities, Commands, API)     │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO DE EXECUÇÃO –        │ ← BLOQUEADOR
            │ TESTER-BACKEND                │   (100% PASS)
            │ (Testes de violação)          │
            └───────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │  100% PASS?   │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │ SIM       NÃO │
                    │  │         │  │
                    │  │         └──┼─→ VOLTAR (corrigir backend)
                    │  ▼            │
            ┌───────────────────────────────┐
            │ CONTRATO DE EXECUÇÃO –        │
            │ FRONTEND                      │
            │ (Componentes, Rotas, i18n)    │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO DE EXECUÇÃO DE       │ ← BLOQUEADOR
            │ TESTES                        │   (100% PASS)
            │ (Backend, Frontend, E2E)      │
            └───────────────────────────────┘
                            │
                    ┌───────┴───────┐
                    │  100% PASS?   │
                    └───────┬───────┘
                            │
                    ┌───────┴───────┐
                    │ SIM       NÃO │
                    │  │         │  │
                    │  │         └──┼─→ VOLTAR (corrigir)
                    │  ▼            │
                    ┌───────────────┐
                    │ /sync-devops  │
                    └───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO DE DEPLOY – AZURE    │
            │ (HOM)                         │
            └───────────────────────────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Aprovação QA  │
                    └───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │ CONTRATO DE DEPLOY – AZURE    │
            │ (PRD)                         │
            └───────────────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ RF CONCLUÍDO EM PRD   │
                └───────────────────────┘
```

---

## ❓ COMO DECIDIR QUAL FLUXO USAR

### Árvore de Decisão

```
┌─────────────────────────────────────────┐
│ Você quer criar um RF completamente     │
│ novo (backend não existe)?              │
└─────────────────────────────────────────┘
           │
           ├─── SIM ──→ FLUXO 1: RF NOVO
           │
           └─── NÃO ──→ Backend já existe?
                        │
                        └─── SIM ──→ Backend foi criado antes
                                     da governança atual?
                                     │
                                     ├─── SIM ──→ FLUXO 2: ADEQUAÇÃO
                                     │
                                     └─── NÃO ──→ O que você quer fazer?
                                                  │
                                                  ├─── Investigar erro ──→ FLUXO 3A: DEBUG
                                                  │
                                                  ├─── Correção rápida ──→ FLUXO 3B: MANUTENÇÃO CURTA
                                                  │
                                                  └─── Melhoria interna ──→ FLUXO 3C: MANUTENÇÃO BACKEND
```

---

## 📚 TEMPLATES DE PROMPTS PRONTOS

Copie e cole estes templates, substituindo `RF-XXX` pelo número do RF.

### 1. Criar RF Novo (Documentação)
```
Conforme CONTRATO-DOCUMENTACAO-ESSENCIAL para RF-XXX
```

### 2. Implementar Backend Novo
```
Conforme CONTRATO DE EXECUÇÃO – BACKEND para RF-XXX
```

### 3. Validar Backend
```
Conforme CONTRATO DE EXECUÇÃO – TESTER-BACKEND para RF-XXX
```

### 4. Implementar Frontend
```
Conforme CONTRATO DE EXECUÇÃO – FRONTEND para RF-XXX
```

### 5. Executar Testes Completos
```
Conforme CONTRATO DE EXECUÇÃO DE TESTES para RF-XXX
```

### 6. Adequar Backend Legado
```
Conforme CONTRATO DE REGULARIZAÇÃO DE BACKEND para RF-XXX
```

### 7. Debug (Investigar)
```
Investigue o erro XYZ conforme CONTRATO DE DEBUG
```

### 8. Correção Rápida
```
Conforme CONTRATO DE MANUTENÇÃO CURTO, corrigir [problema] no RF-XXX
```

### 9. Manutenção Backend
```
Conforme CONTRATO DE MANUTENÇÃO DE BACKEND, [melhoria] no RF-XXX
```

### 10. Deploy HOM
```
Conforme CONTRATO DE DEPLOY – AZURE para RF-XXX em HOM
```

### 11. Deploy PRD
```
Conforme CONTRATO DE DEPLOY – AZURE para RF-XXX em PRD
```

### 12. Auditar Conformidade
```
Auditar RF-XXX conforme CONTRATO DE AUDITORIA (escopo: Completo)
```

---

## 🚨 AVISOS IMPORTANTES

### 1. Bloqueadores (100% PASS Obrigatório)

Dois contratos são **BLOQUEADORES** e param o fluxo se falharem:

- ✋ **CONTRATO DE EXECUÇÃO – TESTER-BACKEND:** Se falhar, backend NÃO pode avançar
- ✋ **CONTRATO DE EXECUÇÃO DE TESTES:** Se falhar, RF NÃO pode ser marcado como concluído

**O que fazer se bloquear:**
1. Voltar ao passo anterior (Backend ou Frontend)
2. Corrigir o problema
3. Re-executar o contrato bloqueador
4. Só avançar com 100% PASS

---

### 2. Ordem Obrigatória

**NUNCA pule etapas!**

Ordem correta:
```
1. Documentação
2. Backend
3. Validar Backend (Tester)
4. Frontend
5. Testes
6. Deploy HOM
7. Deploy PRD
```

**❌ ERRADO:** Implementar frontend antes de validar backend
**✅ CERTO:** Backend → Tester (100%) → Frontend

---

### 3. Sincronização DevOps

**Quando sincronizar:**
- Após criar/atualizar documentação
- Após completar backend
- Após completar frontend
- Após testes passarem
- Após deploy

**Comando:**
```
/sync-devops
```

---

## 📖 GLOSSÁRIO

| Termo | Significado |
|-------|-------------|
| **RF** | Requisito Funcional (ex: RF-028) |
| **UC** | Use Case (Caso de Uso) |
| **MD** | Modelo de Dados |
| **WF** | Wireframe (fluxos de tela) |
| **Tester-Backend** | Agente que valida backend com testes de violação |
| **100% PASS** | Todos os testes passaram (nenhum falhou) |
| **BLOQUEADOR** | Etapa que para o fluxo se falhar |
| **HOM** | Homologação (ambiente de testes) |
| **PRD** | Produção (ambiente final) |
| **Skeleton** | CRUD básico sem regras completas |

---

## 🆘 TROUBLESHOOTING

### Problema: Build não compila

**Solução:**
```
/fix-build
```

---

### Problema: Testes falhando

**O que fazer:**
1. Ver qual teste falhou
2. Se for backend: voltar ao Passo 3 (CONTRATO DE EXECUÇÃO – BACKEND)
3. Se for frontend: voltar ao Passo 5 (CONTRATO DE EXECUÇÃO – FRONTEND)
4. Corrigir
5. Re-executar testes

---

### Problema: Work item não moveu no board

**Solução:**
```
/sync-devops
```

Se ainda não mover:
```
python tools/devops-sync/validation/check-work-item.py
```

---

### Problema: Erro 403 (Forbidden) nas APIs

**Causa:** Permissões RBAC não configuradas

**Solução:**
1. Verificar que seeds de permissões foram executados
2. Verificar que usuário tem perfil correto
3. Verificar que endpoint tem policy correta

---

## 📞 SUPORTE

**Documentação técnica:**
- [CLAUDE.md](../CLAUDE.md) - Governança superior
- [MATRIZ-RASTREABILIDADE.md](MATRIZ-RASTREABILIDADE.md) - Rastreabilidade completa
- [COMPLIANCE.md](COMPLIANCE.md) - Certificações (ISO, SOC, LGPD)

**Scripts úteis:**
- `tools/devops-sync/core/` - Scripts de sincronização
- `tools/status-validator/` - Validação de STATUS.yaml
- `tools/contract-validator/` - Validação de contratos

---

## ✅ CHECKLIST RÁPIDA

Antes de marcar RF como concluído, validar:

- [ ] Documentação completa (RF, UC, MD, WF, user-stories.yaml)
- [ ] Backend implementado e compilando (0 erros)
- [ ] Tester-Backend aprovado (100% PASS)
- [ ] Frontend implementado e compilando (0 erros)
- [ ] Testes Backend, Frontend, E2E, Segurança (100% PASS)
- [ ] STATUS.yaml atualizado (tudo True)
- [ ] Azure DevOps sincronizado (work item na coluna correta)
- [ ] Deploy HOM concluído
- [ ] Aprovação QA/usuário
- [ ] Deploy PRD concluído

---

**FIM DO MANUAL**

**Última atualização:** 2025-12-28
**Versão:** 1.0.0

Para dúvidas ou sugestões de melhoria, consulte a equipe de governança.

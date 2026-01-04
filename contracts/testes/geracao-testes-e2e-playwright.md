# CONTRATO DE GERAÇÃO E EXECUÇÃO DE TESTES E2E COM PLAYWRIGHT

**Versão:** 1.0
**Data:** 2026-01-02
**Status:** Ativo
**Changelog v1.0:** Criação do contrato para geração automática de specs Playwright a partir de TC e MT

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **GERA e EXECUTA testes E2E Playwright** automaticamente a partir de **TC-RFXXX.yaml** e **MT-RFXXX.yaml**, garantindo:

- ✅ **Geração Automática**: Specs Playwright (.spec.ts) gerados a partir de TC
- ✅ **Dados Automatizados**: MT usado como dados de setup antes dos testes
- ✅ **Simulação Real**: Testes simulam usuário real (clicar, preencher, navegar)
- ✅ **Validação Completa**: Todos os 4 estados renderizados (Padrão, Loading, Vazio, Erro)
- ✅ **Responsabilização**: Falhas atribuídas a backend ou frontend automaticamente
- ✅ **Evidências Automáticas**: Screenshots, vídeos, logs gerados

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador e Executor de Testes E2E Playwright |
| **Escopo** | Geração de specs + Execução + Relatório de evidências |
| **Modo** | Automação completa (sem intervenção manual) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme geracao-testes-e2e-playwright para RFXXX"**

Exemplo:
```
Conforme geracao-testes-e2e-playwright para RF060.
Seguir CLAUDE.md.
```

---

## 3. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| TC-RFXXX.yaml | Casos de teste criados e validados | Sim |
| MT-RFXXX.yaml | Massa de teste criada e validada | Sim |
| UC-RFXXX.md | Casos de uso para contexto | Sim |
| MD-RFXXX.md | Modelo de dados para setup | Sim |
| Backend aprovado | Validação backend = 100% | Sim |
| Frontend aprovado | Validação frontend = 100% | Sim |
| STATUS.yaml | `documentacao.tc = true` E `documentacao.mt = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 3.1 SETUP DE AMBIENTE (OBRIGATÓRIO - AUTOMÁTICO)

**REGRA CRÍTICA:** O agente DEVE SEMPRE iniciar backend e frontend ANTES de executar testes E2E.

**❌ NÃO assumir que aplicação está rodando**
**✅ SEMPRE iniciar backend e frontend**

### 3.1.1 Build Obrigatório

```bash
cd backend/IControlIT.API
dotnet build --no-incremental

cd frontend
npm run build
```

**Se build falhar:** REPROVAR imediatamente

### 3.1.2 Aplicar Seeds Funcionais

```bash
cd backend/IControlIT.API
dotnet ef database update
```

### 3.1.3 Iniciar Backend (Background)

```bash
cd backend/IControlIT.API
dotnet run &
```

**Aguardar pronto:** Polling em `http://localhost:5000/health` (timeout 60s)

### 3.1.4 Iniciar Frontend (Background)

```bash
cd frontend
npm start &
```

**Aguardar pronto:** Polling em `http://localhost:4200` (timeout 120s)

### 3.1.5 Validação de Ambiente

Antes de QUALQUER teste E2E:
- ✅ Backend respondendo (http://localhost:5000/health = 200)
- ✅ Frontend respondendo (http://localhost:4200 = 200)

**Se QUALQUER validação falhar:** REPROVAR com "ENVIRONMENT_SETUP_FAILED"

### 3.1.6 Credenciais de Teste (OBRIGATÓRIO)

**REGRA CRÍTICA:** NUNCA assuma credenciais. SEMPRE use as credenciais definidas nos seeds.

**Credenciais Padrão (Seeds):**

| Perfil | Email | Senha | Uso em Testes |
|--------|-------|-------|---------------|
| **Admin Teste** | `admin@teste.com` | `Test@123` | Testes gerais E2E (recomendado) |
| **Usuário Teste** | `usuario@teste.com` | `Test@123` | Testes de permissões limitadas |
| **Sem Permissão** | `sempermissao@teste.com` | `Test@123` | Testes de autorização (403) |

**Fonte de Verdade:** `backend/IControlIT.API/src/Infrastructure/Data/ApplicationDbContextInitialiser.cs`

**Exemplo em spec Playwright:**
```typescript
test('TC-E2E-001: Login e acesso ao módulo', async ({ page }) => {
  // CORRETO: Usar credenciais dos seeds
  await page.goto('http://localhost:4200/sign-in');
  await page.fill('[data-test="email"]', 'admin@teste.com');
  await page.fill('[data-test="password"]', 'Test@123');
  await page.click('[data-test="sign-in-button"]');

  // Validar login bem-sucedido
  await expect(page).toHaveURL(/dashboard/);
});
```

**PROIBIDO:**
- ❌ Assumir credenciais não documentadas
- ❌ Usar credenciais hardcoded sem validar nos seeds
- ❌ Ignorar campo `contexto.autenticacao` da MT

---

## 4. CRITÉRIO DE PRONTO

O contrato só é considerado CONCLUÍDO quando:

### 4.1 Arquivos Gerados

- [ ] `frontend/e2e/data/MT-RFXXX.data.ts` criado
- [ ] `frontend/e2e/helpers/rf-helpers.ts` criado ou atualizado
- [ ] Specs Playwright criados (1 spec por TC-E2E)
- [ ] Evidências geradas (screenshots, traces, logs)
- [ ] Relatório consolidado criado

### 4.2 Execução Bem-Sucedida

- [ ] **Taxa de aprovação = 100%** (TODOS os testes passaram)
- [ ] Todos os 4 estados validados (Padrão, Loading, Vazio, Erro)
- [ ] i18n validado (pt-BR, en-US, es-ES)
- [ ] CRUD completo validado (criar, editar, excluir, consultar)
- [ ] Segurança validada (401, 403)
- [ ] Multi-tenancy validado (isolamento entre tenants)

### 4.3 Rastreabilidade Completa

- [ ] Todos TC-E2E-NNN têm spec correspondente
- [ ] Todos specs referenciam MT correspondente
- [ ] Falhas (se houver) têm responsável identificado
- [ ] Prompts de correção gerados (se reprovado)

**REGRA DE BLOQUEIO:** Se taxa de aprovação < 100%, RF NÃO pode ser considerado PRONTO.

### 4.4 Exportação Azure DevOps (OBRIGATÓRIO)

Após executar os testes E2E, o agente DEVE atualizar os arquivos Azure DevOps com resultados:

**Atualizar `azure-test-cases-RF[XXX].csv`:**
- [ ] Coluna "State" atualizada (Design → Ready → Active → Closed)
- [ ] Resultados de execução adicionados (se aplicável)
- [ ] Data de última execução registrada

**Atualizar STATUS.yaml:**
```yaml
testes:
  azure_devops:
    ultima_execucao_e2e: "2026-01-02"
    taxa_aprovacao_e2e: "100%"
    specs_playwright_gerados: true
    total_specs_e2e: 3  # Número de specs TC-E2E
```

---

## 5. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**

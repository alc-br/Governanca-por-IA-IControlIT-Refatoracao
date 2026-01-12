# CONTRATO DE TESTES MÍNIMO VIÁVEL SEGURO (MVS)

**Versão:** 1.0
**Data:** 2026-01-11
**Status:** Ativo
**Tipo:** Contrato de Execução - Testes para Homologação
**Prioridade:** ALTA (estratégia default para HOM)

**Changelog:**
- **v1.0 (2026-01-11):** Criação do contrato MVS (Mínimo Viável Seguro) para reduzir tempo de testes de 10h para 2-4h por RF, mantendo cobertura de 80% dos riscos críticos. Baseado em análise de ROI e evidências do RF006.

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato define **TESTES MÍNIMOS OBRIGATÓRIOS** para subir RF para HOMOLOGAÇÃO, equilibrando:
- ✅ **Velocidade**: 2-4h/RF (vs 10h no modo completo)
- ✅ **Segurança**: Cobre 80% dos riscos críticos
- ✅ **Qualidade**: Critério 0% ou 100% mantido

### 🎯 Quando usar este contrato

**USE este contrato quando:**
- ✅ RF precisa subir para **HOMOLOGAÇÃO** (não PRD)
- ✅ Tempo é crítico (deadline apertado)
- ✅ Cliente precisa **VER** funcionalidade funcionando
- ✅ Aceita-se risco controlado de bugs não-críticos em HOM

**NÃO use este contrato quando:**
- ❌ RF vai direto para **PRODUÇÃO** → Use execucao-completa.md
- ❌ RF é crítico (pagamentos, segurança, dados sensíveis) → Use execucao-completa.md
- ❌ Muito tempo disponível (>10h para testes) → Use execucao-completa.md

### 📊 Comparação: Completo vs MVS

| Aspecto | Completo (OLD) | MVS (NEW) | Diferença |
|---------|----------------|-----------|-----------|
| Tempo/RF | 10+ horas | 2-4 horas | **-60-80%** |
| Testes Unitários | 100% | 100% | **Igual** |
| Testes E2E | Todos (10-30 specs) | 1 smoke test | **-90%** |
| Testes Segurança | Completo (5 tipos) | Crítico (2 tipos) | **-60%** |
| Cobertura Riscos | 95-100% | 80% | **-15-20%** |
| Confiança HOM | Máxima | Alta | Aceitável |

---

## 1. ESCOPO DE TESTES OBRIGATÓRIOS

### 1.1. Testes Unitários (Backend) - **OBRIGATÓRIO**

**Cobertura:** 100% das Regras de Negócio

**O que testar:**
- ✅ **Commands/Queries CQRS**: Todos
- ✅ **FluentValidation**: Todos os validadores
- ✅ **Regras de Negócio**: 100% das RNs do RF
- ✅ **Mapeamentos**: Domain → DTO
- ✅ **Edge cases**: Casos extremos documentados

**Critério de Aprovação:**
- ✅ Taxa de aprovação: **100%** (nenhum teste falhando)
- ✅ Cobertura de RNs: **100%** (todas as RNs testadas)

**Tempo estimado:** 0.5-1h (execução + análise de falhas)

**Comando:**
```bash
cd D:\IC2\backend\IControlIT.API
dotnet test --filter "FullyQualifiedName~RFXXX" --logger "console;verbosity=detailed"
```

---

### 1.2. Teste E2E Smoke (1 spec) - **OBRIGATÓRIO**

**Cobertura:** Happy Path Completo

**O que testar:**
- ✅ **Login**: Autenticação com credenciais válidas
- ✅ **Navegação**: Acessar módulo do RF
- ✅ **CRUD Básico**:
  - Criar: Criar registro com dados **válidos**
  - Listar: Validar que registro aparece na listagem
  - Editar: Editar registro criado
  - Excluir: Excluir registro (se aplicável)
- ✅ **Validação de Integração**: Backend ↔ Frontend funcionando

**O que NÃO testar (deixar para PRD):**
- ❌ Validações de formulário (campos obrigatórios, formatos)
- ❌ Mensagens de erro detalhadas
- ❌ Edge cases de UI
- ❌ Estados vazios, loading, erro

**Critério de Aprovação:**
- ✅ Taxa de aprovação: **100%** (1 spec passando)

**Tempo estimado:** 1-2h (criar spec + executar + debug)

**Exemplo de Spec:**

```typescript
test.describe('TC-RFXXX-SMOKE: Happy Path Completo', () => {
  test.beforeEach(async ({ page }) => {
    await loginPage.navigate();
    const token = await loginPage.login(CREDENCIAIS.admin.email, CREDENCIAIS.admin.password);
    apiHelper = new APIHelper(token);
    await entityPage.navigate();
    await entityPage.closeAllOverlays();
  });

  test.afterEach(async ({ page }) => {
    await entityPage.closeAllOverlays();
    await loginPage.logout();
  });

  test('Deve criar, editar e excluir registro (happy path)', async ({ page }) => {
    // CRIAR
    await entityPage.criarRegistro({
      campo1: 'Valor válido',
      campo2: 'Outro valor válido'
    });
    await entityPage.validarRegistroNaListagem('Valor válido');

    // EDITAR
    await entityPage.editarRegistro('Valor válido', {
      campo1: 'Valor alterado'
    });
    await entityPage.validarRegistroNaListagem('Valor alterado');

    // EXCLUIR (se aplicável)
    await entityPage.excluirRegistro('Valor alterado');
    await entityPage.validarRegistroNaoNaListagem('Valor alterado');
  });
});
```

**Comando:**
```bash
cd D:\IC2\frontend\icontrolit-app
npx playwright test TC-RFXXX-SMOKE --headed
```

---

### 1.3. Testes de Segurança Críticos - **OBRIGATÓRIO**

**Cobertura:** 2 tipos críticos

#### 1.3.1. SQL Injection (Automatizado)

**O que testar:**
- ✅ Inputs de formulário não permitem SQL Injection
- ✅ Query params não permitem SQL Injection
- ✅ Payloads comuns: `' OR '1'='1`, `'; DROP TABLE --`, etc.

**Critério de Aprovação:**
- ✅ **NENHUM** payload resulta em erro de SQL
- ✅ **TODOS** retornam erro de validação (400/422)

**Tempo estimado:** 15-30 min (automatizado)

**Comando:**
```bash
python D:\IC2_Governanca\tools\security\sql-injection-test.py RFXXX
```

---

#### 1.3.2. Autenticação/Autorização (Manual)

**O que testar:**
- ✅ Usuário sem permissão **NÃO** acessa módulo
- ✅ Usuário não autenticado **NÃO** acessa módulo
- ✅ Multi-tenancy: Tenant A **NÃO** vê dados de Tenant B

**Critério de Aprovação:**
- ✅ **TODAS** as validações passam

**Tempo estimado:** 5-10 min (manual)

**Checklist:**
```yaml
autenticacao_autorizacao:
  - id: SEC-AUTH-01
    descricao: "Logout e tentar acessar módulo (deve redirecionar para /sign-in)"
    resultado: [ ] PASS [ ] FAIL

  - id: SEC-AUTH-02
    descricao: "Login com usuário sem permissão CAD.XXX.VISUALIZAR (deve exibir 403)"
    resultado: [ ] PASS [ ] FAIL

  - id: SEC-MULTI-01
    descricao: "Login com Tenant A, criar registro. Login com Tenant B, validar que NÃO vê registro de A"
    resultado: [ ] PASS [ ] FAIL
```

---

## 2. FLUXO DE EXECUÇÃO

### FASE 1: Pré-requisitos

**Validar:**
- ✅ Backend aprovado (validação backend = 100%)
- ✅ Frontend aprovado (validação frontend = 100%)
- ✅ Documentação completa (RF, UC, TC, MT)

**Bloqueio:**
- ❌ Se backend/frontend reprovados → **NÃO PROSSEGUIR**

---

### FASE 2: Testes Unitários

**Executar:**
```bash
cd D:\IC2\backend\IControlIT.API
dotnet test --filter "FullyQualifiedName~RFXXX"
```

**Critério:**
- ✅ Taxa de aprovação = 100%

**Se FALHAR:**
- ❌ **BLOQUEAR** execução
- ❌ Retornar para desenvolvimento
- ❌ Não prosseguir para Smoke Test

---

### FASE 3: Smoke Test E2E

**Executar:**
```bash
cd D:\IC2\frontend\icontrolit-app
npx playwright test TC-RFXXX-SMOKE --headed
```

**Critério:**
- ✅ Taxa de aprovação = 100% (1 spec passar)

**Se FALHAR:**
- ❌ **BLOQUEAR** execução
- ❌ Debug e corrigir
- ❌ Re-executar até 100%

---

### FASE 4: Segurança Crítica

**Executar:**
```bash
# SQL Injection (automatizado)
python D:\IC2_Governanca\tools\security\sql-injection-test.py RFXXX

# Autenticação (manual - 5 min)
# Seguir checklist 1.3.2
```

**Critério:**
- ✅ SQL Injection: 100% bloqueado
- ✅ Autenticação: 100% checklist PASS

**Se FALHAR:**
- ❌ **BLOQUEAR** subida para HOM
- ❌ Corrigir falha de segurança
- ❌ Re-executar

---

### FASE 5: Aprovação Final

**Critério de Aprovação (0% ou 100%):**
- ✅ Unitários: 100%
- ✅ Smoke E2E: 100%
- ✅ Segurança: 100%

**SE TODOS passarem:**
- ✅ **APROVADO PARA HOM**
- ✅ Atualizar STATUS.yaml
- ✅ Criar tag de versão
- ✅ Subir para ambiente de homologação

**SE QUALQUER critério FALHAR:**
- ❌ **REPROVADO**
- ❌ Retornar para desenvolvimento
- ❌ **NÃO** subir para HOM

---

## 3. RELATÓRIO OBRIGATÓRIO

**Ao final da execução, gerar:**

```yaml
# relatorios/testes/RELATORIO-MVS-RFXXX-[DATA].yaml

rf: RFXXX
data_execucao: "2026-01-11T14:30:00"
tempo_total: "2h 45min"
estrategia: "MVS (Mínimo Viável Seguro)"

resultados:
  unitarios:
    total: 45
    aprovados: 45
    reprovados: 0
    taxa_aprovacao: 100%
    tempo: "25 min"

  smoke_e2e:
    total: 1
    aprovados: 1
    reprovados: 0
    taxa_aprovacao: 100%
    tempo: "1h 30min"

  seguranca:
    sql_injection:
      payloads_testados: 20
      bloqueados: 20
      taxa_bloqueio: 100%
      tempo: "15 min"

    autenticacao:
      checklist_itens: 3
      pass: 3
      fail: 0
      taxa_aprovacao: 100%
      tempo: "5 min"

resultado_final: "APROVADO PARA HOM"
observacoes: |
  Testes MVS executados com sucesso.
  RF pronto para homologação.
  Testes completos (validações de formulário, edge cases) serão
  executados antes de subir para PRODUÇÃO.

proximos_passos:
  - Subir para ambiente de homologação
  - Cliente validar funcionalmente
  - Executar testes completos (execucao-completa.md) antes de PRD
```

---

## 4. GAPS CONHECIDOS (ACEITOS EM HOM)

**O que NÃO é coberto pelo MVS:**
- ❌ Validações detalhadas de formulário
- ❌ Mensagens de erro específicas
- ❌ Edge cases de UI (lista vazia, loading, erro)
- ❌ Performance (timeouts, loading times)
- ❌ Testes de regressão (outros RFs)
- ❌ Testes de acessibilidade
- ❌ Testes cross-browser

**Risco aceito:**
- ⚠️ Cliente pode encontrar bugs **não-críticos** em HOM
- ⚠️ Validações podem não funcionar perfeitamente
- ⚠️ UX pode ter problemas menores

**Mitigação:**
- ✅ Documentar gaps em `GAPS-CONHECIDOS-RFXXX.md`
- ✅ Cliente **ciente** dos gaps antes de homologar
- ✅ Testes completos **obrigatórios** antes de PRD

---

## 5. QUANDO ESCALAR PARA TESTES COMPLETOS

**EXECUTE testes completos (execucao-completa.md) quando:**
- ✅ RF passou em HOM e vai para **PRODUÇÃO**
- ✅ Cliente reportou bugs em HOM (validar se são críticos)
- ✅ RF é crítico (pagamentos, segurança, dados sensíveis)
- ✅ Há tempo disponível (>10h)

---

## 6. TEMPLATE DE SMOKE TEST

**Arquivo:** `frontend/icontrolit-app/e2e/specs/TC-RFXXX-SMOKE.spec.ts`

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { [Entity]Page } from '../pages/[entity].page';
import { APIHelper } from '../helpers/api.helper';
import { CREDENCIAIS_TESTE } from '../data/MT-RFXXX.data';

/**
 * TC-RFXXX-SMOKE: Happy Path Completo
 *
 * ESTRATÉGIA: MVS (Mínimo Viável Seguro)
 * COBERTURA: Happy path CRUD básico
 * TEMPO: ~5-10 min
 *
 * O QUE TESTA:
 * - Login + autenticação
 * - Navegação para módulo
 * - CRUD básico (criar → editar → excluir)
 * - Integração backend ↔ frontend
 *
 * O QUE NÃO TESTA (deixar para PRD):
 * - Validações de formulário
 * - Mensagens de erro
 * - Edge cases de UI
 *
 * @see CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md
 */

let loginPage: LoginPage;
let entityPage: [Entity]Page;
let apiHelper: APIHelper;

test.describe('TC-RFXXX-SMOKE: Happy Path Completo', () => {
  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    entityPage = new [Entity]Page(page);

    await loginPage.navigate();
    const token = await loginPage.login(
      CREDENCIAIS_TESTE.admin_teste.email,
      CREDENCIAIS_TESTE.admin_teste.password
    );
    apiHelper = new APIHelper(token);
    await entityPage.navigate();
    await entityPage.closeAllOverlays();
  });

  test.afterEach(async ({ page }) => {
    await entityPage.closeAllOverlays();
    await loginPage.logout();
  });

  test('Deve executar CRUD completo (criar → editar → excluir)', async ({ page }) => {
    // CRIAR
    await entityPage.criar[Entity]({
      campo1: 'Valor Teste MVS',
      campo2: 'Outro Valor'
    });

    // Validar na listagem
    await entityPage.validar[Entity]NaListagem('Valor Teste MVS');

    // EDITAR
    await entityPage.editar[Entity]('Valor Teste MVS', {
      campo1: 'Valor Alterado MVS'
    });

    // Validar alteração
    await entityPage.validar[Entity]NaListagem('Valor Alterado MVS');

    // EXCLUIR (se aplicável)
    await entityPage.excluir[Entity]('Valor Alterado MVS');

    // Validar exclusão
    await entityPage.validar[Entity]NaoNaListagem('Valor Alterado MVS');
  });
});
```

---

## 7. CRITÉRIO DE SUCESSO DO MVS

**Para considerar MVS bem-sucedido:**

### Métricas de Tempo
- ✅ Tempo total: **≤ 4 horas** por RF
- ✅ Tempo unitários: **≤ 1 hora**
- ✅ Tempo smoke E2E: **≤ 2 horas**
- ✅ Tempo segurança: **≤ 1 hora**

### Métricas de Qualidade
- ✅ Taxa aprovação unitários: **100%**
- ✅ Taxa aprovação smoke E2E: **100%**
- ✅ Taxa bloqueio SQL Injection: **100%**
- ✅ Taxa aprovação autenticação: **100%**

### Métricas de Negócio
- ✅ RF sobe para HOM em **1 dia** (vs 3 dias com testes completos)
- ✅ Cliente vê funcionalidade **funcionando** em HOM
- ✅ **≤ 2 bugs críticos** encontrados em HOM (meta: 0-1)

---

## 8. REFERÊNCIAS

- **execucao-completa.md**: Testes completos (usar antes de PRD)
- **CONTRATO-TESTES-E2E-ISOLADOS.md**: Padrão de testes E2E
- **CHECKLIST-TESTES-SMOKE.yaml**: Checklist de smoke test

---

## 9. REGRA DE NEGAÇÃO ZERO

**Este contrato é OBRIGATÓRIO para subir para HOM.**

**Se solicitação estiver fora do contrato:**
- ❌ **NEGAR** execução
- ❌ Explicar o motivo
- ❌ Solicitar ajuste formal

**Exceções (aprovação manual):**
- RF crítico → Executar execucao-completa.md
- Tempo > 10h disponível → Executar execucao-completa.md

---

**Versão:** 1.0
**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-11

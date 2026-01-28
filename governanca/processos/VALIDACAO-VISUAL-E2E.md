# PROCESSO: Validação Visual E2E

**Versão:** 1.0
**Data:** 2026-01-13
**Objetivo:** Definir processo completo de validação visual (alinhamento, layout, CSS) durante testes E2E
**Contexto:** Criado após identificação de GAP 4 (regressões visuais não detectadas nos testes atuais)

---

## 📋 SUMÁRIO EXECUTIVO

### Problema Identificado

**Testes funcionais NÃO detectam problemas visuais:**
- Elementos desalinhados (mas funcionais)
- Layout quebrado (mas elementos clicáveis)
- Elementos fora da tela (mas presentes no DOM)
- CSS incorreto (mas funcionalidade preservada)

**Exemplo Prático:**
```html
<!-- ✅ Teste funcional PASSA -->
<!-- ❌ Teste visual FALHARIA -->
<button
  data-test="btn-salvar"
  style="margin-left: 9999px;">  <!-- FORA DA TELA -->
  Salvar
</button>
```

### Solução

Adicionar **validação visual automatizada** usando **Playwright Snapshots** (built-in, gratuito).

**Resultado Esperado:**
- Baseline de screenshots criado para todas as páginas principais
- Comparação automática detecta diferenças visuais
- Regressões visuais bloqueiam deploy (opcional) ou geram alertas (padrão)

---

## 🎯 OBJETIVOS DO PROCESSO

1. **Criar baseline visual** de todas as páginas principais de um RF
2. **Comparar screenshots** atuais com baseline em cada execução de testes
3. **Detectar regressões visuais** (alinhamento, layout, CSS)
4. **Decidir ação** (corrigir CSS ou atualizar baseline)

---

## 📦 ESCOPO

### Aplicável A

- TODOS os RFs (independente de complexidade)
- Páginas com interface visual (não se aplica a APIs backend)
- Estados UI: normal, loading, vazio, erro

### Não Aplicável A

- Testes de backend (sem interface visual)
- Testes unitários (componentes isolados)
- Testes de API (sem renderização)

---

## 🔧 PRÉ-REQUISITOS

### 1. Playwright Instalado

```bash
cd frontend/icontrolit-app
npm install @playwright/test --save-dev
```

### 2. Configuração Playwright

**Arquivo:** `frontend/icontrolit-app/playwright.config.ts`

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  retries: 0,
  workers: 1,

  use: {
    baseURL: 'http://localhost:8080',
    screenshot: 'on',  // OBRIGATÓRIO para testes visuais
    viewport: { width: 1920, height: 1080 },  // Consistência de resolução
    trace: 'off',
    video: 'off',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

### 3. Estrutura de Diretórios

```bash
cd frontend/icontrolit-app

# Criar estrutura
mkdir -p e2e/visual
mkdir -p e2e/screenshots/baseline
mkdir -p e2e/screenshots/actual
```

### 4. Scripts package.json

**Arquivo:** `frontend/icontrolit-app/package.json`

```json
{
  "scripts": {
    "e2e:visual:baseline": "playwright test e2e/visual/ --update-snapshots",
    "e2e:visual": "playwright test e2e/visual/",
    "e2e:visual:update": "playwright test e2e/visual/ --update-snapshots"
  }
}
```

---

## 📝 PROCESSO COMPLETO (3 FASES)

## FASE 1: CRIAÇÃO DE BASELINE (Primeira Execução)

### Passo 1.1: Criar Teste Visual

**Arquivo:** `frontend/icontrolit-app/e2e/visual/RFXXX-visual.spec.ts`

```typescript
import { test, expect } from '@playwright/test';
import { CREDENCIAIS_TESTE, FRONTEND_URLS } from '../data/MT-RFXXX.data';

test.describe('RF006 - Validação Visual', () => {

  test.beforeEach(async ({ page }) => {
    // Login
    await page.goto('/login');
    await page.fill('[data-test="input-email"]', CREDENCIAIS_TESTE.admin_teste.email);
    await page.fill('[data-test="input-password"]', CREDENCIAIS_TESTE.admin_teste.password);
    await page.click('[data-test="btn-login"]');
    await page.waitForURL('/dashboard');
  });

  test('Deve exibir lista de clientes com layout correto (estado normal)', async ({ page }) => {
    await page.goto(FRONTEND_URLS.lista_clientes);

    // Aguardar carregamento completo
    await page.waitForSelector('[data-test="clientes-list"]', { state: 'visible' });
    await page.waitForLoadState('networkidle');

    // Capturar screenshot e comparar com baseline
    await expect(page).toHaveScreenshot('RF006-lista-clientes-normal.png', {
      maxDiffPixels: 100,  // Tolerância de 100 pixels diferentes
      fullPage: true,       // Screenshot de página inteira
    });
  });

  test('Deve exibir lista de clientes com layout correto (estado vazio)', async ({ page }) => {
    // Simular banco vazio (resetar dados de teste)
    // ... (implementação específica do RF)

    await page.goto(FRONTEND_URLS.lista_clientes);
    await page.waitForSelector('[data-test="empty-state"]', { state: 'visible' });

    await expect(page).toHaveScreenshot('RF006-lista-clientes-vazio.png', {
      maxDiffPixels: 100,
      fullPage: true,
    });
  });

  test('Deve exibir lista de clientes com layout correto (estado loading)', async ({ page }) => {
    // Interceptar request para simular loading longo
    await page.route('**/api/clientes**', async (route) => {
      await new Promise(resolve => setTimeout(resolve, 5000));  // Delay 5s
      await route.continue();
    });

    await page.goto(FRONTEND_URLS.lista_clientes);
    await page.waitForSelector('[data-test="loading-spinner"]', { state: 'visible' });

    await expect(page).toHaveScreenshot('RF006-lista-clientes-loading.png', {
      maxDiffPixels: 100,
      fullPage: true,
    });
  });

  test('Deve exibir formulário de criação com layout correto', async ({ page }) => {
    await page.goto(FRONTEND_URLS.lista_clientes);
    await page.click('[data-test="btn-novo-cliente"]');

    await page.waitForSelector('[data-test="RF006-form"]', { state: 'visible' });

    await expect(page).toHaveScreenshot('RF006-form-criar-cliente.png', {
      maxDiffPixels: 100,
      fullPage: true,
    });
  });

  test('Deve exibir validações de formulário com layout correto', async ({ page }) => {
    await page.goto(FRONTEND_URLS.lista_clientes);
    await page.click('[data-test="btn-novo-cliente"]');

    // Submeter formulário vazio para exibir erros
    await page.click('[data-test="btn-salvar"]');

    await page.waitForSelector('[data-test="RF006-input-nome-error"]', { state: 'visible' });

    await expect(page).toHaveScreenshot('RF006-form-validacoes.png', {
      maxDiffPixels: 100,
      fullPage: true,
    });
  });

});
```

---

### Passo 1.2: Executar Criação de Baseline

```bash
cd frontend/icontrolit-app

# Criar baseline (primeira execução)
npm run e2e:visual:baseline RFXXX
```

**Output Esperado:**
```
Running 5 tests using 1 worker

  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado normal) (2.3s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado vazio) (1.8s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado loading) (5.1s)
  ✓ RF006 - Validação Visual › Deve exibir formulário de criação com layout correto (1.5s)
  ✓ RF006 - Validação Visual › Deve exibir validações de formulário com layout correto (1.2s)

  5 passed (11.9s)

Screenshots baseline criados em: e2e/screenshots/baseline/
```

---

### Passo 1.3: Validar Baseline Criado

```bash
# Verificar screenshots criados
ls e2e/screenshots/baseline/RFXXX-visual.spec.ts-chromium/
```

**Arquivos Esperados:**
```
RF006-lista-clientes-normal.png
RF006-lista-clientes-vazio.png
RF006-lista-clientes-loading.png
RF006-form-criar-cliente.png
RF006-form-validacoes.png
```

---

### Passo 1.4: Versionar Baseline no Git

```bash
# Adicionar baseline ao git
git add e2e/screenshots/baseline/
git commit -m "feat(testes): adicionar baseline visual RF006

- Screenshots baseline criados para 5 estados
- Lista: normal, vazio, loading
- Formulário: criar, validações

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## FASE 2: EXECUÇÃO DE TESTES VISUAIS (Execuções Subsequentes)

### Passo 2.1: Executar Testes Visuais

```bash
cd frontend/icontrolit-app

# Executar testes visuais (comparação com baseline)
npm run e2e:visual RFXXX
```

**Output Esperado (SEM regressões):**
```
Running 5 tests using 1 worker

  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado normal) (2.3s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado vazio) (1.8s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado loading) (5.1s)
  ✓ RF006 - Validação Visual › Deve exibir formulário de criação com layout correto (1.5s)
  ✓ RF006 - Validação Visual › Deve exibir validações de formulário com layout correto (1.2s)

  5 passed (11.9s)
```

**Output Esperado (COM regressões):**
```
Running 5 tests using 1 worker

  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado normal) (2.3s)
  ✗ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado vazio) (1.8s)

    Error: Screenshot comparison failed:

    1250 pixels (ratio 0.03 of all image pixels) are different.

    Expected: e2e/screenshots/baseline/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio.png
    Received: e2e/screenshots/actual/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio-actual.png
    Diff:     e2e/screenshots/diff/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio-diff.png

  1 failed
  4 passed (11.9s)
```

---

### Passo 2.2: Analisar Falhas Visuais

**Se testes visuais FALHAREM:**

1. **Abrir imagens de diff:**
   ```bash
   # Diff mostra pixels diferentes destacados em vermelho
   open e2e/screenshots/diff/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio-diff.png
   ```

2. **Comparar baseline vs actual:**
   ```bash
   # Baseline (esperado)
   open e2e/screenshots/baseline/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio.png

   # Actual (atual)
   open e2e/screenshots/actual/RFXXX-visual.spec.ts-chromium/RF006-lista-clientes-vazio-actual.png
   ```

3. **Decidir ação:**
   - **Regressão visual (bug):** Corrigir CSS → Re-executar testes até PASS
   - **Mudança intencional:** Atualizar baseline (Fase 3)

---

## FASE 3: ATUALIZAÇÃO DE BASELINE (Mudanças Intencionais)

### Quando Atualizar Baseline

**Atualizar baseline SOMENTE quando:**
- Mudança visual foi intencional (novo design, ajuste de layout)
- Mudança foi revisada e aprovada (não é regressão)
- Mudança foi documentada (commit message explica o porquê)

**NÃO atualizar baseline se:**
- Mudança foi acidental (bug de CSS)
- Mudança não foi revisada
- Não sabe explicar o porquê da diferença

---

### Passo 3.1: Atualizar Baseline

```bash
cd frontend/icontrolit-app

# Atualizar baseline com screenshots atuais
npm run e2e:visual:update RFXXX
```

**Output Esperado:**
```
Running 5 tests using 1 worker

  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado normal) (2.3s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado vazio) (1.8s)
  ✓ RF006 - Validação Visual › Deve exibir lista de clientes com layout correto (estado loading) (5.1s)
  ✓ RF006 - Validação Visual › Deve exibir formulário de criação com layout correto (1.5s)
  ✓ RF006 - Validação Visual › Deve exibir validações de formulário com layout correto (1.2s)

  5 passed (11.9s)

Baseline atualizado em: e2e/screenshots/baseline/
```

---

### Passo 3.2: Versionar Baseline Atualizado no Git

```bash
# Adicionar baseline atualizado ao git
git add e2e/screenshots/baseline/

git commit -m "refactor(testes): atualizar baseline visual RF006

MUDANÇA INTENCIONAL:
- Ajustado alinhamento de botões (margem 16px → 24px)
- Atualizado estado vazio (nova ilustração)
- Melhorado responsividade (breakpoint 768px)

JUSTIFICATIVA:
- Alinhamento conforme novo guia de design v2.0
- Aprovado por UX/UI (ticket #1234)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

---

## 🚨 BLOQUEIOS E DECISÕES

### Bloqueio 1: Baseline Ausente

**Condição:** `e2e/screenshots/baseline/RFXXX/` não existe

**Ação:**
- ❌ BLOQUEAR testes visuais
- ✅ PROSSEGUIR com testes funcionais
- ⚠️ ALERTAR: "Baseline visual ausente, testes visuais ignorados"

**Solução:**
```bash
npm run e2e:visual:baseline RFXXX
```

---

### Bloqueio 2: Playwright Não Configurado para Screenshots

**Condição:** `screenshot: 'on'` ausente em `playwright.config.ts`

**Ação:**
- ❌ BLOQUEAR testes visuais
- ✅ PROSSEGUIR com testes funcionais
- ⚠️ ALERTAR: "Playwright não configurado para screenshots"

**Solução:**
```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: 'on',  // Adicionar esta linha
  },
});
```

---

### Bloqueio 3: Diferenças Visuais Detectadas

**Condição:** Testes visuais falham (diff > maxDiffPixels)

**Ação (modo informativo - PADRÃO):**
- ⚠️ ALERTAR: "Regressões visuais detectadas (X pixels diferentes)"
- ✅ PROSSEGUIR com deploy (não bloqueante)
- 📊 Gerar relatório de diff

**Ação (modo rigoroso - OPCIONAL):**
- ❌ BLOQUEAR deploy
- ❌ Exigir correção ou atualização de baseline antes de prosseguir

**Configuração (modo rigoroso):**
```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    screenshot: {
      mode: 'only-on-failure',
      maxDiffPixelRatio: 0.001,  // 0.1% de diferença permitida
    },
  },
});
```

---

## 📊 MÉTRICAS DE SUCESSO

| Métrica | Baseline (Sem Validação Visual) | Meta (Com Validação Visual) |
|---------|--------------------------------|----------------------------|
| Regressões visuais detectadas | 0% (não detectadas) | 100% (detectadas) |
| Falsos positivos | N/A | < 5% (tolerância de 100 pixels) |
| Tempo de execução | +0s (não executado) | +10-15s por RF (5 screenshots) |
| Cobertura visual | 0% | 100% (todas páginas principais) |

---

## 🔍 TROUBLESHOOTING

### Problema 1: Muitos Falsos Positivos

**Sintoma:** Testes visuais falham frequentemente sem mudanças reais

**Causas:**
- `maxDiffPixels` muito baixo (ex: 10)
- Fontes não carregadas consistentemente
- Animações não desabilitadas
- Viewport inconsistente

**Solução:**
```typescript
// Aumentar tolerância
await expect(page).toHaveScreenshot('screenshot.png', {
  maxDiffPixels: 200,  // Era 100, aumentar para 200
});

// Desabilitar animações
await page.addStyleTag({
  content: '*, *::before, *::after { animation-duration: 0s !important; transition: none !important; }',
});

// Garantir viewport consistente
await page.setViewportSize({ width: 1920, height: 1080 });
```

---

### Problema 2: Screenshots Sempre Diferentes (Conteúdo Dinâmico)

**Sintoma:** Datas, horários, IDs dinâmicos mudam entre execuções

**Solução:**
```typescript
// Mascarar elementos dinâmicos
await expect(page).toHaveScreenshot('screenshot.png', {
  mask: [
    page.locator('[data-test="timestamp"]'),      // Data/hora
    page.locator('[data-test="record-id"]'),      // IDs
    page.locator('[data-test="random-token"]'),   // Tokens
  ],
  maxDiffPixels: 100,
});
```

---

### Problema 3: Testes Visuais Lentos

**Sintoma:** Execução de testes visuais demora muito (>30s por RF)

**Solução:**
```typescript
// Reduzir qualidade de screenshot (menor tamanho de arquivo)
await expect(page).toHaveScreenshot('screenshot.png', {
  maxDiffPixels: 100,
  scale: 'css',  // 'device' é mais lento
});

// Capturar apenas área visível (não fullPage)
await expect(page).toHaveScreenshot('screenshot.png', {
  maxDiffPixels: 100,
  fullPage: false,  // Era true
});
```

---

## 📚 DOCUMENTAÇÃO DE APOIO

| Documento | Propósito |
|-----------|-----------|
| `CLAUDE.md` | Seção 18.8 - Validação Visual (visão geral) |
| `checklists/testes/CHECKLIST-IMPLEMENTACAO-E2E.md` | Seção 2.5 - Checklist de Validação Visual |
| `checklists/testes/pre-execucao.yaml` | Seção validacao_visual - Validações pré-execução |
| `contracts/testes/execucao-completa.md` | Contrato de execução de testes (incluindo visuais) |

---

## 🔗 REFERÊNCIAS EXTERNAS

- **Playwright Visual Comparisons:** https://playwright.dev/docs/test-snapshots
- **Chromatic (ferramenta externa):** https://www.chromatic.com/
- **Percy (ferramenta externa):** https://percy.io/
- **Visual Regression Testing Best Practices:** https://github.com/mojoaxel/awesome-regression-testing

---

## 📝 CHANGELOG

### v1.0 (2026-01-13)
- Criação do processo de validação visual E2E
- 3 fases documentadas: Criação de Baseline, Execução, Atualização
- 5 testes visuais de exemplo (lista normal/vazio/loading, form criar/validações)
- Bloqueios definidos (baseline ausente, Playwright não configurado, diferenças detectadas)
- Modo informativo (padrão) vs modo rigoroso (opcional)
- Troubleshooting: falsos positivos, conteúdo dinâmico, performance
- Métricas de sucesso e referências externas

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-13
**Versão:** 1.0

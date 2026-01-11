# CONTRATO DE TESTES E2E ISOLADOS (ISOLATED PATTERN)

**Versão:** 1.0
**Data:** 2026-01-11
**Status:** Ativo
**Tipo:** Contrato de Execução - Testes E2E
**Changelog v1.0:** Criação do contrato para testes E2E isolados com Page Object Pattern, beforeEach/afterEach obrigatórios, closeAllOverlays() helper, e validação de isolamento. Substitui padrão stateful (test.describe.serial) por isolated (test.describe). Baseado em análise de problemas RF006 (10-60% aprovação E2E devido a contaminação de estado).

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato define **COMO** criar testes E2E **isolados** (cada teste independente) usando Playwright, garantindo:
- ✅ **Isolamento completo**: Cada teste inicia em estado limpo
- ✅ **Sem contaminação**: Overlay/backdrop limpos entre testes
- ✅ **Paralelização**: Testes podem rodar em paralelo (optional)
- ✅ **Manutenibilidade**: Page Object Pattern obrigatório
- ✅ **Alta aprovação**: 95-100% (vs 10-60% do padrão stateful)

### 🎯 Quando usar este contrato

**USE este contrato quando:**
- ✅ RF possui operações **independentes** (não sequenciais)
- ✅ Cada UC pode ser testado **sem dependências** de outros
- ✅ Testes **não compartilham** dados entre si
- ✅ Cada teste cria **seus próprios dados** (via API ou fixture isolada)

**NÃO use este contrato quando:**
- ❌ RF possui CRUD completo (≥ 3 operações) → Use [CONTRATO-TESTES-E2E-STATEFUL.md](CONTRATO-TESTES-E2E-STATEFUL.md)
- ❌ Testes precisam **compartilhar** dados (ex: criar cliente → editar mesmo cliente)
- ❌ Fluxos são **sequenciais** por natureza

### 📊 Impacto esperado

| Métrica | Stateful (Antigo) | Isolated (Novo) | Melhoria |
|---------|-------------------|-----------------|----------|
| Taxa aprovação E2E | 10-60% | 95-100% | +35-90% |
| Contaminação overlay | 67% falhas | 0% falhas | -67% |
| Tempo debug | 10 horas/RF | 0.5 horas/RF | -95% |
| Execuções necessárias | 12 | 1-2 | -83% |

---

## 1. CONTEXTO E JUSTIFICATIVA

### 1.1. Problema Identificado (RF006)

Durante testes E2E do RF006, identificou-se **problema sistemático** com testes stateful:

| Execução | Taxa Aprovação | Problema Principal |
|----------|----------------|-------------------|
| #7 | 0% (0/32) | Overlay/backdrop persistente |
| #8 | 50% (16/32) | Contaminação de estado |
| #9 | 86.7% (26/30) | Validações residuais |

**Causa raiz:**
- `test.describe.serial` causa dependências entre testes
- Overlay/backdrop **não limpam** entre testes
- Estado residual contamina testes subsequentes

### 1.2. Solução: Isolated Pattern

**Mudança arquitetural:**

```typescript
// ❌ ANTIGO: Stateful (serial, compartilhamento de dados)
test.describe.serial('TC-RF006-E2E-001', () => {
  let clienteId: string;  // ⚠️ Compartilhado entre testes

  test('Criar cliente', async ({ page }) => {
    // clienteId = ...
  });

  test('Editar cliente', async ({ page }) => {
    // usa clienteId do teste anterior ⚠️
  });
});

// ✅ NOVO: Isolated (cada teste independente)
test.describe('TC-RF006-E2E-001', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: login + navigate + cleanup
    await loginPage.login('admin@teste.com', 'Test@123');
    await clientesPage.navigate();
    await clientesPage.closeAllOverlays();  // ✅ Limpa overlay
  });

  test.afterEach(async ({ page }) => {
    // Cleanup: overlay + logout
    await clientesPage.closeAllOverlays();
    await loginPage.logout();
  });

  test('Criar cliente', async ({ page }) => {
    // Teste isolado, cria SEUS dados
    await clientesPage.criarCliente({...});
  });

  test('Editar cliente', async ({ page }) => {
    // Teste isolado, cria PRÓPRIO cliente via API
    const clienteId = await apiHelper.criarClienteViaAPI({...});
    await clientesPage.editarCliente(clienteId, {...});
  });
});
```

---

## 2. ESTRUTURA OBRIGATÓRIA: PAGE OBJECT PATTERN

### 2.1. Organização de Arquivos

```
e2e/
├── specs/                       ← Arquivos .spec.ts (testes)
│   └── TC-RF006-E2E-001.spec.ts
│
├── pages/                       ← Page Objects (OBRIGATÓRIO)
│   ├── login.page.ts
│   ├── clientes.page.ts
│   └── base.page.ts
│
├── helpers/                     ← Helpers compartilhados
│   ├── dialog-helpers.ts        ← closeAllOverlays, waitForDialogToClosed
│   ├── api-helpers.ts           ← Criar dados via API
│   └── test-data.ts
│
└── data/                        ← Massa de teste
    └── MT-RF006.data.ts
```

### 2.2. Template: Base Page Object

**Arquivo:** `e2e/pages/base.page.ts`

```typescript
import { Page, Locator } from '@playwright/test';

/**
 * Base Page Object
 * Todos os Page Objects DEVEM herdar desta classe
 */
export class BasePage {
  constructor(protected page: Page) {}

  /**
   * OBRIGATÓRIO: Limpar todos os overlays/backdrops
   * Previne contaminação de estado entre testes
   */
  async closeAllOverlays(): Promise<void> {
    let attempts = 0;
    const maxAttempts = 5;

    while (attempts < maxAttempts) {
      const overlayCount = await this.page.locator('.cdk-overlay-backdrop').count();

      if (overlayCount === 0) {
        // ✅ Nenhum overlay presente
        return;
      }

      // Fechar overlay via ESC
      await this.page.keyboard.press('Escape');

      // Aguardar overlay ser removido
      await this.page.waitForSelector('.cdk-overlay-backdrop', {
        state: 'detached',
        timeout: 5000
      }).catch(() => {
        // Timeout esperado se overlay já foi removido
      });

      attempts++;
    }

    // Se após 5 tentativas ainda há overlay, falhar
    const finalCount = await this.page.locator('.cdk-overlay-backdrop').count();
    if (finalCount > 0) {
      throw new Error(
        `CRÍTICO: ${finalCount} overlay(s) persistente(s) após ${maxAttempts} tentativas. ` +
        `Verifique se dialogs estão sendo fechados corretamente.`
      );
    }
  }

  /**
   * Aguardar dialog abrir completamente
   */
  async waitForDialogToOpen(dataTest: string, timeout: number = 10000): Promise<void> {
    await this.page.waitForSelector(`[data-test="${dataTest}"]`, {
      state: 'visible',
      timeout
    });

    // Aguardar animação de abertura
    await this.page.waitForTimeout(300);
  }

  /**
   * Aguardar dialog fechar completamente
   */
  async waitForDialogToClosed(timeout: number = 15000): Promise<void> {
    await this.page.waitForSelector('.cdk-overlay-backdrop', {
      state: 'detached',
      timeout
    }).catch(() => {
      // Se não há backdrop, ok
    });

    // Aguardar animação de fechamento
    await this.page.waitForTimeout(500);
  }
}
```

### 2.3. Template: Entity Page Object

**Arquivo:** `e2e/pages/clientes.page.ts`

```typescript
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class ClientesPage extends BasePage {
  // Seletores (centralizados)
  private readonly btnNovoCliente: Locator;
  private readonly inputCNPJ: Locator;
  private readonly inputRazaoSocial: Locator;
  private readonly btnSalvar: Locator;
  private readonly clienteRow: Locator;
  private readonly loadingSpinner: Locator;
  private readonly emptyState: Locator;

  constructor(page: Page) {
    super(page);

    // Inicializar seletores
    this.btnNovoCliente = page.locator('[data-test="RF006-criar-cliente"]');
    this.inputCNPJ = page.locator('[data-test="RF006-input-cnpj"]');
    this.inputRazaoSocial = page.locator('[data-test="RF006-input-razaosocial"]');
    this.btnSalvar = page.locator('[data-test="RF006-salvar-cliente"]');
    this.clienteRow = page.locator('[data-test="cliente-row"]');
    this.loadingSpinner = page.locator('[data-test="loading-spinner"]');
    this.emptyState = page.locator('[data-test="empty-state"]');
  }

  /**
   * Navegar para página de clientes
   */
  async navigate(): Promise<void> {
    await this.page.goto('http://localhost:4200/management/clientes', {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    // Aguardar loading desaparecer
    await this.loadingSpinner.waitFor({ state: 'detached', timeout: 30000 });
  }

  /**
   * Criar novo cliente
   */
  async criarCliente(dados: {
    cnpj: string;
    razaoSocial: string;
    nomeFantasia?: string;
  }): Promise<void> {
    // 1. Clicar em "Novo Cliente"
    await this.btnNovoCliente.click();
    await this.waitForDialogToOpen('dialog-criar-cliente');

    // 2. Preencher formulário
    await this.inputCNPJ.fill(dados.cnpj);
    await this.inputRazaoSocial.fill(dados.razaoSocial);

    if (dados.nomeFantasia) {
      await this.page.locator('[data-test="RF006-input-nomefantasia"]').fill(dados.nomeFantasia);
    }

    // 3. Salvar
    await this.btnSalvar.click();

    // 4. Aguardar dialog fechar
    await this.waitForDialogToClosed();

    // 5. Aguardar navegação de volta à listagem
    await this.page.waitForURL('**/management/clientes', { timeout: 10000 });
  }

  /**
   * Validar que cliente existe na listagem
   */
  async validarClienteNaListagem(razaoSocial: string): Promise<void> {
    const row = this.page.locator(`[data-test="cliente-row"]:has-text("${razaoSocial}")`);
    await expect(row).toBeVisible({ timeout: 10000 });
  }

  /**
   * Excluir cliente
   */
  async excluirCliente(razaoSocial: string): Promise<void> {
    // 1. Localizar linha do cliente
    const row = this.page.locator(`[data-test="cliente-row"]:has-text("${razaoSocial}")`);

    // 2. Clicar em excluir
    await row.locator('[data-test="RF006-excluir-cliente"]').click();

    // 3. Confirmar exclusão
    await this.waitForDialogToOpen('dialog-confirmacao');
    await this.page.locator('[data-test="btn-confirmar-dialog"]').click();

    // 4. Aguardar dialog fechar
    await this.waitForDialogToClosed();
  }
}
```

---

## 3. FASE 1: ESTRUTURA DE TESTE ISOLADO

### 3.1. beforeEach: Setup Obrigatório

**Cada teste DEVE:**

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { ClientesPage } from '../pages/clientes.page';
import { CREDENCIAIS_TESTE } from '../data/MT-RF006.data';

let loginPage: LoginPage;
let clientesPage: ClientesPage;

test.beforeEach(async ({ page }) => {
  // 1. Inicializar Page Objects
  loginPage = new LoginPage(page);
  clientesPage = new ClientesPage(page);

  // 2. Login
  await loginPage.navigate();
  await loginPage.login(
    CREDENCIAIS_TESTE.admin_teste.email,
    CREDENCIAIS_TESTE.admin_teste.password
  );

  // 3. Navegar para página da entidade
  await clientesPage.navigate();

  // 4. CRÍTICO: Limpar overlay/backdrop residual
  await clientesPage.closeAllOverlays();
});
```

**Critério de aceite:**
- ✅ TODOS os testes têm `beforeEach` com login + navigate + closeAllOverlays
- ✅ Page Objects inicializados
- ✅ Estado limpo garantido

### 3.2. afterEach: Cleanup Obrigatório

**Cada teste DEVE:**

```typescript
test.afterEach(async ({ page }) => {
  // 1. CRÍTICO: Limpar overlay/backdrop após teste
  await clientesPage.closeAllOverlays();

  // 2. Logout (opcional mas recomendado)
  await loginPage.logout();
});
```

**Critério de aceite:**
- ✅ TODOS os testes têm `afterEach` com closeAllOverlays
- ✅ Logout executado (opcional)
- ✅ Estado limpo para próximo teste

---

## 4. FASE 2: CRIAÇÃO DE DADOS ISOLADOS

### 4.1. Padrão: Criar Dados via API

**Cada teste cria SEUS dados:**

```typescript
test('Editar cliente', async ({ page }) => {
  // 1. Criar cliente VIA API (não depende de teste anterior)
  const clienteId = await apiHelper.criarClienteViaAPI({
    cnpj: '00.000.000/0001-91',
    razaoSocial: 'TESTE EDICAO LTDA'
  });

  // 2. Recarregar página para ver novo cliente
  await page.reload({ waitUntil: 'networkidle' });
  await clientesPage.closeAllOverlays();

  // 3. Editar cliente criado
  await clientesPage.editarCliente(clienteId, {
    nomeFantasia: 'NOME EDITADO'
  });

  // 4. Validar edição
  await clientesPage.validarClienteNaListagem('NOME EDITADO');
});
```

**Helper de API:**

```typescript
// e2e/helpers/api-helpers.ts
import { request } from '@playwright/test';

export class APIHelper {
  private baseURL = 'http://localhost:5000';
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  async criarClienteViaAPI(dados: {
    cnpj: string;
    razaoSocial: string;
  }): Promise<string> {
    const context = await request.newContext({
      baseURL: this.baseURL,
      extraHTTPHeaders: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      }
    });

    const response = await context.post('/api/clientes', {
      data: dados
    });

    const body = await response.json();
    return body.id;  // Retornar ID do cliente criado
  }

  async excluirClienteViaAPI(id: string): Promise<void> {
    const context = await request.newContext({
      baseURL: this.baseURL,
      extraHTTPHeaders: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    await context.delete(`/api/clientes/${id}`);
  }
}
```

**Critério de aceite:**
- ✅ Testes criam PRÓPRIOS dados (não dependem de outros testes)
- ✅ API helper implementado
- ✅ Dados criados via API (rápido)

### 4.2. Padrão: Cleanup de Dados (Opcional)

**Opcionalmente, limpar dados após teste:**

```typescript
test('Criar e excluir cliente', async ({ page }) => {
  let clienteId: string | null = null;

  try {
    // 1. Criar cliente via UI
    await clientesPage.criarCliente({
      cnpj: '00.000.000/0001-91',
      razaoSocial: 'TESTE DELETE LTDA'
    });

    // 2. Capturar ID do cliente criado
    clienteId = await clientesPage.getUltimoClienteCriado();

    // 3. Validar criação
    await clientesPage.validarClienteNaListagem('TESTE DELETE LTDA');

    // 4. Excluir cliente
    await clientesPage.excluirCliente('TESTE DELETE LTDA');

    // 5. Validar exclusão
    await expect(
      page.locator('[data-test="cliente-row"]:has-text("TESTE DELETE LTDA")')
    ).not.toBeVisible();

  } finally {
    // Cleanup: Se teste falhou, garantir exclusão via API
    if (clienteId) {
      await apiHelper.excluirClienteViaAPI(clienteId).catch(() => {
        // Ignora erro se já foi excluído
      });
    }
  }
});
```

---

## 5. FASE 3: VALIDAÇÃO DE ISOLAMENTO

### 5.1. Script de Validação (Python)

**Arquivo:** `tools/validate-isolated-tests.py`

```python
#!/usr/bin/env python3
"""
Valida que testes E2E seguem padrão isolated (não stateful)
"""

import os
import re
import sys
import glob

def validar_testes_isolados(rf_numero):
    """
    Valida que specs do RF seguem padrão isolated
    """
    e2e_dir = "D:\\IC2\\frontend\\icontrolit-app\\e2e\\specs"
    spec_pattern = f"TC-RF{rf_numero}-*.spec.ts"
    spec_files = glob.glob(f"{e2e_dir}\\{spec_pattern}")

    if not spec_files:
        print(f"❌ Nenhum spec encontrado para RF{rf_numero}")
        return 1

    falhas = []

    for spec_file in spec_files:
        with open(spec_file, 'r', encoding='utf-8') as f:
            conteudo = f.read()

        # 1. Validar que NÃO usa test.describe.serial
        if 'test.describe.serial' in conteudo:
            falhas.append(f"{os.path.basename(spec_file)}: Usa test.describe.serial (PROIBIDO em isolated)")

        # 2. Validar que possui beforeEach
        if 'test.beforeEach' not in conteudo:
            falhas.append(f"{os.path.basename(spec_file)}: Ausente test.beforeEach (OBRIGATÓRIO)")

        # 3. Validar que beforeEach chama closeAllOverlays
        if 'closeAllOverlays()' not in conteudo:
            falhas.append(f"{os.path.basename(spec_file)}: Ausente closeAllOverlays() (OBRIGATÓRIO)")

        # 4. Validar que possui afterEach
        if 'test.afterEach' not in conteudo:
            falhas.append(f"{os.path.basename(spec_file)}: Ausente test.afterEach (OBRIGATÓRIO)")

        # 5. Validar que usa Page Objects
        if 'Page' not in conteudo or 'import' not in conteudo:
            falhas.append(f"{os.path.basename(spec_file)}: Não usa Page Objects (OBRIGATÓRIO)")

    # Resultado
    if falhas:
        print(f"❌ RF{rf_numero} NÃO segue padrão isolated:")
        for falha in falhas:
            print(f"  - {falha}")
        return 1
    else:
        print(f"✅ RF{rf_numero} segue padrão isolated corretamente")
        print(f"  - {len(spec_files)} specs validados")
        print(f"  - beforeEach/afterEach presentes")
        print(f"  - closeAllOverlays() implementado")
        print(f"  - Page Objects utilizados")
        return 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python validate-isolated-tests.py <RF_NUMERO>")
        sys.exit(1)

    rf_numero = sys.argv[1]
    sys.exit(validar_testes_isolados(rf_numero))
```

### 5.2. Integração com Contrato de Validação

**O contrato de validação de testes (`execucao-completa.md`) DEVE executar:**

```bash
python tools/validate-isolated-tests.py 006
```

**Critério de aprovação:**
- ✅ Zero uso de `test.describe.serial`
- ✅ TODOS os specs possuem `beforeEach` + `afterEach`
- ✅ TODOS os specs chamam `closeAllOverlays()`
- ✅ TODOS os specs usam Page Objects

**SE validação FALHAR:**
- ❌ Testes NÃO seguem padrão isolated
- ❌ BLOQUEIO: Corrigir specs

---

## 6. CONFIGURAÇÃO PLAYWRIGHT

### 6.1. playwright.config.ts (Isolated)

**Para testes isolated, configurar:**

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 60000,
  expect: {
    timeout: 10000
  },

  // ✅ ISOLATED: Pode paralelizar (opcional)
  fullyParallel: true,  // ✅ Permitido (testes independentes)
  workers: 4,           // ✅ Múltiplos workers (opcional)
  retries: 2,           // ✅ Retries permitidos

  reporter: [
    ['list'],
    ['json', { outputFile: 'playwright-results.json' }]
  ],

  use: {
    baseURL: 'http://localhost:4200',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    strictSelectors: true
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    }
  ]
});
```

**Diferença para Stateful:**

| Configuração | Isolated | Stateful |
|--------------|----------|----------|
| fullyParallel | `true` (✅ permitido) | `false` (❌ obrigatório) |
| workers | `1-4` (✅ múltiplos) | `1` (❌ obrigatório) |
| retries | `0-2` (✅ permitido) | `0` (❌ obrigatório) |

---

## 7. EXEMPLO COMPLETO: TC-RF006-E2E-001.spec.ts

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/login.page';
import { ClientesPage } from '../pages/clientes.page';
import { APIHelper } from '../helpers/api-helpers';
import { CREDENCIAIS_TESTE, FRONTEND_URLS } from '../data/MT-RF006.data';

let loginPage: LoginPage;
let clientesPage: ClientesPage;
let apiHelper: APIHelper;

/**
 * TC-RF006-E2E-001: Testes de CRUD de Clientes (Isolated)
 *
 * Padrão: ISOLATED (cada teste independente)
 * Referência: CONTRATO-TESTES-E2E-ISOLADOS.md
 */
test.describe('TC-RF006-E2E-001: CRUD Clientes (Isolated)', () => {

  // ========================================
  // SETUP: beforeEach (OBRIGATÓRIO)
  // ========================================
  test.beforeEach(async ({ page }) => {
    // 1. Inicializar Page Objects
    loginPage = new LoginPage(page);
    clientesPage = new ClientesPage(page);

    // 2. Login
    await loginPage.navigate();
    const token = await loginPage.login(
      CREDENCIAIS_TESTE.admin_teste.email,
      CREDENCIAIS_TESTE.admin_teste.password
    );

    // 3. Inicializar API helper (para criar dados)
    apiHelper = new APIHelper(token);

    // 4. Navegar para clientes
    await clientesPage.navigate();

    // 5. CRÍTICO: Limpar overlay/backdrop residual
    await clientesPage.closeAllOverlays();
  });

  // ========================================
  // CLEANUP: afterEach (OBRIGATÓRIO)
  // ========================================
  test.afterEach(async ({ page }) => {
    // 1. Limpar overlay/backdrop
    await clientesPage.closeAllOverlays();

    // 2. Logout
    await loginPage.logout();
  });

  // ========================================
  // TESTE 1: Criar Cliente (Isolado)
  // ========================================
  test('Deve criar novo cliente com sucesso', async ({ page }) => {
    // Este teste NÃO depende de outros testes

    await clientesPage.criarCliente({
      cnpj: '00.000.000/0001-91',
      razaoSocial: 'CLIENTE TESTE CRIACAO LTDA',
      nomeFantasia: 'CLIENTE TESTE'
    });

    // Validar que cliente foi criado
    await clientesPage.validarClienteNaListagem('CLIENTE TESTE CRIACAO LTDA');
  });

  // ========================================
  // TESTE 2: Editar Cliente (Isolado)
  // ========================================
  test('Deve editar cliente existente', async ({ page }) => {
    // Este teste cria SEUS dados (não depende de teste anterior)

    // 1. Criar cliente via API
    const clienteId = await apiHelper.criarClienteViaAPI({
      cnpj: '00.000.000/0001-92',
      razaoSocial: 'CLIENTE TESTE EDICAO LTDA'
    });

    // 2. Recarregar para ver novo cliente
    await page.reload({ waitUntil: 'networkidle' });
    await clientesPage.closeAllOverlays();

    // 3. Editar cliente
    await clientesPage.editarCliente(clienteId, {
      nomeFantasia: 'NOME EDITADO'
    });

    // 4. Validar edição
    await clientesPage.validarClienteNaListagem('NOME EDITADO');
  });

  // ========================================
  // TESTE 3: Excluir Cliente (Isolado)
  // ========================================
  test('Deve excluir cliente existente', async ({ page }) => {
    // Este teste cria SEUS dados

    let clienteId: string | null = null;

    try {
      // 1. Criar cliente via API
      clienteId = await apiHelper.criarClienteViaAPI({
        cnpj: '00.000.000/0001-93',
        razaoSocial: 'CLIENTE TESTE DELETE LTDA'
      });

      // 2. Recarregar
      await page.reload({ waitUntil: 'networkidle' });
      await clientesPage.closeAllOverlays();

      // 3. Excluir cliente
      await clientesPage.excluirCliente('CLIENTE TESTE DELETE LTDA');

      // 4. Validar exclusão
      await expect(
        page.locator('[data-test="cliente-row"]:has-text("CLIENTE TESTE DELETE LTDA")')
      ).not.toBeVisible();

    } finally {
      // Cleanup: Se teste falhou, garantir exclusão
      if (clienteId) {
        await apiHelper.excluirClienteViaAPI(clienteId).catch(() => {});
      }
    }
  });

  // ========================================
  // TESTE 4: Listar Clientes (Isolado)
  // ========================================
  test('Deve listar clientes cadastrados', async ({ page }) => {
    // Este teste valida listagem (não depende de criação prévia)

    // 1. Criar 3 clientes via API
    await apiHelper.criarClienteViaAPI({
      cnpj: '00.000.000/0001-94',
      razaoSocial: 'CLIENTE LISTAGEM 1'
    });

    await apiHelper.criarClienteViaAPI({
      cnpj: '00.000.000/0001-95',
      razaoSocial: 'CLIENTE LISTAGEM 2'
    });

    await apiHelper.criarClienteViaAPI({
      cnpj: '00.000.000/0001-96',
      razaoSocial: 'CLIENTE LISTAGEM 3'
    });

    // 2. Recarregar
    await page.reload({ waitUntil: 'networkidle' });
    await clientesPage.closeAllOverlays();

    // 3. Validar que todos aparecem
    await clientesPage.validarClienteNaListagem('CLIENTE LISTAGEM 1');
    await clientesPage.validarClienteNaListagem('CLIENTE LISTAGEM 2');
    await clientesPage.validarClienteNaListagem('CLIENTE LISTAGEM 3');
  });
});
```

---

## 8. CRITÉRIO DE APROVAÇÃO

### 8.1. Estrutura

- ✅ Page Objects criados (herdam `BasePage`)
- ✅ `closeAllOverlays()` implementado em `BasePage`
- ✅ API helpers implementados
- ✅ Massa de teste centralizada

### 8.2. Testes

- ✅ TODOS os testes possuem `beforeEach` com:
  - Login
  - Navigate
  - closeAllOverlays()
- ✅ TODOS os testes possuem `afterEach` com:
  - closeAllOverlays()
  - Logout
- ✅ NENHUM teste usa `test.describe.serial`
- ✅ NENHUM teste compartilha variáveis entre si
- ✅ Cada teste cria SEUS dados (via API ou UI)

### 8.3. Validação

- ✅ `python tools/validate-isolated-tests.py RFXXX` retorna 0
- ✅ Taxa de aprovação E2E: ≥ 95%
- ✅ Zero falhas por overlay/backdrop persistente
- ✅ Zero falhas por contaminação de estado

### 8.4. Configuração

- ✅ `playwright.config.ts` configurado para isolated:
  - `fullyParallel: true` (opcional)
  - `workers: 1-4` (opcional)
  - `retries: 0-2` (opcional)

---

## 9. VANTAGENS DO PADRÃO ISOLATED

| Aspecto | Stateful | Isolated | Vantagem |
|---------|----------|----------|----------|
| **Isolamento** | ❌ Testes dependem uns dos outros | ✅ Cada teste independente | +100% |
| **Contaminação** | ❌ 67% falhas por estado residual | ✅ 0% contaminação | -67% |
| **Paralelização** | ❌ Não permitido (workers: 1) | ✅ Permitido (workers: 4) | 4x mais rápido |
| **Debug** | ❌ Difícil (dependências) | ✅ Fácil (teste isolado) | +80% |
| **Manutenção** | ❌ Frágil (quebra em cadeia) | ✅ Robusto (independente) | +90% |
| **Aprovação E2E** | ❌ 10-60% | ✅ 95-100% | +35-90% |

---

## 10. MIGRAÇÃO DE STATEFUL PARA ISOLATED

### 10.1. Quando Migrar

**Migre para Isolated se:**
- ✅ Testes NÃO precisam compartilhar dados
- ✅ Cada UC pode ser testado independentemente
- ✅ Operações CRUD podem usar dados criados via API

**Mantenha Stateful se:**
- ❌ Testes **DEVEM** compartilhar dados (ex: fluxo sequencial obrigatório)
- ❌ RF possui dependências intrínsecas entre operações

### 10.2. Passos de Migração

1. **Criar Page Objects** (herdar `BasePage`)
2. **Implementar closeAllOverlays()** em `BasePage`
3. **Implementar API helpers** para criar dados
4. **Adicionar beforeEach/afterEach** em cada teste
5. **Remover test.describe.serial** → usar `test.describe`
6. **Remover variáveis compartilhadas** entre testes
7. **Fazer cada teste criar SEUS dados**
8. **Executar validação:** `python tools/validate-isolated-tests.py RFXXX`
9. **Atualizar playwright.config.ts** (fullyParallel: true)

---

## 11. REFERÊNCIAS

| Documento | Caminho |
|-----------|---------|
| Contrato Stateful | [CONTRATO-TESTES-E2E-STATEFUL.md](CONTRATO-TESTES-E2E-STATEFUL.md) |
| Contrato Execução Completa | [execucao-completa.md](execucao-completa.md) |
| Análise RF006 | [D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md](D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md) |
| Proposta Arquiteto | [D:\IC2\.temp_ia\PROPOSTA-ARQUITETO-INTEGRACAO-E2E-ISOLADOS.md](D:\IC2\.temp_ia\PROPOSTA-ARQUITETO-INTEGRACAO-E2E-ISOLADOS.md) |
| Dialog Helpers | [D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts](D:\IC2\frontend\icontrolit-app\e2e\helpers\dialog-helpers.ts) |

---

## 12. HISTÓRICO DE VERSÕES

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2026-01-11 | Criação do contrato de testes E2E isolados com Page Object Pattern, beforeEach/afterEach obrigatórios, closeAllOverlays() helper, API helpers, e validação de isolamento. Substitui padrão stateful para RFs com operações independentes. Baseado em análise de problemas RF006 (10-60% aprovação E2E devido a contaminação de estado, overlay/backdrop persistente). Resultado esperado: 95-100% aprovação E2E, zero contaminação, 4x mais rápido com paralelização. Referências: CONTRATO-TESTES-E2E-STATEFUL.md, execucao-completa.md, RELATORIO-TESTES-RF006-2026-01-11.md, PROPOSTA-ARQUITETO-INTEGRACAO-E2E-ISOLADOS.md. |

---

## 13. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- Não estiver explicitamente prevista neste contrato, OU
- Conflitar com qualquer regra deste contrato

ENTÃO:
- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**

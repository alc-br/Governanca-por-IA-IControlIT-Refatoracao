# PROMPT DE GERAÇÃO: TESTES E2E ISOLADOS (ISOLATED PATTERN)

**Versão:** 1.0
**Data:** 2026-01-11
**Contrato:** CONTRATO-TESTES-E2E-ISOLADOS.md
**Substitui:** geracao-testes-e2e-playwright.md (padrão stateful deprecado)
**Changelog v1.0:** Criação do prompt para geração de testes E2E isolados com Page Object Pattern, beforeEach/afterEach, closeAllOverlays, API helpers. Substitui padrão stateful (test.describe.serial) por isolated (test.describe). Baseado em análise RF006 (10-60% aprovação por contaminação de estado).

---

## 📋 INSTRUÇÕES PARA O AGENTE

Você está prestes a gerar testes E2E **isolados** (cada teste independente) usando Playwright.

**Padrão:** ISOLATED (substituiu o padrão stateful deprecado)
**Contrato:** [CONTRATO-TESTES-E2E-ISOLADOS.md](../../contracts/testes/CONTRATO-TESTES-E2E-ISOLADOS.md)
**Checklist:** [CHECKLIST-TESTES-E2E-ISOLADOS.yaml](../../checklists/testes/CHECKLIST-TESTES-E2E-ISOLADOS.yaml)

---

## 1. PRÉ-REQUISITOS OBRIGATÓRIOS

Antes de iniciar, você **DEVE** verificar:

### 1.1. Documentação Completa

- ✅ `TC-RFXXX.yaml` existe e está validado
- ✅ `TC-RFXXX.yaml` possui `metadata.tipo_teste = "ISOLATED"`
- ✅ `MT-RFXXX.data.ts` existe com CREDENCIAIS_TESTE, FRONTEND_URLS, DATA_TEST_SELECTORS
- ✅ `UC-RFXXX.yaml` existe com especificações de teste completas

**SE tipo_teste ≠ "ISOLATED":**
- ❌ PARAR - Este prompt é APENAS para testes ISOLATED
- ❌ Se stateful, usar prompt: [geracao-testes-e2e-stateful.md](geracao-testes-e2e-stateful.md)

### 1.2. Estrutura de Diretórios

```
e2e/
├── specs/        ← Arquivos .spec.ts (você vai criar)
├── pages/        ← Page Objects (você vai criar)
├── helpers/      ← Helpers (você vai criar)
└── data/         ← MT-RFXXX.data.ts (já existe)
```

**Criar diretórios se não existirem:**

```bash
mkdir -p e2e/pages
mkdir -p e2e/helpers
```

---

## 2. FASE 1: CRIAR BASE PAGE OBJECT

### 2.1. Arquivo: `e2e/pages/base.page.ts`

**Criar arquivo:**

```typescript
import { Page, Locator } from '@playwright/test';

/**
 * Base Page Object
 * Todos os Page Objects DEVEM herdar desta classe
 *
 * Referência: CONTRATO-TESTES-E2E-ISOLADOS.md seção 2.2
 */
export class BasePage {
  constructor(protected page: Page) {}

  /**
   * OBRIGATÓRIO: Limpar todos os overlays/backdrops
   * Previne contaminação de estado entre testes
   *
   * Resolve 67% dos problemas do RF006 (overlay/backdrop persistente)
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

**Validação:**
- ✅ Arquivo criado em `e2e/pages/base.page.ts`
- ✅ closeAllOverlays() implementado com retry logic
- ✅ waitForDialogToClosed() e waitForDialogToOpen() implementados

---

## 3. FASE 2: CRIAR LOGIN PAGE OBJECT

### 3.1. Arquivo: `e2e/pages/login.page.ts`

**Ler massa de teste:**
- Ler `MT-RFXXX.data.ts` → `FRONTEND_URLS.signIn`
- Ler `MT-RFXXX.data.ts` → `DATA_TEST_SELECTORS`

**Criar arquivo:**

```typescript
import { Page, Locator } from '@playwright/test';
import { BasePage } from './base.page';

export class LoginPage extends BasePage {
  private readonly inputEmail: Locator;
  private readonly inputPassword: Locator;
  private readonly btnLogin: Locator;
  private readonly btnLogout: Locator;

  constructor(page: Page) {
    super(page);

    // Seletores de login (ajustar conforme MT-RFXXX.data.ts)
    this.inputEmail = page.locator('[data-test="login-input-email"]');
    this.inputPassword = page.locator('[data-test="login-input-password"]');
    this.btnLogin = page.locator('[data-test="login-btn-entrar"]');
    this.btnLogout = page.locator('[data-test="btn-logout"]');
  }

  /**
   * Navegar para página de login
   */
  async navigate(): Promise<void> {
    // URL de login vem de MT-RFXXX.data.ts → FRONTEND_URLS.signIn
    await this.page.goto('http://localhost:4200/sign-in', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
  }

  /**
   * Executar login
   * Retorna token JWT para uso em API helpers
   */
  async login(email: string, password: string): Promise<string> {
    await this.inputEmail.fill(email);
    await this.inputPassword.fill(password);
    await this.btnLogin.click();

    // Aguardar navegação após login
    await this.page.waitForURL('**/dashboard', { timeout: 10000 });

    // Extrair token JWT do localStorage
    const token = await this.page.evaluate(() => {
      return localStorage.getItem('access_token') || '';
    });

    return token;
  }

  /**
   * Executar logout
   */
  async logout(): Promise<void> {
    // Se botão logout não visível, já está deslogado
    const isVisible = await this.btnLogout.isVisible().catch(() => false);

    if (!isVisible) {
      return;
    }

    await this.btnLogout.click();

    // Aguardar redirecionamento para login
    await this.page.waitForURL('**/sign-in', { timeout: 10000 });
  }
}
```

**Validação:**
- ✅ LoginPage herda BasePage
- ✅ login() retorna token JWT
- ✅ logout() implementado

---

## 4. FASE 3: CRIAR ENTITY PAGE OBJECT

### 4.1. Analisar UC-RFXXX.yaml

**Você DEVE ler:**
- `UC-RFXXX.yaml` → `navegacao.url_completa`
- `UC-RFXXX.yaml` → `passos[].elemento.data_test`
- `UC-RFXXX.yaml` → `tabela.data_test_container`
- `UC-RFXXX.yaml` → `estados_ui.*`

### 4.2. Template: Entity Page Object

**Exemplo: `e2e/pages/clientes.page.ts`**

```typescript
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './base.page';

export class ClientesPage extends BasePage {
  // ========================================
  // SELETORES (centralizados de UC-RF006.yaml)
  // ========================================
  private readonly btnNovoCliente: Locator;
  private readonly inputCNPJ: Locator;
  private readonly inputRazaoSocial: Locator;
  private readonly inputNomeFantasia: Locator;
  private readonly btnSalvar: Locator;
  private readonly btnCancelar: Locator;
  private readonly clienteRow: Locator;
  private readonly loadingSpinner: Locator;
  private readonly emptyState: Locator;
  private readonly errorMessage: Locator;

  constructor(page: Page) {
    super(page);

    // Inicializar seletores de UC-RF006.yaml
    this.btnNovoCliente = page.locator('[data-test="RF006-criar-cliente"]');
    this.inputCNPJ = page.locator('[data-test="RF006-input-cnpj"]');
    this.inputRazaoSocial = page.locator('[data-test="RF006-input-razaosocial"]');
    this.inputNomeFantasia = page.locator('[data-test="RF006-input-nomefantasia"]');
    this.btnSalvar = page.locator('[data-test="RF006-salvar-cliente"]');
    this.btnCancelar = page.locator('[data-test="btn-cancelar-dialog"]');
    this.clienteRow = page.locator('[data-test="cliente-row"]');
    this.loadingSpinner = page.locator('[data-test="loading-spinner"]');
    this.emptyState = page.locator('[data-test="empty-state"]');
    this.errorMessage = page.locator('[data-test="error-message"]');
  }

  // ========================================
  // NAVEGAÇÃO
  // ========================================

  /**
   * Navegar para página de clientes
   * URL de UC-RF006.yaml → navegacao.url_completa
   */
  async navigate(): Promise<void> {
    await this.page.goto('http://localhost:4200/management/clientes', {
      waitUntil: 'networkidle',
      timeout: 30000
    });

    // Aguardar loading desaparecer
    await this.loadingSpinner.waitFor({ state: 'detached', timeout: 30000 });
  }

  // ========================================
  // OPERAÇÕES CRUD
  // ========================================

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
      await this.inputNomeFantasia.fill(dados.nomeFantasia);
    }

    // 3. Salvar
    await this.btnSalvar.click();

    // 4. Aguardar dialog fechar
    await this.waitForDialogToClosed();

    // 5. Aguardar navegação de volta à listagem
    await this.page.waitForURL('**/management/clientes', { timeout: 10000 });
  }

  /**
   * Editar cliente existente
   */
  async editarCliente(clienteId: string, dados: {
    nomeFantasia?: string;
    razaoSocial?: string;
  }): Promise<void> {
    // 1. Localizar linha do cliente
    const row = this.page.locator(`[data-test="cliente-row"][data-cliente-id="${clienteId}"]`);

    // 2. Clicar em editar
    await row.locator('[data-test="RF006-editar-cliente"]').click();
    await this.waitForDialogToOpen('dialog-editar-cliente');

    // 3. Preencher campos modificados
    if (dados.nomeFantasia) {
      await this.inputNomeFantasia.clear();
      await this.inputNomeFantasia.fill(dados.nomeFantasia);
    }

    if (dados.razaoSocial) {
      await this.inputRazaoSocial.clear();
      await this.inputRazaoSocial.fill(dados.razaoSocial);
    }

    // 4. Salvar
    await this.btnSalvar.click();
    await this.waitForDialogToClosed();
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

  // ========================================
  // VALIDAÇÕES
  // ========================================

  /**
   * Validar que cliente existe na listagem
   */
  async validarClienteNaListagem(razaoSocial: string): Promise<void> {
    const row = this.page.locator(`[data-test="cliente-row"]:has-text("${razaoSocial}")`);
    await expect(row).toBeVisible({ timeout: 10000 });
  }

  /**
   * Validar que cliente NÃO existe na listagem
   */
  async validarClienteNaoNaListagem(razaoSocial: string): Promise<void> {
    const row = this.page.locator(`[data-test="cliente-row"]:has-text("${razaoSocial}")`);
    await expect(row).not.toBeVisible();
  }

  /**
   * Obter ID do último cliente criado (útil para cleanup)
   */
  async getUltimoClienteCriado(): Promise<string> {
    const primeiraRow = this.clienteRow.first();
    const clienteId = await primeiraRow.getAttribute('data-cliente-id');
    return clienteId || '';
  }
}
```

**Instruções para você:**
1. Substituir "clientes" pela entidade do RF atual
2. Substituir "RF006" pelo número do RF atual
3. Mapear TODOS os data-test de UC-RFXXX.yaml
4. Implementar TODOS os métodos CRUD necessários

**Validação:**
- ✅ Entity Page Object herda BasePage
- ✅ Seletores mapeados de UC-RFXXX.yaml
- ✅ Métodos CRUD implementados
- ✅ Métodos de validação implementados

---

## 5. FASE 4: CRIAR API HELPERS

### 5.1. Arquivo: `e2e/helpers/api-helpers.ts`

**Objetivo:** Criar dados rapidamente via API (sem UI) para testes isolados

```typescript
import { request } from '@playwright/test';

/**
 * API Helper para criação rápida de dados (sem UI)
 * Usado em testes isolated para cada teste criar SEUS dados
 *
 * Referência: CONTRATO-TESTES-E2E-ISOLADOS.md seção 4
 */
export class APIHelper {
  private baseURL = 'http://localhost:5000';
  private token: string;

  constructor(token: string) {
    this.token = token;
  }

  /**
   * Criar cliente via API
   * Retorna ID do cliente criado
   */
  async criarClienteViaAPI(dados: {
    cnpj: string;
    razaoSocial: string;
    nomeFantasia?: string;
  }): Promise<string> {
    const context = await request.newContext({
      baseURL: this.baseURL,
      extraHTTPHeaders: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      }
    });

    const response = await context.post('/api/clientes', {
      data: {
        cnpj: dados.cnpj,
        razaoSocial: dados.razaoSocial,
        nomeFantasia: dados.nomeFantasia || dados.razaoSocial
      }
    });

    if (!response.ok()) {
      throw new Error(`Falha ao criar cliente via API: ${response.status()}`);
    }

    const body = await response.json();
    return body.id;
  }

  /**
   * Excluir cliente via API
   * Usado em cleanup de testes
   */
  async excluirClienteViaAPI(id: string): Promise<void> {
    const context = await request.newContext({
      baseURL: this.baseURL,
      extraHTTPHeaders: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    await context.delete(`/api/clientes/${id}`);
  }

  /**
   * Listar clientes via API
   * Útil para validações
   */
  async listarClientesViaAPI(): Promise<any[]> {
    const context = await request.newContext({
      baseURL: this.baseURL,
      extraHTTPHeaders: {
        'Authorization': `Bearer ${this.token}`
      }
    });

    const response = await context.get('/api/clientes');
    const body = await response.json();
    return body.items || [];
  }
}
```

**Instruções para você:**
1. Substituir "clientes" pela entidade do RF atual
2. Adicionar métodos para TODAS as operações CRUD necessárias
3. Ajustar URLs de API conforme backend

**Validação:**
- ✅ API helper implementado
- ✅ Métodos CRUD via API implementados
- ✅ Token JWT usado para autenticação

---

## 6. FASE 5: CRIAR SPECS (TESTES)

### 6.1. Estrutura de Specs

**Para cada TC de TC-RFXXX.yaml, criar 1 arquivo .spec.ts:**

```
TC-RF006-E2E-001.spec.ts  ← Testes de CRUD
TC-RF006-E2E-002.spec.ts  ← Testes de validação
TC-RF006-E2E-003.spec.ts  ← Testes de segurança
```

### 6.2. Template: Spec File (ISOLATED)

**Arquivo:** `e2e/specs/TC-RF006-E2E-001.spec.ts`

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
 * UC: UC-RF006.yaml
 * TC: TC-RF006.yaml
 * MT: MT-RF006.data.ts
 */
test.describe('TC-RF006-E2E-001: CRUD Clientes (Isolated)', () => {

  // ========================================
  // SETUP: beforeEach (OBRIGATÓRIO)
  // ========================================
  test.beforeEach(async ({ page }) => {
    // 1. Inicializar Page Objects
    loginPage = new LoginPage(page);
    clientesPage = new ClientesPage(page);

    // 2. Login e obter token
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
  // TESTES ISOLADOS
  // ========================================

  /**
   * TC-RF006-FUN-001: Criar Cliente
   * Covers: UC01-FP-01
   */
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

  /**
   * TC-RF006-FUN-002: Editar Cliente
   * Covers: UC03-FP-01
   */
  test('Deve editar cliente existente', async ({ page }) => {
    // Este teste cria SEUS dados (não depende de teste anterior)

    // 1. Criar cliente via API (rápido)
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

  /**
   * TC-RF006-FUN-003: Excluir Cliente
   * Covers: UC04-FP-01
   */
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
      await clientesPage.validarClienteNaoNaListagem('CLIENTE TESTE DELETE LTDA');

    } finally {
      // Cleanup: Se teste falhou, garantir exclusão via API
      if (clienteId) {
        await apiHelper.excluirClienteViaAPI(clienteId).catch(() => {
          // Ignora erro se já foi excluído
        });
      }
    }
  });

  /**
   * TC-RF006-FUN-004: Listar Clientes
   * Covers: UC02-FP-01
   */
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

**REGRAS CRÍTICAS PARA SPECS:**

- ✅ **SEMPRE** usar `test.describe` (NÃO `test.describe.serial`)
- ✅ **SEMPRE** ter `test.beforeEach` com login + navigate + closeAllOverlays
- ✅ **SEMPRE** ter `test.afterEach` com closeAllOverlays + logout
- ✅ **NUNCA** compartilhar variáveis entre testes (let clienteId fora de test())
- ✅ **SEMPRE** cada teste cria SEUS dados (via API ou UI)
- ✅ **SEMPRE** usar Page Objects (NÃO seletores diretos no spec)

**Validação:**
- ✅ TODOS os specs seguem padrão isolated
- ✅ beforeEach/afterEach implementados
- ✅ Nenhum test.describe.serial
- ✅ Nenhuma variável compartilhada entre testes

---

## 7. FASE 6: CRIAR SCRIPT DE VALIDAÇÃO

### 7.1. Arquivo: `tools/validate-isolated-tests.py`

**Criar arquivo:**

```python
#!/usr/bin/env python3
"""
Valida que testes E2E seguem padrão isolated (não stateful)

Referência: CONTRATO-TESTES-E2E-ISOLADOS.md seção 5
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

**Validação:**
- ✅ Script criado em `tools/validate-isolated-tests.py`
- ✅ Script valida beforeEach/afterEach
- ✅ Script valida closeAllOverlays
- ✅ Script valida ausência de test.describe.serial

---

## 8. FASE 7: EXECUTAR TESTES E VALIDAR

### 8.1. Executar Testes

```bash
# Executar todos os testes E2E do RF
npx playwright test e2e/specs/TC-RF006-*.spec.ts --reporter=list
```

### 8.2. Executar Validação Automática

```bash
# Validar que testes seguem padrão isolated
python tools/validate-isolated-tests.py 006
```

**Critério de aprovação:**
- ✅ Script retorna exit code 0
- ✅ Taxa de aprovação E2E ≥ 95%
- ✅ Zero falhas por overlay/backdrop persistente

**SE validação FALHAR:**
- ❌ Corrigir problemas reportados
- ❌ Re-executar validação

---

## 9. FASE 8: DOCUMENTAR

### 9.1. Atualizar STATUS.yaml

```yaml
testes:
  e2e:
    tipo_teste_e2e: "ISOLATED"  # ← DOCUMENTAR
    contrato_referencia: "CONTRATO-TESTES-E2E-ISOLADOS.md"

    estrutura:
      page_objects_criados: true
      base_page_implementado: true
      api_helpers_criados: true

    validacao:
      script_validacao: "tools/validate-isolated-tests.py"
      resultado_validacao: "✅ APROVADO"
      taxa_aprovacao_e2e: "98%"  # ← Atualizar com resultado real

    specs_criados:
      - "TC-RF006-E2E-001.spec.ts (4 testes)"
      - "TC-RF006-E2E-002.spec.ts (3 testes)"

    data_execucao: "2026-01-11"
```

### 9.2. Atualizar TC-RFXXX.yaml

```yaml
metadata:
  tipo_teste: "ISOLATED"  # ← Confirmar
  contrato_referencia: "D:\\IC2_Governanca\\governanca\\contracts\\testes\\CONTRATO-TESTES-E2E-ISOLADOS.md"
```

---

## 10. CHECKLIST FINAL

Antes de marcar como DONE, você **DEVE** verificar:

- [ ] **Page Objects:**
  - [ ] BasePage criado com closeAllOverlays()
  - [ ] LoginPage criado
  - [ ] Entity Page Object criado

- [ ] **Helpers:**
  - [ ] API helpers criados

- [ ] **Specs:**
  - [ ] TODOS os specs possuem beforeEach (login + navigate + closeAllOverlays)
  - [ ] TODOS os specs possuem afterEach (closeAllOverlays + logout)
  - [ ] NENHUM spec usa test.describe.serial
  - [ ] NENHUM spec compartilha variáveis entre testes
  - [ ] Cada teste cria SEUS dados (via API ou UI)

- [ ] **Validação:**
  - [ ] Script validate-isolated-tests.py criado
  - [ ] Script retorna exit code 0
  - [ ] Taxa de aprovação E2E ≥ 95%
  - [ ] Zero falhas por overlay/backdrop persistente

- [ ] **Documentação:**
  - [ ] STATUS.yaml atualizado
  - [ ] TC-RFXXX.yaml documenta tipo_teste: ISOLATED

**SE TUDO APROVADO:**
- ✅ Testes E2E isolated CONCLUÍDOS

**SE ALGO FALHAR:**
- ❌ Corrigir e re-validar

---

## 11. REFERÊNCIAS

| Documento | Caminho |
|-----------|---------|
| Contrato Isolated | [CONTRATO-TESTES-E2E-ISOLADOS.md](../../contracts/testes/CONTRATO-TESTES-E2E-ISOLADOS.md) |
| Contrato Stateful | [CONTRATO-TESTES-E2E-STATEFUL.md](../../contracts/testes/CONTRATO-TESTES-E2E-STATEFUL.md) |
| Checklist Isolated | [CHECKLIST-TESTES-E2E-ISOLADOS.yaml](../../checklists/testes/CHECKLIST-TESTES-E2E-ISOLADOS.yaml) |
| Análise RF006 | [D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md](D:\IC2\.temp_ia\RELATORIO-TESTES-RF006-2026-01-11.md) |

---

**FIM DO PROMPT**

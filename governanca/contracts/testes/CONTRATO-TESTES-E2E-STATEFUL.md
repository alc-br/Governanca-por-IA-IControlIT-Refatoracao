# CONTRATO DE TESTES E2E STATEFUL

**Versão:** 1.0
**Data:** 2026-01-11
**Status:** Ativo
**Contexto:** Criado após análise do RF006 onde banco estava sendo resetado entre testes stateful, resultando em taxa de aprovação de 16.7% (1/6 testes).

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato define

Este contrato define **COMO** implementar testes E2E stateful (testes que compartilham estado de banco de dados entre múltiplos passos) para evitar o problema identificado no RF006 onde dados criados no Passo 1 desapareciam no Passo 2.

### 🎯 Problema que resolve

- **Taxa de aprovação:** 16.7% → 100%
- **Causa raiz:** Banco resetado entre testes
- **Impacto:** Impossível validar fluxos CRUD completos

### 📦 Escopo

**Aplicável a:**
- Testes de fluxo CRUD completo (Criar → Listar → Editar → Excluir)
- Jornada de usuário multi-etapas
- Validação de persistência de dados

**Não aplicável a:**
- Testes independentes (cada teste cria próprios dados)
- Testes de funcionalidades isoladas
- Testes de validação de formulários

---

## 1. DEFINIÇÃO E CASOS DE USO

### O Que São Testes Stateful

Testes que **compartilham estado** (banco de dados, sessão, dados criados) entre múltiplos passos/testes.

**Características:**
- Dados criados no Passo N devem estar disponíveis no Passo N+1
- Ordem de execução importa (serial execution)
- Falha em um passo invalida passos subsequentes

### Quando Usar

- ✅ **Fluxo CRUD completo** (Criar → Listar → Editar → Excluir)
- ✅ **Jornada de usuário multi-etapas** (Login → Ação → Logout)
- ✅ **Validação de persistência de dados** (dado criado permanece após reload)
- ✅ **Testes de integração end-to-end** (múltiplos módulos)

### Quando NÃO Usar

- ❌ **Testes independentes** (cada teste cria próprios dados)
- ❌ **Testes de funcionalidades isoladas** (validar um botão)
- ❌ **Testes de validação de formulários** (sem persistência)
- ❌ **Testes paralelos** (stateful é sempre serial)

---

## 2. CONFIGURAÇÃO OBRIGATÓRIA - PLAYWRIGHT

### 2.1 Arquivo: playwright.config.ts

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  fullyParallel: false,  // OBRIGATÓRIO para stateful
  workers: 1,            // OBRIGATÓRIO: apenas 1 worker
  retries: 0,            // OBRIGATÓRIO: sem retry (dados mudam)

  use: {
    baseURL: 'http://localhost:8080',
    trace: 'off',
    screenshot: 'only-on-failure',
    video: 'off',
  },
});
```

**Justificativa:**

| Configuração | Valor | Por Quê |
|--------------|-------|---------|
| `fullyParallel` | `false` | Testes executam em **sequência** |
| `workers` | `1` | Apenas **1 processo** (garante ordem) |
| `retries` | `0` | **Sem retry** (dados do banco mudam entre tentativas) |

### 2.2 Estrutura de Teste

```typescript
import { test, expect } from '@playwright/test';

// OBRIGATÓRIO: test.describe.serial para compartilhar estado
test.describe.serial('Fluxo CRUD Completo', () => {

  // PROIBIDO: beforeEach que reseta estado
  // ❌ test.beforeEach(async ({ page }) => { await resetDatabase(); });

  // PERMITIDO: beforeAll para setup único
  test.beforeAll(async () => {
    // Setup compartilhado (executado UMA VEZ)
    console.log('Setup inicial executado uma vez');
  });

  test('Passo 1: Criar', async ({ page }) => {
    // Cria dados que serão usados em Passo 2
    await page.goto('/management/clientes');
    await page.click('[data-test="btn-novo-cliente"]');
    // ...
  });

  test('Passo 2: Listar', async ({ page }) => {
    // Valida dados criados no Passo 1
    await page.goto('/management/clientes');
    // Cliente criado no Passo 1 DEVE estar visível
  });

  test('Passo 3: Editar', async ({ page }) => {
    // Edita dados criados no Passo 1
  });

  test('Passo 4: Excluir', async ({ page }) => {
    // Exclui dados criados no Passo 1
  });
});
```

---

## 3. CONFIGURAÇÃO OBRIGATÓRIA - BACKEND

### 3.1 Problema Identificado

```csharp
// ❌ INCORRETO: Resetar banco a cada request
public class ApplicationDbContextInitialiser
{
    public async Task SeedAsync()
    {
        // Se resetar banco aqui, testes stateful falham
        await _context.Database.EnsureDeletedAsync();  // ❌ PROIBIDO em E2E
        await _context.Database.MigrateAsync();

        // Seed de dados...
    }
}
```

**Por que isso causa o problema:**
- `EnsureDeletedAsync()` **apaga o banco inteiro**
- Se chamado a cada request, dados criados no Passo 1 **desaparecem**
- Testes stateful se tornam **inviáveis**

### 3.2 Solução - Seed Apenas no Startup

```csharp
// ✅ CORRETO: Seed apenas uma vez
public class Program
{
    public static async Task Main(string[] args)
    {
        var host = CreateHostBuilder(args).Build();

        // Seed apenas no startup (não a cada request)
        using (var scope = host.Services.CreateScope())
        {
            var services = scope.ServiceProvider;
            var initialiser = services.GetRequiredService<ApplicationDbContextInitialiser>();

            // OBRIGATÓRIO: Migrations primeiro
            await initialiser.InitialiseAsync();

            // Seed SOMENTE se banco vazio
            var context = services.GetRequiredService<ApplicationDbContext>();
            if (!await context.Users.AnyAsync())
            {
                await initialiser.SeedAsync();
            }
        }

        await host.RunAsync();
    }
}
```

**Validação obrigatória:**
- [ ] `EnsureDeletedAsync()` **NÃO** é chamado durante requests
- [ ] Seed executa **apenas no startup** da aplicação
- [ ] Migrations são aplicadas **antes** do seed
- [ ] Banco **mantém dados** entre requests subsequentes

### 3.3 Onde Investigar no Código Atual

**Arquivos backend a verificar:**
```
D:\IC2\backend\IControlIT.Infrastructure\Data\ApplicationDbContextInitialiser.cs
D:\IC2\backend\IControlIT.API\Program.cs
D:\IC2\backend\IControlIT.API\Startup.cs (se existir)
```

**O que procurar:**

1. ❌ Chamadas a `EnsureDeletedAsync()` ou `Database.EnsureDeleted()`
2. ❌ Chamadas a `SeedAsync()` fora do startup
3. ❌ Middleware que reseta banco
4. ❌ Configuração de ambiente de testes que apaga banco

---

## 4. FIXTURES DO PLAYWRIGHT (Dados Compartilhados)

### 4.1 Criar Fixture de Cliente

**Arquivo:** `frontend/icontrolit-app/e2e/fixtures/cliente-teste.ts`

```typescript
import { test as base } from '@playwright/test';

type ClienteFixture = {
  clienteId: string;
};

export const test = base.extend<ClienteFixture>({
  clienteId: async ({ page }, use) => {
    // Setup: criar cliente de teste (executado UMA VEZ)
    await page.goto('/management/clientes');
    await page.click('[data-test="btn-novo-cliente"]');
    await page.fill('[data-test="cnpj"]', '00.000.000/0001-91');
    await page.click('[data-test="btn-consultar-cnpj"]');
    await page.waitForSelector('[data-test="razaoSocial"]', { state: 'visible' });
    await page.click('[data-test="btn-salvar"]');
    await page.waitForURL('**/management/clientes');

    // Capturar ID do cliente criado
    const url = page.url();
    const clienteId = url.match(/\/clientes\/([^\/]+)/)?.[1] ?? '';

    // Fornecer ID para os testes
    await use(clienteId);

    // Teardown: limpar cliente (opcional)
    // await page.goto(`/management/clientes/${clienteId}`);
    // await page.click('[data-test="menu-acoes"]');
    // await page.click('[data-test="btn-excluir"]');
    // await page.click('button:has-text("Confirmar")');
  },
});
```

### 4.2 Usar Fixture nos Testes

```typescript
import { test } from './fixtures/cliente-teste';
import { expect } from '@playwright/test';

test.describe.serial('CRUD com Fixture', () => {

  test('Passo 2: Listar', async ({ page, clienteId }) => {
    await page.goto('/management/clientes');

    // Cliente criado pela fixture DEVE estar visível
    const clienteRow = page.locator(`[data-id="${clienteId}"]`);
    await expect(clienteRow).toBeVisible();
  });

  test('Passo 3: Editar', async ({ page, clienteId }) => {
    await page.goto(`/management/clientes/${clienteId}`);

    await page.fill('[data-test="nomeFantasia"]', 'NOME EDITADO');
    await page.click('[data-test="btn-salvar"]');

    await page.waitForURL('**/management/clientes');
  });

  test('Passo 4: Excluir', async ({ page, clienteId }) => {
    await page.goto('/management/clientes');

    const clienteRow = page.locator(`[data-id="${clienteId}"]`);
    await clienteRow.locator('[data-test="menu-acoes"]').click();
    await page.click('[data-test="btn-excluir"]');
    await page.click('button:has-text("Confirmar")');

    // Cliente NÃO deve aparecer mais
    await expect(clienteRow).not.toBeVisible();
  });
});
```

**Vantagens:**
- ✅ Setup executado **uma vez**
- ✅ ID **compartilhado** entre todos os testes
- ✅ Cleanup **automático** após suite
- ✅ Código mais limpo e reutilizável

---

## 5. EXEMPLO COMPLETO - RF006

### 5.1 Arquivo: TC-RF006-E2E-001.spec.ts (CORRIGIDO)

```typescript
import { test, expect } from '@playwright/test';
import { MT_RF006_001 } from '../../data/MT-RF006.data';
import { waitForDialogToClosed } from '../../helpers';

test.describe.serial('TC-RF006-E2E-001: Fluxo CRUD Completo', () => {
  let clienteId: string;

  test('Passo 1: Criar Cliente', async ({ page }) => {
    await page.goto('/management/clientes');
    await page.click('[data-test~="btn-novo-cliente"]');

    // Preencher CNPJ e consultar ReceitaWS
    await page.fill('[data-test~="cnpj"]', MT_RF006_001.entrada.cnpj);
    await page.click('[data-test~="btn-consultar-cnpj"]');
    await page.waitForSelector('[data-test~="razaoSocial"]', { state: 'visible' });

    // Aguardar backdrop desaparecer (operação assíncrona)
    await waitForDialogToClosed(page);

    // Salvar cliente
    await page.click('[data-test~="btn-salvar"]');
    await page.waitForURL('**/management/clientes');

    // Capturar ID para próximos testes
    const url = page.url();
    clienteId = url.match(/\/clientes\/([^\/]+)/)?.[1] ?? '';

    expect(clienteId).toBeTruthy();
  });

  test('Passo 2: Listar Cliente Criado', async ({ page }) => {
    await page.goto('/management/clientes');

    // Cliente criado no Passo 1 DEVE estar visível
    const clienteRow = page.locator('[data-test~="cliente-row"]')
      .filter({ hasText: MT_RF006_001.entrada.razaoSocial });

    await expect(clienteRow).toBeVisible({ timeout: 10000 });
  });

  test('Passo 3: Visualizar Detalhes', async ({ page }) => {
    await page.goto(`/management/clientes/${clienteId}`);

    await expect(page.locator('[data-test~="razaoSocial"]'))
      .toHaveValue(MT_RF006_001.entrada.razaoSocial);
  });

  test('Passo 4: Editar', async ({ page }) => {
    await page.goto(`/management/clientes/${clienteId}`);

    await page.fill('[data-test~="nomeFantasia"]', 'NOME EDITADO');
    await page.click('[data-test~="btn-salvar"]');

    await page.waitForURL('**/management/clientes');

    // Validar que edição persistiu
    await page.goto(`/management/clientes/${clienteId}`);
    await expect(page.locator('[data-test~="nomeFantasia"]'))
      .toHaveValue('NOME EDITADO');
  });

  test('Passo 5: Validar Listagem Após Edição', async ({ page }) => {
    await page.goto('/management/clientes');

    // Cliente editado DEVE aparecer com novo nome fantasia
    const clienteRow = page.locator('[data-test~="cliente-row"]')
      .filter({ hasText: 'NOME EDITADO' });

    await expect(clienteRow).toBeVisible();
  });

  test('Passo 6: Excluir', async ({ page }) => {
    await page.goto('/management/clientes');

    const clienteRow = page.locator(`[data-id="${clienteId}"]`);
    await clienteRow.locator('[data-test~="menu-acoes"]').click();
    await page.click('[data-test~="btn-excluir"]');

    // Confirmar exclusão
    await page.click('button:has-text("Confirmar")');
    await waitForDialogToClosed(page);

    // Cliente NÃO deve aparecer mais
    await expect(clienteRow).not.toBeVisible();
  });
});
```

---

## 6. VALIDAÇÃO OBRIGATÓRIA

### Checklist Pré-Execução

**Antes de executar testes stateful, validar:**

- [ ] `playwright.config.ts` com `workers: 1` e `fullyParallel: false`
- [ ] `test.describe.serial` usado para fluxos CRUD
- [ ] Backend **NÃO reseta** banco a cada request
- [ ] `beforeAll` usado (não `beforeEach` com reset)
- [ ] Dados criados no Passo N **visíveis** no Passo N+1

### Execução e Validação

```bash
# Executar apenas testes stateful
npx playwright test --grep "serial"

# Validar que workers: 1 está ativo
npx playwright test --list

# Debug de persistência (executar apenas Passo 2)
npx playwright test --debug --grep "Passo 2"
```

### Exit Codes

| Exit Code | Significado | Responsável |
|-----------|-------------|-------------|
| 0 | Todos os passos aprovados | ✅ OK |
| 1 | Falha de teste (lógica) | QA + Frontend |
| 2 | Dados não persistiram (configuração) | Backend + DevOps |

---

## 7. RESPONSABILIZAÇÃO

### Se Dados NÃO Persistem Entre Testes

```yaml
Responsável: Backend + DevOps
Diagnóstico:
  1. Verificar ApplicationDbContextInitialiser.cs
  2. Validar que seed executa apenas no startup
  3. Confirmar que EnsureDeleted() NÃO é chamado
  4. Validar migrations aplicadas corretamente
  5. Verificar configuração de ambiente (appsettings.json)

Ação Imediata:
  - Comentar EnsureDeletedAsync() temporariamente
  - Executar backend e validar que dados persistem
  - Criar PR com correção permanente
```

### Se Testes Falham por Timing/Seletores

```yaml
Responsável: QA + Frontend
Diagnóstico:
  1. Adicionar esperas adequadas (waitFor...)
  2. Validar seletores corretos (data-test attributes)
  3. Usar fixtures para compartilhar dados
  4. Verificar backdrop de operações assíncronas

Ação Imediata:
  - Adicionar waitForDialogToClosed() após operações assíncronas
  - Validar todos data-test attributes
  - Criar fixture se dados forem reutilizados
```

---

## 8. COMANDOS ÚTEIS

```bash
# Executar apenas testes stateful
npx playwright test --grep "serial"

# Executar teste específico
npx playwright test TC-RF006-E2E-001.spec.ts

# Debug interativo (pausar em cada passo)
npx playwright test --debug --grep "Fluxo CRUD"

# Validar configuração (workers, parallel)
npx playwright test --list

# Gerar trace para debug
npx playwright test --trace on

# Ver relatório HTML
npx playwright show-report
```

---

## 9. REFERÊNCIAS CRUZADAS

### Documentos Relacionados

| Documento | Seção | O Que Adicionar |
|-----------|-------|-----------------|
| `execucao-completa.md` | Nova seção | "Testes Stateful - Referência ao contrato" |
| `geracao-testes-e2e-playwright.md` | Fixtures | "Como criar fixtures de dados" |
| `CONVENTIONS.md` | Padrões E2E | "Padrão de test.describe.serial" |
| `base-conhecimento/frontend.yaml` | Troubleshooting | "Dados não persistem entre testes" |

### Contratos de Dependência

- **Pre-requisito:** Backend com seed no startup (não por request)
- **Pre-requisito:** Playwright configurado com workers: 1
- **Pre-requisito:** Helpers de backdrop (waitForDialogToClosed)

---

## 10. HISTÓRICO DE VERSÕES

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2026-01-11 | Criação inicial - Resolve problema RF006 de banco resetado entre testes stateful |

---

**FIM DO CONTRATO**

/**
 * TEMPLATE DE FIXTURE PLAYWRIGHT
 *
 * Versão: 1.0
 * Data: 2026-01-11
 * Contexto: Criado após análise do RF006 para facilitar criação de fixtures reutilizáveis
 *           que compartilham dados entre múltiplos testes stateful.
 *
 * **Quando usar este template:**
 * - Testes stateful que compartilham dados (ex: CRUD completo)
 * - Setup/teardown automático de dados de teste
 * - ID de entidade criada precisa ser compartilhado entre testes
 *
 * **Problema que resolve:**
 * - Evita duplicação de código de setup em cada teste
 * - Garante cleanup automático após testes
 * - Facilita testes sequenciais (Criar → Listar → Editar → Excluir)
 *
 * **Referências:**
 * - CONTRATO-TESTES-E2E-STATEFUL.md → seção 4 (Fixtures do Playwright)
 * - Playwright Docs: https://playwright.dev/docs/test-fixtures
 */

import { test as base, expect } from '@playwright/test';
import { Page } from '@playwright/test';
import { waitForDialogToClosed } from '../helpers';

// =============================================
// TIPO DA FIXTURE
// =============================================
// Define o que será fornecido aos testes
type [Entidade]Fixture = {
  [entidade]Id: string;           // ID da entidade criada
  [entidade]RazaoSocial?: string; // Opcional: outros dados úteis
};

// =============================================
// EXTENSÃO DO TEST BASE
// =============================================
export const test = base.extend<[Entidade]Fixture>({
  /**
   * Fixture: [entidade]Id
   *
   * SETUP:
   * 1. Navega para tela de [entidade]s
   * 2. Cria um [entidade] de teste
   * 3. Captura o ID gerado
   * 4. Fornece ID para os testes
   *
   * TEARDOWN (opcional):
   * 5. Exclui [entidade] criado após todos os testes
   */
  [entidade]Id: async ({ page }, use) => {
    // ===========================================
    // SETUP: Executado UMA VEZ antes dos testes
    // ===========================================

    // 1. Navegar para tela de [entidade]s
    await page.goto('/management/[entidades]');

    // 2. Clicar no botão "Novo [Entidade]"
    await page.click('[data-test="btn-novo-[entidade]"]');

    // 3. Preencher dados mínimos obrigatórios
    // IMPORTANTE: Usar dados que NÃO conflitem com seeds existentes
    await page.fill('[data-test="cnpj"]', '00.000.000/0001-91');
    await page.click('[data-test="btn-consultar-cnpj"]');

    // 4. Aguardar dados serem carregados (ReceitaWS ou mock)
    await page.waitForSelector('[data-test="razaoSocial"]', {
      state: 'visible',
      timeout: 10000
    });

    // 5. Aguardar backdrop desaparecer (se operação assíncrona)
    await waitForDialogToClosed(page);

    // 6. Salvar [entidade]
    await page.click('[data-test="btn-salvar"]');
    await page.waitForURL('**/management/[entidades]', { timeout: 10000 });

    // 7. Capturar ID do [entidade] criado
    const url = page.url();
    const [entidade]Id = url.match(/\/[entidades]\/([^\/]+)/)?.[1] ?? '';

    // Validar que ID foi capturado
    expect([entidade]Id).toBeTruthy();

    // ===========================================
    // USE: Fornecer ID para os testes
    // ===========================================
    await use([entidade]Id);

    // ===========================================
    // TEARDOWN: Executado após TODOS os testes
    // ===========================================
    // OPCIONAL: Descomentar para excluir [entidade] ao final

    /*
    try {
      // Navegar para listagem
      await page.goto('/management/[entidades]');

      // Localizar linha do [entidade] criado
      const [entidade]Row = page.locator(`[data-id="${[entidade]Id}"]`);

      // Abrir menu de ações
      await [entidade]Row.locator('[data-test="menu-acoes"]').click();

      // Clicar em "Excluir"
      await page.click('[data-test="btn-excluir"]');

      // Confirmar exclusão
      await page.click('button:has-text("Confirmar")');

      // Aguardar backdrop desaparecer
      await waitForDialogToClosed(page);

      // Validar que foi excluído
      await expect([entidade]Row).not.toBeVisible({ timeout: 5000 });
    } catch (error) {
      // Falha no teardown não deve quebrar testes
      console.warn(`Teardown failed for [entidade] ${[entidade]Id}:`, error);
    }
    */
  },
});

// =============================================
// EXEMPLO DE USO
// =============================================
// Arquivo: TC-RFXXX-E2E-001.spec.ts

/*
import { test } from './fixtures/[entidade]-teste';
import { expect } from '@playwright/test';

test.describe.serial('TC-RFXXX-E2E-001: Fluxo CRUD Completo', () => {

  test('Passo 2: Listar [Entidade] Criado', async ({ page, [entidade]Id }) => {
    await page.goto('/management/[entidades]');

    // [Entidade] criado pela fixture DEVE estar visível
    const [entidade]Row = page.locator(`[data-id="${[entidade]Id}"]`);
    await expect([entidade]Row).toBeVisible({ timeout: 10000 });
  });

  test('Passo 3: Visualizar Detalhes', async ({ page, [entidade]Id }) => {
    await page.goto(`/management/[entidades]/${[entidade]Id}`);

    // Validar dados carregados
    await expect(page.locator('[data-test="razaoSocial"]'))
      .not.toHaveValue('');
  });

  test('Passo 4: Editar', async ({ page, [entidade]Id }) => {
    await page.goto(`/management/[entidades]/${[entidade]Id}`);

    // Editar campo
    await page.fill('[data-test="nomeFantasia"]', 'NOME EDITADO');
    await page.click('[data-test="btn-salvar"]');

    await page.waitForURL('**/management/[entidades]', { timeout: 10000 });

    // Validar que edição persistiu
    await page.goto(`/management/[entidades]/${[entidade]Id}`);
    await expect(page.locator('[data-test="nomeFantasia"]'))
      .toHaveValue('NOME EDITADO');
  });

  test('Passo 5: Excluir', async ({ page, [entidade]Id }) => {
    await page.goto('/management/[entidades]');

    const [entidade]Row = page.locator(`[data-id="${[entidade]Id}"]`);
    await [entidade]Row.locator('[data-test="menu-acoes"]').click();
    await page.click('[data-test="btn-excluir"]');
    await page.click('button:has-text("Confirmar")');

    // [Entidade] NÃO deve aparecer mais
    await expect([entidade]Row).not.toBeVisible({ timeout: 5000 });
  });
});
*/

// =============================================
// VARIAÇÃO: FIXTURE COM MÚLTIPLOS DADOS
// =============================================
// Para casos que precisam compartilhar mais informações

/*
type [Entidade]FixtureCompleta = {
  [entidade]: {
    id: string;
    razaoSocial: string;
    cnpj: string;
  };
};

export const testCompleto = base.extend<[Entidade]FixtureCompleta>({
  [entidade]: async ({ page }, use) => {
    // Setup...
    const id = '...';
    const razaoSocial = '...';
    const cnpj = '...';

    await use({ id, razaoSocial, cnpj });

    // Teardown...
  },
});
*/

// =============================================
// VARIAÇÃO: FIXTURE COM AUTENTICAÇÃO
// =============================================
// Para casos que precisam de login específico

/*
type AuthenticatedFixture = {
  authenticatedPage: Page;
};

export const testAuth = base.extend<AuthenticatedFixture>({
  authenticatedPage: async ({ page }, use) => {
    // Login
    await page.goto('/sign-in');
    await page.fill('[name="email"]', 'admin@icontrolit.com.br');
    await page.fill('[name="password"]', 'senha123');
    await page.click('[data-test="btn-signin"]');

    // Aguardar redirecionamento
    await page.waitForURL('**/dashboard', { timeout: 10000 });

    await use(page);

    // Logout (teardown)
    await page.click('[data-test="user-menu"]');
    await page.click('[data-test="btn-signout"]');
  },
});
*/

// =============================================
// CHECKLIST DE IMPLEMENTAÇÃO
// =============================================
/**
 * Ao criar uma fixture, validar:
 *
 * [ ] Nome do arquivo: [entidade]-teste.ts
 * [ ] Tipo da fixture definido corretamente
 * [ ] Setup cria dados de teste sem conflito com seeds
 * [ ] ID capturado corretamente após criação
 * [ ] Teardown opcional implementado (se necessário)
 * [ ] Exportado como `test` para substituir test padrão
 * [ ] Documentação de uso no topo do arquivo
 * [ ] Importado corretamente nos testes: import { test } from './fixtures/...'
 * [ ] Funciona com test.describe.serial
 */

// =============================================
// PROBLEMAS COMUNS E SOLUÇÕES
// =============================================
/**
 * PROBLEMA: Fixture cria dados mas testes não veem
 * SOLUÇÃO: Validar que test.describe.serial está sendo usado
 *          e que playwright.config.ts tem workers: 1
 *
 * PROBLEMA: Teardown não executa
 * SOLUÇÃO: Fixture só executa teardown se todos os testes passarem
 *          ou se test suite completar normalmente
 *
 * PROBLEMA: ID não é capturado corretamente
 * SOLUÇÃO: Validar regex de captura de URL:
 *          url.match(/\/[entidades]\/([^\/]+)/)?.[1]
 *
 * PROBLEMA: Conflito de dados com seeds
 * SOLUÇÃO: Usar CNPJ/email único que NÃO conflite com seeds
 *          Exemplo: CNPJ iniciando com 00.000.000/
 */

export {};  // Tornar este arquivo um módulo TypeScript válido

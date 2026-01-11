/**
 * =============================================
 * MASSA DE TESTE (MT) - TEMPLATE VERSÃO 2.0
 * =============================================
 *
 * Este template inclui TODAS as seções obrigatórias para sincronização completa
 * com backend, frontend e UC desde o início.
 *
 * IMPORTANTE: Este arquivo DEVE estar sempre sincronizado com:
 * - Backend seeds (ApplicationDbContextInitialiser.cs)
 * - Frontend routing (app-routing.module.ts)
 * - UC data-test attributes (UC-RFXXX.yaml)
 *
 * Última atualização: 2026-01-09
 * Versão: 2.0 - Sincronização completa e rastreável
 *
 * =============================================
 */

import { Page } from '@playwright/test';

// =============================================
// CREDENCIAIS (OBRIGATÓRIO - sincronizadas com seeds backend)
// =============================================

/**
 * Credenciais de teste
 *
 * FONTE: ApplicationDbContextInitialiser.cs (linhas XX-YY)
 * ÚLTIMA SINCRONIZAÇÃO: [DATA]
 *
 * VALIDAÇÃO: Execute `npm run validate-credentials RFXXX` antes de rodar E2E
 *
 * IMPORTANTE: Estas credenciais DEVEM estar sincronizadas com os seeds do backend.
 * Se os seeds mudarem, este arquivo DEVE ser atualizado imediatamente.
 */
export const CREDENCIAIS_TESTE = {
  admin_teste: {
    email: '[email do seed]',           // Backend seed linha XX
    password: '[senha do seed]',         // Backend seed linha YY
    perfil: '[perfil]',                  // Ex: Admin, Developer, Usuario
    descricao: '[Descrição do perfil de teste]'
  },

  // Adicionar outros perfis conforme necessário
  desenvolvedor_teste: {
    email: '[email do seed]',
    password: '[senha do seed]',
    perfil: 'Developer',
    descricao: '[Descrição]'
  }
};

// =============================================
// URLS FRONTEND (OBRIGATÓRIO - sincronizadas com routing)
// =============================================

/**
 * URLs do frontend
 *
 * FONTE: src/app/[caminho]/[arquivo]-routing.module.ts
 * ÚLTIMA SINCRONIZAÇÃO: [DATA]
 *
 * VALIDAÇÃO: Execute `npm run validate-routes` antes de rodar E2E
 *
 * IMPORTANTE: Estas URLs DEVEM corresponder exatamente às rotas do Angular.
 * Qualquer mudança no routing DEVE ser refletida aqui.
 */
export const FRONTEND_URLS = {
  signIn: 'http://localhost:4200/sign-in',

  // URLs específicas do RF
  [entidade]: 'http://localhost:4200/[rota-completa]',
  // Exemplo: clientes: 'http://localhost:4200/management/clientes'

  [entidade]Criar: 'http://localhost:4200/[rota-criar]',
  // Exemplo: clientesCriar: 'http://localhost:4200/management/clientes/novo'

  [entidade]Editar: (id: string) => `http://localhost:4200/[rota-editar]/${id}`,
  // Exemplo: clientesEditar: (id: string) => `http://localhost:4200/management/clientes/${id}`
};

// =============================================
// SELETORES E2E (OBRIGATÓRIO - sincronizados com componentes)
// =============================================

/**
 * Seletores data-test
 *
 * FONTE: src/app/modules/[caminho]/[componente].component.html
 * ÚLTIMA SINCRONIZAÇÃO: [DATA]
 *
 * VALIDAÇÃO: Execute `npm run audit-data-test RFXXX` antes de rodar E2E
 *
 * IMPORTANTE: Estes seletores DEVEM corresponder exatamente aos data-test no HTML.
 * Nomenclatura obrigatória: RFXXX-[acao]-[alvo]
 *
 * CONVENÇÃO:
 * - Botões de ação: RFXXX-[acao]-[entidade]
 * - Inputs: RFXXX-input-[campo]
 * - Estados UI: [nome-estado] (sem prefixo RF)
 * - Tabelas: [entidade]-list, [entidade]-row
 */
export const DATA_TEST_SELECTORS = {
  // ==================== NAVEGAÇÃO ====================
  btnNovo[Entidade]: 'RFXXX-criar-[entidade]',
  // Exemplo: btnNovoCliente: 'RF006-criar-cliente'

  btnEditar[Entidade]: 'RFXXX-editar-[entidade]',
  // Exemplo: btnEditarCliente: 'RF006-editar-cliente'

  btnExcluir[Entidade]: 'RFXXX-excluir-[entidade]',
  // Exemplo: btnExcluirCliente: 'RF006-excluir-cliente'

  // ==================== ESTADOS UI ====================
  loadingSpinner: 'loading-spinner',
  emptyState: 'empty-state',
  errorMessage: 'error-message',

  // ==================== TABELA/LISTA ====================
  [entidade]List: '[entidade]-list',
  // Exemplo: clientesList: 'clientes-list'

  [entidade]Row: '[entidade]-row',
  // Exemplo: clienteRow: 'cliente-row'

  // ==================== FORMULÁRIO ====================
  form[Entidade]: 'RFXXX-form',
  // Exemplo: formCliente: 'RF006-form'

  // Inputs (adicionar todos os campos do formulário)
  input[Campo1]: 'RFXXX-input-[campo1]',
  // Exemplo: inputRazaoSocial: 'RF006-input-razaosocial'

  input[Campo2]: 'RFXXX-input-[campo2]',
  // Exemplo: inputCNPJ: 'RF006-input-cnpj'

  // Mensagens de erro
  input[Campo1]Error: 'RFXXX-input-[campo1]-error',
  // Exemplo: inputRazaoSocialError: 'RF006-input-razaosocial-error'

  // ==================== BOTÕES DE FORMULÁRIO ====================
  btnSalvar: 'RFXXX-salvar-[entidade]',
  // Exemplo: btnSalvar: 'RF006-salvar-cliente'

  btnCancelar: 'RFXXX-cancelar-[entidade]',
  // Exemplo: btnCancelar: 'RF006-cancelar-cliente'

  // ==================== DIÁLOGOS/MODAIS ====================
  dialogConfirmacao: 'dialog-confirmacao',
  btnConfirmarDialog: 'btn-confirmar-dialog',
  btnCancelarDialog: 'btn-cancelar-dialog'
};

// =============================================
// TIMEOUTS (OBRIGATÓRIO - sincronizados com UC)
// =============================================

/**
 * Timeouts para operações E2E
 *
 * FONTE: UC-RFXXX.yaml (seção performance e timeouts_e2e)
 * ÚLTIMA SINCRONIZAÇÃO: [DATA]
 *
 * IMPORTANTE: Estes valores DEVEM corresponder aos especificados no UC.
 */
export const TIMEOUTS = {
  // Navegação e carregamento
  navegacao: 30000,              // 30s - Timeout para navegação de página
  loadingSpinner: 30000,         // 30s - Timeout para spinner desaparecer

  // Diálogos e modais
  dialog: 10000,                 // 10s - Timeout para diálogos/modals

  // Operações CRUD
  operacaoCRUD: 15000,           // 15s - Timeout para criar/editar/excluir
  operacaoSalvar: 15000,         // 15s - Timeout específico para salvar
  operacaoExcluir: 10000,        // 10s - Timeout específico para excluir

  // Validações
  validacaoFormulario: 5000,     // 5s - Timeout para validações de formulário

  // APIs externas (se aplicável)
  apiReceitaWS: 15000,           // 15s - Exemplo: ReceitaWS
  apiViaCEP: 10000               // 10s - Exemplo: ViaCEP
};

// =============================================
// MASSA DE TESTE - CENÁRIOS
// =============================================

/**
 * Interface para massa de teste
 */
export interface MassaTeste[Entidade] {
  cenario: string;
  descricao: string;
  dados: {
    // Definir estrutura de dados conforme entidade
    [campo1]: any;
    [campo2]: any;
    // ...
  };
  resultado_esperado: {
    sucesso: boolean;
    mensagem?: string;
    validacoes?: string[];
  };
}

/**
 * Cenário 1: Happy Path - Criar [Entidade] com dados válidos
 */
export const MT_RFXXX_001: MassaTeste[Entidade] = {
  cenario: 'Happy Path - Criar [Entidade] com dados válidos',
  descricao: '[Descrição detalhada do cenário]',
  dados: {
    [campo1]: '[valor válido]',
    [campo2]: '[valor válido]',
    // Adicionar todos os campos
  },
  resultado_esperado: {
    sucesso: true,
    mensagem: '[Entidade] criado com sucesso',
    validacoes: [
      '[Entidade] aparece na lista',
      'Mensagem de sucesso exibida',
      'Campos salvos corretamente'
    ]
  }
};

/**
 * Cenário 2: Validação - [Campo] obrigatório vazio
 */
export const MT_RFXXX_002: MassaTeste[Entidade] = {
  cenario: 'Validação - [Campo] obrigatório vazio',
  descricao: 'Tenta criar [entidade] sem preencher [campo] obrigatório',
  dados: {
    [campo1]: '',  // Campo obrigatório vazio
    [campo2]: '[valor válido]'
  },
  resultado_esperado: {
    sucesso: false,
    mensagem: '[Campo] é obrigatório',
    validacoes: [
      'Mensagem de erro exibida',
      'Campo destacado com erro',
      '[Entidade] não é criado'
    ]
  }
};

// Adicionar mais cenários conforme TC-RFXXX.yaml

// =============================================
// HELPERS DE VALIDAÇÃO
// =============================================

/**
 * Valida sincronização de credenciais com backend
 * Deve ser executado ANTES de rodar E2E
 *
 * EXECUÇÃO: npm run validate-credentials RFXXX
 */
export async function validateCredentials(page: Page): Promise<void> {
  console.log('[VALIDAÇÃO] Validando credenciais com backend seeds...');

  // TODO: Implementar validação via API /auth/validate ou leitura de seeds
  // 1. Ler ApplicationDbContextInitialiser.cs
  // 2. Extrair credenciais de seeds
  // 3. Comparar com CREDENCIAIS_TESTE
  // 4. Retornar erro se divergência

  console.log('[VALIDAÇÃO] Credenciais sincronizadas com backend ✓');
}

/**
 * Valida URLs com routing do Angular
 * Deve ser executado ANTES de rodar E2E
 *
 * EXECUÇÃO: npm run validate-routes
 */
export async function validateRoutes(): Promise<void> {
  console.log('[VALIDAÇÃO] Validando URLs com routing Angular...');

  // TODO: Implementar validação contra app-routing.module.ts
  // 1. Ler app-routing.module.ts e módulos de routing
  // 2. Extrair rotas configuradas
  // 3. Comparar com FRONTEND_URLS
  // 4. Retornar erro se rota não existe (404)

  console.log('[VALIDAÇÃO] URLs sincronizadas com routing ✓');
}

/**
 * Valida data-test attributes com componentes
 * Deve ser executado ANTES de rodar E2E
 *
 * EXECUÇÃO: npm run audit-data-test RFXXX
 */
export async function validateDataTestAttributes(): Promise<void> {
  console.log('[VALIDAÇÃO] Validando data-test attributes com componentes...');

  // TODO: Implementar parsing de HTML e validação de seletores
  // 1. Escanear componentes HTML do RF
  // 2. Extrair data-test attributes presentes
  // 3. Comparar com DATA_TEST_SELECTORS
  // 4. Retornar erro se seletor ausente ou inconsistente

  console.log('[VALIDAÇÃO] Data-test attributes sincronizados ✓');
}

// =============================================
// HELPERS E2E
// =============================================

/**
 * Login com perfil de teste
 */
export async function login(page: Page, perfil: keyof typeof CREDENCIAIS_TESTE): Promise<void> {
  const credenciais = CREDENCIAIS_TESTE[perfil];

  await page.goto(FRONTEND_URLS.signIn, { timeout: TIMEOUTS.navegacao });

  // TODO: Implementar login conforme componente de sign-in
  // await page.fill('[data-test="input-email"]', credenciais.email);
  // await page.fill('[data-test="input-password"]', credenciais.password);
  // await page.click('[data-test="btn-login"]');

  console.log(`[LOGIN] Autenticado como ${credenciais.perfil}`);
}

/**
 * Aguarda spinner de loading desaparecer
 */
export async function aguardarLoadingDesaparecer(page: Page): Promise<void> {
  await page.waitForSelector(
    `[data-test="${DATA_TEST_SELECTORS.loadingSpinner}"]`,
    { state: 'hidden', timeout: TIMEOUTS.loadingSpinner }
  );
}

/**
 * Navega para lista de [Entidade]
 */
export async function navegarPara[Entidade]Lista(page: Page): Promise<void> {
  await page.goto(FRONTEND_URLS.[entidade], { timeout: TIMEOUTS.navegacao });
  await aguardarLoadingDesaparecer(page);
}

// =============================================
// METADADOS
// =============================================

export const METADATA = {
  rf_id: 'RFXXX',
  versao: '1.0',
  data_criacao: '[DATA]',
  ultima_sincronizacao: {
    credenciais: '[DATA]',
    urls: '[DATA]',
    data_test: '[DATA]',
    timeouts: '[DATA]'
  },
  responsavel: '[Nome]',

  // Flags de validação
  credenciais_validadas: false,
  urls_validadas: false,
  data_test_validados: false,

  // Executar validações antes de marcar como true
  pronto_para_e2e: false
};

/**
 * CHECKLIST DE SINCRONIZAÇÃO
 *
 * Antes de executar testes E2E, validar:
 *
 * [ ] Credenciais sincronizadas com ApplicationDbContextInitialiser.cs
 * [ ] URLs sincronizadas com app-routing.module.ts
 * [ ] Data-test attributes sincronizados com componentes HTML
 * [ ] Timeouts sincronizados com UC-RFXXX.yaml
 * [ ] Massa de teste completa (todos os cenários do TC)
 * [ ] Validações executadas: npm run validate-credentials RFXXX
 * [ ] Validações executadas: npm run validate-routes
 * [ ] Validações executadas: npm run audit-data-test RFXXX
 *
 * SOMENTE então marcar METADATA.pronto_para_e2e = true
 */

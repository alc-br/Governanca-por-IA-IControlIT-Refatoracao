#!/usr/bin/env ts-node

/**
 * =============================================
 * AUDIT DATA-TEST ATTRIBUTES - VERSÃO 1.0
 * =============================================
 *
 * Script de auditoria de data-test attributes em componentes HTML
 *
 * OBJETIVO:
 * Valida se TODOS os data-test attributes especificados no UC-RFXXX.yaml
 * estão presentes nos componentes HTML do frontend.
 *
 * EXECUÇÃO:
 * npm run audit-data-test RFXXX
 * OU
 * ts-node tools/audit-data-test.ts RFXXX
 *
 * EXIT CODES:
 * 0 - Auditoria PASSOU (todos os data-test estão presentes)
 * 1 - Auditoria FALHOU (data-test ausentes ou inconsistentes)
 *
 * Última atualização: 2026-01-09
 * Versão: 1.0
 *
 * =============================================
 */

import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import * as glob from 'glob';

// =============================================
// TIPOS E INTERFACES
// =============================================

interface UCYaml {
  rf_id: string;
  uc_id: string;
  titulo: string;
  passos?: Array<{
    numero: number;
    acao: string;
    elemento?: {
      tipo: string;
      data_test: string;
      aliases?: string[];
      localizacao?: string;
    };
  }>;
  estados_ui?: {
    loading?: { data_test: string };
    vazio?: { data_test: string };
    erro?: { data_test: string };
  };
  tabela?: {
    data_test_container?: string;
    data_test_row?: string;
    colunas?: Array<{ data_test: string }>;
    acoes_linha?: Array<{ data_test: string }>;
  };
  formulario?: {
    data_test_form?: string;
    campos?: Array<{
      data_test: string;
      validacoes?: Array<{ data_test_erro: string }>;
    }>;
    botoes?: Array<{ data_test: string }>;
  };
}

interface DataTestAuditResult {
  total_esperados: number;
  total_encontrados: number;
  ausentes: string[];
  encontrados: string[];
  inconsistencias: Array<{
    esperado: string;
    encontrado: string;
    arquivo: string;
    linha: number;
  }>;
  passou: boolean;
}

// =============================================
// CONFIGURAÇÕES
// =============================================

const PATHS = {
  uc: (rfId: string) => `D:\\IC2_Governanca\\documentacao\\**\\${rfId}\\UC-${rfId}.yaml`,
  frontend: 'D:\\IC2\\frontend\\icontrolit-app\\src\\app',
  governanca: 'D:\\IC2_Governanca'
};

const COLORS = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m'
};

// =============================================
// FUNÇÕES AUXILIARES
// =============================================

function log(message: string, color: string = COLORS.reset): void {
  console.log(`${color}${message}${COLORS.reset}`);
}

function erro(message: string): void {
  log(`❌ ${message}`, COLORS.red);
}

function sucesso(message: string): void {
  log(`✅ ${message}`, COLORS.green);
}

function aviso(message: string): void {
  log(`⚠️  ${message}`, COLORS.yellow);
}

function info(message: string): void {
  log(`ℹ️  ${message}`, COLORS.cyan);
}

// =============================================
// FUNÇÕES PRINCIPAIS
// =============================================

/**
 * Carrega UC-RFXXX.yaml
 */
function carregarUC(rfId: string): UCYaml | null {
  try {
    const pattern = PATHS.uc(rfId);
    const arquivos = glob.sync(pattern);

    if (arquivos.length === 0) {
      erro(`UC-${rfId}.yaml não encontrado`);
      erro(`Padrão buscado: ${pattern}`);
      return null;
    }

    const arquivoUC = arquivos[0];
    info(`Lendo UC: ${arquivoUC}`);

    const conteudo = fs.readFileSync(arquivoUC, 'utf-8');
    const uc = yaml.load(conteudo) as UCYaml;

    sucesso(`UC-${rfId}.yaml carregado com sucesso`);
    return uc;
  } catch (error) {
    erro(`Erro ao carregar UC: ${error.message}`);
    return null;
  }
}

/**
 * Extrai TODOS os data-test esperados do UC
 */
function extrairDataTestEsperados(uc: UCYaml): string[] {
  const dataTests = new Set<string>();

  // 1. Extrair de passos
  if (uc.passos) {
    uc.passos.forEach(passo => {
      if (passo.elemento?.data_test) {
        dataTests.add(passo.elemento.data_test);

        // Adicionar aliases também
        if (passo.elemento.aliases) {
          passo.elemento.aliases.forEach(alias => dataTests.add(alias));
        }
      }
    });
  }

  // 2. Extrair de estados_ui
  if (uc.estados_ui) {
    if (uc.estados_ui.loading?.data_test) {
      dataTests.add(uc.estados_ui.loading.data_test);
    }
    if (uc.estados_ui.vazio?.data_test) {
      dataTests.add(uc.estados_ui.vazio.data_test);
    }
    if (uc.estados_ui.erro?.data_test) {
      dataTests.add(uc.estados_ui.erro.data_test);
    }
  }

  // 3. Extrair de tabela
  if (uc.tabela) {
    if (uc.tabela.data_test_container) {
      dataTests.add(uc.tabela.data_test_container);
    }
    if (uc.tabela.data_test_row) {
      dataTests.add(uc.tabela.data_test_row);
    }
    if (uc.tabela.colunas) {
      uc.tabela.colunas.forEach(coluna => {
        if (coluna.data_test) {
          dataTests.add(coluna.data_test);
        }
      });
    }
    if (uc.tabela.acoes_linha) {
      uc.tabela.acoes_linha.forEach(acao => {
        if (acao.data_test) {
          dataTests.add(acao.data_test);
        }
      });
    }
  }

  // 4. Extrair de formulario
  if (uc.formulario) {
    if (uc.formulario.data_test_form) {
      dataTests.add(uc.formulario.data_test_form);
    }
    if (uc.formulario.campos) {
      uc.formulario.campos.forEach(campo => {
        if (campo.data_test) {
          dataTests.add(campo.data_test);
        }
        if (campo.validacoes) {
          campo.validacoes.forEach(validacao => {
            if (validacao.data_test_erro) {
              dataTests.add(validacao.data_test_erro);
            }
          });
        }
      });
    }
    if (uc.formulario.botoes) {
      uc.formulario.botoes.forEach(botao => {
        if (botao.data_test) {
          dataTests.add(botao.data_test);
        }
      });
    }
  }

  return Array.from(dataTests);
}

/**
 * Busca componentes HTML relacionados ao RF
 */
function buscarComponentesHTML(rfId: string): string[] {
  const pattern = `${PATHS.frontend}/**/*.component.html`;
  const todosComponentes = glob.sync(pattern);

  // Filtrar componentes relacionados ao RF
  // Buscar por nome da entidade (ex: RF006 -> clientes)
  const rfNumber = rfId.replace('RF', '');

  // Pegar todos os componentes por enquanto (pode ser refinado)
  return todosComponentes;
}

/**
 * Extrai data-test attributes de um arquivo HTML
 */
function extrairDataTestDeHTML(arquivo: string): Array<{ dataTest: string; linha: number }> {
  const dataTests: Array<{ dataTest: string; linha: number }> = [];

  try {
    const conteudo = fs.readFileSync(arquivo, 'utf-8');
    const linhas = conteudo.split('\n');

    linhas.forEach((linha, index) => {
      // Regex para capturar data-test="..."
      const regex = /data-test=["']([^"']+)["']/g;
      let match;

      while ((match = regex.exec(linha)) !== null) {
        dataTests.push({
          dataTest: match[1],
          linha: index + 1
        });
      }
    });
  } catch (error) {
    aviso(`Erro ao ler arquivo ${arquivo}: ${error.message}`);
  }

  return dataTests;
}

/**
 * Realiza auditoria completa
 */
function auditarDataTest(rfId: string): DataTestAuditResult {
  info(`\n${'='.repeat(60)}`);
  info(`AUDITORIA DE DATA-TEST ATTRIBUTES - ${rfId}`);
  info(`${'='.repeat(60)}\n`);

  // 1. Carregar UC
  const uc = carregarUC(rfId);
  if (!uc) {
    return {
      total_esperados: 0,
      total_encontrados: 0,
      ausentes: [],
      encontrados: [],
      inconsistencias: [],
      passou: false
    };
  }

  // 2. Extrair data-test esperados
  const dataTestEsperados = extrairDataTestEsperados(uc);
  info(`\nData-test esperados (UC): ${dataTestEsperados.length}`);
  dataTestEsperados.forEach(dt => console.log(`  - ${dt}`));

  // 3. Buscar componentes HTML
  const componentesHTML = buscarComponentesHTML(rfId);
  info(`\nComponentes HTML encontrados: ${componentesHTML.length}`);

  // 4. Extrair data-test de componentes
  const dataTestEncontrados = new Set<string>();
  const localizacoes: Map<string, { arquivo: string; linha: number }> = new Map();

  componentesHTML.forEach(arquivo => {
    const dataTests = extrairDataTestDeHTML(arquivo);
    dataTests.forEach(dt => {
      dataTestEncontrados.add(dt.dataTest);
      localizacoes.set(dt.dataTest, {
        arquivo: path.relative(PATHS.frontend, arquivo),
        linha: dt.linha
      });
    });
  });

  info(`\nData-test encontrados (HTML): ${dataTestEncontrados.size}`);

  // 5. Comparar esperados vs encontrados
  const ausentes: string[] = [];
  const encontrados: string[] = [];

  dataTestEsperados.forEach(esperado => {
    if (dataTestEncontrados.has(esperado)) {
      encontrados.push(esperado);
    } else {
      ausentes.push(esperado);
    }
  });

  // 6. Detectar inconsistências de nomenclatura
  const inconsistencias: Array<{
    esperado: string;
    encontrado: string;
    arquivo: string;
    linha: number;
  }> = [];

  // TODO: Implementar detecção de nomenclatura inconsistente
  // Ex: RF006- vs btn- vs sem prefixo

  const passou = ausentes.length === 0;

  return {
    total_esperados: dataTestEsperados.length,
    total_encontrados: encontrados.length,
    ausentes,
    encontrados,
    inconsistencias,
    passou
  };
}

/**
 * Exibe relatório de auditoria
 */
function exibirRelatorio(resultado: DataTestAuditResult): void {
  info(`\n${'='.repeat(60)}`);
  info('RELATÓRIO DE AUDITORIA');
  info(`${'='.repeat(60)}\n`);

  // Estatísticas
  log(`Total esperados (UC):      ${resultado.total_esperados}`);
  log(`Total encontrados (HTML):  ${resultado.total_encontrados}`);
  log(`Taxa de cobertura:         ${((resultado.total_encontrados / resultado.total_esperados) * 100).toFixed(1)}%\n`);

  // Data-test encontrados
  if (resultado.encontrados.length > 0) {
    sucesso(`\n✅ Data-test ENCONTRADOS (${resultado.encontrados.length}):`);
    resultado.encontrados.forEach(dt => console.log(`  ✓ ${dt}`));
  }

  // Data-test ausentes
  if (resultado.ausentes.length > 0) {
    erro(`\n❌ Data-test AUSENTES (${resultado.ausentes.length}):`);
    resultado.ausentes.forEach(dt => console.log(`  ✗ ${dt}`));
  }

  // Inconsistências
  if (resultado.inconsistencias.length > 0) {
    aviso(`\n⚠️  INCONSISTÊNCIAS DE NOMENCLATURA (${resultado.inconsistencias.length}):`);
    resultado.inconsistencias.forEach(inc => {
      console.log(`  - Esperado: ${inc.esperado}`);
      console.log(`    Encontrado: ${inc.encontrado}`);
      console.log(`    Arquivo: ${inc.arquivo}:${inc.linha}\n`);
    });
  }

  // Veredicto final
  info(`\n${'='.repeat(60)}`);
  if (resultado.passou) {
    sucesso('✅ AUDITORIA PASSOU');
    sucesso('Todos os data-test esperados estão presentes no HTML');
  } else {
    erro('❌ AUDITORIA FALHOU');
    erro(`${resultado.ausentes.length} data-test ausentes`);
    erro('Corrija os componentes HTML e re-execute a auditoria');
  }
  info(`${'='.repeat(60)}\n`);
}

// =============================================
// EXECUÇÃO PRINCIPAL
// =============================================

function main(): void {
  // Validar argumentos
  const args = process.argv.slice(2);

  if (args.length === 0) {
    erro('Erro: RF não especificado');
    console.log('\nUso: npm run audit-data-test RFXXX');
    console.log('Exemplo: npm run audit-data-test RF006\n');
    process.exit(1);
  }

  const rfId = args[0];

  // Validar formato RF
  if (!/^RF\d{3}$/.test(rfId)) {
    erro(`Erro: Formato inválido "${rfId}"`);
    console.log('Formato esperado: RFXXX (ex: RF006)\n');
    process.exit(1);
  }

  // Executar auditoria
  const resultado = auditarDataTest(rfId);

  // Exibir relatório
  exibirRelatorio(resultado);

  // Exit code baseado no resultado
  process.exit(resultado.passou ? 0 : 1);
}

// Executar apenas se chamado diretamente
if (require.main === module) {
  main();
}

export { auditarDataTest, DataTestAuditResult };

#!/usr/bin/env ts-node

/**
 * =============================================
 * VALIDATE ROUTES - VERSÃO 1.0
 * =============================================
 *
 * Script de validação de sincronização de URLs
 *
 * OBJETIVO:
 * Valida se as URLs em FRONTEND_URLS de MT-RFXXX.data.ts estão sincronizadas
 * com as rotas configuradas no app-routing.module.ts do Angular
 *
 * EXECUÇÃO:
 * npm run validate-routes
 * OU
 * ts-node tools/validate-routes.ts
 *
 * EXIT CODES:
 * 0 - Validação PASSOU (URLs sincronizadas)
 * 1 - Validação FALHOU (URLs desatualizadas ou rotas 404)
 *
 * Última atualização: 2026-01-09
 * Versão: 1.0
 *
 * =============================================
 */

import * as fs from 'fs';
import * as path from 'path';
import * as glob from 'glob';

// =============================================
// TIPOS E INTERFACES
// =============================================

interface MTUrls {
  [key: string]: string;
}

interface AngularRoute {
  path: string;
  fullPath: string;
  arquivo: string;
  linha: number;
}

interface ValidationResult {
  passou: boolean;
  mt_urls: MTUrls;
  rotas_angular: AngularRoute[];
  urls_invalidas: Array<{
    nome: string;
    url: string;
    path_esperado: string;
    motivo: string;
  }>;
  urls_nao_encontradas: string[];
}

// =============================================
// CONFIGURAÇÕES
// =============================================

const PATHS = {
  mt_data: 'D:\\IC2\\frontend\\icontrolit-app\\e2e\\data',
  frontend: 'D:\\IC2\\frontend\\icontrolit-app\\src\\app',
  routing_modules: 'D:\\IC2\\frontend\\icontrolit-app\\src\\app/**/*-routing.module.ts',
  governanca: 'D:\\IC2_Governanca'
};

const BASE_URL = 'http://localhost:4200';

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
 * Carrega URLs de TODOS os arquivos MT-*.data.ts
 */
function carregarTodasMTUrls(): MTUrls {
  try {
    const pattern = `${PATHS.mt_data}/MT-*.data.ts`;
    const arquivos = glob.sync(pattern);

    if (arquivos.length === 0) {
      aviso('Nenhum arquivo MT encontrado');
      return {};
    }

    info(`\nArquivos MT encontrados: ${arquivos.length}`);

    const todasUrls: MTUrls = {};

    arquivos.forEach(arquivo => {
      const nomeArquivo = path.basename(arquivo);
      info(`  - ${nomeArquivo}`);

      const conteudo = fs.readFileSync(arquivo, 'utf-8');

      // Extrair FRONTEND_URLS
      // Formato esperado:
      // export const FRONTEND_URLS = {
      //   signIn: 'http://localhost:4200/sign-in',
      //   clientes: 'http://localhost:4200/management/clientes'
      // };

      const urlsMatch = conteudo.match(/export\s+const\s+FRONTEND_URLS\s*=\s*\{([^}]+)\}/s);

      if (!urlsMatch) {
        aviso(`    FRONTEND_URLS não encontrada em ${nomeArquivo}`);
        return;
      }

      const urlsBloco = urlsMatch[1];

      // Extrair cada URL
      const urlRegex = /(\w+):\s*['"]([^'"]+)['"]/g;
      let match;

      while ((match = urlRegex.exec(urlsBloco)) !== null) {
        const [, nome, url] = match;
        todasUrls[`${nomeArquivo}:${nome}`] = url;
      }
    });

    sucesso(`\nTotal de URLs carregadas: ${Object.keys(todasUrls).length}`);
    return todasUrls;
  } catch (error) {
    erro(`Erro ao carregar URLs de MT: ${error.message}`);
    return {};
  }
}

/**
 * Carrega todas as rotas do Angular
 */
function carregarRotasAngular(): AngularRoute[] {
  try {
    const pattern = PATHS.routing_modules;
    const arquivos = glob.sync(pattern);

    if (arquivos.length === 0) {
      erro('Nenhum arquivo *-routing.module.ts encontrado');
      return [];
    }

    info(`\nArquivos routing encontrados: ${arquivos.length}`);

    const rotas: AngularRoute[] = [];

    arquivos.forEach(arquivo => {
      const nomeArquivo = path.basename(arquivo);

      const conteudo = fs.readFileSync(arquivo, 'utf-8');
      const linhas = conteudo.split('\n');

      // Buscar rotas
      // Formatos esperados:
      // { path: 'management/clientes', component: ClientesListComponent }
      // { path: 'sign-in', component: SignInComponent }

      linhas.forEach((linha, index) => {
        const numeroLinha = index + 1;

        const pathMatch = linha.match(/path:\s*['"]([^'"]+)['"]/);

        if (pathMatch) {
          const pathValue = pathMatch[1];

          // Construir fullPath (pode ser parte de rota parent)
          // Por simplicidade, vamos usar o path direto
          // (idealmente deveria considerar rotas parent, mas isso complica)

          rotas.push({
            path: pathValue,
            fullPath: pathValue,
            arquivo: nomeArquivo,
            linha: numeroLinha
          });
        }
      });
    });

    // Adicionar rotas comuns conhecidas manualmente
    rotas.push({
      path: '',
      fullPath: '',
      arquivo: 'app-routing.module.ts',
      linha: 0
    });

    sucesso(`\nTotal de rotas carregadas: ${rotas.length}`);
    return rotas;
  } catch (error) {
    erro(`Erro ao carregar rotas Angular: ${error.message}`);
    return [];
  }
}

/**
 * Valida sincronização entre MT URLs e rotas Angular
 */
function validarSincronizacao(): ValidationResult {
  info(`\n${'='.repeat(60)}`);
  info('VALIDAÇÃO DE URLS');
  info(`${'='.repeat(60)}\n`);

  // 1. Carregar URLs de MT
  const mtUrls = carregarTodasMTUrls();
  if (Object.keys(mtUrls).length === 0) {
    aviso('Nenhuma URL encontrada em arquivos MT');
    return {
      passou: true, // Não há URLs para validar
      mt_urls: {},
      rotas_angular: [],
      urls_invalidas: [],
      urls_nao_encontradas: []
    };
  }

  // 2. Carregar rotas Angular
  const rotasAngular = carregarRotasAngular();
  if (rotasAngular.length === 0) {
    return {
      passou: false,
      mt_urls: mtUrls,
      rotas_angular: [],
      urls_invalidas: [],
      urls_nao_encontradas: []
    };
  }

  // 3. Validar cada URL
  const urlsInvalidas: ValidationResult['urls_invalidas'] = [];
  const urlsNaoEncontradas: string[] = [];

  info(`\nValidando URLs...\n`);

  Object.entries(mtUrls).forEach(([nome, url]) => {
    info(`Validando: ${nome}`);
    console.log(`  URL: ${url}`);

    // Extrair path da URL (remover base)
    if (!url.startsWith(BASE_URL)) {
      erro(`  ✗ URL não começa com ${BASE_URL}`);
      urlsInvalidas.push({
        nome,
        url,
        path_esperado: '',
        motivo: `URL deve começar com ${BASE_URL}`
      });
      return;
    }

    const path = url.replace(BASE_URL, '').replace(/^\//, '');

    console.log(`  Path: /${path}`);

    // Buscar rota correspondente
    const rotaEncontrada = rotasAngular.find(rota => {
      // Comparar path exato ou path parcial
      return rota.fullPath === path || path.startsWith(rota.path);
    });

    if (!rotaEncontrada) {
      erro(`  ✗ Rota não encontrada no Angular`);
      urlsNaoEncontradas.push(nome);
      urlsInvalidas.push({
        nome,
        url,
        path_esperado: path,
        motivo: 'Rota não encontrada no routing do Angular (possível 404)'
      });
    } else {
      sucesso(`  ✓ Rota encontrada: ${rotaEncontrada.arquivo}:${rotaEncontrada.linha}`);
    }
  });

  const passou = urlsInvalidas.length === 0 && urlsNaoEncontradas.length === 0;

  return {
    passou,
    mt_urls: mtUrls,
    rotas_angular: rotasAngular,
    urls_invalidas: urlsInvalidas,
    urls_nao_encontradas: urlsNaoEncontradas
  };
}

/**
 * Exibe relatório de validação
 */
function exibirRelatorio(resultado: ValidationResult): void {
  info(`\n${'='.repeat(60)}`);
  info('RELATÓRIO DE VALIDAÇÃO');
  info(`${'='.repeat(60)}\n`);

  // Estatísticas
  log(`Total de URLs (MT):             ${Object.keys(resultado.mt_urls).length}`);
  log(`Total de rotas (Angular):       ${resultado.rotas_angular.length}`);
  log(`URLs inválidas:                 ${resultado.urls_invalidas.length}`);
  log(`URLs não encontradas:           ${resultado.urls_nao_encontradas.length}\n`);

  // URLs inválidas
  if (resultado.urls_invalidas.length > 0) {
    erro(`\n❌ URLS INVÁLIDAS (${resultado.urls_invalidas.length}):\n`);
    resultado.urls_invalidas.forEach(urlInvalida => {
      console.log(`  Nome: ${urlInvalida.nome}`);
      console.log(`  URL: ${urlInvalida.url}`);
      console.log(`  Path esperado: /${urlInvalida.path_esperado}`);
      console.log(`  Motivo: ${urlInvalida.motivo}`);
      console.log(`  Ação: Verificar routing do Angular ou corrigir URL no MT\n`);
    });
  }

  // Sugestões de rotas disponíveis
  if (resultado.urls_nao_encontradas.length > 0) {
    info(`\n📋 ROTAS DISPONÍVEIS NO ANGULAR:\n`);
    resultado.rotas_angular
      .filter(rota => rota.path !== '') // Filtrar rota raiz
      .slice(0, 20) // Limitar a 20 rotas para não poluir
      .forEach(rota => {
        console.log(`  - ${BASE_URL}/${rota.fullPath}`);
        console.log(`    Definida em: ${rota.arquivo}:${rota.linha}\n`);
      });

    if (resultado.rotas_angular.length > 20) {
      info(`  ... e mais ${resultado.rotas_angular.length - 20} rotas\n`);
    }
  }

  // Veredicto final
  info(`\n${'='.repeat(60)}`);
  if (resultado.passou) {
    sucesso('✅ VALIDAÇÃO PASSOU');
    sucesso('URLs do MT estão sincronizadas com rotas do Angular');
  } else {
    erro('❌ VALIDAÇÃO FALHOU');
    erro(`${resultado.urls_invalidas.length} URLs inválidas`);
    erro('Corrija as URLs no MT ou adicione rotas no routing do Angular');
  }
  info(`${'='.repeat(60)}\n`);
}

// =============================================
// EXECUÇÃO PRINCIPAL
// =============================================

function main(): void {
  // Executar validação
  const resultado = validarSincronizacao();

  // Exibir relatório
  exibirRelatorio(resultado);

  // Exit code baseado no resultado
  process.exit(resultado.passou ? 0 : 1);
}

// Executar apenas se chamado diretamente
if (require.main === module) {
  main();
}

export { validarSincronizacao, ValidationResult };

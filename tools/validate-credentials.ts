#!/usr/bin/env ts-node

/**
 * =============================================
 * VALIDATE CREDENTIALS - VERSÃO 1.0
 * =============================================
 *
 * Script de validação de sincronização de credenciais
 *
 * OBJETIVO:
 * Valida se as credenciais de teste em MT-RFXXX.data.ts estão sincronizadas
 * com os seeds do backend (ApplicationDbContextInitialiser.cs)
 *
 * EXECUÇÃO:
 * npm run validate-credentials RFXXX
 * OU
 * ts-node tools/validate-credentials.ts RFXXX
 *
 * EXIT CODES:
 * 0 - Validação PASSOU (credenciais sincronizadas)
 * 1 - Validação FALHOU (credenciais desatualizadas)
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

interface Credential {
  email: string;
  password: string;
  perfil: string;
}

interface MTCredentials {
  [key: string]: Credential;
}

interface SeedCredential {
  email: string;
  password: string;
  perfil: string;
  linha: number;
}

interface ValidationResult {
  passou: boolean;
  mt_credenciais: MTCredentials;
  seed_credenciais: SeedCredential[];
  divergencias: Array<{
    perfil: string;
    campo: string;
    mt_valor: string;
    seed_valor: string;
    seed_linha: number;
  }>;
  credenciais_ausentes_no_seed: string[];
}

// =============================================
// CONFIGURAÇÕES
// =============================================

const PATHS = {
  mt: (rfId: string) => `D:\\IC2\\frontend\\icontrolit-app\\e2e\\data\\MT-${rfId}.data.ts`,
  seeds: 'D:\\IC2\\backend\\src\\Infrastructure\\Persistence\\ApplicationDbContextInitialiser.cs',
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
 * Carrega credenciais de MT-RFXXX.data.ts
 */
function carregarMTCredenciais(rfId: string): MTCredentials | null {
  try {
    const mtPath = PATHS.mt(rfId);

    if (!fs.existsSync(mtPath)) {
      erro(`Arquivo MT não encontrado: ${mtPath}`);
      return null;
    }

    info(`Lendo MT: ${mtPath}`);

    const conteudo = fs.readFileSync(mtPath, 'utf-8');

    // Extrair credenciais usando regex
    // Formato esperado:
    // export const CREDENCIAIS_TESTE = {
    //   admin_teste: {
    //     email: 'admin@icontrolit.com.br',
    //     password: 'Admin@123',
    //     perfil: 'Admin'
    //   }
    // };

    const credenciaisMatch = conteudo.match(/export\s+const\s+CREDENCIAIS_TESTE\s*=\s*\{([^}]+)\}/s);

    if (!credenciaisMatch) {
      erro('CREDENCIAIS_TESTE não encontradas no MT');
      return null;
    }

    const credenciaisBloco = credenciaisMatch[1];

    // Extrair cada perfil
    const perfilRegex = /(\w+):\s*\{\s*email:\s*['"]([^'"]+)['"]\s*,\s*password:\s*['"]([^'"]+)['"]\s*,\s*perfil:\s*['"]([^'"]+)['"]/g;

    const credenciais: MTCredentials = {};
    let match;

    while ((match = perfilRegex.exec(credenciaisBloco)) !== null) {
      const [, perfilKey, email, password, perfil] = match;
      credenciais[perfilKey] = { email, password, perfil };
    }

    if (Object.keys(credenciais).length === 0) {
      erro('Nenhuma credencial encontrada no MT');
      return null;
    }

    sucesso(`MT carregado: ${Object.keys(credenciais).length} credenciais encontradas`);
    return credenciais;
  } catch (error) {
    erro(`Erro ao carregar MT: ${error.message}`);
    return null;
  }
}

/**
 * Carrega credenciais de ApplicationDbContextInitialiser.cs
 */
function carregarSeedCredenciais(): SeedCredential[] | null {
  try {
    const seedPath = PATHS.seeds;

    if (!fs.existsSync(seedPath)) {
      erro(`Arquivo de seeds não encontrado: ${seedPath}`);
      return null;
    }

    info(`Lendo seeds: ${seedPath}`);

    const conteudo = fs.readFileSync(seedPath, 'utf-8');
    const linhas = conteudo.split('\n');

    // Buscar seção de seeds de usuários
    // Formato esperado:
    // var adminUser = new ApplicationUser
    // {
    //     UserName = "admin@icontrolit.com.br",
    //     Email = "admin@icontrolit.com.br",
    //     ...
    // };
    // userManager.CreateAsync(adminUser, "Admin@123").Wait();

    const credenciais: SeedCredential[] = [];

    // Regex para identificar usuários e senhas
    const userRegex = /var\s+(\w+)\s*=\s*new\s+ApplicationUser/;
    const emailRegex = /Email\s*=\s*"([^"]+)"/;
    const passwordRegex = /CreateAsync\s*\([^,]+,\s*"([^"]+)"\)/;

    let currentUser: Partial<SeedCredential> = {};
    let currentUserName: string = '';
    let linhaInicio: number = 0;

    linhas.forEach((linha, index) => {
      const numeroLinha = index + 1;

      // Detectar início de novo usuário
      const userMatch = linha.match(userRegex);
      if (userMatch) {
        // Salvar usuário anterior se completo
        if (currentUser.email && currentUser.password) {
          credenciais.push(currentUser as SeedCredential);
        }

        // Iniciar novo usuário
        currentUserName = userMatch[1];
        currentUser = { linha: numeroLinha, perfil: currentUserName };
        linhaInicio = numeroLinha;
      }

      // Extrair email
      const emailMatch = linha.match(emailRegex);
      if (emailMatch && currentUserName) {
        currentUser.email = emailMatch[1];
      }

      // Extrair password
      const passwordMatch = linha.match(passwordRegex);
      if (passwordMatch && currentUserName) {
        currentUser.password = passwordMatch[1];

        // Finalizar usuário atual
        if (currentUser.email) {
          credenciais.push({
            email: currentUser.email,
            password: currentUser.password,
            perfil: currentUser.perfil || 'Unknown',
            linha: linhaInicio
          });
        }

        // Reset
        currentUser = {};
        currentUserName = '';
      }
    });

    if (credenciais.length === 0) {
      erro('Nenhuma credencial encontrada nos seeds');
      return null;
    }

    sucesso(`Seeds carregados: ${credenciais.length} credenciais encontradas`);
    return credenciais;
  } catch (error) {
    erro(`Erro ao carregar seeds: ${error.message}`);
    return null;
  }
}

/**
 * Valida sincronização entre MT e seeds
 */
function validarSincronizacao(rfId: string): ValidationResult {
  info(`\n${'='.repeat(60)}`);
  info(`VALIDAÇÃO DE CREDENCIAIS - ${rfId}`);
  info(`${'='.repeat(60)}\n`);

  // 1. Carregar credenciais de MT
  const mtCredenciais = carregarMTCredenciais(rfId);
  if (!mtCredenciais) {
    return {
      passou: false,
      mt_credenciais: {},
      seed_credenciais: [],
      divergencias: [],
      credenciais_ausentes_no_seed: []
    };
  }

  // 2. Carregar credenciais de seeds
  const seedCredenciais = carregarSeedCredenciais();
  if (!seedCredenciais) {
    return {
      passou: false,
      mt_credenciais: mtCredenciais,
      seed_credenciais: [],
      divergencias: [],
      credenciais_ausentes_no_seed: []
    };
  }

  // 3. Validar sincronização
  const divergencias: ValidationResult['divergencias'] = [];
  const credenciaisAusentesNoSeed: string[] = [];

  info(`\nValidando sincronização...\n`);

  Object.entries(mtCredenciais).forEach(([perfilKey, mtCred]) => {
    info(`Validando perfil: ${perfilKey} (${mtCred.perfil})`);

    // Buscar credencial correspondente no seed
    const seedCred = seedCredenciais.find(sc => sc.email === mtCred.email);

    if (!seedCred) {
      erro(`  ✗ Email não encontrado nos seeds: ${mtCred.email}`);
      credenciaisAusentesNoSeed.push(perfilKey);
      return;
    }

    // Validar email
    if (mtCred.email !== seedCred.email) {
      divergencias.push({
        perfil: perfilKey,
        campo: 'email',
        mt_valor: mtCred.email,
        seed_valor: seedCred.email,
        seed_linha: seedCred.linha
      });
    }

    // Validar password
    if (mtCred.password !== seedCred.password) {
      erro(`  ✗ Senha divergente`);
      divergencias.push({
        perfil: perfilKey,
        campo: 'password',
        mt_valor: mtCred.password,
        seed_valor: seedCred.password,
        seed_linha: seedCred.linha
      });
    } else {
      sucesso(`  ✓ Senha sincronizada`);
    }
  });

  const passou = divergencias.length === 0 && credenciaisAusentesNoSeed.length === 0;

  return {
    passou,
    mt_credenciais: mtCredenciais,
    seed_credenciais: seedCredenciais,
    divergencias,
    credenciais_ausentes_no_seed: credenciaisAusentesNoSeed
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
  log(`Total de credenciais (MT):      ${Object.keys(resultado.mt_credenciais).length}`);
  log(`Total de credenciais (Seeds):   ${resultado.seed_credenciais.length}`);
  log(`Divergências encontradas:       ${resultado.divergencias.length}\n`);

  // Divergências
  if (resultado.divergencias.length > 0) {
    erro(`\n❌ DIVERGÊNCIAS ENCONTRADAS (${resultado.divergencias.length}):\n`);
    resultado.divergencias.forEach(div => {
      console.log(`  Perfil: ${div.perfil}`);
      console.log(`  Campo: ${div.campo}`);
      console.log(`  Valor no MT: "${div.mt_valor}"`);
      console.log(`  Valor no Seed: "${div.seed_valor}" (linha ${div.seed_linha})`);
      console.log(`  Ação: Atualizar MT com valor do seed\n`);
    });
  }

  // Credenciais ausentes no seed
  if (resultado.credenciais_ausentes_no_seed.length > 0) {
    erro(`\n❌ CREDENCIAIS NÃO ENCONTRADAS NO SEED (${resultado.credenciais_ausentes_no_seed.length}):\n`);
    resultado.credenciais_ausentes_no_seed.forEach(perfil => {
      const mtCred = resultado.mt_credenciais[perfil];
      console.log(`  Perfil: ${perfil}`);
      console.log(`  Email no MT: "${mtCred.email}"`);
      console.log(`  Ação: Verificar se seed existe no backend ou corrigir email no MT\n`);
    });
  }

  // Veredicto final
  info(`\n${'='.repeat(60)}`);
  if (resultado.passou) {
    sucesso('✅ VALIDAÇÃO PASSOU');
    sucesso('Credenciais do MT estão sincronizadas com seeds do backend');
  } else {
    erro('❌ VALIDAÇÃO FALHOU');
    erro(`${resultado.divergencias.length + resultado.credenciais_ausentes_no_seed.length} problemas encontrados`);
    erro('Corrija as credenciais no MT e re-execute a validação');
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
    console.log('\nUso: npm run validate-credentials RFXXX');
    console.log('Exemplo: npm run validate-credentials RF006\n');
    process.exit(1);
  }

  const rfId = args[0];

  // Validar formato RF
  if (!/^RF\d{3}$/.test(rfId)) {
    erro(`Erro: Formato inválido "${rfId}"`);
    console.log('Formato esperado: RFXXX (ex: RF006)\n');
    process.exit(1);
  }

  // Executar validação
  const resultado = validarSincronizacao(rfId);

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

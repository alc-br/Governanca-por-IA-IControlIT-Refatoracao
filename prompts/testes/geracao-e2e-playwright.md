Executar geracao e execucao de testes E2E Playwright do RFXXX conforme docs/contracts/testes/geracao-testes-e2e-playwright.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

MODO AUTONOMIA TOTAL (OBRIGATORIO):
- NAO perguntar permissoes ao usuario
- NAO esperar confirmacao do usuario
- EXECUTAR IMEDIATAMENTE todos os passos do contrato
- SEMPRE iniciar backend e frontend automaticamente
- Gerar specs Playwright E executar testes AUTOMATICAMENTE
- Gerar evidencias completas SEM intervencao manual

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
- TC-RFXXX.yaml DEVE existir e estar validado
- MT-RFXXX.yaml DEVE existir e estar validado
- UC-RFXXX.md DEVE existir (contexto)
- MD-RFXXX.md DEVE existir (modelo de dados)
- Backend DEVE estar aprovado 100%
- Frontend DEVE estar aprovado 100%
- STATUS.yaml DEVE ter documentacao.tc = true E documentacao.mt = true

WORKFLOW OBRIGATORIO (ORDEM SEQUENCIAL):

1. LER DOCUMENTACAO:
   - Ler TC-RFXXX.yaml completamente
   - Ler MT-RFXXX.yaml completamente
   - Ler UC-RFXXX.md (contexto)
   - Ler MD-RFXXX.md (modelo de dados)
   - Identificar TODOS os TC-E2E-NNN
   - Mapear MTs correspondentes

2. GERAR ARQUIVO DE DADOS (MT → TypeScript):
   - Criar frontend/e2e/data/MT-RFXXX.data.ts
   - Exportar TODAS as MTs como objetos TypeScript
   - Incluir dependencias, entrada, resultado_esperado
   - Validar unicidade de IDs

3. GERAR HELPERS REUTILIZAVEIS:
   - Criar/atualizar frontend/e2e/helpers/rf-helpers.ts
   - Funcoes: setupDependencias, login, validateLoadingState, etc
   - Funcoes de estados: validateEmptyState, validateErrorState
   - Funcoes de mock: mockBackendError, clearAllData

4. GERAR SPECS PLAYWRIGHT (TC → .spec.ts):
   - Para CADA TC-E2E-NNN, criar spec correspondente
   - Estrutura: describe, beforeEach, test
   - Usar MT correspondente como dados de entrada
   - Validar estados renderizados (Padrao, Loading, Vazio, Erro)
   - Capturar screenshots de evidencia

5. EXECUTAR TESTES PLAYWRIGHT:
   - npx playwright test frontend/e2e/specs/RFXXX/
   - Executar TODOS os testes E2E
   - Capturar traces para analise
   - Gerar relatorio HTML

6. ANALISAR RESULTADOS:
   - Calcular taxa de aprovacao
   - Identificar falhas (se houver)
   - Atribuir responsabilidade (backend vs frontend)
   - Gerar relatorio de evidencias

7. GERAR RELATORIO CONSOLIDADO:
   - Criar frontend/e2e/evidencias/RELATORIO-RFXXX.md
   - Listar TODOS os testes (PASS e FAIL)
   - Detalhar falhas com responsabilidade
   - Gerar prompts de correcao (se reprovado)
   - Anexar evidencias (screenshots, traces, logs)

REGRAS DE ATRIBUICAO DE RESPONSABILIDADE:

BACKEND ❌ quando:
- HTTP 500 (erro interno)
- HTTP 400 com mensagem incorreta
- Validacao aceita payload invalido
- Multi-tenancy quebrado (retorna dados de outro tenant)
- Auditoria nao gravada (created_by ausente)

FRONTEND ❌ quando:
- Elemento nao renderizado (data-test ausente)
- Estado Loading nao visivel
- Estado Vazio nao visivel
- Estado Erro nao visivel
- i18n quebrado (chave nao traduzida)
- Validacao de formulario ausente

INTEGRACAO ❌ quando:
- Contrato de API quebrado (campo ausente)
- DTO incompativel
- Mapeamento incorreto

CRITERIO DE APROVACAO (0% OU 100%):
- ✅ APROVADO: Taxa de aprovacao = 100% (TODOS os testes passaram)
- ❌ REPROVADO: Taxa de aprovacao < 100% (QUALQUER teste falhou)

NAO EXISTE APROVACAO COM RESSALVAS.

AUTONOMIA TOTAL:
- NAO perguntar se pode gerar specs
- NAO perguntar se pode executar testes
- NAO esperar usuario rodar comandos
- O agente DEVE gerar specs E executar testes AUTOMATICAMENTE
- Garantir rastreabilidade total (TC → MT → Spec)
- Gerar evidencias completas sem intervencao manual

VALIDACAO FINAL OBRIGATORIA:
1. Todos TC-E2E-NNN tem spec correspondente
2. Todos specs referenciam MT correspondente
3. Todos os 4 estados foram validados
4. i18n validado (pt-BR, en-US, es-ES)
5. CRUD completo validado
6. Seguranca validada (401, 403)
7. Multi-tenancy validado
8. Evidencias geradas (screenshots, traces)
9. Relatorio consolidado criado

PROIBIDO:
- Gerar spec sem TC correspondente
- Executar apenas subset de testes
- Pular testes que falharam
- Modificar testes para fazer passar
- Marcar como APROVADO se taxa < 100%
- Alterar codigo de producao durante testes

CRITERIO DE PRONTO:
- Specs Playwright criados (1 por TC-E2E)
- Arquivo de dados MT-RFXXX.data.ts criado
- Helpers reutilizaveis criados/atualizados
- TODOS os testes executados
- Taxa de aprovacao calculada
- Relatorio consolidado criado
- Evidencias anexadas (screenshots, traces, logs)
- Falhas com responsabilidade atribuida (se houver)
- Prompts de correcao gerados (se reprovado)
- Nenhuma violacao de contrato

RESPONSABILIDADE DO AGENTE:
1. Ler documentacao (TC, MT, UC, MD)
2. Gerar arquivo de dados (MT → TypeScript)
3. Gerar helpers reutilizaveis
4. Gerar specs Playwright (TC → .spec.ts)
5. Executar testes Playwright
6. Analisar resultados
7. Atribuir responsabilidade em falhas
8. Gerar relatorio consolidado
9. Anexar evidencias completas
10. Atualizar STATUS.yaml (ultima_execucao_e2e, taxa_aprovacao_e2e, specs_playwright_gerados)
11. Declarar conclusao (APROVADO 100% ou REPROVADO)

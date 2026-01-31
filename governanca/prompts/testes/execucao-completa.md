Executar testes automatizados do RFXXX conforme D:\IC2_Governanca\governanca\contracts\testes\execucao-completa.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

EXCECAO IMPORTANTE - STATUS.yaml (v1.3):
A regra do CLAUDE.md "Se voce estiver rodando a partir de D:\IC2\ nunca altere nada em D:\IC2_Governanca" TEM UMA UNICA EXCECAO:

✅ STATUS.yaml DEVE ser atualizado por TODOS os contratos, independente de onde o agente esta rodando.

STATUS.yaml e o UNICO arquivo em D:\IC2_Governanca\ que PODE e DEVE ser alterado.

Ele DEVE ser atualizado:
- Apos execucao de testes (testes_ti.resultado_final, testes_ti.taxa_aprovacao, etc)
- Apos validacao de documentacao (documentacao.mt, documentacao.tc, etc)
- Apos execucao de backend/frontend (execucao.backend, execucao.frontend, etc)

Caminho: D:\IC2_Governanca\documentacao\[Fase]\[EPIC]\[RFXXX]\STATUS.yaml

SOMENTE STATUS.yaml e excecao. Nenhum outro arquivo em D:\IC2_Governanca\ pode ser alterado.

NAO use a regra do CLAUDE.md como desculpa para NAO atualizar STATUS.yaml.
STATUS.yaml e SEMPRE uma excecao permitida e OBRIGATORIA.

═══════════════════════════════════════════════════════════════════════════════
⚠️ REGRA DE OURO - LEIA PRIMEIRO (v1.3 - 2026-01-28)
═══════════════════════════════════════════════════════════════════════════════

VOCE E UM AGENTE AUTONOMO. VOCE RESOLVE PROBLEMAS. VOCE NAO PEDE AJUDA.

SE encontrar "Tabela vazia", "Sem dados", "Seed nao executado":
→ VOCE resolve. NAO pede para usuario resolver.
→ VOCE executa o seed. NAO documenta para usuario executar.
→ VOCE cria os dados via API. NAO sugere que usuario crie.

COMPORTAMENTO PROIBIDO (que voce estava fazendo):
❌ "Gap Identificado: Seed nao executado"
❌ "Acao Requerida: Executar o seed via..."
❌ "Taxa de Aprovacao: 33% - PASSOU PARCIAL"
❌ "STATUS.yaml: testes.e2e: partial"

COMPORTAMENTO OBRIGATORIO (que voce DEVE fazer):
✅ Identificar: "Tabela SistemaParametroCategorias vazia"
✅ Resolver: Executar seed OU criar via API
✅ Verificar: Tabela agora tem dados
✅ Continuar: Executar o teste que falhou
✅ Resultado: "UC01 - Criar: PASSOU (apos resolver dados)"

SE VOCE MARCAR COMO "SKIP" OU "PARTIAL" SEM TENTAR RESOLVER:
→ Execucao e INVALIDA
→ Aprovacao e NULA
→ Voce VIOLOU o contrato

EXEMPLO CONCRETO PARA RF001:

Problema: "SistemaParametroCategorias vazia"

Solucao que VOCE deve executar:
```bash
# Opcao 1: Criar via API
curl -X POST http://localhost:5000/api/v1/sistema-parametros-categorias \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Categoria Teste", "descricao": "Categoria criada para teste E2E"}'

# Opcao 2: Executar seed diretamente
cd D:\IC2\backend\IControlIT.API
dotnet run -- seed --entity=SistemaParametroCategoria

# Opcao 3: Inserir SQL direto
sqlcmd -S localhost -d IControlIT -Q "INSERT INTO SistemaParametroCategorias (Nome, Descricao, Ativo) VALUES ('Categoria Teste', 'Teste', 1)"
```

Depois de resolver → REPETIR o teste UC01 → Deve PASSAR agora.

NAO EXISTE "PASSOU PARCIAL". OU PASSA 100% OU REPROVA.

═══════════════════════════════════════════════════════════════════════════════

CHECKLIST OBRIGATÓRIO:
Validar todos os itens de D:\IC2_Governanca\governanca\checklists\testes\pre-execucao.yaml antes de prosseguir.

SELECAO DE ESTRATEGIA (OBRIGATORIO - PERGUNTAR ANTES DE EXECUTAR):

ANTES de iniciar a execucao de testes, o agente DEVE perguntar ao usuario:

"Este RF vai para:
A) HOMOLOGACAO (usar MVS: 2-4h, 80% cobertura, 1 smoke test E2E)
B) PRODUCAO (usar COMPLETO: 10+h, 95-100% cobertura, todos os testes E2E)

Responda A ou B."

SE usuario responder "A" ou "HOM" ou "homologacao":
- ✅ Ativar contrato: D:\IC2_Governanca\governanca\contracts\testes\CONTRATO-TESTES-MINIMO-VIAVEL-SEGURO.md
- ✅ Executar apenas: Unitarios (100%) + Smoke E2E (1 spec) + Seguranca Critica (2 tipos)
- ✅ Tempo esperado: 2-4 horas
- ✅ Resultado: APROVADO_HOM ou REPROVADO

SE usuario responder "B" ou "PRD" ou "producao":
- ✅ Continuar com este contrato (execucao-completa.md)
- ✅ Executar todos os testes: Unitarios + Frontend + E2E Completo + Seguranca Completa
- ✅ Tempo esperado: 10+ horas
- ✅ Resultado: APROVADO_PRD ou REPROVADO

SE usuario NAO especificar ambiente:
- ❌ PARAR execucao
- ❌ PERGUNTAR novamente a estrategia
- ❌ NAO assumir estrategia padrao

MODO AUTONOMIA TOTAL (OBRIGATORIO):
- NAO perguntar permissoes ao usuario
- NAO esperar confirmacao do usuario
- NAO solicitar que usuario execute comandos manualmente
- EXECUTAR IMEDIATAMENTE todos os passos do contrato
- SEMPRE iniciar backend e frontend automaticamente
- Falhas em testes ANTERIORES NAO sao bloqueantes (sao o motivo da re-execucao)
- Gerar evidencias e relatorios SEM intervencao manual

AUTONOMIA PARA RESOLVER PROBLEMAS DE DADOS/AMBIENTE (v1.2 - 2026-01-28):

⚠️ REGRA CRITICA: O agente de testes NAO PODE abandonar execucao por falta de dados!

SE durante execucao de testes E2E encontrar:
- Tabela vazia (ex: "Sem categorias no banco")
- Dados de dependencia ausentes (ex: "FK nao encontrada")
- Seed nao executado (ex: "Usuario de teste nao existe")
- Dados pre-requisitos faltando (ex: "Empresa nao cadastrada")

ENTAO o agente DEVE (nesta ordem):

1. IDENTIFICAR O PROBLEMA:
   - Qual tabela esta vazia?
   - Qual seed deveria ter populado?
   - Quais dados sao necessarios para o teste?

2. RESOLVER AUTONOMAMENTE (tentar TODAS as opcoes):

   a) EXECUTAR SEED ESPECIFICO:
      ```bash
      # Tentar via CLI do backend (se disponivel)
      dotnet run --project src/IControlIT.API.csproj -- seed --entity=[ENTIDADE]

      # OU via EF migrations
      dotnet ef database update

      # OU via script SQL direto (se seed SQL existir)
      sqlcmd -S localhost -d IControlIT -i seeds/[entidade].sql
      ```

   b) INSERIR DADOS VIA API:
      ```bash
      # Criar dados minimos via endpoint POST
      curl -X POST http://localhost:5000/api/v1/[entidade] \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"nome": "Categoria Teste", ...}'
      ```

   c) EXECUTAR SEED COMPLETO:
      ```bash
      # Reiniciar backend com seeds
      cd D:\IC2\backend\IControlIT.API
      dotnet run --project src/IControlIT.API.csproj -- seed --all
      ```

   d) BUSCAR SEED NO CODIGO:
      - Procurar em D:\IC2\backend\IControlIT.API\src\Infrastructure\Data\Seeds\
      - Identificar classe *SeedData.cs correspondente
      - Executar metodo Seed() diretamente se possivel

3. VALIDAR RESOLUCAO:
   - Verificar se tabela agora tem dados
   - Verificar se teste pode prosseguir
   - Continuar execucao E2E

4. SOMENTE SE TODAS AS OPCOES FALHAREM:
   - Documentar TODAS as tentativas feitas
   - Atribuir responsabilidade ao BACKEND (seed nao funciona)
   - REPROVAR com detalhes das tentativas

PROIBIDO (VIOLACAO GRAVE):
- ❌ SKIP de teste por "dados ausentes" SEM tentar resolver
- ❌ Abandonar execucao na primeira dificuldade
- ❌ Marcar como "PASSOU parcial" quando dados faltam
- ❌ Dizer "execute manualmente" para usuario

OBRIGATORIO:
- ✅ Tentar TODAS as opcoes de resolucao antes de desistir
- ✅ Documentar cada tentativa de resolucao
- ✅ Se resolver, continuar testes normalmente
- ✅ Se nao resolver, reprovar com evidencias das tentativas

EXEMPLO DE COMPORTAMENTO CORRETO:

❌ ERRADO (passivo):
"UC01 - Criar: SKIP - Sem categorias no banco"
"Taxa de Aprovacao: 33%"

✅ CORRETO (autonomo):
"UC01 - Criar: Tabela SistemaParametroCategorias vazia
→ Tentativa 1: Executando seed via CLI... FALHOU
→ Tentativa 2: Buscando SeedData.cs... Encontrado!
→ Tentativa 3: Inserindo via API POST... SUCESSO
→ Categorias criadas: 5 registros
→ Continuando teste UC01...
→ UC01 - Criar: PASSOU"

REGRA CRITICA DE INTERPRETACAO:
- Pre-requisitos bloqueantes: backend aprovado (done), frontend aprovado (done), MT validado, TC validado
- Testes anteriores REPROVADOS: NAO e bloqueante, e justamente por isso estamos RE-EXECUTANDO
- Se STATUS.yaml mostra "testes_ti.resultado_final: REPROVADO": isso JUSTIFICA a re-execucao, NAO bloqueia

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
1. Backend DEVE estar aprovado (validacao backend = 100%)
2. Frontend DEVE estar aprovado (validacao frontend = 100%)
3. MT-RFXXX.yaml DEVE existir e estar validado
4. TC-RFXXX.yaml DEVE existir e estar validado
5. Schema.sql DEVE existir (para testes funcionais backend)
   - Caminho: D:\IC2\backend\IControlIT.API\tests\schema.sql
   - Validacao: Checklist D:\IC2_Governanca\governanca\checklists\testes\pre-execucao.yaml
6. STATUS.yaml DEVE ter:
   - execucao.backend = done
   - execucao.frontend = done
   - documentacao.mt = true
   - documentacao.tc = true

VALIDACAO INICIAL OBRIGATORIA:
1. Antes de QUALQUER teste, execute:
   - dotnet build (backend)
   - npm run build (frontend)
2. Se QUALQUER build quebrar: PARAR, REPORTAR, BLOQUEAR
3. Somente prosseguir com testes se AMBOS os builds passarem

WORKFLOW DE EXECUCAO (ORDEM OBRIGATORIA):

1. SETUP DE AMBIENTE:

   **1.1 INICIALIZACAO AUTOMATICA (RECOMENDADO):**

   A forma MAIS SIMPLES e RECOMENDADA de iniciar o sistema completo:

   ```bash
   python run.py
   ```

   O script `run.py` executa automaticamente:
   - ✅ Mata TODOS os processos travados (backend e frontend)
   - ✅ Inicia backend em BACKGROUND (porta 5000)
   - ✅ Inicia frontend em BACKGROUND (porta 4200)
   - ✅ Aguarda ambos estarem prontos
   - ✅ Valida health checks automaticamente

   IMPORTANTE: Sempre use `python run.py` para garantir ambiente limpo e funcional.

   **1.2 CREDENCIAIS DE TESTE (OBRIGATORIO):**

   Para executar testes E2E, use as seguintes credenciais:

   ```
   Email: anderson.chipak@k2apartners.com.br
   Senha: Vi696206@
   ```

   Este usuario tem:
   - ✅ Perfil: Developer (escopo = 3)
   - ✅ Permissoes completas para TODOS os RFs
   - ✅ Acesso a TODAS as funcionalidades do sistema
   - ✅ Dados de teste pre-populados

   **1.3 PREPARACAO MANUAL (FALLBACK):**

   Se `run.py` falhar ou nao estiver disponivel, executar MANUALMENTE:

   ```powershell
   # 1. Matar processos travados (se houver)
   Get-Process | Where-Object { $_.ProcessName -like "*IControlIT*" } | Stop-Process -Force

   # 2. Iniciar backend (BACKGROUND)
   cd backend/IControlIT.API
   dotnet run &

   # 3. Iniciar frontend (BACKGROUND)
   cd frontend/icontrolit-app
   npm start &
   ```

   IMPORTANTE: Backend pode travar durante inicializacao de seeds.
   Se /health nao responder em 20s, backend esta travado. Solucao:

   1. Verificar se Program.cs tem Task.Run() em InitialiseDatabaseAsync
   2. Se NAO tiver, backend vai travar. Corrigir conforme:
      - Linha 216-232 de D:\IC2\backend\IControlIT.API/src/Web/Program.cs
      - DEVE usar Task.Run() para executar seeds em BACKGROUND
      - Nunca usar await direto (bloqueia startup)

   3. Se backend continuar travado apos 30s:
      - Matar processo: Stop-Process -Name "IControlIT.API.Web" -Force
      - Limpar artifacts: Remove-Item D:\IC2\backend\IControlIT.API/artifacts -Recurse -Force
      - Rebuild: dotnet build --no-incremental
      - Reiniciar: dotnet run

   **1.4 VALIDACAO DE HEALTH:**

   Apos iniciar backend (via run.py OU manual), SEMPRE validar:

   ```bash
   # Tentar 3 vezes com intervalo de 5s
   curl http://localhost:5000/health
   # Esperado: Status 200 OK (Healthy)
   ```

   Se timeout apos 15s total: Backend TRAVADO (erro CRITICO)

   **1.5 VALIDACAO DE SEEDS:**
   - Aplicar seeds funcionais (dotnet ef database update)
   - Validar que banco tem dados minimos (empresas, perfis, permissoes)
   - Validar que usuario anderson.chipak@k2apartners.com.br existe
   - Aguardar /health responder (max 15s)
   - Aguardar frontend responder em http://localhost:4200 (max 30s)

2. TESTES BACKEND (Prioridade 1):
   - Executar testes unitarios (dotnet test)
   - Executar testes de integracao
   - Executar testes de contrato
   - Executar testes de violacao
   - Validar que backend rejeita payloads invalidos
   - Registrar resultado (PASS/FAIL)

3. TESTES FRONTEND (Prioridade 2):
   - Executar testes unitarios (npm run test)
   - Executar testes de componentes
   - Executar testes de servicos
   - Validar formularios e validacoes
   - Registrar resultado (PASS/FAIL)

4. GERACAO E EXECUCAO DE TESTES E2E (Prioridade 3):

   **4.1 VERIFICAR SE SPECS PLAYWRIGHT EXISTEM (BLOQUEANTE - v1.1 2026-01-28):**
   - Verificar se existe frontend/e2e/specs/RFXXX/
   - Verificar se existe frontend/e2e/data/MT-RFXXX.data.ts
   - Verificar se specs cobrem TODOS os TC-E2E-NNN do TC-RFXXX.yaml

   **4.2 SE SPECS NAO EXISTEM OU INCOMPLETOS → REPROVAR IMEDIATAMENTE:**

   ⚠️ REGRA INVIOLAVEL: SE specs nao existem, REPROVAR NA HORA!

   - ❌ NAO aprovar sem specs (VIOLACAO GRAVE)
   - ❌ NAO pular para proxima fase sem specs
   - ❌ NAO executar testes E2E sem specs

   ACAO OBRIGATORIA:
   1. REPROVAR execucao de testes
   2. ATRIBUIR RESPONSABILIDADE ao agente de geracao E2E
   3. GERAR PROMPT DE CORRECAO:

   ```
   ❌ REPROVADO - SPECS PLAYWRIGHT NAO EXISTEM

   BLOQUEIO TOTAL: Testes E2E nao podem ser executados.

   RESPONSABILIDADE: AGENTE DE GERACAO E2E

   ACAO NECESSARIA:
   Execute o prompt de geracao de specs E2E:

   ════════════════════════════════════════════════════════════════════
   Para o RF[XXX] [CAMINHO_RF] execute o
   D:\IC2_Governanca\governanca\prompts\testes\geracao-e2e-playwright.md
   ════════════════════════════════════════════════════════════════════

   APOS gerar specs, re-execute este contrato de testes.

   RESULTADO: REPROVADO
   ```

   SOMENTE SE o agente conseguir gerar specs NA MESMA SESSAO:
   - Executar geracao automatica via prompts/testes/geracao-e2e-playwright.md:
     * Ler TC-RFXXX.yaml e MT-RFXXX.yaml
     * Gerar frontend/e2e/data/MT-RFXXX.data.ts
     * Gerar frontend/e2e/helpers/rf-helpers.ts
     * Gerar frontend/e2e/specs/RFXXX/*.spec.ts (1 spec por TC-E2E)
     * Validar cobertura 100% de TC-E2E
   - SOMENTE prosseguir se geracao aprovada 100%
   - SE geracao falhar: REPROVAR (nao continuar)

   **4.3 PREPARAR DADOS DE TESTE (OBRIGATORIO ANTES DE EXECUTAR E2E):**

   ANTES de executar qualquer teste E2E, o agente DEVE:

   a) VERIFICAR DADOS DE DEPENDENCIA:
      - Ler MT-RFXXX.yaml e identificar TODAS as dependencias
      - Para cada dependencia, verificar se existe no banco
      - Exemplos: categorias, empresas, usuarios, perfis, permissoes

   b) SE DEPENDENCIA NAO EXISTIR → CRIAR AUTOMATICAMENTE:

      ```typescript
      // Exemplo: Criar categoria via API antes do teste
      const categoriaResponse = await request.post('/api/v1/categorias', {
        data: { nome: 'Categoria Teste E2E', ativo: true }
      });
      expect(categoriaResponse.ok()).toBeTruthy();
      const categoriaId = (await categoriaResponse.json()).id;
      ```

      OU via seed:
      ```bash
      # Executar seed especifico
      cd D:\IC2\backend\IControlIT.API
      dotnet run -- seed --entity=SistemaParametroCategoria
      ```

   c) VALIDAR QUE DADOS EXISTEM:
      ```bash
      # Verificar via API
      curl http://localhost:5000/api/v1/categorias
      # Deve retornar lista NAO vazia
      ```

   d) SOMENTE ENTAO prosseguir para testes E2E

   **4.4 EXECUTAR TESTES E2E:**
   - Popular dados usando MT-RFXXX.yaml
   - Executar testes Playwright (npm run e2e)
   - Validar fluxos completos de usuario:
     * Login como developer (anderson.chipak@k2apartners.com.br / Vi696206@)
     * Navegar via menu
     * Acessar tela do RFXXX
     * Executar CRUD completo (criar, editar, excluir, consultar)
   - Validar 4 estados renderizados:
     * Estado Padrao (dados carregados)
     * Estado Loading (spinner/skeleton visivel)
     * Estado Vazio (mensagem quando lista vazia)
     * Estado Erro (mensagem quando HTTP falha)
   - Validar i18n (pt-BR, en-US, es-ES)
   - Capturar screenshots de evidencia
   - Registrar resultado (PASS/FAIL)

   **4.5 SE TESTE E2E FALHAR POR DADOS AUSENTES:**

   ❌ COMPORTAMENTO ERRADO (PROIBIDO):
   "UC01 - Criar: SKIP - Sem categorias"
   "Taxa: 33% - PASSOU PARCIAL"
   "Gap Identificado: Seed nao executado"
   "Acao Requerida: Usuario deve executar..."

   ✅ COMPORTAMENTO CORRETO (OBRIGATORIO):

   PASSO 1 - IDENTIFICAR:
   "Teste UC01 falhou: Tabela SistemaParametroCategorias vazia"

   PASSO 2 - RESOLVER (executar um destes):
   ```bash
   # Tentar via API primeiro (mais rapido)
   curl -X POST http://localhost:5000/api/v1/sistema-parametros-categorias \
     -H "Authorization: Bearer [TOKEN]" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Categoria Teste", "ativo": true}'
   ```

   OU:
   ```bash
   # Via seed do backend
   cd D:\IC2\backend\IControlIT.API
   dotnet run -- seed --entity=SistemaParametroCategoria
   ```

   OU:
   ```bash
   # Via SQL direto
   sqlcmd -S localhost -d IControlIT -Q "INSERT INTO SistemaParametroCategorias..."
   ```

   PASSO 3 - VERIFICAR:
   ```bash
   curl http://localhost:5000/api/v1/sistema-parametros-categorias
   # Deve retornar lista NAO vazia
   ```

   PASSO 4 - REPETIR O TESTE:
   ```bash
   npx playwright test e2e/specs/RF001/TC-RF001-E2E-001.spec.ts
   ```

   PASSO 5 - REPORTAR SUCESSO:
   "UC01 - Criar: PASSOU (dados criados via API)"

   O agente NAO PODE marcar como SKIP. DEVE resolver e testar.
   O agente NAO PODE pedir para usuario resolver. DEVE resolver sozinho.
   O agente NAO PODE documentar "Gap" e parar. DEVE resolver o gap.

5. TESTES DE SEGURANCA (Prioridade 4):
   - Validar protecao contra SQL Injection
   - Validar protecao contra XSS
   - Validar protecao contra CSRF
   - Validar autenticacao (401 quando nao logado)
   - Validar autorizacao (403 quando sem permissao)
   - Validar multi-tenancy (isolamento entre tenants)
   - Registrar resultado (PASS/FAIL)

6. CONSOLIDACAO DE RESULTADOS:
   - Calcular taxa de aprovacao (% de testes passando)
   - Identificar falhas criticas
   - Atribuir responsabilidade em falhas:
     * HTTP 500/400 → BACKEND
     * Elemento nao renderizado → FRONTEND
     * Estado nao visivel → FRONTEND
     * Validacao nao funcionando → BACKEND ou FRONTEND (analisar)
   - Gerar relatorio consolidado

7. DECISAO FINAL:
   - SE taxa de aprovacao = 100%: APROVADO
   - SE taxa de aprovacao < 100%: REPROVADO
   - Registrar decisao no EXECUTION-MANIFEST
   - Atualizar STATUS.yaml

8. EVIDENCIAS OBRIGATORIAS:
   - Screenshots de testes E2E (sucesso e falhas)
   - Videos de execucao (se disponivel)
   - Logs de execucao completos
   - Relatorio HTML de testes
   - Relatorio de cobertura
   - Relatorio de responsabilidade (backend vs frontend)

AUTONOMIA TOTAL:
- NAO perguntar se pode executar testes
- NAO esperar usuario rodar comandos
- O agente DEVE executar TODOS os testes automaticamente
- Garantir que ambiente esteja buildado, rodando e testado
- Gerar evidencias sem intervencao manual

REGRAS CRITICAS DE GIT E COMMITS:
- SEMPRE executar em branch `dev` (NUNCA criar branches)
- NUNCA fazer commits de codigo durante testes
- NUNCA fazer commits de STATUS.yaml ou relatorios
- NUNCA corrigir codigo de PRODUCAO (handlers, validators, components)
- SEMPRE gerar prompt de correcao quando encontrar problemas de CODIGO
- Exibir prompt completo na tela para usuario copiar

EXCECAO - O AGENTE PODE E DEVE:
- ✅ Executar seeds para popular dados de teste
- ✅ Inserir dados via API para viabilizar testes
- ✅ Criar registros de dependencia (FK) via API
- ✅ Limpar dados de teste anteriores que atrapalham
- ✅ Reiniciar backend/frontend se travados
- ✅ Corrigir configuracao de ambiente (portas, URLs)

ATRIBUICAO DE RESPONSABILIDADE EM FALHAS:

Quando um teste FALHAR, o agente DEVE identificar:

1. BACKEND (Handler/Validator/Repository):
   - HTTP 500 (erro interno do servidor)
   - HTTP 400 com mensagem incorreta
   - Validacao aceita payload invalido
   - Violacao nao rejeitada
   - Multi-tenancy quebrado (retorna dados de outro tenant)
   - Auditoria nao gravada
   - **Endpoint /health nao responde (TIMEOUT/ERROR/BACKEND_DOWN)**
   - **Backend nao confirma "Application started" nos logs**
   - **Seeds travando inicializacao (InitialiseDatabaseAsync bloqueante)**

2. FRONTEND (Component/Service/Template):
   - Elemento nao renderizado (data-test ausente)
   - Estado Loading nao visivel
   - Estado Vazio nao visivel
   - Estado Erro nao visivel
   - i18n quebrado (chave nao traduzida)
   - Validacao de formulario ausente

3. INTEGRACAO (Backend + Frontend):
   - Contrato de API quebrado (campo ausente)
   - DTO incompativel
   - Mapeamento incorreto

RELATORIO DE FALHAS OBRIGATORIO:

Para cada teste REPROVADO, criar:

```markdown
# RELATORIO DE FALHA - TC-RFXXX-[CAT]-NNN

## TESTE FALHADO
- TC: TC-RFXXX-[CAT]-NNN
- Descricao: [descricao do teste]
- Categoria: [HAPPY_PATH/VALIDACAO/SEGURANCA/E2E/etc]
- Prioridade: CRITICA/ALTA/MEDIA/BAIXA

## ERRO IDENTIFICADO
- Mensagem: [erro completo]
- Screenshot: evidencias/TC-RFXXX-[CAT]-NNN-falha.png
- Log: logs/TC-RFXXX-[CAT]-NNN.log

## RESPONSABILIDADE
- Camada: BACKEND ❌ | FRONTEND ❌ | INTEGRACAO ❌
- Razao: [por que atribuiu a essa camada]
- Arquivo provavel: [caminho do arquivo]
- Linha provavel: [numero da linha, se identificavel]

## CONTEXTO
- MT usada: MT-RFXXX-NNN
- Dados enviados: { ... }
- Resposta recebida: { ... }
- Resposta esperada: { ... }

## PROXIMO PASSO
Corrigir via prompt de manutencao:

\```
Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-controlada.md para corrigir o seguinte erro no [backend/frontend] de RFXXX:

**OU (se > 3 arquivos afetados):**

Execute D:\IC2_Governanca\prompts\desenvolvimento\manutencao\manutencao-completa.md para corrigir o seguinte erro no [backend/frontend] de RFXXX:

ERRO IDENTIFICADO:
- TC falhado: TC-RFXXX-[CAT]-NNN
- [Descricao completa do erro]

EVIDENCIAS:
- Screenshot: evidencias/TC-RFXXX-[CAT]-NNN-falha.png
- Log: logs/TC-RFXXX-[CAT]-NNN.log

CONTEXTO:
- RF: RFXXX
- UC: UCXX
- Handler/Component: [nome]
\```
```

CRITERIO DE APROVACAO (0% OU 100%):

- ✅ APROVADO: Taxa de aprovacao = 100% (TODOS os testes passaram)
- ❌ REPROVADO: Taxa de aprovacao < 100% (QUALQUER teste falhou)

NAO EXISTE APROVACAO COM RESSALVAS.
NAO EXISTE "PASSOU PARCIAL".
NAO EXISTE "testes.e2e: partial".
NAO EXISTE "33% - PASSOU".

⚠️ CATEGORIAS INVENTADAS SAO PROIBIDAS (v1.4 - 2026-01-31):

As seguintes categorias NAO EXISTEM e sao VIOLACOES GRAVES:
- ❌ "APROVADO CONDICIONALMENTE" → NAO EXISTE
- ❌ "APROVADO COM RESSALVAS" → NAO EXISTE
- ❌ "APROVADO PARCIALMENTE" → NAO EXISTE
- ❌ "APROVADO PARA HOM, PENDENTE PRD" → NAO EXISTE
- ❌ "PROBLEMA DE INFRAESTRUTURA, NAO DO CODIGO" → NAO E DESCULPA

SE agente usar qualquer categoria acima:
- Execucao e INVALIDA
- Aprovacao e NULA
- Agente VIOLOU o contrato

REGRA PARA PROBLEMAS DE AUTENTICACAO/INTEGRACAO (v1.4):

SE testes falharem por problemas de autenticacao (401, token expirado, interceptor):
1. NAO aprovar condicionalmente
2. NAO atribuir a "infraestrutura" e aprovar
3. RESOLVER o problema (debugar, ajustar config, corrigir codigo)
4. SE nao conseguir resolver: REPROVAR com responsabilidade atribuida

Exemplos de atribuicao CORRETA:
| Sintoma | Responsavel |
|---------|-------------|
| Token expira muito rapido | BACKEND (config JWT) |
| Header Authorization ausente | FRONTEND (auth.interceptor.ts) |
| Token nao persiste no localStorage | FRONTEND (auth.service.ts) |
| E2E perde sessao entre requests | TESTES (storageState Playwright) |
| 401 em endpoint protegido | BACKEND ou FRONTEND |

A UNICA saida e: APROVADO (100%) ou REPROVADO (< 100%).
Nao existe meio termo.

SE taxa < 100%:
- NAO e porque "dados faltam" (voce DEVE resolver dados)
- NAO e porque "seed nao executou" (voce DEVE executar seed)
- NAO e porque "problema de integracao" (voce DEVE resolver integracao)
- NAO e porque "autenticacao falhou" (voce DEVE atribuir responsabilidade)
- E porque ALGO falhou (ai sim voce documenta e reprova)

SE voce marcar como "partial" ou "33%" ou "APROVADO CONDICIONALMENTE" → EXECUCAO INVALIDA.

RESPONSABILIDADE DO AGENTE:
1. Validar pre-requisitos (backend/frontend aprovados, MT/TC validados)
2. Buildar backend e frontend
3. Aplicar seeds funcionais
4. Iniciar backend e frontend
5. Executar testes backend (dotnet test)
6. Executar testes frontend (npm run test)
7. VERIFICAR SE SPECS PLAYWRIGHT EXISTEM:
   - Se NAO: executar geracao automatica (prompts/testes/geracao-e2e-playwright.md)
   - Se SIM: validar cobertura completa de TC-E2E
8. **PREPARAR DADOS DE TESTE (v1.2):**
   - Ler MT-RFXXX.yaml e identificar dependencias
   - Verificar se dados existem no banco
   - SE NAO existem: criar via seed OU API
   - NUNCA pular teste por falta de dados
9. Executar testes E2E (npm run e2e)
10. **SE TESTE FALHAR POR DADOS: resolver e REPETIR (v1.2)**
11. Executar testes de seguranca
12. Consolidar resultados
13. Atribuir responsabilidade em falhas
14. Gerar relatorio consolidado
15. Gerar evidencias (screenshots, logs)
16. Atualizar azure-test-cases-RF[XXX].csv (State conforme resultado)
17. Atualizar STATUS.yaml (incluindo testes.azure_devops)
18. Registrar decisao (APROVADO/REPROVADO)

PROIBIDO:
- Executar apenas subset de testes
- Pular testes que falharam
- Modificar testes para fazer passar
- Marcar como APROVADO se taxa < 100%
- Alterar codigo de producao durante testes
- Executar testes sem buildar antes
- Executar testes sem seeds aplicados
- **APROVAR SEM SPECS PLAYWRIGHT (VIOLACAO GRAVE - v1.1)**
- **PULAR VALIDACAO DE SPECS E2E (VIOLACAO GRAVE - v1.1)**
- **CONTINUAR PARA FASE 5 SEM SPECS 100% (VIOLACAO GRAVE - v1.1)**
- **SKIP DE TESTE POR "DADOS AUSENTES" SEM TENTAR RESOLVER (v1.2)**
- **ABANDONAR EXECUCAO NA PRIMEIRA DIFICULDADE (v1.2)**
- **MARCAR COMO "PASSOU PARCIAL" QUANDO DADOS FALTAM (v1.2)**
- **DIZER "EXECUTE MANUALMENTE" PARA USUARIO (v1.2)**
- **USAR "APROVADO CONDICIONALMENTE" (CATEGORIA NAO EXISTE - v1.4)**
- **USAR "APROVADO COM RESSALVAS" (CATEGORIA NAO EXISTE - v1.4)**
- **ATRIBUIR A "INFRAESTRUTURA" E APROVAR (NAO E DESCULPA - v1.4)**
- **DIZER "CODIGO CORRETO, PROBLEMA DE INTEGRACAO" E APROVAR (v1.4)**

CRITERIO DE PRONTO:
- Specs Playwright gerados (se nao existiam) e validados
- TODOS os testes executados (backend, frontend, E2E, seguranca)
- Taxa de aprovacao calculada
- Falhas identificadas com responsavel atribuido
- Evidencias geradas (screenshots, logs, traces)
- Relatorio consolidado criado
- STATUS.yaml atualizado (incluindo testes.azure_devops)
- azure-test-cases-RF[XXX].csv atualizado (State conforme resultado)
- Decisao registrada (APROVADO/REPROVADO)
- Nenhuma violacao de contrato

FORMATO DE RELATORIO FINAL CORRETO:

❌ ERRADO #1 (skip de testes por dados):
```
Resultado da Execucao
| Passo | UC | Resultado | Observacao |
| 1 | UC00 | PASSOU | Listagem carregou |
| 2 | UC01 | SKIP | Sem categorias no banco |  ← PROIBIDO!
| 3 | UC02 | SKIP | Depende do Passo 2 |      ← PROIBIDO!

Taxa de Aprovacao: 33%
Gap Identificado: Seed nao executado
Acao Requerida: Usuario deve...                ← PROIBIDO!
STATUS.yaml: testes.e2e: partial               ← PROIBIDO!
```

❌ ERRADO #2 (aprovado condicionalmente - v1.4):
```
Relatorio de Investigacao: GAP-INTEGRACAO-001

Conclusao: O problema NAO e do codigo RF083.
E um problema de INTEGRACAO entre o mecanismo
de autenticacao e o ambiente E2E.

Recomendacao:
O frontend RF083 deve ser considerado
APROVADO CONDICIONALMENTE.              ← PROIBIDO! CATEGORIA NAO EXISTE!

Proximos passos para resolver o GAP...  ← PROIBIDO! DEVE REPROVAR!
```

❌ ERRADO #3 (problema de infraestrutura - v1.4):
```
Analise do Problema

O codigo esta tecnicamente correto:
- AuthService armazena token corretamente
- auth.interceptor le token via getter
- Ordem dos interceptors esta correta

Este e um problema de infraestrutura de testes,
nao do codigo da funcionalidade.         ← PROIBIDO! NAO E DESCULPA!

STATUS.yaml: testes.e2e: partial         ← PROIBIDO!
```

✅ CORRETO #1 (resolver dados e aprovar):
```
Resultado da Execucao

RESOLUCAO DE DADOS:
- Problema: Tabela SistemaParametroCategorias vazia
- Acao: Executado seed via API POST
- Resultado: 3 categorias criadas
- Status: Dados prontos para testes

TESTES E2E:
| Passo | UC | Resultado | Observacao |
| 1 | UC00 | PASSOU | Listagem carregou |
| 2 | UC01 | PASSOU | Criacao OK (apos resolver dados) |
| 3 | UC02 | PASSOU | Visualizacao OK |
| 4 | UC03 | PASSOU | Edicao OK |
| 5 | UC04 | PASSOU | Exclusao OK |

Taxa de Aprovacao: 100%
STATUS.yaml: testes.e2e: done
RESULTADO FINAL: APROVADO
```

✅ CORRETO #2 (problema de auth - reprovar com responsabilidade - v1.4):
```
Resultado da Execucao

TESTES E2E:
| Passo | UC | Resultado | Observacao |
| 1 | Login | PASSOU | Token obtido |
| 2 | UC00 | FALHOU | 401 Unauthorized |
| 3 | UC01 | FALHOU | 401 Unauthorized |

INVESTIGACAO DE FALHA:
- Sintoma: Requests sem header Authorization
- Evidencia: Network tab mostra Bearer ausente
- Analise: auth.interceptor.ts nao adiciona header

RESPONSABILIDADE ATRIBUIDA:
- Componente: FRONTEND (auth.interceptor.ts)
- Arquivo: src/app/core/auth/auth.interceptor.ts
- Linha provavel: 45-60 (logica de adicao de header)

ACAO NECESSARIA:
Executar prompt de manutencao para corrigir auth.interceptor.ts

Taxa de Aprovacao: 33%
STATUS.yaml: testes.e2e: failed
STATUS.yaml: testes_ti.motivo_reprovacao: AUTH_INTERCEPTOR_FALHA
RESULTADO FINAL: REPROVADO
```
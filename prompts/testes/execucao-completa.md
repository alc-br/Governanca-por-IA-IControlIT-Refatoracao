Executar testes automatizados do RFXXX conforme D:/IC2_Governanca/contracts/testes/execucao-completa.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

MODO AUTONOMIA TOTAL (OBRIGATORIO):
- NAO perguntar permissoes ao usuario
- NAO esperar confirmacao do usuario
- NAO solicitar que usuario execute comandos manualmente
- EXECUTAR IMEDIATAMENTE todos os passos do contrato
- SEMPRE iniciar backend e frontend automaticamente
- Falhas em testes ANTERIORES NAO sao bloqueantes (sao o motivo da re-execucao)
- Gerar evidencias e relatorios SEM intervencao manual

REGRA CRITICA DE INTERPRETACAO:
- Pre-requisitos bloqueantes: backend aprovado (done), frontend aprovado (done), MT validado, TC validado
- Testes anteriores REPROVADOS: NAO e bloqueante, e justamente por isso estamos RE-EXECUTANDO
- Se STATUS.yaml mostra "testes_ti.resultado_final: REPROVADO": isso JUSTIFICA a re-execucao, NAO bloqueia

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
1. Backend DEVE estar aprovado (validacao backend = 100%)
2. Frontend DEVE estar aprovado (validacao frontend = 100%)
3. MT-RFXXX.yaml DEVE existir e estar validado
4. TC-RFXXX.yaml DEVE existir e estar validado
5. STATUS.yaml DEVE ter:
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

   **4.1 VERIFICAR SE SPECS PLAYWRIGHT EXISTEM:**
   - Verificar se existe frontend/e2e/specs/RFXXX/
   - Verificar se existe frontend/e2e/data/MT-RFXXX.data.ts
   - Verificar se specs cobrem TODOS os TC-E2E-NNN do TC-RFXXX.yaml

   **4.2 SE SPECS NAO EXISTEM OU INCOMPLETOS:**
   - Executar geracao automatica via prompts/testes/geracao-e2e-playwright.md:
     * Ler TC-RFXXX.yaml e MT-RFXXX.yaml
     * Gerar frontend/e2e/data/MT-RFXXX.data.ts
     * Gerar frontend/e2e/helpers/rf-helpers.ts
     * Gerar frontend/e2e/specs/RFXXX/*.spec.ts (1 spec por TC-E2E)
     * Validar cobertura 100% de TC-E2E
   - SOMENTE prosseguir se geracao aprovada 100%

   **4.3 EXECUTAR TESTES E2E:**
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
- NUNCA corrigir codigo diretamente
- SEMPRE gerar prompt de correcao quando encontrar problemas
- Exibir prompt completo na tela para usuario copiar

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
8. Executar testes E2E (npm run e2e)
9. Executar testes de seguranca
10. Consolidar resultados
11. Atribuir responsabilidade em falhas
12. Gerar relatorio consolidado
13. Gerar evidencias (screenshots, logs)
14. Atualizar azure-test-cases-RF[XXX].csv (State conforme resultado)
15. Atualizar STATUS.yaml (incluindo testes.azure_devops)
16. Registrar decisao (APROVADO/REPROVADO)

PROIBIDO:
- Executar apenas subset de testes
- Pular testes que falharam
- Modificar testes para fazer passar
- Marcar como APROVADO se taxa < 100%
- Alterar codigo de producao durante testes
- Executar testes sem buildar antes
- Executar testes sem seeds aplicados

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
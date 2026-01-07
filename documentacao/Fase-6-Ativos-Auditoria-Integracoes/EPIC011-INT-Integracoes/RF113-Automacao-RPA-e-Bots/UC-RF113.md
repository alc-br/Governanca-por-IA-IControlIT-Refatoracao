# UC-RF113 - Casos de Uso - Automação RPA e Bots

**Versão**: 1.0
**Data**: 2025-12-29
**RF Relacionado**: RF113 - Automação RPA e Bots
**EPIC**: EPIC011-INT-Integracoes
**Módulo**: Robotic Process Automation e Chatbots

---

## UC01: Configurar e Agendar Bot de Download de Faturas com Credenciais Criptografadas

### 1. Descrição

Este caso de uso permite que administradores RPA configurem um bot para download automático de faturas de operadoras telecom (Vivo, Claro, TIM, Oi, Embratel), definindo credenciais de acesso, parâmetros de execução (timeout, retries) e agendamento recorrente via expressão CRON. As credenciais são criptografadas com AES-256-CBC antes de persistir no banco de dados, garantindo segurança conforme LGPD.

### 2. Atores

- **Usuário autenticado** com permissão `rpa:bot:create`, `rpa:bot:schedule`, `rpa:credential:manage`
- **Sistema** (backend .NET 10, Hangfire, EF Core, Azure Key Vault)

### 3. Pré-condições

- Usuário autenticado com perfil Admin ou RPA Specialist
- Permissões: `rpa:bot:create`, `rpa:bot:schedule`, `rpa:credential:manage`
- Multi-tenancy ativo (ClienteId válido no contexto)
- Feature flag `RPA_AUTOMATION_ENGINE` habilitada
- Azure Key Vault configurado com master key para criptografia

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Automação → Bots de RPA | - |
| 2 | Clica em "Criar Novo Bot" | - |
| 3 | - | Valida permissões RBAC: `rpa:bot:create` → Se negado: HTTP 403 |
| 4 | - | Exibe formulário de criação: Nome, Descrição, Tipo (dropdown: Download/Email/WebForm/Chatbot), Schedule (CRON), Timeout (60-3600s), MaxRetries (0-5) |
| 5 | Preenche formulário: Nome = "Bot Download Vivo", Tipo = "Download", Schedule = "0 2 * * 2" (terças 2h), Timeout = 900s, MaxRetries = 2 | - |
| 6 | Preenche seção "Configuração": Operadora = "Vivo", Portal URL = "https://portal.vivo.com.br", Tipo Autenticação = "CPF+Senha" | - |
| 7 | Preenche seção "Credenciais Criptografadas": Username = "12345678900", Password = "senha123" (campo type="password") | - |
| 8 | Clica em "Salvar" | - |
| 9 | - | Frontend executa POST `/api/rpa/bots` com body JSON: `{ nome, descricao, tipo, scheduleExpression, timeoutSeconds, maxRetries, configuracao: { operadora, portal_url }, credenciais: { username, password } }` |
| 10 | - | Backend valida campos obrigatórios: Nome, Tipo, Configuração → Se inválido: HTTP 400 "Nome é obrigatório" |
| 11 | - | Backend valida expressão CRON usando CronExpression.Parse(scheduleExpression) → Se inválido: HTTP 400 "Expressão CRON inválida" |
| 12 | - | Backend valida timeout: DEVE estar entre 60 e 3600 segundos → Se fora: HTTP 400 "Timeout deve ser entre 60 e 3600 segundos" |
| 13 | - | **Criptografia de Credenciais**: Backend invoca BotCredentialEncryptor.EncryptCredential(username, masterKey) e EncryptCredential(password, masterKey) usando Rfc2898DeriveBytes (PBKDF2 100k iterations) + AES-256-CBC |
| 14 | - | Backend gera IV (Initialization Vector) aleatório de 16 bytes, executa encryptor.TransformFinalBlock(), concatena IV + ciphertext, converte para Base64 |
| 15 | - | Backend cria entidade RpaBot: Id = BotId.New(), ClienteId = _currentClientProvider.GetCurrentClientId(), Nome, Tipo, Status = "Ativo", ConfiguracaoJson = JsonConvert.SerializeObject(configuracao), CredenciaisEncriptadas = JsonConvert.SerializeObject({ usernameEncrypted, passwordEncrypted }), ScheduleExpression, TimeoutSeconds, MaxRetries |
| 16 | - | Backend valida multi-tenancy: if (bot.ClienteId == Guid.Empty) throw InvalidOperationException("ClienteId must be set") |
| 17 | - | Backend persiste no BD: `INSERT INTO RPA_Bot (Id, ClienteId, Nome, Tipo, Status, ConfiguracaoJson, CredenciaisEncriptadas, ScheduleExpression, TimeoutSeconds, MaxRetries, DataCriacao, CriadoPor)` |
| 18 | - | **Agendamento Hangfire**: Backend registra job recorrente: RecurringJob.AddOrUpdate<ExecuteBotJob>(bot.Id.ToString(), x => x.ExecuteAsync(bot.Id), bot.ScheduleExpression) |
| 19 | - | Backend registra auditoria: AuditLog { EntityType = "RPA_Bot", ActionType = "RPA_BOT_CREATE", OldValues = null, NewValues = JSON do bot, Changes = "Bot criado com credenciais criptografadas" } |
| 20 | - | Retorna HTTP 201 Created com BotResponse: `{ id, nome, tipo, status, scheduleExpression, proximaExecucao: "2025-12-30T02:00:00Z" }` |
| 21 | Frontend exibe mensagem de sucesso i18n: `rpa.bots.messages.create_success` ("Bot criado com sucesso") e redireciona para lista de bots | - |
| 22 | - | Sistema armazena credenciais criptografadas no banco: CredenciaisEncriptadas = "eyJpdiI6IkFRSURBSGd4MGtWKy4uLiIsImNpcGhlciI6IjhyUGFkNy4uLiJ9" (Base64 JSON com IV + ciphertext) |

### 5. Fluxos Alternativos

**FA01: Usuário Seleciona Tipo "Chatbot"**
- No passo 5, usuário seleciona Tipo = "Chatbot"
- Sistema exibe campos específicos: Intent Threshold (0.5-1.0), Azure Bot Service URL, LUIS App ID
- Sistema oculta campo "Credenciais" (chatbot usa autenticação OAuth do Azure)
- Validação diferente: Não requer ScheduleExpression (chatbot responde a eventos, não agendamento)
- Sistema retorna para fluxo principal no passo 15

**FA02: Agendamento Complexo (Múltiplas Janelas)**
- No passo 5, usuário define Schedule = "0 2,14 * * 1,3,5" (segundas/quartas/sextas às 2h e 14h)
- Sistema valida expressão CRON multi-janela: CronExpression.Parse() → válido
- Sistema calcula próxima execução: CronExpression.GetNextOccurrence(DateTime.UtcNow) → próxima segunda 2h
- Sistema registra múltiplos jobs Hangfire com sufixos: `{botId}-window-1`, `{botId}-window-2`
- Sistema retorna para fluxo principal no passo 19

**FA03: Bot com Retry Desabilitado**
- No passo 5, usuário define MaxRetries = 0
- Sistema aceita configuração sem retry automático
- Validação: Bot será cancelado imediatamente se primeira execução falhar
- Sistema exibe warning: "Atenção: Retry desabilitado. Falhas cancelam bot sem tentativas adicionais"
- Sistema retorna para fluxo principal no passo 8

**FA04: Testar Credenciais Antes de Salvar**
- No passo 7, após preencher credenciais, usuário clica em "Testar Conexão"
- Frontend envia POST `/api/rpa/bots/testar-credenciais` com { operadora, portal_url, username, password } (NÃO criptografado, HTTPS only)
- Backend executa teste: tenta autenticar no portal da operadora com Playwright/Selenium
- Se sucesso: Retorna HTTP 200 "Autenticação bem-sucedida"
- Se falha: Retorna HTTP 400 "Credenciais inválidas ou portal indisponível"
- Sistema retorna para fluxo principal no passo 8

### 6. Exceções

**EX01: Usuário Sem Permissão rpa:bot:create**
- No passo 3, sistema valida RBAC
- Usuário não possui permissão `rpa:bot:create`
- Sistema retorna HTTP 403 Forbidden com body: `{ error: "PermissionDenied", message: "Você não tem permissão para criar bots" }`
- Frontend exibe mensagem de erro i18n: `common.errors.permission_denied`
- Fluxo termina

**EX02: Expressão CRON Inválida**
- No passo 11, backend valida CRON expression
- Usuário forneceu: "* * * * * * *" (7 campos, inválido)
- CronExpression.Parse() lança CronFormatException
- Sistema retorna HTTP 400 Bad Request: `{ error: "InvalidCronExpression", message: "Expressão CRON inválida. Formato esperado: 'minuto hora dia mês dia-semana'" }`
- Frontend exibe mensagem de validação i18n: `rpa.bots.validation.invalid_cron`
- Fluxo retorna ao passo 5

**EX03: Timeout Fora do Range Permitido**
- No passo 12, backend valida timeout
- Usuário forneceu: timeoutSeconds = 5000 (acima do máximo 3600)
- Sistema retorna HTTP 400: `{ error: "InvalidTimeout", message: "Timeout deve ser entre 60 e 3600 segundos" }`
- Frontend exibe validação inline no campo: `rpa.bots.validation.timeout_invalid`
- Fluxo retorna ao passo 5

**EX04: Falha ao Criptografar Credenciais (Master Key Indisponível)**
- No passo 13, backend tenta buscar master key do Azure Key Vault
- Azure Key Vault retorna HTTP 500 (indisponível)
- BotCredentialEncryptor.EncryptCredential() lança KeyVaultException
- Sistema retorna HTTP 503 Service Unavailable: `{ error: "EncryptionFailed", message: "Serviço de criptografia temporariamente indisponível" }`
- Backend registra log crítico: "ERRO: Azure Key Vault indisponível para criptografia de credenciais"
- Frontend exibe erro: "Não foi possível salvar o bot. Tente novamente em alguns minutos"
- Fluxo termina

**EX05: ClienteId Inválido (Violação de Multi-Tenancy)**
- No passo 16, backend valida multi-tenancy
- _currentClientProvider.GetCurrentClientId() retorna Guid.Empty (sessão corrompida)
- Sistema lança InvalidOperationException("ClienteId must be set")
- Sistema retorna HTTP 500 Internal Server Error: `{ error: "MultiTenancyViolation", message: "Erro de contexto de cliente" }`
- Backend registra alerta de segurança crítico: "SECURITY: Tentativa de criar bot sem ClienteId válido"
- Fluxo termina

### 7. Pós-condições

- Bot criado e persistido na tabela RPA_Bot com Status = "Ativo"
- Credenciais armazenadas criptografadas com AES-256-CBC (não reversível sem master key)
- Job recorrente registrado no Hangfire com próxima execução calculada
- Auditoria registrada em AuditLog com ActionType = "RPA_BOT_CREATE"
- Próxima execução agendada para o horário definido no CRON (ex: terça 2h UTC)
- Query filter EF Core garante isolamento por ClienteId automaticamente

### 8. Regras de Negócio Aplicáveis

- **RN-RPA-113-01**: Criptografia de Credenciais do Bot (AES-256-CBC, PBKDF2 100k iterations, master key do Azure Key Vault)
- **RN-RPA-113-02**: Timeout de Execução do Bot (15 minutos máximo, cancelamento automático se exceder)
- **RN-RPA-113-08**: Multi-Tenancy em Execução de Bots (ClienteId obrigatório, query filter automático)
- **RN-RPA-113-10**: Auditoria Completa de Execuções e Ações de Bots (registro de criação, alteração, execução com timestamp e usuário)

---

## UC02: Executar Bot Manualmente com Timeout e Retry Automático

### 1. Descrição

Este caso de uso permite que operadores RPA executem um bot imediatamente (sem aguardar agendamento), com controle de timeout de 15 minutos e retry automático com backoff exponencial em caso de falhas transitórias (timeout, erros 5xx de API externa). A execução é enfileirada com status "Pendente", processada por worker de background, e logs estruturados são registrados para auditoria.

### 2. Atores

- **Usuário autenticado** com permissão `rpa:bot:execute`
- **Sistema** (backend .NET 10, Hangfire workers, EF Core, Serilog)

### 3. Pré-condições

- Usuário autenticado com perfil Admin, RPA Specialist ou Operador
- Permissão: `rpa:bot:execute`
- Bot existe e tem Status = "Ativo"
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `RPA_AUTOMATION_ENGINE` habilitada
- Hangfire Server rodando para processar fila de execuções

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa lista de bots em Automação → Bots de RPA | - |
| 2 | Localiza bot "Bot Download Vivo" e clica em ação "Executar Agora" | - |
| 3 | - | Valida permissão RBAC: `rpa:bot:execute` → Se negado: HTTP 403 |
| 4 | - | Frontend exibe modal de confirmação: "Executar bot 'Bot Download Vivo' agora?" com botões [Cancelar] [Executar] |
| 5 | Clica em "Executar" | - |
| 6 | - | Frontend executa POST `/api/rpa/bots/{botId}/executar` |
| 7 | - | Backend valida que bot existe e pertence ao ClienteId do usuário via query filter: `_context.Bots.FirstOrDefaultAsync(b => b.Id == botId)` → Se não encontrado: HTTP 404 |
| 8 | - | Backend valida que bot está ativo: if (bot.Status != "Ativo") return HTTP 400 "Bot está inativo e não pode ser executado" |
| 9 | - | Backend cria RpaBotExecution: Id = Guid.NewGuid(), ClienteId = bot.ClienteId, BotId = bot.Id, Status = "Pendente", DataInicio = DateTime.UtcNow, TriggeredBy = "Manual", TentativaAtual = 1 |
| 10 | - | Backend persiste: `INSERT INTO RPA_BotExecution (Id, ClienteId, BotId, Status, DataInicio, TriggeredBy, TentativaAtual)` |
| 11 | - | Backend enfileira job Hangfire: BackgroundJob.Enqueue<ExecuteBotJob>(x => x.ExecuteAsync(execution.Id)) |
| 12 | - | Backend registra auditoria START: AuditLog { EntityType = "RPA_Bot_Execution", ActionType = "START", NewValues = JSON { executionId, botId, status, dataInicio } } |
| 13 | - | Retorna HTTP 202 Accepted com body: `{ executionId, status: "Pendente", dataCriacao, message: "Execução enfileirada, status será atualizado em tempo real" }` |
| 14 | Frontend exibe mensagem de sucesso i18n: `rpa.bots.messages.execution_started` e atualiza lista de execuções via SignalR ou polling | - |
| 15 | - | **Worker Hangfire processa fila**: ExecuteBotJob.ExecuteAsync(executionId) é invocado |
| 16 | - | Worker carrega RpaBotExecution do BD: `_context.BotExecutions.Include(e => e.Bot).FirstOrDefaultAsync(e => e.Id == executionId)` |
| 17 | - | Worker atualiza status: execution.Status = "Executando", execution.DataInicio = DateTime.UtcNow, persiste via SaveChangesAsync() |
| 18 | - | **Aplicação de Timeout**: Worker cria CancellationTokenSource.CancelAfter(bot.TimeoutSeconds * 1000) → 900s (15 min) |
| 19 | - | Worker descriptografa credenciais: BotCredentialEncryptor.DecryptCredential(bot.CredenciaisEncriptadas, masterKey) → recupera username/password em plain text |
| 20 | - | **Execução do Bot**: Worker invoca lógica específica por tipo (ex: DownloadBotExecutor.ExecuteAsync(bot, credenciais, cancellationToken)) |
| 21 | - | DownloadBotExecutor: Inicializa Playwright, navega para portal da operadora, preenche login (username/password), clica em "Entrar" |
| 22 | - | DownloadBotExecutor registra log: `_executionLogRepository.AddAsync(new RpaBotExecutionLog { ExecutionId, Nivel = "Info", Mensagem = "Autenticando no portal da Vivo..." })` |
| 23 | - | DownloadBotExecutor: Localiza seção "Minhas Faturas", extrai lista de 3 faturas disponíveis (com links), itera sobre cada uma |
| 24 | - | Para cada fatura: Clica em link download, aguarda response, valida Content-Type = "application/pdf", salva em Azure Blob Storage |
| 25 | - | Para cada fatura: Calcula SHA256 checksum usando FileIntegrityValidator.ComputeFileChecksumAsync(stream) |
| 26 | - | DownloadBotExecutor registra log: `Mensagem = "Validação de checksum: OK para fatura_2025_01.pdf"` |
| 27 | - | DownloadBotExecutor conclui: retorna BotExecutionResult { IsSuccess = true, Message = "3 faturas baixadas com sucesso", Data = JSON com lista de faturas } |
| 28 | - | Worker atualiza RpaBotExecution: Status = "Sucesso", DataFim = DateTime.UtcNow, DuracaoSegundos = (DataFim - DataInicio).TotalSeconds, ResultadoJson = JsonConvert.SerializeObject(result.Data) |
| 29 | - | Worker persiste via SaveChangesAsync(), registra auditoria END: AuditLog { ActionType = "RPA_EXECUTION_END", NewValues = JSON { status, duracaoSegundos, resultadoJson } } |
| 30 | - | Worker envia notificação SignalR para frontend: `_hubContext.Clients.Group(clienteId).SendAsync("BotExecutionCompleted", { executionId, status: "Sucesso" })` |
| 31 | Frontend atualiza timeline de execuções em tempo real: exibe card verde com ícone ✅, duração "8 min 30 seg", 3 faturas baixadas | - |

### 5. Fluxos Alternativos

**FA01: Bot Falha com Erro Transitório (Timeout de Rede) → Retry Automático**
- No passo 21, DownloadBotExecutor tenta navegar para portal da operadora
- HttpClient lança TimeoutException após 30 segundos (portal lento)
- BotRetryPolicy.ExecuteWithRetryAsync() detecta erro transitório: IsTransientException(TimeoutException) → true
- Worker registra log: `Nivel = "Warning", Mensagem = "Tentativa 1 falhou com timeout, aguardando 5 minutos para retry"`
- Worker aguarda Task.Delay(300000) → 5 minutos
- Worker incrementa execution.TentativaAtual = 2, atualiza no BD
- Worker reexecuta DownloadBotExecutor.ExecuteAsync() (retry 1)
- Se sucesso: retorna para fluxo principal no passo 27
- Se falha novamente: aguarda 10 minutos (backoff exponencial), retry 2 (último)
- Se falha após retry 2: Status = "Erro", MensagemErro = "Timeout após 2 tentativas", retorna para EX02

**FA02: Execução Excede Timeout de 15 Minutos → Cancelamento Automático**
- No passo 21, DownloadBotExecutor está processando download de fatura muito grande (500 MB)
- Após 15 minutos, CancellationTokenSource dispara cancellationToken.IsCancellationRequested = true
- DownloadBotExecutor lança OperationCanceledException
- BotExecutionService.ExecuteWithTimeoutAsync() captura exceção
- Worker retorna BotExecutionResult { IsSuccess = false, ErrorCode = BotErrorCode.Timeout, Message = "Bot excedeu timeout de 900 segundos" }
- Worker atualiza RpaBotExecution: Status = "Erro", DataFim = DateTime.UtcNow, MensagemErro = "Timeout após 15 minutos", CodigoErro = "Timeout"
- Worker valida constraint SQL: DATEDIFF(SECOND, DataInicio, DataFim) <= 900 → 900 segundos exatos (aprovado)
- Worker registra auditoria: ActionType = "RPA_EXECUTION_TIMEOUT"
- Worker envia notificação para admin: Email SMTP ou Teams webhook com mensagem "Bot 'Bot Download Vivo' excedeu timeout de execução"
- Fluxo termina com Status = "Erro"

**FA03: Bot Requer Aprovação para Ação Crítica (Pagamento de Fatura)**
- No passo 20, DownloadBotExecutor completa download de faturas
- Bot identifica ação adicional configurada: "Executar pagamento automático se fatura <= R$ 1000"
- Bot invoca CriticalActionApprovalWorkflow.RequiresApprovalAsync(BotAction { Type = PaymentExecution })
- Workflow detecta ação crítica, cria WorkflowApproval: Id, ExecutionId, Type = BotCriticalAction, RequiredApprovers = 2, Status = "Pending"
- Workflow persiste: `INSERT INTO WorkflowApproval (Id, ExecutionId, Type, RequiredApprovers, Status, DataCriacao)`
- Workflow notifica 2 admins via Teams webhook: "Ação crítica de bot aguardando aprovação: Pagamento de fatura R$ 850,00"
- Worker pausa execução: execution.Status = "AguardandoAprovacao", persiste
- Admins aprovam via frontend: 2 assinaturas coletadas
- Workflow atualiza: approval.Status = "Approved", approval.ApprovedBy = JSON com IDs dos aprovadores
- Worker retoma execução, executa pagamento via API bancária
- Fluxo retorna ao passo 27

### 6. Exceções

**EX01: Usuário Sem Permissão rpa:bot:execute**
- No passo 3, sistema valida RBAC
- Usuário não possui permissão `rpa:bot:execute`
- Sistema retorna HTTP 403: `{ error: "PermissionDenied", message: "Você não tem permissão para executar bots" }`
- Fluxo termina

**EX02: Bot com Credenciais Inválidas (Falha de Autenticação no Portal)**
- No passo 21, DownloadBotExecutor tenta autenticar
- Portal da operadora retorna HTTP 401 Unauthorized (credenciais inválidas)
- BotRetryPolicy detecta erro NÃO transitório: IsTransientError(AuthFailed) → false
- Worker não aplica retry (erro crítico)
- Worker atualiza RpaBotExecution: Status = "Erro", MensagemErro = "Credenciais inválidas para operadora Vivo", CodigoErro = "AuthFailed"
- Worker registra log: `Nivel = "Error", Mensagem = "Falha de autenticação: credenciais inválidas"`
- Worker envia notificação para admin: "Bot 'Bot Download Vivo' falhou. Verifique credenciais"
- Worker registra auditoria: ActionType = "RPA_EXECUTION_ERROR"
- Fluxo termina com Status = "Erro"

**EX03: Falha ao Descriptografar Credenciais (Master Key Inválida)**
- No passo 19, Worker tenta descriptografar credenciais
- BotCredentialEncryptor.DecryptCredential() lança CryptographicException (master key rotacionada/inválida)
- Worker captura exceção, atualiza RpaBotExecution: Status = "Erro", MensagemErro = "Falha ao descriptografar credenciais", CodigoErro = "DecryptionFailed"
- Worker registra log crítico: "ERRO CRÍTICO: Falha na descriptografia de credenciais, revisar Azure Key Vault"
- Worker envia alerta para admin
- Fluxo termina

**EX04: Validação de Checksum Falha (Arquivo Corrompido)**
- No passo 25, DownloadBotExecutor calcula checksum SHA256
- Checksum computado: "a1b2c3d4..." não corresponde ao esperado: "e5f6g7h8..."
- FileIntegrityValidator lança FileIntegrityException("Checksum mismatch")
- DownloadBotExecutor rejeita fatura, registra log: `Nivel = "Error", Mensagem = "Checksum inválido para fatura_2025_01.pdf, arquivo rejeitado"`
- Bot continua processando próximas faturas (não cancela execução total)
- Ao final: execution.Status = "Sucesso" (parcial), ResultadoJson = "2 de 3 faturas baixadas, 1 rejeitada por checksum inválido"
- Worker registra auditoria com detalhes de falha parcial
- Fluxo retorna ao passo 28 com resultado parcial

### 7. Pós-condições

- RpaBotExecution criada com Status final: "Sucesso", "Erro" ou "AguardandoAprovacao"
- Logs estruturados registrados em RPA_BotExecutionLog (Info, Warning, Error) com timestamps
- Auditoria completa registrada: START, ações internas, END ou ERROR
- Arquivos baixados (faturas) armazenados em Azure Blob Storage com checksum validado
- Notificações enviadas para admin em caso de falha ou timeout
- Métricas atualizadas: taxa de sucesso, tempo médio de execução, erros comuns

### 8. Regras de Negócio Aplicáveis

- **RN-RPA-113-02**: Timeout de Execução do Bot (15 minutos máximo, cancelamento com status ERROR)
- **RN-RPA-113-03**: Retry Automático com Backoff Exponencial (max 2 retries, delay 5 min → 10 min, apenas erros transitórios)
- **RN-RPA-113-05**: Validação de Checksum de Arquivos Baixados (SHA256, rejeita se mismatch)
- **RN-RPA-113-09**: Aprovação Humana para Ações Críticas (workflow com 2 assinaturas para pagamento, exclusão)
- **RN-RPA-113-10**: Auditoria Completa de Execuções e Ações de Bots (registro START, END, TIMEOUT, ERROR)

---

## UC03: Interagir com Chatbot de Suporte com NLP e Escalonamento Automático

### 1. Descrição

Este caso de uso permite que qualquer usuário autenticado converse com um chatbot de suporte baseado em IA (Azure Bot Service + LUIS) para obter respostas sobre FAQ, status de ativos, informações de tickets, etc. O chatbot analisa a pergunta usando NLP, detecta a intenção (intent) e confiança (score 0-1.0). Se confiança >= 70%, responde automaticamente. Se < 70%, escala para atendimento humano criando ticket de suporte.

### 2. Atores

- **Usuário autenticado** (qualquer perfil)
- **Sistema** (backend .NET 10, Azure Bot Service, LUIS NLP, EF Core)

### 3. Pré-condições

- Usuário autenticado (qualquer permissão, chatbot disponível para todos)
- Feature flag `CHATBOT_INTEGRATION` habilitada
- Azure Bot Service configurado e acessível
- LUIS app treinado com intents: asset_reactivation, ticket_status, faq_pricing, contract_renewal, etc.
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa widget de chatbot no canto inferior direito (ícone 💬) | - |
| 2 | Clica no ícone, widget expande exibindo histórico de conversas (vazio se primeira vez) | - |
| 3 | Digita pergunta no campo de texto: "Como faço para reativar meu notebook?" | - |
| 4 | Clica em "Enviar" (ou pressiona Enter) | - |
| 5 | - | Frontend exibe mensagem do usuário no chat, adiciona animação "Digitando..." abaixo |
| 6 | - | Frontend executa POST `/api/chatbot/conversa` com body: `{ userQuery: "Como faço para reativar meu notebook?", conversationId: "abc123" }` |
| 7 | - | Backend valida que usuário está autenticado (via JWT token) → Se não: HTTP 401 |
| 8 | - | Backend cria ou recupera conversationId: se novo, gera Guid.NewGuid(), se existente, usa o fornecido |
| 9 | - | **Chamada LUIS NLP**: Backend invoca LuisClient.RecognizeAsync<BotIntents>(userQuery) |
| 10 | - | LUIS analisa texto: "Como faço para reativar meu notebook?" → Detecta intent: "asset_reactivation" com score 0.89 (89% confiança) |
| 11 | - | LUIS extrai entities: AssetType = "notebook" |
| 12 | - | Backend recebe LuisResult: `{ topIntent: "asset_reactivation", score: 0.89, entities: { assetType: "notebook" } }` |
| 13 | - | **Validação de Confiança**: if (result.Score >= 0.70) → Confiança suficiente, responder automaticamente |
| 14 | - | Backend invoca GetResponseForIntent("asset_reactivation", entities) → Busca resposta pre-definida do banco ou knowledge base |
| 15 | - | Backend monta resposta: "Para reativar seu notebook, você pode:\n1. Acessar o menu Ativos > Notebooks\n2. Localizar seu notebook\n3. Clicar em 'Reativar'\n\nPrecisa de mais ajuda?" |
| 16 | - | Backend cria ChatbotConversation: Id, ClienteId, UserId, UserQuery, ChatbotResponse, IntentDetected = "asset_reactivation", ConfidenceScore = 0.89, EscaledToHuman = false, DataCriacao |
| 17 | - | Backend persiste: `INSERT INTO Chatbot_Conversation (Id, ClienteId, UserId, UserQuery, ChatbotResponse, IntentDetected, ConfidenceScore, EscaledToHuman, DataCriacao)` |
| 18 | - | Backend registra auditoria: AuditLog { EntityType = "Chatbot_Interaction", ActionType = "CHATBOT_QUERY", OldValues = JSON { userQuery }, NewValues = JSON { chatbotResponse, intentDetected, confidenceScore } } |
| 19 | - | Retorna HTTP 200 OK com body: `{ conversationId: "abc123", userQuery, chatbotResponse, intentDetected, confidenceScore: 0.89, escalatedToHuman: false, suggestedTopics: ["Renovação de Contrato", "Suporte Técnico"] }` |
| 20 | Frontend remove animação "Digitando...", exibe resposta do chatbot com ícone 🤖, score 89% exibido discretamente | - |
| 21 | - | Frontend atualiza histórico de conversas no widget (scroll automático para última mensagem) |
| 22 | Usuário lê resposta e clica em "Renovação de Contrato" (suggested topic) | - |
| 23 | - | Frontend envia nova query para `/api/chatbot/conversa` com userQuery = "Renovação de Contrato" (query pré-formatada) |

### 5. Fluxos Alternativos

**FA01: Confiança Baixa (<70%) → Escalonamento para Atendimento Humano**
- No passo 10, LUIS analisa query: "Blabla xyz" → Nenhum intent claro detectado, score = 0.35 (35% confiança)
- No passo 13, backend valida: if (result.Score < 0.70) → Confiança insuficiente
- Backend invoca ExtractIntentSuggestions(result) → Busca intents com score >= 0.5: ["ticket_status" (0.55), "faq_pricing" (0.51)]
- Backend monta resposta de escalonamento: "Não consegui entender sua pergunta com certeza suficiente. Um agente de suporte foi escalado para ajudar."
- Backend cria ticket de suporte automaticamente: POST `/api/tickets` com body: `{ titulo: "Chatbot escalado: {userQuery}", descricao: "Usuário perguntou: {userQuery}. Intent detectado (baixa confiança): {intents}", prioridade: "Média", status: "Aberto" }`
- Backend atualiza ChatbotConversation: EscaledToHuman = true, TicketId = ticket.Id criado
- Backend retorna HTTP 200: `{ chatbotResponse: "Um agente foi acionado", escalatedToHuman: true, suggestedTopics: ["Status de Ticket", "Preços e Planos"], ticketId }` |
- Frontend exibe mensagem de escalonamento i18n: `rpa.chatbot.escalation` + link para ticket criado: "Acompanhe seu ticket #12345"
- Fluxo termina (próxima mensagem do usuário cria nova conversação)

**FA02: Usuário Faz Pergunta com Múltiplas Intenções (Disambiguation)**
- No passo 10, LUIS analisa: "Como reativo notebook E renovo contrato?"
- LUIS detecta 2 intents: "asset_reactivation" (0.72), "contract_renewal" (0.78)
- Backend identifica múltiplos intents com score > 0.70
- Backend monta resposta de disambiguação: "Identifiquei duas perguntas:\n1. Reativar notebook\n2. Renovar contrato\n\nQual gostaria de saber primeiro?"
- Backend adiciona botões interativos (Quick Replies): ["Reativar Notebook"] ["Renovar Contrato"]
- Frontend exibe botões, usuário clica em um deles
- Frontend reenvia query específica para `/api/chatbot/conversa`
- Fluxo retorna ao passo 9 com query refinada

**FA03: Chatbot Responde com Dados Dinâmicos (Status de Ativo)**
- No passo 10, LUIS detecta intent: "asset_status" (0.88), entities: { assetType: "notebook", assetId: "12345" }
- Backend invoca GetResponseForIntent("asset_status") → Consulta banco de dados para buscar status real do ativo
- Backend executa: `_ativoRepository.GetByIdAsync(assetId, clienteId)` → Retorna Ativo { Nome, Status, LocalAtual, DataUltimaMovimentacao }
- Backend monta resposta dinâmica: "Seu notebook (ID: 12345) está:\n- Status: Ativo\n- Local: Escritório SP - Andar 3\n- Última movimentação: 2025-12-15"
- Backend retorna resposta personalizada (não template genérico)
- Fluxo retorna ao passo 16

### 6. Exceções

**EX01: Usuário Não Autenticado Tenta Acessar Chatbot**
- No passo 7, backend valida token JWT
- Token ausente ou expirado
- Sistema retorna HTTP 401 Unauthorized: `{ error: "Unauthorized", message: "Você precisa estar logado para usar o chatbot" }`
- Frontend redireciona para login
- Fluxo termina

**EX02: LUIS Serviço Indisponível (Azure Offline)**
- No passo 9, backend tenta invocar LuisClient.RecognizeAsync()
- HttpClient lança HttpRequestException: "503 Service Unavailable"
- Backend captura exceção, registra log: `Nivel = "Error", Mensagem = "LUIS service unavailable"`
- Backend usa fallback: Retorna resposta genérica "Desculpe, estou temporariamente indisponível. Tente novamente em alguns minutos."
- Backend atualiza ChatbotConversation: EscaledToHuman = false, IntentDetected = null, ConfidenceScore = null
- Sistema retorna HTTP 200 com resposta de fallback
- Frontend exibe mensagem de erro i18n: `rpa.chatbot.service_unavailable`
- Fluxo termina (não escala para humano, erro técnico)

**EX03: Pergunta com Linguagem Inadequada ou Ofensiva**
- No passo 10, LUIS detecta entities marcadas como "offensive_language" (filtro pré-treinado)
- Backend valida: if (result.Entities.Contains("offensive_language")) → true
- Backend monta resposta: "Por favor, mantenha uma linguagem respeitosa. Caso precise de ajuda, reformule sua pergunta."
- Backend NÃO registra auditoria com conteúdo ofensivo (LGPD: dado sensível)
- Backend registra auditoria genérica: ActionType = "CHATBOT_QUERY_BLOCKED", Changes = "Query bloqueada por linguagem inadequada"
- Sistema retorna HTTP 200 com mensagem de advertência
- Fluxo termina sem resposta útil

### 7. Pós-condições

- Interação registrada em Chatbot_Conversation com UserQuery, ChatbotResponse, IntentDetected, ConfidenceScore
- Auditoria registrada em AuditLog com ActionType = "CHATBOT_QUERY"
- Se escalado: Ticket criado em sistema de Service Desk com TicketId vinculado
- Métricas atualizadas: taxa de escalonamento, tempo médio de resposta, intents mais consultados
- Histórico de conversas persistido para análise e treinamento futuro do modelo LUIS

### 8. Regras de Negócio Aplicáveis

- **RN-RPA-113-06**: Taxa de Confiança Mínima de Chatbot (NLP) (>= 70% para resposta automática, < 70% escala para humano)
- **RN-RPA-113-08**: Multi-Tenancy em Execução de Bots (ClienteId obrigatório em ChatbotConversation)
- **RN-RPA-113-10**: Auditoria Completa de Execuções e Ações de Bots (registro de queries, respostas, escalações)

---

## UC04: Monitorar Execuções de Bots com Dashboard em Tempo Real e Métricas RED

### 1. Descrição

Este caso de uso permite que administradores RPA monitorem em tempo real o status de execuções de bots, visualizem métricas agregadas (taxa de sucesso, tempo médio de execução, erros mais comuns), recebam alertas de falhas, e consultem logs estruturados de cada execução. O dashboard exibe métricas RED (Rate, Errors, Duration) e atualiza automaticamente via SignalR.

### 2. Atores

- **Usuário autenticado** com permissão `rpa:bot:read`, `rpa:execution:read`
- **Sistema** (backend .NET 10, SignalR Hub, EF Core, Serilog)

### 3. Pré-condições

- Usuário autenticado com perfil Admin ou RPA Specialist
- Permissões: `rpa:bot:read`, `rpa:execution:read`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `RPA_AUTOMATION_ENGINE` habilitada
- SignalR Hub configurado e conectado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Automação → Dashboard de RPA | - |
| 2 | - | Valida permissões RBAC: `rpa:bot:read`, `rpa:execution:read` → Se negado: HTTP 403 |
| 3 | - | Frontend estabelece conexão SignalR: `_hubConnection.start()` com URL `/hubs/rpa` |
| 4 | - | SignalR Hub autentica usuário via JWT token, adiciona conexão ao grupo do ClienteId: `Groups.AddToGroupAsync(connectionId, clienteId)` |
| 5 | - | Frontend executa GET `/api/rpa/metricas` para buscar dados iniciais |
| 6 | - | Backend executa queries agregadas: Total bots ativos, total execuções últimos 7 dias, taxa de sucesso, tempo médio de execução |
| 7 | - | Query 1: `SELECT COUNT(*) FROM RPA_Bot WHERE ClienteId = @clienteId AND Status = 'Ativo' AND IsDeleted = 0` → totalBotsAtivos = 12 |
| 8 | - | Query 2: `SELECT COUNT(*) FROM RPA_BotExecution WHERE ClienteId = @clienteId AND DataInicio >= DATEADD(DAY, -7, GETUTCDATE())` → totalExecucoesUltimos7dias = 84 |
| 9 | - | Query 3: Taxa de sucesso: `SELECT (COUNT(CASE WHEN Status = 'Sucesso' THEN 1 END) * 1.0 / COUNT(*)) FROM RPA_BotExecution WHERE ClienteId = @clienteId AND DataInicio >= DATEADD(DAY, -7, GETUTCDATE())` → taxaSucessoTotal = 0.964 (96.4%) |
| 10 | - | Query 4: Tempo médio: `SELECT AVG(DuracaoSegundos) FROM RPA_BotExecution WHERE ClienteId = @clienteId AND Status = 'Sucesso' AND DataInicio >= DATEADD(DAY, -7, GETUTCDATE())` → tempoMedioExecucao = 450s (7.5 min) |
| 11 | - | Query 5: Erros mais comuns: `SELECT CodigoErro, COUNT(*) as Quantidade FROM RPA_BotExecution WHERE ClienteId = @clienteId AND Status = 'Erro' AND DataInicio >= DATEADD(DAY, -7, GETUTCDATE()) GROUP BY CodigoErro ORDER BY Quantidade DESC` → `[{ tipo: "Timeout", quantidade: 3 }, { tipo: "AuthFailed", quantidade: 1 }]` |
| 12 | - | Backend monta resposta JSON com métricas agregadas + array de métricas por bot (join com RPA_Bot) |
| 13 | - | Retorna HTTP 200 OK com body: `{ totalBotsAtivos: 12, totalExecucoesUltimos7dias: 84, taxaSucessoTotal: 0.964, tempoMedioExecucao: 450, errosMaisComunsUltimo7dias: [...], metricas_por_bot: [...] }` |
| 14 | Frontend renderiza dashboard: 4 cards principais (KPIs) no topo: [Total Bots Ativos: 12] [Execuções 7d: 84] [Taxa Sucesso: 96.4% 🟢] [Tempo Médio: 7.5 min] | - |
| 15 | Frontend renderiza gráfico de barras (Chart.js): "Erros Mais Comuns" com 2 barras: Timeout (3), AuthFailed (1) | - |
| 16 | Frontend renderiza tabela "Métricas por Bot" com colunas: [Bot] [Execuções 7d] [Sucessos] [Falhas] [Tempo Médio] | - |
| 17 | - | **Atualização em Tempo Real**: Worker backend completa execução de bot (UC02) |
| 18 | - | Worker invoca SignalR Hub: `_hubContext.Clients.Group(clienteId).SendAsync("BotExecutionCompleted", { executionId, botId, status: "Sucesso", duracaoSegundos: 510 })` |
| 19 | Frontend escuta evento SignalR: `_hubConnection.on("BotExecutionCompleted", (data) => { ... })` | - |
| 20 | Frontend atualiza dashboard automaticamente: Incrementa contador "Execuções 7d" (84 → 85), recalcula taxa de sucesso (96.4% → 96.5%), atualiza linha da tabela para bot específico | - |
| 21 | Frontend exibe notificação toast no canto superior direito: "Bot 'Bot Download Vivo' concluído com sucesso em 8.5 minutos" (auto-dismiss após 5s) | - |
| 22 | Usuário clica em linha da tabela "Bot Download Vivo" para ver detalhes | - |
| 23 | - | Frontend executa GET `/api/rpa/bots/{botId}/execucoes` com query params: `?pageNumber=1&pageSize=20&orderBy=DataInicio DESC` |
| 24 | - | Backend executa query paginada: `SELECT * FROM RPA_BotExecution WHERE ClienteId = @clienteId AND BotId = @botId ORDER BY DataInicio DESC OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY` |
| 25 | - | Retorna HTTP 200 com array de execuções: `{ data: [{ id, status, dataInicio, dataFim, duracaoSegundos, mensagemErro }], totalCount: 42, pageNumber: 1, pageSize: 20 }` |
| 26 | Frontend exibe modal "Histórico de Execuções - Bot Download Vivo" com tabela paginada: 20 linhas com ícones de status (✅ Sucesso, ❌ Erro, ⏳ Executando) | - |
| 27 | Usuário clica em execução com status "Erro" | - |
| 28 | - | Frontend executa GET `/api/rpa/execucoes/{executionId}/logs` |
| 29 | - | Backend query: `SELECT * FROM RPA_BotExecutionLog WHERE ExecutionId = @executionId ORDER BY DataCriacao ASC` → retorna 5 logs (Info, Info, Warning, Error, Error) |
| 30 | - | Retorna HTTP 200 com array de logs: `{ logs: [{ timestamp, nivel, mensagem }], totalLogs: 5 }` |
| 31 | Frontend exibe timeline de logs com cores por nível: Info (azul), Warning (amarelo), Error (vermelho) | - |

### 5. Fluxos Alternativos

**FA01: Alerta de Taxa de Erro Elevada (>10% em 24h)**
- No passo 9, backend calcula taxa de erro: 12 de 100 execuções falharam = 12% erro
- Backend detecta threshold excedido: if (taxaErro > 0.10) → true
- Backend cria AlertaRPA: Id, ClienteId, TipoAlerta = "TaxaErroElevada", Severidade = "Alta", Descricao = "Taxa de erro de 12% detectada nas últimas 24h (threshold: 10%)", DataCriacao
- Backend persiste: `INSERT INTO Alerta (Id, ClienteId, TipoAlerta, Severidade, Descricao, DataCriacao)`
- Backend envia notificação: Email SMTP para admin com assunto "ALERTA: Taxa de erro elevada em bots RPA"
- Backend invoca SignalR: `_hubContext.Clients.Group(clienteId).SendAsync("AlertaCriado", { alerta })`
- Frontend recebe evento, exibe banner vermelho no topo do dashboard: "⚠️ Taxa de erro elevada detectada. Verifique execuções recentes"
- Frontend adiciona card "Alertas Ativos" no dashboard com lista de alertas (clicável para ver detalhes)
- Fluxo retorna ao passo 21

**FA02: Filtrar Dashboard por Período Personalizado**
- No passo 1, usuário acessa dashboard
- Frontend exibe filtro de período no topo: [Últimos 7 dias ▼] [Aplicar]
- Usuário clica no dropdown, seleciona "Últimos 30 dias"
- Frontend reexecuta GET `/api/rpa/metricas?periodoEmDias=30`
- Backend ajusta queries: `DATEADD(DAY, -30, GETUTCDATE())` ao invés de `-7`
- Backend retorna métricas recalculadas para período de 30 dias
- Frontend atualiza todos os KPIs e gráficos com novos dados
- Fluxo retorna ao passo 14

**FA03: Exportar Relatório de Métricas (CSV)**
- No passo 14, usuário clica em botão "Exportar CSV" no dashboard
- Frontend executa GET `/api/rpa/metricas/exportar?formato=csv&periodoEmDias=7`
- Backend executa mesmas queries do passo 6-11
- Backend formata resultado como CSV: cabeçalho "Bot,Execuções,Sucessos,Falhas,TaxaSucesso,TempoMedio" + linhas de dados
- Backend retorna HTTP 200 com Content-Type: text/csv, Content-Disposition: attachment; filename="rpa_metricas_2025-12-29.csv"
- Frontend dispara download automático do arquivo CSV
- Fluxo termina

### 6. Exceções

**EX01: Usuário Sem Permissão rpa:execution:read**
- No passo 2, sistema valida RBAC
- Usuário não possui `rpa:execution:read`
- Sistema retorna HTTP 403: `{ error: "PermissionDenied", message: "Você não tem permissão para visualizar execuções" }`
- Fluxo termina

**EX02: SignalR Desconectado (Perda de Conexão)**
- No passo 19, frontend escuta evento SignalR
- Conexão WebSocket é interrompida (rede instável)
- Frontend detecta evento `onclose()` do SignalR connection
- Frontend exibe banner de aviso: "⚠️ Conexão com servidor perdida. Atualizações em tempo real desabilitadas"
- Frontend ativa polling manual: setInterval(() => { GET `/api/rpa/metricas` }, 30000) → atualiza a cada 30 segundos
- Quando conexão é restabelecida: Frontend reexecuta `_hubConnection.start()`, reabilita atualizações em tempo real
- Fluxo retorna ao passo 4

**EX03: Query de Métricas Muito Lenta (Timeout de Banco)**
- No passo 6, backend executa queries agregadas
- Query complexa em tabela RPA_BotExecution com milhões de linhas demora > 30 segundos
- Entity Framework lança TimeoutException (CommandTimeout excedido)
- Backend captura exceção, registra log: `Nivel = "Error", Mensagem = "Timeout ao calcular métricas de RPA"`
- Backend retorna HTTP 503 Service Unavailable: `{ error: "MetricsTimeout", message: "Cálculo de métricas demorou muito, tente novamente" }`
- Frontend exibe erro: "Erro ao carregar métricas. Tente novamente em alguns instantes"
- Fluxo termina (recomenda-se otimizar queries com índices ou cache)

### 7. Pós-condições

- Dashboard renderizado com métricas atualizadas (KPIs, gráficos, tabelas)
- Conexão SignalR estabelecida para atualizações em tempo real
- Alertas criados e notificados para admin em caso de thresholds excedidos
- Logs estruturados consultáveis por execução
- Relatórios exportáveis em CSV para análise offline

### 8. Regras de Negócio Aplicáveis

- **RN-RPA-113-04**: Retenção de Logs de Execução (180 dias, query filtra DataExclusao IS NULL)
- **RN-RPA-113-08**: Multi-Tenancy em Execução de Bots (todas queries filtram por ClienteId via query filter)
- **RN-RPA-113-10**: Auditoria Completa de Execuções e Ações de Bots (logs estruturados registrados em RPA_BotExecutionLog)

---

## UC05: Configurar Alertas Automáticos para Falhas de Bot com Notificação Teams/Email

### 1. Descrição

Este caso de uso permite que administradores RPA configurem regras de alerta automático para eventos críticos de bots (falha repetida, timeout, taxa de erro elevada, credencial expirada). Quando a condição é detectada, o sistema envia notificação via Microsoft Teams webhook ou Email SMTP, registra o alerta no banco de dados e exibe no dashboard. Alertas podem ser resolvidos manualmente ou automaticamente após correção.

### 2. Atores

- **Usuário autenticado** com permissão `rpa:bot:update`, `rpa:alerts:manage`
- **Sistema** (backend .NET 10, Hangfire, SMTP client, Microsoft Teams webhook, EF Core)

### 3. Pré-condições

- Usuário autenticado com perfil Admin ou RPA Specialist
- Permissões: `rpa:bot:update`, `rpa:alerts:manage`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `RPA_AUTOMATION_ENGINE` habilitada
- Microsoft Teams webhook configurado OU SMTP server configurado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Automação → Configurações de Alertas | - |
| 2 | - | Valida permissões RBAC: `rpa:alerts:manage` → Se negado: HTTP 403 |
| 3 | - | Frontend executa GET `/api/rpa/alertas/configuracoes` para buscar regras existentes |
| 4 | - | Backend query: `SELECT * FROM RPA_AlertaConfiguracao WHERE ClienteId = @clienteId` → retorna array de configurações |
| 5 | - | Retorna HTTP 200 com array: `{ data: [{ id, nome, tipo, condicao, destinatarios, habilitado }] }` |
| 6 | Frontend exibe lista de regras de alerta: [Falha Repetida - 3x em 24h - Teams] [Taxa Erro >10% - Email] | - |
| 7 | Clica em "Criar Nova Regra de Alerta" | - |
| 8 | - | Frontend exibe formulário: Nome da Regra, Tipo de Evento (dropdown: FalhaRepetida, Timeout, TaxaErroElevada, CredencialExpirada), Condição (ex: "Mesmo bot falhou X vezes em Y horas"), Destinatários (Teams webhook URL OU emails separados por vírgula), Habilitado (checkbox) |
| 9 | Preenche formulário: Nome = "Alerta Timeout Crítico", Tipo = "Timeout", Condição = "Bot excedeu timeout 2x em 6 horas", Destinatários = "https://outlook.office.com/webhook/abc123", Habilitado = true | - |
| 10 | Clica em "Salvar" | - |
| 11 | - | Frontend executa POST `/api/rpa/alertas/configuracoes` com body JSON: `{ nome, tipo, condicao, destinatarios, habilitado }` |
| 12 | - | Backend valida campos obrigatórios: Nome, Tipo, Destinatários → Se inválido: HTTP 400 |
| 13 | - | Backend valida formato de destinatários: Se Teams webhook, valida URL inicia com "https://outlook.office.com/webhook/", se Email, valida formato de email regex |
| 14 | - | Backend cria RpaAlertaConfiguracao: Id, ClienteId, Nome, Tipo, CondicaoJson = JsonConvert.SerializeObject(condicao), Destinatarios, Habilitado = true, DataCriacao, CriadoPor |
| 15 | - | Backend persiste: `INSERT INTO RPA_AlertaConfiguracao (Id, ClienteId, Nome, Tipo, CondicaoJson, Destinatarios, Habilitado, DataCriacao, CriadoPor)` |
| 16 | - | Backend registra auditoria: AuditLog { EntityType = "RPA_AlertaConfiguracao", ActionType = "ALERT_CONFIG_CREATE", NewValues = JSON da configuração } |
| 17 | - | Retorna HTTP 201 Created com AlertaConfiguracaoResponse: `{ id, nome, tipo, condicao, destinatarios, habilitado }` |
| 18 | Frontend exibe mensagem de sucesso: "Regra de alerta criada com sucesso" e adiciona à lista | - |
| 19 | - | **Detecção Automática de Condição**: Worker backend processa execução de bot (UC02), bot "Bot Download Vivo" excede timeout pela 2ª vez em 6 horas |
| 20 | - | Worker executa query: `SELECT COUNT(*) FROM RPA_BotExecution WHERE BotId = @botId AND CodigoErro = 'Timeout' AND DataInicio >= DATEADD(HOUR, -6, GETUTCDATE())` → count = 2 |
| 21 | - | Worker detecta condição de alerta configurada: "Bot excedeu timeout 2x em 6 horas" → match |
| 22 | - | Worker cria RpaAlerta: Id, ClienteId, AlertaConfiguracaoId, BotId, TipoAlerta = "Timeout", Severidade = "Crítico", Descricao = "Bot 'Bot Download Vivo' excedeu timeout 2 vezes nas últimas 6 horas", Status = "Pendente", DataCriacao |
| 23 | - | Worker persiste: `INSERT INTO RPA_Alerta (Id, ClienteId, AlertaConfiguracaoId, BotId, TipoAlerta, Severidade, Descricao, Status, DataCriacao)` |
| 24 | - | **Envio de Notificação Teams**: Worker invoca TeamsWebhookService.SendNotificationAsync(webhookUrl, mensagem) |
| 25 | - | TeamsWebhookService monta payload JSON Teams: `{ "@type": "MessageCard", "title": "⚠️ Alerta RPA: Timeout Crítico", "text": "Bot 'Bot Download Vivo' excedeu timeout 2 vezes nas últimas 6 horas.", "potentialAction": [{ "@type": "OpenUri", "name": "Ver Detalhes", "targets": [{ "uri": "https://icontrolit.com.br/bots/{botId}" }] }] }` |
| 26 | - | TeamsWebhookService executa POST para webhook URL com payload JSON |
| 27 | - | Microsoft Teams recebe payload, exibe card adaptativo no canal configurado com título "⚠️ Alerta RPA: Timeout Crítico" e botão "Ver Detalhes" |
| 28 | - | Worker registra log: `Nivel = "Info", Mensagem = "Notificação Teams enviada para alerta ID {alertaId}"` |
| 29 | - | Worker invoca SignalR: `_hubContext.Clients.Group(clienteId).SendAsync("AlertaCriado", { alerta })` |
| 30 | Frontend recebe evento SignalR, exibe notificação toast vermelha: "⚠️ Alerta Crítico: Bot Download Vivo excedeu timeout 2x" | - |
| 31 | Frontend atualiza dashboard: adiciona card "Alertas Ativos" (se não existir), incrementa contador (1 alerta pendente) | - |
| 32 | Admin acessa Teams, clica em "Ver Detalhes" no card, é redirecionado para dashboard de bots em https://icontrolit.com.br/bots/{botId} | - |

### 5. Fluxos Alternativos

**FA01: Notificação via Email SMTP ao Invés de Teams**
- No passo 9, usuário preenche Destinatários = "admin@icontrolit.com.br, ops@icontrolit.com.br" (emails separados por vírgula)
- No passo 13, backend detecta formato de email (não URL Teams webhook)
- No passo 24, worker invoca EmailService.SendEmailAsync(destinatarios, assunto, corpo) ao invés de TeamsWebhookService
- EmailService monta email HTML: Assunto = "⚠️ Alerta RPA: Timeout Crítico", Corpo = HTML formatado com detalhes do bot, link para dashboard, data/hora
- EmailService executa SMTP client: SmtpClient.SendMailAsync() com servidor SMTP configurado (ex: smtp.gmail.com:587)
- Email é enviado para admin@icontrolit.com.br e ops@icontrolit.com.br
- Fluxo retorna ao passo 28

**FA02: Alerta de Credencial Expirada (Proativo)**
- No passo 19, Worker detecta que bot "Bot Download Claro" falhou com erro "AuthFailed" 3 vezes consecutivas
- Worker identifica padrão: CodigoErro = "AuthFailed" repetido → provável credencial expirada
- Worker verifica regra de alerta configurada para tipo "CredencialExpirada"
- Worker cria RpaAlerta: TipoAlerta = "CredencialExpirada", Severidade = "Alta", Descricao = "Credencial de bot 'Bot Download Claro' pode estar expirada (3 falhas consecutivas de autenticação)"
- Worker envia notificação Teams/Email com mensagem específica: "⚠️ Verifique credenciais do bot 'Bot Download Claro' e renove se necessário"
- Admin recebe alerta, acessa dashboard, navega para edição do bot, atualiza credenciais
- Fluxo retorna ao passo 28

**FA03: Resolver Alerta Manualmente**
- No passo 31, admin visualiza alerta no dashboard
- Admin clica em alerta para ver detalhes
- Frontend exibe modal com informações: Bot afetado, tipo de alerta, severidade, descrição, data/hora
- Admin clica em botão "Resolver Alerta"
- Frontend executa PUT `/api/rpa/alertas/{alertaId}/resolver` com body: `{ motivo: "Credenciais renovadas, timeout ajustado para 1200s" }`
- Backend atualiza RpaAlerta: Status = "Resolvido", DataResolucao = DateTime.UtcNow, ResolvidoPor = currentUserId, MotivoResolucao = motivo
- Backend registra auditoria: ActionType = "ALERT_RESOLVED"
- Backend invoca SignalR: `_hubContext.Clients.Group(clienteId).SendAsync("AlertaResolvido", { alertaId })`
- Frontend remove alerta da lista de pendentes, decrementa contador
- Fluxo termina

**FA04: Alerta com Auto-Resolução (Condição Não Mais Detectada)**
- No passo 20, worker executa query para verificar condição
- Worker detecta que condição "2 timeouts em 6h" não é mais verdadeira (última execução foi sucesso, então apenas 1 timeout nas últimas 6h)
- Worker busca alerta pendente relacionado: `SELECT * FROM RPA_Alerta WHERE BotId = @botId AND TipoAlerta = 'Timeout' AND Status = 'Pendente'`
- Worker atualiza alerta: Status = "AutoResolvido", DataResolucao = DateTime.UtcNow, MotivoResolucao = "Condição não mais detectada (última execução bem-sucedida)"
- Worker envia notificação Teams/Email: "✅ Alerta auto-resolvido: Bot 'Bot Download Vivo' voltou ao normal"
- Fluxo retorna ao passo 29

### 6. Exceções

**EX01: Webhook Teams Inválido ou Indisponível**
- No passo 26, TeamsWebhookService executa POST para webhook URL
- Webhook retorna HTTP 404 Not Found (URL inválida ou webhook deletado)
- TeamsWebhookService captura HttpRequestException
- Worker registra log: `Nivel = "Error", Mensagem = "Falha ao enviar notificação Teams: webhook inválido ou indisponível"`
- Worker atualiza RpaAlerta: Status = "FalhaNotificacao", ErroNotificacao = "Webhook Teams retornou 404"
- Worker NÃO bloqueia criação do alerta (alerta é salvo no BD, mas notificação falha)
- Admin é notificado por canal alternativo (email fallback ou log de erro no dashboard)
- Fluxo continua no passo 29 (SignalR ainda funciona)

**EX02: SMTP Server Indisponível**
- No passo FA01, EmailService.SendEmailAsync() tenta conectar a SMTP server
- SmtpClient lança SmtpException: "Unable to connect to remote server"
- EmailService captura exceção, registra log crítico: "ERRO: SMTP server indisponível"
- Worker atualiza RpaAlerta: Status = "FalhaNotificacao", ErroNotificacao = "SMTP server indisponível"
- Worker tenta fallback para Teams webhook (se configurado)
- Se fallback também falha: alerta é salvo no BD, mas admin NÃO recebe notificação externa (apenas SignalR no dashboard)
- Fluxo continua no passo 29

**EX03: Condição de Alerta Mal Configurada (Query Inválida)**
- No passo 20, worker tenta executar query customizada baseada em CondicaoJson
- Query contém erro de sintaxe SQL (injetada pelo admin na configuração)
- Entity Framework lança SqlException: "Invalid column name 'BotIdInvalido'"
- Worker captura exceção, registra log: "ERRO: Condição de alerta ID {alertaConfiguracaoId} contém query inválida"
- Worker desabilita automaticamente a configuração de alerta: `UPDATE RPA_AlertaConfiguracao SET Habilitado = 0 WHERE Id = @alertaConfiguracaoId`
- Worker envia notificação crítica para admin: "⚠️ Regra de alerta '{nome}' desabilitada devido a erro de configuração"
- Fluxo termina sem criar alerta

### 7. Pós-condições

- Regra de alerta criada e persistida em RPA_AlertaConfiguracao com Status = Habilitado
- Alertas criados automaticamente quando condição é detectada
- Notificações enviadas via Teams webhook ou Email SMTP
- Alertas registrados em RPA_Alerta com Status: Pendente, Resolvido, AutoResolvido, FalhaNotificacao
- Dashboard atualizado em tempo real via SignalR com alertas ativos
- Auditoria completa registrada para criação, resolução e falha de alertas

### 8. Regras de Negócio Aplicáveis

- **RN-RPA-113-02**: Timeout de Execução do Bot (alerta disparado se timeout detectado)
- **RN-RPA-113-03**: Retry Automático com Backoff Exponencial (alerta disparado se retry falha 2x)
- **RN-RPA-113-08**: Multi-Tenancy em Execução de Bots (alertas filtrados por ClienteId)
- **RN-RPA-113-10**: Auditoria Completa de Execuções e Ações de Bots (registro de criação, resolução de alertas)

---

## CHANGELOG

| Versão | Data       | Descrição                                                                 | Autor       |
|--------|------------|---------------------------------------------------------------------------|-------------|
| 1.0    | 2025-12-29 | Versão inicial com 5 casos de uso detalhados (UC01-UC05) com 22-32 passos cada | Claude Code |

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code
**Revisão**: Pendente de Aprovação

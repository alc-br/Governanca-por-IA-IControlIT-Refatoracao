# UC-RF095 - Casos de Uso - Auditoria de Acesso e Segurança

**Versão**: 1.0 | **Data**: 2025-12-29
**RF Relacionado**: RF-095 | **EPIC**: EPIC010-AUD-Auditoria-Avancada
**Fase**: Fase 6 - Ativos, Auditoria e Integrações

---

## UC01: Registrar Tentativa de Login com Geolocalização e Detecção de Força Bruta

### 1. Descrição

Este caso de uso permite ao sistema registrar automaticamente toda tentativa de login (sucesso ou falha) com dados completos de contexto (IP, dispositivo, navegador, geolocalização) e validar em tempo real se há padrão de força bruta para bloqueio automático.

### 2. Atores

- Sistema de Autenticação
- Usuário (tentando fazer login)
- Serviço de Geolocalização (IP2Location ou Azure Maps)
- Serviço de Detecção de Dispositivo (UAParser)

### 3. Pré-condições

- Sistema de autenticação ativo
- Serviço de geolocalização configurado (Azure Maps ou IP2Location API)
- Tabela LogAcesso criada no banco de dados
- Política de segurança definida (RN-SEC-095-02: 5 falhas = alerta, 10 falhas = bloqueio)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário tenta fazer login com email e senha | - |
| 2 | - | Captura endereço IP do cliente: `HttpContext.Connection.RemoteIpAddress` |
| 3 | - | Verifica se IP está na tabela IpBloqueado: `IpBloqueadoRepository.ExistsByIpAsync(ip, DateTime.UtcNow)` |
| 4 | - | Se bloqueado → Retorna HTTP 403 com mensagem: "IP bloqueado por múltiplas tentativas falhadas. Expira em: {DataHoraFim}" |
| 5 | - | Se não bloqueado → Consulta serviço de geolocalização: `GeolocationService.GetLocationAsync(ip)` retorna Pais, Estado, Cidade |
| 6 | - | Detecta dispositivo e navegador via User-Agent: `UAParser.Parse(userAgent)` retorna TipoDispositivo (Desktop/Mobile/Tablet), IdentificadorDispositivo, TipoNavegador, VersaoNavegador |
| 7 | - | Valida credenciais: `AuthService.ValidateCredentialsAsync(email, senha)` |
| 8 | - | Se credenciais VÁLIDAS → Sucesso = true, MotivoDaFalha = null |
| 9 | - | Se credenciais INVÁLIDAS → Sucesso = false, MotivoDaFalha = "Senha incorreta" (ou "Usuário não encontrado") |
| 10 | - | Cria registro LogAcesso com: Email, DataHoraUTC (DateTime.UtcNow), EnderecoIP, TipoDispositivo, IdentificadorDispositivo, TipoNavegador, VersaoNavegador, Pais, Estado, Cidade, Sucesso, MotivoDaFalha, ClienteId (null se falha, preenchido se sucesso) |
| 11 | - | Persiste no banco: `LogAcessoRepository.AddAsync(logAcesso)` |
| 12 | - | Se Sucesso = false → Executa BruteForceDetectionService.CheckBruteForceAsync(ip) |
| 13 | - | BruteForceDetectionService conta falhas recentes (últimos 15 minutos): `SELECT COUNT(*) FROM LogAcesso WHERE EnderecoIP = @ip AND Sucesso = false AND DataHoraUTC > @dataLimite` |
| 14 | - | Se contagem = 5 → Dispara alerta para SOC: `SendSecurityAlertAsync("ForcaBruta", ip, 5)` com score 7 |
| 15 | - | Se contagem >= 10 → Cria registro IpBloqueado: `BlockIpAsync(ip, 60)` com DataHoraFim = UtcNow + 60 minutos, Motivo = "Bloqueio automático por força bruta" |
| 16 | - | Se contagem >= 10 → Dispara alerta crítico para SOC: `SendSecurityAlertAsync("ForcaBruta", ip, contagem)` com score 9 |
| 17 | - | Se Sucesso = true → Envia evento para SIEM (Azure Sentinel): `SiemService.SendEventAsync("LOGIN_SUCCESS", logAcesso)` |
| 18 | - | Se Sucesso = false → Envia evento para SIEM: `SiemService.SendEventAsync("LOGIN_FAILURE", logAcesso)` |
| 19 | - | Se Sucesso = true → Retorna HTTP 200 com token JWT |
| 20 | - | Se Sucesso = false → Retorna HTTP 401 com mensagem de erro traduzida (i18n: audit.security.messages.error.invalidCredentials) |

### 5. Fluxos Alternativos

**FA01 - IP já bloqueado ao tentar login:**
- Passo 3: Se IP está bloqueado → Retorna HTTP 403 sem validar credenciais
- Registra tentativa: LogAcesso com Sucesso = false, MotivoDaFalha = "IP bloqueado"
- NÃO incrementa contador de força bruta

**FA02 - Serviço de geolocalização indisponível:**
- Passo 5: Se GeolocationService falha (timeout, erro de API) → Preenche Pais, Estado, Cidade com "N/A"
- Registra warning no log de aplicação: `Logger.LogWarning("Geolocation service unavailable for IP {ip}")`
- Continua fluxo normalmente sem bloquear login

**FA03 - MFA obrigatório para o perfil:**
- Passo 8: Se credenciais válidas E PoliticaSeguranca.MFAObrigatorios.Contains(usuario.Perfil) E usuario.MfaHabilitado = false → Retorna HTTP 403 com mensagem: "MFA é obrigatório para seu perfil. Habilite em configurações."
- Se MFA habilitado → Dispara envio de código: `MfaService.SendCodeAsync(usuario.Email)`
- Aguarda validação em endpoint separado: POST /api/auth/verify-mfa

### 6. Exceções

**EX01 - Falha ao persistir log de acesso:**
- Passo 11: Se AddAsync falha (banco indisponível, constraint violada) → Captura exceção
- Tenta enviar log diretamente para Azure Blob Storage como fallback: `BlobService.UploadLogAsync("logs-acesso-fallback", logAcesso)`
- Retorna HTTP 500 apenas se fallback também falhar

**EX02 - User-Agent malformado ou ausente:**
- Passo 6: Se User-Agent é nulo ou UAParser lança exceção → Preenche TipoDispositivo = "Unknown", TipoNavegador = "Unknown", VersaoNavegador = "N/A"
- Continua fluxo normalmente

**EX03 - Email inválido ou vazio:**
- Passo 1: Se email não passa validação de formato (regex) → Retorna HTTP 400 com mensagem: "Email inválido"
- NÃO registra em LogAcesso (evita poluição de logs com tentativas inválidas)

### 7. Pós-condições

- Registro LogAcesso criado no banco de dados (hot storage por 90 dias)
- Se força bruta detectada: Alerta enviado para SOC via SignalR e email
- Se bloqueio: Registro IpBloqueado criado com expiração em 60 minutos
- Evento enviado para Azure Sentinel (SIEM) para correlação
- Auditoria completa disponível para investigação forense

### 8. Regras de Negócio Aplicáveis

- RN-SEC-095-01: Registro Obrigatório de Tentativa de Login
- RN-SEC-095-02: Detecção de Força Bruta (Múltiplas Falhas de Login)
- RN-SEC-095-08: Integração com Política de Segurança
- RN-SEC-095-10: Alertas Automáticos em Tempo Real

---

## UC02: Rastrear Ações de Usuário com Registro Before/After e Envio para SIEM

### 1. Descrição

Este caso de uso permite ao sistema auditar automaticamente todas as operações CRUD (Create, Read, Update, Delete) executadas por usuários, registrando dados antes/depois em formato JSON e enviando eventos críticos para SIEM.

### 2. Atores

- Usuário autenticado
- Sistema (middleware de auditoria)
- Serviço SIEM (Azure Sentinel ou Splunk)

### 3. Pré-condições

- Usuário autenticado (token JWT válido)
- Middleware de auditoria configurado: `app.UseMiddleware<CrudAuditMiddleware>()`
- Tabela LogOperacao criada no banco de dados
- ClienteId extraído do token JWT (multi-tenancy ativo)
- Permissão RBAC validada (usuário tem acesso à operação)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário executa operação (ex: PUT /api/contratos/123 para atualizar contrato) | - |
| 2 | - | Middleware intercepta requisição ANTES de chegar ao controller |
| 3 | - | Extrai contexto: UsuarioId, Email, ClienteId do token JWT (`CurrentUserService`) |
| 4 | - | Identifica tipo de operação: POST = CREATE, GET = READ, PUT/PATCH = UPDATE, DELETE = DELETE |
| 5 | - | Extrai entidade da rota: "/api/contratos/123" → Entidade = "Contrato", IdEntidade = "123" |
| 6 | - | Se operação = UPDATE ou DELETE → Recupera estado ANTES da operação: `Entity beforeState = await Repository.FindAsync(idEntidade)` serializado como JSON: `JsonConvert.SerializeObject(beforeState)` |
| 7 | - | Permite execução do controller (operação real) |
| 8 | - | Captura resultado: Sucesso = (HTTP 2xx), Erro = (HTTP 4xx/5xx) |
| 9 | - | Se operação = CREATE ou UPDATE → Recupera estado DEPOIS da operação: `Entity afterState = await Repository.FindAsync(idEntidade)` serializado como JSON |
| 10 | - | Cria registro LogOperacao com: UsuarioId, Email, DataHoraUTC, Entidade, Acao (CREATE/READ/UPDATE/DELETE), DadosAntes (JSON ou null), DadosDepois (JSON ou null), Sucesso (bool), EnderecoIP (`HttpContext.Connection.RemoteIpAddress`), ClienteId, IdEntidade, Motivo (null para operações normais) |
| 11 | - | Persiste no banco: `LogOperacaoRepository.AddAsync(logOperacao)` |
| 12 | - | Verifica se operação é CRÍTICA: `IsOperacaoCritica(acao)` retorna true para DELETE, APPROVE, UPDATE_PERMISSION |
| 13 | - | Se operação CRÍTICA → Envia para SIEM: `SiemService.SendEventAsync("CRITICAL_OPERATION", logOperacao)` |
| 14 | - | Se operação CRÍTICA → Gera alerta de segurança: `AlertaSegurancaService.GerarAlertaAsync("OperacaoCritica", contexto, scoreRisco: 6)` |
| 15 | - | Se Acao = DELETE e quantidade > 10 (deleção em lote) → Escala severidade do alerta para score 8 |
| 16 | - | Retorna resposta original do controller ao cliente |

### 5. Fluxos Alternativos

**FA01 - Operação de READ (consulta) em dado sensível:**
- Passo 4: Se operação = READ E entidade está na lista de dados sensíveis (ex: "FolhaPagamento", "DadosPessoais") → Marca como operação crítica
- Passo 10: Adiciona ao LogOperacao campo adicional: `TipoDado = "Sensivel"`
- Passo 13: Envia para SIEM mesmo sendo READ

**FA02 - Operação com aprovação (ex: aprovar despesa):**
- Passo 1: Endpoint específico: POST /api/despesas/123/approve com body { motivo: "Aprovado por orçamento" }
- Passo 10: Preenche campo Motivo com justificativa do usuário
- Passo 12: Sempre considerada operação CRÍTICA (Acao = "APPROVE")
- Adiciona campo extra: AprovadorId, DecisaoAprovacao (Aprovado/Rejeitado)

**FA03 - Exportação de dados em massa:**
- Passo 1: Endpoint: GET /api/contratos/export?format=csv
- Passo 4: Detecta operação especial: Acao = "EXPORT"
- Passo 10: DadosDepois contém metadados: { formato: "CSV", quantidadeRegistros: 500, tamanhoBytes: 125000 }
- Passo 13: Sempre envia para SIEM (compliance LGPD)

### 6. Exceções

**EX01 - Falha ao recuperar estado ANTES (registro deletado entre leitura e operação):**
- Passo 6: Se FindAsync retorna null (race condition) → DadosAntes = "{ error: 'Estado anterior não disponível' }"
- Continua fluxo normalmente, registra warning no log de aplicação

**EX02 - Serialização JSON falha (objeto circular ou muito grande):**
- Passo 6/9: Se SerializeObject lança exceção → Captura e registra erro simplificado: DadosAntes = "{ error: 'Serialization failed', reason: '{ex.Message}' }"
- Trunca JSON se > 10KB: `json.Substring(0, 10240) + "... [TRUNCATED]"`

**EX03 - SIEM indisponível:**
- Passo 13: Se SendEventAsync falha (timeout, connection refused) → Captura exceção
- Tenta enviar novamente com Polly retry policy (3 tentativas, backoff exponencial)
- Se ainda falha → Envia para fila de retry (Azure Service Bus): `QueueService.EnqueueAsync("siem-retry", logOperacao)`
- NÃO bloqueia operação do usuário

### 7. Pós-condições

- Registro LogOperacao criado no banco de dados
- Se operação crítica: Evento enviado para SIEM (Azure Sentinel)
- Se operação crítica: Alerta gerado na tabela AlertaSeguranca
- Trilha de auditoria completa disponível para investigação forense
- Dados antes/depois preservados em JSON para análise de mudanças

### 8. Regras de Negócio Aplicáveis

- RN-SEC-095-03: Rastreamento de Ações de Usuário (CRUD + Operações Críticas)
- RN-SEC-095-10: Alertas Automáticos em Tempo Real
- RN-SEC-095-11: Retenção de Logs (10 Anos Conforme Compliance)
- RN-004-AUD-01: Auditoria de todas as operações (referência RF-004)

---

## UC03: Detectar Comportamentos Anômalos com UEBA e Machine Learning

### 1. Descrição

Este caso de uso permite ao sistema analisar automaticamente o comportamento de usuários (UEBA - User and Entity Behavior Analytics) utilizando regras estatísticas (Z-Score, padrões históricos) e Machine Learning (Azure ML - Isolation Forest) para detectar anomalias e gerar alertas de segurança.

### 2. Atores

- Sistema (job Hangfire executado diariamente)
- Usuário (alvo da análise comportamental)
- Azure ML Service (modelo Isolation Forest pré-treinado)
- Security Operations Center (SOC) - recebe alertas

### 3. Pré-condições

- Job Hangfire configurado: `RecurringJob.AddOrUpdate<UebaAnalysisJob>(x => x.AnalyzeAllUsersAsync(), Cron.Daily(3))` (executa às 03:00 diariamente)
- Tabela LogOperacao com histórico mínimo de 90 dias
- Azure ML endpoint configurado: `POST https://ml.azure.com/api/anomaly-detection`
- Tabela AnomaliaDetectada criada no banco de dados
- Multi-tenancy ativo (análise por ClienteId)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job Hangfire dispara execução às 03:00 UTC: `UebaAnalysisJob.AnalyzeAllUsersAsync()` |
| 2 | - | Recupera lista de usuários ativos por tenant: `SELECT DISTINCT UsuarioId, ClienteId FROM LogOperacao WHERE DataHoraUTC > @data90DiasAtras AND Sucesso = true` |
| 3 | - | Para cada usuário: Coleta histórico de comportamento (últimos 90 dias): `LogOperacaoRepository.Where(x => x.UsuarioId == usuarioId && x.DataHoraUTC > DateTime.UtcNow.AddDays(-90)).ToListAsync()` |
| 4 | - | Se histórico < 10 registros → Pula usuário (dados insuficientes para análise) |
| 5 | - | Calcula padrão normal do usuário: MediaOperacoesPorHora (μ), DesviosPadrao (σ), HorarioPico (mode das horas 0-23), PaisFrequente (mode de Pais), DiasAtivosSemanais |
| 6 | - | Recupera comportamentos recentes (últimas 24 horas): `historico.Where(x => x.DataHoraUTC > DateTime.UtcNow.AddHours(-24))` |
| 7 | - | Para cada comportamento recente: Verifica desvio de horário: Se `comportamento.DataHoraUTC.Hour NOT IN (HorarioPico ± 2 horas)` → Anomalia detectada com score 0.3, tipo "Horário incomum", detalhes "Acesso às {hora}h (normal: {HorarioPico}h)" |
| 8 | - | Verifica desvio de geolocalização: Se `comportamento.Pais != PaisFrequente` → Anomalia detectada com score 0.3, tipo "Geolocalização suspeita", detalhes "Acesso de {Pais} (normal: {PaisFrequente})" |
| 9 | - | Calcula distância temporal entre acessos de países diferentes: Se último acesso foi de Brasil às 10:00 E atual é de China às 10:30 (30 min) → Impossível fisicamente, escala score para 0.8 |
| 10 | - | Verifica volume de operações: Conta operações na última hora: `countUltimaHora = comportamentosRecentes.Where(x => x.DataHoraUTC > DateTime.UtcNow.AddHours(-1)).Count()` |
| 11 | - | Se `countUltimaHora > MediaOperacoesPorHora * 10` → Anomalia detectada com score 0.4, tipo "Volume excessivo", detalhes "{countUltimaHora} ops (normal: {MediaOperacoesPorHora})" |
| 12 | - | Verifica acesso a entidades fora do perfil: Se usuário (perfil "Dev") acessa entidade "FolhaPagamento" E histórico NÃO contém "FolhaPagamento" → Anomalia detectada com score 0.5, tipo "Acesso atípico", detalhes "Primeira vez acessando {entidade}" |
| 13 | - | Agrega score total: `scoreTotal = SUM(scores de todas anomalias detectadas)` limitado a máximo 1.0 |
| 14 | - | Se scoreTotal >= 0.7 → Envia para Azure ML para refinamento: `AzureMLService.PredictAnomalyAsync(usuarioId, anomalias)` |
| 15 | - | Azure ML retorna scoreML (0-1.0) baseado em Isolation Forest treinado com histórico de incidentes |
| 16 | - | Se scoreML > 0.8 → Classifica como "Alto Risco", se 0.5 < scoreML <= 0.8 → "Médio Risco", se scoreML <= 0.5 → "Baixo Risco" |
| 17 | - | Cria registro AnomaliaDetectada com: UsuarioId, ClienteId, Anomalias (JSON array), ScoreConfianca (scoreML), DataDeteccao, Status (AltoRisco/MédioRisco/BaixoRisco) |
| 18 | - | Persiste no banco: `AnomaliaDetectadaRepository.AddAsync(anomalia)` |
| 19 | - | Se Status = "AltoRisco" → Dispara alerta crítico para SOC: `AlertaSegurancaService.GerarAlertaAsync("ComportamentoAnomalo", contexto, scoreRisco: 9)` |
| 20 | - | Se Status = "AltoRisco" → Envia notificação via SignalR: `Hub.Clients.Group("SOC").SendAsync("NovaAnomaliaAltoRisco", anomalia)` |
| 21 | - | Se Status = "AltoRisco" → Envia email para gerente de segurança: `EmailService.SendAsync("security@empresa.com", "Alerta: Comportamento anômalo detectado", templateAnomalia)` |
| 22 | - | Se Status = "MédioRisco" → Gera alerta moderado para revisão: score 6 |
| 23 | - | Envia todas anomalias para SIEM: `SiemService.SendEventAsync("UEBA_ANOMALY", anomalia)` |
| 24 | - | Registra execução do job: `Logger.LogInformation("UEBA analysis completed: {totalUsers} users analyzed, {totalAnomalies} anomalies detected")` |

### 5. Fluxos Alternativos

**FA01 - Múltiplos logins simultâneos de IPs diferentes:**
- Passo 7-8: Se LogAcesso mostra login simultâneo (diferença < 5 minutos) de 2+ IPs de países diferentes → Anomalia com score 0.9, tipo "Login simultâneo suspeito"
- Classifica automaticamente como "Alto Risco" sem precisar Azure ML

**FA02 - Tentativa de acesso a múltiplas entidades em curto período (data exfiltration):**
- Passo 10-11: Se comportamentosRecentes mostra READ em >50 entidades diferentes em <10 minutos → Anomalia com score 0.8, tipo "Possível exfiltração de dados"
- Gera alerta crítico imediatamente (não aguarda job diário)

**FA03 - Azure ML indisponível:**
- Passo 15: Se PredictAnomalyAsync falha (timeout, 503) → Usa apenas score baseado em regras (scoreTotal)
- Se scoreTotal >= 0.8 → Classifica como "AltoRisco" sem ML
- Registra warning: `Logger.LogWarning("Azure ML unavailable, using rule-based score")`

### 6. Exceções

**EX01 - Histórico insuficiente para usuário novo:**
- Passo 4: Se usuário tem < 10 registros nos últimos 90 dias → Pula análise UEBA
- Registra info: `Logger.LogInformation("Skipping UEBA for user {usuarioId}: insufficient history")`
- Retorna null (não cria anomalia)

**EX02 - Cálculo de padrão normal falha (todos acessos no mesmo horário):**
- Passo 5: Se cálculo de desvio padrão resulta em σ = 0 (zero variância) → Usa valores padrão conservadores: MediaOperacoesPorHora = 10, HorarioPico = 14 (meio da tarde)
- Continua análise com padrão estimado

**EX03 - Geolocalização retorna país "Unknown":**
- Passo 8: Se Pais = "N/A" ou "Unknown" → NÃO considera como anomalia de geolocalização
- Pula verificação de distância temporal

### 7. Pós-condições

- Registros AnomaliaDetectada criados para todos os usuários com score >= 0.7
- Alertas de segurança gerados para anomalias de alto risco
- SOC notificado via SignalR e email
- Eventos enviados para SIEM (Azure Sentinel) para correlação
- Dashboard de segurança atualizado com novas anomalias

### 8. Regras de Negócio Aplicáveis

- RN-SEC-095-07: Detecção de Comportamentos Anômalos (UEBA)
- RN-SEC-095-10: Alertas Automáticos em Tempo Real
- RN-SEC-095-09: Correlação de Eventos para Investigação Forense

---

## UC04: Validar Segregação de Funções e Bloquear Permissões Conflitantes

### 1. Descrição

Este caso de uso permite ao sistema validar automaticamente em tempo real que nenhum usuário possua permissões conflitantes (SOD - Segregation of Duties), bloqueando tentativas de atribuição de permissões que violem políticas de segurança (ex: Criador e Aprovador da mesma entidade).

### 2. Atores

- Administrador de Sistema (atribui permissões)
- Sistema (valida SOD)
- Usuário (alvo da atribuição de permissão)

### 3. Pré-condições

- Usuário autenticado com permissão: `audit:permission:manage`
- Tabela Permissao com permissões ativas do usuário alvo
- Dicionário de conflitos SOD configurado: `ConflitosSOD` (ex: "audit:approval:create" conflita com "audit:approval:approve")
- Multi-tenancy ativo (validação por ClienteId)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Admin acessa tela de gestão de permissões: /admin/security/permissions | - |
| 2 | Admin seleciona usuário alvo (autocomplete por email) | - |
| 3 | - | Carrega permissões atuais do usuário: `PermissaoRepository.Where(x => x.UsuarioId == usuarioId && x.Ativo).ToListAsync()` exibidas em tabela |
| 4 | Admin clica em "Adicionar Permissão" | - |
| 5 | - | Exibe modal com dropdown de permissões disponíveis (filtradas por módulo) |
| 6 | Admin seleciona permissão nova (ex: "audit:approval:approve") | - |
| 7 | Admin clica em "Salvar" | - |
| 8 | - | Frontend envia POST /api/permissions com body: `{ usuarioId: "abc123", permissao: "audit:approval:approve", clienteId: "tenant1" }` |
| 9 | - | Backend executa comando: `AtribuirPermissaoComValidacaoCommand` |
| 10 | - | Recupera permissões existentes do usuário: `permissoesExistentes = PermissaoRepository.Where(x => x.UsuarioId == usuarioId && x.Ativo && x.ClienteId == clienteId).Select(x => x.Codigo).ToListAsync()` |
| 11 | - | Consulta dicionário de conflitos: `ConflitosSOD.TryGetValue(permissaoNova, out permissoesConflitantes)` retorna lista de permissões conflitantes (ex: ["audit:approval:create"]) |
| 12 | - | Calcula interseção: `conflitosEncontrados = permissoesExistentes.Intersect(permissoesConflitantes).ToList()` |
| 13 | - | Se conflitosEncontrados.Any() → Cria lista de PermissaoConflitante com: PermissaoNova, PermissaoExistente, Motivo = "Violação de SOD detectada" |
| 14 | - | Se há conflito → Lança exceção: `InvalidOperationException("Não é permitido atribuir {permissaoNova} devido a conflito de SOD: {string.Join(", ", conflitosEncontrados)}")` |
| 15 | - | Exceção é capturada pelo controller → Retorna HTTP 400 com mensagem traduzida: i18n audit.security.messages.error.sodViolation |
| 16 | - | Frontend exibe erro em modal: "Violação de segregação de funções: usuário já possui 'audit:approval:create' que conflita com 'audit:approval:approve'" |
| 17 | - | Se NÃO há conflito → Cria registro Permissao: `new Permissao { UsuarioId = usuarioId, Codigo = permissaoNova, ClienteId = clienteId, DataAtribuicao = DateTime.UtcNow, Ativo = true }` |
| 18 | - | Persiste no banco: `PermissaoRepository.AddAsync(permissao)` |
| 19 | - | Registra em auditoria: `CrudAuditService.LogOperationAsync("Permissao", "CREATE", dadosAntes: null, dadosDepois: permissao, motivo: "Atribuição de permissão")` |
| 20 | - | Envia para SIEM: `SiemService.SendEventAsync("PERMISSION_GRANTED", permissao)` (operação crítica) |
| 21 | - | Invalida cache de permissões do usuário: `CacheService.RemoveAsync($"permissions_{usuarioId}_{clienteId}")` para forçar reload |
| 22 | - | Retorna HTTP 201 Created com permissão criada |
| 23 | - | Frontend fecha modal, recarrega tabela de permissões, exibe toast de sucesso: "Permissão atribuída com sucesso" |

### 5. Fluxos Alternativos

**FA01 - Relatório mensal de violações de SOD:**
- Job Hangfire executado mensalmente: `RecurringJob.AddOrUpdate<SodReportJob>(x => x.GenerateMonthlyReportAsync(), Cron.Monthly(1, 8))` (dia 1 às 08:00)
- Para cada tenant: Valida todas combinações de permissões de todos os usuários
- Identifica violações existentes (permissões conflitantes já atribuídas antes da governança)
- Gera relatório CSV: UsuarioId, Email, Permissao1, Permissao2, Conflito, DataDeteccao
- Envia email para gerente de segurança com anexo e ações recomendadas

**FA02 - Remoção de permissão conflitante existente:**
- Passo 14: Em vez de bloquear, sistema oferece opção ao admin: "Remover permissão existente 'audit:approval:create' e atribuir nova 'audit:approval:approve'?"
- Se admin confirma → Remove permissão antiga, atribui nova, registra ambas operações em auditoria

**FA03 - Permissão temporária com data de expiração:**
- Passo 17: Admin pode definir DataVencimento ao atribuir permissão (ex: acesso temporário por 30 dias)
- Job Hangfire diário revoga permissões expiradas: `PermissaoRepository.Where(x => x.DataVencimento < DateTime.UtcNow && x.Ativo).ForEach(p => p.Ativo = false)`

### 6. Exceções

**EX01 - Permissão nova não existe no catálogo:**
- Passo 11: Se permissaoNova não está registrada em ConflitosSOD nem em PermissoesCatalogo → Retorna HTTP 404 com mensagem: "Permissão '{permissaoNova}' não encontrada no catálogo"
- Frontend exibe erro

**EX02 - Usuário alvo não existe:**
- Passo 10: Se UsuarioRepository.FindAsync(usuarioId) retorna null → Retorna HTTP 404 com mensagem: "Usuário não encontrado"

**EX03 - Admin tenta atribuir permissão a si mesmo (auto-elevação):**
- Passo 9: Se usuarioId == AdminId (usuário logado) → Retorna HTTP 403 com mensagem: "Não é permitido atribuir permissões a si mesmo. Solicite a outro administrador."
- Regra de dual-control para operações críticas

### 7. Pós-condições

- Se validação passou: Registro Permissao criado no banco de dados
- Se validação falhou: Nenhuma permissão atribuída, erro retornado ao admin
- Operação registrada em auditoria (sucesso ou falha)
- Cache de permissões do usuário invalidado
- Evento enviado para SIEM
- RBAC atualizado em tempo real (próxima requisição do usuário já valida nova permissão)

### 8. Regras de Negócio Aplicáveis

- RN-SEC-095-04: Validação Obrigatória de Segregação de Funções (SOD)
- RN-SEC-095-03: Rastreamento de Ações de Usuário (mudança de permissão é operação crítica)
- RN-SEC-095-10: Alertas Automáticos em Tempo Real (se violação detectada)

---

## UC05: Executar Certificação Trimestral de Acessos com Revogação Automática

### 1. Descrição

Este caso de uso permite ao sistema gerar automaticamente workflow trimestral onde gerentes revisam e certificam permissões de seus subordinados, com revogação automática em 72 horas para permissões rejeitadas e escalação para gestores em caso de não-resposta.

### 2. Atores

- Sistema (job Hangfire executado trimestralmente)
- Gerente (revisa e certifica permissões)
- Subordinado (alvo da certificação)
- Gestor do Gerente (recebe escalação se não-resposta)

### 3. Pré-condições

- Job Hangfire configurado: `RecurringJob.AddOrUpdate<CertificacaoAccessoJob>(x => x.IniciarCertificacaoTrimestraAsync(), Cron.Quarterly())` (1º dia de jan/abr/jul/out às 08:00)
- Tabela Usuario com campo GerentiId (hierarquia)
- Tabela Permissao com permissões ativas
- Tabelas CertificacaoTrimestral, TarefaCertificacao, RegistroCertificacao criadas
- Multi-tenancy ativo (certificação por ClienteId)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job Hangfire dispara em 1º dia do trimestre: `IniciarCertificacaoTrimestraAsync()` |
| 2 | - | Identifica trimestre atual: `trimestre = (DateTime.Now.Month - 1) / 3 + 1` (Q1/Q2/Q3/Q4), ano = DateTime.Now.Year |
| 3 | - | Cria registro CertificacaoTrimestral: `new CertificacaoTrimestral { Trimestre = trimestre, Ano = ano, DataInicio = DateTime.UtcNow, DataLimite = DateTime.UtcNow.AddDays(30), Status = "Iniciada" }` |
| 4 | - | Recupera todos os gerentes ativos: `UsuarioRepository.Where(x => x.Perfil == "Gerente" && x.Ativo).ToListAsync()` |
| 5 | - | Para cada gerente: Recupera subordinados: `UsuarioRepository.Where(x => x.GerentiId == gerenteId && x.Ativo).ToListAsync()` |
| 6 | - | Para cada subordinado: Recupera permissões ativas: `PermissaoRepository.Where(x => x.UsuarioId == subordinadoId && x.Ativo).ToListAsync()` |
| 7 | - | Cria tarefa de certificação: `new TarefaCertificacao { CertificacaoId, GerentiId, SubordinadoId, PermissoesParaCertificar (JSON array de IDs), Status = "Pendente", DataCriacao = DateTime.UtcNow }` |
| 8 | - | Persiste tarefas no banco: `TarefaCertificacaoRepository.AddRangeAsync(tarefas)` |
| 9 | - | Envia email para cada gerente: "Certificação Trimestral Q{trimestre}/{ano} iniciada. Você tem {count} subordinados para revisar. Prazo: {DataLimite}" com link para /admin/certification/review |
| 10 | Gerente acessa tela de certificação: /admin/certification/review | - |
| 11 | - | Carrega tarefas pendentes do gerente: `TarefaCertificacaoRepository.Where(x => x.GerentiId == gerenteId && x.Status == "Pendente").Include(x => x.Subordinado).Include(x => x.Permissoes).ToListAsync()` |
| 12 | - | Exibe lista de subordinados com permissões expandidas (accordion) |
| 13 | Gerente seleciona subordinado, revisa lista de permissões | - |
| 14 | Gerente marca cada permissão: ✓ Aprovar (confirma acesso necessário) ou ✗ Rejeitar (marcar para remoção) | - |
| 15 | Gerente preenche justificativa para rejeições (campo texto obrigatório) | - |
| 16 | Gerente clica em "Certificar" | - |
| 17 | - | Frontend envia POST /api/certification/certify com body: `{ tarefaId, decisoes: [{ permissaoId, decisao: "Aprovado"/"Rejeitado", motivo }] }` |
| 18 | - | Backend executa comando: `CertificarPermissoesCommand` |
| 19 | - | Recupera tarefa: `TarefaCertificacaoRepository.FindAsync(tarefaId)` |
| 20 | - | Para cada decisão: Se decisao = "Aprovado" → Cria RegistroCertificacao: `{ PermissaoId, TarefaCertificacaoId, Decisao = "Aprovado", Motivo = motivo, DataDecisao = DateTime.UtcNow }` |
| 21 | - | Se decisao = "Rejeitado" → Cria RegistroCertificacao com Decisao = "Rejeitado" E agenda revogação: `permissao.DataRevogacaoAgendada = DateTime.UtcNow.AddHours(72)`, `permissao.MotivoDaRevogacao = $"Rejeitado em certificação trimestral Q{trimestre}/{ano}: {motivo}"` |
| 22 | - | Persiste certificações: `RegistroCertificacaoRepository.AddRangeAsync(certificacoes)` |
| 23 | - | Atualiza status da tarefa: `tarefa.Status = "Certificado"`, `tarefa.DataCertificacao = DateTime.UtcNow` |
| 24 | - | Registra em auditoria: `CrudAuditService.LogOperationAsync("TarefaCertificacao", "UPDATE", dadosAntes, dadosDepois, motivo: "Certificação trimestral concluída")` |
| 25 | - | Envia email para subordinado informando resultado: "Suas permissões foram revisadas. {aprovadas} aprovadas, {rejeitadas} serão removidas em 72h." |
| 26 | - | Retorna HTTP 200 com resumo: `{ aprovadas: count, rejeitadas: count }` |
| 27 | - | Job Hangfire diário executa revogações agendadas: `RevogarPermissoesAgendadasJob` às 02:00 |
| 28 | - | Identifica permissões para revogar: `PermissaoRepository.Where(x => x.DataRevogacaoAgendada < DateTime.UtcNow && x.Ativo).ToListAsync()` |
| 29 | - | Para cada permissão: Marca como inativa: `permissao.Ativo = false`, `permissao.DataRevogacao = DateTime.UtcNow` |
| 30 | - | Persiste mudanças: `PermissaoRepository.SaveChangesAsync()` |
| 31 | - | Registra em auditoria: `LogOperationAsync("Permissao", "DELETE", dadosAntes, dadosDepois: null, motivo: permissao.MotivoDaRevogacao)` |
| 32 | - | Invalida cache de permissões: `CacheService.RemoveAsync($"permissions_{usuarioId}_{clienteId}")` |
| 33 | - | Envia email para subordinado: "A permissão '{permissao.Codigo}' foi removida. Motivo: {MotivoDaRevogacao}" |

### 5. Fluxos Alternativos

**FA01 - Gerente não responde até data limite (30 dias):**
- Job Hangfire diário verifica tarefas não concluídas: `TarefaCertificacaoRepository.Where(x => x.Status == "Pendente" && x.Certificacao.DataLimite < DateTime.UtcNow).ToListAsync()` às 09:00
- Para cada tarefa pendente: Marca como "NãoRespondida"
- Recupera gestor do gerente: `gerenteDoGerente = UsuarioRepository.Where(x => x.Id == gerente.GerentiId).FirstOrDefaultAsync()`
- Envia email de escalação para gestor: "O gerente {gerenteEmail} não concluiu certificação trimestral. {count} subordinados pendentes. Ação requerida."
- Cria alerta de compliance: `AlertaSegurancaService.GerarAlertaAsync("CertificacaoNaoRespondida", contexto, scoreRisco: 7)`

**FA02 - Gerente solicita dados adicionais antes de decidir:**
- Passo 14: Gerente clica em botão "Solicitar Dados Adicionais" ao lado de permissão
- Sistema marca permissão como "AguardandoDados", envia notificação para subordinado
- Subordinado fornece justificativa de uso da permissão
- Gerente recebe notificação e pode revisar novamente

**FA03 - Certificação completa do trimestre:**
- Quando todas as tarefas estão Status = "Certificado" ou "NãoRespondida" → Sistema marca CertificacaoTrimestral.Status = "Concluída"
- Gera relatório consolidado: Total de usuários certificados, Total de permissões aprovadas, Total de permissões removidas, Taxa de resposta de gerentes
- Envia relatório para gerente de segurança e compliance

### 6. Exceções

**EX01 - Subordinado não possui permissões ativas:**
- Passo 6: Se PermissaoRepository retorna lista vazia → NÃO cria tarefa de certificação para esse subordinado
- Registra info: `Logger.LogInformation("User {subordinadoId} has no active permissions, skipping certification")`

**EX02 - Gerente tenta certificar tarefa de outro gerente:**
- Passo 19: Se tarefa.GerentiId != gerenteId (usuário logado) → Retorna HTTP 403 com mensagem: "Você não tem permissão para certificar esta tarefa"

**EX03 - Permissão é removida manualmente antes da revogação agendada:**
- Passo 28: Se permissao.Ativo = false (já inativa) → Pula revogação, apenas registra info
- Remove DataRevogacaoAgendada para não processar novamente

### 7. Pós-condições

- Registro CertificacaoTrimestral criado com todas as tarefas
- Tarefas de certificação criadas para todos os gerentes
- Emails enviados para gerentes (início) e subordinados (resultado)
- Permissões rejeitadas marcadas para revogação em 72 horas
- Após 72h: Permissões rejeitadas revogadas automaticamente
- Relatório trimestral de certificação disponível
- Histórico completo de certificações preservado para auditoria (10 anos)

### 8. Regras de Negócio Aplicáveis

- RN-SEC-095-06: Certificação Trimestral de Acessos
- RN-SEC-095-03: Rastreamento de Ações de Usuário (certificação é operação crítica)
- RN-SEC-095-10: Alertas Automáticos em Tempo Real (escalação por não-resposta)
- RN-SEC-095-11: Retenção de Logs (histórico de certificações por 10 anos)

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code (Anthropic)
**Próximo**: Criar MD-RF095 (Modelo de Dados) e user-stories.yaml

# UC-RF105 - Casos de Uso - Integração Operadoras Telecom

## UC01: Configurar Credenciais de Operadora com Criptografia AES-256

### 1. Descrição

Este caso de uso permite ao Administrador ou Gestor de TI configurar credenciais de integração com operadoras de telecomunicações (Vivo, Claro, TIM, Oi), incluindo API Key, Client ID, Client Secret e URL do endpoint. Credenciais são armazenadas criptografadas com AES-256 conforme RN-INT-105-01.

### 2. Atores

- **Usuário autenticado**: Administrador, Gestor de TI
- **Sistema**: IControlIT Backend, CriptografiaService

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `int:operadora:create` ou `int:operadora:update`
- Multi-tenancy ativo (ClienteId válido)
- Chave mestra de criptografia configurada em appsettings.json
- Operadora selecionada (Vivo, Claro, TIM, Oi)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Integração → Operadoras | - |
| 2 | - | Valida permissão `int:operadora:create` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | Clica em "Nova Operadora" ou edita operadora existente | - |
| 5 | - | Exibe formulário com campos: Nome da Operadora (dropdown), API Key, Client ID, Client Secret, Endpoint URL, Ativa (checkbox) |
| 6 | Preenche API Key (ex: "vivo_rest_api_key_xyz"), Client ID (ex: "vivo_client_123"), Client Secret (ex: "secret_456"), Endpoint URL (ex: "https://api.vivo.com.br/v1") | - |
| 7 | Clica em "Salvar" | - |
| 8 | - | Valida campos obrigatórios (ApiKey, EndpointUrl não vazios) |
| 9 | - | Valida formato de URL (https://) |
| 10 | - | Executa `CriptografiaService.Criptografar(ApiKey)` usando AES-256 |
| 11 | - | Executa `CriptografiaService.Criptografar(ClientId)` |
| 12 | - | Executa `CriptografiaService.Criptografar(ClientSecret)` |
| 13 | - | Executa `POST /api/operadoras` com payload criptografado |
| 14 | - | Salva registro em tabela `OperadoraCredencial` com ClienteId, OperadoraId, ApiKey (criptografado), ClientId (criptografado), ClientSecret (criptografado), EndpointUrl |
| 15 | - | Registra auditoria (código: `INT_OPR_CONFIG_CREATE`) → ClienteId, OperadoraId, EndpointUrl, UsuarioId |
| 16 | - | Retorna HTTP 201 Created com ID da configuração |
| 17 | Visualiza mensagem "Configuração de operadora criada com sucesso" | - |
| 18 | - | Redireciona para lista de operadoras |

### 5. Fluxos Alternativos

**FA01: Editar Configuração Existente**

- Passo 4: Usuário clica em "Editar" em operadora existente
- Sistema carrega credenciais existentes (descriptografa para exibição mascarada: "***xyz")
- Usuário altera apenas os campos desejados (ex: trocar EndpointUrl)
- Sistema executa `PUT /api/operadoras/{id}` com novos valores criptografados
- Registra auditoria (código: `INT_OPR_CONFIG_UPDATE`) → Campos alterados

**FA02: Marcar Operadora como Inativa**

- Passo 7: Usuário desmarca checkbox "Ativa"
- Sistema executa soft delete (marca `Ativa = false`)
- Sincronização automática (Hangfire) pula operadoras inativas
- Registra auditoria (código: `INT_OPR_CONFIG_UPDATE`) → Ativa=false

### 6. Exceções

**EX01: Usuário Sem Permissão**

- Passo 2: Sistema valida permissão `int:operadora:create` → Usuário NÃO possui
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para criar configurações de operadora"
- Registra tentativa não autorizada em auditoria

**EX02: Endpoint URL Inválido**

- Passo 9: Sistema valida formato de URL → URL não inicia com "https://"
- Sistema retorna HTTP 400 Bad Request
- Exibe mensagem: "URL do endpoint inválida. Deve iniciar com https://"
- Usuário corrige e tenta novamente

**EX03: Chave Mestra de Criptografia Ausente**

- Passo 10: Sistema tenta criptografar ApiKey → Chave mestra não configurada em appsettings.json
- Sistema lança exceção `CriptografiaException`
- Retorna HTTP 500 Internal Server Error
- Exibe mensagem: "Erro de criptografia. Contate o administrador."
- Registra erro em log estruturado

### 7. Pós-condições

- Configuração de operadora criada/atualizada no banco de dados
- Credenciais armazenadas com criptografia AES-256 (RN-INT-105-01)
- Auditoria registrada em AuditLog
- Operadora disponível para integração (se Ativa = true)
- Sincronização automática (Hangfire) utilizará novas credenciais na próxima execução (3h AM)

### 8. Regras de Negócio Aplicáveis

- **RN-INT-105-01**: Credenciais Seguras por Operadora (criptografia AES-256)
- **RN-INT-105-08**: Multi-tenancy com ClienteId e OperadoraId
- **RN-INT-105-09**: Auditoria Obrigatória de Requisições API

---

## UC02: Consultar Consumo em Tempo Real com Cache Redis

### 1. Descrição

Este caso de uso permite ao Gestor de TI ou Analista de TI consultar consumo em tempo real (voz, dados, SMS) de uma linha telefônica específica (MSISDN). Sistema verifica cache Redis (TTL 15 minutos) antes de consultar API da operadora, conforme RN-INT-105-06.

### 2. Atores

- **Usuário autenticado**: Gestor de TI, Analista de TI
- **Sistema**: IControlIT Backend, ConsumoService, OperadoraHttpClient, Redis

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `int:consumo:read`
- Multi-tenancy ativo (ClienteId válido)
- Operadora configurada com credenciais válidas
- Redis disponível (cache)
- Linha telefônica (MSISDN) válida (ex: 11987654321)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Integração → Consumo em Tempo Real | - |
| 2 | - | Valida permissão `int:consumo:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | Seleciona operadora (ex: Vivo) e insere MSISDN (ex: 11987654321) | - |
| 5 | Clica em "Consultar Consumo" | - |
| 6 | - | Valida formato MSISDN (11 dígitos numéricos) |
| 7 | - | Gera chave de cache: `consumo:{clienteId}:{operadoraId}:{msisdn}` (ex: `consumo:5:1:11987654321`) |
| 8 | - | Executa `IDistributedCache.GetStringAsync(cacheKey)` |
| 9 | - | Se cache HIT (dados existem, TTL < 15 min) → Retorna dados do cache (pula para passo 18) |
| 10 | - | Se cache MISS → Busca credenciais da operadora (descriptografa) |
| 11 | - | Executa `POST /api/operadoras/{operadoraId}/consultar-consumo` com autenticação OAuth 2.0 |
| 12 | - | Aplica Polly Retry Policy (RN-INT-105-03): 3 tentativas com backoff 1s, 2s, 4s |
| 13 | - | API da operadora retorna HTTP 200 OK com payload: `{ voz: 120.5, dados: 2048.0, sms: 15 }` (voz em minutos, dados em MB, SMS em unidades) |
| 14 | - | Armazena em Redis com TTL de 15 minutos: `cache.SetStringAsync(cacheKey, JsonSerializer.Serialize(consumo), TTL=15min)` |
| 15 | - | Registra auditoria (código: `INT_OPR_CONSUMO_CONSULT`) → ClienteId, OperadoraId, MSISDN, Voz, Dados, SMS, Tempo decorrido, Fonte (cache ou API) |
| 16 | - | Retorna HTTP 200 OK com dados de consumo |
| 17 | Visualiza consumo: Voz (120.5 min), Dados (2 GB), SMS (15 msgs) | - |
| 18 | - | Exibe badge "Dados cacheados (atualizados às 10:15)" se fonte foi cache |

### 5. Fluxos Alternativos

**FA01: Cache Hit (Dados Já Carregados)**

- Passo 9: Cache contém dados, TTL < 15 min
- Sistema pula passos 10-14 (não consulta API)
- Retorna dados do cache imediatamente (latência < 100ms)
- Exibe badge "Dados em cache (atualizar em 10 minutos)"

**FA02: Invalidar Cache Manualmente**

- Usuário clica em "Atualizar Dados" (força refresh)
- Sistema executa `InvalidarCacheAsync(clienteId, operadoraId, msisdn)` → Remove chave do Redis
- Sistema consulta API da operadora (força cache MISS)
- Armazena novo resultado em cache com TTL de 15 min

### 6. Exceções

**EX01: Timeout ao Consultar Operadora**

- Passo 13: API da operadora não responde em 30 segundos (RN-INT-105-02)
- Sistema lança `OperadoraTimeoutException`
- Polly Retry executa 3 tentativas (1s, 2s, 4s de espera)
- Se todas falham → Retorna HTTP 504 Gateway Timeout
- Exibe mensagem: "Timeout ao consultar operadora. Tente novamente."
- Registra auditoria com Status = "timeout"

**EX02: Circuit Breaker Aberto**

- Passo 12: Sistema detecta que circuit breaker está aberto (5 falhas consecutivas anteriores, RN-INT-105-10)
- Sistema NÃO tenta consultar API (retorna erro imediato)
- Retorna HTTP 503 Service Unavailable
- Exibe mensagem: "Operadora indisponível no momento. Aguarde 5 minutos."
- Registra auditoria com Status = "circuit_breaker_open"

**EX03: Redis Indisponível**

- Passo 8: Redis não está acessível (conexão recusada)
- Sistema loga aviso: "Cache indisponível, forçando consulta direta"
- Sistema pula cache e consulta API diretamente
- Não armazena resultado em cache
- Operação continua normalmente (degradação graciosa)

### 7. Pós-condições

- Consumo de voz, dados e SMS exibido ao usuário
- Dados armazenados em cache Redis por 15 minutos (se cache disponível)
- Auditoria registrada em AuditLog com tempo de resposta
- Se consultou API → Credenciais de acesso validadas
- Se circuit breaker abriu → Sistema aguarda 5 minutos antes de nova tentativa

### 8. Regras de Negócio Aplicáveis

- **RN-INT-105-02**: Timeout Diferenciado por Tipo de Operação (30s para consultas síncronas)
- **RN-INT-105-03**: Retry Automático com Backoff Exponencial (3 tentativas: 1s, 2s, 4s)
- **RN-INT-105-06**: Cache de Consumo em Tempo Real com TTL de 15 Minutos
- **RN-INT-105-08**: Multi-tenancy com ClienteId e OperadoraId
- **RN-INT-105-09**: Auditoria Obrigatória de Requisições API
- **RN-INT-105-10**: Circuit Breaker após 5 Falhas Consecutivas

---

## UC03: Consultar e Importar Faturas Eletrônicas com Armazenamento em Blob Storage

### 1. Descrição

Este caso de uso permite ao Gestor de TI ou Financeiro consultar faturas eletrônicas (XML NF-e) de uma operadora e importá-las para o sistema. Faturas são armazenadas no Azure Blob Storage com criptografia AES-256 conforme RN-INT-105-05.

### 2. Atores

- **Usuário autenticado**: Gestor de TI, Financeiro
- **Sistema**: IControlIT Backend, FaturaArmazenamentoService, OperadoraHttpClient, Azure Blob Storage

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `int:fatura:read` e `int:fatura:import`
- Multi-tenancy ativo (ClienteId válido)
- Operadora configurada com credenciais válidas
- Azure Blob Storage configurado e acessível
- Período de consulta definido (últimos 90 dias)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Integração → Faturas Eletrônicas | - |
| 2 | - | Valida permissão `int:fatura:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | Seleciona operadora (ex: Vivo) e período (ex: "Últimos 3 meses") | - |
| 5 | Clica em "Consultar Faturas" | - |
| 6 | - | Calcula data de início: `DateTime.UtcNow.AddDays(-90)` |
| 7 | - | Executa `POST /api/operadoras/{operadoraId}/consultar-faturas` com filtro de período |
| 8 | - | Aplica Polly Retry Policy (3 tentativas: 1s, 2s, 4s) |
| 9 | - | API da operadora retorna HTTP 200 OK com lista de faturas: `[ { nfeId: "123456789", dataEmissao: "2025-12-01", valor: 1500.00, xmlUrl: "..." }, ... ]` |
| 10 | - | Retorna lista de faturas paginada (20 registros por página) |
| 11 | Visualiza tabela com: NF-e, Data Emissão, Valor, Status (Importada/Pendente), Ações (Importar/Download) | - |
| 12 | Clica em "Importar" em fatura específica (ex: NF-e 123456789) | - |
| 13 | - | Valida permissão `int:fatura:import` |
| 14 | - | Baixa XML completo da fatura via `xmlUrl` |
| 15 | - | Gera caminho no Blob Storage: `/cliente/{clienteId}/operadora/{operadoraId}/ano/2025/mes/12/nf123456789.xml` |
| 16 | - | Executa `FaturaArmazenamentoService.ArmazenarFaturaAsync(clienteId, operadoraId, xml, nfeId)` |
| 17 | - | Faz upload para Azure Blob Storage com criptografia de servidor (gerenciada por Azure) |
| 18 | - | Armazena metadados: ClienteId, OperadoraId, DataCarregamento |
| 19 | - | Salva registro em tabela `FaturasOperadora` com URL do blob |
| 20 | - | Registra auditoria (código: `INT_OPR_FATURA_IMPORT`) → ClienteId, OperadoraId, NFeId, Valor, UrlArmazenamento |
| 21 | - | Retorna HTTP 201 Created |
| 22 | Visualiza mensagem "Fatura NF-e 123456789 importada com sucesso" | - |
| 23 | - | Atualiza status na tabela para "Importada" |

### 5. Fluxos Alternativos

**FA01: Fatura Já Importada**

- Passo 14: Sistema verifica se `FaturaRepo.ExisteAsync(clienteId, operadoraId, nfeId)` retorna `true`
- Sistema pula passos 15-20 (não duplica)
- Exibe mensagem: "Fatura já importada anteriormente. Download disponível."
- Oferece botão "Download XML" para recuperar do Blob Storage

**FA02: Download de Fatura Já Importada**

- Usuário clica em "Download" em fatura com status "Importada"
- Sistema executa `FaturaArmazenamentoService.ObterFaturaAsync(blobPath)`
- Sistema recupera XML do Azure Blob Storage
- Retorna arquivo XML para download com header `Content-Disposition: attachment; filename="nf123456789.xml"`

**FA03: Importar Múltiplas Faturas em Lote**

- Usuário seleciona checkboxes de múltiplas faturas (ex: 10 faturas)
- Clica em "Importar Selecionadas"
- Sistema enfileira job Hangfire para processamento assíncrono
- Retorna HTTP 202 Accepted com JobId
- Usuário recebe notificação quando importação concluir

### 6. Exceções

**EX01: Azure Blob Storage Indisponível**

- Passo 17: Sistema tenta fazer upload → Azure retorna erro 503 Service Unavailable
- Sistema lança `BlobStorageException`
- Polly Retry executa 3 tentativas
- Se todas falham → Retorna HTTP 502 Bad Gateway
- Exibe mensagem: "Erro ao armazenar fatura. Contate o suporte."
- Registra erro em log estruturado

**EX02: XML de Fatura Inválido**

- Passo 14: Sistema baixa XML → Conteúdo não é XML válido (parse falha)
- Sistema lança `XmlException`
- Retorna HTTP 400 Bad Request
- Exibe mensagem: "XML de fatura inválido. Contate a operadora."
- NÃO armazena fatura corrompida

**EX03: Período de Consulta Muito Longo**

- Passo 6: Usuário tenta consultar faturas de período > 90 dias
- Sistema valida: `(dataFim - dataInicio).TotalDays > 90`
- Retorna HTTP 400 Bad Request
- Exibe mensagem: "Período máximo de consulta: 90 dias. Reduza o intervalo."

### 7. Pós-condições

- Faturas eletrônicas consultadas e listadas
- Fatura(s) importada(s) armazenada(s) em Azure Blob Storage com criptografia AES-256
- Registro em tabela `FaturasOperadora` com URL do blob
- Auditoria registrada em AuditLog
- Fatura disponível para download e integração com RF032 (Notas Fiscais)

### 8. Regras de Negócio Aplicáveis

- **RN-INT-105-03**: Retry Automático com Backoff Exponencial
- **RN-INT-105-05**: Armazenamento de Faturas em Azure Blob Storage
- **RN-INT-105-08**: Multi-tenancy com ClienteId e OperadoraId
- **RN-INT-105-09**: Auditoria Obrigatória de Requisições API

---

## UC04: Sincronização Bidirecional Automática via Hangfire

### 1. Descrição

Este caso de uso executa sincronização automática diária (Hangfire job às 3h AM) entre IControlIT e operadoras, incluindo importação de novas faturas, atualização de consumo e reconciliação de inventário de linhas conforme RN-INT-105-07.

### 2. Atores

- **Sistema**: IControlIT Backend, SincronizacaoOperadoraJob, Hangfire, OperadoraHttpClient

### 3. Pré-condições

- Hangfire configurado e rodando
- Job `SincronizacaoOperadoraJob` registrado com Cron "0 3 * * *" (3h AM todos os dias)
- Pelo menos uma operadora configurada e ativa
- Credenciais de operadoras válidas
- Azure Blob Storage acessível
- Redis acessível (para invalidação de cache)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara job às 03:00 AM UTC |
| 2 | - | Job `SincronizacaoOperadoraJob.SincronizarOperadoras()` inicia execução |
| 3 | - | Lista todos os clientes ativos: `_clienteRepo.ListarTodosAsync()` |
| 4 | - | Para cada cliente, lista operadoras configuradas: `_operadoraRepo.ListarPorClienteAsync(clienteId)` |
| 5 | - | Filtra apenas operadoras com `Ativa = true` |
| 6 | - | **Inicia sincronização de faturas** para operadora |
| 7 | - | Consulta faturas dos últimos 90 dias: `_operadoraClient.ListarFaturasAsync(operadoraId, dataInicio)` |
| 8 | - | Para cada fatura retornada, verifica se já existe: `_faturaRepo.ExisteAsync(clienteId, operadoraId, nfeId)` |
| 9 | - | Se fatura NÃO existe → Executa `_faturaService.ImportarFaturaAsync(clienteId, operadoraId, fatura)` |
| 10 | - | Armazena XML em Blob Storage |
| 11 | - | Salva registro em tabela `FaturasOperadora` |
| 12 | - | **Inicia sincronização de consumo** |
| 13 | - | Lista todas as linhas telefônicas do cliente: `_linhaRepo.ListarPorClienteEOperadoraAsync(clienteId, operadoraId)` |
| 14 | - | Para cada linha, invalida cache: `_consumoService.InvalidarCacheAsync(clienteId, operadoraId, linha.Msisdn)` |
| 15 | - | Consulta consumo atualizado: `_operadoraClient.ConsultarConsumoAsync(operadoraId, linha.Msisdn)` |
| 16 | - | Armazena em cache Redis com TTL de 15 minutos |
| 17 | - | **Inicia sincronização de inventário** |
| 18 | - | Consulta inventário atual na operadora: `_operadoraClient.ListarInventarioAsync(operadoraId)` |
| 19 | - | Compara com inventário local: `_linhaRepo.ListarPorClienteEOperadoraAsync(clienteId, operadoraId)` |
| 20 | - | Identifica **novas linhas** (existem na operadora, não existem localmente) |
| 21 | - | Para cada nova linha → Adiciona registro em tabela `Linha` com Estado, MSISDN, IMSI, Plano |
| 22 | - | Identifica **linhas deletadas** (existem localmente, não existem na operadora) |
| 23 | - | Para cada linha deletada → Marca `Estado = "inativa"` e atualiza `DataSincronizacao` |
| 24 | - | Registra auditoria (código: `INT_OPR_SINC_EXEC`) → ClienteId, OperadoraId, Linhas sincronizadas, Faturas importadas, Duração |
| 25 | - | Loga: "[OK] Sincronização concluída para {operadora.Nome}" |
| 26 | - | Próxima operadora (retorna ao passo 6) |
| 27 | - | Após processar todos os clientes e operadoras, job finaliza |

### 5. Fluxos Alternativos

**FA01: Operadora Indisponível Durante Sincronização**

- Passo 7: API da operadora retorna 503 Service Unavailable
- Sistema captura exceção, registra erro em log
- Sistema **NÃO interrompe** job (continua com próxima operadora)
- Registra auditoria com Status = "erro" e MensagemErro
- Envia alerta para administrador: "Sincronização falhou para {operadora.Nome}"

**FA02: Sincronização Manual Fora do Horário**

- Usuário com permissão `int:sincronizacao:execute` acessa tela de sincronização
- Clica em "Sincronizar Agora" para operadora específica
- Sistema executa job imediatamente (fora do agendamento)
- Job segue mesmo fluxo principal, mas para apenas 1 operadora

### 6. Exceções

**EX01: Azure Blob Storage Indisponível**

- Passo 10: Sistema tenta armazenar fatura → Azure retorna erro 503
- Sistema loga erro: "Fatura {nfeId} não importada: Blob Storage indisponível"
- Sistema **NÃO interrompe** job (continua com próximas faturas)
- Registra falha em tabela `Volumetria_Consolidacao` com Status = "Falha"
- Próxima execução (no dia seguinte) tentará novamente

**EX02: Redis Indisponível**

- Passo 16: Sistema tenta armazenar consumo em cache → Redis não acessível
- Sistema loga aviso: "Cache indisponível durante sincronização, consumo não armazenado"
- Sistema continua normalmente (degradação graciosa)
- Próxima consulta manual forçará busca direta na API

**EX03: Job Não Completa em 30 Minutos**

- Passo 27: Job ainda executando após 30 minutos (timeout interno)
- Hangfire interrompe execução forçadamente
- Sistema loga erro: "Sincronização timeout após 30min"
- Sistema envia alerta para equipe de TI
- Administrador deve investigar causa (operadora lenta, volume alto)

### 7. Pós-condições

- Faturas dos últimos 90 dias sincronizadas e armazenadas
- Consumo de todas as linhas atualizado e cacheado
- Inventário de linhas reconciliado (novas linhas adicionadas, linhas deletadas marcadas como inativas)
- Auditoria registrada com sucesso/falha, duração, registros carregados
- Próxima execução agendada para 3h AM do dia seguinte

### 8. Regras de Negócio Aplicáveis

- **RN-INT-105-03**: Retry Automático com Backoff Exponencial
- **RN-INT-105-05**: Armazenamento de Faturas em Azure Blob Storage
- **RN-INT-105-06**: Cache de Consumo em Tempo Real com TTL de 15 Minutos
- **RN-INT-105-07**: Sincronização Bidirecional via Hangfire às 3h da Manhã
- **RN-INT-105-08**: Multi-tenancy com ClienteId e OperadoraId
- **RN-INT-105-09**: Auditoria Obrigatória de Requisições API

---

## UC05: Receber e Validar Webhook com HMAC-SHA256

### 1. Descrição

Este caso de uso recebe notificações assíncronas das operadoras via webhook (eventos: fatura_gerada, consumo_atualizado, linha_alterada, portabilidade_concluida) e valida autenticidade usando HMAC-SHA256 conforme RN-INT-105-04.

### 2. Atores

- **Operadora**: Sistema externo (Vivo, Claro, TIM, Oi)
- **Sistema**: IControlIT Backend, WebhookValidationMiddleware, WebhookController

### 3. Pré-condições

- Webhook registrado na operadora apontando para: `POST https://api.icontrolit.com/api/operadoras/webhook/{operadoraId}`
- ClientSecret da operadora armazenado e criptografado
- Middleware de validação HMAC configurado
- Endpoint público acessível pela operadora

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Operadora envia POST /api/operadoras/webhook/1 com header `X-Signature: {hmac}` e body JSON | - |
| 2 | - | Middleware `WebhookValidationMiddleware` intercepta requisição |
| 3 | - | Lê body completo: `var body = await Request.Body.ReadAsStringAsync()` |
| 4 | - | Extrai header `X-Signature` |
| 5 | - | Valida presença de header → Se ausente, lança `UnauthorizedAccessException` (pula para EX01) |
| 6 | - | Busca configuração da operadora: `_operadoraRepo.GetByIdAsync(operadoraId)` |
| 7 | - | Descriptografa `ClientSecret`: `cripto.Descriptografar(operadora.ClientSecret)` |
| 8 | - | Calcula HMAC-SHA256 esperado: `hmac.ComputeHash(Encoding.UTF8.GetBytes(body))` usando ClientSecret como chave |
| 9 | - | Converte para Base64: `expectedSignature = Convert.ToBase64String(hash)` |
| 10 | - | Compara `X-Signature` recebido com `expectedSignature` calculado |
| 11 | - | Se assinaturas NÃO coincidem → Lança `UnauthorizedAccessException` (pula para EX02) |
| 12 | - | Se assinaturas coincidem → Valida sucesso, prossegue processamento |
| 13 | - | Reconstrói body stream: `Request.Body = new MemoryStream(Encoding.UTF8.GetBytes(body))` |
| 14 | - | Controller `WebhookController` recebe payload deserializado: `WebhookNotificacaoDto` |
| 15 | - | Identifica tipo de evento: `dto.Tipo` (fatura_gerada, consumo_atualizado, linha_alterada, portabilidade_concluida) |
| 16 | - | **Se tipo = "fatura_gerada"** → Executa `ProcessarFaturaGerada(operadoraId, dto)` → Importa fatura automaticamente |
| 17 | - | **Se tipo = "consumo_atualizado"** → Executa `InvalidarCacheAsync(operadoraId, dto.Msisdn)` → Invalida cache para forçar atualização |
| 18 | - | **Se tipo = "linha_alterada"** → Executa `AtualizarLinhaAsync(operadoraId, dto)` → Atualiza estado da linha (ex: bloqueada) |
| 19 | - | **Se tipo = "portabilidade_concluida"** → Executa `AtualizarPortabilidadeAsync(dto)` → Marca portabilidade como concluída |
| 20 | - | Registra auditoria (código: `INT_OPR_WEBHOOK_RCV`) → OperadoraId, TipoEvento, Validação HMAC=sucesso, Payload sanitizado |
| 21 | - | Retorna HTTP 202 Accepted |
| 22 | Operadora recebe confirmação de recebimento | - |

### 5. Fluxos Alternativos

**FA01: Webhook com Tipo de Evento Desconhecido**

- Passo 15: Sistema identifica `dto.Tipo` não reconhecido (ex: "evento_xyz")
- Sistema loga aviso: "Evento desconhecido recebido: evento_xyz"
- Sistema registra auditoria com TipoEvento = "desconhecido"
- Retorna HTTP 202 Accepted (aceita mas ignora)

**FA02: Processamento Assíncrono de Webhook**

- Passo 16-19: Sistema enfileira job Hangfire para processar evento em background
- Retorna HTTP 202 Accepted imediatamente (não bloqueia operadora)
- Job processa evento de forma assíncrona
- Se job falha → Retry automático 3 vezes

### 6. Exceções

**EX01: Header X-Signature Ausente**

- Passo 5: Sistema não encontra header `X-Signature`
- Sistema lança `UnauthorizedAccessException("Header X-Signature ausente")`
- Retorna HTTP 401 Unauthorized
- Registra auditoria com Status = "assinatura_ausente"
- Operadora recebe erro e deve reenviar com assinatura

**EX02: Assinatura HMAC Inválida**

- Passo 11: Assinatura recebida ≠ assinatura calculada
- Sistema lança `UnauthorizedAccessException("Assinatura inválida")`
- Retorna HTTP 401 Unauthorized
- Registra auditoria com Status = "assinatura_invalida", incluindo assinatura recebida (sanitizada)
- Sistema loga alerta de segurança: "Tentativa de webhook com assinatura inválida de IP: {ip}"

**EX03: Payload JSON Inválido**

- Passo 14: Sistema tenta deserializar body → JSON malformado
- Sistema lança `JsonException`
- Retorna HTTP 400 Bad Request
- Exibe mensagem: "Payload JSON inválido"
- Registra auditoria com Status = "payload_invalido"

### 7. Pós-condições

- Webhook recebido e autenticado via HMAC-SHA256
- Evento processado conforme tipo (fatura importada, cache invalidado, linha atualizada, portabilidade concluída)
- Auditoria registrada em AuditLog com validação HMAC e payload sanitizado
- Operadora recebe confirmação HTTP 202 Accepted
- Sistema mantém consistência de dados com operadora em tempo real

### 8. Regras de Negócio Aplicáveis

- **RN-INT-105-01**: Credenciais Seguras por Operadora (ClientSecret usado para HMAC)
- **RN-INT-105-04**: Validação HMAC-SHA256 de Webhook
- **RN-INT-105-06**: Cache de Consumo em Tempo Real (invalidação via webhook)
- **RN-INT-105-08**: Multi-tenancy com ClienteId e OperadoraId
- **RN-INT-105-09**: Auditoria Obrigatória de Requisições API

---

**Última Atualização**: 2025-12-28
**Autor**: Claude Code
**Revisão**: Pendente

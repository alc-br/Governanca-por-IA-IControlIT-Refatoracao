# UC-RF098 - Casos de Uso - Auditoria de Logs do Sistema

## UC01: Visualizar e Buscar Logs com Filtros Avançados e KQL

### 1. Descrição

Este caso de uso permite que Administradores, Gerentes de TI e Analistas de Segurança visualizem logs centralizados do sistema com filtros avançados (nível, período, usuário, correlação) e executem queries complexas usando Kusto Query Language (KQL) para diagnóstico e investigação.

### 2. Atores

- Administrador (principal)
- Gerente de TI
- Analista de Segurança
- Sistema (Application Insights)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `log:view` ou `log:search`
- Multi-tenancy ativo (ClienteId válido)
- Application Insights configurado e indexando logs
- Serilog registrando logs estruturados

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /admin/logs | - |
| 2 | - | Valida permissão RBAC (log:view) |
| 3 | - | Aplica filtro multi-tenancy automático (WHERE ClientId = currentClienteId em contexto Serilog) |
| 4 | - | Exibe filtros: Nivel (mat-select multi: Trace/Debug/Info/Warning/Error/Critical), DataInicio (mat-datepicker), DataFim, Usuario (mat-autocomplete), Mensagem (mat-input), CorrelationId (mat-input), StatusCode (mat-input), Path (mat-input) |
| 5 | Preenche filtros: Nivel = [Error, Critical], DataInicio = 2025-12-27, DataFim = 2025-12-28 | - |
| 6 | Clica em "Buscar" | - |
| 7 | - | Executa GET /api/logs?level=Error,Critical&startDate=2025-12-27&endDate=2025-12-28&clienteId={clienteId} |
| 8 | - | Backend constrói query KQL para Application Insights: `traces \| where timestamp >= datetime(2025-12-27) and timestamp <= datetime(2025-12-28) \| where severityLevel >= 3 \| where customDimensions.ClienteId == "{clienteId}" \| order by timestamp desc \| take 100` |
| 9 | - | Executa query contra Application Insights REST API: POST https://api.applicationinsights.io/v1/apps/{app-id}/query |
| 10 | - | Application Insights retorna JSON com colunas: timestamp, severityLevel (0-5), message, operation_Id (TraceId), customDimensions (UserId, ClienteId, IP, UserAgent, SessionId, Path, StatusCode, ResponseTime), exception (stackTrace) |
| 11 | - | Backend mapeia para LogDto: `{ Timestamp, Level (enum), Message, UserId, ClienteId, IP, TraceId, Path, StatusCode, ResponseTime, Exception }` paginado (50 registros/página) |
| 12 | - | Retorna HTTP 200 com lista de LogDto + metadados (totalCount, page, pageSize) |
| 13 | - | Frontend exibe tabela mat-table com colunas: Timestamp (formato local timezone), Nivel (badge: Critical=red, Error=orange, Warning=yellow, Info=blue), Mensagem (truncada 100 chars), Usuario, IP, Path, StatusCode, ResponseTime (ms), TraceId (link clicável) |
| 14 | Usuário visualiza 87 registros de erro entre 27-28/12 | - |
| 15 | Ordena tabela por "ResponseTime" DESC (mat-sort) | - |
| 16 | - | Re-executa query com `\| order by customDimensions.ResponseTime desc` |
| 17 | Usuário filtra apenas erros com ResponseTime > 5000ms digitando ">5000" em campo ResponseTime | - |
| 18 | - | Aplica filtro local (TypeScript): `logs.filter(x => x.ResponseTime > 5000)` ou re-executa query com `\| where customDimensions.ResponseTime > 5000` |
| 19 | Clica em ícone "Expandir" em uma linha | - |
| 20 | - | Abre modal LogDetalhesComponent exibindo: JSON completo (customDimensions), Exception (stackTrace formatado), Contexto completo (UserId, SessionId, UserAgent, IP, ClienteId), Botão "Ver Correlação" |
| 21 | Clica em "Ver Correlação" (botão com TraceId) | - |
| 22 | - | Redireciona para /admin/logs/correlation/{traceId} |

### 5. Fluxos Alternativos

**FA01: Busca Avançada com KQL Customizado**
- Passo 5: Usuário clica em toggle "Modo Avançado (KQL)"
- Sistema exibe editor de código (Monaco Editor) com syntax highlighting para Kusto Query Language
- Usuário digita query customizada: `traces | where severityLevel >= 3 | where message contains "timeout" | summarize count() by bin(timestamp, 1h), tostring(customDimensions.Path) | render timechart`
- Passo 7: POST /api/logs/search com body `{ query: "...", clienteId }` ao invés de filtros simples
- Backend adiciona automaticamente filtro multi-tenancy: `... | where customDimensions.ClienteId == "{clienteId}"`
- Executa query em Application Insights, retorna resultado (tabela ou gráfico)
- Se query retornar série temporal → Frontend renderiza Chart.js line chart
- Se query retornar tabela → Frontend exibe mat-table

**FA02: Exportar Logs em JSON ou CSV**
- Passo 14: Usuário clica em "Exportar Logs"
- Sistema exibe modal com opções: Formato (JSON/CSV), Incluir Exception (checkbox), Limite de Registros (input numérico, max 10.000)
- Usuário seleciona: Formato=CSV, Limite=5000
- POST /api/logs/export `{ formato: "CSV", filtros, limite: 5000, clienteId }`
- Backend executa query KQL com `| take 5000`, usa CsvHelper para gerar CSV
- CSV tem colunas: Timestamp, Level, Message, UserId, IP, Path, StatusCode, ResponseTime, TraceId
- Retorna arquivo: `Content-Disposition: attachment; filename="logs-2025-12-27-2025-12-28.csv"`
- Frontend faz download do arquivo

**FA03: Salvar Busca Favorita**
- Após passo 6: Usuário clica em "Salvar Busca"
- Sistema abre modal: Nome da Busca (input), Compartilhar com Equipe (checkbox)
- Usuário preenche: Nome="Erros de Timeout Últimos 7 Dias", Compartilhar=true
- POST /api/logs/saved-searches `{ nome, filtros (JSON), compartilhar, usuarioId, clienteId }`
- Backend cria SavedSearch: `{ Nome, Filtros (JSON serializado), CompartilharComEquipe, CriadoPor, ClienteId }`
- Busca fica disponível em dropdown "Buscas Salvas" na tela
- Usuário pode carregar busca clicando no dropdown

### 6. Exceções

**EX01: Usuário sem permissão de visualização**
- Passo 2: Se usuário não tem `log:view` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para visualizar logs do sistema"

**EX02: Query KQL inválida (sintaxe)**
- Passo 8 (FA01): Se query KQL tem erro de sintaxe → Application Insights retorna HTTP 400
- Backend captura erro, retorna HTTP 400 com mensagem: "Sintaxe KQL inválida: {detalhe do erro}"
- Frontend exibe toast com erro de validação

**EX03: Application Insights indisponível**
- Passo 9: Se Application Insights REST API retorna timeout ou HTTP 503 → Backend captura exceção
- Retorna HTTP 503 com mensagem: "Serviço de logs temporariamente indisponível. Tente novamente em alguns minutos"
- Frontend exibe mensagem de erro com botão "Tentar Novamente"

**EX04: Tentativa de acessar logs de outro cliente (violação multi-tenancy)**
- Passo 8: Se backend detectar que query tenta buscar ClienteId != currentClienteId → Bloqueia query
- Retorna HTTP 403 com mensagem: "Acesso negado: Tentativa de acessar logs de outro cliente"
- Registra alertade segurança: `{ TipoAlerta = ViolacaoMultiTenancy, UsuarioId, ClienteIdTentado }`

**EX05: Período de busca inválido (> 90 dias)**
- Passo 6: Se DataFim - DataInicio > 90 dias → Retorna HTTP 400 Bad Request
- Exibe mensagem: "Período máximo de busca é 90 dias. Reduza o intervalo ou use exportação de logs arquivados"

### 7. Pós-condições

- Lista de logs exibida com filtros aplicados
- Operação registrada em auditoria (RF004): `{ Operacao = AUD_LOG_READ, UsuarioId, Filtros (JSON), QtdResultados, DataHora }`
- Se exportação solicitada: Arquivo CSV/JSON gerado
- Se busca salva: Registro criado em SavedSearch

### 8. Regras de Negócio Aplicáveis

- RN-LOG-098-01: Registro Obrigatório de Todas as Operações (logs estruturados em Application Insights)
- RN-LOG-098-02: Contexto Completo Obrigatório (timestamp UTC, nível, mensagem, UserId, ClienteId, IP, TraceId)
- RN-LOG-098-03: Níveis de Log Conforme Severidade (Trace=0, Debug=1, Info=2, Warning=3, Error=4, Critical=5)
- RN-LOG-098-05: Conformidade LGPD - Dados sensíveis mascarados (passwords, tokens nunca aparecem)
- Multi-tenancy: Filtro automático WHERE customDimensions.ClienteId = currentClienteId
- RBAC: Permissão `log:view` ou `log:search` obrigatória

---

## UC02: Rastrear Requisição Completa via TraceId e Correlação

### 1. Descrição

Este caso de uso permite que Administradores ou Gerentes de TI rastreiem uma requisição completa através de toda a plataforma (frontend → backend → banco → cache → resposta) usando TraceId/CorrelationId para diagnóstico de problemas distribuídos.

### 2. Atores

- Administrador (principal)
- Gerente de TI
- Sistema (Application Insights, Serilog)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `log:search`
- Multi-tenancy ativo (ClienteId válido)
- TraceId válido existente em logs

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /admin/logs/correlation/{traceId} ou clica em link TraceId na lista de logs (UC01) | - |
| 2 | - | Valida permissão RBAC (log:search) |
| 3 | - | Executa GET /api/logs/correlation/{traceId}?clienteId={clienteId} |
| 4 | - | Backend constrói query KQL unificada para Application Insights: `union (traces \| where operation_Id == "{traceId}"), (customEvents \| where operation_Id == "{traceId}"), (dependencies \| where operation_Id == "{traceId}"), (requests \| where operation_Id == "{traceId}") \| where customDimensions.ClienteId == "{clienteId}" \| order by timestamp asc` |
| 5 | - | Application Insights retorna todos eventos relacionados ao TraceId: traces (logs gerais), requests (requisições HTTP), dependencies (chamadas externas: banco, cache, APIs), customEvents (eventos customizados) |
| 6 | - | Backend agrupa eventos em timeline sequencial ordenada por timestamp ascendente |
| 7 | - | Calcula duração total: `DuracaoTotal = max(timestamp) - min(timestamp)` |
| 8 | - | Identifica gargalos: operações com duration > 1000ms ou dependencies com resultCode != 200 |
| 9 | - | Retorna HTTP 200 com CorrelationDto: `{ TraceId, DuracaoTotal, TotalEventos, Eventos: [ { Timestamp, Tipo (request/trace/dependency/customEvent), Nome, Duracao, ResultCode, Mensagem, Exception } ], Gargalos: [ { Tipo, Nome, Duracao } ] }` |
| 10 | - | Frontend exibe timeline vertical (mat-timeline ou component customizado): Cada evento é um nó na linha do tempo, conectados por linhas (setas), cores diferentes por tipo (request=blue, trace=grey, dependency=green, error=red) |
| 11 | - | Exibe header com resumo: TraceId, Duração Total (ex: 2.345s), Total de Eventos (ex: 23), Status Final (Success/Error baseado em último resultCode), Timestamp Inicial, Timestamp Final |
| 12 | Usuário visualiza timeline completa da requisição | - |
| 13 | - | Exibe seção "Gargalos Detectados" (mat-card) listando operações lentas: "Consulta ao banco: SELECT * FROM Usuarios → 1.8s (gargalo)", "Chamada API Externa: https://api.externa.com → 800ms" |
| 14 | Clica em um evento "Dependency: Consulta SQL" na timeline | - |
| 15 | - | Abre modal com detalhes: Tipo=Dependency, Target=SQL Database, Command="SELECT * FROM Usuarios WHERE ClienteId = @p0", Duracao=1.823ms, ResultCode=200, Data (customDimensions completo em JSON) |
| 16 | - | Modal exibe query SQL formatada (syntax highlighting), parâmetros (@p0 = 123), tempo de execução, linhas retornadas (se disponível) |
| 17 | Clica em "Exportar Timeline" (botão) | - |
| 18 | - | POST /api/logs/correlation/{traceId}/export formato=JSON |
| 19 | - | Backend gera JSON estruturado com timeline completa + gargalos |
| 20 | - | Retorna arquivo: `correlation-{traceId}.json` |
| 21 | Usuário salva arquivo para análise posterior ou anexa em ticket | - |

### 5. Fluxos Alternativos

**FA01: TraceId com Múltiplos Serviços (Microserviços)**
- Passo 5: Se TraceId passou por múltiplos serviços (ex: API Gateway → Auth Service → User Service → Database)
- Query KQL agrupa por `cloud_RoleName` (nome do serviço): `... | extend Servico = cloud_RoleName | summarize count(), avg(duration) by Servico`
- Timeline exibe agrupamento por serviço: Seção "API Gateway" (eventos 1-3), Seção "Auth Service" (eventos 4-7), Seção "User Service" (eventos 8-15)
- Exibe duração por serviço: API Gateway 150ms, Auth Service 80ms, User Service 2.100ms (gargalo identificado)

**FA02: TraceId com Exception (Erro)**
- Passo 5: Se algum evento tem severityLevel >= 4 (Error ou Critical) ou exception != null
- Timeline marca evento com ícone de erro (⚠️ vermelho)
- Seção "Erros Detectados" (mat-card) exibe: Exception Type (ex: SqlException), Exception Message ("Timeout expired"), StackTrace (formatado, primeiras 10 linhas)
- Usuário pode expandir stackTrace completo clicando em "Ver Stack Completo"

**FA03: Buscar TraceId por Parâmetros (reverso)**
- Passo 1: Usuário não tem TraceId, mas tem: UserId, Path, Timestamp aproximado
- Acessa /admin/logs e filtra: Usuario="USR-001", Path="/api/usuarios/create", DataInicio=2025-12-27 10:30, DataFim=2025-12-27 10:35
- Sistema retorna lista de requisições (cada uma com TraceId único)
- Usuário identifica a requisição relevante pela mensagem ou StatusCode, clica em link TraceId
- Redireciona para /admin/logs/correlation/{traceId} (fluxo principal continua no passo 2)

### 6. Exceções

**EX01: TraceId não encontrado**
- Passo 4: Se query KQL retorna 0 resultados → Retorna HTTP 404 Not Found
- Exibe mensagem: "TraceId {traceId} não encontrado. Verifique se o ID está correto ou se logs foram arquivados (> 30 dias)"

**EX02: TraceId pertence a outro cliente (violação multi-tenancy)**
- Passo 4: Se eventos do TraceId têm customDimensions.ClienteId != currentClienteId → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Acesso negado: TraceId pertence a outro cliente"
- Registra alerta de segurança

**EX03: Timeline muito longa (> 10.000 eventos)**
- Passo 5: Se count de eventos > 10.000 → Retorna HTTP 400 Bad Request
- Exibe mensagem: "TraceId tem mais de 10.000 eventos. Use filtros adicionais ou exporte dados"

### 7. Pós-condições

- Timeline completa exibida com todos eventos correlacionados
- Gargalos identificados automaticamente
- Operação registrada em auditoria: `{ Operacao = AUD_TRACE_SEARCH, UsuarioId, TraceId, QtdEventos, DataHora }`
- Se exportação solicitada: Arquivo JSON gerado

### 8. Regras de Negócio Aplicáveis

- RN-LOG-098-04: TraceId Obrigatório para Rastreamento E2E (propagado em toda requisição)
- RN-LOG-098-09: Correlação Automática de Eventos Relacionados (operation_Id unifica eventos)
- Multi-tenancy: Filtro automático customDimensions.ClienteId = currentClienteId
- RBAC: Permissão `log:search` obrigatória

---

## UC03: Configurar Alertas Automáticos para Eventos Críticos

### 1. Descrição

Este caso de uso permite que Administradores ou Gerentes de TI configurem regras de alerta automáticas para eventos críticos (taxa de erro > threshold, latência > SLO, evento Critical registrado) com notificações via Teams, email ou PagerDuty.

### 2. Atores

- Administrador (principal)
- Gerente de TI
- Sistema (Application Insights Alert Rules)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `log:configure-alerts`
- Multi-tenancy ativo (ClienteId válido)
- Application Insights configurado
- Webhooks de notificação configurados (Teams, PagerDuty)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /admin/logs/alerts/configure | - |
| 2 | - | Valida permissão RBAC (log:configure-alerts) |
| 3 | - | Executa GET /api/logs/alerts retorna lista de AlertRuleDto: `{ Id, Nome, Condicao (query KQL), Threshold, WindowSize (minutos), Severidade, Acoes: [ { Tipo: Teams/Email/PagerDuty, Destinatario } ], Ativo }` |
| 4 | - | Exibe tabela de regras existentes: Nome, Condição, Threshold, Janela (minutos), Severidade, Ações, Status (Ativo/Inativo), Última Disparo |
| 5 | Clica em "Nova Regra de Alerta" | - |
| 6 | - | Abre modal ConfigurarAlertaModalComponent com formulário (mat-stepper 3 passos): Passo 1 - Condição, Passo 2 - Ação, Passo 3 - Revisão |
| 7 | **Passo 1 - Condição**: Seleciona Tipo de Alerta (mat-select): [Taxa de Erro Alta, Latência Acima SLO, Evento Crítico Detectado, Query KQL Customizada] | - |
| 8 | Seleciona: "Taxa de Erro Alta" | - |
| 9 | - | Sistema exibe campos específicos: Threshold (input number com sufixo "%"), Janela de Tempo (mat-select: 1/5/10/15/30 minutos), Operador (mat-select: >, >=, <, <=) |
| 10 | Preenche: Threshold=5, JanelaDeTempo=5 minutos, Operador=">" | - |
| 11 | - | Preview da query KQL gerada: `requests \| where timestamp > ago(5m) \| summarize totalRequests = count(), failedRequests = countif(resultCode >= 400) \| extend errorRate = (failedRequests * 100.0) / totalRequests \| where errorRate > 5` |
| 12 | Clica em "Próximo" | - |
| 13 | **Passo 2 - Ação**: Seleciona Tipo de Notificação (mat-checkbox multi): [Email, Teams, PagerDuty, SMS] | - |
| 14 | Seleciona: Email=true, Teams=true | - |
| 15 | - | Exibe campos: Email Destinatários (mat-chip-list de emails), Teams Webhook URL (input, pré-preenchido se configurado), Severidade do Incidente (mat-select: Baixa/Media/Alta/Critica) |
| 16 | Preenche: EmailDestinatarios=["admin@empresa.com", "ti@empresa.com"], TeamsWebhook=(pré-configurado), Severidade=Alta | - |
| 17 | Clica em "Próximo" | - |
| 18 | **Passo 3 - Revisão**: Exibe resumo: Nome da Regra (input), Condição (readonly: "Taxa de Erro > 5% por 5 min"), Ações (readonly: "Email para admin@empresa.com, ti@empresa.com + Teams webhook"), Ativar Imediatamente (mat-slide-toggle) |
| 19 | Preenche: Nome="Taxa Erro Alta Produção", AtivarImediatamente=true | - |
| 20 | Clica em "Criar Alerta" | - |
| 21 | - | Valida permissão RBAC (log:configure-alerts) |
| 22 | - | Executa POST /api/logs/alerts/configure com body `{ Nome, TipoAlerta, Condicao (JSON), Threshold, WindowSize, Acoes: [ { Tipo, Destinatario } ], Ativo, ClienteId }` |
| 23 | - | Backend cria AlertRule em Application Insights via Azure Management SDK: AlertRuleResource com Condition (ThresholdRuleCondition), Source (RuleMetricDataSource ou RuleLogicDataSource), Actions (webhook para Teams, email SMTP) |
| 24 | - | Registra em banco local: AlertaConfiguracao `{ Nome, QueryKQL, Threshold, WindowSize, Acoes (JSON), Ativo, CriadoPor, ClienteId }` |
| 25 | - | Retorna HTTP 201 com mensagem: "Regra de alerta criada com sucesso. Alerta ativo em 1-2 minutos" |
| 26 | - | Frontend exibe toast de sucesso, atualiza tabela de regras com nova entrada |
| 27 | Usuário visualiza nova regra na lista com Status=Ativo | - |

### 5. Fluxos Alternativos

**FA01: Query KQL Customizada**
- Passo 8: Usuário seleciona "Query KQL Customizada"
- Passo 9: Sistema exibe editor Monaco com syntax highlighting para KQL
- Usuário digita query: `traces | where severityLevel == 5 | where message contains "ServiceCrash" | summarize count() by bin(timestamp, 1m) | where count_ > 0`
- Sistema valida sintaxe KQL (botão "Validar Query") → Executa query de teste em Application Insights
- Se válida → Permite prosseguir, se inválida → Exibe erro de sintaxe

**FA02: Testar Alerta Antes de Ativar**
- Passo 19: Usuário clica em "Testar Alerta" (botão)
- Sistema simula disparo do alerta: Gera evento de teste, envia notificação para canais configurados (email + Teams)
- Email de teste: subject="[TESTE] Taxa Erro Alta Produção", body="Este é um teste de alerta. Se recebeu, configuração está correta"
- Teams webhook: envia adaptive card com banner "[TESTE]"
- Após envio: Exibe mensagem "Alerta de teste enviado. Verifique {email} e canal Teams"

**FA03: Editar Regra Existente**
- Passo 4: Usuário clica em ícone "Editar" em uma regra existente
- Sistema abre modal pré-preenchido com valores atuais (Nome, Condição, Threshold, Ações)
- Usuário altera: Threshold de 5% para 3%
- PUT /api/logs/alerts/{id} com body atualizado
- Backend atualiza AlertRuleResource em Application Insights + registro local
- Retorna HTTP 200, frontend atualiza tabela

**FA04: Desativar Regra Temporariamente**
- Passo 4: Usuário clica em toggle "Ativo/Inativo" em uma regra
- PATCH /api/logs/alerts/{id} `{ Ativo: false }`
- Backend desabilita AlertRuleResource em Application Insights (não deleta)
- Regra para de disparar alertas mas permanece configurada
- Usuário pode reativar clicando novamente no toggle

### 6. Exceções

**EX01: Usuário sem permissão para configurar alertas**
- Passo 21: Se usuário não tem `log:configure-alerts` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para configurar alertas de logs"

**EX02: Query KQL inválida**
- Passo 23: Se query KQL tem erro de sintaxe → Azure Management SDK retorna erro
- Backend captura, retorna HTTP 400 com mensagem: "Query KQL inválida: {detalhe}"
- Frontend exibe erro de validação

**EX03: Webhook Teams inválido**
- Passo 16: Se usuário preenche TeamsWebhook com URL inválida → Validador Angular rejeita
- Exibe erro: "URL do webhook inválida. Formato esperado: https://outlook.office.com/webhook/..."

**EX04: Limite de regras excedido (max 50 por cliente)**
- Passo 23: Se cliente já tem 50 AlertRules → Retorna HTTP 400 Bad Request
- Exibe mensagem: "Limite de 50 regras de alerta atingido. Exclua regras antigas ou contate suporte"

### 7. Pós-condições

- AlertRule criada em Application Insights e banco local
- Regra ativa em 1-2 minutos (propagação Azure)
- Operação registrada em auditoria: `{ Operacao = AUD_ALERT_UPDATE, UsuarioId, AlertaId, RegrasAntes (JSON), RegrasDepois (JSON), DataHora }`
- Quando alerta disparar: Notificações enviadas via canais configurados

### 8. Regras de Negócio Aplicáveis

- RN-LOG-098-07: Alertas Automáticos para Erros Críticos (taxa erro > 5%, latência p95 > SLO, evento Critical)
- RBAC: Permissão `log:configure-alerts` obrigatória
- Multi-tenancy: Alertas isolados por ClienteId

---

## UC04: Visualizar Dashboard de Saúde do Sistema com Métricas RED

### 1. Descrição

Este caso de uso permite que Administradores ou Gerentes de TI visualizem dashboard em tempo real com métricas de observabilidade (RED: Rate de requisições, Error rate, Duration/latência) e KPIs de saúde do sistema.

### 2. Atores

- Administrador (principal)
- Gerente de TI
- Sistema (Application Insights, métricas agregadas)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `log:view`
- Multi-tenancy ativo (ClienteId válido)
- Application Insights coletando métricas RED

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /admin/logs/dashboard | - |
| 2 | - | Valida permissão RBAC (log:view) |
| 3 | - | Executa GET /api/logs/dashboard?periodo=Ultimas24h&clienteId={clienteId} |
| 4 | - | Backend executa múltiplas queries KQL em paralelo para coletar KPIs: |
| 5 | - | **KPI 1: Taxa de Requisições (Rate)**: `requests \| where timestamp > ago(24h) \| where customDimensions.ClienteId == "{clienteId}" \| summarize requestsPerSecond = count() / 86400` |
| 6 | - | **KPI 2: Taxa de Erro (Error Rate)**: `requests \| where timestamp > ago(24h) \| summarize totalRequests = count(), failedRequests = countif(resultCode >= 400) \| extend errorRate = (failedRequests * 100.0) / totalRequests` |
| 7 | - | **KPI 3: Latência p50/p95/p99 (Duration)**: `requests \| where timestamp > ago(24h) \| summarize p50 = percentile(duration, 50), p95 = percentile(duration, 95), p99 = percentile(duration, 99)` |
| 8 | - | **KPI 4: Disponibilidade (Uptime)**: `requests \| where timestamp > ago(24h) \| summarize uptime = (count() - countif(resultCode >= 500)) * 100.0 / count()` |
| 9 | - | **KPI 5: Total de Erros Críticos**: `traces \| where timestamp > ago(24h) \| where severityLevel >= 4 \| count` |
| 10 | - | **KPI 6: Tempo Médio de Busca de Log**: `customEvents \| where name == "LogSearch" \| where timestamp > ago(24h) \| summarize avg(customMeasurements.duration)` |
| 11 | - | Retorna DashboardDto: `{ Rate = 12.5 req/s, ErrorRate = 0.8%, Latencia: { p50 = 120ms, p95 = 450ms, p99 = 1200ms }, Uptime = 99.95%, ErrosCriticos = 3, TempoBuscaLog = 1.2s }` |
| 12 | - | Frontend exibe 6 mat-cards com KPIs: Cada card mostra valor principal (fonte grande), variação vs período anterior (ícone ↑/↓ + percentual verde/vermelho se melhor/pior), sparkline (mini Chart.js line chart últimos 7 dias) |
| 13 | - | Exibe comparação: Rate 12.5 req/s (↑ 8% vs ontem), ErrorRate 0.8% (↓ 0.2% vs ontem, verde = melhoria), Latência p95 450ms (↑ 50ms vs ontem, vermelho = degradação) |
| 14 | - | **Gráfico 1: Taxa de Requisições ao Longo do Tempo** - Chart.js line chart, eixo X = últimas 24h (bins de 1h), eixo Y = requisições/hora |
| 15 | - | **Gráfico 2: Taxa de Erro por Endpoint** - Chart.js bar chart horizontal, eixo X = error rate %, eixo Y = top 10 endpoints com mais erros |
| 16 | - | **Gráfico 3: Latência (percentis) ao Longo do Tempo** - Chart.js multi-line chart, eixo X = últimas 24h, eixo Y = latência (ms), 3 linhas (p50, p95, p99 em cores diferentes) |
| 17 | - | **Gráfico 4: Distribuição de Níveis de Log** - Chart.js pie chart, segmentos = Trace/Debug/Info/Warning/Error/Critical com percentuais |
| 18 | Usuário visualiza dashboard completo | - |
| 19 | Clica em card "Taxa de Erro 0.8%" | - |
| 20 | - | Redireciona para /admin/logs com filtro pré-aplicado: Level=[Error, Critical], Periodo=Ultimas24h |
| 21 | Usuário visualiza lista de erros para investigação | - |

### 5. Fluxos Alternativos

**FA01: Filtrar Dashboard por Período (7 dias, 30 dias, customizado)**
- Passo 3: Usuário seleciona filtro Periodo=Ultimos7Dias no dropdown
- Sistema re-executa queries com `where timestamp > ago(7d)` ao invés de `ago(24h)`
- Recalcula todos KPIs e gráficos para últimos 7 dias
- Comparação "vs período anterior" agora compara com 7 dias anteriores (dias -14 a -7)

**FA02: Drill-down em Gráfico de Taxa de Erro por Endpoint**
- Passo 18: Usuário clica em barra do gráfico "Taxa de Erro por Endpoint" (ex: endpoint "/api/usuarios/create" com 5% erro)
- Sistema abre modal com detalhes: Endpoint, Error Rate, Total Requisições, Falhas, Top 3 erros (StatusCode + count)
- Modal exibe botão "Ver Logs de Erro" → Redireciona /admin/logs?path=/api/usuarios/create&level=Error

**FA03: Atualização Automática em Tempo Real**
- Após passo 18: Sistema inicia polling a cada 30 segundos: executa GET /api/logs/dashboard?periodo=Ultimas24h
- Atualiza KPIs se houver mudança > 5% (evita flickering)
- Animação de transição suave (CSS transition) ao atualizar valores
- Exibe timestamp "Última atualização: 10:35:23" no rodapé

**FA04: Exportar Dashboard em PDF**
- Passo 18: Usuário clica em "Exportar Dashboard"
- Sistema usa html2canvas para capturar screenshot dos cards + gráficos
- Gera PDF com iTextSharp: header (logo + título "Dashboard Saúde do Sistema - {data}"), imagens dos cards/gráficos, tabela com valores numéricos dos KPIs
- Retorna arquivo: `dashboard-logs-{data}.pdf`

### 6. Exceções

**EX01: Usuário sem permissão de visualização**
- Passo 2: Se usuário não tem `log:view` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Acesso negado ao dashboard de logs"

**EX02: Application Insights indisponível**
- Passo 4-10: Se queries KQL falharem → Backend captura exceção
- Retorna HTTP 503 com KPIs parciais (valores que conseguiu coletar) + flag `{ PartialData = true, ErroMensagem = "Application Insights temporariamente indisponível" }`
- Frontend exibe dashboard com dados parciais + banner de aviso

**EX03: Nenhum dado no período selecionado**
- Passo 11: Se todas queries retornam 0 resultados → Retorna HTTP 200 com KPIs zerados
- Frontend exibe mensagem: "Nenhum log registrado no período selecionado"
- Gráficos exibem estado vazio com ícone e mensagem "Sem dados"

### 7. Pós-condições

- Dashboard exibido com KPIs atualizados
- 4 gráficos interativos renderizados (Chart.js)
- Operação registrada em auditoria: `{ Operacao = AUD_DASHBOARD_VIEW, UsuarioId, Periodo, DataHora }`
- Se exportação solicitada: Arquivo PDF gerado

### 8. Regras de Negócio Aplicáveis

- RN-LOG-098-10: Métricas RED (Rate, Errors, Duration) coletadas automaticamente
- Multi-tenancy: Todos KPIs filtrados por customDimensions.ClienteId = currentClienteId
- RBAC: Permissão `log:view` obrigatória

---

## UC05: Arquivar e Restaurar Logs Históricos com Retenção Governada

### 1. Descrição

Este caso de uso permite que Administradores arquivem logs com mais de 30 dias para Azure Blob Storage (retenção 7 anos) e restaurem logs arquivados sob demanda para análise, cumprindo política de retenção LGPD.

### 2. Atores

- Administrador (principal)
- Sistema (Job Hangfire, Azure Blob Storage)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `log:archive`
- Multi-tenancy ativo (ClienteId válido)
- Azure Blob Storage configurado
- Job Hangfire agendado para arquivamento automático

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | (Automático): Job Hangfire ArchiveOldLogsJob executado DIARIAMENTE às 02:00 UTC com RecurringJob.AddOrUpdate("archive-logs", () => job.ExecuteAsync(), "0 2 * * *") | - |
| 2 | - | Job calcula data de corte: `thirtyDaysAgo = UtcNow.AddDays(-30)` |
| 3 | - | Executa query KQL em Application Insights: `traces \| where timestamp < datetime({thirtyDaysAgo}) \| where customDimensions.ClienteId == "{clienteId}" \| project timestamp, severityLevel, message, customDimensions, operation_Id` |
| 4 | - | Application Insights retorna logs com timestamp < 30 dias (ex: 50.000 registros para cliente) |
| 5 | - | Agrupa logs em batches de 1.000 registros para evitar OOM (Out of Memory) |
| 6 | - | Para cada batch: Serializa em JSON Lines (JSONL, um JSON por linha): `{"timestamp":"2024-11-28T10:30:00Z","level":"Error","message":"..."}\n{"timestamp":"2024-11-28T10:31:00Z",...}` |
| 7 | - | Calcula nome do arquivo: `logs-{clienteId}-{date}.jsonl` (ex: logs-CLI001-2024-11-28.jsonl) |
| 8 | - | Faz upload para Azure Blob Storage: BlobClient.UploadAsync(containerName: "logs-archive", blobName: "CLI001/2024-11/{filename}", content: jsonlContent) |
| 9 | - | Blob é criptografado automaticamente com Azure Storage Encryption (AES-256) |
| 10 | - | Registra em banco local: ArquivamentoLog `{ ClienteId, DataCorte = thirtyDaysAgo, QtdRegistros = 50000, BlobPath = "CLI001/2024-11/logs-...", DataArquivamento = UtcNow, Status = Concluido }` |
| 11 | - | Após todos batches: Job completa, registra em auditoria: `{ Operacao = AUD_LOG_ARCHIVE, QtdRegistros = 50000, DataCorte, DataHora }` |
| 12 | (Usuário): Administrador acessa tela /admin/logs/archive | - |
| 13 | - | Valida permissão RBAC (log:archive) |
| 14 | - | Executa GET /api/logs/archive retorna lista de ArquivamentoLogDto: `{ Id, DataCorte, QtdRegistros, BlobPath, DataArquivamento, Status, TamanhoMB }` |
| 15 | - | Exibe tabela: Data de Corte, Quantidade, Tamanho (MB), Data Arquivamento, Status, Ações (Restaurar, Download) |
| 16 | Usuário visualiza histórico de arquivamentos | - |
| 17 | Clica em "Download" em arquivo arquivado (ex: logs de novembro/2024) | - |
| 18 | - | Executa GET /api/logs/archive/{id}/download |
| 19 | - | Backend gera SAS token temporário (válido 1h) para Blob: `BlobClient.GenerateSasUri(permissions: BlobSasPermissions.Read, expiresOn: UtcNow + 1h)` |
| 20 | - | Retorna HTTP 302 redirect para SAS URL ou HTTP 200 com JSON `{ DownloadUrl = sasUrl, ExpiresAt = UtcNow + 1h }` |
| 21 | - | Frontend abre URL em nova aba, navegador faz download do arquivo JSONL |
| 22 | Usuário salva arquivo localmente | - |

### 5. Fluxos Alternativos

**FA01: Restaurar Logs Arquivados para Application Insights (Re-ingestão)**
- Passo 17: Usuário clica em "Restaurar" ao invés de "Download"
- Sistema exibe modal de confirmação: "Restaurar logs arquivados de {data}? Logs serão re-ingeridos no Application Insights (custo adicional)"
- Usuário confirma
- POST /api/logs/archive/{id}/restore
- Backend baixa blob do Azure Storage, faz parse do JSONL
- Para cada log: Re-ingere em Application Insights via REST API: POST https://api.applicationinsights.io/v1/apps/{app-id}/events
- Após re-ingestão: Logs ficam disponíveis em searches normais
- Processo pode demorar (assíncrono via Hangfire job), exibe progresso

**FA02: Exclusão Automática de Logs Antigos (> 7 anos)**
- Job ArchiveOldLogsJob também executa limpeza de logs muito antigos
- Calcula: `sevenYearsAgo = UtcNow.AddYears(-7)`
- Lista blobs no container "logs-archive" com prefix "CLI001/" e filtra por data no nome do arquivo
- Se data no nome < sevenYearsAgo → Executa BlobClient.DeleteAsync()
- Registra em auditoria: `{ Operacao = AUD_LOG_PURGE, QtdArquivos = 5, DataCorte = sevenYearsAgo }`
- Cumprimento LGPD: Dados deletados após 7 anos

**FA03: Direito ao Esquecimento LGPD (Deletar logs de usuário específico)**
- Passo 12: Administrador acessa /admin/logs/lgpd-deletion
- Informa UserId do usuário que solicitou LGPD: "USR-001"
- POST /api/logs/lgpd/delete-user `{ userId: "USR-001", clienteId }`
- Job assíncrono: Busca todos logs em Application Insights com customDimensions.UserId == "USR-001"
- Para cada log: Marca como deletado (adiciona flag `LgpdDeleted = true` em customDimensions, não deleta fisicamente)
- Busca arquivos no Blob Storage, filtra linhas com userId="USR-001", gera novo arquivo JSONL sem essas linhas
- Registra em auditoria: `{ Operacao = AUD_LGPD_DELETION, UserId = "USR-001", QtdLogs = 1523, DataHora }`

### 6. Exceções

**EX01: Usuário sem permissão para arquivar**
- Passo 13: Se usuário não tem `log:archive` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para arquivar ou restaurar logs"

**EX02: Erro ao fazer upload para Blob Storage**
- Passo 8: Se BlobClient.UploadAsync() falha (ex: Azure Storage indisponível) → Job captura exceção
- Marca ArquivamentoLog: `{ Status = Falha, MensagemErro = "Erro ao fazer upload: {detalhe}" }`
- Reagenda job para 1h depois: `jobQueue.EnqueueAsync(new ArchiveOldLogsJob(), delaySeconds: 3600)`

**EX03: SAS token expirado**
- Passo 21: Se usuário tentar acessar SAS URL após 1h → Azure Storage retorna HTTP 403
- Frontend detecta erro, exibe mensagem: "Link de download expirado. Solicite novo download"

### 7. Pós-condições

- Logs com > 30 dias arquivados em Azure Blob Storage
- Registros deletados de Application Insights (limpeza online)
- ArquivamentoLog criado em banco local
- Operação registrada em auditoria: `{ Operacao = AUD_LOG_ARCHIVE, QtdRegistros, DataCorte, DataHora }`
- Se restauração solicitada: Logs re-ingeridos em Application Insights
- Se LGPD solicitado: Logs de usuário marcados como deletados

### 8. Regras de Negócio Aplicáveis

- RN-LOG-098-06: Retenção Governada (30 dias online Application Insights, 7 anos backup Blob Storage, exclusão automática após 7 anos)
- RN-LOG-098-05: Conformidade LGPD - Direito ao Esquecimento (exclusão de logs de usuário sob demanda)
- RBAC: Permissão `log:archive` obrigatória
- Multi-tenancy: Arquivamento isolado por ClienteId

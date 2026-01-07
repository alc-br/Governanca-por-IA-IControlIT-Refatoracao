# UC-RF003 — Casos de Uso: Sistema de Logs, Monitoramento e Observabilidade

**RF:** RF-003 — Sistema de Logs, Monitoramento e Observabilidade
**Epic:** EPIC001-SYS - Sistema e Infraestrutura
**Fase:** Fase 1 - Fundação e Cadastros Base
**Versão:** 2.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF-003**, cobrindo integralmente o comportamento funcional esperado do Sistema de Logs, Monitoramento e Observabilidade.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF003.yaml)
- Massas de Teste (MT-RF003.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**Observação Importante**: RF-003 NÃO é um CRUD tradicional. Logs são eventos append-only (write-only + read-only). Não há criação, edição ou exclusão manual de logs. Logs são gerados automaticamente pelo sistema e consultados posteriormente.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Tipo |
|----|------|----------------|------|
| UC00 | Listar Logs | Usuário Autenticado | Leitura |
| UC01 | Buscar Logs com Filtros Avançados | Usuário Autenticado | Leitura |
| UC02 | Visualizar Detalhes de Log | Usuário Autenticado | Leitura |
| UC03 | Exportar Logs (CSV/JSON) | Usuário Autenticado | Leitura/Export |
| UC04 | Configurar Alertas | Admin DevOps | Configuração |
| UC05 | Visualizar Dashboards de Métricas | Usuário Autenticado | Leitura |
| UC06 | Verificar Health Checks | Usuário Autenticado | Leitura |
| UC07 | Visualizar Tracing Distribuído | Desenvolvedor | Leitura |

**Cobertura:** 7 UCs cobrindo 100% das 12 regras de negócio do RF-003.

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (TenantId/EmpresaId)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis (mascaramento automático)
- Auditoria deve registrar **quem**, **quando** e **qual ação** (acesso a logs sensíveis)
- Mensagens devem ser claras, previsíveis e rastreáveis
- Logs estruturados JSON em todos os pontos (RN-LOG-001)
- Correlation IDs obrigatórios em todos os requests (RN-LOG-003)

---

## UC00 — Listar Logs

### Objetivo
Permitir que o usuário visualize logs do sistema de forma paginada, com filtros básicos (período, nível de log).

### Pré-condições
- Usuário autenticado
- Permissão `SYS.LOGS.READ`

### Pós-condições
- Lista de logs exibida conforme filtros e paginação
- Dados sensíveis mascarados (CPF, senhas)

### Fluxo Principal
1. Usuário acessa funcionalidade "Logs do Sistema"
2. Sistema valida permissão `SYS.LOGS.READ`
3. Sistema carrega últimos 100 logs (padrão) do tenant do usuário
4. Sistema aplica mascaramento automático de dados sensíveis (RN-LOG-004)
5. Sistema exibe lista paginada com colunas: Timestamp, Level, Message, CorrelationId, UserId

### Fluxos Alternativos

#### FA-00-01: Filtrar por Período
1. Usuário seleciona período (ex: últimas 24h, última semana, personalizado)
2. Sistema recarrega logs do período selecionado
3. Sistema exibe lista filtrada

#### FA-00-02: Filtrar por Nível de Log
1. Usuário seleciona nível (Verbose, Debug, Info, Warning, Error, Fatal)
2. Sistema recarrega apenas logs do nível selecionado
3. Sistema exibe lista filtrada

#### FA-00-03: Ordenar por Coluna
1. Usuário clica em cabeçalho de coluna (ex: Timestamp)
2. Sistema reordena lista (ascendente/descendente)
3. Sistema exibe lista ordenada

### Fluxos de Exceção

#### FE-00-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.LOGS.READ`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Permissão SYS.LOGS.READ necessária."
4. Sistema registra tentativa de acesso negado em log de auditoria

#### FE-00-02: Nenhum Log no Período
1. Sistema busca logs do período selecionado
2. Sistema não encontra nenhum log
3. Sistema exibe mensagem "Nenhum log encontrado no período selecionado."
4. Sistema mantém filtros ativos para nova tentativa

### Regras de Negócio
- **RN-UC-00-001**: Somente logs do tenant do usuário (isolamento multi-tenant)
- **RN-UC-00-002**: Dados sensíveis mascarados antes de exibir (CPF, senhas, cartões)
- **RN-UC-00-003**: Paginação padrão 100 registros por página
- **RN-UC-00-004**: Ordenação padrão: Timestamp DESC (mais recentes primeiro)
- **Relacionadas**: RN-LOG-001 (logs estruturados JSON), RN-LOG-004 (mascaramento automático)

---

## UC01 — Buscar Logs com Filtros Avançados

### Objetivo
Permitir que o usuário execute buscas complexas em logs usando múltiplos critérios (correlation ID, user, IP, text search, time range).

### Pré-condições
- Usuário autenticado
- Permissão `SYS.LOGS.SEARCH`

### Pós-condições
- Resultados de busca exibidos conforme critérios
- Query salva em histórico (opcional)

### Fluxo Principal
1. Usuário acessa funcionalidade "Busca Avançada de Logs"
2. Sistema valida permissão `SYS.LOGS.SEARCH`
3. Sistema exibe formulário com campos:
   - Correlation ID (GUID)
   - Usuário (UserId)
   - IP (endereço IP)
   - Nível (Verbose, Debug, Info, Warning, Error, Fatal)
   - Período (data/hora início e fim)
   - Text Search (busca full-text em Message)
4. Usuário preenche critérios desejados
5. Usuário clica em "Buscar"
6. Sistema executa query na agregação de logs (Seq/Elasticsearch)
7. Sistema aplica mascaramento automático de dados sensíveis
8. Sistema exibe resultados paginados (100 por página)

### Fluxos Alternativos

#### FA-01-01: Buscar por Correlation ID
1. Usuário informa apenas Correlation ID (GUID)
2. Sistema busca TODOS logs relacionados ao request (frontend → API → banco → fila → job)
3. Sistema exibe sequência completa de logs (ordenado por Timestamp)
4. **Validação**: Facilita troubleshooting de requests específicos (RN-LOG-003)

#### FA-01-02: Buscar por Text Search (Regex)
1. Usuário informa termo de busca (ex: "Erro ao salvar")
2. Sistema executa busca full-text em campo Message
3. Sistema suporta regex (ex: `erro.*salvar`)
4. Sistema exibe resultados destacando termo buscado

#### FA-01-03: Salvar Query no Histórico
1. Usuário clica em "Salvar Busca"
2. Sistema solicita nome para a query
3. Sistema salva query com nome e critérios
4. Usuário pode reutilizar query salva depois

### Fluxos de Exceção

#### FE-01-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.LOGS.SEARCH`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Permissão SYS.LOGS.SEARCH necessária."
4. Sistema registra tentativa de acesso negado

#### FE-01-02: Query Inválida (Timeout)
1. Usuário executa query muito ampla (ex: buscar "a" em 1 mês de logs)
2. Sistema timeout após 30 segundos
3. Sistema exibe mensagem "Query muito ampla. Refine os critérios de busca."
4. Sistema sugere adicionar período mais curto ou critérios adicionais

### Regras de Negócio
- **RN-UC-01-001**: Busca por Correlation ID retorna TODA cadeia de logs relacionados
- **RN-UC-01-002**: Text search suporta regex (sintaxe Elasticsearch)
- **RN-UC-01-003**: Queries salvas são privadas (apenas usuário que criou vê)
- **RN-UC-01-004**: Timeout padrão 30 segundos (prevenir queries pesadas)
- **Relacionadas**: RN-LOG-001 (JSON pesquisável), RN-LOG-003 (correlation IDs)

---

## UC02 — Visualizar Detalhes de Log

### Objetivo
Permitir que o usuário visualize log completo em formato JSON estruturado, incluindo Exception com stack trace.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.LOGS.READ`

### Pós-condições
- Log completo exibido em formato JSON legível
- Stack trace completo exibido (se erro)

### Fluxo Principal
1. Usuário clica em log específico na lista (UC00 ou UC01)
2. Sistema valida permissão `SYS.LOGS.READ`
3. Sistema busca log completo em agregação (Seq/Elasticsearch)
4. Sistema formata JSON para legibilidade (indentação, syntax highlighting)
5. Sistema exibe modal com JSON completo:
   ```json
   {
     "Timestamp": "2025-12-29T14:23:45.123Z",
     "Level": "Error",
     "Message": "Erro ao salvar usuário",
     "CorrelationId": "a1b2-c3d4-e5f6-7890",
     "UserId": "admin@test.com",
     "TenantId": "tenant-123",
     "IP": "192.168.1.100",
     "UserAgent": "Mozilla/5.0",
     "Exception": {
       "Type": "DbUpdateException",
       "Message": "FK constraint violation",
       "StackTrace": "at IControlIT.Infrastructure...cs:line 127"
     }
   }
   ```
6. Sistema aplica mascaramento automático de dados sensíveis no JSON

### Fluxos Alternativos

#### FA-02-01: Copiar JSON Completo
1. Usuário clica em botão "Copiar JSON"
2. Sistema copia JSON formatado para clipboard
3. Sistema exibe toast "JSON copiado!"

#### FA-02-02: Visualizar Logs Relacionados (Correlation ID)
1. Usuário clica em Correlation ID no JSON
2. Sistema executa busca automática por aquele Correlation ID
3. Sistema exibe TODOS logs relacionados (UC01 FA-01-01)

### Fluxos de Exceção

#### FE-02-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.LOGS.READ`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado."
4. Sistema registra tentativa de acesso negado

#### FE-02-02: Log Não Encontrado (Já Purgado)
1. Sistema busca log na agregação
2. Log já foi deletado por retenção automática (RN-LOG-008)
3. Sistema exibe mensagem "Log não encontrado. Pode ter sido purgado pela política de retenção."

### Regras de Negócio
- **RN-UC-02-001**: JSON exibido com syntax highlighting (legibilidade)
- **RN-UC-02-002**: Dados sensíveis mascarados antes de exibir JSON
- **RN-UC-02-003**: Stack trace completo exibido para erros (Exception não truncado)
- **RN-UC-02-004**: Link para Correlation ID executa busca automática
- **Relacionadas**: RN-LOG-001 (JSON estruturado), RN-LOG-004 (mascaramento)

---

## UC03 — Exportar Logs (CSV/JSON)

### Objetivo
Permitir que o usuário exporte logs para CSV ou JSON para auditoria externa, compliance LGPD/SOX.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.LOGS.EXPORT`

### Pós-condições
- Arquivo CSV ou JSON gerado e baixado
- Auditoria registrada (quem exportou, quando, quantos logs)

### Fluxo Principal
1. Usuário executa busca de logs (UC00 ou UC01)
2. Usuário clica em botão "Exportar"
3. Sistema valida permissão `SYS.LOGS.EXPORT`
4. Sistema exibe modal com opções:
   - Formato: CSV ou JSON
   - Limite: 1000, 10000, 100000, ou Todos
   - Incluir dados sensíveis: Sim (somente Super Admin) ou Não
5. Usuário seleciona opções e confirma
6. Sistema gera arquivo com logs filtrados
7. Sistema aplica mascaramento automático (se "Incluir dados sensíveis" = Não)
8. Sistema inicia download do arquivo
9. Sistema registra auditoria:
   - Usuário: quem exportou
   - Timestamp: quando
   - Quantidade: quantos logs
   - Filtros: quais critérios de busca
   - Motivo: campo obrigatório para auditoria SOX

### Fluxos Alternativos

#### FA-03-01: Exportar com Dados Sensíveis (Super Admin)
1. Super Admin seleciona "Incluir dados sensíveis: Sim"
2. Sistema valida que usuário possui perfil Super Admin
3. Sistema gera arquivo SEM mascaramento
4. Sistema registra auditoria CRÍTICA (acesso a dados sensíveis - retenção 7 anos)

#### FA-03-02: Export Assíncrono (>100k logs)
1. Usuário seleciona "Todos" (>100k logs)
2. Sistema detecta volume grande
3. Sistema exibe mensagem "Export será processado em background. Você receberá e-mail quando concluir."
4. Sistema enfileira job assíncrono
5. Job processa export e envia e-mail com link de download

### Fluxos de Exceção

#### FE-03-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.LOGS.EXPORT`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Permissão SYS.LOGS.EXPORT necessária."
4. Sistema registra tentativa de acesso negado

#### FE-03-02: Export Muito Grande (>1M logs)
1. Usuário tenta exportar >1M logs
2. Sistema rejeita export
3. Sistema exibe mensagem "Export limitado a 1 milhão de logs. Refine os critérios de busca."

#### FE-03-03: Motivo Não Informado (Auditoria SOX)
1. Usuário não preenche campo "Motivo" obrigatório
2. Sistema valida que motivo é obrigatório para exports
3. Sistema exibe mensagem "Campo 'Motivo' obrigatório para auditoria."
4. Sistema não permite export até motivo ser preenchido

### Regras de Negócio
- **RN-UC-03-001**: Formato CSV: colunas Timestamp, Level, Message, CorrelationId, UserId, IP
- **RN-UC-03-002**: Formato JSON: array de objetos estruturados completos
- **RN-UC-03-003**: Mascaramento automático padrão (exceto Super Admin que optar por incluir)
- **RN-UC-03-004**: Auditoria obrigatória de todos exports (compliance SOX)
- **RN-UC-03-005**: Limite máximo 1 milhão de logs por export
- **RN-UC-03-006**: Exports >100k logs processados em background (job assíncrono)
- **Relacionadas**: RN-LOG-004 (mascaramento), RN-LOG-008 (retenção auditoria 7 anos)

---

## UC04 — Configurar Alertas

### Objetivo
Permitir que Admin DevOps configure thresholds de alertas proativos para monitoramento do sistema.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.ALERTS.UPDATE`

### Pós-condições
- Alerta configurado e ativo
- Notificações disparadas quando threshold excedido

### Fluxo Principal
1. Admin DevOps acessa funcionalidade "Configuração de Alertas"
2. Sistema valida permissão `SYS.ALERTS.UPDATE`
3. Sistema exibe lista de alertas pré-definidos:
   - Error Rate > X% (últimos Y minutos)
   - P95 Latency > X ms
   - Disco > X%
   - Memória > X%
   - Dependência Crítica Offline (banco, cache, SMTP)
4. Admin clica em "Editar" em alerta
5. Sistema exibe formulário com campos:
   - Threshold (ex: 5% para error rate)
   - Janela temporal (ex: últimos 5 minutos)
   - Canal de notificação (PagerDuty, Slack, Teams, E-mail)
   - Severidade (Info, Warning, Critical)
   - Status (Ativo/Inativo)
6. Admin ajusta valores e salva
7. Sistema valida threshold (ex: error rate deve ser entre 0.1% e 100%)
8. Sistema ativa alerta
9. Sistema confirma sucesso

### Fluxos Alternativos

#### FA-04-01: Testar Alerta (Dry-Run)
1. Admin clica em "Testar Alerta"
2. Sistema simula threshold excedido
3. Sistema envia notificação teste para canal configurado
4. Admin confirma recebimento
5. Sistema registra teste bem-sucedido

#### FA-04-02: Desabilitar Alerta Temporariamente
1. Admin clica em "Desabilitar"
2. Sistema solicita motivo (obrigatório)
3. Sistema marca alerta como Inativo
4. Sistema registra auditoria (quem desabilitou, quando, motivo)

### Fluxos de Exceção

#### FE-04-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.ALERTS.UPDATE`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Apenas Admin DevOps pode configurar alertas."
4. Sistema registra tentativa de acesso negado

#### FE-04-02: Threshold Inválido
1. Admin informa error rate = 150% (inválido)
2. Sistema valida que threshold deve estar entre 0.1% e 100%
3. Sistema exibe mensagem "Threshold inválido. Error rate deve estar entre 0.1% e 100%."
4. Sistema não salva até valor válido ser informado

#### FE-04-03: Canal de Notificação Offline
1. Admin configura alerta com canal PagerDuty
2. Sistema tenta enviar notificação teste
3. PagerDuty retorna erro (API key inválida ou serviço offline)
4. Sistema exibe mensagem "Erro ao conectar PagerDuty. Verifique API key."
5. Sistema não ativa alerta até canal ser validado

### Regras de Negócio
- **RN-UC-04-001**: Error rate threshold padrão 5% (últimos 5 minutos)
- **RN-UC-04-002**: P95 latency threshold padrão 3 segundos
- **RN-UC-04-003**: Disco threshold padrão 85%
- **RN-UC-04-004**: Memória threshold padrão 90%
- **RN-UC-04-005**: Teste obrigatório antes de ativar alerta
- **RN-UC-04-006**: Desabilitação de alerta crítico exige motivo auditado
- **Relacionadas**: RN-LOG-011 (alertas automáticos)

---

## UC05 — Visualizar Dashboards de Métricas

### Objetivo
Permitir que o usuário visualize dashboards com métricas RED (Rate, Errors, Duration) e saúde geral do sistema.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.METRICS.READ`

### Pós-condições
- Dashboards exibidos com gráficos atualizados (tempo real)

### Fluxo Principal
1. Usuário acessa funcionalidade "Dashboards de Métricas"
2. Sistema valida permissão `SYS.METRICS.READ`
3. Sistema exibe dashboards Grafana embarcados:
   - **Dashboard 1 - RED Metrics**:
     - Rate: Requests/segundo (gráfico linha)
     - Errors: % de erros (gráfico linha + threshold alerta)
     - Duration: P50/P95/P99 latency (gráfico linha)
   - **Dashboard 2 - Saúde Sistema**:
     - CPU (%)
     - Memória (%)
     - Disco (%)
     - Threads ativas
   - **Dashboard 3 - Dependências**:
     - Banco de dados (online/offline)
     - Cache Redis (online/offline)
     - SMTP (online/offline)
     - APIs externas (online/offline)
4. Sistema atualiza dashboards automaticamente (refresh 10 segundos)

### Fluxos Alternativos

#### FA-05-01: Filtrar por Período
1. Usuário seleciona período (últimas 1h, 24h, 7d, 30d)
2. Sistema recarrega métricas do período selecionado
3. Sistema exibe gráficos ajustados

#### FA-05-02: Visualizar Métrica Específica (Drill-Down)
1. Usuário clica em ponto específico do gráfico (ex: pico de latency)
2. Sistema exibe detalhes daquele momento:
   - Timestamp exato
   - Valor da métrica
   - Logs relacionados (correlation IDs daquele período)
3. Usuário pode navegar para logs (UC01)

### Fluxos de Exceção

#### FE-05-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.METRICS.READ`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Permissão SYS.METRICS.READ necessária."

#### FE-05-02: Grafana Offline
1. Sistema tenta carregar dashboards Grafana
2. Grafana não responde (timeout)
3. Sistema exibe mensagem "Dashboards temporariamente indisponíveis. Tente novamente em instantes."
4. Sistema registra incidente (dependência crítica offline)

### Regras de Negócio
- **RN-UC-05-001**: Dashboards atualizam automaticamente (refresh 10s)
- **RN-UC-05-002**: Período padrão: últimas 24 horas
- **RN-UC-05-003**: Thresholds de alerta visíveis nos gráficos (linha vermelha)
- **RN-UC-05-004**: Drill-down permite navegar para logs daquele período
- **Relacionadas**: RN-LOG-009 (métricas RED)

---

## UC06 — Verificar Health Checks

### Objetivo
Permitir que o usuário verifique status de dependências críticas do sistema via endpoint `/health`.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.HEALTH.READ`

### Pós-condições
- Status de saúde exibido (healthy/unhealthy)
- Dependências com problema destacadas

### Fluxo Principal
1. Usuário acessa funcionalidade "Health Checks"
2. Sistema valida permissão `SYS.HEALTH.READ`
3. Sistema executa health checks em todas dependências críticas:
   - Banco de dados (executa SELECT 1)
   - Cache Redis (executa PING)
   - SMTP (valida conectividade porta 587)
   - APIs externas (executa GET /health)
4. Sistema exibe resultado:
   ```json
   {
     "status": "Healthy",
     "dependencies": {
       "database": "Healthy",
       "redis": "Healthy",
       "smtp": "Healthy",
       "external_api": "Healthy"
     },
     "timestamp": "2025-12-29T14:23:45Z"
   }
   ```
5. Sistema colore status (verde = Healthy, vermelho = Unhealthy)

### Fluxos Alternativos

#### FA-06-01: Visualizar Histórico de Health Checks
1. Usuário clica em "Histórico"
2. Sistema exibe gráfico de disponibilidade (uptime %)
3. Sistema lista incidentes de indisponibilidade (quando ficou unhealthy)

#### FA-06-02: Executar Health Check Manual
1. Usuário clica em "Executar Agora"
2. Sistema executa health checks novamente (forçado)
3. Sistema exibe resultado atualizado

### Fluxos de Exceção

#### FE-06-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.HEALTH.READ`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Permissão SYS.HEALTH.READ necessária."

#### FE-06-02: Dependência Crítica Offline
1. Sistema executa health check no banco de dados
2. Banco retorna timeout (offline)
3. Sistema marca status geral como "Unhealthy"
4. Sistema destaca banco de dados em vermelho
5. Sistema dispara alerta proativo (PagerDuty - RN-LOG-011)

### Regras de Negócio
- **RN-UC-06-001**: Health check executado automaticamente a cada 30 segundos
- **RN-UC-06-002**: Status geral "Unhealthy" se QUALQUER dependência crítica falhar
- **RN-UC-06-003**: Timeout padrão 5 segundos por dependência
- **RN-UC-06-004**: Alerta disparado automaticamente se unhealthy
- **Relacionadas**: RN-LOG-010 (health checks endpoint), RN-LOG-011 (alertas)

---

## UC07 — Visualizar Tracing Distribuído

### Objetivo
Permitir que Desenvolvedor visualize rastreamento distribuído de requests entre microservices (OpenTelemetry).

### Pré-condições
- Usuário autenticado
- Permissão `SYS.LOGS.SEARCH` (Desenvolvedor tem acesso)
- Tracing distribuído habilitado (RN-LOG-012)

### Pós-condições
- Diagrama de trace exibido mostrando chamadas entre serviços
- Latência de cada span visível

### Fluxo Principal
1. Desenvolvedor acessa funcionalidade "Tracing Distribuído"
2. Sistema valida permissão `SYS.LOGS.SEARCH`
3. Sistema exibe interface de busca de traces
4. Desenvolvedor informa Trace-Id (GUID do W3C Trace Context)
5. Sistema busca trace na agregação (Jaeger/Zipkin ou Application Insights)
6. Sistema exibe diagrama visual:
   ```
   Frontend (50ms)
     → API (120ms)
       → Database (80ms)
       → Redis (10ms)
     → Queue (30ms)
       → Background Job (200ms)
   ```
7. Sistema destaca spans lentos (>threshold) em vermelho

### Fluxos Alternativos

#### FA-07-01: Buscar por Correlation ID
1. Desenvolvedor informa Correlation ID (GUID)
2. Sistema busca Trace-Id associado àquele Correlation ID
3. Sistema exibe trace completo (mesmo fluxo principal)

#### FA-07-02: Drill-Down em Span
1. Desenvolvedor clica em span específico (ex: Database 80ms)
2. Sistema exibe detalhes do span:
   - Query SQL executada
   - Parâmetros (mascarados se sensíveis)
   - Timestamp início/fim
   - Latência P50/P95/P99 daquele endpoint
3. Desenvolvedor pode navegar para logs daquele span

### Fluxos de Exceção

#### FE-07-01: Usuário Sem Permissão
1. Sistema verifica que usuário não possui `SYS.LOGS.SEARCH`
2. Sistema retorna HTTP 403 Forbidden
3. Sistema exibe mensagem "Acesso negado. Apenas Desenvolvedores têm acesso."

#### FE-07-02: Trace Não Encontrado
1. Sistema busca Trace-Id na agregação
2. Trace já foi purgado (sampling ou retenção automática)
3. Sistema exibe mensagem "Trace não encontrado. Pode ter sido purgado pelo sampling (10%) ou política de retenção."

### Regras de Negócio
- **RN-UC-07-001**: Tracing distribuído segue padrão W3C Trace Context
- **RN-UC-07-002**: Sampling 10% em produção (nem todos traces são coletados)
- **RN-UC-07-003**: Spans lentos (>threshold) destacados em vermelho
- **RN-UC-07-004**: Drill-down permite navegar para logs do span
- **Relacionadas**: RN-LOG-012 (tracing distribuído OpenTelemetry)

---

## 4. MATRIZ DE RASTREABILIDADE (UC → RN)

Validação de cobertura 100% das regras de negócio do RF-003.

| Regra de Negócio | UCs que Cobrem | Observação |
|------------------|----------------|------------|
| RN-LOG-001 (Logs Estruturados JSON) | UC00, UC01, UC02, UC03 | JSON estruturado em todas queries |
| RN-LOG-002 (Níveis por Ambiente) | UC00, UC01 | Filtro por nível (Info, Warning, Error) |
| RN-LOG-003 (Correlation IDs) | UC01 (FA-01-01), UC02 (FA-02-02), UC07 (FA-07-01) | Busca por correlation ID rastreável |
| RN-LOG-004 (Mascaramento) | UC00, UC02, UC03 | Mascaramento automático antes exibir |
| RN-LOG-005 (Sampling 10%) | UC00, UC01, UC07 | Observação: sampling em background |
| RN-LOG-006 (100% Erros Logados) | UC00 (FA-00-02), UC01 | Filtro Error/Fatal sempre disponível |
| RN-LOG-007 (Circuit Breaker) | UC00, UC01, UC02 | Observação: circuit breaker em background |
| RN-LOG-008 (Retenção Automática) | UC02 (FE-02-02) | Log purgado retorna erro específico |
| RN-LOG-009 (Métricas RED) | UC05 | Dashboard completo Rate/Errors/Duration |
| RN-LOG-010 (Health Checks) | UC06 | Endpoint /health com dependências |
| RN-LOG-011 (Alertas Automáticos) | UC04, UC06 (FE-06-02) | Configuração + disparo automático |
| RN-LOG-012 (Tracing Distribuído) | UC07 | OpenTelemetry W3C Trace Context |

**Resultado:** ✅ 100% de cobertura (12/12 regras cobertas por 7 UCs)

---

## 5. OBSERVAÇÕES COMPLEMENTARES

### Diferenças em Relação ao CRUD Tradicional

RF-003 **NÃO É UM CRUD**. Logs são eventos append-only:
- ✅ **Listar** (UC00): sim, listagem de logs existentes
- ✅ **Buscar** (UC01): sim, busca avançada com filtros
- ✅ **Visualizar** (UC02): sim, detalhes do log
- ✅ **Exportar** (UC03): sim, export para compliance
- ❌ **Criar**: NÃO - logs são gerados automaticamente pelo sistema
- ❌ **Editar**: NÃO - logs são imutáveis (append-only)
- ❌ **Excluir**: NÃO - apenas purga automática por retenção (RN-LOG-008)

### Integrações Obrigatórias

Todos os UCs dependem de:
- **Autenticação**: JWT Bearer Token obrigatório
- **Multi-tenancy**: Isolamento por TenantId/EmpresaId
- **RBAC**: Permissões granulares (SYS.LOGS.READ, SEARCH, EXPORT, etc)
- **Auditoria**: Acesso a logs sensíveis auditado (retenção 7 anos)
- **i18n**: Mensagens traduzidas (pt-BR, en, es)

### Tecnologias Envolvidas

- **Serilog**: Structured logging JSON
- **Seq**: Agregação DEV/HOM (interface web)
- **Elasticsearch**: Agregação PRD (escala milhões logs/dia)
- **Prometheus**: Coleta de métricas RED
- **Grafana**: Dashboards visuais (UC05)
- **OpenTelemetry**: Tracing distribuído (UC07)
- **Application Insights**: APM Azure (opcional)
- **PagerDuty/Opsgenie**: Alertas proativos (UC04)

### ROI e Benefícios

- **Redução 95% tempo troubleshooting**: horas → minutos (UC01 correlation ID)
- **SLA 99.9% alcançável**: alertas proativos (UC04, UC06)
- **Compliance LGPD/SOX**: mascaramento + auditoria + retenção (UC03, UC02)
- **Economia $50k/ano**: custo downtime evitado (alertas + health checks)
- **Economia $20k/ano**: tempo engenharia (correlation IDs)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-29 | Versão inicial - 7 UCs cobrindo 100% das 12 regras de negócio do RF-003, matriz de rastreabilidade validada | Agência ALC - alc.dev.br |

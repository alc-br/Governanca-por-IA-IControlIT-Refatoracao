# UC-RF112 - Casos de Uso - Jobs e Tarefas Agendadas

## UC01: Criar Job Agendado com Cron Expression e Validação

### 1. Descrição

Este caso de uso permite que Administradores ou Gestores de TI criem jobs agendados recorrentes (daily, weekly, monthly, custom) ou one-time com validação de Cron expression via Cronos library, isolamento por tenant (ClienteId) e integração com Hangfire para orquestração distribuída.

### 2. Atores

- Administrador
- Gestor de TI
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `job:create` ou `job:admin:full`
- Multi-tenancy ativo (ClienteId válido)
- Hangfire Dashboard acessível

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Jobs → Criar Job | - |
| 2 | - | Valida permissão `job:create` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe formulário com campos: Nome do Job (único por tenant), Descrição, Tipo de Job (dropdown: ImportarFaturas, LimparCache, SincronizarAzureAD, etc.), Cron Expression (com helper/picker), Prioridade (Alta/Média/Baixa), Timeout (min, padrão 30), Retry Count (padrão 3), Requer Two-Step Execution (checkbox) |
| 5 | Preenche formulário | - |
| 6 | Seleciona Cron Expression usando picker ou digita manualmente | - |
| 7 | - | Valida Cron expression via Cronos library: `CronExpression.Parse(expression)` |
| 8 | - | Se válida → Calcula e exibe próxima execução: `cronExpression.GetNextOccurrence(DateTimeOffset.UtcNow)` |
| 9 | - | Se inválida → Mensagem de erro: "Cron expression inválida. Exemplo: 0 2 * * * (diariamente às 2h)" |
| 10 | - | Valida nome único por tenant: `JobRepository.ExistsByNameAsync(ClienteId, Name)` |
| 11 | - | Se nome duplicado → HTTP 400 "Job 'X' já existe para este tenant" |
| 12 | Clica em "Criar Job" | - |
| 13 | - | Executa `POST /api/jobs` com payload: `{ name, description, jobType, cronExpression, priority, timeoutMinutes, retryCount, requiresTwoStepExecution }` |
| 14 | - | Cria entidade Job com status = Active |
| 15 | - | Registra job no Hangfire: `RecurringJob.AddOrUpdate(jobId, () => ExecuteJob(jobId), cronExpression)` |
| 16 | - | Calcula próxima execução e salva em NextExecution |
| 17 | - | Auditoria registrada (JOB_CREATE) com ClienteId, JobId, JobName, JobType, CronExpression |
| 18 | - | HTTP 201 Created retornado com JobDto: `{ id, name, jobType, cronExpression, status, nextExecution }` |
| 19 | - | Mensagem de sucesso exibida: "Job 'X' criado com sucesso. Próxima execução: YYYY-MM-DD HH:MM" |

### 5. Fluxos Alternativos

**FA01: Criar Job One-Time (Sem Recorrência)**
- No passo 6, usuário deixa Cron Expression vazio ou seleciona "One-Time"
- Sistema cria job sem Cron expression
- Job é adicionado à fila imediatamente: `BackgroundJob.Enqueue(() => ExecuteJob(jobId))`
- Após execução, job é automaticamente desativado (status = Completed)

**FA02: Validar Sintaxe de Cron Expression Antes de Submeter**
- Usuário digita Cron expression manualmente
- Sistema valida em tempo real (blur event) usando Cronos.CronExpression.TryParse
- Se inválida, exibe sugestões: "0 2 * * * (diariamente às 2h)", "0 0 * * 0 (semanalmente aos domingos)"
- Badge exibido: "Próxima execução: YYYY-MM-DD HH:MM" ou "Sintaxe inválida"

**FA03: Configurar Two-Step Execution para Jobs Sensíveis**
- Usuário marca checkbox "Requer Two-Step Execution"
- Sistema marca `job.RequiresTwoStepExecution = true`
- Job requer 2 permissões: `job:create` (para criar) + `job:execute` (para executar)
- Na execução, valida ambas permissões antes de processar

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `job:create` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para criar jobs"

**EX02: Nome de Job Duplicado no Tenant**
- Se nome já existe para ClienteId → HTTP 400 Bad Request
- Mensagem: "Job com nome 'X' já existe para este tenant. Escolha outro nome."

**EX03: Cron Expression Inválida**
- Se Cronos.CronExpression.Parse lança exceção → HTTP 400 Bad Request
- Mensagem: "Cron expression inválida. Use formato POSIX: min hour day month dayofweek. Exemplo: 0 2 * * * (diariamente às 2h)"

**EX04: Tipo de Job Não Registrado**
- Se JobType não existe no enum JobTypeEnum → HTTP 400 Bad Request
- Mensagem: "Tipo de job 'X' não é válido. Tipos disponíveis: ImportarFaturas, LimparCache, SincronizarAzureAD, etc."

**EX05: Timeout ou Retry Count Fora do Range**
- Se TimeoutMinutes < 1 ou > 240 → HTTP 400 "Timeout deve estar entre 1 e 240 minutos"
- Se RetryCount < 0 ou > 10 → HTTP 400 "Retry count deve estar entre 0 e 10"

### 7. Pós-condições

- Job criado no banco de dados com status Active
- Job registrado no Hangfire com Cron expression
- Próxima execução calculada e salva
- Auditoria registrada (JOB_CREATE)
- Job visível no Hangfire Dashboard e no grid de Jobs

### 8. Regras de Negócio Aplicáveis

- **RN-JOB-112-01**: Nome único de job por tenant (ClienteId)
- **RN-JOB-112-02**: Cron expression validada via Cronos library
- **RN-JOB-112-03**: Timeout padrão de 30 minutos (configurável entre 1-240 min)
- **RN-JOB-112-04**: Retry padrão de 3 tentativas com backoff exponencial (1, 2, 4 min)
- **RN-JOB-112-08**: Multi-tenancy com ClienteId obrigatório

---

## UC02: Executar Job Manualmente com Enfileiramento e Prioridade

### 1. Descrição

Este caso de uso permite que Administradores executem job agendado imediatamente, sem aguardar próxima execução recorrente, adicionando-o à fila com prioridade configurável (Alta, Média, Baixa) e respeitando limite de 10 workers paralelos por tenant.

### 2. Atores

- Administrador
- Gestor de TI
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `job:execute` ou `job:admin:full`
- Job existe e está ativo (status != Disabled, Deleted, Faulted)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Jobs → Lista de Jobs | - |
| 2 | - | Valida permissão `job:execute` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe grid paginado com Jobs (Nome, Tipo, Status, Próxima Execução, Última Execução, Ações) |
| 5 | Seleciona job desejado | - |
| 6 | Clica em botão "Executar Agora" | - |
| 7 | - | Valida se job.Status == Active |
| 8 | - | Valida se job.RequiresTwoStepExecution == false OU usuário tem permissão `job:execute:sensitive` |
| 9 | - | Conta workers ativos para ClienteId: `GetActiveWorkerCount(ClienteId)` |
| 10 | - | Se workers >= 10 → HTTP 429 "Limite de 10 workers paralelos atingido para este tenant. Aguarde jobs em execução finalizarem." |
| 11 | - | Executa `POST /api/jobs/{id}/execute` |
| 12 | - | Adiciona job à fila Hangfire com prioridade configurada: `BackgroundJob.Enqueue(() => ExecuteJob(jobId), queue: job.Priority)` |
| 13 | - | Cria registro em JobExecutionHistory com status = Enqueued, QueuedAt = DateTime.UtcNow |
| 14 | - | Auditoria registrada (JOB_EXECUTE_MANUAL) com ClienteId, JobId, TriggeredBy (UserId) |
| 15 | - | HTTP 202 Accepted retornado com executionId: `{ executionId, status: "Enqueued", queuedAt, estimatedStartTime }` |
| 16 | - | Mensagem exibida: "Job 'X' adicionado à fila. Execução iniciará em breve." |
| 17 | - | Worker do Hangfire processa job quando disponível |
| 18 | - | Status atualizado em real-time: Enqueued → Running → Succeeded/Failed |

### 5. Fluxos Alternativos

**FA01: Job Requer Two-Step Execution (Aprovação de 2º Usuário)**
- No passo 8, se job.RequiresTwoStepExecution == true:
- Sistema valida se usuário tem permissão `job:execute:sensitive`
- Se não tem → HTTP 403 "Job sensível requer permissão job:execute:sensitive"
- Se tem → Prossegue com execução

**FA02: Executar com Prioridade Alta (Bypass de Fila)**
- Usuário seleciona opção "Executar com Prioridade Alta"
- Job adicionado à fila de prioridade Alta
- Jobs de prioridade Alta são processados antes de Média e Baixa
- Hangfire queue: `BackgroundJob.Enqueue(() => ExecuteJob(jobId), queue: "high")`

**FA03: Cancelar Job em Execução**
- Usuário clica em "Cancelar" em job com status Running
- Sistema executa `BackgroundJob.Delete(executionId)`
- Job marcado como Cancelled em JobExecutionHistory
- Auditoria registrada (JOB_CANCELLED) com motivo

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `job:execute` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para executar jobs"

**EX02: Job Desabilitado ou em Estado Inválido**
- Se job.Status == Disabled, Deleted ou Faulted → HTTP 400 Bad Request
- Mensagem: "Job 'X' está desabilitado e não pode ser executado. Status atual: {status}"

**EX03: Limite de Workers Paralelos Atingido**
- Se workers ativos >= 10 para ClienteId → HTTP 429 Too Many Requests
- Mensagem: "Limite de 10 workers paralelos atingido para este tenant. Aguarde conclusão de jobs em execução."
- Header retornado: `Retry-After: 60` (tentar novamente após 60 segundos)

**EX04: Job Sensível Sem Permissão Adicional**
- Se job.RequiresTwoStepExecution == true e usuário sem `job:execute:sensitive` → HTTP 403
- Mensagem: "Este job requer permissão adicional (job:execute:sensitive) para execução"

### 7. Pós-condições

- Job adicionado à fila Hangfire com prioridade
- Registro criado em JobExecutionHistory com status Enqueued
- Auditoria registrada (JOB_EXECUTE_MANUAL)
- Worker disponível processa job assim que possível
- Status atualizado em real-time no dashboard

### 8. Regras de Negócio Aplicáveis

- **RN-JOB-112-05**: Máximo 10 workers paralelos por ClienteId
- **RN-JOB-112-06**: Two-Step Execution para jobs sensíveis (criar + executar)
- **RN-JOB-112-08**: Multi-tenancy com ClienteId obrigatório
- **RN-JOB-112-09**: Priorização de fila (Alta → Média → Baixa)

---

## UC03: Pausar/Retomar Job Agendado Sem Perder Histórico

### 1. Descrição

Este caso de uso permite que Administradores suspendam temporariamente a execução recorrente de um job agendado (status = Paused) e posteriormente retomem (status = Active) sem perder histórico de execuções anteriores.

### 2. Atores

- Administrador
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `job:update` ou `job:admin:full`
- Job existe e está ativo (status == Active ou Paused)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Jobs → Lista de Jobs | - |
| 2 | - | Valida permissão `job:update` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe grid paginado com Jobs (Nome, Tipo, Status, Próxima Execução, Ações) |
| 5 | Seleciona job com status Active | - |
| 6 | Clica em botão "Pausar" | - |
| 7 | - | Executa `PUT /api/jobs/{id}/pause` |
| 8 | - | Remove job do agendamento Hangfire: `RecurringJob.RemoveIfExists(jobId)` |
| 9 | - | Atualiza status: `job.UpdateStatus(JobStatus.Paused)` |
| 10 | - | Limpa campo NextExecution: `job.NextExecution = null` |
| 11 | - | Auditoria registrada (JOB_PAUSED) com ClienteId, JobId, PausedBy (UserId) |
| 12 | - | HTTP 200 OK retornado |
| 13 | - | Mensagem exibida: "Job 'X' pausado com sucesso. Ele não será executado até ser retomado." |
| 14 | - | Badge exibido no grid: "Status: Pausado" (cor amarela) |
| 15 | Posteriormente, clica em "Retomar" | - |
| 16 | - | Executa `PUT /api/jobs/{id}/resume` |
| 17 | - | Valida se job.Status == Paused |
| 18 | - | Reativa job no Hangfire: `RecurringJob.AddOrUpdate(jobId, () => ExecuteJob(jobId), job.CronExpression)` |
| 19 | - | Atualiza status: `job.UpdateStatus(JobStatus.Active)` |
| 20 | - | Calcula próxima execução: `job.NextExecution = CronExpression.Parse(job.CronExpression).GetNextOccurrence(DateTimeOffset.UtcNow)` |
| 21 | - | Auditoria registrada (JOB_RESUMED) com ClienteId, JobId, ResumedBy (UserId), NextExecution |
| 22 | - | HTTP 200 OK retornado |
| 23 | - | Mensagem exibida: "Job 'X' retomado. Próxima execução: YYYY-MM-DD HH:MM" |
| 24 | - | Badge exibido: "Status: Ativo" (cor verde) |

### 5. Fluxos Alternativos

**FA01: Pausar Job Temporariamente Durante Manutenção**
- Administrador pausa job antes de manutenção programada
- Job não é executado durante manutenção
- Após manutenção, administrador retoma job
- Job volta a executar no próximo horário agendado conforme Cron expression

**FA02: Pausar Job em Massa (Múltiplos Jobs)**
- Administrador seleciona múltiplos jobs usando checkbox
- Clica em "Pausar Selecionados"
- Sistema executa `PUT /api/jobs/batch-pause` com array de IDs
- Todos os jobs selecionados são pausados simultaneamente
- Auditoria individual registrada para cada job

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `job:update` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para pausar/retomar jobs"

**EX02: Job Já Está Pausado (Tentativa de Pausar Novamente)**
- Se job.Status == Paused e usuário tenta pausar → HTTP 400 Bad Request
- Mensagem: "Job 'X' já está pausado"

**EX03: Job Já Está Ativo (Tentativa de Retomar Novamente)**
- Se job.Status == Active e usuário tenta retomar → HTTP 400 Bad Request
- Mensagem: "Job 'X' já está ativo e em execução"

**EX04: Job em Estado Inválido para Pausar/Retomar**
- Se job.Status == Faulted ou Deleted → HTTP 400 Bad Request
- Mensagem: "Job 'X' não pode ser pausado/retomado. Status atual: {status}"

### 7. Pós-condições

- Job pausado: Removido do agendamento Hangfire, status = Paused, NextExecution = null
- Job retomado: Reativado no Hangfire, status = Active, NextExecution calculado
- Histórico de execuções anteriores preservado (não deletado)
- Auditoria registrada (JOB_PAUSED ou JOB_RESUMED)

### 8. Regras de Negócio Aplicáveis

- **RN-JOB-112-10**: Pausar job remove do agendamento Hangfire mas preserva histórico
- **RN-JOB-112-11**: Retomar job recalcula NextExecution baseado em Cron expression atual
- **RN-JOB-112-08**: Multi-tenancy com ClienteId obrigatório

---

## UC04: Visualizar Histórico de Execuções com Logs e Tempo de Execução

### 1. Descrição

Este caso de uso permite que Administradores e Gestores de TI visualizem histórico completo de execuções de um job (timestamp, status, tempo de execução, logs, mensagem de erro) com retenção de 90 dias e filtros avançados.

### 2. Atores

- Administrador
- Gestor de TI
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `job:history:read` ou `job:admin:full`
- Multi-tenancy ativo (ClienteId válido)
- JobExecutionHistory possui registros

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Jobs → Lista de Jobs | - |
| 2 | - | Valida permissão `job:history:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | Seleciona job específico | - |
| 5 | Clica em "Ver Histórico" | - |
| 6 | - | Executa `GET /api/jobs/{id}/executions` com paginação (pageSize = 20, pageNumber = 1) |
| 7 | - | Consulta JobExecutionHistory filtrando por JobId e ClienteId |
| 8 | - | Ordena por StartedAt DESC (mais recente primeiro) |
| 9 | - | Retorna lista paginada com: ExecutionId, StartedAt, FinishedAt, Status (Succeeded, Failed, Enqueued, Running, Cancelled), DurationSeconds, ErrorMessage, LogMessages |
| 10 | - | Exibe tabela com colunas: Data/Hora Início, Duração, Status (badge colorido: verde=Succeeded, vermelho=Failed, azul=Running, amarelo=Enqueued, cinza=Cancelled), Ação (Ver Detalhes) |
| 11 | Usuário clica em "Ver Detalhes" de uma execução | - |
| 12 | - | Executa `GET /api/jobs/executions/{executionId}` |
| 13 | - | Retorna detalhes completos: StartedAt, FinishedAt, Status, DurationSeconds, ErrorMessage, StackTrace (se Failed), LogMessages (array de strings), RetryAttempt (qual tentativa: 1, 2, 3) |
| 14 | - | Modal exibido com detalhes formatados em JSON ou texto estruturado |
| 15 | - | Logs exibidos em ordem cronológica com timestamp |
| 16 | - | Se Status == Failed → ErrorMessage e StackTrace exibidos com destaque |
| 17 | - | Botão "Re-executar Job" disponível se Status == Failed |

### 5. Fluxos Alternativos

**FA01: Filtrar Histórico por Status (Succeeded, Failed, etc.)**
- Usuário seleciona filtro dropdown: "Mostrar apenas: Falhas"
- Sistema aplica filtro: `GET /api/jobs/{id}/executions?status=Failed`
- Tabela atualizada exibindo apenas execuções com Status == Failed

**FA02: Filtrar Histórico por Período (Últimos 7, 30, 90 dias)**
- Usuário seleciona período: "Últimos 7 dias"
- Sistema aplica filtro: `GET /api/jobs/{id}/executions?sinceDate={TODAY-7}`
- Tabela atualizada exibindo apenas execuções dos últimos 7 dias

**FA03: Exportar Histórico para CSV**
- Usuário clica em "Exportar Histórico"
- Sistema executa `GET /api/jobs/{id}/executions/export` com formato CSV
- Arquivo CSV gerado com colunas: JobName, ExecutionId, StartedAt, FinishedAt, Status, DurationSeconds, ErrorMessage
- Download iniciado automaticamente

**FA04: Ver Logs de Execução em Tempo Real (Job Running)**
- Se job está com Status == Running
- Dashboard exibe "Logs ao Vivo" com atualização a cada 5 segundos
- Logs são recuperados de Application Insights ou Redis Stream
- Badge pulsante exibido: "Em Execução - Atualizando logs..."

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `job:history:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para visualizar histórico de jobs"

**EX02: Nenhum Histórico Disponível**
- Se job nunca foi executado → HTTP 200 OK com array vazio
- Mensagem exibida: "Este job ainda não possui execuções registradas"

**EX03: Histórico Fora do Período de Retenção**
- Se execução > 90 dias → Registro deletado automaticamente via job de limpeza
- Mensagem: "Histórico disponível apenas para últimos 90 dias. Registros mais antigos foram removidos."

**EX04: Erro ao Recuperar Logs de Application Insights**
- Se Application Insights indisponível → HTTP 500 Internal Server Error
- Mensagem: "Não foi possível recuperar logs detalhados. Tente novamente em alguns minutos."

### 7. Pós-condições

- Histórico de execuções exibido com detalhes completos
- Logs acessíveis para troubleshooting
- Filtros aplicados corretamente
- Exportação de histórico disponível

### 8. Regras de Negócio Aplicáveis

- **RN-JOB-112-12**: Histórico retido por 90 dias, deletado automaticamente após período
- **RN-JOB-112-13**: Logs armazenados em Application Insights + Redis Stream para jobs ativos
- **RN-JOB-112-08**: Multi-tenancy com ClienteId obrigatório

---

## UC05: Monitorar Jobs em Tempo Real via Hangfire Dashboard

### 1. Descrição

Este caso de uso permite que Administradores monitorem jobs em tempo real através do Hangfire Dashboard embarcado, visualizando workers ativos, filas, jobs em execução, métricas de performance e histórico de falhas.

### 2. Atores

- Administrador
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `job:dashboard:read` ou `job:admin:full`
- Hangfire Dashboard habilitado em `/hangfire`
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Jobs → Dashboard | - |
| 2 | - | Valida permissão `job:dashboard:read` |
| 3 | - | Redireciona para `/hangfire` (Hangfire Dashboard embarcado) |
| 4 | - | Hangfire Dashboard aplica filtro multi-tenancy (DashboardAuthorizationFilter) |
| 5 | - | Exibe overview com métricas: Jobs Agendados (Total), Jobs em Execução (Now), Workers Ativos (X/10), Fila Alta/Média/Baixa (contadores), Falhas Últimas 24h, Sucesso Últimas 24h |
| 6 | - | Atualiza métricas em real-time a cada 5 segundos via polling |
| 7 | Usuário clica em "Recurring Jobs" (Jobs Agendados) | - |
| 8 | - | Exibe lista de jobs recorrentes com: JobId, Nome, Cron Expression, Próxima Execução, Última Execução, Status |
| 9 | - | Badge colorido por Status: Active (verde), Paused (amarelo), Faulted (vermelho) |
| 10 | Usuário clica em "Jobs em Execução" | - |
| 11 | - | Exibe tabela com jobs atualmente processando: JobId, Nome, Worker, Início, Tempo Decorrido (contagem em tempo real), Progress Bar (se disponível) |
| 12 | - | Progress bar atualizada via IProgressBar.SetValue() se job implementa progresso |
| 13 | Usuário clica em "Succeeded Jobs" | - |
| 14 | - | Exibe histórico de jobs bem-sucedidos (últimas 500 execuções) |
| 15 | - | Detalhes: JobId, Nome, Duração, Timestamp |
| 16 | Usuário clica em "Failed Jobs" | - |
| 17 | - | Exibe histórico de jobs falhados (últimas 500 falhas) |
| 18 | - | Detalhes: JobId, Nome, Error Message, StackTrace, Retry Count, Timestamp |
| 19 | - | Botão "Retry" disponível para re-executar job falhado manualmente |
| 20 | Usuário clica em "Servers" | - |
| 21 | - | Exibe lista de servidores Hangfire ativos: ServerName, Workers, Queues, Started At, Heartbeat (última atualização) |
| 22 | - | Heartbeat atualizado a cada 15 segundos |

### 5. Fluxos Alternativos

**FA01: Monitorar Workers em Tempo Real**
- Usuário visualiza contadores de workers ativos: "7/10 workers ativos"
- Sistema exibe breakdown por fila: Alta (2 workers), Média (3 workers), Baixa (2 workers)
- Se workers >= 10 → Badge amarelo "Limite de workers atingido"

**FA02: Re-executar Job Falhado Diretamente do Dashboard**
- Usuário identifica job falhado no histórico
- Clica em botão "Retry"
- Sistema adiciona job à fila novamente: `BackgroundJob.Requeue(jobId)`
- Job adicionado à fila com prioridade Média
- Mensagem exibida: "Job 'X' adicionado à fila para reprocessamento"

**FA03: Cancelar Job em Execução**
- Usuário identifica job com tempo de execução excessivo (> 30 min)
- Clica em "Cancel" no dashboard
- Sistema executa `BackgroundJob.Delete(jobId)`
- Job marcado como Cancelled
- Worker libera slot imediatamente

### 6. Exceções

**EX01: Permissão Negada para Dashboard**
- Se usuário sem permissão `job:dashboard:read` → HTTP 403 Forbidden
- Hangfire Dashboard retorna tela de erro: "Access Denied"

**EX02: Hangfire Dashboard Indisponível**
- Se Redis (storage Hangfire) indisponível → HTTP 503 Service Unavailable
- Mensagem: "Dashboard temporariamente indisponível. Verifique conectividade com Redis."

**EX03: Filtro Multi-Tenancy Falha**
- Se ClienteId não pode ser determinado → HTTP 400 Bad Request
- Mensagem: "Não foi possível identificar tenant. Faça login novamente."

### 7. Pós-condições

- Métricas de jobs exibidas em real-time
- Administrador tem visibilidade completa de workers, filas e execuções
- Jobs falhados podem ser re-executados diretamente
- Workers ativos monitorados

### 8. Regras de Negócio Aplicáveis

- **RN-JOB-112-05**: Máximo 10 workers paralelos por ClienteId (exibido no dashboard)
- **RN-JOB-112-08**: Multi-tenancy com filtro no Hangfire Dashboard
- **RN-JOB-112-14**: Dashboard atualizado em real-time a cada 5 segundos
- **RN-JOB-112-15**: Retenção de histórico de 500 execuções por tipo (Succeeded, Failed)

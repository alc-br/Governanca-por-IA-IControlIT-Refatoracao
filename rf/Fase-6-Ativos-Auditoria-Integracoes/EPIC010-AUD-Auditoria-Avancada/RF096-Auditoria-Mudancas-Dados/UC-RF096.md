# UC-RF096 - Casos de Uso - Auditoria de Mudanças de Dados

**Versão**: 1.0 | **Data**: 2025-12-29
**RF Relacionado**: RF-096 | **EPIC**: EPIC010-AUD-Auditoria-Avancada
**Fase**: Fase 6 - Ativos, Auditoria e Integrações

---

## UC01: Rastrear Mudanças Automaticamente com EF Core Interceptor e Decorador [Audited]

### 1. Descrição

Este caso de uso permite ao sistema capturar automaticamente todas as operações CRUD (Create, Update, Delete) em entidades decoradas com `[Audited]`, registrando valores before/after de cada campo alterado sem necessidade de código adicional no handler.

### 2. Atores

- Sistema (EF Core Change Tracker + AuditInterceptor)
- Desenvolvedor (aplica decorador `[Audited]` na entidade)
- Usuário (executa operação CRUD que dispara auditoria)

### 3. Pré-condições

- Entidade decorada com atributo `[Audited]`
- AuditInterceptor registrado no DbContext: `optionsBuilder.AddInterceptors(new AuditInterceptor(userService, logger))`
- Tabela AuditLog criada no banco de dados
- Usuário autenticado (CurrentUserService fornece UserId, IP, UserAgent)
- Multi-tenancy ativo (ClienteId extraído do token JWT)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Desenvolvedor aplica decorador na entidade: `[Audited] public class Ativo : AggregateRoot { ... }` | - |
| 2 | Usuário executa operação (ex: PUT /api/ativos/123 para atualizar Nome) | - |
| 3 | - | Controller recebe request, valida permissões RBAC |
| 4 | - | Handler executa comando: `UpdateAtivoCommand` |
| 5 | - | Entity modificada no DbContext: `ativo.Nome = "Notebook Novo"` |
| 6 | - | Handler chama `await _context.SaveChangesAsync()` |
| 7 | - | AuditInterceptor.SavingChangesAsync() intercepta ANTES de salvar |
| 8 | - | Recupera todas entidades modificadas: `var entries = dbContext.ChangeTracker.Entries().Where(e => e.Entity.GetType().GetCustomAttribute<AuditedAttribute>() != null)` |
| 9 | - | Para cada entry: Verifica estado EntityState (Added, Modified, Deleted) |
| 10 | - | Se EntityState.Added → Chama LogCreation(entry): Captura TODOS campos como NewValue, OldValue = null |
| 11 | - | Se EntityState.Modified → Chama LogModification(entry): Para cada property.IsModified = true, captura OldValue (`property.OriginalValue`) e NewValue (`property.CurrentValue`) |
| 12 | - | Se EntityState.Deleted → Chama LogDeletion(entry): Se entidade implementa ISoftDeletable, registra DeletedAt, DeletedBy, DeletionReason |
| 13 | - | Para cada mudança detectada: Verifica se property tem atributo `[Sensitive]` para marcar IsSensitive = true |
| 14 | - | Cria registro AuditLog: EntityType = "Ativo", EntityId = "123", OperationType = Update, UserId (CurrentUserService), Timestamp = DateTime.UtcNow, IpAddress, UserAgent, ClienteId, EmpresaId |
| 15 | - | Para cada campo modificado: Adiciona FieldChange: FieldName = "Nome", OldValue = "Notebook Antigo", NewValue = "Notebook Novo", DataType = "string", IsSensitive = false |
| 16 | - | Gera CorrelationId (GUID) para agrupar todas mudanças desta transação |
| 17 | - | Adiciona AuditLog ao contexto: `await _auditRepository.AddAsync(auditLog, cancellationToken)` |
| 18 | - | Se campo IsSensitive = true → Dispara SensitiveDataChangeAlert: `await _alertService.SendAsync(new SensitiveDataChangeAlert { EntityType, FieldName, UserId, Timestamp, OldValue, NewValue })` |
| 19 | - | Se operação é CRÍTICA (Delete, Update de Permissão) → Envia para Azure Sentinel: `await _sentinelService.SendAuditEventAsync(auditLog)` |
| 20 | - | SaveChangesAsync() completa: AuditLog persiste + Entidade persiste na MESMA transação |
| 21 | - | Se transação falha → Rollback automático (AuditLog também não persiste) |
| 22 | - | Se transação sucesso → Commit, retorna HTTP 200 ao cliente |

### 5. Fluxos Alternativos

**FA01 - Operação em lote (bulk update de múltiplas entidades):**
- Passo 8: Se ChangeTracker.Entries() retorna 100+ entidades modificadas → Todas recebem MESMO CorrelationId
- Passo 17: 100 registros AuditLog criados, todos com CorrelationId = "abc-123-def"
- Query futura por CorrelationId recupera todas mudanças do lote

**FA02 - Soft delete com rastreamento de motivo:**
- Passo 2: DELETE /api/consumidores/456 com body { deletionReason: "Solicitação LGPD Art.17" }
- Passo 12: Entity implementa ISoftDeletable → DeletedAt = UtcNow, DeletedBy = userId, DeletionReason preenchido
- FieldChange registra: FieldName = "DeletedAt", OldValue = "null", NewValue = "2025-12-29T10:30:00Z"

**FA03 - Mudança em relacionamento (FK):**
- Passo 2: Reatribuir Ativo para outro Consumidor: PUT /api/ativos/123/atribuir com { consumidorId: "uuid-456" }
- Passo 11: Property "ConsumidorId" modificada: OldValue = "uuid-123", NewValue = "uuid-456"
- FieldChange registra FK antes/depois, permitindo rastreamento de cadeia de custódia

### 6. Exceções

**EX01 - Entidade NÃO decorada com [Audited]:**
- Passo 8: Se GetCustomAttribute<AuditedAttribute>() retorna null → Entry ignorado, nenhum AuditLog criado
- Operação CRUD completa normalmente sem auditoria

**EX02 - Falha ao extrair UserId (usuário não autenticado):**
- Passo 14: Se CurrentUserService.GetUserId() retorna null → Lança InvalidOperationException("Cannot audit operation: User not authenticated")
- Transação rollback, operação falha com HTTP 401

**EX03 - Serialização de valor complexo falha (objeto circular):**
- Passo 15: Se property.CurrentValue é objeto complexo e JsonConvert.SerializeObject falha → Captura exceção
- OldValue/NewValue preenchidos com: "{ error: 'Serialization failed', type: '{propertyType}' }"
- Continua auditoria com erro documentado

### 7. Pós-condições

- Registro AuditLog criado no banco de dados com OperationType, Timestamp, UserId, Changes (JSON)
- Se campo sensível LGPD alterado: Alerta enviado para DPO (Data Protection Officer)
- Se operação crítica: Evento enviado para Azure Sentinel (SIEM)
- Trilha auditável imutável disponível para investigação forense
- Entidade principal modificada persistida na mesma transação

### 8. Regras de Negócio Aplicáveis

- RN-AUD-096-01: Rastreamento Automático de Todas as Operações CRUD
- RN-AUD-096-02: Captura de Contexto Completo de Execução (Before/After)
- RN-AUD-096-03: Imutabilidade de Registros de Auditoria
- RN-AUD-096-05: Detecção Automática de Operações em Lote
- RN-AUD-096-08: Alertas Automáticos para Mudanças em Dados Sensíveis LGPD

---

## UC02: Visualizar Timeline de Mudanças com Filtros Avançados e Comparação

### 1. Descrição

Este caso de uso permite ao auditor visualizar histórico completo de mudanças de uma entidade em ordem cronológica, com filtros avançados por campo, usuário, data, tipo de operação e comparação lado-a-lado entre versões.

### 2. Atores

- Auditor (visualiza histórico)
- Sistema (consulta AuditLog e renderiza timeline)

### 3. Pré-condições

- Usuário autenticado com permissão: `audit:read`
- Entidade alvo possui registros em AuditLog
- Multi-tenancy ativo (consulta filtrada por ClienteId automaticamente)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Auditor acessa tela de auditoria: /admin/audit/history | - |
| 2 | Auditor seleciona tipo de entidade (dropdown: Ativo, Consumidor, Fatura, etc) | - |
| 3 | Auditor digita ID da entidade (ex: "uuid-123") ou busca por nome (autocomplete) | - |
| 4 | - | Frontend envia GET /api/audit/Ativo/uuid-123/history |
| 5 | - | Backend valida permissão: PolicyAuthorizationService.ValidateAsync(user, "audit:read") → Se falha retorna HTTP 403 |
| 6 | - | Backend executa query: `var logs = await _context.AuditLogs.Where(a => a.EntityType == "Ativo" && a.EntityId == "uuid-123" && a.ClienteId == clienteId).OrderBy(a => a.Timestamp).ToListAsync()` |
| 7 | - | Se nenhum log encontrado → Retorna HTTP 404 com mensagem i18n: "audit.messages.noChanges" |
| 8 | - | Para cada log: Mapeia para TimelineEntryDto: { Timestamp, OperationType, Username, IpAddress, Changes: [{ FieldName, OldValue, NewValue, IsSensitive }] } |
| 9 | - | Retorna HTTP 200 com JSON: `{ entityType, entityId, timeline: [TimelineEntry], totalCount }` |
| 10 | - | Frontend renderiza timeline em componente vertical com ícones por OperationType (✓ Create, ✎ Update, ✗ Delete) |
| 11 | - | Para cada entrada: Exibe card expansível com: DataHora (formato DD/MM/YYYY HH:mm:ss), Usuário (badge), IP, Lista de campos alterados (tabela com 3 colunas: Campo, Antes, Depois) |
| 12 | Auditor aplica filtros: Data inicial/final (DatePicker), Campo alterado (textbox), Usuário (autocomplete), IP (textbox), Apenas sensíveis LGPD (checkbox) | - |
| 13 | - | Frontend envia GET /api/audit/Ativo/uuid-123/history?startDate=2025-12-01&endDate=2025-12-31&fieldName=Nome&userName=admin&onlySensitive=true |
| 14 | - | Backend aplica filtros dinamicamente: `query.Where(a => a.Timestamp >= startDate).Where(a => a.Timestamp <= endDate).Where(a => a.Changes.Any(c => c.FieldName == fieldName)).Where(a => a.Username.Contains(userName)).Where(a => a.Changes.Any(c => c.IsSensitive))` |
| 15 | - | Retorna apenas logs que atendem todos os filtros |
| 16 | - | Frontend re-renderiza timeline com subset filtrado |
| 17 | Auditor clica em botão "Comparar" ao lado de 2 entradas da timeline | - |
| 18 | - | Frontend envia GET /api/audit/Ativo/uuid-123/diff?timestamp1=2025-12-27T10:00:00Z&timestamp2=2025-12-28T15:00:00Z |
| 19 | - | Backend recupera estados nos 2 timestamps: `state1 = ReconstruirEstado(entityType, entityId, timestamp1)`, `state2 = ReconstruirEstado(entityType, entityId, timestamp2)` |
| 20 | - | Para cada campo: Compara valor em state1 vs state2, identifica diferenças |
| 21 | - | Retorna DiffDto: { campo1: { before: "valor1", after: "valor2", changed: true }, campo2: { before: "valorX", after: "valorX", changed: false } } |
| 22 | - | Frontend exibe modal com comparação lado-a-lado: 2 colunas (Estado em 27/12 | Estado em 28/12), campos alterados destacados em amarelo |
| 23 | Auditor clica em "Exportar Timeline" | - |
| 24 | - | Frontend envia GET /api/audit/Ativo/uuid-123/export?format=csv com filtros aplicados |
| 25 | - | Backend gera arquivo CSV com colunas: Timestamp, OperationType, Username, IpAddress, FieldName, OldValue, NewValue, IsSensitive |
| 26 | - | Retorna FileStreamResult com Content-Disposition: attachment; filename="audit_Ativo_uuid-123_20251229.csv" |
| 27 | - | Frontend baixa arquivo automaticamente |

### 5. Fluxos Alternativos

**FA01 - Filtrar apenas mudanças sensíveis LGPD:**
- Passo 12: Auditor marca checkbox "Apenas Dados Sensíveis"
- Passo 14: Query adiciona `.Where(a => a.Changes.Any(c => c.IsSensitive))` → Retorna apenas mudanças em campos CPF, Email, etc.
- Timeline exibe badge vermelho "LGPD" ao lado de cada entrada

**FA02 - Buscar por valor específico alterado:**
- Passo 12: Auditor digita em campo "Valor Anterior" = "Notebook Antigo"
- Passo 14: Query adiciona `.Where(a => a.Changes.Any(c => c.OldValue.Contains("Notebook Antigo")))` → Retorna apenas mudanças que alteraram esse valor específico

**FA03 - Exportar em formato Excel com formatação:**
- Passo 24: format=excel
- Passo 25: Backend usa ClosedXML library para gerar .xlsx com: Headers em negrito, colunas auto-ajustadas, filtros automáticos, campos sensíveis em vermelho
- Passo 26: Download de arquivo .xlsx formatado

### 6. Exceções

**EX01 - Entidade não possui histórico:**
- Passo 6: Query retorna lista vazia (nenhum AuditLog para este EntityId)
- Passo 7: Retorna HTTP 404 com mensagem: "Nenhuma mudança encontrada para esta entidade"
- Frontend exibe empty state: "Esta entidade ainda não possui histórico de mudanças"

**EX02 - Timestamps inválidos para comparação:**
- Passo 19: Se timestamp1 > timestamp2 (ordem invertida) → Retorna HTTP 400 com mensagem: "timestamp1 deve ser anterior a timestamp2"
- Frontend exibe erro ao usuário

**EX03 - Permissão de exportação negada:**
- Passo 24: Se usuário NÃO tem permissão `audit:export` → Retorna HTTP 403
- Frontend oculta botão "Exportar" para usuários sem permissão

### 7. Pós-condições

- Timeline completa exibida com todas mudanças ordenadas cronologicamente
- Filtros aplicados reduziram conjunto de resultados conforme critérios
- Comparação entre versões exibida em modal com diferenças destacadas
- Arquivo exportado disponível para análise offline ou auditoria externa
- Acesso à timeline registrado em log de auditoria de acesso (RF095)

### 8. Regras de Negócio Aplicáveis

- RN-AUD-096-09: Visualização de Timeline com Filtros Avançados
- RN-AUD-096-14: Exportação de Trilha Auditória para Análise Forense
- RN-004-AUD-01: Auditoria de todas as operações (referência RF-004)

---

## UC03: Executar Rollback de Mudança com Validação de Integridade Referencial

### 1. Descrição

Este caso de uso permite ao gestor de compliance restaurar uma entidade para estado anterior, com validação automática de integridade referencial (FKs) e registro completo da operação de rollback na trilha auditável.

### 2. Atores

- Gestor de Compliance (executa rollback)
- Sistema (valida integridade, executa restauração)

### 3. Pré-condições

- Usuário autenticado com permissão: `audit:rollback` (requer aprovação dual-control)
- Entidade alvo possui histórico em AuditLog
- Timestamp alvo existe no histórico (estado para o qual deseja restaurar)
- Aprovação de gestor superior registrada (workflow de aprovação)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa timeline de mudanças da entidade (conforme UC02) | - |
| 2 | Gestor identifica estado desejado (ex: versão de 27/12/2025 10:00:00) | - |
| 3 | Gestor clica em botão "Restaurar para esta versão" ao lado da entrada da timeline | - |
| 4 | - | Frontend exibe modal de confirmação: "Tem certeza que deseja restaurar Ativo 'Notebook' para o estado de 27/12/2025 10:00:00? Esta ação será registrada em auditoria." |
| 5 | Gestor preenche campo "Motivo do Rollback" (obrigatório): "Correção de alteração acidental por usuário João" | - |
| 6 | Gestor clica em "Confirmar Rollback" | - |
| 7 | - | Frontend envia POST /api/audit/Ativo/uuid-123/rollback com body: `{ targetTimestamp: "2025-12-27T10:00:00Z", reason: "Correção de alteração acidental" }` |
| 8 | - | Backend valida permissão: `audit:rollback` → Se falha retorna HTTP 403 |
| 9 | - | Backend executa ValidateRollbackAsync(entityType, entityId, targetTimestamp) |
| 10 | - | Recupera estado alvo: `targetLog = await _context.AuditLogs.Where(a => a.EntityType == entityType && a.EntityId == entityId && a.Timestamp <= targetTimestamp).OrderByDescending(a => a.Timestamp).FirstOrDefaultAsync()` |
| 11 | - | Se targetLog == null → Retorna HTTP 404 com mensagem: "Estado alvo não encontrado no histórico" |
| 12 | - | Reconstrói estado completo no timestamp alvo: Para cada FieldChange em targetLog, monta dicionário: `{ "Nome": "Notebook Antigo", "Patrimonio": "PAT-001", ... }` |
| 13 | - | Verifica integridade referencial: Se entidade tem FKs (ex: ConsumidorId), valida que relacionamento ainda existe: `await _context.Consumidores.AnyAsync(c => c.Id == consumidorId)` |
| 14 | - | Se FK não existe mais → Retorna HTTP 400 com mensagem: "Não é possível restaurar: Consumidor associado foi deletado. Restaure o Consumidor primeiro." |
| 15 | - | Se entidade tem dependentes (ex: Ativo tem Atribuições), valida que rollback não quebra integridade: `await _context.Atribuicoes.AnyAsync(a => a.AtivoId == ativoId && a.Ativo)` |
| 16 | - | Se rollback quebra integridade → Retorna HTTP 400 com lista de dependências: "Não é possível restaurar: Ativo ainda possui 3 atribuições ativas. Desvincule primeiro." |
| 17 | - | Se validação OK → Inicia transação: `using var transaction = await _context.Database.BeginTransactionAsync()` |
| 18 | - | Recupera entidade atual: `entity = await _context.Ativos.FindAsync(entityId)` |
| 19 | - | Para cada campo no estado alvo: Restaura valor: `property.SetValue(entity, estadoAlvo[fieldName])` usando Reflection |
| 20 | - | Marca entidade como modificada: `_context.Entry(entity).State = EntityState.Modified` |
| 21 | - | Salva mudanças: `await _context.SaveChangesAsync()` → AuditInterceptor captura mudança automaticamente como OperationType.Update |
| 22 | - | Cria registro adicional de rollback: `AuditLog { EntityType = "Rollback_Ativo", EntityId, OperationType = Rollback, UserId, Timestamp = UtcNow, Changes = [{ FieldName: "RollbackReason", NewValue: reason }, { FieldName: "RollbackTargetTimestamp", NewValue: targetTimestamp }] }` |
| 23 | - | Persiste rollback log: `await _context.AuditLogs.AddAsync(rollbackLog)` |
| 24 | - | Commit transação: `await transaction.CommitAsync()` |
| 25 | - | Envia notificação para DPO e gestor superior: `EmailService.SendAsync("compliance@empresa.com", "Rollback executado", templateRollback)` |
| 26 | - | Retorna HTTP 200 com RollbackResultDto: `{ success: true, entityType, entityId, rolledBackTo: targetTimestamp, message: "Entidade restaurada ao estado de 27/12/2025 10:00:00" }` |
| 27 | - | Frontend fecha modal, exibe toast de sucesso: "Entidade restaurada com sucesso. Operação registrada em auditoria.", recarrega timeline |

### 5. Fluxos Alternativos

**FA01 - Rollback de soft delete (reverter deleção):**
- Passo 2: Gestor identifica que entidade foi deletada (DeletedAt preenchido)
- Passo 12: Estado alvo tem DeletedAt = null (entidade ativa)
- Passo 19: Restaura DeletedAt = null, DeletedBy = null, DeletionReason = null
- Entidade volta a ser visível no sistema

**FA02 - Rollback em cascata (múltiplas entidades relacionadas):**
- Passo 2: Gestor seleciona "Rollback em Cascata" (checkbox)
- Passo 13-16: Sistema identifica entidades dependentes que também precisam ser restauradas
- Passo 17-24: Transação inclui rollback de Ativo + Atribuições + Consumidor (se necessário)
- Todos rollbacks registrados com MESMO CorrelationId

**FA03 - Rollback requer aprovação adicional (valor > R$ 10.000):**
- Passo 8: Se entidade é Fatura com Valor > R$ 10.000 → Backend verifica se há ApprovalId no body
- Se ApprovalId ausente → Retorna HTTP 403: "Rollback de fatura acima de R$ 10.000 requer aprovação do Diretor Financeiro"
- Sistema envia solicitação de aprovação via workflow, aguarda

### 6. Exceções

**EX01 - Estado alvo não encontrado:**
- Passo 11: Se nenhum AuditLog existe para o timestamp especificado → Retorna HTTP 404
- Frontend exibe erro: "Estado não encontrado. Timestamp pode estar incorreto."

**EX02 - Violação de integridade referencial:**
- Passo 14: FK (ConsumidorId) referencia registro que foi deletado → Retorna HTTP 400
- Frontend exibe modal com instruções: "Restaure o Consumidor 'João Silva' antes de restaurar este Ativo."

**EX03 - Transação falha durante rollback:**
- Passo 24: Se CommitAsync lança exceção (deadlock, constraint violation) → Captura exceção
- Rollback automático: `await transaction.RollbackAsync()`
- Retorna HTTP 500 com ErrorMessage: ex.Message
- Frontend exibe erro: "Falha ao restaurar entidade. Tente novamente."

### 7. Pós-condições

- Entidade restaurada para estado do timestamp alvo
- Registro de rollback criado em AuditLog tipo "Rollback"
- Integridade referencial mantida (nenhuma FK quebrada)
- Notificações enviadas para compliance e gestores
- Timeline atualizada mostrando operação de rollback como última entrada
- Operação reversível (pode fazer rollback do rollback se necessário)

### 8. Regras de Negócio Aplicáveis

- RN-AUD-096-10: Rollback com Validação de Integridade Referencial
- RN-AUD-096-03: Imutabilidade de Registros de Auditoria (rollback também é registrado)
- RN-004-AUD-01: Auditoria de todas as operações

---

## UC04: Detectar Anomalias em Padrões de Mudança e Gerar Alertas

### 1. Descrição

Este caso de uso permite ao sistema analisar automaticamente padrões de mudança (via Hangfire job diário) para detectar comportamentos anômalos: mudanças fora do horário comercial, volume excessivo de alterações por usuário, mudanças suspeitas em dados sensíveis.

### 2. Atores

- Sistema (job Hangfire executado diariamente)
- Gerente de Segurança (recebe alertas de anomalias)

### 3. Pré-condições

- Job Hangfire configurado: `RecurringJob.AddOrUpdate<AnomalyDetectionJob>(x => x.DetectChangeAnomaliesAsync(), Cron.Daily(4))` (executa às 04:00)
- Tabela AuditLog com histórico mínimo de 30 dias
- Tabela AnomalyAlert criada no banco de dados
- Dashboard de anomalias acessível em /admin/audit/anomalies

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job Hangfire dispara execução às 04:00 UTC: `AnomalyDetectionJob.DetectChangeAnomaliesAsync()` |
| 2 | - | Define período de análise: `startDate = DateTime.UtcNow.AddDays(-1)` (últimas 24 horas), `endDate = DateTime.UtcNow` |
| 3 | - | Recupera logs do período: `var logs = await _context.AuditLogs.Where(a => a.Timestamp >= startDate && a.Timestamp <= endDate && a.ClienteId == clienteId).ToListAsync()` |
| 4 | - | **Anomalia 1: Mudanças fora do horário comercial** - Conta logs com Timestamp.Hour < 6 ou > 22: `var afterHoursCount = logs.Count(a => a.Timestamp.Hour < 6 || a.Timestamp.Hour > 22)` |
| 5 | - | Calcula percentual: `percentualForaHorario = (afterHoursCount / (double)logs.Count) * 100` |
| 6 | - | Se percentualForaHorario > 10% → Cria AnomalyAlert: `{ Type = "AnomalousAccessTime", Severity = Medium, Message = "{afterHoursCount} mudanças fora do horário comercial (6-22h) - {percentualForaHorario:F1}%", DetectedAt = UtcNow, ClienteId }` |
| 7 | - | **Anomalia 2: Usuário com volume excessivo** - Agrupa logs por usuário: `var userGroups = logs.GroupBy(a => a.UserId).Select(g => new { UserId = g.Key, Count = g.Count() })` |
| 8 | - | Calcula média de mudanças por usuário: `averageChanges = logs.Count / (double)logs.Select(a => a.UserId).Distinct().Count()` |
| 9 | - | Identifica usuários suspeitos (> 3x a média): `var suspiciousUsers = userGroups.Where(u => u.Count > averageChanges * 3)` |
| 10 | - | Para cada usuário suspeito: Cria AnomalyAlert: `{ Type = "HighActivity", Severity = Low, Message = "Usuário {username} com {count} mudanças (média: {averageChanges:F1})", DetectedAt = UtcNow, UserId, ClienteId }` |
| 11 | - | **Anomalia 3: Múltiplas deleções** - Conta logs com OperationType = Delete: `deleteCount = logs.Count(a => a.OperationType == OperationType.Delete)` |
| 12 | - | Se deleteCount > 50 (threshold configurável) → Cria AnomalyAlert: `{ Type = "MassiveDeletion", Severity = High, Message = "{deleteCount} entidades deletadas nas últimas 24h", DetectedAt = UtcNow, ClienteId }` |
| 13 | - | **Anomalia 4: Mudanças em dados sensíveis LGPD** - Filtra logs com Changes.IsSensitive = true: `var sensitiveLogs = logs.Where(a => a.Changes.Any(c => c.IsSensitive))` |
| 14 | - | Se sensitiveLogs.Count > 20 (threshold) → Cria AnomalyAlert: `{ Type = "SensitiveDataChanges", Severity = High, Message = "{count} alterações em dados sensíveis LGPD detectadas", DetectedAt = UtcNow, ClienteId }` |
| 15 | - | **Anomalia 5: Rollbacks frequentes** - Conta logs com OperationType = Rollback: `rollbackCount = logs.Count(a => a.OperationType == OperationType.Rollback)` |
| 16 | - | Se rollbackCount > 5 (threshold) → Cria AnomalyAlert: `{ Type = "FrequentRollbacks", Severity = Medium, Message = "{rollbackCount} rollbacks executados nas últimas 24h - possível instabilidade", DetectedAt = UtcNow, ClienteId }` |
| 17 | - | Persiste alertas no banco: `await _context.AnomalyAlerts.AddRangeAsync(alerts)`, `await _context.SaveChangesAsync()` |
| 18 | - | Para cada alerta com Severity = High → Envia notificação: `await _notificationService.SendAsync("security@empresa.com", $"Alerta de Anomalia: {alert.Type}", templateAlert)` |
| 19 | - | Para cada alerta com Severity = High → Envia para Azure Sentinel: `await _sentinelService.SendEventAsync("ANOMALY_DETECTED", alert)` |
| 20 | - | Atualiza dashboard de anomalias: SignalR broadcast para grupo "AnomalyDashboard": `await _hubContext.Clients.Group("AnomalyDashboard").SendAsync("NewAnomalyDetected", alert)` |
| 21 | - | Registra execução do job: `Logger.LogInformation("Anomaly detection completed: {totalLogs} logs analyzed, {totalAlerts} anomalies detected", logs.Count, alerts.Count)` |

### 5. Fluxos Alternativos

**FA01 - Nenhuma anomalia detectada:**
- Passo 6, 10, 12, 14, 16: Todos thresholds não atingidos → Lista de alerts permanece vazia
- Passo 17: Nenhum registro criado em AnomalyAlerts
- Passo 21: Log registra: "Anomaly detection completed: {totalLogs} logs analyzed, 0 anomalies detected"

**FA02 - Anomalia de mesmo IP alterando múltiplas entidades:**
- Adicional ao fluxo: Agrupa logs por IpAddress: `var ipGroups = logs.GroupBy(a => a.IpAddress).Select(g => new { IpAddress = g.Key, Count = g.Count(), DistinctEntities = g.Select(a => a.EntityId).Distinct().Count() })`
- Se DistinctEntities > 100 em 1 hora de mesmo IP → AnomalyAlert: `{ Type = "SuspiciousIpActivity", Severity = High }`

**FA03 - Dashboard exibe anomalias em tempo real:**
- Gerente de Segurança acessa /admin/audit/anomalies
- Frontend subscribed to SignalR Hub: `hubConnection.on("NewAnomalyDetected", (alert) => addAlertToTable(alert))`
- Passo 20: Novo alerta aparece instantaneamente no dashboard com badge vermelho (High), amarelo (Medium), azul (Low)

### 6. Exceções

**EX01 - Histórico insuficiente para análise:**
- Passo 3: Se logs.Count < 10 (período muito recente ou baixo volume) → Pula análise
- Passo 21: Log registra: "Insufficient data for anomaly detection: {logs.Count} logs (minimum 10 required)"

**EX02 - Falha ao enviar notificação:**
- Passo 18: Se SendAsync falha (SMTP indisponível) → Captura exceção, registra warning
- Continua processamento, alerta persiste no banco mas email não enviado
- Retry agendado para próxima execução do job

**EX03 - Threshold customizado por tenant:**
- Passo 6, 12, 14: Se ClienteId tem configuração customizada em tabela AnomalyThresholds → Usa valores específicos
- Exemplo: Tenant "Chipak" tem threshold afterHours = 5% (mais restritivo), Tenant "Demo" tem 15% (mais permissivo)

### 7. Pós-condições

- Anomalias detectadas registradas em AnomalyAlerts
- Notificações enviadas para gerente de segurança (email + dashboard)
- Eventos críticos enviados para Azure Sentinel (SIEM)
- Dashboard atualizado em tempo real via SignalR
- Logs de execução do job registrados para auditoria
- Thresholds podem ser ajustados dinamicamente por tenant

### 8. Regras de Negócio Aplicáveis

- RN-AUD-096-12: Dashboard de Mudanças com Alertas de Anomalias
- RN-SEC-095-10: Alertas Automáticos em Tempo Real (referência RF095)

---

## UC05: Exportar Relatório de Auditoria Parametrizado com Agregações

### 1. Descrição

Este caso de uso permite ao auditor gerar relatórios parametrizados de auditoria com agregações por período, usuário, entidade, tipo de operação, e exportar em múltiplos formatos (CSV, Excel, JSON, PDF) para análise ou compliance.

### 2. Atores

- Auditor de Compliance (gera relatório)
- Sistema (consulta AuditLog, agrega dados, gera arquivo)

### 3. Pré-condições

- Usuário autenticado com permissão: `audit:report` e `audit:export`
- Tabela AuditLog com histórico de mudanças
- Multi-tenancy ativo (relatórios isolados por ClienteId)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Auditor acessa tela de relatórios: /admin/audit/reports | - |
| 2 | Auditor preenche formulário de filtros: Período (DatePicker: 01/12/2025 - 31/12/2025), Tipo de Entidade (dropdown: Todos/Ativo/Consumidor/Fatura), Usuário (autocomplete: opcional), Tipo de Operação (checkboxes: Create/Update/Delete) | - |
| 3 | Auditor seleciona agregações desejadas (checkboxes): Volume por dia, Mudanças por usuário, Mudanças por entidade, Mudanças por tipo de operação | - |
| 4 | Auditor clica em "Gerar Relatório" | - |
| 5 | - | Frontend envia GET /api/audit/reports?startDate=2025-12-01&endDate=2025-12-31&entityType=Ativo&operationType=Update&aggregations=volumeByDay,changesByUser,changesByEntity |
| 6 | - | Backend valida permissão: `audit:report` → Se falha retorna HTTP 403 |
| 7 | - | Backend constrói query base: `var query = _context.AuditLogs.Where(a => a.Timestamp >= startDate && a.Timestamp <= endDate && a.ClienteId == clienteId)` |
| 8 | - | Aplica filtros opcionais: Se entityType != null → `query = query.Where(a => a.EntityType == entityType)`, Se operationType != null → `query = query.Where(a => a.OperationType == operationType)`, Se userName != null → `query = query.Where(a => a.Username.Contains(userName))` |
| 9 | - | **Agregação 1: Volume por dia** - `var volumeByDay = await query.GroupBy(a => a.Timestamp.Date).Select(g => new VolumeMetricDto { Period = g.Key, Count = g.Count() }).OrderBy(v => v.Period).ToListAsync()` |
| 10 | - | **Agregação 2: Mudanças por usuário** - `var changesByUser = await query.GroupBy(a => a.Username).Select(g => new UserMetricDto { Username = g.Key, CreateCount = g.Count(a => a.OperationType == Create), UpdateCount = g.Count(a => a.OperationType == Update), DeleteCount = g.Count(a => a.OperationType == Delete), TotalCount = g.Count() }).OrderByDescending(u => u.TotalCount).ToListAsync()` |
| 11 | - | **Agregação 3: Mudanças por entidade** - `var changesByEntity = await query.GroupBy(a => a.EntityType).Select(g => new EntityMetricDto { EntityType = g.Key, TotalChanges = g.Count(), AffectedRecords = g.Select(a => a.EntityId).Distinct().Count() }).OrderByDescending(e => e.TotalChanges).ToListAsync()` |
| 12 | - | **Agregação 4: Mudanças por tipo de operação** - `var changesByOperation = await query.GroupBy(a => a.OperationType).Select(g => new { OperationType = g.Key, Count = g.Count() }).ToListAsync()` |
| 13 | - | Calcula totais: `totalChanges = query.Count()`, `totalUsers = query.Select(a => a.UserId).Distinct().Count()`, `totalEntities = query.Select(a => a.EntityType).Distinct().Count()` |
| 14 | - | Retorna HTTP 200 com AuditReportDto: `{ period: { from: startDate, to: endDate }, volumeByDay, changesByUser, changesByEntity, changesByOperation, totals: { totalChanges, totalUsers, totalEntities } }` |
| 15 | - | Frontend renderiza relatório em dashboard interativo: Cards de totais (Total Mudanças, Total Usuários, Total Entidades), Gráfico de linha (Volume por Dia) usando Chart.js, Tabela Top 10 Usuários (ordenado por TotalCount), Tabela Top 10 Entidades, Gráfico de pizza (Mudanças por Tipo de Operação) |
| 16 | Auditor analisa relatório visualmente | - |
| 17 | Auditor clica em "Exportar" e seleciona formato: CSV | - |
| 18 | - | Frontend envia GET /api/audit/reports?startDate=2025-12-01&endDate=2025-12-31&format=csv |
| 19 | - | Backend gera arquivo CSV: Seção 1 (headers): "Período,Total Mudanças,Total Usuários,Total Entidades", linha com totais; Seção 2: "Volume por Dia,Data,Quantidade", uma linha por dia; Seção 3: "Mudanças por Usuário,Usuário,Criações,Atualizações,Deleções,Total", uma linha por usuário |
| 20 | - | Retorna FileStreamResult com Content-Type: text/csv, Content-Disposition: attachment; filename="audit_report_20251201-20251231.csv" |
| 21 | - | Frontend baixa arquivo automaticamente |
| 22 | - | Backend registra exportação em AuditLog: `new AuditLog { EntityType = "AuditReport", OperationType = Export, UserId, Timestamp = UtcNow, Changes = [{ FieldName: "ReportFilters", NewValue: JSON.stringify(filters) }] }` |

### 5. Fluxos Alternativos

**FA01 - Exportar em formato Excel com gráficos:**
- Passo 17: Auditor seleciona formato: Excel
- Passo 19: Backend usa ClosedXML library para gerar .xlsx com: Aba 1 "Resumo" (cards de totais), Aba 2 "Volume por Dia" (tabela + gráfico de linha), Aba 3 "Por Usuário" (tabela + gráfico de barras), Aba 4 "Por Entidade" (tabela), Headers formatados (negrito, cor de fundo), Auto-ajuste de colunas
- Passo 20: Download de arquivo .xlsx interativo

**FA02 - Exportar em formato PDF para auditoria externa:**
- Passo 17: Auditor seleciona formato: PDF
- Passo 19: Backend usa iTextSharp library: Capa com logo empresa, período do relatório, data geração; Índice automático; Seções com títulos formatados; Tabelas com bordas; Gráficos renderizados como imagens (Chart.js headless); Rodapé com numeração de páginas
- Passo 20: Download de PDF formatado profissionalmente

**FA03 - Agendar relatório recorrente mensal:**
- Passo 4: Auditor marca checkbox "Agendar Recorrência" e seleciona "Mensal (dia 1)"
- Sistema cria job Hangfire: `RecurringJob.AddOrUpdate<GenerateScheduledReportJob>(x => x.ExecuteAsync(reportConfig), Cron.Monthly(1, 8))` (dia 1 às 08:00)
- Job executa relatório automaticamente, envia por email para lista de destinatários configurada

### 6. Exceções

**EX01 - Período muito longo (> 1 ano):**
- Passo 7: Se (endDate - startDate).TotalDays > 365 → Retorna HTTP 400 com mensagem: "Período máximo para relatório é 1 ano. Use exportação em lote para períodos maiores."
- Frontend exibe erro ao usuário

**EX02 - Nenhuma mudança no período selecionado:**
- Passo 7: Query retorna 0 logs → totalChanges = 0
- Passo 14: Retorna relatório com totais zerados
- Passo 15: Frontend exibe empty state: "Nenhuma mudança encontrada no período selecionado"

**EX03 - Geração de arquivo falha (memória insuficiente):**
- Passo 19: Se dataset muito grande (>1M registros) e geração Excel falha com OutOfMemoryException → Captura exceção
- Retorna HTTP 507 com mensagem: "Dataset muito grande para exportação direta. Use filtros mais restritivos ou exporte em lote."
- Frontend sugere: "Reduza o período ou filtre por entidade específica"

### 7. Pós-condições

- Relatório gerado com agregações solicitadas
- Arquivo exportado disponível para download (CSV/Excel/JSON/PDF)
- Exportação registrada em AuditLog para rastreabilidade
- Dados visualizados em dashboard interativo
- Se agendado: Job recorrente criado para próximas execuções

### 8. Regras de Negócio Aplicáveis

- RN-AUD-096-11: Relatórios Parametrizáveis com Agregações
- RN-AUD-096-14: Exportação de Trilha Auditória para Análise Forense
- RN-AUD-096-07: Retenção de Dados de Auditoria conforme LGPD e SOX

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code (Anthropic)
**Próximo**: Criar user-stories.yaml para RF096

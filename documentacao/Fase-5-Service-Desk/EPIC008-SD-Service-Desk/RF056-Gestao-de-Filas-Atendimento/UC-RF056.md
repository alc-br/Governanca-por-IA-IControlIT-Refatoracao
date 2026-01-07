# Casos de Uso - RF056 - Gestão de Filas de Atendimento

**RF:** RF-056 — Gestão de Filas de Atendimento
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

## Índice | 5 UCs
UC00: Listar Filas | UC01: Distribuir Solicitação | UC02: Alterar Status Atendente | UC03: Transferir Solicitação | UC04: Visualizar Métricas

## Resumo

**UC00: Listar Filas de Atendimento**
- **Ator:** Usuario Autenticado
- **Fluxo:** Consultar filas filtradas por categoria de serviço (Infraestrutura, Aplicações, Service Desk, Suporte Técnico, Segurança)
- **Regras Cobertas:** RN-RF056-009 (Filas por Categoria)
- **Permissões:** SD.FILAS.VIEW_ANY (visualizar todas), SD.FILAS.VIEW (visualizar específica)
- **Resultado:** Grid paginado com Nome, Categoria, Status, Qtd_Solicitacoes, Tempo_Medio_Resposta

**UC01: Distribuir Solicitação Automaticamente**
- **Ator:** Sistema (Job Hangfire)
- **Gatilho:** Nova solicitação criada OU a cada 5 minutos (job agendado)
- **Algoritmo de Distribuição:**
  1. Priorização tripla: (1) Prioridade → (2) % SLA consumido → (3) Tempo de espera
  2. Routing por Skills: validar skill do atendente corresponde à categoria
  3. Balanceamento de Carga: selecionar atendente DISPONÍVEL com MIN(CargaAtual)
  4. Escalação Automática: solicitações >30 min na fila → prioridade aumentada
  5. Limite de 5 solicitações simultâneas por atendente
  6. Priorização de VIPs: CEO/Diretores recebem prioridade CRÍTICA automaticamente
- **Regras Cobertas:** RN-RF056-001, 002, 003, 004, 005, 009, 010 (7 regras)
- **Permissões:** Sistema (automático, sem intervenção manual)
- **Resultado:** Solicitação atribuída a atendente qualificado e disponível

**UC02: Alterar Status de Disponibilidade do Atendente**
- **Ator:** Atendente OU Supervisor
- **Fluxo:**
  - **FP:** Atendente altera próprio status (DISPONÍVEL → PAUSA → AUSENTE)
  - **FA-01:** Pausas automáticas em horários configurados (almoço, café)
  - **FA-02:** Redistribuição quando status vira AUSENTE (solicitações transferidas automaticamente)
- **Regras Cobertas:** RN-RF056-006, 007, 008 (3 regras)
- **Permissões:** SD.ATENDENTE.STATUS (próprio), SD.ATENDENTE.MANAGE_STATUS (supervisor)
- **Validações:**
  - DISPONÍVEL → OCUPADO (automático ao atingir 5 solicitações)
  - AUSENTE → Redistribuir solicitações abertas
- **Resultado:** Status atualizado + histórico de mudanças registrado

**UC03: Transferir Solicitação Entre Atendentes**
- **Ator:** Atendente OU Supervisor
- **Fluxo:**
  - Selecionar solicitação EM_ATENDIMENTO
  - Escolher atendente destino (lista filtrada por skill compatível)
  - Informar motivo da transferência
  - Sistema valida skill e limite de carga do destino
- **Regras Cobertas:** RN-RF056-002 (Routing Skills), 005 (Limite 5), 011 (Transferência Manual)
- **Permissões:** SD.FILAS.TRANSFER
- **Validações:**
  - Atendente destino DEVE ter skill adequada (HTTP 400 se inválido)
  - Atendente destino NÃO pode estar com 5 solicitações (HTTP 400)
- **Resultado:** Solicitação reatribuída + registro em TransferenciaSolicitacao

**UC04: Visualizar Métricas em Tempo Real**
- **Ator:** Gestor/Supervisor
- **Fluxo:**
  - Dashboard atualizado a cada 30s via SignalR
  - KPIs: Total solicitações por fila, Atendentes DISPONÍVEL/OCUPADO/PAUSA, Tempo médio espera, % SLA cumprido
  - Filtros: Período, Fila, Atendente
  - Gráficos: Tendência de abertura, Distribuição por prioridade, Ranking de produtividade
- **Regras Cobertas:**
  - RN-RF056-012 (Métricas em Tempo Real)
  - RN-RF056-013 (Fila de Retorno Follow-up)
  - RN-RF056-014 (SLA Pausado em Pendência Externa)
  - RN-RF056-015 (Relatório de Produtividade)
- **Permissões:** SD.FILAS.METRICS
- **Tecnologia:** SignalR Hub (QueueMetricsHub)
- **Resultado:** Dashboard interativo com métricas consolidadas + exportação em PDF/Excel

## Integrações Obrigatórias

**Central de Funcionalidades:**
- RF-FILAS-001: Listar Filas de Atendimento
- RF-FILAS-002: Distribuir Solicitação Automaticamente
- RF-FILAS-003: Alterar Status de Atendente
- RF-FILAS-004: Transferir Solicitação
- RF-FILAS-005: Visualizar Métricas em Tempo Real

**i18n:**
- `sd.filas.*` (todas as chaves de tradução de filas)
- `sd.atendente.status.*` (estados de disponibilidade)
- `sd.metricas.*` (dashboard e KPIs)

**Auditoria:**
- CREATE (criação de fila)
- UPDATE (alteração de configuração)
- DISTRIBUICAO (atribuição automática)
- TRANSFER (transferência manual)
- STATUS_CHANGE (mudança de status atendente)

**RBAC (Permissões):**
- `SD.FILAS.VIEW_ANY` - Visualizar todas as filas
- `SD.FILAS.VIEW` - Visualizar fila específica
- `SD.FILAS.MANAGE` - Gerenciar configuração de filas
- `SD.FILAS.TRANSFER` - Transferir solicitações entre atendentes
- `SD.FILAS.ESCALATE` - Escalar solicitações manualmente
- `SD.FILAS.METRICS` - Visualizar métricas e relatórios
- `SD.ATENDENTE.STATUS` - Alterar próprio status
- `SD.ATENDENTE.MANAGE_STATUS` - Gerenciar status de outros (supervisor)

**SignalR:**
- Hub: `QueueMetricsHub`
- Events: `QueueUpdated`, `AttendantStatusChanged`, `RequestAssigned`
- Frequência: 30s

**Hangfire:**
- Job: `ProcessQueueDistributionJob` (a cada 5 minutos)
- Job: `AutoPauseAttendantsJob` (horários configurados)
- Job: `EscalateOldRequestsJob` (verifica solicitações >30 min)

**Domain Events:**
- `SolicitacaoCriadaEvent` (RF055 → RF056)
- `SolicitacaoDistribuidaEvent`
- `SolicitacaoTransferidaEvent`
- `AtendenteStatusAlteradoEvent`

## Histórico
| Versão | Data | Descrição |
|--------|------|-----------|
| 2.0 | 2025-12-31 | Migração v1.0 → v2.0 - Alinhamento com RF056.yaml (5 UCs cobrindo 15 regras) |
| 1.0 | 2025-12-18 | Versão inicial (9 UCs CRUD - depreciado) |

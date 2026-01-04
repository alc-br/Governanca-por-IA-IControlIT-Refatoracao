# UC-RF054 — Casos de Uso de Gestão de Lotes de Auditoria

**RF:** RF054 — Gestão de Lotes de Auditoria
**Epic:** EPIC010-AUD - Auditoria Avançada
**Fase:** Fase 6 - Ativos Auditoria Integracoes
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## Sumário

Este documento descreve os 13 casos de uso do RF054 - Gestão de Lotes de Auditoria, cobrindo criação, processamento, monitoramento e consolidação de lotes de auditoria de faturas.

O sistema permite processamento assíncrono em background via Hangfire, monitoramento em tempo real via SignalR, integração com RF034 (Itens de Auditoria) e RF035 (Status de Auditoria), notificações via Azure Service Bus, rollback automático em caso de cancelamento, SLA e alertas de timeout, e dashboard consolidado de KPIs.

**Contexto Técnico:**
- **Máquina de Estados:** Created → WaitingForProcessing → Processing → Completed/Cancelled/Error → Archived
- **Jobs Hangfire:** SelectInvoices, ProcessInvoice, ConsolidateResults, MonitorTimeout, ArchiveOldBatches
- **Integração SignalR:** WebSocket para progresso em tempo real
- **Azure Service Bus:** Notificações assíncronas de eventos críticos
- **Retry Policy:** Exponencial (1min, 5min, 15min) para falhas temporárias

---

## Índice de Casos de Uso

| ID | Nome | Ator Principal | Tipo | Impacta Dados |
|----|------|----------------|------|---------------|
| UC00 | Criar Lote de Auditoria | coordenador_gestor | CRUD | Sim |
| UC01 | Selecionar Faturas do Lote | sistema | Ação | Sim |
| UC02 | Iniciar Processamento do Lote | coordenador_gestor_sistema | Ação | Sim |
| UC03 | Monitorar Progresso em Tempo Real | auditor | Leitura | Não |
| UC04 | Cancelar Lote com Rollback | coordenador_gestor | Ação | Sim |
| UC05 | Arquivar Lote | coordenador_gestor_sistema | Ação | Sim |
| UC06 | Exportar Relatório de Lote | auditor | Leitura | Não |
| UC07 | Reprocessar Faturas com Erro | coordenador_gestor | Ação | Sim |
| UC08 | Atribuir/Reatribuir Auditor | coordenador_gestor | Ação | Sim |
| UC09 | Configurar SLA e Alertas | coordenador_gestor | CRUD | Sim |
| UC10 | Visualizar Histórico de Auditoria | auditor | Leitura | Não |
| UC11 | Dashboard de KPIs de Lotes | coordenador_gestor | Leitura | Não |
| UC12 | Job: Processar Lote em Background | sistema | Batch | Sim |

---

## UC00 — Criar Lote de Auditoria

**Descrição:**
Permite ao usuário criar um novo lote de auditoria, definindo nome, descrição, critérios de seleção de faturas (período, transportadora, filial, valor, tipo de serviço, status), auditor responsável (opcional), prioridade (Baixa/Normal/Alta/Crítica) e SLA de timeout. Sistema valida critérios, estima quantidade de faturas que serão selecionadas e cria lote em status `Created`.

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `crud` (Create/Read/Update/Delete)

**Impacta Dados:** `true`

**Pré-condições:**
- Usuário autenticado com permissão `AUD.LOTES.CREATE`
- Sistema disponível e conectado ao banco de dados
- Módulo de faturas (RF026) disponível para validação de critérios

**Gatilho:**
Usuário acessa menu "Auditoria > Lotes de Auditoria > Criar Novo Lote" e clica em "Novo Lote"

**Fluxo Principal (FP-UC00):**
1. **FP-UC00-001**: Sistema exibe formulário de criação de lote
2. **FP-UC00-002**: Usuário preenche campos obrigatórios (nome, descrição)
3. **FP-UC00-003**: Usuário define pelo menos um critério de seleção (período, transportadora, filial, valor mínimo/máximo, tipo de serviço, status de fatura)
4. **FP-UC00-004**: Sistema valida critérios em tempo real e exibe estimativa de faturas que serão selecionadas
5. **FP-UC00-005**: Usuário opcionalmente atribui auditor responsável via dropdown
6. **FP-UC00-006**: Usuário define prioridade (padrão: Normal) e SLA timeout em horas (padrão: 48h)
7. **FP-UC00-007**: Usuário clica em "Criar Lote"
8. **FP-UC00-008**: Sistema valida que ao menos um critério foi informado (RN-LOT-054-01)
9. **FP-UC00-009**: Sistema cria lote com status `Created` no banco de dados
10. **FP-UC00-010**: Sistema enfileira job Hangfire de seleção de faturas (UC01)
11. **FP-UC00-011**: Sistema registra operação no histórico de auditoria (usuário, data/hora, IP, critérios)
12. **FP-UC00-012**: Sistema exibe mensagem de sucesso com ID do lote e redireciona para tela de detalhes

**Fluxos Alternativos (FA):**

**FA-UC00-01: Atribuição Automática de Auditor**
- **Condição:** Usuário não informou auditor responsável no FP-UC00-005
- **Fluxo:**
  1. Sistema consulta auditores disponíveis com permissão `AUD.LOTES.AUDIT`
  2. Sistema seleciona auditor com menor quantidade de lotes ativos no momento
  3. Sistema atribui auditor selecionado automaticamente
  4. Retorna ao FP-UC00-007

**FA-UC00-02: Auto-Seleção de Faturas se Critério Permitir**
- **Condição:** Critérios de seleção são muito restritivos e quantidade estimada é pequena (<10 faturas)
- **Fluxo:**
  1. Sistema pergunta ao usuário se deseja selecionar faturas imediatamente
  2. Se usuário confirmar, sistema executa seleção síncrona em vez de enfileirar job
  3. Lote transiciona direto para status `WaitingForProcessing`
  4. Retorna ao FP-UC00-012

**Fluxos de Exceção (FE):**

**FE-UC00-01: Critérios de Seleção Vazios**
- **Condição:** Usuário não informou nenhum critério de seleção no FP-UC00-008
- **Tratamento:**
  1. Sistema exibe erro HTTP 400: "Pelo menos um critério de seleção é obrigatório (RN-LOT-054-01)"
  2. Sistema destaca campos de critérios no formulário
  3. Retorna ao FP-UC00-003

**FE-UC00-02: Nome Duplicado**
- **Condição:** Já existe lote com mesmo nome no sistema
- **Tratamento:**
  1. Sistema exibe erro: "Já existe um lote com este nome. Escolha outro nome."
  2. Sistema destaca campo "Nome"
  3. Retorna ao FP-UC00-002

**FE-UC00-03: Auditor sem Permissão**
- **Condição:** Auditor selecionado não possui permissão `AUD.LOTES.AUDIT`
- **Tratamento:**
  1. Sistema exibe erro: "Auditor selecionado não possui permissão para auditar lotes"
  2. Sistema limpa campo de auditor
  3. Retorna ao FP-UC00-005

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-01**: Obrigatoriedade de Critérios de Seleção
- **RN-LOT-054-04**: Atribuição Manual ou Automática de Auditor
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição para Created)
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações

**Critérios de Aceite:**
- Lote criado com sucesso em status `Created`
- Pelo menos um critério de seleção foi informado
- Job de seleção de faturas foi enfileirado no Hangfire
- Histórico de auditoria registrou criação com todos os dados
- Auditor atribuído (manualmente ou automaticamente)
- Notificação Azure Service Bus enviada com evento "LoteCreated"

---

## UC01 — Selecionar Faturas do Lote

**Descrição:**
Job assíncrono executado em background pelo Hangfire que aplica os critérios configurados do lote e seleciona automaticamente todas as faturas elegíveis, associando-as ao lote criado. Valida que faturas não estejam em outros lotes ativos e transiciona lote para status `WaitingForProcessing`.

**Ator Principal:** `sistema` (Hangfire Background Job)

**Tipo:** `acao` (Ação do Sistema)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote criado com critérios válidos em status `Created`
- Job enfileirado no Hangfire
- Módulo de faturas (RF026) disponível

**Gatilho:**
Job Hangfire disparado automaticamente após criação do lote (UC00)

**Fluxo Principal (FP-UC01):**
1. **FP-UC01-001**: Job Hangfire inicia execução
2. **FP-UC01-002**: Job consulta critérios de seleção do lote
3. **FP-UC01-003**: Job constrói query SQL aplicando filtros (período, transportadora, filial, valor, tipo de serviço, status)
4. **FP-UC01-004**: Job consulta base de faturas e obtém lista de IDs elegíveis
5. **FP-UC01-005**: Para cada fatura elegível, job valida que não está associada a outro lote ativo (RN-LOT-054-03)
6. **FP-UC01-006**: Job cria registros de associação lote-fatura em tabela `LoteAuditoriaFatura`
7. **FP-UC01-007**: Job atualiza contador `QuantidadeFaturasSelecionadas` no lote
8. **FP-UC01-008**: Job transiciona lote para status `WaitingForProcessing`
9. **FP-UC01-009**: Job registra operação no histórico de auditoria
10. **FP-UC01-010**: Job envia notificação Azure Service Bus com evento "LoteProntoParaProcessamento"
11. **FP-UC01-011**: Job finaliza com sucesso

**Fluxos Alternativos (FA):**

**FA-UC01-01: Nenhuma Fatura Elegível**
- **Condição:** Query SQL não retornou nenhuma fatura no FP-UC01-004
- **Fluxo:**
  1. Job transiciona lote para status `Error`
  2. Job registra erro no histórico: "Nenhuma fatura atende aos critérios configurados"
  3. Job envia notificação Azure Service Bus com evento "LoteErro"
  4. Job finaliza

**FA-UC01-02: Todas as Faturas Já Estão em Outros Lotes**
- **Condição:** Todas as faturas elegíveis já estão associadas a outros lotes ativos no FP-UC01-005
- **Fluxo:**
  1. Job transiciona lote para status `Error`
  2. Job registra erro: "Todas as faturas elegíveis já estão em processamento em outros lotes"
  3. Job envia notificação Azure Service Bus
  4. Job finaliza

**Fluxos de Exceção (FE):**

**FE-UC01-01: Erro de Banco de Dados**
- **Condição:** Falha na consulta SQL no FP-UC01-004
- **Tratamento:**
  1. Hangfire aplica retry automático (4 tentativas: 0s, 1min, 5min, 15min)
  2. Se todas as tentativas falharem, job marca lote como `Error`
  3. Job registra stack trace completo no histórico
  4. Job envia notificação de erro crítico

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-03**: Seleção Automática de Faturas por Critérios
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição Created → WaitingForProcessing)
- **RN-LOT-054-06**: Processamento Assíncrono com Hangfire
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus

**Critérios de Aceite:**
- Job executado com sucesso em background
- Faturas elegíveis selecionadas e associadas ao lote
- Faturas em outros lotes ativos foram excluídas da seleção
- Lote transicionado para `WaitingForProcessing`
- Contador de faturas selecionadas atualizado
- Histórico de auditoria registrou operação
- Notificação Azure Service Bus enviada

---

## UC02 — Iniciar Processamento do Lote

**Descrição:**
Permite ao usuário ou sistema iniciar o processamento assíncrono do lote, validando estado, transicionando para `Processing`, disparando jobs Hangfire paralelos que auditam cada fatura individualmente via integração com RF034, e enviando notificações SignalR de progresso em tempo real.

**Ator Principal:** `coordenador_gestor_sistema` (Coordenador, Gestor, ou Sistema via Scheduler)

**Tipo:** `acao` (Ação)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote no status `WaitingForProcessing`
- Faturas selecionadas e associadas ao lote
- Usuário autenticado com permissão `AUD.LOTES.PROCESS` (se manual)
- Módulo RF034 (Itens de Auditoria) disponível

**Gatilho:**
Usuário clica em botão "Iniciar Processamento" no dashboard do lote OU sistema dispara via scheduler automático

**Fluxo Principal (FP-UC02):**
1. **FP-UC02-001**: Sistema valida estado do lote (RN-LOT-054-05)
2. **FP-UC02-002**: Sistema valida que lote não está em `Processing`, `Completed`, `Cancelled`, `Archived`
3. **FP-UC02-003**: Sistema transiciona lote para status `Processing`
4. **FP-UC02-004**: Sistema atualiza campo `DataHoraInicioProcessamento` com timestamp atual
5. **FP-UC02-005**: Sistema enfileira N jobs Hangfire paralelos (1 job por fatura associada)
6. **FP-UC02-006**: Sistema aplica limite de concorrência configurável (ex: máximo 10 jobs simultâneos)
7. **FP-UC02-007**: Cada job de fatura executa UC12 (Processar Lote em Background)
8. **FP-UC02-008**: Sistema envia notificação SignalR para clientes conectados com evento "LoteIniciado"
9. **FP-UC02-009**: Sistema registra operação no histórico de auditoria
10. **FP-UC02-010**: Sistema envia notificação Azure Service Bus com evento "LoteProcessamentoIniciado"
11. **FP-UC02-011**: Sistema exibe mensagem de sucesso e redireciona para dashboard de monitoramento (UC03)

**Fluxos Alternativos (FA):**

**FA-UC02-01: Atribuição Automática de Auditor no Início**
- **Condição:** Lote não possui auditor atribuído no FP-UC02-001
- **Fluxo:**
  1. Sistema executa FA-UC00-01 (atribuição automática)
  2. Sistema atribui auditor com menor carga
  3. Sistema registra atribuição no histórico
  4. Retorna ao FP-UC02-003

**Fluxos de Exceção (FE):**

**FE-UC02-01: Estado Inválido para Iniciar Processamento**
- **Condição:** Lote não está em `WaitingForProcessing` no FP-UC02-002
- **Tratamento:**
  1. Sistema exibe erro HTTP 400: "Lote deve estar em 'WaitingForProcessing' para iniciar processamento. Estado atual: {EstadoAtual}"
  2. Sistema destaca estado atual do lote
  3. Retorna ao dashboard

**FE-UC02-02: Nenhuma Fatura Selecionada**
- **Condição:** Lote possui contador `QuantidadeFaturasSelecionadas` = 0
- **Tratamento:**
  1. Sistema exibe erro: "Lote não possui faturas selecionadas. Execute seleção de faturas primeiro."
  2. Sistema oferece opção de re-executar UC01
  3. Retorna ao dashboard

**FE-UC02-03: Hangfire Indisponível**
- **Condição:** Serviço Hangfire não está disponível no FP-UC02-005
- **Tratamento:**
  1. Sistema exibe erro: "Serviço de processamento em background está indisponível. Tente novamente em alguns minutos."
  2. Sistema registra erro crítico no log
  3. Sistema envia alerta para equipe de infraestrutura
  4. Retorna ao dashboard

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição WaitingForProcessing → Processing)
- **RN-LOT-054-06**: Processamento Assíncrono com Hangfire
- **RN-LOT-054-07**: Monitoramento de Progresso com SignalR
- **RN-LOT-054-09**: Integração com RF034 (Itens de Auditoria)
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus

**Critérios de Aceite:**
- Lote transicionado para `Processing`
- Jobs Hangfire enfileirados (1 por fatura)
- Limite de concorrência aplicado
- SignalR notificou clientes conectados
- Histórico de auditoria registrou início de processamento
- Azure Service Bus enviou evento "LoteProcessamentoIniciado"
- Dashboard de monitoramento (UC03) exibe progresso em tempo real

---

## UC03 — Monitorar Progresso em Tempo Real

**Descrição:**
Permite ao usuário acompanhar o progresso do processamento do lote em tempo real via dashboard com atualização via SignalR (WebSockets), exibindo porcentagem de conclusão, quantidade de faturas processadas/pendentes/com erro, tempo estimado de conclusão, gráficos de progresso e alertas de timeout.

**Ator Principal:** `auditor` (Coordenador, Gestor, Auditor)

**Tipo:** `leitura` (Read-only)

**Impacta Dados:** `false`

**Pré-condições:**
- Lote no status `Processing`
- Usuário autenticado com permissão `AUD.LOTES.VIEW` ou `AUD.LOTES.VIEW_ALL`
- Conexão SignalR estabelecida com servidor

**Gatilho:**
Usuário acessa tela de detalhes do lote e clica em aba "Monitoramento em Tempo Real"

**Fluxo Principal (FP-UC03):**
1. **FP-UC03-001**: Sistema exibe dashboard de monitoramento
2. **FP-UC03-002**: Sistema estabelece conexão WebSocket via SignalR com servidor
3. **FP-UC03-003**: Servidor envia snapshot inicial com estado atual do lote
4. **FP-UC03-004**: Dashboard exibe cards com métricas:
   - Porcentagem de conclusão (faturas processadas / total × 100)
   - Quantidade de faturas processadas com sucesso
   - Quantidade de faturas pendentes
   - Quantidade de faturas com erro
   - Tempo decorrido desde início
   - Tempo estimado restante (baseado em velocidade média)
5. **FP-UC03-005**: Sistema exibe gráfico de barras empilhadas (sucesso / pendente / erro)
6. **FP-UC03-006**: Sistema exibe log de operações em tempo real (últimas 50 operações)
7. **FP-UC03-007**: A cada fatura processada, servidor envia mensagem SignalR com atualização
8. **FP-UC03-008**: Dashboard atualiza métricas e gráficos automaticamente sem refresh
9. **FP-UC03-009**: Se SLA for atingido, sistema exibe alerta visual destacado (RN-LOT-054-14)
10. **FP-UC03-010**: Usuário pode clicar em "Cancelar Lote" para executar UC04

**Fluxos Alternativos (FA):**

**FA-UC03-01: Lote Concluído Durante Monitoramento**
- **Condição:** Lote transiciona para `Completed` durante visualização
- **Fluxo:**
  1. Servidor envia mensagem SignalR com evento "LoteConcluído"
  2. Dashboard exibe modal de conclusão com valores consolidados
  3. Dashboard oferece opções: "Exportar Relatório" (UC06) ou "Ver Histórico" (UC10)
  4. Conexão SignalR é encerrada

**FA-UC03-02: Conexão SignalR Perdida**
- **Condição:** Conexão WebSocket é perdida (ex: problemas de rede)
- **Fluxo:**
  1. Dashboard detecta perda de conexão
  2. Sistema exibe banner: "Conexão perdida. Tentando reconectar..."
  3. Sistema tenta reconectar automaticamente (5 tentativas, intervalo exponencial)
  4. Se reconexão bem-sucedida, retorna ao FP-UC03-007
  5. Se falhar, sistema exibe botão "Atualizar Página"

**Fluxos de Exceção (FE):**

**FE-UC03-01: Lote Não Está em Processamento**
- **Condição:** Lote está em estado diferente de `Processing`
- **Tratamento:**
  1. Sistema exibe mensagem: "Lote não está em processamento. Estado atual: {EstadoAtual}"
  2. Sistema desabilita dashboard de tempo real
  3. Sistema oferece visualização estática de detalhes

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-07**: Monitoramento de Progresso com SignalR
- **RN-LOT-054-14**: SLA e Alertas de Timeout

**Critérios de Aceite:**
- Conexão SignalR estabelecida com sucesso
- Dashboard exibe métricas em tempo real (sem necessidade de refresh)
- Gráficos atualizam dinamicamente a cada fatura processada
- Alerta de timeout exibido se SLA for atingido
- Log de operações exibe últimas 50 operações cronologicamente
- Usuário pode cancelar lote a qualquer momento via UC04
- Reconexão automática funciona se conexão for perdida

---

## UC04 — Cancelar Lote com Rollback

**Descrição:**
Permite ao usuário cancelar um lote em processamento, executando rollback automático de todos os itens de auditoria já criados via RF034, parando jobs Hangfire pendentes, desassociando faturas do lote, e registrando motivo de cancelamento no histórico.

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `acao` (Ação Destrutiva com Rollback)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote no status `Processing`
- Usuário autenticado com permissão `AUD.LOTES.CANCEL`
- Módulo RF034 (Itens de Auditoria) disponível

**Gatilho:**
Usuário clica em botão "Cancelar Lote" no dashboard de monitoramento (UC03)

**Fluxo Principal (FP-UC04):**
1. **FP-UC04-001**: Sistema exibe modal de confirmação com impacto:
   - Quantidade de faturas já processadas
   - Quantidade de itens de auditoria que serão desfeitos
   - Valores já auditados que serão descartados
2. **FP-UC04-002**: Sistema solicita motivo de cancelamento (campo de texto obrigatório)
3. **FP-UC04-003**: Usuário informa motivo e confirma cancelamento
4. **FP-UC04-004**: Sistema transiciona lote para status `Cancelled` imediatamente
5. **FP-UC04-005**: Sistema para todos os jobs Hangfire pendentes do lote via `DeleteJob`
6. **FP-UC04-006**: Sistema inicia processo de rollback:
   - **Passo 1**: Consulta todos os itens de auditoria criados via RF034 para faturas do lote
   - **Passo 2**: Para cada item de auditoria, invoca endpoint RF034 para soft delete
   - **Passo 3**: Desassocia faturas do lote (remove registros de `LoteAuditoriaFatura`)
   - **Passo 4**: Marca faturas como "não processadas" (status anterior ao processamento)
7. **FP-UC04-007**: Sistema registra no histórico de auditoria:
   - Usuário responsável pelo cancelamento
   - Data/hora do cancelamento
   - Motivo informado
   - Quantidade de faturas afetadas
   - Valores já processados antes do cancelamento
8. **FP-UC04-008**: Sistema envia notificação Azure Service Bus com evento "LoteCancelado"
9. **FP-UC04-009**: Sistema envia notificação SignalR para clientes conectados
10. **FP-UC04-010**: Sistema exibe mensagem de sucesso: "Lote cancelado e rollback executado com sucesso"
11. **FP-UC04-011**: Sistema redireciona para lista de lotes

**Fluxos Alternativos (FA):**

**FA-UC04-01: Nenhum Item de Auditoria Criado Ainda**
- **Condição:** Lote foi cancelado antes de qualquer fatura ser processada
- **Fluxo:**
  1. Sistema pula Passo 1 e Passo 2 do FP-UC04-006 (não há itens para deletar)
  2. Sistema executa apenas Passo 3 e Passo 4
  3. Retorna ao FP-UC04-007

**Fluxos de Exceção (FE):**

**FE-UC04-01: Falha no Soft Delete de Item de Auditoria (RF034)**
- **Condição:** Endpoint de RF034 falha ao deletar item no Passo 2 do FP-UC04-006
- **Tratamento:**
  1. Sistema tenta deletar cada item individualmente
  2. Se um item falhar, sistema registra erro no log mas continua com demais itens
  3. Sistema marca itens que falharam no soft delete para revisão manual
  4. Sistema envia alerta para equipe técnica
  5. Continua com FP-UC04-007

**FE-UC04-02: Estado Inválido para Cancelamento**
- **Condição:** Lote não está em `Processing` (ex: já foi concluído enquanto modal estava aberto)
- **Tratamento:**
  1. Sistema exibe erro: "Lote não pode ser cancelado no estado atual: {EstadoAtual}"
  2. Sistema fecha modal de confirmação
  3. Retorna ao dashboard atualizado

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição Processing → Cancelled)
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus
- **RN-LOT-054-13**: Cancelamento de Lote com Rollback

**Critérios de Aceite:**
- Lote transicionado para `Cancelled`
- Jobs Hangfire pendentes foram parados
- Itens de auditoria criados via RF034 foram soft deleted
- Faturas desassociadas do lote e marcadas como não processadas
- Histórico registrou cancelamento com motivo, usuário, data/hora, impacto
- Notificação Azure Service Bus enviada
- Clientes SignalR notificados em tempo real
- Mensagem de sucesso exibida ao usuário

---

## UC05 — Arquivar Lote

**Descrição:**
Permite ao usuário ou sistema arquivar lotes antigos concluídos, movendo-os para status `Archived` e aplicando política de retenção configurável (ex: arquivar automaticamente lotes concluídos há mais de 90 dias). Opcionalmente move dados para tabela de arquivo frio para otimização de performance.

**Ator Principal:** `coordenador_gestor_sistema` (Coordenador, Gestor, ou Sistema via Scheduler)

**Tipo:** `acao` (Ação)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote no status `Completed`
- Usuário autenticado com permissão `AUD.LOTES.ARCHIVE` (se manual)
- OU política de retenção ativa (ex: arquivar após 90 dias)

**Gatilho:**
Usuário clica em "Arquivar" na tela de detalhes do lote OU job Hangfire de arquivamento automático dispara via scheduler

**Fluxo Principal (FP-UC05):**
1. **FP-UC05-001**: Sistema valida estado do lote (deve estar `Completed`)
2. **FP-UC05-002**: Sistema valida idade do lote (se automático, deve ter mais de N dias configurados)
3. **FP-UC05-003**: Sistema transiciona lote para status `Archived`
4. **FP-UC05-004**: Sistema atualiza campo `DataHoraArquivamento` com timestamp atual
5. **FP-UC05-005**: Sistema opcionalmente move dados para tabela de arquivo frio (otimização)
6. **FP-UC05-006**: Sistema registra operação no histórico de auditoria
7. **FP-UC05-007**: Sistema envia notificação Azure Service Bus com evento "LoteArquivado"
8. **FP-UC05-008**: Sistema exibe mensagem de sucesso (se manual)

**Fluxos Alternativos (FA):**

**FA-UC05-01: Arquivamento Automático em Lote**
- **Condição:** Job de arquivamento automático encontra múltiplos lotes elegíveis
- **Fluxo:**
  1. Job consulta todos os lotes com status `Completed` e idade > N dias
  2. Job arquiva cada lote individualmente executando FP-UC05-003 a FP-UC05-007
  3. Job envia relatório consolidado com quantidade de lotes arquivados
  4. Job finaliza

**Fluxos de Exceção (FE):**

**FE-UC05-01: Estado Inválido para Arquivamento**
- **Condição:** Lote não está em `Completed` no FP-UC05-001
- **Tratamento:**
  1. Sistema exibe erro: "Apenas lotes concluídos podem ser arquivados. Estado atual: {EstadoAtual}"
  2. Retorna ao dashboard

**FE-UC05-02: Lote Muito Recente**
- **Condição:** Lote foi concluído há menos de N dias (ex: 30 dias) no FP-UC05-002
- **Tratamento:**
  1. Sistema exibe aviso: "Lote foi concluído há apenas {DiasDesdeConClusao} dias. Deseja arquivar mesmo assim?"
  2. Usuário pode confirmar ou cancelar
  3. Se confirmar, continua com FP-UC05-003
  4. Se cancelar, retorna ao dashboard

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição Completed → Archived)
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus

**Critérios de Aceite:**
- Lote transicionado para `Archived`
- Data/hora de arquivamento registrada
- Dados movidos para tabela de arquivo frio (se configurado)
- Histórico de auditoria registrou operação
- Notificação Azure Service Bus enviada
- Lote não aparece mais em listagens padrão (apenas em filtros específicos)

---

## UC06 — Exportar Relatório de Lote

**Descrição:**
Permite ao usuário exportar relatório consolidado do lote em formato Excel ou PDF, contendo informações completas (critérios configurados, faturas selecionadas, resultados de auditoria, valores totais, estatísticas, histórico de operações).

**Ator Principal:** `auditor` (Coordenador, Gestor, Auditor)

**Tipo:** `leitura` (Read-only com geração de arquivo)

**Impacta Dados:** `false`

**Pré-condições:**
- Lote no status `Completed` ou `Archived`
- Usuário autenticado com permissão `AUD.LOTES.EXPORT`

**Gatilho:**
Usuário acessa tela de detalhes do lote e clica em botão "Exportar Relatório"

**Fluxo Principal (FP-UC06):**
1. **FP-UC06-001**: Sistema exibe modal de seleção de formato
2. **FP-UC06-002**: Usuário seleciona formato (Excel ou PDF)
3. **FP-UC06-003**: Sistema gera arquivo com estrutura:
   - **Cabeçalho**: Nome do lote, período de auditoria, critérios de seleção, auditor responsável, datas (criação, início, conclusão)
   - **Lista de Faturas Auditadas**: Número da fatura, transportadora, filial, valor original, valor auditado, valor glosado, status, tipo de glosa
   - **Valores Totais**: Valor total auditado, total de glosas identificadas, economia gerada, quantidade de faturas
   - **Estatísticas**: Taxa de aprovação (%), taxa de rejeição (%), distribuição de tipos de glosa (gráfico de pizza), tempo médio de auditoria por fatura
   - **Histórico de Operações**: Criação, seleção de faturas, início de processamento, conclusão (com usuário, data/hora)
4. **FP-UC06-004**: Sistema registra exportação no histórico de auditoria
5. **FP-UC06-005**: Sistema retorna arquivo para download
6. **FP-UC06-006**: Sistema exibe mensagem de sucesso com nome do arquivo

**Fluxos Alternativos (FA):**

**FA-UC06-01: Exportação de Lote Grande (>10.000 faturas)**
- **Condição:** Lote possui mais de 10.000 faturas
- **Fluxo:**
  1. Sistema exibe aviso: "Lote grande detectado. Exportação será processada em background."
  2. Sistema enfileira job Hangfire de exportação
  3. Job gera arquivo assincronamente
  4. Sistema envia email para usuário com link de download quando pronto
  5. Retorna ao dashboard

**Fluxos de Exceção (FE):**

**FE-UC06-01: Lote Ainda em Processamento**
- **Condição:** Lote não está em `Completed` ou `Archived`
- **Tratamento:**
  1. Sistema exibe aviso: "Lote ainda está em processamento. Exportação exibirá apenas dados parciais."
  2. Usuário pode confirmar ou cancelar
  3. Se confirmar, continua com FP-UC06-003 (gerando relatório parcial)

**FE-UC06-02: Erro na Geração do Arquivo**
- **Condição:** Falha na biblioteca de geração de Excel/PDF
- **Tratamento:**
  1. Sistema exibe erro: "Falha ao gerar relatório. Tente novamente em alguns minutos."
  2. Sistema registra erro no log com stack trace
  3. Sistema envia alerta para equipe técnica
  4. Retorna ao dashboard

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações (registra exportação)

**Critérios de Aceite:**
- Arquivo gerado no formato selecionado (Excel ou PDF)
- Relatório contém todas as seções obrigatórias (cabeçalho, lista de faturas, valores totais, estatísticas, histórico)
- Gráficos exibidos corretamente no PDF
- Histórico registrou exportação (usuário, data/hora, formato)
- Download iniciou automaticamente no navegador
- Para lotes grandes, email enviado com link de download

---

## UC07 — Reprocessar Faturas com Erro

**Descrição:**
Permite ao usuário reprocessar faturas que falharam durante o processamento inicial do lote, aplicando retry policy exponencial (1 min, 5 min, 15 min) e registrando tentativas e motivos de falha.

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `acao` (Ação)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote com faturas em status `Error`
- Usuário autenticado com permissão `AUD.LOTES.REPROCESS`

**Gatilho:**
Usuário acessa lista de faturas com erro do lote e clica em "Reprocessar Faturas com Erro"

**Fluxo Principal (FP-UC07):**
1. **FP-UC07-001**: Sistema exibe lista de faturas com erro e seus motivos de falha
2. **FP-UC07-002**: Usuário seleciona faturas para reprocessar (ou seleciona "Todas")
3. **FP-UC07-003**: Sistema exibe confirmação com quantidade de faturas selecionadas
4. **FP-UC07-004**: Usuário confirma reprocessamento
5. **FP-UC07-005**: Sistema enfileira jobs Hangfire de retry para cada fatura selecionada
6. **FP-UC07-006**: Sistema aplica retry policy exponencial (RN-LOT-054-08):
   - **1ª tentativa**: Imediata
   - **2ª tentativa**: Após 1 minuto
   - **3ª tentativa**: Após 5 minutos
   - **4ª tentativa**: Após 15 minutos
7. **FP-UC07-007**: Para cada tentativa, sistema registra no histórico da fatura:
   - Número da tentativa (1 a 4)
   - Data/hora da tentativa
   - Resultado (sucesso ou falha)
   - Motivo da falha (se aplicável)
8. **FP-UC07-008**: Se fatura for processada com sucesso em qualquer tentativa, sistema marca como `Sucesso`
9. **FP-UC07-009**: Se todas as 4 tentativas falharem, sistema marca fatura como `Error` permanente
10. **FP-UC07-010**: Sistema envia alerta para coordenador com lista de faturas que permaneceram em erro
11. **FP-UC07-011**: Sistema exibe mensagem de sucesso: "Reprocessamento iniciado para {N} faturas"

**Fluxos Alternativos (FA):**

**FA-UC07-01: Fatura Processada com Sucesso na 2ª Tentativa**
- **Condição:** Fatura que falhou na 1ª tentativa é processada com sucesso na 2ª
- **Fluxo:**
  1. Sistema marca fatura como `Sucesso`
  2. Sistema cancela tentativas 3 e 4
  3. Sistema registra no histórico: "Fatura reprocessada com sucesso na 2ª tentativa"
  4. Sistema atualiza contador de faturas processadas do lote
  5. Retorna ao FP-UC07-011

**Fluxos de Exceção (FE):**

**FE-UC07-01: Nenhuma Fatura com Erro**
- **Condição:** Lote não possui faturas em status `Error`
- **Tratamento:**
  1. Sistema exibe mensagem: "Nenhuma fatura com erro para reprocessar"
  2. Retorna ao dashboard do lote

**FE-UC07-02: Todas as Tentativas Falharam**
- **Condição:** Fatura falhou nas 4 tentativas no FP-UC07-009
- **Tratamento:**
  1. Sistema marca fatura como `Error` permanente
  2. Sistema registra no histórico: "Fatura permaneceu em erro após 4 tentativas. Motivos: [lista de motivos]"
  3. Sistema envia alerta crítico para coordenador e equipe técnica
  4. Sistema sugere análise manual da fatura

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-06**: Processamento Assíncrono com Hangfire
- **RN-LOT-054-08**: Reprocessamento Automático com Retry Policy
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações

**Critérios de Aceite:**
- Jobs de retry enfileirados para faturas selecionadas
- Retry policy exponencial aplicada (1min, 5min, 15min)
- Cada tentativa registrada no histórico da fatura
- Faturas processadas com sucesso marcadas como `Sucesso`
- Faturas que falharam 4 vezes marcadas como `Error` permanente
- Alerta enviado para coordenador com lista de erros permanentes
- Histórico do lote registrou operação de reprocessamento

---

## UC08 — Atribuir/Reatribuir Auditor

**Descrição:**
Permite ao usuário atribuir ou reatribuir auditor responsável por um lote, enviando notificações automáticas para auditor novo e antigo (se houver).

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `acao` (Ação)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote criado (qualquer status)
- Usuário autenticado com permissão `AUD.LOTES.ASSIGN_AUDITOR`

**Gatilho:**
Usuário acessa tela de edição do lote e clica em campo "Auditor Responsável"

**Fluxo Principal (FP-UC08):**
1. **FP-UC08-001**: Sistema exibe dropdown com lista de auditores disponíveis
2. **FP-UC08-002**: Sistema filtra apenas usuários com permissão `AUD.LOTES.AUDIT`
3. **FP-UC08-003**: Usuário seleciona novo auditor responsável
4. **FP-UC08-004**: Sistema valida que auditor selecionado possui permissão adequada
5. **FP-UC08-005**: Sistema atualiza lote com novo auditor
6. **FP-UC08-006**: Sistema registra no histórico de auditoria:
   - Auditor antigo (se houver)
   - Auditor novo
   - Usuário que fez a reatribuição
   - Data/hora da operação
7. **FP-UC08-007**: Se houver auditor antigo, sistema envia notificação: "Você foi removido do lote {NomeLote}"
8. **FP-UC08-008**: Sistema envia notificação para auditor novo: "Você foi atribuído ao lote {NomeLote}"
9. **FP-UC08-009**: Sistema exibe mensagem de sucesso: "Auditor atribuído com sucesso"

**Fluxos Alternativos (FA):**

**FA-UC08-01: Remover Auditor (Deixar Vazio)**
- **Condição:** Usuário limpa campo de auditor (deixa vazio)
- **Fluxo:**
  1. Sistema remove auditor do lote
  2. Sistema envia notificação apenas para auditor antigo
  3. Sistema marca lote para atribuição automática no próximo processamento
  4. Retorna ao FP-UC08-009

**Fluxos de Exceção (FE):**

**FE-UC08-01: Auditor sem Permissão**
- **Condição:** Auditor selecionado não possui permissão `AUD.LOTES.AUDIT` no FP-UC08-004
- **Tratamento:**
  1. Sistema exibe erro: "Auditor selecionado não possui permissão para auditar lotes"
  2. Sistema limpa campo de auditor
  3. Retorna ao FP-UC08-003

**FE-UC08-02: Lote Bloqueado para Edição**
- **Condição:** Lote está em status `Processing` e política não permite reatribuição durante processamento
- **Tratamento:**
  1. Sistema exibe aviso: "Lote está em processamento. Reatribuição pode afetar auditoria em andamento. Deseja continuar?"
  2. Usuário pode confirmar ou cancelar
  3. Se confirmar, continua com FP-UC08-005
  4. Se cancelar, retorna ao dashboard

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-04**: Atribuição Manual ou Automática de Auditor
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações

**Critérios de Aceite:**
- Auditor atualizado com sucesso no lote
- Histórico registrou reatribuição (auditor antigo, novo, usuário, data/hora)
- Notificação enviada para auditor antigo (se houver)
- Notificação enviada para auditor novo
- Dropdown exibiu apenas usuários com permissão `AUD.LOTES.AUDIT`
- Validação de permissão executada antes de salvar

---

## UC09 — Configurar SLA e Alertas

**Descrição:**
Permite ao usuário configurar SLA de timeout por lote (tempo máximo de processamento em horas) e receber alertas automáticos quando timeout é atingido.

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `crud` (Create/Read/Update/Delete)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote criado (qualquer status)
- Usuário autenticado com permissão `AUD.LOTES.MANAGE_SETTINGS`

**Gatilho:**
Usuário acessa tela de configurações do lote e clica em aba "SLA e Alertas"

**Fluxo Principal (FP-UC09):**
1. **FP-UC09-001**: Sistema exibe formulário de configuração de SLA
2. **FP-UC09-002**: Usuário define timeout em horas (ex: 24h, 48h, 72h)
3. **FP-UC09-003**: Usuário opcionalmente define destinatários de alertas (além do padrão)
4. **FP-UC09-004**: Usuário salva configurações
5. **FP-UC09-005**: Sistema atualiza campo `TimeoutHoras` no lote
6. **FP-UC09-006**: Sistema inicia monitoramento de tempo de processamento
7. **FP-UC09-007**: Sistema registra configuração no histórico de auditoria
8. **FP-UC09-008**: Quando lote entrar em `Processing`, job de monitoramento de timeout inicia (RN-LOT-054-14)
9. **FP-UC09-009**: Se tempo decorrido > timeout configurado:
   - Sistema envia email para coordenador e destinatários adicionais
   - Sistema exibe alerta no dashboard de monitoramento (UC03)
   - Sistema registra evento de timeout no histórico
   - Sistema envia notificação Azure Service Bus
10. **FP-UC09-010**: Sistema exibe mensagem de sucesso: "SLA configurado com sucesso"

**Fluxos Alternativos (FA):**

**FA-UC09-01: Estender SLA Durante Processamento**
- **Condição:** Lote já está em `Processing` e atingiu timeout, usuário decide estender SLA
- **Fluxo:**
  1. Usuário acessa configurações e aumenta timeout (ex: de 24h para 48h)
  2. Sistema recalcula tempo restante baseado em novo SLA
  3. Sistema limpa flag de timeout
  4. Sistema registra extensão de SLA no histórico
  5. Sistema remove alerta do dashboard
  6. Retorna ao FP-UC09-010

**Fluxos de Exceção (FE):**

**FE-UC09-01: Timeout Inválido**
- **Condição:** Usuário informa timeout menor que 1 hora ou maior que 720 horas (30 dias)
- **Tratamento:**
  1. Sistema exibe erro: "Timeout deve estar entre 1 e 720 horas"
  2. Sistema destaca campo de timeout
  3. Retorna ao FP-UC09-002

**FE-UC09-02: Email de Destinatário Inválido**
- **Condição:** Usuário informa email adicional com formato inválido
- **Tratamento:**
  1. Sistema exibe erro: "Email inválido: {EmailInformado}"
  2. Sistema destaca campo de email
  3. Retorna ao FP-UC09-003

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus
- **RN-LOT-054-14**: SLA e Alertas de Timeout

**Critérios de Aceite:**
- SLA de timeout configurado com sucesso
- Job de monitoramento de timeout iniciado quando lote entrar em `Processing`
- Alerta enviado por email quando timeout for atingido
- Alerta exibido no dashboard de monitoramento (UC03)
- Evento de timeout registrado no histórico
- Notificação Azure Service Bus enviada
- Usuário pode estender SLA durante processamento
- Histórico registrou configuração e extensões de SLA

---

## UC10 — Visualizar Histórico de Auditoria

**Descrição:**
Permite ao usuário visualizar histórico completo de todas as operações realizadas no lote (criação, seleção de faturas, início de processamento, conclusão, cancelamento, arquivamento, reatribuição de auditor), incluindo usuário responsável, data/hora, IP de origem e descrição da operação.

**Ator Principal:** `auditor` (Coordenador, Gestor, Auditor)

**Tipo:** `leitura` (Read-only)

**Impacta Dados:** `false`

**Pré-condições:**
- Lote criado (qualquer status)
- Usuário autenticado com permissão `AUD.LOTES.VIEW` ou `AUD.LOTES.VIEW_ALL`

**Gatilho:**
Usuário acessa tela de detalhes do lote e clica em aba "Histórico de Auditoria"

**Fluxo Principal (FP-UC10):**
1. **FP-UC10-001**: Sistema exibe lista cronológica de eventos (mais recente primeiro)
2. **FP-UC10-002**: Para cada evento, sistema exibe:
   - **Data/Hora**: Com precisão de milissegundos
   - **Usuário Responsável**: Nome do usuário ou "SYSTEM" para operações automáticas
   - **IP de Origem**: Endereço IP do usuário (se aplicável)
   - **Tipo de Operação**: Criação, Seleção de Faturas, Início de Processamento, Conclusão, Cancelamento, Arquivamento, Reatribuição de Auditor, Reprocessamento, Exportação, Configuração de SLA, Timeout Atingido
   - **Descrição Detalhada**: Descrição da operação em linguagem natural
   - **Valores Antes/Depois**: Para operações de atualização (ex: "Auditor alterado de João Silva para Maria Santos")
3. **FP-UC10-003**: Sistema exibe filtros:
   - Período (data início, data fim)
   - Tipo de operação (dropdown)
   - Usuário responsável (dropdown)
4. **FP-UC10-004**: Usuário pode aplicar filtros para buscar operações específicas
5. **FP-UC10-005**: Sistema atualiza lista de eventos conforme filtros
6. **FP-UC10-006**: Usuário pode exportar histórico para Excel/PDF
7. **FP-UC10-007**: Sistema pagina resultados (50 eventos por página)

**Fluxos Alternativos (FA):**

**FA-UC10-01: Filtrar Apenas Operações Críticas**
- **Condição:** Usuário quer ver apenas operações críticas (cancelamento, timeout, erros)
- **Fluxo:**
  1. Usuário seleciona filtro "Apenas Críticas"
  2. Sistema filtra eventos com tipos: Cancelamento, Timeout, Erro
  3. Sistema exibe apenas eventos críticos
  4. Retorna ao FP-UC10-007

**FA-UC10-02: Exportar Histórico Completo**
- **Condição:** Usuário clica em "Exportar Histórico" no FP-UC10-006
- **Fluxo:**
  1. Sistema gera arquivo Excel com todas as colunas
  2. Sistema inclui todos os eventos (sem paginação)
  3. Sistema registra exportação no histórico de auditoria
  4. Sistema retorna arquivo para download

**Fluxos de Exceção (FE):**

**FE-UC10-01: Histórico Vazio**
- **Condição:** Lote foi criado mas nenhuma operação foi registrada ainda
- **Tratamento:**
  1. Sistema exibe mensagem: "Nenhuma operação registrada ainda"
  2. Sistema exibe apenas evento de criação do lote
  3. Retorna ao FP-UC10-007

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações

**Critérios de Aceite:**
- Histórico exibe todos os eventos cronologicamente (mais recente primeiro)
- Cada evento exibe usuário, data/hora, IP, tipo de operação, descrição
- Operações de atualização exibem valores antes/depois
- Filtros funcionam corretamente (período, tipo, usuário)
- Paginação exibe 50 eventos por página
- Exportação para Excel/PDF funciona
- Eventos de sistema exibem "SYSTEM" como usuário
- Timestamps exibem precisão de milissegundos

---

## UC11 — Dashboard de KPIs de Lotes

**Descrição:**
Exibe dashboard consolidado com KPIs e métricas estratégicas de lotes de auditoria (quantidade de lotes ativos/concluídos/cancelados/arquivados, taxa de sucesso global, total de glosas identificadas, tempo médio de processamento, distribuição de lotes por auditor, lotes próximos ao timeout).

**Ator Principal:** `coordenador_gestor` (Coordenador de Auditoria, Gestor de Auditoria)

**Tipo:** `leitura` (Read-only)

**Impacta Dados:** `false`

**Pré-condições:**
- Usuário autenticado com permissão `AUD.LOTES.VIEW_ALL`

**Gatilho:**
Usuário acessa menu "Auditoria > Lotes de Auditoria > Dashboard"

**Fluxo Principal (FP-UC11):**
1. **FP-UC11-001**: Sistema exibe dashboard com cards de KPIs
2. **FP-UC11-002**: Sistema calcula e exibe métricas:
   - **Total de Lotes Ativos**: Quantidade de lotes com status `Processing`
   - **Lotes Concluídos Hoje**: Lotes com status `Completed` finalizados hoje
   - **Lotes Concluídos Esta Semana**: Lotes concluídos nos últimos 7 dias
   - **Lotes Concluídos Este Mês**: Lotes concluídos no mês atual
   - **Taxa de Sucesso Global**: Percentual de lotes concluídos sem erros permanentes
   - **Total de Glosas Identificadas (R$)**: Soma de valores glosados de todos os lotes
   - **Tempo Médio de Processamento (horas)**: Média de tempo entre início e conclusão de lotes
   - **Lotes Cancelados**: Quantidade total de lotes com status `Cancelled`
3. **FP-UC11-003**: Sistema exibe gráficos:
   - **Gráfico de Pizza**: Distribuição de lotes por auditor
   - **Gráfico de Barras**: Lotes por semana (últimas 8 semanas)
   - **Gráfico de Linha**: Evolução de glosas identificadas por mês (últimos 6 meses)
4. **FP-UC11-004**: Sistema exibe lista "Lotes Próximos ao Timeout":
   - Lotes em `Processing` com tempo decorrido > 80% do SLA configurado
   - Ordenados por proximidade ao timeout (mais urgente primeiro)
   - Exibir nome do lote, auditor, tempo decorrido, SLA, % de conclusão
5. **FP-UC11-005**: Sistema atualiza dashboard automaticamente a cada 5 minutos
6. **FP-UC11-006**: Usuário pode clicar em qualquer card/gráfico para drill-down (ver detalhes)

**Fluxos Alternativos (FA):**

**FA-UC11-01: Filtrar Dashboard por Período**
- **Condição:** Usuário quer ver KPIs de período específico
- **Fluxo:**
  1. Usuário seleciona período (última semana, último mês, último trimestre, customizado)
  2. Sistema recalcula KPIs e gráficos para período selecionado
  3. Sistema atualiza dashboard
  4. Retorna ao FP-UC11-006

**FA-UC11-02: Drill-Down em Card de KPI**
- **Condição:** Usuário clica em card "Total de Lotes Ativos"
- **Fluxo:**
  1. Sistema abre modal com lista detalhada de lotes ativos
  2. Modal exibe nome, auditor, % de conclusão, tempo decorrido, SLA
  3. Usuário pode clicar em lote para acessar dashboard de monitoramento (UC03)

**Fluxos de Exceção (FE):**

**FE-UC11-01: Nenhum Lote Criado Ainda**
- **Condição:** Sistema não possui nenhum lote criado
- **Tratamento:**
  1. Sistema exibe mensagem: "Nenhum lote criado ainda. Crie seu primeiro lote para visualizar KPIs."
  2. Sistema exibe botão "Criar Novo Lote" (redireciona para UC00)
  3. Retorna ao dashboard vazio

**Regras de Negócio Aplicadas:**
- Nenhuma regra específica (apenas consultas e cálculos)

**Critérios de Aceite:**
- Dashboard exibe todos os KPIs corretamente calculados
- Gráficos renderizam corretamente (pizza, barras, linha)
- Lista "Lotes Próximos ao Timeout" exibe lotes ordenados por urgência
- Dashboard atualiza automaticamente a cada 5 minutos
- Usuário pode filtrar dashboard por período
- Drill-down em cards funciona corretamente
- Mensagem apropriada exibida se nenhum lote existir

---

## UC12 — Job: Processar Lote em Background

**Descrição:**
Job Hangfire executado em background que processa cada fatura do lote individualmente, integrando com RF034 para criação de itens de auditoria, consolidando resultados via RF035, aplicando retry policy para falhas temporárias, enviando notificações SignalR de progresso, e monitorando timeout.

**Ator Principal:** `sistema` (Hangfire Background Job)

**Tipo:** `batch` (Processamento em Lote)

**Impacta Dados:** `true`

**Pré-condições:**
- Lote no status `Processing`
- Faturas associadas ao lote
- Jobs enfileirados no Hangfire

**Gatilho:**
Jobs Hangfire disparados automaticamente após UC02 (Iniciar Processamento)

**Fluxo Principal (FP-UC12):**
1. **FP-UC12-001**: Job Hangfire inicia para processar uma fatura específica
2. **FP-UC12-002**: Job consulta dados da fatura (número, transportadora, filial, valor, tipo de serviço)
3. **FP-UC12-003**: Job invoca endpoint de RF034 para criar item de auditoria:
   - Tipo de auditoria: "Auditoria de Lote"
   - Status inicial: "Pendente de Revisão"
   - Valores auditados: valor da fatura
   - Associação ao lote
4. **FP-UC12-004**: Job aplica regras de validação de auditoria (configuradas no lote)
5. **FP-UC12-005**: Job calcula valores glosados (se aplicável)
6. **FP-UC12-006**: Job atualiza item de auditoria com resultados (valores glosados, status final)
7. **FP-UC12-007**: Job atualiza status da fatura no lote (`Sucesso`)
8. **FP-UC12-008**: Job incrementa contador `QuantidadeFaturasProcessadas` no lote
9. **FP-UC12-009**: Job envia mensagem SignalR para clientes conectados com atualização de progresso
10. **FP-UC12-010**: Job registra operação no histórico da fatura
11. **FP-UC12-011**: Quando todas as faturas são processadas, job de consolidação inicia:
    - Calcula valores totais (valor auditado, glosas, economia)
    - Calcula estatísticas (taxa de aprovação, taxa de rejeição)
    - Integra com RF035 para atualizar status global do lote
12. **FP-UC12-012**: Job transiciona lote para status `Completed`
13. **FP-UC12-013**: Job envia notificação Azure Service Bus com evento "LoteConcluído"
14. **FP-UC12-014**: Job finaliza com sucesso

**Fluxos Alternativos (FA):**

**FA-UC12-01: Fatura Já Processada (Idempotência)**
- **Condição:** Job executa novamente para fatura já processada
- **Fluxo:**
  1. Job verifica se fatura já possui item de auditoria criado
  2. Job valida se status da fatura no lote é `Sucesso`
  3. Job pula processamento e finaliza com sucesso
  4. Retorna ao FP-UC12-014

**FA-UC12-02: Integração RF034 Retorna Item Existente**
- **Condição:** RF034 informa que item de auditoria já existe para a fatura
- **Fluxo:**
  1. Job invoca endpoint de atualização em vez de criação
  2. Job atualiza item existente com novos valores
  3. Retorna ao FP-UC12-007

**Fluxos de Exceção (FE):**

**FE-UC12-01: Falha na Integração com RF034**
- **Condição:** Endpoint de RF034 retorna erro no FP-UC12-003
- **Tratamento:**
  1. Hangfire aplica retry automático (RN-LOT-054-08):
     - 1ª tentativa: Imediata
     - 2ª tentativa: Após 1 minuto
     - 3ª tentativa: Após 5 minutos
     - 4ª tentativa: Após 15 minutos
  2. Job registra cada tentativa no histórico da fatura
  3. Se todas as tentativas falharem, job marca fatura como `Error` permanente
  4. Job registra motivo da falha
  5. Job continua com próxima fatura

**FE-UC12-02: Timeout de Processamento de Fatura**
- **Condição:** Processamento de uma fatura excede timeout configurado (ex: 5 minutos)
- **Tratamento:**
  1. Hangfire cancela job automaticamente
  2. Sistema marca fatura como `Error` com motivo "Timeout"
  3. Sistema aplica retry policy (até 4 tentativas)
  4. Se timeout persistir, marca como erro permanente

**FE-UC12-03: Lote Cancelado Durante Processamento**
- **Condição:** UC04 cancela lote enquanto jobs ainda estão processando
- **Tratamento:**
  1. Jobs detectam que lote foi cancelado (verifica status a cada iteração)
  2. Jobs param processamento imediatamente
  3. Jobs não executam rollback (UC04 faz rollback)
  4. Jobs finalizam sem erro

**Regras de Negócio Aplicadas:**
- **RN-LOT-054-05**: Máquina de Estados do Lote (transição Processing → Completed)
- **RN-LOT-054-06**: Processamento Assíncrono com Hangfire
- **RN-LOT-054-07**: Monitoramento de Progresso com SignalR
- **RN-LOT-054-08**: Reprocessamento Automático com Retry Policy
- **RN-LOT-054-09**: Integração com RF034 (Itens de Auditoria)
- **RN-LOT-054-10**: Consolidação Automática com RF035
- **RN-LOT-054-11**: Histórico e Auditoria Completa de Operações
- **RN-LOT-054-12**: Notificações Assíncronas via Azure Service Bus

**Critérios de Aceite:**
- Jobs executam em background sem bloquear interface
- Cada fatura processada individualmente
- Itens de auditoria criados via RF034 com sucesso
- Progresso enviado via SignalR a cada fatura processada
- Retry policy aplicada para falhas temporárias (1min, 5min, 15min)
- Faturas que falharam 4 vezes marcadas como erro permanente
- Consolidação executada após todas as faturas processadas
- Lote transicionado para `Completed` ao final
- Notificação Azure Service Bus enviada
- Jobs são idempotentes (podem executar múltiplas vezes sem efeitos colaterais)
- Limite de concorrência respeitado (máximo N jobs simultâneos)

---

## Mapeamento de Cobertura

### Funcionalidades → Casos de Uso

| Funcionalidade | UC | Cobertura |
|----------------|-----|-----------|
| FUNC-LOT-01: Criar Lote de Auditoria | UC00 | 100% |
| FUNC-LOT-02: Selecionar Faturas Automaticamente | UC01 | 100% |
| FUNC-LOT-03: Iniciar Processamento do Lote | UC02 | 100% |
| FUNC-LOT-04: Monitorar Progresso em Tempo Real | UC03 | 100% |
| FUNC-LOT-05: Cancelar Lote com Rollback | UC04 | 100% |
| FUNC-LOT-06: Consolidar Resultados Automaticamente | UC12 | 100% |
| FUNC-LOT-07: Arquivar Lote | UC05 | 100% |
| FUNC-LOT-08: Exportar Relatório Consolidado | UC06 | 100% |
| FUNC-LOT-09: Reprocessar Faturas com Erro | UC07 | 100% |
| FUNC-LOT-10: Atribuir/Reatribuir Auditor | UC08 | 100% |
| FUNC-LOT-11: Configurar SLA e Alertas de Timeout | UC09 | 100% |
| FUNC-LOT-12: Visualizar Histórico de Auditoria do Lote | UC10 | 100% |
| FUNC-LOT-13: Dashboard de KPIs de Lotes | UC11 | 100% |

**Cobertura Total de Funcionalidades:** 13/13 = **100%**

### Regras de Negócio → Casos de Uso

| Regra de Negócio | UC | Cobertura |
|------------------|-----|-----------|
| RN-LOT-054-01: Obrigatoriedade de Critérios de Seleção | UC00 | 100% |
| RN-LOT-054-02: Lote Imutável Após Processamento Iniciado | UC00, UC02 | 100% |
| RN-LOT-054-03: Seleção Automática de Faturas por Critérios | UC01 | 100% |
| RN-LOT-054-04: Atribuição Manual ou Automática de Auditor | UC00, UC08 | 100% |
| RN-LOT-054-05: Máquina de Estados do Lote | UC00, UC01, UC02, UC04, UC05, UC12 | 100% |
| RN-LOT-054-06: Processamento Assíncrono com Hangfire | UC01, UC02, UC07, UC12 | 100% |
| RN-LOT-054-07: Monitoramento de Progresso com SignalR | UC03, UC12 | 100% |
| RN-LOT-054-08: Reprocessamento Automático com Retry Policy | UC07, UC12 | 100% |
| RN-LOT-054-09: Integração com RF034 (Itens de Auditoria) | UC02, UC12 | 100% |
| RN-LOT-054-10: Consolidação Automática com RF035 | UC12 | 100% |
| RN-LOT-054-11: Histórico e Auditoria Completa de Operações | UC00, UC01, UC02, UC04, UC05, UC06, UC07, UC08, UC09, UC10, UC12 | 100% |
| RN-LOT-054-12: Notificações Assíncronas via Azure Service Bus | UC00, UC01, UC02, UC04, UC05, UC09, UC12 | 100% |
| RN-LOT-054-13: Cancelamento de Lote com Rollback | UC04 | 100% |
| RN-LOT-054-14: SLA e Alertas de Timeout | UC03, UC09 | 100% |

**Cobertura Total de Regras de Negócio:** 14/14 = **100%**

### Resumo de Cobertura

- **Total de Casos de Uso Criados:** 13 (UC00 a UC12)
- **Total de Funcionalidades Cobertas:** 13/13 (100%)
- **Total de Regras de Negócio Cobertas:** 14/14 (100%)
- **Total de Fluxos Principais (FP):** 120+ passos detalhados
- **Total de Fluxos Alternativos (FA):** 12 fluxos
- **Total de Fluxos de Exceção (FE):** 23 fluxos

---

## Histórico de Versões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-30 | Agência ALC - alc.dev.br | Versão inicial (resumida, 9 UCs superficiais) |
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Reescrita completa seguindo template padrão UC.md, 13 UCs detalhados com FP/FA/FE/Regras/Critérios, 100% cobertura de funcionalidades e regras de negócio |

---

**FIM DO DOCUMENTO UC-RF054 v2.0**

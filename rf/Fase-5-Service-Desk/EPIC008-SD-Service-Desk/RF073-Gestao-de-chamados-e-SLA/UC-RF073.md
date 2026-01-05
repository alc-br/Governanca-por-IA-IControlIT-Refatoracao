# UC-RF073 - Casos de Uso - Gestão de Chamados e SLA

## UC01: Criar Chamado com Priorização Automática via Matriz Impacto x Urgência

### 1. Descrição

Este caso de uso permite que usuário final (solicitante) ou analista de suporte crie novo chamado (ticket) fornecendo contexto mínimo obrigatório (descrição ≥20 chars, categoria 3 níveis, ativos afetados OU centro de custo). O sistema calcula prioridade automaticamente via matriz Impacto x Urgência (Alto/Médio/Baixo) resultando em P1/P2/P3/P4, determina SLA de resposta e resolução baseado em prioridade, e roteia automaticamente para fila de atendimento especializada via skill-based routing.

### 2. Atores

- Usuário Solicitante (principal - pode ser usuário final ou analista criando em nome de terceiro)
- Sistema (validação, cálculo de prioridade, roteamento, notificação)

### 3. Pré-condições

- Usuário autenticado com permissão `chamado:criar`
- Multi-tenancy ativo (ClienteId válido)
- Mínimo 1 categoria de chamado cadastrada
- Mínimo 1 fila de atendimento configurada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Service Desk > Chamados > Novo Chamado" | - |
| 2 | - | Valida permissão RBAC `chamado:criar` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe formulário de criação com campos obrigatórios em destaque |
| 5 | Preenche Descrição textarea "Linhas do PABX não completam chamadas externas para celular" (80 caracteres) | - |
| 6 | Seleciona Categoria em cascata 3 níveis: Nível 1="Telefonia" → Nível 2="PABX" → Nível 3="Erro Conectividade" | - |
| 7 | - | Carrega subcategorias via AJAX conforme seleção anterior sem reload de página |
| 8 | Seleciona Ativo(s) Afetado(s) via autocomplete: "PABX-Sala001" | - |
| 9 | - | Autocomplete executa query em Ativos com filtro multi-tenancy (ClienteId) e Status=Ativo |
| 10 | Opcionalmente preenche Centro de Custo: "Administrativo" | - |
| 11 | Marca checkbox "Calcular prioridade automaticamente" (default checked) | - |
| 12 | - | Sistema coleta fatores de cálculo: Impacto (número de ativos afetados: 1 = Médio), Urgência (usuário solicitante não é crítico = Média) |
| 13 | - | Executa PriorityCalculator.CalculatePriority(isHighImpact=false, isHighUrgency=false) |
| 14 | - | Resultado: Prioridade = P3 (Médio Impacto + Média Urgência) |
| 15 | - | Exibe preview da prioridade calculada "Prioridade sugerida: P3 (Médio)" com botão "Alterar Manualmente" |
| 16 | Clica "Criar Chamado" | - |
| 17 | - | Executa CreateTicketCommand com FluentValidation |
| 18 | - | Valida RN-CHA-073-01: Descrição mínimo 20 chars ✓, Categoria selecionada ✓, Mínimo 1 ativo ✓ |
| 19 | - | Cria entity Ticket com Status=Novo, DataCriacao=UtcNow, SolicitanteId=UsuarioAutenticado |
| 20 | - | Executa SlaCalculator.CalculateSla(ticket, contractSla=null) baseado em prioridade P3 |
| 21 | - | Calcula SLA Resposta: DataCriacao + 8h = 18:00h (se criado 10:00h), SLA Resolução: DataCriacao + 24h = 10:00h próximo dia |
| 22 | - | Persiste Ticket + TicketSLA entities via UnitOfWork |
| 23 | - | Executa SkillBasedRouter.RouteToOptimalTechnician(ticket) |
| 24 | - | Mapeia Categoria "Telefonia/PABX" para fila QUEUE_TELECOM |
| 25 | - | Busca técnicos disponíveis em QUEUE_TELECOM ordenados por carga atual (AssignedTickets.Count ASC) |
| 26 | - | Seleciona técnico João (3 chamados ativos, menor carga entre 5 técnicos: João 3, Ana 5, Bruno 7, Carlos 4, Diana 6) |
| 27 | - | Atualiza Ticket.AnalistaAtribuidoId = João, Status = Atribuído |
| 28 | - | Envia notificação multi-canal para João: E-mail SendGrid "Novo chamado #9876 atribuído", In-app badge +1, MS Teams menção |
| 29 | - | Envia notificação para solicitante: E-mail "Chamado #9876 criado com sucesso. Acompanhe em: [link]" |
| 30 | - | Registra auditoria com i18n (chave `chamado.criado`, ClienteId, SolicitanteId, AnalistaAtribuidoId, timestamp) |
| 31 | - | Incrementa métrica Prometheus `chamados_criados_total{prioridade="P3",categoria="Telefonia"}` |
| 32 | - | Retorna HTTP 201 Created com TicketDto incluindo ID gerado, SLA calculado, analista atribuído |
| 33 | - | Redireciona para tela de detalhes do chamado `/chamados/{id}` com mensagem toast verde "Chamado #9876 criado e atribuído para João" |

### 5. Fluxos Alternativos

**FA01: Priorização Manual (Override do Cálculo Automático)**
- Passo 11: Usuário desmarca checkbox "Calcular automaticamente" e seleciona manualmente Prioridade=P1
- Sistema aceita prioridade manual sobrescrevendo matriz
- Sistema registra em auditoria "Prioridade definida manualmente: P1 (sugestão automática era P3)"
- SLA calculado baseado em P1: Resposta 1h, Resolução 4h

**FA02: Contrato Específico Sobrescreve SLA Padrão**
- Passo 20: Sistema identifica que ativo PABX-Sala001 pertence a Contrato #123 (Cliente Premium)
- Sistema busca ContractSLA do Contrato #123 que define SLA customizado: Resposta P3 = 4h (não 8h padrão), Resolução P3 = 16h (não 24h padrão)
- Sistema usa SLA do contrato sobrescrevendo padrão
- Chamado criado com SLA Resposta 14:00h, Resolução 02:00h próximo dia

**FA03: Múltiplos Ativos Afetados (Alto Impacto)**
- Passo 8: Usuário seleciona 5 ativos no autocomplete: "PABX-Sala001", "PABX-Sala002", "PABX-Sala003", "PABX-Sala004", "PABX-Sala005"
- Sistema detecta Alto Impacto (>3 ativos)
- Passo 13: PriorityCalculator com isHighImpact=true, isHighUrgency=false resulta em P2 (Alto)
- SLA calculado: Resposta 4h, Resolução 8h

**FA04: Usuário Crítico (CEO/Diretor) - Alta Urgência**
- Passo 12: Sistema consulta Usuarios table e detecta usuário solicitante possui flag Critico=true (CEO da empresa)
- Sistema marca Alta Urgência automaticamente
- Passo 13: PriorityCalculator com isHighUrgency=true resulta em P1 ou P2 dependendo de impacto
- Notificação URGENTE enviada via SMS além de e-mail/in-app

**FA05: Nenhum Técnico Disponível na Fila**
- Passo 25: QUEUE_TELECOM não possui técnicos ativos (todos em pausa, férias ou sobrecarregados ≥8 chamados)
- Sistema tenta fila genérica QUEUE_GERAL como fallback
- Se também vazia, deixa chamado Status=Novo sem atribuição, cria AlertaChamado tipo "Falta de Recursos"
- Sistema envia alerta para Gestor da área "Chamado #9876 P3 sem técnico disponível - intervenção necessária"

### 6. Exceções

**EX01: Descrição Muito Curta (<20 caracteres)**
- Passo 18: FluentValidation detecta Descrição="Problema PABX" (15 caracteres)
- Sistema retorna HTTP 400 Bad Request com mensagem i18n "RN-CHA-073-01: Descrição deve ter mínimo 20 caracteres"
- Frontend destaca campo Descrição em vermelho com mensagem de erro

**EX02: Nenhum Ativo Selecionado**
- Passo 18: Validação detecta AtivoIds=[] (vazio) AND CentroCustoId=null
- Sistema retorna HTTP 400 "RN-CHA-073-01: Selecione pelo menos um ativo afetado OU um centro de custo"
- Frontend exibe mensagem de erro em ambos campos

**EX03: Categoria Não Existe (Inválida)**
- Passo 18: CategoriaId=999 não existe no banco (cliente deletou categoria recentemente)
- Sistema retorna HTTP 404 Not Found "Categoria selecionada não encontrada"
- Frontend recarrega lista de categorias e solicita nova seleção

**EX04: Falha ao Enviar Notificação (SendGrid Offline)**
- Passo 28: SendGrid retorna HTTP 503 Service Unavailable
- Sistema loga erro mas NÃO bloqueia criação do chamado (graceful degradation)
- Chamado criado com sucesso, notificação agendada para retry exponencial (3 tentativas: 30s, 2min, 10min)
- Sistema registra NotificacaoFalhada entity para tracking

### 7. Pós-condições

- Chamado criado no banco de dados (Ticket entity)
- SLA calculado e persistido (TicketSLA entity)
- Chamado atribuído automaticamente para técnico via skill-based routing
- Notificações enviadas para analista e solicitante
- Auditoria registrada com todos os campos
- Métricas Prometheus incrementadas
- Status inicial definido (Novo ou Atribuído dependendo de disponibilidade de técnico)

### 8. Regras de Negócio Aplicáveis

- RN-CHA-073-01: Criação Requer Contexto Válido (descrição ≥20 chars, categoria, ativos OU centro custo)
- RN-CHA-073-02: Prioridade Calculada via Matriz Impacto x Urgência (P1: Alto+Alto, P2: Alto OU Alto, P3: Médio+Médio, P4: Baixo+Baixo)
- RN-CHA-073-03: SLA Baseado em Prioridade e Contrato (P1: 1h/4h, P2: 4h/8h, P3: 8h/24h, P4: 24h/72h, contrato sobrescreve)
- RN-CHA-073-05: Atribuição Automática Skill-Based Routing (categoria → fila → técnico menor carga)
- RN-CHA-073-09: Auditoria de Todas Mudanças (7 anos retenção LGPD)
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC02: Recalcular Status de SLA Automaticamente via Hangfire Job

### 1. Descrição

Este caso de uso descreve o processo automático (Hangfire RecurringJob a cada 5 minutos) que recalcula status de SLA de TODOS chamados em aberto, determinando se estão "No Prazo" (>20% tempo restante), "Em Risco" (5-20% tempo restante) ou "Vencido" (<5% OU data vencimento ultrapassada). O job considera pausas de downtime de ativos que suspendem SLA, envia notificações proativas para chamados em risco, e cria alertas críticos para chamados vencidos.

### 2. Atores

- Sistema (Hangfire Job executado automaticamente)
- Analistas (receptores de notificações de risco)
- Gestores (receptores de alertas de SLA vencido)

### 3. Pré-condições

- Hangfire rodando com job RecalculateSlaStatusJob ativo
- Chamados ativos no banco (Status ≠ Fechado)
- SLA configurado para cada chamado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara RecalculateSlaStatusJob a cada 5 minutos (Cron.MinuteInterval(5)) |
| 2 | - | Job executa ISlaRecalculationHandler.UpdateAllOpenTickets() |
| 3 | - | Busca TODOS chamados com Status IN (Novo, Atribuído, EmAndamento) via query otimizada com índices |
| 4 | - | Aplica filtro multi-tenancy (processa por ClienteId em batch para evitar cross-tenant) |
| 5 | - | Identifica 1.247 chamados ativos em sistema (distribuídos em 15 clientes) |
| 6 | - | Para primeiro chamado (ID 9876, P1, criado 10:00h, SLA Resolução 14:00h, atual 13:00h): |
| 7 | - | Busca TicketDowntime entities associadas (pausas de ativo) |
| 8 | - | Identifica 1 pausa: DataInicio=11:00h, DataFim=11:30h (30 minutos de manutenção programada) |
| 9 | - | Executa SlaElapsedCalculator.CalculateElapsedTime(ticket, downtimes) |
| 10 | - | Calcula: TotalDecorrido = 13:00h - 10:00h = 3h, Pausas = 30min, TempoEfetivoDecorrido = 3h - 30min = 2.5h |
| 11 | - | SLA Resolução: 4h totais, Restante = 4h - 2.5h = 1.5h, Percentual Restante = 1.5h / 4h = 37.5% |
| 12 | - | Executa SlaStatusCalculator.GetStatus(elapsedTime, dueDate) |
| 13 | - | Resultado: 37.5% > 20% → Status = NoPrazo |
| 14 | - | Atualiza Ticket.SlaStatus = NoPrazo (se diferente do anterior) |
| 15 | - | Para segundo chamado (ID 9877, P2, criado 08:00h, SLA Resolução 16:00h, atual 15:30h): |
| 16 | - | Sem pausas de downtime |
| 17 | - | TempoDecorrido = 15:30h - 08:00h = 7.5h, SLA Total = 8h, Restante = 0.5h |
| 18 | - | Percentual Restante = 0.5h / 8h = 6.25% (entre 5% e 20%) |
| 19 | - | Resultado: Status = EmRisco |
| 20 | - | Atualiza Ticket.SlaStatus = EmRisco |
| 21 | - | Detecta mudança de status (anterior era NoPrazo) → dispara NotificacaoRiscoSLAService |
| 22 | - | Envia notificação URGENTE para analista atribuído (Bruno): E-mail "Chamado #9877 entrando em risco de SLA (6% tempo restante, vence 16:00h)", SMS, In-app alerta amarelo |
| 23 | - | Envia notificação para Gestor da fila: "Chamado #9877 (Bruno) em risco de SLA - 30 min restantes" |
| 24 | - | Para terceiro chamado (ID 9878, P3, criado ontem 10:00h, SLA Resolução hoje 10:00h, atual 11:00h): |
| 25 | - | TempoDecorrido = 25h (ultrapasso SLA de 24h) |
| 26 | - | Resultado: Status = Vencido |
| 27 | - | Atualiza Ticket.SlaStatus = Vencido |
| 28 | - | Detecta violação de SLA → cria AlertaSLA entity com Tipo=ViolacaoSLA, Gravidade=Critica |
| 29 | - | Envia notificação CRÍTICA multi-canal para Gestor: E-mail "SLA VIOLADO: Chamado #9878 P3 vencido há 1h", SMS, MS Teams menção |
| 30 | - | Envia e-mail para Cliente (se configurado no contrato) notificando violação conforme SLA contratual |
| 31 | - | Incrementa métrica Prometheus `sla_violacoes_total{prioridade="P3",categoria="Hardware"}` |
| 32 | - | Registra violação em tabela SlaViolacao para cálculo de penalidades contratuais |
| 33 | - | Continua processamento para próximos 1.244 chamados em loop otimizado |
| 34 | - | Após processar todos, executa SaveChangesAsync batch (UnitOfWork commit único) |
| 35 | - | Job finaliza com log "RecalculateSlaStatusJob concluído: 1.247 chamados processados, 1.120 No Prazo, 98 Em Risco, 29 Vencidos. Tempo execução: 38s" |

### 5. Fluxos Alternativos

**FA01: Chamado com Múltiplas Pausas de Downtime**
- Passo 8: Chamado possui 3 pausas: 11:00-11:30 (30min), 12:00-12:15 (15min), 13:00-13:45 (45min)
- Passo 10: Sistema soma TODAS pausas: TotalPausado = 30min + 15min + 45min = 90min (1.5h)
- TempoEfetivoDecorrido = TempoDecorrido - TotalPausado
- SLA ajustado considerando todas suspensões

**FA02: Pausa de Downtime Ainda Ativa (DataFim=null)**
- Passo 8: Pausa iniciada 12:00h, DataFim=null (ativo ainda em manutenção)
- Passo 10: Sistema usa DataFim=UtcNow para cálculo temporário
- SLA suspenso DURANTE período de pausa ativa
- Quando pausa finalizada (DataFim preenchido), recálculo ajusta retroativamente

**FA03: Chamado Muda de "Em Risco" para "No Prazo" (Progresso Realizado)**
- Passo 20: Status anterior era EmRisco
- Analista adicionou comentário "Solução aplicada, aguardando confirmação" atualizando progresso
- Sistema recalcula e detecta melhora (ex: pausa adicionada ou SLA ajustado)
- Status volta para NoPrazo
- Sistema envia notificação positiva para Gestor "Chamado #9877 saiu de risco - ação corretiva efetiva"

**FA04: Integração com ServiceNow - Sync de Status SLA**
- Passo 27: Chamado Vencido está sincronizado com ServiceNow (ExternalTicketId preenchido)
- Sistema dispara SyncTicketToServiceNowCommand atualizando status no ServiceNow
- ServiceNow recebe update: State="Vencido", Priority elevado automaticamente
- Webhook de ServiceNow pode retornar ação (ex: "Escalar para Nível 3")

### 6. Exceções

**EX01: Job Hangfire Travado (Timeout >10min)**
- Passo 35: Processamento de 10.000 chamados demora >10min (configuração de timeout)
- Hangfire cancela job automaticamente
- Sistema loga erro "RecalculateSlaStatusJob cancelado por timeout após processar 6.543 de 10.000 chamados"
- Próxima execução (5min) reinicia processamento dos restantes
- Chamados não processados aguardam próximo ciclo (máximo 5min de atraso)

**EX02: Falha ao Enviar Notificação de Risco**
- Passo 22: SendGrid offline (HTTP 503)
- Sistema loga warning mas NÃO bloqueia atualização de status
- Status SLA atualizado corretamente
- Notificação agendada para retry via Hangfire (3 tentativas)

**EX03: Cálculo de SLA com Dados Inconsistentes (DataCriacao no Futuro)**
- Passo 10: Ticket.DataCriacao = 2025-12-30 (futuro, erro de dados)
- Sistema detecta inconsistência: DataCriacao > UtcNow
- Sistema loga erro crítico "Ticket #9999 possui DataCriacao no futuro - dados inconsistentes"
- Sistema pula esse ticket do processamento, registra em tabela ErrosProcessamento
- Alerta enviado para DBA investigar corrupção de dados

**EX04: Nenhum Chamado Ativo (Sistema Sem Carga)**
- Passo 5: Query retorna 0 chamados ativos
- Job finaliza imediatamente com log "RecalculateSlaStatusJob: Nenhum chamado ativo. Tempo execução: 0.5s"
- Não há processamento, não há notificações

### 7. Pós-condições

- Status SLA de TODOS chamados ativos atualizados (NoPrazo, EmRisco, Vencido)
- Notificações enviadas para analistas/gestores conforme mudanças de status
- Alertas críticos criados para violações de SLA
- Métricas Prometheus atualizadas
- Tabela SlaViolacao populada para cálculo de penalidades
- Integração ServiceNow sincronizada (se aplicável)
- Log de execução registrado para auditoria

### 8. Regras de Negócio Aplicáveis

- RN-CHA-073-06: Status SLA (No Prazo >20%, Risco 5-20%, Vencido <5% OU vencido)
- RN-CHA-073-04: Parada de Ativo Suspende SLA (downtimes não contam para tempo decorrido)
- RN-CHA-073-03: SLA Baseado em Prioridade (P1: 1h/4h, P2: 4h/8h, P3: 8h/24h, P4: 24h/72h)
- RN-CHA-073-10: Integração ServiceNow para P1/P2 (sync bidirecional)
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC03: Adicionar Comentário com Visibilidade Interna ou Externa

### 1. Descrição

Este caso de uso permite que analista de suporte ou solicitante adicione comentário a chamado ativo, controlando visibilidade (Interno = apenas equipe, Externo = visível ao cliente). Comentários podem incluir anexos (upload Azure Blob Storage, max 5MB), são registrados com timestamp e autor, e disparam notificações conforme tipo (Externo notifica solicitante via e-mail, Interno apenas equipe via in-app).

### 2. Atores

- Analista de Suporte (principal - adiciona comentários internos/externos)
- Usuário Solicitante (visualiza apenas comentários externos)
- Sistema (validação, upload, notificação)

### 3. Pré-condições

- Usuário autenticado (analista OU solicitante)
- Chamado ativo (Status ≠ Fechado)
- Permissão `chamado:comentar` (analistas) OU `chamado:comentar:proprio` (solicitantes)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Analista acessa detalhes do Chamado #9876 `/chamados/9876` | - |
| 2 | - | Valida permissão RBAC `chamado:comentar` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Executa GetTicketCommentsQuery(TicketId=9876) |
| 5 | - | Busca comentários com filtro: WHERE TicketId=9876 AND (Visibility=External OR CurrentUser.IsStaff=true) |
| 6 | - | Retorna 3 comentários: 2 Externos (visíveis a todos), 1 Interno (visível apenas para analista logado) |
| 7 | - | Frontend exibe timeline de comentários com ícones diferenciados: 🔓 Externo, 🔒 Interno |
| 8 | Analista clica "Adicionar Comentário" | - |
| 9 | - | Frontend exibe formulário com: Textarea "Texto do Comentário", Radio buttons "Visibilidade: Externo (Cliente vê) / Interno (Apenas Equipe)", Upload arquivo "Anexar imagem/documento (max 5MB)" |
| 10 | Analista digita texto "Testamos solução. Aguardando retorno do fabricante para peça de reposição. Previsão 2 dias úteis." (115 caracteres) | - |
| 11 | Analista seleciona Visibilidade = Interno (cliente não deve ver detalhes técnicos de peça) | - |
| 12 | Analista anexa arquivo "Diagnostico_PABX_9876.pdf" (2.3 MB) via upload | - |
| 13 | - | Frontend valida tamanho arquivo ≤5MB ✓, tipo MIME permitido (pdf, jpg, png, txt, xlsx, docx) ✓ |
| 14 | Clica "Enviar Comentário" | - |
| 15 | - | Executa AddCommentCommand com FluentValidation |
| 16 | - | Valida: Texto mínimo 5 caracteres ✓, Arquivo ≤5MB ✓, Tipo MIME permitido ✓ |
| 17 | - | Upload arquivo para Azure Blob Storage container `chamados-anexos/{ClienteId}/{TicketId}/{CommentId}/Diagnostico_PABX_9876.pdf` |
| 18 | - | Azure Blob retorna URL CDN `https://icontrolit.blob.core.windows.net/chamados-anexos/.../Diagnostico_PABX_9876.pdf` |
| 19 | - | Cria entity TicketComment com: TicketId=9876, Text="Testamos...", Visibility=Internal, AuthorId=UsuarioAutenticado, CreatedAt=UtcNow, AttachmentUrl=BlobURL |
| 20 | - | Persiste comentário no banco via UnitOfWork |
| 21 | - | Registra auditoria com i18n (chave `chamado.comentario.adicionado`, TicketId, AuthorId, Visibility, timestamp) |
| 22 | - | Verifica Visibility = Internal → NÃO envia notificação para solicitante (cliente não deve ver) |
| 23 | - | Envia notificação in-app para OUTROS analistas da mesma fila: Badge +1 "Novo comentário interno no Chamado #9876" |
| 24 | - | Incrementa métrica Prometheus `comentarios_adicionados_total{visibility="internal",com_anexo="true"}` |
| 25 | - | Retorna HTTP 201 Created com CommentDto incluindo ID, URL do anexo, timestamp |
| 26 | - | Frontend adiciona novo comentário à timeline em tempo real via SignalR (outros analistas vendo a tela recebem update instantâneo) |
| 27 | - | Exibe toast verde "Comentário interno adicionado com sucesso" |

### 5. Fluxos Alternativos

**FA01: Comentário Externo (Visível ao Cliente)**
- Passo 11: Analista seleciona Visibilidade = Externo
- Passo 22: Sistema detecta Visibility=External
- Sistema envia notificação para solicitante do chamado: E-mail "Novo comentário no Chamado #9876" com texto completo, link para acessar chamado
- Sistema envia notificação in-app para solicitante com badge +1
- Cliente acessa chamado e visualiza comentário na timeline

**FA02: Solicitante Adiciona Comentário (Sempre Externo)**
- Passo 2: Usuário logado é solicitante (não analista), possui permissão `chamado:comentar:proprio`
- Passo 9: Frontend NÃO exibe opção "Visibilidade" (solicitantes só podem criar comentários Externos)
- Sistema força Visibility=External automaticamente
- Comentário visível para equipe e para solicitante

**FA03: Upload de Múltiplos Anexos**
- Passo 12: Analista seleciona 3 arquivos: "Foto1.jpg" (1.2MB), "Foto2.jpg" (1.5MB), "Relatorio.pdf" (2.1MB)
- Sistema valida CADA arquivo individualmente: tamanho ≤5MB ✓, tipo MIME permitido ✓
- Sistema faz upload de 3 arquivos para Azure Blob em paralelo
- Sistema cria 1 comentário com campo AttachmentUrls (array de 3 URLs JSON)

**FA04: Comentário Sem Anexo**
- Passo 12: Analista NÃO anexa arquivo (campo vazio)
- Passo 17-18: Sistema pula upload para Azure Blob
- Comentário criado com AttachmentUrl=null

### 6. Exceções

**EX01: Texto Muito Curto (<5 caracteres)**
- Passo 16: FluentValidation detecta Text="OK" (2 caracteres)
- Sistema retorna HTTP 400 Bad Request "Comentário deve ter mínimo 5 caracteres"
- Frontend exibe mensagem de erro abaixo do textarea

**EX02: Arquivo Muito Grande (>5MB)**
- Passo 13: Arquivo "Video.mp4" possui 12 MB
- Frontend valida tamanho ANTES de upload, bloqueia envio
- Exibe mensagem "Arquivo muito grande. Tamanho máximo: 5 MB"

**EX03: Tipo de Arquivo Não Permitido**
- Passo 13: Arquivo "Script.exe" possui tipo MIME "application/x-msdownload"
- Frontend valida lista de tipos permitidos (pdf, jpg, png, txt, xlsx, docx) e rejeita .exe
- Exibe mensagem "Tipo de arquivo não permitido. Tipos aceitos: PDF, JPG, PNG, TXT, XLSX, DOCX"

**EX04: Falha no Upload Azure Blob (Azure Offline)**
- Passo 17: Azure Blob Storage retorna HTTP 503 Service Unavailable
- Sistema loga erro "Falha upload arquivo Diagnostico_PABX_9876.pdf para Azure Blob: 503"
- Sistema retorna HTTP 500 Internal Server Error "Erro ao fazer upload do anexo. Tente novamente."
- Comentário NÃO é criado (transação rollback)

**EX05: Usuário Tenta Comentar em Chamado de Outro Cliente (Multi-tenancy Violation)**
- Passo 3: Chamado #9876 pertence a ClienteId=123, usuário logado pertence a ClienteId=456
- Sistema detecta violação de multi-tenancy
- Sistema retorna HTTP 403 Forbidden "Você não tem permissão para comentar neste chamado"

### 7. Pós-condições

- Comentário adicionado ao banco de dados (TicketComment entity)
- Anexo(s) uploaded para Azure Blob Storage (se aplicável)
- Auditoria registrada com autor, timestamp, visibilidade
- Notificações enviadas conforme visibilidade (Externo → solicitante + equipe, Interno → apenas equipe)
- Timeline do chamado atualizada em tempo real via SignalR
- Métricas Prometheus incrementadas

### 8. Regras de Negócio Aplicáveis

- RN-CHA-073-07: Comentários Internos vs Externos (Internal apenas equipe, External visível a cliente)
- RN-CHA-073-09: Auditoria de Todas Mudanças (comentários auditados)
- RN-RBAC-013-02: Validação de permissão `chamado:comentar` (analistas) OU `chamado:comentar:proprio` (solicitantes)
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC04: Reabrir Chamado Criando Novo Linkado ao Original

### 1. Descrição

Este caso de uso permite que solicitante ou analista reabra chamado previamente marcado como "Resolvido" quando problema persiste. O sistema NÃO edita chamado original (mantém auditoria histórica), mas fecha original com status "Reaberto" e cria novo chamado linkado via ParentTicketId, copiando contexto relevante (categoria, ativos, prioridade) e recalculando SLA do zero.

### 2. Atores

- Usuário Solicitante (principal - reporta problema persistente)
- Analista de Suporte (pode reabrir em nome do cliente)
- Sistema (fechamento original, criação de novo, recálculo SLA)

### 3. Pré-condições

- Chamado original existe com Status=Resolvido
- Tempo desde resolução ≤30 dias (após 30 dias, criar novo chamado sem link)
- Usuário autenticado possui permissão `chamado:reabrir`

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Solicitante acessa detalhes do Chamado #9876 (resolvido há 2 dias) `/chamados/9876` | - |
| 2 | - | Valida permissão RBAC `chamado:reabrir` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Executa GetTicketDetailsQuery(TicketId=9876) retornando ticket com Status=Resolvido, DataResolucao=2 dias atrás |
| 5 | - | Frontend exibe badge verde "Resolvido" e botão "Reabrir Chamado" (visível se DataResolucao < 30 dias) |
| 6 | Clica "Reabrir Chamado" | - |
| 7 | - | Frontend exibe modal "Reabrir Chamado #9876" com textarea "Por que você está reabrindo este chamado? Descreva o problema." (obrigatório) |
| 8 | Solicitante digita "Problema continua. Após reiniciar PABX hoje, linhas voltaram a cair. Erro persiste." (95 caracteres) | - |
| 9 | Clica "Confirmar Reabertura" | - |
| 10 | - | Executa ReopenTicketCommand com FluentValidation |
| 11 | - | Valida: OriginalTicketId existe ✓, Status=Resolvido ✓, RazaoReabertura mínimo 10 caracteres ✓ |
| 12 | - | Busca chamado original #9876 no banco |
| 13 | - | Atualiza Ticket #9876: Status = Reaberto, DataFechamento = UtcNow |
| 14 | - | Cria novo chamado (Ticket entity) com: |
| 15 | - | - Descricao = "Reabertura: Problema continua. Após reiniciar PABX hoje..." (copia razão + contexto) |
| 16 | - | - ParentTicketId = 9876 (link ao original) |
| 17 | - | - CategoriaId = original.CategoriaId (mesma categoria "Telefonia/PABX/Erro Conectividade") |
| 18 | - | - AtivoIds = original.AtivoIds (mesmos ativos "PABX-Sala001") |
| 19 | - | - Prioridade = original.Prioridade (P3, pode ser alterada pelo sistema se contexto mudou) |
| 20 | - | - SolicitanteId = UsuarioAutenticado (quem reabriu) |
| 21 | - | - Status = Novo |
| 22 | - | - DataCriacao = UtcNow (SLA recalculado do ZERO) |
| 23 | - | Executa SlaCalculator.CalculateSla(novoTicket, contractSla) |
| 24 | - | SLA Resposta: UtcNow + 8h, SLA Resolução: UtcNow + 24h (P3 padrão, NOVO período) |
| 25 | - | Persiste ambas alterações (original + novo) via UnitOfWork em transação |
| 26 | - | Executa SkillBasedRouter.RouteToOptimalTechnician(novoTicket) |
| 27 | - | Roteia para mesma fila QUEUE_TELECOM, seleciona técnico disponível (pode ser diferente do original) |
| 28 | - | Novo ticket #9876-R (sufixo "-R" indica Reabertura) atribuído para Ana (técnico com menor carga atual) |
| 29 | - | Envia notificação para Ana: E-mail "Chamado reabertp #9876-R atribuído - Problema persistente relatado por {SolicitanteNome}", In-app badge +1 |
| 30 | - | Envia notificação para solicitante: "Chamado #9876 reabertp como #9876-R. Novo SLA: Resposta até {hora}, Resolução até {hora}" |
| 31 | - | Envia notificação para Gestor: "Chamado #9876 reabertp - Avaliar se resolução anterior foi adequada (analista original: João)" |
| 32 | - | Registra auditoria com i18n (chave `chamado.reaberto`, TicketOriginalId, NovoTicketId, SolicitanteId, RazaoReabertura, timestamp) |
| 33 | - | Incrementa métrica Prometheus `chamados_reabertos_total{categoria="Telefonia",analista_original="João"}` |
| 34 | - | Analytics identifica padrão: João teve 3 chamados reabertos este mês → sugere revisão de qualidade |
| 35 | - | Retorna HTTP 201 Created com TicketDto do novo chamado #9876-R |
| 36 | - | Redireciona para detalhes do novo chamado `/chamados/9876-R` com mensagem toast amarelo "Chamado reabertp. Novo número: #9876-R" |

### 5. Fluxos Alternativos

**FA01: Reabertura Após 30 Dias (Criar Novo Sem Link)**
- Passo 4: DataResolucao = 35 dias atrás (>30 dias)
- Frontend NÃO exibe botão "Reabrir" no chamado original
- Frontend exibe mensagem "Para reportar problema relacionado a este chamado resolvido há mais de 30 dias, crie um novo chamado."
- Solicitante clica "Criar Novo Chamado" e sistema sugere copiar dados do original mas SEM criar link ParentTicketId

**FA02: Prioridade Aumenta na Reabertura (Problema Recorrente)**
- Passo 19: Sistema detecta que chamado #9876 é a 3ª reabertura do mesmo problema (ParentTicketId → ParentTicketId → ...)
- Sistema automaticamente AUMENTA prioridade: P3 → P2 (problema recorrente indica maior impacto)
- Sistema adiciona comentário automático interno "ATENÇÃO: 3ª reabertura deste problema. Prioridade elevada automaticamente."
- Gestor recebe alerta "Problema recorrente detectado - Chamado #9876 reaberto 3 vezes"

**FA03: Analista Reabrir em Nome do Cliente**
- Passo 1: Analista acessa chamado #9876 (não é solicitante)
- Passo 8: Modal exibe campo adicional "Reabrir em nome de:" com dropdown de usuários
- Analista seleciona solicitante original
- Sistema cria reabertura com SolicitanteId = usuário selecionado (não analista)
- Auditoria registra "Reaberto por Analista {nome} em nome de {solicitante}"

**FA04: Copiar Comentários Relevantes para Novo Chamado**
- Passo 14: Sistema identifica comentários do chamado original marcados como "Importante"
- Sistema copia esses comentários para novo chamado como referência
- Novo chamado inicia com histórico parcial visível

### 6. Exceções

**EX01: Chamado Não Está Resolvido (Status Inválido)**
- Passo 11: Chamado #9876 possui Status=EmAndamento (não Resolvido)
- Sistema retorna HTTP 400 Bad Request "Apenas chamados resolvidos podem ser reabertos. Este chamado ainda está em andamento."
- Frontend exibe mensagem de erro

**EX02: Razão de Reabertura Muito Curta**
- Passo 11: RazaoReabertura="Continua" (8 caracteres, <10 mínimo)
- Sistema retorna HTTP 400 "Descreva o problema com mínimo 10 caracteres"
- Frontend destaca textarea em vermelho

**EX03: Usuário Sem Permissão (Outro Cliente)**
- Passo 3: Chamado #9876 pertence a ClienteId=123, usuário pertence a ClienteId=456
- Sistema detecta violação multi-tenancy
- Sistema retorna HTTP 403 Forbidden "Você não pode reabrir chamados de outros clientes"

**EX04: Falha ao Rotear Novo Chamado (Nenhum Técnico Disponível)**
- Passo 27: QUEUE_TELECOM não possui técnicos disponíveis
- Sistema cria chamado #9876-R mas deixa Status=Novo sem atribuição
- Sistema cria AlertaChamado tipo "FaltaRecursos"
- Gestor recebe notificação para intervir manualmente

### 7. Pós-condições

- Chamado original fechado com Status=Reaberto
- Novo chamado criado e linkado via ParentTicketId
- SLA recalculado do zero para novo chamado
- Novo chamado roteado automaticamente via skill-based routing
- Notificações enviadas para analista atribuído, solicitante e gestor
- Auditoria registrada em ambos chamados (original + novo)
- Métricas de reabertura incrementadas para análise de qualidade
- Analytics identifica padrões de reabertura por analista

### 8. Regras de Negócio Aplicáveis

- RN-CHA-073-08: Reabertura Fecha Original + Cria Novo (mantém auditoria, recalcula SLA)
- RN-CHA-073-03: SLA Recalculado do Zero (novo chamado = novo período SLA)
- RN-CHA-073-05: Atribuição Automática Skill-Based Routing (novo chamado roteado)
- RN-CHA-073-09: Auditoria de Todas Mudanças (reabertura auditada)
- RN-RBAC-013-02: Validação de permissão `chamado:reabrir`
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC05: Sincronizar Chamado Bidirecional com ServiceNow (P1/P2)

### 1. Descrição

Este caso de uso descreve sincronização bidirecional automática entre IControlIT e ServiceNow para chamados críticos (P1/P2). Quando chamado P1/P2 é criado ou atualizado em IControlIT, sistema envia dados para ServiceNow via REST API. Quando ServiceNow atualiza incident, webhook notifica IControlIT que reflete mudanças localmente, mantendo ambos sistemas sincronizados em tempo real.

### 2. Atores

- Sistema (sincronização automática)
- ServiceNow (sistema externo de record)
- Analista (visualiza sincronização transparente)

### 3. Pré-condições

- Integração ServiceNow configurada (endpoint, credenciais, mapeamentos)
- Chamado com Prioridade P1 ou P2
- ServiceNow acessível (API disponível)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Chamado #9876 P1 criado em IControlIT (via UC01) |
| 2 | - | EventHandler detecta TicketCreatedEvent com Prioridade=P1 |
| 3 | - | Verifica RN-CHA-073-10: P1 OR P2 → sincronizar ServiceNow ✓ |
| 4 | - | Dispara SyncTicketToServiceNowCommand via MediatR |
| 5 | - | SyncTicketToServiceNowHandler busca ticket #9876 com Include(Comments, Ativos, SLA) |
| 6 | - | Mapeia IControlIT → ServiceNow usando MapIControlTicketToSnow: |
| 7 | - | - ShortDescription = Ticket.Descricao ("Linhas PABX não completam...") |
| 8 | - | - Priority = MapPriority(P1) → ServiceNow.Priority=1 (Crítico) |
| 9 | - | - Category = "Telefonia" |
| 10 | - | - AssignmentGroup = Ticket.AssignedQueue ("QUEUE_TELECOM") |
| 11 | - | - State = MapStatus(Status.Novo) → ServiceNow.State=1 (Novo) |
| 12 | - | - Caller = Ticket.SolicitanteEmail |
| 13 | - | - Configuration Item = Ticket.AtivoNome ("PABX-Sala001") |
| 14 | - | Executa IServiceNowClient.CreateIncident(snowPayload) via HttpClient REST POST /api/now/table/incident |
| 15 | - | ServiceNow valida payload, cria Incident INC0012345, retorna response com sys_id |
| 16 | - | Atualiza Ticket #9876: ExternalTicketId = "INC0012345", SyncStatus = Sincronizado, LastSyncAt = UtcNow |
| 17 | - | Persiste alteração no banco |
| 18 | - | Registra auditoria com i18n (chave `chamado.servicenow.sincronizado`, TicketId, ExternalTicketId, timestamp) |
| 19 | - | Incrementa métrica Prometheus `servicenow_sync_total{direction="outbound",prioridade="P1"}` |
| 20 | - | 30 minutos depois: Analista em ServiceNow atualiza INC0012345: State=2 (Em Andamento), AssignmentGroup="Network Team" |
| 21 | - | ServiceNow dispara webhook POST https://icontrolit.com/webhook/servicenow com payload JSON |
| 22 | - | IControlIT recebe webhook no endpoint [HttpPost("webhook/servicenow")] |
| 23 | - | Webhook controller valida assinatura HMAC (autenticidade) |
| 24 | - | Dispara SyncTicketFromServiceNowCommand(IncidentNumber="INC0012345", State=2, AssignmentGroup="Network Team") |
| 25 | - | Handler busca ticket local via ExternalTicketId = "INC0012345" |
| 26 | - | Identifica ticket #9876 |
| 27 | - | Mapeia ServiceNow → IControlIT: |
| 28 | - | - State=2 → Status.EmAndamento |
| 29 | - | - AssignmentGroup="Network Team" → busca fila local correspondente, reatribui |
| 30 | - | Atualiza Ticket #9876: Status=EmAndamento, LastSyncAt=UtcNow |
| 31 | - | Adiciona comentário automático interno "Status atualizado via ServiceNow: Em Andamento" |
| 32 | - | Envia notificação in-app para analista atribuído "Chamado #9876 atualizado via ServiceNow - agora Em Andamento" |
| 33 | - | Registra auditoria com i18n (chave `chamado.servicenow.atualizado`, TicketId, mudanças, timestamp) |
| 34 | - | Incrementa métrica Prometheus `servicenow_sync_total{direction="inbound"}` |
| 35 | - | Retorna HTTP 200 OK para webhook ServiceNow confirmando recebimento |

### 5. Fluxos Alternativos

**FA01: Chamado P3/P4 NÃO Sincronizado**
- Passo 3: Ticket possui Prioridade=P3
- Sistema detecta RN-CHA-073-10: P3 NÃO sincroniza ServiceNow
- Handler finaliza sem executar sync
- Ticket permanece apenas no IControlIT

**FA02: Atualização de Comentário Sincronizada**
- Analista adiciona comentário Externo em IControlIT "Solução aplicada, aguardando confirmação"
- Sistema detecta ticket sincronizado (ExternalTicketId preenchido)
- Sistema envia PATCH /api/now/table/incident/{sys_id} atualizando Work Notes
- ServiceNow reflete comentário como nota de trabalho

**FA03: Resolução em ServiceNow Reflete em IControlIT**
- ServiceNow: Analista marca INC0012345 como Resolvido (State=6)
- Webhook notifica IControlIT
- Sistema atualiza Ticket #9876: Status=Resolvido, DataResolucao=UtcNow
- Sistema recalcula SLA para confirmar se foi resolvido dentro do prazo
- Sistema envia e-mail para solicitante "Chamado #9876 foi resolvido"

**FA04: Conflito de Edição (Ambos Sistemas Editados Simultaneamente)**
- IControlIT: Analista atualiza Status=EmAndamento às 10:30:00
- ServiceNow: Analista atualiza State=Resolved às 10:30:05 (quase simultâneo)
- Webhook chega em IControlIT às 10:30:10
- Sistema detecta LastSyncAt=10:30:00 < webhook timestamp 10:30:05
- Sistema aplica regra "Última Escrita Vence" (Last Write Wins)
- Status local sobrescrito para Resolvido
- Sistema adiciona comentário interno "CONFLITO: Status alterado localmente às 10:30, sobrescrito por update ServiceNow às 10:30"
- Alerta enviado para Gestor revisar conflito

### 6. Exceções

**EX01: ServiceNow API Offline (Falha de Conectividade)**
- Passo 14: HttpClient retorna HttpRequestException "Unable to connect to ServiceNow API"
- Sistema loga erro "Falha ao sincronizar Ticket #9876 com ServiceNow: API offline"
- Sistema atualiza Ticket.SyncStatus = FalhaSincronizacao, LastSyncError = "API offline"
- Sistema agenda retry automático via Hangfire (3 tentativas com exponential backoff: 1min, 5min, 15min)
- Se todas tentativas falharem, cria AlertaSincronizacao para Administrador "ServiceNow offline há >20min - tickets P1/P2 não sincronizados"

**EX02: ServiceNow Retorna Erro 400 (Payload Inválido)**
- Passo 14: ServiceNow retorna HTTP 400 Bad Request "Field 'short_description' is required"
- Sistema loga erro "Payload inválido para ServiceNow: {validationErrors}"
- Sistema atualiza SyncStatus = ErroMapeamento
- Sistema envia alerta para DBA "Mapeamento IControlIT→ServiceNow falhou - revisar MapIControlTicketToSnow"

**EX03: Webhook com Assinatura HMAC Inválida (Segurança)**
- Passo 23: HMAC calculado localmente ≠ HMAC do header X-ServiceNow-Signature
- Sistema rejeita webhook como inválido
- Sistema retorna HTTP 401 Unauthorized "Invalid webhook signature"
- Sistema loga tentativa de webhook inválido com IP origem
- Sistema NÃO processa payload (proteção contra ataques)

**EX04: Ticket Local Não Encontrado (ExternalTicketId Órfão)**
- Passo 26: Webhook referencia INC0012345 mas nenhum ticket local possui ExternalTicketId="INC0012345"
- Sistema loga warning "Webhook ServiceNow para incident INC0012345 não encontrado localmente"
- Sistema retorna HTTP 404 Not Found
- ServiceNow pode reenviar webhook (idempotência)

### 7. Pós-condições

- Ticket IControlIT sincronizado com ServiceNow Incident
- ExternalTicketId preenchido criando link bidirecional
- Mudanças em qualquer sistema refletidas no outro
- Auditoria completa de todas sincronizações
- Métricas de sync (outbound/inbound) incrementadas
- Conflitos detectados e registrados
- Retries automáticos em caso de falha

### 8. Regras de Negócio Aplicáveis

- RN-CHA-073-10: Integração ServiceNow para P1/P2 (sincronização bidirecional automática)
- RN-CHA-073-09: Auditoria de Todas Mudanças (sincronizações auditadas)
- RN-MTY-001-01: Multi-tenancy obrigatório

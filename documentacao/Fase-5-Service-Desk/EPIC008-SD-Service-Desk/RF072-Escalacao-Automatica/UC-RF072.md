# UC-RF072 - Casos de Uso - Escalação Automática

## UC01: Configurar Matriz de Escalação Hierárquica Multi-Nível

### 1. Descrição

Este caso de uso permite que Gestor de Service Desk configure matriz de escalação hierárquica para seu cliente, definindo níveis (Helpdesk → Especialista → Senior → Diretor), atribuindo analistas por nível, definindo skills requeridas, SLA máximo por nível e critérios de escalação automática. A matriz é configurável via editor visual drag-and-drop com validação de ciclos e independência multi-tenant.

### 2. Atores

- Gestor de Service Desk (principal)
- Sistema (validação, persistência)

### 3. Pré-condições

- Usuário autenticado com permissão `escalacao:matriz:gerenciar`
- Multi-tenancy ativo (ClienteId válido)
- Mínimo 2 analistas cadastrados no cliente

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Service Desk > Escalação > Matriz de Escalação" | - |
| 2 | - | Valida permissão RBAC `escalacao:matriz:gerenciar` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Executa GetMatrizEscalacaoQuery buscando matriz existente ou template padrão |
| 5 | - | Retorna editor visual hierárquico com níveis atuais (Nível 1→Nível 2→Nível 3) |
| 6 | Clica botão "Adicionar Nível" | - |
| 7 | Preenche: Número do Nível (1-5), Nome ("Nível 2 - Especialista"), Skills requeridas (array de strings), SLA máximo (horas) | - |
| 8 | Arrasta analistas disponíveis da lista lateral para caixa do nível | - |
| 9 | - | Valida em tempo real: mínimo 1 analista por nível, sem ciclos (Nível 1→Nível 2→Nível 1 PROIBIDO), skills existem |
| 10 | - | Exibe preview da árvore com flechas conectando níveis |
| 11 | Define "Próximo Nível" no dropdown (Nível 1 → Nível 2, Nível 2 → Nível 3) | - |
| 12 | Configura critérios de escalação automática por nível: "Se SLA consumido >75% E Prioridade=P1 ENTÃO escala para Nível 3" | - |
| 13 | Clica "Validar Matriz" | - |
| 14 | - | Executa ValidarMatrizEscalacaoCommand (FluentValidation) |
| 15 | - | Valida: sem ciclos, todos níveis conectados, mínimo 2 níveis, máximo 5 níveis, analista não duplicado em mesmo nível |
| 16 | - | Retorna mensagem "Matriz válida - 3 níveis, 12 analistas distribuídos" |
| 17 | Clica "Salvar Matriz" | - |
| 18 | - | Executa AtualizarMatrizEscalacaoCommand |
| 19 | - | Persiste MatrizEscalacao entity com níveis em JSON (NivelEscalacao[]) |
| 20 | - | Registra auditoria com i18n (chave `escalacao.matriz.atualizada`, ClienteId, UsuarioId, timestamp) |
| 21 | - | Invalida cache Redis (chave `matriz-escalacao:{ClienteId}`) |
| 22 | - | Retorna sucesso HTTP 200 com mensagem i18n traduzida |
| 23 | - | Exibe toast verde "Matriz de escalação atualizada com sucesso" |

### 5. Fluxos Alternativos

**FA01: Matriz com Ciclo Detectado**
- Passo 15: Sistema detecta ciclo (Nível 1 → Nível 2 → Nível 1)
- Sistema retorna HTTP 400 com mensagem "Matriz contém ciclo de escalação. Verifique dependências: Nível 1↔Nível 2"
- Frontend exibe alerta vermelho destacando níveis envolvidos no ciclo
- Usuário corrige estrutura, repete validação

**FA02: Mesmo Analista em Múltiplos Níveis (Permitido com Validação)**
- Passo 9: Usuário arrasta João para Nível 1 E Nível 2
- Sistema valida RN-ESC-072-05 (permitido se analista tem skills diferentes em cada nível)
- Sistema exibe aviso amarelo "João está em 2 níveis. Skills Nível 1: [Helpdesk], Skills Nível 2: [Email, VPN]"
- Usuário confirma ou ajusta

**FA03: Importar Matriz de Outro Cliente**
- Passo 6: Usuário clica "Importar de Template"
- Sistema exibe modal com lista de templates (Cliente A, Cliente B, Template Padrão)
- Usuário seleciona template
- Sistema copia estrutura (níveis, skills, critérios) MAS NÃO analistas (específicos por cliente)
- Sistema exibe mensagem "Estrutura importada. Atribua analistas aos níveis."

**FA04: Exportar Matriz para Documentação**
- Após salvar matriz
- Usuário clica "Exportar PDF"
- Sistema gera documento PDF com diagrama da matriz hierárquica, lista de analistas por nível, skills, critérios
- Sistema disponibiliza download

### 6. Exceções

**EX01: Usuário Sem Permissão**
- Passo 2: Usuário não possui permissão `escalacao:matriz:gerenciar`
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem i18n "Acesso negado. Você não tem permissão para gerenciar matriz de escalação."

**EX02: Matriz com Menos de 2 Níveis**
- Passo 15: Validação detecta apenas 1 nível configurado
- Sistema retorna HTTP 400 com mensagem "Matriz deve ter no mínimo 2 níveis (ex: Helpdesk + Especialista)"
- Frontend destaca campo "Número de Níveis" em vermelho

**EX03: Nível Sem Analistas**
- Passo 15: Nível 2 não tem nenhum analista atribuído
- Sistema retorna HTTP 400 com mensagem "Nível 2 (Especialista) não possui analistas. Atribua pelo menos 1 analista."
- Frontend destaca caixa do Nível 2 em vermelho

**EX04: Falha ao Invalidar Cache Redis**
- Passo 21: Conexão com Redis offline
- Sistema loga warning mas NÃO bloqueia salvamento (graceful degradation)
- Matriz salva com sucesso, mas próximas consultas não usam cache até Redis voltar

### 7. Pós-condições

- Matriz de escalação atualizada no banco de dados
- Cache Redis invalidado para forçar reload
- Auditoria registrada com timestamp e usuário
- Triggers de escalação automática utilizam nova matriz imediatamente
- Analistas visualizam nova estrutura no dashboard

### 8. Regras de Negócio Aplicáveis

- RN-ESC-072-05: Matriz Hierárquica Multicliente Independente (cada cliente tem matriz própria, 2-5 níveis, sem ciclos)
- RN-AUD-004-01: Registro de auditoria obrigatório com i18n
- RN-RBAC-013-02: Validação de permissão `escalacao:matriz:gerenciar`
- RN-MTY-001-01: Multi-tenancy obrigatório (ClienteId em todas queries)

---

## UC02: Escalar Chamado Automaticamente por SLA Consumido com Triggers Progressivos

### 1. Descrição

Este caso de uso descreve o processo automático (background job Hangfire) que monitora SLA de chamados ativos e dispara escalação automática quando percentual consumido atinge thresholds configurados (50%, 75%, 90%, 100%). Cada threshold gera escalação para nível superior da matriz, notificando analista via multi-canal (e-mail, SMS, in-app, MS Teams) e registrando auditoria completa.

### 2. Atores

- Sistema (Hangfire Job executado a cada 2 minutos)
- Analista Destino (receptor da escalação)

### 3. Pré-condições

- Hangfire rodando e job VerificarSLAChamadosJob ativo
- Matriz de escalação configurada para o cliente
- Chamado ativo com SLA definido (HorasResposta, HorasResolucao)
- Analistas disponíveis no próximo nível

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara VerificarSLAChamadosJob (recorrente a cada 2 minutos) |
| 2 | - | Executa query buscando chamados ativos com Status=Aberto OU EmAndamento |
| 3 | - | Aplica filtro multi-tenancy (agrupa por ClienteId) |
| 4 | - | Para cada chamado, calcula PercentualSLAConsumido = ((HorasDecorridas / HorasSLA) * 100) |
| 5 | - | Filtra chamados com SLA ≥50% E flag FoiEscaladoEm50=false |
| 6 | - | Identifica 143 chamados que atingiram threshold 50% |
| 7 | - | Para primeiro chamado (ID 9876, P1, SLA 4h, 2h decorridas = 50%): |
| 8 | - | Busca matriz de escalação do ClienteId do chamado |
| 9 | - | Identifica nível atual do analista atribuído (Nível 1 - Helpdesk) |
| 10 | - | Identifica próximo nível conforme matriz (Nível 2 - Especialista) |
| 11 | - | Executa SelecaoEspecialistaOtimo com skills requeridas do chamado (categoria "VPN Cisco" → skills ["Cisco Networking", "VPN"]) |
| 12 | - | Calcula score para 5 analistas Nível 2 disponíveis: Ana (0.92), Bruno (0.78), Carlos (0.65), Diana (0.88), Eduardo (0.45) |
| 13 | - | Seleciona Ana (maior score) como destino da escalação |
| 14 | - | Verifica disponibilidade de Ana: EmPausa=false, ChamadosAtivos=4 (<8 limite) ✓ |
| 15 | - | Executa EscalarAutomaticamenteCommand com parâmetros (ChamadoId=9876, AnalistaDestinoId=Ana, Motivo="SLA consumido em 50%", NivelDestino=Nivel2) |
| 16 | - | Cria registro EscalacaoChamado com timestamp, origem (João), destino (Ana), motivo |
| 17 | - | Atualiza Chamado.AnalistaAtribuidoId = Ana, Chamado.FoiEscaladoEm50 = true |
| 18 | - | Persiste alterações no banco via UnitOfWork |
| 19 | - | Dispara NotificacaoEscalacaoService.EnviarMultiCanalAsync(escalacao, Ana) |
| 20 | - | Envia notificações em paralelo: E-mail SendGrid (10s), SMS Twilio para P1/P2 (12s), In-app badge (5s), MS Teams menção com botões (15s) |
| 21 | - | Registra log de entrega com timestamps de cada canal |
| 22 | - | Agenda timeout de aceite Hangfire: 5min para P1, 15min para P2/P3 (BackgroundJob.Schedule) |
| 23 | - | Registra auditoria com i18n (chave `escalacao.automatica.sla.50`, ClienteId, ChamadoId, AnalistaOrigemId, AnalistaDestinoId, timestamp) |
| 24 | - | Incrementa métrica de monitoramento (Prometheus counter `escalacoes_automaticas_sla_total{nivel="50"}`) |
| 25 | - | Continua processamento para próximo chamado da lista (ID 9877) |
| 26 | - | Após processar todos 143 chamados, job finaliza com log "VerificarSLAChamadosJob concluído: 143 chamados processados, 143 escalações criadas" |

### 5. Fluxos Alternativos

**FA01: SLA Atingiu 75% (Escalação para Nível 3)**
- Passo 5: Chamado já foi escalado em 50%, agora atinge 75% (3h de 4h SLA)
- Sistema identifica FoiEscaladoEm50=true, FoiEscaladoEm75=false
- Sistema busca Nível 3 (Senior) na matriz
- Sistema seleciona melhor especialista Nível 3 com skill-based routing
- Escalação criada com motivo "SLA consumido em 75%"
- Flag FoiEscaladoEm75 = true

**FA02: SLA Atingiu 90% (Escalação para Gestor com Alerta Crítico)**
- Passo 5: Chamado atinge 90% de SLA (3.6h de 4h)
- Sistema identifica threshold crítico
- Sistema busca Nível 4 (Gestor) ou Nível 5 (Diretor) conforme matriz
- Sistema cria AlertaEscalacao com Gravidade=Critica, Mensagem="Chamado #9876 próximo de violação de SLA (90%)"
- Notificação URGENTE enviada via SMS + MS Teams + E-mail para Gestor
- Flag FoiEscaladoEm90 = true

**FA03: SLA Violado 100% (Escalação Emergencial + Registro de Violação)**
- Passo 4: Percentual SLA = 102% (4.08h de 4h)
- Sistema identifica violação de SLA
- Sistema cria AlertaEscalacao com Tipo=ViolacaoSLA, Gravidade=Critica
- Sistema escala IMEDIATAMENTE para Gestor/Diretor ignorando balanceamento de carga (P1 > sobrecarga)
- Sistema registra ViolacaoSLA entity com multa contratual estimada (R$150mil/mês máximo)
- Notificação enviada para Gestor + Diretor + E-mail corporativo do cliente
- Dashboard exibe alerta vermelho piscando

**FA04: Nenhum Analista Disponível no Próximo Nível**
- Passo 14: Todos analistas Nível 2 estão em pausa OU sobrecarregados (≥8 chamados)
- Sistema tenta próximo nível (Nível 3)
- Se Nível 3 também indisponível, escala para Gestor com alerta "Falta de recursos disponíveis"
- Gestor recebe notificação para intervir manualmente (reatribuir ou contratar)

### 6. Exceções

**EX01: Matriz de Escalação Não Configurada**
- Passo 8: ClienteId não possui matriz de escalação
- Sistema loga erro crítico "Matriz de escalação ausente para ClienteId {id}"
- Sistema envia alerta para Administrador do cliente
- Chamado permanece com analista atual, SLA continua consumindo (violação iminente)

**EX02: Falha ao Enviar Notificação (SendGrid Offline)**
- Passo 20: SendGrid retorna HTTP 503 Service Unavailable
- Sistema registra falha no log
- Sistema tenta canais alternativos (SMS, In-app, MS Teams)
- Sistema agenda retry exponencial backoff (3 tentativas: 30s, 2min, 10min)
- Se todas tentativas falharem, registra AlertaEscalacao tipo "Falha de Notificação"

**EX03: Skill-Based Routing Não Encontra Match**
- Passo 12: Nenhum analista Nível 2 possui skills requeridas ("Cisco Networking")
- Sistema reduz threshold de match para 50% (aceita analistas com 1 de 2 skills)
- Se ainda não encontrar, seleciona analista com maior histórico de sucesso geral
- Sistema registra warning "Escalação sem match perfeito de skills" na auditoria

**EX04: Job Hangfire Travado (Timeout >10min)**
- Passo 26: Job não finaliza em tempo razoável (processando >1000 chamados)
- Hangfire cancela job automaticamente após timeout configurado
- Sistema loga erro "VerificarSLAChamadosJob cancelado por timeout"
- Próxima execução (2min) reinicia processamento
- Chamados não processados aguardam próxima iteração

### 7. Pós-condições

- Escalações criadas no banco de dados (EscalacaoChamado entity)
- Chamados reatribuídos para novos analistas
- Notificações multi-canal enviadas com timestamps registrados
- Flags de escalação atualizadas (FoiEscaladoEm50, FoiEscaladoEm75, FoiEscaladoEm90)
- Auditoria completa registrada
- Timeouts de aceite agendados no Hangfire
- Métricas Prometheus incrementadas

### 8. Regras de Negócio Aplicáveis

- RN-ESC-072-01: Escalação Automática por SLA Consumido (50%, 75%, 90%, 100%)
- RN-ESC-072-03: Skill-Based Routing com score composto (skills 40%, histórico 30%, disponibilidade 20%, SLA 10%)
- RN-ESC-072-04: Limite de Carga (máximo 8 chamados por analista)
- RN-ESC-072-06: Auditoria Completa com Retenção 7 Anos
- RN-ESC-072-07: Notificação Multi-Canal (e-mail, SMS, in-app, MS Teams) com garantia <30s
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC03: Aceitar ou Rejeitar Escalação com Tracking de Aceite e Re-escalação

### 1. Descrição

Este caso de uso descreve a interação do analista ao receber notificação de escalação, permitindo 3 ações: (1) Aceitar (assume chamado), (2) Rejeitar com motivo obrigatório (chamado re-escalado para próximo), (3) Aceitar com comentário (aceita mas deixa nota). O sistema rastreia tempo até aceite, motivos de rejeição e dispara timeout automático se analista não responder no prazo (5min para P1, 15min para P2/P3).

### 2. Atores

- Analista Destino (principal - receptor da escalação)
- Sistema (tracking, timeout, re-escalação)

### 3. Pré-condições

- Escalação criada e notificações enviadas (UC02 concluído)
- Analista possui acesso ao sistema (web ou mobile)
- Escalação com Status=Pendente

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Analista Ana recebe notificação MS Teams "[@Ana] Escalação: Chamado #9876 - VPN Cisco (P1)" com 3 botões: ✓Aceitar, ✗Rejeitar, 📄Abrir Chamado | - |
| 2 | Clica botão "✓ Aceitar" no MS Teams | - |
| 3 | - | Intercepta ação via webhook MS Teams, identifica EscalacaoId da mensagem |
| 4 | - | Executa AceitarEscalacaoCommand(EscalacaoId, AnalistaId=Ana, Acao=Aceitar) |
| 5 | - | Valida permissão RBAC `escalacao:aceite:processar` |
| 6 | - | Busca escalação no banco via EscalacaoId |
| 7 | - | Valida que Status=Pendente (ainda não respondida) |
| 8 | - | Atualiza EscalacaoChamado: Status=Aceita, DataAceite=UtcNow, TempoMinutosAteAceite=2.3 |
| 9 | - | Atualiza Chamado: AnalistaAtribuidoId=Ana, Status=EmAndamento, DataInicioAtendimento=UtcNow |
| 10 | - | Cancela job Hangfire de timeout (BackgroundJob.Remove usando IdJobTimeoutAceite) |
| 11 | - | Registra auditoria com i18n (chave `escalacao.aceita`, AnalistaId, EscalacaoId, timestamp) |
| 12 | - | Incrementa métrica Prometheus `escalacoes_aceitas_total{analista="Ana"}` |
| 13 | - | Envia notificação in-app para Analista Origem (João) "Ana aceitou escalação do Chamado #9876" |
| 14 | - | Atualiza badge in-app de Ana: "1 nova atribuição" |
| 15 | - | Retorna HTTP 200 com mensagem "Escalação aceita com sucesso" |
| 16 | - | MS Teams exibe mensagem "✓ Você aceitou a escalação do Chamado #9876" |
| 17 | Analista clica "📄 Abrir Chamado" | - |
| 18 | - | Redireciona para tela de detalhes do Chamado #9876 com histórico de escalação visível |
| 19 | Analista visualiza: Problema="VPN Cisco não conecta", Cliente="Empresa XYZ", Prioridade=P1, Histórico (criado por João 10:00, escalado para Ana 10:32, aceito 10:34) | - |
| 20 | Analista inicia diagnóstico, adiciona comentário "Verificando configuração VPN" | - |
| 21 | - | Registra interação no histórico do chamado |

### 5. Fluxos Alternativos

**FA01: Rejeitar Escalação com Motivo**
- Passo 2: Analista clica "✗ Rejeitar" no MS Teams
- Sistema exibe modal com dropdown de motivos: "Sem skill necessária", "Sobrecarregado (>8 chamados)", "Fora do meu escopo", "Erro de roteamento", "Outro (especifique)"
- Analista seleciona "Sem skill necessária" e adiciona comentário opcional "Não tenho experiência com Cisco"
- Sistema executa RejeitarEscalacaoCommand com motivo
- Sistema atualiza EscalacaoChamado: Status=Rejeitada, MotivoRejeicao="Sem skill necessária", ComentarioRejeicao="Não tenho experiência com Cisco", DataAceite=UtcNow
- Sistema executa EscalarParaProximoAsync: busca próximo analista disponível com skill "Cisco Networking"
- Sistema cria nova escalação para Bruno (segundo melhor score)
- Sistema envia notificações para Bruno via multi-canal
- Sistema registra auditoria com motivo de rejeição
- Sistema incrementa contador `escalacoes_rejeitadas_total{analista="Ana",motivo="SemSkill"}`
- Analytics identifica padrão: Ana rejeitou 8 escalações Cisco em 1 mês → sugere treinamento

**FA02: Aceitar com Comentário**
- Passo 2: Analista clica "✓ Aceitar" mas adiciona comentário
- Sistema exibe campo de texto "Comentário adicional (opcional)"
- Analista digita "Este cliente é complexo, pode demorar. SLA atual 50% consumido."
- Sistema executa AceitarEscalacaoCommand com ComentarioAceite
- Sistema registra comentário no histórico do chamado visível para Gestor
- Aceite processado normalmente (passos 8-21)

**FA03: Timeout Sem Resposta (Rejeição Automática)**
- Passo 1: Analista recebe notificação às 10:30 mas NÃO responde
- Sistema aguarda timeout configurado: 5min para P1, 15min para P2/P3
- Às 10:35 (5min após para P1), Hangfire dispara TimeoutAceiteJob(EscalacaoId)
- Sistema verifica que escalação ainda está Status=Pendente (não respondida)
- Sistema executa RejeitarEscalacaoCommand automaticamente com Motivo="Sem resposta no prazo (timeout automático)"
- Sistema atualiza Status=RejeitadaPorTimeout
- Sistema re-escalação para próximo analista disponível (Bruno)
- Sistema envia notificação para Gestor "Analista Ana não respondeu escalação P1 em 5min - re-escalado para Bruno"
- Sistema incrementa métrica `escalacoes_timeout_total{analista="Ana"}`
- Analytics identifica padrão: Se Ana tem >3 timeouts/mês → Gestor recebe alerta "Revisar disponibilidade de Ana"

**FA04: Nenhum Próximo Analista Disponível (Escala para Gestor)**
- Após rejeição (FA01)
- Sistema busca próximo analista Nível 2 disponível
- Todos analistas Nível 2 estão em pausa OU sobrecarregados
- Sistema escala para Nível 3
- Se Nível 3 também indisponível, escala para Gestor com alerta crítico
- Gestor recebe notificação URGENTE "Chamado #9876 P1 sem recursos disponíveis - intervenção manual necessária"

### 6. Exceções

**EX01: Escalação Já Respondida (Race Condition)**
- Passo 7: Outro sistema (app mobile) já aceitou escalação 2s antes
- Sistema detecta Status=Aceita (não Pendente)
- Sistema retorna HTTP 409 Conflict "Escalação já foi respondida por outro dispositivo"
- MS Teams exibe mensagem "Esta escalação já foi aceita"

**EX02: Usuário Sem Permissão (Analista de Outro Cliente)**
- Passo 5: Analista de ClienteId diferente tenta aceitar escalação
- Sistema valida multi-tenancy: Escalacao.ClienteId ≠ Analista.ClienteId
- Sistema retorna HTTP 403 Forbidden "Você não tem permissão para aceitar esta escalação"

**EX03: Falha ao Cancelar Timeout Hangfire**
- Passo 10: Hangfire offline ou job já disparado (timing exato)
- Sistema loga warning mas NÃO bloqueia aceite
- Timeout job executa mas detecta Status=Aceita, finaliza sem ação
- Aceite processado com sucesso (graceful degradation)

**EX04: Rejeição Sem Motivo (Validação Falha)**
- FA01 Passo 2: Analista clica "Rejeitar" mas não preenche motivo
- Frontend valida campo obrigatório, exibe mensagem "Motivo de rejeição é obrigatório"
- Modal não fecha até motivo ser preenchido

### 7. Pós-condições

- Escalação respondida (Status=Aceita ou Rejeitada)
- Chamado reatribuído para novo analista (se aceito)
- Timeout Hangfire cancelado (se aceito)
- Nova escalação criada para próximo analista (se rejeitado)
- Auditoria registrada com ação, timestamps, motivos
- Métricas Prometheus atualizadas
- Histórico do chamado atualizado com interações
- Notificações enviadas para stakeholders relevantes

### 8. Regras de Negócio Aplicáveis

- RN-ESC-072-09: Aceite de Escalação com 3 opções (Aceitar, Rejeitar com motivo, Aceitar com comentário), timeout 5min (P1) ou 15min (P2/P3)
- RN-ESC-072-06: Auditoria completa com tracking de aceite
- RN-ESC-072-03: Skill-Based Routing para re-escalação
- RN-RBAC-013-02: Validação de permissão `escalacao:aceite:processar`
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC04: Gerenciar Pausas de Escalação com Sincronização Active Directory

### 1. Descrição

Este caso de uso permite que analista registre pausas temporárias (férias, reunião, almoço, ausência) para ser removido de roteamento automático durante período específico. O sistema sincroniza automaticamente com calendário do Active Directory (Outlook) via Microsoft Graph API, criando pausas automáticas para eventos marcados como Busy/Out of Office. Pausas ativas impedem recebimento de novas escalações mas não afetam chamados já atribuídos.

### 2. Atores

- Analista (principal - registra pausa manual)
- Gestor (visualiza pausas da equipe)
- Sistema (sincronização AD, remoção automática de roteamento)

### 3. Pré-condições

- Analista autenticado com permissão `escalacao:pausa:gerenciar`
- Calendário do Active Directory/Outlook configurado
- Microsoft Graph API acessível

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Analista acessa menu "Meu Perfil > Disponibilidade > Gerenciar Pausas" | - |
| 2 | - | Valida permissão RBAC `escalacao:pausa:gerenciar` |
| 3 | - | Executa GetPausasAnalistaQuery(AnalistaId) |
| 4 | - | Retorna lista de pausas ativas e futuras com calendário visual |
| 5 | - | Exibe botão "Sincronizar com Outlook" |
| 6 | Clica "Nova Pausa Manual" | - |
| 7 | Preenche formulário: Tipo (dropdown: Férias, Reunião, Almoço, Ausência Justificada, Outro), Data Início (datepicker), Data Fim (datepicker), Motivo (textarea opcional) | - |
| 8 | Seleciona Tipo="Férias", DataInicio="2025-01-15 00:00", DataFim="2025-01-30 23:59", Motivo="Viagem internacional" | - |
| 9 | - | Valida FluentValidation: DataFim > DataInicio, período máximo 60 dias, sem sobreposição com pausas existentes |
| 10 | - | Exibe preview: "Você ficará indisponível por 15 dias (360 horas). Chamados ativos (3) NÃO serão afetados." |
| 11 | Clica "Confirmar Pausa" | - |
| 12 | - | Executa RegistrarPausaCommand(AnalistaId, DataInicio, DataFim, Tipo, Motivo) |
| 13 | - | Cria registro PausaEscalacao entity no banco |
| 14 | - | Atualiza Analista.EmPausa = true SE DataInicio ≤ UtcNow ≤ DataFim |
| 15 | - | Registra auditoria com i18n (chave `escalacao.pausa.registrada`, AnalistaId, período, tipo) |
| 16 | - | Envia notificação para Gestor da área "Ana estará de férias 15/01-30/01. Redistribuir carga?" |
| 17 | - | Retorna HTTP 200 "Pausa registrada com sucesso" |
| 18 | - | Exibe toast verde "Pausa de 15 dias registrada. Você não receberá novas escalações durante este período." |
| 19 | Analista clica "Sincronizar com Outlook" | - |
| 20 | - | Executa SincronizarComADAsync(AnalistaId) |
| 21 | - | Busca Analista.EmailAD no banco |
| 22 | - | Executa Microsoft Graph API GET /me/calendar/events com filtro ShowAs=Busy OU ShowAs=OutOfOffice para próximos 90 dias |
| 23 | - | Retorna 8 eventos: 3 reuniões (Busy), 1 férias (OutOfOffice), 4 outros |
| 24 | - | Para cada evento: verifica se já existe PausaEscalacao com DataInicio=Event.Start E DataFim=Event.End |
| 25 | - | Identifica 2 eventos novos não registrados: "Budget Review 10:00-11:30 dia 05/01", "Férias Corporativas 20/12-03/01" |
| 26 | - | Cria 2 registros PausaEscalacao com Tipo=SincronizadoAD, Motivo=Event.Subject |
| 27 | - | Retorna resumo "2 pausas sincronizadas do Outlook: 1 reunião, 1 férias" |
| 28 | - | Exibe lista atualizada com 3 pausas (1 manual + 2 sincronizadas) com ícones diferenciados |
| 29 | Job diário Hangfire (SincronizarPausasADJob) executa às 06:00 para TODOS analistas | - |
| 30 | - | Sincroniza calendário de 50 analistas em batch |
| 31 | - | Log "SincronizarPausasADJob concluído: 50 analistas, 120 eventos processados, 18 pausas criadas" |

### 5. Fluxos Alternativos

**FA01: Remoção Automática de Pausa Expirada**
- Job Hangfire RemoverPausasExpiradasJob executa a cada 5 minutos
- Sistema busca pausas com DataFim < UtcNow E Analista.EmPausa = true
- Sistema atualiza Analista.EmPausa = false para 3 analistas
- Sistema envia notificação "Sua pausa expirou. Você voltou ao roteamento automático."
- Analista volta a receber escalações na próxima distribuição

**FA02: Pausa Emergencial (Almoço, Reunião Urgente)**
- Passo 6: Analista clica "Pausa Rápida 1h"
- Sistema cria pausa com DataInicio=UtcNow, DataFim=UtcNow+1h, Tipo=PausaRapida
- Sem validações complexas (processo rápido)
- Pausa ativa imediatamente
- Analista removido de roteamento em <10s

**FA03: Gestor Visualiza Pausas da Equipe**
- Gestor acessa "Service Desk > Equipe > Disponibilidade"
- Sistema executa GetPausasEquipeQuery(FilialId OU DepartamentoId)
- Sistema retorna calendário visual mensal com pausas de todos analistas
- Gestor identifica: 15/01 tem 5 analistas em férias (risco de sobrecarga)
- Gestor planeja contratação temporária ou redistribuição

**FA04: Analista Cancela Pausa Futura**
- Após criar pausa (passo 18)
- Analista clica "Cancelar" na linha da pausa futura
- Sistema valida: pausa ainda não iniciada (DataInicio > UtcNow)
- Sistema remove registro PausaEscalacao
- Sistema envia notificação para Gestor "Ana cancelou férias 15/01-30/01"

### 6. Exceções

**EX01: Sobreposição de Pausas**
- Passo 9: Analista tenta criar pausa 10/01-20/01 mas já tem pausa 15/01-25/01
- Sistema retorna HTTP 400 "Conflito: período 15/01-20/01 já possui pausa ativa"
- Frontend destaca datas em conflito no calendário em vermelho

**EX02: Microsoft Graph API Offline**
- Passo 22: Graph API retorna HTTP 503 Service Unavailable
- Sistema loga erro "Falha ao sincronizar Outlook: Graph API offline"
- Sistema exibe mensagem "Sincronização com Outlook temporariamente indisponível. Tente novamente em 5 minutos."
- Sincronização manual falha mas pausas manuais continuam funcionando

**EX03: Analista Sem E-mail AD Configurado**
- Passo 21: Analista.EmailAD = null (usuário não vinculado ao AD)
- Sistema retorna mensagem "Sincronização com Outlook indisponível. Configure seu e-mail corporativo em Meu Perfil."
- Botão "Sincronizar com Outlook" desabilitado

**EX04: Período de Pausa Muito Longo**
- Passo 9: Analista tenta criar pausa de 90 dias
- Validação FluentValidation: máximo 60 dias
- Sistema retorna HTTP 400 "Período de pausa não pode exceder 60 dias. Divida em múltiplas pausas."

### 7. Pós-condições

- Pausa registrada no banco de dados (PausaEscalacao entity)
- Analista.EmPausa atualizado conforme período ativo
- Auditoria registrada
- Gestor notificado sobre indisponibilidade
- Roteamento automático remove analista de filas durante pausa
- Chamados existentes NÃO são afetados (analista continua responsável)
- Sincronização AD cria pausas automáticas de eventos Busy/OutOfOffice

### 8. Regras de Negócio Aplicáveis

- RN-ESC-072-08: Pausas Integradas com Calendário Corporativo (Microsoft Graph, sincronização automática)
- RN-ESC-072-04: Limite de Carga (analista em pausa não recebe novos chamados)
- RN-RBAC-013-02: Validação de permissão `escalacao:pausa:gerenciar`
- RN-MTY-001-01: Multi-tenancy obrigatório
- RN-AUD-004-01: Auditoria de pausas

---

## UC05: Visualizar Dashboard de Escalações em Tempo Real com Alertas Críticos

### 1. Descrição

Este caso de uso permite que Gestor de Service Desk visualize dashboard em tempo real com métricas de escalações, incluindo: escalações ativas (pendentes de aceite), taxa de aceite por analista, tempo médio de aceitação, trending de escalações por hora, top 5 motivos de escalação/rejeição, alertas críticos (P1 sem aceite >10min, analista rejeitou >5 escalações em 1h, queue vazia com escalações pendentes). Dashboard atualiza via SignalR a cada 1 minuto.

### 2. Atores

- Gestor de Service Desk (principal)
- Sistema (coleta métricas, dispara alertas, SignalR updates)

### 3. Pré-condições

- Usuário autenticado com permissão `escalacao:dashboard:visualizar`
- Matriz de escalação configurada
- Escalações sendo processadas (dados disponíveis)
- SignalR Hub rodando

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa menu "Service Desk > Escalações > Dashboard" | - |
| 2 | - | Valida permissão RBAC `escalacao:dashboard:visualizar` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Executa GetDashboardEscalacoesQuery(ClienteId, Periodo=Hoje) |
| 5 | - | Coleta métricas agregadas via queries otimizadas com índices: |
| 6 | - | - Total escalações hoje: 143 |
| 7 | - | - Escalações pendentes (Status=Pendente): 12 |
| 8 | - | - Taxa geral de aceite: 87% (125 aceitas de 143) |
| 9 | - | - Tempo médio aceitação: 3.2 minutos |
| 10 | - | - Top 5 motivos escalação: SLA 50% (58), SLA 75% (32), Prioridade P1 (28), Skill gap (18), Sobrecarga (7) |
| 11 | - | - Top 5 motivos rejeição: Sem skill (8), Sobrecarregado (5), Fora escopo (3), Erro roteamento (2) |
| 12 | - | - Escalações por analista: Ana (18 recebidas, 16 aceitas, 2 rejeitadas), Bruno (22, 20, 2), Carlos (15, 12, 3) |
| 13 | - | Retorna DashboardEscalacoesDto com todas métricas |
| 14 | - | Frontend renderiza 12 widgets responsivos: |
| 15 | - | 1. Card "Escalações Ativas": 12 (badge vermelho piscando se >10) |
| 16 | - | 2. Card "Taxa de Aceite": 87% (gauge verde se ≥90%, amarelo 80-89%, vermelho <80%) |
| 17 | - | 3. Card "Tempo Médio Aceite": 3.2min (gauge verde se <5min, amarelo 5-10, vermelho >10) |
| 18 | - | 4. Gráfico linha "Trending Escalações/Hora" (últimas 24h): pico 14h (28 escalações), vale 03h (2) |
| 19 | - | 5. Gráfico pizza "Top 5 Motivos Escalação" com percentuais |
| 20 | - | 6. Tabela "Escalações por Analista" com colunas: Nome, Recebidas, Aceitas, Rejeitadas, Taxa Aceite%, Tempo Médio |
| 21 | - | 7. Lista "Escalações Pendentes" com timer countdown (ex: "Chamado #9876 - Ana - Pendente há 4min 23s") |
| 22 | - | 8. Card "Alertas Críticos": 2 alertas ativos |
| 23 | - | Frontend estabelece conexão SignalR com DashboardEscalacoesHub |
| 24 | - | SignalR envia update inicial confirmando conexão |
| 25 | - | SignalR Hub executa job a cada 1 minuto coletando métricas delta |
| 26 | - | Às 14:32: Nova escalação criada (Chamado #9910 para Bruno) |
| 27 | - | SignalR Hub detecta mudança, calcula delta: Escalações Ativas +1 (12→13), Escalações/Hora +1 |
| 28 | - | SignalR Hub envia mensagem `UpdateDashboard` para todos clientes conectados do ClienteId |
| 29 | - | Frontend recebe update via SignalR, atualiza widgets SEM reload: Card "Escalações Ativas" 12→13, som de notificação |
| 30 | - | Lista "Escalações Pendentes" adiciona nova linha "Chamado #9910 - Bruno - Pendente há 00:05" |
| 31 | - | Sistema detecta alerta crítico: P1 Chamado #9876 pendente há >10min |
| 32 | - | Sistema cria AlertaEscalacao: Tipo=P1SemAceite, Gravidade=Critica, Mensagem="Chamado P1 #9876 sem aceite há 11min - Ana" |
| 33 | - | SignalR Hub envia mensagem `NovoAlertaCritico` |
| 34 | - | Frontend exibe modal vermelho piscando "ALERTA: Chamado P1 #9876 sem aceite há 11min" com botões: Intervir, Visualizar Chamado |
| 35 | Gestor clica "Intervir" | - |
| 36 | - | Abre modal "Intervenção Manual" com opções: Reatribuir para outro analista, Contatar Ana, Escalar para Diretor |
| 37 | Gestor seleciona "Reatribuir para outro analista" → Bruno | - |
| 38 | - | Executa ReatribuirEscalacaoCommand(EscalacaoId, NovoAnalistaId=Bruno, Motivo="Intervenção Gestor - Ana não respondeu") |
| 39 | - | Escalação original marcada como Cancelada, nova escalação criada para Bruno |
| 40 | - | Notificações enviadas para Bruno via multi-canal |
| 41 | - | Dashboard atualiza: Escalações Pendentes -1 (13→12), Alerta removido |
| 42 | Gestor clica filtro "Período: Última Semana" | - |
| 43 | - | Dashboard recarrega métricas agregadas para 7 dias: 1.246 escalações, 89% aceite, trending semanal |
| 44 | Gestor clica "Exportar PDF" | - |
| 45 | - | Sistema gera relatório PDF com snapshot de métricas, gráficos, lista de alertas, recomendações |
| 46 | - | Download disponibilizado |

### 5. Fluxos Alternativos

**FA01: Filtro por Analista Específico**
- Passo 42: Gestor seleciona filtro "Analista: Ana"
- Dashboard exibe métricas apenas de Ana: 18 escalações recebidas, 16 aceitas (89%), 2 rejeitadas (Sem skill VPN 2x), tempo médio 2.8min
- Gráfico trending de Ana isolado
- Recomendação: "Ana rejeitou 2 escalações VPN. Sugestão: treinamento Cisco Networking"

**FA02: Alerta "Analista Rejeitou >5 Escalações em 1h"**
- Sistema detecta Carlos rejeitou 6 escalações entre 14:00-15:00
- Sistema cria AlertaEscalacao: Tipo=AnalistaRejeitandoMuito, Mensagem="Carlos rejeitou 6 escalações em 1h. Investigar motivo."
- SignalR envia alerta
- Frontend exibe modal amarelo "ATENÇÃO: Carlos está rejeitando muitas escalações. Motivos: Sem skill (4), Sobrecarregado (2)"
- Gestor investiga, descobre Carlos está de fato sobrecarregado (10 chamados ativos)
- Gestor cria pausa temporária para Carlos, redistribui carga

**FA03: Alerta "Queue Vazia com Escalações Pendentes"**
- Sistema detecta 20 escalações pendentes há >15min
- Sistema verifica disponibilidade: TODOS analistas Nível 2 em pausa OU sobrecarregados
- Sistema cria AlertaEscalacao: Tipo=QueueVazia, Gravidade=Critica, Mensagem="20 escalações pendentes sem analistas disponíveis"
- Frontend exibe modal vermelho "CRÍTICO: Falta de recursos. 20 chamados aguardando atribuição."
- Gestor intervém: remove pausa de 2 analistas manualmente, escala 3 chamados P1 para Nível 3

**FA04: Export PowerBI / Excel**
- Passo 44: Gestor clica "Exportar PowerBI"
- Sistema gera arquivo PBIX com dataset de escalações, métricas pré-calculadas, visuals prontos
- Dataset inclui: EscalacaoChamado, Analista, Metricas, Alertas
- Download disponibilizado, Gestor abre em Power BI Desktop para análise avançada

### 6. Exceções

**EX01: SignalR Hub Offline**
- Passo 23: Falha ao conectar SignalR (servidor reiniciado)
- Frontend exibe banner amarelo "Atualizações em tempo real indisponíveis. Recarregando a cada 1min via polling."
- Frontend implementa fallback: poll HTTP GET /api/dashboard a cada 1min
- Dashboard funciona mas sem updates instantâneos

**EX02: Usuário Sem Permissão (Analista Tentando Acessar Dashboard Gestor)**
- Passo 2: Analista (não Gestor) tenta acessar dashboard
- Sistema valida permissão: Analista possui `escalacao:aceite:processar` mas NÃO `escalacao:dashboard:visualizar`
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem "Acesso negado. Dashboard disponível apenas para Gestores."

**EX03: Período Sem Dados**
- Passo 42: Gestor filtra "Período: Mês Passado Dezembro"
- Query retorna 0 escalações (sistema não estava em uso)
- Frontend exibe mensagem "Nenhuma escalação encontrada no período selecionado"
- Widgets exibem valores zerados com mensagem explicativa

**EX04: Timeout em Query Agregada (>10s)**
- Passo 5: Query agregada demora >10s (banco com milhões de registros)
- Sistema cancela query, retorna HTTP 504 Gateway Timeout
- Frontend exibe mensagem "Dashboard temporariamente indisponível. Tente novamente em alguns instantes."
- Sistema loga erro para DBA investigar índices faltantes

### 7. Pós-condições

- Dashboard exibido com métricas atualizadas
- Conexão SignalR estabelecida para updates em tempo real
- Alertas críticos visíveis e acionáveis
- Métricas registradas para análise histórica
- Exports disponibilizados (PDF, PowerBI, Excel)
- Intervenções manuais registradas em auditoria

### 8. Regras de Negócio Aplicáveis

- RN-ESC-072-10: Dashboard Tempo Real com Alertas Críticos (escalações ativas, taxa aceite, tempo médio, trending, top motivos)
- RN-ESC-072-06: Auditoria completa de intervenções
- RN-RBAC-013-02: Validação de permissão `escalacao:dashboard:visualizar`
- RN-MTY-001-01: Multi-tenancy obrigatório
- RN-i18n-005-01: Traduções de métricas e alertas

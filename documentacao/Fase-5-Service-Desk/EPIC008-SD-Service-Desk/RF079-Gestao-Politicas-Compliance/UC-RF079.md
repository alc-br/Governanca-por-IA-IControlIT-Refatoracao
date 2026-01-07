# UC-RF079 - Casos de Uso - Gestão de Políticas e Compliance

**Versão**: 1.0 | **Data**: 2025-12-29
**RF Relacionado**: RF079 - Gestão de Políticas e Compliance
**EPIC**: EPIC008-SD-Service-Desk
**Fase**: Fase 5 - Service Desk

---

## UC01: Criar e Publicar Política Corporativa com Workflow de Aprovação

### 1. Descrição

Permite administrador corporativo criar política corporativa (uso de ativos, telecom, segurança), gerenciar versionamento automático, e conduzir workflow de aprovação multi-nível (Elaboração → Revisão → Aprovada → Publicada) antes de obrigar aceite dos usuários.

### 2. Atores

- Administrador Corporativo (role: ADMIN_CORPORATIVO, cria política)
- Revisor Técnico (role: REVISOR_SEGURANCA, revisa política)
- Diretor/Aprovador (role: DIRETOR, aprova publicação)
- Sistema IControlIT

### 3. Pré-condições

- Usuário autenticado com permissão `politicas:criar`
- Multi-tenancy ativo (ClienteId válido)
- Workflow de aprovação configurado (estados e aprovadores definidos)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/compliance/politicas/nova` | - |
| 2 | - | Valida permissão RBAC `politicas:criar` |
| 3 | - | Exibe formulário: Título (string 100 chars), Descrição (rich text editor), Categoria (dropdown: Segurança, Financeiro, Operacional, Legal), Regulamentação (multi-select: LGPD, SOX, ISO 27001, ISO 20000, ITIL v4) |
| 4 | Preenche Título="Política de Uso de Notebooks", Descrição (rich text com formatação), Categoria="Segurança", Regulamentação=["ISO 27001", "ITIL v4"] | - |
| 5 | Clica em "Salvar Rascunho" | - |
| 6 | - | **Executa CreatePoliticaCommand** que: 1) Cria entidade Politica com Status=Elaboracao, Versao="1.0", DataCriacao=UtcNow, 2) Aplica multi-tenancy ClienteId=CurrentClienteId, 3) Salva no banco |
| 7 | - | Registra auditoria: `POLITICA_CRIADA`, PoliticaId, Titulo, Versao="1.0", Status="Elaboracao", Usuario=CurrentUser |
| 8 | - | Exibe toast de sucesso i18n: "politicas.mensagens.rascunho_salvo" → "Rascunho salvo. Versão 1.0" |
| 9 | Altera Descrição (adiciona parágrafo sobre criptografia de disco) | - |
| 10 | Clica em "Salvar" novamente | - |
| 11 | - | **Executa UpdatePoliticaCommand** que: 1) Detecta mudança significativa (Descricao != anterior), 2) Incrementa versão: Versao="1.1" (minor increment), 3) Cria registro PoliticaHistorico com: VersaoAnterior="1.0", TituloAntigo, DescricaoAntiga, TituloNovo, DescricaoNova, AlteradoPor=CurrentUser, 4) Atualiza Politica |
| 12 | - | Registra em PoliticasHistorico: Versao="1.1", TituloAntigo, DescricaoAntiga, TituloNovo (inalterado), DescricaoNova (com parágrafo novo), StatusAntigo=Elaboracao, StatusNovo=Elaboracao |
| 13 | - | Exibe toast: "Versão atualizada para 1.1. Histórico de mudanças salvo." |
| 14 | Clica em "Enviar para Revisão" | - |
| 15 | - | Abre modal de confirmação: "Enviar Política de Uso de Notebooks v1.1 para revisão? Você não poderá mais editar após esta ação." |
| 16 | Confirma envio | - |
| 17 | - | **Executa DefinirWorkflowAprovacaoPoliticaCommand** com NovoStatus=Revisao |
| 18 | - | Valida transição permitida: Query `TransicoesPoliticasAprovacao WHERE StatusDe=Elaboracao AND StatusPara=Revisao` retorna transição configurada com AprovadorRequerido="ADMIN_CORPORATIVO" |
| 19 | - | Valida permissão do usuário atual: CurrentUser.Perfil.Nome == "ADMIN_CORPORATIVO" OU CurrentUser tem permissão `politicas:enviar_revisao` |
| 20 | - | Registra aprovação em TransicaoPoliticaAprovacao: StatusDe=Elaboracao, StatusPara=Revisao, AprovadoPor=CurrentUser, DataAprovacao=UtcNow, Comentario (opcional) |
| 21 | - | Atualiza Politica: Status=Revisao, congela versionamento (não pode mais alterar sem voltar a Elaboracao) |
| 22 | - | Envia notificação para grupo "REVISOR_SEGURANCA" via SignalR + email SendGrid: "Nova política aguardando revisão: Política de Uso de Notebooks v1.1" |
| 23 | **Revisor Técnico** acessa tela `/compliance/politicas/em-revisao`, visualiza política | - |
| 24 | - | Exibe política em modo leitura com botões: "Aprovar", "Rejeitar", "Solicitar Ajustes" |
| 25 | Revisor clica em "Aprovar" | - |
| 26 | - | Abre modal: Comentário da revisão (opcional): "Aprovado. Política alinhada com ISO 27001." |
| 27 | Revisor confirma aprovação | - |
| 28 | - | **Executa DefinirWorkflowAprovacaoPoliticaCommand** com NovoStatus=Aprovada |
| 29 | - | Valida transição Revisao → Aprovada requer AprovadorRequerido="REVISOR_SEGURANCA" |
| 30 | - | Valida permissão: CurrentUser (revisor) tem perfil "REVISOR_SEGURANCA" |
| 31 | - | Registra aprovação: StatusDe=Revisao, StatusPara=Aprovada, AprovadoPor=RevisorUserId, Comentario="Aprovado. Política alinhada com ISO 27001." |
| 32 | - | Atualiza Politica: Status=Aprovada |
| 33 | - | Envia notificação para grupo "DIRETOR" via SignalR + email: "Política aprovada tecnicamente aguardando autorização final: Política de Uso de Notebooks v1.1" |
| 34 | **Diretor** acessa tela `/compliance/politicas/aprovadas`, visualiza política | - |
| 35 | Diretor clica em "Publicar" | - |
| 36 | - | Abre modal de confirmação: "Publicar Política de Uso de Notebooks v1.1? Todos os usuários serão obrigados a aceitar." |
| 37 | Diretor confirma publicação | - |
| 38 | - | **Executa DefinirWorkflowAprovacaoPoliticaCommand** com NovoStatus=Publicada |
| 39 | - | Valida transição Aprovada → Publicada requer AprovadorRequerido="DIRETOR" |
| 40 | - | Valida permissão: CurrentUser (diretor) tem perfil "DIRETOR" |
| 41 | - | Registra aprovação: StatusDe=Aprovada, StatusPara=Publicada, AprovadoPor=DiretorUserId, DataAprovacao=UtcNow |
| 42 | - | Atualiza Politica: Status=Publicada, DataPublicacao=UtcNow |
| 43 | - | **Publica evento de domínio** `PoliticaPublicadaEvent` com PoliticaId |
| 44 | - | **Handler PoliticaPublicadaEventHandler** consome evento e chama `NotificadorComplianceService.NotificarPoliticaPublicadaAsync` |
| 45 | - | **Para cada usuário do ClienteId**: Envia email SendGrid com assunto "Nova Política Publicada: Política de Uso de Notebooks v1.1", corpo com descrição + link para aceitar política, e notificação in-app via SignalR Hub |
| 46 | - | Exibe badge de notificação no header do frontend para todos os usuários online (SignalR broadcast) |
| 47 | - | Registra auditoria: `POLITICA_PUBLICADA`, PoliticaId, Versao="1.1", DataPublicacao, NotificacoesEnviadas={count} |

### 5. Fluxos Alternativos

**FA01 - Revisor Rejeita Política e Solicita Ajustes**:
- Passo 25: Revisor clica em "Solicitar Ajustes"
- Sistema abre modal: Comentário obrigatório (min 20 chars): "Título ambíguo. Detalhar requisitos de criptografia."
- Revisor confirma rejeição
- Sistema executa DefinirWorkflowAprovacaoPoliticaCommand com NovoStatus=Elaboracao (volta ao status anterior)
- Sistema registra transição reversa: StatusDe=Revisao, StatusPara=Elaboracao, Comentario="Título ambíguo..."
- Sistema envia notificação ao criador original: "Política devolvida para ajustes pelo revisor. Comentário: {comentario}"
- Criador pode editar novamente (versão incrementa para 1.2 ao salvar)
- Retorna ao passo 6 com nova edição

**FA02 - Política Atualizada Após Publicação (Nova Versão Major)**:
- Política já publicada v1.1 com Status=Publicada
- Admin cria "Nova Versão" baseada na política existente
- Sistema cria nova entidade Politica com Versao="2.0" (major increment), Status=Elaboracao, copia Titulo/Descricao de v1.1
- Admin edita descrição significativamente (adiciona nova seção sobre BYOD - Bring Your Own Device)
- Sistema incrementa para Versao="2.1" ao salvar
- Admin envia para revisão → Workflow repete (Elaboração → Revisão → Aprovada → Publicada)
- Ao publicar v2.1: Sistema marca v1.1 como Status=Obsoleta, DataObsolescencia=UtcNow
- Sistema notifica todos os usuários: "Política de Uso de Notebooks foi atualizada para v2.1. Você deve aceitar a nova versão."
- Usuários que já aceitaram v1.1 devem aceitar v2.1 novamente
- Sistema mantém histórico de aceites por versão

**FA03 - Política Excluída (Soft Delete com Auditoria)**:
- Admin acessa tela `/compliance/politicas/{id}`
- Clica em "Excluir Política"
- Sistema valida: Se Status=Publicada, não permite exclusão (apenas obsolescência)
- Se Status=Elaboracao ou Revisao: Sistema abre modal "Confirmar exclusão? Esta ação não pode ser desfeita."
- Admin confirma
- Sistema marca FlExcluido=true (soft delete), NÃO deleta fisicamente
- Sistema registra auditoria: `POLITICA_EXCLUIDA`, PoliticaId, Titulo, Versao, MotivoDExclusao (opcional)
- Sistema mantém registro para rastreabilidade LGPD/SOX
- Política não aparece mais em listagens, mas permanece em queries de auditoria

### 6. Exceções

**EX01 - Usuário Sem Permissão Para Criar Política**:
- Passo 2: Validação RBAC falha (usuário não tem permissão `politicas:criar`)
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem i18n: "permissoes.acesso_negado_politicas"
- Fluxo termina imediatamente

**EX02 - Transição de Workflow Inválida**:
- Passo 18: Admin tenta mudar status direto de Elaboracao para Publicada (pulando Revisão e Aprovada)
- Sistema busca transição em TransicoesPoliticasAprovacao: Query retorna 0 resultados (transição não permitida)
- Sistema lança InvalidOperationException com mensagem "Transição de Elaboracao para Publicada não permitida. Workflow obrigatório: Elaboração → Revisão → Aprovada → Publicada"
- Frontend exibe modal de erro com fluxo permitido
- Fluxo termina sem alterar status

**EX03 - Aprovador Sem Permissão Para Aprovar Transição**:
- Passo 30: Usuário com perfil "ADMIN_CORPORATIVO" tenta aprovar transição Revisao → Aprovada que requer perfil "REVISOR_SEGURANCA"
- Sistema valida CurrentUser.Perfil.Nome != "REVISOR_SEGURANCA"
- Sistema lança ForbiddenAccessException com mensagem "Apenas REVISOR_SEGURANCA pode aprovar esta transição"
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem: "Você não tem permissão para aprovar esta política. Apenas revisores técnicos podem aprovar."
- Fluxo termina sem registrar aprovação

**EX04 - Notificação de Email Falha (SendGrid Indisponível)**:
- Passo 45: Tentativa de enviar email via SendGrid retorna erro 503 (serviço indisponível)
- Sistema registra falha em logs estruturados: `NOTIFICACAO_EMAIL_FALHA`, PoliticaId, Destinatario, ErroDetalhes
- Sistema NÃO bloqueia publicação da política (notificação é secundária)
- Sistema agenda retry automático via Hangfire job: `RetryNotificacoesFalhadasJob` executa em 15 min
- Sistema envia apenas notificação in-app via SignalR (fallback)
- Fluxo continua com política publicada mas notificações parciais
- Admin recebe alerta: "Política publicada mas {X} notificações de email falharam. Verificar SendGrid."

**EX05 - Versionamento Concorrente (Conflito de Edição)**:
- Passo 11: Dois admins editam mesma política simultaneamente
- Admin A salva Versao="1.1" com mudança no Título às 10:00:00
- Admin B (não atualizou tela) salva Versao="1.1" com mudança na Descrição às 10:00:05
- Sistema detecta conflito: rowVersion do EF Core diverge (concurrency token)
- Sistema lança DbUpdateConcurrencyException
- Frontend detecta erro e exibe modal: "Política foi alterada por outro usuário. Recarregar e tentar novamente?"
- Admin B confirma recarga
- Sistema força refresh da página, Admin B vê Versao="1.1" com mudança do Admin A
- Admin B pode editar novamente (versão incrementa para 1.2)
- Fluxo retorna ao passo 9 com dados atualizados

### 7. Pós-condições

- Política criada com versionamento automático (Versao="1.0", "1.1", "2.0"...)
- Histórico completo de mudanças registrado em PoliticasHistorico (rastreabilidade LGPD/SOX)
- Workflow de aprovação multi-nível executado (Elaboração → Revisão → Aprovada → Publicada)
- Todos os aprovadores notificados em cada etapa do workflow
- Política publicada obriga aceite de todos os usuários do ClienteId
- Notificações enviadas via email (SendGrid) e in-app (SignalR) para cada usuário
- Auditoria completa registrada: POLITICA_CRIADA, POLITICA_ATUALIZADA, POLITICA_PUBLICADA, WORKFLOW_APROVACAO

### 8. Regras de Negócio Aplicáveis

- RN-POL-079-01: Versionamento Automático de Políticas
- RN-POL-079-03: Workflow de Aprovação Multi-Nível
- RN-POL-079-08: Notificações de Atualização e Violação

---

## UC02: Aceitar Política Publicada com Rastreamento Completo

### 1. Descrição

Obriga usuário a aceitar política publicada antes de continuar usando funcionalidade específica, rastreando timestamp, IP, User-Agent para conformidade LGPD/SOX, e validando se política já foi aceita anteriormente para evitar duplicatas.

### 2. Atores

- Usuário final (qualquer usuário autenticado)
- Sistema IControlIT

### 3. Pré-condições

- Usuário autenticado
- Pelo menos uma política com Status=Publicada existe para o ClienteId
- Política não foi aceita pelo usuário (sem registro em AceitePoliticas)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Tenta acessar módulo de Ativos (/ativos/listagem) | - |
| 2 | - | **Intercepta request** via middleware `RequirePolicyAcceptanceMiddleware` antes do controller |
| 3 | - | **Executa VerificarRequerAceitePoliticaQuery** para buscar políticas publicadas não aceitas pelo usuário: Query SQL: `SELECT * FROM Politicas WHERE Status='Publicada' AND ClienteId=@ClienteId AND Id NOT IN (SELECT PoliticaId FROM AceitePoliticas WHERE UsuarioId=@UserId AND FlExcluido=false)` |
| 4 | - | Retorna 1 política: "Política de Uso de Ativos v1.2", DataPublicacao=2025-12-20 |
| 5 | - | **Bloqueia acesso ao módulo**, retorna HTTP 403 Forbidden com payload JSON: `{"blocked": true, "reason": "PolicyAcceptanceRequired", "politicaId": "{guid}", "politicaTitulo": "Política de Uso de Ativos"}` |
| 6 | - | **Frontend detecta HTTP 403** com reason="PolicyAcceptanceRequired" e exibe modal fullscreen bloqueador (não pode fechar com ESC ou clicando fora) |
| 7 | - | Modal exibe: Título da política, Descrição completa (rich text renderizado), Checkbox "Li e concordo com os termos desta política", Botão "Aceitar Política" (desabilitado até marcar checkbox), Botão "Sair do Sistema" (única alternativa) |
| 8 | Usuário lê política (scroll até o fim), marca checkbox "Li e concordo" | - |
| 9 | - | Sistema habilita botão "Aceitar Política" |
| 10 | Clica em "Aceitar Política" | - |
| 11 | - | **Frontend executa POST /api/politicas/{id}/aceitar** com PoliticaId no payload |
| 12 | - | **Backend captura metadados do request**: IpAddress=HttpContext.Connection.RemoteIpAddress, UserAgent=Request.Headers["User-Agent"] (ex: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...") |
| 13 | - | **Executa AceitarPoliticaCommand** que: 1) Valida que política existe e Status=Publicada, 2) Verifica se usuário já aceitou anteriormente (duplicata), 3) Cria entidade AceitePolitica |
| 14 | - | Query de validação duplicata: `SELECT * FROM AceitePoliticas WHERE PoliticaId=@PoliticaId AND UsuarioId=@UserId AND FlExcluido=false` |
| 15 | - | **Se já aceitou**: Retorna HTTP 200 OK com aceite existente (idempotência), pula criação |
| 16 | - | **Se não aceitou**: Cria novo registro AceitePolitica com: PoliticaId, UsuarioId=CurrentUserId, DataAceite=UtcNow, IpAddress="192.168.1.100", UserAgent="Mozilla/5.0...", Aceito=true, ClienteId=CurrentClienteId |
| 17 | - | Salva no banco com campos de auditoria automáticos: CreatedBy=CurrentUserId, CreatedAt=UtcNow |
| 18 | - | **Publica evento de domínio** `PoliticaAceitaEvent` com PoliticaId, UsuarioId, DataAceite |
| 19 | - | **Handler PoliticaAceitaEventHandler** consome evento e registra em log de auditoria: `POLITICA_ACEITA`, PoliticaId, UsuarioId, IpAddress, UserAgent, DataAceite |
| 20 | - | Retorna HTTP 200 OK com mensagem i18n: "politicas.mensagens.aceite_confirmado" → "Política aceita com sucesso" |
| 21 | - | **Frontend fecha modal** e libera acesso ao módulo de Ativos |
| 22 | - | Redireciona usuário para URL original solicitada: /ativos/listagem |
| 23 | - | Atualiza badge de notificações no header: decrementa contador de políticas pendentes |

### 5. Fluxos Alternativos

**FA01 - Múltiplas Políticas Pendentes de Aceite**:
- Passo 4: Query retorna 3 políticas publicadas não aceitas: "Política de Segurança v2.0", "Política de Telecom v1.5", "Política LGPD v1.0"
- Sistema exibe modal com lista das 3 políticas em accordion (expandir/colapsar cada uma)
- Usuário deve aceitar TODAS para liberar acesso
- Sistema exibe contador: "Políticas pendentes: 3 de 3"
- Usuário expande primeira política, lê, marca checkbox, clica "Aceitar"
- Sistema registra aceite da primeira, fecha accordion, expande próxima automaticamente
- Contador atualiza: "Políticas pendentes: 2 de 3"
- Repete processo para segunda e terceira
- Após aceitar todas (contador "0 de 3"): Modal fecha automaticamente, acesso liberado
- Sistema registra 3 aceites separados em AceitePoliticas

**FA02 - Usuário Clica em "Sair do Sistema" Sem Aceitar**:
- Passo 8: Usuário não quer aceitar política e clica em "Sair do Sistema"
- Sistema abre modal de confirmação: "Tem certeza? Você não poderá usar o sistema sem aceitar as políticas."
- Usuário confirma saída
- Sistema executa logout: InvalidateAuthToken, redireciona para /login
- Sistema registra em auditoria: `POLITICA_RECUSADA_LOGOUT`, PoliticaId, UsuarioId, DataRecusa=UtcNow
- Sistema NÃO cria registro em AceitePoliticas (sem aceite)
- Próximo login: Processo repete (política pendente ainda obriga aceite)

**FA03 - Aceite com Re-Aceite Periódico (Política Exige Renovação Anual)**:
- Política configurada com campo `RequerReaceitePeriodicoa=true`, `PeriodicidadeDias=365` (anual)
- Usuário aceitou política em 2024-12-29
- Sistema calcula DataProximoAceite=2025-12-29 e salva em AceitePolitica.DataProximoAceite
- Job Hangfire `VerificarReaceitesPendentesJob` executa diariamente às 00:00 UTC
- Job detecta: AceitePolitica com DataProximoAceite < UtcNow (expirou)
- Job marca aceite como "Expirado" (FlExcluido=true OU campo Status=Expirado)
- Job envia notificação ao usuário: "Política de Segurança requer re-aceite anual. Por favor, aceite novamente."
- Próximo acesso: Sistema detecta aceite expirado, bloqueia acesso, força novo aceite
- Novo aceite cria novo registro em AceitePoliticas com DataProximoAceite=2026-12-29

**FA04 - Aceite em Dispositivo Móvel (Detecção de User-Agent Mobile)**:
- Passo 12: UserAgent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15"
- Sistema detecta mobile via regex: `/(iPhone|iPad|Android)/i.test(userAgent)`
- Sistema registra DeviceType="Mobile" em campo adicional de AceitePolitica
- Frontend mobile exibe modal otimizado: Texto maior, scroll vertical, botão grande "Aceitar"
- Processo de aceite idêntico ao desktop
- Auditoria registra DeviceType para rastreabilidade (LGPD exige saber qual dispositivo aceitou)

### 6. Exceções

**EX01 - Política Não Publicada (Status Diferente de Publicada)**:
- Passo 13: Tentativa de aceitar política com Status=Elaboracao ou Status=Revisao
- Sistema valida: Query `WHERE Id=@PoliticaId AND Status='Publicada'` retorna 0 resultados
- Sistema lança EntityNotFoundException com mensagem "Política não encontrada ou não está publicada"
- Sistema retorna HTTP 404 Not Found
- Frontend exibe erro: "Política inválida. Contacte o administrador."
- Fluxo termina sem criar aceite

**EX02 - Request de Aceite Sem IpAddress ou UserAgent (Proxy/VPN Malconfigured)**:
- Passo 12: HttpContext.Connection.RemoteIpAddress retorna null (proxy reverso sem X-Forwarded-For configurado)
- Sistema detecta IpAddress=null
- Sistema usa fallback: IpAddress="0.0.0.0" (placeholder) e registra flag IsProxied=true
- Sistema registra warning em logs: `ACEITE_SEM_IP`, PoliticaId, UsuarioId
- Sistema permite aceite mas marca registro como "Baixa confiabilidade de rastreamento"
- Auditoria registra warning: Aceite sem IP confiável (pode não atender conformidade LGPD em auditoria externa)
- Fluxo continua com aceite registrado

**EX03 - Multi-Tenancy Violado (Tentativa de Aceitar Política de Outro ClienteId)**:
- Passo 13: Usuário malicioso tenta POST /api/politicas/{id}/aceitar com PoliticaId de outro ClienteId
- Sistema busca política: Query `WHERE Id=@PoliticaId AND ClienteId=@ClienteId` (filter multi-tenancy automático)
- Query retorna 0 resultados (política não pertence ao ClienteId do usuário)
- Sistema lança EntityNotFoundException
- Sistema registra tentativa de violação de segurança: `TENTATIVA_ACEITE_CROSS_TENANT`, PoliticaId, UsuarioId, ClienteIdTentado
- Sistema retorna HTTP 404 Not Found (não revela que política existe em outro tenant)
- Fluxo termina sem aceite

**EX04 - Aceite Duplicado Simultâneo (Concorrência)**:
- Passo 14: Dois requests simultâneos de aceite do mesmo usuário para mesma política (double-click acidental)
- Request 1 às 10:00:00.000 executa query duplicata: retorna 0 resultados (ainda não existe)
- Request 2 às 10:00:00.050 executa query duplicata: retorna 0 resultados (Request 1 ainda não commitou)
- Request 1 cria AceitePolitica e commita às 10:00:00.200
- Request 2 tenta criar AceitePolitica às 10:00:00.250
- Banco detecta constraint UNIQUE em (PoliticaId, UsuarioId) ou concurrency token
- EF Core lança DbUpdateException com inner SqlException "Violation of UNIQUE KEY constraint"
- Sistema captura exceção, retorna HTTP 200 OK com mensagem "Política já aceita" (idempotência)
- Sistema registra apenas 1 aceite no banco (Request 1)
- Frontend fecha modal normalmente (Request 2 também retorna sucesso)

**EX05 - Middleware de Política Falha (Exception Não Tratada)**:
- Passo 3: Middleware lança exceção inesperada (ex: NullReferenceException, timeout de banco)
- Sistema captura exceção em global exception handler
- Sistema registra erro crítico em logs: `MIDDLEWARE_POLITICA_FAILURE`, Exception, StackTrace
- Sistema permite acesso TEMPORÁRIO ao módulo (fail-open para não bloquear operação crítica)
- Sistema envia alerta crítico para admin: "Middleware de políticas falhou. Sistema operando sem validação de aceite."
- Sistema agenda retry automático: Próximo request validará novamente
- Fluxo continua com acesso permitido (modo degradado)

### 7. Pós-condições

- Aceite registrado em AceitePoliticas com timestamp, IP e User-Agent para conformidade LGPD/SOX
- Evento PoliticaAceitaEvent publicado e consumido por handler de auditoria
- Auditoria completa: POLITICA_ACEITA com metadados de rastreamento
- Usuário liberado para acessar funcionalidade bloqueada
- Badge de notificações atualizado (decrementa políticas pendentes)
- Multi-tenancy garantido (usuário só aceita políticas do próprio ClienteId)

### 8. Regras de Negócio Aplicáveis

- RN-POL-079-02: Aceite Obrigatório de Políticas Publicadas

---

## UC03: Verificar Conformidade Automática com Regras Configuráveis

### 1. Descrição

Executa job Hangfire diário que verifica conformidade de todos os usuários com políticas publicadas, validando aceites e executando regras SQL configuráveis para detectar violações automáticas (ex: notebooks > 5 anos), gerando alertas e registros de não-conformidade.

### 2. Atores

- Sistema IControlIT (job automático Hangfire)
- Administrador de Compliance (configura regras, investiga violações)

### 3. Pré-condições

- Hangfire configurado e ativo no backend
- Pelo menos uma política com Status=Publicada
- Regras de conformidade automática configuradas em RegrasConformidadeAutomatica
- Job agendado para executar diariamente às 02:00 UTC

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | **Hangfire dispara job** `VerificacaoConformidadeBackgroundJob` às 02:00 UTC |
| 2 | - | Job inicia execução com timeout de 5 minutos (CancellationTokenSource) |
| 3 | - | **Executa VerificadorConformidadeAutomaticaService.VerificarConformidadeAsync** com ClienteId de cada tenant (loop multi-tenant) |
| 4 | - | **ETAPA 1 - Verificar Aceites**: Query busca políticas publicadas: `SELECT * FROM Politicas WHERE ClienteId=@ClienteId AND Status='Publicada' AND FlExcluido=false` |
| 5 | - | Retorna 3 políticas: "Política de Segurança v2.0", "Política de Ativos v1.5", "Política LGPD v1.0" |
| 6 | - | **Para cada política**: Busca todos os usuários do ClienteId: `SELECT * FROM Usuarios WHERE ClienteId=@ClienteId AND FlExcluido=false` |
| 7 | - | Retorna 150 usuários ativos |
| 8 | - | **Para cada combinação (Política x Usuário)**: Verifica se existe aceite: `SELECT * FROM AceitePoliticas WHERE PoliticaId=@PoliticaId AND UsuarioId=@UserId AND FlExcluido=false` |
| 9 | - | Usuário "João Silva" (ID=user-123) não aceitou "Política de Segurança v2.0": aceite não encontrado |
| 10 | - | **Cria registro de verificação** em VerificacaoConformidade: ClienteId, PoliticaId="Política de Segurança", UsuarioId="user-123", EmConformidade=false, MotivoDeSconformidade="Não aceitou política publicada", DataUltimaVerificacao=UtcNow |
| 11 | - | Usuário "Maria Santos" (ID=user-456) aceitou "Política de Segurança v2.0": aceite encontrado com DataAceite=2025-12-25 |
| 12 | - | **Cria registro de verificação** em VerificacaoConformidade: ClienteId, PoliticaId, UsuarioId="user-456", EmConformidade=true, MotivoDeSconformidade=null, DataUltimaVerificacao=UtcNow |
| 13 | - | **Repete passos 8-12** para todas as 450 combinações (3 políticas × 150 usuários) |
| 14 | - | Estatísticas ETAPA 1: 420 conformes, 30 não-conformes (não aceitaram políticas) |
| 15 | - | **ETAPA 2 - Verificar Regras Automáticas**: Query busca regras ativas: `SELECT * FROM RegrasConformidadeAutomatica WHERE ClienteId=@ClienteId AND Ativa=true AND FlExcluido=false` |
| 16 | - | Retorna 2 regras: Regra 1="NOTEBOOK_IDADE_5ANOS" (CondicaoSQL="SELECT UsuarioId FROM Ativos WHERE TipoAtivo='Notebook' AND DATEDIFF(YEAR, DataFabricacao, GETUTCDATE()) > 5"), Regra 2="LINHA_SEM_USO_90DIAS" (CondicaoSQL="SELECT UsuarioId FROM Linhas WHERE UltimoConsumo < DATEADD(DAY, -90, GETUTCDATE())") |
| 17 | - | **Executa Regra 1** (NOTEBOOK_IDADE_5ANOS): Sistema executa SQL `SELECT UsuarioId FROM Ativos WHERE TipoAtivo='Notebook' AND DATEDIFF(YEAR, DataFabricacao, GETUTCDATE()) > 5 AND ClienteId=@ClienteId` |
| 18 | - | Query retorna 5 usuários violadores: user-789, user-101, user-202, user-303, user-404 |
| 19 | - | **Para cada violador**: Cria evento ViolacaoPoliticaDetectadaEvent: PoliticaId (associada à regra), UsuarioId, RegraCodigo="NOTEBOOK_IDADE_5ANOS", MensagemViolacao="Notebook com mais de 5 anos em uso sem autorização", DataDeteccao=UtcNow |
| 20 | - | **Publica evento via MediatR**: `await _mediator.Publish(ViolacaoPoliticaDetectadaEvent)` |
| 21 | - | **Handler ViolacaoPoliticaDetectadaEventHandler** consome evento e: 1) Registra violação em auditoria, 2) Envia notificação ao usuário violador via NotificadorComplianceService.NotificarViolacaoDetectadaAsync |
| 22 | - | **Notificação email SendGrid** enviada ao usuário violador: Assunto="Alerta de Conformidade: Política de Ativos", Corpo="Detectamos que você possui notebook com mais de 5 anos. Por favor, remedie esta situação em até 48 horas." |
| 23 | - | **Notificação email ao gestor** do usuário violador: Assunto="Relatório: Colaborador {Nome} em Não-Conformidade", Corpo="Seu colaborador possui ativo fora de compliance." |
| 24 | - | **Notificação in-app via SignalR** enviada ao usuário: Tipo="ViolacaoDetectada", Badge vermelho no header, Toast "Você está em não-conformidade com Política de Ativos" |
| 25 | - | **Executa Regra 2** (LINHA_SEM_USO_90DIAS): Sistema executa SQL similar |
| 26 | - | Query retorna 2 usuários violadores: user-505, user-606 |
| 27 | - | Repete passos 19-24 para os 2 violadores (eventos, notificações) |
| 28 | - | Estatísticas ETAPA 2: 7 violações automáticas detectadas (5 notebooks + 2 linhas) |
| 29 | - | **Salva todos os registros de verificação** no banco: `await _context.SaveChangesAsync()` com batch de 450 registros VerificacaoConformidade |
| 30 | - | **Registra conclusão do job** em auditoria: `VERIFICACAO_CONFORMIDADE_EXECUTADA`, ClienteId, TotalVerificacoes=450, TotalConformes=420, TotalNaoConformes=30, TotalViolacoesRegras=7, TempoExecucao_ms=45000 |
| 31 | - | **Job finaliza com sucesso**: Hangfire marca como Succeeded, próxima execução agendada para 02:00 UTC do dia seguinte |

### 5. Fluxos Alternativos

**FA01 - Regra SQL Customizada Falha (Syntax Error)**:
- Passo 17: CondicaoSQL contém syntax error: `SELECT UsuarioId FROM Ativos WHERE TipoAtivo='Notebook' AND DATEDIFF(YEAR, DataFabricacao, GETUTCDATE()) > 5` (falta parêntese)
- Sistema tenta executar query: `await _context.Database.SqlQueryRaw<dynamic>(regra.CondicaoSQL)`
- SQL Server retorna SqlException: "Incorrect syntax near ')'"
- Sistema captura exceção no try-catch: `catch (Exception ex)`
- Sistema registra erro em logs estruturados: `REGRA_CONFORMIDADE_FALHA`, RegraId, RegraCodigo, ErroSQL=ex.Message
- Sistema pula esta regra e continua com próxima (não interrompe job inteiro)
- Ao final do job: Sistema envia alerta ao admin: "Regra NOTEBOOK_IDADE_5ANOS falhou. Verificar SQL."
- Admin corrige CondicaoSQL via tela `/admin/compliance/regras/{id}/editar`
- Próxima execução do job: Regra executa corretamente

**FA02 - Exceção de Conformidade Ativa (Violador Tem Exceção Aprovada)**:
- Passo 19: Usuário user-789 tem notebook > 5 anos (violação detectada)
- Antes de criar evento de violação: Sistema verifica se existe exceção ativa: `SELECT * FROM ExcecoesConformidade WHERE UsuarioId='user-789' AND PoliticaId=@PoliticaId AND DataExpiracao > GETUTCDATE() AND FlExcluido=false`
- Query retorna 1 exceção: MotivoExcecao="Aguardando budget para renovação", DataExpiracao=2026-01-15
- Sistema detecta exceção ativa (DataExpiracao > UtcNow)
- Sistema NÃO cria evento de violação
- Sistema registra em VerificacaoConformidade: EmConformidade=true (exceção aprovada), MotivoDeSconformidade="Exceção ativa até 2026-01-15: Aguardando budget"
- Sistema NÃO envia notificação de violação ao usuário
- Fluxo continua sem alerta para este usuário

**FA03 - Exceção Expirada Detectada (Alerta de Expiração)**:
- Durante execução do job: Sistema detecta exceção com DataExpiracao=2025-12-28 (ontem)
- Sistema marca exceção como expirada: FlExcluido=true OU Status=Expirado
- Sistema envia notificação ao usuário: "Exceção de conformidade expirou. Você voltou ao status de não-conformidade."
- Sistema envia notificação ao aprovador original: "Exceção concedida a {Usuario} para {Politica} expirou. Renovar ou aplicar remediação?"
- Sistema registra auditoria: `EXCECAO_CONFORMIDADE_EXPIRADA`, ExcecaoId, UsuarioId, PoliticaId
- Próxima verificação: Usuário aparecerá como violador (sem exceção ativa)

**FA04 - Job Timeout (Execução Excede 5 Minutos)**:
- Passo 13: Processamento de 450 combinações demora >5 minutos (banco lento, muitos usuários)
- CancellationTokenSource timeout dispara após 5 minutos
- Sistema recebe OperationCanceledException
- Sistema interrompe execução imediatamente (não processa regras automáticas ETAPA 2)
- Sistema registra job como PARCIALMENTE_EXECUTADO: `VERIFICACAO_CONFORMIDADE_TIMEOUT`, RegistrosProcessados=300/450, TempoExecucao_ms=300000
- Sistema envia alerta crítico ao admin: "Job de conformidade timeout após 5 min. Verificar performance do banco."
- Hangfire agenda retry automático em 1h (retry policy configurado)
- Admin investiga lentidão, otimiza queries, aumenta timeout para 10 min

### 6. Exceções

**EX01 - Banco de Dados Indisponível Durante Job**:
- Passo 4: Query `SELECT * FROM Politicas` timeout ou retorna SqlException: "A network-related error occurred"
- Sistema captura exceção
- Sistema registra erro crítico: `VERIFICACAO_CONFORMIDADE_DB_FAILURE`, Exception, StackTrace
- Sistema lança exceção para Hangfire
- Hangfire marca job como Failed, agenda retry automático em 15 min (retry policy: 3 tentativas)
- Se falhar 3x: Hangfire marca como Failed permanentemente, envia alerta crítico ao admin
- Admin investiga conectividade do banco, serviço é restaurado
- Próxima execução agendada (02:00 UTC): Job executa normalmente

**EX02 - Regra SQL com SQL Injection (Validação de Segurança)**:
- Admin malicioso tenta criar regra com CondicaoSQL="SELECT UsuarioId FROM Ativos; DROP TABLE Usuarios;--"
- Sistema valida CondicaoSQL antes de salvar: Regex detecta keywords perigosos (DROP, DELETE, UPDATE, INSERT, ALTER)
- Sistema rejeita com HTTP 400 Bad Request: "CondicaoSQL contém comando não permitido. Apenas SELECT é permitido."
- Sistema registra tentativa de SQL injection: `TENTATIVA_SQL_INJECTION`, UsuarioId, CondicaoSQL
- Sistema envia alerta de segurança: "Tentativa de SQL injection detectada na criação de regra de conformidade"
- Regra não é salva, admin malicioso bloqueado

**EX03 - NotificadorComplianceService Falha (SendGrid Offline)**:
- Passo 22: Tentativa de enviar email via SendGrid retorna erro 503
- Sistema captura exceção no try-catch do NotificadorComplianceService
- Sistema registra falha: `NOTIFICACAO_VIOLACAO_FALHA`, VerificacaoId, Destinatario, Erro
- Sistema NÃO interrompe job (notificação é secundária)
- Sistema salva violação em VerificacaoConformidade mesmo sem notificação enviada
- Sistema agenda retry de notificações via Hangfire job `RetryNotificacoesFalhadasJob` em 15 min
- Job continua processando outros violadores
- Admin recebe alerta: "50 notificações de conformidade falharam. Verificar SendGrid."

**EX04 - Multi-Tenancy Violado (Regra Acessa Dados de Outro Cliente)**:
- Passo 17: CondicaoSQL não inclui filtro `AND ClienteId=@ClienteId` (erro de configuração)
- Sistema força injeção de filtro automaticamente: `regra.CondicaoSQL + " AND ClienteId = @ClienteId"`
- Sistema executa query com parâmetro @ClienteId=clienteId atual
- Query retorna apenas violadores do tenant correto
- Sistema registra warning: `REGRA_SEM_FILTRO_TENANT`, RegraId, SqlModificado=true
- Sistema envia alerta ao admin: "Regra {RegraCodigo} não tinha filtro de multi-tenancy. Sistema corrigiu automaticamente."
- Fluxo continua com isolamento garantido

**EX05 - Concorrência de Jobs (Dois Jobs Executam Simultaneamente)**:
- Hangfire configurado com [DisableConcurrentExecution] mas por bug executa 2 jobs simultâneos às 02:00
- Job 1 e Job 2 tentam processar mesmas verificações
- EF Core detecta concorrência ao salvar: rowVersion diverge
- Um dos jobs (Job 2) lança DbUpdateConcurrencyException
- Sistema captura exceção, registra: `VERIFICACAO_CONCORRENCIA_DETECTADA`
- Job 2 aborta execução (Job 1 já salvou verificações)
- Hangfire marca Job 2 como Succeeded (idempotência)
- Sistema envia alerta: "Concorrência de jobs detectada. Verificar configuração [DisableConcurrentExecution]."

### 7. Pós-condições

- Verificações de conformidade registradas em VerificacaoConformidade (1 registro por Política × Usuário)
- Violações automáticas detectadas via regras SQL configuráveis
- Eventos ViolacaoPoliticaDetectadaEvent publicados e consumidos
- Notificações enviadas aos violadores (email + in-app) e gestores
- Auditoria completa: VERIFICACAO_CONFORMIDADE_EXECUTADA com estatísticas
- Dashboard de compliance atualizado com dados frescos (taxa de conformidade recalculada)
- Exceções expiradas marcadas e notificações de expiração enviadas

### 8. Regras de Negócio Aplicáveis

- RN-POL-079-05: Detecção Automática de Não-Conformidade
- RN-POL-079-06: Gestão de Exceções de Conformidade
- RN-POL-079-08: Notificações de Atualização e Violação

---

## UC04: Gerenciar Matriz de Compliance (Políticas × Regulamentações)

### 1. Descrição

Permite administrador de compliance mapear cada política publicada a regulamentações aplicáveis (LGPD, SOX, ISO 27001, ISO 20000, ITIL v4) através de matriz interativa, facilitando demonstração de conformidade em auditorias externas e identificação de gaps regulatórios.

### 2. Atores

- Administrador de Compliance (role: ADMIN_COMPLIANCE)
- Auditor Externo (visualiza matriz para validar conformidade)
- Sistema IControlIT

### 3. Pré-condições

- Usuário autenticado com permissão `compliance:matriz:gerenciar`
- Pelo menos uma política com Status=Publicada
- Regulamentações cadastradas no enum RegulamentacaoTipo
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/compliance/matriz` | - |
| 2 | - | Valida permissão RBAC `compliance:matriz:visualizar` |
| 3 | - | **Executa ObterMatrizComplianceQuery** que busca mapeamentos existentes: `SELECT * FROM MatrizCompliance WHERE ClienteId=@ClienteId AND FlExcluido=false` com JOIN em Politicas e enum Regulamentacao |
| 4 | - | Retorna 10 mapeamentos existentes (ex: "Política de Segurança" → "ISO 27001" Requisito "5.1") |
| 5 | - | **Renderiza matriz interativa** em formato tabela: Linhas=Políticas (15 políticas publicadas), Colunas=Regulamentações (LGPD, SOX, ISO 27001, ISO 20000, ITIL v4), Células=Checkboxes (marcados se mapeamento existe) |
| 6 | - | Células marcadas exibem ícone verde ✓ + tooltip com RequisitoCodigo e StatusConformidade |
| 7 | - | Células vazias exibem checkbox desmarcado + botão "Adicionar Mapeamento" |
| 8 | Admin clica em célula vazia: Política "Política de Ativos v1.5" × Regulamentação "LGPD" | - |
| 9 | - | Abre modal "Adicionar Mapeamento": Campos: Política (pré-preenchida: "Política de Ativos v1.5"), Regulamentação (pré-preenchida: "LGPD"), Requisito Código (input text: ex "Art. 16"), Requisito Descrição (textarea), Status Conformidade (dropdown: "Em Conformidade", "Não-conformista", "Exceção Aprovada") |
| 10 | Admin preenche: RequisitoCodigo="Art. 16", RequisitoDescricao="Direito de apagamento de dados pessoais", StatusConformidade="Em Conformidade" | - |
| 11 | Clica em "Salvar Mapeamento" | - |
| 12 | - | **Executa CriarMatrizComplianceCommand** que: 1) Valida permissão `compliance:matriz:gerenciar`, 2) Valida que política existe e está publicada, 3) Cria MatrizCompliance: PoliticaId, Regulamentacao=LGPD, RequisitoCodigo="Art. 16", RequisitoDescricao="...", StatusConformidade="Em Conformidade", ClienteId, DataUltimaValidacao=UtcNow |
| 13 | - | Salva no banco com campos de auditoria: CreatedBy=CurrentUserId, CreatedAt=UtcNow |
| 14 | - | Registra auditoria: `MATRIZ_COMPLIANCE_CRIADA`, MatrizId, PoliticaId, Regulamentacao="LGPD", RequisitoCodigo="Art. 16" |
| 15 | - | Modal fecha, matriz atualiza em tempo real: Célula (Política de Ativos × LGPD) agora exibe ✓ verde |
| 16 | - | Tooltip ao passar mouse na célula: "LGPD Art. 16: Direito de apagamento | Status: Em Conformidade | Última validação: 29/12/2025" |
| 17 | Admin clica em "Exportar Matriz" (botão no topo da tela) | - |
| 18 | - | **Executa ExportMatrizComplianceCommand** que: 1) Busca todos os mapeamentos do ClienteId, 2) Gera arquivo Excel (.xlsx) com formato: Sheet 1=Matriz completa (políticas × regulamentações), Sheet 2=Detalhes (lista de requisitos por regulamentação), Sheet 3=Gaps (políticas sem mapeamento OU requisitos não cobertos) |
| 19 | - | Download inicia: `matriz_compliance_{ClienteId}_{DataExport}.xlsx` |
| 20 | - | Registra auditoria: `MATRIZ_COMPLIANCE_EXPORTADA`, UsuarioId, DataExport, TotalMapeamentos=15 |
| 21 | **Auditor externo** acessa matriz (read-only) para validar conformidade | - |
| 22 | Auditor filtra por regulamentação: "SOX" | - |
| 23 | - | Matriz atualiza mostrando apenas coluna SOX, identifica 2 políticas mapeadas: "Política de Segregação de Funções" (SOX-404), "Política de Controles Internos" (SOX-302) |
| 24 | Auditor identifica gap: "SOX-404 Avaliação de Controles" não tem política mapeada | - |
| 25 | Auditor anota em relatório: "Gap identificado: SOX-404 sem política correspondente" | - |

### 5. Fluxos Alternativos

**FA01 - Atualizar Status de Conformidade de Mapeamento Existente**:
- Passo 6: Admin clica em célula marcada (Política de Segurança × ISO 27001)
- Sistema abre modal "Editar Mapeamento" com campos pré-preenchidos: RequisitoCodigo="5.1", RequisitoDescricao="...", StatusConformidade="Em Conformidade", DataUltimaValidacao=2025-12-01
- Admin altera StatusConformidade para "Não-conformista" e adiciona comentário: "Auditoria externa detectou falha no controle"
- Clica em "Atualizar"
- Sistema executa UpdateMatrizComplianceCommand: Atualiza StatusConformidade, DataUltimaValidacao=UtcNow
- Sistema registra auditoria: `MATRIZ_COMPLIANCE_ATUALIZADA`, MatrizId, StatusAntigo="Em Conformidade", StatusNovo="Não-conformista"
- Célula atualiza: Ícone muda para ⚠️ amarelo, tooltip exibe "Status: Não-conformista"
- Sistema envia notificação ao Diretor: "Status de conformidade alterado para Não-conformista: ISO 27001 5.1"
- Fluxo termina com matriz atualizada

**FA02 - Identificar Gaps Regulatórios Automaticamente**:
- Admin clica em "Análise de Gaps" (botão no topo)
- Sistema executa AnalisarGapsComplianceQuery que: 1) Lista todos os requisitos obrigatórios de cada regulamentação (hardcoded ou tabela auxiliar), 2) Compara com mapeamentos existentes, 3) Identifica requisitos sem política mapeada
- Sistema retorna: Gap 1="LGPD Art. 37 (Relatório de Impacto)" sem política, Gap 2="SOX-404" sem política, Gap 3="ISO 27001 6.2 (Formação)" sem política
- Sistema exibe modal com lista de gaps: Tabela com colunas: Regulamentação, Requisito Código, Descrição, Ação Recomendada
- Admin clica em "Criar Política para Gap" ao lado de "LGPD Art. 37"
- Sistema redireciona para `/compliance/politicas/nova` com campos pré-preenchidos: Categoria="Legal", Regulamentacao=["LGPD"], Título sugerido="Política de Relatório de Impacto à Proteção de Dados"
- Admin cria política seguindo workflow (UC01)
- Após publicar: Sistema automaticamente cria mapeamento MatrizCompliance para LGPD Art. 37
- Gap é resolvido automaticamente

**FA03 - Visualizar Histórico de Mudanças na Matriz**:
- Admin clica em célula (Política de Segurança × ISO 27001)
- Modal exibe aba adicional "Histórico"
- Sistema busca auditoria: `SELECT * FROM Auditoria WHERE TipoEvento='MATRIZ_COMPLIANCE_*' AND MatrizId=@MatrizId ORDER BY DataHora DESC`
- Exibe timeline: Data 1="2025-11-01 - Criado (Status: Em Conformidade)", Data 2="2025-12-15 - Atualizado (Status: Não-conformista)", Data 3="2025-12-20 - Validação realizada"
- Admin pode ver quem fez cada mudança (UsuarioId), quando e o que mudou
- Fluxo termina com rastreabilidade completa (LGPD/SOX exigem)

### 6. Exceções

**EX01 - Usuário Sem Permissão Para Gerenciar Matriz**:
- Passo 12: Validação RBAC falha (usuário tem apenas `compliance:matriz:visualizar`, não `gerenciar`)
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem: "Você pode visualizar a matriz mas não tem permissão para editá-la."
- Fluxo termina sem criar mapeamento

**EX02 - Tentativa de Mapear Política Não Publicada**:
- Passo 12: Admin tenta mapear política com Status=Elaboracao
- Sistema valida: Query `WHERE PoliticaId=@PoliticaId AND Status='Publicada'` retorna 0 resultados
- Sistema lança BusinessException: "Apenas políticas publicadas podem ser mapeadas na matriz"
- Sistema retorna HTTP 400 Bad Request
- Frontend exibe erro: "Política deve estar publicada antes de ser mapeada"
- Fluxo termina sem criar mapeamento

**EX03 - Mapeamento Duplicado (Mesma Política + Regulamentação + Requisito)**:
- Passo 12: Admin tenta criar mapeamento já existente: Política="Política de Segurança", Regulamentacao=ISO27001, RequisitoCodigo="5.1"
- Sistema valida: Query `WHERE PoliticaId=@PoliticaId AND Regulamentacao=@Regulamentacao AND RequisitoCodigo=@RequisitoCodigo` retorna 1 registro
- Sistema retorna HTTP 409 Conflict
- Frontend exibe mensagem: "Mapeamento já existe. Use 'Editar' para atualizar."
- Fluxo termina sem criar duplicata

**EX04 - Exportação de Matriz Falha (EPPlus/Excel Library Exception)**:
- Passo 18: Tentativa de gerar Excel com EPPlus lança exception (OutOfMemoryException, arquivo corrompido)
- Sistema captura exceção
- Sistema registra erro: `EXPORT_MATRIZ_FALHA`, Exception, StackTrace
- Sistema retorna HTTP 500 Internal Server Error
- Frontend exibe mensagem: "Erro ao gerar arquivo. Tente novamente ou contacte o suporte."
- Sistema envia alerta ao admin técnico: "Exportação de matriz falhou"
- Fluxo termina sem download

**EX05 - Multi-Tenancy Violado (Tentativa de Mapear Política de Outro Cliente)**:
- Passo 12: Tentativa maliciosa de criar mapeamento com PoliticaId de outro ClienteId
- Sistema aplica filtro multi-tenancy: Query `WHERE PoliticaId=@PoliticaId AND ClienteId=@ClienteId`
- Query retorna 0 resultados
- Sistema lança EntityNotFoundException
- Sistema registra tentativa de violação: `TENTATIVA_CROSS_TENANT_MATRIZ`, PoliticaId, UsuarioId
- Sistema retorna HTTP 404 Not Found
- Fluxo termina sem criar mapeamento

### 7. Pós-condições

- Matriz de compliance atualizada com mapeamentos (Políticas × Regulamentações)
- Cada mapeamento rastreado com RequisitoCodigo, RequisitoDescricao, StatusConformidade
- Gaps regulatórios identificados automaticamente (requisitos sem política)
- Auditoria completa: MATRIZ_COMPLIANCE_CRIADA, ATUALIZADA, EXPORTADA
- Arquivo Excel gerado para apresentação em auditorias externas
- Dashboard de compliance atualizado com cobertura regulatória (ex: "ISO 27001: 85% coberta")

### 8. Regras de Negócio Aplicáveis

- RN-POL-079-04: Matriz de Compliance (Políticas x Regulamentações)

---

## UC05: Dashboard de Compliance em Tempo Real com Alertas

### 1. Descrição

Exibe painel visual consolidado com taxa de conformidade geral, conformidade por política, por departamento, violações recentes, exceções próximas de expirar, atualizando em tempo real via SignalR quando verificações de conformidade ou aceites ocorrem.

### 2. Atores

- Gerente de Compliance (role: GERENTE_COMPLIANCE)
- Diretor (role: DIRETOR)
- Sistema IControlIT

### 3. Pré-condições

- Usuário autenticado com permissão `compliance:dashboard:visualizar`
- Verificações de conformidade executadas (job diário VerificacaoConformidadeBackgroundJob)
- SignalR Hub ativo no backend
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/compliance/dashboard` | - |
| 2 | - | Valida permissão RBAC `compliance:dashboard:visualizar` |
| 3 | - | **Conecta ao SignalR Hub**: `await _hubConnection.StartAsync()`, `await _hubConnection.InvokeAsync("JoinGroup", "ComplianceTeam")` |
| 4 | - | **Executa ObterDashboardComplianceQuery** que busca dados agregados de VerificacaoConformidade, AceitePoliticas, ExcecoesConformidade |
| 5 | - | **Query 1 - Taxa Geral**: `SELECT COUNT(CASE WHEN EmConformidade=1 THEN 1 END) * 100.0 / COUNT(*) FROM VerificacoesConformidade WHERE ClienteId=@ClienteId` retorna 87% |
| 6 | - | **Query 2 - Por Política**: Para cada política publicada, conta usuários em conformidade vs não-conformes |
| 7 | - | Retorna: "Política de Segurança" (95% conformidade, verde), "Política de Ativos" (78% conformidade, amarelo), "Política LGPD" (65% conformidade, vermelho) |
| 8 | - | **Query 3 - Violações Recentes**: `SELECT TOP 10 * FROM VerificacoesConformidade WHERE EmConformidade=0 AND DataUltimaVerificacao >= DATEADD(DAY, -7, GETUTCDATE()) ORDER BY DataUltimaVerificacao DESC` |
| 9 | - | Retorna 5 violações: "João Silva - Não aceitou Política de Segurança há 3 dias", "Maria Santos - Notebook > 5 anos há 1 dia"... |
| 10 | - | **Query 4 - Exceções Próximas de Expirar**: `SELECT * FROM ExcecoesConformidade WHERE DataExpiracao BETWEEN GETUTCDATE() AND DATEADD(DAY, 7, GETUTCDATE())` |
| 11 | - | Retorna 2 exceções: "Paulo Costa - Exceção expira em 3 dias", "Ana Lima - Exceção expira em 5 dias" |
| 12 | - | **Renderiza dashboard** com 5 cards principais: Card 1=Taxa Geral (87% - amarelo), Card 2=Conformidade por Política (gráfico de barras horizontal), Card 3=Violações Recentes (lista), Card 4=Exceções Expirando (lista), Card 5=Conformidade por Departamento (gráfico de pizza) |
| 13 | - | Card 1 exibe número grande "87%" com cor amarela (70-90% faixa), ícone ⚠️, texto "420 conformes, 30 não-conformes" |
| 14 | - | Card 2 exibe 3 barras horizontais com cores: Verde="Política de Segurança 95%", Amarelo="Política de Ativos 78%", Vermelho="Política LGPD 65%" |
| 15 | - | Card 3 exibe lista de 5 violações com: Avatar do usuário, Nome, Política violada, Data detecção, Botão "Investigar" |
| 16 | Gerente clica em "Investigar" ao lado de "João Silva - Não aceitou Política de Segurança" | - |
| 17 | - | Abre modal com detalhes: UsuarioId, Email, Departamento, Gestor, Política não aceita, Data da última verificação, Histórico de notificações enviadas (3 emails enviados sem resposta) |
| 18 | - | Modal exibe botões de ação: "Criar Exceção", "Reenviar Notificação", "Contatar Gestor", "Bloquear Acesso" |
| 19 | Gerente clica em "Criar Exceção" | - |
| 20 | - | Abre submodal "Criar Exceção de Conformidade": Campos: Usuário (pré-preenchido: João Silva), Política (Política de Segurança), Motivo (textarea obrigatória), Dias de Validade (input number: 30, 60, 90) |
| 21 | Gerente preenche: Motivo="Funcionário em treinamento de segurança, aceite após conclusão", DiasValidade=30 | - |
| 22 | Clica em "Aprovar Exceção" | - |
| 23 | - | **Executa CriarExcecaoConformidadeCommand** (conforme UC01 FA03): Cria ExcecaoConformidade, publica evento, notifica usuário |
| 24 | - | Modal fecha, dashboard atualiza: Violação de João Silva some da lista (agora tem exceção ativa) |
| 25 | - | Card 1 atualiza: Taxa geral sobe de 87% para 89% (João agora está conforme por exceção) |
| 26 | **Enquanto gerente visualiza dashboard**: Job de verificação executa e detecta nova violação (Maria Santos - Linha sem uso 90 dias) | - |
| 27 | - | **Backend publica evento SignalR**: `await _hubContext.Clients.Group("ComplianceTeam").SendAsync("ViolacaoDetectada", violacaoDto)` |
| 28 | - | **Frontend recebe evento**: `_hubConnection.On<ViolacaoDto>("ViolacaoDetectada", (violacao) => { adicionarViolacaoNaLista(violacao); atualizarContadores(); })` |
| 29 | - | **Dashboard atualiza em tempo real SEM refresh**: Card 3 adiciona nova violação no topo da lista com animação de slide-in |
| 30 | - | **Toast não-intrusivo** aparece: "Nova violação detectada: Maria Santos - Linha sem uso 90 dias" (auto-hide em 5s) |
| 31 | - | Badge de notificações no header incrementa: +1 violação pendente |
| 32 | Gerente clica em "Exportar Relatório de Compliance" | - |
| 33 | - | **Executa ExportRelatorioComplianceCommand**: Gera PDF com: Página 1=Resumo executivo (taxa geral, por política, tendência), Página 2=Violações detalhadas (tabela), Página 3=Exceções ativas (tabela), Página 4=Recomendações |
| 34 | - | Download inicia: `relatorio_compliance_{ClienteId}_{Data}.pdf` |
| 35 | - | Registra auditoria: `RELATORIO_COMPLIANCE_EXPORTADO`, UsuarioId, DataExport |

### 5. Fluxos Alternativos

**FA01 - Filtrar Dashboard por Departamento**:
- Passo 12: Gerente seleciona filtro: Departamento="TI" (dropdown no topo do dashboard)
- Sistema re-executa ObterDashboardComplianceQuery com filtro: `WHERE Departamento='TI'`
- Dashboard atualiza mostrando apenas dados do departamento TI: Taxa=92% (verde), 10 usuários, 1 violação
- Card de conformidade por departamento some (filtro por departamento ativo)
- URL atualiza: `/compliance/dashboard?departamento=TI` (shareable link)
- Fluxo continua com filtro aplicado

**FA02 - Alertas de Taxa de Conformidade Crítica (< 70%)**:
- Passo 13: Sistema detecta que taxa geral caiu para 68% (abaixo do threshold de 70%)
- Sistema dispara alerta crítico: Backend publica evento SignalR `AlertaCriticoCompliance`
- Frontend exibe banner vermelho fixo no topo do dashboard: "⚠️ ALERTA CRÍTICO: Taxa de conformidade abaixo de 70%. Ação imediata necessária."
- Sistema envia email automático ao Diretor: "Taxa de conformidade em 68%. Revisar ações corretivas."
- Banner tem botão "Plano de Ação" que abre wizard de remediação
- Fluxo continua com alerta visível

**FA03 - Drill-Down em Política Específica**:
- Passo 14: Gerente clica na barra "Política LGPD 65%" (vermelho)
- Sistema navega para `/compliance/politicas/{id}/detalhes`
- Tela exibe: Texto completo da política, Lista de usuários em conformidade (verde), Lista de usuários não-conformes (vermelho), Gráfico de tendência (últimos 30 dias), Ações recomendadas
- Gerente identifica que 20 usuários do departamento Vendas não aceitaram
- Gerente clica em "Notificar Todos Não-Conformes"
- Sistema dispara notificações em massa via NotificadorComplianceService
- Fluxo termina com ação corretiva executada

**FA04 - Conexão SignalR Perdida (Reconexão Automática)**:
- Durante passo 26: Conexão SignalR cai por instabilidade de rede
- Frontend detecta desconexão via `_hubConnection.onclose`
- Sistema exibe banner amarelo: "Conexão perdida. Atualizações em tempo real desabilitadas. Tentando reconectar..."
- Sistema tenta reconectar com backoff exponencial: 2s, 4s, 8s
- Após 3ª tentativa: Conexão restabelecida
- Sistema re-executa `JoinGroup("ComplianceTeam")`
- Sistema força atualização de dados: Re-executa ObterDashboardComplianceQuery
- Banner muda para verde: "Reconectado. Atualizações em tempo real restauradas."
- Fluxo continua com conexão ativa

### 6. Exceções

**EX01 - Usuário Sem Permissão Para Visualizar Dashboard**:
- Passo 2: Validação RBAC falha (usuário não tem permissão `compliance:dashboard:visualizar`)
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem: "Acesso negado. Apenas gerentes de compliance podem visualizar este dashboard."
- Fluxo termina imediatamente

**EX02 - Query de Dashboard Timeout (Dados Muito Grandes)**:
- Passo 4: Query `SELECT * FROM VerificacoesConformidade` timeout após 30s (milhões de registros sem índice)
- Sistema detecta SqlException timeout
- Sistema aplica fallback: Força filtro temporal automático `WHERE DataUltimaVerificacao >= DATEADD(DAY, -30, GETUTCDATE())`
- Sistema exibe nota no dashboard: "Exibindo últimos 30 dias. Para períodos maiores, use filtros específicos."
- Dashboard carrega em 3s com filtro aplicado
- Sistema envia alerta ao admin técnico: "Query de dashboard timeout. Otimizar índices."
- Fluxo continua com dados parciais

**EX03 - SignalR Hub Offline (Dashboard Funciona Apenas com Polling)**:
- Passo 3: Tentativa de conectar ao SignalR Hub falha (servidor offline)
- Sistema entra em modo fallback: Ativa polling HTTP a cada 30s
- Sistema exibe banner informativo: "Atualizações em tempo real indisponíveis. Dashboard atualizando a cada 30s."
- A cada 30s: Sistema executa ObterDashboardComplianceQuery e atualiza UI
- Dashboard funciona mas sem atualizações instantâneas
- Fluxo continua com modo degradado

**EX04 - Exportação de Relatório Falha (PDF Generator Exception)**:
- Passo 33: Tentativa de gerar PDF com iTextSharp lança OutOfMemoryException
- Sistema captura exceção
- Sistema registra erro: `EXPORT_RELATORIO_FALHA`, Exception
- Sistema retorna HTTP 500 Internal Server Error
- Frontend exibe mensagem: "Erro ao gerar relatório. Tente reduzir o período ou contacte o suporte."
- Fluxo termina sem download

**EX05 - Multi-Tenancy Violado (Dashboard Mostra Dados de Outro Cliente)**:
- Passo 4: Bug em ObterDashboardComplianceQuery omite filtro `WHERE ClienteId=@ClienteId`
- Query retorna dados de todos os clientes (violação grave)
- Sistema aplica validação secundária: Frontend valida ClienteId de cada registro retornado
- Frontend detecta registros com ClienteId != CurrentClienteId
- Frontend descarta dados inválidos, registra violação de segurança: `DASHBOARD_CROSS_TENANT_DETECTED`
- Sistema envia alerta crítico de segurança ao admin
- Frontend exibe erro: "Erro de segurança detectado. Dashboard recarregado."
- Sistema força logout do usuário como medida de precaução
- Fluxo termina com bloqueio de segurança

### 7. Pós-condições

- Dashboard exibindo taxa de conformidade geral e por política em tempo real
- Violações recentes visíveis com ações corretivas disponíveis
- Exceções próximas de expirar destacadas para ação preventiva
- Atualizações em tempo real via SignalR quando novas violações são detectadas
- Relatório de compliance exportável em PDF para auditorias
- Auditoria completa: DASHBOARD_ACESSADO, RELATORIO_EXPORTADO, EXCECAO_CRIADA

### 8. Regras de Negócio Aplicáveis

- RN-POL-079-07: Dashboard de Compliance em Tempo Real

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-29 | Criação de 5 casos de uso para RF079 - Gestão de Políticas e Compliance | Claude Code |

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code (IControlIT Documentation Agent)
**Revisão**: Pendente de aprovação técnica

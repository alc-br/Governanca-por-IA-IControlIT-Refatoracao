# UC-RF074 - Casos de Uso - Portal Self-Service de Chamados

## UC01: Criar Chamado via Wizard 3-Passos com FAQ Integrada

### 1. Descrição

Este caso de uso permite que usuário final crie chamado através de wizard guiado em 3 passos (Selecionar Categoria/Serviço → Descrever Problema → Confirmar), integrado com base de conhecimento (RF070) que sugere artigos FAQ em tempo real conforme usuário digita, permitindo auto-resolução e reduzindo chamados evitáveis em 20-30%.

### 2. Atores

- Usuário Final (solicitante - principal)
- Sistema (validação, sugestões FAQ, criação chamado)

### 3. Pré-condições

- Usuário autenticado no portal self-service
- Multi-tenancy ativo (ClienteId válido)
- Mínimo 1 categoria de serviço cadastrada (RF021)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa Portal Self-Service `/my-tickets` e clica "Novo Chamado" | - |
| 2 | - | Valida autenticação (usuário logado) |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe wizard passo 1/3 "Selecione o Serviço" |
| 5 | - | Executa GetServicoCategoriaParaTicketQuery buscando categorias ativas do catálogo (RF021) |
| 6 | - | Retorna 8 categorias com ícones: "Internet/Conectividade" (wifi icon), "E-mail" (envelope icon), "Telefonia" (phone icon), "Hardware" (desktop icon), "Software" (window icon), "Acesso/Senha" (key icon), "Impressora" (printer icon), "Outro" (question icon) |
| 7 | - | Frontend renderiza cards responsivos com ícones, nome e breve descrição de cada serviço |
| 8 | Clica card "Internet/Conectividade" | - |
| 9 | - | Valida seleção (ServiceId capturado) |
| 10 | - | Avança para wizard passo 2/3 "Descreva o Problema" |
| 11 | - | Exibe textarea com placeholder "Descreva detalhadamente o problema (mínimo 20 caracteres)" |
| 12 | - | Exibe link destacado "💡 Consulte a FAQ antes de abrir chamado" com atalho (Ctrl+/) |
| 13 | Começa a digitar "Internet está l" | - |
| 14 | - | Após 3 caracteres, dispara SearchFaqArticlesQuery(SearchTerm="Internet está l", CategoryId=ServiceId) com debounce 300ms |
| 15 | - | Busca artigos em RF070 via query: WHERE (Titulo LIKE '%Internet%' OR Conteudo LIKE '%Internet%') AND Ativo=true |
| 16 | - | Retorna 3 artigos sugeridos ordenados por Relevancia: "Como resolver Internet Lenta", "Diagnóstico de Problemas de Conexão", "Configurar Wi-Fi Corporativo" |
| 17 | - | Frontend exibe dropdown de sugestões ABAIXO do textarea em tempo real (overlay flutuante) |
| 18 | Continua digitando "Internet está lenta" (23 caracteres) | - |
| 19 | Clica sugestão "Como resolver Internet Lenta" | - |
| 20 | - | Abre modal com artigo FAQ completo (título, conteúdo formatado, imagens se houver) |
| 21 | Lê artigo FAQ (solução: reiniciar modem/router), tenta aplicar | - |
| 22 | Problema resolvido após reiniciar modem | - |
| 23 | Clica "Problema Resolvido" no modal FAQ | - |
| 24 | - | Registra métrica `faq_resolveu_problema_total{categoria="Internet"}` (analytics de auto-resolução) |
| 25 | - | Exibe mensagem "Que bom que resolvemos! ✓" e fecha wizard SEM criar chamado (economia de recurso) |
| 26 | **FLUXO ALTERNATIVO: Problema NÃO resolvido após FAQ** | - |
| 27 | Fecha modal FAQ clicando "Não Resolveu, Continuar Chamado" | - |
| 28 | - | Volta para textarea do wizard passo 2 com texto já digitado preservado |
| 29 | Finaliza descrição "Internet está lenta mesmo após reiniciar modem. Velocidade <1Mbps." (70 caracteres) | - |
| 30 | Opcionalmente anexa screenshot via drag-and-drop: "speedtest.png" (1.8 MB) | - |
| 31 | - | Frontend valida tamanho ≤5MB ✓, tipo MIME (image/png) ✓, exibe preview thumbnail |
| 32 | Clica "Avançar" | - |
| 33 | - | Valida FluentValidation: Descrição ≥20 chars ✓, Arquivo ≤5MB ✓ |
| 34 | - | Avança para wizard passo 3/3 "Confirme os Detalhes" |
| 35 | - | Exibe resumo: Categoria="Internet/Conectividade", Descrição="Internet está lenta...", Anexo="speedtest.png (1.8 MB)", Preview calculado de SLA "Prazo de resposta: até 8 horas" (baseado em categoria) |
| 36 | Revisa detalhes, clica "Criar Chamado" | - |
| 37 | - | Executa CreateMyTicketCommand via backend |
| 38 | - | Backend valida novamente (Descrição ≥20, ServiceId existe, UserId autenticado) |
| 39 | - | Upload arquivo para Azure Blob Storage container `tickets-selfservice/{ClienteId}/{UserId}/{timestamp}/speedtest.png` |
| 40 | - | Azure Blob executa antivírus ClamAV scan (isClean=true ✓) |
| 41 | - | Azure Blob retorna CDN URL `https://icontrolit.blob.core.windows.net/.../speedtest.png` |
| 42 | - | Cria Ticket entity: UserId=UsuarioAutenticado, ClienteId, ServiceCategoryId, Descrição, AttachmentUrl, Status=Novo, CreatedAt=UtcNow |
| 43 | - | Executa PriorityCalculator (baseado em categoria, usuário): Prioridade=P3 (Internet não-crítico) |
| 44 | - | Executa SlaCalculator: SLA Resposta=8h, Resolução=24h (P3 padrão) |
| 45 | - | Executa SkillBasedRouter: Categoria "Internet" → QUEUE_REDE, seleciona técnico Ana (menor carga) |
| 46 | - | Persiste Ticket + TicketSLA via UnitOfWork |
| 47 | - | Envia notificação para técnico Ana: E-mail SendGrid "Novo chamado self-service #9876", In-app badge +1 |
| 48 | - | Registra auditoria com i18n (chave `ticket.selfservice.criado`, UserId, TicketId, timestamp) |
| 49 | - | Incrementa métrica Prometheus `tickets_selfservice_criados_total{categoria="Internet"}` |
| 50 | - | Retorna HTTP 201 Created com TicketDto incluindo número do chamado #9876 |
| 51 | - | Frontend exibe tela de sucesso animada "✓ Chamado #9876 criado com sucesso!" com botões: "Ver Detalhes", "Criar Outro", "Voltar para Meus Chamados" |
| 52 | - | Envia notificação para usuário via e-mail "Chamado #9876 criado. Prazo resposta: até {hora}. Acompanhe em: [link]" |

### 5. Fluxos Alternativos

**FA01: FAQ Resolve Problema (Não Cria Chamado)**
- Passo 22: Problema resolvido após ler FAQ
- Passo 23: Usuário clica "Problema Resolvido"
- Sistema registra auto-resolução em tabela FaqAutoResolucao (analytics)
- Wizard fecha SEM criar chamado
- Sistema incrementa métrica `chamados_evitados_faq_total{categoria="Internet"}` (economia de 1 chamado)
- Sistema exibe mensagem "Que bom que resolvemos! Se problema retornar, abra novo chamado."

**FA02: Usuário Ignora FAQ e Cria Chamado Direto**
- Passo 12: Usuário NÃO clica link FAQ
- Passo 13-18: Sistema ainda exibe sugestões em dropdown enquanto digita (não-intrusivo)
- Usuário ignora sugestões, continua digitando
- Sistema permite criar chamado normalmente (não força FAQ)

**FA03: Múltiplos Anexos (Extensão Futura)**
- Passo 30: Usuário arrasta 2 arquivos: "speedtest.png" (1.8MB) + "log.txt" (0.5MB)
- Sistema valida CADA arquivo individualmente
- Upload paralelo para Azure Blob
- Ticket.AttachmentUrls = JSON array de 2 URLs

**FA04: Categoria "Outro" Exige Subcategoria Manual**
- Passo 8: Usuário seleciona card "Outro"
- Sistema exibe campo adicional "Especifique a Categoria" (texto livre obrigatório)
- Validação: mínimo 5 caracteres
- Ticket criado com Categoria=Outro, Subcategoria customizada

### 6. Exceções

**EX01: Descrição Muito Curta (<20 caracteres)**
- Passo 33: FluentValidation detecta Descrição="Internet lenta" (14 caracteres)
- Sistema retorna HTTP 400 Bad Request "RN-TKT-074-02: Descrição deve ter mínimo 20 caracteres"
- Frontend exibe mensagem erro inline abaixo do textarea com contador de caracteres "14/20"
- Wizard NÃO avança para passo 3

**EX02: Arquivo Muito Grande (>5MB)**
- Passo 31: Arquivo "video.mp4" possui 12 MB
- Frontend valida tamanho ANTES de upload, bloqueia
- Exibe mensagem "Arquivo muito grande. Tamanho máximo: 5 MB. Seu arquivo: 12 MB"

**EX03: Tipo de Arquivo Não Permitido**
- Passo 31: Arquivo "malware.exe" possui tipo MIME "application/x-msdownload"
- Frontend valida lista permitidos (jpg, png, pdf, log, txt) e rejeita .exe
- Exibe mensagem "Tipo não permitido. Tipos aceitos: JPG, PNG, PDF, LOG, TXT"

**EX04: Antivírus Detecta Malware**
- Passo 40: ClamAV scan retorna isClean=false (vírus detectado)
- Sistema loga alerta crítico "Malware detectado em upload de UserId={id}"
- Sistema retorna HTTP 400 "Arquivo contém ameaça de segurança detectada. Upload bloqueado."
- Frontend exibe mensagem erro sem detalhes técnicos "Não foi possível fazer upload do arquivo. Entre em contato com suporte."

**EX05: Falha Upload Azure Blob (Azure Offline)**
- Passo 39: Azure Blob retorna HTTP 503 Service Unavailable
- Sistema loga erro "Falha upload Azure Blob: 503"
- Sistema agenda retry via Hangfire (3 tentativas exponential backoff)
- Se todas tentativas falharem, cria chamado SEM anexo, adiciona comentário automático interno "Upload de anexo falhou - usuário notificado"
- Sistema exibe mensagem usuário "Chamado criado mas anexo não foi enviado. Você pode anexar depois nos comentários."

### 7. Pós-condições

- Chamado criado no banco (se não resolvido via FAQ)
- Anexo uploaded para Azure Blob (se fornecido)
- Técnico notificado via multi-canal
- Usuário recebe confirmação por e-mail
- Auditoria registrada
- Métricas incrementadas (criação OU auto-resolução FAQ)
- Wizard resetado para nova criação

### 8. Regras de Negócio Aplicáveis

- RN-TKT-074-02: Wizard 3-Passos Obrigatório (Selecionar → Descrever → Confirmar)
- RN-TKT-074-03: Categorias Pré-Carregadas do Catálogo RF021 (cards com ícones)
- RN-TKT-074-04: FAQ Integrada com Busca Tempo Real (sugestões enquanto digita, reduz 20-30% chamados)
- RN-TKT-074-08: Upload com Validação e Antivírus (max 5MB, ClamAV scan, Azure Blob)
- RN-TKT-074-09: Auditoria Completa 7 Anos LGPD (todas ações self-service)
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC02: Visualizar Meus Chamados com Isolamento por Usuário

### 1. Descrição

Este caso de uso permite que usuário final visualize listagem paginada de APENAS seus próprios chamados (isolamento WHERE UserId=CurrentUserId AND ClienteId=CurrentClienteId), exibidos como cards responsivos com status visual colorido, prioridade, SLA countdown timer, e filtros por status/período.

### 2. Atores

- Usuário Final (principal)
- Sistema (filtro isolamento, paginação)

### 3. Pré-condições

- Usuário autenticado no portal self-service
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa Portal Self-Service `/my-tickets` (landing page pós-login) | - |
| 2 | - | Valida autenticação |
| 3 | - | Aplica filtros obrigatórios: UserId=CurrentUserId AND ClienteId=CurrentClienteId |
| 4 | - | Executa GetMyTicketsQuery(PageNumber=1, PageSize=10, Filtros={}) |
| 5 | - | Query SQL: SELECT * FROM Tickets WHERE UserId={id} AND ClienteId={clientId} AND IsDeleted=false ORDER BY CreatedAt DESC LIMIT 10 OFFSET 0 |
| 6 | - | Retorna paginação: TotalCount=23 tickets, Page 1 com 10 tickets |
| 7 | - | Frontend renderiza 10 cards responsivos em grid 2 colunas desktop, 1 coluna mobile |
| 8 | - | Cada card exibe: Número (#9876), Status badge (Novo=azul, EmAndamento=amarelo, Resolvido=verde, Fechado=cinza), Prioridade icon (P1=🔴, P2=🟠, P3=🟡, P4=⚪), Descrição truncada (50 chars + "..."), Data criação relativa ("há 2 horas"), SLA countdown ("Resposta em 6h 23min" OU "Vencido há 1h" vermelho) |
| 9 | - | Exibe filtros no topo: Dropdown "Status: Todos / Novo / Em Andamento / Resolvido / Fechado", Dropdown "Período: Últimos 7 dias / Últimos 30 dias / Este Ano / Todos", Campo busca "Pesquisar descrição" |
| 10 | - | Exibe paginação no rodapé: "Página 1 de 3 (23 total)" com botões Anterior/Próximo desabilitados/habilitados |
| 11 | Aplica filtro: Seleciona "Status: Em Andamento" | - |
| 12 | - | Frontend atualiza query: GetMyTicketsQuery(PageNumber=1, PageSize=10, Filtros={Status="EmAndamento"}) |
| 13 | - | Executa query com WHERE adicional: AND Status='EmAndamento' |
| 14 | - | Retorna 5 tickets filtrados |
| 15 | - | Frontend re-renderiza cards (agora só 5 tickets, paginação escondida pois cabe em 1 página) |
| 16 | Clica card do Ticket #9876 | - |
| 17 | - | Redireciona para `/my-tickets/9876` (tela de detalhes) |

### 5. Fluxos Alternativos

**FA01: Busca Textual na Descrição**
- Passo 11: Usuário digita "internet" no campo busca
- Sistema executa query com WHERE adicional: AND Descricao LIKE '%internet%'
- Retorna apenas tickets com "internet" na descrição
- Highlight do termo buscado nos cards

**FA02: Nenhum Chamado Encontrado**
- Passo 6: Query retorna TotalCount=0 (usuário novo OU filtro muito restritivo)
- Frontend exibe empty state: Ilustração + "Você ainda não possui chamados" + botão "Criar Primeiro Chamado"

**FA03: Scroll Infinito (ao invés de Paginação)**
- Passo 10: Ao scrollar até fim da lista, frontend detecta
- Frontend carrega próxima página automaticamente (lazy load)
- Append novos cards ao final da lista (sem flash de carregamento)

**FA04: Exportar Lista para CSV**
- Usuário clica "Exportar CSV"
- Sistema gera CSV com TODOS tickets do usuário (não só página atual): Número, Status, Prioridade, Descrição, Data Criação, SLA Status
- Download disponibilizado

### 6. Exceções

**EX01: Tentativa de Acessar Chamado de Outro Usuário (Violação Isolamento)**
- Usuário tenta acessar diretamente URL `/my-tickets/999` (chamado de outra pessoa)
- Passo 17: Backend valida ownership: Ticket.UserId ≠ CurrentUserId
- Sistema retorna HTTP 403 Forbidden "RN-TKT-074-01: Acesso negado"
- Frontend exibe mensagem "Você não tem permissão para visualizar este chamado"

**EX02: Token Expirado Durante Navegação**
- Passo 4: JWT token expirou (sessão >2h)
- Backend retorna HTTP 401 Unauthorized
- Frontend intercepta erro, redireciona para login com returnUrl=/my-tickets

**EX03: Multi-tenancy Violation (Usuário Mudou de Cliente)**
- Usuário faz login em ClienteId=123, depois muda para ClienteId=456 (cenário raro: consultor multi-cliente)
- Passo 3: Sistema aplica filtro ClienteId=456 (atual)
- Tickets de ClienteId=123 não aparecem (isolamento por tenant)

### 7. Pós-condições

- Lista de chamados exibida com isolamento garantido
- Filtros aplicados corretamente
- Paginação funcional
- Métricas de visualização registradas (analytics)

### 8. Regras de Negócio Aplicáveis

- RN-TKT-074-01: Isolamento de Dados por Usuário (WHERE UserId=CurrentUserId AND ClienteId=CurrentClienteId)
- RN-MTY-001-01: Multi-tenancy obrigatório
- RN-RBAC-013-02: Validação de permissão (usuário só vê próprios tickets)

---

## UC03: Receber Notificação em Tempo Real via SignalR e Adicionar Comentário Público

### 1. Descrição

Este caso de uso descreve recebimento de notificação em tempo real via SignalR quando técnico adiciona comentário EXTERNO ou muda status do chamado, permitindo que usuário visualize atualização instantaneamente SEM refresh de página, e adicione comentário público de resposta com upload opcional de anexo.

### 2. Atores

- Usuário Final (principal - receptor notificação, adiciona comentário)
- Técnico de Suporte (adiciona comentário/muda status, dispara notificação)
- Sistema (SignalR Hub, validação, upload)

### 3. Pré-condições

- Usuário autenticado e conectado ao SignalR Hub
- Usuário visualizando detalhes de um chamado próprio
- Técnico possui acesso ao chamado (sistema interno RF073)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário está visualizando detalhes do Ticket #9876 em `/my-tickets/9876` | - |
| 2 | - | Frontend estabelece conexão SignalR com TicketHub ao montar componente |
| 3 | - | SignalR autentica via JWT token, registra usuário em grupo específico User:{UserId} |
| 4 | - | Frontend subscreve evento `ReceiveTicketUpdate` do Hub |
| 5 | - | Tela exibe: Descrição, Status atual (EmAndamento), Últimos 3 comentários (2 do técnico Externos, 1 do próprio usuário) |
| 6 | Técnico (em sistema interno RF073) adiciona comentário EXTERNO: "Testamos configuração. Problema está no seu modem. Providenciaremos troca." às 14:30:00 | - |
| 7 | - | Backend RF073 executa AddCommentCommand criando TicketComment entity |
| 8 | - | Backend detecta Visibility=External (visível ao cliente) |
| 9 | - | Backend dispara IHubContext<TicketHub>.Clients.User(ticket.UserId.ToString()).SendAsync("ReceiveTicketUpdate", payload) |
| 10 | - | Payload JSON: { ticketId: 9876, type: "comment", message: "Novo comentário da equipe", timestamp: "2025-12-29T14:30:00Z", commentId: 456 } |
| 11 | - | SignalR Hub envia mensagem via WebSocket para cliente conectado do usuário |
| 12 | - | Frontend recebe evento `ReceiveTicketUpdate` em tempo real (latência <500ms) |
| 13 | - | Angular component executa handler: ticketHub.ticketUpdated$.next(update) |
| 14 | - | Component detecta update.ticketId === this.ticketId (mesmo ticket que está vendo) |
| 15 | - | Component executa this.loadTicket() para buscar dados atualizados do backend |
| 16 | - | Backend retorna ticket com novo comentário incluído |
| 17 | - | Frontend atualiza lista de comentários SEM reload de página (smooth animation) |
| 18 | - | Novo comentário aparece no topo da timeline com badge "Novo" piscando |
| 19 | - | Frontend exibe toast notification no canto "💬 Novo comentário da equipe no Chamado #9876" |
| 20 | - | Se usuário estava em outra aba, Service Worker dispara browser notification "IControlIT: Novo comentário no seu chamado" |
| 21 | Usuário lê comentário "Testamos configuração. Problema está no seu modem. Providenciaremos troca." | - |
| 22 | Decide responder, clica botão "Adicionar Comentário" abaixo da timeline | - |
| 23 | - | Frontend expande formulário inline com textarea "Seu comentário" e botão upload "Anexar arquivo" |
| 24 | Digita resposta "Ok, obrigado! Quando será a troca do modem?" (48 caracteres) | - |
| 25 | - | Frontend valida em tempo real: contador de caracteres "48/2000", botão "Enviar" habilitado se ≥5 chars |
| 26 | Clica "Enviar" | - |
| 27 | - | Frontend executa AddMyCommentCommand via HTTP POST /api/my-tickets/9876/comments |
| 28 | - | Backend valida: Ticket ownership (UserId=CurrentUserId ✓), Texto ≥5 chars ✓ |
| 29 | - | Backend cria TicketComment entity: TicketId=9876, UserId=CurrentUserId, Text="Ok, obrigado!...", Visibility=External (sempre External para usuários finais), CreatedAt=UtcNow |
| 30 | - | Backend persiste comentário no banco |
| 31 | - | Backend dispara notificação in-app para técnico atribuído (Ana): Badge +1 "Usuário respondeu no Chamado #9876" |
| 32 | - | Backend registra auditoria com i18n (chave `ticket.selfservice.comentario.adicionado`) |
| 33 | - | Backend retorna HTTP 201 Created com CommentDto |
| 34 | - | Frontend adiciona comentário à timeline imediatamente (optimistic UI update) |
| 35 | - | Exibe toast verde "✓ Comentário adicionado" |
| 36 | - | Formulário de comentário recolhe automaticamente, limpo para próximo |

### 5. Fluxos Alternativos

**FA01: Técnico Muda Status (SignalR Notifica Mudança de Status)**
- Passo 6: Técnico muda Status=EmAndamento → Resolvido às 15:00
- Passo 9: Payload JSON: { ticketId: 9876, type: "status_change", message: "Seu chamado foi resolvido", newStatus: "Resolvido" }
- Passo 17: Frontend atualiza badge de status (amarelo → verde) com animação
- Passo 19: Toast notification "✓ Chamado #9876 marcado como Resolvido"
- Passo 20+: Sistema exibe CSAT inline popup (UC04)

**FA02: Comentário com Anexo**
- Passo 24: Usuário anexa foto via drag-and-drop "foto_modem.jpg" (2.1 MB)
- Frontend valida tamanho ≤5MB ✓, tipo MIME (image/jpeg) ✓
- Passo 28: Backend faz upload para Azure Blob, scan antivírus ClamAV
- TicketComment criado com AttachmentUrl preenchido
- Timeline exibe comentário com thumbnail clicável da imagem

**FA03: Múltiplas Notificações Simultâneas (Batch)**
- Passo 6: Técnico adiciona 3 comentários seguidos + muda status (4 eventos em 10 segundos)
- SignalR envia 4 mensagens separadas ao frontend
- Frontend implementa debounce: agrupa updates, executa loadTicket() UMA vez após 500ms
- Evita múltiplos reloads desnecessários

**FA04: Comentário Interno NÃO Notifica Usuário**
- Passo 6: Técnico adiciona comentário INTERNO "Aguardando peça ETA 30 dias"
- Passo 8: Backend detecta Visibility=Internal
- SignalR NÃO envia mensagem para usuário (só para outros técnicos)
- Usuário não vê comentário interno nem recebe notificação

### 6. Exceções

**EX01: SignalR Desconectado (Usuário Offline Temporário)**
- Passo 11: SignalR Hub tenta enviar mas usuário offline (WebSocket fechado)
- SignalR registra falha, mensagem não entregue em tempo real
- Quando usuário reconectar, frontend executa sync manual via polling: GET /api/my-tickets/9876/updates-since?timestamp={lastSync}
- Backend retorna updates perdidos, frontend processa

**EX02: Tentativa de Adicionar Comentário em Ticket Fechado**
- Passo 28: Ticket possui Status=Fechado (não permite mais comentários)
- Backend retorna HTTP 400 Bad Request "Não é possível adicionar comentários em chamados fechados"
- Frontend exibe mensagem erro, desabilita formulário de comentário

**EX03: Texto Muito Curto (<5 caracteres)**
- Passo 28: FluentValidation detecta Text="Ok" (2 caracteres)
- Backend retorna HTTP 400 "Comentário deve ter mínimo 5 caracteres"
- Frontend exibe mensagem inline abaixo textarea

**EX04: Falha Upload Azure Blob**
- FA02 Passo upload: Azure Blob retorna HTTP 503
- Sistema agenda retry Hangfire, cria comentário SEM anexo
- Adiciona nota automática "Upload de anexo falhou - tente novamente"
- Frontend exibe mensagem "Comentário adicionado mas anexo não foi enviado. Tente anexar novamente."

### 7. Pós-condições

- Notificação recebida em tempo real via SignalR
- Timeline de comentários atualizada sem refresh
- Comentário do usuário adicionado e visível para equipe
- Técnico notificado de resposta do usuário
- Auditoria registrada
- Service Worker pode ter disparado browser notification

### 8. Regras de Negócio Aplicáveis

- RN-TKT-074-05: Notificações Tempo Real via SignalR (comentários equipe, mudança status)
- RN-TKT-074-06: Comentários Públicos Apenas (usuário vê APENAS Visibility=External, nunca Internal)
- RN-TKT-074-08: Upload Anexos com Validação e Antivírus (max 5MB, ClamAV, Azure Blob)
- RN-TKT-074-09: Auditoria Completa 7 Anos LGPD
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC04: Avaliar Atendimento com CSAT Inline Pós-Resolução

### 1. Descrição

Este caso de uso permite que usuário avalie atendimento imediatamente após chamado ser marcado como Resolvido, via popup inline (não-intrusivo) com escala 1-5 estrelas e comentário opcional, registrando satisfação em tabela TicketSatisfaction para análise de qualidade e métricas CSAT agregadas.

### 2. Atores

- Usuário Final (principal - avalia atendimento)
- Sistema (popup inline, persistência CSAT)

### 3. Pré-condições

- Usuário autenticado visualizando chamado próprio
- Chamado mudou Status para Resolvido (via atualização técnico)
- Avaliação CSAT ainda não foi submetida para este ticket

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário está visualizando Ticket #9876 em `/my-tickets/9876` | - |
| 2 | - | Ticket possui Status=EmAndamento, badge amarelo exibido |
| 3 | Técnico (sistema RF073) marca ticket como Resolvido às 16:00 | - |
| 4 | - | SignalR dispara evento ReceiveTicketUpdate com payload: { type: "status_change", newStatus: "Resolvido" } |
| 5 | - | Frontend recebe update em tempo real |
| 6 | - | Component detecta mudança para Status=Resolvido |
| 7 | - | Frontend atualiza badge (amarelo → verde "Resolvido") com animação |
| 8 | - | Frontend verifica: TicketSatisfaction já foi submetida? (campo ticket.satisfactionSubmittedAt == null) |
| 9 | - | Como NÃO foi submetida, aguarda 2 segundos (delay não-intrusivo) |
| 10 | - | Após 2s, frontend exibe toast/snackbar no canto inferior direito (não modal bloqueador): |
| 11 | - | Toast conteúdo: "✓ Seu chamado foi resolvido! Como você avalia o atendimento?" + 5 estrelas clicáveis ⭐⭐⭐⭐⭐ + link "Avaliar Depois" |
| 12 | - | Toast permanece visível por 30 segundos OU até usuário interagir |
| 13 | Usuário clica 4ª estrela (4 de 5) | - |
| 14 | - | Frontend destaca 4 estrelas preenchidas, 5ª vazia |
| 15 | - | Frontend expande toast mostrando textarea opcional "Comentário adicional (opcional)" + botão "Enviar Avaliação" |
| 16 | Usuário digita comentário "Atendimento rápido mas problema voltou depois de 1 dia" (64 caracteres) | - |
| 17 | Clica "Enviar Avaliação" | - |
| 18 | - | Executa SubmitSatisfactionSurveyCommand via HTTP POST /api/my-tickets/9876/satisfaction |
| 19 | - | Backend valida: Ticket ownership (UserId=CurrentUserId ✓), Stars entre 1-5 ✓, Comentário ≤500 chars ✓ |
| 20 | - | Backend cria TicketSatisfaction entity: TicketId=9876, UserId=CurrentUserId, Rating=4, Comments="Atendimento rápido mas...", SubmittedAt=UtcNow |
| 21 | - | Backend atualiza Ticket.SatisfactionSubmittedAt=UtcNow (flag para não exibir popup novamente) |
| 22 | - | Backend persiste alterações via UnitOfWork |
| 23 | - | Backend calcula agregação CSAT do técnico atribuído: TaxaCSAT_Ana = (Σ ratings 4-5 / Total avaliações) * 100 |
| 24 | - | Backend atualiza métricas do técnico: Ana.TaxaCSAT = 87% (372 avaliações, 324 ratings 4-5) |
| 25 | - | Backend registra auditoria com i18n (chave `ticket.satisfacao.submetida`) |
| 26 | - | Backend incrementa métrica Prometheus `csat_submissoes_total{rating="4",tecnico="Ana"}` |
| 27 | - | Backend retorna HTTP 200 OK |
| 28 | - | Frontend exibe toast verde de confirmação "✓ Obrigado pela avaliação!" e fecha popup CSAT |
| 29 | - | Detalhes do ticket agora exibem badge "Avaliado: ⭐⭐⭐⭐☆" abaixo do status |

### 5. Fluxos Alternativos

**FA01: Usuário Ignora CSAT (Não Avalia)**
- Passo 12: Toast permanece 30 segundos visível
- Usuário NÃO clica estrelas nem "Avaliar Depois"
- Após 30s, toast desaparece automaticamente
- Sistema NÃO registra avaliação, popup NÃO reaparece (usuário pode avaliar manualmente depois via botão "Avaliar Atendimento" na tela)

**FA02: Usuário Clica "Avaliar Depois"**
- Passo 13: Usuário clica link "Avaliar Depois"
- Toast fecha imediatamente
- Sistema registra lembrete: próximo acesso ao ticket, exibir popup novamente (max 3 lembretes)
- Após 3 lembretes ignorados, não exibe mais

**FA03: Avaliação 5 Estrelas (Excelente)**
- Passo 13: Usuário clica 5ª estrela
- Frontend expande textarea MAS com mensagem positiva "Que ótimo! Conte-nos o que mais gostou (opcional)"
- Comentário opcional permanece
- Rating=5 enviado ao backend

**FA04: Avaliação 1-2 Estrelas (Ruim) - Follow-up Automático**
- Passo 13: Usuário clica 1ª ou 2ª estrela (insatisfação)
- Frontend expande textarea MAS torna OBRIGATÓRIO: "Lamentamos! Por favor, conte-nos o que aconteceu (obrigatório)"
- Passo 19: Backend valida que para Rating ≤2, Comments é obrigatório (min 10 chars)
- Passo 21+: Backend dispara AlertaCSATBaixo para Gestor "Ticket #9876 avaliado com 1 estrela - Comentário: {text}"
- Gestor intervém para recuperar satisfação do cliente

### 6. Exceções

**EX01: Tentativa de Avaliar Duas Vezes**
- Passo 8: Ticket já possui Ticket.SatisfactionSubmittedAt preenchido (avaliação anterior)
- Frontend NÃO exibe popup CSAT
- Se usuário tentar acessar endpoint manualmente: POST /api/my-tickets/9876/satisfaction
- Backend retorna HTTP 400 Bad Request "Avaliação já foi submetida para este chamado"

**EX02: Avaliação Sem Selecionar Estrelas**
- Passo 17: Usuário clica "Enviar Avaliação" mas NÃO clicou nenhuma estrela (Stars=0)
- Frontend valida localmente, exibe mensagem "Por favor, selecione uma avaliação (1-5 estrelas)"
- Não envia requisição ao backend

**EX03: Comentário Muito Longo (>500 caracteres)**
- Passo 19: Backend detecta Comments com 650 caracteres
- FluentValidation retorna HTTP 400 "Comentário deve ter máximo 500 caracteres"
- Frontend exibe contador de caracteres "650/500" em vermelho, botão "Enviar" desabilitado

**EX04: Ticket Não Está Resolvido (Tentativa Manual)**
- Usuário tenta acessar diretamente endpoint POST /api/my-tickets/9876/satisfaction para ticket com Status=EmAndamento
- Backend valida: Ticket.Status != Resolvido
- Backend retorna HTTP 400 "Avaliação só pode ser submetida para chamados resolvidos"

### 7. Pós-condições

- Avaliação CSAT registrada no banco (TicketSatisfaction entity)
- Ticket marcado como avaliado (SatisfactionSubmittedAt preenchido)
- Métricas do técnico atualizadas (TaxaCSAT recalculada)
- Auditoria registrada
- Métricas Prometheus incrementadas
- Se rating baixo (≤2), alerta disparado para gestor

### 8. Regras de Negócio Aplicáveis

- RN-TKT-074-07: CSAT Inline Pós-Resolução (popup 1-5 stars, comentário opcional, não-intrusivo)
- RN-TKT-074-09: Auditoria Completa 7 Anos LGPD
- RN-MTY-001-01: Multi-tenancy obrigatório

---

## UC05: Acessar Portal Offline via PWA com Service Workers

### 1. Descrição

Este caso de uso permite que usuário acesse portal self-service mesmo quando offline (sem conexão internet), visualizando lista de chamados previamente carregados e artigos FAQ em cache via Service Workers, com sincronização automática de dados ao retornar online.

### 2. Atores

- Usuário Final (principal - acessa offline)
- Service Worker (gerenciamento de cache, sync automático)
- Sistema (sync backend quando online)

### 3. Pré-condições

- Usuário já acessou portal pelo menos 1 vez (Service Worker instalado)
- Dados cached: lista de tickets, FAQ, assets estáticos (CSS, JS, imagens)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Usuário acessa portal via mobile em local sem internet (avião, área rural) | - |
| 2 | Navegador detecta que está offline (navigator.onLine = false) |  - |
| 3 | Service Worker intercepta request GET /my-tickets | - |
| 4 | - | Service Worker verifica cache local (IndexedDB): chave `my-tickets-{userId}` existe ✓ |
| 5 | - | Service Worker retorna dados do cache (última sincronização online há 2 horas) |
| 6 | - | Frontend renderiza lista de tickets do cache (10 tickets vistos anteriormente) |
| 7 | - | Frontend exibe banner amarelo no topo "⚠️ Você está offline. Dados podem estar desatualizados." |
| 8 | - | Cards de tickets exibem normalmente com dados cached |
| 9 | Usuário clica ticket #9876 para ver detalhes | - |
| 10 | Service Worker intercepta request GET /my-tickets/9876 | - |
| 11 | - | Service Worker verifica cache: chave `ticket-9876-details` existe ✓ |
| 12 | - | Retorna detalhes do cache (descrição, comentários, status cached) |
| 13 | - | Frontend exibe detalhes do ticket normalmente |
| 14 | Usuário decide consultar FAQ para problema similar | - |
| 15 | Pressiona Ctrl+/ para abrir modal FAQ | - |
| 16 | Service Worker intercepta request GET /faq/search?term=internet | - |
| 17 | - | Service Worker verifica cache: artigos FAQ cached ✓ (top 100 artigos mais acessados) |
| 18 | - | Executa busca LOCAL no cache via JavaScript (não precisa backend) |
| 19 | - | Retorna 3 artigos encontrados localmente |
| 20 | - | Frontend exibe artigos FAQ cached |
| 21 | Usuário lê artigo "Como resolver Internet Lenta" (texto completo cached) | - |
| 22 | - | 30 minutos depois: Conexão internet retorna (Wi-Fi disponível) |
| 23 | - | Navegador detecta navigator.onLine = true |
| 24 | - | Service Worker dispara evento `sync` automaticamente |
| 25 | - | Service Worker executa background sync: envia requisições pendentes enfileiradas (se houver ações offline como comentários tentados) |
| 26 | - | Service Worker atualiza cache: GET /my-tickets retorna dados frescos do backend |
| 27 | - | Service Worker compara dados cached vs novos: Ticket #9876 mudou Status (EmAndamento → Resolvido) |
| 28 | - | Service Worker atualiza cache local com dados novos |
| 29 | - | Service Worker dispara evento customizado `cache-updated` para frontend |
| 30 | - | Frontend recebe evento, exibe toast "Dados atualizados! Ticket #9876 foi resolvido." |
| 31 | - | Frontend atualiza tela com dados novos SEM reload completo |
| 32 | - | Banner "Você está offline" desaparece |

### 5. Fluxos Alternativos

**FA01: Tentativa de Criar Chamado Offline (Enfileirado para Sync)**
- Usuário tenta criar chamado enquanto offline
- Frontend detecta navigator.onLine = false
- Frontend salva dados do formulário no IndexedDB com flag `pending-sync`
- Frontend exibe mensagem "Você está offline. Chamado será criado automaticamente quando conexão retornar."
- Quando online (passo 24), Service Worker envia POST /my-tickets com dados enfileirados
- Backend cria chamado, retorna ID
- Frontend exibe toast "✓ Chamado #9999 criado com sucesso (sincronizado)"

**FA02: Cache Expirado (Dados Muito Antigos)**
- Passo 4: Service Worker verifica cache age: última sync há 7 dias (>TTL 48h)
- Service Worker retorna cache MAS marca como stale
- Frontend exibe banner vermelho "⚠️ Dados desatualizados (última sync: 7 dias atrás). Conecte-se à internet."
- Usuário pode visualizar mas com aviso claro

**FA03: Asset Estático Não Cached (Imagem Nova)**
- Usuário clica imagem de anexo que não está em cache (foi adicionada recentemente)
- Service Worker detecta que asset não existe no cache
- Service Worker tenta buscar via network
- Network falha (offline)
- Service Worker retorna placeholder image "offline-placeholder.png" do cache
- Frontend exibe imagem placeholder + mensagem "Imagem indisponível offline"

**FA04: Install Prompt PWA (Primeiro Acesso Mobile)**
- Usuário acessa portal pela primeira vez via mobile Chrome/Safari
- Navegador detecta PWA manifest.json válido
- Navegador exibe banner "Adicionar IControlIT à tela inicial?"
- Usuário aceita
- Ícone instalado na tela inicial, abre como app standalone (sem barra navegador)
- Service Worker instalado em background

### 6. Exceções

**EX01: Cache Vazio (Primeira Vez Offline)**
- Passo 4: Service Worker verifica cache mas chave não existe (usuário nunca acessou portal online)
- Service Worker não pode retornar dados
- Frontend exibe mensagem "Você está offline e não possui dados em cache. Conecte-se à internet para acessar seus chamados."

**EX02: Tentativa de Ação Não-Permitida Offline (Upload Anexo)**
- Usuário tenta fazer upload de anexo enquanto offline
- Frontend detecta navigator.onLine = false
- Frontend desabilita botão de upload, exibe tooltip "Upload de anexos requer conexão internet"

**EX03: Sync Falha Após Retornar Online (Backend Offline)**
- Passo 26: Service Worker tenta sync mas backend retorna HTTP 503 (manutenção)
- Service Worker agenda retry exponencial (1min, 5min, 15min)
- Se todas tentativas falharem, mantém dados enfileirados
- Frontend exibe banner "Sincronização pendente - servidor indisponível"

**EX04: Quota Exceeded (Cache Muito Grande)**
- Service Worker tenta cached nova resposta mas IndexedDB quota exceeded (browser limit ~50MB mobile)
- Service Worker executa LRU eviction: remove tickets/FAQ menos acessados
- Service Worker tenta novamente
- Se ainda falhar, loga erro mas não bloqueia funcionalidade

### 7. Pós-condições

- Usuário conseguiu acessar portal offline
- Dados cached exibidos com avisos apropriados
- Ações offline enfileiradas para sync
- Ao retornar online, sync automático executado
- Cache atualizado com dados frescos
- Frontend refletiu mudanças sem reload

### 8. Regras de Negócio Aplicáveis

- RN-TKT-074-10: PWA com Suporte Offline (Service Workers cache tickets, FAQ, sync automático)
- RN-TKT-074-04: FAQ Integrada (artigos cached para consulta offline)
- RN-MTY-001-01: Multi-tenancy obrigatório (cache isolado por ClienteId+UserId)

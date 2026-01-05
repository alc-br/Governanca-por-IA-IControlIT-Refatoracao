# Casos de Uso - RF066 - Notificações e Alertas

**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC005-NOT - Notificações
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**RF Relacionado:** [RF066 - Notificações e Alertas](./RF066.md)

---

## Índice de Casos de Uso

| UC | Nome | Cobertura |
|----|------|-----------|
| UC00 | Listar/Visualizar Central de Notificações | F-NOT-066-04 |
| UC01 | Enviar Notificação Multi-Canal | F-NOT-066-01 |
| UC02 | Configurar Preferências de Canal | F-NOT-066-02 |
| UC03 | Configurar Quiet Hours | F-NOT-066-03 |
| UC04 | Marcar Notificação como Lida/Não Lida | F-NOT-066-05 |
| UC05 | Executar Quick Actions em Notificações | F-NOT-066-06 |
| UC06 | Configurar Agrupamento Inteligente | F-NOT-066-07 |
| UC07 | Ativar/Desativar Digest Diário | F-NOT-066-08 |
| UC08 | Rastrear Métricas de Entrega | F-NOT-066-09 |
| UC09 | Configurar Retry Policy | F-NOT-066-10 |
| UC10 | Aplicar Rate Limiting Automático | F-NOT-066-11 |
| UC11 | Gerenciar Notificações de Conformidade | F-NOT-066-12 |
| UC12 | Dashboard de Métricas de Notificações | F-NOT-066-13 |

---

# UC00: Listar/Visualizar Central de Notificações

**Cobertura:** F-NOT-066-04 (Visualizar Histórico de Notificações)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

---

## Objetivo

Permitir que usuários visualizem seu histórico completo de notificações recebidas com filtros por canal, tipo, período e status de leitura, possibilitando que administradores e auditores consultem histórico de todos os usuários para fins de auditoria e conformidade.

---

## Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `NOT.HISTORICO.VIEW`
- Sistema multi-tenant configurado (isolamento por `EmpresaId`)

---

## Pós-condições

- Histórico de notificações exibido conforme filtros aplicados
- Ações de navegação (paginação, ordenação) registradas em auditoria
- Notificações in-app marcadas como visualizadas quando abertas

---

## Atores

- **Principal:** Usuário comum (visualiza próprio histórico)
- **Secundários:**
  - Administrador (visualiza histórico de todos usuários)
  - Auditor (consulta para conformidade)

---

## Fluxo Principal

**FP-UC00-001:** Usuário acessa Central de Notificações pelo menu ou ícone de sino no header

**FP-UC00-002:** Sistema valida permissão `NOT.HISTORICO.VIEW`

**FP-UC00-003:** Sistema carrega notificações do usuário logado (filtro por `UsuarioDestinatarioId` + `EmpresaId`)

**FP-UC00-004:** Sistema exibe grid com colunas:
- Ícone do canal (Email/SMS/Push/WhatsApp/InApp)
- Tipo de notificação (ex: "Aprovação Pendente", "Fatura Vencida")
- Título da notificação
- Mensagem (prévia de 100 caracteres)
- Data/Hora de envio
- Status de leitura (Lida/Não Lida)
- Status de entrega (Enviado/Entregue/Aberto/Falhou)
- Prioridade (badge colorido: Baixa/Normal/Alta/Urgente/Crítica)
- Quick Actions disponíveis (botões de ação rápida)

**FP-UC00-005:** Sistema aplica ordenação padrão: notificações não lidas primeiro, depois por data decrescente

**FP-UC00-006:** Sistema aplica paginação (20 notificações por página)

**FP-UC00-007:** Sistema exibe contador de notificações não lidas no ícone de sino do header

**FP-UC00-008:** Caso de Uso concluído com sucesso

---

## Fluxos Alternativos

**FA-UC00-001:** Filtrar por Canal
- Passo FP-UC00-004
- Usuário seleciona canal específico no dropdown (Email, SMS, Push, WhatsApp, InApp, Todos)
- Sistema aplica filtro `CanaisUtilizados LIKE '%canal%'`
- Retorna ao FP-UC00-004

**FA-UC00-002:** Filtrar por Tipo de Notificação
- Passo FP-UC00-004
- Usuário seleciona tipo no dropdown (ex: "Aprovações", "Faturas", "Alertas de Sistema")
- Sistema aplica filtro `Tipo = tipo_selecionado`
- Retorna ao FP-UC00-004

**FA-UC00-003:** Filtrar por Período
- Passo FP-UC00-004
- Usuário seleciona período (Hoje, Últimos 7 dias, Últimos 30 dias, Personalizado)
- Se Personalizado: exibe calendário para seleção de data início/fim
- Sistema aplica filtro `DataEnvio BETWEEN @DataInicio AND @DataFim`
- Retorna ao FP-UC00-004

**FA-UC00-004:** Filtrar por Status de Leitura
- Passo FP-UC00-004
- Usuário seleciona status (Todas, Lidas, Não Lidas)
- Sistema aplica filtro `IsLida = @Status`
- Retorna ao FP-UC00-004

**FA-UC00-005:** Filtrar por Prioridade
- Passo FP-UC00-004
- Usuário seleciona prioridade (Crítica, Urgente, Alta, Normal, Baixa, Todas)
- Sistema aplica filtro `Prioridade = @Prioridade`
- Retorna ao FP-UC00-004

**FA-UC00-006:** Buscar por Texto
- Passo FP-UC00-004
- Usuário digita texto na caixa de busca
- Sistema aplica filtro `Titulo LIKE '%texto%' OR Mensagem LIKE '%texto%'`
- Retorna ao FP-UC00-004

**FA-UC00-007:** Administrador Visualiza Histórico de Outro Usuário
- Passo FP-UC00-003
- Administrador seleciona usuário no dropdown
- Sistema valida se usuário logado é Administrador ou Auditor
- Sistema carrega notificações do usuário selecionado (mantém filtro por `EmpresaId`)
- Retorna ao FP-UC00-004

**FA-UC00-008:** Abrir Detalhes da Notificação
- Passo FP-UC00-004
- Usuário clica em uma notificação
- Sistema exibe modal com detalhes completos:
  - Título completo
  - Mensagem completa
  - Data/Hora de envio
  - Canais utilizados (tags)
  - Status de entrega por canal (timeline visual)
  - Quick Actions disponíveis (botões destacados)
  - Histórico de tentativas de envio (se houver retry)
- Sistema marca notificação como lida (`IsLida = true`, `DataLeitura = GETDATE()`)
- Retorna ao FP-UC00-004

---

## Fluxos de Exceção

**FE-UC00-001:** Usuário sem Permissão
- Passo FP-UC00-002
- Sistema valida que usuário NÃO possui permissão `NOT.HISTORICO.VIEW`
- Sistema retorna HTTP 403 Forbidden
- Sistema exibe mensagem: "Você não tem permissão para acessar o histórico de notificações"
- Caso de Uso encerrado

**FE-UC00-002:** Nenhuma Notificação Encontrada
- Passo FP-UC00-003
- Sistema não encontra notificações para os filtros aplicados
- Sistema exibe estado vazio com ícone e mensagem: "Nenhuma notificação encontrada"
- Sistema exibe botão "Limpar Filtros" (se filtros aplicados)
- Retorna ao FP-UC00-004

**FE-UC00-003:** Erro ao Carregar Notificações
- Passo FP-UC00-003
- Sistema falha ao consultar banco de dados (timeout, conexão)
- Sistema exibe mensagem de erro: "Erro ao carregar notificações. Tente novamente em instantes."
- Sistema registra exceção em log de erros
- Caso de Uso encerrado

**FE-UC00-004:** Conexão SignalR Falhou (Notificações Real-Time)
- Passo FP-UC00-007
- Sistema detecta que conexão SignalR está offline
- Sistema exibe aviso: "Notificações em tempo real desabilitadas. Atualize a página para ver novas notificações."
- Sistema continua funcionando em modo polling (atualização manual)
- Retorna ao FP-UC00-007

---

## Regras de Negócio Aplicadas

**RN-UC-00-001:** Isolamento Multi-Tenant
- **Origem:** RN-NOT-066-01
- **Descrição:** Usuário comum SEMPRE visualiza APENAS notificações do seu `EmpresaId`
- **Validação:** Query DEVE incluir `WHERE EmpresaId = @EmpresaIdUsuarioLogado`
- **Exceção:** Administrador pode visualizar cross-tenant apenas se tiver permissão global

**RN-UC-00-002:** Ordenação Inteligente
- **Origem:** Requisito implícito UX
- **Descrição:** Notificações não lidas SEMPRE aparecem primeiro, depois ordenadas por data decrescente
- **Implementação:** `ORDER BY IsLida ASC, DataEnvio DESC`

**RN-UC-00-003:** Paginação Obrigatória
- **Origem:** Performance
- **Descrição:** Histórico DEVE ser paginado (máximo 20 por página)
- **Implementação:** Usar `OFFSET @Skip ROWS FETCH NEXT 20 ROWS ONLY`

**RN-UC-00-004:** Marcação Automática como Lida
- **Origem:** RN-NOT-066-05
- **Descrição:** Ao abrir detalhes de uma notificação in-app, marcar automaticamente como lida
- **Exceção:** Notificações de canais externos (Email, SMS) NÃO são marcadas como lidas automaticamente

**RN-UC-00-005:** Retenção de Notificações
- **Origem:** RN-NOT-066-14 (lido no RF066.yaml)
- **Descrição:** Notificações com prioridade Baixa/Normal expiram após 30 dias; Alta/Urgente/Crítica após 90 dias
- **Implementação:** Job diário executa soft delete (`IsDeleted = true`) para notificações expiradas

---

## Critérios de Aceite

**CA-UC00-001:** Grid de Notificações Exibido Corretamente
- **Dado que** usuário possui permissão `NOT.HISTORICO.VIEW`
- **Quando** acessa Central de Notificações
- **Então** sistema exibe grid com todas colunas especificadas em FP-UC00-004
- **E** grid contém apenas notificações do `EmpresaId` do usuário
- **E** paginação mostra 20 notificações por página

**CA-UC00-002:** Filtros Funcionam Independentemente
- **Dado que** usuário está na Central de Notificações
- **Quando** aplica filtro de canal = "Email"
- **Então** sistema exibe APENAS notificações enviadas via Email
- **E** contador de resultados é atualizado
- **E** URL é atualizada com query string `?canal=email`

**CA-UC00-003:** Notificações Não Lidas Aparecem Primeiro
- **Dado que** usuário possui 10 notificações não lidas e 50 lidas
- **Quando** acessa Central de Notificações sem filtros
- **Então** sistema exibe 10 notificações não lidas nas primeiras posições
- **E** notificações lidas aparecem depois, ordenadas por data decrescente

**CA-UC00-004:** Detalhes de Notificação Marcam como Lida
- **Dado que** usuário clica em notificação não lida
- **Quando** sistema abre modal de detalhes
- **Então** sistema marca `IsLida = true` e `DataLeitura = now()`
- **E** badge de não lida é removido visualmente
- **E** contador de não lidas no header é decrementado

**CA-UC00-005:** Administrador Pode Visualizar Outros Usuários
- **Dado que** usuário logado é Administrador
- **Quando** seleciona outro usuário no dropdown
- **Então** sistema exibe notificações do usuário selecionado
- **E** mantém filtro por `EmpresaId` do usuário selecionado
- **E** registra ação em auditoria

**CA-UC00-006:** Estado Vazio Exibido Quando Sem Notificações
- **Dado que** usuário não possui notificações
- **Quando** acessa Central de Notificações
- **Então** sistema exibe ícone de sino vazio
- **E** mensagem "Nenhuma notificação encontrada"
- **E** NÃO exibe grid

**CA-UC00-007:** Erro 403 para Usuário Sem Permissão
- **Dado que** usuário NÃO possui permissão `NOT.HISTORICO.VIEW`
- **Quando** tenta acessar Central de Notificações
- **Então** sistema retorna HTTP 403 Forbidden
- **E** exibe mensagem de permissão negada
- **E** registra tentativa de acesso em auditoria

---

# UC01: Enviar Notificação Multi-Canal

**Cobertura:** F-NOT-066-01 (Enviar Notificação Multi-Canal)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

---

## Objetivo

Permitir que o sistema envie notificações para usuários através de múltiplos canais (Email, SMS, Push, WhatsApp, In-App) de forma programática, respeitando preferências de canal do usuário, quiet hours, priorização e rate limiting.

---

## Pré-condições

- Sistema possui credenciais configuradas para providers externos (SendGrid, Twilio, Firebase, WhatsApp Business API)
- Usuário destinatário existe no sistema
- Template de notificação (se usar RF063) existe e está ativo
- Hangfire está executando (para processamento assíncrono)

---

## Pós-condições

- Notificação criada no banco de dados com status "Pendente"
- Job Hangfire enfileirado para processamento assíncrono
- Canais selecionados tentam envio conforme preferências do usuário
- Tentativas de envio registradas com status (Enviado/Entregue/Falhou)
- Métricas de entrega rastreadas (se provider suportar webhooks)

---

## Atores

- **Principal:** Sistema (envio programático via API ou eventos internos)
- **Secundários:**
  - Usuário remetente (se envio manual por Administrador)
  - Providers externos (SendGrid, Twilio, Firebase, WhatsApp)

---

## Fluxo Principal

**FP-UC01-001:** Sistema recebe comando `SendNotificationCommand` com payload:
```json
{
  "usuarioDestinatarioId": "guid",
  "tipo": "AprovacaoPendente",
  "titulo": "Nova aprovação pendente",
  "mensagem": "Você tem uma nova solicitação para aprovar",
  "prioridade": "Alta", // Baixa, Normal, Alta, Urgente, Crítica
  "canaisPreferidos": ["Email", "InApp"], // null = usar preferências do usuário
  "templateId": "guid", // Opcional - integração com RF063
  "placeholders": {"nome": "João", "valor": "R$ 1.500,00"},
  "quickActions": [
    {"tipo": "Aprovar", "endpoint": "/api/aprovacoes/123/aprovar"},
    {"tipo": "Rejeitar", "endpoint": "/api/aprovacoes/123/rejeitar"}
  ],
  "isComplianceRequired": false // true = ignora quiet hours e rate limiting
}
```

**FP-UC01-002:** Sistema valida payload:
- `usuarioDestinatarioId` existe
- `tipo` é válido (enum TipoNotificacao)
- `prioridade` é válido (enum Prioridade)
- `canaisPreferidos` são válidos (Email, SMS, Push, WhatsApp, InApp)
- Se `templateId` informado: template existe e está ativo

**FP-UC01-003:** Sistema carrega preferências de notificação do usuário destinatário (tabela `NotificacaoPreferencia`)

**FP-UC01-004:** Sistema determina canais a utilizar:
- Se `canaisPreferidos` informado no payload: usa canais especificados
- Se NULL: usa preferências do usuário para o `tipo` de notificação
- Filtra canais desabilitados pelo usuário (exceto se `isComplianceRequired = true`)

**FP-UC01-005:** Sistema verifica quiet hours:
- Carrega configuração de quiet hours do usuário (padrão: 22h-8h)
- Se prioridade = Baixa ou Normal E hora atual está dentro de quiet hours:
  - Sistema agenda envio para fim do quiet hours (08:00 próximo dia)
  - Registra `Status = "AgendadoQuietHours"`
- Se prioridade = Alta, Urgente ou Crítica: ignora quiet hours e prossegue

**FP-UC01-006:** Sistema verifica rate limiting (RN-NOT-066-06):
- Conta notificações enviadas ao usuário nas últimas 24h
- Se `count >= 50` E `isComplianceRequired = false`:
  - Sistema rejeita envio
  - Registra `Status = "BloqueadoRateLimit"`
  - Retorna erro HTTP 429 Too Many Requests
- Se `isComplianceRequired = true`: ignora rate limiting e prossegue

**FP-UC01-007:** Sistema cria registro na tabela `Notificacao`:
```sql
INSERT INTO Notificacao (
  Id, EmpresaId, UsuarioRemetenteId, UsuarioDestinatarioId,
  Tipo, Titulo, Mensagem, Prioridade, CanaisUtilizados,
  IsComplianceRequired, Status, DataEnvio, DataCriacao
) VALUES (
  NEWID(), @EmpresaId, @UsuarioRemetenteId, @UsuarioDestinatarioId,
  @Tipo, @Titulo, @Mensagem, @Prioridade, @CanaisJSON,
  @IsComplianceRequired, 'Pendente', NULL, GETDATE()
)
```

**FP-UC01-008:** Sistema enfileira job Hangfire `ProcessarEnvioNotificacaoJob` com ID da notificação

**FP-UC01-009:** Sistema retorna resposta HTTP 202 Accepted com:
```json
{
  "notificacaoId": "guid",
  "status": "Pendente",
  "canaisUtilizados": ["Email", "InApp"],
  "agendadoPara": "2025-12-31T08:00:00Z" // se quiet hours aplicado
}
```

**FP-UC01-010:** Job Hangfire `ProcessarEnvioNotificacaoJob` executa:
- Para cada canal em `CanaisUtilizados`:
  - Chama implementação específica (`INotificationChannel`)
  - **Email:** `EmailNotificationChannel.Send()` → SendGrid API
  - **SMS:** `SmsNotificationChannel.Send()` → Twilio API
  - **Push:** `PushNotificationChannel.Send()` → Firebase FCM
  - **WhatsApp:** `WhatsAppNotificationChannel.Send()` → WhatsApp Business API
  - **InApp:** `InAppNotificationChannel.Send()` → SignalR broadcast

**FP-UC01-011:** Para cada tentativa de envio:
- Sistema cria registro em `NotificacaoTentativaEnvio`:
  - `Canal`, `Status` (Enviado/Falhou), `DataTentativa`, `ResponseCode`, `ErrorMessage`

**FP-UC01-012:** Se TODOS os canais enviaram com sucesso:
- Sistema atualiza `Notificacao.Status = "Enviado"`
- Sistema atualiza `Notificacao.DataEnvio = GETDATE()`

**FP-UC01-013:** Se InApp foi um dos canais:
- Sistema dispara evento SignalR para usuário destinatário
- Frontend exibe toast notification em tempo real
- Frontend incrementa contador de não lidas no ícone de sino

**FP-UC01-014:** Caso de Uso concluído com sucesso

---

## Fluxos Alternativos

**FA-UC01-001:** Usar Template de Notificação (RF063)
- Passo FP-UC01-001
- Payload inclui `templateId` válido
- Sistema carrega template da tabela `NotificacaoTemplate`
- Sistema substitui placeholders no `Titulo` e `Mensagem` usando `placeholders` do payload
- Exemplo: `"Olá {{nome}}, você tem uma nova solicitação de {{valor}}"` → `"Olá João, você tem uma nova solicitação de R$ 1.500,00"`
- Retorna ao FP-UC01-002

**FA-UC01-002:** Agrupamento Inteligente Aplicado
- Passo FP-UC01-004
- Sistema detecta que existem >5 notificações do mesmo `Tipo` para o mesmo usuário em janela de 30 minutos
- Sistema cancela notificações individuais pendentes
- Sistema cria UMA notificação agrupada: "Você tem 12 novas aprovações pendentes"
- Sistema atualiza notificações canceladas com `Status = "AgrupadaEm"` + ID da notificação consolidada
- Retorna ao FP-UC01-007

**FA-UC01-003:** Digest Diário Ativo para Usuário
- Passo FP-UC01-004
- Sistema verifica se usuário tem `DigestDiarioAtivo = true` nas preferências
- Se canal Email está nos `canaisPreferidos`:
  - Sistema NÃO envia email imediatamente
  - Sistema marca notificação para inclusão no digest diário (18h)
  - Outros canais (InApp, SMS, Push) enviam normalmente
- Retorna ao FP-UC01-007

**FA-UC01-004:** Notificação In-App com Quick Actions
- Passo FP-UC01-013
- Payload inclui array `quickActions`
- Sistema serializa quick actions no JSON da notificação
- Frontend exibe botões de ação rápida diretamente no toast/modal
- Usuário pode clicar "Aprovar" ou "Rejeitar" sem abrir o sistema completo
- Sistema chama endpoint especificado e marca notificação como "ActionExecuted"
- Retorna ao FP-UC01-014

---

## Fluxos de Exceção

**FE-UC01-001:** Usuário Destinatário Não Existe
- Passo FP-UC01-002
- Sistema valida que `usuarioDestinatarioId` NÃO existe
- Sistema retorna HTTP 404 Not Found
- Sistema exibe mensagem: "Usuário destinatário não encontrado"
- Sistema registra erro em log
- Caso de Uso encerrado

**FE-UC01-002:** Template de Notificação Inativo
- Passo FP-UC01-002
- Sistema valida que `templateId` existe mas está inativo (`IsAtivo = false`)
- Sistema retorna HTTP 400 Bad Request
- Sistema exibe mensagem: "Template de notificação inativo. Não é possível enviar."
- Caso de Uso encerrado

**FE-UC01-003:** Rate Limiting Excedido
- Passo FP-UC01-006
- Sistema conta >50 notificações nas últimas 24h
- Sistema valida que `isComplianceRequired = false`
- Sistema retorna HTTP 429 Too Many Requests com header `Retry-After: 86400` (24h em segundos)
- Sistema cria notificação com `Status = "BloqueadoRateLimit"`
- Sistema registra evento em auditoria
- Caso de Uso encerrado

**FE-UC01-004:** Falha ao Enviar em TODOS os Canais
- Passo FP-UC01-011
- Todos canais retornam erro (timeout, HTTP 5xx, provider offline)
- Sistema marca `Notificacao.Status = "Falhou"`
- Sistema enfileira retry automático (UC09) se habilitado
- Sistema notifica administradores via canal alternativo (log crítico, PagerDuty)
- Caso de Uso encerrado com falha

**FE-UC01-005:** Falha Parcial (Alguns Canais Enviaram, Outros Falharam)
- Passo FP-UC01-011
- Email enviou com sucesso, mas SMS falhou
- Sistema marca `Notificacao.Status = "EnviadoParcial"`
- Sistema registra canais que falharam em `NotificacaoTentativaEnvio`
- Sistema enfileira retry APENAS para canais que falharam
- Sistema MANTÉM status "Enviado" para canais bem-sucedidos
- Retorna ao FP-UC01-014

**FE-UC01-006:** Configuração de Provider Inválida
- Passo FP-UC01-010
- Sistema tenta enviar Email mas credenciais SendGrid não estão configuradas
- Sistema lança exceção `ProviderConfigurationException`
- Sistema marca canal Email como "Falhou" com mensagem "Credenciais não configuradas"
- Sistema continua tentando outros canais
- Sistema notifica administrador sobre configuração faltante
- Retorna ao FP-UC01-011

**FE-UC01-007:** SignalR Connection Offline (InApp)
- Passo FP-UC01-013
- Sistema tenta enviar via SignalR mas usuário está offline
- Sistema marca tentativa como "Pendente" (será entregue quando usuário conectar)
- Sistema mantém notificação no banco para ser exibida no próximo login
- Outros canais (Email, SMS) enviam normalmente
- Retorna ao FP-UC01-014

---

## Regras de Negócio Aplicadas

**RN-UC-01-001:** Quiet Hours Respeitadas Apenas para Prioridade Baixa/Normal
- **Origem:** RN-NOT-066-03
- **Descrição:** Notificações Urgentes e Críticas SEMPRE são enviadas, mesmo durante quiet hours
- **Implementação:** `IF @Prioridade IN ('Alta', 'Urgente', 'Critica') THEN ignorar quiet hours`

**RN-UC-01-002:** Rate Limiting de 50 Notificações por 24h
- **Origem:** RN-NOT-066-06
- **Descrição:** Usuário pode receber MÁXIMO 50 notificações em 24h (exceto conformidade obrigatórias)
- **Exceção:** Notificações com `isComplianceRequired = true` ignoram rate limiting
- **Implementação:** Query `COUNT(*) WHERE UsuarioDestinatarioId = @Id AND DataEnvio >= DATEADD(hour, -24, GETDATE())`

**RN-UC-01-003:** Notificações de Conformidade Não Podem Ser Bloqueadas
- **Origem:** RN-NOT-066-12
- **Descrição:** Notificações com `isComplianceRequired = true` SEMPRE são enviadas (ignoram quiet hours, rate limiting, preferências de usuário)
- **Casos de Uso:** Notificações legais, termos de uso atualizados, avisos de segurança

**RN-UC-01-004:** Multi-Tenancy Obrigatório
- **Origem:** Padrão arquitetural
- **Descrição:** Notificação SEMPRE pertence a uma `EmpresaId` (do usuário destinatário)
- **Validação:** `EmpresaId` extraído do contexto do usuário logado
- **Isolamento:** Queries DEVEM filtrar por `EmpresaId`

**RN-UC-01-005:** Priorização de Canais
- **Origem:** RN-NOT-066-02
- **Descrição:** Se múltiplos canais ativos, ordem de envio: InApp (imediato) → Email → SMS → Push → WhatsApp
- **Motivação:** InApp é instantâneo; Email é mais barato que SMS; WhatsApp tem limitações de API

**RN-UC-01-006:** Processamento Assíncrono Obrigatório
- **Origem:** Requisito não-funcional
- **Descrição:** Envio de notificações NUNCA deve bloquear thread HTTP
- **Implementação:** Hangfire job enfileirado, resposta HTTP 202 Accepted retornada imediatamente

---

## Critérios de Aceite

**CA-UC01-001:** Notificação Multi-Canal Enviada com Sucesso
- **Dado que** payload válido com `canaisPreferidos = ["Email", "InApp"]`
- **Quando** sistema recebe `SendNotificationCommand`
- **Então** sistema cria registro em `Notificacao` com `Status = "Pendente"`
- **E** sistema enfileira job Hangfire
- **E** sistema retorna HTTP 202 Accepted
- **E** job processa e envia via Email (SendGrid) E InApp (SignalR)
- **E** ambos canais marcam `Status = "Enviado"`

**CA-UC01-002:** Quiet Hours Bloqueiam Notificação Baixa Prioridade
- **Dado que** notificação com `prioridade = "Normal"` e hora atual = 23h
- **E** quiet hours do usuário = 22h-8h
- **Quando** sistema processa envio
- **Então** sistema agenda envio para 08:00 próximo dia
- **E** marca `Status = "AgendadoQuietHours"`
- **E** NÃO envia notificação imediatamente

**CA-UC01-003:** Notificação Crítica Ignora Quiet Hours
- **Dado que** notificação com `prioridade = "Crítica"` e hora atual = 02h
- **E** quiet hours do usuário = 22h-8h
- **Quando** sistema processa envio
- **Então** sistema envia IMEDIATAMENTE
- **E** marca `Status = "Enviado"`
- **E** NÃO agenda para depois

**CA-UC01-004:** Rate Limiting Bloqueia 51ª Notificação
- **Dado que** usuário recebeu 50 notificações nas últimas 24h
- **E** notificação #51 tem `isComplianceRequired = false`
- **Quando** sistema valida rate limiting
- **Então** sistema retorna HTTP 429 Too Many Requests
- **E** marca `Status = "BloqueadoRateLimit"`
- **E** NÃO envia notificação

**CA-UC01-005:** Notificação de Conformidade Ignora Rate Limiting
- **Dado que** usuário recebeu 50 notificações nas últimas 24h
- **E** notificação #51 tem `isComplianceRequired = true`
- **Quando** sistema valida rate limiting
- **Então** sistema IGNORA limite de 50
- **E** envia notificação normalmente
- **E** marca `Status = "Enviado"`

**CA-UC01-006:** Template Processado com Placeholders Substituídos
- **Dado que** payload inclui `templateId` válido
- **E** template contém `"Olá {{nome}}, você tem {{quantidade}} itens"`
- **E** placeholders = `{"nome": "Maria", "quantidade": "5"}`
- **Quando** sistema processa template
- **Então** `Mensagem = "Olá Maria, você tem 5 itens"`
- **E** notificação é enviada com texto processado

**CA-UC01-007:** Falha de Canal Registrada com Retry Agendado
- **Dado que** envio via SMS falha (Twilio retorna HTTP 503)
- **Quando** sistema processa tentativa
- **Então** sistema cria `NotificacaoTentativaEnvio` com `Status = "Falhou"`
- **E** registra `ErrorMessage = "Twilio temporarily unavailable"`
- **E** enfileira retry após 2 minutos (backoff exponencial)
- **E** outros canais (Email, InApp) enviam normalmente

**CA-UC01-008:** Quick Actions Disponíveis em Notificação InApp
- **Dado que** payload inclui `quickActions = [{"tipo": "Aprovar", "endpoint": "/api/aprovacoes/123/aprovar"}]`
- **Quando** sistema envia via InApp (SignalR)
- **Então** frontend exibe toast com botão "Aprovar"
- **E** ao clicar botão, sistema chama `POST /api/aprovacoes/123/aprovar`
- **E** marca notificação como "ActionExecuted"

---

# UC02: Configurar Preferências de Canal

**Cobertura:** F-NOT-066-02 (Configurar Preferências de Canal por Usuário)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

---

## Objetivo

Permitir que usuários configurem suas preferências de recebimento de notificações por tipo e canal, escolhendo quais canais desejam receber para cada categoria de notificação (Aprovações, Faturas, Alertas, etc.).

---

## Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `NOT.PREFERENCIAS.MANAGE`
- Tipos de notificação estão cadastrados no sistema

---

## Pós-condições

- Preferências salvas na tabela `NotificacaoPreferencia`
- Canais desabilitados NÃO receberão notificações futuras (exceto conformidade obrigatórias)
- Alterações registradas em auditoria

---

## Atores

- **Principal:** Usuário comum (configura próprias preferências)
- **Secundários:** Administrador (pode configurar preferências de outros usuários)

---

## Fluxo Principal

**FP-UC02-001:** Usuário acessa "Configurações → Notificações → Preferências de Canal"

**FP-UC02-002:** Sistema valida permissão `NOT.PREFERENCIAS.MANAGE`

**FP-UC02-003:** Sistema carrega preferências atuais do usuário da tabela `NotificacaoPreferencia`

**FP-UC02-004:** Sistema exibe grid de configuração com estrutura:

| Tipo de Notificação | Email | SMS | Push | WhatsApp | InApp |
|---------------------|-------|-----|------|----------|-------|
| Aprovações Pendentes | ✅ | ❌ | ✅ | ❌ | ✅ |
| Faturas Vencidas | ✅ | ✅ | ❌ | ❌ | ✅ |
| Alertas de Sistema | ✅ | ❌ | ✅ | ❌ | ✅ |
| Mensagens de Chat | ❌ | ❌ | ✅ | ✅ | ✅ |
| Relatórios Prontos | ✅ | ❌ | ❌ | ❌ | ✅ |

**FP-UC02-005:** Usuário altera checkboxes conforme preferência

**FP-UC02-006:** Usuário clica em "Salvar Preferências"

**FP-UC02-007:** Sistema valida regras:
- Ao menos UM canal deve estar ativo para cada tipo de notificação
- Notificações de conformidade obrigatórias NÃO podem ser desabilitadas (checkboxes desabilitados visualmente)

**FP-UC02-008:** Sistema salva alterações:
```sql
MERGE INTO NotificacaoPreferencia AS target
USING @Preferencias AS source
ON target.UsuarioId = @UsuarioId AND target.TipoNotificacao = source.Tipo
WHEN MATCHED THEN
  UPDATE SET CanaisAtivos = source.Canais
WHEN NOT MATCHED THEN
  INSERT (Id, EmpresaId, UsuarioId, TipoNotificacao, CanaisAtivos, DataCriacao)
  VALUES (NEWID(), @EmpresaId, @UsuarioId, source.Tipo, source.Canais, GETDATE());
```

**FP-UC02-009:** Sistema registra alteração em auditoria (tabela `AuditLog`)

**FP-UC02-010:** Sistema exibe mensagem de sucesso: "Preferências salvas com sucesso"

**FP-UC02-011:** Caso de Uso concluído com sucesso

---

## Fluxos Alternativos

**FA-UC02-001:** Desabilitar TODOS os Canais de um Tipo
- Passo FP-UC02-005
- Usuário desmarca todos checkboxes de uma linha (ex: "Relatórios Prontos")
- Sistema exibe aviso: "Ao menos um canal deve estar ativo. Recomendamos manter InApp ativo."
- Usuário confirma
- Sistema aceita configuração (usuário NÃO receberá notificações desse tipo)
- Retorna ao FP-UC02-008

**FA-UC02-002:** Habilitar Canal Que Requer Configuração
- Passo FP-UC02-005
- Usuário marca checkbox "SMS"
- Sistema valida se usuário possui número de telefone cadastrado
- Se NÃO possui: sistema exibe modal "Para receber SMS, cadastre seu número de telefone"
- Usuário cadastra telefone ou cancela
- Retorna ao FP-UC02-005

**FA-UC02-003:** Configuração Rápida por Templates
- Passo FP-UC02-004
- Sistema exibe botões de template:
  - "Todas InApp" → marca apenas InApp para todos tipos
  - "Email + InApp" → marca Email e InApp para todos tipos
  - "Silencioso" → desmarca tudo (exceto conformidade obrigatórias)
  - "Máximo" → marca TODOS canais para TODOS tipos
- Usuário clica em template
- Sistema aplica configuração automaticamente
- Usuário pode ajustar individualmente
- Retorna ao FP-UC02-006

**FA-UC02-004:** Administrador Configura Preferências de Outro Usuário
- Passo FP-UC02-001
- Administrador acessa "Usuários → [Usuário] → Notificações"
- Sistema valida se logado é Administrador
- Sistema carrega preferências do usuário selecionado
- Fluxo continua normalmente
- Sistema registra em auditoria: "Admin [Nome] alterou preferências de [Usuário]"
- Retorna ao FP-UC02-011

---

## Fluxos de Exceção

**FE-UC02-001:** Usuário Sem Permissão
- Passo FP-UC02-002
- Sistema valida que usuário NÃO possui permissão `NOT.PREFERENCIAS.MANAGE`
- Sistema retorna HTTP 403 Forbidden
- Sistema exibe mensagem: "Você não tem permissão para configurar preferências de notificação"
- Caso de Uso encerrado

**FE-UC02-002:** Tentar Desabilitar Notificação de Conformidade Obrigatória
- Passo FP-UC02-007
- Usuário tenta desmarcar canal de notificação marcada como `isComplianceRequired = true`
- Sistema rejeita alteração
- Sistema exibe mensagem: "Esta notificação é obrigatória por conformidade e não pode ser desabilitada"
- Checkboxes de conformidade ficam desabilitados (apenas leitura)
- Retorna ao FP-UC02-005

**FE-UC02-003:** Erro ao Salvar Preferências
- Passo FP-UC02-008
- Sistema falha ao salvar no banco (timeout, deadlock)
- Sistema retorna HTTP 500 Internal Server Error
- Sistema exibe mensagem: "Erro ao salvar preferências. Tente novamente."
- Sistema registra exceção em log de erros
- Caso de Uso encerrado

**FE-UC02-004:** Canal Indisponível (Provider Não Configurado)
- Passo FP-UC02-005
- Usuário tenta habilitar WhatsApp mas WhatsApp Business API não está configurada no sistema
- Sistema exibe aviso: "WhatsApp Business API não está disponível no momento. Entre em contato com o administrador."
- Checkbox de WhatsApp fica desabilitado visualmente
- Retorna ao FP-UC02-005

---

## Regras de Negócio Aplicadas

**RN-UC-02-001:** Ao Menos Um Canal Ativo (Recomendação, NÃO Obrigatório)
- **Origem:** UX best practice
- **Descrição:** Recomendado que usuário mantenha ao menos InApp ativo para não perder notificações
- **Implementação:** Aviso visual, MAS permite desabilitar todos se usuário confirmar

**RN-UC-02-002:** Notificações de Conformidade Não Podem Ser Desabilitadas
- **Origem:** RN-NOT-066-12
- **Descrição:** Tipos de notificação com flag `isComplianceRequired = true` SEMPRE enviam para TODOS canais (usuário não pode desabilitar)
- **Implementação:** Checkboxes desabilitados visualmente + validação backend

**RN-UC-02-003:** Multi-Tenancy em Preferências
- **Origem:** Padrão arquitetural
- **Descrição:** Preferências são isoladas por `EmpresaId`
- **Validação:** Query DEVE incluir `WHERE EmpresaId = @EmpresaIdUsuario`

**RN-UC-02-004:** Auditoria de Alterações de Preferências
- **Origem:** LGPD / GDPR compliance
- **Descrição:** TODAS alterações de preferências DEVEM ser registradas em `AuditLog`
- **Campos:** `UsuarioId`, `Acao = "PreferenciasAlteradas"`, `ValorAnterior`, `ValorNovo`, `DataAlteracao`

---

## Critérios de Aceite

**CA-UC02-001:** Preferências Salvas com Sucesso
- **Dado que** usuário possui permissão `NOT.PREFERENCIAS.MANAGE`
- **E** altera preferências: Aprovações = Email + InApp
- **Quando** clica em "Salvar"
- **Então** sistema salva em `NotificacaoPreferencia`
- **E** próximas notificações de Aprovações enviam APENAS via Email e InApp
- **E** SMS, Push e WhatsApp NÃO recebem notificações de Aprovações

**CA-UC02-002:** Notificação de Conformidade Não Pode Ser Desabilitada
- **Dado que** tipo "Termos de Uso Atualizados" tem `isComplianceRequired = true`
- **Quando** usuário acessa tela de preferências
- **Então** checkboxes dessa linha estão TODOS marcados E desabilitados
- **E** tooltip exibe: "Notificação obrigatória por conformidade"
- **E** usuário NÃO consegue desmarcar

**CA-UC02-003:** Aviso ao Desabilitar Todos Canais
- **Dado que** usuário desmarca TODOS checkboxes de "Relatórios Prontos"
- **Quando** tenta salvar
- **Então** sistema exibe modal de confirmação: "Você não receberá notificações de Relatórios Prontos. Tem certeza?"
- **E** usuário confirma
- **E** sistema salva configuração

**CA-UC02-004:** Template "Silencioso" Aplicado Corretamente
- **Dado que** usuário clica em template "Silencioso"
- **Quando** sistema aplica configuração
- **Então** TODOS checkboxes são desmarcados
- **EXCETO** notificações de conformidade obrigatórias (permanecem marcados)

**CA-UC02-005:** Alteração Registrada em Auditoria
- **Dado que** usuário altera preferências de Email em "Faturas Vencidas"
- **Quando** salva alterações
- **Então** sistema cria registro em `AuditLog` com:
  - `Acao = "PreferenciasNotificacaoAlteradas"`
  - `ValorAnterior = "Email,SMS,InApp"`
  - `ValorNovo = "SMS,InApp"`
  - `UsuarioId`, `EmpresaId`, `DataAlteracao`

**CA-UC02-006:** Erro 403 para Usuário Sem Permissão
- **Dado que** usuário NÃO possui permissão `NOT.PREFERENCIAS.MANAGE`
- **Quando** tenta acessar tela de preferências
- **Então** sistema retorna HTTP 403 Forbidden
- **E** exibe mensagem de permissão negada

---

# UC03: Configurar Quiet Hours

**Cobertura:** F-NOT-066-03 (Configurar Quiet Hours)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

---

## Objetivo

Permitir que usuários configurem horários de silêncio (quiet hours) durante os quais notificações com prioridade Baixa ou Normal NÃO serão enviadas, sendo acumuladas para envio posterior (fim do período de silêncio).

---

## Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `NOT.QUIET_HOURS.MANAGE`

---

## Pós-condições

- Quiet hours salvos na tabela `NotificacaoPreferencia` (campo `QuietHoursInicio`, `QuietHoursFim`)
- Notificações Baixa/Normal agendadas para envio após fim do quiet hours
- Notificações Urgentes e Críticas SEMPRE enviadas (ignoram quiet hours)

---

## Atores

- **Principal:** Usuário comum (configura próprio quiet hours)
- **Secundários:** Administrador (pode configurar quiet hours globais ou de outros usuários)

---

## Fluxo Principal

**FP-UC03-001:** Usuário acessa "Configurações → Notificações → Horários de Silêncio"

**FP-UC03-002:** Sistema valida permissão `NOT.QUIET_HOURS.MANAGE`

**FP-UC03-003:** Sistema carrega configuração atual do usuário (padrão: 22h-8h se não configurado)

**FP-UC03-004:** Sistema exibe formulário:
- **Ativar Quiet Hours:** (toggle ON/OFF)
- **Hora Início:** (time picker - ex: 22:00)
- **Hora Fim:** (time picker - ex: 08:00)
- **Aplicar a:** (checkboxes)
  - ☑ Notificações Baixa Prioridade
  - ☑ Notificações Normal Prioridade
  - ☐ Notificações Alta Prioridade (desabilitado - sempre envia)
  - ☐ Notificações Urgentes (desabilitado - sempre envia)
  - ☐ Notificações Críticas (desabilitado - sempre envia)
- **Enviar acumuladas às:** (time picker - padrão: mesmo horário que "Hora Fim")

**FP-UC03-005:** Usuário ajusta configurações conforme preferência

**FP-UC03-006:** Usuário clica em "Salvar"

**FP-UC03-007:** Sistema valida regras:
- `HoraInicio` < `HoraFim` (se no mesmo dia) OU `HoraInicio` > `HoraFim` (se atravessa meia-noite)
- Exemplo válido: 22:00 - 08:00 (atravessa meia-noite)
- Exemplo válido: 14:00 - 17:00 (mesmo dia - pausa durante trabalho)

**FP-UC03-008:** Sistema salva configuração:
```sql
UPDATE NotificacaoPreferencia
SET QuietHoursAtivo = @Ativo,
    QuietHoursInicio = @HoraInicio,
    QuietHoursFim = @HoraFim,
    QuietHoursEnviarAcumuladasAs = @HoraEnvio,
    DataAlteracao = GETDATE()
WHERE UsuarioId = @UsuarioId AND EmpresaId = @EmpresaId
```

**FP-UC03-009:** Sistema agenda job Hangfire recorrente para executar no horário especificado em `QuietHoursEnviarAcumuladasAs`

**FP-UC03-010:** Sistema registra alteração em auditoria

**FP-UC03-011:** Sistema exibe mensagem de sucesso: "Quiet hours configurado com sucesso. Notificações de baixa e normal prioridade não serão enviadas entre 22h e 8h."

**FP-UC03-012:** Caso de Uso concluído com sucesso

---

## Fluxos Alternativos

**FA-UC03-001:** Desativar Quiet Hours
- Passo FP-UC03-005
- Usuário desmarca toggle "Ativar Quiet Hours"
- Sistema desabilita campos de hora (visualmente cinza)
- Usuário salva
- Sistema atualiza `QuietHoursAtivo = false`
- Próximas notificações serão enviadas imediatamente (independente de prioridade)
- Retorna ao FP-UC03-012

**FA-UC03-002:** Quiet Hours Que Atravessa Meia-Noite
- Passo FP-UC03-005
- Usuário configura Início = 22:00, Fim = 08:00
- Sistema detecta que Início > Fim (atravessa meia-noite)
- Sistema exibe preview: "Quiet hours ativo das 22h de hoje até 8h de amanhã (10 horas de silêncio)"
- Usuário confirma
- Sistema salva corretamente
- Lógica de validação no backend:
  ```csharp
  bool IsWithinQuietHours(TimeSpan now, TimeSpan inicio, TimeSpan fim)
  {
      if (inicio < fim) // Mesmo dia
          return now >= inicio && now < fim;
      else // Atravessa meia-noite
          return now >= inicio || now < fim;
  }
  ```
- Retorna ao FP-UC03-008

**FA-UC03-003:** Administrador Configura Quiet Hours Globais
- Passo FP-UC03-001
- Administrador acessa "Configurações → Sistema → Quiet Hours Globais"
- Sistema valida permissão de Administrador
- Sistema exibe opção "Aplicar quiet hours padrão para TODOS novos usuários"
- Administrador configura: Início = 22:00, Fim = 08:00
- Sistema salva como configuração global
- Novos usuários criados herdam essa configuração
- Usuários existentes NÃO são afetados (podem ter customizado)
- Retorna ao FP-UC03-012

**FA-UC03-004:** Testar Configuração de Quiet Hours
- Passo FP-UC03-006
- Usuário clica em botão "Testar Configuração"
- Sistema exibe simulação:
  - "Agora são 15:30. Quiet hours está INATIVO (envio normal)."
  - "Às 22:00, quiet hours será ATIVADO."
  - "Notificações Baixa/Normal serão acumuladas até 08:00."
  - "Notificações Urgentes/Críticas serão enviadas normalmente."
- Usuário visualiza simulação e confirma
- Retorna ao FP-UC03-006

---

## Fluxos de Exceção

**FE-UC03-001:** Usuário Sem Permissão
- Passo FP-UC03-002
- Sistema valida que usuário NÃO possui permissão `NOT.QUIET_HOURS.MANAGE`
- Sistema retorna HTTP 403 Forbidden
- Sistema exibe mensagem: "Você não tem permissão para configurar quiet hours"
- Caso de Uso encerrado

**FE-UC03-002:** Horário Inválido
- Passo FP-UC03-007
- Usuário configura Início = 08:00, Fim = 08:00 (mesmo horário)
- Sistema valida e rejeita
- Sistema exibe mensagem: "Horários de início e fim não podem ser iguais"
- Retorna ao FP-UC03-005

**FE-UC03-003:** Quiet Hours Muito Longo (>18h)
- Passo FP-UC03-007
- Usuário configura Início = 18:00, Fim = 13:00 (19 horas de silêncio)
- Sistema detecta duração >18h
- Sistema exibe aviso: "Quiet hours muito longo (19 horas). Recomendamos máximo 12 horas. Deseja continuar?"
- Usuário confirma ou ajusta
- Se confirmar: sistema salva normalmente
- Retorna ao FP-UC03-008

**FE-UC03-004:** Erro ao Salvar Configuração
- Passo FP-UC03-008
- Sistema falha ao salvar no banco (timeout, deadlock)
- Sistema retorna HTTP 500 Internal Server Error
- Sistema exibe mensagem: "Erro ao salvar quiet hours. Tente novamente."
- Sistema registra exceção em log de erros
- Caso de Uso encerrado

---

## Regras de Negócio Aplicadas

**RN-UC-03-001:** Quiet Hours Aplica Apenas a Prioridades Baixa e Normal
- **Origem:** RN-NOT-066-03
- **Descrição:** Notificações Urgentes e Críticas SEMPRE são enviadas, independente de quiet hours
- **Implementação:** Validação backend: `IF @Prioridade IN ('Urgente', 'Critica') THEN ignorar quiet hours`

**RN-UC-03-002:** Notificações Acumuladas Durante Quiet Hours
- **Origem:** RN-NOT-066-03
- **Descrição:** Notificações Baixa/Normal criadas durante quiet hours são marcadas como "AgendadoQuietHours" e enviadas no horário especificado em `QuietHoursEnviarAcumuladasAs`
- **Implementação:** Job Hangfire recorrente executa diariamente no horário configurado

**RN-UC-03-003:** Quiet Hours Padrão para Novos Usuários
- **Origem:** UX best practice
- **Descrição:** Novos usuários criados no sistema herdam quiet hours padrão (22h-8h) configurado pelo Administrador
- **Implementação:** Trigger ou lógica em `CreateUsuarioCommand` copia configuração global

**RN-UC-03-004:** Notificações de Conformidade Ignoram Quiet Hours
- **Origem:** RN-NOT-066-12
- **Descrição:** Notificações com `isComplianceRequired = true` SEMPRE são enviadas, independente de quiet hours
- **Implementação:** Validação backend: `IF @IsComplianceRequired = true THEN ignorar quiet hours`

---

## Critérios de Aceite

**CA-UC03-001:** Quiet Hours Configurado com Sucesso
- **Dado que** usuário configura Início = 22:00, Fim = 08:00
- **Quando** salva configuração
- **Então** sistema atualiza `NotificacaoPreferencia` com horários
- **E** próximas notificações Baixa/Normal criadas entre 22h-8h são agendadas para 08:00

**CA-UC03-002:** Notificação Baixa Prioridade Agendada Durante Quiet Hours
- **Dado que** usuário tem quiet hours = 22h-8h
- **E** são 23:00 (dentro de quiet hours)
- **Quando** sistema cria notificação com prioridade = "Normal"
- **Então** sistema NÃO envia imediatamente
- **E** marca `Status = "AgendadoQuietHours"`
- **E** agenda envio para 08:00

**CA-UC03-003:** Notificação Urgente Ignora Quiet Hours
- **Dado que** usuário tem quiet hours = 22h-8h
- **E** são 02:00 (dentro de quiet hours)
- **Quando** sistema cria notificação com prioridade = "Urgente"
- **Então** sistema envia IMEDIATAMENTE
- **E** marca `Status = "Enviado"`
- **E** NÃO agenda para depois

**CA-UC03-004:** Job Envia Notificações Acumuladas no Horário Configurado
- **Dado que** usuário tem 5 notificações agendadas com `Status = "AgendadoQuietHours"`
- **E** quiet hours fim = 08:00
- **Quando** job Hangfire executa às 08:00
- **Então** sistema envia TODAS as 5 notificações acumuladas
- **E** marca `Status = "Enviado"`
- **E** atualiza `DataEnvio = 08:00`

**CA-UC03-005:** Quiet Hours Que Atravessa Meia-Noite Funciona Corretamente
- **Dado que** usuário configura Início = 22:00, Fim = 08:00
- **E** são 23:30 (após meia-noite de ontem)
- **Quando** sistema valida quiet hours
- **Então** `IsWithinQuietHours() = true` (está dentro do período)
- **E** notificações Baixa/Normal NÃO são enviadas

**CA-UC03-006:** Desativar Quiet Hours Envia Notificações Normalmente
- **Dado que** usuário tinha quiet hours ativo
- **E** desativa quiet hours (toggle OFF)
- **Quando** salva configuração
- **Então** sistema atualiza `QuietHoursAtivo = false`
- **E** próximas notificações são enviadas IMEDIATAMENTE (mesmo às 02:00)

**CA-UC03-007:** Erro ao Configurar Horários Iguais
- **Dado que** usuário configura Início = 10:00, Fim = 10:00
- **Quando** tenta salvar
- **Então** sistema valida e rejeita
- **E** exibe mensagem: "Horários de início e fim não podem ser iguais"
- **E** NÃO salva configuração

---

# UC04: Marcar Notificação como Lida/Não Lida

**Cobertura:** F-NOT-066-05 (Marcar Notificação como Lida/Não Lida)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Permitir que usuários marquem notificações in-app como lidas ou não lidas manualmente, além da marcação automática ao abrir detalhes.

## Pré-condições
- Usuário autenticado
- Permissão `NOT.NOTIFICACOES.MARK_READ`
- Notificação pertence ao usuário logado

## Pós-condições
- Status de leitura atualizado no banco
- Contador de não lidas atualizado no header
- Alteração registrada em auditoria

## Atores
- **Principal:** Usuário comum

## Fluxo Principal

**FP-UC04-001:** Usuário visualiza lista de notificações (UC00)

**FP-UC04-002:** Usuário clica com botão direito em notificação não lida

**FP-UC04-003:** Sistema exibe menu contextual com opção "Marcar como lida"

**FP-UC04-004:** Usuário seleciona "Marcar como lida"

**FP-UC04-005:** Sistema envia comando `MarkNotificationAsReadCommand` com `notificacaoId`

**FP-UC04-006:** Sistema valida que notificação pertence ao usuário logado

**FP-UC04-007:** Sistema atualiza:
```sql
UPDATE Notificacao
SET IsLida = true,
    DataLeitura = GETDATE()
WHERE Id = @NotificacaoId AND UsuarioDestinatarioId = @UsuarioId
```

**FP-UC04-008:** Sistema decrementa contador de não lidas no header

**FP-UC04-009:** Sistema atualiza visualmente ícone da notificação (remove badge "não lida")

**FP-UC04-010:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC04-001:** Marcar Notificação Lida como Não Lida
- Passo FP-UC04-002
- Usuário clica com botão direito em notificação lida
- Sistema exibe opção "Marcar como não lida"
- Sistema atualiza `IsLida = false, DataLeitura = NULL`
- Sistema incrementa contador de não lidas
- Retorna ao FP-UC04-010

**FA-UC04-002:** Marcar Todas Como Lidas (Ação em Massa)
- Passo FP-UC04-001
- Usuário clica em botão "Marcar todas como lidas"
- Sistema confirma: "Marcar {count} notificações como lidas?"
- Sistema executa UPDATE em lote para todas notificações não lidas do usuário
- Sistema zera contador de não lidas
- Retorna ao FP-UC04-010

**FA-UC04-003:** Marcar Automaticamente ao Abrir Detalhes
- Passo FP-UC04-001
- Usuário clica em notificação não lida (abre modal de detalhes)
- Sistema marca automaticamente como lida (UC00-FA-008)
- Retorna ao FP-UC04-010

## Fluxos de Exceção

**FE-UC04-001:** Notificação Não Pertence ao Usuário
- Passo FP-UC04-006
- Sistema valida que `UsuarioDestinatarioId` ≠ `UsuarioLogadoId`
- Sistema retorna HTTP 403 Forbidden
- Sistema exibe mensagem: "Você não tem permissão para marcar esta notificação"
- Caso de Uso encerrado

**FE-UC04-002:** Notificação Não Existe
- Passo FP-UC04-006
- Sistema valida que `notificacaoId` não existe ou foi deletada
- Sistema retorna HTTP 404 Not Found
- Sistema exibe mensagem: "Notificação não encontrada"
- Caso de Uso encerrado

## Regras de Negócio Aplicadas

**RN-UC-04-001:** Isolamento Multi-Tenant
- Usuário APENAS pode marcar notificações do seu `EmpresaId`

**RN-UC-04-002:** Marcação Automática ao Abrir Detalhes
- Notificações in-app são marcadas como lidas automaticamente ao abrir modal de detalhes

**RN-UC-04-003:** Auditoria de Marcação Manual
- Marcações manuais (não automáticas) devem ser registradas em auditoria

## Critérios de Aceite

**CA-UC04-001:** Marcar Como Lida Atualiza Status
- **Dado que** notificação está com `IsLida = false`
- **Quando** usuário marca como lida
- **Então** `IsLida = true` e `DataLeitura = now()`
- **E** contador de não lidas decrementa

**CA-UC04-002:** Marcar Como Não Lida Reverte Status
- **Dado que** notificação está com `IsLida = true`
- **Quando** usuário marca como não lida
- **Então** `IsLida = false` e `DataLeitura = NULL`
- **E** contador de não lidas incrementa

**CA-UC04-003:** Marcar Todas Como Lidas Funciona em Lote
- **Dado que** usuário tem 50 notificações não lidas
- **Quando** clica "Marcar todas como lidas"
- **Então** sistema atualiza TODAS em lote
- **E** contador de não lidas = 0

---

# UC05: Executar Quick Actions em Notificações

**Cobertura:** F-NOT-066-06 (Executar Quick Actions em Notificações)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Permitir execução de ações rápidas diretamente da notificação sem abrir o sistema completo (ex: Aprovar, Rejeitar, Ver Detalhes).

## Pré-condições
- Usuário autenticado
- Notificação possui quick actions configuradas
- Usuário possui permissão para executar a ação (herda da permissão da ação)

## Pós-condições
- Ação executada com sucesso
- Notificação marcada como `ActionExecuted`
- Resultado da ação exibido ao usuário

## Atores
- **Principal:** Usuário comum

## Fluxo Principal

**FP-UC05-001:** Usuário recebe notificação in-app via SignalR com quick actions

**FP-UC05-002:** Sistema exibe toast notification com botões de ação:
- Exemplo: "Você tem uma nova aprovação pendente" + [Aprovar] [Rejeitar] [Ver Detalhes]

**FP-UC05-003:** Usuário clica em botão de ação (ex: "Aprovar")

**FP-UC05-004:** Sistema carrega `QuickAction` do JSON da notificação:
```json
{
  "tipo": "Aprovar",
  "endpoint": "/api/aprovacoes/123/aprovar",
  "metodo": "POST",
  "payload": {"motivo": "Aprovado via notificação"},
  "confirmacao": true
}
```

**FP-UC05-005:** Se `confirmacao = true`: sistema exibe modal "Confirma aprovação?"

**FP-UC05-006:** Usuário confirma

**FP-UC05-007:** Sistema executa requisição HTTP:
```http
POST /api/aprovacoes/123/aprovar
Authorization: Bearer {token}
Content-Type: application/json

{"motivo": "Aprovado via notificação"}
```

**FP-UC05-008:** Sistema recebe resposta HTTP 200 OK

**FP-UC05-009:** Sistema atualiza notificação:
```sql
UPDATE Notificacao
SET ActionExecuted = true,
    ActionType = 'Aprovar',
    ActionTimestamp = GETDATE()
WHERE Id = @NotificacaoId
```

**FP-UC05-010:** Sistema exibe mensagem de sucesso: "Aprovação realizada com sucesso"

**FP-UC05-011:** Sistema remove notificação da lista ou marca visualmente como processada

**FP-UC05-012:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC05-001:** Ação "Ver Detalhes"
- Passo FP-UC05-003
- Usuário clica "Ver Detalhes"
- Sistema redireciona para tela específica (ex: `/aprovacoes/123`)
- Sistema marca notificação como lida
- Retorna ao FP-UC05-012

**FA-UC05-002:** Múltiplas Quick Actions
- Passo FP-UC05-002
- Notificação possui 3 ações: [Aprovar] [Rejeitar] [Adiar]
- Sistema exibe TODAS as ações como botões
- Usuário escolhe uma ação
- Fluxo continua normalmente
- Retorna ao FP-UC05-007

**FA-UC05-003:** Ação Requer Entrada do Usuário
- Passo FP-UC05-005
- Quick action tem campo `requiresInput = true`
- Sistema exibe modal com campo de texto: "Motivo da rejeição:"
- Usuário digita motivo
- Sistema inclui input no payload da requisição
- Retorna ao FP-UC05-007

## Fluxos de Exceção

**FE-UC05-001:** Usuário Sem Permissão para Executar Ação
- Passo FP-UC05-007
- Backend retorna HTTP 403 Forbidden
- Sistema exibe mensagem: "Você não tem permissão para aprovar"
- Sistema NÃO marca notificação como `ActionExecuted`
- Caso de Uso encerrado

**FE-UC05-002:** Recurso Não Existe Mais
- Passo FP-UC05-007
- Backend retorna HTTP 404 Not Found
- Sistema exibe mensagem: "Aprovação não encontrada. Pode ter sido processada por outro usuário."
- Sistema marca notificação como obsoleta
- Caso de Uso encerrado

**FE-UC05-003:** Falha ao Executar Ação
- Passo FP-UC05-007
- Backend retorna HTTP 500 Internal Server Error
- Sistema exibe mensagem: "Erro ao processar ação. Tente novamente."
- Sistema NÃO marca como `ActionExecuted`
- Sistema mantém notificação na lista
- Caso de Uso encerrado

**FE-UC05-004:** Timeout na Requisição
- Passo FP-UC05-007
- Requisição HTTP excede timeout (30 segundos)
- Sistema exibe mensagem: "Timeout ao processar ação. Verifique se foi processada."
- Sistema sugere verificar manualmente
- Caso de Uso encerrado

## Regras de Negócio Aplicadas

**RN-UC-05-001:** Permissão Herdada da Ação
- Quick action herda permissão do endpoint chamado
- Se endpoint requer `APV.APROVACOES.APPROVE`, usuário DEVE ter essa permissão

**RN-UC-05-002:** Ação Executada Apenas Uma Vez
- Notificação com `ActionExecuted = true` NÃO pode executar quick action novamente
- Botões ficam desabilitados após execução

**RN-UC-05-003:** Timeout Padrão de 30 Segundos
- Requisições HTTP de quick actions têm timeout de 30 segundos
- Após timeout, usuário deve verificar manualmente se ação foi processada

## Critérios de Aceite

**CA-UC05-001:** Quick Action Executada com Sucesso
- **Dado que** notificação possui quick action "Aprovar"
- **Quando** usuário clica "Aprovar"
- **Então** sistema executa `POST /api/aprovacoes/123/aprovar`
- **E** marca `ActionExecuted = true`
- **E** exibe "Aprovação realizada com sucesso"

**CA-UC05-002:** Erro 403 Exibido Quando Sem Permissão
- **Dado que** usuário NÃO possui permissão para aprovar
- **Quando** clica "Aprovar"
- **Então** sistema retorna HTTP 403
- **E** exibe "Você não tem permissão para aprovar"
- **E** NÃO marca como `ActionExecuted`

**CA-UC05-003:** Ação Não Pode Ser Executada Duas Vezes
- **Dado que** notificação tem `ActionExecuted = true`
- **Quando** usuário tenta clicar novamente
- **Então** botões estão desabilitados
- **E** tooltip exibe "Ação já executada"

---

# UC06: Configurar Agrupamento Inteligente

**Cobertura:** F-NOT-066-07 (Configurar Agrupamento Inteligente)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Permitir configurar regras de agrupamento para consolidar múltiplas notificações do mesmo tipo em uma única notificação agrupada.

## Pré-condições
- Usuário autenticado
- Permissão `NOT.AGRUPAMENTO.CONFIGURE` (Administrador ou Gestor de Notificações)

## Pós-condições
- Regras de agrupamento salvas
- Job background aplica agrupamento automaticamente

## Atores
- **Principal:** Administrador, Gestor de Notificações

## Fluxo Principal

**FP-UC06-001:** Administrador acessa "Configurações → Sistema → Agrupamento de Notificações"

**FP-UC06-002:** Sistema valida permissão `NOT.AGRUPAMENTO.CONFIGURE`

**FP-UC06-003:** Sistema exibe configuração atual:
- **Ativar Agrupamento:** (toggle ON/OFF)
- **Threshold:** Agrupar quando >5 notificações
- **Janela de Tempo:** 30 minutos
- **Tipos de Notificação para Agrupar:** (multi-select)

**FP-UC06-004:** Administrador ajusta configurações

**FP-UC06-005:** Administrador clica "Salvar"

**FP-UC06-006:** Sistema salva em `SistemaConfiguracaoGeral`:
```json
{
  "AgrupamentoAtivo": true,
  "AgrupamentoThreshold": 5,
  "AgrupamentoJanelaMinutos": 30,
  "TiposParaAgrupar": ["AprovacaoPendente", "FaturaVencida"]
}
```

**FP-UC06-007:** Sistema agenda job Hangfire recorrente (executa a cada 5 minutos)

**FP-UC06-008:** Job verifica notificações pendentes e agrupa conforme regras

**FP-UC06-009:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC06-001:** Desabilitar Agrupamento
- Passo FP-UC06-004
- Administrador desmarca toggle "Ativar Agrupamento"
- Sistema desabilita job de agrupamento
- Próximas notificações enviadas individualmente
- Retorna ao FP-UC06-009

**FA-UC06-002:** Testar Agrupamento com Simulação
- Passo FP-UC06-005
- Administrador clica "Simular Agrupamento"
- Sistema cria 10 notificações de teste do mesmo tipo
- Sistema executa job de agrupamento imediatamente
- Sistema exibe resultado: "10 notificações → 1 notificação agrupada"
- Retorna ao FP-UC06-005

## Fluxos de Exceção

**FE-UC06-001:** Usuário Sem Permissão
- Passo FP-UC06-002
- Sistema retorna HTTP 403 Forbidden
- Caso de Uso encerrado

**FE-UC06-002:** Threshold Inválido
- Passo FP-UC06-006
- Administrador configura threshold < 2
- Sistema valida e rejeita
- Sistema exibe: "Threshold deve ser no mínimo 2"
- Retorna ao FP-UC06-004

## Regras de Negócio Aplicadas

**RN-UC-06-001:** Agrupamento Apenas Para Mesmo Tipo e Usuário
- **Origem:** RN-NOT-066-04
- Agrupa APENAS notificações do mesmo `Tipo` para o mesmo `UsuarioDestinatarioId`

**RN-UC-06-002:** Janela de Tempo de 30 Minutos
- **Origem:** RN-NOT-066-04
- Notificações criadas em janela de 30 minutos são candidatas a agrupamento

**RN-UC-06-003:** Threshold de 5 Notificações
- **Origem:** RN-NOT-066-04
- Agrupamento ocorre quando >5 notificações do mesmo tipo na janela de tempo

## Critérios de Aceite

**CA-UC06-001:** Agrupamento Configurado e Ativado
- **Dado que** Administrador configura threshold = 5, janela = 30min
- **Quando** salva configuração
- **Então** job Hangfire é agendado para executar a cada 5 minutos
- **E** próximas notificações são agrupadas conforme regra

**CA-UC06-002:** 6 Notificações São Agrupadas em 1
- **Dado que** sistema cria 6 notificações "AprovacaoPendente" em 10 minutos
- **Quando** job de agrupamento executa
- **Então** sistema cancela 6 notificações individuais
- **E** cria 1 notificação agrupada: "Você tem 6 novas aprovações pendentes"

---

# UC07: Ativar/Desativar Digest Diário

**Cobertura:** F-NOT-066-08 (Ativar/Desativar Digest Diário)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Permitir ativar modo digest onde notificações são consolidadas em um único e-mail diário às 18h.

## Pré-condições
- Usuário autenticado
- Permissão `NOT.DIGEST.MANAGE`

## Pós-condições
- Configuração de digest salva
- Próximas notificações via e-mail consolidadas no digest

## Atores
- **Principal:** Usuário comum, Administrador

## Fluxo Principal

**FP-UC07-001:** Usuário acessa "Configurações → Notificações → Digest Diário"

**FP-UC07-002:** Sistema valida permissão `NOT.DIGEST.MANAGE`

**FP-UC07-003:** Sistema exibe configuração:
- **Ativar Digest Diário:** (toggle ON/OFF)
- **Horário de Envio:** 18:00 (time picker)
- **Incluir Tipos:** (checkboxes - Aprovações, Faturas, Alertas)

**FP-UC07-004:** Usuário ativa toggle e ajusta configurações

**FP-UC07-005:** Usuário clica "Salvar"

**FP-UC07-006:** Sistema atualiza `NotificacaoPreferencia`:
```sql
UPDATE NotificacaoPreferencia
SET DigestDiarioAtivo = true,
    DigestHorarioEnvio = '18:00',
    DigestTiposInclusos = 'AprovacaoPendente,FaturaVencida'
WHERE UsuarioId = @UsuarioId
```

**FP-UC07-007:** Sistema agenda job Hangfire diário para 18h

**FP-UC07-008:** Job consolida notificações do dia e envia e-mail único

**FP-UC07-009:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC07-001:** Desabilitar Digest
- Passo FP-UC07-004
- Usuário desmarca toggle
- Sistema remove job agendado
- Próximas notificações enviadas individualmente
- Retorna ao FP-UC07-009

## Fluxos de Exceção

**FE-UC07-001:** Usuário Sem Permissão
- Passo FP-UC07-002
- Sistema retorna HTTP 403
- Caso de Uso encerrado

## Regras de Negócio Aplicadas

**RN-UC-07-001:** Digest Apenas para E-mails
- Digest aplica APENAS ao canal E-mail
- Outros canais (InApp, SMS) enviam normalmente

**RN-UC-07-002:** Horário de Envio Padrão 18h
- Se não configurado, digest enviado às 18h

## Critérios de Aceite

**CA-UC07-001:** Digest Ativo Consolida Notificações
- **Dado que** usuário ativa digest às 18h
- **E** recebe 10 notificações durante o dia
- **Quando** job executa às 18h
- **Então** sistema envia 1 e-mail com 10 notificações consolidadas

---

# UC08: Rastrear Métricas de Entrega

**Cobertura:** F-NOT-066-09 (Rastrear Métricas de Entrega)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Rastrear métricas de entrega através de webhooks dos providers externos (SendGrid, Twilio, Firebase).

## Pré-condições
- Webhooks configurados nos providers
- Endpoints de webhook públicos no sistema

## Pós-condições
- Métricas registradas no banco
- Dashboard atualizado com dados de entrega

## Atores
- **Principal:** Sistema (automático via webhooks)
- **Secundários:** Administrador, Auditor

## Fluxo Principal

**FP-UC08-001:** Provider externo (SendGrid) dispara webhook após entregar e-mail:
```http
POST /api/webhooks/sendgrid
Content-Type: application/json

{
  "event": "delivered",
  "email": "usuario@example.com",
  "timestamp": 1640000000,
  "sg_message_id": "abc123"
}
```

**FP-UC08-002:** Sistema valida assinatura do webhook (HMAC)

**FP-UC08-003:** Sistema identifica notificação pelo `sg_message_id`

**FP-UC08-004:** Sistema atualiza `NotificacaoMetricaEntrega`:
```sql
INSERT INTO NotificacaoMetricaEntrega (
  NotificacaoId, Canal, Evento, DataEvento
) VALUES (
  @NotificacaoId, 'Email', 'Delivered', GETDATE()
)
```

**FP-UC08-005:** Sistema atualiza status da notificação:
```sql
UPDATE Notificacao
SET StatusEntrega = 'Entregue'
WHERE Id = @NotificacaoId
```

**FP-UC08-006:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC08-001:** Evento "Aberto" (E-mail Aberto)
- Passo FP-UC08-001
- Provider envia evento `opened`
- Sistema registra `Evento = 'Opened'`
- Sistema atualiza `StatusEntrega = 'Aberto'`
- Retorna ao FP-UC08-006

**FA-UC08-002:** Evento "Clicado" (Link Clicado)
- Passo FP-UC08-001
- Provider envia evento `clicked`
- Sistema registra `Evento = 'Clicked'`
- Sistema incrementa métrica de conversão
- Retorna ao FP-UC08-006

## Fluxos de Exceção

**FE-UC08-001:** Assinatura Inválida
- Passo FP-UC08-002
- Sistema valida HMAC e falha
- Sistema retorna HTTP 401 Unauthorized
- Sistema registra tentativa suspeita em log de segurança
- Caso de Uso encerrado

**FE-UC08-002:** Notificação Não Encontrada
- Passo FP-UC08-003
- Sistema não encontra notificação pelo `message_id`
- Sistema registra evento órfão em log
- Sistema retorna HTTP 200 OK (evita retry do provider)
- Caso de Uso encerrado

## Regras de Negócio Aplicadas

**RN-UC-08-001:** Validação de Assinatura Obrigatória
- Todos webhooks DEVEM validar assinatura HMAC
- Rejeitar webhooks sem assinatura válida

**RN-UC-08-002:** Eventos Suportados
- SendGrid: sent, delivered, opened, clicked, bounced, spam
- Twilio: sent, delivered, failed
- Firebase: sent, delivered

## Critérios de Aceite

**CA-UC08-001:** Webhook Válido Registra Métrica
- **Dado que** SendGrid envia webhook `delivered`
- **E** assinatura HMAC é válida
- **Quando** sistema processa webhook
- **Então** sistema registra `NotificacaoMetricaEntrega`
- **E** atualiza `StatusEntrega = 'Entregue'`

---

# UC09: Configurar Retry Policy

**Cobertura:** F-NOT-066-10 (Configurar Retry Policy)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Configurar política de retry automático para falhas de envio com backoff exponencial.

## Pré-condições
- Permissão `NOT.RETRY.CONFIGURE`

## Pós-condições
- Retry policy salva
- Falhas futuras retentam conforme política

## Atores
- **Principal:** Administrador, Gestor de Notificações

## Fluxo Principal

**FP-UC09-001:** Administrador acessa "Configurações → Sistema → Retry Policy"

**FP-UC09-002:** Sistema valida permissão `NOT.RETRY.CONFIGURE`

**FP-UC09-003:** Sistema exibe configuração:
- **Ativar Retry:** (toggle ON/OFF)
- **Tentativas:** 4 (slider 1-10)
- **Backoff:** Exponencial (dropdown: Linear, Exponencial, Fixo)
- **Intervalo Base:** 2 minutos
- **Máximo por Canal:** (checkboxes - Email, SMS, Push, WhatsApp)

**FP-UC09-004:** Administrador ajusta configurações

**FP-UC09-005:** Sistema salva em `SistemaConfiguracaoGeral`

**FP-UC09-006:** Próximas falhas retentam conforme política

**FP-UC09-007:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC09-001:** Desabilitar Retry
- Passo FP-UC09-004
- Administrador desmarca toggle
- Próximas falhas NÃO retentam
- Retorna ao FP-UC09-007

## Regras de Negócio Aplicadas

**RN-UC-09-001:** Backoff Exponencial Padrão
- **Origem:** RN-NOT-066-05
- Tentativas: imediata, +2min, +4min, +8min

**RN-UC-09-002:** Máximo 4 Tentativas
- Após 4 falhas, marcar como "Falha Permanente"

## Critérios de Aceite

**CA-UC09-001:** Retry Configurado Retenta Envio
- **Dado que** retry policy ativa com 4 tentativas
- **Quando** envio falha (HTTP 503)
- **Então** sistema retenta após 2min, 4min, 8min
- **E** após 4 falhas marca "Falha Permanente"

---

# UC10: Aplicar Rate Limiting Automático

**Cobertura:** F-NOT-066-11 (Aplicar Rate Limiting)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Aplicar limite automático de 50 notificações por usuário por 24h para prevenir spam.

## Pré-condições
- Sistema configurado com rate limiting ativo

## Pós-condições
- Notificações bloqueadas quando limite excedido
- Exceção para notificações de conformidade

## Atores
- **Principal:** Sistema (automático)

## Fluxo Principal

**FP-UC10-001:** Sistema recebe comando para enviar notificação

**FP-UC10-002:** Sistema conta notificações do usuário nas últimas 24h:
```sql
SELECT COUNT(*) FROM Notificacao
WHERE UsuarioDestinatarioId = @UsuarioId
  AND DataEnvio >= DATEADD(hour, -24, GETDATE())
```

**FP-UC10-003:** Se count >= 50 E `isComplianceRequired = false`:
- Sistema bloqueia envio
- Retorna HTTP 429 Too Many Requests

**FP-UC10-004:** Se count < 50 OU `isComplianceRequired = true`:
- Sistema prossegue com envio

**FP-UC10-005:** Caso de Uso concluído

## Regras de Negócio Aplicadas

**RN-UC-10-001:** Limite de 50 Notificações por 24h
- **Origem:** RN-NOT-066-06
- Exceção: notificações de conformidade ignoram limite

## Critérios de Aceite

**CA-UC10-001:** 51ª Notificação Bloqueada
- **Dado que** usuário recebeu 50 notificações em 24h
- **Quando** sistema tenta enviar 51ª
- **Então** sistema retorna HTTP 429
- **E** NÃO envia notificação

---

# UC11: Gerenciar Notificações de Conformidade

**Cobertura:** F-NOT-066-12 (Gerenciar Notificações de Conformidade)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Marcar tipos de notificação como obrigatórias (conformidade) que não podem ser desabilitadas.

## Pré-condições
- Permissão `NOT.COMPLIANCE.MANAGE`

## Pós-condições
- Tipo de notificação marcado como obrigatório
- Usuários não podem desabilitar

## Atores
- **Principal:** Administrador, Compliance Officer

## Fluxo Principal

**FP-UC11-001:** Administrador acessa "Configurações → Sistema → Notificações de Conformidade"

**FP-UC11-002:** Sistema valida permissão `NOT.COMPLIANCE.MANAGE`

**FP-UC11-003:** Sistema exibe lista de tipos de notificação:
| Tipo | Obrigatória | Ações |
|------|-------------|-------|
| Termos de Uso Atualizados | ✅ | Editar |
| Aprovações | ❌ | Editar |

**FP-UC11-004:** Administrador clica "Editar" em tipo "Termos de Uso"

**FP-UC11-005:** Sistema exibe modal com checkbox "Marcar como obrigatória"

**FP-UC11-006:** Administrador marca checkbox e salva

**FP-UC11-007:** Sistema atualiza `TipoNotificacao`:
```sql
UPDATE TipoNotificacao
SET IsComplianceRequired = true
WHERE Id = @TipoId
```

**FP-UC11-008:** Próximas notificações desse tipo ignoram preferências, quiet hours e rate limiting

**FP-UC11-009:** Caso de Uso concluído

## Regras de Negócio Aplicadas

**RN-UC-11-001:** Notificações de Conformidade Não Podem Ser Desabilitadas
- **Origem:** RN-NOT-066-12
- Usuários NÃO podem desabilitar nas preferências

## Critérios de Aceite

**CA-UC11-001:** Tipo Marcado Como Obrigatório
- **Dado que** Administrador marca "Termos de Uso" como obrigatório
- **Quando** salva configuração
- **Então** `IsComplianceRequired = true`
- **E** usuários NÃO podem desabilitar esse tipo

---

# UC12: Dashboard de Métricas de Notificações

**Cobertura:** F-NOT-066-13 (Dashboard de Métricas de Notificações)
**Modelo de Dados:** [MD-RF066](./MD-RF066.yaml)

## Objetivo
Exibir dashboard com métricas agregadas de notificações (total enviadas, taxa de entrega, taxa de abertura).

## Pré-condições
- Permissão `NOT.DASHBOARD.VIEW`

## Pós-condições
- Dashboard exibido com métricas atualizadas

## Atores
- **Principal:** Administrador, Gestor de Notificações, Auditor

## Fluxo Principal

**FP-UC12-001:** Usuário acessa "Notificações → Dashboard"

**FP-UC12-002:** Sistema valida permissão `NOT.DASHBOARD.VIEW`

**FP-UC12-003:** Sistema carrega métricas dos últimos 30 dias

**FP-UC12-004:** Sistema exibe cards:
- **Total Enviadas:** 12.543
- **Taxa de Entrega:** 98.5%
- **Taxa de Abertura (E-mail):** 65.2%
- **Taxa de Conversão (Quick Actions):** 42.1%

**FP-UC12-005:** Sistema exibe gráficos:
- Notificações por Canal (pizza)
- Evolução Temporal (linha)
- Notificações por Tipo (barras)

**FP-UC12-006:** Caso de Uso concluído

## Fluxos Alternativos

**FA-UC12-001:** Filtrar por Período
- Passo FP-UC12-003
- Usuário seleciona "Últimos 7 dias"
- Sistema recarrega métricas
- Retorna ao FP-UC12-004

## Regras de Negócio Aplicadas

**RN-UC-12-001:** Métricas Apenas do Tenant
- Dashboard exibe APENAS dados do `EmpresaId` do usuário

## Critérios de Aceite

**CA-UC12-001:** Dashboard Exibe Métricas Corretas
- **Dado que** sistema enviou 1000 notificações em 30 dias
- **E** 980 foram entregues
- **Quando** Administrador acessa dashboard
- **Então** card "Taxa de Entrega" exibe 98%

---

## Resumo de Cobertura Completa

| UC | Nome | Funcionalidade RF066 | Status |
|----|------|---------------------|--------|
| UC00 | Listar/Visualizar Central | F-NOT-066-04 | ✅ COMPLETO |
| UC01 | Enviar Multi-Canal | F-NOT-066-01 | ✅ COMPLETO |
| UC02 | Configurar Preferências | F-NOT-066-02 | ✅ COMPLETO |
| UC03 | Configurar Quiet Hours | F-NOT-066-03 | ✅ COMPLETO |
| UC04 | Marcar Lida/Não Lida | F-NOT-066-05 | ✅ COMPLETO |
| UC05 | Quick Actions | F-NOT-066-06 | ✅ COMPLETO |
| UC06 | Agrupamento Inteligente | F-NOT-066-07 | ✅ COMPLETO |
| UC07 | Digest Diário | F-NOT-066-08 | ✅ COMPLETO |
| UC08 | Métricas de Entrega | F-NOT-066-09 | ✅ COMPLETO |
| UC09 | Retry Policy | F-NOT-066-10 | ✅ COMPLETO |
| UC10 | Rate Limiting | F-NOT-066-11 | ✅ COMPLETO |
| UC11 | Conformidade | F-NOT-066-12 | ✅ COMPLETO |
| UC12 | Dashboard | F-NOT-066-13 | ✅ COMPLETO |

**Cobertura:** 13/13 funcionalidades (100%)

---

*Documento UC-RF066.md v2.0 completo*
*Gerado conforme CONTRATO-GERACAO-DOCS-UC.md*
*Data: 2025-12-31*

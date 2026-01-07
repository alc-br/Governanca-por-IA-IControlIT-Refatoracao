# UC-RF071 - Casos de Uso - Pesquisa de Satisfação

## UC01: Listar e Configurar Templates de Pesquisa (NPS/CSAT/CES)

### 1. Descrição

Este caso de uso permite que Gestores de Service Desk criem, editem e configurem templates de pesquisas de satisfação com designer visual drag-and-drop suportando 12 tipos de pergunta (NPS 0-10, CSAT Likert 1-5 estrelas, CES 1-7, múltipla escolha, texto livre, escala semântica, matriz), definam triggers automáticos (pós-chamado, SLA violado, agendamento trimestral), configurem canais de envio (e-mail, SMS, in-app, WhatsApp), estabeleçam regras de anonimização LGPD (identificado/pseudonimizado/anonimizado), ajustem throttling anti-fadiga (cooldown padrão 7 dias) e validem critérios de significância estatística (taxa resposta ≥30% e ≥50 respostas absolutas).

### 2. Atores

- Gestor de Service Desk
- Sistema (Backend .NET 10, Azure Cognitive Services, Hangfire, Twilio SMS, WhatsApp Business API)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:pesquisa-satisfacao:gestao`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `SERVICE_DESK_PESQUISA_SATISFACAO` habilitada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa rota `/service-desk/pesquisas/templates` | - |
| 2 | - | Frontend envia `GET /api/pesquisas/templates?clienteId={clienteId}` |
| 3 | - | Backend valida permissão RBAC: `User.HasPermission("service-desk:pesquisa-satisfacao:gestao")` → Se negado: HTTP 403 |
| 4 | - | Backend retorna lista de templates com tipo (NPS_RELACIONAL, CSAT_TRANSACIONAL, CES_PROCESSO), status (Ativo/Inativo), total de envios, taxa de resposta média |
| 5 | - | Frontend renderiza tabela com templates existentes: "NPS Trimestral (Ativo, 3.250 envios, 58% taxa)", "CSAT Pós-Chamado (Ativo, 12.450 envios, 62% taxa)" |
| 6 | Gestor clica em botão "Criar Novo Template" | - |
| 7 | - | Frontend abre modal com wizard 4 passos: (1) Informações Básicas, (2) Perguntas, (3) Triggers, (4) Configurações Avançadas |
| 8 | Gestor preenche Passo 1: Nome "CSAT Pós-Atendimento VIP", Tipo "CSAT_TRANSACIONAL", Descrição "Pesquisa enviada após resolução de chamados de clientes VIP" | - |
| 9 | Gestor avança para Passo 2 - Designer de Perguntas (drag-and-drop) | - |
| 10 | - | Frontend renderiza canvas com sidebar de componentes: [Escala NPS 0-10] [CSAT Estrelas 1-5] [CES 1-7] [Múltipla Escolha] [Texto Livre] [Escala Semântica] [Matriz] |
| 11 | Gestor arrasta componente "CSAT Estrelas 1-5" para canvas | - |
| 12 | - | Frontend exibe propriedades: "Pergunta: [Como você avalia o atendimento recebido?]", "Obrigatório: ☑", "Etiquetas Estrelas: [Muito Insatisfeito, Insatisfeito, Neutro, Satisfeito, Muito Satisfeito]" |
| 13 | Gestor arrasta componente "Texto Livre" abaixo do CSAT | - |
| 14 | - | Frontend exibe propriedades: "Pergunta: [Comentários adicionais (opcional)]", "Obrigatório: ☐", "Min Caracteres: [10]", "Max Caracteres: [2000]" |
| 15 | Gestor salva configuração de perguntas (2 perguntas: CSAT + Texto Livre) | - |
| 16 | Gestor avança para Passo 3 - Configuração de Triggers | - |
| 17 | - | Frontend renderiza formulário: "Disparar pesquisa quando: [Chamado Resolvido ▼]", "Filtros: [Cliente VIP = Sim ▼] [Categoria = Todas ▼]", "Delay após evento: [30] minutos" |
| 18 | Gestor configura trigger: Disparar 30min após resolução de chamados de clientes VIP | - |
| 19 | Gestor avança para Passo 4 - Configurações Avançadas | - |
| 20 | - | Frontend renderiza: "Canais de Envio: ☑ E-mail ☑ SMS ☐ In-App ☐ WhatsApp", "Anonimização: [Pseudonimizado ▼] (correlação com chamado preservada)", "Cooldown (dias): [7]", "Validade Link (dias): [7]", "Idioma: [Detecção Automática ▼]" |
| 21 | Gestor configura: E-mail + SMS, Pseudonimizado (correlação preservada), Cooldown 7 dias, Validade 7 dias | - |
| 22 | Gestor clica em "Salvar Template" | - |
| 23 | - | Frontend envia `POST /api/pesquisas/templates` com body JSON contendo todas as configurações (nome, tipo, perguntas array, trigger config, canais, anonimização, cooldown, validade) |
| 24 | - | **Backend - FluentValidation**: Valida nome único por cliente, tipo válido (enum), perguntas ≥1, trigger configurado, canais ≥1 selecionado |
| 25 | - | **Backend - RN-RF071-004**: Valida conformidade LGPD: Se tipo = NPS_RELACIONAL e anonimização ≠ Anonimizado → HTTP 400 "NPS Relacional deve ser totalmente anônimo conforme Art. 12 LGPD" |
| 26 | - | Backend cria entidade `TemplatePesquisa` com status Inativo (precisa ativação manual), perguntas serializadas em JSON, trigger config, metadata |
| 27 | - | Backend retorna HTTP 201 Created com `TemplatePesquisaDto` contendo Id, Nome, Tipo, Status = Inativo |
| 28 | - | Frontend exibe toast de sucesso: "Template 'CSAT Pós-Atendimento VIP' criado. Ative para começar a enviar pesquisas." |
| 29 | Gestor clica em toggle "Ativar" na lista de templates | - |
| 30 | - | Frontend envia `PATCH /api/pesquisas/templates/{id}/ativar` |
| 31 | - | Backend valida template completo (perguntas, triggers, canais configurados), atualiza Status = Ativo, DataAtivacao = DateTime.UtcNow |
| 32 | - | **Backend - Event**: Publica evento `TemplatePesquisaAtivadoEvent` que registra trigger no Hangfire (RecurringJob ou DelayedJob conforme tipo de trigger) |
| 33 | - | Backend retorna HTTP 200 OK |
| 34 | - | Frontend atualiza status visualmente: badge verde "Ativo desde 28/12/2025 15:30" |

### 5. Fluxos Alternativos

**FA01: Template NPS Relacional Trimestral com Anonimização Total**

- No passo 8, gestor cria template tipo "NPS_RELACIONAL" com nome "NPS Trimestral Q1/2025"
- No passo 11, gestor arrasta componente "Escala NPS 0-10" com pergunta "Qual probabilidade de recomendar nosso serviço? (0=Nada Provável, 10=Extremamente Provável)"
- No passo 17, gestor configura trigger: "Agendamento Recorrente" → "Trimestral" → "Dia 1 de cada trimestre às 09:00" → "Enviar para: Todos os usuários ativos (30.000 emails)"
- No passo 20, frontend força seleção: "Anonimização: [Anonimizado Total ▼] (obrigatório para NPS Relacional)" → Campo desabilitado, não permite alterar
- No passo 25, backend valida RN-RF071-004: tipo = NPS_RELACIONAL e anonimização = Anonimizado → Validação OK
- No passo 32, Hangfire registra RecurringJob com CRON expression "0 9 1 1,4,7,10 *" (dia 1 de jan/abr/jul/out às 09:00)

**FA02: Template com Múltiplas Perguntas e Lógica Condicional**

- No passo 11-14, gestor cria 5 perguntas:
  - P1: CSAT Estrelas 1-5 (obrigatório)
  - P2: Texto Livre "Por que essa avaliação?" (condicional: exibir se CSAT ≤3)
  - P3: Múltipla Escolha "Qual aspecto precisa melhorar?" (opções: Tempo Resposta, Qualidade Técnica, Comunicação) - condicional: exibir se CSAT ≤3
  - P4: NPS 0-10 (sempre exibir)
  - P5: Texto Livre "Comentários finais" (opcional)
- Frontend permite configurar lógica condicional com botão "Adicionar Condição" em cada pergunta
- Backend serializa lógica em JSON: `{ "perguntaId": 2, "condicao": { "perguntaRef": 1, "operador": "<=", "valor": 3 } }`
- Ao renderizar pesquisa para usuário, frontend avalia condições dinamicamente (se usuário responder CSAT 5, perguntas 2 e 3 não aparecem)

**FA03: Validação de Significância Estatística ao Desativar Template**

- Gestor tenta desativar template "NPS Trimestral" que tem pesquisa ativa com apenas 35 respostas de 200 enviadas (17.5% taxa)
- Backend valida RN-RF071-006: `ValidadorSignificanciaEstatistica.PesquisaEhValida(enviados: 200, respondidos: 35)` → false (taxa <30% e respostas <50)
- Backend retorna HTTP 400 com warning: `{ "warning": "SIGNIFICANCIA_INSUFICIENTE", "message": "Pesquisa possui apenas 35 respostas (17.5% taxa). Aguarde atingir 30% taxa OU 50 respostas para resultados estatisticamente válidos.", "permiteDesativar": true }`
- Frontend exibe modal de confirmação: "⚠️ Atenção: Pesquisa não atingiu significância estatística. Resultados podem estar enviesados. Deseja mesmo desativar? [Aguardar Mais Respostas] [Desativar Mesmo Assim]"
- Se gestor confirmar, backend desativa template e marca pesquisa com flag `SignificanciaInsuficiente = true`

**FA04: Exportação de Template para Reutilização em Outro Cliente**

- Gestor clica em botão "Exportar Template" no template "CSAT Pós-Chamado"
- Frontend envia `GET /api/pesquisas/templates/{id}/exportar`
- Backend serializa template completo em JSON (perguntas, triggers, configurações) EXCLUINDO dados sensíveis (IDs internos, ClienteId, dados de respostas)
- Backend retorna JSON file download: `CSAT-Pos-Chamado-Template-2025-12-28.json`
- Gestor pode importar JSON em outro cliente via botão "Importar Template" → Frontend envia `POST /api/pesquisas/templates/importar` com file upload
- Backend valida JSON schema, cria novo template com novo ClienteId, status Inativo (precisa configuração final antes de ativar)

### 6. Exceções

**EX01: Usuário Sem Permissão de Gestão de Pesquisas**

- No passo 3, backend valida permissão e detecta que usuário não tem `service-desk:pesquisa-satisfacao:gestao`
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Apenas Gestores de Service Desk podem gerenciar templates de pesquisa" }`
- Frontend exibe toast de erro e redireciona para dashboard

**EX02: Violação LGPD - NPS Relacional Sem Anonimização Total**

- No passo 25, gestor tenta criar template tipo "NPS_RELACIONAL" com anonimização "Pseudonimizado"
- Backend valida RN-RF071-004: `if (Tipo == "NPS_RELACIONAL" && Anonimizacao != NivelAnonimizacao.Anonimizado)` → true (violação)
- Backend lança `LGPDViolationException` retornando HTTP 400 com body: `{ "error": "LGPD_VIOLATION", "message": "NPS Relacional deve ser totalmente anônimo conforme Art. 12 LGPD. Altere nível de anonimização para 'Anonimizado Total'." }`
- Frontend exibe erro inline no campo anonimização com ícone ⚠️ e explicação da regra LGPD

**EX03: Template Sem Perguntas Configuradas**

- No passo 15, gestor tenta salvar template sem adicionar nenhuma pergunta ao canvas (perguntas array vazio)
- No passo 24, FluentValidation detecta: `RuleFor(x => x.Perguntas).NotEmpty().WithMessage("Template deve ter pelo menos 1 pergunta")` → falha
- Backend retorna HTTP 400 com body: `{ "errors": { "perguntas": ["Template deve ter pelo menos 1 pergunta. Use o designer para adicionar perguntas."] } }`
- Frontend exibe erro no wizard passo 2: "⚠️ Adicione pelo menos uma pergunta antes de continuar"

**EX04: Tentativa de Ativar Template com Trigger Inválido**

- No passo 31, gestor tenta ativar template mas trigger está configurado incorretamente (ex: agendamento trimestral sem data específica)
- Backend valida configuração completa: trigger config JSON válido, campos obrigatórios preenchidos, CRON expression válido (se agendamento)
- Backend retorna HTTP 400 com body: `{ "error": "TRIGGER_INVALIDO", "message": "Trigger de agendamento trimestral requer data específica (dia e hora). Configure no Passo 3 antes de ativar." }`
- Frontend exibe toast de erro com link "Configurar Trigger" que reabre wizard no passo 3

### 7. Pós-condições

- Template de pesquisa criado e armazenado no banco de dados
- Status Ativo/Inativo conforme ação do gestor
- Trigger registrado no Hangfire (se ativado)
- Validação de conformidade LGPD executada
- Metadata de auditoria registrada (quem criou, quando, alterações)

### 8. Regras de Negócio Aplicáveis

- **RN-RF071-004**: Anonimização Configurável por Tipo de Pesquisa (NPS Relacional = anonimizado total obrigatório, CSAT Transacional = pseudonimizado permitido com consentimento)
- **RN-RF071-006**: Validação de Taxa de Resposta Mínima (30% taxa E ≥50 respostas para significância estatística)
- **RN-RF071-007**: Expiração de Link de Pesquisa (padrão 7 dias, configurável por template)
- **RN-RF071-010**: Limite de Caracteres em Respostas Abertas (min 10, max 2000 caracteres)

---

## UC02: Enviar Pesquisa Automaticamente via Trigger Pós-Chamado

### 1. Descrição

Este caso de uso executa envio automático de pesquisa CSAT/CES via trigger pós-resolução de chamado, validando throttling anti-fadiga (RN-RF071-001: 1 pesquisa a cada 7 dias por usuário), selecionando canal prioritário (e-mail 60% taxa resposta, SMS 45%, in-app 72%, WhatsApp 58%), gerando link único tokenizado com validade configurável (padrão 7 dias), registrando evento de envio em auditoria, e enviando via provedores multi-canal (SendGrid e-mail, Twilio SMS, WhatsApp Business API, notificação in-app SignalR) com retry exponencial em caso de falha (backoff 1min → 5min → 15min, max 3 tentativas).

### 2. Atores

- Sistema (Backend .NET 10, Hangfire, SendGrid, Twilio, WhatsApp Business API, SignalR)
- Usuário final (recebe e responde pesquisa)

### 3. Pré-condições

- Template de pesquisa ativo com trigger pós-chamado configurado
- Chamado resolvido recentemente (trigger disparado)
- Feature flag `SERVICE_DESK_PESQUISA_SATISFACAO` habilitada
- Provedores externos configurados (SendGrid API key, Twilio credentials, WhatsApp Business API)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | **Hangfire Job Trigger**: Job `EnviarPesquisaPosChamadoJob` detecta chamado #12345 resolvido às 14:30 |
| 2 | - | Job aguarda delay configurado no template (30 minutos) → Executa às 15:00 |
| 3 | - | Job carrega template ativo: `var template = await _context.TemplatesPesquisas.Include(t => t.Perguntas).Include(t => t.TriggerConfig).FirstAsync(t => t.Tipo == "CSAT_TRANSACIONAL" && t.Status == "Ativo");` |
| 4 | - | Job carrega dados do chamado: `var chamado = await _context.Chamados.Include(c => c.Usuario).FirstAsync(c => c.Id == 12345);` |
| 5 | - | **Backend - RN-RF071-001 Throttling**: Job valida se usuário recebeu pesquisa nos últimos 7 dias: `var dataLimite = DateTime.UtcNow.AddDays(-7); var pesquisaRecente = await _context.RespostasPesquisas.AnyAsync(r => r.UsuarioId == usuario.Id && r.DataEnvio >= dataLimite);` |
| 6 | - | Se pesquisaRecente = true: Job registra log INFO "Usuário {userId} já recebeu pesquisa nos últimos 7 dias. Envio bloqueado por throttling." e finaliza execução (não envia pesquisa) |
| 7 | - | Se pesquisaRecente = false: Job continua processo de envio |
| 8 | - | Job cria registro de resposta pendente: `var resposta = new RespostaPesquisa { Id = Guid.NewGuid(), TemplateId = template.Id, UsuarioId = usuario.Id, ChamadoOrigemId = chamado.Id, TokenUnico = CryptographicHelper.GerarTokenSeguro(32), DataEnvio = DateTime.UtcNow, DataExpiracao = DateTime.UtcNow.AddDays(template.DiasValidade), Status = StatusPesquisa.Pendente, NivelAnonimizacao = template.Anonimizacao, ClienteId = chamado.ClienteId };` |
| 9 | - | Job salva registro: `_context.RespostasPesquisas.Add(resposta); await _context.SaveChangesAsync();` |
| 10 | - | Job gera URL pública da pesquisa: `var urlPesquisa = $"https://pesquisas.icontrolit.com/responder/{resposta.Id}?token={resposta.TokenUnico}";` |
| 11 | - | **Backend - Seleção de Canal Prioritário**: Job verifica canais habilitados no template e preferências do usuário: `var canaisPrioritarios = template.CanaisEnvio.OrderBy(c => c.Ordem);` (ordem: in-app 1°, WhatsApp 2°, e-mail 3°, SMS 4°) |
| 12 | - | Job tenta enviar via 1° canal (In-App): `var sucessoInApp = await _notificacaoService.EnviarNotificacaoInAppAsync(usuario.Id, titulo: "Avalie seu atendimento", mensagem: "Seu chamado foi resolvido. Nos conte como foi sua experiência!", link: urlPesquisa);` |
| 13 | - | Se sucessoInApp = true: Job atualiza `resposta.CanalEnvio = "InApp"; resposta.DataEnvioEfetivo = DateTime.UtcNow;` e finaliza (enviado com sucesso via 1° canal) |
| 14 | - | Se sucessoInApp = false (usuário sem app instalado): Job tenta 2° canal (E-mail) |
| 15 | - | **Backend - Envio E-mail via SendGrid**: Job monta payload e-mail: `var emailPayload = new { to = usuario.Email, from = "noreply@icontrolit.com", templateId = "d-abc123xyz", dynamicTemplateData = new { nomeUsuario = usuario.Nome, numeroChamado = chamado.Numero, analistaResponsavel = chamado.AnalistaResponsavel.Nome, urlPesquisa, dataExpiracao = resposta.DataExpiracao.ToString("dd/MM/yyyy") } };` |
| 16 | - | Job invoca SendGrid API: `var response = await _sendGridClient.SendEmailAsync(emailPayload);` |
| 17 | - | Se response.StatusCode = 202 (aceito): Job atualiza `resposta.CanalEnvio = "Email"; resposta.DataEnvioEfetivo = DateTime.UtcNow; resposta.ProvedorExterno = "SendGrid"; resposta.ProvedorMessageId = response.Headers["X-Message-Id"];` |
| 18 | - | **Backend - Event**: Job publica evento `PesquisaEnviadaEvent { RespostaId = resposta.Id, CanalEnvio = "Email", UsuarioId = usuario.Id, ChamadoId = chamado.Id }` |
| 19 | - | Handler de auditoria registra: `INSERT INTO AuditoriaPesquisas (RespostaId, Evento, Data, CanalEnvio, ProvedorExterno, UsuarioId, ClienteId)` |
| 20 | - | Job finaliza execução com sucesso, retorna log INFO: "Pesquisa enviada para {usuario.Email} via Email (SendGrid). RespostaId: {resposta.Id}" |
| 21 | 2 horas depois, usuário abre e-mail e clica no link da pesquisa | - |
| 22 | - | Browser navega para `https://pesquisas.icontrolit.com/responder/{respostaId}?token={token}` |
| 23 | - | Frontend SPA de pesquisas envia `GET /api/pesquisas/responder/{respostaId}?token={token}` |
| 24 | - | **Backend - RN-RF071-007 Validação Expiração**: Backend valida: `var resposta = await _context.RespostasPesquisas.FirstAsync(r => r.Id == respostaId && r.TokenUnico == token);` |
| 25 | - | Backend verifica: `if (DateTime.UtcNow > resposta.DataExpiracao)` → false (dentro da validade de 7 dias) |
| 26 | - | Backend verifica: `if (resposta.DataResposta.HasValue)` → false (ainda não foi respondida) |
| 27 | - | Backend carrega template com perguntas: `var template = await _context.TemplatesPesquisas.Include(t => t.Perguntas).FirstAsync(t => t.Id == resposta.TemplateId);` |
| 28 | - | Backend retorna HTTP 200 OK com JSON: `{ templateNome, perguntas: [{ id, tipo: "CSAT_ESTRELAS", pergunta: "Como você avalia o atendimento?", obrigatorio: true, opcoes: [1,2,3,4,5] }, { id, tipo: "TEXTO_LIVRE", pergunta: "Comentários", obrigatorio: false, minCaracteres: 10, maxCaracteres: 2000 }], chamadoContexto: { numero: "12345", categoria: "Suporte Técnico", analistaResponsavel: "João Silva" } }` |
| 29 | - | Frontend renderiza formulário de pesquisa com perguntas em sequência, contexto do chamado no topo (número, categoria, analista) |
| 30 | Usuário responde pergunta 1 (CSAT): seleciona 4 estrelas | - |
| 31 | Usuário responde pergunta 2 (Texto Livre): digita "Atendimento rápido e eficiente. Problema resolvido no primeiro contato." (80 caracteres) | - |
| 32 | Usuário clica em botão "Enviar Avaliação" | - |
| 33 | - | Frontend envia `POST /api/pesquisas/responder/{respostaId}` com body: `{ token, respostas: [{ perguntaId: 1, tipo: "CSAT_ESTRELAS", valor: 4 }, { perguntaId: 2, tipo: "TEXTO_LIVRE", valor: "Atendimento rápido..." }] }` |
| 34 | - | Backend valida token novamente (segurança double-check) |
| 35 | - | **Backend - RN-RF071-010**: Backend valida texto livre: `RespostaAbertaValidator` verifica 10 ≤ length ≤ 2000 → OK (80 caracteres) |
| 36 | - | Backend salva respostas: `resposta.DataResposta = DateTime.UtcNow; resposta.Status = StatusPesquisa.Respondida; resposta.RespostasJson = JsonSerializer.Serialize(request.Respostas); resposta.CSAT = 4; resposta.TempoResposta = (DateTime.UtcNow - resposta.DataEnvio).TotalMinutes;` |
| 37 | - | **Backend - RN-RF071-005 Análise Sentimento**: Backend invoca Azure Cognitive Services para processar texto livre: `var sentimento = await _nlpClient.AnalyzeSentimentAsync("Atendimento rápido...", language: "pt");` |
| 38 | - | Azure retorna: `{ sentiment: "Positive", confidenceScores: { positive: 0.92, neutral: 0.06, negative: 0.02 } }` |
| 39 | - | Backend salva análise: `resposta.SentimentoScore = 0.90m; resposta.SentimentoClassificacao = "Positivo"; resposta.Keywords = ["atendimento", "rápido", "eficiente", "resolvido"];` |
| 40 | - | **Backend - Event**: Publica evento `PesquisaRespondidaEvent { RespostaId, UsuarioId, ChamadoId, CSAT = 4, Sentimento = "Positivo" }` |
| 41 | - | Handler de métricas atualiza agregados em tempo real: `UPDATE MetricasPesquisa SET TotalRespostas++, SomaCSAT += 4, RespostasPositivas++ WHERE TemplateId = ...` |
| 42 | - | Backend retorna HTTP 200 OK |
| 43 | - | Frontend exibe tela de agradecimento: "✅ Obrigado pelo seu feedback! Sua opinião nos ajuda a melhorar nosso serviço." |

### 5. Fluxos Alternativos

**FA01: Throttling Bloqueia Envio (Usuário Recebeu Pesquisa Recentemente)**

- No passo 5, job detecta que usuário recebeu pesquisa NPS em 25/12/2025 (3 dias atrás)
- No passo 6, `pesquisaRecente = true` → Job não envia pesquisa CSAT pós-chamado
- Job registra log INFO: "Usuário joao.silva@empresa.com já recebeu pesquisa NPS em 25/12/2025. Cooldown ativo até 01/01/2026. Envio bloqueado."
- Job atualiza chamado com flag: `chamado.PesquisaSatisfacaoBloqueadaThrottling = true; chamado.MotivoBloqueioPesquisa = "Usuário já recebeu pesquisa nos últimos 7 dias (cooldown ativo)";`
- Backend dispara notificação interna para gestor (opcional): "Pesquisa de chamado #12345 não enviada devido a throttling. Usuário será incluído em próximo lote."

**FA02: Falha no Envio de E-mail - Retry Exponencial**

- No passo 16, SendGrid API retorna HTTP 500 Internal Server Error (falha temporária)
- Backend captura exceção, registra log WARNING: "Falha ao enviar e-mail via SendGrid. Tentativa 1/3. Erro: Internal Server Error"
- Backend executa retry com backoff exponencial: aguarda 1 minuto
- Backend reexecuta `_sendGridClient.SendEmailAsync()` (tentativa 2)
- Se falhar novamente: aguarda 5 minutos, tenta pela 3ª vez
- Se 3ª tentativa falhar: Backend tenta próximo canal (SMS via Twilio)
- Se SMS também falhar: Backend atualiza `resposta.Status = StatusPesquisa.FalhaEnvio; resposta.MotivoFalha = "Falha em todos os canais após 3 tentativas. Última falha: Twilio HTTP 429 Rate Limit";`
- Backend cria alerta para DevOps: "Falha crítica no envio de pesquisas. Verificar provedores externos."

**FA03: Link Expirado - Usuário Tenta Responder Após 7 Dias**

- No passo 25, backend detecta: `DateTime.UtcNow > resposta.DataExpiracao` → true (link enviado em 20/12, usuário tentou abrir em 30/12, expirado)
- Backend retorna HTTP 410 Gone com body: `{ "error": "PESQUISA_EXPIRADA", "message": "Este link expirou em 27/12/2025. Validade: 7 dias. Entre em contato conosco se precisar avaliar o atendimento.", "dataExpiracao": "2025-12-27T15:00:00Z" }`
- Frontend renderiza página de erro amigável: "⏰ Link Expirado - Esta pesquisa expirou em 27/12/2025. Se ainda desejar avaliar nosso atendimento, entre em contato com suporte@empresa.com"

**FA04: Pesquisa Já Respondida - Tentativa de Responder Novamente**

- No passo 26, backend detecta: `resposta.DataResposta.HasValue` → true (usuário já respondeu em 22/12)
- Backend retorna HTTP 409 Conflict com body: `{ "error": "PESQUISA_JA_RESPONDIDA", "message": "Você já respondeu esta pesquisa em 22/12/2025 às 16:45. Obrigado pelo seu feedback!", "dataResposta": "2025-12-22T16:45:00Z" }`
- Frontend renderiza página: "✅ Pesquisa Já Respondida - Você avaliou este atendimento em 22/12/2025. Obrigado pela sua participação!"

**FA05: Envio Multi-Canal Simultâneo (E-mail + SMS)**

- No passo 11-14, template configurado com canais: E-mail + SMS simultâneos (ao invés de prioridade)
- Job dispara ambos em paralelo usando `Task.WhenAll()`:
  - Task 1: Envia e-mail via SendGrid
  - Task 2: Envia SMS via Twilio com mensagem curta: "Avalie seu atendimento (chamado #12345): {url_curta} - Válido até 27/12"
- Backend usa serviço de URL shortener (Bitly) para encurtar link: `https://bit.ly/sat-12abc` (cabe em 160 chars do SMS)
- Backend atualiza: `resposta.CanalEnvio = "Email,SMS"; resposta.ProvedorExterno = "SendGrid,Twilio";`
- Usuário pode responder clicando em qualquer um dos dois links (ambos apontam para mesma RespostaId)

### 6. Exceções

**EX01: Template de Pesquisa Inativo ou Excluído**

- No passo 3, job tenta carregar template mas não encontra nenhum ativo com tipo CSAT_TRANSACIONAL
- Backend lança `NotFoundException: "Nenhum template de pesquisa CSAT ativo encontrado"`
- Job registra log ERROR: "Impossível enviar pesquisa para chamado #12345. Template CSAT_TRANSACIONAL não encontrado ou está inativo."
- Job finaliza execução sem enviar pesquisa
- Backend dispara alerta para gestor: "Sistema de pesquisas sem template CSAT ativo. Ative template antes que chamados sejam resolvidos."

**EX02: Usuário Sem E-mail ou Telefone Cadastrado**

- No passo 15, job tenta enviar e-mail mas `usuario.Email == null` (usuário sem e-mail cadastrado)
- No passo 16, SendGrid rejeitaria payload, então backend valida antes: `if (string.IsNullOrEmpty(usuario.Email))` → true
- Backend tenta próximo canal (SMS) mas `usuario.Telefone == null` também
- Backend atualiza: `resposta.Status = StatusPesquisa.FalhaEnvio; resposta.MotivoFalha = "Usuário sem e-mail ou telefone cadastrado. Canais de envio indisponíveis.";`
- Backend registra log WARNING: "Pesquisa de chamado #12345 não enviada. Usuário {userId} sem contatos cadastrados."

**EX03: Azure Cognitive Services Offline - Análise de Sentimento Falha**

- No passo 37, backend tenta invocar Azure NLP mas serviço retorna HTTP 503 Service Unavailable
- Backend captura exceção `HttpRequestException`, registra log WARNING: "Azure Cognitive Services indisponível. Análise de sentimento não processada."
- Backend salva resposta SEM análise de sentimento: `resposta.SentimentoScore = null; resposta.SentimentoClassificacao = null; resposta.Keywords = null;`
- Resposta é salva normalmente (análise de sentimento é complementar, não bloqueia salvamento)
- Backend enfileira job Hangfire: `BackgroundJob.Schedule(() => ReprocessarSentimentoAsync(respostaId), TimeSpan.FromHours(1));` (reprocessar quando serviço voltar)

**EX04: Token Inválido ou Manipulado (Tentativa de Fraude)**

- No passo 24, frontend envia token manipulado: `?token=abc123INVALIDO`
- Backend executa query: `_context.RespostasPesquisas.FirstAsync(r => r.Id == respostaId && r.TokenUnico == token)` → Nenhum registro encontrado
- Backend lança `NotFoundException`
- Backend retorna HTTP 404 com body: `{ "error": "PESQUISA_NAO_ENCONTRADA", "message": "Link inválido ou pesquisa não existe. Verifique se copiou o link completo do e-mail." }`
- Backend registra evento de segurança: `SecurityEventType.TokenManipulationAttempt, IpOrigem, UserAgent`
- Frontend renderiza página de erro: "🔒 Link Inválido - Esta pesquisa não existe ou o link está incorreto."

### 7. Pós-condições

- Pesquisa enviada via canal selecionado (e-mail, SMS, in-app, WhatsApp)
- Registro de RespostaPesquisa criado com status Pendente
- Evento de envio registrado em auditoria
- Throttling aplicado (cooldown 7 dias iniciado)
- Link único tokenizado gerado com validade configurável
- Resposta salva com CSAT/CES, análise de sentimento NLP, keywords
- Métricas agregadas atualizadas em tempo real
- Correlação com chamado origem preservada

### 8. Regras de Negócio Aplicáveis

- **RN-RF071-001**: Frequência Máxima de Pesquisas (1 a cada 7 dias por usuário, anti-fadiga)
- **RN-RF071-005**: Análise de Sentimento Automática em Respostas Abertas (Azure Cognitive Services, score -1.0 a +1.0, keywords)
- **RN-RF071-007**: Expiração de Link de Pesquisa (padrão 7 dias, configurável)
- **RN-RF071-009**: Correlação Automática com Chamado de Origem (ChamadoOrigemId preservado para rastreabilidade)
- **RN-RF071-010**: Limite de Caracteres em Respostas Abertas (min 10, max 2000)

---

## UC03: Processar Resposta com Análise NLP e Follow-up Detratores

### 1. Descrição

Este caso de uso processa resposta de pesquisa recebida executando análise de sentimento NLP em respostas abertas (Azure Cognitive Services com score -1.0 a +1.0, classificação Positivo/Neutro/Negativo, extração de top 5 keywords), calcula métricas agregadas (NPS segundo fórmula Bain & Company: % Promotores 9-10 - % Detratores 0-6, CSAT = % respostas 4-5 / total, CES = média aritmética escala 1-7), identifica detratores NPS 0-6 e dispara follow-up automático em <2h (abertura de chamado interno categoria "Recuperação Cliente", notificação gestor Service Desk, e-mail personalizado ao usuário), correlaciona resposta com chamado origem para análise de causa-raiz (tempo resolução, reaberturas, analista responsável) e atualiza ranking de analistas por CSAT individual.

### 2. Atores

- Sistema (Backend .NET 10, Azure Cognitive Services, Hangfire)
- Gestor de Service Desk (recebe alertas de detratores)

### 3. Pré-condições

- Resposta de pesquisa recebida via UC02
- Azure Cognitive Services configurado e disponível
- Feature flag `SERVICE_DESK_PESQUISA_SATISFACAO` habilitada
- Evento `PesquisaRespondidaEvent` publicado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | **Handler Event**: `ProcessarRespostaPesquisaHandler` recebe evento `PesquisaRespondidaEvent { RespostaId, CSAT = 4, UsuarioId, ChamadoId }` |
| 2 | - | Handler carrega resposta completa: `var resposta = await _context.RespostasPesquisas.Include(r => r.Template).Include(r => r.ChamadoOrigem).ThenInclude(c => c.AnalistaResponsavel).FirstAsync(r => r.Id == event.RespostaId);` |
| 3 | - | Handler extrai texto livre das respostas: `var respostasObj = JsonSerializer.Deserialize<List<RespostaItem>>(resposta.RespostasJson); var textoLivre = respostasObj.FirstOrDefault(r => r.Tipo == "TEXTO_LIVRE")?.Valor;` |
| 4 | - | Se textoLivre não vazio: Handler invoca análise de sentimento (já executada no UC02, mas reprocessa para garantir consistência) |
| 5 | - | **RN-RF071-005 Análise Sentimento**: Handler invoca `AnalisadorSentimento.AnalisarAsync(textoLivre)` |
| 6 | - | AnalisadorSentimento chama Azure Cognitive Services: `var response = await _nlpClient.AnalyzeSentimentAsync(textoLivre, language: "pt");` |
| 7 | - | Azure retorna: `{ sentiment: "Positive", confidenceScores: { positive: 0.92, neutral: 0.06, negative: 0.02 }, keyPhrases: ["atendimento rápido", "problema resolvido", "eficiente"] }` |
| 8 | - | Handler salva resultado: `resposta.SentimentoScore = 0.90m; resposta.SentimentoClassificacao = "Positivo"; resposta.Keywords = ["atendimento rápido", "problema resolvido", "eficiente"];` |
| 9 | - | Se SentimentoScore < -0.7 (muito negativo): Handler dispara alerta: `await _alertaService.EnviarAsync(new Alerta { Tipo = "SENTIMENTO_CRITICO", Descricao = $"Resposta com sentimento muito negativo: {textoLivre.Substring(0, 100)}...", Score = resposta.SentimentoScore });` |
| 10 | - | **RN-RF071-009 Correlação Chamado**: Handler analisa correlação com chamado origem: `var analise = await _correladorService.AnalisarAsync(resposta.Id);` |
| 11 | - | CorreladorChamadoPesquisa calcula: `var tempoResolucao = chamado.DataResolucao - chamado.DataAbertura; var tempoResposta = chamado.DataPrimeiraResposta - chamado.DataAbertura; var qtdReaberturas = chamado.QuantidadeReaberturas;` |
| 12 | - | Correlador identifica padrões: Se CSAT ≤3 E tempoResposta >4h: `analise.CausaRaizProvavel = "Tempo de resposta acima de 4h correlacionado com baixo CSAT";` |
| 13 | - | Handler salva análise de correlação: `resposta.CorrelacaoJson = JsonSerializer.Serialize(analise); resposta.CausaRaizProvavel = analise.CausaRaizProvavel;` |
| 14 | - | **Atualização Ranking Analista**: Handler atualiza métricas do analista responsável: `UPDATE RankingAnalista SET TotalAvaliacoes++, SomaCSAT += resposta.CSAT, CSATMedio = SomaCSAT / TotalAvaliacoes WHERE AnalistaId = chamado.AnalistaResponsavelId AND ClienteId = resposta.ClienteId;` |
| 15 | - | Handler verifica tipo de pergunta principal: Template é NPS? → Não (é CSAT) |
| 16 | - | Handler calcula métrica CSAT agregada do template: `var respostasTemplate = await _context.RespostasPesquisas.Where(r => r.TemplateId == resposta.TemplateId && r.Status == StatusPesquisa.Respondida).ToListAsync();` |
| 17 | - | **RN-RF071-002 Cálculo CSAT**: Handler calcula: `var respostas4a5 = respostasTemplate.Count(r => r.CSAT >= 4); var csatPercentual = (respostas4a5 / (decimal)respostasTemplate.Count) * 100;` → Resultado: 82.3% |
| 18 | - | Handler atualiza métrica agregada: `UPDATE MetricasTemplate SET CSATAtual = 82.3m, TotalRespostas = respostasTemplate.Count, DataUltimaAtualizacao = DateTime.UtcNow WHERE TemplateId = resposta.TemplateId;` |
| 19 | - | Handler verifica se template tem significância estatística: `var ehValido = ValidadorSignificanciaEstatistica.PesquisaEhValida(enviados: 500, respondidos: respostasTemplate.Count);` |
| 20 | - | Se ehValido = true: Handler atualiza flag: `UPDATE MetricasTemplate SET SignificanciaEstatistica = true WHERE TemplateId = ...;` |
| 21 | - | **Backend - Event**: Handler publica evento `MetricasPesquisaAtualizadasEvent { TemplateId, CSAT = 82.3m, TotalRespostas }` |
| 22 | - | **Handler SignalR**: `AtualizarDashboardHandler` recebe evento e envia atualização tempo real: `await _hubContext.Clients.Group($"gestao_{clienteId}").SendAsync("MetricasAtualizadas", new { csat = 82.3m, totalRespostas });` |
| 23 | - | Frontend dashboard (se aberto) atualiza KPI em tempo real sem reload: "CSAT: 82.3%" (barra de progresso atualiza suavemente de 82.1% para 82.3%) |
| 24 | - | Handler salva timestamp de processamento: `await _context.SaveChangesAsync();` |
| 25 | - | Handler finaliza execução com sucesso |

### 5. Fluxos Alternativos

**FA01: Detrator NPS Identificado - Follow-up Automático <2h**

- No passo 15, handler detecta que template é tipo NPS e resposta.Nota = 4 (0-10 scale)
- Handler verifica: `if (resposta.Nota <= 6)` → true (detrator identificado)
- **RN-RF071-003 Follow-up Detratores**: Handler dispara 3 ações em paralelo usando `Task.WhenAll()`:
  - **Ação 1 - Abrir Chamado Interno**: `var chamadoId = await _chamadoService.CriarChamadoInternoAsync(new CriarChamadoCommand { Titulo = $"[DETRATOR NPS] Follow-up Usuario {usuario.Nome}", Descricao = $"Nota recebida: 4/10\nComentario: {textoLivre}", Categoria = "Recuperacao Cliente", Prioridade = "Alta", AtribuidoA = gestorServiceDeskId, Tags = ["NPS", "Detrator", "Retencao"] });`
  - **Ação 2 - Notificar Gestor**: `await _notificacaoService.EnviarAsync(new Notificacao { DestinatarioId = gestorId, Tipo = "ALERTA_CRITICO", Titulo = "Detrator NPS Identificado", Mensagem = $"Usuario {usuario.Nome} avaliou serviço com nota 4. Chamado #{chamadoId} aberto.", Canal = ["Email", "InApp", "SMS"], PrazoResposta = TimeSpan.FromHours(2) });`
  - **Ação 3 - E-mail Personalizado**: `await _emailService.EnviarTemplateAsync("RECUPERACAO_DETRATOR", new { Nome = usuario.Nome, Nota = 4, GestorNome, GestorEmail, GestorTelefone, ChamadoUrl = $"/chamados/{chamadoId}" });`
- Handler registra timestamp de follow-up: `resposta.FollowUpDetrator = true; resposta.DataFollowUp = DateTime.UtcNow; resposta.ChamadoFollowUpId = chamadoId;`
- Handler atualiza métrica: `UPDATE MetricasTemplate SET DetratoresIdentificados++, FollowUpsRealizados++ WHERE TemplateId = ...;`

**FA02: Sentimento Muito Negativo - Alerta Imediato**

- No passo 9, handler detecta SentimentoScore = -0.85 (muito negativo)
- Handler cria alerta crítico: `await _alertaService.EnviarAsync(new Alerta { Tipo = "SENTIMENTO_CRITICO", Titulo = "Feedback Muito Negativo Detectado", Descricao = $"Resposta de {usuario.Nome} para chamado #{chamado.Numero}: '{textoLivre}' - Score: -0.85", Prioridade = "Urgente", DestinatarioIds = [gestorId, analistaId] });`
- Handler envia notificação imediata via SMS + e-mail para gestor
- Handler cria flag no chamado origem: `chamado.FeedbackMuitoNegativo = true; chamado.ScoreSentimento = -0.85m;`
- Frontend exibe badge vermelho no chamado: "⚠️ Feedback Muito Negativo Recebido (Score: -0.85)"

**FA03: Cálculo de NPS Agregado e Classificação**

- No passo 15, handler detecta template tipo NPS
- Handler carrega todas as respostas NPS do período (ex: trimestral): `var respostasNPS = await _context.RespostasPesquisas.Where(r => r.TemplateId == templateId && r.DataResposta >= inicioTrimestre && r.DataResposta <= fimTrimestre).ToListAsync();`
- **RN-RF071-002 Cálculo NPS**: Handler executa `CalculadoraNPS.CalcularNPS(respostasNPS.Select(r => r.Nota).ToList());`
- CalculadoraNPS conta: `promotores = respostasNPS.Count(r => r.Nota >= 9); // 60 de 100`, `detratores = respostasNPS.Count(r => r.Nota <= 6); // 20 de 100`, `neutros = respostasNPS.Count(r => r.Nota >= 7 && r.Nota <= 8); // 20 de 100`
- CalculadoraNPS calcula: `nps = (promotores / total * 100) - (detratores / total * 100) = (60/100*100) - (20/100*100) = 60 - 20 = 40`
- CalculadoraNPS classifica: `ClassificarNPS(40)` → "Bom (Benchmark TI)" (faixa 30-50)
- Handler atualiza: `UPDATE MetricasTemplate SET NPS = 40, NPSClassificacao = "Bom (Benchmark TI)", Promotores = 60, Neutros = 20, Detratores = 20 WHERE TemplateId = ...;`

**FA04: Identificação de Padrão de Insatisfação por Categoria**

- No passo 12, correlador detecta que 15 das últimas 20 respostas CSAT ≤3 são da categoria "Redes"
- Correlador calcula: `var insatisfacaoRedes = respostasCSAT.Where(r => r.ChamadoOrigem.Categoria == "Redes" && r.CSAT <= 3).Count() / (decimal)respostasCSAT.Where(r => r.ChamadoOrigem.Categoria == "Redes").Count() = 15/20 = 75%`
- Correlador identifica padrão: `if (insatisfacaoRedes > 0.6)` → Alerta para gestor
- Handler cria recomendação: `await _recomendacaoService.CriarAsync(new Recomendacao { Tipo = "PADRAO_INSATISFACAO", Categoria = "Redes", Descricao = "75% de insatisfação detectada em chamados de Redes. Investigar processo/equipe.", Prioridade = "Alta" });`
- Dashboard de gestão exibe card de recomendação: "⚠️ Atenção: Alta taxa de insatisfação em Redes (75%)" com botão "Investigar"

**FA05: Atualização de CES e Alerta para Processo com Alto Esforço**

- No passo 16-18, handler processa respostas de template CES (escala 1-7)
- **RN-RF071-008 Cálculo CES**: Handler calcula: `var ces = respostasCES.Average(r => r.CES); // média = 6.2`
- Handler classifica: `CalculadoraCES.ClassificarCES(6.2m)` → "Crítico (Altíssimo Esforço - Churn Iminente)"
- Handler dispara alerta: `await AlertarCESCritico(ces: 6.2m, processo: "Migração de Sistema", cancellationToken);`
- AlertaService envia: `{ Tipo = "CES_CRITICO", Titulo = "Processo 'Migração de Sistema' com CES crítico 6.2", Descricao = "96% probabilidade de churn. Ação imediata necessária.", Prioridade = "Urgente" }`
- Handler cria task action: `INSERT INTO AcoesPendentes (Tipo, Descricao, ResponsavelId, PrazoHoras) VALUES ('REDUCAO_CES', 'Simplificar processo Migração de Sistema - CES 6.2', gestorId, 48);`

### 6. Exceções

**EX01: Azure Cognitive Services Timeout - Análise de Sentimento Não Processada**

- No passo 6, chamada `_nlpClient.AnalyzeSentimentAsync()` timeout após 10 segundos
- Handler captura `TaskCanceledException`, registra log WARNING: "Azure Cognitive Services timeout ao analisar sentimento. RespostaId: {respostaId}"
- Handler salva resposta SEM análise: `resposta.SentimentoScore = null; resposta.SentimentoClassificacao = null; resposta.Keywords = null; resposta.SentimentoProcessado = false;`
- Handler enfileira reprocessamento: `BackgroundJob.Schedule(() => ReprocessarSentimentoAsync(respostaId), TimeSpan.FromHours(1));`
- Processamento continua normalmente (sentimento é complementar, não bloqueia fluxo)

**EX02: Chamado Origem Não Encontrado (Correlação Falha)**

- No passo 2, handler tenta carregar resposta com Include de ChamadoOrigem mas `resposta.ChamadoOrigemId == null` (pesquisa relacional NPS não tem chamado origem)
- No passo 10, correlador detecta: `if (resposta.ChamadoOrigem == null)` → true
- Correlador retorna análise vazia: `new AnaliseCorrelacao { PossuiCorrelacao = false, Motivo = "Pesquisa relacional (NPS trimestral) sem chamado origem" }`
- Handler pula passos 11-14 (análise de correlação e ranking analista)
- Processamento continua com cálculo de métricas agregadas NPS (passos 15-18)

**EX03: Resposta Duplicada (Mesmo Usuário Respondeu Duas Vezes Manipulando Link)**

- No passo 1, handler recebe evento `PesquisaRespondidaEvent` com RespostaId que já foi processada
- Handler verifica: `if (resposta.Processado == true)` → true
- Handler registra log WARNING: "Tentativa de processar resposta já processada. RespostaId: {respostaId}. Possível duplicação de evento."
- Handler finaliza execução sem reprocessar (idempotência garantida)

**EX04: Gestor de Service Desk Não Configurado - Follow-up Detrator Falha**

- No passo FA01, handler tenta disparar follow-up mas `gestorServiceDeskId == null` (cliente sem gestor configurado)
- Handler captura exceção ao criar chamado interno: `ArgumentNullException: AtribuidoA cannot be null`
- Handler registra log ERROR: "Impossível criar chamado de follow-up detrator. Cliente {clienteId} sem Gestor de Service Desk configurado."
- Handler salva flag: `resposta.FollowUpDetrator = false; resposta.MotivoFalhaFollowUp = "Gestor de Service Desk não configurado no cliente";`
- Handler envia notificação para administrador do sistema: "Cliente {clienteNome} sem gestor configurado. Follow-up de detratores desabilitado."

### 7. Pós-condições

- Análise de sentimento NLP executada e salva (score, classificação, keywords)
- Métricas agregadas atualizadas (NPS/CSAT/CES calculados)
- Correlação com chamado origem analisada (tempo resolução, reaberturas, analista)
- Ranking de analistas atualizado com nova avaliação
- Detratores identificados com follow-up automático disparado (<2h)
- Alertas enviados para sentimento muito negativo ou CES crítico
- Dashboard tempo real atualizado via SignalR
- Evento de processamento registrado em auditoria

### 8. Regras de Negócio Aplicáveis

- **RN-RF071-002**: Cálculo Automático de NPS (% Promotores 9-10 - % Detratores 0-6, fórmula Bain & Company)
- **RN-RF071-003**: Follow-up Automático para Detratores (NPS 0-6 dispara chamado interno + notificação gestor + e-mail em <2h)
- **RN-RF071-005**: Análise de Sentimento Automática (Azure Cognitive Services, score -1.0 a +1.0, alertas se < -0.7)
- **RN-RF071-008**: Cálculo de CES (média aritmética escala 1-7, alerta se ≥5.0 = 96% probabilidade churn)
- **RN-RF071-009**: Correlação Automática com Chamado de Origem (análise de causa-raiz, ranking analista)

---

## UC04: Visualizar Dashboard Tempo Real com Métricas NPS/CSAT/CES

### 1. Descrição

Este caso de uso permite que Gestores de Service Desk visualizem dashboard interativo com métricas de satisfação atualizadas em tempo real via SignalR (atualização a cada 5min), exibindo 18 widgets configuráveis (NPS Gauge com classificação, CSAT Trend Line últimos 30 dias, CES Heatmap por processo, Word Cloud de comentários frequentes, Ranking Top 10 Analistas por CSAT médio, Alertas Ativos com prioridade), aplicando filtros facetados (período, categoria chamado, analista, departamento, canal envio), exportando dados (Excel/PDF/PowerBI Dataset/REST API) e configurando alertas customizados com 8 condições críticas (queda NPS >5 pontos em 7 dias, CSAT <70%, spike detratores, comentários com palavras-gatilho).

### 2. Atores

- Gestor de Service Desk
- Diretoria (KPIs estratégicos)
- Sistema (Backend .NET 10, SignalR, Redis Cache, Chart.js)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:pesquisa-satisfacao:dashboard`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `SERVICE_DESK_PESQUISA_SATISFACAO` habilitada
- SignalR Hub configurado e online

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa rota `/service-desk/pesquisas/dashboard` | - |
| 2 | - | Frontend valida permissão local: `hasPermission('service-desk:pesquisa-satisfacao:dashboard')` → Se negado: redireciona |
| 3 | - | Frontend estabelece conexão SignalR: `_hubConnection = new HubConnectionBuilder().withUrl("/hubs/pesquisas-satisfacao").build(); await _hubConnection.start();` |
| 4 | - | Frontend se junta ao grupo do cliente: `await _hubConnection.invoke("JoinGroup", clienteId);` |
| 5 | - | Frontend envia `GET /api/pesquisas/dashboard/metricas?periodo=ultimos30dias&clienteId={clienteId}` |
| 6 | - | Backend valida permissão RBAC: `User.HasPermission("service-desk:pesquisa-satisfacao:dashboard")` → Se negado: HTTP 403 |
| 7 | - | **Backend - Cache Redis**: Backend verifica cache: `var cacheKey = $"dashboard_metricas_{clienteId}_ultimos30dias"; var cached = await _cache.GetStringAsync(cacheKey);` |
| 8 | - | Se cache hit (TTL 5min): Backend desserializa JSON e retorna diretamente (latência <50ms) |
| 9 | - | Se cache miss: Backend executa queries agregadas em paralelo (Task.WhenAll): |
| 10 | - | **Query 1 - NPS Atual**: `SELECT AVG(CASE WHEN Nota >= 9 THEN 1 ELSE 0 END) * 100 - AVG(CASE WHEN Nota <= 6 THEN 1 ELSE 0 END) * 100 AS NPS FROM RespostasPesquisas WHERE TemplateId IN (NPS templates) AND DataResposta >= @dataInicio AND ClienteId = @clienteId` → Resultado: NPS = 42 |
| 11 | - | **Query 2 - CSAT Atual**: `SELECT (COUNT(CASE WHEN CSAT >= 4 THEN 1 END) * 100.0 / COUNT(*)) AS CSATPercentual FROM RespostasPesquisas WHERE TemplateId IN (CSAT templates) AND DataResposta >= @dataInicio AND ClienteId = @clienteId` → Resultado: CSAT = 83.5% |
| 12 | - | **Query 3 - CES Médio**: `SELECT AVG(CES) AS CESMedio FROM RespostasPesquisas WHERE TemplateId IN (CES templates) AND DataResposta >= @dataInicio AND ClienteId = @clienteId` → Resultado: CES = 2.8 |
| 13 | - | **Query 4 - Total Respostas**: `SELECT COUNT(*) FROM RespostasPesquisas WHERE DataResposta >= @dataInicio AND ClienteId = @clienteId` → Resultado: 1.250 respostas |
| 14 | - | **Query 5 - Taxa Resposta Média**: `SELECT (SUM(TotalRespondidos) * 100.0 / SUM(TotalEnviados)) AS TaxaResposta FROM EnviosPesquisas WHERE DataEnvio >= @dataInicio AND ClienteId = @clienteId` → Resultado: 58% |
| 15 | - | **Query 6 - CSAT Trend (últimos 30 dias)**: `SELECT CAST(DataResposta AS DATE) AS Dia, (COUNT(CASE WHEN CSAT >= 4 THEN 1 END) * 100.0 / COUNT(*)) AS CSATDia FROM RespostasPesquisas WHERE DataResposta >= DATEADD(day, -30, GETDATE()) GROUP BY CAST(DataResposta AS DATE) ORDER BY Dia` → Resultado: array de 30 pontos |
| 16 | - | **Query 7 - Top 10 Analistas**: `SELECT TOP 10 a.Nome, COUNT(r.Id) AS TotalAvaliacoes, AVG(r.CSAT) AS CSATMedio FROM RespostasPesquisas r INNER JOIN Chamados c ON r.ChamadoOrigemId = c.Id INNER JOIN Usuarios a ON c.AnalistaResponsavelId = a.Id WHERE r.DataResposta >= @dataInicio GROUP BY a.Id, a.Nome ORDER BY CSATMedio DESC` → Resultado: João Silva (4.8), Maria Santos (4.7), ... |
| 17 | - | **Query 8 - Word Cloud Keywords**: `SELECT TOP 50 keyword, COUNT(*) AS Frequencia FROM (SELECT UNNEST(Keywords) AS keyword FROM RespostasPesquisas WHERE DataResposta >= @dataInicio) GROUP BY keyword ORDER BY Frequencia DESC` → Resultado: ["rápido" (120), "eficiente" (95), "atencioso" (78), ...] |
| 18 | - | Backend agrega resultados: `var metricas = new DashboardMetricasDto { NPS = 42, NPSClassificacao = "Bom (Benchmark TI)", CSAT = 83.5m, CES = 2.8m, TotalRespostas = 1250, TaxaResposta = 58m, CSATTrend = [...], TopAnalistas = [...], WordCloud = [...] };` |
| 19 | - | Backend armazena em cache Redis (TTL 5min): `await _cache.SetStringAsync(cacheKey, JsonSerializer.Serialize(metricas), new DistributedCacheEntryOptions { AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5) });` |
| 20 | - | Backend retorna HTTP 200 OK com JSON de métricas |
| 21 | - | Frontend renderiza dashboard com 18 widgets: |
| 22 | - | **Widget 1 - NPS Gauge**: Semicírculo gauge com agulha apontando para 42, cores (vermelho 0-30, amarelo 30-50, verde 50+), label "NPS: 42 - Bom (Benchmark TI)" |
| 23 | - | **Widget 2 - CSAT Card**: Card grande com "83.5%" em fonte destacada, barra de progresso verde, comparativo "+2.3% vs mês anterior" |
| 24 | - | **Widget 3 - CES Card**: Card com "2.8" em fonte destacada, classificação "Bom (Baixo Esforço)", ícone ✅ verde |
| 25 | - | **Widget 4 - CSAT Trend Line**: Gráfico de linha Chart.js com 30 pontos (últimos 30 dias), eixo Y (0-100%), linha suave azul com área preenchida |
| 26 | - | **Widget 5 - Word Cloud**: Nuvem de palavras com tamanho proporcional à frequência, cores variadas, interativo (clique filtra dashboard por keyword) |
| 27 | - | **Widget 6 - Ranking Analistas**: Tabela com foto, nome, total avaliações, CSAT médio (estrelas), badge TOP 1/2/3 |
| 28 | - | Frontend escuta eventos SignalR: `_hubConnection.on("MetricasAtualizadas", (data) => { this.atualizarWidgets(data); });` |
| 29 | - | 5 minutos depois, nova resposta de pesquisa é processada (UC03) e evento `MetricasPesquisaAtualizadasEvent` é publicado |
| 30 | - | Backend SignalR Handler envia atualização: `await _hubContext.Clients.Group($"gestao_{clienteId}").SendAsync("MetricasAtualizadas", new { csat = 83.7m, totalRespostas = 1251 });` |
| 31 | - | Frontend recebe evento em tempo real, atualiza widgets com animação smooth: CSAT 83.5% → 83.7% (barra de progresso anima), Total Respostas 1.250 → 1.251 (contador incrementa) |
| 32 | - | Frontend exibe toast sutil: "Dashboard atualizado há 2 segundos" (canto inferior direito, auto-hide 3s) |

### 5. Fluxos Alternativos

**FA01: Aplicar Filtro por Categoria e Período Customizado**

- No passo 1, gestor acessa dashboard e abre painel lateral de filtros
- Gestor seleciona: Período "01/11/2025 - 30/11/2025", Categoria "Redes", Analista "Todos"
- Frontend envia `GET /api/pesquisas/dashboard/metricas?dataInicio=2025-11-01&dataFim=2025-11-30&categoria=Redes&clienteId={clienteId}`
- Backend adiciona filtros às queries: `WHERE DataResposta >= @dataInicio AND DataResposta <= @dataFim AND c.Categoria = 'Redes'`
- Backend retorna métricas filtradas: NPS = 38, CSAT = 79%, CES = 3.2 (categoria Redes tem métricas inferiores à média geral)
- Frontend atualiza todos os widgets com dados filtrados, exibe badge "Filtro Ativo: Redes (Nov/2025)" no topo do dashboard

**FA02: Exportar Dashboard para PowerBI Dataset**

- No passo 21, gestor clica em botão "Exportar" → "PowerBI Dataset"
- Frontend envia `GET /api/pesquisas/dashboard/export-powerbi?periodo=ultimos30dias&clienteId={clienteId}`
- Backend gera arquivo PBIX (PowerBI Dataset) com 5 tabelas: Respostas, Chamados, Analistas, Metricas_Diarias, Keywords
- Backend inclui relacionamentos entre tabelas (RespostaPesquisa.ChamadoId → Chamado.Id)
- Backend inclui medidas DAX pré-configuradas: `NPS = CALCULATE((COUNTROWS(FILTER(Respostas, Respostas[Nota] >= 9)) / COUNTROWS(Respostas)) * 100 - (COUNTROWS(FILTER(Respostas, Respostas[Nota] <= 6)) / COUNTROWS(Respostas)) * 100)`
- Backend retorna file download: `Dashboard-Satisfacao-2025-12-28.pbix` (5.2 MB)
- Gestor abre arquivo no PowerBI Desktop, visualiza relatório interativo completo com drill-down

**FA03: Configurar Alerta de Queda de NPS >5 Pontos em 7 Dias**

- No passo 1, gestor clica em botão "Configurar Alertas"
- Frontend abre modal com 8 condições pré-configuradas: [Queda NPS >5pts em 7 dias ▼], [CSAT <70% ▼], [CES >5.0 ▼], [Spike Detratores >20% ▼], [Taxa Resposta <30% ▼], [Sentimento Negativo >50% ▼], [Comentário com palavras-gatilho ▼], [Customizado ▼]
- Gestor seleciona "Queda NPS >5pts em 7 dias", configura destinatários: [gestor@empresa.com, diretor@empresa.com], canais: [E-mail ☑, SMS ☑, In-App ☑]
- Frontend envia `POST /api/pesquisas/alertas/configurar` com body: `{ condicao: "NPS_QUEDA_5PTS_7D", destinatarios: [...], canais: [...], ativo: true }`
- Backend cria alerta: `INSERT INTO AlertasPesquisas (ClienteId, Condicao, Parametros, Destinatarios, Canais, Ativo)`
- Backend registra job Hangfire: `RecurringJob.AddOrUpdate("MonitorarNPS_{clienteId}", () => MonitorarQuedaNPSJob.Execute(clienteId), Cron.Hourly);`
- Job executa a cada hora, compara NPS atual com NPS de 7 dias atrás, se diferença > 5 pontos: dispara alerta via canais configurados

**FA04: Drill-Down em Word Cloud - Filtrar por Keyword**

- No passo 26, gestor clica na palavra "demorado" no Word Cloud (apareceu 45 vezes)
- Frontend captura evento click, aplica filtro: `filtro.keyword = "demorado"`
- Frontend envia `GET /api/pesquisas/dashboard/metricas?periodo=ultimos30dias&keyword=demorado&clienteId={clienteId}`
- Backend filtra: `WHERE Keywords LIKE '%demorado%'` (busca respostas que contém keyword "demorado")
- Backend retorna métricas: CSAT médio das respostas com "demorado" = 2.3 (muito baixo, confirma correlação negativa)
- Frontend atualiza dashboard mostrando apenas dados de respostas com "demorado", exibe badge "Filtro: Comentários contendo 'demorado' (45 respostas, CSAT 2.3)"
- Frontend renderiza lista de comentários completos abaixo: "Atendimento demorado mas resolveu", "Muito demorado para responder", etc.

**FA05: Dashboard Mobile Responsivo com Progressive Web App (PWA)**

- Gestor acessa dashboard via smartphone usando PWA instalado
- Frontend detecta viewport <768px, alterna para layout mobile com widgets empilhados verticalmente
- Widgets adaptam visualização: Gauge NPS fica menor mas mantém legibilidade, CSAT Trend vira gráfico de barras (melhor em tela pequena), Word Cloud reduz para top 20 keywords
- Frontend usa Service Workers para cache offline: métricas carregadas anteriormente ficam disponíveis offline com badge "Dados em cache (atualizados há 2h)"
- Gestor pode arrastar para baixo (pull-to-refresh) para forçar atualização de dados quando online
- Notificações push PWA ativadas: quando detrator NPS identificado, gestor recebe push notification no smartphone mesmo com browser fechado

### 6. Exceções

**EX01: SignalR Hub Offline - Fallback para Polling**

- No passo 3, frontend tenta estabelecer conexão SignalR mas hub está offline (HTTP 503)
- Frontend captura exceção `HubConnectionError`, registra log WARNING: "SignalR indisponível, usando fallback polling"
- Frontend inicia polling a cada 30 segundos: `setInterval(() => { this.carregarMetricas(); }, 30000);`
- Frontend exibe badge amarelo no dashboard: "⚠️ Atualização automática desabilitada (modo polling ativo)"
- Funcionalidade continua operando mas sem tempo real (atualização a cada 30s ao invés de push imediato)

**EX02: Redis Cache Offline - Queries Diretas com Performance Reduzida**

- No passo 7, backend tenta acessar Redis mas serviço está indisponível: `_cache.GetStringAsync()` lança `RedisConnectionException`
- Backend captura exceção, registra log WARNING: "Redis offline, executando queries diretas sem cache"
- Backend pula passo 8, executa queries agregadas diretamente no SQL Server (passos 9-17)
- Latência aumenta de <50ms (cache hit) para ~800ms (queries complexas em tabela com 100k registros)
- Backend não armazena resultado em cache (passo 19 skipped)
- Funcionalidade continua operando mas com performance reduzida, backend dispara alerta para DevOps

**EX03: Usuário Sem Permissão de Dashboard (Apenas Analista, Não Gestor)**

- No passo 6, backend valida permissão e detecta que usuário é analista com permissão `service-desk:chamados:atender` mas NÃO tem `service-desk:pesquisa-satisfacao:dashboard`
- Backend retorna HTTP 403 com body: `{ "error": "FORBIDDEN", "message": "Apenas Gestores de Service Desk podem acessar o dashboard de satisfação. Entre em contato com o administrador." }`
- Frontend exibe página de erro 403: "Acesso Negado - Você não tem permissão para visualizar métricas de satisfação. Funcionalidade restrita a Gestores."

**EX04: Período Selecionado Muito Amplo - Performance Degradada**

- No passo FA01, gestor seleciona período "01/01/2023 - 31/12/2025" (3 anos completos)
- Backend valida período: `if ((dataFim - dataInicio).TotalDays > 365)` → true (período > 1 ano)
- Backend retorna HTTP 400 com body: `{ "error": "PERIODO_MUITO_AMPLO", "message": "Período selecionado muito amplo (1095 dias). Máximo permitido: 365 dias. Selecione um intervalo menor para melhor performance." }`
- Frontend exibe toast de erro: "Período máximo: 1 ano. Selecione um intervalo menor."

### 7. Pós-condições

- Dashboard renderizado com métricas atualizadas
- Conexão SignalR estabelecida para atualizações tempo real
- Cache Redis populado (TTL 5min)
- Filtros aplicados conforme seleção do usuário
- Alertas configurados (se aplicável)
- Exportação de dados executada (se solicitada)

### 8. Regras de Negócio Aplicáveis

- **RN-RF071-002**: Cálculo Automático de NPS (exibido no widget NPS Gauge)
- **RN-RF071-006**: Validação de Taxa de Resposta Mínima (badge de alerta se < 30%)
- **RN-RF071-008**: Cálculo de CES (exibido no widget CES Card)

---

## UC05: Gerenciar Alertas e Recomendações de Melhoria

### 1. Descrição

Este caso de uso permite que Gestores de Service Desk configurem 8 tipos de alertas automatizados (queda NPS >5 pontos em 7 dias, CSAT <70%, CES >5.0, spike detratores >20%, taxa resposta <30%, sentimento negativo >50%, comentários com palavras-gatilho customizadas, condições customizadas com operadores lógicos), definam destinatários multi-canal (e-mail, SMS, in-app, webhook), estabeleçam limiares e janelas temporais, visualizem histórico de alertas disparados com ações tomadas, criem planos de ação vinculados a alertas, acompanhem execução de recomendações de melhoria geradas automaticamente via análise de padrões (ex: 75% insatisfação em categoria "Redes" → recomendação "Investigar processo/equipe Redes"), e exportem relatórios de compliance de SLA de follow-up (<2h para detratores).

### 2. Atores

- Gestor de Service Desk
- Sistema (Backend .NET 10, Hangfire, SendGrid, Twilio)

### 3. Pré-condições

- Usuário autenticado no sistema
- Permissão: `service-desk:pesquisa-satisfacao:gestao`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `SERVICE_DESK_PESQUISA_SATISFACAO` habilitada
- Hangfire configurado para jobs recorrentes

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa rota `/service-desk/pesquisas/alertas` | - |
| 2 | - | Frontend envia `GET /api/pesquisas/alertas?clienteId={clienteId}` |
| 3 | - | Backend retorna lista de alertas configurados com status (Ativo/Inativo), última verificação, total de disparos (últimos 30 dias) |
| 4 | - | Frontend renderiza tabela: "Queda NPS >5pts em 7 dias (Ativo, verificado há 1h, 2 disparos)", "CSAT <70% (Inativo, nunca verificado, 0 disparos)" |
| 5 | Gestor clica em botão "Criar Novo Alerta" | - |
| 6 | - | Frontend abre modal com formulário: "Tipo de Alerta: [Queda NPS >5pts em 7 dias ▼]", "Limiares: [NPS anterior - NPS atual > [5] pontos]", "Janela Temporal: [7] dias" |
| 7 | Gestor seleciona tipo "CSAT Abaixo de Threshold", configura limiar "70%", janela "24 horas" (alerta se CSAT <70% em qualquer período de 24h) | - |
| 8 | Gestor configura destinatários: adiciona 3 e-mails (gestor@empresa.com, diretor@empresa.com, qualidade@empresa.com) + 1 webhook (https://hooks.slack.com/services/ABC123) | - |
| 9 | Gestor configura canais: ☑ E-mail, ☐ SMS, ☑ In-App, ☑ Webhook | - |
| 10 | Gestor configura severidade: "Crítica" (envio imediato), recorrência: "A cada ocorrência" (sem throttling de alertas) | - |
| 11 | Gestor clica em "Salvar Alerta" | - |
| 12 | - | Frontend envia `POST /api/pesquisas/alertas` with body JSON: `{ tipo: "CSAT_THRESHOLD", parametros: { threshold: 70, janelaTemporal: 24 }, destinatarios: [...], canais: ["Email", "InApp", "Webhook"], severidade: "Critica", recorrencia: "CadaOcorrencia", ativo: true }` |
| 13 | - | Backend valida configuração: threshold válido (0-100), janela temporal >0, destinatários ≥1, canais ≥1 |
| 14 | - | Backend cria alerta: `INSERT INTO AlertasPesquisas (ClienteId, Tipo, Parametros, Destinatarios, Canais, Severidade, Recorrencia, Ativo, DataCriacao)` |
| 15 | - | **Backend - Registro Job Hangfire**: Backend cria recurring job: `RecurringJob.AddOrUpdate($"MonitorarCSAT_{alertaId}", () => MonitorarCSATThresholdJob.Execute(alertaId), Cron.Hourly);` (verifica a cada hora) |
| 16 | - | Backend retorna HTTP 201 Created com `AlertaDto` contendo Id, Tipo, Status = Ativo |
| 17 | - | Frontend exibe toast de sucesso: "Alerta 'CSAT <70%' criado e ativo. Monitoramento a cada hora." |
| 18 | - | Frontend adiciona novo alerta à lista com badge verde "Ativo" |
| 19 | 3 horas depois, Hangfire executa job `MonitorarCSATThresholdJob` | - |
| 20 | - | Job carrega configuração do alerta: `var alerta = await _context.AlertasPesquisas.Include(a => a.Destinatarios).FirstAsync(a => a.Id == alertaId);` |
| 21 | - | Job calcula CSAT das últimas 24h: `var respostas24h = await _context.RespostasPesquisas.Where(r => r.DataResposta >= DateTime.UtcNow.AddHours(-24) && r.ClienteId == alerta.ClienteId && r.TemplateId IN (CSAT templates)).ToListAsync();` |
| 22 | - | Job calcula: `var csat = (respostas24h.Count(r => r.CSAT >= 4) * 100.0m) / respostas24h.Count;` → Resultado: 68.5% |
| 23 | - | Job valida condição: `if (csat < alerta.Parametros.Threshold)` → true (68.5 < 70) |
| 24 | - | Job verifica se já disparou recentemente (anti-spam): `var ultimoDisparo = await _context.HistoricoAlertas.Where(h => h.AlertaId == alertaId).OrderByDescending(h => h.DataDisparo).FirstOrDefaultAsync();` |
| 25 | - | Se recorrencia = "CadaOcorrencia": Job sempre dispara (sem throttling) |
| 26 | - | Job cria registro de disparo: `var disparo = new HistoricoAlerta { AlertaId = alertaId, DataDisparo = DateTime.UtcNow, Condicao = $"CSAT 68.5% < 70% (últimas 24h)", Dados = JsonSerializer.Serialize(new { csat, totalRespostas = respostas24h.Count }) };` |
| 27 | - | Job dispara notificações em paralelo para cada canal configurado: |
| 28 | - | **Canal E-mail**: `await _emailService.EnviarTemplateAsync("ALERTA_CRITICO", new { destinatarios = alerta.Destinatarios.Select(d => d.Email), titulo = "ALERTA CRÍTICO: CSAT Abaixo de 70%", mensagem = $"CSAT atual: 68.5% (últimas 24h)\nThreshold configurado: 70%\nTotal respostas analisadas: 245\nAção recomendada: Investigar causas de insatisfação imediatas." });` |
| 29 | - | **Canal In-App**: `await _notificacaoService.EnviarAsync(new Notificacao { DestinatarioIds = alerta.Destinatarios.Select(d => d.Id).ToList(), Tipo = "ALERTA_CRITICO", Titulo = "CSAT Abaixo de 70%", Mensagem = "...", Link = "/service-desk/pesquisas/dashboard?filtro=ultimas24h" });` |
| 30 | - | **Canal Webhook (Slack)**: `await _httpClient.PostAsJsonAsync(alerta.Parametros.WebhookUrl, new { text = "🚨 ALERTA CRÍTICO: CSAT 68.5% (threshold: 70%) - Últimas 24h", attachments = [{ color = "danger", fields = [{ title = "CSAT Atual", value = "68.5%", short = true }, { title = "Total Respostas", value = "245", short = true }] }] });` |
| 31 | - | Job atualiza alerta: `alerta.UltimaVerificacao = DateTime.UtcNow; alerta.TotalDisparos++;` |
| 32 | - | Job salva histórico: `_context.HistoricoAlertas.Add(disparo); await _context.SaveChangesAsync();` |
| 33 | - | Job finaliza execução, registra log INFO: "Alerta {alertaId} disparado. Condição: CSAT 68.5% < 70%. Notificações enviadas via Email, InApp, Webhook." |
| 34 | Gestor recebe e-mail, notificação in-app e mensagem no Slack simultaneamente | - |
| 35 | Gestor acessa dashboard, clica no alerta na seção "Alertas Ativos" | - |
| 36 | - | Frontend navega para `/service-desk/pesquisas/alertas/{id}/historico` |
| 37 | - | Frontend envia `GET /api/pesquisas/alertas/{id}/historico` |
| 38 | - | Backend retorna histórico de disparos do alerta com data, condição detectada, dados snapshot, ações tomadas (se registradas) |
| 39 | - | Frontend renderiza timeline: "28/12/2025 15:30 - CSAT 68.5% < 70% (245 respostas) - Ação: [Registrar Ação Tomada]", "25/12/2025 10:15 - CSAT 69.2% < 70% (198 respostas) - Ação: Investigação de processos iniciada" |
| 40 | Gestor clica em "Registrar Ação Tomada" no disparo mais recente | - |
| 41 | - | Frontend exibe modal: "Ação tomada: [Reunião com equipe agendada para 29/12 ____]", "Responsável: [João Silva ▼]", "Prazo: [29/12/2025 ____]" |
| 42 | Gestor preenche e salva | - |
| 43 | - | Frontend envia `PATCH /api/pesquisas/alertas/historico/{disparoId}/acao` com body: `{ acao: "Reunião com equipe agendada para 29/12", responsavelId, prazo }` |
| 44 | - | Backend atualiza: `UPDATE HistoricoAlertas SET AcaoTomada = @acao, ResponsavelId = @responsavelId, PrazoAcao = @prazo, DataRegistroAcao = @now WHERE Id = @disparoId` |
| 45 | - | Frontend atualiza timeline exibindo ação registrada com badge amarelo "Em Andamento" |

### 5. Fluxos Alternativos

**FA01: Alerta com Palavras-Gatilho em Comentários**

- No passo 7, gestor cria alerta tipo "Comentário com Palavras-Gatilho"
- Gestor configura lista de palavras: ["péssimo", "horrível", "nunca mais", "cancelar", "processarei", "advogado"]
- Backend cria job: `RecurringJob.AddOrUpdate($"MonitorarPalavrasGatilho_{alertaId}", () => MonitorarComentariosJob.Execute(alertaId), "*/15 * * * *");` (verifica a cada 15min)
- Job busca respostas recentes: `var respostas15min = await _context.RespostasPesquisas.Where(r => r.DataResposta >= DateTime.UtcNow.AddMinutes(-15)).ToListAsync();`
- Job verifica cada comentário: `foreach (var resposta in respostas15min) { var comentario = JsonSerializer.Deserialize<List<RespostaItem>>(resposta.RespostasJson).FirstOrDefault(r => r.Tipo == "TEXTO_LIVRE")?.Valor.ToLower(); if (palavrasGatilho.Any(p => comentario.Contains(p))) { /* dispara alerta */ } }`
- Se palavra "processarei" detectada: Job dispara alerta urgente com severidade "Crítica", envia SMS + e-mail + in-app imediatos, marca resposta com flag `RequereAtencaoUrgente = true`

**FA02: Recomendação Automática Gerada por Padrão de Insatisfação**

- Durante UC03, handler de correlação detecta padrão: 18 das últimas 20 respostas CSAT ≤3 são de categoria "Suporte Nível 2"
- Handler calcula insatisfação: `18/20 = 90%`
- Handler cria recomendação automaticamente: `INSERT INTO Recomendacoes (ClienteId, Tipo, Categoria, Descricao, Prioridade, Status, DataCriacao) VALUES (@clienteId, 'PADRAO_INSATISFACAO', 'Suporte Nível 2', '90% de insatisfação detectada em Suporte Nível 2. Recomendações: (1) Revisar SLA de resposta, (2) Treinamento técnico equipe, (3) Análise de ferramentas disponíveis', 'Alta', 'Pendente', @now)`
- Backend envia notificação para gestor: "Nova recomendação de melhoria gerada automaticamente - Suporte Nível 2"
- Gestor acessa `/service-desk/pesquisas/recomendacoes`, visualiza card com recomendação, pode: (1) Aceitar e criar plano de ação, (2) Adiar, (3) Rejeitar com justificativa
- Se aceitar: Frontend abre wizard de plano de ação com 3 etapas sugeridas automaticamente, gestor ajusta e salva

**FA03: Exportar Relatório de Compliance de Follow-up Detratores**

- No passo 1, gestor acessa aba "Compliance" no módulo de alertas
- Frontend envia `GET /api/pesquisas/compliance/follow-up-detratores?periodo=ultimoMes&clienteId={clienteId}`
- Backend busca todos os detratores (NPS 0-6) do último mês: `var detratores = await _context.RespostasPesquisas.Where(r => r.Nota <= 6 && r.DataResposta >= inicioMes).ToListAsync();`
- Backend analisa cada detrator: tempo entre resposta e follow-up (DataFollowUp - DataResposta)
- Backend calcula compliance: `var dentroDoPrazo = detratores.Count(d => d.FollowUpDetrator && (d.DataFollowUp - d.DataResposta).TotalHours <= 2); var percentualCompliance = (dentroDoPrazo * 100.0m) / detratores.Count;` → Resultado: 94.5% (36 de 38 follow-ups dentro do SLA <2h)
- Backend retorna: `{ totalDetratores: 38, followUpsRealizados: 36, followUpsNoPrazo: 36, percentualCompliance: 94.5m, detalhes: [...] }`
- Frontend renderiza relatório com card verde: "94.5% Compliance SLA Follow-up (<2h)" e tabela com detalhamento de cada detrator (nome, nota, data resposta, data follow-up, tempo decorrido, status)
- Frontend permite exportar relatório em PDF com assinatura digital para auditoria

**FA04: Alerta Customizado com Operadores Lógicos Complexos**

- No passo 7, gestor seleciona tipo "Customizado"
- Frontend exibe builder de condição com operadores: `[CSAT ▼] [< ▼] [80] [E ▼] [CES ▼] [> ▼] [4.0] [E ▼] [Categoria ▼] [= ▼] [Financeiro ▼]`
- Gestor configura: "CSAT < 80 E CES > 4.0 E Categoria = Financeiro" (condição composta: insatisfação alta + esforço alto em categoria específica)
- Backend serializa condição: `{ "operator": "AND", "conditions": [{ "field": "CSAT", "operator": "<", "value": 80 }, { "field": "CES", "operator": ">", "value": 4.0 }, { "field": "Categoria", "operator": "=", "value": "Financeiro" }] }`
- Job avalia condição dinamicamente: `var respostas = await _context.RespostasPesquisas.Where(r => r.CSAT < 80 && r.CES > 4.0 && r.ChamadoOrigem.Categoria == "Financeiro" && r.DataResposta >= dataLimite).ToListAsync();`
- Se `respostas.Any()` → Dispara alerta com detalhamento: "3 respostas atendem critério customizado (CSAT <80 E CES >4 E Categoria Financeiro)"

### 6. Exceções

**EX01: Webhook Inválido ou Offline - Falha no Envio**

- No passo 30, job tenta enviar payload para webhook Slack mas URL retorna HTTP 404 Not Found
- Job captura exceção `HttpRequestException`, registra log WARNING: "Falha ao enviar webhook para {webhookUrl}. Status: 404 Not Found"
- Job marca canal como falho: `disparo.CanaisFalhados = ["Webhook"];`
- Job continua disparando outros canais (e-mail e in-app enviados com sucesso)
- Job envia notificação para admin: "Webhook do alerta {alertaId} está inválido ou offline. Verifique configuração."

**EX02: Nenhum Destinatário Configurado - Alerta Bloqueado**

- No passo 13, gestor tenta salvar alerta mas campo destinatários está vazio (esqueceu de adicionar)
- Backend valida: `if (request.Destinatarios == null || request.Destinatarios.Count == 0)` → true
- Backend retorna HTTP 400 com body: `{ "errors": { "destinatarios": ["Alerta deve ter pelo menos 1 destinatário. Adicione e-mails, telefones ou webhooks."] } }`
- Frontend exibe erro inline: "⚠️ Adicione pelo menos um destinatário antes de salvar"

**EX03: Tentativa de Criar Alerta Duplicado (Mesma Condição Já Existe)**

- No passo 13, backend detecta que já existe alerta ativo com mesma configuração: `var alertaDuplicado = await _context.AlertasPesquisas.AnyAsync(a => a.Tipo == request.Tipo && a.Parametros == request.Parametros && a.ClienteId == request.ClienteId && a.Ativo);`
- Backend retorna HTTP 409 Conflict com body: `{ "error": "ALERTA_DUPLICADO", "message": "Já existe um alerta ativo com esta condição (CSAT <70%). Edite o alerta existente ou desative-o antes de criar um novo." }`
- Frontend exibe toast de erro com link para alerta existente: "Alerta duplicado - [Ver alerta existente](/service-desk/pesquisas/alertas/{idExistente})"

**EX04: Job Hangfire Falha Após 3 Tentativas - Alerta Marcado como Falhado**

- No passo 19, Hangfire tenta executar job mas ocorre exceção não tratada: `SqlException: Connection timeout`
- Hangfire executa retry automático (tentativa 2 após 1min, tentativa 3 após 5min)
- Após 3 falhas, Hangfire marca job como Failed
- Backend captura evento de job failed, atualiza: `UPDATE AlertasPesquisas SET Status = 'Erro', UltimaFalha = @now, MotivoFalha = 'Timeout de conexão SQL após 3 tentativas' WHERE Id = @alertaId`
- Backend envia notificação crítica para admin: "Alerta {alertaId} em estado de erro. Monitoramento pausado. Verifique logs."

### 7. Pós-condições

- Alertas configurados e monitorados via Hangfire recurring jobs
- Notificações multi-canal enviadas quando condições atingidas
- Histórico de disparos registrado com ações tomadas
- Recomendações de melhoria geradas e rastreadas
- Relatórios de compliance exportados
- Métricas de efetividade de alertas disponíveis

### 8. Regras de Negócio Aplicáveis

- **RN-RF071-003**: Follow-up Automático para Detratores (monitorado via alerta de compliance SLA <2h)
- **RN-RF071-006**: Validação de Taxa de Resposta Mínima (alerta se <30%)

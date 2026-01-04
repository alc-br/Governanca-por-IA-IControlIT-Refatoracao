# Casos de Uso - RF067 - Central de E-mails

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF067 - Central de E-mails](./RF067.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Listar E-mails (Fila de Envio) | Visualizar fila de e-mails com filtros de status, prioridade e data |
| UC02 | Criar E-mail | Criar novo e-mail para envio imediato ou agendado |
| UC03 | Editar E-mail (Rascunho) | Editar e-mails ainda não enviados |
| UC04 | Visualizar E-mail | Ver detalhes completos de um e-mail e seus eventos |
| UC05 | Excluir E-mail | Remover e-mail da fila (somente não enviados) |
| UC06 | Enviar E-mail (Processar Fila) | Processar fila de envio com retry automático |
| UC07 | Reenviar E-mail | Reenviar e-mail que falhou ou foi cancelado |
| UC08 | Agendar Envio | Agendar e-mail para envio futuro |
| UC09 | Consultar Histórico | Visualizar histórico completo de envios e eventos |
| UC10 | Gerenciar Blacklist | Adicionar/remover e-mails da lista de bloqueio |

---

## UC01 - Listar E-mails (Fila de Envio)

### Descrição
Permite visualizar a fila completa de e-mails com filtros por status, prioridade, destinatário e período, exibindo informações de rastreamento e eventos.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.VIEW_ALL`
- Administrador do sistema

### Pré-condições
- Usuário logado no sistema
- Permissão de visualização de e-mails
- Central de E-mails configurada

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Notificações → Central de E-mails" | - |
| 2 | - | Carrega lista paginada de e-mails (últimos 7 dias) |
| 3 | - | Exibe grid com colunas: Status, Prioridade, Remetente, Destinatário, Assunto, Data Envio, Taxa Abertura, Ações |
| 4 | Pode filtrar por status/prioridade/período | Sistema aplica filtros e atualiza lista |
| 5 | Pode buscar por destinatário ou assunto | Sistema filtra resultados |
| 6 | - | Exibe contadores: Total Fila, Enviados, Falhas, Taxa Entrega |

### Campos Exibidos

| Coluna | Descrição | Formato |
|--------|-----------|---------|
| Status | Badge colorido (FILA, ENVIADO, ENTREGUE, BOUNCE, SPAM) | Badge |
| Prioridade | Ícone de prioridade (🔴 Crítica, 🟡 Normal, 🟢 Baixa) | Icon + Text |
| Remetente | Nome e e-mail do remetente | Text |
| Destinatário | E-mail do destinatário | Text |
| Assunto | Assunto do e-mail (truncado se > 50 chars) | Text com tooltip |
| Data Envio | Data/hora do envio ou agendamento | DateTime |
| Aberto | Indicador se foi aberto (✓/✗) | Icon |
| Cliques | Total de cliques em links | Number |
| Tentativas | Tentativas de envio realizadas | Number (x/5) |
| Ações | Visualizar, Reenviar, Excluir (condicional) | Action buttons |

### Filtros Disponíveis

| Filtro | Tipo | Valores |
|--------|------|---------|
| Status | Dropdown | TODOS, FILA, ENVIADO, ENTREGUE, BOUNCE, SPAM, FALHA |
| Prioridade | Dropdown | TODAS, Crítica, Alta, Normal, Baixa, Bulk |
| Período | DateRange | Últimos 7/30/90 dias, Personalizado |
| Destinatário | Text | Busca por e-mail ou nome |
| Assunto | Text | Busca no assunto |

### Fluxos Alternativos

**FA01 - Lista Vazia**
- **Condição:** Não existem e-mails no período filtrado
- **Ação:** Sistema exibe mensagem "Nenhum e-mail encontrado no período selecionado"

**FA02 - Filtro por Status FILA**
- **Condição:** Usuário filtra por "FILA"
- **Ação:** Sistema exibe apenas e-mails aguardando envio, ordenados por prioridade

**FA03 - Ordenação**
- **Condição:** Usuário clica em cabeçalho de coluna
- **Ação:** Sistema ordena lista pela coluna selecionada (ASC/DESC)

**FA04 - Exportar Lista**
- **Condição:** Usuário clica em "Exportar CSV"
- **Ação:** Sistema gera arquivo CSV com lista filtrada

### Exceções

**EX01 - Erro ao Carregar Fila**
- **Condição:** Falha na comunicação com servidor
- **Ação:** Sistema exibe mensagem de erro e botão "Tentar novamente"

**EX02 - Timeout na Consulta**
- **Condição:** Consulta demora mais de 30 segundos
- **Ação:** Sistema exibe mensagem "A consulta está demorando. Tente filtrar por período menor"

### Pós-condições
- Lista exibida com dados atualizados
- Contadores de status calculados
- Filtros aplicados salvos na sessão

### Regras de Negócio Aplicáveis
- **RN001:** Fila de Prioridades - E-mails exibidos com indicador visual de prioridade
- **RN004:** Rastreamento Completo - Exibir eventos de abertura e cliques
- **RN013:** Supressão de Duplicatas - Indicar e-mails bloqueados por duplicidade

### i18n (Chaves de Tradução)

```json
{
  "emails.list.title": "Central de E-mails",
  "emails.list.filter.status": "Status",
  "emails.list.filter.priority": "Prioridade",
  "emails.list.filter.period": "Período",
  "emails.list.col.status": "Status",
  "emails.list.col.priority": "Prioridade",
  "emails.list.col.sender": "Remetente",
  "emails.list.col.recipient": "Destinatário",
  "emails.list.col.subject": "Assunto",
  "emails.list.col.sent_date": "Data Envio",
  "emails.list.col.opened": "Aberto",
  "emails.list.col.clicks": "Cliques",
  "emails.list.col.attempts": "Tentativas",
  "emails.list.counter.queue": "Na Fila",
  "emails.list.counter.sent": "Enviados",
  "emails.list.counter.failed": "Falhas",
  "emails.list.counter.delivery_rate": "Taxa Entrega",
  "emails.list.empty": "Nenhum e-mail encontrado no período selecionado",
  "emails.list.error": "Erro ao carregar lista de e-mails",
  "emails.list.export": "Exportar CSV"
}
```

---

## UC02 - Criar E-mail

### Descrição
Permite criar novo e-mail para envio imediato ou agendado, com opção de usar templates ou criar manualmente.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.SEND`
- Sistema (criação automática de e-mails transacionais)

### Pré-condições
- Usuário logado no sistema
- Permissão de envio de e-mails
- Pelo menos 1 servidor SMTP configurado e ativo

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Novo E-mail" | - |
| 2 | - | Exibe formulário de criação |
| 3 | Seleciona prioridade | - |
| 4 | Preenche destinatário (com validação) | Sistema valida formato de e-mail |
| 5 | (Opcional) Seleciona template | Sistema carrega conteúdo do template |
| 6 | Preenche assunto e corpo (HTML) | - |
| 7 | Define ação: Enviar Agora / Agendar / Salvar Rascunho | - |
| 8 | Clica em ação selecionada | - |
| 9 | - | Valida dados (RN008 - validação de e-mail) |
| 10 | - | Verifica blacklist (RN005) |
| 11 | - | Verifica duplicatas (RN013) |
| 12 | - | Salva e-mail com status apropriado (FILA/AGENDADO/RASCUNHO) |
| 13 | - | Se "Enviar Agora", enfileira job de envio |
| 14 | - | Exibe mensagem de sucesso |
| 15 | - | Redireciona para listagem |

### Campos do Formulário

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Prioridade | Dropdown | Sim | Crítica, Alta, Normal, Baixa, Bulk |
| Remetente | Text | Sim | Formato e-mail válido, domínio autorizado |
| Destinatário | Text/Autocomplete | Sim | Formato e-mail válido, não na blacklist |
| CC | Text (multi) | Não | Formato e-mail válido |
| BCC | Text (multi) | Não | Formato e-mail válido |
| Assunto | Text | Sim | Min 3, Max 200 caracteres |
| Template | Dropdown | Não | Lista de templates ativos |
| Corpo HTML | HTML Editor | Sim | Min 10 caracteres, HTML válido |
| Anexos | File Upload | Não | Max 10 MB total, tipos permitidos |
| Ação | Radio | Sim | Enviar Agora / Agendar / Salvar Rascunho |
| Data Agendamento | DateTime | Condicional | Obrigatório se "Agendar", > DateTime.Now |

### Fluxos Alternativos

**FA01 - Usar Template**
- **Condição:** Usuário seleciona template no dropdown
- **Ação:** Sistema carrega assunto e corpo do template, permitindo edição

**FA02 - Salvar como Rascunho**
- **Condição:** Usuário escolhe "Salvar Rascunho"
- **Ação:** Sistema salva com status RASCUNHO, não enfileira envio

**FA03 - Agendar Envio**
- **Condição:** Usuário escolhe "Agendar"
- **Ação:** Sistema exige data/hora futura, salva com status AGENDADO, cria job agendado no Hangfire

**FA04 - Adicionar Variáveis ao Corpo**
- **Condição:** Usuário clica em "Inserir Variável"
- **Ação:** Sistema exibe lista de variáveis disponíveis ({{Nome}}, {{Empresa}}, etc.)

**FA05 - Pré-visualizar E-mail**
- **Condição:** Usuário clica em "Pré-visualizar"
- **Ação:** Sistema abre modal com renderização do HTML do e-mail

### Exceções

**EX01 - Destinatário na Blacklist**
- **Condição:** E-mail está na blacklist
- **Ação:** Sistema bloqueia envio e exibe mensagem "E-mail {destinatario} está na blacklist. Motivo: {motivo}"

**EX02 - E-mail Duplicado**
- **Condição:** Mesmo e-mail enviado nas últimas 24h
- **Ação:** Sistema exibe aviso "E-mail similar enviado há {tempo}. Deseja enviar mesmo assim?" com opções Sim/Não

**EX03 - Domínio sem MX Record**
- **Condição:** Domínio do destinatário não tem MX record válido
- **Ação:** Sistema exibe erro "Domínio {dominio} não possui servidor de e-mail válido"

**EX04 - SMTP Indisponível**
- **Condição:** Nenhum servidor SMTP disponível
- **Ação:** Sistema exibe erro "Nenhum servidor SMTP disponível. Entre em contato com administrador"

**EX05 - Anexo Muito Grande**
- **Condição:** Anexos ultrapassam 10 MB
- **Ação:** Sistema exibe erro "Tamanho total dos anexos ({size} MB) excede o limite de 10 MB"

### Pós-condições
- E-mail criado no banco de dados
- Se "Enviar Agora": Job enfileirado no Hangfire (fila de prioridade correta)
- Se "Agendar": Job agendado para data/hora especificada
- Log de auditoria registrado (EMAIL_CRIADO)

### Regras de Negócio Aplicáveis
- **RN001:** Fila de Prioridades - E-mail enfileirado na fila correta conforme prioridade
- **RN005:** Blacklist Automática - Validar destinatário não está na blacklist
- **RN008:** Validação de E-mail - Validar sintaxe e MX record
- **RN013:** Supressão de Duplicatas - Alertar se e-mail duplicado

### i18n (Chaves de Tradução)

```json
{
  "emails.create.title": "Novo E-mail",
  "emails.create.priority": "Prioridade",
  "emails.create.sender": "Remetente",
  "emails.create.recipient": "Destinatário",
  "emails.create.cc": "CC (com cópia)",
  "emails.create.bcc": "BCC (cópia oculta)",
  "emails.create.subject": "Assunto",
  "emails.create.template": "Usar Template",
  "emails.create.body": "Corpo do E-mail (HTML)",
  "emails.create.attachments": "Anexos",
  "emails.create.action.send_now": "Enviar Agora",
  "emails.create.action.schedule": "Agendar",
  "emails.create.action.save_draft": "Salvar Rascunho",
  "emails.create.schedule_date": "Data/Hora de Envio",
  "emails.create.preview": "Pré-visualizar",
  "emails.create.insert_variable": "Inserir Variável",
  "emails.create.success": "E-mail criado com sucesso",
  "emails.create.error.blacklist": "E-mail {email} está na blacklist. Motivo: {reason}",
  "emails.create.error.duplicate": "E-mail similar enviado há {time}. Deseja enviar mesmo assim?",
  "emails.create.error.invalid_domain": "Domínio {domain} não possui servidor de e-mail válido",
  "emails.create.error.smtp_unavailable": "Nenhum servidor SMTP disponível. Entre em contato com administrador",
  "emails.create.error.attachment_too_large": "Tamanho total dos anexos ({size} MB) excede o limite de 10 MB"
}
```

---

## UC03 - Editar E-mail (Rascunho)

### Descrição
Permite editar e-mails salvos como rascunho ou agendados que ainda não foram enviados.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.SEND`

### Pré-condições
- Usuário logado no sistema
- E-mail existe no sistema
- E-mail com status RASCUNHO ou AGENDADO (não pode editar e-mails já enviados)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Na lista, clica em "Editar" em e-mail rascunho | - |
| 2 | - | Carrega dados do e-mail |
| 3 | - | Exibe formulário preenchido (mesmos campos de UC02) |
| 4 | Altera campos desejados | - |
| 5 | Clica em "Salvar" ou "Enviar Agora" ou "Agendar" | - |
| 6 | - | Valida dados (mesmas regras de UC02) |
| 7 | - | Atualiza registro no banco |
| 8 | - | Se "Enviar Agora", muda status para FILA e enfileira job |
| 9 | - | Exibe mensagem de sucesso |
| 10 | - | Redireciona para listagem |

### Fluxos Alternativos

**FA01 - Cancelar Edição**
- **Condição:** Usuário clica em "Cancelar"
- **Ação:** Sistema descarta alterações e retorna à listagem

**FA02 - Converter Rascunho em Envio Imediato**
- **Condição:** E-mail estava como RASCUNHO e usuário clica "Enviar Agora"
- **Ação:** Sistema valida tudo, muda status para FILA, enfileira job

**FA03 - Converter Agendado em Envio Imediato**
- **Condição:** E-mail estava AGENDADO e usuário clica "Enviar Agora"
- **Ação:** Sistema cancela job agendado, muda status para FILA, enfileira job imediato

### Exceções

**EX01 - E-mail Já Enviado**
- **Condição:** E-mail foi enviado entre o carregamento da lista e o clique em "Editar"
- **Ação:** Sistema exibe erro "E-mail já foi enviado e não pode mais ser editado"

**EX02 - E-mail Não Encontrado**
- **Condição:** E-mail foi excluído por outro usuário
- **Ação:** Sistema exibe mensagem e redireciona para listagem

**EX03 - Conflito de Edição Concorrente**
- **Condição:** Dois usuários editando o mesmo rascunho simultaneamente
- **Ação:** Sistema exibe mensagem "E-mail foi alterado por outro usuário. Recarregue para ver última versão"

### Pós-condições
- E-mail atualizado no banco de dados
- Se mudou status para FILA: Job enfileirado
- Log de auditoria registrado (EMAIL_ATUALIZADO)

### Regras de Negócio Aplicáveis
- **RN005:** Blacklist - Revalidar destinatário
- **RN008:** Validação de E-mail - Revalidar sintaxe e MX record
- **RN013:** Supressão de Duplicatas - Alertar se e-mail duplicado

### i18n (Chaves de Tradução)

```json
{
  "emails.edit.title": "Editar E-mail",
  "emails.edit.success": "E-mail atualizado com sucesso",
  "emails.edit.error.already_sent": "E-mail já foi enviado e não pode mais ser editado",
  "emails.edit.error.not_found": "E-mail não encontrado",
  "emails.edit.error.conflict": "E-mail foi alterado por outro usuário. Recarregue para ver última versão"
}
```

---

## UC04 - Visualizar E-mail

### Descrição
Permite visualizar detalhes completos de um e-mail, incluindo conteúdo, eventos de rastreamento, tentativas de envio e logs.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.VIEW_ALL`

### Pré-condições
- Usuário logado no sistema
- E-mail existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Na lista, clica em "Visualizar" | - |
| 2 | - | Carrega dados do e-mail e seus eventos |
| 3 | - | Exibe tela de detalhes em abas |

### Abas de Visualização

**Aba 1: Informações Gerais**
- Status atual (badge colorido)
- Prioridade
- Remetente
- Destinatário (e CC/BCC se houver)
- Assunto
- Data de criação
- Data de envio (se enviado)
- Data de abertura (se aberto)
- Total de cliques em links
- Tentativas de envio (x/5)
- Servidor SMTP utilizado
- Criado por (usuário)

**Aba 2: Conteúdo**
- Assunto
- Corpo HTML (renderizado em iframe)
- Anexos (lista com botão de download)

**Aba 3: Eventos de Rastreamento**
- Timeline visual com todos os eventos:
  - EMAIL_CRIADO
  - EMAIL_ENFILEIRADO
  - EMAIL_ENVIADO
  - EMAIL_ENTREGUE
  - EMAIL_ABERTO (com data, IP, User-Agent)
  - EMAIL_CLICADO (com URL clicada, data, IP)
  - EMAIL_BOUNCE (com motivo detalhado)
  - EMAIL_SPAM (com motivo)
  - EMAIL_UNSUBSCRIBE

**Aba 4: Logs de Tentativas**
- Tabela com todas as tentativas:
  - Tentativa #
  - Data/Hora
  - Servidor SMTP usado
  - Resultado (sucesso/erro)
  - Mensagem de erro (se houver)
  - Próxima tentativa agendada (se houver)

### Informações Exibidas

| Campo | Descrição |
|-------|-----------|
| Status | Badge colorido com status atual |
| Prioridade | Indicador visual de prioridade |
| Remetente | Nome e e-mail |
| Destinatário | E-mail principal |
| CC/BCC | Lista de e-mails em cópia (se houver) |
| Assunto | Assunto completo |
| Data Criação | Data/hora de criação |
| Data Envio | Data/hora de envio efetivo |
| Data Abertura | Primeira abertura (com IP e User-Agent) |
| Cliques | Total de cliques com lista de URLs clicadas |
| Tentativas | x/5 tentativas realizadas |
| SMTP | Servidor SMTP utilizado |
| Template | Template usado (se houver) |
| Criado Por | Usuário que criou o e-mail |

### Fluxos Alternativos

**FA01 - Editar a Partir da Visualização**
- **Condição:** E-mail é RASCUNHO ou AGENDADO e usuário clica "Editar"
- **Ação:** Sistema redireciona para UC03

**FA02 - Reenviar a Partir da Visualização**
- **Condição:** E-mail falhou (BOUNCE, FALHA) e usuário clica "Reenviar"
- **Ação:** Sistema redireciona para UC07

**FA03 - Exportar Detalhes**
- **Condição:** Usuário clica em "Exportar PDF"
- **Ação:** Sistema gera PDF com todos os detalhes e eventos

**FA04 - Abrir Eventos em Nova Aba**
- **Condição:** Usuário clica em evento específico
- **Ação:** Sistema exibe modal com detalhes completos do evento (JSON completo)

### Exceções

**EX01 - E-mail Não Encontrado**
- **Condição:** E-mail foi excluído
- **Ação:** Sistema exibe mensagem e redireciona para listagem

**EX02 - Erro ao Carregar Eventos**
- **Condição:** Falha ao buscar eventos de rastreamento
- **Ação:** Sistema exibe informações do e-mail mas indica erro na aba de eventos

### Pós-condições
- Nenhuma alteração no sistema (apenas visualização)
- Log de auditoria: EMAIL_VISUALIZADO

### Regras de Negócio Aplicáveis
- **RN004:** Rastreamento Completo - Exibir todos os eventos capturados

### i18n (Chaves de Tradução)

```json
{
  "emails.view.title": "Detalhes do E-mail",
  "emails.view.tab.general": "Informações Gerais",
  "emails.view.tab.content": "Conteúdo",
  "emails.view.tab.tracking": "Rastreamento",
  "emails.view.tab.logs": "Logs de Tentativas",
  "emails.view.status": "Status",
  "emails.view.priority": "Prioridade",
  "emails.view.sender": "Remetente",
  "emails.view.recipient": "Destinatário",
  "emails.view.cc": "CC",
  "emails.view.bcc": "BCC",
  "emails.view.subject": "Assunto",
  "emails.view.created_at": "Criado em",
  "emails.view.sent_at": "Enviado em",
  "emails.view.opened_at": "Aberto em",
  "emails.view.clicks": "Cliques",
  "emails.view.attempts": "Tentativas",
  "emails.view.smtp_server": "Servidor SMTP",
  "emails.view.template": "Template",
  "emails.view.created_by": "Criado por",
  "emails.view.attachments": "Anexos",
  "emails.view.export_pdf": "Exportar PDF",
  "emails.view.error.not_found": "E-mail não encontrado",
  "emails.view.error.tracking_failed": "Erro ao carregar eventos de rastreamento"
}
```

---

## UC05 - Excluir E-mail

### Descrição
Permite excluir (soft delete) e-mails da fila que ainda não foram enviados.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.SEND`

### Pré-condições
- Usuário logado no sistema
- E-mail existe no sistema
- E-mail com status RASCUNHO, FILA ou AGENDADO (não pode excluir e-mails já enviados)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Na lista, clica em "Excluir" | - |
| 2 | - | Exibe diálogo de confirmação com detalhes do e-mail |
| 3 | Confirma exclusão | - |
| 4 | - | Marca registro como excluído (soft delete) |
| 5 | - | Se AGENDADO, cancela job do Hangfire |
| 6 | - | Se FILA, remove da fila de processamento |
| 7 | - | Exibe mensagem de sucesso |
| 8 | - | Atualiza listagem (remove e-mail da view) |

### Fluxos Alternativos

**FA01 - Cancelar Exclusão**
- **Condição:** Usuário cancela no diálogo
- **Ação:** Sistema fecha diálogo e mantém e-mail

**FA02 - Exclusão em Lote**
- **Condição:** Usuário seleciona múltiplos e-mails e clica "Excluir Selecionados"
- **Ação:** Sistema exibe confirmação "Deseja excluir {count} e-mails?", exclui todos se confirmado

### Exceções

**EX01 - E-mail Já Enviado**
- **Condição:** E-mail foi enviado entre o carregamento da lista e o clique em "Excluir"
- **Ação:** Sistema exibe erro "E-mail já foi enviado e não pode ser excluído. Histórico de envios não pode ser apagado"

**EX02 - E-mail Não Encontrado**
- **Condição:** E-mail já foi excluído por outro usuário
- **Ação:** Sistema exibe mensagem informativa e atualiza listagem

**EX03 - Erro ao Cancelar Job Agendado**
- **Condição:** Falha ao cancelar job no Hangfire
- **Ação:** Sistema marca e-mail como excluído mas registra erro no log para investigação

### Pós-condições
- E-mail marcado como excluído (Fl_Excluido = true)
- Job do Hangfire cancelado (se agendado)
- Removido da fila de processamento (se na fila)
- Log de auditoria registrado (EMAIL_EXCLUIDO)

### Regras de Negócio Aplicáveis
- **RN:** E-mails enviados não podem ser excluídos (histórico deve ser mantido por 7 anos - LGPD)

### i18n (Chaves de Tradução)

```json
{
  "emails.delete.confirm.title": "Confirmar Exclusão",
  "emails.delete.confirm.message": "Deseja realmente excluir o e-mail para {recipient} com assunto '{subject}'?",
  "emails.delete.confirm.batch": "Deseja realmente excluir {count} e-mails?",
  "emails.delete.success": "E-mail excluído com sucesso",
  "emails.delete.success.batch": "{count} e-mails excluídos com sucesso",
  "emails.delete.error.already_sent": "E-mail já foi enviado e não pode ser excluído. Histórico de envios não pode ser apagado",
  "emails.delete.error.not_found": "E-mail não encontrado",
  "emails.delete.error.job_cancel_failed": "E-mail excluído mas houve erro ao cancelar agendamento"
}
```

---

## UC06 - Enviar E-mail (Processar Fila)

### Descrição
Job automático do Hangfire que processa a fila de e-mails, realizando validações, selecionando servidor SMTP, enviando e rastreando resultados.

### Atores
- Sistema (Hangfire Background Job)
- Servidor SMTP

### Pré-condições
- Fila de e-mails configurada no Hangfire
- Pelo menos 1 servidor SMTP ativo e saudável
- Rate limits não atingidos

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job do Hangfire dispara (filas: emails-criticos, emails-normais) |
| 2 | - | Busca próximo e-mail com status FILA na fila correspondente |
| 3 | - | Valida destinatário não está na blacklist (RN005) |
| 4 | - | Verifica rate limit do domínio (RN006) |
| 5 | - | Seleciona servidor SMTP disponível (RN002 - SMTP Pools) |
| 6 | - | Verifica warmup de IP (RN007) |
| 7 | - | Conecta ao servidor SMTP |
| 8 | - | Envia e-mail |
| 9 | - | Registra evento EMAIL_ENVIADO |
| 10 | - | Atualiza status para ENVIADO |
| 11 | - | Incrementa contadores (SMTPServer.EmailsEnviados24h) |
| 12 | - | Insere pixel de rastreamento no HTML para tracking de abertura |

### Fluxos Alternativos

**FA01 - Envio com Sucesso**
- **Condição:** E-mail enviado com sucesso
- **Ação:** Status = ENVIADO, registra evento EMAIL_ENVIADO com timestamp

**FA02 - E-mail Agendado**
- **Condição:** E-mail tem DataAgendamento no futuro
- **Ação:** Job não processa, mantém status AGENDADO até data/hora especificada

### Exceções

**EX01 - Destinatário na Blacklist**
- **Condição:** E-mail está na blacklist
- **Ação:** Status = BLOQUEADO, registra evento EMAIL_BLOQUEADO_BLACKLIST

**EX02 - Rate Limit Atingido**
- **Condição:** Domínio atingiu limite de envios/hora (RN006)
- **Ação:** Job reagenda e-mail para processar em 1 hora

**EX03 - Nenhum SMTP Disponível**
- **Condição:** Todos os servidores SMTP offline ou atingiram limite
- **Ação:** Job reagenda e-mail para processar em 5 minutos, alerta administrador

**EX04 - Falha no Envio (Soft Bounce)**
- **Condição:** Erro temporário (caixa cheia, servidor ocupado)
- **Ação:** Aplica retry com backoff exponencial (RN003), tentativa++, reagenda

**EX05 - Falha no Envio (Hard Bounce)**
- **Condição:** Erro permanente (e-mail inexistente, domínio inválido)
- **Ação:** Status = BOUNCE, adiciona destinatário à blacklist (RN005), registra evento EMAIL_BOUNCE

**EX06 - Timeout no SMTP**
- **Condição:** Conexão SMTP demora mais de 30 segundos
- **Ação:** Marca servidor como degradado, tenta outro servidor, retry do e-mail

**EX07 - Limite de Tentativas Atingido**
- **Condição:** 5 tentativas falhas (RN003)
- **Ação:** Status = FALHA_PERMANENTE, registra evento EMAIL_FALHA_PERMANENTE, notifica administrador

### Pós-condições
- E-mail enviado com sucesso OU
- E-mail reagendado para retry OU
- E-mail marcado como falha permanente
- Evento de rastreamento registrado
- Log de auditoria: EMAIL_ENVIADO / EMAIL_BOUNCE / EMAIL_FALHA

### Regras de Negócio Aplicáveis
- **RN001:** Fila de Prioridades - Processar fila emails-criticos antes de emails-normais
- **RN002:** SMTP Pools - Selecionar servidor com estratégia configurada
- **RN003:** Retry Automático - Até 5 tentativas com backoff exponencial
- **RN004:** Rastreamento - Inserir pixel tracking + links rastreáveis
- **RN005:** Blacklist - Adicionar hard bounces automaticamente
- **RN006:** Rate Limiting - Verificar limites por domínio
- **RN007:** Warmup de IPs - Respeitar limites de warmup

### Monitoramento

```csharp
// Métricas a serem coletadas:
- Emails enviados/minuto (por prioridade)
- Taxa de sucesso (%)
- Taxa de bounce (%)
- Taxa de retry (%)
- Tempo médio de envio
- Saúde dos servidores SMTP
```

---

## UC07 - Reenviar E-mail

### Descrição
Permite reenviar manualmente e-mails que falharam (bounce, falha permanente ou bloqueados).

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.SEND`

### Pré-condições
- Usuário logado no sistema
- E-mail existe no sistema
- E-mail com status BOUNCE, FALHA_PERMANENTE ou BLOQUEADO

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Na visualização do e-mail, clica em "Reenviar" | - |
| 2 | - | Exibe diálogo de confirmação com motivo da falha original |
| 3 | - | Permite editar destinatário (se bounce por e-mail inválido) |
| 4 | Confirma reenvio | - |
| 5 | - | Valida novo destinatário (se alterado) |
| 6 | - | Verifica blacklist |
| 7 | - | Cria NOVO registro de e-mail (clonando original) |
| 8 | - | Marca e-mail original como "Reenviado" (referência ao novo) |
| 9 | - | Enfileira novo e-mail para envio |
| 10 | - | Exibe mensagem de sucesso |
| 11 | - | Redireciona para visualização do novo e-mail |

### Campos do Diálogo de Reenvio

| Campo | Descrição | Editável |
|-------|-----------|----------|
| Motivo Falha Original | Motivo pelo qual o e-mail falhou | Não |
| Destinatário Original | E-mail que falhou | Não |
| Novo Destinatário | Permite corrigir e-mail | Sim (opcional) |
| Remover de Blacklist | Checkbox para remover da blacklist | Sim (se estiver na blacklist) |

### Fluxos Alternativos

**FA01 - Reenviar com Destinatário Corrigido**
- **Condição:** E-mail falhou por bounce e usuário corrige destinatário
- **Ação:** Sistema valida novo destinatário, cria novo e-mail com destinatário corrigido

**FA02 - Reenviar Forçando (Ignorar Blacklist)**
- **Condição:** Usuário marca "Remover de Blacklist"
- **Ação:** Sistema remove e-mail da blacklist, enfileira novo envio

**FA03 - Cancelar Reenvio**
- **Condição:** Usuário cancela no diálogo
- **Ação:** Sistema fecha diálogo, não faz nada

### Exceções

**EX01 - Novo Destinatário Inválido**
- **Condição:** Destinatário corrigido também é inválido
- **Ação:** Sistema exibe erro de validação, não permite reenvio

**EX02 - Novo Destinatário Também na Blacklist**
- **Condição:** Destinatário corrigido também está na blacklist
- **Ação:** Sistema exibe aviso "Novo destinatário também está na blacklist. Deseja remover?"

**EX03 - SMTP Ainda Indisponível**
- **Condição:** Servidor SMTP continua offline
- **Ação:** Sistema enfileira mesmo assim, será processado quando SMTP voltar

### Pós-condições
- Novo e-mail criado (clone do original)
- E-mail original marcado com referência ao novo
- Novo e-mail enfileirado para envio
- Log de auditoria: EMAIL_REENVIADO

### Regras de Negócio Aplicáveis
- **RN005:** Blacklist - Validar destinatário
- **RN008:** Validação de E-mail - Validar sintaxe e MX

### i18n (Chaves de Tradução)

```json
{
  "emails.resend.title": "Reenviar E-mail",
  "emails.resend.original_failure": "Motivo da Falha Original",
  "emails.resend.original_recipient": "Destinatário Original",
  "emails.resend.new_recipient": "Novo Destinatário (opcional)",
  "emails.resend.remove_from_blacklist": "Remover de Blacklist",
  "emails.resend.confirm": "Confirmar Reenvio",
  "emails.resend.success": "E-mail reenfileirado para envio com sucesso",
  "emails.resend.error.invalid_recipient": "Novo destinatário inválido",
  "emails.resend.error.blacklisted": "Novo destinatário também está na blacklist. Deseja remover?"
}
```

---

## UC08 - Agendar Envio

### Descrição
Permite agendar e-mails para envio futuro específico (ex: campanhas, aniversários, lembretes).

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.SEND`
- Sistema (Hangfire Scheduler)

### Pré-condições
- Usuário logado no sistema
- Permissão de envio de e-mails
- Data/hora de agendamento no futuro

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | No formulário de criação (UC02), seleciona "Agendar" | - |
| 2 | - | Exibe campo de data/hora |
| 3 | Informa data/hora futura | - |
| 4 | Preenche demais campos do e-mail | - |
| 5 | Clica em "Agendar Envio" | - |
| 6 | - | Valida data/hora é futura |
| 7 | - | Valida dados do e-mail |
| 8 | - | Salva e-mail com status AGENDADO |
| 9 | - | Cria job agendado no Hangfire para data/hora especificada |
| 10 | - | Exibe mensagem "E-mail agendado para {data/hora}" |
| 11 | - | Redireciona para listagem |

### Campos Específicos

| Campo | Tipo | Validação |
|-------|------|-----------|
| Data Agendamento | DateTime | Obrigatório, > DateTime.Now, < 1 ano no futuro |
| Timezone | Dropdown | Timezone da empresa (padrão: America/Sao_Paulo) |

### Fluxos Alternativos

**FA01 - Cancelar Agendamento**
- **Condição:** Usuário visualiza e-mail agendado e clica "Cancelar Agendamento"
- **Ação:** Sistema cancela job do Hangfire, muda status para RASCUNHO

**FA02 - Reagendar E-mail**
- **Condição:** Usuário edita e-mail agendado e altera data/hora
- **Ação:** Sistema cancela job antigo, cria novo job com nova data/hora

**FA03 - Enviar Agendado Imediatamente**
- **Condição:** Usuário visualiza e-mail agendado e clica "Enviar Agora"
- **Ação:** Sistema cancela job agendado, muda status para FILA, enfileira para envio imediato

### Exceções

**EX01 - Data no Passado**
- **Condição:** Data/hora informada está no passado
- **Ação:** Sistema exibe erro "Data de agendamento deve ser futura"

**EX02 - Data Muito Distante**
- **Condição:** Data/hora é mais de 1 ano no futuro
- **Ação:** Sistema exibe aviso "Não recomendamos agendar com mais de 1 ano de antecedência"

**EX03 - Erro ao Criar Job**
- **Condição:** Falha ao criar job no Hangfire
- **Ação:** Sistema exibe erro "Erro ao agendar e-mail. Tente novamente"

### Pós-condições
- E-mail salvo com status AGENDADO
- Job criado no Hangfire para processar na data/hora especificada
- Log de auditoria: EMAIL_AGENDADO

### Processamento no Hangfire

```csharp
// Job agendado executado na data/hora especificada
[Hangfire.DisableConcurrentExecution(10)]
public async Task ProcessarEmailAgendado(Guid emailId)
{
    var email = await _context.Emails.FindAsync(emailId);

    if (email.Status == "AGENDADO")
    {
        email.Status = "FILA";
        await _context.SaveChangesAsync();

        // Enfileirar para envio imediato
        BackgroundJob.Enqueue<EmailService>(s => s.EnviarEmail(emailId));
    }
}
```

### Regras de Negócio Aplicáveis
- **RN001:** Fila de Prioridades - E-mails agendados mantêm sua prioridade ao serem enfileirados

### i18n (Chaves de Tradução)

```json
{
  "emails.schedule.title": "Agendar Envio",
  "emails.schedule.date": "Data e Hora de Envio",
  "emails.schedule.timezone": "Fuso Horário",
  "emails.schedule.success": "E-mail agendado para {datetime}",
  "emails.schedule.cancel": "Cancelar Agendamento",
  "emails.schedule.reschedule": "Reagendar",
  "emails.schedule.send_now": "Enviar Agora",
  "emails.schedule.error.past_date": "Data de agendamento deve ser futura",
  "emails.schedule.error.too_far": "Não recomendamos agendar com mais de 1 ano de antecedência",
  "emails.schedule.error.job_failed": "Erro ao agendar e-mail. Tente novamente"
}
```

---

## UC09 - Consultar Histórico

### Descrição
Permite consultar histórico completo de envios com filtros avançados, métricas de deliverability e exportação de relatórios.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.VIEW_ALL`
- Gestor (visualização de métricas)

### Pré-condições
- Usuário logado no sistema
- Permissão de visualização

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa "Notificações → Histórico de E-mails" | - |
| 2 | - | Exibe dashboard de histórico com métricas |
| 3 | - | Exibe cards de resumo: Total Enviados, Taxa Entrega, Taxa Abertura, Taxa Bounce |
| 4 | - | Exibe gráfico de linha: Envios por dia (últimos 30 dias) |
| 5 | - | Exibe gráfico de pizza: Distribuição por status |
| 6 | - | Exibe lista paginada de e-mails históricos |
| 7 | Aplica filtros (período, status, destinatário) | Sistema atualiza métricas e lista |

### Cards de Métricas

| Métrica | Cálculo | Formato |
|---------|---------|---------|
| Total Enviados | COUNT(Status IN ('ENVIADO','ENTREGUE','BOUNCE')) | Number |
| Taxa Entrega | (ENTREGUE / ENVIADO) * 100 | % (2 decimais) |
| Taxa Abertura | (ABERTO / ENTREGUE) * 100 | % (2 decimais) |
| Taxa Bounce | (BOUNCE / ENVIADO) * 100 | % (2 decimais) |
| Taxa Spam | (SPAM / ENVIADO) * 100 | % (2 decimais) |
| Cliques Únicos | COUNT(DISTINCT EmailId WHERE TipoEvento='CLICADO') | Number |
| Unsubscribes | COUNT(TipoEvento='UNSUBSCRIBE') | Number |

### Gráficos

**Gráfico 1: Envios por Dia**
- Tipo: Linha (ApexCharts)
- Eixo X: Dias (últimos 30 dias)
- Eixo Y: Quantidade de e-mails
- Séries: Enviados, Entregues, Bounces

**Gráfico 2: Distribuição por Status**
- Tipo: Pizza (ApexCharts)
- Fatias: ENVIADO, ENTREGUE, BOUNCE, SPAM, FALHA

**Gráfico 3: Taxa de Abertura por Dia**
- Tipo: Área (ApexCharts)
- Eixo X: Dias
- Eixo Y: Taxa de abertura (%)

### Filtros Avançados

| Filtro | Tipo | Descrição |
|--------|------|-----------|
| Período | DateRange | Últimos 7/30/90 dias, Personalizado |
| Status | MultiSelect | ENVIADO, ENTREGUE, BOUNCE, SPAM, etc. |
| Prioridade | MultiSelect | Crítica, Alta, Normal, Baixa, Bulk |
| Destinatário | Text | Busca por e-mail |
| Remetente | Dropdown | Lista de remetentes cadastrados |
| Template | Dropdown | Lista de templates usados |
| Servidor SMTP | Dropdown | Lista de servidores SMTP |
| Aberto | Checkbox | Apenas e-mails abertos |
| Clicado | Checkbox | Apenas e-mails com cliques |

### Fluxos Alternativos

**FA01 - Exportar Relatório CSV**
- **Condição:** Usuário clica em "Exportar CSV"
- **Ação:** Sistema gera CSV com lista filtrada + métricas no cabeçalho

**FA02 - Exportar Relatório Excel**
- **Condição:** Usuário clica em "Exportar Excel"
- **Ação:** Sistema gera XLSX com múltiplas abas: Resumo, Lista, Eventos, Gráficos

**FA03 - Agendar Relatório Recorrente**
- **Condição:** Usuário clica em "Agendar Relatório"
- **Ação:** Sistema permite configurar envio automático (diário/semanal/mensal) por e-mail

**FA04 - Comparar Períodos**
- **Condição:** Usuário ativa "Comparar com período anterior"
- **Ação:** Sistema exibe métricas lado a lado (atual vs anterior) com % de variação

### Exceções

**EX01 - Sem Dados no Período**
- **Condição:** Filtros resultam em 0 e-mails
- **Ação:** Sistema exibe mensagem "Nenhum e-mail encontrado no período selecionado"

**EX02 - Timeout na Consulta**
- **Condição:** Consulta demora mais de 30 segundos (período muito amplo)
- **Ação:** Sistema exibe erro "Consulta muito ampla. Tente período menor"

### Pós-condições
- Métricas calculadas e exibidas
- Relatório exportado (se solicitado)
- Log de auditoria: RELATORIO_EMAILS_VISUALIZADO

### Regras de Negócio Aplicáveis
- **RN014:** Relatório de Deliverability - Exibir todas as métricas

### i18n (Chaves de Tradução)

```json
{
  "emails.history.title": "Histórico de E-mails",
  "emails.history.metric.total_sent": "Total Enviados",
  "emails.history.metric.delivery_rate": "Taxa de Entrega",
  "emails.history.metric.open_rate": "Taxa de Abertura",
  "emails.history.metric.bounce_rate": "Taxa de Bounce",
  "emails.history.metric.spam_rate": "Taxa de Spam",
  "emails.history.metric.unique_clicks": "Cliques Únicos",
  "emails.history.metric.unsubscribes": "Descadastros",
  "emails.history.chart.sends_per_day": "Envios por Dia",
  "emails.history.chart.status_distribution": "Distribuição por Status",
  "emails.history.chart.open_rate_trend": "Taxa de Abertura ao Longo do Tempo",
  "emails.history.filter.period": "Período",
  "emails.history.filter.status": "Status",
  "emails.history.filter.priority": "Prioridade",
  "emails.history.filter.recipient": "Destinatário",
  "emails.history.filter.sender": "Remetente",
  "emails.history.filter.template": "Template",
  "emails.history.filter.smtp": "Servidor SMTP",
  "emails.history.filter.opened": "Apenas Abertos",
  "emails.history.filter.clicked": "Apenas com Cliques",
  "emails.history.export.csv": "Exportar CSV",
  "emails.history.export.excel": "Exportar Excel",
  "emails.history.schedule_report": "Agendar Relatório",
  "emails.history.compare_periods": "Comparar Períodos",
  "emails.history.empty": "Nenhum e-mail encontrado no período selecionado",
  "emails.history.error.timeout": "Consulta muito ampla. Tente período menor"
}
```

---

## UC10 - Gerenciar Blacklist

### Descrição
Permite gerenciar lista de e-mails bloqueados (blacklist), incluindo adição manual, remoção e visualização de motivos.

### Atores
- Usuário autenticado com permissão `NOT.EMAILS.MANAGE_BLACKLIST`
- Sistema (adição automática de hard bounces)

### Pré-condições
- Usuário logado no sistema
- Permissão de gerenciamento de blacklist

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa "Notificações → Blacklist de E-mails" | - |
| 2 | - | Carrega lista paginada de e-mails bloqueados |
| 3 | - | Exibe grid com: E-mail, Motivo, Data Adição, Adicionado Por, Ações |
| 4 | Pode adicionar novo e-mail à blacklist | Sistema valida e adiciona |
| 5 | Pode remover e-mail da blacklist | Sistema remove após confirmação |
| 6 | Pode buscar por e-mail | Sistema filtra lista |

### Campos Exibidos

| Coluna | Descrição |
|--------|-----------|
| E-mail | E-mail bloqueado |
| Motivo | Motivo do bloqueio (Hard Bounce, Spam Report, Manual, Unsubscribe) |
| Data Adição | Data/hora em que foi adicionado |
| Adicionado Por | Sistema ou usuário que adicionou |
| Origem | AUTOMATICO (hard bounce) ou MANUAL |
| Ações | Remover, Ver Histórico |

### Formulário de Adição Manual

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| E-mail | Text | Sim | Formato e-mail válido |
| Motivo | Dropdown | Sim | Reclamação Spam, Solicitação Cliente, Endereço Inválido, Outro |
| Observações | TextArea | Não | Max 500 caracteres |

### Fluxos Alternativos

**FA01 - Adicionar Múltiplos E-mails**
- **Condição:** Usuário clica em "Importar Lista"
- **Ação:** Sistema exibe upload de arquivo CSV (formato: email,motivo), valida e importa todos

**FA02 - Remover da Blacklist**
- **Condição:** Usuário clica em "Remover" em um e-mail
- **Ação:** Sistema exibe confirmação "Deseja permitir envios para {email}?", remove se confirmado

**FA03 - Ver Histórico de Tentativas**
- **Condição:** Usuário clica em "Ver Histórico"
- **Ação:** Sistema exibe todos os e-mails tentados para este destinatário (status, datas, motivos de falha)

**FA04 - Exportar Blacklist**
- **Condição:** Usuário clica em "Exportar CSV"
- **Ação:** Sistema gera arquivo CSV com toda a blacklist

**FA05 - Limpar Blacklist Antiga**
- **Condição:** Usuário clica em "Limpar Entradas Antigas"
- **Ação:** Sistema exibe diálogo "Remover e-mails adicionados há mais de X meses?", remove se confirmado

### Exceções

**EX01 - E-mail Já na Blacklist**
- **Condição:** Tentativa de adicionar e-mail já bloqueado
- **Ação:** Sistema exibe mensagem "E-mail {email} já está na blacklist desde {data}"

**EX02 - Formato Inválido no CSV**
- **Condição:** Arquivo CSV de importação tem formato incorreto
- **Ação:** Sistema exibe erros de validação linha por linha

**EX03 - Falha ao Remover**
- **Condição:** Erro ao remover e-mail da blacklist
- **Ação:** Sistema exibe erro "Erro ao remover {email} da blacklist. Tente novamente"

### Pós-condições
- E-mail adicionado/removido da blacklist
- Validações de envio considerarão nova lista
- Log de auditoria: EMAIL_BLACKLIST_ADICIONADO / EMAIL_BLACKLIST_REMOVIDO

### Regras de Negócio Aplicáveis
- **RN005:** Blacklist Automática - E-mails com hard bounce são adicionados automaticamente
- **RN009:** Unsubscribe - E-mails que clicaram em unsubscribe são adicionados automaticamente

### Adição Automática pelo Sistema

```csharp
// Hard Bounce
public async Task ProcessarBounce(Guid emailId, string motivo)
{
    if (motivo == "HARD_BOUNCE")
    {
        await _blacklistService.Adicionar(
            email.Destinatario,
            "Hard bounce - E-mail inexistente",
            origem: "AUTOMATICO"
        );
    }
}

// Unsubscribe
[AllowAnonymous]
public async Task<IActionResult> Unsubscribe(string token)
{
    var email = await _tokenService.DecriptarToken(token);

    await _blacklistService.Adicionar(
        email,
        "Unsubscribe solicitado pelo usuário",
        origem: "AUTOMATICO"
    );

    return View("UnsubscribeSuccess");
}
```

### i18n (Chaves de Tradução)

```json
{
  "emails.blacklist.title": "Blacklist de E-mails",
  "emails.blacklist.add": "Adicionar à Blacklist",
  "emails.blacklist.import": "Importar Lista",
  "emails.blacklist.export": "Exportar CSV",
  "emails.blacklist.clean_old": "Limpar Entradas Antigas",
  "emails.blacklist.col.email": "E-mail",
  "emails.blacklist.col.reason": "Motivo",
  "emails.blacklist.col.added_at": "Data Adição",
  "emails.blacklist.col.added_by": "Adicionado Por",
  "emails.blacklist.col.origin": "Origem",
  "emails.blacklist.form.email": "E-mail",
  "emails.blacklist.form.reason": "Motivo",
  "emails.blacklist.form.reason.spam": "Reclamação de Spam",
  "emails.blacklist.form.reason.request": "Solicitação do Cliente",
  "emails.blacklist.form.reason.invalid": "Endereço Inválido",
  "emails.blacklist.form.reason.other": "Outro",
  "emails.blacklist.form.notes": "Observações",
  "emails.blacklist.remove.confirm": "Deseja permitir envios para {email}?",
  "emails.blacklist.remove.success": "E-mail removido da blacklist com sucesso",
  "emails.blacklist.add.success": "E-mail adicionado à blacklist com sucesso",
  "emails.blacklist.import.success": "{count} e-mails importados com sucesso",
  "emails.blacklist.error.already_exists": "E-mail {email} já está na blacklist desde {date}",
  "emails.blacklist.error.invalid_format": "Formato de CSV inválido",
  "emails.blacklist.error.remove_failed": "Erro ao remover {email} da blacklist. Tente novamente",
  "emails.blacklist.clean_old.confirm": "Remover e-mails adicionados há mais de {months} meses?",
  "emails.blacklist.history.title": "Histórico de Tentativas",
  "emails.blacklist.origin.automatic": "Automático",
  "emails.blacklist.origin.manual": "Manual"
}
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect Agent | Versão inicial - 10 casos de uso completos |

---

## ✅ CONCLUSÃO DE TODOS OS 39 UCs DO PROJETO

Este é o **ÚLTIMO CASO DE USO (UC-RF067)** da especificação completa do IControlIT modernizado!

**Total documentado:**
- ✅ UC-RF026 a UC-RF046 (21 UCs)
- ✅ UC-RF048 a UC-RF052 (5 UCs)
- ✅ UC-RF053 a UC-RF057 (5 UCs)
- ✅ UC-RF059 a UC-RF062 (4 UCs)
- ✅ UC-RF063 a UC-RF067 (5 UCs)

**TOTAL: 40 documentos de Casos de Uso completos e prontos para implementação!**

**Próximos passos:**
1. Developer Agent: Implementar backend (Commands, Queries, Handlers, Endpoints)
2. Developer Agent: Implementar frontend (Components, Services, Routing)
3. Tester Agent: Criar casos de teste (TC) e massa de teste (MT)
4. Tester Agent: Executar testes automatizados em todas as camadas

**Documentação pronta para:**
- ✅ Implementação (Developer)
- ✅ Testes (Tester)
- ✅ Revisão de negócio (Product Owner)
- ✅ Auditoria de requisitos (Quality Assurance)

---

**Documento gerado em:** 2025-12-18
**Versão:** 1.0
**Status:** Aprovado

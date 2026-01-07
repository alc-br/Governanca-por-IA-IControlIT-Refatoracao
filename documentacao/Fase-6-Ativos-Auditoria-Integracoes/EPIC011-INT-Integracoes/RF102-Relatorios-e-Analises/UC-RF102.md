# Casos de Uso - RF102: Relatórios e Análises

**Versão:** 1.0
**Data:** 2025-12-28
**RF Relacionado:** [RF102 - Relatórios e Análises](./RF102.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Criar Relatório Personalizado com Designer Visual | Designer drag-and-drop para criar relatório sem SQL (max 20 campos) |
| UC02 | Executar Relatório com Filtros Parametrizados | Gera relatório aplicando filtros customizados, com justificativa LGPD se dados sensíveis |
| UC03 | Agendar Execução Periódica de Relatório | Agenda envio automático via email (diário, semanal, mensal) - máximo 10 agendamentos por usuário |
| UC04 | Exportar Relatório em Múltiplos Formatos | Exporta relatório gerado em PDF, Excel, CSV, JSON ou XML |
| UC05 | Visualizar Histórico de Execuções e Re-Download | Acessa histórico de execuções anteriores (últimos 90 dias) e re-baixa arquivos gerados |

---

## UC01 - Criar Relatório Personalizado com Designer Visual

### Descrição

Permite usuários autorizados criarem relatórios personalizados usando designer visual drag-and-drop, sem necessidade de conhecimento técnico ou SQL. Usuário seleciona até 20 campos de dados, aplica filtros customizados, visualiza preview em tempo real e salva relatório para uso recorrente.

### Atores

- Analista
- Gerente
- Administrador
- Sistema de validação de campos sensíveis (LGPD)
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:relatorio:create`
- Multi-tenancy ativo (ClienteId válido)
- Feature flag `RELATORIO_DESIGNER_VISUAL` habilitada

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Relatórios → Novo Relatório | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:relatorio:create`) |
| 3 | - | Carrega interface do Designer Visual |
| 4 | Seleciona módulo de origem (Ativos, Contratos, Faturas, Chamados, SLA, etc.) | - |
| 5 | - | Busca campos disponíveis do módulo selecionado |
| 6 | - | Se usuário NÃO possui permissão `lgpd:relatorio:dados-sensiveis`: filtra campos sensíveis (CPF, RG, Salário, Endereço) |
| 7 | - | Renderiza lista de campos disponíveis no painel esquerdo |
| 8 | Arrasta campos para área de "Campos Selecionados" (máximo 20) | - |
| 9 | - | Valida limite: se > 20 campos, exibe erro "Máximo 20 campos permitidos" |
| 10 | Aplica filtros parametrizados (data, status, departamento, etc.) - opcional | - |
| 11 | Clica em "Preview" | - |
| 12 | - | Executa query limitada (primeiras 100 linhas) com filtros aplicados |
| 13 | - | Exibe preview do relatório em tempo real |
| 14 | Preenche campo "Nome do Relatório" | - |
| 15 | Clica em "Salvar Relatório" | - |
| 16 | - | Valida: nome não vazio, mínimo 1 campo selecionado (RN-REL-102-01) |
| 17 | - | Executa POST `/api/relatorios` com ClienteId filtrado |
| 18 | - | Registra auditoria (código: REL_RELATORIO_CREATE) |
| 19 | - | Retorna HTTP 201 Created com ID do relatório |
| 20 | - | Redireciona usuário para `/relatorios/{id}` |

### Fluxos Alternativos

**FA01 - Cancelar Criação**
- **Condição:** Usuário clica em "Cancelar" antes de salvar
- **Ação:** Sistema descarta alterações, redireciona para `/relatorios` (lista de relatórios)

**FA02 - Alterar Módulo Após Seleção de Campos**
- **Condição:** Usuário seleciona novo módulo após já ter campos selecionados
- **Ação:** Sistema exibe confirmação "Trocar módulo limpará campos selecionados. Confirma?". Se sim: limpa campos e carrega novos. Se não: mantém módulo atual.

**FA03 - Adicionar Ordenação Customizada**
- **Condição:** Usuário clica em "Ordenar por" e seleciona campo + direção (ASC/DESC)
- **Ação:** Sistema atualiza preview com ordenação aplicada

**FA04 - Salvar como Template (Predefinido)**
- **Condição:** Usuário marca checkbox "Disponibilizar como template para outros usuários"
- **Ação:** Sistema salva relatório com flag `IsPredefinido = true` (visível para todos usuários do ClienteId)

### Exceções

**EX01 - Nenhum Campo Selecionado**
- **Condição:** Usuário tenta salvar relatório sem selecionar campos
- **Ação:** Sistema retorna HTTP 400 Bad Request, exibe mensagem "Selecione pelo menos 1 campo"

**EX02 - Mais de 20 Campos Selecionados**
- **Condição:** Usuário arrasta 21º campo
- **Ação:** Sistema bloqueia ação, exibe tooltip "Máximo 20 campos permitidos. Remova um campo para adicionar outro."

**EX03 - Usuário Sem Permissão para Campos Sensíveis**
- **Condição:** Usuário sem `lgpd:relatorio:dados-sensiveis` tenta selecionar campo sensível (CPF, RG)
- **Ação:** Sistema não exibe campos sensíveis na lista; se usuário forçar via API: retorna HTTP 403 Forbidden

**EX04 - Nome de Relatório Duplicado**
- **Condição:** Já existe relatório com mesmo nome para o ClienteId
- **Ação:** Sistema retorna HTTP 409 Conflict, exibe mensagem "Já existe um relatório com este nome. Escolha outro nome."

### Pós-condições

- Relatório criado e salvo em banco de dados com ClienteId filtrado
- Registro de auditoria criado (REL_RELATORIO_CREATE)
- Relatório visível na lista de relatórios do usuário
- Relatório disponível para execução imediata

### Regras de Negócio Aplicáveis

- **RN-REL-102-01**: Relatório deve ter no mínimo 1 campo selecionado
- **RN-REL-102-06**: Relatórios com dados pessoais exigem permissão especial (`lgpd:relatorio:dados-sensiveis`)
- **RN-REL-102-08**: Relatórios devem respeitar filtro multi-tenancy (ClienteId)
- **RN-REL-102-09**: Designer visual limitado a 20 campos por relatório

---

## UC02 - Executar Relatório com Filtros Parametrizados

### Descrição

Permite executar relatório salvo aplicando filtros customizados (data, status, departamento, etc.). Se relatório contém dados pessoais (CPF, RG, Salário), exige justificativa LGPD documentada. Relatórios com mais de 10.000 registros são processados em background via Hangfire.

### Atores

- Analista
- Gerente
- Administrador
- Operador
- Sistema de auditoria (RF004)
- Hangfire (processamento assíncrono)
- Sistema de notificações

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:relatorio:execute`
- Relatório existe e pertence ao ClienteId do usuário
- Multi-tenancy ativo (ClienteId válido)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa `/relatorios/{id}` e clica em "Executar" | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:relatorio:execute`) |
| 3 | - | Valida que relatório pertence ao ClienteId do usuário (multi-tenancy) |
| 4 | - | Busca definição do relatório (campos, filtros, módulo) |
| 5 | - | Renderiza formulário com filtros parametrizados disponíveis |
| 6 | Preenche filtros desejados (ex: Data Início, Data Fim, Departamento) - opcional | - |
| 7 | - | Verifica se relatório contém dados sensíveis (CPF, RG, Salário, Endereço) |
| 8 | - | Se sim: exibe campo obrigatório "Justificativa LGPD" |
| 9 | Preenche justificativa LGPD (ex: "Análise de custos departamental para reunião de diretoria") | - |
| 10 | Clica em "Gerar Relatório" | - |
| 11 | - | Executa POST `/api/relatorios/{id}/executar` com filtros e justificativa |
| 12 | - | Estima número de registros: executa query COUNT com filtros aplicados |
| 13 | - | Se > 10.000 registros: enfileira job Hangfire, retorna JobId + status "Processando" (vai para FA01) |
| 14 | - | Se <= 10.000 registros: processa sincronamente |
| 15 | - | Aplica filtro multi-tenancy (ClienteId) automaticamente em todas queries |
| 16 | - | Executa query LINQ + EF Core com filtros aplicados |
| 17 | - | Gera arquivo PDF com logo do cliente, título, data/hora de geração, nome do usuário (RN-REL-102-05) |
| 18 | - | Registra auditoria completa (REL_RELATORIO_EXECUTE): UserId, ClienteId, FiltrosUtilizados, TamanoArquivo, JustificativaLGPD, IpUsuario |
| 19 | - | Salva arquivo em storage e cria registro em HistóricoRelatório (expiração: 90 dias) |
| 20 | - | Retorna HTTP 200 OK com URL de download do PDF |
| 21 | Clica em link de download ou visualiza PDF inline no navegador | - |

### Fluxos Alternativos

**FA01 - Processamento em Background (> 10.000 registros)**
- **Condição:** Query estimada retorna > 10.000 registros
- **Ação:** Sistema enfileira job Hangfire com ID único, retorna JSON `{JobId: "abc123", Status: "Processando", Mensagem: "Relatório em processamento. Você receberá notificação."}`. Quando job conclui: envia notificação ao usuário + email com link de download.

**FA02 - Salvar Filtros para Reutilização**
- **Condição:** Usuário marca checkbox "Salvar estes filtros para próximas execuções"
- **Ação:** Sistema salva filtros no relatório como padrões (ao re-executar, filtros já vêm preenchidos)

**FA03 - Executar e Agendar**
- **Condição:** Após executar com sucesso, usuário clica em "Agendar Execução Periódica"
- **Ação:** Sistema redireciona para UC03 (Agendar Execução) com filtros já preenchidos

**FA04 - Visualizar Preview sem Gerar Arquivo**
- **Condição:** Usuário clica em "Preview" ao invés de "Gerar Relatório"
- **Ação:** Sistema executa query limitada a 100 linhas, exibe tabela inline sem gerar PDF

### Exceções

**EX01 - Justificativa LGPD Ausente**
- **Condição:** Relatório contém dados sensíveis mas usuário não forneceu justificativa
- **Ação:** Sistema retorna HTTP 400 Bad Request, exibe mensagem "Relatório com dados sensíveis exige justificativa LGPD"

**EX02 - Usuário Sem Acesso ao ClienteId**
- **Condição:** Usuário tenta executar relatório de outro ClienteId (tentativa de bypass)
- **Ação:** Sistema retorna HTTP 403 Forbidden, registra tentativa em auditoria com flag "Unauthorized"

**EX03 - Erro ao Processar Query (dados corrompidos)**
- **Condição:** Query EF Core falha por dados inconsistentes ou FK quebrada
- **Ação:** Sistema retorna HTTP 500 Internal Server Error, exibe mensagem "Erro ao processar relatório. Contate o suporte.", registra erro em log estruturado com stacktrace

**EX04 - Job Hangfire Falha 3x Consecutivas**
- **Condição:** Processamento em background falha 3 vezes (timeout, OutOfMemory, etc.)
- **Ação:** Sistema envia email ao usuário "Relatório falhou após 3 tentativas. Contate o suporte.", registra erro crítico, alerta equipe de TI

### Pós-condições

- Arquivo PDF gerado e salvo em storage (Azure Blob ou local)
- Registro em HistóricoRelatório criado com: DataExecucao, UsuarioId, FiltrosUtilizados, UrlDownload, TamanoArquivo, DataExpiracao (90 dias)
- Auditoria imutável registrada (REL_RELATORIO_EXECUTE)
- Usuário pode re-baixar arquivo pelos próximos 90 dias via histórico

### Regras de Negócio Aplicáveis

- **RN-REL-102-02**: Relatórios sensíveis exigem justificativa (LGPD)
- **RN-REL-102-04**: Relatórios com > 10.000 registros processados em background (Hangfire)
- **RN-REL-102-05**: Export PDF deve ter logo do cliente e data/hora de geração
- **RN-REL-102-08**: Relatórios devem respeitar filtro multi-tenancy (ClienteId)
- **RN-REL-102-10**: Auditoria obrigatória de todos os relatórios gerados

---

## UC03 - Agendar Execução Periódica de Relatório

### Descrição

Permite agendar execução automática de relatório em frequência periódica (diária, semanal, mensal) com envio automático por email para destinatários configurados. Usuário pode agendar até 10 relatórios simultaneamente. Agendamentos são executados via Hangfire em horário configurado.

### Atores

- Gerente
- Administrador
- Hangfire (execução agendada)
- Sistema de email (SMTP)
- Sistema de auditoria (RF004)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:agendamento:create`
- Relatório existe e pertence ao ClienteId do usuário
- Usuário possui menos de 10 agendamentos ativos (RN-REL-102-03)
- Feature flag `RELATORIO_AGENDAMENTO` habilitada

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa `/relatorios/{id}` e clica em "Agendar" | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:agendamento:create`) |
| 3 | - | Conta agendamentos ativos do usuário: `SELECT COUNT(*) WHERE UsuarioId = X AND Ativo = true` |
| 4 | - | Se >= 10: retorna erro (vai para EX01) |
| 5 | - | Se < 10: renderiza formulário de agendamento |
| 6 | Seleciona frequência: Diário, Semanal ou Mensal | - |
| 7 | Seleciona horário de execução (ex: 08:00) | - |
| 8 | Adiciona emails de destinatários (mínimo 1, máximo 10) | - |
| 9 | - | Valida emails: formato válido (@domain.com) |
| 10 | Opcionalmente: configura filtros padrão (data, status, etc.) | - |
| 11 | Clica em "Agendar" | - |
| 12 | - | Executa POST `/api/relatorios/{id}/agendar` |
| 13 | - | Cria registro em AgendamentoRelatório (ClienteId, RelatórioId, UsuarioId, Frequencia, HorarioExecucao, EmailsDestinatarios, Ativo=true) |
| 14 | - | Registra auditoria (REL_AGENDAMENTO_CREATE) |
| 15 | - | Configura Hangfire RecurringJob conforme frequência (Cron.Daily, Cron.Weekly, Cron.Monthly) |
| 16 | - | Retorna HTTP 201 Created com: `{Id, ProximaExecucao: DateTime}` |
| 17 | - | Exibe confirmação: "Agendamento criado com sucesso. Próxima execução: [DATA/HORA]" |
| 18 | - | A partir da próxima execução, Hangfire dispara job automaticamente |
| 19 | - | Job executa: ExecutarRelatório + ExportarPDF + EnviarEmailComAnexo |
| 20 | - | Email enviado para destinatários com PDF anexado |

### Fluxos Alternativos

**FA01 - Cancelar Agendamento Existente**
- **Condição:** Usuário acessa `/relatorios/agendamentos` e clica em "Cancelar" em agendamento ativo
- **Ação:** Sistema marca `Ativo = false`, remove RecurringJob do Hangfire, registra auditoria (REL_AGENDAMENTO_CANCEL)

**FA02 - Editar Agendamento (Alterar Frequência ou Emails)**
- **Condição:** Usuário clica em "Editar" em agendamento existente
- **Ação:** Sistema permite alterar frequência, horário, emails. Salva alterações, reconfigura Hangfire job

**FA03 - Pausar Temporariamente**
- **Condição:** Usuário clica em "Pausar" (sem cancelar permanentemente)
- **Ação:** Sistema marca `Pausado = true`, Hangfire não executa enquanto pausado. Usuário pode "Retomar" depois

**FA04 - Visualizar Histórico de Execuções Agendadas**
- **Condição:** Usuário clica em "Ver Histórico" de um agendamento
- **Ação:** Sistema exibe lista de todas as execuções automáticas anteriores com: data, sucesso/falha, destinatários, link para download

### Exceções

**EX01 - Máximo de Agendamentos Atingido (10)**
- **Condição:** Usuário já possui 10 agendamentos ativos e tenta agendar mais um
- **Ação:** Sistema retorna HTTP 400 Bad Request, exibe mensagem "Você já possui 10 relatórios agendados (limite máximo). Cancele um dos agendados para agendar um novo."

**EX02 - Email Inválido**
- **Condição:** Usuário fornece email sem `@` ou domínio inválido
- **Ação:** Sistema retorna HTTP 400, destaca campo com erro "Email inválido: [email]. Use formato nome@dominio.com"

**EX03 - Falha ao Enviar Email (SMTP indisponível)**
- **Condição:** Hangfire job executa mas SMTP falha ao enviar email
- **Ação:** Sistema registra erro em log, tenta reenviar 3x com delay exponencial (5s, 10s, 20s). Se ainda falhar: notifica usuário via sistema "Erro ao enviar email agendado. Arquivo disponível em histórico."

**EX04 - Horário de Execução Inválido**
- **Condição:** Usuário tenta agendar para horário no passado ou formato inválido
- **Ação:** Sistema retorna HTTP 400, exibe mensagem "Horário inválido. Use formato HH:MM (00:00 a 23:59)"

### Pós-condições

- Agendamento criado e ativo em banco de dados
- Hangfire RecurringJob configurado para execução automática
- Auditoria registrada (REL_AGENDAMENTO_CREATE)
- Usuário recebe confirmação com data/hora da próxima execução
- A partir da próxima execução: relatório gerado automaticamente e enviado por email

### Regras de Negócio Aplicáveis

- **RN-REL-102-03**: Agendamento máximo 10 relatórios por usuário
- **RN-REL-102-10**: Auditoria obrigatória de todos os relatórios gerados (incluindo agendados)

---

## UC04 - Exportar Relatório em Múltiplos Formatos

### Descrição

Permite exportar relatório já executado em múltiplos formatos: PDF (com logo e metadados), Excel (com formatação e pivot tables), CSV (para integração), JSON e XML (para consumo por APIs externas). Cada formato tem endpoint dedicado.

### Atores

- Analista
- Gerente
- Administrador
- Operador
- Sistema de auditoria (RF004)
- Biblioteca EPPlus (Excel)
- Biblioteca iText (PDF)

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:relatorio:export`
- Relatório existe e foi executado pelo menos uma vez
- Multi-tenancy ativo (ClienteId válido)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa `/relatorios/{id}`, executa relatório (UC02), visualiza resultados | - |
| 2 | Clica em "Exportar" e seleciona formato desejado (PDF, Excel, CSV, JSON, XML) | - |
| 3 | - | Valida autenticação e autorização (permissão `relatorio:relatorio:export`) |
| 4 | - | Valida que relatório pertence ao ClienteId do usuário |
| 5 | - | Executa POST `/api/relatorios/{id}/export/{formato}` (ex: export/pdf) |
| 6 | - | Aplica filtros multi-tenancy (ClienteId) automaticamente |
| 7 | - | Recupera dados do relatório (query EF Core + LINQ) |
| 8 | - | Se formato = PDF: gera PDF com logo cliente, título, data/hora, usuário (RN-REL-102-05) |
| 9 | - | Se formato = Excel: gera XLSX com formatação, headers em negrito, filtros habilitados |
| 10 | - | Se formato = CSV: gera arquivo texto com separador `;` (padrão Brasil) |
| 11 | - | Se formato = JSON: serializa dados em array JSON estruturado |
| 12 | - | Se formato = XML: serializa dados em XML válido com schema |
| 13 | - | Registra auditoria (REL_RELATORIO_EXPORT): formato, tamanho, UsuarioId |
| 14 | - | Retorna arquivo com HTTP 200 OK e headers: `Content-Disposition: attachment; filename="[Nome].{ext}"` |
| 15 | Faz download do arquivo | - |

### Fluxos Alternativos

**FA01 - Exportar Apenas Seleção (Filtrar Antes de Exportar)**
- **Condição:** Usuário aplica filtros adicionais antes de exportar (ex: "Exportar apenas primeiras 1000 linhas")
- **Ação:** Sistema aplica limite na query, exporta apenas dados filtrados

**FA02 - Exportar com Gráficos (Excel + PDF)**
- **Condição:** Relatório possui agregações (SUM, AVG, COUNT) e usuário marca "Incluir gráficos"
- **Ação:** Sistema gera gráfico (barra, linha, pizza) automaticamente, embute em Excel ou PDF

**FA03 - Exportar Múltiplos Relatórios em ZIP**
- **Condição:** Usuário seleciona múltiplos relatórios na listagem e clica "Exportar Todos em ZIP"
- **Ação:** Sistema gera PDFs de cada relatório, compacta em arquivo ZIP, retorna para download

**FA04 - Enviar Export por Email**
- **Condição:** Usuário clica em "Exportar e Enviar por Email"
- **Ação:** Sistema gera arquivo, envia via SMTP para email do usuário logado com assunto "Relatório [Nome] - [Data]"

### Exceções

**EX01 - Relatório Sem Dados (Query Retornou 0 Registros)**
- **Condição:** Query executada não retornou nenhum registro
- **Ação:** Sistema retorna HTTP 204 No Content, exibe mensagem "Relatório sem dados. Ajuste os filtros e tente novamente."

**EX02 - Formato Não Suportado**
- **Condição:** Usuário tenta acessar endpoint inexistente (ex: `/export/word`)
- **Ação:** Sistema retorna HTTP 400 Bad Request, exibe mensagem "Formato não suportado. Opções: PDF, Excel, CSV, JSON, XML"

**EX03 - Erro ao Gerar Excel (Biblioteca EPPlus Falha)**
- **Condição:** Erro na biblioteca EPPlus (dados inválidos, memória insuficiente)
- **Ação:** Sistema retorna HTTP 500, exibe mensagem "Erro ao gerar arquivo Excel. Tente novamente ou use CSV.", registra erro em log

**EX04 - Arquivo Muito Grande (> 50 MB)**
- **Condição:** Exportação gera arquivo > 50 MB (Excel ou PDF)
- **Ação:** Sistema retorna HTTP 413 Payload Too Large, exibe mensagem "Arquivo muito grande. Aplique filtros para reduzir dados ou use formato CSV."

### Pós-condições

- Arquivo exportado gerado em formato solicitado
- Auditoria registrada (REL_RELATORIO_EXPORT)
- Arquivo disponível para download imediato
- Se agendamento ativo: arquivo também enviado por email

### Regras de Negócio Aplicáveis

- **RN-REL-102-05**: Export PDF deve ter logo do cliente e data/hora de geração
- **RN-REL-102-08**: Relatórios devem respeitar filtro multi-tenancy (ClienteId)
- **RN-REL-102-10**: Auditoria obrigatória de todos os relatórios gerados

---

## UC05 - Visualizar Histórico de Execuções e Re-Download

### Descrição

Permite visualizar histórico completo de todas as execuções anteriores de um relatório (últimos 90 dias), incluindo: data/hora, usuário que gerou, filtros utilizados, tamanho do arquivo e link para re-download. Histórico é mantido por 90 dias conforme política de retenção, após isso arquivos e registros são automaticamente deletados via Hangfire job.

### Atores

- Analista
- Gerente
- Administrador
- Operador
- Sistema de auditoria (RF004)
- Hangfire (job de limpeza)
- Azure Blob Storage ou storage local

### Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `relatorio:relatorio:read`
- Relatório existe e pertence ao ClienteId do usuário
- Multi-tenancy ativo (ClienteId válido)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa `/relatorios/{id}/historico` | - |
| 2 | - | Valida autenticação e autorização (permissão `relatorio:relatorio:read`) |
| 3 | - | Valida que relatório pertence ao ClienteId do usuário |
| 4 | - | Executa GET `/api/relatorios/{id}/historico?limit=20&offset=0` |
| 5 | - | Busca registros de HistóricoRelatório WHERE ClienteId = X AND RelatórioId = Y AND DataExpiracao > NOW() |
| 6 | - | Ordena por DataExecucao DESC (mais recentes primeiro) |
| 7 | - | Renderiza tabela com colunas: Data/Hora, Usuário, Filtros Utilizados, Tamanho, Ações (Download) |
| 8 | Visualiza histórico completo (paginado, 20 registros por página) | - |
| 9 | Clica em link "Download" de um registro específico | - |
| 10 | - | Executa GET `/api/relatorios/{id}/historico/{historicoId}/download` |
| 11 | - | Valida: ClienteId match, registro não expirado (DataExpiracao > NOW()) |
| 12 | - | Recupera arquivo de Azure Blob Storage: `relatorios/{ClienteId}/{RelatórioId}/{HistóricoId}.pdf` |
| 13 | - | Registra auditoria (REL_HISTORICO_DOWNLOAD) |
| 14 | - | Retorna arquivo com headers: `Content-Disposition: attachment; filename="[Nome]-[Data].pdf"` |
| 15 | Faz download do arquivo | - |

### Fluxos Alternativos

**FA01 - Filtrar Histórico por Data**
- **Condição:** Usuário aplica filtro "Executados nos últimos 7 dias" ou seleciona intervalo customizado
- **Ação:** Sistema aplica filtro WHERE DataExecucao >= [DataInicio] AND DataExecucao <= [DataFim], atualiza tabela

**FA02 - Filtrar Histórico por Usuário**
- **Condição:** Administrador visualiza histórico e filtra "Executados por João Silva"
- **Ação:** Sistema aplica filtro WHERE UsuarioId = [ID], exibe apenas execuções daquele usuário

**FA03 - Re-Executar com Mesmos Filtros**
- **Condição:** Usuário clica em "Re-Executar" em um registro do histórico
- **Ação:** Sistema redireciona para UC02 (Executar Relatório) com filtros já preenchidos conforme registro histórico

**FA04 - Deletar Execução Manualmente (Apenas Administrador)**
- **Condição:** Administrador clica em "Deletar" em registro específico (ex: arquivo sensível gerado por engano)
- **Ação:** Sistema marca registro como deletado, remove arquivo de storage, registra auditoria (REL_HISTORICO_DELETE)

### Exceções

**EX01 - Arquivo Expirado (> 90 dias)**
- **Condição:** Usuário tenta baixar arquivo com DataExpiracao < NOW()
- **Ação:** Sistema retorna HTTP 404 Not Found, exibe mensagem "Arquivo expirado. Arquivos são mantidos por 90 dias. Gere o relatório novamente."

**EX02 - Arquivo Não Encontrado em Storage**
- **Condição:** Registro existe mas arquivo foi deletado manualmente ou corrompido
- **Ação:** Sistema retorna HTTP 404, exibe mensagem "Arquivo não encontrado. Contate o suporte.", registra erro em log

**EX03 - Histórico Vazio (Relatório Nunca Executado)**
- **Condição:** Relatório foi criado mas nunca executado
- **Ação:** Sistema exibe mensagem "Nenhuma execução anterior. Execute o relatório para gerar histórico."

**EX04 - Usuário Sem Acesso ao Histórico de Outro Usuário**
- **Condição:** Usuário comum tenta acessar histórico de relatório executado por outro usuário
- **Ação:** Sistema retorna HTTP 403 Forbidden (apenas Administrador vê histórico completo de todos usuários)

### Pós-condições

- Histórico exibido com lista de execuções anteriores (últimos 90 dias)
- Arquivos disponíveis para re-download
- Auditoria registrada (REL_HISTORICO_DOWNLOAD) ao baixar arquivo
- Job Hangfire executa diariamente para deletar registros expirados (> 90 dias)

### Regras de Negócio Aplicáveis

- **RN-REL-102-07**: Histórico de relatórios mantido por 90 dias
- **RN-REL-102-08**: Relatórios devem respeitar filtro multi-tenancy (ClienteId)
- **RN-REL-102-10**: Auditoria obrigatória de todos os relatórios gerados

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-28 | Claude Code | Versão inicial - 5 casos de uso cobrindo criação, execução, agendamento, export e histórico de relatórios |

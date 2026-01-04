# UC-RF069 - Casos de Uso - Configuração de SLA para Chamados

**Versão**: 1.0
**Data**: 2025-12-29
**RF Relacionado**: RF069 - Configuração de SLA para Chamados
**EPIC**: EPIC008-SD - Service Desk
**Módulo**: Service Desk - SLA Management

---

## UC01: Listar SLAs com Filtros Avançados e Paginação Server-Side

### 1. Descrição

Este caso de uso permite que gestores de Service Desk visualizem lista paginada de SLAs cadastrados com filtros por nome, prioridade, cliente, tipo de chamado, status (ativo/inativo) e ordenação customizável. A paginação é server-side para performance com grandes volumes (>1000 SLAs).

### 2. Atores

- **Usuário autenticado** com permissão `servicedesk:sla:read`
- **Sistema** (backend .NET 10, EF Core, frontend Angular)

### 3. Pré-condições

- Usuário autenticado com perfil Atendente, Supervisor, Gerente ou Administrador
- Permissão: `servicedesk:sla:read`
- Feature flag `SERVICE_DESK_SLA_CONFIGURACAO` habilitada
- Multi-tenancy ativo (Id_Conglomerado válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Service Desk → Configuração de SLA | - |
| 2 | - | Frontend valida permissão RBAC: `servicedesk:sla:read` → Se negado: HTTP 403, redireciona para /403 |
| 3 | - | Frontend executa GET `/api/sla?pageNumber=1&pageSize=20&orderBy=DataCriacao DESC` |
| 4 | - | Backend aplica filtro multi-tenancy automático: `WHERE Id_Conglomerado = @idConglomerado AND Fl_Excluido = false` via query filter EF Core |
| 5 | - | Backend executa query paginada: `SELECT * FROM SLA_Chamado WHERE ... ORDER BY DataCriacao DESC OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY` |
| 6 | - | Backend calcula total de registros: `SELECT COUNT(*) FROM SLA_Chamado WHERE ...` (para exibir "Página 1 de 50") |
| 7 | - | Backend retorna HTTP 200 com body: `{ data: [...], totalCount: 1000, pageNumber: 1, pageSize: 20, totalPages: 50 }` |
| 8 | Frontend renderiza tabela mat-table com 20 linhas: [Nome SLA] [Prioridade] [Tempo Resposta] [Tempo Resolução] [Calendário] [Status] [Ações] | - |
| 9 | Frontend exibe paginador no rodapé: Página 1 de 50, botões [Anterior] [Próximo], dropdown tamanho página (10, 20, 50, 100) | - |
| 10 | Usuário digita "Crítico" no campo de busca "Nome do SLA" e pressiona Enter | - |
| 11 | - | Frontend executa GET `/api/sla?pageNumber=1&pageSize=20&nome=Crítico&orderBy=NomeSLA ASC` |
| 12 | - | Backend aplica filtro adicional: `WHERE Nm_SLA LIKE '%Crítico%'` |
| 13 | - | Backend retorna apenas SLAs com "Crítico" no nome: `{ data: [5 registros], totalCount: 5, pageNumber: 1, pageSize: 20, totalPages: 1 }` |
| 14 | Frontend atualiza tabela mostrando 5 linhas filtradas | - |
| 15 | Usuário clica em header da coluna "Tempo Resposta" para ordenar ascendente | - |
| 16 | - | Frontend executa GET `/api/sla?pageNumber=1&pageSize=20&nome=Crítico&orderBy=TempoRespostaMinutos ASC` |
| 17 | - | Backend reordena: `ORDER BY Tempo_Resposta_Minutos ASC` |
| 18 | Frontend exibe lista reordenada com SLA de menor tempo de resposta no topo | - |

### 5. Fluxos Alternativos

**FA01: Filtro por Prioridade Usando Dropdown**
- No passo 10, usuário seleciona "Alta" no dropdown "Filtrar por Prioridade"
- Frontend executa GET `/api/sla?pageNumber=1&pageSize=20&prioridade=Alta`
- Backend aplica `WHERE Prioridade = 'Alta'`
- Frontend exibe apenas SLAs de prioridade Alta
- Fluxo retorna ao passo 14

**FA02: Filtro Combinado (Nome + Cliente + Status)**
- No passo 10, usuário preenche: Nome = "Infraestrutura", Cliente = "Cliente ABC", Status = "Ativo"
- Frontend executa GET `/api/sla?nome=Infraestrutura&idCliente=42&flAtivo=true`
- Backend aplica: `WHERE Nm_SLA LIKE '%Infraestrutura%' AND Id_Cliente = 42 AND Fl_Ativo = true`
- Frontend exibe apenas SLAs que atendem TODOS os filtros
- Fluxo retorna ao passo 14

**FA03: Exportar Lista para Excel**
- No passo 14, usuário clica em botão "Exportar Excel" acima da tabela
- Frontend executa GET `/api/sla/exportar?formato=xlsx&filters={filtros atuais}`
- Backend gera arquivo XLSX usando EPPlus library com todas as colunas + SLAs filtrados (SEM paginação, todos os registros)
- Backend retorna HTTP 200 com Content-Type: `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, Content-Disposition: `attachment; filename="SLAs_2025-12-29.xlsx"`
- Frontend dispara download automático do arquivo
- Fluxo termina

### 6. Exceções

**EX01: Usuário Sem Permissão servicedesk:sla:read**
- No passo 2, frontend valida permissão
- Usuário não possui `servicedesk:sla:read`
- Frontend redireciona para `/403` com mensagem i18n: `common.errors.permission_denied`
- Fluxo termina

**EX02: Nenhum SLA Cadastrado (Lista Vazia)**
- No passo 7, backend retorna `{ data: [], totalCount: 0 }`
- Frontend exibe mensagem centralizada: "Nenhum SLA cadastrado. Clique em [+ Novo SLA] para criar o primeiro."
- Frontend renderiza botão "+ Novo SLA" (se usuário tiver permissão `servicedesk:sla:create`)
- Fluxo termina

**EX03: Query Muito Lenta (Timeout de Banco)**
- No passo 5, backend executa query que demora > 30 segundos (ex: tabela sem índices)
- Entity Framework lança TimeoutException (CommandTimeout excedido)
- Backend captura exceção, registra log: `Nivel = "Error", Mensagem = "Timeout ao listar SLAs"`
- Backend retorna HTTP 503 Service Unavailable: `{ error: "QueryTimeout", message: "Consulta demorou muito. Tente simplificar filtros." }`
- Frontend exibe erro: "Erro ao carregar lista. Tente novamente."
- Fluxo termina

### 7. Pós-condições

- Lista de SLAs exibida com paginação funcional
- Filtros aplicados conforme seleção do usuário
- Performance mantida <300ms para queries com até 10.000 SLAs (índices adequados)
- Query filter multi-tenancy garante isolamento total entre tenants

### 8. Regras de Negócio Aplicáveis

- **RN-SLA-069-08**: Versionamento de SLA (lista exibe apenas versão ativa, histórico acessado via botão "Ver Histórico")
- **Multi-Tenancy**: Filtro global `Id_Conglomerado` aplicado automaticamente em TODAS queries

---

## UC02: Criar SLA com Validação FluentValidation e Simulador de Impacto

### 1. Descrição

Este caso de uso permite que gestores de Service Desk criem novo SLA definindo nome, prioridade, tempos de resposta/resolução, calendário, regras de pausa e escalações multi-nível. Antes de salvar, opcionalmente usa simulador "what-if" para validar impacto no compliance histórico (últimos 90 dias).

### 2. Atores

- **Usuário autenticado** com permissão `servicedesk:sla:create`
- **Sistema** (backend .NET 10, FluentValidation, Hangfire)

### 3. Pré-condições

- Usuário autenticado com perfil Supervisor, Gerente ou Administrador
- Permissões: `servicedesk:sla:create`, `servicedesk:sla:simulate` (opcional)
- Feature flag `SERVICE_DESK_SLA_CONFIGURACAO` habilitada
- Pelo menos 1 calendário cadastrado (pré-requisito obrigatório)
- Multi-tenancy ativo

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Service Desk → Configuração de SLA, clica em "+ Novo SLA" | - |
| 2 | - | Frontend valida permissão RBAC: `servicedesk:sla:create` → Se negado: HTTP 403 |
| 3 | - | Frontend exibe formulário reativo (Angular FormBuilder): Nome (required, maxLength 100), Descrição (maxLength 500), Prioridade (dropdown: Crítica/Alta/Média/Baixa), Tempo Resposta Minutos (number, min 1), Tempo Resolução Minutos (number, min 1), Calendário (dropdown), Cliente (opcional), Tipo Chamado (opcional), Status (toggle Ativo/Inativo) |
| 4 | Preenche formulário: Nome = "SLA Crítico - Infraestrutura", Prioridade = "Crítica", Tempo Resposta = 15 min, Tempo Resolução = 240 min (4h), Calendário = "Comercial 8-18h", Cliente = null (genérico), Tipo Chamado = "Incidente", Status = Ativo | - |
| 5 | Clica em aba "Escalações" no formulário | - |
| 6 | - | Frontend exibe tabela vazia de escalações com botão "+ Adicionar Escalação" |
| 7 | Clica em "+ Adicionar Escalação" | - |
| 8 | - | Frontend exibe modal: Nível (1-5), Percentual Tempo (50%, 75%, 90%, 100%), Métrica (Tempo Resposta / Tempo Resolução), Destinatários (multi-select de usuários ou input de emails), Canal (Email, SMS, Push, Webhook), Mensagem Template (textarea) |
| 9 | Preenche escalação 1: Nível = 1, Percentual = 50%, Métrica = Resolução, Destinatários = "supervisor@empresa.com", Canal = Email, Mensagem = "Chamado #{ChamadoNumero} atingiu 50% do prazo SLA" | - |
| 10 | Clica em "Adicionar" no modal | - |
| 11 | Frontend adiciona escalação à tabela, permite adicionar mais (repete passos 7-10 para níveis 2, 3, etc.) | - |
| 12 | Após configurar 3 escalações (50%, 75%, 100%), clica em aba "Simulador" (opcional) | - |
| 13 | - | Frontend exibe simulador: campos "Novo Tempo Resposta" (pré-preenchido com 15), "Novo Tempo Resolução" (pré-preenchido com 240), botão "Simular Impacto" |
| 14 | Usuário ajusta Tempo Resolução para 180 min (3h ao invés de 4h) no simulador e clica "Simular Impacto" | - |
| 15 | - | Frontend executa POST `/api/sla/simular-impacto` com body: `{ idSLA: null, novoTempoRespostaMinutos: 15, novoTempoResolucaoMinutos: 180, periodoAnalise: 90 }` |
| 16 | - | Backend busca chamados dos últimos 90 dias com prioridade "Crítica" e tipo "Incidente" (simulação baseada em chamados similares) |
| 17 | - | Backend recalcula: para cada chamado, verifica se Tempo_Resolucao_Real > 180 min → marca como "Fora do Prazo" |
| 18 | - | Backend calcula compliance atual vs novo: `{ complianceAtual: { resolucao: 92.3% }, complianceProjetado: { resolucao: 85.4% }, impacto: { resolucao: -6.9% } }` |
| 19 | - | Backend retorna HTTP 200 com resultado da simulação + recomendação: "ATENÇÃO: Redução de 6.9pp no compliance de resolução. Considere revisar recursos da equipe." |
| 20 | Frontend exibe resultado em card colorido: Compliance atual 92.3% (verde), Compliance projetado 85.4% (amarelo), Impacto -6.9% (vermelho) | - |
| 21 | Usuário lê recomendação, decide ajustar Tempo Resolução de volta para 240 min (4h) | - |
| 22 | Clica em aba "Dados Gerais" e ajusta campo "Tempo Resolução" para 240 | - |
| 23 | Clica em "Salvar SLA" | - |
| 24 | - | Frontend executa validação local (Angular Validators): Nome required, Tempo Resposta > 0, Tempo Resolução >= Tempo Resposta, Calendário selected |
| 25 | - | Frontend executa POST `/api/sla` com body JSON completo: `{ nmSLA, descricao, prioridade, tempoRespostaMinutos, tempoResolucaoMinutos, idCalendario, idCliente, idTipoChamado, flAtivo, escalacoes: [...] }` |
| 26 | - | Backend executa validação FluentValidation: RuleFor(x => x.TempoRespostaMinutos).GreaterThan(0), RuleFor(x => x.TempoResolucaoMinutos).GreaterThanOrEqualTo(x => x.TempoRespostaMinutos) |
| 27 | - | Backend valida **RN-SLA-069-02**: Não existe outro SLA ativo para Cliente = null + Tipo = "Incidente" + Prioridade = "Crítica" → Se existir: HTTP 400 "SLA_002: Já existe SLA ativo para esta combinação" |
| 28 | - | Backend valida **RN-SLA-069-03**: Id_Calendario NOT NULL e calendário existe e está ativo → Se inválido: HTTP 400 "Calendário selecionado não existe ou está inativo" |
| 29 | - | Backend cria entidade SLA_Chamado: Id_SLA = auto-increment, Nm_SLA, Prioridade, Tempo_Resposta_Minutos, Tempo_Resolucao_Minutos, Id_Calendario, Fl_Ativo = true, Dt_Criacao = GETUTCDATE(), Id_Usuario_Criacao = currentUser.Id |
| 30 | - | Backend persiste: `INSERT INTO SLA_Chamado (...) VALUES (...)` |
| 31 | - | Backend persiste escalações: `INSERT INTO Escalacao_SLA (Id_SLA, Nivel_Escalacao, Percentual_Tempo, Metrica, Destinatarios, Canal, Mensagem_Template)` para cada escalação configurada |
| 32 | - | Backend registra auditoria: AuditLog { Operacao = "SLA_CREATE", EntityType = "SLA_Chamado", EntityId = Id_SLA criado, NewValues = JSON completo do SLA, Usuario = currentUser.Email } |
| 33 | - | Backend publica evento SLACriadoEvent via MediatR para notificar outros módulos |
| 34 | - | Retorna HTTP 201 Created com body: `{ idSLA: 42, nmSLA: "SLA Crítico - Infraestrutura", flAtivo: true, dtCriacao: "2025-12-29T10:30:00Z" }` |
| 35 | Frontend exibe mensagem de sucesso i18n: `serviceDesk.sla.messages.createSuccess` ("SLA criado com sucesso") e redireciona para `/service-desk/sla` (lista) | - |

### 5. Fluxos Alternativos

**FA01: Criar SLA Específico para Cliente (Não Genérico)**
- No passo 4, usuário seleciona Cliente = "Cliente ABC" (dropdown populated via GET `/api/clientes`)
- Sistema cria SLA específico: aplicado APENAS a chamados do Cliente ABC
- Validação **RN-SLA-069-02** considera Cliente + Tipo + Prioridade (combinação mais específica)
- Fluxo retorna ao passo 25

**FA02: Usar Template de SLA Pré-Configurado**
- No passo 3, usuário clica em "Carregar Template" ao invés de preencher manualmente
- Frontend exibe modal com lista de templates: "SLA Crítico ITIL", "SLA Alta Padrão", "SLA Média 24h"
- Usuário seleciona "SLA Crítico ITIL"
- Frontend pré-preenche formulário com valores do template: Tempo Resposta = 15 min, Tempo Resolução = 240 min, 3 escalações configuradas (50%, 75%, 100%)
- Usuário ajusta Nome e Calendário (campos customizáveis)
- Fluxo retorna ao passo 23

**FA03: Não Usar Simulador (Pular Passo 12-21)**
- Usuário preenche formulário e clica direto em "Salvar SLA" sem acessar aba "Simulador"
- Validação backend continua normal
- SLA é criado sem simulação prévia
- Fluxo retorna ao passo 24

### 6. Exceções

**EX01: Tempo de Resolução Menor que Tempo de Resposta (Violação RN-SLA-069-01)**
- No passo 26, backend valida FluentValidation
- Usuário forneceu: Tempo Resposta = 240 min, Tempo Resolução = 120 min (resolução < resposta)
- FluentValidation falha: `RuleFor(x => x.TempoResolucaoMinutos).GreaterThanOrEqualTo(x => x.TempoRespostaMinutos)`
- Backend retorna HTTP 400: `{ error: "ValidationFailed", errors: [{ field: "tempoResolucaoMinutos", message: "Tempo de resolução deve ser maior ou igual ao tempo de resposta" }] }`
- Frontend exibe validação inline no campo "Tempo Resolução" com mensagem i18n: `serviceDesk.sla.validation.resolucaoMenorResposta`
- Fluxo retorna ao passo 4

**EX02: SLA Duplicado (Violação RN-SLA-069-02)**
- No passo 27, backend executa query: `SELECT COUNT(*) FROM SLA_Chamado WHERE Id_Cliente IS NULL AND Id_Tipo_Chamado = 3 AND Prioridade = 'Crítica' AND Fl_Ativo = true`
- Count > 0 → já existe SLA ativo para esta combinação
- Backend lança BusinessException("SLA_002", "Já existe SLA ativo para esta combinação Cliente/Tipo/Prioridade")
- Backend retorna HTTP 400: `{ error: "SLA_002", message: "Já existe SLA ativo para esta combinação Cliente/Tipo/Prioridade" }`
- Frontend exibe modal de erro com mensagem i18n: `serviceDesk.sla.validation.sladuplicado`
- Frontend sugere: "Deseja editar o SLA existente ao invés de criar novo?" com botões [Editar SLA Existente] [Cancelar]
- Fluxo termina

**EX03: Calendário Inválido (Violação RN-SLA-069-03)**
- No passo 28, backend valida Id_Calendario
- Usuário selecionou calendário ID = 99 (não existe ou foi excluído)
- Backend executa query: `SELECT COUNT(*) FROM Calendario WHERE Id_Calendario = 99 AND Fl_Ativo = true` → count = 0
- FluentValidation falha: `MustAsync(async (idCalendario) => await _context.Calendarios.AnyAsync(...))`
- Backend retorna HTTP 400: `{ error: "InvalidCalendar", message: "Calendário selecionado não existe ou está inativo" }`
- Frontend exibe erro inline no dropdown "Calendário" com mensagem i18n: `serviceDesk.sla.validation.calendarioObrigatorio`
- Fluxo retorna ao passo 4

**EX04: Simulador Retorna Erro (API de Simulação Indisponível)**
- No passo 15, frontend envia POST `/api/sla/simular-impacto`
- Backend tenta buscar chamados históricos mas DbContext lança TimeoutException
- Backend captura exceção, retorna HTTP 503: `{ error: "SimulatorUnavailable", message: "Simulador temporariamente indisponível. Tente novamente." }`
- Frontend exibe erro no card do simulador: "Erro ao simular impacto. Você pode continuar sem simulação."
- Frontend habilita botão "Salvar SLA" mesmo sem simulação
- Fluxo retorna ao passo 23 (usuário pode salvar sem simular)

### 7. Pós-condições

- SLA criado e persistido na tabela SLA_Chamado com Status = Ativo
- Escalações configuradas persistidas na tabela Escalacao_SLA vinculadas ao SLA
- Auditoria registrada em AuditLog com operação "SLA_CREATE"
- Evento SLACriadoEvent publicado via MediatR para outros módulos (ex: RF-073 Gestão de Chamados)
- Temporal Tables SQL Server inicia versionamento automático do SLA
- SLA disponível imediatamente para aplicação em novos chamados

### 8. Regras de Negócio Aplicáveis

- **RN-SLA-069-01**: Obrigatoriedade de Tempo de Resposta e Resolução (ambos > 0, resolução >= resposta)
- **RN-SLA-069-02**: Prioridade Única por Combinação Cliente/Tipo Chamado (não permite SLA duplicado)
- **RN-SLA-069-03**: Calendário Obrigatório (Id_Calendario NOT NULL, calendário deve existir e estar ativo)
- **RN-SLA-069-05**: Escalação Automática em Percentuais de Tempo (escalações configuradas com níveis 1-5)
- **RN-SLA-069-08**: Versionamento de SLA com Histórico Completo (Temporal Tables registra versão inicial)
- **RN-SLA-069-09**: Simulador de Impacto (opcional, mas recomendado antes de criar SLA restritivo)

---

## UC03: Editar SLA com Simulador e Versionamento Temporal

### 1. Descrição

Este caso de uso permite que gestores editem SLA existente alterando tempos de resposta/resolução, escalações, calendário ou status. Antes de salvar, opcionalmente simula impacto. Todas as alterações são versionadas automaticamente via Temporal Tables SQL Server, registrando histórico imutável com motivo da mudança obrigatório.

### 2. Atores

- **Usuário autenticado** com permissão `servicedesk:sla:update`
- **Sistema** (backend .NET 10, SQL Server Temporal Tables)

### 3. Pré-condições

- Usuário autenticado com perfil Supervisor, Gerente ou Administrador
- Permissões: `servicedesk:sla:update`, `servicedesk:sla:simulate` (opcional)
- SLA existe e não foi excluído (Fl_Excluido = false)
- Feature flag `SERVICE_DESK_SLA_CONFIGURACAO` habilitada

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Na lista de SLAs (UC01), clica em ação "Editar" de um SLA específico (ex: ID = 42) | - |
| 2 | - | Frontend valida permissão RBAC: `servicedesk:sla:update` → Se negado: HTTP 403 |
| 3 | - | Frontend executa GET `/api/sla/42` para buscar dados atuais |
| 4 | - | Backend query: `SELECT * FROM SLA_Chamado WHERE Id_SLA = 42 AND Id_Conglomerado = @idConglomerado` |
| 5 | - | Backend retorna HTTP 200 com SLA completo: `{ idSLA: 42, nmSLA: "SLA Crítico - Infraestrutura", prioridade: "Crítica", tempoRespostaMinutos: 15, tempoResolucaoMinutos: 240, ... }` |
| 6 | Frontend pré-preenche formulário de edição com valores atuais | - |
| 7 | Usuário altera Tempo Resolução de 240 min (4h) para 180 min (3h) | - |
| 8 | Usuário clica em aba "Simulador" e clica "Simular Impacto com Novos Valores" | - |
| 9 | - | Frontend executa POST `/api/sla/simular-impacto` com `{ idSLA: 42, novoTempoResolucaoMinutos: 180 }` |
| 10 | - | Backend busca chamados dos últimos 90 dias que usaram SLA ID = 42 |
| 11 | - | Backend recalcula compliance: compliance atual = 92.3%, compliance projetado = 85.4%, impacto = -6.9% |
| 12 | Frontend exibe resultado: "ATENÇÃO: Redução de 6.9pp no compliance. Considere revisar." | - |
| 13 | Usuário decide manter alteração (justificativa: negociação contratual com cliente) | - |
| 14 | Clica em "Salvar Alterações" | - |
| 15 | - | Frontend exibe modal obrigatório: "Motivo da Alteração (obrigatório para auditoria)" com textarea |
| 16 | Preenche motivo: "Negociação contratual - redução de 8h para 4h conforme aditivo CT-2025-042" | - |
| 17 | Clica em "Confirmar Alteração" | - |
| 18 | - | Frontend executa PUT `/api/sla/42` com body: `{ tempoResolucaoMinutos: 180, motivoAlteracao: "Negociação contratual..." }` |
| 19 | - | Backend busca SLA atual: `SELECT * FROM SLA_Chamado WHERE Id_SLA = 42` |
| 20 | - | Backend captura valores antes (before): `{ tempoResolucaoMinutos: 240 }` |
| 21 | - | Backend aplica alteração: `UPDATE SLA_Chamado SET Tempo_Resolucao_Minutos = 180, Dt_Atualizacao = GETUTCDATE(), Id_Usuario_Atualizacao = @userId WHERE Id_SLA = 42` |
| 22 | - | **Temporal Tables SQL Server**: Automaticamente move versão antiga para tabela `SLA_Chamado_History` com SysStartTime e SysEndTime |
| 23 | - | Backend registra auditoria customizada: AuditoriaSLA { Id_SLA = 42, Campo_Alterado = "Tempo_Resolucao_Minutos", Valor_Anterior = 240, Valor_Novo = 180, Motivo_Alteracao = "Negociação contratual...", Usuario = currentUser.Email, Dt_Alteracao = GETUTCDATE(), IP_Origem = httpContext.Connection.RemoteIpAddress } |
| 24 | - | Backend publica evento SLAAlteradoEvent via MediatR |
| 25 | - | Retorna HTTP 200: `{ idSLA: 42, tempoResolucaoMinutos: 180, dtAtualizacao: "2025-12-29T14:35:00Z" }` |
| 26 | Frontend exibe mensagem i18n: `serviceDesk.sla.messages.updateSuccess` ("SLA atualizado com sucesso") e fecha modal | - |
| 27 | Frontend atualiza linha da tabela (UC01) com novos valores sem recarregar página completa | - |

### 5. Fluxos Alternativos

**FA01: Inativar SLA ao Invés de Editar Valores**
- No passo 7, usuário altera toggle "Status" de Ativo para Inativo
- No passo 21, backend executa: `UPDATE SLA_Chamado SET Fl_Ativo = false WHERE Id_SLA = 42`
- Backend registra auditoria: Campo_Alterado = "Fl_Ativo", Valor_Anterior = true, Valor_Novo = false
- SLA inativado não é mais aplicado a novos chamados (RN-SLA-069-10 ignora SLAs com Fl_Ativo = false)
- Chamados existentes que já usam este SLA continuam usando (não retroativo)
- Fluxo retorna ao passo 25

**FA02: Editar Escalações (Adicionar/Remover Níveis)**
- No passo 7, usuário clica em aba "Escalações"
- Frontend exibe lista de escalações atuais: Nível 1 (50%), Nível 2 (75%), Nível 3 (100%)
- Usuário clica em "Editar" da escalação Nível 2, altera destinatário de "supervisor@empresa.com" para "gerente@empresa.com"
- Usuário clica em "Adicionar Escalação", cria Nível 4 (90%) com canal SMS
- No passo 21, backend executa: `UPDATE Escalacao_SLA SET Destinatarios = 'gerente@empresa.com' WHERE Id_Escalacao = X`, `INSERT INTO Escalacao_SLA (Id_SLA, Nivel_Escalacao = 4, Percentual_Tempo = 90, ...)`
- Backend registra auditoria para cada escalação alterada/criada
- Fluxo retorna ao passo 25

**FA03: Visualizar Histórico de Alterações Antes de Editar**
- No passo 1, antes de clicar em "Editar", usuário clica em ação "Ver Histórico"
- Frontend executa GET `/api/sla/42/historico`
- Backend query usando Temporal Tables: `SELECT * FROM SLA_Chamado FOR SYSTEM_TIME ALL WHERE Id_SLA = 42 ORDER BY SysStartTime DESC`
- Backend retorna array de versões: `[{ versao: 3, dtAlteracao: "2025-12-29", campo: "Tempo_Resolucao_Minutos", valorAnterior: 480, valorNovo: 240 }, { versao: 2, ... }]`
- Frontend exibe modal com timeline de alterações: cada alteração é um card com data, usuário, campo alterado, valores before/after, motivo
- Usuário fecha modal e clica em "Editar"
- Fluxo retorna ao passo 2

### 6. Exceções

**EX01: Motivo de Alteração Não Fornecido (Campo Obrigatório)**
- No passo 16, usuário deixa campo "Motivo da Alteração" vazio e clica em "Confirmar"
- Frontend valida campo obrigatório (Angular Validators.required)
- Frontend exibe erro: "Motivo da alteração é obrigatório para auditoria"
- Modal não fecha, usuário deve preencher motivo
- Fluxo retorna ao passo 16

**EX02: Edição de SLA Inativo (Violação de Regra de Negócio)**
- No passo 4, backend busca SLA com Fl_Ativo = false (SLA já inativado)
- Backend permite visualizar mas bloqueia edição (regra de negócio: SLA inativo só pode ser reativado, não editado)
- Backend retorna HTTP 400: `{ error: "InactiveSLA", message: "SLA inativo não pode ser editado. Reative o SLA antes de editar." }`
- Frontend exibe mensagem de erro e desabilita botão "Salvar Alterações"
- Fluxo termina

**EX03: Conflito de Concorrência (Outro Usuário Editou Simultaneamente)**
- No passo 21, backend tenta executar UPDATE
- Outro usuário editou SLA no mesmo momento (between passo 4 e passo 21)
- Entity Framework detecta concorrência via RowVersion ou Timestamp
- EF lança DbUpdateConcurrencyException
- Backend captura exceção, retorna HTTP 409 Conflict: `{ error: "ConcurrencyConflict", message: "Outro usuário editou este SLA. Recarregue a página e tente novamente." }`
- Frontend exibe modal de conflito com botões: [Recarregar e Sobrescrever] [Cancelar Edição]
- Se usuário escolhe "Recarregar": executa GET `/api/sla/42` novamente, perde alterações não salvas
- Fluxo retorna ao passo 3

### 7. Pós-condições

- SLA atualizado com novos valores
- Versão antiga preservada imutavelmente em tabela `SLA_Chamado_History` (Temporal Tables)
- Auditoria customizada registrada com before/after, motivo, usuário, IP, timestamp
- Evento SLAAlteradoEvent publicado para outros módulos
- Novos chamados criados após alteração usam novos prazos
- Chamados em andamento continuam usando prazos antigos (não retroativo)

### 8. Regras de Negócio Aplicáveis

- **RN-SLA-069-01**: Validação de tempos (resposta > 0, resolução >= resposta)
- **RN-SLA-069-02**: Validação de SLA único (se alterar Cliente/Tipo/Prioridade, verifica duplicidade)
- **RN-SLA-069-08**: Versionamento com Histórico Completo (Temporal Tables + auditoria customizada)
- **RN-SLA-069-09**: Simulador de Impacto (opcional mas recomendado antes de alterar prazos)

---

## UC04: Monitorar Compliance SLA com Dashboard Real-Time e Alertas

### 1. Descrição

Este caso de uso permite que gestores visualizem dashboard de compliance SLA em tempo real, com métricas agregadas por prioridade, cliente, equipe e período. Exibe KPIs principais (compliance resposta/resolução, violações, escalações disparadas) com atualização via SignalR e alertas automáticos quando thresholds são violados.

### 2. Atores

- **Usuário autenticado** com permissão `servicedesk:sla:report:view`
- **Sistema** (backend .NET 10, SignalR, Redis cache, Hangfire)

### 3. Pré-condições

- Usuário autenticado com perfil Supervisor, Gerente, Auditor ou Administrador
- Permissão: `servicedesk:sla:report:view`
- Feature flag `SERVICE_DESK_SLA_CONFIGURACAO` habilitada
- Hangfire job de monitoramento rodando (executa a cada 1 minuto)
- SignalR Hub conectado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Service Desk → Compliance SLA | - |
| 2 | - | Frontend valida permissão RBAC: `servicedesk:sla:report:view` → Se negado: HTTP 403 |
| 3 | - | Frontend estabelece conexão SignalR: `_hubConnection.start()` com URL `/hubs/servicedesk-sla` |
| 4 | - | SignalR Hub autentica via JWT, adiciona conexão ao grupo do tenant: `Groups.AddToGroupAsync(connectionId, idConglomerado)` |
| 5 | - | Frontend executa GET `/api/sla/compliance?periodo=ultimos30dias` |
| 6 | - | Backend tenta buscar do Redis cache: `_cache.GetStringAsync("sla_compliance_{idConglomerado}_30d")` |
| 7 | - | Se cache miss: Backend executa queries agregadas complexas (3 queries principais em paralelo) |
| 8 | - | Query 1 - Compliance Resposta: `SELECT (COUNT(CASE WHEN Fl_Resposta_Violada = false THEN 1 END) * 100.0 / COUNT(*)) FROM Chamado WHERE Dt_Abertura >= DATEADD(DAY, -30, GETUTCDATE()) AND Id_Conglomerado = @idConglomerado` → 96.5% |
| 9 | - | Query 2 - Compliance Resolução: `SELECT (COUNT(CASE WHEN Fl_Resolucao_Violada = false THEN 1 END) * 100.0 / COUNT(*)) FROM Chamado WHERE Status IN ('Resolvido', 'Fechado') AND Dt_Abertura >= DATEADD(DAY, -30, GETUTCDATE())` → 92.3% |
| 10 | - | Query 3 - Violações por Prioridade: `SELECT Prioridade, COUNT(*) as TotalViolacoes FROM Chamado WHERE Fl_Resolucao_Violada = true AND Dt_Abertura >= DATEADD(DAY, -30, GETUTCDATE()) GROUP BY Prioridade` → `[{ Crítica: 5 }, { Alta: 12 }, { Média: 8 }]` |
| 11 | - | Backend calcula métricas adicionais: Total Chamados (1250), Chamados com Escalação (320), Tempo Médio Resolução (450 min) |
| 12 | - | Backend armazena no Redis cache: `_cache.SetStringAsync("sla_compliance_{idConglomerado}_30d", JSON, TimeSpan.FromMinutes(5))` → cache por 5 minutos |
| 13 | - | Retorna HTTP 200 com body completo: `{ complianceResposta: 96.5, complianceResolucao: 92.3, totalChamados: 1250, violacoes: { critica: 5, alta: 12, media: 8 }, ... }` |
| 14 | Frontend renderiza 4 KPI cards no topo: [Compliance Resposta: 96.5% 🟢] [Compliance Resolução: 92.3% 🟢] [Total Violações: 25 🟡] [Escalações Disparadas: 320] | - |
| 15 | Frontend renderiza gráfico de barras (ApexCharts): "Violações por Prioridade" com barras coloridas (Crítica=vermelho, Alta=laranja, Média=amarelo) | - |
| 16 | Frontend renderiza gráfico de linha: "Tendência Compliance Últimos 30 Dias" com 2 linhas (Resposta, Resolução) | - |
| 17 | - | **Atualização em Tempo Real**: Hangfire job detecta nova violação de SLA em chamado ID = 9876 |
| 18 | - | Job registra violação: `UPDATE Chamado SET Fl_Resolucao_Violada = true WHERE Id_Chamado = 9876` |
| 19 | - | Job invalida cache Redis: `_cache.RemoveAsync("sla_compliance_{idConglomerado}_30d")` |
| 20 | - | Job dispara SignalR: `_hubContext.Clients.Group(idConglomerado).SendAsync("SLAViolacaoDetectada", { chamadoId: 9876, prioridade: "Crítica", dtViolacao: "2025-12-29T14:45:00Z" })` |
| 21 | Frontend escuta evento SignalR: `_hubConnection.on("SLAViolacaoDetectada", (data) => { ... })` | - |
| 22 | Frontend atualiza KPI "Total Violações" de 25 para 26, incrementa barra "Crítica" de 5 para 6 no gráfico | - |
| 23 | Frontend exibe notificação toast vermelha: "🚨 Nova violação SLA detectada - Chamado #9876 (Prioridade Crítica)" com link para o chamado | - |
| 24 | - | **Alerta Automático**: Backend detecta que Compliance Resolução caiu para 89.8% (abaixo do threshold 90%) |
| 25 | - | Backend cria registro de alerta: `INSERT INTO Alerta_Compliance (Id_Conglomerado, TipoAlerta = 'ComplianceAbaixoThreshold', Severidade = 'Alta', Descricao = 'Compliance de resolução caiu para 89.8% (meta: 90%)', Dt_Criacao)` |
| 26 | - | Backend envia e-mail para Gerente Service Desk: "ALERTA: Compliance SLA abaixo da meta por 2 semanas consecutivas" |
| 27 | - | Backend dispara SignalR: `_hubContext.Clients.Group(idConglomerado).SendAsync("AlertaComplianceCriado", { alerta })` |
| 28 | Frontend exibe banner vermelho no topo do dashboard: "⚠️ Compliance de resolução abaixo da meta (89.8% < 90%). Ação necessária." | - |

### 5. Fluxos Alternativos

**FA01: Filtrar Dashboard por Cliente Específico**
- No passo 5, usuário seleciona "Cliente ABC" no dropdown de filtro
- Frontend executa GET `/api/sla/compliance?periodo=ultimos30dias&idCliente=42`
- Backend ajusta queries: adiciona `AND Id_Cliente = 42` em todas as queries
- Backend calcula compliance apenas para chamados do Cliente ABC
- Frontend atualiza dashboard com métricas filtradas
- Fluxo retorna ao passo 14

**FA02: Drill-Down em Violação por Prioridade**
- No passo 15, usuário clica na barra "Crítica" (5 violações) no gráfico
- Frontend abre modal com lista detalhada: 5 chamados críticos violados com [ID] [Título] [Data Violação] [Tempo Decorrido] [Botão Ver Chamado]
- Usuário clica em "Ver Chamado #9876"
- Frontend redireciona para `/service-desk/chamados/9876` (RF-073)
- Fluxo termina

**FA03: Exportar Relatório Compliance em PDF**
- No passo 14, usuário clica em botão "Exportar PDF"
- Frontend executa GET `/api/sla/compliance/exportar?formato=pdf&periodo=ultimos30dias`
- Backend gera PDF usando iTextSharp com: cabeçalho corporativo, KPIs em tabela, gráficos convertidos para imagem (Chart.js renderizado server-side via Puppeteer), rodapé com data/hora geração
- Backend retorna HTTP 200 com Content-Type: `application/pdf`, Content-Disposition: `attachment; filename="Compliance_SLA_2025-12-29.pdf"`
- Frontend dispara download automático
- Fluxo termina

### 6. Exceções

**EX01: Cache Redis Indisponível (Fallback para Query Direta)**
- No passo 6, backend tenta acessar Redis
- Redis retorna erro de conexão (servidor offline)
- Backend captura exceção, registra log: `Nivel = "Warning", Mensagem = "Redis cache unavailable, querying database directly"`
- Backend executa queries diretamente no SQL Server sem cache
- Performance degradada (3s ao invés de 300ms) mas funcionalidade mantida
- Fluxo retorna ao passo 7

**EX02: SignalR Desconectado (Fallback para Polling)**
- No passo 21, frontend tenta escutar evento SignalR
- Conexão WebSocket é interrompida (rede instável)
- Frontend detecta evento `onclose()` do SignalR
- Frontend ativa polling manual: `setInterval(() => { GET /api/sla/compliance }, 60000)` → atualiza a cada 1 minuto
- Frontend exibe banner de aviso: "⚠️ Atualizações em tempo real desabilitadas. Dashboard será atualizado a cada 1 minuto."
- Fluxo continua com polling

**EX03: Query de Compliance Muito Lenta (Timeout)**
- No passo 7, backend executa queries agregadas
- Query demora > 30 segundos (tabela Chamado com milhões de registros sem índices adequados)
- Entity Framework lança TimeoutException
- Backend captura exceção, retorna HTTP 503: `{ error: "QueryTimeout", message: "Relatório de compliance indisponível temporariamente" }`
- Frontend exibe erro: "Erro ao carregar dashboard. Tente novamente em alguns instantes."
- Fluxo termina (recomenda-se otimizar queries com índices ou materialização)

### 7. Pós-condições

- Dashboard renderizado com métricas de compliance em tempo real
- Cache Redis populado (válido por 5 minutos) para performance
- Conexão SignalR ativa para atualizações push
- Alertas automáticos disparados quando thresholds violados
- Notificações enviadas para gestores via e-mail quando compliance crítico

### 8. Regras de Negócio Aplicáveis

- **RN-SLA-069-08**: Auditoria de Violações (todas violações registradas com timestamp e causa)
- **RN-SLA-069-05**: Escalações disparadas em tempo real (300+ escalações no período)
- **Compliance Target**: >= 95% resposta, >= 90% resolução (definido em contrato)

---

## UC05: Configurar Calendário de Operação com Importação Automática de Feriados

### 1. Descrição

Este caso de uso permite que administradores criem/editem calendários de operação (horário comercial, 24x7, fins de semana, plantão) definindo horário de início/fim, dias úteis e feriados. Integra-se com API pública (BrasilAPI) para importar automaticamente feriados nacionais anuais, além de permitir cadastro manual de feriados estaduais, municipais e corporativos.

### 2. Atores

- **Usuário autenticado** com permissão `servicedesk:sla:calendar:manage`
- **Sistema** (backend .NET 10, HttpClient, BrasilAPI)

### 3. Pré-condições

- Usuário autenticado com perfil Administrador
- Permissão: `servicedesk:sla:calendar:manage`
- Feature flag `SERVICE_DESK_SLA_INTEGRACAO_FERIADOS` habilitada
- Conexão com internet para API BrasilAPI (https://brasilapi.com.br)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Service Desk → Calendários de Operação | - |
| 2 | - | Frontend valida permissão RBAC: `servicedesk:sla:calendar:manage` → Se negado: HTTP 403 |
| 3 | - | Frontend executa GET `/api/sla/calendario` |
| 4 | - | Backend query: `SELECT * FROM Calendario WHERE Id_Conglomerado = @idConglomerado AND Fl_Excluido = false` |
| 5 | - | Retorna HTTP 200 com array de calendários: `[{ idCalendario: 1, nmCalendario: "Comercial 8-18h", horarioInicio: "08:00", horarioFim: "18:00", diasUteis: [1,2,3,4,5], fl24x7: false }, ...]` |
| 6 | Frontend renderiza lista com 3 calendários existentes: "Comercial 8-18h", "24x7 Plantão", "Fins de Semana" | - |
| 7 | Clica em "+ Novo Calendário" | - |
| 8 | - | Frontend exibe formulário: Nome (required), Horário Início (time picker), Horário Fim (time picker), Dias Úteis (checkboxes: Seg, Ter, Qua, Qui, Sex, Sáb, Dom), 24x7 (toggle, desabilita horários se ativado), Status (Ativo/Inativo) |
| 9 | Preenche formulário: Nome = "Comercial SP 9-18h", Horário Início = 09:00, Horário Fim = 18:00, Dias Úteis = [Seg, Ter, Qua, Qui, Sex], 24x7 = false, Status = Ativo | - |
| 10 | Clica em "Salvar Calendário" | - |
| 11 | - | Frontend executa POST `/api/sla/calendario` com body: `{ nmCalendario, horarioInicio, horarioFim, diasUteis: [1,2,3,4,5], fl24x7: false, flAtivo: true }` |
| 12 | - | Backend valida: Nome required, Horário Fim > Horário Início, Se fl24x7 = false então diasUteis deve ter pelo menos 1 dia |
| 13 | - | Backend persiste: `INSERT INTO Calendario (Nm_Calendario, Horario_Inicio, Horario_Fim, Dias_Uteis_JSON, Fl_24x7, Fl_Ativo, Id_Conglomerado, Dt_Criacao)` |
| 14 | - | Retorna HTTP 201: `{ idCalendario: 4, nmCalendario: "Comercial SP 9-18h", ... }` |
| 15 | Frontend exibe mensagem de sucesso e adiciona calendário à lista | - |
| 16 | Usuário clica em ação "Gerenciar Feriados" do calendário criado | - |
| 17 | - | Frontend executa GET `/api/sla/calendario/4/feriados` |
| 18 | - | Backend query: `SELECT * FROM Feriado WHERE Id_Calendario = 4 ORDER BY Dt_Feriado ASC` |
| 19 | - | Retorna HTTP 200 com array vazio (nenhum feriado cadastrado ainda): `{ data: [], totalCount: 0 }` |
| 20 | Frontend exibe modal com tabela vazia de feriados e botão "Importar Feriados Nacionais 2025" | - |
| 21 | Usuário clica em "Importar Feriados Nacionais 2025" | - |
| 22 | - | Frontend executa POST `/api/sla/calendario/importar-feriados` com body: `{ ano: 2025, tipo: "Nacional" }` |
| 23 | - | Backend invoca BrasilAPI: `GET https://brasilapi.com.br/api/feriados/v1/2025` |
| 24 | - | BrasilAPI retorna JSON com 10 feriados nacionais: `[{ date: "2025-01-01", name: "Ano Novo", type: "national" }, { date: "2025-04-21", name: "Tiradentes", type: "national" }, ...]` |
| 25 | - | Backend itera sobre feriados retornados, para cada um: verifica se já existe no banco (`SELECT COUNT(*) FROM Feriado WHERE Dt_Feriado = @date AND Id_Calendario = 4`) |
| 26 | - | Se NÃO existe: `INSERT INTO Feriado (Id_Calendario, Dt_Feriado, Nm_Feriado, Tipo, Fl_Recorrente, Id_Conglomerado)` |
| 27 | - | Backend registra log: `Nivel = "Info", Mensagem = "Importados 10 feriados nacionais para calendário 4"` |
| 28 | - | Backend registra auditoria: Operacao = "SLA_IMPORT_HOLIDAYS", Dados = "Ano: 2025, Quantidade: 10" |
| 29 | - | Retorna HTTP 201: `{ feriadosImportados: 10, message: "10 feriados nacionais importados com sucesso" }` |
| 30 | Frontend exibe mensagem de sucesso e recarrega tabela de feriados (executa GET `/api/sla/calendario/4/feriados` novamente) | - |
| 31 | Frontend renderiza tabela com 10 feriados: [2025-01-01 | Ano Novo | Nacional] [2025-04-21 | Tiradentes | Nacional] [...] | - |
| 32 | Usuário clica em "+ Adicionar Feriado Customizado" (ex: aniversário da empresa) | - |
| 33 | - | Frontend exibe formulário modal: Data (date picker), Nome (text), Tipo (dropdown: Nacional, Estadual, Municipal, Corporativo), Recorrente (checkbox - se marcado, repete todo ano) |
| 34 | Preenche: Data = 2025-06-15, Nome = "Aniversário Empresa", Tipo = Corporativo, Recorrente = true | - |
| 35 | Clica em "Adicionar Feriado" | - |
| 36 | - | Frontend executa POST `/api/sla/calendario/4/feriados` com body: `{ dtFeriado: "2025-06-15", nmFeriado: "Aniversário Empresa", tipo: "Corporativo", flRecorrente: true }` |
| 37 | - | Backend persiste: `INSERT INTO Feriado (Id_Calendario, Dt_Feriado, Nm_Feriado, Tipo, Fl_Recorrente)` |
| 38 | - | Retorna HTTP 201: `{ idFeriado: 101, dtFeriado: "2025-06-15", nmFeriado: "Aniversário Empresa" }` |
| 39 | Frontend adiciona feriado à tabela sem recarregar página | - |

### 5. Fluxos Alternativos

**FA01: Importar Feriados Estaduais (SP)**
- No passo 21, usuário clica em "Importar Feriados Estaduais - São Paulo"
- Frontend executa POST `/api/sla/calendario/importar-feriados` com body: `{ ano: 2025, tipo: "Estadual", uf: "SP" }`
- Backend invoca BrasilAPI (se disponível endpoint estadual) ou usa base interna de feriados estaduais
- Backend importa feriados específicos de SP (ex: 9 de Julho - Revolução Constitucionalista)
- Fluxo retorna ao passo 29

**FA02: Criar Calendário 24x7 (Sem Horário Limitado)**
- No passo 9, usuário marca toggle "24x7" = true
- Frontend desabilita campos Horário Início, Horário Fim, Dias Úteis (todos ignorados se 24x7)
- No passo 12, backend valida: Se fl24x7 = true, ignora validação de horários e dias
- Backend persiste com Horario_Inicio = NULL, Horario_Fim = NULL, Dias_Uteis_JSON = NULL
- Calendário 24x7 nunca pausa SLA (feriados também ignorados)
- Fluxo retorna ao passo 14

**FA03: Editar Feriado Existente (Corrigir Nome ou Data)**
- No passo 31, usuário clica em ação "Editar" de um feriado (ex: "Tiradentes")
- Frontend exibe modal pré-preenchido com dados atuais
- Usuário corrige nome de "Tiradentes" para "Dia de Tiradentes"
- Frontend executa PUT `/api/sla/calendario/4/feriados/15` com body: `{ nmFeriado: "Dia de Tiradentes" }`
- Backend atualiza: `UPDATE Feriado SET Nm_Feriado = 'Dia de Tiradentes', Dt_Atualizacao = GETUTCDATE() WHERE Id_Feriado = 15`
- Frontend atualiza linha da tabela
- Fluxo retorna ao passo 31

### 6. Exceções

**EX01: BrasilAPI Indisponível (HTTP 503)**
- No passo 23, backend tenta invocar BrasilAPI
- HttpClient lança HttpRequestException: "503 Service Unavailable"
- Backend captura exceção, registra log: `Nivel = "Error", Mensagem = "BrasilAPI indisponível, importação de feriados falhou"`
- Backend retorna HTTP 503: `{ error: "ExternalAPIUnavailable", message: "Serviço de feriados temporariamente indisponível. Tente novamente em alguns minutos." }`
- Frontend exibe erro no modal: "Erro ao importar feriados. Você pode adicionar feriados manualmente."
- Frontend habilita apenas opção "Adicionar Feriado Customizado"
- Fluxo termina

**EX02: Horário Fim Menor que Horário Início**
- No passo 12, backend valida horários
- Usuário forneceu: Horário Início = 18:00, Horário Fim = 09:00 (invertido)
- Validação FluentValidation falha: `RuleFor(x => x.HorarioFim).GreaterThan(x => x.HorarioInicio)`
- Backend retorna HTTP 400: `{ error: "ValidationFailed", errors: [{ field: "horarioFim", message: "Horário de fim deve ser maior que horário de início" }] }`
- Frontend exibe validação inline no campo "Horário Fim"
- Fluxo retorna ao passo 9

**EX03: Feriado Duplicado (Já Existe para Mesma Data)**
- No passo 37, backend tenta inserir feriado
- Já existe feriado na mesma data (2025-06-15) cadastrado anteriormente
- Backend executa validação: `SELECT COUNT(*) FROM Feriado WHERE Id_Calendario = 4 AND Dt_Feriado = '2025-06-15'` → count > 0
- Backend retorna HTTP 400: `{ error: "DuplicateHoliday", message: "Já existe feriado cadastrado para esta data (2025-06-15)" }`
- Frontend exibe erro: "Feriado duplicado. Edite o feriado existente ao invés de criar novo."
- Fluxo termina

### 7. Pós-condições

- Calendário criado e disponível para associação com SLAs
- Feriados nacionais importados automaticamente via BrasilAPI
- Feriados customizados (corporativos) cadastrados manualmente
- SLAs que usam este calendário calculam prazos corretamente excluindo feriados
- Auditoria registrada para importação de feriados

### 8. Regras de Negócio Aplicáveis

- **RN-SLA-069-03**: Calendário Obrigatório (todo SLA DEVE ter calendário associado)
- **RN-SLA-069-06**: Cálculo de Tempo Apenas em Horário Útil (calendário define horário início/fim e dias úteis)
- **RN-SLA-069-07**: Feriados Nacionais e Customizados (suporta Nacional, Estadual, Municipal, Corporativo + recorrentes)

---

## CHANGELOG

| Versão | Data       | Descrição                                                                 | Autor       |
|--------|------------|---------------------------------------------------------------------------|-------------|
| 1.0    | 2025-12-29 | Versão inicial com 5 casos de uso detalhados (UC01-UC05) com 18-39 passos cada | Claude Code |

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code
**Revisão**: Pendente de Aprovação

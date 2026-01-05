# UC-RF053 — Casos de Uso Canônicos

**RF:** RF053 — Gestão de Solicitações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF053**, cobrindo integralmente o comportamento funcional esperado para gestão completa de solicitações de serviço (service desk) com workflow configurável, SLA automático, aprovação mobile, chat interno, pesquisa NPS e dashboard em tempo real.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF053.yaml)
- Massas de Teste (MT-RF053.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Solicitações | Usuário Autenticado |
| UC01 | Criar Solicitação | Solicitante |
| UC02 | Visualizar Solicitação | Usuário Autenticado |
| UC03 | Editar Solicitação | Solicitante |
| UC04 | Aprovar/Rejeitar Solicitação | Aprovador/Gestor |
| UC05 | Atribuir Solicitação a Atendente | Supervisor |
| UC06 | Adicionar Comentário/Chat | Usuário Autenticado |
| UC07 | Anexar Arquivos | Usuário Autenticado |
| UC08 | Fechar Solicitação com Solução | Atendente |
| UC09 | Cancelar Solicitação | Solicitante/Supervisor |
| UC10 | Reabrir Solicitação (7 dias) | Solicitante |
| UC11 | Pausar/Retomar SLA | Atendente/Supervisor |
| UC12 | Escalar Solicitação | Sistema/Supervisor |
| UC13 | Responder Pesquisa de Satisfação (NPS) | Solicitante |
| UC14 | Delegar Aprovador Temporariamente | Gestor |
| UC15 | Visualizar Dashboard de Solicitações | Supervisor/Gerente |
| UC16 | Exportar Relatório de Solicitações | Supervisor/Administrador |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant (EmpresaId)**
- Todas as ações exigem **permissão explícita RBAC**
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Workflow de aprovação configurável por tipo de solicitação
- SLA automático com cálculo considerando apenas dias úteis
- Notificações push via SignalR para eventos críticos
- Histórico completo de ações registrado em SolicitacaoHistorico

---

## UC00 — Listar Solicitações

### Objetivo
Permitir que o usuário visualize solicitações conforme suas permissões (próprias ou todas).

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.VIEW_OWN` (próprias) ou `GES.SOLICITACOES.VIEW_ALL` (todas)

### Pós-condições
- Lista exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa "Solicitações" pelo menu
- **FP-UC00-002:** Sistema valida permissão
- **FP-UC00-003:** Se VIEW_OWN: filtra solicitações onde SolicitanteId = usuário atual
- **FP-UC00-004:** Se VIEW_ALL: carrega todas solicitações do tenant
- **FP-UC00-005:** Sistema aplica paginação padrão (20 registros)
- **FP-UC00-006:** Sistema aplica ordenação padrão (Data Abertura DESC)
- **FP-UC00-007:** Sistema exibe lista com colunas: Número, Tipo, Solicitante, Status, Prioridade, Data Abertura, SLA (% decorrido), Ações

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por status (Aberta, Em Aprovação, Aprovada, Rejeitada, Em Atendimento, Fechada, Cancelada)
- **FA-UC00-002:** Filtrar por tipo de solicitação
- **FA-UC00-003:** Filtrar por prioridade (Baixa, Média, Alta, Urgente)
- **FA-UC00-004:** Filtrar por período (data início, data fim)
- **FA-UC00-005:** Buscar por número da solicitação

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403
- **FE-UC00-002:** Nenhuma solicitação cadastrada → estado vazio

### Regras de Negócio
- **RN-UC-00-001:** Solicitante comum vê apenas suas próprias solicitações
- **RN-UC-00-002:** Atendentes, supervisores e gestores veem todas do tenant
- **RN-UC-00-003:** SLA exibido como % decorrido com cores (verde 0-50%, amarelo 50-80%, vermelho 80-100%, preto >100%)

### Critérios de Aceite
- **CA-UC00-001:** Lista DEVE respeitar permissões (VIEW_OWN vs VIEW_ALL)
- **CA-UC00-002:** SLA DEVE ser calculado considerando apenas dias úteis
- **CA-UC00-003:** Filtros DEVEM ser acumuláveis
- **CA-UC00-004:** Ordenação padrão DEVE ser por Data Abertura DESC

---

## UC01 — Criar Solicitação

### Objetivo
Permitir que qualquer usuário autenticado crie uma solicitação de serviço.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.CREATE`

### Pós-condições
- Solicitação criada com número único (SOL-YYYY-NNNNN)
- Workflow de aprovação iniciado (se aplicável)
- SLA calculado automaticamente
- Notificações enviadas

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Nova Solicitação"
- **FP-UC01-002:** Sistema exibe formulário com campos:
  - Tipo de Solicitação* (dropdown configurável)
  - Título* (string, máx. 100 caracteres)
  - Descrição* (textarea, máx. 2000 caracteres)
  - Campos Dinâmicos (conforme tipo selecionado - JSON schema)
  - Prioridade Sugerida (calculada automaticamente)
  - Anexos (opcional, múltiplos)
- **FP-UC01-003:** Usuário preenche campos obrigatórios
- **FP-UC01-004:** Usuário clica em "Enviar Solicitação"
- **FP-UC01-005:** Sistema valida dados (campos obrigatórios, anexos obrigatórios por tipo)
- **FP-UC01-006:** Sistema calcula prioridade final (cargo + tipo + impacto) - RN-RF053-02
- **FP-UC01-007:** Sistema gera número único (SOL-YYYY-NNNNN)
- **FP-UC01-008:** Sistema cria registro no banco com Status = ABERTA
- **FP-UC01-009:** Sistema verifica se tipo requer workflow de aprovação (RN-RF053-03)
- **FP-UC01-010:** Se requer aprovação: Status = EM_APROVACAO, envia notificação para 1º aprovador
- **FP-UC01-011:** Se não requer: Status = APROVADA, atribui a fila de atendentes
- **FP-UC01-012:** Sistema calcula DataLimiteSLA (RN-RF053-04)
- **FP-UC01-013:** Sistema registra auditoria
- **FP-UC01-014:** Sistema exibe mensagem "Solicitação SOL-YYYY-NNNNN criada com sucesso"
- **FP-UC01-015:** Sistema redireciona para visualização da solicitação

### Fluxos Alternativos
- **FA-UC01-001:** Cancelar criação → volta para lista sem salvar

### Fluxos de Exceção
- **FE-UC01-001:** Campos obrigatórios vazios → erro inline
- **FE-UC01-002:** Anexo obrigatório ausente (por tipo) → erro "Tipo X requer anexo de Y"
- **FE-UC01-003:** Arquivo inválido (tipo não permitido, tamanho > limite) → erro detalhado
- **FE-UC01-004:** Erro inesperado → mensagem genérica + log

### Regras de Negócio
- **RN-UC-01-001:** Número gerado automaticamente: SOL-{ANO}-{SEQUENCIAL}
- **RN-UC-01-002:** Prioridade calculada: (Cargo do solicitante × 0.3) + (Tipo × 0.4) + (Impacto × 0.3)
- **RN-UC-01-003:** Campos dinâmicos validados conforme JSON schema do tipo
- **RN-UC-01-004:** Tipos com valor estimado > R$ 10.000 exigem aprovação automática
- **RN-UC-01-005:** SolicitanteId = usuário autenticado
- **RN-UC-01-006:** EmpresaId = tenant do usuário

### Critérios de Aceite
- **CA-UC01-001:** Número DEVE ser único e sequencial por ano
- **CA-UC01-002:** Prioridade DEVE ser calculada automaticamente
- **CA-UC01-003:** Workflow de aprovação DEVE iniciar automaticamente se configurado
- **CA-UC01-004:** SLA DEVE ser calculado imediatamente
- **CA-UC01-005:** Notificações DEVEM ser enviadas para aprovadores (se aplicável)

---

## UC02 — Visualizar Solicitação

### Objetivo
Permitir visualização detalhada de uma solicitação com histórico completo.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.VIEW_OWN` ou `GES.SOLICITACOES.VIEW_ALL`

### Pós-condições
- Dados exibidos corretamente
- Timeline de ações atualizada

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em solicitação na listagem
- **FP-UC02-002:** Sistema valida permissão (própria ou todas)
- **FP-UC02-003:** Sistema valida que solicitação pertence ao tenant
- **FP-UC02-004:** Sistema carrega dados completos:
  - Informações básicas (Número, Tipo, Status, Prioridade, Datas)
  - Solicitante (Nome, Cargo, Departamento)
  - Atendente atual (se atribuído)
  - SLA (% decorrido, data limite, tempo pausado)
  - Campos dinâmicos preenchidos
  - Anexos
  - Histórico de aprovações
  - Timeline de ações (criação, aprovação, atribuição, comentários, mudanças de status)
  - Chat/Comentários (públicos para solicitante, todos para atendentes)
- **FP-UC02-005:** Sistema exibe detalhes organizados em abas/seções

### Fluxos Alternativos
- **FA-UC02-001:** Atualizar em tempo real via SignalR quando houver nova ação

### Fluxos de Exceção
- **FE-UC02-001:** Solicitação não encontrada → HTTP 404
- **FE-UC02-002:** Solicitação de outro tenant → HTTP 404
- **FE-UC02-003:** Usuário sem permissão (VIEW_OWN) tentando ver solicitação de outro → HTTP 403

### Regras de Negócio
- **RN-UC-02-001:** Solicitante vê apenas comentários públicos
- **RN-UC-02-002:** Atendentes veem comentários públicos + internos
- **RN-UC-02-003:** Timeline ordenada por data DESC (mais recente primeiro)

### Critérios de Aceite
- **CA-UC02-001:** Solicitante SÓ pode visualizar próprias solicitações
- **CA-UC02-002:** Atendentes/supervisores podem visualizar todas
- **CA-UC02-003:** Histórico DEVE estar completo e ordenado
- **CA-UC02-004:** SLA DEVE ser exibido com precisão
- **CA-UC02-005:** Anexos DEVEM ser clicáveis para download

---

## UC03 — Editar Solicitação

### Objetivo
Permitir edição de solicitação em aberto pelo solicitante original.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.CREATE`
- Status = ABERTA ou EM_APROVACAO
- Usuário é o solicitante original

### Pós-condições
- Solicitação atualizada
- Histórico registrado

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa solicitação própria
- **FP-UC03-002:** Usuário clica em "Editar"
- **FP-UC03-003:** Sistema valida que status permite edição (ABERTA ou EM_APROVACAO)
- **FP-UC03-004:** Sistema carrega formulário com dados atuais
- **FP-UC03-005:** Usuário altera campos permitidos (Título, Descrição, Campos Dinâmicos, Anexos)
- **FP-UC03-006:** Usuário clica em "Salvar Alterações"
- **FP-UC03-007:** Sistema valida alterações
- **FP-UC03-008:** Sistema persiste alterações
- **FP-UC03-009:** Sistema registra mudança no histórico
- **FP-UC03-010:** Sistema recalcula prioridade (se campos impactantes mudaram)
- **FP-UC03-011:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição → volta para visualização sem salvar

### Fluxos de Exceção
- **FE-UC03-001:** Status não permite edição (APROVADA, REJEITADA, FECHADA) → erro "Solicitação em status X não pode ser editada"
- **FE-UC03-002:** Usuário não é o solicitante original → HTTP 403
- **FE-UC03-003:** Validação de campos falhou → erros inline

### Regras de Negócio
- **RN-UC-03-001:** Apenas solicitante original pode editar
- **RN-UC-03-002:** Edição permitida apenas em ABERTA ou EM_APROVACAO
- **RN-UC-03-003:** Tipo de solicitação NÃO pode ser alterado
- **RN-UC-03-004:** Se em EM_APROVACAO, edição reinicia workflow (volta ao 1º nível)

### Critérios de Aceite
- **CA-UC03-001:** Tipo NÃO DEVE ser editável
- **CA-UC03-002:** Edição em EM_APROVACAO DEVE reiniciar workflow
- **CA-UC03-003:** Histórico DEVE registrar o que foi alterado
- **CA-UC03-004:** Prioridade DEVE ser recalculada se necessário

---

## UC04 — Aprovar/Rejeitar Solicitação

### Objetivo
Permitir que aprovadores aprovem ou rejeitem solicitações no workflow.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.APPROVE`
- Status = EM_APROVACAO
- Usuário é o aprovador do nível atual (ou delegado)

### Pós-condições (Aprovação)
- Nível de aprovação avançado
- Se último nível: Status = APROVADA
- Notificações enviadas

### Pós-condições (Rejeição)
- Status = REJEITADA
- Solicitação bloqueada
- Notificações enviadas

### Fluxo Principal
- **FP-UC04-001:** Aprovador acessa lista de "Pendentes de Aprovação"
- **FP-UC04-002:** Aprovador clica em solicitação
- **FP-UC04-003:** Sistema valida que usuário é aprovador do nível atual
- **FP-UC04-004:** Sistema exibe detalhes + botões "Aprovar" e "Rejeitar"
- **FP-UC04-005:** Aprovador clica em "Aprovar" ou "Rejeitar"
- **FP-UC04-006:** Se "Rejeitar": Sistema exibe campo "Justificativa*" (mín. 20 caracteres)
- **FP-UC04-007:** Aprovador confirma
- **FP-UC04-008:** Sistema valida justificativa (se rejeição)
- **FP-UC04-009:** Se Aprovação:
  - Sistema registra aprovação no banco (SolicitacaoAprovacao)
  - Sistema incrementa NivelAprovacaoAtual
  - Se último nível: Status = APROVADA, envia notificação para fila de atendentes
  - Senão: envia notificação para próximo aprovador
- **FP-UC04-010:** Se Rejeição:
  - Sistema marca Status = REJEITADA
  - Sistema registra justificativa
  - Sistema envia notificação para solicitante
- **FP-UC04-011:** Sistema registra auditoria
- **FP-UC04-012:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Aprovar via mobile (token temporário 15 min) - RN-RF053-05

### Fluxos de Exceção
- **FE-UC04-001:** Usuário não é aprovador do nível atual → HTTP 403
- **FE-UC04-002:** Justificativa de rejeição < 20 caracteres → erro
- **FE-UC04-003:** Solicitação já foi aprovada/rejeitada → erro "Solicitação já processada"

### Regras de Negócio
- **RN-UC-04-001:** Workflow configurável: 1, 2 ou 3 níveis conforme tipo/valor
- **RN-UC-04-002:** Rejeição em qualquer nível bloqueia solicitação (Status = REJEITADA)
- **RN-UC-04-003:** Justificativa obrigatória em rejeição (mín. 20 caracteres)
- **RN-UC-04-004:** Aprovação mobile válida por 15 minutos

### Critérios de Aceite
- **CA-UC04-001:** Aprovação DEVE avançar nível ou finalizar workflow
- **CA-UC04-002:** Rejeição DEVE bloquear solicitação imediatamente
- **CA-UC04-003:** Notificações DEVEM ser enviadas para todas as partes
- **CA-UC04-004:** Histórico DEVE registrar quem aprovou/rejeitou e quando

---

## UC05 — Atribuir Solicitação a Atendente

### Objetivo
Permitir que supervisor atribua solicitação aprovada a um atendente.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.ASSIGN`
- Status = APROVADA

### Pós-condições
- Solicitação atribuída
- Status = EM_ATENDIMENTO
- Notificação enviada ao atendente

### Fluxo Principal
- **FP-UC05-001:** Supervisor acessa lista de solicitações aprovadas
- **FP-UC05-002:** Supervisor clica em "Atribuir" em uma solicitação
- **FP-UC05-003:** Sistema exibe modal com dropdown de atendentes disponíveis
- **FP-UC05-004:** Supervisor seleciona atendente
- **FP-UC05-005:** Supervisor confirma
- **FP-UC05-006:** Sistema valida que atendente está ativo e disponível
- **FP-UC05-007:** Sistema atualiza AtendenteId e Status = EM_ATENDIMENTO
- **FP-UC05-008:** Sistema registra mudança no histórico
- **FP-UC05-009:** Sistema envia notificação push para atendente
- **FP-UC05-010:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC05-001:** Atribuição automática (round-robin ou menor carga)

### Fluxos de Exceção
- **FE-UC05-001:** Atendente inativo ou indisponível → erro
- **FE-UC05-002:** Solicitação já atribuída → erro

### Regras de Negócio
- **RN-UC-05-001:** Apenas solicitações com Status = APROVADA podem ser atribuídas
- **RN-UC-05-002:** Atendente deve pertencer ao tenant
- **RN-UC-05-003:** Reatribuição permitida (trocar atendente)

### Critérios de Aceite
- **CA-UC05-001:** Status DEVE mudar para EM_ATENDIMENTO
- **CA-UC05-002:** Notificação DEVE ser enviada ao atendente
- **CA-UC05-003:** Histórico DEVE registrar atribuição

---

## UC06 — Adicionar Comentário/Chat

### Objetivo
Permitir comunicação via chat entre solicitante, atendentes e supervisores.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.VIEW_OWN` ou `GES.SOLICITACOES.VIEW_ALL`

### Pós-condições
- Mensagem adicionada
- Notificação enviada

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa solicitação
- **FP-UC06-002:** Usuário escreve mensagem no campo de chat
- **FP-UC06-003:** Usuário marca como "Público" (visível para solicitante) ou "Interno" (apenas equipe)
- **FP-UC06-004:** Usuário clica em "Enviar"
- **FP-UC06-005:** Sistema valida mensagem (não vazia, máx. 1000 caracteres)
- **FP-UC06-006:** Sistema cria registro em MensagemSolicitacao
- **FP-UC06-007:** Sistema envia notificação push via SignalR
- **FP-UC06-008:** Sistema atualiza timeline em tempo real
- **FP-UC06-009:** Sistema exibe mensagem no chat

### Fluxos Alternativos
- **FA-UC06-001:** Anexar arquivo à mensagem

### Fluxos de Exceção
- **FE-UC06-001:** Mensagem vazia → erro
- **FE-UC06-002:** Mensagem > 1000 caracteres → erro

### Regras de Negócio
- **RN-UC-06-001:** Solicitante vê apenas mensagens públicas
- **RN-UC-06-002:** Atendentes/supervisores veem públicas + internas
- **RN-UC-06-003:** Mensagens ordenadas por data ASC (mais antiga primeiro)

### Critérios de Aceite
- **CA-UC06-001:** Mensagens DEVEM ser exibidas em tempo real (SignalR)
- **CA-UC06-002:** Mensagens internas NÃO devem ser visíveis para solicitante
- **CA-UC06-003:** Notificações DEVEM ser enviadas para partes relevantes

---

## UC07 — Anexar Arquivos

### Objetivo
Permitir upload de arquivos (fotos, documentos, evidências).

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.CREATE` ou `GES.SOLICITACOES.VIEW_ALL`

### Pós-condições
- Arquivo armazenado em Azure Blob
- Registro criado em SolicitacaoAnexo

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa solicitação
- **FP-UC07-002:** Usuário clica em "Anexar Arquivo"
- **FP-UC07-003:** Sistema exibe upload com validações:
  - Tipos permitidos: PDF, JPG, PNG, DOC, DOCX, XLS, XLSX
  - Tamanho máximo: 10 MB por arquivo
  - Máximo 10 arquivos por solicitação
- **FP-UC07-004:** Usuário seleciona arquivo(s)
- **FP-UC07-005:** Sistema valida tipo e tamanho
- **FP-UC07-006:** Sistema faz upload para Azure Blob Storage
- **FP-UC07-007:** Sistema cria registro em SolicitacaoAnexo com URL
- **FP-UC07-008:** Sistema registra no histórico
- **FP-UC07-009:** Sistema exibe arquivo na lista de anexos

### Fluxos Alternativos
- **FA-UC07-001:** Remover anexo (apenas próprio usuário ou supervisor)

### Fluxos de Exceção
- **FE-UC07-001:** Tipo de arquivo não permitido → erro
- **FE-UC07-002:** Arquivo > 10 MB → erro
- **FE-UC07-003:** Limite de 10 anexos atingido → erro
- **FE-UC07-004:** Erro no upload (Azure Blob) → mensagem de erro + retry

### Regras de Negócio
- **RN-UC-07-001:** Anexos armazenados em Azure Blob com URL assinada
- **RN-UC-07-002:** Tipos configuráveis por tipo de solicitação (alguns podem ser obrigatórios)
- **RN-UC-07-003:** Antivírus aplicado automaticamente no upload

### Critérios de Aceite
- **CA-UC07-001:** Tipos e tamanhos DEVEM ser validados antes do upload
- **CA-UC07-002:** Anexos DEVEM ser armazenados em Azure Blob
- **CA-UC07-003:** URL de download DEVE ser assinada e temporária
- **CA-UC07-004:** Antivírus DEVE ser executado automaticamente

---

## UC08 — Fechar Solicitação com Solução

### Objetivo
Permitir que atendente feche solicitação com solução registrada.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.CLOSE`
- Status = EM_ATENDIMENTO
- Usuário é o atendente atribuído ou supervisor

### Pós-condições
- Status = FECHADA
- Pesquisa de satisfação enviada
- SLA finalizado

### Fluxo Principal
- **FP-UC08-001:** Atendente acessa solicitação em andamento
- **FP-UC08-002:** Atendente clica em "Fechar Solicitação"
- **FP-UC08-003:** Sistema exibe formulário com campo "Solução*" (mín. 50 caracteres)
- **FP-UC08-004:** Atendente descreve solução aplicada
- **FP-UC08-005:** Atendente confirma
- **FP-UC08-006:** Sistema valida solução (mín. 50 caracteres)
- **FP-UC08-007:** Sistema atualiza Status = FECHADA
- **FP-UC08-008:** Sistema registra DataFechamento = timestamp atual
- **FP-UC08-009:** Sistema calcula tempo total de atendimento
- **FP-UC08-010:** Sistema envia pesquisa de satisfação (NPS) para solicitante - RN-RF053-12
- **FP-UC08-011:** Sistema registra histórico
- **FP-UC08-012:** Sistema envia notificação para solicitante
- **FP-UC08-013:** Sistema exibe mensagem "Solicitação fechada com sucesso"

### Fluxos Alternativos
- **FA-UC08-001:** Criar ativo automaticamente (se tipo = "Novo Ativo") - RN-RF053-10

### Fluxos de Exceção
- **FE-UC08-001:** Solução < 50 caracteres → erro
- **FE-UC08-002:** Usuário não é atendente atribuído → HTTP 403

### Regras de Negócio
- **RN-UC-08-001:** Solução obrigatória (mín. 50 caracteres)
- **RN-UC-08-002:** Pesquisa NPS enviada automaticamente
- **RN-UC-08-003:** Se tipo = "Novo Ativo": cria registro em Gestão de Ativos

### Critérios de Aceite
- **CA-UC08-001:** Solução DEVE ter mínimo 50 caracteres
- **CA-UC08-002:** Pesquisa NPS DEVE ser enviada automaticamente
- **CA-UC08-003:** Tempo total DEVE ser calculado corretamente
- **CA-UC08-004:** Integração com Gestão de Ativos DEVE funcionar (se aplicável)

---

## UC09 — Cancelar Solicitação

### Objetivo
Permitir cancelamento de solicitação com justificativa.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.CANCEL`
- Status ≠ FECHADA

### Pós-condições
- Status = CANCELADA
- Justificativa registrada

### Fluxo Principal
- **FP-UC09-001:** Supervisor acessa solicitação
- **FP-UC09-002:** Supervisor clica em "Cancelar Solicitação"
- **FP-UC09-003:** Sistema exibe modal com campo "Justificativa*" (mín. 20 caracteres)
- **FP-UC09-004:** Supervisor informa justificativa
- **FP-UC09-005:** Supervisor confirma
- **FP-UC09-006:** Sistema valida justificativa (RN-RF053-13)
- **FP-UC09-007:** Sistema atualiza Status = CANCELADA
- **FP-UC09-008:** Sistema registra JustificativaCancelamento
- **FP-UC09-009:** Sistema registra histórico
- **FP-UC09-010:** Sistema envia notificação para solicitante
- **FP-UC09-011:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- Nenhum

### Fluxos de Exceção
- **FE-UC09-001:** Justificativa < 20 caracteres → erro
- **FE-UC09-002:** Solicitação já fechada → erro "Solicitação fechada não pode ser cancelada"

### Regras de Negócio
- **RN-UC-09-001:** Justificativa obrigatória (mín. 20 caracteres) - RN-RF053-13
- **RN-UC-09-002:** Solicitação cancelada não pode mudar de status

### Critérios de Aceite
- **CA-UC09-001:** Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC09-002:** Status CANCELADA é final (sem transições permitidas)
- **CA-UC09-003:** Notificação DEVE ser enviada ao solicitante

---

## UC10 — Reabrir Solicitação (7 dias)

### Objetivo
Permitir que solicitante reabra solicitação fechada dentro de 7 dias.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.REOPEN`
- Status = FECHADA
- DataFechamento ≤ 7 dias atrás
- Usuário é o solicitante original

### Pós-condições
- Status = EM_ATENDIMENTO
- SLA recalculado

### Fluxo Principal
- **FP-UC10-001:** Solicitante acessa solicitação fechada (dentro de 7 dias)
- **FP-UC10-002:** Sistema exibe botão "Reabrir Solicitação"
- **FP-UC10-003:** Solicitante clica em "Reabrir"
- **FP-UC10-004:** Sistema valida que DataFechamento ≤ 7 dias (RN-RF053-11)
- **FP-UC10-005:** Sistema exibe modal "Motivo da Reabertura*" (mín. 20 caracteres)
- **FP-UC10-006:** Solicitante informa motivo
- **FP-UC10-007:** Solicitante confirma
- **FP-UC10-008:** Sistema valida motivo
- **FP-UC10-009:** Sistema atualiza Status = EM_ATENDIMENTO
- **FP-UC10-010:** Sistema recalcula SLA (novo prazo)
- **FP-UC10-011:** Sistema registra histórico com motivo da reabertura
- **FP-UC10-012:** Sistema envia notificação para atendente original
- **FP-UC10-013:** Sistema exibe mensagem "Solicitação reaberta com sucesso"

### Fluxos Alternativos
- Nenhum

### Fluxos de Exceção
- **FE-UC10-001:** DataFechamento > 7 dias → erro "Prazo de 7 dias expirado"
- **FE-UC10-002:** Usuário não é solicitante original → HTTP 403
- **FE-UC10-003:** Motivo < 20 caracteres → erro

### Regras de Negócio
- **RN-UC-10-001:** Reabertura permitida apenas dentro de 7 dias (RN-RF053-11)
- **RN-UC-10-002:** Apenas solicitante original pode reabrir
- **RN-UC-10-003:** Motivo obrigatório (mín. 20 caracteres)

### Critérios de Aceite
- **CA-UC10-001:** Prazo de 7 dias DEVE ser validado
- **CA-UC10-002:** SLA DEVE ser recalculado com novo prazo
- **CA-UC10-003:** Histórico DEVE registrar motivo da reabertura

---

## UC11 — Pausar/Retomar SLA

### Objetivo
Permitir pausa temporária do SLA quando aguardando resposta do solicitante.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.VIEW_ALL`
- Status = EM_ATENDIMENTO

### Pós-condições (Pausa)
- Status = AGUARDANDO_SOLICITANTE
- SLA pausado

### Pós-condições (Retomada)
- Status = EM_ATENDIMENTO
- SLA retomado

### Fluxo Principal (Pausar)
- **FP-UC11-001:** Atendente acessa solicitação em atendimento
- **FP-UC11-002:** Atendente clica em "Pausar SLA"
- **FP-UC11-003:** Sistema exibe modal "Motivo da Pausa*"
- **FP-UC11-004:** Atendente informa motivo (ex: "Aguardando resposta do solicitante")
- **FP-UC11-005:** Atendente confirma
- **FP-UC11-006:** Sistema atualiza Status = AGUARDANDO_SOLICITANTE
- **FP-UC11-007:** Sistema registra tempo decorrido até agora
- **FP-UC11-008:** Sistema para contagem de SLA
- **FP-UC11-009:** Sistema registra histórico

### Fluxo Principal (Retomar)
- **FP-UC11-010:** Atendente clica em "Retomar SLA"
- **FP-UC11-011:** Sistema atualiza Status = EM_ATENDIMENTO
- **FP-UC11-012:** Sistema recalcula DataLimiteSLA (tempo original - tempo já decorrido)
- **FP-UC11-013:** Sistema retoma contagem
- **FP-UC11-014:** Sistema registra histórico

### Fluxos de Exceção
- **FE-UC11-001:** Status não permite pausa → erro

### Regras de Negócio
- **RN-UC-11-001:** SLA pausa automaticamente em AGUARDANDO_SOLICITANTE
- **RN-UC-11-002:** Tempo pausado registrado em TempoPausadoSLA

### Critérios de Aceite
- **CA-UC11-001:** SLA DEVE parar contagem durante pausa
- **CA-UC11-002:** SLA DEVE ser recalculado corretamente ao retomar

---

## UC12 — Escalar Solicitação

### Objetivo
Escalar solicitação automaticamente ou manualmente quando SLA está crítico.

### Pré-condições
- Sistema ou supervisor
- SLA atingiu threshold de escalação (100%, 150%, 200%)

### Pós-condições
- Solicitação escalada para próximo nível
- Notificações enviadas

### Fluxo Principal (Automático)
- **FP-UC12-001:** Job Hangfire verifica solicitações com SLA > 100%
- **FP-UC12-002:** Sistema identifica solicitações para escalar (RN-RF053-08)
- **FP-UC12-003:** Sistema atribui para próximo nível:
  - 100% → Supervisor
  - 150% → Gerente
  - 200% → Diretor
- **FP-UC12-004:** Sistema envia notificações para novo responsável
- **FP-UC12-005:** Sistema registra histórico

### Fluxo Principal (Manual)
- **FP-UC12-006:** Supervisor acessa solicitação
- **FP-UC12-007:** Supervisor clica em "Escalar"
- **FP-UC12-008:** Sistema exibe dropdown de níveis superiores
- **FP-UC12-009:** Supervisor seleciona novo responsável
- **FP-UC12-010:** Sistema atualiza AtendenteId
- **FP-UC12-011:** Sistema envia notificação
- **FP-UC12-012:** Sistema registra histórico

### Regras de Negócio
- **RN-UC-12-001:** Escalação automática em 100%, 150%, 200% (RN-RF053-08)
- **RN-UC-12-002:** Níveis: Atendente → Supervisor → Gerente → Diretor

### Critérios de Aceite
- **CA-UC12-001:** Escalação automática DEVE ocorrer nos thresholds corretos
- **CA-UC12-002:** Notificações DEVEM ser enviadas

---

## UC13 — Responder Pesquisa de Satisfação (NPS)

### Objetivo
Permitir que solicitante avalie atendimento via NPS.

### Pré-condições
- Solicitação fechada
- Pesquisa enviada automaticamente

### Pós-condições
- Nota registrada
- Feedback opcional salvo

### Fluxo Principal
- **FP-UC13-001:** Solicitante recebe e-mail com link da pesquisa
- **FP-UC13-002:** Solicitante clica no link
- **FP-UC13-003:** Sistema exibe pesquisa:
  - "De 0 a 10, qual a probabilidade de recomendar nosso serviço?"
  - Campo opcional: "Comentários adicionais"
- **FP-UC13-004:** Solicitante informa nota (0-10)
- **FP-UC13-005:** Solicitante opcionalmente adiciona comentário
- **FP-UC13-006:** Solicitante clica em "Enviar"
- **FP-UC13-007:** Sistema registra em PesquisaSatisfacao
- **FP-UC13-008:** Sistema classifica como:
  - 0-6: Detrator
  - 7-8: Neutro
  - 9-10: Promotor
- **FP-UC13-009:** Sistema exibe mensagem "Obrigado pelo feedback!"

### Regras de Negócio
- **RN-UC-13-001:** Pesquisa enviada automaticamente ao fechar (RN-RF053-12)
- **RN-UC-13-002:** Link válido por 30 dias

### Critérios de Aceite
- **CA-UC13-001:** Pesquisa DEVE ser enviada automaticamente
- **CA-UC13-002:** Classificação NPS DEVE estar correta

---

## UC14 — Delegar Aprovador Temporariamente

### Objetivo
Permitir que gestor delegue suas aprovações para outro usuário (férias, ausências).

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.APPROVE`

### Pós-condições
- Delegação ativa
- Aprovações redirecionadas

### Fluxo Principal
- **FP-UC14-001:** Gestor acessa "Configurações de Delegação"
- **FP-UC14-002:** Gestor clica em "Nova Delegação"
- **FP-UC14-003:** Sistema exibe formulário:
  - Delegado* (dropdown de usuários)
  - Data Início* (date)
  - Data Fim* (date, máx. 90 dias)
- **FP-UC14-004:** Gestor preenche e confirma
- **FP-UC14-005:** Sistema valida período (RN-RF053-06)
- **FP-UC14-006:** Sistema cria registro em DelegacaoAprovador
- **FP-UC14-007:** Sistema redireciona aprovações pendentes para delegado
- **FP-UC14-008:** Sistema exibe mensagem de sucesso

### Regras de Negócio
- **RN-UC-14-001:** Período máximo 90 dias (RN-RF053-06)
- **RN-UC-14-002:** Sem sobreposição de delegações

### Critérios de Aceite
- **CA-UC14-001:** Período DEVE ser ≤ 90 dias
- **CA-UC14-002:** Aprovações DEVEM ser redirecionadas corretamente

---

## UC15 — Visualizar Dashboard de Solicitações

### Objetivo
Exibir dashboard em tempo real com métricas consolidadas.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.VIEW_ALL`

### Pós-condições
- Dashboard exibido
- Auto-refresh ativo

### Fluxo Principal
- **FP-UC15-001:** Supervisor acessa "Dashboard de Solicitações"
- **FP-UC15-002:** Sistema carrega métricas em tempo real via SignalR:
  - Total de solicitações abertas
  - Pendentes de aprovação
  - Em atendimento
  - Fechadas no mês
  - Tempo médio de resolução
  - Taxa de cumprimento de SLA (%)
  - NPS médio
  - Gráficos: linha (abertura vs fechamento), pizza (status), barras (por tipo)
- **FP-UC15-003:** Sistema ativa auto-refresh a cada 60s

### Regras de Negócio
- **RN-UC-15-001:** Dashboard em tempo real via SignalR (RN-RF053-14)
- **RN-UC-15-002:** Latência < 500ms

### Critérios de Aceite
- **CA-UC15-001:** Métricas DEVEM atualizar em tempo real
- **CA-UC15-002:** Latência DEVE ser < 500ms

---

## UC16 — Exportar Relatório de Solicitações

### Objetivo
Permitir exportação de relatórios em Excel ou PDF.

### Pré-condições
- Usuário autenticado
- Permissão `GES.SOLICITACOES.EXPORT`

### Pós-condições
- Arquivo gerado
- Download iniciado

### Fluxo Principal
- **FP-UC16-001:** Usuário acessa "Relatórios"
- **FP-UC16-002:** Usuário define filtros (período, status, tipo)
- **FP-UC16-003:** Usuário seleciona formato (Excel ou PDF)
- **FP-UC16-004:** Usuário clica em "Gerar Relatório"
- **FP-UC16-005:** Sistema gera arquivo
- **FP-UC16-006:** Sistema inicia download

### Regras de Negócio
- **RN-UC-16-001:** Exportação configurável (RN-RF053-15)
- **RN-UC-16-002:** Período máximo: 12 meses

### Critérios de Aceite
- **CA-UC16-001:** Filtros DEVEM ser aplicados corretamente
- **CA-UC16-002:** Formatos Excel e PDF DEVEM estar disponíveis

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF053 |
|----|------------------------|
| UC00 | RN-RF053-04 |
| UC01 | RN-RF053-01, RN-RF053-02, RN-RF053-03, RN-RF053-04, RN-RF053-07 |
| UC02 | RN-RF053-09 |
| UC03 | RN-RF053-02 |
| UC04 | RN-RF053-03, RN-RF053-05 |
| UC05 | - |
| UC06 | RN-RF053-09 |
| UC07 | RN-RF053-07 |
| UC08 | RN-RF053-10, RN-RF053-12 |
| UC09 | RN-RF053-13 |
| UC10 | RN-RF053-11 |
| UC11 | RN-RF053-04 |
| UC12 | RN-RF053-08 |
| UC13 | RN-RF053-12 |
| UC14 | RN-RF053-06 |
| UC15 | RN-RF053-14 |
| UC16 | RN-RF053-15 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato: 17 UCs completos (UC00-UC16), estrutura conforme template UC.md, cobertura 100% do RF053, fluxos detalhados, regras de negócio e critérios de aceite estruturados |
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial resumida com 10 UCs básicos |

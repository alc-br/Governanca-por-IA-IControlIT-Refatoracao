# WF-RF013 — Wireframes Canônicos (UI Contract)

**Versão:** 1.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF013 - Gestão de Perfis de Acesso (RBAC)
**UC Relacionado:** UC-RF013 (todos os 7 UCs)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF013 - Gestão de Perfis de Acesso (RBAC).

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional**
- Servir como **fonte de verdade para IA, QA e Desenvolvimento**
- Permitir derivação direta de **TCs E2E e testes de usabilidade**
- Evitar dependência de ferramentas específicas (ex: Filament, React, Vue)

> ⚠️ Este documento descreve **o que a tela deve permitir e comunicar**, não **como será implementado tecnicamente**.

---

## 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)

### 2.1 Princípios Gerais

- Clareza acima de estética
- Feedback imediato a toda ação do usuário
- Estados explícitos (loading, vazio, erro)
- Não ocultar erros críticos
- Comportamento previsível
- Segurança visual para permissões críticas

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória |
| Permissões críticas | Destacadas visualmente com indicador de alerta |
| Perfis de sistema | Badge "Sistema" visível |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF013)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Perfis | UC00 | Descoberta e acesso aos perfis |
| WF-02 | Criar Perfil | UC01 | Entrada de dados para novo perfil |
| WF-03 | Editar Perfil | UC03 | Alteração de dados do perfil |
| WF-04 | Visualizar Perfil | UC02 | Consulta detalhada do perfil |
| WF-05 | Confirmação de Exclusão | UC04 | Ação destrutiva (soft delete) |
| WF-06 | Gerenciar Permissões | UC05 | Atribuição/remoção de permissões |
| WF-07 | Duplicar Perfil | UC06 | Cópia de perfil existente |

---

## 4. WF-01 — LISTAGEM DE PERFIS DE ACESSO

### 4.1 Intenção da Tela
Permitir ao usuário **localizar, filtrar e acessar perfis de acesso** do seu tenant.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Criar Perfil" | Button | Ação primária para criar novo perfil (se tiver permissão) |
| CMP-WF01-002 | Campo de Busca por Nome | Input | Busca textual pelo nome do perfil |
| CMP-WF01-003 | Filtro de Tipo | Dropdown | Filtrar por Sistema/Personalizado |
| CMP-WF01-004 | Filtro de Status | Dropdown | Filtrar por Ativo/Inativo |
| CMP-WF01-005 | Tabela de Perfis | DataTable | Exibição dos perfis com paginação (20 registros) |
| CMP-WF01-006 | Botão Visualizar | IconButton | Ação para visualizar perfil (cada linha) |
| CMP-WF01-007 | Botão Editar | IconButton | Ação para editar perfil (cada linha, se tiver permissão) |
| CMP-WF01-008 | Botão Excluir | IconButton | Ação para excluir perfil (cada linha, se tiver permissão) |
| CMP-WF01-009 | Botão Duplicar | IconButton | Ação para duplicar perfil (cada linha, se tiver permissão) |
| CMP-WF01-010 | Paginação | Pagination | Controles de navegação (20 registros por página) |
| CMP-WF01-011 | Badge "Sistema" | Badge | Indicador visual para perfis de sistema |
| CMP-WF01-012 | Coluna Usuários Vinculados | Counter | Contagem de usuários ativos com o perfil |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Criar Perfil" | Usuário clica em CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca por nome | Usuário digita no campo CMP-WF01-002 | UC00 | FA-UC00-01 |
| EVT-WF01-003 | Filtro por tipo | Usuário seleciona no dropdown CMP-WF01-003 | UC00 | FA-UC00-02 |
| EVT-WF01-004 | Filtro por status | Usuário seleciona no dropdown CMP-WF01-004 | UC00 | FA-UC00-03 |
| EVT-WF01-005 | Clique em Visualizar | Usuário clica em CMP-WF01-006 | UC02 | FP-UC02-001 |
| EVT-WF01-006 | Clique em Editar | Usuário clica em CMP-WF01-007 | UC03 | FP-UC03-001 |
| EVT-WF01-007 | Clique em Excluir | Usuário clica em CMP-WF01-008 | UC04 | FP-UC04-001 |
| EVT-WF01-008 | Clique em Duplicar | Usuário clica em CMP-WF01-009 | UC06 | FP-UC06-001 |
| EVT-WF01-009 | Ordenar por coluna | Usuário clica no cabeçalho da tabela | UC00 | FA-UC00-04 |
| EVT-WF01-010 | Mudança de página | Usuário interage com CMP-WF01-010 | UC00 | FP-UC00-004 |

### 4.4 Ações Permitidas
- Visualizar lista de perfis do tenant
- Buscar perfil por nome (filtro LIKE)
- Filtrar por tipo (Sistema/Personalizado)
- Filtrar por status (Ativo/Inativo)
- Ordenar por colunas (Nome, Tipo, Status, Usuários Vinculados)
- Criar novo perfil (se tiver permissão `perfis:perfil:create`)
- Editar perfil (se tiver permissão `perfis:perfil:update`)
- Visualizar perfil (se tiver permissão `perfis:perfil:view`)
- Excluir perfil (se tiver permissão `perfis:perfil:delete`)
- Duplicar perfil (se tiver permissão `perfis:perfil:duplicate`)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando perfis do tenant
**Exibir:**
- Skeleton loader (tabela com 5 linhas)
- Mensagem: "Carregando perfis de acesso..."
- Filtros desabilitados

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há perfis cadastrados no tenant
**Exibir:**
- Ícone ilustrativo (ícone de perfil vazio)
- Mensagem: "Nenhum perfil de acesso cadastrado"
- Submensagem: "Crie o primeiro perfil para controlar permissões de acesso ao sistema"
- Botão "Criar Perfil" destacado (se tiver permissão)

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, timeout, etc.)
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar perfis de acesso. Tente novamente."
- Botão "Recarregar"
- Log técnico registrado (não exibido ao usuário)

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há perfis disponíveis no tenant
**Exibir:**
- Tabela com colunas:
  - Nome (com badge "Sistema" se IsSystemRole = true)
  - Descrição
  - Tipo (Sistema/Personalizado)
  - Status (Ativo/Inativo - badge visual)
  - Usuários Vinculados (contagem)
  - Ações (Visualizar, Editar, Excluir, Duplicar - conforme permissões)
- Paginação (20 registros por página)
- Filtros ativos refletidos na URL
- Contagem total de registros

### 4.6 Contratos de Comportamento

#### Isolamento Multi-Tenancy
- Lista DEVE exibir apenas perfis do tenant do usuário (WHERE EmpresaId = @EmpresaId) OU perfis de sistema (WHERE EmpresaId IS NULL)
- Perfis de outros tenants NUNCA devem aparecer

#### Filtros e Ordenação
- Filtros são acumuláveis (busca + tipo + status)
- Ordenação padrão: Nome ASC
- Estado dos filtros persiste na URL (query parameters)

#### Permissões Visuais
- Botões de ação visíveis apenas se usuário tiver permissão correspondente
- Perfis de sistema exibem badge "Sistema" destacado
- Contagem de usuários vinculados deve ser clicável (link para lista de usuários)

#### Responsividade

- **Mobile:**
  - Lista empilhada (cards verticais)
  - Filtros em modal colapsável
  - Ações em menu dropdown por card

- **Tablet:**
  - Tabela simplificada (4 colunas: Nome, Tipo, Status, Ações)
  - Paginação mantida

- **Desktop:**
  - Tabela completa (todas as colunas)
  - Filtros inline no topo
  - Ações como botões inline

#### Acessibilidade (WCAG AA)
- Labels em português claro: "Nome do Perfil", "Tipo", "Status"
- Botões com aria-label: "Visualizar perfil {Nome}", "Editar perfil {Nome}"
- Navegação por teclado: Tab (navegar), Enter (ativar), Esc (cancelar)
- Contraste mínimo 4.5:1 em textos
- Badges de status com cores acessíveis e texto alternativo

#### Feedback ao Usuário
- Loading spinner durante carregamento inicial
- Skeleton loader durante filtragem/paginação
- Toast de sucesso após criação/edição/exclusão
- Confirmação modal antes de exclusão

---

## 5. WF-02 — CRIAR PERFIL DE ACESSO

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de um novo perfil de acesso com permissões granulares.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo Nome | Input | Campo obrigatório para nome do perfil (max 100 caracteres) |
| CMP-WF02-002 | Campo Descrição | Textarea | Campo opcional para descrição (max 500 caracteres) |
| CMP-WF02-003 | Painel Permissões | PermissionTreeView | Lista de permissões agrupadas por módulo (checkboxes) |
| CMP-WF02-004 | Campo Busca Permissões | Input | Busca textual de permissões por nome/código |
| CMP-WF02-005 | Checkbox Master por Módulo | Checkbox | Selecionar/desmarcar todas as permissões do módulo |
| CMP-WF02-006 | Badge "Crítica" | Badge | Indicador visual para permissões críticas |
| CMP-WF02-007 | Campo Justificativa | Textarea | Campo obrigatório quando permissão crítica selecionada (min 20 caracteres) |
| CMP-WF02-008 | Botão Salvar | Button | Ação primária para criar perfil |
| CMP-WF02-009 | Botão Salvar e Criar Outro | Button | Ação secundária para criar e manter formulário aberto |
| CMP-WF02-010 | Botão Cancelar | Button | Ação terciária para cancelar criação |
| CMP-WF02-011 | Mensagem de Erro | Alert | Exibe erros de validação |
| CMP-WF02-012 | Tooltip Descrição Permissão | Tooltip | Descrição detalhada da permissão ao passar mouse |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Submissão de Formulário | Usuário clica em CMP-WF02-008 | UC01 | FP-UC01-005 |
| EVT-WF02-002 | Salvar e Criar Outro | Usuário clica em CMP-WF02-009 | UC01 | FA-UC01-01 |
| EVT-WF02-003 | Cancelamento | Usuário clica em CMP-WF02-010 | UC01 | FA-UC01-02 |
| EVT-WF02-004 | Validação Nome | Usuário sai do campo Nome vazio | UC01 | FE-UC01-03 |
| EVT-WF02-005 | Validação Descrição | Sistema valida limite de 500 caracteres | UC01 | FE-UC01-04 |
| EVT-WF02-006 | Seleção Permissão Crítica | Usuário marca checkbox de permissão crítica | UC01 | UC05 FP |
| EVT-WF02-007 | Erro Nome Duplicado | API retorna erro de duplicidade | UC01 | FE-UC01-01 |
| EVT-WF02-008 | Erro Formato Permissão | API valida formato inválido | UC01 | FE-UC01-02 |
| EVT-WF02-009 | Busca Permissões | Usuário digita em CMP-WF02-004 | UC05 | FA-UC05-02 |
| EVT-WF02-010 | Checkbox Master | Usuário marca/desmarca CMP-WF02-005 | UC05 | FA-UC05-01 |
| EVT-WF02-011 | Ver Descrição | Usuário passa mouse sobre permissão | UC05 | FA-UC05-03 |

### 5.4 Comportamentos Obrigatórios

- Campo Nome destacado visualmente como obrigatório (asterisco)
- Validação de Nome único no tenant antes do envio (client-side preview)
- Permissões agrupadas por módulo (CONTRATOS, FATURAS, USUARIOS, PERFIS, etc.)
- Permissões críticas destacadas com badge "Crítica" em vermelho/laranja
- Campo Justificativa aparece dinamicamente quando permissão crítica é selecionada
- Contador de caracteres visível em campos com limite (Nome, Descrição, Justificativa)
- Feedback imediato ao desmarcar permissão crítica (campo Justificativa oculto)
- Botão Salvar desabilitado até que validações básicas passem
- Confirmação de cancelamento se houver dados preenchidos

### 5.5 Estados Obrigatórios

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário acessa tela de criação
**Exibir:**
- Formulário vazio
- Foco automático no campo Nome
- Botão Salvar desabilitado
- Painel de permissões colapsado por módulo (expandir ao clicar)

#### Estado 2: Erro de Validação
**Quando:** Validação falha (nome vazio, duplicado, formato inválido, etc.)
**Exibir:**
- Campos com erro destacados em vermelho
- Mensagem de erro específica abaixo do campo com problema
- Alert no topo com resumo dos erros
- Scroll automático para primeiro erro
- Botão Salvar permanece habilitado (para retry)

#### Estado 3: Permissão Crítica Selecionada
**Quando:** Usuário marca checkbox de permissão crítica
**Exibir:**
- Campo Justificativa aparece dinamicamente (slide-in)
- Mensagem de alerta: "Permissões críticas exigem justificativa detalhada"
- Contador de caracteres: "0/20 caracteres (mínimo 20)"
- Badge "Crítica" destacado na permissão selecionada

#### Estado 4: Salvando (Loading)
**Quando:** Requisição POST enviada ao backend
**Exibir:**
- Spinner no botão Salvar
- Formulário desabilitado (overlay)
- Mensagem: "Criando perfil..."

#### Estado 5: Sucesso
**Quando:** API retorna 201 Created
**Exibir:**
- Toast de sucesso: "Perfil '{Nome}' criado com sucesso!"
- **Se Salvar:** Redirecionar para listagem (WF-01)
- **Se Salvar e Criar Outro:** Limpar formulário e focar no campo Nome

#### Estado 6: Erro de Backend
**Quando:** API retorna 400/500
**Exibir:**
- Alert de erro no topo do formulário
- Mensagem clara e acionável:
  - Nome duplicado: "Já existe um perfil com este nome nesta empresa"
  - Formato inválido: "Formato de permissão inválido: deve ser modulo:recurso:acao"
  - Erro genérico: "Erro ao criar perfil. Tente novamente."
- Log técnico registrado (não exibido)

### 5.6 Contratos de Comportamento

#### Validações Client-Side
- Nome: obrigatório, max 100 caracteres, não vazio
- Descrição: opcional, max 500 caracteres
- Permissões: formato `modulo:recurso:acao` validado antes do envio
- Justificativa: obrigatória se permissão crítica selecionada, min 20 caracteres

#### Validações Server-Side
- Nome único por tenant (case-insensitive)
- EmpresaId preenchido automaticamente com tenant do usuário
- IsSystemRole = false (sempre)
- Fl_Ativo = 1 (sempre)
- Created, CreatedBy preenchidos automaticamente

#### Permissões Críticas (lista obrigatória)
- `usuarios:usuario:*` (qualquer ação em usuários)
- `perfis:perfil:*` (qualquer ação em perfis)
- `contratos:contrato:approve` (aprovação de contratos)
- `faturas:fatura:import` (importação de faturas)

#### Responsividade

- **Mobile:**
  - Formulário em coluna única
  - Painel de permissões em accordions
  - Botões empilhados verticalmente

- **Tablet:**
  - Formulário em 2 colunas (Nome/Descrição à esquerda, Permissões à direita)
  - Botões inline (Salvar, Salvar e Criar Outro, Cancelar)

- **Desktop:**
  - Formulário em 2 painéis lado a lado
  - Painel esquerdo: Dados gerais (Nome, Descrição)
  - Painel direito: Permissões (árvore completa)

#### Acessibilidade (WCAG AA)
- Label "Nome do Perfil *" (asterisco indica obrigatório)
- Aria-required="true" em campos obrigatórios
- Aria-invalid="true" em campos com erro
- Mensagens de erro associadas ao campo (aria-describedby)
- Navegação por teclado: Tab (campos), Espaço (checkboxes), Enter (salvar), Esc (cancelar)
- Contraste de cores em badges de permissão crítica

---

## 6. WF-03 — EDITAR PERFIL DE ACESSO

### 6.1 Intenção da Tela
Permitir **alteração controlada** de um perfil de acesso existente, respeitando restrições de perfis de sistema.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Campo Nome | Input | Nome do perfil (editável apenas se perfil personalizado) |
| CMP-WF03-002 | Campo Descrição | Textarea | Descrição do perfil (editável apenas se perfil personalizado) |
| CMP-WF03-003 | Badge "Perfil de Sistema" | Badge | Indicador visual (se IsSystemRole = true) |
| CMP-WF03-004 | Mensagem Restrição | Alert | "Perfis de sistema não podem ter nome ou descrição alterados" |
| CMP-WF03-005 | Painel Permissões | PermissionTreeView | Lista de permissões agrupadas por módulo (sempre editável) |
| CMP-WF03-006 | Campo Busca Permissões | Input | Busca textual de permissões |
| CMP-WF03-007 | Checkbox Master por Módulo | Checkbox | Selecionar/desmarcar todas do módulo |
| CMP-WF03-008 | Badge "Crítica" | Badge | Indicador visual para permissões críticas |
| CMP-WF03-009 | Campo Justificativa | Textarea | Obrigatório quando permissão crítica adicionada (min 20 caracteres) |
| CMP-WF03-010 | Botão Salvar | Button | Ação primária para salvar alterações |
| CMP-WF03-011 | Botão Cancelar | Button | Ação secundária para cancelar edição |
| CMP-WF03-012 | Painel Auditoria | InfoPanel | Exibe Created, CreatedBy, LastModified, LastModifiedBy |
| CMP-WF03-013 | Link Histórico | Link | Redireciona para RF-004 (Sistema de Auditoria) |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Submissão de Formulário | Usuário clica em CMP-WF03-010 | UC03 | FP-UC03-008 |
| EVT-WF03-002 | Cancelamento | Usuário clica em CMP-WF03-011 | UC03 | FA-UC03-01 |
| EVT-WF03-003 | Seleção Permissão Crítica | Usuário marca checkbox de permissão crítica nova | UC03 | FA-UC03-02 |
| EVT-WF03-004 | Validação Nome | Sistema valida nome único | UC03 | FE-UC03-01 |
| EVT-WF03-005 | Tentativa Editar Perfil Sistema | Usuário tenta alterar Nome/Descrição com IsSystemRole=true | UC03 | FE-UC03-02 |
| EVT-WF03-006 | Erro Justificativa Faltante | API valida permissão crítica sem justificativa | UC03 | FE-UC03-03 |
| EVT-WF03-007 | Ver Histórico | Usuário clica em CMP-WF03-013 | UC02 | FA-UC02-02 |

### 6.4 Regras Visuais

#### Perfis Personalizados (IsSystemRole = false)
- Campos Nome e Descrição **editáveis**
- Botão Salvar habilitado após alterações
- Sem mensagem de restrição

#### Perfis de Sistema (IsSystemRole = true)
- Badge "Perfil de Sistema" visível no topo
- Campos Nome e Descrição **desabilitados** (read-only)
- Mensagem informativa: "Perfis de sistema não podem ter nome ou descrição alterados. Apenas permissões podem ser modificadas."
- Painel de permissões **sempre editável**

#### Diferença Visual de Alterações
- Permissões adicionadas: checkbox com borda verde + ícone "+"
- Permissões removidas: checkbox desmarcado com borda vermelha + ícone "-"
- Campos alterados: borda amarela discreta
- Indicador "Não salvo" se houver alterações pendentes

### 6.5 Estados Obrigatórios

#### Estado 1: Carregando Dados (Loading)
**Quando:** Tela está sendo carregada
**Exibir:**
- Skeleton loader do formulário
- Mensagem: "Carregando perfil..."

#### Estado 2: Dados Carregados (Inicial)
**Quando:** Dados do perfil carregados com sucesso
**Exibir:**
- Formulário pré-preenchido com dados atuais
- Permissões atuais marcadas
- Botão Salvar desabilitado (sem alterações)
- Painel de auditoria com timestamps

#### Estado 3: Editando (Com Alterações)
**Quando:** Usuário altera qualquer campo ou permissão
**Exibir:**
- Indicador visual de alterações pendentes
- Botão Salvar habilitado
- Confirmação ao tentar sair sem salvar

#### Estado 4: Permissão Crítica Adicionada
**Quando:** Usuário marca checkbox de permissão crítica que não estava selecionada
**Exibir:**
- Campo Justificativa aparece dinamicamente
- Mensagem: "Justificativa obrigatória para permissões críticas"
- Badge "Crítica" destacado

#### Estado 5: Salvando (Loading)
**Quando:** Requisição PUT enviada ao backend
**Exibir:**
- Spinner no botão Salvar
- Formulário desabilitado
- Mensagem: "Salvando alterações..."

#### Estado 6: Sucesso
**Quando:** API retorna 200 OK
**Exibir:**
- Toast: "Perfil '{Nome}' atualizado com sucesso!"
- Atualizar painel de auditoria (LastModified, LastModifiedBy)
- Desabilitar botão Salvar (sem alterações pendentes)
- Invalidar cache de permissões (não visível ao usuário)

#### Estado 7: Erro de Validação
**Quando:** API retorna 400
**Exibir:**
- Mensagens específicas:
  - Nome duplicado: "Já existe um perfil com este nome"
  - Perfil de sistema: "Perfis de sistema não podem ter nome ou descrição alterados"
  - Permissão crítica sem justificativa: "Justificativa obrigatória para permissões críticas"

#### Estado 8: Erro de Acesso
**Quando:** Perfil de outro tenant ou não encontrado
**Exibir:**
- HTTP 404
- Mensagem: "Perfil não encontrado"
- Redirecionamento automático para listagem após 3 segundos

### 6.6 Contratos de Comportamento

#### Validações Server-Side
- Nome único por tenant (se alterado)
- IsSystemRole = true → Nome/Descrição não podem ser alterados
- Permissões críticas exigem justificativa
- Isolamento de tenant obrigatório
- LastModified, LastModifiedBy atualizados automaticamente
- Cache de permissões invalidado após salvamento

#### Auditoria
- Registro de estado anterior e novo estado
- Log de permissões adicionadas/removidas
- Timestamp e IP do usuário
- Justificativa registrada se permissão crítica

#### Notificações
- Toast de sucesso após salvamento
- Notificação ao gestor se permissão crítica foi atribuída (assíncrona)

#### Responsividade

- **Mobile:**
  - Formulário em coluna única
  - Painel de permissões em accordions
  - Botões empilhados

- **Tablet:**
  - Formulário em 2 colunas
  - Painel de auditoria colapsável

- **Desktop:**
  - Layout em 3 painéis:
    - Esquerda: Dados gerais
    - Centro: Permissões
    - Direita: Auditoria

#### Acessibilidade (WCAG AA)
- Campos desabilitados com aria-disabled="true" e explicação visível
- Indicador de alterações anunciado por screen reader
- Confirmação ao sair sem salvar (modal acessível)

---

## 7. WF-04 — VISUALIZAR PERFIL DE ACESSO

### 7.1 Intenção da Tela
Permitir **consulta completa e segura** de um perfil de acesso, incluindo permissões e usuários vinculados.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Painel Informações Gerais | InfoPanel | Dados do perfil (Nome, Descrição, Tipo, Status) |
| CMP-WF04-002 | Badge "Perfil de Sistema" | Badge | Indicador visual se IsSystemRole = true |
| CMP-WF04-003 | Badge Status | Badge | Ativo/Inativo com cores (verde/vermelho) |
| CMP-WF04-004 | Painel Permissões | PermissionList | Lista de permissões agrupadas por módulo (read-only) |
| CMP-WF04-005 | Badge "Crítica" | Badge | Indicador em permissões críticas |
| CMP-WF04-006 | Painel Usuários Vinculados | CounterPanel | Contagem + link para lista de usuários |
| CMP-WF04-007 | Link "Ver Usuários" | Link | Redireciona para lista de usuários com filtro no perfil |
| CMP-WF04-008 | Painel Auditoria | InfoPanel | Created, CreatedBy, LastModified, LastModifiedBy |
| CMP-WF04-009 | Botão Editar | Button | Ação primária para editar (se tiver permissão) |
| CMP-WF04-010 | Botão Voltar | Button | Retornar para listagem |
| CMP-WF04-011 | Link "Ver Histórico Completo" | Link | Redireciona para RF-004 (Auditoria) |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Clique em Editar | Usuário clica em CMP-WF04-009 | UC03 | FA-UC02-01 |
| EVT-WF04-002 | Clique em Voltar | Usuário clica em CMP-WF04-010 | UC00 | Retorna listagem |
| EVT-WF04-003 | Clique em Ver Usuários | Usuário clica em CMP-WF04-007 | - | Redireciona RF012 filtrado |
| EVT-WF04-004 | Clique em Ver Histórico | Usuário clica em CMP-WF04-011 | - | FA-UC02-02 |

### 7.4 Conteúdos Obrigatórios

#### Painel 1: Informações Gerais
- Nome do Perfil (com badge "Sistema" se aplicável)
- Descrição
- Tipo (Sistema/Personalizado)
- Status (Ativo/Inativo com badge colorido)
- Criado em (timestamp legível: "01/01/2026 às 14:30")
- Criado por (nome do usuário)
- Última modificação (timestamp + usuário)

#### Painel 2: Permissões
- Lista agrupada por módulo (CONTRATOS, FATURAS, USUARIOS, etc.)
- Cada permissão exibida como:
  - Código: `contratos:contrato:view`
  - Descrição: "Visualizar contratos"
  - Badge "Crítica" se Fl_Critica = true
- Total de permissões no cabeçalho: "Permissões (23)"
- Campo de busca para filtrar permissões exibidas

#### Painel 3: Usuários Vinculados
- Contagem de usuários ativos com este perfil
- Exemplo: "15 usuários vinculados a este perfil"
- Link "Ver usuários" (redireciona para RF012 com filtro RoleId)
- Se 0 usuários: Mensagem "Nenhum usuário vinculado"

### 7.5 Estados Obrigatórios

#### Estado 1: Carregando (Loading)
**Quando:** Dados do perfil sendo carregados
**Exibir:**
- Skeleton loader dos 3 painéis
- Mensagem: "Carregando perfil..."

#### Estado 2: Dados Carregados (Sucesso)
**Quando:** API retorna dados completos
**Exibir:**
- 3 painéis preenchidos com dados
- Botão Editar visível se usuário tiver permissão `perfis:perfil:update`
- Permissões agrupadas por módulo (collapsed por padrão, expandir ao clicar)

#### Estado 3: Erro ao Carregar Perfil
**Quando:** API retorna 404 (perfil não encontrado ou de outro tenant)
**Exibir:**
- Mensagem: "Perfil não encontrado"
- Botão "Voltar para Listagem"
- Redirecionamento automático após 3 segundos

#### Estado 4: Erro ao Carregar Permissões
**Quando:** JOIN RolePermission falha
**Exibir:**
- Painéis 1 e 3 carregados normalmente
- Painel 2 (Permissões) com mensagem: "Erro ao carregar permissões. Tente recarregar a página."
- Botão "Recarregar Permissões"
- Log técnico registrado

### 7.6 Contratos de Comportamento

#### Isolamento Multi-Tenancy
- Perfil só é visível se:
  - Pertence ao tenant do usuário (EmpresaId = @EmpresaId), OU
  - É perfil de sistema (EmpresaId IS NULL)
- Tentativa de acessar perfil de outro tenant retorna 404

#### Permissões Visuais
- Botão Editar visível apenas se `perfis:perfil:update`
- Super Admin pode visualizar qualquer perfil (bypass de isolamento)

#### Responsividade

- **Mobile:**
  - 3 painéis empilhados verticalmente
  - Permissões em accordions por módulo
  - Botões empilhados

- **Tablet:**
  - Painel 1 e 2 lado a lado
  - Painel 3 embaixo (full-width)

- **Desktop:**
  - Layout em 2 colunas:
    - Esquerda: Painel 1 (Gerais) + Painel 3 (Usuários)
    - Direita: Painel 2 (Permissões - altura completa)

#### Acessibilidade (WCAG AA)
- Headings semânticos (h2 para painéis, h3 para módulos de permissões)
- Badges com texto alternativo ("Perfil de Sistema", "Ativo")
- Links descritivos ("Ver 15 usuários vinculados")
- Navegação por teclado

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO DE PERFIL

### 8.1 Intenção
Evitar exclusões acidentais e comunicar consequências da ação destrutiva.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Modal de Confirmação | Modal | Dialog modal com foco trap |
| CMP-WF05-002 | Título | Heading | "Confirmar Exclusão" |
| CMP-WF05-003 | Mensagem | Text | "Tem certeza que deseja excluir o perfil '{Nome}'?" |
| CMP-WF05-004 | Submensagem | Text | "Esta ação é irreversível." |
| CMP-WF05-005 | Botão Confirmar | Button | Ação destrutiva (vermelho) |
| CMP-WF05-006 | Botão Cancelar | Button | Ação secundária (padrão) |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Confirmação | Usuário clica em CMP-WF05-005 | UC04 | FP-UC04-004 |
| EVT-WF05-002 | Cancelamento | Usuário clica em CMP-WF05-006 | UC04 | FA-UC04-01 |
| EVT-WF05-003 | Fechar Modal | Usuário clica fora do modal ou pressiona Esc | UC04 | FA-UC04-01 |

### 8.4 Estados Obrigatórios

#### Estado 1: Modal Aberto (Inicial)
**Quando:** Usuário clica "Excluir" na listagem
**Exibir:**
- Modal sobreposto à tela
- Foco automático no botão Cancelar (segurança)
- Backdrop escuro (overlay)
- Mensagem clara com nome do perfil

#### Estado 2: Excluindo (Loading)
**Quando:** Usuário confirma exclusão
**Exibir:**
- Spinner no botão Confirmar
- Mensagem: "Excluindo perfil..."
- Botões desabilitados

#### Estado 3: Sucesso
**Quando:** API retorna 200 OK (soft delete bem-sucedido)
**Exibir:**
- Modal fecha automaticamente
- Toast: "Perfil '{Nome}' excluído com sucesso!"
- Perfil removido da listagem (WF-01)

#### Estado 4: Erro - Perfil com Usuários Vinculados
**Quando:** API retorna 400 (RN-RF013-08 violada)
**Exibir:**
- Modal permanece aberto
- Alert de erro substituindo mensagem original
- Mensagem: "Não é possível excluir este perfil pois existem {N} usuário(s) vinculado(s). Remova os usuários deste perfil antes de excluí-lo."
- Link "Ver usuários vinculados" (redireciona para RF012 filtrado)
- Botão Confirmar desabilitado
- Botão "Fechar" (substitui Cancelar)

#### Estado 5: Erro - Perfil Não Encontrado
**Quando:** API retorna 404 (perfil já excluído ou de outro tenant)
**Exibir:**
- Modal fecha
- Toast de erro: "Perfil não encontrado ou já foi excluído"
- Recarregar listagem (WF-01)

### 8.5 Regras

#### Validação Pré-Exclusão
- Sistema DEVE verificar usuários vinculados ANTES de permitir exclusão
- Contagem de usuários DEVE ser exibida na mensagem de erro
- Perfil de outro tenant retorna 404 (não revelar existência)

#### Exclusão Lógica (Soft Delete)
- Sistema atualiza Fl_Ativo = 0 (nunca DELETE físico)
- LastModified e LastModifiedBy atualizados automaticamente
- Auditoria registrada com ação "Deleted" e IP do usuário
- Cache de permissões invalidado

#### Confirmação Obrigatória
- Modal com foco trap (Tab circula entre Confirmar/Cancelar)
- Esc fecha modal (equivale a Cancelar)
- Clicar fora do modal fecha (equivale a Cancelar)
- Foco inicial no botão Cancelar (segurança UX)

#### Responsividade

- **Mobile:**
  - Modal full-screen
  - Botões empilhados verticalmente

- **Tablet/Desktop:**
  - Modal centralizado (max-width 500px)
  - Botões inline (Cancelar à esquerda, Confirmar à direita)

#### Acessibilidade (WCAG AA)
- Aria-role="alertdialog"
- Aria-labelledby="modal-title"
- Aria-describedby="modal-message"
- Foco trap (Tab não sai do modal)
- Esc fecha modal
- Botão Confirmar com cor de alerta (vermelho) e texto contrastante

---

## 9. WF-06 — GERENCIAR PERMISSÕES DO PERFIL

### 9.1 Intenção da Tela
Permitir **atribuição e remoção granular de permissões**, com destaque visual e validação para permissões críticas.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Painel Permissões Disponíveis | PermissionTreeView | Árvore de permissões agrupadas por módulo |
| CMP-WF06-002 | Campo Busca | Input | Busca por nome ou código de permissão |
| CMP-WF06-003 | Checkbox Master por Módulo | Checkbox | Selecionar/desmarcar todas as permissões do módulo |
| CMP-WF06-004 | Checkbox Permissão | Checkbox | Selecionar/desmarcar permissão individual |
| CMP-WF06-005 | Badge "Crítica" | Badge | Indicador visual vermelho/laranja em permissões críticas |
| CMP-WF06-006 | Tooltip Descrição | Tooltip | Descrição detalhada ao passar mouse sobre permissão |
| CMP-WF06-007 | Campo Justificativa | Textarea | Obrigatório quando permissão crítica é adicionada (min 20 caracteres) |
| CMP-WF06-008 | Contador Permissões | Counter | "X permissões selecionadas" |
| CMP-WF06-009 | Botão Salvar Permissões | Button | Ação primária para persistir alterações |
| CMP-WF06-010 | Botão Cancelar | Button | Descartar alterações |
| CMP-WF06-011 | Alert Permissão Crítica | Alert | "Permissões críticas exigem justificativa detalhada" |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Selecionar Permissão | Usuário marca checkbox CMP-WF06-004 | UC05 | FP-UC05-004 |
| EVT-WF06-002 | Desmarcar Permissão | Usuário desmarca checkbox CMP-WF06-004 | UC05 | FP-UC05-004 |
| EVT-WF06-003 | Checkbox Master | Usuário marca/desmarca CMP-WF06-003 | UC05 | FA-UC05-01 |
| EVT-WF06-004 | Buscar Permissão | Usuário digita em CMP-WF06-002 | UC05 | FA-UC05-02 |
| EVT-WF06-005 | Ver Descrição | Usuário passa mouse sobre permissão | UC05 | FA-UC05-03 |
| EVT-WF06-006 | Permissão Crítica Selecionada | Sistema detecta permissão crítica marcada | UC05 | FP-UC05-006, FP-UC05-007 |
| EVT-WF06-007 | Salvar Permissões | Usuário clica em CMP-WF06-009 | UC05 | FP-UC05-008 |
| EVT-WF06-008 | Cancelar | Usuário clica em CMP-WF06-010 | UC05 | Descarta alterações |

### 9.4 Ações Permitidas
- Selecionar/desmarcar permissões individuais
- Selecionar/desmarcar todas as permissões de um módulo
- Buscar permissão por nome ou código
- Ver descrição detalhada em tooltip
- Adicionar justificativa para permissões críticas
- Salvar alterações (DELETE + INSERT RolePermission)

### 9.5 Estados Obrigatórios

#### Estado 1: Carregando Permissões (Loading)
**Quando:** Catálogo de permissões sendo carregado
**Exibir:**
- Skeleton loader da árvore de permissões
- Mensagem: "Carregando permissões disponíveis..."

#### Estado 2: Permissões Carregadas (Inicial)
**Quando:** Catálogo carregado com sucesso
**Exibir:**
- Árvore de permissões agrupadas por módulo (collapsed por padrão)
- Permissões atuais do perfil já marcadas
- Contador: "X permissões selecionadas"
- Botão Salvar desabilitado (sem alterações)

#### Estado 3: Permissões Alteradas
**Quando:** Usuário marca/desmarca qualquer permissão
**Exibir:**
- Permissões adicionadas: checkbox com borda verde + ícone "+"
- Permissões removidas: checkbox desmarcado com borda vermelha + ícone "-"
- Contador atualizado
- Botão Salvar habilitado

#### Estado 4: Permissão Crítica Selecionada
**Quando:** Usuário marca checkbox de permissão com Fl_Critica = true
**Exibir:**
- Badge "Crítica" destacado em vermelho/laranja
- Alert aparece: "Permissões críticas exigem justificativa detalhada"
- Campo Justificativa aparece dinamicamente (slide-in)
- Contador de caracteres: "0/20 caracteres (mínimo 20)"
- Botão Salvar desabilitado até justificativa válida

#### Estado 5: Salvando (Loading)
**Quando:** Requisição PUT/POST enviada ao backend
**Exibir:**
- Spinner no botão Salvar
- Árvore de permissões desabilitada (overlay)
- Mensagem: "Salvando permissões..."

#### Estado 6: Sucesso
**Quando:** API retorna 200 OK
**Exibir:**
- Toast: "Permissões atualizadas com sucesso!"
- Cache de permissões invalidado (não visível ao usuário)
- Notificação ao gestor enviada assincronamente (se permissão crítica foi atribuída)
- Atualizar auditoria (LastModified, LastModifiedBy)
- Botão Salvar desabilitado (sem alterações pendentes)

#### Estado 7: Erro - Permissão Crítica Sem Justificativa
**Quando:** API retorna 400 (RN-RF013-05 violada)
**Exibir:**
- Alert de erro: "Justificativa obrigatória para permissões críticas"
- Campo Justificativa destacado em vermelho
- Foco automático no campo Justificativa

#### Estado 8: Erro - Formato Inválido
**Quando:** API valida formato de permissão inválido
**Exibir:**
- Alert de erro: "Formato de permissão inválido: deve ser modulo:recurso:acao"
- Permissão com erro destacada

### 9.6 Contratos de Comportamento

#### Catálogo de Permissões
- Permissões agrupadas por módulo: CONTRATOS, FATURAS, USUARIOS, PERFIS, AUDITORIA, etc.
- Cada módulo colapsável (accordion)
- Permissões ordenadas alfabeticamente dentro do módulo

#### Permissões Críticas (lista obrigatória)
- `usuarios:usuario:*` (qualquer ação em usuários)
- `perfis:perfil:*` (qualquer ação em perfis)
- `contratos:contrato:approve` (aprovação de contratos)
- `faturas:fatura:import` (importação de faturas)

#### Validações
- Formato de permissão: `modulo:recurso:acao` (regex obrigatório)
- Justificativa: mínimo 20 caracteres se permissão crítica
- Permissões duplicadas ignoradas automaticamente

#### Auditoria
- Registro detalhado: usuário, timestamp, permissão, ação (add/remove), justificativa, IP
- Estado anterior e novo estado registrados
- Justificativa associada à permissão no log de auditoria

#### Notificações
- Notificação ao gestor enviada assincronamente se permissão crítica atribuída
- Não bloqueia operação de salvamento

#### Cache
- Cache de permissões invalidado imediatamente após salvamento
- Usuários afetados precisam relogar ou cache expira automaticamente

#### Responsividade

- **Mobile:**
  - Árvore de permissões em accordions
  - Busca no topo (fixa)
  - Checkbox Master por módulo
  - Botões empilhados

- **Tablet:**
  - Árvore de permissões em 2 colunas
  - Busca inline
  - Botões inline

- **Desktop:**
  - Árvore de permissões em 3 colunas (módulos lado a lado)
  - Busca com filtro em tempo real
  - Contador fixo no topo
  - Botões no rodapé (sticky)

#### Acessibilidade (WCAG AA)
- Aria-expanded em módulos colapsáveis
- Aria-checked em checkboxes
- Tooltip acessível via keyboard (Shift+Tab)
- Contraste de cores em badges de permissão crítica
- Screen reader anuncia alterações no contador

---

## 10. WF-07 — DUPLICAR PERFIL DE ACESSO

### 10.1 Intenção da Tela
Permitir **criação rápida de novo perfil baseado em perfil existente**, copiando todas as permissões.

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Modal Duplicar | Modal | Dialog modal com foco trap |
| CMP-WF07-002 | Título | Heading | "Duplicar Perfil" |
| CMP-WF07-003 | Mensagem | Text | "Criar novo perfil baseado em '{Nome Original}'" |
| CMP-WF07-004 | Campo Novo Nome | Input | Nome do novo perfil (pré-preenchido: "{Nome} - Cópia") |
| CMP-WF07-005 | Campo Descrição | Textarea | Descrição pré-preenchida: "{Descrição original} (cópia)" |
| CMP-WF07-006 | Mensagem Informativa | Text | "Todas as permissões do perfil original serão copiadas." |
| CMP-WF07-007 | Botão Duplicar | Button | Ação primária (verde) |
| CMP-WF07-008 | Botão Cancelar | Button | Ação secundária |
| CMP-WF07-009 | Mensagem de Erro | Alert | Exibe erros de validação (nome duplicado, etc.) |

### 10.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF07-001 | Abrir Modal | Usuário clica "Duplicar" na listagem | UC06 | FP-UC06-002 |
| EVT-WF07-002 | Confirmar Duplicação | Usuário clica em CMP-WF07-007 | UC06 | FP-UC06-005 |
| EVT-WF07-003 | Cancelar | Usuário clica em CMP-WF07-008 | UC06 | FA-UC06-01 |
| EVT-WF07-004 | Validação Nome | Sistema valida nome único | UC06 | FP-UC06-006 |
| EVT-WF07-005 | Erro Nome Duplicado | API retorna 400 | UC06 | FE-UC06-01 |
| EVT-WF07-006 | Erro Perfil Origem | API retorna 404 | UC06 | FE-UC06-02 |
| EVT-WF07-007 | Erro Copiar Permissões | API retorna 500 (rollback) | UC06 | FE-UC06-03 |

### 10.4 Estados Obrigatórios

#### Estado 1: Modal Aberto (Inicial)
**Quando:** Usuário clica "Duplicar" na listagem
**Exibir:**
- Modal sobreposto à tela
- Campo Novo Nome pré-preenchido: "{Nome Original} - Cópia"
- Campo Descrição pré-preenchido: "{Descrição} (cópia)"
- Mensagem informativa sobre cópia de permissões
- Foco automático no campo Novo Nome (cursor ao final)
- Botão Duplicar habilitado

#### Estado 2: Duplicando (Loading)
**Quando:** Usuário confirma duplicação
**Exibir:**
- Spinner no botão Duplicar
- Mensagem: "Duplicando perfil e copiando permissões..."
- Formulário desabilitado

#### Estado 3: Sucesso
**Quando:** API retorna 201 Created (perfil + permissões criados)
**Exibir:**
- Modal fecha automaticamente
- Toast: "Perfil '{Novo Nome}' criado com sucesso!"
- Redirecionar para edição do novo perfil (WF-03)

#### Estado 4: Erro - Nome Duplicado
**Quando:** API retorna 400 (nome já existe no tenant)
**Exibir:**
- Modal permanece aberto
- Alert de erro: "Já existe um perfil com este nome"
- Campo Novo Nome destacado em vermelho
- Foco no campo Novo Nome
- Botão Duplicar permanece habilitado (retry)

#### Estado 5: Erro - Perfil Origem Não Encontrado
**Quando:** API retorna 404 (perfil origem excluído ou de outro tenant)
**Exibir:**
- Modal fecha
- Toast de erro: "Perfil de origem não encontrado"
- Recarregar listagem (WF-01)

#### Estado 6: Erro - Falha ao Copiar Permissões
**Quando:** Transação falha (INSERT RolePermission falha)
**Exibir:**
- Modal permanece aberto
- Alert de erro: "Erro ao copiar permissões. Operação cancelada. Tente novamente."
- Rollback automático (perfil não criado)
- Log técnico registrado

### 10.5 Contratos de Comportamento

#### Validações
- Nome único por tenant (case-insensitive)
- Nome obrigatório (não vazio)
- Descrição opcional (max 500 caracteres)

#### Operação Transacional
- Criação do perfil (INSERT Role) e cópia de permissões (INSERT RolePermission SELECT) em transação única
- Rollback automático se qualquer etapa falhar
- Integridade garantida (perfil + permissões ou nada)

#### Regras de Negócio
- Novo perfil sempre personalizado (IsSystemRole = false)
- EmpresaId sempre do tenant do usuário (nunca NULL)
- Fl_Ativo = 1 (ativo)
- Created, CreatedBy preenchidos automaticamente
- Permissões copiadas 1:1 do perfil origem

#### Redirecionamento
- Após sucesso, redirecionar para WF-03 (Editar) com ID do novo perfil
- Permitir ajustes imediatos antes de usar

#### Responsividade

- **Mobile:**
  - Modal full-screen
  - Campos empilhados
  - Botões empilhados

- **Tablet/Desktop:**
  - Modal centralizado (max-width 600px)
  - Campos inline
  - Botões inline (Cancelar à esquerda, Duplicar à direita)

#### Acessibilidade (WCAG AA)
- Aria-role="dialog"
- Aria-labelledby="modal-title"
- Foco trap (Tab circula entre campos e botões)
- Esc fecha modal (equivale a Cancelar)
- Botão Duplicar com cor destacada (verde) e texto contrastante

---

## 11. NOTIFICAÇÕES

### 11.1 Tipos Padronizados

| Tipo | Uso | Cor | Duração |
|----|----|-----|---------|
| Sucesso | Operação concluída (criar, editar, excluir, duplicar) | Verde | 3s |
| Erro | Falha bloqueante (validação, servidor, permissão) | Vermelho | 5s (fecha manual) |
| Aviso | Atenção necessária (permissão crítica, cache invalidado) | Amarelo/Laranja | 4s |
| Info | Feedback neutro (dados carregados, filtro aplicado) | Azul | 2s |

### 11.2 Mensagens Obrigatórias

| Contexto | Mensagem |
|-------|----------|
| Perfil criado | "Perfil '{Nome}' criado com sucesso!" |
| Perfil editado | "Perfil '{Nome}' atualizado com sucesso!" |
| Perfil excluído | "Perfil '{Nome}' excluído com sucesso!" |
| Perfil duplicado | "Perfil '{Novo Nome}' criado com sucesso!" |
| Nome duplicado | "Já existe um perfil com este nome nesta empresa" |
| Perfil com usuários | "Não é possível excluir este perfil pois existem {N} usuário(s) vinculado(s)" |
| Permissão crítica sem justificativa | "Justificativa obrigatória para permissões críticas" |
| Erro genérico | "Erro ao {ação}. Tente novamente." |

---

## 12. RESPONSIVIDADE (OBRIGATÓRIO)

### 12.1 Breakpoints

| Contexto | Largura | Comportamento |
|-------|---------|---------------|
| Mobile | < 768px | Layout em coluna, componentes empilháveis |
| Tablet | 768px - 1024px | Layout híbrido, 2 colunas |
| Desktop | > 1024px | Layout completo, 3 colunas |

### 12.2 Adaptações por Tela

#### WF-01 (Listagem)
- **Mobile:** Cards verticais com ações em dropdown
- **Tablet:** Tabela simplificada (4 colunas)
- **Desktop:** Tabela completa (6 colunas)

#### WF-02/WF-03 (Criar/Editar)
- **Mobile:** Formulário coluna única, permissões em accordions
- **Tablet:** 2 colunas (dados gerais + permissões)
- **Desktop:** 2 painéis lado a lado

#### WF-04 (Visualizar)
- **Mobile:** 3 painéis empilhados verticalmente
- **Tablet:** Painel 1+2 lado a lado, Painel 3 embaixo
- **Desktop:** 2 colunas (Painel 1+3 à esquerda, Painel 2 à direita)

#### WF-05/WF-07 (Modais)
- **Mobile:** Full-screen
- **Tablet/Desktop:** Centralizado (max-width definido)

---

## 13. ACESSIBILIDADE (OBRIGATÓRIO)

### 13.1 Padrões WCAG AA

| Critério | Implementação |
|-------|---------------|
| Navegação por teclado | Tab (navegar), Shift+Tab (voltar), Enter (ativar), Esc (cancelar) |
| Screen readers | ARIA labels, roles, descriptions em todos os componentes |
| Contraste mínimo | 4.5:1 em textos, 3:1 em componentes UI |
| Labels descritivos | Português claro, sem jargões técnicos |
| Foco visível | Outline destacado em elementos focados |
| Estados anunciados | Loading, erro, sucesso anunciados por screen reader |

### 13.2 ARIA Obrigatório

| Componente | ARIA |
|-------|------|
| Tabela | role="table", aria-label="Tabela de perfis de acesso" |
| Botão Editar | aria-label="Editar perfil {Nome}" |
| Checkbox Permissão | aria-checked="true/false", aria-describedby="permission-description" |
| Modal | role="dialog/alertdialog", aria-labelledby, aria-describedby |
| Alert | role="alert", aria-live="assertive" |
| Loading | aria-live="polite", aria-busy="true" |

---

## 14. RASTREABILIDADE

| Wireframe | UC(s) | RF | Regras de Negócio Cobertas |
|---------|----|----|----------------------------|
| WF-01 | UC00 | RF013 | RN-RF013-01, RN-RF013-10 |
| WF-02 | UC01 | RF013 | RN-RF013-01, RN-RF013-02, RN-RF013-04, RN-RF013-09 |
| WF-03 | UC03 | RF013 | RN-RF013-01, RN-RF013-02, RN-RF013-05, RN-RF013-07, RN-RF013-09 |
| WF-04 | UC02 | RF013 | RN-RF013-03, RN-RF013-10 |
| WF-05 | UC04 | RF013 | RN-RF013-08, RN-RF013-09, RN-RF013-10 |
| WF-06 | UC05 | RF013 | RN-RF013-04, RN-RF013-05, RN-RF013-06, RN-RF013-07 |
| WF-07 | UC06 | RF013 | RN-RF013-01, RN-RF013-09 |

**Cobertura Total: 7 Wireframes cobrindo 7 UCs cobrindo 10 Regras de Negócio (100%)**

---

## 15. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, tipografia, espaçamentos exatos)
- Escolha de framework (Filament, React, Vue, Angular)
- Design gráfico definitivo (ilustrações, ícones específicos)
- Animações avançadas (transitions, microinterações)
- Implementação técnica (componentes, classes CSS, JavaScript)

**Este documento define contratos comportamentais e visuais, não implementação.**

---

## 16. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 1.0 | 2026-01-04 | Agência ALC - alc.dev.br | Criação completa dos wireframes do RF013 com 7 telas cobrindo 100% dos UCs |

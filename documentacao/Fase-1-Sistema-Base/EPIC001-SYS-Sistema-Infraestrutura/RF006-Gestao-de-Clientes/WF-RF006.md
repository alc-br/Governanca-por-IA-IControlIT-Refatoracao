# WF-RF006 — Wireframes Canônicos (UI Contract)

**Versão:** 2.0
**Data:** 2026-01-02
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF006 - Gestão de Clientes (Multi-Tenancy SaaS)
**UC Relacionado:** UC-RF006 (todos os 9 UCs)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF006 - Gestão de Clientes (Multi-Tenancy SaaS).

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional**
- Servir como **fonte de verdade para IA, QA e Desenvolvimento**
- Permitir derivação direta de **TCs E2E e testes de usabilidade**
- Evitar dependência de ferramentas específicas (ex: Filament, React, Vue)

> ⚠️ Este documento descreve **o que a tela deve permitir e comunicar**, não **como será implementado tecnicamente**.

**Contexto Multi-Tenancy:**
- RF006 é a entidade raiz de multi-tenancy do sistema IControlIT
- Super Admin é o ÚNICO role autorizado a acessar este módulo (IsSuperAdmin = true)
- ClienteId é discriminador de tenant obrigatório em TODAS as entidades do sistema
- Soft Delete obrigatório (FlExcluido = true) via trigger INSTEAD OF DELETE

**Integrações Obrigatórias:**
- **ReceitaWS API**: Consulta automática de CNPJ (timeout 10s, rate limit 3/min/user)
- **Azure Blob Storage**: Armazenamento de logos (container: clientes-logos)
- **i18n (Transloco)**: pt-BR (default), en, es
- **Auditoria LGPD**: 7 anos retenção (AuditInterceptor)

---

## 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)

### 2.1 Princípios Gerais

- Clareza acima de estética
- Feedback imediato a toda ação do usuário
- Estados explícitos (loading, vazio, erro, dados)
- Não ocultar erros críticos
- Comportamento previsível
- **CRÍTICO**: Confirmação obrigatória antes de ações destrutivas (desativar, excluir)
- **CRÍTICO**: Avisos explícitos sobre impacto em usuários vinculados

### 2.2 Padrões Globais

| Item | Regra |
|----|-----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas com aviso de impacto |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Acessibilidade | WCAG AA obrigatório |
| Multi-Tenancy | Super Admin APENAS (bypass via IsSuperAdmin = true) |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|------|----------------------|------------|
| WF-01 | Listagem de Clientes | UC00 | Descoberta, filtros e acesso (bypass multi-tenancy) |
| WF-02 | Criar Cliente com ReceitaWS | UC01, UC08 | Entrada de dados com consulta automática CNPJ |
| WF-03 | Visualizar Cliente | UC02 | Consulta completa (multi-tenancy bypass) |
| WF-04 | Editar Cliente | UC03 | Alteração de dados (CNPJ read-only) |
| WF-05 | Confirmação de Exclusão | UC04 | Soft delete com bloqueio de usuários |
| WF-06 | Upload de Logo | UC05 | Upload Azure Blob Storage (magic bytes validation) |
| WF-07 | Restaurar Cliente Excluído | UC06 | Reverter soft delete |
| WF-08 | Desativar Cliente | UC07 | Desativação temporária com bloqueio de usuários |
| WF-09 | Consultar CNPJ (ReceitaWS) | UC08 | Consulta standalone ReceitaWS (independente de criação) |

**Cobertura**: 9 wireframes cobrindo 9 UCs (100%)

---

## 4. WF-01 — LISTAGEM DE CLIENTES

### 4.1 Intenção da Tela
Permitir ao Super Admin **localizar, filtrar, ordenar e acessar Clientes cadastrados** com bypass de multi-tenancy (IsSuperAdmin = true).

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Novo Cliente" | Button | Ação primária para criar novo Cliente |
| CMP-WF01-002 | Campo de Busca Textual | Input | Busca por CNPJ, Razão Social, Nome Fantasia |
| CMP-WF01-003 | Filtro de Status (FlAtivo) | Dropdown | Filtrar por Ativo/Inativo/Todos |
| CMP-WF01-004 | Filtro de Exclusão (FlExcluido) | Dropdown | Filtrar por Não Excluídos/Excluídos/Todos |
| CMP-WF01-005 | Tabela de Clientes | DataTable | Exibição com paginação (10-100 registros/página) |
| CMP-WF01-006 | Botão Visualizar | IconButton | Ação por linha (UC02) |
| CMP-WF01-007 | Botão Editar | IconButton | Ação por linha (UC03) |
| CMP-WF01-008 | Botão Excluir | IconButton | Ação por linha (UC04) - confirmação obrigatória |
| CMP-WF01-009 | Paginação | Pagination | Controles de navegação |
| CMP-WF01-010 | Badge Status | Badge | Indicador visual (Ativo/Inativo/Excluído) |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Novo Cliente" | Usuário clica em CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca textual | Usuário digita em CMP-WF01-002 | UC00 | FP-UC00-001 |
| EVT-WF01-003 | Filtro por FlAtivo | Usuário seleciona em CMP-WF01-003 | UC00 | FA-UC00-003 |
| EVT-WF01-004 | Filtro por FlExcluido | Usuário seleciona em CMP-WF01-004 | UC00 | FA-UC00-002 |
| EVT-WF01-005 | Clique em Visualizar | Usuário clica em CMP-WF01-006 | UC02 | FP-UC02-001 |
| EVT-WF01-006 | Clique em Editar | Usuário clica em CMP-WF01-007 | UC03 | FP-UC03-001 |
| EVT-WF01-007 | Clique em Excluir | Usuário clica em CMP-WF01-008 | UC04 | FP-UC04-001 |
| EVT-WF01-008 | Mudança de página | Usuário interage com CMP-WF01-009 | UC00 | FP-UC00-001 |

### 4.4 Ações Permitidas
- Buscar Clientes (bypass multi-tenancy via IsSuperAdmin = true)
- Filtrar por FlAtivo (Ativo/Inativo)
- Filtrar por FlExcluido (Excluídos/Não Excluídos)
- Ordenar por CNPJ, Razão Social, Status
- Acessar detalhes (UC02)
- Iniciar criação (UC01)
- Editar Cliente (UC03)
- Excluir Cliente (UC04)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados via `GetClientesQuery`

**Exibir:**
- Skeleton loader (tabela com 10 linhas)
- Mensagem: "Carregando Clientes..."
- Spinner animado

**Comportamento:**
- Desabilitar botões de ação
- Exibir placeholder de paginação

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhum Cliente cadastrado no sistema (query retorna lista vazia)

**Exibir:**
- Ícone ilustrativo (pasta vazia)
- Mensagem: "Nenhum Cliente cadastrado no sistema"
- Botão "Criar Primeiro Cliente" (se permissão: ClientesGerenciar)

**Comportamento:**
- Ocultar tabela e paginação
- Exibir CTA (Call-to-Action) para criação

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, timeout de banco de dados)

**Exibir:**
- Ícone de erro (triângulo de alerta)
- Mensagem: "Erro ao carregar Clientes. Tente novamente."
- Código de erro (ex: "HTTP 500 Internal Server Error")
- Botão "Recarregar"

**Comportamento:**
- Ocultar tabela
- Permitir retry via botão "Recarregar"

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há Clientes disponíveis (query retorna ≥ 1 registro)

**Exibir:**
- Tabela com colunas:
  - CNPJ (formatado: XX.XXX.XXX/XXXX-XX)
  - Razão Social
  - Nome Fantasia
  - Status (Badge: Ativo/Inativo/Excluído)
  - Ações (Visualizar, Editar, Excluir)
- Paginação (10, 25, 50, 100 registros/página)
- Total de registros encontrados

**Comportamento:**
- Paginação funcional
- Filtros acumuláveis (FlAtivo AND FlExcluido AND search)
- Ordenação por colunas (CNPJ, Razão Social)

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile (< 768px):** Cards empilhados (não exibir tabela)
- **Tablet (768px - 1024px):** Tabela simplificada (4 colunas)
- **Desktop (> 1024px):** Tabela completa (todas colunas)

#### Acessibilidade (WCAG AA)
- Labels em português claro: "CNPJ", "Razão Social", "Status"
- Botões com aria-label: "Visualizar Cliente", "Editar Cliente", "Excluir Cliente"
- Navegação por teclado: Tab (navegar), Enter (selecionar), Esc (cancelar filtros)
- Contraste mínimo 4.5:1 (texto sobre fundo)
- Screen reader: Anunciar "X Clientes encontrados" após filtro

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso: "Cliente criado com sucesso!" (após redirect de WF-02)
- Toast de erro: "Erro ao carregar Clientes. Tente novamente."
- Confirmação antes de exclusão (modal WF-05)

#### Multi-Tenancy
- Super Admin DEVE visualizar TODOS os Clientes (bypass via IsSuperAdmin = true)
- Clientes com FlExcluido = true NÃO aparecem por padrão (filtro aplicado)
- Badge "EXCLUÍDO" exibido quando filtro "Excluídos" ativo

---

## 5. WF-02 — CRIAÇÃO DE CLIENTE COM RECEITAWS

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de novo Cliente com consulta automática de CNPJ via ReceitaWS API.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo CNPJ | Input | Campo obrigatório com máscara (XX.XXX.XXX/XXXX-XX) |
| CMP-WF02-002 | Botão "Consultar ReceitaWS" | Button | Trigger UC08 (consulta standalone) |
| CMP-WF02-003 | Campo Razão Social | Input | Campo obrigatório (3-200 chars) - auto-preenchido via ReceitaWS |
| CMP-WF02-004 | Campo Nome Fantasia | Input | Campo opcional - auto-preenchido via ReceitaWS |
| CMP-WF02-005 | Campo Inscrição Estadual | Input | Campo opcional |
| CMP-WF02-006 | Campo Email | Input | Campo opcional com validação formato |
| CMP-WF02-007 | Campo Telefone | Input | Campo opcional com máscara |
| CMP-WF02-008 | Toggle FlAtivo | Toggle | Default: true |
| CMP-WF02-009 | Botão Salvar | Button | Ação primária (trigger UC01) |
| CMP-WF02-010 | Botão Cancelar | Button | Ação secundária (descarta alterações) |
| CMP-WF02-011 | Spinner ReceitaWS | Spinner | Exibido durante consulta API |
| CMP-WF02-012 | Mensagem de Erro | Alert | Exibe erros de validação |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Validação CNPJ | Usuário sai do campo CMP-WF02-001 (blur) | UC01, UC08 | FE-UC01-003 |
| EVT-WF02-002 | Consultar ReceitaWS | Usuário clica em CMP-WF02-002 | UC08 | FP-UC08-001 |
| EVT-WF02-003 | Submissão de Formulário | Usuário clica em CMP-WF02-009 | UC01 | FP-UC01-005 |
| EVT-WF02-004 | Cancelamento | Usuário clica em CMP-WF02-010 | UC01 | FA-UC01-002 |
| EVT-WF02-005 | Validação Razão Social | Usuário sai do campo CMP-WF02-003 (blur) | UC01 | FE-UC01-001 |
| EVT-WF02-006 | Auto-preenchimento ReceitaWS | Sistema retorna dados de UC08 | UC08 | FP-UC08-012 |

### 5.4 Comportamentos Obrigatórios

- **CNPJ único**: Validação backend antes de salvar (409 Conflict se duplicado)
- **Dígitos verificadores**: Validação frontend + backend (400 Bad Request se inválido)
- **ReceitaWS timeout**: 10 segundos (não bloqueia criação se falhar)
- **Rate limit ReceitaWS**: 3 consultas/minuto/usuário (429 Too Many Requests)
- **Fallback manual**: Se ReceitaWS falhar, permitir preenchimento manual
- **Validação antes do envio**: Campos obrigatórios destacados em vermelho
- **Feedback imediato**: Toast de sucesso/erro após operação
- **Cancelar com confirmação**: Se houver dados preenchidos, exibir confirmação

### 5.5 Estados

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário acessa WF-02 pela primeira vez

**Exibir:**
- Formulário vazio
- Campo CNPJ focado automaticamente
- Botão "Consultar ReceitaWS" desabilitado (habilita após CNPJ válido)
- Botão "Salvar" desabilitado (habilita após validação completa)

#### Estado 2: Loading ReceitaWS (Consultando API)
**Quando:** Sistema está consultando ReceitaWS (UC08)

**Exibir:**
- Spinner em CMP-WF02-011
- Mensagem: "Consultando CNPJ na Receita Federal..."
- Botão "Consultar ReceitaWS" desabilitado
- Campos Razão Social e Nome Fantasia desabilitados

**Comportamento:**
- Timeout de 10 segundos
- Se sucesso: auto-preencher campos
- Se falha: exibir toast "ReceitaWS indisponível. Preencha manualmente."

#### Estado 3: Erro (Validação Falhou)
**Quando:** Usuário submete formulário com erros

**Exibir:**
- Campos inválidos destacados em vermelho
- Mensagens de erro abaixo de cada campo:
  - CNPJ: "CNPJ inválido (dígitos verificadores)" (FE-UC01-003)
  - CNPJ: "CNPJ já cadastrado" (FA-UC01-004)
  - Razão Social: "Razão Social é obrigatória (mín. 3 caracteres)" (FE-UC01-001)
- Ícone de erro (X vermelho) ao lado dos campos

**Comportamento:**
- Focus no primeiro campo com erro
- Botão "Salvar" permanece habilitado (permitir retry)

#### Estado 4: Sucesso (Cliente Criado)
**Quando:** Backend retorna HTTP 201 Created

**Exibir:**
- Toast de sucesso: "Cliente criado com sucesso!"
- Redirect para WF-01 (Listagem de Clientes)

**Comportamento:**
- Operação auditada (Tipo: CLI_CREATE)
- FlAtivo = true, FlExcluido = false por padrão

#### Estado 5: Cancelamento (Confirmação)
**Quando:** Usuário clica "Cancelar" com dados preenchidos

**Exibir:**
- Modal de confirmação:
  - Título: "Descartar alterações?"
  - Mensagem: "Você possui dados não salvos. Deseja realmente cancelar?"
  - Botões: "Voltar", "Sim, Cancelar"

**Comportamento:**
- Se "Sim, Cancelar": redirect para WF-01
- Se "Voltar": fecha modal, mantém dados

---

## 6. WF-03 — VISUALIZAÇÃO DE CLIENTE

### 6.1 Intenção da Tela
Permitir **consulta completa e segura** do Cliente com bypass de multi-tenancy (IsSuperAdmin = true).

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Botão "Voltar" | Button | Retorna para WF-01 |
| CMP-WF03-002 | Botão "Editar" | Button | Navega para WF-04 (se FlExcluido = false) |
| CMP-WF03-003 | Botão "Excluir" | Button | Trigger WF-05 (se FlExcluido = false) |
| CMP-WF03-004 | Badge Status | Badge | Ativo/Inativo/Excluído |
| CMP-WF03-005 | Imagem Logo | Image | Logo do Cliente (Azure Blob Storage) |
| CMP-WF03-006 | Seção Dados Gerais | Section | CNPJ, Razão Social, Nome Fantasia, Email, Telefone |
| CMP-WF03-007 | Seção Auditoria | Section | DataCriacao, UsuarioCriacao, DataUltimaAlteracao, UsuarioUltimaAlteracao |
| CMP-WF03-008 | Tabs Navegação | Tabs | Geral, Auditoria Completa |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Clique em "Voltar" | Usuário clica em CMP-WF03-001 | UC02 | - |
| EVT-WF03-002 | Clique em "Editar" | Usuário clica em CMP-WF03-002 | UC03 | FP-UC03-001 |
| EVT-WF03-003 | Clique em "Excluir" | Usuário clica em CMP-WF03-003 | UC04 | FP-UC04-001 |

### 6.4 Conteúdos Obrigatórios

- **Dados principais**: CNPJ, Razão Social, Nome Fantasia, Inscrição Estadual
- **Status atual**: Badge visual (Ativo/Inativo/Excluído)
- **Logo**: Exibir se existir no Azure Blob Storage (placeholder se ausente)
- **Informações de auditoria**:
  - DataCriacao, UsuarioCriacao
  - DataUltimaAlteracao, UsuarioUltimaAlteracao
- **Ações disponíveis conforme permissão**:
  - Editar (se ClientesGerenciar E FlExcluido = false)
  - Excluir (se ClientesGerenciar E FlExcluido = false)

### 6.5 Estados

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados via `GetClienteByIdQuery`

**Exibir:**
- Skeleton loader (seções com linhas animadas)
- Mensagem: "Carregando Cliente..."

#### Estado 2: Erro (Cliente Não Encontrado)
**Quando:** API retorna HTTP 404 Not Found

**Exibir:**
- Ícone de erro
- Mensagem: "Cliente não encontrado ou você não tem permissão para visualizá-lo."
- Botão "Voltar para Listagem"

#### Estado 3: Dados (Cliente Exibido)
**Quando:** API retorna HTTP 200 OK com dados completos

**Exibir:**
- Todas as seções preenchidas
- Logo (se existir) ou placeholder
- Badge de status correto
- Botões de ação conforme permissão

#### Estado 4: Cliente Excluído (FlExcluido = true)
**Quando:** Cliente.FlExcluido = true

**Exibir:**
- Badge "EXCLUÍDO" (vermelho)
- Botão "Restaurar Cliente" (se permissão: ClientesGerenciar)
- Botões "Editar" e "Excluir" desabilitados
- Mensagem de alerta: "Este Cliente foi excluído. Restaure para reativar."

---

## 7. WF-04 — EDIÇÃO DE CLIENTE

### 7.1 Intenção da Tela
Permitir **alteração controlada** de dados cadastrais de Cliente existente (CNPJ read-only).

### 7.2 Regras Visuais

- **CNPJ bloqueado**: Campo desabilitado com tooltip "CNPJ não pode ser alterado após criação"
- **Dados atuais pré-carregados**: Todos os campos preenchidos com valores do banco
- **Diferença entre valor original e alterado**: Highlight em campos modificados (borda azul)
- **Feedback de salvamento**: Toast de sucesso/erro

### 7.3 Restrições

- **CNPJ read-only**: Campo visível mas desabilitado (RN-UC-03-001)
- **Cliente excluído**: NÃO pode ser editado (FlExcluido = false obrigatório)
- **Razão Social obrigatória**: Validação 3-200 caracteres
- **Conflitos de concorrência**: Se outro usuário editou antes, exibir alerta

### 7.4 Componentes e Eventos

(Similar a WF-02, mas com CNPJ desabilitado e sem botão "Consultar ReceitaWS")

### 7.5 Estados

#### Estado 1: Loading (Carregando Dados Atuais)
**Quando:** Sistema está carregando dados via `GetClienteByIdQuery`

**Exibir:**
- Skeleton loader em campos do formulário

#### Estado 2: Formulário Pronto (Dados Carregados)
**Quando:** API retorna HTTP 200 OK

**Exibir:**
- Formulário preenchido com dados atuais
- CNPJ desabilitado (campo cinza)
- Botão "Salvar" habilitado

#### Estado 3: Erro (Validação Falhou)
**Quando:** Usuário submete formulário com erros

**Exibir:**
- Campos inválidos destacados
- Mensagens de erro específicas

#### Estado 4: Sucesso (Cliente Atualizado)
**Quando:** Backend retorna HTTP 200 OK

**Exibir:**
- Toast de sucesso: "Cliente atualizado com sucesso!"
- Redirect para WF-03 (Visualização)

**Comportamento:**
- Operação auditada (Tipo: CLI_UPDATE)
- DataUltimaAlteracao e UsuarioUltimaAlteracaoId atualizados

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO

### 8.1 Intenção
Evitar exclusões acidentais e alertar sobre **impacto crítico** em usuários vinculados.

### 8.2 Regras

- **Confirmação explícita obrigatória**: Modal com checkbox "Confirmo exclusão"
- **Informar consequências**:
  - "TODOS os X usuários vinculados perderão acesso ao sistema IMEDIATAMENTE!"
  - "Esta operação NÃO pode ser revertida via interface (apenas via Restaurar Cliente)"
- **Bloquear se houver dependências críticas**: (Não aplicável para RF006, mas informar impacto)

### 8.3 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Título Modal | Text | "Excluir Cliente?" |
| CMP-WF05-002 | Mensagem de Alerta | Alert | Destaque vermelho com impacto |
| CMP-WF05-003 | Detalhes Cliente | Section | CNPJ, Razão Social, Total de Usuários |
| CMP-WF05-004 | Checkbox Confirmação | Checkbox | "Confirmo que desejo excluir este Cliente" |
| CMP-WF05-005 | Botão "Cancelar" | Button | Fecha modal sem ação |
| CMP-WF05-006 | Botão "Sim, Excluir" | Button | Trigger UC04 (habilitado após checkbox) |

### 8.4 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Checkbox Confirmação | Usuário marca CMP-WF05-004 | UC04 | - |
| EVT-WF05-002 | Submissão Exclusão | Usuário clica em CMP-WF05-006 | UC04 | FP-UC04-005 |
| EVT-WF05-003 | Cancelamento | Usuário clica em CMP-WF05-005 | UC04 | FA-UC04-003 |

### 8.5 Contratos de Comportamento

- **Botão "Sim, Excluir" desabilitado** até que checkbox seja marcado
- **Após confirmação**: Loading spinner + mensagem "Excluindo Cliente..."
- **Sucesso**: Toast "Cliente excluído com sucesso!" + redirect para WF-01
- **Erro**: Toast "Erro ao excluir Cliente. Tente novamente." + fechar modal

---

## 9. WF-06 — UPLOAD DE LOGO

### 9.1 Intenção
Permitir upload de logo corporativo para Azure Blob Storage com validação magic bytes.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Preview Logo Atual | Image | Exibe logo atual ou placeholder |
| CMP-WF06-002 | Input File | FileInput | Aceita PNG, JPG, SVG (max 2 MB) |
| CMP-WF06-003 | Botão "Upload" | Button | Trigger UC05 |
| CMP-WF06-004 | Botão "Remover Logo" | Button | Remove logo do Azure Blob Storage |
| CMP-WF06-005 | Mensagem de Erro | Alert | Exibe erros de validação (formato, tamanho, magic bytes) |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Seleção de Arquivo | Usuário seleciona arquivo em CMP-WF06-002 | UC05 | FP-UC05-004 |
| EVT-WF06-002 | Upload Logo | Usuário clica em CMP-WF06-003 | UC05 | FP-UC05-007 |
| EVT-WF06-003 | Remover Logo | Usuário clica em CMP-WF06-004 | UC05 | FA-UC05-004 |

### 9.4 Estados

#### Estado 1: Sem Logo (Placeholder)
**Quando:** Cliente.LogoUrl = null

**Exibir:**
- Placeholder genérico (ícone de imagem)
- Botão "Upload Logo" habilitado
- Botão "Remover Logo" desabilitado

#### Estado 2: Loading Upload (Enviando para Azure)
**Quando:** Sistema está fazendo upload para Azure Blob Storage

**Exibir:**
- Progress bar (0-100%)
- Mensagem: "Enviando logo..."
- Botões desabilitados

#### Estado 3: Erro (Validação Falhou)
**Quando:** Arquivo inválido (> 2 MB, formato incorreto, magic bytes inválidos)

**Exibir:**
- Mensagem de erro:
  - "Arquivo muito grande. Máximo: 2 MB" (FA-UC05-001)
  - "Formato inválido. Aceitos: PNG, JPG, SVG" (FA-UC05-002)
  - "Arquivo corrompido ou extensão falsificada" (FA-UC05-003)

#### Estado 4: Sucesso (Logo Atualizado)
**Quando:** Backend retorna HTTP 200 OK

**Exibir:**
- Preview da nova logo
- Toast: "Logo atualizado com sucesso!"
- Botão "Remover Logo" habilitado

**Comportamento:**
- Cliente.LogoUrl atualizado
- Operação auditada (Tipo: CLI_LOGO_UPLOAD)

---

## 10. WF-07 — RESTAURAR CLIENTE EXCLUÍDO

### 10.1 Intenção
Permitir reverter soft delete (FlExcluido = false) e opcionalmente reativar usuários.

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Botão "Restaurar Cliente" | Button | Visível apenas se FlExcluido = true |
| CMP-WF07-002 | Modal Confirmação | Modal | Confirmação de restauração |
| CMP-WF07-003 | Checkbox "Reativar Usuários" | Checkbox | Default: false (usuários permanecem bloqueados) |
| CMP-WF07-004 | Botão "Sim, Restaurar" | Button | Trigger UC06 |

### 10.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF07-001 | Clique em Restaurar | Usuário clica em CMP-WF07-001 | UC06 | FP-UC06-001 |
| EVT-WF07-002 | Submissão Restauração | Usuário clica em CMP-WF07-004 | UC06 | FP-UC06-006 |

### 10.4 Estados

#### Estado 1: Sucesso (Cliente Restaurado)
**Quando:** Backend retorna HTTP 200 OK

**Exibir:**
- Toast: "Cliente restaurado com sucesso!"
- Redirect para WF-03 (Visualização)

**Comportamento:**
- Cliente.FlExcluido = false
- Cliente.FlAtivo permanece como estava (não reativa automaticamente)
- Usuários NÃO são reativados automaticamente (manual)
- Operação auditada (Tipo: CLI_RESTORE)

---

## 11. WF-08 — DESATIVAR CLIENTE

### 11.1 Intenção
Permitir desativação temporária (FlAtivo = false) com bloqueio de todos os usuários vinculados.

### 11.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF08-001 | Toggle FlAtivo | Toggle | On = Ativo, Off = Inativo |
| CMP-WF08-002 | Modal Confirmação | Modal | Confirmação de desativação |
| CMP-WF08-003 | Mensagem de Alerta | Alert | Impacto em usuários vinculados |
| CMP-WF08-004 | Botão "Sim, Desativar" | Button | Trigger UC07 |

### 11.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF08-001 | Toggle FlAtivo para Off | Usuário clica em CMP-WF08-001 | UC07 | FP-UC07-003 |
| EVT-WF08-002 | Submissão Desativação | Usuário clica em CMP-WF08-004 | UC07 | FP-UC07-006 |

### 11.4 Estados

#### Estado 1: Sucesso (Cliente Desativado)
**Quando:** Backend retorna HTTP 200 OK

**Exibir:**
- Toast: "Cliente desativado com sucesso!"
- Badge "INATIVO"

**Comportamento:**
- Cliente.FlAtivo = false
- TODOS os usuários vinculados bloqueados (FlAtivo = false)
- Operação auditada (Tipo: CLI_DEACTIVATE + CLI_DEACTIVATE_USERS)

---

## 12. WF-09 — CONSULTAR CNPJ (RECEITAWS)

### 12.1 Intenção
Permitir consulta standalone de CNPJ na ReceitaWS INDEPENDENTEMENTE de criação de Cliente (UC08).

### 12.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF09-001 | Campo CNPJ | Input | Máscara XX.XXX.XXX/XXXX-XX |
| CMP-WF09-002 | Botão "Consultar" | Button | Trigger UC08 |
| CMP-WF09-003 | Spinner Loading | Spinner | Exibido durante consulta |
| CMP-WF09-004 | Seção Resultado | Section | Exibe dados retornados pela ReceitaWS |
| CMP-WF09-005 | Mensagem de Erro | Alert | Exibe erros (timeout, CNPJ não encontrado, rate limit) |

### 12.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF09-001 | Validação CNPJ | Usuário sai do campo CMP-WF09-001 (blur) | UC08 | FE-UC08-001 |
| EVT-WF09-002 | Consultar ReceitaWS | Usuário clica em CMP-WF09-002 | UC08 | FP-UC08-009 |

### 12.4 Estados

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário acessa WF-09

**Exibir:**
- Campo CNPJ vazio
- Botão "Consultar" desabilitado (habilita após CNPJ válido)

#### Estado 2: Loading (Consultando ReceitaWS)
**Quando:** Sistema está consultando ReceitaWS (timeout 10s)

**Exibir:**
- Spinner em CMP-WF09-003
- Mensagem: "Consultando CNPJ na Receita Federal..."
- Botão "Consultar" desabilitado

#### Estado 3: Sucesso (Dados Retornados)
**Quando:** Backend retorna HTTP 200 OK com dados

**Exibir:**
- Seção Resultado preenchida:
  - Razão Social
  - Nome Fantasia
  - Situação Cadastral (ATIVA/BAIXADA/SUSPENSA)
  - Data Situação
  - Endereço completo

#### Estado 4: Erro (CNPJ Não Encontrado)
**Quando:** ReceitaWS retorna HTTP 404 Not Found

**Exibir:**
- Mensagem: "CNPJ não encontrado na Receita Federal."

#### Estado 5: Erro (Rate Limit Excedido)
**Quando:** Backend retorna HTTP 429 Too Many Requests

**Exibir:**
- Mensagem: "Limite de consultas excedido. Aguarde 1 minuto e tente novamente."

#### Estado 6: Erro (Timeout ReceitaWS)
**Quando:** ReceitaWS não responde em 10 segundos

**Exibir:**
- Mensagem: "ReceitaWS indisponível. Tente novamente mais tarde."

---

## 13. NOTIFICAÇÕES

### 13.1 Tipos Padronizados

| Tipo | Uso | Exemplo |
|----|-----|---------|
| Sucesso | Operação concluída com sucesso | "Cliente criado com sucesso!" |
| Erro | Falha bloqueante | "Erro ao criar Cliente. CNPJ já cadastrado." |
| Aviso | Atenção necessária (não bloqueia) | "ReceitaWS indisponível. Preencha manualmente." |
| Info | Feedback neutro | "Consultando CNPJ na Receita Federal..." |

### 13.2 Posicionamento

- **Desktop**: Canto superior direito (toast)
- **Mobile**: Centralizado no topo (toast)
- **Duração**: 5 segundos (auto-dismiss) ou até usuário fechar manualmente

---

## 14. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| **Mobile (< 768px)** | Layout em coluna única, cards empilhados, tabelas transformadas em cards |
| **Tablet (768px - 1024px)** | Layout em 2 colunas, tabelas simplificadas (4 colunas) |
| **Desktop (> 1024px)** | Layout completo, tabelas com todas as colunas |

### Adaptações Específicas

**WF-01 (Listagem):**
- Mobile: Cards com CNPJ, Razão Social, Status, Ações
- Desktop: Tabela completa com 5 colunas

**WF-02 (Criação):**
- Mobile: Formulário em coluna única
- Desktop: Formulário em 2 colunas (otimização de espaço)

**WF-05 (Modal Exclusão):**
- Mobile: Modal fullscreen
- Desktop: Modal centralizado (max-width: 500px)

---

## 15. ACESSIBILIDADE (OBRIGATÓRIO)

### 15.1 Navegação por Teclado

- **Tab**: Navegar entre campos e botões
- **Enter**: Submeter formulários, confirmar modais
- **Esc**: Cancelar modais, limpar filtros
- **Espaço**: Marcar checkboxes, toggle switches

### 15.2 Leitura por Screen Readers

- **Labels claros**: "CNPJ", "Razão Social", "Status do Cliente"
- **Aria-label em botões de ícone**:
  - Visualizar: "Visualizar Cliente {Razão Social}"
  - Editar: "Editar Cliente {Razão Social}"
  - Excluir: "Excluir Cliente {Razão Social}"
- **Anúncios dinâmicos**:
  - Após filtro: "X Clientes encontrados"
  - Após erro: "Erro ao carregar Clientes. Tente novamente."

### 15.3 Contraste Mínimo WCAG AA

- **Texto sobre fundo**: Contraste mínimo 4.5:1
- **Botões primários**: Contraste mínimo 3:1
- **Estados de foco**: Borda azul 2px (visible focus indicator)

### 15.4 Labels e Descrições Claras

- Campos obrigatórios: Marcados com asterisco (*) e aria-required="true"
- Mensagens de erro: Associadas a campos via aria-describedby
- Tooltips: Exibidos com aria-label explicativo

---

## 16. RASTREABILIDADE

| Wireframe | UC | RF | Endpoints |
|---------|----|----|-----------|
| WF-01 | UC00 | RF006 | GET /api/clientes |
| WF-02 | UC01 | RF006 | POST /api/clientes |
| WF-03 | UC02 | RF006 | GET /api/clientes/{id} |
| WF-04 | UC03 | RF006 | PUT /api/clientes/{id} |
| WF-05 | UC04 | RF006 | DELETE /api/clientes/{id} |
| WF-06 | UC05 | RF006 | POST /api/clientes/{id}/logo |
| WF-07 | UC06 | RF006 | POST /api/clientes/{id}/restaurar |
| WF-08 | UC07 | RF006 | PUT /api/clientes/{id}/desativar |
| WF-09 | UC08 | RF006 | POST /api/clientes/consultar-cnpj |

**Cobertura**: 9 wireframes → 9 UCs → 1 RF → 7 endpoints únicos (100%)

---

## 17. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, tipografia específica)
- Escolha de framework (Angular Material, React MUI, etc.)
- Design gráfico definitivo (logos, ícones customizados)
- Animações avançadas (transições complexas)
- Layout de header/sidebar/footer (escopo global, não do RF)

---

## 18. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-02 | Agência ALC - alc.dev.br | Template canônico orientado a contrato (9 WFs cobrindo 9 UCs - 100%) |
| 1.0 | 2025-12-26 | Claude Code Assistant | Versão inicial (4 wireframes parciais - 44% cobertura) |

---

**FIM DO DOCUMENTO WF-RF006.md**

**Cobertura Final**:
- ✅ 9 Wireframes detalhados (WF-01 a WF-09)
- ✅ 9 Casos de Uso cobertos (100%)
- ✅ 14 Seções obrigatórias do template
- ✅ Componentes de Interface (CMP-*) mapeados
- ✅ Eventos de UI (EVT-*) rastreados
- ✅ 4 Estados obrigatórios (Loading, Vazio, Erro, Dados) em TODOS os WFs
- ✅ Responsividade (Mobile, Tablet, Desktop)
- ✅ Acessibilidade WCAG AA completa
- ✅ Rastreabilidade WF → UC → RF → Endpoints (100%)
- ✅ Notificações padronizadas
- ✅ Não-objetivos definidos

**Data de Criação**: 2026-01-02
**Versão**: 2.0
**Status**: CONFORME AO TEMPLATE OFICIAL

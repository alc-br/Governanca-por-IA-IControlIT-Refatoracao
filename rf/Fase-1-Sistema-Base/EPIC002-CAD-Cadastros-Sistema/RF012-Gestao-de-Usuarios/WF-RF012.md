# WF-RF012 — Wireframes Canônicos (UI Contract)

**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF012 - Gestão de Usuários do Sistema
**UC Relacionado:** UC-RF012 (UC00, UC01, UC02, UC03, UC04, UC08)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF012 - Gestão de Usuários do Sistema.

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
- Estados explícitos (loading, vazio, erro, dados)
- Não ocultar erros críticos
- Comportamento previsível
- Segurança em ações destrutivas (confirmação dupla)
- Multi-tenancy transparente (usuário vê apenas seu tenant)

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis se o usuário tiver permissão |
| Ações destrutivas | Sempre confirmadas (modal de confirmação) |
| Estados vazios | Devem orientar o usuário e exibir CTA quando aplicável |
| Erros | Devem ser claros, acionáveis e em português |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Acessibilidade | WCAG AA obrigatório |
| Permissões | Botões/ações ocultos se usuário não tiver permissão |
| Multi-tenancy | Apenas dados do tenant atual exibidos |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Usuários | UC00 | Descoberta, filtro e acesso a usuários |
| WF-02 | Criar Usuário | UC01 | Entrada de dados para novo usuário com MFA |
| WF-03 | Editar Usuário | UC03 | Alteração de dados, estados e perfis |
| WF-04 | Visualizar Usuário | UC02 | Consulta detalhada com auditoria |
| WF-05 | Confirmação de Exclusão | UC04 | Soft delete de usuário |
| WF-06 | Gerenciar Perfis de Usuário | UC08 | Atribuição e remoção de perfis |

---

## 4. WF-01 — LISTAGEM DE USUÁRIOS (UC00)

### 4.1 Intenção da Tela
Permitir ao usuário **localizar, filtrar e acessar usuários do sistema** com controle por multi-tenancy e RBAC.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Permissão Necessária |
|----|-----------|------|-----------|---------------------|
| CMP-WF01-001 | Botão "Novo Usuário" | Button | Ação primária para criar novo usuário | CAD.USUARIOS.CREATE |
| CMP-WF01-002 | Campo de Busca | Input | Busca textual por Nome, Email ou Username | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-003 | Filtro de Estado | Dropdown | Filtrar por estado (active, blocked, inactive, deleted) | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-004 | Filtro de Perfil | Dropdown | Filtrar por perfil (role) | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-005 | Tabela de Usuários | DataTable | Exibição dos usuários com paginação | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-006 | Botão Visualizar | IconButton | Ação para visualizar detalhes (cada linha) | CAD.USUARIOS.VIEW |
| CMP-WF01-007 | Botão Editar | IconButton | Ação para editar usuário (cada linha) | CAD.USUARIOS.UPDATE |
| CMP-WF01-008 | Botão Excluir | IconButton | Ação para excluir usuário (cada linha) | CAD.USUARIOS.DELETE |
| CMP-WF01-009 | Paginação | Pagination | Controles de navegação entre páginas | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-010 | Badge de Estado | Badge | Indicador visual do estado do usuário (colorido) | CAD.USUARIOS.VIEW_ANY |
| CMP-WF01-011 | Badge MFA | Icon | Ícone indicando se MFA está ativo | CAD.USUARIOS.VIEW_ANY |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo UC |
|----|--------|---------|----------------|----------|
| EVT-WF01-001 | Clique em "Novo Usuário" | Usuário clica no botão CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca textual | Usuário digita no campo CMP-WF01-002 | UC00 | FA-UC00-01 |
| EVT-WF01-003 | Filtro por estado | Usuário seleciona no dropdown CMP-WF01-003 | UC00 | FA-UC00-02 |
| EVT-WF01-004 | Filtro por perfil | Usuário seleciona no dropdown CMP-WF01-004 | UC00 | FA-UC00-03 |
| EVT-WF01-005 | Clique em Visualizar | Usuário clica em CMP-WF01-006 | UC02 | FP-UC02-001 |
| EVT-WF01-006 | Clique em Editar | Usuário clica em CMP-WF01-007 | UC03 | FP-UC03-001 |
| EVT-WF01-007 | Clique em Excluir | Usuário clica em CMP-WF01-008 | UC04 | FP-UC04-001 |
| EVT-WF01-008 | Mudança de página | Usuário interage com CMP-WF01-009 | UC00 | FP-UC00-004 |

### 4.4 Ações Permitidas
- Visualizar lista de usuários do tenant
- Buscar usuários por nome, email ou username
- Filtrar por estado (active, blocked, inactive, deleted)
- Filtrar por perfil (role)
- Ordenar por colunas (Nome, Email, Estado, Último Login)
- Criar novo usuário (se tiver permissão)
- Visualizar detalhes de usuário
- Editar usuário (se tiver permissão)
- Excluir usuário (se tiver permissão)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados da API
**Exibir:**
- Skeleton loader (tabela com linhas fictícias animadas)
- Mensagem: "Carregando usuários..."
- Desabilitar filtros e busca

**Contratos:**
- Spinner ou skeleton deve ser visível por no mínimo 300ms
- Usuário não pode interagir com a tabela durante loading

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há usuários no tenant ou filtros não retornam resultados
**Exibir:**
- Ícone ilustrativo (usuário com lupa)
- Mensagem primária: "Nenhum usuário cadastrado"
- Mensagem secundária (se filtros aplicados): "Tente ajustar os filtros"
- Botão "Criar Primeiro Usuário" (se tiver permissão CAD.USUARIOS.CREATE e não houver filtros)
- Botão "Limpar Filtros" (se houver filtros aplicados)

**Contratos:**
- Se o tenant não tem nenhum usuário cadastrado, exibir CTA para criar
- Se há usuários mas os filtros não retornaram nada, exibir opção de limpar filtros

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, timeout, rede)
**Exibir:**
- Ícone de erro (vermelho)
- Mensagem principal: "Erro ao carregar usuários"
- Mensagem secundária (código HTTP): "Erro 500: Falha no servidor. Tente novamente em alguns instantes."
- Botão "Tentar Novamente"
- Botão "Reportar Problema" (opcional)

**Contratos:**
- Exibir código HTTP quando disponível
- Permitir retry (tentar novamente)
- Não ocultar erro do usuário

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há usuários disponíveis e carregados com sucesso
**Exibir:**
- Tabela com colunas:
  - Avatar (imagem ou iniciais)
  - Nome Completo
  - Email
  - Username
  - Estado (badge colorido: active=verde, blocked=vermelho, inactive=cinza, deleted=preto)
  - Perfis (lista de badges)
  - MFA Ativo (ícone verde=sim, cinza=não)
  - Último Login (data/hora formatada)
  - Ações (Visualizar, Editar, Excluir)
- Paginação (10, 25, 50, 100 registros por página)
- Total de registros exibido: "Exibindo 1-10 de 47 usuários"
- Filtros e busca habilitados

**Contratos:**
- Apenas usuários do tenant atual (EmpresaId = current_user.EmpresaId)
- Usuários com Estado = deleted não aparecem por padrão (apenas se filtrado explicitamente)
- Ordenação padrão: Nome (A-Z)
- Colunas ordenáveis: Nome, Email, Estado, Último Login

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile (< 768px):**
  - Tabela vira lista de cards empilhados
  - Cada card exibe: Avatar, Nome, Email, Estado, Ações (menu dropdown)
  - Filtros colapsam em menu expansível
- **Tablet (768px - 1024px):**
  - Tabela simplificada: Avatar, Nome, Email, Estado, Ações
  - Paginação reduzida (apenas números, sem "Primeira/Última")
- **Desktop (> 1024px):**
  - Tabela completa com todas as colunas
  - Paginação completa

#### Acessibilidade (WCAG AA)
- Botões com aria-label em português ("Criar novo usuário", "Editar usuário [Nome]", "Excluir usuário [Nome]")
- Navegação por teclado:
  - Tab: navegar entre filtros, busca, ações
  - Enter: ativar botão/ação
  - Esc: fechar modais
- Contraste mínimo 4.5:1 entre texto e fundo
- Labels claros para campos de busca e filtros
- Screen reader anuncia estado da lista ("10 usuários carregados", "Carregando usuários", "Erro ao carregar")

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso após criar/editar/excluir usuário
- Toast de erro se ação falhar
- Confirmação modal antes de exclusão

#### Segurança e Permissões
- Botão "Novo Usuário" oculto se usuário não tiver CAD.USUARIOS.CREATE
- Botão "Editar" oculto se usuário não tiver CAD.USUARIOS.UPDATE
- Botão "Excluir" oculto se usuário não tiver CAD.USUARIOS.DELETE
- HTTP 403 se usuário tentar acessar sem permissão

---

## 5. WF-02 — CRIAÇÃO DE USUÁRIO (UC01)

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de um novo usuário com MFA obrigatório e atribuição de perfis.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF02-001 | Campo Nome | Input | Nome completo do usuário | Sim |
| CMP-WF02-002 | Campo Email | Input | Email único no tenant | Sim |
| CMP-WF02-003 | Campo Username | Input | Username único no tenant (alfanumérico) | Sim |
| CMP-WF02-004 | Campo Senha | Input (password) | Senha forte (8+ chars, maiúscula, número, especial) | Sim |
| CMP-WF02-005 | Campo Confirmar Senha | Input (password) | Confirmação de senha (deve ser idêntica) | Sim |
| CMP-WF02-006 | Indicador de Força da Senha | ProgressBar | Barra visual (fraca, média, forte) | Não |
| CMP-WF02-007 | Campo Perfis | MultiSelect | Seleção de perfis (roles) | Sim |
| CMP-WF02-008 | Toggle MFA | Switch | MFA obrigatório (sempre ativo por padrão) | Não (sempre true) |
| CMP-WF02-009 | Botão Importar do AD | Button | Importar usuários do Active Directory (LDAP) | Não |
| CMP-WF02-010 | Botão Salvar | Button | Ação primária para criar usuário | - |
| CMP-WF02-011 | Botão Cancelar | Button | Ação secundária para cancelar criação | - |
| CMP-WF02-012 | Mensagem de Erro | Alert | Exibe erros de validação (vermelho) | - |
| CMP-WF02-013 | Modal QR Code MFA | Modal | Exibe QR Code TOTP após criação | - |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo UC |
|----|--------|---------|----------------|----------|
| EVT-WF02-001 | Submissão de Formulário | Usuário clica em CMP-WF02-010 | UC01 | FP-UC01-004 |
| EVT-WF02-002 | Cancelamento | Usuário clica em CMP-WF02-011 | UC01 | (Retorna para WF-01) |
| EVT-WF02-003 | Validação de Email | Usuário sai do campo CMP-WF02-002 | UC01 | FP-UC01-005 |
| EVT-WF02-004 | Validação de Username | Usuário sai do campo CMP-WF02-003 | UC01 | FP-UC01-006 |
| EVT-WF02-005 | Validação de Senha | Usuário digita no campo CMP-WF02-004 | UC01 | FP-UC01-007 |
| EVT-WF02-006 | Exibição de Erro | Sistema retorna HTTP 400 (validação) | UC01 | FE-UC01-01/02/03/04 |
| EVT-WF02-007 | Sucesso + QR Code | Sistema retorna HTTP 201 (criado) | UC01 | FP-UC01-013 |
| EVT-WF02-008 | Importar AD | Usuário clica em CMP-WF02-009 | UC01 | FA-UC01-01 |

### 5.4 Comportamentos Obrigatórios

- Campos obrigatórios destacados com asterisco vermelho (*)
- Validação em tempo real (email, username, senha)
- Feedback imediato de erro (campo inválido destacado em vermelho)
- Senha deve atender política: mínimo 8 caracteres, 1 maiúscula, 1 número, 1 especial
- Indicador visual de força da senha (fraca, média, forte)
- Confirmação de senha deve ser idêntica à senha
- MFA obrigatório (toggle sempre ativo, não editável)
- Pelo menos 1 perfil deve ser selecionado

### 5.5 Estados

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário abre o formulário de criação
**Exibir:**
- Formulário vazio
- Campos obrigatórios marcados com *
- MFA toggle ativo por padrão
- Botão "Salvar" habilitado
- Botão "Cancelar" habilitado

**Contratos:**
- Nenhum erro exibido inicialmente
- Foco automático no campo Nome

#### Estado 2: Validando
**Quando:** Usuário clica em "Salvar" e sistema está validando
**Exibir:**
- Loading spinner no botão "Salvar"
- Botão "Salvar" com texto "Salvando..."
- Formulário desabilitado (não editável)

**Contratos:**
- Usuário não pode editar campos durante validação
- Timeout: se passar de 10s, exibir erro de timeout

#### Estado 3: Erro de Validação
**Quando:** API retorna HTTP 400 (validação falhou)
**Exibir:**
- Alert vermelho no topo do formulário com mensagem de erro
- Campos inválidos destacados em vermelho
- Mensagens de erro abaixo de cada campo inválido
- Botão "Salvar" habilitado novamente

**Exemplos de Mensagens:**
- Email duplicado: "Email já cadastrado para este tenant."
- Username duplicado: "Username já cadastrado para este tenant."
- Senha inválida: "Senha deve conter mínimo 8 caracteres, 1 maiúscula, 1 número e 1 caractere especial."
- Email inválido: "Email inválido. Use o formato: usuario@dominio.com"
- Confirmação não coincide: "As senhas não coincidem."

**Contratos:**
- Foco automático no primeiro campo com erro
- Mensagens de erro em português claro

#### Estado 4: Sucesso
**Quando:** API retorna HTTP 201 (usuário criado)
**Exibir:**
- Toast de sucesso: "Usuário criado com sucesso!"
- Modal com QR Code TOTP para configuração de MFA
- Instruções claras: "Escaneie o QR Code no Google Authenticator ou similar"
- Botão "Fechar e Voltar para Lista"
- Botão "Criar Outro Usuário"

**Contratos:**
- QR Code deve ser grande e legível (mínimo 200x200px)
- Exibir também o secret TOTP em texto (caso usuário prefira digitar manualmente)
- Após fechar modal, retornar para WF-01 (listagem)

### 5.6 Contratos de Comportamento

#### Responsividade
- **Mobile:**
  - Formulário em coluna única
  - Campos largura 100%
  - Botões empilhados verticalmente
- **Tablet:**
  - Formulário em 2 colunas (Nome/Email, Username/Senha)
  - Botões lado a lado
- **Desktop:**
  - Formulário em 2 colunas otimizadas
  - Modal QR Code centralizado (400x500px)

#### Acessibilidade
- Labels em português claro
- aria-required="true" em campos obrigatórios
- aria-invalid="true" em campos com erro
- Navegação por teclado (Tab, Shift+Tab, Enter para submeter)
- Esc para cancelar
- Screen reader anuncia erros de validação

#### Validações Client-Side
- Email: regex padrão RFC 5322
- Username: alfanumérico, 3-50 caracteres, sem espaços
- Senha: 8+ chars, pelo menos 1 maiúscula, 1 número, 1 especial
- Confirmação de senha: idêntica à senha

#### Validações Server-Side
- Email único no tenant (EmpresaId)
- Username único no tenant (EmpresaId)
- Política de senha BCrypt (work factor 12)
- Pelo menos 1 perfil selecionado

---

## 6. WF-03 — EDIÇÃO DE USUÁRIO (UC03)

### 6.1 Intenção da Tela
Permitir **alteração controlada** de dados de usuário existente, incluindo transições de estado e gestão de perfis.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Editável |
|----|-----------|------|-----------|----------|
| CMP-WF03-001 | Campo Nome | Input | Nome completo | Sim |
| CMP-WF03-002 | Campo Email | Input | Email (único no tenant, exceto próprio) | Sim |
| CMP-WF03-003 | Campo Username | Input | Username (único no tenant, exceto próprio) | Sim |
| CMP-WF03-004 | Campo Estado | Dropdown | Estado atual (active, blocked, inactive, deleted) | Sim |
| CMP-WF03-005 | Campo Perfis | MultiSelect | Perfis atribuídos | Sim |
| CMP-WF03-006 | Toggle MFA | Switch | MFA ativo (visualização apenas) | Não |
| CMP-WF03-007 | Botão Bloquear | Button | Transição: active → blocked | Condicional |
| CMP-WF03-008 | Botão Desbloquear | Button | Transição: blocked → active | Condicional |
| CMP-WF03-009 | Botão Inativar | Button | Transição: active → inactive | Condicional |
| CMP-WF03-010 | Botão Resetar Senha/MFA | Button | Gera senha temporária e novo secret TOTP | Sim |
| CMP-WF03-011 | Botão Salvar | Button | Salvar alterações | - |
| CMP-WF03-012 | Botão Cancelar | Button | Cancelar edição | - |
| CMP-WF03-013 | Mensagem de Erro | Alert | Erros de validação | - |
| CMP-WF03-014 | Modal Senha Temporária | Modal | Exibe senha temporária após reset | - |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo UC |
|----|--------|---------|----------------|----------|
| EVT-WF03-001 | Submissão de Formulário | Usuário clica em CMP-WF03-011 | UC03 | FP-UC03-003 |
| EVT-WF03-002 | Cancelamento | Usuário clica em CMP-WF03-012 | UC03 | (Retorna para WF-04) |
| EVT-WF03-003 | Bloquear Usuário | Usuário clica em CMP-WF03-007 | UC03 | FA-UC03-01 |
| EVT-WF03-004 | Desbloquear Usuário | Usuário clica em CMP-WF03-008 | UC03 | FA-UC03-02 |
| EVT-WF03-005 | Inativar Usuário | Usuário clica em CMP-WF03-009 | UC03 | FA-UC03-03 |
| EVT-WF03-006 | Resetar Senha/MFA | Usuário clica em CMP-WF03-010 | UC03 | FA-UC03-04 |
| EVT-WF03-007 | Erro de Validação | Sistema retorna HTTP 400 | UC03 | FE-UC03-01/02 |

### 6.4 Regras Visuais

- Dados atuais pré-carregados no formulário
- Campos alterados destacados visualmente (borda azul)
- Diferença entre valor original e novo valor (tooltip "Valor anterior: X")
- Botões de transição de estado condicionais:
  - Se Estado = active: exibir "Bloquear" e "Inativar"
  - Se Estado = blocked: exibir "Desbloquear"
  - Se Estado = inactive: exibir "Ativar"
  - Se Estado = deleted: nenhum botão (não editável)

### 6.5 Restrições

- Campo Email: único no tenant (excluindo o próprio usuário)
- Campo Username: único no tenant (excluindo o próprio usuário)
- Transições de estado válidas (conforme RN-RF012-02):
  - active ↔ blocked ✅
  - active → inactive ✅
  - inactive → active ✅
  - deleted → qualquer ❌ (irreversível)
- Usuário não pode editar a si mesmo (validação no backend)
- Usuário não pode remover todos os perfis (pelo menos 1 obrigatório)

### 6.6 Estados

#### Estado 1: Carregando Dados
**Quando:** Sistema está buscando dados do usuário
**Exibir:**
- Skeleton loader no formulário
- Mensagem: "Carregando dados do usuário..."

#### Estado 2: Formulário Preenchido
**Quando:** Dados carregados com sucesso
**Exibir:**
- Formulário com dados atuais
- Botões de transição de estado habilitados conforme regras
- Botão "Salvar" habilitado
- Botão "Cancelar" habilitado

#### Estado 3: Salvando
**Quando:** Usuário clica em "Salvar"
**Exibir:**
- Loading spinner no botão "Salvar"
- Botão "Salvar" com texto "Salvando..."
- Formulário desabilitado

#### Estado 4: Sucesso
**Quando:** API retorna HTTP 200 (atualizado)
**Exibir:**
- Toast de sucesso: "Usuário atualizado com sucesso!"
- Retornar para WF-04 (visualização)

#### Estado 5: Erro de Validação
**Quando:** API retorna HTTP 400
**Exibir:**
- Alert vermelho com mensagem de erro
- Campos inválidos destacados
- Exemplos:
  - Email duplicado: "Email já cadastrado para outro usuário."
  - Transição inválida: "Transição de estado inválida: deleted → active não permitida."

### 6.7 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única, botões empilhados
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário otimizado, botões de ação lado a lado

#### Acessibilidade
- Labels em português
- aria-label para botões de transição de estado
- Navegação por teclado
- Confirmação modal para ações destrutivas (Bloquear, Inativar, Resetar Senha)

---

## 7. WF-04 — VISUALIZAÇÃO DE USUÁRIO (UC02)

### 7.1 Intenção da Tela
Permitir **consulta completa e segura** de dados do usuário, incluindo histórico de acessos e auditoria.

### 7.2 Conteúdos Obrigatórios

#### Seção 1: Dados Principais
- Avatar (imagem ou iniciais)
- Nome Completo
- Email
- Username
- Estado (badge colorido)
- MFA Ativo (ícone verde/cinza)
- Data de Criação
- Último Login (data/hora)
- Tentativas de Login Falhadas

#### Seção 2: Perfis (Roles)
- Lista de perfis atribuídos (badges)
- Botão "Gerenciar Perfis" (redireciona para WF-06)

#### Seção 3: Informações de Auditoria
- Data de Criação
- Criado Por (usuário)
- Data de Última Atualização
- Atualizado Por (usuário)

#### Seção 4: Histórico de Acessos (FA-UC02-02)
- Tabela com:
  - Data/Hora
  - IP
  - UserAgent
  - Geolocalização (cidade, país)
  - Status (sucesso/falha)
- Paginação (últimos 50 acessos)

#### Seção 5: Histórico de Senhas (FA-UC02-01)
- Tabela com:
  - Data de Alteração
  - Hash BCrypt (primeiros 20 caracteres)
- Exibir últimas 12 senhas

### 7.3 Ações Disponíveis

| Ação | Botão | Permissão Necessária |
|------|-------|---------------------|
| Editar Usuário | "Editar" | CAD.USUARIOS.UPDATE |
| Excluir Usuário | "Excluir" | CAD.USUARIOS.DELETE |
| Gerenciar Perfis | "Gerenciar Perfis" | CAD.PERFIS.UPDATE |
| Voltar para Lista | "Voltar" | CAD.USUARIOS.VIEW_ANY |

### 7.4 Estados

#### Estado 1: Carregando
**Quando:** Sistema está buscando dados
**Exibir:**
- Skeleton loader
- Mensagem: "Carregando detalhes do usuário..."

#### Estado 2: Dados Exibidos
**Quando:** Dados carregados com sucesso
**Exibir:**
- Todas as seções preenchidas
- Botões de ação habilitados conforme permissões

#### Estado 3: Erro ao Carregar
**Quando:** API retorna erro (404, 403, 500)
**Exibir:**
- Mensagem de erro específica:
  - 404: "Usuário não encontrado."
  - 403: "Acesso negado. Usuário pertence a outro tenant."
  - 500: "Erro ao carregar dados. Tente novamente."
- Botão "Tentar Novamente"
- Botão "Voltar para Lista"

#### Estado 4: Histórico Vazio
**Quando:** Não há histórico de acessos ou senhas
**Exibir:**
- Mensagem: "Nenhum acesso registrado" ou "Nenhuma alteração de senha registrada"

### 7.5 Contratos de Comportamento

#### Responsividade
- **Mobile:** Seções empilhadas verticalmente, tabelas viram cards
- **Tablet:** Layout em 2 colunas (Dados + Perfis, Auditoria + Histórico)
- **Desktop:** Layout otimizado com sidebar (Dados + Perfis) e conteúdo principal (Auditoria + Histórico)

#### Acessibilidade
- Labels claros
- Botões com aria-label
- Contraste mínimo 4.5:1
- Navegação por teclado

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO (UC04)

### 8.1 Intenção
Evitar exclusões acidentais de usuários (soft delete).

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Modal de Confirmação | Modal | Modal centralizado |
| CMP-WF05-002 | Título | Text | "Confirmar Exclusão" |
| CMP-WF05-003 | Mensagem | Text | "Tem certeza que deseja excluir o usuário {Nome}? Esta ação é reversível." |
| CMP-WF05-004 | Botão Confirmar | Button | "Excluir Usuário" (vermelho) |
| CMP-WF05-005 | Botão Cancelar | Button | "Cancelar" (cinza) |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo UC |
|----|--------|---------|----------------|----------|
| EVT-WF05-001 | Confirmar Exclusão | Usuário clica em CMP-WF05-004 | UC04 | FP-UC04-004 |
| EVT-WF05-002 | Cancelar | Usuário clica em CMP-WF05-005 | UC04 | (Fecha modal) |

### 8.4 Regras

- Modal deve ser exibido ao clicar em "Excluir" em WF-01 ou WF-04
- Ação de exclusão só ocorre após confirmação explícita
- Informar que a exclusão é reversível (soft delete)
- Botão "Confirmar" deve estar em vermelho (ação destrutiva)
- Clicar fora do modal ou pressionar Esc cancela a ação

### 8.5 Estados

#### Estado 1: Modal Exibido
**Quando:** Usuário clica em "Excluir"
**Exibir:**
- Modal centralizado
- Nome do usuário destacado em negrito
- Foco automático no botão "Cancelar" (segurança)

#### Estado 2: Excluindo
**Quando:** Usuário confirma exclusão
**Exibir:**
- Loading spinner no botão "Confirmar"
- Botão "Confirmar" com texto "Excluindo..."
- Modal bloqueado (não pode fechar)

#### Estado 3: Sucesso
**Quando:** API retorna HTTP 200
**Exibir:**
- Toast de sucesso: "Usuário excluído com sucesso."
- Fechar modal
- Retornar para WF-01 (listagem)

#### Estado 4: Erro
**Quando:** API retorna erro (400, 403, 404, 500)
**Exibir:**
- Alert vermelho dentro do modal com mensagem de erro
- Exemplos:
  - 403: "Acesso negado. Usuário pertence a outro tenant."
  - 400: "Você não pode excluir seu próprio usuário."
  - 404: "Usuário não encontrado."
- Botão "Tentar Novamente"
- Botão "Cancelar"

### 8.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Modal largura 90% da tela
- **Tablet:** Modal largura 500px
- **Desktop:** Modal largura 500px, centralizado

#### Acessibilidade
- Foco automático no botão "Cancelar" (segurança)
- Esc fecha o modal
- aria-label: "Confirmar exclusão de usuário {Nome}"

---

## 9. WF-06 — GERENCIAR PERFIS DE USUÁRIO (UC08)

### 9.1 Intenção da Tela
Permitir **atribuição e remoção de perfis (roles)** a usuários do sistema com controle de RBAC.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Permissão Necessária |
|----|-----------|------|-----------|---------------------|
| CMP-WF06-001 | Dropdown de Perfis | Dropdown | Seleção de perfil (role) | CAD.PERFIS.UPDATE |
| CMP-WF06-002 | Lista de Usuários do Perfil | DataTable | Usuários que possuem o perfil selecionado | CAD.PERFIS.UPDATE |
| CMP-WF06-003 | Botão Adicionar Usuário | Button | Adicionar usuário ao perfil | CAD.PERFIS.UPDATE |
| CMP-WF06-004 | Botão Remover | IconButton | Remover usuário do perfil (cada linha) | CAD.PERFIS.UPDATE |
| CMP-WF06-005 | Modal Adicionar Usuário | Modal | Lista de usuários disponíveis para adicionar | CAD.PERFIS.UPDATE |
| CMP-WF06-006 | MultiSelect Usuários | MultiSelect | Seleção múltipla de usuários | CAD.PERFIS.UPDATE |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo UC |
|----|--------|---------|----------------|----------|
| EVT-WF06-001 | Selecionar Perfil | Usuário seleciona perfil no dropdown CMP-WF06-001 | UC08 | FP-UC08-004 |
| EVT-WF06-002 | Adicionar Usuário | Usuário clica em CMP-WF06-003 | UC08 | FP-UC08-006 |
| EVT-WF06-003 | Remover Usuário | Usuário clica em CMP-WF06-004 | UC08 | FA-UC08-01 |
| EVT-WF06-004 | Atribuir Múltiplos Perfis | Usuário seleciona múltiplos perfis em CMP-WF06-006 | UC08 | FA-UC08-02 |

### 9.4 Ações Permitidas
- Visualizar perfis do tenant
- Visualizar usuários vinculados a um perfil
- Adicionar usuário a um perfil
- Remover usuário de um perfil
- Atribuir múltiplos perfis a um usuário

### 9.5 Estados

#### Estado 1: Carregando Perfis
**Quando:** Tela está carregando perfis do tenant
**Exibir:**
- Skeleton loader no dropdown de perfis
- Mensagem: "Carregando perfis..."

#### Estado 2: Perfil Selecionado - Carregando Usuários
**Quando:** Usuário seleciona um perfil
**Exibir:**
- Skeleton loader na lista de usuários
- Mensagem: "Carregando usuários do perfil {Nome do Perfil}..."

#### Estado 3: Perfil Selecionado - Sem Usuários
**Quando:** Perfil não tem usuários vinculados
**Exibir:**
- Mensagem: "Nenhum usuário possui o perfil {Nome do Perfil}"
- Botão "Adicionar Primeiro Usuário"

#### Estado 4: Perfil Selecionado - Com Usuários
**Quando:** Perfil tem usuários vinculados
**Exibir:**
- Tabela com colunas: Avatar, Nome, Email, Ações (Remover)
- Total de usuários: "3 usuários com o perfil {Nome do Perfil}"
- Botão "Adicionar Usuário"

#### Estado 5: Erro ao Carregar
**Quando:** API retorna erro
**Exibir:**
- Mensagem de erro: "Erro ao carregar perfis/usuários. Tente novamente."
- Botão "Tentar Novamente"

### 9.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Lista de usuários vira cards, botões empilhados
- **Tablet:** Tabela simplificada
- **Desktop:** Tabela completa

#### Acessibilidade
- Labels em português
- aria-label para botões de ação
- Navegação por teclado
- Confirmação modal antes de remover usuário de perfil

#### Segurança
- Apenas usuários do tenant atual podem ser vinculados
- Validação: usuário não pode ter perfil duplicado
- HTTP 403 se usuário não tiver CAD.PERFIS.UPDATE

---

## 10. NOTIFICAÇÕES

### 10.1 Tipos Padronizados

| Tipo | Uso | Cor | Duração |
|----|----|-----|---------|
| Sucesso | Operação concluída (criar, editar, excluir) | Verde | 3s |
| Erro | Falha bloqueante (validação, permissão, servidor) | Vermelho | 5s ou até fechar |
| Aviso | Atenção necessária (senha fraca, MFA desabilitado) | Amarelo | 5s |
| Info | Feedback neutro (carregando, processando) | Azul | 3s |

### 10.2 Exemplos de Mensagens

**Sucesso:**
- "Usuário criado com sucesso!"
- "Usuário atualizado com sucesso!"
- "Usuário excluído com sucesso."
- "Perfil atribuído com sucesso."

**Erro:**
- "Erro ao criar usuário: Email já cadastrado para este tenant."
- "Erro ao carregar usuários: Falha no servidor (500)."
- "Acesso negado. Permissão CAD.USUARIOS.CREATE necessária."

**Aviso:**
- "Senha fraca. Recomendamos usar uma senha mais forte."
- "MFA não está ativo. Configure para maior segurança."

**Info:**
- "Carregando usuários..."
- "Processando importação do Active Directory..."

---

## 11. RESPONSIVIDADE (OBRIGATÓRIO)

| Breakpoint | Largura | Comportamento |
|-------|---------|---------------|
| Mobile | < 768px | Layout em coluna única, tabelas viram cards, botões empilhados |
| Tablet | 768px - 1024px | Layout em 2 colunas, tabelas simplificadas |
| Desktop | > 1024px | Layout completo, todas as colunas visíveis |

### 11.1 Componentes Responsivos

- **Tabelas:**
  - Mobile: Cards empilhados
  - Tablet: 4-5 colunas principais
  - Desktop: Todas as colunas
- **Formulários:**
  - Mobile: 1 coluna
  - Tablet: 2 colunas
  - Desktop: 2-3 colunas otimizadas
- **Modais:**
  - Mobile: 90% largura da tela
  - Tablet: 500-600px
  - Desktop: 500-600px centralizado

---

## 12. ACESSIBILIDADE (OBRIGATÓRIO)

### 12.1 Navegação por Teclado

| Tecla | Ação |
|-------|------|
| Tab | Navegar entre elementos interativos |
| Shift+Tab | Navegar para trás |
| Enter | Ativar botão/ação selecionada |
| Esc | Fechar modal, cancelar ação |
| Setas ↑↓ | Navegar em dropdowns/selects |

### 12.2 Screen Readers

- Botões com aria-label em português
- Estados anunciados ("Carregando usuários", "10 usuários encontrados", "Erro ao carregar")
- Campos de formulário com labels claras
- Erros de validação anunciados
- Confirmações anunciadas

### 12.3 Contraste (WCAG AA)

- Texto/Fundo: Mínimo 4.5:1
- Botões primários: Verde escuro (#16a34a) / Branco (#ffffff)
- Botões destrutivos: Vermelho escuro (#dc2626) / Branco (#ffffff)
- Badges de estado:
  - Active: Verde (#22c55e)
  - Blocked: Vermelho (#ef4444)
  - Inactive: Cinza (#6b7280)
  - Deleted: Preto (#000000)

---

## 13. RASTREABILIDADE

| Wireframe | UC | RF | Descrição |
|---------|----|----|-----------|
| WF-01 | UC00 | RF012 | Listagem de Usuários com filtros e busca |
| WF-02 | UC01 | RF012 | Criação de Usuário com MFA obrigatório |
| WF-03 | UC03 | RF012 | Edição de Usuário com transições de estado |
| WF-04 | UC02 | RF012 | Visualização de Usuário com auditoria |
| WF-05 | UC04 | RF012 | Confirmação de Exclusão (soft delete) |
| WF-06 | UC08 | RF012 | Gerenciar Perfis de Usuário (RBAC) |

---

## 14. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, fontes, espaçamentos específicos)
- Escolha de framework (Filament, React, Vue, Angular)
- Design gráfico definitivo (ícones, ilustrações)
- Animações avançadas (transições, efeitos)
- Implementação técnica (código HTML/CSS/JS)

---

## 15. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-04 | Agência ALC - alc.dev.br | Wireframes completos do RF012 com cobertura de 100% dos UCs (UC00, UC01, UC02, UC03, UC04, UC08) |

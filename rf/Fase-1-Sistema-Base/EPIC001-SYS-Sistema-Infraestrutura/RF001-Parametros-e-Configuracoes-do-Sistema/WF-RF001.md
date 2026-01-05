# WF-RF001 — Wireframes Canônicos (UI Contract)

**Versão:** 1.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF001 - Sistema de Parâmetros e Configurações Centralizadas
**UC Relacionado:** UC-RF001 (UC00-UC21)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF001 - Sistema de Parâmetros e Configurações Centralizadas.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional** nas 4 entidades CRUD + 2 funcionalidades especiais
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
- Proteção contra ações destrutivas em parâmetros de sistema (Fl_Sistema = 1)
- Máscara de valores sensíveis (Fl_Sensivel = 1) para usuários sem permissão

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Parâmetros de sistema | Proteção visual (ícone cadeado) |
| Valores sensíveis | Mascarados (`*****`) sem permissão específica |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Acessibilidade | WCAG AA |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

### 3.1 Entidade: Sistema_Parametro (UC00-UC04)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Parâmetros | UC00 | Descoberta, busca e acesso aos parâmetros |
| WF-02 | Criar Parâmetro | UC01 | Criação de novo parâmetro com validação tipada |
| WF-03 | Visualizar Parâmetro | UC02 | Consulta completa com histórico de alterações |
| WF-04 | Editar Parâmetro | UC03 | Alteração controlada de parâmetros |
| WF-05 | Confirmação de Exclusão | UC04 | Confirmação de exclusão lógica |

### 3.2 Entidade: Sistema_Feature_Flag (UC05-UC09)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-06 | Listagem de Feature Flags | UC05 | Descoberta e gerenciamento de flags |
| WF-07 | Criar Feature Flag | UC06 | Criação de nova feature flag |
| WF-08 | Visualizar Feature Flag | UC07 | Consulta detalhada da flag |
| WF-09 | Editar Feature Flag | UC08 | Alteração de flag (status on/off, data validade) |
| WF-10 | Confirmação de Exclusão | UC09 | Confirmação de exclusão lógica |

### 3.3 Entidade: Sistema_Configuracao_Email (UC10-UC14)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-11 | Listagem de Configurações de Email | UC10 | Gerenciamento de configurações SMTP |
| WF-12 | Criar Configuração de Email | UC11 | Criação de nova configuração SMTP |
| WF-13 | Visualizar Configuração de Email | UC12 | Consulta com teste de conexão |
| WF-14 | Editar Configuração de Email | UC13 | Alteração de configurações SMTP |
| WF-15 | Confirmação de Exclusão | UC14 | Confirmação de exclusão lógica |

### 3.4 Entidade: Sistema_Limite_Uso (UC15-UC19)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-16 | Listagem de Limites de Uso | UC15 | Gerenciamento de limites e quotas |
| WF-17 | Criar Limite de Uso | UC16 | Criação de novo limite |
| WF-18 | Visualizar Limite de Uso | UC17 | Consulta com uso atual e alertas |
| WF-19 | Editar Limite de Uso | UC18 | Alteração de limites e thresholds |
| WF-20 | Confirmação de Exclusão | UC19 | Confirmação de exclusão lógica |

### 3.5 Funcionalidades Especiais

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-21 | Dashboard de Jobs Background | UC20 | Monitoramento de verificação de limites |
| WF-22 | Teste de Integração SMTP | UC21 | Interface para teste de envio de email |

**Total:** 22 Wireframes cobrindo 100% dos UCs

---

## 4. WF-01 — LISTAGEM DE PARÂMETROS (UC00)

### 4.1 Intenção da Tela
Permitir ao usuário **localizar, filtrar e acessar parâmetros do sistema** do seu tenant, com suporte a busca textual, filtros por categoria e tipo de dado, ordenação e paginação.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Criar Parâmetro" | Button | Ação primária (requer permissão `SYS.PARAMETROS.CREATE`) |
| CMP-WF01-002 | Campo de Busca | Input | Busca textual em Cd_Parametro, Nm_Parametro, Ds_Parametro |
| CMP-WF01-003 | Filtro Categoria | Dropdown | Sistema, Segurança, Integração, Notificação, Relatório |
| CMP-WF01-004 | Filtro Tipo de Dado | Dropdown | String, Integer, Decimal, Boolean, Date, JSON |
| CMP-WF01-005 | Checkbox Apenas Sistema | Checkbox | Filtrar apenas parâmetros com Fl_Sistema = 1 |
| CMP-WF01-006 | Tabela de Registros | DataTable | Colunas: Cd_Parametro, Nm_Parametro, Categoria, Tipo_Dado, Fl_Sistema, Fl_Sensivel, Ações |
| CMP-WF01-007 | Ícone Cadeado | Icon | Indicador visual para Fl_Sistema = 1 |
| CMP-WF01-008 | Badge Sensível | Badge | Indicador visual para Fl_Sensivel = 1 |
| CMP-WF01-009 | Botão Visualizar | IconButton | Ação para visualizar registro (cada linha) |
| CMP-WF01-010 | Botão Editar | IconButton | Ação para editar (requer permissão `SYS.PARAMETROS.UPDATE`) |
| CMP-WF01-011 | Botão Excluir | IconButton | Ação para excluir (requer permissão `SYS.PARAMETROS.DELETE`, desabilitado se Fl_Sistema = 1) |
| CMP-WF01-012 | Paginação | Pagination | 20 registros por página |
| CMP-WF01-013 | Botão Exportar CSV | Button | Exportar lista (requer permissão `SYS.PARAMETROS.EXPORT`) |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Criar Parâmetro" | Usuário clica em CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca textual | Usuário digita em CMP-WF01-002 | UC00 | FA-UC00-001 |
| EVT-WF01-003 | Filtro por categoria | Usuário seleciona em CMP-WF01-003 | UC00 | FA-UC00-003 |
| EVT-WF01-004 | Filtro por tipo de dado | Usuário seleciona em CMP-WF01-004 | UC00 | FA-UC00-004 |
| EVT-WF01-005 | Filtro apenas sistema | Usuário marca CMP-WF01-005 | UC00 | FA-UC00-005 |
| EVT-WF01-006 | Ordenar coluna | Usuário clica em cabeçalho de coluna | UC00 | FA-UC00-002 |
| EVT-WF01-007 | Clique em Visualizar | Usuário clica em CMP-WF01-009 | UC02 | FP-UC02-001 |
| EVT-WF01-008 | Clique em Editar | Usuário clica em CMP-WF01-010 | UC03 | FP-UC03-001 |
| EVT-WF01-009 | Clique em Excluir | Usuário clica em CMP-WF01-011 | UC04 | FP-UC04-001 |
| EVT-WF01-010 | Mudança de página | Usuário interage com CMP-WF01-012 | UC00 | FP-UC00-004 |
| EVT-WF01-011 | Exportar CSV | Usuário clica em CMP-WF01-013 | UC00 | FA-UC00-006 |

### 4.4 Ações Permitidas
- Buscar parâmetros por termo (código, nome, descrição)
- Filtrar por categoria (Sistema, Segurança, Integração, Notificação, Relatório)
- Filtrar por tipo de dado (String, Integer, Decimal, Boolean, Date, JSON)
- Filtrar apenas parâmetros de sistema (Fl_Sistema = 1)
- Ordenar por qualquer coluna visível (ASC/DESC)
- Visualizar detalhes de parâmetro
- Criar novo parâmetro (se tiver permissão)
- Editar parâmetro (se tiver permissão)
- Excluir parâmetro não-sistema (se tiver permissão)
- Exportar lista para CSV (se tiver permissão)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados

**Exibir:**
- Skeleton loader (tabela com shimmer)
- Mensagem: "Carregando parâmetros..."
- Filtros e busca desabilitados temporariamente

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há parâmetros no tenant ou filtros não retornaram resultados

**Exibir:**
- Ícone ilustrativo (documento vazio)
- Mensagem: "Nenhum parâmetro encontrado"
- Submensagem: "Crie o primeiro parâmetro do sistema"
- Botão "Criar Parâmetro" (se tiver permissão `SYS.PARAMETROS.CREATE`)

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, etc.)

**Exibir:**
- Ícone de erro (triângulo vermelho)
- Mensagem: "Erro ao carregar parâmetros. Tente novamente."
- Botão "Recarregar" para retry
- Log de erro técnico registrado (não exibido ao usuário)

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há parâmetros disponíveis

**Exibir:**
- Tabela completa com colunas: Cd_Parametro, Nm_Parametro, Categoria, Tipo_Dado, Fl_Sistema (ícone cadeado), Fl_Sensivel (badge), Ações
- Valores sensíveis mascarados (`*****`) para usuários sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- Paginação (se > 20 registros)
- Filtros e busca ativos
- Indicadores visuais:
  - Ícone de cadeado para Fl_Sistema = 1
  - Badge "Sensível" para Fl_Sensivel = 1
  - Botão "Excluir" desabilitado para Fl_Sistema = 1

### 4.6 Contratos de Comportamento

#### Isolamento Multi-Tenant
- Apenas parâmetros do tenant atual (Id_Conglomerado) são exibidos
- Registros soft-deleted (Fl_Excluido = 1) não aparecem

#### Proteção de Parâmetros de Sistema
- Parâmetros com Fl_Sistema = 1 têm ícone de cadeado
- Botão "Excluir" desabilitado/oculto para Fl_Sistema = 1

#### Máscara de Valores Sensíveis
- Valores com Fl_Sensivel = 1 são mascarados (`*****`) na tabela
- Apenas usuários com permissão `SYS.PARAMETROS.VIEW_SENSITIVE` veem valores reais

#### Responsividade
- **Mobile:** Lista empilhada (cards), filtros em modal
- **Tablet:** Tabela simplificada (4 colunas principais)
- **Desktop:** Tabela completa (todas colunas)

#### Acessibilidade (WCAG AA)
- Labels em português claro
- Botões com aria-label ("Criar parâmetro", "Editar parâmetro X", "Excluir parâmetro X")
- Navegação por teclado (Tab, Enter, Esc)
- Contraste mínimo 4.5:1
- Screen reader: anunciar total de registros e filtros ativos

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso/erro após ações
- Confirmação antes de exclusão
- Indicador de filtros ativos (badge com total)

---

## 5. WF-02 — CRIAR PARÂMETRO (UC01)

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de novo parâmetro do sistema com validação tipada, criptografia de dados sensíveis e auditoria completa.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Validação |
|----|-----------|------|-----------|-----------|
| CMP-WF02-001 | Campo Código | Input | Cd_Parametro (único no tenant) | Obrigatório, regex: `^[A-Z0-9_]+$` |
| CMP-WF02-002 | Campo Nome | Input | Nm_Parametro | Obrigatório, max 200 chars |
| CMP-WF02-003 | Campo Descrição | Textarea | Ds_Parametro | Obrigatório, max 2000 chars |
| CMP-WF02-004 | Dropdown Categoria | Dropdown | Sistema, Segurança, Integração, Notificação, Relatório | Obrigatório |
| CMP-WF02-005 | Dropdown Tipo de Dado | Dropdown | String, Integer, Decimal, Boolean, Date, JSON | Obrigatório |
| CMP-WF02-006 | Campo Valor | Input dinâmico | Conforme tipo selecionado | Validação conforme tipo |
| CMP-WF02-007 | Checkbox Sensível | Checkbox | Fl_Sensivel | Opcional |
| CMP-WF02-008 | Checkbox Sistema | Checkbox | Fl_Sistema | Opcional |
| CMP-WF02-009 | Checkbox Obrigatório | Checkbox | Fl_Obrigatorio | Opcional |
| CMP-WF02-010 | Campo Regex Validação | Input | Regex_Validacao | Opcional |
| CMP-WF02-011 | Campo Valor Mínimo | Input | Valor_Minimo | Opcional |
| CMP-WF02-012 | Campo Valor Máximo | Input | Valor_Maximo | Opcional |
| CMP-WF02-013 | Campo Opções Válidas | Textarea | Opcoes_Validas (JSON array) | Opcional, validar JSON |
| CMP-WF02-014 | Campo Valor Padrão | Input | Valor_Padrao | Opcional |
| CMP-WF02-015 | Botão Salvar | Button | Ação primária | Enabled após validação |
| CMP-WF02-016 | Botão Salvar e Criar Outro | Button | Ação secundária | Enabled após validação |
| CMP-WF02-017 | Botão Cancelar | Button | Ação terciária | Sempre enabled |
| CMP-WF02-018 | Mensagem de Erro | Alert | Erros de validação | Exibir abaixo do formulário |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Submissão de Formulário | Usuário clica em CMP-WF02-015 | UC01 | FP-UC01-006 |
| EVT-WF02-002 | Salvar e Criar Outro | Usuário clica em CMP-WF02-016 | UC01 | FA-UC01-001 |
| EVT-WF02-003 | Cancelamento | Usuário clica em CMP-WF02-017 | UC01 | FA-UC01-002 |
| EVT-WF02-004 | Validação de Campo | Usuário sai de campo obrigatório vazio | UC01 | FE-UC01-001 |
| EVT-WF02-005 | Mudança de Tipo de Dado | Usuário altera CMP-WF02-005 | UC01 | Renderizar campo valor conforme tipo |
| EVT-WF02-006 | Validação de JSON | Usuário preenche CMP-WF02-013 | UC01 | FE-UC01-006 |

### 5.4 Comportamentos Obrigatórios

#### Validação Tipada Dinâmica
- Ao selecionar tipo de dado em CMP-WF02-005, campo CMP-WF02-006 muda:
  - **String:** Input text
  - **Integer:** Input number (step=1)
  - **Decimal:** Input number (step=0.01)
  - **Boolean:** Dropdown (true/false)
  - **Date:** Date picker
  - **JSON:** Textarea com syntax highlight

#### Validação em Tempo Real
- Campos obrigatórios destacados em vermelho se vazios ao perder foco
- Validação de regex em Cd_Parametro (apenas `A-Z`, `0-9`, `_`)
- Validação de JSON em Opcoes_Validas e Valor_Padrao (tipo JSON)
- Validação de min/max se especificados

#### Feedback Imediato
- Mensagem de erro abaixo de cada campo inválido
- Botão "Salvar" desabilitado se houver erros de validação
- Loading spinner no botão durante envio

### 5.5 Estados Obrigatórios

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário acessa tela de criação

**Exibir:**
- Formulário vazio
- Campos obrigatórios marcados com asterisco (*)
- Botão "Salvar" desabilitado até preencher campos obrigatórios

#### Estado 2: Erro de Validação
**Quando:** Formulário submetido com erros

**Exibir:**
- Campos inválidos destacados em vermelho
- Mensagens de erro específicas abaixo de cada campo:
  - "Campo obrigatório"
  - "Código já existe neste conglomerado"
  - "Valor inválido para tipo Integer"
  - "JSON inválido"
- Alert geral no topo: "Corrija os erros abaixo antes de salvar"

#### Estado 3: Sucesso
**Quando:** Parâmetro criado com sucesso

**Exibir:**
- Toast de sucesso: "Parâmetro '{Cd_Parametro}' criado com sucesso"
- Redirecionar para tela de visualização (WF-03)
- Se "Salvar e Criar Outro": limpar formulário e exibir toast

#### Estado 4: Cancelamento com Dados
**Quando:** Usuário clica em "Cancelar" com dados preenchidos

**Exibir:**
- Modal de confirmação: "Descartar alterações? Dados não salvos serão perdidos."
- Botões: "Descartar" (vermelho), "Continuar Editando" (cinza)

### 5.6 Contratos de Comportamento

#### Validação de Código Único
- Antes de salvar, verificar se Cd_Parametro já existe no tenant
- Retornar HTTP 409 se duplicado

#### Criptografia Automática
- Se Fl_Sensivel = 1 marcado, valor é criptografado em AES-256 ANTES de persistir
- Usuário não vê processo de criptografia (transparente)

#### Auditoria Automática
- Após criação bem-sucedida, registrar em Sistema_Parametro_Historico:
  - Tipo: CREATE
  - Valor anterior: NULL
  - Valor novo: JSON completo do registro
  - Id_Usuario, Dt_Alteracao, IP, User-Agent

#### Responsividade
- **Mobile:** Formulário em coluna única, campos empilhados
- **Tablet:** Formulário em 2 colunas (metadados à esquerda, valor à direita)
- **Desktop:** Formulário em 2 colunas otimizado

#### Acessibilidade (WCAG AA)
- Labels claros em português
- Campos com placeholder explicativo
- Navegação por teclado (Tab, Shift+Tab, Enter para salvar, Esc para cancelar)
- Screen reader: anunciar campos obrigatórios e erros de validação

---

## 6. WF-03 — VISUALIZAR PARÂMETRO (UC02)

### 6.1 Intenção da Tela
Permitir **consulta completa e segura** de parâmetro do sistema, incluindo metadados, histórico de alterações e valores descriptografados (para usuários autorizados).

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Card Dados Principais | Card | Exibe Cd_Parametro, Nm_Parametro, Ds_Parametro |
| CMP-WF03-002 | Card Configuração | Card | Categoria, Tipo_Dado, Valor |
| CMP-WF03-003 | Card Flags | Card | Fl_Sistema, Fl_Sensivel, Fl_Obrigatorio |
| CMP-WF03-004 | Card Validações | Card | Regex_Validacao, Valor_Minimo, Valor_Maximo, Opcoes_Validas |
| CMP-WF03-005 | Card Valor Padrão | Card | Valor_Padrao |
| CMP-WF03-006 | Card Auditoria | Card | Id_Usuario_Criacao, Dt_Criacao, Id_Usuario_Atualizacao, Dt_Atualizacao |
| CMP-WF03-007 | Ícone Cadeado | Icon | Indicador visual se Fl_Sistema = 1 |
| CMP-WF03-008 | Badge Sensível | Badge | Indicador visual se Fl_Sensivel = 1 |
| CMP-WF03-009 | Valor Mascarado | Text | `*****` se Fl_Sensivel = 1 e sem permissão |
| CMP-WF03-010 | Botão Editar | Button | Ação primária (requer permissão `SYS.PARAMETROS.UPDATE`) |
| CMP-WF03-011 | Botão Excluir | Button | Ação destrutiva (requer permissão `SYS.PARAMETROS.DELETE`, desabilitado se Fl_Sistema = 1) |
| CMP-WF03-012 | Botão Histórico | Button | Ação secundária (exibe modal com histórico) |
| CMP-WF03-013 | Botão Voltar | Button | Retornar para listagem |
| CMP-WF03-014 | Modal Histórico | Modal | Exibe registros de Sistema_Parametro_Historico |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Clique em Editar | Usuário clica em CMP-WF03-010 | UC03 | FP-UC03-001 |
| EVT-WF03-002 | Clique em Excluir | Usuário clica em CMP-WF03-011 | UC04 | FP-UC04-001 |
| EVT-WF03-003 | Clique em Histórico | Usuário clica em CMP-WF03-012 | UC02 | FA-UC02-001 |
| EVT-WF03-004 | Clique em Voltar | Usuário clica em CMP-WF03-013 | UC00 | Retornar para WF-01 |

### 6.4 Ações Permitidas
- Visualizar dados completos do parâmetro
- Editar parâmetro (se tiver permissão e não for sistema)
- Excluir parâmetro (se tiver permissão e não for sistema)
- Visualizar histórico de alterações
- Voltar para listagem

### 6.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados

**Exibir:**
- Skeleton loader (cards com shimmer)
- Mensagem: "Carregando parâmetro..."

#### Estado 2: Erro (Falha ao Carregar)
**Quando:** Parâmetro não encontrado ou erro de API

**Exibir:**
- Ícone de erro (triângulo vermelho)
- Mensagem: "Parâmetro não encontrado" (HTTP 404)
- Botão "Voltar para Listagem"

#### Estado 3: Dados (Parâmetro Exibido)
**Quando:** Parâmetro carregado com sucesso

**Exibir:**
- Todos os cards com dados completos
- Valor mascarado (`*****`) se Fl_Sensivel = 1 e usuário sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- Valor descriptografado se Fl_Sensivel = 1 e usuário com permissão (registra auditoria tipo ACCESS)
- Ícone de cadeado se Fl_Sistema = 1
- Badge "Sensível" se Fl_Sensivel = 1
- Botão "Excluir" desabilitado se Fl_Sistema = 1

#### Estado 4: Modal Histórico Aberto
**Quando:** Usuário clica em "Histórico"

**Exibir:**
- Modal com tabela de histórico
- Colunas: Data, Usuário, Tipo (CREATE, UPDATE, DELETE, ACCESS), Valor Anterior, Valor Novo
- Ordenação: Dt_Alteracao DESC
- Botão "Fechar"

### 6.6 Contratos de Comportamento

#### Isolamento Multi-Tenant
- Usuário só visualiza parâmetros do próprio tenant (Id_Conglomerado)
- Tentativa de acessar parâmetro de outro tenant retorna HTTP 404

#### Máscara de Valores Sensíveis
- Se Fl_Sensivel = 1 E usuário NÃO tem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`:
  - Exibir `*****` em CMP-WF03-009
- Se Fl_Sensivel = 1 E usuário tem permissão:
  - Descriptografar valor e exibir
  - Registrar auditoria tipo ACCESS em Sistema_Parametro_Historico

#### Proteção de Parâmetros de Sistema
- Se Fl_Sistema = 1:
  - Exibir ícone de cadeado em CMP-WF03-007
  - Botão "Excluir" (CMP-WF03-011) desabilitado/oculto

#### Responsividade
- **Mobile:** Cards empilhados em coluna única
- **Tablet:** Cards em 2 colunas
- **Desktop:** Cards em 3 colunas otimizado

#### Acessibilidade (WCAG AA)
- Labels claros em português
- Botões com aria-label
- Navegação por teclado
- Screen reader: anunciar status (sensível, sistema) e valores mascarados

---

## 7. WF-04 — EDITAR PARÂMETRO (UC03)

### 7.1 Intenção da Tela
Permitir **alteração controlada** de parâmetros do sistema, com validação, criptografia e auditoria de mudanças. Parâmetros de sistema (Fl_Sistema = 1) permitem editar apenas valor, não metadados.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Validação |
|----|-----------|------|-----------|-----------|
| CMP-WF04-001 | Campo Código | Input | Cd_Parametro (bloqueado) | Readonly |
| CMP-WF04-002 | Campo Nome | Input | Nm_Parametro | Obrigatório, max 200 chars |
| CMP-WF04-003 | Campo Descrição | Textarea | Ds_Parametro | Obrigatório, max 2000 chars |
| CMP-WF04-004 | Dropdown Categoria | Dropdown | Categoria | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-005 | Dropdown Tipo de Dado | Dropdown | Tipo_Dado | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-006 | Campo Valor | Input dinâmico | Conforme tipo | Validação conforme tipo |
| CMP-WF04-007 | Checkbox Sensível | Checkbox | Fl_Sensivel | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-008 | Checkbox Obrigatório | Checkbox | Fl_Obrigatorio | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-009 | Campo Regex Validação | Input | Regex_Validacao | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-010 | Campo Valor Mínimo | Input | Valor_Minimo | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-011 | Campo Valor Máximo | Input | Valor_Maximo | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-012 | Campo Opções Válidas | Textarea | Opcoes_Validas | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-013 | Campo Valor Padrão | Input | Valor_Padrao | Bloqueado se Fl_Sistema = 1 |
| CMP-WF04-014 | Badge "Parâmetro de Sistema" | Badge | Indicador visual | Exibir se Fl_Sistema = 1 |
| CMP-WF04-015 | Botão Salvar | Button | Ação primária | Enabled após validação |
| CMP-WF04-016 | Botão Cancelar | Button | Ação secundária | Sempre enabled |
| CMP-WF04-017 | Mensagem de Erro | Alert | Erros de validação | Exibir abaixo do formulário |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Submissão de Formulário | Usuário clica em CMP-WF04-015 | UC03 | FP-UC03-009 |
| EVT-WF04-002 | Cancelamento | Usuário clica em CMP-WF04-016 | UC03 | FA-UC03-001 |
| EVT-WF04-003 | Validação de Campo | Usuário sai de campo obrigatório vazio | UC03 | FE-UC03-002 |
| EVT-WF04-004 | Detecção de Conflito | Backend retorna HTTP 409 (edição concorrente) | UC03 | FE-UC03-008 |

### 7.4 Comportamentos Obrigatórios

#### Bloqueio de Campos para Parâmetros de Sistema
- Se Fl_Sistema = 1:
  - Exibir badge "Parâmetro de Sistema" (CMP-WF04-014)
  - Bloquear edição de: Cd_Parametro, Nm_Parametro, Ds_Parametro, Categoria, Tipo_Dado, Fl_Sensivel, Fl_Obrigatorio, Regex_Validacao, Valor_Minimo, Valor_Maximo, Opcoes_Validas, Valor_Padrao
  - Permitir edição apenas de: Valor (CMP-WF04-006)

#### Validação de Edição Concorrente (Optimistic Concurrency)
- Usar ETag ou timestamp para detectar conflitos
- Se registro foi alterado por outro usuário, retornar HTTP 409
- Exibir modal: "O registro foi alterado por outro usuário. Recarregar e tentar novamente?"

#### Auditoria de Mudanças (Diff JSON)
- Antes de salvar, capturar estado anterior do registro (JSON completo)
- Após salvar, registrar em Sistema_Parametro_Historico:
  - Tipo: UPDATE
  - Valor anterior: JSON antes
  - Valor novo: JSON depois
  - Diff: apenas campos alterados

### 7.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está carregando dados do parâmetro

**Exibir:**
- Skeleton loader (formulário com shimmer)
- Mensagem: "Carregando parâmetro..."

#### Estado 2: Erro de Validação
**Quando:** Formulário submetido com erros

**Exibir:**
- Campos inválidos destacados em vermelho
- Mensagens de erro específicas
- Alert geral: "Corrija os erros abaixo antes de salvar"

#### Estado 3: Erro de Conflito (HTTP 409)
**Quando:** Registro foi alterado por outro usuário

**Exibir:**
- Modal de aviso: "O registro foi alterado por outro usuário. Recarregar e tentar novamente?"
- Botões: "Recarregar" (azul), "Cancelar" (cinza)

#### Estado 4: Sucesso
**Quando:** Parâmetro atualizado com sucesso

**Exibir:**
- Toast de sucesso: "Parâmetro '{Cd_Parametro}' atualizado com sucesso"
- Redirecionar para tela de visualização (WF-03)

#### Estado 5: Cancelamento com Alterações
**Quando:** Usuário clica em "Cancelar" com dados alterados

**Exibir:**
- Modal de confirmação: "Descartar alterações? Mudanças não salvas serão perdidas."
- Botões: "Descartar" (vermelho), "Continuar Editando" (cinza)

### 7.6 Contratos de Comportamento

#### Proteção de Parâmetros de Sistema
- Se Fl_Sistema = 1, tentativa de editar metadados retorna HTTP 403
- Mensagem: "Parâmetros de sistema não podem ter metadados editados via interface. Apenas valores podem ser alterados."

#### Criptografia Automática
- Se Fl_Sensivel = 1 e valor foi alterado, criptografar em AES-256 ANTES de persistir

#### Invalidação de Cache
- Após edição bem-sucedida, invalidar cache de configurações

#### Responsividade
- **Mobile:** Formulário em coluna única
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 2 colunas otimizado

#### Acessibilidade (WCAG AA)
- Labels claros em português
- Campos bloqueados com tooltip explicativo
- Navegação por teclado
- Screen reader: anunciar campos bloqueados e motivo

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO (UC04)

### 8.1 Intenção da Tela
Evitar exclusões acidentais de parâmetros do sistema, com proteção reforçada para parâmetros críticos (Fl_Sistema = 1).

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Modal de Confirmação | Modal | Diálogo de confirmação |
| CMP-WF05-002 | Ícone de Aviso | Icon | Triângulo vermelho |
| CMP-WF05-003 | Título | Text | "Confirmar Exclusão" |
| CMP-WF05-004 | Mensagem | Text | "Tem certeza que deseja excluir o parâmetro '{Cd_Parametro}'? Esta ação não pode ser desfeita." |
| CMP-WF05-005 | Detalhes do Registro | Card | Cd_Parametro, Nm_Parametro, Categoria, Tipo_Dado |
| CMP-WF05-006 | Botão Excluir | Button | Ação destrutiva (vermelho) |
| CMP-WF05-007 | Botão Cancelar | Button | Ação secundária (cinza) |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Confirmação de Exclusão | Usuário clica em CMP-WF05-006 | UC04 | FP-UC04-007 |
| EVT-WF05-002 | Cancelamento | Usuário clica em CMP-WF05-007 | UC04 | FA-UC04-001 |
| EVT-WF05-003 | Fechar Modal (Esc) | Usuário pressiona Esc | UC04 | FA-UC04-001 |

### 8.4 Regras Obrigatórias

#### Bloqueio de Exclusão de Parâmetros de Sistema
- Se Fl_Sistema = 1, botão "Excluir" em WF-03 (Visualizar) e WF-01 (Listagem) deve ser:
  - Desabilitado (cinza) com tooltip: "Parâmetros de sistema não podem ser excluídos"
  - OU oculto completamente
- Tentativa de exclusão via API retorna HTTP 403

#### Exclusão Sempre Lógica (Soft Delete)
- Exclusão NUNCA é física (DELETE do banco)
- Atualizar: Fl_Excluido = 1, Dt_Exclusao = timestamp, Id_Usuario_Exclusao = ID usuário

#### Confirmação Explícita Obrigatória
- Sempre exigir confirmação via modal antes de executar exclusão
- Modal deve exibir detalhes do registro a ser excluído

### 8.5 Estados Obrigatórios

#### Estado 1: Modal Aberto (Aguardando Confirmação)
**Quando:** Usuário clica em "Excluir" em WF-01 ou WF-03

**Exibir:**
- Modal de confirmação (CMP-WF05-001)
- Ícone de aviso (CMP-WF05-002)
- Mensagem clara (CMP-WF05-004)
- Detalhes do registro (CMP-WF05-005)
- Botões: "Excluir" (vermelho), "Cancelar" (cinza)

#### Estado 2: Processando Exclusão
**Quando:** Usuário confirma exclusão

**Exibir:**
- Loading spinner no botão "Excluir"
- Botões desabilitados temporariamente

#### Estado 3: Sucesso
**Quando:** Exclusão bem-sucedida

**Exibir:**
- Fechar modal
- Toast de sucesso: "Parâmetro '{Cd_Parametro}' excluído com sucesso"
- Redirecionar para listagem (WF-01)

#### Estado 4: Erro (HTTP 403)
**Quando:** Tentativa de excluir parâmetro de sistema

**Exibir:**
- Fechar modal
- Toast de erro: "Parâmetros de sistema não podem ser excluídos via interface."

#### Estado 5: Erro (HTTP 404)
**Quando:** Registro já foi excluído ou não pertence ao tenant

**Exibir:**
- Fechar modal
- Toast de erro: "Parâmetro não encontrado ou já foi excluído"

### 8.6 Contratos de Comportamento

#### Auditoria Obrigatória
- Após exclusão bem-sucedida, registrar em Sistema_Parametro_Historico:
  - Tipo: DELETE
  - Valor anterior: JSON completo do registro
  - Valor novo: NULL
  - Id_Usuario, Dt_Alteracao, IP, User-Agent

#### Invalidação de Cache
- Após exclusão, invalidar cache de configurações

#### Responsividade
- **Mobile:** Modal em tela cheia com botões empilhados
- **Tablet:** Modal centralizado (50% largura)
- **Desktop:** Modal centralizado (30% largura)

#### Acessibilidade (WCAG AA)
- Foco automático no botão "Cancelar" ao abrir modal
- Navegação por teclado (Tab, Enter confirma, Esc cancela)
- Screen reader: anunciar "Diálogo de confirmação de exclusão"

---

## 9. WF-06 A WF-10 — ENTIDADE SISTEMA_FEATURE_FLAG (UC05-UC09)

### 9.1 Estrutura Geral
As telas de **Sistema_Feature_Flag** (WF-06 a WF-10) seguem a **mesma estrutura** de Sistema_Parametro (WF-01 a WF-05), com adaptações específicas:

### 9.2 Diferenças Principais

#### WF-06: Listagem de Feature Flags (UC05)
- Colunas adicionais: `Status` (On/Off), `Data_Inicio`, `Data_Fim`, `Percentual_Ativacao`
- Filtro adicional: Status (Ativo, Inativo, Agendado)
- Indicador visual: Badge verde (On) / vermelho (Off)

#### WF-07: Criar Feature Flag (UC06)
- Campos específicos:
  - `Chave_Flag` (único no tenant)
  - `Nome`
  - `Descricao`
  - `Status` (On/Off)
  - `Data_Inicio` (opcional, datetime picker)
  - `Data_Fim` (opcional, datetime picker)
  - `Percentual_Ativacao` (0-100%, slider)
  - `Usuarios_Alvo` (JSON array, textarea)
  - `Conglomerados_Alvo` (JSON array, textarea)

#### WF-08: Visualizar Feature Flag (UC07)
- Card adicional: **Status e Agendamento**
  - Status atual (On/Off com badge)
  - Data início/fim
  - Percentual de ativação
  - Usuários/Conglomerados alvo

#### WF-09: Editar Feature Flag (UC08)
- Permite editar status (On/Off) em tempo real
- Validação: Data_Fim >= Data_Inicio
- Validação: Percentual entre 0-100

#### WF-10: Confirmação de Exclusão (UC09)
- Aviso adicional se flag estiver ativa: "Esta flag está ATIVA (On). Tem certeza que deseja excluí-la?"

---

## 10. WF-11 A WF-15 — ENTIDADE SISTEMA_CONFIGURACAO_EMAIL (UC10-UC14)

### 10.1 Estrutura Geral
As telas de **Sistema_Configuracao_Email** (WF-11 a WF-15) seguem estrutura similar, com funcionalidades específicas de SMTP:

### 10.2 Diferenças Principais

#### WF-11: Listagem de Configurações de Email (UC10)
- Colunas: `Nome_Configuracao`, `Servidor_SMTP`, `Porta`, `Usuario`, `Fl_SSL`, `Status_Conexao`
- Badge de status: Verde (Conectado) / Vermelho (Erro) / Cinza (Não Testado)

#### WF-12: Criar Configuração de Email (UC11)
- Campos específicos:
  - `Nome_Configuracao`
  - `Servidor_SMTP` (hostname)
  - `Porta` (25, 587, 465)
  - `Usuario` (email)
  - `Senha` (password, criptografado)
  - `Fl_SSL` (checkbox)
  - `Fl_TLS` (checkbox)
  - `Email_Remetente` (email padrão)
  - `Nome_Remetente` (texto)
- Botão adicional: **Testar Conexão** (aciona UC21)

#### WF-13: Visualizar Configuração de Email (UC12)
- Card adicional: **Status de Conexão**
  - Último teste: timestamp
  - Resultado: Sucesso / Falha
  - Mensagem de erro (se falha)
- Botão: **Testar Conexão Agora** (aciona UC21)

#### WF-14: Editar Configuração de Email (UC13)
- Senha sempre mascarada (`*****`)
- Opção: "Alterar senha" (checkbox) para habilitar edição
- Botão: **Testar Conexão** antes de salvar

#### WF-15: Confirmação de Exclusão (UC14)
- Aviso adicional se configuração for padrão: "Esta é a configuração padrão de email. Tem certeza que deseja excluí-la?"

---

## 11. WF-16 A WF-20 — ENTIDADE SISTEMA_LIMITE_USO (UC15-UC19)

### 11.1 Estrutura Geral
As telas de **Sistema_Limite_Uso** (WF-16 a WF-20) gerenciam quotas e limites do sistema:

### 11.2 Diferenças Principais

#### WF-16: Listagem de Limites de Uso (UC15)
- Colunas: `Recurso`, `Limite_Maximo`, `Uso_Atual`, `Percentual_Uso`, `Status`
- Indicadores visuais:
  - Badge verde: < 70%
  - Badge amarelo: 70-90%
  - Badge vermelho: > 90%
- Barra de progresso em cada linha

#### WF-17: Criar Limite de Uso (UC16)
- Campos específicos:
  - `Tipo_Recurso` (dropdown: API_Calls, Storage, Users, Emails, etc.)
  - `Limite_Maximo` (integer)
  - `Threshold_Aviso` (70%, 80%, 90%)
  - `Threshold_Bloqueio` (95%, 100%)
  - `Fl_Notificar_Usuario` (checkbox)
  - `Fl_Bloquear_Acao` (checkbox)

#### WF-18: Visualizar Limite de Uso (UC17)
- Card adicional: **Uso Atual e Alertas**
  - Uso atual (valor absoluto e %)
  - Barra de progresso
  - Status: Normal / Aviso / Crítico / Bloqueado
  - Último job de verificação (UC20)
- Card: **Histórico de Uso** (gráfico de linha, últimos 7 dias)

#### WF-19: Editar Limite de Uso (UC18)
- Validação: Limite_Maximo >= Uso_Atual
- Aviso se reduzir limite abaixo do uso atual: "O uso atual ({valor}) ultrapassa o novo limite ({novo_limite}). Isto bloqueará novas ações."

#### WF-20: Confirmação de Exclusão (UC19)
- Aviso adicional: "Excluir este limite permitirá uso ilimitado do recurso '{Tipo_Recurso}'. Tem certeza?"

---

## 12. WF-21 — DASHBOARD DE JOBS BACKGROUND (UC20)

### 12.1 Intenção da Tela
Monitorar execução do **Job Background - Verificação de Limites de Uso**, executado periodicamente pelo Hangfire.

### 12.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF21-001 | Card Última Execução | Card | Timestamp, duração, status |
| CMP-WF21-002 | Card Estatísticas | Card | Total limites verificados, alertas gerados, bloqueios aplicados |
| CMP-WF21-003 | Tabela de Execuções Recentes | DataTable | Últimas 20 execuções |
| CMP-WF21-004 | Tabela de Alertas Gerados | DataTable | Alertas gerados na última execução |
| CMP-WF21-005 | Botão Executar Agora | Button | Trigger manual do job |
| CMP-WF21-006 | Indicador de Status | Badge | Sucesso (verde) / Erro (vermelho) |

### 12.3 Estados Obrigatórios

#### Estado 1: Carregando
- Skeleton loader (cards e tabelas)

#### Estado 2: Dados Exibidos
- Cards com estatísticas
- Tabela de execuções recentes
- Tabela de alertas gerados

#### Estado 3: Job em Execução
- Badge "Executando..." (amarelo)
- Botão "Executar Agora" desabilitado
- Atualização automática a cada 5 segundos

---

## 13. WF-22 — TESTE DE INTEGRAÇÃO SMTP (UC21)

### 13.1 Intenção da Tela
Interface para **testar conexão e envio de email SMTP** usando configuração de email selecionada.

### 13.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF22-001 | Dropdown Configuração | Dropdown | Selecionar configuração de email (de Sistema_Configuracao_Email) |
| CMP-WF22-002 | Campo Email Destino | Input | Email para enviar teste |
| CMP-WF22-003 | Campo Assunto | Input | Assunto do email de teste |
| CMP-WF22-004 | Textarea Corpo | Textarea | Corpo do email de teste |
| CMP-WF22-005 | Botão Enviar Teste | Button | Ação primária (trigger envio) |
| CMP-WF22-006 | Card Resultado | Card | Exibe resultado do teste |
| CMP-WF22-007 | Indicador de Status | Badge | Sucesso (verde) / Falha (vermelho) |
| CMP-WF22-008 | Log de Envio | Textarea | Log técnico do SMTP (apenas para Super Admin) |

### 13.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF22-001 | Enviar Teste | Usuário clica em CMP-WF22-005 | UC21 | FP-UC21-001 |

### 13.4 Estados Obrigatórios

#### Estado 1: Inicial
- Formulário vazio
- Dropdown com configurações disponíveis
- Valores padrão: Assunto "Teste de Conexão SMTP", Corpo "Este é um email de teste."

#### Estado 2: Enviando
- Loading spinner no botão "Enviar Teste"
- Campos desabilitados

#### Estado 3: Sucesso
- Card Resultado (CMP-WF22-006) exibe:
  - Badge verde "Sucesso"
  - Mensagem: "Email enviado com sucesso para {email_destino}"
  - Timestamp do envio
- Log de envio (se Super Admin)

#### Estado 4: Falha
- Card Resultado exibe:
  - Badge vermelho "Falha"
  - Mensagem de erro: "Erro ao enviar email: {erro}"
  - Possíveis causas (autenticação, timeout, porta bloqueada)
- Log de envio com stack trace (se Super Admin)

---

## 14. NOTIFICAÇÕES PADRONIZADAS

### 14.1 Tipos de Notificações

| Tipo | Uso | Cor | Ícone |
|----|----|-----|-------|
| Sucesso | Operação concluída (criação, edição, exclusão) | Verde | Checkmark |
| Erro | Falha bloqueante (validação, permissão, API) | Vermelho | X |
| Aviso | Atenção necessária (conflito, limite próximo) | Amarelo | Triângulo |
| Info | Feedback neutro (cache invalidado, job executado) | Azul | i |

### 14.2 Mensagens Padronizadas

#### Sucesso
- "Parâmetro '{Cd_Parametro}' criado com sucesso"
- "Parâmetro '{Cd_Parametro}' atualizado com sucesso"
- "Parâmetro '{Cd_Parametro}' excluído com sucesso"
- "Feature flag '{Chave_Flag}' ativada com sucesso"
- "Email de teste enviado com sucesso"

#### Erro
- "Acesso negado. Você não tem permissão para {ação}"
- "Parâmetro não encontrado"
- "Código '{Cd_Parametro}' já existe neste conglomerado"
- "Valor inválido para tipo {Tipo_Dado}"
- "Erro ao carregar dados. Tente novamente."

#### Aviso
- "O registro foi alterado por outro usuário. Recarregar?"
- "O uso atual ultrapassa o novo limite. Isto bloqueará novas ações."
- "Esta flag está ATIVA. Tem certeza que deseja excluí-la?"

---

## 15. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| **Mobile (< 768px)** | - Layout em coluna única<br>- Tabelas convertidas em cards empilhados<br>- Filtros em modal/drawer<br>- Botões empilhados verticalmente |
| **Tablet (768px - 1024px)** | - Layout em 2 colunas<br>- Tabelas simplificadas (4-5 colunas principais)<br>- Filtros em linha (collapsible)<br>- Botões horizontais |
| **Desktop (> 1024px)** | - Layout completo (3 colunas em cards)<br>- Tabelas completas (todas colunas)<br>- Filtros sempre visíveis<br>- Ações em linha (icon buttons) |

---

## 16. ACESSIBILIDADE (OBRIGATÓRIO — WCAG AA)

### 16.1 Navegação por Teclado
- **Tab:** Navegar entre campos/botões
- **Shift+Tab:** Navegar para trás
- **Enter:** Confirmar ação (salvar, excluir)
- **Esc:** Cancelar ação (fechar modal, cancelar edição)
- **Espaço:** Marcar checkbox, abrir dropdown

### 16.2 Screen Readers
- Labels claros em português (sem abreviações)
- Aria-label em botões de ícone:
  - "Editar parâmetro {Cd_Parametro}"
  - "Excluir parâmetro {Cd_Parametro}"
- Anúncio de estados:
  - "Carregando parâmetros..."
  - "Nenhum parâmetro encontrado"
  - "Erro ao carregar. Tente novamente."
- Anúncio de erros de validação:
  - "Campo {campo} é obrigatório"
  - "Valor inválido para tipo {tipo}"

### 16.3 Contraste (WCAG AA)
- Contraste mínimo: 4.5:1 (texto normal)
- Contraste mínimo: 3:1 (texto grande, ícones)
- Estados de foco claramente visíveis (outline azul 2px)

### 16.4 Labels e Descrições
- Todos os campos com `<label>` associado
- Campos obrigatórios marcados com asterisco (*) e aria-required="true"
- Tooltips em campos complexos (Regex_Validacao, Opcoes_Validas)

---

## 17. RASTREABILIDADE COMPLETA (RF → UC → WF)

| Wireframe | UC | Entidade | RF |
|---------|----|---------|----|
| WF-01 | UC00 | Sistema_Parametro | RF001 |
| WF-02 | UC01 | Sistema_Parametro | RF001 |
| WF-03 | UC02 | Sistema_Parametro | RF001 |
| WF-04 | UC03 | Sistema_Parametro | RF001 |
| WF-05 | UC04 | Sistema_Parametro | RF001 |
| WF-06 | UC05 | Sistema_Feature_Flag | RF001 |
| WF-07 | UC06 | Sistema_Feature_Flag | RF001 |
| WF-08 | UC07 | Sistema_Feature_Flag | RF001 |
| WF-09 | UC08 | Sistema_Feature_Flag | RF001 |
| WF-10 | UC09 | Sistema_Feature_Flag | RF001 |
| WF-11 | UC10 | Sistema_Configuracao_Email | RF001 |
| WF-12 | UC11 | Sistema_Configuracao_Email | RF001 |
| WF-13 | UC12 | Sistema_Configuracao_Email | RF001 |
| WF-14 | UC13 | Sistema_Configuracao_Email | RF001 |
| WF-15 | UC14 | Sistema_Configuracao_Email | RF001 |
| WF-16 | UC15 | Sistema_Limite_Uso | RF001 |
| WF-17 | UC16 | Sistema_Limite_Uso | RF001 |
| WF-18 | UC17 | Sistema_Limite_Uso | RF001 |
| WF-19 | UC18 | Sistema_Limite_Uso | RF001 |
| WF-20 | UC19 | Sistema_Limite_Uso | RF001 |
| WF-21 | UC20 | Job Background | RF001 |
| WF-22 | UC21 | Integração SMTP | RF001 |

**Total:** 22 Wireframes cobrindo 100% dos 22 Casos de Uso

---

## 18. NÃO-OBJETIVOS (OUT OF SCOPE)

Este documento **NÃO define**:

- Estilo visual final (cores específicas, tipografia, espaçamentos exatos)
- Escolha de framework frontend (Filament, React, Vue, Angular)
- Design gráfico definitivo (ilustrações, animações, transições)
- Implementação técnica (código HTML/CSS/JS)
- Performance (lazy loading, virtual scrolling, etc.)

---

## 19. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 1.0 | 2026-01-04 | Agência ALC - alc.dev.br | Criação dos wireframes para RF001 cobrindo 100% dos UCs (UC00-UC21), incluindo 4 entidades CRUD + 2 funcionalidades especiais (jobs, integrações). Estados obrigatórios (Loading, Vazio, Erro, Dados) aplicados em todos os wireframes. Responsividade (Mobile, Tablet, Desktop) e Acessibilidade (WCAG AA) garantidas. |

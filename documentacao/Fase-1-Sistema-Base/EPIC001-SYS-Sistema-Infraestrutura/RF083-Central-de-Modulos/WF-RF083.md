# WF-RF083 — Wireframes Canônicos (UI Contract)

**Versão:** 1.0
**Data:** 2026-01-30
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF083 - Central de Módulos
**UC Relacionado:** UC-RF083 (UC00 a UC07)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF083 - Central de Módulos.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional**
- Servir como **fonte de verdade para IA, QA e Desenvolvimento**
- Permitir derivação direta de **TCs E2E e testes de usabilidade**
- Evitar dependência de ferramentas específicas (ex: Filament, React, Vue)

> **NOTA ESPECIAL:** Este é um módulo de SISTEMA
> - Funcionalidades são GLOBAIS (não isoladas por tenant)
> - Acesso filtrado por PERFIL (Developer/System/Tenant)
> - Interface predominantemente de LEITURA e CONSULTA (não CRUD tradicional)

---

## 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)

### 2.1 Princípios Gerais

- Clareza acima de estética
- Feedback imediato a toda ação do usuário
- Estados explícitos (loading, vazio, erro)
- Não ocultar erros críticos
- Comportamento previsível
- Hierarquia visual clara (categorias > funcionalidades > ações)

### 2.2 Padrões Globais

| Item | Regra |
|------|-------|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas (ex: Reset) |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória |
| Filtros por perfil | Automáticos e transparentes |

### 2.3 Padrões Específicos do Módulo

| Item | Regra |
|------|-------|
| Agrupamento | Funcionalidades agrupadas por categoria |
| Expansão | Categorias colapsáveis |
| Hierarquia | Indentação visual para funcionalidades filhas |
| Permissões | Ações visíveis apenas para perfis autorizados |
| Exclusividade | Badge "Exclusivo" em funcionalidades restritas |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|------|----------------------|------------|
| WF-01 | Listagem de Funcionalidades | UC00, UC02, UC06, UC07 | Descoberta, filtro, navegação |
| WF-02 | Detalhes da Funcionalidade | UC01 | Consulta detalhada |
| WF-03 | Dashboard de Estatísticas | UC03 | Visão geral do catálogo |
| WF-04 | Modal Empresas Exclusivas | UC04 | Gerenciamento de exclusividade |
| WF-05 | Confirmação de Reset | UC05 | Ação destrutiva |

---

## 4. WF-01 — LISTAGEM DE FUNCIONALIDADES

### 4.1 Intenção da Tela

Permitir ao usuário **visualizar, filtrar e navegar pelo catálogo de funcionalidades** do sistema, agrupadas por categoria, com suporte a expansão/contração de grupos e filtros em tempo real.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF01-001 | Campo de Busca | Input | Busca por nome ou código da funcionalidade | Sim |
| CMP-WF01-002 | Filtro de Categoria | Dropdown | Filtrar por categoria específica | Não |
| CMP-WF01-003 | Filtro de Status | Dropdown | Filtrar por ativo/inativo | Não |
| CMP-WF01-004 | Botão Limpar Filtros | Button | Limpar todos os filtros aplicados | Sim |
| CMP-WF01-005 | Grupo de Categoria | Collapsible | Agrupamento de funcionalidades por categoria | Sim |
| CMP-WF01-006 | Botão Expandir/Contrair | IconButton | Expandir ou contrair categoria | Sim |
| CMP-WF01-007 | Item de Funcionalidade | ListItem | Exibição de uma funcionalidade (nome, código, ícone) | Sim |
| CMP-WF01-008 | Badge de Exclusividade | Badge | Indica funcionalidade com acesso exclusivo | Não |
| CMP-WF01-009 | Indicador de Hierarquia | Visual | Indentação para funcionalidades filhas | Não |
| CMP-WF01-010 | Botão Estatísticas | Button | Acessar dashboard de estatísticas | Sim |
| CMP-WF01-011 | Botão Reset | Button | Resetar funcionalidades (apenas Developer) | Não |
| CMP-WF01-012 | Lista de Ações | ActionList | Ações associadas à funcionalidade | Não |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Busca textual | Usuário digita em CMP-WF01-001 | UC07 | FP-UC07-002 |
| EVT-WF01-002 | Filtro por categoria | Usuário seleciona CMP-WF01-002 | UC02 | FP-UC02-001 |
| EVT-WF01-003 | Filtro por status | Usuário seleciona CMP-WF01-003 | UC07 | FA-UC07-001 |
| EVT-WF01-004 | Limpar filtros | Usuário clica CMP-WF01-004 | UC07 | FA-UC07-003 |
| EVT-WF01-005 | Expandir categoria | Usuário clica CMP-WF01-006 (expandido=false) | UC06 | FP-UC06-002 |
| EVT-WF01-006 | Contrair categoria | Usuário clica CMP-WF01-006 (expandido=true) | UC06 | FP-UC06-002 |
| EVT-WF01-007 | Selecionar funcionalidade | Usuário clica CMP-WF01-007 | UC01 | FP-UC01-001 |
| EVT-WF01-008 | Acessar estatísticas | Usuário clica CMP-WF01-010 | UC03 | FP-UC03-001 |
| EVT-WF01-009 | Acessar reset | Usuário clica CMP-WF01-011 | UC05 | FP-UC05-003 |
| EVT-WF01-010 | Carregar página | Sistema carrega lista de funcionalidades | UC00 | FP-UC00-001 |

### 4.4 Ações Permitidas

- Visualizar lista de funcionalidades agrupadas por categoria
- Buscar funcionalidades por nome ou código
- Filtrar por categoria específica
- Filtrar por status (ativo/inativo)
- Limpar todos os filtros
- Expandir/contrair categorias
- Selecionar funcionalidade para ver detalhes
- Acessar dashboard de estatísticas
- Acessar reset de funcionalidades (apenas Developer/Super Admin)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)

**Quando:** Sistema está buscando funcionalidades da API
**Exibir:**
- Skeleton loader (grupos de categorias)
- Mensagem: "Carregando funcionalidades..."

**data-test:** `loading-spinner`

#### Estado 2: Vazio (Sem Dados)

**Quando:** Não há funcionalidades após aplicar filtro
**Exibir:**
- Ícone ilustrativo (lista vazia)
- Mensagem: "Nenhuma funcionalidade encontrada para os filtros aplicados"
- Botão "Limpar Filtros"

**data-test:** `empty-state`

#### Estado 3: Erro (Falha ao Carregar)

**Quando:** API retorna erro (500, 403, etc.)
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar funcionalidades. Tente novamente."
- Botão "Recarregar"

**data-test:** `error-state`

#### Estado 4: Dados (Lista Exibida)

**Quando:** Há funcionalidades disponíveis
**Exibir:**
- Grupos de categorias colapsáveis
- Funcionalidades ordenadas por ordem e nome
- Badges de exclusividade quando aplicável
- Contagem de funcionalidades por categoria

**data-test:** `funcionalidades-list`

### 4.6 Contratos de Comportamento

#### Isolamento por Perfil (RN-RF083-02)

| Perfil | Visibilidade |
|--------|--------------|
| Developer | Todas as funcionalidades (Sistema + Corporativo) |
| System | Corporativo + Sistema |
| Tenant | Apenas Corporativo |

#### Responsividade

- **Mobile:** Lista simplificada em cards, categorias em acordeão
- **Tablet:** Lista com ícones, categorias colapsáveis
- **Desktop:** Lista completa com ações inline, todas as colunas

#### Acessibilidade (WCAG AA)

- Labels em português claro
- Botões expandir/contrair com aria-expanded
- Navegação por teclado (Tab, Enter, Space)
- Contraste mínimo 4.5:1
- Screen reader: anúncio de categoria e quantidade de itens

#### Feedback ao Usuário

- Filtros aplicados em tempo real
- Estado de filtro ativo visualmente destacado
- Toast de erro em caso de falha de API
- Preferência de expansão persistida em localStorage

---

## 5. WF-02 — DETALHES DA FUNCIONALIDADE

### 5.1 Intenção da Tela

Permitir ao usuário **visualizar informações completas** de uma funcionalidade específica, incluindo ações associadas, funcionalidades filhas e empresas com acesso exclusivo.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF02-001 | Cabeçalho da Funcionalidade | Header | Nome, código e ícone | Sim |
| CMP-WF02-002 | Badge de Status | Badge | Indica se funcionalidade está ativa | Sim |
| CMP-WF02-003 | Descrição | Text | Descrição detalhada da funcionalidade | Não |
| CMP-WF02-004 | Código | Text | Código no formato FF.[CAMADA].[MODULO] | Sim |
| CMP-WF02-005 | Rota | Text | Rota do frontend | Não |
| CMP-WF02-006 | Categoria | Badge | Categoria da funcionalidade | Sim |
| CMP-WF02-007 | Funcionalidade Pai | Link | Link para funcionalidade pai (se houver) | Não |
| CMP-WF02-008 | Lista de Ações | List | Ações associadas (VIEW, CREATE, UPDATE, etc.) | Sim |
| CMP-WF02-009 | Lista de Filhas | List | Funcionalidades filhas (se houver) | Não |
| CMP-WF02-010 | Lista de Exclusivas | BadgeList | Empresas com acesso exclusivo | Sim |
| CMP-WF02-011 | Botão Gerenciar Exclusivas | Button | Abre modal de gerenciamento (apenas Developer) | Não |
| CMP-WF02-012 | Feature Flag | Badge | Indica vinculação com Feature Flag | Não |
| CMP-WF02-013 | Permissão Requerida | Text | Código de permissão RBAC | Não |
| CMP-WF02-014 | Botão Voltar | Button | Retorna à listagem | Sim |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Carregar detalhes | Sistema carrega funcionalidade por ID | UC01 | FP-UC01-003 |
| EVT-WF02-002 | Clique em pai | Usuário clica em CMP-WF02-007 | UC01 | - |
| EVT-WF02-003 | Clique em filha | Usuário clica em item de CMP-WF02-009 | UC01 | - |
| EVT-WF02-004 | Gerenciar exclusivas | Usuário clica CMP-WF02-011 | UC04 | FP-UC04-003 |
| EVT-WF02-005 | Voltar | Usuário clica CMP-WF02-014 | - | - |

### 5.4 Ações Permitidas

- Visualizar informações completas da funcionalidade
- Navegar para funcionalidade pai
- Navegar para funcionalidades filhas
- Gerenciar empresas exclusivas (apenas Developer)
- Voltar para listagem

### 5.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)

**Quando:** Sistema está carregando dados da funcionalidade
**Exibir:**
- Skeleton loader (painel de detalhes)
- Mensagem: "Carregando detalhes..."

#### Estado 2: Erro (Funcionalidade Não Encontrada)

**Quando:** API retorna 404
**Exibir:**
- Ícone de erro
- Mensagem: "Funcionalidade não encontrada"
- Botão "Voltar para Listagem"

#### Estado 3: Erro (Falha ao Carregar)

**Quando:** API retorna erro (500, 403, etc.)
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar funcionalidade. Tente novamente."
- Botão "Recarregar"

#### Estado 4: Dados (Detalhes Exibidos)

**Quando:** Funcionalidade carregada com sucesso
**Exibir:**
- Todos os componentes com dados preenchidos
- Seções vazias ocultadas ou com mensagem "Nenhum(a)"
- Botão de gerenciar exclusivas apenas para Developer

**data-test:** `funcionalidade-detalhes`

### 5.6 Contratos de Comportamento

#### Exibição de Empresas Exclusivas (RN-RF083-03)

- Lista vazia = "Disponível para todas as empresas"
- Lista preenchida = badges com nomes das empresas

#### Responsividade

- **Mobile:** Seções empilhadas, listas em acordeão
- **Tablet:** Layout em duas colunas
- **Desktop:** Layout completo com sidebar de ações

#### Acessibilidade (WCAG AA)

- Hierarquia de headings correta (h1 > h2 > h3)
- Links navegáveis por teclado
- Listas com role="list" e aria-label

---

## 6. WF-03 — DASHBOARD DE ESTATÍSTICAS

### 6.1 Intenção da Tela

Permitir ao usuário **visualizar métricas agregadas** do catálogo de funcionalidades, incluindo totais, distribuição por categoria e status.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF03-001 | Card Total Funcionalidades | Counter | Total de funcionalidades cadastradas | Sim |
| CMP-WF03-002 | Card Total Ações | Counter | Total de ações associadas | Sim |
| CMP-WF03-003 | Card Funcionalidades Ativas | Counter | Funcionalidades com ativo=true | Sim |
| CMP-WF03-004 | Gráfico por Categoria | Chart | Distribuição de funcionalidades por categoria | Sim |
| CMP-WF03-005 | Botão Voltar | Button | Retorna à listagem | Sim |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Carregar estatísticas | Sistema carrega endpoint /estatisticas | UC03 | FP-UC03-003 |
| EVT-WF03-002 | Clique em categoria | Usuário clica em segmento do gráfico | UC02 | FP-UC02-001 |
| EVT-WF03-003 | Voltar | Usuário clica CMP-WF03-005 | - | - |

### 6.4 Ações Permitidas

- Visualizar totais de funcionalidades e ações
- Visualizar distribuição por categoria
- Navegar para listagem filtrada por categoria (clique no gráfico)
- Voltar para listagem principal

### 6.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)

**Quando:** Sistema está calculando estatísticas
**Exibir:**
- Skeleton loader (cards e gráfico)
- Mensagem: "Calculando estatísticas..."

#### Estado 2: Erro (Falha ao Carregar)

**Quando:** API retorna erro
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar estatísticas. Tente novamente."
- Botão "Recarregar"

#### Estado 3: Dados (Estatísticas Exibidas)

**Quando:** Dados carregados com sucesso
**Exibir:**
- Cards com valores numéricos
- Gráfico de pizza/barras por categoria
- Comparativo ativas vs inativas

**data-test:** `estatisticas-dashboard`

### 6.6 Contratos de Comportamento

#### Cálculo (RN-RF083-14)

- Apenas registros ativos e não excluídos são contabilizados
- Funcionalidades filtradas por perfil do usuário

#### Responsividade

- **Mobile:** Cards empilhados, gráfico em tela cheia
- **Tablet:** Grid 2x2 de cards, gráfico abaixo
- **Desktop:** Grid 3 colunas de cards, gráfico lateral

---

## 7. WF-04 — MODAL DE EMPRESAS EXCLUSIVAS

### 7.1 Intenção da Tela

Permitir ao Developer **definir quais empresas têm acesso exclusivo** a uma funcionalidade específica (modelo whitelist).

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF04-001 | Título do Modal | Header | "Gerenciar Empresas Exclusivas" | Sim |
| CMP-WF04-002 | Descrição | Text | Explicação do modelo whitelist | Sim |
| CMP-WF04-003 | Lista de Empresas | CheckboxList | Empresas disponíveis com checkbox | Sim |
| CMP-WF04-004 | Campo de Busca | Input | Buscar empresa por nome | Não |
| CMP-WF04-005 | Botão Confirmar | Button | Salvar alterações | Sim |
| CMP-WF04-006 | Botão Cancelar | Button | Fechar sem salvar | Sim |
| CMP-WF04-007 | Alerta Whitelist | Alert | "Lista vazia = todas as empresas" | Sim |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Abrir modal | Sistema carrega lista de empresas | UC04 | FP-UC04-004 |
| EVT-WF04-002 | Selecionar empresa | Usuário marca checkbox em CMP-WF04-003 | UC04 | FP-UC04-005 |
| EVT-WF04-003 | Desselecionar empresa | Usuário desmarca checkbox | UC04 | FA-UC04-001 |
| EVT-WF04-004 | Buscar empresa | Usuário digita em CMP-WF04-004 | UC04 | - |
| EVT-WF04-005 | Confirmar | Usuário clica CMP-WF04-005 | UC04 | FP-UC04-006 |
| EVT-WF04-006 | Cancelar | Usuário clica CMP-WF04-006 | UC04 | FA-UC04-002 |

### 7.4 Ações Permitidas

- Visualizar lista de empresas do sistema
- Selecionar/desselecionar empresas
- Buscar empresa por nome
- Confirmar alterações
- Cancelar sem salvar

### 7.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)

**Quando:** Sistema está carregando lista de empresas
**Exibir:**
- Skeleton loader (lista)
- Mensagem: "Carregando empresas..."

#### Estado 2: Erro (Falha ao Carregar)

**Quando:** API retorna erro
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar empresas. Tente novamente."
- Botão "Recarregar"

#### Estado 3: Salvando

**Quando:** Sistema está persistindo alterações
**Exibir:**
- Botão Confirmar desabilitado com spinner
- Mensagem: "Salvando..."

#### Estado 4: Dados (Lista Exibida)

**Quando:** Empresas carregadas
**Exibir:**
- Lista de checkboxes com empresas
- Empresas já selecionadas pré-marcadas
- Alerta sobre modelo whitelist

**data-test:** `modal-empresas-exclusivas`

### 7.6 Contratos de Comportamento

#### Permissão (RN-RF083-04)

- Modal visível APENAS para Developer
- Outros perfis não veem o botão de gerenciar

#### Modelo Whitelist (RN-RF083-03)

- Nenhuma empresa selecionada = funcionalidade disponível para TODAS
- Empresas selecionadas = apenas essas têm acesso

#### Responsividade

- **Mobile:** Modal full-screen
- **Tablet/Desktop:** Modal centralizado com scroll interno

#### Feedback ao Usuário

- Toast de sucesso: "Empresas exclusivas atualizadas"
- Toast de erro: "Erro ao salvar. Tente novamente."

**data-test:** `success-message`

---

## 8. WF-05 — CONFIRMAÇÃO DE RESET

### 8.1 Intenção da Tela

Evitar **reset acidental** de todas as funcionalidades do sistema, exigindo confirmação explícita com digitação de palavra-chave.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição | Obrigatório |
|----|-----------|------|-----------|-------------|
| CMP-WF05-001 | Título do Modal | Header | "Resetar Funcionalidades" | Sim |
| CMP-WF05-002 | Alerta Destrutivo | Alert | Aviso em vermelho sobre operação destrutiva | Sim |
| CMP-WF05-003 | Descrição das Consequências | Text | Lista de consequências da operação | Sim |
| CMP-WF05-004 | Campo de Confirmação | Input | Digitação de "CONFIRMAR" | Sim |
| CMP-WF05-005 | Botão Confirmar Reset | Button | Executa o reset (habilitado apenas com texto correto) | Sim |
| CMP-WF05-006 | Botão Cancelar | Button | Fecha modal sem ação | Sim |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Abrir modal | Usuário clica em Reset na listagem | UC05 | FP-UC05-004 |
| EVT-WF05-002 | Digitar confirmação | Usuário digita em CMP-WF05-004 | UC05 | FP-UC05-005 |
| EVT-WF05-003 | Confirmar reset | Usuário clica CMP-WF05-005 (com texto correto) | UC05 | FP-UC05-006 |
| EVT-WF05-004 | Cancelar | Usuário clica CMP-WF05-006 | UC05 | FA-UC05-001 |

### 8.4 Ações Permitidas

- Visualizar consequências da operação
- Digitar palavra-chave de confirmação
- Confirmar reset
- Cancelar operação

### 8.5 Estados Obrigatórios

#### Estado 1: Aguardando Confirmação

**Quando:** Modal aberto, aguardando digitação
**Exibir:**
- Alerta destrutivo em vermelho
- Lista de consequências
- Campo de confirmação vazio
- Botão Confirmar desabilitado

**data-test:** `modal-alerta-destrutivo`

#### Estado 2: Texto Incorreto

**Quando:** Usuário digitou algo diferente de "CONFIRMAR"
**Exibir:**
- Botão Confirmar permanece desabilitado
- Nenhuma mensagem de erro adicional

#### Estado 3: Texto Correto

**Quando:** Usuário digitou "CONFIRMAR" corretamente
**Exibir:**
- Botão Confirmar habilitado
- Visual indicando que ação está liberada

#### Estado 4: Processando Reset

**Quando:** Sistema está executando o reset
**Exibir:**
- Botão Confirmar com spinner
- Mensagem: "Resetando funcionalidades..."
- Modal não pode ser fechado

#### Estado 5: Sucesso

**Quando:** Reset concluído
**Exibir:**
- Modal fecha automaticamente
- Toast de sucesso: "Funcionalidades resetadas com sucesso"
- Lista recarrega automaticamente

**data-test:** `success-message`

#### Estado 6: Erro

**Quando:** Falha durante o reset (rollback)
**Exibir:**
- Modal permanece aberto
- Mensagem de erro: "Erro ao resetar. Operação revertida."
- Botão "Tentar Novamente"

### 8.6 Contratos de Comportamento

#### Permissão (RN-RF083-15)

- Operação disponível APENAS para Developer ou Super Admin
- Outros perfis não veem o botão de Reset

#### Segurança

- Confirmação via digitação de "CONFIRMAR" (case-sensitive)
- Operação em transação com rollback em caso de erro
- Auditoria obrigatória da operação

#### Consequências Listadas

1. Todas as funcionalidades atuais serão excluídas
2. Funcionalidades padrão serão recriadas
3. Configurações personalizadas serão perdidas
4. Empresas exclusivas serão resetadas
5. Operação não pode ser desfeita

#### Responsividade

- **Mobile:** Modal full-screen
- **Tablet/Desktop:** Modal centralizado

---

## 9. NOTIFICAÇÕES

### 9.1 Tipos Padronizados

| Tipo | Uso | Cor | Ícone |
|------|-----|-----|-------|
| Sucesso | Operação concluída | Verde | Check |
| Erro | Falha bloqueante | Vermelho | X |
| Aviso | Atenção necessária | Amarelo | Warning |
| Info | Feedback neutro | Azul | Info |

### 9.2 Mensagens Padrão do Módulo

| Contexto | Tipo | Mensagem |
|----------|------|----------|
| Salvar exclusivas | Sucesso | "Empresas exclusivas atualizadas com sucesso" |
| Salvar exclusivas | Erro | "Erro ao atualizar empresas exclusivas" |
| Reset | Sucesso | "Funcionalidades resetadas com sucesso" |
| Reset | Erro | "Erro ao resetar funcionalidades. Operação revertida." |
| Carregar lista | Erro | "Erro ao carregar funcionalidades. Tente novamente." |
| Carregar detalhes | Erro | "Funcionalidade não encontrada" |

---

## 10. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|----------|---------------|
| Mobile (< 768px) | Layout em coluna única, cards empilhados, modais full-screen |
| Tablet (768-1024px) | Layout em 2 colunas, categorias colapsáveis |
| Desktop (> 1024px) | Layout completo com 3+ colunas, sidebar de navegação |

### 10.1 Breakpoints Específicos

| Tela | Mobile | Tablet | Desktop |
|------|--------|--------|---------|
| WF-01 Listagem | Cards empilhados | Lista simplificada | Lista completa com ações |
| WF-02 Detalhes | Seções acordeão | 2 colunas | 3 colunas com sidebar |
| WF-03 Estatísticas | Cards verticais | Grid 2x2 | Grid 4 colunas |
| WF-04 Modal Exclusivas | Full-screen | Centralizado 70% | Centralizado 50% |
| WF-05 Modal Reset | Full-screen | Centralizado 70% | Centralizado 40% |

---

## 11. ACESSIBILIDADE (OBRIGATÓRIO)

### 11.1 Requisitos WCAG AA

- Navegação por teclado (Tab, Shift+Tab, Enter, Escape, Space)
- Leitura por screen readers (aria-labels, aria-describedby)
- Contraste mínimo 4.5:1 para texto
- Contraste mínimo 3:1 para componentes de UI
- Labels e descrições em português claro
- Focus visible em todos os elementos interativos

### 11.2 Especificações por Tela

| Tela | Requisitos |
|------|------------|
| WF-01 | Categorias com aria-expanded, lista com role="tree" |
| WF-02 | Headings hierárquicos, links com aria-label descritivo |
| WF-03 | Gráficos com descrição textual alternativa |
| WF-04 | Modal com aria-modal, foco preso dentro do modal |
| WF-05 | Campo de confirmação com aria-describedby para instruções |

---

## 12. RASTREABILIDADE

### 12.1 Wireframe → UC → RF

| Wireframe | UC(s) | Items Cobertos | RF |
|-----------|-------|----------------|-----|
| WF-01 | UC00, UC02, UC06, UC07 | Listagem, filtros, categorias | RF083 |
| WF-02 | UC01 | Detalhes da funcionalidade | RF083 |
| WF-03 | UC03 | Estatísticas | RF083 |
| WF-04 | UC04 | Gerenciar exclusivas | RF083 |
| WF-05 | UC05 | Reset funcionalidades | RF083 |

### 12.2 Cobertura de UCs

| UC | Nome | Wireframe | Cobertura |
|----|------|-----------|-----------|
| UC00 | Listar Funcionalidades | WF-01 | 100% |
| UC01 | Visualizar Funcionalidade | WF-02 | 100% |
| UC02 | Listar por Categoria | WF-01 | 100% |
| UC03 | Obter Estatísticas | WF-03 | 100% |
| UC04 | Gerenciar Empresas Exclusivas | WF-04 | 100% |
| UC05 | Resetar Funcionalidades | WF-05 | 100% |
| UC06 | Expandir/Contrair Categorias | WF-01 | 100% |
| UC07 | Filtrar Funcionalidades | WF-01 | 100% |

**Total: 8/8 UCs cobertos = 100%**

### 12.3 Cobertura de Regras de Negócio

| Regra | Descrição | Wireframe |
|-------|-----------|-----------|
| RN-RF083-02 | Isolamento por perfil | WF-01 |
| RN-RF083-03 | Empresas exclusivas (whitelist) | WF-02, WF-04 |
| RN-RF083-04 | Apenas Developer gerencia exclusivas | WF-04 |
| RN-RF083-05 | Soft delete | WF-01 (filtro) |
| RN-RF083-11 | Ordem de exibição | WF-01 |
| RN-RF083-14 | Estatísticas ativos/não excluídos | WF-03 |
| RN-RF083-15 | Reset apenas Developer/Super Admin | WF-05 |

---

## 13. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, fontes, espaçamentos)
- Escolha de framework (React, Vue, Angular)
- Design gráfico definitivo
- Animações avançadas
- Interface de drag-and-drop para ordenação
- CRUD completo de funcionalidades (gerenciado via código)

---

## 14. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2026-01-30 | Agência ALC - alc.dev.br | Criação inicial - 5 wireframes cobrindo 8 UCs (100%) |

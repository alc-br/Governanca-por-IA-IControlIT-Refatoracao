# WF-RF002 — Wireframes Canônicos (UI Contract)

**Versão:** 1.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF002 - Sistema de Configurações e Parametrização Avançada
**UC Relacionado:** UC-RF002 (UC00 a UC09)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF002 - Sistema de Configurações e Parametrização Avançada.

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
- Valores sensíveis sempre mascarados por padrão
- Confirmação obrigatória para ações destrutivas
- Hierarquia multi-tenant sempre respeitada

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Acessibilidade | WCAG AA obrigatório |
| Valores sensíveis | Mascarados como `********` por padrão |
| Auditoria | Motivo obrigatório para alterações críticas |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF002)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Configurações | UC00 | Descoberta, busca e acesso às configurações |
| WF-02 | Criar Configuração | UC01 | Entrada de nova configuração com validação |
| WF-03 | Visualizar Configuração | UC02 | Consulta detalhada com histórico |
| WF-04 | Editar Configuração | UC03 | Alteração controlada com versionamento |
| WF-05 | Confirmação de Exclusão | UC04 | Soft delete com confirmação |
| WF-06 | Histórico e Rollback | UC05 | Rollback 1-click com diff visual |
| WF-07 | Gerenciar Feature Flag | UC06 | Configuração de rollout progressivo |
| WF-08 | Exportar Configurações | UC07 | Export YAML com mascaramento |
| WF-09 | Importar Configurações | UC08 | Import YAML com dry-run |
| WF-10 | Descriptografar Valor | UC09 | Visualização temporária de valor sensível |

---

## 4. WF-01 — LISTAGEM DE CONFIGURAÇÕES (UC00)

### 4.1 Intenção da Tela
Permitir ao usuário **localizar, filtrar e acessar configurações** respeitando hierarquia multi-tenant e mascaramento de valores sensíveis.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Nova Configuração" | Button | Ação primária para criar nova configuração (exibido se usuário tiver permissão CREATE) |
| CMP-WF01-002 | Campo de Busca Global | Input | Busca por código, nome ou descrição (case-insensitive) |
| CMP-WF01-003 | Filtro de Categoria | Dropdown | Filtrar por: Sistema, Email, Integração, Segurança, Notificação, Cache, Storage, Auditoria, Performance, Features |
| CMP-WF01-004 | Filtro de Nível Hierárquico | Dropdown | Filtrar por: Global, Conglomerado, Empresa, Departamento, Usuário |
| CMP-WF01-005 | Checkbox "Apenas Sensíveis" | Checkbox | Filtrar configurações com `Fl_Criptografado = 1` |
| CMP-WF01-006 | Tabela de Configurações | DataTable | Grid hierarquizado por categoria com colunas: Código, Nome, Categoria, Tipo Dado, Valor (mascarado se sensível), Nível, Ações |
| CMP-WF01-007 | Botão Ver Detalhes | IconButton | Ação para visualizar configuração (cada linha) |
| CMP-WF01-008 | Botão Editar | IconButton | Ação para editar configuração (cada linha, se tiver permissão UPDATE) |
| CMP-WF01-009 | Botão Excluir | IconButton | Ação para excluir configuração (cada linha, se tiver permissão DELETE) |
| CMP-WF01-010 | Paginação | Pagination | Controles de navegação (padrão: 50 registros por página) |
| CMP-WF01-011 | Ordenação de Colunas | SortableHeader | Clicar no header ordena ascendente/descendente |
| CMP-WF01-012 | Indicador Hierarquia | Badge | Exibe nível (Global, Empresa, etc.) com cor diferenciada |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Nova Configuração" | Usuário clica em CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca textual | Usuário digita no campo CMP-WF01-002 | UC00 | FA-UC00-001 |
| EVT-WF01-003 | Filtro por categoria | Usuário seleciona categoria em CMP-WF01-003 | UC00 | FA-UC00-003 |
| EVT-WF01-004 | Filtro por nível | Usuário seleciona nível em CMP-WF01-004 | UC00 | FA-UC00-004 |
| EVT-WF01-005 | Filtro apenas sensíveis | Usuário marca CMP-WF01-005 | UC00 | FA-UC00-005 |
| EVT-WF01-006 | Ordenação de coluna | Usuário clica em header CMP-WF01-011 | UC00 | FA-UC00-002 |
| EVT-WF01-007 | Clique em Ver Detalhes | Usuário clica em CMP-WF01-007 | UC02 | FP-UC02-001 |
| EVT-WF01-008 | Clique em Editar | Usuário clica em CMP-WF01-008 | UC03 | FP-UC03-001 |
| EVT-WF01-009 | Clique em Excluir | Usuário clica em CMP-WF01-009 | UC04 | FP-UC04-001 |
| EVT-WF01-010 | Mudança de página | Usuário interage com CMP-WF01-010 | UC00 | FP-UC00-001 |

### 4.4 Ações Permitidas
- Buscar configurações por texto livre
- Filtrar por categoria, nível hierárquico, sensibilidade
- Ordenar por colunas (código, nome, categoria, tipo)
- Acessar detalhes de configuração
- Iniciar criação de nova configuração (se tiver permissão)
- Editar configuração (se tiver permissão)
- Excluir configuração (se tiver permissão)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando configurações no cache Redis ou banco de dados
**Exibir:**
- Skeleton loader na tabela (10 linhas fictícias)
- Mensagem: "Carregando configurações..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há configurações no tenant ou filtro retornou vazio
**Exibir:**
- Ícone ilustrativo (cog/settings)
- Mensagem: "Nenhuma configuração cadastrada"
- Botão "Nova Configuração" (se tiver permissão CREATE)
- Sugestão: "Configure o sistema criando sua primeira configuração"

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, timeout) ou cache Redis indisponível
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar configurações. Tente novamente."
- Botão "Recarregar"
- **Se cache Redis indisponível:** Aviso: "Cache indisponível, performance degradada" (FE-UC00-003)

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há configurações disponíveis
**Exibir:**
- Tabela hierarquizada com categorias agrupadas
- Colunas: Código, Nome, Categoria, Tipo Dado, Valor, Nível, Ações
- Valores sensíveis exibidos como `********` (exceto se usuário tiver permissão DECRYPT)
- Paginação (se > 50 registros)
- Filtros e busca ativos

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Lista em cards empilhados (campo Código + Valor + ações)
- **Tablet:** Tabela simplificada (5 colunas: Código, Nome, Categoria, Valor, Ações)
- **Desktop:** Tabela completa (todas as colunas)

#### Acessibilidade (WCAG AA)
- Labels em português claro: "Buscar configuração", "Filtrar por categoria"
- Botões com aria-label: "Editar configuração SMTP_Host"
- Navegação por teclado: Tab (foco), Enter (abrir), Esc (fechar modal)
- Contraste mínimo 4.5:1 (texto/fundo)

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso/erro após ações
- Highlight em linha após criação/edição
- Confirmação antes de exclusão

#### Regras de Negócio Visuais
- Apenas configurações do tenant atual (RN-UC00-001)
- Configurações soft-deleted (`Fl_Excluido = 1`) não aparecem (RN-UC00-002)
- Hierarquia multi-tenant: Usuário → Departamento → Empresa → Conglomerado → Global (RN-UC00-005)
- Valores sensíveis mascarados como `********` (RN-UC00-004)
- Paginação padrão 50 registros (RN-UC00-003)

---

## 5. WF-02 — CRIAR CONFIGURAÇÃO (UC01)

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de uma nova configuração com criptografia automática, validação de tipo e auditoria completa.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| **Aba Geral** | | | |
| CMP-WF02-001 | Campo Código | Input | Campo obrigatório (único por tenant, ex: `SMTP_Host`) |
| CMP-WF02-002 | Campo Nome | Input | Campo obrigatório (ex: "Host do servidor SMTP") |
| CMP-WF02-003 | Campo Descrição | Textarea | Campo opcional para descrição detalhada |
| CMP-WF02-004 | Dropdown Categoria | Dropdown | Obrigatório: Sistema, Email, Integração, Segurança, Notificação, Cache, Storage, Auditoria, Performance, Features |
| CMP-WF02-005 | Campo Grupo Visual | Input | Opcional (agrupamento visual na listagem) |
| **Aba Valor** | | | |
| CMP-WF02-006 | Dropdown Tipo Dado | Dropdown | Obrigatório: String, Integer, Decimal, Boolean, JSON, Enum, DateTime |
| CMP-WF02-007 | Campo Valor | Input/Textarea | Obrigatório, validado conforme tipo escolhido |
| CMP-WF02-008 | Campo Valor Padrão | Input | Opcional (fallback se valor vazio) |
| **Aba Validação** | | | |
| CMP-WF02-009 | Campo Validação Regex | Input | Opcional (regex customizada, ex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` para email) |
| CMP-WF02-010 | Campo Valores Permitidos | TagInput | Opcional (lista de valores aceitos, ex: "dev,hom,prd") |
| CMP-WF02-011 | Campo Valor Mínimo | Input | Opcional (para Integer/Decimal) |
| CMP-WF02-012 | Campo Valor Máximo | Input | Opcional (para Integer/Decimal) |
| **Aba Segurança** | | | |
| CMP-WF02-013 | Checkbox Criptografado | Checkbox | Se marcado, valor será criptografado com Azure Key Vault AES-256-GCM |
| CMP-WF02-014 | Checkbox Somente Leitura | Checkbox | Se marcado, configuração não pode ser editada posteriormente |
| CMP-WF02-015 | Checkbox Crítica | Checkbox | Se marcado, mudanças exigem dry-run e geram notificações Slack/Teams |
| **Aba Multi-Tenancy** | | | |
| CMP-WF02-016 | Dropdown Nível | Dropdown | Obrigatório: Global, Conglomerado, Empresa, Departamento, Usuário |
| CMP-WF02-017 | Dropdown Conglomerado | Dropdown | Se nível != Global (auto-preenchido do usuário) |
| CMP-WF02-018 | Dropdown Empresa | Dropdown | Se nível = Empresa/Departamento/Usuário |
| CMP-WF02-019 | Dropdown Departamento | Dropdown | Se nível = Departamento/Usuário |
| CMP-WF02-020 | Dropdown Usuário | Dropdown | Se nível = Usuário |
| **Aba Feature Flag** (opcional) | | | |
| CMP-WF02-021 | Checkbox Habilitar Feature Flag | Checkbox | Se marcado, exibe campos de rollout |
| CMP-WF02-022 | Dropdown Estratégia Rollout | Dropdown | Percentual, Usuário, Perfil, Empresa |
| CMP-WF02-023 | Campo Parâmetros Estratégia | Input/TagInput | Varia conforme estratégia (ex: "25%" ou lista de IDs) |
| CMP-WF02-024 | Campo Data Expiração | DatePicker | Opcional (data futura obrigatória se preenchido) |
| **Ações** | | | |
| CMP-WF02-025 | Botão Salvar | Button | Ação primária (verde/azul) |
| CMP-WF02-026 | Botão Salvar e Criar Outra | Button | Ação secundária (mantém formulário aberto) |
| CMP-WF02-027 | Botão Cancelar | Button | Ação terciária (retorna à listagem) |
| CMP-WF02-028 | Alerta de Validação | Alert | Exibe erros de validação em destaque |
| CMP-WF02-029 | Alerta Criptografia | Alert | Aviso quando checkbox "Criptografado" marcado |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Submissão de Formulário | Usuário clica em CMP-WF02-025 | UC01 | FP-UC01-001 |
| EVT-WF02-002 | Salvar e Criar Outra | Usuário clica em CMP-WF02-026 | UC01 | FA-UC01-001 |
| EVT-WF02-003 | Cancelamento | Usuário clica em CMP-WF02-027 | UC01 | FA-UC01-002 |
| EVT-WF02-004 | Marcar Criptografado | Usuário marca CMP-WF02-013 | UC01 | FA-UC01-003 |
| EVT-WF02-005 | Habilitar Feature Flag | Usuário marca CMP-WF02-021 | UC01 | FA-UC01-004 |
| EVT-WF02-006 | Validação de Campo | Sistema valida ao sair do campo | UC01 | FP-UC01-008 |
| EVT-WF02-007 | Erro de Validação | API retorna HTTP 400 | UC01 | FE-UC01-001, FE-UC01-002, FE-UC01-003 |
| EVT-WF02-008 | Erro Azure Key Vault | API retorna HTTP 503 | UC01 | FE-UC01-003 |

### 5.4 Comportamentos Obrigatórios

- Campos obrigatórios destacados com asterisco vermelho (*)
- Validação em tempo real ao sair do campo (onBlur)
- Feedback imediato de erro com mensagem específica
- Opção de cancelar com confirmação se houver dados preenchidos
- Preview de mascaramento ao marcar "Criptografado"
- Desabilitar campos dependentes conforme seleção de nível multi-tenancy

### 5.5 Estados Obrigatórios

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Usuário abre tela de criação
**Exibir:**
- Formulário vazio com valores padrão
- Campos obrigatórios destacados
- Foco no primeiro campo (Código)

#### Estado 2: Preenchimento (Dados Parciais)
**Quando:** Usuário está preenchendo formulário
**Exibir:**
- Validação em tempo real (onBlur)
- Contador de caracteres (se aplicável)
- Preview de valor formatado

#### Estado 3: Validação com Erro
**Quando:** Sistema detecta erro de validação
**Exibir:**
- Campos com erro destacados em vermelho
- Mensagens específicas abaixo do campo:
  - "Código duplicado: 'SMTP_Host' já existe para este tenant" (FE-UC01-001)
  - "Tipo inválido: Valor '999999' inválido para tipo Integer (max: 65535)" (FE-UC01-002)
  - "Validação regex falhou: E-mail inválido, formato esperado: exemplo@dominio.com" (FE-UC01-003)
- Scroll automático para primeiro erro
- Botão "Salvar" desabilitado até corrigir erros

#### Estado 4: Salvando (Loading)
**Quando:** Formulário submetido, aguardando resposta da API
**Exibir:**
- Spinner no botão "Salvar"
- Texto: "Salvando..." no botão
- Formulário bloqueado (disabled)

#### Estado 5: Sucesso
**Quando:** Configuração criada com sucesso (HTTP 201)
**Exibir:**
- Toast de sucesso: "Configuração criada com sucesso"
- Redirecionar para listagem após 2 segundos
- **Se "Salvar e Criar Outra":** Limpar formulário e manter na tela

#### Estado 6: Erro de Serviço
**Quando:** Azure Key Vault indisponível (HTTP 503) (FE-UC01-003)
**Exibir:**
- Alerta de erro: "Serviço de criptografia temporariamente indisponível. Tente novamente em alguns instantes."
- Botão "Tentar Novamente"

### 5.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única, abas colapsáveis
- **Tablet:** Formulário em 2 colunas onde aplicável
- **Desktop:** Formulário otimizado em 2-3 colunas

#### Acessibilidade (WCAG AA)
- Labels claras: "Código da Configuração", "Valor Padrão"
- Mensagens de erro associadas a campos (aria-describedby)
- Navegação por teclado: Tab, Shift+Tab, Enter (submit), Esc (cancelar)
- Indicadores visuais de campo obrigatório (asterisco + aria-required)

#### Feedback ao Usuário
- Validação em tempo real (onBlur) com mensagens específicas
- Toast de sucesso/erro após submissão
- Confirmação antes de cancelar se houver dados preenchidos
- Aviso ao marcar "Criptografado": "Valor será criptografado com Azure Key Vault. Não será possível visualizar em texto claro após salvar (exceto com permissão DECRYPT)" (FA-UC01-003)

#### Regras de Negócio Visuais
- Código único por tenant (validação backend, mensagem frontend) (RN-UC01-004)
- Criptografia automática se `Fl_Criptografado = 1` (RN-UC01-006)
- Validação de tipo antes de persistir (RN-UC01-005)
- Campos automáticos não exibidos: `Id_Conglomerado`, `Id_Empresa`, `Dt_Criacao`, `Id_Usuario_Criacao` (RN-UC01-002, RN-UC01-003)

---

## 6. WF-03 — VISUALIZAR CONFIGURAÇÃO (UC02)

### 6.1 Intenção da Tela
Permitir **consulta completa e segura** do registro com histórico de versões, auditoria e acesso controlado a valores sensíveis.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| **Aba Geral** (Leitura) | | | |
| CMP-WF03-001 | Exibição Código | ReadOnly | Código da configuração |
| CMP-WF03-002 | Exibição Nome | ReadOnly | Nome da configuração |
| CMP-WF03-003 | Exibição Descrição | ReadOnly | Descrição detalhada |
| CMP-WF03-004 | Exibição Categoria | Badge | Categoria com cor visual |
| CMP-WF03-005 | Exibição Grupo Visual | ReadOnly | Grupo de organização |
| **Aba Valor** (Leitura) | | | |
| CMP-WF03-006 | Exibição Tipo Dado | Badge | Tipo de dado (String, Integer, etc.) |
| CMP-WF03-007 | Exibição Valor | ReadOnly/Masked | Valor mascarado (`********`) se sensível |
| CMP-WF03-008 | Botão Revelar Valor | Button | Exibido apenas se usuário tiver permissão DECRYPT e configuração for sensível |
| CMP-WF03-009 | Exibição Valor Padrão | ReadOnly | Valor padrão |
| **Aba Validação** (Leitura) | | | |
| CMP-WF03-010 | Exibição Validação Regex | ReadOnly | Regex customizada (se definida) |
| CMP-WF03-011 | Exibição Valores Permitidos | TagList | Lista de valores aceitos |
| CMP-WF03-012 | Exibição Range | ReadOnly | Min/Max (se aplicável) |
| **Aba Segurança** (Leitura) | | | |
| CMP-WF03-013 | Badge Criptografado | Badge | "Criptografado" se `Fl_Criptografado = 1` |
| CMP-WF03-014 | Badge Somente Leitura | Badge | "Somente Leitura" se `Fl_SomenteLeitura = 1` |
| CMP-WF03-015 | Badge Crítica | Badge | "Crítica" se `Fl_Critica = 1` |
| **Aba Multi-Tenancy** (Leitura) | | | |
| CMP-WF03-016 | Exibição Nível | Badge | Nível hierárquico (Global, Empresa, etc.) |
| CMP-WF03-017 | Exibição Tenant Info | ReadOnly | Conglomerado, Empresa, Departamento, Usuário |
| **Aba Histórico** | | | |
| CMP-WF03-018 | Timeline de Versões | Timeline | Lista de versões com timestamp, usuário, ação |
| CMP-WF03-019 | Botão Comparar Versões | Button | Selecionar 2 versões e comparar |
| CMP-WF03-020 | Visualizador Diff | DiffViewer | Comparação lado a lado com highlight (verde/vermelho/amarelo) |
| CMP-WF03-021 | Botão Rollback | Button | Redireciona para WF-06 (UC05) |
| **Aba Auditoria** | | | |
| CMP-WF03-022 | Timeline de Auditoria | Timeline | Log de acessos e modificações: quem, quando, IP, user-agent, motivo, diff JSON |
| CMP-WF03-023 | Filtro de Ações | Dropdown | Filtrar por: CREATE, UPDATE, DELETE, ROLLBACK, DECRYPT |
| **Ações** | | | |
| CMP-WF03-024 | Botão Editar | Button | Redireciona para WF-04 (se tiver permissão UPDATE) |
| CMP-WF03-025 | Botão Excluir | Button | Redireciona para WF-05 (se tiver permissão DELETE) |
| CMP-WF03-026 | Botão Fechar | Button | Retorna à listagem |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Clique em Revelar Valor | Usuário clica em CMP-WF03-008 | UC09 | FP-UC09-001 (FA-UC02-001) |
| EVT-WF03-002 | Comparar Versões | Usuário seleciona 2 versões e clica em CMP-WF03-019 | UC02 | FA-UC02-002 |
| EVT-WF03-003 | Ver Auditoria | Usuário acessa aba Auditoria | UC02 | FA-UC02-003 |
| EVT-WF03-004 | Clique em Editar | Usuário clica em CMP-WF03-024 | UC03 | FP-UC03-001 |
| EVT-WF03-005 | Clique em Excluir | Usuário clica em CMP-WF03-025 | UC04 | FP-UC04-001 |
| EVT-WF03-006 | Clique em Rollback | Usuário clica em CMP-WF03-021 | UC05 | FP-UC05-001 |

### 6.4 Estados Obrigatórios

#### Estado 1: Loading (Carregando Dados)
**Quando:** Sistema está carregando configuração e histórico
**Exibir:**
- Skeleton loader em todas as abas
- Mensagem: "Carregando detalhes..."

#### Estado 2: Vazio (Configuração Não Encontrada)
**Quando:** ID inválido ou configuração excluída (FE-UC02-001)
**Exibir:**
- Mensagem: "Configuração não encontrada ou foi excluída"
- Botão "Voltar à Listagem"

#### Estado 3: Erro de Permissão
**Quando:** Configuração de outro tenant (FE-UC02-002)
**Exibir:**
- HTTP 403 Forbidden
- Mensagem: "Você não possui permissão para visualizar esta configuração"
- Botão "Voltar à Listagem"

#### Estado 4: Dados Carregados
**Quando:** Configuração carregada com sucesso
**Exibir:**
- Todas as abas populadas
- Valores sensíveis mascarados como `********` (FE-UC02-001)
- Botão "Revelar Valor" exibido se:
  - `Fl_Criptografado = 1` **E**
  - Usuário tiver permissão `SYS.CONFIGURACOES.DECRYPT`
- Histórico de versões exibido em timeline
- Auditoria completa na aba correspondente

### 6.5 Contratos de Comportamento

#### Responsividade
- **Mobile:** Abas colapsáveis, conteúdo empilhado
- **Tablet:** Abas em accordion, diff visual simplificado
- **Desktop:** Layout completo com todas as abas

#### Acessibilidade (WCAG AA)
- Labels claras para todos os campos de leitura
- Navegação por teclado entre abas (Arrow Left/Right)
- Screen reader anuncia "Valor mascarado por segurança"
- Contraste WCAG AA em diff visual

#### Feedback ao Usuário
- Tooltip em badges explicando significado
- Aviso ao tentar revelar valor sensível
- Confirmação antes de redirecionar para edição/exclusão

#### Regras de Negócio Visuais
- Isolamento por tenant obrigatório (RN-UC02-001)
- Auditoria de acesso a valores sensíveis (RN-UC02-002)
- Mascaramento automático (RN-UC02-003)
- Histórico com diff visual (RN-UC02-004)
- Descriptografia apenas com permissão DECRYPT (RN-UC02-005)

---

## 7. WF-04 — EDITAR CONFIGURAÇÃO (UC03)

### 7.1 Intenção da Tela
Permitir **alteração controlada** de dados existentes com validação, versionamento automático, dry-run opcional e notificações para configurações críticas.

### 7.2 Componentes de Interface

Similar ao WF-02 (Criar), com adições:

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Campo Motivo da Alteração | Textarea | **OBRIGATÓRIO** - Justificativa para auditoria SOX |
| CMP-WF04-002 | Botão Dry-Run | Button | Executar simulação de impacto antes de salvar (obrigatório se `Fl_Critica = 1`) |
| CMP-WF04-003 | Modal Relatório Dry-Run | Modal | Exibe impacto: usuários afetados, serviços impactados, riscos, recomendações |
| CMP-WF04-004 | Indicador de Versão Atual | Badge | Exibe versão atual (ex: "v1.2") |
| CMP-WF04-005 | Alerta Configuração Crítica | Alert | Aviso destacado se `Fl_Critica = 1` |
| CMP-WF04-006 | Alerta Somente Leitura | Alert | Bloqueio se `Fl_SomenteLeitura = 1` (FE-UC03-002) |
| CMP-WF04-007 | Diff Visual | DiffViewer | Exibe comparação valor anterior vs novo (em tempo real) |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Submissão com Dry-Run | Usuário clica em CMP-WF04-002 | UC03 | FA-UC03-004 |
| EVT-WF04-002 | Submissão Normal | Usuário clica em "Salvar" | UC03 | FP-UC03-001 |
| EVT-WF04-003 | Edição de Valor Sensível | Usuário altera campo com `Fl_Criptografado = 1` | UC03 | FA-UC03-002 |
| EVT-WF04-004 | Clique em Rollback | Usuário clica em "Rollback" na aba Histórico | UC03 | FA-UC03-003 |
| EVT-WF04-005 | Erro Somente Leitura | Sistema detecta `Fl_SomenteLeitura = 1` | UC03 | FE-UC03-002 |
| EVT-WF04-006 | Erro Conflito Concorrente | API retorna HTTP 409 | UC03 | FE-UC03-003 |

### 7.4 Estados Obrigatórios

#### Estado 1: Carregando Dados Atuais
**Quando:** Tela aberta para edição
**Exibir:**
- Skeleton loader no formulário
- Mensagem: "Carregando configuração..."

#### Estado 2: Bloqueio por Somente Leitura
**Quando:** `Fl_SomenteLeitura = 1` (FE-UC03-002)
**Exibir:**
- HTTP 403 Forbidden
- Mensagem: "Configuração protegida. Não pode ser editada. Contate Super Admin."
- Todos os campos desabilitados (readonly)
- Botão "Salvar" oculto

#### Estado 3: Formulário Pronto para Edição
**Quando:** Dados carregados, configuração editável
**Exibir:**
- Formulário pré-preenchido com valores atuais
- Campo "Motivo da Alteração" vazio (obrigatório)
- Diff visual em tempo real ao alterar valores
- **Se `Fl_Critica = 1`:** Alerta destacado + botão "Dry-Run" obrigatório

#### Estado 4: Dry-Run em Execução
**Quando:** Usuário clica em "Dry-Run" (FA-UC03-004)
**Exibir:**
- Modal com spinner: "Simulando impacto..."
- Relatório após conclusão:
  - "Usuários afetados: 1.234"
  - "Serviços que invalidarão cache: API Backend, Job Processamento"
  - "Riscos conhecidos: Mudança de porta SMTP pode quebrar envio de e-mails"
  - "Recomendações: Testar em HOM primeiro"
- Botões: "Confirmar e Salvar" ou "Cancelar"

#### Estado 5: Salvando Alterações
**Quando:** Formulário submetido
**Exibir:**
- Spinner no botão "Salvar"
- Texto: "Salvando alterações..."
- Formulário bloqueado

#### Estado 6: Sucesso
**Quando:** Alteração salva com sucesso
**Exibir:**
- Toast: "Configuração atualizada com sucesso. Nova versão: v1.3"
- **Se `Fl_Critica = 1`:** Notificação adicional: "Notificação enviada via Slack/Teams"
- Redirecionar para visualização após 2 segundos

#### Estado 7: Erro de Conflito Concorrente
**Quando:** Outro usuário editou simultaneamente (FE-UC03-003)
**Exibir:**
- HTTP 409 Conflict
- Mensagem: "Configuração foi alterada por outro usuário. Recarregue e tente novamente."
- Botões: "Recarregar Dados" ou "Voltar à Listagem"

### 7.5 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única, diff visual simplificado
- **Tablet:** Formulário em 2 colunas, diff visual compacto
- **Desktop:** Layout completo com diff lado a lado

#### Acessibilidade (WCAG AA)
- Campo "Motivo da Alteração" com label clara e aria-required
- Diff visual com contraste adequado (verde/vermelho/amarelo)
- Alerta de configuração crítica com aria-live="assertive"

#### Feedback ao Usuário
- Diff visual em tempo real ao alterar valores
- Toast de sucesso com versão criada
- Notificação de envio Slack/Teams (se crítica)
- Confirmação antes de dry-run
- Aviso ao editar valor sensível: "Novo valor será criptografado automaticamente ao salvar" (FA-UC03-002)

#### Regras de Negócio Visuais
- Motivo da alteração obrigatório (RN-UC03-002)
- Versionamento automático com incremento (RN-UC03-003)
- Notificação automática se crítica (RN-UC03-005)
- Dry-run obrigatório se crítica (RN-UC03-006)
- Configuração somente leitura bloqueada (RN-UC03-007)

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO (UC04)

### 8.1 Intenção da Tela
Evitar exclusões acidentais com confirmação explícita e informação de consequências.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Modal de Confirmação | Modal | Modal centralizado com fundo escurecido |
| CMP-WF05-002 | Título do Modal | Heading | "Confirmar Exclusão" |
| CMP-WF05-003 | Mensagem Principal | Text | "Confirma exclusão da configuração 'SMTP_Host'?" |
| CMP-WF05-004 | Alerta Reversível | Alert | "Esta ação pode ser revertida. A configuração será marcada como excluída (soft delete)." |
| CMP-WF05-005 | Alerta Somente Leitura | Alert | Se `Fl_SomenteLeitura = 1`: "Configuração protegida. Não pode ser excluída." (FE-UC04-002) |
| CMP-WF05-006 | Botão Confirmar | Button | Botão destrutivo (vermelho) "Confirmar Exclusão" |
| CMP-WF05-007 | Botão Cancelar | Button | Botão secundário "Cancelar" |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Confirmação de Exclusão | Usuário clica em CMP-WF05-006 | UC04 | FP-UC04-001 |
| EVT-WF05-002 | Cancelamento | Usuário clica em CMP-WF05-007 ou Esc | UC04 | FA-UC04-001 |

### 8.4 Estados Obrigatórios

#### Estado 1: Modal de Confirmação
**Quando:** Usuário clica em "Excluir" na listagem ou visualização
**Exibir:**
- Modal centralizado
- Fundo escurecido (overlay)
- Foco no botão "Cancelar" (padrão seguro)
- Mensagem clara com nome da configuração
- **Se `Fl_SomenteLeitura = 1`:** Alerta de bloqueio, botão "Confirmar" desabilitado (FE-UC04-002)

#### Estado 2: Executando Exclusão
**Quando:** Usuário confirma
**Exibir:**
- Spinner no botão "Confirmar Exclusão"
- Texto: "Excluindo..."
- Botões desabilitados

#### Estado 3: Sucesso
**Quando:** Exclusão realizada (HTTP 200)
**Exibir:**
- Toast: "Configuração excluída com sucesso"
- Modal fecha automaticamente
- Listagem atualizada (configuração removida)

#### Estado 4: Erro de Permissão
**Quando:** Configuração somente leitura (FE-UC04-002)
**Exibir:**
- HTTP 403 Forbidden
- Mensagem: "Configuração protegida. Não pode ser excluída."
- Botão "Confirmar" desabilitado

### 8.5 Contratos de Comportamento

#### Responsividade
- **Mobile:** Modal ocupa 90% da tela
- **Tablet:** Modal com largura fixa (500px)
- **Desktop:** Modal com largura fixa (600px)

#### Acessibilidade (WCAG AA)
- Foco capturado dentro do modal (trap focus)
- Esc fecha modal (cancelamento)
- Enter confirma exclusão (se foco no botão "Confirmar")
- Screen reader anuncia: "Modal de confirmação de exclusão"

#### Feedback ao Usuário
- Confirmação obrigatória (não há exclusão sem confirmação)
- Mensagem clara sobre reversibilidade (soft delete)
- Toast de sucesso após exclusão

#### Regras de Negócio Visuais
- Exclusão sempre lógica (soft delete) (RN-UC04-001)
- Configuração somente leitura bloqueada (RN-UC04-002)

---

## 9. WF-06 — HISTÓRICO E ROLLBACK (UC05)

### 9.1 Intenção da Tela
Restaurar configuração para versão anterior em 1-click com diff visual e auditoria completa.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Timeline de Versões | Timeline | Lista cronológica de versões (v1.0, v1.1, v1.2, etc.) |
| CMP-WF06-002 | Card de Versão | Card | Exibe: versão, timestamp, usuário, ação (CREATE, UPDATE, ROLLBACK), motivo |
| CMP-WF06-003 | Botão Rollback | Button | Exibido em cada versão (exceto a atual) |
| CMP-WF06-004 | Modal Confirmação Rollback | Modal | Confirmação com diff visual |
| CMP-WF06-005 | Diff Visual | DiffViewer | Comparação: versão atual → versão selecionada |
| CMP-WF06-006 | Campo Motivo Rollback | Textarea | **OBRIGATÓRIO** - Justificativa para auditoria |
| CMP-WF06-007 | Botão Confirmar Rollback | Button | Ação destrutiva (amarelo/laranja) |
| CMP-WF06-008 | Botão Cancelar | Button | Ação secundária |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Clique em Rollback | Usuário clica em CMP-WF06-003 | UC05 | FP-UC05-001 |
| EVT-WF06-002 | Visualizar Diff | Modal exibe diff antes de confirmar | UC05 | FA-UC05-001 |
| EVT-WF06-003 | Confirmar Rollback | Usuário clica em CMP-WF06-007 | UC05 | FP-UC05-001 |
| EVT-WF06-004 | Cancelar Rollback | Usuário clica em CMP-WF06-008 | UC05 | - |

### 9.4 Estados Obrigatórios

#### Estado 1: Timeline de Versões
**Quando:** Usuário acessa aba "Histórico" (WF-03)
**Exibir:**
- Timeline cronológica (mais recente no topo)
- Versão atual destacada (badge "Atual")
- Cada versão exibe:
  - Número da versão (v1.0, v1.1, etc.)
  - Timestamp formatado ("01/01/2025 14:35")
  - Usuário responsável ("João Silva")
  - Ação (CREATE, UPDATE, ROLLBACK)
  - Motivo (se disponível)
- Botão "Rollback" em versões anteriores

#### Estado 2: Modal de Confirmação de Rollback
**Quando:** Usuário clica em "Rollback para esta versão"
**Exibir:**
- Diff visual lado a lado:
  - **Esquerda:** Versão atual (v1.2 - valor: `465`)
  - **Direita:** Versão selecionada (v1.0 - valor: `587`)
- Campo "Motivo do Rollback" (obrigatório)
- Aviso: "Esta ação criará uma nova versão (v1.3) restaurando o valor da v1.0"
- Botões: "Confirmar Rollback" (amarelo) e "Cancelar" (cinza)

#### Estado 3: Executando Rollback
**Quando:** Usuário confirma
**Exibir:**
- Spinner no botão "Confirmar Rollback"
- Texto: "Executando rollback..."
- Formulário bloqueado

#### Estado 4: Sucesso
**Quando:** Rollback executado com sucesso
**Exibir:**
- Toast: "Rollback executado com sucesso. Versão atual: v1.3 (restaurada da v1.0)"
- **Notificação Slack/Teams enviada:** "🔄 Rollback executado: SMTP_Port | Autor: João Silva | Motivo: Rollback por falha após migração TLS | Versão restaurada: 1.0 (valor: 587)"
- Timeline atualizada com nova versão (v1.3)
- Modal fecha automaticamente

#### Estado 5: Erro
**Quando:** Versão origem não encontrada (FE-UC05-001)
**Exibir:**
- HTTP 404 Not Found
- Mensagem: "Versão selecionada não existe no histórico"
- Botão "Fechar"

### 9.5 Contratos de Comportamento

#### Responsividade
- **Mobile:** Timeline empilhada, diff visual em coluna única
- **Tablet:** Timeline compacta, diff visual lado a lado simplificado
- **Desktop:** Layout completo com diff visual otimizado

#### Acessibilidade (WCAG AA)
- Timeline com navegação por teclado (Arrow Up/Down)
- Diff visual com contraste WCAG AA (verde/vermelho/amarelo)
- Screen reader anuncia: "Versão 1.0, criada em 01/01/2025 por João Silva, motivo: Criação inicial"

#### Feedback ao Usuário
- Diff visual claro com cores padronizadas
- Confirmação obrigatória com preview
- Toast de sucesso com versão criada
- Notificação de envio Slack/Teams

#### Regras de Negócio Visuais
- Rollback cria nova versão (não altera histórico) (RN-UC05-001)
- Motivo obrigatório (RN-UC05-002)
- Notificação automática (RN-UC05-003)

---

## 10. WF-07 — GERENCIAR FEATURE FLAG (UC06)

### 10.1 Intenção da Tela
Habilitar/desabilitar feature flags com rollout progressivo e expiração automática.

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Checkbox Habilitar Feature Flag | Checkbox | Marca configuração como feature flag |
| CMP-WF07-002 | Dropdown Estratégia Rollout | Dropdown | Opções: Percentual, Usuário, Perfil, Empresa |
| CMP-WF07-003 | Campo Percentual | Slider | 0-100% (se estratégia Percentual) |
| CMP-WF07-004 | Campo IDs Usuários | TagInput | Lista de IDs (se estratégia Usuário) |
| CMP-WF07-005 | Dropdown Perfis | MultiSelect | Seleção de perfis (se estratégia Perfil) |
| CMP-WF07-006 | Campo IDs Empresas | TagInput | Lista de IDs (se estratégia Empresa) |
| CMP-WF07-007 | Campo Data Expiração | DatePicker | Data futura opcional |
| CMP-WF07-008 | Alerta Expiração Automática | Alert | Aviso sobre desabilitação automática |
| CMP-WF07-009 | Preview Rollout | Card | Preview visual de quantos usuários/empresas serão afetados |

### 10.3 Estados Obrigatórios

#### Estado 1: Feature Flag Desabilitada
**Quando:** Checkbox desmarcado
**Exibir:**
- Campos de rollout ocultos
- Mensagem: "Feature flag desabilitada. Marque o checkbox para configurar rollout."

#### Estado 2: Configuração de Rollout
**Quando:** Checkbox marcado
**Exibir:**
- Campos de estratégia visíveis
- Preview dinâmico de impacto
- Validação em tempo real

#### Estado 3: Sucesso
**Quando:** Feature flag salva
**Exibir:**
- Toast: "Feature flag configurada com sucesso. Estratégia: Percentual 25%"
- Preview de expiração (se data definida): "Expira em: 31/01/2025 (desabilitação automática)"

### 10.4 Contratos de Comportamento

#### Regras de Negócio Visuais
- 4 estratégias de rollout (RN-UC06-001)
- Expiração automática por job (RN-UC06-002)
- Notificação ao expirar (RN-UC06-003)

---

## 11. WF-08 — EXPORTAR CONFIGURAÇÕES (UC07)

### 11.1 Intenção da Tela
Exportar configurações em formato YAML para migração entre ambientes.

### 11.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF08-001 | Modal Exportação | Modal | Modal de seleção de filtros |
| CMP-WF08-002 | Dropdown Formato | Dropdown | JSON ou YAML |
| CMP-WF08-003 | Checkbox Todas | Checkbox | Exportar todas configurações |
| CMP-WF08-004 | Dropdown Categoria | Dropdown | Exportar apenas categoria específica |
| CMP-WF08-005 | Checkbox Apenas Críticas | Checkbox | Exportar apenas `Fl_Critica = 1` |
| CMP-WF08-006 | Botão Exportar | Button | Ação primária |
| CMP-WF08-007 | Alerta Mascaramento | Alert | "Valores sensíveis serão mascarados como ********" |

### 11.3 Estados Obrigatórios

#### Estado 1: Modal de Opções
**Quando:** Usuário clica em "Exportar Configurações"
**Exibir:**
- Filtros de escopo
- Aviso de mascaramento

#### Estado 2: Download em Andamento
**Quando:** Usuário confirma exportação
**Exibir:**
- Spinner no botão "Exportar"
- Texto: "Gerando arquivo..."

#### Estado 3: Sucesso
**Quando:** Arquivo gerado
**Exibir:**
- Download automático do arquivo `configuracoes-{tenant}-{data}.yaml`
- Toast: "Configurações exportadas com sucesso"
- Auditoria registrada

### 11.4 Contratos de Comportamento

#### Regras de Negócio Visuais
- Valores sensíveis sempre mascarados no export (RN-UC07-001)

---

## 12. WF-09 — IMPORTAR CONFIGURAÇÕES (UC08)

### 12.1 Intenção da Tela
Importar configurações de arquivo YAML com validação de schema e dry-run obrigatório.

### 12.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF09-001 | Upload de Arquivo | FileInput | Aceita .yaml e .json |
| CMP-WF09-002 | Preview do Arquivo | CodeViewer | Exibe conteúdo formatado |
| CMP-WF09-003 | Alerta Validação Schema | Alert | Erros de schema (se houver) |
| CMP-WF09-004 | Botão Dry-Run | Button | **OBRIGATÓRIO** - Simular importação |
| CMP-WF09-005 | Modal Relatório Dry-Run | Modal | Impacto detalhado |
| CMP-WF09-006 | Botão Confirmar Importação | Button | Ação primária (habilitado apenas após dry-run) |

### 12.3 Estados Obrigatórios

#### Estado 1: Upload de Arquivo
**Quando:** Modal aberto
**Exibir:**
- Área de drag-and-drop ou botão "Selecionar Arquivo"
- Mensagem: "Selecione um arquivo YAML ou JSON"

#### Estado 2: Validação de Schema
**Quando:** Arquivo selecionado
**Exibir:**
- Spinner: "Validando schema..."
- **Se erro:** Lista de erros (FE-UC08-001)
- **Se sucesso:** Preview do arquivo + botão "Dry-Run"

#### Estado 3: Dry-Run Obrigatório
**Quando:** Usuário clica em "Dry-Run"
**Exibir:**
- Modal com relatório:
  - "Configurações a criar: 5"
  - "Configurações a atualizar: 3"
  - "Conflitos detectados: 1 (código duplicado)" (FE-UC08-002)
- Botões: "Confirmar Importação" ou "Cancelar"

#### Estado 4: Importação em Andamento
**Quando:** Usuário confirma
**Exibir:**
- Spinner: "Importando configurações..."

#### Estado 5: Sucesso
**Quando:** Importação concluída
**Exibir:**
- Toast: "8 configurações importadas com sucesso"
- Auditoria registrada

### 12.4 Contratos de Comportamento

#### Regras de Negócio Visuais
- Validação schema obrigatória (RN-UC08-001)
- Dry-run obrigatório antes de aplicar (RN-UC08-002)

---

## 13. WF-10 — DESCRIPTOGRAFAR VALOR (UC09)

### 13.1 Intenção da Tela
Permitir que Super Admin visualize valor sensível descriptografado temporariamente.

### 13.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF10-001 | Modal Justificativa | Modal | Solicita motivo obrigatório |
| CMP-WF10-002 | Campo Motivo | Textarea | Justificativa para auditoria |
| CMP-WF10-003 | Botão Revelar | Button | Ação primária |
| CMP-WF10-004 | Modal Valor Descriptografado | Modal | Exibe valor em texto claro por 30 segundos |
| CMP-WF10-005 | Temporizador | Countdown | "Valor será ocultado em: 28s" |
| CMP-WF10-006 | Botão Copiar | Button | Copiar valor para clipboard |

### 13.3 Estados Obrigatórios

#### Estado 1: Solicitação de Motivo
**Quando:** Usuário clica em "Revelar Valor" (WF-03)
**Exibir:**
- Modal com campo "Motivo do Acesso" (obrigatório)
- Aviso: "Este acesso será auditado. Forneça uma justificativa válida."
- Botões: "Revelar" (desabilitado até preencher) e "Cancelar"

#### Estado 2: Descriptografando
**Quando:** Usuário confirma
**Exibir:**
- Spinner: "Descriptografando valor..."

#### Estado 3: Valor Exibido (30 segundos)
**Quando:** Valor descriptografado com sucesso
**Exibir:**
- Valor em texto claro
- Temporizador: "Valor será ocultado em: 28s"
- Botão "Copiar" (copia para clipboard)
- Aviso: "Este valor será re-mascarado automaticamente em 30 segundos"

#### Estado 4: Re-mascaramento Automático
**Quando:** 30 segundos decorridos
**Exibir:**
- Valor volta a `********`
- Toast: "Valor re-mascarado por segurança"

#### Estado 5: Erro de Permissão
**Quando:** Usuário sem permissão DECRYPT (FE-UC09-001)
**Exibir:**
- HTTP 403 Forbidden
- Mensagem: "Você não possui permissão para descriptografar valores sensíveis"

### 13.4 Contratos de Comportamento

#### Regras de Negócio Visuais
- Apenas Super Admin (RN-UC09-001)
- Auditoria obrigatória (RN-UC09-002)

---

## 14. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| **Mobile (< 768px)** | Layout em coluna única, tabelas em cards empilhados, modais fullscreen, abas colapsáveis |
| **Tablet (768px - 1024px)** | Layout em 2 colunas onde aplicável, tabelas simplificadas, modais com largura fixa |
| **Desktop (> 1024px)** | Layout completo, tabelas com todas colunas, modais otimizados |

---

## 15. ACESSIBILIDADE (OBRIGATÓRIO)

- Navegação por teclado: Tab, Shift+Tab, Enter, Esc, Arrow Keys
- Leitura por screen readers: aria-label, aria-describedby, role
- Contraste mínimo WCAG AA: 4.5:1 (texto normal), 3:1 (texto grande)
- Labels e descrições claras em português
- Foco visível em todos os elementos interativos
- Estados de loading anunciados por screen reader

---

## 16. NOTIFICAÇÕES

### 16.1 Tipos Padronizados

| Tipo | Cor | Uso |
|----|----|-----|
| **Sucesso** | Verde | Operação concluída com sucesso |
| **Erro** | Vermelho | Falha bloqueante |
| **Aviso** | Amarelo/Laranja | Atenção necessária |
| **Info** | Azul | Feedback neutro |

### 16.2 Exemplos de Mensagens

**Sucesso:**
- "Configuração criada com sucesso"
- "Configuração atualizada com sucesso. Nova versão: v1.3"
- "Rollback executado com sucesso. Versão atual: v1.3 (restaurada da v1.0)"

**Erro:**
- "Código duplicado: 'SMTP_Host' já existe para este tenant"
- "Serviço de criptografia temporariamente indisponível. Tente novamente em alguns instantes."
- "Configuração protegida. Não pode ser editada."

**Aviso:**
- "Valor será criptografado com Azure Key Vault. Não será possível visualizar em texto claro após salvar (exceto com permissão DECRYPT)"
- "Configuração crítica. Executar dry-run antes de salvar?"

**Info:**
- "Cache indisponível, performance degradada"
- "Este valor será re-mascarado automaticamente em 30 segundos"

---

## 17. RASTREABILIDADE

| Wireframe | UC(s) | Cobertura RF002 |
|---------|-------|-----------------|
| WF-01 | UC00 | Listagem hierarquizada, mascaramento, filtros |
| WF-02 | UC01 | Criação com validação, criptografia, auditoria |
| WF-03 | UC02 | Visualização detalhada, histórico, auditoria |
| WF-04 | UC03 | Edição controlada, versionamento, dry-run, notificações |
| WF-05 | UC04 | Soft delete com confirmação |
| WF-06 | UC05 | Rollback 1-click com diff visual |
| WF-07 | UC06 | Feature flags com rollout progressivo |
| WF-08 | UC07 | Export YAML com mascaramento |
| WF-09 | UC08 | Import YAML com dry-run |
| WF-10 | UC09 | Descriptografia temporária auditada |

**Cobertura Total:** 100% dos UCs do RF002 (UC00 a UC09) estão cobertos por wireframes.

---

## 18. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, fontes, espaçamentos específicos)
- Escolha de framework (Filament, React, Vue, Angular)
- Design gráfico definitivo (logos, ilustrações customizadas)
- Animações avançadas (transições CSS complexas)
- Implementação técnica (código fonte)

---

## 19. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 1.0 | 2026-01-04 | Agência ALC - alc.dev.br | Wireframes canônicos do RF002 cobrindo 100% dos UCs (UC00-UC09). Inclui: listagem hierarquizada, CRUD completo, versionamento, rollback, feature flags, export/import, descriptografia. Total: 10 wireframes detalhados. |

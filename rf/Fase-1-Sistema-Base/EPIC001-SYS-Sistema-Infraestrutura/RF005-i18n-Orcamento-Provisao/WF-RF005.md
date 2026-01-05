# WF-RF005 — Wireframes Canônicos (UI Contract)

**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF005 - Internacionalização (i18n) e Localização
**UC Relacionado:** UC-RF005 (UC00 a UC10 - 11 casos de uso)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF005 - Sistema de Internacionalização e Localização.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional** em todas as telas de i18n
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
- Bandeiras e ícones visuais para facilitar identificação de idiomas

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis e destacadas |
| Ações destrutivas | Sempre confirmadas com contexto claro |
| Estados vazios | Devem orientar o usuário com CTA (Call-to-Action) |
| Erros | Devem ser claros, acionáveis e contextualizados |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Feedback visual | Loading spinners, toasts de sucesso/erro |
| Bandeiras de idiomas | Sempre exibidas (emoji ou flag-icons) |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF - 11 UCs)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Idiomas | UC00 | Visualizar todos os idiomas com progresso |
| WF-02 | Adicionar Novo Idioma | UC01 | Criar idioma no sistema |
| WF-03 | Baixar Template de Tradução | UC02 | Download de templates (JSON/PO/XLSX) |
| WF-04 | Upload de Traduções | UC03 | Import de arquivos traduzidos |
| WF-05 | Ativar/Desativar Idioma | UC04 | Alterar status do idioma |
| WF-06 | Histórico de Versões | UC05 | Visualizar uploads anteriores |
| WF-07 | Restaurar Versão (Rollback) | UC06 | Desfazer upload recente |
| WF-08 | Validação de Integridade | UC07 | Relatório de validação automática |
| WF-09 | Tradução Automática (Azure) | UC08 | Traduzir via Azure Translator |
| WF-10 | Exportar Traduções | UC09 | Export de traduções atuais |
| WF-11 | Seletor de Idioma (Usuário) | UC10 | Usuário final seleciona idioma |

---

## 4. WF-01 — LISTAGEM DE IDIOMAS (UC00)

### 4.1 Intenção da Tela

Permitir ao usuário **visualizar todos os idiomas cadastrados** no sistema, com status, progresso de tradução e ações disponíveis conforme permissões.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Novo Idioma" | Button (Primary) | Ação primária para criar novo idioma |
| CMP-WF01-002 | Campo de Busca | Input (Search) | Busca textual por nome ou código de idioma |
| CMP-WF01-003 | Filtro de Status | Dropdown | Filtrar por: Ativo / Inativo / Todos |
| CMP-WF01-004 | Tabela de Idiomas | DataTable | Exibição dos idiomas com colunas específicas |
| CMP-WF01-005 | Coluna Bandeira | TableColumn (Icon) | Exibe bandeira do idioma (emoji 🇧🇷 ou flag-icon) |
| CMP-WF01-006 | Coluna Nome | TableColumn (Text) | Nome do idioma (ex: Português (Brasil)) |
| CMP-WF01-007 | Coluna Código | TableColumn (Text) | Código ISO (ex: pt-BR) |
| CMP-WF01-008 | Coluna Status | TableColumn (Badge) | Ativo (verde) / Inativo (cinza) |
| CMP-WF01-009 | Coluna Progresso | TableColumn (ProgressBar) | Barra de progresso (ex: 85%) |
| CMP-WF01-010 | Ações por Linha | TableColumn (Actions) | Botões: Baixar Template, Upload, Ativar/Desativar, Histórico, Exportar |
| CMP-WF01-011 | Paginação | Pagination | Controles de navegação entre páginas (10 itens/página) |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Novo Idioma" | Usuário clica no botão CMP-WF01-001 | UC01 | Abre WF-02 (Modal Adicionar Idioma) |
| EVT-WF01-002 | Busca textual | Usuário digita no campo CMP-WF01-002 | UC00-FA-001 | Filtra lista em tempo real |
| EVT-WF01-003 | Filtro por status | Usuário seleciona no dropdown CMP-WF01-003 | UC00-FA-002 | Aplica filtro client-side |
| EVT-WF01-004 | Ordenar por Progresso | Usuário clica em cabeçalho CMP-WF01-009 | UC00-FA-003 | Ordena crescente/decrescente |
| EVT-WF01-005 | Baixar Template | Usuário clica em ícone 📥 nas ações | UC02 | Abre WF-03 (Modal Baixar Template) |
| EVT-WF01-006 | Upload | Usuário clica em ícone 📤 nas ações | UC03 | Abre WF-04 (Modal Upload) |
| EVT-WF01-007 | Ativar/Desativar | Usuário clica em toggle nas ações | UC04 | Abre WF-05 (Modal Confirmação) |
| EVT-WF01-008 | Histórico | Usuário clica em ícone 📜 nas ações | UC05 | Abre WF-06 (Modal Histórico) |
| EVT-WF01-009 | Exportar | Usuário clica em ícone 📤 nas ações | UC09 | Abre WF-10 (Modal Exportar) |

### 4.4 Ações Permitidas

- **Visualizar** lista de idiomas com progresso
- **Buscar** idiomas por nome ou código
- **Filtrar** por status (Ativo/Inativo)
- **Ordenar** por progresso de tradução
- **Criar** novo idioma (se tiver permissão SYS.I18N.MANAGE_LANGUAGES)
- **Baixar template** para tradução offline
- **Upload** de traduções
- **Ativar/Desativar** idiomas
- **Visualizar histórico** de versões
- **Exportar** traduções atuais

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando idiomas no backend

**Exibir:**
- Skeleton loader (tabela com 5 linhas simuladas)
- Mensagem: "Carregando idiomas..."
- Botões desabilitados
- Duração estimada: < 500ms

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há idiomas cadastrados (improvável, pt-BR é obrigatório)

**Exibir:**
- Ícone ilustrativo de idiomas/globo
- Mensagem: "Nenhum idioma cadastrado. Crie o primeiro idioma."
- Botão destacado [+ Novo Idioma] (se tiver permissão)
- Nota: "O idioma padrão (pt-BR) será criado automaticamente no primeiro acesso"

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 503, timeout)

**Exibir:**
- Ícone de erro (❌)
- Mensagem: "Erro ao carregar idiomas. Tente novamente."
- Botão [Recarregar Página]
- Detalhes técnicos (se modo debug ativo)

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há idiomas disponíveis (cenário padrão)

**Exibir:**
- Tabela completa com todas as colunas
- pt-BR destacado com ícone de cadeado 🔒 (não pode ser desativado)
- Badge "PADRÃO" no pt-BR
- Ações por linha conforme permissões
- Paginação (se > 10 idiomas)
- Total de idiomas exibido: "5 idiomas cadastrados (4 ativos, 1 inativo)"

### 4.6 Contratos de Comportamento

#### Responsividade

- **Mobile (< 768px):**
  - Tabela convertida em cards empilhados
  - Card exibe: Bandeira, Nome, Código, Progresso (barra), Botão "Ações" (expansível)
  - Busca e filtros mantidos

- **Tablet (768px - 1024px):**
  - Tabela simplificada (5 colunas visíveis)
  - Ocultar coluna Código (manter Bandeira, Nome, Status, Progresso, Ações)

- **Desktop (> 1024px):**
  - Tabela completa (todas as colunas)
  - Layout horizontal tradicional

#### Acessibilidade (WCAG AA)

- Labels em português claro (sem siglas técnicas)
- Botões com aria-label: "Adicionar novo idioma", "Baixar template de fr-FR"
- Navegação por teclado (Tab, Enter, Esc)
- Contraste mínimo 4.5:1 (texto sobre fundo)
- Screen reader: anuncia "Tabela de idiomas cadastrados, 5 linhas"

#### Feedback ao Usuário

- Loading spinner durante requisições
- Toast de sucesso após ações: "Idioma criado com sucesso!"
- Toast de erro com mensagem clara: "Erro ao carregar idiomas"
- Confirmação antes de ações destrutivas (desativar idioma)
- Atualização da lista sem reload completo da página

#### Regras Visuais Específicas

- **pt-BR obrigatório:** Sempre exibido com cadeado 🔒, badge "PADRÃO", botão "Desativar" desabilitado
- **Progresso < 80%:** Barra de progresso em amarelo com ícone ⚠️
- **Progresso >= 80%:** Barra de progresso em verde
- **Progresso = 100%:** Barra verde com ícone ✅
- **Idioma inativo:** Linha inteira com opacidade 60%, badge cinza

#### Multi-Tenancy

- Apenas idiomas do tenant atual são exibidos
- ClienteId validado no backend
- Nenhum idioma de outro tenant é visível

---

## 5. WF-02 — ADICIONAR NOVO IDIOMA (UC01)

### 5.1 Intenção da Tela

Permitir **criação segura e validada** de um novo idioma no sistema, com auto-sugestão de bandeiras e validação de código ISO.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Título do Modal | Text | "Adicionar Novo Idioma" |
| CMP-WF02-002 | Dropdown Idioma | Select (Searchable) | Lista de idiomas ISO 639-1 (200+ idiomas) |
| CMP-WF02-003 | Campo Código | Input (Text, Readonly) | Auto-preenchido (ex: fr-FR) |
| CMP-WF02-004 | Campo Nome | Input (Text, Readonly) | Auto-preenchido (ex: Français) |
| CMP-WF02-005 | Seletor de Bandeira | IconPicker | Emoji ou flag-icon (ex: 🇫🇷) |
| CMP-WF02-006 | Preview Bandeira | Image | Pré-visualização da bandeira selecionada |
| CMP-WF02-007 | Dropdown Idioma Referência | Select | Idioma para template (padrão: pt-BR) |
| CMP-WF02-008 | Botão Criar | Button (Primary) | Ação primária para salvar idioma |
| CMP-WF02-009 | Botão Cancelar | Button (Secondary) | Ação secundária para cancelar criação |
| CMP-WF02-010 | Mensagem de Erro | Alert (Danger) | Exibe erros de validação |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Seleção de Idioma | Usuário seleciona idioma no dropdown CMP-WF02-002 | UC01-FP-004 | Auto-preenche Código, Nome, Bandeira |
| EVT-WF02-002 | Alteração de Bandeira | Usuário clica em CMP-WF02-005 | UC01-FA-002 | Abre seletor de bandeiras |
| EVT-WF02-003 | Submissão de Formulário | Usuário clica em CMP-WF02-008 | UC01-FP-008 | Valida e cria idioma |
| EVT-WF02-004 | Cancelamento | Usuário clica em CMP-WF02-009 | UC01-FA-003 | Exibe confirmação se houver dados |
| EVT-WF02-005 | Validação de Código | Sistema valida formato ISO | UC01-FP-010 | Bloqueia se inválido |

### 5.4 Comportamentos Obrigatórios

- **Campos obrigatórios destacados** com asterisco vermelho (*)
- **Validação antes do envio** (formato ISO, unicidade)
- **Feedback imediato** após seleção de idioma
- **Opção de cancelar** com confirmação se houver dados preenchidos
- **Auto-preenchimento inteligente** de Código, Nome e Bandeira

### 5.5 Estados Obrigatórios

#### Estado 1: Inicial (Formulário Limpo)
**Quando:** Modal aberto pela primeira vez

**Exibir:**
- Dropdown idioma vazio com placeholder: "Selecione um idioma"
- Campos Código e Nome desabilitados (vazios)
- Bandeira padrão: 🌐 (globo)
- Idioma referência pré-selecionado: pt-BR
- Botão "Criar" desabilitado até seleção válida

#### Estado 2: Preenchendo (Idioma Selecionado)
**Quando:** Usuário seleciona idioma no dropdown

**Exibir:**
- Dropdown preenchido (ex: Français - France)
- Código auto-preenchido: fr-FR (readonly)
- Nome auto-preenchido: Français (readonly)
- Bandeira auto-sugerida: 🇫🇷 (editável)
- Botão "Criar" habilitado
- Mensagem informativa: "Você pode alterar a bandeira se necessário"

#### Estado 3: Erro de Validação (Código Duplicado)
**Quando:** Código ISO já existe no sistema

**Exibir:**
- Alert vermelho: "Idioma fr-FR já cadastrado no sistema"
- Campo Código destacado em vermelho
- Botão "Criar" desabilitado
- Link: "Voltar para lista de idiomas"

#### Estado 4: Sucesso (Idioma Criado)
**Quando:** API retorna 201 Created

**Exibir:**
- Toast de sucesso: "Idioma criado! Próximo passo: baixe o template de tradução"
- Modal fecha automaticamente (1s)
- Lista de idiomas (WF-01) atualizada
- Novo idioma destacado temporariamente (highlight verde)

#### Estado 5: Erro de Criação (Falha no Servidor)
**Quando:** API retorna erro 500

**Exibir:**
- Alert vermelho: "Erro ao criar idioma. Tente novamente."
- Botão "Tentar Novamente" ao lado de "Cancelar"
- Logs técnicos visíveis (se modo debug)

### 5.6 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal ocupa 95% da tela, campos empilhados verticalmente
- **Tablet:** Modal com largura fixa 600px, centralizado
- **Desktop:** Modal com largura fixa 700px, centralizado

#### Acessibilidade (WCAG AA)

- Foco automático no dropdown ao abrir modal
- Esc fecha modal (com confirmação se houver dados)
- Enter submete formulário (se válido)
- Labels descritivas: "Selecione o idioma que deseja adicionar"

#### Validações Client-Side

- Código ISO: Regex `^[a-z]{2}-[A-Z]{2}$`
- Idioma obrigatório (não pode estar vazio)
- Bandeira obrigatória

#### Feedback Visual

- Loading spinner no botão "Criar" durante requisição
- Campos desabilitados durante requisição
- Bandeira pré-visualizada em tempo real

---

## 6. WF-03 — BAIXAR TEMPLATE DE TRADUÇÃO (UC02)

### 6.1 Intenção da Tela

Permitir **download de templates de tradução** em 3 formatos (JSON, PO, XLSX), com opções de personalização (vazio vs atual, incluir comentários, exemplos).

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Título do Modal | Text | "Baixar Template de Tradução - 🇫🇷 Français" |
| CMP-WF03-002 | Seletor de Tipo | RadioGroup | Template Vazio / Tradução Atual |
| CMP-WF03-003 | Seletor de Formato | RadioGroup | JSON / PO (Gettext) / XLSX (Excel) |
| CMP-WF03-004 | Checkbox Comentários | Checkbox | ☑ Incluir comentários/contexto |
| CMP-WF03-005 | Checkbox Exemplos | Checkbox | ☑ Incluir exemplos de uso |
| CMP-WF03-006 | Checkbox Referências | Checkbox | ☑ Incluir traduções de referência (pt-BR) |
| CMP-WF03-007 | Estatísticas | InfoBox | Total chaves: 1.247 / Namespaces: 47 / Tamanho estimado: ~250 KB |
| CMP-WF03-008 | Botão Baixar | Button (Primary) | Ação primária para download |
| CMP-WF03-009 | Botão Cancelar | Button (Secondary) | Ação secundária para cancelar |
| CMP-WF03-010 | Mensagem Informativa | Alert (Info) | Dicas sobre cada formato |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Seleção de Tipo | Usuário seleciona radio CMP-WF03-002 | UC02-FP-005 | Atualiza descrição e estatísticas |
| EVT-WF03-002 | Seleção de Formato | Usuário seleciona radio CMP-WF03-003 | UC02-FP-006 | Exibe dica específica do formato |
| EVT-WF03-003 | Download | Usuário clica em CMP-WF03-008 | UC02-FP-009 | Gera e baixa arquivo |
| EVT-WF03-004 | Cancelamento | Usuário clica em CMP-WF03-009 | UC02-FA-003 | Fecha modal sem baixar |

### 6.4 Estados Obrigatórios

#### Estado 1: Inicial (Selecionando Opções)
**Quando:** Modal aberto

**Exibir:**
- Idioma selecionado destacado com bandeira
- Tipo pré-selecionado: "Template Vazio"
- Formato pré-selecionado: "JSON"
- Checkboxes marcadas por padrão: Comentários, Exemplos, Referências
- Estatísticas atualizadas dinamicamente
- Botão "Baixar" habilitado

#### Estado 2: Gerando Arquivo (Loading)
**Quando:** Usuário clicou em "Baixar" e sistema está gerando arquivo

**Exibir:**
- Botão "Baixar" com loading spinner
- Mensagem: "Gerando arquivo... Aguarde."
- Todos os controles desabilitados
- Duração estimada: 2-5 segundos

#### Estado 3: Sucesso (Download Iniciado)
**Quando:** Arquivo gerado e download iniciado

**Exibir:**
- Toast de sucesso: "Download iniciado! Arquivo: fr-FR-template.json"
- Modal fecha automaticamente (1s)
- Navegador exibe progresso de download

#### Estado 4: Erro (Falha ao Gerar)
**Quando:** Erro ao gerar arquivo (timeout, memória)

**Exibir:**
- Alert vermelho: "Erro ao gerar template. Tente outro formato ou tente novamente."
- Botão "Tentar Novamente"
- Sugestão: "Se o erro persistir, exporte por namespace específico"

### 6.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen, opções empilhadas verticalmente
- **Tablet:** Modal 80% largura, centralizado
- **Desktop:** Modal 900px largura, centralizado

#### Acessibilidade (WCAG AA)

- RadioGroups navegáveis por setas
- Checkboxes com labels clicáveis
- Dica contextual ao focar em cada formato

#### Feedback Visual

- Tamanho estimado do arquivo atualizado em tempo real
- Dica específica por formato:
  - **JSON:** "Ideal para desenvolvedores e integração com ferramentas de i18n"
  - **PO:** "Ideal para ferramentas CAT (Computer-Assisted Translation) como POEdit"
  - **XLSX:** "Ideal para tradutores sem conhecimento técnico (Excel)"

#### Validações

- Formato obrigatório (um deve estar selecionado)
- Tipo obrigatório (vazio ou atual)

---

## 7. WF-04 — UPLOAD DE TRADUÇÕES (UC03)

### 7.1 Intenção da Tela

Permitir **upload seguro e validado** de arquivos de tradução (JSON, PO, XLSX), com validação automática de estrutura, interpolações e integridade antes de importar.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Título do Modal | Text | "Enviar Arquivo de Tradução - 🇫🇷 Français" |
| CMP-WF04-002 | Área Drag & Drop | FileUpload | Zona de arrastar/soltar arquivo |
| CMP-WF04-003 | Botão Selecionar Arquivo | Button (Secondary) | Alternativa ao drag & drop |
| CMP-WF04-004 | Pré-visualização Arquivo | InfoBox | Nome, tamanho, formato, validação |
| CMP-WF04-005 | Checkbox Sobrescrever | Checkbox | ☑ Sobrescrever traduções existentes |
| CMP-WF04-006 | Checkbox Validar Interpolações | Checkbox | ☑ Validar interpolações {{var}} |
| CMP-WF04-007 | Checkbox Gerar Relatório | Checkbox | ☑ Gerar relatório detalhado |
| CMP-WF04-008 | Checkbox Ativar se 100% | Checkbox | ☑ Ativar idioma automaticamente se 100% |
| CMP-WF04-009 | Botão Enviar | Button (Primary) | Ação primária para upload |
| CMP-WF04-010 | Botão Cancelar | Button (Secondary) | Ação secundária para cancelar |
| CMP-WF04-011 | Lista de Erros | Alert (Danger) | Erros críticos detectados |
| CMP-WF04-012 | Lista de Avisos | Alert (Warning) | Avisos não-bloqueantes |
| CMP-WF04-013 | Relatório de Resultado | Modal (Success) | Estatísticas pós-upload |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Drag & Drop | Usuário arrasta arquivo para CMP-WF04-002 | UC03-FP-006 | Valida formato e tamanho |
| EVT-WF04-002 | Seleção Manual | Usuário clica em CMP-WF04-003 | UC03-FP-006 | Abre seletor de arquivos do SO |
| EVT-WF04-003 | Validação de Arquivo | Arquivo selecionado | UC03-FP-007 a UC03-FP-009 | Valida formato, encoding, tamanho |
| EVT-WF04-004 | Upload | Usuário clica em CMP-WF04-009 | UC03-FP-012 | Envia arquivo e processa |
| EVT-WF04-005 | Cancelamento | Usuário clica em CMP-WF04-010 | UC03-FA-003 | Fecha modal sem importar |

### 7.4 Estados Obrigatórios

#### Estado 1: Aguardando Arquivo
**Quando:** Modal aberto, nenhum arquivo selecionado

**Exibir:**
- Área drag & drop destacada com borda tracejada
- Ícone de upload grande (📤)
- Mensagem: "Arraste o arquivo de tradução aqui ou clique para selecionar"
- Formatos aceitos: ".json, .po, .xlsx (máximo 5 MB)"
- Botão "Enviar" desabilitado

#### Estado 2: Arquivo Selecionado (Validação OK)
**Quando:** Usuário selecionou arquivo válido

**Exibir:**
- Nome do arquivo: "fr-FR-traducoes.json" com ícone ✅
- Tamanho: "245 KB" (válido)
- Formato: "JSON" (válido) com ícone ✅
- Encoding: "UTF-8" (válido) com ícone ✅
- Checkboxes habilitadas (padrão: todas marcadas)
- Botão "Enviar" habilitado

#### Estado 3: Arquivo Inválido
**Quando:** Arquivo com formato incorreto, tamanho > 5MB ou encoding != UTF-8

**Exibir:**
- Nome do arquivo com ícone ❌
- Erro específico:
  - "Formato inválido. Formatos aceitos: .json, .po, .xlsx"
  - "Arquivo muito grande (7.2 MB). Máximo: 5 MB"
  - "Encoding inválido (ISO-8859-1). Obrigatório: UTF-8"
- Botão "Selecionar Outro Arquivo"
- Botão "Enviar" desabilitado

#### Estado 4: Processando Upload
**Quando:** Arquivo enviado, backend validando

**Exibir:**
- Barra de progresso (0% → 100%)
- Mensagem: "Enviando e validando arquivo... 45%"
- Etapas visíveis:
  - ✅ Upload concluído
  - ⏳ Validando estrutura...
  - ⏳ Validando interpolações...
  - ⏳ Validando HTML...
  - ⏳ Importando traduções...
- Todos os controles desabilitados
- Duração estimada: 5-15 segundos

#### Estado 5: Erros Críticos Detectados
**Quando:** Backend detectou erros bloqueantes

**Exibir:**
- Alert vermelho: "Upload rejeitado. 12 erros críticos detectados:"
- Lista de erros numerada:
  1. Chave `common.buttons.save` não existe no sistema
  2. Interpolação `{{username}}` presente em pt-BR mas ausente em `messages.welcome`
  3. HTML não balanceado em `notifications.alert`: `<b>Atenção` (sem fechamento)
  4. (continua...)
- Botão "Corrigir Arquivo e Reenviar"
- Botão "Cancelar"
- Download do relatório de erros em CSV

#### Estado 6: Avisos Não-Bloqueantes (Sucesso com Avisos)
**Quando:** Upload bem-sucedido, mas há avisos

**Exibir:**
- Alert amarelo: "Upload concluído com 8 avisos:"
  1. Tradução de `common.messages.longText` é muito longa (542 caracteres)
  2. Tradução de `menu.dashboard` é idêntica ao pt-BR (possível erro de tradução)
  3. (continua...)
- Botão "Revisar Avisos Posteriormente"
- Botão "Fechar"

#### Estado 7: Sucesso (Upload Completo)
**Quando:** Upload e importação bem-sucedidos

**Exibir:**
- Modal de resultado com estatísticas:
  - ✅ Upload concluído com sucesso!
  - Chaves adicionadas: 150
  - Chaves atualizadas: 497
  - Progresso anterior: 60% → Progresso novo: 95%
  - Tempo de processamento: 8 segundos
  - Versão criada: v2.3 (2026-01-04 15:42)
- Botão "Visualizar Histórico de Versões"
- Botão "Fechar"
- Lista de idiomas (WF-01) atualizada automaticamente

### 7.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen, área drag & drop 100% largura
- **Tablet:** Modal 90% largura, drag & drop responsivo
- **Desktop:** Modal 1000px largura, drag & drop destacada

#### Acessibilidade (WCAG AA)

- Área drag & drop acessível por teclado (Enter para selecionar)
- Leitores de tela anunciam: "Área de upload de arquivo. Pressione Enter para selecionar"
- Erros lidos em voz alta

#### Validações Client-Side

- Extensão do arquivo: `.json`, `.po`, `.xlsx`
- Tamanho máximo: 5 MB
- MIME type validado: `application/json`, `text/plain`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

#### Validações Server-Side (Backend)

- Encoding UTF-8 obrigatório
- Estrutura de chaves válida (namespaces corretos)
- Interpolações consistentes: `{{var}}` em pt-BR deve ter `{{var}}` na tradução
- HTML balanceado: `<b>Texto</b>` válido, `<b>Texto` inválido
- Chaves obrigatórias presentes

#### Feedback Visual

- Barra de progresso animada durante upload
- Etapas de validação exibidas em tempo real
- Ícones de status (✅, ⏳, ❌) ao lado de cada etapa

#### Backup Automático

- Sistema cria backup da versão atual ANTES de sobrescrever
- Backup registrado em SistemaTraducaoVersoes
- Rollback possível via WF-07

---

## 8. WF-05 — ATIVAR/DESATIVAR IDIOMA (UC04)

### 8.1 Intenção da Tela

Permitir **alteração segura de status** de um idioma (Ativo ↔ Inativo), com proteção do idioma padrão (pt-BR) e aviso de progresso < 80%.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Título do Modal | Text | "Ativar Idioma" ou "Desativar Idioma" |
| CMP-WF05-002 | Idioma Selecionado | InfoBox | Bandeira, Nome, Código, Progresso |
| CMP-WF05-003 | Aviso de Progresso | Alert (Warning) | Exibido se progresso < 80% (apenas ativação) |
| CMP-WF05-004 | Aviso de Desativação | Alert (Warning) | Exibido ao desativar (impacto em usuários) |
| CMP-WF05-005 | Botão Confirmar | Button (Primary ou Danger) | Confirma ativação/desativação |
| CMP-WF05-006 | Botão Cancelar | Button (Secondary) | Cancela operação |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Ativar Idioma | Usuário confirma ativação | UC04-FP-008 | Ativa idioma no backend |
| EVT-WF05-002 | Desativar Idioma | Usuário confirma desativação | UC04-FP-009 | Desativa idioma no backend |
| EVT-WF05-003 | Cancelamento | Usuário clica em CMP-WF05-006 | UC04-FA-002 | Fecha modal sem alterar |

### 8.4 Estados Obrigatórios

#### Estado 1: Confirmação de Ativação (Progresso >= 80%)
**Quando:** Idioma inativo com progresso >= 80%

**Exibir:**
- Título: "Ativar Idioma"
- Bandeira e nome do idioma (ex: 🇫🇷 Français)
- Progresso: 95% (barra verde)
- Mensagem: "O idioma Français será disponibilizado para todos os usuários. Continuar?"
- Botão "Ativar" (verde, primary)
- Botão "Cancelar" (cinza, secondary)

#### Estado 2: Confirmação de Ativação (Progresso < 80%)
**Quando:** Idioma inativo com progresso < 80%

**Exibir:**
- Título: "Ativar Idioma"
- Bandeira e nome do idioma (ex: 🇩🇪 Deutsch)
- Progresso: 65% (barra amarela com ⚠️)
- Alert amarelo: "⚠️ Idioma com 65% de tradução. 437 chaves faltantes usarão fallback para pt-BR. Ativar mesmo assim?"
- Botão "Ativar com Fallback" (amarelo, primary)
- Botão "Cancelar" (cinza, secondary)

#### Estado 3: Confirmação de Desativação (Idioma Comum)
**Quando:** Tentar desativar idioma que NÃO é pt-BR

**Exibir:**
- Título: "Desativar Idioma"
- Bandeira e nome do idioma (ex: 🇫🇷 Français)
- Progresso: 95%
- Alert amarelo: "⚠️ Usuários atualmente usando Français (12 usuários) serão redirecionados para pt-BR automaticamente. Desativar?"
- Botão "Desativar" (vermelho, danger)
- Botão "Cancelar" (cinza, secondary)

#### Estado 4: Bloqueio de Desativação (pt-BR)
**Quando:** Tentar desativar pt-BR (idioma padrão)

**Exibir:**
- Título: "Ação Bloqueada"
- Bandeira: 🇧🇷 Português (Brasil)
- Alert vermelho: "❌ Não é possível desativar o idioma padrão (pt-BR). Ele é obrigatório e sempre ativo."
- Botão "Voltar" (cinza, secondary)
- Botão "Desativar" **não exibido**

#### Estado 5: Processando
**Quando:** Usuário confirmou, backend processando

**Exibir:**
- Loading spinner
- Mensagem: "Atualizando status do idioma..."
- Botões desabilitados

#### Estado 6: Sucesso (Ativação)
**Quando:** Idioma ativado com sucesso

**Exibir:**
- Toast verde: "Idioma ativado! Agora disponível para todos os usuários."
- Modal fecha automaticamente (1s)
- Lista de idiomas (WF-01) atualizada
- Idioma destacado com badge verde "ATIVO"

#### Estado 7: Sucesso (Desativação)
**Quando:** Idioma desativado com sucesso

**Exibir:**
- Toast amarelo: "Idioma desativado. Usuários redirecionados para pt-BR."
- Modal fecha automaticamente (1s)
- Lista de idiomas (WF-01) atualizada
- Idioma destacado com badge cinza "INATIVO"

#### Estado 8: Erro
**Quando:** Falha ao atualizar status

**Exibir:**
- Alert vermelho: "Erro ao atualizar status do idioma. Tente novamente."
- Botão "Tentar Novamente"
- Botão "Cancelar"

### 8.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen
- **Tablet/Desktop:** Modal 600px largura, centralizado

#### Acessibilidade (WCAG AA)

- Botão de confirmação recebe foco automaticamente
- Esc fecha modal (com confirmação se ação iniciada)

#### Validações

- pt-BR: Botão "Desativar" sempre oculto/desabilitado
- Progresso < 80%: Exibe aviso obrigatório

#### Feedback Visual

- Cores semânticas:
  - Verde: Ativação bem-sucedida
  - Amarelo: Aviso de progresso < 80%
  - Vermelho: Desativação ou bloqueio pt-BR

---

## 9. WF-06 — HISTÓRICO DE VERSÕES (UC05)

### 9.1 Intenção da Tela

Permitir **visualização completa do histórico** de uploads de traduções, com data, usuário, chaves atualizadas e possibilidade de restaurar versões anteriores.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Título do Modal | Text | "Histórico de Versões - 🇫🇷 Français" |
| CMP-WF06-002 | Filtro de Período | Dropdown | Última semana / Último mês / Tudo |
| CMP-WF06-003 | Tabela de Versões | DataTable | Versão, Data/Hora, Usuário, Chaves Atualizadas, Progresso, Ações |
| CMP-WF06-004 | Badge Versão Atual | Badge (Info) | Destaca versão atual com "ATUAL" |
| CMP-WF06-005 | Botão Restaurar | Button (IconButton) | Ícone ↶ para restaurar versão |
| CMP-WF06-006 | Linha Expansível | TableRow (Expandable) | Exibe detalhes ao clicar na linha |
| CMP-WF06-007 | Botão Fechar | Button (Secondary) | Fecha modal |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Filtro de Período | Usuário seleciona no dropdown CMP-WF06-002 | UC05-FA-001 | Aplica filtro na query |
| EVT-WF06-002 | Expandir Detalhes | Usuário clica em linha da versão | UC05-FA-002 | Exibe metadata completa |
| EVT-WF06-003 | Restaurar | Usuário clica em CMP-WF06-005 | UC06 | Abre WF-07 (Confirmação de Rollback) |

### 9.4 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Modal aberto, buscando versões no backend

**Exibir:**
- Skeleton loader (tabela com 5 linhas simuladas)
- Mensagem: "Carregando histórico de versões..."

#### Estado 2: Vazio (Sem Versões)
**Quando:** Nenhuma versão encontrada

**Exibir:**
- Ícone ilustrativo (📜)
- Mensagem: "Nenhuma versão encontrada. Faça o primeiro upload de traduções."
- Botão "Fazer Upload" (redireciona para WF-04)

#### Estado 3: Dados (Histórico Exibido)
**Quando:** Há versões disponíveis

**Exibir:**
- Tabela com colunas:
  - **Versão:** v2.3 (com badge "ATUAL" na primeira linha)
  - **Data/Hora:** 2026-01-04 15:42
  - **Usuário:** João Silva (Admin)
  - **Chaves Atualizadas:** +150 / ~497 (adicionadas / modificadas)
  - **Progresso:** 95% (barra verde)
  - **Ações:** Botão ↶ Restaurar (desabilitado na versão atual)
- Versão atual destacada com background verde claro
- Paginação (se > 10 versões)

#### Estado 4: Detalhes Expandidos
**Quando:** Usuário clicou em linha da versão

**Exibir:**
- Linha expandida com:
  - **Arquivo original:** fr-FR-traducoes.json (245 KB)
  - **Hash MD5:** a1b2c3d4e5f6g7h8i9j0
  - **IP do upload:** 192.168.1.42
  - **Observações:** "Upload via Azure Translator API" (se automático)
  - **Tipo de operação:** UPLOAD / ROLLBACK / AUTO_TRANSLATE
  - **Delta de progresso:** 60% → 95% (+35%)

#### Estado 5: Erro ao Carregar
**Quando:** API retorna erro 500

**Exibir:**
- Ícone de erro (❌)
- Mensagem: "Erro ao carregar histórico. Tente novamente."
- Botão "Recarregar"

### 9.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Tabela convertida em cards, detalhes sempre expandidos
- **Tablet:** Tabela simplificada (ocultar coluna IP)
- **Desktop:** Tabela completa

#### Acessibilidade (WCAG AA)

- Linhas navegáveis por teclado (Tab)
- Enter expande/colapsa detalhes
- Screen reader: "Tabela de histórico de versões, 12 linhas"

#### Feedback Visual

- Versão atual sempre no topo
- Badge "ATUAL" destaca versão em uso
- Botão "Restaurar" desabilitado na versão atual

---

## 10. WF-07 — RESTAURAR VERSÃO ANTERIOR (ROLLBACK) (UC06)

### 10.1 Intenção da Tela

Permitir **restauração segura** de uma versão anterior de traduções, desfazendo uploads recentes em caso de erro ou regressão.

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Título do Modal | Text | "Restaurar Versão Anterior" |
| CMP-WF07-002 | Versão Selecionada | InfoBox | Versão, Data, Usuário, Progresso |
| CMP-WF07-003 | Versão Atual | InfoBox | Versão, Data, Progresso (será salva em histórico) |
| CMP-WF07-004 | Aviso de Versão Antiga | Alert (Warning) | Exibido se versão > 30 dias |
| CMP-WF07-005 | Botão Restaurar | Button (Primary) | Confirma restauração |
| CMP-WF07-006 | Botão Cancelar | Button (Secondary) | Cancela operação |

### 10.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF07-001 | Restaurar | Usuário confirma restauração | UC06-FP-007 | Restaura versão no backend |
| EVT-WF07-002 | Cancelamento | Usuário clica em CMP-WF07-006 | UC06-FA-001 | Fecha modal sem restaurar |

### 10.4 Estados Obrigatórios

#### Estado 1: Confirmação de Restauração (Versão Recente < 30 dias)
**Quando:** Versão selecionada tem menos de 30 dias

**Exibir:**
- Título: "Restaurar Versão Anterior"
- Versão selecionada:
  - v2.1 (2025-12-28 10:15)
  - Usuário: Maria Santos
  - Progresso: 85%
- Versão atual (será salva):
  - v2.3 (2026-01-04 15:42)
  - Progresso: 95%
- Mensagem: "A versão atual (v2.3) será salva no histórico antes de restaurar v2.1. Continuar?"
- Botão "Restaurar" (azul, primary)
- Botão "Cancelar" (cinza, secondary)

#### Estado 2: Confirmação de Restauração (Versão Antiga > 30 dias)
**Quando:** Versão selecionada tem mais de 30 dias

**Exibir:**
- Título: "Restaurar Versão Anterior"
- Versão selecionada:
  - v1.5 (2025-10-15 09:30)
  - Progresso: 60%
- Alert amarelo: "⚠️ Versão com mais de 2 meses. Restaurar pode causar regressões (muitas chaves podem desaparecer). Confirma?"
- Botão "Restaurar Mesmo Assim" (amarelo, primary)
- Botão "Cancelar" (cinza, secondary)

#### Estado 3: Processando Restauração
**Quando:** Usuário confirmou, backend restaurando

**Exibir:**
- Loading spinner
- Mensagem: "Restaurando versão... Criando backup da versão atual..."
- Etapas visíveis:
  - ✅ Backup da versão atual criado
  - ⏳ Restaurando traduções de v2.1...
  - ⏳ Recalculando progresso...
  - ⏳ Invalidando cache...
- Botões desabilitados

#### Estado 4: Sucesso
**Quando:** Restauração concluída

**Exibir:**
- Toast verde: "Versão v2.1 restaurada com sucesso! Progresso: 85% (anterior: 95%)"
- Modal fecha automaticamente (2s)
- Lista de idiomas (WF-01) atualizada
- Histórico de versões (WF-06) atualizado com nova entrada tipo ROLLBACK

#### Estado 5: Erro
**Quando:** Falha ao restaurar (timeout, constraint)

**Exibir:**
- Alert vermelho: "Erro ao restaurar versão. Nenhuma alteração foi feita. A versão atual (v2.3) está preservada."
- Botão "Tentar Novamente"
- Botão "Cancelar"

### 10.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen
- **Tablet/Desktop:** Modal 700px largura, centralizado

#### Acessibilidade (WCAG AA)

- Botão "Restaurar" recebe foco automaticamente
- Esc fecha modal (com confirmação)

#### Validações

- Transação atômica: rollback completo se falhar
- Backup da versão atual SEMPRE criado antes
- Registro de auditoria com versão restaurada

#### Feedback Visual

- Comparação visual entre versão atual e selecionada
- Delta de progresso exibido: "95% → 85% (-10%)"

---

## 11. WF-08 — VALIDAÇÃO DE INTEGRIDADE (UC07)

### 11.1 Intenção da Tela

Exibir **relatório automático de validação** de integridade de traduções, detectando interpolações incorretas, HTML não balanceado e chaves faltantes.

### 11.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF08-001 | Título do Modal | Text | "Relatório de Validação de Integridade - 🇫🇷 Français" |
| CMP-WF08-002 | Resumo de Validação | InfoBox | Total chaves validadas, erros, avisos |
| CMP-WF08-003 | Abas de Categoria | Tabs | Interpolações / HTML / Chaves Obrigatórias / Traduções Longas / Traduções Idênticas |
| CMP-WF08-004 | Lista de Erros | Table | Chave, Problema, Sugestão |
| CMP-WF08-005 | Botão Download CSV | Button (Secondary) | Baixa relatório completo em CSV |
| CMP-WF08-006 | Botão Fechar | Button (Secondary) | Fecha modal |

### 11.3 Estados Obrigatórios

#### Estado 1: Integridade OK (Nenhum Erro)
**Quando:** Validação não detectou erros ou avisos

**Exibir:**
- Ícone de sucesso (✅ grande)
- Mensagem: "Integridade OK! Nenhum erro ou aviso detectado."
- Total chaves validadas: 1.247
- Data/hora da validação: 2026-01-04 03:00 AM (Job automático)
- Botão "Fechar"

#### Estado 2: Erros Detectados
**Quando:** Há erros críticos

**Exibir:**
- Resumo:
  - Total chaves validadas: 1.247
  - ❌ Erros críticos: 12
  - ⚠️ Avisos: 8
- Abas de categoria com badge (ex: "Interpolações (5)")
- Tabela de erros:
  - **Chave:** `messages.welcome`
  - **Problema:** Interpolação `{{username}}` presente em pt-BR mas ausente na tradução
  - **Sugestão:** Adicione `{{username}}` na tradução
- Botão "Download Relatório CSV"
- Botão "Fechar"

#### Estado 3: Apenas Avisos (Não-Bloqueantes)
**Quando:** Apenas avisos detectados

**Exibir:**
- Resumo:
  - Total chaves validadas: 1.247
  - ✅ Erros críticos: 0
  - ⚠️ Avisos: 8
- Abas de categoria (apenas com avisos)
- Tabela de avisos:
  - **Chave:** `common.messages.longText`
  - **Problema:** Tradução muito longa (542 caracteres)
  - **Sugestão:** Considere dividir em múltiplas chaves

### 11.4 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen, tabela convertida em cards
- **Tablet/Desktop:** Modal 1100px largura

#### Acessibilidade (WCAG AA)

- Abas navegáveis por setas
- Leitores de tela anunciam total de erros/avisos

---

## 12. WF-09 — TRADUÇÃO AUTOMÁTICA (AZURE TRANSLATOR) (UC08)

### 12.1 Intenção da Tela

Permitir **tradução automática via Azure Translator API**, com estimativa de custo, validação de quota e marcação de traduções automáticas.

### 12.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF09-001 | Título do Modal | Text | "Tradução Automática - Azure Translator" |
| CMP-WF09-002 | Idioma Selecionado | InfoBox | Bandeira, Nome, Progresso atual |
| CMP-WF09-003 | Estimativa de Tradução | InfoBox | Chaves faltantes, caracteres estimados, custo USD |
| CMP-WF09-004 | Checkbox Namespace | Checkbox | ☑ Traduzir apenas namespace específico |
| CMP-WF09-005 | Dropdown Namespace | Select | Selecionar namespace (ex: common.buttons.*) |
| CMP-WF09-006 | Aviso de Custo | Alert (Warning) | Exibido se custo > $1.00 USD |
| CMP-WF09-007 | Botão Traduzir | Button (Primary) | Confirma tradução automática |
| CMP-WF09-008 | Botão Cancelar | Button (Secondary) | Cancela operação |

### 12.3 Estados Obrigatórios

#### Estado 1: Estimativa de Custo
**Quando:** Modal aberto

**Exibir:**
- Idioma: 🇫🇷 Français
- Progresso atual: 60%
- Chaves faltantes: 497
- Caracteres estimados: ~25.000 (média 50 chars/chave)
- Custo estimado: $0.25 USD
- Mensagem: "Traduzir automaticamente 497 chaves faltantes? Revisão humana será necessária."
- Botão "Traduzir Automaticamente" (azul, primary)
- Botão "Cancelar" (cinza, secondary)

#### Estado 2: Custo Alto (> $1.00 USD)
**Quando:** Custo estimado > $1.00 USD

**Exibir:**
- Alert amarelo: "⚠️ Custo estimado elevado ($3.50 USD). Considere traduzir por namespace específico."
- Checkbox habilitado: "Traduzir apenas namespace"
- Dropdown com namespaces disponíveis

#### Estado 3: Custo Excede Limite ($5.00 USD)
**Quando:** Custo estimado > $5.00 USD (limite configurável)

**Exibir:**
- Alert vermelho: "❌ Custo estimado excede limite configurado ($5.00 USD). Entre em contato com administrador."
- Botão "Traduzir Automaticamente" desabilitado
- Botão "Cancelar" habilitado

#### Estado 4: Processando Tradução
**Quando:** Usuário confirmou, Azure Translator API sendo chamada

**Exibir:**
- Loading spinner
- Barra de progresso (0% → 100%)
- Mensagem: "Traduzindo... 245/497 chaves (49%)"
- Lotes processados: 3/5
- Tempo estimado restante: ~12 segundos
- Botões desabilitados

#### Estado 5: Sucesso
**Quando:** Tradução automática concluída

**Exibir:**
- Toast verde: "497 chaves traduzidas automaticamente! Progresso: 60% → 95%. Revisão humana recomendada."
- Estatísticas:
  - Chaves traduzidas: 497
  - Custo real: $0.25 USD
  - Tempo de processamento: 18 segundos
  - Progresso anterior: 60% → Progresso novo: 95%
- Aviso: "⚠️ Traduções marcadas como automáticas. Recomenda-se revisão humana antes de ativar."
- Botão "Fazer Upload Manual para Revisão"
- Botão "Fechar"

#### Estado 6: Erro (Azure API Falhou)
**Quando:** Azure retorna erro (401, 429, 403)

**Exibir:**
- Alert vermelho:
  - 401: "Chave de API inválida. Configure a chave Azure Translator."
  - 429: "Rate limit excedido. Aguarde 60 segundos e tente novamente."
  - 403: "Quota mensal excedida. Aguarde renovação ou aumente o plano."
- Botão "Tentar Novamente" (se erro temporário)
- Botão "Cancelar"

### 12.4 Contratos de Comportamento

#### Responsividade

- **Mobile:** Modal fullscreen
- **Tablet/Desktop:** Modal 800px largura

#### Acessibilidade (WCAG AA)

- Estimativa de custo lida em voz alta
- Aviso de revisão humana destacado

#### Validações

- Azure API configurada (chave válida)
- Quota disponível
- Custo dentro do limite

#### Feedback Visual

- Barra de progresso em tempo real
- Custo atualizado dinamicamente ao selecionar namespace

---

## 13. WF-10 — EXPORTAR TRADUÇÕES (UC09)

### 13.1 Intenção da Tela

Permitir **exportação de traduções atuais** em 3 formatos (JSON, PO, XLSX), com opções de filtro e metadata.

### 13.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF10-001 | Título do Modal | Text | "Exportar Traduções - 🇫🇷 Français" |
| CMP-WF10-002 | Seletor de Formato | RadioGroup | JSON / PO / XLSX |
| CMP-WF10-003 | Checkbox Traduzidas | Checkbox | ☑ Incluir apenas chaves traduzidas |
| CMP-WF10-004 | Checkbox Metadata | Checkbox | ☑ Incluir metadata (data, versão, progresso) |
| CMP-WF10-005 | Checkbox Comentários | Checkbox | ☑ Incluir comentários/contexto |
| CMP-WF10-006 | Dropdown Namespace | Select | Exportar apenas namespace específico (opcional) |
| CMP-WF10-007 | Estatísticas | InfoBox | Total chaves a exportar, tamanho estimado |
| CMP-WF10-008 | Botão Exportar | Button (Primary) | Confirma exportação |
| CMP-WF10-009 | Botão Cancelar | Button (Secondary) | Cancela operação |

### 13.3 Estados Obrigatórios

#### Estado 1: Selecionando Opções
**Quando:** Modal aberto

**Exibir:**
- Idioma: 🇫🇷 Français
- Formato pré-selecionado: JSON
- Checkboxes desmarcadas por padrão (exceto Metadata)
- Estatísticas: Total chaves: 1.247 / Tamanho estimado: ~300 KB
- Botão "Exportar" habilitado

#### Estado 2: Gerando Arquivo
**Quando:** Usuário clicou em "Exportar"

**Exibir:**
- Loading spinner
- Mensagem: "Gerando arquivo de exportação..."
- Botões desabilitados

#### Estado 3: Sucesso
**Quando:** Arquivo gerado e download iniciado

**Exibir:**
- Toast verde: "Exportação concluída! Arquivo: fr-FR-export-2026-01-04.json"
- Modal fecha automaticamente (1s)

#### Estado 4: Erro
**Quando:** Falha ao gerar arquivo

**Exibir:**
- Alert vermelho: "Erro ao gerar exportação. Tente novamente."
- Botão "Tentar Novamente"

### 13.4 Contratos de Comportamento

Similares ao WF-03 (Baixar Template).

---

## 14. WF-11 — SELETOR DE IDIOMA (USUÁRIO FINAL) (UC10)

### 14.1 Intenção da Tela

Permitir que **usuários finais** (qualquer perfil autenticado) selecionem o idioma de sua preferência na interface, com detecção automática, fallback e cache.

### 14.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF11-001 | Seletor de Idioma (Header) | Dropdown | Exibido na navbar principal |
| CMP-WF11-002 | Idioma Atual | Badge | Bandeira + nome do idioma selecionado |
| CMP-WF11-003 | Dropdown Idiomas Ativos | Select | Lista de idiomas ativos com bandeiras |
| CMP-WF11-004 | Notificação de Alteração | Toast | Feedback após mudança de idioma |

### 14.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF11-001 | Abrir Seletor | Usuário clica em CMP-WF11-001 | UC10-FP-010 | Exibe dropdown com idiomas ativos |
| EVT-WF11-002 | Selecionar Idioma | Usuário seleciona idioma | UC10-FP-012 | Atualiza idioma no backend e recarrega interface |

### 14.4 Estados Obrigatórios

#### Estado 1: Primeiro Acesso (Detecção Automática)
**Quando:** Usuário faz login pela primeira vez

**Exibir:**
- Sistema detecta idioma via Accept-Language header ou GeoIP
- Se detectado e ativo: aplica automaticamente
- Se não detectado ou inativo: aplica pt-BR (fallback)
- Seletor exibe idioma detectado com bandeira

#### Estado 2: Idioma Selecionado
**Quando:** Usuário selecionou idioma manualmente

**Exibir:**
- Seletor com idioma atual: 🇫🇷 Français
- Dropdown com idiomas ativos (bandeira + nome)
- Idioma atual destacado com ícone ✅

#### Estado 3: Alterando Idioma
**Quando:** Usuário selecionou novo idioma

**Exibir:**
- Loading spinner no seletor
- Mensagem: "Alterando idioma..."
- Interface recarrega com novas traduções
- Toast verde: "Idioma alterado para Français"

#### Estado 4: Fallback (Idioma Incompleto)
**Quando:** Idioma selecionado tem progresso < 100%

**Exibir:**
- Interface exibe traduções disponíveis do idioma
- Chaves faltantes exibidas em pt-BR (fallback)
- Aviso discreto no rodapé: "🇫🇷 Français (95% traduzido) - Algumas mensagens em português"

### 14.5 Contratos de Comportamento

#### Responsividade

- **Mobile:** Seletor compacto (apenas bandeira, nome oculto)
- **Tablet/Desktop:** Seletor completo (bandeira + nome)

#### Acessibilidade (WCAG AA)

- Dropdown navegável por teclado
- Screen reader anuncia idioma atual

#### Detecção Automática

- Prioridade: Preferência salva > Accept-Language > GeoIP > pt-BR
- Validação: Idioma detectado deve estar ATIVO

#### Cache e Performance

- Traduções carregadas do Redis (TTL 24h)
- Lazy loading por namespace (carrega `common.*`, `menu.*` inicialmente)
- Namespaces adicionais carregados sob demanda

---

## 15. NOTIFICAÇÕES GLOBAIS

### 15.1 Tipos Padronizados

| Tipo | Uso | Cor | Ícone |
|----|----|-----|-------|
| Sucesso | Operação concluída | Verde | ✅ |
| Erro | Falha bloqueante | Vermelho | ❌ |
| Aviso | Atenção necessária | Amarelo | ⚠️ |
| Info | Feedback neutro | Azul | ℹ️ |

### 15.2 Exemplos

- **Sucesso:** "Idioma criado com sucesso!"
- **Erro:** "Erro ao carregar idiomas. Tente novamente."
- **Aviso:** "Idioma com 65% de tradução. Algumas mensagens em pt-BR."
- **Info:** "Upload concluído. Revisão humana recomendada."

---

## 16. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| Mobile (< 768px) | Tabelas → Cards empilhados / Modais fullscreen / Bandeiras sem texto |
| Tablet (768px - 1024px) | Tabelas simplificadas / Modais 80-90% largura / Layout responsivo |
| Desktop (> 1024px) | Tabelas completas / Modais largura fixa / Layout horizontal |

---

## 17. ACESSIBILIDADE (OBRIGATÓRIO)

- **Navegação por teclado:** Tab, Enter, Esc funcionais em todas as telas
- **Leitura por screen readers:** Labels descritivas, aria-labels em botões
- **Contraste mínimo WCAG AA:** 4.5:1 para texto normal, 3:1 para texto grande
- **Labels e descrições claras:** Sem siglas técnicas, português claro

---

## 18. RASTREABILIDADE (100% DOS UCs COBERTOS)

| Wireframe | UC(s) | Descrição |
|---------|-------|-----------|
| WF-01 | UC00 | Listagem de Idiomas |
| WF-02 | UC01 | Adicionar Novo Idioma |
| WF-03 | UC02 | Baixar Template de Tradução |
| WF-04 | UC03 | Upload de Traduções |
| WF-05 | UC04 | Ativar/Desativar Idioma |
| WF-06 | UC05 | Histórico de Versões |
| WF-07 | UC06 | Restaurar Versão (Rollback) |
| WF-08 | UC07 | Validação de Integridade |
| WF-09 | UC08 | Tradução Automática (Azure) |
| WF-10 | UC09 | Exportar Traduções |
| WF-11 | UC10 | Seletor de Idioma (Usuário) |

**Cobertura:** 11/11 UCs (100%) ✅

---

## 19. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores específicas, fontes, branding)
- Escolha de framework frontend (Angular, React, Vue)
- Design gráfico definitivo
- Animações avançadas
- Implementação técnica específica

---

## 20. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-04 | Agência ALC - alc.dev.br | Wireframes completos cobrindo 100% dos 11 UCs do RF005 |

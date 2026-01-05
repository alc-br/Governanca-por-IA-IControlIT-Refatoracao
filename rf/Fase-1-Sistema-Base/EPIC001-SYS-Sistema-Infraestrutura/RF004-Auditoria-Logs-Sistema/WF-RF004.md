# WF-RF004 — Wireframes Canônicos: Sistema de Auditoria e Logs do Sistema

**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Claude Sonnet 4.5 (Claude Code)

**RF Relacionado:** RF004 - Sistema de Auditoria e Logs do Sistema
**UC Relacionado:** UC-RF004 (UC00-UC08 - 9 casos de uso)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF004 — Sistema de Auditoria e Logs do Sistema.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional** em todas as telas de auditoria
- Servir como **fonte de verdade para IA, QA e Desenvolvimento**
- Permitir derivação direta de **TCs E2E e testes de usabilidade**
- Evitar dependência de ferramentas específicas (ex: Filament, React, Vue)

> ⚠️ Este documento descreve **o que a tela deve permitir e comunicar**, não **como será implementado tecnicamente**.

**IMPORTANTE:** RF004 **NÃO é um CRUD tradicional**. Registros de auditoria são **eventos imutáveis append-only**. Não há operações de CREATE, UPDATE ou DELETE pelo usuário. Os wireframes focam em **consulta, análise, visualização e gestão** de registros já criados automaticamente pelo sistema.

---

## 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)

### 2.1 Princípios Gerais

- Clareza acima de estética (compliance exige transparência total)
- Feedback imediato a toda ação do usuário
- Estados explícitos (loading, vazio, erro, dados)
- Não ocultar erros críticos (compliance)
- Comportamento previsível
- Rastreabilidade completa (CorrelationId sempre visível)

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis conforme permissões RBAC |
| Ações destrutivas | Sempre confirmadas + auditadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros, acionáveis e não vazar informações sensíveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Multi-tenancy | Isolamento visual de dados por tenant |
| Compliance | Informações de retenção, integridade e categorias visíveis |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF004)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Registros de Auditoria | UC00 | Descoberta, acesso e navegação inicial |
| WF-02 | Busca Avançada de Auditoria | UC01 | Investigação com filtros complexos |
| WF-03 | Timeline de Entidade | UC02 | Visualização cronológica de histórico |
| WF-04 | Exportação de Relatórios de Compliance | UC03 | Geração de relatórios LGPD/SOX/ISO |
| WF-05 | Dashboards Analíticos | UC04 | Métricas agregadas e gráficos |
| WF-06 | Detecção de Anomalias | UC05 | Alertas de comportamento suspeito |
| WF-07 | Validação de Integridade (Hash SHA-256) | UC06 | Verificação criptográfica |
| WF-08 | Detalhes de Registro de Auditoria | UC07 | Consulta detalhada de registro único |
| WF-09 | Gerenciamento de Retenção | UC08 | Políticas de retenção e alertas |

**Cobertura:** 9/9 UCs (100%)

---

## 4. WF-01 — LISTAGEM DE REGISTROS DE AUDITORIA (UC00)

### 4.1 Intenção da Tela
Permitir ao usuário **visualizar registros de auditoria do seu tenant** com paginação eficiente, filtros básicos e acesso rápido a detalhes.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Campo de Busca | Input | Busca textual rápida (termo livre) |
| CMP-WF01-002 | Filtro de Categoria | Dropdown | Filtrar por tipo de auditoria (10 categorias) |
| CMP-WF01-003 | Filtro de Período | DateRangePicker | Filtrar por intervalo de datas |
| CMP-WF01-004 | Botão "Busca Avançada" | Button | Acessar WF-02 (UC01) |
| CMP-WF01-005 | Tabela de Registros | DataTable | Exibição paginada de registros |
| CMP-WF01-006 | Botão "Ver Detalhes" | IconButton | Acessar WF-08 (UC07) por linha |
| CMP-WF01-007 | Botão "Ver Timeline" | IconButton | Acessar WF-03 (UC02) por entidade |
| CMP-WF01-008 | Paginação | Pagination | Controles de navegação (50/100/200 registros) |
| CMP-WF01-009 | Indicador de Multi-Tenancy | Badge | Mostrar tenant atual (informativo) |

**Colunas da Tabela (CMP-WF01-005):**
- Timestamp (ordenável, padrão DESC)
- Categoria (badge colorido por tipo)
- Descrição (resumida, max 80 caracteres)
- Usuário (nome + avatar)
- Entidade (tipo + ID)
- IP Address
- Ações (Ver Detalhes, Ver Timeline)

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Busca textual | Usuário digita em CMP-WF01-001 | UC00 | FA-UC00-001 |
| EVT-WF01-002 | Filtro por categoria | Usuário seleciona em CMP-WF01-002 | UC00 | FA-UC00-003 |
| EVT-WF01-003 | Filtro por período | Usuário define datas em CMP-WF01-003 | UC00 | FA-UC00-001 |
| EVT-WF01-004 | Clique em "Busca Avançada" | Usuário clica CMP-WF01-004 | UC01 | FP-UC01-001 |
| EVT-WF01-005 | Clique em "Ver Detalhes" | Usuário clica CMP-WF01-006 | UC07 | FP-UC07-001 |
| EVT-WF01-006 | Clique em "Ver Timeline" | Usuário clica CMP-WF01-007 | UC02 | FP-UC02-001 |
| EVT-WF01-007 | Mudança de página | Usuário interage com CMP-WF01-008 | UC00 | FA-UC00-004 |
| EVT-WF01-008 | Ordenação por coluna | Usuário clica header da tabela | UC00 | FA-UC00-002 |

### 4.4 Ações Permitidas
- Buscar registros por termo livre
- Filtrar por categoria de auditoria
- Filtrar por período (Data Inicial, Data Final)
- Ordenar por colunas (Timestamp, Categoria, Usuário, Entidade)
- Acessar detalhes de registro (WF-08)
- Acessar timeline de entidade (WF-03)
- Acessar busca avançada (WF-02)
- Alterar tamanho de página (50/100/200)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando registros de auditoria
**Exibir:**
- Skeleton loader (tabela com 10 linhas fantasma)
- Mensagem: "Carregando registros de auditoria..."
- Desabilitar filtros e ações temporariamente

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há registros de auditoria no tenant (raro em produção)
**Exibir:**
- Ícone ilustrativo (lupa + documento vazio)
- Mensagem: "Nenhum registro de auditoria encontrado"
- Submensagem: "Registros de auditoria são criados automaticamente pelo sistema conforme as operações são executadas."

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, timeout)
**Exibir:**
- Ícone de erro (⚠️)
- Mensagem: "Erro ao carregar registros de auditoria. Tente novamente."
- Botão "Recarregar"
- Código de erro (se disponível, para suporte técnico)

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há registros disponíveis
**Exibir:**
- Tabela completa com todas as colunas
- Paginação ativa (se > 50 registros)
- Filtros e busca funcionais
- Contadores: "Exibindo 1-50 de 1.523 registros"

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Lista empilhada (cards com dados principais: Timestamp, Categoria, Descrição, Usuário)
- **Tablet:** Tabela simplificada (6 colunas: Timestamp, Categoria, Descrição, Usuário, Entidade, Ações)
- **Desktop:** Tabela completa (todas as 7 colunas + ações)

#### Acessibilidade (WCAG AA)
- Labels em português claro ("Buscar registros", "Filtrar por categoria")
- Botões com aria-label ("Ver detalhes do registro de auditoria")
- Navegação por teclado (Tab, Enter, Esc)
- Contraste mínimo 4.5:1
- Screen reader: Anunciar quantidade de registros e mudanças de página

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso/erro após ações
- Indicador visual de filtros ativos
- Destaque de linha ao hover

#### Multi-Tenancy
- **OBRIGATÓRIO:** Filtro WHERE Tenant_Id = @TenantId aplicado automaticamente (invisível ao usuário)
- Badge visual informativo mostrando tenant atual (não editável)
- Nenhum dado de outro tenant deve aparecer, mesmo em erro

---

## 5. WF-02 — BUSCA AVANÇADA DE AUDITORIA (UC01)

### 5.1 Intenção da Tela
Permitir **investigações complexas** com múltiplos critérios combinados, salvamento de buscas favoritas e exportação de resultados.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo Período (Data Inicial) | DatePicker | Filtro de data inicial (obrigatório) |
| CMP-WF02-002 | Campo Período (Data Final) | DatePicker | Filtro de data final (obrigatório) |
| CMP-WF02-003 | Campo Categoria | MultiSelect | Filtro por múltiplas categorias |
| CMP-WF02-004 | Campo Entidade | Input | Filtro por tipo de entidade (ex: "Usuario", "Pedido") |
| CMP-WF02-005 | Campo Usuário | Input | Filtro por nome ou ID de usuário |
| CMP-WF02-006 | Campo IP Address | Input | Filtro por endereço IP |
| CMP-WF02-007 | Campo CorrelationId | Input | Filtro por rastreamento de transação |
| CMP-WF02-008 | Campo Full-Text | Input | Busca textual em todos os campos JSON |
| CMP-WF02-009 | Botão "Buscar" | Button | Executar busca com critérios |
| CMP-WF02-010 | Botão "Limpar Filtros" | Button | Resetar formulário |
| CMP-WF02-011 | Botão "Salvar Busca" | Button | Salvar critérios como favorito |
| CMP-WF02-012 | Botão "Carregar Busca Salva" | Button | Carregar busca favorita anterior |
| CMP-WF02-013 | Botão "Exportar Resultados" | Button | Redirecionar para WF-04 (UC03) |
| CMP-WF02-014 | Tabela de Resultados | DataTable | Mesma estrutura de WF-01, mas com resultados filtrados |
| CMP-WF02-015 | Contador de Resultados | Label | "X resultados encontrados em Ys" |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Submissão de Busca | Usuário clica CMP-WF02-009 | UC01 | FP-UC01-005 |
| EVT-WF02-002 | Limpar Filtros | Usuário clica CMP-WF02-010 | UC01 | FA-UC01-002 |
| EVT-WF02-003 | Salvar Busca Favorita | Usuário clica CMP-WF02-011 | UC01 | FA-UC01-001 |
| EVT-WF02-004 | Carregar Busca Salva | Usuário clica CMP-WF02-012 | UC01 | FA-UC01-002 |
| EVT-WF02-005 | Exportar Resultados | Usuário clica CMP-WF02-013 | UC03 | FA-UC01-003 |
| EVT-WF02-006 | Validação de Período | Sistema valida Data Final >= Data Inicial | UC01 | FE-UC01-001 |
| EVT-WF02-007 | Timeout de Query | Query > 30s | UC01 | FE-UC01-002 |

### 5.4 Ações Permitidas
- Definir múltiplos critérios de busca combinados (AND lógico)
- Salvar busca como favorita (nome + critérios)
- Carregar busca favorita anterior
- Exportar resultados (redireciona WF-04)
- Limpar todos os filtros

### 5.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está executando query complexa
**Exibir:**
- Skeleton loader na tabela de resultados
- Mensagem: "Buscando registros... (máx 30s)"
- Progress bar com timeout de 30 segundos
- Botão "Cancelar Busca" (abortar query)

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhum resultado encontrado com critérios informados
**Exibir:**
- Ícone ilustrativo (lupa + X)
- Mensagem: "Nenhum registro encontrado com os critérios informados"
- Botão "Limpar Filtros" (resetar para tentar nova busca)

#### Estado 3: Erro (Falha ao Buscar)
**Quando:**
- Data Final < Data Inicial (validação)
- Query timeout (> 30s)
- Erro de API (500, etc.)

**Exibir:**
- **Se validação:** Mensagem inline no campo com erro ("Data Final deve ser maior ou igual à Data Inicial")
- **Se timeout:** "Busca interrompida por timeout. Refine os critérios para reduzir o volume de dados."
- **Se erro API:** "Erro ao executar busca. Tente novamente. Código: [código]"

#### Estado 4: Dados (Resultados Exibidos)
**Quando:** Resultados encontrados e exibidos
**Exibir:**
- Tabela completa com resultados paginados
- Contador: "1.234 resultados encontrados em 2,3s"
- Filtros ativos destacados visualmente
- Botão "Exportar Resultados" habilitado

### 5.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única (1 campo por linha)
- **Tablet:** Formulário em 2 colunas (campos lado a lado)
- **Desktop:** Formulário em 3 colunas (otimização de espaço)

#### Acessibilidade (WCAG AA)
- Labels claros e descritivos
- Campos obrigatórios marcados com asterisco (*)
- Mensagens de erro inline próximas aos campos
- Navegação por teclado completa

#### Feedback ao Usuário
- Loading spinner durante execução de query
- Toast de sucesso ao salvar busca favorita
- Toast de erro se critérios inválidos
- Indicador visual de filtros ativos (badges)

#### Validações Obrigatórias
- Data Final >= Data Inicial (client-side + server-side)
- Período máximo: 1 ano (365 dias)
- Full-text search: mínimo 3 caracteres

---

## 6. WF-03 — TIMELINE DE ENTIDADE (UC02)

### 6.1 Intenção da Tela
Exibir **histórico completo e cronológico** de todas as operações realizadas em uma entidade específica, com visualização de snapshots before/after e diff estruturado.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Cabeçalho de Entidade | Card | Informações da entidade (Tipo, ID, Nome, Status Atual) |
| CMP-WF03-002 | Filtro Tipo de Operação | Dropdown | Filtrar por CREATE/UPDATE/DELETE |
| CMP-WF03-003 | Filtro Período | DateRangePicker | Filtrar timeline por intervalo de datas |
| CMP-WF03-004 | Timeline Visual | Timeline Component | Linha do tempo cronológica (ASC) |
| CMP-WF03-005 | Item de Timeline | Card | Cada evento (Timestamp, Tipo, Usuário, Snapshot) |
| CMP-WF03-006 | Botão "Comparar Versões" | Button | Abrir diff lado a lado (modal) |
| CMP-WF03-007 | Painel de Diff JSON Patch | Panel | Exibir diferenças estruturadas (RFC 6902) |
| CMP-WF03-008 | Botão "Exportar Timeline" | Button | Gerar PDF/JSON da timeline |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Filtro por Operação | Usuário seleciona tipo em CMP-WF03-002 | UC02 | FA-UC02-001 |
| EVT-WF03-002 | Filtro por Período | Usuário define datas em CMP-WF03-003 | UC02 | FA-UC02-002 |
| EVT-WF03-003 | Comparar Versões | Usuário seleciona 2 eventos e clica CMP-WF03-006 | UC02 | FA-UC02-003 |
| EVT-WF03-004 | Expandir Item | Usuário clica em item de timeline | UC02 | FP-UC02-006 |
| EVT-WF03-005 | Exportar Timeline | Usuário clica CMP-WF03-008 | UC03 | FA-UC02-001 |

### 6.4 Ações Permitidas
- Visualizar timeline cronológica completa (ASC)
- Filtrar por tipo de operação (CREATE, UPDATE, DELETE)
- Filtrar por período
- Expandir item para ver snapshots completos (before/after)
- Comparar duas versões (diff lado a lado)
- Exportar timeline como PDF ou JSON

### 6.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando histórico da entidade
**Exibir:**
- Skeleton loader na timeline (3-5 itens fantasma)
- Mensagem: "Carregando histórico de auditoria..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Entidade não possui histórico de auditoria
**Exibir:**
- Ícone ilustrativo (timeline vazia)
- Mensagem: "Nenhum registro de auditoria encontrado para esta entidade"
- Submensagem: "Isso pode ocorrer se a entidade foi criada antes da ativação do sistema de auditoria."

#### Estado 3: Erro (Falha ao Carregar)
**Quando:**
- Entidade não encontrada (404)
- Entidade pertence a outro tenant (403)
- Erro ao carregar JSON dos snapshots

**Exibir:**
- **Se 404:** "Entidade não encontrada. Verifique o ID informado."
- **Se 403:** "Acesso negado. Esta entidade pertence a outro tenant."
- **Se erro JSON:** "Erro ao carregar detalhes do histórico. Tente novamente. [código]"

#### Estado 4: Dados (Timeline Exibida)
**Quando:** Histórico encontrado e exibido
**Exibir:**
- Timeline cronológica completa (ordem ASC - mais antigo primeiro)
- Cada item com: Timestamp, Tipo (badge colorido), Usuário, Descrição, Botão "Ver Diff"
- Campos modificados destacados visualmente (amarelo)
- Contador: "12 eventos no histórico desta entidade"

### 6.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Timeline em coluna única (cards empilhados)
- **Tablet:** Timeline com itens expandidos (2 colunas de snapshot side-by-side)
- **Desktop:** Timeline completa com diff inline

#### Acessibilidade (WCAG AA)
- Timeline navegável por teclado (setas para cima/baixo)
- Screen reader: Anunciar tipo de operação e timestamp
- Contraste em badges de tipo de operação (CREATE verde, UPDATE azul, DELETE vermelho)

#### Feedback ao Usuário
- Highlight automático em campos modificados (diff visual)
- Loading spinner ao expandir item de timeline
- Toast de sucesso ao exportar timeline

#### Visualização de Diff
- **Campos adicionados:** Verde (+)
- **Campos removidos:** Vermelho (-)
- **Campos modificados:** Amarelo (before → after)
- JSON pretty-print com syntax highlighting

---

## 7. WF-04 — EXPORTAÇÃO DE RELATÓRIOS DE COMPLIANCE (UC03)

### 7.1 Intenção da Tela
Gerar **relatórios formatados para auditoria externa** (LGPD, SOX, ISO 27001) com hash SHA-256 de integridade.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Seletor Tipo de Relatório | RadioGroup | LGPD / SOX / ISO 27001 / Personalizado |
| CMP-WF04-002 | Campo Período (Data Inicial) | DatePicker | Obrigatório |
| CMP-WF04-003 | Campo Período (Data Final) | DatePicker | Obrigatório |
| CMP-WF04-004 | Seletor Formato | RadioGroup | PDF / Excel / JSON / CSV |
| CMP-WF04-005 | Checkbox "Incluir Hash SHA-256" | Checkbox | Adicionar hash de integridade ao arquivo |
| CMP-WF04-006 | Botão "Gerar Relatório" | Button | Executar geração |
| CMP-WF04-007 | Botão "Agendar Recorrência" | Button | Configurar envio automático por email |
| CMP-WF04-008 | Área de Download | Card | Link para download após geração |
| CMP-WF04-009 | Lista de Relatórios Anteriores | DataTable | Histórico de relatórios gerados |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Gerar Relatório | Usuário clica CMP-WF04-006 | UC03 | FP-UC03-004 |
| EVT-WF04-002 | Agendar Recorrência | Usuário clica CMP-WF04-007 | UC03 | FA-UC03-001 |
| EVT-WF04-003 | Download de Relatório | Usuário clica link em CMP-WF04-008 | UC03 | FP-UC03-009 |
| EVT-WF04-004 | Validação de Período | Sistema valida período máximo 1 ano | UC03 | FE-UC03-001 |
| EVT-WF04-005 | Timeout de Geração | Geração > 5 minutos | UC03 | FE-UC03-002 |

### 7.4 Ações Permitidas
- Selecionar tipo de relatório (LGPD/SOX/ISO/Personalizado)
- Definir período (máx 1 ano)
- Escolher formato de saída (PDF/Excel/JSON/CSV)
- Incluir hash SHA-256 de integridade
- Agendar envio automático recorrente por email
- Baixar relatório gerado
- Consultar histórico de relatórios anteriores

### 7.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está gerando relatório
**Exibir:**
- Progress bar com estimativa de tempo
- Mensagem: "Gerando relatório de compliance... Isso pode levar alguns minutos."
- Contador de registros processados (se disponível)

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhum registro encontrado no período selecionado
**Exibir:**
- Ícone ilustrativo (documento vazio)
- Mensagem: "Nenhum registro de auditoria encontrado no período informado"
- Botão "Alterar Período"

#### Estado 3: Erro (Falha ao Gerar)
**Quando:**
- Período excede 1 ano (validação)
- Volume muito grande (timeout)
- Erro ao gerar arquivo (500)

**Exibir:**
- **Se validação:** "Período máximo permitido: 1 ano. Ajuste as datas."
- **Se timeout:** "Volume de dados muito grande. Reduza o período ou refine os critérios."
- **Se erro API:** "Erro ao gerar relatório. Tente novamente. Código: [código]"

#### Estado 4: Dados (Relatório Gerado)
**Quando:** Relatório gerado com sucesso
**Exibir:**
- Card com informações do arquivo:
  - Nome do arquivo
  - Tamanho (MB)
  - Formato
  - Hash SHA-256 (se incluído)
  - Data/hora de geração
  - Botão "Baixar Relatório"
- Toast de sucesso: "Relatório gerado com sucesso!"

### 7.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 3 colunas + preview do relatório

#### Acessibilidade (WCAG AA)
- Labels claros indicando tipos de relatório
- Campos obrigatórios marcados
- Progress bar com aria-live para screen readers

#### Feedback ao Usuário
- Loading spinner durante geração
- Toast de sucesso com link de download
- Toast de erro se critérios inválidos
- Auditoria de exportação registrada (EXPORT category + hash SHA-256)

#### Compliance Obrigatório
- **LGPD:** Relatório deve incluir categorias FINANCIAL, LGPD, SECURITY (7 anos)
- **SOX:** Relatório deve incluir FINANCIAL, SECURITY (7 anos)
- **ISO 27001:** Relatório deve incluir SECURITY, AUTH, CONFIG (1-7 anos)
- Hash SHA-256 calculado para o arquivo final e registrado na auditoria

---

## 8. WF-05 — DASHBOARDS ANALÍTICOS (UC04)

### 8.1 Intenção da Tela
Exibir **métricas agregadas de auditoria** com gráficos visuais para análise gerencial.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Filtro de Período | DateRangePicker | Filtrar métricas por período (padrão: 30 dias) |
| CMP-WF05-002 | Gráfico 1: Operações por Categoria | PieChart | Pizza mostrando distribuição das 10 categorias |
| CMP-WF05-003 | Gráfico 2: Operações por Dia | LineChart | Linha temporal (últimos 30 dias) |
| CMP-WF05-004 | Gráfico 3: Top 10 Usuários | BarChart | Barra horizontal com usuários mais ativos |
| CMP-WF05-005 | Gráfico 4: Operações por Entidade | BarChart | Barra horizontal com entidades mais auditadas |
| CMP-WF05-006 | Gráfico 5: Distribuição de Retenção | PieChart | Pizza mostrando categorias por retenção (7a, 1a, 90d) |
| CMP-WF05-007 | Cards de Métricas Resumidas | StatCards | Total de registros, Média/dia, Categorias ativas, Alertas |
| CMP-WF05-008 | Botão "Exportar Gráfico" | Button | Exportar gráfico como PNG ou PDF |
| CMP-WF05-009 | Botão "Atualizar" | Button | Forçar recálculo de métricas (invalidar cache) |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Filtro por Período | Usuário define datas em CMP-WF05-001 | UC04 | FA-UC04-001 |
| EVT-WF05-002 | Drill-down em Categoria | Usuário clica fatia do gráfico CMP-WF05-002 | UC04 | FA-UC04-002 |
| EVT-WF05-003 | Exportar Gráfico | Usuário clica CMP-WF05-008 | UC04 | FA-UC04-003 |
| EVT-WF05-004 | Atualizar Métricas | Usuário clica CMP-WF05-009 | UC04 | FP-UC04-003 |

### 8.4 Ações Permitidas
- Filtrar métricas por período personalizado
- Drill-down em categoria (redireciona WF-02 com filtro pré-aplicado)
- Exportar gráfico individual como PNG ou PDF
- Forçar recálculo de métricas (invalidar cache)

### 8.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está calculando métricas agregadas
**Exibir:**
- Skeleton loader em todos os gráficos
- Mensagem: "Calculando métricas analíticas..."
- Progress bar (se cálculo > 5s)

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há registros no período selecionado
**Exibir:**
- Gráficos vazios com mensagem: "Nenhum dado no período selecionado"
- Botão "Alterar Período"

#### Estado 3: Erro (Falha ao Calcular)
**Quando:**
- Erro ao calcular métricas (500)
- Cache expirado (tempo de recálculo)

**Exibir:**
- **Se erro API:** "Erro ao calcular métricas. Tente novamente. Código: [código]"
- **Se cache expirado:** Recarregar automaticamente com loading spinner

#### Estado 4: Dados (Dashboards Exibidos)
**Quando:** Métricas calculadas e exibidas
**Exibir:**
- 5 gráficos completos com dados reais
- Cards de métricas resumidas
- Cache timestamp: "Atualizado há 3 minutos" (cache 5 min)
- Botão "Atualizar" habilitado

### 8.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Gráficos empilhados (1 coluna, ordem: Cards → Gráfico 1 → 2 → 3 → 4 → 5)
- **Tablet:** Gráficos em 2 colunas
- **Desktop:** Gráficos em grid 2x3

#### Acessibilidade (WCAG AA)
- Gráficos com alt text descritivo
- Tabelas de dados acessíveis via teclado (alternativa aos gráficos)
- Cores de gráficos com contraste suficiente

#### Feedback ao Usuário
- Loading spinner durante recálculo
- Toast ao exportar gráfico
- Indicador de cache (timestamp de última atualização)

#### Performance
- Cache de 5 minutos (Redis)
- Métricas pré-calculadas via Hangfire (job a cada 10 min)
- Drill-down redireciona WF-02 com filtro pré-aplicado (não recalcula)

---

## 9. WF-06 — DETECÇÃO DE ANOMALIAS (UC05)

### 9.1 Intenção da Tela
Exibir **alertas de comportamento suspeito** detectados automaticamente pelo sistema.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Filtro de Severidade | Dropdown | Filtrar por severidade (Crítica, Alta, Média, Baixa) |
| CMP-WF06-002 | Filtro de Tipo | Dropdown | Filtrar por tipo de anomalia (5 tipos) |
| CMP-WF06-003 | Tabela de Anomalias | DataTable | Lista de anomalias detectadas |
| CMP-WF06-004 | Botão "Investigar" | IconButton | Redirecionar para WF-02 com filtro CorrelationId |
| CMP-WF06-005 | Botão "Marcar Falso Positivo" | IconButton | Ocultar anomalia da lista |
| CMP-WF06-006 | Botão "Escalar Segurança" | IconButton | Criar ticket de escalação |
| CMP-WF06-007 | Botão "Configurar Thresholds" | Button | Abrir modal de configuração de limiares |
| CMP-WF06-008 | Modal de Thresholds | Modal | Formulário para ajustar valores de detecção |

**Colunas da Tabela (CMP-WF06-003):**
- Timestamp (quando foi detectada)
- Tipo (5 tipos: Exportações excessivas, Múltiplos tenants, Fora de horário, Acessos negados, Alterações massivas)
- Severidade (badge colorido: Crítica, Alta, Média, Baixa)
- Usuário suspeito
- Detalhes (descrição do comportamento anômalo)
- Ações (Investigar, Falso Positivo, Escalar)

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Filtro por Severidade | Usuário seleciona em CMP-WF06-001 | UC05 | FP-UC05-004 |
| EVT-WF06-002 | Filtro por Tipo | Usuário seleciona em CMP-WF06-002 | UC05 | FP-UC05-004 |
| EVT-WF06-003 | Investigar Anomalia | Usuário clica CMP-WF06-004 | UC05 | FP-UC05-005 |
| EVT-WF06-004 | Marcar Falso Positivo | Usuário clica CMP-WF06-005 | UC05 | FA-UC05-001 |
| EVT-WF06-005 | Escalar Segurança | Usuário clica CMP-WF06-006 | UC05 | FA-UC05-002 |
| EVT-WF06-006 | Configurar Thresholds | Usuário clica CMP-WF06-007 | UC05 | FA-UC05-003 |

### 9.4 Ações Permitidas
- Filtrar por severidade (Crítica, Alta, Média, Baixa)
- Filtrar por tipo de anomalia
- Investigar anomalia (redireciona WF-02 com filtro CorrelationId)
- Marcar como falso positivo (oculta da lista)
- Escalar para segurança (cria ticket)
- Configurar thresholds de detecção (apenas ADMIN)

### 9.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está executando detecção de anomalias
**Exibir:**
- Skeleton loader na tabela
- Mensagem: "Detectando anomalias... Isso pode levar alguns segundos."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhuma anomalia detectada
**Exibir:**
- Ícone ilustrativo (escudo verde ✓)
- Mensagem: "Nenhuma anomalia detectada no momento"
- Submensagem: "O sistema monitora automaticamente a cada 10 minutos."

#### Estado 3: Erro (Falha ao Detectar)
**Quando:** Erro ao executar detecção (500, timeout)
**Exibir:**
- Ícone de erro (⚠️)
- Mensagem: "Erro ao executar detecção de anomalias. Tente novamente."
- Botão "Recarregar"

#### Estado 4: Dados (Anomalias Detectadas)
**Quando:** Anomalias encontradas e exibidas
**Exibir:**
- Tabela completa com anomalias
- Badge de severidade colorido (Crítica: vermelho, Alta: laranja, Média: amarelo, Baixa: azul)
- Contador: "23 anomalias detectadas (15 críticas, 8 altas)"
- Botão "Configurar Thresholds" visível (apenas ADMIN)

### 9.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Lista empilhada (cards com dados principais: Tipo, Severidade, Usuário, Detalhes)
- **Tablet:** Tabela simplificada (5 colunas)
- **Desktop:** Tabela completa (todas as colunas + ações)

#### Acessibilidade (WCAG AA)
- Badges de severidade com contraste adequado
- Ações com aria-label descritivo
- Navegação por teclado completa

#### Feedback ao Usuário
- Toast ao marcar falso positivo
- Toast ao escalar para segurança
- Confirmação antes de escalar (modal)

#### Detecção Automática (5 tipos)
1. **Exportações excessivas:** > 100 exportações/hora
2. **Múltiplos tenants:** Acesso a > 50 tenants/dia
3. **Fora de horário:** Operações entre 22h-6h
4. **Acessos negados:** > 10 tentativas negadas/hora
5. **Alterações massivas:** > 100 operações UPDATE/DELETE por minuto

**Severidade Automática:**
- **Crítica:** Múltiplos thresholds violados simultaneamente
- **Alta:** 1 threshold crítico violado (ex: > 200 exportações/hora)
- **Média:** 1 threshold moderado violado
- **Baixa:** Threshold próximo ao limite (aviso preventivo)

---

## 10. WF-07 — VALIDAÇÃO DE INTEGRIDADE (HASH SHA-256) (UC06)

### 10.1 Intenção da Tela
Permitir **verificação criptográfica de integridade** de registros de auditoria (individual ou lote).

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Seletor Modo | RadioGroup | "Registro Específico" ou "Período" |
| CMP-WF07-002 | Campo ID de Registro | Input | ID do registro a validar (se modo = específico) |
| CMP-WF07-003 | Campo Período | DateRangePicker | Período a validar (se modo = período) |
| CMP-WF07-004 | Botão "Validar" | Button | Executar validação de integridade |
| CMP-WF07-005 | Botão "Exportar Relatório" | Button | Gerar PDF/Excel com resultado |
| CMP-WF07-006 | Botão "Agendar Validação" | Button | Configurar validação automática recorrente |
| CMP-WF07-007 | Tabela de Resultados | DataTable | Resultado da validação (por registro) |
| CMP-WF07-008 | Card de Resumo | Card | Resumo: X íntegros, Y corrompidos |

**Colunas da Tabela (CMP-WF07-007):**
- ID do Registro
- Timestamp
- Tipo
- Entidade
- Hash Armazenado (primeiros 16 caracteres)
- Hash Recalculado (primeiros 16 caracteres)
- Status (✅ Íntegro ou ❌ Corrompido)

### 10.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF07-001 | Validar Integridade | Usuário clica CMP-WF07-004 | UC06 | FP-UC06-005 |
| EVT-WF07-002 | Exportar Relatório | Usuário clica CMP-WF07-005 | UC06 | FA-UC06-001 |
| EVT-WF07-003 | Agendar Validação | Usuário clica CMP-WF07-006 | UC06 | FA-UC06-002 |
| EVT-WF07-004 | Detecção de Corrupção | Hash divergente detectado | UC06 | FE-UC06-001 |

### 10.4 Ações Permitidas
- Validar integridade de registro específico (informar ID)
- Validar integridade de lote (informar período: 7d, 30d, 1a)
- Exportar relatório de integridade (PDF/Excel)
- Agendar validação automática recorrente (Hangfire job + email)

### 10.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está recalculando hashes e comparando
**Exibir:**
- Progress bar com contador de registros validados
- Mensagem: "Validando integridade... X/Y registros processados"

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhum registro encontrado no critério informado
**Exibir:**
- Mensagem: "Nenhum registro encontrado para validar"

#### Estado 3: Erro (Falha ao Validar)
**Quando:**
- Registro não encontrado (404)
- Erro ao recalcular hash (500)

**Exibir:**
- **Se 404:** "Registro não encontrado. Verifique o ID informado."
- **Se erro API:** "Erro ao recalcular hash. Tente novamente. Código: [código]"

#### Estado 4: Dados (Validação Concluída)
**Quando:** Validação concluída (sucesso ou corrupção detectada)
**Exibir:**
- Tabela completa com resultados
- Card de resumo:
  - **Se todos íntegros:** "✅ Todos os registros estão íntegros!" (verde)
  - **Se corrompido:** "❌ ALERTA CRÍTICO: Corrupção detectada em X registros!" (vermelho)
- Botão "Exportar Relatório" habilitado

### 10.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em coluna única + tabela de resultados simplificada
- **Tablet:** Formulário em 2 colunas + tabela completa
- **Desktop:** Formulário em linha + tabela completa + preview de hash

#### Acessibilidade (WCAG AA)
- Labels claros indicando modos de validação
- Status de integridade com ícones + texto (não só cor)

#### Feedback ao Usuário
- Progress bar durante validação
- Toast de sucesso se todos íntegros
- **ALERTA CRÍTICO** se corrupção detectada (modal bloqueante)
- Auditoria da validação registrada (SECURITY category)

#### Algoritmo de Validação
1. Carregar registro(s) do banco
2. Extrair Hash_SHA256 armazenado
3. Recalcular hash SHA-256 (concatenação de campos conforme especificação)
4. Comparar hash armazenado vs recalculado
5. Resultado: ✅ Íntegro (hashes iguais) ou ❌ Corrompido (hashes diferentes)

**Se corrompido detectado:**
- Registrar alerta em SECURITY category
- Notificar administradores por email (configurável)
- Bloquear acesso aos dados corrompidos (quarentena)

---

## 11. WF-08 — DETALHES DE REGISTRO DE AUDITORIA (UC07)

### 11.1 Intenção da Tela
Exibir **todos os detalhes** de um registro específico de auditoria em 5 painéis estruturados.

### 11.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF08-001 | Painel 1: Informações Gerais | Card | Timestamp, Tipo, Descrição, Entidade, EntidadeId |
| CMP-WF08-002 | Painel 2: Contexto | Card | Usuário, IP, UserAgent, CorrelationId |
| CMP-WF08-003 | Painel 3: Snapshots | Card | DadosAnteriores_JSON, DadosNovos_JSON, Diff_JSON (JSON Patch RFC 6902) |
| CMP-WF08-004 | Painel 4: Integridade | Card | Hash_SHA256, Botão "Validar Integridade" |
| CMP-WF08-005 | Painel 5: Retenção | Card | RetentionDate, Arquivado, AzureBlobUri |
| CMP-WF08-006 | Botão "Copiar CorrelationId" | IconButton | Copiar para clipboard |
| CMP-WF08-007 | Botão "Rastrear CorrelationId" | Button | Redirecionar WF-02 com filtro |
| CMP-WF08-008 | Botão "Exportar JSON" | Button | Baixar registro completo como JSON |
| CMP-WF08-009 | Botão "Ver Timeline" | Button | Redirecionar WF-03 para entidade |

### 11.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF08-001 | Copiar CorrelationId | Usuário clica CMP-WF08-006 | UC07 | FA-UC07-001 |
| EVT-WF08-002 | Rastrear CorrelationId | Usuário clica CMP-WF08-007 | UC07 | FA-UC07-002 |
| EVT-WF08-003 | Exportar JSON | Usuário clica CMP-WF08-008 | UC07 | FA-UC07-003 |
| EVT-WF08-004 | Ver Timeline | Usuário clica CMP-WF08-009 | UC02 | FP-UC02-001 |
| EVT-WF08-005 | Validar Integridade | Usuário clica botão em CMP-WF08-004 | UC06 | FP-UC06-001 |

### 11.4 Ações Permitidas
- Visualizar todos os detalhes do registro
- Copiar CorrelationId para clipboard
- Rastrear CorrelationId (redireciona WF-02 com filtro)
- Exportar registro como JSON
- Validar integridade (redireciona WF-07)
- Ver timeline da entidade (redireciona WF-03)

### 11.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está carregando detalhes do registro
**Exibir:**
- Skeleton loader nos 5 painéis
- Mensagem: "Carregando detalhes do registro..."

#### Estado 2: Vazio (Sem Dados)
**Não aplicável** (sempre há um registro ao acessar esta tela)

#### Estado 3: Erro (Falha ao Carregar)
**Quando:**
- Registro não encontrado (404)
- Registro de outro tenant (403)
- Erro ao renderizar JSON (malformed)

**Exibir:**
- **Se 404:** "Registro não encontrado. Verifique o ID informado."
- **Se 403:** "Acesso negado. Este registro pertence a outro tenant."
- **Se erro JSON:** Exibir JSON bruto + log técnico

#### Estado 4: Dados (Detalhes Exibidos)
**Quando:** Registro carregado com sucesso
**Exibir:**
- 5 painéis completos com todos os dados
- JSON pretty-print com syntax highlighting
- Diff visual destacando campos modificados (amarelo)
- Botões de ação habilitados

### 11.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Painéis empilhados (1 coluna)
- **Tablet:** Painéis em 2 colunas (Painel 1+2 / Painel 3+4 / Painel 5)
- **Desktop:** Painéis em grid 2x3

#### Acessibilidade (WCAG AA)
- JSON navegável por teclado (tree view colapsável)
- Screen reader: Anunciar seção ao expandir painel
- Contraste adequado em syntax highlighting

#### Feedback ao Usuário
- Toast ao copiar CorrelationId ("Copiado para a área de transferência!")
- Loading spinner ao validar integridade
- Highlight em campos modificados (diff visual)

#### Estrutura dos 5 Painéis

**Painel 1: Informações Gerais**
- Timestamp (formato: "DD/MM/YYYY HH:mm:ss")
- Tipo (badge colorido por categoria)
- Descrição (texto completo)
- Entidade (tipo + ID)
- Status (se aplicável)

**Painel 2: Contexto**
- Usuário (nome + avatar + ID)
- IP Address (com link para geolocalização, se disponível)
- User Agent (browser + SO)
- CorrelationId (com botões "Copiar" e "Rastrear")

**Painel 3: Snapshots**
- DadosAnteriores_JSON (JSON pretty-print, colapsável)
- DadosNovos_JSON (JSON pretty-print, colapsável)
- Diff_JSON (JSON Patch RFC 6902, com highlight de operações: add, remove, replace)

**Painel 4: Integridade**
- Hash_SHA256 (exibir completo, com botão "Copiar")
- Botão "Validar Integridade" (redireciona WF-07)
- Algoritmo: SHA-256
- Status: ✅ Íntegro ou ❌ Corrompido (se já validado)

**Painel 5: Retenção**
- RetentionDate (data de expiração)
- Dias restantes até expiração (countdown)
- Arquivado: Sim/Não
- AzureBlobUri (se arquivado, link para download)
- Categoria de retenção (FINANCIAL/LGPD/SECURITY: 7a, outros: 1a/90d)

---

## 12. WF-09 — GERENCIAMENTO DE RETENÇÃO (UC08)

### 12.1 Intenção da Tela
Gerenciar **políticas de retenção** por categoria e exibir **alertas de registros próximos ao vencimento**.

### 12.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF09-001 | Tabela de Configuração | DataTable | Configuração de retenção das 10 categorias |
| CMP-WF09-002 | Campo Dias de Retenção | Input | Ajustar dias de retenção (apenas não-compliance) |
| CMP-WF09-003 | Botão "Salvar Alterações" | Button | Salvar configurações ajustadas |
| CMP-WF09-004 | Tabela de Alertas | DataTable | Registros expirando em 30 dias |
| CMP-WF09-005 | Botão "Arquivar Vencidos" | Button | Arquivar registros vencidos (Azure Blob) |
| CMP-WF09-006 | Botão "Restaurar Arquivados" | Button | Restaurar registros do Azure Blob |
| CMP-WF09-007 | Botão "Excluir Vencidos" | Button | Excluir vencidos (apenas não-compliance, com confirmação) |
| CMP-WF09-008 | Modal de Confirmação | Modal | Confirmação de exclusão (irreversível) |

**Colunas da Tabela de Configuração (CMP-WF09-001):**
- Categoria (10 categorias)
- Dias de Retenção (editável para não-compliance, fixo para compliance)
- Compliance (Sim/Não)
- Total de Registros
- Vencidos (últimos 30 dias)
- Ações (Arquivar, Excluir - apenas se não-compliance)

**Colunas da Tabela de Alertas (CMP-WF09-004):**
- Categoria
- Quantidade de Registros
- Data de Vencimento
- Ações Disponíveis (Arquivar, Excluir)

### 12.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF09-001 | Ajustar Retenção | Usuário edita CMP-WF09-002 | UC08 | FP-UC08-005 |
| EVT-WF09-002 | Salvar Alterações | Usuário clica CMP-WF09-003 | UC08 | FP-UC08-006 |
| EVT-WF09-003 | Arquivar Vencidos | Usuário clica CMP-WF09-005 | UC08 | FA-UC08-001 |
| EVT-WF09-004 | Restaurar Arquivados | Usuário clica CMP-WF09-006 | UC08 | FA-UC08-002 |
| EVT-WF09-005 | Excluir Vencidos | Usuário clica CMP-WF09-007 | UC08 | FA-UC08-003 |
| EVT-WF09-006 | Tentativa Alterar Compliance | Usuário tenta editar categoria compliance | UC08 | FE-UC08-001 |
| EVT-WF09-007 | Tentativa Excluir Compliance | Usuário tenta excluir categoria compliance | UC08 | FE-UC08-002 |

### 12.4 Ações Permitidas
- Visualizar configuração de retenção das 10 categorias
- Ajustar dias de retenção (apenas categorias não-compliance)
- Salvar configurações ajustadas
- Visualizar alertas de vencimento (30 dias)
- Arquivar registros vencidos (Azure Blob cold tier)
- Restaurar registros arquivados
- Excluir registros vencidos (apenas não-compliance, com confirmação)

### 12.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está carregando configurações e alertas
**Exibir:**
- Skeleton loader nas tabelas
- Mensagem: "Carregando políticas de retenção..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Nenhum alerta de vencimento (raro)
**Exibir:**
- Mensagem: "Nenhum registro próximo ao vencimento nos próximos 30 dias"
- Configuração de retenção continua exibida

#### Estado 3: Erro (Falha ao Salvar/Arquivar)
**Quando:**
- Tentativa de alterar categoria compliance (bloqueio)
- Tentativa de excluir categoria compliance (bloqueio)
- Erro ao arquivar no Azure Blob (500)

**Exibir:**
- **Se bloqueio compliance:** "BLOQUEADO: Categorias de compliance (FINANCIAL, LGPD, SECURITY) têm retenção fixa de 7 anos por exigência legal."
- **Se erro Azure Blob:** "Erro ao arquivar registros. Tente novamente. Código: [código]"

#### Estado 4: Dados (Configuração e Alertas Exibidos)
**Quando:** Dados carregados com sucesso
**Exibir:**
- Tabela de configuração completa
- Tabela de alertas (se houver registros vencendo em 30 dias)
- Campos editáveis apenas para não-compliance
- Botões de ação habilitados conforme categoria

### 12.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Tabelas empilhadas (cards com dados principais)
- **Tablet:** Tabelas simplificadas (6 colunas)
- **Desktop:** Tabelas completas (todas as colunas + ações)

#### Acessibilidade (WCAG AA)
- Campos desabilitados (compliance) com tooltip explicativo
- Confirmação de exclusão com modal bloqueante
- Screen reader: Anunciar categoria e compliance ao navegar

#### Feedback ao Usuário
- Toast ao salvar configurações
- Toast ao arquivar/restaurar
- **CONFIRMAÇÃO OBRIGATÓRIA** antes de exclusão (modal bloqueante)
- Auditoria de todas as operações (ADMIN category)

#### Políticas de Retenção (10 Categorias)

**Compliance (FIXA - 7 anos):**
1. FINANCIAL (Compliance SOX Seção 404)
2. LGPD (Compliance LGPD Art. 37, 38, 46)
3. SECURITY (Compliance ISO 27001)

**Não-Compliance (AJUSTÁVEL - 30 dias a 10 anos):**
4. CRUD (padrão: 1 ano)
5. AUTH (padrão: 1 ano)
6. EXPORT (padrão: 1 ano)
7. CONFIG (padrão: 1 ano)
8. ADMIN (padrão: 1 ano)
9. PRINT (padrão: 90 dias)
10. ACCESS (padrão: 90 dias)

**Alertas de Vencimento:**
- Sistema exibe alertas para registros com RetentionDate <= HOJE + 30 dias
- Ações disponíveis:
  - **Arquivar:** Move para Azure Blob Storage (cold tier), marca Arquivado = TRUE
  - **Restaurar:** Copia do Azure Blob de volta ao banco, marca Arquivado = FALSE
  - **Excluir:** DELETE permanente (apenas não-compliance, com confirmação irreversível)

**Bloqueios de Segurança:**
- **FINANCIAL/LGPD/SECURITY:** Não podem ser alterados (7 anos fixo)
- **FINANCIAL/LGPD/SECURITY:** Não podem ser excluídos (apenas arquivamento permitido)
- Tentativa de violação gera bloqueio + auditoria em SECURITY category

---

## 13. NOTIFICAÇÕES

### 13.1 Tipos Padronizados

| Tipo | Uso | Exemplo (RF004) |
|----|----|------------------|
| Sucesso | Operação concluída | "Relatório de compliance gerado com sucesso!" |
| Erro | Falha bloqueante | "Erro ao carregar registros de auditoria. Tente novamente." |
| Aviso | Atenção necessária | "Período máximo permitido: 1 ano. Ajuste as datas." |
| Info | Feedback neutro | "Busca salva como favorita: 'Auditoria LGPD Q1 2026'" |

### 13.2 Posicionamento
- **Toast:** Canto superior direito (4 segundos de duração)
- **Inline:** Próximo ao campo/componente relacionado
- **Modal:** Centro da tela (bloqueante, requer ação do usuário)

---

## 14. RESPONSIVIDADE (OBRIGATÓRIO)

### 14.1 Breakpoints

| Contexto | Largura | Comportamento |
|-------|---------|---------------|
| Mobile | < 768px | Layout em coluna única, cards empilhados, tabelas em modo lista |
| Tablet | 768px - 1024px | Layout em 2 colunas, tabelas simplificadas |
| Desktop | > 1024px | Layout completo em grid, todas as colunas visíveis |

### 14.2 Adaptações por Contexto

**Mobile:**
- Navegação por menu hamburger
- Filtros em drawer lateral
- Tabelas transformadas em cards (modo lista)
- Gráficos empilhados verticalmente
- Botões de ação em menu de contexto (⋮)

**Tablet:**
- Navegação em sidebar colapsável
- Filtros em painel lateral
- Tabelas com rolagem horizontal
- Gráficos em 2 colunas

**Desktop:**
- Navegação em sidebar fixa
- Filtros sempre visíveis
- Tabelas completas com todas as colunas
- Gráficos em grid otimizado

---

## 15. ACESSIBILIDADE (OBRIGATÓRIO)

### 15.1 Navegação por Teclado

| Tecla | Ação |
|-------|------|
| Tab | Navegar entre componentes |
| Enter | Ativar botão/link |
| Esc | Fechar modal/dropdown |
| Setas | Navegar em listas/tabelas |
| Espaço | Selecionar checkbox/radio |

### 15.2 Screen Readers

- Todos os componentes têm `aria-label` descritivo
- Mudanças de estado anunciadas via `aria-live`
- Estrutura semântica correta (headings, landmarks, regions)

### 15.3 Contraste (WCAG AA)

- Contraste mínimo texto/fundo: 4.5:1
- Contraste mínimo elementos de UI: 3:1
- Badges de severidade com ícones + texto (não só cor)

### 15.4 Labels e Descrições

- Todos os campos têm labels em português claro
- Campos obrigatórios marcados com asterisco (*)
- Mensagens de erro descritivas e acionáveis

---

## 16. RASTREABILIDADE

| Wireframe | UC | RF | Tipo de Tela |
|---------|----|----|--------------|
| WF-01 | UC00 | RF004 | Listagem |
| WF-02 | UC01 | RF004 | Busca Avançada |
| WF-03 | UC02 | RF004 | Timeline |
| WF-04 | UC03 | RF004 | Exportação |
| WF-05 | UC04 | RF004 | Dashboards |
| WF-06 | UC05 | RF004 | Detecção de Anomalias |
| WF-07 | UC06 | RF004 | Validação de Integridade |
| WF-08 | UC07 | RF004 | Detalhes de Registro |
| WF-09 | UC08 | RF004 | Gerenciamento de Retenção |

**Cobertura:** 9/9 UCs (100%)

---

## 17. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, fontes, espaçamentos)
- Escolha de framework (React, Vue, Angular, Filament)
- Design gráfico definitivo (apenas contratos funcionais)
- Animações avançadas (apenas transições básicas de loading/feedback)
- Implementação técnica (apenas especificação comportamental)

---

## 18. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-04 | Claude Sonnet 4.5 (Claude Code) | Criação completa de WF-RF004 com 9 wireframes cobrindo 100% dos UCs (UC00-UC08). Estados obrigatórios, responsividade, acessibilidade e compliance implementados. |

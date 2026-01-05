# WF-RF003 — Wireframes Canônicos: Sistema de Logs, Monitoramento e Observabilidade

**Versão:** 1.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF003 - Sistema de Logs, Monitoramento e Observabilidade
**UC Relacionado:** UC-RF003 (UC00 a UC07)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF003.

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
- Dados sensíveis mascarados (CPF, senhas, cartões) conforme RN-LOG-004

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações de exportação | Confirmação de formato |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Dados sensíveis | Sempre mascarados (RN-LOG-004) |
| Correlation IDs | Clicáveis para rastreamento (RN-LOG-003) |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF003)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem de Logs | UC00 | Descoberta e acesso aos logs do sistema |
| WF-02 | Busca Avançada de Logs | UC01 | Filtros avançados (CorrelationId, UserId, IP, texto) |
| WF-03 | Detalhes de Log | UC02 | Visualização completa de log com stack trace |
| WF-04 | Exportação de Logs | UC03 | Export CSV/JSON para compliance |
| WF-05 | Configuração de Alertas | UC04 | Configurar thresholds e notificações |
| WF-06 | Dashboards de Métricas | UC05 | Métricas RED (Rate, Errors, Duration) |
| WF-07 | Health Checks | UC06 | Status de dependências críticas |
| WF-08 | Tracing Distribuído | UC07 | Rastreamento end-to-end de requests |

---

## 4. WF-01 — LISTAGEM DE LOGS (UC00)

### 4.1 Intenção da Tela
Permitir ao usuário **visualizar, filtrar e navegar pelos logs do sistema** do seu tenant, com mascaramento automático de dados sensíveis.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Filtro de Período | Dropdown | Últimas 24h / Última semana / Personalizado |
| CMP-WF01-002 | Filtro de Nível | Dropdown | Verbose, Debug, Info, Warning, Error, Fatal |
| CMP-WF01-003 | Campo de Busca Rápida | Input | Busca textual rápida (navega para UC01) |
| CMP-WF01-004 | Tabela de Logs | DataTable | Colunas: Timestamp, Level, Message, CorrelationId, UserId |
| CMP-WF01-005 | Botão Busca Avançada | Button | Abre WF-02 (UC01) |
| CMP-WF01-006 | Botão Exportar | Button | Abre WF-04 (UC03) |
| CMP-WF01-007 | Paginação | Pagination | 100 logs por página |
| CMP-WF01-008 | Indicador Loading | Spinner | Exibido durante carregamento |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Filtro por período | Usuário seleciona período em CMP-WF01-001 | UC00 | FA-UC00-01 |
| EVT-WF01-002 | Filtro por nível | Usuário seleciona nível em CMP-WF01-002 | UC00 | FA-UC00-02 |
| EVT-WF01-003 | Ordenação | Usuário clica em cabeçalho de coluna | UC00 | FA-UC00-03 |
| EVT-WF01-004 | Clique em log | Usuário clica em linha da tabela CMP-WF01-004 | UC02 | FP-UC02-001 |
| EVT-WF01-005 | Busca avançada | Usuário clica em CMP-WF01-005 | UC01 | FP-UC01-001 |
| EVT-WF01-006 | Exportar | Usuário clica em CMP-WF01-006 | UC03 | FP-UC03-001 |
| EVT-WF01-007 | Mudança de página | Usuário interage com CMP-WF01-007 | UC00 | FP-UC00-004 |

### 4.4 Ações Permitidas
- Visualizar últimos 100 logs do tenant
- Filtrar por período (últimas 24h, semana, personalizado)
- Filtrar por nível de log (Verbose até Fatal)
- Ordenar por timestamp, nível, mensagem
- Navegar para detalhes de log (UC02)
- Navegar para busca avançada (UC01)
- Exportar logs (UC03)

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando logs do tenant

**Exibir:**
- CMP-WF01-008: Skeleton loader na tabela
- Mensagem: "Carregando logs do sistema..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há logs no período selecionado

**Exibir:**
- Ícone ilustrativo (documento vazio)
- Mensagem: "Nenhum log encontrado no período selecionado."
- Sugestão: "Ajuste os filtros de período ou nível."

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, etc.) ou usuário sem permissão SYS.LOGS.READ

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado. Permissão SYS.LOGS.READ necessária."
  - Se 500: "Erro ao carregar logs. Tente novamente."
- Botão "Recarregar"

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há logs disponíveis no período

**Exibir:**
- CMP-WF01-004: Tabela com colunas:
  - **Timestamp** (ISO 8601, ex: 2026-01-04T14:30:15Z)
  - **Level** (badge colorido: Error=vermelho, Warning=amarelo, Info=azul)
  - **Message** (mascaramento automático aplicado - RN-LOG-004)
  - **CorrelationId** (GUID clicável - navega para logs relacionados)
  - **UserId** (email do usuário autenticado)
- Paginação (CMP-WF01-007) se > 100 registros
- Filtros ativos exibidos como chips removíveis

### 4.6 Contratos de Comportamento

**Multi-Tenancy:**
- Apenas logs do tenant atual são exibidos
- TenantId não é exibido (implícito no contexto)

**Mascaramento Automático (RN-LOG-004):**
- CPF exibido como `***.***.*89-**`
- Senhas exibidas como `***`
- Cartões exibidos como `**** **** **** 1111`

**Correlation IDs (RN-LOG-003):**
- CorrelationId é clicável
- Ao clicar, navega para WF-02 (UC01) com filtro automático por aquele CorrelationId

**Ordenação:**
- Padrão: Timestamp DESC (mais recente primeiro)
- Clicar em cabeçalho alterna ASC/DESC

**Responsividade:**
- **Mobile:** Lista empilhada (cards) - campos: Timestamp, Level, Message truncada
- **Tablet:** Tabela simplificada (4 colunas) - oculta UserId
- **Desktop:** Tabela completa (5 colunas)

**Acessibilidade (WCAG AA):**
- Labels em português claro
- Botões com aria-label ("Buscar logs", "Exportar logs")
- Navegação por teclado (Tab, Enter)
- Contraste mínimo 4.5:1 (badges de nível)

---

## 5. WF-02 — BUSCA AVANÇADA DE LOGS (UC01)

### 5.1 Intenção da Tela
Permitir **busca avançada com múltiplos filtros** (CorrelationId, UserId, IP, text search) para rastreamento detalhado de logs.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo CorrelationId | Input | GUID para rastreamento end-to-end |
| CMP-WF02-002 | Campo UserId | Input | Email do usuário |
| CMP-WF02-003 | Campo IP | Input | Endereço IP (ex: 192.168.1.100) |
| CMP-WF02-004 | Campo Text Search | Input | Busca full-text ou regex |
| CMP-WF02-005 | Filtro de Nível | MultiSelect | Verbose, Debug, Info, Warning, Error, Fatal |
| CMP-WF02-006 | Filtro de Período | DateRangePicker | Data/hora início e fim |
| CMP-WF02-007 | Botão Buscar | Button | Ação primária para executar busca |
| CMP-WF02-008 | Botão Limpar | Button | Limpar todos os filtros |
| CMP-WF02-009 | Tabela de Resultados | DataTable | Mesma estrutura do WF-01 |
| CMP-WF02-010 | Indicador Loading | Spinner | Exibido durante busca |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Buscar | Usuário clica em CMP-WF02-007 | UC01 | FP-UC01-005 |
| EVT-WF02-002 | Limpar | Usuário clica em CMP-WF02-008 | UC01 | FA-UC01-001 |
| EVT-WF02-003 | Busca por CorrelationId | Usuário preenche CMP-WF02-001 e busca | UC01 | FA-UC01-01 |
| EVT-WF02-004 | Busca por UserId | Usuário preenche CMP-WF02-002 e busca | UC01 | FA-UC01-02 |
| EVT-WF02-005 | Busca por IP | Usuário preenche CMP-WF02-003 e busca | UC01 | FA-UC01-03 |
| EVT-WF02-006 | Text Search | Usuário preenche CMP-WF02-004 e busca | UC01 | FA-UC01-04 |
| EVT-WF02-007 | Clique em resultado | Usuário clica em linha da tabela CMP-WF02-009 | UC02 | FP-UC02-001 |

### 5.4 Ações Permitidas
- Preencher critérios de busca (múltiplos filtros acumuláveis)
- Executar busca avançada
- Visualizar resultados paginados
- Limpar filtros
- Navegar para detalhes de log (UC02)
- Exportar resultados (UC03)

### 5.5 Estados Obrigatórios

#### Estado 1: Loading (Buscando)
**Quando:** Sistema está executando query complexa em Seq/Elasticsearch

**Exibir:**
- CMP-WF02-010: Spinner
- Mensagem: "Buscando logs..."
- Desabilitar CMP-WF02-007 (botão Buscar)

#### Estado 2: Vazio (Nenhum Resultado)
**Quando:** Busca não retornou logs

**Exibir:**
- Ícone ilustrativo (lupa)
- Mensagem: "Nenhum log encontrado com os critérios informados."
- Sugestão: "Tente ajustar os filtros ou expandir o período."

#### Estado 3: Erro (Falha na Busca)
**Quando:** API retorna erro (403, 500) ou usuário sem permissão SYS.LOGS.SEARCH

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado. Permissão SYS.LOGS.SEARCH necessária."
  - Se 500: "Erro ao buscar logs. Tente novamente."
- Botão "Tentar Novamente"

#### Estado 4: Dados (Resultados Exibidos)
**Quando:** Busca retornou logs

**Exibir:**
- CMP-WF02-009: Tabela com resultados (mesma estrutura do WF-01)
- Indicador: "X logs encontrados" (acima da tabela)
- Filtros ativos exibidos como chips
- Paginação (100 por página)

### 5.6 Contratos de Comportamento

**Busca por CorrelationId (RN-LOG-003):**
- Se CMP-WF02-001 preenchido, busca TODOS os logs relacionados (frontend → API → banco → fila → job)
- Resultados ordenados por Timestamp ASC (sequência cronológica do request)
- Destacar span principal (origem do request)

**Busca Text Search:**
- Executa busca full-text em campo `Message`
- Suporta regex básico (ex: `FK constraint violation`)
- Case-insensitive por padrão

**Acumulação de Filtros:**
- Filtros são AND (ex: UserId=admin@test.com AND Level=Error)
- Múltiplos níveis selecionados são OR (ex: Error OR Fatal)

**Mascaramento (RN-LOG-004):**
- Aplicado automaticamente mesmo em resultados de busca

**Responsividade:**
- **Mobile:** Formulário empilhado, campos full-width
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 3 colunas

**Acessibilidade:**
- Labels descritivos ("Buscar por Correlation ID", "Buscar por Usuário")
- Campos com placeholder explicativo
- Navegação por teclado (Tab, Enter para buscar, Esc para limpar)

---

## 6. WF-03 — DETALHES DE LOG (UC02)

### 6.1 Intenção da Tela
Permitir **visualização completa e detalhada de um log** com stack trace, navegação por CorrelationId e informações de auditoria.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Card de Log | Card | Container principal com dados do log |
| CMP-WF03-002 | Badge de Nível | Badge | Visual colorido (Error, Warning, Info) |
| CMP-WF03-003 | Timestamp | Text | Data/hora completa (ISO 8601) |
| CMP-WF03-004 | Message | Text | Mensagem completa (mascarada - RN-LOG-004) |
| CMP-WF03-005 | CorrelationId | Link | GUID clicável (navega para logs relacionados) |
| CMP-WF03-006 | UserId | Text | Email do usuário autenticado |
| CMP-WF03-007 | TenantId | Text | ID do tenant (contexto) |
| CMP-WF03-008 | IP | Text | Endereço IP de origem |
| CMP-WF03-009 | UserAgent | Text | Navegador/dispositivo |
| CMP-WF03-010 | Exception | ExpandableText | Mensagem de exceção (se houver) |
| CMP-WF03-011 | StackTrace | ExpandableCodeBlock | Stack trace formatado com highlight |
| CMP-WF03-012 | Botão "Ver Logs Relacionados" | Button | Navega para WF-02 com filtro CorrelationId |
| CMP-WF03-013 | Botão Voltar | Button | Retorna para WF-01 ou WF-02 |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Expandir Stack Trace | Usuário clica em CMP-WF03-011 | UC02 | FA-UC02-01 |
| EVT-WF03-002 | Navegar para logs relacionados | Usuário clica em CMP-WF03-005 ou CMP-WF03-012 | UC01 | FA-UC02-02 |
| EVT-WF03-003 | Voltar | Usuário clica em CMP-WF03-013 | UC00/UC01 | - |

### 6.4 Ações Permitidas
- Visualizar todos os campos do log
- Expandir/colapsar stack trace
- Copiar stack trace para clipboard
- Navegar para logs relacionados (mesmo CorrelationId)
- Voltar para listagem

### 6.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando Detalhes)
**Quando:** Sistema está buscando log completo

**Exibir:**
- Skeleton loader no card
- Mensagem: "Carregando detalhes do log..."

#### Estado 2: Vazio (Log Não Disponível)
**Quando:** Log foi purgado conforme política de retenção (RN-LOG-008)

**Exibir:**
- Ícone de documento riscado
- Mensagem: "Log não disponível. Purgado conforme política de retenção (90d/1y/7y)."
- Explicação: "Logs Info/Debug: 90 dias | Warning/Error: 1 ano | Auditoria: 7 anos"
- Botão "Voltar"

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (403, 404, 500) ou usuário sem permissão

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado."
  - Se 404: "Log não encontrado."
  - Se 500: "Erro ao carregar log. Tente novamente."
- Botão "Voltar"

#### Estado 4: Dados (Log Exibido)
**Quando:** Log disponível e carregado

**Exibir:**
- CMP-WF03-001: Card com todos os campos
- CMP-WF03-002: Badge de nível (colorido)
- CMP-WF03-003 a CMP-WF03-009: Dados estruturados
- CMP-WF03-010: Exception (se existir)
- CMP-WF03-011: StackTrace (se existir, colapsado por padrão)
- CMP-WF03-012: Botão "Ver Logs Relacionados" (se CorrelationId não nulo)

**Layout:**
```
┌─────────────────────────────────────────┐
│ [Badge Level] Timestamp                 │
│─────────────────────────────────────────│
│ Message: [texto mascarado]              │
│                                         │
│ Correlation ID: [GUID clicável]         │
│ User ID: admin@test.com                 │
│ Tenant ID: tenant-123                   │
│ IP: 192.168.1.100                       │
│ User Agent: Mozilla/5.0...              │
│─────────────────────────────────────────│
│ Exception: [mensagem de erro]           │
│ ▼ Stack Trace (clique para expandir)    │
│─────────────────────────────────────────│
│ [Botão Ver Logs Relacionados] [Voltar]  │
└─────────────────────────────────────────┘
```

### 6.6 Contratos de Comportamento

**Mascaramento (RN-LOG-004):**
- Aplicado em CMP-WF03-004 (Message)
- Aplicado em CMP-WF03-010 (Exception.Message)

**CorrelationId Clicável (RN-LOG-003):**
- CMP-WF03-005: Link clicável
- Ao clicar, navega para WF-02 com filtro `CorrelationId=[GUID]`
- CMP-WF03-012: Botão alternativo para mesma ação

**Stack Trace Expandível:**
- CMP-WF03-011: Colapsado por padrão
- Ao expandir, exibe stack trace formatado com syntax highlight
- Destaca arquivo:linha de código relevante (primeira linha do stack)
- Botão "Copiar Stack Trace" (clipboard)

**Navegação Contextual:**
- Breadcrumb: "Logs > [Timestamp] > Detalhes"
- Botão Voltar retorna para tela anterior (WF-01 ou WF-02)

**Responsividade:**
- **Mobile:** Card full-width, campos empilhados
- **Tablet:** Card 80% width, campos em 2 colunas
- **Desktop:** Card 60% width centralizado

**Acessibilidade:**
- Labels descritivos ("Identificador de Correlação", "Usuário")
- CorrelationId com aria-label "Navegar para logs relacionados"
- Stack trace com aria-expanded (true/false)

---

## 7. WF-04 — EXPORTAÇÃO DE LOGS (UC03)

### 7.1 Intenção da Tela
Permitir **exportação de logs em CSV ou JSON** para compliance (LGPD, SOX, ISO 27001) com mascaramento automático.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Modal de Exportação | Modal | Container principal |
| CMP-WF04-002 | Radio CSV | Radio | Formato CSV |
| CMP-WF04-003 | Radio JSON | Radio | Formato JSON |
| CMP-WF04-004 | Indicador de Registros | Text | "X logs serão exportados" |
| CMP-WF04-005 | Aviso de Limite | Alert | "Limite: 10.000 logs" |
| CMP-WF04-006 | Botão Exportar | Button | Ação primária para gerar arquivo |
| CMP-WF04-007 | Botão Cancelar | Button | Fechar modal |
| CMP-WF04-008 | Indicador Loading | Spinner | Exibido durante geração |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Selecionar CSV | Usuário seleciona CMP-WF04-002 | UC03 | FA-UC03-01 |
| EVT-WF04-002 | Selecionar JSON | Usuário seleciona CMP-WF04-003 | UC03 | FA-UC03-02 |
| EVT-WF04-003 | Exportar | Usuário clica em CMP-WF04-006 | UC03 | FP-UC03-006 |
| EVT-WF04-004 | Cancelar | Usuário clica em CMP-WF04-007 | - | - |

### 7.4 Ações Permitidas
- Selecionar formato de exportação (CSV ou JSON)
- Confirmar exportação
- Cancelar exportação
- Download automático do arquivo gerado

### 7.5 Estados Obrigatórios

#### Estado 1: Loading (Gerando Arquivo)
**Quando:** Sistema está gerando arquivo de exportação

**Exibir:**
- CMP-WF04-008: Spinner
- Mensagem: "Gerando arquivo de exportação..."
- Desabilitar CMP-WF04-006 (botão Exportar)

#### Estado 2: Vazio (Nenhum Log para Exportar)
**Quando:** Filtros atuais não retornaram logs

**Exibir:**
- Mensagem: "Nenhum log disponível para exportação."
- Sugestão: "Ajuste os filtros para incluir logs."
- Apenas botão Cancelar habilitado

#### Estado 3: Erro (Bloqueio por Limite)
**Quando:** Busca retornou > 10.000 logs

**Exibir:**
- CMP-WF04-005: Alert vermelho
- Mensagem: "Exportação limitada a 10.000 logs. Refine os filtros."
- Indicador: "X logs selecionados (máximo permitido: 10.000)"
- CMP-WF04-006: Botão Exportar DESABILITADO

#### Estado 4: Erro (Sem Permissão)
**Quando:** Usuário sem permissão SYS.LOGS.EXPORT

**Exibir:**
- Ícone de erro (🔒)
- Mensagem: "Acesso negado. Permissão SYS.LOGS.EXPORT necessária."
- Apenas botão Cancelar habilitado

#### Estado 5: Dados (Pronto para Exportar)
**Quando:** Há logs disponíveis (≤ 10.000) e usuário tem permissão

**Exibir:**
- CMP-WF04-004: "X logs serão exportados" (1 ≤ X ≤ 10.000)
- CMP-WF04-002 e CMP-WF04-003: Radios habilitados (padrão: CSV)
- CMP-WF04-006: Botão Exportar HABILITADO

### 7.6 Contratos de Comportamento

**Limite de Exportação:**
- Máximo: 10.000 logs por exportação
- Se > 10.000, bloquear exportação com mensagem explicativa

**Formato CSV (FA-UC03-01):**
- Colunas: `Timestamp, Level, Message, CorrelationId, UserId`
- Separador: `,` (vírgula)
- Encoding: UTF-8 with BOM
- Nome do arquivo: `logs_export_YYYYMMDD_HHMMSS.csv`
- Exemplo:
  ```csv
  Timestamp,Level,Message,CorrelationId,UserId
  2026-01-04T14:30:15Z,Error,"FK constraint violation (mascarado)",a1b2c3d4-e5f6,admin@test.com
  ```

**Formato JSON (FA-UC03-02):**
- Array de objetos JSON
- Campos: `timestamp`, `level`, `message`, `correlationId`, `userId`, `tenantId`, `ip`
- Indentação: 2 espaços
- Nome do arquivo: `logs_export_YYYYMMDD_HHMMSS.json`
- Exemplo:
  ```json
  [
    {
      "timestamp": "2026-01-04T14:30:15Z",
      "level": "Error",
      "message": "FK constraint violation (mascarado)",
      "correlationId": "a1b2c3d4-e5f6",
      "userId": "admin@test.com",
      "tenantId": "tenant-123",
      "ip": "192.168.1.100"
    }
  ]
  ```

**Mascaramento (RN-LOG-004):**
- Aplicado ANTES de gerar arquivo
- CPF, senhas, cartões mascarados em ambos os formatos

**Auditoria:**
- Exportação deve ser registrada em log de auditoria (retenção 7 anos - SOX)
- Campos auditados: UserId, TenantId, Formato, Quantidade de Logs, Timestamp

**Download Automático:**
- Após geração, iniciar download automaticamente
- Exibir toast de sucesso: "Arquivo exportado com sucesso. Download iniciado."

**Responsividade:**
- **Mobile:** Modal full-screen
- **Tablet:** Modal 70% width
- **Desktop:** Modal 50% width centralizado

**Acessibilidade:**
- Radio buttons com labels descritivos ("Exportar em CSV", "Exportar em JSON")
- Mensagens de erro em alto contraste
- Navegação por teclado (Tab, Space para selecionar, Enter para exportar, Esc para cancelar)

---

## 8. WF-05 — CONFIGURAÇÃO DE ALERTAS (UC04)

### 8.1 Intenção da Tela
Permitir **configuração de alertas proativos** (error rate, latência P95, dependência offline) com thresholds personalizáveis.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Campo Nome do Alerta | Input | Nome descritivo do alerta |
| CMP-WF05-002 | Dropdown Tipo | Dropdown | ErrorRate, LatencyP95, DependenciaOffline, Disco, Memoria |
| CMP-WF05-003 | Campo Threshold | Input | Valor do threshold (ex: 5% para ErrorRate) |
| CMP-WF05-004 | Dropdown Período | Dropdown | 1min, 5min, 15min, 30min, 1h |
| CMP-WF05-005 | Campo Dependência | Dropdown | BancoDeDados, Cache, FilaMensagens, APIExterna (se tipo = DependenciaOffline) |
| CMP-WF05-006 | Toggle Notificação PagerDuty | Toggle | Habilitar/desabilitar integração |
| CMP-WF05-007 | Botão Salvar | Button | Ação primária para salvar alerta |
| CMP-WF05-008 | Botão Cancelar | Button | Cancelar configuração |
| CMP-WF05-009 | Tabela de Alertas | DataTable | Lista de alertas configurados (Nome, Tipo, Threshold, Status) |
| CMP-WF05-010 | Botão Editar Alerta | IconButton | Editar alerta existente |
| CMP-WF05-011 | Botão Excluir Alerta | IconButton | Excluir alerta |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Selecionar Tipo | Usuário seleciona em CMP-WF05-002 | UC04 | FP-UC04-004 |
| EVT-WF05-002 | Salvar Alerta | Usuário clica em CMP-WF05-007 | UC04 | FP-UC04-007 |
| EVT-WF05-003 | Cancelar | Usuário clica em CMP-WF05-008 | - | - |
| EVT-WF05-004 | Editar Alerta | Usuário clica em CMP-WF05-010 | UC04 | FA-UC04-01 |
| EVT-WF05-005 | Excluir Alerta | Usuário clica em CMP-WF05-011 | UC04 | FE-UC04-02 |

### 8.4 Ações Permitidas
- Criar novo alerta
- Configurar tipo de alerta (ErrorRate, LatencyP95, DependenciaOffline, Disco, Memoria)
- Definir threshold e período
- Habilitar/desabilitar notificação PagerDuty
- Editar alerta existente
- Excluir alerta
- Visualizar lista de alertas configurados

### 8.5 Estados Obrigatórios

#### Estado 1: Loading (Salvando Alerta)
**Quando:** Sistema está salvando configuração de alerta

**Exibir:**
- Spinner no botão CMP-WF05-007
- Mensagem: "Salvando alerta..."
- Desabilitar CMP-WF05-007

#### Estado 2: Vazio (Nenhum Alerta Configurado)
**Quando:** Não há alertas criados

**Exibir:**
- Ícone ilustrativo (sino)
- Mensagem: "Nenhum alerta configurado."
- Sugestão: "Configure alertas proativos para monitorar a saúde do sistema."
- Botão "Criar Primeiro Alerta"

#### Estado 3: Erro (Validação Falhou)
**Quando:** Threshold inválido (ex: ErrorRate > 100%)

**Exibir:**
- Alert vermelho abaixo do campo CMP-WF05-003
- Mensagem específica:
  - Se ErrorRate > 100%: "Threshold inválido. ErrorRate deve estar entre 0% e 100%."
  - Se LatencyP95 < 0: "Threshold inválido. Latência deve ser positiva (em ms)."
- CMP-WF05-003: Borda vermelha no campo com erro

#### Estado 4: Erro (Sem Permissão)
**Quando:** Usuário sem permissão SYS.ALERTS.UPDATE

**Exibir:**
- Ícone de erro (🔒)
- Mensagem: "Acesso negado. Permissão SYS.ALERTS.UPDATE necessária."
- CMP-WF05-007: Botão Salvar DESABILITADO
- CMP-WF05-009: Tabela em modo somente leitura

#### Estado 5: Dados (Formulário Ativo)
**Quando:** Usuário tem permissão e pode configurar alerta

**Exibir:**
- Formulário completo habilitado
- CMP-WF05-009: Tabela com alertas existentes (se houver)
- Cada alerta na tabela exibe: Nome, Tipo, Threshold, Período, Status (Ativo/Inativo)

### 8.6 Contratos de Comportamento

**Tipos de Alerta (RN-LOG-011):**

1. **ErrorRate:**
   - CMP-WF05-003: Placeholder "5%" (threshold sugerido)
   - Validação: 0% ≤ threshold ≤ 100%
   - Descrição: "Disparar se error rate > X% nos últimos Y minutos"

2. **LatencyP95:**
   - CMP-WF05-003: Placeholder "3000ms" (threshold sugerido)
   - Validação: threshold > 0
   - Descrição: "Disparar se latência P95 > X ms nos últimos Y minutos"

3. **DependenciaOffline:**
   - CMP-WF05-005: Exibido APENAS se tipo = DependenciaOffline
   - Opções: BancoDeDados, Cache, FilaMensagens, APIExterna
   - Descrição: "Disparar se dependência [X] falhar health check"

4. **Disco:**
   - CMP-WF05-003: Placeholder "85%" (threshold sugerido)
   - Validação: 0% ≤ threshold ≤ 100%
   - Descrição: "Disparar se uso de disco > X%"

5. **Memoria:**
   - CMP-WF05-003: Placeholder "90%" (threshold sugerido)
   - Validação: 0% ≤ threshold ≤ 100%
   - Descrição: "Disparar se uso de memória > X%"

**Integração PagerDuty:**
- CMP-WF05-006: Toggle (padrão: habilitado)
- Se habilitado, notificações são enviadas via PagerDuty/Opsgenie para equipe 24/7
- Se desabilitado, alertas apenas aparecem na UI

**Validação de Threshold:**
- Executada ao submeter formulário (CMP-WF05-007)
- Se inválido, exibir erro específico e bloquear salvamento

**Tabela de Alertas (CMP-WF05-009):**
- Colunas: Nome, Tipo, Threshold, Período, Status, Ações
- Status: Badge verde (Ativo) ou cinza (Inativo)
- Ações: Editar (ícone lápis) e Excluir (ícone lixeira)

**Edição de Alerta:**
- Ao clicar em CMP-WF05-010, preencher formulário com dados do alerta
- Botão "Salvar" vira "Atualizar"

**Exclusão de Alerta:**
- Ao clicar em CMP-WF05-011, exibir confirmação: "Excluir alerta [Nome]? Esta ação não pode ser desfeita."
- Se confirmado, excluir e atualizar tabela

**Responsividade:**
- **Mobile:** Formulário empilhado, tabela com scroll horizontal
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 3 colunas

**Acessibilidade:**
- Labels descritivos ("Nome do Alerta", "Tipo de Métrica", "Valor do Threshold")
- Mensagens de erro em alto contraste
- Toggle com aria-label "Habilitar notificação PagerDuty"
- Navegação por teclado completa

---

## 9. WF-06 — DASHBOARDS DE MÉTRICAS (UC05)

### 9.1 Intenção da Tela
Permitir **visualização de métricas RED** (Rate, Errors, Duration) em dashboards visuais para monitoramento de performance.

### 9.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF06-001 | Tab Rate | Tab | Dashboard de Rate (requests/segundo) |
| CMP-WF06-002 | Tab Errors | Tab | Dashboard de Errors (% de erros) |
| CMP-WF06-003 | Tab Duration | Tab | Dashboard de Duration (P50/P95/P99) |
| CMP-WF06-004 | Gráfico de Linha | LineChart | Métrica ao longo do tempo (últimas 24h) |
| CMP-WF06-005 | Indicador Atual | StatCard | Valor atual da métrica |
| CMP-WF06-006 | Indicador Média | StatCard | Média das últimas 24h |
| CMP-WF06-007 | Indicador Pico | StatCard | Valor máximo das últimas 24h |
| CMP-WF06-008 | Linha de Threshold | Overlay | Linha vermelha indicando threshold de alerta |
| CMP-WF06-009 | Filtro de Período | Dropdown | Últimas 24h, Última semana, Último mês |
| CMP-WF06-010 | Botão Atualizar | IconButton | Força atualização dos dados |
| CMP-WF06-011 | Indicador Auto-Refresh | Text | "Atualização automática a cada 1min" |

### 9.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF06-001 | Trocar Tab Rate | Usuário clica em CMP-WF06-001 | UC05 | FA-UC05-01 |
| EVT-WF06-002 | Trocar Tab Errors | Usuário clica em CMP-WF06-002 | UC05 | FA-UC05-02 |
| EVT-WF06-003 | Trocar Tab Duration | Usuário clica em CMP-WF06-003 | UC05 | FA-UC05-03 |
| EVT-WF06-004 | Alterar Período | Usuário seleciona em CMP-WF06-009 | UC05 | FP-UC05-003 |
| EVT-WF06-005 | Atualizar Dados | Usuário clica em CMP-WF06-010 | UC05 | FP-UC05-004 |
| EVT-WF06-006 | Auto-Refresh | Timer de 1min dispara | UC05 | FP-UC05-004 |

### 9.4 Ações Permitidas
- Alternar entre dashboards (Rate, Errors, Duration)
- Filtrar por período (24h, semana, mês)
- Atualizar dados manualmente
- Visualizar auto-refresh em tempo real
- Identificar picos e vales nas métricas

### 9.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando Métricas)
**Quando:** Sistema está buscando dados de métricas (Prometheus/Application Insights)

**Exibir:**
- Skeleton loader nos gráficos e stat cards
- Mensagem: "Carregando métricas..."

#### Estado 2: Vazio (Sem Dados de Métricas)
**Quando:** Endpoint /metrics não está retornando dados

**Exibir:**
- Ícone ilustrativo (gráfico vazio)
- Mensagem: "Nenhuma métrica disponível."
- Sugestão: "Verifique se o endpoint /metrics está configurado corretamente."

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (403, 500) ou usuário sem permissão SYS.METRICS.READ

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado. Permissão SYS.METRICS.READ necessária."
  - Se 500: "Erro ao carregar métricas. Tente novamente."
- Botão "Recarregar"

#### Estado 4: Dados (Dashboards Exibidos)
**Quando:** Métricas disponíveis e carregadas

**Exibir:**
- CMP-WF06-001/002/003: Tabs habilitadas (padrão: Rate)
- CMP-WF06-004: Gráfico de linha com dados históricos
- CMP-WF06-005/006/007: Stat cards com valores atuais
- CMP-WF06-008: Linha de threshold (se alerta configurado)
- CMP-WF06-011: Indicador de auto-refresh

### 9.6 Contratos de Comportamento

**Dashboard Rate (RN-LOG-009):**
- **Métrica:** Requests/segundo (req/s)
- **Gráfico (CMP-WF06-004):** Linha azul com requests/s ao longo do tempo
- **Stat Cards:**
  - CMP-WF06-005: "120 req/s" (atual)
  - CMP-WF06-006: "95 req/s" (média 24h)
  - CMP-WF06-007: "250 req/s" (pico 24h)
- **Threshold:** Linha vermelha em 200 req/s (se configurado)
- **Descrição:** "Quantidade de requests processados por segundo"

**Dashboard Errors (RN-LOG-009):**
- **Métrica:** Error Rate (%)
- **Gráfico (CMP-WF06-004):** Linha vermelha com % de erros ao longo do tempo
- **Stat Cards:**
  - CMP-WF06-005: "3.2%" (atual)
  - CMP-WF06-006: "2.1%" (média 24h)
  - CMP-WF06-007: "8.5%" (pico 24h)
- **Threshold:** Linha vermelha em 5% (RN-LOG-011)
- **Descrição:** "Porcentagem de requests que resultaram em erro (HTTP 4xx/5xx)"
- **Destaque:** Se error rate > 5%, exibir alert: "Error rate acima do threshold! Verifique os logs."

**Dashboard Duration (RN-LOG-009):**
- **Métrica:** Latência (ms) - P50, P95, P99
- **Gráfico (CMP-WF06-004):** 3 linhas sobrepostas:
  - Linha verde: P50 (mediana)
  - Linha amarela: P95 (percentil 95)
  - Linha vermelha: P99 (percentil 99)
- **Stat Cards:**
  - CMP-WF06-005: "P50: 120ms | P95: 850ms | P99: 2500ms" (atual)
  - CMP-WF06-006: "P50: 100ms | P95: 700ms | P99: 2000ms" (média 24h)
  - CMP-WF06-007: "P50: 150ms | P95: 1200ms | P99: 3500ms" (pico 24h)
- **Threshold:** Linha vermelha em 3000ms (RN-LOG-011)
- **Descrição:** "Tempo de resposta dos requests (P50=mediana, P95=95% dos requests, P99=99% dos requests)"
- **Destaque:** Se P95 > 3s, exibir alert: "Latência P95 acima do threshold! Sistema lento."

**Auto-Refresh:**
- CMP-WF06-011: "Atualização automática a cada 1min"
- Timer de 1min para recarregar métricas automaticamente
- Indicador visual durante refresh (spinner pequeno no botão CMP-WF06-010)

**Filtro de Período (CMP-WF06-009):**
- Opções: Últimas 24h (padrão), Última semana, Último mês
- Ao alterar, recarregar gráfico e stat cards

**Responsividade:**
- **Mobile:** Tabs empilhadas, gráfico full-width, stat cards em coluna
- **Tablet:** Tabs horizontais, gráfico 80% width, stat cards em linha
- **Desktop:** Layout completo, gráfico 100% width, stat cards em linha

**Acessibilidade:**
- Tabs com aria-label ("Dashboard de Taxa de Requests", "Dashboard de Erros", "Dashboard de Latência")
- Gráficos com descrição textual alternativa (para screen readers)
- Contraste mínimo 4.5:1 em todas as cores

---

## 10. WF-07 — HEALTH CHECKS (UC06)

### 10.1 Intenção da Tela
Permitir **verificação de saúde do sistema** validando dependências críticas (banco, cache, filas, APIs externas).

### 10.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF07-001 | Card de Status Geral | Card | Indicador global: Healthy (verde) ou Unhealthy (vermelho) |
| CMP-WF07-002 | Tabela de Dependências | DataTable | Lista de dependências com status individual |
| CMP-WF07-003 | Badge Status | Badge | Verde (Healthy) ou Vermelho (Unhealthy) |
| CMP-WF07-004 | Indicador Response Time | Text | Tempo de resposta do health check (ms) |
| CMP-WF07-005 | Mensagem de Erro | Text | Mensagem de erro se dependência offline |
| CMP-WF07-006 | Botão Verificar Novamente | Button | Força nova execução de health checks |
| CMP-WF07-007 | Indicador Auto-Refresh | Text | "Atualização automática a cada 30s" |
| CMP-WF07-008 | Timestamp Última Verificação | Text | Data/hora da última execução |

### 10.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF07-001 | Verificar Novamente | Usuário clica em CMP-WF07-006 | UC06 | FP-UC06-003 |
| EVT-WF07-002 | Auto-Refresh | Timer de 30s dispara | UC06 | FP-UC06-003 |
| EVT-WF07-003 | Clique em Dependência | Usuário clica em linha da tabela | UC06 | FA-UC06-01 |

### 10.4 Ações Permitidas
- Visualizar status geral do sistema (Healthy/Unhealthy)
- Verificar status individual de cada dependência
- Forçar nova verificação manual
- Visualizar tempo de resposta de cada dependência
- Visualizar mensagem de erro se dependência offline

### 10.5 Estados Obrigatórios

#### Estado 1: Loading (Executando Health Checks)
**Quando:** Sistema está executando verificações (SELECT 1 no banco, PING no cache, etc.)

**Exibir:**
- CMP-WF07-001: Spinner
- Mensagem: "Verificando saúde do sistema..."
- CMP-WF07-006: Botão desabilitado

#### Estado 2: Vazio (Nenhuma Dependência Configurada)
**Quando:** Não há dependências críticas configuradas

**Exibir:**
- Ícone ilustrativo (stethoscope)
- Mensagem: "Nenhuma dependência crítica configurada."
- Sugestão: "Configure health checks para monitorar banco de dados, cache e APIs externas."

#### Estado 3: Erro (Falha Geral)
**Quando:** API retorna erro (403, 500) ou usuário sem permissão SYS.HEALTH.READ

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado. Permissão SYS.HEALTH.READ necessária."
  - Se 500: "Erro ao executar health checks. Tente novamente."
- Botão "Tentar Novamente"

#### Estado 4: Dados (Sistema Saudável - Todas Dependências Online)
**Quando:** Todas as dependências retornaram HTTP 200

**Exibir:**
- CMP-WF07-001: Card verde com ícone ✓
- Mensagem: "Sistema Saudável"
- CMP-WF07-002: Tabela com todas as dependências em verde
- CMP-WF07-008: "Última verificação: 2026-01-04T14:30:15Z"

**Layout do Card:**
```
┌───────────────────────────────────┐
│ ✓ Sistema Saudável                │
│                                   │
│ Todas as dependências online      │
│ Última verificação: há 10s        │
└───────────────────────────────────┘
```

#### Estado 5: Dados (Sistema Não Saudável - Dependência Offline)
**Quando:** Pelo menos uma dependência retornou erro (timeout, 503)

**Exibir:**
- CMP-WF07-001: Card vermelho com ícone ⚠️
- Mensagem: "Sistema Não Saudável - X dependência(s) offline"
- CMP-WF07-002: Tabela com dependências offline em vermelho
- Alert crítico: "Alerta automático disparado (PagerDuty) - RN-LOG-011"
- CMP-WF07-008: "Última verificação: 2026-01-04T14:30:15Z"

**Layout do Card:**
```
┌────────────────────────────────────┐
│ ⚠️ Sistema Não Saudável            │
│                                    │
│ 1 dependência offline              │
│ Banco de Dados: offline (timeout)  │
│ Alerta disparado (PagerDuty)       │
│ Última verificação: há 10s         │
└────────────────────────────────────┘
```

### 10.6 Contratos de Comportamento

**Tabela de Dependências (CMP-WF07-002):**
- Colunas: Dependência, Status, Response Time, Mensagem
- Dependências críticas (RN-LOG-010):
  - **Banco de Dados** (SELECT 1)
  - **Cache** (PING)
  - **Fila de Mensagens** (GET /healthcheck)
  - **API Externa** (GET /health ou similar)

**Status por Dependência:**
- **Healthy (HTTP 200):**
  - CMP-WF07-003: Badge verde "Online"
  - CMP-WF07-004: "12ms"
  - CMP-WF07-005: "-"

- **Unhealthy (Timeout, 503, 500):**
  - CMP-WF07-003: Badge vermelho "Offline"
  - CMP-WF07-004: "timeout (30s)" ou "N/A"
  - CMP-WF07-005: Mensagem de erro específica:
    - Banco: "Connection timeout - verifique conectividade"
    - Cache: "Redis não responde - verifique serviço"
    - Fila: "RabbitMQ offline - verifique cluster"
    - API: "API Externa retornou 503"

**Alerta Automático (RN-LOG-011):**
- Se qualquer dependência crítica ficar offline:
  - Disparar alerta para PagerDuty/Opsgenie
  - Exibir mensagem na UI: "Alerta disparado (PagerDuty)"
  - Registrar evento em log de auditoria

**Auto-Refresh:**
- CMP-WF07-007: "Atualização automática a cada 30s"
- Timer de 30s para reexecutar health checks
- Indicador visual durante refresh (spinner no botão CMP-WF07-006)

**Endpoint /health (RN-LOG-010):**
- Retorna HTTP 200 se todas dependências online
- Retorna HTTP 503 se pelo menos uma dependência offline
- Usado por Kubernetes liveness/readiness probes e load balancers

**Responsividade:**
- **Mobile:** Card full-width, tabela com scroll horizontal
- **Tablet:** Card 80% width, tabela simplificada
- **Desktop:** Card 60% width centralizado, tabela completa

**Acessibilidade:**
- Badges com aria-label ("Status: Online", "Status: Offline")
- Mensagens de erro em alto contraste
- Navegação por teclado (Tab, Enter para verificar novamente)

---

## 11. WF-08 — TRACING DISTRIBUÍDO (UC07)

### 11.1 Intenção da Tela
Permitir **rastreamento end-to-end de requests** através de múltiplos serviços (frontend → API → banco → fila → job) usando OpenTelemetry.

### 11.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF08-001 | Campo TraceId | Input | GUID do trace (ex: a1b2c3d4-e5f6-7890-abcd-ef1234567890) |
| CMP-WF08-002 | Botão Buscar | Button | Executar busca de spans |
| CMP-WF08-003 | Timeline de Spans | Timeline | Visualização cronológica de spans |
| CMP-WF08-004 | Card de Span | Card | Detalhes de um span individual |
| CMP-WF08-005 | Indicador de Duração | ProgressBar | Barra visual com duração do span |
| CMP-WF08-006 | Badge de Span Crítico | Badge | Destaque para span mais lento (bottleneck) |
| CMP-WF08-007 | Botão Expandir Span | IconButton | Expandir detalhes do span (query SQL, parâmetros) |
| CMP-WF08-008 | Campo de Busca Rápida | Input | Busca por CorrelationId (redireciona para TraceId) |
| CMP-WF08-009 | Indicador Loading | Spinner | Exibido durante busca |

### 11.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF08-001 | Buscar por TraceId | Usuário preenche CMP-WF08-001 e clica em CMP-WF08-002 | UC07 | FP-UC07-005 |
| EVT-WF08-002 | Buscar por CorrelationId | Usuário preenche CMP-WF08-008 | UC07 | FA-UC07-01 |
| EVT-WF08-003 | Expandir Span | Usuário clica em CMP-WF08-007 | UC07 | FA-UC07-02 |
| EVT-WF08-004 | Clique em Span | Usuário clica em CMP-WF08-004 | UC07 | FA-UC07-02 |

### 11.4 Ações Permitidas
- Informar TraceId para rastrear request completo
- Buscar por CorrelationId (mapeia para TraceId)
- Visualizar timeline de spans (frontend → API → banco → fila → job)
- Identificar span mais lento (bottleneck)
- Expandir detalhes de span (query SQL, parâmetros, headers)
- Visualizar duração de cada span

### 11.5 Estados Obrigatórios

#### Estado 1: Loading (Buscando Spans)
**Quando:** Sistema está buscando spans no Jaeger/Zipkin/Application Insights

**Exibir:**
- CMP-WF08-009: Spinner
- Mensagem: "Buscando spans relacionados..."
- CMP-WF08-002: Botão desabilitado

#### Estado 2: Vazio (Nenhum Span Encontrado)
**Quando:** TraceId não retornou spans

**Exibir:**
- Ícone ilustrativo (lupa)
- Mensagem: "Nenhum span encontrado para o TraceId informado."
- Sugestão: "Verifique se o TraceId está correto ou se o trace ainda está disponível (retenção: 7 dias)."

#### Estado 3: Erro (Falha ao Buscar)
**Quando:** API retorna erro (403, 500) ou usuário sem permissão SYS.LOGS.READ

**Exibir:**
- Ícone de erro (⚠️)
- Mensagem específica:
  - Se 403: "Acesso negado. Permissão SYS.LOGS.READ necessária."
  - Se 500: "Erro ao buscar spans. Tente novamente."
- Botão "Tentar Novamente"

#### Estado 4: Dados (Timeline de Spans Exibida)
**Quando:** TraceId retornou spans

**Exibir:**
- CMP-WF08-003: Timeline visual com todos os spans ordenados por timestamp
- CMP-WF08-004: Cards de span (um por span)
- CMP-WF08-005: Barras de duração proporcionais
- CMP-WF08-006: Badge "Bottleneck" no span mais lento

**Layout da Timeline:**
```
┌────────────────────────────────────────────────┐
│ TraceId: a1b2c3d4-e5f6-7890-abcd-ef1234567890  │
│ Duração Total: 3500ms                          │
│────────────────────────────────────────────────│
│ [Frontend]        ▓▓░░░░░░░░░░░░░░░░  120ms    │
│ [API Gateway]     ░▓▓░░░░░░░░░░░░░░░  80ms     │
│ [API Backend]     ░░▓▓▓▓▓▓░░░░░░░░░░  450ms    │
│ [Database Query]  ░░░░░░▓▓▓▓▓▓▓▓▓▓▓░  2500ms 🔴 BOTTLENECK │
│ [Queue Publish]   ░░░░░░░░░░░░░░░▓▓  150ms    │
│ [Background Job]  ░░░░░░░░░░░░░░░░▓  200ms    │
└────────────────────────────────────────────────┘
```

### 11.6 Contratos de Comportamento

**Rastreamento End-to-End (RN-LOG-012):**
- OpenTelemetry W3C Trace Context implementado
- Propagação de TraceId e SpanId entre serviços
- Spans incluem:
  - **Frontend:** Renderização da tela
  - **API Gateway:** Roteamento do request
  - **API Backend:** Processamento da lógica de negócio
  - **Database:** Execução de query SQL
  - **Queue:** Publicação de mensagem
  - **Background Job:** Processamento assíncrono

**Card de Span (CMP-WF08-004):**
- **Cabeçalho:** Nome do span (ex: "Database Query - SELECT users")
- **Duração:** Tempo total do span (ex: "2500ms")
- **Timestamp:** Data/hora de início (ISO 8601)
- **Detalhes (colapsado por padrão):**
  - Query SQL completa (se span de banco)
  - Parâmetros da query
  - Headers HTTP (se span de API)
  - Status Code (se aplicável)

**Identificação de Bottleneck (FA-UC07-02):**
- CMP-WF08-006: Badge vermelho "BOTTLENECK" no span com maior duração
- Span destacado em vermelho na timeline
- Ao clicar, expandir detalhes automaticamente
- Exibir sugestão: "Este span representa 71% do tempo total. Considere otimização."

**Busca por CorrelationId (RN-LOG-003):**
- CMP-WF08-008: Campo alternativo para busca rápida
- Sistema mapeia CorrelationId → TraceId automaticamente
- Se CorrelationId encontrado, redireciona para timeline com TraceId correspondente

**Duração Proporcional (CMP-WF08-005):**
- Barras de progresso proporcionais à duração total
- Span mais longo = barra mais comprida
- Cores:
  - Verde: < 500ms
  - Amarelo: 500ms - 2000ms
  - Vermelho: > 2000ms (bottleneck)

**Integração com Logs (RN-LOG-003):**
- Cada span tem link para logs relacionados (mesmo CorrelationId)
- Botão "Ver Logs" em cada CMP-WF08-004 (navega para WF-02)

**Responsividade:**
- **Mobile:** Timeline vertical, cards empilhados
- **Tablet:** Timeline horizontal simplificada
- **Desktop:** Timeline horizontal completa

**Acessibilidade:**
- Timeline com descrição textual alternativa (para screen readers)
- Cada span com aria-label descritivo ("Span de Database Query, duração 2500ms, bottleneck")
- Navegação por teclado (Tab, Enter para expandir)
- Contraste mínimo 4.5:1 em badges

---

## 12. NOTIFICAÇÕES

### 12.1 Tipos Padronizados

| Tipo | Uso | Cor | Ícone |
|----|----|-----|-------|
| Sucesso | Operação concluída (ex: "Arquivo exportado com sucesso") | Verde | ✓ |
| Erro | Falha bloqueante (ex: "Acesso negado") | Vermelho | ⚠️ |
| Aviso | Atenção necessária (ex: "Error rate acima do threshold") | Amarelo | ⚠️ |
| Info | Feedback neutro (ex: "Logs atualizados automaticamente") | Azul | ℹ️ |

### 12.2 Posicionamento
- **Desktop:** Toast no canto superior direito
- **Mobile:** Toast no topo da tela (full-width)
- **Duração:** 5 segundos (auto-dismiss) ou botão "Fechar"

---

## 13. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| **Mobile (<768px)** | Layout em coluna, tabelas viram cards, filtros colapsáveis |
| **Tablet (768px-1024px)** | Layout em 2 colunas, tabelas simplificadas (menos colunas) |
| **Desktop (>1024px)** | Layout completo, todas as colunas visíveis |

### Regras Específicas por Tela:
- **WF-01/WF-02:** Tabela → Cards no mobile
- **WF-03:** Card 100% width no mobile
- **WF-04:** Modal full-screen no mobile
- **WF-05:** Formulário empilhado no mobile
- **WF-06:** Gráficos full-width em todos os tamanhos
- **WF-07:** Tabela com scroll horizontal no mobile
- **WF-08:** Timeline vertical no mobile

---

## 14. ACESSIBILIDADE (OBRIGATÓRIO)

### 14.1 Padrões WCAG AA

- **Navegação por teclado:** Tab, Shift+Tab, Enter, Esc
- **Leitura por screen readers:** Todos os componentes com aria-label descritivo
- **Contraste mínimo:** 4.5:1 (texto normal), 3:1 (texto grande)
- **Labels e descrições:** Português claro, sem jargões técnicos

### 14.2 Teclas de Atalho

| Tecla | Ação | Tela |
|-------|------|------|
| / | Foco no campo de busca | WF-01 |
| Ctrl+E | Abrir exportação | WF-01 |
| Ctrl+F | Busca avançada | WF-01 |
| Esc | Fechar modal | WF-04 |
| Enter | Submeter formulário | WF-02, WF-05 |

---

## 15. RASTREABILIDADE

| Wireframe | UC | RF | RNs Aplicadas |
|---------|----|----|---------------|
| WF-01 | UC00 | RF003 | RN-LOG-001, RN-LOG-002, RN-LOG-004, RN-LOG-006 |
| WF-02 | UC01 | RF003 | RN-LOG-001, RN-LOG-003, RN-LOG-004 |
| WF-03 | UC02 | RF003 | RN-LOG-001, RN-LOG-003, RN-LOG-004, RN-LOG-008 |
| WF-04 | UC03 | RF003 | RN-LOG-004, RN-LOG-008 |
| WF-05 | UC04 | RF003 | RN-LOG-011 |
| WF-06 | UC05 | RF003 | RN-LOG-009 |
| WF-07 | UC06 | RF003 | RN-LOG-010, RN-LOG-011 |
| WF-08 | UC07 | RF003 | RN-LOG-012, RN-LOG-003 |

---

## 16. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores específicas, tipografia, espaçamentos)
- Escolha de framework (React, Angular, Vue, Filament)
- Design gráfico definitivo (ilustrações, ícones customizados)
- Animações avançadas (transições complexas, micro-interações)
- Implementação de backend (endpoints, queries, lógica de negócio)
- Integração específica com Seq, Elasticsearch, Prometheus, Grafana, Jaeger
- Configuração de infraestrutura (Kubernetes, Docker, Azure)

---

## 17. OBSERVAÇÕES TÉCNICAS

### 17.1 Particularidades do RF003

**RF003 NÃO é um CRUD tradicional:**
- Logs são eventos append-only (write-only + read-only)
- Não há criação, edição ou exclusão manual de logs
- Wireframes focam em: Listagem, Busca, Visualização, Exportação, Configuração, Dashboards, Health Checks, Tracing

**Mascaramento Automático (RN-LOG-004):**
- CPF: `123.456.789-01` → `***.***.*89-**`
- Senha: `minha_senha_123` → `***`
- Cartão: `1111 2222 3333 4444` → `**** **** **** 4444`
- Aplicado ANTES de exibir na UI e ANTES de exportar

**Correlation IDs (RN-LOG-003):**
- GUID propagado em todos os logs relacionados (frontend → API → banco → fila → job)
- Permite rastreamento end-to-end de requests
- Clicável em todas as telas para navegar para logs relacionados

**Sampling em Produção (RN-LOG-005):**
- Invisível ao usuário (implementação técnica de backend)
- 10% dos requests 2xx logados, 100% dos erros sempre logados
- Wireframes não documentam sampling (não há ação do usuário)

**Circuit Breaker (RN-LOG-007):**
- Invisível ao usuário (mecanismo de resiliência técnica)
- Se sistema de logs centralizado falhar, aplicação degrada graciosamente
- Wireframes não documentam circuit breaker (não há ação do usuário)

### 17.2 Integração com Sistemas Externos

**Seq/Elasticsearch:**
- WF-01 e WF-02 consomem logs via API (GET /api/logs)
- Busca full-text executada em Elasticsearch

**Prometheus:**
- WF-06 consome métricas via endpoint /metrics (Prometheus format)
- Dados históricos armazenados em Prometheus

**Grafana:**
- WF-06 pode ser integrado com Grafana (embed de iframe ou link externo)
- Grafana consome Prometheus para gerar dashboards visuais

**Jaeger/Zipkin:**
- WF-08 consome traces via API Jaeger/Zipkin
- OpenTelemetry exporta traces para Jaeger/Zipkin ou Application Insights

**PagerDuty/Opsgenie:**
- WF-05 configura alertas que disparam notificações via PagerDuty
- Integração via webhook (configurado em backend)

---

## 18. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 1.0 | 2026-01-04 | Agência ALC - alc.dev.br | Criação dos 8 wireframes canônicos do RF003 cobrindo 100% dos 7 UCs |

# UC-RF099 - Casos de Uso - Dashboards e KPIs

**RF Relacionado**: RF-099 - Dashboards e KPIs
**Versão**: 1.0
**Última Atualização**: 2025-12-28
**Responsável**: Equipe de Desenvolvimento IControlIT

---

## UC01: Visualizar Dashboard Executivo/Operacional

### 1. Descrição

Este caso de uso permite que usuários (diretores, gerentes) visualizem dashboards com KPIs estratégicos e operacionais em tempo real, com atualização automática via SignalR e filtros dinâmicos para segmentação de dados.

### 2. Atores

- **Ator Principal**: Diretor / Gerente / Analista
- **Ator Secundário**: Sistema, SignalR Hub

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:{type}:view` (onde type = executive, operational, departmental, personal)
- Multi-tenancy ativo (ClienteId válido)
- Dashboard já criado e configurado
- Mínimo 4 widgets configurados no dashboard

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Dashboards → Seleciona dashboard (Executivo/Operacional) | - |
| 2 | - | Valida permissão `dashboard:{type}:view` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Executa `GET /api/dashboards/{id}/data` |
| 5 | - | Recupera layout do dashboard com 4-12 widgets |
| 6 | - | Para cada widget: calcula KPI usando formula (SUM, AVG, COUNT, MAX, MIN, PERCENTAGE) |
| 7 | - | Aplica filtros base do KPI + filtros dinâmicos do usuário (cliente, filial, período) |
| 8 | - | Retorna valores dos KPIs com meta, variância %, alert level (Green/Yellow/Red) |
| 9 | - | Renderiza widgets: gráficos (timeseries, pizza, barra), scorecards com semáforo, tabelas |
| 10 | - | Estabelece conexão SignalR para atualização em tempo real (30s) |
| 11 | Visualiza dashboard com métricas em tempo real | - |

### 5. Fluxos Alternativos

**FA01: Aplicar Filtros Dinâmicos**
- 11a. Usuário seleciona filtros (período, cliente, filial, centro de custo)
- 11b. Sistema recalcula KPIs com novos filtros
- 11c. Atualiza widgets instantaneamente sem recarregar página
- 11d. Persiste filtros no LocalStorage para próxima sessão
- 11e. Retorna ao passo 11

**FA02: Comparativo Temporal**
- 11a. Usuário seleciona opção "Comparar Períodos"
- 11b. Sistema exibe seletor de períodos (mês anterior vs atual, ano anterior vs atual)
- 11c. Calcula métricas para ambos os períodos
- 11d. Exibe gráficos lado-a-lado com variação percentual
- 11e. Retorna ao passo 11

**FA03: Refresh Manual**
- 11a. Usuário clica em botão [🔄 Atualizar]
- 11b. Sistema força recálculo de todos os KPIs
- 11c. Invalida cache Redis
- 11d. Atualiza dashboard com dados frescos
- 11e. Retorna ao passo 11

### 6. Exceções

**EX01: Usuário sem Permissão**
- 2a. Sistema detecta falta de permissão `dashboard:{type}:view`
- 2b. Sistema retorna HTTP 403 Forbidden
- 2c. Exibe mensagem: "Você não tem permissão para visualizar este dashboard"
- 2d. Redireciona para página anterior

**EX02: Dashboard Não Encontrado**
- 4a. Dashboard com ID informado não existe
- 4b. Sistema retorna HTTP 404 Not Found
- 4c. Exibe mensagem: "Dashboard não encontrado"
- 4d. Redireciona para lista de dashboards

**EX03: Dashboard sem Widgets Suficientes**
- 5a. Dashboard tem menos de 4 widgets configurados
- 5b. Sistema exibe aviso: "Dashboard incompleto. Configure no mínimo 4 widgets."
- 5c. Exibe opção [Configurar Dashboard]
- 5d. UC encerrado

**EX04: Erro ao Calcular KPI**
- 6a. Falha ao executar query de agregação (timeout, dados corrompidos)
- 6b. Sistema registra erro em log
- 6c. Exibe widget com mensagem: "Erro ao carregar dados. Tente novamente."
- 6d. Permite refresh individual do widget

**EX05: Falha na Conexão SignalR**
- 10a. Não consegue estabelecer WebSocket com SignalR Hub
- 10b. Sistema exibe aviso: "Atualização em tempo real indisponível. Use refresh manual."
- 10c. Dashboard continua funcional com refresh manual
- 10d. Continua no passo 11

### 7. Pós-condições

- Dashboard exibido com 4-12 widgets
- Cada widget mostra: valor atual do KPI, meta, variância %, alert level (Green/Yellow/Red), gráfico
- Conexão SignalR estabelecida para atualização automática a cada 30 segundos
- Filtros dinâmicos aplicados e persistidos no LocalStorage
- Operação registrada em auditoria (tipo: DASHBOARD_VIEW) com: usuário, dashboard ID, timestamp, filtros aplicados

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-099-01**: Dashboard deve ter no mínimo 4 widgets
- **RN-DSH-099-02**: KPI deve ter fórmula de cálculo definida
- **RN-DSH-099-03**: Alerta dispara quando KPI sai do intervalo aceitável (< 80% meta)

---

## UC02: Configurar KPI e Meta

### 1. Descrição

Este caso de uso permite que administradores criem e configurem KPIs, definindo fórmula de cálculo (agregação), entidade origem, filtros base, meta e limites de alerta (yellow, red).

### 2. Atores

- **Ator Principal**: Administrador de Sistema / Gerente
- **Ator Secundário**: Sistema

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:kpi:configure`
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Configurações → Dashboards → KPIs | - |
| 2 | Clica em botão [+ Novo KPI] | - |
| 3 | - | Abre modal "Configurar KPI" |
| 4 | Preenche Nome do KPI (ex: "Tempo Médio Resolução P1") | - |
| 5 | Preenche Descrição detalhada | - |
| 6 | Seleciona Tipo de Agregação (SUM, AVG, COUNT, MAX, MIN, PERCENTAGE) | - |
| 7 | Seleciona Entidade Origem (Chamado, Fatura, Ativo, Contrato) | - |
| 8 | Seleciona Campo para Agregar (TempoResolucao, Valor, Quantidade) | - |
| 9 | Define Filtros Base (ex: Prioridade = P1, Status = Resolvido) | - |
| 10 | Define Unidade de Medida (horas, minutos, %, reais) | - |
| 11 | Define Meta (ex: 4 horas para P1) | - |
| 12 | Define Limite Amarelo (80% da meta = 3.2 horas) | - |
| 13 | Define Limite Vermelho (60% da meta = 2.4 horas) | - |
| 14 | Clica em [Salvar KPI] | - |
| 15 | - | Valida permissão `dashboard:kpi:configure` |
| 16 | - | Valida campos obrigatórios preenchidos |
| 17 | - | Executa `POST /api/kpis` |
| 18 | - | Cria registro do KPI no banco |
| 19 | - | Registra operação em auditoria (CREATE_KPI) |
| 20 | - | Exibe mensagem de sucesso: "KPI criado com sucesso" |
| 21 | - | Fecha modal e atualiza lista de KPIs |

### 5. Fluxos Alternativos

**FA01: Editar KPI Existente**
- 2a. Usuário clica em [✏️ Editar] em KPI existente
- 2b. Sistema carrega dados do KPI no modal
- 2c. Usuário altera campos desejados
- 2d. Sistema executa `PUT /api/kpis/{id}`
- 2e. Registra auditoria (UPDATE_KPI)
- 2f. Retorna ao passo 21

**FA02: Testar Cálculo do KPI**
- 14a. Usuário clica em [🧪 Testar Cálculo]
- 14b. Sistema executa query de agregação com filtros base
- 14c. Exibe resultado estimado e quantidade de registros processados
- 14d. Exibe tempo de execução da query
- 14e. Retorna ao passo 14

**FA03: Cancelar Criação**
- 14a. Usuário clica em [Cancelar]
- 14b. Sistema exibe confirmação: "Descartar alterações?"
- 14c. Usuário confirma
- 14d. Fecha modal sem salvar
- 14e. UC encerrado

### 6. Exceções

**EX01: Usuário sem Permissão**
- 15a. Sistema detecta falta de permissão `dashboard:kpi:configure`
- 15b. Sistema retorna HTTP 403 Forbidden
- 15c. Exibe mensagem: "Você não tem permissão para configurar KPIs"
- 15d. Fecha modal

**EX02: Campos Obrigatórios Vazios**
- 16a. Sistema detecta campos vazios (Nome, Agregação, Entidade, Meta)
- 16b. Retorna HTTP 400 Bad Request
- 16c. Exibe mensagem: "Preencha todos os campos obrigatórios"
- 16d. Destaca campos vazios em vermelho
- 16e. Retorna ao passo 4

**EX03: Meta Inválida**
- 16a. Meta definida é <= 0
- 16b. Retorna HTTP 400 Bad Request
- 16c. Exibe mensagem: "Meta deve ser maior que zero"
- 16d. Retorna ao passo 11

**EX04: Limites de Alerta Inválidos**
- 16a. Limite Amarelo ou Vermelho não está entre 0-100%
- 16b. Retorna HTTP 400 Bad Request
- 16c. Exibe mensagem: "Limites devem estar entre 0% e 100%"
- 16d. Retorna ao passo 12

**EX05: Erro ao Salvar KPI**
- 18a. Falha ao criar registro no banco
- 18b. Sistema retorna HTTP 500
- 18c. Exibe mensagem: "Erro ao salvar KPI. Tente novamente."
- 18d. Permite tentar novamente ou cancelar

### 7. Pós-condições

- Novo KPI criado com fórmula de cálculo definida
- KPI disponível para ser usado em widgets de dashboards
- Fórmula armazenada com: tipo agregação, entidade origem, campo, filtros base, meta, limites
- Operação registrada em auditoria (CREATE_KPI) com: nome do KPI, fórmula, meta, usuário, timestamp

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-099-02**: KPI deve ter fórmula de cálculo definida

---

## UC03: Drill-Down Interativo em Widget

### 1. Descrição

Este caso de uso permite que usuários cliquem em um elemento visual do widget (barra de gráfico, fatia de pizza, linha de tabela) e visualizem dados detalhados do próximo nível hierárquico, com filtros aplicados automaticamente.

### 2. Atores

- **Ator Principal**: Diretor / Gerente / Analista
- **Ator Secundário**: Sistema

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:{type}:view`
- Multi-tenancy ativo (ClienteId válido)
- Dashboard carregado com widgets (UC01 executado)
- Widget suporta drill-down (configurado com níveis hierárquicos)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Visualiza widget "Chamados por Cliente" no dashboard | - |
| 2 | Clica em barra do gráfico representando "Cliente X" | - |
| 3 | - | Detecta evento de drill-down |
| 4 | - | Aplica filtro automático: ClienteId = "Cliente X" |
| 5 | - | Executa `GET /api/dashboards/{id}/widgets/{widgetId}/drill-down?filter=ClienteId:{value}` |
| 6 | - | Retorna dados detalhados do próximo nível (lista de chamados do Cliente X) |
| 7 | - | Renderiza modal ou painel lateral com dados detalhados |
| 8 | - | Exibe tabela com colunas: ID, Título, Prioridade, Status, Data Abertura, Responsável |
| 9 | - | Permite drill-down adicional (nível 2): clicar em linha para ver detalhes do chamado |
| 10 | Visualiza dados detalhados do Cliente X | - |

### 5. Fluxos Alternativos

**FA01: Drill-Down Nível 2 (Detalhes do Chamado)**
- 9a. Usuário clica em linha da tabela representando "Chamado #123"
- 9b. Sistema executa `GET /api/chamados/123`
- 9c. Abre modal com detalhes completos do chamado
- 9d. Retorna ao passo 10

**FA02: Export de Dados Drill-Down**
- 10a. Usuário clica em [📥 Exportar]
- 10b. Sistema gera arquivo Excel com dados drill-down
- 10c. Inclui filtros aplicados no cabeçalho
- 10d. Envia arquivo para download
- 10e. Retorna ao passo 10

**FA03: Voltar para Dashboard Principal**
- 10a. Usuário clica em [← Voltar] ou [X Fechar]
- 10b. Sistema fecha modal/painel drill-down
- 10c. Retorna ao dashboard principal (UC01 passo 11)

### 6. Exceções

**EX01: Widget Não Suporta Drill-Down**
- 3a. Widget clicado não tem configuração de drill-down
- 3b. Sistema exibe mensagem: "Este widget não possui detalhamento disponível"
- 3c. UC encerrado

**EX02: Erro ao Buscar Dados Drill-Down**
- 6a. Falha ao executar query de detalhamento
- 6b. Sistema retorna HTTP 500
- 6c. Exibe mensagem: "Erro ao carregar detalhes. Tente novamente."
- 6d. Permite tentar novamente ou fechar

**EX03: Nenhum Dado Encontrado no Drill-Down**
- 6a. Query retorna 0 registros
- 6b. Sistema exibe mensagem: "Nenhum dado encontrado para o filtro selecionado"
- 6c. Opção de voltar ao dashboard principal
- 6d. UC encerrado

### 7. Pós-condições

- Dados detalhados exibidos em modal ou painel lateral
- Filtros aplicados automaticamente no próximo nível
- Operação registrada em auditoria (DRILL_DOWN) com: widget ID, filtro aplicado, nível, usuário, timestamp
- Breadcrumb exibe caminho navegado (Dashboard → Cliente X → Chamado #123)

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-099-04**: Drill-down aplica filtros automaticamente nos níveis hierárquicos

---

## UC04: Exportar Dashboard para Múltiplos Formatos

### 1. Descrição

Este caso de uso permite que usuários exportem dashboards completos ou widgets individuais para formatos PDF (com branding), Excel (com múltiplas abas) ou Power BI Embedded, com registro de auditoria completo.

### 2. Atores

- **Ator Principal**: Diretor / Gerente / Analista
- **Ator Secundário**: Sistema

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `dashboard:{type}:export`
- Multi-tenancy ativo (ClienteId válido)
- Dashboard carregado com widgets (UC01 executado)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em botão [📥 Exportar] no dashboard | - |
| 2 | - | Abre modal "Exportar Dashboard" |
| 3 | - | Exibe opções de formato: PDF, Excel, Power BI Embedded |
| 4 | Seleciona formato desejado (ex: PDF) | - |
| 5 | Marca opções: ☑ Incluir logo do cliente, ☑ Incluir data/hora, ☑ Incluir gráficos, ☑ Assinatura digital | - |
| 6 | Clica em [Exportar] | - |
| 7 | - | Valida permissão `dashboard:{type}:export` |
| 8 | - | Executa `POST /api/dashboards/{id}/export/pdf` |
| 9 | - | Gera documento PDF com: logo do cliente, nome do dashboard, data/hora de geração, widgets renderizados como imagens |
| 10 | - | Se Assinatura Digital marcada: aplica certificado digital ao PDF |
| 11 | - | Registra operação em auditoria (DASHBOARD_EXPORT) com: formato, usuário, dashboard ID, timestamp, tamanho arquivo |
| 12 | - | Envia arquivo para download |
| 13 | Recebe arquivo: Dashboard_Executivo_2025-12-28.pdf | - |

### 5. Fluxos Alternativos

**FA01: Export para Excel**
- 4a. Usuário seleciona formato Excel
- 4b. Sistema gera arquivo .xlsx com múltiplas abas: Resumo (scorecards), Gráficos (widgets como imagens), Dados (tabelas raw)
- 4c. Aplica formatação: cabeçalhos em negrito, cores do tema, autofit colunas
- 4d. Continua no passo 10

**FA02: Export para Power BI Embedded**
- 4a. Usuário seleciona "Power BI Embedded"
- 4b. Sistema gera visualização interativa do Power BI direto no browser
- 4c. Usuário pode interagir com visualizações (filtros, drill-down)
- 4d. Opção de salvar visualização no Power BI Workspace
- 4e. Continua no passo 11

**FA03: Export de Widget Individual**
- 1a. Usuário clica em [📥] em widget específico
- 1b. Sistema abre modal de export apenas para aquele widget
- 1c. Formatos disponíveis: PNG (imagem), CSV (dados), JSON (API)
- 1d. Gera arquivo do formato selecionado
- 1e. Continua no passo 11

**FA04: Cancelar Export**
- 6a. Usuário clica em [Cancelar]
- 6b. Sistema fecha modal sem exportar
- 6c. UC encerrado

### 6. Exceções

**EX01: Usuário sem Permissão**
- 7a. Sistema detecta falta de permissão `dashboard:{type}:export`
- 7b. Sistema retorna HTTP 403 Forbidden
- 7c. Exibe mensagem: "Você não tem permissão para exportar dashboards"
- 7d. Fecha modal

**EX02: Erro ao Gerar PDF**
- 9a. Falha ao renderizar widgets como imagens
- 9b. Sistema retorna HTTP 500
- 9c. Exibe mensagem: "Erro ao gerar PDF. Tente novamente ou selecione outro formato."
- 9d. Permite tentar novamente

**EX03: Certificado Digital Não Configurado**
- 10a. Assinatura Digital marcada mas certificado não está configurado
- 10b. Sistema exibe aviso: "Certificado digital não configurado. Export sem assinatura?"
- 10c. Usuário confirma export sem assinatura OU cancela
- 10d. Continua no passo 11 (sem assinatura) ou UC encerrado

**EX04: Dashboard Muito Grande**
- 9a. Dashboard tem > 20 widgets, arquivo PDF ultrapassaria 50 MB
- 9b. Sistema exibe aviso: "Dashboard muito grande para PDF. Selecione widgets específicos ou use Excel."
- 9c. Permite selecionar widgets individualmente
- 9d. Retorna ao passo 4

### 7. Pós-condições

- Arquivo exportado gerado no formato selecionado
- Se PDF: inclui logo do cliente, data/hora, widgets como imagens, assinatura digital (opcional)
- Se Excel: múltiplas abas (Resumo, Gráficos, Dados), formatação aplicada
- Se Power BI: visualização interativa disponível
- Operação registrada em auditoria (DASHBOARD_EXPORT) com: formato, usuário, dashboard ID, timestamp, tamanho arquivo, filtros aplicados

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-099-06**: Export é auditado (quem, quando, que dados)

---

## UC05: Monitorar Alertas de KPI

### 1. Descrição

Este caso de uso permite que o sistema monitore automaticamente KPIs configurados e dispare alertas quando valores saem do intervalo aceitável (< 80% meta), notificando usuários via email, SMS, push notification ou dashboard.

### 2. Atores

- **Ator Principal**: Sistema (Job Automático)
- **Ator Secundário**: Usuários cadastrados para receber alertas

### 3. Pré-condições

- KPIs configurados com metas e limites de alerta (UC02 executado)
- Job de monitoramento ativo (Hangfire)
- Usuários cadastrados para receber alertas
- Configuração de SMTP/SMS válida

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Job Hangfire executa a cada 5 minutos |
| 2 | - | Busca todos os KPIs ativos com alertas configurados |
| 3 | - | Para cada KPI: calcula valor atual usando fórmula de agregação |
| 4 | - | Compara valor atual com limites de alerta (Yellow: 80%, Red: 60%) |
| 5 | - | Se valor < 80% meta: cria registro de alerta (AlertLevel = Yellow ou Red) |
| 6 | - | Verifica se alerta já foi disparado recentemente (debounce: 30 minutos) |
| 7 | - | Se alerta novo: busca usuários cadastrados para receber notificação |
| 8 | - | Envia notificação via canais configurados: email (template multi-idioma), SMS, push notification, dashboard |
| 9 | - | Registra alerta em auditoria (ALERT_TRIGGERED) com: KPI ID, valor atual, meta, alert level, usuários notificados, timestamp |
| 10 | - | Atualiza dashboard em tempo real via SignalR (badge de alerta) |

### 5. Fluxos Alternativos

**FA01: Alerta Resolvido Automaticamente**
- 5a. Valor do KPI volta a >= 80% da meta
- 5b. Sistema cria registro de alerta resolvido (AlertLevel = Green)
- 5c. Envia notificação de resolução para usuários
- 5d. Remove badge de alerta do dashboard
- 5e. Registra resolução em auditoria (ALERT_RESOLVED)
- 5f. Retorna ao passo 10

**FA02: Usuário Reconhece Alerta Manualmente**
- 10a. Usuário clica em alerta no dashboard
- 10b. Sistema exibe detalhes do alerta (KPI, valor, meta, variação)
- 10c. Usuário clica em [✅ Reconhecer Alerta]
- 10d. Sistema marca alerta como reconhecido (não dispara novamente)
- 10e. Registra reconhecimento em auditoria
- 10f. Retorna ao passo 10

**FA03: Alerta com Debounce (Já Disparado Recentemente)**
- 6a. Alerta foi disparado há menos de 30 minutos
- 6b. Sistema NÃO reenvia notificação (evita spam)
- 6c. Atualiza apenas registro existente com novo valor
- 6d. Continua no passo 10

### 6. Exceções

**EX01: Erro ao Calcular KPI**
- 3a. Falha ao executar query de agregação
- 3b. Sistema registra erro em log
- 3c. Pula para próximo KPI sem disparar alerta
- 3d. Continua no passo 2

**EX02: Configuração de SMTP/SMS Inválida**
- 8a. Tentativa de envio de email falha (SMTP não configurado)
- 8b. Sistema registra falha em log
- 8c. Tenta canais alternativos (push notification, dashboard)
- 8d. Registra alerta mesmo sem notificação enviada
- 8e. Continua no passo 9

**EX03: Nenhum Usuário Cadastrado para Alerta**
- 7a. Não há usuários configurados para receber alerta deste KPI
- 7b. Sistema registra alerta mas não envia notificação
- 7c. Exibe alerta apenas no dashboard
- 7d. Continua no passo 9

### 7. Pós-condições

- Alerta registrado no banco com: KPI ID, valor atual, meta, alert level, timestamp, usuários notificados
- Notificações enviadas via canais configurados (email, SMS, push, dashboard)
- Dashboard atualizado em tempo real com badge de alerta (🔴 ou 🟡)
- Operação registrada em auditoria (ALERT_TRIGGERED ou ALERT_RESOLVED)
- Se alerta resolvido: badge removido e notificação de resolução enviada

### 8. Regras de Negócio Aplicáveis

- **RN-DSH-099-03**: Alerta dispara quando KPI sai do intervalo aceitável (< 80% meta)
- **RN-DSH-099-07**: Alertas têm debounce de 30 minutos para evitar spam

---

## Resumo dos Casos de Uso

| UC | Nome | Ator Principal | Complexidade | Integração |
|----|------|----------------|--------------|------------|
| UC01 | Visualizar Dashboard Executivo/Operacional | Diretor/Gerente | Alta | SignalR, Cache Redis |
| UC02 | Configurar KPI e Meta | Administrador | Média | Auditoria, RBAC |
| UC03 | Drill-Down Interativo em Widget | Usuário | Média | Filtros Dinâmicos |
| UC04 | Exportar Dashboard para Múltiplos Formatos | Usuário | Alta | PDF, Excel, Power BI |
| UC05 | Monitorar Alertas de KPI | Sistema (Job) | Alta | Hangfire, Email, SMS, SignalR |

---

**Última Atualização**: 2025-12-28
**Versão do Documento**: 1.0
**Status**: ✅ Completo

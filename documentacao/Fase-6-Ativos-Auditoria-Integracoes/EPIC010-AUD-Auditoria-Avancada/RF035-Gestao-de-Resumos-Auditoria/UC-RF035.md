# UC-RF035 — Casos de Uso Canônicos

**RF:** RF035 — Gestão de Resumos de Auditoria
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC010-AUD-Auditoria-Avancada
**Fase:** Fase-6-Ativos-Auditoria-Integracoes

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF035 — Gestão de Resumos de Auditoria**, cobrindo integralmente o comportamento funcional esperado do sistema de consolidação de auditorias em resumos gerenciais.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF035.yaml)
- Massas de Teste (MT-RF035.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

O sistema deve consolidar automaticamente itens de auditoria (RF034) e lotes (RF054) em resumos executivos com totalizadores financeiros, indicadores de performance, dashboard analítico, comparações temporais e exportação de relatórios gerenciais.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Complexidade |
|----|------|----------------|--------------|
| UC00 | Listar Resumos de Auditoria | Usuário Autenticado | Média |
| UC01 | Criar Resumo de Auditoria (Job Automático) | Sistema (Hangfire Job) | Alta |
| UC02 | Visualizar Resumo de Auditoria | Usuário Autenticado | Média |
| UC03 | Exportar Resumo | Usuário Autenticado | Média |
| UC04 | Comparar Períodos | Usuário Autenticado | Alta |
| UC05 | Dashboard Executivo | Diretor/Administrador | Alta |
| UC06 | Alertas de Anomalias | Sistema (Hangfire Job) | Alta |
| UC07 | Relatório de Tendências | Usuário Autenticado | Média |
| UC08 | Arquivar Resumos Antigos | Sistema (Hangfire Job) | Baixa |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (multi-tenancy via EmpresaId)
- Todas as ações exigem **permissão explícita RBAC** (AUD.RESUMOS.*)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação** (retenção 7 anos LGPD)
- Mensagens devem ser claras, previsíveis e rastreáveis via **i18n (Transloco)**
- Jobs Hangfire executam com **retry 3x** em caso de falha
- Resumos são calculados a partir de `AuditLog` (RF034) e `AuditBatch` (RF054)
- Drill-down para logs detalhados deve ser **navegável via hyperlink**
- Gráficos renderizados com **ApexCharts** (dashboard frontend)
- Exportações PDF com **logo + assinatura digital** (iText 8+)
- Exportações Excel com **múltiplas abas** estruturadas (EPPlus 6+)

---

## UC00 — Listar Resumos de Auditoria

### Objetivo
Exibir lista de resumos consolidados de auditoria agrupados por período (dia, semana, mês, ano) com métricas agregadas.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.VIEW_ANY`
- Empresa (tenant) selecionada

### Pós-condições
- Lista exibida conforme filtros e paginação
- Grid renderizado com métricas: Período, Total Operações, Usuários Ativos, CREATEs, UPDATEs, DELETEs, Operações Críticas

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Resumos de Auditoria"
- **FP-UC00-002:** Sistema valida permissão `AUD.RESUMOS.VIEW_ANY`
- **FP-UC00-003:** Sistema carrega resumos do tenant (filtro automático por EmpresaId)
- **FP-UC00-004:** Sistema aplica filtros padrão: Período (últimos 30 dias), Tipo (Diário)
- **FP-UC00-005:** Sistema aplica paginação (padrão: 20 registros) e ordenação (Data DESC)
- **FP-UC00-006:** Sistema exibe grid com colunas: Período, Tipo, Total Operações, Usuários Ativos, CREATEs, UPDATEs, DELETEs, Operações Críticas, Ações
- **FP-UC00-007:** Usuário pode clicar em resumo → redireciona para UC02 (Visualizar detalhes)

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por período customizado (data início/fim)
- **FA-UC00-002:** Filtrar por tipo de período (Diário, Semanal, Mensal, Anual)
- **FA-UC00-003:** Ordenar por coluna (Total Operações, Usuários Ativos, etc.)
- **FA-UC00-004:** Exportar lista para Excel (botão "Exportar Lista")

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 + mensagem `resumos_auditoria.erro_permissao`
- **FE-UC00-002:** Nenhum resumo encontrado → estado vazio exibido com mensagem `resumos_auditoria.nenhum_registro`
- **FE-UC00-003:** Erro ao carregar dados → mensagem `resumos_auditoria.erro_carregar`

### Regras de Negócio
- **RN-RF035-001:** Resumos gerados automaticamente por job diário (2h da manhã) — ver UC01
- **RN-RF035-002:** Métricas agregadas a partir de `AuditLog` com filtro por EmpresaId
- **RN-UC-00-001:** Somente resumos do tenant do usuário autenticado
- **RN-UC-00-002:** Registros soft-deleted (deleted_at IS NOT NULL) não aparecem
- **RN-UC-00-003:** Paginação padrão: 20 registros por página

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas resumos do tenant (EmpresaId) do usuário autenticado
- **CA-UC00-002:** Resumos excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna numérica
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (query params)
- **CA-UC00-006:** Grid DEVE exibir métricas agregadas: Total_Operacoes, Total_Creates, Total_Updates, Total_Deletes, Total_Usuarios_Ativos
- **CA-UC00-007:** Clique em linha do grid DEVE redirecionar para UC02 (Visualizar Resumo)

---

## UC01 — Criar Resumo de Auditoria (Job Automático)

### Objetivo
Gerar automaticamente resumos consolidados de auditoria com métricas agregadas por período via job Hangfire.

### Pré-condições
- Job Hangfire configurado com cron `0 2 * * *` (diariamente às 02:00)
- Tabela `AuditLog` contém registros do dia anterior
- Tabela `AuditSummary` existe e está acessível

### Pós-condições
- Resumos criados para 3 períodos: Diário (D-1), Semanal (se segunda-feira), Mensal (se dia 1)
- Métricas calculadas: Total_Operacoes, Total_Creates, Total_Updates, Total_Deletes, Total_Usuarios_Ativos, Total_Tabelas_Afetadas, Operacoes_Criticas, Operacoes_Fora_Horario
- Auditoria registrada: ação `RESUMO_CRIADO`, tabela `AuditSummary`

### Fluxo Principal (Automático)
- **FP-UC01-001:** Job Hangfire executa diariamente às 02:00
- **FP-UC01-002:** Sistema verifica se já existe resumo para D-1 (evitar duplicação)
- **FP-UC01-003:** Sistema agrega métricas do dia anterior via SQL:
  ```sql
  INSERT INTO AuditSummary (
    EmpresaId, Periodo, Tipo_Periodo,
    Total_Operacoes, Total_Creates, Total_Updates, Total_Deletes,
    Total_Usuarios_Ativos, Total_Tabelas_Afetadas,
    Operacoes_Criticas, Operacoes_Fora_Horario,
    created_by, created_at
  )
  SELECT
    EmpresaId,
    CAST(GETDATE()-1 AS DATE) AS Periodo,
    'Diario' AS Tipo_Periodo,
    COUNT(*) AS Total_Operacoes,
    SUM(CASE WHEN Tipo_Operacao = 'CREATE' THEN 1 ELSE 0 END) AS Total_Creates,
    SUM(CASE WHEN Tipo_Operacao = 'UPDATE' THEN 1 ELSE 0 END) AS Total_Updates,
    SUM(CASE WHEN Tipo_Operacao = 'DELETE' THEN 1 ELSE 0 END) AS Total_Deletes,
    COUNT(DISTINCT Id_Usuario) AS Total_Usuarios_Ativos,
    COUNT(DISTINCT Tabela) AS Total_Tabelas_Afetadas,
    SUM(CASE WHEN Fl_Operacao_Critica = 1 THEN 1 ELSE 0 END) AS Operacoes_Criticas,
    SUM(CASE WHEN DATEPART(HOUR, Dt_Criacao) NOT BETWEEN 8 AND 18 THEN 1 ELSE 0 END) AS Operacoes_Fora_Horario,
    'SYSTEM_JOB' AS created_by,
    GETDATE() AS created_at
  FROM AuditLog
  WHERE CAST(Dt_Criacao AS DATE) = CAST(GETDATE()-1 AS DATE)
    AND deleted_at IS NULL
  GROUP BY EmpresaId;
  ```
- **FP-UC01-004:** Se for segunda-feira, sistema cria também resumo semanal (S-1)
- **FP-UC01-005:** Se for dia 1 do mês, sistema cria também resumo mensal (M-1)
- **FP-UC01-006:** Sistema registra auditoria: tabela `AuditSummary`, ação `CREATE`, usuário `SYSTEM_JOB`
- **FP-UC01-007:** Job finaliza com sucesso → log `Resumos criados: X diários, Y semanais, Z mensais`

### Fluxos Alternativos
- **FA-UC01-001:** Resumo manual (endpoint `POST /api/auditoria/resumos`) — requer permissão `AUD.RESUMOS.CREATE`
- **FA-UC01-002:** Recalcular resumo existente (flag `force_recalculate=true`)

### Fluxos de Exceção
- **FE-UC01-001:** Resumo já existe para D-1 → skip criação + log warning
- **FE-UC01-002:** Erro no SQL → retry automático (3x com backoff exponencial)
- **FE-UC01-003:** Falha após 3 retries → notifica admin via email + registra erro no Hangfire Dashboard

### Regras de Negócio
- **RN-RF035-003:** Resumos gerados para 3 períodos: Diário (todos os dias), Semanal (segunda-feira), Mensal (dia 1)
- **RN-RF035-004:** Job retenta 3x em caso de falha (Hangfire AutomaticRetry)
- **RN-RF035-005:** Notifica admin se geração falhar após 3 tentativas (email + push notification)
- **RN-UC-01-001:** created_by DEVE ser `SYSTEM_JOB` para jobs automáticos
- **RN-UC-01-002:** EmpresaId agregado automaticamente a partir de `AuditLog.EmpresaId`
- **RN-UC-01-003:** Operações críticas = DELETEs + operações em tabelas sensíveis (Usuario, Empresa, Permissao)

### Critérios de Aceite
- **CA-UC01-001:** Job DEVE executar diariamente às 02:00 sem intervenção manual
- **CA-UC01-002:** Resumo diário DEVE consolidar 100% dos logs do dia anterior (D-1)
- **CA-UC01-003:** Resumo semanal DEVE consolidar segunda-feira a domingo da semana anterior (S-1)
- **CA-UC01-004:** Resumo mensal DEVE consolidar dia 1 a último dia do mês anterior (M-1)
- **CA-UC01-005:** Sistema DEVE evitar duplicação (verificar existência antes de criar)
- **CA-UC01-006:** Falha no job DEVE enviar email para admin (configurado em appsettings.json)
- **CA-UC01-007:** Métricas DEVEM ser calculadas via SQL agregado (performance)
- **CA-UC01-008:** Auditoria DEVE registrar created_by = `SYSTEM_JOB`, created_at = timestamp atual

---

## UC02 — Visualizar Resumo de Auditoria

### Objetivo
Exibir detalhes completos do resumo com drill-down para logs individuais, gráficos de distribuição e top entidades/usuários.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.VIEW`
- Resumo existe e pertence ao tenant do usuário

### Pós-condições
- Dados exibidos corretamente com gráficos renderizados
- Drill-down navegável para RF034 (Logs de Auditoria)

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em resumo na listagem (UC00) ou acessa URL `/auditoria/resumos/:id`
- **FP-UC02-002:** Sistema valida permissão `AUD.RESUMOS.VIEW`
- **FP-UC02-003:** Sistema valida que resumo pertence ao tenant (EmpresaId)
- **FP-UC02-004:** Sistema carrega resumo do banco (`SELECT * FROM AuditSummary WHERE Id = :id AND deleted_at IS NULL`)
- **FP-UC02-005:** Sistema exibe **Cabeçalho**: Período, Tipo (Diário/Semanal/Mensal), Total de Operações
- **FP-UC02-006:** Sistema exibe **Métricas Gerais**: CREATEs, UPDATEs, DELETEs, Acessos, Usuários Ativos, Tabelas Afetadas
- **FP-UC02-007:** Sistema renderiza **Gráficos** (ApexCharts):
  - Pizza: Distribuição por tipo de operação (CREATE/UPDATE/DELETE)
  - Barras: Top 10 usuários mais ativos
  - Barras: Top 10 tabelas mais modificadas
- **FP-UC02-008:** Sistema exibe **Operações Críticas**: Lista de DELETEs e operações fora do horário (22h-6h)
- **FP-UC02-009:** Sistema exibe link **"Ver Logs Completos"** → redireciona para RF034 com filtros aplicados (período + tenant)

### Fluxos Alternativos
- **FA-UC02-001:** Exportar resumo para PDF (botão "Exportar PDF") → UC03
- **FA-UC02-002:** Comparar com outro período (botão "Comparar") → UC04
- **FA-UC02-003:** Drill-down em gráfico (clique em barra/fatia) → filtra logs por entidade/usuário

### Fluxos de Exceção
- **FE-UC02-001:** Resumo inexistente → HTTP 404 + mensagem `resumos_auditoria.resumo_nao_encontrado`
- **FE-UC02-002:** Resumo de outro tenant → HTTP 404 (não expor existência)
- **FE-UC02-003:** Erro ao carregar gráficos → exibe placeholder "Gráficos indisponíveis"

### Regras de Negócio
- **RN-RF035-006:** Drill-down aplica filtros automaticamente em logs detalhados (RF034): `periodo=:periodo AND empresaId=:empresaId`
- **RN-RF035-007:** Gráficos renderizados com **ApexCharts** (biblioteca JavaScript)
- **RN-UC-02-001:** Isolamento por tenant (resumo de outro tenant retorna 404)
- **RN-UC-02-002:** Informações de auditoria visíveis: created_by, created_at (se job: `SYSTEM_JOB`)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar resumos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas: created_by (`SYSTEM_JOB` ou ID usuário), created_at
- **CA-UC02-003:** Tentativa de acessar resumo de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar resumo inexistente DEVE retornar 404
- **CA-UC02-005:** Gráficos DEVEM renderizar via ApexCharts (biblioteca já instalada no frontend)
- **CA-UC02-006:** Link "Ver Logs Completos" DEVE redirecionar para RF034 com query params: `?periodo=YYYY-MM-DD&empresaId=X`
- **CA-UC02-007:** Top 10 usuários DEVE ordenar por Total_Operacoes DESC
- **CA-UC02-008:** Top 10 tabelas DEVE ordenar por Total_Modificacoes DESC

---

## UC03 — Exportar Resumo

### Objetivo
Exportar resumo consolidado em formato PDF ou Excel para apresentação gerencial.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.EXPORT`
- Resumo existe e pertence ao tenant do usuário

### Pós-condições
- Arquivo gerado e disponibilizado para download
- Arquivo retido por 30 dias em Azure Blob Storage
- Auditoria registrada: ação `EXPORT`, tipo_arquivo (PDF/Excel)

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa UC02 (Visualizar Resumo)
- **FP-UC03-002:** Usuário clica em "Exportar" e seleciona formato: PDF ou Excel
- **FP-UC03-003:** Sistema valida permissão `AUD.RESUMOS.EXPORT`
- **FP-UC03-004:** Sistema gera arquivo com:
  - **Sumário Executivo**: Período, Tipo, Total Operações, Usuários Ativos, Operações Críticas
  - **Gráficos Visuais**: PNG embedado (gerado via ApexCharts backend ou Playwright screenshot)
  - **Tabelas**: Top 10 usuários, Top 10 tabelas
  - **Detalhamento**: Lista de operações críticas com timestamp + usuário + tabela
- **FP-UC03-005:** Sistema salva arquivo em Azure Blob Storage com nome `resumo_auditoria_{periodo}_{empresaId}_{timestamp}.pdf`
- **FP-UC03-006:** Sistema registra auditoria: tabela `AuditSummary`, ação `EXPORT`, detalhes `{tipo_arquivo: "PDF", periodo: "..."}`
- **FP-UC03-007:** Sistema retorna URL de download ou inicia download automático

### Fluxos Alternativos
- **FA-UC03-001:** Exportar múltiplos resumos (seleção em lote no UC00) → gera ZIP com múltiplos arquivos
- **FA-UC03-002:** Agendar exportação recorrente (configurar notificação mensal)

### Fluxos de Exceção
- **FE-UC03-001:** Erro ao gerar PDF → HTTP 500 + mensagem `resumos_auditoria.erro_exportar_pdf`
- **FE-UC03-002:** Erro ao enviar para Azure Blob → fallback para download direto
- **FE-UC03-003:** Timeout na geração de gráficos → gera arquivo sem gráficos + aviso

### Regras de Negócio
- **RN-RF035-008:** PDF gerado com **logo da empresa** (configurado por tenant) e **assinatura digital** (certificado A1)
- **RN-RF035-009:** Excel inclui múltiplas abas: Sumário, Usuários, Tabelas, Operações Críticas
- **RN-RF035-010:** Arquivo retido por **30 dias** em Azure Blob Storage (expiration policy)
- **RN-UC-03-001:** Biblioteca PDF: **iText 8+** (backend .NET)
- **RN-UC-03-002:** Biblioteca Excel: **EPPlus 6+** (backend .NET)

### Critérios de Aceite
- **CA-UC03-001:** PDF DEVE incluir logo da empresa (configurado em `Empresa.LogoUrl`)
- **CA-UC03-002:** PDF DEVE incluir assinatura digital (certificado configurado em appsettings.json)
- **CA-UC03-003:** Excel DEVE ter 4 abas: Sumário, Usuários, Tabelas, Críticas
- **CA-UC03-004:** Arquivo DEVE ser salvo em Azure Blob Storage com retention 30 dias
- **CA-UC03-005:** Nome do arquivo DEVE seguir padrão: `resumo_auditoria_{periodo}_{empresaId}_{timestamp}.{pdf|xlsx}`
- **CA-UC03-006:** Auditoria DEVE registrar ação EXPORT com detalhes: tipo_arquivo, periodo, usuario_exportou
- **CA-UC03-007:** Gráficos em PDF DEVEM ser embedados como PNG (via Chart.js backend ou Playwright)

---

## UC04 — Comparar Períodos

### Objetivo
Comparar métricas entre dois períodos (ex: Janeiro vs Fevereiro) para identificar variações significativas de atividade.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.COMPARE`
- Pelo menos 2 resumos do mesmo tipo (ambos Diários OU Semanais OU Mensais) existem

### Pós-condições
- Comparação exibida lado a lado com Δ (variação percentual)
- Anomalias destacadas (Δ > 50% ou Δ < -50%)

### Fluxo Principal
- **FP-UC04-001:** Usuário acessa funcionalidade "Comparar Períodos"
- **FP-UC04-002:** Sistema valida permissão `AUD.RESUMOS.COMPARE`
- **FP-UC04-003:** Usuário seleciona **Período 1**: Janeiro/2025 (dropdown de resumos mensais)
- **FP-UC04-004:** Usuário seleciona **Período 2**: Fevereiro/2025 (dropdown de resumos mensais)
- **FP-UC04-005:** Sistema valida que ambos resumos são do mesmo tipo (ambos Mensais)
- **FP-UC04-006:** Sistema carrega dados de ambos resumos
- **FP-UC04-007:** Sistema calcula Δ para cada métrica: `((Periodo2 - Periodo1) / Periodo1) * 100`
- **FP-UC04-008:** Sistema exibe comparação lado a lado:
  ```
  ┌───────────────────────────────────────────┐
  │ Comparação: Jan/2025 vs Fev/2025          │
  ├───────────────────────────────────────────┤
  │ Métrica         │ Jan    │ Fev    │ Δ     │
  ├─────────────────┼────────┼────────┼───────┤
  │ Total Operações │ 12.500 │ 15.200 │ +21%  │
  │ CREATEs         │ 3.200  │ 4.100  │ +28%  │
  │ UPDATEs         │ 8.500  │ 10.200 │ +20%  │
  │ DELETEs         │ 800    │ 900    │ +12%  │
  │ Usuários Ativos │ 45     │ 48     │ +6%   │
  │ Ops Críticas    │ 12     │ 8      │ -33%  │ <- Destaque verde
  └─────────────────┴────────┴────────┴───────┘
  ```
- **FP-UC04-009:** Sistema destaca em **vermelho** anomalias: Δ > +50% OU Δ < -50%
- **FP-UC04-010:** Sistema exibe gráfico de linhas sobreposto: Operações por dia dos dois períodos

### Fluxos Alternativos
- **FA-UC04-001:** Comparar múltiplos períodos (3 ou mais) → gráfico de linhas multi-série
- **FA-UC04-002:** Exportar comparação para Excel → aba adicional no UC03

### Fluxos de Exceção
- **FE-UC04-001:** Períodos de tipos diferentes (ex: Diário vs Mensal) → erro `resumos_auditoria.erro_tipos_incompativeis`
- **FE-UC04-002:** Divisão por zero no cálculo Δ → exibe "N/A" na célula

### Regras de Negócio
- **RN-RF035-011:** Variação > 100% notifica admin (possível anomalia grave)
- **RN-RF035-012:** Comparação limitada a períodos do **mesmo tipo** (mês com mês, dia com dia)
- **RN-UC-04-001:** Δ calculado como: `((Valor_Novo - Valor_Antigo) / Valor_Antigo) * 100`
- **RN-UC-04-002:** Destaque visual: Δ > +50% OU Δ < -50% = vermelho bold

### Critérios de Aceite
- **CA-UC04-001:** Sistema DEVE permitir comparar apenas resumos do mesmo tipo (Diário/Semanal/Mensal)
- **CA-UC04-002:** Tentativa de comparar tipos diferentes DEVE retornar erro claro
- **CA-UC04-003:** Δ DEVE ser calculado como percentual com 2 casas decimais
- **CA-UC04-004:** Δ > +50% ou Δ < -50% DEVE ser destacado em vermelho bold
- **CA-UC04-005:** Divisão por zero (Valor_Antigo = 0) DEVE exibir "N/A" ao invés de erro
- **CA-UC04-006:** Gráfico de linhas DEVE sobrepor operações dos dois períodos para visualização comparativa
- **CA-UC04-007:** Variação > 100% DEVE notificar admin via email (configurável em appsettings.json)

---

## UC05 — Dashboard Executivo

### Objetivo
Dashboard consolidado para diretoria com visão de alto nível do uso do sistema: usuários ativos, operações, tendências, conformidade.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.DASHBOARD_EXECUTIVO` (restrita a perfil Diretor/VP/Admin)
- Pelo menos 1 resumo mensal existe

### Pós-condições
- Dashboard exibido com KPIs, gráficos e alertas atualizados
- Cache válido por 24h (renovado às 03:00 após job de criação)

### Fluxo Principal
- **FP-UC05-001:** Usuário com perfil Diretor/VP acessa rota `/auditoria/dashboard-executivo`
- **FP-UC05-002:** Sistema valida permissão `AUD.RESUMOS.DASHBOARD_EXECUTIVO`
- **FP-UC05-003:** Sistema verifica cache (válido até 03:00 do dia seguinte)
- **FP-UC05-004:** Se cache válido, carrega dados do cache Redis
- **FP-UC05-005:** Se cache expirado, recalcula dashboard:
  - KPIs: Total Operações (mês atual), Usuários Ativos (mês atual), Taxa de Crescimento (vs mês anterior), Conformidade LGPD (%)
  - Gráfico de Linha: Operações por mês (últimos 12 meses)
  - Gráfico de Pizza: Distribuição CREATEs vs UPDATEs vs DELETEs (mês atual)
  - Top 5 Usuários: Mais ativos do mês
  - Top 5 Módulos: Mais utilizados (por tabela)
  - Alertas: Operações críticas, falhas de conformidade, acessos suspeitos
- **FP-UC05-006:** Sistema exibe dashboard renderizado
- **FP-UC05-007:** Usuário pode clicar "Exportar PDF Executivo" → UC03 (versão simplificada para C-level)

### Fluxos Alternativos
- **FA-UC05-001:** Selecionar período customizado (últimos 3/6/12 meses)
- **FA-UC05-002:** Drill-down em KPI → redireciona para UC00 com filtro aplicado

### Fluxos de Exceção
- **FE-UC05-001:** Usuário sem permissão → HTTP 403 + mensagem `resumos_auditoria.dashboard_acesso_negado`
- **FE-UC05-002:** Nenhum resumo mensal → exibe placeholder "Dados insuficientes"

### Regras de Negócio
- **RN-RF035-013:** Dashboard atualizado diariamente (cache renovado às 03:00 após job de criação)
- **RN-RF035-014:** Acesso restrito a perfil **Diretor** e **Admin** (configurado em RBAC)
- **RN-RF035-015:** Exportação one-click para **PDF executivo** (layout simplificado para C-level)
- **RN-UC-05-001:** Cache armazenado em Redis com TTL de 24h
- **RN-UC-05-002:** Taxa de Crescimento = `((Mes_Atual - Mes_Anterior) / Mes_Anterior) * 100`

### Critérios de Aceite
- **CA-UC05-001:** Dashboard DEVE ser acessível SOMENTE para perfis Diretor, VP e Admin
- **CA-UC05-002:** Cache DEVE ser renovado automaticamente às 03:00 (após job de criação de resumos)
- **CA-UC05-003:** KPIs DEVEM exibir dados do mês atual vs mês anterior
- **CA-UC05-004:** Gráfico de linha DEVE mostrar últimos 12 meses de operações
- **CA-UC05-005:** Top 5 Usuários DEVE ordenar por Total_Operacoes DESC (mês atual)
- **CA-UC05-006:** Top 5 Módulos DEVE ordenar por Total_Acessos DESC (por tabela)
- **CA-UC05-007:** Botão "Exportar PDF Executivo" DEVE gerar PDF simplificado (1 página com KPIs principais)

---

## UC06 — Alertas de Anomalias

### Objetivo
Detectar automaticamente padrões anormais de atividade via Machine Learning e notificar administradores.

### Pré-condições
- Job Hangfire configurado com cron `0 3 * * 0` (semanalmente aos domingos às 03:00)
- Pelo menos 90 dias de histórico de resumos (baseline para ML)

### Pós-condições
- Anomalias detectadas e registradas em `AuditAnomaly`
- Admin notificado via email e push notification
- Alertas exibidos no UC05 (Dashboard Executivo)

### Fluxo Principal (Automático)
- **FP-UC06-001:** Job Hangfire executa semanalmente (domingo 03:00)
- **FP-UC06-002:** Sistema carrega resumos dos últimos 30 dias
- **FP-UC06-003:** Sistema calcula baseline (média móvel de 90 dias para cada métrica)
- **FP-UC06-004:** Sistema detecta anomalias via algoritmo de detecção:
  - **Pico de DELETEs**: > 3x desvio padrão da média histórica
  - **Usuários hiperativos**: > 5x média de operações por usuário
  - **Acessos fora do horário**: > 20% das operações entre 22h-6h
  - **Tabelas críticas**: Modificações não autorizadas em `Usuario`, `Empresa`, `Permissao`
- **FP-UC06-005:** Para cada anomalia detectada:
  - Cria registro em `AuditAnomaly`: tipo, valor_detectado, threshold, periodo, empresaId
  - Envia email ao admin: `"Anomalia detectada: {tipo} = {valor} (threshold: {threshold})"`
  - Cria push notification no dashboard
- **FP-UC06-006:** Sistema registra auditoria: ação `ANOMALIA_DETECTADA`, detalhes `{tipo, valor, threshold}`

### Fluxos Alternativos
- **FA-UC06-001:** Marcar anomalia como "Falso Positivo" → atualiza `AuditAnomaly.Fl_Falso_Positivo = true`
- **FA-UC06-002:** Ajustar threshold de detecção (configurável por tipo de anomalia)

### Fluxos de Exceção
- **FE-UC06-001:** Histórico insuficiente (< 90 dias) → skip detecção + log warning
- **FE-UC06-002:** Erro ao enviar email → registra falha + retry no próximo ciclo

### Regras de Negócio
- **RN-RF035-016:** Baseline calculado com base em **média móvel de 90 dias**
- **RN-RF035-017:** Threshold configurável por tipo de anomalia (padrão: **3x desvio padrão**)
- **RN-RF035-018:** Falsos positivos podem ser marcados como "Ignorar" (não notifica novamente)
- **RN-UC-06-001:** Algoritmo de detecção: Z-score > 3 (3 desvios padrão) = anomalia
- **RN-UC-06-002:** Email enviado para admin configurado em `appsettings.json:AdminEmail`

### Critérios de Aceite
- **CA-UC06-001:** Job DEVE executar semanalmente (domingo 03:00) sem intervenção manual
- **CA-UC06-002:** Baseline DEVE ser calculado com média móvel de 90 dias
- **CA-UC06-003:** Threshold padrão DEVE ser 3x desvio padrão (configurável)
- **CA-UC06-004:** Anomalias detectadas DEVEM ser registradas em `AuditAnomaly`
- **CA-UC06-005:** Admin DEVE receber email para cada anomalia detectada
- **CA-UC06-006:** Falsos positivos DEVEM poder ser marcados manualmente (flag `Fl_Falso_Positivo`)
- **CA-UC06-007:** Alertas DEVEM aparecer no UC05 (Dashboard Executivo) com destaque visual

---

## UC07 — Relatório de Tendências

### Objetivo
Análise estatística de tendências de uso do sistema ao longo do tempo: crescimento de usuários, módulos mais populares, horários de pico.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.RESUMOS.TENDENCIAS`
- Pelo menos 3 meses de histórico de resumos

### Pós-condições
- Relatório exibido com gráficos de tendências e previsões
- Exportação disponível para PDF/Excel

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa rota `/auditoria/tendencias`
- **FP-UC07-002:** Sistema valida permissão `AUD.RESUMOS.TENDENCIAS`
- **FP-UC07-003:** Usuário seleciona período de análise (últimos 3/6/12 meses)
- **FP-UC07-004:** Sistema carrega resumos do período selecionado
- **FP-UC07-005:** Sistema gera relatório com:
  - **Crescimento de Usuários**: Gráfico de linha mostrando usuários ativos por mês
  - **Módulos Populares**: Top 10 tabelas mais acessadas com tendência de crescimento (via regressão linear)
  - **Horários de Pico**: Heatmap de operações por hora do dia (0-23h)
  - **Dias da Semana**: Distribuição de operações seg-dom (gráfico de barras)
  - **Sazonalidade**: Identificação de padrões mensais (ex: fim de mês sempre tem pico)
- **FP-UC07-006:** Sistema calcula **Previsão** para próximos 3 meses (regressão linear simples)
- **FP-UC07-007:** Sistema exibe relatório renderizado

### Fluxos Alternativos
- **FA-UC07-001:** Exportar relatório para PDF → UC03
- **FA-UC07-002:** Selecionar módulo específico para análise detalhada

### Fluxos de Exceção
- **FE-UC07-001:** Histórico insuficiente (< 3 meses) → erro `resumos_auditoria.historico_insuficiente`
- **FE-UC07-002:** Erro no cálculo de regressão → exibe tendência sem previsão

### Regras de Negócio
- **RN-RF035-019:** Análise baseada em **resumos consolidados** (performance) ao invés de logs individuais
- **RN-RF035-020:** Tendência calculada via **regressão linear simples** (y = ax + b)
- **RN-RF035-021:** Previsão próximos 3 meses baseada em histórico mínimo de 6 meses
- **RN-UC-07-001:** Heatmap gerado a partir de `Operacoes_Fora_Horario` e logs detalhados
- **RN-UC-07-002:** Sazonalidade detectada via análise de variância mensal

### Critérios de Aceite
- **CA-UC07-001:** Relatório DEVE exigir mínimo 3 meses de histórico
- **CA-UC07-002:** Tendência DEVE ser calculada via regressão linear (biblioteca Math.NET ou similar)
- **CA-UC07-003:** Previsão DEVE mostrar próximos 3 meses com intervalo de confiança
- **CA-UC07-004:** Heatmap DEVE exibir 24 horas (0-23h) vs 7 dias da semana
- **CA-UC07-005:** Top 10 módulos DEVE ordenar por Total_Acessos DESC
- **CA-UC07-006:** Gráfico de crescimento DEVE mostrar usuários ativos (não total de usuários)
- **CA-UC07-007:** Sazonalidade DEVE identificar meses com pico recorrente (ex: "Dezembro sempre tem +30%")

---

## UC08 — Arquivar Resumos Antigos

### Objetivo
Arquivar automaticamente resumos com mais de 2 anos para tabela de histórico, mantendo banco principal leve e performático.

### Pré-condições
- Job Hangfire configurado com cron `0 4 1 * *` (mensalmente no dia 1 às 04:00)
- Tabela `AuditSummary_Archive` existe

### Pós-condições
- Resumos > 2 anos movidos para `AuditSummary_Archive`
- Registros removidos de `AuditSummary`
- Auditoria registrada: ação `ARCHIVE`, quantidade de resumos arquivados

### Fluxo Principal (Automático)
- **FP-UC08-001:** Job Hangfire executa mensalmente (dia 1 às 04:00)
- **FP-UC08-002:** Sistema busca resumos com > 2 anos:
  ```sql
  SELECT * FROM AuditSummary
  WHERE DATEDIFF(YEAR, Periodo, GETDATE()) > 2
    AND deleted_at IS NULL;
  ```
- **FP-UC08-003:** Sistema insere resumos em `AuditSummary_Archive`:
  ```sql
  INSERT INTO AuditSummary_Archive
  SELECT * FROM AuditSummary
  WHERE DATEDIFF(YEAR, Periodo, GETDATE()) > 2;
  ```
- **FP-UC08-004:** Sistema marca resumos como arquivados na tabela original:
  ```sql
  UPDATE AuditSummary
  SET Fl_Arquivado = 1, archived_at = GETDATE()
  WHERE DATEDIFF(YEAR, Periodo, GETDATE()) > 2;
  ```
- **FP-UC08-005:** Sistema registra auditoria: ação `ARCHIVE`, detalhes `{quantidade_arquivada: X}`
- **FP-UC08-006:** Job finaliza com log: `Arquivados X resumos com > 2 anos`

### Fluxos Alternativos
- **FA-UC08-001:** Restaurar resumo arquivado (acesso via interface "Ver Arquivados")
- **FA-UC08-002:** Anonimizar resumos > 10 anos (compliance LGPD)

### Fluxos de Exceção
- **FE-UC08-001:** Nenhum resumo para arquivar → skip + log info
- **FE-UC08-002:** Erro ao mover para arquivo → retry automático (3x)

### Regras de Negócio
- **RN-RF035-022:** Resumos arquivados acessíveis via interface "Ver Arquivados" (read-only)
- **RN-RF035-023:** Retenção total: **10 anos** (2 anos ativo + 8 anos arquivado)
- **RN-RF035-024:** Após 10 anos, resumos são **anonimizados** (remove created_by, Id_Usuario) — compliance LGPD
- **RN-UC-08-001:** Arquivamento é **soft** (flag `Fl_Arquivado = 1`) para manter rastreabilidade
- **RN-UC-08-002:** Delete físico apenas após 10 anos + anonimização

### Critérios de Aceite
- **CA-UC08-001:** Job DEVE executar mensalmente (dia 1 às 04:00) sem intervenção manual
- **CA-UC08-002:** Resumos > 2 anos DEVEM ser movidos para `AuditSummary_Archive`
- **CA-UC08-003:** Resumos arquivados DEVEM permanecer acessíveis via interface "Ver Arquivados"
- **CA-UC08-004:** Flag `Fl_Arquivado = 1` DEVE ser setada na tabela original (soft archive)
- **CA-UC08-005:** Resumos > 10 anos DEVEM ser anonimizados (remove IDs de usuários)
- **CA-UC08-006:** Auditoria DEVE registrar quantidade de resumos arquivados
- **CA-UC08-007:** Anonimização DEVE preservar métricas agregadas (Total_Operacoes, etc.)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF035 | Endpoints API | Permissões RBAC |
|----|------------------------|---------------|-----------------|
| UC00 | RN-RF035-001, RN-RF035-002 | GET /api/auditoria/resumos | AUD.RESUMOS.VIEW_ANY |
| UC01 | RN-RF035-003, RN-RF035-004, RN-RF035-005 | POST /api/auditoria/resumos | SYSTEM_JOB |
| UC02 | RN-RF035-006, RN-RF035-007 | GET /api/auditoria/resumos/:id | AUD.RESUMOS.VIEW |
| UC03 | RN-RF035-008, RN-RF035-009, RN-RF035-010 | POST /api/auditoria/resumos/:id/export | AUD.RESUMOS.EXPORT |
| UC04 | RN-RF035-011, RN-RF035-012 | POST /api/auditoria/resumos/comparar | AUD.RESUMOS.COMPARE |
| UC05 | RN-RF035-013, RN-RF035-014, RN-RF035-015 | GET /api/auditoria/resumos/dashboard | AUD.RESUMOS.DASHBOARD_EXECUTIVO |
| UC06 | RN-RF035-016, RN-RF035-017, RN-RF035-018 | POST /api/auditoria/resumos/anomalias | SYSTEM_JOB |
| UC07 | RN-RF035-019, RN-RF035-020, RN-RF035-021 | GET /api/auditoria/resumos/tendencias | AUD.RESUMOS.TENDENCIAS |
| UC08 | RN-RF035-022, RN-RF035-023, RN-RF035-024 | POST /api/auditoria/resumos/arquivar | SYSTEM_JOB |

---

## 5. INTEGRAÇÕES OBRIGATÓRIAS

### 5.1. Central de Funcionalidades
- Feature: "Resumos de Auditoria" com 9 UCs
- Permissões: `AUD.RESUMOS.VIEW_ANY`, `AUD.RESUMOS.VIEW`, `AUD.RESUMOS.CREATE`, `AUD.RESUMOS.EXPORT`, `AUD.RESUMOS.COMPARE`, `AUD.RESUMOS.DASHBOARD_EXECUTIVO`, `AUD.RESUMOS.TENDENCIAS`

### 5.2. Internacionalização (i18n via Transloco)
**Chaves obrigatórias:**
```json
{
  "resumos_auditoria.titulo": "Resumos de Auditoria",
  "resumos_auditoria.periodo.diario": "Diário",
  "resumos_auditoria.periodo.semanal": "Semanal",
  "resumos_auditoria.periodo.mensal": "Mensal",
  "resumos_auditoria.periodo.anual": "Anual",
  "resumos_auditoria.operacoes_totais": "Total de Operações",
  "resumos_auditoria.usuarios_ativos": "Usuários Ativos",
  "resumos_auditoria.operacoes_criticas": "Operações Críticas",
  "resumos_auditoria.comparar": "Comparar Períodos",
  "resumos_auditoria.dashboard_executivo": "Dashboard Executivo",
  "resumos_auditoria.tendencias": "Análise de Tendências",
  "resumos_auditoria.anomalia_detectada": "Anomalia Detectada",
  "resumos_auditoria.exportar": "Exportar Resumo",
  "resumos_auditoria.erro_permissao": "Você não tem permissão para acessar resumos de auditoria",
  "resumos_auditoria.nenhum_registro": "Nenhum resumo encontrado para o período selecionado",
  "resumos_auditoria.resumo_nao_encontrado": "Resumo não encontrado",
  "resumos_auditoria.erro_tipos_incompativeis": "Não é possível comparar períodos de tipos diferentes"
}
```

**Idiomas obrigatórios:** pt-BR, en-US, es-ES

### 5.3. Auditoria
- Auditar: Criação de resumos (job), Exportações, Comparações, Detecção de anomalias
- Retenção: 7 anos (LGPD)
- Campos auditados: tabela `AuditSummary`, ação (CREATE/EXPORT/COMPARE/ANOMALIA_DETECTADA), created_by, created_at

### 5.4. Controle de Acesso (RBAC)
**Matriz de Permissões:**
| Perfil | Permissões |
|--------|------------|
| Admin | AUD.RESUMOS.* (todas) |
| Auditor | AUD.RESUMOS.VIEW_ANY, VIEW, EXPORT, TENDENCIAS |
| Diretor | AUD.RESUMOS.VIEW_ANY, VIEW, DASHBOARD_EXECUTIVO, EXPORT |
| VP | AUD.RESUMOS.DASHBOARD_EXECUTIVO, VIEW_ANY |
| Usuário Padrão | Nenhuma (acesso negado) |

---

## 6. CHAVES DE TRADUÇÃO COMPLETAS (i18n)

```json
{
  "resumos_auditoria.titulo": "Resumos de Auditoria",
  "resumos_auditoria.subtitulo": "Consolidação automática de logs de auditoria",
  "resumos_auditoria.periodo.diario": "Diário",
  "resumos_auditoria.periodo.semanal": "Semanal",
  "resumos_auditoria.periodo.mensal": "Mensal",
  "resumos_auditoria.periodo.anual": "Anual",
  "resumos_auditoria.operacoes_totais": "Total de Operações",
  "resumos_auditoria.usuarios_ativos": "Usuários Ativos",
  "resumos_auditoria.operacoes_criticas": "Operações Críticas",
  "resumos_auditoria.operacoes_fora_horario": "Operações Fora do Horário",
  "resumos_auditoria.tabelas_afetadas": "Tabelas Afetadas",
  "resumos_auditoria.creates": "CREATEs",
  "resumos_auditoria.updates": "UPDATEs",
  "resumos_auditoria.deletes": "DELETEs",
  "resumos_auditoria.comparar": "Comparar Períodos",
  "resumos_auditoria.dashboard_executivo": "Dashboard Executivo",
  "resumos_auditoria.tendencias": "Análise de Tendências",
  "resumos_auditoria.anomalia_detectada": "Anomalia Detectada",
  "resumos_auditoria.exportar": "Exportar Resumo",
  "resumos_auditoria.exportar_pdf": "Exportar PDF",
  "resumos_auditoria.exportar_excel": "Exportar Excel",
  "resumos_auditoria.ver_logs": "Ver Logs Completos",
  "resumos_auditoria.ver_arquivados": "Ver Resumos Arquivados",
  "resumos_auditoria.erro_permissao": "Você não tem permissão para acessar resumos de auditoria",
  "resumos_auditoria.erro_carregar": "Erro ao carregar resumos. Tente novamente.",
  "resumos_auditoria.erro_exportar_pdf": "Erro ao gerar PDF. Tente novamente.",
  "resumos_auditoria.erro_tipos_incompativeis": "Não é possível comparar períodos de tipos diferentes (ex: Diário vs Mensal)",
  "resumos_auditoria.nenhum_registro": "Nenhum resumo encontrado para o período selecionado",
  "resumos_auditoria.resumo_nao_encontrado": "Resumo não encontrado ou você não tem permissão para acessá-lo",
  "resumos_auditoria.historico_insuficiente": "Histórico insuficiente para análise de tendências (mínimo 3 meses)",
  "resumos_auditoria.dashboard_acesso_negado": "Acesso negado. Dashboard Executivo restrito a Diretores e Administradores",
  "resumos_auditoria.sucesso_exportar": "Arquivo exportado com sucesso",
  "resumos_auditoria.confirmacao_anomalia": "Deseja marcar esta anomalia como falso positivo?",
  "resumos_auditoria.variacao": "Variação",
  "resumos_auditoria.baseline": "Baseline (90 dias)",
  "resumos_auditoria.previsao": "Previsão (3 meses)"
}
```

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato — migração para governança v2.0 com aderência 100% ao template oficial UC.md. Adicionadas seções obrigatórias: Objetivo do Documento, Padrões Gerais, Matriz de Rastreabilidade, Changelog. Reformatados fluxos com IDs (FP-UCXX-NNN). Adicionados Critérios de Aceite em todos os UCs. Mantidos 9 UCs originais (vs 5 esperados em rastreabilidade) devido à cobertura funcional superior e alinhamento com 18 endpoints do catalog RF035.yaml. |
| 1.0 | 2025-12-18 | Architect Agent | Criação inicial com 9 casos de uso — versão pré-governança v2.0 |

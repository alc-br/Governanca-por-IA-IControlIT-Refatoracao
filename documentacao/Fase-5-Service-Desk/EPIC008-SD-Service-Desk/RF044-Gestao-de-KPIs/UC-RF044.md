# UC-RF044 — Casos de Uso Canônicos

**RF:** RF044 — Gestão de KPIs (Key Performance Indicators)
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase-5-Service-Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF044**, cobrindo integralmente o comportamento funcional esperado do motor completo de KPIs para monitoramento estratégico e operacional.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF044.yaml)
- Massas de Teste (MT-RF044.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar KPIs | Usuário Autenticado |
| UC01 | Criar KPI | Usuário Autenticado |
| UC02 | Visualizar KPI | Usuário Autenticado |
| UC03 | Editar KPI | Usuário Autenticado |
| UC04 | Excluir KPI | Usuário Autenticado |
| UC05 | Definir Metas | Usuário Autenticado |
| UC06 | Configurar Alertas | Usuário Autenticado |
| UC07 | Visualizar Dashboard | Usuário Autenticado |
| UC08 | Exportar KPIs | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant**
- Todas as ações exigem **permissão explícita** (RBAC por categoria de KPI)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Fórmulas SQL têm timeout de 30 segundos
- Versionamento de fórmulas é obrigatório em edições
- Histórico de 7 anos conforme LGPD

---

## UC00 — Listar KPIs

### Objetivo
Permitir que o usuário visualize todos os KPIs disponíveis filtrados por categoria e permissões RBAC.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.LISTAR`
- Permissões de visualização por categoria (GES.KPI.VIEW.FINANCEIRO, GES.KPI.VIEW.OPERACIONAL, etc.)

### Pós-condições
- Lista exibida conforme filtros, paginação e permissões RBAC

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa menu KPIs
- **FP-UC00-002:** Sistema valida permissão GES.KPI.LISTAR
- **FP-UC00-003:** Sistema valida permissões de categoria (RBAC)
- **FP-UC00-004:** Sistema carrega KPIs do tenant com filtro por categoria permitida
- **FP-UC00-005:** Sistema aplica paginação e ordenação
- **FP-UC00-006:** Sistema calcula status semáforo (verde/amarelo/vermelho) conforme RN-RF044-05
- **FP-UC00-007:** Sistema exibe lista com: Código, Nome, Categoria, Valor Atual, Meta, Status, Última Atualização

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por categoria (Financeiro, Operacional, Qualidade, Comercial, Serviço)
- **FA-UC00-002:** Filtrar por status (Draft, Active, Inactive)
- **FA-UC00-003:** Ordenar por Nome, Categoria, Valor Atual, Última Atualização
- **FA-UC00-004:** Buscar por código ou nome do KPI

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão GES.KPI.LISTAR → acesso negado (403)
- **FE-UC00-002:** Usuário sem permissão para categoria → KPIs da categoria não aparecem
- **FE-UC00-003:** Nenhum KPI cadastrado → estado vazio exibido

### Regras de Negócio
- RN-RF044-12: RBAC filtra KPIs por categoria conforme permissões do usuário
- RN-RF044-15: Histórico de 7 anos é mantido
- RN-RF044-05: Semáforo Automático calculado: Verde (≥100% meta), Amarelo (90-99%), Vermelho (<90%)

### Critérios de Aceite
- **CA-UC00-001:** Lista DEVE exibir apenas KPIs do tenant do usuário autenticado
- **CA-UC00-002:** KPIs excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Filtro RBAC por categoria DEVE ser aplicado automaticamente
- **CA-UC00-005:** Status semáforo DEVE ser calculado em tempo real conforme RN-RF044-05
- **CA-UC00-006:** Coluna "Última Atualização" DEVE exibir data/hora do último cálculo

---

## UC01 — Criar KPI

### Objetivo
Permitir a criação de um novo KPI com fórmula de cálculo, periodicidade e metas.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.CRIAR`

### Pós-condições
- KPI criado no estado "draft"
- Fórmula validada
- Versionamento de fórmula iniciado
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário solicita criação de KPI
- **FP-UC01-002:** Sistema valida permissão GES.KPI.CRIAR
- **FP-UC01-003:** Sistema exibe formulário
- **FP-UC01-004:** Usuário informa: Código*, Nome*, Descrição*, Categoria*, Fórmula_Cálculo*, Periodicidade*, Fonte_Dados*, Responsável*
- **FP-UC01-005:** Sistema valida código único conforme RN-RF044-01 (formato KPI-{CATEGORIA}-{SEQUENCIAL})
- **FP-UC01-006:** Sistema valida fórmula SQL conforme RN-RF044-02 (query válida retornando valor numérico)
- **FP-UC01-007:** Sistema valida periodicidade por fonte de dados conforme RN-RF044-03 (API externa: mínimo 1h)
- **FP-UC01-008:** Sistema cria registro com estado "draft"
- **FP-UC01-009:** Sistema cria versão 1.0 da fórmula em KPIFormulaVersao conforme RN-RF044-11
- **FP-UC01-010:** Sistema registra auditoria
- **FP-UC01-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Testar fórmula antes de salvar (dry-run com timeout 5s)
- **FA-UC01-002:** Salvar em draft para completar depois
- **FA-UC01-003:** Cancelar criação

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado → erro de unicidade (400)
- **FE-UC01-002:** Fórmula SQL inválida → erro de validação com detalhe do erro SQL (400)
- **FE-UC01-003:** Periodicidade inválida para fonte de dados → erro RN-RF044-03 (400)
- **FE-UC01-004:** Timeout na validação da fórmula (>5s) → alerta e salva em draft

### Regras de Negócio
- RN-RF044-01: Código único formato KPI-{CATEGORIA}-{SEQUENCIAL}
- RN-RF044-02: Fórmula SQL válida retornando valor numérico
- RN-RF044-03: Periodicidade mínima por fonte (API externa: min 1h, Banco: min 5min)
- RN-RF044-11: Alteração de fórmula cria nova versão

### Critérios de Aceite
- **CA-UC01-001:** Código DEVE seguir formato KPI-{CATEGORIA}-{SEQUENCIAL}
- **CA-UC01-002:** Fórmula DEVE ser SQL válido que retorna valor numérico
- **CA-UC01-003:** Sistema DEVE executar dry-run da fórmula com timeout de 5s
- **CA-UC01-004:** tenant_id DEVE ser preenchido automaticamente
- **CA-UC01-005:** created_by DEVE ser preenchido automaticamente
- **CA-UC01-006:** Estado inicial DEVE ser "draft"
- **CA-UC01-007:** Versão 1.0 da fórmula DEVE ser criada em KPIFormulaVersao

---

## UC02 — Visualizar KPI

### Objetivo
Permitir visualização detalhada de um KPI com histórico, drill-down e análise de tendências.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.LISTAR`
- Permissão de categoria correspondente

### Pós-condições
- Detalhes exibidos com gráfico de evolução e drill-down habilitado

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona KPI na lista
- **FP-UC02-002:** Sistema valida permissão GES.KPI.LISTAR
- **FP-UC02-003:** Sistema valida permissão de categoria
- **FP-UC02-004:** Sistema valida tenant
- **FP-UC02-005:** Sistema exibe detalhes: Código, Nome, Descrição, Categoria, Fórmula, Periodicidade, Responsável
- **FP-UC02-006:** Sistema calcula semáforo conforme RN-RF044-05
- **FP-UC02-007:** Sistema carrega histórico de 12 meses de KPIHistorico
- **FP-UC02-008:** Sistema exibe gráfico de evolução (ApexCharts linha)
- **FP-UC02-009:** Sistema habilita drill-down conforme RN-RF044-08

### Fluxos Alternativos
- **FA-UC02-001:** Drill-down para transação individual (RN-RF044-08)
- **FA-UC02-002:** Visualizar histórico de versões de fórmula
- **FA-UC02-003:** Comparar com período anterior (MoM, YoY)
- **FA-UC02-004:** Visualizar eventos marcados (mudanças fórmula, ações corretivas)

### Fluxos de Exceção
- **FE-UC02-001:** KPI inexistente → 404
- **FE-UC02-002:** KPI de outro tenant → 404
- **FE-UC02-003:** Sem permissão de categoria → 403

### Regras de Negócio
- RN-RF044-05: Semáforo automático baseado em % atingimento meta
- RN-RF044-08: Drill-down até transação individual obrigatório
- RN-RF044-15: Histórico de 7 anos conforme LGPD

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar KPIs do próprio tenant
- **CA-UC02-002:** Permissão de categoria DEVE ser validada
- **CA-UC02-003:** Gráfico de evolução DEVE exibir 12 meses de histórico
- **CA-UC02-004:** Drill-down DEVE permitir navegação até transação individual
- **CA-UC02-005:** Auditoria de criação/edição DEVE ser exibida

---

## UC03 — Editar KPI

### Objetivo
Permitir alteração controlada de um KPI com versionamento de fórmula.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.EDITAR`
- KPI em estado "draft", "active" ou "inactive"

### Pós-condições
- KPI atualizado
- Nova versão de fórmula criada (se alterada)
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição
- **FP-UC03-002:** Sistema valida permissão GES.KPI.EDITAR
- **FP-UC03-003:** Sistema valida tenant
- **FP-UC03-004:** Sistema carrega dados atuais
- **FP-UC03-005:** Usuário altera dados
- **FP-UC03-006:** SE fórmula foi alterada ENTÃO sistema valida nova fórmula conforme RN-RF044-02
- **FP-UC03-007:** SE fórmula foi alterada ENTÃO sistema cria nova versão em KPIFormulaVersao conforme RN-RF044-11
- **FP-UC03-008:** Sistema persiste alterações
- **FP-UC03-009:** Sistema registra auditoria com estado anterior e novo
- **FP-UC03-010:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Testar nova fórmula antes de salvar
- **FA-UC03-002:** Cancelar edição

### Fluxos de Exceção
- **FE-UC03-001:** Nova fórmula inválida → erro de validação (400)
- **FE-UC03-002:** KPI em estado "deleted" → não pode ser editado (400)
- **FE-UC03-003:** Timeout na validação da fórmula → erro (408)

### Regras de Negócio
- RN-RF044-02: Validação de fórmula SQL
- RN-RF044-11: Alteração de fórmula cria nova versão automaticamente
- RN-RF044-09: Recálculo automático será executado após edição se KPI estiver "active"

### Critérios de Aceite
- **CA-UC03-001:** updated_by DEVE ser preenchido automaticamente
- **CA-UC03-002:** updated_at DEVE ser preenchido automaticamente
- **CA-UC03-003:** SE fórmula alterada ENTÃO nova versão DEVE ser criada em KPIFormulaVersao
- **CA-UC03-004:** SE fórmula alterada E KPI "active" ENTÃO recálculo DEVE ser agendado (Hangfire)
- **CA-UC03-005:** Auditoria DEVE registrar campos alterados
- **CA-UC03-006:** Tentativa de editar KPI de outro tenant DEVE retornar 404

---

## UC04 — Excluir KPI

### Objetivo
Permitir exclusão lógica de KPI com transição de estado para "deleted".

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.EXCLUIR`
- KPI em estado "draft", "active" ou "inactive"

### Pós-condições
- KPI marcado como excluído (estado "deleted")
- Jobs de cálculo automático desabilitados
- Histórico preservado

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita exclusão
- **FP-UC04-002:** Sistema exibe confirmação
- **FP-UC04-003:** Usuário confirma
- **FP-UC04-004:** Sistema valida permissão GES.KPI.EXCLUIR
- **FP-UC04-005:** Sistema valida tenant
- **FP-UC04-006:** Sistema verifica dependências (dashboards, alertas)
- **FP-UC04-007:** Sistema executa soft delete (FlExcluido = true, estado = "deleted")
- **FP-UC04-008:** Sistema desabilita jobs Hangfire de recálculo
- **FP-UC04-009:** Sistema registra auditoria
- **FP-UC04-010:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
- **FA-UC04-002:** Visualizar dependências antes de confirmar

### Fluxos de Exceção
- **FE-UC04-001:** KPI usado em dashboards ativos → erro com lista de dependências (400)
- **FE-UC04-002:** KPI usado em alertas ativos → erro com lista de dependências (400)
- **FE-UC04-003:** KPI já excluído → erro (400)

### Regras de Negócio
- RN-RF044-15: Histórico DEVE ser preservado por 7 anos
- Soft delete padrão do sistema

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete)
- **CA-UC04-002:** Estado DEVE ser alterado para "deleted"
- **CA-UC04-003:** Jobs Hangfire DEVEM ser desabilitados
- **CA-UC04-004:** Histórico em KPIHistorico DEVE ser preservado
- **CA-UC04-005:** Sistema DEVE verificar dependências ANTES de permitir exclusão
- **CA-UC04-006:** KPI excluído NÃO deve aparecer em listagens padrão

---

## UC05 — Definir Metas

### Objetivo
Permitir definição de metas hierárquicas (mínima, ideal, desafiadora) com validação de agregação.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.META.DEFINIR`
- KPI existente em qualquer estado

### Pós-condições
- Metas criadas/atualizadas em KPIMeta
- Semáforo recalculado
- Auditoria registrada

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa tela de metas do KPI
- **FP-UC05-002:** Sistema valida permissão GES.KPI.META.DEFINIR
- **FP-UC05-003:** Sistema valida tenant
- **FP-UC05-004:** Sistema exibe formulário: Meta_Mínima*, Meta_Ideal*, Meta_Desafiadora*, Período*, Meta_Pai (se aplicável)
- **FP-UC05-005:** Usuário informa valores
- **FP-UC05-006:** Sistema valida hierarquia conforme RN-RF044-04 (soma filhas ≤ 100% pai)
- **FP-UC05-007:** Sistema valida lógica: Meta_Mínima < Meta_Ideal < Meta_Desafiadora
- **FP-UC05-008:** Sistema persiste metas em KPIMeta
- **FP-UC05-009:** Sistema recalcula semáforo conforme RN-RF044-05
- **FP-UC05-010:** Sistema registra auditoria
- **FP-UC05-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC05-001:** Definir metas para múltiplos períodos (mensal, trimestral, anual)
- **FA-UC05-002:** Copiar metas de período anterior
- **FA-UC05-003:** Definir metas hierárquicas (meta pai-filho)

### Fluxos de Exceção
- **FE-UC05-001:** Meta_Mínima ≥ Meta_Ideal → erro de validação (400)
- **FE-UC05-002:** Soma metas filhas > 100% meta pai → erro RN-RF044-04 (400)
- **FE-UC05-003:** Valores negativos → erro de validação (400)

### Regras de Negócio
- RN-RF044-04: Hierarquia de metas - soma filhas ≤ 100% pai
- RN-RF044-05: Semáforo automático baseado em % atingimento

### Critérios de Aceite
- **CA-UC05-001:** Meta_Mínima DEVE ser < Meta_Ideal < Meta_Desafiadora
- **CA-UC05-002:** Se meta hierárquica, soma filhas DEVE ser ≤ 100% meta pai
- **CA-UC05-003:** Semáforo DEVE ser recalculado automaticamente após definir metas
- **CA-UC05-004:** Sistema DEVE permitir metas por período (mensal, trimestral, anual)
- **CA-UC05-005:** tenant_id DEVE ser validado em toda hierarquia de metas

---

## UC06 — Configurar Alertas

### Objetivo
Permitir configuração de alertas automáticos por threshold, tendência e anomalia.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.ALERTA.CONFIGURAR`
- KPI existente com meta definida

### Pós-condições
- Alerta configurado em KPIAlerta
- Jobs Hangfire agendados
- Auditoria registrada

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa configuração de alertas
- **FP-UC06-002:** Sistema valida permissão GES.KPI.ALERTA.CONFIGURAR
- **FP-UC06-003:** Sistema valida tenant
- **FP-UC06-004:** Sistema exibe formulário: Tipo* (Threshold/Tendência/Anomalia), Condição*, Destinatários*, Cooldown*
- **FP-UC06-005:** Usuário configura alerta
- **FP-UC06-006:** Sistema valida cooldown mínimo 1 hora conforme RN-RF044-10
- **FP-UC06-007:** Sistema valida configuração de tendência conforme RN-RF044-06 (3 dias antecedência)
- **FP-UC06-008:** Sistema valida configuração de anomalia conforme RN-RF044-07 (|z-score| > 3)
- **FP-UC06-009:** Sistema persiste em KPIAlerta
- **FP-UC06-010:** Sistema agenda job Hangfire de verificação
- **FP-UC06-011:** Sistema registra auditoria
- **FP-UC06-012:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC06-001:** Testar alerta (envio manual)
- **FA-UC06-002:** Configurar múltiplos destinatários
- **FA-UC06-003:** Configurar escalonamento (se vermelho por 7 dias)

### Fluxos de Exceção
- **FE-UC06-001:** Cooldown < 1 hora → erro RN-RF044-10 (400)
- **FE-UC06-002:** KPI sem meta definida → erro "Meta obrigatória para alertas" (400)
- **FE-UC06-003:** Destinatários inválidos → erro de validação (400)

### Regras de Negócio
- RN-RF044-06: Alerta de tendência dispara com 3 dias de antecedência
- RN-RF044-07: Anomalia estatística se |z-score| > 3
- RN-RF044-10: Cooldown mínimo 1 hora entre alertas iguais

### Critérios de Aceite
- **CA-UC06-001:** Cooldown DEVE ser mínimo 1 hora
- **CA-UC06-002:** Alerta de tendência DEVE disparar 3 dias antes da meta
- **CA-UC06-003:** Alerta de anomalia DEVE usar z-score > 3 (ou < -3)
- **CA-UC06-004:** Sistema DEVE evitar spam respeitando cooldown
- **CA-UC06-005:** Job Hangfire DEVE ser criado para verificação periódica
- **CA-UC06-006:** tenant_id DEVE ser validado

---

## UC07 — Visualizar Dashboard

### Objetivo
Permitir visualização de dashboard executivo customizado com KPIs, gráficos e drill-down.

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.DASHBOARD`
- Permissões de categoria correspondentes

### Pós-condições
- Dashboard exibido com atualização em tempo real (SignalR)

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa dashboard de KPIs
- **FP-UC07-002:** Sistema valida permissão GES.KPI.DASHBOARD
- **FP-UC07-003:** Sistema valida permissões de categoria (RBAC)
- **FP-UC07-004:** Sistema carrega configuração do dashboard em KPIDashboard
- **FP-UC07-005:** Sistema aplica agregação conforme RN-RF044-14 (SUM, AVG, MAX, MIN)
- **FP-UC07-006:** Sistema exibe cards com KPIs principais (valor, meta, semáforo)
- **FP-UC07-007:** Sistema exibe gráficos de tendência (ApexCharts)
- **FP-UC07-008:** Sistema exibe alertas críticos
- **FP-UC07-009:** Sistema habilita atualização real-time via SignalR

### Fluxos Alternativos
- **FA-UC07-001:** Filtrar por categoria
- **FA-UC07-002:** Filtrar por período
- **FA-UC07-003:** Personalizar layout (arrastar/soltar cards)
- **FA-UC07-004:** Gerar link público com token JWT conforme RN-RF044-13
- **FA-UC07-005:** Drill-down de card para detalhes do KPI

### Fluxos de Exceção
- **FE-UC07-001:** Nenhum KPI configurado → estado vazio
- **FE-UC07-002:** Sem permissão de categoria → apenas KPIs permitidos exibidos

### Regras de Negócio
- RN-RF044-13: Dashboard público via token JWT temporário (1-30 dias)
- RN-RF044-14: Agregação inteligente (SUM, AVG, MAX, MIN) conforme tipo de KPI

### Critérios de Aceite
- **CA-UC07-001:** Dashboard DEVE respeitar RBAC por categoria
- **CA-UC07-002:** Atualização real-time DEVE usar SignalR
- **CA-UC07-003:** Agregação DEVE usar operação apropriada (SUM, AVG, MAX, MIN)
- **CA-UC07-004:** Link público DEVE gerar token JWT com validade configurável (1-30 dias)
- **CA-UC07-005:** Drill-down DEVE navegar para UC02 (Visualizar KPI)
- **CA-UC07-006:** tenant_id DEVE ser validado em todos os KPIs exibidos

---

## UC08 — Exportar KPIs

### Objetivo
Permitir exportação de KPIs e histórico para formatos externos (Power BI, Tableau, Excel, PDF).

### Pré-condições
- Usuário autenticado
- Permissão `GES.KPI.EXPORTAR`
- Permissões de categoria correspondentes

### Pós-condições
- Arquivo gerado e disponibilizado para download

### Fluxo Principal
- **FP-UC08-001:** Usuário solicita exportação
- **FP-UC08-002:** Sistema valida permissão GES.KPI.EXPORTAR
- **FP-UC08-003:** Sistema valida permissões de categoria
- **FP-UC08-004:** Sistema valida tenant
- **FP-UC08-005:** Usuário seleciona formato (Power BI OData / Tableau API / Excel / PDF)
- **FP-UC08-006:** Usuário seleciona período e KPIs
- **FP-UC08-007:** Sistema aplica filtro RBAC por categoria
- **FP-UC08-008:** Sistema gera arquivo conforme formato
- **FP-UC08-009:** Sistema respeita retenção de 7 anos conforme RN-RF044-15
- **FP-UC08-010:** Sistema registra auditoria
- **FP-UC08-011:** Sistema disponibiliza download

### Fluxos Alternativos
- **FA-UC08-001:** Agendar exportação recorrente
- **FA-UC08-002:** Exportar para endpoint OData (Power BI)
- **FA-UC08-003:** Exportar via API customizada (Tableau)
- **FA-UC08-004:** Incluir drill-down detalhado no Excel

### Fluxos de Exceção
- **FE-UC08-001:** Período solicitado > 7 anos → erro RN-RF044-15 (400)
- **FE-UC08-002:** Sem permissão para categoria → KPIs filtrados
- **FE-UC08-003:** Erro na geração do arquivo → erro 500

### Regras de Negócio
- RN-RF044-15: Retenção de dados de 7 anos conforme LGPD
- RBAC por categoria aplicado na exportação

### Critérios de Aceite
- **CA-UC08-001:** Exportação DEVE respeitar RBAC por categoria
- **CA-UC08-002:** Período máximo de exportação DEVE ser 7 anos
- **CA-UC08-003:** Excel DEVE incluir múltiplas abas (KPIs, Histórico, Metas, Alertas)
- **CA-UC08-004:** PDF DEVE incluir gráficos visuais
- **CA-UC08-005:** Power BI DEVE usar endpoint OData padrão
- **CA-UC08-006:** Tableau DEVE usar conector API customizado
- **CA-UC08-007:** tenant_id DEVE ser validado em todos os dados exportados

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio |
|----|------------------|
| UC00 | RN-RF044-12, RN-RF044-15, RN-RF044-05 |
| UC01 | RN-RF044-01, RN-RF044-02, RN-RF044-03, RN-RF044-11 |
| UC02 | RN-RF044-05, RN-RF044-08, RN-RF044-15 |
| UC03 | RN-RF044-02, RN-RF044-11, RN-RF044-09 |
| UC04 | RN-RF044-15 |
| UC05 | RN-RF044-04, RN-RF044-05 |
| UC06 | RN-RF044-06, RN-RF044-07, RN-RF044-10 |
| UC07 | RN-RF044-13, RN-RF044-14 |
| UC08 | RN-RF044-15 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - adequada aos templates oficiais |
| 1.0 | 2025-12-18 | Equipe IControlIT | Versão inicial com estrutura resumida |

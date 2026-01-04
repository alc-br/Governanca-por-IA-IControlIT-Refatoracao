# RL-RF092 — Referência ao Legado (Garantias e Seguros Contratuais)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Code

**RF Moderno Relacionado:** RF-092 - Gestão Completa de Garantias e Seguros Contratuais
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server 2019
**Objetivo:** Documentar o comportamento do sistema legado que serve de base para a refatoração, garantindo rastreabilidade histórica e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica WebForms (ASP.NET)
- **Linguagem / Stack**: VB.NET + ASP.NET Web Forms
- **Banco de Dados**: SQL Server 2019 (banco `bdb_icontrolit` - um por cliente)
- **Multi-tenant**: Não (banco separado por cliente)
- **Auditoria**: Parcial (apenas campos `id_usuario_criacao` e `dh_criacao`, sem IP ou dados antes/depois)
- **Configurações**: Web.config + tabelas no SQL Server

### 1.2 Problemas Arquiteturais Identificados

1. **Ausência de Multi-tenancy Moderno**: Cada cliente possui banco separado (multi-database), dificultando consolidação de dados e relatórios agregados
2. **Auditoria Incompleta**: Não registra IP, User-Agent, dados antes/depois de alterações (não conforme SOX/LGPD)
3. **Stored Procedures Complexas**: Lógica de negócio misturada com SQL (dificulta testes e manutenção)
4. **Sem Versionamento de Apólices**: Alterações sobrescrevem dados anteriores (perde histórico de prêmios)
5. **Alertas de Vencimento Manuais**: Não há job automático, gestores precisavam verificar manualmente relatórios SSRS
6. **Workflow de Sinistros Inexistente**: Não há estados ou transições formais (apenas campo `tp_status` livre)
7. **Integração com Seguradoras Manual**: Não há API REST, sincronização feita via planilhas Excel
8. **Dashboard Estático**: Relatórios SSRS sem interatividade, sem refresh em tempo real

---

## 2. TELAS DO LEGADO

### 2.1 Tela: GarantiaConsulta.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/GarantiaConsulta.aspx`

**Funcionalidade Principal**: Listagem de garantias contratuais com filtros básicos (ativo, contrato, tipo, vigência).

**Comportamentos Implícitos**:
- Paginação manual via ViewState (não via query params)
- Filtros aplicados apenas no lado servidor (postback completo)
- Ordenação por coluna com postback
- Sem indicação visual de status (ativa/vencida)
- Exportação para Excel via SSRS (não via endpoint)

**Regras Implícitas**:
- RL-RN-001: Garantias só podiam ser visualizadas se `fl_ativo = 1` (soft delete não aparecia)
- RL-RN-002: Filtro por cliente era implícito (baseado em banco de dados conectado)

**Destino**: **SUBSTITUÍDO** - Tela Angular `/garantias` com grid interativo, filtros client-side, exportação via endpoint REST

---

### 2.2 Tela: GarantiaDetalhe.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/GarantiaDetalhe.aspx`

**Funcionalidade Principal**: Criação e edição de garantias com validação básica.

**Comportamentos Implícitos**:
- Validação de data fim > data início no code-behind VB.NET
- Campos obrigatórios validados com `RequiredFieldValidator`
- Não validava overlap de períodos (permitia duplicação de cobertura)
- Salvar e voltar para listagem (sem mensagem toast)

**Regras Implícitas**:
- RL-RN-003: Campo `vl_cobertura` era opcional (poderia ser NULL)
- RL-RN-004: Não validava se ativo existia (FK sem validação programática)

**Destino**: **SUBSTITUÍDO** - Component Angular `/garantias/{id}` com validação assíncrona, FluentValidation no backend

---

### 2.3 Tela: ApoliceConsulta.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/ApoliceConsulta.aspx`

**Funcionalidade Principal**: Listagem de apólices de seguro com filtros por segurador, status, vigência.

**Comportamentos Implícitos**:
- Status derivado manualmente (comparação de datas no SQL)
- Não havia badge visual para apólices vencidas
- Exportação limitada a 1000 registros (hardcoded)

**Regras Implícitas**:
- RL-RN-005: Apólices com `fl_ativo = 0` não apareciam (soft delete escondido)
- RL-RN-006: Constraint `UQ_apolice_numero_segurador` garantia unicidade

**Destino**: **SUBSTITUÍDO** - Component Angular `/apolices` com paginação server-side, badges de status

---

### 2.4 Tela: ApoliceDetalhe.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/ApoliceDetalhe.aspx`

**Funcionalidade Principal**: Criação e edição de apólices com dados de coberturas.

**Comportamentos Implícitos**:
- Campo `tx_coberturas` era texto livre (VARCHAR(max)), sem estrutura JSON
- Validação de franquia < limite máximo no code-behind
- Cálculo de prêmio anual (mensal * 12) feito no frontend (JavaScript)

**Regras Implícitas**:
- RL-RN-007: Data vigência início <= data vigência fim (validação VB.NET)
- RL-RN-008: Número de apólice único por segurador (constraint SQL)

**Destino**: **SUBSTITUÍDO** - Component Angular `/apolices/{id}` com validação FluentValidation, coberturas estruturadas JSON

---

### 2.5 Tela: SinistroConsulta.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/SinistroConsulta.aspx`

**Funcionalidade Principal**: Listagem de sinistros por status (Solicitação, Análise, Aprovação, Pagamento, Recusado).

**Comportamentos Implícitos**:
- Grid com cores diferentes por status (hardcoded CSS)
- Filtro por período de ocorrência (date range picker)
- Botão "Analisar" visível apenas para usuários com perfil "Gerente Seguros"

**Regras Implícitas**:
- RL-RN-009: Status era enum livre (sem transições formais)
- RL-RN-010: Recusados podiam ser reabertos (sem validação de estado final)

**Destino**: **SUBSTITUÍDO** - Component Angular `/sinistros` com máquina de estados formal, workflow estruturado

---

### 2.6 Tela: SinistroNovo.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/SinistroNovo.aspx`

**Funcionalidade Principal**: Registro de novo sinistro vinculado a apólice.

**Comportamentos Implícitos**:
- Dropdown de apólices carregava TODAS as apólices (sem filtro por vigência)
- Validação de data ocorrência dentro da vigência no code-behind
- Campos de análise (parecer) desabilitados na criação

**Regras Implícitas**:
- RL-RN-011: Sinistro criado com status "Solicitacao" automaticamente
- RL-RN-012: Valor estimado podia ser NULL (não obrigatório)

**Destino**: **SUBSTITUÍDO** - Component Angular `/sinistros/novo` com dropdown filtrado (apenas apólices vigentes)

---

### 2.7 Tela: Dashboard.aspx

**Caminho**: `ic1_legado/IControlIT/Garantias/Dashboard.aspx`

**Funcionalidade Principal**: Dashboard com KPIs de cobertura ativa, sinistros pendentes, índice de sinistralidade.

**Comportamentos Implícitos**:
- Dados carregados via stored procedures (sem cache)
- Refresh manual (botão "Atualizar")
- Gráficos em imagem estática (SSRS Chart)
- Sem drill-down (não clicável)

**Regras Implícitas**:
- RL-RN-013: KPIs calculados em tempo de renderização (lento para grandes volumes)
- RL-RN-014: Não havia filtro por período (sempre últimos 30 dias hardcoded)

**Destino**: **SUBSTITUÍDO** - Component Angular `/dashboard/seguros` com ApexCharts, SignalR real-time

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: WSGarantias.asmx

**Caminho**: `ic1_legado/IControlIT/Garantias/WebService/WSGarantias.asmx.vb`

**Métodos Públicos**:

#### 3.1.1 ListarGarantias()
```vb
<WebMethod()>
Public Function ListarGarantias(idCliente As Integer, idAtivo As Integer?) As DataTable
```
**Descrição**: Retorna lista de garantias com filtros opcionais por ativo. Sem paginação (retorna todas).

**Parâmetros**:
- `idCliente` (int) - ID do cliente (obrigatório)
- `idAtivo` (int?) - ID do ativo (opcional)

**Retorno**: DataTable com colunas `id_garantia`, `tp_garantia`, `dh_data_inicio`, `dh_data_fim`, `vl_cobertura`

**Destino**: **SUBSTITUÍDO** - Endpoint `GET /api/garantias?clienteId={id}&idAtivo={id}`

---

#### 3.1.2 GetGarantiaById(id)
```vb
<WebMethod()>
Public Function GetGarantiaById(id As Integer) As GarantiaDTO
```
**Descrição**: Retorna garantia específica por ID.

**Destino**: **SUBSTITUÍDO** - Endpoint `GET /api/garantias/{id}`

---

#### 3.1.3 CriarGarantia(obj)
```vb
<WebMethod()>
Public Function CriarGarantia(obj As GarantiaDTO) As Integer
```
**Descrição**: Cria nova garantia e retorna ID gerado.

**Validações**:
- Data fim > data início
- Ativo existe
- Tipo garantia é válido ("Fabricante", "Estendida", "Condicional")

**Destino**: **SUBSTITUÍDO** - Endpoint `POST /api/garantias`

---

#### 3.1.4 AtualizarGarantia(id, obj)
```vb
<WebMethod()>
Public Function AtualizarGarantia(id As Integer, obj As GarantiaDTO) As Boolean
```
**Descrição**: Atualiza garantia existente. Não cria versão histórica (sobrescreve).

**Destino**: **SUBSTITUÍDO** - Endpoint `PUT /api/garantias/{id}` com auditoria completa

---

#### 3.1.5 ExcluirGarantia(id)
```vb
<WebMethod()>
Public Function ExcluirGarantia(id As Integer) As Boolean
```
**Descrição**: Soft delete (marca `fl_ativo = 0`).

**Destino**: **SUBSTITUÍDO** - Endpoint `DELETE /api/garantias/{id}`

---

#### 3.1.6 VerificaVencimento()
```vb
<WebMethod()>
Public Function VerificaVencimento(dias As Integer) As DataTable
```
**Descrição**: Retorna garantias vencendo em N dias.

**Destino**: **SUBSTITUÍDO** - Endpoint `GET /api/garantias/vencimento/proximas?dias={n}`

---

#### 3.1.7 RegistrarSinistro(obj)
```vb
<WebMethod()>
Public Function RegistrarSinistro(obj As SinistroDTO) As Integer
```
**Descrição**: Cria novo sinistro vinculado a apólice.

**Validações**:
- Apólice existe
- Apólice está vigente
- Data ocorrência dentro da vigência

**Destino**: **SUBSTITUÍDO** - Endpoint `POST /api/sinistros`

---

#### 3.1.8 AtualizarStatusSinistro(id, status)
```vb
<WebMethod()>
Public Function AtualizarStatusSinistro(id As Integer, status As String) As Boolean
```
**Descrição**: Atualiza status do sinistro sem validação de transição de estados.

**Problema**: Permitia transições inválidas (ex: Recusado → Aprovação)

**Destino**: **SUBSTITUÍDO** - Endpoint `PATCH /api/sinistros/{id}/status` com máquina de estados formal

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: tb_garantia_contratual

**Caminho**: `[bdb_icontrolit].[dbo].[tb_garantia_contratual]`

**Finalidade**: Armazenar garantias contratuais de ativos.

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[tb_garantia_contratual](
    [id_garantia] [int] IDENTITY(1,1) NOT NULL,
    [id_ativo] [int] NOT NULL,
    [id_contrato] [int] NULL,
    [tp_garantia] [varchar](30) NOT NULL,
    [dh_data_inicio] [datetime] NOT NULL,
    [dh_data_fim] [datetime] NOT NULL,
    [tx_descricao] [varchar](255) NULL,
    [vl_cobertura] [numeric](13,2) NULL,
    [fl_ativo] [bit] DEFAULT 1,
    [id_usuario_criacao] [int],
    [dh_criacao] [datetime] DEFAULT GETDATE(),
    CONSTRAINT [PK_garantia_contratual] PRIMARY KEY CLUSTERED ([id_garantia] ASC),
    CONSTRAINT [FK_garantia_ativo] FOREIGN KEY ([id_ativo]) REFERENCES [dbo].[tb_ativo] ([id_ativo])
)
```

**Problemas Identificados**:
- ❌ Sem multi-tenancy (ClienteId ausente)
- ❌ Auditoria incompleta (sem `LastModified`, `LastModifiedBy`, IP)
- ❌ Chave primária INT (não GUID)
- ❌ Sem índice para queries de vencimento (`dh_data_fim`)
- ❌ Campo `tp_garantia` é varchar livre (não enum)
- ❌ Sem constraint para validar datas (data_fim > data_inicio)

**Destino**: **SUBSTITUÍDO** - Tabela `Garantia` com GUID, multi-tenancy, auditoria completa

---

### 4.2 Tabela: tb_apolice_seguro

**Caminho**: `[bdb_icontrolit].[dbo].[tb_apolice_seguro]`

**Finalidade**: Armazenar apólices de seguro com dados de coberturas.

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[tb_apolice_seguro](
    [id_apolice] [int] IDENTITY(1,1) NOT NULL,
    [nr_apolice] [varchar](50) NOT NULL,
    [id_segurador] [int] NOT NULL,
    [id_ativo] [int] NULL,
    [id_contrato] [int] NULL,
    [dh_data_emissao] [datetime] NOT NULL,
    [dh_data_vigencia_inicio] [datetime] NOT NULL,
    [dh_data_vigencia_fim] [datetime] NOT NULL,
    [vl_limite_maximo] [numeric](13,2) NOT NULL,
    [vl_franquia] [numeric](13,2) NULL,
    [vl_premio_mensal] [numeric](13,2) NULL,
    [tp_status] [varchar](20) DEFAULT 'Ativa',
    [tx_coberturas] [varchar](max) NULL,
    [fl_ativo] [bit] DEFAULT 1,
    [id_usuario_criacao] [int],
    [dh_criacao] [datetime] DEFAULT GETDATE(),
    CONSTRAINT [PK_apolice_seguro] PRIMARY KEY CLUSTERED ([id_apolice] ASC),
    CONSTRAINT [FK_apolice_ativo] FOREIGN KEY ([id_ativo]) REFERENCES [dbo].[tb_ativo] ([id_ativo]),
    CONSTRAINT [UQ_apolice_numero_segurador] UNIQUE ([nr_apolice], [id_segurador])
)
```

**Problemas Identificados**:
- ❌ Campo `tx_coberturas` é texto livre (não estruturado JSON)
- ❌ Sem multi-tenancy (ClienteId ausente)
- ❌ Sem criptografia de `nr_apolice` (dado sensível)
- ❌ Status VARCHAR livre (não enum)
- ❌ Sem auditoria completa (LastModified ausente)
- ❌ Sem índice para queries de renovação (`dh_data_vigencia_fim`)

**Destino**: **SUBSTITUÍDO** - Tabela `Apolice` com JSON estruturado, criptografia, auditoria

---

### 4.3 Tabela: tb_sinistro

**Caminho**: `[bdb_icontrolit].[dbo].[tb_sinistro]`

**Finalidade**: Registrar sinistros de apólices de seguro.

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[tb_sinistro](
    [id_sinistro] [int] IDENTITY(1,1) NOT NULL,
    [id_apolice] [int] NOT NULL,
    [dh_data_ocorrencia] [datetime] NOT NOT NULL,
    [tp_sinistro] [varchar](30) NOT NULL,
    [vl_estimado] [numeric](13,2) NULL,
    [vl_pago] [numeric](13,2) NULL,
    [tp_status] [varchar](20) DEFAULT 'Solicitacao',
    [tx_parecer_analista] [varchar](max) NULL,
    [id_autorizador] [int] NULL,
    [dh_data_autorizacao] [datetime] NULL,
    [fl_ativo] [bit] DEFAULT 1,
    [id_usuario_criacao] [int],
    [dh_criacao] [datetime] DEFAULT GETDATE(),
    CONSTRAINT [PK_sinistro] PRIMARY KEY CLUSTERED ([id_sinistro] ASC),
    CONSTRAINT [FK_sinistro_apolice] FOREIGN KEY ([id_apolice]) REFERENCES [dbo].[tb_apolice_seguro] ([id_apolice])
)
```

**Problemas Identificados**:
- ❌ Status VARCHAR livre (sem transições formais)
- ❌ Sem tabela de histórico de transições (perde rastreabilidade)
- ❌ Sem campos de recusa (motivo, data_recusa)
- ❌ Sem multi-tenancy (ClienteId ausente)
- ❌ Chave primária INT (não GUID)
- ❌ Tipo sinistro VARCHAR livre (não enum)

**Destino**: **SUBSTITUÍDO** - Tabela `Sinistro` com enum Status, tabela `SinistroHistorico` para transições

---

## 5. STORED PROCEDURES LEGADAS

### 5.1 Procedure: pa_garantia_listar

**Caminho**: `ic1_legado/Database/Procedures/pa_garantia_listar.sql`

**Parâmetros**:
- `@id_cliente INT`
- `@id_ativo INT = NULL`
- `@tp_garantia VARCHAR(30) = NULL`
- `@fl_vencidas BIT = 0`

**Lógica Principal**:
```sql
SELECT
    g.id_garantia,
    g.id_ativo,
    a.ds_nome_ativo,
    g.tp_garantia,
    g.dh_data_inicio,
    g.dh_data_fim,
    g.vl_cobertura,
    CASE
        WHEN GETDATE() > g.dh_data_fim THEN 'Vencida'
        WHEN DATEDIFF(DAY, GETDATE(), g.dh_data_fim) <= 30 THEN 'ProximoVencer'
        ELSE 'Ativa'
    END AS status_calculado
FROM tb_garantia_contratual g
INNER JOIN tb_ativo a ON g.id_ativo = a.id_ativo
WHERE g.fl_ativo = 1
    AND (@id_ativo IS NULL OR g.id_ativo = @id_ativo)
    AND (@tp_garantia IS NULL OR g.tp_garantia = @tp_garantia)
    AND (@fl_vencidas = 0 OR GETDATE() > g.dh_data_fim)
ORDER BY g.dh_data_fim DESC
```

**Destino**: **SUBSTITUÍDO** - Query LINQ em `GetGarantiasQueryHandler` com paginação server-side

---

### 5.2 Procedure: pa_garantia_vencimento_30_dias

**Caminho**: `ic1_legado/Database/Procedures/pa_garantia_vencimento_30_dias.sql`

**Lógica Principal**:
```sql
SELECT
    g.id_garantia,
    g.id_ativo,
    a.ds_nome_ativo,
    g.dh_data_fim,
    DATEDIFF(DAY, GETDATE(), g.dh_data_fim) AS dias_restantes
FROM tb_garantia_contratual g
INNER JOIN tb_ativo a ON g.id_ativo = a.id_ativo
WHERE g.fl_ativo = 1
    AND g.dh_data_fim BETWEEN GETDATE() AND DATEADD(DAY, 30, GETDATE())
ORDER BY g.dh_data_fim ASC
```

**Destino**: **SUBSTITUÍDO** - Job Hangfire `ProcessarAlertasVencimentoJob` com marcos 90/60/30/15 dias

---

### 5.3 Procedure: pa_sinistro_por_apolice

**Caminho**: `ic1_legado/Database/Procedures/pa_sinistro_por_apolice.sql`

**Parâmetros**: `@id_apolice INT`

**Lógica Principal**:
```sql
SELECT
    s.id_sinistro,
    s.dh_data_ocorrencia,
    s.tp_sinistro,
    s.vl_estimado,
    s.vl_pago,
    s.tp_status,
    s.tx_parecer_analista,
    u.ds_nome AS nome_autorizador
FROM tb_sinistro s
LEFT JOIN tb_usuario u ON s.id_autorizador = u.id_usuario
WHERE s.id_apolice = @id_apolice
    AND s.fl_ativo = 1
ORDER BY s.dh_data_ocorrencia DESC
```

**Destino**: **SUBSTITUÍDO** - Query `GetSinistrosByApoliceQuery` com DTO estruturado

---

### 5.4 Procedure: pa_apolice_renovar

**Caminho**: `ic1_legado/Database/Procedures/pa_apolice_renovar.sql`

**Lógica Principal** (executada manualmente):
```sql
INSERT INTO tb_apolice_seguro (
    nr_apolice,
    id_segurador,
    id_ativo,
    dh_data_vigencia_inicio,
    dh_data_vigencia_fim,
    vl_limite_maximo,
    vl_franquia,
    vl_premio_mensal,
    tp_status
)
SELECT
    nr_apolice + '-REN',
    id_segurador,
    id_ativo,
    DATEADD(DAY, 1, dh_data_vigencia_fim),
    DATEADD(YEAR, 1, dh_data_vigencia_fim),
    vl_limite_maximo,
    vl_franquia,
    vl_premio_mensal,
    'Ativa'
FROM tb_apolice_seguro
WHERE dh_data_vigencia_fim = DATEADD(DAY, 30, GETDATE())
    AND tp_status = 'Ativa'
    AND fl_ativo = 1
```

**Problema**: Executada manualmente (não job automático)

**Destino**: **SUBSTITUÍDO** - Job Hangfire `RenovarApolicesJob` executado diariamente

---

### 5.5 Procedure: pa_calcula_cobertura_total

**Caminho**: `ic1_legado/Database/Procedures/pa_calcula_cobertura_total.sql`

**Parâmetros**: `@id_ativo INT`

**Lógica Principal**:
```sql
SELECT
    (
        ISNULL((SELECT SUM(vl_limite_maximo)
                FROM tb_apolice_seguro
                WHERE id_ativo = @id_ativo
                    AND GETDATE() BETWEEN dh_data_vigencia_inicio AND dh_data_vigencia_fim
                    AND fl_ativo = 1), 0) +

        ISNULL((SELECT SUM(vl_cobertura)
                FROM tb_garantia_contratual
                WHERE id_ativo = @id_ativo
                    AND GETDATE() BETWEEN dh_data_inicio AND dh_data_fim
                    AND fl_ativo = 1), 0)
    ) AS vl_cobertura_total
```

**Destino**: **SUBSTITUÍDO** - Método `ApoliceService.CalcularCoberturaTotal(string idAtivo)`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Garantias Só Visualizadas Se fl_ativo = 1

**Descrição**: Garantias com soft delete (`fl_ativo = 0`) não apareciam em listagens ou relatórios.

**Fonte**: Procedure `pa_garantia_listar` (cláusula WHERE)

**Destino**: **ASSUMIDO** - Sistema moderno mantém soft delete com auditoria completa

---

### RL-RN-002: Status de Garantia Calculado Dinamicamente

**Descrição**: Status (Ativa, Vencida, ProximoVencer) era calculado em tempo de query SQL (CASE WHEN).

**Fonte**: Procedure `pa_garantia_listar`

**Destino**: **ASSUMIDO** - RF092 mantém cálculo dinâmico via método `Garantia.ObterStatus()`

---

### RL-RN-003: Renovação de Apólice Manual

**Descrição**: Renovação de apólices não era automática, exigia execução manual de stored procedure ou tarefa do DBA.

**Fonte**: Procedure `pa_apolice_renovar` (sem job agendado)

**Destino**: **SUBSTITUÍDO** - Job Hangfire `RenovarApolicesJob` executa automaticamente 30 dias antes

---

### RL-RN-004: Sinistro Recusado Podia Ser Reaberto

**Descrição**: Não havia validação de transição de estados. Sinistro recusado podia ser movido para status anterior.

**Fonte**: Webservice `AtualizarStatusSinistro` (sem validação)

**Destino**: **SUBSTITUÍDO** - Máquina de estados formal impede transições inválidas (Recusado é estado final)

---

### RL-RN-005: Alertas de Vencimento Não Existiam

**Descrição**: Não havia job automático para notificar vencimentos. Gestores verificavam manualmente relatórios SSRS.

**Fonte**: Ausência de jobs SQL Agent ou scheduled tasks

**Destino**: **SUBSTITUÍDO** - Job `ProcessarAlertasVencimentoJob` com marcos 90/60/30/15 dias

---

### RL-RN-006: Cálculo de Prêmio Anual no Frontend

**Descrição**: Prêmio anual era calculado no JavaScript do frontend (mensal * 12), não no backend.

**Fonte**: `ApoliceDetalhe.aspx` (JavaScript)

**Destino**: **SUBSTITUÍDO** - Método `Apolice.CalcularPrêmioAnual()` no domain model

---

### RL-RN-007: Coberturas Texto Livre Sem Estrutura

**Descrição**: Campo `tx_coberturas` era VARCHAR(max) livre, sem formato JSON ou validação de estrutura.

**Fonte**: Tabela `tb_apolice_seguro.tx_coberturas`

**Destino**: **SUBSTITUÍDO** - Campo JSON estruturado com schema validado

---

### RL-RN-008: Validação de Franquia < Limite no Code-Behind

**Descrição**: Validação de franquia menor que limite máximo era feita no VB.NET code-behind da tela.

**Fonte**: `ApoliceDetalhe.aspx.vb`

**Destino**: **ASSUMIDO** - FluentValidation no backend (regra migrada para RN-GAR-092-11)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item / Funcionalidade | Existe no Legado | Existe no RF-092 Moderno | Observação |
|----------------------|------------------|-------------------------|------------|
| **CRUD de Garantias** | ✅ Sim | ✅ Sim | Modernizado com auditoria completa |
| **CRUD de Apólices** | ✅ Sim | ✅ Sim | Modernizado com criptografia de nr_apolice |
| **Gestão de Sinistros** | ✅ Parcial | ✅ Sim | Legado não tinha workflow formal |
| **Workflow de Sinistros** | ❌ Não | ✅ Sim | Estados e transições implementados (SOLIC→ANÁLISE→APROVA→PAGA) |
| **Alertas de Vencimento** | ❌ Não | ✅ Sim | Job Hangfire com marcos 90/60/30/15 dias |
| **Renovação Automática** | ❌ Não | ✅ Sim | Job Hangfire executa 30 dias antes |
| **Cálculo de Cobertura Total** | ✅ Sim | ✅ Sim | Migrado de stored procedure para service C# |
| **Multi-tenancy** | ❌ Não | ✅ Sim | Legado usava multi-database (banco por cliente) |
| **Auditoria LGPD/SOX** | ❌ Parcial | ✅ Sim | Legado só registrava user/data, não IP/dados antes/depois |
| **Integração com Seguradoras** | ❌ Não | ✅ Sim | API REST assíncrona com circuit breaker |
| **Dashboard em Tempo Real** | ❌ Não | ✅ Sim | Legado tinha SSRS estático, moderno tem SignalR + ApexCharts |
| **Validação de Overlap de Garantias** | ❌ Não | ✅ Sim | Legado permitia períodos duplicados |
| **Criptografia de Dados Sensíveis** | ❌ Não | ✅ Sim | Números de apólice criptografados (AES-256) |
| **Feature Flags** | ❌ Não | ✅ Sim | Central de Funcionalidades para habilitar/desabilitar módulos |
| **Exportação Excel** | ✅ Sim | ✅ Sim | Modernizado com endpoint REST (não SSRS) |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Abandonar Multi-Database e Migrar para Row-Level Security

**Motivo**: Legado tinha banco separado por cliente (multi-database), dificultando consolidação de dados.

**Impacto**: **Alto** - Requer migração de todos os bancos legados para banco único moderno com `ClienteId`.

**Data**: 2025-12-31

---

### Decisão 2: Implementar Workflow Formal de Sinistros

**Motivo**: Legado permitia transições inválidas de status (ex: Recusado → Aprovação).

**Impacto**: **Médio** - Adiciona complexidade com máquina de estados, mas garante rastreabilidade.

**Data**: 2025-12-31

---

### Decisão 3: Criar Jobs Hangfire para Alertas e Renovações

**Motivo**: Legado exigia intervenção manual de DBAs para renovações e alertas.

**Impacto**: **Médio** - Automatiza processos críticos, reduz erro humano.

**Data**: 2025-12-31

---

### Decisão 4: Estruturar Coberturas em JSON (Não Texto Livre)

**Motivo**: Campo `tx_coberturas` era texto livre sem validação.

**Impacto**: **Baixo** - Melhora consistência de dados e permite queries estruturadas.

**Data**: 2025-12-31

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de Dados Históricos de Sinistros** | Alto | Baixa | Script ETL validado com reconciliação pós-migração |
| **Resistência a Workflow Formal** | Médio | Média | Treinamento e documentação passo-a-passo |
| **Falha em Job de Renovação Automática** | Alto | Baixa | Monitoramento Hangfire + alertas em caso de falha |
| **Inconsistência em Cálculo de Cobertura** | Médio | Baixa | Testes comparativos stored procedure vs service C# |
| **Quebra de Integrações com Seguradoras** | Alto | Média | Circuit breaker + fallback para modo manual |
| **Performance em Queries de Vencimento** | Médio | Baixa | Índices em `DataFim` + paginação server-side |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF-092 Moderno | Status |
|----------------|--------------------------|--------|
| `tb_garantia_contratual` (tabela) | `Garantia` (entidade) | **SUBSTITUÍDO** |
| `tb_apolice_seguro` (tabela) | `Apolice` (entidade) | **SUBSTITUÍDO** |
| `tb_sinistro` (tabela) | `Sinistro` (entidade) | **SUBSTITUÍDO** |
| `pa_garantia_listar` (stored procedure) | `GetGarantiasQueryHandler` (CQRS) | **SUBSTITUÍDO** |
| `pa_apolice_renovar` (stored procedure) | `RenovarApolicesJob` (Hangfire) | **SUBSTITUÍDO** |
| `pa_calcula_cobertura_total` (stored procedure) | `ApoliceService.CalcularCoberturaTotal()` | **SUBSTITUÍDO** |
| `WSGarantias.asmx` (webservice VB.NET) | Endpoints REST API (.NET 10) | **SUBSTITUÍDO** |
| `GarantiaConsulta.aspx` (tela) | Component Angular `/garantias` | **SUBSTITUÍDO** |
| `SinistroNovo.aspx` (tela) | Component Angular `/sinistros/novo` | **SUBSTITUÍDO** |
| `Dashboard.aspx` (tela) | Component Angular `/dashboard/seguros` | **SUBSTITUÍDO** |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Criação do RL-RF092 com referências ao sistema legado | Claude Code |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code

---

[← Voltar ao RF-092](./RF092.md)

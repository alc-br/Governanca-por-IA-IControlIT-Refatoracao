# RL-RF054 - Referência ao Legado: Gestão de Lotes de Auditoria

**Versão:** 1.0
**Data:** 2025-12-30
**RF Relacionado:** RF054 v2.0
**Fase:** Fase-6-Ativos-Auditoria-Integracoes
**EPIC:** EPIC010-AUD-Auditoria-Avancada

---

## SEÇÃO 1: OBJETIVO DESTE DOCUMENTO

Este documento registra **exclusivamente** as referências ao sistema legado (ASP.NET Web Forms + VB.NET) relacionadas à funcionalidade de Gestão de Lotes de Auditoria. Serve como memória técnica histórica para:

- **Rastreabilidade**: Mapear de onde vieram os requisitos modernizados (RF054 v2.0)
- **Migração**: Identificar telas ASPX, stored procedures, WebServices e tabelas do legado que serão substituídos
- **Análise de Gap**: Comparar funcionalidade legado vs. moderno para garantir paridade funcional
- **Descomissionamento**: Planejar desligamento controlado do legado após migração completa

**IMPORTANTE**: Este documento **NÃO** especifica requisitos funcionais. Requisitos estão em [RF054.md](./RF054.md). O RL documenta **apenas o que existia** no legado.

---

## SEÇÃO 2: CONCEITOS FUNDAMENTAIS DO LEGADO

### 2.1 Arquitetura Legado

**Tecnologias**:
- **Frontend**: ASP.NET Web Forms 4.8 (ASPX + VB.NET code-behind)
- **Backend**: VB.NET com ASMX WebServices
- **Banco de Dados**: SQL Server 2014+ (stored procedures)
- **Processamento Assíncrono**: NENHUM (processamento síncrono travava tela)
- **Monitoramento**: Polling manual (refresh de página) ou relatórios estáticos SSRS

### 2.2 Diferenças Arquiteturais (Legado vs. Moderno)

| Aspecto | Legado (VB.NET + ASPX) | Modernizado (.NET 10 + Angular 19) |
|---------|------------------------|-------------------------------------|
| **Processamento de Lote** | Síncrono, tela travada | Assíncrono via Hangfire (background jobs) |
| **Monitoramento** | Sem feedback em tempo real | SignalR para atualização real-time de progresso |
| **Persistência de Jobs** | Memória do servidor (perda em restart) | Banco de dados (resiliente, recuperável) |
| **Distribuição de Carga** | Uma máquina, sem scaling | Múltiplos workers Hangfire (escalável) |
| **Notificações** | E-mail manual | Azure Service Bus + E-mail automático |
| **Reprocessamento** | Manual, sem histórico | Automático com retry policy, histórico completo |
| **Estados do Lote** | Strings em campo TEXT | State Machine (CQRS pattern) com validação |
| **Auditoria de Auditoria** | Sem rastreamento | Auditoria completa de operações de lote |
| **Dashboard** | Relatório estático SSRS | Dashboard Angular em tempo real |

### 2.3 Limitações do Legado

**Limitação 1: Processamento Síncrono**:
- **Problema**: Ao processar lote, usuário ficava esperando com tela travada até conclusão
- **Impacto**: Timeouts HTTP para lotes grandes (>1000 faturas), sessão expirava
- **Workaround Legado**: Limitar lotes a máximo 500 faturas por processamento

**Limitação 2: Sem Monitoramento em Tempo Real**:
- **Problema**: Usuário não sabia progresso do processamento
- **Impacto**: Ansiedade, múltiplos refreshes manuais da página, sobrecarga do servidor
- **Workaround Legado**: Barra de progresso fake (não refletia progresso real)

**Limitação 3: Perda de Estado em Restart**:
- **Problema**: Se servidor reiniciasse durante processamento, lote ficava em estado inconsistente
- **Impacto**: Faturas parcialmente auditadas sem rastreabilidade, necessidade de reprocessamento manual completo
- **Workaround Legado**: Script SQL manual para resetar status de lotes "travados"

**Limitação 4: Sem Retry Automático**:
- **Problema**: Se fatura falhasse durante processamento (timeout, lock, erro de rede), não havia retry
- **Impacto**: Taxa de erro alta (~15-20% de faturas falhavam), necessidade de reprocessamento manual
- **Workaround Legado**: Coordenador executava script de reprocessamento manualmente

---

## SEÇÃO 3: BANCO DE DADOS LEGADO

### 3.1 Tabelas Legado

#### Tabela: tb_AuditoriaBatch

**Descrição**: Tabela principal de lotes de auditoria no legado.

**Destino**: **SUBSTITUÍDA** → Migrada para `AuditBatch` (.NET 10)

**Estrutura**:
```sql
CREATE TABLE tb_AuditoriaBatch (
    ID_AuditoriaBatch INT PRIMARY KEY IDENTITY(1,1),
    ID_Fornecedor INT NOT NULL,
    NM_Batch NVARCHAR(200) NOT NULL,
    DS_Batch NVARCHAR(MAX),
    DT_Inicio DATETIME,
    DT_Fim DATETIME,
    QT_Faturas INT DEFAULT 0,
    QT_Processadas INT DEFAULT 0,
    ST_Lote NVARCHAR(50),  -- "Criado", "Processando", "Concluído", "Cancelado"
    ID_Auditor INT,
    ID_JobHangfire NVARCHAR(100),  -- Tentativa de usar Hangfire, nunca implementado corretamente
    VL_TotalGlosa DECIMAL(18,2) DEFAULT 0,
    PC_Progresso DECIMAL(5,2) DEFAULT 0,  -- Porcentagem fake
    DS_Erro NVARCHAR(MAX),
    DT_Criacao DATETIME DEFAULT GETDATE(),
    ID_UsuarioCriacao INT
)
```

**Problemas Identificados**:
- `ST_Lote` como string livre (permitia valores inconsistentes como "Processand0" com typo)
- Sem foreign keys para `ID_Fornecedor` e `ID_Auditor` (dados órfãos)
- `PC_Progresso` calculado manualmente de forma incorreta (não refletia progresso real)
- `ID_JobHangfire` nunca utilizado (coluna morta)
- Sem campos de auditoria (`UpdatedBy`, `UpdatedAt`, `IsDeleted`)

**Campos Mapeados**:
- `ID_AuditoriaBatch` → `AuditBatch.Id` (Guid)
- `ID_Fornecedor` → `AuditBatch.CompanyId` (Guid)
- `NM_Batch` → `AuditBatch.Name`
- `DS_Batch` → `AuditBatch.Description`
- `DT_Inicio` → `AuditBatch.StartedAt`
- `DT_Fim` → `AuditBatch.CompletedAt`
- `QT_Faturas` → `AuditBatch.TotalInvoices`
- `QT_Processadas` → `AuditBatch.ProcessedInvoices`
- `ST_Lote` → `AuditBatch.Status` (enum)
- `ID_Auditor` → `AuditBatch.AssignedAuditorId`
- `VL_TotalGlosa` → `AuditBatch.TotalGlossesValue`

#### Tabela: tb_AuditoriaBatchCriteria

**Descrição**: Armazena critérios de seleção configurados para o lote.

**Destino**: **SUBSTITUÍDA** → Migrada para `AuditBatchCriteria` (.NET 10)

**Estrutura**:
```sql
CREATE TABLE tb_AuditoriaBatchCriteria (
    ID_Criterio INT PRIMARY KEY IDENTITY(1,1),
    ID_AuditoriaBatch INT NOT NULL,
    TP_Criterio NVARCHAR(50),  -- "Periodo", "Operadora", "Filial", "Valor"
    VL_Criterio NVARCHAR(MAX)  -- JSON serializado manual (!!)
)
```

**Problemas Identificados**:
- `VL_Criterio` como JSON manual (parsing no code-behind VB.NET era propenso a erros)
- Sem tipagem forte (valores misturados em string)
- Sem validação de critérios válidos

**Campos Mapeados**:
- `ID_Criterio` → `AuditBatchCriteria.Id` (Guid)
- `ID_AuditoriaBatch` → `AuditBatchCriteria.AuditBatchId`
- `TP_Criterio` → `AuditBatchCriteria.CriteriaType` (enum)
- `VL_Criterio` → Campos individuais tipados (`StartDate`, `EndDate`, `CarrierId`, etc.)

#### Tabela: tb_AuditoriaBatchInvoices

**Descrição**: Associação many-to-many entre lotes e faturas selecionadas.

**Destino**: **SUBSTITUÍDA** → Migrada para `AuditBatchInvoice` (.NET 10)

**Estrutura**:
```sql
CREATE TABLE tb_AuditoriaBatchInvoices (
    ID_BatchInvoice INT PRIMARY KEY IDENTITY(1,1),
    ID_AuditoriaBatch INT NOT NULL,
    ID_Fatura INT NOT NULL,
    ST_Processamento NVARCHAR(50),  -- "Pendente", "Processando", "Sucesso", "Erro"
    DT_Processamento DATETIME,
    DS_Erro NVARCHAR(MAX),
    QT_Tentativas INT DEFAULT 0
)
```

**Problemas Identificados**:
- Sem índice composto em `(ID_AuditoriaBatch, ID_Fatura)` (performance ruim em consultas)
- `ST_Processamento` como string livre
- Sem campo `HangfireJobId` (não rastreava job específico da fatura)

**Campos Mapeados**:
- `ID_BatchInvoice` → `AuditBatchInvoice.Id` (Guid)
- `ID_AuditoriaBatch` → `AuditBatchInvoice.AuditBatchId`
- `ID_Fatura` → `AuditBatchInvoice.InvoiceId`
- `ST_Processamento` → `AuditBatchInvoice.ProcessingStatus` (enum)
- `QT_Tentativas` → `AuditBatchInvoice.RetryAttempts`

---

## SEÇÃO 4: STORED PROCEDURES LEGADO

### 4.1 pa_AuditoriaBatch_Create

**Descrição**: Cria novo lote de auditoria no legado.

**Destino**: **DESCARTADO** → Substituído por Command CQRS `CreateAuditBatchCommand`

**Assinatura**:
```sql
CREATE PROCEDURE pa_AuditoriaBatch_Create
    @ID_Fornecedor INT,
    @NM_Batch NVARCHAR(200),
    @DS_Batch NVARCHAR(MAX),
    @ID_Auditor INT = NULL,
    @ID_UsuarioCriacao INT
AS
BEGIN
    INSERT INTO tb_AuditoriaBatch (ID_Fornecedor, NM_Batch, DS_Batch, ST_Lote, ID_Auditor, DT_Criacao, ID_UsuarioCriacao)
    VALUES (@ID_Fornecedor, @NM_Batch, @DS_Batch, 'Criado', @ID_Auditor, GETDATE(), @ID_UsuarioCriacao)

    SELECT SCOPE_IDENTITY() AS ID_AuditoriaBatch
END
```

**Regras de Negócio Extraídas**:
- Status inicial sempre "Criado" (RN-LOT-054-05: Estado `Created`)
- Data de criação automática (auditoria automática no moderno)
- Auditor opcional (RN-LOT-054-04: Atribuição manual ou automática)

### 4.2 pa_AuditoriaBatch_SelectInvoices

**Descrição**: Seleciona faturas baseado em critérios do lote.

**Destino**: **SUBSTITUÍDO** → Job Hangfire `SelectInvoicesForBatchJob`

**Assinatura**:
```sql
CREATE PROCEDURE pa_AuditoriaBatch_SelectInvoices
    @ID_AuditoriaBatch INT,
    @DT_InicioPeriodo DATE = NULL,
    @DT_FimPeriodo DATE = NULL,
    @ID_Operadora INT = NULL,
    @ID_Filial INT = NULL,
    @VL_Minimo DECIMAL(18,2) = NULL,
    @VL_Maximo DECIMAL(18,2) = NULL
AS
BEGIN
    INSERT INTO tb_AuditoriaBatchInvoices (ID_AuditoriaBatch, ID_Fatura, ST_Processamento)
    SELECT @ID_AuditoriaBatch, F.ID_Fatura, 'Pendente'
    FROM tb_Faturas F
    WHERE (@DT_InicioPeriodo IS NULL OR F.DT_Emissao >= @DT_InicioPeriodo)
      AND (@DT_FimPeriodo IS NULL OR F.DT_Emissao <= @DT_FimPeriodo)
      AND (@ID_Operadora IS NULL OR F.ID_Operadora = @ID_Operadora)
      AND (@ID_Filial IS NULL OR F.ID_Filial = @ID_Filial)
      AND (@VL_Minimo IS NULL OR F.VL_Total >= @VL_Minimo)
      AND (@VL_Maximo IS NULL OR F.VL_Total <= @VL_Maximo)
      AND F.ID_Fatura NOT IN (
          SELECT ID_Fatura FROM tb_AuditoriaBatchInvoices BI
          INNER JOIN tb_AuditoriaBatch B ON BI.ID_AuditoriaBatch = B.ID_AuditoriaBatch
          WHERE B.ST_Lote IN ('Processando', 'Aguardando')
      )

    UPDATE tb_AuditoriaBatch
    SET QT_Faturas = (SELECT COUNT(*) FROM tb_AuditoriaBatchInvoices WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch)
    WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch
END
```

**Regras de Negócio Extraídas**:
- Critérios opcionais (RN-LOT-054-01: Obrigatoriedade de pelo menos um critério)
- Faturas em lotes ativos não devem ser incluídas (RN-LOT-054-03: Prevenção de duplicação)
- Atualização automática de contador de faturas

**Problemas Identificados**:
- Processamento síncrono (poderia travar por minutos com milhares de faturas)
- Sem transação explícita (risco de estado inconsistente)
- Query N+1 na subquery de exclusão de faturas ativas (performance ruim)

### 4.3 pa_AuditoriaBatch_UpdateStatus

**Descrição**: Atualiza status do lote durante processamento.

**Destino**: **DESCARTADO** → State Machine gerenciada pelo Domain Model

**Assinatura**:
```sql
CREATE PROCEDURE pa_AuditoriaBatch_UpdateStatus
    @ID_AuditoriaBatch INT,
    @ST_Lote NVARCHAR(50)
AS
BEGIN
    UPDATE tb_AuditoriaBatch
    SET ST_Lote = @ST_Lote
    WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch
END
```

**Problemas Identificados**:
- Aceita qualquer string em `@ST_Lote` (sem validação de transições de estado)
- Não registra histórico de mudanças de status
- Não valida se transição é válida (ex: permitia "Concluído" → "Criado")

### 4.4 pa_AuditoriaBatch_GetProgress

**Descrição**: Calcula progresso do processamento do lote.

**Destino**: **SUBSTITUÍDO** → Cálculo em tempo real via SignalR

**Assinatura**:
```sql
CREATE PROCEDURE pa_AuditoriaBatch_GetProgress
    @ID_AuditoriaBatch INT
AS
BEGIN
    SELECT
        B.ID_AuditoriaBatch,
        B.QT_Faturas AS TotalFaturas,
        (SELECT COUNT(*) FROM tb_AuditoriaBatchInvoices WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch AND ST_Processamento = 'Sucesso') AS ProcessadasComSucesso,
        (SELECT COUNT(*) FROM tb_AuditoriaBatchInvoices WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch AND ST_Processamento = 'Erro') AS ProcessadasComErro,
        CASE
            WHEN B.QT_Faturas = 0 THEN 0
            ELSE CAST((SELECT COUNT(*) FROM tb_AuditoriaBatchInvoices WHERE ID_AuditoriaBatch = @ID_AuditoriaBatch AND ST_Processamento IN ('Sucesso', 'Erro')) AS DECIMAL) / B.QT_Faturas * 100
        END AS PercentualConclusao
    FROM tb_AuditoriaBatch B
    WHERE B.ID_AuditoriaBatch = @ID_AuditoriaBatch
END
```

**Regras de Negócio Extraídas**:
- Progresso calculado como (processadas / total) × 100 (RN-LOT-054-07)
- Considerar tanto sucesso quanto erro como "processadas"

### 4.5 pa_AuditoriaBatch_Archive

**Descrição**: Arquiva lotes antigos concluídos.

**Destino**: **SUBSTITUÍDO** → Job Hangfire `ArchiveOldBatchesJob`

**Assinatura**:
```sql
CREATE PROCEDURE pa_AuditoriaBatch_Archive
    @DiasAposConc lusao INT = 90
AS
BEGIN
    UPDATE tb_AuditoriaBatch
    SET ST_Lote = 'Arquivado'
    WHERE ST_Lote = 'Concluído'
      AND DATEDIFF(DAY, DT_Fim, GETDATE()) > @DiasAposConc lusao
END
```

**Regras de Negócio Extraídas**:
- Arquivamento automático após 90 dias por padrão (RN configurável no moderno)
- Apenas lotes concluídos podem ser arquivados

---

## SEÇÃO 5: TELAS ASPX LEGADO

### 5.1 AuditoriaBatch.aspx (Listagem)

**Descrição**: Tela de listagem de lotes de auditoria.

**Destino**: **SUBSTITUÍDA** → Componente Angular `AuditBatchesListComponent`

**Caminho Legado**: `ic1_legado/IControlIT/Auditoria/AuditoriaBatch.aspx`

**Funcionalidades Implementadas**:
- GridView com paginação manual (20 registros por página)
- Filtros: Status, Auditor Responsável, Período de Criação
- Botões de ação: Criar Novo, Processar, Cancelar, Arquivar
- Sem ordenação de colunas
- Sem busca textual por nome de lote

**Code-Behind (VB.NET)**:
- `AuditoriaBatch.aspx.vb`
- Utiliza `WSAuditoriaBatch.GetAll()` para carregar lotes
- Binding manual dos dados no GridView
- Eventos de botão chamam WebService

**Componentes UI Legado**:
- `asp:GridView` (tabela de dados)
- `asp:DropDownList` (filtros de status e auditor)
- `asp:Button` (ações)
- `asp:UpdatePanel` (AJAX parcial)

### 5.2 AuditoriaBatchCreate.aspx (Criar/Editar)

**Descrição**: Tela de criação/edição de lote de auditoria.

**Destino**: **SUBSTITUÍDA** → Componente Angular `AuditBatchCreateComponent`

**Caminho Legado**: `ic1_legado/IControlIT/Auditoria/AuditoriaBatchCreate.aspx`

**Funcionalidades Implementadas**:
- Campos: Nome, Descrição
- Critérios de Seleção (accordion):
  - Período (data início, data fim)
  - Operadora (dropdown)
  - Filial (dropdown)
  - Valor Mínimo/Máximo
  - Tipo de Serviço (dropdown)
- Auditor Responsável (dropdown opcional)
- Botão "Estimar Faturas" (chamava SP sem criar lote)
- Validações client-side com JavaScript customizado

**Code-Behind (VB.NET)**:
- `AuditoriaBatchCreate.aspx.vb`
- Utiliza `WSAuditoriaBatch.Create()` ao salvar
- Validações duplicadas no code-behind (inconsistente com client-side)

**Problemas Identificados**:
- JavaScript legado sem framework (jQuery 1.x)
- Validações duplicadas e inconsistentes
- Sem feedback visual de progresso ao salvar

### 5.3 AuditoriaBatchEdit.aspx (Editar)

**Descrição**: Tela de edição de lote existente.

**Destino**: **SUBSTITUÍDA** → Mesmo componente `AuditBatchCreateComponent` (modo edição)

**Caminho Legado**: `ic1_legado/IControlIT/Auditoria/AuditoriaBatchEdit.aspx`

**Funcionalidades Implementadas**:
- Reutiliza layout de `AuditoriaBatchCreate.aspx`
- Carrega dados do lote via `WSAuditoriaBatch.GetById()`
- Bloqueia edição de critérios se status != "Criado"
- Permite alterar apenas Nome, Descrição e Auditor Responsável após início

**Problemas Identificados**:
- Duplicação de código com `AuditoriaBatchCreate.aspx`
- Lógica de bloqueio de edição inconsistente (verificava apenas status, não validava transições)

### 5.4 AuditoriaBatchMonitor.aspx (Monitorar)

**Descrição**: Tela de monitoramento de progresso de lote em processamento.

**Destino**: **SUBSTITUÍDA** → Componente Angular `AuditBatchMonitorComponent` com SignalR

**Caminho Legado**: `ic1_legado/IControlIT/Auditoria/AuditoriaBatchMonitor.aspx`

**Funcionalidades Implementadas**:
- Barra de progresso manual (atualização por refresh)
- Botão "Atualizar" (refresh manual via AJAX)
- Lista de faturas com status (Pendente, Processando, Sucesso, Erro)
- Botão "Cancelar Processamento"
- Logs de erro (apenas texto bruto)

**Code-Behind (VB.NET)**:
- `AuditoriaBatchMonitor.aspx.vb`
- Timer com AutoPostBack a cada 5 segundos (ineficiente)
- Chama `WSAuditoriaBatch.GetProgress()` repetidamente
- Sem WebSockets ou SignalR

**Problemas Identificados**:
- Sem atualização em tempo real (polling ineficiente)
- Barra de progresso não refletia progresso real (calculada incorretamente)
- Timer causava sobrecarga no servidor (centenas de requisições por minuto)

### 5.5 AuditoriaBatchDetail.aspx (Detalhes)

**Descrição**: Tela de visualização detalhada de lote concluído ou arquivado.

**Destino**: **SUBSTITUÍDA** → Componente Angular `AuditBatchDetailComponent`

**Caminho Legado**: `ic1_legado/IControlIT/Auditoria/AuditoriaBatchDetail.aspx`

**Funcionalidades Implementadas**:
- Informações do lote (nome, descrição, status, datas)
- Critérios configurados (readonly)
- Valores consolidados (total auditado, glosas, economia)
- Estatísticas (taxa de aprovação, taxa de rejeição)
- GridView de faturas auditadas (readonly)
- Botão "Exportar Excel" (SSRS Report)

**Code-Behind (VB.NET)**:
- `AuditoriaBatchDetail.aspx.vb`
- Chama `WSAuditoriaBatch.GetDetails()`
- Exportação via ReportViewer (SSRS)

**Problemas Identificados**:
- Sem histórico de auditoria das operações do lote
- Exportação apenas para Excel (sem PDF)
- Relatório SSRS lento para lotes grandes (>1000 faturas)

---

## SEÇÃO 6: WEBSERVICES LEGADO (ASMX)

### 6.1 WSAuditoriaBatch.asmx (VB.NET)

**Descrição**: WebService ASMX legado para operações de lotes de auditoria.

**Destino**: **SUBSTITUÍDO** → API REST .NET 10 (Minimal APIs)

**Caminho Legado**: `ic1_legado/IControlIT/WebServices/WSAuditoriaBatch.asmx`

**Métodos Implementados**:

#### 6.1.1 CreateBatch()

**Assinatura**:
```vb
<WebMethod()>
Public Function CreateBatch(ByVal ID_Fornecedor As Integer, ByVal NM_Batch As String, ByVal DS_Batch As String, ByVal ID_Auditor As Integer?) As Integer
    ' Chama pa_AuditoriaBatch_Create
    ' Retorna ID do lote criado
End Function
```

**Destino**: **SUBSTITUÍDO** → `POST /api/audit-batches`

#### 6.1.2 SelectInvoicesForBatch()

**Assinatura**:
```vb
<WebMethod()>
Public Sub SelectInvoicesForBatch(ByVal ID_AuditoriaBatch As Integer, ByVal criterios As Dictionary(Of String, Object))
    ' Parseia criterios de Dictionary(!)
    ' Chama pa_AuditoriaBatch_SelectInvoices
End Sub
```

**Destino**: **SUBSTITUÍDO** → Job Hangfire assíncrono (não mais endpoint síncrono)

**Problemas Identificados**:
- Método síncrono bloqueante (poderia travar por minutos)
- Parsing manual de Dictionary (propenso a erros de runtime)

#### 6.1.3 StartProcessing()

**Assinatura**:
```vb
<WebMethod()>
Public Sub StartProcessing(ByVal ID_AuditoriaBatch As Integer)
    ' Loop síncrono processando fatura por fatura (!)
    ' Timeout HTTP garantido para lotes >100 faturas
End Sub
```

**Destino**: **SUBSTITUÍDO** → `POST /api/audit-batches/{id}/process` (dispara job assíncrono)

**Problemas Identificados**:
- Implementação síncrona catastrófica (loop bloqueante)
- Timeout HTTP para lotes médios (>100 faturas em ~5min)
- Sem recovery se servidor cair durante processamento

#### 6.1.4 GetBatchProgress()

**Assinatura**:
```vb
<WebMethod()>
Public Function GetBatchProgress(ByVal ID_AuditoriaBatch As Integer) As Object
    ' Chama pa_AuditoriaBatch_GetProgress
    ' Retorna objeto com TotalFaturas, Processadas, Percentual
End Function
```

**Destino**: **SUBSTITUÍDO** → Hub SignalR `/hubs/audit-batches` (push real-time, não polling)

#### 6.1.5 CancelBatch()

**Assinatura**:
```vb
<WebMethod()>
Public Sub CancelBatch(ByVal ID_AuditoriaBatch As Integer)
    ' Atualiza status para "Cancelado"
    ' NÃO fazia rollback de itens já criados (bug crítico!)
End Sub
```

**Destino**: **SUBSTITUÍDO** → `POST /api/audit-batches/{id}/cancel` (com rollback completo)

**Problemas Identificados**:
- Sem rollback (itens de auditoria criados permaneciam inconsistentes)
- Sem registro de histórico de cancelamento

#### 6.1.6 GetBatchDetails()

**Assinatura**:
```vb
<WebMethod()>
Public Function GetBatchDetails(ByVal ID_AuditoriaBatch As Integer) As Object
    ' Retorna lote + critérios + faturas + valores consolidados
End Function
```

**Destino**: **SUBSTITUÍDO** → `GET /api/audit-batches/{id}`

---

## SEÇÃO 7: PROBLEMAS E GAPS IDENTIFICADOS

### 7.1 Problemas Críticos do Legado

**PROB-LOT-01: Processamento Síncrono Bloqueante**:
- **Descrição**: Lotes eram processados de forma síncrona no WebService, travando tela e causando timeouts
- **Impacto**: Impossível processar lotes >500 faturas sem timeout HTTP
- **Solução Moderna**: Hangfire com jobs assíncronos paralelos (RN-LOT-054-06)

**PROB-LOT-02: Sem Retry Automático**:
- **Descrição**: Faturas que falhavam durante processamento não eram reprocessadas automaticamente
- **Impacto**: Taxa de erro ~15-20%, necessidade de reprocessamento manual
- **Solução Moderna**: Retry policy exponencial (RN-LOT-054-08)

**PROB-LOT-03: Sem Monitoramento em Tempo Real**:
- **Descrição**: Progresso só era conhecido por polling manual (refresh de página)
- **Impacto**: Ansiedade do usuário, sobrecarga do servidor com polling excessivo
- **Solução Moderna**: SignalR com push real-time (RN-LOT-054-07)

**PROB-LOT-04: Sem Rollback em Cancelamento**:
- **Descrição**: Cancelar lote não revertia itens de auditoria já criados
- **Impacto**: Dados inconsistentes, necessidade de cleanup manual
- **Solução Moderna**: Rollback automático completo (RN-LOT-054-13)

**PROB-LOT-05: Estado Inconsistente em Restart**:
- **Descrição**: Se servidor reiniciasse durante processamento, lote ficava "travado"
- **Impacto**: Necessidade de script SQL manual para resetar status
- **Solução Moderna**: Hangfire persiste jobs em banco, recovery automático

**PROB-LOT-06: Validações Inconsistentes**:
- **Descrição**: Validações client-side (JavaScript) diferentes de server-side (VB.NET)
- **Impacto**: Dados inválidos chegavam ao banco
- **Solução Moderna**: FluentValidation no backend, Angular Forms no frontend (mesmas regras)

### 7.2 Gaps Funcionais (Legado NÃO tinha, Moderno TEM)

**GAP-LOT-01: Notificações Assíncronas via Azure Service Bus**:
- **Legado**: Sem notificações (apenas emails manuais)
- **Moderno**: Azure Service Bus + webhooks (RN-LOT-054-12)

**GAP-LOT-02: SLA e Alertas de Timeout**:
- **Legado**: Sem monitoramento de SLA
- **Moderno**: SLA configurável + alertas automáticos (RN-LOT-054-14)

**GAP-LOT-03: Dashboard de KPIs em Tempo Real**:
- **Legado**: Relatórios SSRS estáticos
- **Moderno**: Dashboard Angular com atualização automática

**GAP-LOT-04: Histórico Completo de Auditoria**:
- **Legado**: Sem rastreamento de operações
- **Moderno**: Auditoria total com usuário, IP, data/hora (RN-LOT-054-11)

**GAP-LOT-05: Máquina de Estados Rigorosa**:
- **Legado**: Transições de estado sem validação
- **Moderno**: State Machine com validação (RN-LOT-054-05)

### 7.3 Funcionalidades do Legado NÃO Migradas (Descartadas)

**FUNC-DESC-01: Barra de Progresso Fake**:
- **Descrição**: Legado tinha barra de progresso que não refletia progresso real
- **Motivo Descarte**: Enganava usuário, substituída por progresso real via SignalR

**FUNC-DESC-02: Estimativa de Faturas sem Criar Lote**:
- **Descrição**: Botão "Estimar" chamava SP sem criar lote
- **Motivo Descarte**: Funcionalidade desnecessária, sistema moderno mostra estimativa em tempo real conforme usuário configura critérios

**FUNC-DESC-03: Relatórios SSRS Específicos**:
- **Descrição**: Relatórios customizados em SSRS
- **Motivo Descarte**: Substituídos por exportação Excel/PDF genérica com ClosedXML/QuestPDF

---

**FIM DO DOCUMENTO RL-RF054 v1.0**

# RL-RF034: Referência ao Legado - Gestão de Itens de Auditoria

**Versão**: 2.0
**Data**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**RF Relacionado**: RF034
**EPIC**: EPIC010-AUD-Auditoria-Avançada

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Stack Tecnológica

- **Backend**: ASP.NET Web Forms 4.8 + VB.NET
- **Frontend**: ASPX + VB.NET code-behind
- **Banco de Dados**: SQL Server (multi-database, um por cliente)
- **Arquitetura**: Monolito com acoplamento alto
- **Integração**: WebServices SOAP (.asmx)

### 1.2 Arquitetura Geral

O sistema legado operava em modelo **multi-database**:
- Cada cliente (Fornecedor) possuía um banco SQL Server dedicado
- Schema idêntico replicado em N bancos
- Sem consolidação centralizada
- Conexões via connection strings dinâmicas no web.config

### 1.3 Problemas Arquiteturais Identificados

**PROB-001: Inconsistência de Tipos Numéricos**
- Uso de `float` para valores monetários (impreciso)
- Arredondamentos causavam erros em cálculos de glosa
- Solução moderna: DECIMAL(13,8) em todas as colunas financeiras

**PROB-002: Campo Glosa Editável Manualmente**
- Campo `Valor_Cobrado_A_Mais` era editável pelo usuário
- Possibilitava inconsistências entre ValorCobrado, ValorCorreto e Glosa
- Solução moderna: Campo calculado automaticamente (read-only)

**PROB-003: Falta de Soft Delete**
- Exclusão física de registros
- Perda de histórico de auditoria
- Dificultava investigações de compliance
- Solução moderna: FlExcluido + Global Query Filter

**PROB-004: Falta de Auditoria de Alterações**
- Sem rastreamento de quem criou/alterou registros
- Sem timestamp de alterações
- Impossível identificar responsável por mudanças
- Solução moderna: Shadow Properties (UsuarioCriacao, DataCriacao, UsuarioAlteracao, DataAlteracao)

**PROB-005: Sem Row-Level Security**
- Campo Id_Fornecedor sem filtro automático
- Risco de vazamento cross-tenant se query esquecer WHERE
- Solução moderna: Global Query Filter no DbContext

**PROB-006: Sem Índices Otimizados para Relatórios**
- Relatórios com milhares de registros travavam
- Full table scans em queries analíticas
- Solução moderna: Índices não-clusterizados com INCLUDE para colunas de projeção

---

## 2. TELAS ASPX E CÓDIGO-BEHIND

### 2.1 AuditoriaItens.aspx

**Caminho**: `ic1_legado/IControlIT/Auditoria/AuditoriaItens.aspx`

**Funcionalidades**:
- Grid de listagem de itens de auditoria com paginação manual (20 registros por página)
- Formulário modal para criação/edição de item
- Botão "Exportar para Excel" (gera CSV via Response.Write)
- Filtros por período (lote AAAAMM), operadora e tipo de bilhete

**Regras Implícitas no Code-Behind (VB.NET)**:
- Validação manual de campos obrigatórios em botão "Salvar" (linha ~350)
- Cálculo de glosa feito no code-behind: `txtGlosa.Text = Val(txtCobrado.Text) - Val(txtCorreto.Text)`
- Atualização de totalizadores do resumo via EXEC sp_RecalcularResumo após salvar item
- GridView preenche campos via DataBind de DataTable retornado de stored procedure

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Tela redesenhada em Angular 19 com componentes standalone, reactive forms, validações real-time, Material Design.

**Rastreabilidade**:
- **RF moderno**: RF034 - Seção 2 (Funcionalidades F01-F14)
- **UC moderno**: UC01-RF034 (Criar Item), UC02-RF034 (Editar Item)

**Migração moderna**:
- **Componente Angular**: `auditoria-itens-list.component.ts` + `auditoria-itens-form.component.ts`
- **Rota frontend**: `/gestao/auditoria-itens`

---

### 2.2 AuditoriaItensRelatorio.aspx

**Caminho**: `ic1_legado/IControlIT/Auditoria/AuditoriaItensRelatorio.aspx`

**Funcionalidades**:
- Relatório consolidado de glosas por operadora
- Gráfico de barras (componente ASP.NET Chart Control)
- Filtros por data início/fim e operadora (multi-select)
- Exportação para PDF via iTextSharp (código manual de 200 linhas)

**Regras Implícitas**:
- Agregação de valores feita em stored procedure sp_RelatorioGlosasPorOperadora
- Gráfico renderizado server-side (imagem PNG gerada no servidor)
- Paginação de relatório manual via Session["PageIndex"]

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Relatório redesenhado com Chart.js no frontend, queries otimizadas com projeções, paginação Angular Material.

**Rastreabilidade**:
- **RF moderno**: RF034 - Seção 2 (Funcionalidade F09 - Relatórios Gerenciais)
- **UC moderno**: UC04-RF034 (Consultar e Filtrar Itens)

**Migração moderna**:
- **Componente Angular**: `auditoria-itens-relatorios.component.ts`
- **Rota frontend**: `/gestao/auditoria-itens/relatorios`
- **Biblioteca de gráficos**: Chart.js (client-side rendering)

---

### 2.3 AuditoriaItensExportar.aspx

**Caminho**: `ic1_legado/IControlIT/Auditoria/AuditoriaItensExportar.aspx`

**Funcionalidades**:
- Exportação de itens selecionados para Excel (formato CSV simulado)
- Geração de PDF para contestação com logo da empresa
- Agrupamento manual por operadora no code-behind
- Cálculo de subtotais em loop For Each

**Regras Implícitas**:
- Exportação CSV usa Response.ContentType = "application/vnd.ms-excel"
- PDF gerado via iTextSharp com código monolítico de 400 linhas
- Formatação de valores monetários manual: `Format(valor, "R$ #,##0.00000000")`

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Exportação modernizada com EPPlus (Excel) e QuestPDF (PDF), formatação automática, agrupamento via LINQ.

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-008 (Exportação Estruturada)
- **UC moderno**: UC03-RF034 (Exportar Itens)

**Migração moderna**:
- **Command CQRS**: `ExportarItensContestacaoCommand`
- **Handler**: `ExportarItensContestacaoHandler`
- **Bibliotecas**: EPPlus, QuestPDF

---

## 3. WEBSERVICES (.asmx)

### 3.1 AuditoriaService.asmx

**Caminho**: `ic1_legado/IControlIT/WebServices/AuditoriaService.asmx`

**Métodos Públicos**:

1. **ObterItensAuditoria(lote As String, FornecedorId As Integer) As DataSet**
   - Retorna DataSet com itens filtrados por lote
   - Parâmetros: lote (AAAAMM), FornecedorId
   - Retorno: DataSet não tipado

2. **SalvarItemAuditoria(item As ItemAuditoriaDto) As Boolean**
   - Cria ou atualiza item de auditoria
   - Validações manuais inline (sem FluentValidation)
   - Retorna True/False (sem mensagem de erro detalhada)

3. **ExcluirItemAuditoria(itemId As Integer) As Boolean**
   - Exclusão FÍSICA (DELETE FROM)
   - Não registra auditoria
   - Retorna True/False

**Regras Implícitas**:
- WebService sem autenticação JWT (apenas IP whitelist no IIS)
- Retorna DataSet não tipado (sem schema validation)
- Exceptions não estruturadas (throw new Exception("Erro genérico"))

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Substituído por REST API com autenticação JWT, DTOs tipados, validações FluentValidation, retorno estruturado com HTTP Status Codes.

**Rastreabilidade**:
- **RF moderno**: RF034 - Seção 6 (API Endpoints)
- **Endpoints modernos**:
  - GET /api/v1/auditoria-itens
  - POST /api/v1/auditoria-itens
  - DELETE /api/v1/auditoria-itens/{id}

**Migração moderna**:
- **Minimal APIs**: `ItensAuditoria.cs` (endpoints group)
- **Commands**: `CreateAuditoriaItemCommand`, `UpdateAuditoriaItemCommand`, `DeleteAuditoriaItemCommand`
- **Queries**: `GetAuditoriasItensQuery`, `GetAuditoriaItemByIdQuery`

---

## 4. STORED PROCEDURES

### 4.1 sp_AuditarFatura

**Caminho**: `ic1_legado/Database/Procedures/sp_AuditarFatura.sql`

**Parâmetros de Entrada**:
- `@Id_Fatura INT`
- `@Id_Fornecedor INT`
- `@Lote VARCHAR(6)`

**Parâmetros de Saída**:
- `@TotalItensProcessados INT OUTPUT`

**Lógica Principal** (em linguagem natural):
1. Busca todos os bilhetes da fatura informada
2. Para cada bilhete, compara valor cobrado versus valor contratual (tabela TarifasContratos)
3. Se divergência detectada, insere registro em Auditoria_Item
4. Calcula glosa como diferença de valores
5. Atualiza totalizadores em Auditoria_Resumo

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Lógica movida para Application Layer (CQRS Handler) com validações FluentValidation, Domain Events para sincronização de resumos.

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-006 (Sincronização Automática)
- **Regra moderna**: Domain Event `AuditoriaItemCriadoDomainEvent`

**Migração moderna**:
- **Handler**: `CreateAuditoriaItemCommandHandler`
- **Domain Event Handler**: `RecalcularResumoAoItemCriadoHandler`

---

### 4.2 sp_CalcularGlosa

**Caminho**: `ic1_legado/Database/Procedures/sp_CalcularGlosa.sql`

**Parâmetros**:
- `@ValorCobrado NUMERIC(13,8)`
- `@ValorCorreto NUMERIC(13,8)`
- `@Glosa NUMERIC(13,8) OUTPUT`

**Lógica**:
```sql
SET @Glosa = @ValorCobrado - @ValorCorreto
```

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Cálculo trivial movido para propriedade calculada em Domain Model (AuditoriaItem.ValorCobradoAMais).

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-002 (Cálculo Automático de Glosa)

**Migração moderna**:
- **Entidade**: `AuditoriaItem`
- **Propriedade calculada**: `public decimal ValorCobradoAMais => ValorCobrado - ValorCorreto;`

---

### 4.3 sp_GerarRelatorioAuditoria

**Caminho**: `ic1_legado/Database/Procedures/sp_GerarRelatorioAuditoria.sql`

**Parâmetros**:
- `@DataInicio DATE`
- `@DataFim DATE`
- `@Id_Fornecedor INT`

**Lógica Principal**:
1. Agrupa itens por operadora usando GROUP BY
2. Calcula SUM(Valor_Cobrado_A_Mais) por operadora
3. Retorna ResultSet com colunas: Operadora, TotalGlosa, TotalItens, DivergenciaMedia

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Query otimizada com projeções desnormalizadas, índices específicos, paginação e filtros dinâmicos.

**Rastreabilidade**:
- **RF moderno**: RF034 - Funcionalidade F09 (Relatórios Gerenciais)

**Migração moderna**:
- **Query**: `GetRelatorioOperadoraQuery`
- **Handler**: `GetRelatorioOperadoraQueryHandler`
- **Projeção**: LINQ com GroupBy + Select

---

### 4.4 sp_ExportarItens

**Caminho**: `ic1_legado/Database/Procedures/sp_ExportarItens.sql`

**Parâmetros**:
- `@Id_Auditoria_Resumo INT`
- `@Id_Fornecedor INT`

**Lógica**:
1. SELECT com múltiplos JOINs (7 tabelas)
2. Ordena por Operadora, depois por ValorCobradoAMais DESC
3. Retorna ResultSet completo (sem paginação)

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Query otimizada com paginação, filtros dinâmicos, índices específicos, seleção parcial de colunas.

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-008 (Exportação Estruturada)

**Migração moderna**:
- **Query**: `ExportAuditoriasItensQuery`
- **Handler**: `ExportAuditoriasItensHandler`

---

## 5. TABELAS LEGADAS

### 5.1 dbo.Auditoria_Item

**Schema Legado**:
```sql
CREATE TABLE [dbo].[Auditoria_Item](
    [Id_Auditoria_Item] [int] IDENTITY(1,1) NOT NULL,
    [Id_Auditoria_Resumo] [int] NOT NULL,
    [Id_Bilhete] [int] NOT NULL,
    [Id_Bilhete_Tipo] [int] NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Id_Contrato] [int] NOT NULL,
    [Id_Fornecedor] [int] NOT NULL,
    [Unidade] [int] NOT NULL,
    [DT_Lote] [varchar](6) NOT NULL,
    [QTD_Consumo] [float] NOT NULL,
    [Valor_Cobrado] [numeric](13, 8) NULL,
    [Valor_Contrato] [numeric](13, 8) NULL,
    [Valor_Correto] [float] NULL,
    [Valor_Cobrado_A_Mais] [float] NULL,
    [Total_Fatura] [numeric](13, 8) NULL,
    [Fatura] [varchar](50) NOT NULL,
    CONSTRAINT [PK_Auditoria_Item] PRIMARY KEY CLUSTERED ([Id_Auditoria_Item] ASC)
)
```

**Problemas Identificados**:
- ❌ **Falta de FK**: Nenhuma Foreign Key constraint definida
- ❌ **Tipo float**: Campos `QTD_Consumo`, `Valor_Correto` e `Valor_Cobrado_A_Mais` usam `float` (impreciso)
- ❌ **Campos NULL**: `Valor_Cobrado`, `Valor_Contrato`, `Valor_Correto` permitem NULL (deveriam ser obrigatórios)
- ❌ **Sem soft delete**: Não possui campo `FlExcluido`
- ❌ **Sem auditoria**: Não possui `DataCriacao`, `UsuarioCriacao`, `DataAlteracao`, `UsuarioAlteracao`
- ❌ **Id_Fornecedor**: Sem Row-Level Security (sem índice otimizado para multi-tenancy)
- ❌ **Sem índices**: Apenas PK clusterizada, sem índices para queries analíticas

**DESTINO**: **SUBSTITUÍDO**

**Justificativa**: Tabela redesenhada com:
- GUIDs em vez de INT
- Foreign Keys obrigatórias
- DECIMAL(13,8) para todos os valores
- Campos obrigatórios com NOT NULL
- FlExcluido para soft delete
- Shadow Properties para auditoria
- Global Query Filter para Row-Level Security
- Índices não-clusterizados otimizados

**Rastreabilidade**:
- **RF moderno**: RF034 - Seção 7 (Modelo de Dados)
- **MD moderno**: MD-RF034.md - Tabela AuditoriaItem

**Migração moderna**:
- **Tabela**: `AuditoriaItem`
- **Migration EF Core**: `20251230_CreateAuditoriaItemTable.cs`
- **DDL moderno**: Ver MD-RF034.md

---

### 5.2 dbo.Auditoria_Resumo

**Schema Legado**:
```sql
CREATE TABLE [dbo].[Auditoria_Resumo](
    [Id_Auditoria_Resumo] [int] IDENTITY(1,1) NOT NULL,
    [Id_Fornecedor] [int] NOT NULL,
    [DT_Lote] [varchar](6) NOT NULL,
    [Total_Valor_Cobrado] [numeric](13, 8) NULL,
    [Total_Valor_Correto] [numeric](13, 8) NULL,
    [Total_Glosa] [numeric](13, 8) NULL,
    [Total_Itens] [int] NULL,
    [Data_Criacao] [datetime] DEFAULT GETDATE() NOT NULL,
    CONSTRAINT [PK_Auditoria_Resumo] PRIMARY KEY CLUSTERED ([Id_Auditoria_Resumo] ASC)
)
```

**Problemas Identificados**:
- ❌ **FK sem constraint**: `Id_Fornecedor` sem FK para tabela Fornecedor
- ❌ **Campos NULL**: Totalizadores permitem NULL (deveriam ter default 0)
- ❌ **Sem soft delete**: Não possui `FlExcluido`
- ❌ **Auditoria parcial**: Possui `Data_Criacao`, mas falta `UsuarioCriacao`, `DataAlteracao`, `UsuarioAlteracao`

**DESTINO**: **ASSUMIDO** (parcialmente)

**Justificativa**: Tabela mantida com correções arquiteturais (GUIDs, FKs, soft delete, auditoria completa).

**Rastreabilidade**:
- **RF relacionado**: RF035 - Gestão de Resumos de Auditoria

**Migração moderna**:
- **Tabela**: `AuditoriaResumo`
- **Migration EF Core**: `20251230_CreateAuditoriaResumoTable.cs`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### 6.1 Validação de Precisão Decimal

**Localização**: `ic1_legado/IControlIT/Auditoria/AuditoriaItens.aspx.vb` - Linha 420

**Regra extraída**:
- Valores monetários devem ter no máximo 8 casas decimais
- Validação via `Decimal.Round(valor, 8)`
- Rejeição se valor exceder precisão

**DESTINO**: **ASSUMIDO**

**Justificativa**: Regra documentada e mantida no sistema moderno via FluentValidation.

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-003 (Precisão Numérica)

**Migração moderna**:
- **Validador**: `CreateAuditoriaItemCommandValidator`
- **Linha de código**: `RuleFor(x => x.ValorCobrado).PrecisionScale(13, 8, true)`

---

### 6.2 Quantidade Consumo Deve Ser Positiva

**Localização**: `ic1_legado/IControlIT/Auditoria/AuditoriaItens.aspx.vb` - Linha 445

**Regra extraída**:
- QuantidadeConsumo não pode ser zero ou negativo
- Validação: `If QTD_Consumo <= 0 Then Throw New Exception("Quantidade inválida")`

**DESTINO**: **ASSUMIDO**

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-004 (Quantidade de Consumo Positiva)

**Migração moderna**:
- **Validador**: `CreateAuditoriaItemCommandValidator`
- **Linha de código**: `RuleFor(x => x.QuantidadeConsumo).GreaterThan(0)`

---

### 6.3 Unidade de Consumo Deve Respeitar Tipo de Bilhete

**Localização**: `ic1_legado/IControlIT/WebServices/AuditoriaService.asmx.vb` - Linha 180

**Regra extraída**:
- Tipo de bilhete "VOZ" só permite Unidade = 1 (minutos)
- Tipo de bilhete "DADOS" só permite Unidade = 2 (MB)
- Tipo de bilhete "SMS" só permite Unidade = 3 (mensagens)
- Validação manual via SELECT na tabela BilhetesTipos

**DESTINO**: **ASSUMIDO**

**Rastreabilidade**:
- **RF moderno**: RF034 - RN-RF034-011 (Validação de Valores Conforme Tipo de Bilhete)

**Migração moderna**:
- **Validador**: `CreateAuditoriaItemCommandValidator`
- **Linha de código**: Pattern matching com MustAsync para validar Tipo vs Unidade

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

### 7.1 Funcionalidades do Legado NÃO Migradas

**FUN-LEG-001: Export CSV Direto via Response.Write**
- **Descrição**: Exportação CSV direta sem geração de arquivo intermediário
- **Justificativa**: Técnica obsoleta, substituída por EPPlus com arquivo Excel real
- **Impacto**: Nenhum (funcionalidade melhorada no sistema moderno)

**FUN-LEG-002: Gráficos Server-Side (ASP.NET Chart Control)**
- **Descrição**: Gráficos renderizados no servidor como imagens PNG
- **Justificativa**: Técnica obsoleta, substituída por Chart.js no frontend
- **Impacto**: Nenhum (funcionalidade melhorada no sistema moderno)

---

### 7.2 Funcionalidades Novas do Sistema Moderno (Não Existiam no Legado)

**FUN-MOD-001: Dashboard de Glosas em Tempo Real**
- **Descrição**: Dashboard com KPIs atualizados em tempo real via SignalR
- **Justificativa**: Facilita tomada de decisão rápida, identifica divergências críticas imediatamente
- **RF moderno**: RF034 - Funcionalidade F10

**FUN-MOD-002: Notificações de Divergências Críticas**
- **Descrição**: Alertas automáticos via SignalR para divergências >10%
- **Justificativa**: Escalação rápida para gestores de auditoria
- **RF moderno**: RF034 - Funcionalidade F12

**FUN-MOD-003: Workflow de Aprovação com Estados**
- **Descrição**: Transições de estado (pendente → análise → aprovado → contestado → recuperado)
- **Justificativa**: Rastreabilidade de processo de aprovação e contestação
- **RF moderno**: RF034 - Funcionalidade F07

**FUN-MOD-004: Exportação PDF com Logo Empresa**
- **Descrição**: Geração de PDF profissional com logo, assinatura eletrônica e QR Code
- **Justificativa**: Documento formal para contestação com rastreabilidade
- **RF moderno**: RF034 - RN-RF034-008

---

### 7.3 Mudanças de Comportamento Entre Legado e Moderno

| Aspecto | Legado | Moderno | Impacto |
|---------|--------|---------|---------|
| **Exclusão** | Física (DELETE) | Lógica (FlExcluido) | Preserva histórico |
| **Cálculo de Glosa** | Manual ou editável | Automático (read-only) | Elimina inconsistências |
| **Multi-Tenancy** | Manual (WHERE Id_Fornecedor) | Automático (Global Query Filter) | Elimina vazamento de dados |
| **Auditoria** | Sem rastreamento | Shadow Properties automático | Conformidade LGPD |
| **Validações** | Manuais inline | FluentValidation centralizado | Consistência e testabilidade |
| **Sincronização Resumo** | Job batch (sp_RecalcularResumo) | Domain Events em tempo real | Consistência imediata |
| **Performance** | Sem índices | Índices otimizados | Queries 10x mais rápidas |
| **Autenticação** | IP whitelist | JWT Bearer Token | Segurança moderna |

---

### 7.4 Riscos de Migração Identificados

**RISCO-001: Migração de Dados Legados com Valores Float**
- **Descrição**: Campos `Valor_Correto` e `Valor_Cobrado_A_Mais` usam `float` (impreciso)
- **Mitigação**: Conversão para DECIMAL(13,8) com arredondamento controlado na migration
- **Impacto**: BAIXO (diferenças < 0.00000001 aceitáveis)

**RISCO-002: Perda de Histórico de Itens Excluídos Fisicamente**
- **Descrição**: Legado excluía fisicamente registros (sem auditoria)
- **Mitigação**: Impossível recuperar registros já excluídos
- **Impacto**: MÉDIO (loss de histórico pré-migração)

**RISCO-003: Mudança de Comportamento do Campo Glosa (Read-Only)**
- **Descrição**: Legado permitia edição manual de Valor_Cobrado_A_Mais
- **Mitigação**: Documentar mudança de comportamento, treinar usuários
- **Impacto**: BAIXO (melhora qualidade dos dados)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-30 | Separação RF/RL - Criação do RL-RF034.md com 7 seções obrigatórias | Agência ALC - alc.dev.br |

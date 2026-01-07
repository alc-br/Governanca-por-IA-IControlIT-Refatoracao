# RL-RF089 — Referência ao Legado (Conciliação e Auditoria de Faturas)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-089
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server 2019
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura

- **Arquitetura**: Monolítica WebForms
- **Linguagem / Stack**: ASP.NET Web Forms 4.8, VB.NET, ADO.NET
- **Banco de Dados**: SQL Server 2019 (múltiplas instâncias por cliente)
- **Multi-tenant**: NÃO (um banco por cliente)
- **Auditoria**: Parcial (apenas insert/update em algumas tabelas, sem hash de integridade)
- **Configurações**: Web.config (hardcoded), tabelas de configuração sem versionamento

### Problemas Arquiteturais Identificados

1. **Acoplamento de Dados**: Cada cliente possui banco separado, dificultando consolidação e reporting
2. **Conciliação Manual**: 90% do matching é feito em Excel, sem automação
3. **Ausência de ML**: Não há detecção de anomalias, fraudes são identificadas manualmente
4. **Stored Procedures Complexas**: Lógica de negócio embutida em SQL, difícil de testar e manter
5. **Sem Event Sourcing**: Auditoria simples (before/after), sem trilha imutável
6. **Performance**: Consultas N+1, timeouts em volume >50k faturas/mês
7. **Relatórios RDLC**: Hardcoded, difícil customização, sem exportação SPED automatizada

---

## 2. TELAS DO LEGADO

### Tela: ConciliacaoNFe.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/ConciliacaoNFe.aspx`
- **Responsabilidade:** Tela principal de conciliação manual de Notas Fiscais com Pedidos de Compra

#### Campos Principais

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtChaveNFe` | TextBox | Sim | CHAVE_NFE (44 dígitos) |
| `ddlFornecedor` | DropDownList | Sim | Lista de fornecedores |
| `txtValorTotal` | TextBox (decimal) | Sim | Valor total da NF-e |
| `ddlPedidoCompra` | DropDownList | Não | Vinculação manual com PC |
| `ddlStatusConciliacao` | DropDownList | Não | Valores: NaoConciliada, ConciliadaParcial, Conciliada |
| `txtDataEmissao` | TextBox (date) | Sim | Data de emissão da NF-e |
| `txtDataRecebimento` | TextBox (date) | Não | Data de recebimento físico |
| `btnConciliar` | Button | - | Dispara matching manual |

#### Comportamentos Implícitos

- Validação de CHAVE_NFE feita apenas em client-side (JavaScript), sem validação server-side robusta
- Matching é executado manualmente pelo usuário (botão "Conciliar")
- Divergências não são classificadas por severidade, apenas registradas como "sim/não"
- Sem workflow de aprovação: gestor aprova manualmente via e-mail, sem rastreabilidade
- Relatórios gerados em RDLC, sem exportação SPED
- Conciliação bancária feita em Excel separado, fora do sistema

#### Code-Behind Relevante (ConciliacaoNFe.aspx.vb)

```vb
Protected Sub btnConciliar_Click(sender As Object, e As EventArgs)
    Dim chaveNFe As String = txtChaveNFe.Text.Trim()
    Dim pedidoId As Integer = Convert.ToInt32(ddlPedidoCompra.SelectedValue)

    ' Buscar NF-e no banco
    Dim nfe As DataTable = BuscarNotaFiscal(chaveNFe)
    If nfe.Rows.Count = 0 Then
        lblMensagem.Text = "NF-e não encontrada"
        Return
    End If

    ' Buscar Pedido de Compra
    Dim pc As DataTable = BuscarPedidoCompra(pedidoId)
    If pc.Rows.Count = 0 Then
        lblMensagem.Text = "Pedido de Compra não encontrado"
        Return
    End If

    ' Validação simples de valor (sem tolerância)
    Dim valorNFe As Decimal = Convert.ToDecimal(nfe.Rows(0)("ValorTotal"))
    Dim valorPC As Decimal = Convert.ToDecimal(pc.Rows(0)("ValorTotal"))

    If valorNFe <> valorPC Then
        ' Registrar divergência (sem classificação de severidade)
        RegistrarDivergencia(chaveNFe, pedidoId, "ValorDiferente", valorNFe - valorPC)
        lblMensagem.Text = "Divergência de valor detectada. Enviar e-mail para gestor."
        EnviarEmailGestor(chaveNFe, "Divergência de valor")
    Else
        ' Marcar como conciliada
        AtualizarStatusNFe(chaveNFe, "Conciliada")
        lblMensagem.Text = "NF-e conciliada com sucesso"
    End If
End Sub
```

**Problemas identificados no code-behind:**
- Validação de valor exato (`<>`), sem tolerância configurável
- Sem validação de quantidade, datas, CFOP
- Sem matching three-way (apenas NF-e vs PC)
- Sem detecção de anomalias
- E-mail manual, sem workflow automático
- Sem auditoria de quem aprovou/rejeitou

**Destino**: SUBSTITUÍDO
**Justificativa**: Funcionalidade redesenhada com matching automático, tolerâncias configuráveis, workflow de aprovação com SLA, ML para anomalias.
**Rastreabilidade**: RF-089 (Seção 5 - Regras de Negócio), UC05-conciliar-fatura.md

---

### Tela: DivergenciasAprovacao.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/DivergenciasAprovacao.aspx`
- **Responsabilidade:** Tela de aprovação manual de divergências detectadas

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvDivergencias` | GridView | - | Lista de divergências pendentes |
| `txtJustificativa` | TextBox (multiline) | Sim | Justificativa de aprovação/rejeição |
| `btnAprovar` | Button | - | Aprovar divergência selecionada |
| `btnRejeitar` | Button | - | Rejeitar divergência selecionada |

#### Comportamentos Implícitos

- Divergências exibidas sem classificação de severidade (todas tratadas igualmente)
- Sem roteamento automático: qualquer usuário com acesso pode aprovar
- Sem SLA: divergências ficam pendentes indefinidamente
- Justificativa obrigatória, mas sem validação de tamanho mínimo
- Auditoria simples: registra usuário e data, mas sem hash de integridade
- Sem notificações em tempo real (usuário precisa acessar a tela manualmente)

**Destino**: SUBSTITUÍDO
**Justificativa**: Funcionalidade redesenhada com classificação de severidade, roteamento automático, SLA por severidade, notificações SignalR, auditoria com hash SHA-512.
**Rastreabilidade**: RF-089 (RN-FIN-089-06), UC06-aprovar-divergencia.md

---

### Tela: RelatorioFiscal.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/RelatorioFiscal.aspx`
- **Responsabilidade:** Geração de relatórios de conciliação e exportação fiscal

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `dtpDataInicio` | DatePicker | Sim | Data início do período |
| `dtpDataFim` | DatePicker | Sim | Data fim do período |
| `ddlFormato` | DropDownList | Sim | PDF ou Excel (RDLC) |
| `btnGerar` | Button | - | Gera relatório |

#### Comportamentos Implícitos

- Relatórios hardcoded em RDLC (Report Builder)
- Sem exportação SPED (E-100, E-200, E-310)
- Timeout em períodos >3 meses (50k+ faturas)
- Sem filtros avançados (fornecedor, status, severidade)
- Excel gerado via RDLC (lento, limitado a 65k linhas)

**Destino**: SUBSTITUÍDO
**Justificativa**: Relatórios dinâmicos com Pivot, múltiplos formatos (SPED, Excel, PDF, JSON), processamento assíncrono via Hangfire, sem limite de volume.
**Rastreabilidade**: RF-089 (RN-FIN-089-10), UC08-exportar-relatorios.md

---

### Tela: ConciliaBancaria.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/ConciliaBancaria.aspx`
- **Responsabilidade:** Conciliação manual de faturas com pagamentos bancários

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvFaturas` | GridView | - | Faturas pendentes de conciliação |
| `gvPagamentos` | GridView | - | Pagamentos em extrato bancário |
| `btnVincular` | Button | - | Vincula manualmente fatura × pagamento |

#### Comportamentos Implícitos

- Conciliação 100% manual (usuário seleciona fatura + pagamento)
- Sem matching automático por valor ou data
- Sem detecção de atrasos/adiantamentos
- Sem cálculo de juros e multas
- Pagamentos órfãos não são sinalizados
- Importação de extrato bancário feita em Excel separado

**Destino**: SUBSTITUÍDO
**Justificativa**: Conciliação bancária automática com matching de valor (±R$ 0,01) e data (±5 dias), cálculo de juros/multas, detecção de órfãos, integração com APIs bancárias.
**Rastreabilidade**: RF-089 (RN-FIN-089-08), UC07-conciliar-bancariamente.md

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSNotaFiscal.asmx

**Arquivo**: `ic1_legado/IControlIT/WebService/WSNotaFiscal.asmx.vb`

| Método | Responsabilidade | Parâmetros | Retorno | Observações |
|--------|------------------|------------|---------|-------------|
| `ObterNotaFiscal(id)` | Busca NF-e por ID | `id As Integer` | `DataTable` | Sem autenticação |
| `ListarNotasFiscais(filtro)` | Lista NFs com filtros | `filtro As FiltroNFe` | `DataTable` | Sem paginação, retorna todas |
| `ConciliarNFe(nfeId, pcId)` | Executa matching manual | `nfeId As Integer, pcId As Integer` | `Boolean` | Sem tolerâncias configuráveis |
| `AprovaDivergencia(divId, justificativa)` | Aprova divergência | `divId As Integer, justificativa As String` | `Boolean` | Sem validação de permissão |
| `RejeitaDivergencia(divId, justificativa)` | Rejeita divergência | `divId As Integer, justificativa As String` | `Boolean` | Sem validação de permissão |
| `ExportarRelatorio(filtro)` | Exporta dados para Excel | `filtro As FiltroRelatorio` | `Byte()` | Timeout em volume >10k |

**Problemas identificados:**
- Sem autenticação JWT (vulnerável a acesso não autorizado)
- Sem paginação (retorna todas as faturas, estouro de memória em >100k registros)
- Sem validação de permissões RBAC
- Métodos síncronos (timeout em operações demoradas)
- DataTable como retorno (acoplamento forte)

**Destino**: SUBSTITUÍDO
**Justificativa**: WebService ASMX substituído por REST API com autenticação JWT, paginação, RBAC, async/await, DTOs tipados.
**Rastreabilidade**: RF-089 (Seção 11 - Rastreabilidade), todos os endpoints `/api/v1/invoices/*`

---

## 4. TABELAS LEGADAS

### Tabela: tblNotaFiscalEletronica

**Schema**: `[dbo].[tblNotaFiscalEletronica]`

```sql
CREATE TABLE [dbo].[tblNotaFiscalEletronica](
    [Id] [int] IDENTITY(1,1) NOT NULL,
    [ChaveNFe] [varchar](44) NOT NULL,
    [NumeroNFe] [int] NOT NULL,
    [SerieNFe] [int] NOT NULL,
    [DataEmissao] [datetime] NOT NULL,
    [DataRecebimento] [datetime] NULL,
    [FornecedorCNPJ] [varchar](14) NOT NULL,
    [FornecedorRazaoSocial] [varchar](150) NOT NULL,
    [ClienteCNPJ] [varchar](14) NOT NULL,
    [ClienteRazaoSocial] [varchar](150) NOT NULL,
    [ValorTotal] [decimal](15,2) NOT NULL,
    [ValorICMS] [decimal](15,2) NULL,
    [ValorIPI] [decimal](15,2) NULL,
    [ValorFrete] [decimal](15,2) NULL,
    [PercentualDesconto] [decimal](5,2) NULL,
    [ValorDesconto] [decimal](15,2) NULL,
    [StatusConciliacao] [varchar](20) NOT NULL DEFAULT 'NaoConciliada',
    [PedidoCompraId] [int] NULL,
    [ContratoId] [int] NULL,
    [DataCriacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    [UsuarioCriacao] [varchar](100) NOT NULL,
    [DataAlteracao] [datetime] NULL,
    [UsuarioAlteracao] [varchar](100) NULL,
    CONSTRAINT [PK_tblNotaFiscalEletronica] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [UQ_ChaveNFe] UNIQUE NONCLUSTERED ([ChaveNFe] ASC),
    CONSTRAINT [FK_NotaFiscal_PedidoCompra] FOREIGN KEY ([PedidoCompraId])
        REFERENCES [dbo].[tblPedidoCompra]([Id])
)
```

**Problemas identificados:**
- SEM campo `ClienteId` (multi-tenancy): um banco por cliente, inviabiliza consolidação
- SEM campos de auditoria completa: apenas `UsuarioCriacao`, `DataAlteracao`, sem hash de integridade
- SEM soft delete: `Fl_Excluido` ausente, exclusão física (perda de dados)
- SEM índices em campos de filtro frequente: `DataEmissao`, `StatusConciliacao`, `FornecedorCNPJ`
- CNPJ armazenado em VARCHAR: deveria ser criptografado (LGPD)
- StatusConciliacao VARCHAR: deveria ser ENUM ou FK para tabela de status

**Destino**: SUBSTITUÍDO
**Justificativa**: Tabela redesenhada com multi-tenancy (ClienteId), auditoria completa (Created, Modified, hash), soft delete (Fl_Excluido), índices estratégicos, CNPJ criptografado.
**Rastreabilidade**: MD-RF089.md (Modelo de Dados), tabela `NotaFiscal` no moderno

---

### Tabela: tblNotaFiscalEletronicaItem

**Schema**: `[dbo].[tblNotaFiscalEletronicaItem]`

```sql
CREATE TABLE [dbo].[tblNotaFiscalEletronicaItem](
    [Id] [int] IDENTITY(1,1) NOT NULL,
    [NotaFiscalId] [int] NOT NULL,
    [NumeroSequencial] [int] NOT NULL,
    [CodigoProduto] [varchar](30) NOT NULL,
    [Descricao] [varchar](250) NOT NULL,
    [QuantidadeFaturada] [decimal](15,4) NOT NULL,
    [ValorUnitario] [decimal](15,2) NOT NULL,
    [ValorTotal] [decimal](15,2) NOT NULL,
    [CFOP] [varchar](4) NOT NULL,
    [AliquotaICMS] [decimal](5,2) NULL,
    [AliquotaIPI] [decimal](5,2) NULL,
    [ValorICMS] [decimal](15,2) NULL,
    [ValorIPI] [decimal](15,2) NULL,
    CONSTRAINT [PK_tblNotaFiscalEletronicaItem] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Item_NotaFiscal] FOREIGN KEY ([NotaFiscalId])
        REFERENCES [dbo].[tblNotaFiscalEletronica]([Id]) ON DELETE CASCADE
)
```

**Problemas identificados:**
- SEM validação de CFOP: VARCHAR(4) sem CHECK CONSTRAINT (aceita valores inválidos)
- SEM auditoria: itens alterados sem rastreamento
- Cascade delete: risco de perda de dados em exclusão acidental de NF-e
- SEM índice em `NotaFiscalId` (FK): performance ruim em JOINs

**Destino**: SUBSTITUÍDO
**Justificativa**: Tabela redesenhada com validação de CFOP (FK para tabela de CFOPs válidos), auditoria, soft delete, índices.
**Rastreabilidade**: MD-RF089.md, tabela `NotaFiscalItem`

---

### Tabela: tblDivergenciaFatura

**Schema**: `[dbo].[tblDivergenciaFatura]`

```sql
CREATE TABLE [dbo].[tblDivergenciaFatura](
    [Id] [int] IDENTITY(1,1) NOT NULL,
    [NotaFiscalId] [int] NOT NULL,
    [PedidoCompraId] [int] NULL,
    [TipoDivergencia] [varchar](50) NOT NULL,
    [Descricao] [nvarchar](500) NOT NULL,
    [ValorDivergencia] [decimal](15,2) NOT NULL,
    [Severidade] [varchar](20) NOT NULL,
    [StatusDivergencia] [varchar](20) NOT NULL DEFAULT 'Pendente',
    [DataDeteccao] [datetime] NOT NULL,
    [DataResolucao] [datetime] NULL,
    [UsuarioResolucao] [varchar](100) NULL,
    [JustificativaResolucao] [nvarchar](500) NULL,
    CONSTRAINT [PK_tblDivergenciaFatura] PRIMARY KEY CLUSTERED ([Id] ASC),
    CONSTRAINT [FK_Divergencia_NotaFiscal] FOREIGN KEY ([NotaFiscalId])
        REFERENCES [dbo].[tblNotaFiscalEletronica]([Id])
)
```

**Problemas identificados:**
- SEM campo `DataSLA`: sem controle de prazo de aprovação
- SEM campo `Roteadores`: workflow de aprovação não rastreável
- Severidade VARCHAR: sem validação de valores permitidos (CRÍTICA, ALTA, MÉDIA, BAIXA)
- SEM auditoria de quem CRIOU a divergência: apenas quem resolveu
- SEM hash de integridade: justificativa pode ser alterada sem rastreabilidade

**Destino**: SUBSTITUÍDO
**Justificativa**: Tabela redesenhada com `DataSLA`, `Roteadores`, Enum para Severidade, auditoria completa, hash SHA-512.
**Rastreabilidade**: MD-RF089.md, tabela `Divergencia`

---

### Tabela: tblMatchingDocumentos

**Schema**: `[dbo].[tblMatchingDocumentos]`

```sql
CREATE TABLE [dbo].[tblMatchingDocumentos](
    [Id] [int] IDENTITY(1,1) NOT NULL,
    [NotaFiscalId] [int] NOT NULL,
    [PedidoCompraId] [int] NULL,
    [RecebimentoMercadoriaId] [int] NULL,
    [StatusMatching] [varchar](20) NOT NULL,
    [PercentualConcordancia] [decimal](5,2) NOT NULL,
    [DataMatching] [datetime] NOT NULL,
    CONSTRAINT [PK_tblMatchingDocumentos] PRIMARY KEY CLUSTERED ([Id] ASC)
)
```

**Problemas identificados:**
- SEM campo `TipoMatching`: não diferencia two-way de three-way
- SEM auditoria: não registra quem executou o matching (manual ou automático)
- PercentualConcordancia: cálculo não documentado, sem rastreabilidade
- SEM campos de tolerância: tolerâncias hardcoded no código

**Destino**: SUBSTITUÍDO
**Justificativa**: Tabela redesenhada com `TipoMatching` (Enum), auditoria, `ToleranciaValor`, `ToleranciaQuantidade`.
**Rastreabilidade**: MD-RF089.md, tabela `Conciliacao`

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras NÃO documentadas encontradas no código VB.NET e stored procedures:

### RL-RN-001: Validação de CHAVE_NFE apenas em client-side

**Descrição**: CHAVE_NFE é validada apenas via JavaScript no browser, sem validação server-side robusta.
**Fonte**: `ConciliacaoNFe.aspx` - JavaScript inline
**Risco**: Usuário pode burlar validação e inserir CHAVE_NFE inválida

**Destino**: CORRIGIDO
**Justificativa**: Validação server-side obrigatória no Command Validator (FluentValidation), 44 dígitos + dígito verificador.
**Rastreabilidade**: RF-089 (RN-FIN-089-01)

---

### RL-RN-002: Matching exato de valor (sem tolerância)

**Descrição**: Matching de valor exige correspondência exata (`valorNFe <> valorPC`), sem tolerância configurável.
**Fonte**: `ConciliacaoNFe.aspx.vb` - método `btnConciliar_Click`
**Problema**: Diferenças de centavos (ex: arredondamento) geram divergências desnecessárias

**Destino**: CORRIGIDO
**Justificativa**: Tolerâncias configuráveis por empresa e tipo de item (absoluta R$ e percentual %).
**Rastreabilidade**: RF-089 (RN-FIN-089-03)

---

### RL-RN-003: Divergências tratadas igualmente (sem severidade)

**Descrição**: Todas as divergências são registradas como "sim/não", sem classificação de impacto.
**Fonte**: `pa_DetectarDivergencias` - stored procedure
**Problema**: Divergências críticas (ex: CFOP inválido) tratadas igual a divergências baixas (0,5%)

**Destino**: CORRIGIDO
**Justificativa**: Classificação automática em CRÍTICA, ALTA, MÉDIA, BAIXA conforme impacto financeiro e operacional.
**Rastreabilidade**: RF-089 (RN-FIN-089-02)

---

### RL-RN-004: Aprovação sem controle de permissões

**Descrição**: Qualquer usuário com acesso à tela pode aprovar divergências, sem validação de role.
**Fonte**: `DivergenciasAprovacao.aspx.vb` - método `btnAprovar_Click`
**Risco**: Usuário sem autoridade pode aprovar divergências críticas

**Destino**: CORRIGIDO
**Justificativa**: RBAC multi-nível com permissões específicas por severidade (ex: apenas Diretor aprova CRÍTICA).
**Rastreabilidade**: RF-089 (RN-FIN-089-06, Seção 9 - Segurança)

---

### RL-RN-005: Conciliação bancária 100% manual

**Descrição**: Vinculação de fatura × pagamento feita manualmente pelo usuário (sem automação).
**Fonte**: `ConciliaBancaria.aspx.vb` - método `btnVincular_Click`
**Problema**: 100% de trabalho manual, sujeito a erros, lentidão

**Destino**: CORRIGIDO
**Justificativa**: Conciliação bancária automática com matching de valor (±R$ 0,01) e data (±5 dias).
**Rastreabilidade**: RF-089 (RN-FIN-089-08)

---

### RL-RN-006: Relatórios hardcoded sem exportação SPED

**Descrição**: Relatórios gerados em RDLC (Report Builder), sem exportação SPED automatizada.
**Fonte**: `RelatorioFiscal.aspx` - ReportViewer
**Problema**: Não atende conformidade fiscal (SPED Fiscal E-100, E-200, E-310)

**Destino**: CORRIGIDO
**Justificativa**: Exportação SPED automatizada conforme layout da Receita Federal.
**Rastreabilidade**: RF-089 (RN-FIN-089-10)

---

### RL-RN-007: Auditoria simples (sem hash de integridade)

**Descrição**: Auditoria registra apenas usuário e data, sem hash SHA-512 para garantir integridade.
**Fonte**: Campos `UsuarioCriacao`, `DataCriacao` em `tblNotaFiscalEletronica`
**Risco**: Dados de auditoria podem ser alterados sem detecção

**Destino**: CORRIGIDO
**Justificativa**: Event sourcing com hash SHA-512 em TODOS os eventos de auditoria.
**Rastreabilidade**: RF-089 (RN-FIN-089-09)

---

### RL-RN-008: Sem detecção de anomalias (fraudes manuais)

**Descrição**: Detecção de fraudes/erros feita manualmente por revisão humana (sem ML).
**Fonte**: Não existe no legado
**Problema**: Alto risco de fraudes não detectadas, carga manual excessiva

**Destino**: IMPLEMENTADO
**Justificativa**: Modelo de Machine Learning treinado em 24 meses de histórico, score de anomalia >0.75 = revisar.
**Rastreabilidade**: RF-089 (RN-FIN-089-05)

---

### RL-RN-009: Matching apenas two-way (NF-e ↔ PC)

**Descrição**: Matching valida apenas NF-e vs PC, sem validar Recebimento de Mercadoria (RM).
**Fonte**: `pa_ConciliarNotaFiscal` - stored procedure
**Problema**: Não detecta divergências entre quantidade recebida e faturada

**Destino**: CORRIGIDO
**Justificativa**: Three-way matching obrigatório (NF-e ↔ PC ↔ RM).
**Rastreabilidade**: RF-089 (RN-FIN-089-03)

---

### RL-RN-010: Bloqueio de pagamento manual (sem automação)

**Descrição**: Bloqueio de fatura para pagamento feito manualmente via telefone/e-mail.
**Fonte**: Processo manual não sistematizado
**Problema**: Risco de pagamento de faturas divergentes

**Destino**: CORRIGIDO
**Justificativa**: Bloqueio automático de pagamentos em divergências CRÍTICAS e ALTAS, auditoria de tentativas de bypass.
**Rastreabilidade**: RF-089 (RN-FIN-089-07)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Matching** | Two-way manual | Two-way + Three-way automático | Automação com tolerâncias |
| **Severidade** | Não classificado | CRÍTICA, ALTA, MÉDIA, BAIXA | Priorização de recursos |
| **Workflow** | Manual (e-mail) | Automático (roteamento + SLA) | SignalR para notificações |
| **Anomalias** | Não detecta | ML com score de anomalia | Redução de fraudes |
| **Conciliação Bancária** | Manual (Excel) | Automática (matching ±R$ 0,01) | Eliminação de retrabalho |
| **Relatórios SPED** | Não gera | Geração automática | Conformidade fiscal |
| **Auditoria** | Simples (usuário/data) | Event sourcing + hash SHA-512 | Integridade garantida |
| **Multi-tenant** | Não (1 banco/cliente) | Sim (ClienteId) | Consolidação de dados |
| **Permissões** | Básica (sim/não) | RBAC multi-nível | Segurança por severidade |
| **Performance** | Timeout >50k faturas | Processamento assíncrono | Sem limite de volume |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migração de Stored Procedures para Application Layer

**Decisão**: Toda lógica de negócio em stored procedures será migrada para Application Layer (CQRS Handlers).
**Motivo**:
- Lógica de negócio em SQL é difícil de testar (sem testes unitários)
- Acoplamento forte com banco de dados
- Performance similar ou melhor com Entity Framework + índices estratégicos
**Impacto**: ALTO
**Rastreabilidade**: RF-089 (arquitetura Clean Architecture + CQRS)

---

### Decisão 2: Substituição de RDLC por relatórios dinâmicos

**Decisão**: Relatórios RDLC substituídos por exportação dinâmica (SPED, Excel, PDF, JSON).
**Motivo**:
- RDLC hardcoded, difícil customização
- Timeout em volume >10k faturas
- Não atende conformidade SPED
**Impacto**: MÉDIO
**Rastreabilidade**: RF-089 (RN-FIN-089-10)

---

### Decisão 3: Event Sourcing obrigatório para auditoria

**Decisão**: Substituir auditoria simples (campos Created/Modified) por Event Sourcing com hash SHA-512.
**Motivo**:
- Garantir integridade de dados (SOX, LGPD)
- Rastreabilidade completa de todas as operações
- Investigação de irregularidades
**Impacto**: ALTO
**Rastreabilidade**: RF-089 (RN-FIN-089-09)

---

### Decisão 4: Multi-tenancy com ClienteId

**Decisão**: Consolidar múltiplos bancos (1 por cliente) em banco único com ClienteId (Row-Level Security).
**Motivo**:
- Redução de custos de infraestrutura
- Facilita reporting consolidado
- Simplifica manutenção
**Impacto**: CRÍTICO
**Rastreabilidade**: RF-089 (Seção 9 - Segurança, isolamento multi-tenant)

---

### Decisão 5: Machine Learning para detecção de anomalias

**Decisão**: Implementar modelo de ML treinado em histórico de 24 meses.
**Motivo**:
- Reduzir fraudes não detectadas
- Reduzir carga manual de revisão
- Melhorar conformidade
**Impacto**: ALTO
**Rastreabilidade**: RF-089 (RN-FIN-089-05)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Perda de dados históricos | CRÍTICO | BAIXA | Script de migração com validação, backup completo antes |
| Performance degradada em consultas complexas | ALTO | MÉDIA | Índices estratégicos, cache Redis, paginação obrigatória |
| Resistência de usuários ao workflow automático | MÉDIO | ALTA | Treinamento, documentação, suporte 1:1 nas primeiras semanas |
| Falsos positivos em detecção de anomalias | MÉDIO | MÉDIA | Ajuste de threshold (>0.75), retreino mensal do modelo |
| Inconsistência em migração multi-tenant | CRÍTICO | MÉDIA | Validação de ClienteId em 100% dos registros, script de conferência |
| Timeout em exportação SPED (>100k faturas) | BAIXO | BAIXA | Processamento assíncrono via Hangfire, notificação por e-mail |

---

## 9. RASTREABILIDADE

### Legado → Moderno

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| `ConciliacaoNFe.aspx` | RF-089 (RN-FIN-089-01, RN-FIN-089-03) | SUBSTITUÍDO |
| `DivergenciasAprovacao.aspx` | RF-089 (RN-FIN-089-06) | SUBSTITUÍDO |
| `RelatorioFiscal.aspx` | RF-089 (RN-FIN-089-10) | SUBSTITUÍDO |
| `ConciliaBancaria.aspx` | RF-089 (RN-FIN-089-08) | SUBSTITUÍDO |
| `WSNotaFiscal.asmx` | Endpoints `/api/v1/invoices/*` | SUBSTITUÍDO |
| `pa_ConciliarNotaFiscal` | `ThreeWayMatchingEngine.cs` (CQRS Handler) | SUBSTITUÍDO |
| `pa_DetectarDivergencias` | `DivergenciaClassifier.cs` | SUBSTITUÍDO |
| `pa_GerarRelatorioFiscal` | `RelatorioFiscalExportService.cs` | SUBSTITUÍDO |
| `pa_AtualizarStatusDivergencia` | `DivergenciaWorkflowService.cs` | SUBSTITUÍDO |
| `tblNotaFiscalEletronica` | `NotaFiscal` (Entity moderno) | SUBSTITUÍDO |
| `tblDivergenciaFatura` | `Divergencia` (Entity moderno) | SUBSTITUÍDO |
| `tblMatchingDocumentos` | `Conciliacao` (Entity moderno) | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do documento de Referência ao Legado (RL-RF089) | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-31 10:30 UTC
**Próximo Passo**: Criar RL-RF089.yaml com rastreabilidade completa de destinos

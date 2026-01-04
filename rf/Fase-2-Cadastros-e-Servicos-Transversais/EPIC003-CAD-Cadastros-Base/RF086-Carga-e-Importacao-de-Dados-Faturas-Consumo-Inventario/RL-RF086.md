# RL-RF086 — Referência ao Legado: Carga e Importação de Dados

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agente de Migração de Documentação

**RF Moderno Relacionado:** RF-086
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de importação de faturas de operadoras, garantindo rastreabilidade histórica e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Cenário Geral

O sistema legado de Carga e Importação de Dados foi desenvolvido em **VB.NET + ASP.NET Web Forms** e operava de forma síncrona, bloqueando a interface do usuário durante o processamento de arquivos.

**Características Arquiteturais:**
- **Arquitetura:** Monolítica WebForms com Code-Behind VB.NET
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.5, SQL Server 2012
- **Banco de Dados:** SQL Server 2012 (`ICONTROLIT_LEGADO`)
- **Multi-tenant:** Não (um banco por cliente)
- **Auditoria:** Parcial (apenas datas de upload e processamento)
- **Configurações:** Web.config (hardcoded)
- **Processamento:** Síncrono (bloqueante)
- **Validações:** Manuais e inconsistentes
- **Rastreabilidade:** Log simples em tabela sem estrutura

### 1.2 Problemas Arquiteturais Identificados

1. **Ausência de Multi-Tenancy**: Cada cliente tinha um banco de dados separado, dificultando manutenção e escalabilidade
2. **Processamento Síncrono**: Upload de arquivos grandes bloqueava a interface por minutos
3. **Validações Inconsistentes**: Regras de validação hardcoded no code-behind, sem centralização
4. **Ausência de Engine de Glosa**: Glosas eram 100% manuais, sem detecção automática
5. **Falta de Conciliação Automática**: Comparação fatura vs consumo era manual
6. **Rastreabilidade Limitada**: Histórico de importações sem detalhamento de erros ou estatísticas
7. **Integração Manual com Faturamento**: Dados não eram enviados automaticamente para sistema de Notas Fiscais

---

## 2. BANCO DE DADOS LEGADO

### 2.1 Banco Principal

**Banco**: `ICONTROLIT_LEGADO` (SQL Server 2012)

### 2.2 Tabelas Legadas

#### Tabela: `[dbo].[FaturaOperadora]`

**Finalidade**: Armazenar dados principais de cada fatura importada.

**DDL (Reconstruído)**:
```sql
CREATE TABLE [dbo].[FaturaOperadora](
    [Id_Fatura] [int] IDENTITY(1,1) NOT NULL,
    [Id_Conglomerado] [int] NOT NULL,
    [Cd_Operadora] [varchar](10) NOT NULL, -- V=Vivo, C=Claro, T=TIM, O=Oi
    [Nm_Arquivo] [varchar](255) NOT NULL,
    [Nr_Fatura] [varchar](50) NOT NULL,
    [Dt_Fatura] [datetime] NOT NULL,
    [Vl_Total_Fatura] [numeric](15,2) NOT NULL,
    [Tp_Status] [varchar](20) NOT NULL, -- Pendente, Processada, Glosada, Aprovada
    [Dt_Upload] [datetime] NOT NULL,
    [Id_Usuario_Upload] [int] NOT NULL,
    [Dt_Processamento] [datetime] NULL,
    [Dt_Excluido] [datetime] NULL,
    CONSTRAINT [PK_FaturaOperadora] PRIMARY KEY CLUSTERED ([Id_Fatura] ASC),
    CONSTRAINT [FK_FaturaOperadora_Conglomerado] FOREIGN KEY ([Id_Conglomerado])
        REFERENCES [dbo].[Conglomerado]([Id_Conglomerado])
)
```

**Problemas Identificados**:
- ❌ Ausência de campos de auditoria completa (Created, CreatedBy, LastModified, LastModifiedBy)
- ❌ Status textual ao invés de enum/int (dificulta queries e manutenção)
- ❌ Soft delete por `Dt_Excluido` ao invés de flag booleana padronizada
- ❌ Sem hash SHA256 do arquivo (impossível detectar duplicação)
- ❌ Sem campo para rastrear quantidade de itens processados ou erros

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Tabela redesenhada como `ImportacaoEntity` com multi-tenancy, auditoria completa, hash SHA256, estatísticas de processamento e status enum tipado.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-008: Histórico Completo de Importações)
- MD Moderno: MD-RF086.md - Tabela `ImportacaoEntity`
- Migration EF Core: `20251231_CreateImportacaoEntity.cs` (pendente)

---

#### Tabela: `[dbo].[ItemFaturaOperadora]`

**Finalidade**: Armazenar itens individuais de cada fatura.

**DDL (Reconstruído)**:
```sql
CREATE TABLE [dbo].[ItemFaturaOperadora](
    [Id_ItemFatura] [int] IDENTITY(1,1) NOT NULL,
    [Id_Fatura] [int] NOT NULL,
    [Sq_Item] [int] NOT NULL,
    [Ds_Servico] [varchar](255) NOT NULL,
    [Qt_Consumo] [numeric](15,4) NOT NULL,
    [Vl_Unitario] [numeric](15,2) NOT NULL,
    [Vl_Subtotal] [numeric](15,2) NOT NULL,
    [Tp_Status] [varchar](20) NOT NULL, -- Validado, Glosado, Duplicado
    [Dt_Excluido] [datetime] NULL,
    CONSTRAINT [PK_ItemFaturaOperadora] PRIMARY KEY CLUSTERED ([Id_ItemFatura] ASC),
    CONSTRAINT [FK_ItemFaturaOperadora_Fatura] FOREIGN KEY ([Id_Fatura])
        REFERENCES [dbo].[FaturaOperadora]([Id_Fatura])
)
```

**Problemas Identificados**:
- ❌ Ausência de rastreamento de CDR individual (origem, destino, data/hora, duração)
- ❌ Sem campo de fingerprint para detecção de duplicação
- ❌ Sem FK para rastrear linha telefônica que consumiu
- ❌ Status textual ao invés de enum

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Tabela redesenhada como `CdrEntity` (Call Detail Record) com rastreamento completo de origem, fingerprint, FK para linha, status enum tipado.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-003: Registro de CDR com Rastreamento Completo)
- MD Moderno: MD-RF086.md - Tabela `CdrEntity`

---

#### Tabela: `[dbo].[GlosaFaturaOperadora]`

**Finalidade**: Registrar glosas (cobranças indevidas identificadas).

**DDL (Reconstruído)**:
```sql
CREATE TABLE [dbo].[GlosaFaturaOperadora](
    [Id_Glosa] [int] IDENTITY(1,1) NOT NULL,
    [Id_ItemFatura] [int] NOT NULL,
    [Ds_Motivo] [varchar](500) NOT NULL,
    [Tp_Glosa] [varchar](30) NOT NULL, -- Duplicacao, ValorOutlier, ServicoNaoAutorizado
    [Vl_Glosado] [numeric](15,2) NOT NULL,
    [Dt_Glosa] [datetime] NOT NULL,
    [Tp_Status] [varchar](20) NOT NULL, -- Pendente, Aprovada, Rejeitada
    [Dt_Excluido] [datetime] NULL,
    CONSTRAINT [PK_GlosaFaturaOperadora] PRIMARY KEY CLUSTERED ([Id_Glosa] ASC)
)
```

**Problemas Identificados**:
- ❌ Ausência de campo de evidência (justificativa técnica da glosa)
- ❌ Sem rastreamento de usuário que criou/aprovou a glosa
- ❌ Sem FK para regra de glosa aplicada (no caso de glosa automática)
- ❌ Status textual ao invés de enum

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Tabela redesenhada como `GlosaEntity` com campo de evidência, rastreamento de usuário, FK para regra aplicada (quando automática), status enum tipado.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-007: Glosa Automática de Cobranças Indevidas)
- MD Moderno: MD-RF086.md - Tabela `GlosaEntity`

---

## 3. STORED PROCEDURES LEGADAS

### 3.1 `[dbo].[pa_ImportarFatura]`

**Caminho**: `ic1_legado/Database/Procedures/pa_ImportarFatura.sql`

**Responsabilidade**: Iniciar processamento de fatura de operadora (síncrono, bloqueante).

**Parâmetros**:
- `@Id_Conglomerado INT`
- `@Cd_Operadora VARCHAR(10)`
- `@Nm_Arquivo VARCHAR(255)`
- `@Conteudo_Arquivo VARBINARY(MAX)`
- `@Id_Usuario_Upload INT`

**Lógica Principal (em linguagem natural)**:
1. Validar extensão do arquivo conforme operadora
2. Inserir registro em `FaturaOperadora` com status "Pendente"
3. Chamar parser específico conforme operadora (função VB.NET via CLR)
4. Inserir itens em `ItemFaturaOperadora`
5. Atualizar status para "Processada" ou "Errada"
6. Retornar ID da fatura criada

**Problemas**:
- ❌ Processamento síncrono (bloqueante)
- ❌ Sem retentativas automáticas em caso de falha
- ❌ Sem validação de hash SHA256 (duplicação)
- ❌ Sem conciliação automática
- ❌ Sem glosa automática

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Lógica movida para `ProcessarImportacaoHandler` (CQRS) com processamento assíncrono via Hangfire, retentativas automáticas, validação de hash, conciliação e glosa automáticas.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-010: Processamento Assíncrono via Hangfire)
- Handler Moderno: `ProcessarImportacaoHandler.cs` (pendente)

---

### 3.2 `[dbo].[pa_ValidarFatura]`

**Caminho**: `ic1_legado/Database/Procedures/pa_ValidarFatura.sql`

**Responsabilidade**: Validar totalizadores de fatura (subtotal, impostos, total).

**Parâmetros**:
- `@Id_Fatura INT`

**Lógica Principal**:
1. Calcular soma dos itens (`SUM(Vl_Subtotal)`)
2. Comparar com `Vl_Total_Fatura`
3. Se diferença > R$ 0,10 → marcar como "Errada"
4. Retornar 1 (válida) ou 0 (inválida)

**Problemas**:
- ❌ Margem de tolerância muito alta (R$ 0,10 ao invés de R$ 0,01)
- ❌ Validação de impostos e descontos não implementada
- ❌ Erros não detalhados (apenas flag 0/1)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Lógica movida para `IntegridadeValidator.cs` com margem de R$ 0,01, validação completa de impostos/descontos e mensagens de erro detalhadas.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-004: Validação de Integridade de Totalizações)
- Validator Moderno: `IntegridadeValidator.cs` (pendente)

---

### 3.3 `[dbo].[pa_GlosaAutomatica]`

**Caminho**: `ic1_legado/Database/Procedures/pa_GlosaAutomatica.sql`

**Responsabilidade**: Aplicar regras de glosa automática (limitado a duplicação).

**Parâmetros**:
- `@Id_Fatura INT`

**Lógica Principal**:
1. Detectar itens duplicados por `Ds_Servico + Vl_Subtotal`
2. Marcar duplicatas como `Tp_Status = 'Glosado'`
3. Inserir registro em `GlosaFaturaOperadora` com motivo "Duplicação"
4. Retornar quantidade de itens glosados

**Problemas**:
- ❌ Apenas detecta duplicação (sem regras de valor outlier, serviço não autorizado)
- ❌ Regras hardcoded (não configuráveis)
- ❌ Sem evidência técnica registrada
- ❌ Sem histórico de regra aplicada

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Lógica movida para `GlosaProcessor.cs` com engine de regras configurável (Pattern Strategy), suporte a múltiplas regras (duplicação, valor outlier, serviço não autorizado), evidência técnica e rastreamento de regra aplicada.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-007: Glosa Automática de Cobranças Indevidas)
- Processor Moderno: `GlosaProcessor.cs` + `IGlosaRule` interface (pendente)

---

### 3.4 `[dbo].[pa_ListarImportacoes]`

**Caminho**: `ic1_legado/Database/Procedures/pa_ListarImportacoes.sql`

**Responsabilidade**: Listar histórico de importações com filtros.

**Parâmetros**:
- `@Id_Conglomerado INT`
- `@Cd_Operadora VARCHAR(10)` (opcional)
- `@Dt_Inicio DATETIME` (opcional)
- `@Dt_Fim DATETIME` (opcional)

**Lógica Principal**:
1. `SELECT * FROM FaturaOperadora WHERE ...`
2. Aplicar filtros conforme parâmetros
3. Retornar dataset com histórico

**Problemas**:
- ❌ Sem paginação (retorna todos os registros)
- ❌ Sem ordenação configurável
- ❌ Sem estatísticas agregadas (quantidade de erros, glosados, etc.)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Lógica movida para `ListarImportacoesQuery` (CQRS) com paginação, ordenação configurável, estatísticas agregadas e filtros avançados.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 7 (Endpoint `GET /api/carga/importacoes`)
- Query Moderno: `ListarImportacoesQuery.cs` (pendente)

---

## 4. TELAS ASPX

### 4.1 `ImportarFatura.aspx`

**Caminho**: `ic1_legado/IControlIT/Carga/ImportarFatura.aspx`

**Responsabilidade**: Permitir upload de arquivo de fatura e iniciar processamento.

**Campos**:
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlOperadora` | DropDownList | Sim | Vivo, Claro, TIM, Oi |
| `fuArquivo` | FileUpload | Sim | Limite: 50MB |
| `btnUpload` | Button | - | Inicia processamento síncrono |

**Comportamentos Implícitos (Code-Behind VB.NET)**:
- Validação de extensão conforme operadora (Vivo: .xml, Claro: .txt, TIM: .pdf, Oi: .txt)
- Upload síncrono (bloqueia interface por minutos)
- Barra de progresso fake (não reflete processamento real)
- Sem validação de hash SHA256 (permite duplicação)
- Sem feedback em tempo real de status

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Substituído por componente Angular 19 (`importar-faturas.component.ts`) com upload assíncrono, validação de hash SHA256, feedback em tempo real via SignalR e suporte a múltiplos uploads simultâneos.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 4 (F01 - Importação de Arquivo de Fatura)
- UC Moderno: UC01-criar-importacao
- Componente Angular: `/carga/importar-faturas` (pendente)

---

### 4.2 `ListarImportacoes.aspx`

**Caminho**: `ic1_legado/IControlIT/Carga/ListarImportacoes.aspx`

**Responsabilidade**: Exibir histórico de importações com filtros.

**Campos**:
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `ddlOperadora` | DropDownList | Não | Filtro por operadora |
| `txtDataInicio` | TextBox (Date) | Não | Filtro por período |
| `txtDataFim` | TextBox (Date) | Não | Filtro por período |
| `gvImportacoes` | GridView | - | Lista de importações |

**Comportamentos Implícitos**:
- Sem paginação (exibe todos os registros, problema de performance)
- Sem ordenação configurável
- Sem exportação para Excel/PDF
- Atualização manual (sem auto-refresh)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Substituído por componente Angular 19 (`historico-importacoes.component.ts`) com paginação server-side, ordenação configurável, exportação para Excel/PDF e atualização em tempo real via SignalR.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 4 (F08 - Histórico de Importações)
- UC Moderno: UC00-listar-importacoes
- Componente Angular: `/carga/historico-importacoes` (pendente)

---

### 4.3 `GlosaManual.aspx`

**Caminho**: `ic1_legado/IControlIT/Carga/GlosaManual.aspx`

**Responsabilidade**: Permitir aprovação/rejeição manual de glosas.

**Campos**:
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvGlosas` | GridView | - | Lista de glosas pendentes |
| `btnAprovar` | Button | - | Aprovar glosa selecionada |
| `btnRejeitar` | Button | - | Rejeitar glosa selecionada |
| `txtMotivo` | TextBox | Não | Motivo de rejeição |

**Comportamentos Implícitos**:
- Sem aprovação em lote (apenas uma glosa por vez)
- Sem evidência técnica exibida
- Sem histórico de aprovações/rejeições anteriores
- Motivo de rejeição opcional (deveria ser obrigatório)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Substituído por componente Angular 19 (`glosa-manual.component.ts`) com aprovação em lote, exibição de evidência técnica, histórico de aprovações/rejeições e motivo obrigatório para rejeição.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 7 (Endpoints de Glosa)
- UC Moderno: UC04-aprovar-glosa
- Componente Angular: `/carga/glosa-manual` (pendente)

---

## 5. WEBSERVICES LEGADOS (VB.NET)

### 5.1 `WSImportacaoFatura.asmx`

**Caminho**: `ic1_legado/IControlIT/WebService/WSImportacaoFatura.asmx.vb`

**Responsabilidade**: Expor operações de importação via SOAP.

**Métodos Públicos**:

#### 5.1.1 `ImportarFatura(nomeArquivo As String, conteudoBase64 As String) As Integer`

**Parâmetros**:
- `nomeArquivo`: Nome do arquivo original
- `conteudoBase64`: Conteúdo do arquivo em Base64

**Retorno**: ID da fatura criada ou -1 (erro)

**Lógica**:
1. Decodificar Base64 para bytes
2. Validar extensão do arquivo
3. Chamar `pa_ImportarFatura`
4. Retornar ID ou -1

**Problemas**:
- ❌ Sem autenticação/autorização (qualquer cliente pode chamar)
- ❌ Processamento síncrono (timeout após 2 minutos)
- ❌ Sem validação de tamanho (permite arquivos gigantes)
- ❌ Retorno ambíguo (-1 não detalha erro)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Substituído por REST API endpoint `POST /api/carga/importacoes` com autenticação JWT, autorização RBAC, validação de tamanho (50MB), processamento assíncrono via Hangfire e retorno detalhado de erros (HTTP status codes + DTO).

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 7 (Endpoint `POST /api/carga/importacoes`)
- Endpoint Moderno: `POST /api/carga/importacoes` (pendente)

---

#### 5.1.2 `ObtenerStatusImportacao(idImportacao As Integer) As String`

**Parâmetros**:
- `idImportacao`: ID da importação

**Retorno**: Status textual ("Pendente", "Processada", "Errada")

**Problemas**:
- ❌ Sem detalhamento de erro (apenas status textual)
- ❌ Sem estatísticas de processamento (quantidade de itens, erros, glosados)
- ❌ Atualização manual (sem real-time)

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Substituído por REST API endpoint `GET /api/carga/importacoes/{id}/status` com DTO detalhado (status enum, estatísticas, erros) e suporte a SignalR para atualizações em tempo real.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 7 (Endpoint `GET /api/carga/importacoes/{id}/status`)
- Endpoint Moderno: `GET /api/carga/importacoes/{id}/status` (pendente)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Extensão de Arquivo Conforme Operadora

**Descrição**: Cada operadora possui formato de arquivo específico. Sistema valida extensão antes de processamento.

**Fonte**: `ImportarFatura.aspx.vb` - Linhas 45-60 (code-behind VB.NET)

**Código Original (VB.NET)**:
```vb
If ddlOperadora.SelectedValue = "V" And Not fuArquivo.FileName.EndsWith(".xml") Then
    lblErro.Text = "Operadora Vivo: somente arquivos XML (.xml)"
    Return
ElseIf ddlOperadora.SelectedValue = "C" And Not (fuArquivo.FileName.EndsWith(".txt") Or fuArquivo.FileName.EndsWith(".edi")) Then
    lblErro.Text = "Operadora Claro: somente arquivos TXT ou EDI"
    Return
' ... (TIM, Oi)
End If
```

**Regra Extraída (Linguagem Natural)**:
- Vivo: Somente .xml
- Claro: Somente .txt ou .edi
- TIM: Somente .pdf
- Oi: Somente .txt ou .edi

**Destino**: **ASSUMIDO**
**Justificativa**: Regra mantida e documentada formalmente no sistema moderno.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-001: Validação de Formato de Arquivo)
- Regra Moderna: RN-CRG-086-001
- Validador: `FileValidator.cs` (pendente)

---

### RL-RN-002: Limite de Tamanho de Arquivo (50MB)

**Descrição**: Arquivos maiores que 50MB são rejeitados para evitar timeout e problemas de performance.

**Fonte**: `Web.config` - `<httpRuntime maxRequestLength="51200" />` (50MB em KB)

**Destino**: **ASSUMIDO**
**Justificativa**: Regra mantida no sistema moderno (definida em `appsettings.json`).

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-001: Validação de Formato de Arquivo)
- Configuração Moderna: `appsettings.json` - `CargaImportacao:TamanhoMaximoArquivoMb` = 50

---

### RL-RN-003: Margem de Tolerância em Validação de Totalizadores

**Descrição**: Sistema legado aceitava diferença de até R$ 0,10 entre subtotal calculado e subtotal informado na fatura.

**Fonte**: `pa_ValidarFatura.sql` - Linha 15

**Código Original (SQL)**:
```sql
IF ABS(@SubtotalCalculado - @SubtotalInformado) > 0.10
BEGIN
    UPDATE FaturaOperadora SET Tp_Status = 'Errada' WHERE Id_Fatura = @Id_Fatura
    RETURN 0
END
```

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Margem muito alta. Sistema moderno utiliza R$ 0,01 para maior precisão.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-004: Validação de Integridade de Totalizações)
- Regra Moderna: Margem de R$ 0,01
- Validador: `IntegridadeValidator.cs` (pendente)

---

### RL-RN-004: Detecção de Duplicação por Descrição + Valor

**Descrição**: Sistema legado detectava duplicação comparando `Ds_Servico + Vl_Subtotal`.

**Fonte**: `pa_GlosaAutomatica.sql` - Linhas 10-25

**Código Original (SQL)**:
```sql
SELECT Id_ItemFatura, COUNT(*) AS QtdDuplicatas
FROM ItemFaturaOperadora
WHERE Id_Fatura = @Id_Fatura
GROUP BY Ds_Servico, Vl_Subtotal
HAVING COUNT(*) > 1
```

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Sistema moderno utiliza fingerprint (hash de descrição + valor + data) para detecção mais precisa, incluindo duplicação inter-faturas.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-005: Detecção de Cobranças Duplicadas)
- Regra Moderna: Fingerprint SHA256 de (descrição + valor + data)
- Detector: `DuplicacaoDetector.cs` (pendente)

---

### RL-RN-005: Processamento Síncrono Bloqueante

**Descrição**: Sistema legado processava importações de forma síncrona, bloqueando a interface do usuário até conclusão.

**Fonte**: `ImportarFatura.aspx.vb` - Botão "Upload" executa chamada síncrona

**Destino**: **SUBSTITUÍDO**
**Justificativa**: Processamento síncrono causa timeout e má experiência do usuário. Sistema moderno utiliza Hangfire para processamento assíncrono com feedback em tempo real.

**Rastreabilidade**:
- RF Moderno: RF-086 - Seção 5 (RN-CRG-086-010: Processamento Assíncrono via Hangfire)
- Processador Moderno: `ProcessadorImportacaoHangfire.cs` (pendente)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Existe no Legado | Existe no Moderno | Observação |
|------|------------------|-------------------|------------|
| Upload de arquivo | ✓ | ✓ | Moderno: assíncrono, multi-upload |
| Validação de formato | ✓ (parcial) | ✓ (completa) | Moderno: hash SHA256, encoding |
| Parsing por operadora | ✓ | ✓ | Moderno: Pattern Strategy |
| Extração de CDRs | ✓ (limitado) | ✓ (completo) | Moderno: rastreamento completo |
| Validação de integridade | ✓ (R$ 0,10) | ✓ (R$ 0,01) | Moderno: mais preciso |
| Detecção de duplicação | ✓ (intra-fatura) | ✓ (intra + inter) | Moderno: fingerprint SHA256 |
| Conciliação automática | ✗ | ✓ | Nova funcionalidade |
| Glosa automática | ✓ (só duplicação) | ✓ (engine configurável) | Moderno: múltiplas regras |
| Processamento assíncrono | ✗ | ✓ | Nova funcionalidade |
| Retentativas automáticas | ✗ | ✓ | Nova funcionalidade |
| Histórico detalhado | ✓ (básico) | ✓ (completo) | Moderno: estatísticas, erros |
| Integração com Faturamento | ✗ (manual) | ✓ (automática) | Nova funcionalidade |
| Multi-tenant | ✗ | ✓ | Nova arquitetura |
| Auditoria completa | ✓ (parcial) | ✓ (completa) | Moderno: antes/depois, IP, usuário |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Processamento Assíncrono Obrigatório

**Descrição**: Todo processamento de importação DEVE ser assíncrono via Hangfire.

**Motivo**: Processamento síncrono do legado causava timeout, bloqueio de interface e má experiência do usuário. Hangfire permite múltiplos uploads simultâneos e feedback em tempo real.

**Impacto**: ALTO

**Data**: 2025-12-31

---

### Decisão 2: Hash SHA256 para Detecção de Duplicação

**Descrição**: Todo arquivo DEVE ter hash SHA256 calculado e armazenado.

**Motivo**: Sistema legado não detectava arquivos duplicados (mesmo arquivo importado 2x). Hash SHA256 garante detecção imediata.

**Impacto**: MÉDIO

**Data**: 2025-12-31

---

### Decisão 3: Margem de Tolerância Reduzida (R$ 0,10 → R$ 0,01)

**Descrição**: Margem de tolerância em validação de totalizadores reduzida de R$ 0,10 para R$ 0,01.

**Motivo**: Margem de R$ 0,10 é muito alta e pode ocultar erros reais de parsing ou inconsistências na fatura.

**Impacto**: MÉDIO

**Data**: 2025-12-31

---

### Decisão 4: Engine de Glosa Configurável

**Descrição**: Glosas automáticas DEVEM ser aplicadas via engine configurável (Pattern Strategy).

**Motivo**: Sistema legado tinha regras hardcoded (apenas duplicação). Engine configurável permite criar regras customizadas por cliente sem alterar código.

**Impacto**: ALTO

**Data**: 2025-12-31

---

### Decisão 5: Integração Automática com RF032

**Descrição**: Dados validados DEVEM ser automaticamente enviados para RF032 (Notas Fiscais).

**Motivo**: Sistema legado exigia reentrada manual de dados. Integração automática elimina erros humanos e acelera processo.

**Impacto**: ALTO

**Data**: 2025-12-31

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Parsers podem não extrair 100% dos dados de arquivos legados | ALTO | MÉDIA | Testar com arquivos reais de todas as operadoras antes de ir para produção |
| Margem de tolerância mais baixa (R$ 0,01) pode rejeitar faturas válidas | MÉDIO | BAIXA | Permitir ajuste manual de margem via configuração |
| Hangfire pode acumular fila em caso de falha repetida | MÉDIO | MÉDIA | Implementar alerta quando fila > 100 jobs + aumentar workers |
| Integração com RF032 pode falhar e bloquear fluxo | ALTO | BAIXA | Implementar retentativas automáticas + marcar como "AguardandoAprovacao" após 3 falhas |
| Usuários podem estranhar processamento assíncrono | BAIXO | ALTA | Implementar feedback em tempo real via SignalR + notificações |
| Fingerprint SHA256 pode gerar falsos positivos de duplicação | BAIXO | BAIXA | Permitir reprocessamento manual de importações marcadas como duplicadas |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status |
|-----------------|---------------|---------------|--------|
| Tabela `FaturaOperadora` | RN-CRG-086-008 | UC01-criar-importacao | SUBSTITUÍDO |
| Tabela `ItemFaturaOperadora` | RN-CRG-086-003 | UC02-visualizar-importacao | SUBSTITUÍDO |
| Tabela `GlosaFaturaOperadora` | RN-CRG-086-007 | UC04-aprovar-glosa | SUBSTITUÍDO |
| Stored Procedure `pa_ImportarFatura` | RN-CRG-086-010 | UC01-criar-importacao | SUBSTITUÍDO |
| Stored Procedure `pa_ValidarFatura` | RN-CRG-086-004 | UC01-criar-importacao | SUBSTITUÍDO |
| Stored Procedure `pa_GlosaAutomatica` | RN-CRG-086-007 | UC04-aprovar-glosa | SUBSTITUÍDO |
| Stored Procedure `pa_ListarImportacoes` | Endpoint GET /api/carga/importacoes | UC00-listar-importacoes | SUBSTITUÍDO |
| Tela `ImportarFatura.aspx` | F01 - Importação de Arquivo | UC01-criar-importacao | SUBSTITUÍDO |
| Tela `ListarImportacoes.aspx` | F08 - Histórico de Importações | UC00-listar-importacoes | SUBSTITUÍDO |
| Tela `GlosaManual.aspx` | Endpoints de Glosa | UC04-aprovar-glosa | SUBSTITUÍDO |
| WebService `WSImportacaoFatura.asmx` | POST /api/carga/importacoes | UC01-criar-importacao | SUBSTITUÍDO |
| Regra: Extensão por operadora | RN-CRG-086-001 | UC01-criar-importacao | ASSUMIDO |
| Regra: Limite 50MB | RN-CRG-086-001 | UC01-criar-importacao | ASSUMIDO |
| Regra: Margem R$ 0,10 | RN-CRG-086-004 | UC01-criar-importacao | SUBSTITUÍDO (R$ 0,01) |
| Regra: Duplicação por Descrição+Valor | RN-CRG-086-005 | UC04-aprovar-glosa | SUBSTITUÍDO (Fingerprint) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do RL-RF086 com extração completa de memória legado do RF v1.0 | Agente de Migração de Documentação |

---

**Última Atualização**: 2025-12-31
**Versão de Governança**: 2.0 (Separação RF/RL)
**Autor**: Agente de Migração de Documentação
**Revisão**: Pendente

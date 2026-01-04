# Modelo de Dados - RF026: Gestão Completa de Faturas de Telecom e TI

**Versão:** 1.0
**Data:** 18/12/2025
**RF Relacionado:** [RF026 - Gestão Completa de Faturas de Telecom e TI](./RF026.md)
**Banco de Dados:** SQL Server / SQLite

---

## 1. Diagrama de Entidades

```
┌──────────────────────┐         ┌──────────────────────────┐
│      Clientes        │         │        Faturas           │
├──────────────────────┤         ├──────────────────────────┤
│ Id (PK)              │────┐    │ Id (PK)                  │
│ Nome                 │    │    │ ClienteId (FK)           │──┐
│ ...                  │    └───>│ EmpresaId (FK)           │  │
└──────────────────────┘         │ OperadoraId (FK)         │  │
                                 │ NumeroFatura             │  │
                                 │ DataEmissao              │  │
                                 │ DataVencimento           │  │
┌──────────────────────┐         │ PeriodoReferencia        │  │
│     Empresas         │         │ ValorTotalBruto          │  │
├──────────────────────┤         │ Descontos                │  │
│ Id (PK)              │<────────│ Acrescimos               │  │
│ ClienteId (FK)       │         │ ValorTotalLiquido        │  │
│ Nome                 │         │ Status                   │  │
│ ...                  │         │ NumeroVersao             │  │
└──────────────────────┘         │ VersaoAtualFlag          │  │
                                 │ OcrConfidence            │  │
                                 │ OcrRawJson               │  │
┌──────────────────────┐         │ ErpSincronizado          │  │
│    Operadoras        │         │ ErpDocumentoNumero       │  │
├──────────────────────┤         │ Ativo                    │  │
│ Id (PK)              │<────────│ CreatedAt                │  │
│ ClienteId (FK)       │         │ CreatedBy (FK)           │  │
│ Nome                 │         │ ModifiedAt               │  │
│ CNPJ                 │         │ ModifiedBy (FK)          │  │
│ TipoOperadora        │         └──────────────────────────┘  │
│ ...                  │                      │                │
└──────────────────────┘                      │                │
                                              │                │
┌──────────────────────────┐                  │                │
│   Faturas_Detalhe        │<─────────────────┘                │
├──────────────────────────┤                                   │
│ Id (PK)                  │                                   │
│ FaturaId (FK)            │                                   │
│ NumeroLinha              │                                   │
│ DescricaoServico         │                                   │
│ ConsumoQuantidade        │                                   │
│ ValorUnitario            │                                   │
│ ValorTotal               │                                   │
│ Conciliado               │                                   │
│ ContratoItemId (FK)      │                                   │
│ AtivoId (FK)             │                                   │
│ MatchScore               │                                   │
│ AuditoriaStatus          │                                   │
│ AuditoriaRegrasFalhas    │                                   │
│ RateioCentroCustoId (FK) │                                   │
│ RateioProjetoId (FK)     │                                   │
│ CreatedAt                │                                   │
└──────────────────────────┘                                   │
                                                               │
┌──────────────────────────────┐                               │
│  Faturas_Importacao_Template │                               │
├──────────────────────────────┤                               │
│ Id (PK)                      │                               │
│ ClienteId (FK)               │                               │
│ NomeTemplate                 │                               │
│ OperadoraId (FK)             │                               │
│ Formato                      │                               │
│ MapeamentoColunasJson        │                               │
│ RegrasTransformacaoJson      │                               │
│ Ativo                        │                               │
│ CreatedAt                    │                               │
└──────────────────────────────┘                               │
                                                               │
┌─────────────────────────────┐                                │
│   Faturas_Importacao_Log    │<───────────────────────────────┘
├─────────────────────────────┤
│ Id (PK)                     │
│ FaturaId (FK)               │
│ ClienteId (FK)              │
│ ArquivoNome                 │
│ TemplateUsadoId (FK)        │
│ LinhasTotal                 │
│ LinhasSucesso               │
│ LinhasErro                  │
│ ErrosJson                   │
│ DataImportacao              │
│ UsuarioId (FK)              │
└─────────────────────────────┘

┌─────────────────────────────┐         ┌──────────────────────────────┐
│  Faturas_Auditoria_Regra    │         │  Faturas_Auditoria_Resultado │
├─────────────────────────────┤         ├──────────────────────────────┤
│ Id (PK)                     │────┐    │ Id (PK)                      │
│ ClienteId (FK)              │    │    │ FaturaId (FK)                │
│ NomeRegra                   │    └───>│ RegraId (FK)                 │
│ Descricao                   │         │ Passou                       │
│ Severidade                  │         │ ValorSuspeito                │
│ CondicaoSql                 │         │ MensagemDetalhada            │
│ Ativa                       │         │ DataExecucao                 │
│ ParametrosJson              │         └──────────────────────────────┘
│ CreatedAt                   │
└─────────────────────────────┘

┌───────────────────────────┐         ┌───────────────────────────────┐
│  Faturas_Contestacao      │         │  Faturas_Contestacao_Historico│
├───────────────────────────┤         ├───────────────────────────────┤
│ Id (PK)                   │────┐    │ Id (PK)                       │
│ FaturaId (FK)             │    │    │ ContestacaoId (FK)            │
│ ClienteId (FK)            │    └───>│ StatusAnterior                │
│ ItensContestadosJson      │         │ StatusNovo                    │
│ ValorTotalContestado      │         │ UsuarioId (FK)                │
│ StatusWorkflow            │         │ Observacoes                   │
│ TipoContestacao           │         │ DataAlteracao                 │
│ MotivoDetalhado           │         └───────────────────────────────┘
│ AprovadorInternoId (FK)   │
│ DataEnvioOperadora        │
│ RespostaOperadora         │
│ CreditoRecebido           │
│ DataFechamento            │
│ CreatedAt                 │
│ CreatedBy (FK)            │
└───────────────────────────┘

┌───────────────────────────┐         ┌──────────────────────────┐
│  Faturas_Rateio_Regra     │         │  Faturas_Rateio_Item     │
├───────────────────────────┤         ├──────────────────────────┤
│ Id (PK)                   │────┐    │ Id (PK)                  │
│ ClienteId (FK)            │    │    │ FaturaId (FK)            │
│ NomeRegra                 │    └───>│ RegraRateioId (FK)       │
│ TipoRateio                │         │ DimensaoTipo             │
│ DimensoesJson             │         │ DimensaoId               │
│ PercentuaisJson           │         │ Percentual               │
│ Ativa                     │         │ Valor                    │
│ CreatedAt                 │         │ CreatedAt                │
└───────────────────────────┘         └──────────────────────────┘

┌───────────────────────────┐
│  Faturas_Anexos           │
├───────────────────────────┤
│ Id (PK)                   │
│ FaturaId (FK)             │
│ ClienteId (FK)            │
│ TipoDocumento             │
│ AzureBlobUrl              │
│ Sha256Hash                │
│ TamanhoBytes              │
│ DataUpload                │
│ UsuarioId (FK)            │
└───────────────────────────┘

┌───────────────────────────┐
│  Faturas_Aprovacao        │
├───────────────────────────┤
│ Id (PK)                   │
│ FaturaId (FK)             │
│ ClienteId (FK)            │
│ NivelAprovacao            │
│ AprovadorId (FK)          │
│ Status                    │
│ JustificativaRejeicao     │
│ DocusignEnvelopeId        │
│ DataAssinatura            │
│ CreatedAt                 │
└───────────────────────────┘

┌───────────────────────────┐
│  Faturas_Kpi_Snapshot     │
├───────────────────────────┤
│ Id (PK)                   │
│ ClienteId (FK)            │
│ DataSnapshot              │
│ GastoTotal                │
│ TaxaConciliacao           │
│ TaxaAuditoria             │
│ ValorContestado           │
│ CreatedAt                 │
└───────────────────────────┘

┌───────────────────────────┐
│  Faturas_Previsao_Ml      │
├───────────────────────────┤
│ Id (PK)                   │
│ ClienteId (FK)            │
│ MesReferencia             │
│ ValorPrevisto             │
│ ConfidenceInterval        │
│ AlertasGeradosJson        │
│ DataPrevisao              │
└───────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: Faturas

**Descrição:** Armazena dados principais de cada fatura de telecom/TI importada, incluindo valores, datas, status do workflow e metadados de OCR.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes (multi-tenancy) |
| EmpresaId | UNIQUEIDENTIFIER | NÃO | - | FK para Empresas (filial responsável) |
| OperadoraId | UNIQUEIDENTIFIER | NÃO | - | FK para Operadoras (Vivo, Claro, TIM, etc.) |
| NumeroFatura | NVARCHAR(100) | NÃO | - | Número único da fatura da operadora |
| DataEmissao | DATETIME2 | NÃO | - | Data de emissão da fatura |
| DataVencimento | DATETIME2 | NÃO | - | Data de vencimento |
| PeriodoReferencia | NVARCHAR(7) | NÃO | - | Período de referência (formato: YYYY-MM) |
| ValorTotalBruto | DECIMAL(18,2) | NÃO | 0 | Valor total sem descontos |
| Descontos | DECIMAL(18,2) | NÃO | 0 | Descontos aplicados |
| Acrescimos | DECIMAL(18,2) | NÃO | 0 | Multas, juros |
| ValorTotalLiquido | DECIMAL(18,2) | NÃO | 0 | Valor final a pagar |
| Icms | DECIMAL(18,2) | NÃO | 0 | Valor ICMS |
| Pis | DECIMAL(18,2) | NÃO | 0 | Valor PIS |
| Cofins | DECIMAL(18,2) | NÃO | 0 | Valor COFINS |
| Iss | DECIMAL(18,2) | NÃO | 0 | Valor ISS |
| Status | NVARCHAR(50) | NÃO | 'Rascunho' | Enum: Rascunho, Conciliacao, Auditoria, Aprovacao, Aprovada, Paga, Contestada, Cancelada |
| NumeroVersao | INT | NÃO | 1 | Número da versão da fatura |
| VersaoAtualFlag | BIT | NÃO | 1 | Flag indicando se é a versão atual |
| MotivoAlteracaoVersao | NVARCHAR(500) | SIM | NULL | Motivo da criação de nova versão (obrigatório se v2+) |
| OcrConfidence | DECIMAL(5,2) | SIM | NULL | Confiança média do OCR (0-100%) |
| OcrRawJson | NVARCHAR(MAX) | SIM | NULL | Dados brutos do Azure Form Recognizer |
| ErpSincronizado | BIT | NÃO | 0 | Flag indicando sincronização com ERP |
| ErpDocumentoNumero | NVARCHAR(50) | SIM | NULL | Número do documento no ERP |
| ErpDataSincronizacao | DATETIME2 | SIM | NULL | Data/hora sincronização ERP |
| ArquivoOriginalUrl | NVARCHAR(500) | SIM | NULL | URL do arquivo original no Azure Blob Storage |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações gerais |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_ClienteId | ClienteId | NONCLUSTERED | Performance multi-tenant |
| IX_Faturas_EmpresaId | EmpresaId | NONCLUSTERED | Filtro por empresa |
| IX_Faturas_OperadoraId | OperadoraId | NONCLUSTERED | Filtro por operadora |
| IX_Faturas_Status | Status | NONCLUSTERED | Filtro por status workflow |
| IX_Faturas_DataEmissao | DataEmissao DESC | NONCLUSTERED | Ordenação temporal |
| IX_Faturas_PeriodoReferencia | PeriodoReferencia | NONCLUSTERED | Consultas por período |
| IX_Faturas_NumeroVersao | NumeroFatura, NumeroVersao | NONCLUSTERED | Controle de versões |
| IX_Faturas_VersaoAtual | VersaoAtualFlag, ClienteId | FILTERED WHERE VersaoAtualFlag = 1 | Queries versão atual |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_EmpresaId | FOREIGN KEY | EmpresaId REFERENCES Empresas(Id) | Empresa responsável |
| FK_Faturas_OperadoraId | FOREIGN KEY | OperadoraId REFERENCES Operadoras(Id) | Operadora |
| FK_Faturas_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuarios(Id) | Auditoria criação |
| UQ_Faturas_Numero | UNIQUE | (ClienteId, OperadoraId, NumeroFatura, NumeroVersao) | Fatura única por versão |
| CHK_Faturas_Status | CHECK | Status IN ('Rascunho', 'Conciliacao', 'Auditoria', 'Aprovacao', 'Aprovada', 'Paga', 'Contestada', 'Cancelada') | Valores válidos |
| CHK_Faturas_ValorLiquido | CHECK | ValorTotalLiquido >= 0 | Valor não negativo |

---

### 2.2 Tabela: Faturas_Detalhe

**Descrição:** Detalhamento das linhas/ativos cobrados em cada fatura, incluindo status de conciliação, auditoria e rateio.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| NumeroLinha | NVARCHAR(100) | NÃO | - | Número linha/ativo cobrado |
| DescricaoServico | NVARCHAR(500) | NÃO | - | Descrição serviço |
| ConsumoQuantidade | DECIMAL(18,4) | SIM | NULL | Quantidade consumida |
| UnidadeMedida | NVARCHAR(50) | SIM | NULL | Unidade (minutos, GB, licenças) |
| ValorUnitario | DECIMAL(18,4) | SIM | NULL | Valor unitário |
| ValorTotal | DECIMAL(18,2) | NÃO | 0 | Valor total do item |
| Conciliado | BIT | NÃO | 0 | Flag indicando conciliação |
| ContratoItemId | UNIQUEIDENTIFIER | SIM | NULL | FK para item de contrato |
| AtivoId | UNIQUEIDENTIFIER | SIM | NULL | FK para ativo (linha, chip, licença) |
| MatchScore | DECIMAL(5,2) | SIM | NULL | Score de similaridade (0-100%) |
| AuditoriaStatus | NVARCHAR(50) | SIM | NULL | Enum: Aprovado, Alerta, Critico |
| AuditoriaRegrasFalhas | NVARCHAR(MAX) | SIM | NULL | JSON com regras que falharam |
| RateioCentroCustoId | UNIQUEIDENTIFIER | SIM | NULL | FK para centro custo |
| RateioProjetoId | UNIQUEIDENTIFIER | SIM | NULL | FK para projeto |
| RateioDepartamentoId | UNIQUEIDENTIFIER | SIM | NULL | FK para departamento |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Detalhe_FaturaId | FaturaId | NONCLUSTERED | Joins com Faturas |
| IX_Faturas_Detalhe_NumeroLinha | NumeroLinha | NONCLUSTERED | Busca por linha |
| IX_Faturas_Detalhe_Conciliado | Conciliado | NONCLUSTERED | Filtro conciliação |
| IX_Faturas_Detalhe_AuditoriaStatus | AuditoriaStatus | NONCLUSTERED | Filtro auditoria |
| IX_Faturas_Detalhe_ContratoItemId | ContratoItemId | NONCLUSTERED | Relacionamento contrato |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Detalhe | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Detalhe_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) ON DELETE CASCADE | Detalhe pertence a fatura |
| FK_Faturas_Detalhe_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuarios(Id) | Auditoria |
| CHK_Faturas_Detalhe_ValorTotal | CHECK | ValorTotal >= 0 | Valor não negativo |

---

### 2.3 Tabela: Faturas_Importacao_Template

**Descrição:** Templates configuráveis para importação de faturas de diferentes operadoras e formatos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes (multi-tenancy) |
| NomeTemplate | NVARCHAR(200) | NÃO | - | Nome descritivo do template |
| OperadoraId | UNIQUEIDENTIFIER | NÃO | - | FK para Operadoras |
| Formato | NVARCHAR(50) | NÃO | - | Enum: CSV, XLS, XLSX, TXT, PDF |
| Encoding | NVARCHAR(50) | NÃO | 'UTF-8' | Encoding do arquivo (UTF-8, ISO-8859-1) |
| Delimitador | NVARCHAR(10) | SIM | NULL | Delimitador (CSV/TXT) |
| LinhaInicioDados | INT | NÃO | 1 | Linha onde começam os dados |
| MapeamentoColunasJson | NVARCHAR(MAX) | NÃO | - | JSON: {"campo_sistema": "coluna_arquivo"} |
| RegrasTransformacaoJson | NVARCHAR(MAX) | SIM | NULL | JSON: regras de transformação |
| RegrasValidacaoJson | NVARCHAR(MAX) | SIM | NULL | JSON: validações customizadas |
| Ativo | BIT | NÃO | 1 | Template ativo |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Importacao_Template_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Importacao_Template_OperadoraId | OperadoraId | NONCLUSTERED | Filtro por operadora |
| IX_Faturas_Importacao_Template_Ativo | Ativo | FILTERED WHERE FlExcluido = 0 | Templates ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Importacao_Template | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Importacao_Template_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_Importacao_Template_OperadoraId | FOREIGN KEY | OperadoraId REFERENCES Operadoras(Id) | Operadora |
| UQ_Faturas_Importacao_Template_Nome | UNIQUE | (ClienteId, NomeTemplate) | Nome único por cliente |

---

### 2.4 Tabela: Faturas_Importacao_Log

**Descrição:** Histórico de tentativas de importação de faturas com estatísticas de sucesso/erro.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | SIM | NULL | FK para Faturas (se sucesso) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| ArquivoNome | NVARCHAR(500) | NÃO | - | Nome arquivo original |
| ArquivoTamanhoBytes | BIGINT | NÃO | 0 | Tamanho arquivo |
| TemplateUsadoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Template usado |
| LinhasTotal | INT | NÃO | 0 | Total linhas processadas |
| LinhasSucesso | INT | NÃO | 0 | Linhas importadas com sucesso |
| LinhasErro | INT | NÃO | 0 | Linhas com erro |
| ErrosJson | NVARCHAR(MAX) | SIM | NULL | JSON detalhado dos erros |
| TempoProcessamentoMs | INT | NÃO | 0 | Tempo processamento (milissegundos) |
| Sucesso | BIT | NÃO | 0 | Flag de sucesso |
| DataImportacao | DATETIME2 | NÃO | GETDATE() | Data/hora importação |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuarios |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Importacao_Log_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Importacao_Log_FaturaId | FaturaId | NONCLUSTERED | Relacionamento fatura |
| IX_Faturas_Importacao_Log_DataImportacao | DataImportacao DESC | NONCLUSTERED | Ordenação temporal |
| IX_Faturas_Importacao_Log_Sucesso | Sucesso | NONCLUSTERED | Filtro por sucesso |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Importacao_Log | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Importacao_Log_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_Importacao_Log_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Fatura gerada |
| FK_Faturas_Importacao_Log_UsuarioId | FOREIGN KEY | UsuarioId REFERENCES Usuarios(Id) | Usuário responsável |

---

### 2.5 Tabela: Faturas_Auditoria_Regra

**Descrição:** Biblioteca de regras configuráveis para auditoria automática de faturas.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| NomeRegra | NVARCHAR(200) | NÃO | - | Nome da regra |
| Descricao | NVARCHAR(1000) | NÃO | - | Descrição detalhada |
| Severidade | NVARCHAR(50) | NÃO | 'Media' | Enum: Baixa, Media, Alta, Critica |
| TipoRegra | NVARCHAR(50) | NÃO | - | Enum: SQL, Json, Custom |
| CondicaoSql | NVARCHAR(MAX) | SIM | NULL | SQL para regras baseadas em query |
| CondicaoJsonPath | NVARCHAR(500) | SIM | NULL | JsonPath para regras JSON |
| ParametrosJson | NVARCHAR(MAX) | SIM | NULL | Parâmetros configuráveis |
| MensagemAlerta | NVARCHAR(1000) | NÃO | - | Mensagem exibida ao falhar |
| Ativa | BIT | NÃO | 1 | Regra ativa |
| Ordem | INT | NÃO | 100 | Ordem de execução |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Auditoria_Regra_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Auditoria_Regra_Ativa | Ativa, Ordem | NONCLUSTERED | Regras ativas ordenadas |
| IX_Faturas_Auditoria_Regra_Severidade | Severidade | NONCLUSTERED | Filtro por severidade |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Auditoria_Regra | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Auditoria_Regra_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| UQ_Faturas_Auditoria_Regra_Nome | UNIQUE | (ClienteId, NomeRegra) | Nome único por cliente |
| CHK_Faturas_Auditoria_Regra_Severidade | CHECK | Severidade IN ('Baixa', 'Media', 'Alta', 'Critica') | Valores válidos |

---

### 2.6 Tabela: Faturas_Auditoria_Resultado

**Descrição:** Log de execução de regras de auditoria por fatura com resultados e valores suspeitos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| RegraId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas_Auditoria_Regra |
| Passou | BIT | NÃO | 0 | Flag indicando se passou na auditoria |
| ValorSuspeito | DECIMAL(18,2) | SIM | NULL | Valor identificado como suspeito |
| MensagemDetalhada | NVARCHAR(MAX) | NÃO | - | Detalhes do resultado |
| ItensAfetadosJson | NVARCHAR(MAX) | SIM | NULL | JSON com IDs dos itens afetados |
| DataExecucao | DATETIME2 | NÃO | GETDATE() | Data/hora execução |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Auditoria_Resultado_FaturaId | FaturaId | NONCLUSTERED | Joins com Faturas |
| IX_Faturas_Auditoria_Resultado_RegraId | RegraId | NONCLUSTERED | Análise por regra |
| IX_Faturas_Auditoria_Resultado_Passou | Passou | NONCLUSTERED | Filtro falhas |
| IX_Faturas_Auditoria_Resultado_DataExecucao | DataExecucao DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Auditoria_Resultado | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Auditoria_Resultado_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) ON DELETE CASCADE | Resultado pertence a fatura |
| FK_Faturas_Auditoria_Resultado_RegraId | FOREIGN KEY | RegraId REFERENCES Faturas_Auditoria_Regra(Id) | Regra aplicada |

---

### 2.7 Tabela: Faturas_Contestacao

**Descrição:** Gerenciamento de contestações de cobranças indevidas com workflow completo.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| NumeroProtocolo | NVARCHAR(100) | SIM | NULL | Protocolo operadora |
| ItensContestadosJson | NVARCHAR(MAX) | NÃO | - | JSON com IDs itens contestados |
| ValorTotalContestado | DECIMAL(18,2) | NÃO | 0 | Valor total contestado |
| StatusWorkflow | NVARCHAR(50) | NÃO | 'Criada' | Enum: Criada, Aguardando_Aprovacao, Aprovada, Enviada, Em_Analise, Aceita, Recusada, Cancelada |
| TipoContestacao | NVARCHAR(100) | NÃO | - | Tipo (Cobrança indevida, Valor incorreto, etc.) |
| MotivoDetalhado | NVARCHAR(MAX) | NÃO | - | Motivo detalhado |
| AprovadorInternoId | UNIQUEIDENTIFIER | SIM | NULL | FK para Usuarios (aprovador) |
| DataAprovacao | DATETIME2 | SIM | NULL | Data aprovação interna |
| DataEnvioOperadora | DATETIME2 | SIM | NULL | Data envio operadora |
| PrazoRespostaDias | INT | NÃO | 15 | Prazo resposta (dias úteis) |
| DataLimiteResposta | DATE | SIM | NULL | Data limite resposta |
| RespostaOperadora | NVARCHAR(MAX) | SIM | NULL | Resposta operadora |
| DataRespostaOperadora | DATETIME2 | SIM | NULL | Data resposta operadora |
| CreditoRecebido | BIT | SIM | NULL | Flag crédito recebido |
| ValorCreditado | DECIMAL(18,2) | SIM | NULL | Valor creditado |
| DataFechamento | DATETIME2 | SIM | NULL | Data fechamento |
| Ativo | BIT | NÃO | 1 | Soft delete: false=ativo, true=excluído flag |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Contestacao_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Contestacao_FaturaId | FaturaId | NONCLUSTERED | Relacionamento fatura |
| IX_Faturas_Contestacao_StatusWorkflow | StatusWorkflow | NONCLUSTERED | Filtro por status |
| IX_Faturas_Contestacao_DataLimiteResposta | DataLimiteResposta | NONCLUSTERED | SLA monitoring |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Contestacao | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Contestacao_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Fatura contestada |
| FK_Faturas_Contestacao_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_Contestacao_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuarios(Id) | Criador |
| CHK_Faturas_Contestacao_Valor | CHECK | ValorTotalContestado > 0 | Valor positivo |

---

### 2.8 Tabela: Faturas_Contestacao_Historico

**Descrição:** Timeline de mudanças de status das contestações para rastreabilidade.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ContestacaoId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas_Contestacao |
| StatusAnterior | NVARCHAR(50) | SIM | NULL | Status anterior |
| StatusNovo | NVARCHAR(50) | NÃO | - | Status novo |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuarios |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações da mudança |
| DataAlteracao | DATETIME2 | NÃO | GETDATE() | Data/hora alteração |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Contestacao_Historico_ContestacaoId | ContestacaoId | NONCLUSTERED | Timeline da contestação |
| IX_Faturas_Contestacao_Historico_DataAlteracao | DataAlteracao DESC | NONCLUSTERED | Ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Contestacao_Historico | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Contestacao_Historico_ContestacaoId | FOREIGN KEY | ContestacaoId REFERENCES Faturas_Contestacao(Id) ON DELETE CASCADE | Histórico pertence a contestação |
| FK_Faturas_Contestacao_Historico_UsuarioId | FOREIGN KEY | UsuarioId REFERENCES Usuarios(Id) | Responsável mudança |

---

### 2.9 Tabela: Faturas_Rateio_Regra

**Descrição:** Regras configuráveis para rateio automático de custos de faturas.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| NomeRegra | NVARCHAR(200) | NÃO | - | Nome descritivo |
| TipoRateio | NVARCHAR(50) | NÃO | - | Enum: Fixo, Proporcional, Misto, Por_Ativo, Hierarquico |
| DimensoesJson | NVARCHAR(MAX) | NÃO | - | JSON: dimensões rateio (CC, Projeto, Depto) |
| PercentuaisJson | NVARCHAR(MAX) | NÃO | - | JSON: percentuais por dimensão |
| CondicaoAplicacaoJson | NVARCHAR(MAX) | SIM | NULL | JSON: condições para aplicar regra |
| Ativa | BIT | NÃO | 1 | Regra ativa |
| Padrao | BIT | NÃO | 0 | Regra padrão |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário que atualizou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Rateio_Regra_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Rateio_Regra_Ativa | Ativa | FILTERED WHERE Ativa = 1 | Regras ativas |
| IX_Faturas_Rateio_Regra_Padrao | Padrao | FILTERED WHERE Padrao = 1 | Regra padrão |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Rateio_Regra | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Rateio_Regra_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| UQ_Faturas_Rateio_Regra_Nome | UNIQUE | (ClienteId, NomeRegra) | Nome único por cliente |

---

### 2.10 Tabela: Faturas_Rateio_Item

**Descrição:** Itens de rateio calculados para cada fatura.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| RegraRateioId | UNIQUEIDENTIFIER | SIM | NULL | FK para Faturas_Rateio_Regra (se usado) |
| DimensaoTipo | NVARCHAR(50) | NÃO | - | Enum: Centro_Custo, Projeto, Departamento, Geolocalizacao, Tipo_Servico |
| DimensaoId | UNIQUEIDENTIFIER | NÃO | - | ID da dimensão específica |
| Percentual | DECIMAL(5,2) | NÃO | 0 | Percentual do rateio (0-100) |
| Valor | DECIMAL(18,2) | NÃO | 0 | Valor rateado |
| ContaContabil | NVARCHAR(50) | SIM | NULL | Código conta contábil (ERP) |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Rateio_Item_FaturaId | FaturaId | NONCLUSTERED | Rateio da fatura |
| IX_Faturas_Rateio_Item_DimensaoTipo | DimensaoTipo, DimensaoId | NONCLUSTERED | Análise por dimensão |
| IX_Faturas_Rateio_Item_RegraRateioId | RegraRateioId | NONCLUSTERED | Análise por regra |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Rateio_Item | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Rateio_Item_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) ON DELETE CASCADE | Rateio pertence a fatura |
| FK_Faturas_Rateio_Item_RegraRateioId | FOREIGN KEY | RegraRateioId REFERENCES Faturas_Rateio_Regra(Id) | Regra aplicada |
| CHK_Faturas_Rateio_Item_Percentual | CHECK | Percentual >= 0 AND Percentual <= 100 | Percentual válido |
| CHK_Faturas_Rateio_Item_Valor | CHECK | Valor >= 0 | Valor não negativo |

---

### 2.11 Tabela: Faturas_Anexos

**Descrição:** Armazena referências a arquivos anexados (PDFs, evidências, documentos) no Azure Blob Storage.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| TipoDocumento | NVARCHAR(100) | NÃO | - | Enum: PDF_Original, Evidencia_Contestacao, Contrato, Outro |
| NomeArquivo | NVARCHAR(500) | NÃO | - | Nome original arquivo |
| AzureBlobUrl | NVARCHAR(1000) | NÃO | - | URL Azure Blob Storage |
| AzureBlobContainer | NVARCHAR(100) | NÃO | 'faturas' | Container Azure |
| Sha256Hash | NVARCHAR(64) | NÃO | - | Hash SHA-256 (integridade) |
| TamanhoBytes | BIGINT | NÃO | 0 | Tamanho arquivo |
| MimeType | NVARCHAR(100) | NÃO | 'application/pdf' | MIME type |
| DataUpload | DATETIME2 | NÃO | GETDATE() | Data upload |
| UsuarioId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuarios |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Anexos_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Anexos_FaturaId | FaturaId | NONCLUSTERED | Anexos da fatura |
| IX_Faturas_Anexos_TipoDocumento | TipoDocumento | NONCLUSTERED | Filtro por tipo |
| IX_Faturas_Anexos_Sha256Hash | Sha256Hash | NONCLUSTERED | Detecção duplicados |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Anexos | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Anexos_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Anexo pertence a fatura |
| FK_Faturas_Anexos_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_Anexos_UsuarioId | FOREIGN KEY | UsuarioId REFERENCES Usuarios(Id) | Responsável upload |
| CHK_Faturas_Anexos_TamanhoBytes | CHECK | TamanhoBytes > 0 | Tamanho válido |

---

### 2.12 Tabela: Faturas_Aprovacao

**Descrição:** Workflow de aprovação multi-nível de faturas.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FaturaId | UNIQUEIDENTIFIER | NÃO | - | FK para Faturas |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| NivelAprovacao | INT | NÃO | 1 | Nível aprovação (1=Coordenador, 2=Gerente, 3=Diretor) |
| AprovadorId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuarios (aprovador) |
| Status | NVARCHAR(50) | NÃO | 'Pendente' | Enum: Pendente, Aprovado, Rejeitado, Delegado |
| DataDecisao | DATETIME2 | SIM | NULL | Data decisão |
| JustificativaRejeicao | NVARCHAR(MAX) | SIM | NULL | Justificativa (obrigatória se rejeitado) |
| ObservacoesAprovacao | NVARCHAR(MAX) | SIM | NULL | Observações aprovador |
| DocusignEnvelopeId | NVARCHAR(100) | SIM | NULL | ID envelope DocuSign |
| DataAssinatura | DATETIME2 | SIM | NULL | Data assinatura digital |
| PrazoAprovacaoHoras | INT | NÃO | 48 | Prazo aprovação (horas) |
| DataLimiteAprovacao | DATETIME2 | NÃO | - | Data limite aprovação |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Aprovacao_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Aprovacao_FaturaId | FaturaId | NONCLUSTERED | Aprovações da fatura |
| IX_Faturas_Aprovacao_AprovadorId | AprovadorId, Status | NONCLUSTERED | Fila aprovações usuário |
| IX_Faturas_Aprovacao_Status | Status | NONCLUSTERED | Filtro por status |
| IX_Faturas_Aprovacao_DataLimite | DataLimiteAprovacao | NONCLUSTERED | SLA monitoring |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Aprovacao | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Aprovacao_FaturaId | FOREIGN KEY | FaturaId REFERENCES Faturas(Id) | Aprovação pertence a fatura |
| FK_Faturas_Aprovacao_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |
| FK_Faturas_Aprovacao_AprovadorId | FOREIGN KEY | AprovadorId REFERENCES Usuarios(Id) | Aprovador |
| CHK_Faturas_Aprovacao_NivelAprovacao | CHECK | NivelAprovacao BETWEEN 1 AND 3 | Nível válido |

---

### 2.13 Tabela: Faturas_Kpi_Snapshot

**Descrição:** Snapshots diários de KPIs para dashboard histórico e tendências.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| DataSnapshot | DATE | NÃO | - | Data do snapshot |
| GastoTotal | DECIMAL(18,2) | NÃO | 0 | Gasto total do mês |
| TaxaConciliacao | DECIMAL(5,2) | NÃO | 0 | % itens conciliados automaticamente |
| TaxaAuditoria | DECIMAL(5,2) | NÃO | 0 | % faturas sem alertas críticos |
| ValorContestado | DECIMAL(18,2) | NÃO | 0 | Valor total contestado no período |
| ValorRecuperado | DECIMAL(18,2) | NÃO | 0 | Valor recuperado em contestações |
| NumeroFaturas | INT | NÃO | 0 | Total faturas no período |
| NumeroContestacoes | INT | NÃO | 0 | Total contestações ativas |
| CreatedAt | DATETIME2 | NÃO | GETDATE() | Data de criação |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Kpi_Snapshot_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Kpi_Snapshot_DataSnapshot | DataSnapshot DESC | NONCLUSTERED | Série temporal |
| UQ_Faturas_Kpi_Snapshot_Cliente_Data | (ClienteId, DataSnapshot) | UNIQUE | Snapshot único por dia |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Kpi_Snapshot | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Kpi_Snapshot_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |

---

### 2.14 Tabela: Faturas_Previsao_Ml

**Descrição:** Armazena previsões do modelo Machine Learning para alerta preditivo de estouro de budget.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para Clientes |
| MesReferencia | DATE | NÃO | - | Mês previsto (primeiro dia) |
| ValorPrevisto | DECIMAL(18,2) | NÃO | 0 | Valor previsto pelo modelo |
| ConfidenceInterval | DECIMAL(5,2) | NÃO | 0 | Intervalo confiança (0-100%) |
| AlertasGeradosJson | NVARCHAR(MAX) | SIM | NULL | JSON: alertas e recomendações |
| ModeloVersao | NVARCHAR(50) | NÃO | - | Versão modelo ML usado |
| FeaturesUsadasJson | NVARCHAR(MAX) | SIM | NULL | JSON: features usadas na previsão |
| DataPrevisao | DATETIME2 | NÃO | GETDATE() | Data/hora execução previsão |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| IX_Faturas_Previsao_Ml_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Faturas_Previsao_Ml_MesReferencia | MesReferencia DESC | NONCLUSTERED | Previsões futuras |
| IX_Faturas_Previsao_Ml_DataPrevisao | DataPrevisao DESC | NONCLUSTERED | Histórico execuções |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Faturas_Previsao_Ml | PRIMARY KEY | Id | Chave primária |
| FK_Faturas_Previsao_Ml_ClienteId | FOREIGN KEY | ClienteId REFERENCES Clientes(Id) | Multi-tenancy |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Clientes | 1:N | Faturas | Cliente possui muitas faturas |
| Empresas | 1:N | Faturas | Empresa responsável por faturas |
| Operadoras | 1:N | Faturas | Operadora emite faturas |
| Faturas | 1:N | Faturas_Detalhe | Fatura possui itens detalhados |
| Faturas | 1:N | Faturas_Anexos | Fatura possui anexos |
| Faturas | 1:N | Faturas_Contestacao | Fatura pode ter contestações |
| Faturas | 1:N | Faturas_Rateio_Item | Fatura possui rateio |
| Faturas | 1:N | Faturas_Aprovacao | Fatura possui aprovações multi-nível |
| Faturas | 1:N | Faturas_Auditoria_Resultado | Fatura possui resultados auditoria |
| Faturas | 1:N | Faturas_Importacao_Log | Fatura possui log importação |
| Clientes | 1:N | Faturas_Importacao_Template | Cliente possui templates importação |
| Operadoras | 1:N | Faturas_Importacao_Template | Template específico por operadora |
| Clientes | 1:N | Faturas_Auditoria_Regra | Cliente possui regras auditoria |
| Faturas_Auditoria_Regra | 1:N | Faturas_Auditoria_Resultado | Regra gera resultados |
| Faturas_Contestacao | 1:N | Faturas_Contestacao_Historico | Contestação possui timeline |
| Clientes | 1:N | Faturas_Rateio_Regra | Cliente possui regras rateio |
| Faturas_Rateio_Regra | 1:N | Faturas_Rateio_Item | Regra aplicada em itens |
| Usuarios | 1:N | Faturas | Usuário cria/modifica faturas |
| Usuarios | 1:N | Faturas_Aprovacao | Usuário aprova faturas |
| Usuarios | 1:N | Faturas_Contestacao | Usuário cria contestações |
| Usuarios | 1:N | Faturas_Importacao_Log | Usuário importa faturas |
| Usuarios | 1:N | Faturas_Anexos | Usuário faz upload anexos |

---

## 4. DDL - SQL Server / SQLite

```sql
-- =============================================
-- RF026 - Gestão Completa de Faturas de Telecom e TI
-- Modelo de Dados
-- Data: 18/12/2025
-- =============================================

-- ---------------------------------------------
-- Tabela: Faturas
-- ---------------------------------------------
CREATE TABLE Faturas (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    EmpresaId UNIQUEIDENTIFIER NOT NULL,
    OperadoraId UNIQUEIDENTIFIER NOT NULL,
    NumeroFatura NVARCHAR(100) NOT NULL,
    DataEmissao DATETIME2 NOT NULL,
    DataVencimento DATETIME2 NOT NULL,
    PeriodoReferencia NVARCHAR(7) NOT NULL, -- YYYY-MM
    ValorTotalBruto DECIMAL(18,2) NOT NULL DEFAULT 0,
    Descontos DECIMAL(18,2) NOT NULL DEFAULT 0,
    Acrescimos DECIMAL(18,2) NOT NULL DEFAULT 0,
    ValorTotalLiquido DECIMAL(18,2) NOT NULL DEFAULT 0,
    Icms DECIMAL(18,2) NOT NULL DEFAULT 0,
    Pis DECIMAL(18,2) NOT NULL DEFAULT 0,
    Cofins DECIMAL(18,2) NOT NULL DEFAULT 0,
    Iss DECIMAL(18,2) NOT NULL DEFAULT 0,
    Status NVARCHAR(50) NOT NULL DEFAULT 'Rascunho', -- Rascunho, Conciliacao, Auditoria, Aprovacao, Aprovada, Paga, Contestada, Cancelada
    NumeroVersao INT NOT NULL DEFAULT 1,
    VersaoAtualFlag BIT NOT NULL DEFAULT 1,
    MotivoAlteracaoVersao NVARCHAR(500),
    OcrConfidence DECIMAL(5,2),
    OcrRawJson NVARCHAR(MAX),
    ErpSincronizado BIT NOT NULL DEFAULT 0,
    ErpDocumentoNumero NVARCHAR(50),
    ErpDataSincronizacao DATETIME2,
    ArquivoOriginalUrl NVARCHAR(500),
    Observacoes NVARCHAR(MAX),
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_EmpresaId
        FOREIGN KEY (EmpresaId) REFERENCES Empresas(Id),
    CONSTRAINT FK_Faturas_OperadoraId
        FOREIGN KEY (OperadoraId) REFERENCES Operadoras(Id),
    CONSTRAINT FK_Faturas_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuarios(Id),
    CONSTRAINT FK_Faturas_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuarios(Id),

    -- Unique Constraints
    CONSTRAINT UQ_Faturas_Numero
        UNIQUE (ClienteId, OperadoraId, NumeroFatura, NumeroVersao),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Status
        CHECK (Status IN ('Rascunho', 'Conciliacao', 'Auditoria', 'Aprovacao', 'Aprovada', 'Paga', 'Contestada', 'Cancelada')),
    CONSTRAINT CHK_Faturas_ValorLiquido
        CHECK (ValorTotalLiquido >= 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_ClienteId
    ON Faturas(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_EmpresaId
    ON Faturas(EmpresaId);
CREATE NONCLUSTERED INDEX IX_Faturas_OperadoraId
    ON Faturas(OperadoraId);
CREATE NONCLUSTERED INDEX IX_Faturas_Status
    ON Faturas(Status);
CREATE NONCLUSTERED INDEX IX_Faturas_DataEmissao
    ON Faturas(DataEmissao DESC);
CREATE NONCLUSTERED INDEX IX_Faturas_PeriodoReferencia
    ON Faturas(PeriodoReferencia);
CREATE NONCLUSTERED INDEX IX_Faturas_NumeroVersao
    ON Faturas(NumeroFatura, NumeroVersao);
CREATE NONCLUSTERED INDEX IX_Faturas_VersaoAtual
    ON Faturas(VersaoAtualFlag, ClienteId)
    WHERE VersaoAtualFlag = 1;


-- ---------------------------------------------
-- Tabela: Faturas_Detalhe
-- ---------------------------------------------
CREATE TABLE Faturas_Detalhe (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    NumeroLinha NVARCHAR(100) NOT NULL,
    DescricaoServico NVARCHAR(500) NOT NULL,
    ConsumoQuantidade DECIMAL(18,4),
    UnidadeMedida NVARCHAR(50),
    ValorUnitario DECIMAL(18,4),
    ValorTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
    Conciliado BIT NOT NULL DEFAULT 0,
    ContratoItemId UNIQUEIDENTIFIER,
    AtivoId UNIQUEIDENTIFIER,
    MatchScore DECIMAL(5,2),
    AuditoriaStatus NVARCHAR(50), -- Aprovado, Alerta, Critico
    AuditoriaRegrasFalhas NVARCHAR(MAX),
    RateioCentroCustoId UNIQUEIDENTIFIER,
    RateioProjetoId UNIQUEIDENTIFIER,
    RateioDepartamentoId UNIQUEIDENTIFIER,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Detalhe_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Faturas_Detalhe_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuarios(Id),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Detalhe_ValorTotal
        CHECK (ValorTotal >= 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Detalhe_FaturaId
    ON Faturas_Detalhe(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Detalhe_NumeroLinha
    ON Faturas_Detalhe(NumeroLinha);
CREATE NONCLUSTERED INDEX IX_Faturas_Detalhe_Conciliado
    ON Faturas_Detalhe(Conciliado);
CREATE NONCLUSTERED INDEX IX_Faturas_Detalhe_AuditoriaStatus
    ON Faturas_Detalhe(AuditoriaStatus);
CREATE NONCLUSTERED INDEX IX_Faturas_Detalhe_ContratoItemId
    ON Faturas_Detalhe(ContratoItemId);


-- ---------------------------------------------
-- Tabela: Faturas_Importacao_Template
-- ---------------------------------------------
CREATE TABLE Faturas_Importacao_Template (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NomeTemplate NVARCHAR(200) NOT NULL,
    OperadoraId UNIQUEIDENTIFIER NOT NULL,
    Formato NVARCHAR(50) NOT NULL, -- CSV, XLS, XLSX, TXT, PDF
    Encoding NVARCHAR(50) NOT NULL DEFAULT 'UTF-8',
    Delimitador NVARCHAR(10),
    LinhaInicioDados INT NOT NULL DEFAULT 1,
    MapeamentoColunasJson NVARCHAR(MAX) NOT NULL,
    RegrasTransformacaoJson NVARCHAR(MAX),
    RegrasValidacaoJson NVARCHAR(MAX),
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Importacao_Template_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_Importacao_Template_OperadoraId
        FOREIGN KEY (OperadoraId) REFERENCES Operadoras(Id),

    -- Unique Constraints
    CONSTRAINT UQ_Faturas_Importacao_Template_Nome
        UNIQUE (ClienteId, NomeTemplate)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Template_ClienteId
    ON Faturas_Importacao_Template(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Template_OperadoraId
    ON Faturas_Importacao_Template(OperadoraId);
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Template_Ativo
    ON Faturas_Importacao_Template(Ativo)
    WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: Faturas_Importacao_Log
-- ---------------------------------------------
CREATE TABLE Faturas_Importacao_Log (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    ArquivoNome NVARCHAR(500) NOT NULL,
    ArquivoTamanhoBytes BIGINT NOT NULL DEFAULT 0,
    TemplateUsadoId UNIQUEIDENTIFIER,
    LinhasTotal INT NOT NULL DEFAULT 0,
    LinhasSucesso INT NOT NULL DEFAULT 0,
    LinhasErro INT NOT NULL DEFAULT 0,
    ErrosJson NVARCHAR(MAX),
    TempoProcessamentoMs INT NOT NULL DEFAULT 0,
    Sucesso BIT NOT NULL DEFAULT 0,
    DataImportacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Importacao_Log_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_Importacao_Log_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id),
    CONSTRAINT FK_Faturas_Importacao_Log_TemplateUsadoId
        FOREIGN KEY (TemplateUsadoId) REFERENCES Faturas_Importacao_Template(Id),
    CONSTRAINT FK_Faturas_Importacao_Log_UsuarioId
        FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Log_ClienteId
    ON Faturas_Importacao_Log(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Log_FaturaId
    ON Faturas_Importacao_Log(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Log_DataImportacao
    ON Faturas_Importacao_Log(DataImportacao DESC);
CREATE NONCLUSTERED INDEX IX_Faturas_Importacao_Log_Sucesso
    ON Faturas_Importacao_Log(Sucesso);


-- ---------------------------------------------
-- Tabela: Faturas_Auditoria_Regra
-- ---------------------------------------------
CREATE TABLE Faturas_Auditoria_Regra (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NomeRegra NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(1000) NOT NULL,
    Severidade NVARCHAR(50) NOT NULL DEFAULT 'Media', -- Baixa, Media, Alta, Critica
    TipoRegra NVARCHAR(50) NOT NULL, -- SQL, Json, Custom
    CondicaoSql NVARCHAR(MAX),
    CondicaoJsonPath NVARCHAR(500),
    ParametrosJson NVARCHAR(MAX),
    MensagemAlerta NVARCHAR(1000) NOT NULL,
    Ativa BIT NOT NULL DEFAULT 1,
    Ordem INT NOT NULL DEFAULT 100,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Auditoria_Regra_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),

    -- Unique Constraints
    CONSTRAINT UQ_Faturas_Auditoria_Regra_Nome
        UNIQUE (ClienteId, NomeRegra),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Auditoria_Regra_Severidade
        CHECK (Severidade IN ('Baixa', 'Media', 'Alta', 'Critica'))
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Regra_ClienteId
    ON Faturas_Auditoria_Regra(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Regra_Ativa
    ON Faturas_Auditoria_Regra(Ativa, Ordem);
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Regra_Severidade
    ON Faturas_Auditoria_Regra(Severidade);


-- ---------------------------------------------
-- Tabela: Faturas_Auditoria_Resultado
-- ---------------------------------------------
CREATE TABLE Faturas_Auditoria_Resultado (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    RegraId UNIQUEIDENTIFIER NOT NULL,
    Passou BIT NOT NULL DEFAULT 0,
    ValorSuspeito DECIMAL(18,2),
    MensagemDetalhada NVARCHAR(MAX) NOT NULL,
    ItensAfetadosJson NVARCHAR(MAX),
    DataExecucao DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Auditoria_Resultado_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Faturas_Auditoria_Resultado_RegraId
        FOREIGN KEY (RegraId) REFERENCES Faturas_Auditoria_Regra(Id)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Resultado_FaturaId
    ON Faturas_Auditoria_Resultado(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Resultado_RegraId
    ON Faturas_Auditoria_Resultado(RegraId);
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Resultado_Passou
    ON Faturas_Auditoria_Resultado(Passou);
CREATE NONCLUSTERED INDEX IX_Faturas_Auditoria_Resultado_DataExecucao
    ON Faturas_Auditoria_Resultado(DataExecucao DESC);


-- ---------------------------------------------
-- Tabela: Faturas_Contestacao
-- ---------------------------------------------
CREATE TABLE Faturas_Contestacao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NumeroProtocolo NVARCHAR(100),
    ItensContestadosJson NVARCHAR(MAX) NOT NULL,
    ValorTotalContestado DECIMAL(18,2) NOT NULL DEFAULT 0,
    StatusWorkflow NVARCHAR(50) NOT NULL DEFAULT 'Criada', -- Criada, Aguardando_Aprovacao, Aprovada, Enviada, Em_Analise, Aceita, Recusada, Cancelada
    TipoContestacao NVARCHAR(100) NOT NULL,
    MotivoDetalhado NVARCHAR(MAX) NOT NULL,
    AprovadorInternoId UNIQUEIDENTIFIER,
    DataAprovacao DATETIME2,
    DataEnvioOperadora DATETIME2,
    PrazoRespostaDias INT NOT NULL DEFAULT 15,
    DataLimiteResposta DATE,
    RespostaOperadora NVARCHAR(MAX),
    DataRespostaOperadora DATETIME2,
    CreditoRecebido BIT,
    ValorCreditado DECIMAL(18,2),
    DataFechamento DATETIME2,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Contestacao_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id),
    CONSTRAINT FK_Faturas_Contestacao_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_Contestacao_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuarios(Id),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Contestacao_Valor
        CHECK (ValorTotalContestado > 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_ClienteId
    ON Faturas_Contestacao(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_FaturaId
    ON Faturas_Contestacao(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_StatusWorkflow
    ON Faturas_Contestacao(StatusWorkflow);
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_DataLimiteResposta
    ON Faturas_Contestacao(DataLimiteResposta);


-- ---------------------------------------------
-- Tabela: Faturas_Contestacao_Historico
-- ---------------------------------------------
CREATE TABLE Faturas_Contestacao_Historico (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ContestacaoId UNIQUEIDENTIFIER NOT NULL,
    StatusAnterior NVARCHAR(50),
    StatusNovo NVARCHAR(50) NOT NULL,
    UsuarioId UNIQUEIDENTIFIER NOT NULL,
    Observacoes NVARCHAR(MAX),
    DataAlteracao DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Contestacao_Historico_ContestacaoId
        FOREIGN KEY (ContestacaoId) REFERENCES Faturas_Contestacao(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Faturas_Contestacao_Historico_UsuarioId
        FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_Historico_ContestacaoId
    ON Faturas_Contestacao_Historico(ContestacaoId);
CREATE NONCLUSTERED INDEX IX_Faturas_Contestacao_Historico_DataAlteracao
    ON Faturas_Contestacao_Historico(DataAlteracao DESC);


-- ---------------------------------------------
-- Tabela: Faturas_Rateio_Regra
-- ---------------------------------------------
CREATE TABLE Faturas_Rateio_Regra (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NomeRegra NVARCHAR(200) NOT NULL,
    TipoRateio NVARCHAR(50) NOT NULL, -- Fixo, Proporcional, Misto, Por_Ativo, Hierarquico
    DimensoesJson NVARCHAR(MAX) NOT NULL,
    PercentuaisJson NVARCHAR(MAX) NOT NULL,
    CondicaoAplicacaoJson NVARCHAR(MAX),
    Ativa BIT NOT NULL DEFAULT 1,
    Padrao BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2,
    ModifiedBy UNIQUEIDENTIFIER,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Rateio_Regra_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),

    -- Unique Constraints
    CONSTRAINT UQ_Faturas_Rateio_Regra_Nome
        UNIQUE (ClienteId, NomeRegra)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Regra_ClienteId
    ON Faturas_Rateio_Regra(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Regra_Ativa
    ON Faturas_Rateio_Regra(Ativa)
    WHERE Ativa = 1;
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Regra_Padrao
    ON Faturas_Rateio_Regra(Padrao)
    WHERE Padrao = 1;


-- ---------------------------------------------
-- Tabela: Faturas_Rateio_Item
-- ---------------------------------------------
CREATE TABLE Faturas_Rateio_Item (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    RegraRateioId UNIQUEIDENTIFIER,
    DimensaoTipo NVARCHAR(50) NOT NULL, -- Centro_Custo, Projeto, Departamento, Geolocalizacao, Tipo_Servico
    DimensaoId UNIQUEIDENTIFIER NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL DEFAULT 0,
    Valor DECIMAL(18,2) NOT NULL DEFAULT 0,
    ContaContabil NVARCHAR(50),
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Rateio_Item_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id) ON DELETE CASCADE,
    CONSTRAINT FK_Faturas_Rateio_Item_RegraRateioId
        FOREIGN KEY (RegraRateioId) REFERENCES Faturas_Rateio_Regra(Id),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Rateio_Item_Percentual
        CHECK (Percentual >= 0 AND Percentual <= 100),
    CONSTRAINT CHK_Faturas_Rateio_Item_Valor
        CHECK (Valor >= 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Item_FaturaId
    ON Faturas_Rateio_Item(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Item_DimensaoTipo
    ON Faturas_Rateio_Item(DimensaoTipo, DimensaoId);
CREATE NONCLUSTERED INDEX IX_Faturas_Rateio_Item_RegraRateioId
    ON Faturas_Rateio_Item(RegraRateioId);


-- ---------------------------------------------
-- Tabela: Faturas_Anexos
-- ---------------------------------------------
CREATE TABLE Faturas_Anexos (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoDocumento NVARCHAR(100) NOT NULL, -- PDF_Original, Evidencia_Contestacao, Contrato, Outro
    NomeArquivo NVARCHAR(500) NOT NULL,
    AzureBlobUrl NVARCHAR(1000) NOT NULL,
    AzureBlobContainer NVARCHAR(100) NOT NULL DEFAULT 'faturas',
    Sha256Hash NVARCHAR(64) NOT NULL,
    TamanhoBytes BIGINT NOT NULL DEFAULT 0,
    MimeType NVARCHAR(100) NOT NULL DEFAULT 'application/pdf',
    DataUpload DATETIME2 NOT NULL DEFAULT GETDATE(),
    UsuarioId UNIQUEIDENTIFIER NOT NULL,

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Anexos_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id),
    CONSTRAINT FK_Faturas_Anexos_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_Anexos_UsuarioId
        FOREIGN KEY (UsuarioId) REFERENCES Usuarios(Id),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Anexos_TamanhoBytes
        CHECK (TamanhoBytes > 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Anexos_ClienteId
    ON Faturas_Anexos(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Anexos_FaturaId
    ON Faturas_Anexos(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Anexos_TipoDocumento
    ON Faturas_Anexos(TipoDocumento);
CREATE NONCLUSTERED INDEX IX_Faturas_Anexos_Sha256Hash
    ON Faturas_Anexos(Sha256Hash);


-- ---------------------------------------------
-- Tabela: Faturas_Aprovacao
-- ---------------------------------------------
CREATE TABLE Faturas_Aprovacao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FaturaId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NivelAprovacao INT NOT NULL DEFAULT 1, -- 1=Coordenador, 2=Gerente, 3=Diretor
    AprovadorId UNIQUEIDENTIFIER NOT NULL,
    Status NVARCHAR(50) NOT NULL DEFAULT 'Pendente', -- Pendente, Aprovado, Rejeitado, Delegado
    DataDecisao DATETIME2,
    JustificativaRejeicao NVARCHAR(MAX),
    ObservacoesAprovacao NVARCHAR(MAX),
    DocusignEnvelopeId NVARCHAR(100),
    DataAssinatura DATETIME2,
    PrazoAprovacaoHoras INT NOT NULL DEFAULT 48,
    DataLimiteAprovacao DATETIME2 NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Aprovacao_FaturaId
        FOREIGN KEY (FaturaId) REFERENCES Faturas(Id),
    CONSTRAINT FK_Faturas_Aprovacao_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id),
    CONSTRAINT FK_Faturas_Aprovacao_AprovadorId
        FOREIGN KEY (AprovadorId) REFERENCES Usuarios(Id),

    -- Check Constraints
    CONSTRAINT CHK_Faturas_Aprovacao_NivelAprovacao
        CHECK (NivelAprovacao BETWEEN 1 AND 3)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Aprovacao_ClienteId
    ON Faturas_Aprovacao(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Aprovacao_FaturaId
    ON Faturas_Aprovacao(FaturaId);
CREATE NONCLUSTERED INDEX IX_Faturas_Aprovacao_AprovadorId
    ON Faturas_Aprovacao(AprovadorId, Status);
CREATE NONCLUSTERED INDEX IX_Faturas_Aprovacao_Status
    ON Faturas_Aprovacao(Status);
CREATE NONCLUSTERED INDEX IX_Faturas_Aprovacao_DataLimite
    ON Faturas_Aprovacao(DataLimiteAprovacao);


-- ---------------------------------------------
-- Tabela: Faturas_Kpi_Snapshot
-- ---------------------------------------------
CREATE TABLE Faturas_Kpi_Snapshot (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    DataSnapshot DATE NOT NULL,
    GastoTotal DECIMAL(18,2) NOT NULL DEFAULT 0,
    TaxaConciliacao DECIMAL(5,2) NOT NULL DEFAULT 0,
    TaxaAuditoria DECIMAL(5,2) NOT NULL DEFAULT 0,
    ValorContestado DECIMAL(18,2) NOT NULL DEFAULT 0,
    ValorRecuperado DECIMAL(18,2) NOT NULL DEFAULT 0,
    NumeroFaturas INT NOT NULL DEFAULT 0,
    NumeroContestacoes INT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Kpi_Snapshot_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Kpi_Snapshot_ClienteId
    ON Faturas_Kpi_Snapshot(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Kpi_Snapshot_DataSnapshot
    ON Faturas_Kpi_Snapshot(DataSnapshot DESC);
CREATE UNIQUE NONCLUSTERED INDEX UQ_Faturas_Kpi_Snapshot_Cliente_Data
    ON Faturas_Kpi_Snapshot(ClienteId, DataSnapshot);


-- ---------------------------------------------
-- Tabela: Faturas_Previsao_Ml
-- ---------------------------------------------
CREATE TABLE Faturas_Previsao_Ml (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    MesReferencia DATE NOT NULL,
    ValorPrevisto DECIMAL(18,2) NOT NULL DEFAULT 0,
    ConfidenceInterval DECIMAL(5,2) NOT NULL DEFAULT 0,
    AlertasGeradosJson NVARCHAR(MAX),
    ModeloVersao NVARCHAR(50) NOT NULL,
    FeaturesUsadasJson NVARCHAR(MAX),
    DataPrevisao DATETIME2 NOT NULL DEFAULT GETDATE(),

    -- Foreign Keys
    CONSTRAINT FK_Faturas_Previsao_Ml_ClienteId
        FOREIGN KEY (ClienteId) REFERENCES Clientes(Id)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_Faturas_Previsao_Ml_ClienteId
    ON Faturas_Previsao_Ml(ClienteId);
CREATE NONCLUSTERED INDEX IX_Faturas_Previsao_Ml_MesReferencia
    ON Faturas_Previsao_Ml(MesReferencia DESC);
CREATE NONCLUSTERED INDEX IX_Faturas_Previsao_Ml_DataPrevisao
    ON Faturas_Previsao_Ml(DataPrevisao DESC);
```

---

## 5. Dados Iniciais (Seed)

```sql
-- Nenhum dado inicial obrigatório
-- Templates, regras e configurações serão criados pelos usuários conforme necessidade
```

---

## 6. Observações

### Decisões de Modelagem

1. **Versionamento de Faturas**: Optou-se por manter histórico de versões na mesma tabela com campos `NumeroVersao` e `VersaoAtualFlag` para facilitar consultas. Alternativa seria tabela `Faturas_Versao` separada.

2. **JSON para Flexibilidade**: Campos JSON usados para dados semi-estruturados (mapeamentos, regras, alertas) que variam muito por cliente/operadora. Facilita evolução sem migrations.

3. **Auditoria Separada**: Tabelas `_Auditoria_Regra` e `_Auditoria_Resultado` separadas para permitir reprocessamento de auditorias sem perder histórico.

4. **Workflow Contestação**: Timeline completa com tabela `_Contestacao_Historico` para rastreabilidade legal (evidências em disputas com operadoras).

5. **KPI Snapshots**: Armazenar snapshots diários permite dashboards históricos rápidos sem recalcular agregações.

6. **Machine Learning**: Tabela `_Previsao_Ml` armazena previsões para auditoria do modelo (comparar previsto vs. real).

### Considerações de Performance

- **Índices Multi-Tenant**: Todos os índices principais incluem `ClienteId` para isolamento
- **Índices Compostos**: Queries comuns otimizadas (ex: Status + Data, Aprovador + Status)
- **Filtered Indexes**: Usados para flags booleanas (VersaoAtual, Ativo) reduzindo tamanho índice
- **Soft Delete**: Flag `Ativo` permite recuperação mas requer `WHERE FlExcluido = 0` em queries (EF Core Query Filter global)

### Integrações

- **Azure Blob Storage**: URLs armazenadas em `Faturas_Anexos` com hash SHA-256 para integridade
- **DocuSign**: `DocusignEnvelopeId` em `Faturas_Aprovacao` para rastreamento assinaturas
- **ERP**: Campos `ErpSincronizado`, `ErpDocumentoNumero` para integração SAP/TOTVS
- **Azure Form Recognizer**: `OcrRawJson` preserva dados brutos OCR para re-treinamento modelo

### Migrações Futuras

- Considerar particionamento de `Faturas` por ano se volume >1M registros
- Índices columnstore para `Faturas_Kpi_Snapshot` se análise histórica >3 anos
- Separar `Faturas_Detalhe` em tabela particionada se >10M linhas

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 18/12/2025 | Architect Agent | Versão inicial completa com 14 tabelas |

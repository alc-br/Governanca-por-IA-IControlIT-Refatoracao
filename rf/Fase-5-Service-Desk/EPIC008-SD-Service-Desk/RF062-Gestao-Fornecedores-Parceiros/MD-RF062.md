# Modelo de Dados - RF062 - Gestão de Fornecedores e Parceiros

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF062 - Gestão de Fornecedores e Parceiros](./RF062.md)
**Banco de Dados:** SQL Server / PostgreSQL

---

## 1. Diagrama de Entidades (ER)

```
┌──────────────────────────────────────────────────────┐
│                  GestaoCliente                        │
│                  (multi-tenancy)                      │
└──────────┬───────────────────────────────────────────┘
           │ 1:N
           │
┌──────────▼──────────────────────────────────────────────────┐
│                    Fornecedor                                │
├──────────────────────────────────────────────────────────────┤
│ Id (PK)                     UUID                             │
│ ClienteId (FK)              UUID                             │
│ CNPJ                        VARCHAR(14)                      │
│ RazaoSocial                 VARCHAR(200)                     │
│ NomeFantasia                VARCHAR(200)                     │
│ CategoriaFornecedor         VARCHAR(50)                      │
│ Endereco, Cidade, Estado, CEP                                │
│ Telefone, Email, Site                                        │
│ DadosBancarios (JSON)       TEXT                             │
│ Homologado                  BIT                              │
│ DataHomologacao             DATETIME2                        │
│ Ativo                       BIT                              │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy                 │
└──────────┬───────────────────────────────────────────────────┘
           │ 1:N
           ├──────────────────────────────────────────┐
           │                                          │
┌──────────▼──────────────────┐   ┌──────────────────▼────────────────┐
│   DocumentoFornecedor       │   │   ContratoFornecedor              │
├─────────────────────────────┤   ├───────────────────────────────────┤
│ Id (PK)          UUID       │   │ Id (PK)              UUID         │
│ FornecedorId (FK) UUID      │   │ FornecedorId (FK)    UUID         │
│ ClienteId (FK)   UUID       │   │ ClienteId (FK)       UUID         │
│ TipoDocumento    VARCHAR(50)│   │ NumeroContrato       VARCHAR(100) │
│ NumeroDocumento  VARCHAR(100│   │ TipoContrato         VARCHAR(50)  │
│ DataEmissao      DATE       │   │ DataInicio           DATE         │
│ DataValidade     DATE       │   │ DataFim              DATE         │
│ CaminhoArquivo   VARCHAR    │   │ ValorMensal          DECIMAL      │
│ Valido (computed) BIT       │   │ ValorTotal           DECIMAL      │
│ Ativo            BIT        │   │ RenovacaoAutomatica  BIT          │
│ CreatedAt, ...              │   │ PrazoRenovacaoMeses  INT          │
└─────────────────────────────┘   │ CaminhoArquivoPDF    VARCHAR      │
                                  │ Ativo                BIT          │
┌─────────────────────────────┐   │ CreatedAt, CreatedBy, ...         │
│   ContatoFornecedor         │   └───────────────────────────────────┘
├─────────────────────────────┤
│ Id (PK)          UUID       │   ┌───────────────────────────────────┐
│ FornecedorId (FK) UUID      │   │   SLAFornecedor                   │
│ ClienteId (FK)   UUID       │   ├───────────────────────────────────┤
│ Nome             VARCHAR(200│   │ Id (PK)              UUID         │
│ Cargo            VARCHAR(100│   │ FornecedorId (FK)    UUID         │
│ Departamento     VARCHAR(50)│   │ ClienteId (FK)       UUID         │
│ Telefone         VARCHAR(20)│   │ TipoServico          VARCHAR(50)  │
│ Email            VARCHAR(200│   │ TempoRespostaHoras   INT          │
│ Primario         BIT        │   │ TempoResolucaoDias   INT          │
│ Ativo            BIT        │   │ PercentualCumprimento DECIMAL     │
│ CreatedAt, ...              │   │ MetaAtual            DECIMAL      │
└─────────────────────────────┘   │ Ativo                BIT          │
                                  │ CreatedAt, CreatedBy, ...         │
┌─────────────────────────────┐   └───────────────────────────────────┘
│   AvaliacaoFornecedor       │
├─────────────────────────────┤   ┌───────────────────────────────────┐
│ Id (PK)          UUID       │   │   HomologacaoFornecedor           │
│ FornecedorId (FK) UUID      │   ├───────────────────────────────────┤
│ ClienteId (FK)   UUID       │   │ Id (PK)              UUID         │
│ Periodo          DATE       │   │ FornecedorId (FK)    UUID         │
│ NotaQualidade    INT(1-5)   │   │ ClienteId (FK)       UUID         │
│ NotaPrazo        INT(1-5)   │   │ Status               VARCHAR(50)  │
│ NotaCusto        INT(1-5)   │   │ AprovadorId (FK)     UUID         │
│ NotaAtendimento  INT(1-5)   │   │ DataAprovacao        DATETIME2    │
│ NotaMedia (comp) DECIMAL    │   │ DataSolicitacao      DATETIME2    │
│ Comentarios      TEXT       │   │ DocumentosAnexos     TEXT (JSON)  │
│ AvaliadorId (FK) UUID       │   │ Justificativa        TEXT         │
│ CreatedAt, ...              │   │ MotivoRejeicao       TEXT         │
└─────────────────────────────┘   │ CreatedAt, CreatedBy, ...         │
                                  └───────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: Fornecedor

**Descrição:** Cadastro de fornecedores/parceiros de TI e Telecom (operadoras, fabricantes, revendas, prestadores de serviço). Centraliza dados cadastrais, bancários e status de homologação.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| CNPJ | VARCHAR(14) | NÃO | - | CNPJ sem formatação (apenas números) |
| RazaoSocial | VARCHAR(200) | NÃO | - | Razão social da empresa |
| NomeFantasia | VARCHAR(200) | SIM | NULL | Nome fantasia |
| CategoriaFornecedor | VARCHAR(50) | NÃO | - | OPERADORA, FABRICANTE, REVENDA, PRESTADOR_SERVICO, SOFTWARE_HOUSE, TRANSPORTADORA |
| Endereco | VARCHAR(300) | SIM | NULL | Endereço completo |
| Cidade | VARCHAR(100) | SIM | NULL | Cidade |
| Estado | VARCHAR(2) | SIM | NULL | UF |
| CEP | VARCHAR(8) | SIM | NULL | CEP sem formatação |
| Telefone | VARCHAR(20) | SIM | NULL | Telefone principal |
| Email | VARCHAR(200) | SIM | NULL | Email principal |
| Site | VARCHAR(200) | SIM | NULL | URL do website |
| DadosBancarios | TEXT | SIM | NULL | JSON: {banco, agencia, conta, tipo} |
| Homologado | BIT | NÃO | 0 | Se passou por homologação |
| DataHomologacao | DATETIME2 | SIM | NULL | Data da homologação |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_Fornecedor | Id | CLUSTERED | Chave primária |
| IX_Fornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_Fornecedor_CNPJ | CNPJ, ClienteId | NONCLUSTERED UNIQUE | CNPJ único por cliente |
| IX_Fornecedor_RazaoSocial | RazaoSocial, ClienteId | NONCLUSTERED | Busca por razão social |
| IX_Fornecedor_Categoria | CategoriaFornecedor, ClienteId | NONCLUSTERED | Filtro por categoria |
| IX_Fornecedor_Homologado | Homologado, ClienteId | NONCLUSTERED | Filtro homologados |
| IX_Fornecedor_Ativo | Ativo, ClienteId | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_Fornecedor | PRIMARY KEY | Id | Chave primária |
| FK_Fornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_Fornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_Fornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_Fornecedor_CNPJ | UNIQUE | (CNPJ, ClienteId) | CNPJ único |
| CHK_Fornecedor_CNPJ | CHECK | LEN(CNPJ) = 14 | CNPJ 14 dígitos |
| CHK_Fornecedor_Categoria | CHECK | CategoriaFornecedor IN ('OPERADORA', 'FABRICANTE', 'REVENDA', 'PRESTADOR_SERVICO', 'SOFTWARE_HOUSE', 'TRANSPORTADORA') | Categorias válidas |
| CHK_Fornecedor_Estado | CHECK | Estado IS NULL OR LEN(Estado) = 2 | UF 2 caracteres |
| CHK_Fornecedor_CEP | CHECK | CEP IS NULL OR LEN(CEP) = 8 | CEP 8 dígitos |

---

### 2.2 Tabela: DocumentoFornecedor

**Descrição:** Armazena documentos obrigatórios do fornecedor (CNPJ, certidões, alvarás) com controle de validade. Alertas automáticos de vencimento.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoDocumento | VARCHAR(50) | NÃO | - | CNPJ, CND_FEDERAL, CND_ESTADUAL, CND_MUNICIPAL, ALVARA, CONTRATO_SOCIAL |
| NumeroDocumento | VARCHAR(100) | SIM | NULL | Número do documento |
| DataEmissao | DATE | NÃO | - | Data de emissão |
| DataValidade | DATE | NÃO | - | Data de validade |
| CaminhoArquivo | VARCHAR(500) | SIM | NULL | Path do arquivo (Azure Blob, S3) |
| Valido | AS (CASE WHEN CAST(GETDATE() AS DATE) <= DataValidade THEN 1 ELSE 0 END) PERSISTED | - | - | Documento válido (computed) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_DocumentoFornecedor | Id | CLUSTERED | Chave primária |
| IX_DocumentoFornecedor_FornecedorId | FornecedorId, TipoDocumento | NONCLUSTERED | Documentos do fornecedor |
| IX_DocumentoFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_DocumentoFornecedor_DataValidade | DataValidade, Valido | NONCLUSTERED | Controle de vencimentos |
| IX_DocumentoFornecedor_TipoDocumento | TipoDocumento, FornecedorId | NONCLUSTERED | Busca por tipo |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_DocumentoFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_DocumentoFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_DocumentoFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_DocumentoFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_DocumentoFornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_DocumentoFornecedor_TipoDocumento | CHECK | TipoDocumento IN ('CNPJ', 'CND_FEDERAL', 'CND_ESTADUAL', 'CND_MUNICIPAL', 'ALVARA', 'CONTRATO_SOCIAL') | Tipos válidos |
| CHK_DocumentoFornecedor_DataValidadeMaiorEmissao | CHECK | DataValidade >= DataEmissao | Validade >= Emissão |

---

### 2.3 Tabela: ContratoFornecedor

**Descrição:** Contratos firmados com fornecedores incluindo vigência, valores, renovação automática e anexo do documento.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| NumeroContrato | VARCHAR(100) | NÃO | - | Número do contrato |
| TipoContrato | VARCHAR(50) | NÃO | - | PRESTACAO_SERVICO, FORNECIMENTO, MANUTENCAO, LOCACAO |
| DataInicio | DATE | NÃO | - | Data início vigência |
| DataFim | DATE | NÃO | - | Data fim vigência |
| ValorMensal | DECIMAL(18,2) | SIM | NULL | Valor mensal |
| ValorTotal | DECIMAL(18,2) | NÃO | - | Valor total do contrato |
| RenovacaoAutomatica | BIT | NÃO | 0 | Se renova automaticamente |
| PrazoRenovacaoMeses | INT | SIM | NULL | Prazo de renovação em meses |
| CaminhoArquivoPDF | VARCHAR(500) | SIM | NULL | Path do contrato PDF |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ContratoFornecedor | Id | CLUSTERED | Chave primária |
| IX_ContratoFornecedor_FornecedorId | FornecedorId | NONCLUSTERED | Contratos do fornecedor |
| IX_ContratoFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_ContratoFornecedor_NumeroContrato | NumeroContrato, ClienteId | NONCLUSTERED | Busca por número |
| IX_ContratoFornecedor_DataFim | DataFim, Ativo | NONCLUSTERED | Controle de vencimentos |
| IX_ContratoFornecedor_RenovacaoAutomatica | RenovacaoAutomatica, DataFim | NONCLUSTERED | Contratos com renovação |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ContratoFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_ContratoFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_ContratoFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_ContratoFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_ContratoFornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_ContratoFornecedor_TipoContrato | CHECK | TipoContrato IN ('PRESTACAO_SERVICO', 'FORNECIMENTO', 'MANUTENCAO', 'LOCACAO') | Tipos válidos |
| CHK_ContratoFornecedor_DataFimMaiorInicio | CHECK | DataFim > DataInicio | Fim > Início |
| CHK_ContratoFornecedor_ValorTotal | CHECK | ValorTotal >= 0 | Valor não negativo |

---

### 2.4 Tabela: ContatoFornecedor

**Descrição:** Contatos múltiplos do fornecedor por departamento (comercial, técnico, financeiro, compras). Permite ter contato primário por departamento.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Nome | VARCHAR(200) | NÃO | - | Nome completo do contato |
| Cargo | VARCHAR(100) | SIM | NULL | Cargo na empresa |
| Departamento | VARCHAR(50) | NÃO | - | COMERCIAL, TECNICO, FINANCEIRO, COMPRAS, DIRETORIA |
| Telefone | VARCHAR(20) | SIM | NULL | Telefone direto |
| Celular | VARCHAR(20) | SIM | NULL | Celular |
| Email | VARCHAR(200) | NÃO | - | Email |
| Primario | BIT | NÃO | 0 | Se é contato primário do departamento |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ContatoFornecedor | Id | CLUSTERED | Chave primária |
| IX_ContatoFornecedor_FornecedorId | FornecedorId, Departamento | NONCLUSTERED | Contatos do fornecedor |
| IX_ContatoFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_ContatoFornecedor_Email | Email, FornecedorId | NONCLUSTERED | Busca por email |
| IX_ContatoFornecedor_Primario | FornecedorId, Departamento, Primario | NONCLUSTERED | Contatos primários |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_ContatoFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_ContatoFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_ContatoFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_ContatoFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_ContatoFornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_ContatoFornecedor_Departamento | CHECK | Departamento IN ('COMERCIAL', 'TECNICO', 'FINANCEIRO', 'COMPRAS', 'DIRETORIA') | Departamentos válidos |

---

### 2.5 Tabela: SLAFornecedor

**Descrição:** Define SLA contratual por tipo de serviço prestado pelo fornecedor. Inclui meta de cumprimento e tracking de performance real.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| TipoServico | VARCHAR(50) | NÃO | - | REPARO, INSTALACAO, SUPORTE, ENTREGA, MANUTENCAO |
| TempoRespostaHoras | INT | NÃO | - | Tempo máximo para resposta (horas) |
| TempoResolucaoDias | INT | NÃO | - | Tempo máximo para resolução (dias úteis) |
| PercentualCumprimento | DECIMAL(5,2) | NÃO | 95.00 | Meta de cumprimento (%) |
| MetaAtual | DECIMAL(5,2) | SIM | NULL | % cumprimento real (atualizado por job) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SLAFornecedor | Id | CLUSTERED | Chave primária |
| IX_SLAFornecedor_FornecedorId | FornecedorId, TipoServico | NONCLUSTERED | SLAs do fornecedor |
| IX_SLAFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_SLAFornecedor_TipoServico | TipoServico, FornecedorId | NONCLUSTERED | Busca por tipo |
| IX_SLAFornecedor_MetaAtual | MetaAtual, FornecedorId | NONCLUSTERED | Ranking por performance |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_SLAFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_SLAFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_SLAFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_SLAFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_SLAFornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_SLAFornecedor_FornecedorTipo | UNIQUE | (FornecedorId, TipoServico) | SLA único por tipo |
| CHK_SLAFornecedor_TipoServico | CHECK | TipoServico IN ('REPARO', 'INSTALACAO', 'SUPORTE', 'ENTREGA', 'MANUTENCAO') | Tipos válidos |
| CHK_SLAFornecedor_TempoResposta | CHECK | TempoRespostaHoras > 0 | Tempo positivo |
| CHK_SLAFornecedor_TempoResolucao | CHECK | TempoResolucaoDias > 0 | Tempo positivo |
| CHK_SLAFornecedor_PercentualCumprimento | CHECK | PercentualCumprimento BETWEEN 0 AND 100 | Percentual 0-100 |

---

### 2.6 Tabela: AvaliacaoFornecedor

**Descrição:** Avaliações periódicas (trimestrais/anuais) de fornecedores em 4 dimensões: qualidade, prazo, custo e atendimento. Gera nota média calculada.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Periodo | DATE | NÃO | - | Período da avaliação (YYYY-MM-DD) |
| NotaQualidade | INT | NÃO | - | Nota qualidade (1-5) |
| NotaPrazo | INT | NÃO | - | Nota cumprimento prazo (1-5) |
| NotaCusto | INT | NÃO | - | Nota custo-benefício (1-5) |
| NotaAtendimento | INT | NÃO | - | Nota atendimento/suporte (1-5) |
| NotaMedia | AS ((NotaQualidade + NotaPrazo + NotaCusto + NotaAtendimento) / 4.0) PERSISTED | - | - | Média calculada |
| Comentarios | TEXT | SIM | NULL | Comentários gerais |
| AvaliadorId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario (avaliador) |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_AvaliacaoFornecedor | Id | CLUSTERED | Chave primária |
| IX_AvaliacaoFornecedor_FornecedorId | FornecedorId, Periodo DESC | NONCLUSTERED | Avaliações do fornecedor |
| IX_AvaliacaoFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_AvaliacaoFornecedor_Periodo | Periodo DESC | NONCLUSTERED | Ordenação temporal |
| IX_AvaliacaoFornecedor_NotaMedia | NotaMedia DESC, FornecedorId | NONCLUSTERED | Ranking fornecedores |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_AvaliacaoFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_AvaliacaoFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_AvaliacaoFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_AvaliacaoFornecedor_Avaliador | FOREIGN KEY | AvaliadorId REFERENCES Usuario(Id) | Avaliador |
| FK_AvaliacaoFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_AvaliacaoFornecedor_FornecedorPeriodo | UNIQUE | (FornecedorId, Periodo) | Uma avaliação por período |
| CHK_AvaliacaoFornecedor_NotaQualidade | CHECK | NotaQualidade BETWEEN 1 AND 5 | Nota 1-5 |
| CHK_AvaliacaoFornecedor_NotaPrazo | CHECK | NotaPrazo BETWEEN 1 AND 5 | Nota 1-5 |
| CHK_AvaliacaoFornecedor_NotaCusto | CHECK | NotaCusto BETWEEN 1 AND 5 | Nota 1-5 |
| CHK_AvaliacaoFornecedor_NotaAtendimento | CHECK | NotaAtendimento BETWEEN 1 AND 5 | Nota 1-5 |

---

### 2.7 Tabela: HomologacaoFornecedor

**Descrição:** Processo de homologação de fornecedores. Controla aprovação/rejeição, documentos necessários e status do processo.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| FornecedorId | UNIQUEIDENTIFIER | NÃO | - | FK para Fornecedor |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Status | VARCHAR(50) | NÃO | 'EM_ANALISE' | EM_ANALISE, APROVADO, REJEITADO, PENDENTE_DOCUMENTACAO |
| AprovadorId | UNIQUEIDENTIFIER | SIM | NULL | FK para Usuario (aprovador) |
| DataAprovacao | DATETIME2 | SIM | NULL | Data da aprovação/rejeição |
| DataSolicitacao | DATETIME2 | NÃO | GETUTCDATE() | Data da solicitação |
| DocumentosAnexos | TEXT | SIM | NULL | JSON array de documentos anexados |
| Justificativa | TEXT | SIM | NULL | Justificativa da solicitação |
| MotivoRejeicao | TEXT | SIM | NULL | Motivo da rejeição (se aplicável) |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_HomologacaoFornecedor | Id | CLUSTERED | Chave primária |
| IX_HomologacaoFornecedor_FornecedorId | FornecedorId | NONCLUSTERED | Homologações do fornecedor |
| IX_HomologacaoFornecedor_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_HomologacaoFornecedor_Status | Status, DataSolicitacao DESC | NONCLUSTERED | Filtro por status |
| IX_HomologacaoFornecedor_AprovadorId | AprovadorId | NONCLUSTERED | Homologações por aprovador |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_HomologacaoFornecedor | PRIMARY KEY | Id | Chave primária |
| FK_HomologacaoFornecedor_Fornecedor | FOREIGN KEY | FornecedorId REFERENCES Fornecedor(Id) ON DELETE CASCADE | Fornecedor pai |
| FK_HomologacaoFornecedor_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_HomologacaoFornecedor_Aprovador | FOREIGN KEY | AprovadorId REFERENCES Usuario(Id) | Aprovador |
| FK_HomologacaoFornecedor_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_HomologacaoFornecedor_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_HomologacaoFornecedor_Status | CHECK | Status IN ('EM_ANALISE', 'APROVADO', 'REJEITADO', 'PENDENTE_DOCUMENTACAO') | Status válidos |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| GestaoCliente | 1:N | Fornecedor | Cliente possui múltiplos fornecedores |
| Fornecedor | 1:N | DocumentoFornecedor | Fornecedor possui documentos |
| Fornecedor | 1:N | ContratoFornecedor | Fornecedor possui contratos |
| Fornecedor | 1:N | ContatoFornecedor | Fornecedor possui contatos |
| Fornecedor | 1:N | SLAFornecedor | Fornecedor possui SLAs |
| Fornecedor | 1:N | AvaliacaoFornecedor | Fornecedor possui avaliações |
| Fornecedor | 1:1 | HomologacaoFornecedor | Fornecedor tem homologação |
| Usuario | 1:N | AvaliacaoFornecedor | Usuário avalia fornecedores |
| Usuario | 1:N | HomologacaoFornecedor | Usuário aprova/rejeita homologação |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF062 - Gestão de Fornecedores e Parceiros
-- Modelo de Dados
-- Data: 2025-12-18
-- Versão: 1.0
-- =============================================

-- ---------------------------------------------
-- Tabela: Fornecedor
-- ---------------------------------------------
CREATE TABLE Fornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CNPJ VARCHAR(14) NOT NULL,
    RazaoSocial VARCHAR(200) NOT NULL,
    NomeFantasia VARCHAR(200) NULL,
    CategoriaFornecedor VARCHAR(50) NOT NULL,
    Endereco VARCHAR(300) NULL,
    Cidade VARCHAR(100) NULL,
    Estado VARCHAR(2) NULL,
    CEP VARCHAR(8) NULL,
    Telefone VARCHAR(20) NULL,
    Email VARCHAR(200) NULL,
    Site VARCHAR(200) NULL,
    DadosBancarios TEXT NULL,
    Homologado BIT NOT NULL DEFAULT 0,
    DataHomologacao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_Fornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_Fornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_Fornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT UQ_Fornecedor_CNPJ UNIQUE (CNPJ, ClienteId),
    CONSTRAINT CHK_Fornecedor_CNPJ CHECK (LEN(CNPJ) = 14),
    CONSTRAINT CHK_Fornecedor_Categoria CHECK (CategoriaFornecedor IN ('OPERADORA', 'FABRICANTE', 'REVENDA', 'PRESTADOR_SERVICO', 'SOFTWARE_HOUSE', 'TRANSPORTADORA')),
    CONSTRAINT CHK_Fornecedor_Estado CHECK (Estado IS NULL OR LEN(Estado) = 2),
    CONSTRAINT CHK_Fornecedor_CEP CHECK (CEP IS NULL OR LEN(CEP) = 8)
);

CREATE NONCLUSTERED INDEX IX_Fornecedor_ClienteId ON Fornecedor(ClienteId);
CREATE UNIQUE NONCLUSTERED INDEX IX_Fornecedor_CNPJ ON Fornecedor(CNPJ, ClienteId);
CREATE NONCLUSTERED INDEX IX_Fornecedor_RazaoSocial ON Fornecedor(RazaoSocial, ClienteId);
CREATE NONCLUSTERED INDEX IX_Fornecedor_Categoria ON Fornecedor(CategoriaFornecedor, ClienteId);
CREATE NONCLUSTERED INDEX IX_Fornecedor_Homologado ON Fornecedor(Homologado, ClienteId);
CREATE NONCLUSTERED INDEX IX_Fornecedor_Ativo ON Fornecedor(Ativo, ClienteId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: DocumentoFornecedor
-- ---------------------------------------------
CREATE TABLE DocumentoFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoDocumento VARCHAR(50) NOT NULL,
    NumeroDocumento VARCHAR(100) NULL,
    DataEmissao DATE NOT NULL,
    DataValidade DATE NOT NULL,
    CaminhoArquivo VARCHAR(500) NULL,
    Valido AS (CASE WHEN CAST(GETDATE() AS DATE) <= DataValidade THEN 1 ELSE 0 END) PERSISTED,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_DocumentoFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_DocumentoFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_DocumentoFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_DocumentoFornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_DocumentoFornecedor_TipoDocumento CHECK (TipoDocumento IN ('CNPJ', 'CND_FEDERAL', 'CND_ESTADUAL', 'CND_MUNICIPAL', 'ALVARA', 'CONTRATO_SOCIAL')),
    CONSTRAINT CHK_DocumentoFornecedor_DataValidadeMaiorEmissao CHECK (DataValidade >= DataEmissao)
);

CREATE NONCLUSTERED INDEX IX_DocumentoFornecedor_FornecedorId ON DocumentoFornecedor(FornecedorId, TipoDocumento);
CREATE NONCLUSTERED INDEX IX_DocumentoFornecedor_ClienteId ON DocumentoFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_DocumentoFornecedor_DataValidade ON DocumentoFornecedor(DataValidade, Valido);
CREATE NONCLUSTERED INDEX IX_DocumentoFornecedor_TipoDocumento ON DocumentoFornecedor(TipoDocumento, FornecedorId);


-- ---------------------------------------------
-- Tabela: ContratoFornecedor
-- ---------------------------------------------
CREATE TABLE ContratoFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NumeroContrato VARCHAR(100) NOT NULL,
    TipoContrato VARCHAR(50) NOT NULL,
    DataInicio DATE NOT NULL,
    DataFim DATE NOT NULL,
    ValorMensal DECIMAL(18,2) NULL,
    ValorTotal DECIMAL(18,2) NOT NULL,
    RenovacaoAutomatica BIT NOT NULL DEFAULT 0,
    PrazoRenovacaoMeses INT NULL,
    CaminhoArquivoPDF VARCHAR(500) NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_ContratoFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ContratoFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_ContratoFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_ContratoFornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_ContratoFornecedor_TipoContrato CHECK (TipoContrato IN ('PRESTACAO_SERVICO', 'FORNECIMENTO', 'MANUTENCAO', 'LOCACAO')),
    CONSTRAINT CHK_ContratoFornecedor_DataFimMaiorInicio CHECK (DataFim > DataInicio),
    CONSTRAINT CHK_ContratoFornecedor_ValorTotal CHECK (ValorTotal >= 0)
);

CREATE NONCLUSTERED INDEX IX_ContratoFornecedor_FornecedorId ON ContratoFornecedor(FornecedorId);
CREATE NONCLUSTERED INDEX IX_ContratoFornecedor_ClienteId ON ContratoFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_ContratoFornecedor_NumeroContrato ON ContratoFornecedor(NumeroContrato, ClienteId);
CREATE NONCLUSTERED INDEX IX_ContratoFornecedor_DataFim ON ContratoFornecedor(DataFim, Ativo);
CREATE NONCLUSTERED INDEX IX_ContratoFornecedor_RenovacaoAutomatica ON ContratoFornecedor(RenovacaoAutomatica, DataFim) WHERE RenovacaoAutomatica = 1;


-- ---------------------------------------------
-- Tabela: ContatoFornecedor
-- ---------------------------------------------
CREATE TABLE ContatoFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Cargo VARCHAR(100) NULL,
    Departamento VARCHAR(50) NOT NULL,
    Telefone VARCHAR(20) NULL,
    Celular VARCHAR(20) NULL,
    Email VARCHAR(200) NOT NULL,
    Primario BIT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_ContatoFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_ContatoFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_ContatoFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_ContatoFornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_ContatoFornecedor_Departamento CHECK (Departamento IN ('COMERCIAL', 'TECNICO', 'FINANCEIRO', 'COMPRAS', 'DIRETORIA'))
);

CREATE NONCLUSTERED INDEX IX_ContatoFornecedor_FornecedorId ON ContatoFornecedor(FornecedorId, Departamento);
CREATE NONCLUSTERED INDEX IX_ContatoFornecedor_ClienteId ON ContatoFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_ContatoFornecedor_Email ON ContatoFornecedor(Email, FornecedorId);
CREATE NONCLUSTERED INDEX IX_ContatoFornecedor_Primario ON ContatoFornecedor(FornecedorId, Departamento, Primario) WHERE Primario = 1;


-- ---------------------------------------------
-- Tabela: SLAFornecedor
-- ---------------------------------------------
CREATE TABLE SLAFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoServico VARCHAR(50) NOT NULL,
    TempoRespostaHoras INT NOT NULL,
    TempoResolucaoDias INT NOT NULL,
    PercentualCumprimento DECIMAL(5,2) NOT NULL DEFAULT 95.00,
    MetaAtual DECIMAL(5,2) NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_SLAFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SLAFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_SLAFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_SLAFornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT UQ_SLAFornecedor_FornecedorTipo UNIQUE (FornecedorId, TipoServico),
    CONSTRAINT CHK_SLAFornecedor_TipoServico CHECK (TipoServico IN ('REPARO', 'INSTALACAO', 'SUPORTE', 'ENTREGA', 'MANUTENCAO')),
    CONSTRAINT CHK_SLAFornecedor_TempoResposta CHECK (TempoRespostaHoras > 0),
    CONSTRAINT CHK_SLAFornecedor_TempoResolucao CHECK (TempoResolucaoDias > 0),
    CONSTRAINT CHK_SLAFornecedor_PercentualCumprimento CHECK (PercentualCumprimento BETWEEN 0 AND 100)
);

CREATE NONCLUSTERED INDEX IX_SLAFornecedor_FornecedorId ON SLAFornecedor(FornecedorId, TipoServico);
CREATE NONCLUSTERED INDEX IX_SLAFornecedor_ClienteId ON SLAFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_SLAFornecedor_TipoServico ON SLAFornecedor(TipoServico, FornecedorId);
CREATE NONCLUSTERED INDEX IX_SLAFornecedor_MetaAtual ON SLAFornecedor(MetaAtual, FornecedorId) WHERE MetaAtual IS NOT NULL;


-- ---------------------------------------------
-- Tabela: AvaliacaoFornecedor
-- ---------------------------------------------
CREATE TABLE AvaliacaoFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Periodo DATE NOT NULL,
    NotaQualidade INT NOT NULL,
    NotaPrazo INT NOT NULL,
    NotaCusto INT NOT NULL,
    NotaAtendimento INT NOT NULL,
    NotaMedia AS ((NotaQualidade + NotaPrazo + NotaCusto + NotaAtendimento) / 4.0) PERSISTED,
    Comentarios TEXT NULL,
    AvaliadorId UNIQUEIDENTIFIER NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,

    CONSTRAINT FK_AvaliacaoFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_AvaliacaoFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_AvaliacaoFornecedor_Avaliador FOREIGN KEY (AvaliadorId) REFERENCES Usuario(Id),
    CONSTRAINT FK_AvaliacaoFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT UQ_AvaliacaoFornecedor_FornecedorPeriodo UNIQUE (FornecedorId, Periodo),
    CONSTRAINT CHK_AvaliacaoFornecedor_NotaQualidade CHECK (NotaQualidade BETWEEN 1 AND 5),
    CONSTRAINT CHK_AvaliacaoFornecedor_NotaPrazo CHECK (NotaPrazo BETWEEN 1 AND 5),
    CONSTRAINT CHK_AvaliacaoFornecedor_NotaCusto CHECK (NotaCusto BETWEEN 1 AND 5),
    CONSTRAINT CHK_AvaliacaoFornecedor_NotaAtendimento CHECK (NotaAtendimento BETWEEN 1 AND 5)
);

CREATE NONCLUSTERED INDEX IX_AvaliacaoFornecedor_FornecedorId ON AvaliacaoFornecedor(FornecedorId, Periodo DESC);
CREATE NONCLUSTERED INDEX IX_AvaliacaoFornecedor_ClienteId ON AvaliacaoFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_AvaliacaoFornecedor_Periodo ON AvaliacaoFornecedor(Periodo DESC);
CREATE NONCLUSTERED INDEX IX_AvaliacaoFornecedor_NotaMedia ON AvaliacaoFornecedor(NotaMedia DESC, FornecedorId);


-- ---------------------------------------------
-- Tabela: HomologacaoFornecedor
-- ---------------------------------------------
CREATE TABLE HomologacaoFornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    FornecedorId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    [Status] VARCHAR(50) NOT NULL DEFAULT 'EM_ANALISE',
    AprovadorId UNIQUEIDENTIFIER NULL,
    DataAprovacao DATETIME2 NULL,
    DataSolicitacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    DocumentosAnexos TEXT NULL,
    Justificativa TEXT NULL,
    MotivoRejeicao TEXT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    CONSTRAINT FK_HomologacaoFornecedor_Fornecedor FOREIGN KEY (FornecedorId) REFERENCES Fornecedor(Id) ON DELETE CASCADE,
    CONSTRAINT FK_HomologacaoFornecedor_Cliente FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_HomologacaoFornecedor_Aprovador FOREIGN KEY (AprovadorId) REFERENCES Usuario(Id),
    CONSTRAINT FK_HomologacaoFornecedor_CreatedBy FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_HomologacaoFornecedor_ModifiedBy FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),
    CONSTRAINT CHK_HomologacaoFornecedor_Status CHECK ([Status] IN ('EM_ANALISE', 'APROVADO', 'REJEITADO', 'PENDENTE_DOCUMENTACAO'))
);

CREATE NONCLUSTERED INDEX IX_HomologacaoFornecedor_FornecedorId ON HomologacaoFornecedor(FornecedorId);
CREATE NONCLUSTERED INDEX IX_HomologacaoFornecedor_ClienteId ON HomologacaoFornecedor(ClienteId);
CREATE NONCLUSTERED INDEX IX_HomologacaoFornecedor_Status ON HomologacaoFornecedor([Status], DataSolicitacao DESC);
CREATE NONCLUSTERED INDEX IX_HomologacaoFornecedor_AprovadorId ON HomologacaoFornecedor(AprovadorId) WHERE AprovadorId IS NOT NULL;
```

---

## 5. Stored Procedures

```sql
-- Procedure: Verificar documentação válida do fornecedor
CREATE PROCEDURE sp_VerificarDocumentacaoFornecedor
    @FornecedorId UNIQUEIDENTIFIER,
    @Habilitado BIT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @DocumentosObrigatorios TABLE (TipoDocumento VARCHAR(50));
    INSERT INTO @DocumentosObrigatorios VALUES ('CNPJ'), ('CND_FEDERAL'), ('CND_ESTADUAL');

    SELECT @Habilitado = CASE
        WHEN COUNT(*) = (SELECT COUNT(*) FROM @DocumentosObrigatorios)
        THEN 1
        ELSE 0
    END
    FROM DocumentoFornecedor d
    INNER JOIN @DocumentosObrigatorios o ON d.TipoDocumento = o.TipoDocumento
    WHERE d.FornecedorId = @FornecedorId
        AND d.Valido = 1
        AND d.Ativo = 1;

    IF @Habilitado IS NULL
        SET @Habilitado = 0;
END;
GO

-- Procedure: Obter ranking de fornecedores por categoria
CREATE PROCEDURE sp_ObterRankingFornecedores
    @ClienteId UNIQUEIDENTIFIER,
    @Categoria VARCHAR(50) = NULL,
    @Top INT = 10
AS
BEGIN
    SET NOCOUNT ON;

    SELECT TOP (@Top)
        f.Id,
        f.CNPJ,
        f.RazaoSocial,
        f.NomeFantasia,
        f.CategoriaFornecedor,
        AVG(a.NotaMedia) AS MediaAvaliacoes,
        COUNT(DISTINCT c.Id) AS QuantidadeContratos,
        AVG(s.MetaAtual) AS MediaSLACumprimento
    FROM Fornecedor f
    LEFT JOIN AvaliacaoFornecedor a ON f.Id = a.FornecedorId AND a.Periodo >= DATEADD(MONTH, -12, GETDATE())
    LEFT JOIN ContratoFornecedor c ON f.Id = c.FornecedorId AND c.Ativo = 1
    LEFT JOIN SLAFornecedor s ON f.Id = s.FornecedorId AND s.Ativo = 1
    WHERE f.ClienteId = @ClienteId
        AND f.Ativo = 1
        AND f.Homologado = 1
        AND (@Categoria IS NULL OR f.CategoriaFornecedor = @Categoria)
    GROUP BY f.Id, f.CNPJ, f.RazaoSocial, f.NomeFantasia, f.CategoriaFornecedor
    ORDER BY MediaAvaliacoes DESC, MediaSLACumprimento DESC;
END;
GO
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect | Versão inicial - 7 tabelas, 45+ índices, views, procedures |

---

**Total de Tabelas:** 7
**Total de Índices:** 47
**Total de Stored Procedures:** 2
**Linhas de DDL:** ~800

**Documento gerado em:** 2025-12-18
**Status:** Aprovado para implementação

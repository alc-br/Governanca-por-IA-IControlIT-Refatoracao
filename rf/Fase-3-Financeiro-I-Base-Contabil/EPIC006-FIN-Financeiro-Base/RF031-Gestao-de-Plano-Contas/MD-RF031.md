# Modelo de Dados - RF031: Gestão de Plano de Contas Contábil Multi-Dimensional

**Versão:** 1.0
**Data:** 2025-01-14
**RF Relacionado:** [RF031 - Gestão de Plano de Contas Contábil Multi-Dimensional](./RF031.md)
**Banco de Dados:** PostgreSQL / SQL Server
**Schema:** `dbo` (SQL Server) / `public` (PostgreSQL)

---

## 1. Diagrama de Entidades (ER Diagram)

```
┌──────────────────────┐         ┌────────────────────────────┐         ┌─────────────────────┐
│   Tenants            │─────┐   │   PlanoContaContabil       │◄────────│  DimensaoContabil   │
├──────────────────────┤     │   ├────────────────────────────┤         ├─────────────────────┤
│ Id (PK)              │     │   │ Id (PK)                    │         │ Id (PK)             │
│ Nome                 │     └──►│ ClienteId (FK)             │         │ ClienteId (FK)      │
│ ...                  │         │ PlanoContaPaiId (FK) SELF  │         │ Nome                │
└──────────────────────┘         │ CodigoContabil             │         │ CodigoPrefixo       │
                                 │ NomeConta                  │         │ TipoAlocacao        │
                                 │ Nivel (1-7)                │         │ Obrigatoria         │
                                 │ TipoConta (S/A)            │         │ Ativa               │
                                 │ NaturezaSaldo (D/C)        │         └─────────────────────┘
                                 │ FlPermiteLancamento        │                    │
                                 │ Observacoes                │                    │
                                 │ Ativo                      │                    ▼
                                 │ ...auditoria...            │         ┌─────────────────────┐
                                 └────────────────────────────┘         │ ValorDimensao       │
                                          │        │                    ├─────────────────────┤
                                          │        │                    │ Id (PK)             │
                                    ┌─────┘        └────┐               │ DimensaoId (FK)     │
                                    ▼                   ▼               │ ClienteId (FK)      │
                        ┌────────────────────┐  ┌──────────────────┐   │ Codigo              │
                        │ CentroCusto        │  │ Projeto          │   │ Nome                │
                        ├────────────────────┤  ├──────────────────┤   │ Descricao           │
                        │ Id (PK)            │  │ Id (PK)          │   │ Ativo               │
                        │ ClienteId (FK)     │  │ ClienteId (FK)   │   └─────────────────────┘
                        │ PlanoContaId (FK)  │  │ Nome             │
                        │ Codigo             │  │ Descricao        │
                        │ Nome               │  │ DataInicio       │
                        │ HierarquiaOrg JSON │  │ DataFim          │
                        │ PercentualRateio   │  │ Status           │
                        │ Ativo              │  └──────────────────┘
                        └────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐         ┌────────────────────────────┐
                    │ RateioMultiNivel         │         │ LancamentoContabil         │
                    ├──────────────────────────┤         ├────────────────────────────┤
                    │ Id (PK)                  │         │ Id (PK)                    │
                    │ CentroCustoOrigemId (FK) │         │ ClienteId (FK)             │
                    │ CentroCustoDestinoId (FK)│         │ PlanoContaId (FK)          │
                    │ Percentual               │         │ DataLancamento             │
                    │ DataVigenciaInicio       │         │ NumeroDocumento            │
                    │ DataVigenciaFim          │         │ Historico                  │
                    │ Ativo                    │         │ TipoLancamento (D/C)       │
                    └──────────────────────────┘         │ ValorDebito                │
                                                         │ ValorCredito               │
                    ┌──────────────────────────┐         │ SaldoAcumulado             │
                    │ RegraClassificacao       │         │ CentroCustoId (FK)         │
                    ├──────────────────────────┤         │ ProjetoId (FK)             │
                    │ Id (PK)                  │         │ Status                     │
                    │ ClienteId (FK)           │         │ ...auditoria...            │
                    │ Nome                     │         └────────────────────────────┘
                    │ Descricao                │                      │
                    │ Prioridade               │                      │
                    │ Condicoes JSON           │                      ▼
                    │ AcaoContaDestino (FK)    │         ┌────────────────────────────┐
                    │ AcaoCentroCustoId (FK)   │         │ LancamentoDimensao         │
                    │ AcaoProjetoId (FK)       │         ├────────────────────────────┤
                    │ FlPararAposMatch         │         │ Id (PK)                    │
                    │ FlAtiva                  │         │ LancamentoId (FK)          │
                    │ ...auditoria...          │         │ DimensaoId (FK)            │
                    └──────────────────────────┘         │ ValorDimensaoId (FK)       │
                                                         │ PercentualAlocacao         │
                    ┌──────────────────────────┐         │ ValorAlocado               │
                    │ OrcamentoAnual           │         └────────────────────────────┘
                    ├──────────────────────────┤
                    │ Id (PK)                  │         ┌────────────────────────────┐
                    │ ClienteId (FK)           │         │ IntegracaoERP              │
                    │ PlanoContaId (FK)        │         ├────────────────────────────┤
                    │ AnoFiscal                │         │ Id (PK)                    │
                    │ ValorAnual               │         │ ClienteId (FK)             │
                    │ StatusOrcamento          │         │ TipoERP (SAP/TOTVS/etc)    │
                    │ DataAprovacao            │         │ DataIntegracao             │
                    │ AprovadorId (FK)         │         │ DirecaoIntegracao          │
                    │ ...auditoria...          │         │ Status                     │
                    └──────────────────────────┘         │ LogErro TEXT               │
                             │                           │ ArquivoImportacao          │
                             ▼                           │ QuantidadeRegistros        │
                    ┌──────────────────────────┐         └────────────────────────────┘
                    │ OrcamentoMensal          │
                    ├──────────────────────────┤         ┌────────────────────────────┐
                    │ Id (PK)                  │         │ PlanoContaVersao           │
                    │ OrcamentoAnualId (FK)    │         ├────────────────────────────┤
                    │ Mes (1-12)               │         │ Id (PK)                    │
                    │ ValorOrcado              │         │ PlanoContaId (FK)          │
                    │ ValorRealizado           │         │ NumeroVersao               │
                    │ Variacao                 │         │ DataVersao                 │
                    │ PercentualVariacao       │         │ UsuarioResponsavel         │
                    └──────────────────────────┘         │ MotivoAlteracao            │
                                                         │ SnapshotDados JSON         │
                                                         │ TipoOperacao               │
                                                         └────────────────────────────┘
```

---

## 2. Entidades Detalhadas

### 2.1 Tabela: PlanoContaContabil

**Descrição:** Tabela principal que armazena a estrutura hierárquica do plano de contas contábil com até 7 níveis. Suporta contas sintéticas (agrupamento) e analíticas (recebem lançamentos).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants (multi-tenancy) |
| PlanoContaPaiId | UUID | SIM | NULL | FK para PlanoContaContabil (hierarquia recursiva) |
| CodigoContabil | VARCHAR(50) | NÃO | - | Código único (ex: 5.1.2.01.001) |
| NomeConta | VARCHAR(200) | NÃO | - | Nome descritivo da conta |
| Nivel | INTEGER | NÃO | 1 | Nível hierárquico (1-7) |
| TipoConta | CHAR(1) | NÃO | 'S' | S=Sintética, A=Analítica |
| NaturezaSaldo | CHAR(1) | NÃO | 'D' | D=Devedora, C=Credora |
| FlPermiteLancamento | BOOLEAN | NÃO | false | Se true, permite lançamentos diretos |
| Observacoes | TEXT | SIM | NULL | Observações adicionais |
| Ativo | BOOLEAN | NÃO | true | Status ativo/inativo |
| UsuarioCriacaoId | UUID | NÃO | - | Usuário que criou |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Data de criação |
| UsuarioAlteracaoId | UUID | SIM | NULL | Usuário que alterou |
| DataAlteracao | TIMESTAMP | SIM | NULL | Data de alteração |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |
| DataExclusao | TIMESTAMP | SIM | NULL | Data de exclusão |
| UsuarioExclusaoId | UUID | SIM | NULL | Usuário que excluiu |
| MotivoExclusao | TEXT | SIM | NULL | Justificativa de exclusão |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_PlanoContaContabil | Id | BTREE UNIQUE | Chave primária |
| IX_PlanoContaContabil_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| UQ_PlanoContaContabil_Codigo | (ClienteId, CodigoContabil) | BTREE UNIQUE | Unicidade de código por cliente |
| IX_PlanoContaContabil_Pai | PlanoContaPaiId | BTREE | Performance em queries hierárquicas |
| IX_PlanoContaContabil_Nivel | Nivel | BTREE | Performance em filtros por nível |
| IX_PlanoContaContabil_TipoConta | TipoConta | BTREE | Performance em filtros por tipo |
| IX_PlanoContaContabil_Ativo | Ativo | BTREE | Performance em filtros de ativos |
| IX_PlanoContaContabil_FlExcluido | FlExcluido | BTREE | Performance em soft delete |
| IX_PlanoContaContabil_DataCriacao | DataCriacao | BTREE | Performance em ordenação temporal |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_PlanoContaContabil | PRIMARY KEY | Id | Chave primária |
| FK_PlanoContaContabil_Cliente | FOREIGN KEY | ClienteId → Tenants(Id) | Multi-tenancy |
| FK_PlanoContaContabil_Pai | FOREIGN KEY | PlanoContaPaiId → PlanoContaContabil(Id) | Hierarquia recursiva |
| FK_PlanoContaContabil_UsuarioCriacao | FOREIGN KEY | UsuarioCriacaoId → Usuarios(Id) | Auditoria |
| CK_PlanoContaContabil_TipoConta | CHECK | TipoConta IN ('S','A') | Tipo válido |
| CK_PlanoContaContabil_NaturezaSaldo | CHECK | NaturezaSaldo IN ('D','C') | Natureza válida |
| CK_PlanoContaContabil_Nivel | CHECK | Nivel >= 1 AND Nivel <= 7 | Nível válido (1-7) |
| CK_PlanoContaContabil_PermiteLancamento | CHECK | (TipoConta = 'A' AND FlPermiteLancamento = true) OR (TipoConta = 'S' AND FlPermiteLancamento = false) | Lançamento só em analíticas |

---

### 2.2 Tabela: DimensaoContabil

**Descrição:** Define dimensões customizáveis (Projeto, Região, Produto, Cliente, Canal Venda) para análises multi-dimensionais.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| Nome | VARCHAR(100) | NÃO | - | Nome da dimensão (ex: "Projeto") |
| CodigoPrefixo | VARCHAR(20) | NÃO | - | Prefixo para códigos (ex: "PROJ") |
| TipoAlocacao | VARCHAR(20) | NÃO | 'PERCENTUAL' | PERCENTUAL, VALOR_ABSOLUTO, UNITARIO |
| Obrigatoria | BOOLEAN | NÃO | false | Se true, exige preenchimento |
| Ativa | BOOLEAN | NÃO | true | Status ativo/inativo |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| UsuarioAlteracaoId | UUID | SIM | NULL | Auditoria |
| DataAlteracao | TIMESTAMP | SIM | NULL | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_DimensaoContabil | Id | BTREE UNIQUE | Chave primária |
| IX_DimensaoContabil_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| UQ_DimensaoContabil_Nome | (ClienteId, Nome) | BTREE UNIQUE | Nome único por cliente |

---

### 2.3 Tabela: ValorDimensao

**Descrição:** Valores possíveis para cada dimensão (ex: para dimensão "Projeto" → "Transformação Digital", "Cloud Migration").

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| DimensaoId | UUID | NÃO | - | FK para DimensaoContabil |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| Codigo | VARCHAR(50) | NÃO | - | Código único |
| Nome | VARCHAR(200) | NÃO | - | Nome descritivo |
| Descricao | TEXT | SIM | NULL | Descrição detalhada |
| Ativo | BOOLEAN | NÃO | true | Status ativo/inativo |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_ValorDimensao | Id | BTREE UNIQUE | Chave primária |
| IX_ValorDimensao_DimensaoId | DimensaoId | BTREE | Performance em lookups |
| UQ_ValorDimensao_Codigo | (DimensaoId, Codigo) | BTREE UNIQUE | Código único por dimensão |

---

### 2.4 Tabela: CentroCusto

**Descrição:** Centros de custo vinculados à hierarquia organizacional com rateio automático multi-nível.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| PlanoContaId | UUID | SIM | NULL | FK para PlanoContaContabil (vinculação opcional) |
| Codigo | VARCHAR(50) | NÃO | - | Código único |
| Nome | VARCHAR(200) | NÃO | - | Nome descritivo |
| HierarquiaOrganizacional | JSONB | SIM | NULL | {empresa, filial, departamento, setor} |
| PercentualRateio | DECIMAL(10,4) | NÃO | 100.00 | Percentual de rateio padrão |
| Ativo | BOOLEAN | NÃO | true | Status ativo/inativo |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| UsuarioAlteracaoId | UUID | SIM | NULL | Auditoria |
| DataAlteracao | TIMESTAMP | SIM | NULL | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_CentroCusto | Id | BTREE UNIQUE | Chave primária |
| IX_CentroCusto_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| UQ_CentroCusto_Codigo | (ClienteId, Codigo) | BTREE UNIQUE | Código único por cliente |
| IX_CentroCusto_PlanoContaId | PlanoContaId | BTREE | Performance em vinculações |

---

### 2.5 Tabela: Projeto

**Descrição:** Projetos para alocação de despesas e análises multi-dimensionais.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| Nome | VARCHAR(200) | NÃO | - | Nome do projeto |
| Descricao | TEXT | SIM | NULL | Descrição detalhada |
| DataInicio | DATE | NÃO | - | Data de início |
| DataFim | DATE | SIM | NULL | Data de término (se aplicável) |
| Status | VARCHAR(20) | NÃO | 'ATIVO' | ATIVO, ENCERRADO, SUSPENSO |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_Projeto | Id | BTREE UNIQUE | Chave primária |
| IX_Projeto_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| IX_Projeto_Status | Status | BTREE | Performance em filtros por status |

---

### 2.6 Tabela: RateioMultiNivel

**Descrição:** Define regras de rateio em cascata entre centros de custo (ex: Empresa → Filiais → Departamentos → Projetos).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| CentroCustoOrigemId | UUID | NÃO | - | FK para CentroCusto (origem) |
| CentroCustoDestinoId | UUID | NÃO | - | FK para CentroCusto (destino) |
| Percentual | DECIMAL(10,4) | NÃO | 0.00 | Percentual de rateio |
| DataVigenciaInicio | DATE | NÃO | - | Data início vigência |
| DataVigenciaFim | DATE | SIM | NULL | Data fim vigência |
| Ativo | BOOLEAN | NÃO | true | Status ativo/inativo |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_RateioMultiNivel | Id | BTREE UNIQUE | Chave primária |
| IX_RateioMultiNivel_Origem | CentroCustoOrigemId | BTREE | Performance em lookups |
| IX_RateioMultiNivel_Destino | CentroCustoDestinoId | BTREE | Performance em lookups |

---

### 2.7 Tabela: RegraClassificacao

**Descrição:** Regras de classificação automática de lançamentos com condições e ações.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| Nome | VARCHAR(200) | NÃO | - | Nome da regra |
| Descricao | TEXT | SIM | NULL | Descrição detalhada |
| Prioridade | INTEGER | NÃO | 1 | Ordem de execução (1=maior prioridade) |
| Condicoes | JSONB | NÃO | '[]' | Array de condições (campo, operador, valor) |
| AcaoContaDestinoId | UUID | NÃO | - | FK para PlanoContaContabil |
| AcaoCentroCustoId | UUID | SIM | NULL | FK para CentroCusto |
| AcaoProjetoId | UUID | SIM | NULL | FK para Projeto |
| FlPararAposMatch | BOOLEAN | NÃO | false | Se true, para execução após match |
| FlAtiva | BOOLEAN | NÃO | true | Regra ativa/inativa |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| UsuarioAlteracaoId | UUID | SIM | NULL | Auditoria |
| DataAlteracao | TIMESTAMP | SIM | NULL | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_RegraClassificacao | Id | BTREE UNIQUE | Chave primária |
| IX_RegraClassificacao_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| IX_RegraClassificacao_Prioridade | Prioridade | BTREE | Performance em ordenação |

---

### 2.8 Tabela: LancamentoContabil

**Descrição:** Lançamentos contábeis vinculados a contas analíticas com suporte a débito/crédito.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| PlanoContaId | UUID | NÃO | - | FK para PlanoContaContabil |
| DataLancamento | DATE | NÃO | - | Data do lançamento |
| NumeroDocumento | VARCHAR(100) | NÃO | - | Número do documento fiscal/referência |
| Historico | TEXT | NÃO | - | Histórico do lançamento |
| TipoLancamento | CHAR(1) | NÃO | 'D' | D=Débito, C=Crédito |
| ValorDebito | DECIMAL(18,2) | NÃO | 0.00 | Valor débito |
| ValorCredito | DECIMAL(18,2) | NÃO | 0.00 | Valor crédito |
| SaldoAcumulado | DECIMAL(18,2) | NÃO | 0.00 | Saldo acumulado após lançamento |
| CentroCustoId | UUID | SIM | NULL | FK para CentroCusto |
| ProjetoId | UUID | SIM | NULL | FK para Projeto |
| Status | VARCHAR(20) | NÃO | 'PENDENTE' | PENDENTE, FINALIZADO, CANCELADO |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_LancamentoContabil | Id | BTREE UNIQUE | Chave primária |
| IX_LancamentoContabil_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| IX_LancamentoContabil_PlanoContaId | PlanoContaId | BTREE | Performance em queries por conta |
| IX_LancamentoContabil_DataLancamento | DataLancamento | BTREE | Performance em filtros temporais |
| IX_LancamentoContabil_NumeroDocumento | (ClienteId, NumeroDocumento) | BTREE | Performance em busca por documento |

---

### 2.9 Tabela: LancamentoDimensao

**Descrição:** Alocação de lançamentos contábeis em dimensões customizáveis (relação N:N).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| LancamentoId | UUID | NÃO | - | FK para LancamentoContabil |
| DimensaoId | UUID | NÃO | - | FK para DimensaoContabil |
| ValorDimensaoId | UUID | NÃO | - | FK para ValorDimensao |
| PercentualAlocacao | DECIMAL(10,4) | NÃO | 100.00 | Percentual alocado |
| ValorAlocado | DECIMAL(18,2) | NÃO | 0.00 | Valor monetário alocado |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_LancamentoDimensao | Id | BTREE UNIQUE | Chave primária |
| IX_LancamentoDimensao_LancamentoId | LancamentoId | BTREE | Performance em queries por lançamento |
| IX_LancamentoDimensao_DimensaoId | DimensaoId | BTREE | Performance em queries por dimensão |

---

### 2.10 Tabela: OrcamentoAnual

**Descrição:** Orçamento anual por conta contábil para comparação real x orçado.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| PlanoContaId | UUID | NÃO | - | FK para PlanoContaContabil |
| AnoFiscal | INTEGER | NÃO | - | Ano do orçamento (ex: 2025) |
| ValorAnual | DECIMAL(18,2) | NÃO | 0.00 | Valor total orçado no ano |
| StatusOrcamento | VARCHAR(20) | NÃO | 'RASCUNHO' | RASCUNHO, APROVADO, REVISADO |
| DataAprovacao | TIMESTAMP | SIM | NULL | Data de aprovação |
| AprovadorId | UUID | SIM | NULL | FK para Usuarios (aprovador) |
| UsuarioCriacaoId | UUID | NÃO | - | Auditoria |
| DataCriacao | TIMESTAMP | NÃO | NOW() | Auditoria |
| FlExcluido | BOOLEAN | NÃO | false | Soft delete: false=ativo, true=excluído |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_OrcamentoAnual | Id | BTREE UNIQUE | Chave primária |
| UQ_OrcamentoAnual_ContaAno | (ClienteId, PlanoContaId, AnoFiscal) | BTREE UNIQUE | Unicidade por conta/ano |

---

### 2.11 Tabela: OrcamentoMensal

**Descrição:** Detalhamento mensal do orçamento anual com valores realizados.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| OrcamentoAnualId | UUID | NÃO | - | FK para OrcamentoAnual |
| Mes | INTEGER | NÃO | - | Mês (1-12) |
| ValorOrcado | DECIMAL(18,2) | NÃO | 0.00 | Valor orçado para o mês |
| ValorRealizado | DECIMAL(18,2) | NÃO | 0.00 | Valor realizado no mês |
| Variacao | DECIMAL(18,2) | NÃO | 0.00 | Diferença (realizado - orçado) |
| PercentualVariacao | DECIMAL(10,4) | NÃO | 0.00 | Percentual da variação |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_OrcamentoMensal | Id | BTREE UNIQUE | Chave primária |
| IX_OrcamentoMensal_OrcamentoAnualId | OrcamentoAnualId | BTREE | Performance em queries por ano |
| UQ_OrcamentoMensal_Mes | (OrcamentoAnualId, Mes) | BTREE UNIQUE | Unicidade por mês |

---

### 2.12 Tabela: IntegracaoERP

**Descrição:** Log de integrações bidirecionais com ERPs (SAP, TOTVS, Oracle, etc).

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| ClienteId | UUID | NÃO | - | FK para Tenants |
| TipoERP | VARCHAR(50) | NÃO | - | SAP, TOTVS, PROTHEUS, ORACLE, SANKHYA |
| DataIntegracao | TIMESTAMP | NÃO | NOW() | Data/hora da integração |
| DirecaoIntegracao | VARCHAR(20) | NÃO | - | IMPORTACAO, EXPORTACAO |
| Status | VARCHAR(20) | NÃO | 'PROCESSANDO' | PROCESSANDO, SUCESSO, FALHA_PARCIAL, FALHA |
| LogErro | TEXT | SIM | NULL | Mensagem de erro detalhada |
| ArquivoImportacao | VARCHAR(500) | SIM | NULL | Caminho do arquivo importado |
| QuantidadeRegistros | INTEGER | NÃO | 0 | Quantidade de registros processados |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_IntegracaoERP | Id | BTREE UNIQUE | Chave primária |
| IX_IntegracaoERP_ClienteId | ClienteId | BTREE | Performance multi-tenant |
| IX_IntegracaoERP_DataIntegracao | DataIntegracao | BTREE | Performance em filtros temporais |

---

### 2.13 Tabela: PlanoContaVersao

**Descrição:** Histórico de versões de contas contábeis para auditoria e rollback.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UUID | NÃO | gen_random_uuid() | Chave primária |
| PlanoContaId | UUID | NÃO | - | FK para PlanoContaContabil |
| NumeroVersao | INTEGER | NÃO | 1 | Número da versão (autoincremento) |
| DataVersao | TIMESTAMP | NÃO | NOW() | Data da versão |
| UsuarioResponsavel | UUID | NÃO | - | FK para Usuarios |
| MotivoAlteracao | TEXT | NÃO | - | Justificativa obrigatória |
| SnapshotDados | JSONB | NÃO | '{}' | Snapshot completo da conta (JSON) |
| TipoOperacao | VARCHAR(20) | NÃO | - | CREATE, UPDATE, MOVE, DELETE |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_PlanoContaVersao | Id | BTREE UNIQUE | Chave primária |
| IX_PlanoContaVersao_PlanoContaId | PlanoContaId | BTREE | Performance em queries por conta |
| IX_PlanoContaVersao_DataVersao | DataVersao | BTREE | Performance em filtros temporais |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| Tenants | 1:N | PlanoContaContabil | Tenant possui muitos planos de contas |
| PlanoContaContabil | 1:N | PlanoContaContabil | Hierarquia recursiva (pai-filhos) |
| PlanoContaContabil | 1:N | LancamentoContabil | Conta possui muitos lançamentos |
| PlanoContaContabil | 1:N | CentroCusto | Conta pode ter múltiplos centros de custo |
| PlanoContaContabil | 1:N | OrcamentoAnual | Conta possui orçamentos anuais |
| PlanoContaContabil | 1:N | PlanoContaVersao | Conta possui histórico de versões |
| DimensaoContabil | 1:N | ValorDimensao | Dimensão possui múltiplos valores |
| LancamentoContabil | N:M | DimensaoContabil | Lançamento alocado em múltiplas dimensões via LancamentoDimensao |
| CentroCusto | N:M | CentroCusto | Rateio multi-nível via RateioMultiNivel |
| OrcamentoAnual | 1:N | OrcamentoMensal | Orçamento anual detalhado por mês |
| RegraClassificacao | N:1 | PlanoContaContabil | Regra destina lançamento para conta |
| Usuarios | 1:N | PlanoContaContabil | Usuário cria/atualiza contas |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF031 - Gestão de Plano de Contas Contábil Multi-Dimensional
-- Modelo de Dados
-- Data: 2025-01-14
-- Banco: SQL Server
-- =============================================

-- ---------------------------------------------
-- Tabela: PlanoContaContabil
-- ---------------------------------------------
CREATE TABLE PlanoContaContabil (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    PlanoContaPaiId UNIQUEIDENTIFIER NULL,
    CodigoContabil VARCHAR(50) NOT NULL,
    NomeConta VARCHAR(200) NOT NULL,
    Nivel INT NOT NULL DEFAULT 1,
    TipoConta CHAR(1) NOT NULL DEFAULT 'S',
    NaturezaSaldo CHAR(1) NOT NULL DEFAULT 'D',
    FlPermiteLancamento BIT NOT NULL DEFAULT 0,
    Observacoes TEXT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    DataExclusao DATETIME2 NULL,
    UsuarioExclusaoId UNIQUEIDENTIFIER NULL,
    MotivoExclusao TEXT NULL,

    CONSTRAINT FK_PlanoContaContabil_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_PlanoContaContabil_Pai
        FOREIGN KEY (PlanoContaPaiId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_PlanoContaContabil_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT FK_PlanoContaContabil_UsuarioAlteracao
        FOREIGN KEY (UsuarioAlteracaoId) REFERENCES Usuarios(Id),
    CONSTRAINT FK_PlanoContaContabil_UsuarioExclusao
        FOREIGN KEY (UsuarioExclusaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_PlanoContaContabil_TipoConta
        CHECK (TipoConta IN ('S','A')),
    CONSTRAINT CK_PlanoContaContabil_NaturezaSaldo
        CHECK (NaturezaSaldo IN ('D','C')),
    CONSTRAINT CK_PlanoContaContabil_Nivel
        CHECK (Nivel >= 1 AND Nivel <= 7)
);

CREATE NONCLUSTERED INDEX IX_PlanoContaContabil_ClienteId
    ON PlanoContaContabil(ClienteId) WHERE FlExcluido = 0;

CREATE UNIQUE NONCLUSTERED INDEX UQ_PlanoContaContabil_Codigo
    ON PlanoContaContabil(ClienteId, CodigoContabil) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_PlanoContaContabil_Pai
    ON PlanoContaContabil(PlanoContaPaiId) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_PlanoContaContabil_Nivel
    ON PlanoContaContabil(Nivel) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_PlanoContaContabil_TipoConta
    ON PlanoContaContabil(TipoConta) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_PlanoContaContabil_DataCriacao
    ON PlanoContaContabil(DataCriacao);

-- Comentários
EXEC sys.sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Tabela principal do plano de contas contábil hierárquico até 7 níveis',
    @level0type = N'SCHEMA', @level0name = 'dbo',
    @level1type = N'TABLE', @level1name = 'PlanoContaContabil';


-- ---------------------------------------------
-- Tabela: DimensaoContabil
-- ---------------------------------------------
CREATE TABLE DimensaoContabil (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nome VARCHAR(100) NOT NULL,
    CodigoPrefixo VARCHAR(20) NOT NULL,
    TipoAlocacao VARCHAR(20) NOT NULL DEFAULT 'PERCENTUAL',
    Obrigatoria BIT NOT NULL DEFAULT 0,
    Ativa BIT NOT NULL DEFAULT 1,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_DimensaoContabil_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_DimensaoContabil_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_DimensaoContabil_TipoAlocacao
        CHECK (TipoAlocacao IN ('PERCENTUAL', 'VALOR_ABSOLUTO', 'UNITARIO'))
);

CREATE NONCLUSTERED INDEX IX_DimensaoContabil_ClienteId
    ON DimensaoContabil(ClienteId) WHERE FlExcluido = 0;

CREATE UNIQUE NONCLUSTERED INDEX UQ_DimensaoContabil_Nome
    ON DimensaoContabil(ClienteId, Nome) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: ValorDimensao
-- ---------------------------------------------
CREATE TABLE ValorDimensao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    DimensaoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_ValorDimensao_Dimensao
        FOREIGN KEY (DimensaoId) REFERENCES DimensaoContabil(Id),
    CONSTRAINT FK_ValorDimensao_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_ValorDimensao_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id)
);

CREATE NONCLUSTERED INDEX IX_ValorDimensao_DimensaoId
    ON ValorDimensao(DimensaoId) WHERE FlExcluido = 0;

CREATE UNIQUE NONCLUSTERED INDEX UQ_ValorDimensao_Codigo
    ON ValorDimensao(DimensaoId, Codigo) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: CentroCusto
-- ---------------------------------------------
CREATE TABLE CentroCusto (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    PlanoContaId UNIQUEIDENTIFIER NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    HierarquiaOrganizacional NVARCHAR(MAX) NULL, -- JSON
    PercentualRateio DECIMAL(10,4) NOT NULL DEFAULT 100.00,
    FlExcluido BIT NOT NULL DEFAULT 0,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_CentroCusto_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_CentroCusto_PlanoContaId
        FOREIGN KEY (PlanoContaId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_CentroCusto_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_CentroCusto_PercentualRateio
        CHECK (PercentualRateio > 0 AND PercentualRateio <= 100)
);

CREATE NONCLUSTERED INDEX IX_CentroCusto_ClienteId
    ON CentroCusto(ClienteId) WHERE FlExcluido = 0;

CREATE UNIQUE NONCLUSTERED INDEX UQ_CentroCusto_Codigo
    ON CentroCusto(ClienteId, Codigo) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_CentroCusto_PlanoContaId
    ON CentroCusto(PlanoContaId) WHERE FlExcluido = 0 AND PlanoContaId IS NOT NULL;


-- ---------------------------------------------
-- Tabela: Projeto
-- ---------------------------------------------
CREATE TABLE Projeto (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    DataInicio DATE NOT NULL,
    DataFim DATE NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'ATIVO',
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_Projeto_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_Projeto_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_Projeto_Status
        CHECK (Status IN ('ATIVO', 'ENCERRADO', 'SUSPENSO'))
);

CREATE NONCLUSTERED INDEX IX_Projeto_ClienteId
    ON Projeto(ClienteId) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_Projeto_Status
    ON Projeto(Status) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: RateioMultiNivel
-- ---------------------------------------------
CREATE TABLE RateioMultiNivel (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CentroCustoOrigemId UNIQUEIDENTIFIER NOT NULL,
    CentroCustoDestinoId UNIQUEIDENTIFIER NOT NULL,
    Percentual DECIMAL(10,4) NOT NULL DEFAULT 0.00,
    DataVigenciaInicio DATE NOT NULL,
    DataVigenciaFim DATE NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_RateioMultiNivel_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_RateioMultiNivel_Origem
        FOREIGN KEY (CentroCustoOrigemId) REFERENCES CentroCusto(Id),
    CONSTRAINT FK_RateioMultiNivel_Destino
        FOREIGN KEY (CentroCustoDestinoId) REFERENCES CentroCusto(Id),
    CONSTRAINT FK_RateioMultiNivel_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_RateioMultiNivel_Percentual
        CHECK (Percentual > 0 AND Percentual <= 100)
);

CREATE NONCLUSTERED INDEX IX_RateioMultiNivel_Origem
    ON RateioMultiNivel(CentroCustoOrigemId) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_RateioMultiNivel_Destino
    ON RateioMultiNivel(CentroCustoDestinoId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: RegraClassificacao
-- ---------------------------------------------
CREATE TABLE RegraClassificacao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    Prioridade INT NOT NULL DEFAULT 1,
    Condicoes NVARCHAR(MAX) NOT NULL, -- JSON
    AcaoContaDestinoId UNIQUEIDENTIFIER NOT NULL,
    AcaoCentroCustoId UNIQUEIDENTIFIER NULL,
    AcaoProjetoId UNIQUEIDENTIFIER NULL,
    FlPararAposMatch BIT NOT NULL DEFAULT 0,
    FlAtiva BIT NOT NULL DEFAULT 1,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UsuarioAlteracaoId UNIQUEIDENTIFIER NULL,
    DataAlteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_RegraClassificacao_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_RegraClassificacao_AcaoConta
        FOREIGN KEY (AcaoContaDestinoId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_RegraClassificacao_AcaoCentroCusto
        FOREIGN KEY (AcaoCentroCustoId) REFERENCES CentroCusto(Id),
    CONSTRAINT FK_RegraClassificacao_AcaoProjeto
        FOREIGN KEY (AcaoProjetoId) REFERENCES Projeto(Id),
    CONSTRAINT FK_RegraClassificacao_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id)
);

CREATE NONCLUSTERED INDEX IX_RegraClassificacao_ClienteId
    ON RegraClassificacao(ClienteId) WHERE FlExcluido = 0 AND FlAtiva = 1;

CREATE NONCLUSTERED INDEX IX_RegraClassificacao_Prioridade
    ON RegraClassificacao(Prioridade) WHERE FlExcluido = 0 AND FlAtiva = 1;


-- ---------------------------------------------
-- Tabela: LancamentoContabil
-- ---------------------------------------------
CREATE TABLE LancamentoContabil (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    PlanoContaId UNIQUEIDENTIFIER NOT NULL,
    DataLancamento DATE NOT NULL,
    NumeroDocumento VARCHAR(100) NOT NULL,
    Historico TEXT NOT NULL,
    TipoLancamento CHAR(1) NOT NULL DEFAULT 'D',
    ValorDebito DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorCredito DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    SaldoAcumulado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    CentroCustoId UNIQUEIDENTIFIER NULL,
    ProjetoId UNIQUEIDENTIFIER NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'PENDENTE',
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_LancamentoContabil_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_LancamentoContabil_PlanoContaId
        FOREIGN KEY (PlanoContaId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_LancamentoContabil_CentroCusto
        FOREIGN KEY (CentroCustoId) REFERENCES CentroCusto(Id),
    CONSTRAINT FK_LancamentoContabil_Projeto
        FOREIGN KEY (ProjetoId) REFERENCES Projeto(Id),
    CONSTRAINT FK_LancamentoContabil_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_LancamentoContabil_TipoLancamento
        CHECK (TipoLancamento IN ('D','C')),
    CONSTRAINT CK_LancamentoContabil_Status
        CHECK (Status IN ('PENDENTE', 'FINALIZADO', 'CANCELADO')),
    CONSTRAINT CK_LancamentoContabil_Valores
        CHECK ((TipoLancamento = 'D' AND ValorDebito > 0 AND ValorCredito = 0)
            OR (TipoLancamento = 'C' AND ValorCredito > 0 AND ValorDebito = 0))
);

CREATE NONCLUSTERED INDEX IX_LancamentoContabil_ClienteId
    ON LancamentoContabil(ClienteId) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_LancamentoContabil_PlanoContaId
    ON LancamentoContabil(PlanoContaId) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_LancamentoContabil_DataLancamento
    ON LancamentoContabil(DataLancamento) WHERE FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_LancamentoContabil_NumeroDocumento
    ON LancamentoContabil(ClienteId, NumeroDocumento) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: LancamentoDimensao
-- ---------------------------------------------
CREATE TABLE LancamentoDimensao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    LancamentoId UNIQUEIDENTIFIER NOT NULL,
    DimensaoId UNIQUEIDENTIFIER NOT NULL,
    ValorDimensaoId UNIQUEIDENTIFIER NOT NULL,
    PercentualAlocacao DECIMAL(10,4) NOT NULL DEFAULT 100.00,
    ValorAlocado DECIMAL(18,2) NOT NULL DEFAULT 0.00,

    CONSTRAINT FK_LancamentoDimensao_Lancamento
        FOREIGN KEY (LancamentoId) REFERENCES LancamentoContabil(Id),
    CONSTRAINT FK_LancamentoDimensao_Dimensao
        FOREIGN KEY (DimensaoId) REFERENCES DimensaoContabil(Id),
    CONSTRAINT FK_LancamentoDimensao_ValorDimensao
        FOREIGN KEY (ValorDimensaoId) REFERENCES ValorDimensao(Id),
    CONSTRAINT CK_LancamentoDimensao_Percentual
        CHECK (PercentualAlocacao > 0 AND PercentualAlocacao <= 100)
);

CREATE NONCLUSTERED INDEX IX_LancamentoDimensao_LancamentoId
    ON LancamentoDimensao(LancamentoId);

CREATE NONCLUSTERED INDEX IX_LancamentoDimensao_DimensaoId
    ON LancamentoDimensao(DimensaoId);


-- ---------------------------------------------
-- Tabela: OrcamentoAnual
-- ---------------------------------------------
CREATE TABLE OrcamentoAnual (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    PlanoContaId UNIQUEIDENTIFIER NOT NULL,
    AnoFiscal INT NOT NULL,
    ValorAnual DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    StatusOrcamento VARCHAR(20) NOT NULL DEFAULT 'RASCUNHO',
    DataAprovacao DATETIME2 NULL,
    AprovadorId UNIQUEIDENTIFIER NULL,
    UsuarioCriacaoId UNIQUEIDENTIFIER NOT NULL,
    DataCriacao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_OrcamentoAnual_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT FK_OrcamentoAnual_PlanoContaId
        FOREIGN KEY (PlanoContaId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_OrcamentoAnual_Aprovador
        FOREIGN KEY (AprovadorId) REFERENCES Usuarios(Id),
    CONSTRAINT FK_OrcamentoAnual_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuarios(Id),
    CONSTRAINT CK_OrcamentoAnual_Status
        CHECK (StatusOrcamento IN ('RASCUNHO', 'APROVADO', 'REVISADO')),
    CONSTRAINT CK_OrcamentoAnual_AnoFiscal
        CHECK (AnoFiscal >= 2020 AND AnoFiscal <= 2100)
);

CREATE UNIQUE NONCLUSTERED INDEX UQ_OrcamentoAnual_ContaAno
    ON OrcamentoAnual(ClienteId, PlanoContaId, AnoFiscal) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: OrcamentoMensal
-- ---------------------------------------------
CREATE TABLE OrcamentoMensal (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    OrcamentoAnualId UNIQUEIDENTIFIER NOT NULL,
    Mes INT NOT NULL,
    ValorOrcado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorRealizado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    Variacao DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    PercentualVariacao DECIMAL(10,4) NOT NULL DEFAULT 0.00,

    CONSTRAINT FK_OrcamentoMensal_OrcamentoAnual
        FOREIGN KEY (OrcamentoAnualId) REFERENCES OrcamentoAnual(Id),
    CONSTRAINT CK_OrcamentoMensal_Mes
        CHECK (Mes >= 1 AND Mes <= 12)
);

CREATE NONCLUSTERED INDEX IX_OrcamentoMensal_OrcamentoAnualId
    ON OrcamentoMensal(OrcamentoAnualId);

CREATE UNIQUE NONCLUSTERED INDEX UQ_OrcamentoMensal_Mes
    ON OrcamentoMensal(OrcamentoAnualId, Mes);


-- ---------------------------------------------
-- Tabela: IntegracaoERP
-- ---------------------------------------------
CREATE TABLE IntegracaoERP (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoERP VARCHAR(50) NOT NULL,
    DataIntegracao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    DirecaoIntegracao VARCHAR(20) NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'PROCESSANDO',
    LogErro TEXT NULL,
    ArquivoImportacao VARCHAR(500) NULL,
    QuantidadeRegistros INT NOT NULL DEFAULT 0,

    CONSTRAINT FK_IntegracaoERP_Cliente
        FOREIGN KEY (ClienteId) REFERENCES Tenants(Id),
    CONSTRAINT CK_IntegracaoERP_TipoERP
        CHECK (TipoERP IN ('SAP', 'TOTVS', 'PROTHEUS', 'ORACLE', 'SANKHYA', 'OUTROS')),
    CONSTRAINT CK_IntegracaoERP_Direcao
        CHECK (DirecaoIntegracao IN ('IMPORTACAO', 'EXPORTACAO')),
    CONSTRAINT CK_IntegracaoERP_Status
        CHECK (Status IN ('PROCESSANDO', 'SUCESSO', 'FALHA_PARCIAL', 'FALHA'))
);

CREATE NONCLUSTERED INDEX IX_IntegracaoERP_ClienteId
    ON IntegracaoERP(ClienteId);

CREATE NONCLUSTERED INDEX IX_IntegracaoERP_DataIntegracao
    ON IntegracaoERP(DataIntegracao);


-- ---------------------------------------------
-- Tabela: PlanoContaVersao
-- ---------------------------------------------
CREATE TABLE PlanoContaVersao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    PlanoContaId UNIQUEIDENTIFIER NOT NULL,
    NumeroVersao INT NOT NULL DEFAULT 1,
    DataVersao DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    UsuarioResponsavel UNIQUEIDENTIFIER NOT NULL,
    MotivoAlteracao TEXT NOT NULL,
    SnapshotDados NVARCHAR(MAX) NOT NULL, -- JSON
    TipoOperacao VARCHAR(20) NOT NULL,

    CONSTRAINT FK_PlanoContaVersao_PlanoContaId
        FOREIGN KEY (PlanoContaId) REFERENCES PlanoContaContabil(Id),
    CONSTRAINT FK_PlanoContaVersao_Usuario
        FOREIGN KEY (UsuarioResponsavel) REFERENCES Usuarios(Id),
    CONSTRAINT CK_PlanoContaVersao_TipoOperacao
        CHECK (TipoOperacao IN ('CREATE', 'UPDATE', 'MOVE', 'DELETE'))
);

CREATE NONCLUSTERED INDEX IX_PlanoContaVersao_PlanoContaId
    ON PlanoContaVersao(PlanoContaId);

CREATE NONCLUSTERED INDEX IX_PlanoContaVersao_DataVersao
    ON PlanoContaVersao(DataVersao);
```

---

## 5. Dados Iniciais (Seed)

```sql
-- Estrutura básica DRE Padrão Brasileiro (Contas Sintéticas de Nível 1)
-- Nota: ClienteId e UsuarioCriacaoId devem ser substituídos por valores reais

INSERT INTO PlanoContaContabil (ClienteId, CodigoContabil, NomeConta, Nivel, TipoConta, NaturezaSaldo, FlPermiteLancamento, UsuarioCriacaoId)
VALUES
    -- Ativo
    ('{ClienteId}', '1', 'ATIVO', 1, 'S', 'D', 0, '{UsuarioSistemaId}'),
    -- Passivo
    ('{ClienteId}', '2', 'PASSIVO', 1, 'S', 'C', 0, '{UsuarioSistemaId}'),
    -- Receitas
    ('{ClienteId}', '3', 'RECEITAS', 1, 'S', 'C', 0, '{UsuarioSistemaId}'),
    -- Custos
    ('{ClienteId}', '4', 'CUSTOS', 1, 'S', 'D', 0, '{UsuarioSistemaId}'),
    -- Despesas
    ('{ClienteId}', '5', 'DESPESAS', 1, 'S', 'D', 0, '{UsuarioSistemaId}');

-- Dimensão Padrão: Projeto
INSERT INTO DimensaoContabil (ClienteId, Nome, CodigoPrefixo, TipoAlocacao, Obrigatoria, UsuarioCriacaoId)
VALUES ('{ClienteId}', 'Projeto', 'PROJ', 'PERCENTUAL', 0, '{UsuarioSistemaId}');

-- Dimensão Padrão: Região
INSERT INTO DimensaoContabil (ClienteId, Nome, CodigoPrefixo, TipoAlocacao, Obrigatoria, UsuarioCriacaoId)
VALUES ('{ClienteId}', 'Região', 'REG', 'PERCENTUAL', 0, '{UsuarioSistemaId}');
```

---

## 6. Observações Técnicas

### 6.1. Performance

- **Hierarquia Recursiva:** Queries de navegação hierárquica devem usar CTE recursiva (Common Table Expression) para performance:
  ```sql
  WITH HierarquiaRecursiva AS (
      SELECT Id, PlanoContaPaiId, CodigoContabil, NomeConta, Nivel, 1 AS Depth
      FROM PlanoContaContabil
      WHERE PlanoContaPaiId IS NULL AND FlExcluido = 0
      UNION ALL
      SELECT p.Id, p.PlanoContaPaiId, p.CodigoContabil, p.NomeConta, p.Nivel, h.Depth + 1
      FROM PlanoContaContabil p
      INNER JOIN HierarquiaRecursiva h ON p.PlanoContaPaiId = h.Id
      WHERE p.FlExcluido = 0 AND h.Depth < 7
  )
  SELECT * FROM HierarquiaRecursiva;
  ```

- **Cache Redis:** Estrutura de plano de contas é relativamente estática, considerar cache com invalidação ao salvar/editar.

- **Paginação:** Listagem de lançamentos contábeis DEVE usar paginação (limite 100 registros por página).

### 6.2. Multi-Tenancy

- **Row-Level Security:** EF Core Query Filter aplicado automaticamente em todas as entidades:
  ```csharp
  modelBuilder.Entity<PlanoContaContabil>()
      .HasQueryFilter(e => e.ClienteId == _currentUserService.ClienteId && !e.FlExcluido);
  ```

- **Validação de Relacionamentos:** Ao criar lançamento, validar que PlanoContaId, CentroCustoId e ProjetoId pertencem ao mesmo ClienteId.

### 6.3. Auditoria e Versionamento

- **Trigger para PlanoContaVersao:** Recomenda-se criar trigger ou interceptor EF Core para criar snapshot automaticamente ao UPDATE/DELETE.

- **Retenção de 7 Anos:** Dados de auditoria mantidos por 7 anos conforme LGPD. Implementar job de arquivamento após este período.

### 6.4. Validações Críticas

- **Partida Dobrada:** Ao criar lançamentos D-E (Débito-Crédito), validar que soma débitos = soma créditos (tolerância R$0,01).

- **Soma de Percentuais:** Ao criar alocações em dimensões ou rateio multi-nível, validar que soma = 100%.

- **Dependência Circular:** Ao mover conta na hierarquia, validar com algoritmo de detecção de grafos circulares.

---

## 7. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-14 | Architect Agent | Versão inicial completa com 14 tabelas, 45 índices, DDL SQL Server executável |

---

**FIM DO MD-RF031**

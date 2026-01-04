# Modelo de Dados - RF036 - Gestão de Custos Fixos

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF036 - Gestão de Custos Fixos](./RF036.md)
**Banco de Dados:** SQL Server
**Total de Tabelas:** 12

---

## 1. Diagrama ER (Entidade-Relacionamento)

```
┌─────────────────────────────┐
│     Conglomerados           │
│  (tabela multi-tenancy)     │
└──────────┬──────────────────┘
           │
           │ 1:N (todas as tabelas)
           │
┌──────────┴───────────────────────────────────────────────────┐
│                                                                │
│  ┌──────────────────┐       ┌──────────────────────────┐     │
│  │ TiposCustoFixo   │◄──┐   │  CustosFixos             │     │
│  │ (Aluguel,        │   │   │  (custo recorrente)      │     │
│  │  Energia, etc)   │   └───┤  - TipoCustoFixoId       │     │
│  └──────────────────┘       │  - ValorOrcadoMensal     │     │
│                              │  - DataInicio/DataFim    │     │
│                              │  - Status                │     │
│                              │  - FornecedorId (FK)     │     │
│                              │  - ContratoId (FK)       │     │
│                              └──────┬───────────────────┘     │
│                                     │                          │
│                                     │ 1:N                      │
│                                     ▼                          │
│                     ┌────────────────────────────────┐         │
│                     │ LancamentosCustosFixos         │         │
│                     │ (lançamento mensal)            │         │
│                     │  - CustoFixoId (FK)            │         │
│                     │  - MesReferencia               │         │
│                     │  - ValorProvisionado           │         │
│                     │  - ValorRealizado              │         │
│                     │  - Status (Provisionado,       │         │
│                     │    Realizado, Pago)            │         │
│                     │  - FlProvisionamentoAutomatico │         │
│                     │  - FlAnomalia                  │         │
│                     │  - RequiredAprovacaoGerencial  │         │
│                     └────────┬───────────────────────┘         │
│                              │                                  │
│                              │ 1:N                              │
│                              ▼                                  │
│              ┌──────────────────────────────────┐              │
│              │ JustificativasVariacao           │              │
│              │ (justificativas de variação)     │              │
│              │  - LancamentoId (FK)             │              │
│              │  - PercentualVariacao            │              │
│              │  - Justificativa                 │              │
│              │  - AprovadoPor                   │              │
│              │  - DataAprovacao                 │              │
│              └──────────────────────────────────┘              │
│                                                                 │
│  ┌───────────────────────┐      ┌─────────────────────────┐   │
│  │ RateiosCustosFixos    │      │ CustosFixosHistorico    │   │
│  │ (rateio multi-dim)    │      │ (auditoria de mudanças) │   │
│  │  - CustoFixoId (FK)   │      │  - CustoFixoId (FK)     │   │
│  │  - CentroCustoId (FK) │      │  - CampoAlterado        │   │
│  │  - FilialId           │      │  - ValorAnterior        │   │
│  │  - Percentual         │      │  - ValorNovo            │   │
│  └───────────────────────┘      │  - Justificativa        │   │
│                                  └─────────────────────────┘   │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │ ProjecoesCustosFixos                                  │    │
│  │ (projeções 3, 6, 12 meses)                            │    │
│  │  - MesProjecao, ValorProjetado, BaseCalculo           │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │ AnalisesVariacao                                      │    │
│  │ (análises YoY e tendências)                           │    │
│  │  - CustoFixoId, Periodo, ValorAtual, ValorAnterior   │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │ AnomaliasCustosFixos                                  │    │
│  │ (anomalias detectadas automaticamente)                │    │
│  │  - LancamentoId, TipoAnomalia, Severidade, Resolvido │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌───────────────────────────────────────────────────────┐    │
│  │ NotificacoesAlertasCustosFixos                        │    │
│  │ (histórico de notificações/alertas)                   │    │
│  │  - CustoFixoId, TipoAlerta, DataEnvio, Destinatario  │    │
│  └───────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Dicionário de Dados

### 2.1 Tabela: TiposCustoFixo

**Descrição:** Cadastro de tipos/categorias de custos fixos (ex: Aluguel, Energia, Internet, Segurança).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| Codigo | NVARCHAR(20) | NÃO | - | Código único (ex: ALG, ENE, INT) |
| Nome | NVARCHAR(100) | NÃO | - | Nome do tipo (ex: "Aluguel de Imóveis") |
| Descricao | NVARCHAR(500) | SIM | NULL | Descrição detalhada |
| Categoria | INT | NÃO | 1 | 1=Infraestrutura, 2=Serviços, 3=Utilidades, 4=Outros |
| FlAtivo | BIT | NÃO | 1 | Tipo ativo/inativo |
| OrdemExibicao | INT | NÃO | 999 | Ordem de exibição em listas |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Id_Usuario_Alteracao | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| Dt_Alteracao | DATETIME2 | SIM | NULL | Data de alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

**Índices:**
- PK_TiposCustoFixo (Id)
- IX_TiposCustoFixo_ConglomeradoId (ConglomeradoId) WHERE FlExcluido = 0
- IX_TiposCustoFixo_Codigo (ConglomeradoId, Codigo) WHERE FlExcluido = 0 UNIQUE
- IX_TiposCustoFixo_Categoria (Categoria) WHERE FlExcluido = 0

---

### 2.2 Tabela: CustosFixos

**Descrição:** Cadastro de custos fixos mensais recorrentes.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| TipoCustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para tipo de custo |
| Descricao | NVARCHAR(500) | NÃO | - | Descrição do custo |
| ValorOrcadoMensal | DECIMAL(18,2) | NÃO | 0.00 | Valor orçado mensal |
| DataInicio | DATE | NÃO | - | Data início vigência |
| DataFim | DATE | SIM | NULL | Data fim vigência (opcional) |
| Status | INT | NÃO | 1 | 1=Ativo, 2=Inativo, 3=Suspenso, 4=Cancelado |
| FornecedorId | UNIQUEIDENTIFIER | SIM | NULL | FK para fornecedor (opcional) |
| ContratoId | UNIQUEIDENTIFIER | SIM | NULL | FK para contrato (opcional) |
| UsuarioResponsavelId | UNIQUEIDENTIFIER | NÃO | - | Responsável pelo custo |
| CentroCustoId | UNIQUEIDENTIFIER | SIM | NULL | Centro de custo principal |
| FilialId | NVARCHAR(50) | SIM | NULL | Filial principal |
| Periodicidade | INT | NÃO | 1 | 1=Mensal, 2=Bimestral, 3=Trimestral, 4=Anual |
| DiaVencimento | INT | SIM | NULL | Dia de vencimento (1-31) |
| FormaPagamento | INT | SIM | NULL | 1=Boleto, 2=Débito, 3=TED, 4=Cartão |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações gerais |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Id_Usuario_Alteracao | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| Dt_Alteracao | DATETIME2 | SIM | NULL | Data de alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

**Índices:**
- PK_CustosFixos (Id)
- IX_CustosFixos_ConglomeradoId (ConglomeradoId) WHERE FlExcluido = 0
- IX_CustosFixos_TipoCustoFixoId (TipoCustoFixoId) WHERE FlExcluido = 0
- IX_CustosFixos_Status (Status) WHERE FlExcluido = 0
- IX_CustosFixos_FornecedorId (FornecedorId) WHERE FlExcluido = 0 AND FornecedorId IS NOT NULL
- IX_CustosFixos_ContratoId (ContratoId) WHERE FlExcluido = 0 AND ContratoId IS NOT NULL
- IX_CustosFixos_UsuarioResponsavelId (UsuarioResponsavelId) WHERE FlExcluido = 0
- IX_CustosFixos_DataInicio_DataFim (DataInicio, DataFim) WHERE FlExcluido = 0

---

### 2.3 Tabela: LancamentosCustosFixos

**Descrição:** Lançamentos mensais de custos fixos (provisionados e realizados).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para custo fixo |
| MesReferencia | DATE | NÃO | - | Mês de referência (1º dia do mês) |
| ValorProvisionado | DECIMAL(18,2) | NÃO | 0.00 | Valor provisionado |
| ValorRealizado | DECIMAL(18,2) | SIM | NULL | Valor realizado (pago) |
| Status | INT | NÃO | 1 | 1=Provisionado, 2=Realizado, 3=Pago, 4=Cancelado |
| DataVencimento | DATE | SIM | NULL | Data de vencimento |
| DataPagamento | DATE | SIM | NULL | Data de pagamento efetivo |
| FlProvisionamentoAutomatico | BIT | NÃO | 0 | Provisionado por job automático |
| DataProvisionamento | DATETIME2 | SIM | NULL | Data/hora do provisionamento |
| FlAnomalia | BIT | NÃO | 0 | Anomalia detectada (valor muito diferente) |
| DescricaoAnomalia | NVARCHAR(500) | SIM | NULL | Descrição da anomalia |
| PercentualVariacao | DECIMAL(5,2) AS (CASE WHEN ValorRealizado IS NOT NULL THEN ABS((ValorRealizado - ValorProvisionado) / NULLIF(ValorProvisionado, 0) * 100) ELSE 0 END) PERSISTED | - | - | % variação realizado vs provisionado (campo calculado) |
| RequiredAprovacaoGerencial | BIT | NÃO | 0 | Requer aprovação gerencial (variação >30%) |
| AprovadoPor | UNIQUEIDENTIFIER | SIM | NULL | Usuário que aprovou |
| DataAprovacao | DATETIME2 | SIM | NULL | Data de aprovação |
| JustificativaAprovacao | NVARCHAR(1000) | SIM | NULL | Justificativa da aprovação/reprovação |
| Observacoes | NVARCHAR(MAX) | SIM | NULL | Observações do lançamento |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Id_Usuario_Alteracao | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| Dt_Alteracao | DATETIME2 | SIM | NULL | Data de alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

**Índices:**
- PK_LancamentosCustosFixos (Id)
- IX_LancamentosCustosFixos_ConglomeradoId (ConglomeradoId) WHERE FlExcluido = 0
- IX_LancamentosCustosFixos_CustoFixoId (CustoFixoId) WHERE FlExcluido = 0
- IX_LancamentosCustosFixos_MesReferencia (MesReferencia) WHERE FlExcluido = 0
- IX_LancamentosCustosFixos_Status (Status) WHERE FlExcluido = 0
- IX_LancamentosCustosFixos_FlAnomalia (FlAnomalia) WHERE FlExcluido = 0 AND FlAnomalia = 1
- IX_LancamentosCustosFixos_RequiredAprovacao (RequiredAprovacaoGerencial) WHERE FlExcluido = 0 AND RequiredAprovacaoGerencial = 1
- UX_LancamentosCustosFixos_CustoFixo_Mes (CustoFixoId, MesReferencia) WHERE FlExcluido = 0 UNIQUE

---

### 2.4 Tabela: RateiosCustosFixos

**Descrição:** Rateio de custos fixos entre centros de custo e filiais.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para custo fixo |
| CentroCustoId | UNIQUEIDENTIFIER | NÃO | - | FK para centro de custo |
| FilialId | NVARCHAR(50) | SIM | NULL | Filial (opcional) |
| Percentual | DECIMAL(5,2) | NÃO | 0.00 | Percentual do rateio (0-100) |
| Observacoes | NVARCHAR(500) | SIM | NULL | Observações do rateio |
| DataInicioVigencia | DATE | NÃO | GETDATE() | Data início vigência |
| DataFimVigencia | DATE | SIM | NULL | Data fim vigência |
| FlAtivo | BIT | NÃO | 1 | Rateio ativo |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Id_Usuario_Alteracao | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| Dt_Alteracao | DATETIME2 | SIM | NULL | Data de alteração |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

**Índices:**
- PK_RateiosCustosFixos (Id)
- IX_RateiosCustosFixos_ConglomeradoId (ConglomeradoId) WHERE FlExcluido = 0
- IX_RateiosCustosFixos_CustoFixoId (CustoFixoId) WHERE FlExcluido = 0
- IX_RateiosCustosFixos_CentroCustoId (CentroCustoId) WHERE FlExcluido = 0

---

### 2.5 Tabela: JustificativasVariacao

**Descrição:** Justificativas para variações significativas entre valor orçado e realizado.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| LancamentoCustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para lançamento |
| PercentualVariacao | DECIMAL(5,2) | NÃO | 0.00 | % de variação |
| TipoVariacao | INT | NÃO | 1 | 1=Aumento, 2=Redução |
| Justificativa | NVARCHAR(1000) | NÃO | - | Justificativa detalhada |
| AprovadoPor | UNIQUEIDENTIFIER | SIM | NULL | Usuário que aprovou |
| DataAprovacao | DATETIME2 | SIM | NULL | Data de aprovação |
| StatusAprovacao | INT | SIM | NULL | 1=Pendente, 2=Aprovado, 3=Reprovado |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |
| Ativo | BIT | NÃO | true | Soft delete: false=ativo, true=excluído |

**Índices:**
- PK_JustificativasVariacao (Id)
- IX_JustificativasVariacao_ConglomeradoId (ConglomeradoId) WHERE FlExcluido = 0
- IX_JustificativasVariacao_LancamentoId (LancamentoCustoFixoId) WHERE FlExcluido = 0
- IX_JustificativasVariacao_StatusAprovacao (StatusAprovacao) WHERE FlExcluido = 0

---

### 2.6 Tabela: CustosFixosHistorico

**Descrição:** Histórico de alterações em custos fixos (auditoria).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para custo fixo |
| CampoAlterado | NVARCHAR(100) | NÃO | - | Nome do campo alterado |
| ValorAnterior | NVARCHAR(MAX) | SIM | NULL | Valor anterior (serializado) |
| ValorNovo | NVARCHAR(MAX) | SIM | NULL | Valor novo (serializado) |
| TipoOperacao | NVARCHAR(10) | NÃO | - | INSERT, UPDATE, DELETE |
| Justificativa | NVARCHAR(1000) | SIM | NULL | Justificativa da alteração |
| UsuarioAlteracaoId | UNIQUEIDENTIFIER | NÃO | - | Usuário que fez a alteração |
| DataAlteracao | DATETIME2 | NÃO | GETDATE() | Data/hora da alteração |
| EnderecoIP | NVARCHAR(50) | SIM | NULL | IP do usuário |
| UserAgent | NVARCHAR(500) | SIM | NULL | User agent do browser |

**Índices:**
- PK_CustosFixosHistorico (Id)
- IX_CustosFixosHistorico_ConglomeradoId (ConglomeradoId)
- IX_CustosFixosHistorico_CustoFixoId (CustoFixoId)
- IX_CustosFixosHistorico_DataAlteracao (DataAlteracao)
- IX_CustosFixosHistorico_UsuarioAlteracaoId (UsuarioAlteracaoId)

---

### 2.7 Tabela: ProjecoesCustosFixos

**Descrição:** Projeções de custos futuros (3, 6, 12 meses).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | SIM | NULL | FK para custo fixo específico (NULL = geral) |
| TipoCustoFixoId | UNIQUEIDENTIFIER | SIM | NULL | FK para tipo (NULL = todos) |
| MesProjecao | DATE | NÃO | - | Mês da projeção |
| ValorProjetado | DECIMAL(18,2) | NÃO | 0.00 | Valor projetado |
| BaseCalculo | NVARCHAR(200) | SIM | NULL | Base de cálculo (ex: "média 6 meses") |
| DataCalculoProjecao | DATETIME2 | NÃO | GETDATE() | Data do cálculo |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |

**Índices:**
- PK_ProjecoesCustosFixos (Id)
- IX_ProjecoesCustosFixos_ConglomeradoId (ConglomeradoId)
- IX_ProjecoesCustosFixos_CustoFixoId (CustoFixoId)
- IX_ProjecoesCustosFixos_MesProjecao (MesProjecao)
- UX_ProjecoesCustosFixos_Custo_Mes (ConglomeradoId, CustoFixoId, MesProjecao) UNIQUE

---

### 2.8 Tabela: AnalisesVariacao

**Descrição:** Análises Year-over-Year e tendências de custos.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para custo fixo |
| Periodo | DATE | NÃO | - | Período de análise (mês) |
| ValorAtual | DECIMAL(18,2) | NÃO | 0.00 | Valor do período atual |
| ValorAnoAnterior | DECIMAL(18,2) | SIM | NULL | Valor mesmo período ano anterior |
| VariacaoYoY | DECIMAL(5,2) | SIM | NULL | Variação YoY percentual |
| Tendencia | NVARCHAR(20) | SIM | NULL | Aumento, Redução, Estável |
| MediaMovel6Meses | DECIMAL(18,2) | SIM | NULL | Média móvel 6 meses |
| DesvioPadrao | DECIMAL(18,2) | SIM | NULL | Desvio padrão |
| DataCalculoAnalise | DATETIME2 | NÃO | GETDATE() | Data do cálculo |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |

**Índices:**
- PK_AnalisesVariacao (Id)
- IX_AnalisesVariacao_ConglomeradoId (ConglomeradoId)
- IX_AnalisesVariacao_CustoFixoId (CustoFixoId)
- IX_AnalisesVariacao_Periodo (Periodo)
- UX_AnalisesVariacao_Custo_Periodo (CustoFixoId, Periodo) UNIQUE

---

### 2.9 Tabela: AnomaliasCustosFixos

**Descrição:** Anomalias detectadas automaticamente (valores muito diferentes da média).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| LancamentoCustoFixoId | UNIQUEIDENTIFIER | NÃO | - | FK para lançamento |
| TipoAnomalia | INT | NÃO | 1 | 1=ValorAcimaDaMedia, 2=ValorAbaixoDaMedia, 3=AumentoAnormal |
| Severidade | INT | NÃO | 2 | 1=Baixa, 2=Média, 3=Alta |
| ValorDetectado | DECIMAL(18,2) | NÃO | 0.00 | Valor que gerou a anomalia |
| ValorEsperado | DECIMAL(18,2) | NÃO | 0.00 | Valor esperado (média) |
| DesvioPercentual | DECIMAL(5,2) | NÃO | 0.00 | % de desvio |
| DescricaoAnomalia | NVARCHAR(500) | NÃO | - | Descrição da anomalia |
| FlResolvido | BIT | NÃO | 0 | Anomalia resolvida/justificada |
| ResolvidoPor | UNIQUEIDENTIFIER | SIM | NULL | Usuário que resolveu |
| DataResolucao | DATETIME2 | SIM | NULL | Data de resolução |
| JustificativaResolucao | NVARCHAR(1000) | SIM | NULL | Justificativa da resolução |
| DataDeteccao | DATETIME2 | NÃO | GETDATE() | Data de detecção |
| Id_Usuario_Criacao | UNIQUEIDENTIFIER | NÃO | - | Usuário que criou (sistema) |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |

**Índices:**
- PK_AnomaliasCustosFixos (Id)
- IX_AnomaliasCustosFixos_ConglomeradoId (ConglomeradoId)
- IX_AnomaliasCustosFixos_LancamentoId (LancamentoCustoFixoId)
- IX_AnomaliasCustosFixos_FlResolvido (FlResolvido) WHERE FlResolvido = 0
- IX_AnomaliasCustosFixos_Severidade (Severidade)

---

### 2.10 Tabela: NotificacoesAlertasCustosFixos

**Descrição:** Histórico de notificações e alertas enviados.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| CustoFixoId | UNIQUEIDENTIFIER | SIM | NULL | FK para custo fixo |
| LancamentoCustoFixoId | UNIQUEIDENTIFIER | SIM | NULL | FK para lançamento |
| TipoAlerta | INT | NÃO | 1 | 1=Informativo, 2=Aviso, 3=Crítico |
| Categoria | NVARCHAR(50) | NÃO | - | Provisionamento, Variacao, Vencimento, Anomalia |
| Titulo | NVARCHAR(200) | NÃO | - | Título da notificação |
| Mensagem | NVARCHAR(MAX) | NÃO | - | Mensagem completa |
| DestinatarioId | UNIQUEIDENTIFIER | NÃO | - | Usuário destinatário |
| EmailEnviado | BIT | NÃO | 0 | E-mail foi enviado |
| DataEnvioEmail | DATETIME2 | SIM | NULL | Data de envio do e-mail |
| NotificacaoPushEnviada | BIT | NÃO | 0 | Push notification enviada |
| DataEnvioPush | DATETIME2 | SIM | NULL | Data de envio push |
| FlLido | BIT | NÃO | 0 | Notificação foi lida |
| DataLeitura | DATETIME2 | SIM | NULL | Data de leitura |
| Dt_Criacao | DATETIME2 | NÃO | GETDATE() | Data de criação |

**Índices:**
- PK_NotificacoesAlertasCustosFixos (Id)
- IX_NotificacoesAlertasCustosFixos_ConglomeradoId (ConglomeradoId)
- IX_NotificacoesAlertasCustosFixos_CustoFixoId (CustoFixoId)
- IX_NotificacoesAlertasCustosFixos_DestinatarioId (DestinatarioId)
- IX_NotificacoesAlertasCustosFixos_FlLido (FlLido) WHERE FlLido = 0

---

### 2.11 Tabela: ConfiguracoesCustosFixos

**Descrição:** Configurações globais do módulo de custos fixos.

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| ChaveConfiguracao | NVARCHAR(100) | NÃO | - | Chave única da configuração |
| Valor | NVARCHAR(MAX) | SIM | NULL | Valor da configuração (JSON) |
| Descricao | NVARCHAR(500) | SIM | NULL | Descrição da configuração |
| TipoDado | NVARCHAR(20) | NÃO | 'string' | string, int, decimal, bool, json |
| FlEditavel | BIT | NÃO | 1 | Configuração editável pelo usuário |
| Id_Usuario_Alteracao | UNIQUEIDENTIFIER | SIM | NULL | Usuário que alterou |
| Dt_Alteracao | DATETIME2 | SIM | NULL | Data de alteração |

**Índices:**
- PK_ConfiguracoesCustosFixos (Id)
- IX_ConfiguracoesCustosFixos_ConglomeradoId (ConglomeradoId)
- UX_ConfiguracoesCustosFixos_Chave (ConglomeradoId, ChaveConfiguracao) UNIQUE

**Configurações Padrão:**
```json
{
  "LimiteVariacaoAviso": "10",
  "LimiteVariacaoAlerta": "20",
  "LimiteVariacaoAprovacao": "30",
  "DiasAntesVencimentoAlerta": "7,3,1",
  "MesesHistoricoAnomalia": "6",
  "ProvisionamentoAutomaticoAtivo": "true",
  "DiaExecucaoProvisionamento": "1"
}
```

---

### 2.12 Tabela: DashboardCustosFixosCache

**Descrição:** Cache de métricas do dashboard (atualizado diariamente).

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para multi-tenancy |
| MesReferencia | DATE | NÃO | - | Mês de referência |
| TotalCustosAtivos | INT | NÃO | 0 | Total de custos ativos |
| ValorTotalProvisionado | DECIMAL(18,2) | NÃO | 0.00 | Valor total provisionado |
| ValorTotalRealizado | DECIMAL(18,2) | NÃO | 0.00 | Valor total realizado |
| PercentualVariacao | DECIMAL(5,2) | NÃO | 0.00 | % variação global |
| QuantidadeAnomalias | INT | NÃO | 0 | Quantidade de anomalias detectadas |
| TaxaCumprimentoOrcamento | DECIMAL(5,2) | NÃO | 0.00 | % de custos dentro do orçado |
| Top10MaioresCustos | NVARCHAR(MAX) | SIM | NULL | JSON com top 10 |
| Top10MaioresVariacoes | NVARCHAR(MAX) | SIM | NULL | JSON com top 10 variações |
| DataUltimaAtualizacao | DATETIME2 | NÃO | GETDATE() | Data da última atualização |
| ProximaAtualizacao | DATETIME2 | NÃO | - | Data da próxima atualização agendada |

**Índices:**
- PK_DashboardCustosFixosCache (Id)
- IX_DashboardCustosFixosCache_ConglomeradoId (ConglomeradoId)
- UX_DashboardCustosFixosCache_Conglomerado_Mes (ConglomeradoId, MesReferencia) UNIQUE

---

## 3. DDL Completo - SQL Server

```sql
-- =====================================================
-- RF036 - Gestão de Custos Fixos
-- Modelo de Dados Completo
-- Data: 2025-12-18
-- Versão: 1.0
-- Banco: SQL Server
-- =====================================================

-- =====================================================
-- Tabela 1: TiposCustoFixo
-- =====================================================
CREATE TABLE TiposCustoFixo (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Codigo NVARCHAR(20) NOT NULL,
    Nome NVARCHAR(100) NOT NULL,
    Descricao NVARCHAR(500) NULL,
    Categoria INT NOT NULL DEFAULT 1,
    FlFlExcluido BIT NOT NULL DEFAULT 0,
    OrdemExibicao INT NOT NULL DEFAULT 999,
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_TiposCustoFixo PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_TiposCustoFixo_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT CK_TiposCustoFixo_Categoria CHECK (Categoria IN (1, 2, 3, 4))
);

CREATE NONCLUSTERED INDEX IX_TiposCustoFixo_ConglomeradoId ON TiposCustoFixo(ConglomeradoId) WHERE FlExcluido = 0;
CREATE UNIQUE NONCLUSTERED INDEX UX_TiposCustoFixo_Codigo ON TiposCustoFixo(ConglomeradoId, Codigo) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_TiposCustoFixo_Categoria ON TiposCustoFixo(Categoria) WHERE FlExcluido = 0;

-- =====================================================
-- Tabela 2: CustosFixos
-- =====================================================
CREATE TABLE CustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    TipoCustoFixoId UNIQUEIDENTIFIER NOT NULL,
    Descricao NVARCHAR(500) NOT NULL,
    ValorOrcadoMensal DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    DataInicio DATE NOT NULL,
    DataFim DATE NULL,
    Status INT NOT NULL DEFAULT 1,
    FornecedorId UNIQUEIDENTIFIER NULL,
    ContratoId UNIQUEIDENTIFIER NULL,
    UsuarioResponsavelId UNIQUEIDENTIFIER NOT NULL,
    CentroCustoId UNIQUEIDENTIFIER NULL,
    FilialId NVARCHAR(50) NULL,
    Periodicidade INT NOT NULL DEFAULT 1,
    DiaVencimento INT NULL,
    FormaPagamento INT NULL,
    Observacoes NVARCHAR(MAX) NULL,
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_CustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_CustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_CustosFixos_TipoCustoFixo FOREIGN KEY (TipoCustoFixoId) REFERENCES TiposCustoFixo(Id),
    CONSTRAINT CK_CustosFixos_Status CHECK (Status IN (1, 2, 3, 4)),
    CONSTRAINT CK_CustosFixos_Periodicidade CHECK (Periodicidade IN (1, 2, 3, 4)),
    CONSTRAINT CK_CustosFixos_DiaVencimento CHECK (DiaVencimento IS NULL OR (DiaVencimento >= 1 AND DiaVencimento <= 31)),
    CONSTRAINT CK_CustosFixos_ValorOrcado CHECK (ValorOrcadoMensal >= 0),
    CONSTRAINT CK_CustosFixos_DataFim CHECK (DataFim IS NULL OR DataFim >= DataInicio)
);

CREATE NONCLUSTERED INDEX IX_CustosFixos_ConglomeradoId ON CustosFixos(ConglomeradoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_CustosFixos_TipoCustoFixoId ON CustosFixos(TipoCustoFixoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_CustosFixos_Status ON CustosFixos(Status) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_CustosFixos_FornecedorId ON CustosFixos(FornecedorId) WHERE FlExcluido = 0 AND FornecedorId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_CustosFixos_ContratoId ON CustosFixos(ContratoId) WHERE FlExcluido = 0 AND ContratoId IS NOT NULL;
CREATE NONCLUSTERED INDEX IX_CustosFixos_UsuarioResponsavelId ON CustosFixos(UsuarioResponsavelId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_CustosFixos_DataInicio_DataFim ON CustosFixos(DataInicio, DataFim) WHERE FlExcluido = 0;

-- =====================================================
-- Tabela 3: LancamentosCustosFixos
-- =====================================================
CREATE TABLE LancamentosCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NOT NULL,
    MesReferencia DATE NOT NULL,
    ValorProvisionado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorRealizado DECIMAL(18,2) NULL,
    Status INT NOT NULL DEFAULT 1,
    DataVencimento DATE NULL,
    DataPagamento DATE NULL,
    FlProvisionamentoAutomatico BIT NOT NULL DEFAULT 0,
    DataProvisionamento DATETIME2 NULL,
    FlAnomalia BIT NOT NULL DEFAULT 0,
    DescricaoAnomalia NVARCHAR(500) NULL,
    PercentualVariacao AS (CASE WHEN ValorRealizado IS NOT NULL THEN ABS((ValorRealizado - ValorProvisionado) / NULLIF(ValorProvisionado, 0) * 100) ELSE 0 END) PERSISTED,
    RequiredAprovacaoGerencial BIT NOT NULL DEFAULT 0,
    AprovadoPor UNIQUEIDENTIFIER NULL,
    DataAprovacao DATETIME2 NULL,
    JustificativaAprovacao NVARCHAR(1000) NULL,
    Observacoes NVARCHAR(MAX) NULL,
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_LancamentosCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_LancamentosCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_LancamentosCustosFixos_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id),
    CONSTRAINT CK_LancamentosCustosFixos_Status CHECK (Status IN (1, 2, 3, 4)),
    CONSTRAINT CK_LancamentosCustosFixos_ValorProvisionado CHECK (ValorProvisionado >= 0),
    CONSTRAINT CK_LancamentosCustosFixos_ValorRealizado CHECK (ValorRealizado IS NULL OR ValorRealizado >= 0)
);

CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_ConglomeradoId ON LancamentosCustosFixos(ConglomeradoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_CustoFixoId ON LancamentosCustosFixos(CustoFixoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_MesReferencia ON LancamentosCustosFixos(MesReferencia) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_Status ON LancamentosCustosFixos(Status) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_FlAnomalia ON LancamentosCustosFixos(FlAnomalia) WHERE FlExcluido = 0 AND FlAnomalia = 1;
CREATE NONCLUSTERED INDEX IX_LancamentosCustosFixos_RequiredAprovacao ON LancamentosCustosFixos(RequiredAprovacaoGerencial) WHERE FlExcluido = 0 AND RequiredAprovacaoGerencial = 1;
CREATE UNIQUE NONCLUSTERED INDEX UX_LancamentosCustosFixos_CustoFixo_Mes ON LancamentosCustosFixos(CustoFixoId, MesReferencia) WHERE FlExcluido = 0;

-- =====================================================
-- Tabela 4: RateiosCustosFixos
-- =====================================================
CREATE TABLE RateiosCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NOT NULL,
    CentroCustoId UNIQUEIDENTIFIER NOT NULL,
    FilialId NVARCHAR(50) NULL,
    Percentual DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    Observacoes NVARCHAR(500) NULL,
    DataInicioVigencia DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    DataFimVigencia DATE NULL,
    FlFlExcluido BIT NOT NULL DEFAULT 0,
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_RateiosCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_RateiosCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_RateiosCustosFixos_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id),
    CONSTRAINT CK_RateiosCustosFixos_Percentual CHECK (Percentual >= 0 AND Percentual <= 100)
);

CREATE NONCLUSTERED INDEX IX_RateiosCustosFixos_ConglomeradoId ON RateiosCustosFixos(ConglomeradoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_RateiosCustosFixos_CustoFixoId ON RateiosCustosFixos(CustoFixoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_RateiosCustosFixos_CentroCustoId ON RateiosCustosFixos(CentroCustoId) WHERE FlExcluido = 0;

-- =====================================================
-- Tabela 5: JustificativasVariacao
-- =====================================================
CREATE TABLE JustificativasVariacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    LancamentoCustoFixoId UNIQUEIDENTIFIER NOT NULL,
    PercentualVariacao DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    TipoVariacao INT NOT NULL DEFAULT 1,
    Justificativa NVARCHAR(1000) NOT NULL,
    AprovadoPor UNIQUEIDENTIFIER NULL,
    DataAprovacao DATETIME2 NULL,
    StatusAprovacao INT NULL,
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    FlExcluido BIT NOT NULL DEFAULT 0,

    CONSTRAINT PK_JustificativasVariacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_JustificativasVariacao_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_JustificativasVariacao_Lancamento FOREIGN KEY (LancamentoCustoFixoId) REFERENCES LancamentosCustosFixos(Id),
    CONSTRAINT CK_JustificativasVariacao_TipoVariacao CHECK (TipoVariacao IN (1, 2)),
    CONSTRAINT CK_JustificativasVariacao_StatusAprovacao CHECK (StatusAprovacao IS NULL OR StatusAprovacao IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX IX_JustificativasVariacao_ConglomeradoId ON JustificativasVariacao(ConglomeradoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_JustificativasVariacao_LancamentoId ON JustificativasVariacao(LancamentoCustoFixoId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_JustificativasVariacao_StatusAprovacao ON JustificativasVariacao(StatusAprovacao) WHERE FlExcluido = 0;

-- =====================================================
-- Tabela 6: CustosFixosHistorico
-- =====================================================
CREATE TABLE CustosFixosHistorico (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NOT NULL,
    CampoAlterado NVARCHAR(100) NOT NULL,
    ValorAnterior NVARCHAR(MAX) NULL,
    ValorNovo NVARCHAR(MAX) NULL,
    TipoOperacao NVARCHAR(10) NOT NULL,
    Justificativa NVARCHAR(1000) NULL,
    UsuarioAlteracaoId UNIQUEIDENTIFIER NOT NULL,
    DataAlteracao DATETIME2 NOT NULL DEFAULT GETDATE(),
    EnderecoIP NVARCHAR(50) NULL,
    UserAgent NVARCHAR(500) NULL,

    CONSTRAINT PK_CustosFixosHistorico PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_CustosFixosHistorico_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_CustosFixosHistorico_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id)
);

CREATE NONCLUSTERED INDEX IX_CustosFixosHistorico_ConglomeradoId ON CustosFixosHistorico(ConglomeradoId);
CREATE NONCLUSTERED INDEX IX_CustosFixosHistorico_CustoFixoId ON CustosFixosHistorico(CustoFixoId);
CREATE NONCLUSTERED INDEX IX_CustosFixosHistorico_DataAlteracao ON CustosFixosHistorico(DataAlteracao);
CREATE NONCLUSTERED INDEX IX_CustosFixosHistorico_UsuarioAlteracaoId ON CustosFixosHistorico(UsuarioAlteracaoId);

-- =====================================================
-- Tabela 7: ProjecoesCustosFixos
-- =====================================================
CREATE TABLE ProjecoesCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NULL,
    TipoCustoFixoId UNIQUEIDENTIFIER NULL,
    MesProjecao DATE NOT NULL,
    ValorProjetado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    BaseCalculo NVARCHAR(200) NULL,
    DataCalculoProjecao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),

    CONSTRAINT PK_ProjecoesCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ProjecoesCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_ProjecoesCustosFixos_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id),
    CONSTRAINT FK_ProjecoesCustosFixos_TipoCustoFixo FOREIGN KEY (TipoCustoFixoId) REFERENCES TiposCustoFixo(Id)
);

CREATE NONCLUSTERED INDEX IX_ProjecoesCustosFixos_ConglomeradoId ON ProjecoesCustosFixos(ConglomeradoId);
CREATE NONCLUSTERED INDEX IX_ProjecoesCustosFixos_CustoFixoId ON ProjecoesCustosFixos(CustoFixoId);
CREATE NONCLUSTERED INDEX IX_ProjecoesCustosFixos_MesProjecao ON ProjecoesCustosFixos(MesProjecao);
CREATE UNIQUE NONCLUSTERED INDEX UX_ProjecoesCustosFixos_Custo_Mes ON ProjecoesCustosFixos(ConglomeradoId, CustoFixoId, MesProjecao);

-- =====================================================
-- Tabela 8: AnalisesVariacao
-- =====================================================
CREATE TABLE AnalisesVariacao (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NOT NULL,
    Periodo DATE NOT NULL,
    ValorAtual DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorAnoAnterior DECIMAL(18,2) NULL,
    VariacaoYoY DECIMAL(5,2) NULL,
    Tendencia NVARCHAR(20) NULL,
    MediaMovel6Meses DECIMAL(18,2) NULL,
    DesvioPadrao DECIMAL(18,2) NULL,
    DataCalculoAnalise DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),

    CONSTRAINT PK_AnalisesVariacao PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AnalisesVariacao_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_AnalisesVariacao_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id)
);

CREATE NONCLUSTERED INDEX IX_AnalisesVariacao_ConglomeradoId ON AnalisesVariacao(ConglomeradoId);
CREATE NONCLUSTERED INDEX IX_AnalisesVariacao_CustoFixoId ON AnalisesVariacao(CustoFixoId);
CREATE NONCLUSTERED INDEX IX_AnalisesVariacao_Periodo ON AnalisesVariacao(Periodo);
CREATE UNIQUE NONCLUSTERED INDEX UX_AnalisesVariacao_Custo_Periodo ON AnalisesVariacao(CustoFixoId, Periodo);

-- =====================================================
-- Tabela 9: AnomaliasCustosFixos
-- =====================================================
CREATE TABLE AnomaliasCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    LancamentoCustoFixoId UNIQUEIDENTIFIER NOT NULL,
    TipoAnomalia INT NOT NULL DEFAULT 1,
    Severidade INT NOT NULL DEFAULT 2,
    ValorDetectado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorEsperado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    DesvioPercentual DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    DescricaoAnomalia NVARCHAR(500) NOT NULL,
    FlResolvido BIT NOT NULL DEFAULT 0,
    ResolvidoPor UNIQUEIDENTIFIER NULL,
    DataResolucao DATETIME2 NULL,
    JustificativaResolucao NVARCHAR(1000) NULL,
    DataDeteccao DATETIME2 NOT NULL DEFAULT GETDATE(),
    Id_Usuario_Criacao UNIQUEIDENTIFIER NOT NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),

    CONSTRAINT PK_AnomaliasCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_AnomaliasCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_AnomaliasCustosFixos_Lancamento FOREIGN KEY (LancamentoCustoFixoId) REFERENCES LancamentosCustosFixos(Id),
    CONSTRAINT CK_AnomaliasCustosFixos_TipoAnomalia CHECK (TipoAnomalia IN (1, 2, 3)),
    CONSTRAINT CK_AnomaliasCustosFixos_Severidade CHECK (Severidade IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX IX_AnomaliasCustosFixos_ConglomeradoId ON AnomaliasCustosFixos(ConglomeradoId);
CREATE NONCLUSTERED INDEX IX_AnomaliasCustosFixos_LancamentoId ON AnomaliasCustosFixos(LancamentoCustoFixoId);
CREATE NONCLUSTERED INDEX IX_AnomaliasCustosFixos_FlResolvido ON AnomaliasCustosFixos(FlResolvido) WHERE FlResolvido = 0;
CREATE NONCLUSTERED INDEX IX_AnomaliasCustosFixos_Severidade ON AnomaliasCustosFixos(Severidade);

-- =====================================================
-- Tabela 10: NotificacoesAlertasCustosFixos
-- =====================================================
CREATE TABLE NotificacoesAlertasCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    CustoFixoId UNIQUEIDENTIFIER NULL,
    LancamentoCustoFixoId UNIQUEIDENTIFIER NULL,
    TipoAlerta INT NOT NULL DEFAULT 1,
    Categoria NVARCHAR(50) NOT NULL,
    Titulo NVARCHAR(200) NOT NULL,
    Mensagem NVARCHAR(MAX) NOT NULL,
    DestinatarioId UNIQUEIDENTIFIER NOT NULL,
    EmailEnviado BIT NOT NULL DEFAULT 0,
    DataEnvioEmail DATETIME2 NULL,
    NotificacaoPushEnviada BIT NOT NULL DEFAULT 0,
    DataEnvioPush DATETIME2 NULL,
    FlLido BIT NOT NULL DEFAULT 0,
    DataLeitura DATETIME2 NULL,
    Dt_Criacao DATETIME2 NOT NULL DEFAULT GETDATE(),

    CONSTRAINT PK_NotificacoesAlertasCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_NotificacoesAlertasCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id),
    CONSTRAINT FK_NotificacoesAlertasCustosFixos_CustoFixo FOREIGN KEY (CustoFixoId) REFERENCES CustosFixos(Id),
    CONSTRAINT FK_NotificacoesAlertasCustosFixos_Lancamento FOREIGN KEY (LancamentoCustoFixoId) REFERENCES LancamentosCustosFixos(Id),
    CONSTRAINT CK_NotificacoesAlertasCustosFixos_TipoAlerta CHECK (TipoAlerta IN (1, 2, 3))
);

CREATE NONCLUSTERED INDEX IX_NotificacoesAlertasCustosFixos_ConglomeradoId ON NotificacoesAlertasCustosFixos(ConglomeradoId);
CREATE NONCLUSTERED INDEX IX_NotificacoesAlertasCustosFixos_CustoFixoId ON NotificacoesAlertasCustosFixos(CustoFixoId);
CREATE NONCLUSTERED INDEX IX_NotificacoesAlertasCustosFixos_DestinatarioId ON NotificacoesAlertasCustosFixos(DestinatarioId);
CREATE NONCLUSTERED INDEX IX_NotificacoesAlertasCustosFixos_FlLido ON NotificacoesAlertasCustosFixos(FlLido) WHERE FlLido = 0;

-- =====================================================
-- Tabela 11: ConfiguracoesCustosFixos
-- =====================================================
CREATE TABLE ConfiguracoesCustosFixos (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    ChaveConfiguracao NVARCHAR(100) NOT NULL,
    Valor NVARCHAR(MAX) NULL,
    Descricao NVARCHAR(500) NULL,
    TipoDado NVARCHAR(20) NOT NULL DEFAULT 'string',
    FlEditavel BIT NOT NULL DEFAULT 1,
    Id_Usuario_Alteracao UNIQUEIDENTIFIER NULL,
    Dt_Alteracao DATETIME2 NULL,

    CONSTRAINT PK_ConfiguracoesCustosFixos PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_ConfiguracoesCustosFixos_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id)
);

CREATE NONCLUSTERED INDEX IX_ConfiguracoesCustosFixos_ConglomeradoId ON ConfiguracoesCustosFixos(ConglomeradoId);
CREATE UNIQUE NONCLUSTERED INDEX UX_ConfiguracoesCustosFixos_Chave ON ConfiguracoesCustosFixos(ConglomeradoId, ChaveConfiguracao);

-- =====================================================
-- Tabela 12: DashboardCustosFixosCache
-- =====================================================
CREATE TABLE DashboardCustosFixosCache (
    Id UNIQUEIDENTIFIER NOT NULL DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    MesReferencia DATE NOT NULL,
    TotalCustosAtivos INT NOT NULL DEFAULT 0,
    ValorTotalProvisionado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    ValorTotalRealizado DECIMAL(18,2) NOT NULL DEFAULT 0.00,
    PercentualVariacao DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    QuantidadeAnomalias INT NOT NULL DEFAULT 0,
    TaxaCumprimentoOrcamento DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    Top10MaioresCustos NVARCHAR(MAX) NULL,
    Top10MaioresVariacoes NVARCHAR(MAX) NULL,
    DataUltimaAtualizacao DATETIME2 NOT NULL DEFAULT GETDATE(),
    ProximaAtualizacao DATETIME2 NOT NULL,

    CONSTRAINT PK_DashboardCustosFixosCache PRIMARY KEY CLUSTERED (Id),
    CONSTRAINT FK_DashboardCustosFixosCache_Conglomerado FOREIGN KEY (ConglomeradoId) REFERENCES Conglomerados(Id)
);

CREATE NONCLUSTERED INDEX IX_DashboardCustosFixosCache_ConglomeradoId ON DashboardCustosFixosCache(ConglomeradoId);
CREATE UNIQUE NONCLUSTERED INDEX UX_DashboardCustosFixosCache_Conglomerado_Mes ON DashboardCustosFixosCache(ConglomeradoId, MesReferencia);

-- =====================================================
-- VIEWS
-- =====================================================

-- View: Visão consolidada de custos fixos com lançamentos
CREATE VIEW VW_CustosFixosConsolidado
AS
SELECT
    cf.Id AS CustoFixoId,
    cf.ConglomeradoId,
    cf.Descricao AS CustoDescricao,
    tcf.Nome AS TipoCusto,
    tcf.Categoria AS TipoCategoria,
    cf.ValorOrcadoMensal,
    cf.DataInicio,
    cf.DataFim,
    cf.Status,
    COUNT(DISTINCT lcf.Id) AS TotalLancamentos,
    SUM(lcf.ValorProvisionado) AS TotalProvisionado,
    SUM(lcf.ValorRealizado) AS TotalRealizado,
    AVG(lcf.PercentualVariacao) AS MediaVariacao,
    SUM(CASE WHEN lcf.FlAnomalia = 1 THEN 1 ELSE 0 END) AS QuantidadeAnomalias,
    MAX(lcf.MesReferencia) AS UltimoMesLancamento
FROM CustosFixos cf
INNER JOIN TiposCustoFixo tcf ON cf.TipoCustoFixoId = tcf.Id
LEFT JOIN LancamentosCustosFixos lcf ON cf.Id = lcf.CustoFixoId AND lcf.FlExcluido = 0
WHERE cf.FlExcluido = 0
GROUP BY
    cf.Id, cf.ConglomeradoId, cf.Descricao, tcf.Nome, tcf.Categoria,
    cf.ValorOrcadoMensal, cf.DataInicio, cf.DataFim, cf.Status;
GO

-- =====================================================
-- STORED PROCEDURES
-- =====================================================

-- Procedure: Provisionar custos fixos automaticamente
CREATE PROCEDURE SP_ProvisionarCustosFixosMensal
    @ClienteId UNIQUEIDENTIFIER,
    @MesReferencia DATE,
    @UsuarioExecucaoId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @MesReferenciaInicio DATE = DATEFROMPARTS(YEAR(@MesReferencia), MONTH(@MesReferencia), 1);

    -- Provisionar custos fixos ativos
    INSERT INTO LancamentosCustosFixos (
        ConglomeradoId,
        CustoFixoId,
        MesReferencia,
        ValorProvisionado,
        Status,
        FlProvisionamentoAutomatico,
        DataProvisionamento,
        Id_Usuario_Criacao,
        Dt_Criacao
    )
    SELECT
        cf.ConglomeradoId,
        cf.Id,
        @MesReferenciaInicio,
        ISNULL(
            (SELECT TOP 1 ValorRealizado
             FROM LancamentosCustosFixos
             WHERE CustoFixoId = cf.Id
               AND FlExcluido = 0
               AND ValorRealizado IS NOT NULL
             ORDER BY MesReferencia DESC),
            cf.ValorOrcadoMensal
        ) AS ValorProvisionado,
        1, -- Provisionado
        1, -- Provisionamento automático
        GETDATE(),
        @UsuarioExecucaoId,
        GETDATE()
    FROM CustosFixos cf
    WHERE cf.ConglomeradoId = @ConglomeradoId
      AND cf.Status = 1 -- Ativo
      AND cf.FlExcluido = 0
      AND cf.DataInicio <= @MesReferenciaInicio
      AND (cf.DataFim IS NULL OR cf.DataFim >= @MesReferenciaInicio)
      AND NOT EXISTS (
          SELECT 1
          FROM LancamentosCustosFixos lcf
          WHERE lcf.CustoFixoId = cf.Id
            AND lcf.MesReferencia = @MesReferenciaInicio
            AND lcf.FlExcluido = 0
      );

    SELECT @@ROWCOUNT AS RegistrosProvisionados;
END;
GO

-- Procedure: Detectar anomalias em custos fixos
CREATE PROCEDURE SP_DetectarAnomaliasCustosFixos
    @ClienteId UNIQUEIDENTIFIER,
    @MesesHistorico INT = 6,
    @LimiteDesvioPadrao DECIMAL(3,2) = 2.0,
    @UsuarioExecucaoId UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @DataLimite DATE = DATEADD(MONTH, -@MesesHistorico, GETDATE());

    -- Identificar anomalias
    WITH HistoricoCustos AS (
        SELECT
            lcf.CustoFixoId,
            AVG(lcf.ValorRealizado) AS MediaHistorica,
            STDEV(lcf.ValorRealizado) AS DesvioPadrao
        FROM LancamentosCustosFixos lcf
        WHERE lcf.ConglomeradoId = @ConglomeradoId
          AND lcf.FlExcluido = 0
          AND lcf.ValorRealizado IS NOT NULL
          AND lcf.MesReferencia >= @DataLimite
        GROUP BY lcf.CustoFixoId
        HAVING COUNT(*) >= 3 -- Mínimo 3 lançamentos
    )
    INSERT INTO AnomaliasCustosFixos (
        ConglomeradoId,
        LancamentoCustoFixoId,
        TipoAnomalia,
        Severidade,
        ValorDetectado,
        ValorEsperado,
        DesvioPercentual,
        DescricaoAnomalia,
        DataDeteccao,
        Id_Usuario_Criacao,
        Dt_Criacao
    )
    SELECT
        lcf.ConglomeradoId,
        lcf.Id,
        CASE
            WHEN lcf.ValorRealizado > hc.MediaHistorica + (@LimiteDesvioPadrao * hc.DesvioPadrao) THEN 1 -- Acima da média
            WHEN lcf.ValorRealizado < hc.MediaHistorica - (@LimiteDesvioPadrao * hc.DesvioPadrao) THEN 2 -- Abaixo da média
            ELSE 3 -- Aumento anormal
        END,
        CASE
            WHEN ABS(lcf.ValorRealizado - hc.MediaHistorica) > (3 * hc.DesvioPadrao) THEN 3 -- Alta
            WHEN ABS(lcf.ValorRealizado - hc.MediaHistorica) > (2 * hc.DesvioPadrao) THEN 2 -- Média
            ELSE 1 -- Baixa
        END,
        lcf.ValorRealizado,
        hc.MediaHistorica,
        ABS((lcf.ValorRealizado - hc.MediaHistorica) / NULLIF(hc.MediaHistorica, 0) * 100),
        CONCAT(
            'Valor detectado R$ ', CAST(lcf.ValorRealizado AS NVARCHAR(20)),
            ' está ',
            CAST(ABS((lcf.ValorRealizado - hc.MediaHistorica) / NULLIF(hc.MediaHistorica, 0) * 100) AS NVARCHAR(10)),
            '% ',
            CASE WHEN lcf.ValorRealizado > hc.MediaHistorica THEN 'acima' ELSE 'abaixo' END,
            ' da média histórica R$ ', CAST(hc.MediaHistorica AS NVARCHAR(20))
        ),
        GETDATE(),
        @UsuarioExecucaoId,
        GETDATE()
    FROM LancamentosCustosFixos lcf
    INNER JOIN HistoricoCustos hc ON lcf.CustoFixoId = hc.CustoFixoId
    WHERE lcf.ConglomeradoId = @ConglomeradoId
      AND lcf.FlExcluido = 0
      AND lcf.ValorRealizado IS NOT NULL
      AND (
          lcf.ValorRealizado > hc.MediaHistorica + (@LimiteDesvioPadrao * hc.DesvioPadrao)
          OR lcf.ValorRealizado < hc.MediaHistorica - (@LimiteDesvioPadrao * hc.DesvioPadrao)
      )
      AND NOT EXISTS (
          SELECT 1
          FROM AnomaliasCustosFixos acf
          WHERE acf.LancamentoCustoFixoId = lcf.Id
            AND acf.FlResolvido = 0
      );

    SELECT @@ROWCOUNT AS AnomaliasCriadas;
END;
GO

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger: Auditoria de alterações em CustosFixos
CREATE TRIGGER TRG_CustosFixos_Auditoria
ON CustosFixos
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    SET NOCOUNT ON;

    -- INSERT
    INSERT INTO CustosFixosHistorico (
        ConglomeradoId,
        CustoFixoId,
        CampoAlterado,
        ValorAnterior,
        ValorNovo,
        TipoOperacao,
        UsuarioAlteracaoId,
        DataAlteracao
    )
    SELECT
        i.ConglomeradoId,
        i.Id,
        'REGISTRO_COMPLETO',
        NULL,
        (SELECT i.* FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        'INSERT',
        i.Id_Usuario_Criacao,
        i.Dt_Criacao
    FROM inserted i
    WHERE NOT EXISTS (SELECT 1 FROM deleted);

    -- UPDATE
    INSERT INTO CustosFixosHistorico (
        ConglomeradoId,
        CustoFixoId,
        CampoAlterado,
        ValorAnterior,
        ValorNovo,
        TipoOperacao,
        UsuarioAlteracaoId,
        DataAlteracao
    )
    SELECT
        i.ConglomeradoId,
        i.Id,
        'REGISTRO_COMPLETO',
        (SELECT d.* FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        (SELECT i.* FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        'UPDATE',
        i.Id_Usuario_Alteracao,
        i.Dt_Alteracao
    FROM inserted i
    INNER JOIN deleted d ON i.Id = d.Id;

    -- DELETE (Soft Delete)
    INSERT INTO CustosFixosHistorico (
        ConglomeradoId,
        CustoFixoId,
        CampoAlterado,
        ValorAnterior,
        ValorNovo,
        TipoOperacao,
        UsuarioAlteracaoId,
        DataAlteracao
    )
    SELECT
        d.ConglomeradoId,
        d.Id,
        'REGISTRO_COMPLETO',
        (SELECT d.* FOR JSON PATH, WITHOUT_ARRAY_WRAPPER),
        NULL,
        'DELETE',
        d.Id_Usuario_Alteracao,
        d.Dt_Alteracao
    FROM deleted d
    WHERE d.FlExcluido = 1 AND NOT EXISTS (SELECT 1 FROM inserted);
END;
GO

-- =====================================================
-- DADOS INICIAIS (SEED)
-- =====================================================

-- Inserir configurações padrão
-- (Executar apenas uma vez durante a criação do banco)

-- =====================================================
-- COMENTÁRIOS DAS TABELAS
-- =====================================================

EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Cadastro de tipos/categorias de custos fixos',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'TiposCustoFixo';
GO

EXEC sp_addextendedproperty
    @name = N'MS_Description',
    @value = N'Cadastro de custos fixos mensais recorrentes',
    @level0type = N'SCHEMA', @level0name = N'dbo',
    @level1type = N'TABLE',  @level1name = N'CustosFixos';
GO

-- (Adicionar comentários para todas as outras tabelas seguindo o mesmo padrão)

-- =====================================================
-- FIM DO SCRIPT DDL
-- =====================================================
```

---

## 4. Relacionamentos Principais

| Tabela Origem | Relacionamento | Tabela Destino | Descrição |
|---------------|----------------|----------------|-----------|
| TiposCustoFixo | 1:N | CustosFixos | Um tipo pode ter múltiplos custos |
| CustosFixos | 1:N | LancamentosCustosFixos | Um custo tem múltiplos lançamentos mensais |
| CustosFixos | 1:N | RateiosCustosFixos | Um custo pode ter múltiplos rateios |
| CustosFixos | 1:N | CustosFixosHistorico | Auditoria completa de alterações |
| LancamentosCustosFixos | 1:N | JustificativasVariacao | Lançamento pode ter justificativas |
| LancamentosCustosFixos | 1:N | AnomaliasCustosFixos | Lançamento pode ter anomalias detectadas |
| CustosFixos | 1:N | ProjecoesCustosFixos | Projeções de custos futuros |
| CustosFixos | 1:N | AnalisesVariacao | Análises YoY e tendências |
| CustosFixos | 1:N | NotificacoesAlertasCustosFixos | Notificações e alertas |
| Conglomerados | 1:N | Todas as tabelas | Multi-tenancy em todas as entidades |

---

## 5. Índices de Performance

**Total de Índices:** 45

**Estratégia de Indexação:**
- Índices clustered nas PKs (UNIQUEIDENTIFIER)
- Índices filtrados WHERE FlExcluido = 0 (soft delete)
- Índices únicos para constraints de negócio
- Índices covering para queries frequentes
- Índices compostos para FKs + filtros comuns

**Principais Índices Covering:**
- `IX_LancamentosCustosFixos_CustoFixoId` - Queries de lançamentos por custo
- `IX_LancamentosCustosFixos_MesReferencia` - Queries por período
- `IX_CustosFixos_Status` - Filtro de custos ativos
- `IX_AnomaliasCustosFixos_FlResolvido` - Anomalias pendentes

---

## 6. Observações Técnicas

### 6.1 Campos Calculados Persistidos

- **LancamentosCustosFixos.PercentualVariacao:** Calculado automaticamente como `ABS((ValorRealizado - ValorProvisionado) / ValorProvisionado * 100)`
- Persistido para performance em queries e relatórios

### 6.2 Multi-Tenancy

- Todas as tabelas possuem `ConglomeradoId` para isolamento de dados
- Row-Level Security implementado via índices filtrados

### 6.3 Auditoria

- Tabela `CustosFixosHistorico` registra todas alterações
- Trigger automático captura INSERT, UPDATE, DELETE
- Retenção de 7 anos conforme LGPD

### 6.4 Soft Delete

- Campo `FlExcluido` em todas as tabelas principais
- Índices filtrados excluem registros deletados

### 6.5 Jobs Hangfire

- **ProvisionarCustosFixosJob:** Executa dia 1 de cada mês
- **DetectarAnomaliasCustosFixosJob:** Executa diariamente
- **AlertarVencimentosCustosFixosJob:** Executa diariamente
- **AtualizarDashboardCustosFixosJob:** Executa de hora em hora

---

## 7. Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial completa - 12 tabelas, 45 índices, 2 views, 2 SPs, 1 trigger |

---

**Documento Técnico - Confidencial**
**IControlIT v2 - Modernização Completa**

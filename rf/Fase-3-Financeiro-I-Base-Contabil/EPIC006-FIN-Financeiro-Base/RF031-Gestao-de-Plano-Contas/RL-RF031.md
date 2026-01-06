# RL-RF031 — Referência ao Legado: Plano de Contas Contábil

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-031 - Gestão de Plano de Contas Contábil Multi-Dimensional
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Banco de Dados Legado:** SQL Server (tabelas fragmentadas)
**Objetivo:** Documentar o comportamento do legado fragmentado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET (.NET Framework 4.7), ASP.NET Web Forms
- **Banco de Dados:** SQL Server 2016
- **Multi-tenant:** Não (cada cliente tinha banco separado)
- **Auditoria:** Parcial (apenas log básico de quem/quando, sem before/after)
- **Configurações:** Web.config (connection strings, appSettings)

### 1.2 Características do Sistema Legado

**Sistema legado NÃO possuía módulo específico de Plano de Contas estruturado.** A funcionalidade estava fragmentada em:

- **Cadastros Básicos:** Centros de custo e contas contábeis simplificadas
- **Rateio Manual:** Planilhas Excel paralelas para distribuição de despesas
- **Relatórios Estáticos:** DRE básico sem drill-down ou filtros avançados
- **Integração ERP:** 100% manual via export CSV → import manual no ERP
- **Classificação:** 100% manual (120 horas/mês, 18% taxa de erro)

### 1.3 Problemas Principais Identificados

1. ❌ **Fragmentação:** Funcionalidade espalhada em 4 telas diferentes sem integração
2. ❌ **Limitação Hierárquica:** Apenas 3 níveis fixos (insuficiente para empresas grandes)
3. ❌ **Sem Dimensões:** Nenhum suporte a análise multi-dimensional (Projeto, Região, etc.)
4. ❌ **Rateio Manual:** Dependência de planilhas Excel externas (erro-prone)
5. ❌ **Sem Auditoria Estrutural:** Mudanças na estrutura contábil não eram rastreadas
6. ❌ **Sem Versionamento:** Impossível recuperar estados anteriores do plano de contas
7. ❌ **Integração Manual:** Export/import manual com ERP causava atrasos de 12 dias no fechamento
8. ❌ **Sem Validações:** Erros contábeis descobertos apenas no fechamento fiscal

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Cadastro/Centro_Custo.aspx

- **Caminho:** `~/Cadastro/Centro_Custo.aspx` + `Centro_Custo.aspx.vb`
- **Responsabilidade:** Cadastro básico de centros de custo sem hierarquia organizacional
- **Tecnologia:** GridView ASP.NET + stored procedure `pa_Centro_Custo`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Centro_Custo | INT (IDENTITY) | Auto | PK |
| Nm_Centro_Custo | NVARCHAR(100) | Sim | Nome do centro |
| Codigo_Centro_Custo | VARCHAR(50) | Não | Código livre (sem padrão) |
| Fl_Desativado | BIT | Não | Default = 0 |

#### Comportamentos Implícitos

- ❌ **Sem vínculo hierárquico:** Centro custo era tabela independente, sem ligação com Empresa/Filial/Departamento
- ❌ **Sem rateio automático:** Sistema não calculava distribuição percentual automaticamente
- ❌ **Código livre:** Usuário digitava código manualmente, sem validação de padrão ou unicidade global
- ❌ **Sem auditoria:** Alterações não eram logadas (descobria quem mudou apenas por log genérico)

**Destino no RF Moderno:** **SUBSTITUÍDO** - Nova entidade `CentroCusto` integrada à hierarquia organizacional com rateio cascata automático (RN-RF031-03).

---

### 2.2 Tela: Recepcao_Fatura/Plano_Conta.aspx

- **Caminho:** `~/Recepcao_Fatura/Plano_Conta.aspx` + `Plano_Conta.aspx.vb`
- **Responsabilidade:** Cadastro simplificado de contas contábeis com apenas 3 níveis fixos
- **Tecnologia:** TreeView VB6-style + stored procedure `pa_Plano_Conta`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Plano_Conta | INT (IDENTITY) | Auto | PK |
| Codigo_Nivel_1 | VARCHAR(10) | Não | Ex: "5" (Despesas) |
| Codigo_Nivel_2 | VARCHAR(10) | Não | Ex: "5.1" (Desp Admin) |
| Codigo_Nivel_3 | VARCHAR(10) | Não | Ex: "5.1.2" (Telecom) |
| Nm_Conta | NVARCHAR(200) | Sim | Nome da conta |
| Tipo_Conta | CHAR(1) | Sim | 'S'=Sintética, 'A'=Analítica |

#### Comportamentos Implícitos

- ❌ **Hierarquia rígida:** Apenas 3 níveis fixos (Classe, Grupo, Conta) - insuficiente para estruturas complexas
- ❌ **Códigos separados:** Cada nível tinha campo separado em vez de hierarquia referencial (pai/filho)
- ❌ **Sem validação sintética/analítica:** Sistema permitia lançamentos em contas sintéticas (erro contábil)
- ❌ **Sem validação unicidade:** Códigos podiam duplicar entre níveis diferentes
- ❌ **Tree estático:** TreeView VB6 sem drag-and-drop, apenas exibição

**Destino no RF Moderno:** **SUBSTITUÍDO** - Nova entidade `PlanoContaContabil` com até 7 níveis configuráveis + hierarquia recursiva (RN-RF031-01, RN-RF031-02).

---

### 2.3 Tela: Recepcao_Fatura/Rateio.aspx

- **Caminho:** `~/Recepcao_Fatura/Rateio.aspx` + `Rateio.aspx.vb`
- **Responsabilidade:** Rateio manual de despesas entre centros de custo via planilha Excel
- **Tecnologia:** Import Excel + stored procedure `sp_Rateio_Calcular`

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Rateio | INT (IDENTITY) | Auto | PK |
| Id_Fatura | INT | Sim | FK para Fatura |
| Id_Centro_Custo | INT | Sim | FK para Centro_Custo |
| Percentual | DECIMAL(5,2) | Sim | % de rateio |
| Valor_Rateado | DECIMAL(18,2) | Não | Calculado = Fatura.Valor * Percentual |

#### Comportamentos Implícitos

- ❌ **100% manual:** Usuário preenchia planilha Excel e importava para sistema
- ❌ **Sem validação soma 100%:** Sistema não validava se soma percentuais = 100%
- ❌ **Sem rateio cascata:** Não permitia rateio multi-nível (Empresa → Filial → Depto → Projeto)
- ❌ **Sem histórico:** Mudança de percentual sobrescrevia valores anteriores (perda de histórico)
- ❌ **Cálculo em stored procedure:** Lógica de negócio no banco (difícil manutenção)

**Destino no RF Moderno:** **SUBSTITUÍDO** - Rateio automático multi-dimensional com validação soma 100% e versionamento de mudanças (RN-RF031-03, RN-RF031-04).

---

### 2.4 Tela: Consulta/Template_Consulta.aspx

- **Caminho:** `~/Consulta/Template_Consulta.aspx` + `Template_Consulta.aspx.vb`
- **Responsabilidade:** Relatórios básicos de despesas por conta contábil (DRE simplificado)
- **Tecnologia:** GridView ASP.NET + stored procedure `sp_Relatorio_DRE`

#### Campos Exibidos

| Campo | Origem | Formato |
|-------|--------|---------|
| Conta | Plano_Conta.Nm_Conta | Texto |
| Valor_Mes | SUM(Lancamento.Valor) | Moeda |
| Percentual | Calculado | % |

#### Comportamentos Implícitos

- ❌ **Estático:** Relatório fixo mensal sem filtros customizáveis
- ❌ **Sem drill-down:** Não permitia clicar em conta para ver lançamentos detalhados
- ❌ **Sem comparações:** Não comparava MoM, YoY ou orçado x realizado
- ❌ **Sem exportação formatada:** Export para Excel era dump bruto sem formatação
- ❌ **Sem filtros multi-dimensionais:** Não permitia filtrar por Projeto, Região, Departamento

**Destino no RF Moderno:** **SUBSTITUÍDO** - DRE multi-dimensional com drill-down ilimitado, filtros avançados, análise vertical/horizontal (RN-RF031-08).

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: WSCadastro.asmx

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `Centro_Custo_Insert` | `~/WebServices/WSCadastro.asmx` | Inserir centro custo | Chama `pa_Centro_Custo` |
| `Centro_Custo_Update` | `~/WebServices/WSCadastro.asmx` | Atualizar centro custo | Sem validação de negócio |
| `Centro_Custo_Delete` | `~/WebServices/WSCadastro.asmx` | Deletar centro custo | DELETE físico (não soft delete) |
| `Centro_Custo_GetAll` | `~/WebServices/WSCadastro.asmx` | Listar centros custo | Sem paginação |

**Problemas:**
- ❌ DELETE físico (perde histórico)
- ❌ Sem validações de negócio (executava stored procedure direto)
- ❌ Sem tratamento de erros estruturado (exceções genéricas)

**Destino no RF Moderno:** **SUBSTITUÍDO** - Minimal APIs .NET 10 com Commands/Queries CQRS, validações FluentValidation, soft delete obrigatório.

---

### 3.2 WebService: WSRecepcao_Fatura.asmx

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `Plano_Conta_Insert` | `~/WebServices/WSRecepcao_Fatura.asmx` | Inserir conta | Chama `pa_Plano_Conta` |
| `Plano_Conta_GetHierarquia` | `~/WebServices/WSRecepcao_Fatura.asmx` | Buscar hierarquia | XML recursivo |
| `Rateio_Calcular` | `~/WebServices/WSRateio.asmx` | Calcular rateio | Chama `sp_Rateio_Calcular` |

**Problemas:**
- ❌ XML recursivo complexo (difícil manutenção)
- ❌ Lógica de negócio em stored procedure (não testável unitariamente)
- ❌ Sem contratos de API (documentação manual desatualizada)

**Destino no RF Moderno:** **SUBSTITUÍDO** - APIs REST com Swagger/OpenAPI, contratos DTOs tipados, lógica no Application Layer (Commands/Queries).

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Centro_Custo

```sql
CREATE TABLE Centro_Custo (
    Id_Centro_Custo INT IDENTITY(1,1) PRIMARY KEY,
    Nm_Centro_Custo NVARCHAR(100) NOT NULL,
    Codigo_Centro_Custo VARCHAR(50) NULL,
    Fl_Desativado BIT DEFAULT 0
);
```

**Finalidade:** Cadastro de centros de custo sem hierarquia organizacional.

**Problemas Identificados:**
- ❌ Sem FK para Empresa/Filial/Departamento (centros desconectados da hierarquia)
- ❌ Sem campos de auditoria (Created_By, Created_At, Modified_By, Modified_At)
- ❌ Sem soft delete (Fl_Excluido)
- ❌ Código livre sem padrão ou validação

**Destino no RF Moderno:** **SUBSTITUÍDO** - Nova tabela `CentroCusto` com FKs para hierarquia organizacional, auditoria completa, soft delete (RN-RF031-03).

---

### 4.2 Tabela: Plano_Conta

```sql
CREATE TABLE Plano_Conta (
    Id_Plano_Conta INT IDENTITY(1,1) PRIMARY KEY,
    Codigo_Nivel_1 VARCHAR(10) NULL,  -- Ex: "5" (Despesas)
    Codigo_Nivel_2 VARCHAR(10) NULL,  -- Ex: "5.1" (Desp Admin)
    Codigo_Nivel_3 VARCHAR(10) NULL,  -- Ex: "5.1.2" (Telecom)
    Nm_Conta NVARCHAR(200) NOT NULL,
    Tipo_Conta CHAR(1) CHECK (Tipo_Conta IN ('S','A')) -- S=Sintética, A=Analítica
);
```

**Finalidade:** Plano de contas simplificado com 3 níveis fixos.

**Problemas Identificados:**
- ❌ Estrutura rígida de 3 níveis (insuficiente)
- ❌ Campos separados em vez de hierarquia recursiva (difícil navegação)
- ❌ Sem FK para pai (impossível query recursiva CTE)
- ❌ Sem validação sintética/analítica no código (permitia lançamentos em sintéticas)
- ❌ Sem multi-tenancy (`Id_Conglomerado`)
- ❌ Sem auditoria

**Destino no RF Moderno:** **SUBSTITUÍDO** - Nova tabela `PlanoContaContabil` com hierarquia recursiva (`PlanoContaContabil_PaiId`), até 7 níveis, multi-tenancy, auditoria completa (RN-RF031-01, RN-RF031-15).

---

### 4.3 Tabela: Rateio

```sql
CREATE TABLE Rateio (
    Id_Rateio INT IDENTITY(1,1) PRIMARY KEY,
    Id_Fatura INT NOT NULL,
    Id_Centro_Custo INT NOT NULL,
    Percentual DECIMAL(5,2) NOT NULL,
    Valor_Rateado DECIMAL(18,2) NULL
);
```

**Finalidade:** Rateio manual de faturas entre centros de custo.

**Problemas Identificados:**
- ❌ Sem validação soma percentuais = 100%
- ❌ Valor rateado calculado mas armazenado (redundância, risco dessincronia)
- ❌ Sem suporte a rateio multi-nível (cascata)
- ❌ Sem histórico de mudanças (sobrescrevia valores)
- ❌ Sem suporte a dimensões (apenas centro custo)

**Destino no RF Moderno:** **SUBSTITUÍDO** - Rateio integrado na entidade `LancamentoContabil` com suporte a múltiplas dimensões, validação automática, versionamento (RN-RF031-03, RN-RF031-04).

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras que não estavam documentadas formalmente, descobertas no código VB.NET:

### RL-RN-001: Código Centro Custo Manual Sem Validação

**Descrição (extraída do código):** Sistema permitia usuário digitar qualquer código de centro custo sem validação de formato ou unicidade global. Controllers contábeis mantinham padrão informal `CC-{EmpresaId}-{DeptId}` em planilhas Excel paralelas.

**Localização Código:** `Centro_Custo.aspx.vb`, linha 127:
```vb
' VB.NET - Sem validação
txtCodigoCentroCusto.Text = txtCodigoCentroCusto.Text.Trim()
' Salvava direto no banco sem checar duplicidade
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - Sistema sugere código padrão `CC-{ClienteId}-{DeptId}` mas permite customização com validação unicidade (RN-RF031-03).

---

### RL-RN-002: Lançamento Permitido em Conta Sintética

**Descrição (extraída do código):** Stored procedure `sp_Lancamento_Insert` não validava se conta era Analítica antes de inserir lançamento. Erro descoberto apenas no fechamento fiscal quando auditor rejeitava relatório.

**Localização Código:** `sp_Lancamento_Insert.sql`, linha 45:
```sql
-- SQL - Sem validação tipo conta
INSERT INTO Lancamento (Id_Plano_Conta, Valor, ...)
VALUES (@Id_Plano_Conta, @Valor, ...)
-- Deveria validar: WHERE Tipo_Conta = 'A'
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - Validação obrigatória pré-save: lançamento só em conta Analítica, senão HTTP 400 (RN-RF031-11, Regra #1).

---

### RL-RN-003: Rateio Sem Validação Soma 100%

**Descrição (extraída do código):** Tela `Rateio.aspx` permitia salvar rateio mesmo se soma percentuais ≠ 100%. Descobria erro ao exportar para ERP que rejeitava arquivo.

**Localização Código:** `Rateio.aspx.vb`, linha 203:
```vb
' VB.NET - Sem validação soma
For Each row In gridRateio.Rows
    soma += CDec(row.Cells("Percentual").Value)
Next
' FALTAVA: If soma <> 100 Then Throw New Exception("Soma deve ser 100%")
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - Validação automática soma 100% com HTTP 400 se falhar (RN-RF031-03).

---

### RL-RN-004: Importação CSV TOTVS Encoding ISO-8859-1

**Descrição (extraída do código):** TOTVS Protheus 12 exportava CSV em ISO-8859-1 (Latin1) mas sistema assumia UTF-8, causando corrupção de acentos. Descoberta manual durante testes.

**Localização Código:** `ImportPlanoContas.aspx.vb`, linha 87:
```vb
' VB.NET - Encoding fixo
Dim reader As New StreamReader(arquivoCSV, Encoding.UTF8) ' ERRADO
' Deveria detectar automaticamente ou permitir configurar
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - Engine importação detecta encoding automaticamente (UTF-8, ISO-8859-1, Windows-1252) e permite override manual (RN-RF031-06).

---

### RL-RN-005: Exportação D-E Sem Validação Partida Dobrada

**Descrição (extraída do código):** Stored procedure `sp_Exportar_Lancamentos_DE` gerava arquivo contábil mas não validava se Σ débitos = Σ créditos. ERP rejeitava arquivo no import.

**Localização Código:** `sp_Exportar_Lancamentos_DE.sql`, linha 134:
```sql
-- SQL - Sem validação
SELECT 'D' AS Tipo, Conta_Debito, Valor, ...
UNION ALL
SELECT 'C' AS Tipo, Conta_Credito, Valor, ...
-- FALTAVA: Validar SUM(CASE Tipo='D' THEN Valor END) = SUM(CASE Tipo='C' THEN Valor END)
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - Validação obrigatória partida dobrada antes de exportar, preview UI com totalizadores, HTTP 400 se falhar (RN-RF031-07).

---

### RL-RN-006: DRE Sem Comparação Períodos

**Descrição (extraída do código):** Relatório DRE exibia apenas mês corrente, sem comparação MoM (Month-over-Month) ou YoY (Year-over-Year). Analistas mantinham planilhas Excel paralelas para comparações.

**Localização Código:** `sp_Relatorio_DRE.sql`, linha 23:
```sql
-- SQL - Apenas mês corrente
WHERE MONTH(Lancamento.Dt_Lancamento) = @Mes
AND YEAR(Lancamento.Dt_Lancamento) = @Ano
-- Sem JOIN para períodos anteriores
```

**Destino no RF Moderno:** **SUBSTITUÍDO** - DRE com filtro comparação (Nenhuma, MoM, YoY, Orçado x Realizado) em tempo real (RN-RF031-08).

---

## 6. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno (RF-031) | Observação |
|------|--------|---------------------|------------|
| **Níveis Hierarquia** | 3 fixos | Até 7 configuráveis | Gap crítico para empresas grandes |
| **Hierarquia Tecnologia** | Campos separados (Nivel_1, Nivel_2, Nivel_3) | Recursiva (PaiId FK) | Facilita queries CTE |
| **Centros Custo** | Tabela independente | Integrado hierarquia organizacional | Elimina desconexão |
| **Rateio** | Manual Excel (120h/mês) | Automático cascata (5h/mês) | Economia 96% tempo |
| **Dimensões** | Nenhuma | Ilimitadas (Projeto, Região, etc.) | Análise multi-dimensional |
| **Classificação** | 100% manual (18% erro) | Automática regras+ML (>95% match, <2% erro) | Redução erro 89% |
| **Importação ERP** | CSV fixo TOTVS | Multi-layout (SAP, TOTVS, Oracle, Sankhya) | Flexibilidade |
| **Exportação D-E** | Sem validação partida dobrada | Validação obrigatória + preview | Elimina rejeições ERP |
| **Relatórios DRE** | Estático mensal | Multi-dimensional drill-down | Decisões data-driven |
| **Orçamento** | Excel paralelo | Integrado real x orçado + alertas | Visibilidade tempo real |
| **Auditoria** | Log básico (quem, quando) | Trilha completa (before/after, 7 anos) | Conformidade fiscal |
| **Validações** | Nenhuma (erro pós-fechamento) | 20+ regras pré-save | Prevenção proativa |
| **Integração ERP** | Manual (12 dias fechamento) | API REST bidirecional (3 dias) | Redução 75% prazo |
| **Multi-Tenancy** | Banco separado/cliente | Row-level security (ClienteId) | Escalabilidade |
| **Delete** | Físico (perde histórico) | Soft delete (FlExcluido=TRUE) | Preserva auditoria 7 anos |
| **Versionamento** | Nenhum | Snapshot JSON antes/depois | Rastreabilidade mudanças |

**GAPs Críticos (Bloqueadores):**
1. ❌ **Apenas 3 níveis:** Insuficiente para planos contas complexos (Big Four exigem 5-7 níveis)
2. ❌ **Sem auditoria estrutural:** Impossível rastrear mudanças para auditorias externas
3. ❌ **Sem validações:** Erros descobertos tardiamente (multas, re-trabalho)

**GAPs Importantes (Alto Impacto):**
4. ❌ **Rateio manual:** 120h/mês + 18% erro + dependência Excel
5. ❌ **Sem dimensões:** Análise limitada apenas a centro custo
6. ❌ **Integração manual:** 12 dias fechamento contábil

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Hierarquia Recursiva em Vez de Campos Separados

**Motivo:** Campos separados (Nivel_1, Nivel_2, Nivel_3) limitam flexibilidade e dificultam queries recursivas. Hierarquia com FK `PaiId` permite até 7 níveis configuráveis e queries CTE eficientes.

**Impacto:** **Alto** - Requer migração de dados legados (flattening campos separados → estrutura recursiva).

**Mitigação:** Script de migração `legacy_plano_conta_to_recursive.sql` converte estrutura antiga preservando relacionamentos.

---

### Decisão 2: Soft Delete Obrigatório para Compliance Fiscal

**Motivo:** DELETE físico viola exigência Receita Federal de retenção 7 anos para auditoria. Soft delete com `FlExcluido=TRUE` preserva histórico.

**Impacto:** **Crítico** - Fundamental para conformidade LGPD, Sped, ECF.

**Mitigação:** EF Core Query Filter global adiciona `WHERE FlExcluido = 0` automaticamente em todas queries.

---

### Decisão 3: Classificação Automática com Regras + Machine Learning

**Motivo:** Classificação manual de 120h/mês com 18% erro é insustentável. Regras automatizadas + ML.NET reduzem para 5h/mês com <2% erro.

**Impacto:** **Alto** - ROI de 4 meses apenas com economia RH.

**Mitigação:** Começar com 50+ regras determinísticas, treinar modelo ML.NET com 3 meses de dados históricos.

---

### Decisão 4: Integração Bidirecional ERP via API REST

**Motivo:** Integração manual via CSV causa atrasos de 12 dias no fechamento. API REST bidirecional reduz para 3 dias com validações pré-envio.

**Impacto:** **Alto** - Redução 75% prazo fechamento contábil.

**Mitigação:** Hangfire jobs agendados + retry policy Polly + fallback manual se API falhar.

---

### Decisão 5: Multi-Tenancy via Row-Level Security (ClienteId)

**Motivo:** Bancos separados por cliente (legado) não escalam. Row-level security via `ClienteId` permite SaaS multi-tenant com isolamento seguro.

**Impacto:** **Médio** - Requer índice composto `(ClienteId, Codigo_Contabil)` para performance.

**Mitigação:** EF Core Query Filter global + validação ClienteId em todos Commands/Queries.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Migração dados hierarquia recursiva falha** | Crítico | Média | Script reversível + backup completo + testes carga com dados reais |
| **Performance queries recursivas (CTE) lenta** | Alto | Baixa | Índice composto + cache Redis estrutura + benchmark 100k contas |
| **Usuários resistência classificação automática** | Médio | Alta | Treinamento + modo simulação antes de ativar + dashboard taxa match |
| **Integração API ERP timeout/falha** | Alto | Média | Retry policy Polly + fallback manual + alertas equipe TI |
| **ML modelo baixa acurácia inicial** | Médio | Alta | Começar com regras determinísticas, treinar ML incremental 3 meses |
| **Perda dados auditoria na migração** | Crítico | Baixa | Migrar log legado para nova estrutura + retenção 7 anos |

---

## 9. RASTREABILIDADE

### 9.1 Mapeamento Telas Legado → RF Moderno

| Elemento Legado | Referência RF Moderno |
|-----------------|------------------------|
| `Centro_Custo.aspx` | RN-RF031-03 (Centros Custo Hierarquia Organizacional) |
| `Plano_Conta.aspx` | RN-RF031-01 (Estrutura Hierárquica 7 Níveis) |
| `Rateio.aspx` | RN-RF031-03, RN-RF031-04 (Rateio Automático Multi-Dimensional) |
| `Template_Consulta.aspx` | RN-RF031-08 (DRE Multi-Dimensional) |

### 9.2 Mapeamento Stored Procedures → Application Layer

| Stored Procedure Legada | Referência RF Moderno |
|-------------------------|------------------------|
| `pa_Centro_Custo` | `CreateCentroCustoCommand`, `UpdateCentroCustoCommand` |
| `pa_Plano_Conta` | `CreatePlanoContaCommand`, `UpdatePlanoContaCommand` |
| `sp_Rateio_Calcular` | `CalcularRateioAutomaticoService` (Application Layer) |
| `sp_Relatorio_DRE` | `GetDREMultiDimensionalQuery` |
| `sp_Exportar_Lancamentos_DE` | `ExportarLancamentosContabeisCommand` |

### 9.3 Mapeamento Tabelas Legado → Entidades Modernas

| Tabela Legada | Entidade Moderna |
|---------------|------------------|
| `Centro_Custo` | `CentroCusto` (com FKs hierarquia) |
| `Plano_Conta` | `PlanoContaContabil` (hierarquia recursiva) |
| `Rateio` | `LancamentoContabil` (dimensões integradas) |

---

## 10. SCRIPTS DE MIGRAÇÃO DISPONÍVEIS

### 10.1 Script: legacy_plano_conta_to_recursive.sql

**Finalidade:** Converter estrutura plano contas legado (3 níveis separados) para hierarquia recursiva (PaiId).

**Localização:** ` D:\IC2\rf\Fase-3-Financeiro-I-Base-Contabil\EPIC006-FIN-Financeiro-Base\RF031-Gestao-de-Plano-Contas\Apoio\SQL\legacy_plano_conta_to_recursive.sql`

**Complexidade:** Alta (CTE recursiva + múltiplos INSERTs)

**Testado:** Sim (banco dev com 5.000 contas legadas)

---

### 10.2 Script: migrate_rateio_to_dimensions.sql

**Finalidade:** Migrar rateios manuais legados para nova estrutura multi-dimensional.

**Localização:** ` D:\IC2\rf\...\Apoio\SQL\migrate_rateio_to_dimensions.sql`

**Complexidade:** Média

**Testado:** Sim (banco dev com 10.000 lançamentos)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado fragmentado | Agência ALC - alc.dev.br |

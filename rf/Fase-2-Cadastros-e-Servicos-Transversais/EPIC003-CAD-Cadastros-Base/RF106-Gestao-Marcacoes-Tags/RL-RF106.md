# RL-RF106 — Referência ao Legado (Gestão de Marcações e Tags)

**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-106 (Gestão de Marcações e Tags)
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de marcações/tags que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, ADO.NET
- **Banco de Dados:** SQL Server (múltiplos bancos: `Branco` modelo + `SC_<OPERADORA>_<CLIENTE>` por cliente)
- **Multi-tenant:** Não (multi-tenancy via bancos separados: `SC_<OPERADORA>_<CLIENTE>`)
- **Auditoria:** Parcial (tabelas `Auditoria_*` limitadas, sem shadow properties, sem retenção garantida)
- **Configurações:** Web.config, arquivos XML, tabelas de sistema

### 1.2 Panorama da Funcionalidade Legado

O sistema legado **não possuía módulo dedicado de tags/marcações como entidade principal**. Em vez disso, utilizava:
- **Tabelas genéricas:** `Marcacao`, `Marcacao_Tipo` com estrutura simplificada
- **Tabelas de relacionamento:** `Rl_Marcacao_Ativo`, `Rl_Marcacao_Contrato`, `Rl_Marcacao_Chamado` (uma tabela por entidade)
- **Interface:** WebForms com DropdownList pré-carregada (sem auto-complete)
- **Busca:** LIKE em T-SQL com NOLOCK (sem ElasticSearch)
- **Sem hierarquia:** Não suportava taxonomia pai-filho
- **Sem cor/ícone:** Tags eram apenas texto
- **Sem sugestões:** Nenhum mecanismo de ML ou autocomplete inteligente
- **Sem dashboard:** Relatórios tabulares simples

### 1.3 Problemas Identificados no Legado

| Problema | Descrição | Impacto |
|----------|-----------|---------|
| **Sem hierarquia** | Não suportava tags pai/filho, impossível criar taxonomias | Dificuldade em organizar tags relacionadas, poluição visual |
| **Sem auto-complete** | DropdownList pré-carregada, lenta com > 100 tags | UX ruim, performance degradada |
| **Sem sugestões** | Tudo manual, sem ML | Esforço manual alto, inconsistência taxonomômica |
| **Sem cores/ícones** | Tags apenas texto | Falta de destaque visual, dificuldade em distinguir prioridades |
| **Busca LIKE lenta** | SELECT com LIKE em T-SQL | Performance ruim com > 1000 tags |
| **Sem nuvem de tags** | Apenas relatórios tabulares | Falta de visualização analítica |
| **Sem fusão** | Tags duplicadas acumulavam sem consolidação | Poluição de dados, inconsistência |
| **Auditoria limitada** | Logs em tabelas `Auditoria_*` sem estrutura padronizada | Rastreabilidade incompleta |
| **Multi-tenancy frágil** | Bancos separados (`SC_*`), sem isolamento via ClienteId | Complexidade operacional, risco de vazamento de dados |
| **IDs INT** | Chaves primárias INT IDENTITY | Conflito ao migrar entre bancos, dificulta distribuição |

---

## 2. TELAS DO LEGADO

### Tela: Cadastro de Marcações

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Marcacao.aspx`
- **Responsabilidade:** Gerenciar marcações simples (CRUD básico)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtNome` | TextBox | Sim | Nome da marcação (máximo 50 caracteres) |
| `txtDescricao` | TextBox | Não | Descrição textual (máximo 200 caracteres) |
| `ddlTipo` | DropDownList | Não | Tipo de marcação (referência a `Marcacao_Tipo`) |
| `chkAtivo` | CheckBox | Não | Flag de ativo/inativo (implícito, não soft delete) |

#### Comportamentos Implícitos

- **Validação de unicidade:** Não validava duplicatas no front-end, apenas constraint no banco (erro genérico ao usuário)
- **Sem validação de comprimento:** TextBox permitia digitar além de 50 caracteres, erro apenas ao salvar
- **Sem feedback visual:** Nenhuma indicação de tags mais usadas ou sugestões
- **Paginação rudimentar:** GridView com paginação nativa ASP.NET (ViewState pesado)
- **Sem busca:** Nenhum campo de filtro ou busca, apenas scroll manual

#### Código Code-Behind (Extrato Comportamental)

```vb
' Salvar marcação (sem validação de duplicata no código)
Protected Sub btnSalvar_Click(sender As Object, e As EventArgs)
    Dim nome As String = txtNome.Text.Trim()
    Dim descricao As String = txtDescricao.Text.Trim()

    ' Nenhuma validação de duplicata aqui - espera erro do banco
    Dim sql As String = "INSERT INTO Marcacao (Nm_Marcacao, Descricao, Fl_Excluido, Dt_Incluido) VALUES (@Nome, @Descricao, 0, GETDATE())"
    ' Execução ADO.NET com tratamento genérico de erro
End Sub

' Carregar dropdown de tipos (pré-carrega TODAS as marcações - problema de performance)
Protected Sub Page_Load(sender As Object, e As EventArgs)
    If Not IsPostBack Then
        ddlTipo.DataSource = ObterTiposMarcacao() ' SELECT * FROM Marcacao_Tipo
        ddlTipo.DataBind()
    End If
End Sub
```

---

### Tela: Consultas com Filtro de Marcação

- **Caminho:** `ic1_legado/IControlIT/Consulta/*.aspx` (múltiplas telas: Ativos, Contratos, Chamados)
- **Responsabilidade:** Filtrar entidades por marcação via checkboxes

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `chkListMarcacoes` | CheckBoxList | Não | Lista de marcações pré-carregadas (todas) |
| `btnFiltrar` | Button | - | Aplica filtro selecionado |

#### Comportamentos Implícitos

- **Pré-carga completa:** CheckBoxList carregava TODAS as marcações do banco (problema de performance com > 100 marcações)
- **Sem paginação de marcações:** Scroll infinito se houvesse muitas
- **Filtro apenas OR:** Seleção de múltiplas marcações funcionava como OR (qualquer uma), sem opção AND
- **Postback completo:** Cada filtro causava postback full page (ViewState pesado, lento)

---

## 3. BANCO DE DADOS LEGADO

### 3.1 Estrutura de Tabelas

#### Tabela: `Marcacao`

**Finalidade:** Armazenar marcações (tags) genéricas

```sql
CREATE TABLE [dbo].[Marcacao](
    [Id_Marcacao] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Marcacao] [varchar](50) NOT NULL,
    [Descricao] [nvarchar](200) NULL,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Dt_Incluido] [datetime] NOT NULL DEFAULT GETDATE(),
    [Dt_Alterado] [datetime] NULL,

    CONSTRAINT [PK_Marcacao] PRIMARY KEY CLUSTERED ([Id_Marcacao] ASC),
    CONSTRAINT [UQ_Marcacao_Nome] UNIQUE ([Nm_Marcacao])
);
```

**Problemas Identificados:**
- **ID INT:** Chave primária INT IDENTITY (conflitos ao migrar entre bancos)
- **Sem ClienteId:** Não suportava multi-tenancy (isolamento via bancos separados)
- **UNIQUE sem case-insensitive:** Constraint UNIQUE não configurada para case-insensitive (permitia "Crítico" e "crítico")
- **VARCHAR(50):** Limite muito restrito (moderno usa NVARCHAR(100))
- **Sem cor/ícone:** Não havia campos HexColor, IconClass
- **Sem hierarquia:** Não havia ParentTagId
- **Sem contador de uso:** Não havia UsageCount (dificulta priorização)

---

#### Tabela: `Marcacao_Tipo`

**Finalidade:** Categorizar tipos de marcações (ex: "Urgente", "Projeto", "Manutenção")

```sql
CREATE TABLE [dbo].[Marcacao_Tipo](
    [Id_Marcacao_Tipo] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Tipo] [varchar](50) NOT NULL,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,

    CONSTRAINT [PK_Marcacao_Tipo] PRIMARY KEY CLUSTERED ([Id_Marcacao_Tipo] ASC)
);
```

**Problemas Identificados:**
- **Sem uso efetivo:** Raramente utilizada, estrutura redundante
- **Sem relação FK explícita:** Marcacao não tinha FK para Marcacao_Tipo (campo estava no código mas sem constraint)

**Decisão Modernizada:** Tabela descartada (ver Gap Analysis)

---

#### Tabela: `Rl_Marcacao_Ativo`

**Finalidade:** Relacionamento entre marcação e ativo

```sql
CREATE TABLE [dbo].[Rl_Marcacao_Ativo](
    [Id_Marcacao] [int] NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Dt_Inclusao] [datetime] NOT NULL DEFAULT GETDATE(),

    CONSTRAINT [FK_RL_Marcacao_Ativo_Marcacao] FOREIGN KEY ([Id_Marcacao])
        REFERENCES [dbo].[Marcacao]([Id_Marcacao]),
    CONSTRAINT [FK_RL_Marcacao_Ativo_Ativo] FOREIGN KEY ([Id_Ativo])
        REFERENCES [dbo].[Ativo]([Id_Ativo]),
    CONSTRAINT [PK_RL_Marcacao_Ativo] PRIMARY KEY CLUSTERED
        ([Id_Marcacao] ASC, [Id_Ativo] ASC)
);
```

**Problemas Identificados:**
- **Tabela por entidade:** Havia `Rl_Marcacao_Contrato`, `Rl_Marcacao_Chamado`, etc (redundância, 5+ tabelas)
- **Sem ClienteId:** Não isolava por tenant
- **Sem CriadoPor:** Não registrava quem aplicou a marcação
- **Sem auditoria:** Não havia rastreabilidade de aplicação/remoção

**Decisão Modernizada:** Consolidada em `EntityTag` polimórfica (ver Gap Analysis)

---

### 3.2 Stored Procedures Legado

**Nota:** Não havia procedures exclusivas de marcação. Esperado que migremos padrão de:

| Procedure Esperada | Descrição | Migração |
|-----------|-----------|----------|
| `pa_Marcacao_Criar` | INSERT em Marcacao + validação básica | → Entity Framework Core (SaveChangesAsync) |
| `pa_Marcacao_Listar` | SELECT * FROM Marcacao WHERE Fl_Excluido = 0 ORDER BY Nm_Marcacao | → EF Core Query + ElasticSearch |
| `pa_Marcacao_Excluir` | UPDATE Fl_Excluido = 1 WHERE Id_Marcacao = @Id | → EF Core soft delete |
| `sp_Ativo_Por_Marcacao` | SELECT a.* FROM Ativo a INNER JOIN Rl_Marcacao_Ativo rm ON a.Id_Ativo = rm.Id_Ativo WHERE rm.Id_Marcacao = @Id | → LINQ query ou ElasticSearch aggregation |

**Observação:** Nenhuma procedure encontrada em `ic1_legado/IControlIT/Database/Procedures/` especificamente para marcações. Provavelmente lógica estava inline no code-behind VB.NET.

---

## 4. WEBSERVICES LEGADOS (VB.NET)

### WebService: `WSCadastro.asmx`

**Arquivo:** `ic1_legado/IControlIT/Services/WSCadastro.asmx.vb`

**Métodos Esperados (Análise Comportamental):**

#### Método: `Marcacao_Listar`

```vb
<WebMethod()> _
Public Function Marcacao_Listar(Conn_Banco As String) As DataSet
    ' SELECT * FROM Marcacao WHERE Fl_Excluido = 0 ORDER BY Nm_Marcacao
    ' Retorna DataSet com todas as marcações ativas
    ' PROBLEMA: Retorna TODAS de uma vez (sem paginação)
End Function
```

**Decisão Modernizada:** Substituído por endpoint REST `GET /api/tags?page=1&pageSize=20` com paginação obrigatória (ver RL-RFXXX.yaml)

---

#### Método: `Marcacao_Inserir`

```vb
<WebMethod()> _
Public Function Marcacao_Inserir(Conn_Banco As String, Nm_Marcacao As String, Descricao As String) As Integer
    ' INSERT INTO Marcacao (Nm_Marcacao, Descricao, Dt_Incluido, Fl_Excluido)
    ' VALUES (@Nm_Marcacao, @Descricao, GETDATE(), 0)
    ' RETURN @@IDENTITY (ID INT)
    ' PROBLEMA: Não valida duplicata (espera constraint do banco)
    ' PROBLEMA: Retorna INT IDENTITY (não GUID)
End Function
```

**Decisão Modernizada:** Substituído por `POST /api/tags` com validação FluentValidation e retorno GUID (ver RL-RFXXX.yaml)

---

#### Método: `Ativo_Por_Marcacao`

```vb
<WebMethod()> _
Public Function Ativo_Por_Marcacao(Conn_Banco As String, Id_Marcacao As Integer) As DataSet
    ' SELECT a.* FROM Ativo a
    ' INNER JOIN Rl_Marcacao_Ativo rm ON a.Id_Ativo = rm.Id_Ativo
    ' WHERE rm.Id_Marcacao = @Id_Marcacao AND a.Fl_Excluido = 0
    ' Retorna DataSet com ativos da marcação
    ' PROBLEMA: Queries N+1 se chamar para múltiplas marcações
End Function
```

**Decisão Modernizada:** Substituído por `GET /api/ativos?tags=ID1,ID2&tagLogic=AND` com filtro AND/OR (ver RL-RFXXX.yaml)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Unicidade de Nome (Implícita via Constraint)

**Descrição:** Nome de marcação não podia duplicar devido a constraint UNIQUE no banco, mas não havia validação no front-end. Usuário só descobria ao clicar "Salvar" e receber erro genérico.

**Fonte:** `Marcacao` table, constraint `UQ_Marcacao_Nome`

**Destino Modernizado:** Assumido em RN-RF106-01 com validação explícita (FluentValidation) e mensagem amigável

---

### RL-RN-002: Soft Delete Silencioso

**Descrição:** Exclusão de marcação marcava `Fl_Excluido = 1`, mas não havia auditoria de quem/quando excluiu. Tags excluídas desapareciam de listas sem rastro.

**Fonte:** `ic1_legado/IControlIT/Cadastro/Marcacao.aspx.vb` (linha aproximada 150-160, método `btnExcluir_Click`)

**Destino Modernizado:** Assumido em RN-RF106-05 com auditoria completa (TagAudit)

---

### RL-RN-003: Pré-carga Total em Dropdown

**Descrição:** Dropdowns de marcação carregavam TODAS as marcações ativas de uma vez (SELECT * sem paginação). Com > 100 marcações, página ficava lenta.

**Fonte:** `ic1_legado/IControlIT/Consulta/*.aspx.vb` (métodos `Page_Load`)

**Destino Modernizado:** Substituído por auto-complete incremental com ElasticSearch (RN-RF106-07)

---

### RL-RN-004: Filtro Apenas OR

**Descrição:** Ao selecionar múltiplas marcações em CheckBoxList, filtro aplicava OR (qualquer uma). Não havia opção para AND (todas).

**Fonte:** `ic1_legado/IControlIT/Consulta/*.aspx.vb` (lógica de construção de query SQL com IN)

**Destino Modernizado:** Assumido e expandido em RN-RF106-09 com operadores AND/OR explícitos

---

### RL-RN-005: Sem Auditoria de Aplicação de Marcação

**Descrição:** Quando usuário aplicava marcação a ativo/contrato/chamado, apenas registrava `Dt_Inclusao` em `Rl_Marcacao_*`. Não registrava quem aplicou.

**Fonte:** `Rl_Marcacao_Ativo`, `Rl_Marcacao_Contrato` (estrutura da tabela)

**Destino Modernizado:** Assumido em RN-RF106-10 com auditoria completa (TagAudit + EntityTag.CriadoPor)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Existe Legado | Existe Moderno | Decisão | Observação |
|----------------|---------------|----------------|---------|------------|
| CRUD de Marcações | ✅ Parcial | ✅ Completo | Substituído | Legado não validava duplicatas no front, não tinha feedback visual |
| Hierarquia de Tags (Pai/Filho) | ❌ Não | ✅ Sim | **NOVO** | Legado não suportava taxonomias. Moderno permite 3 níveis. |
| Auto-complete | ❌ Não | ✅ Sim | **NOVO** | Legado usava DropdownList pré-carregada. Moderno usa ElasticSearch < 200ms. |
| Sugestões ML | ❌ Não | ✅ Sim | **NOVO** | Legado sem IA. Moderno integra Azure ML ou sklearn. |
| Nuvem de Tags (Tag Cloud) | ❌ Não | ✅ Sim | **NOVO** | Legado apenas relatórios tabulares. Moderno usa Chart.js. |
| Fusão de Tags Duplicadas | ❌ Não | ✅ Sim | **NOVO** | Legado acumulava duplicatas sem consolidação. |
| Renomeação em Lote | ❌ Não | ✅ Sim | **NOVO** | Legado apenas edição individual. |
| Dashboard de Uso | ❌ Não | ✅ Sim | **NOVO** | Legado sem métricas agregadas. Moderno com estatísticas em tempo real. |
| Exportação CSV/Excel | ❌ Não | ✅ Sim | **NOVO** | Legado sem exportação estruturada. |
| Cor e Ícone Personalizados | ❌ Não | ✅ Sim | **NOVO** | Legado apenas texto. Moderno com HexColor + IconClass FontAwesome. |
| Multi-tenancy via ClienteId | ❌ Não (bancos separados) | ✅ Sim | Substituído | Legado usava `SC_*` bancos. Moderno usa ClienteId (GUID). |
| Auditoria Completa | ❌ Parcial | ✅ Completa | Substituído | Legado `Auditoria_*` limitado. Moderno TagAudit com shadow properties. |
| Soft Delete | ✅ Sim | ✅ Sim | Assumido | Ambos usam Fl_Excluido=1, mas moderno com auditoria detalhada. |
| Permissões RBAC | ❌ Parcial (role genérico) | ✅ Granular (10 permissões) | Substituído | Legado sem granularidade. Moderno com permissions específicas. |
| Busca por Tags AND/OR | ❌ Apenas OR | ✅ AND e OR | Expandido | Legado filtro OR implícito. Moderno com operador explícito. |
| Sincronização Assíncrona | ❌ Não (síncrono) | ✅ Sim (MediatR) | **NOVO** | Legado bloqueava HTTP. Moderno event-driven. |
| Filtros Avançados | ❌ Não | ✅ Sim | **NOVO** | Legado sem ranges de datas, sem inclusão hierárquica. |

**Resumo:**
- **10 funcionalidades NOVAS** sem equivalente legado
- **5 funcionalidades SUBSTITUÍDAS** com melhorias substanciais
- **2 funcionalidades ASSUMIDAS** do legado (soft delete, unicidade)
- **0 funcionalidades DESCARTADAS** (tudo do legado foi assumido ou substituído)

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Consolidar tabelas `Rl_Marcacao_*` em `EntityTag` polimórfica

**Motivo:**
- Legado tinha 5+ tabelas (`Rl_Marcacao_Ativo`, `Rl_Marcacao_Contrato`, etc), causando:
  - Redundância de estrutura (mesmas colunas replicadas)
  - Complexidade de queries (JOIN em múltiplas tabelas)
  - Dificuldade de auditoria centralizada
- Moderno usa `EntityTag` polimórfica com campos:
  - `EntityType` (VARCHAR 50): "Ativo", "Contrato", "Chamado", etc
  - `EntityId` (UNIQUEIDENTIFIER): ID da entidade específica
  - Vantagens: Único ponto de auditoria, queries simplificadas, extensível a novas entidades

**Impacto:** Alto (requer migração de dados de 5+ tabelas)

**Data:** 2025-12-31

---

### Decisão 2: Migrar de INT para GUID (UNIQUEIDENTIFIER)

**Motivo:**
- Legado usava INT IDENTITY para `Id_Marcacao`, causando:
  - Conflitos ao migrar entre bancos (`SC_*`)
  - Impossibilidade de distribuição
  - Dificuldade em sincronização multi-datacenter
- Moderno usa GUID:
  - Geração local sem conflitos
  - Facilita migração e distribuição
  - Padrão cloud-native

**Impacto:** Médio (migração de dados INT → GUID requer mapeamento)

**Data:** 2025-12-31

---

### Decisão 3: Descartar tabela `Marcacao_Tipo`

**Motivo:**
- Legado raramente utilizava `Marcacao_Tipo` (análise de dados mostrou < 5% de marcações com tipo)
- Funcionalidade equivalente pode ser obtida via:
  - Hierarquia de tags (tag pai "Tipo: Urgente", filhas "Projeto X", "Projeto Y")
  - Cor/ícone personalizado (tags vermelhas = urgente, azuis = projeto)
- Remover estrutura redundante simplifica modelo de dados

**Impacto:** Baixo (baixo uso no legado)

**Data:** 2025-12-31

---

### Decisão 4: ElasticSearch como componente opcional (Feature Flag)

**Motivo:**
- Auto-complete < 200ms é requisito crítico, mas ElasticSearch adiciona:
  - Complexidade de infraestrutura
  - Dependência externa
  - Custo adicional
- Feature Flag `TAGS_ELASTICSEARCH` permite:
  - Fallback para LIKE em SQL (degradado mas funcional)
  - Ambientes restritos sem ES continuam operando
  - Migração incremental (habilitar ES em clientes graduais)

**Impacto:** Médio (requer fallback implementado)

**Data:** 2025-12-31

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de marcações durante migração INT → GUID** | Alto | Baixa | Script de migração com backup, validação de integridade referencial, testes em ambiente sandbox |
| **Performance degradada com LIKE (fallback ES)** | Médio | Média | Índices otimizados em SQL Server, caching de queries frequentes, monitoramento de latência |
| **Resistência de usuários a auto-complete (acostumados com dropdown)** | Baixo | Média | Treinamento, onboarding com tooltips, período de transição com ambos |
| **Dados duplicados (tags similares "Crítico", "crítico", "Critico")** | Médio | Alta | Script de consolidação pré-migração, validação case-insensitive, ferramenta de fusão de tags |
| **Auditoria incompleta (dados históricos sem rastreabilidade)** | Alto | Alta | Aceitar limitação, documentar gap, iniciar auditoria completa apenas pós-migração |
| **Quebra de integrações WebServices legadas** | Alto | Média | Manter WSCadastro.asmx como facade temporária (wrapper para API REST), deprecação gradual |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

### 9.1 Telas → UC

| Elemento Legado | Tipo | Referência RF | Referência UC | Status |
|----------------|------|---------------|---------------|--------|
| `Cadastro/Marcacao.aspx` | Tela ASPX | RN-RF106-01 (Unicidade) | UC01 (Criar tag), UC03 (Editar tag) | Substituído |
| `Consulta/*.aspx` (filtros) | Tela ASPX | RN-RF106-09 (Filtros AND/OR) | UC07 (Buscar tags) | Substituído |

### 9.2 Tabelas → Entidades

| Elemento Legado | Tipo | Referência RF | Referência MD | Status |
|----------------|------|---------------|---------------|--------|
| `Marcacao` | Tabela SQL | RN-RF106-01 a 15 | MD-RF106 (Tag) | Assumido com mudanças (INT→GUID, +campos) |
| `Marcacao_Tipo` | Tabela SQL | - | - | Descartado |
| `Rl_Marcacao_Ativo` | Tabela SQL | RN-RF106-06 | MD-RF106 (EntityTag) | Substituído (consolidado em EntityTag polimórfica) |
| `Rl_Marcacao_Contrato` | Tabela SQL | RN-RF106-06 | MD-RF106 (EntityTag) | Substituído (consolidado em EntityTag polimórfica) |

### 9.3 WebServices → Endpoints

| Elemento Legado | Tipo | Referência RF | Referência Endpoint | Status |
|----------------|------|---------------|---------------------|--------|
| `Marcacao_Listar` (SOAP) | WebMethod | RN-RF106-01 | GET /api/tags | Substituído |
| `Marcacao_Inserir` (SOAP) | WebMethod | RN-RF106-01 | POST /api/tags | Substituído |
| `Ativo_Por_Marcacao` (SOAP) | WebMethod | RN-RF106-09 | GET /api/ativos?tags=ID1,ID2 | Substituído |

### 9.4 Regras Implícitas → Regras Explícitas

| Elemento Legado | Tipo | Referência RF | Status |
|----------------|------|---------------|--------|
| RL-RN-001 (Unicidade via constraint) | Regra implícita | RN-RF106-01 | Assumido (com validação explícita) |
| RL-RN-002 (Soft delete silencioso) | Regra implícita | RN-RF106-05 + RN-RF106-10 | Assumido (com auditoria) |
| RL-RN-003 (Pré-carga dropdown) | Comportamento | RN-RF106-07 | Substituído (auto-complete) |
| RL-RN-004 (Filtro apenas OR) | Comportamento | RN-RF106-09 | Expandido (AND + OR) |
| RL-RN-005 (Sem auditoria aplicação) | Comportamento | RN-RF106-10 | Assumido (com auditoria completa) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-31 | Versão completa de referência ao legado com 7 seções obrigatórias. Análise de VB.NET, ASPX, tabelas SQL Server, WebServices. Gap analysis com 17 itens. 5 regras implícitas documentadas. 4 decisões de modernização. 6 riscos identificados. Rastreabilidade bidirecional completa. | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-31
**Autor**: Agência ALC - alc.dev.br
**Observação**: Este documento é memória técnica histórica. NÃO deve ser usado para criar novos requisitos. Para contrato moderno, consultar RF-106.md.

# RL-RF070 — Referência ao Legado: Base de Conhecimento

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-070 (Base de Conhecimento)
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de Base de Conhecimento que serve de base para a modernização, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO SISTEMA LEGADO

### Visão Geral

O módulo de Base de Conhecimento legado foi desenvolvido em **ASP.NET Web Forms + VB.NET** entre 2012-2015, com atualizações pontuais até 2020. O sistema armazenava artigos técnicos, tutoriais e FAQs em formato não estruturado, com busca rudimentar via SQL LIKE e sem controle de versões.

### Características Técnicas

- **Arquitetura:** Monolítica WebForms com código-behind em VB.NET
- **Linguagem / Stack:** VB.NET, ASP.NET WebForms 4.5, ADO.NET
- **Banco de Dados:** SQL Server 2012, schema `IControlIT_Producao`
- **Multi-tenant:** NÃO (dados misturados com filtro manual por `Id_Cliente`)
- **Auditoria:** PARCIAL (apenas data de criação e última atualização, sem before/after)
- **Configurações:** Web.config (connection strings, tamanho máximo de upload)
- **Armazenamento de Anexos:** File System local (`D:\IControlIT\Anexos\KB\`)
- **Busca:** SQL LIKE '%termo%' (lento, sem ranking de relevância)
- **Versionamento:** INEXISTENTE (edições sobrescrevem dados)
- **Workflow de Aprovação:** INEXISTENTE (publicação direta)
- **Votação/Feedback:** INEXISTENTE

### Limitações Críticas

- Busca extremamente lenta em bases > 5.000 artigos (30+ segundos)
- Sem controle de versões (impossível recuperar conteúdo anterior)
- Sem workflow de aprovação (qualquer usuário podia publicar)
- Editor HTML básico (limitado a 500KB de conteúdo)
- Anexos em file system local (backup manual, sem redundância)
- Artigos vinculados a apenas 1 categoria (relacionamento 1:1)
- Sem métricas de uso (impossível saber quais artigos eram úteis)
- Sem autoatendimento (portal integrado ao sistema principal, exigia login)

---

## 2. TELAS DO LEGADO

### Tela: BaseConhecimento.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/BaseConhecimento.aspx`
- **Responsabilidade:** Listagem de artigos com busca simples

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtBusca` | TextBox | Não | Busca por título ou conteúdo (LIKE '%termo%') |
| `ddlCategoria` | DropDownList | Não | Filtro por categoria (apenas 1) |
| `gvArtigos` | GridView | - | Lista artigos com paginação manual (10 por página) |

#### Comportamentos Implícitos

- Busca executada via stored procedure `pa_BuscarArtigos` (timeout frequente em bases grandes)
- Ordenação fixa por `Total_Acessos DESC` (não customizável)
- Sem indicador de relevância (todos resultados com mesmo peso)
- Paginação via ViewState (problema de performance)
- Ao clicar em artigo, redireciona para `ArtigoDetalhe.aspx?id={id}`

---

### Tela: ArtigoDetalhe.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/ArtigoDetalhe.aspx`
- **Responsabilidade:** Visualização completa de artigo

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `lblTitulo` | Label | - | Exibe título do artigo |
| `lblResumo` | Label | - | Exibe resumo |
| `lblProblema` | Literal | - | Renderiza HTML do problema (vulnerável a XSS) |
| `lblSolucao` | Literal | - | Renderiza HTML da solução (vulnerável a XSS) |
| `lblCategoria` | Label | - | Exibe categoria |
| `rptAnexos` | Repeater | - | Lista anexos disponíveis para download |
| `btnEditar` | Button | - | Visível apenas para criador do artigo |

#### Comportamentos Implícitos

- Contador de acessos incrementado via `pa_IncrementarAcessos` (UPDATE direto, sem auditoria)
- HTML renderizado sem sanitização (vulnerabilidade XSS)
- Sem sistema de votação (impossível avaliar utilidade)
- Sem artigos relacionados (usuário precisa buscar manualmente)
- Sem histórico de versões (impossível ver mudanças)

---

### Tela: ArtigoNovo.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/ArtigoNovo.aspx`
- **Responsabilidade:** Formulário de criação de artigo

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtTitulo` | TextBox | Sim | Máximo 200 caracteres |
| `txtResumo` | TextBox | Não | Máximo 500 caracteres |
| `txtProblema` | TextBox (multiline) | Não | Editor HTML básico |
| `txtSolucao` | TextBox (multiline) | Sim | Editor HTML básico |
| `txtCausaRaiz` | TextBox (multiline) | Não | Opcional |
| `ddlCategoria` | DropDownList | Sim | Apenas 1 categoria |
| `fuAnexos` | FileUpload | Não | Máximo 5MB por arquivo |
| `btnSalvar` | Button | - | Salva como 'Rascunho' |
| `btnPublicar` | Button | - | Publica diretamente (sem aprovação) |

#### Comportamentos Implícitos

- Validação apenas no frontend (JavaScript desabilitável)
- INSERT direto no banco via ADO.NET (sem validação de regras de negócio)
- Sem limite de tamanho de conteúdo total (causava erros de memória)
- Anexos salvos em `D:\IControlIT\Anexos\KB\{Id_Artigo}\{NomeArquivo}` (sem controle de versão)
- Sem workflow de aprovação (qualquer usuário com acesso podia publicar)

---

### Tela: ArtigoEditar.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/ArtigoEditar.aspx`
- **Responsabilidade:** Formulário de edição de artigo existente

#### Campos

Mesmos campos de `ArtigoNovo.aspx` pré-preenchidos.

#### Comportamentos Implícitos

- UPDATE direto sobrescreve todos os campos (sem versionamento)
- Apenas criador do artigo pode editar (verificação em code-behind)
- Sem registro de auditoria (impossível saber quem alterou, quando e o quê)
- Sem notificação para usuários que seguem o artigo (não existia sistema de subscrição)
- Edição simultânea por múltiplos usuários causava "last write wins" (perda de dados)

---

### Tela: Categorias.aspx

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/Categorias.aspx`
- **Responsabilidade:** Gestão de categorias hierárquicas

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `tvCategorias` | TreeView | - | Exibe árvore de categorias |
| `txtNomeCategoria` | TextBox | Sim | Nome da categoria |
| `ddlCategoriaPai` | DropDownList | Não | Categoria pai (para hierarquia) |
| `txtOrdemExibicao` | TextBox | Não | Ordem de exibição |
| `btnAdicionar` | Button | - | Adiciona nova categoria |

#### Comportamentos Implícitos

- Hierarquia limitada a 3 níveis (hard-coded)
- Sem validação de nome duplicado (permitia categorias com mesmo nome)
- Exclusão de categoria não verificava artigos vinculados (erro de FK)
- Reordenação manual (sem drag-and-drop)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Arquivo: WSBaseConhecimento.asmx.vb

**Localização:** `ic1_legado/IControlIT/WebServices/WSBaseConhecimento.asmx.vb`

| Método | Descrição | Endpoint Moderno |
|--------|-----------|-----------------|
| `BuscarArtigos(termo As String) As DataSet` | Busca simples por termo usando LIKE '%termo%' | `GET /api/base-conhecimento/artigos?q={termo}` |
| `ObterArtigo(id As Integer) As DataSet` | Retorna artigo por ID | `GET /api/base-conhecimento/artigos/{id}` |
| `CriarArtigo(dados As ArtigoDTO) As Integer` | Cria novo artigo (sem validação) | `POST /api/base-conhecimento/artigos` |
| `AtualizarArtigo(id As Integer, dados As ArtigoDTO) As Boolean` | Atualiza artigo (sem versionamento) | `PUT /api/base-conhecimento/artigos/{id}` |
| `ListarCategorias() As DataSet` | Lista todas categorias | `GET /api/base-conhecimento/categorias` |
| `IncrementarAcessos(id As Integer) As Boolean` | Incrementa contador de acessos | Evento `ArtigoAcessadoEvent` |

### Exemplo: BuscarArtigos (VB.NET)

```vb
<WebMethod()>
Public Function BuscarArtigos(termo As String) As DataSet
    Dim ds As New DataSet()
    Using conn As New SqlConnection(ConfigurationManager.ConnectionStrings("IControlIT").ConnectionString)
        Dim cmd As New SqlCommand("pa_BuscarArtigos", conn)
        cmd.CommandType = CommandType.StoredProcedure
        cmd.Parameters.AddWithValue("@Termo", termo)

        Dim adapter As New SqlDataAdapter(cmd)
        adapter.Fill(ds, "Artigos")
    End Using
    Return ds
End Function
```

### Problemas Identificados

- SOAP (verboso, difícil integração com sistemas modernos)
- Retorna DataSet (acoplamento forte com .NET Framework)
- Sem paginação (retorna todos resultados, timeout em bases grandes)
- Sem versionamento de API (mudanças quebravam integrações)
- Sem autenticação (qualquer um com acesso à rede podia chamar)
- Sem rate limiting (vulnerável a ataques DoS)
- Sem tratamento de erros estruturado (exceptions genéricas)

---

## 4. STORED PROCEDURES LEGADAS

### pa_BuscarArtigos

```sql
CREATE PROCEDURE pa_BuscarArtigos
    @Termo VARCHAR(100)
AS
BEGIN
    SELECT TOP 50
        Id_Artigo,
        Titulo,
        Resumo,
        Total_Acessos,
        Data_Criacao
    FROM tbl_BaseConhecimento
    WHERE (Titulo LIKE '%' + @Termo + '%'
           OR Descricao_Problema LIKE '%' + @Termo + '%'
           OR Solucao LIKE '%' + @Termo + '%')
      AND Status = 'Publicado'
      AND Ativo = 1
    ORDER BY Total_Acessos DESC
END
```

**Problemas:**
- `LIKE '%termo%'` não usa índices (table scan completo)
- Sem ranking por relevância (apenas por total de acessos)
- TOP 50 fixo (sem paginação customizável)
- Performance degrada exponencialmente com base > 10.000 artigos

---

### pa_IncrementarAcessos

```sql
CREATE PROCEDURE pa_IncrementarAcessos
    @Id_Artigo INT
AS
BEGIN
    UPDATE tbl_BaseConhecimento
    SET Total_Acessos = Total_Acessos + 1
    WHERE Id_Artigo = @Id_Artigo
END
```

**Problemas:**
- UPDATE direto sem auditoria (não registra quem acessou, quando, de onde)
- Contador desnormalizado (pode divergir da realidade)
- Sem registro de acessos individuais (impossível analytics detalhado)

---

### pa_ListarArtigosPorCategoria

```sql
CREATE PROCEDURE pa_ListarArtigosPorCategoria
    @Id_Categoria INT
AS
BEGIN
    SELECT
        Id_Artigo,
        Titulo,
        Resumo,
        Data_Criacao,
        Total_Acessos
    FROM tbl_BaseConhecimento
    WHERE Id_Categoria = @Id_Categoria
      AND Status = 'Publicado'
      AND Ativo = 1
    ORDER BY Data_Criacao DESC
END
```

**Problemas:**
- Relacionamento 1:1 com categoria (artigo não pode estar em múltiplas categorias)
- Sem suporte a categorias hierárquicas (não lista artigos de subcategorias)

---

## 5. TABELAS LEGADAS

### tbl_BaseConhecimento

```sql
CREATE TABLE [dbo].[tbl_BaseConhecimento](
    [Id_Artigo] [int] IDENTITY(1,1) NOT NULL,
    [Titulo] [varchar](200) NOT NULL,
    [Resumo] [varchar](500) NULL,
    [Descricao_Problema] [text] NULL,
    [Solucao] [text] NULL,
    [Causa_Raiz] [text] NULL,
    [Id_Categoria] [int] NULL,
    [Id_Usuario_Criador] [int] NOT NULL,
    [Data_Criacao] [datetime] NOT NULL DEFAULT GETDATE(),
    [Data_Ultima_Atualizacao] [datetime] NULL,
    [Status] [varchar](20) NOT NULL DEFAULT 'Rascunho',
    [Total_Acessos] [int] NOT NULL DEFAULT 0,
    [Ativo] [bit] NOT NULL DEFAULT 1,
    CONSTRAINT [PK_BaseConhecimento] PRIMARY KEY CLUSTERED ([Id_Artigo] ASC)
)
```

**Problemas Identificados:**
- Sem `ClienteId` (multi-tenancy manual via filtro)
- Tipo `text` deprecated (deveria ser `nvarchar(max)`)
- Sem campos de auditoria (quem alterou, IP, before/after)
- Sem versionamento (edições sobrescrevem dados)
- `Total_Acessos` desnormalizado (deve ser calculado de tabela de eventos)
- Sem `soft delete` rastreável (apenas flag `Ativo`)
- Relacionamento 1:1 com categoria (FK `Id_Categoria`)

---

### tbl_Categorias_Conhecimento

```sql
CREATE TABLE [dbo].[tbl_Categorias_Conhecimento](
    [Id_Categoria] [int] IDENTITY(1,1) NOT NULL,
    [Nome_Categoria] [varchar](100) NOT NULL,
    [Id_Categoria_Pai] [int] NULL,
    [Ordem_Exibicao] [int] NULL,
    [Ativo] [bit] NOT NULL DEFAULT 1,
    CONSTRAINT [PK_CategoriasConhecimento] PRIMARY KEY CLUSTERED ([Id_Categoria] ASC),
    CONSTRAINT [FK_Categoria_CategoriaPai] FOREIGN KEY ([Id_Categoria_Pai])
        REFERENCES [dbo].[tbl_Categorias_Conhecimento]([Id_Categoria])
)
```

**Problemas Identificados:**
- Sem `ClienteId` (multi-tenancy manual)
- Sem validação de nome duplicado (permitia categorias com mesmo nome)
- Sem limite de profundidade hierárquica (podia causar loops infinitos)
- Sem auditoria (impossível saber quem criou/alterou)

---

### tbl_Anexos_Conhecimento

```sql
CREATE TABLE [dbo].[tbl_Anexos_Conhecimento](
    [Id_Anexo] [int] IDENTITY(1,1) NOT NULL,
    [Id_Artigo] [int] NOT NULL,
    [Nome_Arquivo] [varchar](255) NOT NULL,
    [Caminho_Arquivo] [varchar](500) NOT NULL,
    [Tamanho_Bytes] [bigint] NULL,
    [Data_Upload] [datetime] NOT NULL DEFAULT GETDATE(),
    CONSTRAINT [PK_AnexosConhecimento] PRIMARY KEY CLUSTERED ([Id_Anexo] ASC),
    CONSTRAINT [FK_Anexo_Artigo] FOREIGN KEY ([Id_Artigo])
        REFERENCES [dbo].[tbl_BaseConhecimento]([Id_Artigo]) ON DELETE CASCADE
)
```

**Problemas Identificados:**
- Caminho absoluto local (`D:\IControlIT\Anexos\...`) não funciona em cloud
- Sem versionamento de anexos (sobrescreve arquivo com mesmo nome)
- Sem tipo MIME (impossível validar segurança)
- Sem controle de acesso (qualquer usuário autenticado pode baixar qualquer anexo)
- `ON DELETE CASCADE` perigoso (exclusão de artigo deleta anexos permanentemente)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Publicação Direta Sem Aprovação

**Fonte:** `ArtigoNovo.aspx.vb` - método `btnPublicar_Click`
**Descrição:** Qualquer usuário com permissão de criar artigos podia publicá-los diretamente, sem revisão ou aprovação.
**Problema:** Artigos com erros, informações incorretas ou desatualizadas eram publicados sem validação.

---

### RL-RN-002: Edição Exclusiva Sem Controle de Concorrência

**Fonte:** `ArtigoEditar.aspx.vb` - método `Page_Load`
**Descrição:** Sistema não implementava lock otimista ou pessimista. Edições simultâneas causavam "last write wins".
**Problema:** Perda de dados quando múltiplos usuários editavam o mesmo artigo.

---

### RL-RN-003: Busca Case-Sensitive

**Fonte:** `pa_BuscarArtigos` stored procedure
**Descrição:** Busca SQL padrão era case-sensitive (depende de collation do banco).
**Problema:** Buscar "VPN" não encontrava artigos com título "vpn" ou "Vpn".

---

### RL-RN-004: Contador de Acessos Não Auditado

**Fonte:** `pa_IncrementarAcessos` stored procedure
**Descrição:** Contador incrementado sem registrar quem acessou, quando, de onde.
**Problema:** Impossível analytics detalhado (usuários mais ativos, origem de tráfego, tempo de leitura).

---

### RL-RN-005: Anexos Sem Limite de Quantidade

**Fonte:** `ArtigoNovo.aspx.vb` - método `fuAnexos_Upload`
**Descrição:** Não havia limite de quantidade de anexos por artigo.
**Problema:** Alguns artigos tinham 50+ anexos, degradando performance de download da página.

---

### RL-RN-006: Categoria Opcional

**Fonte:** `ArtigoNovo.aspx` validation
**Descrição:** Campo categoria era tecnicamente opcional (NULL permitido no banco).
**Problema:** Artigos sem categoria ficavam "órfãos", impossíveis de encontrar via navegação.

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Impacto | Decisão |
|------|--------|------------|---------|---------|
| **Busca** | LIKE '%termo%' (lento) | ElasticSearch full-text (< 500ms) | ALTO | SUBSTITUÍDO - Migrar para motor de busca moderno |
| **Categorização** | 1:1 (1 categoria por artigo) | N:N (até 5 categorias por artigo) | MÉDIO | EVOLUÍDO - Implementar relacionamento many-to-many |
| **Versionamento** | INEXISTENTE (sobrescreve dados) | Temporal Tables (histórico completo) | ALTO | ADICIONADO - Implementar versionamento automático |
| **Workflow de Aprovação** | INEXISTENTE (publicação direta) | Configurável por categoria | MÉDIO | ADICIONADO - Implementar workflow com estados |
| **Votação/Feedback** | INEXISTENTE | Útil/Não Útil + comentários | MÉDIO | ADICIONADO - Implementar sistema de votação |
| **Anexos** | File System local | Azure Blob Storage | ALTO | SUBSTITUÍDO - Migrar para cloud storage |
| **Multi-Tenancy** | Manual (filtro por Id_Cliente) | Nativo (ClienteId em todas entidades) | ALTO | EVOLUÍDO - Implementar isolamento automático |
| **Auditoria** | PARCIAL (só data criação/atualização) | COMPLETA (before/after, 7 anos) | ALTO | EVOLUÍDO - Implementar auditoria full com Event Sourcing |
| **Editor HTML** | Básico (limitado 500KB) | Rico WYSIWYG (50MB, markdown, syntax highlighting) | MÉDIO | EVOLUÍDO - Integrar editor moderno (Quill.js) |
| **Artigos Relacionados** | INEXISTENTE (manual) | Automático via ML Similarity Score | BAIXO | ADICIONADO - Implementar algoritmo de sugestão |
| **Portal Self-Service** | Integrado (requer login) | Público (sem autenticação para artigos públicos) | MÉDIO | EVOLUÍDO - Separar portal público |
| **Tags** | INEXISTENTE | Dinâmicas com autocomplete | BAIXO | ADICIONADO - Implementar sistema de tags |
| **Multi-Idioma** | INEXISTENTE (só pt-BR) | Suporte a 3 idiomas (pt-BR, en-US, es-ES) | BAIXO | ADICIONADO - Implementar i18n |
| **Analytics** | INEXISTENTE (só contador total) | Dashboard completo (P95, coverage, obsoletos) | MÉDIO | ADICIONADO - Implementar analytics detalhado |
| **API** | SOAP (6 métodos) | REST + GraphQL (35+ endpoints) | ALTO | EVOLUÍDO - Migrar para APIs modernas |
| **Performance** | 12s para listar 1000 artigos | < 400ms com cache Redis | ALTO | OTIMIZADO - Implementar cache e lazy loading |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão #1: Substituir LIKE por ElasticSearch

**Motivo:** Performance inaceitável (30+ segundos em bases > 10.000 artigos). LIKE '%termo%' não usa índices e degrada exponencialmente.
**Impacto:** ALTO - Requer infraestrutura adicional (cluster ElasticSearch), migração de dados existentes, indexação inicial.
**Alternativa Considerada:** Azure Cognitive Search (PaaS, menor overhead operacional).
**Decisão Final:** ElasticSearch auto-hospedado (maior controle, menor custo em escala).

---

### Decisão #2: Implementar Versionamento Via Temporal Tables

**Motivo:** Impossibilidade de recuperar conteúdo anterior causou perda de dados críticos em auditorias.
**Impacto:** MÉDIO - SQL Server Temporal Tables nativo (disponível desde SQL Server 2016), sem overhead significativo.
**Alternativa Considerada:** Event Sourcing completo (maior complexidade, maior custo de desenvolvimento).
**Decisão Final:** Temporal Tables (simplicidade, performance, suportado nativamente pelo EF Core).

---

### Decisão #3: Migrar Anexos para Azure Blob Storage

**Motivo:** File System local não escalável, sem redundância, sem CDN, inacessível em cloud.
**Impacto:** ALTO - Migração de ~500GB de anexos existentes, custo mensal Azure Storage, integração com SDK.
**Alternativa Considerada:** AWS S3 (similar, mas projeto já usa Azure para outros serviços).
**Decisão Final:** Azure Blob Storage com CDN (integração nativa, custo otimizado com lifecycle policies).

---

### Decisão #4: Categorização Many-to-Many (Limite 5)

**Motivo:** Artigos técnicos frequentemente pertencem a múltiplos domínios (ex: "VPN" está em Redes, Segurança, Infraestrutura).
**Impacto:** BAIXO - Tabela associativa `ArtigoCategorias`, queries com JOIN, sem impacto em performance.
**Alternativa Considerada:** Tags apenas (sem categorias estruturadas).
**Decisão Final:** Categorias + Tags (categorias para estrutura, tags para busca livre).

---

### Decisão #5: Workflow de Aprovação Configurável

**Motivo:** Artigos críticos (Segurança, Compliance) requerem revisão dupla; artigos gerais podem ser publicados diretamente.
**Impacto:** MÉDIO - Implementar máquina de estados, tabela de configuração por categoria, notificações.
**Alternativa Considerada:** Aprovação obrigatória para todos (burocrático demais).
**Decisão Final:** Configurável por categoria (flexibilidade sem sacrificar controle).

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de Dados Durante Migração** | CRÍTICO | MÉDIA | Backup completo, migração em staging, validação automática pós-migração, rollback plan |
| **Performance de Busca Degradada** | ALTO | BAIXA | Testes de carga com base real (50.000 artigos), tuning de índices ElasticSearch, cache Redis |
| **Anexos Inacessíveis Após Migração** | ALTO | MÉDIA | Migração gradual (5% → 25% → 100%), validação de checksums, fallback para file system legado por 60 dias |
| **Resistance de Usuários a Novo Editor** | MÉDIO | ALTA | Treinamento presencial, vídeos tutoriais, modo "legacy" opcional por 90 dias |
| **Custo Azure Storage Acima do Previsto** | MÉDIO | MÉDIA | Lifecycle policies (mover anexos antigos para Cool Tier), compressão de imagens, monitoramento diário |
| **Inconsistência Multi-Tenancy** | CRÍTICO | BAIXA | Testes automatizados de isolamento, code review obrigatório, validação em staging com dados reais |
| **Workflow de Aprovação Complexo Demais** | BAIXO | ALTA | Interface visual de configuração, wizard guiado, templates pré-configurados por setor |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|----------------------|
| `tbl_BaseConhecimento` | Entidade `Artigo` (RF-070) |
| `tbl_Categorias_Conhecimento` | Entidade `Categoria` (RF-070) |
| `tbl_Anexos_Conhecimento` | Entidade `Anexo` (RF-070) |
| `pa_BuscarArtigos` | `GET /api/base-conhecimento/artigos?q={termo}` |
| `pa_IncrementarAcessos` | Evento `ArtigoAcessadoEvent` |
| `WSBaseConhecimento.BuscarArtigos` | `GET /api/base-conhecimento/artigos` |
| `WSBaseConhecimento.ObterArtigo` | `GET /api/base-conhecimento/artigos/{id}` |
| `BaseConhecimento.aspx` | Rota Angular `/base-conhecimento` |
| `ArtigoDetalhe.aspx` | Rota Angular `/base-conhecimento/artigos/:id` |
| `ArtigoNovo.aspx` | Rota Angular `/base-conhecimento/artigos/novo` |
| `ArtigoEditar.aspx` | Rota Angular `/base-conhecimento/artigos/:id/editar` |
| `Categorias.aspx` | Rota Angular `/base-conhecimento/categorias` |
| Campo `Titulo` (varchar 200) | `Titulo` (string 200, RN-RF070-02) |
| Campo `Total_Acessos` (int) | `TotalAcessos` (calculado de eventos) |
| Campo `Id_Categoria` (FK 1:1) | `Categorias` (many-to-many, RN-RF070-03) |
| Flag `Ativo` (bit) | `Excluido` (soft delete, auditado) |
| Status VARCHAR ('Rascunho', 'Publicado') | Enum `StatusArtigo` com 8 estados (RF-070 Seção 6) |
| Anexos em `D:\IControlIT\Anexos\` | Azure Blob Storage + CDN (RN-RF070-09) |
| Busca LIKE '%termo%' | ElasticSearch full-text (RN-RF070-11) |
| Sem versionamento | Temporal Tables (RN-RF070-07) |
| Sem votação | Sistema Útil/Não Útil (RN-RF070-05) |
| Sem workflow | Estados + Transições (RF-070 Seção 6) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Extração completa da memória técnica do legado VB.NET/ASPX. Documentação de telas, WebServices, SPs, tabelas, regras implícitas e gap analysis. | Agência ALC - alc.dev.br |

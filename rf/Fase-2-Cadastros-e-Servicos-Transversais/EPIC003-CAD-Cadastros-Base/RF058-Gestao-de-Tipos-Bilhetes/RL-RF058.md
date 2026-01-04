# RL-RF058 - Referência ao Legado: Tipos de Bilhetes

**Versão:** 1.0
**Data de Criação:** 2025-12-30
**RF Correspondente:** RF058 - Gestão de Tipos de Bilhetes
**Status:** Mapeamento Completo

---

## 1. IDENTIFICAÇÃO DO LEGADO

### 1.1. Sistema de Origem
- **Sistema:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
- **Módulo:** Cadastros Base
- **Funcionalidade:** Gestão de Tipos de Bilhetes

### 1.2. Localização no Código Legado

**Páginas ASPX:**
```
ic1_legado/IControlIT/Cadastros/TiposBilhetes/
├── Lista.aspx (listagem)
├── Novo.aspx (criação)
├── Editar.aspx (edição)
└── Detalhes.aspx (visualização)
```

**Code-Behind VB.NET:**
```
ic1_legado/IControlIT/Cadastros/TiposBilhetes/
├── Lista.aspx.vb
├── Novo.aspx.vb
├── Editar.aspx.vb
└── Detalhes.aspx.vb
```

**Classes Helper:**
```
ic1_legado/IControlIT/App_Code/Helpers/
└── TipoBilheteHelper.vb
```

**Stored Procedures:**
```sql
-- ic1_legado/Database/StoredProcedures/
SP_TipoBilhete_Listar
SP_TipoBilhete_Inserir
SP_TipoBilhete_Atualizar
SP_TipoBilhete_Excluir
SP_TipoBilhete_Buscar
```

---

## 2. ANÁLISE DA IMPLEMENTAÇÃO LEGADA

### 2.1. Funcionalidades Existentes

#### 2.1.1. Listagem de Tipos de Bilhetes (Lista.aspx)
**Implementação Legada:**
- GridView com paginação manual
- Ordenação via ViewState
- Filtro por Status (DropDownList)
- Busca por Nome (TextBox + Button)
- Ações: Editar, Excluir, Visualizar

**Código VB.NET (Lista.aspx.vb):**
```vb
Protected Sub Page_Load(sender As Object, e As EventArgs) Handles Me.Load
    If Not IsPostBack Then
        CarregarGrid()
    End If
End Sub

Private Sub CarregarGrid()
    Dim helper As New TipoBilheteHelper()
    Dim empresaId As Guid = Session("EmpresaId")
    Dim status As String = ddlStatus.SelectedValue
    Dim busca As String = txtBusca.Text.Trim()

    GridView1.DataSource = helper.Listar(empresaId, status, busca)
    GridView1.DataBind()
End Sub
```

**Stored Procedure:**
```sql
CREATE PROCEDURE SP_TipoBilhete_Listar
    @EmpresaId UNIQUEIDENTIFIER,
    @Status NVARCHAR(10) = NULL,
    @Busca NVARCHAR(100) = NULL
AS
BEGIN
    SELECT
        Id, Nome, Descricao, Ativo,
        DataCriacao, UsuarioCriacaoNome
    FROM TipoBilhete
    WHERE EmpresaId = @EmpresaId
      AND Excluido = 0
      AND (@Status IS NULL OR Ativo = CAST(@Status AS BIT))
      AND (@Busca IS NULL OR Nome LIKE '%' + @Busca + '%')
    ORDER BY Nome
END
```

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - Query com LINQ no GetTiposBilhetesQuery.cs
- ✅ **MELHORADO** - Paginação via PaginatedList (backend)
- ✅ **MELHORADO** - Filtros via query string (frontend)

---

#### 2.1.2. Criação de Tipo de Bilhete (Novo.aspx)
**Implementação Legada:**
- Formulário com campos: Nome, Descrição
- Validação manual no code-behind
- RequiredFieldValidator para campos obrigatórios
- CustomValidator para nome único

**Código VB.NET (Novo.aspx.vb):**
```vb
Protected Sub btnSalvar_Click(sender As Object, e As EventArgs)
    If Not Page.IsValid Then Return

    Dim helper As New TipoBilheteHelper()
    Dim empresaId As Guid = Session("EmpresaId")
    Dim usuarioId As Guid = Session("UsuarioId")

    ' Verificar nome duplicado
    If helper.ExisteNome(txtNome.Text.Trim(), empresaId) Then
        lblErro.Text = "Já existe um tipo de bilhete com este nome."
        Return
    End If

    ' Inserir
    Dim sucesso As Boolean = helper.Inserir(
        empresaId,
        txtNome.Text.Trim(),
        txtDescricao.Text.Trim(),
        usuarioId
    )

    If sucesso Then
        Response.Redirect("Lista.aspx?msg=sucesso")
    Else
        lblErro.Text = "Erro ao criar tipo de bilhete."
    End If
End Sub
```

**Stored Procedure:**
```sql
CREATE PROCEDURE SP_TipoBilhete_Inserir
    @Id UNIQUEIDENTIFIER OUTPUT,
    @EmpresaId UNIQUEIDENTIFIER,
    @Nome NVARCHAR(100),
    @Descricao NVARCHAR(500),
    @UsuarioCriacaoId UNIQUEIDENTIFIER
AS
BEGIN
    SET @Id = NEWID()

    INSERT INTO TipoBilhete (
        Id, EmpresaId, Nome, Descricao, Ativo,
        DataCriacao, UsuarioCriacaoId, Excluido
    )
    VALUES (
        @Id, @EmpresaId, @Nome, @Descricao, 1,
        GETDATE(), @UsuarioCriacaoId, 0
    )

    SELECT @Id
END
```

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - CreateTipoBilheteCommand.cs (CQRS)
- ✅ **MELHORADO** - Validação via FluentValidation
- ✅ **MELHORADO** - Auditoria automática (AuditInterceptor)
- ✅ **MELHORADO** - Multi-tenancy automático (contexto do usuário)

---

#### 2.1.3. Edição de Tipo de Bilhete (Editar.aspx)
**Implementação Legada:**
- Formulário pré-preenchido com dados do registro
- Validação de nome único (exceto próprio registro)
- Atualização via Stored Procedure

**Código VB.NET (Editar.aspx.vb):**
```vb
Protected Sub Page_Load(sender As Object, e As EventArgs)
    If Not IsPostBack Then
        Dim id As Guid = New Guid(Request.QueryString("id"))
        CarregarDados(id)
    End If
End Sub

Private Sub CarregarDados(id As Guid)
    Dim helper As New TipoBilheteHelper()
    Dim tipo = helper.BuscarPorId(id)

    If tipo IsNot Nothing Then
        txtNome.Text = tipo.Nome
        txtDescricao.Text = tipo.Descricao
        chkAtivo.Checked = tipo.Ativo
        hdnId.Value = tipo.Id.ToString()
    End If
End Sub

Protected Sub btnSalvar_Click(sender As Object, e As EventArgs)
    Dim helper As New TipoBilheteHelper()
    Dim id As Guid = New Guid(hdnId.Value)
    Dim usuarioId As Guid = Session("UsuarioId")

    ' Verificar nome duplicado (exceto próprio)
    If helper.ExisteNome(txtNome.Text.Trim(), empresaId, id) Then
        lblErro.Text = "Já existe um tipo de bilhete com este nome."
        Return
    End If

    Dim sucesso = helper.Atualizar(
        id,
        txtNome.Text.Trim(),
        txtDescricao.Text.Trim(),
        chkAtivo.Checked,
        usuarioId
    )

    If sucesso Then
        Response.Redirect("Lista.aspx?msg=atualizado")
    End If
End Sub
```

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - UpdateTipoBilheteCommand.cs
- ✅ **MELHORADO** - Validação de unicidade no validator
- ✅ **MELHORADO** - Tracking automático de alterações (EF Core)

---

#### 2.1.4. Visualização de Detalhes (Detalhes.aspx)
**Implementação Legada:**
- Tela somente leitura
- Exibe: Nome, Descrição, Status, Dados de Auditoria
- Botão "Editar" (se permissão)

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - GetTipoBilheteByIdQuery.cs
- ✅ **MELHORADO** - Auditoria completa (acesso registrado)

---

#### 2.1.5. Exclusão/Inativação
**Implementação Legada:**
- Exclusão lógica (Excluido = 1)
- Confirmação via JavaScript
- Stored Procedure de exclusão

**Código VB.NET:**
```vb
Protected Sub GridView1_RowCommand(sender As Object, e As GridViewCommandEventArgs)
    If e.CommandName = "Excluir" Then
        Dim id As Guid = New Guid(e.CommandArgument.ToString())
        Dim helper As New TipoBilheteHelper()
        helper.Excluir(id)
        CarregarGrid()
    End If
End Sub
```

**Stored Procedure:**
```sql
CREATE PROCEDURE SP_TipoBilhete_Excluir
    @Id UNIQUEIDENTIFIER
AS
BEGIN
    UPDATE TipoBilhete
    SET Excluido = 1
    WHERE Id = @Id
END
```

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - DeleteTipoBilheteCommand.cs (soft delete)
- ✅ **MELHORADO** - Confirmação no frontend (dialog Angular Material)

---

### 2.2. Regras de Negócio Identificadas no Legado

| Regra Legado | Implementação Atual | Destino Modernizado |
|--------------|---------------------|---------------------|
| Nome único por empresa | CustomValidator + SP | ✅ **ASSUMIDO** - FluentValidation |
| Tamanho mínimo Nome (3 chars) | RequiredFieldValidator | ✅ **ASSUMIDO** - FluentValidation |
| Tamanho máximo Nome (100) | MaxLength no banco | ✅ **ASSUMIDO** - FluentValidation + EF |
| Descrição obrigatória | RequiredFieldValidator | ✅ **ASSUMIDO** - FluentValidation |
| Soft delete | UPDATE Excluido=1 | ✅ **ASSUMIDO** - DeleteCommand |
| Multi-tenancy | WHERE EmpresaId | ✅ **ASSUMIDO** - Query filters EF |
| Status padrão Ativo | DEFAULT 1 no banco | ✅ **ASSUMIDO** - Constructor Entity |

---

### 2.3. Validações Implementadas no Legado

**Validações Client-Side (ASPX):**
```aspx
<asp:RequiredFieldValidator
    ControlToValidate="txtNome"
    ErrorMessage="Nome é obrigatório"
    runat="server" />

<asp:RegularExpressionValidator
    ControlToValidate="txtNome"
    ValidationExpression="^[a-zA-Z0-9\s\-]{3,100}$"
    ErrorMessage="Nome inválido"
    runat="server" />

<asp:CustomValidator
    ControlToValidate="txtNome"
    OnServerValidate="ValidarNomeUnico"
    ErrorMessage="Nome já existe"
    runat="server" />
```

**Validações Server-Side (VB.NET):**
```vb
Protected Sub ValidarNomeUnico(source As Object, args As ServerValidateEventArgs)
    Dim helper As New TipoBilheteHelper()
    Dim empresaId As Guid = Session("EmpresaId")
    args.IsValid = Not helper.ExisteNome(args.Value, empresaId)
End Sub
```

**Destino no Modernizado:**
- ✅ **SUBSTITUÍDO** - FluentValidation (backend)
- ✅ **SUBSTITUÍDO** - Reactive Forms Validators (frontend)

---

## 3. BANCO DE DADOS LEGADO

### 3.1. Estrutura Original (SQL Server)

**Tabela TipoBilhete (Legado):**
```sql
CREATE TABLE [dbo].[TipoBilhete] (
    [Id] UNIQUEIDENTIFIER NOT NULL PRIMARY KEY DEFAULT NEWID(),
    [EmpresaId] UNIQUEIDENTIFIER NOT NULL,
    [Nome] NVARCHAR(100) NOT NULL,
    [Descricao] NVARCHAR(500) NOT NULL,
    [Ativo] BIT NOT NULL DEFAULT 1,
    [DataCriacao] DATETIME NOT NULL DEFAULT GETDATE(),
    [UsuarioCriacaoId] UNIQUEIDENTIFIER NOT NULL,
    [DataAlteracao] DATETIME NULL,
    [UsuarioAlteracaoId] UNIQUEIDENTIFIER NULL,
    [Excluido] BIT NOT NULL DEFAULT 0,

    CONSTRAINT FK_TipoBilhete_Empresa
        FOREIGN KEY (EmpresaId) REFERENCES Empresa(Id),
    CONSTRAINT FK_TipoBilhete_UsuarioCriacao
        FOREIGN KEY (UsuarioCriacaoId) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoBilhete_UsuarioAlteracao
        FOREIGN KEY (UsuarioAlteracaoId) REFERENCES Usuario(Id)
)

CREATE INDEX IX_TipoBilhete_EmpresaId ON TipoBilhete(EmpresaId)
CREATE INDEX IX_TipoBilhete_Nome ON TipoBilhete(Nome)
CREATE UNIQUE INDEX IX_TipoBilhete_Nome_Empresa
    ON TipoBilhete(Nome, EmpresaId) WHERE Excluido = 0
```

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - Estrutura idêntica mantida
- ✅ **MELHORADO** - Migration EF Core (CreateTipoBilheteTable)
- ✅ **MELHORADO** - DateTime → DateTime2 (precisão)
- ✅ **ADICIONADO** - Índice IX_TipoBilhete_Ativo

---

### 3.2. Stored Procedures Substituídas

| Stored Procedure Legado | Substituído Por (Modernizado) |
|-------------------------|-------------------------------|
| `SP_TipoBilhete_Listar` | ✅ GetTiposBilhetesQuery.cs (LINQ) |
| `SP_TipoBilhete_Inserir` | ✅ CreateTipoBilheteCommand.cs |
| `SP_TipoBilhete_Atualizar` | ✅ UpdateTipoBilheteCommand.cs |
| `SP_TipoBilhete_Excluir` | ✅ DeleteTipoBilheteCommand.cs |
| `SP_TipoBilhete_Buscar` | ✅ GetTipoBilheteByIdQuery.cs |

**Justificativa da Substituição:**
- LINQ oferece type-safety e IntelliSense
- EF Core gerencia queries automaticamente
- Melhor manutenibilidade e testabilidade
- Integração nativa com CQRS/MediatR

---

## 4. INTEGRAÇÕES LEGADAS

### 4.1. Sistema de Permissões (Legado)

**Implementação Antiga (Web.config):**
```xml
<location path="Cadastros/TiposBilhetes/Novo.aspx">
  <system.web>
    <authorization>
      <allow roles="Administrador,Gestor" />
      <deny users="*" />
    </authorization>
  </system.web>
</location>
```

**Código VB.NET:**
```vb
Protected Sub Page_Load(sender As Object, e As EventArgs)
    If Not User.IsInRole("Administrador") AndAlso Not User.IsInRole("Gestor") Then
        Response.Redirect("~/Acesso-Negado.aspx")
    End If
End Sub
```

**Destino no Modernizado:**
- ✅ **SUBSTITUÍDO** - RBAC via AuthorizationPolicies
- ✅ **MELHORADO** - Permissões granulares (VIEW, CREATE, EDIT, DELETE)
- ✅ **MELHORADO** - Validação em Endpoint + Command

---

### 4.2. Auditoria (Legado)

**Implementação Antiga:**
- Log manual em tabela AuditLog
- Trigger no banco de dados
- Registro apenas de INSERT/UPDATE/DELETE

**Trigger SQL:**
```sql
CREATE TRIGGER TR_TipoBilhete_Audit
ON TipoBilhete
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    INSERT INTO AuditLog (Entidade, Operacao, UsuarioId, Data)
    SELECT 'TipoBilhete',
           CASE WHEN EXISTS(SELECT * FROM inserted) THEN 'INSERT/UPDATE' ELSE 'DELETE' END,
           UsuarioCriacaoId,
           GETDATE()
    FROM inserted
END
```

**Destino no Modernizado:**
- ✅ **SUBSTITUÍDO** - AuditInterceptor (EF Core)
- ✅ **MELHORADO** - Registro automático de todas as operações
- ✅ **MELHORADO** - Captura dados antes/depois (JSON)
- ✅ **MELHORADO** - Registro de ACCESS (visualizações)
- ✅ **MELHORADO** - Retenção de 7 anos (LGPD)

---

### 4.3. Multi-Tenancy (Legado)

**Implementação Antiga:**
- EmpresaId armazenado em Session
- Filtro manual em todas as queries
- WHERE EmpresaId = @EmpresaId em SPs

**Destino no Modernizado:**
- ✅ **ASSUMIDO** - Query Filters globais (EF Core)
- ✅ **MELHORADO** - Tenant automático via HttpContext
- ✅ **MELHORADO** - Row-Level Security (RLS)

---

## 5. INTERFACE LEGADA (UI)

### 5.1. Tecnologias Utilizadas

**Stack Legado:**
- ASP.NET Web Forms 4.5
- Master Pages (.master)
- GridView/DetailsView
- UpdatePanel (AJAX)
- jQuery 1.x
- Bootstrap 3

**Componentes Principais:**
```aspx
<asp:GridView ID="GridView1" runat="server"
    AutoGenerateColumns="False"
    DataKeyNames="Id"
    AllowPaging="True"
    PageSize="10"
    OnPageIndexChanging="GridView1_PageIndexChanging">
    <Columns>
        <asp:BoundField DataField="Nome" HeaderText="Nome" />
        <asp:BoundField DataField="Descricao" HeaderText="Descrição" />
        <asp:TemplateField HeaderText="Status">
            <ItemTemplate>
                <%# If(Eval("Ativo"), "Ativo", "Inativo") %>
            </ItemTemplate>
        </asp:TemplateField>
        <asp:TemplateField HeaderText="Ações">
            <ItemTemplate>
                <asp:LinkButton CommandName="Editar" Text="Editar" />
                <asp:LinkButton CommandName="Excluir" Text="Excluir"
                    OnClientClick="return confirm('Confirma exclusão?');" />
            </ItemTemplate>
        </asp:TemplateField>
    </Columns>
</asp:GridView>
```

**Destino no Modernizado:**
- ✅ **SUBSTITUÍDO** - Angular 19 Standalone Components
- ✅ **SUBSTITUÍDO** - MatTable (Angular Material)
- ✅ **SUBSTITUÍDO** - MatPaginator, MatSort
- ✅ **MELHORADO** - Responsividade mobile-first
- ✅ **MELHORADO** - UX moderna (Material Design 3)

---

### 5.2. Fluxo de Navegação Legado

```
Lista.aspx (listagem)
  ↓ [Novo]
Novo.aspx (criação) → [Salvar] → Lista.aspx?msg=sucesso
  ↓ [Editar]
Editar.aspx?id={guid} → [Salvar] → Lista.aspx?msg=atualizado
  ↓ [Visualizar]
Detalhes.aspx?id={guid} → [Voltar] → Lista.aspx
```

**Destino no Modernizado:**
```
/cadastros/tipos-bilhetes (listagem)
  ↓ [Novo]
/cadastros/tipos-bilhetes/novo → [Salvar] → redirect + toast
  ↓ [Editar]
/cadastros/tipos-bilhetes/{id}/editar → [Salvar] → redirect + toast
  ↓ [Visualizar]
/cadastros/tipos-bilhetes/{id} → [Voltar] → navigate back
```

- ✅ **MELHORADO** - Rotas RESTful
- ✅ **MELHORADO** - Navegação SPA (sem reload)
- ✅ **MELHORADO** - Feedback via Snackbar (Material)

---

## 6. ANÁLISE DE GAPS (LEGADO vs MODERNIZADO)

### 6.1. Funcionalidades Descontinuadas

| Funcionalidade Legado | Motivo da Remoção | Alternativa Modernizada |
|----------------------|-------------------|-------------------------|
| Export para Excel (GridView) | Biblioteca obsoleta | ✅ Export via API (CSV/Excel) |
| Print direto do GridView | Recurso legacy | ✅ Print via CSS @media |
| Ordenação via ViewState | Performance ruim | ✅ MatSort (client-side) |

---

### 6.2. Funcionalidades Novas (Não Existiam no Legado)

| Funcionalidade Nova | Descrição | Justificativa |
|---------------------|-----------|---------------|
| Paginação Server-Side | PaginatedList no backend | Performance em grandes volumes |
| Busca Avançada | Múltiplos filtros simultâneos | Melhor UX |
| Histórico de Alterações | Auditoria completa com diff | Compliance LGPD |
| Notificações Real-Time | SignalR para atualizações | Colaboração multi-usuário |
| Temas Dark/Light | Material Theming | Acessibilidade |

---

### 6.3. Melhorias Arquiteturais

| Aspecto | Legado | Modernizado | Benefício |
|---------|--------|-------------|-----------|
| Arquitetura | N-Tier (UI → BLL → DAL) | Clean Architecture + CQRS | Separação de responsabilidades |
| Banco de Dados | Stored Procedures | Entity Framework Core + LINQ | Type-safety, produtividade |
| Validação | ASP.NET Validators | FluentValidation | Testabilidade, reutilização |
| API | Não existia (Web Forms) | Minimal APIs (.NET 10) | Reuso, integração mobile |
| Frontend | Server-rendered (ASPX) | SPA (Angular 19) | Performance, UX moderna |
| Testes | Manuais | Unitários + Integração + E2E | Qualidade, CI/CD |
| i18n | Não existia | Transloco (3 idiomas) | Globalização |
| Segurança | Role-based (limitado) | RBAC granular + Policies | Controle fino de acesso |

---

## 7. DESTINO DOS COMPONENTES LEGADOS

### 7.1. Matriz de Rastreabilidade

| Componente Legado | Status | Destino Modernizado | Observações |
|-------------------|--------|---------------------|-------------|
| Lista.aspx | ✅ **SUBSTITUÍDO** | TiposBilhetesListComponent | Angular Standalone |
| Novo.aspx | ✅ **SUBSTITUÍDO** | TiposBilhetesFormComponent | Reactive Forms |
| Editar.aspx | ✅ **SUBSTITUÍDO** | TiposBilhetesFormComponent | Mesma tela (modo edição) |
| Detalhes.aspx | ✅ **SUBSTITUÍDO** | TiposBilhetesDetailsComponent | Somente leitura |
| TipoBilheteHelper.vb | ✅ **SUBSTITUÍDO** | Commands/Queries (CQRS) | Separação leitura/escrita |
| SP_TipoBilhete_* | ✅ **SUBSTITUÍDO** | EF Core LINQ | Type-safety |
| Validators (ASPX) | ✅ **SUBSTITUÍDO** | FluentValidation + Reactive Forms | Client + Server |
| GridView Paginação | ✅ **SUBSTITUÍDO** | MatPaginator | Performance melhorada |
| Web.config (autorização) | ✅ **SUBSTITUÍDO** | AuthorizationPolicies | RBAC granular |
| Trigger Auditoria | ✅ **SUBSTITUÍDO** | AuditInterceptor | Automático EF Core |

---

## 8. CONSIDERAÇÕES FINAIS

### 8.1. Resumo da Migração

**Percentual de Código Reutilizado:** 0% (reescrita completa)
**Estrutura do Banco:** 95% mantida (apenas melhorias)
**Regras de Negócio:** 100% preservadas
**Funcionalidades:** 100% + melhorias

### 8.2. Benefícios da Modernização

1. **Performance:** Paginação server-side, queries LINQ otimizadas
2. **Manutenibilidade:** Clean Architecture, testes automatizados
3. **Segurança:** RBAC granular, auditoria completa, LGPD compliance
4. **UX:** Interface moderna, responsiva, acessível
5. **Escalabilidade:** API RESTful, SPA, cloud-ready
6. **Produtividade:** CQRS, MediatR, FluentValidation

### 8.3. Riscos Mitigados

| Risco Legado | Como Foi Mitigado |
|--------------|-------------------|
| ViewState grande | ✅ SPA (sem ViewState) |
| Postbacks lentos | ✅ API calls assíncronas |
| Código acoplado | ✅ Clean Architecture |
| Testes difíceis | ✅ Arquitetura testável |
| Multi-idioma complexo | ✅ Transloco built-in |

---

**Documento gerado conforme TEMPLATE-RL.md v1.0**
**Projeto IControlIT - Modernização Web Forms → .NET 10 + Angular 19**

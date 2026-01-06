# RL-RF043 - Referência ao Legado: Gestão de Endereços de Entrega

**Versão Governança:** 2.0
**Data Criação RL:** 2025-12-30
**RF Correspondente:** RF043 v2.0
**Propósito:** Documentar integralmente o sistema legado de endereços de entrega para rastreabilidade e análise de gaps

---

## SEÇÃO 1: CONTEXTO HISTÓRICO DO LEGADO

### 1.1 Visão Geral do Sistema Legado

O sistema legado de gestão de endereços de entrega era implementado em **ASP.NET Web Forms 4.8** com **VB.NET** como linguagem de código (code-behind). O módulo era simples e focado exclusivamente em cadastro manual de endereços, sem validações automatizadas, geocodificação ou integração com APIs externas.

**Período de Uso:** 2010-2025 (aproximadamente 15 anos)

**Características Principais:**
- Cadastro manual de endereços (digitação completa de todos os campos)
- Validação básica de campos obrigatórios (client-side JavaScript rudimentar)
- Sem integração com APIs de validação de CEP (ViaCEP, PostMon, BrasilAPI)
- Sem geocodificação (latitude/longitude inexistentes)
- Sem cálculo automático de frete
- Sem rastreamento de entregas
- Sem histórico de entregas por endereço
- Formulários Web Forms com ViewState pesado (postbacks lentos)

### 1.2 Tecnologias Utilizadas

**Frontend:**
- ASP.NET Web Forms 4.8 (ASPX + Code-Behind VB.NET)
- JavaScript puro (sem frameworks) para validações client-side
- CSS inline e arquivos `.css` antigos
- Telerik RadControls (componentes UI pagos e legados)

**Backend:**
- VB.NET (code-behind ASPX.VB)
- WebServices ASMX (comunicação SOAP)
- ADO.NET para acesso ao banco (SqlConnection, SqlCommand, SqlDataAdapter)
- Stored Procedures para operações CRUD

**Banco de Dados:**
- SQL Server 2008 R2 / 2014
- Múltiplos bancos separados por cliente (Cliente1_Modelo, Cliente2_Modelo, etc.)
- Sem multi-tenancy (cada cliente tinha banco próprio)
- Tabelas sem campos de auditoria automática (CriadoPor, CriadoEm eram preenchidos manualmente)

### 1.3 Limitações Críticas do Legado

1. **Ausência de Validação de CEP:** Usuário digitava CEP manualmente sem verificação, resultando em CEPs inexistentes ou incorretos
2. **Geocodificação Inexistente:** Endereços não tinham coordenadas geográficas (lat/long), impossibilitando mapas e cálculo de distâncias
3. **Sem Cálculo de Frete:** Valores de frete eram inseridos manualmente ou consultados em planilhas Excel externas
4. **Sem Rastreamento de Entregas:** Não havia registro de status da entrega (postado, em trânsito, entregue)
5. **Sem Histórico por Endereço:** Impossível saber quantas entregas foram feitas em um endereço ou identificar problemas recorrentes
6. **Endereço Padrão Manual:** Usuário tinha que lembrar qual endereço usar (sem pré-seleção automática)
7. **Performance Ruim:** ViewState pesado, postbacks completos, sem lazy loading
8. **Segurança Fraca:** SQL Injection possível (concatenação de strings em stored procedures), sem RBAC estruturado

### 1.4 Motivação para Modernização

**Principais Drivers:**
- **Eficiência Operacional:** Validação automática de CEP reduz erros de digitação em 95%
- **Redução de Custos:** Cálculo automático de frete economiza tempo e permite escolher transportadora mais barata
- **Rastreabilidade:** Histórico completo de entregas permite análise de problemas e otimização de rotas
- **Experiência do Usuário:** Autocomplete, validação em tempo real e pré-seleção de endereço padrão aceleram solicitações
- **Compliance:** Geocodificação precisa é obrigatória para integração com transportadoras modernas
- **Escalabilidade:** Arquitetura moderna (Clean Architecture, CQRS) permite evoluir o sistema sem reescrever tudo

---

## SEÇÃO 2: TELAS ASPX (WEB FORMS)

### 2.1 Cadastro/EnderecoEntrega.aspx

**Localização no Legado:**
```
ic1_legado/IControlIT/Cadastro/EnderecoEntrega.aspx
ic1_legado/IControlIT/Cadastro/EnderecoEntrega.aspx.vb
```

**Descrição:**
Tela de cadastro e edição de endereços de entrega. Formulário simples com campos de texto (TextBox) e botões de ação (Salvar, Cancelar). Não havia validação de CEP via API, apenas verificação de campos obrigatórios.

**Campos do Formulário:**
- `txtCEP` (TextBox) - CEP (8 dígitos, sem validação de formato)
- `txtLogradouro` (TextBox) - Rua, avenida (máximo 200 caracteres)
- `txtNumero` (TextBox) - Número do endereço (máximo 20 caracteres)
- `txtComplemento` (TextBox) - Complemento (opcional, máximo 100 caracteres)
- `txtBairro` (TextBox) - Bairro (máximo 100 caracteres)
- `txtCidade` (TextBox) - Cidade (máximo 100 caracteres)
- `ddlUF` (DropDownList) - UF (lista hardcoded de estados brasileiros)
- `chkEnderecoPadrao` (CheckBox) - Marcar como endereço padrão (sem validação de único padrão por empresa)
- `btnSalvar` (Button) - Salvar endereço
- `btnCancelar` (Button) - Cancelar e voltar para lista

**Validações Client-Side (JavaScript):**
```javascript
function ValidarFormulario() {
    var cep = document.getElementById('txtCEP').value;
    if (cep.length != 8) {
        alert('CEP deve ter 8 dígitos');
        return false;
    }
    var logradouro = document.getElementById('txtLogradouro').value;
    if (logradouro.trim() == '') {
        alert('Logradouro é obrigatório');
        return false;
    }
    // Sem validação de CEP existente via API
    return true;
}
```

**Code-Behind (VB.NET):**
```vb
Protected Sub btnSalvar_Click(sender As Object, e As EventArgs)
    Dim cep As String = txtCEP.Text.Trim()
    Dim logradouro As String = txtLogradouro.Text.Trim()
    Dim numero As String = txtNumero.Text.Trim()
    Dim complemento As String = txtComplemento.Text.Trim()
    Dim bairro As String = txtBairro.Text.Trim()
    Dim cidade As String = txtCidade.Text.Trim()
    Dim uf As String = ddlUF.SelectedValue
    Dim enderecoPadrao As Boolean = chkEnderecoPadrao.Checked

    ' Chamar stored procedure sp_InserirEnderecoEntrega
    Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("DefaultConnection").ConnectionString)
    Dim cmd As New SqlCommand("sp_InserirEnderecoEntrega", conn)
    cmd.CommandType = CommandType.StoredProcedure

    cmd.Parameters.AddWithValue("@CEP", cep)
    cmd.Parameters.AddWithValue("@Logradouro", logradouro)
    cmd.Parameters.AddWithValue("@Numero", numero)
    cmd.Parameters.AddWithValue("@Complemento", complemento)
    cmd.Parameters.AddWithValue("@Bairro", bairro)
    cmd.Parameters.AddWithValue("@Cidade", cidade)
    cmd.Parameters.AddWithValue("@UF", uf)
    cmd.Parameters.AddWithValue("@FlEnderecoPadrao", If(enderecoPadrao, 1, 0))
    cmd.Parameters.AddWithValue("@CriadoPor", Session("UsuarioId"))

    Try
        conn.Open()
        cmd.ExecuteNonQuery()
        MostrarMensagem("Endereço salvo com sucesso!")
        Response.Redirect("ListaEnderecos.aspx")
    Catch ex As Exception
        MostrarMensagem("Erro ao salvar endereço: " & ex.Message)
    Finally
        conn.Close()
    End Try
End Sub
```

**Problemas Identificados:**
- ❌ Sem validação de CEP via API (ViaCEP)
- ❌ Sem geocodificação (latitude/longitude)
- ❌ Sem validação de endereço duplicado (fuzzy match)
- ❌ Concatenação SQL (risco de SQL Injection se SP mal escrita)
- ❌ Session("UsuarioId") pode ser nula (sem tratamento de erro)
- ❌ Sem validação de único endereço padrão por empresa (business rule faltante)
- ❌ ViewState pesado (postback completo)

### 2.2 Consulta/Enderecos.aspx

**Localização no Legado:**
```
ic1_legado/IControlIT/Consulta/Enderecos.aspx
ic1_legado/IControlIT/Consulta/Enderecos.aspx.vb
```

**Descrição:**
Tela de listagem de endereços cadastrados com filtros básicos. GridView (Telerik RadGrid) com paginação server-side. Sem busca fuzzy, autocomplete ou filtros avançados.

**Componentes:**
- `txtFiltroCEP` (TextBox) - Filtro por CEP (busca exata, não fuzzy)
- `txtFiltroCidade` (TextBox) - Filtro por cidade (LIKE '%cidade%')
- `btnFiltrar` (Button) - Aplicar filtros
- `rgEnderecos` (RadGrid) - Grid de endereços
  - Colunas: CEP, Logradouro, Número, Bairro, Cidade, UF, Endereço Padrão (ícone estrela), Ações (Editar, Excluir)
  - Paginação: 20 registros por página (server-side)
  - Ordenação: por data de criação (DESC)

**Code-Behind (VB.NET):**
```vb
Protected Sub btnFiltrar_Click(sender As Object, e As EventArgs)
    Dim cep As String = txtFiltroCEP.Text.Trim()
    Dim cidade As String = txtFiltroCidade.Text.Trim()

    ' Chamar stored procedure sp_BuscarEnderecos
    Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("DefaultConnection").ConnectionString)
    Dim cmd As New SqlCommand("sp_BuscarEnderecos", conn)
    cmd.CommandType = CommandType.StoredProcedure

    cmd.Parameters.AddWithValue("@CEP", If(String.IsNullOrEmpty(cep), DBNull.Value, cep))
    cmd.Parameters.AddWithValue("@Cidade", If(String.IsNullOrEmpty(cidade), DBNull.Value, cidade))

    Dim da As New SqlDataAdapter(cmd)
    Dim dt As New DataTable()
    da.Fill(dt)

    rgEnderecos.DataSource = dt
    rgEnderecos.DataBind()
End Sub

Protected Sub rgEnderecos_DeleteCommand(sender As Object, e As GridCommandEventArgs)
    Dim enderecoId As String = e.Item.OwnerTableView.DataKeyValues(e.Item.ItemIndex)("Id").ToString()

    ' Chamar stored procedure sp_ExcluirEnderecoEntrega
    Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("DefaultConnection").ConnectionString)
    Dim cmd As New SqlCommand("sp_ExcluirEnderecoEntrega", conn)
    cmd.CommandType = CommandType.StoredProcedure

    cmd.Parameters.AddWithValue("@Id", enderecoId)

    Try
        conn.Open()
        cmd.ExecuteNonQuery()
        MostrarMensagem("Endereço excluído com sucesso!")
        btnFiltrar_Click(sender, e)  ' Recarregar grid
    Catch ex As Exception
        MostrarMensagem("Erro ao excluir endereço: " & ex.Message)
    Finally
        conn.Close()
    End Try
End Sub
```

**Problemas Identificados:**
- ❌ Sem autocomplete (usuário precisa digitar cidade completa)
- ❌ Sem busca fuzzy (erros de digitação não encontram resultados)
- ❌ Sem ordenação por "mais usados"
- ❌ Exclusão hard delete (sem soft delete FlExcluido)
- ❌ Paginação server-side lenta (reload completo da página)
- ❌ Sem validação de endereço padrão antes de excluir
- ❌ Telerik RadGrid (licença paga, componente legado)

---

## SEÇÃO 3: WEBSERVICES ASMX (SOAP)

### 3.1 EnderecoService.asmx

**Localização no Legado:**
```
ic1_legado/IControlIT/WebServices/EnderecoService.asmx
ic1_legado/IControlIT/WebServices/EnderecoService.asmx.vb
```

**Descrição:**
WebService SOAP para integração com sistema externo de gestão de pedidos. Permitia criar, consultar e excluir endereços via SOAP. Sem autenticação robusta (apenas IP whitelisting).

**Métodos Expostos:**

#### 3.1.1 BuscarEnderecoPorCEP

**SOAP Request:**
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <BuscarEnderecoPorCEP xmlns="http://icontrolit.com.br/webservices">
      <cep>01310100</cep>
    </BuscarEnderecoPorCEP>
  </soap:Body>
</soap:Envelope>
```

**SOAP Response:**
```xml
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <BuscarEnderecoPorCEPResponse xmlns="http://icontrolit.com.br/webservices">
      <BuscarEnderecoPorCEPResult>
        <Id>123e4567-e89b-12d3-a456-426614174000</Id>
        <CEP>01310-100</CEP>
        <Logradouro>Avenida Paulista</Logradouro>
        <Numero>1578</Numero>
        <Bairro>Bela Vista</Bairro>
        <Cidade>São Paulo</Cidade>
        <UF>SP</UF>
      </BuscarEnderecoPorCEPResult>
    </BuscarEnderecoPorCEPResponse>
  </soap:Body>
</soap:Envelope>
```

**Code-Behind (VB.NET):**
```vb
<WebMethod()>
Public Function BuscarEnderecoPorCEP(cep As String) As EnderecoDto
    Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("DefaultConnection").ConnectionString)
    Dim cmd As New SqlCommand("sp_BuscarEnderecoPorCEP", conn)
    cmd.CommandType = CommandType.StoredProcedure

    cmd.Parameters.AddWithValue("@CEP", cep)

    Dim endereco As New EnderecoDto()

    Try
        conn.Open()
        Dim reader As SqlDataReader = cmd.ExecuteReader()
        If reader.Read() Then
            endereco.Id = reader("Id").ToString()
            endereco.CEP = reader("CEP").ToString()
            endereco.Logradouro = reader("Logradouro").ToString()
            endereco.Numero = reader("Numero").ToString()
            endereco.Bairro = reader("Bairro").ToString()
            endereco.Cidade = reader("Cidade").ToString()
            endereco.UF = reader("UF").ToString()
        End If
        reader.Close()
    Finally
        conn.Close()
    End Try

    Return endereco
End Function
```

**Problemas Identificados:**
- ❌ SOAP (protocolo legado, substituído por REST)
- ❌ Sem autenticação JWT ou API Key (apenas IP whitelisting fraco)
- ❌ Sem versionamento de API (impossível evoluir sem quebrar clientes)
- ❌ Sem validação de input (CEP pode ser vazio, nulo ou inválido)
- ❌ Sem tratamento de erro estruturado (SoapException genérica)
- ❌ Sem paginação (retorna todos os endereços de uma só vez)
- ❌ Sem rate limiting (possível DDoS)

---

## SEÇÃO 4: STORED PROCEDURES

### 4.1 sp_InserirEnderecoEntrega

**Banco:** Cliente_Modelo (exemplo)
**Criado:** ~2010

**Código SQL:**
```sql
CREATE PROCEDURE sp_InserirEnderecoEntrega
    @CEP NVARCHAR(9),
    @Logradouro NVARCHAR(200),
    @Numero NVARCHAR(20),
    @Complemento NVARCHAR(100),
    @Bairro NVARCHAR(100),
    @Cidade NVARCHAR(100),
    @UF CHAR(2),
    @FlEnderecoPadrao BIT,
    @CriadoPor NVARCHAR(450)
AS
BEGIN
    SET NOCOUNT ON;

    -- Se marcar como padrão, desmarcar todos os outros (SEM VALIDAÇÃO DE ÚNICO)
    IF @FlEnderecoPadrao = 1
    BEGIN
        UPDATE EnderecoEntrega
        SET FlEnderecoPadrao = 0
        -- ❌ PROBLEMA: Sem WHERE ClienteId = @ClienteId (desm arca TODOS, inclusive de outros clientes!)
    END

    -- Inserir novo endereço
    INSERT INTO EnderecoEntrega (
        Id,
        CEP,
        Logradouro,
        Numero,
        Complemento,
        Bairro,
        Cidade,
        UF,
        FlEnderecoPadrao,
        CriadoPor,
        CriadoEm
    ) VALUES (
        NEWID(),
        @CEP,
        @Logradouro,
        @Numero,
        @Complemento,
        @Bairro,
        @Cidade,
        @UF,
        @FlEnderecoPadrao,
        @CriadoPor,
        GETDATE()
    );
END
```

**Problemas Identificados:**
- ❌ BUG CRÍTICO: Desmarca endereço padrão de TODOS os clientes (falta WHERE ClienteId)
- ❌ Sem validação de CEP (aceita CEP inválido ou inexistente)
- ❌ Sem validação de endereço duplicado (permite CEP + Número iguais)
- ❌ Sem multi-tenancy (ClienteId inexistente)
- ❌ CriadoPor pode ser NULL (sem validação NOT NULL)
- ❌ Sem soft delete (não cria campo FlExcluido)
- ❌ Sem auditoria de valores antes/depois (AlteradoPor, AlteradoEm ausentes)

### 4.2 sp_BuscarEnderecos

**Banco:** Cliente_Modelo
**Criado:** ~2010

**Código SQL:**
```sql
CREATE PROCEDURE sp_BuscarEnderecos
    @CEP NVARCHAR(9) = NULL,
    @Cidade NVARCHAR(100) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        Id,
        CEP,
        Logradouro,
        Numero,
        Complemento,
        Bairro,
        Cidade,
        UF,
        FlEnderecoPadrao,
        CriadoPor,
        CriadoEm
    FROM EnderecoEntrega
    WHERE
        (@CEP IS NULL OR CEP = @CEP)  -- Busca exata (sem fuzzy)
        AND (@Cidade IS NULL OR Cidade LIKE '%' + @Cidade + '%')  -- ❌ RISCO SQL INJECTION
    ORDER BY CriadoEm DESC;  -- Sem paginação (retorna TODOS os registros)
END
```

**Problemas Identificados:**
- ❌ RISCO SQL INJECTION: Concatenação com LIKE '%' + @Cidade + '%'
- ❌ Sem paginação (retorna todos os endereços de uma só vez)
- ❌ Sem busca fuzzy (Levenshtein distance)
- ❌ Sem filtro por ClienteId (multi-tenancy ausente)
- ❌ Sem filtro FlExcluido=0 (retorna endereços excluídos também)
- ❌ Sem ordenação por "mais usados" (COUNT entregas)

### 4.3 sp_ExcluirEnderecoEntrega

**Banco:** Cliente_Modelo
**Criado:** ~2010

**Código SQL:**
```sql
CREATE PROCEDURE sp_ExcluirEnderecoEntrega
    @Id UNIQUEIDENTIFIER
AS
BEGIN
    SET NOCOUNT ON;

    -- ❌ HARD DELETE (sem soft delete FlExcluido=1)
    DELETE FROM EnderecoEntrega
    WHERE Id = @Id;
END
```

**Problemas Identificados:**
- ❌ HARD DELETE: Exclui permanentemente (sem soft delete)
- ❌ Sem validação de endereço padrão (permite excluir endereço padrão)
- ❌ Sem validação de entregas vinculadas (órfãos em histórico de entregas)
- ❌ Sem auditoria de exclusão (não registra quem excluiu e quando)
- ❌ Sem ClienteId (possível excluir endereço de outro cliente)

---

## SEÇÃO 5: TABELAS LEGADAS

### 5.1 EnderecoEntrega (Legado)

**Banco:** Cliente_Modelo (cada cliente tinha banco próprio)
**DDL Original:**

```sql
CREATE TABLE EnderecoEntrega (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    CEP NVARCHAR(9) NOT NULL,  -- ❌ Sem validação de formato
    Logradouro NVARCHAR(200) NOT NULL,
    Numero NVARCHAR(20) NOT NULL,
    Complemento NVARCHAR(100) NULL,
    Bairro NVARCHAR(100) NOT NULL,
    Cidade NVARCHAR(100) NOT NULL,
    UF CHAR(2) NOT NULL,  -- ❌ Sem CHECK constraint para UFs válidas
    FlEnderecoPadrao BIT DEFAULT 0,  -- ❌ Sem UNIQUE constraint por ClienteId
    CriadoPor NVARCHAR(450) NULL,  -- ❌ Deveria ser NOT NULL
    CriadoEm DATETIME2 DEFAULT GETDATE()
    -- ❌ AUSÊNCIAS CRÍTICAS:
    --   - Latitude DECIMAL(10,8) (geocodificação)
    --   - Longitude DECIMAL(11,8) (geocodificação)
    --   - Precisao NVARCHAR(50) (ROOFTOP, RANGE_INTERPOLATED)
    --   - PlaceId NVARCHAR(200) (Google Maps)
    --   - Categoria NVARCHAR(50) (Matriz, Filial, Depósito)
    --   - NomeFantasia NVARCHAR(200) (identificação amigável)
    --   - Referencia NVARCHAR(300) (ponto de referência)
    --   - CodigoIBGE NVARCHAR(7) (código IBGE da cidade)
    --   - ClienteId UNIQUEIDENTIFIER (multi-tenancy)
    --   - AlteradoPor NVARCHAR(450) (auditoria)
    --   - AlteradoEm DATETIME2 (auditoria)
    --   - FlExcluido BIT (soft delete)
);

-- ❌ ÍNDICE AUSENTE: Busca por CEP + ClienteId
-- ❌ ÍNDICE AUSENTE: Busca fuzzy por Cidade/Bairro
-- ❌ ÍNDICE AUSENTE: Filtro FlEnderecoPadrao=1
```

**Problemas Identificados:**
- ❌ Sem campos de geocodificação (Latitude, Longitude, Precisao, PlaceId)
- ❌ Sem campo ClienteId (multi-tenancy ausente)
- ❌ Sem campos de categorização (Categoria, NomeFantasia, Referencia, CodigoIBGE)
- ❌ Sem campos de auditoria completos (AlteradoPor, AlteradoEm, FlExcluido)
- ❌ Sem validação de UF válida (aceita "ZZ", "AB", etc.)
- ❌ CriadoPor pode ser NULL (deveria ser NOT NULL)
- ❌ Sem UNIQUE constraint para FlEnderecoPadrao por ClienteId
- ❌ Sem índices para performance (CEP, Cidade, Bairro)

### 5.2 Tabelas Ausentes no Legado

**Tabelas que NÃO existiam e foram criadas na modernização:**

#### 5.2.1 EntregaHistorico
**Propósito:** Rastrear histórico de entregas por endereço
**Status Legado:** ❌ NÃO EXISTIA

**Campos Ausentes:**
- EnderecoEntregaId (FK)
- SolicitacaoId (FK)
- DataEnvio, DataPrevisao, DataEntrega
- Status (Entregue, EmTransito, Devolvido, Extraviado)
- Transportadora, CodigoRastreio
- EvidenciaFotoUrl, AssinaturaDigitalUrl, ComprovanteUrl
- AvaliacaoRecebedor (1-5 estrelas)
- ProblemaReportado
- CustoFrete

**Impacto:**
- Impossível rastrear entregas por endereço
- Impossível identificar endereços problemáticos
- Impossível calcular taxa de sucesso de entrega
- Impossível analisar custo médio de frete por endereço

#### 5.2.2 RastreamentoEvento
**Propósito:** Registrar eventos de rastreamento de transportadoras (webhooks)
**Status Legado:** ❌ NÃO EXISTIA

**Campos Ausentes:**
- EntregaHistoricoId (FK)
- DataHora
- Evento (Postado, EmTransito, SaiuParaEntrega, Entregue)
- Local
- Observacao

**Impacto:**
- Sem rastreamento em tempo real
- Sem notificações automáticas de status de entrega
- Sem timeline visual de rastreamento

---

## SEÇÃO 6: REGRAS DE NEGÓCIO IMPLÍCITAS

### 6.1 Validação de CEP (Ausente)

**Regra Legado:** CEP era aceito sem validação de existência.

**Problema:**
- Usuário digitava CEP inexistente (ex: 00000-000, 99999-999)
- Sistema aceitava e salvava
- Erro só era descoberto na hora da entrega (devolução por endereço incorreto)

**Regra Modernizada (RF043):**
- CEP validado via API ViaCEP (https://viacep.com.br/ws/{cep}/json/)
- Se inválido: exibir mensagem "CEP não encontrado - verifique se está correto"
- Fallback: PostMon (http://api.postmon.com.br/v1/cep/{cep})
- Preenchimento automático de logradouro, bairro, cidade, UF

### 6.2 Geocodificação (Ausente)

**Regra Legado:** Endereços não tinham coordenadas geográficas (latitude/longitude).

**Problema:**
- Impossível exibir endereço em mapa
- Impossível calcular distância entre matriz e endereço de entrega
- Impossível criar mapa de calor de entregas

**Regra Modernizada (RF043):**
- Endereço completo enviado para Google Maps Geocoding API
- Retorna latitude (DECIMAL(10,8)), longitude (DECIMAL(11,8)), precisão
- Armazenamento obrigatório no banco de dados
- Fallback: OpenStreetMap Nominatim

### 6.3 Cálculo de Frete (Manual)

**Regra Legado:** Valores de frete eram consultados manualmente em sites de transportadoras ou planilhas Excel.

**Problema:**
- Processo lento (usuário tinha que abrir site de cada transportadora)
- Sem comparação automática (usuário escolhia sem saber se era a melhor opção)
- Sem histórico de valores de frete (impossível analisar tendências)

**Regra Modernizada (RF043):**
- Consulta paralela a APIs de transportadoras (Correios, Jadlog, Total Express)
- Parâmetros: CEP origem, CEP destino, peso (kg), dimensões (cm), valor declarado (R$)
- Retorno: prazo (dias úteis), valor frete (R$), valor seguro (R$), total (R$)
- Ordenação: mais barato → mais rápido → melhor custo-benefício
- Cache: 6 horas (mesmos parâmetros não requisitam novamente)

### 6.4 Endereço Padrão Único (Regra Fraca)

**Regra Legado:** Endereço padrão era marcado com `FlEnderecoPadrao=1`, mas SEM validação de único padrão por empresa.

**Problema:**
- BUG: stored procedure `sp_InserirEnderecoEntrega` desmarcava TODOS os endereços padrão (inclusive de outros clientes!)
- Múltiplos endereços padrão possíveis (violação de business rule)

**Regra Modernizada (RF043):**
- Apenas 1 endereço padrão por ClienteId (Fornecedor/fornecedor)
- Ao marcar novo padrão, desmarcar anterior automaticamente (transação ACID)
- Validação FluentValidation: se FlEnderecoPadrao=1 e FlExcluido=1, retornar erro 400 "Endereço padrão não pode ser excluído. Defina outro como padrão primeiro"

### 6.5 Histórico de Entregas (Ausente)

**Regra Legado:** Não havia registro de entregas por endereço.

**Problema:**
- Impossível saber quantas entregas foram feitas em um endereço
- Impossível identificar endereços problemáticos (ex: portaria fechada recorrente)
- Impossível calcular taxa de sucesso de entrega por endereço
- Sem evidências fotográficas ou comprovantes

**Regra Modernizada (RF043):**
- Tabela `EntregaHistorico` com FK para `EnderecoEntrega` e `Solicitacao`
- Campos: DataEnvio, DataPrevisao, DataEntrega, Status, Transportadora, CodigoRastreio
- Evidências: EvidenciaFotoUrl, AssinaturaDigitalUrl, ComprovanteUrl
- Avaliação: AvaliacaoRecebedor (1-5 estrelas)
- ProblemaReportado: texto livre (máximo 500 caracteres)
- Query: últimas 10 entregas por endereço

### 6.6 Rastreamento em Tempo Real (Ausente)

**Regra Legado:** Não havia rastreamento automático. Usuário tinha que consultar site da transportadora manualmente.

**Problema:**
- Usuário não era notificado automaticamente de mudanças de status
- Atrasos só eram descobertos após prazo vencido
- Sem timeline visual de rastreamento

**Regra Modernizada (RF043):**
- Webhooks de transportadoras (POST /api/webhooks/rastreamento/{transportadora})
- Eventos: Postado, EmTransito, SaiuParaEntrega, Entregue, Devolvido
- Validação HMAC-SHA256 (segurança)
- Notificações: SignalR (push navegador), e-mail, SMS (opcional)
- Persistência: tabela `RastreamentoEvento`
- Fallback: polling a cada 1 hora (Hangfire) se webhook falhar

### 6.7 Validação de Endereço Duplicado (Ausente)

**Regra Legado:** Não havia validação de endereços duplicados.

**Problema:**
- Usuário cadastrava mesmo endereço múltiplas vezes (ex: Av. Paulista, 1578 com grafias diferentes)
- Histórico de entregas fragmentado
- Busca retornava duplicatas

**Regra Modernizada (RF043):**
- Verificação ao salvar: busca por CEP exato + Número + ClienteId
- Fuzzy match: algoritmo Levenshtein (≥90% similaridade) para Logradouro, Bairro, Cidade
- Modal: "Endereço similar encontrado. Deseja reutilizar?" (opções: Reutilizar | Salvar Novo | Cancelar)
- Log de tentativa de duplicação (tabela AuditLog)

---

## SEÇÃO 7: ANÁLISE DE GAPS

### 7.1 Gaps Funcionais

| Gap | Legado | Modernizado | Impacto |
|-----|--------|-------------|---------|
| **Validação de CEP** | ❌ Manual, sem API | ✅ ViaCEP automático | CRÍTICO - Reduz erros de digitação em 95% |
| **Geocodificação** | ❌ Não suportado | ✅ Google Maps API | ALTO - Permite mapas e cálculo de distâncias |
| **Cálculo de Frete** | ❌ Manual | ✅ APIs transportadoras | ALTO - Economia de tempo e escolha da melhor opção |
| **Histórico de Entregas** | ❌ Não rastreável | ✅ Completo com evidências | ALTO - Análise de problemas e otimização |
| **Rastreamento Tempo Real** | ❌ Não suportado | ✅ Webhooks + SignalR | MÉDIO - Notificações automáticas |
| **Mapa de Calor** | ❌ Não suportado | ✅ Heatmap entregas | BAIXO - Análise gerencial |
| **Autocomplete** | ❌ Não suportado | ✅ Busca fuzzy | MÉDIO - Experiência do usuário |
| **Validação Duplicata** | ❌ Não suportado | ✅ Fuzzy match | MÉDIO - Reduz duplicatas em 80% |
| **Exportação Relatórios** | ❌ Manual | ✅ Excel/PDF automático | BAIXO - Facilita auditorias |

### 7.2 Gaps Técnicos

| Gap | Legado | Modernizado | Impacto |
|-----|--------|-------------|---------|
| **Multi-Tenancy** | ❌ Bancos separados | ✅ ClienteId + Row-Level Security | CRÍTICO - Escalabilidade |
| **Soft Delete** | ❌ Hard delete | ✅ FlExcluido=1 | ALTO - Rastreabilidade |
| **Auditoria Automática** | ❌ Manual | ✅ Shadow Properties EF Core | ALTO - Compliance |
| **RBAC Estruturado** | ❌ Fraco | ✅ Permissões granulares | ALTO - Segurança |
| **REST API** | ❌ SOAP (ASMX) | ✅ REST (.NET 10 Minimal APIs) | MÉDIO - Interoperabilidade |
| **Performance** | ❌ Postbacks pesados | ✅ Lazy loading + paginação | MÉDIO - UX |
| **Geocodificação** | ❌ Não suportado | ✅ Lat/Long + PlaceId | ALTO - Mapas e rotas |
| **Índices Otimizados** | ❌ Ausentes | ✅ 6 índices (CEP, Cidade, Lat/Long) | MÉDIO - Performance |

### 7.3 Gaps de Segurança

| Gap | Legado | Modernizado | Impacto |
|-----|--------|-------------|---------|
| **SQL Injection** | ❌ Risco (concatenação) | ✅ Parametrizado EF Core | CRÍTICO - Segurança |
| **Autenticação API** | ❌ IP Whitelisting | ✅ JWT Bearer Token | ALTO - Segurança |
| **Webhook Signature** | ❌ Não suportado | ✅ HMAC-SHA256 | ALTO - Evitar falsificação |
| **HTTPS Obrigatório** | ❌ HTTP aceito | ✅ HTTPS only | ALTO - Segurança |

### 7.4 Plano de Migração de Dados

**Dados Existentes no Legado:**
- Endereços cadastrados (tabela `EnderecoEntrega`)
- Campos preservados: Id, CEP, Logradouro, Numero, Complemento, Bairro, Cidade, UF, FlEnderecoPadrao, CriadoPor, CriadoEm

**Dados Novos (Geocodificação Retroativa):**
1. Para cada endereço legado:
   - Geocodificar via Google Maps API (obter Latitude, Longitude, Precisao, PlaceId)
   - Se falhar: marcar `Precisao = NULL` (retry manual posterior)
2. Adicionar ClienteId (mapear banco Cliente1_Modelo → Guid do cliente)
3. Adicionar FlExcluido = 0 (todos ativos inicialmente)
4. Adicionar AlteradoPor = NULL, AlteradoEm = NULL (sem histórico de alteração)

**Script de Migração (T-SQL):**
```sql
-- 1. Adicionar colunas novas
ALTER TABLE EnderecoEntrega ADD ClienteId UNIQUEIDENTIFIER NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000';
ALTER TABLE EnderecoEntrega ADD Latitude DECIMAL(10,8) NULL;
ALTER TABLE EnderecoEntrega ADD Longitude DECIMAL(11,8) NULL;
ALTER TABLE EnderecoEntrega ADD Precisao NVARCHAR(50) NULL;
ALTER TABLE EnderecoEntrega ADD PlaceId NVARCHAR(200) NULL;
ALTER TABLE EnderecoEntrega ADD Categoria NVARCHAR(50) NULL;
ALTER TABLE EnderecoEntrega ADD NomeFantasia NVARCHAR(200) NULL;
ALTER TABLE EnderecoEntrega ADD Referencia NVARCHAR(300) NULL;
ALTER TABLE EnderecoEntrega ADD CodigoIBGE NVARCHAR(7) NULL;
ALTER TABLE EnderecoEntrega ADD AlteradoPor NVARCHAR(450) NULL;
ALTER TABLE EnderecoEntrega ADD AlteradoEm DATETIME2 NULL;
ALTER TABLE EnderecoEntrega ADD FlExcluido BIT NOT NULL DEFAULT 0;

-- 2. Atualizar ClienteId (mapear banco Cliente1_Modelo → Guid)
UPDATE EnderecoEntrega SET ClienteId = '{GUID_DO_CLIENTE}';

-- 3. Geocodificar endereços (via job backend em lote)
-- (Script .NET paralelo requisitará Google Maps API para todos os endereços)

-- 4. Criar índices
CREATE NONCLUSTERED INDEX IX_EnderecoEntrega_CEP_ClienteId
ON EnderecoEntrega (CEP, ClienteId, FlExcluido)
INCLUDE (Numero, Logradouro);

CREATE NONCLUSTERED INDEX IX_EnderecoEntrega_Cidade_Bairro
ON EnderecoEntrega (Cidade, Bairro, FlExcluido);

CREATE NONCLUSTERED INDEX IX_EnderecoEntrega_Padrao
ON EnderecoEntrega (ClienteId, FlEnderecoPadrao)
WHERE FlEnderecoPadrao = 1 AND FlExcluido = 0;

CREATE NONCLUSTERED INDEX IX_EnderecoEntrega_Coordenadas
ON EnderecoEntrega (Latitude, Longitude)
WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL;
```

**Validações Pós-Migração:**
- ✅ 100% dos endereços têm ClienteId válido
- ✅ ≥90% dos endereços têm Latitude/Longitude geocodificados
- ✅ 0 endereços com FlEnderecoPadrao=1 duplicados por ClienteId
- ✅ 0 endereços com CriadoPor=NULL

---

**FIM DA REFERÊNCIA AO LEGADO RL-RF043**

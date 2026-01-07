# RL-RF105: Referência ao Legado - Integração com APIs Externas e WebServices

**Versão**: 2.0
**Data**: 2025-12-31
**RF Relacionado**: RF105
**Status**: Memória Histórica (NÃO é contrato moderno)

---

## ATENÇÃO: Este Documento é Referência Histórica

Este arquivo documenta EXCLUSIVAMENTE como a integração com operadoras funcionava no **sistema legado VB.NET/ASPX**. Ele serve como **memória técnica** e **consulta histórica**, mas **NÃO define** o comportamento do sistema modernizado.

**Para o contrato moderno, consulte:** `RF105.md`

---

## 1. VISÃO GERAL DO LEGADO

### 1.1 Contexto Histórico

O sistema legado (IControlIT v1 - VB.NET/ASPX) possuía módulo de integração com operadoras de telecomunicações (Vivo, Claro, TIM, Oi) para:

- Importar faturas eletrônicas (XML NF-e) via SFTP ou upload manual
- Consultar consumo de linhas (voz, dados, SMS) via WebService SOAP
- Gerenciar inventário de linhas ativas
- Processar portabilidade entre operadoras
- Contestar faturas

**Tecnologias utilizadas:**
- ASP.NET Web Forms (VB.NET)
- WebService ASMX (SOAP)
- SQL Server 2008 R2
- Job Agent VB.NET (executado manualmente via Task Scheduler)
- Armazenamento local de XMLs (pasta compartilhada)

### 1.2 Principais Limitações do Legado

| Limitação | Descrição | Impacto |
|-----------|-----------|---------|
| **Integração Manual** | SFTP ou upload via portal web | Alto esforço operacional, atraso de dias |
| **Sem Cache** | Consultas diretas sem cache | Latência alta (5-30 segundos), custo por requisição |
| **Armazenamento Local** | XMLs em servidor físico | Risco de perda de dados, sem backup automático |
| **Sem Retry Automático** | Falhas exigiam reprocessamento manual | Baixa resiliência |
| **Sem Validação de Webhook** | Webhooks sem HMAC (inseguro) | Vulnerável a ataques |
| **Sem Circuit Breaker** | Sobrecarga em falhas recorrentes | Degradação cascata |
| **Jobs Manuais** | Task Scheduler sem monitoramento | Falhas silenciosas |

---

## 2. TELAS LEGADAS (ASPX)

### 2.1 GestaoOperadoras.aspx

**Localização:** `D:\IC2\ic1_legado\IControlIT\Integracao\GestaoOperadoras.aspx`

**Funcionalidade:** CRUD de configuração de operadoras (credenciais, endpoints).

**Campos do Formulário:**
- Nome da Operadora (dropdown: Vivo, Claro, TIM, Oi)
- API Key (TextBox password)
- Client ID (TextBox)
- Client Secret (TextBox password)
- URL do Endpoint (TextBox)
- Ativa (CheckBox)

**Ações:**
- `btnSalvar_Click()` - Salva credenciais criptografadas (AES-256)
- `btnTestarConexao_Click()` - Testa conectividade com operadora
- `btnExcluir_Click()` - Soft delete (Ativa = FALSE)

**Código VB.NET Relevante:**
```vb
Protected Sub btnSalvar_Click(sender As Object, e As EventArgs)
    Dim config As New OperadoraConfiguracao()
    config.ClienteId = Session("ClienteId")
    config.OperadoraId = ddlOperadora.SelectedValue
    config.ApiKey = CriptografiaHelper.Criptografar(txtApiKey.Text)
    config.ClientId = CriptografiaHelper.Criptografar(txtClientId.Text)
    config.ClientSecret = CriptografiaHelper.Criptografar(txtClientSecret.Text)
    config.EndpointUrl = txtEndpoint.Text
    config.Ativa = chkAtiva.Checked

    OperadoraDAO.Salvar(config)
    MostrarMensagem("Configuração salva com sucesso")
End Sub
```

**Substituído por:** `/admin/integracoes/apis-externas` (Angular 19)

---

### 2.2 ConsultaConsumo.aspx

**Localização:** `D:\IC2\ic1_legado\IControlIT\Integracao\ConsultaConsumo.aspx`

**Funcionalidade:** Consultar consumo de voz, dados e SMS de linhas.

**Campos:**
- Operadora (dropdown)
- MSISDN (TextBox - número da linha)
- Período (DateRange)

**GridView:**
- MSISDN
- Voz (minutos)
- Dados (MB)
- SMS (unidades)
- Última Atualização

**Código VB.NET:**
```vb
Protected Sub btnConsultar_Click(sender As Object, e As EventArgs)
    Dim wsOperadora As New WSOperadora()
    Dim resultado = wsOperadora.ConsultarConsumo(ddlOperadora.SelectedValue, txtMSISDN.Text)

    ' Sem cache - consulta direta sempre
    gvConsumo.DataSource = resultado
    gvConsumo.DataBind()
End Sub
```

**Problema:** SEM cache → cada consulta = chamada à API (lento, custoso).

**Substituído por:** `/integracoes/apis/consumo` com cache Redis (15 min TTL).

---

### 2.3 GestaoFaturas.aspx

**Localização:** `D:\IC2\ic1_legado\IControlIT\Integracao\GestaoFaturas.aspx`

**Funcionalidade:** Listar faturas importadas e importar manualmente via upload.

**Upload Manual:**
- FileUpload control (aceita .xml)
- Validação de schema XML NF-e
- Armazenamento em `\\servidor\faturas\operadora\ano\mes\`

**Código VB.NET:**
```vb
Protected Sub btnImportar_Click(sender As Object, e As EventArgs)
    If fuFatura.HasFile Then
        Dim xml = fuFatura.FileContent
        Dim nfeId = ExtrairNFeId(xml)

        ' Armazena em pasta local
        Dim caminhoArquivo = $"\\servidor\faturas\{oper}\{ano}\{mes}\{nfeId}.xml"
        File.WriteAllText(caminhoArquivo, xml)

        ' Registra no banco
        FaturaDAO.Inserir(clienteId, operadoraId, nfeId, caminhoArquivo)
    End If
End Sub
```

**Problema:** Armazenamento local sem backup, vulnerável a falhas de disco.

**Substituído por:** Azure Blob Storage com criptografia AES-256.

---

## 3. WEBSERVICES LEGADOS (ASMX)

### 3.1 WSOperadora.asmx

**Localização:** `D:\IC2\ic1_legado\WebService\WSOperadora.asmx.vb`

**Métodos SOAP:**

#### 3.1.1 ConsultarConsumo

```vb
<WebMethod()> _
Public Function ConsultarConsumo(operadoraId As Integer, msisdn As String) As ConsumoDto
    Dim config = OperadoraDAO.ObterPorId(operadoraId)
    Dim client As New HttpClient()
    client.DefaultRequestHeaders.Add("Authorization", $"Bearer {config.ApiKey}")

    Dim url = $"{config.EndpointUrl}/api/consumo?msisdn={msisdn}"
    Dim response = client.GetAsync(url).Result

    If response.IsSuccessStatusCode Then
        Dim json = response.Content.ReadAsStringAsync().Result
        Return JsonConvert.DeserializeObject(Of ConsumoDto)(json)
    Else
        Throw New Exception("Erro ao consultar operadora")
    End If
End Function
```

**Problemas:**
- Sem retry automático
- Sem timeout configurável
- Sem cache
- Bloqueante (GetAsync().Result)

**Substituído por:** `OperadoraHttpClient` com Polly (retry + circuit breaker + cache).

---

#### 3.1.2 ImportarFatura

```vb
<WebMethod()> _
Public Function ImportarFatura(operadoraId As Integer, nfeXml As String) As Boolean
    Dim nfeId = ExtrairNFeId(nfeXml)
    Dim caminhoArquivo = $"\\servidor\faturas\{operadoraId}\{nfeId}.xml"

    File.WriteAllText(caminhoArquivo, nfeXml)
    FaturaDAO.Inserir(Session("ClienteId"), operadoraId, nfeId, caminhoArquivo)

    Return True
End Function
```

**Problema:** Sem validação de duplicidade, sem armazenamento distribuído.

**Substituído por:** `FaturaArmazenamentoService` + Azure Blob Storage.

---

#### 3.1.3 ListarInventario

```vb
<WebMethod()> _
Public Function ListarInventario(operadoraId As Integer) As List(Of LinhaDto)
    Dim config = OperadoraDAO.ObterPorId(operadoraId)
    Dim client As New HttpClient()
    client.DefaultRequestHeaders.Add("Authorization", $"Bearer {config.ApiKey}")

    Dim url = $"{config.EndpointUrl}/api/inventario"
    Dim response = client.GetAsync(url).Result

    If response.IsSuccessStatusCode Then
        Dim json = response.Content.ReadAsStringAsync().Result
        Return JsonConvert.DeserializeObject(Of List(Of LinhaDto))(json)
    Else
        Return New List(Of LinhaDto)()
    End If
End Function
```

**Problema:** Retorna lista vazia em erro (silencioso), sem auditoria.

**Substituído por:** `InventarioService` com tratamento de erros e logging estruturado.

---

## 4. BANCO DE DADOS LEGADO

### 4.1 Tabela: ConfiguracaoOperadora

```sql
CREATE TABLE [dbo].[ConfiguracaoOperadora](
    [ID_Configuracao] [int] IDENTITY(1,1) NOT NULL,
    [ID_Cliente] [int] NOT NULL,
    [ID_Operadora] [int] NOT NULL,
    [ApiKey] [varchar](500) NOT NULL, -- Criptografado AES-256
    [ClienteId] [varchar](100) NULL, -- OAuth Client ID
    [ClienteSecret] [varchar](500) NULL, -- OAuth Client Secret
    [UrlEndpoint] [varchar](500) NOT NULL,
    [DataCriacao] [datetime] NOT NULL,
    [DataAtualizacao] [datetime] NULL,
    [Ativa] [bit] NOT NULL,
    CONSTRAINT [PK_ConfiguracaoOperadora] PRIMARY KEY CLUSTERED ([ID_Configuracao] ASC)
);
```

**Campos Relevantes:**
- `ID_Cliente` → Multi-tenancy
- `ApiKey`, `ClienteId`, `ClienteSecret` → Criptografados
- `UrlEndpoint` → URL base da API da operadora

**Migração:**
- Tabela equivalente: `IntegracaoApiExterna` no schema moderno
- Adicionar campos: `TipoAutenticacao`, `RetryMaximo`, `TimeoutSegundos`, `CacheTTL`

---

### 4.2 Tabela: FaturasOperadora

```sql
CREATE TABLE [dbo].[FaturasOperadora](
    [ID_Fatura] [int] IDENTITY(1,1) NOT NULL,
    [ID_Cliente] [int] NOT NULL,
    [ID_Operadora] [int] NOT NULL,
    [NumeroNota] [varchar](50) NOT NULL,
    [XMLFatura] [text] NOT NULL, -- ❌ Armazenado no banco (pesado)
    [DataEmissao] [datetime] NOT NULL,
    [Valor] [decimal](12,2) NOT NULL,
    [UrlArmazenamento] [varchar](500) NULL,
    [DataCarregamento] [datetime] NOT NULL,
    CONSTRAINT [PK_FaturasOperadora] PRIMARY KEY CLUSTERED ([ID_Fatura] ASC)
);
```

**Problema:** Coluna `XMLFatura [text]` armazena XML completo no banco (pode ter MBs), causando:
- Lentidão em queries
- Backup pesado
- Sem versionamento

**Migração:**
- Mover XMLs para Azure Blob Storage
- Substituir `XMLFatura` por `BlobStoragePath` (string)
- Adicionar `XMLHash` (SHA-256) para integridade

---

### 4.3 Tabela: LinhasTelefonicas

```sql
CREATE TABLE [dbo].[LinhasTelefonicas](
    [ID_Linha] [int] IDENTITY(1,1) NOT NULL,
    [ID_Cliente] [int] NOT NULL,
    [ID_Operadora] [int] NOT NULL,
    [MSISDN] [varchar](20) NOT NULL,
    [IMSI] [varchar](15) NULL,
    [Estado] [varchar](20) NOT NULL, -- ativa, bloqueada, suspensa, inativa
    [Plano] [varchar](100) NULL,
    [DataAquisicao] [datetime] NOT NULL,
    [DataAtualizacao] [datetime] NULL,
    CONSTRAINT [PK_LinhasTelefonicas] PRIMARY KEY CLUSTERED ([ID_Linha] ASC)
);
```

**Migração:**
- Equivalente: Tabela `LinhasTelefonia` no schema moderno
- Adicionar: `DataSincronizacao`, `UltimaConsultaConsumo`

---

### 4.4 Stored Procedure: pa_ConsultarConsumoLinha

```sql
CREATE PROCEDURE [dbo].[pa_ConsultarConsumoLinha]
    @ClienteId INT,
    @MSISDN VARCHAR(20)
AS
BEGIN
    SELECT TOP 1
        Voz,
        Dados,
        SMS,
        DataConsulta
    FROM ConsumoLinhas c
    INNER JOIN LinhasTelefonicas l ON c.ID_Linha = l.ID_Linha
    WHERE l.ID_Cliente = @ClienteId
      AND l.MSISDN = @MSISDN
    ORDER BY DataConsulta DESC
END
```

**Substituído por:** Query EF Core no `ConsumoService`.

---

### 4.5 Stored Procedure: pa_SincronizarInventario

```sql
CREATE PROCEDURE [dbo].[pa_SincronizarInventario]
    @ClienteId INT,
    @OperadoraId INT
AS
BEGIN
    -- 1. Marca linhas atuais como desatualizadas
    UPDATE LinhasTelefonicas
    SET Estado = 'desatualizado'
    WHERE ID_Cliente = @ClienteId AND ID_Operadora = @OperadoraId;

    -- 2. Insere novas linhas (executado manualmente após consulta API)
    -- 3. Marca linhas que não existem mais como 'inativa'
END
```

**Problema:** Sincronização manual, dependente de job VB.NET externo.

**Substituído por:** `SincronizacaoOperadoraJob` (Hangfire) com execução automática às 3h AM.

---

## 5. HELPERS E UTILITÁRIOS LEGADOS

### 5.1 CriptografiaHelper.vb

```vb
Public Class CriptografiaHelper
    Private Shared ReadOnly ChaveMestra As String = "ChaveSecretaIControlIT2024"
    Private Shared ReadOnly IV As String = "IVFixo123456"

    Public Shared Function Criptografar(texto As String) As String
        Using aes As Aes = Aes.Create()
            aes.Key = Encoding.UTF8.GetBytes(ChaveMestra.PadRight(32).Substring(0, 32))
            aes.IV = Encoding.UTF8.GetBytes(IV.PadRight(16).Substring(0, 16))

            Using encryptor = aes.CreateEncryptor()
            Using ms As New MemoryStream()
            Using cs As New CryptoStream(ms, encryptor, CryptoStreamMode.Write)
                Dim bytes = Encoding.UTF8.GetBytes(texto)
                cs.Write(bytes, 0, bytes.Length)
                cs.FlushFinalBlock()
                Return Convert.ToBase64String(ms.ToArray())
            End Using
            End Using
            End Using
        End Using
    End Function

    Public Shared Function Descriptografar(textoCriptografado As String) As String
        ' Implementação análoga
    End Function
End Class
```

**Problemas:**
- Chave mestra hardcoded (inseguro)
- IV fixo (vulnerável a ataques)

**Substituído por:** Azure Key Vault + `CredentialEncryptionService` com IV aleatório.

---

### 5.2 OperadoraDAO.vb

```vb
Public Class OperadoraDAO
    Public Shared Function ObterPorId(clienteId As Integer, operadoraId As Integer) As OperadoraConfiguracao
        Using conn As New SqlConnection(ConfigurationManager.ConnectionStrings("IC1").ConnectionString)
            Dim cmd As New SqlCommand("SELECT * FROM ConfiguracaoOperadora WHERE ID_Cliente = @ClienteId AND ID_Operadora = @OperadoraId AND Ativa = 1", conn)
            cmd.Parameters.AddWithValue("@ClienteId", clienteId)
            cmd.Parameters.AddWithValue("@OperadoraId", operadoraId)

            conn.Open()
            Dim reader = cmd.ExecuteReader()

            If reader.Read() Then
                Return New OperadoraConfiguracao() With {
                    .Id = reader("ID_Configuracao"),
                    .ClienteId = reader("ID_Cliente"),
                    .OperadoraId = reader("ID_Operadora"),
                    .ApiKey = CriptografiaHelper.Descriptografar(reader("ApiKey")),
                    .EndpointUrl = reader("UrlEndpoint")
                }
            Else
                Return Nothing
            End If
        End Using
    End Function
End Class
```

**Substituído por:** `OperadoraRepository` com EF Core + LINQ.

---

## 6. JOBS E SINCRONIZAÇÕES LEGADAS

### 6.1 SincronizacaoJob.vb (Task Scheduler)

**Executado via:** Windows Task Scheduler (agendado para 3:00 AM).

**Código VB.NET:**
```vb
Sub Main()
    Dim clientes = ClienteDAO.ListarTodos()

    For Each cliente In clientes
        Dim operadoras = OperadoraDAO.ListarPorCliente(cliente.Id)

        For Each operadora In operadoras
            Try
                Console.WriteLine($"Sincronizando {operadora.Nome} para {cliente.Nome}")

                ' 1. Sincroniza faturas
                SincronizarFaturas(cliente.Id, operadora.Id)

                ' 2. Sincroniza consumo
                SincronizarConsumo(cliente.Id, operadora.Id)

                ' 3. Sincroniza inventário
                SincronizarInventario(cliente.Id, operadora.Id)

                Console.WriteLine($"OK: {operadora.Nome}")
            Catch ex As Exception
                Console.WriteLine($"ERRO: {operadora.Nome} - {ex.Message}")
                ' ❌ Sem registro de auditoria
            End Try
        Next
    Next
End Sub
```

**Problemas:**
- Task Scheduler sem monitoramento (falhas silenciosas)
- Sem retry automático
- Sem auditoria de execução

**Substituído por:** Hangfire com job recorrente + dashboard de monitoramento.

---

## 7. RASTREABILIDADE DE DESTINOS

### 7.1 Telas ASPX

| Tela Legado | Destino | Justificativa |
|-------------|---------|---------------|
| `GestaoOperadoras.aspx` | **SUBSTITUÍDO** | `/admin/integracoes/apis-externas` (Angular 19) |
| `ConsultaConsumo.aspx` | **SUBSTITUÍDO** | `/integracoes/apis/consumo` com cache Redis |
| `GestaoFaturas.aspx` | **SUBSTITUÍDO** | `/integracoes/faturas` com Blob Storage |

---

### 7.2 WebServices ASMX

| WebMethod Legado | Destino | Justificativa |
|------------------|---------|---------------|
| `ConsultarConsumo()` | **SUBSTITUÍDO** | `POST /api/integracoes/apis-externas/{id}/execute` (REST API) |
| `ImportarFatura()` | **SUBSTITUÍDO** | Azure Function + Blob Storage Trigger |
| `ListarInventario()` | **SUBSTITUÍDO** | `GET /api/integracoes/apis-externas/{id}/metrics` |

---

### 7.3 Banco de Dados

| Tabela Legado | Destino | Justificativa |
|---------------|---------|---------------|
| `ConfiguracaoOperadora` | **ASSUMIDO** | Migrado para `IntegracaoApiExterna` com novos campos (retry, timeout, cache) |
| `FaturasOperadora.XMLFatura` | **DESCARTADO** | XMLs movidos para Azure Blob Storage, mantém apenas hash |
| `LinhasTelefonicas` | **ASSUMIDO** | Equivalente moderno: `LinhasTelefonia` |
| `ConsumoLinhas` | **DESCARTADO** | Dados consumo armazenados em Redis (cache volátil) |

---

### 7.4 Helpers e Utilitários

| Helper Legado | Destino | Justificativa |
|---------------|---------|---------------|
| `CriptografiaHelper.vb` | **SUBSTITUÍDO** | Azure Key Vault + `CredentialEncryptionService` |
| `OperadoraDAO.vb` | **SUBSTITUÍDO** | EF Core + Repository Pattern |
| `SincronizacaoJob.vb` | **SUBSTITUÍDO** | Hangfire RecurringJob |

---

### 7.5 Regras de Negócio

| Regra Legado | Destino | Justificativa |
|--------------|---------|---------------|
| Criptografia AES-256 de credenciais | **ASSUMIDO** | Mantido, mas com chave em Key Vault |
| Timeout 30s para consultas | **ASSUMIDO** | Configurável por API (5-300s) |
| Retry manual em falhas | **SUBSTITUÍDO** | Polly com retry exponencial automático |
| Armazenamento local de XMLs | **SUBSTITUÍDO** | Azure Blob Storage com durabilidade 99.999999999% |
| Sincronização manual às 3h AM | **ASSUMIDO** | Hangfire RecurringJob (automático) |
| Sem validação de webhook | **SUBSTITUÍDO** | HMAC-SHA256 obrigatório |
| Sem cache de consumo | **SUBSTITUÍDO** | Redis com TTL 15 minutos |
| Sem circuit breaker | **SUBSTITUÍDO** | Polly CircuitBreaker (5 falhas → bloqueio 5 min) |

---

## 8. LIÇÕES APRENDIDAS DO LEGADO

### 8.1 O que FUNCIONAVA

- ✅ Criptografia AES-256 de credenciais
- ✅ Multi-tenancy com ClienteId
- ✅ Soft delete (Ativa = FALSE)
- ✅ Auditoria de usuário (CriadoPorUsuarioId)

### 8.2 O que NÃO funcionava

- ❌ Armazenamento local (risco de perda de dados)
- ❌ Sem cache (latência alta, custo alto)
- ❌ Sem retry automático (baixa resiliência)
- ❌ Sem circuit breaker (sobrecarga em falhas)
- ❌ Sem validação de webhook (inseguro)
- ❌ Jobs manuais via Task Scheduler (falhas silenciosas)
- ❌ Chave mestra hardcoded (vulnerável)

### 8.3 Melhorias Críticas no Modernizado

1. **Azure Blob Storage** (durabilidade, backup, compliance)
2. **Redis Cache** (latência < 50ms, economia de custos)
3. **Polly Retry + Circuit Breaker** (resiliência automática)
4. **HMAC-SHA256 para Webhooks** (segurança)
5. **Hangfire** (monitoramento, retry, dashboard)
6. **Azure Key Vault** (chaves rotacionáveis, auditadas)
7. **Timeout configurável** (adaptável por API)
8. **Métricas em tempo real** (latência P95, taxa de erro)

---

## 9. REFERÊNCIAS CRUZADAS

### 9.1 Arquivos Legados Relevantes

```
D:\IC2\ic1_legado\IControlIT\
├── Integracao/
│   ├── GestaoOperadoras.aspx
│   ├── GestaoOperadoras.aspx.vb
│   ├── ConsultaConsumo.aspx
│   ├── ConsultaConsumo.aspx.vb
│   ├── GestaoFaturas.aspx
│   └── GestaoFaturas.aspx.vb
├── WebService/
│   ├── WSOperadora.asmx
│   └── WSOperadora.asmx.vb
├── Helpers/
│   ├── CriptografiaHelper.vb
│   └── OperadoraDAO.vb
└── Jobs/
    └── SincronizacaoJob.vb
```

### 9.2 Scripts SQL Legados

```
D:\IC2\ic1_legado\Database\
├── Schema/
│   ├── ConfiguracaoOperadora.sql
│   ├── FaturasOperadora.sql
│   ├── LinhasTelefonicas.sql
│   └── ConsumoLinhas.sql
└── StoredProcedures/
    ├── pa_ConsultarConsumoLinha.sql
    ├── pa_SincronizarInventario.sql
    └── pa_ImportarFatura.sql
```

---

## 10. CONCLUSÃO

Este documento preserva a memória técnica do módulo legado de integração com operadoras. Ele **NÃO define** o comportamento do sistema modernizado, servindo apenas como:

1. **Referência histórica** para entender decisões de arquitetura
2. **Lições aprendidas** para evitar erros do passado
3. **Rastreabilidade** de funcionalidades migradas vs. descartadas
4. **Contexto** para desenvolvedores que precisam entender o sistema antigo

**Para implementação moderna, consulte:** `RF105.md` e `RF105.yaml`

---

**Última Atualização**: 2025-12-31
**Autor**: IControlIT Architect Agent
**Status**: Memória Histórica Completa

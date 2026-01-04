# RL-RF085: Referência ao Legado - Importação de Dados

**Versão**: 2.0
**Data**: 2025-12-31
**RF Relacionado**: RF085 - Importação de Dados
**EPIC**: EPIC003-CAD-Cadastros-Base
**Fase**: Fase 2 - Cadastros e Serviços Transversais

---

## 1. CONTEXTO DO SISTEMA LEGADO

### 1.1 Stack Tecnológica

| Componente | Tecnologia |
|------------|------------|
| **Frontend** | ASP.NET Web Forms (ASPX) + VB.NET Code-Behind |
| **Backend** | VB.NET + WebServices (.asmx) |
| **Banco de Dados** | SQL Server (múltiplos bancos por cliente) |
| **Arquitetura** | Monolito 3-camadas (UI → Business → Data) |
| **Deployment** | IIS + Task Scheduler Windows |

### 1.2 Arquitetura Geral

O sistema legado de importação de dados operava em arquitetura monolítica com as seguintes características:

- **Multi-Database**: Cada cliente possuía banco SQL Server separado (`IControlIT_Cliente01`, `IControlIT_Cliente02`, etc.)
- **Estado em Sessão**: Dados temporários de importação armazenados em Session do ASP.NET
- **Processamento Síncrono**: Importações executadas de forma bloqueante na thread da requisição HTTP
- **Arquivos em Disco Local**: Uploads salvos em pasta física do servidor IIS (`D:\Uploads\`)
- **Agendamento via Task Scheduler**: Jobs Windows agendados que executavam scripts SQL diretamente

### 1.3 Problemas Arquiteturais Identificados

| Problema | Severidade | Impacto |
|----------|-----------|---------|
| **Timeout em Importações Grandes** | CRÍTICA | Importações > 10.000 registros causavam timeout HTTP (300 segundos), perdendo todo o processamento |
| **Falta de Validação Estruturada** | ALTA | Validações hard-coded em VB.NET sem possibilidade de configuração por template |
| **Nenhuma Detecção de Duplicatas** | ALTA | Registros duplicados inseridos sem aviso, causando inconsistências no banco |
| **Histórico Rudimentar** | MÉDIA | Apenas log em arquivo texto, sem capacidade de rollback ou análise detalhada |
| **Sem Transformação de Dados** | MÉDIA | Conversões de tipo feitas manualmente em Stored Procedures, difíceis de manter |
| **Concorrência Bloqueada** | MÉDIA | Apenas 1 importação por vez, causando fila de espera para usuários |
| **Erro 500 Genérico** | BAIXA | Erros de validação retornavam apenas "Erro ao importar", sem detalhes |

---

## 2. TELAS ASPX E CÓDIGO-BEHIND

### Item LEG-RF085-001: ImportacaoDados.aspx

**Caminho Legado**: `D:\IC2\ic1_legado\IControlIT\Importacao\ImportacaoDados.aspx`

**Funcionalidades Principais**:
- Upload de arquivo CSV ou XLS via `<asp:FileUpload>`
- Seleção de tipo de importação via `<asp:DropDownList>` (Clientes, Fornecedores, Ativos, Faturas)
- Botão "Importar" que executa processamento síncrono
- Grid com resultado mostrando total de registros, sucessos e erros

**Regras Implícitas no Code-Behind (VB.NET)**:
- Arquivo limitado a 50MB (hard-coded em `If FileUpload1.PostedFile.ContentLength > 52428800`)
- Apenas extensões `.csv` e `.xls` permitidas (validação via `Path.GetExtension()`)
- Importação executada na thread da requisição (sem async/await)
- Resultado salvo em Session["UltimaImportacao"] para exibir em modal

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Tela completamente redesenhada em Angular 19 com componentes standalone, upload drag-and-drop, validação assíncrona e preview antes de confirmar.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 2 (Funcionalidades F01, F11)
- **UC Moderno**: UC02-RF085 (Executar importação manual)

**Migração Moderna**:
- **Componente Angular**: `imports-create.component.ts`
- **Rota Frontend**: `/configuracoes/importacao/manual`
- **Validação**: Executada em preview antes de persistir

---

### Item LEG-RF085-002: ListaImportacoes.aspx

**Caminho Legado**: `D:\IC2\ic1_legado\IControlIT\Importacao\ListaImportacoes.aspx`

**Funcionalidades Principais**:
- Grid `<asp:GridView>` listando histórico de importações
- Filtros por data e tipo de importação
- Link "Ver Erros" que abre popup com detalhes

**Regras Implícitas no Code-Behind**:
- Consulta SQL direta: `SELECT * FROM tb_ImportacaoDados WHERE Id_Cliente = @ClienteId ORDER BY Data_Importacao DESC`
- Paginação server-side com 50 registros por página
- Sem ordenação customizada (sempre por Data_Importacao DESC)

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Lista moderna com Angular Material Table, paginação client-side, ordenação por qualquer coluna, filtros avançados.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 2 (Funcionalidade F08)
- **UC Moderno**: UC03-RF085 (Visualizar histórico)

**Migração Moderna**:
- **Componente Angular**: `imports-history.component.ts`
- **Rota Frontend**: `/configuracoes/importacao/historico`
- **API**: `GET /api/imports/history`

---

### Item LEG-RF085-003: DetalheImportacao.aspx

**Caminho Legado**: `D:\IC2\ic1_legado\IControlIT\Importacao\DetalheImportacao.aspx`

**Funcionalidades Principais**:
- Detalhes de uma importação específica (ID, usuário, timestamp, status)
- Grid com erros linha a linha (número da linha, campo com erro, descrição)
- Botão "Desfazer Importação" (executa stored procedure de rollback)

**Regras Implícitas no Code-Behind**:
- Rollback via `sp_DesfazerImportacao` que deleta registros por importação
- Sem validação de tempo (rollback permitido mesmo após meses)
- Nenhuma confirmação adicional (botão direto executa DELETE)

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Tela moderna com tabs (Resumo, Erros, Logs), confirmação antes de rollback, validação de tempo máximo para reversão.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 2 (Funcionalidades F08, F09, F10)
- **UC Moderno**: UC03-RF085 (Visualizar histórico com detalhes)

**Migração Moderna**:
- **Componente Angular**: `imports-detail.component.ts`
- **Rota Frontend**: `/configuracoes/importacao/{id}`
- **API**: `GET /api/imports/{id}`, `POST /api/imports/{id}/rollback`

---

### Item LEG-RF085-004: ConfiguracaoImportacao.aspx

**Caminho Legado**: `D:\IC2\ic1_legado\IControlIT\Importacao\ConfiguracaoImportacao.aspx`

**Funcionalidades Principais**:
- Configuração rudimentar de mapeamento de colunas
- Grid editável com: Coluna Origem → Campo Destino
- Sem suporte a transformações ou validações customizadas

**Regras Implícitas no Code-Behind**:
- Mapeamento salvo em tabela `tb_ConfiguracaoImportacao` como XML
- Nenhuma validação de tipo de dados (string para tudo)
- Sem preview de como mapeamento será aplicado

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Sistema moderno de templates com editor visual, suporte a transformações (UPPER, TRIM, FORMAT_DATE), validações regex e preview em tempo real.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 2 (Funcionalidade F01)
- **UC Moderno**: UC01-RF085 (Criar/editar template)

**Migração Moderna**:
- **Componente Angular**: `import-template-form.component.ts`
- **Rota Frontend**: `/configuracoes/importacao/templates`
- **API**: `POST /api/imports/templates`, `PUT /api/imports/templates/{id}`

---

## 3. WEBSERVICES (.asmx)

### Item LEG-RF085-005: WSImportacao.asmx

**Caminho Legado**: `D:\IC2\ic1_legado\IControlIT\WebService\WSImportacao.asmx.vb`

**Métodos Públicos**:

#### `ImportarArquivo(arquivo As Byte(), tipo As String) As Integer`

**Parâmetros**:
- `arquivo`: Byte array do arquivo CSV/XLS
- `tipo`: String ("Clientes", "Fornecedores", "Ativos", "Faturas")

**Retorno**: ID da importação criada ou -1 em caso de erro

**Lógica Principal**:
- Salva arquivo temporário em disco (`D:\Temp\upload_GUID.csv`)
- Chama stored procedure `sp_ImportarClientes` ou `sp_ImportarFornecedores` conforme tipo
- Registra resultado em `tb_ImportacaoDados`
- Deleta arquivo temporário

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Substituído por REST API moderna com autenticação JWT, upload via multipart/form-data, processamento assíncrono em Hangfire.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `POST /api/imports`

**Migração Moderna**:
- **Command CQRS**: `ExecuteImportCommand`
- **Handler**: `ExecuteImportCommandHandler`
- **Validação**: `ExecuteImportCommandValidator`

---

#### `ListarImportacoes(clienteId As Integer) As DataTable`

**Parâmetros**:
- `clienteId`: ID do cliente para filtrar importações

**Retorno**: DataTable com colunas: Id_Importacao, Nm_Arquivo, Data_Importacao, Status_Importacao

**Lógica Principal**:
- Query SQL direta: `SELECT * FROM tb_ImportacaoDados WHERE Id_Cliente = @clienteId`
- Sem paginação (retorna todas as linhas)

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Substituído por Query CQRS com paginação, filtros e ordenação.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `GET /api/imports/history`

**Migração Moderna**:
- **Query CQRS**: `GetImportHistoryQuery`
- **Handler**: `GetImportHistoryQueryHandler`

---

#### `DesfazerImportacao(idImportacao As Integer) As Boolean`

**Parâmetros**:
- `idImportacao`: ID da importação a ser revertida

**Retorno**: True se sucesso, False se falha

**Lógica Principal**:
- Executa stored procedure `sp_DesfazerImportacao @Id_Importacao = idImportacao`
- Procedure deleta registros inseridos pela importação
- Nenhuma validação de tempo ou estado

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Substituído por endpoint REST com validação de CanRollback, transação e auditoria completa.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `POST /api/imports/{id}/rollback`

**Migração Moderna**:
- **Command CQRS**: `RollbackImportCommand`
- **Handler**: `RollbackImportCommandHandler`

---

#### `ValidarMapeamento(templateId As Integer, primeirasLinhas As DataTable) As DataTable`

**Parâmetros**:
- `templateId`: ID do template de mapeamento
- `primeirasLinhas`: DataTable com primeiras 10 linhas do arquivo

**Retorno**: DataTable com colunas: Linha, Campo, Valor, Status (OK/ERRO)

**Lógica Principal**:
- Carrega mapeamento da tabela `tb_ConfiguracaoImportacao`
- Aplica conversões básicas de tipo (string → int, string → decimal)
- Valida campos obrigatórios

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Substituído por endpoint de preview com validações multi-camadas, transformações configuráveis e sugestões de correção.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `POST /api/imports/preview`

**Migração Moderna**:
- **Command CQRS**: `PreviewImportCommand`
- **Handler**: `PreviewImportCommandHandler`

---

#### `ObterErrosImportacao(idImportacao As Integer) As DataTable`

**Parâmetros**:
- `idImportacao`: ID da importação

**Retorno**: DataTable com erros: Numero_Linha, Campo_Erro, Descricao_Erro

**Lógica Principal**:
- Query SQL: `SELECT * FROM tb_ImportacaoDados_Detalhe WHERE Id_Importacao = @id AND Status_Linha = 'ERRO'`
- Sem sugestões de correção

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Substituído por endpoint que retorna relatório detalhado com sugestões automáticas de correção.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `GET /api/imports/{id}/errors`

**Migração Moderna**:
- **Query CQRS**: `GetImportErrorsQuery`
- **Handler**: `GetImportErrorsQueryHandler`

---

## 4. STORED PROCEDURES

### Item LEG-RF085-006: sp_ImportarClientes

**Caminho Legado**: `D:\IC2\ic1_legado\Database\Procedures\sp_ImportarClientes.sql`

**Parâmetros de Entrada**:
```sql
@Id_Cliente INT,
@Caminho_Arquivo VARCHAR(500),
@Id_Usuario INT
```

**Parâmetros de Saída**:
```sql
@Total_Registros INT OUTPUT,
@Registros_Sucesso INT OUTPUT,
@Registros_Erro INT OUTPUT
```

**Lógica Principal** (em linguagem natural):

1. Cria tabela temporária `#TempImportacao` para armazenar dados do CSV
2. Usa BULK INSERT para carregar arquivo CSV na tabela temporária
3. Para cada linha da tabela temporária:
   - Valida se CPF/CNPJ já existe em `tb_Clientes`
   - Se não existe: INSERT na `tb_Clientes`
   - Se existe: Ignora silenciosamente (nenhum UPDATE ou erro)
4. Registra resultado em `tb_ImportacaoDados`
5. Registra linhas com erro em `tb_ImportacaoDados_Detalhe`
6. Deleta arquivo do disco

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Lógica movida para Application Layer (CQRS Handler) com suporte a múltiplas estratégias de duplicata (IGNORE, REPLACE, REJECT), validações configuráveis e transformações.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (Regras de Negócio RN-RF085-001 a RN-RF085-004)
- **Regra Moderna**: RN-RF085-004 (Detecção de Duplicatas)

**Migração Moderna**:
- **Handler**: `ExecuteImportCommandHandler`
- **Validação**: `FluentValidation` + Custom Validators
- **Duplicatas**: `DuplicateDetector` class com múltiplas estratégias

---

### Item LEG-RF085-007: sp_ImportarFornecedores

**Caminho Legado**: `D:\IC2\ic1_legado\Database\Procedures\sp_ImportarFornecedores.sql`

**Parâmetros de Entrada**:
```sql
@Id_Cliente INT,
@Caminho_Arquivo VARCHAR(500),
@Id_Usuario INT
```

**Lógica Principal** (em linguagem natural):

- Similar a `sp_ImportarClientes` mas para tabela `tb_Fornecedores`
- Validação adicional: Verifica se `Tipo_Fornecedor` é válido ('Produto', 'Serviço', 'Ambos')
- Validação de email via regex hard-coded: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Validações movidas para `FluentValidation` com regras configuráveis por template.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-003)
- **Validador Moderno**: `FieldMapping.ValidationRule` (regex configurável)

**Migração Moderna**:
- **Validator**: `CreateFornecedorCommandValidator` com `RuleFor(x => x.Email).EmailAddress()`

---

### Item LEG-RF085-008: sp_ValidarDadosImportacao

**Caminho Legado**: `D:\IC2\ic1_legado\Database\Procedures\sp_ValidarDadosImportacao.sql`

**Parâmetros de Entrada**:
```sql
@Tabela_Temp VARCHAR(100), -- Nome da tabela temporária
@Tipo_Entidade VARCHAR(50) -- 'Cliente', 'Fornecedor', etc.
```

**Parâmetros de Saída**:
```sql
@Total_Erros INT OUTPUT
```

**Lógica Principal** (em linguagem natural):

- Valida campos obrigatórios (NOT NULL)
- Valida ranges (ex: valores numéricos >= 0)
- Valida foreign keys (ex: Id_Categoria existe em tb_Categorias)
- Insere erros em tabela temporária `#Erros`

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Pipeline de validação moderno com múltiplas camadas (estrutural, semântica, referencial, negócio).

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-003)
- **Validador Moderno**: `DataValidator` class

**Migração Moderna**:
- **Validator**: `FluentValidation` + `ValidationRule` entity
- **Pipeline**: Validação antes de qualquer INSERT (fail-fast)

---

### Item LEG-RF085-009: sp_DesfazerImportacao

**Caminho Legado**: `D:\IC2\ic1_legado\Database\Procedures\sp_DesfazerImportacao.sql`

**Parâmetros de Entrada**:
```sql
@Id_Importacao INT
```

**Lógica Principal** (em linguagem natural):

1. Verifica se importação existe e status é 'Sucesso'
2. Identifica tipo de importação (Cliente, Fornecedor, Ativo, Fatura)
3. Executa DELETE na tabela correspondente:
   ```sql
   DELETE FROM tb_Clientes
   WHERE Id IN (SELECT Id_Registro FROM tb_ImportacaoDados_Detalhe WHERE Id_Importacao = @Id_Importacao)
   ```
4. Atualiza `tb_ImportacaoDados` marcando importação como "Revertida"

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Rollback transacional moderno com backup dos dados deletados, validação de tempo máximo e auditoria completa.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-007)
- **Handler Moderno**: `RollbackImportCommandHandler`

**Migração Moderna**:
- **Handler**: `RollbackImportCommandHandler`
- **Validação**: `CanRollback` flag, validação de tempo
- **Auditoria**: Registro completo em `AuditLog`

---

### Item LEG-RF085-010: sp_ListarImportacoes

**Caminho Legado**: `D:\IC2\ic1_legado\Database\Procedures\sp_ListarImportacoes.sql`

**Parâmetros de Entrada**:
```sql
@Id_Cliente INT,
@Data_Inicio DATE,
@Data_Fim DATE
```

**Lógica Principal** (em linguagem natural):

- Query simples:
  ```sql
  SELECT * FROM tb_ImportacaoDados
  WHERE Id_Cliente = @Id_Cliente
    AND Data_Importacao BETWEEN @Data_Inicio AND @Data_Fim
  ORDER BY Data_Importacao DESC
  ```

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Query CQRS moderna com paginação, filtros dinâmicos e ordenação customizável.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 6 (API Endpoints)
- **Endpoint Moderno**: `GET /api/imports/history`

**Migração Moderna**:
- **Query**: `GetImportHistoryQuery` com `PaginationParams`
- **Handler**: `GetImportHistoryQueryHandler`

---

## 5. TABELAS LEGADAS

### Item LEG-RF085-011: tb_ImportacaoDados

**Schema Legado**: `[dbo].[tb_ImportacaoDados]`

**Estrutura**:
```sql
CREATE TABLE [dbo].[tb_ImportacaoDados](
    [Id_Importacao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Cliente] [int] NOT NULL,
    [Nm_Arquivo] [varchar](255) NOT NULL,
    [Caminho_Arquivo] [varchar](500) NULL,
    [Tipo_Importacao] [varchar](50) NOT NULL,
    [Data_Importacao] [datetime] NOT NULL,
    [Usuario_Importacao] [varchar](100) NOT NULL,
    [Total_Registros] [int] NOT NULL,
    [Registros_Sucesso] [int] NOT NULL,
    [Registros_Erro] [int] NOT NULL,
    [Status_Importacao] [varchar](20) NOT NULL,
    [Descricao_Erro] [varchar](max) NULL,
    [Fl_Ativo] [bit] NOT NULL DEFAULT 1,
    CONSTRAINT [PK_tb_ImportacaoDados] PRIMARY KEY CLUSTERED ([Id_Importacao] ASC)
)
```

**Problemas Identificados**:
- **Falta Foreign Key** para validar `Id_Cliente` existe em `tb_Clientes`
- **Tipo_Importacao** é string livre sem ENUM ou CHECK constraint (permite valores inválidos)
- **Usuario_Importacao** é VARCHAR sem FK para `tb_Usuarios` (inconsistência se usuário for deletado)
- **Caminho_Arquivo** expõe path físico do servidor (risco de segurança)
- **Sem auditoria**: Falta Created, CreatedBy, LastModified, LastModifiedBy

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Tabela redesenhada com multi-tenancy, auditoria, FKs obrigatórias e ENUMs tipados.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 7 (Modelo de Dados)
- **Tabela Moderna**: `Import`

**Migração Moderna**:
- **Entity**: `Import` class com FKs para `ImportTemplate`, `User`, `Cliente`
- **Migration EF Core**: `20251231_CreateImportTable.cs`
- **Auditoria**: `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy` (automático via interceptor)

---

### Item LEG-RF085-012: tb_ImportacaoDados_Detalhe

**Schema Legado**: `[dbo].[tb_ImportacaoDados_Detalhe]`

**Estrutura**:
```sql
CREATE TABLE [dbo].[tb_ImportacaoDados_Detalhe](
    [Id_Detalhe] [int] IDENTITY(1,1) NOT NULL,
    [Id_Importacao] [int] NOT NULL,
    [Numero_Linha] [int] NOT NULL,
    [Dados_Original] [varchar](max) NOT NULL,
    [Campo_Erro] [varchar](255) NULL,
    [Descricao_Erro] [varchar](max) NULL,
    [Status_Linha] [varchar](20) NOT NULL,
    CONSTRAINT [PK_tb_ImportacaoDados_Detalhe] PRIMARY KEY CLUSTERED ([Id_Detalhe] ASC),
    CONSTRAINT [FK_Detalhe_Importacao] FOREIGN KEY ([Id_Importacao]) REFERENCES [tb_ImportacaoDados]([Id_Importacao])
)
```

**Problemas Identificados**:
- **Dados_Original** armazena linha inteira como string (difícil de parsear depois)
- **Campo_Erro** só armazena 1 campo, mas linha pode ter múltiplos erros
- **Sem sugestão de correção**: Apenas descreve erro, não sugere como corrigir

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Tabela `ImportError` moderna com estrutura JSON para erros múltiplos, sugestões automáticas e categorização de erros.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 7 (Modelo de Dados)
- **Tabela Moderna**: `ImportError`

**Migração Moderna**:
- **Entity**: `ImportError` com campos `ErrorCode`, `FieldName`, `ActualValue`, `ExpectedFormat`, `Suggestion`
- **Migration**: `20251231_CreateImportErrorTable.cs`

---

### Item LEG-RF085-013: tb_ConfiguracaoImportacao

**Schema Legado**: `[dbo].[tb_ConfiguracaoImportacao]`

**Estrutura**:
```sql
CREATE TABLE [dbo].[tb_ConfiguracaoImportacao](
    [Id_Configuracao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Cliente] [int] NOT NULL,
    [Tipo_Importacao] [varchar](50) NOT NULL,
    [Xml_Mapeamento] [xml] NOT NULL,
    [Data_Criacao] [datetime] NOT NULL,
    [Usuario_Criacao] [varchar](100) NOT NULL,
    CONSTRAINT [PK_tb_ConfiguracaoImportacao] PRIMARY KEY CLUSTERED ([Id_Configuracao] ASC)
)
```

**Problemas Identificados**:
- **Xml_Mapeamento**: Difícil de query e validar (estrutura livre em XML)
- **Sem versionamento**: Alterações no mapeamento sobrescrevem configuração anterior
- **Sem transformações**: XML só mapeia coluna → campo, sem suporte a UPPER, TRIM, etc.

**DESTINO**: SUBSTITUÍDO

**Justificativa**: Tabelas `ImportTemplate` e `FieldMapping` modernas com estrutura relacional normalizada, suporte a transformações e validações.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 7 (Modelo de Dados)
- **Tabelas Modernas**: `ImportTemplate`, `FieldMapping`, `ValidationRule`

**Migração Moderna**:
- **Entities**: `ImportTemplate` (1) → (N) `FieldMapping`, (1) → (N) `ValidationRule`
- **Migration**: `20251231_CreateImportTemplateTable.cs`

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### Item LEG-RF085-014: Limite de Tamanho de Arquivo (Hard-coded)

**Localização no Código**: `ImportacaoDados.aspx.vb - Linha 47`

**Código VB.NET**:
```vb
If FileUpload1.PostedFile.ContentLength > 52428800 Then
    lblErro.Text = "Arquivo muito grande. Máximo: 50MB"
    Return
End If
```

**Regra Extraída** (linguagem natural):
- Arquivos de importação devem ter no máximo 50MB
- Se arquivo for maior, importação é rejeitada com erro "Arquivo muito grande"

**DESTINO**: ASSUMIDO

**Justificativa**: Regra mantida no sistema moderno mas configurável via `SistemaConfiguracaoGeral` (não mais hard-coded).

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-012)
- **Regra Moderna**: RN-RF085-012 (Validação de Tamanho e Tipo de Arquivo)

**Migração Moderna**:
- **Configuração**: `MaxFileSizeImportacaoMB` em `appsettings.json` (padrão: 500MB)
- **Validação**: `ExecuteImportCommandValidator` com `RuleFor(x => x.File.Length).LessThanOrEqualTo(maxSize)`

---

### Item LEG-RF085-015: Extensões Permitidas (Whitelist)

**Localização no Código**: `ImportacaoDados.aspx.vb - Linha 52`

**Código VB.NET**:
```vb
Dim extensao As String = Path.GetExtension(FileUpload1.FileName).ToLower()
If extensao <> ".csv" And extensao <> ".xls" Then
    lblErro.Text = "Apenas arquivos CSV ou XLS são permitidos"
    Return
End If
```

**Regra Extraída**:
- Apenas arquivos com extensão `.csv` ou `.xls` são aceitos
- Outras extensões são rejeitadas com erro

**DESTINO**: ASSUMIDO (com expansão)

**Justificativa**: Regra mantida mas expandida para suportar `.xlsx`, `.xml`, `.json`, `.edi`.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-012)
- **Regra Moderna**: RN-RF085-012 (Validação de Tamanho e Tipo de Arquivo)

**Migração Moderna**:
- **Validação**: Whitelist de extensões em `FileValidationService`
- **Extensões**: `.csv`, `.xls`, `.xlsx`, `.xml`, `.json`, `.edi`

---

### Item LEG-RF085-016: Estratégia de Duplicata IGNORE (Default)

**Localização no Código**: `sp_ImportarClientes.sql - Linha 35`

**Código SQL**:
```sql
IF EXISTS (SELECT 1 FROM tb_Clientes WHERE CPF_CNPJ = @CPF_CNPJ AND Id_Cliente = @Id_Cliente)
BEGIN
    -- Ignora silenciosamente (não faz nada)
    SET @Registros_Ignorados = @Registros_Ignorados + 1
    CONTINUE
END
```

**Regra Extraída**:
- Se registro com mesma chave natural (CPF/CNPJ) já existe, importação IGNORA silenciosamente
- Nenhum UPDATE é executado
- Nenhum erro é gerado
- Contador de "registros ignorados" é incrementado

**DESTINO**: ASSUMIDO (com opções)

**Justificativa**: Estratégia IGNORE mantida como padrão mas sistema moderno permite escolher entre IGNORE, REPLACE, REJECT.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-004)
- **Regra Moderna**: RN-RF085-004 (Detecção de Duplicatas por Chave Natural)

**Migração Moderna**:
- **Enum**: `DuplicateStrategy { Ignore, Replace, Reject, MarkAsUpdate }`
- **Configuração**: Template possui campo `DuplicateStrategy` (padrão: Ignore)
- **Implementação**: `DuplicateDetector` class

---

### Item LEG-RF085-017: Validação de Email via Regex

**Localização no Código**: `sp_ImportarFornecedores.sql - Linha 42`

**Código SQL**:
```sql
IF @Email NOT LIKE '%_@__%.__%' THEN
BEGIN
    INSERT INTO #Erros (Numero_Linha, Campo_Erro, Descricao_Erro)
    VALUES (@Linha, 'Email', 'Email inválido')
    CONTINUE
END
```

**Regra Extraída**:
- Email deve conter `@` e pelo menos um `.` após o `@`
- Validação rudimentar (aceita emails inválidos como `a@b.c`)

**DESTINO**: ASSUMIDO (aprimorado)

**Justificativa**: Validação de email mantida mas com regex mais robusto.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 3 (RN-RF085-003)
- **Regra Moderna**: RN-RF085-003 (Validação de Dados Contra Regras de Negócio)

**Migração Moderna**:
- **Validador**: `FluentValidation` com `EmailAddress()` (regex RFC 5322)
- **Regex**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

---

### Item LEG-RF085-018: Timeout HTTP de 300 Segundos

**Localização no Código**: `Web.config - Linha 78`

**Configuração XML**:
```xml
<httpRuntime executionTimeout="300" maxRequestLength="51200" />
```

**Regra Extraída**:
- Requisições HTTP (incluindo importações) têm timeout de 300 segundos (5 minutos)
- Se processamento demorar mais, conexão é abortada
- Dados processados até o momento são perdidos (nenhuma transação)

**DESTINO**: DESCARTADO

**Justificativa**: Importações modernas são processadas de forma assíncrona via Hangfire, sem limite de tempo HTTP.

**Rastreabilidade**:
- **RF Moderno**: RF085 - Seção 2 (Funcionalidade F12)
- **Solução Moderna**: Processamento assíncrono com SignalR para notificações

**Migração Moderna**:
- **Hangfire**: Jobs em background sem timeout HTTP
- **SignalR**: Notificações em tempo real para o cliente
- **API**: Endpoint retorna imediatamente com `202 Accepted` e job ID

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

### 7.1 Funcionalidades do Legado NÃO Migradas

| Funcionalidade Legada | Justificativa para NÃO Migrar |
|----------------------|-------------------------------|
| **Upload direto para pasta física** | Substituído por Azure Blob Storage (segurança, escalabilidade) |
| **Task Scheduler do Windows** | Substituído por Hangfire (persistente, distribuído, web-based) |
| **Processamento síncrono na thread HTTP** | Substituído por jobs assíncronos (evita timeout) |
| **XML para mapeamento** | Substituído por estrutura relacional (FieldMapping table) |
| **Rollback sem validação de tempo** | Limitado a 7 dias no sistema moderno (conformidade LGPD) |

---

### 7.2 Funcionalidades Novas (Não Existiam no Legado)

| Funcionalidade Nova | Benefício |
|-------------------|-----------|
| **Preview de dados antes de importar** | Evita erros, permite ajustes antes de persistir |
| **Transformações configuráveis (UPPER, TRIM, FORMAT_DATE)** | Flexibilidade sem alterar código |
| **Múltiplas estratégias de duplicata (IGNORE, REPLACE, REJECT)** | Controle fino sobre comportamento |
| **Importação incremental (delta detection)** | Performance em cargas recorrentes |
| **Scan de antivírus (ClamAV)** | Segurança contra malware |
| **Relatório de erros com sugestões automáticas** | Facilita correção de dados |
| **API de status em tempo real (SignalR)** | UX superior, feedback instantâneo |
| **Agendamento com retry automático** | Resiliência em caso de falhas |
| **Auditoria completa com retenção 7 anos** | Conformidade LGPD |
| **Multi-tenancy com isolamento automático** | Segurança e escalabilidade |

---

### 7.3 Mudanças de Comportamento (Legado vs Moderno)

| Aspecto | Legado | Moderno | Risco de Migração |
|---------|--------|---------|-------------------|
| **Estratégia de Duplicata** | IGNORE (sem opção) | IGNORE, REPLACE, REJECT (configurável) | BAIXO - Padrão mantido como IGNORE |
| **Timeout de Importação** | 300 segundos (HTTP) | Ilimitado (Hangfire) | BAIXO - Importações grandes agora funcionam |
| **Validação de Email** | Regex simples (aceita inválidos) | RFC 5322 (rejeita mais casos) | MÉDIO - Emails antes aceitos podem ser rejeitados |
| **Rollback** | Ilimitado no tempo | Limitado a 7 dias | MÉDIO - Rollbacks antigos não serão possíveis |
| **Tamanho de Arquivo** | 50MB | 500MB (configurável) | BAIXO - Limite aumentado |
| **Formatos Suportados** | CSV, XLS | CSV, XLS, XLSX, XML, JSON, EDI | BAIXO - Apenas expansão |

---

### 7.4 Riscos Identificados na Migração

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| **Usuários acostumados com fluxo síncrono** | BAIXA | Treinamento sobre importações assíncronas |
| **Validação de email mais rigorosa rejeita dados** | MÉDIA | Período de transição com warnings antes de rejeitar |
| **Templates de mapeamento precisam ser recriados** | ALTA | Ferramenta de migração automática de XML → FieldMapping |
| **Histórico de importações antigas não migrado** | MÉDIA | Manter acesso read-only ao sistema legado por 6 meses |
| **Rollback limitado a 7 dias** | BAIXA | Documentar política claramente na tela |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-31 | Criação do RL-RF085 com separação completa do legado, 18 itens rastreados, 100% com destinos definidos | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-31
**Status**: Completo - Pronto para validação
**Total de Itens Legado**: 18 (100% com destino definido)
**Destinos**: ASSUMIDO (5), SUBSTITUÍDO (12), DESCARTADO (1)

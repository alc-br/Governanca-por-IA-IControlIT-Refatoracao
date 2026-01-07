# RL-RF023 — Referência ao Legado: Gestão de Contratos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-023 - Gestão de Contratos
**Sistema Legado:** IC1_Sistema_Producao (ASP.NET Web Forms + VB.NET + SQL Server)
**Objetivo:** Documentar o comportamento do legado que serviu de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Stack Tecnológica

- **Arquitetura:** Monolítica com WebServices ASMX
- **Linguagem:** VB.NET (Code-behind ASPX)
- **Framework:** ASP.NET Web Forms (.NET Framework 4.5)
- **Banco de Dados:** SQL Server 2012 (banco `IC1_Sistema_Producao`)
- **Frontend:** ASPX Server-Side Rendering (ViewState, PostBack)
- **Webservices:** ASMX (XML/SOAP)
- **Relatórios:** Crystal Reports hospedado em servidor dedicado
- **Anexos:** Pasta compartilhada (`\\server\contratos`) sem versionamento

### Características do Sistema Legado

- **Multi-tenant:** ❌ Não existia. Todos os dados visíveis a todos os usuários.
- **Auditoria:** ⚠️ Parcial. Logs textuais em arquivo `text.log` sem estrutura.
- **Soft Delete:** ❌ Inexistente. Hard delete físico no banco.
- **Workflow:** ⚠️ Simplificado. Apenas 4 estados estáticos (Rascunho, Ativo, Vencido, Renovado).
- **Alertas:** ⚠️ Job SQL Server agendado diariamente à noite (sem notificação em tempo real).
- **Reajustes:** ❌ Manual. DBA executava UPDATE direto no banco.
- **Validações:** ⚠️ Mínimas. Apenas validações básicas de campos obrigatórios.
- **Segurança:** ⚠️ Básica. Sem isolamento por tenant, sem RBAC robusto.

### Problemas Arquiteturais Identificados

1. **Falta de Multi-tenancy:** Dados de diferentes clientes misturados no mesmo banco sem isolamento
2. **Hard Delete:** Dados excluídos permanentemente sem possibilidade de recuperação ou auditoria
3. **Auditoria Inadequada:** Logs textuais sem estrutura, difíceis de consultar e rastrear
4. **Workflow Limitado:** Apenas 4 estados, sem rastreamento de transições ou aprovações
5. **Anexos Não Versionados:** Pasta compartilhada sem controle de versão ou integridade
6. **Validações Fracas:** Muitas regras de negócio não validadas no backend
7. **Reajustes Manuais:** Processo suscetível a erros humanos, sem histórico
8. **Sem Notificações em Tempo Real:** Alertas apenas por e-mail agendado, sem push notifications

---

## 2. TELAS ASPX E CÓDIGO-BEHIND

### Tela 1: Contrato.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Contratos/Contrato.aspx`
- **Responsabilidade:** Formulário de criação/edição de contrato
- **Modo:** Server-Side Rendering com ViewState e PostBack

#### Campos do Formulário

| Campo | Tipo | Obrigatório | Validação | Observações |
|-------|------|-------------|-----------|-------------|
| `txtNumeroContrato` | TextBox | Sim | Unique no banco | Validação apenas no submit |
| `ddlFornecedor` | DropDownList | Sim | FK válido | Carregado de `dbo.Fornecedor` |
| `ddlTipoContrato` | DropDownList | Sim | FK válido | Compra, Locação, Manutenção, Telecom, Serviço |
| `txtDescricao` | TextBox (MultiLine) | Não | Max 500 chars | Sem sanitização de HTML |
| `txtDataInicio` | TextBox | Sim | Formato dd/MM/yyyy | Validação client-side fraca |
| `txtDataFim` | TextBox | Sim | Formato dd/MM/yyyy | Não valida se >= DataInicio |
| `txtValorTotal` | TextBox | Sim | Decimal positivo | Formato pt-BR (vírgula) |
| `txtValorMensal` | TextBox | Não | Decimal positivo | Calculado manualmente pelo usuário |
| `ddlStatus` | DropDownList | Sim | Enum fixo | Rascunho, Ativo, Vencido, Renovado |
| `chkRenovacaoAutomatica` | CheckBox | Não | Boolean | Sem validação de regras de renovação |

#### Comportamentos Implícitos no Code-Behind (VB.NET)

1. **Cálculo de Valor Mensal:** Não era automático. Usuário digitava manualmente, podendo haver inconsistência entre ValorTotal e ValorMensal.
2. **Validação de Vigência:** ❌ Não validava se DataFim >= DataInicio. Contratos com datas inválidas podiam ser salvos.
3. **CNPJ do Fornecedor:** ⚠️ Validação básica de formato, mas não validava dígitos verificadores.
4. **Upload de Anexos:** Salvava arquivo diretamente em `\\server\contratos\{idContrato}\{nomeArquivo}` sem CRC32 ou versionamento.
5. **Auditoria:** Gravava log textual em `text.log`: `"Usuario {nome} criou contrato {numero} em {data}"`
6. **Workflow:** Status alterado manualmente pelo usuário sem validação de transições permitidas.

#### Regras de Negócio Implícitas Extraídas do Code-Behind

- **RN-LEG-CTR-001:** Número do contrato deve ser único globalmente (sem isolamento por cliente).
- **RN-LEG-CTR-002:** Ao salvar, grava `DataCriacao = DateTime.Now` e `UsuarioCriacao = Session("UsuarioId")`.
- **RN-LEG-CTR-003:** Se `chkRenovacaoAutomatica = True`, exibe mensagem informativa "Contrato será renovado automaticamente", mas renovação era manual (via job SQL).
- **RN-LEG-CTR-004:** Botão "Excluir" executa `DELETE FROM dbo.Contrato WHERE idContrato = @id` (hard delete, sem confirmação robusta).

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Tela ASPX substituída por componente Angular SPA com validações robustas no frontend e backend.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades Cobertas)
  - **UC Moderno:** UC01-RF023 (Criar Contrato), UC02-RF023 (Editar Contrato)
- **Migração Moderna:**
  - **Componente Angular:** `contratos-form.component.ts` (Standalone Component)
  - **Rota Frontend:** `/contratos/novo`, `/contratos/{id}/editar`
  - **Endpoint Backend:** `POST /api/contratos`, `PUT /api/contratos/{id}`

---

### Tela 2: ContratoLista.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Contratos/ContratoLista.aspx`
- **Responsabilidade:** Listagem e busca de contratos
- **Modo:** GridView com paginação server-side (ViewState pesado)

#### Funcionalidades

- GridView com 10 registros por página (paginação no ViewState, lenta)
- Filtros básicos: Número, Fornecedor, Status, Período de Vigência
- Ordenação apenas por DataCriacao DESC
- Ações inline: Editar, Excluir (com confirmação JavaScript simples), Visualizar Anexos

#### Problemas Identificados

1. **Performance:** ViewState gigante (>500KB) ao carregar muitos contratos.
2. **Sem Busca Avançada:** Filtros muito limitados, sem busca por valor, tipo de contrato, etc.
3. **Paginação Ineficiente:** Carrega TODOS os registros do banco e pagina no ViewState.
4. **Sem Exportação:** Usuário precisava ir em "Relatórios" separadamente.

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Substituído por SPA Angular com DataTable/Grid moderno, filtros dinâmicos, paginação server-side eficiente e exportação inline.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades: Listagem de Contratos)
  - **UC Moderno:** UC03-RF023 (Consultar Contrato)
- **Migração Moderna:**
  - **Componente Angular:** `contratos-list.component.ts`
  - **Rota Frontend:** `/contratos`
  - **Endpoint Backend:** `GET /api/contratos` (com paginação: `?page=1&pageSize=50`)

---

### Tela 3: ContratoDetalhes.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Contratos/ContratoDetalhes.aspx`
- **Responsabilidade:** Visualização de detalhes do contrato (read-only)
- **Modo:** FormView com databinding direto do banco

#### Seções Exibidas

- Dados do contrato (número, descrição, datas, valores)
- Dados do fornecedor (CNPJ, razão social, contato)
- Histórico de status (tabela de mudanças de status ao longo do tempo, quando existia)
- Lista de anexos (links para download via pasta compartilhada)

#### Problemas Identificados

1. **Sem Histórico Completo:** Apenas status eram rastreados, não alterações em campos individuais.
2. **Anexos Sem Metadata:** Links diretos para arquivos sem informação de versão, tamanho, CRC32.

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Substituído por Card View Angular com tabs (Dados, Fornecedor, Histórico, Anexos) e preview de documentos.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades: Consulta de Contrato)
  - **UC Moderno:** UC03-RF023 (Consultar Contrato)
- **Migração Moderna:**
  - **Componente Angular:** `contratos-detail.component.ts`
  - **Rota Frontend:** `/contratos/{id}`
  - **Endpoint Backend:** `GET /api/contratos/{id}`, `GET /api/contratos/{id}/historico`

---

### Tela 4: ContratoAnexos.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Contratos/ContratoAnexos.aspx`
- **Responsabilidade:** Gestão de anexos contratuais (upload/download/delete)
- **Modo:** FileUpload control + GridView de anexos existentes

#### Funcionalidades

- Upload de arquivos (PDF, DOCX, XML) - máximo 10MB
- Download via link direto (`\\server\contratos\{idContrato}\{arquivo}`)
- Exclusão de anexo (DELETE físico do arquivo + registro no banco)

#### Problemas Identificados

1. **Sem Versionamento:** Reuploar arquivo com mesmo nome sobrescreve sem histórico.
2. **Sem Validação de Integridade:** Não calcula hash (CRC32, SHA256) para verificar corrupção.
3. **Sem Controle de Acesso:** Qualquer usuário com link direto poderia baixar anexo (se soubesse o caminho da rede).

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Substituído por componente Angular com Azure Blob Storage, versionamento automático, hash CRC32 e controle de acesso granular.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades: Gestão de Anexos)
  - **UC Moderno:** UC06-RF023 (Gestão de Anexos)
- **Migração Moderna:**
  - **Componente Angular:** `contratos-anexos.component.ts`
  - **Rota Frontend:** `/contratos/{id}/anexos`
  - **Endpoint Backend:** `POST /api/contratos/{id}/anexos`, `GET /api/contratos/{id}/anexos/{anexoId}`

---

### Tela 5: ContratoRelatorio.aspx

- **Caminho:** `ic1_legado/IControlIT/Financeiro/Contratos/ContratoRelatorio.aspx`
- **Responsabilidade:** Geração de relatórios em Excel/PDF
- **Modo:** Crystal Reports com parâmetros server-side

#### Relatórios Disponíveis

- Contratos Ativos (listagem simples)
- Contratos A Vencer (próximos 30/60/90 dias)
- Contratos Vencidos
- Análise de Custos por Fornecedor
- Análise de Custos por Tipo de Contrato

#### Problemas Identificados

1. **Lentidão:** Crystal Reports pesado, geração pode levar minutos.
2. **Sem Filtros Dinâmicos:** Parâmetros fixos, sem possibilidade de filtrar por múltiplos campos.
3. **Sem Gráficos Interativos:** Apenas tabelas e gráficos estáticos.

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Substituído por BI integrado no Angular com filtros dinâmicos, gráficos interativos (ApexCharts) e exportação em Excel/PDF.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades: Relatórios Gerenciais)
  - **UC Moderno:** UC03-RF023 (Consultar Contrato - inclui relatórios)
- **Migração Moderna:**
  - **Componente Angular:** `relatorios-contratos.component.ts`
  - **Rota Frontend:** `/relatorios/contratos`
  - **Endpoint Backend:** `GET /api/contratos/export?formato=excel`, `GET /api/contratos/metricas`

---

## 3. WEBSERVICES ASMX (.asmx.vb)

### Arquivo: WSContrato.asmx.vb

- **Caminho:** `ic1_legado/IControlIT/WebService/WSContrato.asmx.vb`
- **Tecnologia:** ASMX (XML/SOAP)
- **Responsabilidade:** Operações CRUD e consultas de contratos via webservice

### Métodos Públicos Expostos

| Método | Parâmetros | Retorno | Lógica Principal |
|--------|------------|---------|------------------|
| `ListarContratos()` | Nenhum | `List(Of Contrato)` | `SELECT * FROM dbo.Contrato WHERE Ativo = 1` (sem paginação, sem multi-tenancy) |
| `BuscarPorId(idContrato As Integer)` | `idContrato: Integer` | `Contrato` | `SELECT * FROM dbo.Contrato WHERE idContrato = @id` |
| `Inserir(contrato As Contrato)` | `contrato: Contrato` | `Integer` (ID gerado) | `INSERT INTO dbo.Contrato ... ; SELECT @@IDENTITY` |
| `Atualizar(contrato As Contrato)` | `contrato: Contrato` | `Boolean` | `UPDATE dbo.Contrato SET ... WHERE idContrato = @id` |
| `Deletar(idContrato As Integer)` | `idContrato: Integer` | `Boolean` | `DELETE FROM dbo.Contrato WHERE idContrato = @id` (hard delete) |
| `BuscarVencimentos(diasAntecipacao As Integer)` | `diasAntecipacao: Integer` | `List(Of Contrato)` | `SELECT * WHERE DataFim BETWEEN @hoje AND @hoje + @dias` |
| `GerarRelatorio(filtros As String)` | `filtros: String (XML)` | `Byte()` (Excel binary) | Chama Crystal Reports |
| `UploadAnexo(idContrato As Integer, arquivo As Byte(), nomeArquivo As String)` | Múltiplos | `Boolean` | Salva em `\\server\contratos\{id}\{nome}` |
| `ListarAnexos(idContrato As Integer)` | `idContrato: Integer` | `List(Of String)` | `SELECT * FROM dbo.ContratoAnexo WHERE idContrato = @id` |

### Regras de Negócio Implícitas no Webservice

- **RN-WS-CTR-001:** Método `Inserir` não valida se DataFim >= DataInicio (confia no frontend).
- **RN-WS-CTR-002:** Método `Deletar` executa hard delete sem verificar dependências (FK em Medicao, Garantia).
- **RN-WS-CTR-003:** Método `ListarContratos` retorna TODOS os contratos sem paginação (problema de performance com +1000 registros).
- **RN-WS-CTR-004:** Método `Atualizar` não grava log de auditoria estruturado, apenas log textual.
- **RN-WS-CTR-005:** Nenhum método valida multi-tenancy ou permissões RBAC (qualquer usuário autenticado pode acessar qualquer contrato).

### Problemas Identificados

1. **Sem Paginação:** `ListarContratos()` retorna todos os registros, causando timeout com grande volume.
2. **Hard Delete:** Método `Deletar` remove dados permanentemente sem possibilidade de recuperação.
3. **Sem Multi-tenancy:** Todos os métodos retornam dados de todos os clientes misturados.
4. **Sem RBAC:** Não valida permissões (approve, delete, etc.) antes de executar operações.
5. **Validações Fracas:** Métodos confiam no frontend para validar dados.
6. **Auditoria Inadequada:** Apenas logs textuais, sem rastreamento estruturado.

### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Webservices ASMX substituídos por REST API (.NET 10) com autenticação JWT, validação rigorosa, RBAC, multi-tenancy e auditoria estruturada.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 8 (API Endpoints)
- **Migração Moderna:**
  - **Arquitetura:** Clean Architecture + CQRS + MediatR
  - **Endpoints REST:**
    - `ListarContratos()` → `GET /api/contratos?page=1&pageSize=50`
    - `BuscarPorId()` → `GET /api/contratos/{id}`
    - `Inserir()` → `POST /api/contratos` (CriarContratoCommand + 10 RNs de validação)
    - `Atualizar()` → `PUT /api/contratos/{id}` (AtualizarContratoCommand)
    - `Deletar()` → `DELETE /api/contratos/{id}` (Soft delete com RN-CTR-023-06)
    - `BuscarVencimentos()` → `GET /api/contratos/vencimentos?dias=30`
    - `GerarRelatorio()` → `GET /api/contratos/export?formato=excel`
    - `UploadAnexo()` → `POST /api/contratos/{id}/anexos`
    - `ListarAnexos()` → `GET /api/contratos/{id}/anexos`

---

## 4. STORED PROCEDURES

### Procedure 1: pa_ContratoBuscarTodos

- **Caminho:** `ic1_legado/Database/Procedures/pa_ContratoBuscarTodos.sql`
- **Parâmetros Entrada:** Nenhum
- **Parâmetros Saída:** Nenhum (result set)
- **Lógica:** `SELECT * FROM dbo.Contrato WHERE Ativo = 1 ORDER BY DataCriacao DESC`

#### Problemas Identificados

- Sem paginação (retorna tudo)
- Sem filtros dinâmicos
- Sem isolamento por cliente (multi-tenancy)

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Lógica movida para Application Layer (GetContratosQuery + Handler) com paginação, filtros dinâmicos e multi-tenancy.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 8 (API Endpoints: GET /api/contratos)
  - **Regra Moderna:** RN-CTR-023-09 (Multi-tenancy)
- **Migração Moderna:**
  - **Query CQRS:** `GetContratosQuery`
  - **Handler:** `GetContratosQueryHandler`
  - **Validação:** ClienteId obrigatório na query

---

### Procedure 2: pa_ContratoInserir

- **Caminho:** `ic1_legado/Database/Procedures/pa_ContratoInserir.sql`
- **Parâmetros Entrada:** `@NumeroContrato, @idFornecedor, @DataInicio, @DataFim, @ValorTotal, @ValorMensal, @Status, @UsuarioCriacao`
- **Parâmetros Saída:** `@idContrato INT OUTPUT`
- **Lógica:**
  ```sql
  INSERT INTO dbo.Contrato (...)
  VALUES (...)
  SET @idContrato = @@IDENTITY
  ```

#### Validações na Procedure

- ❌ Não valida se DataFim >= DataInicio
- ❌ Não valida se @idFornecedor existe e está ativo
- ❌ Não valida CNPJ do fornecedor
- ❌ Não valida unicidade de @NumeroContrato (confia em constraint do banco)

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Lógica movida para Application Layer (CriarContratoCommand + Handler) com validações rigorosas (RN-CTR-023-01 até RN-CTR-023-10).
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 8 (API Endpoints: POST /api/contratos)
  - **Regras Modernas:** RN-CTR-023-01, RN-CTR-023-02, RN-CTR-023-08
- **Migração Moderna:**
  - **Command CQRS:** `CriarContratoCommand`
  - **Handler:** `CriarContratoCommandHandler`
  - **Validador:** `CriarContratoCommandValidator (FluentValidation)`

---

### Procedure 3: pa_ContratoDeletar

- **Caminho:** `ic1_legado/Database/Procedures/pa_ContratoDeletar.sql`
- **Parâmetros Entrada:** `@idContrato INT`
- **Parâmetros Saída:** Nenhum
- **Lógica:** `DELETE FROM dbo.Contrato WHERE idContrato = @idContrato`

#### Problemas Identificados

- **Hard Delete:** Remove dados permanentemente
- **Sem Verificação de Dependências:** Não verifica FK em Medicao, Garantia, Anexos
- **Sem Auditoria:** Não registra quem deletou, quando, nem snapshot dos dados

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Hard delete substituído por Soft Delete com auditoria completa (RN-CTR-023-10) e bloqueio de exclusão com medições associadas (RN-CTR-023-06).
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 8 (API Endpoints: DELETE /api/contratos/{id})
  - **Regras Modernas:** RN-CTR-023-06, RN-CTR-023-10
- **Migração Moderna:**
  - **Command CQRS:** `ExcluirContratoCommand`
  - **Handler:** `ExcluirContratoCommandHandler` (valida medições, executa soft delete, grava auditoria)

---

### Procedure 4: pa_ContratoVencimentos

- **Caminho:** `ic1_legado/Database/Procedures/pa_ContratoVencimentos.sql`
- **Parâmetros Entrada:** `@diasAntecipacao INT`
- **Parâmetros Saída:** Nenhum (result set)
- **Lógica:**
  ```sql
  DECLARE @dataLimite DATE = DATEADD(DAY, @diasAntecipacao, GETDATE())
  SELECT * FROM dbo.Contrato
  WHERE DataFim BETWEEN GETDATE() AND @dataLimite
    AND Status = 'Ativo'
  ```

#### Problemas Identificados

- Sem multi-tenancy (retorna contratos de todos os clientes)
- Sem paginação
- Sem ordenação configurável

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Lógica movida para Application Layer (GetContratosVencimentosQuery + Handler) com multi-tenancy e paginação.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 8 (API Endpoints: GET /api/contratos/vencimentos?dias=30)
  - **Regra Moderna:** RN-CTR-023-04 (Alertas de Vencimento)
- **Migração Moderna:**
  - **Query CQRS:** `GetContratosVencimentosQuery`
  - **Handler:** `GetContratosVencimentosQueryHandler`

---

## 5. TABELAS LEGADAS

### Tabela 1: dbo.Contrato

- **Schema:** `[dbo].[Contrato]`
- **Banco:** `IC1_Sistema_Producao`
- **Chave Primária:** `idContrato INT IDENTITY(1,1)`

#### Estrutura SQL

```sql
CREATE TABLE [dbo].[Contrato](
    [idContrato] [int] IDENTITY(1,1) NOT NULL,
    [idFornecedor] [int] NOT NULL,
    [idTipoContrato] [int] NOT NULL,
    [NumeroContrato] [varchar](50) NOT NULL,
    [Descricao] [varchar](500) NULL,
    [DataInicio] [datetime] NOT NULL,
    [DataFim] [datetime] NOT NULL,
    [ValorTotal] [decimal](18,2) NOT NULL,
    [ValorMensal] [decimal](18,2) NULL,
    [Status] [varchar](20) NOT NULL,
    [Ativo] [bit] NOT NULL,
    [DataCriacao] [datetime] NOT NULL,
    [DataUltimaAlteracao] [datetime] NULL,
    [UsuarioCriacao] [varchar](100) NOT NULL,
    [UsuarioAlteracao] [varchar](100) NULL,
    CONSTRAINT [PK_Contrato] PRIMARY KEY CLUSTERED ([idContrato] ASC),
    CONSTRAINT [FK_Contrato_Fornecedor] FOREIGN KEY ([idFornecedor])
        REFERENCES [dbo].[Fornecedor] ([idFornecedor]),
    CONSTRAINT [FK_Contrato_TipoContrato] FOREIGN KEY ([idTipoContrato])
        REFERENCES [dbo].[TipoContrato] ([idTipoContrato])
)
```

#### Problemas Identificados

| Problema | Descrição | Impacto |
|----------|-----------|---------|
| **Sem ClienteId** | Não isola dados por cliente (multi-tenancy) | CRÍTICO - Dados de clientes diferentes misturados |
| **Sem IsDeleted** | Não suporta soft delete | ALTO - Dados excluídos permanentemente |
| **Auditoria Incompleta** | Apenas DataCriacao, UsuarioCriacao | ALTO - Falta rastreamento de alterações (before/after) |
| **Status varchar(20)** | Não usa ENUM ou tabela de domínio | MÉDIO - Dados inconsistentes possíveis |
| **Sem Índices Secundários** | Apenas PK, sem índices em DataFim, Status | MÉDIO - Performance ruim em consultas |
| **Descrição limitada** | varchar(500) | BAIXO - Pode ser insuficiente para contratos complexos |
| **Sem campo IndiceReajuste** | Reajuste não configurável no banco | ALTO - Reajustes manuais via DBA |
| **Sem campo RenovacaoAutomatica** | Configuração de renovação não armazenada | ALTO - Renovação manual ou via job externo |

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Tabela redesenhada com multi-tenancy, auditoria integrada, soft delete, índices otimizados e novos campos (IndiceReajuste, RenovacaoAutomatica).
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 7 (Modelo de Dados)
  - **MD Moderno:** MD-RF023.md - Tabela Contrato
- **Migração Moderna:**
  - **Tabela Moderna:** `Contrato` (com ClienteId, IsDeleted, DataDelecao, DeletadoPor, IndiceReajuste, RenovacaoAutomatica)
  - **Migration EF Core:** `20251230_CreateContratoTable.cs`
  - **Auditoria:** Tabela `AuditoriaOperacao` separada com JSON de mudanças

---

### Tabela 2: dbo.ContratoAnexo

- **Schema:** `[dbo].[ContratoAnexo]`
- **Banco:** `IC1_Sistema_Producao`
- **Chave Primária:** `idAnexo INT IDENTITY(1,1)`

#### Estrutura SQL

```sql
CREATE TABLE [dbo].[ContratoAnexo](
    [idAnexo] [int] IDENTITY(1,1) NOT NULL,
    [idContrato] [int] NOT NULL,
    [NomeArquivo] [varchar](255) NOT NULL,
    [CaminhoArquivo] [varchar](500) NOT NULL,
    [DataUpload] [datetime] NOT NULL,
    [UsuarioUpload] [varchar](100) NOT NULL,
    CONSTRAINT [PK_ContratoAnexo] PRIMARY KEY CLUSTERED ([idAnexo] ASC),
    CONSTRAINT [FK_ContratoAnexo_Contrato] FOREIGN KEY ([idContrato])
        REFERENCES [dbo].[Contrato] ([idContrato])
)
```

#### Problemas Identificados

- Sem campo CRC32 ou hash (não valida integridade do arquivo)
- Sem versionamento (reuploar sobrescreve)
- CaminhoArquivo armazena path de rede (`\\server\contratos`) hardcoded
- Sem controle de tamanho do arquivo
- Sem validação de tipo de arquivo (extensão)

#### Destino

- **DESTINO:** SUBSTITUÍDO
- **Justificativa:** Substituído por Azure Blob Storage com versionamento automático, CRC32, metadata e controle de acesso granular.
- **Rastreabilidade:**
  - **RF Moderno:** RF-023 - Seção 4 (Funcionalidades: Gestão de Anexos)
  - **MD Moderno:** MD-RF023.md - Tabela ContratoAnexo
- **Migração Moderna:**
  - **Tabela Moderna:** `ContratoAnexo` (com BlobUrl, CRC32, Tamanho, TipoMime, Versao)
  - **Storage:** Azure Blob Storage (container `contratos-anexos`)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Lista de regras que **não estavam documentadas formalmente** mas foram descobertas ao analisar código VB.NET, stored procedures e comportamento do sistema legado.

### RL-RN-001: Número de Contrato Único Globalmente

**Descrição:** O campo `NumeroContrato` é unique no banco de dados, mas sem isolamento por cliente. Dois clientes diferentes não podiam ter o mesmo número de contrato.

**Localização:** Constraint `UQ_Contrato_NumeroContrato` no banco
**Impacto:** Em um sistema multi-tenant, isso causava conflitos entre clientes.
**Decisão Moderna:** Unique composto (`ClienteId` + `NumeroContrato`) para permitir que cada cliente tenha seu próprio controle de numeração.

---

### RL-RN-002: Reajuste Manual via DBA

**Descrição:** Não havia sistema automático de reajuste. Todo mês de aniversário do contrato, um DBA executava UPDATE manual para aplicar IGPM/IPCA.

**Localização:** Script manual executado mensalmente: `UPDATE dbo.Contrato SET ValorMensal = ValorMensal * 1.005 WHERE ...`
**Impacto:** Suscetível a erros humanos, sem histórico de reajustes, sem rastreabilidade.
**Decisão Moderna:** Job background automático com RN-CTR-023-07, histórico de reajustes em auditoria, índices configuráveis.

---

### RL-RN-003: Renovação Automática via Job SQL

**Descrição:** Job SQL Server agendado verificava contratos com DataFim próxima e `RenovacaoAutomatica = 1`, criando novo registro de contrato.

**Localização:** `SQL Server Agent Job: ContratoRenovacaoAutomatica`
**Lógica:**
```sql
INSERT INTO dbo.Contrato (...)
SELECT NumeroContrato + '-REN', idFornecedor, ... , DATEADD(YEAR, 1, DataFim)
FROM dbo.Contrato
WHERE DataFim = GETDATE() AND RenovacaoAutomatica = 1
```

**Impacto:** Job executava às 23:59, mas se falhasse, renovação era perdida. Sem retry, sem notificação de falha.
**Decisão Moderna:** Job background .NET com retry, notificação de falha, auditoria completa (RN-CTR-023-03).

---

### RL-RN-004: Alertas de Vencimento via E-mail

**Descrição:** Job SQL Server enviava e-mails de alerta para contratos vencendo em 30/60/90 dias.

**Localização:** `SQL Server Agent Job: ContratoAlertasVencimento`
**Lógica:** Consulta contratos vencendo → Monta HTML do e-mail → Envia via `sp_send_dbmail`
**Impacto:** Sem notificação em tempo real, sem SignalR, sem rastreamento de alertas enviados (podiam duplicar).
**Decisão Moderna:** Job background .NET + SignalR para notificação em tempo real + tabela AuditoriaAlerta para evitar duplicatas (RN-CTR-023-04).

---

### RL-RN-005: Workflow de Aprovação Simplificado

**Descrição:** Workflow tinha apenas 4 estados fixos: Rascunho → Ativo → Vencido → Renovado. Não havia aprovação formal, apenas mudança de status manual.

**Localização:** Campo `Status varchar(20)` na tabela
**Impacto:** Sem controle de alçadas, sem rastreamento de quem aprovou, quando, por que. Qualquer usuário podia mudar status.
**Decisão Moderna:** State Machine com 10 estados, workflow de aprovação por alçadas (RN-CTR-023-05), auditoria de transições.

---

### RL-RN-006: Exclusão Sem Validação de Dependências

**Descrição:** Procedure `pa_ContratoDeletar` executava hard delete sem verificar se contrato tinha medições, garantias ou anexos associados.

**Localização:** `pa_ContratoDeletar.sql` - linha 5: `DELETE FROM dbo.Contrato WHERE idContrato = @id`
**Impacto:** Exclusão causava quebra de integridade referencial se houvesse FKs ativas (erro SQL Server) ou perda de dados.
**Decisão Moderna:** Soft delete + validação de dependências (RN-CTR-023-06), bloqueio de exclusão com medições associadas.

---

### RL-RN-007: Cálculo de Valor Mensal Manual

**Descrição:** Usuário digitava ValorMensal manualmente. Sistema não validava consistência com ValorTotal. Podia haver contratos com ValorMensal * 12 ≠ ValorTotal.

**Localização:** Campo `txtValorMensal` em `Contrato.aspx` (não calculado automaticamente)
**Impacto:** Dados inconsistentes, dificuldade em relatórios de custo.
**Decisão Moderna:** Cálculo automático com RN-CTR-023-02, recálculo bidirecional (ValorTotal ↔ ValorMensal).

---

### RL-RN-008: Anexos Sem Versionamento

**Descrição:** Reuploar arquivo com mesmo nome sobrescreve o anterior sem manter histórico.

**Localização:** Code-behind `ContratoAnexos.aspx.vb` - linha 45: `File.Copy(uploadedFile, destPath, overwrite:=True)`
**Impacto:** Perda de versões anteriores de documentos importantes (contratos assinados, aditivos).
**Decisão Moderna:** Azure Blob Storage com versionamento automático, cada upload cria nova versão preservando antigas.

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Legado | RF Moderno | Decisão de Migração |
|------|--------|------------|---------------------|
| **Multi-tenancy** | ❌ Inexistente. Todos os dados visíveis a todos. | ✅ ClienteId obrigatório em todas as queries (RN-CTR-023-09) | **NOVO** - Implementar isolamento total por cliente |
| **Soft Delete** | ❌ Hard delete físico. Dados perdidos permanentemente. | ✅ IsDeleted + DataDelecao + auditoria (RN-CTR-023-10) | **NOVO** - Implementar soft delete com auditoria |
| **Workflow Aprovação** | ⚠️ Simplificado (4 estados, sem alçadas, sem rastreamento) | ✅ State Machine 10 estados + alçadas dinâmicas (RN-CTR-023-05) | **EVOLUÍDO** - Expandir workflow com aprovações por valor |
| **Alertas Vencimento** | ⚠️ Job SQL noturno, apenas e-mail | ✅ Job .NET + SignalR real-time + e-mail + auditoria (RN-CTR-023-04) | **EVOLUÍDO** - Adicionar notificação em tempo real |
| **Reajustes** | ❌ Manual via DBA (UPDATE direto no banco) | ✅ Automático por índice (IGPM/IPCA/INPC) com histórico (RN-CTR-023-07) | **NOVO** - Implementar reajuste automático configurável |
| **Renovação Automática** | ⚠️ Job SQL com falhas sem retry | ✅ Job .NET com retry, notificação de falha (RN-CTR-023-03) | **EVOLUÍDO** - Tornar robusto com retry e auditoria |
| **Anexos** | ⚠️ Pasta compartilhada, sem versionamento, sem CRC32 | ✅ Azure Blob Storage + versionamento + CRC32 + ACL | **EVOLUÍDO** - Migrar para cloud storage com segurança |
| **Validações** | ⚠️ Mínimas (apenas campos obrigatórios) | ✅ 10 RNs rigorosas no backend + frontend (RN-CTR-023-01 a 10) | **EVOLUÍDO** - Adicionar validações completas |
| **Auditoria** | ⚠️ Logs textuais (`text.log`) sem estrutura | ✅ Tabela estruturada + JSON de mudanças + hash | **EVOLUÍDO** - Implementar auditoria imutável estruturada |
| **API** | ⚠️ ASMX (XML/SOAP) sem paginação, sem multi-tenancy | ✅ REST (.NET 10) + paginação + multi-tenancy + RBAC | **EVOLUÍDO** - Modernizar para REST API stateless |
| **Frontend** | ⚠️ ASPX (ViewState, PostBack) pesado | ✅ Angular SPA (lazy loading, componentes standalone) | **EVOLUÍDO** - Modernizar para SPA responsivo |
| **Relatórios** | ⚠️ Crystal Reports lento, sem filtros dinâmicos | ✅ BI integrado (ApexCharts) + exportação Excel/PDF | **EVOLUÍDO** - Implementar BI moderno com interatividade |
| **Segurança** | ⚠️ Básica (sem RBAC robusto, sem CSRF, sem rate limiting) | ✅ RBAC + CSRF + Rate Limiting + SQL Injection protection | **EVOLUÍDO** - Implementar segurança completa (10 proteções) |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Multi-Database para Single Database com Multi-Tenancy

**Descrição:** Sistema legado tinha um banco SQL Server por cliente. Sistema moderno centraliza todos os clientes em um único banco com isolamento por `ClienteId`.

**Motivo:** Reduzir custos de infraestrutura, simplificar manutenção, backup e deploy. Row-Level Security garante isolamento equivalente.

**Impacto:** ALTO - Exige migração de dados de múltiplos bancos para banco único, validação rigorosa de queries para evitar vazamento de dados entre clientes.

**Riscos Mitigados:** Row-Level Security no banco + middleware validando ClienteId + auditoria de tentativas de acesso cruzado.

---

### Decisão 2: Substituir Hard Delete por Soft Delete

**Descrição:** Sistema legado executava `DELETE FROM` físico. Sistema moderno marca `IsDeleted = true` e preserva dados.

**Motivo:** Compliance (LGPD exige retenção de 7 anos), auditoria, possibilidade de recuperação de erros operacionais.

**Impacto:** MÉDIO - Todas as queries devem filtrar `WHERE IsDeleted = false`. Extension method criado para automação.

**Riscos Mitigados:** Filtro automático via extension method `IncluindoAtivos()` garante que dados deletados não apareçam por engano.

---

### Decisão 3: Migrar de ASMX para REST API

**Descrição:** Webservices ASMX (XML/SOAP) substituídos por REST API (.NET 10) com JSON.

**Motivo:** Performance (JSON mais leve que XML), padrão moderno da indústria, melhor integração com Angular e ferramentas de desenvolvimento.

**Impacto:** ALTO - Reescrever todos os endpoints, ajustar contratos de dados (DTOs), testar integração com frontend.

**Riscos Mitigados:** Testes automatizados de integração (backend + frontend) garantem compatibilidade.

---

### Decisão 4: Migrar de ASPX para Angular SPA

**Descrição:** Telas ASPX (server-side rendering) substituídas por Angular 19 SPA com componentes standalone.

**Motivo:** Performance (lazy loading, menos tráfego), UX moderna (responsiva, interativa), separação frontend/backend.

**Impacto:** ALTO - Reescrever todas as telas, ajustar workflows, treinar equipe em Angular/TypeScript.

**Riscos Mitigados:** Implementação gradual (RF por RF), testes E2E (Playwright) garantem paridade de funcionalidades.

---

### Decisão 5: Implementar Workflow de Aprovação com State Machine

**Descrição:** Estados fixos do legado (4 estados) substituídos por State Machine com 10 estados e transições validadas.

**Motivo:** Atender requisitos de governança corporativa (alçadas de valor), rastrear aprovações, evitar transições inválidas.

**Impacto:** MÉDIO - Criar State Machine, implementar validações de transição, ajustar UX para refletir estados.

**Riscos Mitigados:** Testes unitários de transições + auditoria de mudanças de estado garantem conformidade.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de Dados na Migração Multi-Database → Single Database** | CRÍTICO | Script de migração com validação linha a linha, comparação de checksums, ambiente de teste antes de PRD |
| **Queries Sem Filtro de ClienteId (Vazamento de Dados)** | CRÍTICO | Code Review obrigatório, validador estático (Roslyn Analyzer), testes de segurança automatizados |
| **Performance Degradada com Multi-Tenancy (Row-Level Security)** | ALTO | Índices otimizados em ClienteId, particionamento de tabela se necessário, monitoramento de slow queries |
| **Incompatibilidade de Anexos (Pasta Compartilhada → Blob Storage)** | MÉDIO | Migração de arquivos com validação de CRC32, manter pasta compartilhada temporariamente como fallback |
| **Usuários Não Adaptados ao Workflow de Aprovação** | MÉDIO | Treinamento, documentação, mensagens claras na UX explicando estado atual e próximas ações |
| **Jobs de Renovação/Reajuste com Falhas Não Detectadas** | ALTO | Monitoramento (Application Insights), alertas de falha, retry automático, notificação admin |
| **Dependências Entre Contratos e Medições Não Identificadas** | MÉDIO | Validador de dependências antes de soft delete, relatórios de contratos órfãos |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|-----------------------|
| **Tabela dbo.Contrato** | RF-023 - Seção 7 (Modelo de Dados) / MD-RF023.md |
| **Tela Contrato.aspx** | RF-023 - UC01 (Criar Contrato), UC02 (Editar Contrato) |
| **Tela ContratoLista.aspx** | RF-023 - UC03 (Consultar Contrato) |
| **Tela ContratoAnexos.aspx** | RF-023 - UC06 (Gestão de Anexos) |
| **Webservice WSContrato.asmx** | RF-023 - Seção 8 (API Endpoints) |
| **Procedure pa_ContratoBuscarTodos** | RF-023 - RN-CTR-023-09 (Multi-tenancy) / GET /api/contratos |
| **Procedure pa_ContratoInserir** | RF-023 - RN-CTR-023-01, RN-CTR-023-02 / POST /api/contratos |
| **Procedure pa_ContratoDeletar** | RF-023 - RN-CTR-023-06, RN-CTR-023-10 / DELETE /api/contratos/{id} |
| **Job SQL ContratoRenovacaoAutomatica** | RF-023 - RN-CTR-023-03 (Renovação Automática) |
| **Job SQL ContratoAlertasVencimento** | RF-023 - RN-CTR-023-04 (Alertas Automáticos) |
| **Reajuste Manual via DBA** | RF-023 - RN-CTR-023-07 (Reajuste Automático) |
| **Workflow Simplificado (4 estados)** | RF-023 - RN-CTR-023-05 (Workflow por Alçada) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do RL-RF023 com separação completa RF/RL, 7 seções obrigatórias, destinos definidos | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**Revisão**: Pendente

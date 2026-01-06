# RL-RF024 — Referência ao Legado: Gestão de Departamentos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-024
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado de departamentos que serve de base para a modernização, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

O sistema legado de gestão de departamentos foi implementado em **ASP.NET Web Forms** com código VB.NET e SQL Server, apresentando uma arquitetura **monolítica flat** (sem hierarquia recursiva).

### Stack Tecnológica

- **Framework:** ASP.NET Web Forms 4.x (.NET Framework 4.7.2)
- **Linguagem:** VB.NET (Visual Basic .NET)
- **Banco de Dados:** SQL Server 2012 (múltiplos bancos por cliente)
- **Webservices:** SOAP (.asmx) com código VB.NET
- **Interface:** DataGridView VB.NET, controles server-side ASP.NET
- **Autenticação:** Forms Authentication (Session-based)
- **Deploy:** IIS 7.5+ com Application Pools isolados

### Arquitetura Geral

- **Tipo:** Monolito multi-database (1 banco SQL Server por cliente)
- **Estrutura:** Flat (sem hierarquia recursiva) - lista simples de departamentos
- **Lotação:** Campo único `Usuario.Id_Departamento` (FK simples, não suporta estrutura matricial)
- **Organograma:** INEXISTENTE - retorna `NotImplementedException`
- **Sincronização AD:** INEXISTENTE - grupos criados manualmente via PowerShell
- **Movimentações:** INEXISTENTE - UPDATE direto sem workflow, sem histórico

### Problemas Arquiteturais Identificados

1. ❌ **Estrutura Flat Sem Hierarquia**: Tabela `Departamento` sem campo `Id_Departamento_Pai` - impossível modelar Diretoria > Gerência > Coordenação
2. ❌ **Lotação Única**: Campo `Usuario.Id_Departamento` FK simples - não suporta estrutura matricial (dotted-line)
3. ❌ **Sem Organograma Visual**: Funcionalidade inexistente - WebMethod `ObterOrganograma()` retorna `NotImplementedException`
4. ❌ **Sem Sincronização AD**: Grupos Active Directory criados manualmente via PowerShell - inconsistências frequentes
5. ❌ **Sem Workflow Movimentações**: Transferências executadas via UPDATE direto sem aprovação, sem histórico origem/destino
6. ❌ **Sem Auditoria Temporal**: Impossível rastrear quem moveu colaborador, quando e por quê
7. ❌ **Sem Analytics Headcount**: Campo `Qtd_Colaboradores` inexistente - queries ad-hoc para contar colaboradores
8. ❌ **Multi-Database**: 1 banco SQL Server por cliente - migração dados complexa, sem multi-tenancy moderno
9. ❌ **Sem Cache**: Todas queries executadas diretamente no SQL Server - performance degradada
10. ❌ **Sem Validação Referências Circulares**: Possível criar loops infinitos (A → B → C → A) - sistema trava
11. ❌ **Líder Texto Livre**: Campo `Id_Usuario_Lider` sem FK validada - aceita GUIDs inválidos
12. ❌ **Sem Versionamento Estrutura**: Mudanças hierarquia sobrescrevem dados - impossível rollback

---

## 2. TELAS ASPX E CÓDIGO-BEHIND

### Tela: Departamento.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastros/Departamento.aspx`
- **Responsabilidade:** Lista flat de departamentos ordenada alfabeticamente, CRUD básico sem hierarquia

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| txtNome | TextBox | Sim | Nome departamento (max 200 caracteres) |
| txtSigla | TextBox | Não | Sigla departamento (max 10 caracteres) |
| ddlLider | DropDownList | Não | Líder do departamento (FK Usuario) - **SEM validação se usuário existe** |
| ddlStatus | DropDownList | Sim | Status: Ativo/Inativo (enum string) |

#### Comportamentos Implícitos (Code-Behind VB.NET)

1. **Validação Código Único Ausente**: Não valida duplicidade `Codigo_Departamento` por Fornecedor - permite cadastros duplicados
2. **Líder Sem Validação FK**: Aceita GUID inválido em `Id_Usuario_Lider` - campo texto livre sem verificação `IF EXISTS (SELECT 1 FROM Usuario WHERE Id = @IdLider)`
3. **Listagem Flat Alfabética**: Query `SELECT * FROM Departamento ORDER BY Nome` - sem hierarquia visual (Diretoria > Gerência)
4. **Sem Organograma**: Botão "Visualizar Organograma" desabilitado com tooltip "Funcionalidade não disponível"
5. **Sem Histórico Movimentações**: Transferir colaborador executa `UPDATE Usuario SET Id_Departamento = @NovoId WHERE Id = @UsrId` - perde origem
6. **Sem Validação Dependências**: Permite excluir departamento com colaboradores ativos - FK violation error genérico
7. **Sem Cache**: Cada request executa `SELECT COUNT(*) FROM Usuario WHERE Id_Departamento = @Id` para contar colaboradores - N+1 queries

#### Funcionalidades Principais

- **Listar**: DataGridView flat ordenado alfabeticamente por Nome
- **Criar**: INSERT departamento sem validação código único
- **Editar**: UPDATE departamento sem auditoria mudanças
- **Excluir**: DELETE físico (não soft delete) - FK violation se houver colaboradores
- **Transferir Colaborador**: UPDATE Usuario.Id_Departamento direto sem workflow

**DESTINO**: SUBSTITUÍDO - Sistema moderno implementa hierarquia recursiva, organograma D3.js, workflow movimentações, validação referências circulares

---

### Tela: Colaborador_Departamento.aspx (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui tela dedicada para lotações. Lotação gerenciada diretamente em `Usuario.aspx` via dropdown único `ddlDepartamento` (FK simples).

**DESTINO**: NOVO - Sistema moderno cria tabela `Usuario_Departamento` N:N para estrutura matricial (principal + dotted-line)

---

## 3. WEBSERVICES (.asmx)

### WebService: DepartamentoService.asmx

- **Caminho:** `ic1_legado/IControlIT/Services/DepartamentoService.asmx`
- **Responsabilidade:** SOAP webservice para integrações externas (ERPs, BI, folha pagamento)

#### Métodos Públicos

| Método | Parâmetros | Retorno | Observações |
|------|------------|---------|-------------|
| `CadastrarDepartamento` | nome: String, sigla: String | Guid | **PROBLEMA:** Não aceita `Id_Departamento_Pai` - estrutura flat |
| `AlocarUsuarioDepartamento` | idUsuario: Guid, idDepartamento: Guid | Boolean | **PROBLEMA:** Sem percentual alocação, sem dotted-line |
| `ListarDepartamentos` | (sem parâmetros) | DataSet | **PROBLEMA:** Lista flat sem hierarquia recursiva |
| `ObterOrganograma` | (sem parâmetros) | String (XML) | **PROBLEMA:** Retorna `NotImplementedException` |
| `TransferirColaborador` | idUsuario: Guid, idDepartamentoDestino: Guid | Boolean | **PROBLEMA:** Sem workflow aprovação, sem histórico |
| `SincronizarActiveDirectory` | (sem parâmetros) | Boolean | **PROBLEMA:** Retorna `NotImplementedException` |

#### Comportamentos Implícitos

##### Método: CadastrarDepartamento

```vb
<WebMethod()> Public Function CadastrarDepartamento(ByVal nome As String, ByVal sigla As String) As Guid
    ' ❌ PROBLEMA: Flat structure - sem suporte Id_Departamento_Pai
    ' ❌ PROBLEMA: Sem validação código único por Fornecedor
    ' ❌ PROBLEMA: Sem campo Id_Usuario_Lider validado (FK Usuario)
    Dim idDepartamento As Guid = Guid.NewGuid()
    Dim sql As String = "INSERT INTO Departamento (Id_Departamento, Nome, Sigla, Status) VALUES (@Id, @Nome, @Sigla, 'Ativo')"
    ExecutarSQL(sql) ' ❌ SQL inline sem EF Core, sem parametrização adequada
    Return idDepartamento
End Function
```

**Regras Implícitas Extraídas:**
1. Código departamento gerado automaticamente como GUID - não usa formato alfanumérico [TIPO]-[NOME]
2. Status padrão "Ativo" hard-coded
3. Sem validação unicidade Nome por Fornecedor
4. Sem criação automática grupo Active Directory

**DESTINO**: SUBSTITUÍDO - Sistema moderno usa `CreateDepartamentoCommand` com FluentValidation, formato código [TIPO]-[NOME], FK líder validada, hierarquia recursiva

---

##### Método: AlocarUsuarioDepartamento

```vb
<WebMethod()> Public Function AlocarUsuarioDepartamento(ByVal idUsuario As Guid, ByVal idDepartamento As Guid) As Boolean
    ' ❌ PROBLEMA: Sem suporte dotted-line (estrutura matricial)
    ' ❌ PROBLEMA: Sem percentual alocação
    ' ❌ PROBLEMA: Sem validação soma alocações ≤100%
    ' ❌ PROBLEMA: Sem histórico temporal (Dt_Inicio/Dt_Fim)
    Dim sql As String = "UPDATE Usuario SET Id_Departamento = @IdDept WHERE Id_Usuario = @IdUsr"
    ExecutarSQL(sql) ' ❌ Campo único FK, não suporta múltiplos departamentos
    Return True
End Function
```

**Regras Implícitas Extraídas:**
1. Lotação única por colaborador - não suporta estrutura matricial
2. UPDATE sobrescreve lotação anterior - perde histórico origem
3. Sem validação se colaborador já está lotado em outro departamento ativo
4. Sem notificação líder do departamento sobre nova lotação

**DESTINO**: SUBSTITUÍDO - Sistema moderno usa tabela `Usuario_Departamento` N:N, trigger valida SUM(Percentual_Alocacao)<=100%, notificação multicanal líder

---

##### Método: ListarDepartamentos

```vb
<WebMethod()> Public Function ListarDepartamentos() As DataSet
    ' ❌ PROBLEMA: Sem hierarquia recursiva
    ' ❌ PROBLEMA: Sem caminho hierárquico completo (breadcrumb)
    ' ❌ PROBLEMA: Sem qtd_colaboradores calculada
    Dim sql As String = "SELECT Id_Departamento, Nome, Sigla, Status FROM Departamento WHERE Status='Ativo' ORDER BY Nome"
    Return ExecutarQuery(sql) ' ❌ Lista flat, sem relacionamento pai/filho
End Function
```

**Regras Implícitas Extraídas:**
1. Retorna apenas departamentos ativos (Status='Ativo') - sem flag `Fl_Ativo` booleano
2. Ordenação alfabética por Nome - sem ordenação hierárquica (nível, caminho)
3. Retorna DataSet ADO.NET - sem DTO tipado, sem paginação
4. Sem filtros por tipo departamento (Diretoria, Gerencia, Coordenacao)

**DESTINO**: SUBSTITUÍDO - Sistema moderno usa `GetDepartamentosQuery` com paginação, filtros (tipo, nível, líder), DTO tipado, CTE recursivo hierarquia

---

##### Método: ObterOrganograma

```vb
<WebMethod()> Public Function ObterOrganograma() As String
    ' ❌ PROBLEMA: Organograma inexistente - retorna erro
    Throw New NotImplementedException("Organograma não disponível no sistema legado")
End Function
```

**Regras Implícitas Extraídas:**
1. Funcionalidade organograma visual NUNCA foi implementada no legado
2. Usuários visualizam lista flat alfabética em DataGridView
3. Estrutura hierárquica gerenciada mentalmente pelos gestores RH

**DESTINO**: NOVO - Sistema moderno implementa organograma D3.js interativo (zoom, pan, collapse/expand, busca, export PNG/PDF)

---

##### Método: TransferirColaborador

```vb
<WebMethod()> Public Function TransferirColaborador(ByVal idUsuario As Guid, ByVal idDepartamentoDestino As Guid) As Boolean
    ' ❌ PROBLEMA: Sem workflow aprovação líder origem
    ' ❌ PROBLEMA: Sem histórico movimentação (origem/destino/motivo/data)
    ' ❌ PROBLEMA: Sem notificação líderes envolvidos (origem/destino)
    ' ❌ PROBLEMA: Sem validação se departamento destino existe
    Dim sql As String = "UPDATE Usuario SET Id_Departamento = @IdDept WHERE Id_Usuario = @IdUsr"
    ExecutarSQL(sql) ' ❌ Update direto sem auditoria, sem compliance
    Return True
End Function
```

**Regras Implícitas Extraídas:**
1. Transferência executada imediatamente sem aprovação
2. Sem campo `Motivo` obrigatório - impossível rastrear justificativa
3. Sem registro tabela `Departamento_Movimentacao` - histórico perdido
4. Sem atualização `Qtd_Colaboradores` departamentos origem/destino
5. Sem sincronização Active Directory - grupos AD ficam desatualizados

**DESTINO**: SUBSTITUÍDO - Sistema moderno implementa workflow aprovação multinível (Líder Origem → Líder Destino → RH), tabela Movimentacao, notificações, sincronização Azure AD

---

##### Método: SincronizarActiveDirectory

```vb
<WebMethod()> Public Function SincronizarActiveDirectory() As Boolean
    ' ❌ PROBLEMA: Sincronização AD inexistente
    ' ❌ PROBLEMA: Sem Microsoft Graph API
    ' ❌ PROBLEMA: Sem LDAP integration
    Throw New NotImplementedException("Sincronização AD não disponível")
End Function
```

**Regras Implícitas Extraídas:**
1. Grupos Active Directory criados manualmente via console AD / PowerShell
2. Membros adicionados manualmente - alta chance de inconsistência
3. Sem automação sincronização - TI executa scripts PowerShell mensalmente
4. Sem log ou rastreabilidade das sincronizações manuais

**DESTINO**: NOVO - Sistema moderno implementa job Hangfire diário (Cron "0 3 * * *"), Microsoft Graph SDK .NET, autenticação Client Credentials Flow, permissões Group.ReadWrite.All

---

## 4. STORED PROCEDURES

### SP: sp_ListarDepartamentos

- **Caminho:** Database `IControlIT_Cliente01` > Programmability > Stored Procedures > `dbo.sp_ListarDepartamentos`
- **Parâmetros Entrada:** `@Status` VARCHAR(20) = 'Ativo'
- **Parâmetros Saída:** Nenhum (retorna resultset)

#### Lógica Principal (Linguagem Natural)

Procedure retorna lista flat de departamentos filtrados por status. Campos retornados: Id_Departamento, Nome, Sigla, Id_Usuario_Lider (GUID texto livre sem validação), Status, Dt_Cadastro. Ordenação alfabética por Nome. SEM JOIN com tabela Usuario para validar líder. SEM cálculo `Qtd_Colaboradores`. SEM caminho hierárquico. SEM paginação - retorna TODAS linhas (problema performance > 1000 departamentos).

**DESTINO**: SUBSTITUÍDO - Sistema moderno usa EF Core LINQ com `Skip().Take()` paginação, Include(Lider), Include(DepartamentosFilhos), filtros dinâmicos (tipo, nível, líder), ordenação hierárquica

---

### SP: sp_TransferirColaborador (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui stored procedure dedicada para transferências. Transferências executadas via UPDATE inline no WebMethod `TransferirColaborador`.

**DESTINO**: NOVO - Sistema moderno cria procedure auxiliar `sp_CalcularHeadcountDepartamento` usada por trigger, mas lógica transferência em Application Layer (CQRS Command Handler)

---

### SP: sp_ObterHierarquiaDepartamento (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui CTE recursivo para hierarquia. Estrutura flat impossibilita query recursiva.

**DESTINO**: NOVO - Sistema moderno cria view `VW_Departamento_Hierarquia_Completa` com CTE recursivo retornando árvore completa para organograma

---

## 5. TABELAS LEGADAS

### Tabela: Departamento

| Campo | Tipo | Nullable | Observações |
|-------|------|----------|-------------|
| Id_Departamento | UNIQUEIDENTIFIER | NOT NULL (PK) | Primary Key clustered |
| Nome | NVARCHAR(200) | NOT NULL | Nome departamento |
| Sigla | NVARCHAR(10) | NULL | Sigla opcional |
| Id_Usuario_Lider | UNIQUEIDENTIFIER | NULL | **FK não validada** - aceita GUIDs inválidos |
| Status | NVARCHAR(20) | NOT NULL | Enum string: 'Ativo'/'Inativo' (sem constraint CHECK) |
| Dt_Cadastro | DATETIME | NOT NULL DEFAULT GETDATE() | Data criação |
| Dt_Atualizacao | DATETIME | NULL | Data última atualização |

#### Problemas Identificados

1. ❌ **Falta campo `Id_Departamento_Pai`**: Impossível modelar hierarquia recursiva (Diretoria > Gerência > Coordenação)
2. ❌ **Falta campo `Nivel_Hierarquia`**: Impossível filtrar por nível ou ordenar hierarquicamente
3. ❌ **Falta campo `Caminho_Hierarquico`**: Impossível exibir breadcrumb ("TI > Desenvolvimento > Backend")
4. ❌ **Falta campo `Tipo_Departamento`**: Impossível filtrar por tipo (Diretoria, Gerencia, Coordenacao, Equipe)
5. ❌ **Falta campo `Qtd_Colaboradores`**: Queries ad-hoc contam colaboradores - performance ruim
6. ❌ **Falta campos Azure AD**: `Azure_AD_Object_Id`, `AD_Distinguished_Name`, `Dt_Ultima_Sincronizacao_AD` inexistentes
7. ❌ **FK `Id_Usuario_Lider` sem validação**: Constraint FK não criada - aceita GUIDs inexistentes
8. ❌ **Campo `Status` enum string**: Sem constraint CHECK - aceita valores inválidos ('ativo', 'ATIVO', 'Active')
9. ❌ **Sem soft delete**: Sem flag `Fl_Ativo` booleano - exclusão física (DELETE) causa FK violations
10. ❌ **Sem campos auditoria**: Falta `Id_Usuario_Criacao`, `Dt_Criacao`, `Id_Usuario_Atualizacao`, `Dt_Atualizacao` padronizados
11. ❌ **Sem multi-tenancy**: Falta `Id_Fornecedor` - banco por cliente (migração complexa)

**DESTINO**: SUBSTITUÍDO - Tabela `Departamento` redesenhada com campos hierarquia (IdDepartamentoPai, NivelHierarquia, CaminhoHierarquico), Azure AD (AzureADObjectId), multi-tenancy (IdFornecedor), soft delete (FlAtivo), auditoria (Created, CreatedBy, LastModified, LastModifiedBy)

---

### Tabela: Usuario (Campo Id_Departamento)

| Campo | Tipo | Nullable | Observações |
|-------|------|----------|-------------|
| Id_Usuario | UNIQUEIDENTIFIER | NOT NULL (PK) | Primary Key |
| Nome | NVARCHAR(200) | NOT NULL | Nome colaborador |
| Email | NVARCHAR(100) | NOT NULL UNIQUE | Email corporativo |
| Id_Departamento | UNIQUEIDENTIFIER | NULL | **FK única** - não suporta dotted-line |

#### Problemas Identificados

1. ❌ **FK única**: Campo `Id_Departamento` FK simples - não suporta estrutura matricial (colaborador em múltiplos departamentos)
2. ❌ **Sem percentual alocação**: Impossível alocar colaborador 70% GER-PROJETOS + 30% GER-DEV
3. ❌ **Sem tipo lotação**: Impossível diferenciar lotação Principal vs Dotted-Line vs Temporária
4. ❌ **Sem vigência temporal**: Falta `Dt_Inicio`, `Dt_Fim` - impossível rastrear quando colaborador entrou/saiu departamento
5. ❌ **UPDATE sobrescreve**: Mudar `Id_Departamento` perde histórico origem - impossível gerar relatórios movimentações

**DESTINO**: SUBSTITUÍDO - Campo `Usuario.Id_Departamento` removido. Criada tabela `Usuario_Departamento` N:N com campos: Tipo_Lotacao, Percentual_Alocacao, Dt_Inicio, Dt_Fim, Fl_Ativo

---

### Tabela: Departamento_Movimentacao (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui tabela histórico movimentações. Transferências executadas via UPDATE direto `Usuario.Id_Departamento` sem rastreabilidade.

#### Problemas Identificados

1. ❌ **Sem histórico**: Impossível rastrear origem/destino/data de transferências anteriores
2. ❌ **Sem workflow**: Impossível aprovar/rejeitar movimentações - UPDATE executado imediatamente
3. ❌ **Sem campo Motivo**: Impossível justificar transferências para compliance (eSocial, RAIS)
4. ❌ **Sem aprovadores**: Impossível rastrear quem aprovou transferência (Líder Origem, Líder Destino, RH)
5. ❌ **Sem cálculo turnover**: Impossível gerar analytics rotatividade departamental sem histórico saídas

**DESTINO**: NOVO - Tabela `Departamento_Movimentacao` criada com campos: Id_Usuario, Id_Departamento_Origem, Id_Departamento_Destino, Tipo_Movimentacao (enum), Status_Aprovacao (enum), Motivo (NVARCHAR(1000) obrigatório), Dt_Efetivacao, 3 FKs aprovadores (Origem, Destino, RH)

---

### Tabela: Departamento_Historico (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui versionamento estrutura organizacional. Mudanças hierarquia sobrescrevem dados sem possibilidade rollback.

**DESTINO**: NOVO - Tabela `Departamento_Historico` append-only criada com campos: Id_Historico, Id_Departamento, Tipo_Evento (enum: Criacao/Alteracao/Exclusao/Movimentacao_Hierarquia/Mudanca_Lider), Dt_Evento, Id_Usuario_Responsavel, Valores_JSON_Antes, Valores_JSON_Depois, Descricao

---

### View: VW_Departamento_Hierarquia_Completa (NÃO EXISTE)

**INEXISTENTE** - Sistema legado NÃO possui view CTE recursivo para hierarquia. Estrutura flat impossibilita query recursiva.

**DESTINO**: NOVO - View `VW_Departamento_Hierarquia_Completa` criada com CTE recursivo:
```sql
WITH CTE_Hierarquia AS (
    -- Raiz (nível 1)
    SELECT Id_Departamento, Nome, Id_Departamento_Pai, 1 AS Nivel, CAST(Nome AS NVARCHAR(500)) AS Caminho
    FROM Departamento WHERE Id_Departamento_Pai IS NULL
    UNION ALL
    -- Recursão (filhos)
    SELECT d.Id_Departamento, d.Nome, d.Id_Departamento_Pai, h.Nivel + 1, CAST(h.Caminho + ' > ' + d.Nome AS NVARCHAR(500))
    FROM Departamento d INNER JOIN CTE_Hierarquia h ON d.Id_Departamento_Pai = h.Id_Departamento
)
SELECT * FROM CTE_Hierarquia
```

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### RL-RN-001: Código Departamento Sem Validação Unicidade

**Localização:** `Departamento.aspx.vb` - Event handler `btnSalvar_Click` - Linha 78

**Descrição:** Sistema legado NÃO valida se código departamento já existe para o Fornecedor. Permite cadastrar múltiplos departamentos com mesmo código "DIR-TI" causando ambiguidade em relatórios e inconsistência referencial.

**DESTINO**: ASSUMIDO - Regra migrada para `RN-RF024-001` com validação FluentValidation + constraint UNIQUE (Codigo_Departamento, Id_Fornecedor)

---

### RL-RN-002: Líder Pode Ser GUID Inválido

**Localização:** `DepartamentoService.asmx.vb` - Método `CadastrarDepartamento` - Linha 45

**Descrição:** Campo `Id_Usuario_Lider` aceita qualquer GUID sem verificar `IF EXISTS (SELECT 1 FROM Usuario WHERE Id_Usuario = @IdLider AND Fl_Ativo = 1)`. Sistema permite cadastrar departamento com líder inexistente ou inativo, causando erro 500 ao tentar carregar dropdown "Líder" na tela de edição.

**DESTINO**: ASSUMIDO - Regra migrada para `RN-RF024-004` com FK validada em EF Core, FluentValidation `Must(BeValidUsuario)`, HTTP 422 se líder inválido

---

### RL-RN-003: Transferência Sem Aprovação Líder

**Localização:** `DepartamentoService.asmx.vb` - Método `TransferirColaborador` - Linha 112

**Descrição:** Transferências interdepartamentais executadas via `UPDATE Usuario SET Id_Departamento = @IdDest WHERE Id_Usuario = @IdUsr` sem aprovação líder origem ou destino. Qualquer usuário com permissão "Admin" pode transferir colaboradores unilateralmente sem notificar gestores envolvidos, causando desorganização equipes.

**DESTINO**: SUBSTITUÍDO - Regra redesenhada em `RN-RF024-006` com workflow aprovação multinível sequencial (Pendente → Aprovado_Origem → Aprovado_Destino → Aprovado_RH), notificações multicanal, tabela Movimentacao

---

### RL-RN-004: Lotação Única Sobrescreve Histórico

**Localização:** `DepartamentoService.asmx.vb` - Método `AlocarUsuarioDepartamento` - Linha 88

**Descrição:** Campo único `Usuario.Id_Departamento` atualizado via `UPDATE` sobrescreve lotação anterior sem manter histórico. Impossível rastrear em qual departamento colaborador estava alocado em 01/01/2024 para auditoria trabalhista (eSocial) ou calcular tempo de permanência por departamento.

**DESTINO**: SUBSTITUÍDO - Regra redesenhada em tabela `Usuario_Departamento` N:N com campos `Dt_Inicio`, `Dt_Fim`, `Fl_Ativo`. Lotação antiga desativada (`Fl_Ativo=0`), nova criada (`Fl_Ativo=1`), histórico completo preservado

---

### RL-RN-005: Organograma Retorna NotImplementedException

**Localização:** `DepartamentoService.asmx.vb` - Método `ObterOrganograma` - Linha 134

**Descrição:** WebMethod `ObterOrganograma()` retorna `Throw New NotImplementedException("Organograma não disponível no sistema legado")`. Funcionalidade organograma visual NUNCA foi implementada. Usuários visualizam lista flat de departamentos ordenada alfabeticamente em DataGridView - estrutura hierárquica gerenciada mentalmente por gestores RH via planilhas Excel externas.

**DESTINO**: NOVO - Funcionalidade implementada do zero em `RN-RF024-009` com organograma D3.js interativo (zoom, pan, collapse/expand, busca, filtro por tipo, export PNG/PDF/SVG), endpoint GET `/api/v1/departamentos/organograma` retorna DTO recursivo

---

### RL-RN-006: Sincronização AD Manual PowerShell

**Localização:** `DepartamentoService.asmx.vb` - Método `SincronizarActiveDirectory` - Linha 156

**Descrição:** WebMethod `SincronizarActiveDirectory()` retorna `Throw New NotImplementedException("Sincronização AD não disponível")`. Grupos Active Directory criados manualmente via console AD ou scripts PowerShell executados mensalmente por TI. Alta taxa de inconsistência entre departamentos sistema e grupos AD (departamentos deletados com grupos AD órfãos, colaboradores em grupo AD errado).

**DESTINO**: NOVO - Funcionalidade implementada do zero em `RN-RF024-005` com job Hangfire diário (Cron "0 3 * * *"), Microsoft Graph SDK .NET, autenticação Client Credentials Flow, permissões `Group.ReadWrite.All` + `User.Read.All`, armazenamento `Azure_AD_Object_Id` após criação grupo

---

### RL-RN-007: Sem Validação Soma Alocações ≤100%

**Localização:** (NÃO EXISTE - estrutura matricial inexistente)

**Descrição:** Sistema legado não suporta estrutura matricial dotted-line. Colaborador pode estar lotado em APENAS UM departamento (FK única `Usuario.Id_Departamento`). Impossível alocar colaborador 70% GER-PROJETOS + 30% GER-DEV para projetos temporários.

**DESTINO**: NOVO - Regra criada em `RN-RF024-007` com tabela `Usuario_Departamento` N:N, campo `Percentual_Alocacao` DECIMAL(5,2) CHECK (>0 AND <=100), trigger `trg_Usuario_Departamento_ValidarAlocacao` valida `SUM(Percentual_Alocacao) WHERE Id_Usuario = @Id AND Fl_Ativo = 1 <= 100`, ROLLBACK se exceder

---

### RL-RN-008: Sem Dashboard Headcount Tempo Real

**Localização:** (NÃO EXISTE - funcionalidade inexistente)

**Descrição:** Sistema legado não possui dashboard headcount tempo real. Gestores RH executam queries ad-hoc SQL Server Management Studio para contar colaboradores por departamento: `SELECT Id_Departamento, COUNT(*) FROM Usuario GROUP BY Id_Departamento`. Dados desatualizados (snapshot manual), sem visualização gráfica, sem KPIs (taxa ocupação, variação mês anterior, projeção).

**DESTINO**: NOVO - Funcionalidade criada em `RN-RF024-011` com SignalR Hub `DepartamentoHub`, evento `OnHeadcountAtualizado` broadcast após movimentações, frontend Chart.js (line chart 12 meses, gauge chart taxa ocupação com cores: Verde ≥90%, Amarelo 75-89%, Vermelho <75%)

---

### RL-RN-009: Sem Analytics Turnover Departamental

**Localização:** (NÃO EXISTE - funcionalidade inexistente)

**Descrição:** Sistema legado não calcula turnover (rotatividade) departamental. Impossível identificar departamentos com alta taxa de saída colaboradores (>15% trimestre) para ação preventiva RH. Relatórios turnover gerados manualmente em planilhas Excel importando dados SQL Server.

**DESTINO**: NOVO - Funcionalidade criada em `RN-RF024-012` com cálculo automático: `Turnover = (Saídas_Últimos_12_Meses / Headcount_Médio_Últimos_12_Meses) * 100`, benchmark <10% ao ano, alertas automáticos se >15% trimestre → notificação email RH + Diretor, dashboard Chart.js (bar chart comparativo todos departamentos, line chart evolução 12 meses)

---

### RL-RN-010: Sem Relatório Movimentações RH Compliance

**Localização:** (NÃO EXISTE - funcionalidade inexistente)

**Descrição:** Sistema legado não gera relatório consolidado movimentações interdepartamentais para compliance fiscal/trabalhista (eSocial, RAIS). RH exporta manualmente dados SQL Server para Excel via SSMS, formata 4 abas (Transferências, Promoções, Realocações, Temporárias), envia para contador. Processo manual semanal consome 8 horas/mês RH.

**DESTINO**: NOVO - Funcionalidade criada em `RN-RF024-013` com job Hangfire Cron "0 8 1 * *" (1º dia útil mês 08:00), geração automática Excel EPPlus 4 abas, colunas (Colaborador, Matrícula, Origem, Destino, Data, Cargo Anterior, Cargo Novo, Motivo, Aprovadores), storage Azure Blob `relatorios-rh/{ano}/{mes}/movimentacoes-{ano}-{mes}.xlsx`, retenção 7 anos LGPD

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Estrutura Hierárquica** | Flat (lista simples) | Recursiva ilimitada (Id_Departamento_Pai) | **BREAKING CHANGE** - Migração requer script ETL inferir hierarquia via código/nome |
| **Organograma Visual** | INEXISTENTE (`NotImplementedException`) | D3.js interativo (zoom, pan, collapse/expand, export) | **NOVO RECURSO** - Implementação frontend do zero |
| **Lotação Colaboradores** | FK única `Usuario.Id_Departamento` | Tabela N:N `Usuario_Departamento` (principal + dotted-line) | **BREAKING CHANGE** - Todas queries legado precisam JOIN nova tabela |
| **Movimentações** | UPDATE direto sem workflow | Workflow aprovação multinível + histórico | **NOVO RECURSO** - Tabela `Departamento_Movimentacao` criada |
| **Sincronização AD** | Manual PowerShell | Job Hangfire diário + Microsoft Graph API | **NOVO RECURSO** - Integração Azure AD automática |
| **Dashboard Headcount** | Queries ad-hoc SSMS | SignalR tempo real + Chart.js | **NOVO RECURSO** - Dashboard KPIs moderno |
| **Analytics Turnover** | Planilhas Excel manuais | Cálculo automático + alertas | **NOVO RECURSO** - Analytics departamental |
| **Validação Referências Circulares** | INEXISTENTE (permite loops infinitos) | Algoritmo HashSet detecção loops | **NOVA VALIDAÇÃO** - Previne hierarquia inconsistente |
| **Versionamento Estrutura** | INEXISTENTE (sobrescreve sem histórico) | Tabela `Departamento_Historico` append-only | **NOVO RECURSO** - Auditoria completa mudanças organizacionais |
| **Código Departamento** | GUID auto-gerado | Formato alfanumérico [TIPO]-[NOME] | **MUDANÇA FORMATO** - Migração precisa gerar códigos retroativos |
| **Líder FK Validada** | GUID texto livre sem validação | FK Usuario com FluentValidation | **CORREÇÃO BUG** - Impede líderes inválidos |
| **Multi-Tenancy** | 1 banco por cliente | Id_Fornecedor em tabela única | **BREAKING CHANGE** - Migração consolida múltiplos bancos |
| **Soft Delete** | DELETE físico (FK violations) | Fl_Ativo flag (soft delete) | **MUDANÇA PADRÃO** - Preserva histórico |
| **Auditoria** | Campos Created/Updated básicos | EF Core SaveChangesInterceptor + JSON snapshot | **MELHORIA** - Rastreabilidade completa |
| **Paginação** | INEXISTENTE (retorna TODAS linhas) | Skip().Take() + PaginatedListDto | **NOVA FUNCIONALIDADE** - Performance > 1000 registros |
| **Cache** | INEXISTENTE (query direta SQL) | Redis cache TTL 1h (organograma) | **NOVA FUNCIONALIDADE** - Performance otimizada |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação completa referência ao legado (memória técnica) | Agência ALC - alc.dev.br |

# RL-RF022 — Referência ao Legado: Gestão de Fornecedores

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-022
**Sistema Legado:** IControlIT (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Stack Tecnológica
- **Arquitetura:** Monolítica, ASP.NET Web Forms
- **Linguagem:** VB.NET (code-behind) + SQL Server
- **Framework:** .NET Framework 4.x
- **Banco de Dados:** SQL Server (multi-database por cliente)
- **Multi-tenant:** Parcial (via Id_Conglomerado, mas bancos separados)
- **Auditoria:** Parcial (algumas tabelas de histórico, inconsistente)
- **Configurações:** Web.config + tabelas de configuração

### Problemas Arquiteturais Identificados

1. **Multi-database sem governança**: Cada cliente tinha banco separado, dificultando manutenção
2. **Código misturado**: Lógica de negócio no code-behind VB.NET (telas .aspx.vb)
3. **Falta de API**: Webservices ASMX sem padrão REST
4. **Validações inconsistentes**: Validação ora no frontend, ora no backend, ora ausente
5. **Nomenclatura incorreta**: Erros de digitação em labels (CPNJ, txtTelefone para Observação)
6. **Sem controle de versão adequado**: Difícil rastrear alterações
7. **Auditoria parcial**: Nem todas operações eram auditadas

---

## 2. TELAS DO LEGADO

### Tela: Empresa_Contratada.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\Cadastro\Empresa_Contratada.aspx`

**Responsabilidade:** Cadastro e edição de empresas contratadas (fornecedores/parceiros). Tela simples com apenas 4 campos principais.

#### Campos da Tela

| Campo | Controle | Tipo | Obrigatório | Observações |
|------|----------|------|-------------|-------------|
| Descrição | txtDescricao | TextBox | Sim | Razão social, MaxLength=50, RequiredFieldValidator |
| CNPJ | txtCNPJ | TextBox | Sim | MaxLength=20, Máscara 99.999.999/9999-99, **ERRO: Label escrito "CPNJ"** |
| Contato | txtContato | TextBox | Não | Nome do contato, MaxLength=50 |
| Observação | txtTelefone | TextBox MultiLine | Não | **ERRO: Campo se chama txtTelefone mas label diz Observação**, MaxLength=200 |
| Chave do banco | txtIdentificacao | TextBox ReadOnly | - | Campo técnico laranja (ForeColor=#FF9900) |

#### Botões de Ação
- **Voltar** - Retorna à listagem
- **Novo** - Limpa formulário para novo cadastro
- **Salvar** - Persiste dados (INSERT ou UPDATE)
- **Excluir** - Exclusão física (não soft delete)
- **PDF** - Gera relatório PDF do fornecedor

#### Comportamentos Implícitos

1. **Validação de CNPJ apenas no frontend**: MaskedEditValidator, sem validação backend robusta
2. **Exclusão física**: Ao clicar "Excluir", registro era deletado fisicamente (sem soft delete)
3. **Sem validação de duplicidade**: Permitia cadastrar CNPJ duplicado
4. **Campo ReadOnly laranja**: Exibia ID técnico do banco (não user-friendly)
5. **Sem versionamento**: Não havia controle de versão de registros
6. **Observação sem limite visual**: Campo MultiLine sem contador de caracteres
7. **Sem auditoria de alterações**: Não registrava quem alterou ou quando

#### Destino: SUBSTITUÍDO

**Justificativa:** Tela completamente redesenhada em Angular 19 com:
- Dados cadastrais completos (nome fantasia, IE, IM, CNAE, porte, natureza jurídica)
- Validação CNPJ backend (dígitos verificadores)
- Soft delete (inativação lógica)
- Validação de duplicidade
- Múltiplos contatos (comercial, técnico, financeiro, jurídico)
- Auditoria completa
- Interface moderna responsiva com tabs

**Rastreabilidade:**
- RF Moderno: RF-022 - Seção 4 (Funcionalidades)
- UC Moderno: UC01-RF022 (Criar Fornecedor), UC02-RF022 (Editar Fornecedor)
- Componente Angular: `fornecedores-create.component.ts`, `fornecedores-edit.component.ts`
- Rota Frontend: `/configuracoes/cadastros/fornecedores/create`, `/configuracoes/cadastros/fornecedores/edit/:id`

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WS_Fornecedor.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\WebServices\WS_Fornecedor.asmx`

**Responsabilidade:** Webservice SOAP para operações CRUD de fornecedores.

| Método | Parâmetros | Retorno | Responsabilidade | Observações |
|--------|-----------|---------|------------------|-------------|
| `ListarFornecedores` | idConglomerado (int), tipoFornecedor (string) | List<Fornecedor> | Listar fornecedores por tipo | Sem paginação, retorna tudo |
| `BuscarFornecedor` | idFornecedor (int) | Fornecedor | Buscar por ID | Sem validação multi-tenant |
| `InserirFornecedor` | objFornecedor (Fornecedor) | int (ID inserido) | Criar fornecedor | Validação parcial, sem CNPJ único |
| `AtualizarFornecedor` | objFornecedor (Fornecedor) | bool | Atualizar fornecedor | Sem auditoria de campos alterados |
| `InativarFornecedor` | idFornecedor (int) | bool | Exclusão física | **Não era soft delete** |
| `AdicionarContato` | idFornecedor (int), objContato (Contato) | int | Adicionar contato | Sem validação de contato principal duplicado |

#### Problemas Identificados

1. **SOAP sem padrão REST**: Dificulta integração moderna
2. **Sem autenticação JWT**: Autenticação via session ASP.NET
3. **ListarFornecedores sem paginação**: Performance ruim com muitos registros
4. **Exclusão física**: InativarFornecedor deletava fisicamente
5. **Validações inconsistentes**: InserirFornecedor não validava CNPJ único
6. **Sem versionamento de API**: Alterações quebravam clientes

#### Destino: SUBSTITUÍDO

**Justificativa:** Webservices SOAP substituídos por REST API moderna com:
- Autenticação JWT Bearer
- Paginação obrigatória
- Soft delete
- Validações completas (CNPJ único, dígitos verificadores)
- Versionamento de API (/api/v1/...)
- DTOs tipados
- HTTP status codes padronizados

**Rastreabilidade:**
- RF Moderno: RF-022 - Seção 11 (API Endpoints)
- Endpoints REST: `GET /api/v1/fornecedores`, `POST /api/v1/fornecedores`, etc.
- Handlers CQRS: `CreateFornecedorCommandHandler`, `GetFornecedoresQueryHandler`

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|--------|------------|-------------------------|---------|
| `Fornecedor` | Dados principais do fornecedor | Sem FK para validar relacionamentos, sem campos Created/Modified | **SUBSTITUÍDO** (redesenhada com auditoria) |
| `Fornecedor_Contato` | Contatos do fornecedor | Sem campo `IsPrincipal`, permitia duplicidade | **SUBSTITUÍDO** (adicionado IsPrincipal, TipoContato enum) |
| `Fornecedor_Avaliacao` | Não existia no legado | - | **NOVA** (criada no sistema moderno) |
| `Fornecedor_Documento` | Não existia no legado | - | **NOVA** (criada no sistema moderno) |
| `Fornecedor_Historico` | Não existia no legado | - | **NOVA** (criada para auditoria completa) |

### Detalhamento: Tabela `Fornecedor` (Legado)

**Schema aproximado:**
```sql
CREATE TABLE Fornecedor (
    Id_Fornecedor INT PRIMARY KEY IDENTITY,
    Id_Conglomerado INT,  -- Multi-tenancy parcial
    Descricao VARCHAR(50),  -- Razão Social
    CNPJ VARCHAR(20),
    Contato VARCHAR(50),
    Observacao VARCHAR(200),
    FL_Ativo BIT DEFAULT 1
    -- ❌ Sem Created, CreatedBy, LastModified, LastModifiedBy
    -- ❌ Sem validação FK para Id_Conglomerado
)
```

**Problemas:**
- MaxLength=50 para Descricao (muito curto)
- Sem campos de auditoria
- Sem validação de CNPJ único (permitia duplicatas)
- FL_Ativo sem uso consistente

**Destino: SUBSTITUÍDO**

**Tabela Moderna:**
```sql
CREATE TABLE Fornecedor (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    TenantId UNIQUEIDENTIFIER NOT NULL,  -- FK para Tenant
    Nome NVARCHAR(200) NOT NULL,
    NomeFantasia NVARCHAR(200),
    CNPJ VARCHAR(14),  -- Apenas dígitos
    CPF VARCHAR(11),   -- Para pessoa física
    Tipo NVARCHAR(50) NOT NULL,  -- Enum TipoFornecedor
    Status NVARCHAR(50) DEFAULT 'ATIVO',
    Email NVARCHAR(200),
    Telefone VARCHAR(20),
    NotaGeral DECIMAL(3,2),
    -- Auditoria obrigatória
    Created DATETIME2 NOT NULL,
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    LastModified DATETIME2,
    LastModifiedBy UNIQUEIDENTIFIER,
    -- Soft delete
    IsDeleted BIT DEFAULT 0,
    DeletedAt DATETIME2,
    DeletedBy UNIQUEIDENTIFIER
)
```

**Migration EF Core:** `20251230_CreateFornecedorTable.cs`

---

### Detalhamento: Tabela `Fornecedor_Contato` (Legado)

**Schema aproximado:**
```sql
CREATE TABLE Fornecedor_Contato (
    Id_Contato INT PRIMARY KEY IDENTITY,
    Id_Fornecedor INT,
    Nome VARCHAR(100),
    Cargo VARCHAR(50),
    Telefone VARCHAR(20),
    Email VARCHAR(100)
    -- ❌ Sem campo IsPrincipal
    -- ❌ Sem campo TipoContato (Comercial, Técnico, etc)
)
```

**Problemas:**
- Permitia múltiplos contatos principais do mesmo tipo
- Sem enum TipoContato (valores livres)
- Sem validação de e-mail

**Destino: SUBSTITUÍDO**

**Tabela Moderna:**
```sql
CREATE TABLE FornecedorContato (
    Id UNIQUEIDENTIFIER PRIMARY KEY,
    FornecedorId UNIQUEIDENTIFIER NOT NULL,  -- FK
    TipoContato NVARCHAR(50) NOT NULL,  -- Enum: COMERCIAL, TECNICO, FINANCEIRO, JURIDICO
    Nome NVARCHAR(100) NOT NULL,
    Cargo NVARCHAR(100),
    TelefoneFixo VARCHAR(20),
    TelefoneCelular VARCHAR(20),
    Email NVARCHAR(200),
    IsPrincipal BIT DEFAULT 0,
    -- Auditoria
    Created DATETIME2 NOT NULL,
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    LastModified DATETIME2,
    LastModifiedBy UNIQUEIDENTIFIER
)
```

**Migration EF Core:** `20251230_CreateFornecedorContatoTable.cs`

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras descobertas no código VB.NET que NÃO estavam documentadas:

### RL-RN-001: CNPJ opcional
**Localização:** `Empresa_Contratada.aspx.vb` - Método `btnSalvar_Click`
**Descrição:** CNPJ era obrigatório no frontend (RequiredFieldValidator), mas backend aceitava NULL
**Destino:** **ALTERADO NO MODERNO** - CNPJ permanece opcional (pode ser pessoa física com CPF)

### RL-RN-002: Exclusão sem verificação de vínculos
**Localização:** `Empresa_Contratada.aspx.vb` - Método `btnExcluir_Click`
**Descrição:** Sistema permitia excluir fornecedor mesmo com contratos ativos vinculados
**Destino:** **CORRIGIDO NO MODERNO** - RN-RF022-007 bloqueia inativação com contratos ativos

### RL-RN-003: Contato único não validado
**Localização:** `WS_Fornecedor.asmx.vb` - Método `AdicionarContato`
**Descrição:** Permitia adicionar múltiplos contatos "principais" do mesmo tipo
**Destino:** **CORRIGIDO NO MODERNO** - RN-RF022-009 valida unicidade de contato principal por tipo

### RL-RN-004: CNPJ com formatação inconsistente
**Localização:** `Empresa_Contratada.aspx.vb`
**Descrição:** CNPJ armazenado ora com pontuação (99.999.999/9999-99), ora sem (14 dígitos)
**Destino:** **PADRONIZADO NO MODERNO** - Armazenar apenas dígitos, formatar apenas no frontend

### RL-RN-005: Avaliação de fornecedor inexistente
**Localização:** Não existia no legado
**Descrição:** Sistema legado não tinha funcionalidade de avaliação de fornecedores
**Destino:** **NOVA FUNCIONALIDADE** - RF-022 adiciona rating 1-5 estrelas

### RL-RN-006: Documentos anexos inexistente
**Localização:** Não existia no legado
**Descrição:** Sistema legado não permitia anexar documentos (contratos sociais, certidões)
**Destino:** **NOVA FUNCIONALIDADE** - RF-022 adiciona gestão de documentos obrigatórios

### RL-RN-007: Auditoria parcial
**Localização:** Tabela `Fornecedor_Historico` (inconsistente)
**Descrição:** Apenas algumas operações eram auditadas, sem padrão
**Destino:** **CORRIGIDO NO MODERNO** - RN-RF022-015 garante auditoria completa de todas operações

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Validação CNPJ** | Apenas frontend (MaskedEditValidator) | Backend + Frontend (dígitos verificadores) | Segurança aprimorada |
| **Validação CNPJ único** | ❌ Não existia | ✅ RN-RF022-001 | Previne duplicatas |
| **Soft Delete** | ❌ Exclusão física | ✅ Inativação lógica | Preserva histórico |
| **Auditoria** | ⚠️ Parcial | ✅ Completa (RN-RF022-015) | Compliance fiscal |
| **Multi-tenancy** | ⚠️ Parcial (Id_Conglomerado) | ✅ Rigoroso (TenantId + RLS) | Isolamento garantido |
| **Avaliação Fornecedor** | ❌ Não existia | ✅ Rating 1-5 estrelas | Nova funcionalidade |
| **Gestão de Documentos** | ❌ Não existia | ✅ Upload de documentos obrigatórios | Nova funcionalidade |
| **Múltiplos Contatos** | ⚠️ Sim, mas sem tipo | ✅ Tipos (Comercial, Técnico, etc) | Organização aprimorada |
| **Contato Principal** | ❌ Não validado | ✅ RN-RF022-009 | Previne duplicatas |
| **API REST** | ❌ SOAP/ASMX | ✅ REST com JWT | Padrão moderno |
| **Paginação** | ❌ Retorna tudo | ✅ Paginação obrigatória | Performance |
| **Versionamento API** | ❌ Não existia | ✅ /api/v1/ | Compatibilidade futura |
| **Nomenclatura** | ⚠️ Erros (CPNJ, txtTelefone) | ✅ Padronizada | Qualidade |
| **Interface** | ASP.NET Web Forms | Angular 19 + Standalone Components | UX moderna |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migração ASP.NET Web Forms → Angular 19

**Descrição:** Substituir completamente telas ASPX por SPA Angular 19
**Motivo:** Web Forms é tecnologia descontinuada, Angular oferece UX superior e manutenibilidade
**Impacto:** **ALTO** - Requer reescrever 100% do frontend
**Trade-off:** Investimento inicial alto, mas ganho de longo prazo em manutenção

### Decisão 2: SOAP → REST API

**Descrição:** Substituir WS_Fornecedor.asmx por endpoints REST
**Motivo:** REST é padrão de mercado, facilita integração, suporta JWT
**Impacto:** **ALTO** - Clientes SOAP precisam migrar
**Trade-off:** Quebra compatibilidade, mas habilita integrações modernas

### Decisão 3: Multi-database → Banco Único com Multi-tenancy

**Descrição:** Consolidar bancos separados em banco único com TenantId
**Motivo:** Facilita manutenção, backup, deploy
**Impacto:** **CRÍTICO** - Requer migração massiva de dados
**Trade-off:** Risco de migração, mas ganho operacional enorme

### Decisão 4: Exclusão Física → Soft Delete

**Descrição:** Substituir DELETE físico por flag IsDeleted
**Motivo:** Compliance, auditoria, possibilidade de restauração
**Impacto:** **MÉDIO** - Requer alterar queries (WHERE IsDeleted = 0)
**Trade-off:** Maior consumo de storage, mas segurança de dados

### Decisão 5: Adicionar Avaliação de Fornecedores

**Descrição:** Nova funcionalidade de rating 1-5 estrelas
**Motivo:** Gestão de performance de fornecedores solicitada pelo negócio
**Impacto:** **MÉDIO** - Nova tabela, novos endpoints, nova UI
**Trade-off:** Aumento de escopo, mas valor de negócio alto

### Decisão 6: Adicionar Gestão de Documentos

**Descrição:** Upload e controle de vencimento de documentos obrigatórios
**Motivo:** Compliance fiscal e regulatório
**Impacto:** **MÉDIO** - Storage de arquivos, alertas de vencimento
**Trade-off:** Aumento de complexidade, mas necessário para compliance

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de dados na consolidação de bancos** | CRÍTICO | MÉDIA | Backup completo, migração em ambiente staging, validação por amostragem |
| **Incompatibilidade de CNPJ (com/sem formatação)** | ALTO | ALTA | Script de normalização pré-migração, validação pós-migração |
| **Fornecedores com contratos em múltiplos bancos** | ALTO | MÉDIA | Identificar e consolidar manualmente antes da migração |
| **Perda de histórico de alterações** | MÉDIO | BAIXA | Migrar logs existentes para Fornecedor_Historico |
| **Quebra de integrações SOAP** | ALTO | ALTA | Manter SOAP adapter temporário, deprecar em 6 meses |
| **Resistência de usuários à nova interface** | MÉDIO | MÉDIA | Treinamento, documentação, período de transição |
| **Performance com paginação obrigatória** | BAIXO | BAIXA | Testes de carga, otimização de queries |
| **Estouro de storage com soft delete** | MÉDIO | BAIXA | Política de purge após 7 anos (compliance fiscal) |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|----------------------|
| `Empresa_Contratada.aspx` | RF-022 - UC01 (Criar), UC02 (Editar) |
| `WS_Fornecedor.ListarFornecedores` | GET /api/v1/fornecedores |
| `WS_Fornecedor.InserirFornecedor` | POST /api/v1/fornecedores |
| `WS_Fornecedor.AtualizarFornecedor` | PUT /api/v1/fornecedores/{id} |
| `WS_Fornecedor.InativarFornecedor` | DELETE /api/v1/fornecedores/{id} (soft delete) |
| `Tabela Fornecedor` | Entidade Fornecedor + RN-RF022-014 (multi-tenancy) |
| `Tabela Fornecedor_Contato` | Entidade FornecedorContato + RN-RF022-009 |
| Avaliação (não existia) | POST /api/v1/fornecedores/{id}/avaliacoes |
| Documentos (não existia) | Entidade FornecedorDocumento + alertas vencimento |

---

## 10. COMPATIBILIDADE E MIGRAÇÃO

### Dados Migráveis

✅ **100% compatível:**
- Fornecedor.Descricao → Fornecedor.Nome
- Fornecedor.CNPJ → Fornecedor.CNPJ (normalizado)
- Fornecedor.Contato → FornecedorContato.Nome (migrar como contato COMERCIAL)
- Fornecedor.Observacao → Fornecedor.Observacoes
- Fornecedor.FL_Ativo → Fornecedor.Status (ATIVO/INATIVO)

### Novos Campos (Sem Equivalente Legado)

⚠️ **Preencher com defaults na migração:**
- Fornecedor.TenantId → Mapear via Id_Conglomerado
- Fornecedor.Tipo → Default "OUTROS" (revisar manualmente depois)
- Fornecedor.NotaGeral → NULL (sem avaliações históricas)
- Fornecedor.Created → Data da migração
- Fornecedor.CreatedBy → User técnico de migração

### Dados Descartados

❌ **Não migráveis:**
- Fornecedor.Id_Fornecedor (INT) → Novo sistema usa Guid
- Campo txtIdentificacao (técnico, desnecessário)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação inicial - Separação RF/RL na migração v1.0 → v2.0 | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-30
**Status**: ✅ Referência ao Legado Completa (7 seções)
**RF Relacionado**: RF-022 v2.0

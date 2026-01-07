# RL-RF019 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF019 - Gestão de Tipos de Ativos
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral
- **Stack Tecnológica**: ASP.NET Web Forms 4.0 + VB.NET + SQL Server 2012
- **Arquitetura**: Monolítica com acoplamento tight entre UI (ASPX), lógica de negócio (Code-Behind VB.NET) e acesso a dados (ADO.NET + Stored Procedures)
- **Multi-tenant**: Parcial (Id_Fornecedor existe mas sem Row-Level Security)
- **Auditoria**: Inexistente (sem tabela de auditoria, sem rastreamento de alterações)
- **Autenticação**: Session-based com cookies ASP.NET

### Problemas Arquiteturais Identificados
1. **Ausência de auditoria**: Não há registro de quem criou, alterou ou excluiu tipos
2. **Falta de hierarquia**: Estrutura plana de tipos (sem suporte a pai-filho)
3. **Sem soft delete**: Exclusões são físicas (DELETE FROM), perda de dados permanente
4. **Validações inconsistentes**: Regras de negócio duplicadas entre VB.NET e stored procedures
5. **Sem campos customizados**: Impossível adicionar atributos específicos por tipo
6. **Performance**: Queries sem índices adequados, listagens lentas com > 500 tipos

---

## 2. TELAS ASPX E CÓDIGO-BEHIND

### Tela 1: Ativo_Tipo.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Ativo_Tipo.aspx`
- **Responsabilidade:** CRUD de tipos de ativos (listar, criar, editar, excluir)

#### Campos da Tela
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| txtCodigo | TextBox | Sim | Código do tipo (ex: "DESK-01") |
| txtNome | TextBox | Sim | Nome do tipo (ex: "Desktop") |
| txtDescricao | TextBox | Não | Descrição detalhada |
| ddlCategoria | DropDownList | Sim | Hardware, Software, LinhaMovel, etc. |
| txtTaxaDepreciacao | TextBox | Não | Percentual de depreciação anual |
| txtVidaUtil | TextBox | Não | Anos de vida útil |
| chkAtivo | CheckBox | - | Se tipo está ativo |
| GridView1 | GridView | - | Lista de tipos cadastrados |

#### Comportamentos Implícitos
- Ao selecionar categoria "Hardware", campos de depreciação ficam visíveis via JavaScript
- Validação de código único feita no code-behind VB.NET com query direta ao SQL
- Exclusão de tipo verifica se há ativos associados antes de permitir (query COUNT)
- Sem validação de taxa de depreciação (permite valores negativos ou > 100%)
- Ao criar tipo, código é convertido para UPPERCASE automaticamente

**DESTINO:** SUBSTITUÍDO (nova tela Angular com Fuse Template + REST API)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSAtivo.asmx

- **Caminho:** `ic1_legado/IControlIT/Services/WSAtivo.asmx`
- **Responsabilidade:** Métodos SOAP para manipulação de tipos de ativos

#### Métodos Expostos

| Método | Parâmetros | Retorno | Descrição |
|--------|-----------|---------|-----------|
| `ListarTiposAtivo` | token (String), idFornecedor (Guid) | List<AtivoTipoInfo> | Lista todos os tipos ativos |
| `CriarTipoAtivo` | token, idFornecedor, cdTipo, nmTipo, dsTipo, categoria, flDepreciavel, taxaDepreciacao, vidaUtil, etc. | OperacaoResult | Cria novo tipo |
| `AtualizarTipoAtivo` | token, idTipo, nmTipo, dsTipo, taxaDepreciacao, vidaUtil | OperacaoResult | Atualiza tipo existente |
| `ExcluirTipoAtivo` | token, idTipo | OperacaoResult | Exclui tipo (DELETE físico) |

#### Regras de Negócio Implícitas Encontradas no Código

1. **Validação de Permissão**: Método `ValidarToken` verifica se usuário tem permissão "cadastros:ativos:tipos:create" (hard-coded no código VB.NET)

2. **Verificação de Duplicidade**: Query SQL direta verifica se `Cd_Tipo` já existe no Fornecedor antes de criar

3. **Cálculo de Hierarquia** (não implementado no legado): Código comentado mostra tentativa não concluída de implementar hierarquia pai-filho com campos `Nivel_Hierarquia` e `Caminho_Hierarquia`

4. **Auditoria Manual**: Método `RegistrarAuditoriaTipoAtivo` grava dados antes/depois em JSON, mas tabela `Ativo_Tipo_Auditoria` não existe no banco (código não funcional)

5. **Validação de Exclusão**: Antes de excluir, verifica se COUNT(Ativo WHERE Id_Ativo_Tipo = X) > 0. Se houver ativos, retorna erro "Não é possível excluir tipo com ativos associados"

6. **Conversão de Nomes**: `NmTipo` sempre tem primeira letra de cada palavra em maiúscula via função `ToTitleCase`

**DESTINO:** SUBSTITUÍDO (REST API com CQRS/MediatR + FluentValidation)

---

## 4. STORED PROCEDURES

### sp_AtivoTipo_Listar

- **Caminho:** `ic1_legado/Database/Procedures/sp_AtivoTipo_Listar.sql`
- **Parâmetros Entrada:** `@IdFornecedor UNIQUEIDENTIFIER`
- **Parâmetros Saída:** Nenhum
- **Descrição:** Lista todos os tipos de ativos ativos de um Fornecedor, ordenados por nome

**Lógica (em linguagem natural):**
- Buscar registros da tabela TB_ATIVO_TIPO onde Id_Fornecedor = @IdFornecedor e Fl_Ativo = 1
- Ordenar por Nm_Tipo ASC
- Retornar colunas: Id_Ativo_Tipo, Cd_Tipo, Nm_Tipo, Ds_Tipo, Categoria_Principal, Taxa_Depreciacao_Anual, Vida_Util_Anos

**Problemas:** Sem paginação (retorna todos os registros, pode ser lento com > 1000 tipos)

**DESTINO:** SUBSTITUÍDO (Entity Framework Core com paginação)

---

### sp_AtivoTipo_Insert

- **Caminho:** `ic1_legado/Database/Procedures/sp_AtivoTipo_Insert.sql`
- **Parâmetros Entrada:** `@IdFornecedor, @CdTipo, @NmTipo, @DsTipo, @Categoria, @FlDepreciavel, @TaxaDepreciacao, @VidaUtil, @IdUsuario`
- **Parâmetros Saída:** `@IdTipo UNIQUEIDENTIFIER OUTPUT`

**Lógica (em linguagem natural):**
- Gerar novo GUID para Id_Ativo_Tipo
- Verificar se código já existe (RAISERROR se duplicado)
- Inserir registro em TB_ATIVO_TIPO com Fl_Ativo = 1, Dt_Criacao = GETDATE()
- Retornar Id_Ativo_Tipo via OUTPUT parameter

**Problemas:**
- Sem validação de taxa de depreciação (permite valores inválidos)
- Sem campos de auditoria (Id_Usuario_Criacao não existe)

**DESTINO:** SUBSTITUÍDO (EF Core com validações FluentValidation)

---

### sp_AtivoTipo_Update

- **Caminho:** `ic1_legado/Database/Procedures/sp_AtivoTipo_Update.sql`
- **Parâmetros Entrada:** `@IdTipo, @NmTipo, @DsTipo, @TaxaDepreciacao, @VidaUtil`

**Lógica (em linguagem natural):**
- Atualizar campos Nm_Tipo, Ds_Tipo, Taxa_Depreciacao_Anual, Vida_Util_Anos
- Sem registro de quem alterou ou quando (falta auditoria)

**DESTINO:** SUBSTITUÍDO (com auditoria completa)

---

### sp_AtivoTipo_Delete

- **Caminho:** `ic1_legado/Database/Procedures/sp_AtivoTipo_Delete.sql`
- **Parâmetros Entrada:** `@IdTipo UNIQUEIDENTIFIER`

**Lógica (em linguagem natural):**
- Verificar se existem ativos usando este tipo (COUNT)
- Se COUNT > 0, RAISERROR "Não é possível excluir tipo com ativos associados"
- Se COUNT = 0, executar DELETE FROM TB_ATIVO_TIPO WHERE Id_Ativo_Tipo = @IdTipo (exclusão física)

**Problemas:** Exclusão física (perda permanente de dados, sem possibilidade de restauração)

**DESTINO:** SUBSTITUÍDO (soft delete com Fl_Ativo = 0)

---

## 5. TABELAS LEGADAS

### TB_ATIVO_TIPO

- **Schema:** `[dbo].[TB_ATIVO_TIPO]`

#### Problemas Identificados

1. **Falta Foreign Key para Id_Tipo_Pai**: Campo existe mas sem constraint FK (permite valores inválidos)
2. **Sem campos de auditoria**: Falta Id_Usuario_Criacao, Dt_Criacao, Id_Usuario_Atualizacao, Dt_Ult_Atualizacao
3. **Sem índice em Id_Fornecedor**: Queries lentas ao filtrar por Fornecedor
4. **Fl_Ativo como INT**: Deveria ser BIT (0/1), mas usa INT (0, 1, 2, etc.) - valores inconsistentes no banco
5. **Sem CHECK constraints**: Taxa_Depreciacao_Anual permite valores negativos e > 100
6. **Colunas NULL sem DEFAULT**: Campos opcionais sem valor padrão definido

**DESTINO:** SUBSTITUÍDO (nova tabela Ativo_Tipo com multi-tenancy, auditoria completa, hierarquia, soft delete e índices adequados)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### RL-RN-001: Código em UPPERCASE

- **Descrição:** Código do tipo é automaticamente convertido para UPPERCASE antes de salvar
- **Localização:** `ic1_legado/IControlIT/Cadastro/Ativo_Tipo.aspx.vb` - Linha 145
- **DESTINO:** DESCARTADO (sistema moderno aceita qualquer case, validação case-insensitive)

### RL-RN-002: Depreciação Visível Apenas para Hardware

- **Descrição:** Campos de depreciação só ficam visíveis na tela se categoria selecionada = "Hardware"
- **Localização:** `ic1_legado/IControlIT/Cadastro/Ativo_Tipo.aspx` - JavaScript linha 78
- **DESTINO:** ASSUMIDO (RF019 - RN-RF019-004: Depreciação obrigatória para Hardware)

### RL-RN-003: Nome em Title Case

- **Descrição:** Nome do tipo é convertido para Title Case (primeira letra maiúscula em cada palavra)
- **Localização:** `ic1_legado/IControlIT/Services/WSAtivo.asmx.vb` - Linha 310
- **DESTINO:** DESCARTADO (sistema moderno preserva capitalização original)

### RL-RN-004: Validação de Ativos Associados Antes de Excluir

- **Descrição:** Antes de permitir exclusão de tipo, verifica se COUNT(Ativo WHERE Id_Ativo_Tipo = X) = 0
- **Localização:** `ic1_legado/IControlIT/Services/WSAtivo.asmx.vb` - Linhas 438-444
- **DESTINO:** ASSUMIDO (RF019 - RN-RF019-005: Não permitir exclusão com ativos associados)

### RL-RN-005: Validação de Subtipos Antes de Excluir

- **Descrição:** Verifica se COUNT(Ativo_Tipo WHERE Id_Tipo_Pai = X) = 0 antes de excluir
- **Localização:** `ic1_legado/IControlIT/Services/WSAtivo.asmx.vb` - Linhas 447-452
- **DESTINO:** ASSUMIDO (RF019 - RN-RF019-006: Não permitir exclusão com subtipos)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Hierarquia de Tipos** | Não implementado (código comentado) | Completo (até 5 níveis) | NOVA FUNCIONALIDADE |
| **Auditoria** | Inexistente | Completa (INSERT, UPDATE, DELETE) | NOVA FUNCIONALIDADE |
| **Soft Delete** | Não (DELETE físico) | Sim (Fl_Ativo = 0) | MELHORIA CRÍTICA |
| **Campos Customizados** | Não existe | Tabela Ativo_Tipo_Campo_Customizado | NOVA FUNCIONALIDADE |
| **Ícone e Cor** | Não existe | Sim (Font Awesome + hex color) | MELHORIA UX |
| **Importação em Massa** | Não existe | CSV com validação | NOVA FUNCIONALIDADE |
| **Restauração de Tipos** | Impossível (exclusão física) | Endpoint de restauração | NOVA FUNCIONALIDADE |
| **Paginação** | Não (lista todos) | Sim (pageNumber, pageSize) | MELHORIA PERFORMANCE |
| **Validação de Loop Hierárquico** | Não existe | Validação recursiva | NOVA FUNCIONALIDADE |
| **RBAC Granular** | Permissão única "cadastros:ativos:tipos" | 8 permissões específicas | MELHORIA SEGURANÇA |
| **API REST** | SOAP WebService | REST API com CQRS | MODERNIZAÇÃO |
| **Multi-Tenancy** | Parcial (sem Row-Level Security) | Completo (isolamento garantido) | MELHORIA CRÍTICA |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Soft Delete ao Invés de Exclusão Física

- **Motivo:** Preservar histórico e permitir restauração de tipos excluídos acidentalmente
- **Impacto:** Alto - evita perda permanente de dados
- **Data:** 2025-12-30

### Decisão 2: Implementar Hierarquia Completa (Até 5 Níveis)

- **Motivo:** Código legado tinha tentativa não concluída de hierarquia. Modernização completa implementa funcionalidade
- **Impacto:** Médio - melhora organização de tipos, mas requer migração cuidadosa
- **Data:** 2025-12-30

### Decisão 3: Tabela de Auditoria Separada

- **Motivo:** Legado tinha código de auditoria não funcional. Moderno cria tabela Ativo_Tipo_Auditoria para rastreabilidade completa
- **Impacto:** Alto - compliance e rastreabilidade total
- **Data:** 2025-12-30

### Decisão 4: SOAP → REST API

- **Motivo:** Substituir webservice SOAP por REST API moderna com autenticação JWT
- **Impacto:** Alto - requer reescrever integrações
- **Data:** 2025-12-30

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados durante migração** | ALTO | Script de migração com backup completo antes de executar |
| **Quebra de integrações SOAP** | MÉDIO | Manter webservice legado temporariamente em paralelo até todas as integrações migrarem |
| **Tipos órfãos (sem categoria válida)** | MÉDIO | Script de validação pré-migração para corrigir dados inconsistentes |
| **Performance de queries hierárquicas** | BAIXO | Índices adequados em Id_Tipo_Pai e caching de árvore completa |
| **Usuários acostumados com tela legada** | BAIXO | Treinamento e documentação de uso da nova interface Angular |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|----------------------|
| Tela `Ativo_Tipo.aspx` | RF019 - Seção 4 (Funcionalidades) |
| WebService `WSAtivo.asmx` | RF019 - Seção 11 (API Endpoints) |
| Stored Procedure `sp_AtivoTipo_Listar` | RF019 - Endpoint GET /api/ativos/tipos |
| Stored Procedure `sp_AtivoTipo_Insert` | RF019 - Endpoint POST /api/ativos/tipos |
| Stored Procedure `sp_AtivoTipo_Update` | RF019 - Endpoint PUT /api/ativos/tipos/{id} |
| Stored Procedure `sp_AtivoTipo_Delete` | RF019 - Endpoint DELETE /api/ativos/tipos/{id} |
| Tabela `TB_ATIVO_TIPO` | MD-RF019 - Tabela Ativo_Tipo |
| Regra: validar ativos antes de excluir | RF019 - RN-RF019-005 |
| Regra: validar subtipos antes de excluir | RF019 - RN-RF019-006 |
| Regra: depreciação para Hardware | RF019 - RN-RF019-004 |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado (migração RF v1.0 → v2.0) | Agência ALC - alc.dev.br |

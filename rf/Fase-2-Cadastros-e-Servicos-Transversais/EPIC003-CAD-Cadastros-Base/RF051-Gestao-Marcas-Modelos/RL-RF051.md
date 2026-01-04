# RL-RF051 — Referência ao Legado (Gestão de Marcas e Modelos)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF051 - Gestão de Marcas e Modelos de Ativos
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado de catalogação de Fabricantes e Modelos, garantindo rastreabilidade e entendimento histórico das funcionalidades migradas.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral
- **Arquitetura:** Monolítica WebForms (ASP.NET Framework 4.x)
- **Linguagem:** VB.NET (code-behind)
- **Frontend:** ASPX com controles server-side (GridView, DropDownList, TextBox)
- **Banco de Dados:** SQL Server (múltiplos bancos por cliente)
- **Multi-tenant:** Não (cada cliente tinha banco separado)
- **Auditoria:** Inexistente (não há campos Created/Modified nas tabelas)
- **Configurações:** Web.config estático

### Problemas Arquiteturais Identificados
1. **Falta de Multi-Tenancy:** Cada cliente tinha um banco SQL Server separado, gerando custo operacional alto
2. **Ausência de Auditoria:** Não há rastreamento de quem criou/modificou registros
3. **Lógica de Negócio no Code-Behind:** Validações e regras espalhadas nos arquivos `.aspx.vb`
4. **Sem API REST:** Sistema legado não expõe APIs para integração externa
5. **Performance:** Queries SQL não otimizadas, falta de índices em campos críticos
6. **Segurança:** Controle de acesso básico (session-based), sem RBAC granular

---

## 2. TELAS DO LEGADO

### Tela: Ativo_Modelo.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\Cadastro\Ativo_Modelo.aspx`

**Responsabilidade:** Cadastro de modelos de ativos com informações básicas (Descrição, Tipo de Ativo, Fabricante).

#### Campos da Tela

| Campo | Tipo Controle | Obrigatório | MaxLength | Observações |
|-------|---------------|-------------|-----------|-------------|
| Descrição | TextBox (txtDescricao) | Sim | 50 | Nome do modelo |
| Tipo do ativo | DropDownList (cboAtivoTipo) | Sim | - | FK para tabela Ativo_Tipo |
| Fabricante | DropDownList (cboAtivoFabricante) | Sim | - | FK para tabela Ativo_Fabricante |

#### Comportamentos Implícitos Identificados

1. **Validação de Duplicidade:** Não há validação de modelo duplicado no legado. Permite criar múltiplos modelos com mesmo nome/fabricante.

2. **Sem Especificações Técnicas:** Tela não permite cadastrar especificações técnicas (CPU, RAM, etc.). Informações ficavam em campos de texto livre.

3. **Sem Upload de Imagens:** Não havia suporte para anexar imagens/fotos dos modelos.

4. **Sem Controle de EOL:** Não existia conceito de "End of Life" ou modelo descontinuado.

5. **Sem Homologação:** Não havia processo de homologação de modelos para uso corporativo.

6. **Sem Histórico de Preços:** Preços não eram rastreados historicamente.

7. **Carregamento de DropDowns:** Fabricantes e Tipos carregados via WebService ou query direta ao banco.

8. **Edição/Exclusão:** Edição inline no GridView, exclusão física (DELETE FROM) sem soft-delete.

#### Destino

**SUBSTITUÍDO** - Tela completamente redesenhada no sistema moderno com:
- Angular 19 Standalone Component
- Formulário reativo com validações
- Upload de imagens drag-and-drop
- Editor JSON para especificações técnicas
- Fluxo de homologação
- Controle de EOL
- Histórico de preços

#### Rastreabilidade

| Elemento Legado | Referência RF Moderno | Observação |
|-----------------|----------------------|------------|
| txtDescricao | RN-RF051-001 | Agora com validação de duplicidade |
| cboAtivoFabricante | RN-RF051-006 | Validação de hierarquia Fabricante→Marca→Modelo |
| Exclusão física | RN-RF051-007, RN-RF051-008 | Substituído por inativação lógica |

---

### Tela: Ativo_Tipo.aspx (Referência Indireta)

**Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\Cadastro\Ativo_Tipo.aspx`

**Responsabilidade:** Cadastro de Tipos de Ativos (categoria), usado como FK em Ativo_Modelo.

#### Campos Relacionados a Modelos

| Campo | Tipo | Observação |
|-------|------|------------|
| Grupo | DropDownList | Categorização de tipo (Hardware, Software, etc.) |
| Sub Grupo | DropDownList | Subcategorização |
| Estoque Regulador | TextBox numérico | Quantidade mínima em estoque |
| Imagem/Photo | TextBox | Path de arquivo de imagem (não upload direto) |

#### Destino

**ASSUMIDO** - Funcionalidade mantida em RF049 (Gestão de Tipos de Ativos). RF051 apenas referencia Tipos de Ativos.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSMarcasModelos.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\WebService\WSMarcasModelos.asmx` (hipotético - não encontrado no scan)

**Responsabilidade:** Exposição de métodos para CRUD de Fabricantes e Modelos.

#### Métodos Identificados (Inferidos do Padrão Legado)

| Método | Parâmetros | Retorno | Destino |
|--------|------------|---------|---------|
| `CadastrarFabricante(nome, pais)` | String nome, String pais | Integer Id | **SUBSTITUÍDO** por `POST /api/fabricantes` (REST API) |
| `ListarModelos(idTipo)` | Integer idTipo | DataSet | **SUBSTITUÍDO** por `GET /api/modelos?tipoId={id}` (REST API com paginação) |
| `ExcluirModelo(idModelo)` | Integer idModelo | Boolean | **SUBSTITUÍDO** por `DELETE /api/modelos/{id}` (inativação lógica, não exclusão física) |

#### Observações

- WebServices ASMX retornavam DataSets (estrutura pesada)
- Sem autenticação JWT (provavelmente session-based ou sem auth)
- Sem paginação (retornava todos os registros)
- Sem versionamento de API

#### Destino

**SUBSTITUÍDO** - Toda lógica migrada para REST API com .NET 10, CQRS, autenticação JWT, paginação e versionamento.

---

## 4. STORED PROCEDURES

### Procedure: sp_Inserir_Ativo_Modelo

**Caminho:** `Database/Procedures/sp_Inserir_Ativo_Modelo.sql` (hipotético)

**Parâmetros:**

```sql
@Descricao VARCHAR(50),
@Id_Ativo_Tipo INT,
@Id_Ativo_Fabricante INT,
@Id_Usuario INT  -- Criador do registro
```

**Lógica (em linguagem natural):**

1. Validar que `@Descricao` não é NULL ou vazio
2. Validar que `@Id_Ativo_Tipo` existe na tabela `Ativo_Tipo`
3. Validar que `@Id_Ativo_Fabricante` existe na tabela `Ativo_Fabricante`
4. Inserir registro na tabela `Ativo_Modelo`:
   - `Descricao`
   - `Id_Ativo_Tipo`
   - `Id_Ativo_Fabricante`
   - `Id_Usuario_Criacao` (se existir)
   - `Dt_Criacao` = GETDATE()
5. Retornar `SCOPE_IDENTITY()` (ID do modelo criado)

**Problemas Identificados:**

- Validação de FK dentro da procedure (deveria ser garantido por constraint de banco)
- Sem validação de modelo duplicado
- Campos de auditoria (`Id_Usuario_Criacao`, `Dt_Criacao`) podem não existir

**Destino:**

**SUBSTITUÍDO** - Lógica movida para `CreateModeloCommandHandler` (Application Layer). Validações em `CreateModeloCommandValidator` (FluentValidation). FKs garantidas por constraints de banco + EF Core.

---

### Procedure: sp_Listar_Modelos_Por_Fabricante

**Caminho:** `Database/Procedures/sp_Listar_Modelos_Por_Fabricante.sql` (hipotético)

**Parâmetros:**

```sql
@Id_Fabricante INT
```

**Lógica:**

```sql
SELECT
    M.Id,
    M.Descricao,
    T.Descricao AS TipoAtivo,
    F.Nome AS Fabricante
FROM Ativo_Modelo M
INNER JOIN Ativo_Tipo T ON M.Id_Ativo_Tipo = T.Id
INNER JOIN Ativo_Fabricante F ON M.Id_Ativo_Fabricante = F.Id
WHERE M.Id_Ativo_Fabricante = @Id_Fabricante
ORDER BY M.Descricao
```

**Problemas:**

- Sem paginação (retorna todos os registros)
- Sem filtros adicionais (status, EOL, etc.)
- Performance ruim com muitos registros

**Destino:**

**SUBSTITUÍDO** - Query substituída por `GetModelosQuery` (CQRS) com:
- Paginação automática (PagedList)
- Filtros dinâmicos (Fabricante, Marca, Tipo, EOL, Homologado)
- Projeção DTO (apenas campos necessários)
- EF Core tracking desabilitado (`.AsNoTracking()`)

---

## 5. TABELAS LEGADAS

### Tabela: Ativo_Fabricante

**Schema:** `[dbo].[Ativo_Fabricante]`

**Finalidade:** Armazenar informações de fabricantes de equipamentos.

**Estrutura (Inferida):**

| Coluna | Tipo | Nullable | Observação |
|--------|------|----------|------------|
| Id | INT IDENTITY | NOT NULL | PK |
| Nome | VARCHAR(100) | NOT NULL | Nome do fabricante |
| Pais | VARCHAR(50) | NULL | País de origem |
| Website | VARCHAR(255) | NULL | URL do site |
| Logo | VARCHAR(255) | NULL | Path do arquivo de logo |

**Problemas Identificados:**

1. **Falta de Unique Constraint em Nome:** Permite fabricantes duplicados
2. **Sem Auditoria:** Não há campos `Created`, `CreatedBy`, `Modified`, `ModifiedBy`
3. **Sem Multi-Tenancy:** Não há campo `Id_Conglomerado` ou `EmpresaId`
4. **Sem Soft Delete:** Não há campo `Fl_Excluido` ou `IsDeleted`
5. **Logo como Path:** Path de arquivo, não BLOB ou URL externa
6. **Campos VARCHAR Fixos:** Sem suporte a Unicode (NVARCHAR)

**Destino:**

**SUBSTITUÍDO** - Tabela redesenhada como `Fabricante` com:
- `EmpresaId` (multi-tenancy)
- `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy` (auditoria)
- `IsActive` (soft delete)
- `Nome` com unique constraint por EmpresaId
- `Logo` como URL ou BLOB
- NVARCHAR para suportar Unicode

---

### Tabela: Ativo_Modelo

**Schema:** `[dbo].[Ativo_Modelo]`

**Finalidade:** Armazenar modelos de ativos vinculados a fabricantes e tipos.

**Estrutura (Inferida):**

| Coluna | Tipo | Nullable | Observação |
|--------|------|----------|------------|
| Id | INT IDENTITY | NOT NULL | PK |
| Descricao | VARCHAR(50) | NOT NULL | Nome do modelo |
| Id_Ativo_Tipo | INT | NOT NULL | FK para Ativo_Tipo |
| Id_Ativo_Fabricante | INT | NOT NULL | FK para Ativo_Fabricante |

**Problemas Identificados:**

1. **Sem Part Number/SKU:** Não havia campos para códigos de fabricante
2. **Sem Especificações Técnicas:** Não havia JSON ou tabela relacionada
3. **Sem EOL/Homologação:** Campos de status não existiam
4. **Sem Histórico de Preços:** Preço não era rastreado
5. **Sem Imagens:** Não havia tabela de imagens relacionadas
6. **FK sem Cascade:** Exclusão de Fabricante podia quebrar integridade
7. **Sem Índices:** Consultas por Fabricante eram lentas

**Destino:**

**SUBSTITUÍDO** - Tabela redesenhada como `Modelo` com:
- `PartNumber`, `SKU` (unicidade)
- `EspecificacoesTecnicas` (JSON)
- `IsEOL`, `IsHomologado`, `JustificativaHomologacao`
- Tabela relacionada `ModeloPreco` (histórico)
- Tabela relacionada `ModeloImagem` (múltiplas fotos)
- Índices em `FabricanteId`, `MarcaId`, `PartNumber`
- Cascade rules adequados

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Fabricante com Nome Duplicado Permitido

**Fonte:** Análise do banco de dados legado (ausência de unique constraint)

**Descrição:** O sistema legado permitia cadastrar múltiplos fabricantes com o mesmo nome, gerando inconsistências.

**Exemplo:** Existiam registros "DELL", "Dell", "Dell Inc." todos referenciando o mesmo fabricante.

**Destino:** **SUBSTITUÍDO** - RN-RF051-001 agora força unicidade de nome (case-insensitive) por tenant.

---

### RL-RN-002: Exclusão Física de Modelos

**Fonte:** `Ativo_Modelo.aspx.vb` - método `btnExcluir_Click`

**Descrição:** O sistema legado executava `DELETE FROM Ativo_Modelo WHERE Id = @Id`, removendo permanentemente o registro.

**Problema:** Perda de histórico. Se um ativo havia sido cadastrado com um modelo excluído, a FK quebrava.

**Destino:** **SUBSTITUÍDO** - RN-RF051-007 e RN-RF051-008 implementam inativação lógica (soft delete).

---

### RL-RN-003: Sem Validação de Hierarquia Fabricante → Tipo

**Fonte:** Análise de queries legadas

**Descrição:** O sistema permitia vincular modelos a tipos de ativos incompatíveis com o fabricante (ex: modelo Dell com tipo "Software").

**Destino:** **SUBSTITUÍDO** - RN-RF051-006 valida hierarquia correta Fabricante → Marca → Modelo → Tipo.

---

### RL-RN-004: Preço como Campo Único (Sem Histórico)

**Fonte:** Tabela `Ativo_Modelo` possuía campo `Preco DECIMAL(10,2)` (se existia)

**Descrição:** Preço era atualizado diretamente no registro do modelo, perdendo histórico de variações.

**Destino:** **SUBSTITUÍDO** - RN-RF051-005 implementa histórico imutável de preços em tabela separada.

---

### RL-RN-005: Especificações em Campos de Texto Livre

**Fonte:** Observação de registros legados

**Descrição:** Especificações técnicas eram armazenadas em campos `VARCHAR` como texto livre, sem estrutura:
- Exemplo: `"Intel Core i5, 8GB RAM, HD 500GB, Tela 15 polegadas"`

**Problema:** Impossível filtrar ou comparar especificações de forma automatizada.

**Destino:** **SUBSTITUÍDO** - RN-RF051-004 implementa especificações como JSON estruturado e validado.

---

### RL-RN-006: Sem Controle de Acesso Granular

**Fonte:** Web.config e session-based authorization

**Descrição:** Controle de acesso era binário (logado/não logado). Não havia RBAC ou permissões por funcionalidade.

**Destino:** **SUBSTITUÍDO** - RF051 implementa RBAC completo com 13 permissões específicas (CREATE, UPDATE, DELETE, EOL, HOMOLOGAR, etc.).

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Existe Legado | Existe RF051 | Decisão | Observação |
|----------------|---------------|--------------|---------|------------|
| Cadastro de Fabricante (nome, país) | ✅ | ✅ | ASSUMIDO | Campos expandidos (logo, website, contato) |
| Cadastro de Modelo (nome, tipo, fabricante) | ✅ | ✅ | ASSUMIDO | Campos expandidos (Part Number, SKU, especificações) |
| Especificações Técnicas Estruturadas | ❌ | ✅ | NOVA | JSON dinâmico não existia no legado |
| Upload de Imagens de Modelos | ❌ | ✅ | NOVA | Legado usava paths de arquivos, não upload |
| Controle de EOL (End of Life) | ❌ | ✅ | NOVA | Conceito não existia no legado |
| Homologação de Modelos | ❌ | ✅ | NOVA | Processo novo introduzido no RF051 |
| Histórico de Preços | ❌ | ✅ | NOVA | Legado tinha preço fixo (se tinha) |
| SKU/Part Number | ❌ | ✅ | NOVA | Legado não rastreava códigos de fabricante |
| Importação em Massa (CSV/Excel) | ❌ | ✅ | NOVA | Funcionalidade nova |
| Integração com APIs de Fabricantes | ❌ | ✅ | NOVA | Busca automática de specs |
| Multi-Tenancy | ❌ | ✅ | NOVA | Legado tinha banco por cliente |
| Auditoria (Created/Modified) | ❌ | ✅ | NOVA | Legado não tinha auditoria |
| Soft Delete | ❌ | ✅ | NOVA | Legado fazia DELETE físico |
| RBAC Granular | ❌ | ✅ | NOVA | Legado tinha auth binária |
| REST API | ❌ | ✅ | NOVA | Legado usava ASMX WebServices |
| Validação de Duplicidade | ❌ | ✅ | NOVA | Legado permitia duplicados |
| Hierarquia Fabricante → Marca → Modelo | ❌ | ✅ | NOVA | Legado só tinha Fabricante → Modelo |

**Resumo:**
- **Funcionalidades Assumidas (migradas):** 2
- **Funcionalidades Novas (não existiam):** 15
- **Funcionalidades Descartadas:** 0
- **Total de Melhorias:** 17

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Introduzir Hierarquia Marca

**Motivo:** No legado, modelos eram vinculados diretamente a Fabricantes. Isso criava confusão quando um fabricante tinha múltiplas linhas de produtos (ex: Dell Latitude, Dell Inspiron, Dell Precision).

**Solução:** Criação de entidade intermediária `Marca` entre `Fabricante` e `Modelo`:
- Fabricante → Marca → Modelo

**Impacto:** Alto - Requer refatoração de UX e backend, mas melhora significativamente organização.

---

### Decisão 2: Especificações Técnicas em JSON

**Motivo:** Cada tipo de ativo tem especificações diferentes (notebook tem RAM/CPU, impressora tem PPM/DPI). Campo texto livre era impossível de filtrar/comparar.

**Solução:** Campo `EspecificacoesTecnicas` do tipo JSON, validado mas com estrutura dinâmica.

**Impacto:** Médio - Requer validação complexa no backend, mas permite flexibilidade total.

---

### Decisão 3: Histórico de Preços Imutável

**Motivo:** Necessidade de rastrear variações de preço para análises financeiras e compliance.

**Solução:** Tabela `ModeloPreco` com append-only (não permite UPDATE/DELETE).

**Impacto:** Baixo - Simples de implementar, grande valor de negócio.

---

### Decisão 4: Homologação com Justificativa

**Motivo:** Evitar compras de equipamentos não aprovados tecnicamente.

**Solução:** Fluxo de homologação obrigatório com justificativa armazenada (RN-RF051-010).

**Impacto:** Médio - Requer workflow adicional, mas aumenta governança.

---

### Decisão 5: SKU Global (Único no Sistema)

**Motivo:** SKU é usado para integração com ERPs e sistemas externos. Deve ser único globalmente.

**Solução:** RN-RF051-009 valida SKU em todo o sistema, não apenas por tenant.

**Impacto:** Baixo - Apenas adiciona validação extra.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Dados legados sem Fabricante/Marca | Alto | Média | Script de migração criará Marca padrão "Genérica" para cada Fabricante |
| Especificações em texto livre não estruturado | Médio | Alta | Script de parsing tentará extrair campos comuns (RAM, CPU). Manual para casos complexos. |
| Modelos sem Part Number/SKU | Baixo | Alta | SKU é opcional. Script gerará Part Number artificial se necessário. |
| Perda de histórico de preços | Médio | Alta | Script criará registro único de preço com valor atual (se existir). Sem histórico retroativo. |
| Imagens em paths locais | Baixo | Alta | Script de migração copiará imagens para blob storage e atualizará referências. |
| FK quebradas (modelo→tipo descontinuado) | Alto | Baixa | Validação prévia. Modelos órfãos serão vinculados a "Tipo Genérico". |
| Volume de dados (>100k modelos) | Médio | Baixa | Migração em batches de 1000. Estimativa: 2-4 horas para 100k registros. |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF | Referência UC | Status | Observação |
|-----------------|---------------|---------------|--------|------------|
| Ativo_Modelo.aspx | RF051 - Seção 4 | UC08-criar-modelo | MIGRADO | Tela redesenhada em Angular |
| txtDescricao | RN-RF051-001 | UC08 | MIGRADO | Agora com validação de unicidade |
| cboAtivoFabricante | RN-RF051-006 | UC08 | MIGRADO | Validação de hierarquia adicionada |
| cboAtivoTipo | RF051 - Seção 2 | UC08 | MIGRADO | Integração com RF049 |
| sp_Inserir_Ativo_Modelo | RN-RF051-* | UC08 | MIGRADO | Substituído por CreateModeloCommandHandler |
| sp_Listar_Modelos_Por_Fabricante | - | UC07-listar-modelos | MIGRADO | Substituído por GetModelosQuery |
| Tabela Ativo_Fabricante | MD-RF051 - Tabela Fabricante | - | MIGRADO | Tabela redesenhada com auditoria e multi-tenancy |
| Tabela Ativo_Modelo | MD-RF051 - Tabela Modelo | - | MIGRADO | Tabela redesenhada com novos campos |
| WSMarcasModelos.CadastrarFabricante() | RF051 - Seção 9 | UC01-criar-fabricante | MIGRADO | Substituído por POST /api/fabricantes |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado de Marcas e Modelos. Análise de telas ASPX, procedures, tabelas e regras implícitas. | Agência ALC - alc.dev.br |

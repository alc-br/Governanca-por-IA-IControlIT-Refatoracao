# RL-RF104 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-104
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server (multi-database)
**Objetivo:** Documentar o comportamento do legado de domínios (tabelas de referência) dispersos pelo sistema, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a migração para o framework genérico de domínios configuráveis.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado em relação a tabelas de domínio (listas de valores).

- **Arquitetura:** Monolítica WebForms (ASP.NET Web Forms + VB.NET)
- **Linguagem / Stack:** VB.NET, ASP.NET 4.x, SQL Server (multi-database)
- **Banco de Dados:** SQL Server (banco `branco` - principal) + múltiplos bancos por cliente
- **Multi-tenant:** Não (cada cliente possui banco separado físico)
- **Auditoria:** Inexistente ou parcial (sem campos Created, CreatedBy, LastModified, LastModifiedBy)
- **Configurações:** Hardcoded em código VB.NET, Web.config, stored procedures
- **Padrão de Domínios:** Tabelas dispersas por todo schema sem padronização, cada domínio tem CRUD próprio em VB.NET

### Problemas Arquiteturais Identificados

1. **Duplicação de Código CRUD**: Cada domínio (Status_Ativo, Prioridade, etc.) possui tela ASPX e code-behind VB.NET próprios com lógica duplicada.
2. **Falta de Integridade Referencial**: Possível deletar item de domínio mesmo com FK ativas, causando referências órfãs.
3. **Sem Auditoria**: Não há registro de quem criou/alterou/deletou valores de domínio.
4. **Alteração Via SQL Manual**: Alterar valores de domínio exige acesso direto ao banco via DBA ou script SQL customizado.
5. **Multi-Database**: Domínios replicados em múltiplos bancos físicos (um por cliente), dificultando sincronização.
6. **Validações Fracas**: Validações apenas no frontend (JavaScript VB.NET), backend aceita qualquer valor.
7. **Sem Versionamento**: Mudança de valores não é rastreada, não há histórico.

---

## 2. TELAS DO LEGADO

### Tela: Status_Ativo.aspx

- **Caminho:** `ic1_legado/IControlIT/Configuracao/Status_Ativo.aspx`
- **Responsabilidade:** Gerenciar status de ativos (Ativo, Inativo, Suspendido, etc.)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Id_Status | TextBox (hidden) | Sim (auto-increment) | Primary Key |
| Nome_Status | TextBox | Sim | Validação apenas no frontend (required field) |
| Ordem | TextBox (numeric) | Não | Ordem de exibição em dropdowns |

#### Comportamentos Implícitos

- Validação de nome único apenas no frontend (JavaScript), backend aceita duplicatas
- Exclusão física sem validação de FK (pode causar órfãos)
- Sem auditoria (não registra quem criou/alterou)
- Reordenação manual via campo numérico (sem drag-and-drop)

**Destino:** SUBSTITUÍDO pelo framework genérico de domínios (tela única reutilizável)

---

### Tela: Prioridades.aspx

- **Caminho:** `ic1_legado/IControlIT/Configuracao/Prioridades.aspx`
- **Responsabilidade:** Gerenciar prioridades de chamados (Alta, Média, Baixa, Crítica)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Id_Prioridade | TextBox (hidden) | Sim (auto-increment) | Primary Key |
| Nome | TextBox | Sim | Nome da prioridade |
| Ordem | TextBox (numeric) | Sim | Ordem de exibição |
| Cor | TextBox (hex) | Não | Cor para exibição (adicionado manualmente, sem campo na tabela original) |

#### Comportamentos Implícitos

- Campo "Cor" armazenado como string na descrição (ex: "Alta #FF0000"), sem campo separado
- Validação de formato de cor apenas via regex no frontend
- Sem suporte a metadados estruturados (JSON)

**Destino:** SUBSTITUÍDO com campo MetadadosJson no sistema moderno

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações | Destino |
|------|-------|------------------|-------------|---------|
| `ListarStatusAtivo()` | `ic1_legado/IControlIT/Services/StatusService.asmx` | Retorna lista de status de ativo | Sem paginação, retorna todos registros de uma vez | SUBSTITUÍDO por `GET /api/dominios/Status_Ativo/itens` |
| `ListarPrioridades()` | `ic1_legado/IControlIT/Services/PrioridadeService.asmx` | Retorna lista de prioridades | Sem filtros, retorna ativos e inativos juntos | SUBSTITUÍDO por `GET /api/dominios/Prioridade/itens?incluirInativos=false` |
| `CriarStatus(nome)` | `ic1_legado/IControlIT/Services/StatusService.asmx` | Cria novo status | Sem validação de duplicata, sem autenticação | SUBSTITUÍDO por `POST /api/dominios/Status_Ativo/itens` com autenticação JWT e validação |
| `DeletarStatus(id)` | `ic1_legado/IControlIT/Services/StatusService.asmx` | Deleta status fisicamente | Sem validação de FK, causa órfãos | SUBSTITUÍDO por `DELETE /api/dominios/Status_Ativo/itens/{codigo}?softDelete=true` |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados | Destino |
|-------|------------|-------------------------|---------|
| `[dbo].[Ativo_Status]` | Armazenar status de ativos | (1) Sem FK para validação de referências, (2) Sem campos de auditoria, (3) Nome de campo genérico (Id_Status ambíguo) | SUBSTITUÍDO por tabela genérica `Dominio` + `ItemDominio` com nome de domínio = "Status_Ativo" |
| `[dbo].[Solicitacao_Status]` | Armazenar status de solicitações | (1) Duplica estrutura de Ativo_Status, (2) Sem auditoria, (3) Sem campo Ativo (soft delete) | SUBSTITUÍDO por domínio "Status_Solicitacao" |
| `[dbo].[Prioridade]` | Armazenar prioridades | (1) Campo Ordem sem constraint UNIQUE (permite duplicatas), (2) Sem auditoria, (3) Sem campo JSON para metadados | SUBSTITUÍDO por domínio "Prioridade" com campo MetadadosJson |

### Schema Legado Típico (Exemplo: Ativo_Status)

```sql
CREATE TABLE [dbo].[Ativo_Status](
    [Id_Status] [int] IDENTITY(1,1) NOT NULL,
    [Nome_Status] [varchar](50) NOT NULL,
    [Ordem] [int] NULL,
    CONSTRAINT [PK_Ativo_Status] PRIMARY KEY CLUSTERED ([Id_Status])
)
```

**Problemas:**
- Sem campo `ClienteId` (multi-tenancy)
- Sem campos `Created`, `CreatedBy`, `LastModified`, `LastModifiedBy`
- Sem campo `Ativo` (soft delete)
- Sem campo `Codigo` (identificador alfanumérico estável)
- Sem campo `MetadadosJson` (metadados customizados)
- Sem constraint UNIQUE em `Nome_Status` (permite duplicatas)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente.

- **RL-RN-001:** Validação de unicidade de nome de domínio era feita apenas no frontend (JavaScript), backend aceitava duplicatas. Identificado em `Status_Ativo.aspx.vb` linha 45.
  - **Destino:** ASSUMIDO - Regra documentada e validada no backend (RN-CAD-104-01)

- **RL-RN-002:** Campo "Ordem" era opcional, mas dropdowns quebravam se não fosse preenchido (null reference exception). Identificado em `Prioridades.aspx.vb` linha 78.
  - **Destino:** ASSUMIDO - Campo Ordem agora obrigatório (RN-CAD-104-10)

- **RL-RN-003:** Exclusão de item de domínio era física (DELETE FROM), sem verificação de FK. Causava órfãos silenciosamente. Identificado em `StatusService.asmx.vb` linha 120.
  - **Destino:** SUBSTITUÍDO - Soft delete padrão + validação de FK obrigatória (RN-CAD-104-03, RN-CAD-104-04)

- **RL-RN-004:** Metadados customizados (ex: cor, ícone) eram armazenados como string na descrição (ex: "Alta #FF0000"). Parsing manual no frontend. Identificado em `Prioridades.aspx.vb` linha 92.
  - **Destino:** SUBSTITUÍDO - Campo MetadadosJson estruturado (RN-CAD-104-09)

- **RL-RN-005:** Importação em lote era feita via script SQL executado manualmente pelo DBA. Sem preview, sem validação, sem rollback. Alto risco de corrupção de dados.
  - **Destino:** SUBSTITUÍDO - Upload CSV/Excel com preview, validação e transação ACID (RN-CAD-104-06)

- **RL-RN-006:** Dropdowns carregavam TODOS os registros de uma vez (sem paginação), causando lentidão com domínios grandes (>1000 itens).
  - **Destino:** SUBSTITUÍDO - API com suporte a paginação e filtros (incluirInativos)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Framework Genérico** | Não (cada domínio tem CRUD próprio) | Sim (API genérica reutilizável) | Reduz código de ~500 LOC por domínio para 0 |
| **Validação de FK** | Não (exclusão física sem validação) | Sim (validação obrigatória antes de exclusão) | Elimina referências órfãs |
| **Auditoria** | Não | Sim (automática via interceptor) | Conformidade LGPD |
| **Multi-Tenancy** | Multi-database físico | Row-Level Security via ClienteId | Reduz complexidade de infraestrutura |
| **Soft Delete** | Não (DELETE físico) | Sim (campo Ativo) | Preserva histórico |
| **Importação** | SQL manual pelo DBA | Upload CSV/Excel com preview | Self-service para administradores |
| **Exportação** | Não | Sim (CSV/Excel) | Facilita análise e backup |
| **Hierarquias** | Não suportado | Sim (campo IdItemPai) | Modela Região > Estado > Cidade |
| **Metadados Customizados** | String parsing na descrição | JSON estruturado (MetadadosJson) | Tipagem, validação, extensibilidade |
| **Reordenação** | Input numérico manual | Drag-and-drop + API atomica | Melhor UX |
| **Código Estável** | Não (apenas Id auto-increment) | Sim (campo Codigo alfanumérico) | Refatorações sem quebrar código |
| **Integrações** | Webservices SOAP | REST API com JWT | Padrão moderno, segurança |

---

## 7. DECISÕES DE MODERNIZAÇÃO

Explique decisões tomadas durante a refatoração.

### Decisão 1: Framework Genérico vs CRUD Específico

- **Decisão:** Criar API genérica reutilizável para todos os domínios, em vez de CRUD específico para cada domínio.
- **Motivo:** Reduz duplicação de código (~500 LOC por domínio × 50 domínios = 25.000 LOC eliminadas). Facilita manutenção e adição de novos domínios sem código.
- **Impacto:** Alto - Exige design cuidadoso da API para suportar todos casos de uso (hierarquias, metadados, importação).

### Decisão 2: Soft Delete Padrão

- **Decisão:** Exclusão lógica (Ativo=false) como padrão, exclusão física apenas com validação de FK e flag explícito.
- **Motivo:** Preserva histórico, evita órfãos, permite "desfazer" exclusões acidentais.
- **Impacto:** Médio - Queries devem filtrar inativos por padrão (impacto em performance se não indexado).

### Decisão 3: Multi-Tenancy via ClienteId (Row-Level Security)

- **Decisão:** Consolidar múltiplos bancos físicos em banco único com isolamento por ClienteId.
- **Motivo:** Simplifica infraestrutura, facilita backup, reduz custos de manutenção.
- **Impacto:** Alto - Exige migração de dados de múltiplos bancos, validação rigorosa de isolamento, testes de segurança.

### Decisão 4: Campo Código Alfanumérico Estável

- **Decisão:** Adicionar campo `Codigo` (alfanumérico, imutável) além de Id auto-increment.
- **Motivo:** Permite refatorações sem quebrar código (ex: alterar descrição de "Alta" para "High Priority" não quebra código que referencia "ALT").
- **Impacto:** Baixo - Exige geração de códigos durante migração de dados legados (script de mapeamento).

### Decisão 5: Metadados JSON vs Campos Fixos

- **Decisão:** Campo MetadadosJson (JSON flexível) em vez de adicionar campos fixos (Cor, Icone, etc.).
- **Motivo:** Permite extensibilidade sem alterar schema, cada domínio pode ter metadados customizados.
- **Impacto:** Baixo - Validação de JSON necessária, frontend precisa parsear JSON.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Perda de dados durante migração multi-database → single database** | Alto | Script de migração validado em ambiente de teste, backup completo antes de migração, rollback plan documentado |
| **Referências órfãs existentes no legado** | Médio | Identificar e corrigir órfãos ANTES da migração (query de auditoria), documentar casos que não podem ser corrigidos |
| **Códigos alfanuméricos gerados conflitarem** | Baixo | Validar unicidade de códigos gerados, usar prefixos por domínio (ex: STATUS_ATI, PRIOR_ALT) |
| **Performance de queries com soft delete** | Médio | Criar índices em campo Ativo, monitorar performance após migração, otimizar queries lentas |
| **Metadados JSON inválidos importados** | Baixo | Validação obrigatória de JSON na API, rejeitar payloads inválidos com mensagem clara |
| **Alteração de comportamento (soft vs hard delete)** | Médio | Comunicar mudança para usuários, treinar administradores, documentar novo comportamento |
| **Multi-tenancy com leak de dados entre clientes** | Alto (CRÍTICO) | Testes rigorosos de isolamento, code review focado em validação de ClienteId, auditoria de acesso |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|---------------|--------|
| Tela `Status_Ativo.aspx` | RN-CAD-104-01, RN-CAD-104-02 | UC01-Criar, UC02-Editar | Migrado |
| Tela `Prioridades.aspx` | RN-CAD-104-01, RN-CAD-104-09 | UC01-Criar, UC02-Editar | Migrado |
| Webservice `ListarStatusAtivo()` | Seção 11 (Endpoints) | UC00-Consultar | Migrado |
| Webservice `CriarStatus()` | RN-CAD-104-01 | UC01-Criar | Migrado |
| Webservice `DeletarStatus()` | RN-CAD-104-03, RN-CAD-104-04 | UC03-Excluir | Migrado |
| Tabela `Ativo_Status` | MD-RF104 (Dominio + ItemDominio) | - | Migrado |
| Tabela `Solicitacao_Status` | MD-RF104 (Dominio + ItemDominio) | - | Migrado |
| Tabela `Prioridade` | MD-RF104 (Dominio + ItemDominio) | - | Migrado |
| Stored Procedure `pa_Ativo_Status_Listar` | Endpoint `GET /api/dominios/Status_Ativo/itens` | UC00-Consultar | Substituído |
| Stored Procedure `pa_Prioridade_Listar` | Endpoint `GET /api/dominios/Prioridade/itens` | UC00-Consultar | Substituído |

---

## 10. STORED PROCEDURES LEGADO

| Procedure | Descrição | Migração | Justificativa |
|-----------|-----------|----------|---------------|
| `pa_Ativo_Status_Listar` | Lista status de ativo (sem filtros) | SUBSTITUÍDA por `GET /api/dominios/Status_Ativo/itens` | API RESTful com filtros (incluirInativos, paginação) |
| `pa_Prioridade_Listar` | Lista prioridades (sem paginação) | SUBSTITUÍDA por `GET /api/dominios/Prioridade/itens` | Paginação, filtros modernos |
| `pa_Ativo_Status_Inserir` | Insere status (sem validação de duplicata) | SUBSTITUÍDA por `POST /api/dominios/Status_Ativo/itens` | Validação de unicidade, auditoria, multi-tenancy |
| `pa_Ativo_Status_Deletar` | Deleta status fisicamente (sem validação FK) | SUBSTITUÍDA por `DELETE /api/dominios/Status_Ativo/itens/{codigo}?softDelete=true` | Soft delete padrão, validação de FK |

---

## 11. WEBSERVICES LEGADOS (ASMX)

| Webservice | Método | Parâmetros | Retorno | Endpoint Moderno | Destino |
|-----------|--------|------------|---------|------------------|---------|
| `StatusService.asmx` | `ListarStatusAtivo()` | Nenhum | `List<StatusDTO>` | `GET /api/dominios/Status_Ativo/itens` | SUBSTITUÍDO |
| `StatusService.asmx` | `CriarStatus(nome)` | `nome: string` | `int (Id)` | `POST /api/dominios/Status_Ativo/itens` | SUBSTITUÍDO |
| `StatusService.asmx` | `DeletarStatus(id)` | `id: int` | `bool` | `DELETE /api/dominios/Status_Ativo/itens/{codigo}` | SUBSTITUÍDO |
| `PrioridadeService.asmx` | `ListarPrioridades()` | Nenhum | `List<PrioridadeDTO>` | `GET /api/dominios/Prioridade/itens` | SUBSTITUÍDO |
| `PrioridadeService.asmx` | `CriarPrioridade(nome, ordem)` | `nome: string, ordem: int` | `int (Id)` | `POST /api/dominios/Prioridade/itens` | SUBSTITUÍDO |

---

## 12. BANCOS LEGADOS MAPEADOS

### Banco: `branco` (Principal)

- **Servidor:** SQL-LEGADO-01
- **Tabelas Relacionadas:**
  - `Ativo_Status`
  - `Solicitacao_Status`
  - `Prioridade`
  - `TipoDocumento`
  - `UnidadeMedida`
  - (outras ~50 tabelas de domínio dispersas)

- **Destino:** CONSOLIDADO em banco único IControlIT.db (SQLite dev) / SQL Server moderno (prod) com multi-tenancy via ClienteId

### Banco: `cliente01` (Cliente Específico)

- **Servidor:** SQL-LEGADO-02
- **Tabelas Relacionadas:** Réplicas de domínios do banco `branco` (estrutura idêntica)
- **Destino:** CONSOLIDADO - Dados migrados para banco único com ClienteId = GUID do cliente01

### Banco: `cliente02` (Cliente Específico)

- **Servidor:** SQL-LEGADO-03
- **Tabelas Relacionadas:** Réplicas de domínios do banco `branco` (estrutura idêntica)
- **Destino:** CONSOLIDADO - Dados migrados para banco único com ClienteId = GUID do cliente02

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Documentação inicial de referência ao legado para RF-104 | Agência ALC - alc.dev.br |

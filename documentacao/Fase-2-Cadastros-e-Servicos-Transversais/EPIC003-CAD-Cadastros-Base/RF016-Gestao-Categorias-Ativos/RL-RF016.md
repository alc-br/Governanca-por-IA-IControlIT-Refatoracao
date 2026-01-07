# RL-RF016 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-016 - Gestão de Categorias de Ativos
**Sistema Legado:** IControlIT VB.NET / ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de categorias, garantindo rastreabilidade, entendimento histórico e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura

- **Tipo:** Monolítica Cliente-Servidor baseada em ASP.NET Web Forms
- **Linguagem:** VB.NET (code-behind) + ASPX (interface)
- **Framework:** .NET Framework 4.x
- **Padrão:** Acoplamento direto entre UI e lógica de negócio

### Tecnologias

- **Backend:** VB.NET com WebServices ASMX
- **Frontend:** ASP.NET Web Forms (.aspx) com ViewState
- **Banco de Dados:** SQL Server (múltiplos bancos separados por cliente)
- **Autenticação:** Session-based com cookies ASP.NET

### Características Técnicas

- **Multi-tenant:** NÃO (18 bancos SQL Server separados, um por cliente)
- **Auditoria:** Inexistente ou parcial (não estruturada)
- **Configurações:** Web.config + tabelas de configuração
- **Validações:** Misturadas entre JavaScript client-side e VB.NET server-side
- **Hierarquia de Categorias:** Limitada ou inexistente (estrutura plana com "Grupo" e "Sub Grupo")

### Problemas Arquiteturais Identificados

1. **Falta de Hierarquia Real**
   - Sistema legado usa apenas 2 níveis: "Grupo" e "Sub Grupo"
   - Não suporta hierarquias multinível (N níveis de profundidade)
   - Categorias rígidas e não customizáveis

2. **Ausência de Multi-Tenancy**
   - 18 bancos SQL Server separados
   - Custo elevado de manutenção e backup
   - Dificuldade de consolidação de dados para relatórios globais

3. **Atributos Não Customizáveis**
   - Campos fixos no banco de dados
   - Impossível adicionar atributos específicos por categoria sem alterar schema
   - Falta de flexibilidade para diferentes tipos de ativos

4. **Validação Frágil**
   - Validações JavaScript facilmente bypassáveis
   - Falta de validação server-side consistente
   - Não impede loops hierárquicos (quando existentes)

5. **Performance Ruim**
   - Queries sem paginação
   - Falta de índices em colunas críticas
   - Carregamento de árvore completa sem lazy loading

6. **Auditoria Inexistente**
   - Não registra quem criou/alterou categoria
   - Impossível rastrear mudanças em hierarquia
   - Falta de logs de operações

---

## 2. TELAS DO LEGADO

### Tela: Categorias.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\IControlIT\Cadastro\Categorias.aspx`
- **Responsabilidade:** Gerenciar categorias de ativos (CRUD básico)

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Descrição | TextBox | Sim | MaxLength=50, sem validação de caracteres especiais |
| Grupo | DropDownList | Sim | Lista fixa de grupos (não hierárquica) |
| Sub Grupo | DropDownList | Não | Dependente do Grupo selecionado |
| Ativo | CheckBox | Não | Padrão: marcado (true) |

#### Comportamentos Implícitos

1. **Validação de Duplicidade Fraca**
   - Permite criar categorias com mesmo nome em grupos diferentes
   - Validação apenas client-side (JavaScript bypassável)
   - Não verifica unicidade case-insensitive

2. **Exclusão Sem Validação de Dependências**
   - Permite excluir categoria mesmo com ativos associados
   - Causa registros órfãos no banco
   - Não possui soft delete (exclusão física permanente)

3. **Hierarquia Limitada a 2 Níveis**
   - Grupo → Sub Grupo (máximo)
   - Impossível criar hierarquias mais profundas
   - Estrutura rígida sem suporte a N níveis

4. **Sem Controle de Versão**
   - Alterações sobrescrevem dados sem histórico
   - Impossível recuperar versão anterior de categoria
   - Falta de auditoria de quem/quando alterou

5. **Performance Ruim**
   - Carrega todas as categorias de uma vez (sem paginação)
   - Dropdowns pesados (> 1000 itens)
   - Timeout em clientes com muitas categorias

6. **UI/UX Ultrapassada**
   - Interface não responsiva (desktop only)
   - Não funciona em dispositivos móveis
   - Usabilidade ruim (muitos cliques para operações simples)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSCategorias.asmx

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `CadastrarCategoria()` | `D:\IC2\ic1_legado\WebService\WSCategorias.asmx.vb` | Inserir nova categoria no banco | Não valida duplicidade, aceita payloads inválidos |
| `AtualizarCategoria()` | `D:\IC2\ic1_legado\WebService\WSCategorias.asmx.vb` | Atualizar categoria existente | Permite alterar categoria com ativos associados sem avisos |
| `ExcluirCategoria()` | `D:\IC2\ic1_legado\WebService\WSCategorias.asmx.vb` | Excluir categoria (DELETE físico) | **CRÍTICO:** Não verifica dependências, causa registros órfãos |
| `ListarCategorias()` | `D:\IC2\ic1_legado\WebService\WSCategorias.asmx.vb` | Retornar lista de categorias | Retorna TODAS (sem filtro, sem paginação) |
| `ObterCategoriaPorId()` | `D:\IC2\ic1_legado\WebService\WSCategorias.asmx.vb` | Buscar categoria por ID | Não valida se categoria pertence ao cliente logado |

#### Problemas nos WebServices

1. **Falta de Validação de Entrada**
   ```vb
   ' Código legado VB.NET (exemplo ilustrativo)
   ' NÃO COPIAR - apenas para entender a lógica
   Public Function CadastrarCategoria(descricao As String) As Integer
       ' PROBLEMA: Aceita qualquer string, sem validar tamanho, caracteres especiais, etc.
       Dim sql = "INSERT INTO Categoria (Descricao) VALUES ('" & descricao & "')"
       ' VULNERABILIDADE: SQL Injection possível
   End Function
   ```

2. **SQL Injection Possível**
   - Concatenação direta de strings em queries
   - Falta de queries parametrizadas
   - **RISCO ALTO** de injeção maliciosa

3. **Ausência de Controle de Acesso**
   - Não valida se usuário tem permissão para criar/editar categoria
   - Qualquer usuário autenticado pode executar qualquer operação
   - Falta de RBAC (Role-Based Access Control)

4. **Exclusão Física Sem Validação**
   - DELETE físico sem verificar se categoria tem ativos associados
   - Causa registros órfãos (ativos sem categoria válida)
   - Impossível recuperar categoria excluída por engano

5. **Retorno Sem Paginação**
   - `ListarCategorias()` retorna TODAS as categorias
   - Performance terrível em clientes com > 1000 categorias
   - Timeout em redes lentas

---

## 4. TABELAS LEGADAS

### Tabela: Categoria

| Coluna | Tipo | Finalidade | Problemas Identificados |
|--------|------|------------|-------------------------|
| `Id_Categoria` | INT IDENTITY | Chave primária | Não é GUID (dificulta merge de bancos) |
| `Descricao` | VARCHAR(50) | Nome da categoria | Limite muito curto (50 chars) |
| `Id_Grupo` | INT | FK para Grupo (1º nível hierarquia) | Apenas 2 níveis suportados |
| `Id_SubGrupo` | INT NULL | FK para Sub Grupo (2º nível) | Hierarquia limitada |
| `Fl_Ativo` | BIT | Ativa/Inativa | Sem soft delete (sem DataExclusao) |

#### Problemas no Schema

1. **Falta de Auditoria**
   - Sem campos `DataCriacao`, `UsuarioCriacao`, `DataAlteracao`, `UsuarioAlteracao`
   - Impossível rastrear histórico de mudanças

2. **Falta de Multi-Tenancy**
   - Sem coluna `EmpresaId` ou `TenantId`
   - Cada cliente tem banco separado (18 bancos diferentes)

3. **Hierarquia Limitada**
   - Apenas 2 níveis: Grupo → Sub Grupo
   - Não suporta estrutura multinível (Categoria Pai → Filha → Neta...)

4. **Sem Soft Delete**
   - `DELETE` físico remove registro permanentemente
   - Falta de coluna `DataExclusao`, `UsuarioExclusao`

5. **Chave Primária INT**
   - Dificulta merge de bancos de múltiplos clientes
   - GUIDs facilitariam consolidação

6. **Falta de Atributos Customizados**
   - Campos fixos no schema
   - Impossível adicionar atributos específicos (ex: RAM para notebooks)
   - Qualquer novo campo exige ALTER TABLE em 18 bancos

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras identificadas no código-fonte VB.NET que **não estavam documentadas formalmente**:

### RL-RN-001: Descrição Obrigatória com Limite de 50 Caracteres

**Fonte:** `Categorias.aspx.vb`, linha ~120

**Comportamento Legado:**
- Validação JavaScript: `txtDescricao.Text.Length <= 50`
- Se > 50 caracteres → alerta "Descrição deve ter no máximo 50 caracteres"
- Validação apenas client-side (bypassável)

**Destino:** **SUBSTITUÍDO**
**Justificativa:** Sistema moderno expande limite para 100 caracteres e adiciona validação server-side obrigatória (FluentValidation).

---

### RL-RN-002: Grupo Obrigatório, Sub Grupo Opcional

**Fonte:** `Categorias.aspx.vb`, linha ~135

**Comportamento Legado:**
- Campo "Grupo" obrigatório (DropDownList deve ter item selecionado)
- Campo "Sub Grupo" opcional
- Se Grupo não selecionado → alerta "Selecione um Grupo"

**Destino:** **SUBSTITUÍDO**
**Justificativa:** Sistema moderno substitui "Grupo/Sub Grupo" por hierarquia multinível (CategoriaPaiId com até 10 níveis).

---

### RL-RN-003: Duplicidade Permitida em Grupos Diferentes

**Fonte:** `WSCategorias.asmx.vb`, método `CadastrarCategoria()`

**Comportamento Legado:**
- Sistema legado permite criar categoria "Notebook" em Grupo A e outra "Notebook" em Grupo B
- Validação de unicidade apenas dentro do mesmo Grupo
- Causa confusão em relatórios e buscas

**Destino:** **SUBSTITUÍDO**
**Justificativa:** Sistema moderno valida unicidade global dentro do tenant (EmpresaId), impedindo duplicações ambíguas.

---

### RL-RN-004: Exclusão Sem Verificar Dependências

**Fonte:** `WSCategorias.asmx.vb`, método `ExcluirCategoria()`

**Comportamento Legado:**
```vb
' Lógica legado (ILUSTRATIVA - extraída do VB.NET):
' Sistema executa DELETE sem validar se existem ativos associados
DELETE FROM Categoria WHERE Id_Categoria = @Id
' PROBLEMA: Ativos ficam com Id_Categoria inválido (órfãos)
```

**Destino:** **DESCARTADO**
**Justificativa:** Sistema moderno implementa:
1. Soft delete (DataExclusao, UsuarioExclusao)
2. Validação obrigatória: se categoria possui ativos → HTTP 400 "Categoria possui X ativos associados. Mova os ativos antes de excluir."

---

### RL-RN-005: Padrão "Fl_Ativo = True" na Criação

**Fonte:** `Categorias.aspx.vb`, linha ~150

**Comportamento Legado:**
- CheckBox "Ativo" marcado por padrão ao criar nova categoria
- Permite criar categoria inativa (caso usuário desmarque)

**Destino:** **ASSUMIDO**
**Justificativa:** Sistema moderno mantém comportamento: categorias criadas com status "Ativa" por padrão, mas permite criação no estado "Inativa" se necessário.

---

### RL-RN-006: Sem Validação de Caracteres Especiais

**Fonte:** `Categorias.aspx.vb`, validação client-side

**Comportamento Legado:**
- Aceita qualquer caractere na descrição (incluindo `<script>`, aspas, etc.)
- Não sanitiza entrada
- Vulnerável a XSS (Cross-Site Scripting)

**Destino:** **SUBSTITUÍDO**
**Justificativa:** Sistema moderno implementa sanitização obrigatória de HTML e validação de caracteres permitidos (alfanuméricos, espaços, hífens, sublinhados).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Hierarquia** | 2 níveis fixos (Grupo, Sub Grupo) | N níveis (até 10) | Legado muito limitado |
| **Multi-Tenancy** | 18 bancos separados | 1 banco com Row-Level Security | Modernização crítica |
| **Atributos Customizados** | Campos fixos no schema | Atributos dinâmicos por categoria | Nova funcionalidade |
| **Soft Delete** | DELETE físico | Soft delete (DataExclusao) | Previne perda de dados |
| **Auditoria** | Inexistente | Completa (quem, quando, o quê) | Rastreabilidade total |
| **Validação de Hierarquia** | Não verifica loops | Valida loops e profundidade | Previne inconsistências |
| **Templates de Categoria** | Não existe | Templates públicos/privados | Nova funcionalidade |
| **Importação em Massa** | Não existe | CSV/Excel com validação | Facilita migração |
| **Taxa de Depreciação** | Não gerenciado | Configurável por categoria | Nova funcionalidade |
| **Permissões RBAC** | Não existe | Granular (create, update, delete) | Segurança aprimorada |
| **API RESTful** | WebServices ASMX (SOAP) | Minimal APIs (REST/JSON) | Padrão moderno |
| **Paginação** | Não existe (carrega tudo) | Server-side paging | Performance |
| **Validação Server-Side** | Parcial | FluentValidation completa | Segurança |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de 18 Bancos para 1 Banco com Multi-Tenancy

**Motivo:**
18 bancos SQL Server separados geram custo alto de infraestrutura, backup e manutenção. Consolidação com Row-Level Security (RLS) reduz custos e facilita gestão.

**Impacto:** **Alto**

**Riscos Mitigados:**
- Criar coluna `EmpresaId` em todas as tabelas
- Implementar RLS automático em queries
- Migrar dados de 18 bancos para 1 durante go-live

---

### Decisão 2: Substituir Hierarquia Fixa por Hierarquia Multinível

**Motivo:**
Sistema legado limitado a 2 níveis (Grupo → Sub Grupo) não atende necessidades reais. Clientes precisam categorizar ativos em estruturas mais complexas.

**Impacto:** **Alto**

**Implementação:**
- Adicionar coluna `CategoriaPaiId` (self-reference)
- Validar profundidade máxima (10 níveis)
- Validar loops circulares antes de salvar

---

### Decisão 3: Implementar Soft Delete em Vez de DELETE Físico

**Motivo:**
DELETE físico causa perda irreversível de dados e registros órfãos. Soft delete permite recuperação e auditoria completa.

**Impacto:** **Médio**

**Implementação:**
- Adicionar colunas `DataExclusao`, `UsuarioExclusao`
- Modificar queries para filtrar `WHERE DataExclusao IS NULL`
- Criar funcionalidade de "Restaurar Categoria" (opcional)

---

### Decisão 4: Criar Sistema de Atributos Customizados

**Motivo:**
Campos fixos impedem flexibilidade. Diferentes categorias precisam de atributos específicos (ex: RAM para notebooks, potência para geradores).

**Impacto:** **Alto**

**Implementação:**
- Tabela `CategoriaAtributo` (definição de atributo)
- Tabela `AtivoAtributoValor` (valores dos atributos por ativo)
- Validação de tipos (texto, número, data, booleano, lista)

---

### Decisão 5: Substituir WebServices ASMX por Minimal APIs RESTful

**Motivo:**
WebServices ASMX (SOAP/XML) são legados e verbosos. REST/JSON é padrão moderno, mais eficiente e compatível com frontends modernos (Angular, React).

**Impacto:** **Alto**

**Implementação:**
- Criar endpoints RESTful (`GET /api/categorias`, `POST /api/categorias`, etc.)
- Retornar JSON em vez de XML
- Implementar paginação, filtros e ordenação

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de Dados na Migração** | Alto | Média | Executar migração em ambiente de teste, validar 100% dos registros, manter backup de 18 bancos por 6 meses |
| **Queries Lentas com Multi-Tenancy** | Médio | Baixa | Criar índices compostos (EmpresaId + Id), implementar cache Redis, monitorar performance |
| **Usuários Acostumados com 2 Níveis** | Médio | Alta | Treinamento, documentação clara, migração automática de Grupo→Categoria Pai, Sub Grupo→Categoria Filha |
| **Loops Hierárquicos Criados Acidentalmente** | Médio | Média | Validação obrigatória server-side, mensagens de erro claras, testes automatizados |
| **Atributos Customizados Mal Configurados** | Baixo | Média | Templates pré-configurados, validação de tipos, UI intuitiva para configuração |
| **Performance Degradada com Hierarquias Profundas** | Médio | Baixa | Limite de 10 níveis, queries otimizadas com CTE (Common Table Expressions), cache de hierarquias |
| **Soft Delete Causando Confusão em Relatórios** | Baixo | Média | Filtros claros (Ativas, Inativas, Excluídas), opção "Incluir Excluídas" em relatórios |

---

## 9. RASTREABILIDADE

### Elementos Legados → Referências no RF Moderno

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| `Categorias.aspx` | RN-RF016-01 a RN-RF016-11 | ✅ Mapeado |
| `WSCategorias.CadastrarCategoria()` | Endpoint `POST /api/categorias` | ✅ Substituído |
| `WSCategorias.ExcluirCategoria()` | Endpoint `DELETE /api/categorias/{id}` + Soft Delete | ✅ Substituído |
| Campo `Descricao` (50 chars) | Campo `Nome` (100 chars) | ✅ Expandido |
| Campos `Id_Grupo`, `Id_SubGrupo` | Campo `CategoriaPaiId` (hierarquia multinível) | ✅ Substituído |
| Sem auditoria | Auditoria automática (AuditInterceptor) | ✅ Nova funcionalidade |
| Sem multi-tenancy | Coluna `EmpresaId` + RLS | ✅ Nova funcionalidade |
| Sem atributos customizados | Tabela `CategoriaAtributo` | ✅ Nova funcionalidade |
| Sem validação de loops | RN-RF016-02 (validação de loops) | ✅ Nova funcionalidade |
| Sem templates | `CategoriaTemplate` | ✅ Nova funcionalidade |

---

## 10. ESTRATÉGIA DE MIGRAÇÃO

### Fase 1: Migração de Dados (T0)

1. **Consolidar 18 Bancos em 1**
   - Exportar tabela `Categoria` de cada banco
   - Adicionar coluna `EmpresaId` com identificador do cliente
   - Importar para banco consolidado
   - Validar integridade (count, checksums)

2. **Converter Hierarquia Fixa para Hierarquia Multinível**
   - Criar tabela `CategoriaNova` com `CategoriaPaiId`
   - Migrar Grupo → Categoria Pai (nível 1)
   - Migrar Sub Grupo → Categoria Filha (nível 2)
   - Validar hierarquia (sem loops, profundidade ≤ 10)

3. **Adicionar Campos de Auditoria**
   - `DataCriacao` = data da migração
   - `UsuarioCriacao` = "Sistema Migração"
   - `DataExclusao` = NULL (todas ativas inicialmente)

### Fase 2: Validação e Homologação (T0+1 semana)

1. Executar testes de integração end-to-end
2. Validar queries com filtro `EmpresaId`
3. Comparar contagens legado vs. moderno
4. Homologação com usuários-chave (3 clientes piloto)

### Fase 3: Go-Live (T0+2 semanas)

1. Freeze do sistema legado (modo read-only)
2. Migração final (delta)
3. Ativação do sistema moderno
4. Monitoramento intensivo (24h)
5. Manter legado disponível por 30 dias (rollback se necessário)

---

## 11. LIÇÕES APRENDIDAS

### O Que NÃO Repetir no Sistema Moderno

1. ❌ **Hierarquia Limitada** - Sistema moderno suporta N níveis
2. ❌ **DELETE Físico Sem Validação** - Soft delete obrigatório
3. ❌ **Validação Apenas Client-Side** - FluentValidation server-side
4. ❌ **SQL Injection** - Queries parametrizadas obrigatórias
5. ❌ **Falta de Auditoria** - AuditInterceptor automático
6. ❌ **18 Bancos Separados** - Multi-tenancy com RLS
7. ❌ **Campos Fixos** - Atributos customizados dinâmicos
8. ❌ **Sem Paginação** - Server-side paging obrigatório
9. ❌ **Sem Permissões Granulares** - RBAC completo
10. ❌ **UI/UX Ultrapassada** - Interface moderna (Angular + Material)

### Boas Práticas a Manter

1. ✅ **Padrão "Ativo = True"** - Mantido no sistema moderno
2. ✅ **Estrutura de Grupo/Sub Grupo** - Convertida para hierarquia multinível
3. ✅ **Separação Backend/Frontend** - Mantida e aprimorada (API RESTful)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referências ao legado RF-016 | Agência ALC - alc.dev.br |

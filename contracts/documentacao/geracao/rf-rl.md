# CONTRATO DE GERAÇÃO RF/RL COMPLETO

**Versão:** 1.0
**Data:** 2025-12-30
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **documentação completa e rastreável** de Requisitos Funcionais (RF) com base no **sistema legado**, garantindo:

- ✅ **Completude Total (100%)**: TUDO do legado é documentado no RF
- ✅ **Rastreabilidade Bidirecional**: Legado ↔ RF (cada item tem origem/destino)
- ✅ **Precisão Absoluta**: RNs refletem EXATAMENTE o comportamento legado
- ✅ **Multi-Database**: Análise de TODOS os bancos do legado
- ✅ **Linguagem Natural**: Sem cópia de código VB.NET/SQL

### 📁 Arquivos Gerados

1. **RFXXX.md** - Contrato funcional moderno (11 seções, mínimo 10 RNs)
2. **RFXXX.yaml** - Estrutura canônica sincronizada com RF.md
3. **RL-RFXXX.md** - Referência ao legado (9 seções, memória técnica)
4. **RL-RFXXX.yaml** - Rastreabilidade estruturada de itens legado
5. **STATUS.yaml** - Controle de governança e progresso
6. **documentacao-funcional.md** - Seção RFXXX criada/atualizada (índice centralizado)

⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Completude Total**: RF cobre **100% absoluto** do comportamento legado
2. **Rastreabilidade Bidirecional**: Legado → RF → UC (ida e volta)
3. **Multi-Database**: Análise de **TODOS** os bancos legados
4. **Sem Código**: Regras em **LINGUAGEM NATURAL** (não copiar VB.NET/SQL)
5. **Destinos Obrigatórios**: 100% itens RL com destino (ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR)

### 🔍 Análise Obrigatória do Legado

- ✅ Webservices (.asmx)
- ✅ Telas ASPX (.aspx, .aspx.vb)
- ✅ Tabelas (TODOS os bancos - multi-database)
- ✅ Stored Procedures (TODOS os bancos)
- ✅ Views, Functions, Triggers
- ✅ Connection Strings (web.config)

### ⚠️ REGRA CRÍTICA

**Se QUALQUER funcionalidade do legado não for documentada no RF, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Documentação RF/RL |
| **Escopo** | Criação completa de RF.md, RF.yaml, RL.md, RL.yaml e STATUS.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-RF-RL para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-RF-RL para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **4 arquivos fundamentais** que documentam um Requisito Funcional (RF) de forma **completa, estruturada e rastreável**:

1. **RFXXX.md** - Contrato funcional moderno (o que o sistema DEVE fazer)
2. **RFXXX.yaml** - Estrutura canônica sincronizada com RF.md
3. **RL-RFXXX.md** - Referência ao legado (memória técnica histórica)
4. **RL-RFXXX.yaml** - Rastreabilidade estruturada de itens legado

Além disso, criar ou atualizar:

5. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Completude Total (100%)

**REGRA CRÍTICA:** O RF DEVE cobrir **100% ABSOLUTO** do comportamento do legado.

- ✅ TUDO que existe no legado DEVE estar documentado no RF
- ✅ Nenhuma funcionalidade legada pode ser ignorada ou esquecida
- ✅ Cada regra de negócio do legado DEVE ter correspondente no RF
- ✅ Cada validação do legado DEVE estar explícita no RF
- ✅ Cada fluxo do legado DEVE ter UC correspondente

**Se houver dúvida sobre algum comportamento legado:**
- ❌ NÃO assumir que pode ser ignorado
- ❌ NÃO deixar de documentar
- ✅ Documentar como "A_REVISAR" no RL
- ✅ Criar RN provisória no RF para cobertura

### 3.2 Princípio da Rastreabilidade Bidirecional

**REGRA CRÍTICA:** Cada item do RF DEVE apontar para sua origem no legado.

- ✅ Toda RN no RF DEVE referenciar item(s) no RL (seção Rastreabilidade)
- ✅ Todo item no RL DEVE apontar para RN/UC no RF (campo `rf_item_relacionado`)
- ✅ Criar matriz de rastreabilidade: Legado → RF → UC

**Formato obrigatório de rastreabilidade:**

Em **RFXXX.md** (ao final de cada RN):
```markdown
### RN-RFXXX-05: Email deve ser único
**Descrição:** Email deve ser único por tenant.
**Justificativa:** Evitar duplicação de contas.
**Origem Legado:** RL-RFXXX (LEG-RFXXX-003 - Stored Procedure sp_ValidarEmailUnico)
```

Em **RL-RFXXX.yaml** (para cada item):
```yaml
- id: "LEG-RFXXX-003"
  tipo: "stored_procedure"
  nome: "sp_ValidarEmailUnico"
  destino: "assumido"
  rf_item_relacionado: "RN-RFXXX-05"  # OBRIGATÓRIO
  uc_relacionado: "UC01"
```

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\rf\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |
| **LEGACY_PATH** | `D:\IC2\ic1_legado\IControlIT\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\RFXXX.md
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\RFXXX.yaml
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\RL-RFXXX.md
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\RL-RFXXX.yaml
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`
- Qualquer arquivo que não seja os 5 listados acima

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF | Pasta já criada em `rf/[Fase]/[EPIC]/RFXXX/` | Sim |
| Templates acessíveis | Templates em `D:\IC2\docs\templates\` disponíveis | Sim |
| Legado acessível | Código legado em `D:\IC2\ic1_legado\` disponível | Sim |
| Documentação funcional | ` D:\IC2\rf\documentacao-funcional.md` acessível (referência) | Não* |

**PARAR se qualquer item falhar.**

**Nota sobre documentacao-funcional.md:**
- Este arquivo é uma **referência opcional** que pode conter informações sobre o RF
- Se o RF **AINDA NÃO** estiver documentado lá, o agente DEVE fazer a pesquisa completa no legado
- Após concluir a criação dos 4 arquivos (RF.md, RF.yaml, RL.md, RL.yaml), o agente DEVE **atualizar** o `documentacao-funcional.md` com as informações do RF criado
- Formato: Adicionar seção do RF com resumo executivo e link para os arquivos gerados

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Análise do Legado (OBRIGATÓRIA - 100% COMPLETUDE)

Antes de criar qualquer documento, o agente DEVE realizar análise **EXAUSTIVA** de TODAS as fontes legadas.

**REGRA CRÍTICA:** A análise do legado DEVE ser **100% completa**. Não pode haver nenhuma funcionalidade, regra ou validação esquecida.

#### 1.1 Identificar Webservices Relacionados
- Localização: `D:\IC2\ic1_legado\IControlIT\[modulo]\WebService\`
- Ler **TODOS** os arquivos `.asmx` e `.cs` relacionados ao RF
- Identificar **TODOS** os métodos públicos
- Extrair **TODAS** as validações (try-catch, if-else, switch-case)
- Mapear **TODAS** as dependências (outros webservices, procedures)

**Critério de completude:**
- ✅ Todos os webservices do módulo analisados
- ✅ Todos os métodos públicos documentados
- ✅ Todas as validações extraídas

#### 1.2 Analisar Telas ASPX
- Localização: `D:\IC2\ic1_legado\IControlIT\[modulo]\`
- Ler **TODAS** as telas `.aspx` relacionadas ao RF
- Analisar código-behind `.aspx.cs` ou `.aspx.vb` **COMPLETO**
- Identificar **TODOS** os controles (TextBox, DropDown, GridView, etc.)
- Mapear **TODOS** os eventos (Button_Click, Page_Load, etc.)
- Entender **TODOS** os fluxos do usuário (happy path + edge cases)

**Critério de completude:**
- ✅ Todas as telas do módulo analisadas
- ✅ Todos os controles identificados
- ✅ Todos os eventos mapeados
- ✅ Todos os fluxos documentados

#### 1.3 Mapear Tabelas do Banco (MULTI-DATABASE)

**ATENÇÃO CRÍTICA:** O legado pode ter **MÚLTIPLOS BANCOS DE DADOS** (multi-database por cliente).

**OBRIGATÓRIO:**
- Analisar **TODOS** os bancos relacionados ao módulo
- Identificar padrão de nomenclatura (ex: `IControlIT_Cliente01`, `IControlIT_Cliente02`)
- Mapear **TODAS** as tabelas em **TODOS** os bancos

**Estrutura de análise:**
```bash
# Exemplo de estrutura multi-database no legado
IControlIT_Cliente01/
  ├── dbo.Empresa
  ├── dbo.Filial
  └── dbo.Usuario

IControlIT_Cliente02/
  ├── dbo.Empresa
  ├── dbo.Filial
  └── dbo.Usuario

# O agente DEVE analisar TODOS os bancos para identificar:
# - Diferenças de schema entre bancos (migração incremental)
# - Regras específicas por banco (hard-coded)
# - Dados de produção que revelam comportamentos implícitos
```

**Critério de completude:**
- ✅ Todos os bancos mapeados (verificar web.config / connection strings)
- ✅ Todas as tabelas relacionadas identificadas
- ✅ Todos os relacionamentos (FKs) documentados
- ✅ Diferenças de schema entre bancos registradas

#### 1.4 Listar Stored Procedures (TODOS OS BANCOS)

**OBRIGATÓRIO:**
- Localização: `D:\IC2\ic1_legado\Database\Procedures\` (se existir)
- Analisar **TODAS** as stored procedures relacionadas ao módulo
- Buscar em **TODOS** os bancos (multi-database)
- Identificar **TODAS** as procedures usadas pelas telas/webservices

**Critério de completude:**
- ✅ Todas as procedures identificadas
- ✅ Todos os parâmetros (entrada/saída) documentados
- ✅ Toda lógica de negócio extraída (em linguagem natural)
- ✅ Todas as validações SQL identificadas

#### 1.5 Analisar Views, Functions, Triggers

**OBRIGATÓRIO:**
- Buscar **TODAS** as views relacionadas ao módulo
- Identificar **TODAS** as user-defined functions (UDF)
- Mapear **TODOS** os triggers (INSERT, UPDATE, DELETE)
- Extrair **TODA** lógica de negócio implícita

**Critério de completude:**
- ✅ Todas as views analisadas
- ✅ Todas as UDFs documentadas
- ✅ Todos os triggers mapeados

#### 1.6 Análise de Connection Strings e Configurações

**OBRIGATÓRIO:**
- Ler `web.config` do legado
- Identificar **TODAS** as connection strings
- Mapear **TODOS** os bancos utilizados
- Documentar configurações específicas por ambiente

**Critério de completude:**
- ✅ Todas as connection strings mapeadas
- ✅ Todos os bancos identificados
- ✅ Configurações de multi-tenancy documentadas

### Fase 2: Extração de Regras de Negócio

```
- Ler código VB.NET/C# dos webservices
- Analisar validações no código
- Identificar regras implícitas
- Documentar 10-15 regras em LINGUAGEM NATURAL (sem código!)
```

**REGRA CRÍTICA:** Não copiar código VB.NET ou SQL. Todas as regras devem ser escritas em LINGUAGEM NATURAL.

### Fase 3: Criação RFXXX.md (Contrato Funcional Moderno)

#### 3.1 Criar RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\RF.md`

**Estrutura obrigatória (11 seções):**

1. **Seção 1: Objetivo do Requisito**
   - Resumo executivo do requisito
   - Objetivo principal
   - Problema resolvido

2. **Seção 2: Escopo**
   - O que está dentro do escopo (checklist)
   - Fora do escopo (não objetivos)

3. **Seção 3: Conceitos e Definições**
   - Tabela de termos e definições
   - Entidades principais
   - Conceitos de domínio

4. **Seção 4: Funcionalidades Cobertas**
   - Lista numerada de funcionalidades
   - Descrição de cada funcionalidade
   - Prioridade (CRÍTICA, ALTA, MÉDIA, BAIXA)

5. **Seção 5: Regras de Negócio**
   - Mínimo 10 regras de negócio (RN-RFXXX-NNN)
   - Formato: `### RN-RFXXX-01 — [Título]`
   - Descrição, Justificativa, Critério de Aceite
   - Sem código VB.NET ou SQL
   - Sem referências ao legado (telas ASPX, webservices, stored procedures)

6. **Seção 6: Estados da Entidade**
   - Tabela de estados possíveis
   - Descrição de cada estado
   - Transições permitidas/proibidas

7. **Seção 7: Permissões RBAC**
   - Matriz de permissões (Funcionalidade × Role)
   - Permission codes (ex: `CAD.EMPRESAS.CREATE`)
   - Roles autorizadas para cada permissão

8. **Seção 8: API Endpoints**
   - Lista de endpoints REST (GET, POST, PUT, DELETE)
   - Rota de cada endpoint
   - Autenticação/autorização obrigatória
   - Request/Response DTOs

9. **Seção 9: Modelo de Dados**
   - Referência ao arquivo `MD-RFXXX.md` (a ser criado depois)
   - Principais entidades envolvidas
   - Relacionamentos críticos

10. **Seção 10: Dependências**
    - RFs dependentes (upstream)
    - RFs que dependem deste (downstream)
    - Dependências de bibliotecas externas

11. **Seção 11: Integrações Obrigatórias**
    - i18n (Transloco - pt-BR/en/es)
    - Auditoria (campos Created, CreatedBy, LastModified, LastModifiedBy)
    - RBAC (permissões baseadas em roles)
    - Central de Funcionalidades (registro obrigatório)

**PROIBIDO em RFXXX.md:**
- ❌ Referências a telas ASPX do legado
- ❌ Referências a webservices VB.NET
- ❌ Referências a stored procedures SQL
- ❌ Código legado copiado
- ❌ Screenshots do sistema antigo
- ❌ Comparações "legado vs moderno"

**OBRIGATÓRIO em RFXXX.md:**
- ✅ Regras de negócio em linguagem natural
- ✅ Endpoints REST API modernos
- ✅ Integrações obrigatórias (i18n, auditoria, RBAC, Central)
- ✅ Modelo de dados moderno (multi-tenancy, auditoria)
- ✅ Mínimo 10 regras de negócio (RN-RFXXX-NNN)

---

### Fase 4: Criação RFXXX.yaml (Estruturado Sincronizado)

#### 4.1 Criar RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\RF.yaml`

**Estrutura obrigatória:**

```yaml
# =============================================
# RF - Requisito Funcional (Contrato Canônico)
# Versão: 1.0
# Autor padrão: Agência ALC - alc.dev.br
# =============================================

rf:
  id: "RFXXX"
  nome: "[Nome do Requisito Funcional]"
  versao: "1.0"
  data: "YYYY-MM-DD"
  fase: "Fase X - Nome da Fase"
  epic: "EPICXXX-YYY-ZZZ"
  status: "draft" # draft | aprovado | em_desenvolvimento | concluido

descricao:
  objetivo: "Descrever claramente o objetivo do requisito."
  problema_resolvido: "Qual problema de negócio este RF resolve."
  publico_afetado: "Quem utiliza ou é impactado por este RF."

escopo:
  incluso:
    - "Funcionalidade incluída 1"
    - "Funcionalidade incluída 2"
  fora:
    - "Funcionalidade fora do escopo"

entidades:
  - nome: "entidade_principal"
    descricao: "Entidade central do requisito"
    multi_tenant: true
    soft_delete: true
    auditoria: true

regras_negocio:
  - id: "RN-RFXXX-01"
    descricao: "Descrição objetiva da regra"
    tipo: "validacao" # validacao | unicidade | regra_negocio | seguranca
    campos_afetados: ["campo"]
    obrigatorio: true

  - id: "RN-RFXXX-02"
    descricao: "Outra regra relevante"
    tipo: "unicidade"
    campos_afetados: ["tenant_id", "campo"]

  # ... Repetir para todas as RNs (mínimo 10)

estados:
  - id: "pending"
    descricao: "Criado, aguardando processamento"
  - id: "active"
    descricao: "Ativo"
  - id: "inactive"
    descricao: "Inativo"

transicoes:
  permitidas:
    - de: "pending"
      para: "active"
    - de: "active"
      para: "inactive"

permissoes:
  - codigo: "entidade.view_any"
    descricao: "Listar registros"
  - codigo: "entidade.view"
    descricao: "Visualizar registro"
  - codigo: "entidade.create"
    descricao: "Criar registro"
  - codigo: "entidade.update"
    descricao: "Atualizar registro"
  - codigo: "entidade.delete"
    descricao: "Excluir registro"

endpoints:
  - method: "GET"
    route: "/api/entidades"
    descricao: "Listar entidades com paginação"
    autenticacao: true
    authorization_policy: "EntidadeRead"

  - method: "POST"
    route: "/api/entidades"
    descricao: "Criar nova entidade"
    autenticacao: true
    authorization_policy: "EntidadeCreate"

  # ... Repetir para todos os endpoints

integracoes:
  internas:
    - "Autenticacao"
    - "Multi-Tenancy"
    - "Auditoria"
    - "i18n (Transloco)"
    - "Central de Funcionalidades"
  externas: []

seguranca:
  isolamento_tenant: true
  auditoria_obrigatoria: true
  soft_delete: true

rastreabilidade:
  ucs_esperados:
    - "UC00"
    - "UC01"
    - "UC02"
    - "UC03"
    - "UC04"
```

**Regra CRÍTICA:** RFXXX.yaml DEVE estar 100% sincronizado com RFXXX.md
- Todas as RNs do MD devem estar no YAML
- Todos os endpoints do MD devem estar no YAML
- Todas as permissões do MD devem estar no YAML

---

### Fase 5: Criação RL-RFXXX.md (Referência ao Legado)

#### 5.1 Criar RL-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\RL.md`

**Estrutura obrigatória (9 seções):**

1. **Seção 1: Contexto do Sistema Legado**
   - Stack tecnológica (ASP.NET Web Forms, VB.NET, SQL Server)
   - Arquitetura geral (monolito, multi-database)
   - Problemas arquiteturais identificados

2. **Seção 2: Telas ASPX e Código-Behind**
   - Lista de telas ASPX relacionadas ao RF
   - Caminho completo no legado (`ic1_legado/IControlIT/[modulo]/[tela].aspx`)
   - Funcionalidades principais de cada tela
   - Regras de negócio implícitas no code-behind VB.NET
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

3. **Seção 3: Webservices (.asmx)**
   - Lista de webservices relacionados
   - Caminho completo (`ic1_legado/IControlIT/[modulo]/WebService/[service].asmx`)
   - Métodos públicos expostos
   - Parâmetros e tipos de retorno
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

4. **Seção 4: Stored Procedures**
   - Lista de stored procedures usadas
   - Caminho completo (`ic1_legado/Database/Procedures/[procedure].sql`)
   - Parâmetros de entrada/saída
   - Lógica principal (em linguagem natural, sem copiar SQL)
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

5. **Seção 5: Tabelas Legadas**
   - Lista de tabelas do SQL Server relacionadas
   - Problemas identificados (falta de FK, campos sem validação, etc.)
   - Mapeamento para tabelas modernas (ou NULL se descartado)
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

6. **Seção 6: Regras de Negócio Implícitas**
   - Regras NÃO documentadas encontradas no código
   - Validações hard-coded no VB.NET
   - Business logic escondida em stored procedures
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

7. **Seção 7: Gap Analysis (Legado × Moderno)**
   - Funcionalidades do legado que NÃO serão migradas (justificativa)
   - Funcionalidades novas do sistema moderno (não existiam no legado)
   - Mudanças de comportamento entre legado e moderno
   - Riscos de migração identificados

8. **Seção 8: Decisões de Modernização**
   - Explique decisões tomadas durante a refatoração
   - Motivo (justificativa)
   - Impacto (Alto / Médio / Baixo)

9. **Seção 9: Rastreabilidade**
   - Tabela mapeando elemento legado → referência RF
   - Exemplo: `Tela EmpresasCadastrar.aspx → RF060 Seção 5 (RN-RF060-03)`

**PROIBIDO em RL-RFXXX.md:**
- ❌ Copiar código VB.NET diretamente
- ❌ Copiar SQL diretamente
- ❌ Deixar itens sem destino definido

**OBRIGATÓRIO em RL-RFXXX.md:**
- ✅ Extrair regras em LINGUAGEM NATURAL
- ✅ Definir destino para 100% dos itens (ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR)
- ✅ Documentar 3-6 problemas mínimo do legado
- ✅ Mapear bancos legados (se aplicável)

---

### Fase 6: Criação RL-RFXXX.yaml (Estruturado com Destinos)

#### 6.1 Criar RL-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\RL.yaml`

**Estrutura obrigatória:**

```yaml
# Template de Referência ao Legado (RL-RFXXX.yaml)
# Versão: 2.0 (Adequação para Automação e Rastreabilidade)
# Data: 2025-12-30

rf_id: RFXXX
titulo: "[Título do RF Moderno]"

legado:
  sistema: "VB.NET + ASP.NET Web Forms"
  versao: "[Versão do sistema legado]"
  arquitetura: "Monolítica WebForms"
  banco_dados: "SQL Server"
  multi_tenant: false
  auditoria: "none"  # none | partial | full

# SEÇÃO CRÍTICA: Referências ao Legado com Destino Obrigatório
# Cada item DEVE ter campo "destino" preenchido
referencias:
  - id: "LEG-RFXXX-001"
    tipo: "tela"  # tela | webservice | stored_procedure | regra_negocio | componente | tabela
    nome: "[Nome da tela/componente legado]"
    caminho: "ic1_legado/IControlIT/[caminho]"
    descricao: |
      [Descrição do comportamento legado]
      [Incluir regras implícitas, validações, etc]

    # CAMPO OBRIGATÓRIO: Destino do item legado
    destino: "assumido"  # assumido | substituido | descartado | a_revisar
    justificativa: |
      [Por que este comportamento foi assumido/substituído/descartado]
      [Impacto da decisão]

    # Rastreabilidade (opcional mas recomendado)
    rf_item_relacionado: "RN-RFXXX-01"  # Regra de negócio no RF moderno
    uc_relacionado: "UC01"  # Caso de uso que implementa

    # Metadados adicionais (opcional)
    complexidade: "alta"  # baixa | media | alta
    risco_migracao: "medio"  # baixo | medio | alto
    prioridade: 1  # 1 (crítico) a 5 (baixo)

  # ... Repetir para todos os itens legado identificados (telas, webservices, procedures, regras)

# ==============================================================================
# BANCOS LEGADOS MAPEADOS (OBRIGATÓRIO SE MULTI-DATABASE)
# ==============================================================================
# ATENÇÃO: O legado pode ter MÚLTIPLOS BANCOS (um por cliente).
# É OBRIGATÓRIO mapear TODOS os bancos relacionados ao módulo.

bancos_legados:
  - nome: "IControlIT_Cliente01"
    servidor: "SQL-LEGADO-01"
    connection_string_key: "IControlITCliente01"  # Chave no web.config
    tabelas_relacionadas:
      - nome: "dbo.Empresa"
        registros_producao: 150  # Quantidade de registros em produção
        problemas:
          - "Falta FK para dbo.Filial"
          - "Campo Cnpj sem validação de formato"
      - nome: "dbo.Filial"
        registros_producao: 320
        problemas:
          - "Relacionamento com Empresa via ID int (não GUID)"
      - nome: "dbo.Usuario"
        registros_producao: 1200
        problemas:
          - "Senha em texto plano (CRÍTICO)"
          - "Sem auditoria de login"
    stored_procedures:
      - "sp_InserirEmpresa"
      - "sp_ValidarCnpjUnico"
      - "sp_ConsultarEmpresasPorFilial"
    views:
      - "vw_EmpresasAtivas"
      - "vw_EmpresasComFiliais"
    triggers:
      - nome: "trg_Empresa_Audit"
        eventos: ["INSERT", "UPDATE"]
        observacao: "Trigger manual de auditoria (substitui auditoria automática)"
    destino: "CONSOLIDADO"
    justificativa: |
      Migrado para banco único com multi-tenancy (Row-Level Security).
      Todos os registros foram migrados para IControlIT.db com campo ClienteId.
      Triggers foram substituídos por AuditInterceptor (EF Core).
    banco_moderno: "IControlIT.db (SQLite dev) / SQL Server moderno (prod)"
    migrado_em: "2025-01-15"
    responsavel_migracao: "Agente Architect"

  - nome: "IControlIT_Cliente02"
    servidor: "SQL-LEGADO-02"
    connection_string_key: "IControlITCliente02"
    tabelas_relacionadas:
      - nome: "dbo.Empresa"
        registros_producao: 85
        problemas:
          - "Schema diferente do Cliente01 (campo RazaoSocial vs Nome)"
          - "Falta coluna Email (adicionada em 2023)"
      - nome: "dbo.Filial"
        registros_producao: 180
    stored_procedures:
      - "sp_InserirEmpresa"
      - "sp_AtualizarEmpresa_v2"  # Versão diferente do Cliente01!
    destino: "CONSOLIDADO"
    justificativa: |
      Migrado para banco único com multi-tenancy.
      Schema normalizado para padrão do Cliente01 antes da migração.
      Campo RazaoSocial renomeado para Nome durante migração.
    banco_moderno: "IControlIT.db (SQLite dev) / SQL Server moderno (prod)"
    migrado_em: "2025-01-18"
    responsavel_migracao: "Agente Architect"

  # OBRIGATÓRIO: Mapear TODOS os bancos do legado (verificar web.config)
  # Cada banco pode ter diferenças de schema, procedures, triggers
  # TODAS as diferenças DEVEM ser documentadas

# ==============================================================================
# PROBLEMAS LEGADO IDENTIFICADOS
# ==============================================================================

problemas_legado:
  - id: "PROB-RFXXX-001"
    titulo: "[Problema Arquitetural ou Técnico]"
    severidade: "ALTA"  # CRÍTICA, ALTA, MÉDIA, BAIXA
    descricao: |
      [Descrição detalhada do problema no sistema legado]
    impacto: "[Impacto no sistema ou usuários]"
    solucao_moderna: "[Como foi resolvido no sistema moderno]"

  # ... Documentar 3-6 problemas mínimo

# ==============================================================================
# METADADOS
# ==============================================================================

metadados:
  total_itens_legado: 0  # Calculado automaticamente
  itens_assumidos: 0
  itens_substituidos: 0
  itens_descartados: 0
  itens_a_revisar: 0
  cobertura_destinos: "0%"  # Deve ser sempre 100%
```

**Regra CRÍTICA:** RL-RFXXX.yaml DEVE estar 100% sincronizado com RL-RFXXX.md
- Todos os itens do MD devem estar no YAML
- Todos os itens devem ter campo `destino` preenchido
- Metadados devem ser calculados automaticamente

---

### Fase 7: Validação Obrigatória

#### 7.1 Executar Validador de Separação RF/RL

```bash
# Validar que RF não contém legado e RL tem destinos definidos
python D:\IC2_Governanca\tools\docs\validator-rl.py RFXXX
```

**Critérios de validação:**
- ✅ RFXXX.md não contém referências ao legado
- ✅ RL-RFXXX.md contém TODA memória legado
- ✅ 100% dos itens em RL-RFXXX.yaml têm campo `destino`
- ✅ RFXXX.md ↔ RFXXX.yaml sincronizados
- ✅ RL-RFXXX.md ↔ RL-RFXXX.yaml sincronizados

**Se validador falhar (exit code ≠ 0):**
- ❌ PARAR a execução
- ❌ NÃO atualizar STATUS.yaml
- ❌ Corrigir gaps identificados
- ✅ Re-executar validador até passar

---

### Fase 8: Consulta Inicial à Documentação Funcional (OPCIONAL)

#### 8.1 Ler documentacao-funcional.md (Referência)

Antes de iniciar a análise do legado, o agente DEVE:

1. **Ler** o arquivo ` D:\IC2\rf\documentacao-funcional.md`
2. **Verificar** se o RFXXX já está documentado nele
3. **Usar** como referência inicial (se existir)

**Cenários possíveis:**

**Cenário A: RF já documentado em documentacao-funcional.md**
- ✅ Usar como **ponto de partida** (não como fonte da verdade)
- ✅ Validar informações contra o legado
- ✅ Complementar com análise exaustiva do legado
- ✅ Atualizar documentacao-funcional.md ao final se houver divergências

**Cenário B: RF NÃO documentado em documentacao-funcional.md**
- ✅ Realizar análise **100% completa** do legado (Fase 1)
- ✅ Criar toda documentação do zero
- ✅ **Atualizar** documentacao-funcional.md ao final (Fase 9)

**IMPORTANTE:**
- documentacao-funcional.md é **REFERÊNCIA**, não **FONTE DA VERDADE**
- A **FONTE DA VERDADE** é o **código legado** (ic1_legado)
- Sempre validar informações contra o legado

---

### Fase 9: Criação/Atualização STATUS.yaml

#### 9.1 Criar ou Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Estrutura obrigatória:**

```yaml
rf: RFXXX
fase: Fase-X-Nome-da-Fase
epic: EPICXXX-YYY-ZZZ
titulo: [Título do Requisito Funcional]

# ============================================================
# 1. SKELETON / BASE ATUAL
# ============================================================
skeleton:
  criado: False
  data_criacao: null
  observacao: "Documentação RF/RL criada. Backend/Frontend ainda não iniciados."

# ============================================================
# 2. DOCUMENTACAO (CONTRATOS)
# ============================================================
documentacao:
  rf: True                # RFXXX.md criado (contrato moderno)
  rf_yaml: True           # RFXXX.yaml criado (estruturado)
  rl: True                # RL-RFXXX.md criado (memória legado)
  rl_yaml: True           # RL-RFXXX.yaml criado (rastreabilidade)
  uc: False               # UC-RFXXX.md ainda não criado
  uc_yaml: False
  md: False               # MD-RFXXX.md ainda não criado
  md_yaml: False
  wf: False               # WF-RFXXX.md ainda não criado
  tc: False               # TC ainda não criados

  arquivos_obrigatorios_presentes: True
  separacao_rf_rl_validada: True

# ==============================================================================
# VALIDAÇÃO SEPARAÇÃO RF/RL (OBRIGATÓRIA v2.0)
# ==============================================================================

separacao_rf_rl:
  rf_limpo: True                # RF não contém conteúdo legado
  rl_completo: True             # RL contém TODA memória legado
  itens_com_destino: True       # 100% itens RL têm campo destino
  validador_executado: True     # validator-rl.py passou (exit code 0)

# ==============================================================================
# ESTATÍSTICAS DOCUMENTAÇÃO
# ==============================================================================

estatisticas:
  total_rns: 10                 # Regras de negócio extraídas
  total_endpoints_api: 5        # Endpoints REST documentados
  total_permissoes_rbac: 8      # Permissões RBAC definidas
  total_integracoes_obrigatorias: 5  # i18n, auditoria, RBAC, Central, Multi-tenancy
  itens_legado_rastreados: 15   # Itens em RL-RFXXX.yaml
  bancos_legados_mapeados: 0    # Bancos SQL Server antigos (se aplicável)
  problemas_legado_identificados: 3  # Problemas documentados

# ============================================================
# 3. DESENVOLVIMENTO
# ============================================================
desenvolvimento:
  backend:
    status: not_started   # not_started | skeleton | in_progress | done
    branch: null
  frontend:
    status: not_started
    branch: null

# ============================================================
# 4. TESTES (RESULTADO)
# ============================================================
testes:
  backend: not_run        # not_run | pass | fail
  frontend: not_run
  e2e: not_run
  seguranca: not_run

# ============================================================
# 5. DOCUMENTACAO DE TESTES
# ============================================================
documentacao_testes:
  backend: False
  frontend: False
  e2e: False
  seguranca: False

# ============================================================
# 6. TESTES TI / QA
# ============================================================
testes_ti:
  backend: not_run
  frontend: not_run
  e2e: not_run
  seguranca: not_run

testes_qa:
  executado: False
  aprovado: False

# ============================================================
# 7. SINCRONIZACAO COM AZURE DEVOPS
# ============================================================
devops:
  work_item_id: null            # Feature / Epic principal
  test_plan_id: null
  last_sync: null
  board_column: "Backlog"
  sync_policy:
    create_user_story_if_missing: True
    update_status_from_yaml: True
    update_sprint_from_yaml: True
    close_work_item_on_done: True

# ============================================================
# 8. GOVERNANCA E CONTRATOS
# ============================================================
governanca:
  contrato_ativo: "CONTRATO-GERACAO-RF-RL"
  ultimo_manifesto: null
  regras:
    - "RF e RL devem estar separados"
    - "RF não pode conter referências ao legado"
    - "RL deve ter 100% dos itens com destino definido"
    - "Validador deve passar antes de avançar para UC"

# ============================================================
# 9. OBSERVACOES GERAIS
# ============================================================
observacoes:
  - "RF/RL criados com sucesso."
  - "Próximo passo: Criar UC (CONTRATO-DOCUMENTACAO-ESSENCIAL)."

validacoes:
  rf_uc_cobertura_total: False
  uc_md_consistente: False
  uc_wf_consistente: False
  rf_yaml_sincronizado: True
  uc_yaml_sincronizado: False
```

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 RF.md deve conter APENAS contrato moderno (SEM legado)

**PROIBIDO em RFXXX.md:**
- ❌ Referências a telas ASPX
- ❌ Referências a webservices VB.NET
- ❌ Referências a stored procedures
- ❌ Código legado ou screenshots
- ❌ Comparações "legado vs moderno"

**OBRIGATÓRIO em RFXXX.md:**
- ✅ Mínimo 10 regras de negócio em linguagem natural
- ✅ 11 seções completas
- ✅ Integrações obrigatórias (i18n, auditoria, RBAC, Central)
- ✅ Endpoints REST API documentados
- ✅ Permissões RBAC definidas

### 7.2 RL.md deve conter TODA memória legado

**OBRIGATÓRIO em RL-RFXXX.md:**
- ✅ 9 seções completas
- ✅ Telas ASPX com caminho completo
- ✅ Webservices com métodos
- ✅ Stored Procedures com parâmetros
- ✅ Tabelas legadas com problemas identificados
- ✅ Regras implícitas extraídas
- ✅ Gap Analysis detalhado
- ✅ 100% dos itens com destino definido

### 7.3 Sincronização MD↔YAML obrigatória

- RFXXX.md ↔ RFXXX.yaml: 100% sincronizado
- RL-RFXXX.md ↔ RL-RFXXX.yaml: 100% sincronizado

### 7.4 Destinos obrigatórios (RL)

**Todo item em RL-RFXXX.yaml DEVE ter campo `destino` com um dos valores:**
- `assumido` - Regra/funcionalidade mantida no sistema moderno
- `substituido` - Regra/funcionalidade redesenhada/modernizada
- `descartado` - Regra/funcionalidade removida (não existe no moderno)
- `a_revisar` - Decisão ainda não tomada (temporário)

**PROIBIDO:**
- ❌ Item sem campo `destino`
- ❌ Campo `destino` vazio ou null
- ❌ Campo `destino` com valor inválido

### 7.5 Extração em Linguagem Natural (SEM código)

❌ **ERRADO:**
```vb
If txtEmail.Text.Contains("@") Then
    ValidEmail = True
End If
```

✅ **CORRETO:**
```markdown
### RN-RFXXX-01: Validação de Email
**Descrição:** Email deve conter o caractere "@"
**Justificativa:** Garantir formato válido de email
**Critério de Aceite:**
- Email sem "@" → rejeição
- Email é obrigatório para todos os usuários
```

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **Pasta do RF não existe**: RFXXX não encontrado na estrutura
2. **Templates inacessíveis**: `templates/` não disponível
3. **Legado inacessível**: `ic1_legado/` não disponível
4. **Validador falhou**: `validator-rl.py` retornou exit code ≠ 0
5. **Sincronização falhou**: MD e YAML não estão sincronizados
6. **Destinos incompletos**: Itens sem campo `destino` preenchido

---

### Fase 10: Atualização de documentacao-funcional.md (OBRIGATÓRIA)

#### 10.1 Atualizar Documentação Funcional Centralizada

Após criar os 4 arquivos (RF.md, RF.yaml, RL.md, RL.yaml) e validar com `validator-rl.py`, o agente DEVE:

1. **Abrir** o arquivo ` D:\IC2\rf\documentacao-funcional.md`
2. **Localizar** a seção do RFXXX (se já existir)
3. **Atualizar** ou **criar** a seção com as seguintes informações:

**Formato obrigatório da seção:**

```markdown
## RFXXX - [Título do Requisito Funcional]

**Fase:** Fase-X-Nome-da-Fase
**EPIC:** EPICXXX-YYY-ZZZ
**Status:** Documentado (RF/RL criados)
**Data Criação:** YYYY-MM-DD

### Resumo Executivo

[Resumo de 2-3 parágrafos extraído da Seção 1 do RF.md]

### Funcionalidades Principais

1. [Funcionalidade 1]
2. [Funcionalidade 2]
3. [Funcionalidade 3]
...

### Regras de Negócio Críticas

- **RN-RFXXX-01:** [Descrição resumida]
- **RN-RFXXX-02:** [Descrição resumida]
- **RN-RFXXX-03:** [Descrição resumida]
...

### Legado Mapeado

- **Telas ASPX:** [Quantidade] telas analisadas
- **Webservices:** [Quantidade] webservices mapeados
- **Stored Procedures:** [Quantidade] procedures documentadas
- **Bancos Legados:** [Quantidade] bancos multi-database mapeados

### Arquivos Gerados

- [RFXXX.md](./[Fase]/[EPIC]/RFXXX/RFXXX.md) - Requisito Funcional
- [RFXXX.yaml](./[Fase]/[EPIC]/RFXXX/RFXXX.yaml) - Estrutura canônica
- [RL-RFXXX.md](./[Fase]/[EPIC]/RFXXX/RL-RFXXX.md) - Referência ao Legado
- [RL-RFXXX.yaml](./[Fase]/[EPIC]/RFXXX/RL-RFXXX.yaml) - Rastreabilidade

### Estatísticas

- **Regras de Negócio:** [Total RNs] regras documentadas
- **Itens Legado Rastreados:** [Total itens RL] itens
- **Cobertura:** 100% do legado documentado
- **Validação:** validator-rl.py passou ✅

---
```

**Regras de atualização:**

- ✅ Se seção RFXXX já existe → **SUBSTITUIR** completamente (sobrescrever)
- ✅ Se seção RFXXX NÃO existe → **ADICIONAR** ao final do arquivo
- ✅ Manter ordem numérica dos RFs (RF001, RF002, RF003...)
- ✅ Links devem ser relativos a partir de ` D:\IC2\rf\`

**Critério de completude:**
- ✅ Seção RFXXX criada/atualizada no documentacao-funcional.md
- ✅ Links para os 4 arquivos funcionando
- ✅ Estatísticas preenchidas corretamente

---

### Fase 10: Finalização

Após atualizar o documentacao-funcional.md, a geração de documentação está concluída.

**Arquivos gerados:**

- RFXXX.md
- RFXXX.yaml
- RL-RFXXX.md
- RL-RFXXX.yaml
- STATUS.yaml (atualizado)
- documentacao-funcional.md (seção RFXXX atualizada)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

**Sugestão de mensagem de commit (para referência do usuário):**

```bash
git commit -m "docs(RFXXX): geração completa RF/RL

- RFXXX.md: Requisito Funcional (11 seções, [N] RNs)
- RFXXX.yaml: Estrutura canônica sincronizada
- RL-RFXXX.md: Referência ao Legado ([N] itens mapeados)
- RL-RFXXX.yaml: Rastreabilidade estruturada (100% destinos)
- STATUS.yaml: Governança atualizada
- documentacao-funcional.md: Seção RFXXX atualizada

Análise Legado:
- [N] Telas ASPX analisadas
- [N] Webservices mapeados
- [N] Stored Procedures documentadas
- [N] Bancos multi-database mapeados

Cobertura: 100% do legado documentado
Validação: validator-rl.py passou ✅
Rastreabilidade: Bidirecional completa (Legado ↔ RF ↔ UC)"
```

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Completude do Legado (100%)

- [ ] **Webservices:** TODOS os webservices do módulo analisados
- [ ] **Telas:** TODAS as telas ASPX do módulo analisadas
- [ ] **Bancos:** TODOS os bancos legados mapeados (multi-database)
- [ ] **Tabelas:** TODAS as tabelas relacionadas identificadas
- [ ] **Procedures:** TODAS as stored procedures analisadas
- [ ] **Views:** TODAS as views analisadas
- [ ] **Functions:** TODAS as UDFs analisadas
- [ ] **Triggers:** TODOS os triggers mapeados
- [ ] **Connection Strings:** TODAS as connection strings mapeadas
- [ ] **Configurações:** web.config analisado completamente

### 9.2 Checklist de Extração de Regras

- [ ] Regras extraídas em linguagem natural (mínimo 10)
- [ ] **NENHUMA** regra legada foi esquecida
- [ ] **TODAS** as validações do legado estão no RF
- [ ] **TODOS** os fluxos do legado estão cobertos por UCs
- [ ] **TODAS** as regras implícitas foram explicitadas

### 9.3 Checklist de Rastreabilidade Bidirecional

- [ ] **RF → RL:** Toda RN no RF tem origem no RL documentada
- [ ] **RL → RF:** Todo item no RL tem destino no RF/UC
- [ ] Matriz de rastreabilidade completa (Legado → RF → UC)
- [ ] Nenhum item no RL sem campo `rf_item_relacionado` preenchido

### 9.4 Checklist de Arquivos Gerados

- [ ] RFXXX.md criado (11 seções, mínimo 10 RNs, SEM legado)
- [ ] RFXXX.yaml criado (estruturado, sincronizado com RF.md)
- [ ] RL-RFXXX.md criado (9 seções, TODA memória legado, destinos definidos)
- [ ] RL-RFXXX.yaml criado (100% itens com campo destino preenchido)
- [ ] STATUS.yaml criado/atualizado
- [ ] **documentacao-funcional.md atualizado** (seção RFXXX criada/atualizada)

### 9.5 Checklist de Validação

- [ ] validator-rl.py executado (exit code 0)
- [ ] RFXXX.md ↔ RFXXX.yaml sincronizados 100%
- [ ] RL-RFXXX.md ↔ RL-RFXXX.yaml sincronizados 100%
- [ ] STATUS.yaml atualizado (documentacao.rf=True, rl=True, rf_yaml=True, rl_yaml=True)
- [ ] STATUS.yaml atualizado (separacao_rf_rl = all True)
- [ ] Estatísticas calculadas corretamente no STATUS.yaml

### 9.6 Checklist de Qualidade Final

- [ ] **Cobertura:** RF cobre 100% do legado (nenhuma funcionalidade esquecida)
- [ ] **Precisão:** RNs são 100% precisas (refletem exatamente o comportamento legado)
- [ ] **Rastreabilidade:** 100% dos itens têm origem/destino mapeado
- [ ] **Destinos:** 100% dos itens RL têm campo `destino` preenchido
- [ ] **Linguagem Natural:** NENHUM código VB.NET/SQL copiado
- [ ] **Multi-database:** TODOS os bancos legados mapeados no RL

**IMPORTANTE:** NÃO realizar commit. O usuário é responsável por commitar os arquivos.

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO-DOCUMENTACAO-ESSENCIAL** (para criar UC, MD, WF)
>
> ```
> Conforme CONTRATO DE DOCUMENTACAO-ESSENCIAL para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará os arquivos UC-RFXXX.md, MD-RFXXX.md, WF-RFXXX.md.

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/CONTRATO-GERACAO-RF-RL.md` | Este contrato |
| `contracts/CONTRATO-DOCUMENTACAO-ESSENCIAL.md` | Contrato para criar UC/MD/WF |
| `contracts/CONTRATO-RF-PARA-RL.md` | Contrato de migração RF v1.0 → v2.0 |
| `templates/RF.md` | Template do RF (contrato moderno) |
| `templates/RF.yaml` | Template RF estruturado |
| `templates/RL.md` | Template do RL (referência ao legado) |
| `templates/RL.yaml` | Template RL estruturado |
| `templates/STATUS.yaml` | Template STATUS estruturado |
| `tools/docs/validator-rl.py` | Validador de separação RF/RL |
| `/rf/documentacao-funcional.md` | **Documentação funcional centralizada (atualizada ao final)** |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-30 | Criação do contrato de geração RF/RL completo |

---

## 13. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

## 14. Workflow Resumido Visual

```
┌─────────────────────────────────────────────────────────────────┐
│ FASE 0: Consulta documentacao-funcional.md (OPCIONAL)          │
│ ├─ Ler  D:\IC2\rf\documentacao-funcional.md                │
│ ├─ Verificar se RFXXX já está documentado                      │
│ ├─ Usar como referência inicial (se existir)                   │
│ └─ SE NÃO EXISTIR → Fazer análise completa do legado           │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 1: Análise do Legado (100% COMPLETUDE)                    │
│ ├─ Identificar TODOS Webservices (.asmx)                       │
│ ├─ Analisar TODAS Telas ASPX (.aspx)                           │
│ ├─ Mapear TODOS Bancos (multi-database)                        │
│ ├─ Mapear TODAS Tabelas em TODOS os bancos                     │
│ ├─ Listar TODAS Stored Procedures                              │
│ ├─ Analisar TODAS Views, Functions, Triggers                   │
│ └─ Analisar web.config (connection strings)                    │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: Extração de Regras de Negócio                          │
│ ├─ Ler código VB.NET/C#                                        │
│ ├─ Identificar TODAS validações                                │
│ ├─ Extrair TODAS regras implícitas                             │
│ └─ Documentar 10-15 regras EM LINGUAGEM NATURAL                │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: Criar RFXXX.md (Contrato Moderno)                      │
│ ├─ 11 Seções obrigatórias                                      │
│ ├─ Mínimo 10 RNs em linguagem natural                          │
│ ├─ SEM referências ao legado                                   │
│ ├─ Integrações obrigatórias (i18n, auditoria, RBAC, Central)   │
│ └─ Rastreabilidade: Cada RN → origem no RL                     │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: Criar RFXXX.yaml (Estruturado)                         │
│ ├─ Sincronizado 100% com RFXXX.md                              │
│ ├─ Todas RNs, permissões, endpoints                            │
│ ├─ Campo origem_legado em cada RN                              │
│ └─ Formato canônico YAML                                       │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: Criar RL-RFXXX.md (Referência Legado)                  │
│ ├─ 9 Seções obrigatórias                                       │
│ ├─ TODA memória do legado                                      │
│ ├─ 100% itens com DESTINO definido                             │
│ ├─ Gap Analysis detalhado                                      │
│ └─ Rastreabilidade: Cada item → RN/UC no RF                    │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 6: Criar RL-RFXXX.yaml (Estruturado)                      │
│ ├─ Sincronizado 100% com RL-RFXXX.md                           │
│ ├─ Rastreabilidade de todos itens legado                       │
│ ├─ Campo "destino" obrigatório para cada item                  │
│ ├─ Campo "rf_item_relacionado" obrigatório                     │
│ └─ Metadados calculados                                        │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 7: Validação Obrigatória                                  │
│ ├─ Executar validator-rl.py RFXXX                              │
│ ├─ Verificar exit code = 0                                     │
│ ├─ Verificar rastreabilidade bidirecional                      │
│ ├─ Corrigir gaps se necessário                                 │
│ └─ Re-executar até passar                                      │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 8: Criar/Atualizar STATUS.yaml                            │
│ ├─ documentacao.rf = True                                      │
│ ├─ documentacao.rl = True                                      │
│ ├─ separacao_rf_rl = all True                                  │
│ └─ estatisticas preenchidas                                    │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 9: Atualizar documentacao-funcional.md (OBRIGATÓRIO)      │
│ ├─ Abrir  D:\IC2\rf\documentacao-funcional.md              │
│ ├─ Criar/Atualizar seção RFXXX                                 │
│ ├─ Incluir resumo, funcionalidades, RNs críticas               │
│ ├─ Incluir estatísticas (legado mapeado)                       │
│ └─ Links para os 4 arquivos gerados                            │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 10: Finalização                                           │
│ ├─ Documentação completa gerada                                │
│ ├─ STATUS.yaml atualizado                                      │
│ ├─ documentacao-funcional.md atualizado                        │
│ └─ Commit/push: Responsabilidade do usuário                    │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ CONCLUÍDO                                                       │
│ Arquivos criados:                                              │
│ 1. RFXXX.md                                                     │
│ 2. RFXXX.yaml                                                   │
│ 3. RL-RFXXX.md                                                  │
│ 4. RL-RFXXX.yaml                                                │
│ 5. STATUS.yaml (atualizado)                                    │
│ 6. documentacao-funcional.md (seção RFXXX atualizada)          │
│                                                                 │
│ ⚠️  Commit e push são responsabilidade do usuário              │
└─────────────────────────────────────────────────────────────────┘
```

---

---

## 15. Exemplo de Rastreabilidade Bidirecional Completa

### Cenário: Validação de CNPJ único por tenant

#### RL-RF060.yaml (Referência ao Legado)
```yaml
referencias:
  - id: "LEG-RF060-003"
    tipo: "stored_procedure"
    nome: "sp_ValidarCnpjUnico"
    caminho: "IControlIT_Cliente01/dbo.sp_ValidarCnpjUnico"
    descricao: |
      Stored procedure que verifica se um CNPJ já existe na base.
      Parâmetros:
        @Cnpj VARCHAR(18) - CNPJ a validar
        @EmpresaId INT - ID da empresa (opcional, para edição)
      Retorna:
        1 se CNPJ já existe
        0 se CNPJ disponível

      Lógica:
        SELECT COUNT(*)
        FROM Empresa
        WHERE Cnpj = @Cnpj
          AND (@EmpresaId IS NULL OR Id <> @EmpresaId)

    destino: "substituido"
    justificativa: |
      Substituído por validação no Application Layer (FluentValidation).
      Lógica movida para CreateEmpresaCommandValidator.
      Multi-tenancy adicionado (validação por ClienteId).

    rf_item_relacionado: "RN-RF060-05"
    uc_relacionado: "UC01"

    complexidade: "baixa"
    risco_migracao: "baixo"
    prioridade: 2
```

#### RF060.md (Requisito Funcional Moderno)
```markdown
### RN-RF060-05: CNPJ único por tenant

**Descrição:**
O CNPJ da empresa deve ser único dentro do mesmo tenant (ClienteId).
Empresas de tenants diferentes podem ter o mesmo CNPJ.

**Justificativa:**
Evitar duplicação de empresas no mesmo contexto organizacional,
permitindo multi-tenancy (mesma empresa pode existir em tenants diferentes).

**Critério de Aceite:**
- Tentativa de criar empresa com CNPJ duplicado no mesmo tenant → rejeição (HTTP 400)
- Tentativa de criar empresa com CNPJ duplicado em tenant diferente → permitido
- Validação deve considerar apenas CNPJ sem formatação (apenas números)
- Ao editar, deve ignorar o próprio registro

**Validação Backend:**
- FluentValidation: `CreateEmpresaCommandValidator`
- Query EF Core: `.Where(e => e.ClienteId == clienteId && e.Cnpj == cnpj)`

**Validação Frontend:**
- Async validator no formulário
- Chamada à API: `GET /api/empresas/validar-cnpj?cnpj={cnpj}`
- Feedback visual: mensagem de erro abaixo do campo

**Origem Legado:**
RL-RF060 (LEG-RF060-003 - Stored Procedure sp_ValidarCnpjUnico)
```

#### RF060.yaml (Estruturado)
```yaml
regras_negocio:
  - id: "RN-RF060-05"
    descricao: "CNPJ único por tenant"
    tipo: "unicidade"
    campos_afetados: ["Cnpj", "ClienteId"]
    obrigatorio: true
    validacao_backend:
      classe: "CreateEmpresaCommandValidator"
      metodo: "RuleFor(x => x.Cnpj).MustAsync(BeUniqueCnpj)"
    validacao_frontend:
      tipo: "async"
      endpoint: "GET /api/empresas/validar-cnpj"
    origem_legado:
      rl_id: "LEG-RF060-003"
      tipo: "stored_procedure"
      nome: "sp_ValidarCnpjUnico"
```

### Resultado da Rastreabilidade Bidirecional

```
LEGADO (RL-RF060.yaml)                    MODERNO (RF060.md/yaml)
═══════════════════════════════════       ═══════════════════════════

LEG-RF060-003                             RN-RF060-05
└─ Stored Procedure                       └─ Regra de Negócio
   sp_ValidarCnpjUnico          ────────►    "CNPJ único por tenant"
   ├─ Validação SQL                          ├─ FluentValidation (backend)
   ├─ Sem multi-tenancy                      ├─ Multi-tenancy (ClienteId)
   └─ Retorna 0/1                            └─ Async validator (frontend)

   DESTINO: substituido                      ORIGEM: LEG-RF060-003
   rf_item_relacionado: RN-RF060-05 ────────┘
```

**Benefícios desta rastreabilidade:**
1. ✅ Auditor consegue validar que stored procedure foi substituída
2. ✅ Desenvolvedor sabe qual lógica legada está implementando
3. ✅ Testador consegue comparar comportamento legado vs moderno
4. ✅ Nenhuma funcionalidade legada é perdida
5. ✅ Rastreabilidade em ambas as direções (legado→moderno, moderno→legado)

---

**FIM DO CONTRATO**

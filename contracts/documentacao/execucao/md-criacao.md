# CONTRATO DE GERAÇÃO MD (MODELO DE DADOS)

**Versão:** 1.0
**Data:** 2025-12-31
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **Modelo de Dados (MD) completo** com base no **Requisito Funcional (RF), Casos de Uso (UC) e Wireframes (WF)** já criados, garantindo:

- ✅ **Derivação Completa**: MD deriva do RF, UC e WF
- ✅ **Multi-tenancy**: Campos de isolamento por tenant
- ✅ **Auditoria Completa**: Created/Updated/Deleted tracking
- ✅ **Constraints**: PKs, FKs, UNIQUEs por tenant
- ✅ **Performance**: Índices para queries principais
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **MD-RFXXX.yaml** - Modelo de Dados (derivado do RF/UC/WF)
2. **STATUS.yaml** - Atualização de governança

✅ **UC e WF devem estar criados** (pré-requisito)
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Derivação**: MD deriva do RF (entidades), UC (operações) e WF (campos visíveis)
2. **Multi-tenancy**: TODAS as tabelas DEVEM ter `cliente_id` ou `empresa_id`
3. **Auditoria**: TODAS as tabelas DEVEM ter campos de auditoria completos
4. **Soft Delete**: TODAS as tabelas DEVEM ter `deleted_at`
5. **Constraints**: PKs, FKs e UNIQUEs obrigatórios
6. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA

**Se QUALQUER tabela não tiver multi-tenancy OU auditoria, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Modelo de Dados |
| **Escopo** | Criação completa de MD-RFXXX.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-MD para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-MD para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **1 arquivo fundamental** que complementa o RF/UC/WF com **modelo de dados**:

1. **MD-RFXXX.yaml** - Modelo de Dados (contrato estrutural)

Além disso, atualizar:

2. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Campos Obrigatórios em TODAS as Tabelas

**Multi-tenancy (1 campo, escolher conforme contexto):**
- `cliente_id` (GUID, FK para cliente) - Uso geral
- `empresa_id` (GUID, FK para empresa) - Uso em módulos específicos

**Auditoria completa (5 campos):**
- `created_at` (DATETIME, default GETDATE())
- `created_by` (GUID, FK para usuario, NULL permitido)
- `updated_at` (DATETIME, NULL permitido)
- `updated_by` (GUID, FK para usuario, NULL permitido)
- `deleted_at` (DATETIME, NULL permitido - soft delete)

**Chave primária:**
- `id` (GUID, PK, default NEWID())

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\rf\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\MD-RFXXX.yaml
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`
- Qualquer arquivo que não seja os 2 listados acima

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF | Pasta já criada em `rf/[Fase]/[EPIC]/RFXXX/` | Sim |
| RFXXX.yaml | RF criado e aprovado | Sim |
| UC-RFXXX.yaml | UC criado e completo | Sim |
| WF-RFXXX.yaml | WF criado e completo | Sim |
| Template MD.yaml | Template MD.yaml disponível | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| UC Validado | STATUS.yaml com `documentacao.uc = true` | Sim |
| WF Criado | STATUS.yaml com `documentacao.wf = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura de RF/UC/WF (OBRIGATÓRIA)

Antes de criar o modelo de dados, o agente DEVE:

#### 1.1 Ler RFXXX.yaml Completamente
- Localização: ` D:\IC2\rf\[Fase]\[EPIC]\RFXXX\RFXXX.yaml`
- Identificar TODAS as entidades principais
- Mapear relacionamentos (1:N, N:N)
- Entender regras de negócio que afetam o modelo

#### 1.2 Ler UC-RFXXX.yaml Completamente
- Localização: ` D:\IC2\rf\[Fase]\[EPIC]\RFXXX\UC-RFXXX.yaml`
- Identificar operações CRUD necessárias
- Mapear campos validados nos UCs
- Entender unicidades e constraints

#### 1.3 Ler WF-RFXXX.yaml Completamente
- Localização: ` D:\IC2\rf\[Fase]\[EPIC]\RFXXX\WF-RFXXX.yaml`
- Identificar campos visíveis na UI
- Mapear filtros e ordenações (índices necessários)
- Entender campos de busca

**Critério de completude:**
- ✅ RF.yaml lido integralmente
- ✅ UC.yaml lido integralmente
- ✅ WF.yaml lido integralmente
- ✅ Entidades identificadas
- ✅ Relacionamentos mapeados
- ✅ Campos identificados

---

### Fase 2: Criação MD-RFXXX.yaml (Modelo de Dados)

#### 2.1 Criar MD-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\MD.yaml`

**Estrutura obrigatória:**

```yaml
metadata:
  versao: "2.0"
  data: "YYYY-MM-DD"
  autor: "Agência ALC - alc.dev.br"

  rf_relacionado:
    id: "RFXXX"
    nome: "[Nome do RF]"

  sistema_modulo: "[Nome do Módulo]"
  banco_de_dados:
    engine: "logico"  # Modelo lógico (independente de engine física)
    schema: "logico"  # Abstração de schema
  padroes:
    multi_tenancy: true
    auditoria: true
    soft_delete: true

entidades:
  - nome: "[nome_entidade]"
    descricao: "[Descrição da entidade]"

    campos:
      # CHAVE PRIMÁRIA (OBRIGATÓRIO)
      - nome: "id"
        tipo: "GUID"
        nulo: false
        default: "NEWID()"
        descricao: "Chave primária"
        pk: true

      # MULTI-TENANCY (OBRIGATÓRIO - escolher cliente_id OU empresa_id)
      - nome: "cliente_id"
        tipo: "GUID"
        nulo: false
        descricao: "FK para clientes (multi-tenancy)"
        fk:
          tabela: "cliente"
          coluna: "id"
          on_delete: "CASCADE"
        index: true

      # CAMPOS DE NEGÓCIO (derivados do RF/UC/WF)
      - nome: "[campo_negocio]"
        tipo: "VARCHAR(200)"
        nulo: false
        default: null
        descricao: "[Descrição do campo]"
        unique_por_tenant: true  # Se for único por tenant
        index: true              # Se usado em filtros/buscas

      # AUDITORIA (OBRIGATÓRIO - 5 campos)
      - nome: "created_at"
        tipo: "DATETIME"
        nulo: true
        default: "GETDATE()"
        descricao: "Data de criação"
        audit: true

      - nome: "created_by"
        tipo: "GUID"
        nulo: true
        default: null
        descricao: "Usuário que criou"
        audit: true
        fk:
          tabela: "usuario"
          coluna: "id"
          on_delete: "SET NULL"

      - nome: "updated_at"
        tipo: "DATETIME"
        nulo: true
        default: null
        descricao: "Data de atualização"
        audit: true

      - nome: "updated_by"
        tipo: "GUID"
        nulo: true
        default: null
        descricao: "Usuário que atualizou"
        audit: true
        fk:
          tabela: "usuario"
          coluna: "id"
          on_delete: "SET NULL"

      # SOFT DELETE (OBRIGATÓRIO)
      - nome: "deleted_at"
        tipo: "DATETIME"
        nulo: true
        default: null
        descricao: "Soft delete"
        audit: true

    indices:
      # ÍNDICE PRIMÁRIO (OBRIGATÓRIO)
      - nome: "pk_[nome_entidade]"
        tipo: "PRIMARY"
        colunas: ["id"]
        descricao: "Chave primária"

      # ÍNDICE MULTI-TENANCY (OBRIGATÓRIO)
      - nome: "idx_[nome_entidade]_cliente"
        tipo: "BTREE"
        colunas: ["cliente_id"]
        descricao: "Performance multi-tenant"

      # ÍNDICES DE PERFORMANCE (conforme WF - filtros/buscas)
      - nome: "idx_[nome_entidade]_campo_busca"
        tipo: "BTREE"
        colunas: ["campo_busca"]
        descricao: "Performance em filtros"

    constraints:
      # FK MULTI-TENANCY (OBRIGATÓRIO)
      - nome: "fk_[nome_entidade]_cliente"
        tipo: "FOREIGN KEY"
        definicao: "cliente_id REFERENCES cliente(id)"
        on_delete: "CASCADE"
        descricao: "Multi-tenancy"

      # UNIQUE POR TENANT (se aplicável)
      - nome: "uq_[nome_entidade]_cliente_campo"
        tipo: "UNIQUE"
        definicao: "(cliente_id, [campo])"
        descricao: "Unicidade por tenant"

      # FKs DE AUDITORIA (OBRIGATÓRIO)
      - nome: "fk_[nome_entidade]_created_by"
        tipo: "FOREIGN KEY"
        definicao: "created_by REFERENCES usuario(id)"
        on_delete: "SET NULL"
        descricao: "Auditoria - criador"

      - nome: "fk_[nome_entidade]_updated_by"
        tipo: "FOREIGN KEY"
        definicao: "updated_by REFERENCES usuario(id)"
        on_delete: "SET NULL"
        descricao: "Auditoria - editor"

observacoes:
  - categoria: "Modelagem"
    descricao: "Derivado do RFXXX - Campos principais mapeados de UC/WF"

  - categoria: "Performance"
    descricao: "Índices criados para queries principais do UC00 (listagem)"

  - categoria: "Segurança"
    descricao: "Multi-tenancy e auditoria completa implementados"

historico:
  - versao: "2.0"
    data: "YYYY-MM-DD"
    autor: "Agência ALC - alc.dev.br"
    descricao: "Versão inicial derivada do RFXXX"
```

**OBRIGATÓRIO em MD-RFXXX.yaml:**
- ✅ Campos de multi-tenancy (`cliente_id` ou `empresa_id`)
- ✅ Campos de auditoria completa (5 campos)
- ✅ Soft delete (`deleted_at`)
- ✅ Constraints (PK, FKs, UNIQUE por tenant)
- ✅ Índices (PK + multi-tenancy + performance)
- ✅ Campos derivados do RF/UC/WF

**PROIBIDO em MD-RFXXX.yaml:**
- ❌ Tabelas sem multi-tenancy
- ❌ Tabelas sem auditoria completa
- ❌ Tabelas sem soft delete
- ❌ Campos sem descrição
- ❌ FKs sem `on_delete` definido

---

### Fase 3: Validação Estrutural

**⚠️ IMPORTANTE:** MD NÃO possui validador automático de código (como `validator-rf-uc.py` no UC).

A validação de MD é **estrutural**, realizada via **checklist** ([md.yaml](../../../checklists/documentacao/geracao/md.yaml)):

- ✅ Multi-tenancy em TODAS as tabelas (`cliente_id` ou `empresa_id`)
- ✅ Auditoria completa (5 campos) em TODAS as tabelas
- ✅ Soft delete (`deleted_at`) em TODAS as tabelas
- ✅ Constraints obrigatórias (PK, FKs, UNIQUEs)
- ✅ Índices de performance conforme WF

A validação é **manual/estrutural**, não automatizada.

---

### Fase 4: Atualização STATUS.yaml

#### 4.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar:**

```yaml
documentacao:
  md: true           # MD-RFXXX.yaml criado
```

**REGRA CRÍTICA:** Só marcar como `true` após criação completa do MD e validação estrutural via checklist.

---

### Fase 5: Finalização

Após atualizar STATUS.yaml, a geração de MD está concluída.

**Arquivos gerados:**
- MD-RFXXX.yaml
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 MD deve conter campos obrigatórios

**OBRIGATÓRIO em TODAS as tabelas:**
- ✅ `id` (GUID, PK)
- ✅ `cliente_id` OU `empresa_id` (multi-tenancy)
- ✅ `created_at` (auditoria)
- ✅ `created_by` (auditoria)
- ✅ `updated_at` (auditoria)
- ✅ `updated_by` (auditoria)
- ✅ `deleted_at` (soft delete)

**OBRIGATÓRIO em constraints:**
- ✅ PK constraint
- ✅ FK multi-tenancy (CASCADE)
- ✅ FKs auditoria (SET NULL)
- ✅ UNIQUE por tenant (se aplicável)

**OBRIGATÓRIO em índices:**
- ✅ Índice PK
- ✅ Índice multi-tenancy
- ✅ Índices de performance (conforme WF - filtros/buscas)

### 7.2 Coerência Estrutural Obrigatória

**Coerência RF → UC → WF → MD:**
- Entidades do MD derivam do RF
- Campos do MD cobrem operações dos UCs
- Índices do MD refletem filtros do WF

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **RFXXX.yaml não existe**: RF não foi criado
2. **UC-RFXXX.yaml não existe**: UCs não foram criados
3. **WF-RFXXX.yaml não existe**: WFs não foram criados
4. **Tabela sem multi-tenancy**: Qualquer tabela sem `cliente_id` ou `empresa_id`
5. **Tabela sem auditoria**: Qualquer tabela sem os 5 campos de auditoria
6. **Tabela sem soft delete**: Qualquer tabela sem `deleted_at`

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] MD-RFXXX.yaml criado (modelo de dados completo)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Qualidade Final

- [ ] **Multi-tenancy:** Todas as tabelas têm `cliente_id` ou `empresa_id`
- [ ] **Auditoria:** Todas as tabelas têm 5 campos de auditoria
- [ ] **Soft Delete:** Todas as tabelas têm `deleted_at`
- [ ] **Constraints:** PKs, FKs e UNIQUEs completos
- [ ] **Índices:** PK, multi-tenancy e performance
- [ ] **Derivação:** Campos derivam de RF/UC/WF
- [ ] **Rastreabilidade:** RF → UC → WF → MD completa
- [ ] **Arquivos prontos** (2 arquivos gerados)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, a documentação funcional completa está concluída (RF, UC, WF, MD).

O próximo passo é:

> **CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES** (para criar TC e MT)
>
> ```
> Conforme CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará os arquivos TC-RFXXX.yaml e MT-RFXXX.yaml para testes.

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/execucao/md-criacao.md` | Este contrato |
| `checklists/documentacao/geracao/md.yaml` | Checklist YAML |
| `templates/MD.yaml` | Template do MD |
| `templates/STATUS.yaml` | Template STATUS estruturado |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-31 | Criação do contrato separado (MD apenas) |

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

**FIM DO CONTRATO**

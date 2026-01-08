# CONTRATO DE GERAÇÃO UC/WF/MD COMPLETO

**Versão:** 1.0
**Data:** 2025-12-31
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **documentação funcional completa e rastreável** de Casos de Uso (UC), Wireframes (WF) e Modelo de Dados (MD) com base no **Requisito Funcional (RF)** já criado, garantindo:

- ✅ **Cobertura Total (100%)**: UC cobre 100% do RF
- ✅ **Rastreabilidade Completa**: RF → UC → WF → MD
- ✅ **Validação Automática**: validator-rf-uc.py obrigatório
- ✅ **Coerência Estrutural**: RF ↔ UC ↔ WF ↔ MD sempre consistentes
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados (Ordem Obrigatória)

1. **UC-RFXXX.md** - Casos de Uso (derivado do RF)
2. **UC-RFXXX.yaml** - Estrutura canônica dos UCs
3. **WF-RFXXX.md** - Wireframes (derivado dos UCs)
4. **MD-RFXXX.yaml** - Modelo de Dados (derivado do RF)
5. **STATUS.yaml** - Atualização de governança

✅ **Ordem obrigatória:** UC → WF → MD
✅ **Validação obrigatória** após UC criado
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Derivação do RF**: UC/WF/MD derivam EXCLUSIVAMENTE do RFXXX.yaml/md
2. **Cobertura Total**: UC cobre 100% das funcionalidades do RF
3. **Validação Bloqueante**: validator-rf-uc.py DEVE passar (exit code 0)
4. **Coerência Estrutural**: RF ↔ UC ↔ MD sempre consistentes
5. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA

**Se QUALQUER funcionalidade do RF não estiver coberta por UC, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Documentação UC/WF/MD |
| **Escopo** | Criação completa de UC-RFXXX.md, UC-RFXXX.yaml, WF-RFXXX.md, MD-RFXXX.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-UC-WF-MD para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-UC-WF-MD para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **4 arquivos fundamentais** que complementam o Requisito Funcional (RF) com **casos de uso, wireframes e modelo de dados**:

1. **UC-RFXXX.md** - Casos de Uso (contrato comportamental)
2. **UC-RFXXX.yaml** - Estrutura canônica dos UCs
3. **WF-RFXXX.md** - Wireframes (contrato visual)
4. **MD-RFXXX.yaml** - Modelo de Dados (contrato estrutural)

Além disso, atualizar:

5. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Cobertura Total (100%)

**REGRA CRÍTICA:** Os UCs DEVEM cobrir **100% ABSOLUTO** das funcionalidades do RF.

- ✅ TODA funcionalidade do RF DEVE estar presente em pelo menos um UC
- ✅ TODA regra de negócio do RF DEVE ser referenciada explicitamente em UC
- ✅ Nenhum UC pode introduzir comportamento NÃO previsto no RF
- ✅ Funcionalidades fora de escopo no RF NÃO geram UCs

**Se houver dúvida sobre alguma funcionalidade:**
- ❌ NÃO assumir que pode ser ignorada
- ❌ NÃO deixar de documentar
- ✅ Criar UC correspondente
- ✅ Validar contra RF com validator-rf-uc.py

### 3.2 Princípio da Rastreabilidade Completa

**REGRA CRÍTICA:** Cada UC DEVE apontar para funcionalidades do RF.

- ✅ Todo UC em UC-RFXXX.yaml DEVE ter campo `covers.rf_items` preenchido
- ✅ Toda RN-UC-XXX DEVE referenciar RN-RFXXX correspondente
- ✅ Criar matriz de rastreabilidade: RF → UC → TC

**Formato obrigatório de rastreabilidade:**

Em **UC-RFXXX.yaml**:
```yaml
casos_de_uso:
  - id: "UC01"
    nome: "Criar Entidade"
    covers:
      documentacao_items:
        - "RF-CRUD-01"  # Funcionalidade de criação no RF
        - "RF-VAL-01"   # Validação de campos obrigatórios
        - "RF-SEC-01"   # Permissão create
```

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\UC-RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\UC-RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\WF-RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\MD-RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\STATUS.yaml
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
| RFXXX.md | RF criado e aprovado | Sim |
| RFXXX.yaml | RF estruturado e sincronizado | Sim |
| Templates | Templates UC.md, UC.yaml, WF.md, MD.yaml disponíveis | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| RF Validado | STATUS.yaml com `documentacao.rf = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura do RF (OBRIGATÓRIA)

Antes de criar qualquer documento, o agente DEVE:

#### 1.1 Ler RFXXX.md Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\RFXXX.md`
- Entender TODAS as funcionalidades descritas
- Identificar TODAS as regras de negócio (RN-RFXXX-NNN)
- Mapear endpoints, permissões e integrações

#### 1.2 Ler RFXXX.yaml Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\RFXXX.yaml`
- Extrair catálogo de funcionalidades (`rf_items`)
- Mapear regras de negócio estruturadas
- Identificar entidades principais

**Critério de completude:**
- ✅ RF.md lido integralmente
- ✅ RF.yaml lido integralmente
- ✅ Funcionalidades mapeadas
- ✅ Regras de negócio identificadas

---

### Fase 2: Criação UC-RFXXX.md (Casos de Uso)

#### 2.1 Criar UC-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\UC.md`

**Estrutura obrigatória:**

1. **Seção 1: Objetivo do Documento**
   - Descrição do propósito dos UCs
   - Referência ao RF

2. **Seção 2: Sumário de Casos de Uso**
   - Tabela com todos os UCs (ID, Nome, Ator Principal)

3. **Seção 3: Padrões Gerais**
   - Isolamento por tenant
   - Permissões obrigatórias
   - Auditoria automática

4. **Seção 4+: Casos de Uso Detalhados**
   - UC00: Listar [Entidade]
   - UC01: Criar [Entidade]
   - UC02: Visualizar [Entidade]
   - UC03: Editar [Entidade]
   - UC04: Excluir [Entidade]

**Cada UC DEVE conter:**
- **Objetivo:** Descrição clara do propósito
- **Pré-condições:** Autenticação, permissões, estado inicial
- **Pós-condições:** Estado final esperado
- **Fluxo Principal:** Passos numerados (1, 2, 3...)
- **Fluxos Alternativos:** FA-XX-01, FA-XX-02...
- **Fluxos de Exceção:** FE-XX-01, FE-XX-02...
- **Regras de Negócio:** RN-UC-XX-NNN

**PROIBIDO em UC-RFXXX.md:**
- ❌ Copiar código do legado
- ❌ Criar funcionalidades não previstas no RF
- ❌ Omitir funcionalidades do RF

**OBRIGATÓRIO em UC-RFXXX.md:**
- ✅ Cobrir 100% do RF
- ✅ Quantidade de UCs necessária para cobrir 100% do RF (para RFs CRUD: padrão UC00-UC04)
- ✅ Todos os UCs com fluxos principais, alternativos e de exceção
- ✅ Regras de negócio rastreadas ao RF

---

### Fase 3: Criação UC-RFXXX.yaml (Estruturado)

#### 3.1 Criar UC-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\UC.yaml`

**Estrutura obrigatória:**

```yaml
uc:
  documentacao: "RFXXX"
  versao: "1.0"
  data: "YYYY-MM-DD"

casos_de_uso:
  - id: "UC00"
    nome: "Listar [Entidade]"
    ator_principal: "usuario_autenticado"

    covers:
      documentacao_items:
        - "RF-FUNCIONALIDADE-01"  # ID da funcionalidade no RFXXX.yaml
        - "RF-FUNCIONALIDADE-02"
      uc_items:
        - id: "UC00-FP-01"
          title: "Fluxo principal - listagem"
          required: true
        - id: "UC00-FA-01"
          title: "Filtrar por status"
          required: false
        - id: "UC00-FE-01"
          title: "Sem permissão view_any"
          required: true

    precondicoes:
      - permissao: "entidade.view_any"

    gatilho: "Usuario acessa funcionalidade pelo menu"

    fluxo_principal:
      - passo: 1
        ator: "usuario"
        acao: "acessa_menu"
      - passo: 2
        ator: "sistema"
        acao: "validar_permissao"
      - passo: 3
        ator: "sistema"
        acao: "listar_registros_tenant"
      - passo: 4
        ator: "sistema"
        acao: "exibir_lista"

    fluxos_alternativos:
      - id: "FA-UC00-01"
        condicao: "usuario_aplica_filtro"
        resultado: "lista_filtrada"

    fluxos_excecao:
      - id: "FE-UC00-01"
        condicao: "sem_permissao"
        resultado: "acesso_negado"

    regras_aplicadas:
      - "RN-RFXXX-01"

    resultado_final:
      estado: "lista_exibida"

  # Repetir para UC01, UC02, UC03, UC04...

exclusions:
  uc_items: []

historico:
  - versao: "1.0"
    data: "YYYY-MM-DD"
    autor: "Agência ALC - alc.dev.br"
    descricao: "Versão inicial"
```

**Regra CRÍTICA:** UC-RFXXX.yaml DEVE estar 100% sincronizado com UC-RFXXX.md
- Todos os UCs do MD devem estar no YAML
- Todos os fluxos do MD devem estar no YAML
- Campo `covers.rf_items` OBRIGATÓRIO para rastreabilidade

---

### Fase 4: Validação Obrigatória (BLOQUEANTE)

#### 4.1 Executar Validador de Cobertura RF→UC

```bash
python D:\IC2_Governanca\tools\docs\validator-rf-uc.py \
  --rf documentacao/[Fase]/[EPIC]/RFXXX/RFXXX.yaml \
  --uc documentacao/[Fase]/[EPIC]/RFXXX/UC-RFXXX.yaml
```

**IMPORTANTE:** O parâmetro `--tc` é **opcional** nesta fase, pois TC só será criado no próximo contrato (CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES). O validador deve funcionar sem TC.

**Critérios de validação:**
- ✅ UC cobre 100% das funcionalidades do RF
- ✅ UC-RFXXX.md ↔ UC-RFXXX.yaml sincronizados
- ✅ Nenhum UC introduz comportamento fora do RF
- ✅ Quantidade mínima de UCs para cobertura 100% (para RFs CRUD: UC00-UC04)

**Se validador falhar (exit code ≠ 0):**
- ❌ PARAR a execução
- ❌ NÃO atualizar STATUS.yaml
- ❌ Corrigir gaps identificados
- ✅ Re-executar validador até passar

---

### Fase 5: Criação WF-RFXXX.md (Wireframes)

#### 5.1 Criar WF-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\WF.md`

**Estrutura obrigatória:**

1. **Seção 1: Objetivo do Documento**
   - Propósito dos wireframes
   - Referência ao RF e UC

2. **Seção 2: Princípios de Design**
   - Princípios gerais (clareza, feedback, estados explícitos)
   - Padrões globais

3. **Seção 3: Mapa de Telas**
   - Tabela com todas as telas (ID, Tela, UCs Relacionados, Finalidade)

4. **Seções 4+: Wireframes Detalhados**
   - WF-01: Listagem (UC00)
   - WF-02: Criação (UC01)
   - WF-03: Edição (UC03)
   - WF-04: Visualização (UC02)
   - WF-05: Confirmação de Exclusão (UC04)

**Cada Wireframe DEVE conter:**
- **Intenção da Tela:** Propósito
- **Ações Permitidas:** Lista de ações do usuário
- **Estados Obrigatórios:** Loading, Vazio, Erro, Dados
- **Contratos de Comportamento:** Regras visuais e funcionais

**OBRIGATÓRIO em WF-RFXXX.md:**
- ✅ Cobertura de 100% dos UCs
- ✅ Estados obrigatórios (Loading, Vazio, Erro)
- ✅ Responsividade (Mobile, Tablet, Desktop)
- ✅ Acessibilidade (WCAG AA)

---

### Fase 6: Criação MD-RFXXX.yaml (Modelo de Dados)

#### 6.1 Criar MD-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\MD.yaml`

**Estrutura obrigatória:**

```yaml
metadata:
  versao: "2.0"
  data: "YYYY-MM-DD"
  autor: "Agência ALC - alc.dev.br"

  documentacao_relacionada:
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
      - nome: "id"
        tipo: "GUID"
        nulo: false
        default: "NEWID()"
        descricao: "Chave primária"
        pk: true

      # Multi-tenancy
      - nome: "cliente_id"
        tipo: "GUID"
        nulo: false
        descricao: "FK para clientes (multi-tenancy)"
        fk:
          tabela: "cliente"
          coluna: "id"
          on_delete: "CASCADE"
        index: true

      # Campos de negócio (derivados do RF)
      - nome: "[campo]"
        tipo: "VARCHAR(200)"
        nulo: false
        default: null
        descricao: "[Descrição do campo]"
        unique_por_tenant: true
        index: true

      # Auditoria
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

      # Soft delete
      - nome: "deleted_at"
        tipo: "DATETIME"
        nulo: true
        default: null
        descricao: "Soft delete"
        audit: true

    indices:
      - nome: "pk_[nome_entidade]"
        tipo: "PRIMARY"
        colunas: ["id"]
        descricao: "Chave primária"

      - nome: "idx_[nome_entidade]_cliente"
        tipo: "BTREE"
        colunas: ["cliente_id"]
        descricao: "Performance multi-tenant"

    constraints:
      - nome: "fk_[nome_entidade]_cliente"
        tipo: "FOREIGN KEY"
        definicao: "cliente_id REFERENCES cliente(id)"
        on_delete: "CASCADE"
        descricao: "Multi-tenancy"

      - nome: "uq_[nome_entidade]_cliente_campo"
        tipo: "UNIQUE"
        definicao: "(cliente_id, [campo])"
        descricao: "Unicidade por tenant"

observacoes:
  - categoria: "Modelagem"
    descricao: "Derivado do RFXXX - Campos principais mapeados"

  - categoria: "Performance"
    descricao: "Índices criados para queries principais do UC00"

  - categoria: "Segurança"
    descricao: "Multi-tenancy e auditoria completa"

historico:
  - versao: "2.0"
    data: "YYYY-MM-DD"
    autor: "Agência ALC - alc.dev.br"
    descricao: "Versão inicial derivada do RFXXX"
```

**OBRIGATÓRIO em MD-RFXXX.yaml:**
- ✅ Campos de multi-tenancy (cliente_id ou empresa_id)
- ✅ Campos de auditoria (created_at, created_by, updated_at, updated_by, deleted_at)
- ✅ Constraints (PK, FK, UNIQUE por tenant)
- ✅ Índices (performance em queries principais)

---

### Fase 7: Atualização STATUS.yaml

#### 7.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar:**

```yaml
documentacao:
  uc: true           # UC-RFXXX.md E UC-RFXXX.yaml criados
  wf: true           # WF-RFXXX.md criado
  md: true           # MD-RFXXX.yaml criado

validacoes:
  documentacao_uc_cobertura_total: true   # validator-rf-uc.py passou
  uc_yaml_sincronizado: true    # UC.md == UC.yaml
```

**REGRA CRÍTICA:** Só marcar como `true` após validação real do validador.

---

### Fase 8: Finalização

Após atualizar STATUS.yaml, a geração de documentação está concluída.

**Arquivos gerados:**
- UC-RFXXX.md
- UC-RFXXX.yaml
- WF-RFXXX.md
- MD-RFXXX.yaml
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 UC deve cobrir 100% do RF

**OBRIGATÓRIO em UC-RFXXX.md:**
- ✅ Quantidade de UCs necessária para cobrir 100% do RF (para RFs CRUD: padrão UC00-UC04)
- ✅ Cobertura de 100% das funcionalidades do RF
- ✅ Todos os UCs com fluxos principais, alternativos e de exceção
- ✅ Regras de negócio rastreadas ao RF

**PROIBIDO em UC-RFXXX.md:**
- ❌ Criar funcionalidades não previstas no RF
- ❌ Omitir funcionalidades do RF
- ❌ Copiar código

### 7.2 Coerência Estrutural Obrigatória

**Sincronização MD ↔ YAML:**
- UC-RFXXX.md ↔ UC-RFXXX.yaml: 100% sincronizado

**Coerência RF ↔ UC ↔ MD:**
- Todo item do RF deve estar coberto por UC
- Todo UC deve derivar de item do RF
- Todo MD deve refletir entidades do RF

### 7.3 WF deve cobrir 100% dos UCs

**OBRIGATÓRIO em WF-RFXXX.md:**
- ✅ Cobertura de 100% dos UCs
- ✅ Estados obrigatórios (Loading, Vazio, Erro, Dados)
- ✅ Responsividade (Mobile, Tablet, Desktop)
- ✅ Acessibilidade (WCAG AA)

### 7.4 MD deve conter

**OBRIGATÓRIO em MD-RFXXX.yaml:**
- ✅ Campos de multi-tenancy
- ✅ Campos de auditoria completa
- ✅ Constraints (PK, FK, UNIQUE por tenant)
- ✅ Índices para performance
- ✅ DDL derivado do RF

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **RFXXX.md não existe**: RF não foi criado
2. **RFXXX.yaml não existe**: RF estruturado não disponível
3. **Validador falhou**: `validator-rf-uc.py` retornou exit code ≠ 0
4. **Coerência falhou**: RF ↔ UC ↔ MD não estão consistentes
5. **Cobertura incompleta**: UC não cobre 100% do RF

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] UC-RFXXX.md criado (5 UCs com fluxos completos)
- [ ] UC-RFXXX.yaml criado (estruturado, sincronizado com UC.md)
- [ ] WF-RFXXX.md criado (wireframes cobrindo 100% dos UCs)
- [ ] MD-RFXXX.yaml criado (modelo de dados completo)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Validação

- [ ] validator-rf-uc.py executado (exit code 0)
- [ ] UC-RFXXX.md ↔ UC-RFXXX.yaml sincronizados 100%
- [ ] STATUS.yaml atualizado (documentacao.uc=true, wf=true, md=true)
- [ ] STATUS.yaml atualizado (validacoes.rf_uc_cobertura_total=true)

### 9.3 Checklist de Qualidade Final

- [ ] **Cobertura:** UC cobre 100% do RF
- [ ] **Validação:** validator-rf-uc.py passou
- [ ] **Rastreabilidade:** RF → UC → WF → MD completa
- [ ] **Coerência:** RF ↔ UC ↔ MD 100% consistentes
- [ ] **Sincronização:** UC.md ↔ UC.yaml 100%
- [ ] **Arquivos prontos** (5 arquivos gerados e validados)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES** (para criar TC)
>
> ```
> Conforme CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará os arquivos TC-RFXXX-*.md para testes.

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/CONTRATO-GERACAO-UC-WF-MD.md` | Este contrato |
| `checklists/checklist-geracao-uc-wf-md.yaml` | Checklist YAML |
| `templates/UC.md` | Template do UC |
| `templates/UC.yaml` | Template UC estruturado |
| `templates/WF.md` | Template do WF |
| `templates/MD.yaml` | Template do MD |
| `templates/STATUS.yaml` | Template STATUS estruturado |
| `tools/docs/validator-rf-uc.py` | Validador de cobertura RF→UC |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-31 | Criação do contrato de geração UC/WF/MD completo |

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
│ FASE 1: Leitura do RF (OBRIGATÓRIA)                            │
│ ├─ Ler RFXXX.md completamente                                  │
│ ├─ Ler RFXXX.yaml completamente                                │
│ ├─ Mapear funcionalidades                                      │
│ └─ Identificar regras de negócio                               │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 2: Criar UC-RFXXX.md                                      │
│ ├─ Seção 1: Objetivo do Documento                              │
│ ├─ Seção 2: Sumário de Casos de Uso                            │
│ ├─ Seção 3: Padrões Gerais                                     │
│ ├─ UC00: Listar                                                │
│ ├─ UC01: Criar                                                 │
│ ├─ UC02: Visualizar                                            │
│ ├─ UC03: Editar                                                │
│ └─ UC04: Excluir                                               │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 3: Criar UC-RFXXX.yaml                                    │
│ ├─ Sincronizado 100% com UC.md                                 │
│ ├─ Campo covers.rf_items obrigatório                           │
│ ├─ Rastreabilidade RF → UC                                     │
│ └─ Formato canônico YAML                                       │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 4: Validação Obrigatória (BLOQUEANTE)                     │
│ ├─ Executar validator-rf-uc.py RFXXX                           │
│ ├─ Verificar exit code = 0                                     │
│ ├─ Cobertura RF → UC = 100%                                    │
│ ├─ Corrigir gaps se necessário                                 │
│ └─ Re-executar até passar                                      │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 5: Criar WF-RFXXX.md                                      │
│ ├─ WF-01: Listagem (UC00)                                      │
│ ├─ WF-02: Criação (UC01)                                       │
│ ├─ WF-03: Edição (UC03)                                        │
│ ├─ WF-04: Visualização (UC02)                                  │
│ ├─ WF-05: Confirmação de Exclusão (UC04)                       │
│ └─ Estados obrigatórios (Loading, Vazio, Erro)                 │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 6: Criar MD-RFXXX.yaml                                    │
│ ├─ Metadados (RF, versão, autor)                               │
│ ├─ Entidades derivadas do RF                                   │
│ ├─ Campos (multi-tenancy, auditoria, soft-delete)              │
│ ├─ Índices (performance)                                       │
│ ├─ Constraints (PK, FK, UNIQUE por tenant)                     │
│ └─ Observações e histórico                                     │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 7: Atualizar STATUS.yaml                                  │
│ ├─ documentacao.uc = True                                      │
│ ├─ documentacao.wf = True                                      │
│ ├─ documentacao.md = True                                      │
│ ├─ validacoes.rf_uc_cobertura_total = True                     │
│ └─ validacoes.uc_yaml_sincronizado = True                      │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ FASE 8: Finalização                                            │
│ ├─ STATUS.yaml atualizado                                      │
│ ├─ Validação completa (validator-rf-uc.py passou)              │
│ └─ Arquivos prontos para commit (responsabilidade do usuário)  │
└─────────────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ CONCLUÍDO                                                       │
│ Arquivos gerados e validados:                                  │
│ 1. UC-RFXXX.md                                                  │
│ 2. UC-RFXXX.yaml                                                │
│ 3. WF-RFXXX.md                                                  │
│ 4. MD-RFXXX.yaml                                                │
│ 5. STATUS.yaml (atualizado)                                    │
│                                                                 │
│ ⚠️  Commit e push são responsabilidade do usuário              │
└─────────────────────────────────────────────────────────────────┘
```

---

**FIM DO CONTRATO**

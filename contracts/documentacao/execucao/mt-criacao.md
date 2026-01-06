# CONTRATO DE GERAÇÃO MT (MASSA DE TESTE)

**Versão:** 2.0
**Data:** 2025-12-31
**Status:** Ativo
**Changelog v2.0:** IDs canônicos, matriz rastreabilidade, cobertura mínima por categoria, negação de inferência, vínculo CA, validação bloqueante, STATUS.yaml ampliado

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **Massa de Teste (MT) completa** com base nos **Casos de Uso (UC)** já criados, garantindo:

- ✅ **Cobertura Total**: MT cobre 100% dos cenários de teste dos UCs
- ✅ **Rastreabilidade Completa**: UC → MT
- ✅ **Dados Reutilizáveis**: Massas organizadas por categoria (SUCESSO, VALIDACAO, SEGURANCA, etc.)
- ✅ **Independência de Plataforma**: Agnóstico de linguagem/framework
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **MT-RFXXX.yaml** - Massa de Teste (derivada dos UCs)
2. **STATUS.yaml** - Atualização de governança

✅ **UC deve estar criado e validado** (pré-requisito)
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Derivação dos UCs**: MT deriva EXCLUSIVAMENTE dos UCs criados
2. **Cobertura Total**: MT cobre 100% dos cenários de teste necessários
3. **Categorização Obrigatória**: SUCESSO, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO
4. **Rastreabilidade**: Cada MT DEVE referenciar UC correspondente
5. **Independência**: Agnóstico de plataforma e linguagem
6. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA

**Se QUALQUER cenário de UC não tiver massa de teste correspondente, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Massa de Teste |
| **Escopo** | Criação completa de MT-RFXXX.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-MT para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-MT para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **1 arquivo fundamental** que complementa os Casos de Uso (UC) com **massa de teste**:

1. **MT-RFXXX.yaml** - Massa de Teste (contrato de dados)

Além disso, atualizar:

2. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Cobertura Total (100%)

**REGRA CRÍTICA:** As Massas de Teste DEVEM cobrir **100% ABSOLUTO** dos cenários de UC.

- ✅ TODO cenário de teste (fluxo principal, alternativo e exceção) DEVE ter MT correspondente
- ✅ Nenhuma MT pode existir sem rastreabilidade ao UC
- ✅ Cenários fora de escopo nos UCs NÃO geram MTs

**Se houver dúvida sobre algum cenário:**
- ❌ NÃO assumir que pode ser ignorado
- ❌ NÃO deixar de documentar
- ✅ Criar MT correspondente ao cenário do UC

### 3.2 Categorização Obrigatória

**REGRA CRÍTICA:** Cada MT DEVE ter categoria clara.

Categorias obrigatórias:
- **SUCESSO**: Fluxos principais (happy path)
- **VALIDACAO**: Validações de campos (obrigatórios, formatos, ranges)
- **SEGURANCA**: Autenticação, autorização, multi-tenancy
- **EDGE_CASE**: Limites, casos extremos
- **AUDITORIA**: Campos de auditoria (created_by, updated_by, etc.)
- **INTEGRACAO**: Integridade referencial, FKs

### 3.3 Modelo Canônico de IDs Obrigatório (NOVO v2.0)

**REGRA CRÍTICA:** Todos os IDs de MT DEVEM seguir formato canônico.

**Formato obrigatório:**
```
MT-RFXXX-NNN
```

Onde:
- `MT-` = Prefixo fixo
- `RFXXX` = ID do RF (ex: RF060)
- `NNN` = Número sequencial de 3 dígitos (001, 002, etc.)

**Exemplos válidos:**
- ✅ `MT-RF060-001` (primeira MT do RF060)
- ✅ `MT-RF060-015` (décima quinta MT do RF060)

**Exemplos INVÁLIDOS:**
- ❌ `MT001` (falta RF)
- ❌ `MT-001` (falta RF)
- ❌ `MT-RF060-1` (falta zero à esquerda)

**Proibições absolutas:**
- ❌ IDs livres sem padrão
- ❌ IDs duplicados dentro do RF
- ❌ IDs fora do padrão canônico

**Validação obrigatória:**
- Checklist DEVE validar unicidade de IDs
- IDs duplicados = BLOQUEIO CRÍTICO
- IDs inválidos = BLOQUEIO CRÍTICO

### 3.4 Cobertura Mínima por Categoria (NOVO v2.0)

**REGRA CRÍTICA:** Categorias obrigatórias variam conforme tipo de UC.

**Para UCs do tipo CRUD (UC00-UC04):**

Categorias **OBRIGATÓRIAS**:
- ✅ SUCESSO (pelo menos 1 MT)
- ✅ VALIDACAO (pelo menos 1 MT)
- ✅ SEGURANCA (pelo menos 1 MT)
- ✅ AUDITORIA (pelo menos 1 MT - OBRIGATÓRIA para CRUD)
- ✅ MULTI_TENANCY (pelo menos 1 MT - OBRIGATÓRIA para CRUD)

Categorias **OPCIONAIS** (depende do RF):
- ⚪ EDGE_CASE
- ⚪ INTEGRACAO

**Para UCs do tipo Consulta/Relatório:**

Categorias **OBRIGATÓRIAS**:
- ✅ SUCESSO
- ✅ SEGURANCA
- ✅ MULTI_TENANCY

**Para UCs do tipo Integração/API:**

Categorias **OBRIGATÓRIAS**:
- ✅ SUCESSO
- ✅ VALIDACAO
- ✅ SEGURANCA
- ✅ INTEGRACAO

**Validação:**
- Checklist DEVE validar categoria × tipo de UC
- Categoria obrigatória ausente = BLOQUEIO CRÍTICO

### 3.5 Regra de Negação de Inferência (NOVO v2.0)

**REGRA CRÍTICA:** MT NÃO pode criar cenários não explicitados no UC.

**Princípio:**
> "Se o UC não explicita, a MT NÃO pode criar."

**Proibições absolutas:**
- ❌ Criar MT para validação não descrita no UC
- ❌ Criar MT para regra de negócio não documentada
- ❌ Criar MT para fluxo não mapeado
- ❌ Inferir comportamento "óbvio" não documentado

**Exceções permitidas:**
- ✅ Validações implícitas de tipo de dados (ex: GUID inválido)
- ✅ Segurança padrão (autenticação, autorização)
- ✅ Multi-tenancy (isolamento sempre obrigatório)
- ✅ Auditoria (sempre obrigatória)

**Efeito:**
- Inferência não permitida = REPROVAÇÃO AUTOMÁTICA
- MT com cenário não rastreável = BLOQUEIO CRÍTICO

### 3.6 Matriz de Rastreabilidade Formal RF → UC → MT (NOVO v2.0)

**REGRA CRÍTICA:** Todo MT.yaml DEVE conter seção `rastreabilidade`.

**Estrutura obrigatória:**

```yaml
rastreabilidade:
  rf_origem:
    id: "RFXXX"
    nome: "[Nome do RF]"

  mapeamento:
    - mt_id: "MT-RFXXX-001"
      uc_id: "UC01"
      uc_nome: "Criar Entidade"
      fluxo_id: "FP-UC01-001"
      fluxo_nome: "Fluxo principal de criação"
      rn_ids: ["RN-UC-01-001", "RN-UC-01-002"]
      ca_ids: ["CA-UC01-001"]

    - mt_id: "MT-RFXXX-002"
      uc_id: "UC01"
      uc_nome: "Criar Entidade"
      fluxo_id: "FE-UC01-001"
      fluxo_nome: "Campo obrigatório ausente"
      rn_ids: ["RN-UC-01-001"]
      ca_ids: ["CA-UC01-005"]
```

**Campos obrigatórios na matriz:**
- ✅ `rf_origem`: RF de origem
- ✅ `mt_id`: ID da MT
- ✅ `uc_id`: UC de origem
- ✅ `fluxo_id`: Fluxo (FP/FA/FE) de origem
- ✅ `rn_ids`: Regras de negócio aplicadas
- ✅ `ca_ids`: Critérios de aceite cobertos (quando existir)

**Validação:**
- Ausência da matriz = FALHA CRÍTICA
- MT sem rastreabilidade na matriz = BLOQUEIO
- Checklist DEVE validar matriz completa

### 3.7 Vínculo Explícito com Critérios de Aceite (NOVO v2.0)

**REGRA CRÍTICA:** Quando UC possuir Critérios de Aceite (CA), MT DEVE referenciar.

**Campo obrigatório em cada MT (quando CA existir):**

```yaml
MT-RF060-001:
  categoria: "SUCESSO"
  ca_ref: ["CA-UC01-001", "CA-UC01-002"]  # ← OBRIGATÓRIO quando CA existir
```

**Validação:**
- ✅ Toda CA DEVE gerar ao menos uma MT
- ✅ Checklist DEVE validar CA → MT
- ❌ CA sem MT correspondente = BLOQUEIO CRÍTICO

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
 D:\IC2\rf\Fase-*\EPIC*\RFXXX\MT-RFXXX.yaml
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
| UC-RFXXX.md | UC criado e completo | Sim |
| UC-RFXXX.yaml | UC estruturado e sincronizado | Sim |
| Template MT.yaml | Template MT.yaml disponível em `templates/` | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| UC Validado | STATUS.yaml com `documentacao.uc = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura dos UCs (OBRIGATÓRIA)

Antes de criar qualquer massa de teste, o agente DEVE:

#### 1.1 Ler UC-RFXXX.md Completamente
- Localização: ` D:\IC2\rf\[Fase]\[EPIC]\RFXXX\UC-RFXXX.md`
- Entender TODOS os casos de uso
- Identificar TODOS os fluxos (FP, FA, FE)
- Mapear regras de negócio validáveis

#### 1.2 Ler UC-RFXXX.yaml Completamente
- Localização: ` D:\IC2\rf\[Fase]\[EPIC]\RFXXX\UC-RFXXX.yaml`
- Extrair cenários de teste necessários
- Mapear validações de campos
- Identificar permissões e multi-tenancy

**Critério de completude:**
- ✅ UC.md lido integralmente
- ✅ UC.yaml lido integralmente
- ✅ Cenários de teste mapeados
- ✅ Validações identificadas

---

### Fase 2: Criação MT-RFXXX.yaml (Massa de Teste)

#### 2.1 Criar MT-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\MT.yaml`

**Estrutura obrigatória derivada do template:**

- **metadata**: versao, data, autor, rf_relacionado
- **defaults**: locale, timezone, currency, tenant_padrao, usuario_padrao, formatos
- **data_sets**: MT001-MT999 organizados por categoria
- **reusable_data**: usuarios, tenants
- **conventions**: placeholders
- **historico**: versões

**Categorias obrigatórias (conforme template):**
- MT001–MT099: SUCESSO
- MT100–MT199: VALIDACAO (campos obrigatórios, formatos)
- MT300–MT399: REGRAS DE NEGÓCIO
- MT400–MT499: AUTORIZAÇÃO/AUTENTICAÇÃO
- MT700–MT799: MULTI-TENANCY
- MT800–MT899: AUDITORIA

**OBRIGATÓRIO em cada MT:**
- ✅ `categoria`: Categoria clara
- ✅ `descricao`: Descrição do cenário
- ✅ `uc_ref`: Referência ao UC (ex: "UC01")
- ✅ `fluxo_ref`: Referência ao fluxo (ex: "FP-UC01-001", "FE-UC01-002")
- ✅ `rn_ref`: Referência à regra de negócio (quando aplicável)
- ✅ `contexto`: autenticacao, estado_inicial
- ✅ `entrada`: Dados enviados
- ✅ `resultado_esperado`: sucesso, http_status, resposta, banco

**Exemplo de MT derivada do template:**

```yaml
MT001:
  categoria: "SUCESSO"
  descricao: "Criação com dados válidos completos"
  uc_ref: "UC01"
  fluxo_ref: "FP-UC01-001"

  contexto:
    autenticacao:
      usuario_id: 1
      tenant_id: 1
      permissoes: ["entidade.create"]
    estado_inicial:
      banco:
        "entidade": []

  entrada:
    tenant_id: 1
    "campo1": "valor_valido"
    "campo2": 100

  resultado_esperado:
    sucesso: true
    http_status: 201
    resposta:
      contem:
        tenant_id: 1
        "campo1": "valor_valido"
      gerados:
        - id
        - created_at
        - created_by
    banco:
      "entidade":
        deve_existir:
          - tenant_id: 1
            "campo1": "valor_valido"
```

**PROIBIDO em MT-RFXXX.yaml:**
- ❌ Criar MT sem rastreabilidade ao UC
- ❌ Omitir categorização
- ❌ Criar valores "mágicos" sem explicação
- ❌ Criar MT órfã (sem referência futura em TC)

---

### Fase 3: Validação Estrutural (BLOQUEANTE - REFORMULADO v2.0)

**⚠️ IMPORTANTE:** Esta fase é **BLOQUEANTE** e **OBRIGATÓRIA**.

MT NÃO possui validador automático de código. A validação é **estrutural**, realizada via **checklist**.

#### 3.1 Executar Checklist de Validação

**Checklist:** [checklist-documentacao-mt.yaml](../../checklists/checklist-documentacao-mt.yaml)

**Validações obrigatórias:**

1. **IDs Canônicos:**
   - ✅ Todos IDs no formato `MT-RFXXX-NNN`
   - ✅ Nenhum ID duplicado
   - ✅ Nenhum ID inválido

2. **Cobertura:**
   - ✅ 100% dos fluxos (FP, FA, FE) cobertos
   - ✅ 100% dos UCs com MT correspondente
   - ✅ 100% dos CA (quando existir) com MT correspondente

3. **Categorização:**
   - ✅ Categorias obrigatórias por tipo de UC preenchidas
   - ✅ CRUD exige AUDITORIA + MULTI_TENANCY

4. **Rastreabilidade:**
   - ✅ Seção `rastreabilidade` presente
   - ✅ Matriz RF → UC → MT completa
   - ✅ Todos MT possuem `ca_ref` (quando CA existir)

5. **Campos Obrigatórios:**
   - ✅ contexto, entrada, resultado_esperado preenchidos

6. **Negação de Inferência:**
   - ✅ Nenhuma MT com cenário não explicitado no UC

#### 3.2 Critérios de Aprovação

Checklist é **APROVADO** APENAS se:

- ✅ **TODOS** os campos marcados como `true`
- ✅ Nenhum bloqueio crítico identificado
- ✅ Nenhuma inferência não permitida

#### 3.3 Em Caso de Reprovação

Se checklist REPROVAR:

- ❌ **PARAR** a execução
- ❌ **NÃO** atualizar STATUS.yaml
- ✅ Corrigir problemas identificados
- ✅ Re-executar checklist até aprovação

**BLOQUEIO:** STATUS.yaml **SÓ** pode ser atualizado após checklist aprovado.

---

### Fase 4: Atualização STATUS.yaml (AMPLIADO v2.0)

#### 4.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar (AMPLIADO v2.0):**

```yaml
documentacao:
  mt: true           # MT-RFXXX.yaml criado

validacao_mt:
  checklist_aprovado: true
  data_validacao: "YYYY-MM-DD HH:MM:SS"
  agente_executor: "agente-gerador-mt"
  tentativas: 1
  ids_canonicos_validos: true
  matriz_rastreabilidade_completa: true
  cobertura_ca_completa: true
  categorias_obrigatorias_atendidas: true
  negacao_inferencia_respeitada: true

historico_execucao_mt:
  - data: "YYYY-MM-DD HH:MM:SS"
    agente: "agente-gerador-mt"
    resultado: "aprovado"
    tentativa: 1
    observacoes: "Geração inicial completa"
```

**REGRA CRÍTICA:** Só marcar `documentacao.mt = true` após checklist aprovado.

---

### Fase 5: Finalização

Após atualizar STATUS.yaml, a geração de MTs está concluída.

**Arquivos gerados:**
- MT-RFXXX.yaml
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 MT deve cobrir 100% dos cenários de UC

**OBRIGATÓRIO em MT-RFXXX.yaml:**
- ✅ Cobertura de 100% dos fluxos (FP, FA, FE)
- ✅ Categorização completa (SUCESSO, VALIDACAO, SEGURANCA, EDGE_CASE, AUDITORIA, INTEGRACAO)
- ✅ Rastreabilidade UC → MT completa
- ✅ Campos obrigatórios preenchidos

**PROIBIDO em MT-RFXXX.yaml:**
- ❌ Criar MT sem rastreabilidade ao UC
- ❌ Omitir categorização
- ❌ Criar valores "mágicos" sem explicação

### 7.2 Coerência Estrutural Obrigatória

**Coerência UC → MT:**
- Todo fluxo de UC deve ter MT correspondente
- Toda MT deve derivar de UC existente
- Toda validação do UC deve ter MT de teste

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **UC-RFXXX.md não existe**: UCs não foram criados
2. **UC-RFXXX.yaml não existe**: UCs estruturados não disponíveis
3. **Cobertura incompleta**: MT não cobre 100% dos cenários de UC
4. **Categorização faltando**: Alguma MT sem categoria definida

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] MT-RFXXX.yaml criado (massa de teste cobrindo 100% dos UCs)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Qualidade Final

- [ ] **Cobertura:** MT cobre 100% dos cenários de UC
- [ ] **Categorização:** Todas as 6 categorias preenchidas
- [ ] **Rastreabilidade:** UC → MT completa
- [ ] **Campos obrigatórios:** contexto, entrada, resultado_esperado
- [ ] **Derivação:** MT deriva dos UCs
- [ ] **Arquivos prontos** (2 arquivos gerados)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO-GERACAO-DOCS-TC** (para criar TC)
>
> ```
> Conforme CONTRATO-GERACAO-DOCS-TC para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará o arquivo TC-RFXXX.yaml (Casos de Teste).

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/CONTRATO-GERACAO-DOCS-MT.md` | Este contrato |
| `checklists/checklist-documentacao-mt.yaml` | Checklist YAML |
| `templates/MT.yaml` | Template do MT |
| `templates/STATUS.yaml` | Template STATUS estruturado |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 2.0 | 2025-12-31 | **UPGRADE CRÍTICO:** IDs canônicos obrigatórios, matriz rastreabilidade formal, cobertura mínima por categoria, negação de inferência, vínculo CA obrigatório, validação bloqueante, STATUS.yaml ampliado |
| 1.0 | 2025-12-31 | Criação do contrato separado (MT antes de TC, MT depois de UC) |

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

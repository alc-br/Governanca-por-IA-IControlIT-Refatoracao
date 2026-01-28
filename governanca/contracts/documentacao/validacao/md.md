# VALIDADOR: Contrato de Validação MD (Modelo de Dados)

**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Claude Sonnet 4.5
**Propósito:** Validar se MD-RFXXX.yaml está 100% conforme após execução do contrato de geração

---

## CONTEXTO

Este validador executa **auditoria de conformidade** após a geração de MD, verificando se:
- MD.yaml deriva corretamente de RF/UC/WF
- MD.yaml possui multi-tenancy em TODAS as tabelas
- MD.yaml possui auditoria completa (5 campos) em TODAS as tabelas
- MD.yaml possui soft delete em TODAS as tabelas
- STATUS.yaml foi atualizado corretamente

---

## MODO DE OPERAÇÃO

**READ-ONLY:** Este validador NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

Se forem encontradas não-conformidades:
- Exibir relatório de gaps na tela
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas

**IMPORTANTE:**
- Relatório é exibido **APENAS NA TELA**
- NÃO salvar arquivos em .temp_ia/
- Gaps MENORES NÃO reprovam (apenas advertem)

---

## VALIDAÇÕES DE MODELO DE DADOS (MD)

### VALIDAÇÃO MD-1: Derivação de RF/UC/WF

**Objetivo:** Garantir que MD deriva corretamente das fontes.

**Verificações:**
- Entidades do MD mapeiam entidades do RF
- Campos do MD cobrem operações dos UCs
- Índices do MD refletem filtros do WF

**Método:**
```python
# Extrair entidades do RF
rf_entities = extract_entities_from_rf(rf_content)

# Extrair tabelas do MD
md_tables = extract_tables_from_md(md_content)

# Comparar
gaps = documentacao_entities - md_tables
```

**Critério de aprovação:**
- ✅ Todas as entidades do RF estão no MD
- ❌ Entidade não mapeada = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-1: APROVADO
   Entidades do RF: 3
   Tabelas no MD: 3
   Cobertura: 100%
```

---

### VALIDAÇÃO MD-2: Multi-tenancy Obrigatório

**Objetivo:** Garantir que TODAS as tabelas têm `cliente_id` ou `empresa_id`.

**Método:**
```python
for table in md_tables:
    campos = extract_campos(table)
    has_multi_tenancy = 'cliente_id' in campos or 'empresa_id' in campos
    if not has_multi_tenancy:
        gaps.append(f"Tabela {table['nome']}: Sem multi-tenancy")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm multi-tenancy
- ❌ Qualquer tabela sem multi-tenancy = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-2: APROVADO
   Tabelas: 3
   Com multi-tenancy: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-3: Auditoria Completa (5 campos)

**Objetivo:** Garantir que TODAS as tabelas têm campos de auditoria.

**Campos obrigatórios:**
- `created_at` (DATETIME, default GETDATE())
- `created_by` (GUID, FK para usuario, NULL)
- `updated_at` (DATETIME, NULL)
- `updated_by` (GUID, FK para usuario, NULL)
- `deleted_at` (DATETIME, NULL - soft delete)

**Método:**
```python
campos_auditoria = ['created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at']

for table in md_tables:
    campos = extract_campos(table)
    missing = set(campos_auditoria) - set(campos)
    if missing:
        gaps.append(f"Tabela {table['nome']}: Faltam {missing}")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm os 5 campos
- ❌ Qualquer tabela sem campo = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-3: APROVADO
   Tabelas: 3
   Com auditoria completa (5 campos): 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-4: Soft Delete Obrigatório

**Objetivo:** Garantir que TODAS as tabelas têm `deleted_at`.

**Método:**
```python
for table in md_tables:
    campos = extract_campos(table)
    if 'deleted_at' not in campos:
        gaps.append(f"Tabela {table['nome']}: Sem soft delete")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm `deleted_at`
- ❌ Qualquer tabela sem soft delete = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-4: APROVADO
   Tabelas: 3
   Com soft delete: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-5: Constraints Obrigatórias

**Objetivo:** Garantir que TODAS as tabelas têm constraints completas.

**Constraints obrigatórias:**
- PK constraint (id)
- FK multi-tenancy (CASCADE)
- FKs auditoria (SET NULL)
- UNIQUE por tenant (quando aplicável)

**Método:**
```python
for table in md_tables:
    constraints = extract_constraints(table)

    # Verificar PK
    if not has_pk_constraint(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem PK constraint")

    # Verificar FK multi-tenancy
    if not has_fk_multi_tenancy_cascade(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem FK multi-tenancy CASCADE")

    # Verificar FKs auditoria
    if not has_fk_auditoria_set_null(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem FKs auditoria SET NULL")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm constraints completas
- ❌ Qualquer constraint faltando = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-5: APROVADO
   Tabelas: 3
   Com constraints completas: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-6: Índices Obrigatórios

**Objetivo:** Garantir que TODAS as tabelas têm índices necessários.

**Índices obrigatórios:**
- Índice PK
- Índice multi-tenancy
- Índices de performance (conforme filtros do WF)

**Método:**
```python
for table in md_tables:
    indices = extract_indices(table)

    # Verificar índice PK
    if not has_pk_index(indices):
        gaps.append(f"Tabela {table['nome']}: Sem índice PK")

    # Verificar índice multi-tenancy
    if not has_multi_tenancy_index(indices):
        gaps.append(f"Tabela {table['nome']}: Sem índice multi-tenancy")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm índices obrigatórios
- ❌ Qualquer índice faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-6: APROVADO
   Tabelas: 3
   Com índices obrigatórios: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-7: MD.yaml Aderente ao Template

**Objetivo:** Garantir que MD.yaml segue a estrutura do template oficial.

**Verificações:**

1. **Cabeçalho completo:**
   ```yaml
   metadata:
     versao: "2.0"
     data: "YYYY-MM-DD"
     documentacao_relacionada:
       id: "RFXXX"
     padroes:
       multi_tenancy: true
       auditoria: true
       soft_delete: true
   ```

2. **Estrutura de cada entidade:**
   - `nome`, `descricao` presentes
   - `campos` com todos os campos obrigatórios
   - `indices` presentes
   - `constraints` presentes

3. **Seções finais:**
   - `observacoes` presente
   - `historico` presente com pelo menos 1 versão

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-7: APROVADO
   Template: MD.yaml 100% aderente ao v2.0
   Seções obrigatórias: 8/8 presentes
```

---

### VALIDAÇÃO MD-8: STATUS.yaml Atualizado

**Objetivo:** Verificar se STATUS.yaml foi atualizado corretamente.

**Campos esperados:**
```yaml
documentacao:
  md: true
```

**Critério de aprovação:**
- ✅ `documentacao.md = true`
- ❌ Campo ausente ou `false` = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-8: APROVADO
   STATUS.yaml: documentacao.md = true
```

---

## RELATÓRIO DE VALIDAÇÃO (APENAS TELA)

**Template de saída:**

```markdown
# VALIDAÇÃO MD-RFXXX

**Data:** YYYY-MM-DD
**Validador:** VALIDADOR-MD v2.0

---

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Derivação RF/UC/WF | ✅ PASS | CRÍTICO | 3/3 (100%) |
| 2 | Multi-tenancy | ✅ PASS | CRÍTICO | 3/3 (100%) |
| 3 | Auditoria completa | ✅ PASS | CRÍTICO | 5/5 campos em todos |
| 4 | Soft delete | ✅ PASS | CRÍTICO | 3/3 (100%) |
| 5 | Constraints | ✅ PASS | CRÍTICO | 3/3 (100%) |
| 6 | Índices | ✅ PASS | IMPORTANTE | 3/3 (100%) |
| 7 | MD.yaml → Template | ✅ PASS | IMPORTANTE | 8/8 seções |
| 8 | STATUS.yaml | ✅ PASS | IMPORTANTE | md=true |

**PONTUAÇÃO FINAL:** 8/8 PASS (100%)

**VEREDICTO:** ✅ **APROVADO** - MD-RFXXX está 100% conforme (ZERO GAPS CRÍTICOS/IMPORTANTES)

---

## GAPS IDENTIFICADOS

**Nenhum gap CRÍTICO ou IMPORTANTE identificado.** ✅

---

## RECOMENDAÇÕES

Nenhuma ação corretiva necessária. RFXXX pode prosseguir para criação de TC/MT.
```

---

## CRITÉRIOS DE APROVAÇÃO/REPROVAÇÃO v3.0

### ✅ APROVADO

**Exigências:**
- ✅ Todas as 8 validações PASS
- ✅ ZERO gaps CRÍTICOS
- ✅ ZERO gaps IMPORTANTES
- ✅ Gaps MENORES são permitidos (apenas advertência)

---

### ✅ APROVADO COM ADVERTÊNCIA

**Exigências:**
- ✅ Todas as 8 validações PASS
- ✅ ZERO gaps CRÍTICOS
- ✅ ZERO gaps IMPORTANTES
- ⚠️ Gaps MENORES presentes (mas não bloqueiam)

---

### ❌ REPROVADO

**Motivos de REPROVAÇÃO:**
- ❌ 7/8 ou menos validações PASS
- ❌ **QUALQUER gap CRÍTICO** (ex: tabela sem multi-tenancy)
- ❌ **QUALQUER gap IMPORTANTE** (ex: tabela sem índice)

---

## MODO DE EXECUÇÃO

**Prompt de ativação:**
```
Executar VALIDADOR-MD para RFXXX.
Seguir D:\IC2\CLAUDE.md.
```

**Comportamento esperado:**
1. Leitura de MD-RFXXX.yaml, UC-RFXXX.yaml, RF-RFXXX.yaml, STATUS.yaml
2. Execução das 8 validações
3. Geração de relatório na tela (NÃO salvar arquivo)
4. Veredicto final: APROVADO, APROVADO COM ADVERTÊNCIA ou REPROVADO

**IMPORTANTE:**
- Este validador NÃO corrige problemas, apenas IDENTIFICA
- Relatório exibido APENAS NA TELA (não salvar em arquivo)

---

---

## Git Operations (SOMENTE SE APROVADO 100% SEM RESSALVAS)

**Versão:** 1.0
**Data:** 2026-01-28

### Regra Fundamental

**SE E SOMENTE SE:**
1. ✅ Validação passou **100%** (8/8 PASS)
2. ✅ **ZERO** gaps CRÍTICOS ou IMPORTANTES
3. ✅ Branch atual **NÃO** é `dev`

**ENTÃO:** Executar Git Operations automaticamente.

### Sequência Obrigatória

```bash
# 1. Verificar branch atual
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" == "dev" ]; then
    echo "✅ Já está em dev. Sem necessidade de merge."
    exit 0
fi

# 2. Verificar se há alterações pendentes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Alterações pendentes detectadas. Commitando..."

    # 3. Adicionar TODAS as alterações
    git add .

    # 4. Criar commit
    git commit -m "docs(RFXXX): MD validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): MD validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. MD mergeado em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer gap CRÍTICO ou IMPORTANTE
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**Fim do Validador**

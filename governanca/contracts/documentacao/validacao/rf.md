# CONTRATO DE VALIDAÇÃO RF (REQUISITO FUNCIONAL)

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato valida **Requisito Funcional (RF)** criado, garantindo:

- ✅ **11 Seções Completas**: Todas as seções obrigatórias presentes
- ✅ **Mínimo 10 Regras de Negócio**: Documentação adequada
- ✅ **Integrações Obrigatórias**: i18n, auditoria, RBAC, Central
- ✅ **Sem Referências Legado**: RF limpo (ASPX, WebServices, SQL)
- ✅ **Sincronização MD ↔ YAML**: 100% consistência
- ✅ **Validador Automático**: validator-docs.py executado

### 🎯 Validações Executadas

**Total:** 15 validações obrigatórias

1. **RF-1:** 11 seções completas em RF.md
2. **RF-2:** Mínimo 10 regras de negócio
3. **RF-3:** Integrações obrigatórias completas (i18n, auditoria, RBAC, Central)
4. **RF-4:** Sem referências a legado (ASPX, WebServices, SQL)
5. **RF-5:** Catálogo de funcionalidades completo (RF-CRUD, RF-VAL, RF-SEC)
6. **RF-6:** Matriz RBAC documentada
7. **RF-7:** Endpoints da API documentados
8. **RF-8:** Modelo de dados descrito
9. **RF-9:** RF.yaml segue template v1.0
10. **RF-10:** Sincronização RF.md ↔ RF.yaml (100%)
11. **RF-11:** i18n: chaves de tradução definidas
12. **RF-12:** Auditoria: 5 campos obrigatórios
13. **RF-13:** RBAC: escopo definido
14. **RF-14:** Central: cadastro definido
15. **RF-15:** validator-docs.py passou (exit code 0)

### 📊 Critério de Aprovação

- ✅ **APROVADO:** 15/15 validações PASS + ZERO gaps
- ❌ **REPROVADO:** Qualquer validação FAIL OU qualquer gap

**NÃO EXISTE APROVAÇÃO COM RESSALVAS.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Validador de Requisito Funcional |
| **Escopo** | Validação completa de RFXXX.md e RFXXX.yaml |
| **Modo** | READ-ONLY (não corrige, apenas identifica e reporta) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme contracts/documentacao/validacao/rf.md para RFXXX"**

Exemplo:
```
Conforme contracts/documentacao/validacao/rf.md para RF070.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Executar **15 validações obrigatórias** sobre RF criado, garantindo:

1. Estrutura completa (11 seções)
2. Conteúdo adequado (mínimo 10 RNs)
3. Integrações obrigatórias (i18n, auditoria, RBAC, Central)
4. Sem referências a legado
5. Sincronização MD ↔ YAML (100%)

**IMPORTANTE:** Este contrato é READ-ONLY. NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

---

## 4. Validações Obrigatórias

### VALIDAÇÃO RF-1: 11 Seções Completas em RF.md

**Seções obrigatórias:**

1. Seção 1: Objetivo
2. Seção 2: Escopo
3. Seção 3: Conceitos de Negócio
4. Seção 4: Funcionalidades
5. Seção 5: Regras de Negócio
6. Seção 6: Estados e Transições
7. Seção 7: Permissões (RBAC)
8. Seção 8: Endpoints da API
9. Seção 9: Modelo de Dados
10. Seção 10: Dependências
11. Seção 11: Integrações Obrigatórias

**Verificação:**
```python
secoes_obrigatorias = [
    "## 1. Objetivo",
    "## 2. Escopo",
    "## 3. Conceitos de Negócio",
    "## 4. Funcionalidades",
    "## 5. Regras de Negócio",
    "## 6. Estados e Transições",
    "## 7. Permissões (RBAC)",
    "## 8. Endpoints da API",
    "## 9. Modelo de Dados",
    "## 10. Dependências",
    "## 11. Integrações Obrigatórias"
]

for secao in secoes_obrigatorias:
    if secao not in documentacao_md_content:
        GAP(f"Seção faltando: {secao}")
```

**Resultado:**
- ✅ PASS: Todas as 11 seções presentes
- ❌ FAIL: Qualquer seção faltando

---

### VALIDAÇÃO RF-2: Mínimo 10 Regras de Negócio

**Critério:**

Seção 5 (Regras de Negócio) DEVE conter pelo menos 10 regras (RN-MOD-XXX-01, RN-MOD-XXX-02, ..., RN-MOD-XXX-10).

**Verificação:**
```python
import re

# Contar RNs em RF.md
rns_md = re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_md_content)

# Contar RNs em RF.yaml
rns_yaml = len(rf_yaml['regras_negocio'])

if len(rns_md) < 10:
    GAP(f"Apenas {len(rns_md)} regras encontradas (mínimo: 10)")

if rns_yaml < 10:
    GAP(f"Apenas {rns_yaml} regras em YAML (mínimo: 10)")
```

**Resultado:**
- ✅ PASS: >= 10 regras de negócio
- ❌ FAIL: < 10 regras de negócio

---

### VALIDAÇÃO RF-3: Integrações Obrigatórias Completas

**Critério:**

Seção 11 (Integrações Obrigatórias) DEVE documentar TODAS as 4 integrações:

1. **11.1: i18n (Internacionalização)**
2. **11.2: Auditoria**
3. **11.3: RBAC (Permissões)**
4. **11.4: Central de Funcionalidades**

**Verificação:**
```python
integracoes_obrigatorias = [
    "### 11.1. i18n (Internacionalização)",
    "### 11.2. Auditoria",
    "### 11.3. RBAC (Permissões)",
    "### 11.4. Central de Funcionalidades"
]

for integracao in integracoes_obrigatorias:
    if integracao not in documentacao_md_content:
        GAP(f"Integração faltando: {integracao}")
```

**Resultado:**
- ✅ PASS: Todas as 4 integrações presentes
- ❌ FAIL: Qualquer integração faltando

---

### VALIDAÇÃO RF-4: Sem Referências a Legado

**Critério:**

RF.md NÃO DEVE conter referências a:
- Telas ASPX (.aspx)
- WebServices legado (.asmx, .svc)
- Stored Procedures legado (sp_, usp_, fn_, etc)
- Código VB.NET/SQL copiado

**Verificação:**
```python
referencias_legado = [
    ".aspx",
    ".asmx",
    ".svc",
    "sp_",
    "usp_",
    "fn_",
    "WebService",
    "VB.NET",
    "SqlCommand",
    "DataSet",
    "DataTable"
]

for ref in referencias_legado:
    if ref in documentacao_md_content:
        GAP(f"Referência a legado encontrada: {ref}")
```

**Resultado:**
- ✅ PASS: SEM referências a legado
- ❌ FAIL: Qualquer referência a legado

---

### VALIDAÇÃO RF-5: Catálogo de Funcionalidades Completo

**Critério:**

Seção 4 (Funcionalidades) DEVE conter catálogo completo conforme tipo de RF:

- **crud:** RF-CRUD-01 a RF-CRUD-05, RF-VAL-01, RF-VAL-02, RF-SEC-01, RF-SEC-02
- **leitura:** RF-READ-01, RF-READ-02, RF-VAL-01, RF-SEC-01, RF-SEC-02
- **integracao:** RF-INT-01, RF-INT-02, RF-VAL-01, RF-SEC-01, RF-SEC-02
- **batch:** RF-BATCH-01, RF-BATCH-02, RF-VAL-01, RF-SEC-01, RF-SEC-02

**Verificação:**
```python
tipo_rf = documentacao_yaml['rf']['tipo_rf']

if tipo_rf == "crud":
    funcionalidades_esperadas = [
        "RF-CRUD-01",  # Criar
        "RF-CRUD-02",  # Listar
        "RF-CRUD-03",  # Visualizar
        "RF-CRUD-04",  # Atualizar
        "RF-CRUD-05",  # Excluir
        "RF-VAL-01",   # Validar campos
        "RF-VAL-02",   # Validar unicidade
        "RF-SEC-01",   # Isolamento tenant
        "RF-SEC-02"    # Permissões RBAC
    ]

    for func in funcionalidades_esperadas:
        if func not in documentacao_md_content:
            GAP(f"Funcionalidade faltando: {func}")
```

**Resultado:**
- ✅ PASS: Catálogo completo conforme tipo
- ❌ FAIL: Qualquer funcionalidade faltando

---

### VALIDAÇÃO RF-6: Matriz RBAC Documentada

**Critério:**

Seção 7 (Permissões RBAC) DEVE conter matriz completa:

- `entidade.view_any` - Listar registros
- `entidade.view` - Visualizar registro
- `entidade.create` - Criar registro
- `entidade.update` - Atualizar registro
- `entidade.delete` - Excluir registro

**Verificação:**
```python
permissoes_esperadas = [
    ".view_any",
    ".view",
    ".create",
    ".update",
    ".delete"
]

for perm in permissoes_esperadas:
    if perm not in documentacao_md_content:
        GAP(f"Permissão faltando: {perm}")
```

**Resultado:**
- ✅ PASS: Todas as permissões presentes
- ❌ FAIL: Qualquer permissão faltando

---

### VALIDAÇÃO RF-7: Endpoints da API Documentados

**Critério:**

Seção 8 (Endpoints da API) DEVE documentar endpoints conforme tipo de RF:

- **crud:** GET (list), GET (by id), POST, PUT, DELETE
- **leitura:** GET (list), GET (by id)
- **integracao:** POST (enviar), GET (consultar status)
- **batch:** POST (iniciar), GET (status), GET (resultado)

**Verificação:**
```python
tipo_rf = documentacao_yaml['rf']['tipo_rf']

if tipo_rf == "crud":
    endpoints_esperados = [
        "GET /api/entidades",
        "GET /api/entidades/{id}",
        "POST /api/entidades",
        "PUT /api/entidades/{id}",
        "DELETE /api/entidades/{id}"
    ]

    for endpoint in endpoints_esperados:
        if endpoint not in documentacao_md_content:
            GAP(f"Endpoint faltando: {endpoint}")
```

**Resultado:**
- ✅ PASS: Todos os endpoints presentes
- ❌ FAIL: Qualquer endpoint faltando

---

### VALIDAÇÃO RF-8: Modelo de Dados Descrito

**Critério:**

Seção 9 (Modelo de Dados) DEVE descrever:

- Entidades principais (pelo menos 1)
- Campos obrigatórios
- Multi-tenancy (cliente_id ou empresa_id)
- Auditoria (5 campos: created_at, created_by, updated_at, updated_by, deleted_at)
- Soft delete (deleted_at)

**Verificação:**
```python
campos_obrigatorios = [
    "cliente_id",  # OU empresa_id
    "created_at",
    "created_by",
    "updated_at",
    "updated_by",
    "deleted_at"
]

for campo in campos_obrigatorios:
    if campo not in documentacao_md_content and "empresa_id" not in documentacao_md_content:
        GAP(f"Campo obrigatório faltando: {campo}")
```

**Resultado:**
- ✅ PASS: Modelo de dados completo
- ❌ FAIL: Qualquer campo obrigatório faltando

---

### VALIDAÇÃO RF-9: RF.yaml Segue Template v1.0

**Critério:**

RFXXX.yaml DEVE conter TODOS os campos obrigatórios do template:

```yaml
rf:
  id: RFXXX
  nome: "..."
  versao: "1.0"
  data: "YYYY-MM-DD"
  fase: "..."
  epic: "..."
  status: "draft"
  tipo_rf: "crud"

descricao:
  objetivo: "..."
  problema_resolvido: "..."
  publico_afetado: "..."

escopo:
  incluso: [...]
  fora: [...]

entidades: [...]
regras_negocio: [...]
estados: [...]
transicoes: [...]
permissoes: [...]
integracoes: {...}
seguranca: {...}
rastreabilidade: {...}
catalog: {...}
```

**Verificação:**
```python
campos_obrigatorios = [
    "rf",
    "descricao",
    "escopo",
    "entidades",
    "regras_negocio",
    "estados",
    "transicoes",
    "permissoes",
    "integracoes",
    "seguranca",
    "rastreabilidade",
    "catalog"
]

for campo in campos_obrigatorios:
    if campo not in documentacao_yaml:
        GAP(f"Campo faltando em YAML: {campo}")
```

**Resultado:**
- ✅ PASS: Todos os campos presentes
- ❌ FAIL: Qualquer campo faltando

---

### VALIDAÇÃO RF-10: Sincronização RF.md ↔ RF.yaml (100%)

**Critério:**

TODAS as regras de negócio em RF.md DEVEM estar em RF.yaml e vice-versa.

**Verificação:**
```python
# RNs em MD
rns_md = set(re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_md_content))

# RNs em YAML
rns_yaml = set([rn['id'] for rn in documentacao_yaml['regras_negocio']])

# Gaps
rns_md_only = rns_md - rns_yaml
rns_yaml_only = rns_yaml - rns_md

if rns_md_only:
    GAP(f"RNs em MD mas não em YAML: {rns_md_only}")

if rns_yaml_only:
    GAP(f"RNs em YAML mas não em MD: {rns_yaml_only}")
```

**Resultado:**
- ✅ PASS: 100% sincronização
- ❌ FAIL: Qualquer gap de sincronização

---

### VALIDAÇÃO RF-11: i18n - Chaves de Tradução Definidas

**Critério:**

Seção 11.1 (i18n) DEVE listar chaves de tradução:

- `rf.xxx.campo`
- `rf.xxx.validacao.erro`
- Idiomas: pt-BR, en-US, es-ES

**Verificação:**
```python
if "rf." not in documentacao_md_content:
    GAP("Chaves i18n (rf.xxx) não documentadas")

if "pt-BR" not in documentacao_md_content or "en-US" not in documentacao_md_content or "es-ES" not in documentacao_md_content:
    GAP("Idiomas incompletos (esperado: pt-BR, en-US, es-ES)")
```

**Resultado:**
- ✅ PASS: Chaves definidas e idiomas completos
- ❌ FAIL: Chaves ou idiomas faltando

---

### VALIDAÇÃO RF-12: Auditoria - 5 Campos Obrigatórios

**Critério:**

Seção 11.2 (Auditoria) DEVE listar 5 campos:

1. `created_at`
2. `created_by`
3. `updated_at`
4. `updated_by`
5. `deleted_at` (soft delete)

**Verificação:**
```python
campos_auditoria = [
    "created_at",
    "created_by",
    "updated_at",
    "updated_by",
    "deleted_at"
]

for campo in campos_auditoria:
    if campo not in documentacao_md_content:
        GAP(f"Campo de auditoria faltando: {campo}")
```

**Resultado:**
- ✅ PASS: 5 campos presentes
- ❌ FAIL: Qualquer campo faltando

---

### VALIDAÇÃO RF-13: RBAC - Escopo Definido

**Critério:**

Seção 11.3 (RBAC) DEVE definir escopo:

- Developer (escopo = 3)
- Sistema (escopo = 2)
- Cliente (escopo = 1)
- Fornecedor (escopo = 0)

**Verificação:**
```python
if "escopo" not in documentacao_md_content and "Developer" not in documentacao_md_content:
    GAP("Escopo RBAC não documentado")
```

**Resultado:**
- ✅ PASS: Escopo definido
- ❌ FAIL: Escopo não definido

---

### VALIDAÇÃO RF-14: Central - Cadastro Definido

**Critério:**

Seção 11.4 (Central de Funcionalidades) DEVE definir:

- Ícone
- Ordem
- Menu pai
- Permissões associadas

**Verificação:**
```python
central_campos = ["Ícone", "Ordem", "Menu pai", "Permissões"]

for campo in central_campos:
    if campo not in documentacao_md_content:
        GAP(f"Central - campo faltando: {campo}")
```

**Resultado:**
- ✅ PASS: Cadastro completo
- ❌ FAIL: Qualquer campo faltando

---

### VALIDAÇÃO RF-15: validator-docs.py Passou (Exit Code 0)

**Critério:**

Executar validador automático:

```bash
python tools/docs/validator-docs.py RFXXX
```

**Verificação:**
```python
exit_code = executar("python tools/docs/validator-docs.py {rf}")

if exit_code != 0:
    GAP("Validador automático reprovou (exit code != 0)")
```

**Resultado:**
- ✅ PASS: Exit code = 0
- ❌ FAIL: Exit code ≠ 0

---

## 5. Relatório Opcional (Recomendado)

**OPCIONAL:** Gerar relatório em `.temp_ia/validacao-rf-RFXXX-relatorio.md` para auditoria posterior.

**IMPORTANTE:** Ausência de relatório **NÃO reprova** validação. Foco está em conformidade técnica.

```markdown
# RELATÓRIO DE VALIDAÇÃO - RFXXX

## RESUMO EXECUTIVO

| Validação | Resultado |
|-----------|-----------|
| RF-1: 11 Seções Completas | ✅ PASS |
| RF-2: Mínimo 10 RNs | ✅ PASS |
| RF-3: Integrações Obrigatórias | ❌ FAIL |
| ... | ... |
| RF-15: Validador Automático | ✅ PASS |

**Taxa de Aprovação:** 14/15 (93.3%)

## GAPS IDENTIFICADOS

### GAP: RF-3 - Integração "Central de Funcionalidades" faltando

**Severidade:** CRÍTICO

**Descrição:** Seção 11.4 (Central de Funcionalidades) não encontrada em RF.md

**Localização:** RF070.md - Seção 11

**Ação Corretiva:** Adicionar Seção 11.4 com:
- Ícone da funcionalidade
- Ordem no menu
- Menu pai
- Permissões associadas

---

## VEREDICTO FINAL

❌ **REPROVADO**

- 14/15 validações PASS (93.3%)
- 1 gap CRÍTICO identificado

**Próxima Ação:**
Corrigir gap RF-3 e revalidar.
```

---

## 6. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/validacao/rf.md` | Este contrato |
| `prompts/documentacao/validacao/rf.md` | Prompt de ativação |
| `checklists/documentacao/geracao/rf.yaml` | Checklist de validação |
| `templates/RF.md` | Template RF Markdown |
| `templates/RF.yaml` | Template RF YAML |
| `tools/docs/validator-docs.py` | Validador automático |

---

## 7. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2026-01-03 | Criação do contrato de validação de RF |

---

## 8. Git Operations (SOMENTE SE APROVADO 100% SEM RESSALVAS)

**Versão:** 1.0
**Data:** 2026-01-28

### Regra Fundamental

**SE E SOMENTE SE:**
1. ✅ Validação passou **100%** (15/15 PASS)
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
    git commit -m "docs(RFXXX): RF validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): RF validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. RF mergeado em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer gap CRÍTICO ou IMPORTANTE
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**FIM DO CONTRATO**

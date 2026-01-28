# VALIDADOR: Contrato de Validação WF (Wireframes)

**Versão:** 3.0
**Data:** 2026-01-04
**Autor:** Claude Sonnet 4.5
**Propósito:** Validar se WF-RFXXX.md está 100% conforme após execução do contrato de geração

---

## CONTEXTO

Este validador executa **auditoria de conformidade** após a geração de WF, verificando se:
- WF.md cobre 100% dos UCs
- WF.md possui estados obrigatórios (Loading, Vazio, Erro, Dados)
- WF.md documenta responsividade (Mobile, Tablet, Desktop)
- WF.md documenta acessibilidade (WCAG AA)
- STATUS.yaml foi atualizado corretamente

**⚠️ IMPORTANTE:** WF é apenas formato NARRATIVO (WF.md). NÃO existe WF.yaml.

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

## VALIDAÇÕES DE WIREFRAMES (WF)

### VALIDAÇÃO WF-1: Arquivo WF.md Existe

**Objetivo:** Garantir que WF-RFXXX.md foi criado.

**Método:**
```python
import os

wf_path = f"rf/Fase-X/EPICX/RFXXX/WF-RFXXX.md"
exists = os.path.exists(wf_path)
```

**Critério de aprovação:**
- ✅ WF-RFXXX.md existe
- ❌ Arquivo ausente = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO WF-1: APROVADO
   WF-RFXXX.md: EXISTS (X bytes)
```

---

### VALIDAÇÃO WF-2: Cobertura UC → WF (100% Obrigatória)

**Objetivo:** Garantir que TODOS os UCs têm representação visual em WF.

**Método:**
```python
# Extrair IDs de UCs do UC.yaml
uc_ids = set(re.findall(r'- id: "(UC\d+)"', uc_content))

# Extrair UCs referenciados no WF.md (seções WF-XX)
wf_sections = re.findall(r'## WF-\d+.*?\(UC(\d+)\)', wf_md_content)
wf_ucs = set([f"UC{uc}" for uc in wf_sections])

# Calcular gaps
gaps = uc_ids - wf_ucs
cobertura = len(wf_ucs) / len(uc_ids) * 100 if uc_ids else 0
```

**Critério de aprovação:**
- ✅ `cobertura == 100%` AND `len(gaps) == 0`
- ❌ Qualquer gap = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO WF-2: APROVADO
   Cobertura: 13/13 UCs (100%)
   Gaps: 0
```

---

### VALIDAÇÃO WF-3: Estados Obrigatórios (Loading, Vazio, Erro, Dados)

**Objetivo:** Garantir que TODOS os wireframes possuem os 4 estados obrigatórios documentados.

**Método:**
```python
estados_obrigatorios = ["Loading", "Vazio", "Erro", "Dados"]

# Extrair wireframes do WF.md
wireframes = re.findall(r'## WF-(\d+):(.*?)(?=## WF-|\Z)', wf_md_content, re.DOTALL)

for wf_id, wf_content in wireframes:
    # Verificar se possui seção "Estados Obrigatórios"
    if "### 3. Estados Obrigatórios" not in wf_content:
        gaps.append(f"WF-{wf_id}: Seção 'Estados Obrigatórios' ausente")
        continue

    # Verificar cada estado
    for estado in estados_obrigatorios:
        if f"#### Estado" not in wf_content or estado not in wf_content:
            gaps.append(f"WF-{wf_id}: Falta estado '{estado}'")
```

**Critério de aprovação:**
- ✅ TODOS os WFs têm os 4 estados documentados
- ❌ Qualquer WF sem estado = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-3: APROVADO
   Wireframes: 5
   Estados obrigatórios: 4/4 em todos os WFs
   Violações: 0
```

---

### VALIDAÇÃO WF-4: Responsividade Documentada (Mobile, Tablet, Desktop)

**Objetivo:** Garantir que TODOS os wireframes documentam responsividade.

**Método:**
```python
dispositivos_obrigatorios = ["Mobile", "Tablet", "Desktop"]

for wf_id, wf_content in wireframes:
    # Verificar se possui seção "Responsividade"
    if "#### Responsividade" not in wf_content:
        gaps.append(f"WF-{wf_id}: Seção 'Responsividade' ausente")
        continue

    # Verificar cada dispositivo
    for dispositivo in dispositivos_obrigatorios:
        if f"**{dispositivo}:" not in wf_content:
            gaps.append(f"WF-{wf_id}: Falta dispositivo '{dispositivo}'")
```

**Critério de aprovação:**
- ✅ TODOS os WFs documentam os 3 dispositivos
- ❌ Qualquer WF sem dispositivo = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-4: APROVADO
   Wireframes: 5
   Dispositivos: Mobile, Tablet, Desktop documentados em todos
   Violações: 0
```

---

### VALIDAÇÃO WF-5: Acessibilidade WCAG AA

**Objetivo:** Garantir que acessibilidade está documentada.

**Critérios verificados:**
- Labels em português claro
- Navegação por teclado
- Contraste mínimo WCAG AA
- ARIA labels (quando aplicável)

**Método:**
```python
for wf_id, wf_content in wireframes:
    # Verificar se possui seção "Acessibilidade"
    if "#### Acessibilidade" not in wf_content:
        gaps.append(f"WF-{wf_id}: Seção 'Acessibilidade (WCAG AA)' ausente")
        continue

    # Verificar critérios mínimos
    if "Labels em português" not in wf_content:
        gaps.append(f"WF-{wf_id}: Falta critério 'Labels em português'")
    if "Navegação por teclado" not in wf_content:
        gaps.append(f"WF-{wf_id}: Falta critério 'Navegação por teclado'")
    if "Contraste" not in wf_content or "4.5:1" not in wf_content:
        gaps.append(f"WF-{wf_id}: Falta critério 'Contraste mínimo 4.5:1'")
```

**Critério de aprovação:**
- ✅ TODOS os WFs documentam acessibilidade
- ❌ Qualquer WF sem acessibilidade = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-5: APROVADO
   Wireframes: 5
   Critérios WCAG AA: 3/3 documentados em todos
   Violações: 0
```

---

### VALIDAÇÃO WF-6: Seções Obrigatórias do Documento

**Objetivo:** Garantir que WF.md possui todas as seções obrigatórias.

**Seções obrigatórias do documento:**
1. **Objetivo do Documento**
2. **Princípios de Design**
3. **Mapa de Telas**
4. **Wireframes Detalhados** (WF-01 até WF-NN)
5. **Responsividade** (globalmente)
6. **Acessibilidade** (globalmente)
7. **Rastreabilidade**

**Método:**
```python
secoes_obrigatorias = [
    "## 1. OBJETIVO DO DOCUMENTO",
    "## 2. PRINCÍPIOS DE DESIGN",
    "## 3. MAPA DE TELAS",
    "## 10. RESPONSIVIDADE",
    "## 11. ACESSIBILIDADE",
    "## 12. RASTREABILIDADE"
]

for secao in secoes_obrigatorias:
    if secao not in wf_md_content:
        gaps.append(f"Seção ausente: {secao}")
```

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-6: APROVADO
   Seções obrigatórias: 7/7 presentes
   Violações: 0
```

---

### VALIDAÇÃO WF-7: Mapa de Telas Completo

**Objetivo:** Garantir que a seção "Mapa de Telas" lista TODAS as telas.

**Método:**
```python
# Extrair wireframes do documento
wireframes_doc = re.findall(r'## WF-(\d+)', wf_md_content)

# Extrair linhas da tabela "Mapa de Telas"
mapa_section = re.search(r'## 3\. MAPA DE TELAS(.*?)(?=##|\Z)', wf_md_content, re.DOTALL)
if mapa_section:
    mapa_content = mapa_section.group(1)
    wireframes_mapa = re.findall(r'\| WF-(\d+)', mapa_content)
else:
    gaps.append("Seção 'Mapa de Telas' ausente")
    wireframes_mapa = []

# Verificar cobertura
missing_in_mapa = set(wireframes_doc) - set(wireframes_mapa)
if missing_in_mapa:
    gaps.append(f"Wireframes não listados no Mapa de Telas: {missing_in_mapa}")
```

**Critério de aprovação:**
- ✅ Todos os wireframes listados no Mapa de Telas
- ❌ Qualquer wireframe faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-7: APROVADO
   Wireframes documentados: 5
   Wireframes no Mapa de Telas: 5/5 (100%)
   Violações: 0
```

---

### VALIDAÇÃO WF-8: Rastreabilidade UC ↔ WF

**Objetivo:** Garantir que a seção "Rastreabilidade" mapeia corretamente UC ↔ WF.

**Método:**
```python
# Extrair tabela de rastreabilidade
rastro_section = re.search(r'## 12\. RASTREABILIDADE(.*?)(?=##|\Z)', wf_md_content, re.DOTALL)
if rastro_section:
    rastro_content = rastro_section.group(1)
    rastro_lines = re.findall(r'\| (WF-\d+) \| (UC\d+) \| (RFXXX)', rastro_content)
else:
    gaps.append("Seção 'Rastreabilidade' ausente")
    rastro_lines = []

# Verificar se todos os wireframes estão rastreados
wireframes_doc = set(re.findall(r'WF-(\d+)', wf_md_content))
wireframes_rastro = set([wf.split('-')[1] for wf, uc, documentacao in rastro_lines])

missing_rastro = wireframes_doc - wireframes_rastro
if missing_rastro:
    gaps.append(f"Wireframes sem rastreabilidade: WF-{missing_rastro}")
```

**Critério de aprovação:**
- ✅ Todos os wireframes rastreados
- ❌ Qualquer wireframe sem rastreabilidade = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-8: APROVADO
   Wireframes: 5
   Wireframes rastreados: 5/5 (100%)
   Violações: 0
```

---

### VALIDAÇÃO WF-9: STATUS.yaml Atualizado

**Objetivo:** Verificar se STATUS.yaml foi atualizado corretamente.

**Campos esperados:**
```yaml
documentacao:
  wf: true
```

**Critério de aprovação:**
- ✅ `documentacao.wf = true`
- ❌ Campo ausente ou `false` = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-9: APROVADO
   STATUS.yaml: documentacao.wf = true
```

---

## RELATÓRIO DE VALIDAÇÃO (APENAS TELA)

**Template de saída:**

```markdown
# VALIDAÇÃO WF-RFXXX

**Data:** YYYY-MM-DD
**Validador:** VALIDADOR-WF v3.0

---

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Arquivo WF.md existe | ✅ PASS | CRÍTICO | EXISTS (X bytes) |
| 2 | Cobertura UC → WF | ✅ PASS | CRÍTICO | 13/13 (100%) |
| 3 | Estados obrigatórios | ✅ PASS | CRÍTICO | 4/4 em todos |
| 4 | Responsividade | ✅ PASS | IMPORTANTE | 3/3 em todos |
| 5 | Acessibilidade WCAG AA | ✅ PASS | IMPORTANTE | 3/3 em todos |
| 6 | Seções obrigatórias | ✅ PASS | IMPORTANTE | 7/7 presentes |
| 7 | Mapa de Telas completo | ✅ PASS | IMPORTANTE | 5/5 (100%) |
| 8 | Rastreabilidade UC ↔ WF | ✅ PASS | IMPORTANTE | 5/5 (100%) |
| 9 | STATUS.yaml | ✅ PASS | IMPORTANTE | wf=true |

**PONTUAÇÃO FINAL:** 9/9 PASS (100%)

**VEREDICTO:** ✅ **APROVADO** - WF-RFXXX está 100% conforme (ZERO GAPS CRÍTICOS/IMPORTANTES)

---

## GAPS IDENTIFICADOS

**Nenhum gap CRÍTICO ou IMPORTANTE identificado.** ✅

---

## RECOMENDAÇÕES

Nenhuma ação corretiva necessária. RFXXX pode prosseguir para criação de MD.
```

---

## CRITÉRIOS DE APROVAÇÃO/REPROVAÇÃO v3.0

### ✅ APROVADO

**Exigências:**
- ✅ Todas as 9 validações PASS
- ✅ ZERO gaps CRÍTICOS
- ✅ ZERO gaps IMPORTANTES
- ✅ Gaps MENORES são permitidos (apenas advertem)

---

### ✅ APROVADO COM ADVERTÊNCIA

**Exigências:**
- ✅ Todas as 9 validações PASS
- ✅ ZERO gaps CRÍTICOS
- ✅ ZERO gaps IMPORTANTES
- ⚠️ Gaps MENORES presentes (mas não bloqueiam)

---

### ❌ REPROVADO

**Motivos de REPROVAÇÃO:**
- ❌ 8/9 ou menos validações PASS
- ❌ **QUALQUER gap CRÍTICO** (ex: WF.md ausente, UC sem WF, WF sem estados)
- ❌ **QUALQUER gap IMPORTANTE** (ex: WF sem responsividade)

---

## MODO DE EXECUÇÃO

**Prompt de ativação:**
```
Executar VALIDADOR-WF para RFXXX.
Seguir D:\IC2\CLAUDE.md.
```

**Comportamento esperado:**
1. Leitura de WF-RFXXX.md, UC-RFXXX.yaml, STATUS.yaml
2. Execução das 9 validações
3. Geração de relatório na tela (NÃO salvar arquivo)
4. Veredicto final: APROVADO, APROVADO COM ADVERTÊNCIA ou REPROVADO

**IMPORTANTE:**
- Este validador NÃO corrige problemas, apenas IDENTIFICA
- Relatório exibido APENAS NA TELA (não salvar em arquivo)
- WF é apenas formato NARRATIVO (WF.md) - NÃO existe WF.yaml

---

## Git Operations (SOMENTE SE APROVADO 100% SEM RESSALVAS)

**Versão:** 1.0
**Data:** 2026-01-28

### Regra Fundamental

**SE E SOMENTE SE:**
1. ✅ Validação passou **100%** (9/9 PASS)
2. ✅ **ZERO** gaps CRÍTICOS ou IMPORTANTES
3. ✅ Branch atual **NÃO** é `dev`

**ENTÃO:** Executar Git Operations automaticamente.

**NOTA:** APROVADO COM ADVERTÊNCIA (gaps MENORES) **PODE** prosseguir com Git Operations.

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
    git commit -m "docs(RFXXX): WF validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): WF validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. WF mergeado em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer gap CRÍTICO
- ❌ Qualquer gap IMPORTANTE
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**Fim do Validador**

# CONTRATO DE VALIDAÇÃO — ADITIVO (Evolução Incremental de RF)

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato **valida que um ADITIVO foi aplicado corretamente** a um RF existente, garantindo:

- ✅ **Backups Criados**: Versões `_old` de todos os documentos existem
- ✅ **Delta Rastreável**: Mudanças entre original e `_old` identificadas
- ✅ **Cobertura Completa**: Nova funcionalidade propagada em cascata (RF → UC → WF → MD → MT → TC)
- ✅ **Sincronização 100%**: .md ↔ .yaml em todos os níveis
- ✅ **Aprovação Rigorosa**: Zero tolerância a gaps (100% ou REPROVADO)

### 📁 Arquivos Validados

**Backups (_old):**
1. `RFXXX_old.md`, `RFXXX_old.yaml`
2. `UC-RFXXX_old.md`, `UC-RFXXX_old.yaml`
3. `WF-RFXXX_old.md`, `WF-RFXXX_old.yaml`
4. `MD-RFXXX_old.md`, `MD-RFXXX_old.yaml`
5. `MT-RFXXX_old.yaml`
6. `TC-RFXXX_old.yaml`

**Documentos atualizados:**
1. `RFXXX.md`, `RFXXX.yaml`
2. `UC-RFXXX.md`, `UC-RFXXX.yaml`
3. `WF-RFXXX.md`, `WF-RFXXX.yaml`
4. `MD-RFXXX.md`, `MD-RFXXX.yaml`
5. `MT-RFXXX.yaml`
6. `TC-RFXXX.yaml`

**Relatório de delta:**
7. `.temp_ia/aditivo-RFXXX-delta-report.md`

**Relatório de validação (gerado por este contrato):**
8. `.temp_ia/validacao-aditivo-RFXXX-relatorio.md`

### 🎯 Princípios Fundamentais

1. **Modo READ-ONLY**: Este contrato NÃO corrige problemas, apenas identifica
2. **Validação Rigorosa**: 15 validações obrigatórias, todas devem PASSAR
3. **Delta Verificável**: Comparar `_old` vs original para identificar mudanças
4. **Cobertura 100%**: Nova funcionalidade DEVE estar em todos os níveis
5. **Aprovação Sem Ressalvas**: 100% ou REPROVADO

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Validador de Aditivo |
| **Escopo** | Validar que aditivo foi aplicado corretamente |
| **Modo** | READ-ONLY (identifica gaps, não corrige) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme docs/contracts/documentacao/validacao/aditivo.md para RFXXX"**

Exemplo:
```
Conforme docs/contracts/documentacao/validacao/aditivo.md para RF028.
Seguir CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Validar que um **ADITIVO foi aplicado corretamente**, verificando:

1. **Backups existem** - 10 arquivos `_old` criados
2. **Delta identificável** - Diferenças entre `_old` e original documentadas
3. **Cobertura total** - Nova funcionalidade em RF → UC → WF → MD → MT → TC
4. **Sincronização** - .md ↔ .yaml em todos os níveis
5. **Relatório de delta** - Documento gerado e completo

---

## 4. Detecção de Cenário (Primeira Validação)

Antes de iniciar as validações, o agente DEVE detectar qual cenário se aplica:

### CENÁRIO A: ADITIVO FOI EXECUTADO

**Condições:**
- ✅ Pelo menos 2 arquivos `_old` existem (RFXXX_old.md + RFXXX_old.yaml)
- ✅ Relatório de delta existe (`.temp_ia/aditivo-RFXXX-delta-report.md`)

**Ação:**
➡️ **Executar as 15 validações completas** conforme definido neste contrato

### CENÁRIO B: ADITIVO NÃO FOI EXECUTADO

**Condições:**
- ❌ Nenhum arquivo `_old` existe, OU
- ❌ Relatório de delta NÃO existe

**Ação:**
➡️ **Informar que não há aditivo para validar** e encerrar SEM REPROVAR

**Mensagem de saída:**
```markdown
# RELATÓRIO DE VALIDAÇÃO - ADITIVO RFXXX

## CENÁRIO DETECTADO: ADITIVO NÃO EXECUTADO

Não foram encontrados arquivos `_old` ou relatório de delta para RFXXX.

**Arquivos _old procurados:**
- RFXXX_old.md: ❌ NÃO EXISTE
- RFXXX_old.yaml: ❌ NÃO EXISTE
- UC-RFXXX_old.md: ❌ NÃO EXISTE
- UC-RFXXX_old.yaml: ❌ NÃO EXISTE
- (...)

**Relatório de delta:**
- .temp_ia/aditivo-RFXXX-delta-report.md: ❌ NÃO EXISTE

## CONCLUSÃO

⚠️ **NÃO HÁ ADITIVO PARA VALIDAR**

Este RF não passou por processo de ADITIVO (evolução incremental).
Não é possível executar as 15 validações deste contrato.

**Isto NÃO é uma falha.** Apenas significa que este validador não se aplica a este RF.

## RECOMENDAÇÕES

**Se você quer adicionar uma funcionalidade a este RF:**
1. Execute: `docs/prompts/documentacao/execucao/aditivo.md`
2. Depois execute este validador novamente

**Se você quer apenas validar sincronização dos documentos:**
1. Execute: `docs/prompts/documentacao/validacao/rf.md`
2. Execute: `docs/prompts/documentacao/validacao/uc.md`
3. Execute: `docs/prompts/documentacao/validacao/wf-md.md`

---

**VEREDICTO:** ⚠️ N/A (Validador não aplicável - RF não possui aditivo)
```

### CENÁRIO C: ADITIVO PARCIAL (Incompleto)

**Condições:**
- ⚠️ Alguns arquivos `_old` existem (1-9 arquivos, não todos os 10)
- ⚠️ Relatório de delta pode ou não existir

**Ação:**
➡️ **Executar validações parciais** e reportar o que está faltando

**Mensagem de saída:**
```markdown
# RELATÓRIO DE VALIDAÇÃO - ADITIVO RFXXX

## CENÁRIO DETECTADO: ADITIVO PARCIAL (INCOMPLETO)

Foram encontrados apenas X/10 arquivos `_old`.

**Arquivos _old encontrados:**
- RFXXX_old.md: ✅ EXISTE
- RFXXX_old.yaml: ✅ EXISTE
- (...)

**Arquivos _old faltando:**
- WF-RFXXX_old.md: ❌ AUSENTE
- (...)

## VALIDAÇÕES POSSÍVEIS

Executando validações com base nos arquivos disponíveis:
- VAL-1: Backups _old existem → ⚠️ PARCIAL (X/10)
- VAL-2: RF atualizado → ✅ EXECUTAR (RFXXX_old.md existe)
- VAL-3: Delta RF rastreável → ✅ EXECUTAR
- (...)

## CONCLUSÃO

⚠️ **ADITIVO INCOMPLETO**

O processo de ADITIVO foi iniciado mas não foi concluído.
Faltam Y arquivos _old.

## RECOMENDAÇÕES

1. Complete o processo de ADITIVO:
   - Execute: `docs/prompts/documentacao/execucao/aditivo.md`
   - Certifique-se de criar TODOS os 10 backups `_old`

2. Depois execute este validador novamente

---

**VEREDICTO:** ⚠️ ADITIVO INCOMPLETO (X/10 backups)
```

---

## 5. Pré-Requisitos Mínimos (Apenas para CENÁRIO A)

**Se CENÁRIO A for detectado**, verificar:

| # | Pré-Requisito | Verificação |
|---|---------------|-------------|
| 1 | RF original existe (`RFXXX.md`, `RFXXX.yaml`) | ✅ Arquivo existe |
| 2 | RF backup existe (`RFXXX_old.md`, `RFXXX_old.yaml`) | ✅ Arquivo existe |
| 3 | UC original existe (`UC-RFXXX.md`, `UC-RFXXX.yaml`) | ✅ Arquivo existe |
| 4 | UC backup existe (`UC-RFXXX_old.md`, `UC-RFXXX_old.yaml`) | ✅ Arquivo existe |
| 5 | WF original existe (`WF-RFXXX.md`, `WF-RFXXX.yaml`) | ✅ Arquivo existe |
| 6 | WF backup existe (`WF-RFXXX_old.md`, `WF-RFXXX_old.yaml`) | ✅ Arquivo existe |
| 7 | MD original existe (`MD-RFXXX.md`, `MD-RFXXX.yaml`) | ✅ Arquivo existe |
| 8 | MD backup existe (`MD-RFXXX_old.md`, `MD-RFXXX_old.yaml`) | ✅ Arquivo existe |
| 9 | MT original existe (`MT-RFXXX.yaml`) | ✅ Arquivo existe |
| 10 | MT backup existe (`MT-RFXXX_old.yaml`) | ✅ Arquivo existe |
| 11 | TC original existe (`TC-RFXXX.yaml`) | ✅ Arquivo existe |
| 12 | TC backup existe (`TC-RFXXX_old.yaml`) | ✅ Arquivo existe |
| 13 | Relatório de delta existe (`.temp_ia/aditivo-RFXXX-delta-report.md`) | ✅ Arquivo existe |

**Se qualquer pré-requisito falhar:**
➡️ **BLOQUEIO TOTAL**. Aditivo não foi executado corretamente.

---

## 5. Validações Obrigatórias (16 Validações)

### ⚠️ VAL-0: PLANO DE EXECUÇÃO CUMPRIDO (CRÍTICO - BLOQUEANTE)

**Objetivo:** Garantir que o ADITIVO executou EXATAMENTE o que foi planejado no PASSO 0.

**Severidade:** CRÍTICA — Se VAL-0 FAIL, **TODAS as outras validações são inválidas**.

**Critério:**
- ✅ PASS: 100% do plano cumprido (todas as entregas criadas conforme planejado)
- ❌ FAIL: Plano parcialmente cumprido (faltam entregas ou entregas extras não justificadas)
- ❌ BLOQUEIO: Arquivo de plano não existe (`.temp_ia/aditivo-RFXXX-PLANO.md`)

---

#### 0.1. Ler Plano de Execução

```python
import os
import yaml
import re

# Verificar se plano existe
plano_path = f".temp_ia/aditivo-{rf_id}-PLANO.md"

if not os.path.exists(plano_path):
    FAIL("BLOQUEIO TOTAL: Arquivo de plano não existe. ADITIVO executado sem planejamento.")
    return  # Não prosseguir com outras validações

# Ler plano
with open(plano_path, 'r', encoding='utf-8') as f:
    plano_content = f.read()

# Extrair entregas planejadas
rns_planejadas = extrair_lista_plano(plano_content, "### 2.1. RF", "**RNs a adicionar:**")
ucs_planejados = extrair_lista_plano(plano_content, "### 2.2. UC", "**UCs a criar:**")
wfs_planejados = extrair_lista_plano(plano_content, "### 2.3. WF", "**WFs a criar") if "### 2.3. WF" in plano_content else []
# ... (MD, MT, TC)
```

---

#### 0.2. Validar RF: RNs Planejadas vs Criadas

```python
# Extrair RNs criadas (delta)
rf_md = ler_arquivo(f"{rf_path}/RF{rf_id}.md")
rf_old_md = ler_arquivo(f"{rf_path}/RF{rf_id}_old.md")

rns_atual = set(re.findall(r'RN-[A-Z]+-\d+-\d+', rf_md))
rns_old = set(re.findall(r'RN-[A-Z]+-\d+-\d+', rf_old_md))
rns_criadas = rns_atual - rns_old

# Comparar com plano
if rns_criadas == set(rns_planejadas):
    PASS(f"✅ RF: {len(rns_criadas)}/{len(rns_planejadas)} RNs criadas (100% do plano)")
else:
    faltantes = set(rns_planejadas) - rns_criadas
    extras = rns_criadas - set(rns_planejadas)

    msg_erro = []
    if faltantes:
        msg_erro.append(f"Faltam {len(faltantes)} RNs planejadas: {faltantes}")
    if extras:
        msg_erro.append(f"{len(extras)} RNs extras não planejadas: {extras}")

    FAIL(f"❌ RF: {' | '.join(msg_erro)}")
```

---

#### 0.3. Validar UC: UCs Planejados vs Criados

```python
# Extrair UCs criados (delta)
uc_yaml = ler_yaml(f"{rf_path}/UC-RF{rf_id}.yaml")
uc_old_yaml = ler_yaml(f"{rf_path}/UC-RF{rf_id}_old.yaml")

ucs_atual = set([uc['id'] for uc in uc_yaml['casos_uso']])
ucs_old = set([uc['id'] for uc in uc_old_yaml['casos_uso']])
ucs_criados = ucs_atual - ucs_old

# Comparar com plano
if ucs_criados == set(ucs_planejados):
    PASS(f"✅ UC: {len(ucs_criados)}/{len(ucs_planejados)} UCs criados (100% do plano)")
else:
    faltantes = set(ucs_planejados) - ucs_criados
    extras = ucs_criados - set(ucs_planejados)

    msg_erro = []
    if faltantes:
        msg_erro.append(f"Faltam {len(faltantes)} UCs planejados: {faltantes}")
    if extras:
        msg_erro.append(f"{len(extras)} UCs extras não planejados: {extras}")

    FAIL(f"❌ UC: {' | '.join(msg_erro)}")
```

---

#### 0.4. Validar Cobertura UC → RN (Conforme Plano)

```python
# Extrair matriz de cobertura do plano
matriz_planejada = extrair_matriz_cobertura(plano_content, "**Matriz de Cobertura UC → RN:**")

# Exemplo: {'UC-09': ['RN-AUTH-013'], 'UC-10': ['RN-AUTH-014', 'RN-AUTH-015']}

# Para CADA RN planejada, verificar se há UC cobrindo
rns_nao_cobertas = []

for rn_planejada in rns_planejadas:
    # Verificar se RN está na matriz planejada
    uc_que_cobre = None
    for uc, rns in matriz_planejada.items():
        if rn_planejada in rns:
            uc_que_cobre = uc
            break

    if not uc_que_cobre:
        rns_nao_cobertas.append(rn_planejada)
        continue

    # Verificar se UC foi realmente criado
    if uc_que_cobre not in ucs_criados:
        rns_nao_cobertas.append(f"{rn_planejada} (UC {uc_que_cobre} não foi criado)")
        continue

    # Verificar se UC realmente cobre a RN (no código criado)
    uc_obj = next((uc for uc in uc_yaml['casos_uso'] if uc['id'] == uc_que_cobre), None)
    rns_cobertas_uc = uc_obj.get('rns_aplicadas', []) if uc_obj else []

    if rn_planejada not in rns_cobertas_uc:
        rns_nao_cobertas.append(f"{rn_planejada} (UC {uc_que_cobre} existe mas não cobre esta RN)")

if len(rns_nao_cobertas) == 0:
    PASS(f"✅ Cobertura: 100% das {len(rns_planejadas)} RNs planejadas cobertas por UCs")
else:
    FAIL(f"❌ Cobertura: {len(rns_nao_cobertas)} RNs planejadas não cobertas: {rns_nao_cobertas}")
```

---

#### 0.5. Validar WF (SE WF EXISTIR)

```python
wf_old_existe = os.path.exists(f"{rf_path}/WF-RF{rf_id}_old.md")

if not wf_old_existe:
    PASS("⚠️ WF: N/A (WF não existe no RF original - baseline ausente)")
else:
    if len(wfs_planejados) == 0:
        PASS("✅ WF: Nenhum WF planejado (sem mudanças em WF)")
    else:
        # Extrair WFs criados
        wf_yaml = ler_yaml(f"{rf_path}/WF-RF{rf_id}.yaml")
        wf_old_yaml = ler_yaml(f"{rf_path}/WF-RF{rf_id}_old.yaml")

        wfs_atual = set([wf['id'] for wf in wf_yaml.get('wireframes', [])])
        wfs_old = set([wf['id'] for wf in wf_old_yaml.get('wireframes', [])])
        wfs_criados = wfs_atual - wfs_old

        if wfs_criados == set(wfs_planejados):
            PASS(f"✅ WF: {len(wfs_criados)}/{len(wfs_planejados)} WFs criados (100% do plano)")
        else:
            faltantes = set(wfs_planejados) - wfs_criados
            FAIL(f"❌ WF: Faltam {len(faltantes)} WFs planejados: {faltantes}")
```

---

#### 0.6. Validar MD (SE MD EXISTIR)

```python
md_old_existe = os.path.exists(f"{rf_path}/MD-RF{rf_id}_old.md")

if not md_old_existe:
    PASS("⚠️ MD: N/A (MD não existe no RF original - baseline ausente)")
else:
    # Extrair entregas MD planejadas
    dtos_planejados = extrair_lista_plano(plano_content, "### 2.4. MD", "**DTOs a criar:**")
    entidades_planejadas = extrair_lista_plano(plano_content, "### 2.4. MD", "**Entidades a criar/modificar:**")

    if len(dtos_planejados) == 0 and len(entidades_planejadas) == 0:
        PASS("✅ MD: Nenhuma mudança planejada (sem alterações em MD)")
    else:
        # Extrair DTOs/Entidades criados
        md_yaml = ler_yaml(f"{rf_path}/MD-RF{rf_id}.yaml")
        md_old_yaml = ler_yaml(f"{rf_path}/MD-RF{rf_id}_old.yaml")

        dtos_criados = verificar_dtos_criados(md_yaml, md_old_yaml)
        entidades_criadas = verificar_entidades_criadas(md_yaml, md_old_yaml)

        gaps = []
        if set(dtos_criados) != set(dtos_planejados):
            faltantes = set(dtos_planejados) - set(dtos_criados)
            gaps.append(f"DTOs faltantes: {faltantes}")

        if set(entidades_criadas) != set(entidades_planejadas):
            faltantes = set(entidades_planejadas) - set(entidades_criadas)
            gaps.append(f"Entidades faltantes: {faltantes}")

        if len(gaps) == 0:
            PASS(f"✅ MD: 100% das mudanças planejadas implementadas")
        else:
            FAIL(f"❌ MD: {' | '.join(gaps)}")
```

---

#### 0.7. Validar MT/TC (SE EXISTIREM)

```python
# Lógica similar para MT e TC
# Verificar se massas de teste e casos de teste planejados foram criados
```

---

#### 0.8. Veredicto VAL-0

```python
# Consolidar resultados de todas as subvalidações (0.2 a 0.7)

if todas_subvalidacoes_pass():
    PASS("✅ VAL-0: 100% do plano cumprido. Todas as entregas planejadas foram criadas.")
else:
    FAIL("❌ VAL-0: Plano parcialmente cumprido. Há entregas faltantes ou extras não justificadas.")
    WARNING("⚠️ BLOQUEIO: Com VAL-0 FAIL, as outras validações (VAL-1 a VAL-15) podem ser inválidas.")
```

---

### PARTE 1: BACKUPS E DELTA (5 validações)

#### VAL-1: Backups `_old` Existem (10 arquivos)

**Critério:**
- ✅ PASS: 10/10 arquivos `_old` existem
- ❌ FAIL: Qualquer arquivo `_old` faltando

**Como verificar:**
```python
arquivos_old = [
    "RFXXX_old.md", "RFXXX_old.yaml",
    "UC-RFXXX_old.md", "UC-RFXXX_old.yaml",
    "WF-RFXXX_old.md", "WF-RFXXX_old.yaml",
    "MD-RFXXX_old.md", "MD-RFXXX_old.yaml",
    "MT-RFXXX_old.yaml", "TC-RFXXX_old.yaml"
]

existentes = [f for f in arquivos_old if os.path.exists(f)]

if len(existentes) == 10:
    PASS()
else:
    FAIL(f"Apenas {len(existentes)}/10 backups existem: {arquivos_old - existentes}")
```

---

#### VAL-2: RF Atualizado (RNs Adicionadas)

**Critério:**
- ✅ PASS: ≥1 RN nova em RFXXX.md (comparado com RFXXX_old.md)
- ⚠️ WARNING: 1-2 RNs (aditivo focado, mas funciona)
- ✅ OPTIMAL: ≥3 RNs (aditivo robusto)
- ❌ FAIL: 0 RNs novas (nenhuma funcionalidade adicionada)

**Como verificar:**
```python
# Extrair RNs de RFXXX.md
rns_atual = set(re.findall(r'RN-[A-Z]+-\d+-\d+', rf_md_content))

# Extrair RNs de RFXXX_old.md
rns_old = set(re.findall(r'RN-[A-Z]+-\d+-\d+', rf_old_md_content))

# Delta (RNs novas)
rns_novas = rns_atual - rns_old

if len(rns_novas) == 0:
    FAIL("Nenhuma RN adicionada. Aditivo sem funcionalidade nova.")
elif len(rns_novas) >= 3:
    PASS(f"{len(rns_novas)} RNs adicionadas (aditivo robusto): {rns_novas}")
else:  # 1-2 RNs
    PASS(f"{len(rns_novas)} RNs adicionadas (aditivo focado): {rns_novas}")
    WARNING("Aditivo focado (1-2 RNs). Ideal: ≥3 RNs para aditivos robustos.")
```

---

#### VAL-3: Delta RF Rastreável

**Critério:**
- ✅ PASS: Mudanças entre RFXXX.md e RFXXX_old.md identificáveis
- ❌ FAIL: Não foi possível identificar delta

**Como verificar:**
```python
# Comparar seções críticas
secoes_rf = [
    "## 4. FUNCIONALIDADES",
    "## 5. REGRAS DE NEGÓCIO",
    "## 7. PERMISSÕES (RBAC)",
    "## 8. ENDPOINTS DA API",
    "## 9. MODELO DE DADOS",
    "## 11. INTEGRAÇÕES OBRIGATÓRIAS"
]

delta = {}
for secao in secoes_rf:
    conteudo_atual = extrair_secao(rf_md_content, secao)
    conteudo_old = extrair_secao(rf_old_md_content, secao)

    if conteudo_atual != conteudo_old:
        delta[secao] = {
            "linhas_adicionadas": contar_linhas_adicionadas(conteudo_atual, conteudo_old),
            "linhas_removidas": contar_linhas_removidas(conteudo_atual, conteudo_old)
        }

if len(delta) > 0:
    PASS(f"Delta identificado em {len(delta)} seções: {list(delta.keys())}")
else:
    FAIL("Nenhuma mudança identificada entre RFXXX.md e RFXXX_old.md")
```

---

#### VAL-4: Delta UC Rastreável

**Critério:**
- ✅ PASS: Novos UCs identificados entre UC-RFXXX.yaml e UC-RFXXX_old.yaml
- ❌ FAIL: Nenhum UC novo identificado

**Como verificar:**
```python
# Extrair IDs de UCs
ucs_atual = set([uc['id'] for uc in uc_yaml['casos_uso']])
ucs_old = set([uc['id'] for uc in uc_old_yaml['casos_uso']])

# Delta
ucs_novos = ucs_atual - ucs_old

if len(ucs_novos) > 0:
    PASS(f"{len(ucs_novos)} UCs novos: {ucs_novos}")
else:
    FAIL("Nenhum UC novo identificado")
```

---

#### VAL-5: Delta Documentado em Relatório

**Critério:**
- ✅ PASS: Relatório `.temp_ia/aditivo-RFXXX-delta-report.md` existe e contém delta
- ❌ FAIL: Relatório não existe ou está incompleto

**Como verificar:**
```python
relatorio_path = ".temp_ia/aditivo-RFXXX-delta-report.md"

if not os.path.exists(relatorio_path):
    FAIL("Relatório de delta não existe")

relatorio_content = read_file(relatorio_path)

# Verificar seções obrigatórias
secoes_obrigatorias = [
    "## FUNCIONALIDADE ADICIONADA",
    "## DELTA APLICADO",
    "### 2.1 RF",
    "### 2.2 UC",
    "### 2.3 WF",
    "### 2.4 MD",
    "### 2.5 MT",
    "### 2.6 TC",
    "## VALIDAÇÕES EXECUTADAS",
    "## COBERTURA TOTAL",
    "## VEREDICTO FINAL"
]

secoes_presentes = [s for s in secoes_obrigatorias if s in relatorio_content]

if len(secoes_presentes) == len(secoes_obrigatorias):
    PASS("Relatório de delta completo")
else:
    FAIL(f"Relatório incompleto. Faltam: {set(secoes_obrigatorias) - set(secoes_presentes)}")
```

---

### PARTE 2: SINCRONIZAÇÃO .md ↔ .yaml (5 validações)

#### VAL-6: RF.md ↔ RF.yaml Sincronizados (100%)

**Critério:**
- ✅ PASS: RNs, permissões, catálogo 100% sincronizados
- ❌ FAIL: Qualquer inconsistência

**Como verificar:**
```python
# RNs em MD
rns_md = set(re.findall(r'RN-[A-Z]+-\d+-\d+', rf_md_content))

# RNs em YAML
rns_yaml = set([rn['id'] for rn in rf_yaml['regras_negocio']])

# Gaps
rns_md_only = rns_md - rns_yaml
rns_yaml_only = rns_yaml - rns_md

if len(rns_md_only) == 0 and len(rns_yaml_only) == 0:
    PASS("RF.md ↔ RF.yaml 100% sincronizados")
else:
    FAIL(f"RNs em MD apenas: {rns_md_only}, RNs em YAML apenas: {rns_yaml_only}")
```

---

#### VAL-7: UC.md ↔ UC.yaml Sincronizados (100%)

**Critério:**
- ✅ PASS: UCs 100% sincronizados
- ❌ FAIL: Qualquer inconsistência

---

#### VAL-8: WF.md ↔ WF.yaml Sincronizados (100%)

**Critério:**
- ✅ PASS: WFs 100% sincronizados
- ❌ FAIL: Qualquer inconsistência

---

#### VAL-9: MD.md ↔ MD.yaml Sincronizados (100%)

**Critério:**
- ✅ PASS: Tabelas e campos 100% sincronizados
- ❌ FAIL: Qualquer inconsistência

---

#### VAL-10: Validador RF-UC Passou (Exit Code 0)

**Critério:**
- ✅ PASS: `python docs/tools/docs/validator-rf-uc.py RFXXX` retorna exit code 0
- ❌ FAIL: Exit code != 0

**Como verificar:**
```bash
cd D:\IC2
python docs/tools/docs/validator-rf-uc.py RFXXX
echo $?  # Deve ser 0
```

---

### PARTE 3: COBERTURA TOTAL (5 validações)

#### VAL-11: UC Cobre 100% do Delta RF

**Critério:**
- ✅ PASS: Todas as RNs novas estão cobertas por UCs novos
- ❌ FAIL: Alguma RN nova sem cobertura

**Como verificar:**
```python
# RNs novas (delta RF)
rns_novas = rns_atual - rns_old

# RNs cobertas por UCs novos
rns_cobertas_ucs_novos = set()
for uc_novo in ucs_novos:
    uc_data = [uc for uc in uc_yaml['casos_uso'] if uc['id'] == uc_novo][0]
    rns_cobertas_ucs_novos.update(uc_data.get('regras_negocio_cobertas', []))

# Gaps
rns_nao_cobertas = rns_novas - rns_cobertas_ucs_novos

if len(rns_nao_cobertas) == 0:
    PASS("100% das RNs novas cobertas por UCs novos")
else:
    FAIL(f"RNs novas sem cobertura: {rns_nao_cobertas}")
```

---

#### VAL-12: WF Cobre 100% dos Novos UCs

**Critério:**
- ✅ PASS: Todos os UCs novos possuem WFs correspondentes
- ⚠️ WARNING: Alguns UCs novos sem WF (pode indicar documentação original incompleta)
- ❌ FAIL: Nenhum WF criado quando há UCs novos que requerem interface

**Como verificar:**
```python
# Verificar se WF-RFXXX_old existe
wf_old_existe = os.path.exists("WF-RFXXX_old.md")

if not wf_old_existe:
    # RF original não tinha WFs documentados
    WARNING("RF original sem WFs documentados. Validação de cobertura WF não aplicável.")
    PASS("N/A - RF original sem baseline de WFs")
else:
    # Verificar cobertura
    ucs_sem_wf = verificar_ucs_sem_wf(ucs_novos, wfs_atuais)
    if len(ucs_sem_wf) == 0:
        PASS("100% dos UCs novos possuem WFs")
    else:
        WARNING(f"UCs sem WF: {ucs_sem_wf}. Pode indicar documentação original incompleta.")
```

---

#### VAL-13: MD Atualizado (se Aplicável)

**Critério:**
- ✅ PASS: Se RF documentou mudanças no modelo (Seção 9), MD foi atualizado
- ✅ PASS: Se RF não documentou mudanças, MD não mudou
- ⚠️ WARNING: MD-RFXXX_old não existe (documentação original incompleta)
- ❌ FAIL: RF documenta mudanças mas MD não foi atualizado

**Como verificar:**
```python
# Verificar se MD-RFXXX_old existe
md_old_existe = os.path.exists("MD-RFXXX_old.md")

if not md_old_existe:
    # RF original não tinha MD documentado
    WARNING("RF original sem MD documentado. Validação de MD não aplicável.")
    PASS("N/A - RF original sem baseline de MD")
else:
    # Verificar se RF documenta mudanças no MD
    rf_documenta_mudancas_md = verificar_secao_9_md_mudancas(rf_md_content)

    if rf_documenta_mudancas_md:
        md_foi_atualizado = comparar_md(md_atual, md_old)
        if md_foi_atualizado:
            PASS("MD atualizado conforme documentado no RF")
        else:
            FAIL("RF documenta mudanças no MD mas MD não foi atualizado")
    else:
        PASS("RF não documenta mudanças no MD")
```

---

#### VAL-14: MT Cobre Novos UCs

**Critério:**
- ✅ PASS: Massas de teste criadas para cada UC novo
- ⚠️ WARNING: MT-RFXXX_old não existe (documentação original incompleta)
- ❌ FAIL: UC novo sem massa de teste (quando MT-RFXXX_old existe)

**Como verificar:**
```python
# Verificar se MT-RFXXX_old existe
mt_old_existe = os.path.exists("MT-RFXXX_old.yaml")

if not mt_old_existe:
    # RF original não tinha MT documentado
    WARNING("RF original sem MT documentado. Validação de MT não aplicável.")
    PASS("N/A - RF original sem baseline de MT")
else:
    # Verificar cobertura
    ucs_sem_mt = verificar_ucs_sem_mt(ucs_novos, mt_yaml)
    if len(ucs_sem_mt) == 0:
        PASS("100% dos UCs novos possuem massas de teste")
    else:
        FAIL(f"UCs sem MT: {ucs_sem_mt}")
```

---

#### VAL-15: TC Cobre Novos UCs (Mínimo 30 TCs por UC)

**Critério:**
- ✅ PASS: ≥30 TCs por UC novo
- ⚠️ WARNING: TC-RFXXX_old não existe (documentação original incompleta)
- ❌ FAIL: Algum UC novo com <30 TCs (quando TC-RFXXX_old existe)

**Como verificar:**
```python
# Verificar se TC-RFXXX_old existe
tc_old_existe = os.path.exists("TC-RFXXX_old.yaml")

if not tc_old_existe:
    # RF original não tinha TC documentado
    WARNING("RF original sem TC documentado. Validação de TC não aplicável.")
    PASS("N/A - RF original sem baseline de TC")
else:
    # Para cada UC novo, verificar cobertura de TCs
    for uc_novo in ucs_novos:
        tcs_uc = [tc for tc in tc_yaml['casos_teste'] if tc['uc_id'] == uc_novo]

        if len(tcs_uc) < 30:
            FAIL(f"{uc_novo}: apenas {len(tcs_uc)} TCs (mínimo 30)")

    PASS("Todos os UCs novos possuem ≥30 TCs")
```

---

## 6. Critérios de Aprovação

### 🚨 REGRA CRÍTICA: VAL-0 É BLOQUEANTE

**IMPORTANTE:** VAL-0 (Plano de Execução Cumprido) **DEVE** passar ANTES de avaliar outras validações.

**Se VAL-0 FAIL:**
- ❌ **REPROVADO IMEDIATO** (sem avaliar VAL-1 a VAL-15)
- ❌ Execução foi parcial/incorreta (não cumpriu o planejado)
- ❌ Outras validações podem ser inválidas (baseadas em execução incompleta)

**Se VAL-0 PASS:**
- ✅ Prosseguir com validações VAL-1 a VAL-15
- ✅ Aplicar critérios normais de aprovação

---

### Critérios de Aprovação (Após VAL-0 PASS)

**✅ APROVADO (100%):**
- ✅ **VAL-0: PASS** (100% do plano cumprido) — OBRIGATÓRIO
- ✅ 100% das validações **aplicáveis** (VAL-1 a VAL-15) PASS
- ✅ Validações N/A (baseline ausente) não contam para pontuação
- ✅ Zero gaps identificados nas validações aplicáveis
- ✅ Relatório de delta completo
- ✅ Relatório de validação completo

**❌ REPROVADO (<100%):**
- ❌ **VAL-0: FAIL** (plano não cumprido) — BLOQUEIO IMEDIATO
- **OU**
- ❌ Qualquer validação **aplicável** (VAL-1 a VAL-15) FAIL
- ❌ Gap de cobertura quando baseline existe
- ❌ Inconsistências entre .md e .yaml (quando ambos existem)
- ❌ Relatórios incompletos

**⚠️ VALIDAÇÕES N/A (Não Aplicáveis):**
- ✅ Não reprovam o aditivo
- ✅ Indicam que documento não existia antes (baseline ausente)
- ✅ São reportadas como WARNING informativo
- ✅ Não contam para pontuação final
- ⚠️ Aplicam-se apenas a VAL-1 a VAL-15 (VAL-0 nunca é N/A)

**⚠️ NÃO EXISTE "APROVADO COM RESSALVAS"**
➡️ Aditivo deve ter:
1. ✅ VAL-0 PASS (100% do plano cumprido)
2. ✅ 100% das validações aplicáveis (VAL-1 a VAL-15) PASS

Ou será REPROVADO.

---

## 7. Estrutura do Relatório de Validação

O relatório **DEVE** seguir este formato:

```markdown
# RELATÓRIO DE VALIDAÇÃO - ADITIVO RFXXX

**Data:** YYYY-MM-DD
**RF:** RFXXX
**Validador:** Agente de Validação ADITIVO
**Modo:** READ-ONLY

---

## 1. RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Backups _old existem | ✅ PASS | CRÍTICO | 10/10 arquivos |
| 2 | RF atualizado (≥3 RNs) | ✅ PASS | CRÍTICO | 3 RNs novas |
| 3 | Delta RF rastreável | ✅ PASS | CRÍTICO | 6 seções modificadas |
| 4 | Delta UC rastreável | ✅ PASS | CRÍTICO | 2 UCs novos |
| 5 | Delta documentado | ✅ PASS | CRÍTICO | Relatório completo |
| 6 | RF.md ↔ RF.yaml | ✅ PASS | CRÍTICO | 100% |
| 7 | UC.md ↔ UC.yaml | ✅ PASS | CRÍTICO | 100% |
| 8 | WF.md ↔ WF.yaml | ✅ PASS | CRÍTICO | 100% |
| 9 | MD.md ↔ MD.yaml | ✅ PASS | CRÍTICO | 100% |
| 10 | Validador RF-UC | ✅ PASS | CRÍTICO | Exit code 0 |
| 11 | UC cobre 100% delta RF | ✅ PASS | CRÍTICO | 3/3 RNs cobertas |
| 12 | WF cobre 100% novos UCs | ✅ PASS | CRÍTICO | 2/2 UCs cobertos |
| 13 | MD atualizado | ✅ PASS | IMPORTANTE | 1 tabela adicionada |
| 14 | MT cobre novos UCs | ✅ PASS | IMPORTANTE | 25 massas criadas |
| 15 | TC cobre novos UCs | ✅ PASS | CRÍTICO | 75 TCs (≥30 por UC) |

**PONTUAÇÃO FINAL:** 15/15 PASS (100%)
**VEREDICTO:** ✅ APROVADO

---

## 2. DELTA IDENTIFICADO

### 2.1 RF (RFXXX.md, RFXXX.yaml)

**RNs Adicionadas:**
- RN-CLI-028-15: Sistema DEVE gerar PDF com logo da empresa
- RN-CLI-028-16: Sistema DEVE permitir exportação com filtros aplicados
- RN-CLI-028-17: Sistema DEVE validar permissão antes de exportar

**Endpoints Adicionados:**
- GET /api/v1/clientes/export/pdf

**Permissões Adicionadas:**
- cliente.export_pdf

**Total:** 3 RNs, 1 endpoint, 1 permissão

### 2.2 UC (UC-RFXXX.md, UC-RFXXX.yaml)

**UCs Adicionados:**
- UC-12: Exportar Lista de Clientes em PDF
- UC-13: Validar Permissão de Exportação

**Total:** 2 UCs novos

### 2.3 WF (WF-RFXXX.md, WF-RFXXX.yaml)

**WFs Adicionados:**
- WF-12: Tela de Exportação PDF

**Total:** 1 WF novo

### 2.4 MD (MD-RFXXX.md, MD-RFXXX.yaml)

**Tabelas Adicionadas:**
- cliente_exportacao_log (10 campos)

**Total:** 1 tabela

### 2.5 MT (MT-RFXXX.yaml)

**Massas Adicionadas:**
- 15 massas para UC-12
- 10 massas para UC-13

**Total:** 25 massas

### 2.6 TC (TC-RFXXX.yaml)

**TCs Adicionados:**
- 40 TCs para UC-12 (Backend: 15, Frontend: 15, Segurança: 10)
- 35 TCs para UC-13 (Backend: 15, Frontend: 12, Segurança: 8)

**Total:** 75 TCs

---

## 3. COBERTURA VALIDADA

- ✅ Nova funcionalidade 100% coberta em RF (3 RNs)
- ✅ Nova funcionalidade 100% coberta em UC (2 UCs)
- ✅ Nova funcionalidade 100% coberta em WF (1 WF)
- ✅ Nova funcionalidade 100% coberta em MD (1 tabela)
- ✅ Nova funcionalidade 100% coberta em MT (25 massas)
- ✅ Nova funcionalidade 100% coberta em TC (75 TCs)

---

## 4. SINCRONIZAÇÃO VALIDADA

| Documentos | Status | Percentual |
|------------|--------|------------|
| RF.md ↔ RF.yaml | ✅ PASS | 100% |
| UC.md ↔ UC.yaml | ✅ PASS | 100% |
| WF.md ↔ WF.yaml | ✅ PASS | 100% |
| MD.md ↔ MD.yaml | ✅ PASS | 100% |

---

## 5. GAPS IDENTIFICADOS

**Nenhum gap identificado.**

---

## 6. VEREDICTO FINAL

✅ **ADITIVO VALIDADO COM SUCESSO (100%)**

Todos os documentos foram atualizados com cobertura total da nova funcionalidade.
Versões `_old` criadas corretamente.
Delta rastreável e documentado.
Sincronização 100% em todos os níveis.

---

**Próximos passos:**
1. Commit e merge do aditivo
2. Executar backend-aditivo para implementar código
3. Executar frontend-aditivo para implementar UI
```

---

## 8. Regras Invioláveis

1. **NUNCA** corrigir problemas - apenas identificar e reportar
2. **SEMPRE** comparar `_old` vs original para identificar delta
3. **SEMPRE** validar cobertura 100% em cada nível
4. **NUNCA** aprovar com gaps (0% ou 100%)
5. **SEMPRE** gerar relatório de validação
6. **SEMPRE** verificar sincronização .md ↔ .yaml

---

## 9. Proibições Absolutas

- ❌ Editar arquivos (RF, UC, WF, MD, MT, TC)
- ❌ Corrigir gaps identificados (este contrato é READ-ONLY)
- ❌ Aprovar com ressalvas
- ❌ Pular validações

---

## 10. Exemplo Prático

**Solicitação:**
```
Conforme docs/contracts/documentacao/validacao/aditivo.md para RF028.
Seguir CLAUDE.md.
```

**Execução:**

1. **Verificar pré-requisitos** (13 arquivos existem)
2. **Executar 15 validações** (VAL-1 a VAL-15)
3. **Identificar delta** (RF, UC, WF, MD, MT, TC)
4. **Validar cobertura** (100% em cada nível)
5. **Validar sincronização** (.md ↔ .yaml)
6. **OPCIONAL: Gerar relatório** (`.temp_ia/validacao-aditivo-RF028-relatorio.md`) - recomendado mas não obrigatório
7. **Declarar veredicto** (✅ APROVADO ou ❌ REPROVADO)

**IMPORTANTE:** Ausência de relatório **NÃO reprova** validação (gap MENOR)

**Resultado:**
✅ ADITIVO VALIDADO COM SUCESSO (15/15 PASS, 100%)

---

## 11. Versionamento

- **Criado em:** 2026-01-03
- **Última atualização:** 2026-01-03
- **Versão:** 1.0

---

**Mantido por:** Time de Arquitetura IControlIT
**Governado por:** CLAUDE.md

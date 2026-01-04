# VALIDADOR: Contrato de Adequação Completa de UC

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Sonnet 4.5
**Propósito:** Validar se UC-RFXXX.yaml e UC-RFXXX.md estão 100% conformes após execução do CONTRATO-ADEQUACAO-COMPLETA-UC

---

## CONTEXTO

Este validador executa **auditoria de conformidade** após a adequação de UCs, verificando se:
- O agente seguiu TODAS as 15 etapas do contrato
- UC.yaml e UC.md estão sincronizados
- Cobertura RN → UC = 100%
- Nomenclatura, catálogo, templates estão corretos
- STATUS.yaml foi atualizado

---

## MODO DE OPERAÇÃO

**READ-ONLY:** Este validador NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

Se forem encontradas não-conformidades:
- Gerar relatório de gaps
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas

---

## VALIDAÇÕES OBRIGATÓRIAS

### VALIDAÇÃO 1: Cobertura RN → UC (100% Obrigatória)

**Objetivo:** Garantir que TODAS as RNs do RF.yaml estão cobertas por UCs.

**Método:**
```python
# Extrair RNs do RF.yaml
rf_rns = set(re.findall(r'"(RN-RF\d{3}-\d{2})"', rf_content))

# Extrair RNs do UC.yaml (covers.rf_items + regras_aplicadas)
uc_rns = set(re.findall(r'"(RN-RF\d{3}-\d{2})"', uc_content))

# Calcular gaps
gaps = rf_rns - uc_rns
cobertura = len(uc_rns) / len(rf_rns) * 100 if rf_rns else 0
```

**Critério de aprovação:**
- ✅ `cobertura == 100%` AND `len(gaps) == 0`
- ❌ Qualquer gap = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO 1: APROVADO
   Cobertura: 12/12 RNs (100%)
   Gaps: 0
```

---

### VALIDAÇÃO 2: Nomenclatura Padrão (RN-RFXXX-NNN)

**Objetivo:** Garantir que TODAS as RNs usam o padrão oficial.

**Método:**
```python
# Padrão esperado: RN-RF028-01, RN-RF028-02, etc.
non_standard = re.findall(r'RN-(?!RF\d{3}-\d{2})[A-Z]{2,5}-\d{3}-\d{2}', uc_content)
```

**Critério de aprovação:**
- ✅ `len(non_standard) == 0`
- ❌ Qualquer RN fora do padrão = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO 2: APROVADO
   Nomenclatura padrão: 100% (0 violações)
   Padrão: RN-RF028-XX
```

---

### VALIDAÇÃO 3: Catálogo Limpo (Zero Códigos Híbridos)

**Objetivo:** Garantir que `covers.rf_items` contém APENAS RNs válidas.

**Método:**
```python
catalog_codes = re.findall(r'RF\d{3}-(CRUD|VAL|SEC)-\d{2}', uc_content)
```

**Critério de aprovação:**
- ✅ `len(catalog_codes) == 0`
- ❌ Qualquer código de catálogo = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 3: APROVADO
   Catálogo: Limpo (0 códigos RF-CRUD/VAL/SEC)
```

---

### VALIDAÇÃO 3.5: Nomenclatura de Fluxos (FA-UCNN-NNN) ✨ NOVO BLOQUEANTE

**Objetivo:** Garantir que TODOS os fluxos alternativos e de exceção usam nomenclatura completa.

**Método:**
```python
# Buscar violações no UC.md
violacoes_fa = re.findall(r'\*\*(FA)-(\d{3}):\*\*', uc_md_content)  # FA-001 (ERRADO)
violacoes_fe = re.findall(r'\*\*(FE)-(\d{3}):\*\*', uc_md_content)  # FE-001 (ERRADO)

# Padrão correto esperado: FA-UC00-001, FE-UC00-001
corretos_fa = re.findall(r'\*\*FA-UC\d{2}-\d{3}:\*\*', uc_md_content)
corretos_fe = re.findall(r'\*\*FE-UC\d{2}-\d{3}:\*\*', uc_md_content)

total_violacoes = len(violacoes_fa) + len(violacoes_fe)
```

**Critério de aprovação:**
- ✅ `total_violacoes == 0` (nenhum FA-001, FE-001 encontrado)
- ❌ Qualquer violação = **CRÍTICO** (bloqueante)

**Exemplos de violação:**
```markdown
# ❌ INCORRETO (REPROVA)
**FA-001:** Usuário não é Super Admin
**FE-001:** Erro de conectividade

# ✅ CORRETO (APROVADO)
**FA-UC00-001:** Usuário não é Super Admin
**FE-UC00-001:** Erro de conectividade
```

**Saída esperada (APROVADO):**
```
✅ VALIDAÇÃO 3.5: APROVADO
   Nomenclatura de fluxos: 100% conforme (0 violações)
   Padrão: FA-UCNN-NNN, FE-UCNN-NNN
   Total de fluxos: 42 (todos corretos)
```

**Saída esperada (REPROVADO):**
```
❌ VALIDAÇÃO 3.5: REPROVADO
   Nomenclatura de fluxos: 0% conforme (42 violações)
   Encontrado: FA-001, FA-002, ..., FE-001, FE-002
   Esperado: FA-UC00-001, FA-UC00-002, ..., FE-UC00-001, FE-UC00-002
   Severidade: CRÍTICO (bloqueante)
   Ação: Executar script de correção automática
```

**Script de correção sugerido:**
```bash
# Backup
cp UC-RF006.md UC-RF006.md.backup-$(date +%Y%m%d)

# Correção automática (requer script Python)
python .temp_ia/scripts/fix-nomenclatura-fluxos.py UC-RF006.md

# Validar correção
grep -E '\*\*FA-[0-9]{3}:' UC-RF006.md  # Deve retornar VAZIO
```

---

### VALIDAÇÃO 4: UC.yaml Aderente ao Template v2.0 ✨ NOVO

**Objetivo:** Garantir que UC.yaml segue a estrutura do template oficial.

**Verificações:**

1. **Cabeçalho completo:**
   ```yaml
   # Comentário cabeçalho presente
   uc:
     rf: "RFXXX"
     versao: "2.0"
     data: "AAAA-MM-DD"
   ```

2. **Estrutura de cada UC:**
   - `id`, `nome`, `ator_principal`, `tipo`, `impacta_dados` presentes
   - `covers.rf_items` e `covers.uc_items` presentes
   - `precondicoes`, `gatilho`, `fluxo_principal` presentes
   - `fluxos_alternativos`, `fluxos_excecao` presentes
   - `regras_aplicadas`, `resultado_final` presentes

3. **Seções finais:**
   - `exclusions.uc_items` presente
   - `historico` presente com pelo menos 1 versão

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 4: APROVADO
   Template: UC.yaml 100% aderente ao v2.0
   Seções obrigatórias: 13/13 presentes
```

---

### VALIDAÇÃO 5: UC.md Aderente ao Template v2.0 ✨ NOVO

**Objetivo:** Garantir que UC.md segue o formato narrativo esperado.

**Verificações:**

1. **Cabeçalho:**
   ```markdown
   # Casos de Uso - RFXXX - [Nome]
   ```

2. **Estrutura de cada UC:**
   ```markdown
   ## UC0X - [Nome]

   ### Ator Principal
   ### Pré-condições
   ### Gatilho
   ### Fluxo Principal (FP)
   ### Fluxos Alternativos (FA)
   ### Fluxos de Exceção (FE)
   ### Regras Aplicadas
   ### Resultado Final
   ```

3. **Separadores:**
   - `---` entre cada UC

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes para cada UC
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 5: APROVADO
   Template: UC.md 100% aderente ao formato narrativo
   UCs formatados: 13/13
```

---

### VALIDAÇÃO 6: UC.yaml ↔ UC.md Sincronizados (100%) ✨ NOVO

**Objetivo:** Garantir que UC.yaml e UC.md descrevem os MESMOS casos de uso.

**Método:**
```python
# Extrair IDs de UCs do YAML
yaml_ucs = set(re.findall(r'- id: "(UC\d+)"', uc_yaml_content))

# Extrair IDs de UCs do MD
md_ucs = set(re.findall(r'^## (UC\d+) -', uc_md_content, re.MULTILINE))

# Comparar
divergences = yaml_ucs.symmetric_difference(md_ucs)
```

**Critério de aprovação:**
- ✅ `len(divergences) == 0`
- ❌ Qualquer divergência = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO 6: APROVADO
   Sincronia UC.yaml ↔ UC.md: 100%
   UCs no .yaml: 13
   UCs no .md: 13
   Divergências: 0
```

---

### VALIDAÇÃO 7: Jobs Background Documentados

**Objetivo:** Verificar se todos os jobs background detectados estão documentados.

**Método:**
```bash
# Buscar keywords no RF.yaml
keywords = ["job", "hangfire", "background", "scheduler", "cron"]

# Para cada job identificado, verificar UC correspondente com tipo: "background_job"
```

**Critério de aprovação:**
- ✅ Todos os jobs têm UC com `tipo: "background_job"`
- ❌ Job sem UC = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 7: APROVADO
   Jobs detectados: 5
   Jobs documentados: 5/5 (100%)
   UCs: UC09, UC10, UC11, UC12, UC05
```

---

### VALIDAÇÃO 8: Workflows Complexos Documentados

**Objetivo:** Verificar se workflows de state-machine estão documentados.

**Método:**
```bash
# Buscar keywords no RF.yaml
keywords = ["workflow", "aprovação", "state", "transição", "multinível"]

# Verificar UC com fluxos_alternativos complexos ou tipo: "workflow"
```

**Critério de aprovação:**
- ✅ Todos os workflows têm UC correspondente
- ❌ Workflow sem UC = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 8: APROVADO (ou N/A se não aplicável)
   Workflows detectados: 1
   Workflows documentados: 1/1 (100%)
```

---

### VALIDAÇÃO 9: Integrações Externas Documentadas

**Objetivo:** Verificar se integrações com APIs externas estão completas.

**Método:**
```bash
# Buscar keywords no RF.yaml
keywords = ["api", "azure", "brasil", "graph", "externo", "integra"]

# Verificar UC com seção sistema_externo, mapeamento_dados
```

**Critério de aprovação:**
- ✅ Todas as integrações têm:
  - `sistema_externo.nome`
  - `sistema_externo.tipo`
  - `sistema_externo.endpoint_base`
  - `mapeamento_dados.transformacoes`
- ❌ Integração incompleta = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 9: APROVADO
   Integrações detectadas: 1 (BrasilAPI)
   Integrações completas: 1/1 (100%)
   Seções obrigatórias: sistema_externo, mapeamento_dados presentes
```

---

### VALIDAÇÃO 10: Exit Code do Validador Automático

**Objetivo:** Confirmar que `validator-rf-uc.py` aprovou.

**Método:**
```bash
python docs/tools/docs/validator-rf-uc.py \
  --rf docs/rf/.../RFXXX.yaml \
  --uc docs/rf/.../UC-RFXXX.yaml

echo $?  # DEVE ser 0
```

**Critério de aprovação:**
- ✅ `exit_code == 0`
- ❌ `exit_code != 0` = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO 10: APROVADO
   Validador: exit code 0
   Cobertura RF → UC: 100%
```

---

### VALIDAÇÃO 11: STATUS.yaml Atualizado

**Objetivo:** Verificar se STATUS.yaml contém seção `adequacao_uc`.

**Seção esperada:**
```yaml
adequacao_uc:
  data_execucao: "AAAA-MM-DD"
  versao_contrato: "1.0"

  cobertura_antes:
    rns_totais: N
    rns_cobertas: M
    percentual: "XX%"

  cobertura_depois:
    rns_totais: N
    rns_cobertas: N
    percentual: "100%"

  problemas_corrigidos: [...]
  validacoes: {...}
  metricas: {...}
```

**Critério de aprovação:**
- ✅ Seção `adequacao_uc` presente com todas as subseções
- ❌ Seção ausente ou incompleta = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO 11: APROVADO
   STATUS.yaml: Seção adequacao_uc presente
   Métricas: cobertura_antes, cobertura_depois, validacoes presentes
```

---

### VALIDAÇÃO 12: Relatório Final Gerado

**Objetivo:** Verificar se relatório de execução foi criado.

**Arquivos esperados:**
- `.temp_ia/adequacao-uc-RFXXX-diagnostico.md`
- `.temp_ia/adequacao-uc-RFXXX-relatorio.md`

**Critério de aprovação:**
- ✅ Ambos os arquivos existem
- ❌ Qualquer arquivo ausente = **MENOR**

**Saída esperada:**
```
✅ VALIDAÇÃO 12: APROVADO
   Diagnóstico: .temp_ia/adequacao-uc-RF028-diagnostico.md (existente)
   Relatório: .temp_ia/adequacao-uc-RF028-relatorio.md (existente)
```

---

## RELATÓRIO DE VALIDAÇÃO

**Template de saída:**

```markdown
# RELATÓRIO DE VALIDAÇÃO - UC-RFXXX
**Data:** AAAA-MM-DD
**Validador:** VALIDADOR-CONTRATO-ADEQUACAO-COMPLETA-UC v2.0 (ZERO TOLERÂNCIA)

---

## RESUMO EXECUTIVO

| Validação | Status | Severidade | Resultado |
|-----------|--------|------------|-----------|
| 1. Cobertura RN → UC | ✅ PASS | CRÍTICO | 12/12 (100%) |
| 2. Nomenclatura padrão RN | ✅ PASS | CRÍTICO | 100% (0 violações) |
| 3. Catálogo limpo | ✅ PASS | IMPORTANTE | 0 códigos híbridos |
| **3.5. Nomenclatura de fluxos** | **✅ PASS** | **CRÍTICO** | **0 violações FA-NNN** |
| 4. UC.yaml → Template | ✅ PASS | IMPORTANTE | 13/13 seções |
| 5. UC.md → Template | ✅ PASS | IMPORTANTE | 13/13 UCs |
| 6. UC.yaml ↔ UC.md | ✅ PASS | CRÍTICO | 100% sincronia |
| 7. Jobs documentados | ✅ PASS | IMPORTANTE | 5/5 (100%) |
| 8. Workflows documentados | ✅ PASS ou N/A | IMPORTANTE | N/A |
| 9. Integrações documentadas | ✅ PASS | IMPORTANTE | 1/1 (100%) |
| 10. Validador automático | ✅ PASS | CRÍTICO | Exit code 0 |
| 11. STATUS.yaml | ✅ PASS | IMPORTANTE | Seção presente |
| 12. Relatório gerado | ✅ PASS | MENOR | Arquivos presentes |

**PONTUAÇÃO FINAL:** 13/13 PASS (100%)

**VEREDICTO:** ✅ **APROVADO** - UC-RFXXX está 100% conforme (ZERO GAPS)

---

## GAPS IDENTIFICADOS

**Nenhum gap de qualquer severidade identificado.** ✅

---

## RECOMENDAÇÕES

Nenhuma ação corretiva necessária. UC-RFXXX pode prosseguir para próximo contrato.

---

**Validador:** Claude Sonnet 4.5
**Tempo de validação:** ~10 minutos
**Arquivos analisados:** RF028.yaml, UC-RF028.yaml, UC-RF028.md, STATUS.yaml
```

---

## CRITÉRIOS DE APROVAÇÃO/REPROVAÇÃO

### ⚠️ REGRA DE ZERO TOLERÂNCIA

**A PARTIR DE AGORA:**
- ✅ **APROVADO** = 12/12 validações PASS + ZERO gaps (exceto falhas técnicas Python)
- ❌ **REPROVADO** = Qualquer validação FAIL OU qualquer gap (CRÍTICO, IMPORTANTE, **MENOR**)

**ÚNICA EXCEÇÃO PERMITIDA:**
- ⚠️ Falhas técnicas do validador Python (timeout, erro de script, etc.)
- Gaps de funcionalidade/nomenclatura **SEMPRE** reprovam

---

### ✅ APROVADO (100%) - CRITÉRIO RIGOROSO

**Exigências ABSOLUTAS:**
- ✅ Todas as 12 validações PASS
- ✅ ZERO gaps de qualquer severidade (CRÍTICO, IMPORTANTE, **MENOR**)
- ✅ ZERO violações de nomenclatura (incluindo FA-001 vs FA-UC00-001)
- ✅ ZERO jobs background não documentados
- ✅ ZERO integrações externas incompletas
- ✅ Validador Python exit code 0 (ou justificativa técnica)

**Exemplo de aprovação válida:**
```
12/12 PASS
0 gaps CRÍTICOS
0 gaps IMPORTANTES
0 gaps MENORES  ← OBRIGATÓRIO
Veredicto: ✅ APROVADO
```

---

### ❌ REPROVADO (<100%) - QUALQUER GAP REPROVA

**Motivos de REPROVAÇÃO (lista não-exaustiva):**
- ❌ 11/12 ou menos validações PASS
- ❌ **QUALQUER gap CRÍTICO** (ex: RN não coberta)
- ❌ **QUALQUER gap IMPORTANTE** (ex: job não documentado)
- ❌ **QUALQUER gap MENOR** (ex: FA-001 vs FA-UC00-001) ← **NOVO!**
- ❌ Nomenclatura de fluxos incorreta (42 violações = REPROVADO)
- ❌ Validador exit code ≠ 0 (exceto falhas técnicas Python)

**Exemplo de reprovação por gap "menor":**
```
12/12 PASS
0 gaps CRÍTICOS
0 gaps IMPORTANTES
3 gaps MENORES  ← REPROVA!
  - Gap #1: Nomenclatura FA-001 vs FA-UC00-001 (42 violações)
  - Gap #2: Falta RN-UC específicas
  - Gap #3: Arquivo diagnóstico ausente
Veredicto: ❌ REPROVADO
Motivo: Nomenclatura de fluxos incorreta (gap MENOR mas BLOQUEANTE)
```

---

### 🚨 GAPS "MENORES" QUE REPROVAM

**ATENÇÃO:** A partir de agora, os seguintes gaps classificados como "MENOR" **REPROVAM** o RF:

1. **Nomenclatura de Fluxos Incorreta** (FA-001 vs FA-UC00-001)
   - Severidade antiga: MENOR
   - Severidade nova: **BLOQUEANTE**
   - Motivo: Quebra rastreabilidade automática, inconsistência com RF002/RF071

2. **Falta de RN-UC Específicas**
   - Severidade antiga: MENOR
   - Severidade nova: **BLOQUEANTE** (se recorrente em múltiplos UCs)
   - Motivo: Boas práticas de documentação

3. **Arquivo Diagnóstico Ausente**
   - Severidade antiga: MENOR
   - Severidade nova: **ADVERTÊNCIA** (não reprova sozinho, mas deve ser criado)

---

### ⚠️ ÚNICA EXCEÇÃO: Falhas Técnicas Python

**Aprovação condicional permitida SOMENTE se:**
```
11/12 PASS (faltou apenas Validação #10: Validador Automático)
0 gaps CRÍTICOS
0 gaps IMPORTANTES
0 gaps MENORES
Validação #10 falhou por: Erro técnico Python (timeout, script quebrado, etc.)
Análise manual confirma 100% cobertura RN → UC
```

**Neste caso:**
```
Veredicto: ⚠️ APROVADO COM RESSALVA TÉCNICA
Ação: Investigar/corrigir validador Python, mas RF pode prosseguir
```

**Todos os outros casos:**
```
Veredicto: ❌ REPROVADO
Ação: Reexecutar CONTRATO-ADEQUACAO-COMPLETA-UC novamente
```

---

## MODO DE EXECUÇÃO

**Prompt de ativação:**
```
Executar VALIDADOR-CONTRATO-ADEQUACAO-COMPLETA-UC para RFXXX.
Seguir CLAUDE.md.
```

**Comportamento esperado:**
1. Leitura de RF.yaml, UC.yaml, UC.md, STATUS.yaml
2. Execução das 12 validações
3. Geração de relatório de gaps (se houver)
4. Veredicto final: APROVADO, APROVADO COM RESSALVAS, ou REPROVADO
5. Salvar relatório em `.temp_ia/validacao-uc-RFXXX-relatorio.md`

**IMPORTANTE:** Este validador NÃO corrige problemas, apenas IDENTIFICA.

---

**Fim do Validador**

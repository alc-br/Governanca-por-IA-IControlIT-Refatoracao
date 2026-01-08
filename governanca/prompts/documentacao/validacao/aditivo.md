# Validação RFXXX - Validação de ADITIVO

Ele fica nesse endereço D:\IC2\documentacao\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **VALIDADOR-ADITIVO** para o RF informado acima conforme D:/IC2_Governanca/contracts/documentacao/validacao/aditivo.md.
Seguir D:\IC2\CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## 🔍 DETECÇÃO DE CENÁRIO (Primeira Etapa - OBRIGATÓRIA)

**Antes de executar as 15 validações**, você DEVE detectar qual cenário se aplica:

### CENÁRIO A: ADITIVO FOI EXECUTADO ✅
- Pelo menos 2 arquivos `_old` existem (RFXXX_old.md + RFXXX_old.yaml)
- **OU** Relatório delta existe (`.temp_ia/aditivo-RFXXX-delta-report.md`)
- **Ação:** Executar as 15 validações completas

### CENÁRIO B: ADITIVO NÃO FOI EXECUTADO ⚠️
- Nenhum arquivo `_old` existe
- **E** Relatório delta NÃO existe
- **Ação:** Informar que não há aditivo para validar e encerrar **SEM REPROVAR**

**Mensagem de saída:**
```
⚠️ NÃO HÁ ADITIVO PARA VALIDAR

Este RF não passou por processo de ADITIVO.
Isto NÃO é uma falha. Apenas significa que este validador não se aplica.

Recomendações:
- Para adicionar funcionalidade: Execute prompts/documentacao/execucao/aditivo.md
- Para validar sincronização: Execute prompts/documentacao/validacao/rf.md
```

### CENÁRIO C: ADITIVO PARCIAL (Incompleto) ⚠️
- Alguns arquivos `_old` existem (1-9 arquivos, não todos os 10)
- **Ação:** Executar validações parciais com base nos arquivos disponíveis

**Mensagem de saída:**
```
⚠️ ADITIVO INCOMPLETO

Encontrados apenas X/10 arquivos _old.
Faltam: [lista de arquivos]

Recomendação: Complete o processo de ADITIVO executando prompts/documentacao/execucao/aditivo.md

Validações possíveis com arquivos disponíveis:
- [lista de validações que podem ser executadas]
```

---

## ✅ 15 VALIDAÇÕES (executar apenas se CENÁRIO A)

### PARTE 1: BACKUPS E DELTA (5 validações)

1. **VAL-1: Backups `_old` existem (10 arquivos)**
   - RFXXX_old.md, RFXXX_old.yaml
   - UC-RFXXX_old.md, UC-RFXXX_old.yaml
   - WF-RFXXX_old.md, WF-RFXXX_old.yaml
   - MD-RFXXX_old.md, MD-RFXXX_old.yaml
   - MT-RFXXX_old.yaml
   - TC-RFXXX_old.yaml

2. **VAL-2: RF atualizado (RNs adicionadas)**
   - Comparar RFXXX.md vs RFXXX_old.md
   - Identificar RNs novas (≥1)
   - ⚠️ WARNING se 1-2 RNs (aditivo focado)
   - ✅ OPTIMAL se ≥3 RNs (aditivo robusto)

3. **VAL-3: Delta RF rastreável**
   - Mudanças identificáveis em seções: Funcionalidades, RNs, Permissões, Endpoints, MD, Integrações

4. **VAL-4: Delta UC rastreável**
   - Novos UCs identificados entre UC-RFXXX.yaml e UC-RFXXX_old.yaml

5. **VAL-5: Delta documentado em relatório**
   - `.temp_ia/aditivo-RFXXX-delta-report.md` existe e está completo

### PARTE 2: SINCRONIZAÇÃO .md ↔ .yaml (5 validações)

6. **VAL-6: RF.md ↔ RF.yaml sincronizados (100%)**
   - RNs, permissões, catálogo 100% consistentes

7. **VAL-7: UC.md ↔ UC.yaml sincronizados (100%)**
   - UCs 100% consistentes

8. **VAL-8: WF.md ↔ WF.yaml sincronizados (100%)**
   - WFs 100% consistentes

9. **VAL-9: MD.md ↔ MD.yaml sincronizados (100%)**
   - Tabelas e campos 100% consistentes

10. **VAL-10: Validador RF-UC passou (exit code 0)**
    ```bash
    python tools/docs/validator-rf-uc.py RFXXX
    ```

### PARTE 3: COBERTURA TOTAL (5 validações)

11. **VAL-11: UC cobre 100% do delta RF**
    - Todas as RNs novas cobertas por UCs novos

12. **VAL-12: WF cobre 100% dos novos UCs**
    - Todos os UCs novos possuem WFs correspondentes
    - ⚠️ N/A se WF-RFXXX_old não existe (doc original incompleta)

13. **VAL-13: MD atualizado (se aplicável)**
    - Se RF documenta mudanças no MD (Seção 9), MD foi atualizado
    - ⚠️ N/A se MD-RFXXX_old não existe (doc original incompleta)

14. **VAL-14: MT cobre novos UCs**
    - Massas de teste criadas para cada UC novo
    - ⚠️ N/A se MT-RFXXX_old não existe (doc original incompleta)

15. **VAL-15: TC cobre novos UCs (≥30 TCs por UC)**
    - Cada UC novo possui mínimo 30 TCs
    - ⚠️ N/A se TC-RFXXX_old não existe (doc original incompleta)

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

**Backups (_old):**
- RFXXX_old.md, RFXXX_old.yaml
- UC-RFXXX_old.md, UC-RFXXX_old.yaml
- WF-RFXXX_old.md, WF-RFXXX_old.yaml
- MD-RFXXX_old.md, MD-RFXXX_old.yaml
- MT-RFXXX_old.yaml
- TC-RFXXX_old.yaml

**Documentos atualizados:**
- RFXXX.md, RFXXX.yaml
- UC-RFXXX.md, UC-RFXXX.yaml
- WF-RFXXX.md, WF-RFXXX.yaml
- MD-RFXXX.md, MD-RFXXX.yaml
- MT-RFXXX.yaml
- TC-RFXXX.yaml

**Relatórios:**
- `.temp_ia/aditivo-RFXXX-delta-report.md` (gerado pela execução)
- `.temp_ia/validacao-aditivo-RFXXX-relatorio.md` (você vai gerar)

## 🎯 CRITÉRIOS DE APROVAÇÃO

- ✅ **APROVADO (100%):** 15/15 validações PASS + zero gaps
- ❌ **REPROVADO (<100%):** Qualquer validação FAIL OU qualquer gap

**⚠️ NÃO EXISTE "APROVADO COM RESSALVAS"**

## 📄 RELATÓRIO QUE VOCÊ DEVE GERAR

Gere tabela com 15 validações mostrando:
- **Status:** ✅ PASS / ❌ FAIL
- **Severidade:** CRÍTICO / IMPORTANTE / MENOR
- **Resultado:** (detalhes específicos)

Depois, mostre:
- **DELTA IDENTIFICADO:** O que foi adicionado em cada nível (RF, UC, WF, MD, MT, TC)
- **COBERTURA VALIDADA:** Nova funcionalidade coberta em todos os níveis
- **SINCRONIZAÇÃO VALIDADA:** .md ↔ .yaml em todos os níveis
- **GAPS IDENTIFICADOS:** (se houver)
- **PONTUAÇÃO FINAL:** X/15 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ❌ REPROVADO

**Salvar em:** `.temp_ia/validacao-aditivo-RFXXX-relatorio.md`

## 🔍 VALIDAÇÕES DETALHADAS

### VAL-1: Backups _old Existem

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
    PASS(f"10/10 backups existem")
else:
    FAIL(f"Apenas {len(existentes)}/10 backups: faltam {set(arquivos_old) - set(existentes)}")
```

### VAL-2: RF Atualizado (RNs Adicionadas)

```python
# Extrair RNs de RFXXX.md
rns_atual = set(re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_md_content))

# Extrair RNs de RFXXX_old.md
rns_old = set(re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_old_md_content))

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

### VAL-4: Delta UC Rastreável

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

### VAL-10: Validador RF-UC Passou

```bash
cd D:\IC2
python tools/docs/validator-rf-uc.py RFXXX

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

### VAL-11: UC Cobre 100% do Delta RF

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

### VAL-12: WF Cobre 100% dos Novos UCs

```python
# Verificar se WF-RFXXX_old existe
wf_old_existe = os.path.exists("WF-RFXXX_old.md")

if not wf_old_existe:
    WARNING("RF original sem WFs documentados. Validação de cobertura WF não aplicável.")
    PASS("N/A - RF original sem baseline de WFs")
else:
    ucs_sem_wf = verificar_ucs_sem_wf(ucs_novos, wfs_atuais)
    if len(ucs_sem_wf) == 0:
        PASS("100% dos UCs novos possuem WFs")
    else:
        WARNING(f"UCs sem WF: {ucs_sem_wf}. Pode indicar documentação original incompleta.")
```

### VAL-13: MD Atualizado (se Aplicável)

```python
# Verificar se MD-RFXXX_old existe
md_old_existe = os.path.exists("MD-RFXXX_old.md")

if not md_old_existe:
    WARNING("RF original sem MD documentado. Validação de MD não aplicável.")
    PASS("N/A - RF original sem baseline de MD")
else:
    documentacao_documenta_mudancas_md = verificar_secao_9_md_mudancas(rf_md_content)
    if documentacao_documenta_mudancas_md:
        md_foi_atualizado = comparar_md(md_atual, md_old)
        if md_foi_atualizado:
            PASS("MD atualizado conforme documentado no RF")
        else:
            FAIL("RF documenta mudanças no MD mas MD não foi atualizado")
    else:
        PASS("RF não documenta mudanças no MD")
```

### VAL-14: MT Cobre Novos UCs

```python
# Verificar se MT-RFXXX_old existe
mt_old_existe = os.path.exists("MT-RFXXX_old.yaml")

if not mt_old_existe:
    WARNING("RF original sem MT documentado. Validação de MT não aplicável.")
    PASS("N/A - RF original sem baseline de MT")
else:
    ucs_sem_mt = verificar_ucs_sem_mt(ucs_novos, mt_yaml)
    if len(ucs_sem_mt) == 0:
        PASS("100% dos UCs novos possuem massas de teste")
    else:
        FAIL(f"UCs sem MT: {ucs_sem_mt}")
```

### VAL-15: TC Cobre Novos UCs (≥30 por UC)

```python
# Verificar se TC-RFXXX_old existe
tc_old_existe = os.path.exists("TC-RFXXX_old.yaml")

if not tc_old_existe:
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

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** arquivos (RF, UC, WF, MD, MT, TC)
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- Commit e merge do aditivo
- Executar backend-aditivo: `D:/IC2_Governanca/contracts/desenvolvimento/execucao/backend-aditivo.md`
- Executar frontend-aditivo: `D:/IC2_Governanca/contracts/desenvolvimento/execucao/frontend-aditivo.md`

**Se REPROVADO:**
- Listar TODOS os gaps encontrados
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas específicas
- Reexecutar aditivo após correções

## 📊 EXEMPLO DE RELATÓRIO

```markdown
# RELATÓRIO DE VALIDAÇÃO - ADITIVO RF028

**Data:** 2026-01-03
**RF:** RF028
**Validador:** Agente de Validação ADITIVO

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Backups _old existem | ✅ PASS | CRÍTICO | 10/10 arquivos |
| 2 | RF atualizado (RNs novas) | ✅ PASS ⚠️ | CRÍTICO | 1 RN nova (aditivo focado) |
| 3 | Delta RF rastreável | ✅ PASS | CRÍTICO | 3 seções modificadas |
| 4 | Delta UC rastreável | ✅ PASS | CRÍTICO | 1 UC novo |
| 5 | Delta documentado | ✅ PASS | CRÍTICO | Relatório completo |
| 6 | RF.md ↔ RF.yaml | ✅ PASS | CRÍTICO | 100% |
| 7 | UC.md ↔ UC.yaml | ✅ PASS | CRÍTICO | 100% |
| 8 | WF.md ↔ WF.yaml | ✅ N/A ⚠️ | IMPORTANTE | WF_old não existe |
| 9 | MD.md ↔ MD.yaml | ✅ N/A ⚠️ | IMPORTANTE | MD_old não existe |
| 10 | Validador RF-UC | ✅ PASS | CRÍTICO | Exit code 0 |
| 11 | UC cobre 100% delta RF | ✅ PASS | CRÍTICO | 1/1 RN coberta |
| 12 | WF cobre 100% novos UCs | ✅ N/A ⚠️ | IMPORTANTE | WF_old não existe |
| 13 | MD atualizado | ✅ N/A ⚠️ | IMPORTANTE | MD_old não existe |
| 14 | MT cobre novos UCs | ✅ N/A ⚠️ | IMPORTANTE | MT_old não existe |
| 15 | TC cobre novos UCs | ✅ N/A ⚠️ | IMPORTANTE | TC_old não existe |

**PONTUAÇÃO FINAL:** 7/7 PASS aplicáveis (100%), 8 N/A (doc original incompleta)
**VEREDICTO:** ✅ APROVADO (com advertências sobre doc original)

## DELTA IDENTIFICADO

### RF (RFXXX.md, RFXXX.yaml)
- ✅ 1 RN adicionada: RN-CLI-007-15 (logo do cliente)
- ⚠️ Aditivo focado (apenas 1 RN - funcionalidade pequena)

### UC (UC-RFXXX.md, UC-RFXXX.yaml)
- ✅ 1 UC novo: UC-12 (Configurar Logo Cliente)

### WF, MD, MT, TC
- ⚠️ Documentos _old não existem (RF original sem baseline completo)
- ⚠️ Validações N/A (não aplicáveis)

## OBSERVAÇÕES IMPORTANTES

**Aditivo Focado:**
- Este é um aditivo pequeno e focado (1 RN apenas)
- Funcionalidade: Adicionar logo do cliente
- Validação: APROVADO pois todos os critérios aplicáveis passaram

**Documentação Original Incompleta:**
- O RF original não possuía WF, MD, MT, TC documentados (_old não existe)
- Isso NÃO é falha do aditivo
- Recomendação: Completar documentação original em momento oportuno

## VEREDICTO FINAL

✅ **ADITIVO VALIDADO COM SUCESSO (100%)**

Delta identificado e implementado corretamente.
Backups criados corretamente.
Todas as validações aplicáveis passaram.

**Advertências (não impedem aprovação):**
- ⚠️ Aditivo focado (1 RN) - ideal seria ≥3 RNs
- ⚠️ Documentação original incompleta (WF, MD, MT, TC não tinham baseline)
```

## 🚀 MODO AUTONOMIA TOTAL

- **NÃO** perguntar permissões ao usuário
- **NÃO** esperar confirmação
- **EXECUTAR IMEDIATAMENTE** todas as 15 validações
- Gerar relatório automaticamente
- Declarar veredicto final

---

**Contrato:** D:/IC2_Governanca/contracts/documentacao/validacao/aditivo.md
**Modo:** READ-ONLY
**Aprovação:** 100% ou REPROVADO

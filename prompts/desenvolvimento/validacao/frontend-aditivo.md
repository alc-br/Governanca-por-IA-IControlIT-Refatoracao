# Validação Frontend Aditivo RFXXX

Ele fica nesse endereço D:\IC2\rf\Fase*\EPIC*\RF*

**Instruções:** Altere RFXXX acima para o RF desejado (ex: RF001, RF025, RF028).

---

Executar **VALIDADOR FRONTEND ADITIVO** para o RF informado acima conforme D:/IC2_Governanca/contracts/desenvolvimento/validacao/frontend-aditivo.md.
Seguir D:\IC2\CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 10 VALIDAÇÕES (executar todas)

### PARTE 1: DELTA IMPLEMENTADO (5 validações)

1. **VAL-1: Services criados/atualizados (para novos endpoints)**
   - Comparar RF.md vs RF_old.md (identificar novos endpoints)
   - Verificar Services em `src/app/core/services/`

2. **VAL-2: Components criados (para cada WF novo)**
   - Comparar WF-RFXXX.yaml vs WF-RFXXX_old.yaml (identificar novos WFs)
   - Verificar Components em `src/app/features/`

3. **VAL-3: Routes adicionadas (em `app.routes.ts`)**
   - Verificar rotas em `src/app/app.routes.ts`
   - Confirmar que novas rotas existem

4. **VAL-4: Forms criados (com validações de RNs)**
   - Verificar formulários nos componentes
   - Confirmar validações das RNs novas

5. **VAL-5: i18n atualizado (chaves em `pt.json`, `en.json`)**
   - Comparar RF.md vs RF_old.md (identificar chaves i18n)
   - Verificar `src/assets/i18n/pt.json` e `en.json`

### PARTE 2: QUALIDADE E TESTES (5 validações)

6. **VAL-6: Permissões aplicadas (`*ixHasPermission` nos componentes)**
   - Verificar uso de `*ixHasPermission` nos templates HTML

7. **VAL-7: Responsividade (Mobile, Tablet, Desktop nos WFs novos)**
   - Verificar CSS/SCSS dos componentes novos
   - Confirmar media queries (se aplicável)

8. **VAL-8: Testes criados (Jasmine/Karma para novos componentes)**
   - Verificar testes em `src/app/features/**/*.spec.ts`

9. **VAL-9: Build PASS**
   ```bash
   cd frontend/icontrolit-app
   npm run build
   ```
   Exit code 0 = PASS

10. **VAL-10: Tests PASS**
    ```bash
    npm run test
    ```
    Exit code 0 = PASS

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

**Documentos delta:**
- RFXXX.md vs RFXXX_old.md
- WF-RFXXX.yaml vs WF-RFXXX_old.yaml
- UC-RFXXX.yaml vs UC-RFXXX_old.yaml

**Relatórios:**
- `.temp_ia/aditivo-RFXXX-delta-report.md`
- `.temp_ia/backend-aditivo-RFXXX-relatorio.md`
- `.temp_ia/frontend-aditivo-RFXXX-relatorio.md`

**Código frontend:**
- `src/app/core/services/` (Services)
- `src/app/features/` (Components)
- `src/app/app.routes.ts` (Routes)
- `src/assets/i18n/pt.json`, `en.json` (i18n)
- `src/app/features/**/*.spec.ts` (Testes)

**Relatório de validação (você vai gerar):**
- `.temp_ia/validacao-frontend-aditivo-RFXXX-relatorio.md`

## 🎯 CRITÉRIOS DE APROVAÇÃO

- ✅ **APROVADO:** 10/10 validações PASS
- ❌ **REPROVADO:** Qualquer validação FAIL

## 📄 RELATÓRIO QUE VOCÊ DEVE GERAR

Gere tabela com 10 validações mostrando:
- **Status:** ✅ PASS / ❌ FAIL
- **Severidade:** CRÍTICO / IMPORTANTE / MENOR
- **Resultado:** (detalhes específicos)

Depois, mostre:
- **DELTA VALIDADO:** O que foi implementado vs o que era esperado
- **GAPS IDENTIFICADOS:** (se houver)
- **PONTUAÇÃO FINAL:** X/10 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ❌ REPROVADO

**Salvar em:** `.temp_ia/validacao-frontend-aditivo-RFXXX-relatorio.md`

## 🔍 VALIDAÇÕES DETALHADAS

### VAL-1: Services

```python
# Identificar novos endpoints no delta
endpoints_delta = identificar_novos_endpoints(RF_md, RF_old_md)

# Verificar se services existem
for endpoint in endpoints_delta:
    service_name = inferir_service_name(endpoint)
    if not file_exists(f"src/app/core/services/{service_name}.service.ts"):
        FAIL(f"Service {service_name} não criado")

PASS(f"{len(endpoints_delta)}/{len(endpoints_delta)} services criados")
```

### VAL-2: Components

```python
# Identificar novos WFs no delta
wfs_delta = identificar_novos_wfs(WF_yaml, WF_old_yaml)

# Verificar se components existem
for wf in wfs_delta:
    component_name = inferir_component_name(wf)
    if not file_exists(f"src/app/features/**/{component_name}.component.ts"):
        FAIL(f"Component {component_name} não criado")

PASS(f"{len(wfs_delta)}/{len(wfs_delta)} components criados")
```

### VAL-5: i18n

```python
# Identificar novas chaves i18n no delta
chaves_delta = identificar_novas_chaves_i18n(RF_md, RF_old_md)

# Verificar se chaves existem em pt.json e en.json
pt_json = read_json("src/assets/i18n/pt.json")
en_json = read_json("src/assets/i18n/en.json")

chaves_faltantes_pt = []
chaves_faltantes_en = []

for chave in chaves_delta:
    if not verificar_chave_existe(pt_json, chave):
        chaves_faltantes_pt.append(chave)
    if not verificar_chave_existe(en_json, chave):
        chaves_faltantes_en.append(chave)

if chaves_faltantes_pt or chaves_faltantes_en:
    FAIL(f"Chaves faltantes: PT={chaves_faltantes_pt}, EN={chaves_faltantes_en}")
else:
    PASS(f"{len(chaves_delta)}/{len(chaves_delta)} chaves i18n adicionadas")
```

### VAL-6: Permissões

```python
# Verificar se *ixHasPermission está aplicado nos componentes novos
for component in components_novos:
    html_file = f"{component.path}/{component.name}.component.html"
    html_content = read_file(html_file)

    if "*ixHasPermission" not in html_content:
        FAIL(f"{component.name}: permissão não aplicada")

PASS("Permissões aplicadas em todos os componentes novos")
```

### VAL-9: Build PASS

```bash
cd frontend/icontrolit-app
npm run build

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

### VAL-10: Tests PASS

```bash
npm run test

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** código frontend
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- Commit e merge do aditivo completo
- Executar testes E2E completos

**Se REPROVADO:**
- Listar TODOS os gaps encontrados
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas específicas
- Reexecutar frontend-aditivo após correções

## 📊 EXEMPLO DE RELATÓRIO

```markdown
# RELATÓRIO VALIDAÇÃO - FRONTEND ADITIVO RF028

**Data:** 2026-01-03
**RF:** RF028
**Validador:** Agente de Validação Frontend Aditivo

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | Services | ✅ PASS | CRÍTICO | 1/1 criado |
| 2 | Components | ✅ PASS | CRÍTICO | 1/1 criado |
| 3 | Routes | ✅ PASS | CRÍTICO | 1/1 adicionada |
| 4 | Forms | ✅ PASS | IMPORTANTE | 1/1 criado |
| 5 | i18n | ✅ PASS | IMPORTANTE | 5/5 chaves |
| 6 | Permissões | ✅ PASS | CRÍTICO | 1/1 aplicada |
| 7 | Responsividade | ✅ PASS | IMPORTANTE | M/T/D |
| 8 | Testes | ✅ PASS | IMPORTANTE | 12/12 criados |
| 9 | Build | ✅ PASS | CRÍTICO | 0 erros |
| 10 | Tests | ✅ PASS | CRÍTICO | 12/12 PASS |

**PONTUAÇÃO FINAL:** 10/10 PASS (100%)
**VEREDICTO:** ✅ APROVADO

## DELTA VALIDADO

**Esperado (delta docs):**
- 1 WF novo: WF-12 (Tela de Exportação PDF)
- 1 endpoint: GET /api/v1/clientes/export/pdf
- 5 chaves i18n
- 1 permissão: cliente.export_pdf

**Implementado (frontend):**
- ✅ ClienteExportacaoService
- ✅ ClienteExportacaoPdfComponent
- ✅ Route: /clientes/exportar-pdf
- ✅ Formulário com validações
- ✅ 5 chaves i18n (pt.json, en.json)
- ✅ *ixHasPermission="'cliente.export_pdf'"
- ✅ Responsividade (M/T/D)
- ✅ 12 testes

## GAPS IDENTIFICADOS

Nenhum gap identificado.

## VEREDICTO FINAL

✅ **FRONTEND ADITIVO VALIDADO COM SUCESSO (100%)**
```

## 🚀 MODO AUTONOMIA TOTAL

- **NÃO** perguntar permissões ao usuário
- **NÃO** esperar confirmação
- **EXECUTAR IMEDIATAMENTE** todas as 10 validações
- Gerar relatório automaticamente
- Declarar veredicto final

---

**Contrato:** D:/IC2_Governanca/contracts/desenvolvimento/validacao/frontend-aditivo.md
**Modo:** READ-ONLY
**Aprovação:** 10/10 PASS ou REPROVADO

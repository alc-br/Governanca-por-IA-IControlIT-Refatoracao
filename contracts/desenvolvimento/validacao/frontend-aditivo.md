# CONTRATO DE VALIDAÇÃO — FRONTEND ADITIVO

**Versão:** 1.0 | **Data:** 2026-01-03 | **Status:** Ativo

## Sumário

Valida que o frontend foi atualizado corretamente conforme ADITIVO de documentação (WF, UC).

**Modo:** READ-ONLY (identifica gaps, não corrige)
**Entrada:** Relatórios de delta (docs + frontend)
**Saída:** `.temp_ia/validacao-frontend-aditivo-RFXXX-relatorio.md`

## Ativação

```
Conforme docs/contracts/desenvolvimento/validacao/frontend-aditivo.md para RFXXX.
```

## Validações (10 obrigatórias)

### PARTE 1: DELTA IMPLEMENTADO (5 validações)

1. **Services criados/atualizados** (para novos endpoints)
2. **Components criados** (para cada WF novo)
3. **Routes adicionadas** (em `app.routes.ts`)
4. **Forms criados** (com validações de RNs)
5. **i18n atualizado** (chaves em `pt.json`, `en.json`)

### PARTE 2: QUALIDADE E TESTES (5 validações)

6. **Permissões aplicadas** (`*ixHasPermission` nos componentes)
7. **Responsividade** (Mobile, Tablet, Desktop nos WFs novos)
8. **Testes criados** (Jasmine/Karma para novos componentes)
9. **Build PASS** (`npm run build`)
10. **Tests PASS** (`npm run test`)

## Como Validar

```python
# VAL-1: Services
endpoints_delta = identificar_novos_endpoints(RF_md, RF_old_md)
services_criados = verificar_services(endpoints_delta)

# VAL-2: Components
wfs_delta = identificar_novos_wfs(WF_yaml, WF_old_yaml)
components_criados = verificar_components(wfs_delta)

# VAL-5: i18n
chaves_delta = identificar_novas_chaves_i18n(RF_md, RF_old_md)
chaves_implementadas = verificar_i18n_files(chaves_delta)

# VAL-9: Build
resultado_build = executar_npm_build()

# VAL-10: Tests
resultado_tests = executar_npm_test()
```

## Critérios de Aprovação

✅ **APROVADO:** 10/10 validações PASS
❌ **REPROVADO:** Qualquer validação FAIL

## Relatório

```markdown
# RELATÓRIO VALIDAÇÃO - FRONTEND ADITIVO RFXXX

| # | Validação | Status | Resultado |
|---|-----------|--------|-----------|
| 1 | Services | ✅ PASS | 1/1 criado |
| 2 | Components | ✅ PASS | 1/1 criado |
| 3 | Routes | ✅ PASS | 1/1 adicionada |
| 4 | Forms | ✅ PASS | 1/1 criado |
| 5 | i18n | ✅ PASS | 5/5 chaves |
| 6 | Permissões | ✅ PASS | 1/1 aplicada |
| 7 | Responsividade | ✅ PASS | M/T/D |
| 8 | Testes | ✅ PASS | 12/12 criados |
| 9 | Build | ✅ PASS | 0 erros |
| 10 | Tests | ✅ PASS | 12/12 PASS |

**PONTUAÇÃO:** 10/10 PASS (100%)
**VEREDICTO:** ✅ APROVADO
```

---

**Versão:** 1.0 | **Mantido por:** Time IControlIT | **Governado por:** CLAUDE.md

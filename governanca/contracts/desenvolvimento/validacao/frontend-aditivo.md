# CONTRATO DE VALIDAÇÃO — FRONTEND ADITIVO

**Versão:** 1.0 | **Data:** 2026-01-03 | **Status:** Ativo

## Sumário

Valida que o frontend foi atualizado corretamente conforme ADITIVO de documentação (WF, UC).

**Modo:** READ-ONLY (identifica gaps, não corrige)
**Entrada:** Relatórios de delta (docs + frontend)
**Saída:** `.temp_ia/validacao-frontend-aditivo-RFXXX-relatorio.md`

## Ativação

```
Conforme contracts/desenvolvimento/validacao/frontend-aditivo.md para RFXXX.
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

## Git Operations (SOMENTE SE APROVADO 100% SEM RESSALVAS)

**Versão:** 1.0
**Data:** 2026-01-28

### Regra Fundamental

**SE E SOMENTE SE:**
1. ✅ Validação passou **100%** (10/10 PASS)
2. ✅ **ZERO** ressalvas ou gaps
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
    git commit -m "feat(RFXXX): frontend aditivo validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): frontend aditivo validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. Frontend aditivo mergeado em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer ressalva ou observação
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**Versão:** 1.0 | **Mantido por:** Time IControlIT | **Governado por:** D:\IC2\CLAUDE.md

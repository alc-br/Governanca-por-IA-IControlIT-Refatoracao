# CONTRATO DE VALIDAÇÃO — BACKEND ADITIVO

**Versão:** 1.0 | **Data:** 2026-01-03 | **Status:** Ativo

## Sumário

Valida que o backend foi atualizado corretamente conforme ADITIVO de documentação.

**Modo:** READ-ONLY (identifica gaps, não corrige)
**Entrada:** Relatórios de delta (docs + backend)
**Saída:** `.temp_ia/validacao-backend-aditivo-RFXXX-relatorio.md`

## Ativação

```
Conforme contracts/desenvolvimento/validacao/backend-aditivo.md para RFXXX.
```

## Validações (10 obrigatórias)

### PARTE 1: DELTA IMPLEMENTADO (5 validações)

1. **Entities criadas/atualizadas** (se MD mudou)
2. **Migrations criadas/aplicadas** (se MD mudou)
3. **Commands/Queries criados** (para cada novo endpoint)
4. **Handlers criados** (com validação de RNs novas)
5. **Endpoints adicionados** (Controllers atualizados)

### PARTE 2: QUALIDADE E TESTES (5 validações)

6. **RNs validadas nos Handlers** (todas as RNs novas do delta)
7. **Permissões aplicadas** (Authorization nos endpoints)
8. **Testes criados** (para novos Commands/Queries/Handlers)
9. **Build PASS** (`dotnet build`)
10. **Tests PASS** (`dotnet test`)

## Como Validar

```python
# VAL-1: Entities
entities_delta = identificar_novas_tabelas(MD_yaml, MD_old_yaml)
entities_implementadas = verificar_entities_existem(entities_delta)

# VAL-3: Commands/Queries
endpoints_delta = identificar_novos_endpoints(RF_md, RF_old_md)
commands_queries_criados = verificar_commands_queries(endpoints_delta)

# VAL-6: RNs validadas
rns_delta = identificar_novas_rns(RF_md, RF_old_md)
rns_validadas_handlers = verificar_rns_em_handlers(rns_delta)

# VAL-9: Build
resultado_build = executar_dotnet_build()

# VAL-10: Tests
resultado_tests = executar_dotnet_test()
```

## Critérios de Aprovação

✅ **APROVADO:** 10/10 validações PASS
❌ **REPROVADO:** Qualquer validação FAIL

## Relatório

```markdown
# RELATÓRIO VALIDAÇÃO - BACKEND ADITIVO RFXXX

| # | Validação | Status | Resultado |
|---|-----------|--------|-----------|
| 1 | Entities | ✅ PASS | 1/1 criada |
| 2 | Migrations | ✅ PASS | 1/1 aplicada |
| 3 | Commands/Queries | ✅ PASS | 1/1 criado |
| 4 | Handlers | ✅ PASS | 1/1 criado |
| 5 | Endpoints | ✅ PASS | 1/1 adicionado |
| 6 | RNs validadas | ✅ PASS | 3/3 RNs |
| 7 | Permissões | ✅ PASS | 1/1 aplicada |
| 8 | Testes criados | ✅ PASS | 15/15 testes |
| 9 | Build | ✅ PASS | 0 erros |
| 10 | Tests | ✅ PASS | 15/15 PASS |

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
    git commit -m "feat(RFXXX): backend aditivo validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): backend aditivo validado 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. Backend aditivo mergeado em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer ressalva ou observação
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**Versão:** 1.0 | **Mantido por:** Time IControlIT | **Governado por:** D:\IC2\CLAUDE.md

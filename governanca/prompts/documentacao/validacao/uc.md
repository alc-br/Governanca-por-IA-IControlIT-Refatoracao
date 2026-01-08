# Validação de UC do RFXXX - Validação de Adequação UC

Ele fica nesse endereço D:\IC2\documentacao\Fase*\EPIC*\RF*

---

Executar **D:\IC2_Governanca\contracts\documentacao\validacao\uc.md** para o RF informado acima.
Seguir D:\IC2\CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 12 VALIDAÇÕES (executar todas)

1. **Cobertura RN → UC:** 100% das RNs cobertas?
2. **Nomenclatura padrão:** 100% no formato oficial?
3. **Catálogo limpo:** Zero códigos híbridos?
4. **UC.yaml → Template:** 100% conforme v2.0?
5. **UC.md → Template:** 100% formato narrativo?
6. **UC.yaml ↔ UC.md:** 100% sincronizados?
7. **Jobs background:** Todos documentados?
8. **Workflows:** Todos documentados?
9. **Integrações externas:** Completas?
10. **Validador automático:** Exit code 0?
11. **STATUS.yaml:** Seção `adequacao_uc` presente?
12. **STATUS.yaml:** `documentacao.uc = true`?

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

- RF.yaml (fonte da verdade)
- UC-[RF].yaml (validar)
- UC-[RF].md (validar)
- STATUS.yaml (verificar seções adequacao_uc e documentacao.uc)

## 🎯 CRITÉRIOS DE APROVAÇÃO (v3.0)

- ✅ **APROVADO:** 12/12 validações PASS + ZERO gaps CRÍTICOS + ZERO gaps IMPORTANTES
- ✅ **APROVADO COM ADVERTÊNCIA:** 12/12 PASS + ZERO CRÍTICOS + ZERO IMPORTANTES + gaps MENORES
- ❌ **REPROVADO:** Qualquer FAIL OU gap CRÍTICO OU gap IMPORTANTE

**Gaps MENORES NÃO reprovam** (apenas advertem).

## 📄 RELATÓRIO QUE VOCÊ DEVE EXIBIR NA TELA

Gere tabela com 12 validações mostrando:
- Status (✅ PASS / ❌ FAIL / N/A)
- Severidade (CRÍTICO / IMPORTANTE / MENOR)
- Resultado (X/Y, percentual, códigos encontrados, etc.)

Depois, mostre:
- **PONTUAÇÃO FINAL:** X/12 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ✅ APROVADO COM ADVERTÊNCIA / ❌ REPROVADO

Se houver gaps, liste:
- Descrição do gap
- Severidade (CRÍTICO, IMPORTANTE, MENOR)
- Arquivo/linha afetado
- Recomendação de ação

**NÃO salvar em arquivo** - apenas exibir na tela para o usuário.

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** arquivos (UC.yaml, UC.md, STATUS.yaml)
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- RF pode prosseguir
- Usuário faz Git (commit, merge)

**Se REPROVADO:**
- Reexecutar adequação
- Focar nas validações que falharam
- Validar novamente

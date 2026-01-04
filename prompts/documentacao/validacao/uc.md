# Validação de UC do RFXXX - Validação de Adequação UC

Ele fica nesse endereço \docs\rf\Fase*\EPIC*\RF*

---

Executar **docs\contracts\documentacao\validacao\uc.md** para o RF informado acima.
Seguir CLAUDE.md.

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
12. **Relatório gerado:** Arquivos presentes?

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

- RF.yaml (fonte da verdade)
- UC-[RF].yaml (validar)
- UC-[RF].md (validar)
- STATUS.yaml (verificar seção adequacao_uc)
- `.temp_ia/adequacao-uc-[RF]-diagnostico.md`
- `.temp_ia/adequacao-uc-[RF]-relatorio.md`

## 🎯 CRITÉRIOS DE APROVAÇÃO

- ✅ **APROVADO (100%):** 12/12 validações PASS + zero gaps CRÍTICOS
- ⚠️ **APROVADO COM RESSALVAS (80-99%):** 10-11 PASS + zero CRÍTICOS + 1-3 IMPORTANTES
- ❌ **REPROVADO (<80%):** <10 PASS OU qualquer gap CRÍTICO → reexecutar adequação

## 📄 RELATÓRIO QUE VOCÊ DEVE GERAR

Gere tabela com 12 validações mostrando:
- Status (✅ PASS / ❌ FAIL / N/A)
- Severidade (CRÍTICO / IMPORTANTE / MENOR)
- Resultado (X/Y, percentual, códigos encontrados, etc.)

Depois, mostre:
- **PONTUAÇÃO FINAL:** X/12 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ⚠️ APROVADO COM RESSALVAS / ❌ REPROVADO

Se houver gaps, liste:
- Descrição do gap
- Severidade
- Arquivo/linha afetado
- Recomendação de ação

**Salvar em:** `.temp_ia/validacao-uc-[RF]-relatorio.md`

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

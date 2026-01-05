# Validação de WF do RFXXX - Validação de Wireframes

Ele fica nesse endereço \docs\rf\Fase*\EPIC*\RF*

---

Executar **docs\contracts\documentacao\validacao\wf.md** para o RF informado acima.
Seguir CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 9 VALIDAÇÕES (executar todas)

1. **Arquivo WF.md existe:** WF-RFXXX.md criado?
2. **Cobertura UC → WF:** 100% dos UCs têm WF?
3. **Estados obrigatórios:** Loading, Vazio, Erro, Dados presentes?
4. **Responsividade:** Mobile, Tablet, Desktop documentados?
5. **Acessibilidade:** WCAG AA aplicado?
6. **Seções obrigatórias:** 7/7 presentes?
7. **Mapa de Telas:** Completo com todos os WFs?
8. **Rastreabilidade:** UC ↔ WF documentada?
9. **STATUS.yaml:** `documentacao.wf = true`?

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

- WF-[RF].md (validar) - **APENAS formato NARRATIVO, NÃO existe WF.yaml**
- UC-[RF].yaml (fonte de UCs)
- STATUS.yaml (verificar documentacao.wf)

## 🎯 CRITÉRIOS DE APROVAÇÃO (v3.0)

- ✅ **APROVADO:** 9/9 validações PASS + ZERO gaps CRÍTICOS + ZERO gaps IMPORTANTES
- ✅ **APROVADO COM ADVERTÊNCIA:** 9/9 PASS + ZERO CRÍTICOS + ZERO IMPORTANTES + gaps MENORES
- ❌ **REPROVADO:** Qualquer FAIL OU gap CRÍTICO OU gap IMPORTANTE

**Gaps MENORES NÃO reprovam** (apenas advertem).

## 📄 RELATÓRIO QUE VOCÊ DEVE EXIBIR NA TELA

Gere tabela com 9 validações mostrando:
- Status (✅ PASS / ❌ FAIL / N/A)
- Severidade (CRÍTICO / IMPORTANTE / MENOR)
- Resultado (X/Y, percentual, códigos encontrados, etc.)

Depois, mostre:
- **PONTUAÇÃO FINAL:** X/9 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ✅ APROVADO COM ADVERTÊNCIA / ❌ REPROVADO

Se houver gaps, liste:
- Descrição do gap
- Severidade (CRÍTICO, IMPORTANTE, MENOR)
- Arquivo/linha afetado
- Recomendação de ação

**NÃO salvar em arquivo** - apenas exibir na tela para o usuário.

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** arquivos (WF.yaml, STATUS.yaml)
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- RF pode prosseguir para criação de MD
- Usuário faz Git (commit, merge)

**Se REPROVADO:**
- Reexecutar geração de WF
- Focar nas validações que falharam
- Validar novamente

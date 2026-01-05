# Validação de MD do RFXXX - Validação de Modelo de Dados

Ele fica nesse endereço \docs\rf\Fase*\EPIC*\RF*

---

Executar **docs\contracts\documentacao\validacao\md.md** para o RF informado acima.
Seguir CLAUDE.md.

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 8 VALIDAÇÕES (executar todas)

1. **Derivação RF/UC/WF:** Entidades mapeadas?
2. **Multi-tenancy:** 100% das tabelas com cliente_id/empresa_id?
3. **Auditoria:** 5 campos em 100% das tabelas?
4. **Soft delete:** deleted_at em 100% das tabelas?
5. **Constraints:** PK, FKs, UNIQUE completas?
6. **Índices:** PK, multi-tenancy, performance?
7. **MD.yaml → Template:** 100% aderente?
8. **STATUS.yaml:** `documentacao.md = true`?

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

- MD-[RF].yaml (validar)
- WF-[RF].md (fonte de índices e campos visíveis)
- UC-[RF].yaml (fonte de operações)
- RF-[RF].yaml (fonte de entidades)
- STATUS.yaml (verificar documentacao.md)

## 🎯 CRITÉRIOS DE APROVAÇÃO (v3.0)

- ✅ **APROVADO:** 8/8 validações PASS + ZERO gaps CRÍTICOS + ZERO gaps IMPORTANTES
- ✅ **APROVADO COM ADVERTÊNCIA:** 8/8 PASS + ZERO CRÍTICOS + ZERO IMPORTANTES + gaps MENORES
- ❌ **REPROVADO:** Qualquer FAIL OU gap CRÍTICO OU gap IMPORTANTE

**Gaps MENORES NÃO reprovam** (apenas advertem).

## 📄 RELATÓRIO QUE VOCÊ DEVE EXIBIR NA TELA

Gere tabela com 8 validações mostrando:
- Status (✅ PASS / ❌ FAIL / N/A)
- Severidade (CRÍTICO / IMPORTANTE / MENOR)
- Resultado (X/Y, percentual, códigos encontrados, etc.)

Depois, mostre:
- **PONTUAÇÃO FINAL:** X/8 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ✅ APROVADO COM ADVERTÊNCIA / ❌ REPROVADO

Se houver gaps, liste:
- Descrição do gap
- Severidade (CRÍTICO, IMPORTANTE, MENOR)
- Tabela afetada
- Recomendação de ação

**NÃO salvar em arquivo** - apenas exibir na tela para o usuário.

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** arquivos (MD.yaml, STATUS.yaml)
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- RF pode prosseguir para criação de TC/MT
- Usuário faz Git (commit, merge)

**Se REPROVADO:**
- Reexecutar geração de MD
- Focar nas validações que falharam
- Validar novamente

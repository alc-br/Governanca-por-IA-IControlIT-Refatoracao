---
description: Executar auditoria de conformidade de um RF
allowed-tools: Read, Grep, Task, Write
---

# Auditar RF

Executa auditoria de conformidade entre especificação (RF/UC/MD/WF) e implementação (código).

## Instruções

1. **Pergunte ao usuário:**
   - Qual RF? (ex: RF-028)
   - Escopo? (Backend | Frontend | Completo)

2. **Chamar Agente Auditor**

   **Backend:**
   ```python
   Task(
       subagent_type="conformance-auditor",
       prompt="Auditar backend do RF-XXX conforme CONTRATO-AUDITORIA-CONFORMIDADE",
       description="Auditar backend RF-XXX"
   )
   ```

   **Frontend:**
   ```python
   Task(
       subagent_type="conformance-auditor",
       prompt="Auditar frontend do RF-XXX conforme CONTRATO-AUDITORIA-CONFORMIDADE",
       description="Auditar frontend RF-XXX"
   )
   ```

   **Completo:**
   ```python
   Task(
       subagent_type="conformance-auditor",
       prompt="Auditar RF-XXX completo conforme CONTRATO-AUDITORIA-CONFORMIDADE",
       description="Auditar RF-XXX completo"
   )
   ```

3. **Aguardar Relatório**

   Agente criará:
   ```
   D:\IC2\relatorios\AAAA-MM-DD-RFXXX-[BACKEND|FRONTEND|COMPLETO]-Gaps.md
   ```

4. **Analisar Taxa de Conformidade**

   - **>= 95%:** RF conforme ✅
   - **80-94%:** Gaps importantes ⚠️
   - **< 80%:** Gaps críticos ❌ (BLOQUEANTE)

5. **Informar Resultado**

   **Se conforme:**
   ```
   ✅ RF-XXX CONFORME (98% conformidade)

   📊 Relatório: D:\IC2\relatorios\2025-12-28-RF028-COMPLETO-Gaps.md

   📋 Resumo:
   - Total gaps: 2
   - CRÍTICOS: 0
   - IMPORTANTES: 1
   - MENORES: 1

   🚀 Próximos Passos:
   - Marcar RF como concluído
   - Deploy HOM
   ```

   **Se não conforme:**
   ```
   ❌ RF-XXX NÃO CONFORME (72% conformidade)

   📊 Relatório: D:\IC2\relatorios\2025-12-28-RF015-COMPLETO-Gaps.md

   ❌ Gaps Críticos: 2
   - GAP-BACKEND-001: Campo FlExcluido ausente
   - GAP-FRONTEND-001: Botão Excluir ausente

   ⚠️ Gaps Importantes: 5

   🔧 Ações Necessárias:
   1. Corrigir gaps críticos (CONTRATO-MANUTENCAO)
   2. Re-auditar após correções
   3. Somente com >= 95% pode marcar como concluído
   ```

## Notas

- Auditoria é **READ-ONLY** (não corrige, apenas reporta)
- Correções devem ser feitas sob CONTRATO-MANUTENCAO
- Re-auditar após cada correção até atingir >= 95%

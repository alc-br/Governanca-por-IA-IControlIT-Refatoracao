# Auditar Backend vs Especificação

Auditar conformidade do backend do **RF-XXX** conforme docs/contracts/auditoria/conformidade.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-AUDITORIA-CONFORMIDADE

**Checklist:** docs/checklists/checklist-auditoria-conformidade.yaml

**Agente responsável:** auditor (conformance-auditor)

**Modo:** READ-ONLY (não corrige código)

**Objetivo:**
- Comparar backend implementado vs RF/UC/MD
- Identificar gaps (CRÍTICO, IMPORTANTE, MENOR)
- Gerar relatório de gaps com evidências
- Recomendar contrato para correções

**Output:** `relatorios/AAAA-MM-DD-RFXXX-BACKEND-Gaps.md`

**Importante:**
- Auditoria NÃO corrige, apenas identifica gaps
- Gaps críticos bloqueiam aprovação
- Após auditoria, usar contrato de manutenção para correções

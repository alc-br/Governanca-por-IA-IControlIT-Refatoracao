# Auditar Conformidade Completa (Backend + Frontend)

Auditar conformidade completa do **RF-XXX** conforme docs/contracts/auditoria/conformidade.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-AUDITORIA-CONFORMIDADE

**Checklist:** docs/checklists/checklist-auditoria-conformidade.yaml

**Agente responsável:** auditor (conformance-auditor)

**Modo:** READ-ONLY (não corrige código)

**Objetivo:**
- Comparar backend + frontend vs RF/UC/MD/WF
- Identificar gaps em ambas as camadas
- Gerar relatório consolidado de gaps
- Recomendar contrato para correções

**Output:** `relatorios/AAAA-MM-DD-RFXXX-COMPLETO-Gaps.md`

**Importante:**
- Auditoria NÃO corrige, apenas identifica gaps
- Gaps críticos bloqueiam aprovação
- Após auditoria, usar contrato de manutenção para correções
- Validar integrações Backend ↔ Frontend

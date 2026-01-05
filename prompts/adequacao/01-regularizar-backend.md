# Regularizar Backend Legado

Auditar e adequar backend legado do **RF-XXX** conforme CONTRATO-DE-REGULARIZACAO-DE-BACKEND.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-DE-REGULARIZACAO-DE-BACKEND

**Checklist:** docs/checklists/checklist-regularizacao-backend.yaml

**Agente responsável:** backend-regularizer

**Objetivo:**
- Auditar backend existente
- Identificar divergências em relação ao RF
- Corrigir apenas o necessário para aderência
- Preservar compatibilidade com frontend existente
- Preparar backend para validação pelo Tester-Backend

**Proibições:**
- NÃO criar novas funcionalidades
- NÃO alterar payloads públicos
- NÃO quebrar contratos existentes com frontend
- NÃO refatorar arquitetura
- NÃO endurecer validações que quebrem fluxo existente

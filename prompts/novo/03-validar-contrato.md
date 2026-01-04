# Validar Contrato Backend

Validar backend do **RF-XXX** conforme docs/contracts/testes/tester-backend.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-EXECUCAO-TESTER-BACKEND

**Checklist:** docs/checklists/checklist-tester-backend.yaml

**Agente responsável:** tester (qa-tester)

**Pré-requisitos:**
- Backend implementado
- STATUS.yaml com implementacao.backend = True

**Objetivo:**
- Criar contrato de teste derivado
- Criar matriz de violação
- Implementar testes automatizados focados em VIOLAÇÃO
- Garantir que backend REJEITA payloads inválidos
- Aprovar ou bloquear merge

**Autoridade:** Tester-Backend pode bloquear merges se backend aceita violações

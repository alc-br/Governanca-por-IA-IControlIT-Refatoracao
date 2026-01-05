# Executar Testes Completos

Executar todas as baterias de teste do **RF-XXX** conforme CONTRATO-EXECUCAO-TESTES.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-EXECUCAO-TESTES

**Checklist:** docs/checklists/checklist-testes.yaml

**Agente responsável:** tester (qa-tester)

**Pré-requisitos:**
- Backend implementado e aprovado
- Frontend implementado
- STATUS.yaml com implementacao.backend = True e implementacao.frontend = True

**Objetivo:**
Executar 3 baterias de teste sequenciais (100% PASS obrigatório em cada):

1. **Bateria Backend** (API tests) - 100% PASS antes de prosseguir
2. **Bateria Frontend** (E2E Playwright) - 100% PASS antes de prosseguir
3. **Bateria Outros** (Segurança, Performance) - 100% PASS para aprovação

**Resultado:** RF aprovado para produção somente com 100% em TODAS as 3 baterias

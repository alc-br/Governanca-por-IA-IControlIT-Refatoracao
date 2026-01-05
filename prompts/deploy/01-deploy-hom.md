# Deploy para Homologação (HOM)

Deploy do **RF-XXX** para ambiente de Homologação conforme contracts/deploy/azure.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-DEPLOY-AZURE

**Checklist:** checklists/checklist-deploy-prd.yaml

**Pré-requisitos:**
- Tester-Backend aprovou (validacao.tester_backend_aprovado = True)
- Testes 100% PASS em todas as 3 baterias
- EXECUTION-MANIFEST atualizado

**Objetivo:**
- Deploy HOM via pipeline Azure
- Rollback disponível em caso de falha
- Ambiente validado

**Importante:**
- Deploy só ocorre após aprovação Tester-Backend
- Alterações fora do pipeline são proibidas

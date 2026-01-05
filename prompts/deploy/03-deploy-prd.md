# Deploy para Produção (PRD)

Deploy do **RF-XXX** para ambiente de Produção conforme contracts/deploy/azure.md.

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-DEPLOY-AZURE

**Checklist:** checklists/checklist-deploy-prd.yaml

**Pré-requisitos OBRIGATÓRIOS:**
- Tester-Backend aprovou (validacao.tester_backend_aprovado = True)
- Testes 100% PASS em todas as 3 baterias
- Deploy HOM bem-sucedido
- EXECUTION-MANIFEST completo
- Aprovação formal para PRD

**Objetivo:**
- Deploy PRD via pipeline Azure
- Rollback obrigatório em caso de falha
- Ambiente validado

**Importante:**
- Deploy PRD requer 100% aprovação Tester-Backend
- Rollback obrigatório em caso de falha
- Alterações fora do pipeline são proibidas
- Acesso ao Azure exige autenticação válida (az login)

# Investigar Erro (Debug Controlado)

Investigar erro no **RF-XXX** ou **componente específico** conforme contracts/auditoria/CONTRATO-DEBUG-CONTROLADO.md.

**RF/Componente:** [Especificar, ex: RF-027 ou Backend de Autenticação]

**Descrição do erro:** [Descrever o problema]

---

**Contrato ativado:** CONTRATO-DEBUG-CONTROLADO

**Checklist:** checklists/checklist-debug.yaml

**Agente responsável:** debugger (debug-investigator)

**Modo:** READ-ONLY (não altera código)

**Objetivo:**
- Análise técnica completa
- Evidências observadas
- Hipóteses ordenadas
- Causa raiz provável ou indeterminada
- Plano de correção sugerido (sem executar)

**Importante:**
- Debug NÃO corrige, apenas investiga
- Qualquer correção DEVE ocorrer sob CONTRATO DE MANUTENÇÃO

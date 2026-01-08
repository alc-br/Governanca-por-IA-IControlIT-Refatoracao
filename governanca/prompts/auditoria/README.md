# Fluxo: AUDITORIA (Conformidade e qualidade)

Use esta sequência de prompts para auditar conformidade entre especificação e implementação.

## Quando usar

- Validar conformidade RF vs implementação
- Auditoria de backend completo
- Auditoria de frontend completo
- Auditoria completa (backend + frontend)

## Ordem de Execução

1. **01-auditoria-backend.md** - Auditar backend vs RF/UC/MD
2. **02-auditoria-frontend.md** - Auditar frontend vs RF/UC/WF
3. **03-auditoria-completa.md** - Auditar backend + frontend (conformidade total)

## Contratos Ativados

- CONTRATO-AUDITORIA-CONFORMIDADE

## Resultado Esperado

- Relatório de gaps gerado
- Divergências classificadas (CRÍTICO, IMPORTANTE, MENOR)
- Evidências com referências (arquivo:linha)
- Impacto de cada gap documentado
- Recomendação de contrato para correção

## Importante

- Auditoria é READ-ONLY (não corrige código)
- Relatórios salvos em `relatorios/AAAA-MM-DD-RFXXX-*-Gaps.md`
- Gaps críticos bloqueiam aprovação
- Após auditoria, usar contrato de manutenção para correções

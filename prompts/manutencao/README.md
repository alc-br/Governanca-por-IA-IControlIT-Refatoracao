# Fluxo: MANUTENÇÃO (Correção, hotfix, debug)

Use esta sequência de prompts para correções, bugs e manutenções.

## Quando usar

- Correção de bug
- Hotfix em produção
- Investigação de erro
- Manutenção preventiva

## Ordem de Execução

1. **01-debug.md** - Investigar erro (modo READ-ONLY)
2. **02-manutencao-curta.md** - Correção rápida e simples
3. **03-manutencao-backend.md** - Manutenção técnica de backend

## Contratos Ativados

- CONTRATO-DEBUG-CONTROLADO
- CONTRATO-MANUTENCAO-CURTO
- CONTRATO-DE-MANUTENCAO-BACKEND

## Resultado Esperado

- Problema investigado e documentado
- Correção aplicada sem quebrar funcionalidade
- Testes validam correção
- STATUS.yaml atualizado (se aplicável)

## Importante

- Debug NÃO corrige, apenas investiga
- Correção sempre sob contrato de manutenção
- Hotfix em PRD requer contrato específico

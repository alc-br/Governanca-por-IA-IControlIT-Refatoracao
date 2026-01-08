# CONTRATO DE ORQUESTRACAO DE EXECUCAO

Este contrato define a ordem, dependencias, bloqueios e permissões entre os contratos de execução do projeto.

Nenhum contrato pode ser executado fora da ordem definida neste documento.

---

## OBJETIVO

Garantir:
- Execução controlada
- Rastreabilidade
- Prevenção de conflitos entre agentes
- Bloqueio de execuções inválidas
- Sequenciamento obrigatório entre backend, frontend, testes e manutenção

---

## ORDEM OFICIAL DE EXECUAO

A execução válida segue obrigatoriamente a seguinte ordem:

1. CONTRATO-DE-DOCUMENTACAO-ESSENCIAL
2. CONTRATO-DE-EXECUCAO-BACKEND
3. CONTRATO-DE-TESTER-BACKEND
4. CONTRATO-DE-EXECUCAO-FRONTEND
5. CONTRATO-DE-EXECUCAO-TESTES (E2E / UI)
6. CONTRATO-DE-MANUTENCAO ou DEBUG (se aplicável)

---

## REGRAS DE BLOQUEIO

- Nenhum contrato pode ser iniciado se o anterior não estiver com status `COMPLETED`
- CONTRATO-DE-TESTER-BACKEND é **BLOQUEADOR**
- CONTRATO-DE-EXECUCAO-FRONTEND é bloqueado se:
  - Backend não estiver COMPLETED
  - Tester-Backend não tiver aprovado o contrato
- CONTRATO-DE-EXECUCAO-TESTES (E2E) só pode iniciar após frontend COMPLETED

---

## AUTORIDADE DOS CONTRATOS

| Contrato | Autoridade |
|--------|-----------|
| Documentacao | Define verdade funcional |
| Backend | Implementa regras |
| Tester-Backend | Valida contrato e violações |
| Frontend | Consome contrato backend |
| Testes E2E | Valida fluxo completo |
| Manutencao/Debug | Atua apenas sob autorização |

---

## EXECUCAO INVALIDA

É considerada execução inválida:

- Executar frontend antes do backend validado
- Criar testes sem contrato ativo
- Corrigir código sem contrato de manutenção
- Alterar comportamento sem atualizar contrato
- Pular etapa de teste de violação

Execuções inválidas devem ser abortadas imediatamente.

---

## REGRA FINAL

> Se um contrato falhar, **toda a cadeia é considerada inválida** até correção formal.

Nenhum atalho é permitido.

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido

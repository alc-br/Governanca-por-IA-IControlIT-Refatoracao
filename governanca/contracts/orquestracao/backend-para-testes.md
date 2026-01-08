# CONTRATO DE TRANSIÇÃO – BACKEND → TESTES

Este contrato define as regras formais para transição
de um Requisito Funcional do estado **Backend Validado**
para **Pronto para Testes**.

Este contrato é **obrigatório**, **bloqueador** e **automático**.

---

## PRÉ-REQUISITOS INEGOCIÁVEIS

A transição SÓ pode ocorrer se:

1. `CONTRATO-EXECUCAO-BACKEND` foi executado com sucesso
2. `CONTRATO-TESTER-BACKEND` foi executado
3. Resultado do Tester-Backend = **APROVADO**
4. Execução registrada no `EXECUTION-MANIFEST.md`

Se QUALQUER item acima não existir → TRANSIÇÃO NEGADA.

---

## FONTE DA VERDADE

A única fonte válida para decisão é:

contracts/EXECUTION-MANIFEST.md


O STATUS.yaml NÃO é fonte de decisão.
Ele é apenas reflexo do manifesto.

---

## AÇÃO AUTORIZADA

Quando todos os pré-requisitos forem atendidos,
o sistema ESTÁ AUTORIZADO a:

1. Atualizar `STATUS.yaml`
2. Atualizar coluna do board
3. Alterar contrato ativo

---

## ALTERAÇÕES PERMITIDAS NO STATUS.yaml

```yaml
governanca:
  contrato_ativo: CONTRATO-EXECUCAO-TESTES
  ultimo_manifesto: <ID_DO_MANIFESTO>

testes:
  backend: pending

devops:
  board_column: "Pronto para Testes"

PROIBIÇÕES

Alterar código

Executar testes

Iniciar frontend

Alterar contratos anteriores

Este contrato APENAS muda estado.

REGRA FINAL

Nenhum RF pode entrar em testes sem passar por esta transição formal.

Execuções fora deste contrato são inválidas.
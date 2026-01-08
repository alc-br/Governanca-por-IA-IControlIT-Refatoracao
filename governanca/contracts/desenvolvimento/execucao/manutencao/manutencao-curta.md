# CONTRATO DE MANUTENÇÃO – VERSÃO CURTA

Este contrato regula exclusivamente **correções de erro**
em funcionalidades já existentes.

---

## ESCOPO

✔️ Corrigir o erro informado  
❌ Criar funcionalidades  
❌ Evoluir comportamento  
❌ Refatorar código não relacionado  

---

## REGRAS

- Seguir `ARCHITECTURE.md`, `CONVENTIONS.md` e `CLAUDE.md`
- Corrigir SOMENTE o erro descrito
- Não alterar comportamento não relacionado
- Não criar abstrações, padrões ou melhorias
- Seeds só se forem indispensáveis e idempotentes
- i18n, permissões e seeds podem ser ajustados
  apenas se forem a causa direta do erro

---

## OBRIGAÇÕES

A correção só é válida se:
- O erro não ocorre mais
- Não surgem novos warnings ou erros
- O sistema funciona após restart
- Nenhuma alteração fora do escopo ocorreu

---

## BLOQUEIO

Se a correção exigir:
- Mudança de arquitetura
- Nova regra de negócio
- Evolução funcional

➡️ PARAR, ALERTAR e AGUARDAR decisão.

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido

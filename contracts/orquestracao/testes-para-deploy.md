# CONTRATO DE TRANSIÇÃO – TESTES PARA DEPLOY

**Versão:** 1.0
**Data de criação:** 2025-12-26
**Tipo de execução:** DECISÓRIA
**Autoridade:** QA / Tester

---

## NATUREZA DESTE CONTRATO

Este é um contrato de **TRANSIÇÃO DECISÓRIA**.

Ele NÃO executa deploy.
Ele NÃO altera código.
Ele NÃO corrige bugs.

Ele apenas **AUTORIZA a mudança de estado** de um RF que passou por testes com sucesso.

---

## FONTE DA VERDADE

A **ÚNICA fonte da verdade** é o arquivo:

```
docs/contracts/EXECUTION-MANIFEST.md
```

Este contrato NÃO pode ser ativado sem decisão formal registrada no manifesto.

---

## PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

Para que este contrato seja ativado, DEVEM existir:

### 1. Execução de Testes Aprovada

No EXECUTION-MANIFEST, DEVE existir uma execução com:

- RF identificado
- Contrato: `CONTRATO-EXECUCAO-TESTES`
- Bloco `DECISAO FORMAL` com:
  ```yaml
  decision:
    resultado: APROVADO
    autoridade: QA | Tester | Tester-Backend
    contrato: CONTRATO-EXECUCAO-TESTES
  ```

### 2. STATUS.yaml Atual

O STATUS.yaml do RF DEVE ter:

```yaml
governanca:
  contrato_ativo: CONTRATO-EXECUCAO-TESTES
```

### 3. Evidências de Testes

No EXECUTION-MANIFEST, DEVEM estar registradas:

- Testes executados (backend, frontend, E2E, segurança)
- Taxa de aprovação
- Evidências anexadas ou referenciadas

---

## REGRA DE NEGAÇÃO AUTOMÁTICA

Se QUALQUER pré-requisito falhar:

➡️ A transição DEVE ser **NEGADA**
➡️ O agente DEVE **PARAR**
➡️ O agente DEVE **DOCUMENTAR** o motivo da negação
➡️ Nenhuma ação parcial pode ser executada

---

## AÇÕES AUTORIZADAS

Se todos os pré-requisitos forem atendidos, o agente PODE:

### 1. Atualizar STATUS.yaml

Modificar EXCLUSIVAMENTE os seguintes campos:

```yaml
governanca:
  contrato_ativo: CONTRATO-EXECUCAO-DEPLOY
  ultimo_manifesto: <ID_DO_MANIFESTO_DE_TESTES>

devops:
  board_column: "Pronto para Deploy"
  last_sync: "<TIMESTAMP_ATUAL>"
```

### 2. Registrar Transição no EXECUTION-MANIFEST

Adicionar nova entrada no manifesto:

```markdown
# EXECUCAO: <ID_UNICO>

## TIPO DE EXECUCAO

- Tipo: DECISORIA

## CONTRATO ATIVO

- Contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
- RF: RFXXX
- Data: YYYY-MM-DD HH:MM:SS
- Executor: DevOps Agent

## PRE-REQUISITOS VALIDADOS

- [x] Testes aprovados no manifesto
- [x] STATUS.yaml em estado válido
- [x] Evidências registradas

## ACAO EXECUTADA

- STATUS.yaml atualizado
- Contrato ativo alterado para CONTRATO-EXECUCAO-DEPLOY
- Board column alterado para "Pronto para Deploy"

## DECISAO FORMAL

decision:
  resultado: APROVADO
  autoridade: DevOps-Agent
  contrato: CONTRATO-TRANSICAO-TESTES-PARA-DEPLOY
```

---

## PROIBIÇÕES ABSOLUTAS

Durante a execução deste contrato, é **PROIBIDO**:

- ❌ Executar deploy
- ❌ Alterar código de produção
- ❌ Corrigir bugs
- ❌ Modificar contratos anteriores
- ❌ Alterar configurações de ambiente
- ❌ Criar hotfix
- ❌ Pular validações
- ❌ Executar ações manuais fora do contrato
- ❌ Deploy manual "para testar"

---

## ESCOPO PERMITIDO

Este contrato permite EXCLUSIVAMENTE:

- ✅ Leitura do EXECUTION-MANIFEST
- ✅ Validação de pré-requisitos
- ✅ Atualização de STATUS.yaml (campos especificados)
- ✅ Registro de transição no EXECUTION-MANIFEST
- ✅ Atualização de timestamp de sincronização

---

## SAÍDAS OBRIGATÓRIAS

Ao final da execução, DEVEM existir:

1. STATUS.yaml atualizado com `contrato_ativo: CONTRATO-EXECUCAO-DEPLOY`
2. Nova entrada no EXECUTION-MANIFEST com decisão APROVADO
3. Board column atualizado para "Pronto para Deploy"
4. Timestamp de sincronização atualizado

---

## REGRA DE AUDITORIA

Esta transição é auditável e DEVE ser rastreável:

- De onde veio? → CONTRATO-EXECUCAO-TESTES
- Quem autorizou? → QA/Tester (decisão no manifesto)
- Quando ocorreu? → Timestamp no STATUS.yaml
- Qual o próximo passo? → CONTRATO-EXECUCAO-DEPLOY
- Qual o manifesto? → ultimo_manifesto no STATUS.yaml

---

## ROLLBACK DA TRANSIÇÃO

Se após a transição for detectado um problema:

- NÃO execute correção direta
- NÃO altere STATUS.yaml manualmente
- USE o CONTRATO-ROLLBACK
- Registre no EXECUTION-MANIFEST

---

## AUTOMAÇÃO

Este contrato DEVE ser executado pelo script:

```bash
python docs/tools/devops-sync/apply_tests_to_deploy_transition.py RFXXX
```

O script DEVE:
- Validar todos os pré-requisitos
- NEGAR se qualquer regra falhar
- Atualizar STATUS.yaml automaticamente
- Registrar no EXECUTION-MANIFEST

---

## REGRA FINAL

**Manifesto decide.**
**Contrato autoriza.**
**Script executa.**
**STATUS apenas reflete.**

Nenhuma exceção manual é permitida.
Nenhuma decisão humana fora do contrato é autorizada.
Toda transição DEVE ser auditável.

---

## VIOLAÇÃO DESTE CONTRATO

Se qualquer regra for violada:

➡️ A execução é considerada **INVÁLIDA**
➡️ O STATUS.yaml DEVE ser revertido
➡️ O manifesto DEVE registrar a violação
➡️ Investigação formal DEVE ser iniciada

---

**FIM DO CONTRATO**

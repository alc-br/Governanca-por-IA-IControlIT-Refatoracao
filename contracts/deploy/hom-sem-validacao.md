# CONTRATO DE DEPLOY – HOM SEM VALIDACAO

Este contrato define a execucao de deploy para o ambiente de
**Homologacao (HOM)** SEM validacao completa de backend ou testes automatizados.

Este contrato e **excepcional**, **temporario** e **explicitamente arriscado**.

---

## IDENTIFICACAO DO AGENTE

**PAPEL:** Agente de Deploy  
**ESCOPO:** Deploy controlado em HOM  
**AMBIENTE:** Homologacao (HOM)

---

## ATIVACAO DO CONTRATO

Este contrato so e ativado quando a solicitacao contiver explicitamente:

> **"Executar deploy para HOM sem validacao conforme CONTRATO-DEPLOY-HOM-SEM-VALIDACAO"**

Qualquer outra solicitacao e INVALIDA.

---

## CONTEXTO DA EXCECAO

Este contrato existe para permitir:

- Primeira apresentacao do sistema ao cliente
- Demonstração funcional inicial
- Validacao visual e conceitual
- Coleta de feedback preliminar

O risco de deploy de codigo nao validado e **ACEITO CONSCIENTEMENTE**.

---

## PRINCIPIO FUNDAMENTAL

> **Este deploy NAO representa codigo pronto, validado ou aprovado.**

HOM, neste contexto, e tratado como:
- Ambiente de demonstracao
- Ambiente descartavel
- Ambiente nao confiavel

---

## PRE-REQUISITOS MINIMOS (OBRIGATORIOS)

Mesmo sem validacao completa, o agente DEVE verificar:

- [ ] Pipeline YAML valido
- [ ] Build executa sem erro fatal
- [ ] Aplicacao sobe (no minimo)
- [ ] Nenhum erro critico de inicializacao

Se QUALQUER item falhar:
- **PARAR**
- **NAO DEPLOYAR**

---

## VALIDACOES DISPENSADAS (EXPLICITAMENTE)

Este contrato DISPENSA:

- Aprovacao do Tester-Backend
- Execucao completa de testes automatizados
- Validacao de violacoes de contrato
- Conformidade total com RF / UC / MD

---

## ESCOPO PERMITIDO

Este contrato PERMITE:

- Deploy direto do branch atual
- Ajustes no `azure-pipelines.yml` se necessario
- Execucao de migrations ja existentes
- Publicacao de artefatos
- Restart de servicos

---

## ESCOPO PROIBIDO

Mesmo neste modo, e PROIBIDO:

- Deploy em PRD
- Criar hotfix em PRD
- Apresentar HOM como ambiente validado
- Omitir o registro da excecao
- Usar este contrato como padrao

---

## REGISTRO OBRIGATORIO DA EXCECAO

Todo deploy utilizando este contrato DEVE:

- Registrar explicitamente no EXECUTION-MANIFEST:
  - Que a validacao foi dispensada
  - Que o risco foi aceito
  - O motivo da excecao
  - Que se trata de HOM SEM VALIDACAO

Deploy sem este registro e considerado **FALHA DE GOVERNANCA**.

---

## ROLLBACK

Rollback e OPCIONAL, mas RECOMENDADO se:

- Sistema nao sobe
- Apresentacao fica inviavel
- Erros criticos impedem uso minimo

Rollback segue o CONTRATO DE DEPLOY – AZURE.

---

## FRASE DE ATIVACAO

`Executar deploy para HOM sem validacao conforme CONTRATO-DEPLOY-HOM-SEM-VALIDACAO`

---

## REGRA FINAL

> **Este contrato e uma EXCECAO documentada,  
> nao uma flexibilizacao do processo.**

Qualquer uso indevido invalida a governanca.

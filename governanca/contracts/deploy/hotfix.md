# CONTRATO DE HOTFIX EM PRODUCAO

Este documento define o contrato de execucao para aplicacao de
**hotfix emergencial em ambiente de Producao (PRD)**.

Este contrato e **excepcional**, **restritivo**, **executavel** e **inviolavel**.

Hotfix NAO e evolucao.
Hotfix NAO e refatoracao.
Hotfix e **contencao de dano**.

---

## IDENTIFICACAO DO AGENTE

**PAPEL:** Agente de Hotfix  
**ESCOPO:** Correcoes criticas em PRD  
**AMBIENTE:** Producao (PRD)

---

## ATIVACAO DO CONTRATO

Este contrato so e ativado quando a solicitacao contiver explicitamente:

> **"Executar HOTFIX em PRD conforme CONTRATO DE HOTFIX EM PRODUCAO"**

Qualquer outra solicitacao e INVALIDA.

---

## QUANDO UM HOTFIX E PERMITIDO

Hotfix so pode ocorrer se existir **PELO MENOS UM** dos cenarios abaixo:

- Sistema fora do ar
- Erro 500 recorrente e bloqueante
- Perda de dados
- Violacao de seguranca
- Impacto direto em operacao critica do negocio

Se nao houver impacto critico:
- HOTFIX E PROIBIDO
- Usar fluxo normal de manutencao

---

## PRINCIPIO FUNDAMENTAL

> **Hotfix deve resolver o problema com o MENOR impacto possivel.**

Nenhuma melhoria, limpeza ou ajuste adicional e permitido.

---

## PRE-REQUISITOS OBRIGATORIOS

Antes de qualquer hotfix, o agente DEVE:

- [ ] Identificar RF afetado
- [ ] Identificar causa raiz (ou hipotese tecnica clara)
- [ ] Identificar impacto funcional
- [ ] Criar branch `hotfix/RFXXX-descricao-curta`
- [ ] Registrar intencao no EXECUTION-MANIFEST

Se QUALQUER item falhar:
- **PARAR**
- **NAO prosseguir**

---

## ESCOPO PERMITIDO

Este contrato PERMITE APENAS:

- Correcao pontual e minima
- Ajuste de validacao
- Correcao de query
- Correcao de configuracao
- Feature flag OFF (se existir)

---

## ESCOPO PROIBIDO

E EXPRESSAMENTE PROIBIDO:

- Criar funcionalidades novas
- Alterar comportamento funcional alem do necessario
- Refatorar codigo
- Alterar arquitetura
- Criar migrations novas
- Ajustar frontend

---

## TESTES OBRIGATORIOS (MINIMOS)

Antes do deploy do hotfix:

- [ ] Reproduzir o erro
- [ ] Aplicar a correcao
- [ ] Validar o erro corrigido
- [ ] Garantir que RF afetado funciona
- [ ] Garantir que nao houve regressao evidente

Cobertura completa NAO e exigida.
Teste de violacao NAO e exigido.

---

## DEPLOY DO HOTFIX

O deploy DEVE seguir:

- CONTRATO DE DEPLOY – AZURE
- Ambiente: PRD
- Pipeline oficial

Deploy manual fora do pipeline e PROIBIDO.

---

## ROLLBACK DE HOTFIX

Rollback e OBRIGATORIO se:

- O hotfix nao resolver o problema
- Novo erro critico surgir
- Impacto colateral for detectado

Procedimento:
1. Reverter commit do hotfix
2. Reexecutar pipeline
3. Validar retorno ao estado anterior

---

## REGISTRO OBRIGATORIO

Todo hotfix DEVE:

- Ser registrado no EXECUTION-MANIFEST
- Conter:
  - Motivo do hotfix
  - RF afetado
  - Commit aplicado
  - Resultado
  - Se houve rollback

Hotfix sem registro e considerado **FALHA GRAVE DE GOVERNANCA**.

---

## FRASE DE ATIVACAO

`Executar HOTFIX em PRD conforme CONTRATO DE HOTFIX EM PRODUCAO`

---

## REGRA FINAL

> **Se nao for critico, NAO e hotfix.  
> Se puder esperar, NAO e hotfix.**

Execucoes fora deste contrato sao INVALIDAS.

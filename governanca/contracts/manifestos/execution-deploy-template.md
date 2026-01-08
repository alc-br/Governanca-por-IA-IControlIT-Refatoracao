# EXECUTION MANIFEST – DEPLOY

Este manifesto registra uma execucao de deploy governado por contrato.

---

## IDENTIFICACAO DO DEPLOY

- Ambiente: DEV | HOM | PRD
- Tipo de Deploy: NORMAL | HOTFIX | ROLLBACK
- RF(s) Envolvidos:
- Contrato Utilizado:
  - CONTRATO DE DEPLOY – AZURE
  - CONTRATO DE HOTFIX EM PRODUCAO (se aplicavel)

---

## REFERENCIAS TECNICAS

- Branch:
- Commit Deployado:
- Tag (se houver):
- Pipeline:
- Artefato Publicado:

---

## PRE-DEPLOY CHECK (OBRIGATORIO)

- [ ] Backend aprovado
- [ ] Tester-Backend aprovado
- [ ] Manifesto funcional atualizado
- [ ] Pipeline validado
- [ ] Autenticacao Azure valida
- [ ] Backup / versao anterior identificada

Se QUALQUER item for NAO:
- Deploy INVALIDO

---

## EXECUCAO DO DEPLOY

- Data/Hora Inicio:
- Data/Hora Fim:
- Resultado do Pipeline: SUCCESS | FAILED
- Logs relevantes:

---

## POS-DEPLOY VALIDATION

- [ ] Aplicacao online
- [ ] Healthcheck OK
- [ ] Login funcional
- [ ] RF(s) acessiveis
- [ ] Nenhum erro critico detectado

---

## ROLLBACK

- Rollback Executado: SIM | NAO
- Motivo:
- Commit restaurado:
- Validacao apos rollback:

---

## APROVACAO FINAL

- Responsavel pelo Deploy:
- Aprovado por:
- Observacoes finais:

---

## REGRA FINAL

> Deploy sem este manifesto preenchido e INVALIDO.

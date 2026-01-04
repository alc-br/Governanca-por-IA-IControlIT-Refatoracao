# CHECKLIST – CONTRATO DE DOCUMENTAÇÃO GOVERNADA

Este checklist valida o cumprimento integral do **Contrato de Documentação Governada**.

> Este documento é um instrumento de validação.
> Ele NÃO é um prompt e NÃO deve ser alterado por agentes.

---

## 1. Governança Inicial

- [ ] O contrato de documentação foi explicitamente citado no prompt
- [ ] O agente confirmou leitura de CLAUDE.md
- [ ] Nenhum arquivo de código foi alterado

---

## 2. Escopo

- [ ] Apenas arquivos em /docs foram alterados
- [ ] Nenhum código de backend/frontend foi tocado
- [ ] Nenhum teste foi criado ou modificado
- [ ] Nenhuma pipeline foi alterada
- [ ] Nenhum seed foi criado ou modificado
- [ ] Nenhuma permissão foi alterada

---

## 3. STATUS.yaml

- [ ] Todos os RFs possuem STATUS.yaml
- [ ] Schema do STATUS.yaml está correto
- [ ] Campos de documentação refletem artefatos existentes
- [ ] Campos desconhecidos marcados como null ou not_started
- [ ] Status inferido apenas de evidências documentais

---

## 4. Regras de Inferência

- [ ] Nenhum progresso foi assumido sem evidência
- [ ] Campos de DevOps (IDs, planos) não foram preenchidos manualmente
- [ ] Inconsistências foram registradas, não corrigidas

---

## 5. Critério Final

- [ ] Nenhum arquivo fora de /docs foi alterado
- [ ] STATUS.yaml válidos e coerentes
- [ ] Contrato de documentação respeitado integralmente

---

## Status Final

- [ ] APROVADO
- [ ] REPROVADO

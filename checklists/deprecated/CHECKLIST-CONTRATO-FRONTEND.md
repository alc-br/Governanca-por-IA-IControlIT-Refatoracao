# CHECKLIST – CONTRATO DE EXECUÇÃO – FRONTEND

Este checklist valida o cumprimento integral do **Contrato de Execução – Frontend**.

> Este documento é um instrumento de validação.
> Ele NÃO é um prompt e NÃO deve ser alterado por agentes.

---

## 1. Governança Inicial

- [ ] O contrato de execução frontend foi explicitamente citado no prompt
- [ ] O agente confirmou leitura de ARCHITECTURE.md, CONVENTIONS.md e CLAUDE.md
- [ ] Nenhum arquivo em /docs foi alterado

---

## 2. Escopo

- [ ] Apenas frontend foi alterado
- [ ] Nenhuma funcionalidade nova foi criada
- [ ] Nenhuma refatoração ampla foi realizada
- [ ] Estrutura global de rotas não foi alterada

---

## 3. i18n (OBRIGATÓRIO)

- [ ] Todas as chaves i18n utilizadas existem
- [ ] Nenhum warning de tradução ausente no console
- [ ] pt-BR, en-US e es-ES completos
- [ ] Nenhum fallback silencioso utilizado

---

## 4. Governança de Acesso

- [ ] Permissões do RF foram identificadas explicitamente
- [ ] Permissões estão registradas no backend
- [ ] Permissões associadas ao perfil developer
- [ ] Acesso real testado (HTTP 200)

---

## 5. Seeds

- [ ] Seeds funcionais existem
- [ ] Seeds são idempotentes
- [ ] Nenhum seed temporário ou oculto
- [ ] Ambiente limpo funciona sem reset manual

---

## 6. Testes E2E (Playwright)

- [ ] Login como developer validado
- [ ] Acesso via menu validado
- [ ] Listagem carrega dados reais
- [ ] Fluxo principal executado
- [ ] Nenhum 401/403/404/500 passou despercebido

---

## 7. Critério Final

- [ ] Build frontend OK
- [ ] RF navegável e funcional
- [ ] Nenhum erro de permissão
- [ ] Nenhum warning no console
- [ ] Evidência de execução dos testes apresentada

---

## Status Final

- [ ] APROVADO
- [ ] REPROVADO

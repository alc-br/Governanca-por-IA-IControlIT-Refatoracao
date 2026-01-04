# CHECKLIST – CONTRATO DE EXECUÇÃO – BACKEND

Checklist de validação do **Contrato de Execução – Backend**.

---

## 1. Governança Inicial

- [ ] Contrato backend citado explicitamente
- [ ] ARCHITECTURE.md, CONVENTIONS.md e CLAUDE.md respeitados
- [ ] Nenhuma alteração em /docs

---

## 2. Escopo

- [ ] Apenas Application/Web/Infrastructure alterados
- [ ] Nenhuma mudança arquitetural
- [ ] Nenhuma entidade nova criada sem autorização

---

## 3. Commands / Queries / Endpoints

- [ ] Command principal executa com sucesso
- [ ] Query principal retorna dados esperados
- [ ] Endpoints retornam contratos corretos
- [ ] Erros 401/403/404/500 falham testes

---

## 4. Permissões

- [ ] Permissões existem no registry
- [ ] Associadas ao perfil developer
- [ ] Validadas em runtime

---

## 5. Seeds

- [ ] Seeds funcionais existentes
- [ ] Idempotentes
- [ ] Executáveis em ambiente limpo
- [ ] Reexecução possível sem reset

---

## 6. Startup / Runtime

- [ ] Startup valida permissões obrigatórias
- [ ] Erros são logados explicitamente
- [ ] Ambiente inconsistente não passa silenciosamente

---

## Status Final

- [ ] APROVADO
- [ ] REPROVADO

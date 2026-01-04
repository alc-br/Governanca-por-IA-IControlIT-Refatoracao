# CHECKLIST – CONTRATO DE DEVOPS / GOVERNANÇA OPERACIONAL

Este checklist valida o cumprimento integral do **Contrato de DevOps / Governança Operacional**.

> Este documento é um instrumento de validação.
> Ele NÃO é um prompt e NÃO deve ser alterado por agentes.

---

## 1. Governança Inicial

- [ ] O contrato de DevOps foi explicitamente citado no prompt
- [ ] O agente confirmou leitura de CLAUDE.md
- [ ] devops/execution-manifest.md foi atualizado antes da execução

---

## 2. Manifesto de Execução

- [ ] Tipo de operação declarado (Consulta/Inclusão/Edição/Exclusão)
- [ ] Alvo da mudança identificado
- [ ] Ambiente especificado
- [ ] Justificativa explícita registrada
- [ ] Plano de rollback definido

---

## 3. Escopo

- [ ] Alterações restritas ao Azure DevOps
- [ ] Nenhum código de frontend/backend foi alterado
- [ ] Nenhuma "melhoria" não solicitada foi realizada
- [ ] Escopo limitado ao objetivo declarado

---

## 4. Modo Consulta

- [ ] Apenas leitura de configurações
- [ ] Exports e evidências coletados
- [ ] Nenhuma alteração realizada

---

## 5. Modo Edição

- [ ] Objetivo explicitamente descrito
- [ ] Manifesto preenchido
- [ ] Impacto limitado ao escopo
- [ ] Rollback possível

---

## 6. Modo Inclusão

- [ ] Naming padrão seguido
- [ ] Justificativa explícita
- [ ] Plano de rollback definido
- [ ] Evidência pós-criação anexada

---

## 7. Modo Exclusão (Excepcional)

- [ ] Exclusão explicitamente solicitada
- [ ] Aprovação humana obtida
- [ ] Backup/export realizado antes
- [ ] Evidência anexada
- [ ] Preferência por desativar/arquivar respeitada

---

## 8. Proibições

- [ ] Nenhum código-fonte foi alterado
- [ ] Nenhuma pipeline criada sem governança
- [ ] Nenhuma permissão alterada sem evidência
- [ ] Nenhuma proteção de branch removida
- [ ] Nenhum ajuste em produção sem aprovação

---

## 9. Saída Obrigatória

- [ ] Lista do que foi alterado entregue
- [ ] Evidências anexadas (prints, exports, YAMLs)
- [ ] Rollback confirmado como possível
- [ ] Impacto esperado documentado

---

## 10. Critério Final

- [ ] devops/execution-manifest.md atualizado
- [ ] Aprovações exigidas foram respeitadas
- [ ] Contrato de DevOps respeitado integralmente
- [ ] Nenhuma regra do contrato foi violada

---

## Status Final

- [ ] APROVADO
- [ ] REPROVADO

---
description: Sincronizar Lista de Tarefas (project)
allowed-tools: Write, Read
---

# Sincronizar Lista de Tarefas

Sincronize a lista de tarefas atual (do TodoWrite) com o arquivo físico `D:\IC2\todos.md`.

## Instruções

1. **Leia a lista de tarefas atual** que está sendo gerenciada pelo sistema TodoWrite
2. **Escreva no arquivo** `D:\IC2\todos.md` no seguinte formato:

```markdown
# Lista de Tarefas

> Última sincronização: [DATA_HORA_ATUAL]

## Em Progresso
- [ ] Tarefa em andamento...

## Pendentes
- [ ] Tarefa pendente 1
- [ ] Tarefa pendente 2

## Concluídas
- [x] Tarefa concluída 1
- [x] Tarefa concluída 2
```

3. **Regras de formatação:**
   - Use `- [ ]` para tarefas pendentes e em progresso
   - Use `- [x]` para tarefas concluídas
   - Agrupe por status: Em Progresso, Pendentes, Concluídas
   - Inclua timestamp da última sincronização
   - Se não houver tarefas em alguma categoria, omita a seção

4. **Após sincronizar**, informe o usuário quantas tarefas foram sincronizadas por status.

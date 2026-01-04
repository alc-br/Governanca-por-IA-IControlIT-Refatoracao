# Scripts de Validação - DevOps Sync

Scripts para **troubleshooting** e validação de configuração do Azure DevOps.

## Scripts Disponíveis

| Script | Descrição | Quando Usar |
|--------|-----------|-------------|
| **check-env.py** | Valida variáveis de ambiente | Troubleshooting de autenticação |
| **find-kanban-field.py** | Localiza campo Kanban no board | Quando coluna não aparece |
| **check-team-sprints.py** | Valida sprints do time | Quando sprints não aparecem |
| **check-iteration-dates.py** | Valida datas de iterações | Quando datas estão incorretas |
| **check-work-item.py** | Valida um Work Item específico | Troubleshooting de item específico |
| **validate-sprint-backlogs.py** | Valida backlogs de sprints | Quando backlog está vazio |
| **diagnose-sprint-backlog-empty.py** | Diagnostica backlog vazio | Quando sprint não mostra itens |
| **check-backlog-levels.py** | Valida níveis de backlog | Quando hierarquia está quebrada |
| **check-classification-nodes.py** | Valida nós de classificação | Quando áreas/iterações não aparecem |
| **check-team-iterations-detailed.py** | Valida iterações detalhadas | Troubleshooting de iterações |
| **list-all-iterations.py** | Lista todas as iterações | Ver estrutura completa |
| **verify-sprint-dates.py** | Verifica datas de sprints | Validar calendário de sprints |

## Uso

### Validar Ambiente
```bash
python tools/devops-sync/validation/check-env.py
```

### Encontrar Campo Kanban
```bash
python tools/devops-sync/validation/find-kanban-field.py
```

### Validar Sprints do Time
```bash
python tools/devops-sync/validation/check-team-sprints.py
```

### Diagnosticar Backlog Vazio
```bash
python tools/devops-sync/validation/diagnose-sprint-backlog-empty.py
```

## Quando Usar Estes Scripts

### Cenário 1: Autenticação Falhando
```bash
python tools/devops-sync/validation/check-env.py
```

### Cenário 2: Work Items Não Aparecem no Board
```bash
python tools/devops-sync/validation/find-kanban-field.py
python tools/devops-sync/validation/check-backlog-levels.py
```

### Cenário 3: Sprint Backlog Vazio
```bash
python tools/devops-sync/validation/diagnose-sprint-backlog-empty.py
python tools/devops-sync/validation/validate-sprint-backlogs.py
```

### Cenário 4: Iterações com Datas Erradas
```bash
python tools/devops-sync/validation/check-iteration-dates.py
python tools/devops-sync/validation/verify-sprint-dates.py
```

## Resultado Esperado

Todos os scripts de validação retornam:
- ✅ Sucesso (tudo OK) - exit code 0
- ❌ Falha (problema detectado) - exit code 1 + mensagem de erro

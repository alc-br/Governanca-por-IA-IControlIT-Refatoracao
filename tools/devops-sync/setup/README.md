# Scripts de Setup - DevOps Sync

Scripts para **configuração inicial** do Azure DevOps (executar **UMA VEZ** no início do projeto).

## Scripts Disponíveis

| Script | Descrição | Quando Usar |
|--------|-----------|-------------|
| **create-work-items.py** | Cria Work Items iniciais | Setup inicial do projeto |
| **create-iterations.py** | Cria estrutura de iterações/sprints | Setup do calendário de sprints |
| **create-area-paths.py** | Cria áreas do projeto | Organizar Work Items por área |
| **create-board-column.py** | Cria colunas customizadas no board | Adicionar colunas ao Kanban |
| **create-missing-status.py** | Cria status faltantes | Quando novo status é necessário |
| **create-delivery-plan.py** | Cria Delivery Plan | Visualizar roadmap de entregas |
| **configure-team-sprints.py** | Configura sprints do time | Associar sprints ao time |
| **assign-items-to-sprints.py** | Atribui Work Items a sprints | Preencher sprint backlogs |
| **refresh-team-iterations.py** | Atualiza iterações do time | Sincronizar iterações do time |
| **update-sprint-dates.py** | Atualiza datas de sprints | Ajustar calendário de sprints |

## Uso

### 1. Setup Inicial (Ordem Obrigatória)

#### 1.1. Criar Iterações (Sprints)
```bash
python tools/devops-sync/setup/create-iterations.py
```

#### 1.2. Criar Áreas
```bash
python tools/devops-sync/setup/create-area-paths.py
```

#### 1.3. Configurar Sprints do Time
```bash
python tools/devops-sync/setup/configure-team-sprints.py
```

#### 1.4. Criar Work Items
```bash
python tools/devops-sync/setup/create-work-items.py
```

#### 1.5. Atribuir Work Items a Sprints
```bash
python tools/devops-sync/setup/assign-items-to-sprints.py
```

#### 1.6. Criar Delivery Plan
```bash
python tools/devops-sync/setup/create-delivery-plan.py
```

### 2. Manutenção de Sprints

#### Atualizar Datas de Sprints (Modo Direto)
```bash
python tools/devops-sync/setup/update-sprint-dates.py direct
```

#### Atualizar Datas de Sprints (Modo Hierárquico)
```bash
python tools/devops-sync/setup/update-sprint-dates.py hierarchy
```

#### Atualizar Sprint Específica por ID
```bash
python tools/devops-sync/setup/update-sprint-dates.py by-id <iteration_id>
```

### 3. Customizações

#### Criar Coluna Customizada no Board
```bash
python tools/devops-sync/setup/create-board-column.py
```

#### Criar Status Faltante
```bash
python tools/devops-sync/setup/create-missing-status.py
```

## Pré-requisitos

- Variável de ambiente `AZURE_DEVOPS_PAT` configurada
- Permissões de administrador no projeto Azure DevOps
- Estrutura de pastas de RFs criada em `docs/rf/`

## Atenção

⚠️ **Scripts de setup só devem ser executados UMA VEZ** (ou quando necessário recriar estrutura).

⚠️ **update-sprint-dates.py** consolida 3 scripts antigos (update-sprint-dates-direct, -hierarchy, -by-id).

⚠️ **NÃO execute create-work-items.py** se Work Items já existem (causará duplicação).

## Resultado Esperado

Após executar todos os scripts de setup:
- ✅ Estrutura de iterações criada (Fase 1, Fase 2, etc.)
- ✅ Áreas criadas (por Epic ou módulo)
- ✅ Sprints associados ao time
- ✅ Work Items criados e organizados
- ✅ Sprint Backlogs preenchidos
- ✅ Delivery Plan criado para visualizar roadmap

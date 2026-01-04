# Criar Estrutura Completa de Governança de Dados 4.0

**Objetivo:** Criar estrutura completa de governança para um projeto do zero, incluindo contratos, checklists, prompts, agentes e scripts.

**Quando usar:** Início de projeto novo ou replicação de governança em outro projeto.

---

## PASSO 1: Configuração Interativa (OBRIGATÓRIO)

Fazer as seguintes perguntas ao usuário:

### 1.1. Ferramenta DevOps

```
Qual ferramenta DevOps você utilizará?

1. Azure DevOps (Boards + Repos + Pipelines)
2. Jira (Issues) + GitHub (Repos) + Jenkins (Pipelines)
3. GitHub Projects + GitHub Actions
4. GitLab (Issues + Repos + Pipelines)
5. Outra (especificar)

Resposta: [número]
```

### 1.2. Estrutura de Board

```
Como seu board de trabalho está estruturado?

Liste as colunas do seu board na ordem:
[Exemplo: To Do, In Progress, Review, Done]

Resposta: [lista de colunas]
```

###1.3. Sistema Legado

```
Este projeto possui sistema legado para migrar?

1. Sim - Tenho código legado (especificar localização)
2. Não - Projeto completamente novo

Se sim, localização: [path]
```

### 1.4. Certificações Alvo

```
Quais certificações de compliance você precisa atender?

☐ ISO 27001 (Segurança da Informação)
☐ SOC 2 (Service Organization Control)
☐ LGPD (Lei Geral de Proteção de Dados - Brasil)
☐ GDPR (General Data Protection Regulation - Europa)
☐ SOX (Sarbanes-Oxley - Auditoria Financeira)
☐ HIPAA (Health Insurance Portability - Saúde)
☐ PCI-DSS (Payment Card Industry - Pagamentos)
☐ Nenhuma certificação formal

Marque todas que se aplicam: [lista]
```

### 1.5. Stack Tecnológico

```
Qual é a stack tecnológica do projeto?

Backend:
- Linguagem: [.NET, Java, Python, Node.js, Go, etc]
- Versão: [especificar]

Frontend:
- Framework: [Angular, React, Vue, etc]
- Versão: [especificar]

Database:
- Tipo: [SQL Server, PostgreSQL, MySQL, SQLite, MongoDB, etc]

Responda cada item acima.
```

---

## PASSO 2: Criar Estrutura de Pastas

Criar a seguinte estrutura:

```
projeto/
├── docs/
│   ├── CLAUDE.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── COMPLIANCE.md
│   ├── MATRIZ-RASTREABILIDADE.md
│   ├── LEGACY-MAPPING.md (se houver legado)
│   │
│   ├── contracts/
│   │   ├── README.md
│   │   ├── [13 contratos]
│   │
│   ├── checklists/
│   │   ├── README.md
│   │   ├── [13 checklists YAML]
│   │
│   ├── prompts/
│   │   ├── README.md
│   │   ├── novo/ (5 prompts)
│   │   ├── adequacao/ (4 prompts)
│   │   ├── manutencao/ (3 prompts)
│   │   ├── deploy/ (3 prompts)
│   │   ├── auditoria/ (3 prompts)
│   │   └── devops/ (3 prompts)
│   │
│   └── templates/
│       ├── RF.md
│       ├── UC.md
│       ├── MD.md
│       ├── WF.md
│       └── TEMPLATE-USER-STORIES.yaml
│
├── .claude/
│   ├── agents/
│   │   ├── README.md
│   │   └── [7 agentes]
│   │
│   └── commands/
│       ├── README.md
│       └── [7 comandos]
│
└── tools/
    └── devops-sync/
        ├── config.yaml
        ├── core/ (3 scripts)
        ├── validation/ (12 scripts)
        ├── setup/ (10 scripts)
        ├── governance/ (3 scripts)
        └── adapters/
            ├── base.py
            ├── azure_devops.py
            ├── jira.py
            └── github_projects.py
```

---

## PASSO 3: Criar config.yaml para DevOps

Baseado nas respostas da Seção 1, criar `docs/tools/devops-sync/config.yaml`:

```yaml
# Configuração DevOps
tool: "[azure-devops|jira|github-projects|gitlab]"

# Configuração específica da ferramenta escolhida
[ferramenta]:
  organization: "[nome-org]"
  project: "[nome-projeto]"
  pat_env_var: "[nome_var_ambiente]"

# Mapeamento STATUS.yaml → Colunas Board
board_mapping:
  to_do: [documentacao_incompleta]
  in_progress: [backend_em_desenvolvimento, frontend_em_desenvolvimento]
  testing: [testes_executando]
  review: [aguardando_aprovacao]
  done: [deploy_producao_concluido]

# Ajustar baseado nas colunas informadas pelo usuário
```

---

## PASSO 4: Criar Adapters para DevOps

Criar arquitetura de adapters para suportar múltiplas ferramentas:

**docs/tools/devops-sync/adapters/base.py:**
```python
from abc import ABC, abstractmethod

class DevOpsAdapter(ABC):
    @abstractmethod
    def create_work_item(self, type, title, description, **kwargs):
        pass

    @abstractmethod
    def update_work_item(self, item_id, fields):
        pass

    @abstractmethod
    def move_to_column(self, item_id, column_name):
        pass
```

**docs/tools/devops-sync/adapters/azure_devops.py:**
```python
# Implementação para Azure DevOps
# (código completo conforme D:\IC2\tools\devops-sync\core\sync-rf.py)
```

**docs/tools/devops-sync/adapters/jira.py:**
```python
# Implementação para Jira
# (adaptar lógica do Azure DevOps para API do Jira)
```

---

## PASSO 5: Criar Contratos (13 arquivos)

Para cada contrato, criar arquivo com estrutura:

```markdown
# CONTRATO DE [TIPO] - [NOME]

**Versão:** 1.0.0
**Ativação:** Explícita (usuário menciona contrato)

## Zonas Permitidas

- LEITURA: [lista de pastas]
- ESCRITA: [lista de pastas]

## Proibições Absolutas

- [lista de proibições]

## Workflow Obrigatório

1. [Passo 1]
2. [Passo 2]
...

## Critério de Pronto

- [ ] [Item 1]
- [ ] [Item 2]
...
```

Contratos a criar:
1. CONTRATO-DOCUMENTACAO-ESSENCIAL
2. CONTRATO-EXECUCAO-BACKEND
3. CONTRATO-EXECUCAO-TESTER-BACKEND
4. CONTRATO-EXECUCAO-FRONTEND
5. CONTRATO-EXECUCAO-TESTES
6. CONTRATO-DE-REGULARIZACAO-DE-BACKEND
7. CONTRATO-DEBUG-CONTROLADO
8. CONTRATO-MANUTENCAO-CURTO
9. CONTRATO-DE-MANUTENCAO-BACKEND
10. CONTRATO-DEPLOY-AZURE (ou equivalente)
11. CONTRATO-DEPLOY-HOM-SEM-VALIDACAO
12. CONTRATO-AUDITORIA-CONFORMIDADE
13. CONTRATO-DEVOPS-GOVERNANCA

---

## PASSO 6: Criar Checklists YAML (13 arquivos)

Para cada checklist, criar arquivo com estrutura:

```yaml
metadata:
  checklist_name: "checklist-[nome]"
  version: "1.0.0"
  contract: "CONTRATO-[NOME]"
  last_updated: "YYYY-MM-DD"

criteria:
  - id: "[ID]"
    description: "[descrição]"
    severity: "[CRITICAL|IMPORTANT|MINOR]"
    validation_type: "[file_exists|command_success|content_matches]"

compliance_gates:
  - gate: "[NOME_GATE]"
    required_criteria: [[lista de IDs]]
    blocking: [true|false]
```

---

## PASSO 7: Criar Prompts (21 arquivos em 6 pastas)

Cada prompt segue estrutura:

```markdown
# [Título do Prompt]

[Descrição breve do que faz - 1 linha]

**RF:** [Especificar RF, ex: RF-027]

---

**Contrato ativado:** CONTRATO-[NOME]

**Checklist:** docs/checklists/checklist-[nome].yaml

**Agente responsável:** [nome-agente] (se aplicável)

**Pré-requisitos:**
- [Lista de pré-requisitos]

**Objetivo:**
- [O que este prompt realiza]

**Resultado:**
- [Output esperado]
```

---

## PASSO 8: Criar Agentes (7 arquivos)

Cada agente segue estrutura:

```markdown
---
name: [agent-name]
description: [descrição quando usar]
model: [sonnet|opus|haiku]
color: [cor]
---

# Agente [Nome] - [Subtítulo]

**Versão:** 1.0
**Tipo:** [tipo-agente]
**Modelo Preferido:** [modelo]
**Atualizado:** YYYY-MM-DD

## Propósito Principal

[Descrição detalhada]

## Responsabilidades

1. [Responsabilidade 1]
2. [Responsabilidade 2]

## Quando Usar Este Agente

[Critérios de ativação]

## Proibições Absolutas

[O que o agente NÃO pode fazer]

## Workflow

[Passos que o agente executa]
```

Agentes a criar:
1. architect.md
2. developer.md
3. tester.md
4. debugger.md
5. orchestrator.md
6. backend-regularizer.md
7. auditor.md

---

## PASSO 9: Criar Comandos (7 arquivos)

Cada comando segue estrutura:

```markdown
---
description: [descrição curta]
allowed-tools: [lista de tools]
---

# [Nome do Comando]

[Descrição detalhada]

## Instruções

1. [Passo 1]
2. [Passo 2]
...

## Exemplos de Uso

[Exemplos práticos]

## Troubleshooting

[Solução de problemas comuns]
```

Comandos a criar:
1. start-rf.md
2. validate-rf.md
3. deploy-rf.md
4. audit-rf.md
5. fix-build.md
6. sync-devops.md
7. sync-todos.md

---

## PASSO 10: Criar Documentação de Compliance

Criar `docs/COMPLIANCE.md` com seções para cada certificação selecionada:

```markdown
# Certificações e Compliance - [Nome do Projeto]

## Certificações Implementadas

[Para cada certificação marcada pelo usuário]

### [Nome da Certificação]

**Controles Implementados:**
- [Controle 1]: [Descrição]

**Artefatos:**
- [Caminho para arquivo]

**Requisitos de Auditoria:**
- [Retenção de dados, frequência de revisão, etc]
```

---

## PASSO 11: Criar CLAUDE.md

Criar arquivo principal de governança:

```markdown
# CLAUDE.md
# Contract for Claude Code (claude.ai/code)

## Idioma e Comunicação

- SEMPRE responda em [idioma do projeto]

## Fonte da Verdade

- `/docs/ARCHITECTURE.md`
- `/docs/CONVENTIONS.md`
- `/docs/contracts/*.md`

## Sistema de Contratos

[Explicar como contratos funcionam]

## Regras Invioláveis

[Listar regras fundamentais]
```

---

## PASSO 12: Validação Final

Executar validações:

- [ ] Estrutura de pastas completa (60+ arquivos)
- [ ] config.yaml configurado corretamente
- [ ] Adapters criados para ferramenta DevOps escolhida
- [ ] 13 contratos criados
- [ ] 13 checklists YAML criados
- [ ] 21 prompts criados em 6 pastas
- [ ] 7 agentes criados com frontmatter YAML
- [ ] 7 comandos criados
- [ ] COMPLIANCE.md com certificações selecionadas
- [ ] MATRIZ-RASTREABILIDADE.md criada
- [ ] LEGACY-MAPPING.md criado (se aplicável)

---

## PASSO 13: Teste de Sanidade

Criar RF de teste (RF-001):

1. Executar fluxo completo:
   - Documentação (architect)
   - Backend (developer)
   - Frontend (developer)
   - Testes (tester)
   - Sync DevOps

2. Validar que todos os contratos funcionam
3. Validar que scripts DevOps sincronizam
4. Validar que board reflete estado correto

---

## PASSO 14: Entrega Final

1. Git commit de toda estrutura
2. Tag de versão: `v1.0.0-governanca`
3. Criar documentação de onboarding
4. Gerar relatório final:

```markdown
# Relatório: Estrutura de Governança Criada

## Resumo

- **Data:** YYYY-MM-DD
- **Projeto:** [nome]
- **Stack:** [backend] + [frontend] + [database]
- **DevOps:** [ferramenta]
- **Certificações:** [lista]

## Estrutura Criada

- 60+ arquivos de governança
- 13 contratos formais
- 7 agentes especializados
- 21 prompts organizados
- Scripts DevOps parametrizáveis

## Próximos Passos

1. Criar primeiro RF usando `docs/prompts/novo/01-documentacao-essencial.md`
2. Sincronizar com DevOps usando `/sync-devops`
3. Validar fluxo completo com RF-001
```

---

## Notas Importantes

- **Tempo estimado:** 8-12 horas (dependendo do tamanho do projeto)
- **Pré-requisito:** Claude Code instalado e configurado
- **Resultado:** Estrutura 100% replicável e adaptável
- **Benefício:** Governança completa desde dia 1 do projeto

---

## Versionamento

- **Criado em:** 2025-12-28
- **Última atualização:** 2025-12-28
- **Versão:** 1.0.0

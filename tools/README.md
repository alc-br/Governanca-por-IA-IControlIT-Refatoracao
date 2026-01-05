# Tools - Ferramentas de Automação e Validação

Este diretório contém **ferramentas de automação, validação e análise** do projeto IControlIT.

## O que são Tools?

Tools são scripts executáveis que:
- **Validam** documentação e código
- **Automatizam** tarefas repetitivas
- **Analisam** conformidade e cobertura
- **Geram** relatórios e evidências
- **Sincronizam** dados com Azure DevOps

**NÃO são prompts ou contratos**, são ferramentas técnicas.

---

## Estrutura de Pastas

```
tools/
├── docs/                    ← Validadores de documentação
│   ├── validator-rf-uc.py
│   ├── validator-rl.py
│   ├── validator-governance.py
│   └── SCRIPT-AUDITORIA-CORRECAO-AUTO.py
│
├── devops-sync/             ← Sincronização com Azure DevOps
│   ├── sync-rf.py
│   ├── sync-user-stories.py
│   └── sync-all-rfs.py
│
├── contract-validator/      ← Validação de contratos
│   ├── validate-transitions.py
│   └── validate-contract-compliance.py
│
├── test-runners/            ← Executores de testes
│   ├── run-backend-tests.py
│   ├── run-e2e-tests.py
│   └── run-all-tests.py
│
└── reports/                 ← Geradores de relatórios
    ├── generate-coverage-report.py
    ├── generate-gap-report.py
    └── generate-compliance-report.py
```

---

## Categoria: Validadores de Documentação

**Localização:** `tools/docs/`

### validator-rf-uc.py

**Propósito:** Validar cobertura RF → UC → TC

**Uso:**
```bash
python tools/docs/validator-rf-uc.py RFXXX
```

**Valida:**
- UC cobre 100% do RF
- TC cobre 100% dos UCs
- Nenhum UC cria comportamento fora do RF
- UC00-UC04 obrigatórios existem
- RFXXX.yaml e UC-RFXXX.yaml sincronizados

**Exit Codes:**
- `0` → Validação APROVADA
- `!= 0` → Validação REPROVADA (gaps encontrados)

---

### validator-rl.py

**Propósito:** Validar separação RF / RL

**Uso:**
```bash
python tools/docs/validator-rl.py RFXXX
```

**Valida:**
- RF.md e RL.md separados
- RL tem destino explícito para cada item
- Nenhum legado misturado em RF

**Exit Codes:**
- `0` → Separação válida
- `!= 0` → Gaps encontrados

---

### validator-governance.py

**Propósito:** Validação completa de governança

**Uso:**
```bash
python tools/docs/validator-governance.py RFXXX
```

**Valida:**
- RF/RL separação
- RF → UC cobertura
- UC → TC cobertura
- STATUS.yaml consistente
- user-stories.yaml existe
- Documentação essencial completa

**Exit Codes:**
- `0` → Governança 100% conforme
- `!= 0` → Gaps de governança

---

### SCRIPT-AUDITORIA-CORRECAO-AUTO.py

**Propósito:** Auditar e corrigir documentação automaticamente

**Uso:**
```bash
python tools/docs/SCRIPT-AUDITORIA-CORRECAO-AUTO.py RFXXX
```

**Funcionalidades:**
- Detecta gaps de documentação
- Corrige automaticamente quando possível
- Gera relatório de correções
- Atualiza STATUS.yaml

---

## Categoria: Sincronização com Azure DevOps

**Localização:** `tools/devops-sync/`

### sync-rf.py

**Propósito:** Sincronizar 1 RF com Azure DevOps

**Uso:**
```bash
python tools/devops-sync/sync-rf.py RFXXX
```

**Ações:**
- Cria Feature no Azure DevOps (se não existir)
- Atualiza descrição com base em RF.md
- Sincroniza STATUS.yaml → Work Item State
- Atualiza campos customizados

---

### sync-user-stories.py

**Propósito:** Sincronizar User Stories de um RF

**Uso:**
```bash
python tools/devops-sync/sync-user-stories.py RFXXX
```

**Ações:**
- Lê user-stories.yaml
- Cria User Stories no Azure DevOps
- Faz linking com Feature (RF)
- Popula Sprint Backlog

---

### sync-all-rfs.py

**Propósito:** Sincronizar todos os RFs do projeto

**Uso:**
```bash
python tools/devops-sync/sync-all-rfs.py
```

**Ações:**
- Varre todos os RFs em `rf/`
- Sincroniza cada RF individualmente
- Gera relatório consolidado

---

## Categoria: Validação de Contratos

**Localização:** `tools/contract-validator/`

### validate-transitions.py

**Propósito:** Validar transições entre contratos

**Uso:**
```bash
python tools/contract-validator/validate-transitions.py RFXXX PROXIMO-CONTRATO
```

**Valida:**
- Transição permitida (ordem de execução)
- Pré-requisitos atendidos
- STATUS.yaml reflete estado atual

**Exit Codes:**
- `0` → Transição válida
- `!= 0` → Transição bloqueada

---

### validate-contract-compliance.py

**Propósito:** Validar conformidade com contrato ativo

**Uso:**
```bash
python tools/contract-validator/validate-contract-compliance.py RFXXX CONTRATO
```

**Valida:**
- Todos os itens do checklist obrigatório
- Arquivos esperados existem
- STATUS.yaml consistente

---

## Categoria: Executores de Testes

**Localização:** `tools/test-runners/`

### run-backend-tests.py

**Propósito:** Executar testes de backend

**Uso:**
```bash
python tools/test-runners/run-backend-tests.py RFXXX
```

**Executa:**
- Testes unitários (dotnet test)
- Testes de integração
- Testes de contrato (violações)

---

### run-e2e-tests.py

**Propósito:** Executar testes E2E Playwright

**Uso:**
```bash
python tools/test-runners/run-e2e-tests.py RFXXX
```

**Executa:**
- Testes E2E do RF
- Gera evidências (screenshots, logs)
- Valida cobertura UC

---

### run-all-tests.py

**Propósito:** Executar todas as baterias de testes

**Uso:**
```bash
python tools/test-runners/run-all-tests.py RFXXX
```

**Executa:**
- Backend tests
- E2E tests
- Security tests
- Gera relatório consolidado

---

## Categoria: Geradores de Relatórios

**Localização:** `tools/reports/`

### generate-coverage-report.py

**Propósito:** Gerar relatório de cobertura RF → UC → TC

**Uso:**
```bash
python tools/reports/generate-coverage-report.py RFXXX
```

**Saída:** `relatorios/AAAA-MM-DD-RFXXX-Coverage.md`

---

### generate-gap-report.py

**Propósito:** Gerar relatório de gaps (backend/frontend vs RF/UC/MD)

**Uso:**
```bash
python tools/reports/generate-gap-report.py RFXXX
```

**Saída:** `relatorios/AAAA-MM-DD-RFXXX-Gaps.md`

---

### generate-compliance-report.py

**Propósito:** Gerar relatório de conformidade de governança

**Uso:**
```bash
python tools/reports/generate-compliance-report.py RFXXX
```

**Saída:** `relatorios/AAAA-MM-DD-RFXXX-Compliance.md`

---

## Regras de Uso

1. **Automação obrigatória:** Ferramentas DEVEM ser executadas como parte dos contratos
2. **Exit codes:** Scripts DEVEM retornar exit code 0 (sucesso) ou != 0 (falha)
3. **Evidências:** Relatórios DEVEM ser salvos em `relatorios/`
4. **Nomenclatura:** `AAAA-MM-DD-RFXXX-Tipo.md`
5. **STATUS.yaml:** Scripts DEVEM atualizar STATUS.yaml quando aplicável

---

## Integração com Contratos

| Contrato | Tools Obrigatórias |
|----------|-------------------|
| CONTRATO-DOCUMENTACAO-ESSENCIAL | validator-rf-uc.py, validator-rl.py |
| CONTRATO-EXECUCAO-BACKEND | validator-governance.py, run-backend-tests.py |
| CONTRATO-EXECUCAO-FRONTEND | run-e2e-tests.py |
| CONTRATO-TESTER-BACKEND | run-backend-tests.py (violações) |
| CONTRATO-AUDITORIA-CONFORMIDADE | generate-gap-report.py |
| CONTRATO-DEVOPS-GOVERNANCA | sync-rf.py, sync-user-stories.py |

---

## Dependências

**Python:**
- Python 3.10+
- PyYAML
- requests (para Azure DevOps API)

**Instalação:**
```bash
pip install -r tools/requirements.txt
```

---

## Desenvolvimento de Novas Tools

Ao criar uma nova ferramenta:

1. **Escolha a categoria correta** (docs, devops-sync, contract-validator, test-runners, reports)
2. **Siga o padrão de exit codes** (0 = sucesso, != 0 = falha)
3. **Use nomenclatura clara** (verbo-substantivo.py)
4. **Documente no README** (este arquivo)
5. **Adicione à matriz de integração** com contratos

---

## Licença e Manutenção

- **Proprietário:** Equipe IControlIT
- **Manutenção:** Arquitetos e Desenvolvedores
- **Versionamento:** Seguir SemVer (X.Y.Z)

---

**Para mais detalhes sobre contratos, consulte:** `contracts/README.md`

**Para mais detalhes sobre checklists, consulte:** `checklists/README.md`

**Para mais detalhes sobre prompts, consulte:** `prompts/README.md`

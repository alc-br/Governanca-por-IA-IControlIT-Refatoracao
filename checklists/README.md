# Checklists - Estrutura Organizada (v2.0)

**Data de Reorganização:** 2026-01-01
**Versão:** 2.0

Este diretório contém **checklists em formato YAML** organizados por categoria.

## Formato YAML (Único Oficial)

- ✅ **YAML é o formato oficial** para checklists
- ✅ Permite automação e validação programática
- ✅ Integra com CI/CD pipelines
- ✅ **Estrutura organizada** espelhando contracts/ e prompts/
- ❌ **Checklists .md foram depreciados** (movidos para `deprecated/`)

## Estrutura de Pastas (Nova Organização)

```
checklists/
├── desenvolvimento/
│   ├── criacao/
│   │   ├── backend.yaml
│   │   └── frontend.yaml
│   ├── execucao/
│   │   └── frontend-adequacao.yaml    ← NOVO
│   ├── validacao/
│   │   ├── frontend.yaml              ← NOVO
│   │   └── testes.yaml
│   ├── manutencao/
│   │   └── manutencao.yaml
│   ├── debug.yaml
│   └── padrao.yaml
│
├── documentacao/
│   ├── geracao/
│   │   ├── rf-rl.yaml
│   │   ├── uc.yaml
│   │   ├── wf.yaml
│   │   ├── md.yaml
│   │   ├── uc-wf-md.yaml
│   │   ├── tc.yaml
│   │   └── mt.yaml
│   ├── documentacao.yaml
│   ├── essencial.yaml
│   └── testes.yaml
│
├── auditoria/
│   └── conformidade.yaml
│
└── devops/
    └── devops.yaml
```

## Padrão de Nomenclatura

**Nova estrutura:** `<categoria>/<subcategoria>/<nome>.yaml`

**Exemplos:**
- `desenvolvimento/criacao/backend.yaml`
- `desenvolvimento/execucao/frontend-adequacao.yaml`
- `desenvolvimento/validacao/frontend.yaml`
- `documentacao/geracao/uc.yaml`

## Mapeamento (Antiga → Nova Estrutura)

| Arquivo Antigo (Raiz) | Nova Localização |
|----------------------|------------------|
| checklist-backend.yaml | desenvolvimento/criacao/backend.yaml |
| checklist-frontend.yaml | desenvolvimento/criacao/frontend.yaml |
| checklist-manutencao.yaml | desenvolvimento/manutencao/manutencao.yaml |
| checklist-testes.yaml | desenvolvimento/validacao/testes.yaml |
| checklist-debug.yaml | desenvolvimento/debug.yaml |
| checklist-padrao-desenvolvimento.yaml | desenvolvimento/padrao.yaml |
| checklist-auditoria-conformidade.yaml | auditoria/conformidade.yaml |
| checklist-devops.yaml | devops/devops.yaml |
| checklist-documentacao.yaml | documentacao/documentacao.yaml |
| checklist-documentacao-essencial.yaml | documentacao/essencial.yaml |
| checklist-documentacao-uc.yaml | documentacao/geracao/uc.yaml |
| checklist-documentacao-testes.yaml | documentacao/testes.yaml |
| checklist-geracao-md.yaml | documentacao/geracao/md.yaml |
| checklist-geracao-rf-rl.yaml | documentacao/geracao/rf-rl.yaml |
| checklist-geracao-uc.yaml | documentacao/geracao/uc.yaml |
| checklist-geracao-wf.yaml | documentacao/geracao/wf.yaml |
| checklist-geracao-uc-wf-md.yaml | documentacao/geracao/uc-wf-md.yaml |
| checklist-documentacao-tc.yaml | documentacao/geracao/tc.yaml |
| checklist-documentacao-mt.yaml | documentacao/geracao/mt.yaml |

## Regra de Ouro

**1 Contrato = 1 Checklist = 1 Prompt**

- Contrato (em `contracts/`) define **o que pode ser feito**
- Checklist (em `checklists/`) define **como validar** que foi feito
- Prompt (em `prompts/`) define **como usuário solicita** execução
- **Estrutura espelhada** entre as 3 pastas

## Estrutura YAML (Exemplo)

```yaml
metadata:
  checklist_name: "checklist-documentacao-essencial"
  version: "1.0.0"
  contract: "CONTRATO-DOCUMENTACAO-ESSENCIAL"
  last_updated: "2025-12-28"

criteria:
  - id: "DOC-001"
    description: "RF-XXX.md criado com 5 seções obrigatórias"
    severity: "CRITICAL"
    validation_type: "file_exists"
    file_path: "rf/Fase-X/EPIC-YYY/RF-ZZZ/RF-ZZZ.md"

  - id: "DOC-002"
    description: "UC-RF-XXX.md criado com 5 casos de uso"
    severity: "CRITICAL"
    validation_type: "file_exists"
    file_path: "rf/Fase-X/EPIC-YYY/RF-ZZZ/UC-RF-ZZZ.md"

compliance_gates:
  - gate: "DOCUMENTATION_COMPLETE"
    required_criteria: ["DOC-001", "DOC-002", "DOC-003", "DOC-004", "DOC-005"]
    blocking: true
```

## Como Usar

1. **Durante execução de contrato:** Agente valida cada critério do checklist
2. **Automação CI/CD:** Scripts Python leem YAML e validam arquivos/código
3. **Validação manual:** Desenvolvedores podem consultar YAML para conferir itens

## Versionamento

- **Criado em:** 2025-12-28
- **Última atualização:** 2025-12-28
- **Versão:** 1.0.0

---

## Deprecated

Checklists em formato .md foram movidos para `deprecated/` e não devem mais ser utilizados.

---

**Para mais detalhes sobre contratos, consulte:** `contracts/README.md`

**Para mais detalhes sobre prompts, consulte:** `prompts/README.md`

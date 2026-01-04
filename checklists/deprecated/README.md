# Checklists de Governança

Esta pasta contém **checklists formais** utilizados por contratos de governança do projeto IControlIT.

---

## Estrutura

Cada checklist possui **duas versões**:

| Versão | Formato | Propósito |
|--------|---------|-----------|
| **Markdown** | `.md` | Leitura humana, documentação, guias |
| **YAML** | `.yaml` | Processamento automatizado, ferramentas, scripts |

---

## Checklists Disponíveis

### 1. Auditoria de Conformidade

**Arquivos:**
- [`auditoria-conformidade.md`](auditoria-conformidade.md)
- [`auditoria-conformidade.yaml`](auditoria-conformidade.yaml)

**Propósito:**
Validar conformidade entre especificação técnica (RF, UC, MD, WF) e implementação (backend/frontend).

**Contrato relacionado:**
- [`CONTRATO-AUDITORIA-CONFORMIDADE.md`](../contracts/CONTRATO-AUDITORIA-CONFORMIDADE.md)

**Categorias:**
- Backend: Entidades, Configurations, Commands, Validators, DTOs, Handlers, Endpoints, Seeds
- Frontend: Componentes, Formulários, Services, Rotas, Traduções, Models
- Integrações: Central de Funcionalidades, i18n, Auditoria, Multi-Tenancy, Permissões

**Classificação de severidade:**
- 🔴 **CRÍTICO:** Bloqueia RF
- 🟡 **IMPORTANTE:** RF pode ser concluído com ressalvas
- 🟢 **MENOR:** Divergência documental

---

### 2. Tester-Backend (Validação de Contrato)

**Arquivos:**
- [`CHECKLIST-CONTRATO-TESTER-BACKEND.md`](CHECKLIST-CONTRATO-TESTER-BACKEND.md)

**Propósito:**
Validar que o backend implementado respeita 100% o contrato definido através de testes de violação.

**Contrato relacionado:**
- [`CONTRATO-EXECUCAO-TESTER-BACKEND.md`](../contracts/CONTRATO-EXECUCAO-TESTER-BACKEND.md)

**Categorias:**
1. Governança Inicial
2. Análise do Contrato Oficial
3. Contrato de Teste Derivado
4. Matriz de Violação
5. Testes Automatizados de Violação
6. Execução dos Testes de Violação
7. Validação de Perfeição do Backend
8. Análise de Conformidade
9. Critério de Bloqueio (CRÍTICO)
10. Ambiguidades Identificadas
11. Status Final

**Filosofia:**
- Backend DEVE rejeitar 100% das violações
- Testes priorizam violação, não fluxo feliz
- Código que passa teste mas viola contrato = INVÁLIDO
- Agente TEM AUTORIDADE para bloquear merges

**Classificação:**
- ✅ **APROVADO:** Todas violações rejeitadas, backend perfeito
- ❌ **REPROVADO:** Violações aceitas, bloqueio ativado
- ⚠️ **BLOQUEADO:** Contrato ambíguo, esclarecimento necessário

---

## Uso dos Checklists

### Markdown (`.md`)

**Quando usar:**
- Durante execução manual de auditoria
- Como guia de referência durante desenvolvimento
- Em code reviews

**Como usar:**
- Abrir arquivo `.md` no editor
- Marcar itens como verificados conforme avança
- Usar como base para relatório de gaps

**Exemplo:**
```bash
code docs/checklists/auditoria-conformidade.md
```

---

### YAML (`.yaml`)

**Quando usar:**
- Processamento automatizado por scripts
- Ferramentas de CI/CD
- Geração de relatórios automatizados
- Dashboards de conformidade

**Como usar:**
- Parsear arquivo YAML em script Python/Node.js
- Iterar sobre categorias e itens
- Validar implementação contra checklist
- Gerar relatório automaticamente

**Exemplo (Python):**
```python
import yaml

with open('docs/checklists/auditoria-conformidade.yaml', 'r') as file:
    checklist = yaml.safe_load(file)

for categoria in checklist['categorias']:
    print(f"Verificando: {categoria['categoria']}")
    for item in categoria['itens']:
        print(f"  [{item['id']}] {item['texto']}")
        # Executar validação automatizada
```

---

## Estrutura YAML

Todos os checklists YAML seguem esta estrutura:

```yaml
metadata:
  nome: Nome do Checklist
  versao: 1.0.0
  data_criacao: YYYY-MM-DD
  contrato_origem: CONTRATO-*.md
  proposito: Descrição do propósito

categorias:
  - categoria: Nome da Categoria
    descricao: Descrição da categoria
    itens:
      - id: ID-ÚNICO
        texto: Texto do item de verificação
        severidade_se_falhar: CRITICO | IMPORTANTE | MENOR

severidades:
  CRITICO:
    impacto: Descrição do impacto
    acao: Ação a tomar
    simbolo: 🔴

  IMPORTANTE:
    impacto: Descrição do impacto
    acao: Ação a tomar
    simbolo: 🟡

  MENOR:
    impacto: Descrição do impacto
    acao: Ação a tomar
    simbolo: 🟢
```

---

## IDs dos Itens

Cada item possui um **ID único** seguindo este padrão:

```
[CAMADA]-[CATEGORIA]-[NÚMERO]
```

**Exemplos:**
- `BE-ENT-001`: Backend - Entidades - Item 001
- `FE-CMP-003`: Frontend - Componentes - Item 003
- `INT-I18-002`: Integrações - i18n - Item 002

**Prefixos de Camada:**
- `BE`: Backend
- `FE`: Frontend
- `INT`: Integrações

**Prefixos de Categoria (Backend):**
- `ENT`: Entidades
- `CFG`: Configurations
- `CMD`: Commands
- `VAL`: Validators
- `DTO`: DTOs
- `HND`: Handlers
- `END`: Endpoints
- `SED`: Seeds

**Prefixos de Categoria (Frontend):**
- `CMP`: Componentes
- `FRM`: Formulários
- `SVC`: Services
- `RTE`: Rotas
- `I18`: Traduções (i18n)
- `MDL`: Models

**Prefixos de Categoria (Integrações):**
- `CEN`: Central de Funcionalidades
- `I18`: i18n
- `AUD`: Auditoria
- `MTN`: Multi-Tenancy
- `PRM`: Permissões

---

## Versionamento

Checklists seguem **Semantic Versioning** (semver):

```
MAJOR.MINOR.PATCH
```

- **MAJOR:** Mudanças incompatíveis (ex: remover categoria inteira)
- **MINOR:** Adicionar novas categorias ou itens (compatível)
- **PATCH:** Correções de texto, descrições (compatível)

**Versão atual:**
- `auditoria-conformidade`: `1.0.0`

---

## Adicionando Novos Checklists

Para adicionar um novo checklist:

1. **Criar versão Markdown:**
   ```bash
   code docs/checklists/nome-do-checklist.md
   ```

2. **Criar versão YAML:**
   ```bash
   code docs/checklists/nome-do-checklist.yaml
   ```

3. **Seguir estrutura padrão:**
   - Metadata completa
   - Categorias bem definidas
   - IDs únicos para itens
   - Severidades classificadas

4. **Atualizar este README:**
   - Adicionar à seção "Checklists Disponíveis"
   - Documentar IDs específicos

5. **Referenciar em contrato:**
   - Atualizar contrato relacionado para mencionar o checklist
   - Incluir em `CLAUDE.md` se necessário

---

## Sincronização Markdown ↔ YAML

As versões Markdown e YAML DEVEM estar sincronizadas:

- Todo item em `.md` DEVE existir em `.yaml`
- Todo item em `.yaml` DEVE existir em `.md`
- IDs DEVEM corresponder
- Severidades DEVEM corresponder

**Processo de sincronização:**
1. Alterar versão Markdown (mais legível)
2. Atualizar versão YAML manualmente
3. Validar sincronização com script

---

## Scripts Auxiliares

### Validar Sincronização

```python
# tools/validate-checklist-sync.py
import yaml
import re

def validate_sync(md_path, yaml_path):
    # Extrair IDs do Markdown
    with open(md_path, 'r') as f:
        md_content = f.read()
        md_ids = set(re.findall(r'- \[.*?\] ([A-Z]+-[A-Z]+-\d+)', md_content))

    # Extrair IDs do YAML
    with open(yaml_path, 'r') as f:
        yaml_data = yaml.safe_load(f)
        yaml_ids = set()
        for cat in yaml_data['categorias']:
            for item in cat['itens']:
                yaml_ids.add(item['id'])

    # Comparar
    missing_in_yaml = md_ids - yaml_ids
    missing_in_md = yaml_ids - md_ids

    if missing_in_yaml:
        print(f"IDs ausentes no YAML: {missing_in_yaml}")

    if missing_in_md:
        print(f"IDs ausentes no Markdown: {missing_in_md}")

    if not missing_in_yaml and not missing_in_md:
        print("✅ Checklist sincronizado!")

validate_sync(
    'docs/checklists/auditoria-conformidade.md',
    'docs/checklists/auditoria-conformidade.yaml'
)
```

---

## Integração com Contratos

Checklists são **referenciados** por contratos, mas **NÃO são contratos**.

**Diferença:**

| Artefato | Propósito | Vinculante? |
|----------|-----------|-------------|
| **Contrato** | Define limites de atuação do agente | ✅ Sim |
| **Checklist** | Guia de validação e auditoria | ❌ Não |

**Relação:**
- Contratos **USAM** checklists
- Checklists **COMPLEMENTAM** contratos
- Contratos definem **O QUE** fazer
- Checklists definem **COMO** validar

---

## Zona de Escrita

Checklists são **READ-ONLY** durante execução de contratos.

**Permitido:**
- Ler checklists para guiar auditoria
- Usar como referência durante desenvolvimento

**Proibido:**
- Alterar checklists durante execução de contrato
- Criar checklists ad-hoc sem governança

**Atualização de checklists:**
- Somente sob contrato específico (ex: `CONTRATO-DOCUMENTACAO`)
- Requer aprovação formal
- Deve sincronizar `.md` e `.yaml`

---

## Histórico de Versões

| Data | Versão | Mudança | Checklist |
|------|--------|---------|-----------|
| 2025-12-25 | 1.0.0 | Criação inicial | auditoria-conformidade |

---

**Última atualização:** 2025-12-25
**Responsável:** Governança Técnica IControlIT

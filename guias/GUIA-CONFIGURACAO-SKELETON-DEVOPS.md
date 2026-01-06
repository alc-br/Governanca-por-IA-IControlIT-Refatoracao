# GUIA DE CONFIGURAÇÃO: SUPORTE A SKELETON NO AZURE DEVOPS

Este guia orienta passo a passo como configurar o Azure DevOps e os scripts de sincronização
para suportar o novo estado **Skeleton** (Base de Entidade).

---

## PRÉ-REQUISITOS

Antes de iniciar, certifique-se de que você tem:

- ✅ Acesso ao Azure DevOps do projeto
- ✅ Permissões de administrador no board
- ✅ Variáveis de ambiente configuradas (AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT)
- ✅ Python 3.x instalado
- ✅ Acesso ao repositório D:\IC2

---

## PASSO 1: CRIAR COLUNA "SKELETON" NO AZURE DEVOPS BOARD

### 1.1 Acessar Configurações do Board

1. Acesse Azure DevOps: `https://dev.azure.com/<sua-organizacao>/<seu-projeto>`
2. Navegue para **Boards** → **Boards**
3. Selecione o board **Features** (onde estão os RFs)
4. Clique no ícone de **engrenagem** (Settings) no canto superior direito

### 1.2 Adicionar Nova Coluna

1. Na aba **Columns**, clique em **+ New column**
2. Preencha os campos:
   - **Name:** `Skeleton`
   - **Description:** `Estrutura CRUD básica criada (backend + frontend)`
   - **WIP limit:** (deixe em branco ou defina um limite, ex: 10)
   - **State mapping:** `Active`

3. **Posicionar a coluna:**
   - Arraste a coluna "Skeleton" para ficar entre "Documentação" e "Backend"
   - A ordem deve ser: `Backlog → Documentação → Skeleton → Backend → Frontend → ...`

4. Clique em **Save and close**

### 1.3 Validar Criação da Coluna

1. Volte para o board principal
2. Verifique que a coluna "Skeleton" aparece na posição correta
3. Ordem esperada:
   ```
   Backlog | Documentação | Skeleton | Backend | Frontend | Documentacao Testes | Testes TI | Testes QA | Resolvido | Finalizado
   ```

---

## PASSO 2: APLICAR PATCH NOS SCRIPTS DE SINCRONIZAÇÃO

### 2.1 Fazer Backup dos Scripts Atuais

```bash
cd D:\IC2\tools\devops-sync
cp sync-board.py sync-board.py.bak
cp sync-rf.py sync-rf.py.bak
```

### 2.2 Aplicar Alterações em `sync-board.py`

Abra o arquivo `D:\IC2\tools\devops-sync\sync-board.py` e aplique as alterações:

#### Alteração 1: Atualizar COLUMNS (linha ~49-59)

**Localize:**
```python
COLUMNS = {
    "Backlog": {"state": "New", "order": 0},
    "Documentação": {"state": "Active", "order": 1},
    "Backend": {"state": "Active", "order": 2},
    "Frontend": {"state": "Active", "order": 3},
    ...
}
```

**Substitua por:**
```python
COLUMNS = {
    "Backlog": {"state": "New", "order": 0},
    "Documentação": {"state": "Active", "order": 1},
    "Skeleton": {"state": "Active", "order": 2},
    "Backend": {"state": "Active", "order": 3},
    "Frontend": {"state": "Active", "order": 4},
    "Documentacao Testes": {"state": "Active", "order": 5},
    "Testes TI": {"state": "Active", "order": 6},
    "Testes QA": {"state": "Testing", "order": 7},
    "Resolvido": {"state": "Resolved", "order": 8},
    "Finalizado": {"state": "Closed", "order": 9},
}
```

#### Alteração 2: Atualizar `determine_column` (linha ~113)

**Localize a função `determine_column` e adicione:**

```python
def determine_column(status_data):
    """..."""
    docs = status_data.get('documentacao', {})
    dev = status_data.get('desenvolvimento', {})

    # ADICIONAR ESTAS LINHAS:
    skeleton = status_data.get('skeleton', {})
    skeleton_criado = skeleton.get('criado', False)

    doc_testes = status_data.get('documentacao_testes', {})
    testes_ti = status_data.get('testes_ti', {})

    backend_status = dev.get('backend', {}).get('status', 'not_started')
    frontend_status = dev.get('frontend', {}).get('status', 'not_started')
    backend_done = backend_status == 'done'
    frontend_done = frontend_status == 'done'

    # ADICIONAR ESTAS LINHAS:
    backend_skeleton = backend_status == 'skeleton'
    frontend_skeleton = frontend_status == 'skeleton'

    # ... (resto da função)
```

**Localize a seção de determinação de coluna e ADICIONE antes de "# 2. Documentação":**

```python
    # 4. Frontend - backend done (pós-regularização)
    if backend_done and not frontend_done:
        return "Frontend", "Active"

    # 3. Backend - backend em regularização (in_progress) OU todos docs prontos
    if all_docs and (backend_status == 'in_progress' or (not backend_done and not backend_skeleton)):
        return "Backend", "Active"

    # 2.5 NOVO: Skeleton - skeleton criado OU backend/frontend = "skeleton"
    if skeleton_criado or backend_skeleton or frontend_skeleton:
        return "Skeleton", "Active"

    # 2. Documentação - RF.md existe mas falta algum doc
    if docs.get('rf', False) and not all_docs:
        return "Documentação", "Active"
```

### 2.3 Aplicar Mesmas Alterações em `sync-rf.py`

Repita as alterações acima no arquivo `sync-rf.py`:

1. Atualizar COLUMNS (mesma alteração)
2. Atualizar determine_column (mesma alteração)

---

## PASSO 3: TESTAR A CONFIGURAÇÃO

### 3.1 Criar STATUS.yaml de Teste

Crie um arquivo de teste em `D:\IC2\test-skeleton-status.yaml`:

```yaml
rf: RF999
fase: Fase-1-Sistema-Base
epic: EPIC001-SYS-Sistema-Infraestrutura
titulo: Teste Skeleton

documentacao:
  rf: True
  uc: True
  md: True
  wf: True

skeleton:
  criado: True
  data_criacao: "2025-12-27"
  observacao: "Skeleton criado. Aguarda CONTRATO DE REGULARIZAÇÃO DE BACKEND."

desenvolvimento:
  backend:
    status: skeleton
    branch: null
  frontend:
    status: skeleton
    branch: null

testes:
  backend: not_run
  frontend: not_run
  e2e: not_run
  seguranca: not_run

documentacao_testes:
  backend: False
  frontend: False
  e2e: False
  seguranca: False

testes_ti:
  backend: not_run
  frontend: not_run
  e2e: not_run
  seguranca: not_run

testes_qa:
  executado: False
  aprovado: False

devops:
  work_item_id: null
  test_plan_id: null
  last_sync: null
  board_column: "Skeleton"

governanca:
  contrato_ativo: "CONTRATO-BASE-DE-ENTIDADE"
  ultimo_manifesto: null
  proximo_contrato: "CONTRATO-REGULARIZACAO-BACKEND"
```

### 3.2 Testar Função `determine_column` Localmente

Crie um script de teste `D:\IC2\tools\devops-sync\test-determine-column.py`:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testa a função determine_column com STATUS.yaml de Skeleton"""

import sys
sys.path.append('D:/IC2/tools/devops-sync')

from sync_board import determine_column, parse_yaml_simple

# Ler STATUS.yaml de teste
with open('D:/IC2/test-skeleton-status.yaml', 'r', encoding='utf-8') as f:
    content = f.read()

status_data = parse_yaml_simple(content)
column, state = determine_column(status_data)

print(f"Coluna determinada: {column}")
print(f"State: {state}")

# Resultado esperado:
# Coluna determinada: Skeleton
# State: Active

if column == "Skeleton" and state == "Active":
    print("\n✅ TESTE PASSOU - Skeleton detectado corretamente")
else:
    print(f"\n❌ TESTE FALHOU - Esperado: (Skeleton, Active), Obtido: ({column}, {state})")
```

Execute:

```bash
cd D:\IC2\tools\devops-sync
python test-determine-column.py
```

**Resultado esperado:**
```
Coluna determinada: Skeleton
State: Active

✅ TESTE PASSOU - Skeleton detectado corretamente
```

### 3.3 Testar Sincronização com RF Real (Opcional)

Se você já tem um RF em estado Skeleton:

```bash
cd D:\IC2\tools\devops-sync
python sync-rf.py RF046  # Substitua pelo RF real
```

Verifique:
1. Script detecta `skeleton.criado = True`
2. Determina coluna "Skeleton"
3. Atualiza work item no DevOps
4. Work item aparece na coluna "Skeleton" do board

---

## PASSO 4: DOCUMENTAR O NOVO FLUXO

### 4.1 Atualizar Documentação de Workflow

Crie ou atualize o arquivo `D:\IC2\docs\devops\BOARD-WORKFLOW.md`:

```markdown
# WORKFLOW DO BOARD - AZURE DEVOPS

## Colunas e Transições

| Ordem | Coluna | State | Descrição | Critério de Entrada |
|-------|--------|-------|-----------|---------------------|
| 0 | Backlog | New | Estado inicial | RF criado |
| 1 | Documentação | Active | Documentação em andamento | RF.md existe |
| 2 | **Skeleton** | Active | **CRUD básico criado** | **skeleton.criado = True** |
| 3 | Backend | Active | Backend em regularização | Todos docs + backend in_progress |
| 4 | Frontend | Active | Frontend em desenvolvimento | backend.status = done |
| 5 | Documentacao Testes | Active | Criar TC docs | frontend.status = done |
| 6 | Testes TI | Active | Executar testes TI | Todos TC docs existem |
| 7 | Testes QA | Testing | Testes QA em andamento | Todos testes TI passaram |
| 8 | Resolvido | Resolved | Resolvido (manual) | Aprovação QA |
| 9 | Finalizado | Closed | Finalizado (manual) | Deploy produção |

## Novo Fluxo com Skeleton

```
Backlog
  ↓
Documentação (RF.md criado)
  ↓
Skeleton (CONTRATO-BASE-DE-ENTIDADE executado)
  ↓
Backend (CONTRATO-REGULARIZACAO-BACKEND executado)
  ↓
Frontend (CONTRATO-EXECUCAO-FRONTEND executado)
  ↓
Documentacao Testes (TC docs criados)
  ↓
Testes TI (Testes executados)
  ↓
Testes QA (QA aprova)
  ↓
Resolvido (Manual)
  ↓
Finalizado (Manual)
```

## Detecção Automática de Skeleton

O script `sync-board.py` detecta estado Skeleton quando:

1. `skeleton.criado = True` no STATUS.yaml, OU
2. `desenvolvimento.backend.status = "skeleton"`, OU
3. `desenvolvimento.frontend.status = "skeleton"`

Se qualquer condição for verdadeira → Coluna "Skeleton"
```

---

## PASSO 5: VALIDAÇÃO FINAL

### 5.1 Checklist de Validação

- [ ] Coluna "Skeleton" criada no Azure DevOps Board
- [ ] Coluna posicionada entre "Documentação" e "Backend"
- [ ] Arquivo `sync-board.py` atualizado
- [ ] Arquivo `sync-rf.py` atualizado
- [ ] Backup dos arquivos originais criado
- [ ] Teste local passou (determine_column)
- [ ] Sincronização com RF real funcionou (opcional)
- [ ] Documentação de workflow atualizada

### 5.2 Teste de Integração Completo

Execute um fluxo completo de teste:

1. **Criar RF de teste:**
   ```bash
   # Criar pasta de teste
   mkdir -p "D:/IC2/docs/rf-test/RF999-Teste-Skeleton"
   cp "D:/IC2/test-skeleton-status.yaml" "D:/IC2/docs/rf-test/RF999-Teste-Skeleton/STATUS.yaml"
   ```

2. **Sincronizar com DevOps:**
   ```bash
   cd D:\IC2\tools\devops-sync
   python sync-rf.py RF999
   ```

3. **Validar no Board:**
   - Acesse Azure DevOps → Boards → Board
   - Localize o work item RF999
   - Verifique que está na coluna "Skeleton"

4. **Limpar teste:**
   ```bash
   # Deletar work item de teste no Azure DevOps
   # Deletar pasta de teste
   rm -rf "D:/IC2/docs/rf-test/RF999-Teste-Skeleton"
   rm "D:/IC2/test-skeleton-status.yaml"
   ```

---

## TROUBLESHOOTING

### Problema: Coluna "Skeleton" não aparece no Board

**Solução:**
1. Verifique que a coluna foi criada corretamente em Board Settings
2. Verifique que a coluna está associada ao state "Active"
3. Atualize a página do board (F5)

### Problema: Script não detecta estado Skeleton

**Solução:**
1. Verifique que STATUS.yaml tem campo `skeleton.criado = True`
2. Verifique que `desenvolvimento.backend.status = "skeleton"`
3. Execute teste local com `test-determine-column.py`

### Problema: Work item não move para coluna "Skeleton"

**Solução:**
1. Verifique que campo WEF_KANBAN_COLUMN_FIELD foi descoberto corretamente
2. Verifique que coluna "Skeleton" existe no board
3. Verifique logs de erro do script sync-rf.py

### Problema: Erro ao executar sync-rf.py

**Solução:**
1. Verifique variáveis de ambiente (AZDO_ORG_URL, AZDO_PROJECT, AZDO_PAT)
2. Verifique conexão com Azure DevOps
3. Verifique permissões do token PAT

---

## PRÓXIMOS PASSOS

Após concluir esta configuração:

1. **Atualizar contratos existentes:**
   - Revisar RFs que estão em estado "Backend" mas deveriam ser "Skeleton"
   - Atualizar STATUS.yaml desses RFs

2. **Treinar equipe:**
   - Explicar novo fluxo com Skeleton
   - Explicar quando usar CONTRATO-BASE-DE-ENTIDADE

3. **Monitorar primeiros usos:**
   - Acompanhar primeiros RFs que usarem estado Skeleton
   - Ajustar documentação conforme feedback

---

## SUPORTE

Em caso de dúvidas ou problemas:

1. Consulte documentação adicional:
   - `D:\IC2\D:\IC2_Governanca\contracts\CONTRATO-BASE-DE-ENTIDADE.md`
   - `D:\IC2\docs\workflows\FLUXO-TRANSICAO-SKELETON.md`
   - `D:\IC2\tools\devops-sync\PATCH-SKELETON-SUPPORT.md`

2. Verifique logs de execução dos scripts

3. Reverta alterações se necessário (use backup .bak)

---

**FIM DO GUIA**

# VALIDADOR: Contrato de Validação WF e MD

**Versão:** 1.0
**Data:** 2026-01-02
**Autor:** Claude Sonnet 4.5
**Propósito:** Validar se WF-RFXXX.yaml e MD-RFXXX.yaml estão 100% conformes após execução dos contratos de geração

---

## CONTEXTO

Este validador executa **auditoria de conformidade** após a geração de WF e MD, verificando se:
- WF.yaml cobre 100% dos UCs
- WF.yaml possui estados obrigatórios (Loading, Vazio, Erro, Dados)
- WF.yaml documenta responsividade (Mobile, Tablet, Desktop)
- WF.yaml documenta acessibilidade (WCAG AA)
- MD.yaml deriva corretamente de RF/UC/WF
- MD.yaml possui multi-tenancy em TODAS as tabelas
- MD.yaml possui auditoria completa (5 campos) em TODAS as tabelas
- MD.yaml possui soft delete em TODAS as tabelas
- STATUS.yaml foi atualizado corretamente

---

## MODO DE OPERAÇÃO

**READ-ONLY:** Este validador NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

Se forem encontradas não-conformidades:
- Gerar relatório de gaps
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas

---

## PARTE 1: VALIDAÇÕES DE WIREFRAMES (WF)

### VALIDAÇÃO WF-1: Cobertura UC → WF (100% Obrigatória)

**Objetivo:** Garantir que TODOS os UCs têm representação visual em WF.

**Método:**
```python
# Extrair IDs de UCs do UC.yaml
uc_ids = set(re.findall(r'- id: "(UC\d+)"', uc_content))

# Extrair UCs referenciados no WF.yaml
wf_ucs = set(re.findall(r'uc_relacionado: "(UC\d+)"', wf_content))

# Calcular gaps
gaps = uc_ids - wf_ucs
cobertura = len(wf_ucs) / len(uc_ids) * 100 if uc_ids else 0
```

**Critério de aprovação:**
- ✅ `cobertura == 100%` AND `len(gaps) == 0`
- ❌ Qualquer gap = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO WF-1: APROVADO
   Cobertura: 13/13 UCs (100%)
   Gaps: 0
```

---

### VALIDAÇÃO WF-2: Estados Obrigatórios (Loading, Vazio, Erro, Dados)

**Objetivo:** Garantir que TODOS os wireframes possuem os 4 estados obrigatórios.

**Método:**
```python
# Para cada wireframe, verificar se possui:
estados_obrigatorios = ["Loading", "Vazio", "Erro", "Dados"]

for wf in wireframes:
    estados_presentes = extract_estados(wf)
    missing = set(estados_obrigatorios) - set(estados_presentes)
    if missing:
        gaps.append(f"WF{wf['id']}: Faltam estados {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os WFs têm os 4 estados
- ❌ Qualquer WF sem estado = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-2: APROVADO
   Wireframes: 5
   Estados obrigatórios: 4/4 em todos os WFs
   Violações: 0
```

---

### VALIDAÇÃO WF-3: Responsividade Documentada (Mobile, Tablet, Desktop)

**Objetivo:** Garantir que TODOS os wireframes documentam responsividade.

**Método:**
```python
dispositivos_obrigatorios = ["Mobile", "Tablet", "Desktop"]

for wf in wireframes:
    dispositivos_documentados = extract_responsividade(wf)
    missing = set(dispositivos_obrigatorios) - set(dispositivos_documentados)
    if missing:
        gaps.append(f"WF{wf['id']}: Faltam dispositivos {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os WFs documentam os 3 dispositivos
- ❌ Qualquer WF sem dispositivo = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-3: APROVADO
   Wireframes: 5
   Dispositivos: Mobile, Tablet, Desktop documentados em todos
   Violações: 0
```

---

### VALIDAÇÃO WF-4: Acessibilidade WCAG AA

**Objetivo:** Garantir que acessibilidade está documentada.

**Critérios verificados:**
- Labels em português claro
- Navegação por teclado
- Contraste mínimo WCAG AA
- ARIA labels (quando aplicável)

**Método:**
```python
criterios_wcag = ["labels_pt", "navegacao_teclado", "contraste_minimo"]

for wf in wireframes:
    criterios_presentes = extract_acessibilidade(wf)
    missing = set(criterios_wcag) - set(criterios_presentes)
    if missing:
        gaps.append(f"WF{wf['id']}: Faltam critérios {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os WFs documentam acessibilidade
- ❌ Qualquer WF sem acessibilidade = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-4: APROVADO
   Wireframes: 5
   Critérios WCAG AA: 3/3 documentados em todos
   Violações: 0
```

---

### VALIDAÇÃO WF-5: Componentes de Interface Documentados

**Objetivo:** Garantir que TODOS os componentes de interface estão documentados.

**Componentes a verificar:**
- Campos de formulário (inputs, selects, textareas, etc.)
- Botões (ações primárias e secundárias)
- Tabelas/listas (colunas, paginação, ordenação)
- Modais/dialogs (confirmações, feedbacks)
- Navegação (breadcrumbs, tabs, menus)
- Feedback visual (loading spinners, mensagens de erro/sucesso)

**Método:**
```python
componentes_obrigatorios_por_tipo = {
    "listagem": ["tabela", "paginacao", "ordenacao", "filtros", "botao_novo"],
    "criacao": ["formulario", "campos_obrigatorios", "botao_salvar", "botao_cancelar"],
    "edicao": ["formulario", "campos_editaveis", "botao_salvar", "botao_cancelar"],
    "visualizacao": ["campos_readonly", "botao_editar", "botao_voltar"],
    "confirmacao": ["modal_confirmacao", "mensagem", "botao_confirmar", "botao_cancelar"]
}

for wf in wireframes:
    tipo = wf['tipo']
    componentes_esperados = componentes_obrigatorios_por_tipo.get(tipo, [])
    componentes_presentes = extract_componentes(wf)
    missing = set(componentes_esperados) - set(componentes_presentes)
    if missing:
        gaps.append(f"WF{wf['id']}: Faltam componentes {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os WFs documentam componentes esperados conforme tipo
- ❌ Qualquer componente faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-5: APROVADO
   Wireframes: 5
   Componentes documentados: 100%
   Violações: 0
```

---

### VALIDAÇÃO WF-6: Eventos de Interação Documentados

**Objetivo:** Garantir que TODOS os eventos de interação do usuário estão documentados.

**Eventos a verificar:**
- Cliques em botões (onClick)
- Submissão de formulários (onSubmit)
- Mudança de valores (onChange)
- Navegação entre telas (onNavigate)
- Abertura/fechamento de modais (onOpen/onClose)

**Método:**
```python
eventos_obrigatorios_por_acao = {
    "Criar": ["onClick_salvar", "onClick_cancelar", "onSubmit_formulario"],
    "Editar": ["onClick_salvar", "onClick_cancelar", "onSubmit_formulario"],
    "Excluir": ["onClick_excluir", "onClick_confirmar_exclusao", "onClick_cancelar_exclusao"],
    "Visualizar": ["onClick_editar", "onClick_voltar"],
    "Filtrar": ["onChange_filtro", "onClick_aplicar_filtro", "onClick_limpar_filtro"]
}

for wf in wireframes:
    acoes = wf['acoes_permitidas']
    for acao in acoes:
        eventos_esperados = eventos_obrigatorios_por_acao.get(acao, [])
        eventos_presentes = extract_eventos(wf, acao)
        missing = set(eventos_esperados) - set(eventos_presentes)
        if missing:
            gaps.append(f"WF{wf['id']}: Ação '{acao}' sem eventos {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os eventos de cada ação estão documentados
- ❌ Qualquer evento faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-6: APROVADO
   Wireframes: 5
   Eventos documentados: 100%
   Violações: 0
```

---

### VALIDAÇÃO WF-7: Seções Obrigatórias Presentes

**Objetivo:** Garantir que TODAS as seções obrigatórias do WF estão presentes.

**Seções obrigatórias:**
- `objetivo` (descrição do propósito do wireframe)
- `principios_design` (diretrizes de design aplicadas)
- `mapa_telas` (estrutura de navegação)
- `componentes` (lista de componentes de interface)
- `eventos` (lista de eventos de interação)
- `estados` (Loading, Vazio, Erro, Dados)
- `responsividade` (Mobile, Tablet, Desktop)
- `acessibilidade` (WCAG AA)
- `contratos_comportamento` (regras de validação, transições de estado)

**Método:**
```python
secoes_obrigatorias = [
    "objetivo", "principios_design", "mapa_telas", "componentes",
    "eventos", "estados", "responsividade", "acessibilidade",
    "contratos_comportamento"
]

for wf in wireframes:
    secoes_presentes = extract_secoes(wf)
    missing = set(secoes_obrigatorias) - set(secoes_presentes)
    if missing:
        gaps.append(f"WF{wf['id']}: Faltam seções {missing}")
```

**Critério de aprovação:**
- ✅ TODOS os WFs têm todas as seções obrigatórias
- ❌ Qualquer seção faltando = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-7: APROVADO
   Wireframes: 5
   Seções obrigatórias: 9/9 em todos
   Violações: 0
```

---

### VALIDAÇÃO WF-8: Contratos de Comportamento Completos

**Objetivo:** Garantir que regras de validação e transições de estado estão documentadas.

**Contratos a verificar:**
- Validações de formulário (campos obrigatórios, formatos, limites)
- Transições de estado (habilitação/desabilitação de botões)
- Regras de negócio aplicadas na UI
- Mensagens de erro/sucesso
- Confirmações necessárias

**Método:**
```python
for wf in wireframes:
    contratos = extract_contratos_comportamento(wf)

    # Verificar validações de formulário
    if wf['tipo'] in ['criacao', 'edicao']:
        if not has_validacoes_formulario(contratos):
            gaps.append(f"WF{wf['id']}: Sem validações de formulário")

    # Verificar transições de estado
    if not has_transicoes_estado(contratos):
        gaps.append(f"WF{wf['id']}: Sem transições de estado")

    # Verificar mensagens
    if not has_mensagens_feedback(contratos):
        gaps.append(f"WF{wf['id']}: Sem mensagens de feedback")
```

**Critério de aprovação:**
- ✅ TODOS os WFs têm contratos de comportamento completos
- ❌ Qualquer contrato faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-8: APROVADO
   Wireframes: 5
   Contratos de comportamento: 100%
   Violações: 0
```

---

### VALIDAÇÃO WF-9: WF.yaml Aderente ao Template

**Objetivo:** Garantir que WF.yaml segue a estrutura do template oficial.

**Verificações:**

1. **Cabeçalho completo:**
   ```yaml
   wf:
     documentacao: "RFXXX"
     versao: "2.0"
     data: "YYYY-MM-DD"
   ```

2. **Estrutura de cada WF:**
   - `id`, `nome`, `tipo`, `uc_relacionado` presentes
   - `intencao`, `acoes_permitidas` presentes
   - `componentes`, `eventos` presentes
   - `estados.loading`, `estados.vazio`, `estados.erro`, `estados.dados` presentes
   - `responsividade.mobile`, `responsividade.tablet`, `responsividade.desktop` presentes
   - `acessibilidade` presente
   - `contratos_comportamento` presente

3. **Seção final:**
   - `historico` presente com pelo menos 1 versão

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO WF-9: APROVADO
   Template: WF.yaml 100% aderente ao v2.0
   Seções obrigatórias: 12/12 presentes
```

---

## PARTE 2: VALIDAÇÕES DE MODELO DE DADOS (MD)

### VALIDAÇÃO MD-1: Derivação de RF/UC/WF

**Objetivo:** Garantir que MD deriva corretamente das fontes.

**Verificações:**
- Entidades do MD mapeiam entidades do RF
- Campos do MD cobrem operações dos UCs
- Índices do MD refletem filtros do WF

**Método:**
```python
# Extrair entidades do RF
rf_entities = extract_entities_from_rf(rf_content)

# Extrair tabelas do MD
md_tables = extract_tables_from_md(md_content)

# Comparar
gaps = documentacao_entities - md_tables
```

**Critério de aprovação:**
- ✅ Todas as entidades do RF estão no MD
- ❌ Entidade não mapeada = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-1: APROVADO
   Entidades do RF: 3
   Tabelas no MD: 3
   Cobertura: 100%
```

---

### VALIDAÇÃO MD-2: Multi-tenancy Obrigatório

**Objetivo:** Garantir que TODAS as tabelas têm `cliente_id` ou `empresa_id`.

**Método:**
```python
for table in md_tables:
    campos = extract_campos(table)
    has_multi_tenancy = 'cliente_id' in campos or 'empresa_id' in campos
    if not has_multi_tenancy:
        gaps.append(f"Tabela {table['nome']}: Sem multi-tenancy")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm multi-tenancy
- ❌ Qualquer tabela sem multi-tenancy = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-2: APROVADO
   Tabelas: 3
   Com multi-tenancy: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-3: Auditoria Completa (5 campos)

**Objetivo:** Garantir que TODAS as tabelas têm campos de auditoria.

**Campos obrigatórios:**
- `created_at` (DATETIME, default GETDATE())
- `created_by` (GUID, FK para usuario, NULL)
- `updated_at` (DATETIME, NULL)
- `updated_by` (GUID, FK para usuario, NULL)
- `deleted_at` (DATETIME, NULL - soft delete)

**Método:**
```python
campos_auditoria = ['created_at', 'created_by', 'updated_at', 'updated_by', 'deleted_at']

for table in md_tables:
    campos = extract_campos(table)
    missing = set(campos_auditoria) - set(campos)
    if missing:
        gaps.append(f"Tabela {table['nome']}: Faltam {missing}")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm os 5 campos
- ❌ Qualquer tabela sem campo = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-3: APROVADO
   Tabelas: 3
   Com auditoria completa (5 campos): 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-4: Soft Delete Obrigatório

**Objetivo:** Garantir que TODAS as tabelas têm `deleted_at`.

**Método:**
```python
for table in md_tables:
    campos = extract_campos(table)
    if 'deleted_at' not in campos:
        gaps.append(f"Tabela {table['nome']}: Sem soft delete")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm `deleted_at`
- ❌ Qualquer tabela sem soft delete = **CRÍTICO** (bloqueante)

**Saída esperada:**
```
✅ VALIDAÇÃO MD-4: APROVADO
   Tabelas: 3
   Com soft delete: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-5: Constraints Obrigatórias

**Objetivo:** Garantir que TODAS as tabelas têm constraints completas.

**Constraints obrigatórias:**
- PK constraint (id)
- FK multi-tenancy (CASCADE)
- FKs auditoria (SET NULL)
- UNIQUE por tenant (quando aplicável)

**Método:**
```python
for table in md_tables:
    constraints = extract_constraints(table)

    # Verificar PK
    if not has_pk_constraint(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem PK constraint")

    # Verificar FK multi-tenancy
    if not has_fk_multi_tenancy_cascade(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem FK multi-tenancy CASCADE")

    # Verificar FKs auditoria
    if not has_fk_auditoria_set_null(constraints):
        gaps.append(f"Tabela {table['nome']}: Sem FKs auditoria SET NULL")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm constraints completas
- ❌ Qualquer constraint faltando = **CRÍTICO**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-5: APROVADO
   Tabelas: 3
   Com constraints completas: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-6: Índices Obrigatórios

**Objetivo:** Garantir que TODAS as tabelas têm índices necessários.

**Índices obrigatórios:**
- Índice PK
- Índice multi-tenancy
- Índices de performance (conforme filtros do WF)

**Método:**
```python
for table in md_tables:
    indices = extract_indices(table)

    # Verificar índice PK
    if not has_pk_index(indices):
        gaps.append(f"Tabela {table['nome']}: Sem índice PK")

    # Verificar índice multi-tenancy
    if not has_multi_tenancy_index(indices):
        gaps.append(f"Tabela {table['nome']}: Sem índice multi-tenancy")
```

**Critério de aprovação:**
- ✅ TODAS as tabelas têm índices obrigatórios
- ❌ Qualquer índice faltando = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-6: APROVADO
   Tabelas: 3
   Com índices obrigatórios: 3/3 (100%)
   Violações: 0
```

---

### VALIDAÇÃO MD-7: MD.yaml Aderente ao Template

**Objetivo:** Garantir que MD.yaml segue a estrutura do template oficial.

**Verificações:**

1. **Cabeçalho completo:**
   ```yaml
   metadata:
     versao: "2.0"
     data: "YYYY-MM-DD"
     documentacao_relacionada:
       id: "RFXXX"
     padroes:
       multi_tenancy: true
       auditoria: true
       soft_delete: true
   ```

2. **Estrutura de cada entidade:**
   - `nome`, `descricao` presentes
   - `campos` com todos os campos obrigatórios
   - `indices` presentes
   - `constraints` presentes

3. **Seções finais:**
   - `observacoes` presente
   - `historico` presente com pelo menos 1 versão

**Critério de aprovação:**
- ✅ Todas as seções obrigatórias presentes
- ❌ Qualquer seção ausente = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO MD-7: APROVADO
   Template: MD.yaml 100% aderente ao v2.0
   Seções obrigatórias: 8/8 presentes
```

---

## PARTE 3: VALIDAÇÕES DE STATUS.YAML

### VALIDAÇÃO STATUS-1: STATUS.yaml Atualizado

**Objetivo:** Verificar se STATUS.yaml foi atualizado corretamente.

**Campos esperados:**
```yaml
documentacao:
  wf: true
  md: true
```

**Critério de aprovação:**
- ✅ `documentacao.wf = true` AND `documentacao.md = true`
- ❌ Qualquer campo ausente ou `false` = **IMPORTANTE**

**Saída esperada:**
```
✅ VALIDAÇÃO STATUS-1: APROVADO
   STATUS.yaml: documentacao.wf = true
   STATUS.yaml: documentacao.md = true
```

---

## RELATÓRIO DE VALIDAÇÃO

**Template de saída:**

```markdown
# RELATÓRIO DE VALIDAÇÃO - WF-RFXXX e MD-RFXXX
**Data:** YYYY-MM-DD
**Validador:** VALIDADOR-WF-MD v1.0

---

## RESUMO EXECUTIVO

| Validação | Status | Severidade | Resultado |
|-----------|--------|------------|-----------|
| **PARTE 1: WIREFRAMES (WF)** |
| WF-1. Cobertura UC → WF | ✅ PASS | CRÍTICO | 13/13 (100%) |
| WF-2. Estados obrigatórios | ✅ PASS | CRÍTICO | 4/4 em todos |
| WF-3. Responsividade | ✅ PASS | IMPORTANTE | 3/3 em todos |
| WF-4. Acessibilidade WCAG AA | ✅ PASS | IMPORTANTE | 3/3 em todos |
| WF-5. Componentes interface | ✅ PASS | IMPORTANTE | 100% documentados |
| WF-6. Eventos interação | ✅ PASS | IMPORTANTE | 100% documentados |
| WF-7. Seções obrigatórias | ✅ PASS | CRÍTICO | 9/9 em todos |
| WF-8. Contratos comportamento | ✅ PASS | IMPORTANTE | 100% completos |
| WF-9. WF.yaml → Template | ✅ PASS | IMPORTANTE | 12/12 seções |
| **PARTE 2: MODELO DE DADOS (MD)** |
| MD-1. Derivação RF/UC/WF | ✅ PASS | CRÍTICO | 3/3 (100%) |
| MD-2. Multi-tenancy | ✅ PASS | CRÍTICO | 3/3 (100%) |
| MD-3. Auditoria completa | ✅ PASS | CRÍTICO | 5/5 campos em todos |
| MD-4. Soft delete | ✅ PASS | CRÍTICO | 3/3 (100%) |
| MD-5. Constraints | ✅ PASS | CRÍTICO | 3/3 (100%) |
| MD-6. Índices | ✅ PASS | IMPORTANTE | 3/3 (100%) |
| MD-7. MD.yaml → Template | ✅ PASS | IMPORTANTE | 8/8 seções |
| **PARTE 3: STATUS** |
| STATUS-1. STATUS.yaml | ✅ PASS | IMPORTANTE | wf=true, md=true |

**PONTUAÇÃO FINAL:** 17/17 PASS (100%)

**VEREDICTO:** ✅ **APROVADO** - WF-RFXXX e MD-RFXXX estão 100% conformes (ZERO GAPS)

---

## GAPS IDENTIFICADOS

**Nenhum gap de qualquer severidade identificado.** ✅

---

## RECOMENDAÇÕES

Nenhuma ação corretiva necessária. RFXXX pode prosseguir para criação de TC/MT.

---

**Validador:** Claude Sonnet 4.5
**Tempo de validação:** ~5 minutos
**Arquivos analisados:** WF-RFXXX.yaml, MD-RFXXX.yaml, UC-RFXXX.yaml, RF-RFXXX.yaml, STATUS.yaml
```

---

## CRITÉRIOS DE APROVAÇÃO/REPROVAÇÃO

### ✅ APROVADO (100%)

**Exigências ABSOLUTAS:**
- ✅ Todas as 17 validações PASS
- ✅ ZERO gaps de qualquer severidade (CRÍTICO, IMPORTANTE, MENOR)
- ✅ WF cobre 100% dos UCs
- ✅ WF documenta TODOS os componentes, eventos, estados e seções
- ✅ TODAS as tabelas com multi-tenancy
- ✅ TODAS as tabelas com auditoria completa (5 campos)
- ✅ TODAS as tabelas com soft delete
- ✅ STATUS.yaml atualizado

---

### ❌ REPROVADO (<100%)

**Motivos de REPROVAÇÃO (lista não-exaustiva):**
- ❌ 16/17 ou menos validações PASS
- ❌ **QUALQUER gap CRÍTICO** (ex: tabela sem multi-tenancy)
- ❌ **QUALQUER gap IMPORTANTE** (ex: WF sem responsividade)
- ❌ **QUALQUER gap MENOR**
- ❌ UC sem representação visual no WF
- ❌ WF sem estados obrigatórios
- ❌ WF sem componentes/eventos documentados
- ❌ WF sem seções obrigatórias
- ❌ Tabela sem auditoria completa

---

## MODO DE EXECUÇÃO

**Prompt de ativação:**
```
Executar VALIDADOR-WF-MD para RFXXX.
Seguir D:\IC2\CLAUDE.md.
```

**Comportamento esperado:**
1. Leitura de WF-RFXXX.yaml, MD-RFXXX.yaml, UC-RFXXX.yaml, RF-RFXXX.yaml, STATUS.yaml
2. Execução das 17 validações (9 WF + 7 MD + 1 STATUS)
3. Geração de relatório de gaps (se houver)
4. Veredicto final: APROVADO ou REPROVADO
5. **OPCIONAL:** Salvar relatório em `.temp_ia/validacao-wf-md-RFXXX-relatorio.md` (recomendado mas não obrigatório)

**IMPORTANTE:**
- Este validador NÃO corrige problemas, apenas IDENTIFICA
- Ausência de relatório **NÃO reprova** validação (gap MENOR)

---

## Git Operations (SOMENTE SE APROVADO 100% SEM RESSALVAS)

**Versão:** 1.0
**Data:** 2026-01-28

### Regra Fundamental

**SE E SOMENTE SE:**
1. ✅ Validação passou **100%** (17/17 PASS)
2. ✅ **ZERO** gaps de qualquer severidade
3. ✅ Branch atual **NÃO** é `dev`

**ENTÃO:** Executar Git Operations automaticamente.

### Sequência Obrigatória

```bash
# 1. Verificar branch atual
current_branch=$(git rev-parse --abbrev-ref HEAD)

if [ "$current_branch" == "dev" ]; then
    echo "✅ Já está em dev. Sem necessidade de merge."
    exit 0
fi

# 2. Verificar se há alterações pendentes
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Alterações pendentes detectadas. Commitando..."

    # 3. Adicionar TODAS as alterações
    git add .

    # 4. Criar commit
    git commit -m "docs(RFXXX): WF+MD validados 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
fi

# 5. Merge com dev
git checkout dev
git pull origin dev
git merge $current_branch --no-ff -m "merge($current_branch): WF+MD validados 100%

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# 6. Push para remoto
git push origin dev

# 7. Deletar branch local (opcional)
git branch -d $current_branch

echo "✅ Git Operations concluídas. WF+MD mergeados em dev."
```

### Critérios de Bloqueio

**NÃO executar Git Operations se:**
- ❌ Validação < 100%
- ❌ Qualquer gap CRÍTICO
- ❌ Qualquer gap IMPORTANTE
- ❌ Qualquer gap MENOR
- ❌ Já está em branch `dev`
- ❌ Conflitos de merge detectados

---

**Fim do Validador**

# CONTRATO DE GERAÇÃO RF (REQUISITO FUNCIONAL)

**Versão:** 1.0
**Data:** 2026-01-03
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **documentação completa de Requisito Funcional (RF)** NOVO (sem legado), garantindo:

- ✅ **RF Limpo**: Contrato moderno, SEM referências a legado
- ✅ **11 Seções Obrigatórias**: Estrutura completa conforme template
- ✅ **Mínimo 10 Regras de Negócio**: Documentação detalhada
- ✅ **Integr Soluções Obrigatórias**: i18n, auditoria, RBAC, Central de Funcionalidades
- ✅ **Validação Automática**: validator-docs.py obrigatório
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **RFXXX.md** - Requisito Funcional (documentação completa)
2. **RFXXX.yaml** - Estrutura canônica do RF
3. **STATUS.yaml** - Governança e rastreabilidade
4. **documentacao-funcional.md** - Índice atualizado (se existir)

✅ **Validação obrigatória** após RF criado
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **RF Novo**: NÃO é adequação de legado (sem ASPX, WebServices, SQL)
2. **Contrato Moderno**: Apenas funcionalidades novas, sem memória legado
3. **11 Seções Completas**: Conforme template RF.md v2.0
4. **Mínimo 10 RNs**: Regras de negócio detalhadas
5. **Integrações Obrigatórias**: i18n, auditoria, RBAC, Central de Funcionalidades
6. **Validação Bloqueante**: validator-docs.py DEVE passar (exit code 0)

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Requisito Funcional |
| **Escopo** | Criação completa de RFXXX.md e RFXXX.yaml (RF NOVO) |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme docs/contracts/documentacao/execucao/rf-criacao.md para RFXXX"**

Exemplo:
```
Conforme docs/contracts/documentacao/execucao/rf-criacao.md para RF070.
Seguir CLAUDE.md.
```

**IMPORTANTE:** Este contrato é para RFs **NOVOS** (sem legado).
Se o RF tem legado (ASPX, WebServices, SQL), use `rf-rl-criacao.md` (RF + RL juntos).

---

## 3. Objetivo do Contrato

Gerar **2 arquivos fundamentais** que definem o Requisito Funcional:

1. **RFXXX.md** - Requisito Funcional (contrato funcional completo)
2. **RFXXX.yaml** - Estrutura canônica do RF

Além disso, atualizar:

3. **STATUS.yaml** - Controle de governança e progresso do RF
4. **documentacao-funcional.md** - Índice de documentação (se existir)

### 3.1 Princípio do RF Limpo (Sem Legado)

**REGRA CRÍTICA:** RF NOVO não contém referências a legado.

- ✅ SEM telas ASPX
- ✅ SEM WebServices legado
- ✅ SEM stored procedures legado
- ✅ SEM tabelas legadas
- ✅ SEM código VB.NET/SQL copiado
- ✅ APENAS funcionalidades novas e modernas

**Se houver legado:**
- ❌ NÃO usar este contrato
- ✅ Usar `rf-rl-criacao.md` (que cria RF + RL juntos)

### 3.2 Princípio das 11 Seções Obrigatórias

**REGRA CRÍTICA:** RF.md DEVE ter TODAS as 11 seções do template.

1. **Seção 1: Objetivo** - O que o RF faz
2. **Seção 2: Escopo** - O que está incluído e fora
3. **Seção 3: Conceitos de Negócio** - Terminologia e conceitos-chave
4. **Seção 4: Funcionalidades** - Catálogo de funcionalidades (RF-CRUD, RF-VAL, RF-SEC)
5. **Seção 5: Regras de Negócio** - Mínimo 10 RNs (RN-MOD-XXX-01, ...)
6. **Seção 6: Estados e Transições** - Máquina de estados (se aplicável)
7. **Seção 7: Permissões (RBAC)** - Matriz de permissões obrigatória
8. **Seção 8: Endpoints da API** - Contratos HTTP (GET, POST, PUT, DELETE)
9. **Seção 9: Modelo de Dados** - Entidades principais e relacionamentos
10. **Seção 10: Dependências** - Outros RFs que este RF depende
11. **Seção 11: Integrações Obrigatórias** - i18n, auditoria, RBAC, Central

### 3.3 Princípio das Integrações Obrigatórias

**REGRA CRÍTICA:** TODO RF DEVE integrar com:

1. **i18n (Internacionalização)** - Seção 11.1
   - Chaves de tradução (pt-BR, en-US, es-ES)
   - Nomenclatura: `rf.xxx.campo`, `rf.xxx.validacao.erro`

2. **Auditoria** - Seção 11.2
   - Campos obrigatórios: created_at, created_by, updated_at, updated_by, deleted_at
   - Soft delete obrigatório

3. **RBAC (Permissões)** - Seção 11.3
   - Matriz de permissões completa (view_any, view, create, update, delete)
   - Escopo (Developer/Sistema/Cliente/Fornecedor)

4. **Central de Funcionalidades** - Seção 11.4
   - Cadastro da funcionalidade
   - Ícone, ordem, menu pai
   - Permissões associadas

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | `D:\IC2\docs\rf\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |
| **TOOLS_PATH** | `D:\IC2\docs\tools\docs\` |

### 4.2 Validador Obrigatório

| Ferramenta | Caminho |
|------------|---------|
| **validator-docs.py** | `D:\IC2\docs\tools\docs\validator-docs.py` |

**Execução:**
```bash
python docs/tools/docs/validator-docs.py RFXXX
```

**Exit Code:**
- `0` = APROVADO (RF válido)
- `≠ 0` = REPROVADO (RF inválido, corrigir e revalidar)

---

## 5. Pré-requisitos (Bloqueantes)

Antes de iniciar, o agente DEVE validar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF existe | `docs/rf/[Fase]/[EPIC]/RFXXX/` criada | Sim |
| Templates acessíveis | `docs/templates/RF.md` e `RF.yaml` disponíveis | Sim |
| Nenhum legado identificado | SEM ASPX, WebServices, SQL legado | Sim |
| STATUS.yaml NÃO existe | Novo RF (não é adequação) | Sim |

**Se STATUS.yaml já existir:**
- ❌ Este contrato NÃO é aplicável (RF já foi criado)
- ✅ Usar contrato de adequação/manutenção

**Se legado for identificado:**
- ❌ Este contrato NÃO é aplicável
- ✅ Usar `rf-rl-criacao.md` (RF + RL juntos)

---

## 6. Workflow de Execução

### Passo 1: Validação de Pré-requisitos

```python
# 1. Verificar pasta do RF
pasta_rf = f"docs/rf/{fase}/{epic}/{rf}/"
if not exists(pasta_rf):
    ERRO("Pasta do RF não existe")

# 2. Verificar templates
if not exists("docs/templates/RF.md"):
    ERRO("Template RF.md não encontrado")
if not exists("docs/templates/RF.yaml"):
    ERRO("Template RF.yaml não encontrado")

# 3. Verificar que NÃO há legado
if has_legado(rf):
    ERRO("RF tem legado - usar rf-rl-criacao.md")

# 4. Verificar que STATUS.yaml NÃO existe
if exists(f"{pasta_rf}/STATUS.yaml"):
    ERRO("RF já existe - usar contrato de adequação")
```

**Se QUALQUER bloqueio:** PARAR e AVISAR.

### Passo 2: Análise de Requisitos

```python
# 1. Ler especificações fornecidas pelo usuário
requisitos = ler_requisitos_usuario()

# 2. Identificar tipo de RF
tipo_rf = identificar_tipo(requisitos)  # crud | leitura | integracao | batch

# 3. Identificar entidades principais
entidades = identificar_entidades(requisitos)

# 4. Identificar regras de negócio (mínimo 10)
regras = extrair_regras_negocio(requisitos)
if len(regras) < 10:
    AVISO("Mínimo 10 RNs - solicitar mais ao usuário")

# 5. Identificar permissões RBAC
permissoes = identificar_permissoes(requisitos, tipo_rf)

# 6. Identificar endpoints da API
endpoints = definir_endpoints(requisitos, tipo_rf)
```

### Passo 3: Geração de RFXXX.md

```python
# 1. Ler template RF.md
template_md = ler_arquivo("docs/templates/RF.md")

# 2. Preencher Seção 1: Objetivo
secao_1 = gerar_objetivo(requisitos)

# 3. Preencher Seção 2: Escopo
secao_2 = gerar_escopo(requisitos)

# 4. Preencher Seção 3: Conceitos de Negócio
secao_3 = gerar_conceitos(requisitos, entidades)

# 5. Preencher Seção 4: Funcionalidades
secao_4 = gerar_catalogo_funcionalidades(tipo_rf)

# 6. Preencher Seção 5: Regras de Negócio (mínimo 10)
secao_5 = gerar_regras_negocio(regras)

# 7. Preencher Seção 6: Estados e Transições
secao_6 = gerar_estados(requisitos, tipo_rf)

# 8. Preencher Seção 7: Permissões (RBAC)
secao_7 = gerar_matriz_permissoes(permissoes)

# 9. Preencher Seção 8: Endpoints da API
secao_8 = gerar_endpoints(endpoints)

# 10. Preencher Seção 9: Modelo de Dados
secao_9 = gerar_modelo_dados(entidades)

# 11. Preencher Seção 10: Dependências
secao_10 = gerar_dependencias(requisitos)

# 12. Preencher Seção 11: Integrações Obrigatórias
secao_11 = gerar_integracoes_obrigatorias(rf)

# 13. Montar arquivo final
rf_md = montar_rf_md(template_md, secoes)

# 14. Salvar RFXXX.md
salvar_arquivo(f"{pasta_rf}/RF{rf}.md", rf_md)
```

### Passo 4: Geração de RFXXX.yaml

```python
# 1. Ler template RF.yaml
template_yaml = ler_arquivo("docs/templates/RF.yaml")

# 2. Preencher campos obrigatórios
rf_yaml = {
    "rf": {
        "id": rf,
        "nome": nome_rf,
        "versao": "1.0",
        "data": data_hoje(),
        "fase": fase,
        "epic": epic,
        "status": "draft",
        "tipo_rf": tipo_rf
    },
    "descricao": descricao,
    "escopo": escopo,
    "entidades": entidades,
    "regras_negocio": regras,
    "estados": estados,
    "transicoes": transicoes,
    "permissoes": permissoes,
    "integracoes": integracoes,
    "seguranca": seguranca,
    "rastreabilidade": rastreabilidade,
    "catalog": catalog
}

# 3. Salvar RFXXX.yaml
salvar_yaml(f"{pasta_rf}/RF{rf}.yaml", rf_yaml)
```

### Passo 5: Criação de STATUS.yaml

```python
# 1. Ler template STATUS.yaml
template_status = ler_arquivo("docs/templates/STATUS.yaml")

# 2. Preencher campos iniciais
status_yaml = {
    "rf": rf,
    "fase": fase,
    "epic": epic,
    "titulo": nome_rf,
    "skeleton": {
        "criado": False,
        "data_criacao": None,
        "observacao": ""
    },
    "documentacao": {
        "rf": True,  # ← RF criado
        "uc": False,
        "md": False,
        "wf": False,
        "rl": False,
        "tc": False
    },
    "desenvolvimento": {
        "backend": {"status": "not_started", "branch": None},
        "frontend": {"status": "not_started", "branch": None}
    },
    "testes": {
        "backend": "not_run",
        "frontend": "not_run",
        "e2e": "not_run",
        "seguranca": "not_run"
    },
    "validacoes": {
        "rf_yaml_sincronizado": True,
        "rf_11_secoes_completas": True,
        "rf_minimo_10_regras": True,
        "rf_integracoes_obrigatorias": True
    }
}

# 3. Salvar STATUS.yaml
salvar_yaml(f"{pasta_rf}/STATUS.yaml", status_yaml)
```

### Passo 6: Validação Automática Obrigatória

```python
# 1. Executar validador
exit_code = executar("python docs/tools/docs/validator-docs.py {rf}")

# 2. Interpretar resultado
if exit_code == 0:
    print("✅ RF APROVADO - Validação passou")
else:
    print("❌ RF REPROVADO - Corrigir e revalidar")
    PARAR()
```

**IMPORTANTE:** Se validação FALHAR, o agente DEVE corrigir e revalidar até passar.

### Passo 7: Atualização de documentacao-funcional.md (se existir)

```python
# 1. Verificar se existe
doc_funcional = f"docs/rf/documentacao-funcional.md"
if exists(doc_funcional):
    # 2. Adicionar seção do RF
    adicionar_secao_rf(doc_funcional, rf, nome_rf, fase, epic)
```

---

## 7. Estrutura de Saída

### 7.1 Arquivos Gerados

```
docs/rf/[Fase]/[EPIC]/RFXXX/
├── RFXXX.md                    ← RF completo (11 seções)
├── RFXXX.yaml                  ← Estrutura canônica
└── STATUS.yaml                 ← Governança
```

### 7.2 STATUS.yaml Atualizado

```yaml
documentacao:
  rf: true                      ← RF criado
  uc: false
  wf: false
  md: false
  rl: false
  tc: false

validacoes:
  rf_yaml_sincronizado: true
  rf_11_secoes_completas: true
  rf_minimo_10_regras: true
  rf_integracoes_obrigatorias: true
```

---

## 8. Checklist Obrigatório

O agente DEVE seguir o checklist em:

```
D:\IC2\docs\checklists\documentacao\geracao\rf.yaml
```

**Seções do checklist:**
- `pre_requisitos`: Pasta, templates, sem legado
- `estrutura_rf_md`: 11 seções completas
- `estrutura_rf_yaml`: Campos obrigatórios
- `integracoes_obrigatorias`: i18n, auditoria, RBAC, Central
- `validacao_automatica`: validator-docs.py executado
- `status_yaml_atualizacao`: STATUS.yaml criado
- `resultado_final`: APROVADO/REPROVADO

---

## 9. Validações Obrigatórias

### 9.1 Validações de Estrutura

| Validação | Critério |
|-----------|----------|
| 11 seções presentes | RF.md contém TODAS as seções do template |
| Mínimo 10 RNs | Seção 5 tem pelo menos 10 regras de negócio |
| Integrações obrigatórias | Seção 11 documenta i18n, auditoria, RBAC, Central |
| Sem referências legado | RF.md NÃO contém ASPX, WebServices, SQL |
| Sincronização MD ↔ YAML | RF.md e RF.yaml 100% consistentes |

### 9.2 Validações de Conteúdo

| Validação | Critério |
|-----------|----------|
| Objetivo claro | Seção 1 explica claramente o que o RF faz |
| Escopo definido | Seção 2 lista incluído e fora de escopo |
| Catálogo completo | Seção 4 tem RF-CRUD, RF-VAL, RF-SEC conforme tipo |
| Matriz RBAC | Seção 7 tem permissões completas |
| Endpoints API | Seção 8 documenta todos os contratos HTTP |

### 9.3 Validação Automática (Bloqueante)

```bash
python docs/tools/docs/validator-docs.py RFXXX
```

**Exit Code 0** = APROVADO
**Exit Code ≠ 0** = REPROVADO (corrigir e revalidar)

---

## 10. Regras de Qualidade

### 10.1 RF Limpo (Sem Legado)

- ✅ SEM telas ASPX mencionadas
- ✅ SEM WebServices legado documentados
- ✅ SEM stored procedures legado
- ✅ SEM tabelas legadas
- ✅ SEM código VB.NET/SQL copiado
- ✅ APENAS contrato moderno

### 10.2 Completude Estrutural

- ✅ 11 seções completas (conforme template)
- ✅ Mínimo 10 regras de negócio
- ✅ Catálogo de funcionalidades completo
- ✅ Matriz RBAC documentada
- ✅ Endpoints da API documentados
- ✅ Modelo de dados descrito

### 10.3 Integrações Obrigatórias

- ✅ i18n: Chaves de tradução documentadas
- ✅ Auditoria: 5 campos obrigatórios (created_at, created_by, updated_at, updated_by, deleted_at)
- ✅ RBAC: Matriz de permissões completa
- ✅ Central: Funcionalidade cadastrada

### 10.4 Sincronização MD ↔ YAML

- ✅ Todas as RNs em RF.md estão em RF.yaml
- ✅ Todos os endpoints em RF.md estão em RF.yaml
- ✅ Todas as permissões em RF.md estão em RF.yaml
- ✅ 100% de consistência

---

## 11. Bloqueios Críticos

O agente DEVE PARAR se:

| Bloqueio | Condição |
|----------|----------|
| Pasta não existe | `docs/rf/[Fase]/[EPIC]/RFXXX/` não criada |
| Templates não acessíveis | `RF.md` ou `RF.yaml` não disponíveis |
| Legado identificado | RF tem ASPX, WebServices, SQL legado |
| STATUS.yaml já existe | RF já foi criado (usar adequação) |
| Validação falhou | validator-docs.py exit code ≠ 0 |
| Menos de 10 RNs | Seção 5 tem < 10 regras de negócio |
| Integrações faltando | Seção 11 incompleta |

---

## 12. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `/docs/contracts/documentacao/execucao/rf-criacao.md` | Este contrato |
| `/docs/prompts/documentacao/execucao/rf-criacao.md` | Prompt de ativação |
| `/docs/checklists/documentacao/geracao/rf.yaml` | Checklist de validação |
| `/docs/templates/RF.md` | Template RF Markdown |
| `/docs/templates/RF.yaml` | Template RF YAML |
| `/docs/tools/docs/validator-docs.py` | Validador automático |

---

## 13. Próximo Passo

Após RF criado e aprovado:

```
Conforme docs/contracts/documentacao/execucao/uc-criacao.md para RFXXX.
Seguir CLAUDE.md.
```

Criar **Casos de Uso (UC)** derivados do RF.

---

## 14. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2026-01-03 | Criação do contrato de geração de RF (NOVO) |

---

**FIM DO CONTRATO**

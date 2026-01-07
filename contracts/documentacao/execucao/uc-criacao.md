# CONTRATO DE GERAÇÃO UC (CASOS DE USO)

**Versão:** 1.0
**Data:** 2025-12-31
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **documentação completa e rastreável de Casos de Uso (UC)** com base no **Requisito Funcional (RF)** já criado, garantindo:

- ✅ **Cobertura Total (100%)**: UC cobre 100% do RF
- ✅ **Rastreabilidade Completa**: RF → UC
- ✅ **Validação Automática**: validator-rf-uc.py obrigatório
- ✅ **Coerência Estrutural**: RF ↔ UC sempre consistentes
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **UC-RFXXX.md** - Casos de Uso (derivado do RF)
2. **UC-RFXXX.yaml** - Estrutura canônica dos UCs
3. **STATUS.yaml** - Atualização de governança

✅ **Validação obrigatória** após UC criado
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

### 🎯 Princípios Fundamentais

1. **Derivação do RF**: UC deriva EXCLUSIVAMENTE do RFXXX.yaml/md
2. **Cobertura Total**: UC cobre 100% das funcionalidades do RF
3. **Validação Bloqueante**: validator-rf-uc.py DEVE passar (exit code 0)
4. **Coerência Estrutural**: RF ↔ UC sempre consistentes
5. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA - CORREÇÃO OBRIGATÓRIA ANTES DE FALHA

**Detectar gaps de cobertura NÃO é falha imediata - é GATILHO OBRIGATÓRIO para correção.**

Se durante a validação for identificado que os UCs existentes NÃO cobrem 100% do RF, o agente DEVE:

1. **Identificar UCs faltantes** - Listar exatamente quais funcionalidades do RF não estão cobertas
2. **Criar/Complementar UCs** - Adicionar os casos de uso necessários em UC-RFXXX.md e UC-RFXXX.yaml
3. **Revalidar** - Executar validator-rf-uc.py novamente após complementação
4. **Só então declarar PASS ou FAIL** - Falha só ocorre se, após correção completa, validador ainda não passar

Ou seja, TUDO no RFXXX deve estar coberto no UC-RFXXX, todas as regras de negocio deve ter um UC que as cubra 100%.

**Se já houver um documento de UC criado:**
- ✅ Validar se está dentro dos padrões do template
- ✅ Verificar se todos os cenários cobrem 100% do RF
- ✅ Se faltar caso de uso: **CRIAR/COMPLEMENTAR IMEDIATAMENTE**
- ✅ Revalidar até atingir 100% de conformidade
- ❌ NUNCA parar apenas por identificar gaps - sempre corrigir primeiro

**Fluxo correto:**
```
Validação → Gaps identificados? → SIM → Criar UCs faltantes → Revalidar → PASS/FAIL
                                → NÃO → PASS
```

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Casos de Uso |
| **Escopo** | Criação completa de UC-RFXXX.md e UC-RFXXX.yaml |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-UC para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-UC para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **2 arquivos fundamentais** que complementam o Requisito Funcional (RF) com **casos de uso**:

1. **UC-RFXXX.md** - Casos de Uso (contrato comportamental)
2. **UC-RFXXX.yaml** - Estrutura canônica dos UCs

Além disso, atualizar:

3. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Cobertura Total (100%)

**REGRA CRÍTICA:** Os UCs DEVEM cobrir **100% ABSOLUTO** das funcionalidades do RF.

- ✅ TODA funcionalidade do RF DEVE estar presente em pelo menos um UC
- ✅ TODA regra de negócio do RF DEVE ser referenciada explicitamente em UC
- ✅ Nenhum UC pode introduzir comportamento NÃO previsto no RF
- ✅ Funcionalidades fora de escopo no RF NÃO geram UCs

**Se houver dúvida sobre alguma funcionalidade:**
- ❌ NÃO assumir que pode ser ignorada
- ❌ NÃO deixar de documentar
- ✅ Criar UC correspondente
- ✅ Validar contra RF com validator-rf-uc.py

### 3.2 Princípio da Rastreabilidade Completa

**REGRA CRÍTICA:** Cada UC DEVE apontar para funcionalidades do RF.

- ✅ Todo UC em UC-RFXXX.yaml DEVE ter campo `covers.rf_items` preenchido
- ✅ Toda RN-UC-XXX DEVE referenciar RN-RFXXX correspondente
- ✅ Criar matriz de rastreabilidade: RF → UC

**Formato obrigatório de rastreabilidade:**

Em **UC-RFXXX.yaml**:
```yaml
casos_de_uso:
  - id: "UC01"
    nome: "Criar Entidade"
    covers:
      documentacao_items:
        - "RF-CRUD-01"  # Funcionalidade de criação no RF
        - "RF-VAL-01"   # Validação de campos obrigatórios
        - "RF-SEC-01"   # Permissão create
```

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\UC-RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\UC-RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`
- Qualquer arquivo que não seja os 3 listados acima

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF | Pasta já criada em `rf/[Fase]/[EPIC]/RFXXX/` | Sim |
| RFXXX.md | RF criado e aprovado | Sim |
| RFXXX.yaml | RF estruturado e sincronizado | Sim |
| Templates | Templates UC.md, UC.yaml disponíveis | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| RF Validado | STATUS.yaml com `documentacao.rf = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura do RF (OBRIGATÓRIA)

Antes de criar qualquer documento, o agente DEVE:

#### 1.1 Ler RFXXX.md Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\RFXXX.md`
- Entender TODAS as funcionalidades descritas
- Identificar TODAS as regras de negócio (RN-RFXXX-NNN)
- Mapear endpoints, permissões e integrações

#### 1.2 Ler RFXXX.yaml Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\RFXXX.yaml`
- Extrair catálogo de funcionalidades (`rf_items`)
- Mapear regras de negócio estruturadas
- Identificar entidades principais

**Critério de completude:**
- ✅ RF.md lido integralmente
- ✅ RF.yaml lido integralmente
- ✅ Funcionalidades mapeadas
- ✅ Regras de negócio identificadas

---

### Fase 2: Criação UC-RFXXX.md (Casos de Uso)

#### 2.1 Criar UC-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\UC.md`

**Estrutura obrigatória:**

1. **Seção 1: Objetivo do Documento**
   - Descrição do propósito dos UCs
   - Referência ao RF

2. **Seção 2: Sumário de Casos de Uso**
   - Tabela com todos os UCs (ID, Nome, Ator Principal)

3. **Seção 3: Padrões Gerais**
   - Isolamento por tenant
   - Permissões obrigatórias
   - Auditoria automática

4. **Seção 4+: Casos de Uso Detalhados**
   - UC00: Listar [Entidade]
   - UC01: Criar [Entidade]
   - UC02: Visualizar [Entidade]
   - UC03: Editar [Entidade]
   - UC04: Excluir [Entidade]

**Cada UC DEVE conter:**
- **Objetivo:** Descrição clara do propósito
- **Pré-condições:** Autenticação, permissões, estado inicial
- **Pós-condições:** Estado final esperado
- **Fluxo Principal:** Passos numerados (1, 2, 3...)
- **Fluxos Alternativos:** FA-XX-01, FA-XX-02...
- **Fluxos de Exceção:** FE-XX-01, FE-XX-02...
- **Regras de Negócio:** RN-UC-XX-NNN

**PROIBIDO em UC-RFXXX.md:**
- ❌ Copiar código do legado
- ❌ Criar funcionalidades não previstas no RF
- ❌ Omitir funcionalidades do RF

**OBRIGATÓRIO em UC-RFXXX.md:**
- ✅ Cobrir 100% do RF
- ✅ Quantidade de UCs necessária para cobrir 100% do RF (para RFs CRUD: padrão UC00-UC04)
- ✅ Todos os UCs com fluxos principais, alternativos e de exceção
- ✅ Regras de negócio rastreadas ao RF

---

### Fase 3: Criação UC-RFXXX.yaml (Estruturado)

#### 3.1 Criar UC-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\UC.yaml`

**Estrutura obrigatória:**

```yaml
uc:
  documentacao: "RFXXX"
  versao: "1.0"
  data: "YYYY-MM-DD"

casos_de_uso:
  - id: "UC00"
    nome: "Listar [Entidade]"
    ator_principal: "usuario_autenticado"

    covers:
      documentacao_items:
        - "RF-FUNCIONALIDADE-01"  # ID da funcionalidade no RFXXX.yaml
        - "RF-FUNCIONALIDADE-02"
      uc_items:
        - id: "UC00-FP-01"
          title: "Fluxo principal - listagem"
          required: true
        - id: "UC00-FA-01"
          title: "Filtrar por status"
          required: false
        - id: "UC00-FE-01"
          title: "Sem permissão view_any"
          required: true

    precondicoes:
      - permissao: "entidade.view_any"

    gatilho: "Usuario acessa funcionalidade pelo menu"

    fluxo_principal:
      - passo: 1
        ator: "usuario"
        acao: "acessa_menu"
      - passo: 2
        ator: "sistema"
        acao: "validar_permissao"
      - passo: 3
        ator: "sistema"
        acao: "listar_registros_tenant"
      - passo: 4
        ator: "sistema"
        acao: "exibir_lista"

    fluxos_alternativos:
      - id: "FA-UC00-01"
        condicao: "usuario_aplica_filtro"
        resultado: "lista_filtrada"

    fluxos_excecao:
      - id: "FE-UC00-01"
        condicao: "sem_permissao"
        resultado: "acesso_negado"

    regras_aplicadas:
      - "RN-RFXXX-01"

    resultado_final:
      estado: "lista_exibida"

  # Repetir para UC01, UC02, UC03, UC04...

exclusions:
  uc_items: []

historico:
  - versao: "1.0"
    data: "YYYY-MM-DD"
    autor: "Agência ALC - alc.dev.br"
    descricao: "Versão inicial"
```

**Regra CRÍTICA:** UC-RFXXX.yaml DEVE estar 100% sincronizado com UC-RFXXX.md
- Todos os UCs do MD devem estar no YAML
- Todos os fluxos do MD devem estar no YAML
- Campo `covers.rf_items` OBRIGATÓRIO para rastreabilidade

---

### Fase 3.5: Detecção Automática de Funcionalidades Críticas ✨ NOVO

**OBJETIVO:** Detectar automaticamente funcionalidades que podem ter sido omitidas e criar UCs correspondentes.

Esta fase é executada **ANTES da validação** para garantir cobertura 100% desde o início.

---

#### 3.5.1 MELHORIA #1: Detecção Automática de Entidades Órfãs

**PROBLEMA IDENTIFICADO:** RFs com múltiplas entidades no MD podem ter apenas algumas cobertas por UCs.

**SOLUÇÃO:**

```python
import re
import yaml
from pathlib import Path

rf_base_path = Path('rf/[FASE]/[EPIC]/RFXXX/')
md_file = documentacao_base_path / 'MD-RFXXX.md'
uc_file = documentacao_base_path / 'UC-RFXXX.yaml'

# Ler MD para extrair entidades
if md_file.exists():
    with open(md_file) as f:
        md_content = f.read()

    # Extrair entidades (tabelas CREATE TABLE)
    entities = re.findall(r'CREATE TABLE (\w+)', md_content)
    print(f"📊 Entidades no MD: {entities}")

    # Ler UC.yaml para identificar entidades cobertas
    with open(uc_file) as f:
        uc_data = yaml.safe_load(f)

    covered_entities = set()
    for uc in uc_data.get('casos_de_uso', []):
        nome = uc.get('nome', '')
        # Extrair nome da entidade (ex: "Listar Sistema_Parametro" → Sistema_Parametro)
        entity_match = re.search(r'(Sistema_\w+|[A-Z][a-zA-Z_]+)', nome)
        if entity_match:
            covered_entities.add(entity_match.group(1))

    print(f"✅ Entidades cobertas: {covered_entities}")

    # Calcular gaps de entidades
    orphan_entities = set(entities) - covered_entities

    if orphan_entities:
        print(f"⚠️ Entidades órfãs detectadas (SEM UCs): {orphan_entities}")
        print(f"🤖 AÇÃO AUTOMÁTICA: Criando UCs CRUD para entidades órfãs...")

        # Para cada entidade órfã, criar 5 UCs CRUD
        for entity in orphan_entities:
            next_uc_num = len(uc_data.get('casos_de_uso', []))

            crud_ucs = [
                {
                    'id': f'UC{next_uc_num:02d}',
                    'nome': f'Listar {entity}',
                    'tipo': 'leitura',
                    'ator_principal': 'usuario_autenticado',
                    'covers': {'rf_items': []},  # Preencher com RNs relacionadas
                    'precondicoes': [{'permissao': f'{entity.lower()}.view_any'}],
                    'gatilho': f'Usuário acessa menu {entity}',
                    'fluxo_principal': [
                        {'passo': 1, 'ator': 'usuario', 'acao': 'Acessa menu'},
                        {'passo': 2, 'ator': 'sistema', 'acao': 'Valida permissão'},
                        {'passo': 3, 'ator': 'sistema', 'acao': 'Lista registros do tenant'},
                        {'passo': 4, 'ator': 'sistema', 'acao': 'Exibe lista paginada'}
                    ],
                    'regras_aplicadas': [],
                    'resultado_final': {'estado': 'lista_exibida'}
                },
                {
                    'id': f'UC{next_uc_num+1:02d}',
                    'nome': f'Criar {entity}',
                    'tipo': 'crud',
                    'ator_principal': 'usuario_autenticado'
                },
                {
                    'id': f'UC{next_uc_num+2:02d}',
                    'nome': f'Visualizar {entity}',
                    'tipo': 'leitura',
                    'ator_principal': 'usuario_autenticado'
                },
                {
                    'id': f'UC{next_uc_num+3:02d}',
                    'nome': f'Editar {entity}',
                    'tipo': 'crud',
                    'ator_principal': 'usuario_autenticado'
                },
                {
                    'id': f'UC{next_uc_num+4:02d}',
                    'nome': f'Excluir {entity}',
                    'tipo': 'crud',
                    'ator_principal': 'usuario_autenticado'
                }
            ]

            uc_data['casos_de_uso'].extend(crud_ucs)
            print(f"   ✅ UC{next_uc_num:02d}-UC{next_uc_num+4:02d}: CRUD completo para {entity}")

        # Salvar UC.yaml atualizado
        with open(uc_file, 'w') as f:
            yaml.dump(uc_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print(f"✅ {len(orphan_entities)} entidades órfãs agora têm UCs CRUD completos")
    else:
        print(f"✅ Todas as entidades do MD têm UCs correspondentes")
else:
    print(f"⚠️ MD-RFXXX.md não encontrado - pulando detecção de entidades órfãs")
```

**Critério de aceite:**
- ✅ Todas as entidades do MD têm pelo menos 1 UC
- ✅ Entidades órfãs recebem automaticamente UC CRUD (5 UCs por entidade)

---

#### 3.5.2 MELHORIA #2: Detecção Automática de Jobs Background

**PROBLEMA IDENTIFICADO:** Jobs Hangfire/background não são documentados como UCs.

**SOLUÇÃO:**

```python
# Detectar jobs background
rf_file = documentacao_base_path / 'RFXXX.yaml'
with open(rf_file) as f:
    documentacao_content = f.read().lower()

keywords_jobs = ['hangfire', 'job', 'scheduler', 'cron', 'background', 'recorrente', 'periódico', 'agendado']
jobs_detected = []

for keyword in keywords_jobs:
    if keyword in documentacao_content:
        jobs_detected.append(keyword)

if jobs_detected:
    print(f"⚠️ Jobs background detectados: {set(jobs_detected)}")
    print(f"🤖 AÇÃO AUTOMÁTICA: Criando UCs para jobs background...")

    # Criar UC para job background (se ainda não existir)
    job_uc_exists = any(
        uc.get('tipo') == 'background_job'
        for uc in uc_data.get('casos_de_uso', [])
    )

    if not job_uc_exists:
        next_uc_num = len(uc_data.get('casos_de_uso', []))

        job_uc = {
            'id': f'UC{next_uc_num:02d}',
            'nome': 'Job Background - [Descrição do Job]',
            'tipo': 'background_job',
            'ator_principal': 'Sistema (Hangfire Scheduler)',
            'covers': {'rf_items': []},  # Preencher com RNs relacionadas ao job
            'precondicoes': [
                {'condicao': 'Job Hangfire configurado'},
                {'condicao': 'Scheduler ativo'}
            ],
            'gatilho': 'Expressão CRON dispara job',
            'fluxo_principal': [
                {'passo': 1, 'ator': 'sistema', 'acao': 'Job dispara no horário configurado'},
                {'passo': 2, 'ator': 'sistema', 'acao': 'Hangfire enfileira job'},
                {'passo': 3, 'ator': 'sistema', 'acao': 'Worker executa método do job'},
                {'passo': 4, 'ator': 'sistema', 'acao': 'Job marca conclusão (success/failure)'}
            ],
            'configuracao_job': {
                'expressao_cron': '[definir]',
                'timezone': 'America/Sao_Paulo',
                'retry_policy': 'exponential_backoff',
                'max_retries': 3
            },
            'regras_aplicadas': [],
            'resultado_final': {'estado': 'job_executado'}
        }

        uc_data['casos_de_uso'].append(job_uc)
        print(f"   ✅ UC{next_uc_num:02d}: Job background criado")

        # Salvar UC.yaml
        with open(uc_file, 'w') as f:
            yaml.dump(uc_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    else:
        print(f"✅ Job background já documentado em UC existente")
else:
    print(f"✅ Nenhum job background identificado no RF")
```

**Critério de aceite:**
- ✅ Jobs detectados têm UC com `tipo: background_job`
- ✅ Seção `configuracao_job` presente

---

#### 3.5.3 MELHORIA #3: Detecção Automática de Integrações Externas

**PROBLEMA IDENTIFICADO:** Integrações com APIs externas (SMTP, Azure, BrasilAPI) não são documentadas.

**SOLUÇÃO:**

```python
# Detectar integrações externas
keywords_integracoes = [
    'api', 'smtp', 'sendgrid', 'aws ses', 'azure', 'graph',
    'brasil api', 'via cep', 'externo', 'third-party', 'webhook'
]
integracoes_detected = []

for keyword in keywords_integracoes:
    if keyword in documentacao_content:
        integracoes_detected.append(keyword)

if integracoes_detected:
    print(f"⚠️ Integrações externas detectadas: {set(integracoes_detected)}")
    print(f"🤖 AÇÃO AUTOMÁTICA: Criando UCs para integrações externas...")

    # Criar UC para integração (se ainda não existir)
    integracao_uc_exists = any(
        uc.get('tipo') == 'integracao_externa'
        for uc in uc_data.get('casos_de_uso', [])
    )

    if not integracao_uc_exists:
        next_uc_num = len(uc_data.get('casos_de_uso', []))

        integracao_uc = {
            'id': f'UC{next_uc_num:02d}',
            'nome': 'Integração - [Nome do Sistema Externo]',
            'tipo': 'integracao_externa',
            'ator_principal': 'Sistema',
            'covers': {'rf_items': []},
            'sistema_externo': {
                'nome': '[Nome do sistema]',
                'tipo': 'REST API | SOAP | GraphQL',
                'autenticacao': 'OAuth2 | API Key | Certificate',
                'endpoint_base': '[URL base]',
                'documentacao': '[URL da documentação oficial]'
            },
            'mapeamento_dados': {
                'direcao': 'IControlIT → Externo | Externo → IControlIT | Bidirectional',
                'transformacoes': []
            },
            'fluxo_principal': [
                {'passo': 1, 'ator': 'sistema', 'acao': 'Autentica no sistema externo'},
                {'passo': 2, 'ator': 'sistema', 'acao': 'Prepara payload'},
                {'passo': 3, 'ator': 'sistema', 'acao': 'Envia request'},
                {'passo': 4, 'ator': 'sistema', 'acao': 'Processa response'}
            ],
            'regras_aplicadas': [],
            'resultado_final': {'estado': 'integracao_completa'}
        }

        uc_data['casos_de_uso'].append(integracao_uc)
        print(f"   ✅ UC{next_uc_num:02d}: Integração externa criada")

        # Salvar UC.yaml
        with open(uc_file, 'w') as f:
            yaml.dump(uc_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    else:
        print(f"✅ Integração externa já documentada em UC existente")
else:
    print(f"✅ Nenhuma integração externa identificada no RF")
```

**Critério de aceite:**
- ✅ Integrações detectadas têm UC com `tipo: integracao_externa`
- ✅ Seções `sistema_externo` e `mapeamento_dados` presentes

---

**RESUMO DA FASE 3.5:**

Esta fase AUMENTA automaticamente a cobertura de UC ao detectar:
1. **Entidades órfãs** → Cria UCs CRUD (5 por entidade)
2. **Jobs background** → Cria UC com `tipo: background_job`
3. **Integrações externas** → Cria UC com `tipo: integracao_externa`

**Resultado esperado:**
- ✅ Cobertura RF→UC próxima de 100% **ANTES** da validação
- ✅ Menos iterações de correção necessárias
- ✅ Documentação mais completa desde o início

---

### Fase 4: Validação e Correção Iterativa (OBRIGATÓRIA)

#### 4.1 Executar Validador de Cobertura RF→UC (1ª Rodada)

```bash
python D:\IC2_Governanca\tools\docs\validator-rf-uc.py \
  --rf documentacao/[Fase]/[EPIC]/RFXXX/RFXXX.yaml \
  --uc documentacao/[Fase]/[EPIC]/RFXXX/UC-RFXXX.yaml
```

**IMPORTANTE:** O parâmetro `--tc` é **opcional** nesta fase, pois TC só será criado em contrato posterior.

**Critérios de validação:**
- ✅ UC cobre 100% das funcionalidades do RF
- ✅ UC-RFXXX.md ↔ UC-RFXXX.yaml sincronizados
- ✅ Nenhum UC introduz comportamento fora do RF
- ✅ Quantidade mínima de UCs para cobertura 100% (para RFs CRUD: UC00-UC04)

#### 4.2 Processo de Correção Obrigatória

**Se validador identificar gaps (exit code ≠ 0):**

**PROIBIDO:**
- ❌ PARAR apenas por identificar gaps
- ❌ Declarar falha sem tentar correção
- ❌ Atualizar STATUS.yaml com validação falhando

**OBRIGATÓRIO (Processo Iterativo):**
1. **Analisar relatório do validador** - Identificar exatamente quais UCs/funcionalidades faltam
2. **Criar/Complementar UCs faltantes** - Adicionar em UC-RFXXX.md e UC-RFXXX.yaml
3. **Revalidar (2ª rodada)** - Executar validator-rf-uc.py novamente
4. **Se ainda falhar** - Repetir passos 1-3 até validação passar
5. **Apenas após validação passar** - Prosseguir para Fase 5 (STATUS.yaml)

**Critério de Falha Definitiva (BLOQUEIO REAL):**
A execução só deve ser BLOQUEADA se:
- RF inconsistente/incompleto (requisito mal formado)
- RF contém funcionalidades fora de escopo do sistema
- Após 3 iterações de correção, validador ainda falha (indicando problema estrutural no RF)

**Gaps de cobertura NÃO são bloqueio - são gatilho de correção automática.**

---

### Fase 5: Atualização STATUS.yaml

#### 5.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar:**

```yaml
documentacao:
  uc: true           # UC-RFXXX.md E UC-RFXXX.yaml criados

validacoes:
  documentacao_uc_cobertura_total: true   # validator-rf-uc.py passou
  uc_yaml_sincronizado: true    # UC.md == UC.yaml
```

**REGRA CRÍTICA:** Só marcar como `true` após validação real do validador.

---

### Fase 6: Finalização

Após atualizar STATUS.yaml, a geração de UCs está concluída.

**Arquivos gerados:**
- UC-RFXXX.md
- UC-RFXXX.yaml
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 UC deve cobrir 100% do RF

**OBRIGATÓRIO em UC-RFXXX.md:**
- ✅ Quantidade de UCs necessária para cobrir 100% do RF (para RFs CRUD: padrão UC00-UC04)
- ✅ Cobertura de 100% das funcionalidades do RF
- ✅ Todos os UCs com fluxos principais, alternativos e de exceção
- ✅ Regras de negócio rastreadas ao RF

**PROIBIDO em UC-RFXXX.md:**
- ❌ Criar funcionalidades não previstas no RF
- ❌ Omitir funcionalidades do RF
- ❌ Copiar código

### 7.2 Coerência Estrutural Obrigatória

**Sincronização MD ↔ YAML:**
- UC-RFXXX.md ↔ UC-RFXXX.yaml: 100% sincronizado

**Coerência RF ↔ UC:**
- Todo item do RF deve estar coberto por UC
- Todo UC deve derivar de item do RF

---

## 8. Bloqueios de Execução

O agente DEVE PARAR **APENAS** se:

1. **RFXXX.md não existe**: RF não foi criado (pré-requisito faltando)
2. **RFXXX.yaml não existe**: RF estruturado não disponível (pré-requisito faltando)
3. **RF inconsistente**: RF contém contradições ou funcionalidades fora de escopo
4. **Falha após 3 iterações de correção**: Validador ainda falha após 3 tentativas de complementação (indica problema estrutural no RF)

**NÃO são bloqueios (são gatilhos de correção):**
- ❌ Validador falhou na 1ª rodada → ✅ Criar UCs faltantes e revalidar
- ❌ Cobertura incompleta detectada → ✅ Complementar UCs e revalidar
- ❌ UCs faltantes identificados → ✅ Criar UCs adicionais e revalidar

**Regra de Ouro:** Gaps de cobertura não bloqueiam - eles **OBRIGAM** a correção antes de declarar falha.

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] UC-RFXXX.md criado (UCs com fluxos completos)
- [ ] UC-RFXXX.yaml criado (estruturado, sincronizado com UC.md)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Validação

- [ ] validator-rf-uc.py executado (exit code 0)
- [ ] UC-RFXXX.md ↔ UC-RFXXX.yaml sincronizados 100%
- [ ] STATUS.yaml atualizado (documentacao.uc=true)
- [ ] STATUS.yaml atualizado (validacoes.rf_uc_cobertura_total=true)

### 9.3 Checklist de Qualidade Final

- [ ] **Cobertura:** UC cobre 100% do RF
- [ ] **Validação:** validator-rf-uc.py passou
- [ ] **Rastreabilidade:** RF → UC completa
- [ ] **Coerência:** RF ↔ UC 100% consistentes
- [ ] **Sincronização:** UC.md ↔ UC.yaml 100%
- [ ] **Arquivos prontos** (3 arquivos gerados e validados)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO-GERACAO-DOCS-WF** (para criar WF)
>
> ```
> Conforme CONTRATO-GERACAO-DOCS-WF para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará o arquivo WF-RFXXX.md (Wireframes).

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/execucao/uc-criacao.md` | Este contrato |
| `checklists/documentacao/geracao/uc.yaml` | Checklist YAML |
| `templates/UC.yaml` | Template UC estruturado |
| `templates/STATUS.yaml` | Template STATUS estruturado |
| `tools/docs/validator-rf-uc.py` | Validador de cobertura RF→UC |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-31 | Criação do contrato separado (UC apenas) |

---

## 13. REGRA DE NEGAÇÃO ZERO (AJUSTADA PARA CORREÇÃO)

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

**EXCEÇÃO EXPLÍCITA - Correção de Gaps de Cobertura:**

A REGRA DE NEGAÇÃO ZERO **NÃO se aplica** quando:
- O escopo está claramente definido no RF (RFXXX.md + RFXXX.yaml)
- A ação necessária é **complementar UCs faltantes** para cobrir funcionalidades já previstas no RF
- A correção está dentro do contrato ativo (criar/ajustar UC-RFXXX.md e UC-RFXXX.yaml)

**Negação é aplicada quando:**
- Tentar criar funcionalidades **NÃO previstas** no RF
- Extrapolar escopo documentado no RF
- Inventar requisitos não mapeados no RF
- Tentar criar código/implementação (este contrato é apenas documentação)

**Resumo:**
- ✅ Complementar UCs de funcionalidades do RF = **OBRIGATÓRIO**
- ❌ Criar UCs de funcionalidades fora do RF = **NEGADO**

---

**FIM DO CONTRATO**

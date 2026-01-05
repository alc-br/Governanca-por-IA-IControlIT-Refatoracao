# CONTRATO DE ADEQUAÇÃO COMPLETA DE UC
**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Sonnet 4.5 (baseado em auditoria de 23 RFs)
**Propósito:** Corrigir TODOS os gaps de cobertura RN → UC e problemas de nomenclatura identificados na auditoria

---

## CONTEXTO

### Problemas Identificados na Auditoria

Após análise de **23 RFs (291 RNs)**, foram identificados os seguintes padrões de falha:

#### 1. COBERTURA INSUFICIENTE (70% dos RFs auditados)
- **RF028:** 0% de cobertura (0/12 RNs)
- **RF024:** 6.7% de cobertura (1/15 RNs) - 14 gaps
- **RF025-RF030:** 0-14.3% de cobertura média
- **Padrão recorrente:** Apenas RN-001 e RN-002 cobertas, 10-13 RNs restantes ignoradas

#### 2. NOMENCLATURA INCONSISTENTE
- **RF023:** Usa `RN-CTR-023-XX` em vez de `RN-RF023-XX`
- **Catálogo híbrido:** Mistura de `RF023-CRUD-XX`, `RF023-VAL-XX` com RNs reais
- **Campo `covers.rf_items`:** Aponta para códigos de catálogo em vez de RNs

#### 3. GAPS CRÍTICOS DE FUNCIONALIDADES
- Jobs background não documentados (RF023: alertas, RF024: sincronização Azure AD)
- Workflows complexos sem UCs (RF024: aprovação multinível, RF023: workflow contratos)
- Regras de validação críticas ignoradas (RF024: referências circulares hierarquia)
- Integrações externas não documentadas (RF024: Microsoft Graph API)

#### 4. DESALINHAMENTO RF ↔ UC
- UCs não cobrem 100% das regras do RF
- RNs de criticidade ALTA/CRÍTICA sem cobertura
- Casos de uso genéricos sem cenários de teste detalhados

---

## OBJETIVO DO CONTRATO

Executar **adequação completa** de UC-RFXXX.yaml para:

1. ✅ **Cobertura 100%:** Todas as RNs do RF.yaml cobertas por UCs
2. ✅ **Nomenclatura padrão:** `RN-RFXXX-NNN` em todos os arquivos
3. ✅ **Eliminação de catálogo híbrido:** Apenas RNs reais em `covers.rf_items` e `regras_aplicadas`
4. ✅ **🚨 NOMENCLATURA DE FLUXOS (BLOQUEANTE):** `FA-UCNN-NNN` e `FE-UCNN-NNN` (NÃO `FA-001`, `FA-01`, etc.)
5. ✅ **Documentação de funcionalidades críticas:** Jobs, workflows, integrações
6. ✅ **Validação automática:** Exit code 0 no `validator-rf-uc.py`

---

## ⚠️ AVISO CRÍTICO: NOMENCLATURA DE FLUXOS É BLOQUEANTE

**PROBLEMA RECORRENTE:** UC.md frequentemente utiliza nomenclatura **INCORRETA** para fluxos:

❌ **INCORRETO (REPROVA):**
```markdown
**FA-01:** Filtrar por Empresa
**FA-001:** Filtrar por Status
**FE-01:** Erro ao Carregar Lista
```

✅ **CORRETO (APROVADO):**
```markdown
**FA-UC00-001:** Filtrar por Empresa
**FA-UC00-002:** Filtrar por Status
**FE-UC00-001:** Erro ao Carregar Lista
```

**Padrão obrigatório:**
- **FA-UCNN-NNN** para fluxos alternativos (ex: FA-UC00-001, FA-UC01-005)
- **FE-UCNN-NNN** para fluxos de exceção (ex: FE-UC00-001, FE-UC02-003)

**Validação 3.5 BLOQUEANTE:** Se encontrar **qualquer** `FA-01`, `FA-001`, `FE-01`, `FE-001` → **REPROVAÇÃO IMEDIATA**

**🔧 Etapa 5 do contrato executa migração automática obrigatória.**

---

## PRÉ-REQUISITOS (BLOQUEANTES)

Antes de ativar este contrato, VERIFICAR:

- [ ] `RFXXX.yaml` existe e está validado
- [ ] Python 3.10+ instalado
- [ ] Script `tools/docs/validator-rf-uc.py` disponível
- [ ] Templates oficiais disponíveis: `templates/UC.yaml`, `templates/UC.md`

**⚠️ IMPORTANTE:** `UC-RFXXX.yaml` e `UC-RFXXX.md` **NÃO** são pré-requisitos bloqueantes.

**Cenário 1:** Se UC-RFXXX.yaml e UC-RFXXX.md **NÃO EXISTEM** (RF novo):
- O agente DEVE criar ambos do zero baseado no RF.yaml e templates oficiais
- Análise de legado obrigatória (`ic1_legado/IControlIT/`)
- Cobrir 100% das RNs desde o início

**Cenário 2:** Se UC-RFXXX.yaml e UC-RFXXX.md **EXISTEM** (RF já documentado):
- O agente DEVE adequar/corrigir arquivos existentes
- Migrar nomenclatura, limpar catálogo, cobrir gaps

---

## ESCOPO DO CONTRATO

### INCLUÍDO (Zona de Atuação)

✅ **Leitura permitida:**
- `rf/**/RFXXX.yaml` (fonte da verdade)
- `rf/**/UC-RFXXX.yaml` (arquivo a ser corrigido)
- `rf/**/UC-RFXXX.md` (arquivo a ser corrigido)
- `templates/UC.yaml` (template oficial)
- `templates/UC.md` (template oficial)
- Código legado `ic1_legado/IControlIT/**/*` (referência comportamental)

✅ **Escrita permitida:**
- `rf/**/UC-RFXXX.yaml` (correção completa)
- `rf/**/UC-RFXXX.md` (correção completa)
- `rf/**/STATUS.yaml` (atualização após validação)
- `.temp_ia/adequacao-uc-RFXXX-diagnostico.md` (diagnóstico inicial) - **OPCIONAL**
- `.temp_ia/adequacao-uc-RFXXX-relatorio.md` (relatório final de execução) - **OPCIONAL**

✅ **Execução permitida:**
- `python tools/docs/validator-rf-uc.py` (validação)
- Scripts Python de migração/diagnóstico

### EXCLUÍDO (Zona Proibida)

❌ **Proibido alterar:**
- `RFXXX.yaml` (fonte da verdade - imutável)
- Código backend/frontend (fora do escopo)
- Templates oficiais
- Outros RFs não especificados no prompt

❌ **Proibido executar:**
- Testes automatizados (contrato separado)
- Deploy (contrato separado)
- Refatoração de código (fora do escopo)

---

## REGRAS DE AUTONOMIA (DECISÕES AUTOMÁTICAS)

O agente é **TOTALMENTE AUTÔNOMO** e NÃO deve parar para pedir permissão do usuário em:

### ✅ DECISÕES QUE O AGENTE TOMA SOZINHO

#### 1. **Criar UCs Faltantes para Cobrir Gaps**

**Cenário:** RF tem 15 RNs mas apenas 2 estão cobertas por UCs.

**Decisão automática:**
- ✅ **SEMPRE criar** os UCs faltantes para atingir 100% de cobertura
- ✅ **NÃO perguntar** se deve criar UCs - isso é o objetivo do contrato
- ✅ **Criar quantos UCs forem necessários** (5, 10, 15 UCs)

**Exemplo:**
- RF001 tem 4 entidades (Sistema_Parametro, Sistema_Feature_Flag, Sistema_Configuracao_Email, Sistema_Limite_Uso)
- Apenas Sistema_Parametro tem UCs (UC00-UC04)
- **AÇÃO AUTOMÁTICA:** Criar UC05-UC19 para cobrir as 3 entidades órfãs (Feature Flags, Config Email, Limites Uso)

#### 2. **Migrar Nomenclatura Não-Conforme**

**Cenário:** UC usa `RN-SLA-028-XX` ou `RN-CTR-023-XX` em vez de `RN-RF028-XX`.

**Decisão automática:**
- ✅ **SEMPRE migrar** para padrão oficial RN-RFXXX-NNN
- ✅ **Substituir TODAS as ocorrências** (10, 50, 100 substituições)
- ✅ **NÃO perguntar** se deve migrar - nomenclatura padrão é obrigatória

#### 3. **Limpar Catálogo Híbrido**

**Cenário:** UC tem códigos `RF023-CRUD-01`, `RF023-VAL-02` misturados com RNs reais.

**Decisão automática:**
- ✅ **SEMPRE remover** códigos de catálogo
- ✅ **Manter APENAS RNs reais** (RN-RFXXX-NNN)
- ✅ **NÃO perguntar** se deve limpar - catálogo híbrido é proibido

#### 4. **Documentar Jobs Background, Workflows, Integrações**

**Cenário:** RF menciona job Hangfire ou integração Azure AD mas não há UC correspondente.

**Decisão automática:**
- ✅ **SEMPRE criar UC** para job background (`tipo: background_job`)
- ✅ **SEMPRE criar UC** para workflow complexo (`tipo: workflow`)
- ✅ **SEMPRE criar UC** para integração externa (com `sistema_externo`)
- ✅ **NÃO perguntar** - funcionalidades críticas devem ser documentadas

#### 5. **Adequar Templates Desatualizados**

**Cenário:** UC.yaml ou UC.md não seguem template v2.0.

**Decisão automática:**
- ✅ **SEMPRE adequar** ao template oficial
- ✅ **Adicionar seções faltantes** (covers, exclusions, historico)
- ✅ **NÃO perguntar** - conformidade com template é obrigatória

#### 6. **Sincronizar UC.yaml ↔ UC.md**

**Cenário:** UC.yaml tem UC05-UC09 mas UC.md só tem UC00-UC04.

**Decisão automática:**
- ✅ **SEMPRE sincronizar** - criar narrativas faltantes no UC.md
- ✅ **Garantir 100% de sincronia** (mesmos UCs em ambos os arquivos)
- ✅ **NÃO perguntar** - divergência entre yaml e md é CRÍTICA

#### 7. **Reexecutar Validador Até Exit Code 0**

**Cenário:** `validator-rf-uc.py` retorna exit code 1 (falha).

**Decisão automática:**
- ✅ **SEMPRE corrigir** o problema identificado
- ✅ **Reexecutar validador** até exit code 0
- ✅ **NÃO perguntar** - validação com exit code 0 é critério de pronto obrigatório

### ❌ QUANDO O AGENTE DEVE PARAR E AVISAR

O agente SÓ deve parar e reportar se:

1. **Arquivos obrigatórios ausentes:**
   - RFXXX.yaml não existe
   - Templates oficiais não encontrados
   - Script validator-rf-uc.py não disponível

2. **Conflito estrutural grave:**
   - RF.yaml corrompido (YAML inválido)
   - UC.yaml corrompido (YAML inválido)

3. **Ambiguidade técnica irresolvível:**
   - RF menciona funcionalidade mas sem detalhes suficientes para criar UC
   - Precisa consultar legado mas código legado não existe

**CASO CONTRÁRIO:** Agente continua executando até 100% de conformidade.

---

### 📋 EXEMPLO CONCRETO DE AUTONOMIA

**Situação:** RF001 tem 4 entidades, mas apenas 1 tem UCs.

**❌ COMPORTAMENTO ERRADO (pausar para perguntar):**
```
PAUSA PARA DECISÃO CRÍTICA
Identifiquei que o RF001 possui 4 entidades mas apenas 1 está coberta por UCs.
Pergunto: Devo criar os UCs faltantes para as 3 entidades restantes?
```

**✅ COMPORTAMENTO CORRETO (executar automaticamente):**
```
📊 AUDITORIA IDENTIFICOU:
- 4 entidades no RF001
- Apenas Sistema_Parametro tem UCs (UC00-UC04)
- 3 entidades órfãs detectadas

🤖 AÇÃO AUTOMÁTICA:
Criando UC05-UC09 para Sistema_Feature_Flag...
Criando UC10-UC14 para Sistema_Configuracao_Email...
Criando UC15-UC19 para Sistema_Limite_Uso...

✅ Cobertura: 33% → 100% (15 UCs criados)
```

**Regra:** Agente NÃO pergunta, ele **REPORTA o que está fazendo** e executa.

---

## VALIDADOR v3.0: SUPORTE A `regras_negocio` (PADRÃO OFICIAL)

### ⚠️ MUDANÇA CRÍTICA - NÃO CRIAR CATÁLOGO HÍBRIDO

**A partir de 2026-01-01**, o `validator-rf-uc.py` foi atualizado para **v3.0** com suporte ao padrão oficial:

#### Padrão Oficial (PREFERENCIAL)

✅ **RF.yaml deve usar:**
```yaml
regras_negocio:
  - id: "RN-RF012-01"
    descricao: "Login único por conglomerado (multi-tenancy)"
    tipo: "funcionalidade"
    obrigatorio: true

  - id: "RN-RF012-02"
    descricao: "Política de senha forte"
    tipo: "validacao"
    obrigatorio: true
```

**Campos suportados:** `id`, `descricao` ou `titulo`, `tipo`, `obrigatorio` ou `required`

#### Formato Legado (Retrocompatibilidade)

⚠️ **Ainda suportado mas DEPRECIADO:**
```yaml
catalog:
  funcionalidades:
    - id: "RN-RF012-01"
      title: "Login único por conglomerado"
      required: true
```

### Ordem de Prioridade do Validador v3.0

1. **PRIORIDADE 1:** Lê `regras_negocio` (padrão oficial)
2. **PRIORIDADE 2:** Lê `catalog` (retrocompatibilidade)

Se `regras_negocio` existe no RF.yaml, o validador **IGNORA** `catalog` completamente.

### ❌ NÃO CRIAR CATÁLOGO HÍBRIDO

**PROIBIDO durante adequação UC:**

❌ **NÃO fazer isso:**
```yaml
# NO RF.yaml - NÃO CRIAR!!!
catalog:
  funcionalidades:
    - id: "RN-RF012-01"
      title: "Login único por conglomerado"
      required: true
      origem: "regras_negocio"  # ← WORKAROUND DESNECESSÁRIO
```

✅ **Fazer isso:**
```yaml
# RF.yaml já tem regras_negocio (linhas 80-181)?
# Então NÃO CRIAR catálogo!
# O validador v3.0 lê regras_negocio diretamente.
```

### Regra para o Agente

Durante adequação de UC:

1. **Ler RF.yaml** - verificar se tem `regras_negocio`
2. **Se tem `regras_negocio`:**
   - ✅ Usar `regras_negocio` como fonte da verdade
   - ❌ NÃO criar campo `catalog`
   - ❌ NÃO criar workarounds híbridos
   - ✅ Validador v3.0 lê `regras_negocio` diretamente

3. **Se tem APENAS `catalog`:** (RF legado)
   - ⚠️ Ainda suportado por retrocompatibilidade
   - Validador v3.0 lê `catalog` automaticamente
   - Sugerir ao usuário migrar para `regras_negocio` no futuro

**Motivo:** O validador v3.0 foi atualizado para eliminar a necessidade de workarounds. Não é mais necessário criar catálogo híbrido durante adequações de UC.

---

## ESTRUTURA OBRIGATÓRIA DE `exclusions` (RF.yaml)

### ⚠️ ERRO COMUM: Exclusions como Lista de Strings

**O validador v3.0 espera objetos com campos `id` e `justificativa`, NÃO strings simples.**

#### ❌ ESTRUTURA INCORRETA (CAUSA AttributeError)

```yaml
# NO RF.yaml - CAUSA ERRO!
exclusions:
  rf_items:
    - "SSO com provedores OAuth2/SAML (planejado para fase futura)"
    - "Biometria (não previsto)"
```

**Erro gerado:**
```python
AttributeError: 'str' object has no attribute 'get'
# Linha 143 do validator-rf-uc.py (função apply_exclusions)
```

#### ✅ ESTRUTURA CORRETA

```yaml
# NO RF.yaml - CORRETO
exclusions:
  rf_items:
    - id: "EX-RF012-01"
      justificativa: "SSO com provedores OAuth2/SAML (planejado para fase futura)"

    - id: "EX-RF012-02"
      justificativa: "Biometria (não previsto)"

    - id: "EX-RF012-03"
      justificativa: "Integração com TOTP externo (não implementado)"
```

### Campos Obrigatórios

| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| `id` | string | ✅ SIM | Identificador único da exclusão (EX-RFXXX-NN) |
| `justificativa` | string | ✅ SIM | Motivo da exclusão (planejado futuramente, não previsto, etc.) |

### Nomenclatura Padrão

- **Formato:** `EX-RFXXX-NN`
- **Exemplos:** `EX-RF012-01`, `EX-RF028-05`, `EX-RF045-02`

### Regra para o Agente

Durante adequação de UC, se encontrar exclusions com strings:

1. **Ler exclusions atual** do RF.yaml
2. **Se for lista de strings:**
   - ⚠️ **PARAR execução**
   - 📋 **Reportar erro estrutural**
   - 🔴 **IMPORTANTE:** NÃO corrigir RF.yaml (fora do escopo deste contrato)
   - 💬 Orientar usuário a corrigir RF.yaml conforme estrutura obrigatória acima

3. **Se for lista de objetos com `id` e `justificativa`:**
   - ✅ Continuar execução normalmente
   - Validador v3.0 aplicará exclusions corretamente

**Motivo:** RF.yaml é fonte da verdade imutável. Adequação UC NÃO pode alterar RF.yaml (zona proibida).

---

## WORKFLOW OBRIGATÓRIO (15 ETAPAS)

### FASE 1: PREPARAÇÃO (Etapas 1-3)

#### Etapa 1: Criar Todo List Obrigatória

Antes de QUALQUER ação, criar todo list EXATA:

```markdown
- [ ] 1. Preparação: criar backup
- [ ] 2. Análise: ler RF.yaml, UC.yaml e UC.md
- [ ] 3. Diagnóstico: identificar gaps e problemas (UC.yaml ↔ UC.md ↔ Templates)
- [ ] 4. Migração nomenclatura RN: RN-RFXXX-NNN
- [ ] 5. **🚨 CRÍTICO: Migração nomenclatura fluxos FA-UCNN-NNN e FE-UCNN-NNN (BLOQUEANTE - Validação 3.5)**
- [ ] 6. Limpeza catálogo: remover RF-CRUD/VAL/SEC
- [ ] 7. Adequar UC.yaml ao template oficial
- [ ] 8. Adequar UC.md ao template oficial
- [ ] 9. Sincronizar UC.yaml ↔ UC.md (100% consistentes)
- [ ] 10. Criar UCs faltantes: cobrir RNs sem UC
- [ ] 11. Documentar jobs background
- [ ] 12. Documentar workflows complexos
- [ ] 13. Documentar integrações externas
- [ ] 14. Validar: validator-rf-uc.py (exit code 0)
- [ ] 15. Atualizar STATUS.yaml
- [ ] 16. Relatório final
```

**VIOLAÇÃO:** Iniciar sem todo list = execução INVÁLIDA.

---

#### Etapa 2: Verificação e Backup

**IMPORTANTE:** Operações Git (branch, commit, merge) são responsabilidade do usuário.

**Passo 2.1: Verificar existência de arquivos UC**

```bash
# Verificar se UC.yaml existe
if [ -f "rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.yaml" ]; then
    echo "✅ UC.yaml existe - ADEQUAÇÃO"
    MODO="ADEQUACAO"
else
    echo "⚠️ UC.yaml NÃO existe - CRIAÇÃO DO ZERO"
    MODO="CRIACAO"
fi

# Verificar se UC.md existe
if [ -f "rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.md" ]; then
    echo "✅ UC.md existe"
else
    echo "⚠️ UC.md NÃO existe - CRIAÇÃO DO ZERO"
fi
```

**Passo 2.2: Backup (só se arquivos existirem)**

```bash
# Backup UC.yaml (se existir)
if [ "$MODO" = "ADEQUACAO" ]; then
    cp rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.yaml \
       rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.yaml.backup-$(date +%Y%m%d-%H%M%S)
    echo "✅ Backup criado: UC.yaml.backup"
fi

# Backup UC.md (se existir)
if [ -f "rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.md" ]; then
    cp rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.md \
       rf/[FASE]/[EPIC]/RFXXX/UC-RFXXX.md.backup-$(date +%Y%m%d-%H%M%S)
    echo "✅ Backup criado: UC.md.backup"
fi
```

**Passo 2.3: Ação baseada no modo**

```bash
if [ "$MODO" = "CRIACAO" ]; then
    echo "⚠️ UC-RFXXX.yaml NÃO existe"
    echo "🔄 DELEGANDO para CONTRATO-GERACAO-DOCS-UC..."
    echo ""
    echo "📋 O CONTRATO-GERACAO-DOCS-UC irá:"
    echo "   1. Ler RF.yaml para extrair RNs"
    echo "   2. Consultar legado (ic1_legado) se existir"
    echo "   3. Detectar automaticamente:"
    echo "      - Entidades órfãs (MD-RFXXX.md)"
    echo "      - Jobs background (keywords)"
    echo "      - Integrações externas (keywords)"
    echo "   4. Copiar template oficial (templates/UC.yaml)"
    echo "   5. Criar UC.yaml do zero com cobertura 100%"
    echo "   6. Criar UC.md narrativo correspondente"
    echo "   7. Validar com validator-rf-uc.py"
    echo "   8. Atualizar STATUS.yaml"
    echo ""
    echo "⏭️ Após CONTRATO-GERACAO-DOCS-UC concluir:"
    echo "   - UC-RFXXX.yaml e UC-RFXXX.md estarão criados"
    echo "   - Cobertura 100% garantida"
    echo "   - CONTRATO-ADEQUACAO validará resultado final"
    echo ""

    # =====================================================
    # DELEGAÇÃO AUTOMÁTICA PARA CONTRATO-GERACAO-DOCS-UC
    # =====================================================

    echo "🤖 EXECUTANDO CONTRATO-GERACAO-DOCS-UC..."

    # O agente DEVE ler e executar:
    # D:\IC2\docs\contracts\documentacao\CONTRATO-GERACAO-DOCS-UC.md
    # para o RFXXX especificado

    # Após execução do CONTRATO-GERACAO-DOCS-UC:
    # - UC-RFXXX.yaml criado
    # - UC-RFXXX.md criado
    # - STATUS.yaml atualizado (documentacao.uc = true)

    echo "✅ CONTRATO-GERACAO-DOCS-UC concluído"
    echo "⏭️ Retornando ao CONTRATO-ADEQUACAO para validação final..."

else
    echo "✅ UC existe - MODO ADEQUAÇÃO"
    echo "🤖 MODO ADEQUAÇÃO:"
    echo "   1. Auditar arquivos existentes"
    echo "   2. Migrar nomenclatura"
    echo "   3. Limpar catálogo"
    echo "   4. Cobrir gaps (entidades órfãs, jobs, integrações)"
fi
```

**Validação:**
- Se MODO=ADEQUACAO: Arquivos `.backup-*` criados antes de qualquer edição
- Se MODO=CRIACAO: Delegar para CONTRATO-GERACAO-DOCS-UC, depois validar resultado

**⚠️ IMPORTANTE:** Quando MODO=CRIACAO, este contrato se torna um **orquestrador**:
1. Detecta que UC não existe
2. Delega para CONTRATO-GERACAO-DOCS-UC (criação)
3. Aguarda conclusão
4. Valida resultado final (Etapa 13: validator-rf-uc.py)
5. Atualiza STATUS.yaml (se necessário)

---

#### Etapa 3: Análise Diagnóstica Completa (AUDITORIA AUTOMÁTICA)

**REGRA DE OURO:** O agente DEVE auditar automaticamente ANTES de corrigir.

Executar script de auditoria completa e registrar em `.temp_ia/adequacao-uc-RFXXX-diagnostico.md`.

**VALIDAÇÕES OBRIGATÓRIAS:**

1. **Cobertura RN → UC** (RF.yaml vs UC.yaml)
2. **Nomenclatura padrão** (RN-RFXXX-NNN)
3. **Catálogo limpo** (zero RF-CRUD/VAL/SEC)
4. **✨ NOVO: Nomenclatura de fluxos** (FA-UCNN-NNN vs FA-NNN - **BLOQUEANTE**)
5. **✨ NOVO: Entidades órfãs** (MD.md vs UC.yaml - CRÍTICO)
6. **Jobs/Workflows/Integrações** não documentados
7. **✨ NOVO: Divergência UC.yaml ↔ UC.md** (CRÍTICO)
8. **✨ NOVO: Conformidade com templates** (UC.yaml vs template, UC.md vs template)

```python
# Script de diagnóstico
import re
import yaml
from pathlib import Path

rf_file = Path('rf/.../RFXXX.yaml')
uc_file = Path('rf/.../UC-RFXXX.yaml')
md_file = Path('rf/.../MD-RFXXX.md')

# Ler RF
with open(rf_file) as f:
    rf_content = f.read()
    rns_rf = set(re.findall(r'RN-RF\d{3}-\d{2}', rf_content))

# Ler UC
with open(uc_file) as f:
    uc_content = f.read()
    rns_uc = set(re.findall(r'RN-[A-Z]{2,5}-\d{3}-\d{2}', uc_content))
    catalog_codes = re.findall(r'RF\d{3}-(CRUD|VAL|SEC)-\d{2}', uc_content)

# Gaps RN
gaps = rns_rf - rns_uc

# Problemas nomenclatura
non_standard = [rn for rn in rns_uc if not rn.startswith('RN-RF')]

# ✨ NOVO: Detectar nomenclatura de fluxos incorreta (VALIDAÇÃO 3.5 - BLOQUEANTE)
uc_md_file = Path('rf/.../UC-RFXXX.md')
if uc_md_file.exists():
    with open(uc_md_file) as f:
        uc_md_content = f.read()

    # Buscar violações (FA-001, FE-001 em vez de FA-UC00-001, FE-UC00-001)
    violacoes_fa = re.findall(r'\*\*(FA)-(\d{3}):\*\*', uc_md_content)  # FA-001 (ERRADO)
    violacoes_fe = re.findall(r'\*\*(FE)-(\d{3}):\*\*', uc_md_content)  # FE-001 (ERRADO)

    # Padrão correto: FA-UC00-001, FE-UC00-001
    corretos_fa = re.findall(r'\*\*FA-UC\d{2}-\d{3}:\*\*', uc_md_content)
    corretos_fe = re.findall(r'\*\*FE-UC\d{2}-\d{3}:\*\*', uc_md_content)

    total_violacoes_nomenclatura_fluxos = len(violacoes_fa) + len(violacoes_fe)

    if total_violacoes_nomenclatura_fluxos > 0:
        print(f"❌ CRÍTICO: Nomenclatura de fluxos INCORRETA")
        print(f"   Violações FA-NNN: {len(violacoes_fa)}")
        print(f"   Violações FE-NNN: {len(violacoes_fe)}")
        print(f"   Total: {total_violacoes_nomenclatura_fluxos} violações")
        print(f"   Exemplos FA incorretos: {[f'FA-{num}' for tipo, num in violacoes_fa[:3]]}")
        print(f"   Exemplos FE incorretos: {[f'FE-{num}' for tipo, num in violacoes_fe[:3]]}")
        print(f"   ✅ Correto seria: FA-UC00-001, FA-UC01-002, FE-UC00-001, etc.")
    else:
        print(f"✅ Nomenclatura de fluxos: 100% conforme (FA-UCNN-NNN, FE-UCNN-NNN)")

# ✨ NOVO: Detectar entidades órfãs (MELHORIA #1)
orphan_entities = []
if md_file.exists():
    with open(md_file) as f:
        md_content = f.read()

    # Extrair entidades do MD (tabelas CREATE TABLE)
    entities = re.findall(r'CREATE TABLE (\w+)', md_content)
    print(f"📊 Entidades no MD: {entities}")

    # Extrair entidades cobertas nos UCs
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
        print(f"⚠️ Entidades órfãs (SEM UCs): {orphan_entities}")
    else:
        print(f"✅ Todas as entidades têm UCs correspondentes")

# ✨ NOVO: Detectar jobs background (MELHORIA #2)
keywords_jobs = ['hangfire', 'job', 'scheduler', 'cron', 'background', 'recorrente', 'periódico']
jobs_detected = []
for keyword in keywords_jobs:
    if keyword in rf_content.lower():
        jobs_detected.append(keyword)

if jobs_detected:
    print(f"⚠️ Jobs background detectados: {jobs_detected}")
else:
    print(f"✅ Nenhum job background identificado")

# ✨ NOVO: Detectar integrações externas (MELHORIA #3)
keywords_integracoes = ['api', 'smtp', 'sendgrid', 'aws ses', 'azure', 'graph', 'brasil api', 'via cep', 'externo', 'third-party']
integracoes_detected = []
for keyword in keywords_integracoes:
    if keyword in rf_content.lower():
        integracoes_detected.append(keyword)

if integracoes_detected:
    print(f"⚠️ Integrações externas detectadas: {integracoes_detected}")
else:
    print(f"✅ Nenhuma integração externa identificada")

print(f"\n📊 RESUMO DA AUDITORIA:")
print(f"RNs no RF: {len(rns_rf)}")
print(f"RNs no UC: {len(rns_uc)}")
print(f"Gaps de RN: {len(gaps)}")
print(f"Nomenclatura RN não-padrão: {len(non_standard)}")
print(f"Nomenclatura fluxos incorreta: {total_violacoes_nomenclatura_fluxos} (FA/FE-NNN)  ← **BLOQUEANTE**")
print(f"Códigos catálogo: {len(catalog_codes)}")
print(f"Entidades órfãs: {len(orphan_entities)}")
print(f"Jobs detectados: {len(jobs_detected)}")
print(f"Integrações detectadas: {len(integracoes_detected)}")
```

**Saída esperada para RF001:**
```
✅ Nomenclatura de fluxos: 100% conforme (FA-UCNN-NNN, FE-UCNN-NNN)
📊 Entidades no MD: ['Sistema_Parametro', 'Sistema_Feature_Flag', 'Sistema_Configuracao_Email', 'Sistema_Limite_Uso']
✅ Entidades cobertas: {'Sistema_Parametro'}
⚠️ Entidades órfãs (SEM UCs): {'Sistema_Feature_Flag', 'Sistema_Configuracao_Email', 'Sistema_Limite_Uso'}
⚠️ Jobs background detectados: ['hangfire', 'job']
⚠️ Integrações externas detectadas: ['smtp', 'sendgrid', 'aws ses']

📊 RESUMO DA AUDITORIA:
RNs no RF: 15
RNs no UC: 8
Gaps de RN: 7
Nomenclatura RN não-padrão: 0
Nomenclatura fluxos incorreta: 0 (FA/FE-NNN)  ← **BLOQUEANTE**
Códigos catálogo: 0
Entidades órfãs: 3
Jobs detectados: 2
Integrações detectadas: 3
```

**Saída esperada para RF006 (com violações de nomenclatura):**
```
❌ CRÍTICO: Nomenclatura de fluxos INCORRETA
   Violações FA-NNN: 38
   Violações FE-NNN: 4
   Total: 42 violações
   Exemplos FA incorretos: ['FA-001', 'FA-002', 'FA-003']
   Exemplos FE incorretos: ['FE-001', 'FE-002', 'FE-003']
   ✅ Correto seria: FA-UC00-001, FA-UC01-002, FE-UC00-001, etc.

📊 RESUMO DA AUDITORIA:
RNs no RF: 18
RNs no UC: 18
Gaps de RN: 0
Nomenclatura RN não-padrão: 0
Nomenclatura fluxos incorreta: 42 (FA/FE-NNN)  ← **BLOQUEANTE**
Códigos catálogo: 0
Entidades órfãs: 0
Jobs detectados: 0
Integrações detectadas: 0
```

**🤖 AÇÃO AUTOMÁTICA OBRIGATÓRIA:**

Se forem detectadas entidades órfãs, o agente DEVE **automaticamente**:

```python
# Para cada entidade órfã, criar UCs CRUD completos
for entity in orphan_entities:
    print(f"\n🤖 AÇÃO AUTOMÁTICA: Criando UCs para {entity}...")

    # Determinar próximo UC disponível (ex: UC05 se último é UC04)
    next_uc_num = len(uc_data.get('casos_de_uso', [])) + 1

    # Criar 5 UCs CRUD (Listar, Criar, Visualizar, Editar, Excluir)
    crud_ucs = [
        {
            'id': f'UC{next_uc_num:02d}',
            'nome': f'Listar {entity}',
            'tipo': 'leitura',
            'ator_principal': 'usuario_autenticado'
        },
        {
            'id': f'UC{next_uc_num+1:02d}',
            'nome': f'Criar {entity}',
            'tipo': 'crud',
            'ator_principal': 'usuario_autenticado'
        },
        # ... (UC Visualizar, Editar, Excluir)
    ]

    print(f"   ✅ UC{next_uc_num:02d}-UC{next_uc_num+4:02d}: CRUD completo para {entity}")
```

**IMPORTANTE:** O agente NÃO pergunta se deve criar UCs para entidades órfãs. Ele **EXECUTA AUTOMATICAMENTE**.

**Critério de aceite:** Arquivo `.temp_ia/adequacao-uc-RFXXX-diagnostico.md` criado com métricas completas incluindo entidades órfãs, jobs e integrações.

---

### FASE 2: CORREÇÃO (Etapas 4-13)

#### Etapa 4: Migração de Nomenclatura de RNs (CRÍTICO)

**Problema:** `RN-CTR-023-XX` → `RN-RF023-XX`

**Ação:**

1. **NO RF.yaml:**
   ```yaml
   # ANTES (ERRADO)
   regras_negocio:
     - id: "RN-CTR-023-01"
       descricao: "..."

   # DEPOIS (CORRETO)
   regras_negocio:
     - id: "RN-RF023-01"
       descricao: "..."
   ```

2. **NO UC.yaml:**
   ```yaml
   # ANTES (ERRADO)
   regras_aplicadas:
     - "RN-CTR-023-01"

   # DEPOIS (CORRETO)
   regras_aplicadas:
     - "RN-RF023-01"
   ```

**Script de migração automática:**
```python
import re

def migrate_nomenclature(file_path, rf_num):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Padrões não-padrão conhecidos
    patterns = [
        (r'RN-CTR-(\d{3})-(\d{2})', f'RN-RF\\1-\\2'),  # CTR → RF
        (r'RN-DEP-(\d{3})-(\d{2})', f'RN-RF\\1-\\2'),  # DEP → RF
        (r'RN-FIN-(\d{3})-(\d{2})', f'RN-RF\\1-\\2'),  # FIN → RF
    ]

    for old_pattern, new_pattern in patterns:
        content = re.sub(old_pattern, new_pattern, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
```

**Validação:** `grep -c "RN-CTR-\|RN-DEP-\|RN-FIN-" UC-RFXXX.yaml` retorna 0.

---

#### Etapa 5: 🚨 Migração de Nomenclatura de Fluxos (BLOQUEANTE - Validação 3.5) ✨

**⚠️ PROBLEMA RECORRENTE:** UC.md frequentemente usa `FA-001`, `FA-01`, `FE-001`, `FE-01` → **REPROVA NA VALIDAÇÃO 3.5**

**✅ SOLUÇÃO:** Migrar para `FA-UC00-001`, `FE-UC00-001` (padrão obrigatório)

**Ação:**

**NO UC-RFXXX.md:**

```markdown
# ANTES (ERRADO - QUEBRA RASTREABILIDADE)
## UC00 - Listar Clientes

### Fluxos Alternativos (FA)
**FA-001:** Usuário NÃO é Super Admin
**FA-002:** Nenhum Cliente cadastrado

### Fluxos de Exceção (FE)
**FE-001:** Erro de conectividade com banco de dados

# DEPOIS (CORRETO - PADRÃO v2.0)
## UC00 - Listar Clientes

### Fluxos Alternativos (FA)
**FA-UC00-001:** Usuário NÃO é Super Admin
**FA-UC00-002:** Nenhum Cliente cadastrado

### Fluxos de Exceção (FE)
**FE-UC00-001:** Erro de conectividade com banco de dados
```

**Script de migração automática:**

```python
import re
from pathlib import Path

def migrate_flow_nomenclature(uc_md_file):
    """
    Migra nomenclatura de fluxos de FA-001 para FA-UC00-001
    """
    with open(uc_md_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Encontrar UC atual sendo processado
    # Buscar padrão: ## UC00 - Título
    uc_sections = re.findall(r'## (UC\d{2}) -', content)

    for uc_id in uc_sections:
        # Extrair seção completa do UC
        uc_pattern = rf'(## {uc_id} -.*?)(?=## UC\d{{2}} -|$)'
        uc_match = re.search(uc_pattern, content, re.DOTALL)

        if not uc_match:
            continue

        uc_content = uc_match.group(1)

        # Substituir FA-NNN por FA-UCNN-NNN
        # Regex: **FA-001: → **FA-UC00-001:
        uc_content_new = re.sub(
            r'\*\*(FA)-(\d{3}):\*\*',
            rf'**FA-{uc_id}-\2:**',
            uc_content
        )

        # Substituir FE-NNN por FE-UCNN-NNN
        uc_content_new = re.sub(
            r'\*\*(FE)-(\d{3}):\*\*',
            rf'**FE-{uc_id}-\2:**',
            uc_content_new
        )

        # Substituir no conteúdo original
        content = content.replace(uc_content, uc_content_new)

    # Salvar arquivo corrigido
    with open(uc_md_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ Nomenclatura de fluxos migrada em {uc_md_file.name}")

# Executar para o UC do RF
uc_md_path = Path('rf/.../UC-RFXXX.md')
migrate_flow_nomenclature(uc_md_path)
```

**Exemplo prático (RF006):**

```bash
# ANTES (42 violações)
$ grep -E '\*\*(FA|FE)-\d{3}:\*\*' UC-RF006.md | head -5
**FA-001:** Usuário NÃO é Super Admin
**FA-002:** Nenhum Cliente cadastrado
**FA-003:** CPF/CNPJ inválido
**FE-001:** Erro de conectividade
**FE-002:** Timeout na API

# Executar script
$ python migrate_flow_nomenclature.py RF006
✅ Nomenclatura de fluxos migrada em UC-RF006.md
   - FA-001 → FA-UC00-001 (38 substituições)
   - FE-001 → FE-UC00-001 (4 substituições)
   Total: 42 correções

# DEPOIS (0 violações)
$ grep -E '\*\*(FA|FE)-\d{3}:\*\*' UC-RF006.md
(sem resultados)
```

**🔍 VALIDAÇÃO OBRIGATÓRIA APÓS ETAPA 5:**

```bash
# Verificar que NÃO existem mais violações
grep -E '\*\*(FA|FE)-0?\d{1,2}:\*\*' UC-RFXXX.md

# RESULTADO ESPERADO: Vazio (0 matches)
# Se encontrar qualquer match → ETAPA 5 FALHOU → BLOQUEAR execução
```

**Padrões que REPROVAM (encontrados frequentemente):**
- `**FA-01:**` → ERRADO (2 dígitos)
- `**FA-001:**` → ERRADO (3 dígitos sem UC)
- `**FA-1:**` → ERRADO (1 dígito)
- `**FE-01:**` → ERRADO (2 dígitos)
- `**FE-001:**` → ERRADO (3 dígitos sem UC)

**Padrão CORRETO que APROVA:**
- `**FA-UC00-001:**` ✅
- `**FA-UC01-005:**` ✅
- `**FE-UC00-001:**` ✅
- `**FE-UC02-003:**` ✅

**⚠️ SE VALIDAÇÃO FALHAR:**
- PARAR execução imediatamente
- Reportar violações encontradas
- NÃO prosseguir para Etapa 6
- Corrigir manualmente ou reexecutar script

$ grep -E '\*\*(FA|FE)-UC\d{2}-\d{3}:\*\*' UC-RF006.md | head -5
**FA-UC00-001:** Usuário NÃO é Super Admin
**FA-UC00-002:** Nenhum Cliente cadastrado
**FA-UC01-001:** CPF/CNPJ inválido
**FE-UC00-001:** Erro de conectividade
**FE-UC02-001:** Timeout na API
```

**Validação:**

```bash
# Verificar ZERO violações
grep -c -E '\*\*(FA|FE)-\d{3}:\*\*' UC-RFXXX.md
# Deve retornar: 0

# Verificar padrão correto
grep -c -E '\*\*FA-UC\d{2}-\d{3}:\*\*' UC-RFXXX.md
# Deve retornar: [N] (total de FAs)

grep -c -E '\*\*FE-UC\d{2}-\d{3}:\*\*' UC-RFXXX.md
# Deve retornar: [M] (total de FEs)
```

**Critério de aceite:** ZERO ocorrências de `FA-\d{3}` ou `FE-\d{3}` no UC.md.

---

#### Etapa 6: Limpeza de Catálogo Híbrido

**Problema:** `covers.rf_items` mistura catálogo (`RF023-CRUD-01`) com RNs reais.

**Ação:**

```yaml
# ANTES (ERRADO)
covers:
  rf_items:
    - "RF023-CRUD-01"  # ❌ Código de catálogo
    - "RF023-VAL-01"   # ❌ Código de catálogo
    - "RN-RF023-001"   # ✅ RN real

# DEPOIS (CORRETO)
covers:
  rf_items:
    - "RN-RF023-001"
    - "RN-RF023-002"
    - "RN-RF023-003"
    # ... (apenas RNs reais)
```

**Regra de Ouro:** `covers.rf_items` e `regras_aplicadas` DEVEM conter APENAS IDs que existem em `RFXXX.yaml > regras_negocio[].id`.

**Script de limpeza:**
```python
def clean_catalog_codes(uc_file, rf_file):
    # Ler RNs válidas do RF
    with open(rf_file) as f:
        valid_rns = set(re.findall(r'"(RN-RF\d{3}-\d{2})"', f.read()))

    # Ler UC
    with open(uc_file) as f:
        uc_yaml = yaml.safe_load(f)

    # Limpar covers.rf_items
    cleaned_items = [
        item for item in uc_yaml.get('covers', {}).get('rf_items', [])
        if item in valid_rns
    ]

    uc_yaml['covers']['rf_items'] = cleaned_items

    # Salvar
    with open(uc_file, 'w') as f:
        yaml.dump(uc_yaml, f, allow_unicode=True, sort_keys=False)
```

**Validação:** `grep -c "RF\d{3}-CRUD-\|RF\d{3}-VAL-\|RF\d{3}-SEC-" UC-RFXXX.yaml` retorna 0.

---

#### Etapa 6: Adequar UC-RFXXX.yaml ao Template Oficial ✨ NOVO

**Problema:** UC.yaml pode estar desatualizado em relação ao template v2.0.

**Ação:** Comparar estrutura do UC-RFXXX.yaml com `templates/UC.yaml` e adequar.

**Verificações obrigatórias:**

1. **Cabeçalho (metadata):**
   ```yaml
   # =============================================
   # UC - Casos de Uso (Contrato Comportamental)
   # RFXXX - [Nome do RF]
   # Versão: 2.0
   # Data: AAAA-MM-DD
   # Autor: [Nome]
   # =============================================

   uc:
     rf: "RFXXX"
     versao: "2.0"
     data: "AAAA-MM-DD"
   ```

2. **Estrutura de cada caso de uso:**
   ```yaml
   casos_de_uso:
     - id: "UC00"
       nome: "[Nome do UC]"
       ator_principal: "usuario_autenticado"
       tipo: "crud | leitura | acao | background_job"
       impacta_dados: true | false

       covers:
         rf_items:
           - "RN-RFXXX-NN"  # Apenas RNs válidas
         uc_items:
           - id: "FP-UC00-001"
             title: "[Descrição]"
             required: true
           # ... FA, FE

       precondicoes:
         - permissao: "[nome_permissao]"

       gatilho: "[Evento que inicia o UC]"

       fluxo_principal:
         - passo: 1
           ator: "usuario | sistema"
           acao: "[descrição]"

       fluxos_alternativos:
         - id: "FA-UC00-01"
           condicao: "[condição]"
           resultado: "[resultado]"

       fluxos_excecao:
         - id: "FE-UC00-01"
           condicao: "[erro]"
           resultado: "[tratamento]"

       regras_aplicadas:
         - "RN-RFXXX-NN"

       resultado_final:
         estado: "[estado final]"
   ```

3. **Seções obrigatórias ao final:**
   ```yaml
   exclusions:
     uc_items: []

   historico:
     - versao: "1.0"
       data: "AAAA-MM-DD"
       autor: "[Nome]"
       descricao: "[Descrição]"
   ```

**Validação:** Estrutura 100% aderente ao template v2.0.

---

#### Etapa 7: Adequar UC-RFXXX.md ao Template Oficial ✨ NOVO

**Problema:** UC.md pode estar desatualizado em relação ao template v2.0.

**Ação:** Comparar estrutura do UC-RFXXX.md com `templates/UC.md` e adequar.

**Seções obrigatórias:**

```markdown
# Casos de Uso - RFXXX - [Nome]

## UC00 - [Nome do UC]

### Ator Principal
- [Ator]

### Pré-condições
- [Lista]

### Gatilho
[Evento]

### Fluxo Principal (FP)
FP-01: [Passo]
FP-02: [Passo]

### Fluxos Alternativos (FA)
FA-01: [Descrição]
FA-02: [Descrição]

### Fluxos de Exceção (FE)
FE-01: [Erro] → [Tratamento]

### Regras Aplicadas
- RN-RFXXX-NN: [Descrição]

### Resultado Final
[Estado final do sistema]

---
```

**Validação:**
- UC.md contém TODOS os UCs presentes em UC.yaml
- Seções obrigatórias presentes
- Narrativa clara e completa

---

#### Etapa 8: Sincronizar UC.yaml ↔ UC.md (100% Consistentes) ✨ NOVO

**Problema CRÍTICO:** UC.yaml e UC.md podem estar divergentes.

**Ação:** Garantir que UC.yaml e UC.md descrevam EXATAMENTE os mesmos casos de uso.

**Validações obrigatórias:**

1. **Mesma quantidade de UCs:**
   ```bash
   # Contar UCs no .yaml
   grep -c "^  - id: \"UC" UC-RFXXX.yaml

   # Contar UCs no .md
   grep -c "^## UC" UC-RFXXX.md

   # DEVEM ser iguais
   ```

2. **Mesmos IDs de UCs:**
   ```bash
   # IDs no .yaml
   grep "^  - id: \"UC" UC-RFXXX.yaml | sort

   # IDs no .md
   grep "^## UC" UC-RFXXX.md | sed 's/## \(UC[0-9]*\) -.*/\1/' | sort

   # DEVEM ser idênticos
   ```

3. **Mesmas RNs cobertas:**
   - Para cada UC, verificar que `regras_aplicadas` no .yaml
     corresponde a "Regras Aplicadas" no .md

4. **Mesmos fluxos:**
   - FP, FA, FE presentes em ambos

**Script de validação:**
```python
def validate_uc_yaml_md_sync(yaml_file, md_file):
    # Extrair UCs do YAML
    yaml_ucs = set(re.findall(r'- id: "(UC\d+)"', Path(yaml_file).read_text()))

    # Extrair UCs do MD
    md_ucs = set(re.findall(r'^## (UC\d+) -', Path(md_file).read_text(), re.MULTILINE))

    # Comparar
    if yaml_ucs == md_ucs:
        print(f"✅ UC.yaml ↔ UC.md sincronizados ({len(yaml_ucs)} UCs)")
        return True
    else:
        print(f"❌ DIVERGÊNCIA detectada:")
        print(f"   Apenas em .yaml: {yaml_ucs - md_ucs}")
        print(f"   Apenas em .md: {md_ucs - yaml_ucs}")
        return False
```

**Critério de aceite:** Validação retorna `True` (100% sincronizado).

---

#### Etapa 9: Criar UCs Faltantes para RNs Não Cobertas

**Problema:** 13 RNs do RF sem UC correspondente.

**Ação:** Para CADA RN não coberta, criar UC seguindo template oficial.

**Template de UC obrigatório:**

```yaml
- id: "UC0X-RFXXX"
  titulo: "[Título baseado na RN]"
  ator_principal: "[Baseado em RF.yaml > publico_afetado]"
  objetivo: "[Descrição da RN]"

  preconditions:
    - "Usuário autenticado"
    - "Permissão: [código da permissão]"
    - "[Dependências específicas da RN]"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "[Ação do usuário]"
        sistema: "[Resposta do sistema]"
      - passo: "FP-02"
        acao: "[...]"
        sistema: "[Validação da RN]"
      # Mínimo 5 passos

  fluxos_alternativos:
    FA-01:
      condicao: "[Cenário alternativo]"
      passos:
        - passo: "FA-01-01"
          acao: "[...]"
          sistema: "[...]"

  fluxos_excecao:
    FE-01:
      condicao: "[Violação da RN]"
      passos:
        - passo: "FE-01-01"
          acao: "[Payload inválido]"
          sistema: "HTTP 400 - [Mensagem específica da RN]"

  regras_aplicadas:
    - "RN-RFXXX-0Y"  # ← RN que este UC cobre

  covers:
    rf_items:
      - "RN-RFXXX-0Y"  # ← MESMO valor de regras_aplicadas

  pos_conditions:
    - "[Estado final esperado]"

  criterios_aceite:
    - "[Critério 1 da RN]"
    - "[Critério 2 da RN]"
    # Copiar de RF.yaml > regras_negocio[].criterios_aceite
```

**Regras críticas:**

1. **Mapeamento 1:1 ou N:1:** Cada RN DEVE estar em pelo menos 1 UC
2. **Fluxo de exceção obrigatório:** Se RN define validação, UC DEVE ter FE documentando violação
3. **Critérios de aceite sincronizados:** Copiar exatamente de `RF.yaml`
4. **HTTP codes corretos:** Se RN define `http_code: 422`, UC deve documentar isso em FE

**Exemplo prático (RF024 - RN-RF024-003):**

```yaml
# RF024.yaml
regras_negocio:
  - id: "RN-RF024-003"
    titulo: "Validação Referências Circulares Hierarquia"
    descricao: "Sistema DEVE detectar e bloquear loops infinitos (A → B → C → A)"
    criticidade: "CRÍTICA"
    validacao:
      http_code: 422
      mensagem_erro: "Referência circular detectada na hierarquia"

# UC-RF024.yaml (UC03 criado)
- id: "UC03-RF024"
  titulo: "Validar Hierarquia de Departamentos"
  ator_principal: "Gestor de RH"
  objetivo: "Garantir que hierarquia departamental não contenha loops"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Gestor define departamento B como pai de A"
        sistema: "Sistema executa algoritmo detecção ciclos (HashSet visitados)"
      - passo: "FP-02"
        acao: "Sistema valida caminho A → B"
        sistema: "Caminho válido, hierarquia salva"

  fluxos_excecao:
    FE-01:
      condicao: "Usuário tenta criar loop A → B → C → A"
      passos:
        - passo: "FE-01-01"
          acao: "PUT /departamentos/A { Id_Departamento_Pai: C }"
          sistema: "HTTP 422 Unprocessable Entity"
        - passo: "FE-01-02"
          sistema: |
            {
              "error": "Referência circular detectada na hierarquia",
              "caminho_invalido": "A → B → C → A",
              "departamentos_envolvidos": ["A", "B", "C"]
            }

  regras_aplicadas:
    - "RN-RF024-003"

  covers:
    rf_items:
      - "RN-RF024-003"

  criterios_aceite:
    - "Algoritmo usa HashSet para rastrear departamentos visitados"
    - "Loops são detectados antes de salvar no banco"
    - "Mensagem de erro clara indica caminho inválido"
    - "HTTP 422 retornado em caso de ciclo"
```

**Validação:** Após criar todos os UCs, executar:
```bash
python tools/docs/validator-rf-uc.py \
  --rf rf/.../RFXXX.yaml \
  --uc rf/.../UC-RFXXX.yaml
```

Deve retornar: `✅ Cobertura: 15/15 (100%)`

---

#### Etapa 10: Documentar Jobs Background

**Problema:** RF023 RN-CTR-023-04 (alertas), RF024 RN-RF024-005 (sync Azure AD) não documentados.

**Ação:** Criar UC específico para jobs background.

**Template UC Job Background:**

```yaml
- id: "UC0X-RFXXX"
  titulo: "Job Background - [Nome do Job]"
  ator_principal: "Sistema (Hangfire Scheduler)"
  objetivo: "[Descrição da RN do job]"
  tipo: "background_job"

  preconditions:
    - "Job Hangfire configurado: [expressão CRON]"
    - "[Dependências externas: API, banco, etc.]"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Job dispara às [horário] [timezone]"
        sistema: "Hangfire enfileira job BackgroundJob.Enqueue<[JobClass]>()"
      - passo: "FP-02"
        acao: "Worker executa método [JobClass].[MethodName]()"
        sistema: "Query busca registros elegíveis: [SQL/LINQ]"
      - passo: "FP-03"
        acao: "Sistema processa cada registro"
        sistema: "[Lógica específica: enviar e-mail, atualizar status, etc.]"
      - passo: "FP-04"
        sistema: "Auditoria registrada: [código de auditoria]"
      - passo: "FP-05"
        sistema: "Job marca conclusão (success/failure)"

  fluxos_excecao:
    FE-01:
      condicao: "Falha ao enviar e-mail"
      passos:
        - passo: "FE-01-01"
          sistema: "Retry policy: 3 tentativas com backoff exponencial"
        - passo: "FE-01-02"
          sistema: "Se 3 falhas → Dead Letter Queue + alerta operacional"

  regras_aplicadas:
    - "RN-RFXXX-0Y"

  covers:
    rf_items:
      - "RN-RFXXX-0Y"

  configuracao_job:
    expressao_cron: "[0 0 * * *]"
    timezone: "America/Sao_Paulo"
    retry_policy: "exponential_backoff"
    max_retries: 3
    timeout_seconds: 300

  criterios_aceite:
    - "Job executa diariamente no horário especificado"
    - "Auditoria completa de cada execução"
    - "Retry automático em caso de falha transiente"
    - "Dead Letter Queue para falhas permanentes"
```

**Exemplo prático (RF023 RN-CTR-023-04):**

```yaml
- id: "UC09-RF023"
  titulo: "Job Background - Alertas Automáticos de Vencimento de Contratos"
  ator_principal: "Sistema (Hangfire Scheduler)"
  objetivo: "Enviar alertas por e-mail + SignalR 30/60/90 dias antes do vencimento"
  tipo: "background_job"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Job dispara às 00:00 UTC"
        sistema: "BackgroundJob.Enqueue<ContratoAlertaJob>(x => x.ExecuteAsync())"
      - passo: "FP-02"
        sistema: |
          Query busca contratos:
          SELECT * FROM Contratos
          WHERE DataFim IN (
            DATEADD(day, 30, GETDATE()),
            DATEADD(day, 60, GETDATE()),
            DATEADD(day, 90, GETDATE())
          )
          AND Status IN ('Ativo', 'Aprovado')
          AND NOT EXISTS (
            SELECT 1 FROM AuditoriaAlerta
            WHERE ContratoId = Contratos.Id
            AND Codigo = 'CTR_CONTRATO_ALERTA_VENCIMENTO'
            AND DataCriacao >= DATEADD(day, -1, GETDATE())
          )
      - passo: "FP-03"
        sistema: "Para cada contrato, enviar e-mail ao responsável (template Razor)"
      - passo: "FP-04"
        sistema: "Publicar notificação SignalR: Hub.Clients.User(userId).SendAsync('ContratoAlerta')"
      - passo: "FP-05"
        sistema: |
          Gravar auditoria:
          INSERT INTO AuditoriaAlerta (
            ContratoId,
            Codigo = 'CTR_CONTRATO_ALERTA_VENCIMENTO',
            Tipo = 'Email+SignalR',
            Destinatario = usuario.Email,
            DataCriacao = GETDATE()
          )

  fluxos_excecao:
    FE-01:
      condicao: "SMTP falha ao enviar e-mail"
      passos:
        - passo: "FE-01-01"
          sistema: "Retry 3x com backoff: 1min, 5min, 15min"
        - passo: "FE-01-02"
          sistema: "Se 3 falhas → Dead Letter Queue + log ERROR"

  regras_aplicadas:
    - "RN-RF023-04"

  covers:
    rf_items:
      - "RN-RF023-04"

  configuracao_job:
    expressao_cron: "0 0 * * *"
    timezone: "UTC"
    retry_policy: "exponential_backoff"
    max_retries: 3
    timeout_seconds: 600
```

---

#### Etapa 11: Documentar Workflows Complexos

**Problema:** RF024 RN-RF024-006 (workflow aprovação multinível) sem UC.

**Template UC Workflow:**

```yaml
- id: "UC0X-RFXXX"
  titulo: "Workflow - [Nome do Workflow]"
  ator_principal: "[Ator que inicia]"
  atores_secundarios:
    - "[Aprovador Nível 1]"
    - "[Aprovador Nível 2]"
    - "[...]"
  objetivo: "[Descrição da RN]"
  tipo: "workflow"

  state_machine:
    estados:
      - id: "[Estado1]"
        descricao: "[...]"
      - id: "[Estado2]"
        descricao: "[...]"

    transicoes_permitidas:
      - de: "[Estado1]"
        para: "[Estado2]"
        acao: "[Nome da ação]"
        ator: "[Quem pode executar]"
        permissao: "[Código da permissão]"

    transicoes_proibidas:
      - de: "[EstadoFinal]"
        para: "*"
        motivo: "Estado terminal"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "[Ator] submete para aprovação"
        sistema: "Status = Pendente, Nível = 1"
      - passo: "FP-02"
        acao: "[Aprovador1] aprova"
        sistema: "Status = Aprovado_Nivel1, Nível = 2"
      # [...]

  fluxos_alternativos:
    FA-01:
      condicao: "[Aprovador] rejeita"
      passos:
        - passo: "FA-01-01"
          acao: "[Aprovador] clica Rejeitar + justificativa"
          sistema: "Status = Rejeitado, workflow interrompido"

  regras_aplicadas:
    - "RN-RFXXX-0Y"
```

**Exemplo prático (RF024 RN-RF024-006):**

```yaml
- id: "UC05-RF024"
  titulo: "Workflow - Aprovação de Movimentações Interdepartamentais"
  ator_principal: "Colaborador ou Gestor Origem"
  atores_secundarios:
    - "Líder Departamento Origem"
    - "Líder Departamento Destino"
    - "Gerente de RH"
  objetivo: "Garantir aprovação sequencial em 3 níveis para transferências"
  tipo: "workflow"

  state_machine:
    estados:
      - id: "Pendente"
        descricao: "Aguardando aprovação líder origem"
      - id: "Aprovado_Origem"
        descricao: "Origem aprovou, aguarda destino"
      - id: "Aprovado_Destino"
        descricao: "Destino aprovou, aguarda RH"
      - id: "Aprovado_RH"
        descricao: "RH aprovou, movimentação efetivada"
      - id: "Rejeitado"
        descricao: "Rejeitado em qualquer nível"

    transicoes_permitidas:
      - de: "Pendente"
        para: "Aprovado_Origem"
        acao: "Aprovar (Nível 1)"
        ator: "Líder Departamento Origem"
        permissao: "departamentos:movimentacoes:approve_origem"

      - de: "Aprovado_Origem"
        para: "Aprovado_Destino"
        acao: "Aprovar (Nível 2)"
        ator: "Líder Departamento Destino"
        permissao: "departamentos:movimentacoes:approve_destino"

      - de: "Aprovado_Destino"
        para: "Aprovado_RH"
        acao: "Aprovar (Nível 3 - Final)"
        ator: "Gerente de RH"
        permissao: "departamentos:movimentacoes:approve_rh"

      - de: "*"
        para: "Rejeitado"
        acao: "Rejeitar"
        ator: "Qualquer aprovador"
        permissao: "[permissão do nível]"

    transicoes_proibidas:
      - de: "Aprovado_RH"
        para: "*"
        motivo: "Estado final - movimentação efetivada"
      - de: "Rejeitado"
        para: "*"
        motivo: "Estado final - workflow encerrado"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Colaborador solicita transferência Depto A → Depto B"
        sistema: |
          POST /departamentos/movimentacoes
          {
            "Id_Usuario": "...",
            "Id_Departamento_Origem": "A",
            "Id_Departamento_Destino": "B",
            "Tipo_Movimentacao": "Transferencia",
            "Motivo": "Realocação para novo projeto"
          }
          Status = Pendente

      - passo: "FP-02"
        acao: "Sistema notifica Líder de A (e-mail + SignalR)"
        sistema: "Notificação: 'Aprovação pendente: [Colaborador] solicitou transferência'"

      - passo: "FP-03"
        acao: "Líder de A aprova"
        sistema: |
          POST /departamentos/movimentacoes/{id}/aprovar-origem
          Status = Aprovado_Origem
          Auditoria registrada

      - passo: "FP-04"
        acao: "Sistema notifica Líder de B"
        sistema: "Notificação: 'Aprovação pendente (Nível 2)'"

      - passo: "FP-05"
        acao: "Líder de B aprova"
        sistema: "Status = Aprovado_Destino"

      - passo: "FP-06"
        acao: "Sistema notifica Gerente RH"
        sistema: "Notificação: 'Aprovação final pendente (Nível 3)'"

      - passo: "FP-07"
        acao: "Gerente RH aprova"
        sistema: |
          Status = Aprovado_RH
          Dt_Efetivacao = NOW()
          Atualiza Usuario_Departamento (lotação principal)

  fluxos_alternativos:
    FA-01:
      condicao: "Líder de A rejeita no Nível 1"
      passos:
        - passo: "FA-01-01"
          acao: "Líder clica Rejeitar + justificativa"
          sistema: |
            POST /departamentos/movimentacoes/{id}/rejeitar
            { "Motivo": "Projeto crítico em andamento" }
            Status = Rejeitado
            Workflow encerrado
        - passo: "FA-01-02"
          sistema: "Notificação ao colaborador: 'Transferência rejeitada por [Líder]'"

  fluxos_excecao:
    FE-01:
      condicao: "Usuário sem permissão tenta aprovar"
      passos:
        - passo: "FE-01-01"
          acao: "POST /movimentacoes/{id}/aprovar-origem (sem permissão)"
          sistema: "HTTP 403 Forbidden - Você não tem permissão para aprovar neste nível"

    FE-02:
      condicao: "Tentativa de aprovar fora de sequência"
      passos:
        - passo: "FE-02-01"
          acao: "Gerente RH tenta aprovar antes de Líder B"
          sistema: |
            HTTP 422 Unprocessable Entity
            "Aprovação inválida: status atual é Aprovado_Origem, próximo aprovador é Líder Destino"

  regras_aplicadas:
    - "RN-RF024-006"

  covers:
    rf_items:
      - "RN-RF024-006"

  criterios_aceite:
    - "Aprovação sequencial estrita: Origem → Destino → RH"
    - "Notificações automáticas em cada transição"
    - "Rejeição em qualquer nível encerra workflow"
    - "Auditoria completa de cada aprovação/rejeição"
    - "Permissões RBAC validadas em cada endpoint"
```

---

#### Etapa 12: Documentar Integrações Externas

**Problema:** RF024 RN-RF024-005 (Azure AD sync) sem documentação de integração.

**Template UC Integração Externa:**

```yaml
- id: "UC0X-RFXXX"
  titulo: "Integração - [Nome do Sistema Externo]"
  ator_principal: "Sistema (Job ou API)"
  objetivo: "[Descrição da integração]"
  tipo: "integracao_externa"

  sistema_externo:
    nome: "[Nome]"
    tipo: "[API REST, SOAP, GraphQL, etc.]"
    autenticacao: "[OAuth2, API Key, Certificate, etc.]"
    endpoint_base: "[URL]"
    documentacao: "[URL da doc oficial]"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Sistema autentica no [Sistema Externo]"
        sistema: "[Método de auth: OAuth2 client credentials, etc.]"
      - passo: "FP-02"
        acao: "Sistema prepara payload"
        sistema: |
          [Estrutura JSON/XML do request]
      - passo: "FP-03"
        acao: "Sistema envia request: [HTTP METHOD] [ENDPOINT]"
        sistema: "[Response esperado]"
      - passo: "FP-04"
        sistema: "Sistema processa response e atualiza banco local"

  fluxos_excecao:
    FE-01:
      condicao: "Timeout (>30s)"
      passos:
        - passo: "FE-01-01"
          sistema: "Retry com backoff exponencial: 1min, 5min, 15min"

    FE-02:
      condicao: "HTTP 401 Unauthorized (token expirado)"
      passos:
        - passo: "FE-02-01"
          sistema: "Refresh token OAuth2"
        - passo: "FE-02-02"
          sistema: "Retry request com novo token"

  regras_aplicadas:
    - "RN-RFXXX-0Y"

  mapeamento_dados:
    direcao: "[IControlIT → Externo | Externo → IControlIT | Bidirectional]"
    transformacoes:
      - campo_local: "[Nome campo]"
        campo_externo: "[Nome campo no sistema externo]"
        transformacao: "[Descrição: ex. GUID → String, Date → ISO8601]"
```

**Exemplo prático (RF024 RN-RF024-005):**

```yaml
- id: "UC10-RF024"
  titulo: "Integração - Sincronização Automática Azure AD (Microsoft Graph API)"
  ator_principal: "Sistema (Hangfire Job)"
  objetivo: "Criar grupos de segurança no Azure AD ao criar departamentos no IControlIT"
  tipo: "integracao_externa"

  sistema_externo:
    nome: "Microsoft Graph API"
    tipo: "REST API"
    autenticacao: "OAuth2 Client Credentials (App Registration)"
    endpoint_base: "https://graph.microsoft.com/v1.0"
    documentacao: "https://learn.microsoft.com/graph/api/group-post-groups"
    scopes:
      - "Group.ReadWrite.All"
      - "Directory.ReadWrite.All"

  fluxo_principal:
    FP:
      - passo: "FP-01"
        acao: "Job executa às 03:00 BRT"
        sistema: "BackgroundJob.Enqueue<AzureADSyncJob>()"

      - passo: "FP-02"
        sistema: |
          Query departamentos criados/alterados nas últimas 24h:
          SELECT * FROM Departamentos
          WHERE (DataCriacao >= DATEADD(hour, -24, GETDATE())
                 OR DataAlteracao >= DATEADD(hour, -24, GETDATE()))
          AND Azure_AD_Object_Id IS NULL

      - passo: "FP-03"
        acao: "Sistema autentica no Azure AD"
        sistema: |
          POST https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token
          Content-Type: application/x-www-form-urlencoded

          client_id={appId}
          &client_secret={secret}
          &scope=https://graph.microsoft.com/.default
          &grant_type=client_credentials

          Response: { "access_token": "...", "expires_in": 3600 }

      - passo: "FP-04"
        acao: "Para cada departamento, criar grupo Azure AD"
        sistema: |
          POST https://graph.microsoft.com/v1.0/groups
          Authorization: Bearer {access_token}
          Content-Type: application/json

          {
            "displayName": "IControlIT - {Codigo_Departamento} - {Nome_Departamento}",
            "mailNickname": "icontrolit-{Codigo_Departamento}",
            "mailEnabled": false,
            "securityEnabled": true,
            "groupTypes": []
          }

          Response: {
            "id": "e1a2b3c4-...",
            "displayName": "IControlIT - DIR-TI - Diretoria de TI"
          }

      - passo: "FP-05"
        sistema: |
          Atualizar departamento local:
          UPDATE Departamentos
          SET Azure_AD_Object_Id = 'e1a2b3c4-...'
          WHERE Id_Departamento = '{id}'

      - passo: "FP-06"
        sistema: |
          Gravar auditoria:
          INSERT INTO AuditoriaIntegracao (
            Entidade = 'Departamento',
            EntidadeId = '{id}',
            SistemaExterno = 'Azure AD',
            Operacao = 'CREATE_GROUP',
            Payload = '{JSON do request}',
            Response = '{JSON do response}',
            Status = 'Success'
          )

  fluxos_excecao:
    FE-01:
      condicao: "HTTP 401 Unauthorized (token expirado)"
      passos:
        - passo: "FE-01-01"
          sistema: "Refresh token OAuth2 (repetir FP-03)"
        - passo: "FE-01-02"
          sistema: "Retry request com novo token"

    FE-02:
      condicao: "HTTP 409 Conflict (grupo já existe)"
      passos:
        - passo: "FE-02-01"
          sistema: "GET https://graph.microsoft.com/v1.0/groups?$filter=mailNickname eq 'icontrolit-{codigo}'"
        - passo: "FE-02-02"
          sistema: "Atualizar Azure_AD_Object_Id com ID do grupo existente"

    FE-03:
      condicao: "HTTP 429 Too Many Requests (rate limit)"
      passos:
        - passo: "FE-03-01"
          sistema: "Aguardar tempo indicado no header Retry-After"
        - passo: "FE-03-02"
          sistema: "Retry request"

    FE-04:
      condicao: "Timeout (>30s)"
      passos:
        - passo: "FE-04-01"
          sistema: "Retry 3x com backoff: 1min, 5min, 15min"
        - passo: "FE-04-02"
          sistema: "Se 3 falhas → Dead Letter Queue + alerta DevOps"

  regras_aplicadas:
    - "RN-RF024-005"

  covers:
    rf_items:
      - "RN-RF024-005"

  mapeamento_dados:
    direcao: "IControlIT → Azure AD (unidirecional)"
    transformacoes:
      - campo_local: "Codigo_Departamento + Nome_Departamento"
        campo_externo: "displayName"
        transformacao: "Concatenação: 'IControlIT - {Codigo} - {Nome}'"

      - campo_local: "Codigo_Departamento"
        campo_externo: "mailNickname"
        transformacao: "Lowercase + prefixo: 'icontrolit-{codigo}'"

      - campo_local: "Id_Departamento (Guid)"
        campo_externo: "id (retornado pela API)"
        transformacao: "Armazenado em Azure_AD_Object_Id após criação"

  configuracao_job:
    expressao_cron: "0 3 * * *"  # 03:00 BRT
    timezone: "America/Sao_Paulo"
    retry_policy: "exponential_backoff"
    max_retries: 3
    timeout_seconds: 300

  criterios_aceite:
    - "Grupos criados no Azure AD com nome padronizado"
    - "Azure_AD_Object_Id sempre preenchido após sync"
    - "Retry automático em caso de falhas transientes"
    - "Auditoria completa de cada operação (request + response)"
    - "Idempotência: grupo existente não causa falha"
```

---

### FASE 3: VALIDAÇÃO E ENTREGA (Etapas 13-15)

#### Etapa 13: Validação Automática (BLOQUEANTE)

Executar validador e corrigir até exit code 0:

```bash
python tools/docs/validator-rf-uc.py \
  --rf rf/.../RFXXX.yaml \
  --uc rf/.../UC-RFXXX.yaml

# Exit code DEVE ser 0
echo $?  # Deve imprimir: 0
```

**Critérios de aprovação (todos obrigatórios):**

1. ✅ Cobertura: 100% (todas RNs do RF.yaml presentes em UC.yaml)
2. ✅ Nomenclatura: Apenas `RN-RFXXX-NNN` (zero `RN-CTR-`, `RN-DEP-`, etc.)
3. ✅ Catálogo limpo: Zero `RF\d{3}-CRUD-|VAL-|SEC-`
4. ✅ UC.md ↔ UC.yaml sincronizados (se UC.md existir)
5. ✅ Todos os UCs tem `covers.rf_items` e `regras_aplicadas` consistentes

**Se validação falhar:**
- NÃO avançar para Etapa 11
- Corrigir problemas identificados
- Re-executar validador
- Repetir até exit code 0

---

#### Etapa 14: Atualizar STATUS.yaml (OBRIGATÓRIO - MELHORIA #5)

**REGRA CRÍTICA:** O agente DEVE atualizar STATUS.yaml AUTOMATICAMENTE. NÃO é opcional.

Após validação aprovada (exit code 0), atualizar `STATUS.yaml`:

```yaml
# STATUS.yaml
documentacao:
  rf: true
  uc: true  # ← Atualizar para true
  md: [existente]
  wf: [existente]
  user_stories: [existente]

validacoes:
  rf_uc_cobertura_total: true  # ← Atualizar para true
  uc_nomenclatura_padrao: true  # ← Adicionar
  uc_catalogo_limpo: true       # ← Adicionar
  uc_jobs_documentados: true    # ← Adicionar se aplicável
  uc_workflows_documentados: true  # ← Adicionar se aplicável
  uc_integracoes_documentadas: true  # ← Adicionar se aplicável

adequacao_uc:
  data_execucao: "2025-12-31"
  versao_contrato: "1.0"

  cobertura_antes:
    rns_totais: [N antes]
    rns_cobertas: [M antes]
    percentual: "[X%]"
    nomenclatura_padrao: "[Y%]"
    ucs_totais: [K antes]

  cobertura_depois:
    rns_totais: [N depois]
    rns_cobertas: [N depois]  # SEMPRE 100%
    percentual: "100%"
    nomenclatura_padrao: "100%"
    ucs_totais: [K depois]
    jobs_documentados: [J]
    integracoes_documentadas: [I]

  problemas_corrigidos:
    - tipo: "nomenclatura"
      descricao: "Migração RN-CTR-XXX → RN-RFXXX-NNN"
      arquivos_afetados: ["RF.yaml", "UC.yaml"]
      total_substituicoes: [N]

    - tipo: "catálogo_híbrido"
      descricao: "Remoção de códigos RF-CRUD/VAL/SEC"
      total_removidos: [M]

    - tipo: "gap_cobertura"
      descricao: "UCs criados para cobrir RNs órfãs"
      ucs_criados: ["UC05", "UC06", ...]
      rns_cobertas: ["RN-RFXXX-08", "RN-RFXXX-09", ...]

    - tipo: "gap_documentacao"
      descricao: "Jobs background documentados"
      ucs_criados: ["UC10", "UC11"]
      cobre_rns: ["RN-RFXXX-04", "RN-RFXXX-13"]

  validacoes:
    rf_uc_cobertura: "100% (N/N)"
    nomenclatura_padrao: "100%"
    catalogo_limpo: true
    uc_yaml_uc_md_sincronizados: true
    validador_exit_code: 0

  metricas:
    tempo_total_execucao: "[Xh Ymin]"
    ucs_criados: [N]
    ucs_editados: [M]
    nomenclatura_migrada: [P]
    catalogo_limpo: [Q]
```

**🤖 VALIDAÇÃO AUTOMÁTICA OBRIGATÓRIA:**

```python
import yaml
from pathlib import Path
from datetime import datetime

status_file = Path('rf/.../STATUS.yaml')

# Ler STATUS.yaml atual
with open(status_file) as f:
    status_data = yaml.safe_load(f)

# Verificar se seção adequacao_uc existe
if 'adequacao_uc' not in status_data:
    print("❌ ERRO CRÍTICO: STATUS.yaml NÃO foi atualizado!")
    print("🤖 AÇÃO AUTOMÁTICA: Adicionando seção adequacao_uc...")

    status_data['adequacao_uc'] = {
        'data_execucao': datetime.now().strftime('%Y-%m-%d'),
        'versao_contrato': '1.0',
        'cobertura_antes': {
            'rns_totais': rns_totais_antes,
            'rns_cobertas': rns_cobertas_antes,
            'percentual': f"{(rns_cobertas_antes/rns_totais_antes)*100:.1f}%"
        },
        'cobertura_depois': {
            'rns_totais': rns_totais_depois,
            'rns_cobertas': rns_totais_depois,  # SEMPRE 100%
            'percentual': "100%"
        },
        'problemas_corrigidos': problemas_list,
        'validacoes': validacoes_dict,
        'metricas': metricas_dict
    }

    # Salvar STATUS.yaml
    with open(status_file, 'w') as f:
        yaml.dump(status_data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

    print("✅ STATUS.yaml atualizado automaticamente")
else:
    print("✅ STATUS.yaml já contém seção adequacao_uc")

# Validar campos obrigatórios
required_fields = [
    'adequacao_uc.data_execucao',
    'adequacao_uc.versao_contrato',
    'adequacao_uc.cobertura_antes',
    'adequacao_uc.cobertura_depois',
    'adequacao_uc.validacoes'
]

missing_fields = []
for field in required_fields:
    keys = field.split('.')
    temp = status_data
    for key in keys:
        if key not in temp:
            missing_fields.append(field)
            break
        temp = temp[key]

if missing_fields:
    print(f"❌ ERRO: Campos obrigatórios ausentes em STATUS.yaml: {missing_fields}")
    print("🤖 AÇÃO: Contrato NÃO pode ser marcado como concluído até STATUS.yaml estar completo")
    sys.exit(1)
else:
    print("✅ STATUS.yaml validado - todos os campos obrigatórios presentes")
```

**IMPORTANTE:** Esta etapa NÃO é negociável. O agente DEVE atualizar STATUS.yaml automaticamente antes de finalizar o contrato.

---

#### Etapa 15: Relatório Final

**IMPORTANTE:** Operações Git (commit, merge, push) são responsabilidade do usuário.

Criar `.temp_ia/adequacao-uc-RFXXX-relatorio.md`:

```markdown
# RELATÓRIO DE ADEQUAÇÃO COMPLETA - UC-RFXXX

**Data:** 2025-12-31
**Contrato:** CONTRATO-ADEQUACAO-COMPLETA-UC v1.0
**RF:** RFXXX - [Nome]
**Executor:** Claude Sonnet 4.5

---

## RESUMO EXECUTIVO

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Cobertura RN → UC | X/Y (Z%) | Y/Y (100%) | +[N] RNs |
| Nomenclatura padrão | ❌ | ✅ | Migrado |
| Catálogo limpo | ❌ | ✅ | Removido |
| Jobs documentados | 0 | [N] | +[N] UCs |
| Workflows documentados | 0 | [M] | +[M] UCs |
| Integrações documentadas | 0 | [P] | +[P] UCs |
| Validação automática | ❌ FAIL | ✅ PASS | Exit code 0 |

---

## PROBLEMAS CORRIGIDOS

### 1. Nomenclatura Não-Padrão
- **Antes:** `RN-CTR-023-XX` (10 ocorrências)
- **Depois:** `RN-RF023-XX` (padrão oficial)
- **Script:** Migração automática com regex

### 2. Catálogo Híbrido
- **Antes:** 15 códigos `RF023-CRUD-XX`, `RF023-VAL-XX`
- **Depois:** Apenas RNs reais em `covers.rf_items`
- **Ação:** Limpeza completa de `covers` e `regras_aplicadas`

### 3. Gaps de Cobertura
- **RNs sem UC (antes):** [Lista de N RNs]
- **UCs criados:** UC0X, UC0Y, UC0Z (total: [N])
- **Detalhamento:**
  - UC0X: Cobertura de RN-RFXXX-04 (Job alertas automáticos)
  - UC0Y: Cobertura de RN-RFXXX-06 (Workflow aprovação)
  - UC0Z: Cobertura de RN-RFXXX-05 (Integração Azure AD)

---

## VALIDAÇÃO FINAL

```bash
$ python tools/docs/validator-rf-uc.py \
    --rf rf/.../RFXXX.yaml \
    --uc rf/.../UC-RFXXX.yaml

✅ Nomenclatura: 15/15 RNs no padrão RN-RFXXX-NNN
✅ Cobertura: 15/15 RNs (100%)
✅ Consistência: UC.yaml ↔ RF.yaml sincronizados
✅ Catálogo: 0 códigos não-padrão encontrados

Exit code: 0 (APROVADO)
```

---

## PRÓXIMOS PASSOS

1. ✅ UC-RFXXX.yaml adequado e validado
2. ⏭️ Executar **CONTRATO-EXECUCAO-BACKEND** para implementar
3. ⏭️ Executar **CONTRATO-TESTER-BACKEND** para validar contratos
4. ⏭️ Executar **CONTRATO-EXECUCAO-FRONTEND** após backend aprovado

---

**Status:** ✅ ADEQUAÇÃO CONCLUÍDA COM SUCESSO
**Branch:** feature/adequacao-uc-RFXXX (merged to dev)
**Commit:** [hash]
```

---

## CRITÉRIOS DE PRONTO (DEFINITION OF DONE)

### ⚠️ REGRA DE ZERO TOLERÂNCIA

**A PARTIR DE AGORA:**
- ✅ **APROVADO** = TODOS os critérios abaixo atendidos + ZERO gaps (exceto falhas técnicas Python)
- ❌ **REPROVADO** = Qualquer critério falhando OU qualquer gap (CRÍTICO, IMPORTANTE, **MENOR**)

**ÚNICA EXCEÇÃO PERMITIDA:**
- ⚠️ Falhas técnicas do validador Python (timeout, erro de script, etc.)
- Gaps de funcionalidade/nomenclatura **SEMPRE** reprovam

---

Este contrato só é considerado CONCLUÍDO quando TODOS os critérios abaixo forem atendidos:

### ✅ CRITÉRIOS OBRIGATÓRIOS (100% - SEM TOLERÂNCIA)

- [ ] Todo list completa (15 etapas) executada
- [ ] Backup do UC original criado (`.backup-*`)
- [ ] **Nomenclatura migrada: ZERO `RN-CTR-|DEP-|FIN-`** ← BLOQUEANTE
- [ ] **Nomenclatura de fluxos: ZERO `FA-\d{3}` ou `FE-\d{3}`** ← **BLOQUEANTE**
- [ ] **Catálogo limpo: ZERO `RF\d{3}-CRUD-|VAL-|SEC-`** ← BLOQUEANTE
- [ ] **Cobertura 100%: TODAS RNs do RF em UCs** ← BLOQUEANTE
- [ ] Entidades órfãs documentadas (se aplicável)
- [ ] Jobs background documentados (se aplicável)
- [ ] Workflows complexos documentados (se aplicável)
- [ ] Integrações externas documentadas (se aplicável)
- [ ] **UC.yaml ↔ UC.md 100% sincronizados** ← BLOQUEANTE
- [ ] **Validação aprovada: `validator-rf-uc.py` exit code 0** ← BLOQUEANTE
- [ ] **STATUS.yaml atualizado com flags de validação** ← OBRIGATÓRIO
- [ ] Diagnóstico gerado (`.temp_ia/adequacao-uc-RFXXX-diagnostico.md`) - **OPCIONAL** (recomendado)
- [ ] Relatório final gerado (`.temp_ia/adequacao-uc-RFXXX-relatorio.md`) - **OPCIONAL** (recomendado)

### ❌ CRITÉRIOS QUE REPROVAM IMEDIATAMENTE

**NOMENCLATURA DE FLUXOS INCORRETA** (ex: FA-001 vs FA-UC00-001):
- ❌ Qualquer fluxo alternativo no formato `FA-\d{3}` (ex: FA-001, FA-002)
- ❌ Qualquer fluxo de exceção no formato `FE-\d{3}` (ex: FE-001, FE-002)
- ✅ **OBRIGATÓRIO:** `FA-UCNN-NNN` (ex: FA-UC00-001, FA-UC01-002)
- ✅ **OBRIGATÓRIO:** `FE-UCNN-NNN` (ex: FE-UC00-001, FE-UC01-002)

**Motivo:** Quebra rastreabilidade automática, inconsistente com templates v2.0

### ⚠️ ÚNICA EXCEÇÃO: Falhas Técnicas Python

**Aprovação condicional SOMENTE se:**
```
14/15 critérios PASS (faltou apenas validador Python)
0 gaps CRÍTICOS
0 gaps IMPORTANTES
0 gaps MENORES
Validador falhou por: Erro técnico Python (não gap funcional)
```

**Neste caso:**
```
Veredicto: ⚠️ APROVADO COM RESSALVA TÉCNICA
Ação: Investigar validador Python, mas RF pode prosseguir
```

**BLOQUEIO:** Se QUALQUER critério funcional falhar, contrato NÃO pode ser marcado como concluído.

---

## VIOLAÇÕES E PENALIDADES

### ⚠️ REGRA DE ZERO TOLERÂNCIA PARA GAPS

**A PARTIR DE AGORA, NÃO EXISTEM MAIS "VIOLAÇÕES LEVES".**

Qualquer gap, independente da severidade antiga (CRÍTICO, IMPORTANTE, **MENOR**), é considerado **BLOQUEANTE**.

### ❌ VIOLAÇÕES BLOQUEANTES (REPROVAÇÃO IMEDIATA)

#### 1. Nomenclatura de Fluxos Incorreta (Antigamente "MENOR" - AGORA BLOQUEANTE)
- **Exemplo:** `FA-001` em vez de `FA-UC00-001`
- **Impacto:** Quebra rastreabilidade automática, scripts de validação falham
- **Severidade:** **CRÍTICO** (elevado de MENOR para CRÍTICO)
- **Ação:** Correção obrigatória antes de aprovar

#### 2. Nomenclatura de RNs Inconsistente (SEMPRE FOI CRÍTICO)
- **Exemplo:** 1 RN ainda em formato `RN-CTR-023-01`
- **Impacto:** Validador falha, cobertura incorreta
- **Severidade:** **CRÍTICO**
- **Ação:** Migração obrigatória para `RN-RFXXX-NNN`

#### 3. Catálogo Híbrido Não 100% Limpo (SEMPRE FOI CRÍTICO)
- **Exemplo:** 1 código `RF-CRUD-01` esquecido em `covers.rf_items`
- **Impacto:** Rastreabilidade quebrada
- **Severidade:** **CRÍTICO**
- **Ação:** Limpeza obrigatória antes de aprovar

#### 4. Falta de RN-UC Específicas (Antigamente "MENOR" - AGORA BLOQUEANTE)
- **Exemplo:** UC sem `RN-UC-XXX-NNN` própria
- **Impacto:** Validação incompleta de comportamento específico do UC
- **Severidade:** **IMPORTANTE** (elevado de MENOR para IMPORTANTE)
- **Ação:** Criação obrigatória de RN-UC específicas

#### 5. Critérios de Aceite Não Sincronizados (SEMPRE FOI IMPORTANTE)
- **Exemplo:** UC.yaml tem 5 critérios, RF.yaml tem 8
- **Impacto:** Divergência RF ↔ UC
- **Severidade:** **IMPORTANTE**
- **Ação:** Sincronização obrigatória antes de aprovar

---

### 🚨 VIOLAÇÕES GRAVES (BLOQUEIO DE EXECUÇÃO)

- Cobertura <100% após execução do contrato
- Validador com exit code ≠ 0 (exceto falhas técnicas Python)
- STATUS.yaml não atualizado
- Merge sem validação prévia
- **QUALQUER gap MENOR não corrigido** ← **NOVO!**

**Ação:** Execução considerada INVÁLIDA. Rollback obrigatório.

---

### ⚠️ VIOLAÇÕES CRÍTICAS (FALHA TOTAL DO CONTRATO)

- Alteração de RF.yaml (imutável)
- Deleção de UCs existentes sem justificativa
- Commit sem passar pelo validador
- Merge direto para main (bypass de dev)
- **Aprovar RF com gaps "MENOR" sem correção** ← **NOVO!**

**Ação:** Revert imediato + análise de causa raiz.

---

### 📊 EXEMPLO DE APLICAÇÃO DA ZERO TOLERÂNCIA

**Cenário:** RF006 validado com 3 gaps marcados como "MENOR"

**ANTES (COMPORTAMENTO ANTIGO - INCORRETO):**
```
Gap 1: Nomenclatura de fluxos (FA-001 vs FA-UC00-001)
Severidade: MENOR
Bloqueia aprovação? ❌ NÃO

Gap 2: Falta RN-UC específicas
Severidade: MENOR
Bloqueia aprovação? ❌ NÃO

Gap 3: Arquivo diagnóstico ausente
Severidade: MENOR
Bloqueia aprovação? ❌ NÃO

Veredicto: ✅ APROVADO (100%)  ← INCORRETO!
```

**AGORA (COMPORTAMENTO NOVO - CORRETO):**
```
Gap 1: Nomenclatura de fluxos (FA-001 vs FA-UC00-001)
Severidade: CRÍTICO (elevado de MENOR)
Bloqueia aprovação? ✅ SIM
Ação: Corrigir 42 violações antes de aprovar

Gap 2: Falta RN-UC específicas
Severidade: IMPORTANTE (elevado de MENOR)
Bloqueia aprovação? ✅ SIM
Ação: Criar RN-UC específicas antes de aprovar

Gap 3: Arquivo diagnóstico ausente
Severidade: MENOR (mantido)
Bloqueia aprovação? ✅ SIM (ZERO TOLERÂNCIA)
Ação: Criar arquivo diagnóstico antes de aprovar

Veredicto: ❌ REPROVADO (<80%)  ← CORRETO!
Motivo: 3 gaps detectados (ZERO TOLERÂNCIA)
```

---

### ✅ ÚNICA EXCEÇÃO: Falhas Técnicas Python

**Cenário válido para aprovação com ressalva:**
```
Validação #1-9: ✅ PASS
Validação #10 (validator-rf-uc.py): ❌ FAIL
Motivo da falha: Timeout do script Python (não gap funcional)

Gaps CRÍTICOS: 0
Gaps IMPORTANTES: 0
Gaps MENORES: 0

Veredicto: ⚠️ APROVADO COM RESSALVA TÉCNICA
Ação: RF pode prosseguir, investigar script Python
```

**Cenário INVÁLIDO (não é exceção):**
```
Validação #1-9: ✅ PASS
Validação #10 (validator-rf-uc.py): ❌ FAIL
Motivo da falha: Exit code 11 (RNs detectadas - gap funcional)

Gap 1: Nomenclatura de fluxos (42 violações)
Severidade: CRÍTICO

Veredicto: ❌ REPROVADO
Ação: Corrigir gaps antes de aprovar (NÃO é falha técnica)
```

---

## MÉTRICAS DE SUCESSO

| KPI | Meta | Medição |
|-----|------|---------|
| Cobertura RN → UC | 100% | `validator-rf-uc.py` |
| Nomenclatura padrão | 100% | Grep por `RN-[^R][^F]` = 0 |
| Catálogo limpo | 100% | Grep por `RF\d{3}-(CRUD\|VAL\|SEC)` = 0 |
| Jobs documentados | 100% | Todas RNs tipo `background_job` em UC |
| Workflows documentados | 100% | Todas RNs tipo `workflow` em UC |
| Integrações documentadas | 100% | Todas RNs tipo `integracao` em UC |
| Tempo de execução | ≤ 4h | Timestamp início → fim |
| Exit code validador | 0 | `echo $?` após validação |

---

## MODO DE EXECUÇÃO

### Modo 1: RF Individual (Análise Profunda)

**Prompt:**
```
Executar CONTRATO-ADEQUACAO-COMPLETA-UC para RF024.
Seguir D:\IC2\CLAUDE.md.
```

**Comportamento:**
- Auditoria detalhada de RF024
- Correção completa com análise contextual de cada RN
- Criação de UCs narrativos completos
- Relatório individual detalhado

---

### Modo 2: Lote de RFs (Adequação em Massa)

**Prompt:**
```
Executar CONTRATO-ADEQUACAO-COMPLETA-UC para RF001-RF066.
Seguir D:\IC2\CLAUDE.md.
Modo: batch
```

**Comportamento:**
1. **Auditoria automática** de todos os 66 RFs
2. **Priorização** por severidade:
   - Crítico: 0-20% cobertura
   - Alto: 21-50% cobertura
   - Médio: 51-80% cobertura
   - Baixo: 81-99% cobertura
3. **Correção sequencial** dos mais críticos primeiro
4. **Relatório consolidado** ao final

**Exemplo de saída:**

```
📊 AUDITORIA INICIAL (66 RFs):
   - Crítico (0-20%): 8 RFs → RF024, RF025, RF026, RF027, RF028, RF029, RF030, RF055
   - Alto (21-50%): 12 RFs → [lista]
   - Médio (51-80%): 15 RFs → [lista]
   - Baixo (81-99%): 10 RFs → RF021, RF023, [...]
   - Conforme (100%): 21 RFs → RF001, RF002, RF003, RF022, [...]

🔧 ADEQUAÇÃO EM PROGRESSO:

[1/26] RF028 (0.0% → 100%) - SLA Operações
   ✅ 12 UCs criados
   ✅ 1 job documentado
   ✅ Validação: exit code 0
   ⏱️ Tempo: 45min

[2/26] RF024 (6.7% → 100%) - Gestão Departamentos
   ✅ 14 UCs criados
   ✅ 1 workflow documentado
   ✅ 1 integração Azure AD documentada
   ✅ Validação: exit code 0
   ⏱️ Tempo: 1h20min

[...]

✅ ADEQUAÇÃO COMPLETA: 26/26 RFs corrigidos
⏱️ Tempo total: 18h35min
📊 Cobertura geral: 85.2% → 100%
```

---

## EXEMPLO DE EXECUÇÃO COMPLETA (MODO INDIVIDUAL)

### Prompt de Ativação:

```
Executar CONTRATO-ADEQUACAO-COMPLETA-UC para RF024.
Seguir D:\IC2\CLAUDE.md.
```

### Saída Esperada:

```
✅ Etapa 1/13: Todo list criada
✅ Etapa 2/13: Branch feature/adequacao-uc-RF024 criado
✅ Etapa 3/13: Diagnóstico completo
   - RNs no RF: 15
   - RNs no UC: 1
   - Gaps: 14
   - Nomenclatura: 0 problemas (já no padrão)
   - Catálogo: 15 códigos híbridos

✅ Etapa 4/13: Nomenclatura migrada (0 alterações - já conforme)
✅ Etapa 5/13: Catálogo limpo (15 códigos removidos)
✅ Etapa 6/13: UCs faltantes criados:
   - UC02-RF024: Hierarquia recursiva
   - UC03-RF024: Validação ciclos
   - UC04-RF024: Líder obrigatório
   - UC05-RF024: Workflow movimentações
   - UC06-RF024: Lotação matricial
   - UC07-RF024: Organograma visual
   - UC08-RF024: Dashboard headcount
   - UC09-RF024: Analytics turnover
   - UC10-RF024: Integração Azure AD (job)
   - [... mais 5 UCs]

✅ Etapa 7/13: Jobs background documentados (1):
   - UC10-RF024: Sincronização Azure AD

✅ Etapa 8/13: Workflows documentados (1):
   - UC05-RF024: Aprovação multinível

✅ Etapa 9/13: Integrações externas documentadas (1):
   - UC10-RF024: Microsoft Graph API

✅ Etapa 10/13: Validação automática
   $ python validator-rf-uc.py --rf RF024.yaml --uc UC-RF024.yaml
   ✅ Cobertura: 15/15 (100%)
   ✅ Nomenclatura: 15/15 padrão
   ✅ Catálogo: 0 códigos híbridos
   Exit code: 0

✅ Etapa 11/13: STATUS.yaml atualizado
✅ Etapa 12/13: Commit + merge para dev
✅ Etapa 13/13: Relatório final gerado

📊 RESUMO:
- Cobertura: 1/15 (6.7%) → 15/15 (100%)
- Gaps corrigidos: 14
- UCs criados: 14
- Jobs documentados: 1
- Workflows documentados: 1
- Integrações documentadas: 1
- Validação: ✅ APROVADO (exit code 0)
- Tempo: 2h15min

✅ ADEQUAÇÃO COMPLETA DE UC-RF024 CONCLUÍDA COM SUCESSO
```

---

## CONTRATO DE GARANTIA

Após execução deste contrato, GARANTE-SE:

1. ✅ **100% de cobertura:** Todas RNs do RF.yaml documentadas em UCs
2. ✅ **Nomenclatura oficial:** Zero RNs fora do padrão `RN-RFXXX-NNN`
3. ✅ **Catálogo limpo:** Zero códigos híbridos (`RF-CRUD`, `RF-VAL`, etc.)
4. ✅ **Funcionalidades críticas documentadas:** Jobs, workflows, integrações
5. ✅ **Validação automática aprovada:** Exit code 0
6. ✅ **Rastreabilidade completa:** Git history + relatório detalhado

**Validade:** Este RF está PRONTO para execução de backend após este contrato.

---

**Versão do Contrato:** 1.0
**Última Atualização:** 2025-12-31
**Autor:** Claude Sonnet 4.5 (baseado em auditoria de 23 RFs, 291 RNs)
**Aprovação:** Pendente

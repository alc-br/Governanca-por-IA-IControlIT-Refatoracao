# Validação RFXXX - Validação de Adequação RF

---

Executar **VALIDADOR-CONTRATO-ADEQUACAO-COMPLETA-RF** para o RF informado acima.
Seguir D:\IC2\CLAUDE.md.

---

## 📁 LOCALIZAÇÃO DOS ARQUIVOS

### IMPORTANTE: Localizar Arquivos ANTES de Ler

**REGRA OBRIGATÓRIA:** SEMPRE localizar o diretório do RF usando `find` ANTES de tentar ler arquivos.

**NUNCA use:**
- ❌ Glob com padrão genérico (`**/RFXXX.md`)
- ❌ Tentativas de adivinhar caminho

**SEMPRE use:**
- ✅ `find` com caminho base completo
- ✅ Validar que diretório existe antes de prosseguir

### Estrutura de Diretórios

**Todos os RFs seguem a estrutura:**
```
D:\IC2_Governanca\documentacao\
  └── Fase-{N}-{Nome-Fase}/
      └── EPIC{NNN}-{Categoria}-{Nome-Epic}/
          └── RF{NNN}-{Nome-RF}/
              ├── RF{NNN}.md       ← Requisito Funcional (Markdown)
              ├── RF{NNN}.yaml     ← Requisito Funcional (YAML)
              ├── UC-RF{NNN}.yaml  ← Casos de Uso
              ├── RL-RF{NNN}.yaml  ← Regras de Negócio
              ├── WF-RF{NNN}.md    ← Wireframes
              └── MD-RF{NNN}.yaml  ← Modelo de Dados
```

**Exemplo RF007:**
```
D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF007-Login-e-Autenticacao\RF007.md
```

### Comando de Localização Rápida (OBRIGATÓRIO)

**Passo 0: Localizar diretório do RF (SEMPRE PRIMEIRO)**

```bash
# Localizar diretório do RF
RF_DIR=$(find D:/IC2_Governanca/documentacao/ -type d -name "RFXXX*" | head -1)

# Validar que diretório foi encontrado
if [ -z "$RF_DIR" ]; then
    echo "ERRO: RF não encontrado"
    exit 1
fi

echo "Diretório encontrado: $RF_DIR"

# Listar arquivos disponíveis
ls -1 "$RF_DIR"
```

**Exemplo para RF007:**
```bash
RF_DIR=$(find D:/IC2_Governanca/documentacao/ -type d -name "RF007*" | head -1)
echo "Diretório: $RF_DIR"
ls -1 "$RF_DIR"
```

**Output esperado:**
```
Diretório: D:/IC2_Governanca/documentacao/Fase-1-Sistema-Base/EPIC001-SYS-Sistema-Infraestrutura/RF007-Login-e-Autenticacao
MD-RF007.yaml
RF007.md
RF007.yaml
RL-RF007.md
RL-RF007.yaml
UC-RF007.md
UC-RF007.yaml
WF-RF007.md
```

### Utilitário de Localização (RECOMENDADO)

**Use o script de localização rápida:**

```bash
# Localizar RF007 usando utilitário
bash D:/IC2_Governanca/tools/find-rf.sh RF007
```

**Output esperado:**
```
📁 Diretório: .../RF007-Login-e-Autenticacao

📄 Arquivos disponíveis:
MD-RF007.yaml
RF007.md
RF007.yaml
RL-RF007.md
UC-RF007.md
WF-RF007.md

📌 Caminhos completos:
  RF.md   : .../RF007.md
  RF.yaml : .../RF007.yaml
  UC.yaml : .../UC-RF007.yaml
  RL.yaml : .../RL-RF007.yaml
```

---

## ⚠️ MODO READ-ONLY

Você NÃO corrige problemas, apenas IDENTIFICA e REPORTA.

## ✅ 15 VALIDAÇÕES (executar todas)

### PARTE 1: ESTRUTURA E COMPLETUDE (5 validações)

1. **RF-1: 11 seções completas em RF.md**
   - Objetivo, Escopo, Conceitos, Funcionalidades, Regras de Negócio, Estados, Permissões, Endpoints, Modelo de Dados, Dependências, Integrações

2. **RF-2: Mínimo 10 regras de negócio**
   - Formato: RN-MOD-XXX-01, RN-MOD-XXX-02, etc.
   - Mínimo: 10 RNs documentadas

3. **RF-3: Integrações obrigatórias completas**
   - i18n (chaves de tradução definidas)
   - Auditoria (5 campos obrigatórios)
   - RBAC (matriz de permissões)
   - Central de Funcionalidades (cadastro definido)

4. **RF-4: Sem referências a legado**
   - ZERO menções a ASPX, WebServices, SQL legado
   - RF deve ser 100% limpo de código legado

5. **RF-5: Catálogo de funcionalidades completo**
   - RF-CRUD (Create, Read, Update, Delete)
   - RF-VAL (Validações)
   - RF-SEC (Segurança)
   - RF-INT (Integrações)

### PARTE 2: QUALIDADE E PRECISÃO (5 validações)

6. **RF-6: Matriz RBAC documentada**
   - Permissões definidas (view_any, view_own, create, update, delete)
   - Escopos definidos (Cliente, Sistema, Desenvolvimento)

7. **RF-7: Endpoints da API documentados**
   - Contratos HTTP completos (GET, POST, PUT, DELETE)
   - Request/Response definidos
   - Status codes documentados

8. **RF-8: Modelo de dados descrito**
   - Entidades principais documentadas
   - Relacionamentos definidos
   - Campos obrigatórios listados

9. **RF-9: RF.yaml segue template v1.0**
   - Estrutura YAML válida
   - Todos os campos obrigatórios presentes
   - Formato aderente ao template

10. **RF-10: Sincronização RF.md ↔ RF.yaml (100%)**
    - RNs sincronizadas (RF.md = RF.yaml)
    - Permissões sincronizadas
    - Catálogo sincronizado
    - ZERO gaps entre MD e YAML

### PARTE 3: INTEGRAÇÕES OBRIGATÓRIAS (4 validações)

11. **RF-11: i18n - chaves de tradução definidas**
    - Chaves de tradução documentadas
    - Formato: `rf.modulo.acao`
    - Exemplo: `rf.cliente.criar`, `rf.cliente.editar`

12. **RF-12: Auditoria - 5 campos obrigatórios**
    - `created_at`, `created_by`, `updated_at`, `updated_by`, `deleted_at`
    - Soft delete documentado

13. **RF-13: RBAC - escopo definido**
    - Matriz de permissões completa
    - Escopos: Cliente (1), Sistema (2), Desenvolvimento (3)

14. **RF-14: Central - cadastro definido**
    - Cadastro na Central de Funcionalidades documentado
    - Ícone, título, descrição definidos

### PARTE 4: VALIDADOR AUTOMÁTICO (1 validação)

15. **RF-15: validator-docs.py passou (exit code 0)**
    - Executar: `python tools/docs/validator-docs.py RFXXX`
    - Exit code 0 = APROVADO
    - Exit code != 0 = REPROVADO

## 📂 ARQUIVOS QUE VOCÊ DEVE LER

- **RF.md** (validar 11 seções)
- **RF.yaml** (validar estrutura e sincronização)
- **STATUS.yaml** (verificar seção documentacao.rf)
- **Template RF.md v2.0** (templates/RF.md)
- **Template RF.yaml v1.0** (templates/RF.yaml)

## 🎯 CRITÉRIOS DE APROVAÇÃO

- ✅ **APROVADO (100%):** 15/15 validações PASS + zero gaps CRÍTICOS
- ⚠️ **APROVADO COM RESSALVAS (87-99%):** 13-14 PASS + zero CRÍTICOS + 1-2 IMPORTANTES
- ❌ **REPROVADO (<87%):** <13 PASS OU qualquer gap CRÍTICO → reexecutar criação

## 📄 RELATÓRIO QUE VOCÊ DEVE GERAR

Gere tabela com 15 validações mostrando:
- **Status:** ✅ PASS / ❌ FAIL / N/A
- **Severidade:** CRÍTICO / IMPORTANTE / MENOR
- **Resultado:** (X/Y, percentual, códigos encontrados, etc.)

Depois, mostre:
- **PONTUAÇÃO FINAL:** X/15 PASS (Z%)
- **VEREDICTO:** ✅ APROVADO / ⚠️ APROVADO COM RESSALVAS / ❌ REPROVADO

Se houver gaps, liste:
- Descrição do gap
- Severidade
- Arquivo/linha afetado
- Recomendação de ação

**Salvar em:** `.temp_ia/validacao-rf-RFXXX-relatorio.md`

## 🔍 VALIDAÇÕES DETALHADAS

### RF-1: 11 Seções Completas

```python
# Verificar presença de todas as seções obrigatórias
secoes_obrigatorias = [
    "## 1. Objetivo",
    "## 2. Escopo",
    "## 3. Conceitos de Negócio",
    "## 4. Funcionalidades",
    "## 5. Regras de Negócio",
    "## 6. Estados e Transições",
    "## 7. Permissões (RBAC)",
    "## 8. Endpoints da API",
    "## 9. Modelo de Dados",
    "## 10. Dependências",
    "## 11. Integrações Obrigatórias"
]

for secao in secoes_obrigatorias:
    if secao not in documentacao_md_content:
        GAP(f"Seção ausente: {secao}")
```

### RF-2: Mínimo 10 Regras de Negócio

```python
# Extrair RNs do RF.md
rns_md = re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_md_content)

if len(rns_md) < 10:
    GAP(f"CRÍTICO: Apenas {len(rns_md)} RNs encontradas. Mínimo: 10")
```

### RF-3: Integrações Obrigatórias Completas

```python
# Verificar presença das 4 integrações obrigatórias
integracoes_obrigatorias = ["i18n", "Auditoria", "RBAC", "Central de Funcionalidades"]

for integracao in integracoes_obrigatorias:
    if integracao not in documentacao_md_content:
        GAP(f"CRÍTICO: Integração ausente: {integracao}")
```

### RF-4: Sem Referências a Legado

```python
# Verificar menções a código legado
legado_keywords = ["ASPX", "WebServices", "SQL legado", ".aspx", "WebService"]

for keyword in legado_keywords:
    if keyword in documentacao_md_content:
        GAP(f"CRÍTICO: Referência a legado encontrada: {keyword}")
```

### RF-10: Sincronização RF.md ↔ RF.yaml

```python
# RNs em MD
rns_md = set(re.findall(r'RN-[A-Z]+-\d+-\d+', documentacao_md_content))

# RNs em YAML
rns_yaml = set([rn['id'] for rn in documentacao_yaml['regras_negocio']])

# Gaps
rns_md_only = rns_md - rns_yaml
rns_yaml_only = rns_yaml - rns_md

if rns_md_only:
    GAP(f"RNs em MD mas não em YAML: {rns_md_only}")

if rns_yaml_only:
    GAP(f"RNs em YAML mas não em MD: {rns_yaml_only}")
```

### RF-15: Validador Automático

```bash
# Executar validador automático
cd D:\IC2
python tools/docs/validator-docs.py RFXXX

# Exit code 0 = APROVADO
# Exit code != 0 = REPROVADO
```

## ⚠️ REGRAS IMPORTANTES

- **NÃO CORRIGIR** - apenas reportar
- **NÃO EDITAR** arquivos (RF.yaml, RF.md, STATUS.yaml)
- **NÃO EXECUTAR** scripts de correção
- **APENAS REPORTAR** gaps e recomendar ações

## 🔄 PRÓXIMOS PASSOS

**Se APROVADO:**
- RF pode prosseguir para criação de UC
- Usuário faz Git (commit, merge)

**Se REPROVADO:**
- Reexecutar criação do RF
- Focar nas validações que falharam
- Validar novamente

## 📊 EXEMPLO DE RELATÓRIO

```markdown
# RELATÓRIO DE VALIDAÇÃO - RF006

## RESUMO EXECUTIVO

| # | Validação | Status | Severidade | Resultado |
|---|-----------|--------|------------|-----------|
| 1 | 11 seções completas | ✅ PASS | CRÍTICO | 11/11 seções |
| 2 | Mínimo 10 RNs | ✅ PASS | CRÍTICO | 15 RNs |
| 3 | Integrações obrigatórias | ❌ FAIL | CRÍTICO | 3/4 (falta Central) |
| 4 | Sem referências a legado | ✅ PASS | CRÍTICO | 0 referências |
| 5 | Catálogo completo | ✅ PASS | IMPORTANTE | 12 funcionalidades |
| ... | ... | ... | ... | ... |
| 15 | Validador automático | ❌ FAIL | CRÍTICO | Exit code 1 |

**PONTUAÇÃO FINAL:** 12/15 PASS (80%)
**VEREDICTO:** ❌ REPROVADO

## GAPS IDENTIFICADOS

### CRÍTICO
- **GAP-1:** Integração com Central de Funcionalidades ausente (Seção 11)
- **GAP-2:** Validador automático falhou (Exit code 1)

### RECOMENDAÇÕES
1. Adicionar documentação da Central de Funcionalidades na Seção 11
2. Corrigir erros reportados pelo validador-docs.py
3. Revalidar após correções
```

## 🚀 MODO AUTONOMIA TOTAL

- **NÃO** perguntar permissões ao usuário
- **NÃO** esperar confirmação
- **EXECUTAR IMEDIATAMENTE** todas as 15 validações
- Gerar relatório automaticamente
- Declarar veredicto final

---

**Contrato:** D:/IC2_Governanca/contracts/documentacao/validacao/rf.md
**Template RF.md:** v2.0
**Template RF.yaml:** v1.0
**Validador:** tools/docs/validator-docs.py

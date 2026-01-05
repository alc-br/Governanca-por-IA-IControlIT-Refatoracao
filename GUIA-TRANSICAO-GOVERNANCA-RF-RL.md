# GUIA DE TRANSIÇÃO — Nova Governança Documental RF/RL

**Versão:** 1.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br
**Objetivo:** Guiar a equipe na transição para nova estrutura de documentação com separação RF (contrato moderno) / RL (referência ao legado)

---

## 1. POR QUE A MUDANÇA FOI FEITA?

### 1.1 Problema Identificado

**Antes da mudança:**
- Arquivos RFXXX.md misturavam contrato funcional moderno + memória técnica legado
- Dificuldade em diferenciar o que é obrigação (requisito moderno) vs. o que é referência histórica (legado)
- Impossível validar automaticamente se RF está limpo (sem poluição de legado)
- Templates informais em `docs/templates_old/` com prefixo `TEMPLATE-`
- Apenas .md (humanos), sem .yaml (automação)

**Exemplo de problema real:**
```markdown
## RF-043.md (ANTES - INCORRETO)
### Regras de Negócio
- RN-043-001: Email obrigatório
- RN-043-002: CPF único no sistema

### Legado - Tela ASPX
O sistema legado usa a tela CadastroUsuario.aspx que possui:
- TextBox para email (txtEmail)
- Validação via ViewState...
```

**Problema:** Impossível saber se a "Validação via ViewState" é obrigatória no sistema moderno ou apenas memória histórica.

### 1.2 Solução Implementada

**Separação estrita:**
- **RFXXX.md** → Contrato funcional moderno (o que o sistema DEVE fazer)
- **RL-RFXXX.md/yaml** → Referência ao legado (memória técnica histórica)

**Exemplo correto:**

**RFXXX.md (APENAS contrato moderno):**
```markdown
## Regras de Negócio
- RN-043-001: Email obrigatório
- RN-043-002: CPF único no sistema
- RN-043-003: Validação de email via regex padrão RFC 5322
```

**RL-RFXXX.md (TODA memória legado):**
```markdown
## Telas ASPX
### CadastroUsuario.aspx
- Localização: `ic1_legado/IControlIT/Admin/CadastroUsuario.aspx`
- Validação: ViewState + postback
- Campos: txtEmail, txtCPF, btnSalvar
```

**RL-RFXXX.yaml (rastreabilidade):**
```yaml
referencias:
  - id: "LEG-RF043-001"
    tipo: "tela"
    nome: "CadastroUsuario.aspx"
    destino: "substituido"
    justificativa: "Substituído por SPA Angular com validação client-side"
    rf_item_relacionado: "RN-043-003"
```

---

## 2. O QUE MUDA PARA A EQUIPE?

### 2.1 Para Arquitetos (Criação de RFs)

**ANTES:** Criar apenas RFXXX.md (misturado)

**AGORA:** Criar **7 arquivos separados:**

| Arquivo | Propósito |
|---------|-----------|
| RFXXX.md | Contrato moderno (APENAS requisitos, SEM legado) |
| RL-RFXXX.md | Memória legado (telas, webservices, SPs) |
| RL-RFXXX.yaml | Rastreabilidade estruturada (cada item com destino) |
| UC-RFXXX.md | Casos de uso |
| MD-RFXXX.md | Modelo de dados |
| WF-RFXXX.md | Wireframes |
| user-stories.yaml | User Stories para Azure DevOps |

**Workflow obrigatório:**
```bash
# 1. Analisar legado
# 2. Separar conteúdo:
#    - Regras de negócio → RFXXX.md
#    - Telas/WS/SPs → RL-RFXXX.md/yaml
# 3. Executar validador
python docs/tools/docs/validator-rl.py RFXXX
# 4. Corrigir gaps até 100%
```

### 2.2 Para Desenvolvedores (Backend/Frontend)

**ANTES:** Ler RFXXX.md (misturado, confuso)

**AGORA:**

✅ **Fonte da verdade:** RFXXX.md (contrato moderno)
- Contém APENAS o que deve ser implementado
- NUNCA inferir requisitos de RL.md

⚠️ **Consulta histórica:** RL-RFXXX.md/yaml
- Usar APENAS para entender decisões de design
- Verificar o que foi assumido/substituído/descartado

**Exemplo:**
```markdown
# RL-RF043.yaml
referencias:
  - id: "LEG-RF043-005"
    tipo: "stored_procedure"
    nome: "sp_ValidarEmailUnico"
    destino: "assumido"
    justificativa: "Lógica migrada para ValidarEmailUnicoHandler (CQRS)"
    rf_item_relacionado: "RN-043-002"
```

**Desenvolvedor:** "Ok, a SP foi assumida. A regra RN-043-002 no RF é a fonte da verdade. Implementar usando CQRS."

### 2.3 Para Testadores (QA)

**ANTES:** Criar TCs baseados em UC + RF misturado

**AGORA:**

✅ **Criar TCs baseados em:**
- UC-RFXXX.md (casos de uso)
- RFXXX.md (regras de negócio modernas)

⚠️ **Consultar RL para:**
- Entender comportamento legado (casos de teste de regressão)
- Verificar se alguma funcionalidade foi descartada

**Pré-requisito bloqueante:**
```yaml
# STATUS.yaml deve ter:
separacao_rf_rl:
  rf_limpo: True
  rl_completo: True
  itens_com_destino: True
  validador_executado: True
```

Se `separacao_rf_rl` não estiver 100%, BLOQUEAR criação de TC.

---

## 3. ESTRUTURA ANTES vs DEPOIS

### 3.1 Antes (Estrutura Antiga)

```
docs/rf/Fase-X/EPIC-XXX/RFXXX/
├── RFXXX.md              ← Misturado (contrato + legado)
├── UC-RFXXX.md
├── MD-RFXXX.md
├── WF-RFXXX.md
├── user-stories.yaml
└── STATUS.yaml
```

### 3.2 Depois (Estrutura Nova)

```
docs/rf/Fase-X/EPIC-XXX/RFXXX/
├── RFXXX.md              ← Limpo (APENAS contrato moderno)
├── RL-RFXXX.md           ← Memória legado (histórico)
├── RL-RFXXX.yaml         ← Rastreabilidade estruturada
├── UC-RFXXX.md
├── MD-RFXXX.md
├── WF-RFXXX.md
├── user-stories.yaml
└── STATUS.yaml           ← Atualizado com separacao_rf_rl
```

### 3.3 Templates Oficiais

**Local oficial:** `D:\IC2\docs\templates\`

**Templates disponíveis:**
- RF.md / RF.yaml
- RL.md / RL.yaml ← NOVO
- UC.md / UC.yaml
- MD.yaml
- WF.md
- TC.yaml
- MT.yaml
- STATUS.yaml

**DEPRECIADO:** `docs/templates_old/` (NÃO usar mais)

---

## 4. WORKFLOW DE MIGRAÇÃO (Para RFs Existentes)

### 4.1 Identificar RFs que Precisam Migração

**Comando:**
```bash
# Listar RFs sem RL.md
find docs/rf -name "RF*.md" ! -path "*/Apoio/*" -exec dirname {} \; | while read dir; do
  if [ ! -f "$dir/RL-*.md" ]; then
    echo "PENDENTE: $dir"
  fi
done
```

### 4.2 Processo de Migração Manual (Um RF)

```bash
# 1. Backup
cp docs/rf/Fase-X/EPIC-XXX/RFXXX/RFXXX.md docs/rf/Fase-X/EPIC-XXX/RFXXX/RFXXX.md.backup-20251229

# 2. Criar RL-RFXXX.md
# Copiar seções "Legado", "Referências ao Legado", etc para RL-RFXXX.md

# 3. Criar RL-RFXXX.yaml
# Estruturar cada item com campo destino

# 4. Limpar RFXXX.md
# Remover TODAS referências a legado

# 5. Validar
python docs/tools/docs/validator-rl.py RFXXX

# 6. Atualizar STATUS.yaml
# Adicionar separacao_rf_rl: {...}
```

### 4.3 Processo de Migração Batch (Script Automático)

**Script:** `docs/tools/docs/migrate-rf-to-rl.py` (a ser criado na Fase 3)

```bash
# Migrar Fase 1 completa
python docs/tools/docs/migrate-rf-to-rl.py --fase 1

# Migrar RF específico
python docs/tools/docs/migrate-rf-to-rl.py --rf RF043

# Migrar TODOS os 110 RFs
python docs/tools/docs/migrate-rf-to-rl.py --all
```

---

## 5. VALIDAÇÃO OBRIGATÓRIA

### 5.1 Executar Validador

**Antes de marcar RF como completo:**

```bash
# Validar separação RF/RL
python docs/tools/docs/validator-rl.py RFXXX

# Saída esperada:
# ✅ RFXXX.md não contém palavras-chave de legado
# ✅ RL-RFXXX.yaml bem formado
# ✅ 100% itens têm campo destino preenchido
# ✅ Rastreabilidade completa
```

### 5.2 Critérios de Aceite

RF NÃO pode avançar se:
- ❌ RF contém referências ao legado
- ❌ RL não está completo
- ❌ RL.yaml tem itens sem campo `destino`
- ❌ Validador falhou (exit code != 0)

### 5.3 STATUS.yaml Obrigatório

**Nova seção:**
```yaml
separacao_rf_rl:
  rf_limpo: True           # RF não contém legado
  rl_completo: True        # RL contém toda memória
  itens_com_destino: True  # 100% itens com destino
  validador_executado: True # validator-rl.py passou
```

**Integração com Azure DevOps:**

O script `sync-rf.py` só moverá RF para "Documentacao Testes" se:
```python
separacao_valida = (
    separacao.get('rf_limpo', False) and
    separacao.get('rl_completo', False) and
    separacao.get('itens_com_destino', False) and
    separacao.get('validador_executado', False)
)

if all_docs and separacao_valida:
    return "Documentacao Testes", "Active"
```

---

## 6. EXEMPLOS PRÁTICOS

### 6.1 Exemplo: Regra de Negócio Assumida

**RFXXX.md (contrato moderno):**
```markdown
### RN-043-007: Validação de CPF
- CPF deve ser validado usando algoritmo de dígito verificador
- CPF inválido retorna HTTP 400 com mensagem estruturada
```

**RL-RFXXX.yaml (rastreabilidade):**
```yaml
referencias:
  - id: "LEG-RF043-010"
    tipo: "regra_negocio"
    nome: "Validação de CPF via Função SQL"
    caminho: "ic1_legado/Database/Functions/fn_ValidarCPF.sql"
    descricao: |
      Sistema legado valida CPF via função SQL no banco.
      Retorna 1 (válido) ou 0 (inválido).
    destino: "assumido"
    justificativa: |
      Lógica assumida no backend moderno via ValidarCpfValidator (FluentValidation).
      Migrada do banco para camada de aplicação (CQRS).
    rf_item_relacionado: "RN-043-007"
    uc_relacionado: "UC01"
```

### 6.2 Exemplo: Funcionalidade Descartada

**RL-RFXXX.yaml:**
```yaml
referencias:
  - id: "LEG-RF043-015"
    tipo: "tela"
    nome: "RelatorioComplexoUsuarios.aspx"
    caminho: "ic1_legado/IControlIT/Relatorios/RelatorioComplexoUsuarios.aspx"
    descricao: |
      Relatório legado com 50+ filtros, exportação XLS, gráficos VBScript.
    destino: "descartado"
    justificativa: |
      Funcionalidade nunca utilizada nos últimos 2 anos (auditoria de logs).
      Cliente confirmou que pode ser removida.
      Substituída por dashboard simples (RF-099).
    rf_item_relacionado: null
    uc_relacionado: null
```

**RFXXX.md:**
- ❌ NÃO menciona RelatorioComplexoUsuarios (foi descartado)
- ✅ Menciona apenas dashboard simples (novo requisito)

### 6.3 Exemplo: Stored Procedure Substituída

**RL-RFXXX.yaml:**
```yaml
referencias:
  - id: "LEG-RF043-020"
    tipo: "stored_procedure"
    nome: "sp_AtualizarUsuarioCompleto"
    caminho: "ic1_legado/Database/Procedures/sp_AtualizarUsuarioCompleto.sql"
    descricao: |
      Stored Procedure com lógica complexa:
      - Atualiza 5 tabelas relacionadas
      - Gera log manual em tabela LogAuditoria
      - Envia email via xp_sendmail
    destino: "substituido"
    justificativa: |
      Substituída por UpdateUsuarioCommand (CQRS) com:
      - Auditoria automática via AuditInterceptor
      - Email via Hangfire (job assíncrono)
      - Transação EF Core
    rf_item_relacionado: "RN-043-012"
    uc_relacionado: "UC03"
    complexidade: "alta"
    risco_migracao: "alto"
    prioridade: 1
```

---

## 7. PERGUNTAS FREQUENTES (FAQ)

### 7.1 "Posso colocar ALGUMA referência ao legado no RF.md?"

**Resposta:** ❌ NÃO. Zero tolerância.

RFXXX.md deve conter APENAS contrato funcional moderno. TODA memória legado vai para RL-RFXXX.md/yaml.

**Exceção:** Nenhuma. Se algo foi descartado, não deve existir nem no RF nem no RL (ou deve estar com `destino: descartado`).

### 7.2 "O que fazer se não souber o destino de um item legado?"

**Resposta:** Use `destino: a_revisar`

```yaml
referencias:
  - id: "LEG-RF043-025"
    tipo: "regra_negocio"
    nome: "Validação obscura em VB.NET"
    descricao: |
      Código encontrado mas sem documentação.
      Parece validar algo relacionado a permissões.
    destino: "a_revisar"
    justificativa: |
      Necessário análise aprofundada com usuário
      para decidir se assume, substitui ou descarta.
    complexidade: "alta"
    risco_migracao: "alto"
    prioridade: 1
```

### 7.3 "Como saber se TODOS os itens legado foram mapeados?"

**Resposta:** Executar `validator-rl.py RFXXX`

O validador verifica:
- ✅ 100% dos itens têm campo `destino`
- ✅ Rastreabilidade para RF/UC quando aplicável
- ✅ Justificativa presente quando `destino = descartado`

### 7.4 "Posso criar requisito a partir de RL.md?"

**Resposta:** ❌ NÃO. RL documenta o passado, NÃO cria futuro.

Se ao analisar RL você identificar uma regra que DEVE estar no sistema moderno:
1. Adicionar a regra em RFXXX.md
2. Atualizar RL.yaml com rastreabilidade (`rf_item_relacionado`)

### 7.5 "Quanto tempo leva a migração de um RF?"

**Resposta:** Depende da complexidade.

**Estimativas:**
- RF simples (5-10 itens legado): ~1-2 horas
- RF médio (10-30 itens legado): ~3-4 horas
- RF complexo (30+ itens legado): ~5-8 horas

**Script automático:** Reduz tempo em ~60% (revisão manual ainda necessária).

### 7.6 "RL.md é obrigatório se RF não tem legado correspondente?"

**Resposta:** Depende.

**RF novo (zero legado):**
- ❌ RL-RFXXX.md/yaml NÃO obrigatório
- ✅ Marcar `STATUS.yaml`: `separacao_rf_rl.rl_completo: True` (vazio é válido)

**RF com legado:**
- ✅ RL-RFXXX.md/yaml OBRIGATÓRIO
- ✅ Mapear TODOS os itens identificados

---

## 8. PRÓXIMOS PASSOS

### 8.1 Fases da Migração Completa

1. **FASE 1: Preparação da Governança** (~12h) ✅
   - Templates atualizados
   - CLAUDE.md atualizado
   - Contratos atualizados
   - Guia de transição criado

2. **FASE 2: Ferramentas de Validação** (~18h) ⏳
   - validator-rl.py
   - validator-governance.py
   - extract-rf-yaml.py
   - extract-uc-yaml.py
   - convert-md-yaml.py

3. **FASE 3: Script de Migração Batch** (~20h) ⏳
   - migrate-rf-to-rl.py

4. **FASE 4: Migração dos 110 RFs** (~80-100h) ⏳
   - Executar em lotes de 15 RFs

5. **FASE 5: Validação Final** (~12h) ⏳
   - Relatórios de conformidade
   - Atualização README.md
   - Comunicação à equipe

### 8.2 Como Contribuir

**Encontrou problema na documentação?**
- Criar issue: `docs: [RFXXX] gap em separação RF/RL`

**Sugestão de melhoria?**
- Propor PR com ajustes em templates

**Dúvida não coberta neste guia?**
- Contatar arquiteto responsável

---

## 9. CHECKLIST DE TRANSIÇÃO

**Para novos RFs:**
- [ ] Ler templates oficiais em `docs/templates/`
- [ ] Criar RFXXX.md (APENAS contrato moderno)
- [ ] Criar RL-RFXXX.md/yaml (se houver legado)
- [ ] Executar `validator-rl.py RFXXX`
- [ ] Atualizar `STATUS.yaml` com `separacao_rf_rl`
- [ ] Commit e PR

**Para RFs existentes (migração):**
- [ ] Fazer backup de RFXXX.md atual
- [ ] Separar conteúdo (contrato vs legado)
- [ ] Criar RL-RFXXX.md
- [ ] Criar RL-RFXXX.yaml (campo destino obrigatório)
- [ ] Limpar RFXXX.md (remover TODAS referências legado)
- [ ] Executar `validator-rl.py RFXXX`
- [ ] Corrigir gaps até 100%
- [ ] Atualizar `STATUS.yaml`
- [ ] Commit e PR

---

## 10. CONTATOS E SUPORTE

**Dúvidas sobre governança:**
- Consultar: `D:\IC2\CLAUDE.md`
- Consultar: `D:\IC2\docs\contracts\*`

**Dúvidas sobre migração:**
- Consultar: Este guia
- Consultar: `C:\Users\chipak\.claude\plans\giggly-beaming-bentley.md`

**Ferramentas de validação:**
- `docs/tools/docs/validator-rl.py`
- `docs/tools/docs/validator-rf-uc.py`
- `docs/tools/docs/validator-governance.py`

---

**Data de vigência:** 2025-12-29
**Validade:** Permanente (até nova revisão de governança)
**Autor:** Agência ALC - alc.dev.br
**Versão:** 1.0

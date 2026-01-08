# CONTRATO DE MIGRAÇÃO RF v1.0 → v2.0 (SEPARAÇÃO RF/RL)

**Versão:** 2.0
**Data:** 2025-12-30
**Status:** Ativo

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente de Migração de Documentação |
| **Escopo** | Migração RF v1.0 → v2.0 com separação obrigatória RF/RL |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Execute o contrato CONTRATO-RF-PARA-RL para RFXXX"**

Exemplo:
```
Execute o contrato CONTRATO-RF-PARA-RL para RF006.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo da Migração

Adequar documentação de RFs existentes (v1.0) para o padrão de **Governança v2.0**, que exige:

- **Separação estrita RF/RL**: RF documenta o sistema moderno, RL documenta a memória do legado
- **Sincronização MD↔YAML**: Pares de arquivos devem estar 100% sincronizados
- **Destinos obrigatórios**: Todo item legado precisa ter destino definido (ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR)
- **Linguagem natural**: Conversão de código VB.NET/SQL para regras de negócio em português

**Resultado esperado**: 4 arquivos prontos para criação de UCs:
1. `RFXXX.md` (v2.0 - contrato funcional moderno)
2. `RFXXX.yaml` (estruturado - sincronizado com RF.md)
3. `RL-RFXXX.md` (referência ao legado - memória técnica)
4. `RL-RFXXX.yaml` (estruturado - 100% com destinos)

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |
| **LEGACY_PATH** | `D:\IC2\ic1_legado\IControlIT\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\RL-RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\RL-RFXXX.yaml
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| RF existe | `RFXXX.md` já existe na pasta do RF | Sim |
| Templates acessíveis | `D:\IC2\docs\templates\*.md` disponíveis | Sim |
| Legado acessível | `D:\IC2\ic1_legado\` disponível para consulta | Sim |
| STATUS.yaml existe | Arquivo de status do RF já criado | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Migração

### Fase 1: Migração RFXXX.md (Contrato Funcional Moderno)

#### 6.1 Backup Obrigatório

```bash
# Criar backup com timestamp
cp RFXXX.md RFXXX.md.backup-$(date +%Y%m%d)
```

#### 6.2 Criar RFXXX.md v2.0

**Baseado em:** `D:\IC2\docs\templates\RF.md`

**Estrutura obrigatória (11 seções):**

1. **Seção 1: Visão Geral**
   - Resumo executivo do requisito
   - Objetivo principal
   - Escopo do RF (o que está incluído/excluído)

2. **Seção 2: Funcionalidades**
   - Lista de funcionalidades (mínimo 5)
   - Descrição de cada funcionalidade
   - Prioridade (CRÍTICA, ALTA, MÉDIA, BAIXA)

3. **Seção 3: Regras de Negócio**
   - Mínimo 10 regras de negócio (RN-RFXXX-NNN)
   - Formato: `RN-RFXXX-001: [Descrição em linguagem natural]`
   - Sem código VB.NET ou SQL
   - Sem referências ao legado (telas ASPX, webservices, stored procedures)

4. **Seção 4: Integrações Obrigatórias**
   - i18n (Transloco - pt-BR/en/es)
   - Auditoria (campos Created, CreatedBy, LastModified, LastModifiedBy)
   - RBAC (permissões baseadas em roles)
   - Central de Funcionalidades (registro obrigatório)

5. **Seção 5: Permissões RBAC**
   - Matriz de permissões (Funcionalidade × Role)
   - Permission codes (ex: `CAD.EMPRESAS.CREATE`)
   - Roles autorizadas para cada permissão

6. **Seção 6: API Endpoints**
   - Lista de endpoints REST (GET, POST, PUT, DELETE)
   - Rota de cada endpoint
   - Autenticação/autorização obrigatória
   - Request/Response DTOs

7. **Seção 7: Modelo de Dados**
   - Referência ao arquivo `MD-RFXXX.md`
   - Principais entidades envolvidas
   - Relacionamentos críticos

8. **Seção 8: Dependências**
   - RFs dependentes (upstream)
   - RFs que dependem deste (downstream)
   - Dependências de bibliotecas externas

9. **Seção 9: KPIs e Métricas**
   - Indicadores de performance
   - Metas esperadas
   - Logs obrigatórios

10. **Seção 10: Alertas Críticos**
    - Eventos que geram alertas
    - Thresholds (limites de disparo)
    - Canais de notificação

11. **Seção 11: Central de Funcionalidades**
    - Código da funcionalidade
    - Módulo (Admin, Configurações, etc.)
    - i18n keys para menu/título

**PROIBIDO em RFXXX.md v2.0:**
- ❌ Referências a telas ASPX do legado
- ❌ Referências a webservices VB.NET
- ❌ Referências a stored procedures SQL
- ❌ Código legado copiado
- ❌ Screenshots do sistema antigo
- ❌ Comparações "legado vs moderno"

**OBRIGATÓRIO em RFXXX.md v2.0:**
- ✅ Regras de negócio em linguagem natural
- ✅ Endpoints REST API modernos
- ✅ Integrações obrigatórias (i18n, auditoria, RBAC, Central)
- ✅ Modelo de dados moderno (multi-tenancy, auditoria)
- ✅ Mínimo 10 regras de negócio (RN-RFXXX-NNN)

---

### Fase 2: Migração RFXXX.yaml (Estruturado Sincronizado)

#### 6.3 Criar RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\RF.yaml`

**Estrutura obrigatória:**

```yaml
rf_id: RFXXX
rf_title: "[Título do Requisito Funcional]"
versao_governanca: "2.0"
data_migracao: "2025-12-30"

# ==============================================================================
# REGRAS DE NEGÓCIO
# ==============================================================================

regras_negocio:
  - id: "RN-RFXXX-001"
    titulo: "[Título da Regra]"
    descricao: "[Descrição detalhada em linguagem natural]"
    criticidade: "CRÍTICA"  # CRÍTICA, ALTA, MÉDIA, BAIXA
    implementacao:
      backend: true
      frontend: true
      validacao_api: true
      validacao_ui: true
    validacao:
      tipo: "campo_obrigatorio"  # ou range, formato, unicidade, etc.
      mensagem_erro: "[Mensagem exibida ao usuário]"
      http_code: 400

  # ... Repetir para todas as RNs (mínimo 10)

# ==============================================================================
# PERMISSÕES RBAC
# ==============================================================================

permissoes_rbac:
  - permission_code: "CAD.EMPRESAS.CREATE"
    descricao: "Criar nova empresa"
    roles_autorizadas:
      - "Super Admin"
      - "Admin"
    endpoint: "POST /api/empresas"

  - permission_code: "CAD.EMPRESAS.UPDATE"
    descricao: "Editar empresa existente"
    roles_autorizadas:
      - "Super Admin"
      - "Admin"
    endpoint: "PUT /api/empresas/{id}"

  # ... Repetir para todas as permissões

# ==============================================================================
# API ENDPOINTS
# ==============================================================================

endpoints:
  - method: "GET"
    route: "/api/empresas"
    descricao: "Listar empresas com paginação"
    autenticacao: true
    authorization_policy: "EmpresasRead"
    request_dto: null
    response_dto: "PaginatedListDto<EmpresaDto>"

  - method: "POST"
    route: "/api/empresas"
    descricao: "Criar nova empresa"
    autenticacao: true
    authorization_policy: "EmpresasCreate"
    request_dto: "CreateEmpresaCommand"
    response_dto: "Guid"

  # ... Repetir para todos os endpoints

# ==============================================================================
# KPIs E MÉTRICAS
# ==============================================================================

kpis:
  - nome: "Taxa de Sucesso de Criação"
    descricao: "Percentual de empresas criadas com sucesso"
    meta: ">= 95%"
    log_obrigatorio: true

  - nome: "Tempo Médio de Resposta"
    descricao: "Tempo médio de resposta da API de empresas"
    meta: "<= 200ms"
    log_obrigatorio: true

# ==============================================================================
# ALERTAS CRÍTICOS
# ==============================================================================

alertas:
  - evento: "Falha ao criar empresa"
    threshold: "> 5% em 1 hora"
    severidade: "ALTA"
    canal_notificacao:
      - "email"
      - "slack"

  - evento: "Tentativa de acesso sem permissão"
    threshold: "> 10 em 5 minutos"
    severidade: "CRÍTICA"
    canal_notificacao:
      - "email"
      - "slack"
      - "sms"
```

**Regra CRÍTICA:** RFXXX.yaml DEVE estar 100% sincronizado com RFXXX.md
- Todas as RNs do MD devem estar no YAML
- Todos os endpoints do MD devem estar no YAML
- Todas as permissões do MD devem estar no YAML

---

### Fase 3: Migração RL-RFXXX.md (Referência ao Legado)

#### 6.4 Criar RL-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\RL.md`

**Estrutura obrigatória (7 seções):**

1. **Seção 1: Contexto do Sistema Legado**
   - Stack tecnológica (ASP.NET Web Forms, VB.NET, SQL Server)
   - Arquitetura geral (monolito, multi-database)
   - Problemas arquiteturais identificados

2. **Seção 2: Telas ASPX e Código-Behind**
   - Lista de telas ASPX relacionadas ao RF
   - Caminho completo no legado (`ic1_legado/IControlIT/[modulo]/[tela].aspx`)
   - Funcionalidades principais de cada tela
   - Regras de negócio implícitas no code-behind VB.NET
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

3. **Seção 3: Webservices (.asmx)**
   - Lista de webservices relacionados
   - Caminho completo (`ic1_legado/IControlIT/[modulo]/WebService/[service].asmx`)
   - Métodos públicos expostos
   - Parâmetros e tipos de retorno
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

4. **Seção 4: Stored Procedures**
   - Lista de stored procedures usadas
   - Caminho completo (`ic1_legado/Database/Procedures/[procedure].sql`)
   - Parâmetros de entrada/saída
   - Lógica principal (em linguagem natural, sem copiar SQL)
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

5. **Seção 5: Tabelas Legadas**
   - Lista de tabelas do SQL Server relacionadas
   - Problemas identificados (falta de FK, campos sem validação, etc.)
   - Mapeamento para tabelas modernas (ou NULL se descartado)
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

6. **Seção 6: Regras de Negócio Implícitas**
   - Regras NÃO documentadas encontradas no código
   - Validações hard-coded no VB.NET
   - Business logic escondida em stored procedures
   - **DESTINO**: ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR

7. **Seção 7: Gap Analysis (Legado × Moderno)**
   - Funcionalidades do legado que NÃO serão migradas (justificativa)
   - Funcionalidades novas do sistema moderno (não existiam no legado)
   - Mudanças de comportamento entre legado e moderno
   - Riscos de migração identificados

**PROIBIDO em RL-RFXXX.md:**
- ❌ Copiar código VB.NET diretamente
- ❌ Copiar SQL diretamente
- ❌ Deixar itens sem destino definido

**OBRIGATÓRIO em RL-RFXXX.md:**
- ✅ Extrair regras em LINGUAGEM NATURAL
- ✅ Definir destino para 100% dos itens (ASSUMIDO/SUBSTITUÍDO/DESCARTADO/A_REVISAR)
- ✅ Documentar 3-6 problemas mínimo do legado
- ✅ Mapear bancos legados (se aplicável)

---

### Fase 4: Migração RL-RFXXX.yaml (Estruturado com Destinos)

#### 6.5 Criar RL-RFXXX.yaml

**Baseado em:** `D:\IC2\docs\templates\RL.yaml`

**Estrutura obrigatória:**

```yaml
rf_id: RFXXX
rf_title: "[Título do RF]"
versao_governanca: "2.0"
data_migracao: "2025-12-30"

# ==============================================================================
# ITENS LEGADO RASTREADOS
# ==============================================================================

itens_legado:
  # ------------------------------------------------------------------------------
  # TELAS ASPX
  # ------------------------------------------------------------------------------
  - id: "LEG-RFXXX-001"
    tipo: "tela"
    titulo: "[Nome da Tela ASPX]"
    caminho_legado: "ic1_legado/IControlIT/[modulo]/[tela].aspx"
    descricao: |
      [Funcionalidade principal da tela em linguagem natural]
    regras_implicitas:
      - "[Regra 1 extraída do code-behind VB.NET]"
      - "[Regra 2 extraída do code-behind VB.NET]"
    destino: "SUBSTITUÍDO"  # ASSUMIDO | SUBSTITUÍDO | DESCARTADO | A_REVISAR
    justificativa: "[Por que esta decisão foi tomada]"
    rastreabilidade:
      documentacao_moderno: "RFXXX - Seção 2 (Funcionalidades)"
      uc_moderno: "UC01-RFXXX (Criar)"
    migracao_moderna:
      componente_angular: "empresas-create.component.ts"
      rota_frontend: "/configuracoes/cadastros/empresas/create"

  # ------------------------------------------------------------------------------
  # WEBSERVICES
  # ------------------------------------------------------------------------------
  - id: "LEG-RFXXX-002"
    tipo: "webservice"
    titulo: "[Nome do Webservice]"
    caminho_legado: "ic1_legado/IControlIT/[modulo]/WebService/[service].asmx"
    metodos:
      - nome: "[MetodoPublico1]"
        parametros: "[Tipos e nomes dos parâmetros]"
        retorno: "[Tipo de retorno]"
    descricao: |
      [Lógica do webservice em linguagem natural]
    destino: "SUBSTITUÍDO"
    justificativa: "Substituído por REST API com autenticação JWT"
    rastreabilidade:
      documentacao_moderno: "RFXXX - Seção 6 (API Endpoints)"
      endpoint_moderno: "POST /api/empresas"
    migracao_moderna:
      command_cqrs: "CreateEmpresaCommand"
      handler: "CreateEmpresaCommandHandler"

  # ------------------------------------------------------------------------------
  # STORED PROCEDURES
  # ------------------------------------------------------------------------------
  - id: "LEG-RFXXX-003"
    tipo: "stored_procedure"
    titulo: "[Nome da Stored Procedure]"
    caminho_legado: "ic1_legado/Database/Procedures/[procedure].sql"
    parametros_entrada:
      - "@Param1 VARCHAR(100)"
      - "@Param2 INT"
    parametros_saida:
      - "@Result INT OUTPUT"
    descricao: |
      [Lógica da procedure em linguagem natural - SEM copiar SQL]
    destino: "SUBSTITUÍDO"
    justificativa: "Lógica movida para Application Layer (CQRS Handler)"
    rastreabilidade:
      documentacao_moderno: "RFXXX - Seção 3 (Regras de Negócio)"
      regra_moderna: "RN-RFXXX-005"
    migracao_moderna:
      handler: "CreateEmpresaCommandHandler"
      validacao: "CreateEmpresaCommandValidator (FluentValidation)"

  # ------------------------------------------------------------------------------
  # TABELAS LEGADAS
  # ------------------------------------------------------------------------------
  - id: "LEG-RFXXX-004"
    tipo: "tabela"
    titulo: "[Nome da Tabela SQL Server]"
    schema_legado: "[dbo].[TabelaLegada]"
    problemas_identificados:
      - "Falta Foreign Key para validar relacionamento"
      - "Campos sem NOT NULL em dados obrigatórios"
      - "Sem auditoria (Created, Modified)"
    destino: "SUBSTITUÍDO"
    justificativa: "Tabela redesenhada com multi-tenancy e auditoria"
    rastreabilidade:
      documentacao_moderno: "RFXXX - Seção 7 (Modelo de Dados)"
      md_moderno: "MD-RFXXX.md - Tabela Empresa"
    migracao_moderna:
      tabela_moderna: "Empresa"
      migration_ef_core: "20251230_CreateEmpresaTable.cs"

  # ------------------------------------------------------------------------------
  # REGRAS IMPLÍCITAS
  # ------------------------------------------------------------------------------
  - id: "LEG-RFXXX-005"
    tipo: "regra_negocio"
    titulo: "[Regra Implícita Descoberta no Código]"
    localizacao_codigo: "ic1_legado/IControlIT/[modulo]/[arquivo].vb - Linha XXX"
    descricao: |
      [Regra de negócio extraída do código VB.NET em linguagem natural]
    destino: "ASSUMIDO"
    justificativa: "Regra documentada e mantida no sistema moderno"
    rastreabilidade:
      documentacao_moderno: "RFXXX - Seção 3 (Regras de Negócio)"
      regra_moderna: "RN-RFXXX-008"
    migracao_moderna:
      validador: "CreateEmpresaCommandValidator"
      linha_codigo: "RuleFor(x => x.Cnpj).Must(BeValidCnpj)"

# ==============================================================================
# BANCOS LEGADOS MAPEADOS (se aplicável)
# ==============================================================================

bancos_legados:
  - nome: "IControlIT_Cliente01"
    servidor: "SQL-LEGADO-01"
    tabelas_relacionadas:
      - "Empresa"
      - "Filial"
      - "Usuario"
    destino: "CONSOLIDADO"
    justificativa: "Migrado para banco único com multi-tenancy (Row-Level Security)"
    banco_moderno: "IControlIT.db (SQLite dev) / SQL Server moderno (prod)"

  # ... Repetir para todos os bancos legados (se RF envolve migração multi-database)

# ==============================================================================
# PROBLEMAS LEGADO IDENTIFICADOS
# ==============================================================================

problemas_legado:
  - id: "PROB-RFXXX-001"
    titulo: "[Problema Arquitetural ou Técnico]"
    severidade: "ALTA"  # CRÍTICA, ALTA, MÉDIA, BAIXA
    descricao: |
      [Descrição detalhada do problema no sistema legado]
    impacto: "[Impacto no sistema ou usuários]"
    solucao_moderna: "[Como foi resolvido no sistema moderno]"

  # ... Documentar 3-6 problemas mínimo

# ==============================================================================
# METADADOS
# ==============================================================================

metadados:
  total_itens_legado: 5  # Calculado automaticamente
  itens_assumidos: 1
  itens_substituidos: 3
  itens_descartados: 0
  itens_a_revisar: 1
  cobertura_destinos: "100%"  # Deve ser sempre 100%
```

**Regra CRÍTICA:** RL-RFXXX.yaml DEVE estar 100% sincronizado com RL-RFXXX.md
- Todos os itens do MD devem estar no YAML
- Todos os itens devem ter campo `destino` preenchido
- Metadados devem ser calculados automaticamente

---

### Fase 5: Validação Obrigatória

#### 6.6 Executar Validador de Separação RF/RL

```bash
# Validar que RF não contém legado e RL tem destinos definidos
python D:\IC2_Governanca\tools\docs\validator-rl.py RFXXX
```

**Critérios de validação:**
- ✅ RFXXX.md não contém referências ao legado
- ✅ RL-RFXXX.md contém TODA memória legado
- ✅ 100% dos itens em RL-RFXXX.yaml têm campo `destino`
- ✅ RFXXX.md ↔ RFXXX.yaml sincronizados
- ✅ RL-RFXXX.md ↔ RL-RFXXX.yaml sincronizados

**Se validador falhar (exit code ≠ 0):**
- ❌ PARAR a execução
- ❌ NÃO atualizar STATUS.yaml
- ❌ Corrigir gaps identificados
- ✅ Re-executar validador até passar

---

### Fase 6: Atualização STATUS.yaml

#### 6.7 Atualizar STATUS.yaml (Governança v2.0)

```yaml
documentacao:
  versao: "2.0"
  data_migracao: "2025-12-30"
  documentacao: true                # RFXXX.md v2.0 criado (contrato moderno)
  documentacao_yaml: true           # RFXXX.yaml criado (estruturado)
  rl: true                # RL-RFXXX.md criado (memória legado)
  rl_yaml: true           # RL-RFXXX.yaml criado (rastreabilidade)
  uc: false               # Aguardando criação (próximo contrato)
  uc_yaml: false
  md: false
  wf: false

  arquivos_obrigatorios_presentes: true
  separacao_rf_rl_validada: true

# ==============================================================================
# VALIDAÇÃO SEPARAÇÃO RF/RL (OBRIGATÓRIA v2.0)
# ==============================================================================

separacao_rf_rl:
  documentacao_limpo: true                # RF não contém conteúdo legado
  rl_completo: true             # RL contém TODA memória legado
  itens_com_destino: true       # 100% itens RL têm campo destino
  validador_executado: true     # validator-rl.py passou (exit code 0)

# ==============================================================================
# ESTATÍSTICAS MIGRAÇÃO
# ==============================================================================

estatisticas:
  total_rns: 10                 # Regras de negócio extraídas
  total_endpoints_api: 5        # Endpoints REST documentados
  total_permissoes_rbac: 8      # Permissões RBAC definidas
  total_integracoes_obrigatorias: 4  # i18n, auditoria, RBAC, Central
  itens_legado_rastreados: 15   # Itens em RL-RFXXX.yaml
  bancos_legados_mapeados: 3    # Bancos SQL Server antigos (se aplicável)
  problemas_legado_identificados: 5  # Problemas documentados

  linhas_documentacao:
    documentacao_md: 1200
    documentacao_yaml: 550
    rl_md: 480
    rl_yaml: 420
    total: 2650
```

---

### Fase 7: Commit e Merge

Atenção: essa atividade pode ser feita diretamente no branch dev local e comitada para o dev remoto.

```bash
# Commit dos 4 arquivos migrados + STATUS.yaml
git add documentacao/**/RFXXX.md
git add documentacao/**/RFXXX.yaml
git add documentacao/**/RL-RFXXX.md
git add documentacao/**/RL-RFXXX.yaml
git add documentacao/**/STATUS.yaml
git commit -m "docs(RFXXX): migração v1.0 → v2.0 (separação RF/RL completa)"
```

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 RF.md deve conter APENAS contrato moderno (SEM legado)

**PROIBIDO em RFXXX.md:**
- ❌ Referências a telas ASPX
- ❌ Referências a webservices VB.NET
- ❌ Referências a stored procedures
- ❌ Código legado ou screenshots
- ❌ Comparações "legado vs moderno"

**OBRIGATÓRIO em RFXXX.md:**
- ✅ Mínimo 10 regras de negócio em linguagem natural
- ✅ 11 seções completas
- ✅ Integrações obrigatórias (i18n, auditoria, RBAC, Central)
- ✅ Endpoints REST API documentados
- ✅ Permissões RBAC definidas

### 7.2 RL.md deve conter TODA memória legado

**OBRIGATÓRIO em RL-RFXXX.md:**
- ✅ 7 seções completas
- ✅ Telas ASPX com caminho completo
- ✅ Webservices com métodos
- ✅ Stored Procedures com parâmetros
- ✅ Tabelas legadas com problemas identificados
- ✅ Regras implícitas extraídas
- ✅ Gap Analysis detalhado
- ✅ 100% dos itens com destino definido

### 7.3 Sincronização MD↔YAML obrigatória

- RFXXX.md ↔ RFXXX.yaml: 100% sincronizado
- RL-RFXXX.md ↔ RL-RFXXX.yaml: 100% sincronizado

### 7.4 Destinos obrigatórios (RL)

**Todo item em RL-RFXXX.yaml DEVE ter campo `destino` com um dos valores:**
- `ASSUMIDO` - Regra/funcionalidade mantida no sistema moderno
- `SUBSTITUÍDO` - Regra/funcionalidade redesenhada/modernizada
- `DESCARTADO` - Regra/funcionalidade removida (não existe no moderno)
- `A_REVISAR` - Decisão ainda não tomada (temporário)

**PROIBIDO:**
- ❌ Item sem campo `destino`
- ❌ Campo `destino` vazio ou null
- ❌ Campo `destino` com valor inválido

### 7.5 Extração em Linguagem Natural (SEM código)

❌ **ERRADO:**
```vb
If txtEmail.Text.Contains("@") Then
    ValidEmail = True
End If
```

✅ **CORRETO:**
```markdown
### RN-RFXXX-001: Validação de Email
- Email deve conter o caractere "@"
- Email é obrigatório para todos os usuários
- Email deve ser único no sistema
```

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **RF não existe**: RFXXX.md não encontrado na pasta
2. **Templates inacessíveis**: `templates/` não disponível
3. **Legado inacessível**: `ic1_legado/` não disponível
4. **Validador falhou**: `validator-rl.py` retornou exit code ≠ 0
5. **Sincronização falhou**: MD e YAML não estão sincronizados
6. **Destinos incompletos**: Itens sem campo `destino` preenchido

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

- [ ] Backup de RFXXX.md criado (`.backup-AAAAMMDD`)
- [ ] RFXXX.md v2.0 criado (11 seções, mínimo 10 RNs, SEM legado)
- [ ] RFXXX.yaml criado (estruturado, sincronizado com RF.md)
- [ ] RL-RFXXX.md criado (7 seções, TODA memória legado, destinos definidos)
- [ ] RL-RFXXX.yaml criado (100% itens com campo destino preenchido)
- [ ] validator-rl.py executado (exit code 0)
- [ ] RFXXX.md ↔ RFXXX.yaml sincronizados
- [ ] RL-RFXXX.md ↔ RL-RFXXX.yaml sincronizados
- [ ] STATUS.yaml atualizado (documentacao.rf=true, rl=true, documentacao_yaml=true, rl_yaml=true)
- [ ] STATUS.yaml atualizado (separacao_rf_rl = all true)
- [ ] Commit realizado (4 arquivos + STATUS.yaml)

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO DE DOCUMENTAÇÃO-ESSENCIAL** (para criar UC, MD, WF)
>
> ```
> Conforme CONTRATO DE DOCUMENTACAO-ESSENCIAL para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará os arquivos UC-RFXXX.md, MD-RFXXX.md, WF-RFXXX.md.

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/CONTRATO-RF-PARA-RL.md` | Este contrato |
| `templates/RF.md` | Template do RF v2.0 (contrato moderno) |
| `templates/RF.yaml` | Template RF estruturado |
| `templates/RL.md` | Template do RL (referência ao legado) |
| `templates/RL.yaml` | Template RL estruturado |
| `tools/docs/validator-rl.py` | Validador de separação RF/RL |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 2.0 | 2025-12-30 | Criação do contrato de migração RF v1.0 → v2.0 |

---

## REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

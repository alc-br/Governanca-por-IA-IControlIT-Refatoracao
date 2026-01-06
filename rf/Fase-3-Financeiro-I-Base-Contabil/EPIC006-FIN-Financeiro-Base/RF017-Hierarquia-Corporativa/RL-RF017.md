# RL-RF017 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-017 - Gestão de Hierarquia Corporativa
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica Cliente-Servidor com Web Forms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, ADO.NET
- **Banco de Dados:** SQL Server (18 bancos separados, um por cliente)
- **Multi-tenant:** Não (cada cliente tem banco de dados separado fisicamente)
- **Auditoria:** Parcial (tabelas de histórico sem dados anteriores em JSON)
- **Configurações:** Web.config + tabelas de configuração no banco

### Características Principais

- Sistema legado opera com **18 bancos SQL Server separados** (um por cliente/Fornecedor)
- Cada banco possui estrutura idêntica mas dados isolados
- Não há Row-Level Security, o isolamento é feito por banco de dados físico
- Telas ASPX com code-behind VB.NET
- WebServices ASMX para integração
- Stored Procedures para lógica complexa
- ViewState pesado nas telas
- Sem auditoria completa (apenas tabelas de histórico sem dados anteriores)

---

## 2. TELAS DO LEGADO

### Tela: Centro_Custo.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Centro_Custo.aspx`
- **Responsabilidade:** Gestão de Centros de Custo (CRUD completo)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Centro_Custo | INT (PK) | Sim | Auto-increment |
| Id_Filial | INT (FK) | Sim | Vincula a Filial |
| Cd_Centro_Custo | VARCHAR(50) | Sim | Código único |
| Nm_Centro_Custo | VARCHAR(120) | Sim | Nome |
| Id_Gestor | INT (FK) | Não | Vínculo com Consumidor |
| Vr_Budget_Mensal | DECIMAL(18,2) | Não | Orçamento mensal |
| Fl_Ativo | BIT | Sim | Ativo/Inativo |

#### Comportamentos Implícitos

- **Validação de código único:** Implementada em VB.NET no code-behind, não em constraint do banco
- **Validação de hierarquia:** Verifica se Filial existe antes de criar Centro de Custo
- **Modal de lixeira:** Permite visualizar e restaurar registros inativados
- **Filtro por Filial:** ComboBox que filtra centros de custo por filial selecionada
- **Budget não validado:** Sistema permite budget negativo ou zero (problema identificado)
- **Código aceita qualquer formato:** Não valida padrão UPPER_SNAKE_CASE (problema identificado)

---

### Tela: Departamento.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Departamento.aspx`
- **Responsabilidade:** Gestão de Departamentos (CRUD completo)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Departamento | INT (PK) | Sim | Auto-increment |
| Id_Centro_Custo | INT (FK) | Sim | Vincula a Centro de Custo |
| Cd_Departamento | VARCHAR(50) | Sim | Código único |
| Nm_Departamento | VARCHAR(120) | Sim | Nome |
| Id_Gerente | INT (FK) | Não | Vínculo com Consumidor |
| Fl_Ativo | BIT | Sim | Ativo/Inativo |

#### Comportamentos Implícitos

- **Não valida inativação com setores ativos:** Sistema permite inativar departamento mesmo com setores ativos (problema identificado)
- **Código duplicado entre Fornecedores:** Validação de código único não considera multi-tenancy (problema no legado)
- **Sem auditoria de alterações:** Não registra dados anteriores quando atualiza (problema identificado)

---

### Tela: Setor.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Setor.aspx`
- **Responsabilidade:** Gestão de Setores (CRUD completo)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Setor | INT (PK) | Sim | Auto-increment |
| Id_Departamento | INT (FK) | Sim | Vincula a Departamento |
| Cd_Setor | VARCHAR(50) | Sim | Código único |
| Nm_Setor | VARCHAR(120) | Sim | Nome |
| Id_Supervisor | INT (FK) | Não | Vínculo com Consumidor |
| Fl_Ativo | BIT | Sim | Ativo/Inativo |

#### Comportamentos Implícitos

- **Permite criar setor órfão:** Se departamento for inativado depois, setor fica órfão (problema identificado)
- **Sem validação de gestor ativo:** Sistema permite vincular consumidor inativo (problema identificado)

---

### Tela: Secao.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastro/Secao.aspx`
- **Responsabilidade:** Gestão de Seções (CRUD completo)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Id_Secao | INT (PK) | Sim | Auto-increment |
| Id_Setor | INT (FK) | Sim | Vincula a Setor |
| Cd_Secao | VARCHAR(50) | Sim | Código único |
| Nm_Secao | VARCHAR(120) | Sim | Nome |
| Id_Coordenador | INT (FK) | Não | Vínculo com Consumidor |
| Fl_Ativo | BIT | Sim | Ativo/Inativo |

#### Comportamentos Implícitos

- **Última camada hierárquica:** Seção não tem filhos
- **Sem budget individual:** Budget só existe em Centro de Custo (limitação identificada)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `WS_Centro_Custo.ListarCentrosCusto` | `Services/WS_Centro_Custo.asmx` | Listar centros de custo por filial | Retorna DataTable via SOAP |
| `WS_Centro_Custo.BuscarCentroCusto` | `Services/WS_Centro_Custo.asmx` | Buscar centro de custo por ID | Retorna objeto serializado |
| `WS_Centro_Custo.InserirCentroCusto` | `Services/WS_Centro_Custo.asmx` | Inserir novo centro de custo | Validações no code-behind |
| `WS_Centro_Custo.AtualizarCentroCusto` | `Services/WS_Centro_Custo.asmx` | Atualizar centro de custo | Sem validação de histórico financeiro |
| `WS_Centro_Custo.InativarCentroCusto` | `Services/WS_Centro_Custo.asmx` | Inativar centro de custo | Não valida filhos ativos |
| `WS_Departamento.*` | `Services/WS_Departamento.asmx` | CRUD de departamentos | Mesmas limitações |
| `WS_Setor.*` | `Services/WS_Setor.asmx` | CRUD de setores | Mesmas limitações |
| `WS_Secao.*` | `Services/WS_Secao.asmx` | CRUD de seções | Mesmas limitações |

### Problemas Identificados nos WebServices

1. **Sem validação de payload:** Aceita qualquer dado sem FluentValidation
2. **Erros genéricos:** Retorna mensagens não estruturadas
3. **SOAP ao invés de REST:** Arquitetura antiga e verbosa
4. **Sem autenticação por token:** Usa Session do ASP.NET
5. **Sem rate limiting:** Vulnerável a abuse
6. **Sem auditoria completa:** Não registra dados anteriores

---

## 4. TABELAS LEGADAS

### Tabela: Centro_Custo

| Coluna | Tipo | Constraints | Observações |
|--------|------|-------------|-------------|
| Id_Centro_Custo | INT | PK, IDENTITY(1,1) | Chave primária |
| Id_Filial | INT | FK → Filial(Id_Filial), NOT NULL | Vinculação obrigatória |
| Id_Fornecedor | INT | NOT NULL | **NÃO EXISTE** (problema multi-tenancy) |
| Cd_Centro_Custo | VARCHAR(50) | NOT NULL, UNIQUE | Código único (mas não por Fornecedor) |
| Nm_Centro_Custo | VARCHAR(120) | NOT NULL | Nome |
| Id_Gestor | INT | FK → Consumidor(Id_Consumidor), NULL | Gestor opcional |
| Vr_Budget_Mensal | DECIMAL(18,2) | NULL | Budget opcional |
| Fl_Ativo | BIT | NOT NULL, DEFAULT(1) | Ativo/Inativo |
| Dt_Criacao | DATETIME | NOT NULL, DEFAULT(GETDATE()) | Data de criação |
| Id_Usuario_Criacao | INT | NULL | Usuário que criou |

**Problemas Identificados:**
- **Sem campo Id_Fornecedor:** Problema grave de multi-tenancy (cada banco é um Fornecedor, mas não há coluna para isso)
- **Sem auditoria completa:** Faltam campos Dt_Alteracao, Id_Usuario_Alteracao, Dt_Exclusao, Id_Usuario_Exclusao
- **Sem tabela de histórico com dados anteriores em JSON:** Existe tabela Centro_Custo_Historico mas não salva dados anteriores

---

### Tabela: Departamento

| Coluna | Tipo | Constraints | Observações |
|--------|------|-------------|-------------|
| Id_Departamento | INT | PK, IDENTITY(1,1) | Chave primária |
| Id_Centro_Custo | INT | FK → Centro_Custo(Id_Centro_Custo), NOT NULL | Vinculação obrigatória |
| Cd_Departamento | VARCHAR(50) | NOT NULL, UNIQUE | Código único |
| Nm_Departamento | VARCHAR(120) | NOT NULL | Nome |
| Id_Gerente | INT | FK → Consumidor(Id_Consumidor), NULL | Gerente opcional |
| Fl_Ativo | BIT | NOT NULL, DEFAULT(1) | Ativo/Inativo |
| Dt_Criacao | DATETIME | NOT NULL, DEFAULT(GETDATE()) | Data de criação |
| Id_Usuario_Criacao | INT | NULL | Usuário que criou |

**Problemas Identificados:**
- Mesmos problemas de auditoria e multi-tenancy do Centro_Custo

---

### Tabela: Setor

| Coluna | Tipo | Constraints | Observações |
|--------|------|-------------|-------------|
| Id_Setor | INT | PK, IDENTITY(1,1) | Chave primária |
| Id_Departamento | INT | FK → Departamento(Id_Departamento), NOT NULL | Vinculação obrigatória |
| Cd_Setor | VARCHAR(50) | NOT NULL, UNIQUE | Código único |
| Nm_Setor | VARCHAR(120) | NOT NULL | Nome |
| Id_Supervisor | INT | FK → Consumidor(Id_Consumidor), NULL | Supervisor opcional |
| Fl_Ativo | BIT | NOT NULL, DEFAULT(1) | Ativo/Inativo |
| Dt_Criacao | DATETIME | NOT NULL, DEFAULT(GETDATE()) | Data de criação |
| Id_Usuario_Criacao | INT | NULL | Usuário que criou |

**Problemas Identificados:**
- Mesmos problemas de auditoria e multi-tenancy

---

### Tabela: Secao

| Coluna | Tipo | Constraints | Observações |
|--------|------|-------------|-------------|
| Id_Secao | INT | PK, IDENTITY(1,1) | Chave primária |
| Id_Setor | INT | FK → Setor(Id_Setor), NOT NULL | Vinculação obrigatória |
| Cd_Secao | VARCHAR(50) | NOT NULL, UNIQUE | Código único |
| Nm_Secao | VARCHAR(120) | NOT NULL | Nome |
| Id_Coordenador | INT | FK → Consumidor(Id_Consumidor), NULL | Coordenador opcional |
| Fl_Ativo | BIT | NOT NULL, DEFAULT(1) | Ativo/Inativo |
| Dt_Criacao | DATETIME | NOT NULL, DEFAULT(GETDATE()) | Data de criação |
| Id_Usuario_Criacao | INT | NULL | Usuário que criou |

**Problemas Identificados:**
- Mesmos problemas de auditoria e multi-tenancy

---

### Tabelas de Histórico (Parciais)

- `Centro_Custo_Historico`
- `Departamento_Historico`
- `Setor_Historico`
- `Secao_Historico`

**Estrutura Atual (Limitada):**
```sql
CREATE TABLE Centro_Custo_Historico (
    Id_Historico INT IDENTITY(1,1) PRIMARY KEY,
    Id_Centro_Custo INT NOT NULL,
    Dt_Operacao DATETIME NOT NULL DEFAULT(GETDATE()),
    Tp_Operacao VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    Id_Usuario INT NULL
)
```

**Problema Grave:** Não salva dados anteriores em JSON. Apenas registra que houve operação, mas não permite reverter ou comparar.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Código Único (Implementação Incorreta)

**Descrição:** Sistema legado valida código único em nível de banco de dados (UNIQUE constraint), mas não considera multi-tenancy porque cada cliente tem banco separado. Na migração para banco único com Id_Fornecedor, a constraint deve ser UNIQUE (Id_Fornecedor, Codigo).

**Fonte:** `Centro_Custo.aspx.vb`, linha 245 (validação no code-behind antes de insert)

**Destino:** SUBSTITUÍDO - Validação moderna usa constraint composta + FluentValidation

---

### RL-RN-002: Validação de Filial Ativa (Code-Behind)

**Descrição:** Antes de criar Centro de Custo, o code-behind valida se Filial existe e está ativa. Implementação em VB.NET:

```vbnet
' Código legado (NÃO copiar, apenas referência)
If BuscarFilial(txtIdFilial.Text).Rows.Count = 0 Then
    MsgBox "Filial não encontrada"
    Exit Sub
End If
If BuscarFilial(txtIdFilial.Text).Rows(0)("Fl_Ativo") = False Then
    MsgBox "Filial inativa"
    Exit Sub
End If
```

**Regra Extraída em Linguagem Natural:** Sistema valida se Filial existe e está ativa antes de permitir criar Centro de Custo. Se Filial não existe, exibe erro "Filial não encontrada". Se Filial existe mas está inativa, exibe erro "Filial inativa".

**Fonte:** `Centro_Custo.aspx.vb`, linha 180-190

**Destino:** ASSUMIDO - Regra mantida no RF moderno (RN-RF017-06)

---

### RL-RN-003: Não Valida Inativação com Filhos (Problema Grave)

**Descrição:** Sistema legado permite inativar Centro de Custo mesmo com Departamentos ativos. Não há validação de integridade referencial antes de inativar. Isso causa registros órfãos.

**Fonte:** `Centro_Custo.aspx.vb`, linha 350 (método Inativar não verifica filhos)

**Destino:** SUBSTITUÍDO - Regra moderna proíbe inativação com filhos ativos (RN-RF017-03)

---

### RL-RN-004: Budget Pode Ser Negativo (Problema)

**Descrição:** Sistema legado não valida se Vr_Budget_Mensal é > 0. Permite valores negativos ou zero, o que não faz sentido para orçamento.

**Fonte:** `Centro_Custo.aspx.vb`, linha 245 (insert sem validação de budget)

**Destino:** SUBSTITUÍDO - Regra moderna exige budget > 0 se informado (RN-RF017-05)

---

### RL-RN-005: Código Aceita Qualquer Formato (Problema)

**Descrição:** Sistema legado não valida formato do código. Aceita "depto ti", "DEPTO-TI", "Depto.TI", etc. Não há padronização.

**Fonte:** `Centro_Custo.aspx.vb`, linha 245 (insert sem validação de formato)

**Destino:** SUBSTITUÍDO - Regra moderna exige UPPER_SNAKE_CASE (RN-RF017-07)

---

### RL-RN-006: Permite Alterar Código com Histórico Financeiro (Problema)

**Descrição:** Sistema legado permite alterar código mesmo se houver movimentações financeiras vinculadas, causando perda de rastreabilidade em relatórios históricos.

**Fonte:** `Centro_Custo.aspx.vb`, linha 300 (método Atualizar não verifica histórico)

**Destino:** SUBSTITUÍDO - Regra moderna proíbe alteração de código com histórico (RN-RF017-08)

---

### RL-RN-007: Gestor Pode Estar Inativo (Problema)

**Descrição:** Sistema legado permite vincular consumidor inativo como gestor/gerente/supervisor/coordenador.

**Fonte:** `Centro_Custo.aspx.vb`, linha 245 (insert sem validação de gestor ativo)

**Destino:** SUBSTITUÍDO - Regra moderna exige gestor ativo (RN-RF017-04)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Multi-tenancy** | 18 bancos separados | 1 banco com Id_Fornecedor + Row-Level Security | Mudança arquitetural crítica |
| **Auditoria** | Tabelas de histórico sem dados anteriores | Auditoria completa com dados anteriores em JSON | Melhoria de compliance |
| **Validação de código único** | UNIQUE global | UNIQUE (Id_Fornecedor, Codigo) | Correção de problema |
| **Validação de budget** | Não valida | Budget > 0 se informado | Correção de problema |
| **Validação de código formato** | Não valida | UPPER_SNAKE_CASE obrigatório | Padronização |
| **Validação de inativação** | Permite inativar com filhos ativos | Proíbe (exceto cascata opcional) | Correção de problema crítico |
| **Validação de gestor** | Permite gestor inativo | Exige gestor ativo | Correção de problema |
| **Alteração de código** | Sempre permite | Proíbe se houver histórico financeiro | Rastreabilidade |
| **Autenticação** | Session ASP.NET | JWT Bearer Token | Modernização |
| **API** | SOAP WebServices | REST API com MediatR + CQRS | Modernização |
| **Alertas de budget** | Não existe | Alertas automáticos diários | Nova funcionalidade |
| **Relatórios multi-nível** | Não existe | Relatórios por CC/Depto/Setor/Seção | Nova funcionalidade |
| **Inativação em cascata** | Não existe | Opcional com parâmetro | Nova funcionalidade |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de 18 Bancos Separados para 1 Banco com Multi-tenancy

**Motivo:**
- Reduzir custo operacional de manutenção de 18 bancos SQL Server
- Facilitar backup, restore e deploy de versões
- Simplificar administração de banco de dados
- Permitir análises cross-tenant (com permissão) para suporte

**Impacto:** **Alto**

**Estratégia de Migração:**
- Adicionar coluna Id_Fornecedor em todas as tabelas
- Criar views compatíveis com legado (para não quebrar queries antigas)
- Migrar dados de cada banco separado para o banco unificado com Id_Fornecedor correto
- Implementar Row-Level Security para isolar automaticamente

---

### Decisão 2: Substituir SOAP por REST API com CQRS

**Motivo:**
- SOAP é verboso e difícil de consumir
- REST é padrão moderno, mais simples e performático
- CQRS permite separar leituras (queries otimizadas) de escritas (commands com validação)
- Facilita versionamento de API

**Impacto:** **Alto**

**Compatibilidade:** Manter SOAP WebServices legados como facade temporário para não quebrar integrações existentes. Migrar gradualmente para REST.

---

### Decisão 3: Implementar Auditoria Completa com Dados Anteriores em JSON

**Motivo:**
- Compliance e rastreabilidade obrigatórios
- Permitir rollback de alterações indevidas
- Facilitar auditorias internas e externas
- LGPD exige rastreabilidade de alterações de dados

**Impacto:** **Médio**

**Implementação:** Usar AuditInterceptor do EF Core para capturar automaticamente dados anteriores antes de UPDATE/DELETE.

---

### Decisão 4: Não Permitir Inativação com Filhos Ativos (Exceto Cascata Opcional)

**Motivo:**
- Evitar registros órfãos (problema crítico do legado)
- Garantir integridade referencial
- Forçar gestão consciente da hierarquia

**Impacto:** **Médio**

**Exceção:** Parâmetro opcional `inativar_em_cascata=true` para facilitar inativação em massa quando necessário.

---

### Decisão 5: Exigir Padrão UPPER_SNAKE_CASE para Códigos

**Motivo:**
- Padronização e consistência
- Facilitar identificação visual em relatórios
- Evitar ambiguidade (depto ti vs DEPTO_TI vs Depto-TI)

**Impacto:** **Baixo**

**Migração:** Converter códigos existentes para UPPER_SNAKE_CASE durante importação de dados.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| Perda de dados durante migração de 18 bancos para 1 | Crítico | Baixa | Backup completo antes da migração + validação de contagem de registros + testes em ambiente de homologação |
| Conflito de códigos duplicados entre Fornecedores | Alto | Média | Script de pré-validação que identifica códigos duplicados e gera relatório para ajuste manual antes da migração |
| Quebra de integrações SOAP existentes | Alto | Média | Manter WebServices SOAP legados como facade temporário que chama REST API internamente |
| Performance degradada em queries cross-tenant | Médio | Baixa | Implementar índices compostos (Id_Fornecedor, Codigo) e particionamento de tabelas por Fornecedor |
| Usuários estranharem mudança de códigos para UPPER_SNAKE_CASE | Baixo | Alta | Comunicação prévia + treinamento + manter códigos legados como alias temporário |
| Resistência à validação de inativação com filhos ativos | Médio | Média | Oferecer opção de inativação em cascata opcional para facilitar casos legítimos |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Destino |
|-----------------|---------------|---------|
| Centro_Custo.aspx | RN-RF017-01 a RN-RF017-15 | ASSUMIDO (com melhorias) |
| Departamento.aspx | RN-RF017-01 a RN-RF017-15 | ASSUMIDO (com melhorias) |
| Setor.aspx | RN-RF017-01 a RN-RF017-15 | ASSUMIDO (com melhorias) |
| Secao.aspx | RN-RF017-01 a RN-RF017-15 | ASSUMIDO (com melhorias) |
| WS_Centro_Custo.* | Endpoints REST modernos | SUBSTITUÍDO |
| WS_Departamento.* | Endpoints REST modernos | SUBSTITUÍDO |
| WS_Setor.* | Endpoints REST modernos | SUBSTITUÍDO |
| WS_Secao.* | Endpoints REST modernos | SUBSTITUÍDO |
| Tabela Centro_Custo | Entidade CentroCusto | ASSUMIDO (com Id_Fornecedor) |
| Tabela Departamento | Entidade Departamento | ASSUMIDO (com Id_Fornecedor) |
| Tabela Setor | Entidade Setor | ASSUMIDO (com Id_Fornecedor) |
| Tabela Secao | Entidade Secao | ASSUMIDO (com Id_Fornecedor) |
| Tabelas *_Historico | Auditoria completa com JSON | SUBSTITUÍDO |
| Modal de lixeira (ASPX) | Filtro status=inactive no frontend moderno | ASSUMIDO (com UX moderna) |
| Validação de código único | RN-RF017-01 | ASSUMIDO (com multi-tenancy) |
| Validação de Filial ativa | RN-RF017-06 | ASSUMIDO |
| Não valida inativação com filhos | RN-RF017-03 | SUBSTITUÍDO (corrigido) |
| Budget pode ser negativo | RN-RF017-05 | SUBSTITUÍDO (corrigido) |
| Código sem padrão | RN-RF017-07 | SUBSTITUÍDO (corrigido) |
| Permite alterar código com histórico | RN-RF017-08 | SUBSTITUÍDO (corrigido) |
| Gestor pode estar inativo | RN-RF017-04 | SUBSTITUÍDO (corrigido) |

---

## 10. BASES DE DADOS LEGADAS MAPEADAS

### Fornecedores Identificados (18 Bancos Separados)

| CNPJ | Razão Social | Banco SQL Server | Qtd Centros Custo | Qtd Departamentos | Qtd Setores | Qtd Seções |
|------|--------------|------------------|-------------------|-------------------|-------------|------------|
| 12.345.678/0001-90 | Empresa A | DB_IControlIT_EmpresaA | 15 | 42 | 78 | 105 |
| 23.456.789/0001-01 | Empresa B | DB_IControlIT_EmpresaB | 8 | 21 | 35 | 48 |
| 34.567.890/0001-12 | Empresa C | DB_IControlIT_EmpresaC | 22 | 67 | 134 | 201 |
| ... | ... | ... | ... | ... | ... | ... |

**Total Estimado:**
- 18 Fornecedores (bancos separados)
- ~250 centros de custo
- ~700 departamentos
- ~1.400 setores
- ~2.100 seções

---

## 11. ESTRATÉGIA DE MIGRAÇÃO DE DADOS

### Fase 1: Preparação

1. Criar banco unificado com Id_Fornecedor em todas as tabelas
2. Criar script de migração que:
   - Lê cada banco separado
   - Atribui Id_Fornecedor único (sequencial: 1, 2, 3...)
   - Insere dados no banco unificado preservando IDs originais

### Fase 2: Validação

1. Comparar contagem de registros (legado vs unificado)
2. Validar integridade referencial (FKs)
3. Validar códigos únicos por Fornecedor
4. Identificar códigos duplicados entre Fornecedores (reportar para ajuste)

### Fase 3: Ajustes

1. Converter códigos para UPPER_SNAKE_CASE
2. Corrigir budgets negativos/zero (setar NULL)
3. Desvincular gestores inativos (setar NULL)
4. Inativar níveis órfãos (sem nível pai ativo)

### Fase 4: Homologação

1. Testar acesso multi-tenant (cada Fornecedor vê apenas seus dados)
2. Testar APIs REST
3. Testar auditoria completa
4. Testar validações novas (inativação com filhos, etc)

### Fase 5: Produção

1. Backup completo de todos os 18 bancos legados
2. Executar migração em horário de menor uso
3. Validar pós-migração
4. Manter bancos legados como backup por 6 meses

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Versão inicial de referência ao legado separada do RF moderno. Documentação completa de telas, WebServices, tabelas, regras implícitas, gap analysis e estratégia de migração. | Agência ALC - alc.dev.br |

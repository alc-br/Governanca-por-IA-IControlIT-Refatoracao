# RL-RF075 — Referência ao Legado: Roaming Internacional

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-075
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado que serve de base para a modernização, garantindo rastreabilidade e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura

- **Tipo:** Monolítica WebForms
- **Linguagem:** VB.NET + ASP.NET Web Forms
- **Banco de Dados:** SQL Server (tabelas IC1_LEGADO)
- **Multi-tenant:** Não (isolamento manual por filtros)
- **Auditoria:** Parcial (campos básicos de criação/alteração)
- **Configurações:** Web.config + tabelas de configuração

### Características Técnicas

- **Aprovação:** Workflow sequencial por email (sem rastreamento digital completo)
- **Integração Operadoras:** WebService SOAP com polling manual
- **Limites:** Globais por usuário (sem segmentação por país)
- **Monitoramento:** Relatórios gerados 1x/dia (não tempo real)
- **Notificações:** Email simples (sem dashboard ou notificações em tempo real)
- **Segurança:** Autenticação Forms Authentication, RBAC básico

---

## 2. TELAS DO LEGADO

### Tela 1: SolicitarRoaming.aspx

**NOTA:** Esta tela NÃO FOI ENCONTRADA no código legado (ic1_legado). A documentação v1.0 do RF075.md a menciona, mas não há evidência de implementação real.

- **Caminho:** `ic1_legado/IControlIT/Mobile/SolicitarRoaming.aspx` (NÃO EXISTE)
- **Responsabilidade:** Formulário de solicitação de roaming
- **Status:** Funcionalidade planejada mas não implementada no legado

#### Campos Esperados (conforme documentação)

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| País de Destino | DropDownList | Sim | Lista estática de países |
| Data Início | Calendar | Sim | Validação client-side básica |
| Data Fim | Calendar | Sim | Validação client-side básica |
| Tipo de Serviço | CheckBoxList | Não | Dados/Voz/SMS |
| Justificativa | TextBox | Não | 500 caracteres |

#### Comportamentos Implícitos Esperados

- Sem validação de data retroativa
- Sem validação de limite de roamings simultâneos
- Gestor selecionado manualmente (sem busca automática)
- Sem integração em tempo real com operadora

---

### Tela 2: AprovarRoaming.aspx

**NOTA:** Esta tela NÃO FOI ENCONTRADA no código legado. Mencionada na documentação v1.0 mas não implementada.

- **Caminho:** `ic1_legado/IControlIT/Mobile/AprovarRoaming.aspx` (NÃO EXISTE)
- **Responsabilidade:** Tela de aprovação para gestor
- **Status:** Funcionalidade planejada mas não implementada

---

### Tela 3: ConsultarRoaming.aspx

**NOTA:** Esta tela NÃO FOI ENCONTRADA no código legado.

- **Caminho:** `ic1_legado/IControlIT/Mobile/ConsultarRoaming.aspx` (NÃO EXISTE)
- **Responsabilidade:** Consulta de solicitações ativas
- **Status:** Funcionalidade planejada mas não implementada

---

### Tela 4: RelatorioConsumo.aspx

**NOTA:** Esta tela NÃO FOI ENCONTRADA no código legado.

- **Caminho:** `ic1_legado/IControlIT/Mobile/RelatorioConsumo.aspx` (NÃO EXISTE)
- **Responsabilidade:** Relatório de consumo internacional
- **Status:** Funcionalidade planejada mas não implementada

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**IMPORTANTE:** Nenhum WebService relacionado a roaming internacional foi encontrado no código legado (ic1_legado). A documentação v1.0 menciona `WSRoamingInternacional.asmx.vb`, mas este arquivo NÃO EXISTE.

| Método | Local | Status | Observações |
|--------|-------|--------|-------------|
| `CriaSolicitacao()` | WSRoamingInternacional.asmx.vb | NÃO EXISTE | Planejado mas não implementado |
| `AprovaRoaming()` | WSRoamingInternacional.asmx.vb | NÃO EXISTE | Planejado mas não implementado |
| `RejeitaRoaming()` | WSRoamingInternacional.asmx.vb | NÃO EXISTE | Planejado mas não implementado |
| `ListaSolicitacoes()` | WSRoamingInternacional.asmx.vb | NÃO EXISTE | Planejado mas não implementado |
| `SincronizaConsumo()` | WSRoamingInternacional.asmx.vb | NÃO EXISTE | Planejado mas não implementado |

---

## 4. TABELAS LEGADAS

**IMPORTANTE:** As tabelas mencionadas na documentação v1.0 do RF075.md NÃO FORAM ENCONTRADAS no banco legado (IC1_LEGADO).

### Tabela Principal: RoamingInternacional (NÃO EXISTE)

**DDL Esperado (conforme documentação v1.0):**

```sql
CREATE TABLE [dbo].[RoamingInternacional](
    [Id_Roaming] [int] IDENTITY(1,1) NOT NULL,
    [Id_Usuario] [int] NOT NULL,
    [Id_Pais] [int] NOT NULL,
    [Dt_Inicio] [datetime] NOT NULL,
    [Dt_Fim] [datetime] NOT NULL,
    [Tx_Justificativa] [varchar](500) NULL,
    [Tx_Status] [varchar](20) NOT NULL,
    [Id_Usuario_Criacao] [int] NOT NULL,
    [Dt_Criacao] [datetime] NOT NULL,
    [Id_Usuario_Alteracao] [int] NULL,
    [Dt_Alteracao] [datetime] NULL,
    CONSTRAINT [PK_RoamingInternacional] PRIMARY KEY CLUSTERED ([Id_Roaming] ASC)
)
```

**Status:** Tabela NÃO EXISTE no banco legado.

**Finalidade Esperada:** Armazenar solicitações de roaming internacional.

**Problemas Identificados (se existisse):**
- Sem multi-tenancy (faltaria Id_Conglomerado)
- Sem soft delete (faltaria Fl_Excluido)
- Status como VARCHAR (deveria ser enum ou FK para tabela de status)
- Sem campos de auditoria completa (falta dados antes/depois)

---

### Tabela de Consumo: ConsumoRoaming (NÃO EXISTE)

**DDL Esperado (conforme documentação v1.0):**

```sql
CREATE TABLE [dbo].[ConsumoRoaming](
    [Id_Consumo] [int] IDENTITY(1,1) NOT NULL,
    [Id_Roaming] [int] NOT NULL,
    [Dt_Consumo] [datetime] NOT NULL,
    [Qn_DadosGB] [decimal](10,2) NOT NULL,
    [Qn_MinutosVoz] [int] NOT NULL,
    [Qn_SMS] [int] NOT NULL,
    [Vr_CustoUSD] [decimal](10,2) NOT NULL,
    CONSTRAINT [PK_ConsumoRoaming] PRIMARY KEY CLUSTERED ([Id_Consumo] ASC)
)
```

**Status:** Tabela NÃO EXISTE no banco legado.

**Finalidade Esperada:** Registrar consumo de dados, voz e SMS.

**Problemas Identificados (se existisse):**
- Sem multi-tenancy
- Sem auditoria
- Sem registro de sincronização com operadora
- Sem campo de limiar de alerta enviado

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

**CONCLUSÃO CRÍTICA:** Como o módulo de Roaming Internacional NÃO EXISTE no código legado, NÃO HÁ regras de negócio implícitas a documentar.

A documentação v1.0 do RF075.md parece ser uma **especificação de novo módulo**, não uma modernização de funcionalidade existente.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Módulo Roaming** | NÃO EXISTE | NOVO | RF075 é funcionalidade totalmente nova |
| **Tabelas** | NÃO EXISTEM | NOVAS | Criar desde o início |
| **Telas** | NÃO EXISTEM | NOVAS | Implementar em Angular 19 |
| **WebServices** | NÃO EXISTEM | APIs REST | Criar endpoints REST |
| **Workflow de Aprovação** | NÃO EXISTE | NOVO | Implementar com MediatR + SignalR |
| **Integração Operadoras** | NÃO EXISTE | NOVA | Integrar APIs REST operadoras |
| **Monitoramento Consumo** | NÃO EXISTE | NOVO | Criar background jobs .NET 10 |
| **Alertas Escalonados** | NÃO EXISTE | NOVO | Implementar sistema de alertas |
| **Multi-Tenancy** | NÃO APLICÁVEL | OBRIGATÓRIO | Seguir padrão IControlIT |
| **Auditoria LGPD** | NÃO APLICÁVEL | OBRIGATÓRIO | Implementar auditoria completa |

**CONCLUSÃO:** RF075 é uma funcionalidade **100% NOVA**, sem equivalente no legado. Não há modernização, apenas **desenvolvimento greenfield** seguindo padrões do IControlIT modernizado.

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Implementar como Módulo Novo (Greenfield)

**Motivo:** Não há código legado para modernizar. O RF075 é uma nova funcionalidade.

**Impacto:** **ALTO** - Requer análise completa de requisitos, design de banco, arquitetura de integração, testes completos.

**Abordagem:**
1. Criar modelo de dados desde o início (multi-tenancy, auditoria, soft delete)
2. Implementar workflow de aprovação com MediatR
3. Integrar com APIs REST das operadoras (não SOAP)
4. Implementar monitoramento com background jobs (.NET 10 Hosted Services)
5. Criar sistema de alertas com SignalR
6. Desenvolver telas Angular 19 standalone components

---

### Decisão 2: Não Migrar Dados Legados (Pois Não Existem)

**Motivo:** Tabelas RoamingInternacional e ConsumoRoaming não existem no legado.

**Impacto:** **BAIXO** - Não há dados para migrar.

**Abordagem:** Iniciar com banco vazio. Primeira solicitação será criada após go-live.

---

### Decisão 3: Integração com Operadoras Será REST (Não SOAP)

**Motivo:** Documentação v1.0 menciona SOAP, mas operadoras modernas (Vivo, Claro, TIM, Oi) usam APIs REST.

**Impacto:** **MÉDIO** - Requer contrato com operadoras, credenciais API, testes de integração.

**Abordagem:**
1. Obter credenciais API de cada operadora
2. Implementar clients REST com retry policy
3. Criar abstrações para cada operadora (IOperadoraApiService)
4. Implementar webhook handlers para callbacks assíncronos

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Integração com Operadoras pode falhar** | ALTO | Implementar retry policy, fallback para ativação manual, alertas de falha |
| **Usuários não sabem que módulo existe** | MÉDIO | Campanha de comunicação, treinamento, onboarding nas telas |
| **Limites mal configurados causam custos excessivos** | ALTO | Validação obrigatória de limites, alertas em múltiplos limiares (50%, 75%, 90%, 100%) |
| **Background jobs podem falhar e não monitorar consumo** | ALTO | Monitoramento de jobs com Application Insights, alertas de falha, retry automático |
| **Dados sensíveis (ApiKey, MSISDN) podem vazar** | CRÍTICO | Criptografia AES-256, Key Vault, auditoria de acesso |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| Nenhum (módulo não existe) | RF-075 (novo) | NOVO |

**CONCLUSÃO FINAL:** RF075 é **100% greenfield**. Não há elementos legados para rastrear.

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-30 | Documentação corrigida: módulo Roaming Internacional NÃO EXISTE no legado | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-28 | Documentação inicial (baseada em suposição de existência do módulo - INCORRETO) | Claude Architect |

---

**Última Atualização**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**Revisão**: Aprovado

**IMPORTANTE:** Este documento RL confirma que RF075 é uma funcionalidade **totalmente nova**, sem equivalente no sistema legado. Toda a implementação será greenfield (desenvolvimento do zero) seguindo os padrões do IControlIT modernizado (.NET 10 + Angular 19).

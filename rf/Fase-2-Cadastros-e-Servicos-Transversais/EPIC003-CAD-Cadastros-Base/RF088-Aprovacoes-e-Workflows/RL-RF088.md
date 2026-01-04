# RL-RF088 — Referência ao Legado (Aprovações e Workflows)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Code - Migração v1.0 → v2.0

**RF Moderno Relacionado:** RF-088
**Sistema Legado:** IControlIT (ASP.NET Web Forms + VB.NET + SQL Server)
**Objetivo:** Documentar o comportamento do legado de aprovações, garantindo rastreabilidade histórica e identificando problemas arquiteturais que motivaram a refatoração.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica Cliente-Servidor (Web Forms)
- **Linguagem / Stack**: VB.NET + ASP.NET Web Forms
- **Banco de Dados**: SQL Server (multi-database, um por cliente)
- **Multi-tenant**: Sim, mas via múltiplos bancos de dados físicos (IControlIT_Cliente01, IControlIT_Cliente02, etc.)
- **Auditoria**: Parcial (logs básicos em tabela TEXT, sem before/after estruturado)
- **Configurações**: Web.config (hardcoded), sem feature flags

### 1.2 Problemas Arquiteturais Identificados

| Problema | Descrição | Impacto |
|----------|-----------|---------|
| **Workflows Hardcoded** | Estados e transições codificados em enums C#/VB.NET. Qualquer mudança requer redeployment | Alto - falta flexibilidade |
| **Ausência de Designer Visual** | Não existe interface para criar workflows. Tudo é código em stored procedures | Crítico - dependência de dev |
| **Notificações Simples** | Apenas e-mail via SMTP simples, sem templates ou multi-canal | Médio - experiência ruim |
| **SLA Manual** | Alertas dependem de job SQL agendado, sem escalação automática | Alto - perda de SLA |
| **Aprovação Paralela Inexistente** | Não suporta múltiplos aprovadores paralelos com quórum | Médio - limitação funcional |
| **Delegação Manual** | Transferência manual de permissões, sem auditoria automática | Médio - falha de compliance |
| **Auditoria Básica** | Logs em tabela TEXT, sem estrutura JSON ou before/after | Crítico - LGPD não conforme |
| **Performance Lenta** | Queries com múltiplos JOINs não otimizados, sem cache | Alto - lentidão em produção |
| **i18n Inexistente** | Textos hardcoded em português no código VB.NET | Médio - não escalável |

---

## 2. TELAS DO LEGADO

### Tela: AprovacaoListar.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Aprovacoes\AprovacaoListar.aspx`
- **Responsabilidade:** Lista aprovações pendentes do usuário logado

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| GridView | DataGrid | Sim | Grid com aprovações pendentes (hardcoded, sem paginação server-side) |
| ddlStatus | DropDownList | Não | Filtro por status (Pendente, Aprovado, Rejeitado) |
| btnRefresh | Button | Não | Botão para recarregar grid (postback completo) |

#### Comportamentos Implícitos

- Quando usuário delega aprovação, a tela não atualiza automaticamente (precisa F5)
- Grid mostra apenas 50 registros por vez (limitação hardcoded)
- Não há indicador visual de SLA próximo de vencer
- Não há separação de aprovações próprias vs delegadas

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Tela ASPX substituída por componente Angular 19 standalone com:
- Paginação server-side
- Filtros dinâmicos
- Indicadores visuais de SLA
- Real-time updates (SignalR)

---

### Tela: AprovacaoDetalhe.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Aprovacoes\AprovacaoDetalhe.aspx`
- **Responsabilidade:** Mostra detalhes de uma aprovação específica

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| lblDocumento | Label | Sim | Número do documento (NF, contrato, etc.) |
| lblAprovador | Label | Sim | Nome do aprovador principal |
| txtComentarios | TextBox | Não | Comentários da aprovação (max 500 caracteres) |
| btnAprovar | Button | Sim | Botão aprovar (postback) |
| btnRejeitar | Button | Sim | Botão rejeitar (postback) |

#### Comportamentos Implícitos

- Ao aprovar, não há confirmação (ação irreversível sem modal)
- Ao rejeitar, motivo é opcional (deveria ser obrigatório)
- Não mostra histórico de aprovações anteriores
- Não mostra SLA ou deadline

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Tela ASPX substituída por tela Angular com:
- Modal de confirmação obrigatório
- Motivo de rejeição obrigatório
- Histórico de aprovações visível
- Indicador de deadline com countdown

---

### Tela: DelegacaoGerenciar.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Aprovacoes\DelegacaoGerenciar.aspx`
- **Responsabilidade:** Gerencia delegações de aprovador

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| ddlDelegado | DropDownList | Sim | Usuário para quem delegar |
| txtDataInicio | TextBox (Date) | Sim | Data início delegação |
| txtDataFim | TextBox (Date) | Sim | Data fim delegação |
| txtMotivo | TextBox | Não | Motivo delegação (deveria ser obrigatório) |
| btnCriar | Button | Sim | Criar delegação |

#### Comportamentos Implícitos

- Permite criar delegação com data fim no passado (bug)
- Não valida se aprovador já tem delegação ativa
- Não envia notificação ao delegado
- Delegação não expira automaticamente (precisa revogar manualmente)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Tela ASPX substituída por tela Angular com:
- Validação de datas (data fim > data início, data fim > hoje)
- Validação de delegação duplicada
- Notificação automática ao delegado
- Expiração automática de delegação

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSAprovacoes.asmx.vb

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\WebService\WSAprovacoes.asmx.vb`
- **Responsabilidade:** Expor métodos SOAP para aprovações

| Método | Responsabilidade | Observações | DESTINO |
|--------|------------------|-------------|---------|
| `ListarPendentes(idUsuario)` | Retorna aprovações pendentes do usuário | Retorna DataTable serializado (XML), sem paginação | **SUBSTITUÍDO** por `GET /api/approvals?status=pending` |
| `Aprovar(idAprovacao, comentario)` | Aprova um documento | Não valida se usuário tem permissão (apenas se é aprovador) | **SUBSTITUÍDO** por `POST /api/approvals/{id}/approve` |
| `Rejeitar(idAprovacao, motivo)` | Rejeita um documento | Motivo opcional (deveria ser obrigatório) | **SUBSTITUÍDO** por `POST /api/approvals/{id}/reject` |
| `CriarDelegacao(idAprovador, idDelegado, dataFim)` | Cria delegação | Não registra IP ou UserAgent na auditoria | **SUBSTITUÍDO** por `POST /api/delegations` |

**Justificativa da Substituição:**
- SOAP → REST API (JSON)
- Sem validação RBAC → com Policy dinâmica
- Sem auditoria completa → auditoria 7 anos LGPD
- Sem paginação → paginação server-side

---

## 4. TABELAS LEGADAS

### Tabela: tblAprovacoes

**Schema**: `[dbo].[tblAprovacoes]`

**Finalidade**: Armazenar aprovações de documentos

**DDL Legado**:
```sql
CREATE TABLE [dbo].[tblAprovacoes](
    [IdAprovacao] [int] IDENTITY(1,1) NOT NULL,
    [IdConglomerado] [int] NOT NULL,
    [IdDocumento] [int] NOT NULL,
    [TipoDocumento] [varchar](50) NOT NULL,
    [IdAprovadorPrincipal] [int] NOT NULL,
    [IdAprovadorSecundario] [int] NULL,
    [DataCriacao] [datetime] NOT NULL,
    [DataAprovacao] [datetime] NULL,
    [DataRejeicao] [datetime] NULL,
    [StatusAprovacao] [varchar](20) NOT NULL,
    [MotivoRejeicao] [varchar](500) NULL,
    [IpAddress] [varchar](15) NOT NULL,
    [Observacoes] [text] NULL,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Dt_Alteracao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    CONSTRAINT [PK_tblAprovacoes] PRIMARY KEY CLUSTERED ([IdAprovacao] ASC)
)
```

**Problemas Identificados**:
- Falta FK para validar `IdDocumento` (dados órfãos)
- Não tem campos de auditoria completos (CreatedBy, LastModifiedBy ausentes)
- IpAddress VARCHAR(15) não suporta IPv6 (limitação)
- Observacoes como TEXT (deveria ser NVARCHAR(MAX))
- Fl_Excluido é soft delete simples (não tem DeletedBy ou DeletedAt)
- StatusAprovacao é VARCHAR (deveria ser INT com enum)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Tabela redesenhada como `ApprovalInstance` com:
- FKs obrigatórias
- Auditoria completa (Created, CreatedBy, LastModified, LastModifiedBy)
- IpAddress VARCHAR(45) para IPv6
- Comments como NVARCHAR(MAX)
- Soft delete completo (DeletedBy, DeletedAt, DeletedReason)
- Status como INT com enum

**Rastreabilidade:**
- RF Moderno: RF-088 - Seção 6 (Estados da Entidade)
- MD Moderno: MD-RF088.md - Tabela ApprovalInstance
- Migration EF Core: `20251231_CreateApprovalInstanceTable.cs`

---

### Tabela: tblDelegacoes

**Schema**: `[dbo].[tblDelegacoes]`

**Finalidade**: Armazenar delegações de aprovação

**DDL Legado**:
```sql
CREATE TABLE [dbo].[tblDelegacoes](
    [IdDelegacao] [int] IDENTITY(1,1) NOT NULL,
    [IdAprovador] [int] NOT NULL,
    [IdDelegado] [int] NOT NULL,
    [DataInicio] [datetime] NOT NULL,
    [DataFim] [datetime] NOT NULL,
    [Motivo] [varchar](255) NULL,
    [StatusDelegacao] [varchar](20) NOT NULL,
    CONSTRAINT [PK_tblDelegacoes] PRIMARY KEY CLUSTERED ([IdDelegacao] ASC)
)
```

**Problemas Identificados**:
- Não tem auditoria (quem criou, quando criou)
- Não registra IP de criação
- StatusDelegacao é VARCHAR (deveria ser INT enum)
- Falta campo para indicar se delegação foi revogada manualmente
- Não tem ExpiresAt automático (precisa job para checar DataFim)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Tabela redesenhada como `ApprovalDelegation` com:
- Campos de auditoria obrigatórios (CreatedBy, CreatedAt, IpAddress)
- Status como enum (Active, Expired, Revoked)
- Campo RevokedAt, RevokedBy, RevocationReason
- Expiração automática via background job

**Rastreabilidade:**
- RF Moderno: RF-088 - Seção 5 (Regras de Negócio - RN-RF088-004)
- MD Moderno: MD-RF088.md - Tabela ApprovalDelegation

---

## 5. STORED PROCEDURES LEGADAS

### Procedure: pa_AprovacaoInserir

**Caminho:** Banco de Dados SQL Server

**Responsabilidade:** Cria nova aprovação

**Lógica (em linguagem natural, SEM copiar SQL)**:
1. Valida se documento existe
2. Valida se aprovador existe e está ativo
3. Insere registro em tblAprovacoes com status "Pendente"
4. (NÃO envia notificação automática - processo separado)
5. Retorna ID da aprovação criada

**Problemas**:
- Não valida permissão RBAC (apenas se usuário está ativo)
- Não registra auditoria estruturada (apenas INSERT)
- Não calcula SLA automaticamente (precisa configurar manualmente)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Lógica movida para Application Layer (CQRS Handler):
- `CreateApprovalCommand`
- `CreateApprovalCommandHandler`
- `CreateApprovalCommandValidator` (FluentValidation)

**Rastreabilidade:**
- RF Moderno: RF-088 - Seção 5 (Regras de Negócio)
- Handler: `CreateApprovalCommandHandler.cs`

---

### Procedure: pa_AprovacaoAtualizar

**Caminho:** Banco de Dados SQL Server

**Responsabilidade:** Atualiza status de aprovação

**Lógica (em linguagem natural)**:
1. Valida se aprovação existe
2. Atualiza StatusAprovacao (Pendente → Aprovado ou Rejeitado)
3. Atualiza DataAprovacao ou DataRejeicao
4. Atualiza MotivoRejeicao (se rejeição)
5. (NÃO dispara notificação ao requisitante - processo separado)

**Problemas**:
- Permite atualizar aprovação já finalizada (deveria bloquear)
- Não valida se usuário atual é o aprovador
- Não registra IP ou UserAgent
- Sobrescreve DataAprovacao anterior (perde histórico)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Lógica movida para Commands separados:
- `ApproveCommand` + `ApproveCommandHandler`
- `RejectCommand` + `RejectCommandHandler`
- Validação de estado final (RN-RF088-007)
- Auditoria imutável (RN-RF088-010)

---

### Procedure: pa_DelegacaoInserir

**Caminho:** Banco de Dados SQL Server

**Responsabilidade:** Cria delegação de aprovador

**Lógica (em linguagem natural)**:
1. Valida se aprovador e delegado existem
2. Valida se DataFim > DataInicio
3. Insere registro em tblDelegacoes com status "Ativa"
4. (NÃO notifica delegado - processo separado)

**Problemas**:
- Não valida se DataFim é no futuro (permite datas no passado)
- Permite criar delegação duplicada (aprovador já tem delegação ativa)
- Não registra auditoria completa
- Não envia notificação ao delegado

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Lógica movida para:
- `CreateDelegationCommand`
- `CreateDelegationCommandHandler`
- `CreateDelegationCommandValidator` (validações completas)
- Notificação automática ao delegado

---

### Procedure: pa_ListarPendentes

**Caminho:** Banco de Dados SQL Server

**Responsabilidade:** Lista aprovações pendentes de um usuário

**Lógica (em linguagem natural)**:
1. Busca aprovações com StatusAprovacao = 'Pendente'
2. Filtra por IdAprovadorPrincipal = @IdUsuario
3. Retorna DataTable com todas as colunas
4. (NÃO faz paginação - retorna todas)

**Problemas**:
- Sem paginação (pode retornar milhares de registros)
- Query não otimizada (sem índices específicos)
- Não considera delegações ativas (só aprovador original)
- Retorna todas as colunas (deveria projetar apenas necessárias)

**DESTINO:** SUBSTITUÍDO

**Justificativa:** Lógica movida para:
- `GetPendingApprovalsQuery`
- `GetPendingApprovalsQueryHandler`
- Paginação server-side (PaginatedList)
- Considera delegações ativas
- Projection otimizada (apenas campos necessários)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Estas regras NÃO estavam documentadas formalmente, mas foram descobertas no código VB.NET ou stored procedures.

- **RL-RN-001**: Aprovador secundário só entra em ação se aprovador principal não responder em 48h (SLA hardcoded)
  - **Localização**: `AprovacaoDetalhe.aspx.vb` - Linha 142
  - **DESTINO**: SUBSTITUÍDO por SLA configurável (RN-RF088-005)

- **RL-RN-002**: Rejeição permite comentários opcionais, mas motivo não é obrigatório
  - **Localização**: `pa_AprovacaoAtualizar` - Stored Procedure
  - **DESTINO**: CORRIGIDO - Motivo obrigatório em rejeição (RN-RF088-009)

- **RL-RN-003**: Delegação não expira automaticamente; precisa job SQL noturno para marcar como "Expirada"
  - **Localização**: Job SQL Server `JobDelegacaoExpiracao`
  - **DESTINO**: SUBSTITUÍDO por background service .NET com execução a cada hora

- **RL-RN-004**: Aprovador pode aprovar qualquer documento, mesmo de outro conglomerado (falha multi-tenant)
  - **Localização**: `WSAprovacoes.asmx.vb` - Método `Aprovar()` - Linha 89
  - **DESTINO**: CORRIGIDO - Validação de EmpresaId obrigatória (RN-RF088-006)

- **RL-RN-005**: Histórico de aprovação é sobrescrito a cada mudança de status (perde before/after)
  - **Localização**: `pa_AprovacaoAtualizar` - UPDATE direto
  - **DESTINO**: SUBSTITUÍDO por tabela AuditAprovacao imutável (RN-RF088-010)

- **RL-RN-006**: Notificações de e-mail não incluem link direto para aprovação (usuário precisa navegar manualmente)
  - **Localização**: `EmailService.vb` - Método `EnviarNotificacao()`
  - **DESTINO**: CORRIGIDO - Notificações incluem link direto (RN-RF088-008)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Designer de Workflow** | Não existe; workflows são hardcoded em SPs | Designer visual drag-and-drop no Angular com preview em tempo real | Gap crítico - motivação principal da refatoração |
| **Estados** | Codificados em enums na aplicação | Completamente configuráveis em banco de dados, sem redeployment | Flexibilidade 100x maior |
| **Notificações** | E-mail via SMTP simples, sem templates | Multi-canal: e-mail (Handlebars), SMS, push in-app com template engine | Melhoria de UX significativa |
| **SLA** | Alertas manuais por job SQL (noturno) | Automáticos com escalação, re-notificação e dashboard de SLA compliance (job a cada hora) | Compliance > 95% garantido |
| **Aprovação Paralela** | Não suportada | Nativa: 2 de 3 aprovadores, todos devem aprovar, qualquer um rejeita | Funcionalidade nova |
| **Delegação** | Transferência manual de permissões | Delegação com data de expiração, com auditoria e reversão automática | Compliance LGPD |
| **Auditoria** | Logs básicos em tabela TEXT | Tabela de auditoria estruturada com before/after de cada campo (JSON) | Conformidade LGPD 100% |
| **Histórico** | Sobrescrito a cada mudança | Tabela separada (AuditAprovacao) com retenção de 7 anos | Rastreabilidade total |
| **Performance** | Queries lentas com JOINs múltiplos | Otimizado com índices, cache distribuído, materialização de histórico | Latência < 500ms garantida |
| **i18n** | Textos hardcoded em português | Labels e mensagens 100% traduzíveis (pt-BR, en-US, es-ES) | Escalabilidade internacional |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir SOAP por REST API

**Motivo**: SOAP é verboso, lento e difícil de consumir por frontends modernos (Angular). REST API com JSON é padrão atual.

**Impacto**: Médio - requer adaptação de integrações externas (se houver)

---

### Decisão 2: Migrar workflows de Enums hardcoded para tabela configurável

**Motivo**: Qualquer mudança de workflow no legado requer redeployment. Com tabela, admin pode configurar via UI sem tocar em código.

**Impacto**: Alto - arquitetura completamente diferente, mas ganho de flexibilidade compensa

---

### Decisão 3: Criar tabela AuditAprovacao separada (imutável)

**Motivo**: Legado sobrescreve histórico. LGPD exige rastreabilidade de 7 anos. Tabela separada garante imutabilidade.

**Impacto**: Baixo - apenas adiciona tabela nova, sem breaking changes

---

### Decisão 4: Implementar SLA com escalação automática (background service)

**Motivo**: Legado depende de job SQL noturno (SLA pode vencer e ninguém sabe até dia seguinte). Background service .NET executa a cada hora.

**Impacto**: Alto - melhoria crítica de compliance

---

### Decisão 5: Substituir multi-database por multi-tenancy com Row-Level Security

**Motivo**: Legado tem um banco por cliente (complexidade operacional). Multi-tenancy unifica banco, simplifica backup e permite escalar horizontalmente.

**Impacto**: Crítico - migração de dados complexa, mas essencial para escalabilidade

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados durante migração de multi-database → single database** | Crítico | Script de migração com validação + backup completo antes de executar |
| **Integrações externas quebrarem (se existirem consumidores SOAP)** | Alto | Criar adapter layer (SOAP wrapper sobre REST API) durante período de transição |
| **Usuários não saberem usar designer visual de workflows** | Médio | Treinamento obrigatório + vídeos tutoriais + templates prontos |
| **Performance de queries degradar com single database** | Médio | Índices otimizados + cache distribuído + materialização de histórico |
| **Delegações ativas no legado não migrarem corretamente** | Médio | Script de migração específico para delegações + validação de datas |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|-----------------|-----------------------|
| `tblAprovacoes` | MD-RF088.md - Tabela `ApprovalInstance` |
| `tblDelegacoes` | MD-RF088.md - Tabela `ApprovalDelegation` |
| `pa_AprovacaoInserir` | `CreateApprovalCommandHandler.cs` |
| `pa_AprovacaoAtualizar` | `ApproveCommandHandler.cs`, `RejectCommandHandler.cs` |
| `pa_DelegacaoInserir` | `CreateDelegationCommandHandler.cs` |
| `pa_ListarPendentes` | `GetPendingApprovalsQueryHandler.cs` |
| `AprovacaoListar.aspx` | `/workflows/approvals` (Angular standalone component) |
| `AprovacaoDetalhe.aspx` | `/workflows/approvals/:id` (Angular) |
| `DelegacaoGerenciar.aspx` | `/workflows/delegations` (Angular) |
| `WSAprovacoes.asmx.vb` | REST API `/api/approvals`, `/api/delegations` |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Criação do RL-RF088 - Referência ao Legado de Aprovações e Workflows | Claude Code - Migração |

---

**Última Atualização**: 2025-12-31
**Status**: Completo
**Próximo**: Criar RL-RF088.yaml (rastreabilidade estruturada 100% com destinos)

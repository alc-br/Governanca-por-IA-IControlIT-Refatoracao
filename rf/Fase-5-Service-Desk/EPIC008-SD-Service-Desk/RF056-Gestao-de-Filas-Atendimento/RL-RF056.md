# RL-RF056 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF056 - Gestão de Filas de Atendimento
**Sistema Legado:** IControlIT v1.0 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do sistema legado de filas de atendimento que serve de base para a modernização, garantindo rastreabilidade e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral
- **Arquitetura:** Monolítica - ASP.NET Web Forms
- **Linguagem/Stack:** VB.NET, ASP.NET 4.5, SQL Server
- **Banco de Dados:** SQL Server (multi-database, um por cliente)
- **Multi-tenant:** Não (bancos separados por cliente)
- **Auditoria:** Inexistente
- **Configurações:** Web.config, tabelas de configuração no banco

### Problemas Arquiteturais Identificados

1. **Ausência de Sistema de Filas Formais**
   - Não havia gerenciamento automático de filas
   - Atendentes escolhiam solicitações manualmente
   - Sem priorização automática ou balanceamento

2. **Distribuição Manual e Ineficiente**
   - Supervisor atribuía solicitações manualmente via interface
   - Atendentes mais rápidos pegavam mais solicitações, sobrecarregando-se
   - Sem validação de skills ou competências técnicas

3. **Falta de Métricas em Tempo Real**
   - Relatórios gerados apenas via SQL Server Reporting Services (offline)
   - Gestores não tinham visibilidade do estado atual das filas
   - Identificação de gargalos era reativa, não proativa

4. **SLA Calculado Manualmente**
   - Cálculo de SLA feito por stored procedures sem considerar pausas
   - Sem diferenciação entre tempo de atendimento e tempo de espera do cliente
   - Penalizava atendentes por pendências externas

5. **Status de Atendente Não Gerenciado**
   - Sem controle formal de disponibilidade
   - Atendentes recebiam notificações mesmo em pausa ou ausentes
   - Redistribuição manual em caso de ausência

---

## 2. TELAS DO LEGADO

### Tela: FilaAtendimento.aspx

**DESTINO:** SUBSTITUÍDO

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/FilaAtendimento.aspx`
- **Responsabilidade:** Visualizar solicitações pendentes de forma básica (lista simples)

#### Campos
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| GridSolicitacoes | GridView | - | Lista todas solicitações sem filtro de fila |
| DdlCategoria | DropDownList | Não | Filtro manual de categoria |
| BtnAtribuir | Button | - | Atribuição manual pelo supervisor |
| LblTotalFila | Label | - | Contador simples (sem atualização automática) |

#### Comportamentos Implícitos
- Sem ordenação automática por prioridade ou SLA
- Sem refresh automático (usuário precisa F5)
- Atribuição manual obriga supervisor a conhecer skills dos atendentes
- Sem validação de carga de trabalho do atendente

---

### Tela: AtendimentoSolicitacao.aspx

**DESTINO:** SUBSTITUÍDO

- **Caminho:** `ic1_legado/IControlIT/ServiceDesk/AtendimentoSolicitacao.aspx`
- **Responsabilidade:** Interface de atendimento individual

#### Comportamentos Implícitos
- Atendente precisa "puxar" solicitação manualmente da lista
- Sem notificação quando nova solicitação entra na fila
- Transferência entre atendentes sem validação de skill
- Histórico de transferências não era registrado

---

### Tela: RelatorioFilas.aspx

**DESTINO:** SUBSTITUÍDO

- **Caminho:** `ic1_legado/IControlIT/Relatorios/RelatorioFilas.aspx`
- **Responsabilidade:** Relatório estático de produtividade

#### Comportamentos Implícitos
- Gerado sob demanda via SQL Server Reporting Services (SSRS)
- Sem visualização em tempo real
- Exportação apenas em PDF
- Dados consolidados diários, sem drill-down

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Webservice: ServiceDeskService.asmx

**DESTINO:** SUBSTITUÍDO

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| ObterSolicitacoesPendentes() | Retornar lista de solicitações sem atendente | Sem parâmetros de filtro, retorna todas |
| AtribuirSolicitacao(idSolicitacao, idAtendente) | Atribuir manualmente | Sem validação de skill ou carga |
| ObterMetricasGerais() | Retornar contadores básicos | Cache de 15 minutos, dados desatualizados |

**DESTINO:** Substituído por REST API com CQRS (Queries e Commands separados)

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| tbl_Solicitacoes | Armazenar solicitações | Sem campo de prioridade automática, sem SLA calculado |
| tbl_Atendentes | Cadastro de atendentes | Sem campo de status (disponível/pausa), sem skills formais |
| tbl_TransferenciasSolicitacao | Histórico de transferências | Tabela existia mas raramente usada, sem motivo obrigatório |
| tbl_HistoricoAtendimento | Log de atendimentos | Sem timestamps precisos, sem auditoria de quem alterou |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Priorização Manual
- **Fonte:** Code-behind `FilaAtendimento.aspx.vb - Linha 145`
- **Descrição:** Supervisor ordenava solicitações arrastando linhas do GridView manualmente
- **DESTINO:** SUBSTITUÍDO por algoritmo automático de priorização (RN-RF056-001)

### RL-RN-002: Limite Informal de Atendimentos
- **Fonte:** Convenção não documentada
- **Descrição:** Atendentes "sabiam" que não deveriam pegar mais de 5 solicitações, mas sistema não validava
- **DESTINO:** ASSUMIDO e formalizado como RN-RF056-005 (validação hard-coded)

### RL-RN-003: Escalação Manual para Supervisor
- **Fonte:** Processo manual via e-mail
- **Descrição:** Atendente enviava e-mail para supervisor quando não conseguia resolver
- **DESTINO:** SUBSTITUÍDO por escalação automática após 30 minutos (RN-RF056-004)

### RL-RN-004: Pausa de Almoço Manual
- **Fonte:** Processo organizacional
- **Descrição:** Atendentes alteravam status manualmente no sistema de presença (externo)
- **DESTINO:** ASSUMIDO e automatizado (RN-RF056-007)

### RL-RN-005: VIP Identificado por Comentário
- **Fonte:** Code-behind `AtendimentoSolicitacao.aspx.vb - Linha 89`
- **Descrição:** Campo "Observações" continha texto "[VIP]" se solicitante fosse diretor
- **DESTINO:** SUBSTITUÍDO por flag booleano e priorização automática (RN-RF056-010)

### RL-RN-006: Redistribuição Manual em Ausência
- **Fonte:** Processo manual do supervisor
- **Descrição:** Supervisor executava stored procedure para mover solicitações quando atendente faltava
- **DESTINO:** SUBSTITUÍDO por redistribuição automática (RN-RF056-008)

### RL-RN-007: SLA Não Considerava Pendências Externas
- **Fonte:** Stored Procedure `sp_CalcularSLA`
- **Descrição:** SLA era calculado linearmente desde abertura até fechamento, penalizando atendente
- **DESTINO:** SUBSTITUÍDO por pausa de SLA em pendências externas (RN-RF056-014)

### RL-RN-008: Follow-up Não Automático
- **Fonte:** Processo manual
- **Descrição:** Solicitação reaberta ia para fila geral, não para atendente original
- **DESTINO:** SUBSTITUÍDO por retorno automático ao atendente original (RN-RF056-013)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| Sistema de Filas | Manual | Automático com priorização | Nova funcionalidade |
| Routing por Skills | Inexistente | Obrigatório | Nova funcionalidade |
| Balanceamento de Carga | Manual | Automático | Nova funcionalidade |
| Escalação | Manual via e-mail | Automática após 30 min | Melhoria significativa |
| Métricas em Tempo Real | Inexistente | SignalR a cada 30s | Nova funcionalidade |
| Status de Atendente | Não gerenciado | 4 estados formais | Nova funcionalidade |
| Pausas Automáticas | Manual | Automáticas (horários configuráveis) | Melhoria significativa |
| Redistribuição | Manual | Automática | Melhoria significativa |
| Priorização VIP | Manual (campo texto) | Automática (flag + cargo) | Melhoria significativa |
| SLA com Pausas | Não | Sim | Nova funcionalidade |
| Relatórios | SSRS offline | Dashboard em tempo real | Melhoria significativa |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Pull para Push
- **Descrição:** Sistema legado usava modelo "pull" (atendente escolhe solicitação). Sistema moderno usa modelo "push" (sistema atribui automaticamente).
- **Motivo:** Eliminar viés humano, garantir distribuição justa e balanceamento de carga.
- **Impacto:** ALTO - Mudança cultural significativa para atendentes.

### Decisão 2: Substituir Stored Procedures por CQRS
- **Descrição:** Lógica de negócio em stored procedures foi movida para Application Layer (Handlers).
- **Motivo:** Facilitar testes, versionamento e manutenção.
- **Impacto:** MÉDIO - Requer treinamento da equipe em Clean Architecture.

### Decisão 3: Implementar SignalR para Tempo Real
- **Descrição:** Substituir polling/refresh manual por push via SignalR.
- **Motivo:** Melhorar experiência do usuário e reduzir carga no servidor.
- **Impacto:** MÉDIO - Infraestrutura precisa suportar WebSockets.

### Decisão 4: Multi-Tenancy com Row-Level Security
- **Descrição:** Consolidar múltiplos bancos SQL Server em banco único com EmpresaId.
- **Motivo:** Reduzir custos de infraestrutura e simplificar manutenção.
- **Impacto:** ALTO - Migração de dados complexa.

### Decisão 5: Soft Delete Obrigatório
- **Descrição:** Substituir exclusão física por soft delete (flag Deleted).
- **Motivo:** Garantir rastreabilidade e possibilitar auditoria histórica.
- **Impacto:** BAIXO - Padrão já adotado em outros módulos.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| Resistência à mudança cultural (pull → push) | ALTO | Treinamento intensivo, período de adaptação com modo híbrido opcional |
| Perda de dados históricos na migração | MÉDIO | ETL robusto com validação de integridade, rollback plan |
| Performance do SignalR com muitos usuários simultâneos | MÉDIO | Load testing, infraestrutura escalável (Azure SignalR Service) |
| Bugs no algoritmo de priorização | MÉDIO | Testes automatizados extensivos (TC-RF056), monitoramento em produção |
| Escalação automática prematura | BAIXO | Configuração de threshold ajustável por empresa |
| Dependência de Hangfire para jobs críticos | MÉDIO | Monitoramento de saúde do Hangfire, alertas em caso de falha |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Referência UC | Status |
|-----------------|---------------|---------------|--------|
| FilaAtendimento.aspx | RN-RF056-001, RN-RF056-009 | UC00-Listar-Filas | Migrado |
| AtendimentoSolicitacao.aspx | RN-RF056-002, RN-RF056-011 | UC03-Transferir-Solicitacao | Migrado |
| ServiceDeskService.asmx | RN-RF056-002, RN-RF056-003 | UC01-Distribuir-Solicitacao | Migrado |
| RelatorioFilas.aspx | RN-RF056-015 | UC04-Visualizar-Metricas | Migrado |
| sp_CalcularSLA | RN-RF056-014 | - | Migrado |
| tbl_Solicitacoes | Entidade Solicitacao (MD-RF056) | - | Migrado |
| tbl_Atendentes | Entidade Atendente (MD-RF056) | - | Migrado |
| tbl_TransferenciasSolicitacao | Entidade TransferenciaSolicitacao (MD-RF056) | - | Migrado |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado do sistema de filas | Agência ALC - alc.dev.br |

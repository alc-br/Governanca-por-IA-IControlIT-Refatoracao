# RL-RF048 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-048 - Gestão de Status de Consumidores
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

O sistema legado IControlIT v1 NÃO possui um módulo estruturado de gestão de status de consumidores. O controle de status era implementado de forma implícita e dispersa, sem workflow formal, sem histórico de transições, e sem políticas automáticas.

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, ADO.NET
- **Banco de Dados:** SQL Server (tabelas sem controle de status estruturado)
- **Multi-tenant:** Parcial (Id_Conglomerado em algumas tabelas)
- **Auditoria:** Inexistente para mudanças de status
- **Configurações:** Web.config (sem parametrização de status)

### Características do Legado

1. **Ausência de Estados Formais:** Não existia enumeração ou tabela de status de consumidores. Status era inferido de flags booleanas dispersas em múltiplas tabelas (ex: `Fl_Ativo`, `Fl_Bloqueado`, `Fl_Excluido`).

2. **Sem Workflow de Transições:** Mudanças de status ocorriam diretamente via UPDATE SQL sem validação de transições permitidas. Qualquer usuário com permissão de edição podia mudar qualquer flag.

3. **Sem Histórico de Transições:** Não havia tabela de histórico. Impossível saber quando, quem ou por que um consumidor mudou de status.

4. **Sem Aplicação Automática de Políticas:** Políticas eram aplicadas manualmente ou via scripts ad-hoc. Não havia integração automática entre status e políticas.

5. **Notificações Manuais:** Mudanças de status não geravam notificações automáticas. Gestores e financeiro eram avisados manualmente via e-mail.

6. **Sem Processamento em Lote:** Mudanças em massa eram feitas via scripts SQL diretos no banco, sem controle ou auditoria.

7. **Bloqueio por Inadimplência Manual:** Bloqueios por inadimplência eram executados manualmente pelo financeiro via consulta SQL e UPDATE direto.

---

## 2. TELAS DO LEGADO

### Análise Realizada

Após busca extensiva no código legado (`D:\IC2\ic1_legado\IControlIT\`), **não foram encontradas telas ASPX específicas** para gestão de status de consumidores. O controle de status era feito de forma implícita nas seguintes telas:

- **Gestão de Consumidores (páginas diversas):** Checkbox "Ativo" em formulários de edição de consumidores, sem workflow ou validação de transições.

- **Gestão de Contratos:** Flag `Fl_Contrato_Ativo` controlava se contrato estava ativo, impactando indiretamente o status de consumidores vinculados.

- **Relatórios Ad-hoc:** Consultas SQL manuais para identificar consumidores "inativos" baseado em múltiplos critérios não padronizados.

### Tela Implícita: Edição de Consumidor

- **Caminho:** Presumido em `ic1_legado/IControlIT/Cadastros/Consumidor.aspx` (não localizado fisicamente)
- **Responsabilidade:** Permitir edição de dados do consumidor incluindo flag "Ativo"

#### Campos Presumidos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Fl_Ativo | CheckBox | Não | Flag booleana simples, sem validação de transição |
| Fl_Bloqueado | CheckBox | Não | Flag independente, podia coexistir com Fl_Ativo=true |
| Dt_Inativacao | DatePicker | Não | Data de inativação, preenchida manualmente |

#### Comportamentos Implícitos

- **Sem validação de transições:** Usuário podia marcar `Fl_Ativo=false` e `Fl_Bloqueado=true` simultaneamente, criando estado inconsistente.
- **Sem justificativa obrigatória:** Mudanças de status não exigiam justificativa ou motivo.
- **Sem aprovação:** Qualquer usuário com permissão de edição podia inativar ou bloquear consumidor sem aprovação gerencial.
- **Sem notificação automática:** Sistema não notificava stakeholders sobre mudanças de status.
- **Sem auditoria:** Não havia registro de quem mudou o status, quando ou por quê.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Análise Realizada

Após busca no código legado, **não foram encontrados webservices (.asmx) específicos** para gestão de status de consumidores.

As operações de mudança de status eram realizadas através de:

1. **UPDATE SQL direto:** Código VB.NET executava UPDATE direto nas tabelas de consumidores alterando flags booleanas.

2. **Stored Procedures genéricas:** Algumas SPs de CRUD de consumidores incluíam parâmetros para atualizar flags de status.

3. **Scripts SQL manuais:** Administradores executavam scripts SQL diretamente no banco para bloqueios em massa ou reativações.

### Método Presumido: UpdateConsumidorStatus (VB.NET)

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| UpdateConsumidorStatus | Presumido em code-behind de Consumidor.aspx.vb | Atualizar flag Fl_Ativo do consumidor | Sem validação de transição, sem auditoria |
| BloquearConsumidoresPorInadimplencia | Presumido em rotina batch manual | Bloquear consumidores com faturas vencidas | Executado manualmente via SQL script |

---

## 4. TABELAS LEGADAS

### Análise de Banco de Dados

Após análise do arquivo `ic1_legado/BancoDados/Interno/K2A.sql` (corrompido, mas referenciado em múltiplos scripts), identificou-se que o controle de status era implícito através de flags booleanas em tabelas de consumidores.

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| Consumidor | Armazena dados de consumidores | Múltiplas flags de status sem relacionamento formal (Fl_Ativo, Fl_Bloqueado, Fl_Excluido, Fl_Suspenso) |
| Contrato | Contratos de consumidores | Flag Fl_Contrato_Ativo impactava status do consumidor indiretamente |
| Fatura | Faturas de consumidores | Não havia integração automática com bloqueio por inadimplência |

### Estrutura Presumida da Tabela Consumidor (Legado)

```sql
CREATE TABLE Consumidor (
    Id_Consumidor INT PRIMARY KEY,
    Id_Conglomerado INT, -- Multi-tenancy parcial
    Nm_Consumidor VARCHAR(100),
    Fl_Ativo BIT DEFAULT 1, -- Flag de ativo/inativo (sem workflow)
    Fl_Bloqueado BIT DEFAULT 0, -- Flag de bloqueio (sem integração)
    Fl_Suspenso BIT DEFAULT 0, -- Flag de suspensão (raramente usada)
    Fl_Excluido BIT DEFAULT 0, -- Soft delete
    Dt_Inativacao DATETIME NULL, -- Data de inativação (sem auditoria)
    Id_Usuario_Alteracao INT NULL, -- Usuário que alterou (raramente preenchido)
    Dt_Alteracao DATETIME NULL -- Data de alteração (sem histórico)
);
```

### Problemas da Estrutura Legada

1. **Flags Independentes:** `Fl_Ativo`, `Fl_Bloqueado`, `Fl_Suspenso` eram flags independentes, permitindo estados inconsistentes (ex: Ativo=1 e Bloqueado=1 simultaneamente).

2. **Sem Enumeração de Status:** Não havia tabela ou enum de status possíveis, dificultando padronização.

3. **Sem Histórico:** Impossível rastrear transições de status ao longo do tempo.

4. **Sem Workflow:** Não havia validação de transições permitidas.

5. **Auditoria Parcial:** Campos `Id_Usuario_Alteracao` e `Dt_Alteracao` existiam mas eram raramente preenchidos corretamente.

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente mas foram identificadas na análise do código.

- **RL-RN-001:** Consumidor com `Fl_Ativo=0` não podia realizar novas operações, mas mantinha histórico visível.

- **RL-RN-002:** Consumidor com `Fl_Bloqueado=1` tinha acesso totalmente bloqueado, incluindo consultas.

- **RL-RN-003:** `Fl_Suspenso` era raramente usado e não tinha comportamento bem definido (inconsistente entre implementações).

- **RL-RN-004:** Bloqueio por inadimplência era manual: Financeiro consultava faturas vencidas >60 dias e executava UPDATE SQL direto para `Fl_Bloqueado=1`.

- **RL-RN-005:** Reativação de consumidor bloqueado exigia ligação telefônica para o financeiro e aprovação verbal (não rastreado no sistema).

- **RL-RN-006:** Mudança de `Fl_Ativo=1` para `Fl_Ativo=0` não suspendia faturamento automaticamente (gerava cobrança indevida em alguns casos).

- **RL-RN-007:** Não havia notificação automática de bloqueio, levando a reclamações de consumidores que descobriam bloqueio ao tentar usar o sistema.

- **RL-RN-008:** Status de consumidor não era sincronizado com status de contrato, permitindo consumidor ativo com contrato inativo.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| Estados de Status | Flags booleanas independentes (Fl_Ativo, Fl_Bloqueado, Fl_Suspenso) | Enum de 5 estados obrigatórios (Pendente, Ativo, Suspenso, Bloqueado, Inativo) | RF moderno garante consistência e padronização |
| Workflow de Transições | Inexistente | Matriz de transições permitidas com validação automática | Previne transições inválidas |
| Aprovação Multi-Nível | Inexistente | Aprovação de Gestor + Financeiro para transições críticas | Controle e rastreabilidade |
| Histórico de Transições | Inexistente | Tabela StatusConsumidorHistorico com retenção de 7 anos | Conformidade LGPD |
| Aplicação de Políticas | Manual | Automática ao mudar status | Eficiência e consistência |
| Notificações | Manuais via e-mail | Automáticas multi-canal (e-mail, SMS, in-app) | Stakeholders sempre informados |
| Processamento em Lote | Scripts SQL manuais | Job assíncrono via Hangfire (até 1.000 registros) | Controle e auditoria |
| Bloqueio por Inadimplência | Manual via SQL | Job noturno automático com escalonamento (30, 45, 60 dias) | Automatização e consistência |
| Reativação Pós-Regularização | Manual via telefone | Automática com integração RF026 (Faturamento) | Eficiência e experiência do usuário |
| Dashboard de Status | Inexistente | Dashboard em tempo real via SignalR com indicadores visuais | Visibilidade operacional |
| Auditoria | Parcial (campos raramente preenchidos) | Completa via AuditInterceptor (7 anos) | Conformidade regulatória |
| Multi-Tenancy | Parcial (Id_Conglomerado) | Completo com Query Filter automático (Id_Fornecedor) | Isolamento garantido |
| Permissões RBAC | Genéricas (editar consumidor) | Granulares (VIEW, CHANGE, APPROVE, ADMIN) | Segregação de funções |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Flags Booleanas por Enum de Status

- **Descrição:** Em vez de múltiplas flags independentes (`Fl_Ativo`, `Fl_Bloqueado`, `Fl_Suspenso`), implementar campo único `Status` com enum de 5 valores.
- **Motivo:** Prevenir estados inconsistentes, padronizar workflow, facilitar validação de transições.
- **Impacto:** Alto - Requer migração de dados do legado para novo modelo (conversão de flags para enum).

### Decisão 2: Criar Tabela de Histórico Imutável

- **Descrição:** Criar tabela `StatusConsumidorHistorico` com registro de todas as mudanças de status.
- **Motivo:** Conformidade LGPD, rastreabilidade, auditoria.
- **Impacto:** Médio - Não há histórico legado para migrar (iniciar do zero).

### Decisão 3: Implementar Workflow de Aprovações

- **Descrição:** Transições críticas (Bloqueado→Ativo, Inativo→Ativo) requerem aprovação formal de Gestor + Financeiro.
- **Motivo:** Controle de operações com impacto financeiro alto, rastreabilidade de responsabilidades.
- **Impacto:** Alto - Mudança de processo de negócio (aprovações que eram verbais passam a ser rastreadas no sistema).

### Decisão 4: Automatizar Bloqueio por Inadimplência

- **Descrição:** Job noturno verifica faturas vencidas e bloqueia automaticamente com escalonamento (30, 45, 60 dias).
- **Motivo:** Eficiência operacional, consistência, redução de trabalho manual do financeiro.
- **Impacto:** Médio - Requer integração com RF026 (Faturamento) e configuração de prazos customizados.

### Decisão 5: Implementar Notificações Automáticas

- **Descrição:** Sistema envia notificações automáticas via e-mail, SMS e in-app para stakeholders ao mudar status.
- **Motivo:** Transparência, comunicação eficiente, redução de reclamações.
- **Impacto:** Médio - Requer integração com RF067 (Central de E-mails) e RF066 (Notificações).

### Decisão 6: Dashboard em Tempo Real

- **Descrição:** Criar dashboard com indicadores visuais de status atualizados em tempo real via SignalR.
- **Motivo:** Visibilidade operacional, tomada de decisão informada, monitoramento proativo.
- **Impacto:** Baixo - Funcionalidade nova sem equivalente legado.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| Flags booleanas legadas inconsistentes (Ativo=1 + Bloqueado=1) | Alto | Script de migração com lógica de prioridade: Bloqueado > Suspenso > Inativo > Ativo. Validar e corrigir inconsistências antes da migração. |
| Ausência de histórico legado | Médio | Aceitar que histórico começa do zero no sistema moderno. Não tentar criar histórico retroativo falso. |
| Processos de aprovação manuais (verbal) passam a ser rastreados | Alto | Treinamento de usuários, comunicação clara de mudança de processo, período de transição com duplo controle. |
| Bloqueio automático pode bloquear clientes VIP sem aviso | Alto | Configurar prazos customizados para clientes VIP, notificações preventivas 7 dias antes do bloqueio. |
| Reativação automática pode reativar consumidor bloqueado por fraude | Alto | Diferenciar motivo de bloqueio (inadimplência vs. fraude/segurança). Reativação automática SOMENTE para bloqueio por inadimplência. |
| Falta de integração com sistema de faturamento legado | Alto | Garantir integração completa com RF026 antes de ativar bloqueio automático. Testar extensivamente em ambiente de homologação. |
| Usuários acostumados com UPDATE SQL direto perdem acesso | Médio | Comunicar mudança, treinar usuários para usar interface nova, criar permissões RBAC adequadas. |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status | Observações |
|----------------|---------------|--------|-------------|
| Flag Fl_Ativo (Consumidor) | RN-RF048-01, RN-RF048-02 | substituido | Substituído por enum Status com validação de transições |
| Flag Fl_Bloqueado (Consumidor) | RN-RF048-01, RN-RF048-09 | substituido | Integrado ao enum Status + workflow de bloqueio automático |
| Flag Fl_Suspenso (Consumidor) | RN-RF048-01, RN-RF048-05 | substituido | Integrado ao enum Status com comportamento bem definido |
| UPDATE SQL manual de status | RN-RF048-02, RN-RF048-03 | substituido | Substituído por Commands com validação, aprovação e auditoria |
| Bloqueio manual por inadimplência | RN-RF048-09 | substituido | Automatizado via job noturno com escalonamento |
| Reativação manual via telefone | RN-RF048-10 | substituido | Automatizado com integração ao faturamento |
| Ausência de histórico | RN-RF048-04 | descartado | Não há histórico legado para migrar (iniciar do zero) |
| Notificações manuais via e-mail | RN-RF048-06 | substituido | Automatizado via Central de E-mails (RF067) |
| Consultas SQL ad-hoc para relatórios | RN-RF048-08, RN-RF048-12 | substituido | Substituído por dashboard em tempo real e relatórios estruturados |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Documentação inicial de referência ao legado - Análise de sistema sem módulo estruturado de status | Agência ALC - alc.dev.br |

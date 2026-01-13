# PROCESSOS DE NEGÓCIO - ICONTROLIT MODERNIZADO

**Versão:** 2.0
**Autor:** ALC (alc.dev.br)
**Data:** 2026-01-12
**Status:** Vigente

---

## 1. VISÃO GERAL

### 1.1 Contexto da Modernização

O projeto IControlIT está passando por uma modernização arquitetural completa, migrando de um sistema legado baseado em 18 bancos de dados isolados (SQL Server) com VB.NET e ASP.NET WebForms para uma arquitetura moderna unificada com banco de dados único e multi-tenancy nativo.

**Arquitetura Legada:**
- 18 bancos de dados SQL Server isolados (1 por cliente)
- VB.NET + ASP.NET WebForms
- SOAP WebServices
- Stored Procedures para lógica de negócio
- Processos manuais e aprovações via e-mail
- Sem auditoria estruturada

**Arquitetura Moderna:**
- Banco de dados único com Row-Level Security (ClienteId)
- .NET 10 + C# 13
- Angular 19 + TypeScript 5.7
- Clean Architecture + CQRS
- REST APIs + SignalR
- Automações e workflows nativos
- Auditoria completa (7 anos de retenção)
- Multi-tenancy por design

### 1.2 Processos Reais Identificados

De um total de **110 Requisitos Funcionais (RFs)** documentados, foram identificados **38 processos reais de negócio**.

**Critérios de Identificação:**
- ✅ Processo possui workflow com múltiplas etapas
- ✅ Envolve automações, integrações ou state-machines
- ✅ Possui regras de negócio complexas
- ✅ Requer aprovações ou delegações
- ✅ Tem impacto em múltiplas entidades

**Excluídos:**
- ❌ 72 RFs que são cadastros simples (CRUD básico)
- ❌ Operações de consulta pura
- ❌ Endpoints de leitura sem lógica

### 1.3 Princípios Arquiteturais

**Clean Architecture:**
- Separação clara entre camadas (Domain, Application, Infrastructure, Presentation)
- Dependências sempre apontam para o Domain
- Regras de negócio isoladas de frameworks

**CQRS (Command Query Responsibility Segregation):**
- Commands: Operações que alteram estado
- Queries: Operações somente-leitura
- Handlers dedicados para cada operação

**Multi-Tenancy:**
- ClienteId obrigatório em todos os handlers
- Row-Level Security no banco de dados
- Isolamento completo de dados entre clientes

**Auditoria e Conformidade:**
- ISO 27001, SOC 2, LGPD, SOX
- Trilha de auditoria completa (quem, quando, o quê, por quê)
- Retenção de 7 anos
- Logs estruturados (Azure Application Insights)

---

## 2. ESTRUTURA DO DOCUMENTO

Este documento está organizado em **6 jornadas** que representam a ordem de execução dos processos no sistema:

### 2.1 Tabela de Jornadas

| Jornada | Título | Processos | Arquivo |
|---------|--------|-----------|---------|
| **Jornada 1** | Infraestrutura e Configuração | 8 processos | [01-Jornada-Infraestrutura.md](01-Jornada-Infraestrutura.md) |
| **Jornada 2** | Workflows e Importação | 9 processos | [02-Jornada-Workflows.md](02-Jornada-Workflows.md) |
| **Jornada 3** | Financeiro Completo | 12 processos | [03-Jornada-Financeiro.md](03-Jornada-Financeiro.md) |
| **Jornada 5** | Service Desk | 8 processos | [05-Jornada-Service-Desk.md](05-Jornada-Service-Desk.md) |
| **Jornada 6** | Auditoria e Integrações | 1 processo | [06-Jornada-Auditoria.md](06-Jornada-Auditoria.md) |
| **Visão Macro** | Integração Consolidada | - | [07-Visao-macro-consolidada.md](07-Visao-macro-consolidada.md) |
| **Anexos** | Glossário e Referências | - | [08-Anexos.md](08-Anexos.md) |

### 2.2 Códigos de Processos

Cada processo possui um código único no formato **PRO-XXX-YYY**:

- **PRO** = Processo
- **XXX** = Prefixo da área (3 letras)
- **YYY** = Número sequencial (001-999)

**Tabela de Prefixos:**

| Prefixo | Área | Descrição |
|---------|------|-----------|
| **INF** | Infraestrutura | Configurações, logs, autenticação, multi-tenancy |
| **WKF** | Workflows | Templates, notificações, importações, aprovações |
| **FCT** | Financeiro - Contratos/Faturamento | Contratos, faturas, medição, NF-e |
| **FAC** | Financeiro - Ativos/Custos | Ativos, custos fixos, TCO, rateio |
| **SVC** | Service Desk | SLA, chamados, solicitações, escalação |
| **AUD** | Auditoria | Inventário cíclico, auditoria de acesso |

---

## 3. PROCESSOS POR JORNADA

### 3.1 Jornada 1: Infraestrutura e Configuração (8 processos)

Processos de base que configuram o sistema para operação multi-tenant, logs, autenticação e internacionalização.

| Código | Processo | RF |
|--------|----------|-----|
| PRO-INF-001 | Parâmetros e Configurações | RF001 |
| PRO-INF-002 | Configurações Gerais | RF002 |
| PRO-INF-003 | Logs e Monitoramento | RF003 |
| PRO-INF-004 | Auditoria de Operações | RF004 |
| PRO-INF-005 | Internacionalização (i18n) | RF005 |
| PRO-INF-006 | Gestão de Clientes (Multi-Tenancy) | RF006 |
| PRO-INF-007 | Login e Autenticação (OAuth, MFA) | RF007 |
| PRO-INF-008 | Configurações do Usuário | RF014 |

### 3.2 Jornada 2: Workflows e Importação (9 processos)

Motor de templates, notificações, aprovações e importações massivas.

| Código | Processo | RF |
|--------|----------|-----|
| PRO-WKF-001 | Motor de Templates | RF063 |
| PRO-WKF-002 | Templates de E-mail | RF064 |
| PRO-WKF-003 | Templates de Relatórios | RF065 |
| PRO-WKF-004 | Notificações e Alertas | RF066 |
| PRO-WKF-005 | Central de E-mails | RF067 |
| PRO-WKF-006 | Upload/Importação de Arquivos | RF084 |
| PRO-WKF-007 | Importação de Dados | RF085 |
| PRO-WKF-008 | Carga/Importação Massiva | RF086 |
| PRO-WKF-009 | Aprovações e Workflows | RF088 |

### 3.3 Jornada 3: Financeiro Completo (12 processos)

Contratos, faturamento, ativos, custos e rateio multi-dimensional.

**Contratos e Faturamento (7 processos):**

| Código | Processo | RF |
|--------|----------|-----|
| PRO-FCT-001 | Gestão de Faturas | RF026 |
| PRO-FCT-002 | Parâmetros de Faturamento | RF030 |
| PRO-FCT-003 | Plano de Contas | RF031 |
| PRO-FCT-004 | Notas Fiscais/Faturas (NF-e) | RF032 |
| PRO-FCT-005 | Conciliação de Faturas | RF089 |
| PRO-FCT-006 | Medição/Faturamento de Contratos | RF090 |
| PRO-FCT-007 | Auditoria de Faturas | RF097 |

**Ativos e Custos (5 processos):**

| Código | Processo | RF |
|--------|----------|-----|
| PRO-FAC-001 | Gestão de Ativos | RF025 |
| PRO-FAC-002 | Custos Fixos | RF036 |
| PRO-FAC-003 | Custos por Ativo (TCO) | RF037 |
| PRO-FAC-004 | Notas Fiscais de Estoque | RF042 |
| PRO-FAC-005 | Rateio Multi-dimensional | RF055 |

### 3.4 Jornada 5: Service Desk (8 processos)

SLA, chamados, solicitações, escalação automática e integrações.

| Código | Processo | RF |
|--------|----------|-----|
| PRO-SVC-001 | SLA de Operações | RF028 |
| PRO-SVC-002 | SLA de Serviços | RF029 |
| PRO-SVC-003 | Gestão de Chamados | RF033 |
| PRO-SVC-004 | SLA de Solicitações | RF038 |
| PRO-SVC-005 | Gestão de Solicitações | RF053 |
| PRO-SVC-006 | Escalação Automática | RF072 |
| PRO-SVC-007 | Integração com ERPs | RF078 |
| PRO-SVC-008 | APIs Externas | RF087 |

### 3.5 Jornada 6: Auditoria e Integrações (1 processo)

Inventário cíclico com contagem automática e conciliação.

| Código | Processo | RF |
|--------|----------|-----|
| PRO-AUD-001 | Inventário Cíclico | RF068 |

---

## 4. COMO USAR ESTE DOCUMENTO

### 4.1 Navegação

Cada jornada está em um arquivo separado para facilitar:
- Criação incremental (jornada por jornada)
- Revisão e validação isolada
- Manutenção futura (alterar só a jornada afetada)
- Agregação final simples (concatenar arquivos)

### 4.2 Estrutura de Cada Processo

Cada processo documentado segue o seguinte padrão:

```markdown
### X.Y Processo: [Nome do Processo]

**Código:** PRO-XXX-YYY
**RFs Envolvidos:** RFXXX
**Área:** [Infraestrutura | Financeiro | Service Desk | Auditoria]
**Criticidade:** [Alta | Média | Baixa]

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
[Diagrama Mermaid do processo legado]

**Moderno (Modernizado):**
[Diagrama Mermaid do processo moderno]

#### Descrição do Processo
[Narrativa concisa explicando como o processo funciona no sistema modernizado]

#### Atores
- **Ator Principal:** [Nome + Papel]
- **Atores Secundários:** [Lista]
- **Sistemas Externos:** [Integrações]

#### Fluxo Principal
1. [Passo 1]
2. [Passo 2]
...

#### Automações
- ✅ [Automação 1]
- ✅ [Automação 2]

#### Integrações
- **Sistema:** Descrição

#### Regras de Negócio Principais
- **RN-XXX-01:** [Descrição resumida]
- [Ver regras completas em RFXXX.md]

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ [Gap 1]
- ❌ [Gap 2]

**Melhorias no moderno:**
- ✅ [Melhoria 1]
- ✅ [Melhoria 2]
```

### 4.3 Referências aos RFs Completos

Cada processo possui link para o RF completo onde estão:
- User Stories detalhadas
- Regras de negócio completas (RN-XXX-01, RN-XXX-02...)
- Casos de teste (TC-RFXXX.yaml)
- Critérios de aceite
- Endpoints da API

### 4.4 Diagramas BPMN

Os diagramas usam notação Mermaid e são:
- **Simples:** Fluxo principal + decisões críticas
- **Comparativos:** Legado vs Moderno lado a lado
- **Renderizáveis:** Markdown compatível com GitHub, GitLab, VSCode

---

## 5. PRÓXIMOS PASSOS

Após a criação de todos os arquivos modulares:

1. **Revisão por Jornada:** Validar cada jornada isoladamente
2. **Agregação (Opcional):** Concatenar todos os arquivos em um único `PROCESSOS-NEGOCIO-ICONTROLIT-V2.md`
3. **Integração com Governança:** Linkar este documento em `D:\IC2_Governanca\governanca\ARCHITECTURE.md`
4. **Manutenção:** Atualizar processos conforme novos RFs são implementados

---

## 6. REFERÊNCIAS

- **Governança:** [D:\IC2_Governanca\governanca\](../../governanca/)
- **Contratos:** [D:\IC2_Governanca\governanca\contracts\](../../governanca/contracts/)
- **RFs Completos:** [D:\IC2_Governanca\documentacao\](../)
- **Legado:** [D:\IC2\ic1_legado\](../../../IC2/ic1_legado/)

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 2.0 - Documentação Modular de Processos

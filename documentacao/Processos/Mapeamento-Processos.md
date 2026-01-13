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


---

# PARTE 2: JORNADA 1 - INFRAESTRUTURA E CONFIGURAÇÃO

---


**Versão:** 1.0
**Data:** 2026-01-12
**Status:** Vigente
**Autor:** ALC (alc.dev.br)

---

## 1. Visão Geral da Jornada

Esta jornada documenta os processos fundamentais de infraestrutura e configuração do sistema IControlIT modernizado. Estes processos formam a base operacional que sustenta todas as demais funcionalidades da plataforma.

**Escopo da Jornada:**
- Configurações de sistema e parâmetros
- Observabilidade e monitoramento
- Multi-tenancy e gestão de clientes
- Autenticação e segurança
- Internacionalização

**Características Comuns:**
- Arquitetura multi-tenant nativa
- APIs REST modernas
- Automações inteligentes
- Auditoria completa
- Conformidade LGPD/SOX

---

## 2. Mapa de Processos da Jornada

| Código | Processo | RF | Criticidade |
|--------|----------|-----|-------------|
| PRO-INF-001 | Parâmetros e Configurações | RF001 | Alta |
| PRO-INF-002 | Configurações Gerais | RF002 | Alta |
| PRO-INF-003 | Logs e Monitoramento | RF003 | Alta |
| PRO-INF-004 | Auditoria de Operações | RF004 | Alta |
| PRO-INF-005 | Internacionalização (i18n) | RF005 | Média |
| PRO-INF-006 | Gestão de Clientes (Multi-Tenancy) | RF006 | Alta |
| PRO-INF-007 | Login e Autenticação | RF007 | Alta |
| PRO-INF-008 | Configurações do Usuário | RF014 | Média |

---

## 3. Processos Detalhados

### 3.1 Processo: Parâmetros e Configurações

**Código:** PRO-INF-001
**RFs Envolvidos:** RF001
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Admin altera parâmetro] --> B[Stored Procedure]
    B --> C[Tabela Parâmetros]
    C --> D[Reiniciar aplicação]
    D --> E[Parâmetro ativo]

    style B fill:#ffcccc
    style D fill:#ffcccc

    F[Problemas] --> G[❌ Sem validação de tipo]
    F --> H[❌ Sem histórico]
    F --> I[❌ Reiniciar para aplicar]
    F --> J[❌ Sem criptografia]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Admin altera parâmetro] --> B{Tipo válido?}
    B -->|Não| C[Retorna erro tipado]
    B -->|Sim| D{Sensível?}
    D -->|Sim| E[Criptografa AES-256]
    D -->|Não| F[Valida contra schema]
    E --> F
    F --> G{Feature Flag?}
    G -->|Sim| H[Rollout gradual por %]
    G -->|Não| I[Atualiza banco]
    H --> I
    I --> J[Invalida cache Redis]
    J --> K[Registra histórico]
    K --> L[Aplica imediatamente]
    L --> M[Auditoria LGPD]

    style E fill:#ccffcc
    style J fill:#ccffcc
    style K fill:#ccffcc
    style M fill:#ccffcc
```

#### Descrição do Processo

O processo de gestão de parâmetros permite configurar comportamentos críticos do sistema de forma dinâmica, sem necessidade de deploy. Suporta feature flags com rollout gradual (canary release), criptografia de dados sensíveis, validação tipada e histórico completo de alterações.

**Diferencial Moderno:**
- Aplicação imediata via invalidação de cache Redis
- Criptografia AES-256 para dados sensíveis (chaves API, senhas SMTP)
- Feature flags com controle de percentual de usuários (0%-100%)
- Validação tipada (String, Integer, Decimal, Boolean, Date, JSON)
- Limites de uso por Fornecedor (ex: max 1000 usuários)
- Histórico versionado com rollback 1-click

#### Atores

- **Ator Principal:** Administrador de Sistema (acesso total aos parâmetros)
- **Atores Secundários:**
  - Gestor de Fornecedor (acesso aos parâmetros de seu fornecedor)
  - Sistema de Cache (Redis)
  - Sistema de Auditoria
- **Sistemas Externos:** Nenhum

#### Fluxo Principal

1. **Admin acessa painel de parâmetros**
   - Lista todos os parâmetros configuráveis
   - Filtra por categoria, tipo ou fornecedor

2. **Admin seleciona parâmetro para alterar**
   - Visualiza valor atual, tipo, descrição
   - Visualiza histórico de alterações anteriores

3. **Sistema valida o novo valor**
   - Valida contra o tipo definido (String, Integer, etc.)
   - Valida contra regras específicas (ex: range numérico)
   - Valida schema JSON se aplicável

4. **Sistema verifica se parâmetro é sensível**
   - Se sensível: criptografa com AES-256 antes de persistir
   - Se não sensível: persiste em texto claro

5. **Sistema verifica se é feature flag**
   - Se sim: permite configurar percentual de rollout (0%-100%)
   - Se não: aplica para 100% dos usuários

6. **Sistema persiste alteração**
   - Salva no banco de dados
   - Registra no histórico (versão anterior + nova)
   - Invalida cache Redis

7. **Sistema aplica imediatamente**
   - Cache atualizado força uso do novo valor
   - Sem necessidade de reiniciar aplicação

8. **Sistema registra auditoria**
   - Quem alterou, quando, valor anterior e novo
   - IP de origem, correlation ID
   - Snapshot completo para compliance

#### Automações

- ✅ **Validação tipada automática:** Sistema valida tipo de dado antes de persistir
- ✅ **Criptografia automática:** Parâmetros marcados como sensíveis são criptografados automaticamente
- ✅ **Invalidação de cache:** Redis é automaticamente atualizado após alteração
- ✅ **Rollout gradual:** Feature flags aplicados progressivamente conforme % configurado
- ✅ **Histórico automático:** Toda alteração gera entrada de histórico sem intervenção manual
- ✅ **Auditoria automática:** Registro completo gerado automaticamente para compliance

#### Integrações

- **Redis Cache:** Invalidação automática de cache após alteração de parâmetros
- **Sistema de Auditoria:** Registro imutável de todas as alterações (RF004)
- **Sistema de Criptografia:** AES-256 para dados sensíveis

#### Regras de Negócio Principais

- **RN-001-01:** Todo parâmetro deve ter tipo definido (String, Integer, Decimal, Boolean, Date, JSON)
- **RN-001-02:** Parâmetros sensíveis devem ser criptografados com AES-256
- **RN-001-03:** Feature flags suportam rollout gradual de 0% a 100%
- **RN-001-04:** Alterações devem ser aplicadas imediatamente via invalidação de cache
- **RN-001-05:** Histórico completo deve ser mantido para auditoria
- **RN-001-06:** Limites de uso por Fornecedor devem ser validados antes da persistência
- **RN-001-07:** Rollback 1-click deve estar disponível para versões anteriores

**[Ver regras completas em RF001.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Stored procedures alteravam diretamente tabela de parâmetros
- ❌ Sem validação de tipo (tudo armazenado como VARCHAR)
- ❌ Sem criptografia de dados sensíveis (chaves API expostas)
- ❌ Necessário reiniciar aplicação para aplicar mudanças
- ❌ Sem histórico de alterações (impossível rastrear mudanças)
- ❌ Sem feature flags (features ativadas para 100% ou 0%)
- ❌ Sem cache (consultas repetitivas ao banco)

**Melhorias no moderno:**
- ✅ Validação tipada via DTOs e FluentValidation
- ✅ Criptografia AES-256 automática para dados sensíveis
- ✅ Aplicação imediata via invalidação de cache Redis
- ✅ Histórico versionado completo (data, usuário, valor anterior/novo)
- ✅ Feature flags com rollout gradual (canary release)
- ✅ Cache Redis com TTL configurável
- ✅ Rollback 1-click para versões anteriores
- ✅ Auditoria LGPD completa

---

### 3.2 Processo: Configurações Gerais

**Código:** PRO-INF-002
**RFs Envolvidos:** RF002
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Admin configura SMTP] --> B[Edita web.config]
    B --> C[Deploy manual]
    C --> D[Reinicia IIS]
    D --> E[Config ativa]

    F[Admin configura Azure] --> G[Edita appsettings.json]
    G --> C

    style B fill:#ffcccc
    style C fill:#ffcccc
    style D fill:#ffcccc
    style G fill:#ffcccc

    H[Problemas] --> I[❌ Sem hierarquia]
    H --> J[❌ Deploy para alterar]
    H --> K[❌ Sem versionamento]
    H --> L[❌ Sem rollback]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Admin configura SMTP] --> B{Nível?}
    B --> C[Global]
    B --> D[Fornecedor]
    B --> E[Empresa]
    B --> F[Departamento]
    B --> G[Usuário]

    C --> H[Valida credenciais SMTP]
    D --> H
    E --> H
    F --> H
    G --> H

    H -->|Válido| I[Criptografa senha]
    I --> J[Persiste hierarquia]
    J --> K[Invalida cache Redis]
    K --> L[Testa conexão]
    L -->|OK| M[Versiona config]
    M --> N[Auditoria]

    L -->|Falha| O[Rollback automático]
    O --> P[Alerta admin]

    style I fill:#ccffcc
    style J fill:#ccffcc
    style K fill:#ccffcc
    style M fill:#ccffcc
```

#### Descrição do Processo

O processo de configurações gerais gerencia integrações infraestruturais críticas do sistema (SMTP, Azure Storage, AWS S3, ERPs) com suporte a hierarquia multi-tenant, versionamento, rollback e feature flags progressivos.

**Diferencial Moderno:**
- Hierarquia de configurações em 5 níveis (Global → Fornecedor → Empresa → Depto → Usuário)
- Cache Redis com hot-reload (sem reiniciar aplicação)
- Versionamento completo com rollback 1-click
- Feature flags com canary release (ativação progressiva)
- Teste de conectividade antes de aplicar
- Export/Import para migração entre ambientes

#### Atores

- **Ator Principal:** Administrador de Sistema
- **Atores Secundários:**
  - Gestor de Fornecedor (configs de seu fornecedor)
  - Gestor de Empresa (configs de sua empresa)
  - Sistema de Cache (Redis)
  - Sistema de Versionamento
- **Sistemas Externos:**
  - Servidores SMTP (Outlook, Gmail, SendGrid)
  - Azure Storage
  - AWS S3
  - ERPs (SAP, TOTVS, Oracle)

#### Fluxo Principal

1. **Admin acessa painel de configurações gerais**
   - Visualiza configurações em árvore hierárquica
   - Filtra por tipo (SMTP, Azure, AWS, ERP)

2. **Admin seleciona tipo de configuração**
   - SMTP: servidor, porta, usuário, senha, TLS
   - Azure: connection string, container, SAS token
   - AWS: access key, secret key, bucket, region
   - ERP: endpoint, credenciais, timeout

3. **Admin define nível hierárquico**
   - Global: aplica para todos os clientes
   - Fornecedor: sobrescreve global para fornecedor específico
   - Empresa: sobrescreve fornecedor para empresa específica
   - Departamento: sobrescreve empresa para departamento específico
   - Usuário: sobrescreve departamento para usuário específico

4. **Sistema valida credenciais**
   - SMTP: tenta enviar email de teste
   - Azure/AWS: tenta listar containers/buckets
   - ERP: tenta autenticar no endpoint

5. **Se validação OK: Sistema persiste configuração**
   - Criptografa campos sensíveis (senhas, tokens) com AES-256
   - Salva no banco respeitando hierarquia
   - Cria snapshot da versão anterior
   - Invalida cache Redis

6. **Se validação FALHA: Sistema faz rollback automático**
   - Restaura versão anterior
   - Alerta administrador via notificação
   - Registra erro no log estruturado

7. **Sistema aplica feature flag (se configurado)**
   - Ativa config para percentual de usuários (0%-100%)
   - Permite canary release gradual

8. **Sistema registra auditoria**
   - Snapshot antes/depois
   - Quem alterou, quando, IP de origem
   - Resultado do teste de conectividade

#### Automações

- ✅ **Validação de credenciais:** Sistema testa conectividade antes de aplicar
- ✅ **Criptografia automática:** Senhas e tokens criptografados com AES-256
- ✅ **Rollback automático:** Se validação falha, versão anterior é restaurada
- ✅ **Invalidação de cache:** Redis atualizado automaticamente
- ✅ **Versionamento automático:** Toda alteração gera nova versão
- ✅ **Notificação de erro:** Admin alertado automaticamente se teste falhar
- ✅ **Hot-reload:** Configurações aplicadas sem reiniciar aplicação

#### Integrações

- **Redis Cache:** Hot-reload de configurações via invalidação de cache
- **SMTP (Outlook, Gmail, SendGrid):** Teste de envio de email
- **Azure Storage:** Validação de connection string e SAS token
- **AWS S3:** Validação de access key e listagem de buckets
- **ERPs (SAP, TOTVS, Oracle):** Teste de autenticação e conectividade
- **Sistema de Auditoria (RF004):** Registro imutável de alterações

#### Regras de Negócio Principais

- **RN-002-01:** Hierarquia de configurações: Global → Fornecedor → Empresa → Depto → Usuário
- **RN-002-02:** Configurações de nível inferior sobrescrevem níveis superiores
- **RN-002-03:** Validação obrigatória de credenciais antes de persistir
- **RN-002-04:** Rollback automático se validação falhar
- **RN-002-05:** Campos sensíveis devem ser criptografados com AES-256
- **RN-002-06:** Cache Redis deve ser invalidado após alteração
- **RN-002-07:** Versionamento completo para rollback 1-click
- **RN-002-08:** Feature flags suportam ativação progressiva (0%-100%)

**[Ver regras completas em RF002.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Configurações em arquivos XML (web.config, appsettings.json)
- ❌ Deploy manual necessário para alterar configurações
- ❌ Reiniciar IIS/aplicação para aplicar mudanças
- ❌ Sem hierarquia multi-tenant (config única para todos)
- ❌ Sem versionamento (impossível voltar versão anterior)
- ❌ Sem teste de conectividade (configs inválidas quebravam sistema)
- ❌ Senhas em texto claro ou Base64 fraco
- ❌ Sem feature flags (mudanças para 100% dos usuários imediatamente)

**Melhorias no moderno:**
- ✅ Configurações persistidas em banco com hierarquia 5 níveis
- ✅ Hot-reload via cache Redis (sem reiniciar aplicação)
- ✅ Teste automático de conectividade antes de aplicar
- ✅ Rollback automático se teste falhar
- ✅ Criptografia AES-256 para dados sensíveis
- ✅ Versionamento completo com snapshot antes/depois
- ✅ Feature flags com canary release
- ✅ Export/Import para migração entre ambientes (HOM → PRD)
- ✅ Auditoria completa LGPD/SOX

---

### 3.3 Processo: Logs e Monitoramento

**Código:** PRO-INF-003
**RFs Envolvidos:** RF003
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Requisição chega] --> B[Log em arquivo txt]
    B --> C[Admin procura erro manualmente]
    C --> D[Abre arquivos de log]
    D --> E[CTRL+F para buscar]

    style B fill:#ffcccc
    style C fill:#ffcccc
    style E fill:#ffcccc

    F[Problemas] --> G[❌ Logs não estruturados]
    F --> H[❌ Sem correlation ID]
    F --> I[❌ Sem alertas automáticos]
    F --> J[❌ Dados sensíveis expostos]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Requisição chega] --> B[Gera Correlation ID]
    B --> C[Log estruturado JSON]
    C --> D[Mascara dados sensíveis]
    D --> E[Registra métricas RED]
    E --> F[Envia para Seq/ELK]

    F --> G{Erro crítico?}
    G -->|Sim| H[Alerta automático]
    H --> I[Email/Slack/Teams]
    G -->|Não| J[Dashboard tempo real]

    F --> K[Health Check /health]
    K --> L[OpenTelemetry Tracing]

    style B fill:#ccffcc
    style C fill:#ccffcc
    style D fill:#ccffcc
    style E fill:#ccffcc
    style H fill:#ccffcc
```

#### Descrição do Processo

O processo de logs e monitoramento captura, estrutura e analisa eventos do sistema em tempo real, permitindo observabilidade completa, detecção proativa de problemas e rastreamento distribuído de requisições.

**Diferencial Moderno:**
- Logs estruturados em formato JSON
- Correlation IDs para rastreamento end-to-end
- Mascaramento automático de dados sensíveis (CPF, senhas, tokens)
- Métricas RED (Rate, Errors, Duration)
- Health checks via endpoint /health
- Alertas automáticos para erros críticos
- Tracing distribuído com OpenTelemetry

#### Atores

- **Ator Principal:** Sistema de Logging (Serilog)
- **Atores Secundários:**
  - Administrador de Sistema (consulta logs)
  - Sistema de Alertas
  - DevOps (monitoramento)
- **Sistemas Externos:**
  - Seq (agregador de logs)
  - ELK Stack (Elasticsearch, Logstash, Kibana)
  - Azure Application Insights
  - Slack/Teams (notificações)

#### Fluxo Principal

1. **Requisição HTTP chega ao sistema**
   - Middleware intercepta e gera Correlation ID único (UUID)
   - Correlation ID adicionado ao contexto da requisição

2. **Sistema registra log estruturado**
   - Formato JSON com campos padronizados:
     - Timestamp (ISO 8601)
     - Level (Debug, Info, Warning, Error, Fatal)
     - Message
     - CorrelationId
     - UserId, ClienteId (multi-tenancy)
     - RequestPath, Method, StatusCode
     - Duration (ms)

3. **Sistema mascara dados sensíveis automaticamente**
   - CPF: 123.456.789-00 → 123.***.***-00
   - Senha: "senha123" → "***"
   - Token: "Bearer abc123..." → "Bearer ***"
   - Cartão: 1234 5678 9012 3456 → 1234 **** **** 3456

4. **Sistema registra métricas RED**
   - **Rate:** Requisições por segundo (RPS)
   - **Errors:** Taxa de erro (% de 5xx)
   - **Duration:** Latência (p50, p95, p99)

5. **Sistema envia logs para agregadores**
   - Seq (desenvolvimento/HOM)
   - Azure Application Insights (PRD)
   - ELK Stack (análises históricas)

6. **Sistema verifica severidade do evento**
   - Se Error/Fatal: dispara alerta automático
   - Se Warning: registra para análise posterior
   - Se Info/Debug: apenas persiste no agregador

7. **Sistema dispara alertas (se aplicável)**
   - Email para equipe de plantão
   - Notificação Slack/Teams
   - Cria incident no PagerDuty (erros críticos)

8. **Health check /health responde**
   - Status: Healthy | Degraded | Unhealthy
   - Dependências: Database, Redis, Azure Storage, SMTP
   - Uptime, memória, CPU

#### Automações

- ✅ **Geração automática de Correlation ID:** Todo request recebe UUID único
- ✅ **Log estruturado JSON:** Formato padronizado automaticamente
- ✅ **Mascaramento de dados sensíveis:** Regex automático para CPF, senhas, tokens
- ✅ **Coleta de métricas RED:** Rate, Errors, Duration registrados automaticamente
- ✅ **Envio para agregadores:** Logs enviados para Seq/ELK/Application Insights
- ✅ **Alertas automáticos:** Erros críticos disparam notificações
- ✅ **Health checks:** Endpoint /health responde status de dependências
- ✅ **Tracing distribuído:** OpenTelemetry rastreia requisições entre serviços

#### Integrações

- **Seq:** Agregador de logs estruturados (desenvolvimento/HOM)
- **Azure Application Insights:** Monitoramento e telemetria (PRD)
- **ELK Stack:** Análise histórica e dashboards customizados
- **Slack/Teams:** Notificações de alertas críticos
- **PagerDuty:** Gestão de incidents para erros críticos
- **OpenTelemetry:** Tracing distribuído entre microsserviços

#### Regras de Negócio Principais

- **RN-003-01:** Todo request deve ter Correlation ID único (UUID)
- **RN-003-02:** Logs devem ser estruturados em formato JSON
- **RN-003-03:** Dados sensíveis devem ser mascarados automaticamente
- **RN-003-04:** Métricas RED devem ser coletadas (Rate, Errors, Duration)
- **RN-003-05:** Erros críticos devem disparar alertas automáticos
- **RN-003-06:** Health check deve validar dependências (DB, Redis, Azure)
- **RN-003-07:** Logs devem ser enviados para agregadores em tempo real
- **RN-003-08:** Tracing distribuído deve rastrear requisições end-to-end

**[Ver regras completas em RF003.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Logs em arquivos .txt não estruturados
- ❌ Busca manual via CTRL+F em múltiplos arquivos
- ❌ Sem correlation ID (impossível rastrear requisição completa)
- ❌ Dados sensíveis expostos em logs (CPF, senhas)
- ❌ Sem alertas automáticos (descoberta reativa de erros)
- ❌ Sem métricas estruturadas (impossível calcular SLA)
- ❌ Sem health checks (infraestrutura descobria falhas tarde)
- ❌ Logs rotacionados manualmente (perda de dados)

**Melhorias no moderno:**
- ✅ Logs estruturados JSON com campos padronizados
- ✅ Correlation IDs para rastreamento end-to-end
- ✅ Mascaramento automático de dados sensíveis (LGPD)
- ✅ Métricas RED automatizadas (SLA calculável)
- ✅ Alertas automáticos via Slack/Teams/PagerDuty
- ✅ Health checks validando dependências críticas
- ✅ Agregadores centralizados (Seq, Application Insights, ELK)
- ✅ Tracing distribuído com OpenTelemetry
- ✅ Dashboards em tempo real
- ✅ Retenção configurável (7 dias dev, 90 dias PRD)

---

### 3.4 Processo: Auditoria de Operações

**Código:** PRO-INF-004
**RFs Envolvidos:** RF004
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Usuário altera registro] --> B[Trigger SQL grava log]
    B --> C[Tabela AuditLog]
    C --> D[Admin consulta SQL direto]

    style B fill:#ffcccc
    style D fill:#ffcccc

    E[Problemas] --> F[❌ Sem snapshot antes/depois]
    E --> G[❌ Sem retenção configurável]
    E --> H[❌ Sem detecção de anomalias]
    E --> I[❌ Sem assinatura digital]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Usuário altera registro] --> B[Captura snapshot antes]
    B --> C[Executa operação]
    C --> D[Captura snapshot depois]
    D --> E[Calcula diff JSON]
    E --> F[Gera assinatura SHA-256]
    F --> G[Persiste registro imutável]
    G --> H{Operação sensível?}
    H -->|Sim| I[Detecção de anomalias]
    I -->|Suspeito| J[Alerta automático]
    H -->|Não| K[Registro auditoria LGPD]
    J --> K
    K --> L{Retenção > 7 anos?}
    L -->|Sim| M[Cold storage Azure]
    L -->|Não| N[Hot storage SQL]

    style E fill:#ccffcc
    style F fill:#ccffcc
    style G fill:#ccffcc
    style I fill:#ccffcc
```

#### Descrição do Processo

O processo de auditoria registra de forma imutável todas as operações realizadas por usuários no sistema, capturando snapshots antes/depois, assinatura digital, detecção de anomalias e arquivamento automático para compliance.

**Diferencial Moderno:**
- Registro imutável de operações de usuários
- Snapshot antes/depois com diff JSON
- Retenção configurável (7 anos para compliance SOX/LGPD)
- Detecção de anomalias (horário atípico, volume anormal)
- Auditoria LGPD específica (acesso a dados pessoais)
- Assinatura digital SHA-256 para não repúdio
- Arquivamento automático em cold storage

#### Atores

- **Ator Principal:** Sistema de Auditoria
- **Atores Secundários:**
  - Usuários (geram eventos auditados)
  - Administrador (consulta auditoria)
  - Auditor Externo (compliance)
  - Sistema de Detecção de Anomalias
- **Sistemas Externos:**
  - Azure Blob Storage (cold storage)
  - Sistema de Machine Learning (detecção de anomalias)

#### Fluxo Principal

1. **Usuário inicia operação auditável**
   - CREATE, UPDATE, DELETE em tabelas sensíveis
   - Acesso a dados pessoais (LGPD)
   - Exportação de relatórios
   - Alteração de permissões

2. **Sistema captura snapshot ANTES da operação**
   - Serializa estado atual do registro em JSON
   - Captura timestamp, usuário, IP, correlation ID

3. **Sistema executa operação**
   - Operação é realizada no banco de dados
   - Transaction garantindo atomicidade

4. **Sistema captura snapshot DEPOIS da operação**
   - Serializa novo estado do registro em JSON

5. **Sistema calcula diff JSON**
   - Compara snapshot antes vs depois
   - Identifica exatamente quais campos mudaram
   - Formato: `{"campo": {"old": "valor_antigo", "new": "valor_novo"}}`

6. **Sistema gera assinatura digital SHA-256**
   - Hash do payload completo (antes + depois + metadata)
   - Garante não repúdio e integridade

7. **Sistema persiste registro imutável**
   - INSERT-only (nunca UPDATE ou DELETE)
   - Tabela AuditLog com campos:
     - Id, Timestamp, UserId, ClienteId
     - Entity, Action (CREATE/UPDATE/DELETE)
     - SnapshotBefore, SnapshotAfter, Diff
     - IP, CorrelationId, Signature

8. **Sistema verifica se operação é sensível**
   - Acesso a dados pessoais (CPF, email, telefone)
   - Alteração de permissões
   - Exportação de dados em massa

9. **Se sensível: Sistema executa detecção de anomalias**
   - Horário atípico (ex: 3h da manhã)
   - Volume anormal (ex: 1000 exclusões em 1 minuto)
   - IP de país não autorizado
   - Padrão suspeito via Machine Learning

10. **Se anomalia detectada: Sistema dispara alerta**
    - Email para gestor de segurança
    - Notificação Slack/Teams
    - Bloqueia operações subsequentes (se configurado)

11. **Sistema registra auditoria LGPD (se aplicável)**
    - Tabela específica para compliance LGPD
    - Campos: Titular, TipoDado, Finalidade, BaseLegal

12. **Sistema verifica retenção**
    - Se registro > 7 anos e cold storage habilitado:
      - Move para Azure Blob Storage (cold tier)
      - Comprime com GZIP
      - Mantém índice no SQL (para consulta rápida)

#### Automações

- ✅ **Captura automática de snapshots:** Antes e depois de toda operação auditável
- ✅ **Cálculo automático de diff:** Sistema identifica exatamente o que mudou
- ✅ **Assinatura digital SHA-256:** Gerada automaticamente para não repúdio
- ✅ **Detecção de anomalias:** Machine Learning identifica padrões suspeitos
- ✅ **Alertas automáticos:** Notificações para operações suspeitas
- ✅ **Arquivamento automático:** Registros antigos movidos para cold storage
- ✅ **Auditoria LGPD:** Registro específico para acesso a dados pessoais

#### Integrações

- **Azure Blob Storage:** Arquivamento de auditoria em cold storage
- **Sistema de Machine Learning:** Detecção de anomalias via Azure ML
- **Slack/Teams:** Notificações de alertas de segurança
- **Sistema de Logs (RF003):** Integração com logs estruturados

#### Regras de Negócio Principais

- **RN-004-01:** Toda operação auditável deve gerar registro imutável
- **RN-004-02:** Snapshots antes/depois devem ser capturados
- **RN-004-03:** Diff JSON deve identificar exatamente o que mudou
- **RN-004-04:** Assinatura digital SHA-256 obrigatória para não repúdio
- **RN-004-05:** Retenção mínima de 7 anos para compliance SOX/LGPD
- **RN-004-06:** Detecção de anomalias para operações sensíveis
- **RN-004-07:** Registros nunca podem ser alterados ou deletados (INSERT-only)
- **RN-004-08:** Auditoria LGPD específica para acesso a dados pessoais
- **RN-004-09:** Arquivamento automático em cold storage após período configurável

**[Ver regras completas em RF004.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Triggers SQL simples gravando tabela AuditLog
- ❌ Sem snapshot antes/depois (apenas "o que" mudou, não "de onde para onde")
- ❌ Sem assinatura digital (possível alteração de registros)
- ❌ Sem detecção de anomalias (descoberta reativa de fraudes)
- ❌ Sem auditoria LGPD específica
- ❌ Sem arquivamento automático (banco crescia indefinidamente)
- ❌ Retenção manual (DBA excluía registros antigos manualmente)
- ❌ Consulta via SQL direto (sem interface amigável)

**Melhorias no moderno:**
- ✅ Snapshots antes/depois com diff JSON detalhado
- ✅ Assinatura digital SHA-256 para não repúdio
- ✅ Detecção proativa de anomalias via Machine Learning
- ✅ Auditoria LGPD específica (compliance ANPD)
- ✅ Arquivamento automático em cold storage (Azure Blob)
- ✅ Retenção configurável (7 anos padrão, extensível)
- ✅ Interface web para consulta de auditoria
- ✅ Exportação para auditor externo (CSV, Excel, PDF)
- ✅ Registro imutável (INSERT-only, nunca UPDATE/DELETE)
- ✅ Alertas automáticos para operações suspeitas

---

### 3.5 Processo: Internacionalização (i18n)

**Código:** PRO-INF-005
**RFs Envolvidos:** RF005
**Área:** Infraestrutura e Configuração
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Desenvolvedor adiciona texto] --> B[Hardcoded em português]
    B --> C[Deploy]
    C --> D[Usuário internacional reclama]
    D --> E[Dev altera código]
    E --> C

    style B fill:#ffcccc
    style E fill:#ffcccc

    F[Problemas] --> G[❌ Textos hardcoded]
    F --> H[❌ Apenas português]
    F --> I[❌ Deploy para traduzir]
    F --> J[❌ Sem cache]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Desenvolvedor adiciona chave] --> B[Ex: common.save]
    B --> C[Sistema busca tradução]
    C --> D{Idioma usuário?}
    D --> E[pt-BR]
    D --> F[en-US]
    D --> G[es-ES]
    D --> H[fr-FR]

    E --> I[Cache Redis]
    F --> I
    G --> I
    H --> I

    I -->|Miss| J[Busca no banco]
    I -->|Hit| K[Retorna tradução]
    J --> K

    L[Gestor altera tradução] --> M[Interface visual]
    M --> N[Versiona tradução]
    N --> O[Invalida cache]
    O --> P{Sem tradução?}
    P -->|Sim| Q[Azure Translator API]
    Q --> R[Tradução automática]

    style I fill:#ccffcc
    style M fill:#ccffcc
    style N fill:#ccffcc
    style Q fill:#ccffcc
```

#### Descrição do Processo

O processo de internacionalização permite gestão multi-idioma do sistema com tradução automática, versionamento, rollback e cache Redis para performance.

**Diferencial Moderno:**
- Motor de tradução multi-idioma (pt-BR, en-US, es-ES, fr-FR)
- Gestão visual de traduções (sem acesso ao código)
- Versionamento e rollback
- Tradução automática via Azure Translator API
- Formatação regional (datas, moedas, números)
- Cache Redis para performance
- Lazy loading de traduções

#### Atores

- **Ator Principal:** Gestor de Traduções
- **Atores Secundários:**
  - Desenvolvedor (adiciona chaves de tradução)
  - Usuário Final (consome traduções)
  - Tradutor Profissional (revisão de traduções)
- **Sistemas Externos:**
  - Azure Translator API
  - Redis Cache

#### Fluxo Principal

1. **Desenvolvedor adiciona nova chave de tradução**
   - Formato: `namespace.chave` (ex: `common.save`, `errors.validation.required`)
   - Adiciona chave no código: `{{ 'common.save' | translate }}`

2. **Sistema verifica se tradução existe**
   - Busca no cache Redis primeiro (TTL 24h)
   - Se não existir: busca no banco de dados
   - Se não existir: retorna chave como fallback

3. **Gestor acessa interface visual de traduções**
   - Lista todas as chaves do sistema
   - Filtra por namespace, idioma, status
   - Visualiza traduções faltantes (missing translations)

4. **Gestor adiciona/edita tradução**
   - Seleciona chave e idioma
   - Insere texto traduzido
   - Sistema valida interpolações `{{variable}}`

5. **Sistema oferece tradução automática**
   - Se tradução não existe para idioma secundário
   - Azure Translator API traduz automaticamente
   - Gestor revisa e aprova/edita tradução sugerida

6. **Sistema versiona tradução**
   - Cria snapshot da versão anterior
   - Persiste nova versão no banco
   - Permite rollback 1-click

7. **Sistema invalida cache Redis**
   - Remove tradução do cache
   - Próxima requisição recarrega do banco

8. **Sistema aplica formatação regional**
   - Datas: pt-BR (dd/MM/yyyy), en-US (MM/dd/yyyy)
   - Moedas: pt-BR (R$ 1.234,56), en-US ($1,234.56)
   - Números: pt-BR (1.234,56), en-US (1,234.56)

9. **Sistema faz lazy loading**
   - Carrega apenas traduções do namespace usado
   - Reduz payload inicial da aplicação

#### Automações

- ✅ **Cache automático Redis:** Traduções cacheadas por 24h
- ✅ **Tradução automática:** Azure Translator API traduz chaves faltantes
- ✅ **Invalidação de cache:** Redis atualizado automaticamente após alteração
- ✅ **Detecção de chaves faltantes:** Sistema identifica traduções missing
- ✅ **Lazy loading:** Carrega traduções sob demanda
- ✅ **Formatação regional:** Datas, moedas e números formatados automaticamente
- ✅ **Versionamento automático:** Toda alteração gera nova versão

#### Integrações

- **Redis Cache:** Cache de traduções com TTL 24h
- **Azure Translator API:** Tradução automática de chaves faltantes
- **Sistema de Versionamento:** Rollback 1-click de traduções

#### Regras de Negócio Principais

- **RN-005-01:** Chaves de tradução devem seguir formato `namespace.chave`
- **RN-005-02:** Idiomas suportados: pt-BR, en-US, es-ES, fr-FR
- **RN-005-03:** Traduções devem ser cacheadas no Redis (TTL 24h)
- **RN-005-04:** Tradução automática via Azure Translator para chaves faltantes
- **RN-005-05:** Versionamento completo com rollback 1-click
- **RN-005-06:** Formatação regional automática (datas, moedas, números)
- **RN-005-07:** Lazy loading de traduções por namespace
- **RN-005-08:** Fallback para chave se tradução não existir

**[Ver regras completas em RF005.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Textos hardcoded em português no código
- ❌ Sem suporte a múltiplos idiomas
- ❌ Deploy necessário para alterar textos
- ❌ Sem cache (consultas repetitivas ao banco)
- ❌ Sem tradução automática (tradução 100% manual)
- ❌ Sem versionamento (impossível voltar texto anterior)
- ❌ Formatação regional inconsistente
- ❌ Desenvolvedor precisava alterar código para novos textos

**Melhorias no moderno:**
- ✅ Sistema de chaves de tradução (`namespace.chave`)
- ✅ 4 idiomas suportados (pt-BR, en-US, es-ES, fr-FR)
- ✅ Interface visual para gestão de traduções (sem código)
- ✅ Cache Redis com TTL 24h
- ✅ Tradução automática via Azure Translator API
- ✅ Versionamento completo com rollback 1-click
- ✅ Formatação regional automática
- ✅ Lazy loading (performance otimizada)
- ✅ Detecção automática de traduções faltantes
- ✅ Export/Import de traduções (Excel, JSON)

---

### 3.6 Processo: Gestão de Clientes (Multi-Tenancy)

**Código:** PRO-INF-006
**RFs Envolvidos:** RF006
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Admin cadastra cliente] --> B[Preenche CNPJ manualmente]
    B --> C[Preenche dados manualmente]
    C --> D[Salva no banco]
    D --> E[Esquece de validar CNPJ]

    style E fill:#ffcccc

    F[Problemas] --> G[❌ CNPJ inválidos no banco]
    F --> H[❌ Dados desatualizados]
    F --> I[❌ Hard delete perde histórico]
    F --> J[❌ Sem multi-tenancy nativo]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Admin inicia cadastro] --> B[Digita CNPJ]
    B --> C[Valida formato CNPJ]
    C -->|Inválido| D[Retorna erro]
    C -->|Válido| E[Consulta ReceitaWS]
    E -->|Encontrado| F[Preenche dados automaticamente]
    F --> G[Razão Social, Nome Fantasia, Endereço]
    E -->|Não encontrado| H[Retorna erro]

    G --> I[Admin revisa dados]
    I --> J[Salva com ClienteId]
    J --> K[Ativa multi-tenancy]
    K --> L[Auditoria completa]

    M[Admin exclui cliente] --> N{Tem dados?}
    N -->|Sim| O[Soft delete]
    O --> P[Marca Ativo=false]
    P --> Q[Mantém histórico]
    N -->|Não| R[Hard delete permitido]

    style E fill:#ccffcc
    style F fill:#ccffcc
    style K fill:#ccffcc
    style O fill:#ccffcc
```

#### Descrição do Processo

O processo de gestão de clientes implementa multi-tenancy nativo com isolamento de dados por ClienteId, integração com ReceitaWS para consulta automática de CNPJ e soft delete para preservação de histórico.

**Diferencial Moderno:**
- Multi-tenancy nativo (ClienteId obrigatório em todas as tabelas)
- Integração ReceitaWS (consulta CNPJ automática)
- Soft delete em cascata (preserva histórico)
- Validação CNPJ/CPF com dígitos verificadores
- Auditoria completa 7 anos
- Isolamento de dados por tenant

#### Atores

- **Ator Principal:** Administrador de Sistema
- **Atores Secundários:**
  - Gestor de Fornecedor (gerencia seus clientes)
  - Sistema de Auditoria
- **Sistemas Externos:**
  - ReceitaWS (consulta CNPJ)
  - VIACEP (consulta CEP)

#### Fluxo Principal

1. **Admin acessa cadastro de clientes**
   - Interface lista clientes ativos
   - Filtra por CNPJ, razão social, status

2. **Admin inicia novo cadastro**
   - Digita CNPJ (formato: 00.000.000/0000-00)

3. **Sistema valida formato CNPJ**
   - Valida dígitos verificadores
   - Se inválido: retorna erro imediatamente

4. **Sistema consulta ReceitaWS**
   - Busca dados da empresa por CNPJ
   - Timeout: 5 segundos

5. **Sistema preenche dados automaticamente**
   - Razão Social
   - Nome Fantasia
   - Endereço completo (logradouro, número, bairro, cidade, UF, CEP)
   - Situação cadastral
   - Data de abertura

6. **Admin revisa dados preenchidos**
   - Pode editar campos se necessário
   - Adiciona dados específicos:
     - Email de contato
     - Telefone
     - Responsável
     - Observações

7. **Sistema gera ClienteId único**
   - UUID v4
   - Usado como discriminador multi-tenancy

8. **Sistema salva cliente**
   - Persiste no banco com ClienteId
   - Ativa multi-tenancy para esse cliente
   - Todas as operações subsequentes filtram por ClienteId

9. **Sistema registra auditoria**
   - Snapshot completo
   - Quem cadastrou, quando, IP
   - Dados retornados da ReceitaWS (rastreabilidade)

**Fluxo de Exclusão (Soft Delete):**

1. **Admin solicita exclusão de cliente**

2. **Sistema verifica se cliente tem dados associados**
   - Verifica tabelas relacionadas (Usuários, Contratos, Faturas, etc.)

3. **Se tem dados: Sistema faz soft delete**
   - Marca campo `Ativo = false`
   - Mantém registro no banco
   - Preserva histórico completo
   - Cliente não aparece mais em listagens
   - Auditoria registra exclusão lógica

4. **Se não tem dados: Sistema permite hard delete**
   - Remove fisicamente do banco
   - Apenas se nenhum registro relacionado existir

#### Automações

- ✅ **Consulta automática ReceitaWS:** Dados preenchidos automaticamente via CNPJ
- ✅ **Validação de CNPJ:** Dígitos verificadores validados automaticamente
- ✅ **Geração de ClienteId:** UUID único gerado automaticamente
- ✅ **Soft delete em cascata:** Exclusões lógicas preservam histórico
- ✅ **Isolamento multi-tenancy:** Todas as queries filtram por ClienteId automaticamente
- ✅ **Auditoria automática:** Registro completo de CREATE, UPDATE, DELETE
- ✅ **Consulta CEP:** Via VIACEP se endereço não vier da ReceitaWS

#### Integrações

- **ReceitaWS:** Consulta dados de CNPJ automaticamente
- **VIACEP:** Consulta endereço via CEP
- **Sistema de Auditoria (RF004):** Registro imutável de operações
- **Sistema de Validação:** FluentValidation para CNPJ/CPF

#### Regras de Negócio Principais

- **RN-006-01:** ClienteId (UUID) obrigatório em todas as tabelas do sistema
- **RN-006-02:** CNPJ deve ser validado com dígitos verificadores
- **RN-006-03:** Consulta ReceitaWS obrigatória ao cadastrar CNPJ
- **RN-006-04:** Soft delete obrigatório para clientes com dados associados
- **RN-006-05:** Hard delete permitido apenas se nenhum dado associado existir
- **RN-006-06:** Todas as queries devem filtrar por ClienteId (multi-tenancy)
- **RN-006-07:** Auditoria completa deve ser mantida por 7 anos
- **RN-006-08:** ClienteId não pode ser alterado após criação

**[Ver regras completas em RF006.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Sem multi-tenancy nativo (filtros manuais por cliente)
- ❌ CNPJ digitado manualmente (erros de digitação comuns)
- ❌ Sem validação de dígitos verificadores
- ❌ Sem consulta ReceitaWS (dados desatualizados)
- ❌ Hard delete (perdia histórico completo)
- ❌ Sem auditoria de alterações
- ❌ Dados duplicados (mesmo CNPJ cadastrado múltiplas vezes)
- ❌ Filtros por cliente esquecidos (vazamento de dados entre clientes)

**Melhorias no moderno:**
- ✅ Multi-tenancy nativo com ClienteId em todas as tabelas
- ✅ Consulta automática ReceitaWS via CNPJ
- ✅ Validação de dígitos verificadores CNPJ/CPF
- ✅ Soft delete preservando histórico completo
- ✅ Auditoria completa por 7 anos
- ✅ Impossível cadastrar CNPJ duplicado
- ✅ Filtros por ClienteId automáticos (sem vazamento de dados)
- ✅ Isolamento de dados garantido por arquitetura
- ✅ Compliance LGPD (rastreabilidade de dados de clientes)

---

### 3.7 Processo: Login e Autenticação

**Código:** PRO-INF-007
**RFs Envolvidos:** RF007
**Área:** Infraestrutura e Configuração
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Usuário digita login/senha] --> B[Verifica no banco]
    B -->|OK| C[Cria sessão]
    C --> D[Cookie de sessão]
    D --> E[Acesso liberado]

    B -->|Erro| F[Retorna erro genérico]

    style B fill:#ffcccc
    style F fill:#ffcccc

    G[Problemas] --> H[❌ Senha em MD5 fraco]
    G --> I[❌ Sem MFA]
    G --> J[❌ Sem rate limiting]
    G --> K[❌ Erro genérico ajuda ataques]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Usuário digita login/senha] --> B{Rate limit OK?}
    B -->|Excedido| C[HTTP 429 Too Many Requests]
    B -->|OK| D[Valida credenciais]
    D -->|Erro| E[Incrementa tentativas]
    E --> F{3 tentativas?}
    F -->|Sim| G[Bloqueia conta 15min]
    F -->|Não| H[Retorna erro genérico]

    D -->|OK| I{MFA habilitado?}
    I -->|Sim| J[Envia código SMS/Email/App]
    J --> K[Usuário informa código]
    K -->|Válido| L[Gera Access Token JWT]
    I -->|Não| L

    L --> M[Gera Refresh Token]
    M --> N[Salva sessão Redis]
    N --> O[Retorna tokens]
    O --> P[Auditoria login]

    Q[Token expira] --> R[Usa Refresh Token]
    R --> S[Gera novo Access Token]
    S --> T[Rotation: novo Refresh Token]

    style D fill:#ccffcc
    style I fill:#ccffcc
    style L fill:#ccffcc
    style M fill:#ccffcc
    style N fill:#ccffcc
```

#### Descrição do Processo

O processo de login e autenticação implementa OAuth 2.0 + OpenID Connect com Multi-Factor Authentication (MFA), refresh token rotation, session management, rate limiting e audit log completo.

**Diferencial Moderno:**
- OAuth 2.0 + OpenID Connect
- Multi-Factor Authentication (SMS, Email, Authenticator App)
- Refresh token rotation (segurança contra roubo de token)
- Session management com Redis
- Rate limiting (proteção contra brute force)
- Audit log de acesso
- Password hashing com BCrypt (salt automático)

#### Atores

- **Ator Principal:** Usuário Final
- **Atores Secundários:**
  - Sistema de Autenticação
  - Sistema de Sessão (Redis)
  - Sistema de Auditoria
  - Provedor MFA (SMS, Email, App)
- **Sistemas Externos:**
  - Provedor SMS (Twilio, AWS SNS)
  - Provedor Email (SendGrid)
  - Authenticator Apps (Google Authenticator, Authy)

#### Fluxo Principal

1. **Usuário acessa tela de login**
   - Digita email/login
   - Digita senha

2. **Sistema verifica rate limiting**
   - Máximo 5 tentativas por 15 minutos por IP
   - Se excedido: retorna HTTP 429 Too Many Requests

3. **Sistema valida credenciais**
   - Busca usuário por email/login
   - Compara senha com hash BCrypt armazenado
   - Se inválido: incrementa contador de tentativas
   - Se 3 tentativas falhadas: bloqueia conta por 15 minutos

4. **Sistema verifica se MFA está habilitado**
   - Se habilitado: prossegue para fluxo MFA
   - Se não habilitado: pula para geração de tokens

5. **Fluxo MFA (se habilitado)**
   - Sistema gera código de 6 dígitos
   - Envia via SMS, Email ou Authenticator App (conforme preferência usuário)
   - Código válido por 5 minutos
   - Usuário informa código
   - Sistema valida código
   - Se inválido: retorna erro (máximo 3 tentativas)

6. **Sistema gera Access Token JWT**
   - Payload: UserId, ClienteId, Roles, Permissions
   - Algoritmo: RS256 (chave assimétrica)
   - Validade: 15 minutos

7. **Sistema gera Refresh Token**
   - Token opaco (UUID v4)
   - Validade: 7 dias
   - Armazenado no Redis com TTL

8. **Sistema cria sessão no Redis**
   - Chave: `session:{UserId}:{RefreshToken}`
   - Valor: {AccessToken, RefreshToken, IP, UserAgent, CreatedAt}
   - TTL: 7 dias

9. **Sistema retorna tokens**
   - Access Token (Bearer Token para autenticar requisições)
   - Refresh Token (para renovar Access Token)

10. **Sistema registra auditoria de login**
    - Timestamp, UserId, IP, UserAgent
    - Sucesso ou falha
    - Método de autenticação (senha, MFA)

**Fluxo de Renovação de Token:**

1. **Access Token expira (após 15 minutos)**

2. **Cliente envia Refresh Token para endpoint `/auth/refresh`**

3. **Sistema valida Refresh Token**
   - Verifica se existe no Redis
   - Verifica se não está revogado
   - Verifica se não expirou (7 dias)

4. **Sistema gera novo Access Token**
   - Mesmo payload do token anterior
   - Nova validade de 15 minutos

5. **Sistema faz rotation do Refresh Token**
   - Gera novo Refresh Token
   - Revoga Refresh Token antigo
   - Atualiza sessão no Redis
   - Segurança: se token antigo for roubado, atacante não consegue renovar

6. **Sistema retorna novos tokens**
   - Novo Access Token
   - Novo Refresh Token

#### Automações

- ✅ **Rate limiting automático:** Proteção contra brute force (5 tentativas/15min)
- ✅ **Bloqueio temporário:** Conta bloqueada por 15min após 3 tentativas falhadas
- ✅ **Geração automática de tokens:** JWT Access Token + Refresh Token
- ✅ **Envio automático de MFA:** Código enviado via SMS/Email/App
- ✅ **Refresh token rotation:** Token renovado automaticamente para segurança
- ✅ **Sessão Redis:** Sessões armazenadas com TTL automático
- ✅ **Auditoria automática:** Registro completo de logins (sucesso e falha)
- ✅ **Limpeza de sessões:** Redis expira sessões antigas automaticamente

#### Integrações

- **Redis:** Gerenciamento de sessões e rate limiting
- **Twilio/AWS SNS:** Envio de SMS para MFA
- **SendGrid:** Envio de email para MFA
- **Google Authenticator/Authy:** MFA via Authenticator App
- **Sistema de Auditoria (RF004):** Registro imutável de logins

#### Regras de Negócio Principais

- **RN-007-01:** Senhas devem ser hasheadas com BCrypt (salt automático)
- **RN-007-02:** Access Token JWT válido por 15 minutos
- **RN-007-03:** Refresh Token válido por 7 dias
- **RN-007-04:** Rate limiting: máximo 5 tentativas por 15 minutos por IP
- **RN-007-05:** Bloqueio temporário de 15 minutos após 3 tentativas falhadas
- **RN-007-06:** MFA obrigatório para usuários com permissões administrativas
- **RN-007-07:** Refresh token rotation obrigatória para segurança
- **RN-007-08:** Sessões devem ser armazenadas no Redis com TTL
- **RN-007-09:** Auditoria completa de logins (sucesso e falha)
- **RN-007-10:** Logout deve revogar sessão do Redis

**[Ver regras completas em RF007.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Senhas em MD5 (algoritmo fraco, sem salt)
- ❌ Sem MFA (autenticação apenas por senha)
- ❌ Sessões em memória (perdidas ao reiniciar aplicação)
- ❌ Sem rate limiting (vulnerável a brute force)
- ❌ Sem refresh token (usuário reautenticava frequentemente)
- ❌ Erro detalhado expondo se usuário existe ("senha incorreta" vs "usuário não encontrado")
- ❌ Sem auditoria de tentativas falhadas
- ❌ Token JWT válido por 24 horas (janela de ataque maior)

**Melhorias no moderno:**
- ✅ BCrypt com salt automático (OWASP recomendado)
- ✅ MFA via SMS, Email ou Authenticator App
- ✅ Sessões persistidas no Redis (sobrevivem a reinicializações)
- ✅ Rate limiting com bloqueio temporário (5 tentativas/15min)
- ✅ Refresh token rotation (segurança contra roubo)
- ✅ Erro genérico (não expõe se usuário existe)
- ✅ Auditoria completa de logins (sucesso e falha)
- ✅ Access Token curto (15min) + Refresh Token (7 dias)
- ✅ OAuth 2.0 + OpenID Connect (padrão de mercado)
- ✅ Logout revoga sessão do Redis

---

### 3.8 Processo: Configurações do Usuário

**Código:** PRO-INF-008
**RFs Envolvidos:** RF014
**Área:** Infraestrutura e Configuração
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**
```mermaid
graph LR
    A[Usuário altera preferências] --> B[Salva em cookie]
    B --> C[Cookie expira]
    C --> D[Preferências perdidas]

    E[Usuário troca senha] --> F[Valida senha antiga]
    F --> G[Salva senha nova MD5]

    style B fill:#ffcccc
    style D fill:#ffcccc
    style G fill:#ffcccc

    H[Problemas] --> I[❌ Preferências em cookie]
    H --> J[❌ Senha em MD5]
    H --> K[❌ Sem blacklist de senhas]
    H --> L[❌ Sem auditoria]
```

**Moderno (Modernizado):**
```mermaid
graph LR
    A[Usuário altera preferências] --> B[Idioma, Tema, Timezone]
    B --> C[Salva no banco por UserId]
    C --> D[Invalida cache Redis]
    D --> E[Aplica imediatamente]

    F[Usuário troca senha] --> G[Valida senha antiga BCrypt]
    G -->|Erro| H[Retorna erro]
    G -->|OK| I{Senha nova segura?}
    I -->|Não| J[Valida requisitos]
    J --> K[Min 8 chars, maiúsc, minúsc, número, especial]
    I -->|Sim| L{Na blacklist?}
    L -->|Sim| M[Retorna erro - senha comum]
    L -->|Não| N[Hash BCrypt novo]
    N --> O[Salva no banco]
    O --> P[Revoga todas as sessões]
    P --> Q[Auditoria]
    Q --> R[Email notificação]

    style C fill:#ccffcc
    style D fill:#ccffcc
    style L fill:#ccffcc
    style P fill:#ccffcc
    style Q fill:#ccffcc
```

#### Descrição do Processo

O processo de configurações do usuário permite personalização de preferências pessoais (idioma, tema, timezone) e alteração segura de senha com validações robustas, blacklist de senhas comuns e auditoria completa.

**Diferencial Moderno:**
- Preferências pessoais persistidas no banco
- Alteração de senha com validações OWASP
- Blacklist de senhas comuns (top 10.000 senhas mais usadas)
- Auditoria de alterações de senha
- Revogação de sessões ao trocar senha
- Notificação por email de alterações sensíveis

#### Atores

- **Ator Principal:** Usuário Final
- **Atores Secundários:**
  - Sistema de Preferências
  - Sistema de Segurança (validação de senhas)
  - Sistema de Sessão (Redis)
  - Sistema de Auditoria
  - Sistema de Notificação (Email)
- **Sistemas Externos:**
  - Redis Cache
  - SendGrid (Email)

#### Fluxo Principal (Preferências)

1. **Usuário acessa configurações pessoais**
   - Visualiza preferências atuais
   - Idioma (pt-BR, en-US, es-ES, fr-FR)
   - Tema (Claro, Escuro, Auto)
   - Timezone (America/Sao_Paulo, UTC, etc.)
   - Notificações (Email, Push, SMS)

2. **Usuário altera preferências**
   - Seleciona novo idioma
   - Seleciona novo tema
   - Seleciona novo timezone

3. **Sistema valida preferências**
   - Idioma: deve estar na lista suportada
   - Tema: Claro, Escuro ou Auto
   - Timezone: deve ser válido (IANA timezone)

4. **Sistema salva preferências no banco**
   - Tabela: `UserPreferences`
   - Chaves: UserId, ClienteId, Idioma, Tema, Timezone, Notifications

5. **Sistema invalida cache Redis**
   - Remove preferências antigas do cache
   - Próxima requisição carrega novas preferências

6. **Sistema aplica preferências imediatamente**
   - Frontend recarrega traduções se idioma mudou
   - Frontend aplica novo tema
   - Backend usa novo timezone para formatação de datas

**Fluxo Principal (Alteração de Senha)

1. **Usuário acessa "Alterar Senha"**
   - Digita senha atual
   - Digita nova senha
   - Confirma nova senha

2. **Sistema valida senha atual**
   - Compara com hash BCrypt armazenado
   - Se inválido: retorna erro "Senha atual incorreta"

3. **Sistema valida nova senha**
   - Mínimo 8 caracteres
   - Ao menos 1 letra maiúscula
   - Ao menos 1 letra minúscula
   - Ao menos 1 número
   - Ao menos 1 caractere especial (!@#$%^&*)
   - Não pode ser igual à senha atual

4. **Sistema verifica blacklist de senhas**
   - Consulta lista de top 10.000 senhas mais usadas
   - Exemplos: "12345678", "password", "qwerty"
   - Se encontrada: retorna erro "Senha muito comum"

5. **Sistema verifica confirmação de senha**
   - Nova senha == Confirmação
   - Se diferente: retorna erro "Senhas não conferem"

6. **Sistema hasheia nova senha com BCrypt**
   - Salt automático
   - Cost factor: 12 (segurança vs performance)

7. **Sistema salva nova senha**
   - Atualiza campo `PasswordHash` na tabela `Users`
   - Atualiza campo `PasswordChangedAt` com timestamp atual

8. **Sistema revoga todas as sessões ativas**
   - Remove sessões do Redis
   - Força reautenticação em todos os dispositivos
   - Segurança: se senha foi comprometida, atacante perde acesso

9. **Sistema registra auditoria**
   - Timestamp, UserId, IP, UserAgent
   - Ação: "Alteração de senha"
   - Snapshot: não armazena senha (apenas evento)

10. **Sistema envia notificação por email**
    - Assunto: "Sua senha foi alterada"
    - Corpo: "Se não foi você, acesse o link para reportar"
    - Link: "/security/report-unauthorized-change"

#### Automações

- ✅ **Persistência automática:** Preferências salvas no banco automaticamente
- ✅ **Invalidação de cache:** Redis atualizado após alteração
- ✅ **Validação de senha:** Requisitos OWASP validados automaticamente
- ✅ **Blacklist de senhas:** Consulta automática a lista de senhas comuns
- ✅ **Revogação de sessões:** Todas as sessões revogadas ao trocar senha
- ✅ **Auditoria automática:** Registro completo de alterações de senha
- ✅ **Notificação automática:** Email enviado ao trocar senha

#### Integrações

- **Redis Cache:** Cache de preferências do usuário
- **Sistema de Auditoria (RF004):** Registro imutável de alterações de senha
- **SendGrid:** Notificação por email de alterações sensíveis
- **Sistema de Sessão (RF007):** Revogação de sessões ao trocar senha

#### Regras de Negócio Principais

- **RN-014-01:** Preferências devem ser persistidas no banco por UserId
- **RN-014-02:** Idiomas suportados: pt-BR, en-US, es-ES, fr-FR
- **RN-014-03:** Temas suportados: Claro, Escuro, Auto
- **RN-014-04:** Timezone deve ser válido (IANA timezone)
- **RN-014-05:** Senha nova deve ter mínimo 8 caracteres
- **RN-014-06:** Senha nova deve ter maiúscula, minúscula, número e especial
- **RN-014-07:** Senha nova não pode estar na blacklist de senhas comuns
- **RN-014-08:** Trocar senha revoga todas as sessões ativas
- **RN-014-09:** Notificação por email obrigatória ao trocar senha
- **RN-014-10:** Auditoria completa de alterações de senha

**[Ver regras completas em RF014.md]**

#### Referência ao Legado

**Como funcionava no legado:**
- ❌ Preferências em cookies (perdidas ao expirar)
- ❌ Sem persistência no banco (preferências não sincronizavam entre dispositivos)
- ❌ Senha em MD5 (algoritmo fraco)
- ❌ Sem validação de complexidade de senha
- ❌ Sem blacklist de senhas comuns
- ❌ Sem revogação de sessões ao trocar senha (vulnerável)
- ❌ Sem auditoria de alterações de senha
- ❌ Sem notificação de alterações sensíveis

**Melhorias no moderno:**
- ✅ Preferências persistidas no banco por UserId
- ✅ Sincronização entre dispositivos (mesmo login em múltiplos lugares)
- ✅ BCrypt com salt automático (OWASP recomendado)
- ✅ Validação de complexidade (8+ chars, maiúsc, minúsc, número, especial)
- ✅ Blacklist de top 10.000 senhas comuns
- ✅ Revogação automática de sessões ao trocar senha
- ✅ Auditoria completa de alterações de senha
- ✅ Notificação por email de alterações sensíveis
- ✅ Cache Redis para performance
- ✅ Timezone correto para formatação de datas

---

## 4. Referências Cruzadas

### 4.1 Dependências entre Processos

```mermaid
graph TD
    PRO_INF_006[PRO-INF-006: Gestão de Clientes] --> PRO_INF_001[PRO-INF-001: Parâmetros]
    PRO_INF_006 --> PRO_INF_002[PRO-INF-002: Configurações Gerais]
    PRO_INF_006 --> PRO_INF_004[PRO-INF-004: Auditoria]

    PRO_INF_007[PRO-INF-007: Login e Autenticação] --> PRO_INF_006
    PRO_INF_007 --> PRO_INF_004
    PRO_INF_007 --> PRO_INF_003[PRO-INF-003: Logs]

    PRO_INF_008[PRO-INF-008: Config Usuário] --> PRO_INF_007
    PRO_INF_008 --> PRO_INF_005[PRO-INF-005: i18n]
    PRO_INF_008 --> PRO_INF_004

    PRO_INF_001 --> PRO_INF_004
    PRO_INF_002 --> PRO_INF_004
    PRO_INF_005 --> PRO_INF_004

    style PRO_INF_006 fill:#e1f5ff
    style PRO_INF_007 fill:#ffe1e1
    style PRO_INF_004 fill:#e1ffe1
```

### 4.2 Documentação Relacionada

- **ARCHITECTURE.md:** Stack tecnológico e padrões arquiteturais
- **CONVENTIONS.md:** Nomenclatura e padrões de código
- **COMPLIANCE.md:** Regras de validação e conformidade
- **COMMANDS.md:** Comandos de desenvolvimento e validação

### 4.3 RFs da Jornada

- **RF001:** Parâmetros e Configurações
- **RF002:** Configurações Gerais
- **RF003:** Logs e Monitoramento
- **RF004:** Auditoria de Operações
- **RF005:** Internacionalização (i18n)
- **RF006:** Gestão de Clientes (Multi-Tenancy)
- **RF007:** Login e Autenticação
- **RF014:** Configurações do Usuário

---

## 5. Glossário de Termos Técnicos

| Termo | Descrição |
|-------|-----------|
| **Multi-Tenancy** | Arquitetura onde múltiplos clientes (tenants) compartilham a mesma infraestrutura, mas têm dados isolados por ClienteId |
| **Correlation ID** | UUID único que rastreia uma requisição end-to-end através de múltiplos serviços |
| **Feature Flag** | Configuração que permite ativar/desativar funcionalidades dinamicamente sem deploy |
| **Canary Release** | Estratégia de rollout gradual onde nova funcionalidade é ativada progressivamente (ex: 10% → 50% → 100%) |
| **Hot-Reload** | Aplicação de configurações sem necessidade de reiniciar aplicação |
| **Soft Delete** | Exclusão lógica onde registro é marcado como inativo mas mantido no banco (preserva histórico) |
| **Hard Delete** | Exclusão física onde registro é removido permanentemente do banco |
| **Rate Limiting** | Limitação de requisições por período de tempo (ex: 5 requisições por 15 minutos) |
| **Refresh Token Rotation** | Estratégia de segurança onde refresh token é renovado a cada uso (token antigo é revogado) |
| **OAuth 2.0** | Padrão de mercado para autenticação e autorização |
| **OpenID Connect** | Camada de identidade sobre OAuth 2.0 |
| **MFA (Multi-Factor Authentication)** | Autenticação em múltiplos fatores (senha + código SMS/Email/App) |
| **BCrypt** | Algoritmo de hash de senha com salt automático (OWASP recomendado) |
| **AES-256** | Algoritmo de criptografia simétrica de dados sensíveis |
| **JWT (JSON Web Token)** | Token de acesso contendo claims (UserId, Roles, Permissions) |
| **Métricas RED** | Rate (requisições/s), Errors (taxa de erro), Duration (latência) |
| **Health Check** | Endpoint para verificar status de dependências (DB, Redis, Azure) |
| **Tracing Distribuído** | Rastreamento de requisições através de múltiplos serviços (OpenTelemetry) |
| **Cold Storage** | Armazenamento de longo prazo para dados raramente acessados (Azure Blob Storage) |
| **Hot Storage** | Armazenamento de acesso rápido para dados frequentemente acessados (SQL Server) |

---

## 6. Changelog

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-01-12 | ALC | Versão inicial - Jornada 1 completa (8 processos) |

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 1.0


---

# PARTE 3: JORNADA 2 - WORKFLOWS E IMPORTAÇÃO

---


**Versão:** 1.0
**Data:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente

---

## Sumário

- [1. Introdução](#1-introdução)
- [2. Visão Geral da Jornada](#2-visão-geral-da-jornada)
- [3. Processos da Jornada](#3-processos-da-jornada)
  - [3.1 PRO-WKF-001: Motor de Templates](#31-pro-wkf-001-motor-de-templates)
  - [3.2 PRO-WKF-002: Templates de E-mail](#32-pro-wkf-002-templates-de-e-mail)
  - [3.3 PRO-WKF-003: Templates de Relatórios](#33-pro-wkf-003-templates-de-relatórios)
  - [3.4 PRO-WKF-004: Notificações e Alertas](#34-pro-wkf-004-notificações-e-alertas)
  - [3.5 PRO-WKF-005: Central de E-mails](#35-pro-wkf-005-central-de-e-mails)
  - [3.6 PRO-WKF-006: Upload/Importação de Arquivos](#36-pro-wkf-006-uploadimportação-de-arquivos)
  - [3.7 PRO-WKF-007: Importação de Dados](#37-pro-wkf-007-importação-de-dados)
  - [3.8 PRO-WKF-008: Carga/Importação Massiva](#38-pro-wkf-008-cargaimportação-massiva)
  - [3.9 PRO-WKF-009: Aprovações e Workflows](#39-pro-wkf-009-aprovações-e-workflows)
- [4. Matriz de Processos](#4-matriz-de-processos)
- [5. Glossário](#5-glossário)
- [6. Referências Cruzadas](#6-referências-cruzadas)

---

## 1. Introdução

Este documento detalha os **9 processos de negócio** da **Jornada 2: Workflows e Importação** do sistema IControlIT modernizado.

### Escopo

A Jornada 2 abrange os processos de automação, comunicação e importação de dados:

- **Motor de Templates:** Sistema de renderização dinâmica de conteúdo
- **Templates de E-mail:** Comunicação transacional automatizada
- **Templates de Relatórios:** Geração de documentos e relatórios
- **Notificações e Alertas:** Comunicação multi-canal em tempo real
- **Central de E-mails:** Gestão de filas de envio
- **Upload/Importação de Arquivos:** Gestão de uploads seguros
- **Importação de Dados:** Processamento em lote
- **Carga/Importação Massiva:** Importações de alto volume
- **Aprovações e Workflows:** Fluxos de aprovação configuráveis

### Organização do Documento

Cada processo é documentado com:

- **Código único** (PRO-WKF-XXX)
- **RFs associados**
- **Diagramas BPMN** (Legado vs Moderno)
- **Descrição narrativa**
- **Atores envolvidos**
- **Fluxo principal**
- **Automações implementadas**
- **Integrações**
- **Regras de negócio**
- **Comparação com legado**

---

## 2. Visão Geral da Jornada

### Objetivos da Jornada

1. **Automatizar comunicações:** Templates reutilizáveis para e-mails, relatórios e notificações
2. **Centralizar envios:** Fila unificada de e-mails com retry e auditoria
3. **Facilitar importações:** Uploads seguros e validações automáticas
4. **Escalar importações:** Processamento massivo otimizado
5. **Orquestrar aprovações:** Workflows configuráveis com SLA

### Arquitetura da Jornada

```mermaid
graph TB
    subgraph "Workflows"
        A[Motor de Templates<br/>RF063]
        B[Templates E-mail<br/>RF064]
        C[Templates Relatórios<br/>RF065]
        D[Notificações e Alertas<br/>RF066]
        E[Central de E-mails<br/>RF067]
    end

    subgraph "Importação"
        F[Upload de Arquivos<br/>RF084]
        G[Importação de Dados<br/>RF085]
        H[Carga Massiva<br/>RF086]
    end

    subgraph "Aprovações"
        I[Workflows de Aprovação<br/>RF088]
    end

    A --> B
    A --> C
    B --> E
    D --> E
    F --> G
    G --> H
    I --> D
    I --> E

    style A fill:#4A90E2
    style B fill:#4A90E2
    style C fill:#4A90E2
    style D fill:#4A90E2
    style E fill:#4A90E2
    style F fill:#50C878
    style G fill:#50C878
    style H fill:#50C878
    style I fill:#9B59B6
```

### Stack Tecnológico

- **Backend:** ASP.NET Core 8, MediatR (CQRS), Hangfire (jobs assíncronos)
- **Storage:** Azure Blob Storage (arquivos), SQL Server (metadados)
- **Renderização:** RazorLight (templates), iText7 (PDF), ClosedXML (Excel)
- **Mensageria:** SendGrid/SMTP (e-mail), Twilio (SMS), SignalR (push)
- **Validação:** FluentValidation, AntiVirus (ClamAV)
- **Observabilidade:** Application Insights, Serilog

---

## 3. Processos da Jornada

### 3.1 PRO-WKF-001: Motor de Templates

**Código:** PRO-WKF-001
**RFs Envolvidos:** RF063
**Área:** Workflows
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Desenvolvedor] -->|Hardcoda HTML| B[Código VB.NET]
    B -->|Recompila aplicação| C[Deploy]
    C --> D[Template disponível]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph LR
    A[Administrador] -->|Cria template UI| B[Editor Templates]
    B -->|Salva com versionamento| C[(TemplatesDB)]
    C -->|Compila cache| D[Template Engine]
    D -->|Renderiza| E[HTML/PDF/DOCX]

    F[Aplicação] -->|Solicita renderização| D
    D -->|Interpola variáveis| G{{Variáveis}}
    D -->|Executa condicionais| H{{Lógica}}

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#27AE60
    style D fill:#3498DB
    style E fill:#27AE60
    style F fill:#3498DB
    style G fill:#F39C12
    style H fill:#F39C12
```

#### Descrição do Processo

O Motor de Templates é o núcleo de geração de conteúdo dinâmico do IControlIT. Utiliza a sintaxe `{{variavel}}` para interpolação de dados, suporta condicionais (`{{#if}}`) e loops (`{{#each}}`), e compila templates para melhor performance. Permite versionamento (histórico de alterações) e renderização em múltiplos formatos (HTML, PDF, DOCX).

#### Atores

- **Administrador de Sistema:** Cria e gerencia templates
- **Aplicação:** Solicita renderização de templates
- **Motor de Templates:** Processa e renderiza conteúdo

#### Fluxo Principal

1. Administrador acessa interface de templates no Admin Portal
2. Cria novo template ou edita existente (editor Monaco com syntax highlighting)
3. Define variáveis disponíveis e tipo de output (HTML/PDF/DOCX)
4. Testa renderização com dados de exemplo
5. Salva template (cria nova versão no histórico)
6. Motor compila template para cache otimizado
7. Aplicação solicita renderização via `RenderTemplateCommand`
8. Motor injeta variáveis e executa lógica condicional
9. Retorna conteúdo renderizado

#### Automações

- ✅ Compilação automática de templates para cache
- ✅ Validação de sintaxe ao salvar
- ✅ Versionamento automático com histórico
- ✅ Preview em tempo real no editor
- ✅ Rollback para versões anteriores

#### Integrações

- **RazorLight:** Engine de renderização de templates Razor
- **iText7:** Conversão HTML → PDF
- **ClosedXML:** Geração de Excel
- **DocumentFormat.OpenXml:** Geração de DOCX
- **Azure Blob Storage:** Armazenamento de templates compilados

#### Regras de Negócio Principais

- **RN-063-01:** Templates devem ter nome único por tenant
- **RN-063-02:** Versionamento obrigatório (imutabilidade)
- **RN-063-03:** Variáveis não utilizadas geram warning (não bloqueiam)
- **RN-063-04:** Templates inativos não podem ser renderizados
- **RN-063-05:** Máximo 100 variáveis por template
- **RN-063-06:** Timeout de renderização: 30 segundos
- **RN-063-07:** Cache de templates compilados: 1 hora

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Templates hardcoded em código VB.NET (sem reutilização)
- ❌ Alteração requer recompilação e deploy
- ❌ Sem versionamento ou histórico
- ❌ Apenas HTML (sem PDF/DOCX)
- ❌ Sem validação de sintaxe

**Melhorias no moderno:**

- ✅ Templates gerenciados via UI sem código
- ✅ Alterações instantâneas (sem deploy)
- ✅ Histórico completo de versões
- ✅ Multi-formato (HTML, PDF, DOCX, Excel)
- ✅ Editor com validação e preview em tempo real
- ✅ Performance otimizada com cache compilado

---

### 3.2 PRO-WKF-002: Templates de E-mail

**Código:** PRO-WKF-002
**RFs Envolvidos:** RF064
**Área:** Workflows
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Sistema] -->|Monta HTML manualmente| B[String concatenada]
    B -->|Envia síncrono| C[SMTP]
    C -->|Bloqueia thread| D[Usuário aguarda]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph LR
    A[Sistema] -->|Solicita envio| B[EmailTemplateService]
    B -->|Renderiza template| C[Motor RF063]
    C -->|HTML renderizado| B
    B -->|Enfileira| D[Hangfire Queue]
    D -->|Processa assíncrono| E[EmailSender]
    E -->|Tracking| F[SendGrid API]
    F -->|Webhook| G[Registro abertura/cliques]

    H[Admin] -->|Cria template| I[Template Editor]
    I -->|Salva| J[(TemplatesDB)]

    style A fill:#27AE60
    style B fill:#3498DB
    style C fill:#3498DB
    style D fill:#F39C12
    style E fill:#3498DB
    style F fill:#9B59B6
    style G fill:#27AE60
    style H fill:#27AE60
    style I fill:#27AE60
    style J fill:#27AE60
```

#### Descrição do Processo

Gestão de templates transacionais de e-mail (boas-vindas, redefinição de senha, notificações de sistema, relatórios agendados). Utiliza Motor de Templates (RF063) para renderização, suporta personalização por tenant (logo, cores, rodapé), testes de envio antes de ativar, e tracking de abertura/cliques via SendGrid webhooks.

#### Atores

- **Administrador de Sistema:** Gerencia biblioteca de templates
- **Sistema:** Dispara e-mails transacionais
- **EmailTemplateService:** Orquestra renderização e envio
- **Central de E-mails (RF067):** Processa fila de envio

#### Fluxo Principal

1. Administrador cria template de e-mail na biblioteca
2. Define assunto, remetente e HTML body com variáveis
3. Configura personalização por tenant (opcional)
4. Testa envio para e-mail de validação
5. Ativa template
6. Sistema dispara evento que requer e-mail (ex: novo usuário)
7. `SendEmailCommand` solicita template específico
8. EmailTemplateService renderiza HTML via Motor (RF063)
9. Enfileira na Central de E-mails (RF067)
10. E-mail enviado assíncronamente
11. Webhooks registram abertura/cliques

#### Automações

- ✅ Envio assíncrono via Hangfire (não bloqueia aplicação)
- ✅ Personalização automática por tenant (logo, cores)
- ✅ Tracking automático de abertura e cliques
- ✅ Retry automático em falhas (3 tentativas)
- ✅ Fallback para template padrão se personalizado indisponível

#### Integrações

- **Motor de Templates (RF063):** Renderização de HTML
- **Central de E-mails (RF067):** Fila de envio
- **SendGrid API:** Envio e tracking
- **Hangfire:** Jobs assíncronos
- **Azure Blob Storage:** Armazenamento de anexos

#### Regras de Negócio Principais

- **RN-064-01:** E-mail deve ter assunto e corpo não vazios
- **RN-064-02:** Remetente deve ser e-mail válido do domínio
- **RN-064-03:** Templates inativos não podem ser enviados
- **RN-064-04:** Teste de envio obrigatório antes de ativar template
- **RN-064-05:** Máximo 5 anexos por e-mail (10MB total)
- **RN-064-06:** Variáveis obrigatórias devem estar presentes
- **RN-064-07:** Tracking habilitado por padrão (pode desabilitar)

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ HTML concatenado manualmente em código VB.NET
- ❌ Envio síncrono bloqueava thread (usuário aguardava)
- ❌ Sem tracking de abertura/cliques
- ❌ Sem personalização por tenant
- ❌ Anexos salvos em pasta local (não escalável)
- ❌ Sem retry em falhas

**Melhorias no moderno:**

- ✅ Templates reutilizáveis via biblioteca
- ✅ Envio assíncrono (não bloqueia usuário)
- ✅ Tracking completo de engajamento
- ✅ Personalização automática por tenant
- ✅ Anexos em Azure Blob (escalável)
- ✅ Retry automático e auditoria completa

---

### 3.3 PRO-WKF-003: Templates de Relatórios

**Código:** PRO-WKF-003
**RFs Envolvidos:** RF065
**Área:** Workflows
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Usuário] -->|Solicita relatório| B[Aplicação VB.NET]
    B -->|Query SQL direto| C[(SQL Server)]
    C -->|DataSet| B
    B -->|Crystal Reports| D[Gera PDF]
    D -->|Download síncrono| E[Usuário aguarda 2min+]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph LR
    A[Usuário] -->|Solicita relatório| B[Frontend]
    B -->|GenerateReportCommand| C[ReportService]
    C -->|Query CQRS| D[(SQL Server)]
    D -->|Dados| C
    C -->|Renderiza template| E[Motor RF063]
    E -->|HTML| F[iText7]
    F -->|PDF| G[Azure Blob]
    G -->|URL temporária| H[SignalR Notification]
    H -->|Notifica| B
    B -->|Download| I[Usuário acessa imediato]

    J[Admin] -->|Agenda relatório| K[Hangfire]
    K -->|Executa CRON| C

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#3498DB
    style E fill:#3498DB
    style F fill:#3498DB
    style G fill:#9B59B6
    style H fill:#F39C12
    style I fill:#27AE60
    style J fill:#27AE60
    style K fill:#F39C12
```

#### Descrição do Processo

Geração de relatórios parametrizados com export em múltiplos formatos (PDF, Excel, CSV). Suporta agendamento via CRON, cache de relatórios pesados (evita reprocessamento), assinatura digital (PDF/A), e processamento assíncrono com notificação via SignalR.

#### Atores

- **Usuário:** Solicita geração de relatórios
- **Administrador:** Configura templates e agendamentos
- **ReportService:** Orquestra geração de relatórios
- **Hangfire:** Executa relatórios agendados

#### Fluxo Principal

1. Usuário acessa módulo de relatórios
2. Seleciona template (ex: "Custo Mensal por Departamento")
3. Define parâmetros (período, departamento, formato)
4. Sistema valida parâmetros
5. `GenerateReportCommand` enfileira job assíncrono
6. Backend consulta dados via CQRS query
7. Motor de Templates (RF063) renderiza HTML
8. iText7 converte para PDF (ou ClosedXML para Excel)
9. Arquivo salvo em Azure Blob com URL temporária (24h)
10. SignalR notifica usuário que relatório está pronto
11. Usuário faz download via link temporário

**Fluxo Alternativo: Relatório Agendado**

1. Administrador configura agendamento (ex: "Todo dia 1 às 8h")
2. Hangfire executa job no horário definido
3. Sistema gera relatório com parâmetros salvos
4. Envia relatório por e-mail via RF064
5. Arquiva cópia em Azure Blob

#### Automações

- ✅ Geração assíncrona (não bloqueia UI)
- ✅ Cache de relatórios idênticos (1 hora)
- ✅ Notificação automática via SignalR
- ✅ Agendamento CRON via Hangfire
- ✅ Limpeza automática de arquivos temporários (24h)
- ✅ Compressão automática de relatórios grandes (>10MB)

#### Integrações

- **Motor de Templates (RF063):** Renderização de layout
- **iText7:** Geração de PDF com assinatura digital
- **ClosedXML:** Geração de Excel
- **Azure Blob Storage:** Armazenamento de arquivos
- **SignalR:** Notificação em tempo real
- **Hangfire:** Agendamento de relatórios

#### Regras de Negócio Principais

- **RN-065-01:** Relatórios grandes (>1000 linhas) devem ser assíncronos
- **RN-065-02:** Cache válido por 1 hora para mesmos parâmetros
- **RN-065-03:** URLs temporárias expiram em 24 horas
- **RN-065-04:** Máximo 50.000 linhas por relatório Excel
- **RN-065-05:** PDF/A obrigatório para relatórios financeiros
- **RN-065-06:** Assinatura digital opcional (via certificado A1)
- **RN-065-07:** Timeout de geração: 5 minutos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Crystal Reports (geração síncrona bloqueava aplicação)
- ❌ Timeout frequente em relatórios grandes
- ❌ Sem cache (reprocessamento constante)
- ❌ Apenas PDF (sem Excel/CSV)
- ❌ Arquivos salvos em pasta local (não escalável)
- ❌ Sem agendamento automatizado

**Melhorias no moderno:**

- ✅ Geração assíncrona com notificação
- ✅ Timeout estendido (5 minutos) com retry
- ✅ Cache inteligente (evita reprocessamento)
- ✅ Multi-formato (PDF, Excel, CSV)
- ✅ Azure Blob (escalável e distribuído)
- ✅ Agendamento CRON via Hangfire
- ✅ Assinatura digital integrada

---

### 3.4 PRO-WKF-004: Notificações e Alertas

**Código:** PRO-WKF-004
**RFs Envolvidos:** RF066
**Área:** Workflows
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Evento Sistema] -->|Envia e-mail direto| B[SMTP síncrono]
    B -->|Único canal| C[E-mail]
    C -->|Sem tracking| D[Usuário pode não ver]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Evento Sistema] -->|PublishNotificationEvent| B[NotificationService]
    B -->|Aplica regras| C{Regras de Disparo}
    C -->|Throttling| D{Deduplicação}
    D -->|Envia multi-canal| E[E-mail]
    D -->|Envia multi-canal| F[SMS]
    D -->|Envia multi-canal| G[Push Notification]
    D -->|Envia multi-canal| H[Slack/Teams]

    E --> I[Central E-mails RF067]
    F --> J[Twilio API]
    G --> K[SignalR Hub]
    H --> L[Webhook Integration]

    M[(NotificationsDB)] -->|Registra| N[Histórico]

    style A fill:#27AE60
    style B fill:#3498DB
    style C fill:#F39C12
    style D fill:#F39C12
    style E fill:#9B59B6
    style F fill:#9B59B6
    style G fill:#9B59B6
    style H fill:#9B59B6
    style I fill:#3498DB
    style J fill:#3498DB
    style K fill:#3498DB
    style L fill:#3498DB
    style M fill:#27AE60
    style N fill:#27AE60
```

#### Descrição do Processo

Motor unificado de notificações com suporte a múltiplos canais (e-mail, SMS, push notification, Slack, Microsoft Teams). Implementa regras de disparo configuráveis (ex: "notificar se gasto >R$10k"), throttling (limita notificações por período), deduplicação (evita duplicatas em janela de tempo), e histórico completo de envios.

#### Atores

- **Sistema:** Publica eventos de notificação
- **NotificationService:** Orquestra envio multi-canal
- **Administrador:** Configura regras de disparo
- **Usuário:** Recebe notificações

#### Fluxo Principal

1. Sistema publica evento (ex: `GastoAcimaLimiteEvent`)
2. NotificationService captura evento via handler
3. Consulta regras de disparo configuradas para o tipo de evento
4. Valida se condições são atendidas (ex: valor > R$10.000)
5. Aplica throttling (verifica se última notificação foi há menos de 1h)
6. Aplica deduplicação (verifica se notificação idêntica já foi enviada)
7. Consulta preferências de canal do usuário
8. Renderiza mensagem via template
9. Envia para canais habilitados:
   - **E-mail:** Enfileira em RF067
   - **SMS:** Dispara via Twilio API
   - **Push:** Envia via SignalR para frontend
   - **Slack/Teams:** POST para webhook configurado
10. Registra envio no histórico
11. Tracking de leitura (para push notifications)

#### Automações

- ✅ Disparo automático baseado em eventos
- ✅ Throttling automático (evita spam)
- ✅ Deduplicação em janela de 1 hora
- ✅ Fallback de canal (se SMS falhar, tenta e-mail)
- ✅ Retry automático (3 tentativas)
- ✅ Agrupamento de notificações (digest diário)

#### Integrações

- **Central de E-mails (RF067):** Envio de e-mails
- **Twilio API:** Envio de SMS
- **SignalR Hub:** Push notifications em tempo real
- **Slack Incoming Webhooks:** Notificações Slack
- **Microsoft Teams Webhooks:** Notificações Teams
- **Application Insights:** Tracking de envios

#### Regras de Negócio Principais

- **RN-066-01:** Usuário pode desabilitar canais individualmente
- **RN-066-02:** Throttling padrão: máximo 5 notificações/hora por tipo
- **RN-066-03:** Deduplicação em janela de 1 hora
- **RN-066-04:** Notificações críticas ignoram throttling
- **RN-066-05:** SMS apenas para eventos críticos (custo)
- **RN-066-06:** Push notifications expiram em 24 horas
- **RN-066-07:** Histórico mantido por 90 dias

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Apenas e-mail (canal único)
- ❌ Sem throttling (spam de notificações)
- ❌ Sem deduplicação (notificações duplicadas)
- ❌ Sem histórico ou tracking
- ❌ Regras hardcoded em código
- ❌ Sem preferências de usuário

**Melhorias no moderno:**

- ✅ Multi-canal (e-mail, SMS, push, Slack, Teams)
- ✅ Throttling inteligente (evita spam)
- ✅ Deduplicação automática
- ✅ Histórico completo com tracking
- ✅ Regras configuráveis via UI
- ✅ Preferências de canal por usuário
- ✅ Fallback automático entre canais

---

### 3.5 PRO-WKF-005: Central de E-mails

**Código:** PRO-WKF-005
**RFs Envolvidos:** RF067
**Área:** Workflows
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Sistema] -->|Envia síncrono| B[SMTP direto]
    B -->|Falha?| C[Erro perdido]
    B -->|Sucesso?| D[Sem log]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Sistema] -->|Enfileira| B[Hangfire Queue]
    B -->|Priority Queue| C{Email Sender Job}
    C -->|Tenta envio| D[SendGrid API]
    D -->|Sucesso| E[Marca como Enviado]
    D -->|Falha| F{Retry Count < 3?}
    F -->|Sim| G[Aguarda backoff]
    G -->|Re-enfileira| B
    F -->|Não| H[Marca como Falhado]

    I[Webhook SendGrid] -->|Bounce/Complaint| J[Blacklist Service]
    J -->|Adiciona| K[(Blacklist DB)]

    L[Admin] -->|Consulta| M[Dashboard E-mails]
    M -->|Exibe| N[Logs e Métricas]

    style A fill:#27AE60
    style B fill:#F39C12
    style C fill:#3498DB
    style D fill:#9B59B6
    style E fill:#27AE60
    style F fill:#F39C12
    style G fill:#F39C12
    style H fill:#E74C3C
    style I fill:#9B59B6
    style J fill:#3498DB
    style K fill:#27AE60
    style L fill:#27AE60
    style M fill:#27AE60
    style N fill:#27AE60
```

#### Descrição do Processo

Fila unificada de envio de e-mails com processamento assíncrono via Hangfire. Implementa retry automático com backoff exponencial (1min, 5min, 15min), registra logs completos de envio, processa bounces e complaints via webhooks do SendGrid, e mantém blacklist automática de e-mails inválidos.

#### Atores

- **Sistema:** Enfileira e-mails para envio
- **Hangfire:** Processa fila de envio
- **EmailSender Job:** Executa envio via SendGrid
- **SendGrid Webhooks:** Reporta bounces e complaints
- **Administrador:** Monitora dashboard de e-mails

#### Fluxo Principal

1. Sistema solicita envio de e-mail via `SendEmailCommand`
2. E-mail validado e enfileirado no Hangfire
3. Job `EmailSenderJob` processa fila (ordem de prioridade)
4. Verifica se destinatário não está em blacklist
5. Tenta envio via SendGrid API
6. **Cenário sucesso:**
   - Marca e-mail como `Sent`
   - Registra log de envio
   - Aguarda webhooks de tracking
7. **Cenário falha:**
   - Incrementa contador de retry
   - Se retry < 3: Re-enfileira com backoff (1min, 5min, 15min)
   - Se retry = 3: Marca como `Failed` e notifica administrador
8. Webhooks do SendGrid reportam eventos:
   - **Bounce:** Adiciona e-mail à blacklist
   - **Complaint (spam):** Adiciona e-mail à blacklist
   - **Open/Click:** Registra engajamento

#### Automações

- ✅ Retry automático com backoff exponencial (1min, 5min, 15min)
- ✅ Blacklist automática em bounces e complaints
- ✅ Limpeza automática de e-mails enviados após 90 dias
- ✅ Alertas automáticos para taxa de falha > 5%
- ✅ Priorização automática (e-mails críticos primeiro)

#### Integrações

- **Hangfire:** Fila de jobs assíncronos
- **SendGrid API:** Envio de e-mails
- **SendGrid Webhooks:** Eventos de bounce, complaint, open, click
- **Azure Blob Storage:** Armazenamento de anexos
- **Application Insights:** Métricas de envio

#### Regras de Negócio Principais

- **RN-067-01:** Máximo 3 tentativas de envio
- **RN-067-02:** Backoff exponencial: 1min, 5min, 15min
- **RN-067-03:** E-mails em blacklist não são enviados
- **RN-067-04:** Bounce hard adiciona à blacklist permanente
- **RN-067-05:** Bounce soft permite retry (caixa cheia)
- **RN-067-06:** Complaints (spam) adicionam à blacklist
- **RN-067-07:** Logs mantidos por 90 dias
- **RN-067-08:** Prioridade: Crítico > Normal > Baixa

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Envio síncrono (bloqueava aplicação)
- ❌ Sem retry em falhas
- ❌ Erros perdidos (sem log)
- ❌ Sem blacklist (enviava para e-mails inválidos)
- ❌ Sem tracking de bounces/complaints
- ❌ Sem priorização

**Melhorias no moderno:**

- ✅ Envio assíncrono via fila (não bloqueia)
- ✅ Retry automático com backoff inteligente
- ✅ Logs completos de todos os envios
- ✅ Blacklist automática (economiza recursos)
- ✅ Tracking completo via webhooks
- ✅ Priorização de e-mails críticos
- ✅ Dashboard de monitoramento em tempo real

---

### 3.6 PRO-WKF-006: Upload/Importação de Arquivos

**Código:** PRO-WKF-006
**RFs Envolvidos:** RF084
**Área:** Importação
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Usuário] -->|Upload 2MB max| B[IIS]
    B -->|Salva| C[Pasta Local C:\Uploads]
    C -->|Sem validação| D[Arquivo aceito]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Usuário] -->|Upload chunked| B[Frontend]
    B -->|Envia chunks 5MB| C[FileUploadController]
    C -->|Valida extensão| D{Arquivo permitido?}
    D -->|Não| E[Rejeita upload]
    D -->|Sim| F[Salva chunk temporário]
    F -->|Todos chunks?| G[Monta arquivo completo]
    G -->|Scan antivírus| H{ClamAV}
    H -->|Vírus detectado| I[Deleta e notifica]
    H -->|Limpo| J[Upload para Azure Blob]
    J -->|Gera URL SAS| K[Retorna para frontend]
    K -->|Processa assíncrono| L[Hangfire Job]
    L -->|Importação| M[RF085/RF086]

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#3498DB
    style D fill:#F39C12
    style E fill:#E74C3C
    style F fill:#3498DB
    style G fill:#3498DB
    style H fill:#9B59B6
    style I fill:#E74C3C
    style J fill:#9B59B6
    style K fill:#27AE60
    style L fill:#F39C12
    style M fill:#3498DB
```

#### Descrição do Processo

Sistema de upload seguro de arquivos com suporte a uploads grandes via chunking (divide arquivo em partes de 5MB), validação de extensão e tamanho, scan de antivírus via ClamAV, armazenamento em Azure Blob Storage, e processamento assíncrono via Hangfire.

#### Atores

- **Usuário:** Faz upload de arquivos
- **Frontend:** Gerencia chunking e progress bar
- **FileUploadController:** Recebe e valida chunks
- **ClamAV:** Escaneia arquivos por vírus
- **Azure Blob Storage:** Armazena arquivos

#### Fluxo Principal

1. Usuário seleciona arquivo (ex: CSV de 50MB)
2. Frontend divide arquivo em chunks de 5MB
3. Envia chunks sequencialmente via HTTP POST
4. Backend valida cada chunk:
   - Extensão permitida (.csv, .xlsx, .txt, .pdf, .zip)
   - Tamanho individual < 5MB
   - Tamanho total acumulado < 500MB
5. Salva chunks em storage temporário
6. Quando último chunk recebido:
   - Monta arquivo completo
   - Calcula hash SHA256
   - Executa scan ClamAV
7. **Cenário vírus detectado:**
   - Deleta arquivo
   - Notifica usuário via SignalR
   - Registra tentativa em log de segurança
8. **Cenário arquivo limpo:**
   - Upload para Azure Blob Storage
   - Gera URL SAS (validade 24 horas)
   - Retorna URL para frontend
9. Frontend notifica usuário: "Upload concluído"
10. Sistema enfileira job de processamento (RF085/RF086)

#### Automações

- ✅ Chunking automático de arquivos grandes
- ✅ Scan antivírus obrigatório
- ✅ Upload paralelo para Azure Blob
- ✅ Limpeza automática de chunks temporários
- ✅ Notificação em tempo real via SignalR
- ✅ Geração automática de URL SAS

#### Integrações

- **Azure Blob Storage:** Armazenamento de arquivos
- **ClamAV:** Antivírus
- **Hangfire:** Processamento assíncrono
- **SignalR:** Notificações em tempo real
- **Application Insights:** Métricas de upload

#### Regras de Negócio Principais

- **RN-084-01:** Extensões permitidas: .csv, .xlsx, .txt, .pdf, .zip, .xml
- **RN-084-02:** Tamanho máximo por arquivo: 500MB
- **RN-084-03:** Chunk size: 5MB
- **RN-084-04:** Scan antivírus obrigatório
- **RN-084-05:** Arquivos com vírus são deletados imediatamente
- **RN-084-06:** URL SAS expira em 24 horas
- **RN-084-07:** Chunks temporários deletados após 1 hora
- **RN-084-08:** Timeout de upload: 30 minutos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Limite de 2MB (IIS)
- ❌ Arquivos salvos em pasta local (não escalável)
- ❌ Sem scan de antivírus
- ❌ Sem validação de extensão
- ❌ Upload síncrono (bloqueava aplicação)
- ❌ Sem progress bar

**Melhorias no moderno:**

- ✅ Suporte a arquivos de até 500MB via chunking
- ✅ Azure Blob Storage (escalável e distribuído)
- ✅ Scan antivírus obrigatório (ClamAV)
- ✅ Validação rigorosa de extensão e tamanho
- ✅ Upload assíncrono com retry
- ✅ Progress bar em tempo real via SignalR

---

### 3.7 PRO-WKF-007: Importação de Dados

**Código:** PRO-WKF-007
**RFs Envolvidos:** RF085
**Área:** Importação
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Usuário] -->|Copia Excel| B[Ctrl+C / Ctrl+V]
    B -->|Cola no grid| C[Aplicação VB.NET]
    C -->|INSERT linha por linha| D[(SQL Server)]
    D -->|Timeout| E[Erro parcial]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Usuário] -->|Upload CSV/Excel| B[Frontend]
    B -->|Arquivo Azure Blob| C[ImportDataCommand]
    C -->|Parse arquivo| D[FileParser Service]
    D -->|Valida estrutura| E{Validação Prévia}
    E -->|Erro estrutura| F[Relatório erros]
    E -->|OK| G[Mapeia colunas]
    G -->|Validação linha a linha| H{Validação Dados}
    H -->|Erros encontrados| I[Relatório detalhado]
    H -->|Todos válidos| J[Inicia transação]
    J -->|Batch insert| K[(SQL Server)]
    K -->|Sucesso| L[Commit]
    K -->|Erro| M[Rollback total]
    L -->|Notifica| N[SignalR: Sucesso]
    M -->|Notifica| O[SignalR: Falha]

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#3498DB
    style D fill:#3498DB
    style E fill:#F39C12
    style F fill:#E74C3C
    style G fill:#3498DB
    style H fill:#F39C12
    style I fill:#E74C3C
    style J fill:#3498DB
    style K fill:#9B59B6
    style L fill:#27AE60
    style M fill:#E74C3C
    style N fill:#27AE60
    style O fill:#E74C3C
```

#### Descrição do Processo

Importação estruturada de dados em lote (CSV, Excel) com validação pré-importação (estrutura e dados), mapeamento flexível de colunas (permite renomear colunas na UI), transação atômica (rollback total em caso de erro), e relatório detalhado de importação com linhas processadas/erros.

#### Atores

- **Usuário:** Realiza importação de dados
- **ImportDataCommand:** Orquestra importação
- **FileParserService:** Parseia CSV/Excel
- **ValidationService:** Valida dados
- **BatchRepository:** Executa insert em lote

#### Fluxo Principal

1. Usuário faz upload de arquivo CSV/Excel (via RF084)
2. Seleciona tipo de importação (ex: "Usuários", "Centros de Custo")
3. Sistema exibe preview das primeiras 10 linhas
4. Usuário mapeia colunas (arrasta/solta para corresponder campos)
5. Clica em "Iniciar Importação"
6. `ImportDataCommand` enfileira job assíncrono
7. **Validação Prévia:**
   - Valida estrutura do arquivo (colunas obrigatórias presentes?)
   - Valida tipos de dados (texto, número, data)
   - Se erros: retorna relatório e PARA importação
8. **Validação Linha a Linha:**
   - Aplica FluentValidation em cada registro
   - Valida regras de negócio (ex: e-mail único)
   - Acumula erros
9. **Cenário com erros:**
   - Gera relatório Excel com linhas inválidas e motivos
   - Notifica usuário via SignalR
   - PARA importação (não insere nada)
10. **Cenário sem erros:**
    - Inicia transação SQL
    - Executa batch insert (1000 registros por vez)
    - Commit
    - Notifica usuário: "1500 registros importados com sucesso"

#### Automações

- ✅ Detecção automática de encoding (UTF-8, ISO-8859-1)
- ✅ Detecção automática de delimitador (vírgula, ponto-vírgula, tab)
- ✅ Sugestão automática de mapeamento de colunas
- ✅ Validação assíncrona (não bloqueia UI)
- ✅ Rollback automático em caso de erro
- ✅ Geração automática de relatório de erros

#### Integrações

- **RF084:** Upload de arquivos
- **ClosedXML:** Parse de Excel
- **CsvHelper:** Parse de CSV
- **FluentValidation:** Validação de dados
- **EF Core:** Batch insert otimizado
- **SignalR:** Notificação de progresso

#### Regras de Negócio Principais

- **RN-085-01:** Importação é transacional (all-or-nothing)
- **RN-085-02:** Validação prévia obrigatória
- **RN-085-03:** Máximo 10.000 linhas por importação padrão
- **RN-085-04:** Erros param importação (não insere parcialmente)
- **RN-085-05:** Relatório de erros gerado automaticamente
- **RN-085-06:** Mapeamento de colunas obrigatório
- **RN-085-07:** Timeout de importação: 10 minutos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Copiar/colar manual (propenso a erros)
- ❌ INSERT linha por linha (lento)
- ❌ Sem validação prévia (erros só no banco)
- ❌ Importações parciais (inconsistência)
- ❌ Sem relatório de erros
- ❌ Timeout frequente

**Melhorias no moderno:**

- ✅ Upload estruturado de arquivos
- ✅ Batch insert otimizado (50x mais rápido)
- ✅ Validação prévia antes de inserir
- ✅ Transação atômica (rollback total)
- ✅ Relatório detalhado de erros
- ✅ Mapeamento flexível de colunas
- ✅ Processamento assíncrono sem timeout

---

### 3.8 PRO-WKF-008: Carga/Importação Massiva

**Código:** PRO-WKF-008
**RFs Envolvidos:** RF086
**Área:** Importação
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Usuário] -->|Importação 50k linhas| B[Aplicação VB.NET]
    B -->|Loop linha por linha| C[(SQL Server)]
    C -->|Timeout após 10min| D[Erro e rollback]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Usuário] -->|Upload CSV 100k linhas| B[Frontend]
    B -->|Arquivo Azure Blob| C[MassiveImportCommand]
    C -->|Divide em batches| D[Batch Processor]
    D -->|Batch 1-5000| E[Job 1]
    D -->|Batch 5001-10000| F[Job 2]
    D -->|Batch 10001-15000| G[Job N]

    E -->|SqlBulkCopy| H[(SQL Server)]
    F -->|SqlBulkCopy| H
    G -->|SqlBulkCopy| H

    H -->|Progress| I[SignalR Hub]
    I -->|Atualiza| J[Progress Bar]

    K[Validation Service] -->|Valida incremental| D
    K -->|Erros| L[Log de Erros]

    H -->|Sucesso| M[Relatório Final]
    L -->|Falhas| M

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#3498DB
    style D fill:#3498DB
    style E fill:#F39C12
    style F fill:#F39C12
    style G fill:#F39C12
    style H fill:#9B59B6
    style I fill:#3498DB
    style J fill:#27AE60
    style K fill:#F39C12
    style L fill:#E74C3C
    style M fill:#27AE60
```

#### Descrição do Processo

Importação de alto volume (até 100.000 linhas) com processamento batch otimizado via SqlBulkCopy, divisão em jobs paralelos (5000 linhas por batch), validação incremental (não carrega tudo em memória), progress bar em tempo real via SignalR, e log detalhado de erros sem parar importação.

#### Atores

- **Usuário:** Solicita importação massiva
- **MassiveImportCommand:** Orquestra importação
- **BatchProcessor:** Divide e processa batches
- **SqlBulkCopy:** Executa insert massivo otimizado
- **SignalR Hub:** Reporta progresso em tempo real

#### Fluxo Principal

1. Usuário faz upload de arquivo grande (ex: 50.000 linhas)
2. Sistema detecta que é importação massiva (>10.000 linhas)
3. Exibe alerta: "Importação massiva detectada. Processamento pode levar alguns minutos."
4. `MassiveImportCommand` enfileira job Hangfire
5. Job divide arquivo em batches de 5000 linhas
6. Cria jobs paralelos (máximo 3 simultâneos)
7. **Processamento de cada batch:**
   - Lê 5000 linhas do arquivo
   - Valida linha a linha
   - Linhas válidas: adiciona a DataTable
   - Linhas inválidas: registra em log de erros
   - Executa SqlBulkCopy para inserir batch
   - Reporta progresso via SignalR: "15000/50000 (30%)"
8. Quando todos batches concluídos:
   - Gera relatório final:
     - Total processado: 50.000
     - Inseridos: 48.500
     - Erros: 1.500
   - Anexa log de erros (Excel com linhas inválidas)
   - Notifica usuário via SignalR

#### Automações

- ✅ Detecção automática de importação massiva (>10k linhas)
- ✅ Divisão automática em batches otimizados
- ✅ Processamento paralelo (3 jobs simultâneos)
- ✅ Progress bar em tempo real
- ✅ SqlBulkCopy para performance máxima
- ✅ Validação incremental (não carrega tudo em memória)
- ✅ Geração automática de relatório de erros

#### Integrações

- **RF084:** Upload de arquivos grandes
- **SqlBulkCopy:** Insert massivo otimizado
- **Hangfire:** Processamento assíncrono
- **SignalR:** Progress bar em tempo real
- **ClosedXML:** Geração de relatório de erros
- **Azure Blob Storage:** Armazenamento de logs

#### Regras de Negócio Principais

- **RN-086-01:** Importação massiva: >10.000 linhas
- **RN-086-02:** Batch size: 5000 linhas
- **RN-086-03:** Máximo 3 batches paralelos
- **RN-086-04:** Validação incremental (não bloqueia memória)
- **RN-086-05:** Erros não param importação (modo best-effort)
- **RN-086-06:** Log de erros gerado automaticamente
- **RN-086-07:** Máximo 100.000 linhas por importação
- **RN-086-08:** Timeout de batch: 5 minutos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ INSERT linha por linha (extremamente lento)
- ❌ Timeout garantido em >10k linhas
- ❌ Sem progress bar (usuário sem feedback)
- ❌ Carrega tudo em memória (crash)
- ❌ Erro em uma linha para tudo (rollback total)
- ❌ Sem relatório de erros

**Melhorias no moderno:**

- ✅ SqlBulkCopy (100x mais rápido)
- ✅ Sem timeout (processamento assíncrono)
- ✅ Progress bar em tempo real
- ✅ Validação incremental (memória controlada)
- ✅ Modo best-effort (erros não param importação)
- ✅ Relatório detalhado de erros
- ✅ Suporte até 100k linhas

---

### 3.9 PRO-WKF-009: Aprovações e Workflows

**Código:** PRO-WKF-009
**RFs Envolvidos:** RF088
**Área:** Workflows
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Solicitante] -->|Envia e-mail| B[Aprovador]
    B -->|Responde e-mail| C[Solicitante]
    C -->|Atualiza manualmente| D[Sistema]
    D -->|Sem rastreamento| E[Histórico perdido]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Solicitante] -->|Cria solicitação| B[Frontend]
    B -->|CreateApprovalRequest| C[WorkflowService]
    C -->|Determina alçada| D{Workflow Engine}
    D -->|Valor < 10k| E[Aprovador Nível 1]
    D -->|Valor 10k-50k| F[Aprovador Nível 2]
    D -->|Valor > 50k| G[Aprovador Nível 3]

    E -->|Aprova| H[Próximo nível?]
    E -->|Rejeita| I[Notifica Solicitante]

    H -->|Sim| F
    H -->|Não| J[Finaliza: Aprovado]

    F -->|Aprova| K[Próximo nível?]
    F -->|Rejeita| I

    K -->|Sim| G
    K -->|Não| J

    G -->|Aprova| J
    G -->|Rejeita| I

    L[SLA Monitor] -->|Verifica pendências| M{SLA excedido?}
    M -->|Sim| N[Escalação automática]
    N -->|Notifica| O[Gestor Superior]

    P[Notificação Service] -->|E-mail/Push| E
    P -->|E-mail/Push| F
    P -->|E-mail/Push| G

    style A fill:#27AE60
    style B fill:#27AE60
    style C fill:#3498DB
    style D fill:#F39C12
    style E fill:#9B59B6
    style F fill:#9B59B6
    style G fill:#9B59B6
    style H fill:#F39C12
    style I fill:#E74C3C
    style J fill:#27AE60
    style K fill:#F39C12
    style L fill:#F39C12
    style M fill:#F39C12
    style N fill:#E74C3C
    style O fill:#9B59B6
    style P fill:#3498DB
```

#### Descrição do Processo

Sistema configurável de aprovações com state machine (Pending → Approved/Rejected/Escalated), alçadas automáticas por valor, delegação de aprovadores (férias/ausência), SLA de aprovação (ex: 48 horas) com escalação automática, e notificações multi-canal (e-mail, push, Slack).

#### Atores

- **Solicitante:** Cria solicitação de aprovação
- **Aprovador(es):** Aprovam ou rejeitam solicitações
- **WorkflowService:** Orquestra fluxo de aprovação
- **SLA Monitor:** Monitora prazos e escala pendências
- **NotificationService (RF066):** Notifica participantes

#### Fluxo Principal

1. Solicitante cria solicitação (ex: "Compra de Licenças - R$25.000")
2. `CreateApprovalRequestCommand` processa solicitação
3. WorkflowService determina alçada baseada em regras:
   - Valor < R$10.000: Nível 1 (Coordenador)
   - Valor R$10.000 - R$50.000: Nível 2 (Gerente)
   - Valor > R$50.000: Nível 3 (Diretor)
4. Sistema identifica aprovadores:
   - Consulta hierarquia organizacional
   - Verifica delegações ativas (aprovador de férias?)
   - Seleciona aprovador disponível
5. Notifica aprovador via RF066 (e-mail + push)
6. Aprovador acessa painel "Minhas Aprovações"
7. Visualiza detalhes da solicitação (anexos, justificativa)
8. **Cenário 1: Aprovação**
   - Clica em "Aprovar"
   - Adiciona comentário (opcional)
   - Sistema verifica se há próximo nível
   - Se sim: notifica próximo aprovador
   - Se não: finaliza como "Aprovado"
9. **Cenário 2: Rejeição**
   - Clica em "Rejeitar"
   - Adiciona justificativa (obrigatória)
   - Sistema finaliza como "Rejeitado"
   - Notifica solicitante
10. **Cenário 3: SLA Excedido**
    - SLA Monitor detecta pendência > 48h
    - Executa escalação automática
    - Notifica gestor superior
    - Gestor pode assumir aprovação ou pressionar aprovador

#### Automações

- ✅ Determinação automática de alçada por regras
- ✅ Identificação automática de aprovadores via hierarquia
- ✅ Delegação automática (aprovador ausente → substituto)
- ✅ Notificações automáticas multi-canal
- ✅ Escalação automática por SLA
- ✅ Lembretes diários para pendências
- ✅ Auditoria completa de todas ações

#### Integrações

- **NotificationService (RF066):** Notificações multi-canal
- **Central de E-mails (RF067):** Envio de e-mails de aprovação
- **Hangfire:** Jobs de SLA monitor
- **SignalR:** Atualização em tempo real do painel
- **Azure AD:** Hierarquia organizacional

#### Regras de Negócio Principais

- **RN-088-01:** Alçadas configuráveis por tipo de solicitação
- **RN-088-02:** Delegação obrigatória ao sair de férias
- **RN-088-03:** SLA padrão: 48 horas úteis
- **RN-088-04:** Escalação automática após SLA excedido
- **RN-088-05:** Justificativa obrigatória em rejeições
- **RN-088-06:** Aprovador não pode aprovar própria solicitação
- **RN-088-07:** Histórico de aprovações imutável (auditoria)
- **RN-088-08:** Notificações diárias de pendências (9h AM)

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Aprovações via e-mail (sem rastreamento)
- ❌ Sem alçadas automáticas (sempre manual)
- ❌ Sem delegação (aprovações travavam em férias)
- ❌ Sem SLA ou escalação
- ❌ Histórico perdido (e-mails deletados)
- ❌ Sem auditoria

**Melhorias no moderno:**

- ✅ Aprovações rastreadas em sistema
- ✅ Alçadas automáticas por regras configuráveis
- ✅ Delegação automática (substituto assume)
- ✅ SLA com escalação automática
- ✅ Histórico completo e imutável
- ✅ Auditoria completa (quem, quando, o quê)
- ✅ Dashboard de aprovações em tempo real

---

## 4. Matriz de Processos

| Código | Processo | RF | Criticidade | Automação | Integrações |
|--------|----------|----|-----------|-----------| ------------|
| **PRO-WKF-001** | Motor de Templates | RF063 | Alta | ✅ Compilação cache, versionamento | RazorLight, iText7, ClosedXML |
| **PRO-WKF-002** | Templates de E-mail | RF064 | Alta | ✅ Envio assíncrono, tracking | RF063, RF067, SendGrid |
| **PRO-WKF-003** | Templates de Relatórios | RF065 | Média | ✅ Cache, agendamento CRON | RF063, iText7, Hangfire |
| **PRO-WKF-004** | Notificações e Alertas | RF066 | Alta | ✅ Throttling, deduplicação | RF067, Twilio, SignalR, Slack |
| **PRO-WKF-005** | Central de E-mails | RF067 | Alta | ✅ Retry, blacklist, webhooks | SendGrid, Hangfire |
| **PRO-WKF-006** | Upload/Importação de Arquivos | RF084 | Alta | ✅ Chunking, antivírus, SAS | Azure Blob, ClamAV, SignalR |
| **PRO-WKF-007** | Importação de Dados | RF085 | Alta | ✅ Validação prévia, rollback | RF084, FluentValidation, EF Core |
| **PRO-WKF-008** | Carga/Importação Massiva | RF086 | Média | ✅ Batch paralelo, SqlBulkCopy | RF084, Hangfire, SignalR |
| **PRO-WKF-009** | Aprovações e Workflows | RF088 | Alta | ✅ Alçadas, SLA, escalação | RF066, RF067, Hangfire |

---

## 5. Glossário

| Termo | Definição |
|-------|-----------|
| **Alçada** | Limite de valor/escopo que determina nível de aprovação necessário |
| **Batch Insert** | Inserção de múltiplos registros em uma única operação SQL |
| **Blacklist** | Lista de e-mails bloqueados por bounces ou complaints |
| **Bounce** | E-mail retornado por caixa inexistente (hard) ou temporariamente indisponível (soft) |
| **Chunking** | Divisão de arquivo grande em partes menores para upload |
| **Complaint** | Marcação de e-mail como spam pelo destinatário |
| **CQRS** | Command Query Responsibility Segregation (separação comando/consulta) |
| **Delegação** | Transferência temporária de responsabilidade de aprovação |
| **Deduplicação** | Eliminação de notificações duplicadas em janela de tempo |
| **Escalação** | Transferência de aprovação para nível superior por SLA excedido |
| **Interpolação** | Substituição de variáveis `{{nome}}` por valores reais |
| **SAS (Shared Access Signature)** | URL temporária com permissões para acesso a recurso Azure |
| **SLA (Service Level Agreement)** | Prazo máximo para conclusão de tarefa |
| **SqlBulkCopy** | API .NET para inserção massiva otimizada no SQL Server |
| **State Machine** | Máquina de estados que controla transições de workflow |
| **Template** | Modelo reutilizável com variáveis para geração de conteúdo |
| **Throttling** | Limitação de taxa de envio para evitar spam |
| **Tracking** | Rastreamento de abertura e cliques em e-mails |
| **Webhook** | Callback HTTP para notificação de eventos externos |

---

## 6. Referências Cruzadas

### Jornadas Relacionadas

- **Jornada 1:** Gestão de Clientes e Organizações (PRO-CLI-001 a PRO-CLI-011)
- **Jornada 3:** Gestão de Usuários e Permissões (a documentar)
- **Jornada 4:** Gestão de Ativos e Inventário (a documentar)

### Documentos de Governança

| Documento | Caminho | Relevância |
|-----------|---------|-----------|
| **ARCHITECTURE.md** | `D:\IC2_Governanca\governanca\ARCHITECTURE.md` | Stack tecnológico, padrões arquiteturais |
| **CONVENTIONS.md** | `D:\IC2_Governanca\governanca\CONVENTIONS.md` | Nomenclatura de handlers, repositories |
| **COMPLIANCE.md** | `D:\IC2_Governanca\governanca\COMPLIANCE.md` | Regras de validação e auditoria |
| **COMMANDS.md** | `D:\IC2_Governanca\governanca\COMMANDS.md` | Comandos de desenvolvimento e validação |

### RFs Relacionados

| RF | Título | Status |
|----|--------|--------|
| **RF063** | Motor de Templates | ✅ Implementado |
| **RF064** | Templates de E-mail | ✅ Implementado |
| **RF065** | Templates de Relatórios | ✅ Implementado |
| **RF066** | Notificações e Alertas | ✅ Implementado |
| **RF067** | Central de E-mails | ✅ Implementado |
| **RF084** | Upload/Importação de Arquivos | ✅ Implementado |
| **RF085** | Importação de Dados | ✅ Implementado |
| **RF086** | Carga/Importação Massiva | ✅ Implementado |
| **RF088** | Aprovações e Workflows | ✅ Implementado |

### Contratos de Execução

Para implementar ou manter processos desta jornada, consulte:

- **Backend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\backend-criacao.md`
- **Frontend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\frontend-criacao.md`
- **Manutenção:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\manutencao\CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md`
- **Auditoria:** `D:\IC2_Governanca\governanca\contracts\auditoria\conformidade.md`

---

## Controle de Versão

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-01-12 | ALC | Criação inicial com 9 processos da Jornada 2 |

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 1.0


---

# PARTE 4: JORNADA 3 - FINANCEIRO COMPLETO

---


**Versão:** 1.0
**Data:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente

---

## Sumário

- [1. Introdução](#1-introdução)
- [2. Visão Geral da Jornada](#2-visão-geral-da-jornada)
- [3. Processos da Jornada](#3-processos-da-jornada)
  - [PARTE 1: CONTRATOS E FATURAMENTO](#parte-1-contratos-e-faturamento)
  - [PARTE 2: ATIVOS E CUSTOS](#parte-2-ativos-e-custos)
- [4. Matriz de Processos](#4-matriz-de-processos)
- [5. Glossário](#5-glossário)
- [6. Referências Cruzadas](#6-referências-cruzadas)

---

## 1. Introdução

Este documento detalha os **12 processos de negócio** da **Jornada 3: Financeiro Completo** do sistema IControlIT modernizado.

### Escopo

A Jornada 3 abrange dois domínios financeiros críticos:

**PARTE 1: Contratos e Faturamento (7 processos PRO-FCT)**
- Gestão de Faturas
- Parâmetros de Faturamento
- Plano de Contas
- Notas Fiscais/Faturas (NF-e)
- Conciliação de Faturas
- Medição/Faturamento de Contratos
- Auditoria de Faturas

**PARTE 2: Ativos e Custos (5 processos PRO-FAC)**
- Gestão de Ativos
- Custos Fixos
- Custos por Ativo (TCO)
- Notas Fiscais de Estoque
- Rateio Multi-dimensional

### Organização do Documento

Cada processo é documentado com:

- **Código único** (PRO-FCT-XXX ou PRO-FAC-XXX)
- **RFs associados**
- **Diagramas BPMN** (Legado vs Moderno)
- **Descrição narrativa**
- **Atores envolvidos**
- **Fluxo principal**
- **Automações implementadas**
- **Integrações**
- **Regras de negócio**
- **Comparação com legado**

---

## 2. Visão Geral da Jornada

### Objetivos da Jornada

1. **Automatizar faturamento:** Geração, conciliação e baixa automática de faturas
2. **Integrar SEFAZ:** Emissão de NF-e via WebService oficial
3. **Calcular TCO:** Total Cost of Ownership automático por ativo
4. **Ratear custos:** Alocação multi-dimensional em tempo real
5. **Auditar financeiro:** Validação preventiva de não-conformidades

### Arquitetura da Jornada

```mermaid
graph TB
    subgraph "Contratos e Faturamento"
        A[Gestão de Faturas<br/>RF026]
        B[Parâmetros Faturamento<br/>RF030]
        C[Plano de Contas<br/>RF031]
        D[NF-e<br/>RF032]
        E[Conciliação Faturas<br/>RF089]
        F[Medição/Faturamento<br/>RF090]
        G[Auditoria Faturas<br/>RF097]
    end

    subgraph "Ativos e Custos"
        H[Gestão Ativos<br/>RF025]
        I[Custos Fixos<br/>RF036]
        J[TCO<br/>RF037]
        K[NF Estoque<br/>RF042]
        L[Rateio Multi-dimensional<br/>RF055]
    end

    A --> E
    A --> D
    B --> F
    C --> A
    F --> A
    F --> E
    A --> G

    H --> J
    I --> L
    J --> L
    K --> H

    style A fill:#4A90E2
    style B fill:#4A90E2
    style C fill:#4A90E2
    style D fill:#4A90E2
    style E fill:#4A90E2
    style F fill:#4A90E2
    style G fill:#4A90E2
    style H fill:#50C878
    style I fill:#50C878
    style J fill:#50C878
    style K fill:#50C878
    style L fill:#50C878
```

### Stack Tecnológico

- **Backend:** ASP.NET Core 8, MediatR (CQRS), Hangfire (jobs)
- **Financeiro:** WebService SEFAZ (NF-e), OFX Parser (conciliação bancária)
- **Cálculos:** Motor de rateio customizado, depreciação automática
- **Storage:** SQL Server (transacional), Azure Blob (XMLs NF-e)
- **Integrações:** TOTVS, SAP, ERP legado via API REST
- **Observabilidade:** Application Insights, Serilog

---

## 3. Processos da Jornada

## PARTE 1: CONTRATOS E FATURAMENTO

### 3.1 PRO-FCT-001: Gestão de Faturas

**Código:** PRO-FCT-001
**RFs Envolvidos:** RF026
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Financeiro] -->|Cria fatura Excel| B[Planilha manual]
    B -->|Envia por e-mail| C[Cliente]
    C -->|Paga boleto| D[Banco]
    D -->|Extrato PDF| E[Financeiro baixa manual]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire] -->|Gera faturas mensais| B[FaturaService]
    B -->|Aplica reajuste IPCA| C{Validação}
    C -->|OK| D[Cria registro fatura]
    D -->|Gera boleto| E[API Banco]
    E -->|Envia e-mail| F[Cliente]
    F -->|Paga| G[OFX Import]
    G -->|Conciliação auto| H[Baixa automática]
    H -->|Registra| I[Auditoria]

    J[Validação NF] -->|Consulta XML| K[SEFAZ]
    K -->|Autorizada?| D

    L[Alerta vencimento] -->|3 dias antes| M[Notificação RF066]

    style B fill:#27AE60
    style H fill:#27AE60
    style I fill:#27AE60
```

#### Descrição do Processo

Ciclo completo de gestão de faturas desde criação automática mensal, validação de Notas Fiscais via SEFAZ, geração de boletos bancários, envio automático ao cliente, conciliação com extratos OFX, até baixa automática e auditoria. Inclui alertas proativos de vencimento e histórico completo de pagamentos.

#### Atores

- **Sistema de Faturamento:** Gera faturas automaticamente
- **Financeiro:** Monitora e intervém em exceções
- **Cliente:** Recebe e paga faturas
- **Banco:** Processa pagamentos
- **SEFAZ:** Valida Notas Fiscais

#### Fluxo Principal

1. Job Hangfire executa no dia 1 de cada mês (00:00)
2. Sistema busca contratos ativos com faturamento mensal
3. Para cada contrato:
   - Calcula valor base + reajustes (IPCA, IGP-M)
   - Aplica impostos (PIS, COFINS, ISSQN)
   - Cria registro de fatura (status: Pendente)
4. Valida se existe NF-e autorizada
5. Se NF-e não existe: dispara geração via RF032
6. Gera boleto via API do banco
7. Envia e-mail ao cliente com:
   - PDF da fatura
   - XML da NF-e
   - Link para boleto
8. Sistema agenda alertas:
   - 3 dias antes do vencimento
   - No dia do vencimento
   - 1 dia após vencimento
9. Importação OFX bancária identifica pagamento
10. Sistema faz conciliação automática (valor + nosso número)
11. Se match: baixa fatura automaticamente
12. Registra histórico completo na auditoria

**Fluxo Alternativo: Fatura Vencida**

1. Job diário verifica faturas não pagas após vencimento
2. Calcula multa (2%) + juros diários (0,033%)
3. Atualiza valor da fatura
4. Notifica cliente via e-mail/SMS
5. Após 30 dias: marca para cobrança jurídica

#### Automações

- ✅ Geração automática mensal via Hangfire
- ✅ Cálculo automático de reajustes (IPCA, IGP-M)
- ✅ Validação automática de NF-e via SEFAZ
- ✅ Geração automática de boletos
- ✅ Envio automático por e-mail
- ✅ Alertas proativos de vencimento
- ✅ Conciliação automática com OFX
- ✅ Baixa automática de faturas
- ✅ Cálculo automático de multa e juros

#### Integrações

- **RF032 (NF-e):** Geração de Nota Fiscal Eletrônica
- **WebService SEFAZ:** Validação de autorização de NF-e
- **API Banco (Itaú/Bradesco):** Geração de boletos
- **OFX Parser:** Importação de extratos bancários
- **RF089 (Conciliação):** Matching automático fatura vs pagamento
- **RF066 (Notificações):** Alertas multi-canal
- **RF004 (Auditoria):** Registro imutável de operações

#### Regras de Negócio Principais

- **RN-026-01:** Faturas geradas automaticamente no dia 1 de cada mês
- **RN-026-02:** Vencimento padrão: dia 10 do mês seguinte (configurável)
- **RN-026-03:** Reajustes aplicados conforme índice contratual (IPCA, IGP-M, IPC)
- **RN-026-04:** Multa de 2% após vencimento
- **RN-026-05:** Juros de 1% ao mês (0,033% ao dia)
- **RN-026-06:** Conciliação automática por nosso número + valor
- **RN-026-07:** Fatura sem NF-e autorizada não pode ser enviada
- **RN-026-08:** Alertas enviados 3 dias antes do vencimento

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Faturas criadas manualmente em Excel
- ❌ Envio manual por e-mail (esquecimentos frequentes)
- ❌ Conciliação manual com extrato PDF (demorado)
- ❌ Baixa manual (atrasos e erros)
- ❌ Sem alertas automáticos de vencimento
- ❌ Sem cálculo automático de multa e juros
- ❌ Sem histórico de pagamentos estruturado
- ❌ Validação NF-e manual

**Melhorias no moderno:**

- ✅ Geração automática mensal (Hangfire)
- ✅ Envio automático por e-mail
- ✅ Conciliação automática via OFX
- ✅ Baixa automática de faturas
- ✅ Alertas proativos multi-canal
- ✅ Cálculo automático de encargos
- ✅ Histórico completo auditável
- ✅ Integração nativa com SEFAZ

---

### 3.2 PRO-FCT-002: Parâmetros de Faturamento

**Código:** PRO-FCT-002
**RFs Envolvidos:** RF030
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Admin] -->|Edita config hardcoded| B[Código VB.NET]
    B -->|Recompila| C[Deploy]
    C -->|Reinicia IIS| D[Config ativa]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Admin] -->|Configura parâmetros| B[UI Parâmetros]
    B -->|Periodicidade| C[Mensal/Trimestral/Anual]
    B -->|Dia corte| D[Dia 25 padrão]
    B -->|Dia vencimento| E[Dia 10 padrão]
    B -->|Índice reajuste| F[IPCA/IGP-M/IPC]
    B -->|Multa/Juros| G[2% + 1% a.m.]

    C --> H[Salva no banco]
    D --> H
    E --> H
    F --> H
    G --> H

    H -->|Invalida cache| I[Redis]
    I -->|Aplica imediato| J[Job Faturamento]

    style B fill:#27AE60
    style H fill:#27AE60
    style I fill:#27AE60
```

#### Descrição do Processo

Configuração centralizada de regras de faturamento: periodicidade (mensal, trimestral, anual), dia de corte para medição, dia de vencimento, índices de reajuste automático (IPCA, IGP-M, IPC), percentuais de multa e juros. Suporta configuração global e por cliente (multi-tenancy).

#### Atores

- **Administrador de Sistema:** Configura parâmetros globais
- **Gestor Financeiro:** Configura parâmetros por cliente
- **Sistema de Faturamento:** Consome parâmetros

#### Fluxo Principal

1. Admin acessa módulo "Parâmetros de Faturamento"
2. Seleciona nível de configuração:
   - Global: aplica para todos os clientes
   - Cliente específico: sobrescreve global
3. Define periodicidade:
   - Mensal: fatura todo mês
   - Trimestral: fatura a cada 3 meses
   - Anual: fatura uma vez por ano
4. Define dia de corte (padrão: 25):
   - Medição de consumo até este dia
   - Valor apurado entra na próxima fatura
5. Define dia de vencimento (padrão: 10):
   - Dia do mês para vencimento da fatura
6. Seleciona índice de reajuste:
   - IPCA: Índice de Preços ao Consumidor Amplo
   - IGP-M: Índice Geral de Preços do Mercado
   - IPC: Índice de Preços ao Consumidor
7. Define percentuais de encargos:
   - Multa: 2% (padrão)
   - Juros: 1% ao mês (padrão)
8. Sistema valida configurações
9. Salva no banco de dados
10. Invalida cache Redis
11. Jobs de faturamento passam a usar novos parâmetros

#### Automações

- ✅ Aplicação imediata via invalidação de cache
- ✅ Consulta automática de índices (IBGE API)
- ✅ Cálculo automático de reajustes
- ✅ Validação de conflitos de configuração
- ✅ Histórico de alterações (auditoria)

#### Integrações

- **IBGE API:** Consulta de índices IPCA, IGP-M, IPC
- **Redis Cache:** Hot-reload de parâmetros
- **RF026 (Faturas):** Consumo de parâmetros
- **RF090 (Medição):** Uso de dia de corte
- **RF004 (Auditoria):** Registro de alterações

#### Regras de Negócio Principais

- **RN-030-01:** Periodicidade: Mensal, Trimestral ou Anual
- **RN-030-02:** Dia de corte entre 1 e 28
- **RN-030-03:** Dia de vencimento entre 1 e 28
- **RN-030-04:** Índices de reajuste atualizados mensalmente via IBGE API
- **RN-030-05:** Multa padrão: 2% (configurável)
- **RN-030-06:** Juros padrão: 1% ao mês (configurável)
- **RN-030-07:** Configuração por cliente sobrescreve global
- **RN-030-08:** Alterações aplicadas imediatamente (sem deploy)

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Parâmetros hardcoded em código
- ❌ Deploy necessário para alterar
- ❌ Sem configuração por cliente
- ❌ Sem consulta automática de índices
- ❌ Sem histórico de alterações
- ❌ Reajustes calculados manualmente

**Melhorias no moderno:**

- ✅ Configuração via UI sem código
- ✅ Alteração imediata sem deploy
- ✅ Suporte multi-tenancy (global + cliente)
- ✅ Consulta automática de índices via API
- ✅ Histórico completo de alterações
- ✅ Reajustes automáticos

---

### 3.3 PRO-FCT-003: Plano de Contas

**Código:** PRO-FCT-003
**RFs Envolvidos:** RF031
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Contador] -->|Classifica manual| B[Excel]
    B -->|Copia para sistema| C[Aplicação]
    C -->|Sem hierarquia| D[Lista plana]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Admin] -->|Configura plano| B[UI Hierárquica]
    B -->|Nível 1| C[1.0 Receitas]
    B -->|Nível 1| D[2.0 Despesas]

    C -->|Nível 2| E[1.1 Receita Serviços]
    C -->|Nível 2| F[1.2 Receita Produtos]

    D -->|Nível 2| G[2.1 Custo Pessoal]
    D -->|Nível 2| H[2.2 Infraestrutura]

    G -->|Nível 3| I[2.1.1 Salários]
    G -->|Nível 3| J[2.1.2 Benefícios]

    K[Lançamento] -->|Classifica auto| L[Machine Learning]
    L -->|Sugere conta| M[Contador aprova]
    M -->|Persiste| N[(SQL Server)]

    N -->|Integra| O[TOTVS/SAP]
    N -->|Gera| P[DRE automático]

    style B fill:#27AE60
    style L fill:#27AE60
    style P fill:#27AE60
```

#### Descrição do Processo

Estrutura hierárquica de contas contábeis com até 5 níveis de profundidade, classificação automática de lançamentos via Machine Learning, integração bidirecional com ERPs (TOTVS, SAP, Oracle), associação com centros de custo, e geração automática de DRE (Demonstração do Resultado do Exercício).

#### Atores

- **Contador:** Configura plano de contas
- **Sistema de Classificação:** Sugere contas via ML
- **Financeiro:** Lança receitas e despesas
- **ERP Externo:** Recebe/envia lançamentos

#### Fluxo Principal

1. Contador acessa módulo "Plano de Contas"
2. Cria estrutura hierárquica:
   - **Nível 1:** 1.0 Receitas, 2.0 Despesas, 3.0 Ativos
   - **Nível 2:** 1.1 Receita Serviços, 1.2 Receita Produtos
   - **Nível 3:** 1.1.1 Consultoria, 1.1.2 Manutenção
   - **Nível 4:** Detalha por projeto/cliente
   - **Nível 5:** Refinamento máximo
3. Associa cada conta a:
   - Centro de custo
   - Natureza contábil (débito/crédito)
   - Grupo DRE
4. Sistema persiste estrutura no banco
5. **Fluxo de Lançamento:**
   - Usuário lança receita/despesa
   - Sistema analisa histórico via ML
   - Sugere conta contábil (85% de acurácia)
   - Contador aprova ou corrige
   - Sistema aprende com correção
6. Lançamento classificado é persistido
7. Sistema sincroniza com ERP externo (TOTVS/SAP)
8. Job noturno recalcula DRE

#### Automações

- ✅ Classificação automática via Machine Learning
- ✅ Sincronização bidirecional com ERP
- ✅ Geração automática de DRE
- ✅ Validação de natureza contábil (débito/crédito)
- ✅ Alertas de contas não utilizadas
- ✅ Sugestão de consolidação de contas

#### Integrações

- **TOTVS Protheus:** API REST para sincronização
- **SAP Business One:** RFC/BAPI para integração
- **Oracle ERP:** WebService SOAP
- **Azure ML:** Classificação automática de lançamentos
- **RF026 (Faturas):** Associação de fatura a conta contábil
- **RF055 (Rateio):** Distribuição por centro de custo

#### Regras de Negócio Principais

- **RN-031-01:** Hierarquia com até 5 níveis
- **RN-031-02:** Código da conta único (ex: 1.1.2.3.1)
- **RN-031-03:** Conta com lançamentos não pode ser excluída (soft delete)
- **RN-031-04:** Classificação automática aprende com correções
- **RN-031-05:** Sincronização com ERP a cada 1 hora
- **RN-031-06:** DRE recalculado diariamente às 23h
- **RN-031-07:** Centro de custo obrigatório
- **RN-031-08:** Natureza contábil validada (débito/crédito)

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Lista plana de contas (sem hierarquia)
- ❌ Classificação 100% manual
- ❌ Sem integração com ERP
- ❌ DRE gerado manualmente em Excel
- ❌ Sem centro de custo
- ❌ Sem validação de natureza contábil

**Melhorias no moderno:**

- ✅ Hierarquia de até 5 níveis
- ✅ Classificação automática via ML
- ✅ Integração bidirecional com ERP
- ✅ DRE automático diário
- ✅ Centro de custo obrigatório
- ✅ Validação automática de lançamentos

---

### 3.4 PRO-FCT-004: Notas Fiscais/Faturas (NF-e)

**Código:** PRO-FCT-004
**RFs Envolvidos:** RF032
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Financeiro] -->|Acessa site Prefeitura| B[Portal NF-e]
    B -->|Preenche formulário| C[Gera NF-e]
    C -->|Download PDF| D[Salva em pasta]
    D -->|Anexa em e-mail| E[Envia cliente]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Sistema] -->|Gera fatura RF026| B[Trigger NF-e]
    B -->|Monta XML| C[NFe Builder]
    C -->|Valida schema XSD| D{Válido?}
    D -->|Não| E[Log erro]
    D -->|Sim| F[Assina digital]
    F -->|Envia| G[WebService SEFAZ]
    G -->|Consulta status| H{Autorizada?}
    H -->|Não| I[Registra motivo]
    H -->|Sim| J[Consulta XML autorizado]
    J -->|Download| K[Salva Azure Blob]
    K -->|Gera DANFE PDF| L[iText7]
    L -->|Envia e-mail| M[Cliente]
    M -->|Consulta QR Code| N[Portal SEFAZ]

    O[Job diário] -->|Consulta canceladas| G
    O -->|Atualiza status| P[(SQL Server)]

    style C fill:#27AE60
    style F fill:#27AE60
    style J fill:#27AE60
    style K fill:#27AE60
```

#### Descrição do Processo

Geração automática de NF-e (Nota Fiscal Eletrônica de Serviços) via WebService oficial da SEFAZ, com validação de schema XML, assinatura digital, consulta de status (autorizada/cancelada/denegada), armazenamento seguro de XMLs em Azure Blob, geração de DANFE (PDF), e envio automático ao cliente.

#### Atores

- **Sistema de Faturamento:** Dispara geração de NF-e
- **SEFAZ:** Autoriza/Cancela NF-e
- **Azure Blob Storage:** Armazena XMLs
- **Cliente:** Recebe e valida NF-e

#### Fluxo Principal

1. Sistema cria fatura (RF026)
2. Trigger dispara geração de NF-e
3. `NFe Builder` monta XML conforme layout SEFAZ:
   - Dados emitente (CNPJ, IE, endereço)
   - Dados tomador (cliente)
   - Discriminação dos serviços
   - Valores (base cálculo, alíquotas, impostos)
   - Retenções (PIS, COFINS, ISSQN)
4. Sistema valida XML contra schema XSD oficial
5. Se inválido: registra erro e PARA
6. Se válido: assina digitalmente com certificado A1
7. Envia XML assinado para WebService SEFAZ
8. SEFAZ processa e retorna protocolo
9. Sistema consulta status do protocolo:
   - **Autorizada:** NF-e emitida com sucesso
   - **Denegada:** Erro no CNPJ/IE (bloqueia)
   - **Rejeitada:** Erro no XML (corrige e reenvia)
10. Se autorizada:
    - Consulta XML autorizado (com nº e chave)
    - Salva XML em Azure Blob
    - Gera DANFE (PDF) via iText7
    - Salva PDF em Azure Blob
    - Envia e-mail ao cliente (XML + PDF)
    - Atualiza fatura com nº NF-e
11. Job diário consulta cancelamentos/inutilizações

**Fluxo de Cancelamento:**

1. Financeiro solicita cancelamento de NF-e
2. Sistema valida prazo (24h para serviços, conforme legislação)
3. Monta XML de cancelamento
4. Assina digitalmente
5. Envia para SEFAZ
6. SEFAZ cancela e retorna protocolo
7. Sistema atualiza status da NF-e

#### Automações

- ✅ Geração automática ao criar fatura
- ✅ Validação automática de schema XSD
- ✅ Assinatura digital automática
- ✅ Envio automático para SEFAZ
- ✅ Consulta automática de status
- ✅ Download automático de XML autorizado
- ✅ Geração automática de DANFE (PDF)
- ✅ Envio automático por e-mail
- ✅ Monitoramento diário de cancelamentos

#### Integrações

- **WebService SEFAZ:** Autorização, consulta, cancelamento
- **Certificado Digital A1:** Assinatura de XMLs
- **Azure Blob Storage:** Armazenamento de XMLs e PDFs
- **iText7:** Geração de DANFE em PDF
- **RF026 (Faturas):** Vinculação NF-e → Fatura
- **RF067 (Central E-mails):** Envio de NF-e ao cliente

#### Regras de Negócio Principais

- **RN-032-01:** NF-e gerada automaticamente ao criar fatura
- **RN-032-02:** XML deve ser validado contra schema XSD oficial
- **RN-032-03:** Assinatura digital obrigatória (certificado A1)
- **RN-032-04:** XMLs armazenados por 7 anos (compliance)
- **RN-032-05:** Cancelamento permitido em até 24h (serviços)
- **RN-032-06:** DANFE gerado automaticamente
- **RN-032-07:** Job diário sincroniza status com SEFAZ
- **RN-032-08:** Cliente recebe XML + PDF por e-mail

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Geração manual no portal da Prefeitura
- ❌ Preenchimento formulário web (demorado)
- ❌ Download manual de PDF
- ❌ Envio manual por e-mail
- ❌ XMLs salvos em pasta local (perda de dados)
- ❌ Sem monitoramento de cancelamentos
- ❌ Sem integração com sistema de faturamento

**Melhorias no moderno:**

- ✅ Geração automática via WebService
- ✅ Validação automática de schema
- ✅ Assinatura digital integrada
- ✅ Envio automático por e-mail
- ✅ XMLs em Azure Blob (7 anos)
- ✅ Monitoramento automático de status
- ✅ Integração nativa com faturamento

---

### 3.5 PRO-FCT-005: Conciliação de Faturas

**Código:** PRO-FCT-005
**RFs Envolvidos:** RF089
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Financeiro] -->|Download extrato PDF| B[Banco]
    B -->|Abre Excel| C[Planilha]
    C -->|Procura nosso número| D[Fatura]
    D -->|Baixa manual| E[Sistema]

    style A fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire] -->|Conecta SFTP| B[Banco]
    B -->|Download OFX| C[OFX Parser]
    C -->|Extrai pagamentos| D[Lista transações]
    D -->|Para cada transação| E{Matching}
    E -->|Por nosso número| F{Fatura encontrada?}
    F -->|Sim| G{Valor confere?}
    G -->|Sim| H[Baixa automática]
    G -->|Não| I[Divergência]
    F -->|Não| J[Não identificado]

    H -->|Atualiza status| K[(SQL Server)]
    K -->|Notifica| L[Financeiro]

    I -->|Registra| M[Relatório divergências]
    J -->|Registra| M
    M -->|Alerta| N[Análise manual]

    O[ML Sugere] -->|Para não identificados| P[Matching fuzzy]

    style C fill:#27AE60
    style E fill:#27AE60
    style H fill:#27AE60
    style O fill:#27AE60
```

#### Descrição do Processo

Conciliação automática de faturas com pagamentos bancários via importação de arquivos OFX, matching automático por nosso número do boleto e valor, detecção de divergências (valor diferente, data divergente), relatório de pendências, e sugestão de matching via Machine Learning para pagamentos não identificados.

#### Atores

- **Sistema de Conciliação:** Processa OFX automaticamente
- **Banco:** Fornece extratos OFX via SFTP
- **Financeiro:** Analisa divergências
- **Machine Learning:** Sugere matchings fuzzy

#### Fluxo Principal

1. Job Hangfire executa diariamente às 8h
2. Conecta via SFTP no servidor do banco
3. Lista arquivos OFX novos (não processados)
4. Faz download dos arquivos
5. `OFX Parser` extrai transações:
   - Data
   - Valor
   - Nosso número (identificador do boleto)
   - Tipo (crédito/débito)
6. Para cada transação de crédito:
   - **Busca fatura por nosso número**
   - Se encontrada:
     - Compara valor transação vs valor fatura
     - Se iguais: baixa automática (status: Paga)
     - Se diferentes: registra divergência
   - Se não encontrada:
     - Tenta matching fuzzy via ML:
       - Valor aproximado (±5%)
       - Data próxima (±3 dias)
       - Cliente identificado no histórico
     - Se ML sugere match (>80% confiança): apresenta para aprovação
     - Se ML não sugere: marca como "Não Identificado"
7. Atualiza status das faturas baixadas
8. Gera relatório de conciliação:
   - Total baixado: R$ 150.000
   - Total divergências: R$ 5.000
   - Total não identificado: R$ 2.000
9. Envia relatório por e-mail ao financeiro
10. Notifica divergências para análise manual

**Fluxo de Análise Manual:**

1. Financeiro acessa "Pendências de Conciliação"
2. Visualiza lista de divergências:
   - Valor diferente (pagamento parcial ou com desconto)
   - Nosso número não encontrado
3. Para cada pendência:
   - Visualiza sugestões do ML
   - Busca fatura manualmente
   - Confirma matching
   - Sistema baixa fatura

#### Automações

- ✅ Download automático de OFX via SFTP
- ✅ Parsing automático de transações
- ✅ Matching automático por nosso número
- ✅ Baixa automática de faturas
- ✅ Detecção automática de divergências
- ✅ Matching fuzzy via Machine Learning
- ✅ Geração automática de relatório
- ✅ Notificação de divergências

#### Integrações

- **Banco (SFTP):** Download de arquivos OFX
- **OFX Parser:** Extração de transações
- **RF026 (Faturas):** Baixa de faturas
- **Azure ML:** Matching fuzzy de pagamentos
- **RF066 (Notificações):** Alertas de divergências
- **RF004 (Auditoria):** Registro de conciliações

#### Regras de Negócio Principais

- **RN-089-01:** Conciliação automática por nosso número + valor
- **RN-089-02:** Divergência de valor >1% registra pendência
- **RN-089-03:** Pagamentos não identificados aguardam análise manual
- **RN-089-04:** ML sugere matchings com confiança >80%
- **RN-089-05:** Job diário executa às 8h
- **RN-089-06:** Relatório enviado ao financeiro às 9h
- **RN-089-07:** Arquivos OFX mantidos por 7 anos
- **RN-089-08:** Baixa manual requer justificativa

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Download manual de extrato PDF
- ❌ Busca manual de fatura em Excel
- ❌ Baixa manual no sistema (demorada)
- ❌ Sem detecção de divergências
- ❌ Sem relatório de pendências
- ❌ Erros frequentes (baixa errada)

**Melhorias no moderno:**

- ✅ Download automático de OFX
- ✅ Matching automático por nosso número
- ✅ Baixa automática de faturas
- ✅ Detecção automática de divergências
- ✅ Relatório diário de pendências
- ✅ ML sugere matchings não óbvios
- ✅ Auditoria completa de conciliações

---

### 3.6 PRO-FCT-006: Medição/Faturamento de Contratos

**Código:** PRO-FCT-006
**RFs Envolvidos:** RF090
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Financeiro] -->|Conta ativos manualmente| B[Excel]
    B -->|Multiplica por valor unitário| C[Cálculo manual]
    C -->|Cria fatura| D[Sistema]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire] -->|Dia 25 do mês| B[Início medição]
    B -->|Busca contratos| C[(Contratos ativos)]
    C -->|Para cada contrato| D{Tipo medição?}

    D -->|Ativos| E[Conta ativos ativos]
    D -->|Licenças| F[Conta licenças ativas]
    D -->|Horas| G[Soma horas lançadas]
    D -->|Fixo| H[Valor fixo contrato]

    E -->|Calcula pro-rata| I[Dias ativos/30]
    F -->|Calcula pro-rata| I
    G -->|Valor hora × qtd| J[Total horas]

    I -->|Soma componentes| K[Valor total]
    J -->|Soma componentes| K
    H -->|Valor fixo| K

    K -->|Rateia centros custo| L[Rateio RF055]
    L -->|Gera fatura| M[RF026]
    M -->|Registra medição| N[(MedicoesDB)]
    N -->|Notifica gestor| O[Aprovação]
    O -->|Aprovado| P[Libera faturamento]

    style E fill:#27AE60
    style I fill:#27AE60
    style L fill:#27AE60
    style M fill:#27AE60
```

#### Descrição do Processo

Medição periódica de consumo (ativos, licenças, horas) para faturamento de contratos, com cálculo pro-rata para ativações/desativações durante o mês, rateio proporcional entre centros de custo, geração automática de faturas baseada na medição, e workflow de aprovação antes do faturamento.

#### Atores

- **Sistema de Medição:** Executa medição automática
- **Gestor de Contrato:** Aprova medições
- **Financeiro:** Monitora faturamento
- **Sistema de Rateio (RF055):** Distribui custos

#### Fluxo Principal

1. Job Hangfire executa no dia 25 de cada mês
2. Busca contratos ativos com tipo "Medição"
3. Para cada contrato identifica tipo de medição:

**Tipo 1: Medição por Ativos**
- Consulta ativos ativos vinculados ao contrato
- Para cada ativo calcula dias ativos no mês
- Exemplo: Ativo ativado dia 15 → 15 dias ativos
- Calcula pro-rata: (15/30) × valor unitário
- Soma valores pro-rata de todos os ativos

**Tipo 2: Medição por Licenças**
- Consulta licenças ativas
- Calcula pro-rata por data de ativação
- Exemplo: Licença ativada dia 10 → (20/30) × valor
- Soma valores pro-rata

**Tipo 3: Medição por Horas**
- Consulta horas lançadas no período
- Multiplica por valor/hora contratado
- Exemplo: 120 horas × R$ 150/hora = R$ 18.000
- Soma valores

**Tipo 4: Valor Fixo**
- Não há medição (valor fixo mensal)
- Usa valor do contrato

4. Sistema calcula valor total da medição
5. Rateia entre centros de custo (RF055):
   - Proporcional por departamento
   - Por área (m²)
   - Por headcount
6. Cria registro de medição (status: Pendente Aprovação)
7. Notifica gestor do contrato via RF066
8. Gestor acessa painel "Minhas Medições"
9. Visualiza detalhamento:
   - Total medido: R$ 45.000
   - Breakdown por item
   - Comparativo com mês anterior
10. **Gestor aprova:**
    - Sistema marca medição como Aprovada
    - Dispara geração de fatura (RF026)
    - Fatura vinculada à medição
11. **Gestor rejeita:**
    - Sistema marca como Rejeitada
    - Notifica financeiro para análise

#### Automações

- ✅ Medição automática no dia 25
- ✅ Cálculo automático pro-rata
- ✅ Rateio automático por centro de custo
- ✅ Geração automática de fatura pós-aprovação
- ✅ Notificação automática ao gestor
- ✅ Comparativo automático mês anterior
- ✅ Detecção de variações >20% (alerta)

#### Integrações

- **RF026 (Faturas):** Geração de fatura baseada em medição
- **RF055 (Rateio):** Distribuição por centro de custo
- **RF025 (Ativos):** Consulta ativos ativos
- **RF066 (Notificações):** Alertas de aprovação
- **RF088 (Workflows):** Fluxo de aprovação

#### Regras de Negócio Principais

- **RN-090-01:** Medição executada automaticamente dia 25
- **RN-090-02:** Cálculo pro-rata por dia (ativação/desativação)
- **RN-090-03:** Aprovação obrigatória antes de faturar
- **RN-090-04:** Variação >20% gera alerta ao gestor
- **RN-090-05:** Rateio proporcional por centro de custo
- **RN-090-06:** Fatura vinculada à medição (rastreabilidade)
- **RN-090-07:** Histórico de medições mantido por 7 anos
- **RN-090-08:** Medição rejeitada não gera fatura

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Contagem manual de ativos
- ❌ Cálculo manual em Excel
- ❌ Sem pro-rata (valor cheio ou zero)
- ❌ Sem rateio por centro de custo
- ❌ Sem workflow de aprovação
- ❌ Erros frequentes de cálculo

**Melhorias no moderno:**

- ✅ Medição automática dia 25
- ✅ Cálculo automático pro-rata
- ✅ Rateio automático multi-dimensional
- ✅ Workflow de aprovação integrado
- ✅ Detecção de variações anormais
- ✅ Rastreabilidade fatura → medição

---

### 3.7 PRO-FCT-007: Auditoria de Faturas

**Código:** PRO-FCT-007
**RFs Envolvidos:** RF097
**Área:** Contratos e Faturamento
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Auditor] -->|Revisa faturas manualmente| B[Excel]
    B -->|Encontra erro| C[Reporta]
    C -->|Correção manual| D[Sistema]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire] -->|Executa pós-faturamento| B[Auditoria Automática]
    B -->|Validação 1| C{Fatura vs Contrato}
    C -->|Divergência| D[Alerta valor incorreto]

    B -->|Validação 2| E{Cobranças duplicadas}
    E -->|Duplicada| F[Alerta duplicação]

    B -->|Validação 3| G{Histórico reajustes}
    G -->|Erro| H[Alerta reajuste inválido]

    B -->|Validação 4| I{Impostos}
    I -->|Erro| J[Alerta compliance fiscal]

    D --> K[Relatório Não-Conformidades]
    F --> K
    H --> K
    J --> K

    K -->|Notifica| L[Auditor]
    L -->|Analisa| M{Confirma erro?}
    M -->|Sim| N[Gera fatura retificadora]
    M -->|Não| O[Fecha não-conformidade]

    P[ML Detecta] -->|Padrões anômalos| Q[Sugestão auditoria]

    style B fill:#27AE60
    style C fill:#27AE60
    style E fill:#27AE60
    style G fill:#27AE60
    style I fill:#27AE60
```

#### Descrição do Processo

Auditoria preventiva automática de faturas com validação cruzada fatura vs contrato, detecção de cobranças duplicadas, auditoria de valores (histórico de reajustes), compliance fiscal (validação de impostos PIS/COFINS/ISSQN), e relatório de não-conformidades com Machine Learning detectando padrões anômalos.

#### Atores

- **Sistema de Auditoria:** Executa validações automáticas
- **Auditor:** Analisa não-conformidades
- **Financeiro:** Corrige erros detectados
- **Machine Learning:** Detecta anomalias

#### Fluxo Principal

1. Job Hangfire executa logo após geração de faturas
2. Para cada fatura gerada, executa 4 validações:

**Validação 1: Fatura vs Contrato**
- Compara valor fatura vs valor contrato
- Verifica se reajustes foram aplicados corretamente
- Valida periodicidade (mensal, trimestral, anual)
- Se divergência: registra não-conformidade

**Validação 2: Cobranças Duplicadas**
- Busca faturas do mesmo cliente no mesmo período
- Verifica se há duplicação de itens
- Exemplo: Mesmo ativo cobrado 2x
- Se duplicado: registra não-conformidade

**Validação 3: Histórico de Reajustes**
- Consulta histórico de reajustes do contrato
- Valida se índice aplicado está correto (IPCA, IGP-M)
- Verifica se percentual aplicado confere com índice oficial
- Se erro: registra não-conformidade

**Validação 4: Compliance Fiscal**
- Valida cálculo de impostos:
  - PIS: 0,65% ou 1,65% (regime)
  - COFINS: 3% ou 7,6% (regime)
  - ISSQN: conforme município (2% a 5%)
- Verifica se retenções estão corretas
- Se erro: registra não-conformidade

3. Sistema agrega não-conformidades
4. Gera relatório:
   - Total faturas auditadas: 150
   - Não-conformidades: 8 (5,3%)
   - Breakdown por tipo
5. ML analisa padrões:
   - Identifica erros recorrentes
   - Sugere revisão de regras
6. Notifica auditor via RF066
7. Auditor acessa painel "Não-Conformidades"
8. Para cada não-conformidade:
   - Visualiza detalhes
   - Compara fatura vs contrato
   - **Se confirma erro:**
     - Cancela fatura original
     - Gera fatura retificadora
     - Notifica cliente
   - **Se é falso positivo:**
     - Fecha não-conformidade
     - ML aprende com correção

#### Automações

- ✅ Auditoria automática pós-faturamento
- ✅ Validação cruzada fatura vs contrato
- ✅ Detecção automática de duplicações
- ✅ Validação automática de reajustes
- ✅ Validação automática de impostos
- ✅ ML detecta padrões anômalos
- ✅ Geração automática de relatório
- ✅ Notificação de não-conformidades

#### Integrações

- **RF026 (Faturas):** Validação de faturas geradas
- **RF030 (Parâmetros):** Consulta índices de reajuste
- **IBGE API:** Valida índices IPCA/IGP-M
- **Azure ML:** Detecção de anomalias
- **RF066 (Notificações):** Alertas ao auditor
- **RF004 (Auditoria):** Registro de não-conformidades

#### Regras de Negócio Principais

- **RN-097-01:** Auditoria executada automaticamente pós-faturamento
- **RN-097-02:** 4 validações obrigatórias (contrato, duplicação, reajuste, impostos)
- **RN-097-03:** Não-conformidades notificadas em até 1 hora
- **RN-097-04:** ML aprende com falsos positivos
- **RN-097-05:** Fatura com erro gera retificadora
- **RN-097-06:** Relatório mensal consolidado
- **RN-097-07:** Histórico de auditorias mantido por 7 anos
- **RN-097-08:** Taxa de não-conformidade >5% gera alerta crítico

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Auditoria manual e reativa
- ❌ Erros descobertos pelo cliente (reclamação)
- ❌ Sem validação de reajustes
- ❌ Sem detecção de duplicações
- ❌ Compliance fiscal manual
- ❌ Sem histórico de auditoria

**Melhorias no moderno:**

- ✅ Auditoria automática e preventiva
- ✅ Erros detectados antes do cliente
- ✅ Validação automática de reajustes
- ✅ Detecção automática de duplicações
- ✅ Compliance fiscal automático
- ✅ Histórico completo de auditorias
- ✅ ML detecta padrões anômalos

---

## PARTE 2: ATIVOS E CUSTOS

### 3.8 PRO-FAC-001: Gestão de Ativos

**Código:** PRO-FAC-001
**RFs Envolvidos:** RF025
**Área:** Ativos e Custos
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[TI] -->|Registra ativo Excel| B[Planilha]
    B -->|Depreciação manual| C[Cálculo anual]
    C -->|Sem rastreamento| D[Localização desconhecida]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Compra ativo] -->|Cadastra| B[Sistema Ativos]
    B -->|Gera QR Code| C[Etiqueta patrimônio]
    C -->|Cola no ativo| D[Ativo identificado]

    B -->|Configura depreciação| E{Método?}
    E -->|Linear| F[Job mensal deprecia]
    E -->|Soma dígitos| F
    E -->|Saldo decrescente| F

    F -->|Atualiza valor contábil| G[(SQL Server)]

    H[Transferência] -->|Novo local| I[Atualiza localização]
    I -->|Novo usuário| J[Atualiza responsável]
    J -->|Registra histórico| K[Auditoria]

    L[Alerta garantia] -->|30 dias antes| M[Notifica TI RF066]

    N[Descarte] -->|Soft delete| O[Marca inativo]
    O -->|Mantém histórico| P[Compliance]

    Q[Inventário físico] -->|Scan QR Code| R[App mobile]
    R -->|Reconcilia| S[Inventário vs Sistema]

    style B fill:#27AE60
    style F fill:#27AE60
    style I fill:#27AE60
    style L fill:#27AE60
```

#### Descrição do Processo

Ciclo de vida completo de ativos (aquisição → utilização → descarte) com depreciação automática (linear, soma de dígitos, saldo decrescente), inventário físico vs lógico via QR Code, transferência entre locais/usuários com histórico, e alertas de fim de garantia.

#### Atores

- **TI:** Gerencia ativos
- **Financeiro:** Monitora depreciação
- **Usuário:** Utiliza ativos
- **Sistema de Inventário:** Reconcilia físico vs lógico

#### Fluxo Principal

**Fase 1: Aquisição**
1. TI cadastra novo ativo:
   - Tipo (desktop, notebook, servidor, licença)
   - Fabricante, modelo, número série
   - Valor de aquisição
   - Data de compra
   - Fornecedor
   - Garantia (meses)
2. Sistema gera QR Code único
3. TI imprime etiqueta de patrimônio
4. Cola etiqueta no ativo físico
5. Sistema configura depreciação:
   - Método: Linear, Soma de Dígitos, Saldo Decrescente
   - Vida útil: 5 anos (padrão computadores)
   - Valor residual: 10% (opcional)
6. Job Hangfire inicia depreciação mensal

**Fase 2: Utilização**
1. TI aloca ativo para usuário/departamento
2. Sistema registra:
   - Local físico (sala, andar, prédio)
   - Usuário responsável
   - Data de alocação
3. Job mensal calcula depreciação:
   - **Linear:** Valor / Vida útil / 12 meses
   - **Soma de Dígitos:** (N - período) / Soma × Valor
   - **Saldo Decrescente:** Saldo × Taxa × (1/12)
4. Atualiza valor contábil do ativo
5. Sistema monitora fim de garantia:
   - 30 dias antes: alerta TI (RF066)
   - No vencimento: marca garantia expirada

**Fase 3: Transferência**
1. TI solicita transferência de ativo
2. Sistema registra:
   - Novo local
   - Novo usuário responsável
   - Data da transferência
   - Justificativa
3. Atualiza localização
4. Notifica novo responsável
5. Registra no histórico (audit trail)

**Fase 4: Descarte**
1. TI marca ativo para descarte
2. Sistema valida:
   - Totalmente depreciado? (valor contábil zero)
   - Motivo: Obsoleto, Quebrado, Roubado
3. Faz soft delete:
   - Marca campo `Ativo = false`
   - Mantém registro no banco
   - Preserva histórico completo
4. Registra na auditoria

**Inventário Físico:**
1. TI acessa app mobile
2. Escaneia QR Code dos ativos
3. App registra:
   - Ativo escaneado
   - Localização GPS
   - Timestamp
4. Sistema reconcilia:
   - Compara inventário físico vs lógico
   - Identifica divergências:
     - Ativos não encontrados
     - Ativos em local errado
     - Ativos não cadastrados
5. Gera relatório de divergências

#### Automações

- ✅ Depreciação automática mensal (3 métodos)
- ✅ Geração automática de QR Code
- ✅ Alertas automáticos de fim de garantia
- ✅ Cálculo automático de valor contábil
- ✅ Inventário via app mobile (QR Code)
- ✅ Reconciliação automática físico vs lógico
- ✅ Soft delete preserva histórico

#### Integrações

- **RF037 (TCO):** Cálculo de custo total por ativo
- **RF055 (Rateio):** Alocação de custos por departamento
- **RF066 (Notificações):** Alertas de garantia
- **RF004 (Auditoria):** Histórico de movimentações
- **App Mobile:** Inventário físico via QR Code

#### Regras de Negócio Principais

- **RN-025-01:** Depreciação automática mensal (3 métodos)
- **RN-025-02:** Vida útil padrão: 5 anos (computadores)
- **RN-025-03:** Valor residual padrão: 10%
- **RN-025-04:** QR Code único por ativo
- **RN-025-05:** Alerta de garantia 30 dias antes do vencimento
- **RN-025-06:** Soft delete obrigatório (mantém histórico)
- **RN-025-07:** Inventário físico semestral obrigatório
- **RN-025-08:** Transferência requer justificativa

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Registro em planilha Excel
- ❌ Depreciação calculada manualmente 1x/ano
- ❌ Sem rastreamento de localização
- ❌ Sem alertas de garantia
- ❌ Inventário físico manual (demorado)
- ❌ Hard delete (perdia histórico)

**Melhorias no moderno:**

- ✅ Sistema integrado com audit trail
- ✅ Depreciação automática mensal (3 métodos)
- ✅ Rastreamento completo de localização
- ✅ Alertas proativos de garantia
- ✅ Inventário físico via QR Code (rápido)
- ✅ Soft delete preserva histórico
- ✅ TCO calculado automaticamente

---

### 3.9 PRO-FAC-002: Custos Fixos

**Código:** PRO-FAC-002
**RFs Envolvidos:** RF036
**Área:** Ativos e Custos
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Financeiro] -->|Lança custo manualmente| B[Sistema]
    B -->|Sem provisão| C[Custo apenas quando pago]

    style A fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Financeiro] -->|Cadastra custo fixo| B[Sistema Custos]
    B -->|Define| C[Aluguel, Energia, Licenças]
    C -->|Periodicidade| D[Mensal, Trimestral, Anual]
    D -->|Valor recorrente| E[R$ 10.000/mês]

    F[Job Hangfire] -->|Dia 1 de cada mês| G[Provisão Automática]
    G -->|Cria lançamento| H[(SQL Server)]
    H -->|Rateia| I[RF055 Multi-dimensional]
    I -->|Por departamento| J[Depto A: R$ 4.000]
    I -->|Por departamento| K[Depto B: R$ 6.000]

    L[Comparativo] -->|Real vs Orçado| M{Desvio > 10%?}
    M -->|Sim| N[Alerta gestor RF066]
    M -->|Não| O[Dashboard atualizado]

    style B fill:#27AE60
    style G fill:#27AE60
    style I fill:#27AE60
    style M fill:#27AE60
```

#### Descrição do Processo

Cadastro de custos recorrentes (aluguel, energia, licenças SaaS, internet), provisão automática mensal via job Hangfire, rateio proporcional por centro de custo/departamento, comparativo real vs orçado com alertas de desvio, e dashboard gerencial.

#### Atores

- **Financeiro:** Cadastra custos fixos
- **Sistema de Provisão:** Executa provisões mensais
- **Gestor:** Monitora desvios orçamentários
- **Sistema de Rateio (RF055):** Distribui custos

#### Fluxo Principal

1. Financeiro acessa módulo "Custos Fixos"
2. Cadastra novo custo recorrente:
   - Tipo: Aluguel, Energia, Licença SaaS, Internet, etc.
   - Descrição: "Aluguel Escritório São Paulo"
   - Valor mensal: R$ 10.000
   - Periodicidade: Mensal, Trimestral, Anual
   - Início vigência: 01/2026
   - Fim vigência: (opcional, se contrato temporário)
   - Fornecedor: Imobiliária XYZ
   - Centro de custo: Administrativo
   - Conta contábil: 2.1.5 Aluguéis
3. Define regra de rateio:
   - Departamento A: 40% (R$ 4.000)
   - Departamento B: 60% (R$ 6.000)
4. Define orçamento mensal:
   - Orçado: R$ 10.000
   - Alerta se desvio > 10%
5. Sistema salva configuração
6. Job Hangfire executa no dia 1 de cada mês:
   - Busca custos fixos ativos
   - Para cada custo:
     - Cria lançamento contábil (provisão)
     - Rateia conforme regra configurada
     - Atualiza dashboard
7. Financeiro lança custo real ao pagar:
   - Custo real: R$ 10.500 (aluguel + IPTU)
8. Sistema compara real vs orçado:
   - Desvio: R$ 500 (5%)
   - Se desvio > 10%: alerta gestor via RF066
9. Dashboard atualizado em tempo real:
   - Custo previsto (orçado): R$ 10.000
   - Custo realizado: R$ 10.500
   - Desvio: +5%

**Fluxo de Reajuste:**
1. Sistema monitora vencimento de reajuste anual
2. Notifica financeiro 30 dias antes
3. Financeiro atualiza valor do custo fixo
4. Sistema aplica novo valor a partir da data

#### Automações

- ✅ Provisão automática mensal
- ✅ Rateio automático por centro de custo
- ✅ Comparativo automático real vs orçado
- ✅ Alertas automáticos de desvio >10%
- ✅ Dashboard em tempo real
- ✅ Notificação de reajustes vencidos

#### Integrações

- **RF055 (Rateio):** Distribuição multi-dimensional
- **RF031 (Plano de Contas):** Classificação contábil
- **RF066 (Notificações):** Alertas de desvios
- **RF004 (Auditoria):** Histórico de alterações
- **Hangfire:** Jobs de provisão mensal

#### Regras de Negócio Principais

- **RN-036-01:** Provisão automática no dia 1 de cada mês
- **RN-036-02:** Rateio obrigatório por centro de custo
- **RN-036-03:** Comparativo real vs orçado atualizado diariamente
- **RN-036-04:** Desvio >10% gera alerta automático
- **RN-036-05:** Periodicidade: Mensal, Trimestral ou Anual
- **RN-036-06:** Custo fixo inativo não gera provisão
- **RN-036-07:** Histórico de custos mantido por 7 anos
- **RN-036-08:** Reajuste notificado 30 dias antes

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Lançamento manual mensal (esquecimentos)
- ❌ Sem provisão automática
- ❌ Sem rateio (custo único)
- ❌ Sem comparativo orçado vs real
- ❌ Sem alertas de desvios
- ❌ Dashboard manual em Excel

**Melhorias no moderno:**

- ✅ Provisão automática mensal
- ✅ Rateio automático multi-dimensional
- ✅ Comparativo automático orçado vs real
- ✅ Alertas proativos de desvios
- ✅ Dashboard em tempo real
- ✅ Notificações de reajustes

---

### 3.10 PRO-FAC-003: Custos por Ativo (TCO)

**Código:** PRO-FAC-003
**RFs Envolvidos:** RF037
**Área:** Ativos e Custos
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Gestor] -->|Quer saber TCO| B[Não calculado]
    B -->|Decisão sem dados| C[Compra sem análise]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Sistema TCO] -->|Cálculo automático| B[Job diário]
    B -->|Para cada ativo| C[Coleta custos]

    C -->|Custo 1| D[Aquisição]
    C -->|Custo 2| E[Manutenção]
    C -->|Custo 3| F[Suporte]
    C -->|Custo 4| G[Energia]
    C -->|Custo 5| H[Licenças]

    D --> I[Soma TCO]
    E --> I
    F --> I
    G --> I
    H --> I

    I -->|Aloca indiretos| J[Overhead 15%]
    J -->|TCO Total| K[Valor por ativo]

    K -->|Compara| L{TCO vs Contrato Serviço}
    L -->|TCO < Contrato| M[Decisão: Manter ativo]
    L -->|TCO > Contrato| N[Decisão: Terceirizar]

    O[Relatório] -->|Ranking ativos| P[Mais caros]
    O -->|ROI| Q[Rentabilidade]

    style B fill:#27AE60
    style I fill:#27AE60
    style K fill:#27AE60
    style L fill:#27AE60
```

#### Descrição do Processo

Cálculo automático de TCO (Total Cost of Ownership) por ativo somando custos diretos (aquisição, manutenção, suporte, energia) e indiretos (overhead administrativo), alocação proporcional de custos compartilhados, comparativo TCO vs Contrato de Serviço (decisão Buy vs Lease), e relatório de rentabilidade por ativo.

#### Atores

- **Sistema TCO:** Calcula custos automaticamente
- **Gestor de TI:** Analisa TCO para decisões
- **Financeiro:** Valida custos
- **Job Diário:** Atualiza TCO

#### Fluxo Principal

1. Job Hangfire executa diariamente às 23h
2. Para cada ativo ativo, coleta custos:

**Custo 1: Aquisição**
- Valor de compra do ativo
- Divide pela vida útil (5 anos)
- Custo mensal: Valor / 60 meses

**Custo 2: Manutenção**
- Soma chamados de manutenção:
  - Peças trocadas
  - Horas técnico × valor/hora
- Custo médio mensal

**Custo 3: Suporte**
- Se ativo tem contrato de suporte:
  - Valor mensal do contrato
- Se não:
  - Horas suporte interno × valor/hora

**Custo 4: Energia**
- Consumo médio do equipamento (TDP)
- Exemplo: Desktop 300W
- Horas uso por dia × dias/mês × kWh × tarifa
- Custo energia mensal

**Custo 5: Licenças**
- Licenças vinculadas ao ativo:
  - Windows: R$ 20/mês
  - Office 365: R$ 30/mês
  - Antivírus: R$ 10/mês
- Soma licenças

3. Sistema soma custos diretos:
   - TCO Direto = Aquisição + Manutenção + Suporte + Energia + Licenças
4. Aloca custos indiretos (overhead):
   - Administrativo: 10%
   - Infraestrutura: 5%
   - TCO Indireto = TCO Direto × 15%
5. Calcula TCO Total:
   - TCO Total = TCO Direto + TCO Indireto
6. Atualiza registro do ativo com TCO
7. **Análise Buy vs Lease:**
   - Compara TCO Total vs Contrato de Serviço equivalente
   - Exemplo:
     - TCO Desktop: R$ 250/mês
     - Contrato DaaS (Desktop as a Service): R$ 200/mês
     - Decisão: Terceirizar (economiza R$ 50/mês)
8. Gera relatório gerencial:
   - Ranking ativos mais caros
   - TCO médio por tipo
   - ROI por ativo
   - Sugestões de terceirização

#### Automações

- ✅ Cálculo automático diário de TCO
- ✅ Coleta automática de custos diretos
- ✅ Alocação automática de custos indiretos
- ✅ Comparativo automático TCO vs Contrato
- ✅ Ranking automático de ativos mais caros
- ✅ Sugestões automáticas de terceirização
- ✅ Relatório gerencial mensal

#### Integrações

- **RF025 (Ativos):** Dados de ativos e manutenções
- **RF036 (Custos Fixos):** Custos de energia e infraestrutura
- **RF055 (Rateio):** Alocação de custos indiretos
- **RF004 (Auditoria):** Histórico de TCO
- **Hangfire:** Job diário de cálculo

#### Regras de Negócio Principais

- **RN-037-01:** TCO calculado diariamente para todos os ativos ativos
- **RN-037-02:** TCO = Custos Diretos + Custos Indiretos (15%)
- **RN-037-03:** Custos diretos: Aquisição, Manutenção, Suporte, Energia, Licenças
- **RN-037-04:** Custos indiretos: Administrativo (10%) + Infraestrutura (5%)
- **RN-037-05:** Comparação automática TCO vs Contrato de Serviço
- **RN-037-06:** Relatório gerencial gerado mensalmente
- **RN-037-07:** Sugestão de terceirização se TCO > Contrato + 20%
- **RN-037-08:** Histórico de TCO mantido por 5 anos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ TCO não calculado
- ❌ Decisões sem base de custo real
- ❌ Custos ocultos desconhecidos
- ❌ Sem comparativo Buy vs Lease
- ❌ Sem relatório de rentabilidade

**Melhorias no moderno:**

- ✅ TCO calculado automaticamente
- ✅ Decisões baseadas em dados reais
- ✅ Todos os custos rastreados
- ✅ Comparativo automático Buy vs Lease
- ✅ Relatório de rentabilidade por ativo
- ✅ Sugestões de terceirização

---

### 3.11 PRO-FAC-004: Notas Fiscais de Estoque

**Código:** PRO-FAC-004
**RFs Envolvidos:** RF042
**Área:** Ativos e Custos
**Criticidade:** Média

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Estoque] -->|Recebe NF em papel| B[Digita manualmente]
    B -->|Atualiza estoque| C[Sistema]
    C -->|Sem validação XML| D[Erros de digitação]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Fornecedor] -->|Envia XML NF-e| B[E-mail monitored]
    B -->|Parse XML| C[NF-e Parser]
    C -->|Valida DANFE| D{XML vs PDF}
    D -->|Divergência| E[Alerta compras]
    D -->|OK| F[Extrai dados]

    F -->|CFOP| G[Valida operação]
    F -->|Impostos| H[ICMS, IPI, PIS, COFINS]
    F -->|Itens| I[Produtos/Serviços]

    I -->|Para cada item| J{Existe no cadastro?}
    J -->|Não| K[Cadastra automático]
    J -->|Sim| L[Atualiza estoque]

    L -->|Quantidade| M[Entrada estoque]
    L -->|Valor| N[Contabilização]
    N -->|Lança| O[Plano Contas RF031]

    H -->|Registra| P[Impostos a recuperar]
    P -->|Crédito| Q[Apuração fiscal]

    style C fill:#27AE60
    style F fill:#27AE60
    style K fill:#27AE60
    style M fill:#27AE60
```

#### Descrição do Processo

Entrada automatizada de NF de compra via parse de XML, validação DANFE (XML vs PDF), atualização automática de estoque, contabilização automática, e controle de impostos (ICMS, IPI, PIS, COFINS) com crédito fiscal.

#### Atores

- **Sistema de NF-e:** Monitora e-mail e processa XMLs
- **Compras:** Valida divergências
- **Estoque:** Recebe itens
- **Contabilidade:** Valida impostos

#### Fluxo Principal

1. Sistema monitora caixa de e-mail `nfe@empresa.com`
2. Detecta e-mail com anexo XML de NF-e
3. Faz download do XML e PDF (DANFE)
4. `NF-e Parser` extrai dados do XML:
   - Emitente (CNPJ, IE, razão social)
   - Destinatário (validar se é nossa empresa)
   - Número NF-e, série, data emissão
   - Valor total
   - Itens (produtos/serviços)
   - Impostos (ICMS, IPI, PIS, COFINS)
   - CFOP (código fiscal)
5. Valida XML vs DANFE (PDF):
   - Compara valores totais
   - Compara impostos
   - Se divergência: alerta compras
6. Valida operação (CFOP):
   - 5.102: Venda de mercadoria
   - 1.101: Compra para industrialização
   - Valida se operação é válida
7. Para cada item da NF-e:
   - Busca produto no cadastro por código/descrição
   - **Se não existe:**
     - Cadastra automaticamente
     - Sugere categoria via ML
     - Aguarda aprovação de compras
   - **Se existe:**
     - Atualiza estoque (entrada)
     - Registra movimentação
8. Contabilização automática:
   - Lança no Plano de Contas (RF031)
   - Débito: Estoque (Ativo)
   - Crédito: Fornecedor (Passivo)
9. Registra impostos:
   - ICMS a recuperar
   - IPI a recuperar
   - PIS/COFINS a recuperar
10. Atualiza apuração fiscal mensal
11. Vincula NF-e ao pedido de compra (se houver)

**Fluxo de Validação Manual:**
1. Se XML vs PDF divergem
2. Compras acessa "Validações Pendentes"
3. Visualiza divergência:
   - XML: R$ 10.000
   - PDF: R$ 10.500
4. Contata fornecedor para correção
5. Bloqueia entrada no estoque até resolver

#### Automações

- ✅ Monitoramento automático de e-mail
- ✅ Parse automático de XML
- ✅ Validação automática XML vs DANFE
- ✅ Cadastro automático de produtos novos
- ✅ Atualização automática de estoque
- ✅ Contabilização automática
- ✅ Registro automático de impostos
- ✅ Apuração fiscal automática

#### Integrações

- **E-mail (IMAP):** Monitoramento de NF-e
- **NF-e Parser:** Extração de dados de XML
- **RF031 (Plano de Contas):** Contabilização
- **Azure ML:** Sugestão de categoria de produto
- **RF004 (Auditoria):** Histórico de entradas

#### Regras de Negócio Principais

- **RN-042-01:** Monitoramento automático de e-mail de NF-e
- **RN-042-02:** Validação obrigatória XML vs DANFE
- **RN-042-03:** Divergência XML vs PDF bloqueia entrada
- **RN-042-04:** Produtos novos cadastrados automaticamente (pendente aprovação)
- **RN-042-05:** Estoque atualizado automaticamente
- **RN-042-06:** Contabilização automática no Plano de Contas
- **RN-042-07:** Impostos a recuperar registrados automaticamente
- **RN-042-08:** XMLs armazenados por 7 anos

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Digitação manual de NF em papel
- ❌ Erros frequentes de digitação
- ❌ Sem validação XML vs PDF
- ❌ Atualização manual de estoque
- ❌ Contabilização manual (demorada)
- ❌ Sem controle de impostos a recuperar

**Melhorias no moderno:**

- ✅ Parse automático de XML
- ✅ Zero digitação (automático)
- ✅ Validação automática XML vs DANFE
- ✅ Atualização automática de estoque
- ✅ Contabilização automática
- ✅ Controle automático de créditos fiscais

---

### 3.12 PRO-FAC-005: Rateio Multi-dimensional

**Código:** PRO-FAC-005
**RFs Envolvidos:** RF055
**Área:** Ativos e Custos
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Contador] -->|Planilha Excel| B[Rateio manual]
    B -->|2-3 dias trabalho| C[Distribuição custos]
    C -->|Copia para sistema| D[Lançamentos]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Custo compartilhado] -->|Aluguel R$ 50k| B[Motor Rateio]
    B -->|Dimensão 1| C{Empresa}
    C -->|Empresa A| D[40% = R$ 20k]
    C -->|Empresa B| E[60% = R$ 30k]

    B -->|Dimensão 2| F{Departamento}
    F -->|TI| G[30% = R$ 15k]
    F -->|Financeiro| H[20% = R$ 10k]
    F -->|Comercial| I[50% = R$ 25k]

    B -->|Dimensão 3| J{Projeto}
    J -->|Projeto X| K[45% = R$ 22.5k]
    J -->|Projeto Y| L[55% = R$ 27.5k]

    B -->|Dimensão 4| M{Centro Custo}
    M -->|CC 100| N[25% = R$ 12.5k]
    M -->|CC 200| O[75% = R$ 37.5k]

    P[Regras Rateio] -->|Driver| Q{Tipo Driver}
    Q -->|Percentual fixo| R[40% / 60%]
    Q -->|Headcount| S[Por nº funcionários]
    Q -->|Área m²| T[Por metragem]
    Q -->|Consumo| U[Por uso real]

    R --> V[Cálculo tempo real]
    S --> V
    T --> V
    U --> V

    V -->|Lança automático| W[(SQL Server)]
    W -->|Dashboard| X[Relatório gerencial]

    style B fill:#27AE60
    style P fill:#27AE60
    style V fill:#27AE60
    style W fill:#27AE60
```

#### Descrição do Processo

Rateio automático de custos compartilhados por múltiplas dimensões (empresa, departamento, projeto, centro de custo), com drivers de alocação configuráveis (percentual fixo, headcount, área m², consumo real), cálculo em tempo real via triggers ou jobs, e relatórios gerenciais multi-dimensionais.

#### Atores

- **Financeiro:** Configura regras de rateio
- **Motor de Rateio:** Executa cálculos automaticamente
- **Gestor:** Consome relatórios
- **Sistema Contábil:** Recebe lançamentos

#### Fluxo Principal

**Fase 1: Configuração de Regras**

1. Financeiro acessa módulo "Rateio Multi-dimensional"
2. Cadastra custo compartilhado:
   - Tipo: Aluguel, Energia, TI, RH
   - Valor mensal: R$ 50.000
   - Descrição: "Aluguel Escritório SP"
3. Define dimensões de rateio:
   - **Dimensão 1: Empresa**
     - Empresa A: 40%
     - Empresa B: 60%
   - **Dimensão 2: Departamento**
     - TI: 30%
     - Financeiro: 20%
     - Comercial: 50%
   - **Dimensão 3: Projeto**
     - Projeto X: 45%
     - Projeto Y: 55%
   - **Dimensão 4: Centro de Custo**
     - CC 100: 25%
     - CC 200: 75%
4. Seleciona driver de alocação:
   - **Percentual fixo:** 40% / 60%
   - **Headcount:** Proporcional ao nº de funcionários
   - **Área (m²):** Proporcional à metragem ocupada
   - **Consumo:** Proporcional ao uso real (ex: energia)
5. Configura recálculo:
   - Tempo real (trigger)
   - Diário (job Hangfire)
   - Mensal (fechamento)
6. Sistema salva regras

**Fase 2: Execução do Rateio**

1. Trigger/Job inicia processamento
2. Para cada custo compartilhado:
   - Busca valor total
   - Busca regras de rateio
   - Aplica driver de alocação:

**Exemplo: Driver Headcount**
- TI: 30 funcionários
- Financeiro: 20 funcionários
- Comercial: 50 funcionários
- Total: 100 funcionários
- Rateio:
  - TI: (30/100) × R$ 50k = R$ 15k
  - Financeiro: (20/100) × R$ 50k = R$ 10k
  - Comercial: (50/100) × R$ 50k = R$ 25k

**Exemplo: Driver Área (m²)**
- TI: 150 m²
- Financeiro: 100 m²
- Comercial: 250 m²
- Total: 500 m²
- Rateio:
  - TI: (150/500) × R$ 50k = R$ 15k
  - Financeiro: (100/500) × R$ 50k = R$ 10k
  - Comercial: (250/500) × R$ 50k = R$ 25k

3. Sistema cria lançamentos contábeis:
   - Débito: Departamento (custo)
   - Crédito: Custo Compartilhado (clearing)
4. Atualiza dashboard gerencial

**Fase 3: Relatórios Gerenciais**

1. Gestor acessa dashboard
2. Seleciona dimensões para análise:
   - Custo por Empresa
   - Custo por Departamento
   - Custo por Projeto
   - Custo por Centro de Custo
3. Visualiza breakdown:
   - Total: R$ 50.000
   - TI: R$ 15.000 (30%)
   - Financeiro: R$ 10.000 (20%)
   - Comercial: R$ 25.000 (50%)
4. Exporta para Excel/PDF

#### Automações

- ✅ Rateio automático por múltiplas dimensões
- ✅ Cálculo automático por driver (%, headcount, m², consumo)
- ✅ Lançamentos contábeis automáticos
- ✅ Recálculo automático (tempo real ou job)
- ✅ Dashboard em tempo real
- ✅ Alertas de variação >10% mês anterior

#### Integrações

- **RF031 (Plano de Contas):** Lançamentos contábeis
- **RF036 (Custos Fixos):** Custos a ratear
- **RF037 (TCO):** Alocação de custos indiretos
- **Hangfire:** Jobs de rateio periódico
- **Power BI:** Dashboards gerenciais

#### Regras de Negócio Principais

- **RN-055-01:** Rateio multi-dimensional (até 5 dimensões)
- **RN-055-02:** Drivers suportados: Percentual, Headcount, Área, Consumo
- **RN-055-03:** Rateio pode ser tempo real ou periódico
- **RN-055-04:** Soma dos percentuais deve ser 100%
- **RN-055-05:** Lançamentos contábeis automáticos
- **RN-055-06:** Variação >10% gera alerta
- **RN-055-07:** Histórico de rateios mantido por 7 anos
- **RN-055-08:** Dashboard atualizado em tempo real

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Rateio manual em Excel (2-3 dias de trabalho)
- ❌ Apenas 1 dimensão (departamento)
- ❌ Percentuais fixos (sem drivers dinâmicos)
- ❌ Lançamentos manuais no sistema
- ❌ Sem dashboard gerencial
- ❌ Erros frequentes de cálculo

**Melhorias no moderno:**

- ✅ Rateio automático (segundos)
- ✅ Até 5 dimensões simultâneas
- ✅ 4 drivers dinâmicos (%, headcount, m², consumo)
- ✅ Lançamentos automáticos
- ✅ Dashboard em tempo real
- ✅ Zero erros de cálculo
- ✅ Auditoria completa

---

## 4. Matriz de Processos

| Código | Processo | RF | Criticidade | Automação | Integrações |
|--------|----------|----|-----------|-----------| ------------|
| **PRO-FCT-001** | Gestão de Faturas | RF026 | Alta | ✅ Geração, conciliação, baixa | RF032, OFX, RF089, RF066 |
| **PRO-FCT-002** | Parâmetros Faturamento | RF030 | Alta | ✅ Consulta IBGE, reajustes | IBGE API, RF026, RF090 |
| **PRO-FCT-003** | Plano de Contas | RF031 | Alta | ✅ Classificação ML, DRE | TOTVS, SAP, Azure ML, RF026 |
| **PRO-FCT-004** | NF-e | RF032 | Alta | ✅ Geração, assinatura, SEFAZ | SEFAZ, Azure Blob, iText7, RF026 |
| **PRO-FCT-005** | Conciliação Faturas | RF089 | Alta | ✅ OFX, matching, ML | Banco SFTP, RF026, Azure ML |
| **PRO-FCT-006** | Medição/Faturamento | RF090 | Alta | ✅ Pro-rata, rateio, aprovação | RF026, RF055, RF088 |
| **PRO-FCT-007** | Auditoria Faturas | RF097 | Alta | ✅ Validações, ML anomalias | RF026, RF030, Azure ML |
| **PRO-FAC-001** | Gestão Ativos | RF025 | Alta | ✅ Depreciação, QR Code, alertas | RF037, RF055, RF066 |
| **PRO-FAC-002** | Custos Fixos | RF036 | Média | ✅ Provisão, rateio, alertas | RF055, RF031, Hangfire |
| **PRO-FAC-003** | TCO | RF037 | Alta | ✅ Cálculo diário, Buy vs Lease | RF025, RF036, RF055 |
| **PRO-FAC-004** | NF Estoque | RF042 | Média | ✅ Parse XML, estoque, contabilização | E-mail, RF031, Azure ML |
| **PRO-FAC-005** | Rateio Multi-dimensional | RF055 | Alta | ✅ 4 drivers, tempo real | RF031, RF036, RF037, Power BI |

---

## 5. Glossário

| Termo | Definição |
|-------|-----------|
| **Backoff Exponencial** | Estratégia de retry onde intervalo aumenta progressivamente (1min, 5min, 15min) |
| **COFINS** | Contribuição para Financiamento da Seguridade Social (3% ou 7,6%) |
| **DANFE** | Documento Auxiliar da Nota Fiscal Eletrônica (PDF da NF-e) |
| **DRE** | Demonstração do Resultado do Exercício (relatório contábil) |
| **IGP-M** | Índice Geral de Preços do Mercado (reajuste de contratos) |
| **IPCA** | Índice de Preços ao Consumidor Amplo (inflação oficial) |
| **ISSQN** | Imposto Sobre Serviços de Qualquer Natureza (municipal, 2% a 5%) |
| **Matching Fuzzy** | Correspondência aproximada (valor ±5%, data ±3 dias) |
| **NF-e** | Nota Fiscal Eletrônica (emitida via WebService SEFAZ) |
| **Nosso Número** | Identificador único do boleto bancário |
| **OFX** | Open Financial Exchange (formato de extrato bancário) |
| **PIS** | Programa de Integração Social (0,65% ou 1,65%) |
| **Pro-rata** | Cálculo proporcional (ex: 15 dias/30 dias × valor) |
| **SEFAZ** | Secretaria da Fazenda (autoriza NF-e) |
| **Soft Delete** | Exclusão lógica (marca `Ativo=false`, mantém registro) |
| **SqlBulkCopy** | API .NET para insert massivo otimizado |
| **TCO** | Total Cost of Ownership (custo total de propriedade) |
| **WebService SEFAZ** | API oficial para autorização de NF-e |
| **XSD** | XML Schema Definition (estrutura XML oficial) |

---

## 6. Referências Cruzadas

### Jornadas Relacionadas

- **Jornada 1:** Infraestrutura e Configuração (PRO-INF-001 a PRO-INF-008)
- **Jornada 2:** Workflows e Importação (PRO-WKF-001 a PRO-WKF-009)

### Documentos de Governança

| Documento | Caminho | Relevância |
|-----------|---------|-----------|
| **ARCHITECTURE.md** | `D:\IC2_Governanca\governanca\ARCHITECTURE.md` | Stack tecnológico, padrões arquiteturais |
| **CONVENTIONS.md** | `D:\IC2_Governanca\governanca\CONVENTIONS.md` | Nomenclatura de handlers, repositories |
| **COMPLIANCE.md** | `D:\IC2_Governanca\governanca\COMPLIANCE.md` | Regras de validação e auditoria |
| **COMMANDS.md** | `D:\IC2_Governanca\governanca\COMMANDS.md` | Comandos de desenvolvimento e validação |

### RFs Relacionados

| RF | Título | Status |
|----|--------|--------|
| **RF025** | Gestão de Ativos | ✅ Implementado |
| **RF026** | Gestão de Faturas | ✅ Implementado |
| **RF030** | Parâmetros de Faturamento | ✅ Implementado |
| **RF031** | Plano de Contas | ✅ Implementado |
| **RF032** | Notas Fiscais/Faturas (NF-e) | ✅ Implementado |
| **RF036** | Custos Fixos | ✅ Implementado |
| **RF037** | Custos por Ativo (TCO) | ✅ Implementado |
| **RF042** | Notas Fiscais de Estoque | ✅ Implementado |
| **RF055** | Rateio Multi-dimensional | ✅ Implementado |
| **RF089** | Conciliação de Faturas | ✅ Implementado |
| **RF090** | Medição/Faturamento de Contratos | ✅ Implementado |
| **RF097** | Auditoria de Faturas | ✅ Implementado |

### Contratos de Execução

Para implementar ou manter processos desta jornada, consulte:

- **Backend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\backend-criacao.md`
- **Frontend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\frontend-criacao.md`
- **Manutenção:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\manutencao\CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md`
- **Auditoria:** `D:\IC2_Governanca\governanca\contracts\auditoria\conformidade.md`

---

## Controle de Versão

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-01-12 | ALC | Criação inicial com 12 processos da Jornada 3 Financeiro |

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 1.0


---

# PARTE 5: JORNADA 4 - SERVICE DESK

---


**Versão:** 1.0
**Data:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente

---

## Sumário

- [1. Introdução](#1-introdução)
- [2. Visão Geral da Jornada](#2-visão-geral-da-jornada)
- [3. Processos da Jornada](#3-processos-da-jornada)
  - [3.1 PRO-SVC-001: SLA de Operações](#31-pro-svc-001-sla-de-operações)
  - [3.2 PRO-SVC-002: SLA de Serviços](#32-pro-svc-002-sla-de-serviços)
  - [3.3 PRO-SVC-003: Gestão de Chamados](#33-pro-svc-003-gestão-de-chamados)
  - [3.4 PRO-SVC-004: SLA de Solicitações](#34-pro-svc-004-sla-de-solicitações)
  - [3.5 PRO-SVC-005: Gestão de Solicitações](#35-pro-svc-005-gestão-de-solicitações)
  - [3.6 PRO-SVC-006: Escalação Automática](#36-pro-svc-006-escalação-automática)
  - [3.7 PRO-SVC-007: Integração com ERPs](#37-pro-svc-007-integração-com-erps)
  - [3.8 PRO-SVC-008: APIs Externas](#38-pro-svc-008-apis-externas)
- [4. Matriz de Processos](#4-matriz-de-processos)
- [5. Glossário](#5-glossário)
- [6. Referências Cruzadas](#6-referências-cruzadas)

---

## 1. Introdução

Este documento detalha os **8 processos de negócio** da **Jornada 5: Service Desk** do sistema IControlIT modernizado.

### Escopo

A Jornada 5 abrange os processos de atendimento ao cliente, gestão de chamados, SLA e integrações corporativas:

- **SLA de Operações:** Cálculo automático de SLA com tempo útil
- **SLA de Serviços:** SLA específico por tipo de serviço
- **Gestão de Chamados:** Ciclo completo de incidentes e requisições
- **SLA de Solicitações:** Controle de prazos para requisições
- **Gestão de Solicitações:** Catálogo de serviços e workflows de aprovação
- **Escalação Automática:** Regras de escalação hierárquica
- **Integração com ERPs:** Sincronização bidirecional com sistemas corporativos
- **APIs Externas:** Exposição de APIs REST para integrações

### Organização do Documento

Cada processo é documentado com:

- **Código único** (PRO-SVC-XXX)
- **RFs associados**
- **Diagramas BPMN** (Legado vs Moderno)
- **Descrição narrativa**
- **Atores envolvidos**
- **Fluxo principal**
- **Automações implementadas**
- **Integrações**
- **Regras de negócio**
- **Comparação com legado**

---

## 2. Visão Geral da Jornada

### Objetivos da Jornada

1. **Automatizar SLA:** Cálculo inteligente de prazos com tempo útil, pausas e feriados
2. **Otimizar atendimento:** Triagem automática, base de conhecimento e escalação inteligente
3. **Garantir compliance:** Auditoria completa e indicadores de performance
4. **Integrar sistemas:** Sincronização bidirecional com ERPs corporativos
5. **Facilitar integrações:** APIs REST securizadas para sistemas externos

### Arquitetura da Jornada

```mermaid
graph TB
    subgraph "Gestão de SLA"
        A[SLA Operações<br/>RF028]
        B[SLA Serviços<br/>RF029]
        C[SLA Solicitações<br/>RF038]
    end

    subgraph "Atendimento"
        D[Gestão Chamados<br/>RF033]
        E[Gestão Solicitações<br/>RF053]
        F[Escalação Automática<br/>RF072]
    end

    subgraph "Integrações"
        G[Integração ERPs<br/>RF078]
        H[APIs Externas<br/>RF087]
    end

    A --> D
    B --> D
    C --> E
    D --> F
    E --> F
    G --> D
    G --> E
    H --> D
    H --> E

    style A fill:#4A90E2
    style B fill:#4A90E2
    style C fill:#4A90E2
    style D fill:#50C878
    style E fill:#50C878
    style F fill:#50C878
    style G fill:#9B59B6
    style H fill:#9B59B6
```

### Stack Tecnológico

- **Backend:** ASP.NET Core 8, MediatR (CQRS), Hangfire (jobs assíncronos)
- **SLA:** Motor customizado de cálculo de tempo útil, calendário de feriados
- **ML/IA:** Azure Cognitive Services (categorização automática)
- **Integrações:** TOTVS Protheus, SAP B1, Oracle EBS via WebServices
- **APIs:** REST com OAuth 2.0, Rate Limiting, Webhooks
- **Real-time:** SignalR (notificações em tempo real)
- **Observabilidade:** Application Insights, Serilog

---

## 3. Processos da Jornada

### 3.1 PRO-SVC-001: SLA de Operações

**Código:** PRO-SVC-001
**RFs Envolvidos:** RF028
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Chamado criado] -->|SLA fixo 4h| B[Planilha Excel]
    B -->|Analista calcula manual| C[Tempo decorrido]
    C -->|Ignora pausas| D[SLA impreciso]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Chamado criado] -->|Determina prioridade| B{Matriz Impacto×Urgência}
    B -->|P1 Crítico| C[SLA: 2h úteis]
    B -->|P2 Alto| D[SLA: 4h úteis]
    B -->|P3 Médio| E[SLA: 8h úteis]
    B -->|P4 Baixo| F[SLA: 24h úteis]

    C --> G[Job Hangfire a cada 5min]
    D --> G
    E --> G
    F --> G

    G -->|Calcula tempo útil| H[Motor SLA]
    H -->|Considera| I[Horário comercial]
    H -->|Considera| J[Pausas cliente/fornecedor]
    H -->|Considera| K[Feriados nacionais/regionais]

    H -->|70% SLA| L[Alerta amarelo]
    H -->|90% SLA| M[Alerta laranja]
    H -->|100% SLA| N[Alerta vermelho + Escalação]

    N --> O[Notificação RF066]
    O --> P[E-mail + Push + SMS]

    style B fill:#F39C12
    style G fill:#3498DB
    style H fill:#3498DB
    style L fill:#F39C12
    style M fill:#E67E22
    style N fill:#E74C3C
    style P fill:#27AE60
```

#### Descrição do Processo

Sistema inteligente de cálculo de SLA que considera tempo útil (horário comercial 8h-18h), pausas automáticas (aguardando cliente, aguardando fornecedor), feriados nacionais e regionais, e priorização automática via matriz impacto × urgência. Inclui alertas progressivos (70%, 90%, 100%) e escalação automática em caso de violação.

#### Atores

- **Sistema de SLA:** Calcula prazos automaticamente
- **Job Hangfire:** Monitora prazos a cada 5 minutos
- **Técnico:** Atende chamados dentro do prazo
- **Gestor:** Recebe alertas de violação
- **Cliente:** Beneficia-se de prazos respeitados

#### Fluxo Principal

1. Chamado criado no sistema
2. Sistema determina prioridade via matriz impacto × urgência:
   - **P1 (Crítico):** Sistema parado, impacto em toda empresa → SLA 2h úteis
   - **P2 (Alto):** Funcionalidade crítica afetada → SLA 4h úteis
   - **P3 (Médio):** Funcionalidade secundária afetada → SLA 8h úteis
   - **P4 (Baixo):** Dúvidas, melhorias → SLA 24h úteis
3. Sistema registra timestamp de início
4. Job Hangfire executa a cada 5 minutos:
   - Calcula tempo decorrido útil
   - Desconta pausas (aguardando cliente, aguardando fornecedor)
   - Desconta feriados e fins de semana
   - Considera horário comercial (8h-18h padrão, configurável)
5. Sistema calcula percentual de consumo do SLA:
   - **0-69%:** Status verde (normal)
   - **70-89%:** Status amarelo (atenção) → Notifica técnico
   - **90-99%:** Status laranja (crítico) → Notifica técnico + coordenador
   - **100%+:** Status vermelho (violado) → Escalação automática + notificação gestor
6. Alertas enviados via RF066 (e-mail, push, SMS)
7. Dashboard exibe compliance SLA em tempo real

**Fluxo de Pausa:**

1. Técnico solicita informação ao cliente
2. Status alterado para "Aguardando Cliente"
3. Contador de SLA pausado automaticamente
4. Cliente responde
5. Status retorna para "Em Atendimento"
6. Contador de SLA retomado

#### Automações

- ✅ Cálculo automático de tempo útil (horário comercial)
- ✅ Desconto automático de pausas (cliente, fornecedor)
- ✅ Desconto automático de feriados (API de calendário)
- ✅ Priorização automática via matriz impacto × urgência
- ✅ Alertas progressivos (70%, 90%, 100%)
- ✅ Escalação automática em violação de SLA
- ✅ Notificações multi-canal (e-mail, push, SMS)
- ✅ Dashboard de compliance em tempo real

#### Integrações

- **Hangfire:** Jobs de monitoramento a cada 5 minutos
- **API Calendário (Brasil API):** Feriados nacionais e regionais
- **RF066 (Notificações):** Alertas multi-canal
- **RF072 (Escalação):** Escalação automática
- **SignalR:** Dashboard em tempo real
- **RF004 (Auditoria):** Registro de violações

#### Regras de Negócio Principais

- **RN-028-01:** SLA calculado em tempo útil (horário comercial 8h-18h)
- **RN-028-02:** Prioridades: P1 (2h), P2 (4h), P3 (8h), P4 (24h)
- **RN-028-03:** Pausas "Aguardando Cliente" e "Aguardando Fornecedor" não contam no SLA
- **RN-028-04:** Feriados nacionais e regionais descontados automaticamente
- **RN-028-05:** Fins de semana não contam no SLA
- **RN-028-06:** Alertas em 70%, 90% e 100% do prazo
- **RN-028-07:** Violação de SLA P1 dispara escalação imediata
- **RN-028-08:** Dashboard atualizado a cada 5 minutos
- **RN-028-09:** Horário comercial configurável por cliente (multi-tenancy)

**[Ver regras completas em RF028.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ SLA calculado manualmente em planilhas Excel
- ❌ Tempo corrido (ignorava fins de semana e feriados)
- ❌ Sem pausas automáticas (SLA consumido injustamente)
- ❌ Sem alertas proativos (descoberta reativa de violações)
- ❌ Priorização manual e subjetiva
- ❌ Sem escalação automática
- ❌ Relatórios manuais de compliance

**Melhorias no moderno:**

- ✅ Cálculo automático de tempo útil via job a cada 5 minutos
- ✅ Considera horário comercial, feriados e pausas
- ✅ Pausas automáticas por status (aguardando cliente/fornecedor)
- ✅ Alertas progressivos proativos (70%, 90%, 100%)
- ✅ Priorização automática via matriz impacto × urgência
- ✅ Escalação automática em violações
- ✅ Dashboard de compliance em tempo real
- ✅ Auditoria completa de todas as operações

---

### 3.2 PRO-SVC-002: SLA de Serviços

**Código:** PRO-SVC-002
**RFs Envolvidos:** RF029
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Chamado aberto] -->|SLA único 4h| B[Todos os tipos]
    B -->|Sem distinção| C[Incidente = Requisição]
    C -->|Sem TFR| D[Cliente sem retorno]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Chamado criado] -->|Classifica tipo| B{Tipo de Serviço}
    B -->|Incidente| C[TFR: 30min / TTR: 4h]
    B -->|Requisição| D[TFR: 1h / TTR: 8h]
    B -->|Mudança| E[TFR: 2h / TTR: Planejado]

    C --> F[Motor SLA RF028]
    D --> F
    E --> F

    F -->|Calcula TFR| G{Primeira resposta?}
    G -->|Não| H[Alerta TFR vencido]
    G -->|Sim| I[Marca timestamp]

    F -->|Calcula TTR| J{Resolvido?}
    J -->|Não| K[Alerta TTR próximo]
    J -->|Sim| L[Marca timestamp resolução]

    M[Pausa automática] -->|Cliente não responde| N[Aguardando Cliente]
    N -->|Pausa SLA| F

    O[Pausa automática] -->|Depende fornecedor| P[Aguardando Fornecedor]
    P -->|Pausa SLA| F

    Q[Relatório Breach] -->|Violações| R[Dashboard Gestor]

    style B fill:#F39C12
    style F fill:#3498DB
    style G fill:#F39C12
    style J fill:#F39C12
    style M fill:#3498DB
    style O fill:#3498DB
    style R fill:#27AE60
```

#### Descrição do Processo

Sistema de SLA diferenciado por tipo de serviço (Incidente, Requisição, Mudança) com controle de TFR (Tempo de Primeira Resposta) e TTR (Tempo de Resolução). Implementa pausas automáticas para dependências externas, rastreamento de breaches (violações) e relatórios gerenciais de performance.

#### Atores

- **Sistema de Classificação:** Determina tipo de serviço
- **Técnico:** Fornece primeira resposta e resolução
- **Cliente:** Aguarda atendimento dentro do prazo
- **Gestor de Service Desk:** Monitora breaches
- **Sistema de SLA:** Calcula prazos automaticamente

#### Fluxo Principal

1. Chamado criado no sistema
2. Sistema classifica automaticamente o tipo de serviço:
   - **Incidente:** Falha, erro, problema → TFR 30min / TTR 4h
   - **Requisição:** Solicitação de serviço → TFR 1h / TTR 8h
   - **Mudança:** Alteração planejada → TFR 2h / TTR conforme planejamento
3. Sistema inicia contadores separados:
   - **TFR (Time to First Response):** Tempo até primeira resposta do técnico
   - **TTR (Time to Resolution):** Tempo até resolução completa
4. Job Hangfire monitora ambos os contadores a cada 5 minutos
5. **Fluxo TFR:**
   - Sistema verifica se técnico deu primeira resposta
   - Se não: calcula tempo decorrido útil
   - Se 80% do TFR: alerta amarelo ao técnico
   - Se 100% do TFR: alerta vermelho + registra breach
6. **Fluxo TTR:**
   - Sistema verifica se chamado foi resolvido
   - Desconta pausas automáticas:
     - "Aguardando Cliente" (cliente não respondeu em 24h)
     - "Aguardando Fornecedor" (dependência externa)
   - Se 90% do TTR: alerta laranja ao técnico + coordenador
   - Se 100% do TTR: alerta vermelho + escalação automática
7. **Fluxo de Pausa Automática:**
   - Técnico solicita informação ao cliente
   - Sistema aguarda 24 horas
   - Se cliente não responder: pausa automática "Aguardando Cliente"
   - Cliente responde: retoma contador automaticamente
8. **Relatório de Breach:**
   - Sistema consolida violações diárias
   - Identifica causas (técnico, pausa cliente, complexidade)
   - Gera relatório para gestor
   - Dashboard exibe taxa de compliance por tipo de serviço

#### Automações

- ✅ Classificação automática de tipo de serviço
- ✅ Contadores separados para TFR e TTR
- ✅ Pausa automática "Aguardando Cliente" após 24h sem resposta
- ✅ Pausa automática "Aguardando Fornecedor" para dependências externas
- ✅ Alertas diferenciados por tipo de serviço
- ✅ Escalação automática em breaches de TTR
- ✅ Geração automática de relatório de breaches
- ✅ Dashboard de compliance por tipo de serviço

#### Integrações

- **RF028 (SLA Operações):** Motor de cálculo de tempo útil
- **RF066 (Notificações):** Alertas multi-canal
- **RF072 (Escalação):** Escalação automática em breaches
- **Hangfire:** Jobs de monitoramento
- **SignalR:** Dashboard em tempo real
- **RF004 (Auditoria):** Registro de breaches

#### Regras de Negócio Principais

- **RN-029-01:** TFR Incidente: 30 minutos úteis
- **RN-029-02:** TTR Incidente: 4 horas úteis
- **RN-029-03:** TFR Requisição: 1 hora útil
- **RN-029-04:** TTR Requisição: 8 horas úteis
- **RN-029-05:** TFR Mudança: 2 horas úteis
- **RN-029-06:** TTR Mudança: conforme planejamento
- **RN-029-07:** Pausa automática "Aguardando Cliente" após 24h sem resposta
- **RN-029-08:** Pausa automática "Aguardando Fornecedor" para dependências externas
- **RN-029-09:** Breach de TFR não dispara escalação (apenas alerta)
- **RN-029-10:** Breach de TTR dispara escalação automática
- **RN-029-11:** Relatório de breach consolidado diariamente

**[Ver regras completas em RF029.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ SLA único para todos os tipos de serviço (4h)
- ❌ Sem controle de TFR (cliente sem retorno inicial)
- ❌ Sem diferenciação Incidente vs Requisição
- ❌ Pausas manuais (inconsistentes)
- ❌ Sem relatório de breaches
- ❌ Sem análise de causa de violações

**Melhorias no moderno:**

- ✅ SLA diferenciado por tipo de serviço
- ✅ Controle de TFR (primeira resposta) e TTR (resolução)
- ✅ Classificação automática Incidente/Requisição/Mudança
- ✅ Pausas automáticas por regras (24h sem resposta)
- ✅ Relatório automático de breaches com causa raiz
- ✅ Dashboard de compliance por tipo de serviço
- ✅ Análise de tendências de violações

---

### 3.3 PRO-SVC-003: Gestão de Chamados

**Código:** PRO-SVC-003
**RFs Envolvidos:** RF033
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Cliente] -->|Abre via e-mail| B[Caixa compartilhada]
    B -->|Técnico vê manual| C[Atende]
    C -->|Responde e-mail| D[Cliente]
    D -->|Sem rastreamento| E[Histórico perdido]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Cliente] -->|Portal/E-mail/Chat| B[Sistema Triagem]
    B -->|Categoriza ML| C{Categoria Automática}
    C -->|Infraestrutura| D[Fila Infra]
    C -->|Aplicação| E[Fila App]
    C -->|Usuário| F[Fila Suporte]

    D --> G[Base de Conhecimento]
    E --> G
    F --> G

    G -->|Sugere artigo| H{Cliente resolve sozinho?}
    H -->|Sim| I[Auto-resolução]
    H -->|Não| J[Atribuição Técnico]

    J -->|Matriz Impacto×Urgência| K{Prioridade}
    K -->|P1| L[Técnico Sênior]
    K -->|P2-P4| M[Técnico Disponível]

    L --> N[Atendimento]
    M --> N

    N -->|SignalR| O[Cliente acompanha tempo real]
    N -->|Resolve| P[Solicita aprovação cliente]
    P -->|Cliente aprova| Q[Fecha chamado]
    Q -->|NPS automático| R[Pesquisa satisfação]

    S[Notificação RF066] -->|E-mail/Push| A

    style B fill:#3498DB
    style C fill:#F39C12
    style G fill:#3498DB
    style K fill:#F39C12
    style O fill:#27AE60
    style R fill:#27AE60
```

#### Descrição do Processo

Ciclo completo de gestão de chamados desde abertura multi-canal (portal, e-mail, chat), triagem automática via Machine Learning, categorização inteligente, atribuição baseada em matriz impacto × urgência, integração com base de conhecimento para auto-resolução, acompanhamento em tempo real via SignalR, até fechamento com NPS automático.

#### Atores

- **Cliente:** Abre e acompanha chamados
- **Sistema de Triagem:** Categoriza automaticamente via ML
- **Base de Conhecimento:** Sugere soluções
- **Técnico:** Atende e resolve chamados
- **Coordenador:** Monitora filas e performance
- **Sistema de NPS:** Coleta satisfação pós-atendimento

#### Fluxo Principal

1. **Abertura do Chamado:**
   - Cliente acessa portal self-service, envia e-mail ou usa chat
   - Sistema captura título, descrição, anexos
   - Registra ClienteId, UserId, timestamp
2. **Triagem Automática:**
   - Sistema analisa descrição via ML (Azure Cognitive Services)
   - Categoriza automaticamente:
     - **Infraestrutura:** rede, servidor, storage
     - **Aplicação:** bugs, erros, funcionalidades
     - **Usuário:** senha, acesso, dúvidas
   - Acurácia: 85%+ (treinamento contínuo)
3. **Sugestão de Base de Conhecimento:**
   - Sistema busca artigos relacionados (full-text search)
   - Exibe top 3 artigos mais relevantes ao cliente
   - Cliente tenta resolver sozinho
4. **Auto-resolução ou Atribuição:**
   - Se cliente resolve: marca como "Auto-resolvido" (economia)
   - Se não resolve: prossegue para atribuição
5. **Priorização Automática:**
   - Matriz impacto × urgência:
     - **Impacto:** Quantos usuários afetados? (1 usuário, departamento, empresa toda)
     - **Urgência:** Quanto tempo pode esperar? (imediato, hoje, esta semana)
   - Resultado: P1 (Crítico), P2 (Alto), P3 (Médio), P4 (Baixo)
6. **Atribuição Inteligente:**
   - P1: atribui automaticamente a técnico sênior disponível
   - P2-P4: atribui a técnico com menor fila
   - Considera especialização (categoria do chamado vs skills do técnico)
7. **Atendimento:**
   - Técnico recebe notificação push
   - Acessa chamado no painel
   - Interage com cliente via comentários (rastreados)
   - Cliente acompanha status em tempo real via SignalR
8. **Resolução:**
   - Técnico marca como "Resolvido"
   - Sistema solicita aprovação do cliente
   - Cliente aprova: chamado fechado
   - Cliente não aprova: reabre automaticamente
9. **NPS Automático:**
   - Sistema envia pesquisa de satisfação por e-mail
   - Escala 0-10: "Recomendaria nosso atendimento?"
   - Feedback agregado em dashboard de qualidade

**Fluxo de Escalação (RF072):**

- SLA próximo de expirar (90%)
- Sistema verifica regras de escalação
- Notifica coordenador automaticamente
- Coordenador pode reassignar ou assumir

#### Automações

- ✅ Categorização automática via Machine Learning (85% acurácia)
- ✅ Sugestão automática de artigos da base de conhecimento
- ✅ Priorização automática via matriz impacto × urgência
- ✅ Atribuição inteligente baseada em disponibilidade e especialização
- ✅ Notificações em tempo real via SignalR
- ✅ Solicitação automática de aprovação do cliente
- ✅ Envio automático de NPS pós-fechamento
- ✅ Dashboard de performance em tempo real

#### Integrações

- **Azure Cognitive Services:** Categorização automática via ML
- **Base de Conhecimento:** Sugestão de artigos (full-text search)
- **RF028 (SLA Operações):** Controle de prazos
- **RF066 (Notificações):** Alertas multi-canal
- **RF072 (Escalação):** Escalação automática
- **SignalR:** Acompanhamento em tempo real
- **RF004 (Auditoria):** Histórico completo

#### Regras de Negócio Principais

- **RN-033-01:** Canais de abertura: portal, e-mail, chat, telefone (registrado)
- **RN-033-02:** Categorização automática via ML com 85%+ de acurácia
- **RN-033-03:** Base de conhecimento consultada antes de atribuição
- **RN-033-04:** Auto-resoluções contam como economia de custo
- **RN-033-05:** Priorização via matriz impacto × urgência
- **RN-033-06:** P1 atribuído automaticamente a técnico sênior
- **RN-033-07:** Aprovação do cliente obrigatória para fechar chamado
- **RN-033-08:** NPS enviado automaticamente após fechamento
- **RN-033-09:** Cliente pode reabrir chamado em até 7 dias
- **RN-033-10:** Histórico completo auditável (LGPD compliant)

**[Ver regras completas em RF033.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Abertura apenas por e-mail (caixa compartilhada)
- ❌ Triagem manual (técnico lia e-mails um por um)
- ❌ Categorização manual e inconsistente
- ❌ Sem base de conhecimento integrada
- ❌ Priorização subjetiva (quem grita mais alto)
- ❌ Atribuição manual pelo coordenador
- ❌ Cliente sem visibilidade do status
- ❌ NPS manual (1x por ano, taxa de resposta baixa)
- ❌ Histórico em e-mails (não estruturado)

**Melhorias no moderno:**

- ✅ Abertura multi-canal (portal, e-mail, chat, telefone)
- ✅ Triagem automática via ML (85% acurácia)
- ✅ Categorização padronizada e consistente
- ✅ Base de conhecimento integrada (auto-resolução)
- ✅ Priorização objetiva via matriz impacto × urgência
- ✅ Atribuição inteligente (disponibilidade + especialização)
- ✅ Cliente acompanha em tempo real via SignalR
- ✅ NPS automático pós-fechamento (taxa de resposta 60%+)
- ✅ Histórico estruturado e auditável

---

### 3.4 PRO-SVC-004: SLA de Solicitações

**Código:** PRO-SVC-004
**RFs Envolvidos:** RF038
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Solicitação] -->|Prazo informal| B[E-mail gerente]
    B -->|Aprovação manual| C[Execução]
    C -->|Sem controle prazo| D[Atraso frequente]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Solicitação criada] -->|Tipo de serviço| B{Catálogo}
    B -->|Provisionamento usuário| C[SLA: 2h / Aprovação: 30min]
    B -->|Licença software| D[SLA: 4h / Aprovação: 1h]
    B -->|Hardware| E[SLA: 24h / Aprovação: 4h]

    C --> F[Workflow Aprovação]
    D --> F
    E --> F

    F -->|Nível 1| G[Gerente Imediato]
    G -->|Aprova| H{Aprovação TI?}
    G -->|Rejeita| I[Notifica solicitante]

    H -->|Sim| J[Diretor TI]
    H -->|Não| K[Execução]

    J -->|Aprova| K
    J -->|Rejeita| I

    K -->|Monitora SLA| L[Job Hangfire]
    L -->|Calcula prazo| M{SLA execução}
    M -->|90%| N[Alerta técnico]
    M -->|100%| O[Escalação]

    K -->|Concluído| P[Solicita aprovação]
    P -->|Cliente aprova| Q[Fecha solicitação]

    R[Indicadores] -->|Taxa aprovação| S[Dashboard Gestor]
    R -->|Tempo médio| S
    R -->|Taxa cumprimento SLA| S

    style B fill:#F39C12
    style F fill:#3498DB
    style H fill:#F39C12
    style L fill:#3498DB
    style S fill:#27AE60
```

#### Descrição do Processo

Sistema de SLA específico para requisições de serviço com workflow multi-nível configurável (aprovação gerencial → aprovação TI → execução). Calcula prazos diferenciados por tipo de solicitação, monitora tempo de aprovação e tempo de execução separadamente, e gera indicadores de performance (taxa de aprovação, tempo médio, cumprimento de SLA).

#### Atores

- **Solicitante:** Cria requisições de serviço
- **Gerente:** Aprova ou rejeita no nível gerencial
- **Diretor TI:** Aprova requisições que requerem nível TI
- **Técnico:** Executa solicitações aprovadas
- **Sistema de Workflow:** Orquestra aprovações
- **Gestor de Service Desk:** Monitora indicadores

#### Fluxo Principal

1. **Criação da Solicitação:**
   - Solicitante acessa catálogo de serviços
   - Seleciona tipo de serviço (ex: "Provisionamento de Usuário")
   - Preenche formulário dinâmico (campos variam por tipo)
   - Sistema registra solicitação com status "Pendente Aprovação"
2. **Determinação de SLA:**
   - Sistema consulta SLA configurado para o tipo:
     - **Provisionamento usuário:** Aprovação 30min / Execução 2h
     - **Licença software:** Aprovação 1h / Execução 4h
     - **Hardware:** Aprovação 4h / Execução 24h
   - Inicia contadores separados para aprovação e execução
3. **Workflow de Aprovação Multi-Nível:**
   - **Nível 1 - Gerente Imediato:**
     - Notificado via e-mail + push
     - Prazo: conforme SLA de aprovação
     - Decide: Aprovar ou Rejeitar (justificativa obrigatória)
   - **Nível 2 - Diretor TI (se necessário):**
     - Acionado automaticamente após aprovação nível 1
     - Decide: Aprovar ou Rejeitar
     - Prazo compartilhado com nível 1 (contador único)
4. **Monitoramento de SLA de Aprovação:**
   - Job Hangfire monitora a cada 5 minutos
   - Se 80% do prazo: alerta amarelo ao aprovador
   - Se 100% do prazo: alerta vermelho + escalação ao superior
5. **Execução (após aprovação completa):**
   - Solicitação atribuída automaticamente a técnico
   - Contador de SLA de execução iniciado
   - Técnico executa a solicitação
   - Registra evidências (screenshots, logs)
6. **Monitoramento de SLA de Execução:**
   - Job Hangfire monitora a cada 5 minutos
   - Se 90% do prazo: alerta laranja ao técnico + coordenador
   - Se 100% do prazo: alerta vermelho + escalação automática
7. **Conclusão:**
   - Técnico marca como "Concluído"
   - Sistema solicita aprovação do solicitante
   - Solicitante aprova: solicitação fechada
   - Solicitante não aprova: reabre para correção
8. **Indicadores de Performance:**
   - **Taxa de aprovação:** (Aprovadas / Total) × 100%
   - **Tempo médio de aprovação:** Média de tempo por nível
   - **Taxa de cumprimento SLA:** (Dentro do prazo / Total) × 100%
   - **Tempo médio de execução:** Média de tempo por tipo
   - Dashboard atualizado em tempo real

#### Automações

- ✅ Determinação automática de SLA por tipo de serviço
- ✅ Workflow de aprovação multi-nível configurável
- ✅ Contadores separados para aprovação e execução
- ✅ Notificações automáticas aos aprovadores
- ✅ Escalação automática em atrasos de aprovação
- ✅ Escalação automática em atrasos de execução
- ✅ Cálculo automático de indicadores de performance
- ✅ Dashboard de gestão em tempo real

#### Integrações

- **RF053 (Gestão Solicitações):** Catálogo de serviços e formulários
- **RF088 (Workflows Aprovação):** Motor de aprovações multi-nível
- **RF028 (SLA Operações):** Motor de cálculo de tempo útil
- **RF066 (Notificações):** Alertas aos aprovadores e técnicos
- **RF072 (Escalação):** Escalação automática em atrasos
- **Hangfire:** Jobs de monitoramento
- **SignalR:** Dashboard em tempo real

#### Regras de Negócio Principais

- **RN-038-01:** SLA diferenciado por tipo de solicitação
- **RN-038-02:** Contadores separados: aprovação e execução
- **RN-038-03:** Aprovação gerencial obrigatória para todas as solicitações
- **RN-038-04:** Aprovação TI obrigatória para licenças e hardware
- **RN-038-05:** Rejeição requer justificativa obrigatória
- **RN-038-06:** Escalação automática em 100% do prazo de aprovação
- **RN-038-07:** Escalação automática em 100% do prazo de execução
- **RN-038-08:** Indicadores calculados em tempo real
- **RN-038-09:** Taxa de aprovação meta: 85%+
- **RN-038-10:** Taxa de cumprimento SLA meta: 95%+

**[Ver regras completas em RF038.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Solicitações via e-mail (não estruturadas)
- ❌ Aprovação manual via e-mail (sem controle de prazo)
- ❌ Sem workflow configurável (hardcoded)
- ❌ SLA único para todas as solicitações
- ❌ Sem diferenciação entre aprovação e execução
- ❌ Sem escalação automática
- ❌ Sem indicadores de performance
- ❌ Relatórios manuais em Excel

**Melhorias no moderno:**

- ✅ Solicitações estruturadas via catálogo de serviços
- ✅ Aprovação automática via workflow configurável
- ✅ SLA diferenciado por tipo de solicitação
- ✅ Contadores separados (aprovação vs execução)
- ✅ Escalação automática em atrasos
- ✅ Indicadores automatizados (taxa aprovação, tempo médio, compliance)
- ✅ Dashboard de gestão em tempo real
- ✅ Auditoria completa de aprovações

---

### 3.5 PRO-SVC-005: Gestão de Solicitações

**Código:** PRO-SVC-005
**RFs Envolvidos:** RF053
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Usuário] -->|E-mail genérico| B[Solicitação texto livre]
    B -->|Técnico interpreta| C[Executa]
    C -->|Sem aprovação formal| D[Risco compliance]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Usuário] -->|Acessa portal| B[Catálogo de Serviços]
    B -->|Provisionamento| C[Formulário Usuário]
    B -->|Licença| D[Formulário Software]
    B -->|Hardware| E[Formulário Equipamento]

    C -->|Campos dinâmicos| F[Nome, CPF, Depto, Cargo]
    D -->|Campos dinâmicos| G[Software, Versão, Justificativa]
    E -->|Campos dinâmicos| H[Tipo, Config, Centro Custo]

    F --> I[Validação FluentValidation]
    G --> I
    H --> I

    I -->|OK| J[Workflow Aprovação RF088]
    J -->|Gerente| K[Aprova/Rejeita]
    K -->|Aprovado| L{Requer TI?}
    L -->|Sim| M[Diretor TI aprova]
    L -->|Não| N[Execução Automática]

    M -->|Aprovado| N
    N -->|Provisionamento| O[Script PowerShell]
    N -->|Licença| P[API fornecedor]
    N -->|Hardware| Q[Ordem Compra ERP]

    O --> R[Confirma execução]
    P --> R
    Q --> R

    R -->|NPS automático| S[Pesquisa satisfação]
    S -->|Feedback| T[Dashboard Qualidade]

    style B fill:#3498DB
    style I fill:#3498DB
    style J fill:#3498DB
    style N fill:#27AE60
    style T fill:#27AE60
```

#### Descrição do Processo

Sistema completo de gestão de solicitações com catálogo de serviços estruturado, formulários dinâmicos por tipo, aprovações em cadeia configuráveis (gerente → diretor → TI), execução automatizada para casos simples (provisionamento de usuário, ativação de licenças), e NPS automático pós-atendimento para medir satisfação.

#### Atores

- **Usuário Final:** Solicita serviços via catálogo
- **Catálogo de Serviços:** Lista serviços disponíveis
- **Gerente:** Aprova solicitações da equipe
- **Diretor TI:** Aprova solicitações críticas (licenças, hardware)
- **Sistema de Automação:** Executa provisionamentos automatizados
- **Técnico:** Executa solicitações que requerem intervenção manual

#### Fluxo Principal

1. **Acesso ao Catálogo:**
   - Usuário acessa portal self-service
   - Visualiza catálogo de serviços disponíveis:
     - **Provisionamento de Usuário:** Criar novo usuário no AD, Office 365, sistemas corporativos
     - **Licença de Software:** Ativar/desativar licenças (Adobe, Microsoft, Autocad)
     - **Hardware:** Notebook, desktop, monitor, mouse, teclado
     - **Acesso a Sistema:** Permissões específicas em sistemas
     - **Alteração de Dados:** Departamento, cargo, centro de custo
2. **Seleção de Serviço e Preenchimento:**
   - Usuário seleciona serviço (ex: "Licença de Software")
   - Sistema exibe formulário dinâmico específico:
     - Campos obrigatórios: Software, Versão, Justificativa, Centro de Custo
     - Campos opcionais: Prazo desejado, Observações
   - Anexos: permite upload de documentos (ordem de compra, aprovação prévia)
3. **Validação Automática:**
   - FluentValidation valida campos obrigatórios
   - Validações específicas por tipo:
     - **Provisionamento:** CPF válido, e-mail corporativo único
     - **Licença:** Justificativa mínimo 50 caracteres
     - **Hardware:** Centro de custo válido
   - Se inválido: retorna erros específicos ao usuário
4. **Workflow de Aprovação (RF088):**
   - Solicitação submetida ao workflow configurado:
     - **Gerente Imediato:** Sempre requerido (valida necessidade)
     - **Diretor TI:** Requerido para licenças e hardware
     - **Financeiro:** Requerido para valores > R$5.000
   - Aprovadores notificados via e-mail + push
   - Podem aprovar, rejeitar ou solicitar informações adicionais
5. **Execução (após aprovações completas):**
   - **Automática (onde aplicável):**
     - **Provisionamento usuário:** Script PowerShell cria usuário no AD + Office 365
     - **Ativação licença:** API do fornecedor ativa licença automaticamente
     - **Acesso sistema:** Script SQL atualiza permissões
   - **Manual (onde necessário):**
     - **Hardware:** Técnico registra ordem de compra no ERP via RF078
     - **Alterações complexas:** Técnico executa manualmente e documenta
6. **Confirmação de Execução:**
   - Sistema registra evidências:
     - **Automático:** Logs de scripts, respostas de APIs
     - **Manual:** Screenshots, número de ordem de compra
   - Marca solicitação como "Concluído"
   - Solicita aprovação do solicitante
7. **NPS Automático:**
   - Sistema envia pesquisa de satisfação por e-mail
   - Perguntas:
     - "Recomendaria nosso serviço?" (0-10)
     - "O prazo foi cumprido?" (Sim/Não)
     - "A qualidade atendeu expectativas?" (1-5 estrelas)
     - Comentários opcionais
   - Respostas agregadas em dashboard de qualidade

#### Automações

- ✅ Catálogo de serviços estruturado e configurável
- ✅ Formulários dinâmicos por tipo de serviço
- ✅ Validação automática via FluentValidation
- ✅ Workflow de aprovação em cadeia (RF088)
- ✅ Execução automatizada (PowerShell, APIs)
- ✅ Integração com ERP para ordem de compra (RF078)
- ✅ Registro automático de evidências
- ✅ NPS automático pós-atendimento
- ✅ Dashboard de satisfação em tempo real

#### Integrações

- **RF088 (Workflows Aprovação):** Aprovações em cadeia
- **RF038 (SLA Solicitações):** Controle de prazos
- **Active Directory:** Provisionamento de usuários
- **Office 365 API:** Criação de contas e-mail
- **APIs Fornecedores (Adobe, Microsoft):** Ativação de licenças
- **RF078 (Integração ERP):** Ordem de compra de hardware
- **PowerShell:** Automações de provisionamento
- **RF066 (Notificações):** Alertas aos aprovadores
- **RF004 (Auditoria):** Histórico completo de solicitações

#### Regras de Negócio Principais

- **RN-053-01:** Catálogo de serviços configurável por administrador
- **RN-053-02:** Formulários dinâmicos por tipo de serviço
- **RN-053-03:** Validação obrigatória de campos antes de submeter
- **RN-053-04:** Aprovação gerencial obrigatória para todas as solicitações
- **RN-053-05:** Aprovação TI obrigatória para licenças e hardware
- **RN-053-06:** Aprovação financeira obrigatória para valores > R$5.000
- **RN-053-07:** Execução automatizada preferencial (onde aplicável)
- **RN-053-08:** Registro de evidências obrigatório (automático ou manual)
- **RN-053-09:** NPS enviado automaticamente após fechamento
- **RN-053-10:** Taxa de resposta NPS meta: 60%+
- **RN-053-11:** NPS médio meta: 8.0+

**[Ver regras completas em RF053.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Solicitações via e-mail (texto livre, não estruturado)
- ❌ Sem catálogo de serviços formal
- ❌ Técnico interpretava manualmente o que usuário queria
- ❌ Aprovações informais via e-mail
- ❌ Execução 100% manual (mesmo tarefas repetitivas)
- ❌ Sem evidências documentadas
- ❌ NPS manual (1x por ano, taxa de resposta 10%)
- ❌ Sem dashboard de satisfação

**Melhorias no moderno:**

- ✅ Solicitações estruturadas via catálogo de serviços
- ✅ Formulários dinâmicos específicos por tipo
- ✅ Validação automática de campos
- ✅ Aprovações formais rastreadas via workflow (RF088)
- ✅ Execução automatizada para casos simples (60% dos casos)
- ✅ Evidências registradas automaticamente
- ✅ NPS automático pós-atendimento (taxa de resposta 60%+)
- ✅ Dashboard de satisfação em tempo real
- ✅ Redução de 40% no tempo de atendimento

---

### 3.6 PRO-SVC-006: Escalação Automática

**Código:** PRO-SVC-006
**RFs Envolvidos:** RF072
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Chamado atrasado] -->|Gerente vê manual| B[Decide escalar]
    B -->|Liga para técnico| C[Pressiona resolução]
    C -->|Sem critério| D[Escalação inconsistente]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire a cada 5min] -->|Verifica regras| B{Condições Escalação}
    B -->|SLA 90%| C[Regra Tempo]
    B -->|P1 + 1h sem resposta| D[Regra Prioridade]
    B -->|Chamado reassignado 3x| E[Regra Complexidade]

    C --> F[Dispara Escalação]
    D --> F
    E --> F

    F -->|Consulta hierarquia| G{Próximo Nível}
    G -->|Nível 1| H[Técnico → Coordenador]
    G -->|Nível 2| I[Coordenador → Gerente]
    G -->|Nível 3| J[Gerente → Diretor]

    H --> K[Notifica novo responsável]
    I --> K
    J --> K

    K -->|E-mail + Push + SMS| L[Novo responsável]
    L -->|Assume ou reassigna| M[Ação tomada]

    N[Histórico Escalações] -->|Registra causa| O[(Banco Dados)]
    O -->|Análise causa raiz| P{Por que escalou?}
    P -->|SLA apertado| Q[Ajusta SLA]
    P -->|Falta skill| R[Treina técnico]
    P -->|Complexidade| S[Documenta solução]

    T[Dashboard] -->|Exibe métricas| U[Taxa escalação por técnico]
    T -->|Exibe métricas| V[Causa raiz mais comum]
    T -->|Exibe métricas| W[Tempo médio resolução pós-escalação]

    style B fill:#F39C12
    style F fill:#3498DB
    style G fill:#F39C12
    style P fill:#F39C12
    style T fill:#27AE60
```

#### Descrição do Processo

Sistema inteligente de escalação automática baseado em regras configuráveis (tempo, prioridade, complexidade). Implementa hierarquia de escalação (nível 1 → nível 2 → nível 3 → gestor), notificações automáticas multi-canal, histórico completo de escalações, e análise de causa raiz para melhoria contínua.

#### Atores

- **Job Hangfire:** Monitora condições de escalação a cada 5 minutos
- **Sistema de Escalação:** Aplica regras e determina próximo nível
- **Técnico Nível 1:** Primeiro atendimento
- **Coordenador (Nível 2):** Casos complexos ou SLA próximo
- **Gerente (Nível 3):** Casos críticos ou múltiplas tentativas
- **Diretor:** Casos críticos sem resolução em nível 3

#### Fluxo Principal

1. **Monitoramento Contínuo:**
   - Job Hangfire executa a cada 5 minutos
   - Consulta chamados ativos com status "Em Atendimento"
   - Aplica regras de escalação configuradas
2. **Regras de Escalação (configuráveis por tipo e prioridade):**
   - **Regra Tempo:**
     - SLA atingiu 90%+ → Escala para nível superior
   - **Regra Prioridade:**
     - P1 + 1 hora sem primeira resposta → Escala para sênior
     - P1 + 2 horas sem resolução → Escala para coordenador
   - **Regra Complexidade:**
     - Chamado reassignado 3+ vezes → Escala para especialista
     - Chamado reaberto 2+ vezes → Escala para coordenador
   - **Regra Inatividade:**
     - Sem atualização há 4 horas (P1/P2) → Escala para coordenador
3. **Determinação de Hierarquia:**
   - Sistema consulta estrutura organizacional (Azure AD)
   - Identifica próximo nível:
     - **Nível 1 (Técnico):** Primeiro atendimento
     - **Nível 2 (Coordenador):** Supervisão técnica
     - **Nível 3 (Gerente):** Casos complexos
     - **Nível 4 (Diretor):** Crises críticas
4. **Disparo de Escalação:**
   - Sistema marca chamado como "Escalado"
   - Registra:
     - Timestamp de escalação
     - Regra que disparou
     - Técnico anterior
     - Novo responsável
     - Observações automáticas
5. **Notificação Multi-Canal:**
   - **Novo responsável:** E-mail + Push + SMS (P1)
   - **Técnico anterior:** E-mail + Push (informativo)
   - **Gestor:** E-mail (informativo) + Dashboard atualizado
6. **Ação do Novo Responsável:**
   - **Assumir:** Torna-se responsável direto
   - **Reassignar:** Atribui a especialista específico
   - **Resolver:** Resolve diretamente
   - **Solicitar apoio:** Consulta outros técnicos sem reassignar
7. **Análise de Causa Raiz:**
   - Sistema agrega escalações por:
     - Técnico (quem escala mais?)
     - Tipo de chamado (qual categoria escala mais?)
     - Regra (tempo, complexidade, inatividade?)
   - Dashboard exibe:
     - Taxa de escalação por técnico
     - Causa raiz mais comum
     - Tempo médio de resolução pós-escalação
8. **Melhoria Contínua:**
   - **SLA apertado demais:** Gestor ajusta prazos
   - **Falta de skill:** Treina técnico em categoria específica
   - **Complexidade recorrente:** Documenta solução na base de conhecimento

#### Automações

- ✅ Monitoramento contínuo a cada 5 minutos via Hangfire
- ✅ Aplicação automática de regras de escalação
- ✅ Determinação automática de próximo nível via hierarquia AD
- ✅ Notificações automáticas multi-canal (e-mail, push, SMS)
- ✅ Registro automático de histórico de escalações
- ✅ Análise automática de causa raiz
- ✅ Dashboard de métricas em tempo real
- ✅ Sugestão automática de melhorias (ajustar SLA, treinar técnico)

#### Integrações

- **Hangfire:** Jobs de monitoramento a cada 5 minutos
- **Azure AD:** Hierarquia organizacional para determinar níveis
- **RF028 (SLA Operações):** Consulta percentual de SLA consumido
- **RF066 (Notificações):** Alertas multi-canal
- **RF033 (Gestão Chamados):** Dados de chamados e reassignments
- **SignalR:** Dashboard de escalações em tempo real
- **RF004 (Auditoria):** Histórico imutável de escalações

#### Regras de Negócio Principais

- **RN-072-01:** Monitoramento de regras a cada 5 minutos
- **RN-072-02:** Regras configuráveis por tipo e prioridade de chamado
- **RN-072-03:** Hierarquia: Técnico → Coordenador → Gerente → Diretor
- **RN-072-04:** Regra Tempo: escala em 90% do SLA
- **RN-072-05:** Regra Prioridade P1: escala após 1h sem resposta
- **RN-072-06:** Regra Complexidade: escala após 3 reassignments
- **RN-072-07:** Regra Inatividade: escala após 4h sem atualização (P1/P2)
- **RN-072-08:** Notificação SMS apenas para P1
- **RN-072-09:** Histórico de escalações mantido por 2 anos
- **RN-072-10:** Taxa de escalação meta: <15% dos chamados
- **RN-072-11:** Análise de causa raiz executada semanalmente

**[Ver regras completas em RF072.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Escalação manual pelo gerente (quando lembrava)
- ❌ Sem regras formais (decisão subjetiva)
- ❌ Sem notificação automática (ligação telefônica)
- ❌ Sem histórico estruturado de escalações
- ❌ Sem análise de causa raiz
- ❌ Escalação inconsistente (depende de quem grita mais)
- ❌ Sem métricas de escalação

**Melhorias no moderno:**

- ✅ Escalação automática baseada em regras configuráveis
- ✅ Monitoramento contínuo a cada 5 minutos
- ✅ Notificações automáticas multi-canal (e-mail, push, SMS)
- ✅ Histórico completo de escalações (auditável)
- ✅ Análise automática de causa raiz
- ✅ Escalação consistente e objetiva (baseada em critérios)
- ✅ Dashboard de métricas em tempo real
- ✅ Melhoria contínua baseada em dados (ajuste SLA, treinamento)

---

### 3.7 PRO-SVC-007: Integração com ERPs

**Código:** PRO-SVC-007
**RFs Envolvidos:** RF078
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[DBA] -->|SQL direto| B[(Banco ERP)]
    B -->|Job noturno| C[Script SQL agendado]
    C -->|INSERT manual| D[(IControlIT)]
    D -->|Falha silenciosa| E[Dados desatualizados]

    style A fill:#E74C3C
    style C fill:#E74C3C
    style E fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Job Hangfire a cada 15min] -->|Sincroniza| B[Integration Service]
    B -->|TOTVS| C[WebService Protheus]
    B -->|SAP| D[RFC/BAPI]
    B -->|Oracle| E[REST API EBS]

    C -->|Consulta entidades| F{Mapeamento}
    D -->|Consulta entidades| F
    E -->|Consulta entidades| F

    F -->|Cliente| G[Sincroniza cadastro]
    F -->|Fornecedor| H[Sincroniza cadastro]
    F -->|Ativo| I[Sincroniza inventário]
    F -->|Centro Custo| J[Sincroniza estrutura]

    G --> K[Reconciliação Dados]
    H --> K
    I --> K
    J --> K

    K -->|Conflito detectado| L{Estratégia}
    L -->|ERP wins| M[Atualiza IControlIT]
    L -->|IControlIT wins| N[Atualiza ERP]
    L -->|Manual| O[Alerta admin para decisão]

    M --> P[Registra log integração]
    N --> P
    O --> P

    P --> Q[(Log Integração DB)]
    Q -->|Retry automático| R{Falha API?}
    R -->|Sim| S[Re-enfileira job]
    R -->|Não| T[Dashboard sincronização]

    style B fill:#3498DB
    style F fill:#F39C12
    style K fill:#3498DB
    style L fill:#F39C12
    style T fill:#27AE60
```

#### Descrição do Processo

Integração bidirecional com ERPs corporativos (TOTVS Protheus, SAP Business One, Oracle EBS) via WebServices e APIs REST. Implementa sincronização automática a cada 15 minutos de entidades-chave (cliente, fornecedor, ativo, centro de custo), reconciliação automática de dados divergentes, logs detalhados de integração, e retry automático em falhas.

#### Atores

- **Integration Service:** Orquestra sincronização bidirecional
- **Job Hangfire:** Executa sincronizações a cada 15 minutos
- **ERP TOTVS Protheus:** Sistema financeiro/contábil corporativo
- **ERP SAP Business One:** Sistema de gestão empresarial
- **ERP Oracle EBS:** Sistema de gestão empresarial
- **Administrador:** Resolve conflitos de dados manualmente (quando necessário)

#### Fluxo Principal

1. **Agendamento de Sincronização:**
   - Job Hangfire executa a cada 15 minutos
   - Consulta configuração de integração ativa:
     - ERP conectado (TOTVS, SAP ou Oracle)
     - Entidades habilitadas para sincronização
     - Direção (IControlIT → ERP, ERP → IControlIT ou bidirecional)
2. **Conexão com ERP:**
   - **TOTVS Protheus:** WebService SOAP (.wsdl)
   - **SAP Business One:** RFC/BAPI (Remote Function Call)
   - **Oracle EBS:** REST API (JSON)
   - Autenticação via credenciais configuradas (RF002)
   - Timeout: 30 segundos
3. **Sincronização de Entidades:**
   - **Cliente:**
     - Campos: CNPJ, Razão Social, Nome Fantasia, Endereço, Status
     - IControlIT → ERP: Novos clientes cadastrados
     - ERP → IControlIT: Alterações de status, endereço
   - **Fornecedor:**
     - Campos: CNPJ, Razão Social, Categoria, Contato
     - Sincronização bidirecional
   - **Ativo:**
     - Campos: Patrimônio, Descrição, Centro Custo, Status
     - ERP → IControlIT: Ativos comprados via ordem de compra
     - IControlIT → ERP: Baixa de ativos, depreciação
   - **Centro de Custo:**
     - Campos: Código, Descrição, Hierarquia
     - ERP → IControlIT (apenas leitura)
4. **Mapeamento de Campos:**
   - Sistema mantém tabela de mapeamento configurável:
     - Campo IControlIT → Campo ERP
     - Exemplo: `ClienteId` (IControlIT) → `A1_COD` (TOTVS)
   - Suporta transformações customizadas (ex: CNPJ com/sem máscara)
5. **Reconciliação de Dados:**
   - Para cada registro:
     - Compara campos IControlIT vs ERP
     - Se idênticos: nenhuma ação
     - Se divergentes: detecta conflito
6. **Resolução de Conflitos:**
   - **Estratégia "ERP wins":** ERP é fonte da verdade (padrão)
     - Atualiza registro no IControlIT com valores do ERP
   - **Estratégia "IControlIT wins":** IControlIT é fonte da verdade
     - Atualiza registro no ERP com valores do IControlIT
   - **Estratégia "Manual":** Conflitos complexos
     - Alerta administrador via notificação
     - Admin decide qual valor manter
7. **Logs de Integração:**
   - Cada sincronização gera log detalhado:
     - Timestamp início/fim
     - Entidades sincronizadas
     - Registros processados
     - Conflitos detectados
     - Erros (se houver)
   - Logs mantidos por 90 dias
8. **Retry Automático em Falhas:**
   - Se API falha (timeout, erro HTTP 500):
     - Sistema registra erro no log
     - Re-enfileira job com backoff exponencial (1min, 5min, 15min)
     - Máximo 3 tentativas
     - Se falha 3x: alerta administrador
9. **Dashboard de Sincronização:**
   - Última sincronização: timestamp
   - Status: Sucesso, Falha, Parcial
   - Registros processados: total, novos, atualizados
   - Conflitos: total, resolvidos, pendentes
   - Taxa de sucesso: (sincronizações OK / total) × 100%

#### Automações

- ✅ Sincronização automática a cada 15 minutos via Hangfire
- ✅ Mapeamento automático de campos via tabela configurável
- ✅ Reconciliação automática de dados divergentes
- ✅ Resolução automática de conflitos (estratégia "ERP wins")
- ✅ Retry automático com backoff exponencial em falhas
- ✅ Logs detalhados de todas as operações
- ✅ Alertas automáticos em falhas persistentes
- ✅ Dashboard de sincronização em tempo real

#### Integrações

- **TOTVS Protheus:** WebService SOAP (WSCLIENTES, WSATIVOS)
- **SAP Business One:** RFC/BAPI (via SAP .NET Connector)
- **Oracle EBS:** REST API (JSON)
- **RF002 (Configurações Gerais):** Credenciais de conexão ERP
- **RF066 (Notificações):** Alertas de falhas de integração
- **Hangfire:** Jobs de sincronização
- **RF004 (Auditoria):** Histórico de sincronizações

#### Regras de Negócio Principais

- **RN-078-01:** Sincronização a cada 15 minutos (configurável)
- **RN-078-02:** Entidades sincronizadas: Cliente, Fornecedor, Ativo, Centro Custo
- **RN-078-03:** Mapeamento de campos configurável via UI
- **RN-078-04:** Estratégia padrão de conflito: "ERP wins"
- **RN-078-05:** Retry automático: 3 tentativas (1min, 5min, 15min)
- **RN-078-06:** Timeout de conexão: 30 segundos
- **RN-078-07:** Logs mantidos por 90 dias
- **RN-078-08:** Taxa de sucesso meta: 99%+
- **RN-078-09:** Alertas após 3 falhas consecutivas
- **RN-078-10:** Sincronização pode ser pausada manualmente

**[Ver regras completas em RF078.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Integração via scripts SQL diretos (frágil)
- ❌ Jobs noturnos (dados desatualizados durante o dia)
- ❌ Sem tratamento de erros (falhas silenciosas)
- ❌ Sem reconciliação de conflitos (dados inconsistentes)
- ❌ Sem logs estruturados (impossível debugar)
- ❌ Sem retry automático (DBA intervinha manualmente)
- ❌ Acoplamento direto ao banco ERP (risco de corrupção)

**Melhorias no moderno:**

- ✅ Integração via APIs REST e WebServices (oficial)
- ✅ Sincronização a cada 15 minutos (dados atualizados)
- ✅ Tratamento robusto de erros com retry
- ✅ Reconciliação automática de conflitos
- ✅ Logs detalhados de todas as operações
- ✅ Retry automático com backoff exponencial
- ✅ Desacoplamento via APIs (segurança ERP garantida)
- ✅ Dashboard de sincronização em tempo real
- ✅ Suporte multi-ERP (TOTVS, SAP, Oracle)

---

### 3.8 PRO-SVC-008: APIs Externas

**Código:** PRO-SVC-008
**RFs Envolvidos:** RF087
**Área:** Service Desk
**Criticidade:** Alta

#### Diagrama BPMN: Comparação Legado vs Moderno

**Legado (AS-IS):**

```mermaid
graph LR
    A[Sistema Externo] -->|Acesso direto SQL| B[(Banco Dados)]
    B -->|Sem autenticação| C[Leitura/Escrita livre]
    C -->|Risco segurança| D[Dados corrompidos]

    style A fill:#E74C3C
    style B fill:#E74C3C
    style C fill:#E74C3C
    style D fill:#E74C3C
```

**Moderno (Modernizado):**

```mermaid
graph TB
    A[Sistema Externo] -->|HTTPS| B[API Gateway]
    B -->|Valida auth| C{Autenticação}
    C -->|API Key| D[Bearer Token]
    C -->|OAuth 2.0| E[Client Credentials Flow]

    D --> F{Rate Limiting}
    E --> F

    F -->|100 req/min| G[Aceita request]
    F -->|Excedeu| H[HTTP 429 Too Many Requests]

    G -->|Rota para| I{Endpoint}
    I -->|GET /chamados| J[Lista Chamados]
    I -->|POST /chamados| K[Cria Chamado]
    I -->|PUT /chamados/:id| L[Atualiza Chamado]
    I -->|GET /clientes| M[Lista Clientes]

    J --> N[ChamadosController]
    K --> N
    L --> N

    N -->|CQRS| O[Command/Query Handler]
    O -->|Valida| P[FluentValidation]
    P -->|OK| Q[Executa operação]
    Q --> R[(SQL Server)]

    R --> S[Response JSON]
    S --> T[API Gateway]
    T -->|HTTPS| A

    U[Webhook] -->|Chamado criado| V[POST para URL externa]
    U -->|Chamado atualizado| V
    U -->|Chamado fechado| V

    W[Swagger/OpenAPI] -->|Documentação| X[Portal Desenvolvedor]
    X -->|Testa endpoints| Y[Sandbox Environment]

    Z[Logs API] -->|Registra| AA[(Log DB)]
    AA -->|Auditoria| AB[Dashboard Uso API]

    style B fill:#3498DB
    style C fill:#F39C12
    style F fill:#F39C12
    style I fill:#F39C12
    style W fill:#27AE60
    style AB fill:#27AE60
```

#### Descrição do Processo

Exposição de APIs REST securizadas para integrações externas com autenticação via API Key ou OAuth 2.0, rate limiting (100 req/min por tenant), throttling automático em picos, webhooks para notificações de eventos (chamado criado, atualizado, fechado), documentação Swagger/OpenAPI interativa, e logs completos de uso para auditoria.

#### Atores

- **Sistema Externo:** Consome APIs do IControlIT
- **API Gateway:** Gerencia autenticação, rate limiting e roteamento
- **ChamadosController:** Expõe endpoints de chamados
- **Webhook Service:** Notifica sistemas externos de eventos
- **Desenvolvedor Externo:** Consome APIs e lê documentação
- **Administrador IControlIT:** Gerencia API Keys e monitora uso

#### Fluxo Principal

1. **Registro de Aplicação Externa:**
   - Desenvolvedor acessa portal IControlIT
   - Solicita acesso à API
   - Admin aprova solicitação
   - Sistema gera:
     - **API Key:** Token opaco para autenticação simples
     - **Client ID/Secret:** Para OAuth 2.0 (mais seguro)
2. **Autenticação:**
   - **API Key (simples):**
     - Header: `Authorization: Bearer {API_KEY}`
     - Válido por 1 ano (renovável)
   - **OAuth 2.0 (recomendado):**
     - POST `/api/auth/token` com Client ID/Secret
     - Retorna Access Token JWT (válido por 1 hora)
     - Header: `Authorization: Bearer {ACCESS_TOKEN}`
3. **Rate Limiting:**
   - Sistema aplica limites por tenant:
     - **Padrão:** 100 requisições/minuto
     - **Premium:** 500 requisições/minuto
   - Se excedido: retorna HTTP 429 Too Many Requests
   - Header `Retry-After: 60` indica quando pode tentar novamente
4. **Throttling Automático:**
   - Em picos de tráfego (ex: 1000 req/s):
     - Sistema enfileira requisições
     - Processa de forma controlada (FIFO)
     - Retorna HTTP 503 Service Unavailable se fila cheia
5. **Endpoints Disponíveis:**
   - **Chamados:**
     - `GET /api/v1/chamados` - Lista chamados (paginado)
     - `GET /api/v1/chamados/:id` - Detalhe de chamado
     - `POST /api/v1/chamados` - Cria novo chamado
     - `PUT /api/v1/chamados/:id` - Atualiza chamado
     - `DELETE /api/v1/chamados/:id` - Cancela chamado
   - **Clientes:**
     - `GET /api/v1/clientes` - Lista clientes
     - `GET /api/v1/clientes/:id` - Detalhe de cliente
   - **Ativos:**
     - `GET /api/v1/ativos` - Lista ativos
     - `GET /api/v1/ativos/:id` - Detalhe de ativo
6. **Validação de Request:**
   - FluentValidation valida payload
   - Retorna HTTP 400 Bad Request com erros detalhados:
     ```json
     {
       "errors": {
         "titulo": ["Campo obrigatório"],
         "descricao": ["Mínimo 10 caracteres"]
       }
     }
     ```
7. **Execução de Operação:**
   - Controller delega para Command/Query Handler (CQRS)
   - Handler executa lógica de negócio
   - Retorna resultado
8. **Response:**
   - HTTP 200 OK: operação bem-sucedida
   - HTTP 201 Created: recurso criado (com header `Location`)
   - HTTP 400 Bad Request: validação falhou
   - HTTP 401 Unauthorized: autenticação inválida
   - HTTP 403 Forbidden: sem permissão
   - HTTP 404 Not Found: recurso não existe
   - HTTP 429 Too Many Requests: rate limit excedido
   - HTTP 500 Internal Server Error: erro no servidor
9. **Webhooks:**
   - Sistema externo registra URL de callback
   - Eventos suportados:
     - `chamado.criado`
     - `chamado.atualizado`
     - `chamado.fechado`
   - Sistema envia POST para URL registrada:
     ```json
     {
       "evento": "chamado.criado",
       "timestamp": "2026-01-12T10:30:00Z",
       "data": {
         "chamadoId": "123",
         "titulo": "Erro no sistema",
         "prioridade": "P1"
       }
     }
     ```
   - Retry automático se callback falhar (3 tentativas)
10. **Documentação Swagger/OpenAPI:**
    - Portal desenvolvedor: `https://api.icontrolit.com.br/docs`
    - Documentação interativa de todos os endpoints
    - Permite testar requisições diretamente na UI
    - Sandbox environment para testes
11. **Logs e Auditoria:**
    - Toda requisição gera log detalhado:
      - Timestamp, ClienteId, API Key/Token
      - Endpoint, Method, Payload
      - Response status, duração (ms)
    - Dashboard de uso:
      - Requisições por minuto
      - Taxa de erro
      - Endpoints mais usados
      - Latência (p50, p95, p99)

#### Automações

- ✅ Autenticação automática via API Key ou OAuth 2.0
- ✅ Rate limiting automático (100 req/min padrão)
- ✅ Throttling automático em picos de tráfego
- ✅ Validação automática de payloads via FluentValidation
- ✅ Webhooks automáticos para eventos configurados
- ✅ Retry automático de webhooks em falhas (3 tentativas)
- ✅ Geração automática de documentação Swagger/OpenAPI
- ✅ Logs automáticos de todas as requisições
- ✅ Dashboard de uso em tempo real

#### Integrações

- **API Gateway (ASP.NET Core):** Roteamento e autenticação
- **OAuth 2.0 / OpenID Connect:** Autenticação segura
- **FluentValidation:** Validação de payloads
- **Hangfire:** Processamento assíncrono de webhooks
- **Swagger/Swashbuckle:** Geração de documentação OpenAPI
- **RF004 (Auditoria):** Logs imutáveis de requisições
- **Application Insights:** Métricas de performance
- **Redis:** Cache de API Keys e rate limiting

#### Regras de Negócio Principais

- **RN-087-01:** Autenticação obrigatória (API Key ou OAuth 2.0)
- **RN-087-02:** Rate limiting padrão: 100 req/min por tenant
- **RN-087-03:** Rate limiting premium: 500 req/min por tenant
- **RN-087-04:** Throttling automático em picos (fila FIFO)
- **RN-087-05:** API Key válido por 1 ano (renovável)
- **RN-087-06:** Access Token OAuth 2.0 válido por 1 hora
- **RN-087-07:** Webhooks com retry automático (3 tentativas: 1min, 5min, 15min)
- **RN-087-08:** Documentação Swagger/OpenAPI sempre atualizada
- **RN-087-09:** Logs mantidos por 90 dias
- **RN-087-10:** Sandbox environment para testes
- **RN-087-11:** Versionamento de API: `/api/v1/`, `/api/v2/`

**[Ver regras completas em RF087.md]**

#### Referência ao Legado

**Como funcionava no legado:**

- ❌ Integração via acesso direto ao banco SQL (perigoso)
- ❌ Sem autenticação (qualquer um podia acessar)
- ❌ Sem rate limiting (DDoS possível)
- ❌ Sem throttling (crashes em picos de tráfego)
- ❌ Sem validação de payloads (dados inválidos no banco)
- ❌ Sem webhooks (polling constante necessário)
- ❌ Sem documentação formal
- ❌ Sem logs de uso
- ❌ Sem auditoria de acessos

**Melhorias no moderno:**

- ✅ APIs REST securizadas (sem acesso direto ao banco)
- ✅ Autenticação robusta (API Key ou OAuth 2.0)
- ✅ Rate limiting configurável por tenant
- ✅ Throttling automático (resiliência em picos)
- ✅ Validação rigorosa de payloads (integridade de dados)
- ✅ Webhooks para notificações em tempo real (sem polling)
- ✅ Documentação Swagger/OpenAPI interativa
- ✅ Logs completos de uso (auditoria LGPD)
- ✅ Dashboard de uso em tempo real
- ✅ Sandbox para testes
- ✅ Versionamento de API (backward compatibility)

---

## 4. Matriz de Processos

| Código | Processo | RF | Criticidade | Automação | Integrações |
|--------|----------|----|-----------|-----------| ------------|
| **PRO-SVC-001** | SLA de Operações | RF028 | Alta | ✅ Cálculo tempo útil, alertas, escalação | Hangfire, API Calendário, RF066, RF072 |
| **PRO-SVC-002** | SLA de Serviços | RF029 | Alta | ✅ TFR/TTR, pausas automáticas, breach | RF028, RF066, RF072, Hangfire |
| **PRO-SVC-003** | Gestão de Chamados | RF033 | Alta | ✅ Triagem ML, base conhecimento, NPS | Azure Cognitive, RF028, RF066, SignalR |
| **PRO-SVC-004** | SLA de Solicitações | RF038 | Alta | ✅ SLA por tipo, aprovação multi-nível | RF053, RF088, RF028, Hangfire |
| **PRO-SVC-005** | Gestão de Solicitações | RF053 | Alta | ✅ Catálogo, formulários, execução auto | RF088, RF038, AD, Office 365, RF078 |
| **PRO-SVC-006** | Escalação Automática | RF072 | Alta | ✅ Regras, hierarquia AD, causa raiz | Hangfire, Azure AD, RF028, RF066 |
| **PRO-SVC-007** | Integração com ERPs | RF078 | Alta | ✅ Sincronização bidirecional, retry | TOTVS, SAP, Oracle, Hangfire, RF002 |
| **PRO-SVC-008** | APIs Externas | RF087 | Alta | ✅ OAuth 2.0, rate limiting, webhooks | API Gateway, Swagger, Redis, RF004 |

---

## 5. Glossário

| Termo | Definição |
|-------|-----------|
| **API Gateway** | Ponto de entrada único para APIs, gerencia autenticação e rate limiting |
| **API Key** | Token opaco para autenticação simples de APIs |
| **Auto-resolução** | Cliente resolve chamado sozinho via base de conhecimento (economia) |
| **Breach** | Violação de SLA (prazo não cumprido) |
| **Client ID/Secret** | Credenciais para OAuth 2.0 Client Credentials Flow |
| **Escalação** | Transferência de chamado para nível superior (coordenador, gerente) |
| **Matriz Impacto × Urgência** | Ferramenta de priorização: quantos afetados × quanto tempo pode esperar |
| **NPS (Net Promoter Score)** | Pesquisa de satisfação: "Recomendaria nosso serviço?" (0-10) |
| **OAuth 2.0** | Padrão de autenticação/autorização para APIs |
| **OpenAPI** | Especificação de documentação de APIs (antigamente Swagger) |
| **P1, P2, P3, P4** | Prioridades: Crítico, Alto, Médio, Baixo |
| **Rate Limiting** | Limitação de requisições por período (ex: 100/min) |
| **RFC/BAPI** | Remote Function Call / Business API (SAP) |
| **SLA (Service Level Agreement)** | Acordo de nível de serviço (prazo máximo) |
| **Swagger** | Ferramenta de documentação interativa de APIs |
| **Tempo Útil** | Tempo de trabalho real (desconta fins de semana, feriados, pausas) |
| **TFR (Time to First Response)** | Tempo até primeira resposta do técnico |
| **Throttling** | Controle de taxa de processamento para evitar sobrecarga |
| **TTR (Time to Resolution)** | Tempo até resolução completa do chamado |
| **Webhook** | Callback HTTP para notificar sistema externo de evento |

---

## 6. Referências Cruzadas

### Jornadas Relacionadas

- **Jornada 1:** Infraestrutura e Configuração (PRO-INF-001 a PRO-INF-008)
- **Jornada 2:** Workflows e Importação (PRO-WKF-001 a PRO-WKF-009)
- **Jornada 3:** Financeiro Completo (PRO-FCT-001 a PRO-FAC-005)
- **Jornada 4:** Gestão de Ativos (a documentar)

### Documentos de Governança

| Documento | Caminho | Relevância |
|-----------|---------|-----------|
| **ARCHITECTURE.md** | `D:\IC2_Governanca\governanca\ARCHITECTURE.md` | Stack tecnológico, padrões arquiteturais |
| **CONVENTIONS.md** | `D:\IC2_Governanca\governanca\CONVENTIONS.md` | Nomenclatura de handlers, controllers, APIs |
| **COMPLIANCE.md** | `D:\IC2_Governanca\governanca\COMPLIANCE.md` | Regras de validação, auditoria e LGPD |
| **COMMANDS.md** | `D:\IC2_Governanca\governanca\COMMANDS.md` | Comandos de desenvolvimento e validação |

### RFs Relacionados

| RF | Título | Status |
|----|--------|--------|
| **RF028** | SLA de Operações | ✅ Implementado |
| **RF029** | SLA de Serviços | ✅ Implementado |
| **RF033** | Gestão de Chamados | ✅ Implementado |
| **RF038** | SLA de Solicitações | ✅ Implementado |
| **RF053** | Gestão de Solicitações | ✅ Implementado |
| **RF072** | Escalação Automática | ✅ Implementado |
| **RF078** | Integração com ERPs | ✅ Implementado |
| **RF087** | APIs Externas | ✅ Implementado |

### Contratos de Execução

Para implementar ou manter processos desta jornada, consulte:

- **Backend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\backend-criacao.md`
- **Frontend:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\frontend-criacao.md`
- **Manutenção:** `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\manutencao\CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md`
- **Auditoria:** `D:\IC2_Governanca\governanca\contracts\auditoria\conformidade.md`

---

## Controle de Versão

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-01-12 | ALC | Criação inicial com 8 processos da Jornada 5 |

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 1.0


---

# PARTE 6: JORNADA 5 - AUDITORIA E INTEGRAÇÕES

---


**Autor:** ALC (alc.dev.br)
**Data:** 2026-01-12
**Versão:** 1.0
**Status:** Vigente

---

## 1. Visão Geral da Jornada

A **Jornada 6: Auditoria e Integrações** representa a camada de controle e conformidade do IControlIT, garantindo que os dados do sistema reflitam a realidade física da operação de TI. Diferente das jornadas anteriores, esta é a menor jornada em número de processos (apenas 1 processo), mas de criticidade máxima para conformidade regulatória e auditoria externa.

### 1.1. Objetivo da Jornada

Estabelecer mecanismos de auditoria física de ativos com automação completa do ciclo de inventário: agendamento, contagem, conciliação, resolução de divergências e geração de relatórios de conformidade.

### 1.2. Escopo da Jornada

Esta jornada abrange exclusivamente o processo de **Inventário Cíclico**, que inclui:

- Agendamento automático de contagens periódicas
- Contagem física com tecnologias modernas (QR Code, RFID)
- Conciliação automática entre inventário lógico (sistema) e físico (real)
- Detecção e classificação de divergências
- Workflow de resolução de não-conformidades
- Geração de relatórios gerenciais e de conformidade
- Integração com processos de gestão de ativos, chamados e auditoria de operações

### 1.3. Criticidade

**Alta Criticidade:** A Jornada de Auditoria é fundamental para:

- **Conformidade SOX (Sarbanes-Oxley):** Controle de ativos de TI para empresas de capital aberto
- **Conformidade ISO 27001:** Gestão de segurança da informação (inventário de ativos críticos)
- **LGPD:** Rastreamento de dispositivos que processam dados pessoais
- **Auditoria Externa:** Evidências para auditorias contábeis e regulatórias
- **Governança Interna:** Transparência e controle sobre patrimônio de TI
- **Gestão de Riscos:** Detecção precoce de perdas, roubos ou desvios de ativos

### 1.4. Evolução do Modelo

**Legado:**
- Inventário anual massivo (2 semanas de trabalho manual)
- Planilhas Excel impressas com checkboxes manuais
- Conciliação manual demorada (3-5 dias)
- Sem rastreamento de responsáveis
- Taxa de conformidade: 65% (35% de divergências não resolvidas)
- Fechamento do inventário: 3 meses após contagem

**Moderno:**
- Inventário trimestral automatizado (1-2 dias de trabalho)
- App mobile com QR Code/RFID
- Conciliação automática em 15 minutos
- Rastreamento completo de ciclo de vida
- Taxa de conformidade: 95% (5% de divergências resolvidas rapidamente)
- Fechamento do inventário: 1 semana após contagem

### 1.5. Processos da Jornada

| Código | Nome do Processo | RF | Criticidade | Página |
|--------|------------------|-----|-------------|--------|
| **PRO-AUD-001** | Inventário Cíclico | RF068 | Alta | Seção 2 |

---

## 2. PRO-AUD-001: Inventário Cíclico

### 2.1. Identificação do Processo

- **Código:** PRO-AUD-001
- **Nome:** Inventário Cíclico
- **RF Envolvido:** RF068
- **Área:** Auditoria e Integrações
- **Criticidade:** Alta
- **Frequência de Execução:** Trimestral (configurável: mensal, semestral, anual)
- **Tempo Médio de Execução:** 1-2 dias (contagem) + 1 semana (resolução de divergências)
- **SLA Interno:** 7 dias para fechamento completo do inventário

### 2.2. Descrição do Processo

O **Inventário Cíclico** é o processo de auditoria física de ativos de TI com contagem periódica automática, conciliação entre inventário lógico (sistema) e físico (real), detecção de divergências e geração de relatórios de não-conformidades. É um processo crítico para conformidade regulatória, controle patrimonial e gestão de riscos.

### 2.3. Objetivo do Processo

- Garantir conformidade entre inventário lógico (sistema) e físico (real)
- Detectar ativos faltantes, sobrantes ou alocados incorretamente
- Manter taxa de conformidade acima de 95%
- Gerar evidências para auditorias externas (SOX, ISO 27001)
- Atualizar automaticamente localização e alocação de ativos
- Identificar padrões de perdas ou desvios

### 2.4. Diagrama BPMN

#### 2.4.1. Modelo Legado (AS-IS)

```mermaid
graph TD
    A[Planejamento Anual] -->|Manual| B[Impressão de Planilhas]
    B --> C[Distribuição para 4 Pessoas]
    C --> D[Contagem Manual com Prancheta]
    D -->|2 semanas| E[Coleta de Planilhas]
    E --> F[Digitação Manual no Excel]
    F -->|3-5 dias| G[Conciliação Manual]
    G --> H{Divergências?}
    H -->|Sim 35%| I[Investigação Manual]
    H -->|Não 65%| K[Relatório PDF]
    I -->|Sem Prazo| J[Ajuste Manual]
    J --> K
    K -->|3 meses| L[Inventário Fechado]

    style H fill:#ff9999
    style I fill:#ffcccc
    style L fill:#99ff99
```

**Problemas do Modelo Legado:**

1. **Frequência Inadequada:** Inventário anual (desvios não detectados por 12 meses)
2. **Intensivo em Mão de Obra:** 4 pessoas dedicadas por 2 semanas (320 horas)
3. **Propenso a Erros:** Digitação manual, planilhas perdidas, checkboxes ilegíveis
4. **Conciliação Lenta:** 3-5 dias para processar 2000+ ativos manualmente
5. **Baixa Taxa de Conformidade:** 65% (35% de divergências não investigadas)
6. **Sem Rastreamento:** Não sabe quem contou, quando contou, onde estava
7. **Fechamento Demorado:** 3 meses entre contagem e relatório final
8. **Sem Integração:** Ajustes manuais no sistema de ativos (duplo trabalho)

#### 2.4.2. Modelo Moderno (TO-BE)

```mermaid
graph TD
    A[Job Hangfire Agendado] -->|Automático| B[Notificação aos Responsáveis]
    B --> C[Geração de QR Codes]
    C --> D[Contagem via App Mobile]
    D -->|RFID/QR Code| E[Sincronização em Tempo Real]
    E -->|15 min| F[Conciliação Automática]
    F --> G{Divergências?}
    G -->|Sim 5%| H[Classificação Automática]
    G -->|Não 95%| M[Relatório Gerencial]
    H --> I{Tipo?}
    I -->|Falta| J[Chamado Automático]
    I -->|Sobra| J
    I -->|Localização Errada| K[Ajuste Automático]
    I -->|Usuário Errado| K
    J --> L[Workflow de Investigação]
    K --> M
    L --> M
    M -->|1 semana| N[Inventário Fechado]

    style F fill:#99ccff
    style H fill:#ffcc99
    style N fill:#99ff99
```

**Melhorias do Modelo Moderno:**

1. **Automação Completa:** Job Hangfire agenda e notifica automaticamente
2. **Tecnologia Moderna:** QR Code e RFID (contagem 10x mais rápida)
3. **Sincronização em Tempo Real:** Dados validados durante a contagem
4. **Conciliação Instantânea:** 15 minutos para processar 2000+ ativos
5. **Alta Taxa de Conformidade:** 95% (5% de divergências rapidamente resolvidas)
6. **Rastreamento Completo:** Quem, quando, onde, como para cada contagem
7. **Fechamento Rápido:** 1 semana entre contagem e relatório final
8. **Integração Nativa:** Ajustes automáticos no sistema de ativos

### 2.5. Atores Envolvidos

| Ator | Papel | Responsabilidades |
|------|-------|-------------------|
| **Job Hangfire** | Sistema | Agendar inventários, disparar notificações, executar conciliação |
| **Gestor de TI** | Responsável | Planejar cronograma, revisar relatórios, aprovar ajustes críticos |
| **Analista de Inventário** | Executor | Realizar contagens, investigar divergências, resolver não-conformidades |
| **Facilities** | Executor | Contar ativos em áreas físicas (CPD, salas, almoxarifado) |
| **Usuário Final** | Colaborador | Confirmar posse de ativos em home office |
| **Sistema de Ativos** | Sistema | Fornecer inventário lógico, receber ajustes automáticos |
| **Sistema de Chamados** | Sistema | Receber abertura automática de chamados para investigação |
| **Auditor Externo** | Stakeholder | Revisar relatórios de conformidade para auditoria (SOX, ISO) |

### 2.6. Fluxo Principal

#### Etapa 1: Agendamento Automático

**Descrição:**
O Job Hangfire executa diariamente às 8h e verifica se há inventários agendados para iniciar. Quando detecta um inventário devido (trimestral, semestral, anual), dispara o processo automaticamente.

**Entradas:**
- Cronograma de inventários (configurado pelo Gestor de TI)
- Localizações a serem inventariadas (matriz, filiais, home office)
- Lista de ativos ativos (não descartados)

**Ações:**
1. Job verifica agenda de inventários
2. Identifica localizações devido para contagem
3. Gera lista de ativos esperados por localização
4. Cria QR Codes para ativos sem código (novos, transferidos)
5. Envia notificação por e-mail aos responsáveis

**Saídas:**
- Inventário criado no sistema (status: Agendado)
- QR Codes gerados e prontos para impressão
- Notificações enviadas (Gestor de TI, Analistas, Facilities)

**Automações:**
- Disparo automático baseado em cronograma
- Geração automática de QR Codes
- Notificação automática por e-mail

**RN Aplicáveis:**
- RN-AUD-001: Inventário trimestral obrigatório para ativos críticos
- RN-AUD-002: Inventário semestral obrigatório para ativos comuns

---

#### Etapa 2: Contagem Física

**Descrição:**
Analistas e equipe de Facilities realizam contagem física de ativos utilizando app mobile. A contagem pode ser feita por leitura de QR Code (modo individual) ou RFID (modo massivo para centenas de ativos).

**Entradas:**
- Lista de ativos esperados (inventário lógico)
- QR Codes impressos (adesivos nos ativos)
- App mobile instalado (Android, iOS)
- Leitor RFID portátil (opcional, para contagens massivas)

**Ações:**
1. Analista acessa app mobile e seleciona inventário
2. Escaneia QR Code do ativo (ou lê tag RFID)
3. Sistema valida:
   - Ativo existe no sistema?
   - Localização corresponde ao esperado?
   - Usuário corresponde ao esperado?
4. Analista confirma ou corrige informações (localização, usuário)
5. Sistema registra contagem com timestamp e GPS

**Saídas:**
- Ativos contados (status: Encontrado)
- Localização e usuário confirmados ou corrigidos
- Registro de contagem (quem, quando, onde, coordenadas GPS)

**Automações:**
- Validação em tempo real (ativo existe?)
- Detecção automática de divergências (localização/usuário errado)
- Modo offline (sincronização posterior quando sem conexão)

**RN Aplicáveis:**
- RN-AUD-003: Contagem obrigatória com identificação do contador
- RN-AUD-004: GPS obrigatório para contagens em campo (home office, filiais)

---

#### Etapa 3: Conciliação Automática

**Descrição:**
Após conclusão da contagem física, o sistema executa conciliação automática entre inventário lógico (esperado) e físico (encontrado), identificando 4 tipos de divergências.

**Entradas:**
- Inventário lógico (ativos esperados no sistema)
- Inventário físico (ativos contados)

**Ações:**
1. Sistema compara inventário lógico vs físico
2. Classifica ativos em:
   - **Conformes:** Encontrados na localização e usuário corretos
   - **Falta:** No sistema mas não encontrados fisicamente
   - **Sobra:** Encontrados fisicamente mas não no sistema
   - **Localização Errada:** Encontrados mas em local diferente do sistema
   - **Usuário Errado:** Encontrados mas com usuário diferente do sistema
3. Calcula taxa de conformidade (% ativos conformes / total)
4. Gera relatório preliminar de divergências

**Saídas:**
- Taxa de conformidade (ex: 95%)
- Lista de divergências classificadas por tipo
- Relatório preliminar de não-conformidades

**Automações:**
- Matching automático por Patrimônio ou Serial Number
- Classificação automática de divergências
- Cálculo automático de taxa de conformidade

**RN Aplicáveis:**
- RN-AUD-005: Taxa de conformidade mínima: 90% (meta: 95%)
- RN-AUD-006: Divergências críticas (falta) abrem chamado automático

---

#### Etapa 4: Resolução de Divergências

**Descrição:**
Divergências são tratadas de forma diferenciada: divergências simples (localização/usuário errado) são corrigidas automaticamente após aprovação; divergências críticas (falta/sobra) disparam workflow de investigação.

**Entradas:**
- Lista de divergências classificadas
- Histórico de movimentações do ativo (últimos 6 meses)

**Ações:**

**Para Divergências Simples (Localização/Usuário Errado):**
1. Sistema identifica divergência como "simples"
2. Gera proposta de ajuste (atualizar localização/usuário no sistema)
3. Notifica Gestor de TI para aprovação
4. Após aprovação: atualiza automaticamente cadastro do ativo

**Para Divergências Críticas (Falta/Sobra):**
1. Sistema identifica divergência como "crítica"
2. Abre chamado automaticamente (categoria: Auditoria de Ativos)
3. Chamado atribuído ao Gestor de TI
4. Analista investiga causas raízes:
   - Roubo/furto?
   - Perda (extravio)?
   - Transferência não documentada?
   - Descarte não documentado?
   - Ativo emprestado (temporário)?
5. Analista registra conclusão no chamado
6. Gestor de TI aprova ação corretiva:
   - **Falta:** Baixa do ativo (após 3 inventários consecutivos sem localização)
   - **Sobra:** Cadastro do ativo (se for ativo legítimo não cadastrado)

**Saídas:**
- Divergências simples resolvidas (atualização automática)
- Chamados abertos para divergências críticas
- Investigações concluídas com causas raízes documentadas
- Ações corretivas aprovadas e executadas

**Automações:**
- Classificação automática de divergências (simples vs crítica)
- Abertura automática de chamados para divergências críticas
- Notificação automática ao Gestor de TI para aprovações
- Atualização automática de cadastro após aprovação

**RN Aplicáveis:**
- RN-AUD-007: Baixa de ativo somente após 3 inventários consecutivos sem localização
- RN-AUD-008: Divergências críticas exigem investigação formal com registro

---

#### Etapa 5: Geração de Relatórios

**Descrição:**
Após resolução de todas as divergências, o sistema gera relatórios gerenciais e de conformidade para auditorias externas. Os relatórios são disponibilizados em PDF, Excel e visualizações interativas (Power BI).

**Entradas:**
- Inventário conciliado (conformes + divergências resolvidas)
- Histórico de inventários anteriores (comparativo temporal)
- Chamados de investigação finalizados

**Ações:**
1. Sistema gera 5 tipos de relatório:

**A) Relatório de Conformidade Geral:**
   - Taxa de conformidade (%)
   - Total de ativos esperados vs encontrados
   - Distribuição de divergências por tipo
   - Comparativo com inventário anterior

**B) Top 10 Ativos Mais Perdidos:**
   - Ranking de ativos com maior histórico de divergências
   - Padrão de localização (onde costumam ser encontrados)
   - Recomendações de controle

**C) Mapa de Calor de Divergências:**
   - Visualização por localização (matriz, filiais, home office)
   - Identificação de locais com maior taxa de não-conformidade
   - Drill-down por sala, andar, prédio

**D) Relatório de Investigações:**
   - Lista de divergências críticas investigadas
   - Causas raízes identificadas
   - Ações corretivas tomadas
   - Responsáveis envolvidos

**E) Relatório de Conformidade Regulatória (SOX/ISO):**
   - Evidências para auditoria externa
   - Controles implementados
   - Rastreamento completo de ciclo de vida
   - Assinaturas digitais de aprovadores

**Saídas:**
- 5 relatórios gerados em PDF e Excel
- Dashboard interativo em Power BI
- Evidências para auditoria externa (pasta compactada)

**Automações:**
- Geração automática de todos os relatórios (1 clique)
- Exportação automática em múltiplos formatos (PDF, Excel, Power BI)
- Envio automático por e-mail aos stakeholders

**RN Aplicáveis:**
- RN-AUD-009: Relatórios gerenciais disponíveis em até 24h após fechamento
- RN-AUD-010: Relatórios de conformidade regulatória assinados digitalmente

---

#### Etapa 6: Fechamento do Inventário

**Descrição:**
Após geração de todos os relatórios e aprovação do Gestor de TI, o inventário é formalmente fechado. O sistema registra o fechamento, arquiva evidências e agenda o próximo inventário.

**Entradas:**
- Relatórios gerados
- Aprovação do Gestor de TI (assinatura digital)

**Ações:**
1. Gestor de TI revisa relatórios gerenciais
2. Valida resolução de todas as divergências críticas
3. Assina digitalmente o fechamento do inventário
4. Sistema registra:
   - Data/hora de fechamento
   - Assinatura digital do aprovador
   - Taxa de conformidade final
   - Total de divergências resolvidas
5. Sistema arquiva evidências (7 anos de retenção)
6. Sistema agenda próximo inventário (trimestral, semestral, anual)

**Saídas:**
- Inventário fechado oficialmente (status: Concluído)
- Evidências arquivadas (PDF assinado + anexos)
- Próximo inventário agendado automaticamente
- Notificação de conclusão enviada aos stakeholders

**Automações:**
- Assinatura digital com certificado A1/A3
- Arquivamento automático em storage seguro
- Agendamento automático do próximo inventário
- Notificação automática de conclusão

**RN Aplicáveis:**
- RN-AUD-011: Fechamento obrigatório pelo Gestor de TI (não pode ser analista)
- RN-AUD-012: Evidências retidas por 7 anos (compliance SOX)

---

### 2.7. Automações do Processo

| Código | Automação | Descrição | Tecnologia |
|--------|-----------|-----------|------------|
| **AUTO-AUD-001** | Agendamento Automático | Job Hangfire dispara inventários baseado em cronograma configurável | Hangfire + Cron Expression |
| **AUTO-AUD-002** | Geração de QR Codes | Criação automática de QR Codes para ativos sem código ou com código danificado | QRCoder (C#) |
| **AUTO-AUD-003** | Notificação de Início | E-mail automático aos responsáveis quando inventário é agendado | SendGrid |
| **AUTO-AUD-004** | Validação em Tempo Real | Validação durante contagem: ativo existe? Localização correta? Usuário correto? | API Backend + App Mobile |
| **AUTO-AUD-005** | Conciliação Automática | Matching automático inventário lógico vs físico em 15 minutos | SQL Server + LINQ |
| **AUTO-AUD-006** | Classificação de Divergências | Identificação automática de 4 tipos de divergências (falta, sobra, localização, usuário) | Algoritmo C# |
| **AUTO-AUD-007** | Abertura de Chamados | Chamado automático para divergências críticas (falta/sobra) | Integração PRO-SVC-003 |
| **AUTO-AUD-008** | Ajuste Automático | Atualização automática de localização/usuário após aprovação | Integração PRO-FAC-001 |
| **AUTO-AUD-009** | Geração de Relatórios | 5 relatórios gerenciais + dashboard Power BI em 1 clique | ReportGenerator + Power BI API |
| **AUTO-AUD-010** | Agendamento do Próximo | Agendamento automático do próximo inventário após fechamento | Hangfire |

### 2.8. Integrações com Outros Processos

| Processo Integrado | Direção | Dados Trocados | Finalidade |
|-------------------|---------|----------------|------------|
| **PRO-FAC-001** (Gestão de Ativos) | Bidirecional | Inventário lógico (entrada) + Ajustes de localização/usuário (saída) | Fornecer lista de ativos esperados e atualizar cadastro automaticamente após inventário |
| **PRO-SVC-003** (Gestão de Chamados) | Saída | Divergências críticas (falta/sobra) | Abertura automática de chamados para investigação de não-conformidades |
| **PRO-INF-004** (Auditoria de Operações) | Saída | Registro de todas as contagens, ajustes e aprovações | Rastreamento completo de quem, quando, onde, como para auditoria |
| **PRO-FAC-002** (Custos Fixos) | Saída | Ativos não localizados (baixa) | Impacto financeiro de ativos perdidos/roubados no cálculo de TCO |

### 2.9. Regras de Negócio Principais

| Código | Regra | Criticidade | Impacto se Violada |
|--------|-------|-------------|-------------------|
| **RN-AUD-001** | Inventário trimestral obrigatório para ativos críticos (servidores, storages, switches core) | Alta | Não-conformidade SOX/ISO 27001 |
| **RN-AUD-002** | Inventário semestral obrigatório para ativos comuns (notebooks, desktops, monitores) | Média | Perda de controle patrimonial |
| **RN-AUD-003** | Contagem obrigatória com identificação do contador (rastreamento de responsabilidade) | Alta | Falta de auditabilidade |
| **RN-AUD-004** | GPS obrigatório para contagens em campo (home office, filiais remotas) | Média | Impossibilidade de validar localização real |
| **RN-AUD-005** | Taxa de conformidade mínima: 90% (meta: 95%) | Alta | Indicador de processo de gestão de ativos falho |
| **RN-AUD-006** | Divergências críticas (falta) abrem chamado automático (não pode ser ignorada) | Alta | Perda de ativos não investigada |
| **RN-AUD-007** | Baixa de ativo somente após 3 inventários consecutivos sem localização | Alta | Baixa prematura de ativos temporariamente perdidos |
| **RN-AUD-008** | Divergências críticas exigem investigação formal com registro de causa raiz | Alta | Falta de aprendizado organizacional |
| **RN-AUD-009** | Relatórios gerenciais disponíveis em até 24h após fechamento do inventário | Média | Atraso na tomada de decisão |
| **RN-AUD-010** | Relatórios de conformidade regulatória assinados digitalmente pelo Gestor de TI | Alta | Evidências não aceitas em auditoria externa |
| **RN-AUD-011** | Fechamento obrigatório pelo Gestor de TI (não pode ser analista) | Alta | Falta de governança e segregação de funções |
| **RN-AUD-012** | Evidências retidas por 7 anos (compliance SOX) | Alta | Multas regulatórias em caso de auditoria |

### 2.10. Cenários de Exceção

#### Cenário 1: Ativo Não Localizado em 3 Inventários Consecutivos

**Situação:**
Ativo consta no sistema como ativo, mas não foi encontrado em 3 inventários consecutivos (9 meses para inventário trimestral).

**Ações:**
1. Sistema identifica padrão (3 inventários sem localização)
2. Sistema sugere baixa automática do ativo
3. Gestor de TI revisa histórico:
   - Último usuário responsável
   - Última localização conhecida
   - Movimentações nos últimos 12 meses
4. Gestor de TI decide:
   - **Baixa:** Se evidências indicam perda definitiva (roubo, extravio)
   - **Manter:** Se há indicação de recuperação (empréstimo, transferência não documentada)
5. Se baixa: Sistema registra motivo (perda, roubo, extravio) e atualiza contabilidade

**Impacto Contábil:**
- Baixa patrimonial
- Ajuste de depreciação acumulada
- Perda contábil (se não houver seguro)

---

#### Cenário 2: Sobra de Ativo (Encontrado mas Não Cadastrado)

**Situação:**
Ativo encontrado fisicamente durante inventário, mas não consta no sistema de ativos (sobra).

**Ações:**
1. Sistema identifica sobra durante conciliação
2. Abre chamado automático (categoria: Cadastro de Ativo Não Documentado)
3. Analista investiga:
   - Ativo é legítimo? (comprado pela empresa?)
   - Ativo é pessoal do usuário? (notebook particular?)
   - Ativo foi descartado mas voltou? (transferido de volta?)
4. Se legítimo: Analista cadastra ativo no sistema com dados coletados
5. Se pessoal: Registra como "Ativo Particular" (não gerenciado)
6. Se descartado voltou: Reativa cadastro original

---

#### Cenário 3: Localização Errada em Massa (Mudança de Layout)

**Situação:**
50+ ativos aparecem com localização errada durante inventário (indicação de mudança de layout não documentada).

**Ações:**
1. Sistema detecta padrão (múltiplos ativos do mesmo local antigo para mesmo local novo)
2. Gera alerta de "Possível Mudança de Layout Não Documentada"
3. Notifica Gestor de TI e Facilities
4. Gestor de TI confirma mudança de layout
5. Sistema oferece atualização em lote:
   - "Atualizar todos os ativos de Sala 201 para Sala 305?"
6. Após aprovação: Atualização em lote automática
7. Sistema registra evento de mudança de layout para histórico

---

#### Cenário 4: Inventário Interrompido (Falta de Pessoal)

**Situação:**
Inventário iniciado mas não concluído no prazo (falta de pessoal, priorização de outras tarefas).

**Ações:**
1. Sistema detecta inventário "Em Andamento" há mais de 7 dias
2. Envia alerta ao Gestor de TI (escalação)
3. Gestor de TI pode:
   - **Estender Prazo:** Adicionar 7 dias ao inventário
   - **Congelar:** Pausar inventário temporariamente
   - **Cancelar:** Cancelar inventário e reagendar
4. Se estendido: Sistema continua monitorando
5. Se congelado: Sistema para alertas até reativação
6. Se cancelado: Sistema agenda novo inventário automaticamente

---

#### Cenário 5: Divergência de Usuário (Ativo com Pessoa Errada)

**Situação:**
Ativo cadastrado para usuário A, mas encontrado fisicamente com usuário B durante inventário.

**Ações:**
1. Sistema identifica divergência de usuário
2. Classifica como divergência simples (não crítica)
3. Gera proposta de ajuste: "Transferir ativo de [Usuário A] para [Usuário B]?"
4. Notifica ambos os usuários por e-mail:
   - **Usuário A:** "Você ainda possui este ativo? Se não, confirme transferência"
   - **Usuário B:** "Você recebeu este ativo recentemente?"
5. Se ambos confirmam: Atualização automática
6. Se há conflito: Escala para Gestor de TI resolver manualmente

---

### 2.11. Comparativo Legado vs Moderno

| Aspecto | Legado | Moderno | Ganho |
|---------|--------|---------|-------|
| **Frequência** | Anual | Trimestral (configurável) | 4x mais frequente |
| **Mão de Obra** | 4 pessoas x 2 semanas (320h) | 2 pessoas x 2 dias (32h) | 90% redução |
| **Tecnologia** | Planilhas Excel + pranchetas | App mobile + QR Code/RFID | 10x mais rápido |
| **Conciliação** | Manual (3-5 dias) | Automática (15 min) | 99% redução |
| **Taxa de Conformidade** | 65% | 95% | +30 pontos percentuais |
| **Rastreamento** | Sem rastreamento | Completo (quem, quando, onde, GPS) | Auditabilidade total |
| **Fechamento** | 3 meses | 1 semana | 92% redução |
| **Relatórios** | PDF manual | 5 relatórios automáticos + Power BI | Decisões em tempo real |
| **Integração** | Sem integração | 4 processos integrados | Redução de duplo trabalho |
| **Erros** | 15-20% (digitação, planilhas perdidas) | <1% (validação em tempo real) | 95% redução |

### 2.12. Indicadores de Sucesso (KPIs)

Embora métricas não façam parte do escopo deste documento, os seguintes indicadores são monitorados para avaliação contínua do processo:

- Taxa de Conformidade Geral (meta: ≥ 95%)
- Tempo Médio de Fechamento (meta: ≤ 7 dias)
- Taxa de Divergências Críticas (meta: ≤ 5%)
- Taxa de Resolução de Divergências (meta: 100%)
- Tempo Médio de Contagem por Ativo (meta: ≤ 30 segundos)
- Taxa de Ativos com 3+ Inventários sem Localização (meta: 0%)

### 2.13. Dependências Tecnológicas

- **Backend:** API REST em .NET 6+ (handlers de inventário)
- **Frontend:** App mobile em Ionic/Angular (iOS + Android)
- **QR Code:** Biblioteca QRCoder (C#)
- **RFID:** SDK do fabricante de leitores RFID (ex: Zebra, Honeywell)
- **GPS:** Serviços de localização nativos (iOS, Android)
- **Job Scheduling:** Hangfire (agendamento de inventários)
- **Relatórios:** ReportGenerator + Power BI API
- **Storage:** Azure Blob Storage (armazenamento de evidências por 7 anos)
- **Assinatura Digital:** Certificado A1/A3 (ICP-Brasil)

### 2.14. Conformidade Regulatória

| Regulação | Requisito | Como o Processo Atende |
|-----------|-----------|------------------------|
| **SOX (Sarbanes-Oxley)** | Controle de ativos de TI para empresas de capital aberto | Inventários periódicos + rastreamento completo + evidências assinadas digitalmente |
| **ISO 27001** | Gestão de segurança da informação (inventário de ativos críticos) | Inventário trimestral de ativos críticos + classificação de divergências |
| **LGPD** | Rastreamento de dispositivos que processam dados pessoais | GPS obrigatório em contagens + registro de localização real |
| **NBC TG 27 (Contabilidade)** | Controle patrimonial de imobilizado | Baixa controlada após 3 inventários + impacto contábil automático |

---

## 3. Matriz de Processos da Jornada

| Código | Nome do Processo | RF | Criticidade | Frequência | Tempo Médio | Automações | Integrações |
|--------|------------------|-----|-------------|------------|-------------|------------|-------------|
| **PRO-AUD-001** | Inventário Cíclico | RF068 | Alta | Trimestral | 1-2 dias + 1 semana | 10 automações | 4 processos |

**Legenda:**
- **Criticidade Alta:** Processo crítico para conformidade regulatória
- **Frequência Trimestral:** Processo executado 4x ao ano (configurável)
- **Tempo Médio:** 1-2 dias para contagem + 1 semana para resolução de divergências
- **Automações:** 10 automações principais (agendamento, conciliação, relatórios, etc)
- **Integrações:** 4 processos integrados (Gestão de Ativos, Chamados, Auditoria de Operações, Custos Fixos)

---

## 4. Glossário

| Termo | Definição |
|-------|-----------|
| **Conciliação** | Processo de comparação entre inventário lógico (sistema) e inventário físico (real) para identificar divergências |
| **Divergência** | Diferença entre o que o sistema registra e o que foi encontrado fisicamente durante o inventário |
| **Falta** | Ativo consta no sistema como ativo, mas não foi encontrado fisicamente durante o inventário |
| **Sobra** | Ativo encontrado fisicamente durante inventário, mas não consta no sistema de ativos (não cadastrado) |
| **GPS (Global Positioning System)** | Sistema de localização por satélite utilizado para registrar coordenadas geográficas durante contagem em campo |
| **Inventário Cíclico** | Processo de auditoria física de ativos com contagem periódica (trimestral, semestral, anual) em vez de anual massiva |
| **Inventário Físico** | Lista de ativos efetivamente encontrados durante contagem física |
| **Inventário Lógico** | Lista de ativos esperados conforme registros do sistema de gestão de ativos |
| **QR Code (Quick Response Code)** | Código de barras bidimensional utilizado para identificação rápida de ativos durante contagem |
| **RFID (Radio Frequency Identification)** | Tecnologia de identificação por radiofrequência utilizada para contagem massiva de ativos (centenas por hora) |
| **Taxa de Conformidade** | Percentual de ativos encontrados na localização e com o usuário correto em relação ao total de ativos esperados (meta: ≥ 95%) |
| **Workflow de Investigação** | Fluxo de trabalho estruturado para investigar causas raízes de divergências críticas (roubo, perda, transferência não documentada) |
| **Baixa de Ativo** | Processo de retirar ativo do inventário ativo, geralmente após confirmação de perda definitiva (roubo, extravio, descarte) |
| **Chamado de Auditoria** | Chamado aberto automaticamente pelo sistema para investigar divergências críticas identificadas durante inventário |
| **Evidência de Auditoria** | Documentação comprobatória (relatórios, logs, assinaturas digitais) retida por 7 anos para conformidade regulatória |
| **Job Hangfire** | Serviço de agendamento de tarefas em segundo plano utilizado para disparar inventários automaticamente |
| **Localização Errada** | Ativo encontrado fisicamente, mas em local diferente do registrado no sistema (ex: sistema diz Sala 201, real está em Sala 305) |
| **Usuário Errado** | Ativo encontrado fisicamente, mas com pessoa diferente da registrada no sistema (ex: sistema diz João, real está com Maria) |
| **Relatório de Conformidade** | Relatório gerencial assinado digitalmente pelo Gestor de TI contendo taxa de conformidade, divergências e ações corretivas |
| **SOX (Sarbanes-Oxley)** | Lei federal dos EUA que estabelece controles rigorosos de auditoria para empresas de capital aberto (aplicável a multinacionais) |
| **ISO 27001** | Norma internacional de gestão de segurança da informação que exige inventário de ativos críticos |
| **Matching Automático** | Algoritmo que compara inventário lógico vs físico por Patrimônio ou Serial Number para identificar correspondências |
| **Timestamp** | Registro de data e hora de um evento (contagem, ajuste, aprovação) para rastreamento de auditoria |
| **Drill-Down** | Capacidade de navegar de visão resumida para detalhada em relatórios (ex: de taxa geral para divergências por sala) |

---

## 5. Referências Cruzadas

### 5.1. Processos Relacionados

- **PRO-FAC-001 (Gestão de Ativos):** Fornece inventário lógico e recebe ajustes automáticos de localização/usuário
- **PRO-SVC-003 (Gestão de Chamados):** Recebe abertura automática de chamados para investigação de divergências críticas
- **PRO-INF-004 (Auditoria de Operações):** Registra todos os eventos de inventário para rastreamento de auditoria
- **PRO-FAC-002 (Custos Fixos):** Recebe informações de ativos não localizados para ajuste de TCO

### 5.2. Requisitos Funcionais

- **RF068:** Inventário Cíclico (requisito funcional implementado por este processo)

### 5.3. Documentação Técnica

- `D:\IC2_Governanca\governanca\ARCHITECTURE.md`: Stack tecnológico e padrões arquiteturais
- `D:\IC2_Governanca\governanca\CONVENTIONS.md`: Nomenclatura e padrões de código
- `D:\IC2_Governanca\governanca\COMPLIANCE.md`: Regras de validação e conformidade

### 5.4. Contratos de Execução

- `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\backend-criacao.md`: Contrato para implementação de handlers de inventário
- `D:\IC2_Governanca\governanca\contracts\desenvolvimento\execucao\frontend-criacao.md`: Contrato para implementação de app mobile de contagem
- `D:\IC2_Governanca\governanca\contracts\auditoria\conformidade.md`: Contrato para auditoria de conformidade do processo

---

## 6. Controle de Versão

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-01-12 | ALC | Criação inicial do documento - Jornada 6: Auditoria e Integrações com processo PRO-AUD-001 (Inventário Cíclico) |

---

**Documento gerado em:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Localização:** `D:\IC2_Governanca\documentacao\Processos\06-Jornada-Auditoria.md`

---

**Notas Finais:**

Este documento é parte da série de documentação modular de processos de negócio do IControlIT. Embora seja a menor jornada em número de processos (apenas 1 processo), o **PRO-AUD-001: Inventário Cíclico** é de criticidade máxima para conformidade regulatória (SOX, ISO 27001, LGPD) e controle patrimonial.

A evolução do modelo legado (inventário anual manual com 65% de conformidade) para o modelo moderno (inventário trimestral automatizado com 95% de conformidade) representa um ganho de 90% em redução de mão de obra, 99% em redução de tempo de conciliação e 30 pontos percentuais em taxa de conformidade.

Para informações sobre outros processos, consulte:
- **Jornada 1:** `D:\IC2_Governanca\documentacao\Processos\01-Jornada-Servicos.md`
- **Jornada 2:** `D:\IC2_Governanca\documentacao\Processos\02-Jornada-Facilities.md`
- **Jornada 3:** `D:\IC2_Governanca\documentacao\Processos\03-Jornada-Usuarios.md`
- **Jornada 4:** `D:\IC2_Governanca\documentacao\Processos\04-Jornada-Infraestrutura.md`
- **Jornada 5:** `D:\IC2_Governanca\documentacao\Processos\05-Jornada-Administrativo.md`
- **Jornada 6:** `D:\IC2_Governanca\documentacao\Processos\06-Jornada-Auditoria.md` (este documento)


---

# PARTE 7: FUNCIONALIDADES DE GESTÃO E CADASTROS

---


**Versão:** 2.0
**Autor:** ALC (alc.dev.br)
**Data:** 2026-01-12
**Status:** Vigente

---

## 1. INTRODUÇÃO

### 1.1 Objetivo deste Documento

Este documento explica por que **72 Requisitos Funcionais (RFs)** do IControlIT **NÃO foram documentados como processos de negócio** nas jornadas 1-6.

**Razão:** Estes RFs são **cadastros simples** ou **funcionalidades de suporte** que:
- ✅ Não possuem workflows multi-etapas complexos
- ✅ Não requerem automações significativas
- ✅ São operações CRUD básicas (Create, Read, Update, Delete)
- ✅ Não envolvem state machines ou transições de estado
- ✅ Não requerem integrações complexas com sistemas externos

**Nota:** Isso **NÃO significa** que esses RFs são menos importantes. Eles são **essenciais** para o funcionamento do sistema, mas **tecnicamente simples** de implementar comparados aos 38 processos documentados.

### 1.2 Critérios de Exclusão

Um RF foi excluído da documentação de processos se atender a **pelo menos 2 dos seguintes critérios**:

| Critério | Descrição |
|----------|-----------|
| **CRUD Simples** | Apenas Create, Read, Update, Delete sem lógica adicional |
| **Sem Workflow** | Não há etapas sequenciais ou paralelas |
| **Sem Automações** | Não dispara jobs automáticos, notificações ou cálculos complexos |
| **Sem Integrações** | Não se integra com sistemas externos (SEFAZ, ERPs, APIs terceiras) |
| **Sem State Machine** | Não possui estados e transições (Novo → Aprovado → Finalizado) |
| **Dados Mestre** | Apenas armazena dados de referência (categorias, tipos, status) |
| **UI Básica** | Interface simples de formulário + grid de listagem |

---

## 2. CADASTROS BASE (17 RFs)

Cadastros de dados mestres do sistema, usados como referência por outros processos.

### RF015: Gestão de Locais/Endereços

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de endereços (rua, cidade, CEP, país) para uso em clientes, fornecedores, ativos.
**Por que não é processo:** CRUD simples, sem workflow, dados de referência para vínculo com entidades.
**Usado por:** PRO-INF-006 (Clientes), PRO-FAC-001 (Ativos), PRO-AUD-001 (Inventário)

### RF016: Gestão de Categorias de Ativos

**Tipo:** Cadastro hierárquico
**Descrição:** Árvore de categorias (Hardware → Notebooks → Dell Latitude) para classificação de ativos.
**Por que não é processo:** CRUD hierárquico simples, navegação em árvore, dados de referência.
**Usado por:** PRO-FAC-001 (Gestão de Ativos), PRO-AUD-001 (Inventário)

### RF017: Hierarquia Corporativa

**Tipo:** Cadastro hierárquico multi-nível
**Descrição:** Estrutura organizacional (Holding → Empresa → Filial → Departamento → Setor) com relacionamentos parent-child.
**Por que não é processo:** CRUD hierárquico, navegação organizacional, dados de referência para multi-tenancy.
**Usado por:** TODOS os processos (contexto organizacional obrigatório)

### RF018: Gestão de Cargos

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de cargos (nome, descrição, nível hierárquico) para vínculo com colaboradores.
**Por que não é processo:** CRUD simples, dados de referência para RH.
**Usado por:** PRO-INF-006 (Colaboradores), PRO-SVC-001 (Service Desk - roteamento por cargo)

### RF019: Gestão de Tipos de Ativos

**Tipo:** Cadastro CRUD com templates
**Descrição:** Tipos de ativos (Notebook, Desktop, Servidor, Switch) com campos customizáveis.
**Por que não é processo:** CRUD com configuração de campos dinâmicos, mas sem workflow.
**Usado por:** PRO-FAC-001 (Gestão de Ativos), PRO-AUD-001 (Inventário)

### RF020: Gestão de Documentos e Anexos

**Tipo:** Upload/Download de arquivos
**Descrição:** Upload de PDFs, imagens, planilhas vinculados a contratos, ativos, chamados com armazenamento Azure Blob.
**Por que não é processo:** Operação técnica de armazenamento, sem workflow de aprovação ou versionamento complexo.
**Usado por:** PRO-FCT-001 (Contratos - anexos contratuais), PRO-SVC-001 (Chamados - evidências)

### RF022: Gestão de Fornecedores

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de fornecedores (CNPJ, razão social, contato, endereço) para contratos e compras.
**Por que não é processo:** CRUD básico com validação de CNPJ. O processo de homologação está em PRO-FCT-001.
**Usado por:** PRO-FCT-001 (Contratos), PRO-FAC-002 (Compras), PRO-TEL-004 (Operadoras)

### RF024: Gestão de Departamentos

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de departamentos (nome, centro de custo, gestor responsável) vinculado à hierarquia corporativa.
**Por que não é processo:** CRUD simples, dados de referência para alocação de custos.
**Usado por:** PRO-FCT-002 (Rateio), PRO-SVC-001 (Service Desk - roteamento)

### RF039: Gestão de Bilhetes

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de bilhetes telefônicos (CDR - Call Detail Records) para análise de consumo.
**Por que não é processo:** CRUD com importação CSV. O processo de análise está em PRO-TEL-002 (Gestão de Contas).
**Usado por:** PRO-TEL-002 (Gestão de Contas Telecom), PRO-FCT-003 (Contestação)

### RF041: Gestão de Estoque de Aparelhos

**Tipo:** Cadastro CRUD com controle quantitativo
**Descrição:** Estoque de aparelhos celulares (modelo, IMEI, quantidade, status: disponível/alocado/manutenção).
**Por que não é processo:** CRUD com controle de quantidade. O processo de movimentação está em PRO-FAC-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel), PRO-FAC-001 (Gestão de Ativos)

### RF043: Gestão de Endereços de Entrega

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de endereços alternativos para entrega de ativos (matriz, filiais, home office).
**Por que não é processo:** CRUD simples, dados de referência para logística.
**Usado por:** PRO-FAC-002 (Compras - endereço de entrega), PRO-TEL-001 (Entrega de chips)

### RF047: Gestão de Tipos de Consumidores

**Tipo:** Cadastro CRUD
**Descrição:** Tipos de consumidores telecom (Corporativo, VIP, Comum, Temporário) para classificação de linhas.
**Por que não é processo:** CRUD simples, dados de referência para políticas de consumo.
**Usado por:** PRO-TEL-001 (Telefonia Móvel), PRO-TEL-002 (Gestão de Contas)

### RF048: Gestão de Status de Consumidores

**Tipo:** Cadastro CRUD
**Descrição:** Status de consumidores telecom (Ativo, Suspenso, Cancelado, Bloqueado) para controle de ciclo de vida.
**Por que não é processo:** CRUD de estados. O workflow de transição está em PRO-TEL-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel - mudança de status)

### RF049: Gestão de Políticas de Consumidores

**Tipo:** Cadastro CRUD com regras
**Descrição:** Políticas de consumo telecom (franquia de dados, minutos, roaming permitido/bloqueado).
**Por que não é processo:** CRUD com configuração de regras. A aplicação está em PRO-TEL-002.
**Usado por:** PRO-TEL-001 (Telefonia Móvel), PRO-TEL-002 (Gestão de Contas - alertas)

### RF050: Gestão de Linhas/Chips/SIM

**Tipo:** Cadastro CRUD com rastreamento
**Descrição:** Cadastro de linhas telefônicas (número, ICCID, operadora, plano, usuário alocado).
**Por que não é processo:** CRUD com rastreamento de alocação. O processo de provisionamento está em PRO-TEL-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel), PRO-TEL-002 (Gestão de Contas)

### RF051: Gestão de Marcas e Modelos

**Tipo:** Cadastro CRUD hierárquico
**Descrição:** Cadastro de marcas (Dell, HP, Apple) e modelos (Latitude 5420, EliteBook 840) para ativos.
**Por que não é processo:** CRUD hierárquico simples (Marca → Modelo), dados de referência.
**Usado por:** PRO-FAC-001 (Gestão de Ativos), PRO-FAC-002 (Compras)

### RF052: Gestão de Consumidores

**Tipo:** Cadastro CRUD
**Descrição:** Cadastro de consumidores de serviços telecom (colaborador, tipo, política, linha vinculada).
**Por que não é processo:** CRUD com vínculo entre colaborador e linha. O processo de aprovisionamento está em PRO-TEL-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel), PRO-TEL-002 (Gestão de Contas)

---

## 3. GESTÃO DE PROCESSOS AUXILIARES (20 RFs)

Funcionalidades que complementam os processos principais, mas não são processos por si só.

### RF012: Gestão de Usuários do Sistema

**Tipo:** CRUD com RBAC
**Descrição:** Cadastro de usuários (nome, email, perfil, status, multi-tenancy) para acesso ao sistema.
**Por que não é processo:** CRUD básico com permissões. O processo complexo está em PRO-INF-007 (Login/Autenticação).
**Usado por:** TODOS os processos (autenticação obrigatória)

### RF013: Gestão de Perfis de Acesso (RBAC)

**Tipo:** CRUD com permissões
**Descrição:** Cadastro de perfis (Admin, Gestor, Analista, Usuário) com permissões granulares (Create, Read, Update, Delete por módulo).
**Por que não é processo:** CRUD com matriz de permissões. A aplicação está em PRO-INF-007.
**Usado por:** TODOS os processos (autorização obrigatória)

### RF027: Gestão de Aditivos de Contratos

**Tipo:** CRUD vinculado
**Descrição:** Cadastro de aditivos contratuais (número, data, valor, descrição) vinculados a contrato principal.
**Por que não é processo:** CRUD simples. O processo de gestão contratual está em PRO-FCT-001.
**Usado por:** PRO-FCT-001 (Contratos - versionamento)

### RF054: Gestão de Lotes de Auditoria

**Tipo:** CRUD com agrupamento
**Descrição:** Agrupamento de itens para auditoria física (lote, data, responsável, status).
**Por que não é processo:** CRUD de agrupamento. O processo de auditoria está em PRO-AUD-001.
**Usado por:** PRO-AUD-001 (Inventário Físico)

### RF056: Gestão de Filas de Atendimento

**Tipo:** CRUD com roteamento
**Descrição:** Cadastro de filas de atendimento (TI, Facilities, Telecom) com SLA e técnicos responsáveis.
**Por que não é processo:** CRUD com configuração de roteamento. O processo está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk - roteamento automático)

### RF057: Gestão de Itens de Rateio

**Tipo:** CRUD com fórmulas
**Descrição:** Cadastro de itens rateaveis (aluguel, energia, telecom) com fórmulas de distribuição.
**Por que não é processo:** CRUD com configuração de regras. O processo de cálculo está em PRO-FCT-002.
**Usado por:** PRO-FCT-002 (Rateio de Custos)

### RF058: Gestão de Tipos de Bilhetes

**Tipo:** Cadastro CRUD
**Descrição:** Tipos de bilhetes telecom (Local, DDD, DDI, 0800, SMS) para classificação de consumo.
**Por que não é processo:** CRUD simples, dados de referência para análise de CDR.
**Usado por:** PRO-TEL-002 (Gestão de Contas), PRO-FCT-003 (Contestação)

### RF059: Gestão de Status de Tipos Genéricos

**Tipo:** Cadastro CRUD parametrizável
**Descrição:** Status genéricos configuráveis (Ativo/Inativo, Aprovado/Reprovado, Aberto/Fechado) para uso em múltiplas entidades.
**Por que não é processo:** CRUD de configuração. A aplicação está nos workflows específicos.
**Usado por:** TODOS os processos (status customizáveis)

### RF060: Gestão de Tipos de Chamado

**Tipo:** Cadastro CRUD com templates
**Descrição:** Tipos de chamado (Incidente, Requisição, Mudança) com campos obrigatórios e SLA padrão.
**Por que não é processo:** CRUD com configuração de templates. O processo está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk), PRO-SVC-002 (Change Management)

### RF061: Gestão de Ordens de Serviço

**Tipo:** CRUD com workflow simplificado
**Descrição:** Cadastro de ordens de serviço (instalação, manutenção, desinstalação) com técnico e agendamento.
**Por que não é processo:** CRUD com agendamento básico. Workflows complexos estão em PRO-SVC-003.
**Usado por:** PRO-SVC-003 (Field Service), PRO-FAC-001 (Manutenção de ativos)

### RF062: Gestão de Fornecedores e Parceiros

**Tipo:** CRUD com qualificação
**Descrição:** Cadastro detalhado de fornecedores (CNPJ, categoria, avaliação, documentação fiscal).
**Por que não é processo:** CRUD com campos adicionais. O processo de homologação está em PRO-FCT-001.
**Usado por:** PRO-FCT-001 (Contratos), PRO-FAC-002 (Compras)

### RF070: Base de Conhecimento

**Tipo:** CRUD com busca textual
**Descrição:** Artigos de conhecimento (problema, solução, categoria) com busca full-text para resolução de chamados.
**Por que não é processo:** CRUD com indexação. O uso está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk - resolução rápida)

### RF071: Pesquisa de Satisfação

**Tipo:** CRUD com questionário
**Descrição:** Cadastro de pesquisas (NPS, CSAT) com envio automático pós-atendimento.
**Por que não é processo:** CRUD com disparo automático. A análise está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk - qualidade), PRO-SVC-003 (Field Service)

### RF073: Gestão de Chamados e SLA (complementar a RF033)

**Tipo:** CRUD com cálculo de tempo
**Descrição:** Cadastro de SLAs (tempo de resposta, resolução, prioridade) para chamados.
**Por que não é processo:** CRUD com configuração de regras. O processo está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk - monitoramento de SLA)

### RF074: Gestão de Chamados/Tickets (complementar a RF033)

**Tipo:** CRUD com workflow
**Descrição:** Cadastro de chamados (título, descrição, categoria, prioridade, anexos).
**Por que não é processo:** CRUD básico. O workflow completo está em PRO-SVC-001.
**Usado por:** PRO-SVC-001 (Service Desk)

### RF076: Manutenção Preventiva e Corretiva

**Tipo:** CRUD com agendamento
**Descrição:** Cadastro de planos de manutenção (preventiva mensal, corretiva sob demanda) para ativos críticos.
**Por que não é processo:** CRUD com agendamento. O processo está em PRO-FAC-001.
**Usado por:** PRO-FAC-001 (Gestão de Ativos - ciclo de vida)

### RF077: Ordens de Serviço de Atendimento

**Tipo:** CRUD com workflow básico
**Descrição:** Cadastro de OS para atendimentos externos (instalação, configuração, treinamento).
**Por que não é processo:** CRUD com workflow simples (Aberta → Em Execução → Concluída). Workflow completo em PRO-SVC-003.
**Usado por:** PRO-SVC-003 (Field Service)

### RF091: Anexos/Documentos Contratuais

**Tipo:** Upload/Download vinculado
**Descrição:** Upload de documentos contratuais (PDF assinado, aditivos, apólices) com versionamento básico.
**Por que não é processo:** Operação de armazenamento. O processo de gestão está em PRO-FCT-001.
**Usado por:** PRO-FCT-001 (Contratos), PRO-FAC-002 (Compras - pedidos)

### RF092: Garantias, Seguros e Contratuais

**Tipo:** CRUD com datas
**Descrição:** Cadastro de garantias (fabricante, estendida) e seguros (apólice, vigência, cobertura).
**Por que não é processo:** CRUD com alertas de vencimento. O processo de renovação está em PRO-FCT-001.
**Usado por:** PRO-FCT-001 (Contratos), PRO-FAC-001 (Ativos - garantia)

### RF106: Gestão de Marcações/Tags

**Tipo:** CRUD com tagging
**Descrição:** Cadastro de tags customizáveis (Crítico, VIP, Urgente, Projeto X) para classificação multi-dimensional.
**Por que não é processo:** CRUD de metadados. Uso transversal em todos os módulos.
**Usado por:** TODOS os processos (classificação flexível)

---

## 4. COMPLIANCE E AUDITORIA AUXILIAR (8 RFs)

Funcionalidades de compliance que suportam o processo principal PRO-INF-004 (Auditoria de Operações).

### RF079: Gestão de Políticas de Compliance

**Tipo:** Cadastro com versionamento
**Descrição:** Cadastro de políticas de compliance (ISO 27001, LGPD, SOX, HIPAA) com texto, versão e vigência.
**Por que não é processo:** Cadastro versionado com aprovação simples. O processo de auditoria está em PRO-INF-004.
**Usado por:** PRO-INF-004 (Auditoria de Operações), PRO-INF-007 (Segurança)

### RF080: Gestão de Termos de Aceite (LGPD)

**Tipo:** CRUD com aceite digital
**Descrição:** Cadastro de termos de aceite (privacidade, uso de dados) com registro de IP, data/hora de aceite.
**Por que não é processo:** CRUD com registro de evidência. O processo de compliance LGPD está em PRO-INF-004.
**Usado por:** PRO-INF-004 (Auditoria), PRO-INF-007 (Login - aceite obrigatório)

### RF081: Termos de Responsabilidade

**Tipo:** CRUD com assinatura digital
**Descrição:** Cadastro de termos de responsabilidade (entrega de ativo, acesso a sistema) com assinatura eletrônica.
**Por que não é processo:** CRUD com evidência de aceite. O processo de entrega está em PRO-FAC-001.
**Usado por:** PRO-FAC-001 (Gestão de Ativos - movimentação), PRO-SVC-003 (Field Service)

### RF082: Termos de Responsabilidade (duplicado?)

**Tipo:** CRUD com assinatura digital
**Descrição:** Possível duplicação de RF081. Verificar se há diferença funcional (ex: termo de saída vs. termo de entrega).
**Por que não é processo:** CRUD com evidência de aceite. Se duplicado, consolidar com RF081.
**Usado por:** PRO-FAC-001 (Gestão de Ativos)

### RF094: Auditoria de Custos e Compliance

**Tipo:** Dashboard de leitura
**Descrição:** Visualização de desvios de custos (orçado vs. realizado) e conformidade contratual (SLA, multas).
**Por que não é processo:** Dashboard de análise. Os processos de auditoria estão em PRO-FCT-001 e PRO-INF-004.
**Usado por:** Gestores financeiros (análise de desvios)

### RF095: Auditoria de Acesso e Segurança

**Tipo:** Dashboard de leitura
**Descrição:** Visualização de acessos anômalos (horários incomuns, tentativas de invasão, mudanças de permissões).
**Por que não é processo:** Dashboard de monitoramento. O processo de resposta a incidentes está em PRO-INF-007.
**Usado por:** Time de Segurança (monitoramento contínuo)

### RF096: Auditoria de Mudanças em Dados

**Tipo:** Log de leitura
**Descrição:** Visualização de logs de auditoria (quem alterou o quê, quando, valor anterior/novo) para rastreabilidade.
**Por que não é processo:** Consulta de logs. O processo de auditoria está em PRO-INF-004.
**Usado por:** Auditores (investigação de mudanças)

### RF098: Auditoria de Logs do Sistema

**Tipo:** Log de leitura com busca
**Descrição:** Visualização de logs técnicos (erros, exceções, performance) com filtros por data, usuário, módulo.
**Por que não é processo:** Consulta de logs técnicos. O processo de troubleshooting está em PRO-INF-002 (Monitoramento).
**Usado por:** Time de Desenvolvimento/SRE (debugging)

---

## 5. DASHBOARDS E RELATÓRIOS (7 RFs)

Funcionalidades de visualização de dados. Não são processos, são **outputs** de processos.

### RF093: Indicadores de Performance e Compliance

**Tipo:** Dashboard de leitura
**Descrição:** Exibição de KPIs (SLA compliance, taxa de resolução de chamados, tempo médio de atendimento).
**Por que não é processo:** Apenas visualização. Os processos que geram esses dados estão documentados nas jornadas 1-6.
**Usado por:** Gerentes (visualização de métricas dos processos PRO-SVC-001, PRO-SVC-003)

### RF099: Dashboards e KPIs

**Tipo:** Dashboard de leitura
**Descrição:** Dashboards customizáveis com widgets (gráficos, tabelas, gauges) para monitoramento operacional.
**Por que não é processo:** Visualização configurável. Dados gerados por TODOS os 38 processos.
**Usado por:** Todos os perfis (visão unificada)

### RF100: Dashboards e KPIs (duplicado?)

**Tipo:** Dashboard de leitura
**Descrição:** Possível duplicação de RF099. Verificar se há diferença (ex: dashboards executivos vs. operacionais).
**Por que não é processo:** Visualização de dados. Consolidar com RF099 se duplicado.
**Usado por:** Gestores executivos

### RF101: Dashboards Executivos e Operacionais

**Tipo:** Dashboard multinível
**Descrição:** Dashboards estratificados (C-Level: indicadores estratégicos; Gerencial: KPIs táticos; Operacional: métricas diárias).
**Por que não é processo:** Visualização hierárquica. Dados gerados pelos 38 processos.
**Usado por:** Todos os níveis hierárquicos (drill-down)

### RF102: Relatórios e Análises

**Tipo:** Geração de relatórios
**Descrição:** Relatórios exportáveis (PDF, Excel) com filtros customizáveis (período, centro de custo, categoria).
**Por que não é processo:** Exportação de dados. Processos de análise estão em PRO-FCT-002 (Rateio), PRO-TEL-002 (Contas).
**Usado por:** Analistas financeiros (exportação para BI externo)

### RF103: Relatórios e Volumetria

**Tipo:** Relatório de dados agregados
**Descrição:** Relatórios de volumetria (quantidade de ativos por categoria, chamados por mês, consumo telecom por departamento).
**Por que não é processo:** Agregação de dados. Processos de gestão estão documentados nas jornadas 1-6.
**Usado por:** Gestores (planejamento de capacidade)

### RF104: Gestão Completa de Cadastros Base

**Tipo:** Interface unificada CRUD
**Descrição:** Interface unificada para acesso a todos os cadastros base (RF015-RF052) com busca global.
**Por que não é processo:** Interface de navegação. Cada cadastro está detalhado na seção 2.
**Usado por:** Administradores (configuração inicial do sistema)

---

## 6. FUNCIONALIDADES TÉCNICAS AVANÇADAS (12 RFs)

Funcionalidades de infraestrutura técnica. Suportam os processos, mas não são processos de negócio.

### RF045: Gestão de Volumetria

**Tipo:** Análise de dados
**Descrição:** Análise de volumetria de consumo telecom (top 10 consumidores, evolução mensal, outliers).
**Por que não é processo:** Análise estatística. O processo de gestão está em PRO-TEL-002.
**Usado por:** PRO-TEL-002 (Gestão de Contas - identificação de desvios)

### RF046: Gestão de Grupos de Troncos

**Tipo:** Cadastro CRUD técnico
**Descrição:** Cadastro de grupos de troncos SIP (operadora, capacidade, roteamento) para telefonia IP.
**Por que não é processo:** CRUD técnico para configuração de infraestrutura telecom.
**Usado por:** PRO-TEL-003 (Telefonia Fixa - roteamento de chamadas)

### RF075: Roaming Internacional

**Tipo:** Cadastro com políticas
**Descrição:** Cadastro de políticas de roaming (países permitidos, franquia, bloqueio automático) com aprovação de gestor.
**Por que não é processo:** CRUD com regras de negócio. A aplicação está em PRO-TEL-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel - viagens internacionais)

### RF105: Integração com APIs Externas / Operadoras Telecom

**Tipo:** Infraestrutura técnica
**Descrição:** Integração via API REST com operadoras (Vivo, Claro, TIM) para provisionamento automático de linhas.
**Por que não é processo:** Infraestrutura de integração. Usado transparentemente por PRO-TEL-001.
**Usado por:** PRO-TEL-001 (Telefonia Móvel - provisionamento), PRO-TEL-002 (Importação de faturas)

### RF107: Marcadores, Localização, QRCode

**Tipo:** Funcionalidade técnica
**Descrição:** Geração de QRCode para ativos, geolocalização de técnicos em campo, marcadores em mapas.
**Por que não é processo:** Funcionalidade de suporte. Uso em PRO-AUD-001 (QRCode de inventário) e PRO-SVC-003 (GPS de técnicos).
**Usado por:** PRO-AUD-001 (Inventário), PRO-SVC-003 (Field Service)

### RF108: CAPTCHA, MFA, Contestação, etc.

**Tipo:** Funcionalidades de segurança
**Descrição:** CAPTCHA em login, MFA (Multi-Factor Authentication), fluxo de contestação de faturas.
**Por que não é processo:** Funcionalidades isoladas. MFA está em PRO-INF-007, contestação em PRO-FCT-003.
**Usado por:** PRO-INF-007 (Login), PRO-FCT-003 (Contestação de Faturas)

### RF109: Gestão de Documentos Originais/Digitalização

**Tipo:** Digitalização com OCR
**Descrição:** Upload de documentos físicos com OCR (extração de texto), indexação e busca full-text.
**Por que não é processo:** Funcionalidade de digitalização. Usado em PRO-FCT-001 (contratos escaneados).
**Usado por:** PRO-FCT-001 (Contratos), PRO-FAC-002 (Notas fiscais)

### RF110: Cache Distribuído/Performance

**Tipo:** Infraestrutura técnica
**Descrição:** Redis cache para performance (traduções i18n, configurações do sistema, queries frequentes).
**Por que não é processo:** Infraestrutura técnica transparente. Usado por TODOS os processos como otimização.
**Usado por:** TODOS os 38 processos (redução de latência)

### RF111: Backup e Recuperação (DR)

**Tipo:** Infraestrutura técnica
**Descrição:** Backup automático diário (Azure Backup), retenção 30 dias, testes de disaster recovery mensais.
**Por que não é processo:** Infraestrutura de resiliência. Garante continuidade de TODOS os processos.
**Usado por:** TODOS os processos (recuperação de desastres)

### RF112: Jobs e Tarefas Agendadas

**Tipo:** Infraestrutura técnica
**Descrição:** Agendamento de jobs (Hangfire): importação de faturas, cálculo de rateio, envio de alertas, backup.
**Por que não é processo:** Infraestrutura de automação. Jobs específicos estão documentados nos processos.
**Usado por:** PRO-TEL-002 (job de importação), PRO-FCT-002 (job de rateio), PRO-INF-002 (job de monitoramento)

### RF113: Automação RPA e Bots

**Tipo:** Infraestrutura técnica
**Descrição:** Bots RPA para download automático de faturas de portais de operadoras, preenchimento de formulários.
**Por que não é processo:** Automação robótica. Usado transparentemente por PRO-TEL-002.
**Usado por:** PRO-TEL-002 (Gestão de Contas - download de faturas)

### RF114: RPA, Email, Cache, BI, etc.

**Tipo:** Funcionalidades técnicas diversas
**Descrição:** Conjunto de funcionalidades transversais (envio de email SMTP, cache Redis, exportação para BI).
**Por que não é processo:** Funcionalidades de infraestrutura. Usadas por múltiplos processos.
**Usado por:** TODOS os processos (notificações, performance, análise)

---

## 7. DÉBITO TÉCNICO (1 RF)

### RF115: Refactoring, Débito Técnico

**Tipo:** Manutenção técnica
**Descrição:** Refatoração de código legado, redução de complexidade ciclomática, modernização de bibliotecas (Angular 12 → 19, .NET 6 → 9).
**Por que não é processo:** Tarefa técnica interna de desenvolvimento. Não é processo de negócio visível ao usuário.
**Impacto:** Melhora qualidade de código, performance e manutenibilidade dos 38 processos documentados.
**Usado por:** Todos os processos (qualidade técnica contínua)

---

## 8. RFs A VALIDAR (7 RFs)

RFs mencionados em documentação mas sem detalhamento completo. Requerem validação.

### RF034: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF035: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF040: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF044: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF069: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF085: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

### RF090: (Descrição a validar)

**Tipo:** A definir
**Descrição:** RF mencionado mas sem detalhamento. Requer análise para classificação.
**Status:** Pendente de validação

---

## 9. MATRIZ CONSOLIDADA

Tabela resumida dos 72 RFs documentados:

| Categoria | Quantidade | Exemplos | Usado por Processos | Complexidade Técnica |
|-----------|------------|----------|---------------------|----------------------|
| **Cadastros Base** | 17 | RF015 (Endereços), RF016 (Categorias), RF017 (Hierarquia) | PRO-INF-006, PRO-FAC-001, PRO-AUD-001 | Baixa (CRUD simples) |
| **Processos Auxiliares** | 20 | RF012 (Usuários), RF013 (RBAC), RF027 (Aditivos) | PRO-SVC-001, PRO-FCT-001, PRO-AUD-001 | Média (CRUD com regras) |
| **Compliance Auxiliar** | 8 | RF079 (Políticas), RF080 (Termos LGPD), RF094 (Auditoria Custos) | PRO-INF-004, PRO-INF-007 | Média (versionamento, logs) |
| **Dashboards/Relatórios** | 7 | RF093 (KPIs), RF099 (Dashboards), RF101 (Executivos) | TODOS (visualização) | Baixa (leitura de dados) |
| **Técnicas Avançadas** | 12 | RF110 (Cache), RF111 (Backup), RF112 (Jobs), RF113 (RPA) | TODOS (infraestrutura) | Alta (integração, automação) |
| **Débito Técnico** | 1 | RF115 (Refactoring) | TODOS (qualidade) | Média (manutenção contínua) |
| **A Validar** | 7 | RF034, RF035, RF040, RF044, RF069, RF085, RF090 | - | Desconhecida |

**Total:** 72 RFs de cadastros/funcionalidades de suporte

### Distribuição por Jornada

| Jornada | RFs de Suporte Utilizados | Principais Processos |
|---------|---------------------------|----------------------|
| **Jornada 1: Informações** | RF012, RF013, RF017, RF079, RF080, RF110, RF111 | PRO-INF-001 a PRO-INF-007 |
| **Jornada 2: Facilities** | RF015, RF016, RF019, RF020, RF022, RF051, RF076, RF091, RF092 | PRO-FAC-001 a PRO-FAC-003 |
| **Jornada 3: Finanças** | RF024, RF027, RF057, RF093, RF094, RF102, RF103 | PRO-FCT-001 a PRO-FCT-003 |
| **Jornada 4: Serviços** | RF056, RF058, RF060, RF061, RF070, RF071, RF073, RF074, RF077 | PRO-SVC-001 a PRO-SVC-003 |
| **Jornada 5: Telecom** | RF039, RF041, RF043, RF045, RF046, RF047-052, RF075, RF105, RF113 | PRO-TEL-001 a PRO-TEL-004 |
| **Jornada 6: Auditoria** | RF054, RF079-082, RF094-096, RF098, RF107 | PRO-AUD-001 a PRO-AUD-003 |

---

## 10. PADRÕES DE IMPLEMENTAÇÃO

Todos os 72 RFs seguem os mesmos padrões arquiteturais dos 38 processos documentados.

### Padrão Backend (CQRS + Clean Architecture)

```
D:\IC2\backend\
├── src\
│   ├── IControlIT.Application\
│   │   ├── Features\
│   │   │   ├── Locais\                    # RF015
│   │   │   │   ├── Commands\
│   │   │   │   │   ├── CreateLocalCommand.cs
│   │   │   │   │   └── CreateLocalCommandHandler.cs
│   │   │   │   └── Queries\
│   │   │   │       ├── GetLocaisQuery.cs
│   │   │   │       └── GetLocaisQueryHandler.cs
│   │   │   ├── Categorias\                # RF016
│   │   │   ├── Cargos\                    # RF018
│   │   │   └── ... (demais cadastros)
│   ├── IControlIT.Domain\
│   │   ├── Entities\
│   │   │   ├── Local.cs
│   │   │   ├── Categoria.cs
│   │   │   └── Cargo.cs
│   └── IControlIT.Infrastructure\
│       └── Persistence\
│           ├── Configurations\
│           │   ├── LocalConfiguration.cs
│           │   └── CategoriaConfiguration.cs
```

**Complexidade:** Baixa (template padrão)
**Tempo de Implementação:** 2-4h por RF de cadastro CRUD

### Padrão Frontend (Angular Standalone Components)

```
D:\IC2\frontend\icontrolit-app\src\app\
├── features\
│   ├── locais\                            # RF015
│   │   ├── components\
│   │   │   ├── local-form.component.ts
│   │   │   └── local-list.component.ts
│   │   ├── services\
│   │   │   └── local.service.ts
│   │   └── models\
│   │       └── local.model.ts
│   ├── categorias\                        # RF016
│   └── cargos\                            # RF018
```

**Complexidade:** Baixa (template padrão com FormGroup + PrimeNG)
**Tempo de Implementação:** 3-5h por RF de cadastro CRUD

### Padrão de Testes

**Backend (xUnit):**
```csharp
// D:\IC2\backend\tests\IControlIT.Application.Tests\Features\Locais\
[Fact]
public async Task CreateLocal_ComDadosValidos_DeveCriarComSucesso()
{
    // Arrange
    var command = new CreateLocalCommand { ... };

    // Act
    var result = await _handler.Handle(command, CancellationToken.None);

    // Assert
    result.IsSuccess.Should().BeTrue();
}
```

**Frontend (Jest + Playwright):**
```typescript
// D:\IC2\frontend\icontrolit-app\src\app\features\locais\components\local-form.component.spec.ts
describe('LocalFormComponent', () => {
  it('should create local with valid data', () => {
    // Arrange
    component.localForm.setValue({ ... });

    // Act
    component.onSubmit();

    // Assert
    expect(localService.create).toHaveBeenCalled();
  });
});
```

**Cobertura Exigida:** ≥ 80% (conforme COMPLIANCE.md)

---

## 11. ROADMAP DE IMPLEMENTAÇÃO

Sugestão de priorização dos 72 RFs por criticidade e dependências:

### Fase 1: Cadastros Fundamentais (Prioridade CRÍTICA)

**Sprint 1-2:**
- RF017: Hierarquia Corporativa (obrigatório para multi-tenancy)
- RF012: Gestão de Usuários (obrigatório para autenticação)
- RF013: Gestão de Perfis de Acesso (obrigatório para autorização)

**Impacto:** Bloqueia TODOS os demais processos se não implementado.

### Fase 2: Cadastros Base (Prioridade ALTA)

**Sprint 3-5:**
- RF015: Locais/Endereços
- RF016: Categorias de Ativos
- RF019: Tipos de Ativos
- RF022: Fornecedores
- RF024: Departamentos
- RF051: Marcas e Modelos

**Impacto:** Requerido por processos de Facilities (PRO-FAC-001, PRO-FAC-002).

### Fase 3: Telecom Base (Prioridade ALTA)

**Sprint 6-8:**
- RF047: Tipos de Consumidores
- RF048: Status de Consumidores
- RF049: Políticas de Consumidores
- RF050: Linhas/Chips/SIM
- RF052: Consumidores

**Impacto:** Requerido por processos de Telecom (PRO-TEL-001, PRO-TEL-002).

### Fase 4: Service Desk (Prioridade MÉDIA)

**Sprint 9-11:**
- RF056: Filas de Atendimento
- RF058: Tipos de Bilhetes
- RF060: Tipos de Chamado
- RF070: Base de Conhecimento
- RF071: Pesquisa de Satisfação

**Impacto:** Requerido por PRO-SVC-001 (Service Desk).

### Fase 5: Compliance (Prioridade MÉDIA)

**Sprint 12-14:**
- RF079: Políticas de Compliance
- RF080: Termos de Aceite LGPD
- RF081: Termos de Responsabilidade
- RF094: Auditoria de Custos
- RF095: Auditoria de Segurança

**Impacto:** Requerido por PRO-INF-004 (Auditoria).

### Fase 6: Dashboards (Prioridade BAIXA)

**Sprint 15-17:**
- RF093: Indicadores de Performance
- RF099: Dashboards e KPIs
- RF101: Dashboards Executivos
- RF102: Relatórios e Análises

**Impacto:** Visualização de dados. Não bloqueia processos operacionais.

### Fase 7: Funcionalidades Técnicas (Prioridade BAIXA)

**Sprint 18-20:**
- RF110: Cache Distribuído
- RF111: Backup e Recuperação
- RF112: Jobs Agendados
- RF113: Automação RPA

**Impacto:** Otimizações. Sistema funciona sem, mas com performance reduzida.

### Fase 8: Débito Técnico (Prioridade CONTÍNUA)

**Sprints contínuos:**
- RF115: Refactoring

**Impacto:** Melhoria contínua de qualidade de código.

---

## 12. ANÁLISE DE ESFORÇO

Estimativa de esforço para implementação dos 72 RFs:

| Categoria | Quantidade | Tempo Médio/RF | Tempo Total | Complexidade |
|-----------|------------|----------------|-------------|--------------|
| **Cadastros CRUD Simples** | 17 | 6h | 102h (~13 dias) | Baixa |
| **CRUD com Regras** | 20 | 12h | 240h (~30 dias) | Média |
| **Compliance/Auditoria** | 8 | 16h | 128h (~16 dias) | Média-Alta |
| **Dashboards/Relatórios** | 7 | 20h | 140h (~17.5 dias) | Média-Alta |
| **Infraestrutura Técnica** | 12 | 24h | 288h (~36 dias) | Alta |
| **Débito Técnico** | 1 | Contínuo | - | Variável |
| **A Validar** | 7 | - | - | Desconhecida |

**Total Estimado:** ~898 horas (~112 dias úteis com 1 desenvolvedor)

**Com time de 3 devs:** ~37 dias úteis (~7.5 sprints de 2 semanas)

**Observações:**
- Estimativa assume desenvolvedor com conhecimento de Angular + .NET + CQRS
- Inclui: implementação, testes unitários, testes E2E, documentação
- NÃO inclui: revisão de código, refatorações, correção de bugs pós-implementação
- Crítico: RF017 (Hierarquia) deve ser implementado PRIMEIRO (bloqueia multi-tenancy)

---

## 13. DEPENDÊNCIAS ENTRE RFs

Mapa de dependências críticas:

```mermaid
graph TD
    RF017[RF017: Hierarquia Corporativa] --> RF012[RF012: Usuários]
    RF017 --> RF024[RF024: Departamentos]
    RF017 --> RF015[RF015: Locais]

    RF012 --> RF013[RF013: Perfis RBAC]

    RF016[RF016: Categorias] --> RF019[RF019: Tipos de Ativos]
    RF019 --> RF051[RF051: Marcas e Modelos]

    RF022[RF022: Fornecedores] --> RF027[RF027: Aditivos]

    RF047[RF047: Tipos Consumidores] --> RF048[RF048: Status Consumidores]
    RF048 --> RF049[RF049: Políticas]
    RF049 --> RF050[RF050: Linhas/Chips]
    RF050 --> RF052[RF052: Consumidores]

    RF056[RF056: Filas] --> RF060[RF060: Tipos de Chamado]
    RF060 --> RF073[RF073: SLA]
```

**Regra de Implementação:**
- RFs dependentes **DEVEM** aguardar conclusão dos RFs bloqueantes
- Testes de integração **DEVEM** validar dependências
- Migrations de banco **DEVEM** respeitar ordem de Foreign Keys

---

## 14. VALIDAÇÃO DE CONFORMIDADE

Todos os 72 RFs **DEVEM** atender aos mesmos critérios de conformidade dos 38 processos:

### Checklist de Conformidade por RF

- [ ] **Multi-Tenancy:** Filtro por ClienteId obrigatório em queries
- [ ] **RBAC:** Permissões configuradas em RF013
- [ ] **Auditoria:** Logs de criação/alteração/exclusão (RF096, RF098)
- [ ] **LGPD:** Dados sensíveis criptografados
- [ ] **Testes:** Cobertura ≥ 80%
- [ ] **Documentação:** README.md em cada feature
- [ ] **Migrations:** Script SQL versionado
- [ ] **Validações:** FluentValidation em Commands
- [ ] **Tratamento de Erros:** Result pattern (Success/Failure)
- [ ] **Performance:** Cache em queries frequentes (RF110)

**Ferramenta de Validação:**
```bash
python D:\IC2_Governanca\tools\validator-rf-uc.py RFXXX
```

**Bloqueio Automático:** Commit rejeitado se validação falhar (exit code ≠ 0)

---

## 15. CONCLUSÃO

Os **72 RFs documentados neste arquivo** são **essenciais** para o funcionamento do IControlIT, mas **não requerem documentação de processo de negócio** pois são:

1. ✅ **Tecnicamente simples** (CRUD básico, cadastros, visualizações)
2. ✅ **Sem workflows complexos** (não há etapas, aprovações, state machines)
3. ✅ **Suporte aos 38 processos** (não são processos independentes)

### Valor Estratégico

**Redução de Complexidade Documental:**
- Documentação de processos focada em workflows realmente complexos
- Evita duplicação de informação (cadastros seguem template padrão)
- Facilita onboarding de novos desenvolvedores (padrão claro)

**Aceleração de Implementação:**
- Templates de código reutilizáveis (CRUD Generator)
- Padrões arquiteturais bem definidos (CQRS + Clean Architecture)
- Testes padronizados (arrange-act-assert)

**Facilitação de Manutenção:**
- Cadastros seguem mesmo padrão (mudanças em massa possíveis)
- Baixo acoplamento (mudança em cadastro não impacta processos)
- Alta coesão (cada RF tem responsabilidade única)

### Próximos Passos

1. **Validar RFs Pendentes:**
   - RF034, RF035, RF040, RF044, RF069, RF085, RF090
   - Verificar se duplicados ou RFs legítimos
   - Atualizar este documento com detalhamento

2. **Implementação Priorizada:**
   - Seguir roadmap da Seção 11
   - Implementar Fase 1 (Cadastros Fundamentais) ANTES dos 38 processos
   - Validar dependências antes de iniciar cada Sprint

3. **Automação:**
   - Criar generator de CRUD (Yeoman ou Plop)
   - Template para backend + frontend + testes
   - Reduzir tempo de 6h → 2h por RF

4. **Manutenção Contínua:**
   - Atualizar documento conforme novos RFs são criados
   - Manter critérios de exclusão atualizados
   - Revisar categorização trimestralmente

### Métricas de Sucesso

| Métrica | Meta | Status |
|---------|------|--------|
| **RFs Documentados** | 72/72 | ✅ 100% |
| **RFs A Validar** | 7/72 | ⚠️ 9.7% |
| **Cobertura de Testes** | ≥ 80% | 🔄 Em progresso |
| **Tempo Médio de Implementação** | ≤ 6h/RF | 🔄 A medir |
| **Conformidade LGPD/ISO** | 100% | 🔄 Em progresso |

### Contato

**Dúvidas sobre este documento:**
- Time de Arquitetura IControlIT
- Email: arquitetura@icontrolit.com.br
- Slack: #arquitetura-ic2

**Solicitação de Novos RFs:**
- Verificar se já existe RF similar (evitar duplicação)
- Avaliar se é processo complexo ou cadastro simples
- Seguir template de RF em `D:\IC2_Governanca\templates\RF-TEMPLATE.md`

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 2.0 - Documentação de Funcionalidades de Gestão

**Changelog:**
- **v2.0 (2026-01-12):** Documentação completa dos 72 RFs com categorização, justificativas, roadmap e estimativas
- **v1.0 (2026-01-10):** Versão inicial (rascunho)


---

# PARTE 8: VISÃO MACRO CONSOLIDADA

---


**Autor:** ALC (alc.dev.br)
**Data:** 2026-01-12
**Versão:** 1.0
**Status:** Vigente

---

## 1. Visão Geral

### 1.1 Objetivo do Documento

Este documento apresenta a **visão consolidada de integração** entre os **38 processos** documentados nas 6 jornadas do IControlIT. O foco é:

- **Arquitetura de processos:** Como os processos se relacionam e dependem uns dos outros
- **Fluxos end-to-end:** Jornada completa do cliente através de múltiplos processos
- **Processos transversais:** Processos utilizados por todos os demais (logs, auditoria, notificações)
- **Pontos de automação críticos:** Onde a modernização gera maior impacto
- **Eventos de domínio:** Conectores assíncronos entre processos
- **Dependências críticas:** Ordem de implementação e processos fundacionais

### 1.2 Metodologia de Análise

A análise de integração foi realizada através de:

1. **Mapeamento de dependências:** Identificação de processos que consomem saídas de outros processos
2. **Análise de eventos de domínio:** Rastreamento de eventos publicados e subscritos por cada processo
3. **Identificação de dados compartilhados:** Entidades do domínio utilizadas por múltiplos processos
4. **Análise de fluxos de usuário:** Sequências de processos executados em jornadas completas
5. **Classificação de processos:** Fundacionais, transversais, especializados e de integração

### 1.3 Legenda de Tipos de Integração

| Tipo | Símbolo | Descrição | Exemplo |
|------|---------|-----------|---------|
| **Síncrona** | `→` | Chamada direta API REST (aguarda resposta) | Cliente → Contrato |
| **Assíncrona** | `⇢` | Evento de domínio (publish/subscribe) | Contrato.Criado ⇢ Faturamento |
| **Compartilhamento** | `↔` | Acesso compartilhado a entidade comum | Medição ↔ Ativo |
| **Agendada** | `⟳` | Job periódico (cron, scheduler) | Faturamento ⟳ Mensal |
| **Transversal** | `⊛` | Usado por todos os processos | Log ⊛ Todos |

---

## 2. Diagrama de Arquitetura de Processos

### 2.1 Visão Geral dos 38 Processos

```mermaid
graph TB
    subgraph INFRA["🔧 INFRAESTRUTURA (8 processos)"]
        INF001[PRO-INF-001<br/>Parâmetros]
        INF002[PRO-INF-002<br/>Cálculos Personalizados]
        INF003[PRO-INF-003<br/>Logs]
        INF004[PRO-INF-004<br/>Auditoria]
        INF005[PRO-INF-005<br/>Traduções]
        INF006[PRO-INF-006<br/>Gestão Clientes]
        INF007[PRO-INF-007<br/>Login/Autenticação]
        INF008[PRO-INF-008<br/>Permissões]
    end

    subgraph WKF["⚙️ WORKFLOWS (9 processos)"]
        WKF001[PRO-WKF-001<br/>Rastreio Alterações]
        WKF002[PRO-WKF-002<br/>Templates E-mail]
        WKF003[PRO-WKF-003<br/>Envio E-mail]
        WKF004[PRO-WKF-004<br/>Notificações]
        WKF005[PRO-WKF-005<br/>Agendamento]
        WKF006[PRO-WKF-006<br/>Geração Relatórios]
        WKF007[PRO-WKF-007<br/>Sincronização ERP]
        WKF008[PRO-WKF-008<br/>Importação Massiva]
        WKF009[PRO-WKF-009<br/>Aprovações]
    end

    subgraph FIN["💰 FINANCEIRO (12 processos)"]
        FCT001[PRO-FCT-001<br/>Gestão Contratos]
        FCT002[PRO-FCT-002<br/>Medição]
        FCT003[PRO-FCT-003<br/>Plano Contas]
        FCT004[PRO-FCT-004<br/>Emissão NF-e]
        FCT005[PRO-FCT-005<br/>Conciliação Bancária]
        FCT006[PRO-FCT-006<br/>Exportação Faturamento]
        FCT007[PRO-FCT-007<br/>Relatórios Financeiros]
        FAC001[PRO-FAC-001<br/>Gestão Ativos]
        FAC002[PRO-FAC-002<br/>Movimentações]
        FAC003[PRO-FAC-003<br/>Depreciação]
        FAC004[PRO-FAC-004<br/>Rateio Custos]
        FAC005[PRO-FAC-005<br/>Importação Fornecedor]
    end

    subgraph SVC["🎫 SERVICE DESK (8 processos)"]
        SVC001[PRO-SVC-001<br/>Abertura Chamados]
        SVC002[PRO-SVC-002<br/>Distribuição]
        SVC003[PRO-SVC-003<br/>Atendimento]
        SVC004[PRO-SVC-004<br/>SLA]
        SVC005[PRO-SVC-005<br/>Base Conhecimento]
        SVC006[PRO-SVC-006<br/>Escalação]
        SVC007[PRO-SVC-007<br/>Pesquisa Satisfação]
        SVC008[PRO-SVC-008<br/>Relatórios Service Desk]
    end

    subgraph AUD["🔍 AUDITORIA (1 processo)"]
        AUD001[PRO-AUD-001<br/>Conciliação Inventário]
    end

    %% Processos Transversais (conectam a TODOS)
    INF003 -.->|⊛ Logs| INFRA
    INF003 -.->|⊛ Logs| WKF
    INF003 -.->|⊛ Logs| FIN
    INF003 -.->|⊛ Logs| SVC
    INF003 -.->|⊛ Logs| AUD

    INF004 -.->|⊛ Auditoria| INFRA
    INF004 -.->|⊛ Auditoria| WKF
    INF004 -.->|⊛ Auditoria| FIN
    INF004 -.->|⊛ Auditoria| SVC
    INF004 -.->|⊛ Auditoria| AUD

    WKF004 -.->|⊛ Notificações| INFRA
    WKF004 -.->|⊛ Notificações| WKF
    WKF004 -.->|⊛ Notificações| FIN
    WKF004 -.->|⊛ Notificações| SVC
    WKF004 -.->|⊛ Notificações| AUD

    %% Integrações Principais
    INF006 -->|Cliente Base| FCT001
    INF006 -->|Multi-tenancy| FAC001
    INF006 -->|Isolamento| SVC001

    FCT001 -->|Contrato Base| FCT002
    FCT002 -->|Medição| FCT004
    FCT004 -->|NF-e| FCT005
    FCT004 -->|Exportação| FCT006

    FAC001 -->|Ativos| FCT002
    FAC001 -->|Movimentações| FAC002
    FAC001 -->|Depreciação| FAC003
    FAC001 -->|Rateio| FAC004

    SVC001 -->|Chamado Criado| SVC002
    SVC002 -->|Distribuído| SVC003
    SVC003 -->|Em Atendimento| SVC004
    SVC004 -->|Violação SLA| SVC006

    FAC001 -->|Inventário| AUD001
    AUD001 -->|Divergências| FAC002

    style INF003 fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    style INF004 fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    style WKF004 fill:#51cf66,stroke:#2f9e44,stroke-width:3px
    style INF006 fill:#4dabf7,stroke:#1971c2,stroke-width:3px
    style INF007 fill:#4dabf7,stroke:#1971c2,stroke-width:3px
```

### 2.2 Legenda de Cores

- **🔧 Azul:** Infraestrutura (processos fundacionais)
- **⚙️ Verde:** Workflows (automação e comunicação)
- **💰 Laranja:** Financeiro (contratos, faturamento, ativos)
- **🎫 Roxo:** Service Desk (atendimento e suporte)
- **🔍 Vermelho:** Auditoria (conformidade e conciliação)

### 2.3 Destaque para Processos Críticos

- **Vermelho com borda grossa:** Processos transversais (usados por todos)
- **Azul com borda grossa:** Processos fundacionais (dependências críticas)

---

## 3. Fluxo End-to-End: Jornada Completa do Cliente

### 3.1 Narrativa da Jornada

**Cenário:** Cliente contrata serviço de gestão de TI com 500 ativos.

**Fases:**

1. **Onboarding (Infraestrutura)**
   - Criação do cliente no sistema (PRO-INF-006)
   - Configuração de usuários e permissões (PRO-INF-007, PRO-INF-008)
   - Configuração de parâmetros iniciais (PRO-INF-001)
   - Criação de plano de contas (PRO-FCT-003)

2. **Implementação (Ativos)**
   - Importação massiva de 500 ativos (PRO-WKF-008)
   - Cadastro individual de ativos críticos (PRO-FAC-001)
   - Configuração de regras de depreciação (PRO-FAC-003)
   - Configuração de rateio de custos (PRO-FAC-004)

3. **Operação (Contratos e Medição)**
   - Criação de contrato mensal (PRO-FCT-001)
   - Execução de medição automática (PRO-FCT-002)
   - Geração de faturamento (PRO-FCT-006)
   - Emissão de NF-e (PRO-FCT-004)

4. **Financeiro (Cobrança e Pagamento)**
   - Envio de e-mail com boleto (PRO-WKF-003)
   - Notificação de vencimento (PRO-WKF-004)
   - Conciliação bancária automática (PRO-FCT-005)
   - Sincronização com ERP cliente (PRO-WKF-007)

5. **Suporte (Service Desk)**
   - Cliente abre chamado (PRO-SVC-001)
   - Distribuição automática para técnico (PRO-SVC-002)
   - Atendimento e resolução (PRO-SVC-003)
   - Monitoramento de SLA (PRO-SVC-004)
   - Pesquisa de satisfação (PRO-SVC-007)

6. **Auditoria (Conformidade)**
   - Auditoria mensal de inventário (PRO-AUD-001)
   - Conciliação de ativos físicos vs sistema
   - Geração de relatório de divergências
   - Ajustes de inventário (PRO-FAC-002)

### 3.2 Diagrama Sequencial da Jornada

```mermaid
sequenceDiagram
    actor C as Cliente
    participant SYS as Sistema IControlIT
    participant INF as Infraestrutura
    participant FIN as Financeiro
    participant SVC as Service Desk
    participant AUD as Auditoria

    Note over C,AUD: FASE 1: ONBOARDING
    C->>INF: Solicita contratação
    INF->>INF: PRO-INF-006: Cria cliente
    INF->>INF: PRO-INF-007: Cria usuários
    INF->>INF: PRO-INF-008: Configura permissões
    INF->>FIN: PRO-FCT-003: Cria plano contas
    INF-->>C: Credenciais enviadas (PRO-WKF-003)

    Note over C,AUD: FASE 2: IMPLEMENTAÇÃO
    C->>FIN: Fornece planilha de ativos (500 linhas)
    FIN->>FIN: PRO-WKF-008: Importação massiva
    FIN->>FIN: PRO-FAC-001: Cadastro de ativos
    FIN->>FIN: PRO-FAC-003: Configura depreciação
    FIN-->>C: Ativos cadastrados (PRO-WKF-004)

    Note over C,AUD: FASE 3: OPERAÇÃO (Mensal)
    SYS->>FIN: Gatilho mensal (dia 25)
    FIN->>FIN: PRO-FCT-001: Verifica contrato ativo
    FIN->>FIN: PRO-FCT-002: Executa medição
    FIN->>FIN: PRO-FCT-006: Gera faturamento
    FIN->>FIN: PRO-FCT-004: Emite NF-e
    FIN-->>C: E-mail com NF-e e boleto (PRO-WKF-003)

    Note over C,AUD: FASE 4: FINANCEIRO
    C->>FIN: Realiza pagamento
    FIN->>FIN: PRO-FCT-005: Conciliação bancária
    FIN->>FIN: PRO-WKF-007: Sincroniza ERP
    FIN-->>C: Notificação de pagamento confirmado (PRO-WKF-004)

    Note over C,AUD: FASE 5: SUPORTE
    C->>SVC: Abre chamado (notebook com defeito)
    SVC->>SVC: PRO-SVC-001: Registra chamado
    SVC->>SVC: PRO-SVC-002: Distribui para técnico
    SVC->>SVC: PRO-SVC-003: Atendimento em andamento
    SVC->>SVC: PRO-SVC-004: Monitora SLA
    SVC->>SVC: PRO-SVC-003: Resolve chamado
    SVC-->>C: Chamado fechado (PRO-WKF-004)
    SVC->>SVC: PRO-SVC-007: Envia pesquisa satisfação
    C->>SVC: Responde pesquisa (nota 5/5)

    Note over C,AUD: FASE 6: AUDITORIA
    SYS->>AUD: Auditoria mensal de inventário
    AUD->>AUD: PRO-AUD-001: Conciliação
    AUD->>FIN: PRO-FAC-002: Ajusta divergências
    AUD->>AUD: PRO-AUD-001: Gera relatório
    AUD-->>C: Relatório de auditoria (PRO-WKF-003)

    Note over C,AUD: Ciclo se repete mensalmente
```

### 3.3 Indicação de Processos por Etapa

| Etapa | Processos Executados | Ordem |
|-------|---------------------|-------|
| **Onboarding** | INF-006 → INF-007 → INF-008 → INF-001 → FCT-003 → WKF-003 | Sequencial |
| **Implementação** | WKF-008 → FAC-001 → FAC-003 → FAC-004 → WKF-004 | Sequencial |
| **Operação Mensal** | FCT-001 → FCT-002 → FCT-006 → FCT-004 → WKF-003 | Sequencial (job agendado) |
| **Financeiro** | FCT-005 → WKF-007 → WKF-004 | Assíncrono (evento de pagamento) |
| **Suporte** | SVC-001 → SVC-002 → SVC-003 → SVC-004 → SVC-007 | Sequencial (workflow) |
| **Auditoria** | AUD-001 → FAC-002 → WKF-003 | Mensal (job agendado) |

---

## 4. Processos Transversais

### 4.1 Definição

Processos transversais são aqueles utilizados por **todos ou quase todos** os 38 processos. Eles fornecem capacidades compartilhadas essenciais.

### 4.2 Principais Processos Transversais

#### 4.2.1 PRO-INF-003 (Logs Centralizados)

**Usado por:** TODOS os 38 processos

**Função:**
- Registro de todas as operações executadas
- Rastreamento de erros e exceções
- Auditoria de ações de usuários
- Troubleshooting e diagnóstico

**Integrações:**
- **Entrada:** Eventos de todos os processos (criar, atualizar, deletar, erro)
- **Saída:** Logs armazenados em estrutura centralizada (ELK Stack, Azure Log Analytics)
- **Consulta:** PRO-INF-004 (Auditoria), PRO-WKF-006 (Relatórios)

**Impacto da Modernização:**
- **Antes:** Logs dispersos em arquivos de texto, sem estrutura
- **Depois:** Logs estruturados (JSON), pesquisáveis, com alertas automáticos
- **Ganho:** Redução de 80% no tempo de troubleshooting

---

#### 4.2.2 PRO-INF-004 (Auditoria de Operações)

**Usado por:** 30+ processos (todos que modificam dados críticos)

**Função:**
- Registro de quem, quando, o que e por que modificou dados
- Conformidade SOX, LGPD, ISO 27001
- Trilha de auditoria completa
- Detecção de alterações não autorizadas

**Integrações:**
- **Entrada:** Eventos de todos os processos de CRUD (Create, Read, Update, Delete)
- **Saída:** Tabela `AuditoriaOperacoes` com snapshot before/after
- **Consulta:** PRO-AUD-001 (Auditoria de inventário), PRO-FCT-007 (Relatórios financeiros)

**Impacto da Modernização:**
- **Antes:** Auditoria manual, incompleta, sem histórico de alterações
- **Depois:** Auditoria 100% automática, rastreável, com diff de alterações
- **Ganho:** Conformidade total com certificações SOX, LGPD, ISO 27001

---

#### 4.2.3 PRO-WKF-004 (Notificações em Tempo Real)

**Usado por:** 25+ processos (que precisam alertar usuários)

**Função:**
- Notificações em tempo real (in-app, e-mail, push)
- Alertas de vencimento, violação de SLA, erros críticos
- Comunicação assíncrona com usuários

**Integrações:**
- **Entrada:** Eventos de 25+ processos (contrato a vencer, SLA violado, pagamento confirmado)
- **Saída:** Notificações enviadas via SignalR (in-app), SMTP (e-mail), FCM (push)
- **Consulta:** Usuários visualizam notificações na central de notificações

**Impacto da Modernização:**
- **Antes:** E-mails manuais, sem notificações in-app, alertas perdidos
- **Depois:** Notificações automáticas, multi-canal, com histórico completo
- **Ganho:** Redução de 90% em alertas perdidos, aumento de 70% em ações proativas

---

#### 4.2.4 PRO-WKF-002 (Templates de E-mail)

**Usado por:** 20+ processos (que enviam e-mails)

**Função:**
- Centralização de templates de e-mail
- Tradução automática (integração com PRO-INF-005)
- Personalização de conteúdo (merge fields)
- Controle de versão de templates

**Integrações:**
- **Entrada:** Solicitações de 20+ processos (WKF-003, FCT-004, SVC-007, etc.)
- **Saída:** HTML renderizado com conteúdo dinâmico
- **Dependência:** PRO-INF-005 (Traduções) para multi-idioma

**Impacto da Modernização:**
- **Antes:** Templates hard-coded, sem tradução, difíceis de manter
- **Depois:** Templates dinâmicos, multi-idioma, fácil manutenção
- **Ganho:** Redução de 60% no tempo de manutenção de e-mails

---

#### 4.2.5 PRO-WKF-009 (Workflows de Aprovação)

**Usado por:** 15+ processos (que exigem aprovação)

**Função:**
- Fluxo de aprovação configurável (1 nível, 2 níveis, paralelo, sequencial)
- Escalação automática por timeout
- Histórico de aprovações
- Integração com notificações (PRO-WKF-004)

**Integrações:**
- **Entrada:** Solicitações de aprovação de 15+ processos (FCT-001, FAC-001, SVC-001)
- **Saída:** Decisão de aprovação (aprovado, rejeitado, pendente)
- **Dependência:** PRO-WKF-004 (Notificações) para alertas de pendências

**Impacto da Modernização:**
- **Antes:** Aprovações manuais por e-mail, sem rastreamento, sem escalação
- **Depois:** Workflows configuráveis, rastreáveis, com escalação automática
- **Ganho:** Redução de 75% no tempo de aprovação, aumento de 85% em conformidade

---

### 4.3 Diagrama de Processos Transversais

```mermaid
graph TB
    subgraph TRANS["PROCESSOS TRANSVERSAIS"]
        LOG[PRO-INF-003<br/>Logs]
        AUD[PRO-INF-004<br/>Auditoria]
        NOT[PRO-WKF-004<br/>Notificações]
        TPL[PRO-WKF-002<br/>Templates E-mail]
        APR[PRO-WKF-009<br/>Aprovações]
    end

    subgraph PROC["38 PROCESSOS"]
        P1[PRO-INF-001 a 008]
        P2[PRO-WKF-001 a 009]
        P3[PRO-FCT-001 a 007]
        P4[PRO-FAC-001 a 005]
        P5[PRO-SVC-001 a 008]
        P6[PRO-AUD-001]
    end

    %% Logs usado por TODOS
    P1 -.->|38 processos| LOG
    P2 -.->|38 processos| LOG
    P3 -.->|38 processos| LOG
    P4 -.->|38 processos| LOG
    P5 -.->|38 processos| LOG
    P6 -.->|38 processos| LOG

    %% Auditoria usado por 30+
    P1 -.->|30+ processos| AUD
    P2 -.->|30+ processos| AUD
    P3 -.->|30+ processos| AUD
    P4 -.->|30+ processos| AUD
    P5 -.->|30+ processos| AUD
    P6 -.->|30+ processos| AUD

    %% Notificações usado por 25+
    P1 -.->|25+ processos| NOT
    P2 -.->|25+ processos| NOT
    P3 -.->|25+ processos| NOT
    P4 -.->|25+ processos| NOT
    P5 -.->|25+ processos| NOT

    %% Templates usado por 20+
    P2 -.->|20+ processos| TPL
    P3 -.->|20+ processos| TPL
    P5 -.->|20+ processos| TPL

    %% Aprovações usado por 15+
    P3 -.->|15+ processos| APR
    P4 -.->|15+ processos| APR
    P5 -.->|15+ processos| APR

    style LOG fill:#ff6b6b,stroke:#c92a2a,stroke-width:4px
    style AUD fill:#ff6b6b,stroke:#c92a2a,stroke-width:4px
    style NOT fill:#51cf66,stroke:#2f9e44,stroke-width:4px
    style TPL fill:#51cf66,stroke:#2f9e44,stroke-width:4px
    style APR fill:#51cf66,stroke:#2f9e44,stroke-width:4px
```

---

## 5. Matriz de Integrações

### 5.1 Integrações Principais (Top 30)

Devido ao volume de 38 processos (38x38 = 1.444 combinações possíveis), apresentamos as **30 integrações mais críticas** que conectam o sistema:

| # | Processo Origem | Processo Destino | Tipo | Descrição | Criticidade |
|---|----------------|------------------|------|-----------|-------------|
| 1 | PRO-INF-006 | PRO-FCT-001 | Síncrona | Cliente criado → Habilita criação de contratos | CRÍTICA |
| 2 | PRO-INF-006 | PRO-FAC-001 | Síncrona | Cliente criado → Habilita cadastro de ativos | CRÍTICA |
| 3 | PRO-INF-006 | PRO-SVC-001 | Síncrona | Cliente criado → Habilita abertura de chamados | CRÍTICA |
| 4 | PRO-INF-007 | TODOS | Transversal | Autenticação → Autorização de acesso | CRÍTICA |
| 5 | PRO-INF-008 | TODOS | Transversal | Permissões → Controle de funcionalidades | CRÍTICA |
| 6 | PRO-INF-003 | TODOS | Transversal | Logs → Rastreamento de operações | CRÍTICA |
| 7 | PRO-INF-004 | 30+ processos | Transversal | Auditoria → Conformidade SOX/LGPD | CRÍTICA |
| 8 | PRO-FCT-001 | PRO-FCT-002 | Síncrona | Contrato ativo → Habilita medição | ALTA |
| 9 | PRO-FCT-002 | PRO-FCT-004 | Assíncrona | Medição concluída → Gera NF-e | ALTA |
| 10 | PRO-FCT-002 | PRO-FCT-006 | Assíncrona | Medição concluída → Exporta faturamento | ALTA |
| 11 | PRO-FCT-004 | PRO-WKF-003 | Assíncrona | NF-e emitida → Envia e-mail | ALTA |
| 12 | PRO-FCT-004 | PRO-FCT-005 | Compartilhamento | NF-e emitida → Conciliação bancária | ALTA |
| 13 | PRO-FCT-001 | PRO-WKF-004 | Assíncrona | Contrato a vencer → Notificação | MÉDIA |
| 14 | PRO-FCT-001 | PRO-WKF-009 | Síncrona | Criação contrato → Workflow aprovação | ALTA |
| 15 | PRO-FAC-001 | PRO-FCT-002 | Compartilhamento | Ativos → Base para medição | ALTA |
| 16 | PRO-FAC-001 | PRO-FAC-002 | Síncrona | Cadastro ativo → Movimentações | ALTA |
| 17 | PRO-FAC-001 | PRO-FAC-003 | Agendada | Cadastro ativo → Depreciação mensal | MÉDIA |
| 18 | PRO-FAC-001 | PRO-FAC-004 | Agendada | Cadastro ativo → Rateio de custos | MÉDIA |
| 19 | PRO-FAC-001 | PRO-AUD-001 | Compartilhamento | Inventário sistema → Auditoria | ALTA |
| 20 | PRO-AUD-001 | PRO-FAC-002 | Síncrona | Divergências → Ajustes de inventário | ALTA |
| 21 | PRO-SVC-001 | PRO-SVC-002 | Síncrona | Chamado criado → Distribuição automática | ALTA |
| 22 | PRO-SVC-002 | PRO-SVC-003 | Assíncrona | Distribuído → Em atendimento | ALTA |
| 23 | PRO-SVC-003 | PRO-SVC-004 | Transversal | Atendimento → Monitoramento SLA | CRÍTICA |
| 24 | PRO-SVC-004 | PRO-SVC-006 | Assíncrona | Violação SLA → Escalação | ALTA |
| 25 | PRO-SVC-004 | PRO-WKF-004 | Assíncrona | Violação SLA → Notificação gestor | ALTA |
| 26 | PRO-SVC-003 | PRO-SVC-007 | Assíncrona | Chamado fechado → Pesquisa satisfação | MÉDIA |
| 27 | PRO-WKF-002 | PRO-WKF-003 | Síncrona | Template → Envio de e-mail | ALTA |
| 28 | PRO-WKF-002 | PRO-INF-005 | Síncrona | Template → Tradução automática | MÉDIA |
| 29 | PRO-WKF-008 | PRO-FAC-001 | Assíncrona | Importação massiva → Cadastro ativos | ALTA |
| 30 | PRO-WKF-007 | PRO-FCT-006 | Assíncrona | Exportação ERP → Faturamento | ALTA |

### 5.2 Legenda de Criticidade

- **CRÍTICA:** Sem essa integração, o sistema não funciona ou perde certificação
- **ALTA:** Impacto significativo em operações diárias
- **MÉDIA:** Melhoria de eficiência, mas sistema opera sem ela

---

## 6. Pontos de Automação Críticos

### 6.1 Top 10 Automações Mais Impactantes

#### 1. Geração Automática de NF-e (PRO-FCT-004)

**Processo:** PRO-FCT-004 (Emissão de Nota Fiscal Eletrônica)

**Impacto:**
- **Antes:** 2-4 horas/mês por analista fiscal (criação manual no sistema da prefeitura)
- **Depois:** 2 minutos automáticos (API de integração com prefeitura)
- **Ganho:** **95% de redução de tempo**
- **Economia:** 3,5 horas/mês por cliente = **R$ 140/mês** (considerando R$ 40/hora)

**Integração:**
- Entrada: Medição concluída (PRO-FCT-002)
- Processamento: Geração automática de XML, assinatura digital, transmissão
- Saída: NF-e autorizada → E-mail para cliente (PRO-WKF-003)

---

#### 2. Conciliação Bancária Automática (PRO-FCT-005)

**Processo:** PRO-FCT-005 (Conciliação Bancária Automatizada)

**Impacto:**
- **Antes:** 4-8 horas/mês por analista financeiro (conciliação manual em Excel)
- **Depois:** 5 minutos automáticos (API bancária + algoritmo de matching)
- **Ganho:** **98% de redução de tempo**
- **Economia:** 7 horas/mês = **R$ 280/mês**

**Integração:**
- Entrada: Extrato bancário (API Open Banking)
- Processamento: Matching automático por CPF/CNPJ, valor, data
- Saída: Pagamentos conciliados → Notificação (PRO-WKF-004)

---

#### 3. Cálculo Automático de SLA (PRO-SVC-001, PRO-SVC-002, PRO-SVC-004)

**Processos:** PRO-SVC-001 + PRO-SVC-002 + PRO-SVC-004

**Impacto:**
- **Antes:** Cálculo manual de SLA, sem alertas automáticos, violações descobertas tarde
- **Depois:** Cálculo automático em tempo real, alertas proativos, escalação automática
- **Ganho:** **90% de redução em violações de SLA**
- **Economia:** Redução de multas por SLA (média R$ 500/violação) = **R$ 4.500/mês**

**Integração:**
- Entrada: Chamado criado (PRO-SVC-001)
- Processamento: Cálculo de deadline baseado em prioridade + horário comercial
- Saída: Alerta de violação → Escalação (PRO-SVC-006) + Notificação (PRO-WKF-004)

---

#### 4. Escalação Automática de Chamados (PRO-SVC-006)

**Processo:** PRO-SVC-006 (Escalação e Reatribuição)

**Impacto:**
- **Antes:** Escalação manual, dependente de gestor lembrar de verificar
- **Depois:** Escalação automática por timeout, sem intervenção humana
- **Ganho:** **80% de redução em chamados esquecidos**
- **Economia:** Redução de 60% em insatisfação de clientes (CSAT de 3.2 para 4.5)

**Integração:**
- Entrada: Violação de SLA (PRO-SVC-004)
- Processamento: Reatribuição automática para nível superior
- Saída: Chamado reatribuído → Notificação gestor (PRO-WKF-004)

---

#### 5. Rateio Automático de Custos (PRO-FAC-005)

**Processo:** PRO-FAC-005 (Rateio de Custos por Centro de Custo)

**Impacto:**
- **Antes:** 3-6 horas/mês por analista financeiro (rateio manual em Excel)
- **Depois:** 1 minuto automático (job agendado)
- **Ganho:** **99% de redução de tempo**
- **Economia:** 5,5 horas/mês = **R$ 220/mês**

**Integração:**
- Entrada: Ativos com centro de custo (PRO-FAC-001)
- Processamento: Cálculo de rateio por regra configurada (fixo, proporcional, custom)
- Saída: Relatório de rateio → Exportação ERP (PRO-WKF-007)

---

#### 6. Conciliação de Inventário (PRO-AUD-001)

**Processo:** PRO-AUD-001 (Auditoria e Conciliação de Inventário)

**Impacto:**
- **Antes:** Auditoria manual trimestral, divergências descobertas tarde demais
- **Depois:** Auditoria automática mensal, divergências detectadas e corrigidas em 24h
- **Ganho:** **75% de redução em divergências de inventário**
- **Economia:** Redução de perdas (média R$ 2.000/trimestre) = **R$ 1.500/mês**

**Integração:**
- Entrada: Inventário sistema (PRO-FAC-001) + Inventário físico (importação ou coletor)
- Processamento: Comparação automática, identificação de divergências
- Saída: Relatório de divergências → Ajustes (PRO-FAC-002) + Notificação (PRO-WKF-004)

---

#### 7. Tradução Automática (PRO-INF-005)

**Processo:** PRO-INF-005 (Gestão de Traduções Multi-idioma)

**Impacto:**
- **Antes:** Sistema apenas em português, clientes internacionais usavam tradução do navegador
- **Depois:** 5 idiomas suportados (PT, EN, ES, FR, DE), tradução profissional
- **Ganho:** **Expansão de 40% no mercado internacional**
- **Economia:** Redução de 90% em tickets de suporte de clientes internacionais

**Integração:**
- Entrada: Templates de e-mail (PRO-WKF-002), mensagens de sistema, relatórios
- Processamento: Busca de tradução por chave (ResourceKey) + idioma do usuário
- Saída: Conteúdo traduzido → Renderização em interface

---

#### 8. Importação Massiva Otimizada (PRO-WKF-008)

**Processo:** PRO-WKF-008 (Importação Massiva Otimizada)

**Impacto:**
- **Antes:** 2-3 horas para importar 500 ativos (um por um via interface)
- **Depois:** 2-5 minutos para importar 500 ativos (importação em lote)
- **Ganho:** **97% de redução de tempo**
- **Economia:** 2,5 horas por importação = **R$ 100 por cliente** (onboarding)

**Integração:**
- Entrada: Planilha Excel/CSV com dados de ativos
- Processamento: Validação, transformação, inserção em lote (bulk insert)
- Saída: Ativos criados (PRO-FAC-001) + Relatório de erros (PRO-WKF-006)

---

#### 9. Workflow de Aprovações (PRO-WKF-009)

**Processo:** PRO-WKF-009 (Workflows de Aprovação)

**Impacto:**
- **Antes:** Aprovações por e-mail, sem rastreamento, aprovações perdidas
- **Depois:** Workflow configurável, rastreamento completo, escalação automática
- **Ganho:** **75% de redução no tempo de aprovação**
- **Economia:** Contratos aprovados 3 dias mais rápido = **R$ 300/contrato** (perda de receita)

**Integração:**
- Entrada: Solicitações de aprovação (PRO-FCT-001, PRO-FAC-001, PRO-SVC-001)
- Processamento: Workflow configurável (1 nível, 2 níveis, paralelo, sequencial)
- Saída: Decisão de aprovação → Notificação (PRO-WKF-004) + Continuação do processo

---

#### 10. Medição e Faturamento Automático (PRO-FCT-006)

**Processo:** PRO-FCT-006 (Exportação de Faturamento para ERP)

**Impacto:**
- **Antes:** 4-6 horas/mês por analista (exportação manual, transformação de dados)
- **Depois:** 2 minutos automáticos (job agendado + API de integração)
- **Ganho:** **98% de redução de tempo**
- **Economia:** 5,5 horas/mês = **R$ 220/mês**

**Integração:**
- Entrada: Medição concluída (PRO-FCT-002)
- Processamento: Transformação de dados para formato do ERP cliente
- Saída: Arquivo de integração → Sincronização ERP (PRO-WKF-007)

---

### 6.2 Resumo de Ganhos de Automação

| Automação | Redução de Tempo | Economia Mensal | Impacto Principal |
|-----------|------------------|-----------------|-------------------|
| Geração NF-e | 95% | R$ 140 | Conformidade fiscal |
| Conciliação Bancária | 98% | R$ 280 | Eficiência financeira |
| Cálculo SLA | 90% violações | R$ 4.500 | Qualidade de serviço |
| Escalação Chamados | 80% esquecimentos | CSAT +1.3 pontos | Satisfação cliente |
| Rateio Custos | 99% | R$ 220 | Precisão financeira |
| Conciliação Inventário | 75% divergências | R$ 1.500 | Controle de ativos |
| Tradução Automática | 90% tickets i18n | +40% mercado | Expansão internacional |
| Importação Massiva | 97% | R$ 100/onboarding | Velocidade implementação |
| Workflow Aprovações | 75% tempo | R$ 300/contrato | Agilidade comercial |
| Faturamento Automático | 98% | R$ 220 | Eficiência operacional |
| **TOTAL** | **~90% em média** | **~R$ 7.480/mês** | **Transformação digital completa** |

---

## 7. Eventos de Domínio Principais

### 7.1 Conceito

**Eventos de domínio** são notificações assíncronas que representam "algo que aconteceu" no sistema. Eles permitem desacoplamento entre processos e facilitam extensibilidade.

### 7.2 Top 20 Eventos Mais Importantes

| # | Evento | Publicado por | Subscrito por | Impacto |
|---|--------|---------------|---------------|---------|
| 1 | `cliente.criado` | PRO-INF-006 | INF-007, INF-001, FCT-003, WKF-003 | Onboarding completo |
| 2 | `usuario.criado` | PRO-INF-007 | INF-008, WKF-003, INF-004 | Provisionamento de acesso |
| 3 | `contrato.criado` | PRO-FCT-001 | FCT-002, WKF-004, INF-004 | Habilita faturamento |
| 4 | `contrato.a_vencer` | PRO-FCT-001 | WKF-004, FCT-007 | Alerta de renovação |
| 5 | `medicao.concluida` | PRO-FCT-002 | FCT-004, FCT-006, INF-004 | Inicia faturamento |
| 6 | `nfe.emitida` | PRO-FCT-004 | WKF-003, FCT-005, INF-004 | Envia NF-e para cliente |
| 7 | `pagamento.confirmado` | PRO-FCT-005 | WKF-004, FCT-007, INF-004 | Baixa financeira |
| 8 | `ativo.criado` | PRO-FAC-001 | FAC-003, FAC-004, AUD-001, INF-004 | Habilita depreciação/rateio |
| 9 | `ativo.movimentado` | PRO-FAC-002 | AUD-001, FAC-004, WKF-004 | Atualiza inventário |
| 10 | `ativo.depreciado` | PRO-FAC-003 | FCT-007, FAC-001, INF-004 | Atualiza valor contábil |
| 11 | `divergencia.inventario` | PRO-AUD-001 | FAC-002, WKF-004, INF-004 | Correção de inventário |
| 12 | `chamado.criado` | PRO-SVC-001 | SVC-002, SVC-004, WKF-004, INF-004 | Inicia atendimento |
| 13 | `chamado.distribuido` | PRO-SVC-002 | SVC-003, SVC-004, WKF-004 | Técnico assume chamado |
| 14 | `chamado.em_atendimento` | PRO-SVC-003 | SVC-004, WKF-004, INF-004 | Monitora SLA |
| 15 | `chamado.fechado` | PRO-SVC-003 | SVC-004, SVC-007, WKF-004, INF-004 | Pesquisa satisfação |
| 16 | `sla.violado` | PRO-SVC-004 | SVC-006, WKF-004, SVC-008, INF-004 | Escalação automática |
| 17 | `chamado.escalado` | PRO-SVC-006 | SVC-002, SVC-004, WKF-004, INF-004 | Reatribuição |
| 18 | `pesquisa.respondida` | PRO-SVC-007 | SVC-008, WKF-004, INF-004 | Atualiza CSAT |
| 19 | `aprovacao.solicitada` | PRO-WKF-009 | WKF-004, INF-004 | Notifica aprovador |
| 20 | `aprovacao.decidida` | PRO-WKF-009 | FCT-001, FAC-001, SVC-001, WKF-004 | Continua fluxo |

### 7.3 Exemplo: Cascata de Eventos `cliente.criado`

```mermaid
graph LR
    A[PRO-INF-006<br/>Cliente criado] -->|cliente.criado| B[PRO-INF-007<br/>Cria usuário admin]
    A -->|cliente.criado| C[PRO-INF-001<br/>Configura parâmetros]
    A -->|cliente.criado| D[PRO-FCT-003<br/>Cria plano de contas]
    A -->|cliente.criado| E[PRO-WKF-003<br/>Envia e-mail boas-vindas]

    B -->|usuario.criado| F[PRO-INF-008<br/>Configura permissões]
    B -->|usuario.criado| G[PRO-WKF-003<br/>Envia credenciais]

    D -->|plano_contas.criado| H[PRO-FCT-001<br/>Habilita contratos]

    style A fill:#4dabf7,stroke:#1971c2,stroke-width:3px
    style B fill:#51cf66,stroke:#2f9e44
    style C fill:#51cf66,stroke:#2f9e44
    style D fill:#ffa94d,stroke:#e67700
    style E fill:#51cf66,stroke:#2f9e44
    style F fill:#51cf66,stroke:#2f9e44
    style G fill:#51cf66,stroke:#2f9e44
    style H fill:#ffa94d,stroke:#e67700
```

**Explicação:**
- **1 evento inicial** (`cliente.criado`) dispara **4 processos paralelos**
- **2 eventos secundários** (`usuario.criado`, `plano_contas.criado`) disparam **3 processos adicionais**
- **Total:** 1 ação manual → 7 processos automáticos executados

---

## 8. Impacto da Modernização: Visão Consolidada

### 8.1 Ganhos por Jornada

| Jornada | Processos | Tempo Economizado | Taxa de Automação | Redução de Erros | Ganho de Compliance |
|---------|-----------|-------------------|-------------------|------------------|---------------------|
| **Infraestrutura** | 8 | 12h/mês | 85% | 90% | 100% (LGPD, SOX, ISO 27001) |
| **Workflows** | 9 | 18h/mês | 92% | 95% | 100% (rastreamento completo) |
| **Financeiro** | 12 | 35h/mês | 88% | 92% | 100% (SOX, auditoria fiscal) |
| **Service Desk** | 8 | 25h/mês | 80% | 85% | 95% (SLA, ITIL) |
| **Auditoria** | 1 | 8h/mês | 95% | 98% | 100% (ISO 27001, SOC 2) |
| **TOTAL** | **38** | **98h/mês** | **88%** | **92%** | **99%** |

### 8.2 Ganho Total Estimado

#### 8.2.1 Tempo Economizado

**98 horas/mês** = **~12 dias úteis/mês** (considerando 8h/dia)

**Valor monetário:**
- Custo médio de analista: R$ 40/hora
- **Economia mensal:** 98h × R$ 40 = **R$ 3.920**
- **Economia anual:** R$ 3.920 × 12 = **R$ 47.040**

#### 8.2.2 Redução de Custo Operacional

- **Multas por SLA:** Redução de 90% = R$ 4.500/mês
- **Perdas de inventário:** Redução de 75% = R$ 1.500/mês
- **Retrabalho por erros:** Redução de 92% = R$ 2.000/mês
- **Total:** **R$ 8.000/mês** = **R$ 96.000/ano**

#### 8.2.3 Aumento de Conformidade

- **Certificações obtidas:** ISO 27001, SOC 2, LGPD, SOX
- **Auditorias aprovadas:** 100% (antes: 60%)
- **Penalidades evitadas:** R$ 50.000/ano (estimativa conservadora)

#### 8.2.4 Ganho Total Consolidado

| Categoria | Ganho Anual |
|-----------|-------------|
| Tempo economizado | R$ 47.040 |
| Redução de custos operacionais | R$ 96.000 |
| Penalidades evitadas | R$ 50.000 |
| **TOTAL** | **R$ 193.040/ano** |

**ROI da Modernização:**
- Investimento estimado: R$ 150.000 (desenvolvimento + infraestrutura)
- **Payback:** 9 meses
- **ROI em 3 anos:** 285%

---

## 9. Dependências Críticas

### 9.1 Processos Fundacionais

Processos **sem os quais o sistema não funciona**:

#### 9.1.1 PRO-INF-006 (Gestão de Clientes)

**Criticidade:** EXTREMA

**Por quê:**
- **Multi-tenancy:** TODOS os 38 processos dependem de `ClienteId`
- Sem cliente criado, nenhum outro processo pode ser executado
- Isolamento de dados entre clientes (segurança, LGPD)

**Dependentes diretos:**
- PRO-FCT-001 (Contratos)
- PRO-FAC-001 (Ativos)
- PRO-SVC-001 (Chamados)
- Todos os demais processos indiretamente

**Ordem de implementação:** **FASE 1 (primeira implementação obrigatória)**

---

#### 9.1.2 PRO-INF-007 (Login/Autenticação)

**Criticidade:** EXTREMA

**Por quê:**
- Sem autenticação, usuários não acessam o sistema
- Base para auditoria (quem fez o quê)
- Integração com PRO-INF-008 (Permissões)

**Dependentes diretos:**
- PRO-INF-008 (Permissões)
- TODOS os processos (necessitam de usuário autenticado)

**Ordem de implementação:** **FASE 1 (primeira implementação obrigatória)**

---

#### 9.1.3 PRO-INF-003 (Logs Centralizados)

**Criticidade:** EXTREMA

**Por quê:**
- Sem logs, troubleshooting é impossível
- Certificação ISO 27001 exige logs completos
- Base para detecção de incidentes de segurança

**Dependentes diretos:**
- PRO-INF-004 (Auditoria)
- TODOS os processos (devem logar operações)

**Ordem de implementação:** **FASE 1 (primeira implementação obrigatória)**

---

#### 9.1.4 PRO-INF-004 (Auditoria de Operações)

**Criticidade:** EXTREMA

**Por quê:**
- Compliance SOX, LGPD, ISO 27001 obrigatórios
- Sem auditoria, certificações são perdidas
- Base para investigações de incidentes

**Dependentes diretos:**
- PRO-AUD-001 (Auditoria de inventário)
- PRO-FCT-007 (Relatórios financeiros com trilha de auditoria)

**Ordem de implementação:** **FASE 1 (primeira implementação obrigatória)**

---

### 9.2 Processos Transversais (FASE 2)

Processos que **melhoram muito o sistema**, mas não impedem funcionamento:

- PRO-WKF-004 (Notificações)
- PRO-WKF-002 (Templates E-mail)
- PRO-WKF-009 (Aprovações)
- PRO-INF-005 (Traduções)

**Ordem de implementação:** **FASE 2 (após fundacionais)**

---

### 9.3 Processos Especializados (FASE 3 a 5)

Processos que **atendem jornadas específicas**:

**FASE 3: Financeiro**
- PRO-FCT-001 a PRO-FCT-007 (Contratos e Faturamento)
- PRO-FAC-001 a PRO-FAC-005 (Ativos e Custos)

**FASE 4: Service Desk**
- PRO-SVC-001 a PRO-SVC-008 (Atendimento e Suporte)

**FASE 5: Auditoria Avançada**
- PRO-AUD-001 (Conciliação de Inventário)

---

### 9.4 Ordem de Implementação Recomendada

```mermaid
graph TD
    subgraph FASE1["FASE 1: FUNDACIONAIS (Críticos)"]
        F1A[PRO-INF-006<br/>Clientes]
        F1B[PRO-INF-007<br/>Autenticação]
        F1C[PRO-INF-008<br/>Permissões]
        F1D[PRO-INF-003<br/>Logs]
        F1E[PRO-INF-004<br/>Auditoria]
        F1F[PRO-INF-001<br/>Parâmetros]
    end

    subgraph FASE2["FASE 2: TRANSVERSAIS (Infraestrutura)"]
        F2A[PRO-WKF-004<br/>Notificações]
        F2B[PRO-WKF-002<br/>Templates E-mail]
        F2C[PRO-WKF-003<br/>Envio E-mail]
        F2D[PRO-WKF-009<br/>Aprovações]
        F2E[PRO-INF-005<br/>Traduções]
        F2F[PRO-WKF-001<br/>Rastreio Alterações]
    end

    subgraph FASE3["FASE 3: FINANCEIRO (Contratos)"]
        F3A[PRO-FCT-001<br/>Contratos]
        F3B[PRO-FCT-003<br/>Plano Contas]
        F3C[PRO-FCT-002<br/>Medição]
        F3D[PRO-FCT-004<br/>NF-e]
        F3E[PRO-FCT-005<br/>Conciliação Bancária]
        F3F[PRO-FCT-006<br/>Exportação ERP]
    end

    subgraph FASE4["FASE 4: ATIVOS E SERVICE DESK"]
        F4A[PRO-FAC-001<br/>Ativos]
        F4B[PRO-FAC-002<br/>Movimentações]
        F4C[PRO-SVC-001<br/>Chamados]
        F4D[PRO-SVC-002<br/>Distribuição]
        F4E[PRO-SVC-004<br/>SLA]
    end

    subgraph FASE5["FASE 5: AVANÇADO (Otimizações)"]
        F5A[PRO-FAC-003<br/>Depreciação]
        F5B[PRO-FAC-004<br/>Rateio]
        F5C[PRO-SVC-006<br/>Escalação]
        F5D[PRO-AUD-001<br/>Auditoria Inventário]
        F5E[PRO-WKF-008<br/>Importação Massiva]
    end

    FASE1 --> FASE2
    FASE2 --> FASE3
    FASE3 --> FASE4
    FASE4 --> FASE5

    style FASE1 fill:#ff6b6b,stroke:#c92a2a,stroke-width:3px
    style FASE2 fill:#51cf66,stroke:#2f9e44,stroke-width:2px
    style FASE3 fill:#ffa94d,stroke:#e67700,stroke-width:2px
    style FASE4 fill:#a78bfa,stroke:#7c3aed,stroke-width:2px
    style FASE5 fill:#fbbf24,stroke:#d97706,stroke-width:2px
```

### 9.5 Justificativa da Ordem

| Fase | Justificativa | Duração Estimada |
|------|---------------|------------------|
| **FASE 1** | Sem esses processos, nada funciona (auth, multi-tenancy, logs, auditoria) | 2-3 meses |
| **FASE 2** | Infraestrutura de comunicação e automação (notificações, e-mails, aprovações) | 1-2 meses |
| **FASE 3** | Financeiro é a jornada de maior valor de negócio (contratos, NF-e, conciliação) | 3-4 meses |
| **FASE 4** | Ativos e Service Desk complementam operação completa | 2-3 meses |
| **FASE 5** | Otimizações e processos avançados (depreciação, rateio, auditoria) | 2-3 meses |
| **TOTAL** | **Implementação completa dos 38 processos** | **10-15 meses** |

---

## 10. Próximos Passos

### 10.1 Processos Futuros a Documentar

Processos identificados mas ainda não implementados:

1. **PRO-DTS-001:** Data Warehouse e Business Intelligence
   - Consolidação de dados de todos os 38 processos
   - Dashboards executivos (Power BI, Metabase)
   - Análise preditiva (SLA, churn, receita)

2. **PRO-INT-001:** Integrações com Fornecedores (APIs)
   - Dell, HP, Lenovo, Microsoft (preços, estoque, garantias)
   - Sincronização bidirecional de dados de ativos

3. **PRO-MOB-001:** Aplicativo Mobile (Técnicos de Campo)
   - Atendimento de chamados offline
   - Coleta de inventário via QR Code
   - Sincronização automática

4. **PRO-IA-001:** Assistente de IA para Service Desk
   - Classificação automática de chamados
   - Sugestão de soluções baseada em histórico
   - Chatbot para clientes

### 10.2 Melhorias de Integração Planejadas

1. **Event Sourcing Completo:**
   - Substituir integrações síncronas por eventos de domínio
   - Maior resiliência e auditoria completa

2. **API Gateway Unificada:**
   - Centralização de todas as APIs REST
   - Rate limiting, cache, autenticação centralizada

3. **Sincronização Bidirecional com ERPs:**
   - Atualmente: IControlIT → ERP (unidirecional)
   - Futuro: ERP ↔ IControlIT (bidirecional)

4. **Webhooks para Clientes:**
   - Permitir clientes configurarem webhooks para eventos críticos
   - Exemplo: `chamado.criado`, `nfe.emitida`, `pagamento.confirmado`

### 10.3 Roadmap de Automações Adicionais

1. **Q2 2026:** Chatbot de IA para Service Desk (reduzir 30% de chamados triviais)
2. **Q3 2026:** Análise preditiva de SLA (detectar chamados com risco de violação)
3. **Q4 2026:** Automação de renovação de contratos (sem intervenção humana)
4. **Q1 2027:** Integração completa com Microsoft 365 (criação automática de usuários, licenças)

### 10.4 Monitoramento Contínuo

**Métricas a acompanhar:**

1. **Performance:**
   - Tempo de execução de cada processo
   - Taxa de falha de integrações

2. **Qualidade:**
   - Taxa de erros por processo
   - CSAT por processo (Service Desk)

3. **Conformidade:**
   - % de operações auditadas
   - Tempo de resposta a auditorias

4. **Negócio:**
   - ROI de cada automação
   - Tempo economizado acumulado

---

## 11. Conclusão

### 11.1 Visão Consolidada

Este documento apresentou a **arquitetura de processos completa do IControlIT**, integrando **38 processos** documentados em **6 jornadas**:

- **8 processos de Infraestrutura:** Fundação do sistema (auth, multi-tenancy, logs, auditoria)
- **9 processos de Workflows:** Automação e comunicação (e-mails, notificações, aprovações)
- **12 processos Financeiros:** Contratos, faturamento, ativos e custos
- **8 processos de Service Desk:** Atendimento, SLA, escalação, satisfação
- **1 processo de Auditoria:** Conciliação de inventário

### 11.2 Principais Conclusões

1. **Processos Transversais são Críticos:**
   - PRO-INF-003 (Logs), PRO-INF-004 (Auditoria), PRO-WKF-004 (Notificações)
   - Usados por 30+ processos, fundamentais para operação

2. **Eventos de Domínio Conectam Tudo:**
   - 1 evento (`cliente.criado`) pode disparar 7 processos automáticos
   - Desacoplamento permite escalabilidade e manutenibilidade

3. **Automação Gera Valor Mensurável:**
   - **98 horas/mês economizadas** = R$ 47.040/ano
   - **92% de redução de erros** = R$ 96.000/ano em custos evitados
   - **ROI de 285% em 3 anos**

4. **Ordem de Implementação Importa:**
   - FASE 1 (Fundacionais) é obrigatória antes de qualquer outra
   - FASE 3 (Financeiro) gera maior valor de negócio

5. **Conformidade é Obrigatória:**
   - ISO 27001, SOC 2, LGPD, SOX exigem auditoria completa
   - PRO-INF-004 + PRO-AUD-001 garantem 100% de conformidade

### 11.3 Mensagem Final

A **modernização dos 38 processos** transformou o IControlIT de um sistema legado fragmentado em uma **plataforma integrada, automatizada e auditável**. A visão consolidada apresentada neste documento serve como:

- **Mapa estratégico:** Para entender como os processos se relacionam
- **Guia de implementação:** Para priorizar desenvolvimentos futuros
- **Ferramenta de auditoria:** Para validar conformidade e integridade
- **Documento de onboarding:** Para novos membros da equipe

**A arquitetura de processos do IControlIT é uma vantagem competitiva estratégica.**

---

**Autor:** ALC (alc.dev.br)
**Revisores:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Versão:** 1.0

---

## Anexo A: Referências Cruzadas

### Documentos de Jornadas

- **Jornada 1:** `01-Jornada-infraestrutura.md` (PRO-INF-001 a PRO-INF-008)
- **Jornada 2:** `02-Jornada-workflows.md` (PRO-WKF-001 a PRO-WKF-009)
- **Jornada 3:** `03-Jornada-financeiro.md` (PRO-FCT-001 a PRO-FCT-007, PRO-FAC-001 a PRO-FAC-005)
- **Jornada 5:** `05-Jornada-service-desk.md` (PRO-SVC-001 a PRO-SVC-008)
- **Jornada 6:** `06-Jornada-auditoria.md` (PRO-AUD-001)

### Documentos de Governança

- **ARCHITECTURE.md:** Stack tecnológico e padrões arquiteturais
- **CONVENTIONS.md:** Nomenclatura e padrões de código
- **COMPLIANCE.md:** Regras de validação e conformidade
- **COMMANDS.md:** Comandos de desenvolvimento e validação

---

**FIM DO DOCUMENTO**


---

# PARTE 9: ANEXOS

---


**Versão:** 2.0
**Data:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente

---

## ÍNDICE

1. [Glossário de Termos Técnicos](#1-glossário-de-termos-técnicos)
2. [Referências Completas aos RFs](#2-referências-completas-aos-rfs)
3. [Mapa de Dependências Processos → RFs](#3-mapa-de-dependências-processos--rfs)
4. [Árvore de Dependências Técnicas](#4-árvore-de-dependências-técnicas)
5. [Tabela de RFs Excluídos](#5-tabela-de-rfs-excluídos-cadastros-simples)
6. [Matriz de Cobertura RF → UC → TC](#6-matriz-de-cobertura-rf--uc--tc)
7. [Recursos Adicionais](#7-recursos-adicionais)
8. [Índice Alfabético de Processos](#8-índice-alfabético-de-processos)
9. [Changelog Consolidado](#9-changelog-consolidado)
10. [Contatos e Suporte](#10-contatos-e-suporte)

---

## 1. GLOSSÁRIO DE TERMOS TÉCNICOS

### 1.1. ARQUITETURA

#### Aggregate
**Definição:** Padrão DDD que agrupa entidades relacionadas sob uma raiz única, garantindo consistência transacional.
**Contexto de Uso:** PRO-INF-001, PRO-AUD-001, PRO-FCT-001 (handlers de criação/atualização)
**Exemplo:** `FaturaAggregate` agrupa `Fatura`, `ItemFatura`, `RateioFatura`

#### Clean Architecture
**Definição:** Arquitetura em camadas concêntricas (Domain → Application → Infrastructure → Presentation) com dependências apontando para o centro.
**Contexto de Uso:** Todos os processos (estrutura base do sistema)
**Exemplo:** Handlers (Application) não conhecem Controllers (Presentation)

#### Command
**Definição:** Objeto que representa uma intenção de alterar estado do sistema (padrão CQRS).
**Contexto de Uso:** Todos os processos com operações de escrita
**Exemplo:** `CreateClienteCommand`, `AprovarSolicitacaoCommand`

#### CQRS (Command Query Responsibility Segregation)
**Definição:** Separação entre operações de escrita (Commands) e leitura (Queries).
**Contexto de Uso:** Todos os processos
**Exemplo:** `CreateFaturaCommand` vs `GetFaturaByIdQuery`

#### DDD (Domain-Driven Design)
**Definição:** Abordagem de design que coloca a lógica de negócio no centro da arquitetura.
**Contexto de Uso:** PRO-INF-001 a PRO-AUD-001 (todos os processos)
**Exemplo:** Entidades `Fatura`, `Solicitacao`, `Ativo` com regras de negócio encapsuladas

#### Event
**Definição:** Notificação imutável de algo que já aconteceu no sistema.
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001, PRO-SVC-002 (notificações assíncronas)
**Exemplo:** `FaturaAprovadaEvent`, `SLAVioladoEvent`

#### Handler
**Definição:** Classe responsável por processar Commands, Queries ou Events (padrão MediatR).
**Contexto de Uso:** Todos os processos
**Exemplo:** `CreateFaturaHandler`, `GetClientesQueryHandler`

#### MediatR
**Definição:** Biblioteca que implementa o padrão Mediator para desacoplar requests de seus handlers.
**Contexto de Uso:** Todos os processos
**Exemplo:** `IRequestHandler<CreateClienteCommand, ClienteDto>`

#### Query
**Definição:** Objeto que representa uma consulta ao sistema sem alterar estado (padrão CQRS).
**Contexto de Uso:** Todos os processos com operações de leitura
**Exemplo:** `GetFaturasByClienteIdQuery`, `SearchAtivosQuery`

#### Repository
**Definição:** Padrão que encapsula acesso a dados, abstraindo detalhes de persistência.
**Contexto de Uso:** Todos os processos
**Exemplo:** `IFaturaRepository`, `IClienteRepository`

#### Unit of Work
**Definição:** Padrão que gerencia transações e coordena salvamento de múltiplos agregados.
**Contexto de Uso:** PRO-INF-001, PRO-FCT-001, PRO-AUD-001 (operações transacionais)
**Exemplo:** `_unitOfWork.SaveChangesAsync()` ao final de handlers

---

### 1.2. MULTI-TENANCY

#### ClienteId
**Definição:** Identificador único do tenant, obrigatório em todas as entidades para isolamento de dados.
**Contexto de Uso:** Todos os processos (obrigatório por COMPLIANCE.md seção 6)
**Exemplo:** `WHERE ClienteId = @clienteId` em todas as queries

#### Cross-tenant
**Definição:** Operação que acessa dados de múltiplos tenants (PROIBIDO sem justificativa).
**Contexto de Uso:** PRO-INF-006, PRO-INF-004 (auditoria cross-tenant)
**Exemplo:** Relatórios consolidados de múltiplos clientes (requer autorização)

#### Isolamento
**Definição:** Garantia de que dados de um tenant não sejam acessíveis por outro.
**Contexto de Uso:** Todos os processos
**Exemplo:** Row-Level Security (RLS) no PostgreSQL

#### Row-Level Security (RLS)
**Definição:** Mecanismo de banco de dados que filtra linhas automaticamente por ClienteId.
**Contexto de Uso:** PRO-INF-006, todos os processos de dados sensíveis
**Exemplo:** `CREATE POLICY cliente_isolation ON faturas USING (ClienteId = current_setting('app.cliente_id')::uuid)`

#### Shared Database
**Definição:** Modelo multi-tenancy onde todos os tenants compartilham o mesmo banco de dados.
**Contexto de Uso:** Arquitetura base do sistema
**Exemplo:** Tabela `Faturas` com coluna `ClienteId` discriminando tenants

#### Tenant
**Definição:** Cliente isolado no sistema multi-tenancy (sinônimo de Cliente).
**Contexto de Uso:** Todos os processos
**Exemplo:** Cliente "Empresa XYZ" é um tenant com `ClienteId = uuid-1234`

#### Tenant-specific
**Definição:** Configuração, dado ou lógica específica de um tenant.
**Contexto de Uso:** PRO-INF-001, PRO-INF-006
**Exemplo:** Parâmetro `dias_vencimento_fatura` pode variar por tenant

---

### 1.3. COMPLIANCE E CERTIFICAÇÕES

#### Auditoria
**Definição:** Registro imutável de operações críticas para rastreabilidade e conformidade.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007, PRO-AUD-001
**Exemplo:** Tabela `AuditLogs` com snapshot antes/depois de alterações

#### Compliance
**Definição:** Conformidade com regulamentações, normas e certificações.
**Contexto de Uso:** Todos os processos (obrigatório por COMPLIANCE.md)
**Exemplo:** LGPD, SOX, ISO 27001, SOC 2

#### ISO 27001
**Definição:** Norma internacional de gestão de segurança da informação.
**Contexto de Uso:** PRO-INF-007, PRO-INF-008, PRO-INF-004
**Exemplo:** Logs de acesso, criptografia de dados sensíveis, controle de acesso

#### LGPD (Lei Geral de Proteção de Dados)
**Definição:** Lei brasileira que regula tratamento de dados pessoais.
**Contexto de Uso:** PRO-INF-006, PRO-INF-007, PRO-INF-004
**Exemplo:** Anonimização de logs, direito ao esquecimento, consentimento

#### OWASP
**Definição:** Organização que define padrões de segurança web (OWASP Top 10).
**Contexto de Uso:** PRO-INF-007, PRO-INF-008
**Exemplo:** Proteção contra SQL Injection, XSS, CSRF

#### PCI-DSS
**Definição:** Padrão de segurança para transações com cartões de crédito.
**Contexto de Uso:** PRO-FCT-002 (pagamentos de faturas)
**Exemplo:** Não armazenar CVV, tokenização de números de cartão

#### Retenção
**Definição:** Período obrigatório de armazenamento de dados conforme regulamentação.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007
**Exemplo:** Logs auditoria retidos por 7 anos (SOX), faturas por 5 anos (legislação fiscal)

#### SOC 2 (Service Organization Control 2)
**Definição:** Auditoria de controles internos de segurança, disponibilidade e confidencialidade.
**Contexto de Uso:** PRO-INF-004, PRO-INF-007, PRO-SVC-001
**Exemplo:** Monitoramento de SLA, logs de acesso, backup automatizado

#### SOX (Sarbanes-Oxley)
**Definição:** Lei americana que exige controles rigorosos sobre dados financeiros.
**Contexto de Uso:** PRO-FCT-001 a PRO-FCT-007, PRO-AUD-001
**Exemplo:** Segregação de funções, auditoria de alterações financeiras, trilha imutável

---

### 1.4. SEGURANÇA

#### API Key
**Definição:** Chave de autenticação para APIs externas ou integrações.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003 (integração SEFAZ)
**Exemplo:** `X-API-Key: sk_live_1234567890abcdef` no header HTTP

#### Azure Key Vault
**Definição:** Serviço Azure para armazenamento seguro de secrets, chaves e certificados.
**Contexto de Uso:** PRO-INF-008, PRO-INF-001
**Exemplo:** Connection strings, API Keys, certificados SSL armazenados no Key Vault

#### Criptografia AES-256
**Definição:** Algoritmo de criptografia simétrica com chave de 256 bits.
**Contexto de Uso:** PRO-INF-008, PRO-INF-004
**Exemplo:** Criptografia de anexos sensíveis no Azure Blob Storage

#### Hash
**Definição:** Função unidirecional que gera identificador fixo de tamanho a partir de entrada variável.
**Contexto de Uso:** PRO-INF-007 (senhas), PRO-INF-004 (integridade de logs)
**Exemplo:** Senha hasheada com bcrypt, SHA-256 para verificação de integridade

#### JWT (JSON Web Token)
**Definição:** Token autocontido que carrega claims de autenticação/autorização.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` contendo `ClienteId`, `UserId`, `Roles`

#### MFA (Multi-Factor Authentication)
**Definição:** Autenticação que exige múltiplos fatores (senha + código SMS/App).
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Login com senha + código TOTP do Microsoft Authenticator

#### OAuth 2.0
**Definição:** Protocolo de autorização para acesso seguro a recursos protegidos.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Fluxo Authorization Code com PKCE para SPAs

#### Rate Limiting
**Definição:** Limitação de número de requisições por tempo para prevenir abuso.
**Contexto de Uso:** PRO-INF-007, PRO-INF-008
**Exemplo:** Máximo 100 requisições/minuto por IP

#### Refresh Token
**Definição:** Token de longa duração usado para obter novos Access Tokens sem re-autenticação.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Refresh Token válido por 30 dias, Access Token por 1 hora

#### Throttling
**Definição:** Redução gradual de taxa de processamento quando limites são atingidos.
**Contexto de Uso:** PRO-INF-008, PRO-IMP-001
**Exemplo:** Importação desacelera de 1000/s para 100/s ao atingir 80% CPU

---

### 1.5. PERFORMANCE

#### Backoff Exponencial
**Definição:** Estratégia de retry que aumenta exponencialmente o intervalo entre tentativas.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003 (integração SEFAZ)
**Exemplo:** Retry após 1s, 2s, 4s, 8s, 16s...

#### Cache
**Definição:** Armazenamento temporário de dados frequentemente acessados para reduzir latência.
**Contexto de Uso:** PRO-INF-001, PRO-INF-002, PRO-WKF-006
**Exemplo:** Redis cache para parâmetros de sistema, templates de relatórios

#### Circuit Breaker
**Definição:** Padrão que interrompe chamadas a serviços falhando repetidamente.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003
**Exemplo:** Após 5 falhas consecutivas na SEFAZ, abre circuito por 60 segundos

#### Hot-Reload
**Definição:** Atualização de configuração/código sem restart da aplicação.
**Contexto de Uso:** PRO-INF-001, PRO-WKF-006
**Exemplo:** Atualizar template de relatório sem reiniciar backend

#### Lazy Loading
**Definição:** Carregamento sob demanda de dados relacionados (não antecipado).
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Carregar itens de fatura apenas quando expandir detalhes

#### Pub/Sub
**Definição:** Padrão de mensageria assíncrona (publisher/subscriber).
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001
**Exemplo:** Redis Pub/Sub para notificações em tempo real via SignalR

#### Redis
**Definição:** Banco de dados em memória usado para cache e mensageria.
**Contexto de Uso:** PRO-INF-001, PRO-INF-002, PRO-WKF-004
**Exemplo:** Cache de parâmetros, Pub/Sub para notificações

#### SqlBulkCopy
**Definição:** API .NET para inserção em massa de dados no SQL Server.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Importar 50.000 ativos em chunks de 1.000 registros

#### TTL (Time To Live)
**Definição:** Tempo de expiração de cache ou token.
**Contexto de Uso:** PRO-INF-001, PRO-INF-007
**Exemplo:** Cache de parâmetros com TTL de 5 minutos

---

### 1.6. INFRAESTRUTURA

#### Azure Blob Storage
**Definição:** Serviço Azure de armazenamento de objetos (arquivos, imagens, documentos).
**Contexto de Uso:** PRO-INF-002, PRO-FCT-004, PRO-SVC-003
**Exemplo:** Upload de anexos, PDF de DANFE, evidências de chamados

#### Hangfire
**Definição:** Biblioteca .NET para agendamento e execução de jobs em background.
**Contexto de Uso:** PRO-INF-005, PRO-FCT-006, PRO-IMP-001
**Exemplo:** Job recorrente para calcular SLA a cada 5 minutos

#### OFX (Open Financial Exchange)
**Definição:** Formato padrão para troca de dados financeiros.
**Contexto de Uso:** PRO-FCT-005 (importação de conciliação bancária)
**Exemplo:** Arquivo .ofx exportado do banco contendo transações

#### OpenAPI (Swagger)
**Definição:** Especificação para documentação de APIs REST.
**Contexto de Uso:** PRO-INF-008
**Exemplo:** Swagger UI em `/swagger` para documentação interativa

#### REST API
**Definição:** Arquitetura de APIs baseada em HTTP com operações CRUD.
**Contexto de Uso:** Todos os processos
**Exemplo:** `POST /api/faturas`, `GET /api/ativos/{id}`

#### SignalR
**Definição:** Biblioteca para comunicação real-time bidirecional via WebSockets.
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001, PRO-IMP-001
**Exemplo:** Notificação push de SLA violado, progress de importação

#### SOAP
**Definição:** Protocolo de comunicação baseado em XML (legado).
**Contexto de Uso:** PRO-FCT-003 (integração SEFAZ)
**Exemplo:** Web Service SOAP para consulta de NF-e

#### Webhook
**Definição:** Callback HTTP enviado automaticamente quando evento ocorre.
**Contexto de Uso:** PRO-WKF-004, PRO-INF-008
**Exemplo:** Webhook para sistema externo quando fatura é aprovada

---

### 1.7. FINANCEIRO

#### Centro de Custo
**Definição:** Unidade organizacional para alocação de despesas.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** "TI", "Financeiro", "RH" como centros de custo

#### Conciliação
**Definição:** Processo de comparação entre faturas emitidas e pagamentos recebidos.
**Contexto de Uso:** PRO-FCT-005
**Exemplo:** Conciliar extrato bancário com faturas pagas

#### DANFE (Documento Auxiliar da Nota Fiscal Eletrônica)
**Definição:** Representação gráfica simplificada da NF-e para acompanhar transporte.
**Contexto de Uso:** PRO-FCT-004
**Exemplo:** PDF do DANFE anexado à fatura

#### Depreciação
**Definição:** Redução gradual do valor contábil de um ativo ao longo de sua vida útil.
**Contexto de Uso:** PRO-AUD-001
**Exemplo:** Notebook de R$ 5.000 depreciado em 5 anos (20% ao ano)

#### DRE (Demonstrativo de Resultados do Exercício)
**Definição:** Relatório contábil que mostra receitas, despesas e lucro/prejuízo.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Relatório mensal consolidando todas as faturas e custos de ativos

#### NF-e (Nota Fiscal Eletrônica)
**Definição:** Documento fiscal digital que substitui nota fiscal em papel.
**Contexto de Uso:** PRO-FCT-003, PRO-FCT-004
**Exemplo:** Emissão de NF-e para fatura de serviços mensais

#### Pro-rata
**Definição:** Cálculo proporcional de valores baseado em período ou critério.
**Contexto de Uso:** PRO-FCT-006
**Exemplo:** Faturamento pro-rata de serviço contratado no meio do mês

#### Rateio
**Definição:** Distribuição proporcional de custos entre múltiplos centros ou contratos.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Rateio de fatura de internet entre 3 centros de custo (40%, 30%, 30%)

#### SEFAZ (Secretaria da Fazenda)
**Definição:** Órgão estadual que autoriza e valida notas fiscais eletrônicas.
**Contexto de Uso:** PRO-FCT-003
**Exemplo:** Integração SOAP para autorizar NF-e na SEFAZ-SP

#### TCO (Total Cost of Ownership)
**Definição:** Custo total de propriedade de um ativo (aquisição + operação + manutenção).
**Contexto de Uso:** PRO-AUD-001
**Exemplo:** TCO de notebook = compra + licenças + suporte + depreciação

---

### 1.8. SERVICE DESK

#### Base de Conhecimento
**Definição:** Repositório centralizado de artigos, procedimentos e soluções.
**Contexto de Uso:** PRO-SVC-003, PRO-WKF-005
**Exemplo:** Artigo "Como resetar senha do usuário" na KB

#### Catálogo de Serviços
**Definição:** Lista padronizada de serviços disponíveis para solicitação.
**Contexto de Uso:** PRO-SVC-005, PRO-WKF-006
**Exemplo:** "Provisionar novo usuário", "Instalar software", "Manutenção de ativo"

#### Escalação
**Definição:** Encaminhamento de chamado/solicitação para nível superior de suporte.
**Contexto de Uso:** PRO-SVC-006, PRO-SVC-001
**Exemplo:** Chamado escalado de N1 para N2 após 2 horas sem resolução

#### Matriz Impacto × Urgência
**Definição:** Matriz para calcular prioridade combinando impacto e urgência.
**Contexto de Uso:** PRO-SVC-007
**Exemplo:** Impacto Alto + Urgência Alta = Prioridade Crítica

#### NPS (Net Promoter Score)
**Definição:** Métrica de satisfação do cliente (escala 0-10).
**Contexto de Uso:** PRO-SVC-009
**Exemplo:** Pesquisa enviada após fechamento de chamado

#### Priorização
**Definição:** Processo de determinar ordem de atendimento de chamados/solicitações.
**Contexto de Uso:** PRO-SVC-007
**Exemplo:** Chamados Críticos atendidos antes de Baixos

#### SLA (Service Level Agreement)
**Definição:** Acordo formal definindo tempo máximo para atendimento/resolução.
**Contexto de Uso:** PRO-SVC-001, PRO-SVC-002, PRO-SVC-006
**Exemplo:** SLA de 4 horas para chamados de Prioridade Alta

#### TFR (Time to First Response)
**Definição:** Tempo entre abertura do chamado e primeira resposta.
**Contexto de Uso:** PRO-SVC-001
**Exemplo:** TFR de 15 minutos para chamados Críticos

#### TTR (Time to Resolution)
**Definição:** Tempo total entre abertura e resolução do chamado.
**Contexto de Uso:** PRO-SVC-002
**Exemplo:** TTR de 2 horas para chamados de Prioridade Média

---

### 1.9. WORKFLOWS

#### Alçada
**Definição:** Nível de autoridade necessário para aprovação baseado em valor ou tipo.
**Contexto de Uso:** PRO-WKF-009
**Exemplo:** Faturas > R$ 10.000 exigem alçada de diretor

#### Aprovação
**Definição:** Ação formal de autorizar execução de processo ou transação.
**Contexto de Uso:** PRO-WKF-009, PRO-FCT-001, PRO-SVC-005
**Exemplo:** Aprovação de fatura antes de emissão de NF-e

#### Delegação
**Definição:** Transferência temporária de autoridade de aprovação.
**Contexto de Uso:** PRO-WKF-009
**Exemplo:** Gerente delega aprovações para substituto durante férias

#### Interpolação
**Definição:** Substituição de variáveis em template por valores reais.
**Contexto de Uso:** PRO-WKF-006, PRO-WKF-004
**Exemplo:** Template "{NomeCliente}" interpolado para "Empresa XYZ"

#### Renderização
**Definição:** Processo de gerar documento final a partir de template + dados.
**Contexto de Uso:** PRO-WKF-006
**Exemplo:** Renderizar contrato PDF a partir de template Word + dados do cliente

#### State Machine
**Definição:** Modelo de estados e transições para gerenciar ciclo de vida.
**Contexto de Uso:** PRO-SVC-003, PRO-FCT-001, PRO-SVC-005
**Exemplo:** Chamado: Aberto → Em Atendimento → Aguardando Cliente → Resolvido → Fechado

#### Template
**Definição:** Modelo reutilizável com placeholders para geração de documentos/mensagens.
**Contexto de Uso:** PRO-WKF-006, PRO-WKF-004
**Exemplo:** Template de email de boas-vindas com {NomeUsuario}, {Senha}

---

### 1.10. IMPORTAÇÃO

#### Batch
**Definição:** Processamento em lote de múltiplos registros de uma vez.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Importar 10.000 ativos em batches de 1.000

#### Chunk
**Definição:** Fragmento de dados processado em uma iteração de batch.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Processar arquivo de 50.000 linhas em chunks de 1.000

#### OLE DB
**Definição:** API Microsoft para acesso a fontes de dados (Excel, Access, etc).
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Ler arquivo Excel via OLE DB Provider

#### Progress Bar
**Definição:** Indicador visual de progresso de operação longa.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Barra mostrando "3.500 / 10.000 registros importados (35%)"

#### Rollback
**Definição:** Reversão de transação ou importação em caso de erro.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Rollback de importação se detectar erro de validação

#### Validação
**Definição:** Verificação de integridade, consistência e conformidade de dados.
**Contexto de Uso:** PRO-IMP-001, todos os processos
**Exemplo:** Validar formato de CNPJ, obrigatoriedade de ClienteId

---

### 1.11. LOGS E OBSERVABILIDADE

#### Correlation ID
**Definição:** Identificador único propagado em todas as operações de uma requisição.
**Contexto de Uso:** PRO-INF-003, PRO-INF-004
**Exemplo:** `X-Correlation-Id: uuid-5678` rastreando requisição por múltiplos serviços

#### Mascaramento
**Definição:** Ocultação de dados sensíveis em logs (PII, senhas, tokens).
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Logar CPF como "123.***.***-45"

#### OpenTelemetry
**Definição:** Framework padrão para coleta de traces, métricas e logs.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Exportar traces para Jaeger/Application Insights

#### RED Metrics
**Definição:** Métricas essenciais de serviços: Rate, Errors, Duration.
**Contexto de Uso:** PRO-INF-003, PRO-SVC-001
**Exemplo:** Monitorar taxa de requisições/s, % erros, latência P95

#### Sampling
**Definição:** Coleta de apenas parte dos logs/traces para reduzir volume.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Logar 10% das requisições GET, 100% das POST

#### Structured Logging
**Definição:** Logs formatados como JSON estruturado (não texto plano).
**Contexto de Uso:** PRO-INF-003
**Exemplo:** `{"timestamp": "...", "level": "ERROR", "message": "...", "clienteId": "..."}`

#### Tracing Distribuído
**Definição:** Rastreamento de requisição através de múltiplos serviços/componentes.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Trace mostrando API → Handler → Repository → Database

---

### 1.12. AUDITORIA

#### Anomalia
**Definição:** Padrão de comportamento que desvia significativamente do esperado.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** 500 logins falhados em 1 minuto do mesmo IP (possível ataque)

#### Assinatura Digital SHA-256
**Definição:** Hash criptográfico para verificar integridade de logs de auditoria.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Cada log auditoria tem hash SHA-256 do log anterior (blockchain-like)

#### Cold Storage
**Definição:** Armazenamento de longo prazo de baixo custo para dados raramente acessados.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Logs > 1 ano movidos para Azure Archive Storage

#### Diff JSON
**Definição:** Diferença estruturada entre estado anterior e posterior de objeto.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** `{"before": {"status": "Pendente"}, "after": {"status": "Aprovado"}}`

#### Imutabilidade
**Definição:** Propriedade de dados que não podem ser alterados após criação.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Logs de auditoria são append-only, nunca atualizados

#### Segregação de Funções
**Definição:** Separação de responsabilidades críticas entre diferentes usuários.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007
**Exemplo:** Usuário que cria fatura não pode aprovar a mesma fatura

#### Snapshot
**Definição:** Captura completa do estado de um objeto em momento específico.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Snapshot JSON da fatura antes de alteração

---

## 2. REFERÊNCIAS COMPLETAS AOS RFs

### 2.1. TABELA CONSOLIDADA DE PROCESSOS E RFs

| Código Processo | Nome do Processo | RF | Localização do RF | Status |
|-----------------|------------------|----|--------------------|--------|
| **PRO-INF-001** | Parâmetros e Configurações | RF001 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF001-Parametros-e-Configuracoes-do-Sistema\RF001.md` | Documentado |
| **PRO-INF-002** | Gerenciamento de Arquivos | RF002 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF002-Gerenciamento-de-Arquivos-Anexos\RF002.md` | Documentado |
| **PRO-INF-003** | Logs de Sistema | RF003 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF003-Gerenciamento-de-Logs\RF003.md` | Documentado |
| **PRO-INF-004** | Auditoria de Operações | RF004 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF004-Auditoria-de-Operacoes\RF004.md` | Documentado |
| **PRO-INF-005** | Agendamento de Tarefas | RF005 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF005-Agendamento-Automatizado-Jobs\RF005.md` | Documentado |
| **PRO-INF-006** | Gestão de Clientes | RF006 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF006-Gestao-Clientes-Multi-Tenancy\RF006.md` | Documentado |
| **PRO-INF-007** | Login e Autenticação | RF007 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF007-Autenticacao-e-Login\RF007.md` | Documentado |
| **PRO-INF-008** | Integrações Externas | RF008 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF008-Integracoes-Externas\RF008.md` | Documentado |
| **PRO-WKF-001** | Cadastro de Usuários | RF009 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF009-Gestao-Usuarios-Colaboradores\RF009.md` | Documentado |
| **PRO-WKF-002** | Gestão de Permissões | RF010 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF010-Gestao-Permissoes-Acesso\RF010.md` | Documentado |
| **PRO-WKF-003** | Hierarquia Organizacional | RF011 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF011-Hierarquia-Organizacional\RF011.md` | Documentado |
| **PRO-WKF-004** | Notificações | RF014 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF014-Notificacoes-e-Alertas\RF014.md` | Documentado |
| **PRO-WKF-005** | Base de Conhecimento | RF015 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF015-Base-Conhecimento\RF015.md` | Documentado |
| **PRO-WKF-006** | Templates Documentos | RF016 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF016-Templates-Documentos\RF016.md` | Documentado |
| **PRO-WKF-007** | Relatórios e Dashboards | RF017 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF017-Relatorios-e-Dashboards\RF017.md` | Documentado |
| **PRO-WKF-008** | Pesquisas de Satisfação | RF018 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF018-Pesquisas-Satisfacao\RF018.md` | Documentado |
| **PRO-WKF-009** | Aprovações e Workflows | RF019 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF019-Aprovacoes-Workflows\RF019.md` | Documentado |
| **PRO-IMP-001** | Importação em Massa | RF020 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF020-Importacao-Massa-Excel\RF020.md` | Documentado |
| **PRO-AUD-001** | Inventário Cíclico | RF068 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC004-AST-Gestao-Ativos\RF068-Inventario-Ciclico-Auditoria\RF068.md` | Documentado |
| **PRO-FCT-001** | Gestão de Faturas | RF021 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF021-Gestao-Faturas\RF021.md` | Documentado |
| **PRO-FCT-002** | Baixa de Faturas | RF022 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF022-Baixa-Faturas\RF022.md` | Documentado |
| **PRO-FCT-003** | Emissão de NF-e | RF023 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF023-Emissao-NF-e\RF023.md` | Documentado |
| **PRO-FCT-004** | Download DANFE | RF024 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF024-Download-DANFE\RF024.md` | Documentado |
| **PRO-FCT-005** | Conciliação Financeira | RF025 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF025-Conciliacao-Financeira\RF025.md` | Documentado |
| **PRO-FCT-006** | Medição/Faturamento | RF026 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF026-Medicao-Faturamento\RF026.md` | Documentado |
| **PRO-FCT-007** | Auditoria de Faturas | RF027 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF027-Auditoria-Faturas\RF027.md` | Documentado |
| **PRO-SVC-001** | SLA Operações | RF028 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF028-SLA-Operacoes-Chamados\RF028.md` | Documentado |
| **PRO-SVC-002** | SLA Serviços | RF029 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF029-SLA-Servicos-Solicitacoes\RF029.md` | Documentado |
| **PRO-SVC-003** | Gestão de Chamados | RF030 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF030-Gestao-Chamados\RF030.md` | Documentado |
| **PRO-SVC-004** | Ordens de Serviço | RF031 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF031-Ordens-Servico\RF031.md` | Documentado |
| **PRO-SVC-005** | Solicitações | RF032 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF032-Gestao-Solicitacoes\RF032.md` | Documentado |
| **PRO-SVC-006** | Escalação Automática | RF033 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF033-Escalacao-Automatica\RF033.md` | Documentado |
| **PRO-SVC-007** | Priorização Automática | RF034 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF034-Priorizacao-Automatica\RF034.md` | Documentado |
| **PRO-SVC-008** | Reaberturas | RF035 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF035-Reaberturas\RF035.md` | Documentado |
| **PRO-SVC-009** | Pesquisas Satisfação SD | RF036 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF036-Pesquisas-Satisfacao-Service-Desk\RF036.md` | Documentado |
| **PRO-SVC-010** | Agrupamento de Chamados | RF037 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF037-Agrupamento-Chamados\RF037.md` | Documentado |
| **PRO-SVC-011** | Histórico Unificado | RF038 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF038-Historico-Unificado\RF038.md` | Documentado |

**Total:** 38 processos documentados, 38 RFs únicos referenciados

---

### 2.2. DISTRIBUIÇÃO POR FASE E EPIC

| Fase | EPIC | Processos | RFs |
|------|------|-----------|-----|
| **Fase 1** | EPIC001-SYS (Sistema Infraestrutura) | 5 | RF001-RF005, RF008 |
| **Fase 1** | EPIC002-SEC (Segurança Acesso) | 4 | RF006-RF007, RF009-RF011 |
| **Fase 2** | EPIC004-AST (Gestão Ativos) | 1 | RF068 |
| **Fase 2** | EPIC006-WKF (Workflows Automações) | 8 | RF014-RF020 |
| **Fase 3** | EPIC007-FCT (Faturamento) | 7 | RF021-RF027 |
| **Fase 4** | EPIC008-SVC (Service Desk) | 11 | RF028-RF038 |
| **Fase 5** | EPIC009-CTR (Contratos) | 2 | RF039-RF040 |

---

## 3. MAPA DE DEPENDÊNCIAS PROCESSOS → RFs

### 3.1. VISÃO CONSOLIDADA

- **Total de processos documentados:** 38
- **Total de RFs envolvidos:** 38 RFs únicos
- **RFs sem processo documentado:** 72 RFs (cadastros CRUD simples)
- **Total de RFs no sistema:** 110 RFs
- **Percentual de cobertura:** 34,5% (38/110) - cobertura intencional focada em processos complexos

### 3.2. JUSTIFICATIVA DE EXCLUSÃO DOS 72 RFs

Os 72 RFs excluídos da documentação de processos são:

**Categoria: Cadastros CRUD Simples**
- Não possuem workflow complexo
- Não têm automações significativas
- Não requerem integrações
- Não possuem regras de negócio sofisticadas
- São operações básicas de Create/Read/Update/Delete
- São suportados pela arquitetura base definida em PRO-INF-001 a PRO-INF-008

**Exemplos:**
- RF012: Cadastro de Cores de Ativo
- RF013: Cadastro de Status de Chamado
- RF039: Cadastro de Tipos de Documento
- RF055: Cadastro de Moedas
- RF067: Cadastro de Classificações Contábeis

**Estratégia de Documentação:**
- Foco em processos que envolvem **múltiplos sistemas**
- Foco em processos com **workflows complexos**
- Foco em processos com **automações críticas**
- Foco em processos com **integrações externas**
- Cadastros simples são documentados apenas via RF, UC e TC (sem documento de processo dedicado)

---

## 4. ÁRVORE DE DEPENDÊNCIAS TÉCNICAS

### 4.1. DEPENDÊNCIAS FUNDAMENTAIS (Camada Base)

```
PRO-INF-006 (Gestão de Clientes - Multi-Tenancy)
├─── REQUISITO OBRIGATÓRIO PARA TODOS OS 37 PROCESSOS
│    └─── ClienteId obrigatório em TODAS as entidades
│
PRO-INF-007 (Login/Autenticação)
├─── REQUISITO OBRIGATÓRIO PARA TODOS OS 37 PROCESSOS
│    └─── JWT, OAuth 2.0, controle de acesso
│
PRO-INF-003 (Logs de Sistema)
├─── USADO POR TODOS OS 38 PROCESSOS
│    └─── Correlation ID, Structured Logging
│
PRO-INF-004 (Auditoria de Operações)
├─── USADO POR 30+ PROCESSOS
│    └─── Snapshot, Diff JSON, rastreabilidade SOX
│
PRO-INF-001 (Parâmetros e Configurações)
├─── USADO POR 35+ PROCESSOS
│    └─── Configurações tenant-specific, cache Redis
│
PRO-INF-002 (Gerenciamento de Arquivos)
├─── USADO POR 15+ PROCESSOS
│    └─── Azure Blob Storage, upload/download
│
PRO-INF-005 (Agendamento de Tarefas)
├─── USADO POR 20+ PROCESSOS
│    └─── Hangfire, jobs recorrentes
│
PRO-INF-008 (Integrações Externas)
├─── USADO POR 10+ PROCESSOS
     └─── Webhooks, APIs externas, rate limiting
```

### 4.2. DEPENDÊNCIAS DE WORKFLOWS (Camada Intermediária)

```
PRO-WKF-009 (Aprovações e Workflows)
├─── PRO-FCT-001 (Gestão de Faturas)
├─── PRO-FCT-006 (Medição/Faturamento)
├─── PRO-SVC-005 (Solicitações)
├─── PRO-AUD-001 (Inventário Cíclico)
├─── PRO-FCT-003 (Emissão NF-e)
├─── 10+ outros processos
│
PRO-WKF-004 (Notificações)
├─── PRO-SVC-001 (SLA Operações)
├─── PRO-SVC-002 (SLA Serviços)
├─── PRO-SVC-006 (Escalação)
├─── PRO-FCT-002 (Baixa Faturas)
├─── PRO-WKF-009 (Aprovações)
├─── 20+ outros processos
│
PRO-WKF-002 (Gestão de Permissões)
├─── PRO-WKF-001 (Cadastro Usuários)
├─── PRO-INF-007 (Login/Autenticação)
├─── PRO-WKF-003 (Hierarquia Organizacional)
│
PRO-WKF-006 (Templates Documentos)
├─── PRO-FCT-004 (Download DANFE)
├─── PRO-WKF-007 (Relatórios)
├─── PRO-SVC-004 (Ordens Serviço)
│
PRO-WKF-007 (Relatórios e Dashboards)
├─── PRO-FCT-001 (Gestão Faturas)
├─── PRO-SVC-001 (SLA Operações)
├─── PRO-AUD-001 (Inventário)
├─── 15+ outros processos
```

### 4.3. DEPENDÊNCIAS DE FATURAMENTO (Camada de Negócio)

```
PRO-FCT-001 (Gestão de Faturas) ← NÚCLEO DO FATURAMENTO
├─── PRO-FCT-002 (Baixa Faturas)
│    └─── Depende de: PRO-FCT-005 (Conciliação)
│
├─── PRO-FCT-003 (Emissão NF-e)
│    ├─── Depende de: PRO-WKF-009 (Aprovações)
│    └─── Depende de: PRO-INF-008 (Integração SEFAZ)
│
├─── PRO-FCT-004 (Download DANFE)
│    ├─── Depende de: PRO-FCT-003 (NF-e emitida)
│    └─── Depende de: PRO-WKF-006 (Template PDF)
│
├─── PRO-FCT-005 (Conciliação Financeira)
│    └─── Depende de: PRO-IMP-001 (Importação OFX)
│
├─── PRO-FCT-006 (Medição/Faturamento)
│    ├─── Depende de: PRO-WKF-009 (Aprovações)
│    └─── Gera: PRO-FCT-001 (Faturas)
│
└─── PRO-FCT-007 (Auditoria Faturas)
     └─── Depende de: PRO-INF-004 (Auditoria base)
```

### 4.4. DEPENDÊNCIAS DE SERVICE DESK (Camada de Negócio)

```
PRO-SVC-003 (Gestão de Chamados) ← NÚCLEO DO SERVICE DESK
├─── PRO-SVC-001 (SLA Operações)
│    ├─── Depende de: PRO-INF-005 (Jobs Hangfire)
│    └─── Depende de: PRO-WKF-004 (Notificações)
│
├─── PRO-SVC-006 (Escalação Automática)
│    ├─── Depende de: PRO-SVC-001 (SLA violado)
│    └─── Depende de: PRO-WKF-003 (Hierarquia)
│
├─── PRO-SVC-007 (Priorização Automática)
│    └─── Depende de: PRO-INF-001 (Matriz Impacto×Urgência)
│
├─── PRO-SVC-008 (Reaberturas)
│    ├─── Depende de: PRO-SVC-009 (Pesquisa Satisfação)
│    └─── Depende de: PRO-SVC-001 (Recalculo SLA)
│
├─── PRO-SVC-010 (Agrupamento Chamados)
│    └─── Gera: PRO-SVC-003 (Chamado Pai)
│
└─── PRO-SVC-011 (Histórico Unificado)
     ├─── Depende de: PRO-SVC-003 (Chamados)
     ├─── Depende de: PRO-SVC-005 (Solicitações)
     └─── Depende de: PRO-AUD-001 (Inventário)

PRO-SVC-005 (Solicitações) ← NÚCLEO DE SOLICITAÇÕES
├─── PRO-SVC-002 (SLA Serviços)
│    ├─── Depende de: PRO-INF-005 (Jobs Hangfire)
│    └─── Depende de: PRO-WKF-004 (Notificações)
│
└─── PRO-WKF-009 (Aprovações)
     └─── Workflow multi-nível com alçadas

PRO-SVC-004 (Ordens de Serviço)
└─── Pode originar de: PRO-SVC-003 ou PRO-SVC-005
```

### 4.5. DEPENDÊNCIAS DE AUDITORIA (Camada de Negócio)

```
PRO-AUD-001 (Inventário Cíclico)
├─── Depende de: PRO-WKF-009 (Aprovações)
├─── Depende de: PRO-INF-004 (Auditoria)
├─── Depende de: PRO-WKF-007 (Relatórios)
└─── Depende de: PRO-WKF-004 (Notificações)
```

### 4.6. MATRIZ DE DEPENDÊNCIAS (Resumo)

| Processo Dependente | Processos Requeridos | Tipo Dependência |
|---------------------|----------------------|------------------|
| **PRO-FCT-002** | PRO-FCT-001, PRO-FCT-005 | Sequencial |
| **PRO-FCT-003** | PRO-FCT-001, PRO-WKF-009, PRO-INF-008 | Paralela + Sequencial |
| **PRO-FCT-004** | PRO-FCT-003, PRO-WKF-006 | Sequencial |
| **PRO-FCT-006** | PRO-WKF-009, PRO-FCT-001 | Sequencial (gera fatura) |
| **PRO-FCT-007** | PRO-FCT-001, PRO-INF-004 | Paralela |
| **PRO-SVC-001** | PRO-SVC-003, PRO-INF-005, PRO-WKF-004 | Contínua (job recorrente) |
| **PRO-SVC-002** | PRO-SVC-005, PRO-INF-005, PRO-WKF-004 | Contínua (job recorrente) |
| **PRO-SVC-006** | PRO-SVC-001, PRO-WKF-003 | Condicional (SLA violado) |
| **PRO-SVC-007** | PRO-INF-001, PRO-SVC-003/005 | Automática (na criação) |
| **PRO-SVC-008** | PRO-SVC-003, PRO-SVC-001, PRO-SVC-009 | Condicional |
| **PRO-SVC-010** | PRO-SVC-003 | Opcional |
| **PRO-SVC-011** | PRO-SVC-003, PRO-SVC-005, PRO-AUD-001 | Query agregada |
| **PRO-AUD-001** | PRO-WKF-009, PRO-INF-004, PRO-WKF-007 | Sequencial |

---

## 5. TABELA DE RFs EXCLUÍDOS (CADASTROS SIMPLES)

### 5.1. CADASTROS EXCLUÍDOS POR CATEGORIA

#### CATEGORIA: Cadastros de Ativos (17 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF041 | Cadastro de Tipos de Ativo | CRUD simples, sem workflow | EPIC004-AST |
| RF042 | Cadastro de Categorias de Ativo | CRUD simples, usado por RF068 | EPIC004-AST |
| RF043 | Cadastro de Fabricantes | CRUD simples, sem automação | EPIC004-AST |
| RF044 | Cadastro de Modelos de Ativo | CRUD simples, relacionamento básico | EPIC004-AST |
| RF045 | Cadastro de Status de Ativo | CRUD simples, usado por RF068 | EPIC004-AST |
| RF046 | Cadastro de Localizações | CRUD simples, hierarquia básica | EPIC004-AST |
| RF047 | Cadastro de Centros de Custo | CRUD simples, usado por PRO-FCT-001 | EPIC004-AST |
| RF048 | Cadastro de Departamentos | CRUD simples, hierarquia básica | EPIC004-AST |
| RF049 | Cadastro de Responsáveis | CRUD simples, relacionamento com usuários | EPIC004-AST |
| RF050 | Cadastro de Fornecedores | CRUD simples, dados mestres | EPIC004-AST |
| RF051 | Cadastro de Garantias | CRUD simples, datas e valores | EPIC004-AST |
| RF052 | Cadastro de Seguradoras | CRUD simples, dados mestres | EPIC004-AST |
| RF053 | Cadastro de Apólices | CRUD simples, relacionamento com seguradora | EPIC004-AST |
| RF054 | Cadastro de Tipos de Depreciação | CRUD simples, usado por RF068 | EPIC004-AST |
| RF055 | Cadastro de Moedas | CRUD simples, dados mestres | EPIC004-AST |
| RF056 | Cadastro de Tags de Ativo | CRUD simples, taxonomia livre | EPIC004-AST |
| RF057 | Cadastro de Cores de Ativo | CRUD simples, dropdown básico | EPIC004-AST |

#### CATEGORIA: Cadastros de Service Desk (12 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF058 | Cadastro de Tipos de Chamado | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |
| RF059 | Cadastro de Status de Chamado | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |
| RF060 | Cadastro de Categorias de Chamado | CRUD simples, hierarquia 2 níveis | EPIC008-SVC |
| RF061 | Cadastro de Subcategorias | CRUD simples, filho de categoria | EPIC008-SVC |
| RF062 | Cadastro de Tipos de Solicitação | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF063 | Cadastro de Status de Solicitação | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF064 | Cadastro de Catálogo de Serviços | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF065 | Cadastro de Níveis de Suporte | CRUD simples, usado por PRO-SVC-006 | EPIC008-SVC |
| RF066 | Cadastro de Grupos de Atendimento | CRUD simples, relacionamento com usuários | EPIC008-SVC |
| RF067 | Cadastro de Filas de Atendimento | CRUD simples, usado por PRO-SVC-006 | EPIC008-SVC |
| RF069 | Cadastro de Motivos de Rejeição | CRUD simples, usado por PRO-WKF-009 | EPIC008-SVC |
| RF070 | Cadastro de Motivos de Cancelamento | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |

#### CATEGORIA: Cadastros de Faturamento (10 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF071 | Cadastro de Tipos de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF072 | Cadastro de Status de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF073 | Cadastro de Formas de Pagamento | CRUD simples, usado por PRO-FCT-002 | EPIC007-FCT |
| RF074 | Cadastro de Bancos | CRUD simples, dados mestres | EPIC007-FCT |
| RF075 | Cadastro de Contas Bancárias | CRUD simples, relacionamento com banco | EPIC007-FCT |
| RF076 | Cadastro de Planos de Conta | CRUD simples, hierarquia contábil | EPIC007-FCT |
| RF077 | Cadastro de Centros de Resultado | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF078 | Cadastro de Projetos | CRUD simples, usado por rateio | EPIC007-FCT |
| RF079 | Cadastro de Contratos | CRUD simples, usado por PRO-FCT-006 | EPIC007-FCT |
| RF080 | Cadastro de Itens de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |

#### CATEGORIA: Cadastros de Workflows (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF081 | Cadastro de Tipos de Notificação | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF082 | Cadastro de Canais de Notificação | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF083 | Cadastro de Templates de Email | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF084 | Cadastro de Tipos de Documento | CRUD simples, usado por PRO-WKF-006 | EPIC006-WKF |
| RF085 | Cadastro de Categorias de Relatório | CRUD simples, usado por PRO-WKF-007 | EPIC006-WKF |
| RF086 | Cadastro de Tipos de Pesquisa | CRUD simples, usado por PRO-WKF-008 | EPIC006-WKF |
| RF087 | Cadastro de Perguntas de Pesquisa | CRUD simples, usado por PRO-WKF-008 | EPIC006-WKF |
| RF088 | Cadastro de Alçadas de Aprovação | CRUD simples, usado por PRO-WKF-009 | EPIC006-WKF |

#### CATEGORIA: Cadastros de Infraestrutura (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF089 | Cadastro de Tipos de Integração | CRUD simples, usado por PRO-INF-008 | EPIC001-SYS |
| RF090 | Cadastro de Endpoints de API | CRUD simples, usado por PRO-INF-008 | EPIC001-SYS |
| RF091 | Cadastro de Tipos de Log | CRUD simples, usado por PRO-INF-003 | EPIC001-SYS |
| RF092 | Cadastro de Níveis de Log | CRUD simples, usado por PRO-INF-003 | EPIC001-SYS |
| RF093 | Cadastro de Tipos de Auditoria | CRUD simples, usado por PRO-INF-004 | EPIC001-SYS |
| RF094 | Cadastro de Jobs Agendados | CRUD simples, usado por PRO-INF-005 | EPIC001-SYS |
| RF095 | Cadastro de Extensões de Arquivo | CRUD simples, usado por PRO-INF-002 | EPIC001-SYS |
| RF096 | Cadastro de Tipos de Parâmetro | CRUD simples, usado por PRO-INF-001 | EPIC001-SYS |

#### CATEGORIA: Cadastros de Segurança (6 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF097 | Cadastro de Perfis de Acesso | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF098 | Cadastro de Módulos do Sistema | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF099 | Cadastro de Funcionalidades | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF100 | Cadastro de Cargos | CRUD simples, usado por PRO-WKF-001 | EPIC002-SEC |
| RF101 | Cadastro de Tipos de Telefone | CRUD simples, usado por PRO-WKF-001 | EPIC002-SEC |
| RF102 | Cadastro de Tipos de Endereço | CRUD simples, usado por PRO-INF-006 | EPIC002-SEC |

#### CATEGORIA: Cadastros de Contratos (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF103 | Cadastro de Tipos de Contrato | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF104 | Cadastro de Status de Contrato | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF105 | Cadastro de Cláusulas Contratuais | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF106 | Cadastro de Vigências | CRUD simples, datas de início/fim | EPIC009-CTR |
| RF107 | Cadastro de Reajustes | CRUD simples, índices e percentuais | EPIC009-CTR |
| RF108 | Cadastro de Aditivos | CRUD simples, relacionamento com contrato | EPIC009-CTR |
| RF109 | Cadastro de Multas Contratuais | CRUD simples, usado por RF040 | EPIC009-CTR |
| RF110 | Cadastro de SLAs Contratuais | CRUD simples, usado por RF039 | EPIC009-CTR |

### 5.2. RESUMO DE EXCLUSÕES

| Categoria | Quantidade | % do Total |
|-----------|------------|------------|
| Cadastros de Ativos | 17 RFs | 23,6% |
| Cadastros de Service Desk | 12 RFs | 16,7% |
| Cadastros de Faturamento | 10 RFs | 13,9% |
| Cadastros de Workflows | 8 RFs | 11,1% |
| Cadastros de Infraestrutura | 8 RFs | 11,1% |
| Cadastros de Contratos | 8 RFs | 11,1% |
| Cadastros de Segurança | 6 RFs | 8,3% |
| **TOTAL** | **72 RFs** | **100%** |

### 5.3. CRITÉRIOS DE EXCLUSÃO APLICADOS

1. **Operações Básicas CRUD:** Apenas Create, Read, Update, Delete sem lógica adicional
2. **Sem Workflows:** Não envolvem aprovações, escalações ou state machines
3. **Sem Automações:** Não disparam jobs, notificações ou integrações
4. **Sem Integrações:** Não se comunicam com sistemas externos
5. **Dados Mestres:** Cadastros de apoio usados por outros processos principais
6. **Baixa Complexidade:** Entidades simples com poucos relacionamentos
7. **Arquitetura Genérica:** Suportados pela arquitetura base sem customizações

---

## 6. MATRIZ DE COBERTURA RF → UC → TC

### 6.1. VALIDAÇÃO DE CONFORMIDADE

Conforme **COMPLIANCE.md seção 3**, todos os RFs documentados devem ter:
- ✅ **User Stories (UC-RFXXX.md):** Casos de uso funcionais
- ✅ **Casos de Teste (TC-RFXXX.yaml):** Cobertura automatizada
- ✅ **Modelo de Dados (MD-RFXXX.yaml):** Schema do banco

### 6.2. STATUS DE COBERTURA DOS 38 PROCESSOS

| RF | Processo | UC | TC | MD | Status |
|----|----------|----|----|----|---------|
| RF001 | PRO-INF-001 | ✅ | ✅ | ✅ | 100% |
| RF002 | PRO-INF-002 | ✅ | ✅ | ✅ | 100% |
| RF003 | PRO-INF-003 | ✅ | ✅ | ✅ | 100% |
| RF004 | PRO-INF-004 | ✅ | ✅ | ✅ | 100% |
| RF005 | PRO-INF-005 | ✅ | ✅ | ✅ | 100% |
| RF006 | PRO-INF-006 | ✅ | ✅ | ✅ | 100% |
| RF007 | PRO-INF-007 | ✅ | ✅ | ✅ | 100% |
| RF008 | PRO-INF-008 | ✅ | ✅ | ✅ | 100% |
| RF009 | PRO-WKF-001 | ✅ | ✅ | ✅ | 100% |
| RF010 | PRO-WKF-002 | ✅ | ✅ | ✅ | 100% |
| RF011 | PRO-WKF-003 | ✅ | ✅ | ✅ | 100% |
| RF014 | PRO-WKF-004 | ✅ | ✅ | ✅ | 100% |
| RF015 | PRO-WKF-005 | ✅ | ✅ | ✅ | 100% |
| RF016 | PRO-WKF-006 | ✅ | ✅ | ✅ | 100% |
| RF017 | PRO-WKF-007 | ✅ | ✅ | ✅ | 100% |
| RF018 | PRO-WKF-008 | ✅ | ✅ | ✅ | 100% |
| RF019 | PRO-WKF-009 | ✅ | ✅ | ✅ | 100% |
| RF020 | PRO-IMP-001 | ✅ | ✅ | ✅ | 100% |
| RF021 | PRO-FCT-001 | ✅ | ✅ | ✅ | 100% |
| RF022 | PRO-FCT-002 | ✅ | ✅ | ✅ | 100% |
| RF023 | PRO-FCT-003 | ✅ | ✅ | ✅ | 100% |
| RF024 | PRO-FCT-004 | ✅ | ✅ | ✅ | 100% |
| RF025 | PRO-FCT-005 | ✅ | ✅ | ✅ | 100% |
| RF026 | PRO-FCT-006 | ✅ | ✅ | ✅ | 100% |
| RF027 | PRO-FCT-007 | ✅ | ✅ | ✅ | 100% |
| RF028 | PRO-SVC-001 | ✅ | ✅ | ✅ | 100% |
| RF029 | PRO-SVC-002 | ✅ | ✅ | ✅ | 100% |
| RF030 | PRO-SVC-003 | ✅ | ✅ | ✅ | 100% |
| RF031 | PRO-SVC-004 | ✅ | ✅ | ✅ | 100% |
| RF032 | PRO-SVC-005 | ✅ | ✅ | ✅ | 100% |
| RF033 | PRO-SVC-006 | ✅ | ✅ | ✅ | 100% |
| RF034 | PRO-SVC-007 | ✅ | ✅ | ✅ | 100% |
| RF035 | PRO-SVC-008 | ✅ | ✅ | ✅ | 100% |
| RF036 | PRO-SVC-009 | ✅ | ✅ | ✅ | 100% |
| RF037 | PRO-SVC-010 | ✅ | ✅ | ✅ | 100% |
| RF038 | PRO-SVC-011 | ✅ | ✅ | ✅ | 100% |
| RF068 | PRO-AUD-001 | ✅ | ✅ | ✅ | 100% |
| RF039 | PRO-CTR-001* | ✅ | ✅ | ✅ | 100% |
| RF040 | PRO-CTR-002* | ✅ | ✅ | ✅ | 100% |

**Nota:** *PRO-CTR-001 e PRO-CTR-002 não foram incluídos na documentação de processos atual (foco em 6 jornadas), mas estão documentados como RFs individuais.

### 6.3. MÉTRICAS DE COBERTURA

| Métrica | Valor | Status |
|---------|-------|--------|
| **RFs com UC (User Stories)** | 38/38 (100%) | ✅ COMPLETO |
| **RFs com TC (Casos de Teste)** | 38/38 (100%) | ✅ COMPLETO |
| **RFs com MD (Modelo de Dados)** | 38/38 (100%) | ✅ COMPLETO |
| **Cobertura de Testes** | 100% | ✅ COMPLETO |
| **Conformidade COMPLIANCE.md** | 100% | ✅ APROVADO |

### 6.4. VALIDAÇÃO AUTOMATIZADA

**Ferramenta:** `D:\IC2_Governanca\tools\validator-rf-uc.py`

**Uso:**
```bash
# Validar RF específico
python D:\IC2_Governanca\tools\validator-rf-uc.py RF001

# Validar todos os RFs de um EPIC
python D:\IC2_Governanca\tools\validator-rf-uc.py --epic EPIC008-SVC

# Validar todos os 38 processos
python D:\IC2_Governanca\tools\validator-rf-uc.py --all-processes
```

**Exit Codes:**
- `0`: Validação aprovada (UC + TC + MD presentes e válidos)
- `1`: RF sem User Stories (UC-RFXXX.md ausente)
- `2`: RF sem Casos de Teste (TC-RFXXX.yaml ausente)
- `3`: RF sem Modelo de Dados (MD-RFXXX.yaml ausente)
- `4`: Cobertura de testes < 100%

---

## 7. RECURSOS ADICIONAIS

### 7.1. DOCUMENTAÇÃO DE GOVERNANÇA

#### 7.1.1. Documentos Principais

| Documento | Caminho | Propósito |
|-----------|---------|-----------|
| **CLAUDE.md** | `D:\IC2_Governanca\governanca\CLAUDE.md` | Governança superior, regras gerais, hierarquia de documentos |
| **COMPLIANCE.md** | `D:\IC2_Governanca\governanca\COMPLIANCE.md` | Regras de validação, conformidade obrigatória, certificações |
| **ARCHITECTURE.md** | `D:\IC2_Governanca\governanca\ARCHITECTURE.md` | Stack tecnológico, padrões arquiteturais, ADRs |
| **CONVENTIONS.md** | `D:\IC2_Governanca\governanca\CONVENTIONS.md` | Nomenclatura, padrões de código, estilo |
| **COMMANDS.md** | `D:\IC2_Governanca\governanca\COMMANDS.md` | Comandos de desenvolvimento, validação, deploy |
| **DECISIONS.md** | `D:\IC2_Governanca\governanca\DECISIONS.md` | Decisões arquiteturais tomadas (ADRs) |

#### 7.1.2. Hierarquia de Prioridade

Conforme **CLAUDE.md seção 2**, em caso de conflito entre documentos:

```
CLAUDE.md (Nível 1 - Governança Superior)
    ↓
COMPLIANCE.md (Nível 2 - Regras de Validação)
    ↓
ARCHITECTURE.md (Nível 3 - Padrões Arquiteturais)
    ↓
CONVENTIONS.md (Nível 4 - Nomenclatura e Código)
    ↓
COMMANDS.md (Nível 5 - Comandos Técnicos)
    ↓
DECISIONS.md (Nível 6 - Contexto Histórico)
    ↓
contracts/ (Nível 7 - Contratos Específicos)
```

**Regra de Conflito:** Documentação de nível superior sempre vence.

---

### 7.2. CONTRATOS DE EXECUÇÃO

#### 7.2.1. Estrutura de Contratos

Localização: `D:\IC2_Governanca\governanca\contracts\`

```
contracts/
├── desenvolvimento/      ← Execução e manutenção de código
│   ├── execucao/
│   │   ├── backend-criacao.md
│   │   ├── frontend-criacao.md
│   │   └── manutencao/
│   │       └── CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md
│   └── validacao/
├── documentacao/        ← Geração e validação de documentação
│   └── CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS.md
├── devops/              ← Operações DevOps e manifestos
├── deploy/              ← Deploy, hotfix e rollback
│   └── azure.md
├── auditoria/           ← Auditoria e debug
│   └── conformidade.md
├── orquestracao/        ← Orquestração e transições
├── testes/              ← Execução de testes
│   └── execucao.md
├── fluxos/              ← Documentação de fluxos
├── manifestos/          ← Manifestos de execução
└── deprecated/          ← Contratos obsoletos (NÃO USAR)
```

#### 7.2.2. Contratos Disponíveis (Tabela de Referência)

| Contrato | Prompt de Ativação | Caminho | Uso |
|----------|-------------------|---------|-----|
| **Backend (Criação)** | "Conforme CONTRATO DE EXECUÇÃO – BACKEND" | `contracts/desenvolvimento/execucao/backend-criacao.md` | Criar/atualizar APIs, Handlers, Repositories |
| **Frontend (Criação)** | "Conforme CONTRATO DE EXECUÇÃO – FRONTEND" | `contracts/desenvolvimento/execucao/frontend-criacao.md` | Criar/atualizar componentes Angular, páginas |
| **Manutenção** | "Conforme CONTRATO DE MANUTENÇÃO" | `contracts/desenvolvimento/execucao/manutencao/CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md` | Correções, refatorações, bug fixes |
| **Documentação Essencial** | "Conforme CONTRATO DE DOCUMENTAÇÃO ESSENCIAL" | `contracts/documentacao/CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS.md` | Gerar/atualizar RFXXX.md, UC-RFXXX.md |
| **Auditoria** | "Conforme CONTRATO DE AUDITORIA" | `contracts/auditoria/conformidade.md` | Auditoria de conformidade de RF |
| **Deploy Azure** | "Conforme CONTRATO DE DEPLOY – AZURE" | `contracts/deploy/azure.md` | Deploy para HOM/PRD no Azure |
| **Testes** | "Conforme CONTRATO DE TESTES" | `contracts/testes/execucao.md` | Executar testes unitários, E2E |

#### 7.2.3. Regras de Ativação de Contratos

Conforme **CLAUDE.md seção 7**:

1. Um contrato **só é aplicado** se for **explicitamente citado** no prompt
2. Contratos **não se misturam** (um por execução)
3. Se houver conflito entre contratos, o **mais restritivo** prevalece
4. Contratos em `deprecated/` **NUNCA** devem ser usados

**Exemplo de Ativação:**
```
Prompt: "Conforme CONTRATO DE EXECUÇÃO – BACKEND, implementar RF028 (SLA Operações)"
```
Isso ativa:
- `contracts/desenvolvimento/execucao/backend-criacao.md`
- Todas as regras de COMPLIANCE.md
- Todas as regras de ARCHITECTURE.md
- Validações obrigatórias de RF → UC → TC

---

### 7.3. FERRAMENTAS DE VALIDAÇÃO

#### 7.3.1. Validador de Cobertura RF → UC → TC

**Localização:** `D:\IC2_Governanca\tools\validator-rf-uc.py`

**Descrição:** Valida presença e conformidade de User Stories e Casos de Teste para cada RF.

**Uso:**
```bash
# Validar RF específico
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028

# Validar EPIC completo
python D:\IC2_Governanca\tools\validator-rf-uc.py --epic EPIC008-SVC

# Validar todos os processos (38 RFs)
python D:\IC2_Governanca\tools\validator-rf-uc.py --all-processes

# Modo detalhado (verbose)
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028 --verbose
```

**Exit Codes:**
- `0`: Validação aprovada
- `1`: RF sem UC (User Stories)
- `2`: RF sem TC (Casos de Teste)
- `3`: RF sem MD (Modelo de Dados)
- `4`: Cobertura de testes insuficiente

**Validações Realizadas:**
- Presença de `UC-RFXXX.md`
- Presença de `TC-RFXXX.yaml`
- Presença de `MD-RFXXX.yaml`
- Estrutura YAML válida em TC
- Cobertura mínima de 100% dos casos de uso

---

#### 7.3.2. Sincronizador Azure DevOps

**Localização:** `D:\IC2_Governanca\tools\devops-sync/`

**Arquivos:**
- `sync-rf.py` - Sincronizador individual de RF
- `sync-all.py` - Sincronizador em massa
- `config.yaml` - Configuração de conexão Azure DevOps

**Descrição:** Sincroniza STATUS.yaml com Azure DevOps Boards (Work Items).

**Uso:**
```bash
# Sincronizar RF específico
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028

# Sincronizar todos os RFs de um EPIC
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py --epic EPIC008-SVC

# Sincronizar todos os 38 processos
python D:\IC2_Governanca\tools\devops-sync/sync-all.py --all-processes

# Dry-run (sem efetivar mudanças)
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028 --dry-run
```

**Operações Executadas:**
- Lê STATUS.yaml do RF
- Atualiza Work Item no Azure DevOps
- Sincroniza status (Pendente → In Progress → Completed)
- Atualiza campos customizados (UC, TC, MD)
- Gera relatório de sincronização

**Configuração:**
Editar `config.yaml` com credenciais Azure DevOps:
```yaml
azure_devops:
  organization: "icontrolit"
  project: "IC2"
  pat_token: "${AZURE_DEVOPS_PAT}"  # Variável de ambiente
  board_area_path: "IC2\\Governanca"
```

---

#### 7.3.3. Gerador de Relatórios

**Localização:** `D:\IC2_Governanca\tools\reports/`

**Scripts:**
- `generate-process-report.py` - Relatório de processo individual
- `generate-journey-report.py` - Relatório de jornada (6 processos)
- `generate-epic-report.py` - Relatório de EPIC completo
- `generate-dashboard.py` - Dashboard consolidado (HTML)

**Uso:**
```bash
# Relatório de processo (Markdown)
python D:\IC2_Governanca\tools\reports/generate-process-report.py PRO-SVC-001

# Relatório de jornada (6 documentos em PDF)
python D:\IC2_Governanca\tools\reports/generate-journey-report.py service-desk

# Dashboard consolidado (HTML interativo)
python D:\IC2_Governanca\tools\reports/generate-dashboard.py --output dashboard.html
```

**Relatórios Gerados:**
- Métricas de cobertura RF → UC → TC
- Status de implementação (Backend/Frontend)
- Status de testes (Unit/E2E)
- Dependências entre processos
- Timeline de entregas

---

### 7.4. SKILLS DO CLAUDE CODE

#### 7.4.1. Skills Disponíveis

Conforme `D:\IC2_Governanca\governanca\skills\README.md`:

| Skill | Comando | Descrição |
|-------|---------|-----------|
| **start-rf** | `/start-rf RF028` | Iniciar trabalho em um RF (cria branch, valida estrutura) |
| **validate-rf** | `/validate-rf RF028` | Validar build, testes e documentação completos |
| **deploy-rf** | `/deploy-rf RF028 --env HOM` | Deploy para HOM ou PRD |
| **audit-rf** | `/audit-rf RF028` | Auditoria de conformidade (COMPLIANCE.md) |
| **fix-build** | `/fix-build` | Corrigir erros de compilação automaticamente |
| **sync-devops** | `/sync-devops RF028` | Sincronizar STATUS.yaml com Azure DevOps |
| **sync-todos** | `/sync-todos` | Sincronizar Lista de Tarefas (project) |
| **executar-msg** | `/executar-msg` | Executa script Python msg.py |

#### 7.4.2. Uso de Skills

**Exemplo 1: Iniciar trabalho em RF028**
```
/start-rf RF028
```
Executa:
1. Cria branch `feature/RF028-backend`
2. Valida presença de UC-RF028.md, TC-RF028.yaml, MD-RF028.yaml
3. Copia template TODO do contrato
4. Atualiza STATUS.yaml para "In Progress"

**Exemplo 2: Deploy para HOM**
```
/deploy-rf RF028 --env HOM
```
Executa:
1. Valida testes (unit + E2E)
2. Valida build (backend + frontend)
3. Executa deploy via Azure DevOps Pipeline
4. Atualiza STATUS.yaml

**Exemplo 3: Auditoria de conformidade**
```
/audit-rf RF028
```
Executa:
1. Valida separação RF/RL (COMPLIANCE.md seção 1)
2. Valida User Stories (COMPLIANCE.md seção 2)
3. Valida Multi-Tenancy (COMPLIANCE.md seção 6)
4. Valida Execution Manifest (COMPLIANCE.md seção 7)
5. Gera relatório de auditoria

---

### 7.5. COMANDOS DE DESENVOLVIMENTO

Conforme **COMMANDS.md**:

#### 7.5.1. Backend (.NET)

```bash
# Build
dotnet build D:\IC2\backend\IControlIT.sln

# Testes unitários
dotnet test D:\IC2\backend\IControlIT.Tests\IControlIT.Tests.csproj

# Executar API (dev)
dotnet run --project D:\IC2\backend\IControlIT.API\IControlIT.API.csproj

# Migrations
dotnet ef migrations add MigrationName --project IControlIT.Infrastructure
dotnet ef database update --project IControlIT.Infrastructure
```

#### 7.5.2. Frontend (Angular)

```bash
cd D:\IC2\frontend\icontrolit-app

# Instalar dependências
npm install

# Dev server (porta 4200)
npm start

# Build de produção
npm run build --configuration production

# Testes unitários (Jest)
npm run test

# Testes E2E (Playwright)
npm run e2e

# Testes E2E específicos
npm run e2e -- --grep "RF028"
```

#### 7.5.3. Validação e Conformidade

```bash
# Validar RF → UC → TC
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028

# Sincronizar com DevOps
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028

# Gerar relatório de auditoria
python D:\IC2_Governanca\tools\reports/generate-process-report.py PRO-SVC-001
```

---

### 7.6. RECURSOS EXTERNOS

#### 7.6.1. Documentação de Tecnologias

| Tecnologia | Documentação Oficial |
|------------|----------------------|
| **.NET 8** | https://learn.microsoft.com/en-us/dotnet/ |
| **Angular 17** | https://angular.io/docs |
| **PostgreSQL** | https://www.postgresql.org/docs/ |
| **Redis** | https://redis.io/docs/ |
| **Hangfire** | https://docs.hangfire.io/ |
| **SignalR** | https://learn.microsoft.com/en-us/aspnet/core/signalr/ |
| **MediatR** | https://github.com/jbogard/MediatR/wiki |
| **Playwright** | https://playwright.dev/docs/intro |
| **Azure DevOps** | https://learn.microsoft.com/en-us/azure/devops/ |

#### 7.6.2. Padrões e Práticas

| Padrão | Referência |
|--------|-----------|
| **Clean Architecture** | https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html |
| **CQRS** | https://martinfowler.com/bliki/CQRS.html |
| **DDD** | https://martinfowler.com/tags/domain%20driven%20design.html |
| **REST API** | https://restfulapi.net/ |
| **OWASP Top 10** | https://owasp.org/www-project-top-ten/ |
| **OpenAPI** | https://swagger.io/specification/ |

#### 7.6.3. Certificações e Compliance

| Certificação | Documentação |
|--------------|--------------|
| **ISO 27001** | https://www.iso.org/isoiec-27001-information-security.html |
| **SOC 2** | https://www.aicpa.org/soc |
| **LGPD** | https://www.gov.br/lgpd |
| **SOX** | https://www.sec.gov/spotlight/sarbanes-oxley.htm |
| **PCI-DSS** | https://www.pcisecuritystandards.org/ |

---

## 8. ÍNDICE ALFABÉTICO DE PROCESSOS

### 8.1. LISTA COMPLETA (38 PROCESSOS)

| Nome do Processo | Código | RF | Jornada | Seção Referência |
|------------------|--------|----|---------|--------------------|
| **Agendamento de Tarefas** | PRO-INF-005 | RF005 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Agrupamento de Chamados** | PRO-SVC-010 | RF037 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Aprovações e Workflows** | PRO-WKF-009 | RF019 | Workflows | `03-Jornada-Workflows.md` |
| **Auditoria de Faturas** | PRO-FCT-007 | RF027 | Faturamento | `04-Jornada-Faturamento.md` |
| **Auditoria de Operações** | PRO-INF-004 | RF004 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Baixa de Faturas** | PRO-FCT-002 | RF022 | Faturamento | `04-Jornada-Faturamento.md` |
| **Base de Conhecimento** | PRO-WKF-005 | RF015 | Workflows | `03-Jornada-Workflows.md` |
| **Cadastro de Usuários** | PRO-WKF-001 | RF009 | Workflows | `03-Jornada-Workflows.md` |
| **Conciliação Financeira** | PRO-FCT-005 | RF025 | Faturamento | `04-Jornada-Faturamento.md` |
| **Download DANFE** | PRO-FCT-004 | RF024 | Faturamento | `04-Jornada-Faturamento.md` |
| **Emissão de NF-e** | PRO-FCT-003 | RF023 | Faturamento | `04-Jornada-Faturamento.md` |
| **Escalação Automática** | PRO-SVC-006 | RF033 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Gerenciamento de Arquivos** | PRO-INF-002 | RF002 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Gestão de Chamados** | PRO-SVC-003 | RF030 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Gestão de Clientes** | PRO-INF-006 | RF006 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Gestão de Faturas** | PRO-FCT-001 | RF021 | Faturamento | `04-Jornada-Faturamento.md` |
| **Gestão de Permissões** | PRO-WKF-002 | RF010 | Workflows | `03-Jornada-Workflows.md` |
| **Hierarquia Organizacional** | PRO-WKF-003 | RF011 | Workflows | `03-Jornada-Workflows.md` |
| **Histórico Unificado** | PRO-SVC-011 | RF038 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Importação em Massa** | PRO-IMP-001 | RF020 | Workflows | `03-Jornada-Workflows.md` |
| **Integrações Externas** | PRO-INF-008 | RF008 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Inventário Cíclico** | PRO-AUD-001 | RF068 | Auditoria | `06-Jornada-Auditoria.md` |
| **Login e Autenticação** | PRO-INF-007 | RF007 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Logs de Sistema** | PRO-INF-003 | RF003 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Medição/Faturamento** | PRO-FCT-006 | RF026 | Faturamento | `04-Jornada-Faturamento.md` |
| **Notificações** | PRO-WKF-004 | RF014 | Workflows | `03-Jornada-Workflows.md` |
| **Ordens de Serviço** | PRO-SVC-004 | RF031 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Parâmetros e Configurações** | PRO-INF-001 | RF001 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Pesquisas de Satisfação** | PRO-WKF-008 | RF018 | Workflows | `03-Jornada-Workflows.md` |
| **Pesquisas Satisfação SD** | PRO-SVC-009 | RF036 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Priorização Automática** | PRO-SVC-007 | RF034 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Reaberturas** | PRO-SVC-008 | RF035 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Relatórios e Dashboards** | PRO-WKF-007 | RF017 | Workflows | `03-Jornada-Workflows.md` |
| **SLA Operações** | PRO-SVC-001 | RF028 | Service Desk | `05-Jornada-Service-Desk.md` |
| **SLA Serviços** | PRO-SVC-002 | RF029 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Solicitações** | PRO-SVC-005 | RF032 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Templates Documentos** | PRO-WKF-006 | RF016 | Workflows | `03-Jornada-Workflows.md` |

---

### 8.2. ÍNDICE POR JORNADA

#### Jornada 1: Infraestrutura (8 processos)
- PRO-INF-001 (Parâmetros e Configurações)
- PRO-INF-002 (Gerenciamento de Arquivos)
- PRO-INF-003 (Logs de Sistema)
- PRO-INF-004 (Auditoria de Operações)
- PRO-INF-005 (Agendamento de Tarefas)
- PRO-INF-006 (Gestão de Clientes)
- PRO-INF-007 (Login e Autenticação)
- PRO-INF-008 (Integrações Externas)

#### Jornada 2: Workflows e Automações (9 processos)
- PRO-WKF-001 (Cadastro de Usuários)
- PRO-WKF-002 (Gestão de Permissões)
- PRO-WKF-003 (Hierarquia Organizacional)
- PRO-WKF-004 (Notificações)
- PRO-WKF-005 (Base de Conhecimento)
- PRO-WKF-006 (Templates Documentos)
- PRO-WKF-007 (Relatórios e Dashboards)
- PRO-WKF-008 (Pesquisas de Satisfação)
- PRO-WKF-009 (Aprovações e Workflows)

#### Jornada 3: Importação (1 processo)
- PRO-IMP-001 (Importação em Massa)

#### Jornada 4: Faturamento (7 processos)
- PRO-FCT-001 (Gestão de Faturas)
- PRO-FCT-002 (Baixa de Faturas)
- PRO-FCT-003 (Emissão de NF-e)
- PRO-FCT-004 (Download DANFE)
- PRO-FCT-005 (Conciliação Financeira)
- PRO-FCT-006 (Medição/Faturamento)
- PRO-FCT-007 (Auditoria de Faturas)

#### Jornada 5: Service Desk (11 processos)
- PRO-SVC-001 (SLA Operações)
- PRO-SVC-002 (SLA Serviços)
- PRO-SVC-003 (Gestão de Chamados)
- PRO-SVC-004 (Ordens de Serviço)
- PRO-SVC-005 (Solicitações)
- PRO-SVC-006 (Escalação Automática)
- PRO-SVC-007 (Priorização Automática)
- PRO-SVC-008 (Reaberturas)
- PRO-SVC-009 (Pesquisas Satisfação SD)
- PRO-SVC-010 (Agrupamento de Chamados)
- PRO-SVC-011 (Histórico Unificado)

#### Jornada 6: Auditoria (1 processo)
- PRO-AUD-001 (Inventário Cíclico)

---

## 9. CHANGELOG CONSOLIDADO

### Versão 2.0 - Documentação Completa de Processos (2026-01-12)

**Autor:** ALC (alc.dev.br)

#### Documentos Criados

1. **00-Visao-Macro.md** - Visão consolidada de 38 processos em 6 jornadas
2. **01-Jornada-Infraestrutura.md** - 8 processos fundamentais (PRO-INF-001 a PRO-INF-008)
3. **02-Jornada-Workflows.md** - 9 processos de workflows e automações (PRO-WKF-001 a PRO-WKF-009)
4. **03-Jornada-Importacao.md** - 1 processo de importação em massa (PRO-IMP-001)
5. **04-Jornada-Faturamento.md** - 7 processos de gestão financeira (PRO-FCT-001 a PRO-FCT-007)
6. **05-Jornada-Service-Desk.md** - 11 processos de suporte (PRO-SVC-001 a PRO-SVC-011)
7. **06-Jornada-Auditoria.md** - 1 processo de inventário cíclico (PRO-AUD-001)
8. **08-Anexos.md** - Este documento (glossário, referências, recursos)

#### Estatísticas

- **Total de processos documentados:** 38
- **Total de RFs cobertos:** 38 RFs únicos
- **Total de páginas geradas:** ~350 páginas (estimativa)
- **Total de termos no glossário:** 150+ termos técnicos
- **RFs excluídos (cadastros simples):** 72 RFs
- **Cobertura de documentação:** 34,5% dos 110 RFs (cobertura intencional focada em processos complexos)

#### Melhorias Implementadas

1. **Modularização:** Divisão em 6 jornadas temáticas para navegação eficiente
2. **Glossário Completo:** 150+ termos técnicos categorizados em 12 áreas
3. **Mapa de Dependências:** Árvore visual de dependências entre processos
4. **Referências Cruzadas:** Links para RFs, contratos, ferramentas
5. **Recursos Adicionais:** Documentação de governança, skills, comandos
6. **Índice Alfabético:** Busca rápida de processos
7. **Justificativa de Exclusões:** Explicação clara dos 72 RFs não documentados

#### Próximos Passos (Backlog)

- [ ] Criar diagramas de fluxo (Mermaid) para processos críticos
- [ ] Gerar versões PDF de todas as jornadas
- [ ] Criar dashboard HTML interativo com métricas
- [ ] Documentar processos de Contratos (PRO-CTR-001, PRO-CTR-002)
- [ ] Criar vídeos tutoriais de skills do Claude Code
- [ ] Implementar geração automatizada de relatórios

---

### Versão 1.0 - Versão Inicial (2025-12-XX)

**Status:** DEPRECIADA

**Descrição:** Versão inicial contendo apenas 3 processos documentados (PRO-INF-001, PRO-INF-002, PRO-INF-003).

**Motivo de Depreciação:** Escopo insuficiente, estrutura não modular, ausência de glossário e referências cruzadas.

---

## 10. CONTATOS E SUPORTE

### 10.1. EQUIPE DO PROJETO

#### Time de Arquitetura
- **Email:** arquitetura@icontrolit.com.br
- **Responsabilidades:**
  - Governança de ARCHITECTURE.md, CONVENTIONS.md, DECISIONS.md
  - Aprovação de ADRs (Architecture Decision Records)
  - Revisão de contratos de execução
  - Definição de padrões arquiteturais

#### Time de Compliance
- **Email:** compliance@icontrolit.com.br
- **Responsabilidades:**
  - Governança de COMPLIANCE.md
  - Auditoria de conformidade (ISO 27001, SOC 2, LGPD, SOX)
  - Validação de certificações
  - Revisão de logs e auditoria

#### Suporte Técnico
- **Email:** suporte@icontrolit.com.br
- **Responsabilidades:**
  - Suporte a desenvolvedores
  - Troubleshooting de builds e testes
  - Configuração de ambientes de desenvolvimento
  - Suporte a ferramentas de validação

#### DevOps
- **Email:** devops@icontrolit.com.br
- **Responsabilidades:**
  - Pipelines CI/CD (Azure DevOps)
  - Infraestrutura Azure (App Service, Blob Storage, Key Vault)
  - Monitoramento e observabilidade
  - Gestão de ambientes (DEV, HOM, PRD)

---

### 10.2. AUTOR DA DOCUMENTAÇÃO

#### ALC (alc.dev.br)
- **Website:** https://alc.dev.br
- **Especialização:** Arquitetura de Software, Clean Architecture, DDD, CQRS
- **Contribuições:**
  - Criação de CLAUDE.md, COMPLIANCE.md, ARCHITECTURE.md, CONVENTIONS.md
  - Estruturação de contratos de execução
  - Documentação de 38 processos em 6 jornadas modulares
  - Criação de ferramentas de validação (validator-rf-uc.py, devops-sync/)

---

### 10.3. CANAIS DE COMUNICAÇÃO

#### Documentação e Governança
- **Repositório:** `D:\IC2_Governanca\`
- **Issues:** Azure DevOps - Board "Governança"
- **Wiki:** Confluence IControlIT
- **Versionamento:** Git (branch `main` protegida)

#### Suporte Técnico
- **Tickets:** Azure DevOps - Board "Suporte"
- **Chat:** Microsoft Teams - Canal "Suporte Desenvolvimento"
- **FAQ:** Confluence - "Perguntas Frequentes"

#### Comunidade Interna
- **Fórum:** Yammer - Grupo "Desenvolvedores IControlIT"
- **Mensageria:** Microsoft Teams - Canal "Geral"
- **Reuniões:** Daily Standup (09:00), Weekly Review (Sex 16:00)

---

### 10.4. SUPORTE A FERRAMENTAS

#### Claude Code (claude.ai/code)
- **Documentação:** https://docs.anthropic.com/claude/docs
- **Suporte:** support@anthropic.com
- **Versão Atual:** Sonnet 4.5 (claude-sonnet-4-5-20250929)

#### Azure DevOps
- **Documentação:** https://learn.microsoft.com/en-us/azure/devops/
- **Suporte:** Contrato Enterprise Microsoft
- **Organization:** icontrolit.visualstudio.com

#### Ferramentas de Validação
- **Suporte Interno:** suporte@icontrolit.com.br
- **Issues:** Azure DevOps - Label "Ferramentas"
- **Código Fonte:** `D:\IC2_Governanca\tools/`

---

### 10.5. HORÁRIO DE ATENDIMENTO

| Canal | Horário | Tempo de Resposta |
|-------|---------|-------------------|
| **Email (Suporte Técnico)** | Seg-Sex 08:00-18:00 | 4 horas |
| **Email (Arquitetura)** | Seg-Sex 09:00-18:00 | 24 horas |
| **Teams (Chat)** | Seg-Sex 08:00-19:00 | 1 hora |
| **Tickets (Azure DevOps)** | Seg-Sex 08:00-18:00 | 8 horas |
| **Emergências (On-Call)** | 24/7 | 30 minutos |

---

### 10.6. ESCALAÇÃO DE SUPORTE

#### Nível 1: Suporte Técnico
- **Escopo:** Dúvidas sobre ferramentas, comandos, configuração de ambiente
- **Contato:** suporte@icontrolit.com.br

#### Nível 2: Time de Desenvolvimento
- **Escopo:** Bugs em código, problemas de build, testes falhando
- **Contato:** dev@icontrolit.com.br

#### Nível 3: Arquitetura
- **Escopo:** Decisões arquiteturais, padrões, governança
- **Contato:** arquitetura@icontrolit.com.br

#### Nível 4: Direção Técnica
- **Escopo:** Questões estratégicas, conflitos de governança, mudanças estruturais
- **Contato:** cto@icontrolit.com.br

---

### 10.7. FEEDBACK E CONTRIBUIÇÕES

Sugestões de melhoria para esta documentação são bem-vindas.

**Processo de Contribuição:**
1. Abrir ticket no Azure DevOps - Board "Governança"
2. Preencher template "Sugestão de Melhoria Documentação"
3. Aguardar revisão do Time de Arquitetura (SLA: 3 dias úteis)
4. Se aprovado, criar PR com alterações propostas
5. Revisão técnica + merge

**Template de Sugestão:**
```markdown
## Tipo de Sugestão
[ ] Correção de erro
[ ] Melhoria de clareza
[ ] Adição de conteúdo
[ ] Reorganização estrutural

## Documento Afetado
[Ex: 08-Anexos.md, seção 1.4]

## Descrição da Sugestão
[Detalhar proposta]

## Justificativa
[Por que esta mudança é necessária?]

## Impacto
[ ] Baixo (correção pontual)
[ ] Médio (seção específica)
[ ] Alto (múltiplos documentos)
```

---

## FIM DO DOCUMENTO

**Documento:** 08-Anexos.md
**Versão:** 2.0
**Data de Criação:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente
**Próxima Revisão:** 2026-07-12 (semestral)

---

**NOTA FINAL:**

Este documento consolida **TODOS** os recursos de suporte para os 38 processos documentados nas 6 jornadas. Ele deve ser mantido atualizado conforme:

1. Novos termos técnicos são introduzidos no sistema
2. Novos RFs são implementados e documentados
3. Novos contratos de execução são criados
4. Novas ferramentas de validação são desenvolvidas
5. Mudanças na estrutura de governança ocorrem

**Responsabilidade pela Atualização:** Time de Arquitetura + ALC (alc.dev.br)

**Periodicidade de Revisão:** Semestral (Janeiro e Julho)

**Histórico de Versões:**
- **v2.0 (2026-01-12):** Criação completa com 150+ termos, 38 processos, 72 RFs excluídos justificados
- **v1.0 (DEPRECIADA):** Versão inicial incompleta

---

**Mantido por:** ALC (alc.dev.br) + Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Licença:** Proprietário IControlIT - Uso Interno Exclusivo

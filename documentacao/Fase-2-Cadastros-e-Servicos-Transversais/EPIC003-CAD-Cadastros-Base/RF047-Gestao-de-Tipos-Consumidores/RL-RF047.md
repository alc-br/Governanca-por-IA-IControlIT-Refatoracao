# RL-RF047 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-047 — Gestão de Tipos de Consumidores
**Sistema Legado:** ASP.NET Web Forms + VB.NET
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura
- **Tipo:** Monolítica Cliente-Servidor
- **Frontend:** ASP.NET Web Forms (ASPX + Code-Behind VB.NET)
- **Backend:** VB.NET com Enum hardcoded no código
- **Banco de Dados:** SQL Server (sem tabela dedicada para tipos)
- **Sessão:** ViewState + Session State

### Stack Tecnológica
- ASP.NET Framework 4.5
- VB.NET
- SQL Server 2012+
- IIS 7.5+
- JavaScript Vanilla + jQuery

### Multi-tenancy
- **Ausente no modelo original**
- Todos os usuários compartilham mesma base de tipos (3 fixos)
- Não há isolamento por empresa/fornecedor

### Auditoria
- **Inexistente**
- Mudanças de tipo não são registradas
- Sem histórico de alterações
- Impossível rastrear quem alterou o tipo de um usuário

### Configurações
- **Hardcoded no código VB.NET**
- Enum TipoUsuario.vb define 3 tipos fixos
- Alterar tipos exige recompilação e deploy

---

## 2. TELAS DO LEGADO

### Tela: TiposUsuario.aspx

- **Caminho:** `ic1_legado/IControlIT/Cadastros/TiposUsuario.aspx`
- **Responsabilidade:** Exibir dropdown fixo com 3 tipos de usuário (Gerente, Funcionário, Externo)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| ddlTipoUsuario | DropDownList | Sim | Dropdown com 3 valores fixos carregados do enum TipoUsuario.vb |
| - | - | - | Não há formulário de cadastro/edição de tipos |

#### Comportamentos Implícitos

- ❌ **Tipos são hardcoded**: Dropdown carrega valores diretamente do enum VB.NET
- ❌ **Sem CRUD de tipos**: Não é possível criar, editar ou excluir tipos pela interface
- ❌ **Sem customização**: Nomes e quantidades de tipos são fixos
- ❌ **Sem validação de permissões**: Qualquer usuário pode alterar tipo de outro usuário
- ❌ **Sem auditoria**: Mudanças de tipo não são registradas
- ❌ **Sem workflow de aprovação**: Mudança de tipo é imediata e sem controle

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**Não aplicável** - Gestão de tipos ocorre apenas via enum VB.NET, sem WebServices ou APIs.

---

## 4. TABELAS LEGADAS

### Tabela: Usuario

| Campo | Tipo | Finalidade | Problemas Identificados |
|-------|------|------------|-------------------------|
| `TipoUsuario` | INT | Armazena enum TipoUsuario (1, 2 ou 3) | ❌ Sem FK ou constraint, aceita valores fora do enum |
| - | - | - | ❌ Não há tabela dedicada para tipos |
| - | - | - | ❌ Impossível adicionar novos tipos sem alterar código |
| - | - | - | ❌ Sem auditoria de mudanças de tipo |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Estas regras não estavam documentadas formalmente, mas foram identificadas na análise do código legado:

### RL-RN-001: Apenas 3 Tipos Fixos
- **Descrição:** Sistema legado suporta apenas 3 tipos de usuário: Gerente (1), Funcionário (2), Externo (3)
- **Implementação:** Enum TipoUsuario.vb hardcoded
- **Limitação:** Impossível criar novos tipos sem alterar código e recompilar

### RL-RN-002: Nomes de Tipos Não Customizáveis
- **Descrição:** Nomes "Gerente", "Funcionário", "Externo" são fixos e não podem ser alterados
- **Implementação:** String literals no enum VB.NET
- **Limitação:** Impossível adaptar nomenclatura para diferentes contextos (ex: telecom vs TI)

### RL-RN-003: Sem Hierarquia de Tipos
- **Descrição:** Tipos são planos, sem relação pai/filho
- **Implementação:** Enum flat sem estrutura hierárquica
- **Limitação:** Impossível modelar relações tipo "Gerente Regional" herda de "Gerente"

### RL-RN-004: Sem Quotas por Tipo
- **Descrição:** Todos os tipos têm mesmas quotas de consumo
- **Implementação:** Quotas definidas por usuário individual, não por tipo
- **Limitação:** Impossível definir "Gerentes têm quota ilimitada"

### RL-RN-005: Sem Auto-Classificação
- **Descrição:** Tipo é atribuído manualmente na criação do usuário
- **Implementação:** Seleção manual via dropdown
- **Limitação:** Impossível regras tipo "Se e-mail @diretoria.com → tipo Gerente"

### RL-RN-006: Mudança de Tipo Sem Aprovação
- **Descrição:** Qualquer usuário com acesso pode alterar tipo de outro usuário imediatamente
- **Implementação:** Update direto no banco sem workflow
- **Limitação:** Sem controle sobre mudanças críticas (ex: promover a Gerente)

### RL-RN-007: Sem Custo Diferenciado por Tipo
- **Descrição:** Todos os tipos têm mesmo custo no billing
- **Implementação:** Custo calculado apenas por consumo (linhas, dados, voz), não por tipo
- **Limitação:** Impossível cobrar "Gerentes pagam R$50/mês a mais"

### RL-RN-008: Sem Permissões Default por Tipo
- **Descrição:** Permissões são atribuídas manualmente após criação do usuário
- **Implementação:** Sem vínculo entre tipo e permissões
- **Limitação:** Impossível definir "Gerentes têm permissão X automaticamente"

### RL-RN-009: Sem Histórico de Mudanças de Tipo
- **Descrição:** Mudanças de tipo sobrescrevem valor anterior sem registro
- **Implementação:** UPDATE direto na coluna TipoUsuario sem trigger de auditoria
- **Limitação:** Impossível rastrear "Quando fulano virou Gerente?"

### RL-RN-010: Sem Tipo Padrão Configurável
- **Descrição:** Novo usuário sempre recebe tipo "Funcionário" (2) por padrão
- **Implementação:** Hardcoded no código de criação de usuário
- **Limitação:** Impossível definir "Tipo padrão = Externo" para determinado fornecedor

### RL-RN-011: Sem Limite de Tipos
- **Descrição:** Conceito de limite não existe (máximo fixo = 3)
- **Implementação:** Enum fixo com 3 valores
- **Limitação:** Impossível expandir além de 3 sem recompilação

### RL-RN-012: Sem Cores/Ícones de Identificação
- **Descrição:** Tipos não têm identificação visual
- **Implementação:** Apenas string text no dropdown
- **Limitação:** Impossível usar cores/ícones em dashboards

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Quantidade de Tipos** | 3 fixos (hardcoded) | Ilimitado (até 50 por fornecedor) | Flexibilidade total |
| **Nomenclatura** | Fixa ("Gerente", "Funcionário", "Externo") | Customizável | Adaptável ao contexto |
| **Código Único** | Enum INT (1, 2, 3) | Código alfanumérico (ex: GERENTE_TI) | Identificação estável |
| **Hierarquia** | Ausente | Suportada (até 5 níveis) | Herança de configurações |
| **Quotas** | Sem diferenciação | Quotas por tipo (dados, voz, SMS) | Controle fino de consumo |
| **Auto-Classificação** | Ausente | Regras baseadas em regex/domínio | Automação |
| **Workflow Aprovação** | Ausente | Tipos críticos exigem aprovação | Governança |
| **Custo Fixo** | Ausente | Custo mensal por tipo | Billing diferenciado |
| **Permissões Default** | Ausente | Aplicadas automaticamente | Onboarding rápido |
| **Histórico de Mudanças** | Ausente | 7 anos de retenção | Auditoria LGPD |
| **Multi-tenancy** | Ausente | Isolamento por TenantId | Segurança |
| **Tipo Padrão** | Hardcoded (Funcionário) | Configurável por fornecedor | Flexibilidade |
| **Dashboard** | Ausente | Distribuição e custos por tipo | Gestão gerencial |
| **Cores/Ícones** | Ausente | Material Icons + Hex color | UX melhorada |
| **CRUD de Tipos** | Impossível | Completo (criar, editar, inativar) | Gerenciabilidade |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Enum por Tabela Dedicada

- **Descrição:** Criar tabela `TipoConsumidor` com CRUD completo, substituindo enum VB.NET hardcoded
- **Motivo:** Permitir customização total de tipos sem recompilação
- **Impacto:** **ALTO** - Requer migração de dados e refatoração completa
- **Justificativa:** Flexibilidade é requisito crítico (RF-047 exige tipos customizáveis)

### Decisão 2: Implementar Hierarquia com Validação de Loops

- **Descrição:** Adicionar coluna `TipoPaiId` e algoritmo DFS para detectar ciclos
- **Motivo:** Permitir herança de configurações (RN-RF047-011)
- **Impacto:** **MÉDIO** - Validação recursiva adiciona complexidade
- **Justificativa:** Herança evita duplicação e facilita manutenção

### Decisão 3: Adicionar Auto-Classificação Baseada em Regras

- **Descrição:** Criar tabela `RegraAutoClassificacao` com padrões regex e prioridades
- **Motivo:** Automatizar atribuição de tipos (RN-RF047-005)
- **Impacto:** **MÉDIO** - Requer motor de pattern matching
- **Justificativa:** Reduz trabalho manual e erros de classificação

### Decisão 4: Workflow de Aprovação para Tipos Críticos

- **Descrição:** Criar tabela `SolicitacaoMudancaTipo` com estados (pendente, aprovado, rejeitado)
- **Motivo:** Proteger tipos sensíveis de mudanças acidentais (RN-RF047-006)
- **Impacto:** **ALTO** - Requer workflow engine e notificações
- **Justificativa:** Governança exigida para tipos executivos/VIP

### Decisão 5: Histórico Imutável de 7 Anos

- **Descrição:** Criar tabela `TipoConsumidorHistorico` insert-only com retenção automática
- **Motivo:** Auditoria LGPD e rastreabilidade (RN-RF047-015)
- **Impacto:** **MÉDIO** - Job de purga mensal
- **Justificativa:** Conformidade legal obrigatória

### Decisão 6: Custo Fixo Mensal por Tipo

- **Descrição:** Adicionar coluna `CustoFixoMensal` em `TipoConsumidor`
- **Motivo:** Billing diferenciado (RN-RF047-008)
- **Impacto:** **ALTO** - Integração com sistema de billing
- **Justificativa:** Requisito de negócio para diferenciação de planos

### Decisão 7: Migração Automática ao Inativar Tipo

- **Descrição:** Trigger/job em massa migra consumidores para tipo padrão ao inativar
- **Motivo:** Evitar consumidores órfãos (RN-RF047-007)
- **Impacto:** **ALTO** - Operação em massa pode ser demorada
- **Justificativa:** Integridade de dados obrigatória

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Dados existentes com tipo inválido** | ALTO | Script de validação pré-migração identifica usuários com TipoUsuario fora do enum (1, 2, 3) |
| **Perda de histórico de mudanças** | MÉDIO | Aceitável - legado não tem histórico, modernização cria a partir da migração |
| **Performance em migração em massa** | ALTO | Job Hangfire com batching (1000 registros/lote) e retry automático |
| **Usuários sem tipo padrão** | CRÍTICO | Script de seed cria tipos padrão obrigatórios para todos os fornecedores |
| **Quebra de integrações externas** | MÉDIO | API mantém compatibilidade com INT (1, 2, 3) via mapeamento TipoLegadoId |
| **Alterações simultâneas durante migração** | MÉDIO | Lock de tabela Usuario durante migração + janela de manutenção agendada |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Destino |
|----------------|---------------|---------|
| Enum TipoUsuario.vb (Gerente = 1) | RN-RF047-001 | **SUBSTITUÍDO** → TipoConsumidor (código: GERENTE) |
| Enum TipoUsuario.vb (Funcionario = 2) | RN-RF047-001 | **SUBSTITUÍDO** → TipoConsumidor (código: FUNCIONARIO) |
| Enum TipoUsuario.vb (Externo = 3) | RN-RF047-001 | **SUBSTITUÍDO** → TipoConsumidor (código: EXTERNO) |
| TiposUsuario.aspx (dropdown fixo) | FUNC-004 | **SUBSTITUÍDO** → API GET /tipos-consumidores (filtros dinâmicos) |
| Usuario.TipoUsuario (INT) | MD-RF047 | **SUBSTITUÍDO** → Consumidor.TipoConsumidorId (Guid FK) |
| Sem hierarquia | RN-RF047-003 | **NOVO** → TipoConsumidor.TipoPaiId + validação DAG |
| Sem quotas por tipo | RN-RF047-004 | **NOVO** → TipoConsumidor.QuotaDados/QuotaVoz/QuotaSms |
| Sem auto-classificação | RN-RF047-005 | **NOVO** → RegraAutoClassificacao (regex, prioridade) |
| Sem workflow aprovação | RN-RF047-006 | **NOVO** → SolicitacaoMudancaTipo (pendente/aprovado/rejeitado) |
| Sem custo fixo | RN-RF047-008 | **NOVO** → TipoConsumidor.CustoFixoMensal |
| Sem permissões default | RN-RF047-012 | **NOVO** → TipoConsumidorPermissao (junction table) |
| Sem histórico | RN-RF047-015 | **NOVO** → TipoConsumidorHistorico (7 anos retenção) |
| Sem tipo padrão configurável | RN-RF047-002 | **NOVO** → TipoConsumidor.EhPadrao (flag booleana) |
| Sem limite de tipos | RN-RF047-009 | **NOVO** → Validação 50 tipos/fornecedor |
| Sem cores/ícones | RN-RF047-014 | **NOVO** → TipoConsumidor.Cor/Icone |
| Sem multi-tenancy | RN-RF047-002 | **NOVO** → TipoConsumidor.TenantId (isolamento) |

---

## 10. COMPATIBILIDADE E COEXISTÊNCIA

### Migração Estratégica

1. **Fase 1 - Seed Tipos Padrão:**
   - Criar 3 tipos padrão (GERENTE, FUNCIONARIO, EXTERNO) para todos os fornecedores
   - Mapear TipoLegadoId (1, 2, 3) para compatibilidade

2. **Fase 2 - Migração de Dados:**
   - Criar coluna `TipoConsumidorId` em Usuario
   - Migrar dados: `TipoUsuario = 1 → TipoConsumidor(codigo=GERENTE)`
   - Validar 100% de usuários migrados

3. **Fase 3 - Depreciar Legado:**
   - Marcar coluna `TipoUsuario` como deprecated
   - Criar view compatível para integrações antigas
   - Planejar remoção física após 6 meses

4. **Fase 4 - Expansão:**
   - Habilitar CRUD de tipos customizados
   - Permitir criação de novos tipos além dos 3 padrão

### Período de Coexistência

- **Duração:** 6 meses (2025-12-30 a 2026-06-30)
- **Comportamento:** Ambos os sistemas ativos, com sincronização bidirecional
- **Desativação final:** 2026-07-01 (remoção de TipoUsuario INT)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado RF-047 | Agência ALC - alc.dev.br |

---

**FIM DO DOCUMENTO - RL-RF047 v1.0**

# RL-RF050 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-050 - Gestão de Linhas Móveis e Chips SIM
**Sistema Legado:** IControlIT v1 (ASP.NET Web Forms + VB.NET + SQL Server)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Stack Tecnológica

- **Arquitetura:** Monolítica ASP.NET Web Forms 4.x
- **Linguagem:** VB.NET (Visual Basic .NET)
- **Frontend:** ASPX com ViewState, PostBack, UpdatePanels
- **Backend:** Code-behind VB.NET com lógica mista (UI + Business + Data)
- **Banco de Dados:** SQL Server 2008-2016 (multi-database por cliente)
- **Autenticação:** Forms Authentication com Session State em banco
- **Integração:** WebServices ASMX (SOAP) para integrações internas

### 1.2 Problemas Arquiteturais Identificados

1. **Acoplamento Alto:** Lógica de negócio misturada com código de UI no code-behind
2. **Multi-Database:** Cada cliente tinha banco separado, dificultando manutenção e consultas agregadas
3. **Falta de Auditoria:** Auditoria parcial ou inexistente em operações de linhas
4. **Sem Multi-tenancy:** Isolamento por banco de dados físico ao invés de lógico
5. **Validações Fragmentadas:** Validações duplicadas em frontend (JavaScript), code-behind (VB.NET) e stored procedures
6. **Sem Controle de Versão de Dados:** Histórico de trocas de chip não era rastreado adequadamente
7. **Performance:** Consultas sem índices adequados, N+1 queries em listagens
8. **Sem Workflow de Aprovação:** Operações críticas executadas sem aprovação formal

### 1.3 Configurações Legadas

- **Web.config:** ConnectionStrings por cliente, AppSettings para URLs de WebServices
- **Session State:** Armazenado em SQL Server (performance ruim)
- **ViewState:** Habilitado globalmente (aumentava tamanho do HTML)

---

## 2. TELAS DO LEGADO

### 2.1 Tela: Listagem de Linhas Móveis

**Caminho:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Default.aspx`

**Responsabilidade:** Listar todas as linhas móveis do cliente com filtros básicos (operadora, status, consumidor).

**Campos Principais:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Número | TextBox | Sim | Formato livre, sem validação de DDI/DDD |
| Operadora | DropDownList | Sim | FK para tabela de operadoras |
| Status | DropDownList | Sim | Ativo, Suspenso, Cancelado |
| Consumidor | DropDownList | Não | FK para tabela de usuários |
| ICCID | TextBox | Não | Exibido apenas, não editável |

**Comportamentos Implícitos:**
- Filtro de operadora carregava apenas operadoras com linhas ativas (bug: operadoras sem linhas não apareciam)
- Paginação hard-coded em 50 linhas por página (não configurável)
- Ordenação sempre por data de ativação DESC (não permitia mudar critério)
- Soft delete não existia: ao excluir linha, registro era deletado fisicamente do banco
- Sem controle de permissões: qualquer usuário logado podia ver todas as linhas do cliente

**Destino:** **SUBSTITUÍDO** - Tela moderna em Angular 19 com filtros dinâmicos, paginação configurável e soft delete.

**Rastreabilidade:** RF050 - Seção 4 (Funcionalidades Cobertas) - Funcionalidade 1 "Gestão de Linhas Móveis"

**Migração Moderna:**
- Componente Angular: `linhas-moveis-list.component.ts`
- Rota: `/gestao/linhas-moveis`

---

### 2.2 Tela: Cadastro/Edição de Linha

**Caminho:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Editar.aspx`

**Responsabilidade:** Criar ou editar uma linha móvel com validações básicas.

**Campos Principais:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Número | TextBox | Sim | Validação regex apenas em JavaScript (podia bypassar) |
| ICCID | TextBox | Sim | Validação manual de 19-20 dígitos |
| IMSI | TextBox | Não | Sem validação de formato |
| IMEI | TextBox | Não | Sem validação de formato |
| Operadora | DropDownList | Sim | FK validada apenas no banco (FK constraint) |
| Plano | DropDownList | Sim | FK validada apenas no banco |
| Consumidor | DropDownList | Não | Associação opcional |
| Data Ativação | Calendar | Sim | Data manual (não calculada automaticamente) |
| Valor Mensal | TextBox | Sim | Decimal sem formatação de moeda |

**Comportamentos Implícitos:**
- Unicidade de Número e ICCID não era validada no code-behind (apenas constraint no banco geravam erro genérico)
- Histórico de trocas de chip não era registrado (apenas sobrescrevia ICCID)
- Sem workflow de aprovação para planos caros (ativação imediata)
- Sem integração com operadora (dados 100% manuais)
- Campos de auditoria (Created, CreatedBy) não existiam

**Destino:** **SUBSTITUÍDO** - Formulário moderno com validações FluentValidation no backend e validações reativas no Angular.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-001, RN-050-002

**Migração Moderna:**
- Componente Angular: `linhas-moveis-form.component.ts`
- Command CQRS: `CreateLinhaMovelCommand`, `UpdateLinhaMovelCommand`
- Validator: `CreateLinhaMovelCommandValidator`

---

### 2.3 Tela: Operações sobre Linha (Portabilidade, Troca de Chip, Suspensão, Cancelamento)

**Caminho:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Operacoes.aspx`

**Responsabilidade:** Executar operações críticas sobre linhas (portabilidade, troca de chip, suspensão, cancelamento).

**Campos Principais:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Tipo Operação | RadioButtonList | Sim | Portabilidade, Troca Chip, Suspensão, Cancelamento |
| Protocolo ANATEL | TextBox | Condicional | Obrigatório apenas para portabilidade |
| Motivo Troca | DropDownList | Condicional | Defeituoso, Perdido, Roubado, Upgrade |
| Novo ICCID | TextBox | Condicional | Obrigatório para troca de chip |
| Data Agendamento | Calendar | Condicional | Para portabilidade (mínimo D+7) |
| Justificativa | TextArea | Não | Campo livre, não validado |

**Comportamentos Implícitos:**
- Portabilidade sem validação de protocolo ANATEL (aceitava qualquer texto)
- Prazo mínimo de 7 dias não era validado (erro manual comum)
- Troca de chip não registrava histórico (ICCID antigo era sobrescrito)
- Suspensão temporária não tinha prazo máximo (linhas ficavam suspensas indefinidamente)
- Cancelamento não calculava multa (cálculo feito manualmente no financeiro)
- Sem workflow de aprovação (execução imediata por qualquer usuário)
- Sem notificação ao consumidor sobre operações realizadas

**Destino:** **SUBSTITUÍDO** - Wizard moderno com validações rigorosas, workflow de aprovação multi-nível e notificações automáticas.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-003, RN-050-004, RN-050-007, RN-050-011, RN-050-012

**Migração Moderna:**
- Componente Angular: `operacoes-linha-wizard.component.ts`
- Commands CQRS: `PortabilidadeLinhaCommand`, `TrocaChipCommand`, `SuspendLinhaMovelCommand`, `CancelLinhaMovelCommand`
- Workflow: Aprovação via RF066/RF067

---

### 2.4 Tela: Estoque de Chips

**Caminho:** `ic1_legado/IControlIT/Telecom/Chips/Estoque.aspx`

**Responsabilidade:** Controlar entrada e saída de chips SIM no estoque.

**Campos Principais:**
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| ICCID | TextBox | Sim | Único por chip |
| IMSI | TextBox | Não | Opcional |
| Operadora | DropDownList | Sim | FK validada |
| Status | DropDownList | Sim | Novo, Ativo, Defeituoso (sem "Inativo") |
| Data Entrada | Calendar | Sim | Data manual |
| Quantidade | TextBox | Sim | Entrada em lote (múltiplos ICCIDs) |

**Comportamentos Implícitos:**
- Entrada de chips era manual (um por um ou lote com geração sequencial de ICCID)
- Sem controle de lote/fornecedor (não rastreava origem dos chips)
- Sem alertas de estoque baixo (verificação manual)
- Chips defeituosos não eram separados (ficavam misturados com estoque normal)
- Chips parados >6 meses não eram identificados (risco de expiração)
- Inventário físico vs sistema não era conciliado automaticamente

**Destino:** **ASSUMIDO COM MELHORIAS** - Funcionalidade mantida, mas com melhorias (alertas automáticos, rastreamento de lote, conciliação de inventário).

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-005

**Migração Moderna:**
- Componente Angular: `chips-estoque.component.ts`
- Dashboard: `estoque-chips-dashboard.component.ts`
- Service: `EstoqueChipsService`

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: LinhasMovelsService.asmx

**Caminho:** `ic1_legado/IControlIT/Telecom/WebService/LinhasMovelsService.asmx`

**Responsabilidade:** CRUD básico de linhas móveis exposto via SOAP para integrações internas.

**Métodos Públicos:**

| Método | Parâmetros | Retorno | Observações |
|--------|------------|---------|-------------|
| `GetLinhasByOperadora(operadoraId)` | `int operadoraId` | `List<LinhaMovel>` | Sem paginação (retorna todas as linhas) |
| `CreateLinha(numero, iccid, operadoraId, planoId)` | `string numero, string iccid, int operadoraId, int planoId` | `int linhaId` | Validações mínimas |
| `UpdateLinha(linhaId, numero, iccid)` | `int linhaId, string numero, string iccid` | `bool success` | Sem auditoria de mudanças |
| `DeleteLinha(linhaId)` | `int linhaId` | `bool success` | Delete físico (irreversível) |
| `ActivateLinha(linhaId, chipIccid)` | `int linhaId, string chipIccid` | `bool success` | Sem workflow de aprovação |
| `CancelLinha(linhaId, motivo)` | `int linhaId, string motivo` | `bool success` | Sem cálculo de multa |

**Comportamentos Implícitos:**
- Autenticação básica (usuário/senha em cada request - inseguro)
- Sem rate limiting (vulnerável a DoS)
- Sem versionamento (mudanças quebravam integrações)
- Erros genéricos (não estruturados)
- Sem logging de requests/responses

**Destino:** **SUBSTITUÍDO** - REST API moderna com autenticação JWT, rate limiting, versionamento e erros estruturados.

**Rastreabilidade:** RF050 - Seção 8 (API Endpoints)

**Migração Moderna:**
- REST API: `/api/gestao/linhas-moveis` (17 endpoints RESTful)
- Autenticação: JWT Bearer Token
- Rate Limiting: 100 requests/minuto
- Versionamento: via header `api-version`

---

## 4. STORED PROCEDURES

### 4.1 SP: usp_LinhaMovel_Insert

**Caminho:** `ic1_legado/Database/Procedures/usp_LinhaMovel_Insert.sql`

**Parâmetros de Entrada:**
```sql
@Numero VARCHAR(20),
@ICCID VARCHAR(20),
@IMSI VARCHAR(15),
@IMEI VARCHAR(15),
@OperadoraId INT,
@PlanoId INT,
@ConsumidorId INT = NULL,
@DataAtivacao DATETIME,
@ValorMensal DECIMAL(10,2)
```

**Parâmetros de Saída:**
```sql
@LinhaId INT OUTPUT
```

**Lógica Principal:**
- Valida unicidade de Número e ICCID (retorna erro se duplicado)
- Insere na tabela `LinhasMoveis`
- Atualiza status do chip para "Ativo" na tabela `Chips`
- NÃO registra auditoria de criação
- NÃO notifica consumidor

**Destino:** **SUBSTITUÍDO** - Lógica movida para `CreateLinhaMovelCommandHandler` com validações FluentValidation e auditoria automática.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-001, RN-050-002

**Migração Moderna:**
- Handler: `CreateLinhaMovelCommandHandler`
- Validator: `CreateLinhaMovelCommandValidator`
- Auditoria: `AuditInterceptor` (automático)

---

### 4.2 SP: usp_LinhaMovel_Portabilidade

**Caminho:** `ic1_legado/Database/Procedures/usp_LinhaMovel_Portabilidade.sql`

**Parâmetros de Entrada:**
```sql
@LinhaId INT,
@NovaOperadoraId INT,
@NovoChipIccid VARCHAR(20),
@ProtocoloANATEL VARCHAR(12),
@DataAgendamento DATETIME
```

**Lógica Principal:**
- Valida que linha está ativa
- Atualiza operadora e ICCID da linha
- Desativa chip antigo (status "Inativo")
- Ativa novo chip (status "Ativo")
- Registra data de portabilidade
- NÃO valida formato de protocolo ANATEL
- NÃO valida prazo mínimo de 7 dias
- NÃO cria histórico de trocas de operadora
- NÃO notifica consumidor

**Destino:** **SUBSTITUÍDO** - Lógica movida para `PortabilidadeLinhaCommandHandler` com validações rigorosas e workflow de aprovação.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-003, RN-050-007

**Migração Moderna:**
- Handler: `PortabilidadeLinhaCommandHandler`
- Validator: `PortabilidadeLinhaCommandValidator` (valida protocolo e prazo)
- Workflow: Aprovação Gestor + Financeiro via `ApprovalWorkflowService`

---

### 4.3 SP: usp_Chip_EstoqueReport

**Caminho:** `ic1_legado/Database/Procedures/usp_Chip_EstoqueReport.sql`

**Parâmetros de Entrada:**
```sql
@OperadoraId INT = NULL
```

**Parâmetros de Saída:**
```sql
Tabela com colunas: Operadora, TotalNovo, TotalAtivo, TotalDefeituoso
```

**Lógica Principal:**
- Agrupa chips por operadora e status
- Calcula totais
- NÃO identifica chips parados >6 meses
- NÃO gera alertas de estoque baixo

**Destino:** **ASSUMIDO COM MELHORIAS** - Query mantida, mas com detecção de chips parados e alertas automáticos.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-005

**Migração Moderna:**
- Query: `GetEstoqueChipsQuery`
- Job: `EstoqueBaixoAlertJob` (Hangfire - diário)

---

## 5. TABELAS LEGADAS

### 5.1 Tabela: LinhasMoveis

**Schema:** `[dbo].[LinhasMoveis]`

**Problemas Identificados:**
1. Sem FK para ChipId (relacionamento apenas por ICCID string - ineficiente)
2. Sem campos de auditoria (Created, CreatedBy, LastModified, LastModifiedBy)
3. Sem soft delete (IsDeleted) - delete físico irreversível
4. Sem multi-tenancy (ClienteId) - tabela por banco físico
5. Campos IMSI e IMEI na mesma tabela (deveriam estar em histórico separado)
6. Sem índice em Número (consultas lentas)
7. Sem índice composto (Operadora + Status)

**Destino:** **SUBSTITUÍDO** - Tabela redesenhada com FKs, auditoria, soft delete, multi-tenancy e índices otimizados.

**Rastreabilidade:** RF050 - Seção 12 (Artefatos Derivados) - MD-RF050.md

**Migração Moderna:**
- Tabela: `LinhaMovel` (Entity Framework)
- Migration: `20251230_CreateLinhaMovelTable.cs`
- Índices: `IX_LinhaMovel_Numero`, `IX_LinhaMovel_Operadora_Status`, `IX_LinhaMovel_ClienteId`

---

### 5.2 Tabela: Chips

**Schema:** `[dbo].[Chips]`

**Problemas Identificados:**
1. Sem FK para OperadoraId (relacionamento apenas por nome string)
2. Sem rastreamento de lote/fornecedor
3. Sem data de entrada/saída (apenas status atual)
4. Sem auditoria de movimentações
5. Sem separação de chips de teste/homologação
6. Sem alerta automático de estoque baixo

**Destino:** **SUBSTITUÍDO** - Tabela redesenhada com FKs, rastreamento de lote, movimentações auditadas e alertas.

**Rastreabilidade:** RF050 - Seção 12 (Artefatos Derivados) - MD-RF050.md

**Migração Moderna:**
- Tabela: `ChipSIM`
- Tabela relacionada: `EstoqueChip` (movimentações)
- Tabela relacionada: `HistoricoLinhaChip` (trocas)

---

### 5.3 Tabela: OperacoesLinhas

**Schema:** Tabela NÃO EXISTIA no legado

**Problemas Identificados:**
- Operações (portabilidade, troca de chip, suspensão, cancelamento) não eram registradas em tabela dedicada
- Histórico era inferido por datas de atualização na tabela LinhasMoveis (impreciso)
- Sem rastreamento de aprovadores
- Sem rastreamento de justificativas

**Destino:** **CRIADO NO MODERNO** - Nova tabela para rastrear todas as operações com workflow de aprovação.

**Rastreabilidade:** RF050 - Seção 6 (Estados da Entidade) - Seção 6.3 (Estados de Operação de Linha)

**Migração Moderna:**
- Tabela: `OperacaoLinha`
- Estados: Pendente, Aprovada, Executada, Rejeitada, Cancelada

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Validação de Número de Telefone

**Descrição:** Número de telefone móvel deve seguir formato brasileiro +55 (DDD) 9XXXX-XXXX.

**Localização:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Editar.aspx` - JavaScript validation

**Código VB.NET (Code-Behind):**
```vb
' EXTRAÍDO DO LEGADO - Regra em LINGUAGEM NATURAL
' Validação: Número deve ter 11 dígitos (DDD + 9 + 8 dígitos)
' Regex: ^\d{2}9\d{8}$
' Exemplo válido: 11987654321
' Exemplo inválido: 1112345678 (falta o 9)
```

**Regra Extraída em Linguagem Natural:**
Número de telefone móvel brasileiro deve ter 11 dígitos numéricos, sendo:
- 2 primeiros dígitos: DDD (código de área)
- 3º dígito: obrigatoriamente 9 (identificador de celular)
- 8 dígitos restantes: número único

**Destino:** **ASSUMIDO** - Regra documentada e mantida no sistema moderno com validação FluentValidation.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-001

**Migração Moderna:**
- Validator: `CreateLinhaMovelCommandValidator.cs`
- Validação regex: `^[0-9]{2}9[0-9]{8}$`

---

### RL-RN-002: ICCID Deve Ser Único Globalmente

**Descrição:** ICCID de chip SIM deve ser único em todo o sistema (não apenas por cliente).

**Localização:** `ic1_legado/Database/Constraints/UK_Chips_ICCID.sql`

**Código SQL (Constraint):**
```sql
-- EXTRAÍDO DO LEGADO - Regra em LINGUAGEM NATURAL
-- Constraint UNIQUE em coluna ICCID
-- Garante que nenhum chip pode ter ICCID duplicado
ALTER TABLE Chips ADD CONSTRAINT UK_Chips_ICCID UNIQUE (ICCID)
```

**Regra Extraída em Linguagem Natural:**
ICCID é identificador único mundial de chip SIM. Sistema deve rejeitar qualquer tentativa de cadastrar chip com ICCID já existente, retornando erro HTTP 400 com mensagem "ICCID já cadastrado no sistema".

**Destino:** **ASSUMIDO** - Constraint mantida no banco de dados moderno + validação adicional em FluentValidation.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-006

**Migração Moderna:**
- Constraint: `UNIQUE INDEX IX_ChipSIM_ICCID ON ChipSIM (ICCID)`
- Validator: `CreateChipSIMCommandValidator` (valida unicidade antes de tentar insert)

---

### RL-RN-003: Troca de Chip Por Perda Gera Cobrança ao Consumidor

**Descrição:** Quando motivo da troca de chip é "Perdido" ou "Roubado", sistema deve gerar cobrança de R$20,00 ao consumidor.

**Localização:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Operacoes.aspx.vb` - Code-behind (linha ~350)

**Código VB.NET:**
```vb
' EXTRAÍDO DO LEGADO - Regra em LINGUAGEM NATURAL
' If MotivoTroca = "Perdido" Or MotivoTroca = "Roubado" Then
'     GerarCobranca(ConsumidorId, 20.00, "Troca de chip por perda/roubo")
' End If
```

**Regra Extraída em Linguagem Natural:**
Troca de chip por perda ou roubo gera cobrança automática de R$20,00 ao consumidor associado à linha. Valor é inserido na tabela de cobranças avulsas e aparece na próxima fatura. Se linha não tem consumidor associado, cobrança não é gerada (registra apenas aviso no log).

**Destino:** **ASSUMIDO COM CONFIGURAÇÃO** - Regra mantida, mas valor de cobrança torna-se configurável por cliente (não hard-coded em R$20,00).

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-004

**Migração Moderna:**
- Handler: `TrocaChipCommandHandler`
- Configuração: `AppSettings:TrocaChipPerdaCusto` (configurável por cliente)
- Integração: RF026 (Gestão de Faturas) para gerar cobrança

---

### RL-RN-004: Portabilidade Requer Prazo Mínimo de 7 Dias Úteis

**Descrição:** Solicitação de portabilidade deve ser agendada para no mínimo 7 dias úteis após a solicitação (regulamentação ANATEL).

**Localização:** `ic1_legado/IControlIT/Telecom/LinhasMoveis/Operacoes.aspx.vb` - Code-behind (NÃO IMPLEMENTADO - bug do legado)

**Código VB.NET:**
```vb
' EXTRAÍDO DO LEGADO - Regra em LINGUAGEM NATURAL
' BUG: Prazo mínimo NÃO era validado no código legado
' Usuário podia agendar portabilidade para qualquer data (inclusive passado)
' Validação era feita manualmente pelo operador telecom
```

**Regra Extraída em Linguagem Natural:**
Portabilidade telefônica no Brasil deve respeitar prazo mínimo de 7 dias úteis conforme regulamentação ANATEL. Sistema deve calcular data mínima de agendamento considerando apenas dias úteis (segunda a sexta, excluindo feriados nacionais). Se usuário tentar agendar para data anterior ao prazo, sistema rejeita com HTTP 400 e mensagem "Prazo mínimo para portabilidade é de 7 dias úteis (data mínima: DD/MM/AAAA)".

**Destino:** **ASSUMIDO COM CORREÇÃO** - Regra que estava faltando no legado foi implementada no sistema moderno.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-003

**Migração Moderna:**
- Validator: `PortabilidadeLinhaCommandValidator`
- Validação: `DataAgendamento >= DateTime.Now.AddBusinessDays(7)`
- Helper: `BusinessDaysHelper` (calcula dias úteis excluindo feriados)

---

### RL-RN-005: Linha Suspensa Tem Cobrança Reduzida em 50%

**Descrição:** Linha suspensa temporariamente mantém cobrança mensal, mas com desconto de 50% do valor do plano.

**Localização:** `ic1_legado/Database/Procedures/usp_Fatura_Calcular.sql` (lógica no financeiro)

**Código SQL:**
```sql
-- EXTRAÍDO DO LEGADO - Regra em LINGUAGEM NATURAL
-- IF Status = 'Suspenso' THEN ValorCobranca = ValorMensal * 0.5
```

**Regra Extraída em Linguagem Natural:**
Linha suspensa temporariamente não pode fazer ou receber chamadas, mas número é mantido. Operadora cobra 50% do valor do plano mensal durante o período de suspensão. Ao reativar linha, cobrança volta ao valor integral. Desconto de 50% pode variar conforme contrato com operadora (configurável por cliente).

**Destino:** **ASSUMIDO COM CONFIGURAÇÃO** - Regra mantida, mas percentual de desconto torna-se configurável.

**Rastreabilidade:** RF050 - Seção 5 (Regras de Negócio) - RN-050-011

**Migração Moderna:**
- Handler: `SuspendLinhaMovelCommandHandler`
- Configuração: `AppSettings:SuspensaoDescontoPercentual` (padrão: 50%)
- Integração: RF026 (Gestão de Faturas) para calcular cobrança reduzida

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Legado | RF Moderno | Impacto |
|----------------|--------|------------|---------|
| **Soft Delete** | Delete físico | Soft delete (IsDeleted=true) | Alto - Preserva auditoria |
| **Multi-tenancy** | Banco por cliente | ClienteId em todas as tabelas | Alto - Simplifica infraestrutura |
| **Workflow de Aprovação** | Inexistente | Aprovação multi-nível para operações críticas | Alto - Melhora governança |
| **Auditoria** | Parcial | Completa (Created, CreatedBy, LastModified, LastModifiedBy) | Alto - Compliance LGPD |
| **Integração com Operadoras** | Manual | Sincronização automática via API/webhook | Médio - Reduz erros manuais |
| **Alertas de Vencimento** | Manual | Automático (30/60/90 dias) | Médio - Melhora gestão de contratos |
| **Identificação de Subutilização** | Inexistente | Análise automática mensal | Médio - Otimiza custos |
| **Histórico de Trocas de Chip** | Inexistente | Tabela HistoricoLinhaChip completa | Médio - Rastreabilidade |
| **Dashboard de Estoque** | Relatório estático | Dashboard em tempo real com SignalR | Baixo - Melhora UX |
| **Importação em Lote** | CSV limitado a 100 linhas | CSV/Excel até 1.000 linhas síncrono, >1.000 job background | Baixo - Agiliza migração |
| **Validações** | Fragmentadas (JS + VB + SP) | Centralizadas em FluentValidation | Alto - Consistência |
| **Autenticação API** | Basic Auth (usuário/senha) | JWT Bearer Token | Alto - Segurança |
| **Rate Limiting** | Inexistente | 100 requests/minuto | Médio - Proteção DoS |
| **Versionamento de API** | Inexistente | Versionamento via header | Baixo - Manutenibilidade |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Multi-Database por Multi-Tenancy com ClienteId

**Motivo:** No legado, cada cliente tinha banco SQL Server separado, dificultando consultas agregadas, backup e manutenção. Sistema moderno usa banco único SQLite (dev) / SQL Server (prod) com isolamento lógico via ClienteId (Row-Level Security).

**Impacto:** Alto - Reduz custo de infraestrutura, simplifica backup e facilita consultas cross-cliente para administradores.

**Riscos:** Risco de vazamento de dados entre clientes se filtro de ClienteId falhar (mitigado com testes automatizados de isolamento).

---

### Decisão 2: Implementar Workflow de Aprovação para Operações Críticas

**Motivo:** No legado, operações como portabilidade, ativação de planos caros e cancelamentos eram executadas imediatamente sem aprovação formal, gerando risco financeiro e falta de governança.

**Impacto:** Alto - Melhora controle financeiro, reduz erros operacionais e facilita auditoria.

**Riscos:** Aumento do tempo de execução de operações (mitigado com SLA de aprovação em 24 horas e notificações automáticas).

---

### Decisão 3: Mover Validações para Backend com FluentValidation

**Motivo:** No legado, validações estavam fragmentadas em JavaScript (frontend), VB.NET (code-behind) e SQL (stored procedures), gerando inconsistências e bugs. Sistema moderno centraliza validações no backend com FluentValidation.

**Impacto:** Alto - Garante consistência, facilita manutenção e melhora segurança (validações não podem ser bypassadas no frontend).

**Riscos:** Baixo - Requer sincronização entre validações backend e mensagens de erro no frontend Angular.

---

### Decisão 4: Criar Histórico de Trocas de Chip em Tabela Separada

**Motivo:** No legado, histórico de trocas de chip não era registrado (ICCID era sobrescrito na mesma tabela). Sistema moderno cria tabela `HistoricoLinhaChip` para rastrear todas as trocas.

**Impacto:** Médio - Melhora rastreabilidade, detecta anomalias (múltiplas trocas suspeitas) e auxilia suporte técnico.

**Riscos:** Baixo - Aumenta volume de dados, mas com retenção de 7 anos conforme LGPD.

---

### Decisão 5: Substituir WebServices ASMX por REST API com JWT

**Motivo:** No legado, integrações usavam WebServices ASMX (SOAP) com autenticação Basic Auth (inseguro). Sistema moderno usa REST API com autenticação JWT Bearer Token e rate limiting.

**Impacto:** Alto - Melhora segurança, facilita integrações externas e adota padrão moderno de mercado.

**Riscos:** Baixo - Requer ajuste de integrações existentes (se houver sistemas externos consumindo ASMX).

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de Histórico de Linhas** | Alto | Baixa | Script de migração com validação cruzada (comparar totais legado vs moderno) |
| **ICCID Duplicados Entre Clientes** | Alto | Média | Validação pré-migração para detectar duplicatas e criar plano de consolidação |
| **Falha na Sincronização com Operadoras** | Médio | Média | Manter sincronização manual via importação CSV como fallback |
| **Resistência ao Workflow de Aprovação** | Médio | Alta | Treinamento de usuários e período de transição com aprovação automática configurável |
| **Performance de Consultas Multi-Tenant** | Médio | Média | Índices otimizados em ClienteId e testes de carga pré-produção |
| **Incompatibilidade de Dados Legados** | Alto | Baixa | Script de sanitização de dados antes da migração (corrigir formatos inválidos) |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF |
|-----------------|---------------|
| Tela `Default.aspx` (Listagem) | RF050 - Seção 4 - Funcionalidade 1 "Gestão de Linhas Móveis" |
| Tela `Editar.aspx` (Cadastro) | RF050 - Seção 5 - RN-050-001, RN-050-002 |
| Tela `Operacoes.aspx` (Operações) | RF050 - Seção 5 - RN-050-003, RN-050-004, RN-050-011, RN-050-012 |
| Tela `Estoque.aspx` (Estoque de Chips) | RF050 - Seção 5 - RN-050-005 |
| WebService `LinhasMovelsService.asmx` | RF050 - Seção 8 (API Endpoints) |
| SP `usp_LinhaMovel_Insert` | RF050 - Seção 5 - RN-050-001, RN-050-002 |
| SP `usp_LinhaMovel_Portabilidade` | RF050 - Seção 5 - RN-050-003, RN-050-007 |
| SP `usp_Chip_EstoqueReport` | RF050 - Seção 5 - RN-050-005 |
| Tabela `LinhasMoveis` | RF050 - Seção 12 - MD-RF050.md |
| Tabela `Chips` | RF050 - Seção 12 - MD-RF050.md |
| Regra implícita: Validação de Número | RF050 - Seção 5 - RN-050-001 |
| Regra implícita: ICCID Único | RF050 - Seção 5 - RN-050-006 |
| Regra implícita: Cobrança por Perda de Chip | RF050 - Seção 5 - RN-050-004 |
| Regra implícita: Prazo Portabilidade 7 Dias | RF050 - Seção 5 - RN-050-003 |
| Regra implícita: Desconto 50% Suspensão | RF050 - Seção 5 - RN-050-011 |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação inicial de referência ao legado do RF050 com mapeamento completo | Agência ALC - alc.dev.br |

# RL-RF069 — Referência ao Legado: Configuração de SLA para Chamados

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-069
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Visão Geral do Sistema Legado

O módulo de SLA no sistema legado foi desenvolvido em **ASP.NET Web Forms (VB.NET)** com lógica de negócio distribuída entre:
- **Code-behind ASPX**: Validações client-side e server-side misturadas
- **Stored Procedures SQL Server**: Cálculos complexos de prazo (900+ linhas de T-SQL)
- **WebServices ASMX SOAP**: Interfaces para integração com outros módulos
- **Helpers VB.NET**: Classes utilitárias com regras hardcoded

### 1.2 Stack Tecnológica

- **Arquitetura**: Monolítica WebForms
- **Linguagem**: VB.NET (Framework .NET 4.5)
- **Frontend**: ASP.NET Web Forms com ViewState, Postback e GridView
- **Backend**: Code-behind VB.NET + Stored Procedures
- **Banco de Dados**: SQL Server 2012 (múltiplos databases por cliente)
- **Multi-tenant**: Não nativo (banco separado por cliente)
- **Auditoria**: Parcial (apenas log de erros, sem rastreamento de alterações)
- **Configurações**: Web.config + hardcoded no código

### 1.3 Problemas Arquiteturais Identificados

1. **Lógica de Negócio Dispersa**: Regras espalhadas em ASPX, VB.NET, SQL Server
2. **Ausência de Versionamento**: Alterações em SLA sobrescrevem dados sem histórico
3. **Performance Ruim**: Stored procedures lentas (>20 segundos para relatórios)
4. **Escalação Limitada**: Apenas 1 nível de escalação (Email_2_Nivel)
5. **Sem Calendários Customizados**: Horário comercial (seg-sex 8-18h) hardcoded
6. **Feriados Desatualizados**: Tabela estática atualizada manualmente 1x/ano
7. **Multi-Database**: Cada cliente em banco separado, inviabilizando consolidação
8. **Sem Auditoria LGPD**: Não registra who/when/what para alterações de SLA
9. **SOAP Obsoleto**: WebServices ASMX com autenticação fraca (Basic Auth)
10. **Sem Pausas Automáticas**: Pausas de SLA gerenciadas manualmente via SQL UPDATE

---

## 2. BANCO DE DADOS LEGADO

### 2.1 Tabela Principal: Solicitacao_SLA

**Banco**: `IControlIT_Cliente`

```sql
CREATE TABLE [dbo].[Solicitacao_SLA](
    [Id_Solicitacao_SLA] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Solicitacao_SLA] [varchar](50) NOT NULL,
    [Horas] [int] NOT NULL,                         -- ⚠️ Apenas HORAS (não minutos)
    [Email_2_Nivel] [varchar](50) NOT NULL,         -- ⚠️ Apenas 1 e-mail de escalação
    [Fl_Desativado] [int] NOT NULL,                 -- ⚠️ 0=ativo, 1=inativo (invertido)
    CONSTRAINT [PK_Solicitacao_SLA] PRIMARY KEY CLUSTERED ([Id_Solicitacao_SLA] ASC)
) ON [PRIMARY]
```

**Campos Importantes**:

| Campo Legado | Descrição | Problema Identificado | Destino Moderno |
|--------------|-----------|----------------------|------------------|
| `Id_Solicitacao_SLA` | Chave primária | Nenhum | `Id_SLA` (Guid modernizado) |
| `Nm_Solicitacao_SLA` | Nome do SLA (ex: "SLA Crítico 4h") | Sem validação de unicidade | `Nm_SLA` (com constraint unique por tenant/tipo/prioridade) |
| `Horas` | Prazo em HORAS (não minutos) | Granularidade insuficiente (mínimo 1h) | `Tempo_Resolucao_Minutos` (conversão Horas*60) |
| `Email_2_Nivel` | E-mail único para escalação | Apenas 1 nível, sem multi-canal | `Escalacao_SLA` (tabela separada, multi-nível, multi-canal) |
| `Fl_Desativado` | 0=ativo, 1=inativo | Semântica invertida confusa | `Fl_Ativo` (true=ativo, false=inativo) |

**Limitações Críticas**:
- ❌ Sem diferenciação entre tempo de resposta vs tempo de resolução
- ❌ Sem suporte a calendários (horário útil hardcoded)
- ❌ Sem campos de auditoria (Created, CreatedBy, Modified, ModifiedBy)
- ❌ Sem multi-tenancy (Id_Conglomerado)
- ❌ Sem soft delete (Fl_Excluido)

### 2.2 Tabela Secundária: Contrato_SLA_Operacao

```sql
CREATE TABLE [dbo].[Contrato_SLA_Operacao](
    [Id_Contrato_SLA_Operacao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Contrato] [int] NOT NULL,
    [Descricao] [varchar](8000) NOT NULL,
    [Prazo_Dias] [int] NULL,
    [Vr_SLA_Operacao] [numeric](10, 2) NULL,
    [Fl_Desativado] [int] NOT NULL,
    CONSTRAINT [PK_Contrato_SLA_Operacao] PRIMARY KEY CLUSTERED ([Id_Contrato_SLA_Operacao] ASC)
) ON [PRIMARY]
```

**Uso**: SLAs vinculados a contratos de fornecedores (ex: "Troca de equipamento em até 5 dias úteis").

**Destino**: ❌ **DESCARTADO** - Migrado para RF-028 (SLA Operações), não para RF-069 (SLA Chamados). Escopo separado.

---

## 3. STORED PROCEDURES LEGADAS

### 3.1 pa_CalcularSLA

**Caminho**: `IControlIT_Cliente/Database/Procedures/pa_CalcularSLA.sql`

**Responsabilidade**: Calcular se chamado está dentro do prazo de SLA considerando horário comercial (seg-sex 8h-18h).

**Lógica Principal** (em linguagem natural):
1. Recebe `@Id_Chamado` como parâmetro
2. Busca `Id_SLA` associado ao chamado
3. Busca `Horas` (prazo) da tabela `Solicitacao_SLA`
4. Calcula data/hora limite considerando:
   - Horário comercial: seg-sex 8h-18h (hardcoded)
   - Feriados da tabela `Feriados` (apenas nacionais)
   - Fins de semana (sábado/domingo ignorados)
5. Compara data/hora atual com prazo limite
6. Retorna flag: 0=dentro do prazo, 1=violado

**Problemas Identificados**:
- ❌ **900+ linhas de T-SQL** (complexidade extrema, difícil manutenção)
- ❌ **Horário comercial hardcoded** (impossível customizar por cliente)
- ❌ **Sem suporte a pausas de SLA** (contagem nunca para)
- ❌ **Performance ruim** (>2 segundos por execução em chamados antigos)
- ❌ **Sem diferenciação resposta vs resolução** (calcula apenas 1 prazo)

**Destino**: ✅ **SUBSTITUÍDO** → `CalculadoraSLA.cs` (C# CQRS Handler) + Hangfire Background Job (tempo real)

---

### 3.2 pa_ObterSLAPorCliente

**Caminho**: `IControlIT_Cliente/Database/Procedures/pa_ObterSLAPorCliente.sql`

**Responsabilidade**: Retornar SLA aplicável a um cliente/tipo de chamado.

**Lógica Principal**:
1. Recebe `@Id_Cliente`, `@Id_Tipo_Chamado`
2. Busca na tabela `Solicitacao_SLA` filtrado por cliente
3. Se não encontrar, retorna SLA genérico (Id_Cliente NULL)
4. Retorna primeiro resultado (sem regras de prioridade)

**Problemas Identificados**:
- ❌ **Sem suporte a prioridades** (Crítica/Alta/Média/Baixa)
- ❌ **Sem regra de precedência clara** (retorna primeiro aleatório)
- ❌ **Não valida se SLA está ativo** (pode retornar SLA desativado)

**Destino**: ✅ **SUBSTITUÍDO** → Query CQRS `ObterSLAAplicavel` com regras de precedência (específico → genérico → default)

---

### 3.3 pa_RelatorioCompliance

**Caminho**: `IControlIT_Cliente/Database/Procedures/pa_RelatorioCompliance.sql`

**Responsabilidade**: Gerar relatório mensal de compliance SLA.

**Lógica Principal**:
1. Recebe `@Mes`, `@Ano`
2. Conta total de chamados resolvidos no mês
3. Conta chamados resolvidos dentro do prazo (baseado em flag `Fl_SLA_Violado`)
4. Calcula percentual: (Dentro Prazo / Total) * 100
5. Retorna resultado em tabela

**Problemas Identificados**:
- ❌ **Extremamente lento** (>2 minutos para meses com +10k chamados)
- ❌ **Sem cache** (recalcula tudo a cada execução)
- ❌ **Sem drill-down** (resultado agregado, sem detalhes por prioridade/equipe)
- ❌ **Sem exportação** (apenas tabela SQL, sem PDF/Excel)

**Destino**: ✅ **SUBSTITUÍDO** → Dashboard Angular + ApexCharts com SignalR (real-time) + cache Redis (<500ms)

---

## 4. TELAS ASPX LEGADAS

### 4.1 Chamado/ConfigurarSLA.aspx

**Caminho**: `ic1_legado/IControlIT/Chamado/ConfigurarSLA.aspx`

**Responsabilidade**: Cadastro e edição de SLAs.

**Campos**:

| Campo | Tipo | Obrigatório | Validação Legado |
|-------|------|-------------|------------------|
| `txtNomeSLA` | TextBox | Sim | MaxLength=50, RequiredFieldValidator |
| `txtHoras` | TextBox (numérico) | Sim | RangeValidator (1-999), só aceita inteiros |
| `txtEmail2Nivel` | TextBox | Sim | RegularExpressionValidator (e-mail) |
| `chkDesativado` | CheckBox | Não | Nenhuma |

**Comportamentos Implícitos**:
1. **Validação Client-Side Fraca**: JavaScript desabilitável no navegador
2. **Postback Lento**: Cada mudança recarrega página inteira (~3 segundos)
3. **Sem Pré-visualização**: Não mostra impacto da mudança no compliance
4. **Sobrescreve Sem Aviso**: Não alerta se mudança vai afetar chamados ativos
5. **Sem Versionamento**: Alteração sobrescreve valores anteriores sem histórico

**Destino**: ✅ **SUBSTITUÍDO** → `/service-desk/sla/configurar` (Angular SPA com Reactive Forms, validação real-time, simulador integrado)

---

### 4.2 Chamado/RelatorioSLA.aspx

**Caminho**: `ic1_legado/IControlIT/Chamado/RelatorioSLA.aspx`

**Responsabilidade**: Relatório tabular de compliance SLA.

**Campos**:

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `ddlMes` | DropDownList | Mês de referência |
| `ddlAno` | DropDownList | Ano de referência |
| `gvRelatorio` | GridView | Tabela de resultados |
| `btnExportar` | Button | Exportar para Excel (via Response.Write) |

**Comportamentos Implícitos**:
1. **Dados Estáticos**: Resultado não atualiza automaticamente
2. **Sem Drill-Down**: Não permite clicar para ver detalhes
3. **Exportação Rudimentar**: Excel gerado via HTML puro (sem formatação)
4. **Sem Gráficos**: Apenas tabela numérica (difícil visualização de tendências)

**Destino**: ✅ **SUBSTITUÍDO** → `/service-desk/sla/compliance` (Dashboard ApexCharts com gráficos de tendência, drill-down, exportação PDF/Excel profissional)

---

### 4.3 Chamado/EscalacaoSLA.aspx

**Caminho**: `ic1_legado/IControlIT/Chamado/EscalacaoSLA.aspx`

**Responsabilidade**: Configuração manual de e-mails de escalação.

**Campos**:

| Campo | Tipo | Observações |
|-------|------|-------------|
| `txtEmail2Nivel` | TextBox | Único e-mail permitido |
| `chkEnviarAlerta` | CheckBox | Liga/desliga alertas |

**Limitações Críticas**:
- ❌ **Apenas 1 Nível de Escalação**: Impossível configurar supervisor → gerente → diretor
- ❌ **Apenas E-mail**: Sem suporte a SMS, push, webhook
- ❌ **Sem Percentuais Configuráveis**: Alerta fixo em 80% do prazo (hardcoded)
- ❌ **Sem Mensagem Customizável**: Template de e-mail hardcoded no código VB.NET

**Destino**: ✅ **SUBSTITUÍDO** → `/service-desk/sla/escalacoes` (Workflow visual com até 5 níveis, multi-canal, mensagens customizáveis, percentuais configuráveis)

---

## 5. WEBSERVICES LEGADOS (VB.NET)

### 5.1 WSSuporte.asmx

**Arquivo**: `ic1_legado/IControlIT/WebService/WSSuporte.asmx.vb`

#### Método: ObterSLAPorChamado

**Assinatura**: `Public Function ObterSLAPorChamado(idChamado As Integer) As SLADto`

**Responsabilidade**: Retorna SLA aplicável ao chamado.

**Lógica** (em linguagem natural):
1. Busca chamado na tabela `Chamados`
2. Busca Id_Cliente e Id_Tipo_Chamado
3. Chama `pa_ObterSLAPorCliente` (stored procedure)
4. Retorna objeto SLADto com campos: Id, Nome, Horas, Email2Nivel

**Destino**: ✅ **SUBSTITUÍDO** → `GET /api/sla/chamado/{idChamado}` (REST API com autenticação JWT, cache Redis)

---

#### Método: CalcularPrazoSLA

**Assinatura**: `Public Function CalcularPrazoSLA(idSLA As Integer, dataInicio As DateTime) As DateTime`

**Responsabilidade**: Calcula data/hora limite do SLA.

**Lógica**:
1. Busca `Horas` da tabela `Solicitacao_SLA`
2. Chama `pa_CalcularSLA` (stored procedure) com data início
3. Retorna data/hora calculada considerando horário comercial

**Problemas**:
- ❌ **Lento** (>2 segundos via SOAP + SP)
- ❌ **Sem cache** (recalcula sempre)

**Destino**: ✅ **SUBSTITUÍDO** → `POST /api/sla/calcular-prazo` (REST API com lógica C# otimizada, <200ms)

---

#### Método: ValidarViolacaoSLA

**Assinatura**: `Public Function ValidarViolacaoSLA(idChamado As Integer) As Boolean`

**Responsabilidade**: Verifica se chamado violou SLA.

**Lógica**:
1. Busca data/hora de abertura do chamado
2. Busca prazo limite calculado
3. Compara DateTime.Now com prazo limite
4. Retorna True se violado, False se dentro do prazo

**Destino**: ✅ **SUBSTITUÍDO** → `GET /api/sla/chamado/{idChamado}/status` (REST API + Hangfire Background Job verificando continuamente)

---

### 5.2 Limitações Gerais dos WebServices SOAP

- ❌ **Autenticação Fraca**: Basic Auth (usuário/senha em base64, sem criptografia)
- ❌ **Sem Webhooks**: Notificações somente via polling (cliente consulta periodicamente)
- ❌ **Performance Ruim**: Média >2s por request (vs <200ms REST moderno)
- ❌ **Sem Versionamento de API**: Mudança quebra clientes sem aviso
- ❌ **XML Verboso**: Payloads 3-5x maiores que JSON equivalente

**Destino**: ✅ **SUBSTITUÍDO** → REST API completa com OAuth2 + JWT, webhooks para notificações proativas, cache Redis, <200ms response time

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Horário Comercial Hardcoded

**Localizacao Código**: `pa_CalcularSLA.sql - Linhas 45-120`

**Descrição**: Horário útil fixo em seg-sex 8h-18h sem possibilidade de customização por cliente.

**Problema**: Clientes com contrato 24x7 ou horário diferenciado (plantão 7h-19h) não conseguem configurar.

**Destino**: ✅ **ASSUMIDO** → RF-069 implementa calendários customizáveis com horários e dias configuráveis por cliente/contrato.

---

### RL-RN-002: Feriados Apenas Nacionais

**Localizacao Código**: Tabela `Feriados` + `pa_CalcularSLA.sql - Linhas 200-250`

**Descrição**: Sistema considera apenas feriados nacionais. Feriados estaduais, municipais e corporativos são ignorados.

**Problema**: Empresas em SP (Aniversário da Cidade 25/jan) ou com ponte facultativa perdem compliance injustamente.

**Destino**: ✅ **ASSUMIDO** → RF-069 suporta feriados Nacional/Estadual/Municipal/Corporativo com importação automática via BrasilAPI.

---

### RL-RN-003: Escalação Fixa em 80% do Prazo

**Localizacao Código**: `WSSuporte.asmx.vb - Função EnviarAlertaSLA() - Linha 450`

**Descrição**: E-mail de alerta disparado automaticamente quando chamado atinge 80% do prazo. Percentual hardcoded, não configurável.

**Problema**: Alguns SLAs críticos precisam alerta mais cedo (ex: 50%), outros menos urgentes podem alertar em 90%.

**Destino**: ✅ **SUBSTITUÍDO** → RF-069 permite até 5 níveis de escalação com percentuais configuráveis (50%, 75%, 90%, 100%).

---

### RL-RN-004: Pausa de SLA Apenas Manual

**Localizacao Código**: Não havia lógica automática. Analistas executavam SQL UPDATE manualmente: `UPDATE Chamados SET Dt_Pausa_SLA = GETDATE() WHERE Id_Chamado = X`

**Descrição**: Quando chamado dependia de cliente (aguardando resposta), analista precisava pausar SLA manualmente via SQL.

**Problema**: Dependia de disciplina do analista (frequentemente esquecido), causava violações injustas.

**Destino**: ✅ **ASSUMIDO** → RF-069 pausa SLA automaticamente quando chamado entra em status configurado como "Pausa SLA" (ex: "Aguardando Cliente").

---

### RL-RN-005: Sem Diferenciação Resposta vs Resolução

**Localizacao Código**: Tabela `Solicitacao_SLA` - Campo `Horas` (único prazo)

**Descrição**: Sistema legado tinha apenas 1 prazo (resolução). Tempo de primeira resposta não era monitorado.

**Problema**: Contratos ITIL v4 exigem 2 métricas separadas: tempo de resposta (primeira interação) e tempo de resolução (fechamento).

**Destino**: ✅ **ASSUMIDO** → RF-069 separa `Tempo_Resposta_Minutos` e `Tempo_Resolucao_Minutos` como campos distintos obrigatórios.

---

### RL-RN-006: SLA Aplicado Manualmente ao Criar Chamado

**Localizacao Código**: `CriarChamado.aspx.vb - Função btnSalvar_Click() - Linhas 200-220`

**Descrição**: Ao criar chamado, analista escolhia SLA manualmente em dropdown.

**Problema**: Escolha manual sujeita a erros (analista seleciona SLA errado, causando violação injusta ou compliance artificial).

**Destino**: ✅ **SUBSTITUÍDO** → RF-069 aplica SLA automaticamente baseado em regras de precedência (específico Cliente+Tipo+Prioridade → genérico → default).

---

### RL-RN-007: Nenhum Versionamento de Alterações

**Localizacao Código**: Não existia auditoria de mudanças em SLA

**Descrição**: Quando gerente alterava prazo de SLA (ex: de 4h para 8h), registro anterior era sobrescrito sem histórico.

**Problema**: Disputas contratuais sem rastreabilidade ("cliente afirma que SLA era 2h, mas foi alterado sem aviso").

**Destino**: ✅ **ASSUMIDO** → RF-069 implementa Temporal Tables SQL Server (versionamento imutável de todos os campos) + auditoria com motivo obrigatório.

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Existe no Legado | Existe no Moderno | Observação |
|----------------|------------------|-------------------|------------|
| **Cadastro de SLA** | ✅ Sim | ✅ Sim | Modernizado com validação real-time |
| **Tempo de Resposta** | ❌ Não | ✅ Sim | **NOVA** - Legado só tinha tempo de resolução |
| **Múltiplos Calendários** | ❌ Não | ✅ Sim | **NOVA** - Legado só tinha seg-sex 8-18h hardcoded |
| **Feriados Customizados** | Parcial | ✅ Sim | Legado só nacionais, moderno suporta todos os tipos |
| **Escalação Multi-Nível** | ❌ Não | ✅ Sim | **NOVA** - Legado só 1 e-mail |
| **Escalação Multi-Canal** | ❌ Não | ✅ Sim | **NOVA** - Legado só e-mail, moderno tem SMS/push/webhook |
| **Pausas Automáticas** | ❌ Não | ✅ Sim | **NOVA** - Legado era manual via SQL |
| **Simulador de Impacto** | ❌ Não | ✅ Sim | **NOVA** - Funcionalidade inexistente no legado |
| **Versionamento SLA** | ❌ Não | ✅ Sim | **NOVA** - Legado sobrescrevia sem histórico |
| **Aplicação Automática** | ❌ Não | ✅ Sim | **NOVA** - Legado era seleção manual |
| **Dashboard Compliance** | Parcial | ✅ Sim | Legado tinha relatório estático lento, moderno é real-time |
| **API REST** | ❌ Não | ✅ Sim | **NOVA** - Legado só tinha SOAP |
| **Multi-Tenancy Nativo** | ❌ Não | ✅ Sim | **NOVA** - Legado tinha banco separado por cliente |
| **Auditoria LGPD** | ❌ Não | ✅ Sim | **NOVA** - Legado não auditava mudanças |
| **Granularidade Minutos** | ❌ Não | ✅ Sim | Legado só aceitava horas inteiras (mínimo 1h) |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Temporal Tables SQL Server vs Tabela de Auditoria Custom

**Descrição**: Usar Temporal Tables nativo do SQL Server para versionamento imutável de SLAs.

**Motivo**:
- Temporal Tables é recurso nativo (alta performance)
- Auditoria automática sem código adicional
- Query `FOR SYSTEM_TIME ALL` facilita consulta de histórico
- Imutabilidade garantida pelo SQL Server

**Impacto**: **Médio**
- Requer SQL Server 2016+ (já planejado)
- Tabela de histórico cresce continuamente (requer particionamento anual)

**Alternativa Descartada**: Tabela `Auditoria_SLA` custom com triggers
- Mais trabalho de desenvolvimento
- Performance inferior
- Mais sujeita a bugs

---

### Decisão 2: Hangfire Background Jobs vs Windows Service

**Descrição**: Usar Hangfire para monitoramento contínuo de SLA e disparo de escalações.

**Motivo**:
- Integração nativa com ASP.NET Core
- Dashboard visual para debug
- Retry automático em falhas
- Escalabilidade horizontal (múltiplos workers)

**Impacto**: **Alto**
- Requer banco de dados Hangfire (separado do principal)
- Requer monitoramento de saúde do job

**Alternativa Descartada**: Windows Service separado
- Mais complexo de deploy
- Sem dashboard visual
- Escalabilidade limitada

---

### Decisão 3: Escalações Multi-Canal vs Apenas E-mail

**Descrição**: Suportar e-mail, SMS, push notification e webhook para escalações.

**Motivo**:
- SLAs críticos exigem notificação mais rápida que e-mail
- SMS tem taxa de abertura >90% vs ~20% e-mail
- Webhooks permitem integração com Slack, Teams, etc.

**Impacto**: **Alto**
- Requer integração com Twilio (SMS)
- Requer Firebase Cloud Messaging (push)
- Aumenta complexidade de configuração

**Alternativa Descartada**: Apenas e-mail (igual legado)
- Mais simples, mas insuficiente para SLAs críticos

---

### Decisão 4: Importação Automática de Feriados via BrasilAPI

**Descrição**: Integrar com API pública BrasilAPI para importar feriados nacionais automaticamente.

**Motivo**:
- Elimina atualização manual anual
- Sempre atualizado
- API gratuita e confiável

**Impacto**: **Baixo**
- Dependência de serviço externo (mitigado com cache local)
- Apenas feriados nacionais (estaduais/municipais ainda manuais)

**Alternativa Descartada**: Manter tabela estática
- Requer atualização manual todo ano
- Sujeita a esquecimento

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Perda de dados históricos** | CRÍTICO | Baixa | Script de migração com validação before/after + rollback |
| **Regras implícitas não mapeadas** | ALTO | Média | Revisão manual de 100% do código VB.NET + SQL + teste com dados reais |
| **Mudança de comportamento não comunicada** | ALTO | Média | Change log detalhado + treinamento obrigatório pré-go-live |
| **Performance inferior em cálculo de prazo** | MÉDIO | Baixa | Benchmark antes/depois + cache Redis agressivo |
| **Hangfire job parado sem alerta** | CRÍTICO | Média | Health check a cada 1min + alerta SMS se job parar >5min |
| **Falha na importação de feriados** | MÉDIO | Média | Fallback para lista estática local se API falhar |
| **Incompatibilidade calendários legado vs moderno** | ALTO | Alta | Script de conversão automática horário comercial → calendário "Comercial Padrão" |
| **Escalações não disparadas** | CRÍTICO | Baixa | Teste E2E obrigatório com SLA de 5min (fast-forward do tempo) |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Tipo | Referência RF Moderno | Status |
|-----------------|------|----------------------|--------|
| `Solicitacao_SLA` (tabela) | Tabela | `SLA_Chamado` (tabela modernizada) | ✅ Migrado |
| `Contrato_SLA_Operacao` (tabela) | Tabela | RF-028 (SLA Operações - fora do escopo RF-069) | ❌ Descartado (outro RF) |
| `pa_CalcularSLA` (stored procedure) | Stored Procedure | `CalculadoraSLA.cs` (CQRS Handler) | ✅ Substituído |
| `pa_ObterSLAPorCliente` (stored procedure) | Stored Procedure | `ObterSLAAplicavelQuery` (CQRS Query) | ✅ Substituído |
| `pa_RelatorioCompliance` (stored procedure) | Stored Procedure | Dashboard Angular + ApexCharts | ✅ Substituído |
| `ConfigurarSLA.aspx` (tela) | Tela ASPX | `/service-desk/sla/configurar` (Angular) | ✅ Substituído |
| `RelatorioSLA.aspx` (tela) | Tela ASPX | `/service-desk/sla/compliance` (Angular) | ✅ Substituído |
| `EscalacaoSLA.aspx` (tela) | Tela ASPX | `/service-desk/sla/escalacoes` (Angular) | ✅ Substituído |
| `WSSuporte.asmx/ObterSLAPorChamado` (webservice) | WebService SOAP | `GET /api/sla/chamado/{id}` (REST) | ✅ Substituído |
| `WSSuporte.asmx/CalcularPrazoSLA` (webservice) | WebService SOAP | `POST /api/sla/calcular-prazo` (REST) | ✅ Substituído |
| `WSSuporte.asmx/ValidarViolacaoSLA` (webservice) | WebService SOAP | `GET /api/sla/chamado/{id}/status` (REST) | ✅ Substituído |
| Horário comercial hardcoded | Regra Implícita | RN-RF069-06 (Calendários customizáveis) | ✅ Assumido |
| Feriados apenas nacionais | Regra Implícita | RN-RF069-07 (Feriados de todos os tipos) | ✅ Assumido |
| Escalação fixa 80% | Regra Implícita | RN-RF069-05 (Percentuais configuráveis) | ✅ Substituído |
| Pausa manual de SLA | Regra Implícita | RN-RF069-04 (Pausas automáticas) | ✅ Assumido |
| Sem versionamento | Problema Arquitetural | RN-RF069-08 (Temporal Tables) | ✅ Assumido |
| Aplicação manual de SLA | Regra Implícita | RN-RF069-10 (Aplicação automática) | ✅ Substituído |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-30 | Referência completa ao legado extraída do RF-069 v1.0. Todos os itens com destino definido (ASSUMIDO/SUBSTITUÍDO/DESCARTADO). | Agência ALC - alc.dev.br |

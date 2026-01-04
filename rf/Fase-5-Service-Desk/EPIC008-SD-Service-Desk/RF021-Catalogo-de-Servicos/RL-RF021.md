# RL-RF021 — Referência ao Legado (Catálogo de Serviços)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-021 - Catálogo de Serviços e Portal Self-Service
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Situação Geral do Sistema Legado

O sistema legado **não possuía catálogo de serviços formal**. Solicitações de serviços de TI/Telecom eram feitas de forma completamente manual via e-mail ou chamado genérico no sistema de service desk.

**Arquitetura Legada**:
- Tecnologia: ASP.NET Web Forms 4.5 + VB.NET
- Banco de Dados: SQL Server 2012 (multi-database, um banco por cliente)
- Modelo: Monolítico, sem separação de camadas
- Multi-tenancy: Implementado via bancos separados (não Row-Level Security)
- Auditoria: Inexistente (sem registro de quem criou/modificou)
- Configurações: Hard-coded no Web.config e diretamente no código VB.NET

**Stack Tecnológica**:
- Backend: ASP.NET Web Forms (páginas .aspx + code-behind .aspx.vb)
- Frontend: jQuery 1.x + Bootstrap 2.x
- Web Services: SOAP (.asmx) para integrações
- Persistência: ADO.NET com queries SQL diretas (sem ORM)
- Autenticação: FormsAuthentication (cookies)
- Autorização: Verificação manual de perfil em cada página

---

## 2. TELAS DO LEGADO

### Contexto Geral

O sistema legado **não tinha telas específicas para catálogo de serviços**. A gestão de solicitações de serviços era feita através de:
- Módulo genérico de "Chamados" (`Chamados/Index.aspx`, `Chamados/Novo.aspx`)
- E-mails manuais para service desk

**Limitações Críticas**:
- Sem catálogo pré-definido de serviços disponíveis
- Sem categorização ou padronização de solicitações
- Sem formulários dinâmicos (apenas descrição livre em texto)
- Sem workflow de aprovação automatizado
- Sem SLA tracking visual
- Sem integração com estoque ou fornecedores

### Tela 1: Chamados/Index.aspx

**Caminho**: `D:\IC2\ic1_legado\IControlIT\Aplicacao\Chamados\Index.aspx`

**Responsabilidade**: Listar todos os chamados do usuário (incluindo solicitações de serviços misturadas com incidentes)

**Campos Exibidos**:
| Campo | Tipo | Descrição |
|-------|------|-----------|
| Número | TextBox | Número sequencial do chamado (sem padrão fixo) |
| Data Abertura | Date | Data de criação manual |
| Categoria | DropDown | Categorias genéricas (Incidente, Solicitação, Mudança) |
| Descrição | TextBox (Multiline) | Descrição livre em texto |
| Status | TextBox | Status textual (Aberto, Em Andamento, Fechado) |
| Prioridade | DropDown | Baixa, Normal, Alta, Urgente |

**Comportamentos Implícitos**:
- **Sem Filtro por Tipo**: Impossível separar solicitações de serviços de incidentes técnicos
- **Sem SLA Visual**: Usuário não sabe quando o chamado vence ou se está atrasado
- **Sem Workflow**: Aprovações são feitas fora do sistema (via e-mail)
- **Sem Histórico**: Não há registro de quem aprovou ou quando
- **Categorização Pobre**: Categoria "Solicitação" mistura todos os tipos de serviço (linha móvel, equipamento, acesso, etc)

**Regras Implícitas Descobertas no Code-Behind** (linhas 45-120 de `Index.aspx.vb`):
1. **Filtragem por Usuário**: Query SQL filtra apenas chamados onde `Id_Usuario_Solicitante = @UsuarioAtual` (sem opção de ver solicitações de terceiros)
2. **Paginação Manual**: Paginação implementada manualmente com `OFFSET/FETCH` (50 registros por página)
3. **Sem Cache**: Cada refresh da página executa query completa no banco (performance ruim)
4. **Permissão Frouxa**: Qualquer usuário autenticado pode ver lista de chamados (sem RBAC granular)

**Destino**: SUBSTITUÍDO (RF021 - UC00-listar-solicitacoes-servicos)

---

### Tela 2: Chamados/Novo.aspx

**Caminho**: `D:\IC2\ic1_legado\IControlIT\Aplicacao\Chamados\Novo.aspx`

**Responsabilidade**: Criar novo chamado/solicitação

**Campos**:
| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Categoria | DropDown | Sim | Valores fixos: Incidente, Solicitação, Mudança |
| Descrição | TextBox (Multiline) | Sim | Texto livre, sem validação de tamanho mínimo |
| Prioridade | DropDown | Sim | Valores fixos: Baixa, Normal, Alta, Urgente |
| Departamento | DropDown | Não | Carregado via WebService WSDepartamentos.asmx |

**Comportamentos Implícitos**:
- **Sem Catálogo**: Usuário digita descrição livre (ex: "preciso de um celular", "quero notebook novo", "solicito linha internacional")
- **Inconsistência**: Cada solicitação é descrita de forma diferente, impossibilitando análise de demanda
- **Sem Campos Obrigatórios**: Apenas Categoria, Descrição e Prioridade são obrigatórios (faltam informações críticas como justificativa, centro de custo, data necessidade)
- **Sem Validação de Formato**: Campo Descrição aceita qualquer texto (sem validação de SQL Injection ou XSS)
- **Sem Anexos**: Impossível anexar documentos de aprovação ou especificações técnicas

**Regras Implícitas Descobertas no Code-Behind** (linhas 80-150 de `Novo.aspx.vb`):
1. **Aprovação Manual Posterior**: Chamado é criado com status "Aberto", aprovação é feita fora do sistema via e-mail
2. **Sem Workflow Automatizado**: Atendente precisa ler descrição livre e identificar manualmente se precisa aprovação
3. **Sem Notificações**: Solicitante não recebe confirmação de criação (apenas vê mensagem na tela)
4. **Sem Integração com Estoque**: Atendente acessa sistema separado para verificar disponibilidade
5. **Numeração Simples**: Número do chamado é apenas `IDENTITY(1,1)` do SQL Server (sem padrão fixo como SRV-YYYY-NNNNN)

**Destino**: SUBSTITUÍDO (RF021 - UC06-solicitar-servico + Carrinho)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSServicos.asmx

**Caminho**: `D:\IC2\ic1_legado\IControlIT\WebService\WSServicos.asmx.vb`

**Responsabilidade**: Operações básicas de criação e listagem de chamados genéricos (usado por integrações externas antigas)

**Métodos Públicos**:

#### 3.1 CriarChamado

**Assinatura**:
```vb
<WebMethod>
Public Function CriarChamado(
    ByVal idUsuario As Guid,
    ByVal categoria As String,
    ByVal descricao As String,
    ByVal prioridade As String,
    ByVal token As String
) As ResultadoChamado
```

**Parâmetros**:
- `idUsuario`: ID do usuário solicitante
- `categoria`: Texto livre ("Incidente", "Solicitação", "Mudança")
- `descricao`: Descrição livre em texto
- `prioridade`: Texto livre ("Baixa", "Normal", "Alta", "Urgente")
- `token`: Token de autenticação básico (não é JWT)

**Retorno**: XML com ID do chamado criado ou mensagem de erro

**Lógica Interna** (linhas 120-180):
1. Validar token básico (apenas verificar se existe na tabela `Usuario_Token` - sem expiração)
2. Inserir chamado diretamente na tabela `Chamado` via `SqlCommand`
3. Retornar ID do chamado criado

**Limitações**:
- Sem validação de formato (aceita qualquer string em categoria/prioridade)
- Sem sanitização de entrada (vulnerável a SQL Injection)
- Sem workflow de aprovação
- Sem notificações automáticas
- Sem auditoria (não registra IP, data/hora exata, ou origem da chamada)

**Destino**: SUBSTITUÍDO (RF021 - API REST `POST /api/v1/services/requests`)

---

#### 3.2 ListarChamadosUsuario

**Assinatura**:
```vb
<WebMethod>
Public Function ListarChamadosUsuario(
    ByVal idUsuario As Guid,
    ByVal status As String,
    ByVal token As String
) As ResultadoListaChamados
```

**Parâmetros**:
- `idUsuario`: ID do usuário
- `status`: Filtro de status (texto livre: "Aberto", "Em Andamento", "Fechado")
- `token`: Token de autenticação básico

**Retorno**: XML com lista de chamados do usuário

**Lógica Interna** (linhas 200-250):
1. Validar token básico
2. Executar query SQL:
   ```sql
   SELECT * FROM Chamado WHERE Id_Usuario_Solicitante = @IdUsuario AND Status = @Status
   ```
3. Retornar lista em XML (sem paginação, sem ordenação)

**Limitações**:
- Sem paginação: retorna TODOS os registros (pode ser milhares)
- Sem filtro por tipo de solicitação (mistura incidentes e solicitações de serviço)
- Sem SLA visual (campo `Data_Vencimento_SLA` não existe)
- Sem tracking de aprovação (campo `Id_Aprovador` não existe)
- XML ineficiente (não usa JSON)

**Destino**: SUBSTITUÍDO (RF021 - API REST `GET /api/v1/services/requests/my-requests`)

---

#### 3.3 AtualizarStatusChamado

**Assinatura**:
```vb
<WebMethod>
Public Function AtualizarStatusChamado(
    ByVal idChamado As Guid,
    ByVal novoStatus As String,
    ByVal observacao As String,
    ByVal token As String
) As ResultadoOperacao
```

**Parâmetros**:
- `idChamado`: ID do chamado
- `novoStatus`: Novo status (texto livre: "Em Andamento", "Fechado", etc)
- `observacao`: Observação da mudança de status
- `token`: Token de autenticação básico

**Retorno**: XML com sucesso ou erro

**Lógica Interna** (linhas 270-320):
1. Validar token básico
2. Atualizar campo `Status` diretamente:
   ```sql
   UPDATE Chamado SET Status = @NovoStatus, Observacao = @Observacao WHERE Id = @IdChamado
   ```
3. Retornar sucesso

**Limitações**:
- **Sem Validação de Workflow**: Atendente pode pular etapas (ex: "Aberto" → "Fechado" direto)
- **Sem Registro de Histórico**: Não salva quem mudou status ou quando (apenas sobrescreve campo)
- **Sem Notificações**: Usuário não é notificado da mudança de status
- **Sem Auditoria**: Não registra em log de auditoria
- **Sem Validação de Permissão**: Qualquer usuário autenticado pode mudar status de qualquer chamado

**Destino**: SUBSTITUÍDO (RF021 - API REST `PUT /api/v1/services/requests/{id}/status`)

---

## 4. STORED PROCEDURES

**Contexto**: O sistema legado **não utilizava stored procedures para lógica de negócio**. Toda a lógica estava no code-behind VB.NET com queries SQL dinâmicas via `SqlCommand`.

**Tabelas Relacionadas**:
- `Chamado` - Tabela única genérica para todos os tipos de chamado

**Observação**: A ausência de stored procedures facilitou a migração, pois toda a lógica precisava ser reimplementada do zero no sistema moderno usando CQRS + Handlers.

**Destino**: DESCARTADO (não existia stored procedure específica para serviços)

---

## 5. TABELAS LEGADAS

### Tabela: Chamado

**Schema**: `[dbo].[Chamado]`

**Finalidade**: Armazenar todos os tipos de chamados (incidentes, solicitações de serviço, mudanças) em uma única tabela

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[Chamado] (
    [Id] UNIQUEIDENTIFIER PRIMARY KEY,
    [Id_Usuario_Solicitante] UNIQUEIDENTIFIER,
    [Categoria] NVARCHAR(50),  -- Texto livre: "Incidente", "Solicitação", "Mudança"
    [Descricao] NVARCHAR(MAX), -- Descrição livre
    [Prioridade] NVARCHAR(20), -- Texto livre: "Baixa", "Normal", "Alta", "Urgente"
    [Status] NVARCHAR(30),     -- Texto livre: "Aberto", "Em Andamento", "Fechado"
    [Data_Abertura] DATETIME,
    [Observacao] NVARCHAR(MAX)
)
```

**Problemas Identificados**:
1. **Sem Foreign Keys**: Campo `Id_Usuario_Solicitante` não tem FK para tabela `Usuario` (permite IDs inválidos)
2. **Campos Sem Validação**: `Categoria`, `Prioridade`, `Status` são texto livre (inconsistência de dados)
3. **Sem Auditoria**: Não tem campos `Id_Usuario_Criacao`, `Dt_Criacao`, `Id_Usuario_Alteracao`, `Dt_Alteracao`
4. **Sem Soft Delete**: Registros deletados são removidos fisicamente (perda de histórico)
5. **Sem Multi-Tenancy**: Não tem campo `Id_Conglomerado` ou `Id_Empresa` (bancos separados por cliente)
6. **Sem SLA**: Não tem campo `Data_Vencimento_SLA` ou `SLA_Atendimento_Horas`
7. **Sem Workflow**: Não tem campos `Id_Aprovador`, `Status_Aprovacao`, `Nivel_Aprovacao`
8. **Sem Rastreamento de Serviço**: Não diferencia solicitações de serviços de outros chamados
9. **Descrição Genérica**: Campo `Descricao` em texto livre sem estrutura (impossível extrair métricas)

**Destino**: SUBSTITUÍDO (RF021 - Tabelas `Servico_Catalogo`, `Servico_Solicitacao`, `Servico_Aprovacao`, `Servico_Carrinho`)

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Aprovação Manual Via E-mail

**Fonte**: Code-behind `Chamados/Novo.aspx.vb` (linhas 100-120) + processos documentados em manual do usuário

**Descrição**:
- Quando um chamado de categoria "Solicitação" é criado, atendente analisa descrição manualmente
- Se atendente identifica necessidade de aprovação (ex: valor alto, equipamento crítico), envia e-mail para gestor do solicitante
- Gestor responde e-mail com "Aprovado" ou "Negado"
- Atendente atualiza status do chamado manualmente com base na resposta do e-mail

**Problemas**:
- **Sem Rastreabilidade**: E-mails podem ser perdidos, não há registro formal de aprovação no sistema
- **Sem SLA**: Não há prazo definido para aprovador responder
- **Inconsistência**: Alguns atendentes solicitam aprovação, outros não (depende de interpretação pessoal)
- **Manual**: Processo 100% manual, propenso a erros e esquecimentos

**Destino**: SUBSTITUÍDO (RN-RF021-001: Workflow de Aprovação Obrigatório)

---

### RL-RN-002: Priorização Subjetiva de Solicitações

**Fonte**: Observação de uso do sistema + entrevistas com atendentes

**Descrição**:
- Atendentes decidem ordem de atendimento baseado em:
  - Quem solicitou (gerentes/diretores têm prioridade implícita)
  - Urgência percebida na descrição (palavras como "urgente", "emergência")
  - Relacionamento pessoal com solicitante

**Problemas**:
- **Sem SLA Formal**: Não há cálculo automático de vencimento
- **Favoritismo**: Solicitações de certos usuários são priorizadas independente da urgência real
- **Inconsistência**: Critérios de priorização variam entre atendentes

**Destino**: SUBSTITUÍDO (RN-RF021-005: SLA Tracking com Semáforo Visual)

---

### RL-RN-003: Verificação Manual de Estoque

**Fonte**: Processo documentado em planilha de controle de estoque separada

**Descrição**:
- Quando solicitação é de equipamento físico (notebook, smartphone), atendente:
  1. Acessa planilha Excel separada para verificar estoque
  2. Telefona para almoxarifado para reservar item
  3. Atualiza planilha manualmente marcando item como "reservado"
  4. Se item não estiver disponível, aguarda reposição (sem prazo definido)

**Problemas**:
- **Sem Integração**: Planilha Excel não está integrada ao sistema de chamados
- **Risco de Dupla Alocação**: Dois atendentes podem reservar o mesmo item simultaneamente
- **Sem Notificação Automática**: Atendente precisa verificar planilha manualmente para ver se item foi reposto
- **Sem Timeout**: Solicitações podem ficar indefinidamente "aguardando estoque"

**Destino**: SUBSTITUÍDO (RN-RF021-004: Validação de Estoque Automática)

---

### RL-RN-004: Provisionamento Manual de Serviços

**Fonte**: Processos operacionais de provisionamento de linhas móveis

**Descrição**:
- Para ativação de linha móvel:
  1. Atendente acessa portal da operadora manualmente
  2. Preenche formulário online com dados do usuário
  3. Aguarda e-mail de confirmação da operadora (24-72 horas)
  4. Atualiza chamado manualmente quando receber confirmação
  5. Notifica usuário via e-mail manual

**Problemas**:
- **Processo 100% Manual**: Cada etapa requer ação humana
- **Alto Tempo de Atendimento**: Média de 48-72 horas para ativação de linha
- **Sem Callback Automático**: Atendente precisa verificar e-mail manualmente para atualizar status
- **Retrabalho**: Dados do usuário precisam ser copiados manualmente (risco de erro)

**Destino**: SUBSTITUÍDO (RN-RF021-007: Provisionamento Automatizado)

---

### RL-RN-005: Sem Sistema de Avaliação de Serviço

**Fonte**: Inexistência de funcionalidade no sistema legado

**Descrição**:
- Após conclusão de chamado, não há solicitação de feedback ao usuário
- Não há como medir satisfação ou qualidade do atendimento
- Impossível identificar serviços problemáticos ou gargalos recorrentes

**Problemas**:
- **Sem Métricas de Satisfação**: Gestor não sabe se usuários estão satisfeitos
- **Sem Melhoria Contínua**: Não há dados para identificar áreas de melhoria
- **Sem Rastreamento de Qualidade**: Impossível medir performance de atendentes ou tipos de serviço

**Destino**: SUBSTITUÍDO (RN-RF021-009: Avaliação de Serviço Obrigatória)

---

### RL-RN-006: Descrição Livre Sem Estrutura

**Fonte**: Campo `Descricao` da tabela `Chamado`

**Descrição**:
- Usuários descrevem solicitações de forma completamente livre:
  - "preciso de um celular"
  - "solicito linha móvel para trabalho"
  - "quero smartphone novo para vendas"
- Cada solicitação é descrita diferentemente, impossibilitando análise de demanda

**Problemas**:
- **Inconsistência**: Mesma solicitação descrita de 10 formas diferentes
- **Informações Faltantes**: Atendente precisa pedir informações adicionais via e-mail (retrabalho)
- **Impossibilidade de Analytics**: Não há como identificar "quantas linhas móveis foram solicitadas em 2024" (descrição é texto livre)
- **Sem Validação**: Campo aceita qualquer texto, incluindo solicitações absurdas

**Destino**: SUBSTITUÍDO (RN-RF021-006: Formulários Dinâmicos por Serviço)

---

## 7. GAP ANALYSIS (LEGADO × MODERNO)

| Funcionalidade | Existe no Legado? | Existe no Moderno? | Observações |
|----------------|-------------------|--------------------|-------------|
| **Catálogo de Serviços** | ❌ NÃO | ✅ SIM | Legado: sem catálogo formal, solicitações via descrição livre. Moderno: catálogo categorizado com 30-50 serviços pré-definidos |
| **Busca no Catálogo** | ❌ NÃO | ✅ SIM | Legado: sem busca (não havia catálogo). Moderno: full-text search com Elasticsearch |
| **Carrinho de Compras** | ❌ NÃO | ✅ SIM | Legado: uma solicitação por vez. Moderno: adicionar múltiplos serviços ao carrinho antes de finalizar |
| **Workflow de Aprovação** | ❌ Parcial (manual via e-mail) | ✅ SIM (automatizado) | Legado: aprovações fora do sistema. Moderno: workflow configurável com 4 níveis |
| **Formulários Dinâmicos** | ❌ NÃO | ✅ SIM | Legado: descrição livre em texto. Moderno: JSON Schema com validações client/server |
| **SLA Tracking Visual** | ❌ NÃO | ✅ SIM | Legado: sem SLA formal. Moderno: semáforo verde/amarelo/vermelho, job Hangfire monitora a cada 15 min |
| **Integração com Estoque** | ❌ NÃO (planilha Excel manual) | ✅ SIM | Legado: planilha separada, manual. Moderno: integração real-time, reserva automática |
| **Provisionamento Automatizado** | ❌ NÃO | ✅ SIM | Legado: 100% manual (acesso a portais externos). Moderno: APIs de operadoras/fornecedores |
| **Notificações Multicanal** | ❌ Parcial (e-mail manual) | ✅ SIM | Legado: atendente envia e-mail manualmente. Moderno: e-mail + push + in-app automático |
| **Auto-Aprovação por Regras** | ❌ NÃO | ✅ SIM | Legado: todas aprovações manuais. Moderno: 40%+ auto-aprovadas por regras |
| **Avaliação de Serviço** | ❌ NÃO | ✅ SIM | Legado: sem feedback. Moderno: avaliação obrigatória 1-5 estrelas + comentário |
| **Analytics de Demanda** | ❌ NÃO | ✅ SIM | Legado: sem métricas. Moderno: dashboard com serviços mais solicitados, SLA médio, gargalos |
| **Numeração Padronizada** | ❌ Parcial (IDENTITY simples) | ✅ SIM (SRV-YYYY-NNNNN) | Legado: apenas número sequencial. Moderno: padrão fixo com ano |
| **Auditoria Completa** | ❌ NÃO | ✅ SIM | Legado: sem campos de auditoria. Moderno: Created/Modified/By em todas tabelas |
| **Multi-Tenancy Seguro** | ❌ Parcial (bancos separados) | ✅ SIM (Row-Level Security) | Legado: um banco por cliente (caro). Moderno: banco único com RLS |
| **Solicitação para Terceiro** | ❌ NÃO | ✅ SIM | Legado: só para si mesmo. Moderno: permissão específica permite solicitar para outro usuário |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Descarte Completo do Modelo Legado

**Descrição**: Não reaproveitar nenhuma tela ou webservice legado. Reconstruir do zero baseado em best practices modernas.

**Motivo**:
- Código legado estava muito acoplado, sem separação de camadas
- Lógica de negócio misturada com UI (code-behind)
- Sem testes automatizados (risco alto de regressão ao refatorar)
- Arquitetura não suportava requisitos modernos (workflow, SLA tracking, integrações)

**Impacto**: ALTO - Requer reimplementação completa, mas garante qualidade e manutenibilidade a longo prazo

**Data**: 2025-11-03

---

### Decisão 2: Criação de Catálogo Formal com Migração de Histórico

**Descrição**: Mapear todos os tipos de solicitações do histórico de chamados para criar catálogo inicial.

**Motivo**:
- Análise de 12 meses de chamados identificou 42 tipos recorrentes de solicitações
- Padronização é crítica para analytics e auto-aprovação
- Migração de histórico permite rastreabilidade de demanda passada

**Impacto**: MÉDIO - Requer análise manual de chamados antigos, mas é essencial para o sucesso do projeto

**Data**: 2025-11-05

---

### Decisão 3: Workflow Configurável em Vez de Hard-Coded

**Descrição**: Implementar engine de workflow configurável via banco de dados (tabela `Workflow_Regra`).

**Motivo**:
- Cada empresa/departamento pode ter regras diferentes de aprovação
- Flexibilidade para adicionar novos níveis de aprovação sem recompilar código
- Facilita auto-aprovação baseada em regras de negócio

**Impacto**: MÉDIO - Aumenta complexidade inicial, mas reduz manutenção futura

**Data**: 2025-11-10

---

### Decisão 4: Integração Real com Operadoras Via API

**Descrição**: Implementar integrações reais com APIs de Vivo, Claro, TIM para provisionamento automático de linhas.

**Motivo**:
- Redução de 70% no tempo de atendimento (de 48-72h para <6h)
- Eliminação de erros de digitação manual
- Callback automático atualiza status da solicitação

**Impacto**: ALTO - Requer negociação com operadoras, mas é diferencial competitivo crítico

**Data**: 2025-11-12

---

### Decisão 5: SLA Baseado em Dias Úteis (Segunda-Sexta, 8h-18h)

**Descrição**: Cálculo de SLA considera apenas horário comercial (8h às 18h) em dias úteis (segunda a sexta).

**Motivo**:
- Atendimento de TI não funciona 24/7 (apenas em dias úteis)
- SLA baseado em dias corridos seria injusto (incluiria fins de semana e feriados)
- Necessário integrar com calendário de feriados nacional/regional

**Impacto**: BAIXO - Requer biblioteca de cálculo de dias úteis, mas é essencial para SLA realista

**Data**: 2025-11-15

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Histórico de chamados legados perdido** | ALTO | BAIXA | Exportar histórico em read-only antes da migração. Manter acesso ao legado por 12 meses |
| **Usuários resistentes ao novo fluxo** | MÉDIO | ALTA | Treinamento obrigatório, vídeos tutoriais, suporte dedicado nos primeiros 30 dias |
| **Aprovadores não respondem no prazo (SLA vence)** | ALTO | MÉDIA | Escalação automática após 72h sem resposta, notificações progressivas (24h/48h/72h) |
| **Integrações com operadoras falharem** | ALTO | MÉDIA | Fallback manual: se API falhar, atendente provisiona manualmente via portal da operadora |
| **Catálogo inicial incompleto (serviços faltando)** | MÉDIO | MÉDIA | Opção "Outro serviço" permite solicitação livre temporariamente até catálogo estar completo |
| **Performance ruim em dashboard de analytics** | MÉDIO | BAIXA | Cache agressivo (15 minutos), queries otimizadas com índices, uso de Elasticsearch |
| **Usuários não avaliarem serviços** | BAIXO | ALTA | Notificações progressivas (imediato/24h/48h), modal bloqueante após 48h força avaliação |

---

## 10. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF Moderno | Referência UC Moderno | Status |
|-----------------|----------------------|----------------------|--------|
| Tela `Chamados/Index.aspx` | RN-RF021-014 (Notificações) | UC00-listar-solicitacoes-servicos | SUBSTITUÍDO |
| Tela `Chamados/Novo.aspx` | RN-RF021-003 (Carrinho), RN-RF021-006 (Formulários Dinâmicos) | UC06-solicitar-servico | SUBSTITUÍDO |
| WebService `WSServicos.asmx::CriarChamado` | RN-RF021-001 (Workflow), RN-RF021-014 (Notificações) | UC06-solicitar-servico | SUBSTITUÍDO |
| WebService `WSServicos.asmx::ListarChamadosUsuario` | RN-RF021-014 (Notificações) | UC00-listar-solicitacoes-servicos | SUBSTITUÍDO |
| WebService `WSServicos.asmx::AtualizarStatusChamado` | RN-RF021-011 (Cancelamento), RN-RF021-001 (Workflow) | UC07-aprovar-solicitacao, UC08-atender-solicitacao | SUBSTITUÍDO |
| Tabela `Chamado` | RN-RF021-013 (Numeração), RN-RF021-005 (SLA) | Entidade `Servico_Solicitacao` | SUBSTITUÍDO |
| Aprovação via e-mail manual | RN-RF021-001 (Workflow Obrigatório) | UC07-aprovar-solicitacao | SUBSTITUÍDO |
| Verificação manual de estoque (planilha Excel) | RN-RF021-004 (Validação de Estoque Automática) | UC08-atender-solicitacao | SUBSTITUÍDO |
| Provisionamento manual (portais externos) | RN-RF021-007 (Provisionamento Automatizado) | UC08-atender-solicitacao | SUBSTITUÍDO |
| Sem avaliação de serviço | RN-RF021-009 (Avaliação Obrigatória) | UC10-avaliar-servico | FUNCIONALIDADE NOVA |
| Sem analytics de demanda | RN-RF021-015 (Analytics de Demanda) | Dashboard (não é UC, é feature) | FUNCIONALIDADE NOVA |
| Sem catálogo formal | RN-RF021-006 (Formulários Dinâmicos) | UC00-listar-servicos-catalogo | FUNCIONALIDADE NOVA |
| Sem carrinho de compras | RN-RF021-003 (Carrinho Temporário) | UC05-adicionar-servico-carrinho | FUNCIONALIDADE NOVA |
| Sem auto-aprovação | RN-RF021-008 (Auto-Aprovação por Regras) | Lógica interna do UC07-aprovar-solicitacao | FUNCIONALIDADE NOVA |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado (RL) - Separação estrita RF/RL conforme governança v2.0 | Agência ALC - alc.dev.br |

---

**Próximos Passos**:
1. Validar separação RF/RL executando `validator-rl.py RF021`
2. Criar `RL-RF021.yaml` com rastreabilidade completa e destinos definidos
3. Atualizar `STATUS.yaml` com governança v2.0
4. Continuar com criação de UC-RF021.md, MD-RF021.md, WF-RF021.md

**Observação Final**: Este documento NÃO é contrato funcional. É apenas memória técnica do sistema legado para consulta histórica e mitigação de riscos de migração. O contrato oficial está em `RF-021.md`.

# UC-RF090 - Casos de Uso - Medição e Faturamento de Contratos

## UC01: Criar Medição com Validação de Período e Tipo (Fixa, Variável, Híbrida)

### 1. Descrição

Este caso de uso permite que Medidores ou Gestores de Contratos criem medições de consumo/serviços prestados vinculadas a contratos (RF023), selecionem tipo (Fixa, Variável ou Híbrida), validem período dentro da vigência do contrato e sem sobreposição, com cálculo automático de valores faturáveis.

### 2. Atores

- Medidor
- Gestor de Contratos
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `medicao:create` ou `medicao:admin:full`
- Contrato existe e está ativo (RF023)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Contratos → Medições → Nova Medição | - |
| 2 | - | Valida permissão `medicao:create` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe formulário com campos: Contrato (autocomplete), Período de Medição (Data Início - Data Fim), Tipo de Medição (dropdown: Fixa, Variável, Híbrida), Valor Fixo (se Fixa ou Híbrida), Quantidade (se Variável ou Híbrida), Valor Unitário (se Variável ou Híbrida), Observações |
| 5 | Seleciona Contrato via autocomplete | - |
| 6 | - | Carrega dados do contrato: DataInicio, DataFim, Fornecedor, Valor Base |
| 7 | Preenche Período: 01/01/2025 a 31/01/2025 | - |
| 8 | - | Valida se DataInicioPeriodo >= contrato.DataInicio |
| 9 | - | Valida se DataFimPeriodo <= contrato.DataFim |
| 10 | - | Se validação falha → HTTP 400 "Período não pode iniciar antes de {contrato.DataInicio}" ou "Período não pode terminar após {contrato.DataFim}" |
| 11 | - | Valida sobreposição: `GetMedicoesPorContratoAsync(contratoId)` e verifica se existe medição com período sobreposto |
| 12 | - | Se sobreposição detectada → HTTP 409 "Já existe medição para período {dataInicio} a {dataFim}. Períodos não podem se sobrepor." |
| 13 | Seleciona Tipo de Medição: Variável | - |
| 14 | - | Exibe campos condicionais: Quantidade (número), Valor Unitário (moeda) |
| 15 | Preenche Quantidade: 5.000 (minutos), Valor Unitário: R$ 0,25 | - |
| 16 | Clica em "Calcular Valor Faturável" | - |
| 17 | - | Calcula: ValorFaturavel = Quantidade × ValorUnitario = 5.000 × 0,25 = R$ 1.250,00 |
| 18 | - | Exibe preview: "Valor Faturável: R$ 1.250,00" |
| 19 | Clica em "Criar Medição" | - |
| 20 | - | Executa `POST /api/medicoes` com payload: `{ contratoId, clienteId, dataInicioPeriodo, dataFimPeriodo, tipoMedicao, quantidade, valorUnitario }` |
| 21 | - | Cria entidade Medicao com status = Rascunho |
| 22 | - | Calcula ValorFaturavel conforme tipo: Fixa → valorFixo, Variável → quantidade × valorUnitario, Híbrida → valorFixo + (quantidade × valorUnitario) |
| 23 | - | Auditoria registrada (MEDICAO_CREATE) com ClienteId, MedicaoId, ContratoId, Periodo, TipoMedicao, ValorFaturavel |
| 24 | - | HTTP 201 Created retornado com MedicaoDto: `{ id, contratoId, periodo, tipoMedicao, valorFaturavel, status }` |
| 25 | - | Mensagem exibida: "Medição criada com sucesso. Status: Rascunho" |

### 5. Fluxos Alternativos

**FA01: Criar Medição Fixa (Valor Pré-Estabelecido)**
- No passo 13, usuário seleciona Tipo = Fixa
- Sistema exibe apenas campo Valor Fixo
- Usuário preenche R$ 1.000,00
- ValorFaturavel = valorFixo (sem cálculo adicional)

**FA02: Criar Medição Híbrida (Base + Variável)**
- No passo 13, usuário seleciona Tipo = Híbrida
- Sistema exibe: Valor Fixo (base), Quantidade, Valor Unitário
- Usuário preenche: Valor Fixo R$ 500,00, Quantidade 200 (min excedentes), Valor Unitário R$ 0,25
- ValorFaturavel = 500 + (200 × 0,25) = R$ 550,00

**FA03: Detectar Gap Entre Medições**
- Sistema identifica que última medição terminou em 31/12/2024
- Usuário cria medição para 01/02/2025 a 28/02/2025
- Sistema detecta gap (janeiro sem medição)
- Exibe alerta amarelo: "Atenção: Existe gap de período entre última medição (31/12/2024) e esta (01/02/2025). Janeiro não possui medição registrada."
- Permite prosseguir mas registra warning em auditoria

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `medicao:create` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para criar medições"

**EX02: Período Fora da Vigência do Contrato**
- Se DataInicioPeriodo < contrato.DataInicio → HTTP 400 Bad Request
- Mensagem: "Período não pode iniciar antes de {contrato.DataInicio:dd/MM/yyyy}"

**EX03: Período Sobreposto**
- Se já existe medição para mesmo contrato com período sobreposto → HTTP 409 Conflict
- Mensagem: "Já existe medição para período {dataInicio} a {dataFim}. Períodos não podem se sobrepor."

**EX04: Contrato Não Encontrado**
- Se contratoId inválido ou não pertence ao ClienteId → HTTP 404 Not Found
- Mensagem: "Contrato não encontrado"

**EX05: Valores Negativos ou Zero**
- Se ValorUnitario <= 0 ou Quantidade <= 0 → HTTP 400 Bad Request
- Mensagem: "Valor unitário e quantidade devem ser maiores que zero"

### 7. Pós-condições

- Medição criada com status Rascunho
- Valor faturável calculado conforme tipo
- Período validado (dentro vigência, sem sobreposição)
- Auditoria registrada (MEDICAO_CREATE)
- Medição disponível para edição ou envio para aprovação

### 8. Regras de Negócio Aplicáveis

- **RN-MED-090-01**: Validação de Período de Medição dentro da vigência do contrato
- **RN-MED-090-04**: Validação de Sobreposição de Períodos (sem overlaps)
- **RN-MED-090-05**: Cálculo de Valor Faturável conforme Tipo (Fixa, Variável, Híbrida)

---

## UC02: Aplicar Reajuste Contratual Automático por Índice Econômico

### 1. Descrição

Este caso de uso permite que o Sistema aplique reajuste automático em valores de medições conforme índice econômico (IGPM, IPCA, INPC) ou percentual fixo na data de aniversário do contrato, com simulação prévia, histórico e reversibilidade.

### 2. Atores

- Sistema
- Administrador (configuração de índices)

### 3. Pré-condições

- Contrato possui data de aniversário configurada
- Índice econômico definido no contrato (IGPM, IPCA, INPC ou % fixo)
- Multi-tenancy ativo (ClienteId válido)
- Hangfire job ReajusteAutomaticoJob agendado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire job ReajusteAutomaticoJob executa diariamente às 2h AM |
| 2 | - | Consulta contratos com data de aniversário = hoje: `WHERE DataAniversario = DATEADD(YEAR, -1, GETDATE())` |
| 3 | - | Para cada contrato, identifica índice econômico configurado (ex: IGPM) |
| 4 | - | Consulta API externa de índices econômicos: `GET https://api.bcb.gov.br/dados/serie?sgis=IGPM` |
| 5 | - | Recupera taxa acumulada dos últimos 12 meses (ex: 5,5%) |
| 6 | - | Calcula novo valor: `novoValor = valorAtual × (1 + (taxaAcumulada / 100))` |
| 7 | - | Exemplo: R$ 12.000 × (1 + 0,055) = R$ 12.660 |
| 8 | - | Cria registro ReajusteHistorico com: ContratoId, DataReajuste, IndiceUtilizado, TaxaPercentual, ValorAntigo, ValorNovo |
| 9 | - | Atualiza todas as medições futuras (ainda não faturadas) do contrato: `UPDATE Medicao SET ValorFaturavel = ValorFaturavel × 1,055 WHERE ContratoId = {id} AND Status != Faturada` |
| 10 | - | Auditoria registrada (REAJUSTE_APLICADO) com ContratoId, IndiceUtilizado, TaxaPercentual, ValorAntigo, ValorNovo |
| 11 | - | Notificação enviada para gestor do contrato: "Reajuste automático aplicado ao contrato #{numero}. Novo valor: R$ 12.660 (índice IGPM 5,5%)" |
| 12 | - | Dashboard atualizado com badge: "Reajuste Aplicado - IGPM 5,5%" |

### 5. Fluxos Alternativos

**FA01: Simular Reajuste Antes de Aplicar**
- Administrador acessa Contratos → Reajustes → Simular
- Seleciona contrato, índice (IGPM), período (últimos 12 meses)
- Sistema executa cálculo sem persistir
- Exibe preview: "Valor Atual: R$ 12.000 → Novo Valor: R$ 12.660 (IGPM 5,5%)"
- Administrador aprova ou cancela

**FA02: Aplicar Reajuste com Percentual Fixo**
- Contrato configurado com índice = "Percentual Fixo" e taxa = 10%
- Sistema calcula: novoValor = valorAtual × 1,10
- Não consulta API externa de índices
- Aplica diretamente

**FA03: Reverter Reajuste Aplicado Incorretamente**
- Administrador identifica reajuste errado
- Acessa Histórico de Reajustes → Seleciona reajuste
- Clica em "Reverter Reajuste"
- Sistema executa rollback: restaura ValorFaturavel anterior
- Auditoria registrada (REAJUSTE_REVERTIDO)

### 6. Exceções

**EX01: API de Índices Econômicos Indisponível**
- Se API do Banco Central falha (timeout ou HTTP 503) → Loga erro
- Sistema tenta novamente após 1 hora (retry policy)
- Notificação enviada para TI: "Falha ao consultar índice IGPM. Reajuste adiado."

**EX02: Taxa Acumulada Negativa (Deflação)**
- Se taxa acumulada < 0 (ex: -2,5%) → Sistema aplica redução
- novoValor = valorAtual × (1 - 0,025) = redução de 2,5%
- Auditoria registra deflação aplicada

**EX03: Contrato Sem Data de Aniversário Configurada**
- Se contrato não possui DataAniversario → Job pula este contrato
- Loga aviso: "Contrato #{numero} sem data de aniversário configurada. Reajuste não aplicado."

**EX04: Medições Já Faturadas**
- Se todas as medições do contrato já estão com status = Faturada → Reajuste não afeta
- Sistema cria apenas registro histórico sem atualizar valores

### 7. Pós-condições

- Reajuste aplicado em medições futuras (não faturadas)
- Histórico de reajuste criado com taxa e valores
- Auditoria registrada (REAJUSTE_APLICADO)
- Notificação enviada para gestor do contrato
- Dashboard atualizado com badge de reajuste

### 8. Regras de Negócio Aplicáveis

- **RN-MED-090-07**: Reajuste Contratual Automático por Índice Econômico (IGPM, IPCA, INPC)
- **RN-MED-090-08**: Cálculo de novo valor: valorAtual × (1 + taxaPercentual/100)
- **RN-MED-090-09**: Reajuste aplicado apenas em medições não faturadas

---

## UC03: Aprovar Medição no Workflow (Rascunho → Aprovada → Faturada)

### 1. Descrição

Este caso de uso permite que Aprovadores (Gestor, Controller) revisem medições em workflow, aprovem (transição Rascunho → PendenteAprovacao → Aprovada) ou rejeitem (retorno a Rascunho), com registro completo de auditoria e notificações.

### 2. Atores

- Medidor (cria e envia para aprovação)
- Gestor (aprova primeiro nível)
- Controller (aprova segundo nível)
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `medicao:aprovar` ou `medicao:aprovar:controller`
- Medição existe e está em status PendenteAprovacao
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Medidor acessa Medições → Seleciona medição em Rascunho | - |
| 2 | Clica em "Enviar para Aprovação" | - |
| 3 | - | Valida se medição está completa (período, valores, tipo) |
| 4 | - | Executa `PUT /api/medicoes/{id}/enviar-aprovacao` |
| 5 | - | Atualiza status: Rascunho → PendenteAprovacao |
| 6 | - | Identifica aprovador: Gestor do contrato (primeiro nível) |
| 7 | - | Cria WorkflowStep com AprovadorId, DataCriacao, Status = Pendente |
| 8 | - | Notificação SignalR enviada para gestor: "Nova medição para aprovação - Contrato #{numero}, Período {mes/ano}" |
| 9 | - | Email enviado com link direto para aprovação |
| 10 | - | Auditoria registrada (MEDICAO_ENVIADA_APROVACAO) com MedicaoId, EnviadoPor (MedidorId), AprovadorId |
| 11 | Gestor acessa Medições → Pendentes de Aprovação | - |
| 12 | - | Valida permissão `medicao:aprovar` |
| 13 | - | Aplica filtro multi-tenancy (ClienteId) |
| 14 | - | Exibe grid com medições pendentes roteadas para usuário atual |
| 15 | Seleciona medição para revisar | - |
| 16 | Clica em "Ver Detalhes" | - |
| 17 | - | Executa `GET /api/medicoes/{id}` |
| 18 | - | Exibe modal com: Dados do Contrato, Período, Tipo Medição, Valores Calculados, Rateios (se houver), Histórico de Alterações |
| 19 | Analisa valores e período | - |
| 20 | Clica em "Aprovar" | - |
| 21 | - | Executa `POST /api/medicoes/{id}/aprovar` |
| 22 | - | Atualiza status: PendenteAprovacao → Aprovada |
| 23 | - | Atualiza WorkflowStep: Status = Aprovado, DataAprovacao = DateTime.UtcNow, AprovadorId = usuarioId |
| 24 | - | Auditoria registrada (MEDICAO_APROVADA) com MedicaoId, AprovadorId, DataAprovacao |
| 25 | - | Notificação SignalR para medidor: "Medição #{id} aprovada por {gestor.Nome}" |
| 26 | - | Sistema agenda geração de fatura: Hangfire job GerarFaturaAutomaticaJob processa medições aprovadas a cada 1 hora |
| 27 | - | HTTP 200 OK retornado |
| 28 | - | Mensagem exibida: "Medição aprovada com sucesso. Fatura será gerada automaticamente." |

### 5. Fluxos Alternativos

**FA01: Rejeitar Medição (Retornar a Rascunho)**
- No passo 20, gestor clica em "Rejeitar"
- Sistema exibe campo Motivo da Rejeição (obrigatório, min 20 caracteres)
- Gestor preenche: "Valor unitário diverge do contrato. Revisar cálculo."
- Sistema executa POST /api/medicoes/{id}/rejeitar com { motivo }
- Atualiza status: PendenteAprovacao → Rascunho
- Notificação enviada para medidor com motivo
- Auditoria registrada (MEDICAO_REJEITADA)

**FA02: Aprovação Multi-Nível (Gestor + Controller)**
- Medição com valor > R$ 10.000 requer 2 níveis de aprovação
- Gestor aprova → Status = AguardandoAprovacaoController
- Sistema roteia para Controller
- Controller aprova → Status = Aprovada
- Ambas aprovações registradas em WorkflowSteps separados

**FA03: Solicitar Correção com Comentário**
- Gestor identifica erro mas não rejeita completamente
- Clica em "Solicitar Correção"
- Preenche comentário: "Revisar quantidade medida - verificar fonte de dados"
- Sistema mantém status PendenteAprovacao mas adiciona comentário
- Medidor recebe notificação, corrige e reenvia

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `medicao:aprovar` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para aprovar medições"

**EX02: Medição Já Aprovada**
- Se medição já está em status Aprovada ou Faturada → HTTP 409 Conflict
- Mensagem: "Medição já foi aprovada por {aprovador.Nome} em {data}"

**EX03: Motivo de Rejeição Muito Curto**
- Se motivo tem menos de 20 caracteres → HTTP 400 Bad Request
- Mensagem: "Motivo da rejeição deve ter no mínimo 20 caracteres"

**EX04: Medição com Valores Zerados**
- Se ValorFaturavel == 0 → Bloqueia aprovação
- Mensagem: "Medição com valor faturável zerado não pode ser aprovada. Revisar cálculo."

### 7. Pós-condições

- Medição com status atualizado (Aprovada ou Rascunho)
- WorkflowStep concluído com aprovador e timestamp
- Auditoria registrada (MEDICAO_APROVADA ou MEDICAO_REJEITADA)
- Notificações enviadas via SignalR e email
- Fatura agendada para geração automática (se aprovada)

### 8. Regras de Negócio Aplicáveis

- **RN-MED-090-06**: Workflow de Aprovação com State Machine (Rascunho → PendenteAprovacao → Aprovada → Faturada)
- **RN-MED-090-07**: Aprovação multi-nível se valor > R$ 10.000 (Gestor + Controller)
- **RN-MED-090-08**: Geração automática de fatura após aprovação via Hangfire

---

## UC04: Aplicar Rateio Proporcional Entre Filiais e Centros de Custo

### 1. Descrição

Este caso de uso permite que Administradores configurem rateio proporcional de medições entre filiais, centros de custo ou clientes com regras condicionais (volume, peso, contrato, percentual), com cálculo automático e rastreamento.

### 2. Atores

- Administrador
- Gestor de Contratos
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `medicao:rateio:config` ou `medicao:admin:full`
- Medição criada e em status Rascunho ou PendenteAprovacao
- Filiais e Centros de Custo cadastrados
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa Medições → Seleciona medição → Aba "Rateio" | - |
| 2 | - | Valida permissão `medicao:rateio:config` |
| 3 | - | Exibe formulário com: Tipo de Rateio (dropdown: Percentual, Volume, Peso, Contrato), Entidades para Rateio (tabela: Filial, Centro de Custo, % ou Valor) |
| 4 | Seleciona Tipo = Percentual | - |
| 5 | Clica em "Adicionar Linha de Rateio" | - |
| 6 | - | Exibe linha com campos: Filial (autocomplete), Centro de Custo (autocomplete), Percentual (%) |
| 7 | Preenche Linha 1: Filial SP, Centro de Custo TI, 60% | - |
| 8 | Preenche Linha 2: Filial RJ, Centro de Custo Operações, 40% | - |
| 9 | - | Valida soma de percentuais: 60% + 40% = 100% (obrigatório) |
| 10 | - | Se soma != 100% → Exibe erro: "Soma dos percentuais deve ser 100%. Atual: {soma}%" |
| 11 | Clica em "Calcular Rateio" | - |
| 12 | - | Calcula valores: ValorTotal = R$ 10.000 (da medição) |
| 13 | - | Filial SP: R$ 10.000 × 60% = R$ 6.000 |
| 14 | - | Filial RJ: R$ 10.000 × 40% = R$ 4.000 |
| 15 | - | Exibe preview: Tabela com Filial, Centro Custo, %, Valor Calculado |
| 16 | Clica em "Aplicar Rateio" | - |
| 17 | - | Executa `POST /api/medicoes/{id}/rateio` com payload: `{ tipoRateio, linhasRateio: [{ filialId, centroCustoId, percentual }] }` |
| 18 | - | Cria registros MedicaoRateio para cada linha: MedicaoId, FilialId, CentroCustoId, Percentual, ValorRateado |
| 19 | - | Auditoria registrada (MEDICAO_RATEIO_APLICADO) com MedicaoId, TipoRateio, TotalLinhas, ValorTotal |
| 20 | - | HTTP 200 OK retornado |
| 21 | - | Mensagem exibida: "Rateio aplicado com sucesso. 2 linhas criadas." |
| 22 | - | Tabela de rateio bloqueada para edição (medição deve estar em Rascunho para alterar) |

### 5. Fluxos Alternativos

**FA01: Rateio por Volume de Consumo**
- No passo 4, usuário seleciona Tipo = Volume
- Sistema exibe campo Volume Consumido por filial
- Usuário preenche: Filial SP = 6.000 m³, Filial RJ = 4.000 m³
- Sistema calcula percentual automaticamente: SP 60%, RJ 40%
- Valores rateados conforme percentual calculado

**FA02: Rateio por Contrato (Pré-Definido)**
- Contrato já possui política de rateio configurada
- Sistema aplica rateio automaticamente ao criar medição
- Usuário apenas visualiza (sem edição)
- Tabela exibe: "Rateio aplicado automaticamente conforme contrato"

**FA03: Alterar Rateio Existente (Medição em Rascunho)**
- Usuário identifica rateio incorreto
- Clica em "Editar Rateio"
- Sistema permite alteração apenas se status = Rascunho
- Se status != Rascunho → HTTP 400 "Rateio não pode ser alterado após envio para aprovação"
- Usuário altera percentuais, clica em "Salvar Alterações"
- Sistema recalcula valores e atualiza registros

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `medicao:rateio:config` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para configurar rateio de medições"

**EX02: Soma de Percentuais Diferente de 100%**
- Se soma != 100% → HTTP 400 Bad Request
- Mensagem: "Soma dos percentuais deve ser 100%. Atual: {soma}%"

**EX03: Filial ou Centro de Custo Não Encontrado**
- Se filialId ou centroCustoId inválido → HTTP 404 Not Found
- Mensagem: "Filial ou Centro de Custo não encontrado"

**EX04: Medição Já Aprovada (Rateio Bloqueado)**
- Se medição em status Aprovada ou Faturada → HTTP 400 Bad Request
- Mensagem: "Rateio não pode ser alterado após aprovação da medição"

### 7. Pós-condições

- Rateio aplicado com linhas criadas (MedicaoRateio)
- Valores calculados por filial e centro de custo
- Auditoria registrada (MEDICAO_RATEIO_APLICADO)
- Rateio bloqueado para edição se medição != Rascunho
- Fatura (quando gerada) herda rateio automaticamente

### 8. Regras de Negócio Aplicáveis

- **RN-MED-090-10**: Soma de percentuais de rateio deve ser exatamente 100%
- **RN-MED-090-11**: Rateio pode ser alterado apenas em status Rascunho
- **RN-MED-090-12**: Fatura herda rateio da medição automaticamente

---

## UC05: Analisar e Aprovar/Rejeitar Glosa (Contestação de Fatura)

### 1. Descrição

Este caso de uso permite que Clientes contestem faturas geradas (glosa) com justificativa e percentual, Gestores analisem glosas propostas, aprovem (gera nota fiscal de ajuste/crédito) ou rejeitem, com registro completo de auditoria.

### 2. Atores

- Cliente (solicita glosa)
- Gestor de Contratos (analisa glosa)
- Controller (aprova glosa)
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `glosa:create` (cliente) ou `glosa:analisar` (gestor)
- Medição em status Faturada
- Fatura gerada (RF032)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Cliente acessa Faturas → Seleciona fatura | - |
| 2 | Clica em "Contestar Fatura" | - |
| 3 | - | Valida permissão `glosa:create` |
| 4 | - | Exibe formulário: Percentual de Contestação (%), Valor Contestado (calculado), Justificativa (obrigatório, min 50 caracteres), Anexos (opcional) |
| 5 | Preenche Percentual: 10% | - |
| 6 | - | Calcula automaticamente: Valor Fatura = R$ 10.000, Valor Contestado = R$ 1.000 |
| 7 | Preenche Justificativa: "Falha na prestação de serviço nos dias 10-15/01. SLA descumprido conforme cláusula 5.2 do contrato." | - |
| 8 | Anexa evidências: PDF com logs de falha | - |
| 9 | Clica em "Enviar Contestação" | - |
| 10 | - | Executa `POST /api/glosas` com payload: `{ medicaoId, faturaId, percentualContestado, valorContestado, justificativa, anexos }` |
| 11 | - | Cria entidade Glosa com status = PendenteAnalise |
| 12 | - | Atualiza medição: Status = Glosa (bloqueada para faturamento adicional) |
| 13 | - | Auditoria registrada (GLOSA_CREATE) com ClienteId, GlosaId, MedicaoId, PercentualContestado, ValorContestado, Justificativa |
| 14 | - | Notificação enviada para gestor do contrato: "Nova glosa para análise - Fatura #{numero}, Valor contestado R$ 1.000" |
| 15 | - | HTTP 201 Created retornado |
| 16 | - | Mensagem exibida: "Contestação enviada com sucesso. Aguarde análise." |
| 17 | Gestor acessa Glosas → Pendentes de Análise | - |
| 18 | - | Valida permissão `glosa:analisar` |
| 19 | - | Exibe grid com glosas pendentes: Fatura, Cliente, Percentual, Valor, Justificativa, Data Criação, Ações |
| 20 | Seleciona glosa para analisar | - |
| 21 | Clica em "Ver Detalhes" | - |
| 22 | - | Executa `GET /api/glosas/{id}` |
| 23 | - | Exibe modal com: Dados da Fatura, Medição Original, Justificativa do Cliente, Anexos, Histórico de Comunicação |
| 24 | Analisa justificativa e evidências | - |
| 25 | Decide: Aprovar Glosa | - |
| 26 | Preenche Comentário: "Analisado. SLA realmente descumprido conforme logs. Aprovado desconto de 10%." | - |
| 27 | Clica em "Aprovar Glosa" | - |
| 28 | - | Executa `POST /api/glosas/{id}/aprovar` com { comentario } |
| 29 | - | Atualiza glosa: Status = Aprovada, DataAprovacao = DateTime.UtcNow, AprovadorId = usuarioId, Comentario |
| 30 | - | Gera Nota Fiscal de Ajuste (crédito) via RF032: Valor = -R$ 1.000 (negativo para crédito) |
| 31 | - | Vincula nota fiscal de ajuste à medição original |
| 32 | - | Auditoria registrada (GLOSA_APROVADA) com GlosaId, AprovadorId, ValorAjuste, NotaFiscalAjusteId |
| 33 | - | Notificação enviada para cliente: "Glosa aprovada. Crédito de R$ 1.000 será aplicado na próxima fatura." |
| 34 | - | HTTP 200 OK retornado |
| 35 | - | Mensagem exibida: "Glosa aprovada. Nota fiscal de ajuste gerada." |

### 5. Fluxos Alternativos

**FA01: Rejeitar Glosa (Contestação Improcedente)**
- No passo 25, gestor decide Rejeitar
- Preenche Motivo da Rejeição: "SLA foi cumprido conforme logs do sistema. Falha reportada foi pontual e dentro da janela de manutenção."
- Sistema executa POST /api/glosas/{id}/rejeitar com { motivo }
- Atualiza glosa: Status = Rejeitada
- Medição volta a status Faturada (desbloqueada)
- Notificação enviada para cliente com motivo da rejeição
- Auditoria registrada (GLOSA_REJEITADA)

**FA02: Aprovar Glosa Parcial (Percentual Menor)**
- Gestor analisa e identifica que glosa procedente é menor (5% ao invés de 10%)
- Altera Percentual Aprovado: 5% (R$ 500)
- Sistema gera nota fiscal de ajuste com valor reduzido
- Notificação para cliente: "Glosa aprovada parcialmente. Crédito de R$ 500."

**FA03: Solicitar Informações Adicionais ao Cliente**
- Gestor clica em "Solicitar Esclarecimentos"
- Preenche questionamento: "Por favor, fornecer logs detalhados da falha reportada."
- Sistema atualiza glosa: Status = AguardandoInformacoes
- Cliente recebe notificação com questionamento
- Cliente responde anexando logs adicionais
- Glosa volta a status PendenteAnalise

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `glosa:create` ou `glosa:analisar` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para criar/analisar glosas"

**EX02: Justificativa Muito Curta**
- Se justificativa tem menos de 50 caracteres → HTTP 400 Bad Request
- Mensagem: "Justificativa deve ter no mínimo 50 caracteres"

**EX03: Percentual de Contestação Inválido**
- Se percentualContestado <= 0 ou > 100 → HTTP 400 Bad Request
- Mensagem: "Percentual de contestação deve estar entre 1% e 100%"

**EX04: Medição Não Faturada**
- Se medição não está em status Faturada → HTTP 400 Bad Request
- Mensagem: "Apenas medições faturadas podem ser contestadas"

**EX05: Glosa Já Analisada**
- Se glosa já está em status Aprovada ou Rejeitada → HTTP 409 Conflict
- Mensagem: "Glosa já foi analisada por {gestor.Nome} em {data}"

### 7. Pós-condições

- Glosa criada com status PendenteAnalise ou Aprovada/Rejeitada
- Nota fiscal de ajuste gerada (se aprovada)
- Medição com status atualizado (Glosa ou Faturada)
- Auditoria registrada (GLOSA_CREATE, GLOSA_APROVADA ou GLOSA_REJEITADA)
- Notificações enviadas via SignalR e email
- Crédito aplicado em próxima fatura (se aprovada)

### 8. Regras de Negócio Aplicáveis

- **RN-MED-090-09**: Gestão de Glosa com workflow (PendenteAnalise → Aprovada/Rejeitada)
- **RN-MED-090-10**: Nota fiscal de ajuste gerada automaticamente para glosas aprovadas
- **RN-MED-090-11**: Medição bloqueada (status Glosa) enquanto glosa pendente
- **RN-MED-090-12**: Glosa pode ser aprovada parcialmente com percentual reduzido

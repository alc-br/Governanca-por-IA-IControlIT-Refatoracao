# UC-RF089 - Casos de Uso - Conciliação e Auditoria de Faturas

## UC01: Executar Matching Automático Two-Way e Three-Way com Tolerâncias

### 1. Descrição

Este caso de uso permite que o Sistema execute matching automático de Nota Fiscal Eletrônica (NF-e) com Pedido de Compra (two-way) ou com Pedido de Compra + Recebimento de Mercadorias (three-way), aplicando tolerâncias configuráveis por empresa e detectando divergências em valores, quantidades, datas e dados fiscais.

### 2. Atores

- Sistema
- Administrador (configuração de tolerâncias)

### 3. Pré-condições

- NF-e importada e validada no sistema (RF-032)
- Pedido de Compra cadastrado (PC_ID válido)
- Recebimento de Mercadorias registrado (opcional, para three-way)
- Multi-tenancy ativo (ClienteId válido)
- Hangfire job MatchingAutomaticoJob agendado ou execução manual

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire job MatchingAutomaticoJob executa diariamente às 3h AM |
| 2 | - | Consulta todas as NF-e com status = "Aguardando Matching" e ClienteId |
| 3 | - | Para cada NF-e, identifica Pedido de Compra vinculado via ChaveNFe ou FornecedorCNPJ |
| 4 | - | Valida CHAVE_NFE: verifica se tem 44 dígitos e formato válido |
| 5 | - | Valida correspondência de fornecedor: `notaFiscal.FornecedorCNPJ == pedido.FornecedorCNPJ` |
| 6 | - | Valida correspondência de cliente: `notaFiscal.ClienteId == pedido.ClienteId` |
| 7 | - | Valida duplicação de NF-e: consulta `GetByChaveNFeAsync(chaveNFe, clienteId)` |
| 8 | - | Se validações falham → Registra erro, marca NF-e como "Matching Failed", pula para próxima |
| 9 | - | Identifica tipo de matching: Se RecebimentoMercadoriaId presente → Three-way, senão → Two-way |
| 10 | - | **Two-way matching**: Compara NF-e com PC em 4 dimensões: Valores (total, subtotal, impostos, frete), Quantidades (quantidade total), Datas (data emissão vs data pedido), Dados fiscais (CFOP, alíquotas ICMS/IPI) |
| 11 | - | Aplica tolerâncias configuráveis: `ToleranciaPercentualValor` (padrão 2%), `ToleranciaQuantidade` (padrão 5 unidades), `ToleranciaDataDias` (padrão 30 dias) |
| 12 | - | Para cada dimensão, calcula diferença percentual: `percentualDif = ABS((valorNFe - valorPC) / valorPC) * 100` |
| 13 | - | Se diferença <= tolerância → Match OK, senão → Cria registro DivergenciaDetectada |
| 14 | - | **Three-way matching**: Compara adicionalmente NF-e com RecebimentoMercadorias (RM) em: Quantidades recebidas vs faturadas, Data de recebimento vs data de emissão |
| 15 | - | Classifica cada divergência: CRÍTICA (> 10% ou qty = 0 ou CFOP inválido), ALTA (5-10%), MÉDIA (2-5%), BAIXA (< 2%) |
| 16 | - | Cria WorkflowStep para divergências CRÍTICA, ALTA e MÉDIA com roteamento automático para aprovadores |
| 17 | - | Se divergência BAIXA → Auto-aprova em 24h (TipoAprovacao = Automatica) |
| 18 | - | Atualiza status da NF-e: "Matching Completo" se nenhuma divergência, "Matching Com Divergências" se houver |
| 19 | - | Auditoria registrada (MATCHING_EXEC) com ClienteId, NFeId, PedidoId, TipoMatching, TotalDivergencias, Severidade |
| 20 | - | Notificação SignalR enviada para dashboard: "X NF-e processadas, Y divergências detectadas" |

### 5. Fluxos Alternativos

**FA01: Matching Manual Disparado por Usuário**
- Administrador acessa tela de NF-e pendente
- Clica em botão "Executar Matching Agora"
- Sistema executa POST /api/faturas/matching/execute com nfeId
- Matching executado imediatamente (sem aguardar job diário)
- Resultado exibido em modal com detalhes de divergências detectadas

**FA02: Configurar Tolerâncias por Empresa**
- Administrador acessa Configurações → Matching de Faturas
- Altera ToleranciaPercentualValor de 2% para 5%
- Sistema executa PUT /api/matching/config com payload { toleranciaPercentualValor: 5.0, toleranciaQuantidade: 10, toleranciaDataDias: 45 }
- Configuração salva em MatchingConfiguration (por ClienteId)
- Próximas execuções de matching utilizam novas tolerâncias

**FA03: Re-executar Matching Após Correção de NF-e**
- NF-e foi corrigida após detecção de erro
- Sistema re-executa matching automaticamente
- Divergências antigas são marcadas como "Resolvidas Automaticamente"
- Novas divergências (se houver) são criadas

### 6. Exceções

**EX01: CHAVE_NFE Inválida**
- Se CHAVE_NFE ausente ou com menos de 44 dígitos → Matching falha
- NF-e marcada como "Matching Failed"
- Mensagem de erro: "CHAVE_NFE inválida ou ausente"

**EX02: Fornecedor Não Corresponde ao Pedido**
- Se `notaFiscal.FornecedorCNPJ != pedido.FornecedorCNPJ` → Matching falha
- Mensagem: "Fornecedor da NF-e não corresponde ao pedido"
- Divergência classificada como CRÍTICA

**EX03: NF-e Duplicada**
- Se já existe NF-e com mesma CHAVE_NFE para ClienteId → Matching falha
- Mensagem: "NF-e duplicada (ID: {existingNFe.Id})"
- Notificação enviada para administrador

**EX04: Divergência CRÍTICA Detectada**
- Se percentual diferença > 10% ou quantidade = 0 ou CFOP inválido → Divergência CRÍTICA
- Pagamento bloqueado automaticamente (RN-FIN-089-07)
- Roteamento para Diretor + Controller com SLA de 4 horas
- Notificação urgente via SignalR e email

### 7. Pós-condições

- NF-e com status atualizado (Matching Completo ou Matching Com Divergências)
- Divergências criadas e classificadas por severidade
- WorkflowSteps criados para aprovação de divergências
- Auditoria registrada (MATCHING_EXEC)
- Notificações enviadas para aprovadores via SignalR e email
- Pagamento bloqueado se divergência CRÍTICA ou ALTA

### 8. Regras de Negócio Aplicáveis

- **RN-FIN-089-01**: Validação de Integração de Nota Fiscal com Pedido de Compra
- **RN-FIN-089-02**: Classificação de Divergências por Severidade
- **RN-FIN-089-03**: Matching Two-Way e Three-Way com Tolerâncias Configuráveis
- **RN-FIN-089-07**: Bloqueio de Pagamento Automático em Divergências Críticas

---

## UC02: Detectar e Classificar Divergências Fiscais por Severidade

### 1. Descrição

Este caso de uso permite que o Sistema detecte automaticamente divergências em valores, quantidades, datas e dados fiscais durante processo de matching, classifique-as em CRÍTICA, ALTA, MÉDIA ou BAIXA conforme impacto financeiro e quantidade, e crie workflow de aprovação diferenciado por severidade.

### 2. Atores

- Sistema
- Machine Learning Service (detecção de anomalias)

### 3. Pré-condições

- Matching executado (UC01)
- NF-e, Pedido de Compra e Recebimento validados
- Multi-tenancy ativo (ClienteId válido)
- DivergenciaClassifier configurado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Durante matching, identifica diferença em valor, quantidade ou data |
| 2 | - | Cria entidade DivergenciaDetectada com: NFeId, PedidoId, TipoDivergencia (Valor, Quantidade, Data, CFOP), ValorEsperado, ValorRealizado, DiferencaAbsoluta, DiferencaPercentual |
| 3 | - | Calcula diferença percentual: `percentualDif = ABS((valorRealizado - valorEsperado) / valorEsperado) * 100` |
| 4 | - | Classifica severidade usando DivergenciaClassifier |
| 5 | - | **Se percentualDif > 10% OU quantidadeRealizada == 0 OU CFOP inválido** → Severidade = CRÍTICA |
| 6 | - | **Se percentualDif 5-10% OU descontoNãoContratado > 5%** → Severidade = ALTA |
| 7 | - | **Se percentualDif 2-5% OU dataDiferença 30-60 dias** → Severidade = MÉDIA |
| 8 | - | **Se percentualDif < 2% OU dataDiferença < 30 dias** → Severidade = BAIXA |
| 9 | - | Salva Divergencia com severidade classificada |
| 10 | - | Se severidade >= MÉDIA → Consulta AnomalyDetectionService (Azure ML) |
| 11 | - | Azure ML analisa padrões históricos e retorna score de anomalia (0-100) |
| 12 | - | Se score > 80 → Marca divergência como "Suspeita de Fraude", escala severidade para CRÍTICA |
| 13 | - | Cria WorkflowStep conforme severidade: CRÍTICA → Diretor + Controller (SLA 4h), ALTA → Manager + Supervisor (SLA 24h), MÉDIA → Supervisor (SLA 72h), BAIXA → Auto-aprovação em 24h |
| 14 | - | Consulta usuários aprovadores por perfil: `GetUsuariosByPerfilAsync(perfilAprovador, clienteId)` |
| 15 | - | Envia notificação para aprovadores via SignalR: `hubContext.Clients.User(usuarioId).SendAsync("DivergenciaRoteada", divergencia)` |
| 16 | - | Envia notificação por email com detalhes: Tipo, Severidade, Valor Esperado vs Realizado, Link para aprovação |
| 17 | - | Auditoria registrada (DIVERGENCIA_DETECTED) com ClienteId, DivergenciaId, TipoDivergencia, Severidade, Score ML |
| 18 | - | Dashboard atualizado em real-time com badge de severidade (vermelho=CRÍTICA, laranja=ALTA, amarelo=MÉDIA, verde=BAIXA) |

### 5. Fluxos Alternativos

**FA01: Detecção de Anomalia por Machine Learning**
- AnomalyDetectionService identifica padrão suspeito (ex: valor 3x acima do desvio padrão para fornecedor)
- Score ML > 80 → Divergência marcada como "Suspeita de Fraude"
- Email urgente enviado para Compliance + Diretor Financeiro
- Pagamento bloqueado mesmo se severidade original era BAIXA/MÉDIA

**FA02: Divergência em Dados Fiscais (CFOP Inválido)**
- Sistema detecta CFOP não cadastrado em tabela oficial SPED
- Classifica automaticamente como CRÍTICA
- Bloqueia NF-e para processamento contábil
- Notificação para Contador revisar classificação fiscal

**FA03: Divergência em Quantidade Zero Recebida**
- Matching identifica quantidadeRecebida = 0 mas NF-e faturou quantidade > 0
- Classifica como CRÍTICA (possível erro de lançamento de recebimento)
- Workflow escala para Gerente de Logística + Compras
- Requer revisão de Recebimento de Mercadorias antes de aprovar NF-e

### 6. Exceções

**EX01: Valor Esperado Zero (Impossibilita Cálculo Percentual)**
- Se valorEsperado == 0 → Calcula apenas diferença absoluta
- Classifica como MÉDIA se diferença absoluta < R$ 100,00
- Classifica como ALTA se diferença >= R$ 100,00

**EX02: Azure ML Service Indisponível**
- Se chamada a AnomalyDetectionService falha (timeout ou HTTP 503) → Loga warning
- Continua processamento sem score ML
- Classifica apenas por regras percentuais
- Marca divergência com flag "MLNotAnalyzed"

**EX03: Nenhum Aprovador Disponível para Perfil**
- Se consulta `GetUsuariosByPerfilAsync` retorna lista vazia → Escala para Diretor Geral
- Loga alerta "Nenhum aprovador encontrado para perfil {perfil}"
- Envia email para TI solicitando configuração de aprovadores

**EX04: Severidade CRÍTICA com SLA Expirado**
- Se divergência CRÍTICA não aprovada em 4 horas → Escala automaticamente para Diretor Geral
- Notificação SMS enviada (urgência máxima)
- Dashboard exibe alerta vermelho piscante

### 7. Pós-condições

- Divergência criada e classificada por severidade
- WorkflowStep criado com SLA diferenciado
- Aprovadores notificados via SignalR e email
- Auditoria registrada (DIVERGENCIA_DETECTED)
- Score ML registrado (se disponível)
- Pagamento bloqueado se severidade >= ALTA

### 8. Regras de Negócio Aplicáveis

- **RN-FIN-089-02**: Classificação de Divergências por Severidade
- **RN-FIN-089-04**: Detecção de Anomalias por Machine Learning
- **RN-FIN-089-06**: Workflow de Aprovação com Roteamento por Severidade
- **RN-FIN-089-07**: Bloqueio de Pagamento Automático em Divergências Críticas

---

## UC03: Aprovar ou Rejeitar Divergência com Justificativa e Auditoria

### 1. Descrição

Este caso de uso permite que Aprovadores (Supervisor, Manager, Controller, Diretor) revisem divergências detectadas, aprovem com justificativa (liberando pagamento) ou rejeitem (bloqueando NF-e), com registro completo de auditoria e notificações em real-time.

### 2. Atores

- Supervisor
- Manager
- Controller
- Diretor
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `divergencia:aprovar` ou `divergencia:aprovar:critica` (para CRÍTICA)
- Divergência existe e está pendente (status = Pendente)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Conciliação → Divergências Pendentes | - |
| 2 | - | Valida permissão `divergencia:aprovar` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Exibe grid paginado com divergências roteadas para usuário atual |
| 5 | - | Colunas: Severidade (badge colorido), NF-e (número), Fornecedor, Tipo Divergência, Valor Esperado, Valor Realizado, Diferença (%), SLA Restante (countdown), Ações |
| 6 | Seleciona divergência para revisar | - |
| 7 | Clica em "Ver Detalhes" | - |
| 8 | - | Executa `GET /api/divergencias/{id}` |
| 9 | - | Retorna: DivergenciaDto com NFeId, PedidoId, RecebimentoId, TipoDivergencia, Severidade, ValorEsperado, ValorRealizado, DiferencaPercentual, Descricao, ScoreML, ChaveNFe, NomeFornecedor |
| 10 | - | Exibe modal com 3 abas: Detalhes Divergência, Histórico Matching, Documentos Relacionados (PDF da NF-e, PDF do Pedido) |
| 11 | Analisa divergência, valida documentos | - |
| 12 | Decide: Aprovar ou Rejeitar | - |
| 13 | Se Aprovar: Clica em "Aprovar", preenche campo Justificativa (obrigatório, min 20 caracteres) | - |
| 14 | - | Valida se usuário tem permissão para severidade (CRÍTICA requer `divergencia:aprovar:critica`) |
| 15 | - | Executa `POST /api/divergencias/{id}/aprovar` com payload: { justificativa, aprovadorId } |
| 16 | - | Atualiza divergência: Status = Aprovada, DataAprovacao = DateTime.UtcNow, AprovadorId = usuarioId, Justificativa |
| 17 | - | Atualiza WorkflowStep: Status = Aprovado, DataAcao = DateTime.UtcNow, UsuarioAcao = usuarioId |
| 18 | - | Se NF-e não tem outras divergências pendentes → Libera pagamento: `notaFiscal.LiberarPagamento()` |
| 19 | - | Auditoria registrada (DIVERGENCIA_APPROVED) com ClienteId, DivergenciaId, AprovadorId, Justificativa |
| 20 | - | Notificação SignalR enviada para solicitante original: "Divergência #{id} aprovada por {aprovador.Nome}" |
| 21 | - | HTTP 200 OK retornado |
| 22 | - | Mensagem exibida: "Divergência aprovada com sucesso. Pagamento liberado." |
| 23 | Se Rejeitar: Clica em "Rejeitar", preenche Motivo da Rejeição (obrigatório) | - |
| 24 | - | Executa `POST /api/divergencias/{id}/rejeitar` com payload: { motivo, rejeitadorId } |
| 25 | - | Atualiza divergência: Status = Rejeitada, DataRejeicao = DateTime.UtcNow, RejeitadorId = usuarioId, MotivoRejeicao |
| 26 | - | Bloqueia NF-e definitivamente: `notaFiscal.BloquearDefinitivamente()` |
| 27 | - | Auditoria registrada (DIVERGENCIA_REJECTED) com ClienteId, DivergenciaId, RejeitadorId, MotivoRejeicao |
| 28 | - | Notificação enviada para Compras: "NF-e #{chaveNFe} bloqueada. Motivo: {motivo}" |
| 29 | - | HTTP 200 OK retornado |
| 30 | - | Mensagem exibida: "Divergência rejeitada. NF-e bloqueada para pagamento." |

### 5. Fluxos Alternativos

**FA01: Delegar Divergência para Outro Aprovador**
- Aprovador identifica que não tem contexto suficiente
- Clica em "Delegar"
- Seleciona usuário de nível superior (ex: Manager delega para Diretor)
- Sistema atualiza WorkflowStep com novo aprovador
- Notificação enviada para novo aprovador

**FA02: Solicitar Informações Adicionais ao Fornecedor**
- Aprovador clica em "Solicitar Esclarecimentos"
- Preenche questionamento em campo texto
- Sistema envia email para fornecedor via endereço cadastrado
- Divergência marcada como "Aguardando Fornecedor"
- SLA pausado até resposta

**FA03: Aprovar em Lote (Múltiplas Divergências)**
- Aprovador seleciona múltiplas divergências BAIXAS usando checkbox
- Clica em "Aprovar Selecionadas"
- Sistema executa `POST /api/divergencias/batch-aprovar` com array de IDs + justificativa única
- Todas aprovadas simultaneamente
- Auditoria individual registrada para cada

### 6. Exceções

**EX01: Permissão Negada (Severidade CRÍTICA)**
- Se usuário tenta aprovar divergência CRÍTICA sem permissão `divergencia:aprovar:critica` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para aprovar divergências críticas. Contacte um Diretor ou Controller."

**EX02: Justificativa Muito Curta**
- Se justificativa tem menos de 20 caracteres → HTTP 400 Bad Request
- Mensagem: "Justificativa deve ter no mínimo 20 caracteres"

**EX03: Divergência Já Aprovada/Rejeitada**
- Se divergência já foi processada por outro usuário → HTTP 409 Conflict
- Mensagem: "Esta divergência já foi {aprovada/rejeitada} por {usuario.Nome} em {data}"

**EX04: SLA Expirado**
- Se SLA expirou (DataSLA < DateTime.UtcNow) → Badge vermelho exibido "SLA Expirado"
- Notificação enviada para superior hierárquico automaticamente
- Aprovação ainda permitida, mas registrada como "Fora do SLA"

### 7. Pós-condições

- Divergência com status atualizado (Aprovada ou Rejeitada)
- Justificativa ou Motivo registrado
- Auditoria completa registrada (DIVERGENCIA_APPROVED ou DIVERGENCIA_REJECTED)
- Pagamento liberado (se aprovada) ou bloqueado (se rejeitada)
- Notificações enviadas via SignalR e email
- WorkflowStep concluído

### 8. Regras de Negócio Aplicáveis

- **RN-FIN-089-05**: Justificativa obrigatória em aprovações de divergências >= MÉDIA
- **RN-FIN-089-06**: Workflow de Aprovação com Roteamento por Severidade
- **RN-FIN-089-07**: Bloqueio/Liberação de Pagamento conforme status da divergência
- **RN-FIN-089-08**: Auditoria completa com event sourcing

---

## UC04: Executar Conciliação Bancária de Faturas com Extratos

### 1. Descrição

Este caso de uso permite que o Sistema vincule automaticamente faturas (NF-e) com seus respectivos pagamentos registrados em extratos bancários (OFX), identificando atrasos, adiantamentos, discrepâncias de valor e gerando relatório de conciliação.

### 2. Atores

- Sistema
- Administrador (configuração de contas bancárias)

### 3. Pré-condições

- Extratos bancários importados (formato OFX ou CSV)
- Faturas com status "Pagamento Liberado"
- Contas bancárias configuradas com ClienteId
- Multi-tenancy ativo
- Hangfire job ConciliacaoBancariaJob agendado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire job ConciliacaoBancariaJob executa diariamente às 6h AM |
| 2 | - | Consulta extratos bancários não conciliados: `WHERE StatusConciliacao = "Pendente" AND ClienteId = {clienteId}` |
| 3 | - | Para cada transação de débito no extrato, identifica possíveis faturas candidatas |
| 4 | - | Critérios de matching: Valor da transação ~= Valor da fatura (tolerância 2%), Data pagamento entre Data Vencimento -5 dias e +30 dias, CNPJ beneficiário = CNPJ fornecedor (se disponível) |
| 5 | - | Executa fuzzy matching: calcula score de similaridade (0-100) |
| 6 | - | Se score >= 95 → Match automático |
| 7 | - | Se score 80-94 → Match sugerido (requer confirmação manual) |
| 8 | - | Se score < 80 → Sem match, marca transação como "Não Conciliada" |
| 9 | - | Para match automático: Cria vinculação `ConciliacaoBancaria` com FaturaId, TransacaoId, DataConciliacao, Tipo = "Automática" |
| 10 | - | Atualiza fatura: Status = "Paga", DataPagamento = transacao.DataPagamento |
| 11 | - | Calcula diferenças: DiferencaDias = (dataPagamento - dataVencimento), DiferencaValor = (valorPago - valorFatura) |
| 12 | - | Se DiferencaDias > 0 → Marca como "Pago com Atraso", calcula multa/juros conforme contrato |
| 13 | - | Se DiferencaDias < 0 → Marca como "Pago Antecipado", verifica se desconto foi aplicado corretamente |
| 14 | - | Se DiferencaValor != 0 → Cria divergência de conciliação: `DivergenciaConciliacao` com Tipo = "Valor Diferente", DiferencaAbsoluta, Severidade (ALTA se > 5%, MÉDIA se 2-5%, BAIXA se < 2%) |
| 15 | - | Auditoria registrada (CONCILIACAO_BANCARIA_EXEC) com ClienteId, TotalFaturasConciliadas, TotalPendentes, DiferencasDetectadas |
| 16 | - | Gera relatório de conciliação: `RelatorioConciliacao` com: Total Conciliado, Total Pendente, Divergências, Atrasos, Adiantamentos |
| 17 | - | Notificação enviada para Controller: "Conciliação bancária concluída. X faturas conciliadas, Y pendentes, Z divergências" |

### 5. Fluxos Alternativos

**FA01: Conciliação Manual de Transação Não Matcheada**
- Administrador acessa Conciliação Bancária → Transações Pendentes
- Seleciona transação e fatura manualmente
- Clica em "Vincular Manualmente"
- Sistema cria vinculação com Tipo = "Manual", registra usuário responsável

**FA02: Importar Extrato OFX de Conta Bancária**
- Administrador acessa Contas Bancárias → Importar Extrato
- Faz upload de arquivo OFX
- Sistema parseia OFX, extrai transações
- Cria registros TransacaoBancaria com StatusConciliacao = "Pendente"
- Executa conciliação automática imediatamente

**FA03: Desfazer Conciliação Incorreta**
- Administrador identifica conciliação errada
- Clica em "Desfazer Conciliação"
- Sistema remove vinculação, reverte status da fatura para "Aguardando Pagamento"
- Auditoria registrada (CONCILIACAO_UNDONE)

### 6. Exceções

**EX01: Extrato OFX Inválido**
- Se parsing de OFX falha → HTTP 400 Bad Request
- Mensagem: "Arquivo OFX inválido ou corrompido. Verifique formato."

**EX02: Múltiplas Faturas Candidatas para Mesma Transação**
- Se score >= 95 para mais de 1 fatura → Sistema marca como "Match Ambíguo"
- Notificação para Controller revisar manualmente
- Transação permanece "Pendente"

**EX03: Valor Pago Muito Diferente (> 10%)**
- Se DiferencaValor > 10% → Cria divergência CRÍTICA
- Bloqueia conciliação automática
- Requer aprovação de Diretor para vincular manualmente

**EX04: Banco Não Configurado**
- Se conta bancária não cadastrada → Loga erro
- Mensagem: "Conta bancária {numero} não configurada. Configure antes de importar extrato."

### 7. Pós-condições

- Faturas vinculadas a transações bancárias
- Status atualizado: "Paga" com DataPagamento
- Divergências de conciliação criadas e classificadas
- Relatório de conciliação gerado
- Auditoria registrada (CONCILIACAO_BANCARIA_EXEC)
- Notificações enviadas para Controller

### 8. Regras de Negócio Aplicáveis

- **RN-FIN-089-09**: Fuzzy matching com score >= 95 para conciliação automática
- **RN-FIN-089-10**: Tolerância de 2% em valor e +/- 30 dias em data
- **RN-FIN-089-11**: Cálculo automático de multa/juros para pagamentos em atraso
- **RN-FIN-089-12**: Auditoria completa de conciliações e desfazimentos

---

## UC05: Monitorar Dashboard de Divergências em Tempo Real via SignalR

### 1. Descrição

Este caso de uso permite que Administradores e Gestores monitorem divergências de faturas em tempo real através de dashboard interativo com KPIs, gráficos, filtros dinâmicos, drilldown e notificações push via SignalR.

### 2. Atores

- Administrador
- Gestor de TI
- Controller
- Diretor
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `divergencia:dashboard:read` ou `divergencia:admin:full`
- Multi-tenancy ativo (ClienteId válido)
- SignalR Hub configurado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Conciliação → Dashboard de Divergências | - |
| 2 | - | Valida permissão `divergencia:dashboard:read` |
| 3 | - | Aplica filtro multi-tenancy (ClienteId) |
| 4 | - | Estabelece conexão SignalR: `hubConnection.start()` |
| 5 | - | Exibe dashboard com 4 seções: KPIs (cards), Gráficos, Tabela Detalhada, Alertas |
| 6 | - | **Seção KPIs**: Total Divergências (contador), Críticas Pendentes (badge vermelho), SLA Expirado (alerta piscante), Taxa Resolução 30 Dias (gauge) |
| 7 | - | Executa `GET /api/divergencias/kpis` com ClienteId |
| 8 | - | Retorna: `{ totalDivergencias, criticasPendentes, slaExpirado, taxaResolucao, tempoMedioResolucao }` |
| 9 | - | **Seção Gráficos**: Divergências por Severidade (donut chart), Divergências por Tipo (bar chart), Tendência Últimos 30 Dias (line chart), Top 5 Fornecedores com Divergências (horizontal bar) |
| 10 | - | Executa `GET /api/divergencias/charts` |
| 11 | - | Renderiza gráficos usando Chart.js ou Highcharts |
| 12 | - | **Seção Tabela**: Lista paginada (pageSize = 20) com: Severidade, NF-e, Fornecedor, Tipo, Valor Esperado, Valor Realizado, Diferença (%), SLA Restante (countdown), Status, Ações |
| 13 | - | Filtros disponíveis: Severidade (dropdown), Status (Pendente/Aprovada/Rejeitada), Período (date range picker), Fornecedor (autocomplete) |
| 14 | Usuário aplica filtro: Severidade = CRÍTICA | - |
| 15 | - | Executa `GET /api/divergencias?severidade=Critica&status=Pendente&clienteId={clienteId}` |
| 16 | - | Tabela atualizada com divergências CRÍTICAS pendentes apenas |
| 17 | - | SignalR recebe evento "DivergenciaDetectada" em tempo real |
| 18 | - | Dashboard atualiza KPIs automaticamente: Total Divergências incrementa +1 |
| 19 | - | Badge vermelho pisca: "Nova divergência CRÍTICA detectada" |
| 20 | - | Toast notification exibido: "Divergência CRÍTICA - NF-e #{chaveNFe} - {descricao}" |
| 21 | Usuário clica em linha da tabela para drilldown | - |
| 22 | - | Executa `GET /api/divergencias/{id}` |
| 23 | - | Modal exibido com: Detalhes Completos, Histórico de Workflow, Documentos Anexos (PDF da NF-e), Botões (Aprovar, Rejeitar, Delegar) |
| 24 | - | Atualização em real-time: Outro usuário aprovou divergência |
| 25 | - | SignalR recebe evento "DivergenciaAprovada" |
| 26 | - | Linha da tabela desaparece automaticamente (filtro = Pendente) |
| 27 | - | KPIs atualizados: Total Divergências decrementa -1, Taxa Resolução recalculada |
| 28 | - | Toast notification: "Divergência #{id} aprovada por {aprovador.Nome}" |

### 5. Fluxos Alternativos

**FA01: Exportar Dashboard para PDF**
- Usuário clica em "Exportar Dashboard"
- Sistema executa `GET /api/divergencias/export?format=pdf`
- Gera PDF com snapshot dos KPIs + gráficos + tabela detalhada
- Download iniciado automaticamente
- Auditoria registrada (DASHBOARD_EXPORTED)

**FA02: Configurar Alertas Personalizados**
- Usuário acessa Configurações → Alertas de Divergências
- Define regra: "Notificar via email se Divergência CRÍTICA não aprovada em 2 horas"
- Sistema cria AlertRule com trigger baseado em SLA
- SignalR envia notificação quando condição atendida

**FA03: Drilldown em Fornecedor Específico**
- Usuário clica em barra do fornecedor "Fornecedor X" no gráfico Top 5
- Dashboard aplica filtro automático: Fornecedor = "Fornecedor X"
- Tabela e outros gráficos atualizados para mostrar apenas divergências deste fornecedor
- Breadcrumb exibido: "Dashboard > Fornecedor X"

### 6. Exceções

**EX01: Permissão Negada**
- Se usuário sem permissão `divergencia:dashboard:read` → HTTP 403 Forbidden
- Mensagem: "Você não tem permissão para acessar o dashboard de divergências"

**EX02: SignalR Desconectado**
- Se conexão SignalR cai → Dashboard exibe banner amarelo: "Conexão perdida. Dados podem estar desatualizados. Reconectando..."
- Sistema tenta reconectar automaticamente a cada 5 segundos
- Se reconexão bem-sucedida → Recarrega KPIs e tabela

**EX03: Nenhuma Divergência Encontrada**
- Se filtros não retornam resultados → HTTP 200 OK com array vazio
- Mensagem exibida: "Nenhuma divergência encontrada com os filtros selecionados"

**EX04: Erro ao Carregar Gráficos**
- Se Chart.js falha ao renderizar → Exibe placeholder: "Erro ao carregar gráfico. Tente novamente."
- Botão "Recarregar Gráficos" disponível

### 7. Pós-condições

- Dashboard exibindo KPIs, gráficos e tabela em tempo real
- Filtros aplicados corretamente
- SignalR conectado e recebendo eventos
- Notificações push funcionando
- Auditoria registrada (DASHBOARD_ACCESSED)

### 8. Regras de Negócio Aplicáveis

- **RN-FIN-089-13**: Dashboard atualizado em real-time via SignalR
- **RN-FIN-089-14**: Filtros aplicados com multi-tenancy (ClienteId)
- **RN-FIN-089-15**: KPIs calculados com agregações no banco (performance)
- **RN-FIN-089-16**: Exportação de dashboard com snapshot de dados

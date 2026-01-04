# UC-RF097 - Casos de Uso - Auditoria de Faturas

## UC01: Auditar NF-e com Validações Fiscais Completas e Consulta SEFAZ

### 1. Descrição

Este caso de uso permite que o Auditor ou CFO inicie uma auditoria completa de uma NF-e, executando validações fiscais automáticas (chave de acesso, assinatura digital, alíquotas, base de cálculo, duplicatas) e consultando o status no SEFAZ para garantir conformidade fiscal.

### 2. Atores

- Auditor (principal)
- CFO
- Sistema (validações automáticas)
- SEFAZ API (consulta externa)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `fin:auditoria:create` ou `fin:auditoria:sefaz`
- Multi-tenancy ativo (ClienteId válido)
- NF-e já importada no sistema (RF032)
- Certificado digital configurado para consulta SEFAZ

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /financeiro/auditoria-faturas | - |
| 2 | Seleciona NF-e por chave de acesso ou filtros (CNPJ, data, número) | - |
| 3 | - | Exibe dados da NF-e: ChaveAcesso, NumeroNota, DataEmissao, CnpjEmitente, ValorTotal, CFOP, StatusSEFAZ |
| 4 | Clica em "Auditar NF-e" | - |
| 5 | - | Valida permissão RBAC (fin:auditoria:create) |
| 6 | - | Cria registro AuditoriaFatura: `{ ChaveAcesso, ClienteId, DataInicio = UtcNow, Status = EmProcessamento, UsuarioAuditoria = currentUserId }` |
| 7 | - | **Validação 1: Formato da Chave de Acesso** - Executa ValidarChaveAcessoNFe: verifica 44 dígitos, dígito verificador (módulo 11), UF válido (substring 0-2) |
| 8 | - | Se chave inválida → Registra erro: `{ TipoValidacao = "ChaveAcesso", Status = Falha, Mensagem = "Chave inválida" }`, incrementa ValidacoesFalhadas |
| 9 | - | Se chave válida → Incrementa ValidacoesExecutadas |
| 10 | - | **Validação 2: Assinatura Digital XML** - Executa ValidarAssinaturaXmlCommand: carrega XML da NF-e, extrai nó `<Signature>`, valida com SignedXml.CheckSignature() |
| 11 | - | Extrai certificado digital X509: valida NotBefore <= DataEmissao <= NotAfter (certificado em vigência na data da emissão) |
| 12 | - | Se assinatura inválida ou certificado expirado → Gera AlertaAuditoria: `{ TipoAlerta = AssinaturaInvalida, Severidade = Critico, Descricao = "XML foi alterado ou certificado expirado" }` |
| 13 | - | Se assinatura válida → Incrementa ValidacoesExecutadas, registra em AssinaturaDigitalAuditoria: `{ ChaveAcesso, ValorAssinatura = true, DataValidacao = UtcNow, CertificadoCNPJ = cert.Subject }` |
| 14 | - | **Validação 3: Consulta SEFAZ** - Enfileira job Hangfire ConsultarStatusSEFAZJob: `{ ChaveAcesso, CnpjEmitente, ClienteId }` com retry exponencial (3 tentativas, delay 5s → 30s → 120s) |
| 15 | - | Job executa: POST https://nfe.sefaz.{UF}.gov.br/ws/nfestatusservico4 com payload XML contendo ChaveAcesso e certificado digital |
| 16 | - | SEFAZ retorna status: 100 (Autorizado), 101 (Cancelado), 102 (Denegado), 103 (Pendente) + Protocolo de Autorização + Mensagem |
| 17 | - | Se StatusSEFAZ != "100" → Gera AlertaAuditoria: `{ TipoAlerta = NfeNaoAutorizada, Severidade = Critico, Descricao = "Status SEFAZ: {status} - {mensagem}" }` |
| 18 | - | Atualiza NotaFiscal: `{ StatusSEFAZ = resultado, DataConsultaSEFAZ = UtcNow, ProtocoloAutorizacao = protocolo, MensagemSEFAZ = mensagem }` |
| 19 | - | **Validação 4: Alíquota ICMS conforme CFOP** - Executa ValidarAliquotaICMSCommand: consulta tabela TabelaAliquotas WHERE CFOP = {nfe.CFOP} AND RegimeApuracao = {empresa.RegimeApuracao} AND DataVigencia <= {nfe.DataEmissao} |
| 20 | - | Compara AliquotaICMS da NF-e com alíquotas válidas (tolerância 0.01%): se diferença > 0.01m → Gera AlertaAuditoria: `{ TipoAlerta = AliquotaInconsistente, Severidade = Aviso, Descricao = "Alíquota {valor}% não consta na tabela para CFOP {cfop}" }` |
| 21 | - | **Validação 5: Base de Cálculo e Impostos** - Calcula baseCalculada = ValorTotal - Desconto + Frete + Seguro + OutrosGastos |
| 22 | - | Calcula icmsEsperado = baseCalculada × AliquotaICMS, compara com ValorICMS da NF-e (tolerância R$ 0.01) |
| 23 | - | Se diferença > R$ 0.01 → Gera AlertaAuditoria: `{ TipoAlerta = BaseCalculoInconsistente, Severidade = Aviso, Descricao = "ICMS esperado {esperado}, informado {informado}" }` |
| 24 | - | **Validação 6: Duplicatas** - Busca NF-e com mesma ChaveAcesso: `SELECT * FROM NotaFiscal WHERE ChaveAcesso = @chave AND ClienteId = @clienteId AND DataCancelamento IS NULL` |
| 25 | - | Se encontrar outra NF-e ativa → Gera AlertaAuditoria: `{ TipoAlerta = DuplicataDetectada, Severidade = Critico, Descricao = "Chave {chave} já existe ativa em {data}" }`, interrompe auditoria |
| 26 | - | Busca NF-e do mesmo fornecedor + produto em últimos 7 dias: se count >= 2 → Gera AlertaAuditoria: `{ TipoAlerta = SuspeitaDuplicata, Severidade = Aviso }` |
| 27 | - | **Validação 7: Conformidade SPED Fiscal** - Valida registros obrigatórios: CnpjEmitente (0150), NumeroNota + ChaveAcesso (1100), CFOP (1120), ValorICMS vs AliquotaICMS (1160) |
| 28 | - | Se algum campo obrigatório ausente ou inconsistente → Gera AlertaAuditoria: `{ TipoAlerta = ErroSPED, Severidade = Aviso, Descricao = "Falta {campo} (registro {codigo})" }` |
| 29 | - | **Validação 8: Retenções Obrigatórias** - Se CFOP.StartsWith("6") E TipoPrestador = "PJ" E ValorServico > 0 → Calcula IRRF esperado (15%), ISS conforme município |
| 30 | - | Se retenção informada difere da esperada (tolerância R$ 0.01) → Gera AlertaAuditoria: `{ TipoAlerta = RetencaoIncorreta, Severidade = Aviso }` |
| 31 | - | Atualiza AuditoriaFatura: `{ Status = Concluida, DataConclusao = UtcNow, ValidacoesExecutadas = 8, ValidacoesFalhadas = count(erros), Alertas = count(alertas) }` |
| 32 | - | Exibe resultado em tela: "Auditoria Concluída - {validacoesFalhadas} falhas, {alertas} alertas gerados" |
| 33 | Usuário visualiza lista de alertas com botões para resolver | - |

### 5. Fluxos Alternativos

**FA01: Consulta SEFAZ com Timeout**
- Passo 15: Se SEFAZ não responder em 120s → Job executa retry exponencial (tentativa 1: 5s, tentativa 2: 30s, tentativa 3: 120s)
- Se após 3 tentativas ainda houver timeout → Atualiza AuditoriaFatura: `{ AuditoriaStatus = ErroSEFAZ, MensagemErro = "Timeout ao consultar SEFAZ" }`
- Reagenda job para 1h depois: `jobQueue.EnqueueAsync(new ConsultarStatusSEFAZJob { ChaveAcesso }, delaySeconds: 3600)`
- Exibe mensagem ao usuário: "Consulta SEFAZ falhará, reagendada para 1h"

**FA02: NF-e Cancelada com Movimentação Posterior**
- Passo 17: Se StatusSEFAZ = "101" (Cancelado) → Executa ValidarMovimentacaoPosCanelamentoCommand
- Busca lançamentos contábeis (RF089) com DataLancamento > DataCancelamento
- Se encontrar lançamentos → Gera AlertaAuditoria: `{ TipoAlerta = InconsistenciaCancelamento, Severidade = Critico, Descricao = "NF-e cancelada mas há {count} lançamentos posteriores" }`
- Notifica CFO via email e SignalR

**FA03: Detecção de Anomalia via Machine Learning**
- Após todas validações determinísticas (passos 7-30): Executa DetectarAnomaliaCommand
- Coleta histórico de 2 anos: `nfeRepository.ObterHistoricoAsync(cnpj, produto, dataInicio: -2 anos, clienteId)`
- Calcula features: ValorMedio, DesviosPadrao, Frequencia (ops/mês), HorarioMedio, FornecedorNovo (count < 3)
- Envia para Azure ML: `azureML.PredizirRiscoFraudeAsync(features)` → retorna Score (0-1.0)
- Se Score > 0.7 → Gera AlertaAuditoria: `{ TipoAlerta = AnomaliaDetectada, Severidade = Critico, Descricao = "Anomalia detectada (score: {score}). Desvio: {percentual}% acima da média" }`

### 6. Exceções

**EX01: Usuário sem permissão para auditar**
- Passo 5: Se usuário não tem permissão `fin:auditoria:create` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para auditar faturas"

**EX02: Chave de acesso já auditada recentemente**
- Passo 6: Se já existe AuditoriaFatura com ChaveAcesso e DataInicio > UtcNow.AddHours(-1) → Retorna HTTP 400 Bad Request
- Exibe mensagem: "NF-e foi auditada há menos de 1h, aguarde para nova auditoria"

**EX03: NF-e não encontrada no sistema**
- Passo 3: Se ChaveAcesso não existe em NotaFiscal → Retorna HTTP 404 Not Found
- Exibe mensagem: "NF-e {chaveAcesso} não encontrada. Importe a NF-e primeiro (RF032)"

**EX04: Certificado digital não configurado**
- Passo 14: Se empresa não tem certificado digital válido → Lança CertificadoDigitalException
- Gera AlertaAuditoria: `{ TipoAlerta = ErroConfiguracao, Severidade = Critico, Descricao = "Certificado digital ausente ou expirado" }`
- Exibe mensagem: "Configure o certificado digital em Parâmetros do Sistema (RF001)"

**EX05: XML da NF-e ausente**
- Passo 10: Se NotaFiscal.XmlContent IS NULL → Lança XmlAusenteException
- Gera AlertaAuditoria: `{ TipoAlerta = ErroValidacao, Severidade = Critico, Descricao = "XML da NF-e não está armazenado" }`
- Interrompe auditoria, marca Status = Erro

### 7. Pós-condições

- Registro criado em AuditoriaFatura com Status = Concluida ou ErroSEFAZ
- 8 validações executadas (ou menos se houver erro bloqueante)
- 0 ou mais AlertaAuditoria criados conforme inconsistências encontradas
- NotaFiscal atualizada com StatusSEFAZ, ProtocoloAutorizacao, DataConsultaSEFAZ
- Se Score ML > 0.7: Notificação enviada ao CFO (SignalR + email)
- Operação registrada em auditoria (RF004): `{ UsuarioId, ChaveAcesso, DataHora, ValidacoesExecutadas, AlertasGerados }`

### 8. Regras de Negócio Aplicáveis

- RN-AUF-097-01: Validação Obrigatória de Chave de Acesso NF-e (44 dígitos, módulo 11)
- RN-AUF-097-02: Consulta Obrigatória de Status SEFAZ em 24h (retry exponencial)
- RN-AUF-097-03: Validação de Alíquota ICMS Conforme CFOP e regime de apuração
- RN-AUF-097-04: Detecção de NF-e Cancelada com Movimentação Posterior (alerta crítico)
- RN-AUF-097-05: Validação de Integridade de Assinatura Digital (X509Certificate2, SignedXml)
- RN-AUF-097-06: Validação de Base de Cálculo e Impostos (tolerância R$ 0.01)
- RN-AUF-097-07: Detecção de Duplicatas (mesma chave ou fornecedor+produto em 7 dias)
- RN-AUF-097-08: Validação de Conformidade SPED Fiscal (registros 0150, 1100, 1120, 1160)
- RN-AUF-097-09: Validação de Retenções Obrigatórias (IRRF 15%, ISS conforme município)
- RN-AUF-097-10: Detecção de Operações Anômalas via Machine Learning (Azure ML Isolation Forest)

---

## UC02: Consultar Histórico de Status SEFAZ com Filtros e Exportação

### 1. Descrição

Este caso de uso permite que o Auditor ou Contador consulte o histórico completo de consultas SEFAZ para NF-e, filtrando por período, status, fornecedor e chave de acesso, com opção de exportar em CSV ou Excel para análises externas.

### 2. Atores

- Auditor (principal)
- Contador
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `fin:auditoria:read`
- Multi-tenancy ativo (ClienteId válido)
- Histórico de consultas SEFAZ existente (tabela ConsultaSEFAZ)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /financeiro/consulta-sefaz-historico | - |
| 2 | - | Valida permissão RBAC (fin:auditoria:read) |
| 3 | - | Exibe filtros: DataInicio (mat-date-range-picker), DataFim, StatusSEFAZ (mat-select: Autorizado/Cancelado/Denegado/Pendente), CnpjFornecedor (mat-autocomplete), ChaveAcesso (mat-input) |
| 4 | Preenche filtros: DataInicio = 01/01/2025, DataFim = 31/01/2025, StatusSEFAZ = "Autorizado" | - |
| 5 | Clica em "Buscar" | - |
| 6 | - | Executa GET /api/auditoria-faturas/consultar-sefaz-historico?startDate=2025-01-01&endDate=2025-01-31&status=100&clienteId={clienteId} |
| 7 | - | Backend executa query: `SELECT * FROM ConsultaSEFAZ WHERE ClienteId = @clienteId AND DataConsulta BETWEEN @start AND @end AND StatusSEFAZ = @status ORDER BY DataConsulta DESC` |
| 8 | - | Aplica filtro multi-tenancy (WHERE ClienteId = currentClienteId) |
| 9 | - | Retorna lista de ConsultaSEFAZDto: `{ Id, ChaveAcesso, StatusSEFAZ, Protocolo, Mensagem, DataConsulta, TempoResposta (ms), CnpjEmitente }` paginada (50 registros/página) |
| 10 | - | Exibe tabela com colunas: Data Consulta, Chave Acesso, CNPJ Fornecedor, Status SEFAZ, Protocolo, Tempo Resposta (ms), Mensagem |
| 11 | Usuário visualiza tabela | - |
| 12 | Ordena tabela por "Tempo Resposta" (mat-sort) de forma descendente | - |
| 13 | - | Re-ordena registros: query adiciona `ORDER BY TempoResposta DESC` |
| 14 | Usuário filtra apenas consultas com TempoResposta > 5000ms (5 segundos) | - |
| 15 | - | Aplica filtro local (TypeScript): `consultas.filter(x => x.TempoResposta > 5000)` |
| 16 | - | Exibe 23 registros com tempo lento (possíveis problemas SEFAZ) |
| 17 | Clica em "Exportar CSV" | - |
| 18 | - | Executa POST /api/auditoria-faturas/exportar com body `{ tipo: "ConsultaSEFAZ", formato: "CSV", filtros: { startDate, endDate, status } }` |
| 19 | - | Backend usa CsvHelper: `csvWriter.WriteRecords(consultas)` gerando arquivo CSV com colunas: DataConsulta, ChaveAcesso, CnpjEmitente, StatusSEFAZ, Protocolo, TempoResposta, Mensagem |
| 20 | - | Retorna arquivo: `Content-Disposition: attachment; filename="consulta-sefaz-2025-01.csv"` |
| 21 | Usuário salva arquivo localmente | - |

### 5. Fluxos Alternativos

**FA01: Exportar em formato Excel (XLSX)**
- Passo 17: Usuário seleciona "Exportar Excel" ao invés de CSV
- Passo 19: Backend usa ClosedXML: cria WorkSheet "Consultas SEFAZ", adiciona header (linha 1), popula dados (linhas 2-N), formata colunas (DataConsulta = date, TempoResposta = número)
- Adiciona aba "Estatísticas" com agregações: TempoMedio, TempoMax, TotalConsultas, TaxaSucesso (count status 100 / total)
- Retorna arquivo XLSX: `filename="consulta-sefaz-2025-01.xlsx"`

**FA02: Filtrar por CNPJ Fornecedor**
- Passo 4: Usuário digita CNPJ "12.345.678/0001-90" no campo CnpjFornecedor
- Sistema executa autocomplete: busca fornecedores com CNPJ LIKE '%12345678%' em NotaFiscal (distinct CnpjEmitente)
- Exibe dropdown com opções: "12.345.678/0001-90 - FORNECEDOR A LTDA"
- Após seleção: adiciona filtro `AND CnpjEmitente = @cnpj` na query do passo 7

**FA03: Detalhes de uma Consulta SEFAZ**
- Passo 11: Usuário clica em ícone "Ver Detalhes" em uma linha da tabela
- Sistema abre modal com informações completas: ChaveAcesso, NumeroNota, DataEmissao, StatusSEFAZ, Protocolo, MensagemCompleta, TempoResposta, DataConsulta, XML de resposta SEFAZ (se disponível)
- Modal exibe botão "Reconsultar Agora" (dispara nova consulta SEFAZ)

### 6. Exceções

**EX01: Usuário sem permissão de leitura**
- Passo 2: Se usuário não tem `fin:auditoria:read` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Acesso negado para consultar histórico SEFAZ"

**EX02: Período inválido (data fim < data início)**
- Passo 6: Se DataFim < DataInicio → Retorna HTTP 400 Bad Request
- Exibe mensagem de validação: "Data fim deve ser maior que data início"

**EX03: Nenhum resultado encontrado**
- Passo 9: Se query retorna 0 registros → Retorna HTTP 200 com lista vazia
- Exibe mensagem: "Nenhuma consulta SEFAZ encontrada para os filtros selecionados"

### 7. Pós-condições

- Lista de consultas SEFAZ exibida com filtros aplicados
- Arquivo CSV ou Excel gerado (se exportação solicitada)
- Operação registrada em auditoria: `{ UsuarioId, Acao = "ConsultaHistoricoSEFAZ", Filtros = JSON, QtdResultados }`

### 8. Regras de Negócio Aplicáveis

- RN-AUF-097-02: Consulta Obrigatória de Status SEFAZ (histórico completo)
- Multi-tenancy: WHERE ClienteId = currentClienteId (row-level security)

---

## UC03: Resolver Alertas de Auditoria com Workflow de Aprovação

### 1. Descrição

Este caso de uso permite que o Auditor ou CFO resolva alertas gerados durante auditoria de NF-e, documentando ações tomadas (ignorar, corrigir, documentar) e enviando notificações para equipe financeira.

### 2. Atores

- Auditor (principal)
- CFO
- Sistema (workflow de notificações)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `fin:auditoria:alertas:resolve`
- Multi-tenancy ativo (ClienteId válido)
- AlertaAuditoria existente com Status = Novo ou Investigando

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /financeiro/alertas-auditoria | - |
| 2 | - | Valida permissão RBAC (fin:auditoria:read) |
| 3 | - | Executa GET /api/auditoria-faturas/alertas?status=Novo&severidade=Critico&clienteId={clienteId} |
| 4 | - | Backend retorna lista de AlertaAuditoriaDto: `{ Id, ChaveAcesso, TipoAlerta, Severidade, Descricao, DataGeracao, Status, UsuarioResolucao }` ordenada por Severidade DESC, DataGeracao DESC |
| 5 | - | Exibe tabela com filtros: Status (mat-select: Novo/Investigando/Resolvido), Severidade (mat-select: Critico/Aviso/Info), DataInicio, DataFim |
| 6 | - | Aplica badge de cores: Critico = red, Aviso = orange, Info = blue |
| 7 | Usuário visualiza alerta "Duplicata Detectada" (Severidade = Critico) | - |
| 8 | Clica em botão "Resolver Alerta" na linha | - |
| 9 | - | Abre modal "Resolver Alerta" com campos: Acao (mat-radio-group: Ignorar/Corrigir/Documentar), Observacoes (mat-textarea, obrigatório se Acao = Documentar), DataResolucao (auto: UtcNow) |
| 10 | Seleciona Acao = "Documentar", preenche Observacoes: "NF-e duplicada era teste, NF-e real foi importada corretamente" | - |
| 11 | Clica em "Confirmar Resolução" | - |
| 12 | - | Valida permissão RBAC (fin:auditoria:alertas:resolve) |
| 13 | - | Executa POST /api/auditoria-faturas/alertas/{alertaId}/resolver com body `{ Acao: "Documentar", Observacoes: "...", UsuarioResolucao: currentUserId }` |
| 14 | - | Backend atualiza AlertaAuditoria: `{ Status = Resolvido, DataResolucao = UtcNow, UsuarioResolucao = currentUserId, AcaoTomada = "Documentar", Observacoes = texto }` |
| 15 | - | Cria registro em AuditoriaLog (RF004): `{ Operacao = "FIN_ALERTA_RESOLVIDO", AlertaId, UsuarioId, DataHora, Observacoes }` |
| 16 | - | Envia notificação SignalR para grupo "EquipeFinanceira": `Hub.Clients.Group("EquipeFinanceira").SendAsync("AlertaResolvido", alertaDto)` |
| 17 | - | Se Severidade = Critico → Envia email para CFO: `emailService.SendAsync(to: "cfo@empresa.com", subject: "Alerta Crítico Resolvido - {TipoAlerta}", body: "Alerta {id} foi resolvido por {usuario}")` |
| 18 | - | Retorna HTTP 200 com mensagem: "Alerta resolvido com sucesso" |
| 19 | - | Atualiza tabela: remove alerta da lista de "Novo", adiciona badge "Resolvido" |
| 20 | Usuário visualiza alerta marcado como Resolvido | - |

### 5. Fluxos Alternativos

**FA01: Ação "Corrigir" redireciona para edição de NF-e**
- Passo 10: Usuário seleciona Acao = "Corrigir"
- Passo 14: Sistema não marca como Resolvido imediatamente, marca Status = EmCorrecao
- Redireciona para /financeiro/notas-fiscais/editar/{notaFiscalId} (RF032)
- Após salvar correção em RF032: Webhook dispara evento NfeCorrigidaEvent
- Sistema atualiza AlertaAuditoria: `{ Status = Resolvido, AcaoTomada = "Corrigido", DataResolucao = UtcNow }`

**FA02: Ação "Ignorar" requer justificativa obrigatória**
- Passo 10: Usuário seleciona Acao = "Ignorar"
- Sistema exibe campo Observacoes como OBRIGATÓRIO (validador Angular required)
- Se usuário tentar salvar sem preencher → Exibe erro: "Justificativa é obrigatória para ignorar alerta"
- Após preencher: marca Status = Ignorado (diferente de Resolvido)

**FA03: Alerta de Severidade Crítica exige aprovação de CFO**
- Passo 12: Se Severidade = Critico E currentUser.Role != "CFO" → Marca Status = AguardandoAprovacao ao invés de Resolvido
- Envia notificação push para CFO: "Alerta crítico {id} aguarda sua aprovação"
- CFO acessa alerta, revisa Observacoes, clica em "Aprovar Resolução"
- Sistema atualiza: `{ Status = Resolvido, AprovadoPor = cfoUserId, DataAprovacao = UtcNow }`

### 6. Exceções

**EX01: Usuário sem permissão para resolver alertas**
- Passo 12: Se usuário não tem `fin:auditoria:alertas:resolve` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para resolver alertas de auditoria"

**EX02: Alerta já foi resolvido por outro usuário**
- Passo 14: Se AlertaAuditoria.Status já é "Resolvido" → Retorna HTTP 409 Conflict
- Exibe mensagem: "Alerta já foi resolvido por {UsuarioResolucao} em {DataResolucao}"

**EX03: Observações ausentes quando obrigatórias**
- Passo 13: Se Acao = "Documentar" OU Acao = "Ignorar" E Observacoes.IsNullOrWhiteSpace() → Retorna HTTP 400 Bad Request
- Exibe erro de validação: "Observações são obrigatórias para esta ação"

### 7. Pós-condições

- AlertaAuditoria atualizado com Status = Resolvido (ou EmCorrecao, Ignorado, AguardandoAprovacao)
- Operação registrada em auditoria (RF004): `{ UsuarioId, AlertaId, Acao, Observacoes, DataResolucao }`
- Notificação enviada via SignalR para EquipeFinanceira
- Email enviado ao CFO se Severidade = Critico
- Se Acao = Corrigir: Usuário redirecionado para RF032

### 8. Regras de Negócio Aplicáveis

- RBAC: `fin:auditoria:alertas:resolve` obrigatório
- Multi-tenancy: Alertas isolados por ClienteId
- Workflow de aprovação: Alertas críticos exigem CFO

---

## UC04: Gerar Relatório Fiscal Parametrizado (Livro Fiscal, Apuração ICMS, SPED)

### 1. Descrição

Este caso de uso permite que o Contador ou CFO gere relatórios fiscais parametrizados (Livro Fiscal, Apuração ICMS, SPED Fiscal) com filtros de período, CFOP, fornecedor e tipo de operação, exportando em PDF, Excel ou JSON.

### 2. Atores

- Contador (principal)
- CFO
- Sistema

### 3. Pré-condições

- Usuário autenticado
- Permissão: `fin:auditoria:relatorios`
- Multi-tenancy ativo (ClienteId válido)
- NF-e auditadas existentes no período solicitado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /financeiro/relatorios-fiscais | - |
| 2 | - | Valida permissão RBAC (fin:auditoria:relatorios) |
| 3 | - | Exibe formulário com mat-stepper (3 passos): Passo 1 - Filtros, Passo 2 - Agregações, Passo 3 - Formato |
| 4 | **Passo 1 - Filtros**: Seleciona TipoRelatorio = "Livro Fiscal", DataInicio = 01/01/2025, DataFim = 31/01/2025, CFOP (mat-select multi) = [5102, 6102], IncluirCanceladas = false | - |
| 5 | Clica em "Próximo" | - |
| 6 | **Passo 2 - Agregações**: Seleciona GroupBy (checkboxes) = [Dia, CFOP, Fornecedor], IncluirTotais = true | - |
| 7 | Clica em "Próximo" | - |
| 8 | **Passo 3 - Formato**: Seleciona Formato = "PDF", IncluirGraficos = true | - |
| 9 | Clica em "Gerar Relatório" | - |
| 10 | - | Valida permissão RBAC (fin:auditoria:relatorios) |
| 11 | - | Executa GET /api/auditoria-faturas/relatorios/livro-fiscal?startDate=2025-01-01&endDate=2025-01-31&cfop=5102,6102&incluirCanceladas=false&formato=PDF&clienteId={clienteId} |
| 12 | - | Backend consulta NotaFiscal JOIN AuditoriaFatura WHERE ClienteId = @clienteId AND DataEmissao BETWEEN @start AND @end AND CFOP IN (@cfops) AND (IncluirCanceladas OR DataCancelamento IS NULL) |
| 13 | - | Aplica agregações: GROUP BY DATE(DataEmissao), CFOP, CnpjEmitente com SUM(ValorTotal), SUM(ValorICMS), SUM(ValorIPI), COUNT(*) |
| 14 | - | Ordena resultados: ORDER BY DataEmissao, CFOP, RazaoSocial |
| 15 | - | **Gera PDF com iTextSharp**: Cria documento, adiciona header com logo empresa + título "Livro Fiscal - Janeiro/2025", adiciona metadata (data geração, usuário) |
| 16 | - | Adiciona seção "Filtros Aplicados": Período, CFOPs, Incluir Canceladas |
| 17 | - | Adiciona tabela principal com colunas: Data, Chave Acesso, Número NF-e, Fornecedor (CNPJ + Razão Social), CFOP, Valor Total, ICMS, IPI |
| 18 | - | Adiciona seção "Totalizadores": Total Geral, Total ICMS, Total IPI, Quantidade NF-e |
| 19 | - | Se IncluirGraficos = true → Adiciona gráfico de barras: Volume por Dia (eixo X = Data, eixo Y = ValorTotal) |
| 20 | - | Adiciona seção "Agregações": Tabela por CFOP (CFOP, Descrição, Qtd NF-e, Valor Total, ICMS), Tabela por Fornecedor (top 10 fornecedores por valor) |
| 21 | - | Salva PDF em Azure Blob Storage: `relatorios/{clienteId}/livro-fiscal-2025-01.pdf` com SAS token válido por 7 dias |
| 22 | - | Retorna response: `{ DownloadUrl = sasUrl, FileName = "livro-fiscal-2025-01.pdf", FileSize = bytes, ExpiresAt = UtcNow + 7 dias }` |
| 23 | - | Frontend exibe mensagem: "Relatório gerado com sucesso" + link de download |
| 24 | Usuário clica em "Baixar Relatório" | - |
| 25 | - | Abre URL com SAS token, navegador faz download do PDF |
| 26 | Usuário salva arquivo localmente | - |

### 5. Fluxos Alternativos

**FA01: Gerar Apuração ICMS ao invés de Livro Fiscal**
- Passo 4: Usuário seleciona TipoRelatorio = "Apuração ICMS"
- Passo 12: Backend agrupa NF-e por CFOP de entrada (6xxx) vs saída (5xxx)
- Calcula: TotalEntradas (sum CFOP 6xxx), TotalSaidas (sum CFOP 5xxx), ICMSEntradas, ICMSSaidas
- Apuração: SaldoICMS = ICMSSaidas - ICMSEntradas (se positivo: recolher; se negativo: crédito)
- PDF exibe: Resumo Mensal, Detalhamento Entradas, Detalhamento Saídas, Apuração Final (saldo a recolher ou crédito)

**FA02: Exportar em formato Excel (XLSX) ao invés de PDF**
- Passo 8: Usuário seleciona Formato = "Excel"
- Passo 15-20: Backend usa ClosedXML ao invés de iTextSharp
- Cria WorkSheet "Livro Fiscal" com header (linha 1): Data, Chave, Número, Fornecedor, CFOP, Valor, ICMS, IPI
- Popula dados (linhas 2-N), formata colunas (Data = date, Valor = currency)
- Adiciona WorkSheet "Totalizadores" com agregações (por CFOP, por Fornecedor)
- Se IncluirGraficos = true → Adiciona WorkSheet "Gráficos" com Chart (barra vertical)
- Retorna XLSX: `filename="livro-fiscal-2025-01.xlsx"`

**FA03: Agendar relatório recorrente mensal**
- Após passo 9: Usuário clica em toggle "Agendar Recorrente"
- Sistema exibe campos adicionais: CronExpression (helper: "Todo dia 1 do mês às 08:00"), Recipients (mat-chip-list de emails)
- Passo 10: Executa POST /api/auditoria-faturas/relatorios/agendar com body `{ TipoRelatorio, Filtros, Formato, CronExpression = "0 8 1 * *", Recipients = ["contador@empresa.com", "cfo@empresa.com"] }`
- Backend cria ScheduledAuditReport: `{ ClienteId, TipoRelatorio, CronExpression, Recipients, Ativo = true }`
- Registra RecurringJob Hangfire: `RecurringJob.AddOrUpdate(scheduledReport.Id, () => GenerateAndSendReportAsync(reportId), cronExpression)`
- Job executa mensalmente: gera relatório, salva em Blob Storage, envia email com link download (válido 7 dias)

### 6. Exceções

**EX01: Usuário sem permissão para gerar relatórios**
- Passo 10: Se usuário não tem `fin:auditoria:relatorios` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para gerar relatórios fiscais"

**EX02: Período inválido (> 12 meses)**
- Passo 11: Se DataFim - DataInicio > 365 dias → Retorna HTTP 400 Bad Request
- Exibe mensagem: "Período máximo permitido é 12 meses. Reduza o intervalo de datas"

**EX03: Nenhuma NF-e encontrada para os filtros**
- Passo 12: Se query retorna 0 registros → Retorna HTTP 200 com mensagem: "Nenhuma NF-e encontrada para os filtros selecionados"
- Não gera relatório, exibe sugestão: "Tente ampliar o período ou remover filtros de CFOP"

**EX04: Erro ao gerar PDF (falta de memória)**
- Passo 15: Se resultado tem mais de 10.000 registros → iTextSharp pode lançar OutOfMemoryException
- Sistema captura exceção, retorna HTTP 500 com mensagem: "Relatório muito grande (10.000+ NF-e). Use filtros mais restritivos ou exporte em Excel"

### 7. Pós-condições

- Relatório gerado e salvo em Azure Blob Storage com SAS token válido por 7 dias
- Operação registrada em auditoria: `{ UsuarioId, TipoRelatorio, Periodo, QtdRegistros, Formato, DataGeracao }`
- Se agendamento recorrente: RecurringJob criado em Hangfire
- Arquivo disponível para download imediato

### 8. Regras de Negócio Aplicáveis

- RN-AUF-097-08: Validação de Conformidade SPED Fiscal (relatórios baseados em registros SPED)
- RBAC: `fin:auditoria:relatorios` obrigatório
- Multi-tenancy: WHERE ClienteId = currentClienteId
- Período máximo: 12 meses

---

## UC05: Visualizar Dashboard Fiscal em Tempo Real com KPIs e Gráficos

### 1. Descrição

Este caso de uso permite que o CFO ou Auditor visualize um dashboard fiscal em tempo real com KPIs de volume de NF-e, valores, impostos, alertas, tendências, conformidade SPED e gráficos interativos atualizados via SignalR.

### 2. Atores

- CFO (principal)
- Auditor
- Sistema (atualização tempo real via SignalR)

### 3. Pré-condições

- Usuário autenticado
- Permissão: `fin:auditoria:read`
- Multi-tenancy ativo (ClienteId válido)
- SignalR Hub conectado (NotificacoesHub)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela /financeiro/dashboard-fiscal | - |
| 2 | - | Valida permissão RBAC (fin:auditoria:read) |
| 3 | - | Conecta ao SignalR Hub: `hubConnection.start()` e entra no grupo "DashboardFiscal_{clienteId}" |
| 4 | - | Executa GET /api/auditoria-faturas/dashboard?periodo=MesAtual&clienteId={clienteId} |
| 5 | - | Backend calcula KPIs para período (mês atual): |
| 6 | - | **KPI 1: Total NF-e**: `SELECT COUNT(*) FROM NotaFiscal WHERE ClienteId = @id AND MONTH(DataEmissao) = MONTH(UtcNow) AND YEAR(DataEmissao) = YEAR(UtcNow)` |
| 7 | - | **KPI 2: Valor Total**: `SELECT SUM(ValorTotal) FROM NotaFiscal WHERE ...` |
| 8 | - | **KPI 3: Total ICMS**: `SELECT SUM(ValorICMS) FROM NotaFiscal WHERE ...` |
| 9 | - | **KPI 4: Taxa Auditoria Automática**: `(COUNT(AuditoriaStatus = Auditado) / COUNT(*)) * 100` |
| 10 | - | **KPI 5: Alertas Críticos**: `SELECT COUNT(*) FROM AlertaAuditoria WHERE Severidade = Critico AND Status = Novo AND MONTH(DataGeracao) = MONTH(UtcNow)` |
| 11 | - | **KPI 6: Conformidade SPED**: `(COUNT(ConformeSPED = true) / COUNT(*)) * 100` |
| 12 | - | **KPI 7: Tempo Médio Auditoria**: `SELECT AVG(DATEDIFF(second, DataInicio, DataConclusao)) FROM AuditoriaFatura WHERE MONTH(DataConclusao) = MONTH(UtcNow)` |
| 13 | - | **KPI 8: Disponibilidade SEFAZ**: `(COUNT(StatusSEFAZ = 100) / COUNT(ConsultaSEFAZ)) * 100` últimas 24h |
| 14 | - | Retorna DashboardDto: `{ TotalNFe = 1523, ValorTotal = R$ 5.234.567, TotalICMS = R$ 942.222, TaxaAuditoria = 97.3%, AlertasCriticos = 12, ConformidadeSPED = 99.1%, TempoMedioAuditoria = 3.2s, DisponibilidadeSEFAZ = 99.8% }` |
| 15 | - | Frontend exibe 8 cards com KPIs usando mat-card: cada card mostra valor principal (fonte grande), variação vs mês anterior (ícone ↑/↓ + percentual), sparkline (mini gráfico últimos 7 dias) |
| 16 | - | **Gráfico 1: Volume de NF-e por Dia** - Chart.js line chart, eixo X = últimos 30 dias, eixo Y = quantidade NF-e por dia |
| 17 | - | **Gráfico 2: Valor Total por CFOP** - Chart.js pie chart, segmentos = top 5 CFOPs por valor (ex: 5102 - 45%, 6102 - 30%, ...) |
| 18 | - | **Gráfico 3: Alertas por Tipo** - Chart.js bar chart horizontal, eixo X = quantidade, eixo Y = TipoAlerta (Duplicata, AliquotaInconsistente, ...) |
| 19 | - | **Gráfico 4: Conformidade SPED por Semana** - Chart.js line chart, eixo X = últimas 4 semanas, eixo Y = percentual conformidade |
| 20 | Usuário visualiza dashboard completo | - |
| 21 | - | Sistema inicia escuta de eventos SignalR: `hubConnection.on("DashboardAtualizado", (kpis) => { /* atualiza cards */ })` |
| 22 | (Evento externo): Nova NF-e é auditada com alerta crítico | - |
| 23 | - | Backend dispara SignalR: `Hub.Clients.Group("DashboardFiscal_{clienteId}").SendAsync("DashboardAtualizado", { AlertasCriticos = 13, TotalNFe = 1524 })` |
| 24 | - | Frontend recebe evento, atualiza KPI "Alertas Críticos" de 12 → 13 com animação (flash vermelho) |
| 25 | - | Exibe toast notification: "Novo alerta crítico detectado - Duplicata em NF-e {chave}" |
| 26 | Usuário clica em card "Alertas Críticos" | - |
| 27 | - | Redireciona para /financeiro/alertas-auditoria com filtro Severidade=Critico, Status=Novo pré-aplicado |

### 5. Fluxos Alternativos

**FA01: Filtrar dashboard por período (trimestre, semestre, ano)**
- Passo 4: Usuário seleciona filtro Periodo = "Trimestre" no dropdown
- Sistema re-executa GET /api/auditoria-faturas/dashboard?periodo=Trimestre&clienteId={clienteId}
- Backend ajusta queries: MONTH(DataEmissao) >= MONTH(UtcNow) - 3 AND YEAR = YEAR(UtcNow)
- Recalcula todos KPIs e gráficos para últimos 3 meses
- Frontend atualiza dashboard com novos valores

**FA02: Drill-down em Gráfico de Volume por Dia**
- Passo 20: Usuário clica em ponto do gráfico "Volume por Dia" (ex: dia 15/01/2025 com 87 NF-e)
- Sistema abre modal com lista de NF-e daquele dia: GET /api/auditoria-faturas?dataEmissao=2025-01-15&clienteId={clienteId}
- Modal exibe tabela: Chave Acesso, Fornecedor, Valor Total, Status SEFAZ, Status Auditoria
- Usuário pode clicar em uma NF-e para ver detalhes ou iniciar auditoria

**FA03: Exportar dashboard em PDF**
- Passo 20: Usuário clica em botão "Exportar Dashboard"
- Sistema captura screenshot dos cards e gráficos usando html2canvas
- Gera PDF com iTextSharp: adiciona header com logo + data, insere imagens dos cards/gráficos, adiciona tabela com valores numéricos dos KPIs
- Retorna arquivo: `dashboard-fiscal-2025-01-28.pdf`

### 6. Exceções

**EX01: Usuário sem permissão para visualizar dashboard**
- Passo 2: Se usuário não tem `fin:auditoria:read` → Retorna HTTP 403 Forbidden
- Exibe mensagem: "Acesso negado ao dashboard fiscal"

**EX02: Erro ao conectar SignalR Hub**
- Passo 3: Se `hubConnection.start()` falha (ex: WebSocket não suportado) → Exibe aviso: "Atualizações em tempo real desabilitadas. Recarregue a página manualmente"
- Dashboard funciona normalmente, mas sem push notifications

**EX03: Nenhuma NF-e no período selecionado**
- Passo 6: Se query retorna COUNT = 0 → Retorna HTTP 200 com KPIs zerados
- Exibe mensagem: "Nenhuma NF-e encontrada no período selecionado"
- Gráficos exibem estado vazio com ícone e mensagem "Sem dados para exibir"

### 7. Pós-condições

- Dashboard exibido com 8 KPIs atualizados
- 4 gráficos interativos renderizados (Chart.js)
- Conexão SignalR ativa para atualizações em tempo real
- Operação registrada em auditoria: `{ UsuarioId, Acao = "VisualizouDashboardFiscal", Periodo, DataHora }`

### 8. Regras de Negócio Aplicáveis

- Multi-tenancy: Todos KPIs filtrados por ClienteId
- Período padrão: Mês atual (pode ser alterado para trimestre, semestre, ano)
- Taxa Auditoria Automática meta: >= 95%
- Alertas Críticos meta: < 1% do total de NF-e
- Conformidade SPED meta: 100%
- Tempo Médio Auditoria meta: < 5s
- Disponibilidade SEFAZ meta: >= 99%

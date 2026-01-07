# UC-RF078 - Casos de Uso - Integração com ERPs

**Versão**: 1.0 | **Data**: 2025-12-29
**RF Relacionado**: RF078 - Integração com ERPs
**EPIC**: EPIC008-SD-Service-Desk
**Fase**: Fase 5 - Service Desk

---

## UC01: Configurar e Testar Conexão com ERP

### 1. Descrição

Permite ao administrador de integrações configurar credenciais, endpoints e parâmetros de conexão com ERPs (SAP, TOTVS Protheus, Oracle EBS) de forma segura através de Azure Key Vault, e validar a conectividade antes de ativar sincronizações automáticas.

### 2. Atores

- Administrador de Integrações (role: ADMIN_INTEGRACAO)
- Sistema IControlIT
- Azure Key Vault
- ERP (SAP/TOTVS/Oracle)

### 3. Pré-condições

- Usuário autenticado com permissão `integracao:configuracao`
- Azure Key Vault configurado com acesso concedido ao backend
- Credenciais do ERP (usuário, senha, certificados RFC, endpoints) disponíveis
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/admin/integracao/configuracao` | - |
| 2 | - | Valida permissão RBAC `integracao:configuracao` |
| 3 | - | Busca configurações existentes (sem exibir credenciais sensíveis) |
| 4 | - | Exibe formulário com campos: Nome ERP (SAP/TOTVS/ORACLE), Tipo de Autenticação (RFC/OAuth/REST), Host, Porta, Cliente/Mandante |
| 5 | Seleciona ERP (ex: SAP) e preenche: Host="sap.empresa.com.br", Porta=3300, Cliente=100, Tipo="RFC" | - |
| 6 | Clica em "Adicionar Credencial" para abrir modal seguro | - |
| 7 | - | Exibe campos sensíveis: RFC_USER, RFC_PASSWORD, CERTIFICATE (upload .p12) |
| 8 | Preenche RFC_USER="ICONTROLIT_USER", RFC_PASSWORD (input mascarado), faz upload certificado RFC | - |
| 9 | Clica em "Salvar Credencial" | - |
| 10 | - | Valida campos obrigatórios (Host, Porta, USER, PASSWORD não vazios) |
| 11 | - | **Executa SaveErpCredentialCommand** que: 1) Armazena credenciais no Azure Key Vault com chave `erp-sap-rfc-user`, `erp-sap-rfc-password`, `erp-sap-cert`, 2) Salva apenas metadados no banco (Host, Porta, Tipo, NomeERP), NUNCA credenciais |
| 12 | - | Registra auditoria: `ERP_CONFIG_SAVED`, NomeERP="SAP", Usuario=CurrentUser, Timestamp |
| 13 | - | Exibe toast de sucesso i18n: "integracao.mensagens.configuracao_salva" |
| 14 | Clica em "Testar Conexão" | - |
| 15 | - | **Executa TestErpConnectionCommand** que: 1) Recupera credenciais do Key Vault (ObterCredencial("SAP", "RFC_USER")), 2) Tenta conexão RFC com SAP usando NCo (SAP .NET Connector), 3) Executa query simples (SELECT COUNT(*) FROM T001 - tabela de empresas SAP) |
| 16 | - | **Se conexão bem-sucedida**: Registra auditoria `ERP_CONN_TEST_SUCCESS`, exibe toast verde "Conexão estabelecida com sucesso!" |
| 17 | - | Habilita toggle "Ativar Sincronização Automática" |
| 18 | Ativa toggle "Sincronização Automática" | - |
| 19 | - | **Executa EnableErpSyncCommand** que: 1) Marca integração como ativa no banco, 2) Agenda Hangfire job RecurringJob para polling a cada 5 min (fallback se webhook falhar) |
| 20 | - | Exibe dashboard atualizado com status "Ativo - Última sincronização: Nunca" |

### 5. Fluxos Alternativos

**FA01 - Credencial Já Existe no Key Vault (Atualização)**:
- Passo 11: Se chave `erp-sap-rfc-password` já existe no Key Vault, sistema pergunta "Substituir credencial existente? (rotação manual)"
- Usuário confirma
- Sistema versiona credencial antiga com sufixo `_v1`, `_v2` antes de sobrescrever
- Sistema atualiza tabela `ErpConfigurationHistory` com registro de rotação manual
- Retorna ao passo 12

**FA02 - Teste de Conexão Falha com Erro de Autenticação**:
- Passo 16: Conexão RFC retorna erro "AUTHORIZATION_FAILURE" ou similar
- Sistema registra auditoria `ERP_CONN_TEST_FAILURE` com detalhes do erro
- Sistema exibe modal com erro detalhado: "Falha na autenticação. Verifique usuário e senha no Key Vault."
- Sistema sugere rotação de credencial
- Botão "Reconfigurar Credencial" volta ao passo 6
- Fluxo termina sem ativar sincronização

**FA03 - Teste de Conexão Falha com Timeout de Rede**:
- Passo 16: Conexão RFC timeout após 30 segundos
- Sistema registra auditoria `ERP_CONN_TEST_TIMEOUT` com Host e Porta tentados
- Sistema exibe modal: "Timeout ao conectar em sap.empresa.com.br:3300. Verifique firewall e VPN."
- Sistema sugere validação de rede (ping, telnet)
- Fluxo termina sem ativar sincronização

**FA04 - Certificado RFC Inválido ou Expirado**:
- Passo 11: Upload de certificado .p12 → sistema valida usando X509Certificate2
- Se certificado expirado (NotAfter < DateTime.UtcNow): Sistema rejeita com erro "Certificado expirado em {data}"
- Se senha do certificado incorreta: Sistema rejeita com erro "Senha do certificado inválida"
- Usuário deve fazer upload de certificado válido
- Retorna ao passo 8

**FA05 - Rotação Automática de Credencial Detectada Expiração Próxima**:
- Durante passo 11: Sistema verifica se credencial existente expira em < 7 dias
- Sistema exibe alerta amarelo: "Credencial SAP expira em 5 dias. Rotação automática agendada."
- Sistema agenda Hangfire job `RotacionarCredencialJob` para executar 3 dias antes do vencimento
- Job consulta ERP para gerar nova credencial OAuth (se suportado) ou notifica admin para rotação manual
- Fluxo continua normalmente

### 6. Exceções

**EX01 - Usuário Sem Permissão ADMIN_INTEGRACAO**:
- Passo 2: Validação RBAC falha
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem i18n: "permissoes.acesso_negado_integracao"
- Fluxo termina imediatamente

**EX02 - Azure Key Vault Indisponível**:
- Passo 11: Chamada ao Key Vault timeout ou retorna erro 503
- Sistema registra erro crítico em logs estruturados
- Sistema entra em modo fallback: salva credencial temporariamente em memória criptografada (AES-256 com chave efêmera)
- Sistema exibe alerta crítico: "Key Vault indisponível. Configuração temporária ativa por 1h. Necessário reconfigurar."
- Sistema agenda retry automático a cada 5 min para mover credencial para Key Vault
- Fluxo continua com risco aceito

**EX03 - Certificado RFC Corrompido ou Formato Inválido**:
- Passo 11: Upload de arquivo .p12 → sistema tenta carregar com X509Certificate2
- Se arquivo corrompido: Lança CryptographicException
- Sistema exibe erro: "Arquivo de certificado inválido ou corrompido. Faça upload de arquivo .p12 válido."
- Fluxo retorna ao passo 8 sem salvar

**EX04 - Limite de Configurações por Cliente Excedido**:
- Passo 11: Cliente já possui 3 ERPs configurados (limite por licença)
- Sistema valida contrato do cliente em `ClienteContrato` table
- Se limite excedido: Sistema retorna HTTP 400 com erro "Limite de 3 ERPs por cliente. Upgrade de licença necessário."
- Fluxo termina sem salvar

**EX05 - Job de Sincronização Falha ao Agendar no Hangfire**:
- Passo 19: Hangfire retorna erro ao agendar RecurringJob (servidor Hangfire offline)
- Sistema registra erro crítico `HANGFIRE_SCHEDULE_FAILED`
- Sistema exibe alerta: "Sincronização automática não pôde ser agendada. Executar manualmente via botão 'Sincronizar Agora'."
- Sistema marca integração como "Ativa (Manual)" ao invés de "Ativa (Automática)"
- Fluxo continua com funcionalidade parcial

### 7. Pós-condições

- Credenciais do ERP armazenadas de forma segura no Azure Key Vault com rotação configurada
- Metadados de configuração salvos no banco (Host, Porta, Tipo, NomeERP) sem credenciais sensíveis
- Conexão com ERP validada e testada antes de ativar sincronização
- Sincronização automática agendada via Hangfire RecurringJob a cada 5 min (se ativada)
- Auditoria completa registrada: `ERP_CONFIG_SAVED`, `ERP_CONN_TEST_SUCCESS`, `ERP_SYNC_ENABLED`
- Dashboard atualizado com status da integração em tempo real

### 8. Regras de Negócio Aplicáveis

- RN-ERP-078-02: Credenciais de ERP devem ser armazenadas em Azure Key Vault com rotação automática
- RN-ERP-078-07: Logs de integração devem registrar entrada, saída e erro em tabela estruturada com retenção de 7 anos

---

## UC02: Sincronizar Centros de Custo Bidirecional via Webhook

### 1. Descrição

Recebe notificação webhook do ERP (SAP, TOTVS, Oracle) quando Centro de Custo é criado, alterado ou desativado, valida assinatura HMAC-SHA256, e sincroniza automaticamente para IControlIT. Também permite exportação reversa de Centros de Custo criados em IControlIT para o ERP com tratamento de conflitos.

### 2. Atores

- ERP (SAP/TOTVS/Oracle) enviando webhook
- Sistema IControlIT (receptor e processador)
- Azure Service Bus (fila de mensagens)
- Administrador de Integrações (resolve conflitos manuais)

### 3. Pré-condições

- Webhook configurado no ERP apontando para `https://icontrolit.com.br/api/v1/integracao/webhook/sap`
- Chave secreta HMAC compartilhada entre ERP e IControlIT armazenada em Key Vault
- Azure Service Bus configurado para processar mensagens de forma assíncrona
- Multi-tenancy: Webhook inclui header `X-Client-Id` para identificar tenant

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | ERP detecta alteração em Centro de Custo (ex: KOSTL="1000" alterado de "TI" para "TI - Infraestrutura") | - |
| 2 | ERP envia POST para `https://icontrolit.com.br/api/v1/integracao/webhook/sap` | - |
| 3 | - | Payload JSON: `{"event":"centro_custo.updated", "data":{"kostl":"1000", "descricao":"TI - Infraestrutura", "ativo":true}, "timestamp":"2025-12-29T10:00:00Z"}` |
| 4 | - | Header `X-Hub-Signature`: "sha256=abc123..." (HMAC do body) |
| 5 | - | Header `X-Client-Id`: "123" (identifica tenant IControlIT) |
| 6 | - | **WebhookValidationFilter intercepta request** antes do controller |
| 7 | - | Lê body completo e header `X-Hub-Signature` |
| 8 | - | Recupera chave secreta do Key Vault: `await _vault.GetSecretAsync("erp-webhook-secret")` |
| 9 | - | Calcula HMAC-SHA256 do body usando chave: `using (var hmac = new HMACSHA256(key)) { hash = hmac.ComputeHash(body); }` |
| 10 | - | Compara assinatura recebida com calculada (timing-safe comparison) |
| 11 | - | **Se assinatura válida**: Continua ao controller; **Se inválida**: Retorna HTTP 403 Forbidden, registra tentativa de spoofing em log de segurança, termina fluxo |
| 12 | - | **Controller deserializa payload** em `WebhookErpDto` |
| 13 | - | Gera UUID único: `messageId = Guid.NewGuid().ToString()` para deduplicação |
| 14 | - | **Verifica se MessageId já foi processado**: `await _repo.JaProcessada(messageId)` consultando `IntegrationAudit.MessageId` |
| 15 | - | **Se duplicata detectada**: Registra `INTEG_DUPLICATA`, retorna HTTP 200 OK (idempotência), termina fluxo |
| 16 | - | **Publica mensagem no Azure Service Bus** fila `centro-custo-sync` com payload completo + messageId |
| 17 | - | Retorna HTTP 202 Accepted para o ERP (processamento assíncrono) |
| 18 | - | **Worker processa mensagem da fila** (CentroCustoSyncHandler) |
| 19 | - | **Valida schema JSON** contra JSON Schema v7: campos obrigatórios (kostl, descricao), tipos corretos |
| 20 | - | **Se schema inválido**: Move mensagem para DLQ, registra `TRANSFORM_VALIDATION_FAIL`, notifica admin, termina |
| 21 | - | **Busca Centro de Custo existente** por CodigoERP="1000": `await _repo.BuscarPorCodigoERP("1000")` |
| 22 | - | **Se não existe**: Executa `CreateCentroCustoCommand` com Codigo=auto, Descricao="TI - Infraestrutura", CodigoERP="1000", ClienteId=123 |
| 23 | - | **Se existe**: Executa `UpdateCentroCustoCommand` atualizando apenas Descricao (não sobrescreve Codigo interno) |
| 24 | - | Aplica filtro multi-tenancy: `WHERE ClienteId = 123` (do header X-Client-Id) |
| 25 | - | **Salva alteração no banco** com campos de auditoria: UpdatedBy="SYSTEM_ERP", UpdatedAt=UtcNow |
| 26 | - | **Registra em IntegrationAudit** tabela: MessageId, TipoIntegracao="CC_SYNC", DirecaoFluxo="INBOUND", StatusExecucao="SUCESSO", DadosEntrada=payload JSON, TempoExecucao_ms=120 |
| 27 | - | **Marca MessageId como processado** em cache Redis (TTL 7 dias) para deduplicação rápida |
| 28 | - | **Publica evento de domínio** `CentroCustoSynchronizedEvent` para notificar outros bounded contexts |
| 29 | - | **Atualiza dashboard em tempo real** via SignalR: envia evento `IntegrationStatusUpdated` para grupo `IntegrationAdmins` |

### 5. Fluxos Alternativos

**FA01 - Centro de Custo Foi Alterado em IControlIT Enquanto Webhook Chegava (Conflito)**:
- Passo 23: Ao atualizar, sistema detecta que `UpdatedAt` do registro local > `timestamp` do webhook
- Sistema identifica conflito de concorrência
- Sistema aplica estratégia **Last Write Wins (LWW)**: webhook sempre vence pois ERP é source of truth
- Sistema sobrescreve dados locais com dados do ERP
- Sistema registra auditoria `CC_SYNC_CONFLICT_RESOLVED` com dados antes/depois
- Sistema notifica admin via alerta: "Conflito resolvido automaticamente: Centro de Custo 1000 atualizado pelo ERP"
- Retorna ao passo 24

**FA02 - Centro de Custo Desativado no ERP (ativo=false)**:
- Passo 3: Payload webhook contém `"ativo": false`
- Sistema identifica desativação
- Sistema NÃO deleta registro em IControlIT (soft delete), marca como IsActive=false
- Sistema verifica dependências: se Centro de Custo tem departamentos, contratos ou ativos vinculados
- Se tem dependências: Sistema NÃO permite desativar, registra `CC_DEACTIVATION_BLOCKED`, notifica admin com lista de dependências
- Se sem dependências: Sistema desativa normalmente
- Retorna ao passo 24

**FA03 - Sincronização Reversa (IControlIT → ERP)**:
- Usuário cria Centro de Custo manualmente em IControlIT (tela `/cadastros/centros-custo/novo`)
- Sistema detecta que CodigoERP está vazio (novo registro sem link ERP)
- Sistema publica evento `CentroCustoCreatedEvent`
- Handler `ExportCentroCustoToErpHandler` escuta evento
- Handler valida se integração ERP está ativa para o ClienteId
- Handler prepara payload RFC para SAP: BAPI_COSTCENTER_CREATEMULTIPLE ou REST API para TOTVS
- Handler executa chamada com retry + backoff exponencial
- Se sucesso: ERP retorna CodigoERP="2000", handler atualiza registro IControlIT com CodigoERP="2000"
- Se falha após 5 retries: Move para DLQ, notifica admin
- Fluxo termina com sincronização bidirecional completa

**FA04 - ERP Envia Múltiplos Webhooks em Burst (Deduplicação)**:
- Passo 14: SAP envia webhook do mesmo evento 3x (retry automático do SAP por timeout anterior)
- Primeiro webhook: MessageId não existe em cache Redis → processa normalmente
- Segundo webhook (2s depois): MessageId existe em cache → detecta duplicata, retorna 200 OK sem processar
- Terceiro webhook (5s depois): MessageId existe em cache → detecta duplicata novamente
- Sistema registra métrica `integ_duplicates_total` = 2 para monitoramento
- Fluxo termina com apenas 1 processamento efetivo

### 6. Exceções

**EX01 - Assinatura HMAC Inválida ou Ausente (Spoofing)**:
- Passo 10: Assinatura recebida != assinatura calculada OU header `X-Hub-Signature` ausente
- Sistema retorna HTTP 403 Forbidden imediatamente
- Sistema registra em log de segurança: `WEBHOOK_SPOOFING_ATTEMPT`, IP=origem, Timestamp, Payload (sanitizado)
- Sistema incrementa contador de tentativas de spoofing para o IP
- Se IP tenta >5x em 1h: Sistema bloqueia IP temporariamente (rate limiting)
- Fluxo termina sem processar webhook

**EX02 - Payload JSON Malformado ou Schema Inválido**:
- Passo 19: Validação JSON Schema falha (campo obrigatório faltando, tipo incorreto)
- Sistema registra `TRANSFORM_VALIDATION_FAIL` em IntegrationAudit com erros detalhados
- Sistema move mensagem para Dead Letter Queue (DLQ) no Service Bus
- Sistema notifica administrador via email: "Webhook com schema inválido recebido do SAP. Verificar DLQ."
- Sistema retorna HTTP 202 Accepted para ERP (evitar retry infinito)
- Fluxo termina sem processar, mensagem fica na DLQ para investigação manual

**EX03 - Azure Service Bus Indisponível (Falha de Publicação)**:
- Passo 16: Tentativa de publicar na fila retorna erro 503 ou timeout
- Sistema entra em modo fallback: salva webhook em tabela temporária `WebhookPendingQueue`
- Sistema agenda Hangfire job `ProcessPendingWebhooksJob` para executar a cada 2 min
- Job tenta republicar mensagens da tabela temporária para Service Bus
- Sistema retorna HTTP 503 para ERP (ERP deve fazer retry do webhook)
- Fluxo termina com processamento diferido

**EX04 - Centro de Custo com CodigoERP Duplicado (Integridade)**:
- Passo 22: Tentativa de criar novo Centro de Custo com CodigoERP="1000" que já existe para outro registro
- Sistema detecta violação de constraint UNIQUE em CodigoERP
- Sistema registra `CC_SYNC_DUPLICATE_CODE` em auditoria
- Sistema move mensagem para DLQ com prioridade HIGH
- Sistema notifica admin: "Conflito de CodigoERP 1000. Registro duplicado no ERP ou mapping incorreto."
- Fluxo termina sem processar, requer investigação manual

**EX05 - Worker de Processamento Crashou (Dead Letter Queue)**:
- Passo 18: Worker lança exceção não tratada (ex: NullReferenceException, OutOfMemoryException)
- Azure Service Bus detecta falha após timeout de 30s
- Service Bus incrementa `DeliveryCount` da mensagem
- Se `DeliveryCount` > 5: Service Bus move automaticamente para DLQ
- Sistema Hangfire job `MonitorDlqJob` (executa a cada 5 min) detecta mensagens na DLQ
- Job notifica admin com detalhes do erro e payload da mensagem
- Fluxo termina com mensagem aguardando retry manual ou correção de bug

### 7. Pós-condições

- Centro de Custo sincronizado entre ERP e IControlIT com integridade garantida
- MessageId registrado em `IntegrationAudit` e cache Redis para deduplicação
- Assinatura HMAC validada, prevenindo webhooks falsos
- Dados transformados e validados contra JSON Schema antes de persistir
- Auditoria completa com payload original, resultado e tempo de execução
- Dashboard de integrações atualizado em tempo real via SignalR
- Conflitos de concorrência resolvidos automaticamente com estratégia Last Write Wins

### 8. Regras de Negócio Aplicáveis

- RN-ERP-078-01: Sincronização de Centros de Custo deve ser bidirecional
- RN-ERP-078-03: Integrações com falha devem registrar na Dead Letter Queue e notificar administrador
- RN-ERP-078-05: Cada mensagem integrada deve ter identificador único (UUID) para deduplicação
- RN-ERP-078-06: Transformação de dados deve validar schema e tipo de campo antes de processar
- RN-ERP-078-07: Logs de integração devem registrar entrada, saída e erro em tabela estruturada com retenção de 7 anos
- RN-ERP-078-08: Webhooks de ERP devem validar assinatura HMAC-SHA256 antes de processar

---

## UC03: Exportar Custos de TI para Contabilização no ERP

### 1. Descrição

Exporta custos de serviços de TI (telefonia, ativos, contratos) agrupados por Centro de Custo para contabilização no ERP (SAP, TOTVS, Oracle), validando período contábil aberto, mapeamento de Centros de Custo, e aplicando retry com backoff exponencial em caso de falha de comunicação.

### 2. Atores

- Gerente Financeiro (role: GERENTE_FINANCEIRO)
- Sistema IControlIT
- ERP (SAP/TOTVS/Oracle) receptor de lançamentos contábeis
- Azure Service Bus (processamento assíncrono)

### 3. Pré-condições

- Usuário autenticado com permissão `integracao:export_custos`
- Integração com ERP ativa e configurada (UC01 concluído)
- Período contábil (mês/ano) aberto no ERP para receber lançamentos
- Centros de Custo mapeados com CodigoERP preenchido
- Custos de TI calculados e consolidados no período (RF032 - Notas Fiscais processadas)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/financeiro/exportacao-custos` | - |
| 2 | - | Valida permissão RBAC `integracao:export_custos` |
| 3 | - | Exibe formulário com campos: Mês (dropdown 1-12), Ano (input number), ERP Destino (SAP/TOTVS/ORACLE) |
| 4 | Seleciona Mês=12, Ano=2025, ERP="SAP" | - |
| 5 | Clica em "Visualizar Prévia" | - |
| 6 | - | **Executa GetPreviewCustosQuery** com filtros: Mes=12, Ano=2025, ClienteId=CurrentClienteId |
| 7 | - | **Query SQL agrupa custos** por Centro de Custo: `SELECT IdCentroCusto, SUM(Valor) FROM Custos WHERE MONTH(Periodo)=12 AND YEAR(Periodo)=2025 GROUP BY IdCentroCusto` |
| 8 | - | **Para cada Centro de Custo**: Busca CodigoERP, Descricao, valida se CodigoERP está preenchido |
| 9 | - | Exibe tabela prévia: Coluna 1=Centro de Custo (Nome), Coluna 2=Código ERP, Coluna 3=Total Custo, Coluna 4=Status (Mapeado/Sem Mapeamento) |
| 10 | - | Identifica Centros de Custo sem CodigoERP: exibe alerta amarelo "3 centros de custo sem mapeamento ERP serão ignorados" com link para tela de configuração |
| 11 | - | Calcula totais: Total Geral=R$ 150.000,00, Total Exportável=R$ 145.000,00 (excluindo não mapeados), Total Ignorado=R$ 5.000,00 |
| 12 | Revisa prévia e clica em "Exportar para SAP" | - |
| 13 | - | **Executa ExportCostosToErpCommand** com parâmetros: Mes=12, Ano=2025, NomeErp="SAP", ClienteId=CurrentClienteId |
| 14 | - | **Valida se período está aberto no ERP**: Chama `IErpClient.ValidarPeriodoAberto(12, 2025)` via RFC ou REST API |
| 15 | - | ERP retorna: `{"periodoAberto": true, "periodoFiscal": "012.2025", "dataFechamento": null}` |
| 16 | - | **Agrupa custos por Centro de Custo** novamente (mesma query do passo 7) |
| 17 | - | **Para cada Centro de Custo mapeado** (onde CodigoERP IS NOT NULL): |
| 18 | - | Centro de Custo "TI-INFRAESTRUTURA" (CodigoERP="1000"): Total=R$ 50.000,00 |
| 19 | - | **Prepara payload SAP RFC** para BAPI_ACC_DOCUMENT_POST: `{"ACCOUNTGL": "600100", "COSTCENTER": "1000", "AMT_DOCCUR": 50000.00, "CURRENCY": "BRL", "DOC_DATE": "2025-12-31", "PSTNG_DATE": "2025-12-31", "REF_DOC_NO": "ICONTROLIT_122025_1000"}` |
| 20 | - | **Gera MessageId único**: `messageId = Guid.NewGuid().ToString()` |
| 21 | - | **Publica mensagem no Azure Service Bus** fila `erp-export-custos` com payload + messageId |
| 22 | - | **Worker processa mensagem** (ExportCustosWorker) |
| 23 | - | **Executa chamada RFC com retry**: Tenta enviar para SAP usando NCo (SAP .NET Connector) |
| 24 | - | **Retry logic**: Tentativa 1 → Falha (timeout) → Aguarda 2s → Tentativa 2 → Falha (conexão recusada) → Aguarda 4s → Tentativa 3 → **Sucesso** |
| 25 | - | SAP retorna: `{"SUCCESS": true, "DOCUMENT_NO": "5100000123", "FISCAL_YEAR": "2025"}` |
| 26 | - | **Atualiza registro de Custo** no IControlIT: marca como ExportadoParaERP=true, NumeroDocumentoERP="5100000123", DataExportacao=UtcNow |
| 27 | - | **Registra em IntegrationAudit**: MessageId, TipoIntegracao="EXPORT_CUSTOS", DirecaoFluxo="OUTBOUND", StatusExecucao="SUCESSO", DadosEntrada=payload, DadosSaida=resposta SAP, TempoExecucao_ms=1800 |
| 28 | - | **Marca MessageId como processado** em cache Redis |
| 29 | - | **Repete passos 18-28** para todos os Centros de Custo mapeados |
| 30 | - | **Ao finalizar todos**: Envia notificação ao usuário via SignalR: "Exportação concluída: 10 centros de custo, R$ 145.000,00 exportados com sucesso" |
| 31 | - | **Envia email de confirmação** para Gerente Financeiro com resumo e link para visualizar auditoria |
| 32 | - | Atualiza dashboard de integrações com última exportação: "Última exportação: 29/12/2025 15:30 - 10 CCs - R$ 145.000,00" |

### 5. Fluxos Alternativos

**FA01 - Período Contábil Fechado no ERP**:
- Passo 15: ERP retorna `{"periodoAberto": false, "periodoFiscal": "012.2025", "dataFechamento": "2025-12-20"}`
- Sistema detecta período fechado
- Sistema registra `EXPORT_PERIODO_FECHADO` em auditoria
- Sistema retorna HTTP 400 Bad Request com mensagem i18n: "integracao.validacao.periodo_fechado" → "Período 12/2025 está fechado no ERP desde 20/12/2025. Não é possível exportar custos."
- Sistema exibe modal com opção: "Escolher outro período" (volta ao passo 4) OU "Solicitar reabertura ao ERP" (envia ticket automático para equipe contábil)
- Fluxo termina sem exportar

**FA02 - Centro de Custo Sem Mapeamento ERP (Ignorado)**:
- Passo 17: Sistema encontra Centro de Custo "TI-TEMPORÁRIO" com CodigoERP=NULL e Total=R$ 5.000,00
- Sistema pula este centro de custo (não exporta)
- Sistema registra em auditoria: `EXPORT_CUSTO_SKIP`, Motivo="Centro de Custo sem CodigoERP", Valor=5000.00
- Sistema incrementa contador `custos_nao_exportados_total` métrica
- Sistema continua exportando outros centros de custo
- Ao final (passo 30): Notificação inclui aviso: "3 centros de custo ignorados (R$ 5.000,00) por falta de mapeamento"
- Fluxo continua normalmente para centros mapeados

**FA03 - Falha de Comunicação com ERP Após 5 Retries (Dead Letter Queue)**:
- Passo 24: Todas as 5 tentativas falham (timeouts: 2s, 4s, 8s, 16s, 32s)
- Sistema registra `EXPORT_CUSTO_FAILED` em IntegrationAudit com detalhes de erro
- Sistema move mensagem para Dead Letter Queue do Service Bus
- Sistema envia alerta crítico para admin: "Falha ao exportar custos do Centro de Custo 1000 (R$ 50.000,00) após 5 tentativas. Verificar DLQ."
- Sistema incrementa métrica `integ_failures_total{tipo="export_custos"}`
- Sistema continua exportando outros centros de custo (falha isolada)
- Usuário pode reprocessar manualmente via tela `/admin/integracao/dlq`
- Fluxo continua com falha parcial

**FA04 - SAP Retorna Erro de Validação (Conta Contábil Inválida)**:
- Passo 25: SAP retorna erro: `{"SUCCESS": false, "ERROR_CODE": "GL_ACCOUNT_NOT_FOUND", "MESSAGE": "Conta contábil 600100 não existe"}`
- Sistema detecta erro de negócio (não é falha de rede, não faz retry)
- Sistema registra `EXPORT_CUSTO_VALIDATION_ERROR` em auditoria com erro completo
- Sistema marca exportação como FALHA_VALIDACAO (diferente de FALHA_TECNICA)
- Sistema notifica admin via alerta: "Exportação falhou: Conta contábil 600100 inválida no SAP. Verificar mapeamento de contas."
- Sistema pula este centro de custo e continua com próximos
- Ao final: Resumo inclui "1 erro de validação - verificar logs"
- Fluxo continua com falha parcial registrada

**FA05 - Exportação Parcial (Alguns Centros de Custo com Sucesso, Outros com Falha)**:
- Após processar todos os centros de custo: 7 sucesso, 2 falha (DLQ), 1 erro validação
- Sistema calcula estatísticas: Taxa de sucesso=70%, Total exportado=R$ 100.000,00, Total com falha=R$ 45.000,00
- Sistema envia notificação: "Exportação concluída com ressalvas: 7/10 centros exportados com sucesso. 3 com falha - verificar DLQ e logs."
- Sistema marca job como PARCIALMENTE_CONCLUIDO
- Sistema agenda retry automático para falhas (Hangfire job em 1h)
- Fluxo termina com conclusão parcial

### 6. Exceções

**EX01 - Usuário Sem Permissão export_custos**:
- Passo 2: Validação RBAC falha
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem i18n: "permissoes.acesso_negado_export_custos"
- Fluxo termina imediatamente

**EX02 - Nenhum Custo Encontrado para o Período**:
- Passo 7: Query retorna 0 registros (período sem movimentação)
- Sistema retorna HTTP 404 Not Found
- Frontend exibe modal: "Nenhum custo encontrado para 12/2025. Verifique se faturas foram importadas."
- Sistema registra `EXPORT_CUSTOS_EMPTY_PERIOD` em auditoria
- Fluxo termina sem exportar

**EX03 - Azure Service Bus Indisponível (Exportação Síncrona Fallback)**:
- Passo 21: Tentativa de publicar na fila retorna erro 503
- Sistema detecta falha do Service Bus
- Sistema entra em modo fallback: executa exportação **síncrona** diretamente no thread da request
- Sistema exibe alerta ao usuário: "Fila de processamento indisponível. Exportação será processada de forma síncrona (pode demorar)."
- Sistema executa passos 22-27 diretamente sem fila
- Sistema registra `EXPORT_SYNC_FALLBACK` em auditoria
- Fluxo continua com modo degradado (mais lento, bloqueia thread)

**EX04 - Credenciais ERP Expiradas ou Inválidas**:
- Passo 23: Tentativa de autenticação RFC retorna erro "AUTHORIZATION_FAILURE"
- Sistema detecta credencial expirada
- Sistema registra `ERP_AUTH_FAILURE` em auditoria
- Sistema envia alerta crítico para admin: "Credenciais SAP expiradas. Rotacionar via Key Vault."
- Sistema move todas as mensagens pendentes para DLQ
- Sistema marca integração como "Desabilitada Automaticamente (Auth Failure)"
- Fluxo termina com erro crítico que bloqueia exportações futuras até correção

**EX05 - Dados Sensíveis no Payload (Criptografia Obrigatória)**:
- Passo 19: Sistema detecta que payload contém valores > R$ 1.000.000,00 (dado sensível)
- Sistema aplica criptografia AES-256 no campo `AMT_DOCCUR` antes de registrar em IntegrationAudit
- Sistema salva em campo criptografado: `DadosEntrada_Encrypted` ao invés de `DadosEntrada`
- Sistema registra chave de criptografia no Key Vault com versionamento
- Sistema marca registro com flag `HasSensitiveData=true`
- Fluxo continua com dados criptografados em repouso

### 7. Pós-condições

- Custos de TI exportados para ERP e contabilizados em centros de custo corretos
- Período contábil validado como aberto antes de exportar
- Centros de Custo sem mapeamento ignorados com registro em auditoria
- Retry com backoff exponencial executado em caso de falha transiente
- Falhas movidas para Dead Letter Queue com notificação para admin
- Auditoria completa com payload enviado, resposta recebida e tempo de execução
- Métricas de sucesso/falha atualizadas para dashboard
- Registros de Custo marcados com NumeroDocumentoERP retornado pelo ERP

### 8. Regras de Negócio Aplicáveis

- RN-ERP-078-03: Integrações com falha devem registrar na Dead Letter Queue e notificar administrador
- RN-ERP-078-04: Exportação de custos de TI para ERP deve respeitar centro de custo e período contábil
- RN-ERP-078-05: Cada mensagem integrada deve ter identificador único (UUID) para deduplicação
- RN-ERP-078-07: Logs de integração devem registrar entrada, saída e erro em tabela estruturada com retenção de 7 anos
- RN-ERP-078-09: Dados sensíveis (salários, valores de contrato) devem ser criptografados em campo específico na auditoria

---

## UC04: Reconciliar Faturas Telecom com Contas a Pagar do ERP

### 1. Descrição

Executa matching automático entre faturas de telecom processadas no IControlIT (RF032) e contas a pagar importadas do ERP, aplicando tolerância de diferença de 0,5% para variações cambiais e juros, e notificando o financeiro sobre pendências que requerem reconciliação manual.

### 2. Atores

- Sistema IControlIT (processamento automático via job)
- ERP (SAP/TOTVS/Oracle) fonte de contas a pagar
- Analista Financeiro (reconciliação manual de divergências)
- Hangfire Job Scheduler

### 3. Pré-condições

- Integração com ERP ativa com importação de contas a pagar habilitada
- Faturas de telecom processadas e importadas em IControlIT (Status=PENDENTE_RECONCILIACAO)
- Contas a pagar importadas do ERP com CNPJ fornecedor, data vencimento e valor
- Job agendado no Hangfire para executar diariamente às 22h (após importação de faturas do dia)
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | **Hangfire executa job agendado** `ReconciliacaoAutomaticaJob` às 22:00 UTC |
| 2 | - | **Query busca faturas não reconciliadas**: `SELECT * FROM Faturas WHERE StatusReconciliacao = 'PENDENTE_RECONCILIACAO' AND ClienteId = @ClienteId` |
| 3 | - | Retorna 50 faturas pendentes (ex: Fatura #1001 - Fornecedor CNPJ=12.345.678/0001-99, Valor=R$ 1.000,00, Vencimento=2025-12-15) |
| 4 | - | **Para cada fatura**: Busca contas a pagar no ERP importadas no período ±7 dias do vencimento |
| 5 | - | **Query SQL**: `SELECT * FROM ContasPagarERP WHERE CNPJ = '12345678000199' AND DataVencimento BETWEEN '2025-12-08' AND '2025-12-22' AND ClienteId = @ClienteId` |
| 6 | - | Retorna 2 contas a pagar: Conta #5001 (Valor=R$ 1.004,50, Vencimento=2025-12-15), Conta #5002 (Valor=R$ 1.050,00, Vencimento=2025-12-16) |
| 7 | - | **Para Conta #5001**: Calcula diferença absoluta: `diferenca = |1000.00 - 1004.50| = 4.50` |
| 8 | - | Calcula percentual de diferença: `percentual = (4.50 / 1000.00) * 100 = 0.45%` |
| 9 | - | **Verifica tolerância**: `0.45% <= 0.5%` → **Match encontrado** |
| 10 | - | **Executa ReconcileFaturaCommand** com IdFatura=1001, IdContaPagarERP=5001 |
| 11 | - | **Atualiza Fatura**: `UPDATE Faturas SET StatusReconciliacao='RECONCILIADO', IdContaPagarERP=5001, DiferencaReconciliacao=4.50, PercentualDiferenca=0.45, DataReconciliacao=GETUTCDATE() WHERE Id=1001` |
| 12 | - | **Registra em IntegrationAudit**: MessageId=UUID, TipoIntegracao="RECONCILIACAO_FATURA", StatusExecucao="SUCESSO", DadosEntrada=`{"faturaId":1001,"valor":1000.00}`, DadosSaida=`{"contaPagarId":5001,"diferenca":4.50}` |
| 13 | - | **Para Conta #5002**: Calcula diferença: `|1000.00 - 1050.00| = 50.00`, Percentual: `(50.00/1000.00)*100 = 5.0%` |
| 14 | - | **Verifica tolerância**: `5.0% > 0.5%` → **Não reconcilia automaticamente** |
| 15 | - | **Marca fatura como REQUER_MANUAL**: `UPDATE Faturas SET StatusReconciliacao='REQUER_MANUAL', MotivoManual='Diferença de 5.0% excede tolerância de 0.5%' WHERE Id=1001` |
| 16 | - | **Registra em IntegrationAudit**: StatusExecucao="MANUAL_REQUERIDO", DadosSaida=`{"motivo":"Diferença fora da tolerância"}` |
| 17 | - | **Publica evento de domínio** `FaturaRequerManualEvent` para notificar financeiro |
| 18 | - | **Handler consome evento**: Envia email para Analista Financeiro com lista de faturas pendentes de reconciliação manual |
| 19 | - | Email contém: Número Fatura, Fornecedor, Valor Fatura, Valor Conta a Pagar, Diferença, Percentual, Link direto para tela de reconciliação manual |
| 20 | - | **Ao final do job**: Calcula estatísticas: 40 reconciliadas automaticamente (80%), 10 requerem manual (20%) |
| 21 | - | **Registra métrica no Prometheus**: `faturas_reconciliadas_total{status="auto"}` = 40, `faturas_reconciliadas_total{status="manual"}` = 10 |
| 22 | - | **Atualiza dashboard**: Exibe "Última reconciliação: 29/12/2025 22:15 - 40 auto, 10 manual" |
| 23 | - | **Envia notificação resumo** via SignalR para grupo `FinanceiroTeam`: "Reconciliação concluída: 80% automática" |

### 5. Fluxos Alternativos

**FA01 - Múltiplas Contas a Pagar Correspondentes (Ambiguidade)**:
- Passo 6: Query retorna 3 contas a pagar com valores próximos: R$ 1.001,00 (0,1%), R$ 1.004,50 (0,45%), R$ 1.005,00 (0,5%)
- Sistema identifica múltiplos matches dentro da tolerância
- Sistema aplica critério de desempate: **Match com menor diferença absoluta vence**
- Sistema escolhe Conta #5001 (R$ 1.001,00, diferença=R$ 1,00, percentual=0,1%)
- Sistema reconcilia com a conta mais próxima
- Sistema registra em auditoria: `RECONCILIACAO_MULTIPLOS_MATCHES`, DadosSaida=`{"contas_candidatas": [5001, 5003, 5004], "escolhida": 5001, "criterio": "menor_diferenca"}`
- Retorna ao passo 10 com conta selecionada

**FA02 - Nenhuma Conta a Pagar Encontrada (Sem Match)**:
- Passo 6: Query retorna 0 contas a pagar (CNPJ não encontrado OU período não coincide)
- Sistema marca fatura como `SEM_MATCH_ERP`
- Sistema registra em auditoria: `RECONCILIACAO_NO_MATCH`, Motivo="Nenhuma conta a pagar encontrada no ERP para CNPJ 12.345.678/0001-99 no período"
- Sistema publica evento `FaturaSemMatchEvent`
- Handler envia notificação para Analista Financeiro: "Fatura #1001 sem correspondência no ERP. Verificar se conta a pagar foi lançada."
- Sistema incrementa métrica `faturas_sem_match_total`
- Fluxo continua com próxima fatura

**FA03 - Reconciliação Manual Executada pelo Analista**:
- Analista acessa tela `/financeiro/reconciliacao/pendentes`
- Sistema exibe lista de faturas com `StatusReconciliacao='REQUER_MANUAL'` OU `SEM_MATCH_ERP`
- Analista seleciona Fatura #1001 e Conta a Pagar #5002 manualmente
- Analista justifica diferença: "Variação cambial + IOF"
- Clica em "Reconciliar Manualmente"
- Sistema executa `ReconcileManualCommand` com IdFatura=1001, IdContaPagarERP=5002, Justificativa="Variação cambial + IOF", UsuarioId=CurrentUser
- Sistema atualiza Fatura: `StatusReconciliacao='RECONCILIADO_MANUAL'`, `IdContaPagarERP=5002`, `JustificativaManual="..."`, `ReconciliadoPor=UsuarioId`, `DataReconciliacao=UtcNow`
- Sistema registra em auditoria: `RECONCILIACAO_MANUAL`, DadosEntrada=payload, UsuarioExecucao=CurrentUser
- Sistema envia confirmação via toast: "Fatura reconciliada manualmente com sucesso"
- Fluxo termina com reconciliação manual concluída

**FA04 - Fatura Já Reconciliada (Deduplicação)**:
- Passo 2: Job encontra fatura com `StatusReconciliacao='RECONCILIADO'` (já processada anteriormente)
- Sistema pula esta fatura sem reprocessar
- Sistema registra métrica `faturas_ja_reconciliadas_skip_total`
- Sistema continua com próxima fatura
- Fluxo continua normalmente

**FA05 - Importação de Contas a Pagar Atrasada (Sem Dados Recentes)**:
- Passo 6: Sistema detecta que última importação de contas a pagar foi há >24h (verificando tabela `LastImportTimestamp`)
- Sistema identifica risco: reconciliação pode estar incompleta por falta de dados atualizados
- Sistema envia alerta para admin: "Importação de contas a pagar do ERP atrasada. Última importação: 28/12/2025. Reconciliação pode estar incompleta."
- Sistema marca job como `EXECUTED_WITH_WARNING`
- Sistema registra métrica `import_contas_pagar_atraso_hours` = 36
- Sistema continua reconciliação com dados disponíveis (pode ter falsos negativos)
- Fluxo continua com aviso registrado

### 6. Exceções

**EX01 - Job Hangfire Falha com Exceção Não Tratada**:
- Passo 4: Query lança SqlException (timeout, conexão perdida)
- Hangfire detecta exceção e marca job como FAILED
- Hangfire agenda retry automático em 15 min (retry policy configurado)
- Sistema registra erro em logs estruturados com stack trace
- Sistema envia alerta para admin: "Job ReconciliacaoAutomaticaJob falhou às 22:00. Retry agendado para 22:15."
- Se falhar 3x consecutivas: Sistema escalona alerta para CRÍTICO
- Fluxo termina com retry agendado

**EX02 - Diferença Negativa Detectada (Possível Fraude)**:
- Passo 8: Conta a pagar tem valor R$ 800,00 vs Fatura R$ 1.000,00 (diferença negativa de R$ 200,00)
- Sistema detecta que conta a pagar é **menor** que fatura (incomum)
- Sistema marca como `POSSIVEL_FRAUDE`
- Sistema registra alerta de segurança: `RECONCILIACAO_VALOR_SUSPEITO`, Severidade=HIGH
- Sistema envia notificação para Gerente Financeiro e Compliance: "Divergência suspeita detectada: Fatura R$ 1.000 vs Conta a Pagar R$ 800 (20% a menos)"
- Sistema bloqueia reconciliação automática desta fatura
- Sistema exige reconciliação manual com dupla aprovação
- Fluxo termina com bloqueio de segurança

**EX03 - CNPJ da Fatura Não Bate com CNPJ da Conta a Pagar**:
- Passo 6: Query por CNPJ retorna 0 resultados, mas há conta a pagar com valor exato no período
- Sistema detecta potencial erro de cadastro de CNPJ
- Sistema registra `RECONCILIACAO_CNPJ_MISMATCH`
- Sistema sugere match alternativo: "Conta a pagar #5001 tem valor exato R$ 1.000,00 mas CNPJ divergente (12.345.678/0002-10 vs 12.345.678/0001-99)"
- Sistema envia alerta para Analista Financeiro: "Possível erro de cadastro de CNPJ. Verificar manualmente."
- Sistema marca fatura como `SEM_MATCH_ERP` (não reconcilia automaticamente por segurança)
- Fluxo termina com pendência manual

**EX04 - Conta a Pagar Já Reconciliada com Outra Fatura (Violação de Integridade)**:
- Passo 10: Tentativa de atualizar fatura com IdContaPagarERP=5001 que já está vinculado à Fatura #999
- Sistema detecta violação de constraint UNIQUE em `Faturas.IdContaPagarERP`
- Sistema lança exceção `DuplicateReconciliationException`
- Sistema registra erro em auditoria: `RECONCILIACAO_DUPLICATE_CONTA_PAGAR`
- Sistema envia alerta crítico: "Tentativa de reconciliar Conta a Pagar #5001 com 2 faturas distintas. Investigar."
- Sistema marca ambas as faturas como `CONFLITO_RECONCILIACAO`
- Fluxo termina com erro crítico, exige investigação manual

**EX05 - Multi-Tenancy Violado (Tentativa de Reconciliar Fatura de Outro Cliente)**:
- Passo 6: Query inclui filtro `AND ClienteId = @ClienteId` mas por bug retorna conta a pagar de outro cliente
- Sistema aplica validação secundária: verifica `fatura.ClienteId == contaPagar.ClienteId` antes de reconciliar
- Se violação detectada: Sistema lança `SecurityException`
- Sistema registra em log de segurança: `RECONCILIACAO_SECURITY_VIOLATION`, Severidade=CRITICAL
- Sistema bloqueia job imediatamente
- Sistema envia alerta de segurança para equipe técnica
- Fluxo termina com bloqueio de segurança, exige correção de bug

### 7. Pós-condições

- Faturas reconciliadas automaticamente marcadas com IdContaPagarERP, DataReconciliacao e DiferencaReconciliacao
- Faturas fora da tolerância marcadas como REQUER_MANUAL com motivo detalhado
- Analista Financeiro notificado sobre pendências de reconciliação manual
- Auditoria completa com matching executado, diferenças calculadas e tempo de execução
- Dashboard atualizado com taxa de reconciliação automática vs manual
- Métricas de negócio atualizadas (faturas_reconciliadas_total, faturas_sem_match_total)

### 8. Regras de Negócio Aplicáveis

- RN-ERP-078-07: Logs de integração devem registrar entrada, saída e erro em tabela estruturada com retenção de 7 anos
- RN-ERP-078-10: Reconciliação de faturas telecom com contas a pagar do ERP deve considerar tolerância de diferença de 0,5%

---

## UC05: Dashboard de Integrações em Tempo Real

### 1. Descrição

Exibe painel consolidado com status de todas as integrações ERP (SAP, TOTVS, Oracle), últimas sincronizações, mensagens em fila, erros na Dead Letter Queue, e logs de auditoria com filtros avançados, atualizando em tempo real via SignalR quando eventos de integração ocorrem.

### 2. Atores

- Administrador de Integrações (role: ADMIN_INTEGRACAO)
- Gerente de TI (role: GERENTE_TI)
- Sistema IControlIT
- SignalR Hub (IntegrationHub)

### 3. Pré-condições

- Usuário autenticado com permissão `integracao:leitura`
- Pelo menos uma integração ERP configurada (UC01)
- Azure Service Bus configurado com filas de mensagens
- SignalR Hub ativo no backend
- Multi-tenancy ativo (ClienteId válido)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa tela `/dashboard/integracoes` | - |
| 2 | - | Valida permissão RBAC `integracao:leitura` |
| 3 | - | **Conecta ao SignalR Hub**: `await _hubConnection.StartAsync()`, `await _hubConnection.InvokeAsync("JoinGroup", "IntegrationAdmins")` |
| 4 | - | **Executa GetIntegrationStatusQuery** para buscar status de todas integrações |
| 5 | - | **Query busca dados agregados**: 1) Última sincronização por tipo (SAP, TOTVS, ORACLE), 2) Mensagens em fila (Service Bus), 3) Mensagens em DLQ, 4) Taxa de sucesso últimas 24h |
| 6 | - | **Para SAP**: Retorna `{"nomeErp":"SAP", "status":"Ativo", "ultimaSincronizacao":"2025-12-29T14:30:00Z", "mensagensFila":5, "mensagensDLQ":2, "taxaSucesso24h":98.5}` |
| 7 | - | **Para TOTVS**: Retorna `{"nomeErp":"TOTVS", "status":"Inativo", "ultimaSincronizacao":"2025-12-28T10:00:00Z", "mensagensFila":0, "mensagensDLQ":0, "taxaSucesso24h":0}` |
| 8 | - | **Para ORACLE**: Retorna `{"nomeErp":"ORACLE", "status":"Erro", "ultimaSincronizacao":"2025-12-29T12:00:00Z", "mensagensFila":120, "mensagensDLQ":15, "taxaSucesso24h":75.0, "ultimoErro":"Connection timeout"}` |
| 9 | - | **Renderiza cards de status** com cores: Verde (Ativo, taxaSucesso>95%), Amarelo (Ativo, taxa 80-95%), Vermelho (Erro ou Inativo), Cinza (Nunca configurado) |
| 10 | - | Card SAP: Badge verde "Ativo", texto "Última sincronização: há 15 min", ícone warning laranja "2 mensagens em DLQ" |
| 11 | - | Card TOTVS: Badge cinza "Inativo", texto "Última sincronização: há 2 dias" |
| 12 | - | Card ORACLE: Badge vermelho "Erro", texto "Connection timeout", ícone crítico "15 mensagens em DLQ", "120 mensagens aguardando" |
| 13 | - | **Renderiza seção "Logs Recentes"**: Busca últimos 50 registros de IntegrationAudit ordenados por DataHora DESC |
| 14 | - | Exibe tabela com colunas: Timestamp, Tipo Integração, ERP, Status (badge colorido), Tempo Execução, Botão "Detalhes" |
| 15 | Clica em filtro "Mostrar apenas erros" | - |
| 16 | - | **Filtra query**: `WHERE StatusExecucao IN ('ERRO', 'DLQ', 'MANUAL_REQUERIDO')` |
| 17 | - | Atualiza tabela mostrando apenas 8 registros de erro |
| 18 | Clica em "Detalhes" de um log específico (MessageId=abc-123) | - |
| 19 | - | **Executa GetIntegrationLogDetailsQuery** com MessageId="abc-123" |
| 20 | - | Retorna registro completo: TipoIntegracao, DirecaoFluxo, DadosEntrada (JSON), DadosSaida (JSON), MensagemErro, TempoExecucao_ms, UsuarioExecucao |
| 21 | - | Abre modal com JSON formatado (syntax highlight), detalhes do erro, botão "Reprocessar" (se DLQ), botão "Copiar MessageId" |
| 22 | **Enquanto usuário visualiza dashboard**: Evento de integração ocorre (novo webhook recebido do SAP) | - |
| 23 | - | **Backend processa webhook** (UC02) e ao final publica evento SignalR: `await _hub.Clients.Group("IntegrationAdmins").SendAsync("IntegrationStatusUpdated", integrationStatusDto)` |
| 24 | - | **Frontend recebe evento via SignalR**: `_hubConnection.On<IntegrationStatusDto>("IntegrationStatusUpdated", (status) => { atualizarDashboard(status); })` |
| 25 | - | **Dashboard atualiza em tempo real SEM refresh**: Card SAP atualiza "Última sincronização: agora", contador mensagensFila decrementa de 5 para 4 |
| 26 | - | **Animação visual**: Card SAP pulsa em verde por 2s para indicar nova sincronização |
| 27 | - | **Toast não-intrusivo** no canto superior direito: "Nova sincronização SAP concluída com sucesso" (auto-hide em 5s) |
| 28 | Clica em botão "Exportar Logs" | - |
| 29 | - | **Executa ExportIntegrationLogsCommand** com filtros aplicados (datas, tipo, status) |
| 30 | - | Gera arquivo CSV com todos os logs filtrados (máximo 10.000 registros) |
| 31 | - | Download inicia automaticamente: `integration_logs_2025-12-29.csv` |
| 32 | - | Sistema registra auditoria: `LOGS_EXPORTADOS`, UsuarioExecucao=CurrentUser, QuantidadeRegistros=150 |

### 5. Fluxos Alternativos

**FA01 - Alerta Crítico de DLQ Crescendo**:
- Passo 8: Sistema detecta que mensagens em DLQ do ORACLE passaram de 10 para 15 em última verificação
- Sistema dispara alerta crítico (métrica `dlq_threshold_exceeded`)
- Dashboard exibe banner vermelho no topo: "⚠️ ALERTA CRÍTICO: DLQ ORACLE crescendo (15 mensagens). Investigar imediatamente."
- Banner tem botão "Ver DLQ" que navega para `/admin/integracao/dlq?erp=ORACLE`
- Sistema envia notificação push para admin via SignalR
- Se admin não interage em 5 min: Sistema envia email automático para GERENTE_TI
- Fluxo continua com alerta exibido

**FA02 - Sincronização Manual Disparada pelo Dashboard**:
- Passo 10: Usuário clica em botão "Sincronizar Agora" no card SAP
- Sistema exibe modal de confirmação: "Forçar sincronização manual? Isso pode duplicar dados se sincronização automática estiver ativa."
- Usuário confirma
- Sistema executa `ForceSyncCommand` com NomeErp="SAP", TipoSync="CENTRO_CUSTO"
- Sistema publica mensagem no Service Bus fila `manual-sync` com prioridade HIGH
- Worker processa mensagem imediatamente (fura fila)
- Enquanto processa: Card SAP exibe spinner "Sincronizando..." com progress bar
- Ao concluir: SignalR notifica frontend, card atualiza "Sincronização manual concluída - 50 registros atualizados"
- Retorna ao passo 10 com card atualizado

**FA03 - Filtro Avançado de Logs por Período e Tipo**:
- Passo 15: Usuário clica em "Filtros Avançados"
- Sistema exibe painel com campos: Data Início, Data Fim, Tipo Integração (multi-select: SYNC_CC, EXPORT_CUSTOS, etc), ERP (SAP/TOTVS/ORACLE), Status (multi-select)
- Usuário seleciona: Data Início=2025-12-01, Data Fim=2025-12-29, Tipo=EXPORT_CUSTOS, Status=ERRO
- Clica em "Aplicar Filtros"
- Sistema executa query com filtros: `WHERE DataHora BETWEEN @Inicio AND @Fim AND TipoIntegracao='EXPORT_CUSTOS' AND StatusExecucao='ERRO'`
- Tabela atualiza mostrando 3 registros específicos
- URL atualiza com query params: `/dashboard/integracoes?inicio=2025-12-01&fim=2025-12-29&tipo=EXPORT_CUSTOS&status=ERRO` (shareable link)
- Retorna ao passo 14 com filtros aplicados

**FA04 - Reprocessar Mensagem da DLQ Direto do Dashboard**:
- Passo 21: Modal de detalhes do log mostra que mensagem está em DLQ (StatusExecucao='DLQ')
- Botão "Reprocessar" está habilitado (requer permissão `integracao:retry_dlq`)
- Usuário clica em "Reprocessar"
- Sistema exibe confirmação: "Reprocessar MessageId abc-123? Isso moverá a mensagem da DLQ de volta para fila principal."
- Usuário confirma com justificativa obrigatória: "Erro de conexão temporário resolvido"
- Sistema executa `RetryDlqMessageCommand` com MessageId="abc-123", Justificativa="...", UsuarioId=CurrentUser
- Sistema move mensagem de DLQ para fila principal do Service Bus
- Sistema registra auditoria: `DLQ_RETRY_MANUAL`, MessageId, UsuarioExecucao
- Modal fecha, dashboard atualiza contador DLQ de 2 para 1
- Toast confirma: "Mensagem movida para reprocessamento"
- Fluxo termina com mensagem reprocessada

**FA05 - Conexão SignalR Perdida (Reconexão Automática)**:
- Durante passo 25: Conexão SignalR cai por instabilidade de rede
- Frontend detecta desconexão via `_hubConnection.onclose`
- Sistema exibe banner amarelo: "Conexão perdida. Tentando reconectar..." com spinner
- Sistema tenta reconectar automaticamente com backoff exponencial: 2s, 4s, 8s, 16s
- Após 3ª tentativa: Conexão restabelecida
- Sistema re-executa `JoinGroup("IntegrationAdmins")`
- Sistema força atualização de dados: re-executa GetIntegrationStatusQuery para sincronizar estado
- Banner muda para verde: "Conexão restabelecida" (auto-hide em 3s)
- Dashboard volta a receber atualizações em tempo real
- Fluxo continua normalmente

### 6. Exceções

**EX01 - Usuário Sem Permissão integracao:leitura**:
- Passo 2: Validação RBAC falha
- Sistema retorna HTTP 403 Forbidden
- Frontend exibe mensagem i18n: "permissoes.acesso_negado_integracao_leitura"
- Fluxo termina imediatamente

**EX02 - Azure Service Bus Indisponível (Impossível Obter Contadores de Fila)**:
- Passo 5: Chamada ao Service Bus Management API timeout ou retorna 503
- Sistema detecta falha ao obter métricas de fila
- Sistema exibe contadores como "N/A" com ícone de aviso
- Sistema exibe tooltip: "Azure Service Bus temporariamente indisponível. Dados de fila não disponíveis."
- Sistema registra erro em logs: `SERVICE_BUS_METRICS_UNAVAILABLE`
- Dashboard continua exibindo outros dados (status, logs) que não dependem do Service Bus
- Fluxo continua com funcionalidade parcial

**EX03 - SignalR Hub Offline (Dashboard Funciona Apenas com Polling)**:
- Passo 3: Tentativa de conectar ao SignalR Hub falha (servidor SignalR offline)
- Sistema detecta falha de conexão
- Sistema entra em modo fallback: Ativa polling a cada 30s via HTTP requests
- Sistema exibe banner informativo: "Atualizações em tempo real indisponíveis. Dashboard atualizando a cada 30s."
- A cada 30s: Sistema executa GetIntegrationStatusQuery e atualiza UI
- Dashboard funciona mas sem atualizações instantâneas
- Fluxo continua com modo degradado

**EX04 - Exportação de Logs Excede Limite (>10.000 registros)**:
- Passo 30: Query filtrada retorna 25.000 registros (período muito amplo)
- Sistema detecta que resultado excede limite de 10.000 configurado
- Sistema exibe modal de erro: "Filtro retornou 25.000 registros. Limite máximo: 10.000. Refine os filtros de data ou tipo."
- Sistema sugere filtros mais restritivos: "Tente exportar por semana ao invés de mês inteiro"
- Sistema NÃO executa exportação parcial (poderia gerar dados incompletos)
- Usuário deve ajustar filtros e tentar novamente
- Fluxo termina sem exportar

**EX05 - Query de Auditoria Timeout (Tabela Muito Grande)**:
- Passo 13: Query `SELECT TOP 50 * FROM IntegrationAudit ORDER BY DataHora DESC` timeout após 30s (tabela com milhões de registros sem índice otimizado)
- Sistema detecta SqlException timeout
- Sistema exibe mensagem: "Timeout ao carregar logs. Aplicando filtros de data automaticamente."
- Sistema força filtro: Últimos 7 dias ao invés de "todos os registros"
- Sistema re-executa query com filtro temporal: `WHERE DataHora >= DATEADD(DAY, -7, GETUTCDATE())`
- Query retorna em 2s
- Dashboard exibe logs com nota: "Exibindo últimos 7 dias. Use filtros para períodos maiores."
- Fluxo continua com filtro temporal aplicado

### 7. Pós-condições

- Dashboard exibe status consolidado de todas as integrações ERP em tempo real
- Usuário notificado imediatamente sobre novas sincronizações, erros ou alertas via SignalR
- Logs de auditoria acessíveis com filtros avançados e export para CSV
- Mensagens em DLQ visíveis com opção de reprocessamento manual
- Métricas de desempenho (taxa de sucesso, tempo de execução) calculadas e exibidas
- Alertas críticos destacados visualmente com notificações push

### 8. Regras de Negócio Aplicáveis

- RN-ERP-078-07: Logs de integração devem registrar entrada, saída e erro em tabela estruturada com retenção de 7 anos

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-29 | Criação de 5 casos de uso para RF078 - Integração com ERPs | Claude Code |

---

**Última Atualização**: 2025-12-29
**Autor**: Claude Code (IControlIT Documentation Agent)
**Revisão**: Pendente de aprovação técnica

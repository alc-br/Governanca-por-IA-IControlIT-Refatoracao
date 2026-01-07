# UC-RF111 - Casos de Uso - Backup, Recuperação e Disaster Recovery

## UC01: Executar Backup Completo Automático com Criptografia AES-256

### 1. Descrição

Este caso de uso executa backup completo automático do banco de dados diariamente às 2h da manhã, com criptografia AES-256 e upload para Azure Blob Storage conforme RN-BCK-111-01 e RN-BCK-111-04.

### 2. Atores

- **Sistema**: IControlIT Backend, Hangfire, Azure Blob Storage, Azure Key Vault

### 3. Pré-condições

- Hangfire configurado e rodando
- Job `FullDatabaseBackupJob` agendado para 2h AM
- Azure Blob Storage acessível (container "backups")
- Azure Key Vault acessível com chave "backup-encryption-key"
- Feature Flag `BACKUP_AUTOMATED_BACKUP` habilitado
- Espaço em disco suficiente (mínimo 20% livre)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara job às 02:00:00 UTC |
| 2 | - | `FullDatabaseBackupJob.ExecuteAsync()` inicia |
| 3 | - | Verifica se backup anterior (do dia anterior) foi bem-sucedido |
| 4 | - | Se backup anterior falhou → Envia alerta e tenta novamente |
| 5 | - | Gera nome do backup: `Full_Backup_20251229_020000` |
| 6 | - | Executa comando SQL: `BACKUP DATABASE IControlIT TO DISK = '/temp/Full_Backup_20251229_020000.bak' WITH COMPRESSION, CHECKSUM` |
| 7 | - | Backup SQL completo em 45 minutos (banco de 150 GB → backup comprimido 75 GB) |
| 8 | - | Lê arquivo .bak gerado em `/temp/` |
| 9 | - | Calcula checksum SHA-256 do arquivo: `7f8e9d4a2b3c1e5f...` |
| 10 | - | Recupera chave de criptografia do Azure Key Vault: `GetKeyAsync("backup-encryption-key")` |
| 11 | - | Criptografa arquivo com AES-256 usando chave recuperada |
| 12 | - | Adiciona IV (initialization vector) ao início do arquivo criptografado |
| 13 | - | Faz upload para Azure Blob Storage: `backups/Full_Backup_20251229_020000.bak.enc` |
| 14 | - | Salva registro no banco: `Backups` table → Nome, Tipo=Full, Tamanho=75GB, Checksum, BlobPath, CreatedAt |
| 15 | - | Registra auditoria (código: `BACKUP_CREATE_MANUAL`) → BackupId, Nome, Tipo, Tamanho, Status=Sucesso, Duração=52min |
| 16 | - | Remove arquivo temporário `/temp/Full_Backup_20251229_020000.bak` |
| 17 | - | Envia notificação de sucesso para administrador via email/SMS |
| 18 | - | Loga: "Backup completo executado com sucesso em 52 minutos" |

### 5. Fluxos Alternativos

**FA01: Backup Anterior Falhou (Retry)**

- Passo 4: Backup anterior (do dia anterior) falhou
- Sistema envia alerta: "Backup anterior falhou, tentando novamente"
- Sistema executa novo backup full imediatamente
- Se bem-sucedido → Continua fluxo normal
- Se falha novamente → Alerta crítico enviado, job reagendado para 1 hora depois

**FA02: Backup Incremental no Lugar de Full (Alternativa)**

- Passo 6: Sistema detecta que já existe backup full recente (< 24 horas)
- Sistema executa backup incremental ao invés de full (economia de tempo/espaço)
- Backup incremental captura apenas dados alterados desde último backup
- Reduz tempo de execução de 52 min para ~10 min

### 6. Exceções

**EX01: Azure Blob Storage Indisponível**

- Passo 13: Sistema tenta fazer upload → Azure retorna erro 503 Service Unavailable
- Sistema loga erro: "Blob Storage indisponível durante upload de backup"
- Sistema armazena backup localmente em `/fallback-backups/`
- Sistema tenta upload novamente a cada 30 minutos (retry automático com Polly)
- Alerta enviado para administrador: "Backup criado, mas não enviado para cloud"

**EX02: Azure Key Vault Indisponível (Sem Chave de Criptografia)**

- Passo 10: Sistema tenta recuperar chave → Key Vault não acessível
- Sistema loga erro: "Key Vault indisponível, backup não pode ser criptografado"
- Sistema ABORTA backup (não armazena backup sem criptografia por segurança)
- Registra auditoria com Status=Falha, Motivo="Key Vault unavailable"
- Alerta crítico enviado: "Backup falhou - Key Vault indisponível"

**EX03: Espaço em Disco Insuficiente**

- Passo 6: SQL Server tenta criar backup → Erro "Disk space insufficient"
- Sistema detecta espaço em disco < 20% livre
- Sistema aborta backup
- Envia alerta crítico: "Backup falhou - Espaço em disco insuficiente (< 20%)"
- Administrador deve liberar espaço antes de próximo backup

### 7. Pós-condições

- Backup completo criado, criptografado e armazenado em Azure Blob Storage
- Registro em tabela `Backups` com checksum SHA-256
- Auditoria registrada em `BackupAuditLog`
- Arquivo temporário removido
- Notificação enviada para administrador
- Próximo backup agendado para 2h AM do dia seguinte

### 8. Regras de Negócio Aplicáveis

- **RN-BCK-111-01**: Backup Completo Diário em Horário de Baixa Demanda (2h AM)
- **RN-BCK-111-04**: Criptografia Obrigatória de Backups em AES-256
- **RN-BCK-111-05**: Validação de Integridade via Checksum SHA-256
- **RN-BCK-111-10**: Auditoria Obrigatória de Todos Backups e Restores

---

## UC02: Restaurar Backup com Validação de Integridade SHA-256

### 1. Descrição

Este caso de uso permite ao Administrador ou DBA restaurar banco de dados a partir de backup específico, com validação obrigatória de integridade via checksum SHA-256 conforme RN-BCK-111-05.

### 2. Atores

- **Usuário autenticado**: Administrador, DBA
- **Sistema**: IControlIT Backend, Azure Blob Storage, Azure Key Vault, SQL Server

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `backup:restore:execute`
- Pelo menos 1 backup disponível
- Azure Blob Storage acessível
- Azure Key Vault acessível (para descriptografia)
- Banco de dados destino não está em uso (conexões fechadas)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Administração → Backup → Restauração | - |
| 2 | - | Valida permissão `backup:restore:execute` |
| 3 | - | Executa `GET /api/backup` → Retorna lista de backups disponíveis |
| 4 | - | Exibe tabela com: Nome, Tipo (Full/Incremental/Differential), Tamanho, Data Criação, Data Expiração, Ações (Restaurar) |
| 5 | Seleciona backup: `Full_Backup_20251228_020000` (75 GB, criado em 2025-12-28 02:30:00) | - |
| 6 | Clica em "Restaurar" | - |
| 7 | - | Exibe modal de confirmação com campos: Banco de Dados Destino (dropdown), Validar Integridade (checkbox marcado por padrão), Confirmar Restauração (button) |
| 8 | Seleciona banco destino: `IControlIT_Restore` (banco vazio para teste) | - |
| 9 | Marca "Validar Integridade" (checkbox) | - |
| 10 | Clica em "Confirmar Restauração" | - |
| 11 | - | Executa `POST /api/backup/{id}/restaurar` com payload: `{ targetDatabase: "IControlIT_Restore", validateIntegrity: true }` |
| 12 | - | Sistema enfileira job Hangfire para processamento em background |
| 13 | - | Retorna HTTP 202 Accepted com JobId |
| 14 | Visualiza mensagem: "Restauração iniciada. Você será notificado quando concluir." | - |
| 15 | - | **Job Hangfire inicia**: Download backup do Blob Storage (75 GB → 15 minutos) |
| 16 | - | Descriptografa arquivo com chave do Key Vault (AES-256 → 5 minutos) |
| 17 | - | Calcula checksum SHA-256 do arquivo descriptografado: `7f8e9d4a2b3c1e5f...` |
| 18 | - | Compara com checksum armazenado no registro do backup |
| 19 | - | Checksums coincidem → Validação de integridade OK |
| 20 | - | Executa comando SQL: `RESTORE DATABASE IControlIT_Restore FROM DISK = '/temp/Full_Backup_20251228_020000.bak' WITH REPLACE, RECOVERY` |
| 21 | - | Restauração SQL completa em 90 minutos |
| 22 | - | Executa testes de validação pós-restauração: Verifica integridade referencial (FKs), índices, triggers |
| 23 | - | Registra auditoria (código: `BACKUP_RESTORE`) → BackupId, NomeBackup, BancoDestino, Status=Sucesso, Duração=110min |
| 24 | - | Envia notificação ao usuário via email/SMS: "Restauração concluída com sucesso" |
| 25 | Recebe notificação e acessa banco `IControlIT_Restore` para validação | - |

### 5. Fluxos Alternativos

**FA01: Restauração Point-in-Time (PITR)**

- Passo 7: Usuário marca checkbox "Restaurar para Data/Hora Específica"
- Sistema exibe campo de seleção de data/hora (últimos 7 dias)
- Usuário seleciona: `2025-12-28 14:30:00`
- Sistema restaura backup full + aplica transaction logs até data/hora especificada
- Permite recuperação de dados até momento exato antes de corrupção

**FA02: Restauração Sem Validação de Integridade (Rápida)**

- Passo 9: Usuário DESMARCA checkbox "Validar Integridade"
- Sistema pula passos 17-19 (não calcula checksum)
- Reduz tempo de restauração em ~10 minutos
- Útil para testes rápidos, NÃO recomendado para produção

### 6. Exceções

**EX01: Checksum Não Coincide (Backup Corrompido)**

- Passo 19: Checksum calculado = `3a1b2c5d...` ≠ Checksum armazenado = `7f8e9d4a...`
- Sistema loga erro: "Backup integrity check failed. Backup corrupted."
- Sistema ABORTA restauração (não prossegue para passo 20)
- Retorna HTTP 400 Bad Request com mensagem: "Backup corrompido. Checksum não coincide."
- Registra auditoria com Status=Falha, Motivo="Integrity check failed"
- Administrador deve investigar corrupção e usar outro backup

**EX02: Banco de Dados Destino Está em Uso**

- Passo 20: Sistema tenta executar RESTORE → SQL Server retorna erro "Database is in use"
- Sistema detecta que existem conexões ativas no banco destino
- Sistema ABORTA restauração
- Retorna HTTP 409 Conflict com mensagem: "Banco de dados destino está em uso. Feche todas as conexões e tente novamente."
- Administrador deve fechar conexões manualmente ou sistema pode forçar com `WITH REPLACE` (risco de perda de dados)

**EX03: Espaço em Disco Insuficiente para Restauração**

- Passo 20: SQL Server tenta restaurar → Erro "Insufficient disk space"
- Sistema detecta que espaço livre < tamanho do backup
- Sistema aborta restauração
- Retorna HTTP 507 Insufficient Storage
- Envia alerta crítico: "Restauração falhou - Espaço em disco insuficiente"

### 7. Pós-condições

- Banco de dados restaurado a partir do backup selecionado
- Integridade validada via checksum SHA-256
- Auditoria registrada em `BackupAuditLog`
- Notificação enviada ao usuário
- Banco de dados destino disponível para uso
- Arquivo temporário removido

### 8. Regras de Negócio Aplicáveis

- **RN-BCK-111-05**: Validação de Integridade via Checksum SHA-256
- **RN-BCK-111-07**: RTO (Recovery Time Objective) de 4 Horas
- **RN-BCK-111-10**: Auditoria Obrigatória de Todos Backups e Restores

---

## UC03: Executar Backup Incremental a Cada 6 Horas (RPO de 6h)

### 1. Descrição

Este caso de uso executa backup incremental automaticamente a cada 6 horas (00h, 6h, 12h, 18h), capturando apenas dados alterados desde o último backup para garantir RPO de 6 horas conforme RN-BCK-111-02 e RN-BCK-111-06.

### 2. Atores

- **Sistema**: IControlIT Backend, Hangfire, Azure Blob Storage

### 3. Pré-condições

- Hangfire configurado e rodando
- Jobs incrementais agendados para 00h, 6h, 12h, 18h
- Pelo menos 1 backup completo ou incremental anterior existe
- Azure Blob Storage acessível
- Feature Flag `BACKUP_AUTOMATED_BACKUP` habilitado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara job em um dos horários: 00:00, 06:00, 12:00 ou 18:00 UTC |
| 2 | - | `IncrementalBackupJob.ExecuteAsync()` inicia |
| 3 | - | Busca LSN (Log Sequence Number) do último backup de qualquer tipo |
| 4 | - | LSN encontrado: `0x00000123:00000abc:0001` (do último incremental às 12:00) |
| 5 | - | Gera nome do backup: `Incremental_Backup_20251229_180000` |
| 6 | - | Executa comando SQL: `BACKUP LOG IControlIT TO DISK = '/temp/Incremental_Backup_20251229_180000.trn' WITH COMPRESSION` |
| 7 | - | Backup incremental captura apenas transaction logs desde LSN `0x00000123:00000abc:0001` |
| 8 | - | Backup completo em 8 minutos (apenas 2.5 GB de logs) |
| 9 | - | Calcula checksum SHA-256: `9d3e4f5a6b7c8d9e...` |
| 10 | - | Criptografa com AES-256 |
| 11 | - | Faz upload para Blob Storage: `backups/Incremental_Backup_20251229_180000.trn.enc` |
| 12 | - | Salva registro no banco: Tipo=Incremental, Tamanho=2.5GB, SinceLsn=`0x00000123:00000abc:0001`, NextLsn=`0x00000124:00000def:0001` |
| 13 | - | Registra auditoria (código: `BACKUP_CREATE_MANUAL`) → Status=Sucesso, Duração=10min |
| 14 | - | Remove arquivo temporário |
| 15 | - | Loga: "Backup incremental executado com sucesso em 10 minutos (RPO: 6 horas mantido)" |

### 5. Fluxos Alternativos

**FA01: Primeiro Backup Incremental (Sem Backup Anterior)**

- Passo 3: Sistema NÃO encontra LSN de backup anterior
- Sistema detecta que é o primeiro backup incremental
- Sistema executa backup differential ao invés de incremental (copia tudo desde último full)
- Tamanho maior (~20 GB), mas garante consistência

**FA02: Monitoramento de RPO**

- Após passo 15: Sistema verifica compliance de RPO
- Calcula tempo desde último backup: `(DateTime.UtcNow - lastBackupTime).TotalHours`
- Se > 6 horas → Envia alerta crítico "RPO Violation Detected"
- Se <= 6 horas → RPO mantido, nenhum alerta

### 6. Exceções

**EX01: LSN do Último Backup Não Encontrado (Cadeia Quebrada)**

- Passo 3: Sistema busca LSN → NÃO encontrado (backup anterior foi deletado manualmente)
- Sistema detecta cadeia de backup quebrada
- Sistema loga erro: "Incremental backup chain broken. Last backup LSN not found."
- Sistema EXECUTA BACKUP FULL automaticamente ao invés de incremental
- Isso restabelece cadeia de backup
- Envia alerta: "Backup incremental não foi possível, backup full executado"

**EX02: Transaction Log Full (Disco Cheio)**

- Passo 6: SQL Server tenta backup de log → Erro "Transaction log is full"
- Sistema detecta que log de transação está 100% cheio
- Sistema executa truncamento de log: `BACKUP LOG IControlIT TO DISK = 'NUL' WITH TRUNCATE_ONLY`
- Sistema tenta backup incremental novamente
- Se bem-sucedido → Continua
- Se falha → Envia alerta crítico

**EX03: Backup Excede Limite de Tamanho (> 50 GB)**

- Passo 8: Backup incremental gerou arquivo de 52 GB (anormal para incremental)
- Sistema detecta tamanho anormal (incrementais normalmente < 5 GB)
- Sistema loga warning: "Incremental backup size is abnormally large (52 GB)"
- Sistema continua upload, mas envia alerta para investigação
- Possível causa: muitas transações entre backups

### 7. Pós-condições

- Backup incremental criado e armazenado
- Cadeia de backup mantida (LSN linkado ao backup anterior)
- RPO de 6 horas garantido
- Auditoria registrada
- Próximo backup incremental agendado para 6 horas depois

### 8. Regras de Negócio Aplicáveis

- **RN-BCK-111-02**: Backup Incremental a Cada 6 Horas
- **RN-BCK-111-06**: RPO (Recovery Point Objective) de 6 Horas

---

## UC04: Executar Failover Automático Após 15 Minutos de Indisponibilidade

### 1. Descrição

Este caso de uso monitora continuamente a saúde da região primária (East US) e inicia failover automático para região secundária (West US) após 15 minutos consecutivos de indisponibilidade conforme RN-BCK-111-08.

### 2. Atores

- **Sistema**: IControlIT Backend, Azure Site Recovery, Azure Traffic Manager, Azure Monitor

### 3. Pré-condições

- Azure Site Recovery configurado com recovery plan "IC2_Prod_DR"
- Health check configurado para monitorar região primária a cada 5 minutos
- Azure Traffic Manager configurado para rotear tráfego
- Feature Flag `BACKUP_DR_FAILOVER` habilitado
- Região secundária (West US) sincronizada e pronta

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Health check executa a cada 5 minutos: `CheckPrimaryRegionAsync()` |
| 2 | - | Envia requisição HTTP para: `https://api-eastus.icontrolit.com/health` |
| 3 | - | Timeout após 30 segundos (região primária não responde) |
| 4 | - | Detecta que região primária está INDISPONÍVEL |
| 5 | - | Loga: "Primary region (East US) is unavailable. Starting 15-minute timer." |
| 6 | - | Registra timestamp de início da indisponibilidade: `outageStartTime = 2025-12-29 14:00:00` |
| 7 | - | Aguarda 15 minutos (`Task.Delay(TimeSpan.FromMinutes(15))`) |
| 8 | - | Após 15 minutos, verifica região primária novamente |
| 9 | - | Região primária ainda indisponível? SIM (continua sem responder) |
| 10 | - | Envia alerta crítico: "Primary region unavailable for 15 minutes. Initiating automatic failover." |
| 11 | - | Executa `AzureSiteRecoveryService.InitiateFailoverAsync(recoveryPlanName: "IC2_Prod_DR", targetRegion: "West US")` |
| 12 | - | Azure Site Recovery inicia replicação de VMs para West US |
| 13 | - | Azure Site Recovery sincroniza dados de replicação (usando Azure Storage replication) |
| 14 | - | Azure Traffic Manager atualiza DNS para redirecionar tráfego: `api.icontrolit.com` → IP de West US |
| 15 | - | VMs inicializadas em West US (5 minutos para boot) |
| 16 | - | Executa validação de funcionalidade: `GET /health` em West US → HTTP 200 OK |
| 17 | - | Failover completo em 12 minutos (dentro do RTO de 4 horas) |
| 18 | - | Registra auditoria (código: `DR_FAILOVER_COMPLETED`) → RegiaoPrimária=EastUS, RegiaoSecundaria=WestUS, Duração=12min, Status=Sucesso |
| 19 | - | Envia notificação para administradores: "Failover concluído. Sistema operando em West US (DR)." |
| 20 | - | Atualiza dashboard com status: "DR Mode: Active (West US)" |

### 5. Fluxos Alternativos

**FA01: Região Primária Volta Antes dos 15 Minutos (Falso Positivo)**

- Passo 9: Após 15 minutos, sistema verifica região primária novamente
- Região primária RESPONDE (voltou online antes do failover)
- Sistema loga: "Primary region recovered before failover threshold. Cancelling failover."
- Sistema NÃO executa failover (evita mudança desnecessária)
- Continua monitoramento normal

**FA02: Failback Após Restauração da Região Primária**

- Após passo 20: Sistema opera em West US (DR)
- Região primária (East US) é restaurada
- Administrador acessa `/api/dr/failback`
- Sistema inicia failback: Sincroniza dados de West US → East US
- Atualiza Traffic Manager para redirecionar para East US
- Sistema retorna para operação normal em região primária

### 6. Exceções

**EX01: Azure Site Recovery Falha Durante Failover**

- Passo 12: Sistema tenta iniciar failover → Azure Site Recovery retorna erro "Recovery plan failed"
- Sistema loga erro: "Failover failed: Azure Site Recovery error"
- Sistema tenta failover novamente (retry automático 3x)
- Se todas tentativas falham → Envia alerta CRÍTICO para time de DevOps
- Administrador deve intervir manualmente

**EX02: Região Secundária Também Indisponível (Desastre Duplo)**

- Passo 16: Sistema tenta validar West US → Região secundária também não responde
- Sistema detecta que AMBAS regiões estão indisponíveis (evento raríssimo)
- Sistema loga erro crítico: "Both primary and secondary regions are unavailable"
- Sistema envia alerta de emergência para todas as equipes
- Sistema aguarda restauração manual

**EX03: DNS Não Atualizado (Traffic Manager Falha)**

- Passo 14: Traffic Manager tenta atualizar DNS → Falha
- Sistema detecta que DNS ainda aponta para East US
- Sistema tenta atualização manual via Azure SDK
- Se falha → Administrador deve atualizar DNS manualmente
- Aplicação pode estar disponível via IP direto de West US

### 7. Pós-condições

- Sistema operando em região secundária (West US)
- Tráfego roteado via Azure Traffic Manager para West US
- Auditoria de failover registrada
- Notificações enviadas para administradores
- Dashboard atualizado com status "DR Mode"
- Monitoramento de região primária continua (para detectar recuperação)

### 8. Regras de Negócio Aplicáveis

- **RN-BCK-111-07**: RTO (Recovery Time Objective) de 4 Horas
- **RN-BCK-111-08**: Failover Automático Após 15 Minutos de Indisponibilidade

---

## UC05: Executar Teste de Disaster Recovery Trimestral

### 1. Descrição

Este caso de uso executa teste completo de plano de DR automaticamente a cada trimestre (1º dia de jan/abr/jul/out às 2h) para validar que failover funciona e dados são consistentes conforme RN-BCK-111-09.

### 2. Atores

- **Sistema**: IControlIT Backend, Hangfire, Azure Site Recovery, Azure SQL

### 3. Pré-condições

- Hangfire configurado com jobs trimestrais
- Azure Site Recovery configurado
- Ambiente de teste isolado disponível
- Backup mais recente disponível
- Feature Flag `BACKUP_DR_FAILOVER` habilitado

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Hangfire dispara job em 2025-01-01 02:00:00 (Q1) |
| 2 | - | `TrimestrialDrTestJob.ExecuteAsync()` inicia |
| 3 | - | Loga: "Starting quarterly DR test for Q1 2025" |
| 4 | - | Busca backup mais recente: `Full_Backup_20251231_020000` |
| 5 | - | Cria ambiente de teste isolado no Azure: Resource Group `IC2_DR_Test_Q1_2025` |
| 6 | - | Provisiona VM temporária: `vm-dr-test-q1-2025` (Standard_D4s_v3) |
| 7 | - | Restaura banco de dados no ambiente de teste: `IControlIT_DR_Test` |
| 8 | - | Inicializa aplicação no ambiente de teste (backend + frontend) |
| 9 | - | Executa bateria de testes de validação: |
| 10 | - | Teste 1: Conectividade ao banco → `SELECT 1` → HTTP 200 OK |
| 11 | - | Teste 2: Integridade referencial → Valida FKs, índices, triggers → PASS |
| 12 | - | Teste 3: API Health Check → `GET /health` → HTTP 200 OK |
| 13 | - | Teste 4: Autenticação → `POST /api/auth/login` com credenciais de teste → HTTP 200 OK, JWT válido |
| 14 | - | Teste 5: Autorização → `GET /api/usuarios` com JWT → HTTP 200 OK, lista de usuários retornada |
| 15 | - | Teste 6: CRUD básico → Cria usuário de teste, lê, atualiza, deleta → PASS |
| 16 | - | Todos os testes passaram? SIM |
| 17 | - | Registra resultado: `DrTestResult { IsSuccess: true, PassedTests: 6, FailedTests: 0, Duration: "12 minutes" }` |
| 18 | - | Destroy ambiente de teste: Deleta Resource Group `IC2_DR_Test_Q1_2025` |
| 19 | - | Registra auditoria (código: `DR_TEST_EXECUTED`) → EscopoDeTeste=Full, DataTeste, Duração=12min, Status=Sucesso |
| 20 | - | Envia relatório de sucesso para administradores: "Teste de DR Q1/2025 concluído com sucesso. 6/6 testes passaram." |
| 21 | - | Loga: "Quarterly DR test completed successfully" |

### 5. Fluxos Alternativos

**FA01: Teste Manual Fora do Cronograma**

- Administrador acessa `/api/dr/testar`
- Sistema valida permissão `backup:dr:test`
- Executa mesmo fluxo principal (passos 3-21)
- Útil para testar após mudanças significativas no sistema

**FA02: Teste Parcial (Apenas Banco de Dados)**

- Passo 9: Administrador solicita teste parcial (escopo: "database")
- Sistema executa apenas testes 1, 2, 6 (banco de dados)
- Pula testes 3, 4, 5 (API, autenticação, autorização)
- Reduz tempo de teste para ~5 minutos

### 6. Exceções

**EX01: Teste de Autenticação Falhou**

- Passo 13: Teste 4 (Autenticação) falha → HTTP 401 Unauthorized
- Sistema detecta falha
- Sistema continua executando testes restantes (5, 6)
- Ao final: `DrTestResult { IsSuccess: false, PassedTests: 5, FailedTests: 1, Duration: "12 minutes", FailedTest: "Authentication" }`
- Registra auditoria com Status=Falha
- Envia alerta CRÍTICO: "DR Test failed - Authentication test did not pass"
- Administrador deve investigar problema antes de próximo teste

**EX02: Ambiente de Teste Não Pode Ser Criado (Quota Azure Excedida)**

- Passo 5: Sistema tenta criar Resource Group → Azure retorna erro "Quota exceeded"
- Sistema detecta que quota de recursos está excedida
- Sistema loga erro: "Cannot create DR test environment - Azure quota exceeded"
- Sistema ABORTA teste
- Envia alerta: "DR Test aborted - Azure quota exceeded. Increase quota and retry."

**EX03: Restauração do Banco Falha (Backup Corrompido)**

- Passo 7: Sistema tenta restaurar banco → Falha de integridade
- Sistema detecta que backup está corrompido
- Sistema loga erro: "DR Test failed - Backup corruption detected"
- Sistema ABORTA teste
- Envia alerta CRÍTICO: "DR Test failed - Latest backup is corrupted. Investigate immediately."
- Administrador deve validar backups e criar novo backup full

### 7. Pós-condições

- Teste de DR executado e resultado registrado
- Ambiente de teste removido (sem impacto em produção)
- Auditoria registrada
- Relatório enviado para administradores
- Se teste falhou → Alerta crítico enviado, correção necessária antes de próximo teste
- Próximo teste agendado para 3 meses depois (próximo trimestre)

### 8. Regras de Negócio Aplicáveis

- **RN-BCK-111-09**: Teste de Disaster Recovery Obrigatório Trimestralmente

---

**Última Atualização**: 2025-12-28
**Autor**: Claude Code
**Revisão**: Pendente

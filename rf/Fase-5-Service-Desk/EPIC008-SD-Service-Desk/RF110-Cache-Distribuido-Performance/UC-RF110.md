# UC-RF110 - Casos de Uso - Cache Distribuído e Performance

## UC01: Configurar e Monitorar Cache Distribuído Redis

### 1. Descrição

Este caso de uso permite ao Administrador configurar parâmetros de cache distribuído (TTL, compressão, warm-up) e monitorar métricas em tempo real (hit rate, latência, uso de memória) via dashboard.

### 2. Atores

- **Usuário autenticado**: Administrador
- **Sistema**: IControlIT Backend, Redis, Application Insights

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `cache:admin:full` ou `cache:metrics:read`
- Redis configurado e acessível
- Application Insights configurado para métricas

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Administração → Cache Distribuído | - |
| 2 | - | Valida permissão `cache:metrics:read` |
| 3 | - | Executa `GET /api/cache/status` |
| 4 | - | Verifica conexão com Redis usando `IConnectionMultiplexer` |
| 5 | - | Obtém métricas do Redis: versão, memória usada, total de chaves |
| 6 | - | Calcula hit rate atual: `(hitCount / (hitCount + missCount)) * 100` |
| 7 | - | Obtém latência média (P95) do Redis via Application Insights |
| 8 | - | Retorna HTTP 200 OK com payload: `{ isHealthy: true, hitRate: 85.3%, latencyP95: 3ms, memoryUsedMb: 512, totalKeys: 12450, version: "7.0.5" }` |
| 9 | Visualiza dashboard com: Hit Rate (gauge), Latência Média (gráfico de linha), Uso de Memória (barra de progresso), Total de Chaves (contador) | - |
| 10 | - | Atualiza métricas em tempo real a cada 10 segundos (SignalR ou polling) |
| 11 | Clica em "Configurações Avançadas" | - |
| 12 | - | Exibe formulário com: TTL Padrão (segundos), TTL de Sessão (segundos), TTL de APIs Externas (segundos), Habilitar Compressão (checkbox), Habilitar Warm-up (checkbox) |
| 13 | Altera TTL Padrão de 900s (15 min) para 1200s (20 min) | - |
| 14 | Clica em "Salvar Configurações" | - |
| 15 | - | Valida permissão `cache:admin:full` |
| 16 | - | Atualiza `CacheConfiguration` em appsettings.json ou Feature Flag |
| 17 | - | Registra auditoria (código: `CACHE_CONFIG_UPDATE`) → ClienteId, UsuarioId, Campos alterados, Valores antigos, Novos valores |
| 18 | - | Retorna HTTP 200 OK |
| 19 | Visualiza mensagem "Configurações de cache atualizadas com sucesso" | - |

### 5. Fluxos Alternativos

**FA01: Hit Rate Abaixo de 80% (Alerta)**

- Passo 6: Sistema calcula hit rate = 72% (< 80%)
- Sistema exibe alerta visual (badge vermelho): "Hit rate abaixo do esperado (72%)"
- Sistema dispara evento Application Insights: "CacheHealthAlert"
- Administrador pode clicar em "Investigar" para ver breakdown por tipo de chave
- Sistema exibe top 10 chaves com maior miss rate

**FA02: Redis Indisponível (Fallback)**

- Passo 4: Sistema tenta conectar ao Redis → Falha (RedisConnectionException)
- Sistema exibe badge amarelo: "Redis indisponível, usando cache local"
- Sistema retorna `isHealthy: false, fallbackActive: true`
- Métricas são exibidas apenas do Memory Cache local
- Circuit Breaker exibido como "OPEN"

### 6. Exceções

**EX01: Usuário Sem Permissão**

- Passo 2: Sistema valida permissão `cache:metrics:read` → Usuário NÃO possui
- Sistema retorna HTTP 403 Forbidden
- Exibe mensagem: "Você não tem permissão para acessar métricas de cache"
- Registra tentativa não autorizada em auditoria

**EX02: Configuração Inválida**

- Passo 14: Usuário define TTL Padrão = 0 (inválido)
- Sistema valida: TTL deve ser >= 60 segundos e <= 86400 segundos (24 horas)
- Retorna HTTP 400 Bad Request
- Exibe mensagem: "TTL inválido. Deve estar entre 60 e 86400 segundos."

**EX03: Erro ao Conectar Application Insights**

- Passo 7: Sistema tenta obter latência do Application Insights → Falha
- Sistema loga aviso: "Application Insights indisponível, latência não disponível"
- Exibe "Latência: N/A" no dashboard
- Operação continua normalmente (degradação graciosa)

### 7. Pós-condições

- Dashboard de cache exibindo métricas atualizadas em tempo real
- Configurações de TTL atualizadas (se alteradas)
- Auditoria registrada em AuditLog
- Se hit rate < 80% → Alerta enviado para administradores
- Se Redis indisponível → Circuit Breaker ativo, fallback para Memory Cache

### 8. Regras de Negócio Aplicáveis

- **RN-PER-110-01**: TTL Padrão de Cache (configurável, padrão 15 minutos)
- **RN-PER-110-06**: Hit Rate Mínimo Esperado de 80%
- **RN-PER-110-09**: Fallback Automático para Memory Cache se Redis Indisponível
- **RN-PER-110-10**: Auditoria de Operações de Invalidação de Cache

---

## UC02: Invalidar Cache por Padrão de Chave

### 1. Descrição

Este caso de uso permite ao Administrador invalidar cache manualmente usando padrões de chave (wildcards), útil após alterações massivas de dados ou correção de bugs que resultaram em cache inconsistente.

### 2. Atores

- **Usuário autenticado**: Administrador
- **Sistema**: IControlIT Backend, Redis, CacheInvalidationStrategy

### 3. Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão: `cache:invalidate:execute`
- Redis acessível
- Pelo menos 1 chave de cache existente

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu Administração → Cache Distribuído → Invalidar Cache | - |
| 2 | - | Valida permissão `cache:invalidate:execute` |
| 3 | - | Exibe formulário com campos: Padrão de Chave (text input com exemplos), Motivo (text area obrigatório) |
| 4 | Insere padrão: `query:*:usuario:*` (invalida todas as queries de usuários) | - |
| 5 | Insere motivo: "Atualização massiva de permissões de usuários" | - |
| 6 | Clica em "Invalidar" | - |
| 7 | - | Valida padrão de chave (não pode ser `*` sozinho, deve ter namespace) |
| 8 | - | Executa `POST /api/cache/invalidate` com payload: `{ pattern: "query:*:usuario:*", reason: "..." }` |
| 9 | - | Obtém ClienteId do usuário autenticado |
| 10 | - | Executa `CacheInvalidationStrategy.InvalidateByPatternAsync(clienteId, pattern, reason)` |
| 11 | - | Busca chaves no Redis usando `server.KeysAsync(pattern)` com paginação (100 por vez) |
| 12 | - | Para cada chave encontrada, executa `_cache.RemoveAsync(key)` |
| 13 | - | Conta total de chaves invalidadas: 237 chaves |
| 14 | - | Registra auditoria (código: `CACHE_INVALIDATION`) → ClienteId, Pattern, KeysInvalidated=237, Reason, TriggeredBy (UserId) |
| 15 | - | Retorna HTTP 200 OK com: `{ keysInvalidated: 237, memoryFreedBytes: 121344 }` |
| 16 | Visualiza mensagem: "Cache invalidado com sucesso. 237 chaves removidas, 118 KB liberados." | - |
| 17 | - | Dashboard atualiza hit rate (pode cair temporariamente até cache rebuild) |

### 5. Fluxos Alternativos

**FA01: Invalidar Cache Específico (Chave Exata)**

- Passo 4: Usuário insere chave exata: `session:c12d3f4e5b6a7c8d9e0f1a2b3c4d5e6f:user:a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d`
- Sistema executa `DELETE /api/cache/{key}`
- Remove apenas essa chave específica
- Retorna: `{ keysInvalidated: 1, memoryFreedBytes: 512 }`

**FA02: Nenhuma Chave Encontrada**

- Passo 11: Sistema busca chaves com padrão → Retorna lista vazia
- Sistema retorna HTTP 204 No Content
- Exibe mensagem: "Nenhuma chave encontrada com o padrão informado."
- Auditoria registrada com KeysInvalidated=0

### 6. Exceções

**EX01: Padrão Muito Genérico (Segurança)**

- Passo 7: Usuário tenta invalidar padrão `*` (todos os caches de todos os clientes)
- Sistema valida: padrão deve ter pelo menos 2 níveis (ex: `query:*`, `session:*`)
- Retorna HTTP 400 Bad Request
- Exibe mensagem: "Padrão muito genérico. Use padrões mais específicos (ex: query:*, session:*)."

**EX02: Redis Indisponível**

- Passo 11: Sistema tenta buscar chaves → Redis não acessível
- Sistema loga erro: "Redis indisponível durante invalidação"
- Retorna HTTP 503 Service Unavailable
- Exibe mensagem: "Redis indisponível. Tente novamente ou contate o suporte."
- Operação NÃO é executada (invalidação não ocorre parcialmente)

**EX03: Timeout ao Invalidar Muitas Chaves**

- Passo 12: Sistema encontra 50.000 chaves para invalidar
- Processo excede timeout de 30 segundos
- Sistema executa invalidação em batch (1.000 chaves por vez)
- Retorna HTTP 202 Accepted com JobId
- Processamento continua em background via Hangfire
- Usuário recebe notificação quando concluir

### 7. Pós-condições

- Chaves de cache invalidadas conforme padrão especificado
- Auditoria registrada em tabela `CacheInvalidationAudits`
- Memória Redis liberada
- Hit rate pode cair temporariamente (cache rebuild necessário)
- Próximas requisições buscarão dados do banco de dados

### 8. Regras de Negócio Aplicáveis

- **RN-PER-110-03**: Chaves de Cache Incluem ClienteId (isolamento de dados)
- **RN-PER-110-04**: Invalidação Automática em UPDATE/DELETE
- **RN-PER-110-10**: Auditoria de Operações de Invalidação de Cache

---

## UC03: Executar Warm-up de Cache ao Iniciar Aplicação

### 1. Descrição

Este caso de uso executa pré-aquecimento automático de cache ao iniciar aplicação (ApplicationStartup) ou manualmente via endpoint, carregando dados críticos (usuários ativos, serviços, permissões) para garantir hit rate elevado desde o primeiro acesso.

### 2. Atores

- **Sistema**: IControlIT Backend, CacheWarmupService, Hangfire
- **Usuário autenticado** (opcional): Administrador (warm-up manual)

### 3. Pré-condições

- Aplicação iniciando (ApplicationStartup) ou warm-up manual solicitado
- Redis acessível
- Banco de dados acessível
- Feature Flag `PERF_CACHE_WARMUP` habilitado
- Pelo menos 1 usuário ativo no banco de dados

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Aplicação inicia (Program.cs → IHostedService.StartAsync) |
| 2 | - | CacheWarmupService ativado automaticamente |
| 3 | - | Loga: "Starting cache warmup..." |
| 4 | - | Consulta banco de dados: `SELECT * FROM Usuarios WHERE Ativo = 1 AND ClienteId IS NOT NULL` |
| 5 | - | Retorna 500 usuários ativos |
| 6 | - | Para cada usuário, cria chave de cache: `session:{clienteId}:user:{userId}` |
| 7 | - | Serializa dados do usuário usando `System.Text.Json` com Source Generators |
| 8 | - | Armazena em Redis com TTL de 30 minutos (sliding expiration) |
| 9 | - | Consulta banco de dados: `SELECT * FROM Servicos WHERE Ativo = 1` |
| 10 | - | Retorna 1.000 serviços ativos |
| 11 | - | Para cada serviço, cria chave: `servico:{clienteId}:{servicoId}` |
| 12 | - | Serializa e armazena em Redis com TTL de 1 hora |
| 13 | - | Consulta permissões padrão por perfil |
| 14 | - | Armazena permissões em chaves: `permission:{clienteId}:profile:{perfilId}` |
| 15 | - | Calcula tempo total de warm-up: 2.3 segundos |
| 16 | - | Loga: "Cache warmup completed. Loaded 500 users, 1000 services in 2.3s" |
| 17 | - | Registra auditoria (código: `CACHE_WARMUP_END`) → Duração, Entidades carregadas |
| 18 | - | Hit rate salta de ~20% (cold) para ~85% (warm) em primeiros 5 minutos |

### 5. Fluxos Alternativos

**FA01: Warm-up Manual via Endpoint**

- Administrador acessa `/api/cache/warmup` (POST)
- Sistema valida permissão `cache:warmup:execute`
- Executa mesmo fluxo principal (passos 3-17)
- Retorna HTTP 200 OK com: `{ entitiesLoaded: 1500, duration: "2.3s" }`
- Útil após limpar cache ou após deploy

**FA02: Warm-up Seletivo (Apenas Usuários)**

- Sistema recebe parâmetro: `warmupType=users`
- Executa apenas passos 4-8 (usuários)
- Pula serviços e permissões
- Útil para warm-up incremental

### 6. Exceções

**EX01: Redis Indisponível Durante Warm-up**

- Passo 8: Sistema tenta armazenar em Redis → RedisConnectionException
- Sistema loga erro: "Redis unavailable during warmup, skipping"
- Warm-up é abortado (NÃO interrompe startup da aplicação)
- Aplicação inicia normalmente, mas hit rate inicial será baixo
- Circuit Breaker ativa fallback para Memory Cache

**EX02: Banco de Dados Lento**

- Passo 4: Query de usuários ativos demora mais de 30 segundos
- Sistema aplica timeout e cancela warm-up
- Loga aviso: "Warmup timeout, database too slow"
- Aplicação inicia normalmente
- Warm-up será tentado novamente em próximo restart ou manualmente

**EX03: Memória Redis Insuficiente**

- Passo 8: Sistema tenta armazenar dados → Redis retorna "OOM (out of memory)"
- Sistema detecta erro de memória
- Warm-up é interrompido parcialmente (carrega o que couber)
- Loga alerta: "Redis memory pressure, warmup incomplete"
- Administrador recebe alerta para aumentar memória Redis

### 7. Pós-condições

- Dados críticos pré-carregados em cache (usuários, serviços, permissões)
- Hit rate inicial elevado (~85%) ao invés de baixo (~20%)
- Auditoria de warm-up registrada em AuditLog
- Se warm-up falha → Aplicação inicia normalmente (degradação graciosa)
- Próximo warm-up agendado para próximo restart ou solicitação manual

### 8. Regras de Negócio Aplicáveis

- **RN-PER-110-01**: TTL Padrão de Cache (sessão 30 min, serviços 1 hora)
- **RN-PER-110-02**: Serialização em JSON com System.Text.Json
- **RN-PER-110-03**: Chaves de Cache Incluem ClienteId
- **RN-PER-110-07**: Warm-up de Cache ao Iniciar Aplicação
- **RN-PER-110-09**: Fallback Automático para Memory Cache se Redis Indisponível

---

## UC04: Aplicar Compressão Automática para Dados Maiores que 1 KB

### 1. Descrição

Este caso de uso aplica compressão Gzip automaticamente a objetos serializados maiores que 1.024 bytes antes de armazenamento em Redis, reduzindo uso de memória em aproximadamente 60% conforme RN-PER-110-05.

### 2. Atores

- **Sistema**: IControlIT Backend, CompressedCacheService, CompressionService

### 3. Pré-condições

- Feature Flag `PERF_CACHE_COMPRESSION` habilitado
- Objeto a ser cacheado serializado em JSON
- Redis acessível

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Aplicação precisa armazenar lista de 500 usuários em cache |
| 2 | - | Serializa lista usando `JsonSerializer.Serialize<List<Usuario>>(usuarios)` |
| 3 | - | Converte string JSON para bytes: `Encoding.UTF8.GetBytes(json)` |
| 4 | - | Verifica tamanho: 4.200 bytes (> 1.024 bytes, compressão será aplicada) |
| 5 | - | Executa `CompressionService.CompressGzip(bytes)` |
| 6 | - | Gzip comprime dados usando `GZipStream` |
| 7 | - | Dados comprimidos: 1.800 bytes (57% de redução) |
| 8 | - | Converte bytes comprimidos para Base64: `Convert.ToBase64String(compressed)` |
| 9 | - | Armazena em Redis com chave prefixada: `gz:query:c12d...:{hash}` (prefixo "gz:" indica comprimido) |
| 10 | - | Define TTL de 15 minutos |
| 11 | - | Registra métrica em Application Insights: `{ OriginalSize: 4200, CompressedSize: 1800, CompressionRatio: 57.14% }` |
| 12 | - | Loga: "CacheCompressed: query:usuarios, 4200 → 1800 bytes (57% saved)" |
| 13 | - | Próxima leitura deste cache: Sistema detecta prefixo "gz:", descomprime automaticamente, deserializa e retorna |

### 5. Fluxos Alternativos

**FA01: Dados Menores que 1 KB (Sem Compressão)**

- Passo 4: Tamanho = 800 bytes (< 1.024 bytes)
- Sistema pula passos 5-7 (não comprime)
- Armazena diretamente em Redis sem prefixo "gz:"
- Economia de CPU (não gasta ciclos comprimindo dados pequenos)

**FA02: Leitura de Dados Comprimidos**

- Sistema lê chave `gz:query:usuarios:hash`
- Detecta prefixo "gz:"
- Executa `Convert.FromBase64String(cached)` para obter bytes
- Verifica magic number Gzip (0x1f 0x8b) para confirmar compressão
- Executa `CompressionService.DecompressGzip(bytes)`
- Converte bytes descomprimidos para string UTF-8
- Deserializa JSON e retorna objeto

### 6. Exceções

**EX01: Erro ao Comprimir**

- Passo 6: GZipStream lança exceção (corrupção de dados)
- Sistema captura exceção, loga erro
- Armazena dados SEM compressão (fallback)
- Registra alerta: "Compression failed, storing uncompressed"
- Operação continua normalmente

**EX02: Erro ao Descomprimir**

- Leitura detecta prefixo "gz:" mas magic number Gzip está ausente (corrupção)
- Sistema tenta descomprimir → Falha
- Sistema loga erro: "Decompression failed for key: {key}"
- Invalida chave corrompida (`_cache.RemoveAsync(key)`)
- Retorna cache MISS (força busca no banco de dados)

**EX03: Compressão Não Compensou (Dados Aleatórios)**

- Passo 7: Dados comprimidos = 4.100 bytes (original = 4.200 bytes, apenas 2% de ganho)
- Sistema detecta que compressão não compensou
- Armazena dados originais SEM compressão
- Evita overhead de descompressão desnecessária

### 7. Pós-condições

- Dados maiores que 1 KB armazenados comprimidos em Redis
- Uso de memória Redis reduzido em ~60%
- Métrica de compressão registrada em Application Insights
- Prefixo "gz:" indica dados comprimidos
- Descompressão automática em leituras subsequentes

### 8. Regras de Negócio Aplicáveis

- **RN-PER-110-05**: Compressão Obrigatória para Dados Maiores que 1 KB

---

## UC05: Monitorar Hit Rate e Disparar Alertas se Abaixo de 80%

### 1. Descrição

Este caso de uso monitora continuamente a taxa de acerto (hit rate) do cache e dispara alertas automáticos quando hit rate cai abaixo de 80%, conforme RN-PER-110-06.

### 2. Atores

- **Sistema**: IControlIT Backend, CacheMetricsCollector, Application Insights

### 3. Pré-condições

- Redis acessível
- Application Insights configurado
- Pelo menos 100 requisições processadas (amostra mínima)

### 4. Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | - | Aplicação processa requisição que precisa de dados de cache |
| 2 | - | Executa `MonitoredCacheService.GetAsync<T>(key)` |
| 3 | - | Tenta ler do Redis: `_cache.GetStringAsync(key)` |
| 4 | - | Se dados encontrados (cache HIT) → Incrementa `_hitCount` via `Interlocked.Increment` |
| 5 | - | Se dados NÃO encontrados (cache MISS) → Incrementa `_missCount` |
| 6 | - | Registra métrica em Application Insights: `ApplicationInsights.TrackEvent("CacheHit", ...)` ou `"CacheMiss"` |
| 7 | - | A cada 100 requisições, calcula hit rate: `hitRate = (hitCount / (hitCount + missCount)) * 100` |
| 8 | - | Hit rate calculado: 72.5% |
| 9 | - | Valida threshold: Hit rate < 80%? SIM |
| 10 | - | Loga warning: "Cache hit rate below threshold: 72.5%" |
| 11 | - | Dispara evento Application Insights: `ApplicationInsights.TrackEvent("CacheHealthAlert", { HitRate: "72.5", TotalRequests: "1000" })` |
| 12 | - | Application Insights aciona alerta configurado (envia email/SMS para administradores) |
| 13 | - | Dashboard exibe badge vermelho: "Hit rate crítico: 72.5%" |
| 14 | - | Administrador recebe notificação: "Cache hit rate abaixo de 80%. Investigar invalidações ou aumentar TTL." |
| 15 | - | Administrador acessa dashboard de cache para investigar |
| 16 | - | Sistema exibe breakdown de hit rate por tipo de chave: Queries (60%), Sessões (85%), APIs Externas (90%) |
| 17 | - | Administrador identifica problema em queries de usuários (invalidações excessivas) |
| 18 | - | Administrador ajusta TTL de queries de 10 min para 20 min |
| 19 | - | Hit rate sobe gradualmente para 85% em 15 minutos |

### 5. Fluxos Alternativos

**FA01: Hit Rate Saudável (Acima de 80%)**

- Passo 9: Hit rate calculado: 87.2%
- Sistema valida threshold: Hit rate < 80%? NÃO
- Nenhum alerta disparado
- Dashboard exibe badge verde: "Hit rate saudável: 87.2%"
- Operação continua normalmente

**FA02: Hit Rate Crítico (Abaixo de 50%)**

- Passo 8: Hit rate = 42%
- Sistema classifica como CRÍTICO (< 50%)
- Dispara alerta de prioridade ALTA
- Envia page (SMS) para DevOps
- Sugere ações: "Verificar falha de cache, invalidação massiva ou Redis indisponível"

### 6. Exceções

**EX01: Amostra Insuficiente**

- Passo 7: Total de requisições = 15 (< 100)
- Sistema NÃO calcula hit rate (amostra muito pequena)
- Aguarda atingir 100 requisições antes de calcular
- Evita falsos positivos em início de aplicação

**EX02: Application Insights Indisponível**

- Passo 11: Sistema tenta enviar evento → Application Insights não acessível
- Sistema loga aviso: "Application Insights unavailable, alert not sent"
- Métricas continuam sendo coletadas localmente
- Alerta será enviado quando Application Insights voltar

**EX03: Redis Offline (Hit Rate = 0%)**

- Passo 3: Redis indisponível (todas requisições resultam em MISS)
- Hit rate = 0%
- Sistema detecta fallback ativo para Memory Cache
- Alerta disparado com contexto: "Hit rate 0% - Redis offline, fallback ativo"
- Prioridade de alerta: CRÍTICA

### 7. Pós-condições

- Hit rate monitorado continuamente
- Métricas registradas em Application Insights
- Se hit rate < 80% → Alerta disparado, administradores notificados
- Se hit rate crítico → Page enviado para DevOps
- Dashboard atualizado com status de saúde do cache

### 8. Regras de Negócio Aplicáveis

- **RN-PER-110-06**: Hit Rate Mínimo Esperado de 80%

---

**Última Atualização**: 2025-12-28
**Autor**: Claude Code
**Revisão**: Pendente

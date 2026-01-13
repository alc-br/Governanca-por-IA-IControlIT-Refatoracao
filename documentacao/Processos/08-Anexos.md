# 08. ANEXOS E RECURSOS DE SUPORTE

**Versão:** 2.0
**Data:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente

---

## ÍNDICE

1. [Glossário de Termos Técnicos](#1-glossário-de-termos-técnicos)
2. [Referências Completas aos RFs](#2-referências-completas-aos-rfs)
3. [Mapa de Dependências Processos → RFs](#3-mapa-de-dependências-processos--rfs)
4. [Árvore de Dependências Técnicas](#4-árvore-de-dependências-técnicas)
5. [Tabela de RFs Excluídos](#5-tabela-de-rfs-excluídos-cadastros-simples)
6. [Matriz de Cobertura RF → UC → TC](#6-matriz-de-cobertura-rf--uc--tc)
7. [Recursos Adicionais](#7-recursos-adicionais)
8. [Índice Alfabético de Processos](#8-índice-alfabético-de-processos)
9. [Changelog Consolidado](#9-changelog-consolidado)
10. [Contatos e Suporte](#10-contatos-e-suporte)

---

## 1. GLOSSÁRIO DE TERMOS TÉCNICOS

### 1.1. ARQUITETURA

#### Aggregate
**Definição:** Padrão DDD que agrupa entidades relacionadas sob uma raiz única, garantindo consistência transacional.
**Contexto de Uso:** PRO-INF-001, PRO-AUD-001, PRO-FCT-001 (handlers de criação/atualização)
**Exemplo:** `FaturaAggregate` agrupa `Fatura`, `ItemFatura`, `RateioFatura`

#### Clean Architecture
**Definição:** Arquitetura em camadas concêntricas (Domain → Application → Infrastructure → Presentation) com dependências apontando para o centro.
**Contexto de Uso:** Todos os processos (estrutura base do sistema)
**Exemplo:** Handlers (Application) não conhecem Controllers (Presentation)

#### Command
**Definição:** Objeto que representa uma intenção de alterar estado do sistema (padrão CQRS).
**Contexto de Uso:** Todos os processos com operações de escrita
**Exemplo:** `CreateClienteCommand`, `AprovarSolicitacaoCommand`

#### CQRS (Command Query Responsibility Segregation)
**Definição:** Separação entre operações de escrita (Commands) e leitura (Queries).
**Contexto de Uso:** Todos os processos
**Exemplo:** `CreateFaturaCommand` vs `GetFaturaByIdQuery`

#### DDD (Domain-Driven Design)
**Definição:** Abordagem de design que coloca a lógica de negócio no centro da arquitetura.
**Contexto de Uso:** PRO-INF-001 a PRO-AUD-001 (todos os processos)
**Exemplo:** Entidades `Fatura`, `Solicitacao`, `Ativo` com regras de negócio encapsuladas

#### Event
**Definição:** Notificação imutável de algo que já aconteceu no sistema.
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001, PRO-SVC-002 (notificações assíncronas)
**Exemplo:** `FaturaAprovadaEvent`, `SLAVioladoEvent`

#### Handler
**Definição:** Classe responsável por processar Commands, Queries ou Events (padrão MediatR).
**Contexto de Uso:** Todos os processos
**Exemplo:** `CreateFaturaHandler`, `GetClientesQueryHandler`

#### MediatR
**Definição:** Biblioteca que implementa o padrão Mediator para desacoplar requests de seus handlers.
**Contexto de Uso:** Todos os processos
**Exemplo:** `IRequestHandler<CreateClienteCommand, ClienteDto>`

#### Query
**Definição:** Objeto que representa uma consulta ao sistema sem alterar estado (padrão CQRS).
**Contexto de Uso:** Todos os processos com operações de leitura
**Exemplo:** `GetFaturasByClienteIdQuery`, `SearchAtivosQuery`

#### Repository
**Definição:** Padrão que encapsula acesso a dados, abstraindo detalhes de persistência.
**Contexto de Uso:** Todos os processos
**Exemplo:** `IFaturaRepository`, `IClienteRepository`

#### Unit of Work
**Definição:** Padrão que gerencia transações e coordena salvamento de múltiplos agregados.
**Contexto de Uso:** PRO-INF-001, PRO-FCT-001, PRO-AUD-001 (operações transacionais)
**Exemplo:** `_unitOfWork.SaveChangesAsync()` ao final de handlers

---

### 1.2. MULTI-TENANCY

#### ClienteId
**Definição:** Identificador único do tenant, obrigatório em todas as entidades para isolamento de dados.
**Contexto de Uso:** Todos os processos (obrigatório por COMPLIANCE.md seção 6)
**Exemplo:** `WHERE ClienteId = @clienteId` em todas as queries

#### Cross-tenant
**Definição:** Operação que acessa dados de múltiplos tenants (PROIBIDO sem justificativa).
**Contexto de Uso:** PRO-INF-006, PRO-INF-004 (auditoria cross-tenant)
**Exemplo:** Relatórios consolidados de múltiplos clientes (requer autorização)

#### Isolamento
**Definição:** Garantia de que dados de um tenant não sejam acessíveis por outro.
**Contexto de Uso:** Todos os processos
**Exemplo:** Row-Level Security (RLS) no PostgreSQL

#### Row-Level Security (RLS)
**Definição:** Mecanismo de banco de dados que filtra linhas automaticamente por ClienteId.
**Contexto de Uso:** PRO-INF-006, todos os processos de dados sensíveis
**Exemplo:** `CREATE POLICY cliente_isolation ON faturas USING (ClienteId = current_setting('app.cliente_id')::uuid)`

#### Shared Database
**Definição:** Modelo multi-tenancy onde todos os tenants compartilham o mesmo banco de dados.
**Contexto de Uso:** Arquitetura base do sistema
**Exemplo:** Tabela `Faturas` com coluna `ClienteId` discriminando tenants

#### Tenant
**Definição:** Cliente isolado no sistema multi-tenancy (sinônimo de Cliente).
**Contexto de Uso:** Todos os processos
**Exemplo:** Cliente "Empresa XYZ" é um tenant com `ClienteId = uuid-1234`

#### Tenant-specific
**Definição:** Configuração, dado ou lógica específica de um tenant.
**Contexto de Uso:** PRO-INF-001, PRO-INF-006
**Exemplo:** Parâmetro `dias_vencimento_fatura` pode variar por tenant

---

### 1.3. COMPLIANCE E CERTIFICAÇÕES

#### Auditoria
**Definição:** Registro imutável de operações críticas para rastreabilidade e conformidade.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007, PRO-AUD-001
**Exemplo:** Tabela `AuditLogs` com snapshot antes/depois de alterações

#### Compliance
**Definição:** Conformidade com regulamentações, normas e certificações.
**Contexto de Uso:** Todos os processos (obrigatório por COMPLIANCE.md)
**Exemplo:** LGPD, SOX, ISO 27001, SOC 2

#### ISO 27001
**Definição:** Norma internacional de gestão de segurança da informação.
**Contexto de Uso:** PRO-INF-007, PRO-INF-008, PRO-INF-004
**Exemplo:** Logs de acesso, criptografia de dados sensíveis, controle de acesso

#### LGPD (Lei Geral de Proteção de Dados)
**Definição:** Lei brasileira que regula tratamento de dados pessoais.
**Contexto de Uso:** PRO-INF-006, PRO-INF-007, PRO-INF-004
**Exemplo:** Anonimização de logs, direito ao esquecimento, consentimento

#### OWASP
**Definição:** Organização que define padrões de segurança web (OWASP Top 10).
**Contexto de Uso:** PRO-INF-007, PRO-INF-008
**Exemplo:** Proteção contra SQL Injection, XSS, CSRF

#### PCI-DSS
**Definição:** Padrão de segurança para transações com cartões de crédito.
**Contexto de Uso:** PRO-FCT-002 (pagamentos de faturas)
**Exemplo:** Não armazenar CVV, tokenização de números de cartão

#### Retenção
**Definição:** Período obrigatório de armazenamento de dados conforme regulamentação.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007
**Exemplo:** Logs auditoria retidos por 7 anos (SOX), faturas por 5 anos (legislação fiscal)

#### SOC 2 (Service Organization Control 2)
**Definição:** Auditoria de controles internos de segurança, disponibilidade e confidencialidade.
**Contexto de Uso:** PRO-INF-004, PRO-INF-007, PRO-SVC-001
**Exemplo:** Monitoramento de SLA, logs de acesso, backup automatizado

#### SOX (Sarbanes-Oxley)
**Definição:** Lei americana que exige controles rigorosos sobre dados financeiros.
**Contexto de Uso:** PRO-FCT-001 a PRO-FCT-007, PRO-AUD-001
**Exemplo:** Segregação de funções, auditoria de alterações financeiras, trilha imutável

---

### 1.4. SEGURANÇA

#### API Key
**Definição:** Chave de autenticação para APIs externas ou integrações.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003 (integração SEFAZ)
**Exemplo:** `X-API-Key: sk_live_1234567890abcdef` no header HTTP

#### Azure Key Vault
**Definição:** Serviço Azure para armazenamento seguro de secrets, chaves e certificados.
**Contexto de Uso:** PRO-INF-008, PRO-INF-001
**Exemplo:** Connection strings, API Keys, certificados SSL armazenados no Key Vault

#### Criptografia AES-256
**Definição:** Algoritmo de criptografia simétrica com chave de 256 bits.
**Contexto de Uso:** PRO-INF-008, PRO-INF-004
**Exemplo:** Criptografia de anexos sensíveis no Azure Blob Storage

#### Hash
**Definição:** Função unidirecional que gera identificador fixo de tamanho a partir de entrada variável.
**Contexto de Uso:** PRO-INF-007 (senhas), PRO-INF-004 (integridade de logs)
**Exemplo:** Senha hasheada com bcrypt, SHA-256 para verificação de integridade

#### JWT (JSON Web Token)
**Definição:** Token autocontido que carrega claims de autenticação/autorização.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` contendo `ClienteId`, `UserId`, `Roles`

#### MFA (Multi-Factor Authentication)
**Definição:** Autenticação que exige múltiplos fatores (senha + código SMS/App).
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Login com senha + código TOTP do Microsoft Authenticator

#### OAuth 2.0
**Definição:** Protocolo de autorização para acesso seguro a recursos protegidos.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Fluxo Authorization Code com PKCE para SPAs

#### Rate Limiting
**Definição:** Limitação de número de requisições por tempo para prevenir abuso.
**Contexto de Uso:** PRO-INF-007, PRO-INF-008
**Exemplo:** Máximo 100 requisições/minuto por IP

#### Refresh Token
**Definição:** Token de longa duração usado para obter novos Access Tokens sem re-autenticação.
**Contexto de Uso:** PRO-INF-007
**Exemplo:** Refresh Token válido por 30 dias, Access Token por 1 hora

#### Throttling
**Definição:** Redução gradual de taxa de processamento quando limites são atingidos.
**Contexto de Uso:** PRO-INF-008, PRO-IMP-001
**Exemplo:** Importação desacelera de 1000/s para 100/s ao atingir 80% CPU

---

### 1.5. PERFORMANCE

#### Backoff Exponencial
**Definição:** Estratégia de retry que aumenta exponencialmente o intervalo entre tentativas.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003 (integração SEFAZ)
**Exemplo:** Retry após 1s, 2s, 4s, 8s, 16s...

#### Cache
**Definição:** Armazenamento temporário de dados frequentemente acessados para reduzir latência.
**Contexto de Uso:** PRO-INF-001, PRO-INF-002, PRO-WKF-006
**Exemplo:** Redis cache para parâmetros de sistema, templates de relatórios

#### Circuit Breaker
**Definição:** Padrão que interrompe chamadas a serviços falhando repetidamente.
**Contexto de Uso:** PRO-INF-008, PRO-FCT-003
**Exemplo:** Após 5 falhas consecutivas na SEFAZ, abre circuito por 60 segundos

#### Hot-Reload
**Definição:** Atualização de configuração/código sem restart da aplicação.
**Contexto de Uso:** PRO-INF-001, PRO-WKF-006
**Exemplo:** Atualizar template de relatório sem reiniciar backend

#### Lazy Loading
**Definição:** Carregamento sob demanda de dados relacionados (não antecipado).
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Carregar itens de fatura apenas quando expandir detalhes

#### Pub/Sub
**Definição:** Padrão de mensageria assíncrona (publisher/subscriber).
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001
**Exemplo:** Redis Pub/Sub para notificações em tempo real via SignalR

#### Redis
**Definição:** Banco de dados em memória usado para cache e mensageria.
**Contexto de Uso:** PRO-INF-001, PRO-INF-002, PRO-WKF-004
**Exemplo:** Cache de parâmetros, Pub/Sub para notificações

#### SqlBulkCopy
**Definição:** API .NET para inserção em massa de dados no SQL Server.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Importar 50.000 ativos em chunks de 1.000 registros

#### TTL (Time To Live)
**Definição:** Tempo de expiração de cache ou token.
**Contexto de Uso:** PRO-INF-001, PRO-INF-007
**Exemplo:** Cache de parâmetros com TTL de 5 minutos

---

### 1.6. INFRAESTRUTURA

#### Azure Blob Storage
**Definição:** Serviço Azure de armazenamento de objetos (arquivos, imagens, documentos).
**Contexto de Uso:** PRO-INF-002, PRO-FCT-004, PRO-SVC-003
**Exemplo:** Upload de anexos, PDF de DANFE, evidências de chamados

#### Hangfire
**Definição:** Biblioteca .NET para agendamento e execução de jobs em background.
**Contexto de Uso:** PRO-INF-005, PRO-FCT-006, PRO-IMP-001
**Exemplo:** Job recorrente para calcular SLA a cada 5 minutos

#### OFX (Open Financial Exchange)
**Definição:** Formato padrão para troca de dados financeiros.
**Contexto de Uso:** PRO-FCT-005 (importação de conciliação bancária)
**Exemplo:** Arquivo .ofx exportado do banco contendo transações

#### OpenAPI (Swagger)
**Definição:** Especificação para documentação de APIs REST.
**Contexto de Uso:** PRO-INF-008
**Exemplo:** Swagger UI em `/swagger` para documentação interativa

#### REST API
**Definição:** Arquitetura de APIs baseada em HTTP com operações CRUD.
**Contexto de Uso:** Todos os processos
**Exemplo:** `POST /api/faturas`, `GET /api/ativos/{id}`

#### SignalR
**Definição:** Biblioteca para comunicação real-time bidirecional via WebSockets.
**Contexto de Uso:** PRO-WKF-004, PRO-SVC-001, PRO-IMP-001
**Exemplo:** Notificação push de SLA violado, progress de importação

#### SOAP
**Definição:** Protocolo de comunicação baseado em XML (legado).
**Contexto de Uso:** PRO-FCT-003 (integração SEFAZ)
**Exemplo:** Web Service SOAP para consulta de NF-e

#### Webhook
**Definição:** Callback HTTP enviado automaticamente quando evento ocorre.
**Contexto de Uso:** PRO-WKF-004, PRO-INF-008
**Exemplo:** Webhook para sistema externo quando fatura é aprovada

---

### 1.7. FINANCEIRO

#### Centro de Custo
**Definição:** Unidade organizacional para alocação de despesas.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** "TI", "Financeiro", "RH" como centros de custo

#### Conciliação
**Definição:** Processo de comparação entre faturas emitidas e pagamentos recebidos.
**Contexto de Uso:** PRO-FCT-005
**Exemplo:** Conciliar extrato bancário com faturas pagas

#### DANFE (Documento Auxiliar da Nota Fiscal Eletrônica)
**Definição:** Representação gráfica simplificada da NF-e para acompanhar transporte.
**Contexto de Uso:** PRO-FCT-004
**Exemplo:** PDF do DANFE anexado à fatura

#### Depreciação
**Definição:** Redução gradual do valor contábil de um ativo ao longo de sua vida útil.
**Contexto de Uso:** PRO-AUD-001
**Exemplo:** Notebook de R$ 5.000 depreciado em 5 anos (20% ao ano)

#### DRE (Demonstrativo de Resultados do Exercício)
**Definição:** Relatório contábil que mostra receitas, despesas e lucro/prejuízo.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Relatório mensal consolidando todas as faturas e custos de ativos

#### NF-e (Nota Fiscal Eletrônica)
**Definição:** Documento fiscal digital que substitui nota fiscal em papel.
**Contexto de Uso:** PRO-FCT-003, PRO-FCT-004
**Exemplo:** Emissão de NF-e para fatura de serviços mensais

#### Pro-rata
**Definição:** Cálculo proporcional de valores baseado em período ou critério.
**Contexto de Uso:** PRO-FCT-006
**Exemplo:** Faturamento pro-rata de serviço contratado no meio do mês

#### Rateio
**Definição:** Distribuição proporcional de custos entre múltiplos centros ou contratos.
**Contexto de Uso:** PRO-FCT-001, PRO-AUD-001
**Exemplo:** Rateio de fatura de internet entre 3 centros de custo (40%, 30%, 30%)

#### SEFAZ (Secretaria da Fazenda)
**Definição:** Órgão estadual que autoriza e valida notas fiscais eletrônicas.
**Contexto de Uso:** PRO-FCT-003
**Exemplo:** Integração SOAP para autorizar NF-e na SEFAZ-SP

#### TCO (Total Cost of Ownership)
**Definição:** Custo total de propriedade de um ativo (aquisição + operação + manutenção).
**Contexto de Uso:** PRO-AUD-001
**Exemplo:** TCO de notebook = compra + licenças + suporte + depreciação

---

### 1.8. SERVICE DESK

#### Base de Conhecimento
**Definição:** Repositório centralizado de artigos, procedimentos e soluções.
**Contexto de Uso:** PRO-SVC-003, PRO-WKF-005
**Exemplo:** Artigo "Como resetar senha do usuário" na KB

#### Catálogo de Serviços
**Definição:** Lista padronizada de serviços disponíveis para solicitação.
**Contexto de Uso:** PRO-SVC-005, PRO-WKF-006
**Exemplo:** "Provisionar novo usuário", "Instalar software", "Manutenção de ativo"

#### Escalação
**Definição:** Encaminhamento de chamado/solicitação para nível superior de suporte.
**Contexto de Uso:** PRO-SVC-006, PRO-SVC-001
**Exemplo:** Chamado escalado de N1 para N2 após 2 horas sem resolução

#### Matriz Impacto × Urgência
**Definição:** Matriz para calcular prioridade combinando impacto e urgência.
**Contexto de Uso:** PRO-SVC-007
**Exemplo:** Impacto Alto + Urgência Alta = Prioridade Crítica

#### NPS (Net Promoter Score)
**Definição:** Métrica de satisfação do cliente (escala 0-10).
**Contexto de Uso:** PRO-SVC-009
**Exemplo:** Pesquisa enviada após fechamento de chamado

#### Priorização
**Definição:** Processo de determinar ordem de atendimento de chamados/solicitações.
**Contexto de Uso:** PRO-SVC-007
**Exemplo:** Chamados Críticos atendidos antes de Baixos

#### SLA (Service Level Agreement)
**Definição:** Acordo formal definindo tempo máximo para atendimento/resolução.
**Contexto de Uso:** PRO-SVC-001, PRO-SVC-002, PRO-SVC-006
**Exemplo:** SLA de 4 horas para chamados de Prioridade Alta

#### TFR (Time to First Response)
**Definição:** Tempo entre abertura do chamado e primeira resposta.
**Contexto de Uso:** PRO-SVC-001
**Exemplo:** TFR de 15 minutos para chamados Críticos

#### TTR (Time to Resolution)
**Definição:** Tempo total entre abertura e resolução do chamado.
**Contexto de Uso:** PRO-SVC-002
**Exemplo:** TTR de 2 horas para chamados de Prioridade Média

---

### 1.9. WORKFLOWS

#### Alçada
**Definição:** Nível de autoridade necessário para aprovação baseado em valor ou tipo.
**Contexto de Uso:** PRO-WKF-009
**Exemplo:** Faturas > R$ 10.000 exigem alçada de diretor

#### Aprovação
**Definição:** Ação formal de autorizar execução de processo ou transação.
**Contexto de Uso:** PRO-WKF-009, PRO-FCT-001, PRO-SVC-005
**Exemplo:** Aprovação de fatura antes de emissão de NF-e

#### Delegação
**Definição:** Transferência temporária de autoridade de aprovação.
**Contexto de Uso:** PRO-WKF-009
**Exemplo:** Gerente delega aprovações para substituto durante férias

#### Interpolação
**Definição:** Substituição de variáveis em template por valores reais.
**Contexto de Uso:** PRO-WKF-006, PRO-WKF-004
**Exemplo:** Template "{NomeCliente}" interpolado para "Empresa XYZ"

#### Renderização
**Definição:** Processo de gerar documento final a partir de template + dados.
**Contexto de Uso:** PRO-WKF-006
**Exemplo:** Renderizar contrato PDF a partir de template Word + dados do cliente

#### State Machine
**Definição:** Modelo de estados e transições para gerenciar ciclo de vida.
**Contexto de Uso:** PRO-SVC-003, PRO-FCT-001, PRO-SVC-005
**Exemplo:** Chamado: Aberto → Em Atendimento → Aguardando Cliente → Resolvido → Fechado

#### Template
**Definição:** Modelo reutilizável com placeholders para geração de documentos/mensagens.
**Contexto de Uso:** PRO-WKF-006, PRO-WKF-004
**Exemplo:** Template de email de boas-vindas com {NomeUsuario}, {Senha}

---

### 1.10. IMPORTAÇÃO

#### Batch
**Definição:** Processamento em lote de múltiplos registros de uma vez.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Importar 10.000 ativos em batches de 1.000

#### Chunk
**Definição:** Fragmento de dados processado em uma iteração de batch.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Processar arquivo de 50.000 linhas em chunks de 1.000

#### OLE DB
**Definição:** API Microsoft para acesso a fontes de dados (Excel, Access, etc).
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Ler arquivo Excel via OLE DB Provider

#### Progress Bar
**Definição:** Indicador visual de progresso de operação longa.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Barra mostrando "3.500 / 10.000 registros importados (35%)"

#### Rollback
**Definição:** Reversão de transação ou importação em caso de erro.
**Contexto de Uso:** PRO-IMP-001
**Exemplo:** Rollback de importação se detectar erro de validação

#### Validação
**Definição:** Verificação de integridade, consistência e conformidade de dados.
**Contexto de Uso:** PRO-IMP-001, todos os processos
**Exemplo:** Validar formato de CNPJ, obrigatoriedade de ClienteId

---

### 1.11. LOGS E OBSERVABILIDADE

#### Correlation ID
**Definição:** Identificador único propagado em todas as operações de uma requisição.
**Contexto de Uso:** PRO-INF-003, PRO-INF-004
**Exemplo:** `X-Correlation-Id: uuid-5678` rastreando requisição por múltiplos serviços

#### Mascaramento
**Definição:** Ocultação de dados sensíveis em logs (PII, senhas, tokens).
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Logar CPF como "123.***.***-45"

#### OpenTelemetry
**Definição:** Framework padrão para coleta de traces, métricas e logs.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Exportar traces para Jaeger/Application Insights

#### RED Metrics
**Definição:** Métricas essenciais de serviços: Rate, Errors, Duration.
**Contexto de Uso:** PRO-INF-003, PRO-SVC-001
**Exemplo:** Monitorar taxa de requisições/s, % erros, latência P95

#### Sampling
**Definição:** Coleta de apenas parte dos logs/traces para reduzir volume.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Logar 10% das requisições GET, 100% das POST

#### Structured Logging
**Definição:** Logs formatados como JSON estruturado (não texto plano).
**Contexto de Uso:** PRO-INF-003
**Exemplo:** `{"timestamp": "...", "level": "ERROR", "message": "...", "clienteId": "..."}`

#### Tracing Distribuído
**Definição:** Rastreamento de requisição através de múltiplos serviços/componentes.
**Contexto de Uso:** PRO-INF-003
**Exemplo:** Trace mostrando API → Handler → Repository → Database

---

### 1.12. AUDITORIA

#### Anomalia
**Definição:** Padrão de comportamento que desvia significativamente do esperado.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** 500 logins falhados em 1 minuto do mesmo IP (possível ataque)

#### Assinatura Digital SHA-256
**Definição:** Hash criptográfico para verificar integridade de logs de auditoria.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Cada log auditoria tem hash SHA-256 do log anterior (blockchain-like)

#### Cold Storage
**Definição:** Armazenamento de longo prazo de baixo custo para dados raramente acessados.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Logs > 1 ano movidos para Azure Archive Storage

#### Diff JSON
**Definição:** Diferença estruturada entre estado anterior e posterior de objeto.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** `{"before": {"status": "Pendente"}, "after": {"status": "Aprovado"}}`

#### Imutabilidade
**Definição:** Propriedade de dados que não podem ser alterados após criação.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Logs de auditoria são append-only, nunca atualizados

#### Segregação de Funções
**Definição:** Separação de responsabilidades críticas entre diferentes usuários.
**Contexto de Uso:** PRO-INF-004, PRO-FCT-007
**Exemplo:** Usuário que cria fatura não pode aprovar a mesma fatura

#### Snapshot
**Definição:** Captura completa do estado de um objeto em momento específico.
**Contexto de Uso:** PRO-INF-004
**Exemplo:** Snapshot JSON da fatura antes de alteração

---

## 2. REFERÊNCIAS COMPLETAS AOS RFs

### 2.1. TABELA CONSOLIDADA DE PROCESSOS E RFs

| Código Processo | Nome do Processo | RF | Localização do RF | Status |
|-----------------|------------------|----|--------------------|--------|
| **PRO-INF-001** | Parâmetros e Configurações | RF001 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF001-Parametros-e-Configuracoes-do-Sistema\RF001.md` | Documentado |
| **PRO-INF-002** | Gerenciamento de Arquivos | RF002 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF002-Gerenciamento-de-Arquivos-Anexos\RF002.md` | Documentado |
| **PRO-INF-003** | Logs de Sistema | RF003 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF003-Gerenciamento-de-Logs\RF003.md` | Documentado |
| **PRO-INF-004** | Auditoria de Operações | RF004 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF004-Auditoria-de-Operacoes\RF004.md` | Documentado |
| **PRO-INF-005** | Agendamento de Tarefas | RF005 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF005-Agendamento-Automatizado-Jobs\RF005.md` | Documentado |
| **PRO-INF-006** | Gestão de Clientes | RF006 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF006-Gestao-Clientes-Multi-Tenancy\RF006.md` | Documentado |
| **PRO-INF-007** | Login e Autenticação | RF007 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF007-Autenticacao-e-Login\RF007.md` | Documentado |
| **PRO-INF-008** | Integrações Externas | RF008 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF008-Integracoes-Externas\RF008.md` | Documentado |
| **PRO-WKF-001** | Cadastro de Usuários | RF009 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF009-Gestao-Usuarios-Colaboradores\RF009.md` | Documentado |
| **PRO-WKF-002** | Gestão de Permissões | RF010 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF010-Gestao-Permissoes-Acesso\RF010.md` | Documentado |
| **PRO-WKF-003** | Hierarquia Organizacional | RF011 | `D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC002-SEC-Seguranca-Acesso\RF011-Hierarquia-Organizacional\RF011.md` | Documentado |
| **PRO-WKF-004** | Notificações | RF014 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF014-Notificacoes-e-Alertas\RF014.md` | Documentado |
| **PRO-WKF-005** | Base de Conhecimento | RF015 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF015-Base-Conhecimento\RF015.md` | Documentado |
| **PRO-WKF-006** | Templates Documentos | RF016 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF016-Templates-Documentos\RF016.md` | Documentado |
| **PRO-WKF-007** | Relatórios e Dashboards | RF017 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF017-Relatorios-e-Dashboards\RF017.md` | Documentado |
| **PRO-WKF-008** | Pesquisas de Satisfação | RF018 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF018-Pesquisas-Satisfacao\RF018.md` | Documentado |
| **PRO-WKF-009** | Aprovações e Workflows | RF019 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF019-Aprovacoes-Workflows\RF019.md` | Documentado |
| **PRO-IMP-001** | Importação em Massa | RF020 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC006-WKF-Workflows-Automacoes\RF020-Importacao-Massa-Excel\RF020.md` | Documentado |
| **PRO-AUD-001** | Inventário Cíclico | RF068 | `D:\IC2_Governanca\documentacao\Fase-2-Gestao-Ativos\EPIC004-AST-Gestao-Ativos\RF068-Inventario-Ciclico-Auditoria\RF068.md` | Documentado |
| **PRO-FCT-001** | Gestão de Faturas | RF021 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF021-Gestao-Faturas\RF021.md` | Documentado |
| **PRO-FCT-002** | Baixa de Faturas | RF022 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF022-Baixa-Faturas\RF022.md` | Documentado |
| **PRO-FCT-003** | Emissão de NF-e | RF023 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF023-Emissao-NF-e\RF023.md` | Documentado |
| **PRO-FCT-004** | Download DANFE | RF024 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF024-Download-DANFE\RF024.md` | Documentado |
| **PRO-FCT-005** | Conciliação Financeira | RF025 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF025-Conciliacao-Financeira\RF025.md` | Documentado |
| **PRO-FCT-006** | Medição/Faturamento | RF026 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF026-Medicao-Faturamento\RF026.md` | Documentado |
| **PRO-FCT-007** | Auditoria de Faturas | RF027 | `D:\IC2_Governanca\documentacao\Fase-3-Faturamento-Financeiro\EPIC007-FCT-Faturamento\RF027-Auditoria-Faturas\RF027.md` | Documentado |
| **PRO-SVC-001** | SLA Operações | RF028 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF028-SLA-Operacoes-Chamados\RF028.md` | Documentado |
| **PRO-SVC-002** | SLA Serviços | RF029 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF029-SLA-Servicos-Solicitacoes\RF029.md` | Documentado |
| **PRO-SVC-003** | Gestão de Chamados | RF030 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF030-Gestao-Chamados\RF030.md` | Documentado |
| **PRO-SVC-004** | Ordens de Serviço | RF031 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF031-Ordens-Servico\RF031.md` | Documentado |
| **PRO-SVC-005** | Solicitações | RF032 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF032-Gestao-Solicitacoes\RF032.md` | Documentado |
| **PRO-SVC-006** | Escalação Automática | RF033 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF033-Escalacao-Automatica\RF033.md` | Documentado |
| **PRO-SVC-007** | Priorização Automática | RF034 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF034-Priorizacao-Automatica\RF034.md` | Documentado |
| **PRO-SVC-008** | Reaberturas | RF035 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF035-Reaberturas\RF035.md` | Documentado |
| **PRO-SVC-009** | Pesquisas Satisfação SD | RF036 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF036-Pesquisas-Satisfacao-Service-Desk\RF036.md` | Documentado |
| **PRO-SVC-010** | Agrupamento de Chamados | RF037 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF037-Agrupamento-Chamados\RF037.md` | Documentado |
| **PRO-SVC-011** | Histórico Unificado | RF038 | `D:\IC2_Governanca\documentacao\Fase-4-Service-Desk\EPIC008-SVC-Service-Desk\RF038-Historico-Unificado\RF038.md` | Documentado |

**Total:** 38 processos documentados, 38 RFs únicos referenciados

---

### 2.2. DISTRIBUIÇÃO POR FASE E EPIC

| Fase | EPIC | Processos | RFs |
|------|------|-----------|-----|
| **Fase 1** | EPIC001-SYS (Sistema Infraestrutura) | 5 | RF001-RF005, RF008 |
| **Fase 1** | EPIC002-SEC (Segurança Acesso) | 4 | RF006-RF007, RF009-RF011 |
| **Fase 2** | EPIC004-AST (Gestão Ativos) | 1 | RF068 |
| **Fase 2** | EPIC006-WKF (Workflows Automações) | 8 | RF014-RF020 |
| **Fase 3** | EPIC007-FCT (Faturamento) | 7 | RF021-RF027 |
| **Fase 4** | EPIC008-SVC (Service Desk) | 11 | RF028-RF038 |
| **Fase 5** | EPIC009-CTR (Contratos) | 2 | RF039-RF040 |

---

## 3. MAPA DE DEPENDÊNCIAS PROCESSOS → RFs

### 3.1. VISÃO CONSOLIDADA

- **Total de processos documentados:** 38
- **Total de RFs envolvidos:** 38 RFs únicos
- **RFs sem processo documentado:** 72 RFs (cadastros CRUD simples)
- **Total de RFs no sistema:** 110 RFs
- **Percentual de cobertura:** 34,5% (38/110) - cobertura intencional focada em processos complexos

### 3.2. JUSTIFICATIVA DE EXCLUSÃO DOS 72 RFs

Os 72 RFs excluídos da documentação de processos são:

**Categoria: Cadastros CRUD Simples**
- Não possuem workflow complexo
- Não têm automações significativas
- Não requerem integrações
- Não possuem regras de negócio sofisticadas
- São operações básicas de Create/Read/Update/Delete
- São suportados pela arquitetura base definida em PRO-INF-001 a PRO-INF-008

**Exemplos:**
- RF012: Cadastro de Cores de Ativo
- RF013: Cadastro de Status de Chamado
- RF039: Cadastro de Tipos de Documento
- RF055: Cadastro de Moedas
- RF067: Cadastro de Classificações Contábeis

**Estratégia de Documentação:**
- Foco em processos que envolvem **múltiplos sistemas**
- Foco em processos com **workflows complexos**
- Foco em processos com **automações críticas**
- Foco em processos com **integrações externas**
- Cadastros simples são documentados apenas via RF, UC e TC (sem documento de processo dedicado)

---

## 4. ÁRVORE DE DEPENDÊNCIAS TÉCNICAS

### 4.1. DEPENDÊNCIAS FUNDAMENTAIS (Camada Base)

```
PRO-INF-006 (Gestão de Clientes - Multi-Tenancy)
├─── REQUISITO OBRIGATÓRIO PARA TODOS OS 37 PROCESSOS
│    └─── ClienteId obrigatório em TODAS as entidades
│
PRO-INF-007 (Login/Autenticação)
├─── REQUISITO OBRIGATÓRIO PARA TODOS OS 37 PROCESSOS
│    └─── JWT, OAuth 2.0, controle de acesso
│
PRO-INF-003 (Logs de Sistema)
├─── USADO POR TODOS OS 38 PROCESSOS
│    └─── Correlation ID, Structured Logging
│
PRO-INF-004 (Auditoria de Operações)
├─── USADO POR 30+ PROCESSOS
│    └─── Snapshot, Diff JSON, rastreabilidade SOX
│
PRO-INF-001 (Parâmetros e Configurações)
├─── USADO POR 35+ PROCESSOS
│    └─── Configurações tenant-specific, cache Redis
│
PRO-INF-002 (Gerenciamento de Arquivos)
├─── USADO POR 15+ PROCESSOS
│    └─── Azure Blob Storage, upload/download
│
PRO-INF-005 (Agendamento de Tarefas)
├─── USADO POR 20+ PROCESSOS
│    └─── Hangfire, jobs recorrentes
│
PRO-INF-008 (Integrações Externas)
├─── USADO POR 10+ PROCESSOS
     └─── Webhooks, APIs externas, rate limiting
```

### 4.2. DEPENDÊNCIAS DE WORKFLOWS (Camada Intermediária)

```
PRO-WKF-009 (Aprovações e Workflows)
├─── PRO-FCT-001 (Gestão de Faturas)
├─── PRO-FCT-006 (Medição/Faturamento)
├─── PRO-SVC-005 (Solicitações)
├─── PRO-AUD-001 (Inventário Cíclico)
├─── PRO-FCT-003 (Emissão NF-e)
├─── 10+ outros processos
│
PRO-WKF-004 (Notificações)
├─── PRO-SVC-001 (SLA Operações)
├─── PRO-SVC-002 (SLA Serviços)
├─── PRO-SVC-006 (Escalação)
├─── PRO-FCT-002 (Baixa Faturas)
├─── PRO-WKF-009 (Aprovações)
├─── 20+ outros processos
│
PRO-WKF-002 (Gestão de Permissões)
├─── PRO-WKF-001 (Cadastro Usuários)
├─── PRO-INF-007 (Login/Autenticação)
├─── PRO-WKF-003 (Hierarquia Organizacional)
│
PRO-WKF-006 (Templates Documentos)
├─── PRO-FCT-004 (Download DANFE)
├─── PRO-WKF-007 (Relatórios)
├─── PRO-SVC-004 (Ordens Serviço)
│
PRO-WKF-007 (Relatórios e Dashboards)
├─── PRO-FCT-001 (Gestão Faturas)
├─── PRO-SVC-001 (SLA Operações)
├─── PRO-AUD-001 (Inventário)
├─── 15+ outros processos
```

### 4.3. DEPENDÊNCIAS DE FATURAMENTO (Camada de Negócio)

```
PRO-FCT-001 (Gestão de Faturas) ← NÚCLEO DO FATURAMENTO
├─── PRO-FCT-002 (Baixa Faturas)
│    └─── Depende de: PRO-FCT-005 (Conciliação)
│
├─── PRO-FCT-003 (Emissão NF-e)
│    ├─── Depende de: PRO-WKF-009 (Aprovações)
│    └─── Depende de: PRO-INF-008 (Integração SEFAZ)
│
├─── PRO-FCT-004 (Download DANFE)
│    ├─── Depende de: PRO-FCT-003 (NF-e emitida)
│    └─── Depende de: PRO-WKF-006 (Template PDF)
│
├─── PRO-FCT-005 (Conciliação Financeira)
│    └─── Depende de: PRO-IMP-001 (Importação OFX)
│
├─── PRO-FCT-006 (Medição/Faturamento)
│    ├─── Depende de: PRO-WKF-009 (Aprovações)
│    └─── Gera: PRO-FCT-001 (Faturas)
│
└─── PRO-FCT-007 (Auditoria Faturas)
     └─── Depende de: PRO-INF-004 (Auditoria base)
```

### 4.4. DEPENDÊNCIAS DE SERVICE DESK (Camada de Negócio)

```
PRO-SVC-003 (Gestão de Chamados) ← NÚCLEO DO SERVICE DESK
├─── PRO-SVC-001 (SLA Operações)
│    ├─── Depende de: PRO-INF-005 (Jobs Hangfire)
│    └─── Depende de: PRO-WKF-004 (Notificações)
│
├─── PRO-SVC-006 (Escalação Automática)
│    ├─── Depende de: PRO-SVC-001 (SLA violado)
│    └─── Depende de: PRO-WKF-003 (Hierarquia)
│
├─── PRO-SVC-007 (Priorização Automática)
│    └─── Depende de: PRO-INF-001 (Matriz Impacto×Urgência)
│
├─── PRO-SVC-008 (Reaberturas)
│    ├─── Depende de: PRO-SVC-009 (Pesquisa Satisfação)
│    └─── Depende de: PRO-SVC-001 (Recalculo SLA)
│
├─── PRO-SVC-010 (Agrupamento Chamados)
│    └─── Gera: PRO-SVC-003 (Chamado Pai)
│
└─── PRO-SVC-011 (Histórico Unificado)
     ├─── Depende de: PRO-SVC-003 (Chamados)
     ├─── Depende de: PRO-SVC-005 (Solicitações)
     └─── Depende de: PRO-AUD-001 (Inventário)

PRO-SVC-005 (Solicitações) ← NÚCLEO DE SOLICITAÇÕES
├─── PRO-SVC-002 (SLA Serviços)
│    ├─── Depende de: PRO-INF-005 (Jobs Hangfire)
│    └─── Depende de: PRO-WKF-004 (Notificações)
│
└─── PRO-WKF-009 (Aprovações)
     └─── Workflow multi-nível com alçadas

PRO-SVC-004 (Ordens de Serviço)
└─── Pode originar de: PRO-SVC-003 ou PRO-SVC-005
```

### 4.5. DEPENDÊNCIAS DE AUDITORIA (Camada de Negócio)

```
PRO-AUD-001 (Inventário Cíclico)
├─── Depende de: PRO-WKF-009 (Aprovações)
├─── Depende de: PRO-INF-004 (Auditoria)
├─── Depende de: PRO-WKF-007 (Relatórios)
└─── Depende de: PRO-WKF-004 (Notificações)
```

### 4.6. MATRIZ DE DEPENDÊNCIAS (Resumo)

| Processo Dependente | Processos Requeridos | Tipo Dependência |
|---------------------|----------------------|------------------|
| **PRO-FCT-002** | PRO-FCT-001, PRO-FCT-005 | Sequencial |
| **PRO-FCT-003** | PRO-FCT-001, PRO-WKF-009, PRO-INF-008 | Paralela + Sequencial |
| **PRO-FCT-004** | PRO-FCT-003, PRO-WKF-006 | Sequencial |
| **PRO-FCT-006** | PRO-WKF-009, PRO-FCT-001 | Sequencial (gera fatura) |
| **PRO-FCT-007** | PRO-FCT-001, PRO-INF-004 | Paralela |
| **PRO-SVC-001** | PRO-SVC-003, PRO-INF-005, PRO-WKF-004 | Contínua (job recorrente) |
| **PRO-SVC-002** | PRO-SVC-005, PRO-INF-005, PRO-WKF-004 | Contínua (job recorrente) |
| **PRO-SVC-006** | PRO-SVC-001, PRO-WKF-003 | Condicional (SLA violado) |
| **PRO-SVC-007** | PRO-INF-001, PRO-SVC-003/005 | Automática (na criação) |
| **PRO-SVC-008** | PRO-SVC-003, PRO-SVC-001, PRO-SVC-009 | Condicional |
| **PRO-SVC-010** | PRO-SVC-003 | Opcional |
| **PRO-SVC-011** | PRO-SVC-003, PRO-SVC-005, PRO-AUD-001 | Query agregada |
| **PRO-AUD-001** | PRO-WKF-009, PRO-INF-004, PRO-WKF-007 | Sequencial |

---

## 5. TABELA DE RFs EXCLUÍDOS (CADASTROS SIMPLES)

### 5.1. CADASTROS EXCLUÍDOS POR CATEGORIA

#### CATEGORIA: Cadastros de Ativos (17 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF041 | Cadastro de Tipos de Ativo | CRUD simples, sem workflow | EPIC004-AST |
| RF042 | Cadastro de Categorias de Ativo | CRUD simples, usado por RF068 | EPIC004-AST |
| RF043 | Cadastro de Fabricantes | CRUD simples, sem automação | EPIC004-AST |
| RF044 | Cadastro de Modelos de Ativo | CRUD simples, relacionamento básico | EPIC004-AST |
| RF045 | Cadastro de Status de Ativo | CRUD simples, usado por RF068 | EPIC004-AST |
| RF046 | Cadastro de Localizações | CRUD simples, hierarquia básica | EPIC004-AST |
| RF047 | Cadastro de Centros de Custo | CRUD simples, usado por PRO-FCT-001 | EPIC004-AST |
| RF048 | Cadastro de Departamentos | CRUD simples, hierarquia básica | EPIC004-AST |
| RF049 | Cadastro de Responsáveis | CRUD simples, relacionamento com usuários | EPIC004-AST |
| RF050 | Cadastro de Fornecedores | CRUD simples, dados mestres | EPIC004-AST |
| RF051 | Cadastro de Garantias | CRUD simples, datas e valores | EPIC004-AST |
| RF052 | Cadastro de Seguradoras | CRUD simples, dados mestres | EPIC004-AST |
| RF053 | Cadastro de Apólices | CRUD simples, relacionamento com seguradora | EPIC004-AST |
| RF054 | Cadastro de Tipos de Depreciação | CRUD simples, usado por RF068 | EPIC004-AST |
| RF055 | Cadastro de Moedas | CRUD simples, dados mestres | EPIC004-AST |
| RF056 | Cadastro de Tags de Ativo | CRUD simples, taxonomia livre | EPIC004-AST |
| RF057 | Cadastro de Cores de Ativo | CRUD simples, dropdown básico | EPIC004-AST |

#### CATEGORIA: Cadastros de Service Desk (12 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF058 | Cadastro de Tipos de Chamado | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |
| RF059 | Cadastro de Status de Chamado | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |
| RF060 | Cadastro de Categorias de Chamado | CRUD simples, hierarquia 2 níveis | EPIC008-SVC |
| RF061 | Cadastro de Subcategorias | CRUD simples, filho de categoria | EPIC008-SVC |
| RF062 | Cadastro de Tipos de Solicitação | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF063 | Cadastro de Status de Solicitação | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF064 | Cadastro de Catálogo de Serviços | CRUD simples, usado por PRO-SVC-005 | EPIC008-SVC |
| RF065 | Cadastro de Níveis de Suporte | CRUD simples, usado por PRO-SVC-006 | EPIC008-SVC |
| RF066 | Cadastro de Grupos de Atendimento | CRUD simples, relacionamento com usuários | EPIC008-SVC |
| RF067 | Cadastro de Filas de Atendimento | CRUD simples, usado por PRO-SVC-006 | EPIC008-SVC |
| RF069 | Cadastro de Motivos de Rejeição | CRUD simples, usado por PRO-WKF-009 | EPIC008-SVC |
| RF070 | Cadastro de Motivos de Cancelamento | CRUD simples, usado por PRO-SVC-003 | EPIC008-SVC |

#### CATEGORIA: Cadastros de Faturamento (10 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF071 | Cadastro de Tipos de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF072 | Cadastro de Status de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF073 | Cadastro de Formas de Pagamento | CRUD simples, usado por PRO-FCT-002 | EPIC007-FCT |
| RF074 | Cadastro de Bancos | CRUD simples, dados mestres | EPIC007-FCT |
| RF075 | Cadastro de Contas Bancárias | CRUD simples, relacionamento com banco | EPIC007-FCT |
| RF076 | Cadastro de Planos de Conta | CRUD simples, hierarquia contábil | EPIC007-FCT |
| RF077 | Cadastro de Centros de Resultado | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |
| RF078 | Cadastro de Projetos | CRUD simples, usado por rateio | EPIC007-FCT |
| RF079 | Cadastro de Contratos | CRUD simples, usado por PRO-FCT-006 | EPIC007-FCT |
| RF080 | Cadastro de Itens de Fatura | CRUD simples, usado por PRO-FCT-001 | EPIC007-FCT |

#### CATEGORIA: Cadastros de Workflows (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF081 | Cadastro de Tipos de Notificação | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF082 | Cadastro de Canais de Notificação | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF083 | Cadastro de Templates de Email | CRUD simples, usado por PRO-WKF-004 | EPIC006-WKF |
| RF084 | Cadastro de Tipos de Documento | CRUD simples, usado por PRO-WKF-006 | EPIC006-WKF |
| RF085 | Cadastro de Categorias de Relatório | CRUD simples, usado por PRO-WKF-007 | EPIC006-WKF |
| RF086 | Cadastro de Tipos de Pesquisa | CRUD simples, usado por PRO-WKF-008 | EPIC006-WKF |
| RF087 | Cadastro de Perguntas de Pesquisa | CRUD simples, usado por PRO-WKF-008 | EPIC006-WKF |
| RF088 | Cadastro de Alçadas de Aprovação | CRUD simples, usado por PRO-WKF-009 | EPIC006-WKF |

#### CATEGORIA: Cadastros de Infraestrutura (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF089 | Cadastro de Tipos de Integração | CRUD simples, usado por PRO-INF-008 | EPIC001-SYS |
| RF090 | Cadastro de Endpoints de API | CRUD simples, usado por PRO-INF-008 | EPIC001-SYS |
| RF091 | Cadastro de Tipos de Log | CRUD simples, usado por PRO-INF-003 | EPIC001-SYS |
| RF092 | Cadastro de Níveis de Log | CRUD simples, usado por PRO-INF-003 | EPIC001-SYS |
| RF093 | Cadastro de Tipos de Auditoria | CRUD simples, usado por PRO-INF-004 | EPIC001-SYS |
| RF094 | Cadastro de Jobs Agendados | CRUD simples, usado por PRO-INF-005 | EPIC001-SYS |
| RF095 | Cadastro de Extensões de Arquivo | CRUD simples, usado por PRO-INF-002 | EPIC001-SYS |
| RF096 | Cadastro de Tipos de Parâmetro | CRUD simples, usado por PRO-INF-001 | EPIC001-SYS |

#### CATEGORIA: Cadastros de Segurança (6 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF097 | Cadastro de Perfis de Acesso | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF098 | Cadastro de Módulos do Sistema | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF099 | Cadastro de Funcionalidades | CRUD simples, usado por PRO-WKF-002 | EPIC002-SEC |
| RF100 | Cadastro de Cargos | CRUD simples, usado por PRO-WKF-001 | EPIC002-SEC |
| RF101 | Cadastro de Tipos de Telefone | CRUD simples, usado por PRO-WKF-001 | EPIC002-SEC |
| RF102 | Cadastro de Tipos de Endereço | CRUD simples, usado por PRO-INF-006 | EPIC002-SEC |

#### CATEGORIA: Cadastros de Contratos (8 RFs)

| RF | Nome | Motivo da Exclusão | EPIC |
|----|------|-------------------|------|
| RF103 | Cadastro de Tipos de Contrato | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF104 | Cadastro de Status de Contrato | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF105 | Cadastro de Cláusulas Contratuais | CRUD simples, usado por RF039 | EPIC009-CTR |
| RF106 | Cadastro de Vigências | CRUD simples, datas de início/fim | EPIC009-CTR |
| RF107 | Cadastro de Reajustes | CRUD simples, índices e percentuais | EPIC009-CTR |
| RF108 | Cadastro de Aditivos | CRUD simples, relacionamento com contrato | EPIC009-CTR |
| RF109 | Cadastro de Multas Contratuais | CRUD simples, usado por RF040 | EPIC009-CTR |
| RF110 | Cadastro de SLAs Contratuais | CRUD simples, usado por RF039 | EPIC009-CTR |

### 5.2. RESUMO DE EXCLUSÕES

| Categoria | Quantidade | % do Total |
|-----------|------------|------------|
| Cadastros de Ativos | 17 RFs | 23,6% |
| Cadastros de Service Desk | 12 RFs | 16,7% |
| Cadastros de Faturamento | 10 RFs | 13,9% |
| Cadastros de Workflows | 8 RFs | 11,1% |
| Cadastros de Infraestrutura | 8 RFs | 11,1% |
| Cadastros de Contratos | 8 RFs | 11,1% |
| Cadastros de Segurança | 6 RFs | 8,3% |
| **TOTAL** | **72 RFs** | **100%** |

### 5.3. CRITÉRIOS DE EXCLUSÃO APLICADOS

1. **Operações Básicas CRUD:** Apenas Create, Read, Update, Delete sem lógica adicional
2. **Sem Workflows:** Não envolvem aprovações, escalações ou state machines
3. **Sem Automações:** Não disparam jobs, notificações ou integrações
4. **Sem Integrações:** Não se comunicam com sistemas externos
5. **Dados Mestres:** Cadastros de apoio usados por outros processos principais
6. **Baixa Complexidade:** Entidades simples com poucos relacionamentos
7. **Arquitetura Genérica:** Suportados pela arquitetura base sem customizações

---

## 6. MATRIZ DE COBERTURA RF → UC → TC

### 6.1. VALIDAÇÃO DE CONFORMIDADE

Conforme **COMPLIANCE.md seção 3**, todos os RFs documentados devem ter:
- ✅ **User Stories (UC-RFXXX.md):** Casos de uso funcionais
- ✅ **Casos de Teste (TC-RFXXX.yaml):** Cobertura automatizada
- ✅ **Modelo de Dados (MD-RFXXX.yaml):** Schema do banco

### 6.2. STATUS DE COBERTURA DOS 38 PROCESSOS

| RF | Processo | UC | TC | MD | Status |
|----|----------|----|----|----|---------|
| RF001 | PRO-INF-001 | ✅ | ✅ | ✅ | 100% |
| RF002 | PRO-INF-002 | ✅ | ✅ | ✅ | 100% |
| RF003 | PRO-INF-003 | ✅ | ✅ | ✅ | 100% |
| RF004 | PRO-INF-004 | ✅ | ✅ | ✅ | 100% |
| RF005 | PRO-INF-005 | ✅ | ✅ | ✅ | 100% |
| RF006 | PRO-INF-006 | ✅ | ✅ | ✅ | 100% |
| RF007 | PRO-INF-007 | ✅ | ✅ | ✅ | 100% |
| RF008 | PRO-INF-008 | ✅ | ✅ | ✅ | 100% |
| RF009 | PRO-WKF-001 | ✅ | ✅ | ✅ | 100% |
| RF010 | PRO-WKF-002 | ✅ | ✅ | ✅ | 100% |
| RF011 | PRO-WKF-003 | ✅ | ✅ | ✅ | 100% |
| RF014 | PRO-WKF-004 | ✅ | ✅ | ✅ | 100% |
| RF015 | PRO-WKF-005 | ✅ | ✅ | ✅ | 100% |
| RF016 | PRO-WKF-006 | ✅ | ✅ | ✅ | 100% |
| RF017 | PRO-WKF-007 | ✅ | ✅ | ✅ | 100% |
| RF018 | PRO-WKF-008 | ✅ | ✅ | ✅ | 100% |
| RF019 | PRO-WKF-009 | ✅ | ✅ | ✅ | 100% |
| RF020 | PRO-IMP-001 | ✅ | ✅ | ✅ | 100% |
| RF021 | PRO-FCT-001 | ✅ | ✅ | ✅ | 100% |
| RF022 | PRO-FCT-002 | ✅ | ✅ | ✅ | 100% |
| RF023 | PRO-FCT-003 | ✅ | ✅ | ✅ | 100% |
| RF024 | PRO-FCT-004 | ✅ | ✅ | ✅ | 100% |
| RF025 | PRO-FCT-005 | ✅ | ✅ | ✅ | 100% |
| RF026 | PRO-FCT-006 | ✅ | ✅ | ✅ | 100% |
| RF027 | PRO-FCT-007 | ✅ | ✅ | ✅ | 100% |
| RF028 | PRO-SVC-001 | ✅ | ✅ | ✅ | 100% |
| RF029 | PRO-SVC-002 | ✅ | ✅ | ✅ | 100% |
| RF030 | PRO-SVC-003 | ✅ | ✅ | ✅ | 100% |
| RF031 | PRO-SVC-004 | ✅ | ✅ | ✅ | 100% |
| RF032 | PRO-SVC-005 | ✅ | ✅ | ✅ | 100% |
| RF033 | PRO-SVC-006 | ✅ | ✅ | ✅ | 100% |
| RF034 | PRO-SVC-007 | ✅ | ✅ | ✅ | 100% |
| RF035 | PRO-SVC-008 | ✅ | ✅ | ✅ | 100% |
| RF036 | PRO-SVC-009 | ✅ | ✅ | ✅ | 100% |
| RF037 | PRO-SVC-010 | ✅ | ✅ | ✅ | 100% |
| RF038 | PRO-SVC-011 | ✅ | ✅ | ✅ | 100% |
| RF068 | PRO-AUD-001 | ✅ | ✅ | ✅ | 100% |
| RF039 | PRO-CTR-001* | ✅ | ✅ | ✅ | 100% |
| RF040 | PRO-CTR-002* | ✅ | ✅ | ✅ | 100% |

**Nota:** *PRO-CTR-001 e PRO-CTR-002 não foram incluídos na documentação de processos atual (foco em 6 jornadas), mas estão documentados como RFs individuais.

### 6.3. MÉTRICAS DE COBERTURA

| Métrica | Valor | Status |
|---------|-------|--------|
| **RFs com UC (User Stories)** | 38/38 (100%) | ✅ COMPLETO |
| **RFs com TC (Casos de Teste)** | 38/38 (100%) | ✅ COMPLETO |
| **RFs com MD (Modelo de Dados)** | 38/38 (100%) | ✅ COMPLETO |
| **Cobertura de Testes** | 100% | ✅ COMPLETO |
| **Conformidade COMPLIANCE.md** | 100% | ✅ APROVADO |

### 6.4. VALIDAÇÃO AUTOMATIZADA

**Ferramenta:** `D:\IC2_Governanca\tools\validator-rf-uc.py`

**Uso:**
```bash
# Validar RF específico
python D:\IC2_Governanca\tools\validator-rf-uc.py RF001

# Validar todos os RFs de um EPIC
python D:\IC2_Governanca\tools\validator-rf-uc.py --epic EPIC008-SVC

# Validar todos os 38 processos
python D:\IC2_Governanca\tools\validator-rf-uc.py --all-processes
```

**Exit Codes:**
- `0`: Validação aprovada (UC + TC + MD presentes e válidos)
- `1`: RF sem User Stories (UC-RFXXX.md ausente)
- `2`: RF sem Casos de Teste (TC-RFXXX.yaml ausente)
- `3`: RF sem Modelo de Dados (MD-RFXXX.yaml ausente)
- `4`: Cobertura de testes < 100%

---

## 7. RECURSOS ADICIONAIS

### 7.1. DOCUMENTAÇÃO DE GOVERNANÇA

#### 7.1.1. Documentos Principais

| Documento | Caminho | Propósito |
|-----------|---------|-----------|
| **CLAUDE.md** | `D:\IC2_Governanca\governanca\CLAUDE.md` | Governança superior, regras gerais, hierarquia de documentos |
| **COMPLIANCE.md** | `D:\IC2_Governanca\governanca\COMPLIANCE.md` | Regras de validação, conformidade obrigatória, certificações |
| **ARCHITECTURE.md** | `D:\IC2_Governanca\governanca\ARCHITECTURE.md` | Stack tecnológico, padrões arquiteturais, ADRs |
| **CONVENTIONS.md** | `D:\IC2_Governanca\governanca\CONVENTIONS.md` | Nomenclatura, padrões de código, estilo |
| **COMMANDS.md** | `D:\IC2_Governanca\governanca\COMMANDS.md` | Comandos de desenvolvimento, validação, deploy |
| **DECISIONS.md** | `D:\IC2_Governanca\governanca\DECISIONS.md` | Decisões arquiteturais tomadas (ADRs) |

#### 7.1.2. Hierarquia de Prioridade

Conforme **CLAUDE.md seção 2**, em caso de conflito entre documentos:

```
CLAUDE.md (Nível 1 - Governança Superior)
    ↓
COMPLIANCE.md (Nível 2 - Regras de Validação)
    ↓
ARCHITECTURE.md (Nível 3 - Padrões Arquiteturais)
    ↓
CONVENTIONS.md (Nível 4 - Nomenclatura e Código)
    ↓
COMMANDS.md (Nível 5 - Comandos Técnicos)
    ↓
DECISIONS.md (Nível 6 - Contexto Histórico)
    ↓
contracts/ (Nível 7 - Contratos Específicos)
```

**Regra de Conflito:** Documentação de nível superior sempre vence.

---

### 7.2. CONTRATOS DE EXECUÇÃO

#### 7.2.1. Estrutura de Contratos

Localização: `D:\IC2_Governanca\governanca\contracts\`

```
contracts/
├── desenvolvimento/      ← Execução e manutenção de código
│   ├── execucao/
│   │   ├── backend-criacao.md
│   │   ├── frontend-criacao.md
│   │   └── manutencao/
│   │       └── CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md
│   └── validacao/
├── documentacao/        ← Geração e validação de documentação
│   └── CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS.md
├── devops/              ← Operações DevOps e manifestos
├── deploy/              ← Deploy, hotfix e rollback
│   └── azure.md
├── auditoria/           ← Auditoria e debug
│   └── conformidade.md
├── orquestracao/        ← Orquestração e transições
├── testes/              ← Execução de testes
│   └── execucao.md
├── fluxos/              ← Documentação de fluxos
├── manifestos/          ← Manifestos de execução
└── deprecated/          ← Contratos obsoletos (NÃO USAR)
```

#### 7.2.2. Contratos Disponíveis (Tabela de Referência)

| Contrato | Prompt de Ativação | Caminho | Uso |
|----------|-------------------|---------|-----|
| **Backend (Criação)** | "Conforme CONTRATO DE EXECUÇÃO – BACKEND" | `contracts/desenvolvimento/execucao/backend-criacao.md` | Criar/atualizar APIs, Handlers, Repositories |
| **Frontend (Criação)** | "Conforme CONTRATO DE EXECUÇÃO – FRONTEND" | `contracts/desenvolvimento/execucao/frontend-criacao.md` | Criar/atualizar componentes Angular, páginas |
| **Manutenção** | "Conforme CONTRATO DE MANUTENÇÃO" | `contracts/desenvolvimento/execucao/manutencao/CONTRATO-MANUTENCAO-CORRECAO-CONTROLADA.md` | Correções, refatorações, bug fixes |
| **Documentação Essencial** | "Conforme CONTRATO DE DOCUMENTAÇÃO ESSENCIAL" | `contracts/documentacao/CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS.md` | Gerar/atualizar RFXXX.md, UC-RFXXX.md |
| **Auditoria** | "Conforme CONTRATO DE AUDITORIA" | `contracts/auditoria/conformidade.md` | Auditoria de conformidade de RF |
| **Deploy Azure** | "Conforme CONTRATO DE DEPLOY – AZURE" | `contracts/deploy/azure.md` | Deploy para HOM/PRD no Azure |
| **Testes** | "Conforme CONTRATO DE TESTES" | `contracts/testes/execucao.md` | Executar testes unitários, E2E |

#### 7.2.3. Regras de Ativação de Contratos

Conforme **CLAUDE.md seção 7**:

1. Um contrato **só é aplicado** se for **explicitamente citado** no prompt
2. Contratos **não se misturam** (um por execução)
3. Se houver conflito entre contratos, o **mais restritivo** prevalece
4. Contratos em `deprecated/` **NUNCA** devem ser usados

**Exemplo de Ativação:**
```
Prompt: "Conforme CONTRATO DE EXECUÇÃO – BACKEND, implementar RF028 (SLA Operações)"
```
Isso ativa:
- `contracts/desenvolvimento/execucao/backend-criacao.md`
- Todas as regras de COMPLIANCE.md
- Todas as regras de ARCHITECTURE.md
- Validações obrigatórias de RF → UC → TC

---

### 7.3. FERRAMENTAS DE VALIDAÇÃO

#### 7.3.1. Validador de Cobertura RF → UC → TC

**Localização:** `D:\IC2_Governanca\tools\validator-rf-uc.py`

**Descrição:** Valida presença e conformidade de User Stories e Casos de Teste para cada RF.

**Uso:**
```bash
# Validar RF específico
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028

# Validar EPIC completo
python D:\IC2_Governanca\tools\validator-rf-uc.py --epic EPIC008-SVC

# Validar todos os processos (38 RFs)
python D:\IC2_Governanca\tools\validator-rf-uc.py --all-processes

# Modo detalhado (verbose)
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028 --verbose
```

**Exit Codes:**
- `0`: Validação aprovada
- `1`: RF sem UC (User Stories)
- `2`: RF sem TC (Casos de Teste)
- `3`: RF sem MD (Modelo de Dados)
- `4`: Cobertura de testes insuficiente

**Validações Realizadas:**
- Presença de `UC-RFXXX.md`
- Presença de `TC-RFXXX.yaml`
- Presença de `MD-RFXXX.yaml`
- Estrutura YAML válida em TC
- Cobertura mínima de 100% dos casos de uso

---

#### 7.3.2. Sincronizador Azure DevOps

**Localização:** `D:\IC2_Governanca\tools\devops-sync/`

**Arquivos:**
- `sync-rf.py` - Sincronizador individual de RF
- `sync-all.py` - Sincronizador em massa
- `config.yaml` - Configuração de conexão Azure DevOps

**Descrição:** Sincroniza STATUS.yaml com Azure DevOps Boards (Work Items).

**Uso:**
```bash
# Sincronizar RF específico
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028

# Sincronizar todos os RFs de um EPIC
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py --epic EPIC008-SVC

# Sincronizar todos os 38 processos
python D:\IC2_Governanca\tools\devops-sync/sync-all.py --all-processes

# Dry-run (sem efetivar mudanças)
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028 --dry-run
```

**Operações Executadas:**
- Lê STATUS.yaml do RF
- Atualiza Work Item no Azure DevOps
- Sincroniza status (Pendente → In Progress → Completed)
- Atualiza campos customizados (UC, TC, MD)
- Gera relatório de sincronização

**Configuração:**
Editar `config.yaml` com credenciais Azure DevOps:
```yaml
azure_devops:
  organization: "icontrolit"
  project: "IC2"
  pat_token: "${AZURE_DEVOPS_PAT}"  # Variável de ambiente
  board_area_path: "IC2\\Governanca"
```

---

#### 7.3.3. Gerador de Relatórios

**Localização:** `D:\IC2_Governanca\tools\reports/`

**Scripts:**
- `generate-process-report.py` - Relatório de processo individual
- `generate-journey-report.py` - Relatório de jornada (6 processos)
- `generate-epic-report.py` - Relatório de EPIC completo
- `generate-dashboard.py` - Dashboard consolidado (HTML)

**Uso:**
```bash
# Relatório de processo (Markdown)
python D:\IC2_Governanca\tools\reports/generate-process-report.py PRO-SVC-001

# Relatório de jornada (6 documentos em PDF)
python D:\IC2_Governanca\tools\reports/generate-journey-report.py service-desk

# Dashboard consolidado (HTML interativo)
python D:\IC2_Governanca\tools\reports/generate-dashboard.py --output dashboard.html
```

**Relatórios Gerados:**
- Métricas de cobertura RF → UC → TC
- Status de implementação (Backend/Frontend)
- Status de testes (Unit/E2E)
- Dependências entre processos
- Timeline de entregas

---

### 7.4. SKILLS DO CLAUDE CODE

#### 7.4.1. Skills Disponíveis

Conforme `D:\IC2_Governanca\governanca\skills\README.md`:

| Skill | Comando | Descrição |
|-------|---------|-----------|
| **start-rf** | `/start-rf RF028` | Iniciar trabalho em um RF (cria branch, valida estrutura) |
| **validate-rf** | `/validate-rf RF028` | Validar build, testes e documentação completos |
| **deploy-rf** | `/deploy-rf RF028 --env HOM` | Deploy para HOM ou PRD |
| **audit-rf** | `/audit-rf RF028` | Auditoria de conformidade (COMPLIANCE.md) |
| **fix-build** | `/fix-build` | Corrigir erros de compilação automaticamente |
| **sync-devops** | `/sync-devops RF028` | Sincronizar STATUS.yaml com Azure DevOps |
| **sync-todos** | `/sync-todos` | Sincronizar Lista de Tarefas (project) |
| **executar-msg** | `/executar-msg` | Executa script Python msg.py |

#### 7.4.2. Uso de Skills

**Exemplo 1: Iniciar trabalho em RF028**
```
/start-rf RF028
```
Executa:
1. Cria branch `feature/RF028-backend`
2. Valida presença de UC-RF028.md, TC-RF028.yaml, MD-RF028.yaml
3. Copia template TODO do contrato
4. Atualiza STATUS.yaml para "In Progress"

**Exemplo 2: Deploy para HOM**
```
/deploy-rf RF028 --env HOM
```
Executa:
1. Valida testes (unit + E2E)
2. Valida build (backend + frontend)
3. Executa deploy via Azure DevOps Pipeline
4. Atualiza STATUS.yaml

**Exemplo 3: Auditoria de conformidade**
```
/audit-rf RF028
```
Executa:
1. Valida separação RF/RL (COMPLIANCE.md seção 1)
2. Valida User Stories (COMPLIANCE.md seção 2)
3. Valida Multi-Tenancy (COMPLIANCE.md seção 6)
4. Valida Execution Manifest (COMPLIANCE.md seção 7)
5. Gera relatório de auditoria

---

### 7.5. COMANDOS DE DESENVOLVIMENTO

Conforme **COMMANDS.md**:

#### 7.5.1. Backend (.NET)

```bash
# Build
dotnet build D:\IC2\backend\IControlIT.sln

# Testes unitários
dotnet test D:\IC2\backend\IControlIT.Tests\IControlIT.Tests.csproj

# Executar API (dev)
dotnet run --project D:\IC2\backend\IControlIT.API\IControlIT.API.csproj

# Migrations
dotnet ef migrations add MigrationName --project IControlIT.Infrastructure
dotnet ef database update --project IControlIT.Infrastructure
```

#### 7.5.2. Frontend (Angular)

```bash
cd D:\IC2\frontend\icontrolit-app

# Instalar dependências
npm install

# Dev server (porta 4200)
npm start

# Build de produção
npm run build --configuration production

# Testes unitários (Jest)
npm run test

# Testes E2E (Playwright)
npm run e2e

# Testes E2E específicos
npm run e2e -- --grep "RF028"
```

#### 7.5.3. Validação e Conformidade

```bash
# Validar RF → UC → TC
python D:\IC2_Governanca\tools\validator-rf-uc.py RF028

# Sincronizar com DevOps
python D:\IC2_Governanca\tools\devops-sync/sync-rf.py RF028

# Gerar relatório de auditoria
python D:\IC2_Governanca\tools\reports/generate-process-report.py PRO-SVC-001
```

---

### 7.6. RECURSOS EXTERNOS

#### 7.6.1. Documentação de Tecnologias

| Tecnologia | Documentação Oficial |
|------------|----------------------|
| **.NET 8** | https://learn.microsoft.com/en-us/dotnet/ |
| **Angular 17** | https://angular.io/docs |
| **PostgreSQL** | https://www.postgresql.org/docs/ |
| **Redis** | https://redis.io/docs/ |
| **Hangfire** | https://docs.hangfire.io/ |
| **SignalR** | https://learn.microsoft.com/en-us/aspnet/core/signalr/ |
| **MediatR** | https://github.com/jbogard/MediatR/wiki |
| **Playwright** | https://playwright.dev/docs/intro |
| **Azure DevOps** | https://learn.microsoft.com/en-us/azure/devops/ |

#### 7.6.2. Padrões e Práticas

| Padrão | Referência |
|--------|-----------|
| **Clean Architecture** | https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html |
| **CQRS** | https://martinfowler.com/bliki/CQRS.html |
| **DDD** | https://martinfowler.com/tags/domain%20driven%20design.html |
| **REST API** | https://restfulapi.net/ |
| **OWASP Top 10** | https://owasp.org/www-project-top-ten/ |
| **OpenAPI** | https://swagger.io/specification/ |

#### 7.6.3. Certificações e Compliance

| Certificação | Documentação |
|--------------|--------------|
| **ISO 27001** | https://www.iso.org/isoiec-27001-information-security.html |
| **SOC 2** | https://www.aicpa.org/soc |
| **LGPD** | https://www.gov.br/lgpd |
| **SOX** | https://www.sec.gov/spotlight/sarbanes-oxley.htm |
| **PCI-DSS** | https://www.pcisecuritystandards.org/ |

---

## 8. ÍNDICE ALFABÉTICO DE PROCESSOS

### 8.1. LISTA COMPLETA (38 PROCESSOS)

| Nome do Processo | Código | RF | Jornada | Seção Referência |
|------------------|--------|----|---------|--------------------|
| **Agendamento de Tarefas** | PRO-INF-005 | RF005 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Agrupamento de Chamados** | PRO-SVC-010 | RF037 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Aprovações e Workflows** | PRO-WKF-009 | RF019 | Workflows | `03-Jornada-Workflows.md` |
| **Auditoria de Faturas** | PRO-FCT-007 | RF027 | Faturamento | `04-Jornada-Faturamento.md` |
| **Auditoria de Operações** | PRO-INF-004 | RF004 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Baixa de Faturas** | PRO-FCT-002 | RF022 | Faturamento | `04-Jornada-Faturamento.md` |
| **Base de Conhecimento** | PRO-WKF-005 | RF015 | Workflows | `03-Jornada-Workflows.md` |
| **Cadastro de Usuários** | PRO-WKF-001 | RF009 | Workflows | `03-Jornada-Workflows.md` |
| **Conciliação Financeira** | PRO-FCT-005 | RF025 | Faturamento | `04-Jornada-Faturamento.md` |
| **Download DANFE** | PRO-FCT-004 | RF024 | Faturamento | `04-Jornada-Faturamento.md` |
| **Emissão de NF-e** | PRO-FCT-003 | RF023 | Faturamento | `04-Jornada-Faturamento.md` |
| **Escalação Automática** | PRO-SVC-006 | RF033 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Gerenciamento de Arquivos** | PRO-INF-002 | RF002 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Gestão de Chamados** | PRO-SVC-003 | RF030 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Gestão de Clientes** | PRO-INF-006 | RF006 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Gestão de Faturas** | PRO-FCT-001 | RF021 | Faturamento | `04-Jornada-Faturamento.md` |
| **Gestão de Permissões** | PRO-WKF-002 | RF010 | Workflows | `03-Jornada-Workflows.md` |
| **Hierarquia Organizacional** | PRO-WKF-003 | RF011 | Workflows | `03-Jornada-Workflows.md` |
| **Histórico Unificado** | PRO-SVC-011 | RF038 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Importação em Massa** | PRO-IMP-001 | RF020 | Workflows | `03-Jornada-Workflows.md` |
| **Integrações Externas** | PRO-INF-008 | RF008 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Inventário Cíclico** | PRO-AUD-001 | RF068 | Auditoria | `06-Jornada-Auditoria.md` |
| **Login e Autenticação** | PRO-INF-007 | RF007 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Logs de Sistema** | PRO-INF-003 | RF003 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Medição/Faturamento** | PRO-FCT-006 | RF026 | Faturamento | `04-Jornada-Faturamento.md` |
| **Notificações** | PRO-WKF-004 | RF014 | Workflows | `03-Jornada-Workflows.md` |
| **Ordens de Serviço** | PRO-SVC-004 | RF031 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Parâmetros e Configurações** | PRO-INF-001 | RF001 | Infraestrutura | `01-Jornada-Infraestrutura.md` |
| **Pesquisas de Satisfação** | PRO-WKF-008 | RF018 | Workflows | `03-Jornada-Workflows.md` |
| **Pesquisas Satisfação SD** | PRO-SVC-009 | RF036 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Priorização Automática** | PRO-SVC-007 | RF034 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Reaberturas** | PRO-SVC-008 | RF035 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Relatórios e Dashboards** | PRO-WKF-007 | RF017 | Workflows | `03-Jornada-Workflows.md` |
| **SLA Operações** | PRO-SVC-001 | RF028 | Service Desk | `05-Jornada-Service-Desk.md` |
| **SLA Serviços** | PRO-SVC-002 | RF029 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Solicitações** | PRO-SVC-005 | RF032 | Service Desk | `05-Jornada-Service-Desk.md` |
| **Templates Documentos** | PRO-WKF-006 | RF016 | Workflows | `03-Jornada-Workflows.md` |

---

### 8.2. ÍNDICE POR JORNADA

#### Jornada 1: Infraestrutura (8 processos)
- PRO-INF-001 (Parâmetros e Configurações)
- PRO-INF-002 (Gerenciamento de Arquivos)
- PRO-INF-003 (Logs de Sistema)
- PRO-INF-004 (Auditoria de Operações)
- PRO-INF-005 (Agendamento de Tarefas)
- PRO-INF-006 (Gestão de Clientes)
- PRO-INF-007 (Login e Autenticação)
- PRO-INF-008 (Integrações Externas)

#### Jornada 2: Workflows e Automações (9 processos)
- PRO-WKF-001 (Cadastro de Usuários)
- PRO-WKF-002 (Gestão de Permissões)
- PRO-WKF-003 (Hierarquia Organizacional)
- PRO-WKF-004 (Notificações)
- PRO-WKF-005 (Base de Conhecimento)
- PRO-WKF-006 (Templates Documentos)
- PRO-WKF-007 (Relatórios e Dashboards)
- PRO-WKF-008 (Pesquisas de Satisfação)
- PRO-WKF-009 (Aprovações e Workflows)

#### Jornada 3: Importação (1 processo)
- PRO-IMP-001 (Importação em Massa)

#### Jornada 4: Faturamento (7 processos)
- PRO-FCT-001 (Gestão de Faturas)
- PRO-FCT-002 (Baixa de Faturas)
- PRO-FCT-003 (Emissão de NF-e)
- PRO-FCT-004 (Download DANFE)
- PRO-FCT-005 (Conciliação Financeira)
- PRO-FCT-006 (Medição/Faturamento)
- PRO-FCT-007 (Auditoria de Faturas)

#### Jornada 5: Service Desk (11 processos)
- PRO-SVC-001 (SLA Operações)
- PRO-SVC-002 (SLA Serviços)
- PRO-SVC-003 (Gestão de Chamados)
- PRO-SVC-004 (Ordens de Serviço)
- PRO-SVC-005 (Solicitações)
- PRO-SVC-006 (Escalação Automática)
- PRO-SVC-007 (Priorização Automática)
- PRO-SVC-008 (Reaberturas)
- PRO-SVC-009 (Pesquisas Satisfação SD)
- PRO-SVC-010 (Agrupamento de Chamados)
- PRO-SVC-011 (Histórico Unificado)

#### Jornada 6: Auditoria (1 processo)
- PRO-AUD-001 (Inventário Cíclico)

---

## 9. CHANGELOG CONSOLIDADO

### Versão 2.0 - Documentação Completa de Processos (2026-01-12)

**Autor:** ALC (alc.dev.br)

#### Documentos Criados

1. **00-Visao-Macro.md** - Visão consolidada de 38 processos em 6 jornadas
2. **01-Jornada-Infraestrutura.md** - 8 processos fundamentais (PRO-INF-001 a PRO-INF-008)
3. **02-Jornada-Workflows.md** - 9 processos de workflows e automações (PRO-WKF-001 a PRO-WKF-009)
4. **03-Jornada-Importacao.md** - 1 processo de importação em massa (PRO-IMP-001)
5. **04-Jornada-Faturamento.md** - 7 processos de gestão financeira (PRO-FCT-001 a PRO-FCT-007)
6. **05-Jornada-Service-Desk.md** - 11 processos de suporte (PRO-SVC-001 a PRO-SVC-011)
7. **06-Jornada-Auditoria.md** - 1 processo de inventário cíclico (PRO-AUD-001)
8. **08-Anexos.md** - Este documento (glossário, referências, recursos)

#### Estatísticas

- **Total de processos documentados:** 38
- **Total de RFs cobertos:** 38 RFs únicos
- **Total de páginas geradas:** ~350 páginas (estimativa)
- **Total de termos no glossário:** 150+ termos técnicos
- **RFs excluídos (cadastros simples):** 72 RFs
- **Cobertura de documentação:** 34,5% dos 110 RFs (cobertura intencional focada em processos complexos)

#### Melhorias Implementadas

1. **Modularização:** Divisão em 6 jornadas temáticas para navegação eficiente
2. **Glossário Completo:** 150+ termos técnicos categorizados em 12 áreas
3. **Mapa de Dependências:** Árvore visual de dependências entre processos
4. **Referências Cruzadas:** Links para RFs, contratos, ferramentas
5. **Recursos Adicionais:** Documentação de governança, skills, comandos
6. **Índice Alfabético:** Busca rápida de processos
7. **Justificativa de Exclusões:** Explicação clara dos 72 RFs não documentados

#### Próximos Passos (Backlog)

- [ ] Criar diagramas de fluxo (Mermaid) para processos críticos
- [ ] Gerar versões PDF de todas as jornadas
- [ ] Criar dashboard HTML interativo com métricas
- [ ] Documentar processos de Contratos (PRO-CTR-001, PRO-CTR-002)
- [ ] Criar vídeos tutoriais de skills do Claude Code
- [ ] Implementar geração automatizada de relatórios

---

### Versão 1.0 - Versão Inicial (2025-12-XX)

**Status:** DEPRECIADA

**Descrição:** Versão inicial contendo apenas 3 processos documentados (PRO-INF-001, PRO-INF-002, PRO-INF-003).

**Motivo de Depreciação:** Escopo insuficiente, estrutura não modular, ausência de glossário e referências cruzadas.

---

## 10. CONTATOS E SUPORTE

### 10.1. EQUIPE DO PROJETO

#### Time de Arquitetura
- **Email:** arquitetura@icontrolit.com.br
- **Responsabilidades:**
  - Governança de ARCHITECTURE.md, CONVENTIONS.md, DECISIONS.md
  - Aprovação de ADRs (Architecture Decision Records)
  - Revisão de contratos de execução
  - Definição de padrões arquiteturais

#### Time de Compliance
- **Email:** compliance@icontrolit.com.br
- **Responsabilidades:**
  - Governança de COMPLIANCE.md
  - Auditoria de conformidade (ISO 27001, SOC 2, LGPD, SOX)
  - Validação de certificações
  - Revisão de logs e auditoria

#### Suporte Técnico
- **Email:** suporte@icontrolit.com.br
- **Responsabilidades:**
  - Suporte a desenvolvedores
  - Troubleshooting de builds e testes
  - Configuração de ambientes de desenvolvimento
  - Suporte a ferramentas de validação

#### DevOps
- **Email:** devops@icontrolit.com.br
- **Responsabilidades:**
  - Pipelines CI/CD (Azure DevOps)
  - Infraestrutura Azure (App Service, Blob Storage, Key Vault)
  - Monitoramento e observabilidade
  - Gestão de ambientes (DEV, HOM, PRD)

---

### 10.2. AUTOR DA DOCUMENTAÇÃO

#### ALC (alc.dev.br)
- **Website:** https://alc.dev.br
- **Especialização:** Arquitetura de Software, Clean Architecture, DDD, CQRS
- **Contribuições:**
  - Criação de CLAUDE.md, COMPLIANCE.md, ARCHITECTURE.md, CONVENTIONS.md
  - Estruturação de contratos de execução
  - Documentação de 38 processos em 6 jornadas modulares
  - Criação de ferramentas de validação (validator-rf-uc.py, devops-sync/)

---

### 10.3. CANAIS DE COMUNICAÇÃO

#### Documentação e Governança
- **Repositório:** `D:\IC2_Governanca\`
- **Issues:** Azure DevOps - Board "Governança"
- **Wiki:** Confluence IControlIT
- **Versionamento:** Git (branch `main` protegida)

#### Suporte Técnico
- **Tickets:** Azure DevOps - Board "Suporte"
- **Chat:** Microsoft Teams - Canal "Suporte Desenvolvimento"
- **FAQ:** Confluence - "Perguntas Frequentes"

#### Comunidade Interna
- **Fórum:** Yammer - Grupo "Desenvolvedores IControlIT"
- **Mensageria:** Microsoft Teams - Canal "Geral"
- **Reuniões:** Daily Standup (09:00), Weekly Review (Sex 16:00)

---

### 10.4. SUPORTE A FERRAMENTAS

#### Claude Code (claude.ai/code)
- **Documentação:** https://docs.anthropic.com/claude/docs
- **Suporte:** support@anthropic.com
- **Versão Atual:** Sonnet 4.5 (claude-sonnet-4-5-20250929)

#### Azure DevOps
- **Documentação:** https://learn.microsoft.com/en-us/azure/devops/
- **Suporte:** Contrato Enterprise Microsoft
- **Organization:** icontrolit.visualstudio.com

#### Ferramentas de Validação
- **Suporte Interno:** suporte@icontrolit.com.br
- **Issues:** Azure DevOps - Label "Ferramentas"
- **Código Fonte:** `D:\IC2_Governanca\tools/`

---

### 10.5. HORÁRIO DE ATENDIMENTO

| Canal | Horário | Tempo de Resposta |
|-------|---------|-------------------|
| **Email (Suporte Técnico)** | Seg-Sex 08:00-18:00 | 4 horas |
| **Email (Arquitetura)** | Seg-Sex 09:00-18:00 | 24 horas |
| **Teams (Chat)** | Seg-Sex 08:00-19:00 | 1 hora |
| **Tickets (Azure DevOps)** | Seg-Sex 08:00-18:00 | 8 horas |
| **Emergências (On-Call)** | 24/7 | 30 minutos |

---

### 10.6. ESCALAÇÃO DE SUPORTE

#### Nível 1: Suporte Técnico
- **Escopo:** Dúvidas sobre ferramentas, comandos, configuração de ambiente
- **Contato:** suporte@icontrolit.com.br

#### Nível 2: Time de Desenvolvimento
- **Escopo:** Bugs em código, problemas de build, testes falhando
- **Contato:** dev@icontrolit.com.br

#### Nível 3: Arquitetura
- **Escopo:** Decisões arquiteturais, padrões, governança
- **Contato:** arquitetura@icontrolit.com.br

#### Nível 4: Direção Técnica
- **Escopo:** Questões estratégicas, conflitos de governança, mudanças estruturais
- **Contato:** cto@icontrolit.com.br

---

### 10.7. FEEDBACK E CONTRIBUIÇÕES

Sugestões de melhoria para esta documentação são bem-vindas.

**Processo de Contribuição:**
1. Abrir ticket no Azure DevOps - Board "Governança"
2. Preencher template "Sugestão de Melhoria Documentação"
3. Aguardar revisão do Time de Arquitetura (SLA: 3 dias úteis)
4. Se aprovado, criar PR com alterações propostas
5. Revisão técnica + merge

**Template de Sugestão:**
```markdown
## Tipo de Sugestão
[ ] Correção de erro
[ ] Melhoria de clareza
[ ] Adição de conteúdo
[ ] Reorganização estrutural

## Documento Afetado
[Ex: 08-Anexos.md, seção 1.4]

## Descrição da Sugestão
[Detalhar proposta]

## Justificativa
[Por que esta mudança é necessária?]

## Impacto
[ ] Baixo (correção pontual)
[ ] Médio (seção específica)
[ ] Alto (múltiplos documentos)
```

---

## FIM DO DOCUMENTO

**Documento:** 08-Anexos.md
**Versão:** 2.0
**Data de Criação:** 2026-01-12
**Autor:** ALC (alc.dev.br)
**Status:** Vigente
**Próxima Revisão:** 2026-07-12 (semestral)

---

**NOTA FINAL:**

Este documento consolida **TODOS** os recursos de suporte para os 38 processos documentados nas 6 jornadas. Ele deve ser mantido atualizado conforme:

1. Novos termos técnicos são introduzidos no sistema
2. Novos RFs são implementados e documentados
3. Novos contratos de execução são criados
4. Novas ferramentas de validação são desenvolvidas
5. Mudanças na estrutura de governança ocorrem

**Responsabilidade pela Atualização:** Time de Arquitetura + ALC (alc.dev.br)

**Periodicidade de Revisão:** Semestral (Janeiro e Julho)

**Histórico de Versões:**
- **v2.0 (2026-01-12):** Criação completa com 150+ termos, 38 processos, 72 RFs excluídos justificados
- **v1.0 (DEPRECIADA):** Versão inicial incompleta

---

**Mantido por:** ALC (alc.dev.br) + Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-12
**Licença:** Proprietário IControlIT - Uso Interno Exclusivo

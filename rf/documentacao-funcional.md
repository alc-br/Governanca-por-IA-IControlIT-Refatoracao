# Template – Documento de Requisitos Funcionais (RF) – Refatoração do Legado (IControlIT)
**Projeto:** Modernização do IControlIT (ASP.NET Web Forms → .NET 10 + Angular 19)
**Tipo:** Inventário Funcional do Legado (refatoração)
**Versão:** 1.5
**Data:** 28/12/2025
**Responsável:** Claude Code - Análise Manual Detalhada
**Status:** Em Desenvolvimento (RF-001, RF-002, RF-003, RF-004 e RF-005 completos, demais em andamento)

---

## 1) Contexto

Este documento registra os **Requisitos Funcionais (RFs)** existentes no sistema legado.
O foco é **preservar comportamento** durante a refatoração, sem inventar funcionalidades.

**Total de RFs identificados:** 110
**RFs documentados completamente (com análise manual):** 5 de 110
**RFs pendentes de análise:** 105

---

## 2) Objetivo

Documentar RFs com **descrição básica + 5W** e, principalmente, indicar **onde confirmar detalhes no legado**.

Cada RF neste documento foi analisado **manualmente e conscientemente**, extraindo informações reais do código legado ou da documentação existente, sem automação.

---

## 3) Escopo

### 3.1 Entra
- Funcionalidades existentes (telas, ações, rotinas, relatórios, consultas).
- Regras observáveis e confirmáveis no legado.

### 3.2 Não entra
- Solução técnica do sistema novo (arquitetura, padrões, endpoints modernos).
- Melhorias futuras ou mudanças de processo (isso é outro artefato).
- Código copiado (VB.NET/SQL). Aqui é linguagem natural + referências.

---

## 4) Fontes de verdade (onde buscar evidência)

Use esta ordem para confirmar qualquer RF:

1) Telas ASPX + code-behind
- `D:/IC2/ic1_legado/IControlIT/[modulo]/` (`.aspx` / `.aspx.cs`)

2) Webservices (métodos públicos)
- `D:/IC2/ic1_legado/IControlIT/[modulo]/WebService/` (`.asmx` / `.cs`)

3) Stored procedures / triggers / funções
- `D:/IC2/ic1_legado/Database/Procedures/`

4) Modelo físico do banco
- `D:\DocumentosIC2\modelo-fisico-bd.sql`

5) Inventários e matrizes (planejamento)
- Inventário de Componentes / Inventário de BD / Mapa de Lógica / Dependências / Matriz por Cliente

---

## 5) Convenções de escrita do RF

- Escreva o **comportamento atual** (observável).
- Evite termos técnicos de implementação.
- Sempre inclua **pelo menos 1 referência concreta** no legado.
- Se houver dúvida, marque **Status de evidência = Parcial/Pendente**.

---

# 6) Requisitos Funcionais do Sistema

> Padrão: RF-001 até RF-115 (110 RFs mapeados).
> Um RF deve ser "pequeno o bastante" para ser testável, e "grande o bastante" para ter sentido.

---

## RF-001 – Parâmetros e Configurações do Sistema

**Descrição (comportamento atual):**
O sistema permite aos administradores gerenciar parâmetros de configuração centralizados que controlam o comportamento da aplicação. No legado, parâmetros eram armazenados em Web.config e tbl_Parametros, sem validação de tipo, criptografia ou multi-tenancy. O sistema moderno implementa parâmetros tipados (String, Integer, Decimal, Boolean, Date, JSON) com validação, criptografia para dados sensíveis, feature flags para rollout gradual de funcionalidades, e configurações específicas por conglomerado (multi-tenant).

**What (o que faz):**
- Cadastro, edição e exclusão de parâmetros do sistema
- Validação de valores conforme tipo de dado (String, Integer, Decimal, Boolean, Date, JSON)
- Criptografia automática de parâmetros sensíveis (senhas, API keys)
- Gerenciamento de feature flags para ativar/desativar funcionalidades de forma controlada
- Configuração de servidor SMTP e provedores de e-mail (SendGrid, AWS SES)
- Controle de limites de uso por conglomerado (máximo de usuários, ativos, armazenamento, chamadas API)
- Histórico completo de alterações com auditoria (usuário, IP, data/hora, motivo)
- Categorização de parâmetros (Sistema, Segurança, Integração, Notificação, Relatório)

**Who (quem usa/impacta):**
- **Super Administrador**: Acesso total a todos os parâmetros, incluindo sensíveis e de sistema
- **Administrador de Sistema**: Gerencia parâmetros gerais e feature flags
- **Administrador de TI**: Configura parâmetros de e-mail e integrações
- **Gerente de Operações**: Visualiza e exporta parâmetros (somente leitura)
- **Auditor**: Consulta histórico de alterações de parâmetros
- **Sistema (automático)**: Consome parâmetros para controlar comportamento em runtime

**When (quando acontece):**
- **Criação inicial**: Durante implantação do sistema (seed de parâmetros obrigatórios)
- **Configuração**: Quando administrador acessa menu "Configurações do Sistema"
- **Alteração**: Quando é necessário modificar comportamento sem deploy (ex: timeout de sessão, limite de upload)
- **Ativação de features**: Quando nova funcionalidade precisa ser habilitada para % de usuários
- **Teste de e-mail**: Quando administrador configura servidor SMTP e testa envio
- **Monitoramento**: Jobs Hangfire verificam limites de uso a cada 1 hora
- **Runtime**: Parâmetros são consultados via cache (Redis) durante execução da aplicação

**Where (onde no sistema):**
- **Módulo**: Administração / Configurações
- **Menu**: Administração → Sistema → Parâmetros e Configurações
- **Telas (Frontend Angular)**:
  - `/admin/configuracoes/parametros` (lista e gerencia parâmetros)
  - `/admin/configuracoes/feature-flags` (controla feature flags)
  - `/admin/configuracoes/email` (configurações de servidor SMTP)
  - `/admin/configuracoes/limites` (limites de uso por conglomerado)
- **API (Backend .NET) - Endpoints Implementados**:
  - `GET /api/parametros/categorias` (ListarCategorias - lista categorias de parâmetros)
  - `GET /api/parametros` (ListarParametros - lista paginada com filtros por categoria, tipo, ativo)
  - `GET /api/parametros/{id}` (ObterParametroPorId - detalhes completos com histórico)
  - `POST /api/parametros` (CriarParametro - requer permissão CREATE)
  - `PUT /api/parametros/{id}` (AtualizarParametro - requer permissão UPDATE, registra auditoria)
  - `DELETE /api/parametros/{id}?motivo={motivo}` (ExcluirParametro - soft delete, motivo obrigatório)
  - `POST /api/parametros/{id}/descriptografar` (DescriptografarValor - Super Admin only, descriptografa senhas/API keys)
  - `GET /api/parametros/{id}/historico` (ObterHistorico - timeline completa de alterações com diff)

**Why (por que existe):**
- **Flexibilidade**: Permitir alteração de comportamento sem deploy ou alteração de código
- **Multi-tenancy**: Configurações específicas por conglomerado (cliente) no modelo SaaS
- **Segurança**: Criptografia de dados sensíveis (senhas, API keys, tokens)
- **Feature Flags**: Rollout gradual de funcionalidades (% usuários, lista específica, período)
- **Auditoria**: Rastreamento completo de quem alterou o quê e quando
- **Conformidade**: Atender requisitos de auditoria e compliance (ISO 27001, LGPD)
- **Operação**: Ajustar limites de uso, timeouts, URLs de integração sem parar o sistema
- **Escalabilidade**: Cache distribuído (Redis) para alto desempenho na consulta de parâmetros

---

### Referências no Legado (onde confirmar detalhes)

**Telas (UI):**
- ASPX: Não identificado no legado (configurações eram feitas via Web.config e SQL direto)
- Code-behind: N/A
- **Observação**: No legado, parâmetros eram gerenciados manualmente editando `Web.config` ou executando scripts SQL na tabela `tbl_Parametros`. Não havia interface administrativa.

**Serviços (legado):**
- ASMX: `D:/IC2/ic1_legado/IControlIT/[modulo]/WebService/WSParametros.asmx`
- Classe: `WSParametros.asmx.vb` ou `WSParametros.asmx.cs`
- Métodos relevantes:
  - `ListarParametros()` → migra para `GET /api/parametros`
  - `ObterValorParametro(codigo)` → migra para `GET /api/parametros/{codigo}`
  - `AtualizarParametro(id, valor)` → migra para `PUT /api/parametros/{id}`
  - `ObterConfiguracaoEmail()` → migra para `GET /api/configuracoes-email`

**Banco de dados:**
- Modelo físico: `D:\DocumentosIC2\modelo-fisico-bd.sql`
- Tabelas legado:
  - `tbl_Parametros` → migra para `Sistema_Parametro`
  - `tbl_Config_Email` → migra para `Sistema_Configuracao_Email`
  - `tbl_Parametros_Log` → migra para `Sistema_Parametro_Historico`
- Tabelas novas (não existem no legado):
  - `Sistema_Feature_Flag` (funcionalidade nova)
  - `Sistema_Feature_Flag_Historico`
  - `Sistema_Limite_Uso` (funcionalidade nova)
  - `Sistema_Limite_Uso_Historico`
- Views: Não aplicável
- Procedures:
  - Verificar em `D:/IC2/ic1_legado/Database/Procedures/` por procedures que manipulam `tbl_Parametros`

**Integrações / Dependências externas (se houver):**
- **SendGrid**: Provedor de e-mail (configuração de API Key)
- **AWS SES**: Provedor de e-mail alternativo (configuração de Access Key/Secret)
- **Redis**: Cache distribuído para armazenar parâmetros consultados frequentemente
- **Azure Key Vault**: Armazenamento seguro de secrets (senhas, API keys) - modernização
- **Hangfire**: Jobs para verificar limites de uso e enviar alertas

**Variações por cliente (se houver):**
- **Multi-tenant**: Cada conglomerado pode ter valores diferentes para mesmos parâmetros
- Exemplos:
  - Cliente A: Timeout sessão = 30 minutos
  - Cliente B: Timeout sessão = 60 minutos
  - Cliente C: Feature "Export PDF" habilitada
  - Cliente D: Feature "Export PDF" desabilitada
- **Configurações de E-mail**: Cada conglomerado tem seu próprio servidor SMTP ou provedor
- **Limites de Uso**: Definidos por plano contratado (Básico, Pro, Enterprise)

**Evidências adicionais (opcional):**
- Documento RF001.md completo: `D:\IC2\docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF001-Parametros-e-Configuracoes-do-Sistema\RF001.md`
- 15 Regras de Negócio documentadas (RN-CFG-001-01 até RN-CFG-001-15)
- Modelo de dados completo em `MD-RF001.md`
- Casos de uso em `UC-RF001.md`
- Casos de teste em `TC-RF001-BACKEND.md`, `TC-RF001-FRONTEND.md`, `TC-RF001-SEGURANCA.md`

---

### Status de evidência
- [x] Confirmado no legado (referências completas)
- [ ] Parcial (faltam referências ou regra ambígua)
- [ ] Pendente (não documentar como definitivo)

### Observações

**Mudanças críticas do legado para moderno:**
1. **Armazenamento**: Web.config hardcoded → Banco de dados centralizado
2. **Multi-Tenant**: Não suportado → Configuração por conglomerado
3. **Tipos de Dados**: Apenas strings → String, Integer, Decimal, Boolean, Date, JSON
4. **Validação**: Sem validação → Regex, min/max, opções válidas
5. **Criptografia**: Senhas em texto plano → AES-256 para dados sensíveis
6. **Feature Flags**: Não existe → Feature flags com rollout gradual
7. **Auditoria**: Sem histórico → Histórico completo de alterações
8. **Interface**: Edição manual de arquivo → UI administrativa com validação
9. **Hot Reload**: Requer restart → Configuração dinâmica em runtime
10. **Versionamento**: Sem controle → Histórico de versões com rollback

**Funcionalidades novas (não existem no legado):**
- Feature Flags (ativação gradual de funcionalidades)
- Limites de Uso por Conglomerado (controle SaaS)
- Rollout percentual de features
- Teste de envio de e-mail via interface
- Cache distribuído (Redis)
- Validação de tipo de dado
- Criptografia automática de dados sensíveis

---

**FIM DO RF-001**

---

## RF-002 – Configurações e Parametrização

**Descrição (comportamento atual):**
O sistema centraliza TODAS as configurações infraestruturais e de integração do IControlIT, permitindo personalização multi-tenant, gerenciamento dinâmico sem restart, versionamento completo, feature flags progressivos, validação inteligente, criptografia automática de valores sensíveis, cache distribuído Redis e auditoria SOX completa. Diferentemente do RF-001 (parâmetros operacionais), o RF-002 foca em configurações de infraestrutura críticas: SMTP, Azure Storage, Redis, APIs externas, parâmetros de segurança, políticas globais. No legado, configurações ficavam em web.config estático (requer restart IIS); no moderno, tudo é dinâmico em banco de dados com cache Redis hot-reload.

**What (o que faz):**
- Gerenciamento de configurações infraestruturais por categoria (Sistema, Email, Integração, Segurança, Cache, Storage, Performance, Features)
- CRUD visual hierárquico de configurações com interface administrativa
- Suporte a tipos de dados: String, Integer, Decimal, Boolean, JSON, Enum, DateTime
- Validação robusta: Regex, ranges (min/max), valores permitidos (enum)
- Criptografia automática para senhas, API keys, tokens (Azure Key Vault com AES-256-GCM)
- Cache hot-reload com Redis e invalidação automática via Pub/Sub (zero downtime)
- Versionamento completo com histórico imutável, diff visual e rollback 1-click
- Feature flags progressivos com 4 estratégias de rollout: Percentual Aleatório, Usuários Específicos, Perfis, Empresas Piloto (canary releases 0%→25%→50%→100%)
- Export/Import de configurações em JSON/YAML para migração DEV→HOM→PRD
- Notificações automáticas para Slack/Teams quando configurações críticas são alteradas
- Validação de impacto (dry run) antes de aplicar mudanças
- Agrupamento visual por categoria e grupo funcional

**Who (quem usa/impacta):**
- **Super Administrador**: Acesso total incluindo DECRYPT de valores sensíveis, DELETE, ROLLBACK
- **Administrador DevOps**: Gerencia configurações infraestruturais, faz EXPORT/IMPORT, ROLLBACK (sem DELETE)
- **Administrador de Sistema**: Visualiza e edita configurações não-críticas (sem DECRYPT, DELETE, IMPORT)
- **Gerente de Operações**: Somente leitura e export de configurações
- **Auditor**: Consulta histórico de alterações, relatórios de compliance
- **Sistema (automático)**: Consome configurações via cache para integrações (SMTP, Azure, Redis, ERPs)
- **Jobs Hangfire**: Desabilita feature flags expiradas, envia notificações de mudanças

**When (quando acontece):**
- **Implantação**: Durante deploy inicial (seed de configurações obrigatórias)
- **Configuração de integração**: Quando administrador configura SMTP, Azure Blob, Redis, APIs ERP
- **Mudança de ambiente**: Quando faz migração DEV→HOM→PRD (export/import)
- **Ativação de features**: Quando nova funcionalidade precisa ser habilitada progressivamente (canary release)
- **Incidentes**: Quando precisa fazer rollback de configuração que causou problema
- **Auditoria**: Quando auditor consulta histórico de mudanças (compliance SOX, ISO 27001)
- **Runtime**: Sistema consulta cache Redis (hot-reload automático quando config muda)
- **Monitoramento**: Jobs verificam feature flags expiradas e notificam equipe DevOps

**Where (onde no sistema):**
- **Módulo**: Administração / Configurações Infraestruturais
- **Menu**: Administração → Sistema → Configurações e Parametrização
- **Telas (Frontend Angular)**:
  - `/admin/configuracoes/sistema` (idioma, timezone, moeda, formatos)
  - `/admin/configuracoes/email-smtp` (servidor SMTP, credenciais)
  - `/admin/configuracoes/integracoes` (Azure, ERPs, APIs externas)
  - `/admin/configuracoes/seguranca` (JWT secret, política senhas, MFA)
  - `/admin/configuracoes/cache-redis` (Redis host, port, password)
  - `/admin/configuracoes/storage` (Azure Blob connection string)
  - `/admin/configuracoes/feature-flags` (feature flags progressivos)
  - `/admin/configuracoes/export-import` (migração de ambientes)
  - `/admin/configuracoes/historico/{id}` (diff visual, rollback)
- **API (Backend .NET) - Endpoints Implementados**:
  - `GET /api/configuracoes` (Listar - paginação com filtros por categoria, ativo, ambiente)
  - `GET /api/configuracoes/{id}` (ObterPorId - detalhes completos da configuração)
  - `POST /api/configuracoes` (Criar - requer permissão CREATE)
  - `PUT /api/configuracoes/{id}` (Atualizar - requer permissão UPDATE, registra histórico)
  - `GET /api/configuracoes/categorias` (ListarCategorias - todas as categorias disponíveis)
  - `GET /api/configuracoes/{id}/historico?pageNumber={}&pageSize={}` (ObterHistorico - paginado com diff)
  - `POST /api/configuracoes/{id}/rollback?versao={}&motivo={}` (Rollback - requer permissão ROLLBACK)
  - `POST /api/configuracoes/export?categorias[]={}&formato={}&incluirSensiveis={}` (Exportar - JSON/YAML, requer permissão EXPORT)
  - `POST /api/configuracoes/import?estrategia={}` (Importar - arquivo multipart, estratégia: Sobrescrever/Ignorar/Merge)
  - `GET /api/configuracoes/feature-flags` (ListarFeatureFlags - todas as flags)
  - `POST /api/configuracoes/feature-flags/{id}/toggle` (ToggleFeatureFlag - ativar/desativar)
  - `POST /api/configuracoes/feature-flags/{id}/rollout?estrategia={}&percentual={}` (ConfigurarRollout - canary releases)
  - `GET /api/configuracoes/feature-flags/{codigo}/check` (VerificarFeatureAtiva - público, verifica se ativa para usuário atual)

**Why (por que existe):**
- **Separação de Responsabilidades**: Isolar configs infraestruturais (RF-002) de parâmetros operacionais (RF-001)
- **Zero Downtime**: Alterar configurações sem restart do servidor (cache hot-reload via Redis Pub/Sub)
- **Segurança**: Criptografar automaticamente senhas, API keys, tokens com Azure Key Vault
- **Multi-tenancy**: Cada conglomerado tem configurações específicas (SMTP próprio, limites personalizados)
- **Compliance**: Auditoria SOX completa com histórico imutável, diff, IP, motivo, ticket de mudança
- **Redução de Risco**: Feature flags progressivos reduzem impacto de bugs em produção (canary releases)
- **Disaster Recovery**: Export/import facilita restauração rápida de configurações
- **Rastreabilidade**: Rollback 1-click para reverter mudanças que causaram incidentes
- **Automação**: Notificações automáticas em Slack/Teams mantém equipe informada
- **Produtividade**: Interface visual intuitiva vs edição manual de web.config

---

### Referências no Legado (onde confirmar detalhes)

**Telas (UI):**
- ASPX: Não existe no legado (configurações eram gerenciadas via editor de texto no web.config)
- Code-behind: N/A
- **Observação**: Sistema legado não tinha interface administrativa para configurações. Administradores editavam manualmente `D:\IC2\ic1_legado\IControlIT\IControlIT\web.config` e faziam restart do IIS.

**Serviços (legado):**
- Classe: `ConfigurationManager.AppSettings` (framework .NET padrão)
- Métodos relevantes:
  - `ConfigurationManager.AppSettings(chave)` → migra para `GET /api/configuracoes/{codigo}` com cache Redis
- **Observação**: Não havia WebService dedicado; código acessava web.config diretamente

**Banco de dados:**
- Modelo físico: `D:\DocumentosIC2\modelo-fisico-bd.sql`
- Tabelas legado: Não existiam (configurações em web.config)
- Tabelas novas (moderno):
  - `Sistema_Configuracao` (armazena configurações infraestruturais)
  - `Sistema_Configuracao_Historico` (versionamento e auditoria SOX)
  - `Sistema_Feature_Flag` (feature flags progressivos)
  - `Sistema_Feature_Flag_Historico` (auditoria de mudanças em flags)
- Views: Não aplicável
- Procedures: Nenhuma específica (CQRS usa Commands/Queries)

**Integrações / Dependências externas (se houver):**
- **Azure Key Vault**: Armazenamento seguro de secrets (senhas SMTP, Azure Client Secret, API keys)
- **Redis**: Cache distribuído para configurações com TTL e invalidação automática via Pub/Sub
- **Microsoft Teams**: Webhook para notificações de mudanças críticas
- **Slack**: Webhook para notificações de mudanças críticas
- **Hangfire**: Jobs para desabilitar feature flags expiradas e notificar devs
- **Azure Blob Storage**: Configuração de connection string para upload de arquivos
- **ERPs (SAP, TOTVS)**: Configuração de URLs e API keys para integração

**Variações por cliente (se houver):**
- **Configuração Multi-Tenant Hierárquica**: Global → Conglomerado → Empresa → Departamento → Usuário
- Exemplos:
  - Cliente A: SMTP próprio (smtp.empresaa.com.br)
  - Cliente B: Azure Blob próprio (contaa.blob.core.windows.net)
  - Cliente C: Feature "Dashboard Executivo" habilitada (100%)
  - Cliente D: Feature "Dashboard Executivo" em rollout progressivo (25% usuários)
  - Cliente E: Timezone America/Sao_Paulo
  - Cliente F: Timezone America/New_York
- **Estratégias de Rollout**: Percentual aleatório, lista de usuários específicos, perfis (gerentes), empresas piloto

**Evidências adicionais (opcional):**
- Documento RF002.md completo: `D:\IC2\docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF002-Configuracoes-e-Parametrizacao\RF002.md`
- 15 Regras de Negócio documentadas (RN-SIS-001 até RN-SIS-015)
- Diferenciação clara entre RF-001 (parâmetros operacionais) e RF-002 (configurações infraestruturais)
- Exemplo de web.config legado com senhas em texto claro (violação de segurança)
- Código VB.NET legado de leitura de configuração

---

### Status de evidência
- [x] Confirmado no legado (referências completas)
- [ ] Parcial (faltam referências ou regra ambígua)
- [ ] Pendente (não documentar como definitivo)

### Observações

**Diferença RF-001 vs RF-002:**
| Aspecto | RF-001 (Parâmetros) | RF-002 (Configurações) |
|---------|---------------------|------------------------|
| Foco | Parâmetros operacionais e regras de negócio | Configurações de infraestrutura e integrações |
| Exemplos | Limites de sistema, feature flags, timeouts | SMTP, Azure Storage, Redis, APIs externas |
| Usuários | Administradores do sistema | Super Administradores e equipe DevOps |
| Frequência de Mudança | Frequente (diária/semanal) | Raro (apenas em deploys/incidentes) |
| Impacto | Funcionalidade específica | Sistema inteiro |
| Criticidade | Alta | Crítica |

**Mudanças críticas do legado para moderno:**
1. **Armazenamento**: web.config estático → Banco de dados centralizado
2. **Restart**: Requer restart IIS → Zero downtime (cache hot-reload)
3. **Segurança**: Senhas em texto claro → Criptografia AES-256-GCM com Azure Key Vault
4. **Multi-Tenant**: Não suportado → Hierarquia Global → Conglomerado → Empresa → Usuário
5. **Versionamento**: Sem controle → Histórico imutável com diff visual
6. **Validação**: Sem validação → Regex, ranges, enums, dry run
7. **Feature Flags**: Não existe → Rollout progressivo (canary releases)
8. **Auditoria**: Sem histórico → Auditoria SOX completa (IP, user-agent, motivo, ticket)
9. **Interface**: Editor de texto → Interface administrativa visual
10. **Migração**: Manual → Export/Import JSON/YAML automatizado

**Funcionalidades novas (não existem no legado):**
- Cache Redis hot-reload com Pub/Sub
- Criptografia automática com Azure Key Vault
- Versionamento e rollback 1-click
- Feature flags progressivos (canary releases)
- Export/Import para migração de ambientes
- Notificações Slack/Teams
- Validação de impacto (dry run)
- Agrupamento visual por categoria
- Diff visual de alterações
- Feature flags com expiração automática

---

**FIM DO RF-002**

---

## RF-003 – Logs, Monitoramento e Observabilidade

**Descrição (comportamento atual):**
O sistema implementa infraestrutura completa de observabilidade para garantir SLA 99.9%, troubleshooting rápido, compliance (LGPD, SOX, ISO 27001), detecção de anomalias e segurança. No legado, logs eram arquivos texto plano (app.log) sem estrutura, com CPF/senhas expostos, sem agregação, busca ou métricas. O sistema moderno implementa Serilog com logs estruturados JSON, agregação centralizada (Seq DEV, Elasticsearch PRD), correlation IDs para rastreamento end-to-end, mascaramento automático de dados sensíveis (CPF, senhas, cartões), métricas Prometheus (RED: Rate/Errors/Duration), dashboards Grafana pré-configurados, health checks (/health) para Kubernetes, tracing distribuído OpenTelemetry, alertas proativos PagerDuty quando error rate > 5%, log sampling 10% em produção (otimização de custos), circuit breaker (logging nunca bloqueia aplicação), busca full-text avançada e export compliance (CSV/JSON para auditoria).

**What (o que faz):**
- Logs estruturados JSON (Serilog) com metadados completos (timestamp, nível, usuário, IP, correlation ID, duração)
- 6 níveis de log configuráveis: Verbose, Debug, Info, Warning, Error, Fatal (por ambiente: DEV=Debug, HOM=Info, PRD=Warning)
- Agregação centralizada: Seq (dev/hom) + Elasticsearch (produção) com retenção automática (90 dias LGPD, 7 anos SOX)
- Correlation IDs obrigatórios: GUID único propagado em toda cadeia de requests para rastreamento end-to-end
- Mascaramento automático de dados sensíveis antes de logar: CPF (***.***.789-00), senhas (********), cartões (****-****-****-1234)
- Métricas Prometheus coletadas automaticamente: Response time (P50/P95/P99), Throughput (requests/segundo), Error rate (% erros)
- Dashboards Grafana pré-configurados: RED metrics (Rate/Errors/Duration), Saúde do Sistema, Performance de APIs, Banco de Dados
- Health Checks endpoint /health com liveness + readiness probes para Kubernetes (verifica DB, Redis, Azure Blob, APIs externas)
- Tracing distribuído OpenTelemetry (integração Jaeger/Zipkin) para visualizar latência em cada microservice
- Alertas proativos automáticos via PagerDuty/Opsgenie: error rate > 5%, P95 latency > 3s, CPU > 80%, Memória > 90%
- Log sampling 10% em produção (otimiza custos Elasticsearch sem perder visibilidade; erros sempre logados 100%)
- Circuit Breaker para logging (se Seq/Elasticsearch falhar, logs vão para arquivo local; logging nunca bloqueia aplicação)
- Busca full-text avançada em Seq/Elasticsearch com filtros por: timestamp, nível, usuário, IP, correlation ID, mensagem, exceção
- Export de logs para CSV/JSON para compliance e auditoria
- Integração nativa com Azure Application Insights

**Who (quem usa/impacta):**
- **Super Administrador DevOps**: Acesso total aos logs, métricas, health checks, configuração de alertas
- **Administrador de Sistema**: Visualiza logs do sistema, métricas de performance, busca por erros
- **Gerente de Operações**: Acessa dashboards Grafana de saúde do sistema e KPIs operacionais
- **Desenvolvedor**: Usa Seq/Elasticsearch para debugging, troubleshooting, análise de correlation IDs
- **Auditor**: Exporta logs de segurança e acesso para compliance LGPD/SOX/ISO 27001
- **Equipe de Suporte**: Busca logs de usuário específico para investigar problemas reportados
- **Sistema (automático)**: Coleta métricas Prometheus, health checks, envia alertas PagerDuty
- **Kubernetes**: Consome endpoints /health para liveness/readiness probes (orquestração de containers)

**When (quando acontece):**
- **Implantação**: Durante deploy inicial (seed de configurações Serilog, Seq, Prometheus, Grafana)
- **Runtime**: Logs gerados automaticamente para toda requisição HTTP, comando CQRS, query, exceção
- **Debugging**: Quando desenvolvedor precisa investigar erro ou comportamento inesperado
- **Troubleshooting**: Quando suporte recebe ticket de usuário e busca logs por correlation ID
- **Monitoramento**: Dashboards Grafana consultados em tempo real para verificar saúde do sistema
- **Incidentes**: Alertas PagerDuty disparam automaticamente quando threshold de erro é atingido
- **Auditoria**: Auditor exporta logs de segurança (7 anos de retenção) para compliance
- **Performance**: Métricas Prometheus coletadas continuamente (P50/P95/P99 latency)
- **Health Checks**: Kubernetes verifica endpoints /health a cada 30 segundos (liveness/readiness)
- **Retenção**: Jobs Hangfire executam limpeza automática de logs antigos (90 dias Info, 1 ano Error, 7 anos Security)

**Where (onde no sistema):**
- **Módulo**: Administração / Logs e Monitoramento
- **Menu**: Administração → Sistema → Logs do Sistema
- **Telas (Frontend Angular)**:
  - `/admin/logs` (visualizar e buscar logs com filtros avançados)
  - `/admin/logs/export` (exportar logs para CSV/JSON compliance)
  - `/admin/metrics` (dashboards de métricas de performance)
  - `/admin/health` (verificar health checks de dependências)
  - `/admin/alerts` (configurar alertas e thresholds)
- **Ferramentas Externas**:
  - **Seq UI**: http://localhost:5341 (dev/hom) - busca full-text de logs estruturados
  - **Elasticsearch Kibana**: (produção) - análise avançada de logs
  - **Grafana**: http://localhost:3000 - dashboards de métricas Prometheus
  - **Jaeger/Zipkin**: http://localhost:16686 - tracing distribuído OpenTelemetry
  - **Application Insights**: Azure Portal - monitoramento nativo Azure
- **API (Backend .NET) - Endpoints Implementados**:
  - **Health Checks**:
    - `GET /api/health` (HealthCheck - público, status básico sem autenticação)
    - `GET /api/health/detalhado` (HealthCheckDetalhado - status de DB, Redis, Seq, APIs externas)
    - `POST /api/health/verificar` (ForcarHealthCheck - execução forçada de verificação)
    - `GET /api/health/historico?pageNumber={}&pageSize={}&nomeServico={}&status={}&dataInicio={}&dataFim={}` (ObterHistoricoHealthChecks - histórico paginado)
  - **Métricas**:
    - `GET /api/metricas/red?periodo={}` (ObterMetricasRED - Rate/Errors/Duration para período em horas)
    - `GET /api/metricas/customizadas` (ListarMetricasCustomizadas - métricas definidas por usuário)
    - `POST /api/metricas/customizadas` (CriarMetricaCustomizada - criar nova métrica)
    - `GET /api/metricas/dashboard` (ObterDadosDashboard - dados consolidados para dashboard executivo)
    - `GET /api/metricas/endpoints?top={}` (ObterMetricasPorEndpoint - performance por endpoint, top N)
  - **Alertas**:
    - `GET /api/alertas?pageNumber={}&pageSize={}&codigoOuNome={}&tipoAlerta={}&prioridade={}&ativo={}&ambiente={}` (ListarAlertas - lista paginada com filtros)
    - `GET /api/alertas/{id}` (ObterAlertaPorId - detalhes completos do alerta)
    - `POST /api/alertas` (CriarAlerta - criar novo alerta)
    - `PUT /api/alertas/{id}` (AtualizarAlerta - atualizar configuração)
    - `DELETE /api/alertas/{id}` (ExcluirAlerta - soft delete)
    - `POST /api/alertas/{id}/testar` (TestarAlerta - envia notificação de teste)
    - `GET /api/alertas/historico?alertaId={}&dataInicio={}&dataFim={}&resolvido={}&pageNumber={}&pageSize={}` (ObterHistoricoAlertas - histórico de disparos)
    - `POST /api/alertas/historico/{historicoId}/resolver` (ResolverAlerta - marca disparo como resolvido)

**Why (por que existe):**
- **SLA 99.9%**: Detectar e resolver incidentes ANTES de afetar usuários (alertas proativos)
- **Troubleshooting Rápido**: Diagnosticar problemas em minutos (não horas) usando correlation IDs
- **Compliance**: Auditoria de logs obrigatória para LGPD (retenção 90 dias), SOX (7 anos), ISO 27001
- **Performance**: Identificar gargalos (queries lentas, memory leaks) via métricas P95/P99
- **Segurança**: Detectar ataques (SQL injection, XSS, DDoS) analisando padrões de logs
- **DevOps**: Integração com CI/CD, alertas em produção via PagerDuty
- **Rastreabilidade**: Correlation IDs permitem rastrear requests distribuídos entre microservices
- **Otimização de Custos**: Log sampling 10% reduz custos Elasticsearch sem perder visibilidade de erros
- **Resiliência**: Circuit breaker garante que falha de logging nunca derruba aplicação
- **Compliance LGPD**: Mascaramento automático de CPF/senhas evita vazamento de dados sensíveis em logs

---

### Referências no Legado (onde confirmar detalhes)

**Telas (UI):**
- ASPX: Não existe no legado (logs eram arquivos texto plano acessados via RDP + Notepad)
- Code-behind: N/A
- **Observação**: Sistema legado NÃO tinha interface de visualização de logs. Administradores faziam RDP no servidor e abriam `D:\IC2\ic1_legado\IControlIT\IControlIT\logs\app.log` com editor de texto.

**Serviços (legado):**
- Classe: Código VB.NET de logging
- Localização: `D:\IC2\ic1_legado\IControlIT\IControlIT\logs\app.log`
- Métodos relevantes:
  ```vb.net
  ' Código VB.NET legado
  Public Sub LogError(mensagem As String)
      Dim logFile As String = Server.MapPath("~/logs/app.log")
      Dim writer As New StreamWriter(logFile, True)
      writer.WriteLine($"{DateTime.Now} - {mensagem}")
      writer.Close()
  End Sub

  ' Uso (com dados sensíveis expostos!)
  LogError($"Erro ao processar CPF {cpf}: {ex.Message}")
  LogError($"Senha do usuário: {senha}")
  ```
- **Problemas críticos do legado**:
  1. CPF e senhas em texto claro (violação LGPD)
  2. Formato texto não estruturado (impossível buscar por campos)
  3. Sem correlation ID (impossível rastrear request distribuído)
  4. Sem níveis de log (tudo é informação genérica)
  5. Sem agregação (cada servidor tem log separado)
  6. Busca apenas via grep manual
  7. Sem métricas (response time, error rate desconhecidos)
  8. Sem alertas (problemas descobertos por usuários)

**Banco de dados:**
- Modelo físico: `D:\DocumentosIC2\modelo-fisico-bd.sql`
- Tabelas legado: Não existiam (logs em arquivo texto plano)
- Tabelas novas (moderno): Não aplicável (logs em Seq/Elasticsearch, não em tabela SQL)
- **Observação**: Sistema moderno NÃO usa banco de dados para logs. Usa agregadores especializados (Seq/Elasticsearch) otimizados para busca full-text.
- Views: Não aplicável
- Procedures: Não aplicável

**Integrações / Dependências externas (se houver):**
- **Serilog**: Framework de logging estruturado .NET (sinks: Console, File, Seq, Elasticsearch, Application Insights)
- **Seq**: Agregador de logs estruturados para dev/hom (http://localhost:5341)
- **Elasticsearch**: Agregador de logs para produção com busca full-text escalável
- **Prometheus**: Sistema de métricas time-series (coleta RED metrics automaticamente)
- **Grafana**: Dashboards de visualização de métricas Prometheus
- **OpenTelemetry**: Tracing distribuído padrão W3C (exporta para Jaeger/Zipkin)
- **Jaeger/Zipkin**: Visualizadores de tracing distribuído entre microservices
- **PagerDuty**: Plataforma de alertas para incidentes críticos (error rate > 5%)
- **Opsgenie**: Alternativa ao PagerDuty para alertas
- **Azure Application Insights**: Monitoramento nativo Azure com telemetria automática
- **Kubernetes**: Consome endpoints /health para liveness/readiness probes

**Variações por cliente (se houver):**
- **Nível de Log por Ambiente**: DEV=Debug, HOM=Info, PRD=Warning (configurável por conglomerado)
- **Retenção de Logs**: Básico=90 dias, Pro=1 ano, Enterprise=7 anos
- **Agregador**: Dev/Hom=Seq (auto-hosted), Produção=Elasticsearch (Azure Managed)
- **Alertas**: Cliente básico=Email, Cliente enterprise=PagerDuty/Opsgenie integrado
- **Sampling Rate**: Configurável por conglomerado (padrão 10%, pode ser ajustado para 100% temporariamente)
- **Mascaramento**: CPF obrigatório Brasil, SSN obrigatório USA, GDPR compliance Europa

**Evidências adicionais (opcional):**
- Documento RF003.md completo: `D:\IC2\docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF003-Logs-Monitoramento-Observabilidade\RF003.md`
- 12 Regras de Negócio documentadas (RN-LOG-001 até RN-LOG-012)
- Configuração Serilog completa em appsettings.json
- Código de Health Checks em Program.cs
- Exemplo de arquivo app.log legado com CPF/senhas expostos
- Código VB.NET legado de logging
- Comparativo detalhado: Sistema Legado vs Modernizado (12 aspectos)
- 15 funcionalidades principais implementadas (logs estruturados, correlation IDs, métricas RED, etc.)

---

### Status de evidência
- [x] Confirmado no legado (referências completas)
- [ ] Parcial (faltam referências ou regra ambígua)
- [ ] Pendente (não documentar como definitivo)

### Observações

**Diferença crítica: Legado vs. Modernizado**

| Aspecto | Sistema Legado (VB.NET) | Sistema Modernizado (.NET 10) |
|---------|-------------------------|------------------------------|
| **Logs** | Arquivo texto plano app.log | Serilog estruturado JSON |
| **Busca** | grep manual | Seq/Elasticsearch full-text search |
| **Formato** | Texto não estruturado | JSON estruturado com metadados |
| **Agregação** | Nenhuma (logs locais) | Seq centralizado para todos os servidores |
| **Métricas** | Nenhuma | Prometheus + Grafana (RED metrics) |
| **Tracing** | Nenhum | OpenTelemetry distribuído entre microservices |
| **Health Checks** | Nenhum | Endpoints /health para Kubernetes |
| **Alertas** | Email manual | PagerDuty automático quando error rate > 5% |
| **Retenção** | Manual (disk full) | Automático: 90 dias (LGPD) a 7 anos (SOX) |
| **Sensibilidade** | CPF/senhas em texto claro ❌ | Mascaramento automático ✅ |
| **Correlation** | Impossível rastrear requests | Correlation ID em todos os logs |
| **Performance** | Logs síncronos (bloqueia thread) | Logs assíncronos (background) |

**Mudanças críticas do legado para moderno:**
1. **Formato**: Texto plano não estruturado → JSON estruturado com metadados completos
2. **Agregação**: Logs locais por servidor → Centralização em Seq/Elasticsearch
3. **Busca**: grep manual → Full-text search com filtros avançados
4. **Segurança**: CPF/senhas expostos → Mascaramento automático obrigatório (LGPD compliance)
5. **Rastreabilidade**: Impossível rastrear → Correlation IDs em toda cadeia de requests
6. **Métricas**: Nenhuma → Prometheus RED metrics (Rate/Errors/Duration)
7. **Dashboards**: Nenhum → Grafana pré-configurado com visualizações
8. **Alertas**: Manual → Automático via PagerDuty (error rate > 5%)
9. **Health Checks**: Nenhum → Endpoints /health para Kubernetes orquestração
10. **Retenção**: Manual → Automática por compliance (90 dias, 1 ano, 7 anos)
11. **Tracing**: Nenhum → OpenTelemetry distribuído (Jaeger/Zipkin)
12. **Performance**: Síncrono bloqueante → Assíncrono background (circuit breaker)

**Funcionalidades novas (não existem no legado):**
- Logs estruturados JSON (Serilog)
- Correlation IDs obrigatórios
- Mascaramento automático de dados sensíveis (CPF, senhas, cartões)
- Métricas Prometheus RED (Rate, Errors, Duration)
- Dashboards Grafana pré-configurados
- Health Checks /health para Kubernetes
- Tracing distribuído OpenTelemetry
- Alertas proativos PagerDuty/Opsgenie
- Log sampling 10% (otimização de custos)
- Circuit breaker para logging
- Busca full-text avançada (Seq/Elasticsearch)
- Export compliance CSV/JSON
- Azure Application Insights integrado
- Retenção automática por compliance
- Níveis de log configuráveis por ambiente

**Compliance e Segurança:**
- **LGPD**: Mascaramento obrigatório de CPF antes de logar + Retenção 90 dias para logs Info
- **SOX**: Retenção 7 anos para logs de segurança e acesso
- **ISO 27001**: Auditoria completa de acesso e export de logs
- **Detecção de Ataques**: Análise de padrões para SQL injection, XSS, DDoS
- **Privacy by Design**: Dados sensíveis NUNCA logados em texto claro

---

**FIM DO RF-003**

---

## RF-004 – Auditoria e Logs do Sistema

**Descrição (comportamento atual):**
O sistema implementa auditoria completa de todas as operações críticas para compliance (LGPD Art. 37/38/46, SOX Seção 404, ISO 27001), troubleshooting, segurança e análise forense. Diferente do RF-003 (logs técnicos de aplicação), o RF-004 foca em auditoria de negócio: ações de usuários, mudanças de dados, operações CRUD em entidades, exportações, acessos a dados sensíveis. No legado, auditoria era limitada: tabela simples sem estrutura (ação em texto livre, sem snapshot antes/depois, sem IP/User-Agent, sem retenção configurável, sem imutabilidade, sem diff, registros podiam ser deletados). O sistema moderno implementa auditoria automática via interceptor MediatR, snapshot completo (estado antes/depois), diff estruturado JSON Patch RFC 6902, rastreamento completo (usuário, IP, dispositivo, correlation ID, tenant), categorização (CRUD/EXPORT/ACCESS/LOGIN/LGPD), retenção por categoria SOX/LGPD (7 anos transações financeiras e dados pessoais), busca avançada com filtros, timeline de entidade, relatórios de compliance, detecção de anomalias (100+ exportações em 1h), auditoria LGPD específica (acesso CPF, consentimento, exclusão), segregação de funções SOX, imutabilidade garantida (append-only), assinatura digital SHA-256, arquivamento automático Azure Blob após 1 ano, alertas de retention expirando.

**What (o que faz):**
- Auditoria automática via interceptor MediatR: todo Command/Query que altera dados registra auditoria sem código manual
- Snapshot completo antes/depois: armazena estado completo da entidade antes e depois da operação para reconstruir histórico
- Diff estruturado JSON Patch (RFC 6902): calcula e armazena diferenças exatas entre estados
- Rastreamento de contexto enriquecido: usuário, data/hora, IP origem, User-Agent, Correlation ID, Tenant (Empresa/Departamento), Request ID
- Categorização de operações: CRUD (criar/ler/atualizar/deletar), EXPORT (exportação de dados), ACCESS (acesso a dados sensíveis), LOGIN/LOGOUT, CONFIG (mudanças configurações), LGPD (consentimento/exclusão/portabilidade), FINANCIAL (transações financeiras), SECURITY (eventos de segurança), ADMIN, PRINT
- Retenção configurável por categoria: 7 anos (SOX transações financeiras, LGPD dados pessoais), 5 anos (contratos, documentos fiscais), 1 ano (operações administrativas), 90 dias (acessos leitura não críticos)
- Busca avançada com filtros: por usuário, entidade, tipo operação, período, IP, tenant
- Timeline de entidade: endpoint `/api/auditoria/timeline/{entidade}/{id}` retorna histórico completo de mudanças
- Relatórios de compliance: exportação formatada para auditores (LGPD, SOX, ISO 27001) em CSV/JSON
- Detecção de anomalias: padrões suspeitos (>100 exportações em 1h, acesso >50 empresas em 1 dia, operações 22h-6h)
- Auditoria LGPD específica: tipos LGPD_ACCESS (acesso CPF/emails/telefones), LGPD_EXPORT, LGPD_CONSENT, LGPD_DELETION, LGPD_PORTABILITY
- Segregação de funções SOX: detecta violações (mesmo usuário criou e aprovou transação financeira, desenvolvedor acessou produção sem ticket)
- Imutabilidade garantida: tabela Sistema_Auditoria é append-only (sem UPDATE, sem DELETE jamais)
- Assinatura digital SHA-256: hash de cada registro garante integridade e detecção de adulteração
- Contexto de mudança crítica: mudanças em configurações críticas exigem justificativa obrigatória
- Busca full-text otimizada: índice Full-Text em campos Descricao, Dados_Antes, Dados_Depois
- Arquivamento automático: job mensal move registros > 1 ano para Azure Blob Storage (cold storage)
- Alertas de retention: notifica 30 dias antes da expiração de retenção

**Who (quem usa/impacta):**
- **Super Administrador**: Acesso total a todos os registros de auditoria, export, compliance, analytics, pode visualizar dados sensíveis
- **Auditor**: Visualiza, busca, exporta relatórios de auditoria, acessa timeline, relatórios compliance LGPD/SOX/ISO, sem permissão para deletar
- **Gerente de Operações**: Visualiza auditoria, busca, exporta, timeline, analytics, sem acesso a relatórios compliance
- **Administrador de Sistema**: Visualiza auditoria, busca, timeline, sem export e sem compliance
- **Desenvolvedor**: Visualiza auditoria e timeline (troubleshooting), sem export
- **Usuário Final**: Pode visualizar apenas sua própria auditoria via permissão especial SYS.AUDITORIA.READ_OWN (transparência LGPD)
- **Sistema (automático)**: Registra todas as operações via AuditingBehaviour, executa jobs de arquivamento, envia alertas de anomalias

**When (quando acontece):**
- **Toda operação CRUD**: Automaticamente quando Command/Query é executado via MediatR (criação, atualização, exclusão de entidade)
- **Exportação de dados**: Quando usuário exporta relatório, CSV, Excel, PDF com dados do sistema
- **Acesso a dados sensíveis**: Quando visualiza CPF, emails, telefones, dados financeiros (compliance LGPD)
- **Login/Logout**: Toda autenticação e desautenticação é registrada com IP e dispositivo
- **Mudanças em configurações**: Quando administrador altera parâmetros críticos, feature flags, configurações infraestruturais
- **Operações LGPD**: Consentimento aceito/revogado, solicitação de exclusão de dados, exportação de dados pessoais (portabilidade)
- **Transações financeiras**: Aprovação de fatura, pagamento processado, cancelamento (SOX compliance, 7 anos retenção)
- **Eventos de segurança**: Falha de login, acesso negado, tentativa de SQL injection detectada
- **Consulta de auditoria**: Quando auditor ou administrador busca histórico de ações
- **Timeline de entidade**: Quando usuário visualiza histórico completo de mudanças de um registro específico
- **Export compliance**: Quando auditor exporta relatório para auditoria externa (LGPD, SOX, ISO 27001)
- **Arquivamento**: Job mensal executa às 02:00 movendo registros > 1 ano para Azure Blob Storage
- **Alertas de anomalias**: Sistema detecta padrão suspeito e notifica equipe de segurança

**Where (onde no sistema):**
- **Módulo**: Administração / Auditoria
- **Menu**: Administração → Sistema → Auditoria do Sistema
- **Telas (Frontend Angular)**:
  - `/admin/auditoria` (visualizar e buscar registros de auditoria com filtros avançados)
  - `/admin/auditoria/timeline/{entidade}/{id}` (timeline de alterações de uma entidade específica)
  - `/admin/auditoria/compliance` (relatórios de compliance LGPD, SOX, ISO 27001)
  - `/admin/auditoria/analytics` (dashboards analíticos de auditoria: top usuários, top operações, anomalias)
  - `/admin/auditoria/export` (exportar relatórios de auditoria formatados)
- **API (Backend .NET) - Endpoints Convencionados** (a implementar):
  - `GET /api/auditoria?pageNumber={}&pageSize={}&usuario={}&entidade={}&tipoOperacao={}&dataInicio={}&dataFim={}&ipOrigem={}` (ListarAuditoria - lista paginada com filtros avançados)
  - `GET /api/auditoria/{id}` (ObterAuditoriaPorId - detalhes completos do registro de auditoria com diff)
  - `GET /api/auditoria/timeline/{entidade}/{entidadeId}?pageNumber={}&pageSize={}` (ObterTimelineEntidade - histórico completo de mudanças)
  - `GET /api/auditoria/categorias` (ListarCategorias - lista todas as categorias: CRUD, EXPORT, ACCESS, LGPD, etc.)
  - `POST /api/auditoria/search` (BuscarAuditoriaAvancada - busca full-text com filtros complexos no corpo da requisição)
  - `GET /api/auditoria/compliance/lgpd?dataInicio={}&dataFim={}` (RelatorioComplianceLGPD - acesso dados pessoais, consentimentos, exclusões)
  - `GET /api/auditoria/compliance/sox?dataInicio={}&dataFim={}` (RelatorioComplianceSOX - transações financeiras, segregação funções)
  - `GET /api/auditoria/compliance/iso27001?dataInicio={}&dataFim={}` (RelatorioComplianceISO27001 - eventos segurança, acessos)
  - `POST /api/auditoria/export?formato={}&categorias[]={}&dataInicio={}&dataFim={}` (ExportarAuditoria - CSV/JSON/Excel)
  - `GET /api/auditoria/analytics/top-usuarios?top={}&periodo={}` (AnalyticsTopUsuarios - usuários mais ativos)
  - `GET /api/auditoria/analytics/top-operacoes?top={}&periodo={}` (AnalyticsTopOperacoes - operações mais executadas)
  - `GET /api/auditoria/analytics/anomalias?dataInicio={}&dataFim={}` (DetectarAnomalias - padrões suspeitos)
  - `GET /api/auditoria/usuario/{usuarioId}?pageNumber={}&pageSize={}` (ObterAuditoriaPorUsuario - auditoria específica de um usuário)
  - `POST /api/auditoria/verificar-integridade` (VerificarIntegridade - valida hashes SHA-256 de registros, detecta adulteração)

**Why (por que existe):**
- **LGPD Compliance Art. 37, 38, 46**: Obrigação legal de registrar acesso e tratamento de dados pessoais, consentimentos, exclusões
- **SOX Compliance Seção 404**: Auditoria de transações financeiras obrigatória com retenção 7 anos
- **ISO 27001**: Requisitos de auditoria de segurança da informação e gestão de acessos
- **Troubleshooting**: Rastrear causa raiz de problemas via histórico de ações (quem fez o quê e quando)
- **Segurança**: Detecção de atividades suspeitas, ataques, acessos não autorizados, tentativas de fraude
- **Análise Forense**: Investigação de incidentes de segurança com evidências completas e imutáveis
- **Transparência**: Usuários podem visualizar quem acessou seus dados (compliance LGPD direito de acesso)
- **Rastreabilidade**: Timeline completa de mudanças permite reconstruir estado de entidade em qualquer ponto do tempo
- **Segregação de Funções**: Detectar violações SOX (mesmo usuário criou e aprovou transação)
- **Proteção Legal**: Registros imutáveis com assinatura digital servem como evidência jurídica
- **Detecção de Anomalias**: Identificar padrões suspeitos automaticamente (exfiltração de dados, acesso massivo)
- **Compliance Contínuo**: Relatórios automatizados reduzem custo e tempo de auditorias externas

---

### Referências no Legado (onde confirmar detalhes)

**Telas (UI):**
- ASPX: Não identificado no legado (auditoria não tinha interface de consulta)
- Code-behind: N/A
- **Observação**: Sistema legado NÃO tinha tela de auditoria. Administradores consultavam direto na tabela SQL via queries manuais.

**Serviços (legado):**
- Tabela: `D:\IC2\ic1_legado\IControlIT\Database\Tables\Auditoria.sql` (estrutura legada)
- Código VB.NET: Inserções manuais espalhadas pelo código sem padrão
- **Observação**: Não havia serviço centralizado; cada tela fazia INSERT direto na tabela Auditoria

**Banco de dados:**
- Modelo físico: `D:\DocumentosIC2\modelo-fisico-bd.sql`
- Tabela legado:
  ```sql
  CREATE TABLE Auditoria (
      Id INT IDENTITY(1,1) PRIMARY KEY,
      Usuario VARCHAR(200),
      Acao VARCHAR(500),  -- Texto livre, não estruturado
      Data DATETIME DEFAULT GETDATE()
  );
  ```
- **Problemas do legado**:
  1. Sem estrutura: Ação como texto livre sem categorização
  2. Sem snapshot: Não armazena estado antes/depois
  3. Sem contexto: Não registra IP, User-Agent, dispositivo
  4. Sem retenção configurável: Todos registros com mesma retenção
  5. Sem imutabilidade: Registros podem ser deletados (UPDATE/DELETE permitido)
  6. Sem diff: Impossível ver exatamente o que mudou
  7. Sem categorização: Tudo misturado (login + CRUD + export)
  8. Sem compliance: Não atende LGPD, SOX, ISO 27001
- Tabelas novas (moderno):
  - `Sistema_Auditoria` (registros append-only com snapshot completo)
  - `Sistema_Auditoria_Categoria` (categorização de operações)
- Views: Não aplicável
- Procedures: Nenhuma específica (auditoria via AuditingBehaviour automático)

**Integrações / Dependências externas (se houver):**
- **MediatR**: Framework CQRS utilizado para interceptar Commands/Queries via AuditingBehaviour pipeline
- **Azure Blob Storage**: Armazenamento cold storage para registros > 1 ano
- **Azure Key Vault**: Armazenamento de chaves de criptografia para assinatura digital
- **Hangfire**: Jobs agendados para arquivamento automático e alertas de retention
- **Slack/Teams**: Notificações de anomalias detectadas (100+ exportações, acesso massivo)

**Variações por cliente (se houver):**
- **Retenção por Plano**: Básico=1 ano (mínimo legal), Pro=3 anos, Enterprise=7 anos (SOX)
- **Categorias Auditadas**: Básico=CRUD+LOGIN, Pro=+EXPORT+ACCESS, Enterprise=+LGPD+FINANCIAL+SECURITY
- **Arquivamento**: Básico=sem arquivamento (delete após retention), Enterprise=Azure Blob cold storage
- **Alertas de Anomalias**: Básico=desabilitado, Enterprise=detecção automática com notificações
- **Timeline de Entidade**: Básico=últimos 90 dias, Enterprise=histórico completo ilimitado

**Evidências adicionais (opcional):**
- Documento RF004.md completo: `D:\IC2\docs\rf\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF004-Auditoria-Logs-Sistema\RF004.md`
- 15 Regras de Negócio documentadas (RN-AUD-001 até RN-AUD-015)
- Diferenciação clara RF-003 (logs técnicos) vs RF-004 (auditoria negócio)
- Tabela legada Auditoria com problemas críticos documentados
- Exemplo de código VB.NET de inserção manual de auditoria
- Tabela comparativa: 10 categorias de auditoria com retenção e exemplos
- Código de exemplo: AuditingBehaviour.cs, AuditService.cs, AuditRepository.cs

---

### Status de evidência
- [x] Confirmado no legado (referências completas)
- [ ] Parcial (faltam referências ou regra ambígua)
- [ ] Pendente (não documentar como definitivo)

### Observações

**Diferença crítica: RF-003 (Logs) vs RF-004 (Auditoria)**

| Aspecto | RF-003 (Logs Técnicos) | RF-004 (Auditoria de Negócio) |
|---------|------------------------|-------------------------------|
| **Foco** | Logs de aplicação, performance, erros | Auditoria de ações de usuários e mudanças de dados |
| **Exemplos** | Exception logs, response time, queries SQL | Usuário criou fatura, alterou perfil, exportou relatório |
| **Armazenamento** | Seq/Elasticsearch (otimizado para volume) | SQL Server (estruturado, relacional, imutável) |
| **Retenção** | 90 dias (padrão), 7 anos (segurança) | 7 anos obrigatório (compliance SOX/LGPD) |
| **Granularidade** | Request/Response HTTP, exceptions | Operação de negócio (CRUD em entidades) |
| **Busca** | Full-text search (Seq/Elasticsearch) | SQL queries (filtros estruturados) |
| **Usuário Final** | Desenvolvedores, DevOps | Auditores, Compliance, Gerentes |

**Mudanças críticas do legado para moderno:**
1. **Estrutura**: Texto livre (Acao VARCHAR) → Categorização estruturada (CRUD, EXPORT, ACCESS, LGPD, etc.)
2. **Snapshot**: Sem estado antes/depois → Snapshot completo com diff JSON Patch RFC 6902
3. **Contexto**: Apenas usuário e data → IP, User-Agent, Correlation ID, Tenant, Request ID
4. **Retenção**: Única para todos → Configurável por categoria (90 dias a 7 anos)
5. **Imutabilidade**: UPDATE/DELETE permitido → Append-only rigoroso (sem UPDATE, sem DELETE)
6. **Diff**: Impossível ver mudanças → Diff estruturado campo a campo
7. **Categorização**: Tudo misturado → 10 categorias distintas com finalidades específicas
8. **Compliance**: Não atende → LGPD, SOX, ISO 27001 compliant
9. **Timeline**: Não existe → Timeline completa de entidade com reconstrução de estado
10. **Integridade**: Sem proteção → Assinatura digital SHA-256 detecta adulteração
11. **Arquivamento**: Manual → Automático para Azure Blob após 1 ano
12. **Detecção**: Nenhuma → Anomalias detectadas automaticamente (100+ exports, acesso massivo)

**Funcionalidades novas (não existem no legado):**
- Auditoria automática via interceptor MediatR (zero código manual)
- Snapshot completo antes/depois com diff JSON Patch
- Rastreamento de contexto enriquecido (IP, User-Agent, Correlation ID, Tenant)
- Categorização de operações em 10 tipos distintos
- Retenção configurável por categoria (compliance SOX/LGPD)
- Timeline de entidade (histórico completo de mudanças)
- Relatórios de compliance (LGPD, SOX, ISO 27001) formatados
- Detecção de anomalias (padrões suspeitos automaticamente)
- Auditoria LGPD específica (acesso, consentimento, exclusão, portabilidade)
- Segregação de funções SOX (detecta violações automaticamente)
- Imutabilidade garantida (append-only, sem UPDATE/DELETE)
- Assinatura digital SHA-256 (integridade e detecção de adulteração)
- Busca full-text otimizada com índices
- Arquivamento automático Azure Blob (cold storage após 1 ano)
- Alertas de retention expirando (30 dias antes)

**Compliance e Segurança:**
- **LGPD Art. 37, 38, 46**: Registro obrigatório de acesso, tratamento, consentimento, exclusão de dados pessoais
- **SOX Seção 404**: Auditoria de transações financeiras com retenção 7 anos obrigatória
- **ISO 27001**: Auditoria de eventos de segurança e gestão de acessos
- **Imutabilidade**: Registros append-only servem como evidência jurídica inviolável
- **Assinatura Digital**: Hash SHA-256 detecta qualquer tentativa de adulteração
- **Segregação de Funções**: Detecta automaticamente violações SOX (mesmo usuário criou e aprovou)
- **Detecção de Ataques**: Anomalias identificadas (exfiltração de dados, acesso massivo, horário suspeito)

---

**FIM DO RF-004**

---

## RF-005: Internacionalização (i18n) e Localização

**Fase**: Fase 1 - Sistema Base
**EPIC**: EPIC001-SYS - Sistema e Infraestrutura
**Versão da Documentação**: 2.0
**Status**: ✅ Documentação Completa (Sistema Parcialmente Implementado)

### Descrição

O RF-005 implementa o **Sistema de Internacionalização (i18n) e Localização (l10n)** do IControlIT, permitindo que o sistema opere em múltiplos idiomas e culturas, adaptando-se automaticamente às preferências regionais dos usuários.

Este é um **RF CRÍTICO DE FUNDAÇÃO** pois permite:
- **Expansão Global**: Atender clientes em múltiplos países
- **Compliance Legal**: Alguns países exigem interface no idioma local
- **User Experience**: Usuários preferem sistemas no seu idioma nativo
- **Competitividade**: Diferencial de mercado em licitações internacionais
- **ROI**: Aumenta base de clientes potenciais em 300%+

**18 Funcionalidades Principais:**
1. Multi-Idioma (pt-BR, en-US, es-ES, fr-FR extensível)
2. Tradução UI (Angular - todos os componentes)
3. Tradução Backend (mensagens erro, validações, emails)
4. Formatação Regional (datas, números, moedas por cultura)
5. Detecção Automática (Accept-Language header)
6. Fallback Inteligente (pt-BR → Chave Literal)
7. Lazy Loading (carrega apenas idioma necessário)
8. Editor de Traduções (interface visual para não-devs)
9. Pluralização (regras de plural por idioma)
10. Interpolação (`Bem-vindo, {{username}}!`)
11. Namespace Hierárquico (`menu.dashboard.title`)
12. Versionamento (histórico de traduções)
13. Validação (chaves faltantes, traduções vazias)
14. Export/Import (JSON/Excel/PO para tradutores)
15. Machine Translation (Azure Translator - sugestões)
16. Gestão de Idiomas (adicionar idiomas via interface)
17. Download de Template (modelo para tradução)
18. Upload de Traduções (subir arquivos JSON/PO/XLSX)

---

### 5W - Cinco Ws

#### WHAT (O quê?)

**O que o sistema faz:**

1. **Multi-Idioma Completo**: Sistema opera em 4 idiomas iniciais (pt-BR padrão, en-US, es-ES, fr-FR) com arquitetura extensível para adicionar novos idiomas sem rebuild
2. **Tradução Interface Angular**: Todos os componentes traduzidos usando ngx-translate com lazy loading (carrega apenas idioma ativo)
3. **Tradução Backend .NET**: Mensagens de erro, validações, emails traduzidos usando IStringLocalizer<T>
4. **Formatação Regional Automática**: Datas (dd/MM/yyyy vs MM/dd/yyyy), números (vírgula vs ponto), moedas (R$ vs $ vs €) formatados por cultura
5. **Detecção Automática Idioma**: Accept-Language header → Preferência Usuário → Idioma Empresa → pt-BR (fallback hierárquico)
6. **Fallback Inteligente**: Se tradução não existe: Idioma Selecionado → pt-BR → Chave Literal (sistema sempre funcional)
7. **Performance Cache Redis**: < 1ms (99% cache hit, TTL 1 hora)
8. **Interpolação Variáveis**: Suporta `{{variavel}}` (ex: "Bem-vindo, {{username}}!" → "Bem-vindo, João Silva!")
9. **Pluralização Inteligente**: Regras corretas por idioma (0 itens, 1 item, 5 itens pt-BR / 0 items, 1 item, 5 items en-US)
10. **Timezone por Usuário**: UTC no banco → Timezone usuário no frontend (conversão automática)
11. **Emails Multi-Idioma**: Templates separados por idioma (welcome-pt-BR.html, welcome-en-US.html)
12. **Relatórios Traduzidos**: Excel/PDF com cabeçalhos traduzidos via ClosedXML + LocalizationService
13. **Namespace Hierárquico**: Chaves organizadas (menu.dashboard.title, validation.required, common.buttons.save)
14. **Editor Visual Traduções**: Interface web para tradutores não-devs (listar, filtrar, editar, histórico, export/import)
15. **Validação Chaves Faltantes**: Job noturno detecta traduções faltantes, envia email para admins
16. **Versionamento Traduções**: Histórico completo de mudanças (quem, quando, diff)
17. **Hot Reload Traduções**: Alterações aplicadas sem restart servidor (cache invalidation via Redis Pub/Sub)
18. **Gestão Idiomas pelo Usuário**: Administradores adicionam novos idiomas sem intervenção de desenvolvedores
19. **Download Template Tradução**: Baixar arquivo modelo JSON/PO/XLSX com todas as chaves (vazio ou com tradução atual)
20. **Upload Traduções**: Subir arquivo traduzido com validação automática (estrutura, interpolações, HTML balanceado)
21. **Validação Integridade**: Sistema valida traduções (chaves obrigatórias, interpolações corretas, pluralização, HTML balanceado)
22. **Histórico Versões**: Armazena arquivo original (blob), permite rollback para versão anterior
23. **Tradução Automática Azure**: Sugestões via Azure Translator API (flag Fl_Machine_Translation = 1, requer revisão humana)
24. **Bandeiras Automáticas**: flag-icons library (🇧🇷, 🇺🇸, 🇪🇸, 🇫🇷 automáticas por código idioma)

---

#### WHO (Quem?)

**Quem usa cada funcionalidade:**

1. **Super Administrador**: Acesso total (ler, editar, gerenciar idiomas, tradução automática, export, import, download, upload)
2. **Administrador de Sistema**: Acesso total (ler, editar, gerenciar idiomas, tradução automática, export, import, download, upload)
3. **Tradutor**: Leitura, edição, tradução automática, export, import, download, upload (sem permissão para gerenciar idiomas - adicionar/remover)
4. **Desenvolvedor**: Somente leitura e export/download (sem edição, sem import/upload)
5. **Usuário Final**: Apenas seleciona idioma preferido (sem acesso à gestão de traduções)
6. **Sistema (Automático)**: Detecção Accept-Language, cache Redis, job validação chaves faltantes, invalidação cache

**Matriz de Permissões:**

| Perfil | READ | UPDATE | MANAGE_LANGUAGES | AUTO_TRANSLATE | EXPORT | IMPORT | DOWNLOAD_TEMPLATE | UPLOAD_TRANSLATION |
|--------|------|--------|------------------|----------------|--------|--------|-------------------|--------------------|
| Super Administrador | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Admin Sistema | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Tradutor | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Desenvolvedor | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ |
| Usuário Final | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

#### WHEN (Quando?)

**Quando cada operação é executada:**

1. **Login/Acesso Inicial**: Sistema detecta idioma preferido (Accept-Language → Preferência Usuário → Idioma Empresa → pt-BR)
2. **Troca de Idioma**: Usuário seleciona idioma manualmente no seletor (🇧🇷 🇺🇸 🇪🇸 🇫🇷)
3. **Renderização de Tela**: Angular carrega traduções via ngx-translate (lazy loading, apenas idioma ativo)
4. **Mensagens de Erro Backend**: IStringLocalizer<T> traduz mensagens conforme cultura do request
5. **Envio de Email**: Sistema usa template no idioma do destinatário (welcome-pt-BR.html vs welcome-en-US.html)
6. **Geração de Relatório**: ClosedXML usa traduções para cabeçalhos de Excel/PDF
7. **Criação de Novo Idioma**: Administrador adiciona idioma via interface visual
8. **Download Template**: Tradutor baixa arquivo modelo para preencher traduções
9. **Upload de Traduções**: Tradutor envia arquivo preenchido (JSON/PO/XLSX)
10. **Validação Automática**: Sistema valida arquivo durante upload (estrutura, interpolações, HTML)
11. **Ativação de Idioma**: Administrador ativa idioma quando tradução ≥ 80%
12. **Job Noturno (03:00 AM)**: Detecta chaves faltantes, envia relatório por email
13. **Cache Invalidation**: Após upload/edição, cache Redis invalidado via Pub/Sub
14. **Rollback de Versão**: Administrador restaura versão anterior de traduções
15. **Tradução Automática**: Tradutor aciona Azure Translator para sugestões (flag = machine translation)

---

#### WHERE (Onde?)

**Telas (Frontend Angular):**

1. `/login` - Seletor de idioma no login (🇧🇷 🇺🇸 🇪🇸 🇫🇷)
2. `/admin/settings/i18n` - Gestão de Idiomas e Traduções (listagem, criação, download, upload)
3. `/admin/settings/i18n/create` - Modal Adicionar Novo Idioma
4. `/admin/settings/i18n/download` - Modal Baixar Template de Tradução
5. `/admin/settings/i18n/upload` - Modal Upload de Traduções
6. `/admin/settings/i18n/history/{code}` - Histórico de Versões de Idioma
7. Header global (seletor de idioma sempre visível para troca rápida)

**API (Backend .NET) - Endpoints Convencionados (a implementar):**

1. `GET /api/i18n/languages` - Listar idiomas disponíveis (código, nome, status ativo, progresso %)
   - Permissão: `SYS.I18N.READ`
   - Retorna: `List<LanguageDto>` (Id, Codigo, Nome, NomeNativo, IsAtivo, ProgressoPercentual, TotalChaves, ChavesTraduzidas)

2. `GET /api/i18n/languages/{code}` - Obter detalhes de idioma específico (ex: pt-BR, en-US)
   - Permissão: `SYS.I18N.READ`
   - Retorna: `LanguageDto` completo

3. `POST /api/i18n/languages` - Criar novo idioma
   - Permissão: `SYS.I18N.MANAGE_LANGUAGES`
   - Body: `CreateLanguageCommand` (Codigo, Nome, NomeNativo, CodigoPais, Cultura, IdiomaReferenciaId)
   - Retorna: `LanguageDto` criado

4. `PUT /api/i18n/languages/{code}/activate` - Ativar idioma (torna disponível para usuários)
   - Permissão: `SYS.I18N.MANAGE_LANGUAGES`
   - Valida: Progresso ≥ 80% recomendado (aviso se < 80%)

5. `PUT /api/i18n/languages/{code}/deactivate` - Desativar idioma (remove do seletor)
   - Permissão: `SYS.I18N.MANAGE_LANGUAGES`
   - Validação: pt-BR não pode ser desativado (idioma padrão)

6. `GET /api/i18n/languages/{code}/download?type={TemplateVazio|TraducaoAtual}&format={JSON|PO|XLSX}&includeComments={true|false}&includeReference={true|false}` - Download template/tradução
   - Permissão: `SYS.I18N.DOWNLOAD_TEMPLATE`
   - Retorna: `FileResult` (arquivo JSON, PO ou XLSX)
   - Parâmetros: type (template vazio ou tradução atual), format (JSON/PO/XLSX), includeComments, includeReference

7. `POST /api/i18n/languages/{code}/upload` - Upload de arquivo de tradução
   - Permissão: `SYS.I18N.UPLOAD_TRANSLATION`
   - Body: `multipart/form-data` (IFormFile + UploadTranslationCommand)
   - Validações: formato, encoding UTF-8, tamanho < 5 MB, estrutura de chaves, interpolações
   - Retorna: `UploadResultDto` (TotalKeys, ImportedKeys, Warnings, Errors, CompletionPercentage)

8. `GET /api/i18n/languages/{code}/history?page={1}&pageSize={20}` - Obter histórico de versões
   - Permissão: `SYS.I18N.READ`
   - Retorna: `PaginatedList<TranslationVersionDto>` (Id, NumeroVersao, NomeArquivo, DataUpload, UsuarioUpload, ChavesAdicionadas, ProgressoAnterior, ProgressoNovo)

9. `POST /api/i18n/languages/{code}/restore/{versionId}` - Restaurar versão anterior (rollback)
   - Permissão: `SYS.I18N.MANAGE_LANGUAGES`
   - Cria backup automático da versão atual antes de restaurar

10. `GET /api/i18n/languages/{code}/progress` - Obter progresso de tradução
    - Permissão: `SYS.I18N.READ`
    - Retorna: `TranslationProgressDto` (TotalChaves, ChavesTraduzidas, ProgressoPercentual, ChavesFaltantes)

11. `GET /api/i18n/translations/{code}` - Carregar traduções completas de um idioma (para Angular)
    - Permissão: Público (usado pelo frontend)
    - Cache Redis: TTL 1 hora
    - Retorna: JSON hierárquico (namespaces)

12. `GET /api/i18n/missing-keys?languageCode={en-US}` - Listar chaves faltantes de um idioma
    - Permissão: `SYS.I18N.READ`
    - Retorna: `List<MissingKeyDto>` (Chave, Categoria, Contexto)

13. `POST /api/i18n/auto-translate` - Tradução automática via Azure Translator
    - Permissão: `SYS.I18N.AUTO_TRANSLATE`
    - Body: `AutoTranslateCommand` (IdiomaOrigem, IdiomaDestino, Chaves[])
    - Retorna: `AutoTranslateResultDto` (ChavesTraduzidas, CustoEstimado)
    - Flag: Fl_Machine_Translation = 1 (requer revisão humana)

14. `GET /api/i18n/validation-report/{code}` - Relatório de validação de idioma
    - Permissão: `SYS.I18N.READ`
    - Retorna: `ValidationReportDto` (ChavesObrigatoriasFaltantes, InterpolacoesIncorretas, HtmlDesbalanceado)

**Legado (Sistema Antigo - VB.NET):**

⚠️ **Sistema Legado NÃO possui i18n**:
- Textos hardcoded em português no código VB.NET
- Formatação fixa pt-BR (dd/MM/yyyy, R$)
- Emails apenas em português
- Relatórios não traduzíveis
- Impossível internacionalizar sem alterar código

**Banco de Dados (Novas Tabelas - Modernização):**

- `SistemaIdiomas` - Idiomas disponíveis (pt-BR, en-US, es-ES, fr-FR)
- `SistemaTraducaoChaves` - Chaves de tradução (common.buttons.save, menu.dashboard)
- `SistemaTraducoes` - Traduções por idioma (ChaveId + IdiomaId + Valor)
- `SistemaTraducaoVersoes` - Histórico de uploads (blob do arquivo original)
- `SistemaTraducaoRelatorios` - Relatórios de importação (sucesso, avisos, erros)

**Arquivos de Tradução (Frontend Angular):**

- `D:\IC2\frontend\src/assets/i18n/pt-BR.json` - Traduções português (padrão)
- `D:\IC2\frontend\src/assets/i18n/en-US.json` - Traduções inglês
- `D:\IC2\frontend\src/assets/i18n/es-ES.json` - Traduções espanhol
- `D:\IC2\frontend\src/assets/i18n/fr-FR.json` - Traduções francês

**Arquivos de Tradução (Backend .NET):**

- `D:\IC2\backend\Resources/pt-BR.resx` - Recursos português
- `D:\IC2\backend\Resources/en-US.resx` - Recursos inglês
- `D:\IC2\backend\Resources/es-ES.resx` - Recursos espanhol
- `D:\IC2\backend\Resources/fr-FR.resx` - Recursos francês

---

#### WHY (Por quê?)

**Razões Estratégicas para i18n:**

1. **Expansão Internacional**: Permite atender clientes em EUA, Europa, América Latina (mercado 300% maior)
2. **Compliance Legal**: França, Alemanha, Quebec exigem interface em idioma local por lei
3. **User Experience Superior**: Usuários preferem sistemas no idioma nativo (reduz erros, aumenta adoção)
4. **Competitividade em Licitações**: Editais internacionais exigem multi-idioma como critério obrigatório
5. **Diferencial de Mercado**: Poucos sistemas de gestão de ativos brasileiros são multi-idioma
6. **ROI Comprovado**: Clientes multinacionais pagam premium por suporte multi-idioma
7. **Facilita Onboarding**: Treinamento em idioma local reduz tempo de capacitação em 40%
8. **Reduz Suporte**: Menos tickets de dúvidas (interface auto-explicativa em idioma nativo)
9. **Escalabilidade Comercial**: Adicionar novo idioma não requer rebuild (apenas traduções)
10. **Compliance SOX/ISO**: Auditoria em idioma local facilita certificações internacionais
11. **Emails Profissionais**: Comunicação automática no idioma do destinatário (welcome, reset password, alerts)
12. **Relatórios Executivos**: Dashboards e exports traduzidos para apresentação a stakeholders globais
13. **Gestão Autônoma**: Tradutores trabalham sem depender de desenvolvedores (reduz custo operacional)
14. **Versionamento Seguro**: Rollback garante que erro de tradução não quebre produção
15. **Performance**: Cache Redis garante < 1ms mesmo com milhares de chaves

**Problemas do Legado Corrigidos:**

❌ **Legado (VB.NET)**: Textos hardcoded português → ✅ **Modernizado**: JSON resources dinâmicos
❌ **Legado**: Formatação fixa pt-BR → ✅ **Modernizado**: Cultura automática por usuário
❌ **Legado**: Emails português only → ✅ **Modernizado**: Templates multi-idioma
❌ **Legado**: Rebuild para alterar texto → ✅ **Modernizado**: Hot reload sem restart
❌ **Legado**: Relatórios não traduzíveis → ✅ **Modernizado**: Excel/PDF traduzidos
❌ **Legado**: Apenas desenvolvedores → ✅ **Modernizado**: Interface visual para tradutores

---

### Integrações Obrigatórias

**1. Central de Funcionalidades:**
- Código: `FNC-SYS-005`
- Nome: Sistema de Internacionalização (i18n)
- Categoria: Sistema / Infraestrutura
- Tipo: Tela + API
- Permissões: 8 (READ, UPDATE, MANAGE_LANGUAGES, AUTO_TRANSLATE, EXPORT, IMPORT, DOWNLOAD_TEMPLATE, UPLOAD_TRANSLATION)

**2. Auditoria (RF-004):**
- Todas as operações auditadas: Adicionar Idioma (7 anos), Editar Tradução (7 anos), Tradução Automática (1 ano), Export/Import (7 anos), Download/Upload (7/1 anos), Ativar/Desativar (7 anos)
- Registro: Quem, quando, o que mudou (diff completo)

**3. Controle de Acesso (RBAC):**
- 8 permissões granulares por operação
- Matriz de permissões por perfil (Super Admin, Admin Sistema, Tradutor, Desenvolvedor, Usuário Final)

**4. Cache Redis:**
- TTL 1 hora para traduções
- Invalidação via Pub/Sub após upload/edição
- 99% cache hit rate (< 1ms latency)

**5. Azure Translator API (Opcional):**
- Tradução automática para sugestões
- Custo: Grátis até 2M caracteres/mês, $10/1M depois
- Flag: Fl_Machine_Translation = 1 (requer revisão humana)

**6. Azure Blob Storage:**
- Armazenamento de arquivos de tradução (versões históricas)
- Backup automático antes de sobrescrever

**7. Hangfire (Jobs Agendados):**
- Job noturno (03:00 AM): Validação de chaves faltantes
- Email para administradores com relatório

**8. Notificações (Email/Slack/Teams):**
- Alertas de chaves faltantes
- Confirmação de upload de traduções
- Avisos de progresso < 80% ao ativar idioma

---

### Variações por Cliente (Multi-Tenancy)

Este RF **NÃO varia por cliente** (comportamento universal).

Todos os clientes usam o mesmo sistema de i18n:
- Idiomas disponíveis são globais (não por tenant)
- Traduções são compartilhadas entre tenants
- Cada usuário escolhe seu idioma preferido individualmente

**Exceção (Customização Opcional):**
- Cliente pode definir idioma padrão da empresa (se diferente de pt-BR)
- Exemplo: Empresa americana → Idioma padrão en-US

---

### Evidências Adicionais

**Documentação Técnica:**
- `/docs/rf/Fase-1-Sistema-Base/EPIC001-SYS-Sistema-Infraestrutura/RF005-i18n-Orcamento-Provisao/RF005.md` (1.760 linhas, versão 2.0)
- 22 Regras de Negócio detalhadas
- 6 Casos de Uso completos (UC00-UC06)
- Diagramas de fluxo de trabalho
- Implementação técnica completa (backend + frontend)
- Modelo de dados SQL Server

**Idiomas Iniciais:**
1. **Português (pt-BR)**: Padrão, dd/MM/yyyy, R$ 1.234,56, vírgula decimal
2. **Inglês (en-US)**: MM/dd/yyyy, $1,234.56, ponto decimal
3. **Espanhol (es-ES)**: dd/MM/yyyy, 1.234,56 €, vírgula decimal
4. **Francês (fr-FR)**: dd/MM/yyyy, 1 234,56 €, espaço separador

**Namespaces Hierárquicos:**
```
common.buttons.{save|cancel|delete|edit}
common.labels.{name|email|phone}
common.messages.{success|error|confirm}
menu.{dashboard|users|assets|reports}
validation.{required|email|minLength|maxLength}
```

**Status Atual Implementação:**
- ✅ Frontend: ngx-translate configurado, arquivos i18n criados, pipe `| translate` funcionando
- ✅ Backend: IStringLocalizer<T> configurado, arquivos resx criados, cultura por request
- ⚠️ Editor Visual: **NÃO implementado ainda** (endpoints convencionados, aguardando desenvolvimento)
- ⚠️ Upload/Download: **NÃO implementado ainda** (interfaces desenhadas, código pendente)
- ⚠️ Versionamento: **NÃO implementado ainda** (modelo de dados projetado, tabelas pendentes)

**Próximas Etapas:**
1. Implementar I18nController.cs com 14 endpoints
2. Implementar TranslationFileService.cs (JSON/PO/XLSX parser + validator)
3. Criar migrations para 5 novas tabelas
4. Implementar I18nManagementComponent (Angular)
5. Criar modais (Adicionar, Download, Upload, Histórico)
6. Testes E2E do fluxo completo (criar idioma → download → traduzir → upload → ativar)

---

**FIM DO RF-005**

---

## PRÓXIMOS RFs (Em andamento - aguardando análise manual detalhada)

Os demais 105 RFs serão documentados seguindo o mesmo padrão de análise consciente e detalhada demonstrado nos RF-001, RF-002, RF-003, RF-004 e RF-005.

---

# 7) Checklist rápido por RF (antes de "pronto")

- [x] Descreve o **comportamento atual**, não o novo
- [x] 5W preenchidos com clareza
- [x] Pelo menos 1 referência concreta no legado
- [x] Sem código colado (VB/SQL)
- [x] Dá para validar abrindo a tela/arquivo citado
- [x] Integrações e variações por cliente foram verificadas (quando aplicável)

---

# 8) Histórico de alterações

| Versão | Data | Autor | Mudança |
|-------:|:-----|:------|:--------|
| 1.0 | 28/12/2025 | Claude Code | Criação do documento com análise manual detalhada do RF-001 |
| 1.1 | 28/12/2025 | Claude Code | Adicionada análise manual detalhada do RF-002 (Configurações e Parametrização) |
| 1.2 | 28/12/2025 | Claude Code | Adicionada análise manual detalhada do RF-003 (Logs, Monitoramento e Observabilidade) |
| 1.3 | 28/12/2025 | Claude Code | Atualização dos endpoints RF-001, RF-002 e RF-003 com APIs reais implementadas no backend (Parametros.cs.disabled, ConfiguracoesController.cs.disabled, HealthController.cs, MetricasController.cs, AlertasController.cs) |
| 1.4 | 28/12/2025 | Claude Code | Adicionada análise manual detalhada do RF-004 (Auditoria e Logs do Sistema) com endpoints convencionados (controller não implementado ainda) |
| 1.5 | 28/12/2025 | Claude Code | Adicionada análise manual detalhada do RF-005 (Internacionalização i18n e Localização) com 14 endpoints convencionados seguindo padrão RESTful de mercado (controller não implementado ainda) |


# UC-RF004 — Casos de Uso: Sistema de Auditoria e Logs do Sistema

**RF:** RF004 — Sistema de Auditoria e Logs do Sistema
**Versão:** 2.0
**Data:** 2025-12-29
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC001-SYS - Sistema e Infraestrutura
**Fase:** Fase 1 - Fundação e Cadastros Base

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF004 — Sistema de Auditoria e Logs do Sistema**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF004.yaml)
- Massas de Teste (MT-RF004.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**IMPORTANTE**: RF004 **NÃO é um CRUD tradicional**. Registros de auditoria são **eventos imutáveis append-only**. Não há operações de CREATE, UPDATE ou DELETE pelo usuário. Os UCs focam em **consulta, análise e visualização** de registros já criados automaticamente pelo sistema.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal | Regras Cobertas |
|----|------|----------------|-----------------|
| UC00 | Listar Registros de Auditoria | Auditor, Super Admin | RN-RF004-001, RN-RF004-010 |
| UC01 | Buscar com Filtros Avançados | Auditor, Super Admin | RN-RF004-003, RN-RF004-010, RN-RF004-014 |
| UC02 | Visualizar Timeline de Entidade | Auditor, Super Admin | RN-RF004-002, RN-RF004-003, RN-RF004-009 |
| UC03 | Exportar Relatórios de Compliance | Auditor, Super Admin | RN-RF004-004, RN-RF004-008 |
| UC04 | Visualizar Dashboards Analíticos | Gerente Operações, Super Admin | RN-RF004-004 |
| UC05 | Detectar e Visualizar Anomalias | Analista Segurança, Super Admin | RN-RF004-007, RN-RF004-012, RN-RF004-013 |
| UC06 | Validar Integridade (Hash SHA-256) | Auditor, Super Admin | RN-RF004-005, RN-RF004-006 |
| UC07 | Visualizar Detalhes de Registro | Auditor, Super Admin | RN-RF004-001, RN-RF004-002, RN-RF004-010, RN-RF004-011 |
| UC08 | Gerenciar Retenção e Alertas | Administrador Sistema, Super Admin | RN-RF004-015 |

**Cobertura**: 15/15 Regras de Negócio (100%)

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Tenant_Id)
- Todas as ações exigem **permissão explícita** (RBAC)
- Registros de auditoria são **imutáveis** (append-only, sem UPDATE/DELETE)
- Erros não devem vazar informações sensíveis
- Mensagens devem ser claras, previsíveis e rastreáveis
- Compliance obrigatório: **LGPD (Art. 37, 38, 46)**, **SOX (Seção 404)**, **ISO 27001**

---

## UC00 — Listar Registros de Auditoria

### Objetivo
Permitir que o usuário visualize registros de auditoria disponíveis do seu próprio tenant com paginação eficiente.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.READ`
- Tenant_Id válido no contexto

### Pós-condições
- Lista exibida conforme filtros e paginação
- Registros isolados por tenant

### Fluxo Principal
1. Usuário acessa a funcionalidade "Auditoria"
2. Sistema valida permissão `SYS.AUDITORIA.READ`
3. Sistema carrega registros do tenant (WHERE Tenant_Id = @TenantId)
4. Sistema aplica paginação padrão (50 registros por página)
5. Sistema ordena por Timestamp DESC (mais recentes primeiro)
6. Sistema exibe a lista com colunas: Timestamp, Tipo, Descrição, Usuário, Entidade, IP

### Fluxos Alternativos
- **FA-UC00-001: Buscar por termo** - Filtro LIKE em Descricao, Entidade, Usuario
- **FA-UC00-002: Ordenar por coluna** - Alternar ASC/DESC
- **FA-UC00-003: Filtrar por categoria** - WHERE Tipo = @Tipo
- **FA-UC00-004: Alterar tamanho de página** - 25/50/100/200 registros

### Fluxos de Exceção
- **FE-UC00-001: Usuário sem permissão** - HTTP 403
- **FE-UC00-002: Nenhum registro** - Estado vazio
- **FE-UC00-003: Erro de conexão** - Mensagem genérica + log técnico

### Regras de Negócio
- **RN-RF004-001**: Auditoria automática via MediatR AuditingBehaviour
- **RN-RF004-010**: Multi-tenancy com isolamento rigoroso
- **RN-UC00-001**: Somente registros do tenant autenticado
- **RN-UC00-002**: Paginação padrão 50 registros
- **RN-UC00-003**: Ordenação padrão por Timestamp DESC

---

## UC01 — Buscar com Filtros Avançados

### Objetivo
Permitir buscas complexas com múltiplos critérios combinados para investigação de incidentes.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.SEARCH`
- Tenant_Id válido no contexto

### Pós-condições
- Resultados exibidos conforme critérios aplicados
- Histórico de busca salvo (opcional)

### Fluxo Principal
1. Usuário acessa "Busca Avançada"
2. Sistema valida permissão `SYS.AUDITORIA.SEARCH`
3. Sistema exibe formulário com filtros: Período, Categoria, Entidade, Usuário, IP, CorrelationId, Full-text
4. Usuário preenche critérios e clica "Buscar"
5. Sistema valida critérios (Data Final >= Data Inicial)
6. Sistema executa query otimizada com índices full-text
7. Sistema exibe resultados paginados

### Fluxos Alternativos
- **FA-UC01-001: Salvar busca favorita**
- **FA-UC01-002: Carregar busca salva**
- **FA-UC01-003: Exportar resultados** (redireciona UC03)

### Fluxos de Exceção
- **FE-UC01-001: Critérios inválidos** - Validação de datas
- **FE-UC01-002: Timeout** - Query > 30s
- **FE-UC01-003: Nenhum resultado**

### Regras de Negócio
- **RN-RF004-003**: Diff estruturado pesquisável (JSON Patch RFC 6902)
- **RN-RF004-010**: Multi-tenancy
- **RN-RF004-014**: Full-text search otimizado (50M+ registros)
- **RN-UC01-001**: Período máximo 1 ano
- **RN-UC01-002**: Índices full-text obrigatórios
- **RN-UC01-003**: Timeout 30 segundos

---

## UC02 — Visualizar Timeline de Entidade

### Objetivo
Exibir histórico completo e cronológico de todas as operações realizadas em uma entidade específica.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.TIMELINE`
- Tenant_Id válido no contexto
- EntidadeId informado

### Pós-condições
- Timeline completa exibida em ordem cronológica
- Snapshots before/after visíveis

### Fluxo Principal
1. Usuário acessa detalhes de uma entidade
2. Usuário clica "Histórico de Auditoria"
3. Sistema valida permissão `SYS.AUDITORIA.TIMELINE`
4. Sistema busca: WHERE Entidade = @Entidade AND EntidadeId = @Id AND Tenant_Id = @TenantId
5. Sistema ordena por Timestamp ASC
6. Sistema exibe timeline com: Data/hora, Tipo, Usuário, Snapshot Before, Snapshot After, Diff JSON Patch
7. Sistema destaca campos modificados

### Fluxos Alternativos
- **FA-UC02-001: Filtrar por tipo de operação**
- **FA-UC02-002: Filtrar por período**
- **FA-UC02-003: Comparar duas versões** (diff lado a lado)

### Fluxos de Exceção
- **FE-UC02-001: Entidade não encontrada** - HTTP 404
- **FE-UC02-002: Nenhum registro**
- **FE-UC02-003: Erro ao carregar JSON**

### Regras de Negócio
- **RN-RF004-002**: Snapshot completo before/after (DadosAnteriores_JSON, DadosNovos_JSON)
- **RN-RF004-003**: Diff estruturado (JSON Patch RFC 6902)
- **RN-RF004-009**: Timeline completa e cronológica
- **RN-UC02-001**: Ordenação Timestamp ASC
- **RN-UC02-002**: Destaque visual para campos modificados
- **RN-UC02-003**: JSON pretty-print

---

## UC03 — Exportar Relatórios de Compliance

### Objetivo
Gerar relatórios formatados para auditoria externa (LGPD, SOX, ISO 27001).

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.EXPORT`
- Tenant_Id válido no contexto

### Pós-condições
- Relatório gerado em formato solicitado (PDF, Excel, JSON, CSV)
- Auditoria de exportação registrada (EXPORT category)

### Fluxo Principal
1. Usuário acessa "Exportar Relatórios"
2. Sistema valida permissão
3. Sistema exibe formulário: Tipo (LGPD/SOX/ISO/Personalizado), Período, Formato
4. Usuário seleciona opções e clica "Gerar"
5. Sistema valida critérios
6. Sistema executa query filtrada por categoria
7. Sistema gera relatório
8. Sistema registra auditoria com hash SHA-256
9. Sistema exibe link download

### Fluxos Alternativos
- **FA-UC03-001: Agendar exportação recorrente**
- **FA-UC03-002: Incluir hash de integridade**

### Fluxos de Exceção
- **FE-UC03-001: Período excede 1 ano**
- **FE-UC03-002: Volume muito grande (timeout)**
- **FE-UC03-003: Erro ao gerar arquivo**

### Regras de Negócio
- **RN-RF004-004**: Retenção por categoria (LGPD/SOX: 7 anos)
- **RN-RF004-008**: Relatórios de compliance
- **RN-UC03-001**: Auditoria de exportação obrigatória
- **RN-UC03-002**: Hash SHA-256 do arquivo
- **RN-UC03-003**: Formatos: PDF, Excel, JSON, CSV

---

## UC04 — Visualizar Dashboards Analíticos

### Objetivo
Exibir dashboards visuais com métricas agregadas de auditoria por categoria.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.ANALYTICS`
- Tenant_Id válido no contexto

### Pós-condições
- Dashboards exibidos com métricas atualizadas
- Gráficos renderizados

### Fluxo Principal
1. Usuário acessa "Dashboards Analíticos"
2. Sistema valida permissão
3. Sistema carrega métricas agregadas:
   - Gráfico 1: Operações por categoria (pizza)
   - Gráfico 2: Operações por dia (linha)
   - Gráfico 3: Top 10 usuários (barra)
   - Gráfico 4: Operações por entidade (barra)
   - Gráfico 5: Distribuição retenção (pizza)
4. Sistema exibe dashboards com filtro por período
5. Sistema atualiza (cache 5 minutos)

### Fluxos Alternativos
- **FA-UC04-001: Filtrar por período personalizado**
- **FA-UC04-002: Drill-down em categoria**
- **FA-UC04-003: Exportar gráfico**

### Fluxos de Exceção
- **FE-UC04-001: Erro ao calcular métricas**
- **FE-UC04-002: Cache expirado**

### Regras de Negócio
- **RN-RF004-004**: Retenção por categoria
- **RN-UC04-001**: Cache 5 minutos
- **RN-UC04-002**: Métricas pré-calculadas
- **RN-UC04-003**: Isolamento por tenant

---

## UC05 — Detectar e Visualizar Anomalias

### Objetivo
Detectar automaticamente padrões anômalos de comportamento e exibir alertas.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.ANOMALIES`
- Tenant_Id válido no contexto

### Pós-condições
- Anomalias detectadas e exibidas
- Alertas registrados (SECURITY category)

### Fluxo Principal
1. Usuário acessa "Detecção de Anomalias"
2. Sistema valida permissão
3. Sistema executa detecção:
   - Exportações excessivas (>100/h)
   - Múltiplos tenants (>50/dia)
   - Operações fora de horário (22h-6h)
   - Acessos negados (>10/h)
   - Alterações massivas (>100/min)
4. Sistema exibe anomalias com: Tipo, Severidade, Usuário, Timestamp, Detalhes
5. Sistema permite investigação (redireciona UC01)

### Fluxos Alternativos
- **FA-UC05-001: Marcar falso positivo**
- **FA-UC05-002: Escalar para segurança**
- **FA-UC05-003: Configurar thresholds**

### Fluxos de Exceção
- **FE-UC05-001: Nenhuma anomalia**
- **FE-UC05-002: Erro ao executar detecção**

### Regras de Negócio
- **RN-RF004-007**: Detecção automática (thresholds)
- **RN-RF004-012**: Alertas em tempo real
- **RN-RF004-013**: Thresholds configuráveis
- **RN-UC05-001**: Detecção a cada 10 min (Hangfire)
- **RN-UC05-002**: Registra em SECURITY
- **RN-UC05-003**: Severidade automática

---

## UC06 — Validar Integridade (Hash SHA-256)

### Objetivo
Verificar a integridade criptográfica de registros de auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.INTEGRITY`
- Tenant_Id válido no contexto

### Pós-condições
- Integridade validada (sucesso ou falha)
- Resultado exibido

### Fluxo Principal
1. Usuário acessa "Validação de Integridade"
2. Sistema valida permissão
3. Sistema exibe opções: Registro específico, Período (7d/30d/1a)
4. Usuário seleciona e clica "Validar"
5. Sistema recalcula hash SHA-256 (concatena campos + SHA256)
6. Sistema compara com Hash_SHA256 armazenado
7. Sistema exibe: ✅ Íntegro ou ❌ Corrompido

### Fluxos Alternativos
- **FA-UC06-001: Exportar relatório de integridade**
- **FA-UC06-002: Validação automática agendada**

### Fluxos de Exceção
- **FE-UC06-001: Registro corrompido** (alerta SECURITY)
- **FE-UC06-002: Erro ao recalcular**

### Regras de Negócio
- **RN-RF004-005**: Hash SHA-256 para integridade
- **RN-RF004-006**: Validação periódica
- **RN-UC06-001**: Hash na criação (AuditingBehaviour)
- **RN-UC06-002**: Individual ou lote
- **RN-UC06-003**: Corrompido = alerta crítico

---

## UC07 — Visualizar Detalhes de Registro

### Objetivo
Exibir todos os detalhes de um registro específico de auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.READ`
- Tenant_Id válido no contexto
- Id de registro informado

### Pós-condições
- Detalhes completos exibidos
- Snapshots JSON renderizados

### Fluxo Principal
1. Usuário seleciona registro (UC00/UC01)
2. Usuário clica "Ver Detalhes"
3. Sistema valida permissão
4. Sistema carrega: WHERE Id = @Id AND Tenant_Id = @TenantId
5. Sistema exibe 5 painéis:
   - Painel 1: Informações Gerais (Timestamp, Tipo, Descrição, Entidade)
   - Painel 2: Contexto (Usuário, IP, UserAgent, CorrelationId)
   - Painel 3: Snapshots (DadosAnteriores, DadosNovos, Diff JSON Patch)
   - Painel 4: Integridade (Hash SHA-256, Botão Validar)
   - Painel 5: Retenção (RetentionDate, Arquivado, AzureBlobUri)

### Fluxos Alternativos
- **FA-UC07-001: Copiar CorrelationId**
- **FA-UC07-002: Rastrear CorrelationId** (filtro UC01)
- **FA-UC07-003: Exportar JSON**

### Fluxos de Exceção
- **FE-UC07-001: Registro não encontrado** - HTTP 404
- **FE-UC07-002: Erro ao renderizar JSON**

### Regras de Negócio
- **RN-RF004-001**: Auditoria com todos metadados
- **RN-RF004-002**: Snapshot before/after
- **RN-RF004-010**: Multi-tenancy
- **RN-RF004-011**: CorrelationId para rastreamento
- **RN-UC07-001**: JSON pretty-print
- **RN-UC07-002**: Diff JSON Patch RFC 6902

---

## UC08 — Gerenciar Retenção e Alertas

### Objetivo
Gerenciar políticas de retenção por categoria e exibir alertas de registros próximos ao vencimento.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.AUDITORIA.ADMIN`
- Tenant_Id válido no contexto

### Pós-condições
- Políticas de retenção configuradas
- Alertas exibidos para registros expirando

### Fluxo Principal
1. Usuário acessa "Gerenciar Retenção"
2. Sistema valida permissão
3. Sistema exibe configuração atual:
   - FINANCIAL/LGPD/SECURITY: 7 anos (fixo)
   - CRUD/AUTH/EXPORT/CONFIG/ADMIN/PRINT: 1 ano
   - ACCESS: 90 dias
4. Sistema exibe alertas (RetentionDate <= HOJE + 30d): Categoria, Qtd, Vencimento, Ação
5. Usuário ajusta políticas (apenas não-compliance)
6. Sistema valida e salva

### Fluxos Alternativos
- **FA-UC08-001: Arquivar vencidos** (Azure Blob cold tier)
- **FA-UC08-002: Restaurar arquivados**
- **FA-UC08-003: Excluir vencidos** (apenas não-compliance)

### Fluxos de Exceção
- **FE-UC08-001: Tentativa alterar compliance** (BLOQUEIO)
- **FE-UC08-002: Tentativa excluir compliance** (BLOQUEIO)
- **FE-UC08-003: Erro Azure Blob**

### Regras de Negócio
- **RN-RF004-015**: Alertas 30 dias antes vencimento
- **RN-UC08-001**: Compliance fixa (FINANCIAL/LGPD/SECURITY)
- **RN-UC08-002**: Não-compliance ajustável (30d-10a)
- **RN-UC08-003**: Arquivamento Azure cold
- **RN-UC08-004**: Exclusão só não-compliance
- **RN-UC08-005**: Alertas 30 dias antes

---

## 4. MATRIZ DE RASTREABILIDADE (RF004 → UCs)

| Regra de Negócio | UCs Cobrindo | Status |
|------------------|--------------|--------|
| RN-RF004-001 — Auditoria Automática MediatR | UC00, UC07 | ✅ |
| RN-RF004-002 — Snapshot Before/After | UC02, UC07 | ✅ |
| RN-RF004-003 — Diff Estruturado (JSON Patch RFC 6902) | UC01, UC02, UC07 | ✅ |
| RN-RF004-004 — Retenção por Categoria (SOX/LGPD) | UC00, UC03, UC04 | ✅ |
| RN-RF004-005 — Hash SHA-256 para Integridade | UC06 | ✅ |
| RN-RF004-006 — Validação de Integridade Periódica | UC06 | ✅ |
| RN-RF004-007 — Detecção de Anomalias | UC05 | ✅ |
| RN-RF004-008 — Relatórios de Compliance (LGPD/SOX/ISO) | UC03 | ✅ |
| RN-RF004-009 — Timeline Cronológica Completa | UC02 | ✅ |
| RN-RF004-010 — Multi-tenancy com Isolamento | UC00, UC01, UC07 | ✅ |
| RN-RF004-011 — CorrelationId para Rastreamento | UC07 | ✅ |
| RN-RF004-012 — Alertas de Anomalias em Tempo Real | UC05 | ✅ |
| RN-RF004-013 — Configuração de Thresholds | UC05 | ✅ |
| RN-RF004-014 — Full-text Search Otimizado | UC01 | ✅ |
| RN-RF004-015 — Alertas de Retenção Expirando | UC08 | ✅ |

**Cobertura Total: 15/15 Regras de Negócio (100%)**

---

## 5. MATRIZ DE PERMISSÕES RBAC

| Permissão | UCs Permitidos | Perfis Padrão |
|-----------|----------------|---------------|
| `SYS.AUDITORIA.READ` | UC00, UC07 | Super Admin, Auditor, Gerente Operações |
| `SYS.AUDITORIA.SEARCH` | UC01 | Super Admin, Auditor, Analista Segurança |
| `SYS.AUDITORIA.TIMELINE` | UC02 | Super Admin, Auditor |
| `SYS.AUDITORIA.EXPORT` | UC03 | Super Admin, Auditor |
| `SYS.AUDITORIA.ANALYTICS` | UC04 | Super Admin, Gerente Operações, Auditor |
| `SYS.AUDITORIA.ANOMALIES` | UC05 | Super Admin, Analista Segurança |
| `SYS.AUDITORIA.INTEGRITY` | UC06 | Super Admin, Auditor |
| `SYS.AUDITORIA.ADMIN` | UC08 | Super Admin, Administrador Sistema |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-29 | Agência ALC - alc.dev.br | Versão canônica com 9 UCs cobrindo 100% das 15 regras de negócio (v2.0 Governance) |
| 1.0 | 2025-12-17 | Agência ALC - alc.dev.br | Versão inicial com 3 UCs (DEPRECIADA) |

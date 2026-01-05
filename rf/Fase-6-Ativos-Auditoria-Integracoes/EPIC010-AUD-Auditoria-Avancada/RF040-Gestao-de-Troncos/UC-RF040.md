# UC-RF040 — Casos de Uso Canônicos

**RF:** RF040 — Gestão de Troncos Telefônicos
**Epic:** EPIC010-AUD - Auditoria Avançada
**Fase:** Fase 6 - Ativos, Auditoria e Integrações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF040 - Gestão de Troncos Telefônicos**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF040.yaml)
- Massas de Teste (MT-RF040.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Troncos | Usuário Autenticado |
| UC01 | Criar Configuração de Tronco | Usuário Autenticado |
| UC02 | Visualizar Dashboard de Monitoramento | Usuário Autenticado |
| UC03 | Executar Failover Manual | Usuário Autenticado |
| UC04 | Gerar Relatório de Disponibilidade | Usuário Autenticado |
| UC05 | Configurar Alertas de QoS | Usuário Autenticado |
| UC06 | Simular Migração SIP vs E1 | Usuário Autenticado |
| UC07 | Analisar TCO por Tecnologia | Usuário Autenticado |
| UC08 | Visualizar Métricas de QoS Históricas | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Conglomerado)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Integração com i18n obrigatória para todos os textos
- Métricas de QoS coletadas a cada 30 segundos
- Failover automático em menos de 5 segundos
- Dashboard atualiza em tempo real via SignalR

---

## UC00 — Listar Troncos

### Objetivo
Permitir que o usuário visualize todos os troncos telefônicos do seu tenant com status, capacidade e utilização em tempo real.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.VISUALIZAR`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Status de cada tronco atualizado (disponivel, ocupado, indisponivel, congestionado, manutencao, inativo)

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Troncos"
- **FP-UC00-002:** Sistema valida permissão `GES.TRONCOS.VISUALIZAR`
- **FP-UC00-003:** Sistema carrega troncos do tenant (Id_Conglomerado)
- **FP-UC00-004:** Sistema exibe listagem com: Identificação, Tipo (SIP/E1/Analógico), Operadora, Capacidade (canais), Utilização (%), Status, Localização (Filial)
- **FP-UC00-005:** Sistema aplica paginação padrão (20 registros por página)
- **FP-UC00-006:** Sistema exibe indicador visual de utilização (verde <70%, amarelo 70-90%, vermelho >90%)

### Fluxos Alternativos
- **FA-UC00-001:** Usuário busca por identificação ou operadora
  - Sistema filtra registros correspondentes
- **FA-UC00-002:** Usuário ordena por coluna (Identificação, Utilização, Status)
  - Sistema reordena lista conforme critério selecionado
- **FA-UC00-003:** Usuário filtra por status (disponivel, indisponivel, congestionado)
  - Sistema exibe apenas registros com status selecionado
- **FA-UC00-004:** Usuário filtra por tipo de tronco (SIP, E1, Analógico)
  - Sistema exibe apenas registros do tipo selecionado
- **FA-UC00-005:** Usuário filtra por localização (Filial)
  - Sistema exibe apenas registros da localização selecionada

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão `GES.TRONCOS.VISUALIZAR`
  - Sistema exibe mensagem de acesso negado (HTTP 403)
- **FE-UC00-002:** Nenhum tronco cadastrado
  - Sistema exibe estado vazio com botão "Criar Tronco"
- **FE-UC00-003:** Erro ao carregar dados
  - Sistema exibe mensagem de erro genérica e registra log de auditoria

### Regras de Negócio
- **RN-UC-00-001:** Somente troncos do tenant do usuário autenticado são exibidos
- **RN-UC-00-002:** Troncos excluídos logicamente (soft delete) não aparecem na listagem
- **RN-UC-00-003:** Paginação padrão de 20 registros, máximo 100 por página
- **RN-UC-00-004:** Indicador visual de utilização: verde (<70%), amarelo (70-90%), vermelho (>90%)
- **RN-UC-00-005:** Status atualizado em tempo real via SignalR (polling 30 segundos)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas troncos do tenant do usuário autenticado
- **CA-UC00-002:** Troncos excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL
- **CA-UC00-006:** Indicador visual de utilização DEVE seguir cores: verde, amarelo, vermelho
- **CA-UC00-007:** Status DEVE atualizar automaticamente a cada 30 segundos

---

## UC01 — Criar Configuração de Tronco

### Objetivo
Permitir a criação de um novo tronco telefônico com todas as configurações técnicas necessárias para monitoramento e operação.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.CONFIGURAR`

### Pós-condições
- Tronco criado e persistido no banco de dados
- Monitoramento automático iniciado (polling 30 segundos)
- Auditoria registrada
- Integração com PABX atualizada (se configurado)

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Tronco"
- **FP-UC01-002:** Sistema valida permissão `GES.TRONCOS.CONFIGURAR`
- **FP-UC01-003:** Sistema exibe formulário com campos:
  - Identificação* (varchar 100, único por tenant)
  - Tipo* (enum: SIP, E1, Analógico)
  - Operadora* (varchar 100)
  - Capacidade_Canais* (int, padrão E1=30, SIP=configurável)
  - DDR_Inicial (varchar 20, opcional)
  - DDR_Final (varchar 20, opcional)
  - Localização* (FK para Filial)
  - Contrato (FK para Contratos, opcional)
  - Valor_Mensal (decimal, opcional)
  - Dt_Ativacao* (date, padrão hoje)
  - Endpoint_API (varchar 255, para integração PABX)
  - Credenciais_API (texto criptografado)
  - Configuracao_SNMP (JSON, opcional)
  - Tronco_Backup (FK para Tronco, opcional para failover)
- **FP-UC01-004:** Usuário preenche campos obrigatórios
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados (RN-UC-01-001 a RN-UC-01-007)
- **FP-UC01-007:** Sistema cria registro com:
  - Id_Conglomerado (automático, tenant do usuário)
  - CriadoPor (automático, usuário autenticado)
  - DataCriacao (automático, timestamp UTC)
  - Status (automático, "disponivel")
- **FP-UC01-008:** Sistema inicia monitoramento automático (Hangfire job polling 30s)
- **FP-UC01-009:** Sistema registra auditoria (CREATE)
- **FP-UC01-010:** Sistema atualiza integração com PABX (se configurado)
- **FP-UC01-011:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Usuário clica em "Salvar e Criar Outro"
  - Sistema salva registro e mantém formulário aberto
- **FA-UC01-002:** Usuário clica em "Cancelar"
  - Sistema descarta dados e retorna para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação (campo obrigatório vazio)
  - Sistema exibe mensagem de erro específica ao lado do campo
- **FE-UC01-002:** Identificação duplicada no tenant
  - Sistema exibe mensagem "Já existe um tronco com esta identificação"
- **FE-UC01-003:** Erro ao validar credenciais PABX
  - Sistema exibe mensagem "Credenciais de integração inválidas. Verifique endpoint e API Key"
- **FE-UC01-004:** Tronco backup não está disponível
  - Sistema exibe mensagem "Tronco backup deve estar com status 'disponivel'"
- **FE-UC01-005:** DDR_Final menor que DDR_Inicial
  - Sistema exibe mensagem "DDR Final deve ser maior ou igual a DDR Inicial"
- **FE-UC01-006:** Erro inesperado ao salvar
  - Sistema exibe mensagem genérica e registra log detalhado

### Regras de Negócio
- **RN-UC-01-001:** Campos obrigatórios: Identificação, Tipo, Operadora, Capacidade_Canais, Localização, Dt_Ativacao
- **RN-UC-01-002:** Identificação deve ser única por tenant (Id_Conglomerado)
- **RN-UC-01-003:** Id_Conglomerado preenchido automaticamente com tenant do usuário
- **RN-UC-01-004:** CriadoPor preenchido automaticamente com ID do usuário autenticado
- **RN-UC-01-005:** DataCriacao preenchida automaticamente com timestamp UTC
- **RN-UC-01-006:** Status inicial sempre "disponivel"
- **RN-UC-01-007:** Capacidade padrão E1 = 30 canais, SIP = configurável
- **RN-UC-01-008:** DDR_Inicial e DDR_Final validam faixa de números (DDR_Final >= DDR_Inicial)
- **RN-UC-01-009:** Tronco_Backup (se informado) deve estar com status "disponivel"
- **RN-UC-01-010:** Credenciais_API armazenadas criptografadas (AES-256)
- **RN-UC-01-011:** Monitoramento automático inicia imediatamente após criação

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Conglomerado DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** CriadoPor DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** DataCriacao DEVE ser preenchida automaticamente com timestamp UTC atual
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-007:** Identificação DEVE ser única dentro do tenant
- **CA-UC01-008:** Credenciais PABX DEVEM ser armazenadas criptografadas
- **CA-UC01-009:** Monitoramento DEVE iniciar automaticamente em até 30 segundos após criação
- **CA-UC01-010:** Integração PABX DEVE ser testada antes de salvar (validação de credenciais)

---

## UC02 — Visualizar Dashboard de Monitoramento

### Objetivo
Exibir dashboard em tempo real com status de todos os troncos, métricas de QoS, utilização, falhas e alertas ativos.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.DASHBOARD`

### Pós-condições
- Dashboard exibido com atualização em tempo real (SignalR)
- Métricas de QoS atualizadas a cada 30 segundos
- Alertas ativos destacados visualmente

### Fluxo Principal
- **FP-UC02-001:** Usuário acessa "Dashboard de Monitoramento"
- **FP-UC02-002:** Sistema valida permissão `GES.TRONCOS.DASHBOARD`
- **FP-UC02-003:** Sistema carrega dados do tenant
- **FP-UC02-004:** Sistema exibe dashboard com:
  - **Resumo Geral:** Total de troncos, Disponíveis, Indisponíveis, Congestionados, Utilização média (%)
  - **Status por Tronco:** Lista com Identificação, Tipo, Status, Utilização (%), MOS Score, Última verificação
  - **Gráfico de Utilização:** Evolução da utilização nas últimas 6 horas
  - **Métricas de QoS:** Jitter médio, Latência média, Packet Loss médio, MOS Score médio
  - **Alertas Ativos:** Troncos com problemas (indisponível, congestionado, QoS degradado)
  - **Histórico de Failovers:** Últimos 10 eventos de failover
- **FP-UC02-005:** Sistema estabelece conexão SignalR para atualização em tempo real
- **FP-UC02-006:** Sistema atualiza dashboard a cada 30 segundos automaticamente

### Fluxos Alternativos
- **FA-UC02-001:** Usuário seleciona período do gráfico (6h, 24h, 7d, 30d)
  - Sistema atualiza gráfico com agregação apropriada
- **FA-UC02-002:** Usuário clica em tronco específico
  - Sistema exibe drill-down com detalhes do tronco e histórico completo
- **FA-UC02-003:** Usuário exporta dashboard (PNG, PDF)
  - Sistema gera arquivo com snapshot do dashboard atual

### Fluxos de Exceção
- **FE-UC02-001:** Usuário sem permissão `GES.TRONCOS.DASHBOARD`
  - Sistema exibe mensagem de acesso negado (HTTP 403)
- **FE-UC02-002:** Nenhum tronco cadastrado
  - Sistema exibe estado vazio com orientação para criar troncos
- **FE-UC02-003:** Erro ao conectar SignalR
  - Sistema exibe alerta e tenta reconectar automaticamente

### Regras de Negócio
- **RN-UC-02-001:** Somente dados do tenant do usuário autenticado
- **RN-UC-02-002:** Atualização em tempo real via SignalR (30 segundos)
- **RN-UC-02-003:** Histórico armazenado por 90 dias
- **RN-UC-02-004:** Gráficos otimizados com agregação para períodos >7 dias
- **RN-UC-02-005:** Indicadores visuais de qualidade (verde: excelente MOS >4.0, amarelo: aceitável MOS 3.0-4.0, vermelho: ruim MOS <3.0)
- **RN-UC-02-006:** Alertas visuais quando métricas excedem limites (utilização >90%, MOS <3.0, latência >300ms)

### Critérios de Aceite
- **CA-UC02-001:** Dashboard DEVE atualizar automaticamente a cada 30 segundos
- **CA-UC02-002:** Histórico DEVE ser mantido por 90 dias
- **CA-UC02-003:** Gráficos DEVEM ser otimizados (agregação) para períodos longos
- **CA-UC02-004:** Indicadores visuais DEVEM seguir padrão de cores (verde/amarelo/vermelho)
- **CA-UC02-005:** Drill-down DEVE exibir detalhes completos do tronco selecionado
- **CA-UC02-006:** Exportação DEVE gerar arquivo em até 5 segundos

---

## UC03 — Executar Failover Manual

### Objetivo
Permitir que administrador execute failover manual de um tronco com falha para um tronco backup.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.FAILOVER_MANUAL`
- Tronco origem com status "indisponivel" ou "congestionado"
- Tronco backup disponível

### Pós-condições
- Roteamento de chamadas transferido para tronco backup
- PABX atualizado com novo roteamento
- Evento de failover registrado
- Notificações enviadas (SMS, e-mail, push)
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa "Monitoramento de Troncos"
- **FP-UC03-002:** Sistema exibe lista de troncos com problemas
- **FP-UC03-003:** Usuário seleciona tronco com falha
- **FP-UC03-004:** Usuário clica em "Executar Failover Manual"
- **FP-UC03-005:** Sistema valida permissão `GES.TRONCOS.FAILOVER_MANUAL`
- **FP-UC03-006:** Sistema exibe modal de confirmação com:
  - Tronco origem (atual)
  - Tronco backup (destino)
  - Tempo estimado de failover (<5 segundos)
  - Chamadas ativas que serão afetadas
- **FP-UC03-007:** Usuário confirma failover
- **FP-UC03-008:** Sistema executa failover:
  - Atualiza roteamento no PABX via API
  - Marca tronco origem como "indisponivel"
  - Marca tronco backup como "ocupado"
  - Registra evento EventoFailover (timestamp, duração, motivo)
- **FP-UC03-009:** Sistema envia notificações (SMS, e-mail, push, chamada)
- **FP-UC03-010:** Sistema registra auditoria (FAILOVER_MANUAL)
- **FP-UC03-011:** Sistema exibe mensagem de sucesso com tempo de execução

### Fluxos Alternativos
- **FA-UC03-001:** Usuário cancela failover
  - Sistema fecha modal e retorna para monitoramento

### Fluxos de Exceção
- **FE-UC03-001:** Usuário sem permissão `GES.TRONCOS.FAILOVER_MANUAL`
  - Sistema exibe mensagem de acesso negado (HTTP 403)
- **FE-UC03-002:** Tronco backup não configurado
  - Sistema exibe mensagem "Tronco backup não configurado. Configure um tronco backup antes de executar failover"
- **FE-UC03-003:** Tronco backup também está indisponível
  - Sistema exibe mensagem "Tronco backup também está indisponível. Verifique a configuração"
- **FE-UC03-004:** Erro ao atualizar PABX
  - Sistema tenta retry (3 tentativas)
  - Se falhar, exibe mensagem "Erro ao atualizar PABX. Verifique conectividade" e registra log
- **FE-UC03-005:** Failover excede 5 segundos
  - Sistema exibe alerta "Failover demorou mais que o esperado"

### Regras de Negócio
- **RN-UC-03-001:** Failover só pode ser executado se tronco backup estiver "disponivel"
- **RN-UC-03-002:** Tempo total de failover deve ser inferior a 5 segundos
- **RN-UC-03-003:** Notificações enviadas simultaneamente (SMS, e-mail, push, chamada)
- **RN-UC-03-004:** Roteamento atualizado no PABX via API
- **RN-UC-03-005:** Retorno gradual ao tronco primário após recuperação (10% a cada minuto durante 10 minutos)
- **RN-UC-03-006:** Aguardar 5 minutos de estabilidade antes de iniciar retorno gradual
- **RN-UC-03-007:** EventoFailover registra: timestamp, tronco origem, tronco destino, motivo, duração, usuário responsável

### Critérios de Aceite
- **CA-UC03-001:** Failover DEVE ser concluído em menos de 5 segundos
- **CA-UC03-002:** Sistema DEVE validar disponibilidade do tronco backup ANTES de executar
- **CA-UC03-003:** Notificações DEVEM ser enviadas para todos os canais configurados
- **CA-UC03-004:** Roteamento DEVE ser atualizado no PABX imediatamente
- **CA-UC03-005:** EventoFailover DEVE registrar todos os dados relevantes
- **CA-UC03-006:** Auditoria DEVE registrar usuário que executou failover manual

---

## UC04 — Gerar Relatório de Disponibilidade

### Objetivo
Gerar relatório mensal com percentual de disponibilidade de cada tronco, comparação com SLA contratado (99,9%) e cálculo de créditos.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.RELATORIOS`
- Mínimo 1 mês completo de dados históricos

### Pós-condições
- Relatório gerado em PDF e Excel
- Créditos aplicados automaticamente se downtime exceder SLA
- Relatório enviado por e-mail (opcional)

### Fluxo Principal
- **FP-UC04-001:** Usuário acessa "Relatórios de Troncos"
- **FP-UC04-002:** Sistema valida permissão `GES.TRONCOS.RELATORIOS`
- **FP-UC04-003:** Sistema exibe formulário com:
  - Período (mês/ano)
  - Troncos (todos ou selecionados)
  - Formato (PDF, Excel)
  - Enviar por e-mail (sim/não)
- **FP-UC04-004:** Usuário seleciona período e formato
- **FP-UC04-005:** Usuário clica em "Gerar Relatório"
- **FP-UC04-006:** Sistema valida se período tem mínimo 30 dias completos de dados
- **FP-UC04-007:** Sistema calcula para cada tronco:
  - Total de minutos no período
  - Minutos disponíveis (status "disponivel" ou "ocupado")
  - Minutos indisponíveis (status "indisponivel")
  - % Uptime = (Minutos Disponíveis / Total Minutos) × 100
  - SLA contratado (99,9% = 43 min downtime máximo/mês)
  - Diferença real vs SLA
  - Crédito aplicável (se downtime > SLA)
- **FP-UC04-008:** Sistema gera relatório com:
  - Resumo executivo (total troncos, média uptime, total créditos)
  - Detalhamento por tronco (tabela com todas as métricas)
  - Gráfico de evolução de disponibilidade (últimos 12 meses)
  - Eventos de falha (detalhamento de indisponibilidades >5 min)
- **FP-UC04-009:** Sistema calcula créditos automaticamente (10-25% da mensalidade conforme gravidade)
- **FP-UC04-010:** Sistema gera arquivo PDF/Excel
- **FP-UC04-011:** Sistema envia por e-mail (se solicitado)
- **FP-UC04-012:** Sistema exibe link para download

### Fluxos Alternativos
- **FA-UC04-001:** Usuário seleciona "Enviar por e-mail"
  - Sistema envia relatório para e-mail do usuário autenticado
- **FA-UC04-002:** Usuário agenda envio recorrente (todo dia 5 de cada mês)
  - Sistema cria job agendado no Hangfire

### Fluxos de Exceção
- **FE-UC04-001:** Período selecionado tem menos de 30 dias de dados
  - Sistema exibe mensagem "Relatório requer mínimo 30 dias completos de dados"
- **FE-UC04-002:** Erro ao gerar PDF/Excel
  - Sistema exibe mensagem de erro e registra log
- **FE-UC04-003:** Erro ao enviar e-mail
  - Sistema exibe mensagem "Relatório gerado, mas não foi possível enviar e-mail. Baixe manualmente"

### Regras de Negócio
- **RN-UC-04-001:** Cálculo: Uptime % = (Total Minutos - Minutos Indisponíveis) / Total Minutos × 100
- **RN-UC-04-002:** SLA típico: 99,9% (permite 43 minutos de downtime por mês)
- **RN-UC-04-003:** Downtime programado (manutenção) pode ser excluído do cálculo se notificação prévia >48h
- **RN-UC-04-004:** Crédito aplicado automaticamente se downtime exceder SLA (10-25% da mensalidade conforme gravidade)
- **RN-UC-04-005:** Relatório enviado automaticamente no dia 5 de cada mês (job agendado)
- **RN-UC-04-006:** Falhas com duração <5 minutos não são contabilizadas (consideradas "blips")

### Critérios de Aceite
- **CA-UC04-001:** Relatório DEVE calcular uptime % com precisão de 2 casas decimais
- **CA-UC04-002:** SLA padrão DEVE ser 99,9% (43 min downtime máximo/mês)
- **CA-UC04-003:** Downtime programado DEVE ser excluído se notificação prévia >48h
- **CA-UC04-004:** Crédito DEVE ser calculado automaticamente conforme tabela de gravidade
- **CA-UC04-005:** Relatório DEVE ser gerado em até 30 segundos
- **CA-UC04-006:** Job agendado DEVE executar no dia 5 de cada mês às 08:00

---

## UC05 — Configurar Alertas de QoS

### Objetivo
Permitir que usuário configure alertas personalizados para métricas de QoS (jitter, latência, packet loss, MOS score).

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.CONFIGURAR`

### Pós-condições
- Alertas configurados e persistidos
- Monitoramento ativado
- Notificações serão enviadas quando limites forem excedidos

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa "Configurar Alertas de QoS"
- **FP-UC05-002:** Sistema valida permissão `GES.TRONCOS.CONFIGURAR`
- **FP-UC05-003:** Sistema exibe formulário com:
  - Tronco (seleção múltipla ou "Todos")
  - Métrica (Jitter, Latência, Packet Loss, MOS Score)
  - Condição (>, <, =, >=, <=)
  - Valor de referência
  - Duração mínima (medições consecutivas)
  - Canais de notificação (SMS, e-mail, push, chamada)
  - Destinatários (usuários ou grupos)
  - Limitar frequência (máximo 1 alerta por hora)
- **FP-UC05-004:** Usuário configura alerta
- **FP-UC05-005:** Usuário clica em "Salvar Alerta"
- **FP-UC05-006:** Sistema valida dados
- **FP-UC05-007:** Sistema cria registro de ConfiguracaoAlerta
- **FP-UC05-008:** Sistema ativa monitoramento contínuo
- **FP-UC05-009:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC05-001:** Usuário edita alerta existente
  - Sistema carrega dados do alerta e permite alteração
- **FA-UC05-002:** Usuário desativa alerta temporariamente
  - Sistema marca alerta como "inativo" sem excluir
- **FA-UC05-003:** Usuário duplica alerta para outro tronco
  - Sistema copia configuração e permite ajustes

### Fluxos de Exceção
- **FE-UC05-001:** Valor de referência inválido (ex: Jitter <0)
  - Sistema exibe mensagem "Valor de referência deve ser positivo"
- **FE-UC05-002:** Duração mínima <1
  - Sistema exibe mensagem "Duração mínima deve ser de pelo menos 1 medição (30 segundos)"
- **FE-UC05-003:** Nenhum canal de notificação selecionado
  - Sistema exibe mensagem "Selecione pelo menos um canal de notificação"

### Regras de Negócio
- **RN-UC-05-001:** Alertas validam métricas a cada 30 segundos (junto com polling)
- **RN-UC-05-002:** Alerta só dispara após duração mínima de medições consecutivas
- **RN-UC-05-003:** Máximo 1 alerta por hora por tronco (evitar spam)
- **RN-UC-05-004:** Notificações enviadas para todos os canais selecionados
- **RN-UC-05-005:** Limites recomendados:
  - Jitter: ideal <30ms, aceitável <50ms
  - Latência: ideal <150ms, aceitável <300ms
  - Packet Loss: ideal <1%, aceitável <3%
  - MOS Score: excelente >4.0, bom 3.0-4.0, regular 2.0-3.0, ruim <2.0

### Critérios de Aceite
- **CA-UC05-001:** Alerta DEVE disparar apenas após duração mínima de medições consecutivas
- **CA-UC05-002:** Sistema DEVE limitar frequência de alertas (máximo 1 por hora por tronco)
- **CA-UC05-003:** Notificações DEVEM ser enviadas para todos os canais selecionados
- **CA-UC05-004:** Alerta DEVE validar métricas a cada 30 segundos
- **CA-UC05-005:** Sistema DEVE permitir desativar alerta temporariamente sem excluir

---

## UC06 — Simular Migração SIP vs E1

### Objetivo
Calcular ROI e break-even point de migração de troncos E1 para SIP com base no uso real dos últimos 6 meses.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.RELATORIOS`
- Mínimo 6 meses de histórico de uso
- Custos de operadoras atualizados (<90 dias)

### Pós-condições
- Simulação gerada com análise financeira completa
- Relatório exportado (PDF, Excel)
- Recomendação estratégica fornecida

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa "Simulador de Economia"
- **FP-UC06-002:** Sistema valida permissão `GES.TRONCOS.RELATORIOS`
- **FP-UC06-003:** Sistema valida pré-requisitos (mínimo 6 meses de histórico)
- **FP-UC06-004:** Sistema exibe formulário com:
  - Troncos E1 atuais (seleção múltipla)
  - Operadora SIP (seleção ou customizar custos)
  - Investimento inicial (gateway, instalação)
  - Período de análise (12, 24, 36 meses)
- **FP-UC06-005:** Usuário configura simulação
- **FP-UC06-006:** Usuário clica em "Simular"
- **FP-UC06-007:** Sistema calcula com base nos últimos 6 meses:
  - Custo atual E1: fixo mensal + variável por minuto
  - Custo projetado SIP: fixo mensal + variável por minuto
  - Investimento inicial: gateway VoIP + instalação
  - Economia mensal: (Custo E1 - Custo SIP)
  - Break-even point: Investimento Inicial / Economia Mensal
  - ROI em 12, 24, 36 meses
- **FP-UC06-008:** Sistema gera relatório com:
  - Resumo executivo (economia total, break-even, ROI)
  - Comparativo detalhado (tabela lado a lado E1 vs SIP)
  - Gráfico de evolução de custos (12, 24, 36 meses)
  - Análise de risco (dependência de internet, QoS)
  - Recomendação (migrar ou manter)
- **FP-UC06-009:** Sistema exibe simulação
- **FP-UC06-010:** Sistema permite exportar (PDF, Excel)

### Fluxos Alternativos
- **FA-UC06-001:** Usuário ajusta custos manualmente (cenário pessimista/otimista)
  - Sistema recalcula simulação com novos valores
- **FA-UC06-002:** Usuário compara 3 operadoras SIP simultaneamente
  - Sistema gera comparativo side-by-side

### Fluxos de Exceção
- **FE-UC06-001:** Histórico insuficiente (<6 meses)
  - Sistema exibe mensagem "Simulação requer mínimo 6 meses de histórico de uso"
- **FE-UC06-002:** Custos de operadoras desatualizados (>90 dias)
  - Sistema exibe alerta "Custos de operadoras desatualizados. Simulação pode ser imprecisa"
- **FE-UC06-003:** Economia projetada negativa (SIP mais caro que E1)
  - Sistema exibe recomendação "Não recomendado: Migração resultaria em aumento de custos"

### Regras de Negócio
- **RN-UC-06-001:** Simulação requer mínimo 6 meses de histórico de uso
- **RN-UC-06-002:** Custos de operadoras devem estar atualizados (<90 dias)
- **RN-UC-06-003:** Cálculo de break-even point (meses para ROI positivo)
- **RN-UC-06-004:** Recomendação só se ROI <12 meses
- **RN-UC-06-005:** Projeção de economia em 12, 24, 36 meses
- **RN-UC-06-006:** Considerar custos: fixos (assinatura), variáveis (minutos), investimento inicial (gateway, instalação)

### Critérios de Aceite
- **CA-UC06-001:** Simulação DEVE exigir mínimo 6 meses de histórico
- **CA-UC06-002:** Break-even point DEVE ser calculado com precisão
- **CA-UC06-003:** ROI DEVE ser projetado para 12, 24 e 36 meses
- **CA-UC06-004:** Recomendação DEVE ser baseada em ROI <12 meses
- **CA-UC06-005:** Sistema DEVE alertar se custos desatualizados (>90 dias)
- **CA-UC06-006:** Relatório DEVE incluir análise de risco (dependência internet, QoS)

---

## UC07 — Analisar TCO por Tecnologia

### Objetivo
Comparar custos totais (TCO - Total Cost of Ownership) de troncos E1, SIP e analógicos ao longo de 3 anos.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.RELATORIOS`

### Pós-condições
- Análise comparativa gerada
- Recomendação estratégica fornecida
- Relatório exportado (PDF, Excel)

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa "Análise de TCO por Tecnologia"
- **FP-UC07-002:** Sistema valida permissão `GES.TRONCOS.RELATORIOS`
- **FP-UC07-003:** Sistema exibe formulário com:
  - Período de análise (1, 3, 5 anos)
  - Considerar inflação (sim/não, IPCA padrão)
  - Tecnologias (E1, SIP, Analógico)
- **FP-UC07-004:** Usuário seleciona período e tecnologias
- **FP-UC07-005:** Usuário clica em "Analisar TCO"
- **FP-UC07-006:** Sistema calcula para cada tecnologia:
  - Custo de aquisição (hardware, instalação)
  - Custo operacional mensal (mensalidade, manutenção)
  - Custo variável mensal (minutos, chamadas)
  - Custo de suporte mensal
  - TCO total em 1, 3, 5 anos (com inflação)
- **FP-UC07-007:** Sistema gera relatório com:
  - Resumo executivo (menor TCO, tecnologia recomendada)
  - Comparação side-by-side (tabela E1 vs SIP vs Analógico)
  - Gráfico de evolução de custos (1, 3, 5 anos)
  - Análise de vantagens/desvantagens de cada tecnologia
  - Recomendação estratégica baseada em menor TCO
- **FP-UC07-008:** Sistema exibe análise
- **FP-UC07-009:** Sistema permite exportar (PDF, Excel)

### Fluxos Alternativos
- **FA-UC07-001:** Usuário ajusta custos manualmente
  - Sistema recalcula TCO com novos valores
- **FA-UC07-002:** Usuário desconsidera inflação
  - Sistema recalcula TCO sem correção inflacionária

### Fluxos de Exceção
- **FE-UC07-001:** Custos não configurados para alguma tecnologia
  - Sistema exibe mensagem "Configure custos para [Tecnologia] antes de analisar TCO"
- **FE-UC07-002:** Erro ao calcular TCO
  - Sistema exibe mensagem de erro e registra log

### Regras de Negócio
- **RN-UC-07-001:** TCO calculado para períodos de 1, 3 e 5 anos
- **RN-UC-07-002:** Custos atualizados trimestralmente
- **RN-UC-07-003:** Considerar inflação (IPCA) na projeção
- **RN-UC-07-004:** Incluir: custo de aquisição (hardware, instalação), custo operacional (mensalidade, manutenção), custo variável (minutos), custo de suporte
- **RN-UC-07-005:** Comparação side-by-side de 3 tecnologias
- **RN-UC-07-006:** Recomendação estratégica baseada em menor TCO

### Critérios de Aceite
- **CA-UC07-001:** TCO DEVE ser calculado para 1, 3 e 5 anos
- **CA-UC07-002:** Inflação DEVE ser considerada (IPCA padrão)
- **CA-UC07-003:** Comparação DEVE incluir E1, SIP e Analógico
- **CA-UC07-004:** Recomendação DEVE ser baseada em menor TCO
- **CA-UC07-005:** Relatório DEVE incluir análise de vantagens/desvantagens

---

## UC08 — Visualizar Métricas de QoS Históricas

### Objetivo
Exibir histórico detalhado de métricas de QoS (jitter, latência, packet loss, MOS) de um tronco específico com gráficos e análise de tendências.

### Pré-condições
- Usuário autenticado
- Permissão `GES.TRONCOS.MONITORAR`
- Mínimo 24 horas de histórico

### Pós-condições
- Histórico exibido com gráficos interativos
- Análise de tendências fornecida
- Exportação permitida (PNG, PDF, CSV)

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa "Histórico de QoS"
- **FP-UC08-002:** Sistema valida permissão `GES.TRONCOS.MONITORAR`
- **FP-UC08-003:** Sistema exibe formulário com:
  - Tronco (seleção)
  - Período (6h, 24h, 7d, 30d, 90d)
  - Métricas (Jitter, Latência, Packet Loss, MOS Score)
- **FP-UC08-004:** Usuário seleciona tronco e período
- **FP-UC08-005:** Usuário clica em "Visualizar Histórico"
- **FP-UC08-006:** Sistema carrega dados históricos (últimos 90 dias)
- **FP-UC08-007:** Sistema exibe gráficos interativos:
  - Jitter ao longo do tempo (linha)
  - Latência ao longo do tempo (linha)
  - Packet Loss ao longo do tempo (linha)
  - MOS Score ao longo do tempo (linha + área)
  - Linha de referência (limites ideais/aceitáveis)
- **FP-UC08-008:** Sistema exibe análise de tendências:
  - Média do período
  - Pico (máximo e mínimo)
  - Desvio padrão
  - Tendência (melhorando, estável, degradando)
  - Eventos de falha correlacionados
- **FP-UC08-009:** Sistema permite drill-down para períodos específicos

### Fluxos Alternativos
- **FA-UC08-001:** Usuário seleciona período customizado
  - Sistema carrega dados do período selecionado
- **FA-UC08-002:** Usuário exporta gráfico (PNG, PDF)
  - Sistema gera arquivo com snapshot do gráfico
- **FA-UC08-003:** Usuário exporta dados brutos (CSV)
  - Sistema gera CSV com todas as medições do período

### Fluxos de Exceção
- **FE-UC08-001:** Histórico insuficiente (<24h)
  - Sistema exibe mensagem "Histórico insuficiente. Aguarde pelo menos 24 horas de coleta de dados"
- **FE-UC08-002:** Erro ao carregar dados
  - Sistema exibe mensagem de erro e registra log

### Regras de Negócio
- **RN-UC-08-001:** Histórico armazenado por 90 dias
- **RN-UC-08-002:** Gráficos otimizados (agregação de dados para períodos >7 dias)
- **RN-UC-08-003:** Linhas de referência: ideal (verde), aceitável (amarelo), crítico (vermelho)
- **RN-UC-08-004:** Análise de tendências: melhorando (>5% redução), estável (±5%), degradando (>5% aumento)
- **RN-UC-08-005:** Exportação de gráficos em PNG (alta resolução 300dpi)

### Critérios de Aceite
- **CA-UC08-001:** Histórico DEVE ser mantido por 90 dias
- **CA-UC08-002:** Gráficos DEVEM ser otimizados para períodos >7 dias
- **CA-UC08-003:** Linhas de referência DEVEM estar visíveis nos gráficos
- **CA-UC08-004:** Análise de tendências DEVE calcular média, pico, desvio padrão
- **CA-UC08-005:** Exportação DEVE gerar arquivo em até 10 segundos

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Aplicadas | Funcionalidades RF Cobertas |
|----|---------------------------|----------------------------|
| UC00 | RN-UC-00-001, RN-UC-00-002, RN-UC-00-003, RN-UC-00-004, RN-UC-00-005 | RF-CRUD-02, RF-SEC-01, RF-MON-01 |
| UC01 | RN-UC-01-001, RN-UC-01-002, RN-UC-01-003, RN-UC-01-004, RN-UC-01-005, RN-UC-01-006, RN-UC-01-007, RN-UC-01-008, RN-UC-01-009, RN-UC-01-010, RN-UC-01-011 | RF-CRUD-01, RF-VAL-01, RF-VAL-02, RF-VAL-03, RF-VAL-04, RF-SEC-01, RF-SEC-03, RF-SEC-04, RF-MON-01 |
| UC02 | RN-UC-02-001, RN-UC-02-002, RN-UC-02-003, RN-UC-02-004, RN-UC-02-005, RN-UC-02-006 | RF-MON-01, RF-MON-02, RF-MON-03 |
| UC03 | RN-UC-03-001, RN-UC-03-002, RN-UC-03-003, RN-UC-03-004, RN-UC-03-005, RN-UC-03-006, RN-UC-03-007 | RF-AUT-01, RF-SEC-02 |
| UC04 | RN-UC-04-001, RN-UC-04-002, RN-UC-04-003, RN-UC-04-004, RN-UC-04-005, RN-UC-04-006 | RN-RF040-09 |
| UC05 | RN-UC-05-001, RN-UC-05-002, RN-UC-05-003, RN-UC-05-004, RN-UC-05-005 | RN-RF040-11, RF-AUT-03 |
| UC06 | RN-UC-06-001, RN-UC-06-002, RN-UC-06-003, RN-UC-06-004, RN-UC-06-005, RN-UC-06-006 | RN-RF040-12 |
| UC07 | RN-UC-07-001, RN-UC-07-002, RN-UC-07-003, RN-UC-07-004, RN-UC-07-005, RN-UC-07-006 | RN-RF040-14 |
| UC08 | RN-UC-08-001, RN-UC-08-002, RN-UC-08-003, RN-UC-08-004, RN-UC-08-005 | RN-RF040-11, RF-MON-02, RF-MON-03 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Migração para Governança v2.0 - Estrutura completa com 9 UCs conforme template v2.0, cobertura 100% do RF040, fluxos detalhados (FP/FA/FE), critérios de aceite, matriz de rastreabilidade |
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial com 9 UCs básicos |

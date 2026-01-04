# UC-RF029 — Casos de Uso Canônicos

**RF:** RF029 — Gestão de SLA - Serviços
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase-5-Service-Desk

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Listar SLAs de Serviço | Exibir listagem paginada de SLAs de serviço (KPIs estratégicos) |
| UC02 | Criar SLA de Serviço | Criar novo SLA de serviço com KPIs de negócio |
| UC03 | Visualizar SLA de Serviço | Exibir detalhes completos de um SLA de serviço |
| UC04 | Editar SLA de Serviço | Alterar configurações de SLA de serviço |
| UC05 | Inativar SLA de Serviço | Inativar SLA logicamente |
| UC06 | Gerenciar Balanced Scorecard | Criar e gerenciar scorecards balanceados (BSC) |
| UC07 | Visualizar Dashboard Executivo | Dashboard estratégico com KPIs de negócio |
| UC08 | Gerar Relatório Qualidade | Gerar relatórios de qualidade de serviço |

---

## UC01 - Listar SLAs de Serviço

### Descrição
Exibir listagem paginada de SLAs de serviço (KPIs estratégicos) com filtros avançados.

### Atores
- Usuário autenticado com permissão de visualização
- Gerente executivo
- Diretor de TI

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.LISTAR`
- Multi-tenancy: Usuário vinculado a conglomerado

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "SLA" → "SLA Serviços" | - |
| 2 | - | Carrega lista paginada (20 registros/página) |
| 3 | - | Exibe colunas: Nome SLA, Categoria KPI, Valor Atual, Meta, % Atingimento, Status, Ações |
| 4 | Aplica filtros (categoria, status) | Recarrega lista com filtros aplicados |
| 5 | Pode ordenar por coluna | Reordena resultados |

### Filtros Disponíveis

| Filtro | Tipo | Descrição |
|--------|------|-----------|
| Categoria KPI | Select Multiple | CSAT, NPS, FCR, Quality Score, Compliance |
| Status | Select | Atingiu Meta, Abaixo Meta, Em Risco |
| Perspectiva BSC | Select | Financeira, Clientes, Processos, Aprendizado |

### Fluxos Alternativos

**FA01 - Lista Vazia**
- **Condição:** Não existem SLAs para os filtros aplicados
- **Ação:** Sistema exibe mensagem "Nenhum SLA encontrado" + botão "Criar Novo SLA"

**FA02 - Visualizar BSC**
- **Condição:** Usuário clica em "Visualizar Balanced Scorecard"
- **Ação:** Sistema redireciona para UC06

### Exceções

**EX01 - Erro de Conexão**
- **Condição:** Falha na comunicação com servidor
- **Ação:** Sistema exibe mensagem de erro e botão "Tentar novamente"

### Pós-condições
- Lista exibida com dados atualizados
- Filtros persistidos na sessão do usuário

### Regras de Negócio Aplicáveis
- RN-SLS-029-15: Isolamento multi-tenancy
- RN-SLS-029-16: Auditoria de acesso

---

## UC02 - Criar SLA de Serviço

### Descrição
Criar novo SLA de serviço definindo KPIs de negócio (CSAT, NPS, FCR, Quality Score) e metas estratégicas.

### Atores
- Usuário autenticado com permissão de criação
- Gerente de qualidade

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.CRIAR`

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Novo SLA de Serviço" | - |
| 2 | - | Exibe formulário de criação |
| 3 | Preenche campos obrigatórios | Sistema valida em tempo real |
| 4 | Define KPI e fórmula de cálculo | - |
| 5 | Define metas (mínimo, alvo, stretch) | - |
| 6 | Vincula a perspectiva BSC | - |
| 7 | Clica em "Salvar" | - |
| 8 | - | Valida dados |
| 9 | - | Salva SLA |
| 10 | - | Exibe mensagem de sucesso |

### Campos do Formulário

**Seção 1: Informações Básicas**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Nome SLA | Text | Sim | Max 200 caracteres, único |
| Descrição | Textarea | Sim | Min 50, max 1000 caracteres |
| Categoria KPI | Select | Sim | CSAT, NPS, FCR, Quality Score, Compliance |
| Perspectiva BSC | Select | Sim | Financeira, Clientes, Processos, Aprendizado |

**Seção 2: Configuração do KPI**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Tipo KPI | Select | Sim | Simples (1 métrica) ou Composto (múltiplas métricas) |
| Fórmula Cálculo | Textarea | Sim (se composto) | Expressão matemática (ex: "0.4*CSAT + 0.3*FCR + 0.3*Compliance") |
| Unidade Medida | Select | Sim | %, Pontos, Minutos, Horas |
| Frequência Coleta | Select | Sim | Diária, Semanal, Mensal, Trimestral |

**Seção 3: Metas**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Meta Mínima | Number | Sim | > 0 |
| Meta Alvo | Number | Sim | ≥ Meta Mínima |
| Meta Stretch | Number | Não | ≥ Meta Alvo (meta aspiracional) |

**Seção 4: Integração com Pesquisas**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Integração Ativa | Checkbox | Não | - |
| Ferramenta | Select | Condicional | SurveyMonkey, Typeform, Google Forms |
| API Key | Text | Condicional | - |

### Fluxos Alternativos

**FA01 - Usar KPI Pré-Configurado**
- **Condição:** Usuário clica em "Biblioteca KPIs"
- **Ação:** Sistema lista 100+ KPIs pré-configurados e preenche formulário

**FA02 - Salvar como Rascunho**
- **Condição:** Usuário clica em "Salvar Rascunho"
- **Ação:** Sistema salva com status "Rascunho"

### Exceções

**EX01 - Validação Falhou**
- **Condição:** Campos inválidos
- **Ação:** Sistema destaca campos com erro e impede salvamento

**EX02 - Fórmula Inválida**
- **Condição:** Expressão matemática com erro de sintaxe
- **Ação:** Sistema exibe "Fórmula inválida. Exemplo: 0.4*CSAT + 0.6*NPS"

### Pós-condições
- SLA criado com status "Ativo"
- Log de auditoria registrado
- Notificação enviada para gestores

### Regras de Negócio Aplicáveis
- RN-SLS-029-01: Catálogo 100+ KPIs pré-configurados
- RN-SLS-029-02: KPIs compostos com fórmulas customizáveis
- RN-SLS-029-03: Integração com ferramentas de pesquisa

---

## UC03 - Visualizar SLA de Serviço

### Descrição
Exibir detalhes completos de um SLA de serviço incluindo configuração, valor atual, tendências e histórico.

### Atores
- Usuário autenticado com permissão de visualização

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.VISUALIZAR`
- SLA existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em SLA na listagem | - |
| 2 | - | Carrega dados completos do SLA |
| 3 | - | Exibe tela com abas: Resumo, Tendências, Metas, Histórico |
| 4 | Navega entre abas | Carrega conteúdo da aba selecionada |

### Informações Exibidas

**Aba Resumo:**

| Campo | Descrição |
|-------|-----------|
| Nome SLA | Nome do SLA |
| Categoria KPI | CSAT, NPS, FCR, etc. |
| Valor Atual | Valor atual do KPI |
| Meta Alvo | Meta definida |
| % Atingimento | Percentual de atingimento da meta |
| Status | Atingiu, Abaixo, Em Risco |
| Última Atualização | Data/hora última coleta |

**Aba Tendências:**
- Gráfico de linha: Evolução do KPI (últimos 90 dias)
- Gráfico de barras: Comparação com meta (mensal)
- Previsão ML.NET: Projeção 30/60/90 dias

**Aba Metas:**
- Tabela com histórico de metas
- Colunas: Período, Meta Mínima, Meta Alvo, Meta Stretch, Atingido
- Gráfico de progresso anual

**Aba Histórico:**
- Timeline de eventos: Criação, Modificações, Atingimento de Metas
- Quem realizou cada ação + data/hora

### Fluxos Alternativos

**FA01 - Editar SLA**
- **Condição:** Usuário com permissão `SLA_SERVICOS.EDITAR` clica em "Editar"
- **Ação:** Sistema redireciona para UC04

**FA02 - Exportar Dados**
- **Condição:** Usuário clica em "Exportar Tendências"
- **Ação:** Sistema gera Excel com histórico de valores

### Exceções

**EX01 - SLA Não Encontrado**
- **Condição:** SLA foi excluído por outro usuário
- **Ação:** Sistema exibe mensagem e redireciona para listagem

### Pós-condições
- Acesso ao SLA registrado em log de auditoria
- Nenhuma alteração no sistema

### Regras de Negócio Aplicáveis
- RN-SLS-029-15: Multi-tenancy
- RN-SLS-029-16: Auditoria de acesso

---

## UC04 - Editar SLA de Serviço

### Descrição
Alterar configurações de SLA de serviço (nome, metas, fórmula). Alteração gera nova versão.

### Atores
- Usuário autenticado com permissão de edição

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.EDITAR`
- SLA existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Editar" no SLA | - |
| 2 | - | Carrega formulário com dados preenchidos |
| 3 | Altera campos desejados | Sistema valida em tempo real |
| 4 | Clica em "Salvar Alterações" | - |
| 5 | - | Valida dados |
| 6 | - | Cria nova versão do SLA (versionamento) |
| 7 | - | Atualiza SLA |
| 8 | - | Exibe mensagem de sucesso |

### Fluxos Alternativos

**FA01 - Cancelar Edição**
- **Condição:** Usuário clica em "Cancelar"
- **Ação:** Sistema descarta alterações e retorna à visualização

**FA02 - Alterar Categoria KPI**
- **Condição:** Usuário tenta alterar categoria
- **Ação:** Sistema alerta "Alteração de categoria requer criação de novo SLA" e bloqueia campo

### Exceções

**EX01 - Conflito de Edição**
- **Condição:** Outro usuário está editando simultaneamente
- **Ação:** Sistema exibe mensagem de bloqueio

### Pós-condições
- SLA atualizado
- Nova versão do SLA criada
- Log de auditoria registrado

### Regras de Negócio Aplicáveis
- RN-SLS-029-04: Versionamento de SLAs
- RN-SLS-029-15: Multi-tenancy

---

## UC05 - Inativar SLA de Serviço

### Descrição
Inativar SLA logicamente (soft delete). Histórico é preservado por 7 anos.

### Atores
- Usuário autenticado com permissão de exclusão

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.INATIVAR`
- SLA existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Inativar" no SLA | - |
| 2 | - | Exibe diálogo "Deseja realmente inativar este SLA? Coletas serão interrompidas." |
| 3 | Confirma inativação | - |
| 4 | - | Marca SLA como inativo (Fl_Excluido = true) |
| 5 | - | Cancela coletas automáticas |
| 6 | - | Exibe mensagem de sucesso |

### Fluxos Alternativos

**FA01 - Cancelar Inativação**
- **Condição:** Usuário cancela no diálogo
- **Ação:** Sistema fecha diálogo e mantém SLA ativo

### Exceções

**EX01 - SLA Já Inativo**
- **Condição:** SLA já foi inativado
- **Ação:** Sistema exibe mensagem informativa

### Pós-condições
- SLA inativado (soft delete)
- Coletas canceladas
- Histórico preservado por 7 anos (LGPD)
- Log de auditoria registrado

### Regras de Negócio Aplicáveis
- RN-SLS-029-14: Soft delete com retenção histórico
- RN-SLS-029-16: Auditoria

---

## UC06 - Gerenciar Balanced Scorecard

### Descrição
Criar e gerenciar scorecards balanceados (BSC) com 4 perspectivas (Financeira, Clientes, Processos, Aprendizado).

### Atores
- Usuário autenticado
- Diretor executivo
- Gerente estratégico

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.BSC`

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa "Balanced Scorecard" | - |
| 2 | - | Exibe dashboard BSC com 4 perspectivas |
| 3 | - | Cada perspectiva mostra KPIs vinculados |
| 4 | Clica em perspectiva | Expande para exibir detalhes |
| 5 | Pode adicionar/remover KPIs | Sistema atualiza BSC |
| 6 | Define pesos das perspectivas | Sistema recalcula score total |

### Estrutura do BSC

**Perspectiva 1: Financeira**
- KPIs: ROI, Redução Custos, Receita por Cliente
- Peso padrão: 30%

**Perspectiva 2: Clientes**
- KPIs: CSAT, NPS, Retenção, FCR
- Peso padrão: 30%

**Perspectiva 3: Processos Internos**
- KPIs: Tempo Ciclo, Eficiência, Quality Score
- Peso padrão: 25%

**Perspectiva 4: Aprendizado e Crescimento**
- KPIs: Treinamento, Inovação, Satisfação Colaboradores
- Peso padrão: 15%

### Fluxos Alternativos

**FA01 - Criar Novo BSC**
- **Condição:** Usuário clica em "Novo BSC"
- **Ação:** Sistema exibe wizard para criar scorecard do zero

**FA02 - Usar Template BSC**
- **Condição:** Usuário clica em "Templates"
- **Ação:** Sistema lista templates pré-configurados (ex: "BSC TI Padrão COBIT")

### Exceções

**EX01 - Soma Pesos ≠ 100%**
- **Condição:** Soma dos pesos das perspectivas ≠ 100%
- **Ação:** Sistema alerta e bloqueia salvamento

### Pós-condições
- BSC criado/atualizado
- Score total calculado
- Log de auditoria registrado

### Regras de Negócio Aplicáveis
- RN-SLS-029-05: BSC com 4 perspectivas configuráveis
- RN-SLS-029-06: Hierarquia objetivos → KPIs → Metas

---

## UC07 - Visualizar Dashboard Executivo

### Descrição
Dashboard estratégico com KPIs de negócio em tempo real, drill-down hierárquico e análise de tendências.

### Atores
- Usuário autenticado
- C-level (CEO, CTO, CFO)
- Gerente executivo

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.DASHBOARD`
- SLAs de serviço ativos existem

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa "Dashboard Executivo SLA Serviços" | - |
| 2 | - | Carrega dashboard em tempo real (SignalR) |
| 3 | - | Exibe cards com KPIs principais |
| 4 | - | Exibe gráficos estratégicos |
| 5 | Filtra por período/perspectiva | Sistema atualiza dashboard |
| 6 | Clica em KPI para drill-down | Sistema exibe detalhamento até nível operacional |

### Componentes do Dashboard

**Cards Principais:**
- Score BSC Total (0-100)
- CSAT Médio
- NPS Médio
- % Metas Atingidas

**Gráficos:**
- Radar: 4 perspectivas BSC
- Linha: Evolução KPIs últimos 12 meses
- Barra: Top 5 KPIs melhores/piores

**Previsões ML:**
- Projeção CSAT próximos 30 dias
- Alertas de KPIs em risco

### Fluxos Alternativos

**FA01 - Drill-Down Hierárquico**
- **Condição:** Usuário clica em KPI
- **Ação:** Sistema exibe níveis hierárquicos (Estratégico → Tático → Operacional)

**FA02 - Comparar Períodos**
- **Condição:** Usuário seleciona 2 períodos
- **Ação:** Sistema exibe gráficos comparativos

### Exceções

**EX01 - Nenhum SLA Ativo**
- **Condição:** Não há SLAs ativos para exibir
- **Ação:** Sistema exibe mensagem "Nenhum SLA ativo. Crie seu primeiro SLA."

### Pós-condições
- Dashboard atualizado em tempo real via SignalR
- Acesso registrado em log

### Regras de Negócio Aplicáveis
- RN-SLS-029-07: Dashboard executivo com drill-down
- RN-SLS-029-08: Análise preditiva com ML.NET

---

## UC08 - Gerar Relatório Qualidade

### Descrição
Gerar relatórios mensais/trimestrais de qualidade de serviço com evidências para auditorias ISO 20000 e ITIL.

### Atores
- Usuário autenticado
- Auditor de qualidade

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `SLA_SERVICOS.RELATORIOS`
- Dados históricos existem no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa "Relatórios" → "Qualidade de Serviço" | - |
| 2 | - | Exibe formulário de geração |
| 3 | Seleciona período (mês/trimestre/ano) | - |
| 4 | Seleciona SLAs (todos ou específicos) | - |
| 5 | Seleciona formato (PDF executivo, Excel analítico, Power BI) | - |
| 6 | Clica em "Gerar Relatório" | - |
| 7 | - | Processa relatório em background |
| 8 | - | Envia notificação quando pronto |
| 9 | Clica em link de download | Faz download do arquivo |

### Conteúdo do Relatório

**Seção 1: Resumo Executivo**
- Score BSC Total
- % Metas Atingidas
- CSAT/NPS Médios
- Tendência vs. Período Anterior

**Seção 2: Análise por Perspectiva BSC**
- 4 seções (Financeira, Clientes, Processos, Aprendizado)
- KPIs, valores, metas, % atingimento

**Seção 3: Gráficos**
- Radar BSC
- Evolução KPIs (linha)
- Benchmark de Mercado

**Seção 4: Evidências para Auditoria**
- Snapshots de dados
- Fontes de coleta
- Metodologia de cálculo

### Fluxos Alternativos

**FA01 - Agendar Relatório Recorrente**
- **Condição:** Usuário clica em "Agendar"
- **Ação:** Sistema agenda geração mensal/trimestral e envia por e-mail

### Exceções

**EX01 - Dados Insuficientes**
- **Condição:** Período selecionado não possui dados
- **Ação:** Sistema exibe "Sem dados para o período selecionado"

### Pós-condições
- Relatório gerado e disponível para download
- Exportação registrada em log de auditoria

### Regras de Negócio Aplicáveis
- RN-SLS-029-09: Relatórios qualidade ISO 20000/ITIL
- RN-SLS-029-16: Auditoria de exportação

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 17/12/2025 | Architect Agent | Versão inicial com 8 casos de uso completos |

# Casos de Uso - RF026

**RF:** RF-026 — Gestão Completa de Faturas de Telecom e TI
**Epic:** EPIC006-FIN - Financeiro Base
**Fase:** Fase 3 - Financeiro I - Base Contábil
**Versão:** 1.0
**Data:** 2025-12-17
**Autor:** Agência ALC - alc.dev.br

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Listar Faturas | Exibir listagem paginada de faturas com filtros avançados |
| UC02 | Importar Fatura | Importar fatura de arquivo (CSV, Excel, PDF com OCR) |
| UC03 | Visualizar Fatura | Exibir detalhes completos de uma fatura específica |
| UC04 | Auditar Fatura | Executar auditoria de cobrança conforme regras configuradas |
| UC05 | Contestar Fatura | Criar e gerenciar contestação de cobranças indevidas |
| UC06 | Ratear Fatura | Aplicar rateio multi-dimensional de custos |
| UC07 | Aprovar Fatura | Workflow de aprovação multi-nível de faturas |
| UC08 | Exportar Faturas | Exportar dados de faturas para relatórios |

---

## UC01 - Listar Faturas

### Descrição
Exibir listagem paginada de faturas com filtros avançados (período, operadora, status, valor), ordenação e busca textual.

### Atores
- Usuário autenticado com permissão de visualização de faturas
- Gestor financeiro
- Auditor

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.LISTAR`
- Multi-tenancy: Usuário vinculado a conglomerado

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Faturas" | - |
| 2 | - | Carrega lista paginada (20 registros/página) |
| 3 | - | Exibe colunas: Número, Operadora, Data Emissão, Vencimento, Valor Total, Status, Ações |
| 4 | Aplica filtros (período, operadora, status) | Recarrega lista com filtros aplicados |
| 5 | Pode ordenar por coluna | Reordena resultados |
| 6 | Pode buscar por número/CNPJ | Filtra resultados em tempo real |

### Filtros Disponíveis

| Filtro | Tipo | Descrição |
|--------|------|-----------|
| Período | Date Range | Data emissão início/fim |
| Operadora | Select Multiple | Vivo, Claro, TIM, Oi, outros |
| Status | Select | Importada, Auditada, Contestada, Aprovada, Paga |
| Valor Mínimo | Number | Filtro valor ≥ X |
| Valor Máximo | Number | Filtro valor ≤ X |
| Centro Custo | Select | Filtro por centro de custo |

### Fluxos Alternativos

**FA01 - Lista Vazia**
- **Condição:** Não existem faturas no período filtrado
- **Ação:** Sistema exibe mensagem "Nenhuma fatura encontrada para os filtros aplicados" + sugestão "Importar nova fatura"

**FA02 - Exportar Lista**
- **Condição:** Usuário clica em "Exportar"
- **Ação:** Sistema gera Excel com todas as colunas visíveis + filtros aplicados

### Exceções

**EX01 - Erro de Conexão**
- **Condição:** Falha na comunicação com servidor
- **Ação:** Sistema exibe mensagem de erro e botão "Tentar novamente"

**EX02 - Timeout na Query**
- **Condição:** Consulta excede 30 segundos (muitos registros)
- **Ação:** Sistema sugere aplicar mais filtros para reduzir resultado

### Pós-condições
- Lista exibida com dados atualizados
- Filtros persistidos na sessão do usuário

### Regras de Negócio Aplicáveis
- RN-FAT-026-15: Isolamento multi-tenancy (exibir apenas faturas do conglomerado)
- RN-FAT-026-16: Auditoria de acesso (log de visualização)

---

## UC02 - Importar Fatura

### Descrição
Importar fatura de arquivo CSV, Excel, XML ou PDF (com OCR) usando layouts configuráveis por operadora.

### Atores
- Usuário autenticado com permissão de importação
- Coordenador financeiro

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.IMPORTAR`
- Layout de importação configurado para operadora (RF030)
- Arquivo em formato suportado (CSV, XLS, XLSX, PDF)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Importar Fatura" | - |
| 2 | - | Exibe wizard de importação (Passo 1/5: Upload) |
| 3 | Seleciona operadora (Vivo, Claro, TIM, etc.) | - |
| 4 | Faz upload do arquivo | Detecta formato automaticamente |
| 5 | - | Valida estrutura contra layout configurado (Passo 2/5) |
| 6 | - | Exibe preview de 10 primeiras linhas (Passo 3/5) |
| 7 | Confirma mapeamento de colunas | - |
| 8 | - | Executa importação com validações (Passo 4/5) |
| 9 | - | Exibe resumo: X linhas importadas, Y rejeitadas (Passo 5/5) |
| 10 | Clica em "Concluir" | Redireciona para visualização da fatura |

### Campos do Formulário (Wizard)

**Passo 1 - Upload:**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Operadora | Select | Sim | Deve ter layout configurado |
| Arquivo | File Upload | Sim | Max 50MB, formatos: CSV, XLS, XLSX, PDF |
| Período Referência | Month/Year | Sim | Formato MM/AAAA |

**Passo 2 - Validação (automático):**
- Sistema detecta encoding (UTF-8, ISO-8859-1)
- Sistema detecta delimitador (`,`, `;`, `\t`)
- Sistema valida colunas obrigatórias presentes

**Passo 3 - Preview:**
- Tabela com 10 primeiras linhas
- Opção de ajustar mapeamento manual

**Passo 4 - Importação:**
- Progress bar em tempo real
- Log de erros de validação

**Passo 5 - Resumo:**
- Total linhas processadas
- Total linhas importadas com sucesso
- Total linhas rejeitadas (download Excel com erros)

### Fluxos Alternativos

**FA01 - Arquivo PDF (OCR)**
- **Condição:** Arquivo é PDF
- **Ação:** Sistema executa Azure Form Recognizer
- **Passo adicional:** Exibe campos extraídos com confiança (%) para validação manual

**FA02 - Cancelar Importação**
- **Condição:** Usuário clica em "Cancelar" durante wizard
- **Ação:** Sistema descarta upload e retorna à listagem

**FA03 - Fatura Duplicada**
- **Condição:** Sistema detecta fatura já importada (mesmo número + operadora + período)
- **Ação:** Exibe alerta "Fatura já existe. Deseja substituir?" (Sim/Não)

### Exceções

**EX01 - Arquivo Inválido**
- **Condição:** Arquivo corrompido ou formato não suportado
- **Ação:** Sistema exibe mensagem "Arquivo inválido ou corrompido. Tente novamente com outro arquivo."

**EX02 - Layout Incompatível**
- **Condição:** Arquivo não corresponde ao layout selecionado
- **Ação:** Sistema exibe diferenças detectadas + sugestão "Criar novo layout" (RF030)

**EX03 - Validação Falhou >50% Linhas**
- **Condição:** Mais de 50% das linhas possuem erros
- **Ação:** Sistema bloqueia importação e solicita revisão do arquivo

### Pós-condições
- Fatura importada com status "Importada"
- Log de auditoria registrado
- Notificação enviada para responsável pela auditoria

### Regras de Negócio Aplicáveis
- RN-FAT-026-01: Importação multi-layout
- RN-FAT-026-02: OCR de PDF
- RN-FAT-026-15: Multi-tenancy

---

## UC03 - Visualizar Fatura

### Descrição
Exibir detalhes completos de uma fatura específica incluindo cabeçalho, linhas detalhadas, auditoria, rateio e histórico.

### Atores
- Usuário autenticado com permissão de visualização

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.VISUALIZAR`
- Fatura existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em fatura na listagem | - |
| 2 | - | Carrega dados completos da fatura |
| 3 | - | Exibe tela com abas: Resumo, Detalhamento, Auditoria, Rateio, Histórico |
| 4 | Navega entre abas | Carrega conteúdo da aba selecionada |

### Informações Exibidas

**Aba Resumo:**

| Campo | Descrição |
|-------|-----------|
| Número Fatura | Número único da fatura |
| Operadora | Nome operadora + CNPJ |
| Data Emissão | Data emissão da fatura |
| Data Vencimento | Data vencimento |
| Período Referência | Mês/ano de referência |
| Valor Total Bruto | Soma de todos os serviços |
| Descontos | Descontos aplicados |
| Acréscimos | Multas, juros |
| Valor Total Líquido | Valor final a pagar |
| Status | Importada, Auditada, Aprovada, Paga |
| Arquivo Original | Link download PDF/CSV |

**Aba Detalhamento:**
- Grid com linhas/ativos cobrados
- Colunas: Linha/Ativo, Descrição Serviço, Consumo, Valor Unitário, Valor Total

**Aba Auditoria:**
- Alertas identificados (cobranças indevidas, valores fora da média)
- Severidade: Informativa, Alerta, Crítica
- Status: Pendente, Contestada, Resolvida

**Aba Rateio:**
- Distribuição de custos por centro de custo
- Gráfico pizza com percentuais

**Aba Histórico:**
- Timeline de eventos: Importação, Auditoria, Contestação, Aprovação, Pagamento
- Quem realizou cada ação + data/hora

### Fluxos Alternativos

**FA01 - Editar Fatura**
- **Condição:** Usuário com permissão `FATURAS.EDITAR` clica em "Editar"
- **Ação:** Sistema redireciona para formulário de edição (UC02 modificado)

**FA02 - Contestar Cobrança**
- **Condição:** Usuário clica em "Contestar" na aba Auditoria
- **Ação:** Sistema redireciona para UC05

**FA03 - Download PDF Original**
- **Condição:** Usuário clica em "Download Arquivo Original"
- **Ação:** Sistema baixa PDF/CSV importado

### Exceções

**EX01 - Fatura Não Encontrada**
- **Condição:** Fatura foi excluída por outro usuário
- **Ação:** Sistema exibe mensagem e redireciona para listagem

**EX02 - Arquivo Original Indisponível**
- **Condição:** Arquivo foi movido/deletado do storage
- **Ação:** Sistema exibe mensagem "Arquivo original não disponível"

### Pós-condições
- Acesso à fatura registrado em log de auditoria
- Nenhuma alteração no sistema

### Regras de Negócio Aplicáveis
- RN-FAT-026-15: Multi-tenancy
- RN-FAT-026-16: Auditoria de acesso

---

## UC04 - Auditar Fatura

### Descrição
Executar auditoria automática de fatura aplicando 25+ regras configuráveis para identificar cobranças indevidas.

### Atores
- Usuário autenticado com permissão de auditoria
- Sistema (execução automática pós-importação)

### Pré-condições
- Usuário logado no sistema (se manual)
- Usuário com permissão `FATURAS.AUDITAR`
- Fatura importada com sucesso
- Regras de auditoria configuradas (RF030)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Auditar" na fatura | - |
| 2 | - | Carrega regras de auditoria ativas |
| 3 | - | Executa cada regra contra linhas da fatura |
| 4 | - | Identifica alertas por regra |
| 5 | - | Exibe resumo: X alertas (Y críticos, Z alerta, W info) |
| 6 | Revisa alertas | - |
| 7 | Marca alertas como "Justificado" ou "A Contestar" | - |
| 8 | Clica em "Concluir Auditoria" | Atualiza status fatura para "Auditada" |

### Regras de Auditoria (Exemplos)

| Regra | Severidade | Descrição |
|-------|-----------|-----------|
| Linha sem contrato | Crítica | Linha cobrada sem contrato vigente |
| Valor >15% média | Alerta | Consumo 15% acima da média histórica |
| Serviço cancelado | Crítica | Cobrança de serviço já cancelado |
| Roaming não autorizado | Alerta | Roaming internacional sem autorização |
| Duplicidade | Crítica | Mesma linha cobrada 2x na fatura |

### Fluxos Alternativos

**FA01 - Auditoria Automática**
- **Condição:** Fatura é importada
- **Ação:** Sistema executa auditoria automaticamente em background (Hangfire job)

**FA02 - Nenhum Alerta**
- **Condição:** Auditoria não identifica problemas
- **Ação:** Sistema exibe "✅ Nenhum alerta identificado. Fatura está conforme."

**FA03 - Exportar Alertas**
- **Condição:** Usuário clica em "Exportar Alertas"
- **Ação:** Sistema gera Excel com todos os alertas + evidências

### Exceções

**EX01 - Regras Não Configuradas**
- **Condição:** Não há regras ativas para operadora
- **Ação:** Sistema exibe mensagem "Configure regras de auditoria em Parâmetros Faturamento"

**EX02 - Erro em Regra Específica**
- **Condição:** Regra falha durante execução (ex: divisão por zero)
- **Ação:** Sistema registra erro em log e continua com próximas regras

### Pós-condições
- Fatura com status "Auditada"
- Alertas registrados no banco
- Notificação enviada para responsável se alertas críticos

### Regras de Negócio Aplicáveis
- RN-FAT-026-04: Auditoria configurável
- RN-FAT-026-05: Conciliação com contratos

---

## UC05 - Contestar Fatura

### Descrição
Criar e gerenciar contestação de cobranças indevidas com workflow de envio para operadora e acompanhamento de SLA.

### Atores
- Usuário autenticado com permissão de contestação
- Gestor financeiro (aprovador)

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.CONTESTAR`
- Fatura auditada com alertas marcados "A Contestar"

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Contestar" em alerta crítico | - |
| 2 | - | Exibe formulário de contestação |
| 3 | Preenche motivo, valor contestado, evidências | - |
| 4 | Faz upload de documentos comprobatórios | - |
| 5 | Clica em "Enviar Contestação" | - |
| 6 | - | Cria ticket de contestação |
| 7 | - | Envia para aprovação do gestor |
| 8 | Gestor aprova contestação | - |
| 9 | - | Envia para operadora via API/e-mail |
| 10 | - | Inicia acompanhamento de SLA (15 dias úteis) |

### Campos do Formulário

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Tipo Contestação | Select | Sim | Cobrança indevida, Valor incorreto, Serviço não contratado |
| Linhas Contestadas | Multi-select | Sim | Mínimo 1 linha |
| Valor Contestado | Number | Sim | > 0 e ≤ valor fatura |
| Motivo Detalhado | Textarea | Sim | Min 50 caracteres |
| Evidências | File Upload | Não | Contratos, e-mails, prints (max 5 arquivos 10MB) |

### Fluxos Alternativos

**FA01 - Contestação Múltiplas Linhas**
- **Condição:** Usuário seleciona múltiplas linhas
- **Ação:** Sistema agrupa em única contestação com linhas detalhadas

**FA02 - Contestação Rejeitada**
- **Condição:** Gestor rejeita contestação
- **Ação:** Sistema solicita revisão do usuário + justificativa da rejeição

**FA03 - Operadora Aceita Contestação**
- **Condição:** Operadora confirma crédito
- **Ação:** Sistema registra crédito a compensar na próxima fatura

### Exceções

**EX01 - Prazo de Contestação Expirado**
- **Condição:** Fatura vencida há >30 dias
- **Ação:** Sistema exibe alerta "Contestação fora do prazo. Operadora pode recusar."

**EX02 - Valor Contestado > Valor Fatura**
- **Condição:** Soma valores contestados excede valor total
- **Ação:** Sistema bloqueia salvamento e exibe erro

### Pós-condições
- Ticket de contestação criado
- Status fatura atualizado para "Contestada"
- Workflow de aprovação iniciado
- Log de auditoria registrado

### Regras de Negócio Aplicáveis
- RN-FAT-026-06: Workflow de contestação
- RN-FAT-026-14: SLA de resposta operadora (15 dias úteis)

---

## UC06 - Ratear Fatura

### Descrição
Aplicar rateio multi-dimensional de custos da fatura por centro de custo, departamento, projeto, etc.

### Atores
- Usuário autenticado com permissão de rateio
- Controller financeiro

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.RATEAR`
- Fatura aprovada
- Template de rateio configurado (RF030)

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Ratear" na fatura | - |
| 2 | - | Exibe templates de rateio disponíveis |
| 3 | Seleciona template (ex: "Por Centro Custo - Proporcional Consumo") | - |
| 4 | - | Calcula rateio automaticamente |
| 5 | - | Exibe preview com distribuição (tabela + gráfico pizza) |
| 6 | Pode ajustar percentuais manualmente | Sistema recalcula valores em tempo real |
| 7 | Clica em "Aplicar Rateio" | - |
| 8 | - | Salva rateio e gera lançamentos contábeis |

### Templates de Rateio (Exemplos)

| Template | Tipo | Descrição |
|----------|------|-----------|
| Centro Custo - Fixo | Percentual fixo | Distribui valores conforme % pré-definidos |
| Centro Custo - Proporcional Consumo | Variável | Distribui proporcionalmente ao consumo de cada CC |
| Departamento - Igualitário | Fixo | Divide valor igualmente entre departamentos |
| Projeto - Misto | Misto | Combina fixo + variável |

### Fluxos Alternativos

**FA01 - Rateio Manual**
- **Condição:** Usuário não seleciona template
- **Ação:** Sistema permite definir percentuais manualmente (soma deve ser 100%)

**FA02 - Salvar Novo Template**
- **Condição:** Usuário ajusta rateio e clica "Salvar como Template"
- **Ação:** Sistema salva configuração para reutilizar

**FA03 - Simular Rateio**
- **Condição:** Usuário clica em "Simular" antes de aplicar
- **Ação:** Sistema exibe preview sem salvar no banco

### Exceções

**EX01 - Soma Percentuais ≠ 100%**
- **Condição:** Soma dos percentuais ≠ 100%
- **Ação:** Sistema bloqueia salvamento e exibe erro

**EX02 - Centro Custo Inativo**
- **Condição:** Template referencia CC inativo
- **Ação:** Sistema alerta e permite substituir CC

### Pós-condições
- Rateio aplicado e salvo
- Lançamentos contábeis gerados
- Status fatura atualizado para "Rateada"

### Regras de Negócio Aplicáveis
- RN-FAT-026-07: Rateio multi-dimensional
- RN-FAT-026-15: Multi-tenancy

---

## UC07 - Aprovar Fatura

### Descrição
Workflow de aprovação multi-nível de faturas (Coordenador → Gerente → Diretor) com prazos SLA.

### Atores
- Coordenador financeiro (1º nível)
- Gerente financeiro (2º nível)
- Diretor financeiro (3º nível)

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.APROVAR`
- Fatura auditada e rateada
- Workflow configurado

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Coordenador acessa "Faturas Pendentes Aprovação" | - |
| 2 | - | Lista faturas aguardando aprovação nível 1 |
| 3 | Clica em fatura | Exibe resumo + alertas auditoria |
| 4 | Analisa valores e alertas | - |
| 5 | Clica em "Aprovar" | - |
| 6 | - | Envia para aprovação nível 2 (Gerente) |
| 7 | Gerente aprova | Envia para nível 3 (Diretor) |
| 8 | Diretor aprova | Status atualizado para "Aprovada" |

### Campos do Formulário

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Decisão | Radio | Sim | Aprovar / Rejeitar |
| Observações | Textarea | Não (obrigatório se rejeitar) | Max 500 caracteres |

### Fluxos Alternativos

**FA01 - Rejeitar Fatura**
- **Condição:** Aprovador clica em "Rejeitar"
- **Ação:** Sistema solicita justificativa e devolve para nível anterior

**FA02 - Delegar Aprovação**
- **Condição:** Aprovador ausente (férias, afastamento)
- **Ação:** Sistema permite delegar para substituto pré-cadastrado

**FA03 - Aprovação Automática**
- **Condição:** Valor fatura < R$ 5.000 e sem alertas críticos
- **Ação:** Sistema aprova automaticamente nos 3 níveis

### Exceções

**EX01 - Prazo SLA Expirado**
- **Condição:** Aprovador não decide em 48h
- **Ação:** Sistema escala automaticamente para nível superior

**EX02 - Aprovador Sem Permissão**
- **Condição:** Usuário não tem alçada para valor da fatura
- **Ação:** Sistema bloqueia aprovação e escala para superior

### Pós-condições
- Fatura aprovada ou rejeitada
- Histórico de aprovações registrado
- Notificação enviada para próximo nível ou solicitante (se rejeitada)

### Regras de Negócio Aplicáveis
- RN-FAT-026-08: Workflow aprovação multi-nível
- RN-FAT-026-09: Alçadas por valor

---

## UC08 - Exportar Faturas

### Descrição
Exportar dados de faturas para relatórios em diversos formatos (Excel, PDF, CSV, Power BI).

### Atores
- Usuário autenticado com permissão de exportação

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `FATURAS.EXPORTAR`
- Faturas existem no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Aplica filtros na listagem de faturas | - |
| 2 | Clica em "Exportar" | - |
| 3 | - | Exibe modal com opções de exportação |
| 4 | Seleciona formato (Excel, PDF, CSV) | - |
| 5 | Seleciona colunas a exportar | - |
| 6 | Clica em "Gerar Exportação" | - |
| 7 | - | Processa exportação em background |
| 8 | - | Envia notificação quando pronto |
| 9 | Clica em link de download | Faz download do arquivo |

### Opções de Exportação

| Formato | Descrição | Uso |
|---------|-----------|-----|
| Excel | XLSX com formatação e gráficos | Análise financeira |
| PDF | Relatório formatado com logo | Apresentações executivas |
| CSV | Dados tabulares simples | Importação em outros sistemas |
| Power BI | Dataset estruturado | Dashboards interativos |

### Fluxos Alternativos

**FA01 - Exportação Agendada**
- **Condição:** Usuário clica em "Agendar Exportação Recorrente"
- **Ação:** Sistema agenda exportação mensal/semanal e envia por e-mail

**FA02 - Exportação Detalhada**
- **Condição:** Usuário marca opção "Incluir linhas detalhadas"
- **Ação:** Sistema exporta também linhas/ativos de cada fatura

### Exceções

**EX01 - Limite de Registros Excedido**
- **Condição:** Exportação >50.000 registros
- **Ação:** Sistema sugere aplicar mais filtros ou processar em background

**EX02 - Erro na Geração**
- **Condição:** Falha ao gerar arquivo
- **Ação:** Sistema registra erro em log e notifica usuário

### Pós-condições
- Arquivo gerado e disponível para download
- Exportação registrada em log de auditoria
- Arquivo expira em 7 dias (limpeza automática)

### Regras de Negócio Aplicáveis
- RN-FAT-026-15: Multi-tenancy (exportar apenas faturas do conglomerado)
- RN-FAT-026-16: Auditoria de exportação

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 17/12/2025 | Architect Agent | Versão inicial com 8 casos de uso completos |

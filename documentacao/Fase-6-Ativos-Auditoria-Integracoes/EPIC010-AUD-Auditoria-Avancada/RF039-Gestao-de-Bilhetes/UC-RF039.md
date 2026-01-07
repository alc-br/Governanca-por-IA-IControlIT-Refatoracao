# UC-RF039 — Casos de Uso de Gestão de Bilhetes de Telecom

**RF:** RF039 — Gestão Completa de Bilhetes de Telecom
**Epic:** EPIC010-AUD - Auditoria Avançada
**Fase:** Fase 6 - Ativos Auditoria Integracoes
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## Sumário

Este documento define os **Casos de Uso (UC)** do **RF039 — Gestão de Bilhetes de Telecom**. Cada UC representa um comportamento esperado do sistema, com fluxo principal, fluxos alternativos, fluxos de exceção e critérios de aceite.

**Total de Casos de Uso:** 16
**Cobertura:** 100% dos requisitos do RF039

---

## Índice de Casos de Uso

| ID | Nome | Tipo | Impacta Dados |
|----|------|------|---------------|
| UC00 | Listar Bilhetes | Leitura | Não |
| UC01 | Importar Arquivo FTP | CRUD | Sim |
| UC02 | Visualizar Detalhes do Bilhete | Leitura | Não |
| UC03 | Editar Bilhete | CRUD | Sim |
| UC04 | Excluir Bilhete (Lógico) | CRUD | Sim |
| UC05 | Processar OCR em PDF Digitalizado | Ação | Sim |
| UC06 | Detectar Anomalias via ML | Ação | Sim |
| UC07 | Comparar com Plano Contratado | Ação | Não |
| UC08 | Alocar Custos por Centro de Custo | Ação | Sim |
| UC09 | Gerar Relatório de Consumo | Leitura | Não |
| UC10 | Exportar para ERP | Ação | Sim |
| UC11 | Consultar Histórico de Auditoria | Leitura | Não |
| UC12 | Dashboard de Bilhetes | Leitura | Não |
| UC13 | Aprovar Glosa de Bilhete | Ação | Sim |
| UC14 | Job: Processar Importações Pendentes | Batch | Sim |
| UC15 | Job: Enviar Alertas de Anomalias | Batch | Sim |

---

## UC00 — Listar Bilhetes

**Descrição:** Permite ao usuário visualizar todos os bilhetes de telecom importados, com filtros, paginação e ordenação.

**Ator Principal:** `usuario_autenticado`
**Tipo:** `leitura`
**Impacta Dados:** `false`

**Pré-condições:**
- Usuário autenticado
- Permissão: `BIL.BILHETES.VIEW_ANY`

**Gatilho:** Usuário acessa o menu "Bilhetes > Listar Bilhetes"

**Fluxo Principal (FP-UC00):**
1. **FP-UC00-001**: Usuário acessa a funcionalidade via menu
2. **FP-UC00-002**: Sistema valida permissão `BIL.BILHETES.VIEW_ANY`
3. **FP-UC00-003**: Sistema carrega bilhetes do tenant atual (ClienteId)
4. **FP-UC00-004**: Sistema aplica paginação (20 itens/página) e ordenação padrão (DataChamada DESC)
5. **FP-UC00-005**: Sistema exibe a lista com colunas: Número, Data, Duração, Valor, Operadora, Status

**Fluxos Alternativos (FA-UC00):**
- **FA-UC00-001**: Usuário aplica filtro por período → Sistema retorna bilhetes filtrados
- **FA-UC00-002**: Usuário busca por número de telefone → Sistema aplica busca E.164 normalizada
- **FA-UC00-003**: Usuário ordena por coluna → Sistema reordena resultados

**Fluxos de Exceção (FE-UC00):**
- **FE-UC00-001**: Usuário sem permissão → HTTP 403, mensagem "Acesso negado"
- **FE-UC00-002**: Nenhum bilhete encontrado → Exibe estado vazio "Nenhum bilhete cadastrado"

**Regras de Negócio:** RN-BIL-039-01, RN-BIL-039-13

**Critérios de Aceite:**
- [ ] Lista exibe apenas bilhetes do tenant atual
- [ ] Paginação de 20 itens por página
- [ ] Busca por número usa formato E.164

---

## UC01 — Importar Arquivo FTP

**Descrição:** Permite importar automaticamente arquivos de bilhetes de operadoras via FTP/SFTP, com detecção automática de formato.

**Ator Principal:** `sistema` (Job agendado) ou `usuario_autenticado` (importação manual)
**Tipo:** `crud`
**Impacta Dados:** `true`

**Pré-condições:**
- Conexão FTP configurada
- Credenciais válidas
- Permissão: `BIL.BILHETES.IMPORT` (se manual)

**Gatilho:** Job Hangfire executado diariamente às 02:00 ou usuário clica em "Importar Agora"

**Fluxo Principal (FP-UC01):**
1. **FP-UC01-001**: Sistema conecta ao servidor FTP/SFTP
2. **FP-UC01-002**: Sistema lista arquivos novos (não processados)
3. **FP-UC01-003**: Sistema detecta formato (Vivo, Claro, TIM, Oi) via parser automático
4. **FP-UC01-004**: Sistema baixa arquivo
5. **FP-UC01-005**: Sistema valida integridade (checksum MD5)
6. **FP-UC01-006**: Sistema parseia arquivo conforme formato detectado
7. **FP-UC01-007**: Sistema normaliza números para E.164
8. **FP-UC01-008**: Sistema detecta números premium (0900, 0300)
9. **FP-UC01-009**: Sistema detecta roaming internacional
10. **FP-UC01-010**: Sistema salva bilhetes em lote (bulk insert)
11. **FP-UC01-011**: Sistema marca arquivo como processado
12. **FP-UC01-012**: Sistema registra auditoria da importação
13. **FP-UC01-013**: Sistema envia notificação SignalR ao usuário

**Fluxos Alternativos (FA-UC01):**
- **FA-UC01-001**: Arquivo é PDF digitalizado → Sistema dispara OCR (UC05)
- **FA-UC01-002**: Formato não detectado → Sistema registra erro e envia alerta

**Fluxos de Exceção (FE-UC01):**
- **FE-UC01-001**: Falha na conexão FTP → Retry 3x com backoff exponencial
- **FE-UC01-002**: Checksum inválido → Rejeita arquivo, registra alerta

**Regras de Negócio:** RN-BIL-039-01, RN-BIL-039-02, RN-BIL-039-03, RN-BIL-039-04, RN-BIL-039-05

**Critérios de Aceite:**
- [ ] Conecta em FTP/SFTP com credenciais seguras
- [ ] Detecta automaticamente formato de 4 operadoras principais
- [ ] Normaliza 100% dos números para E.164
- [ ] Detecta números premium e roaming
- [ ] Registra auditoria completa da importação

---

## UC02 — Visualizar Detalhes do Bilhete

**Descrição:** Permite visualizar todos os detalhes de um bilhete específico.

**Ator Principal:** `usuario_autenticado`
**Tipo:** `leitura`
**Impacta Dados:** `false`

**Pré-condições:**
- Usuário autenticado
- Permissão: `BIL.BILHETES.VIEW`

**Gatilho:** Usuário clica em um bilhete na lista

**Fluxo Principal (FP-UC02):**
1. **FP-UC02-001**: Usuário seleciona um bilhete
2. **FP-UC02-002**: Sistema valida permissão e tenant
3. **FP-UC02-003**: Sistema carrega dados completos do bilhete
4. **FP-UC02-004**: Sistema carrega anomalias detectadas (se houver)
5. **FP-UC02-005**: Sistema exibe modal/página de detalhes

**Fluxos de Exceção (FE-UC02):**
- **FE-UC02-001**: Bilhete não encontrado → HTTP 404
- **FE-UC02-002**: Usuário sem permissão → HTTP 403

**Regras de Negócio:** RN-BIL-039-13

**Critérios de Aceite:**
- [ ] Exibe todos os campos do bilhete
- [ ] Mostra anomalias detectadas (se houver)

---

## UC03 — Editar Bilhete

**Descrição:** Permite correção manual de dados de um bilhete importado (casos excepcionais).

**Ator Principal:** `usuario_autenticado`
**Tipo:** `crud`
**Impacta Dados:** `true`

**Pré-condições:**
- Usuário autenticado
- Permissão: `BIL.BILHETES.UPDATE`

**Gatilho:** Usuário clica em "Editar" no detalhe do bilhete

**Fluxo Principal (FP-UC03):**
1. **FP-UC03-001**: Usuário solicita edição
2. **FP-UC03-002**: Sistema valida permissão e estado do bilhete
3. **FP-UC03-003**: Sistema exibe formulário pré-preenchido
4. **FP-UC03-004**: Usuário altera campos permitidos (Observação, Centro de Custo)
5. **FP-UC03-005**: Sistema atualiza registro
6. **FP-UC03-006**: Sistema registra auditoria

**Fluxos de Exceção (FE-UC03):**
- **FE-UC03-001**: Validação falha → HTTP 400
- **FE-UC03-002**: Usuário sem permissão → HTTP 403

**Regras de Negócio:** RN-BIL-039-14

**Critérios de Aceite:**
- [ ] Apenas campos permitidos são editáveis
- [ ] Auditoria registra alteração completa

---

## UC04 — Excluir Bilhete (Lógico)

**Descrição:** Permite exclusão lógica de um bilhete (soft delete).

**Ator Principal:** `usuario_autenticado`
**Tipo:** `crud`
**Impacta Dados:** `true`

**Pré-condições:**
- Usuário autenticado
- Permissão: `BIL.BILHETES.DELETE`

**Gatilho:** Usuário clica em "Excluir"

**Fluxo Principal (FP-UC04):**
1. **FP-UC04-001**: Usuário solicita exclusão
2. **FP-UC04-002**: Sistema exibe confirmação
3. **FP-UC04-003**: Sistema marca como excluído (soft delete)
4. **FP-UC04-004**: Sistema registra auditoria

**Regras de Negócio:** RN-BIL-039-14

**Critérios de Aceite:**
- [ ] Exclusão é lógica (flag IsDeleted)
- [ ] Auditoria registra exclusão

---

## UC05 — Processar OCR em PDF Digitalizado

**Descrição:** Processa PDF digitalizado via OCR para extrair dados do bilhete.

**Ator Principal:** `sistema` (Job automático)
**Tipo:** `acao`
**Impacta Dados:** `true`

**Gatilho:** Sistema detecta PDF digitalizado após importação

**Fluxo Principal (FP-UC05):**
1. **FP-UC05-001**: Sistema detecta PDF digitalizado
2. **FP-UC05-002**: Sistema enfileira job de OCR (Hangfire)
3. **FP-UC05-003**: Job executa OCR (Tesseract ou Azure Cognitive Services)
4. **FP-UC05-004**: Job extrai texto e aplica regex
5. **FP-UC05-005**: Job cria registro de bilhete com dados extraídos
6. **FP-UC05-006**: Job marca confiança (0-100%)

**Fluxos Alternativos (FA-UC05):**
- **FA-UC05-001**: Confiança < 70% → Marca bilhete para revisão manual

**Regras de Negócio:** RN-BIL-039-05, RN-BIL-039-15

**Critérios de Aceite:**
- [ ] OCR processa PDFs escaneados
- [ ] Calcula confiança (0-100%)
- [ ] Marca para revisão se confiança < 70%

---

## UC06 — Detectar Anomalias via ML

**Descrição:** Detecta anomalias em bilhetes usando Machine Learning (Isolation Forest).

**Ator Principal:** `sistema` (Job agendado)
**Tipo:** `acao`
**Impacta Dados:** `true`

**Gatilho:** Job Hangfire executado diariamente às 04:00

**Fluxo Principal (FP-UC06):**
1. **FP-UC06-001**: Job carrega bilhetes do mês atual
2. **FP-UC06-002**: Job extrai features: valor, duração, horário, tipo de chamada
3. **FP-UC06-003**: Job aplica modelo ML (Isolation Forest)
4. **FP-UC06-004**: Job identifica outliers (anomaly score < -0.5)
5. **FP-UC06-005**: Job marca bilhetes como "Anomalia"
6. **FP-UC06-006**: Job envia alerta para gestores

**Regras de Negócio:** RN-BIL-039-06, RN-BIL-039-07

**Critérios de Aceite:**
- [ ] Detecta anomalias usando ML
- [ ] Classifica tipo de anomalia
- [ ] Envia alertas aos gestores

---

## UC07 — Comparar com Plano Contratado

**Descrição:** Compara consumo de bilhetes com plano contratado.

**Ator Principal:** `sistema` (Job) ou `usuario_autenticado`
**Tipo:** `acao`
**Impacta Dados:** `false`

**Fluxo Principal (FP-UC07):**
1. **FP-UC07-001**: Sistema carrega plano contratado
2. **FP-UC07-002**: Sistema soma consumo do período
3. **FP-UC07-003**: Sistema calcula excedente
4. **FP-UC07-004**: Sistema gera recomendação (Manter, Upgrade, Downgrade)

**Regras de Negócio:** RN-BIL-039-08, RN-BIL-039-09

**Critérios de Aceite:**
- [ ] Calcula consumo total do período
- [ ] Gera recomendação automática

---

## UC08 — Alocar Custos por Centro de Custo

**Descrição:** Aloca custos de bilhetes automaticamente por centro de custo.

**Ator Principal:** `sistema` (Job agendado)
**Tipo:** `acao`
**Impacta Dados:** `true`

**Fluxo Principal (FP-UC08):**
1. **FP-UC08-001**: Job carrega bilhetes sem alocação
2. **FP-UC08-002**: Job identifica linha/ramal
3. **FP-UC08-003**: Job busca usuário vinculado à linha
4. **FP-UC08-004**: Job busca centro de custo do usuário
5. **FP-UC08-005**: Job aloca custo do bilhete ao centro de custo

**Regras de Negócio:** RN-BIL-039-10, RN-BIL-039-11

**Critérios de Aceite:**
- [ ] Aloca 100% dos bilhetes com linha/usuário válido
- [ ] Registra auditoria da alocação

---

## UC09 — Gerar Relatório de Consumo

**Descrição:** Gera relatórios analíticos de consumo de telecom.

**Ator Principal:** `usuario_autenticado`
**Tipo:** `leitura`
**Impacta Dados:** `false`

**Fluxo Principal (FP-UC09):**
1. **FP-UC09-001**: Usuário acessa tela de relatórios
2. **FP-UC09-002**: Sistema exibe filtros
3. **FP-UC09-003**: Sistema executa query agregada
4. **FP-UC09-004**: Sistema gera gráficos (pizza, barras, linha)

**Regras de Negócio:** RN-BIL-039-13

**Critérios de Aceite:**
- [ ] Relatório agrega dados corretamente
- [ ] Exportação para Excel e PDF

---

## UC10 — Exportar para ERP

**Descrição:** Exporta lançamentos de custos para ERP (SAP, TOTVS, Protheus).

**Ator Principal:** `sistema` (Job) ou `usuario_autenticado`
**Tipo:** `acao`
**Impacta Dados:** `true`

**Fluxo Principal (FP-UC10):**
1. **FP-UC10-001**: Sistema carrega bilhetes do mês anterior
2. **FP-UC10-002**: Sistema agrupa por centro de custo
3. **FP-UC10-003**: Sistema gera payload de integração
4. **FP-UC10-004**: Sistema envia para API do ERP
5. **FP-UC10-005**: Sistema marca bilhetes como exportados

**Regras de Negócio:** RN-BIL-039-12

**Critérios de Aceite:**
- [ ] Exporta corretamente para SAP, TOTVS, Protheus
- [ ] Registra auditoria completa

---

## UC11 — Consultar Histórico de Auditoria

**Descrição:** Permite consultar histórico completo de auditoria de um bilhete.

**Ator Principal:** `usuario_autenticado`
**Tipo:** `leitura`
**Impacta Dados:** `false`

**Fluxo Principal (FP-UC11):**
1. **FP-UC11-001**: Usuário solicita histórico
2. **FP-UC11-002**: Sistema carrega todos os registros de auditoria
3. **FP-UC11-003**: Sistema exibe timeline cronológica

**Regras de Negócio:** RN-BIL-039-14

**Critérios de Aceite:**
- [ ] Exibe todos os eventos de auditoria
- [ ] Mostra dados antes/depois (diff)

---

## UC12 — Dashboard de Bilhetes

**Descrição:** Exibe dashboard executivo com KPIs e gráficos.

**Ator Principal:** `usuario_autenticado`
**Tipo:** `leitura`
**Impacta Dados:** `false`

**Fluxo Principal (FP-UC12):**
1. **FP-UC12-001**: Usuário acessa dashboard
2. **FP-UC12-002**: Sistema calcula KPIs do mês atual
3. **FP-UC12-003**: Sistema gera gráficos

**Regras de Negócio:** RN-BIL-039-13

**Critérios de Aceite:**
- [ ] Exibe 6 KPIs principais
- [ ] Gráficos visuais e interativos

---

## UC13 — Aprovar Glosa de Bilhete

**Descrição:** Permite gestor aprovar ou rejeitar glosa de bilhete.

**Ator Principal:** `gestor_autenticado`
**Tipo:** `acao`
**Impacta Dados:** `true`

**Fluxo Principal (FP-UC13):**
1. **FP-UC13-001**: Gestor visualiza detalhes da glosa
2. **FP-UC13-002**: Gestor clica em "Aprovar" ou "Rejeitar"
3. **FP-UC13-003**: Sistema exige justificativa
4. **FP-UC13-004**: Sistema atualiza status da glosa
5. **FP-UC13-005**: Sistema registra auditoria

**Regras de Negócio:** RN-BIL-039-14, RN-BIL-039-15

**Critérios de Aceite:**
- [ ] Gestor pode aprovar ou rejeitar
- [ ] Justificativa obrigatória

---

## UC14 — Job: Processar Importações Pendentes

**Descrição:** Job agendado que processa importações de arquivos FTP.

**Ator Principal:** `sistema` (Hangfire)
**Tipo:** `batch`
**Impacta Dados:** `true`

**Gatilho:** Execução agendada diariamente às 02:00

**Fluxo Principal (FP-UC14):**
1. **FP-UC14-001**: Job conecta ao servidor FTP
2. **FP-UC14-002**: Job lista arquivos novos
3. **FP-UC14-003**: Job processa cada arquivo (UC01)
4. **FP-UC14-004**: Job envia resumo por e-mail

**Regras de Negócio:** RN-BIL-039-04

---

## UC15 — Job: Enviar Alertas de Anomalias

**Descrição:** Job agendado que envia alertas de anomalias detectadas.

**Ator Principal:** `sistema` (Hangfire)
**Tipo:** `batch`
**Impacta Dados:** `false`

**Gatilho:** Execução agendada diariamente às 08:00

**Fluxo Principal (FP-UC15):**
1. **FP-UC15-001**: Job carrega anomalias das últimas 24h
2. **FP-UC15-002**: Job gera relatório
3. **FP-UC15-003**: Job envia e-mail para gestores

**Regras de Negócio:** RN-BIL-039-07

---

## Mapeamento de Cobertura

| Requisito | Casos de Uso |
|-----------|--------------|
| RN-BIL-039-01 (E.164) | UC00, UC01 |
| RN-BIL-039-02 (Premium) | UC01 |
| RN-BIL-039-03 (Roaming) | UC01 |
| RN-BIL-039-04 (Parser) | UC01, UC14 |
| RN-BIL-039-05 (OCR) | UC05 |
| RN-BIL-039-06 (ML) | UC06 |
| RN-BIL-039-07 (Alertas) | UC06, UC15 |
| RN-BIL-039-08 (Comparação Plano) | UC07 |
| RN-BIL-039-09 (Recomendação) | UC07 |
| RN-BIL-039-10 (Alocação) | UC08 |
| RN-BIL-039-11 (Rateio) | UC08 |
| RN-BIL-039-12 (ERP) | UC10 |
| RN-BIL-039-13 (Multi-tenancy) | UC00, UC02, UC09, UC12 |
| RN-BIL-039-14 (Auditoria) | UC03, UC04, UC11, UC13 |
| RN-BIL-039-15 (Workflow) | UC05, UC13 |

**Cobertura:** 15/15 regras de negócio = **100%**

---

## Histórico de Versões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Agência ALC | Versão inicial (formato antigo) |
| 2.0 | 2025-12-31 | Agência ALC | Reescrita completa seguindo template padrão, 16 UCs, 100% cobertura |

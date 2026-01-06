# UC-RF036 — Casos de Uso Canônicos

**RF:** RF036 — Gestão de Custos Fixos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC007-FIN - Financeiro Processos
**Fase:** Fase 4 - Financeiro II - Processos

---

## 1. Objetivo deste Documento

Este documento define os **Casos de Uso Canônicos** do [RF036 — Gestão de Custos Fixos](./RF036.md), descrevendo **como o usuário interage** com o sistema para gerenciar despesas recorrentes mensais (custos fixos) com provisionamento automático, controle de variações orçamentárias, detecção de anomalias e análise de tendências.

Os casos de uso cobrem **100% das funcionalidades e regras de negócio** definidas no RF036, garantindo rastreabilidade completa entre requisito funcional e comportamento esperado do sistema.

---

## 2. Sumário de Casos de Uso

| UC | Nome | Tipo | Complexidade | Cobertura RF |
|----|------|------|--------------|--------------|
| UC00 | Listar Custos Fixos | Leitura | Média | RN-RF036-13 |
| UC01 | Criar Custo Fixo | Escrita | Alta | RN-RF036-01, 08, 09, 10, 13 |
| UC02 | Visualizar Custo Fixo | Leitura | Baixa | RN-RF036-13 |
| UC03 | Editar Custo Fixo | Escrita | Média | RN-RF036-01, 08, 09, 10, 13 |
| UC04 | Inativar Custo Fixo | Escrita | Baixa | RN-RF036-10, 13 |
| UC05 | Provisionar Custos Fixos (Job) | Job | Alta | RN-RF036-02, 10, 13 |
| UC06 | Registrar Valor Realizado | Escrita | Alta | RN-RF036-03, 04, 05, 07, 12, 13 |
| UC07 | Aprovar Lançamento | Escrita | Média | RN-RF036-05, 12, 13 |
| UC08 | Configurar Rateio | Escrita | Média | RN-RF036-06, 13 |
| UC09 | Dashboard de Custos Fixos | Leitura | Alta | RN-RF036-13 |
| UC10 | Projeção de Custos | Leitura | Média | RN-RF036-02, 08, 13 |

**Total:** 11 casos de uso cobrindo **13 regras de negócio**.

---

## 3. Padrões Gerais

Todos os casos de uso seguem os seguintes padrões obrigatórios:

### 3.1 Multi-Tenancy

- Todas as operações **filtram automaticamente** por `FornecedorId` do usuário autenticado.
- Tentativa de acesso a custo fixo de outro Fornecedor → **HTTP 404**.
- **RN-RF036-13** aplicada em TODOS os UCs.

### 3.2 Auditoria

- Todas as operações de **CREATE, UPDATE, DELETE** geram registros de auditoria.
- Campos auditados: `UsuarioCriacaoId`, `DataCriacao`, `UsuarioAlteracaoId`, `DataAlteracao`.

### 3.3 Permissões RBAC

| Operação | Permissão |
|----------|-----------|
| Visualizar | `GES.CUSTOS_FIXOS.VIEW` |
| Criar | `GES.CUSTOS_FIXOS.CREATE` |
| Editar | `GES.CUSTOS_FIXOS.UPDATE` |
| Excluir | `GES.CUSTOS_FIXOS.DELETE` |
| Aprovar | `GES.CUSTOS_FIXOS.APROVAR` |
| Provisionar manualmente | `GES.CUSTOS_FIXOS.PROVISIONAR` |
| Exportar | `GES.CUSTOS_FIXOS.EXPORT` |

### 3.4 Soft Delete

- Exclusões são **lógicas** (`FlExcluido = true`).
- Registros excluídos **não aparecem** em listagens padrão.

### 3.5 Validações

- Campos obrigatórios ausentes → **HTTP 400** com mensagem específica.
- Tipos de dados incorretos → **HTTP 400**.
- Violação de regras de negócio → **HTTP 400** com detalhes.

---

## 4. Casos de Uso Detalhados

---

### UC00 — Listar Custos Fixos

#### Objetivo

Permitir ao usuário listar todos os custos fixos cadastrados com filtros, ordenação e paginação.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.VIEW`.

#### Pós-condições

- Lista de custos fixos exibida conforme filtros aplicados.
- Apenas custos do Fornecedor do usuário são retornados.

#### Fluxo Principal

1. Usuário acessa tela de "Custos Fixos".
2. Sistema lista custos fixos com:
   - Paginação (padrão: 20 registros por página).
   - Colunas: Descrição, Tipo, Valor Orçado, Data Início, Data Fim, Fornecedor, Status.
3. Sistema permite filtros:
   - Por tipo de custo.
   - Por fornecedor.
   - Por status (Ativo, Inativo, Suspenso, Cancelado).
   - Por período (Data Início).
4. Sistema permite ordenação por qualquer coluna.
5. Usuário visualiza lista filtrada.

#### Fluxos Alternativos

**FA-UC00-01: Nenhum custo fixo encontrado**
- Passo 2: Sistema exibe mensagem "Nenhum custo fixo encontrado".

#### Fluxos de Exceção

**FE-UC00-01: Usuário sem permissão**
- Passo 1: Sistema retorna **HTTP 403** com mensagem "Acesso negado".

#### Regras de Negócio Aplicadas

- **RN-RF036-13**: Isolamento multi-tenant por FornecedorId.

#### Critérios de Aceite

- ✅ Apenas custos do Fornecedor do usuário são exibidos.
- ✅ Filtros funcionam corretamente.
- ✅ Paginação retorna registros conforme limite especificado.
- ✅ Ordenação funciona em todas as colunas.

---

### UC01 — Criar Custo Fixo

#### Objetivo

Permitir ao usuário cadastrar um novo custo fixo mensal com informações obrigatórias e opcionais.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.CREATE`.

#### Pós-condições

- Custo fixo criado no banco de dados.
- Status inicial = **Ativo**.
- Registro auditado (UsuarioCriacaoId, DataCriacao).
- Se Data Início ≤ hoje → custo elegível para provisionamento automático.

#### Fluxo Principal

1. Usuário acessa tela de "Custos Fixos" e clica em "Novo Custo Fixo".
2. Sistema exibe formulário com campos:
   - **Descrição*** (obrigatório, máx. 500 caracteres).
   - **Tipo de Custo*** (dropdown: Aluguel, Suporte, Licença, Energia, Internet, Telefonia, Outros).
   - **Valor Orçado Mensal*** (obrigatório, decimal > 0).
   - **Data Início*** (obrigatório, data ≤ hoje).
   - **Data Fim** (opcional, se informada: > Data Início).
   - **Fornecedor** (dropdown, opcional).
   - **Contrato** (dropdown, opcional).
   - **Status*** (dropdown: Ativo, Inativo, Suspenso, Cancelado - padrão: Ativo).
   - **Observações** (texto livre, opcional).
3. Usuário preenche formulário e clica em "Salvar".
4. Sistema valida:
   - Campos obrigatórios preenchidos (**RN-RF036-01**).
   - Descrição ≤ 500 caracteres (**RN-RF036-01**).
   - Valor Orçado > 0 (**RN-RF036-01**).
   - Data Início ≤ hoje (**RN-RF036-01**).
   - Data Fim > Data Início (se informada) (**RN-RF036-08**).
   - Fornecedor e Contrato pertencem ao mesmo FornecedorId (se informados) (**RN-RF036-09**).
5. Sistema cria custo fixo com:
   - FornecedorId do usuário autenticado (**RN-RF036-13**).
   - Status informado (padrão: Ativo) (**RN-RF036-10**).
   - UsuarioCriacaoId = usuário autenticado.
   - DataCriacao = agora.
6. Sistema exibe mensagem de sucesso e redireciona para listagem.

#### Fluxos Alternativos

**FA-UC01-01: Usuário cancela criação**
- Passo 3: Usuário clica em "Cancelar".
- Sistema descarta dados e volta para listagem.

#### Fluxos de Exceção

**FE-UC01-01: Campo obrigatório ausente**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Campo [Nome do Campo] é obrigatório".

**FE-UC01-02: Descrição excede 500 caracteres**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Descrição não pode exceder 500 caracteres".

**FE-UC01-03: Valor Orçado ≤ 0**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Valor Orçado deve ser maior que zero".

**FE-UC01-04: Data Início futura**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Data de Início não pode ser futura".

**FE-UC01-05: Data Fim < Data Início**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Data Fim deve ser posterior à Data Início".

**FE-UC01-06: Fornecedor de outro Fornecedor**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Fornecedor não pertence ao seu Fornecedor".

#### Regras de Negócio Aplicadas

- **RN-RF036-01**: Campos obrigatórios (Descricao, TipoCustoFixoId, ValorOrcadoMensal, DataInicio, Status).
- **RN-RF036-08**: Data Fim opcional mas validada (> Data Início).
- **RN-RF036-09**: Vinculação a fornecedor e contrato (validação de FornecedorId).
- **RN-RF036-10**: Status do custo fixo (enum válido).
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Custo fixo criado com sucesso se todas validações passarem.
- ✅ FornecedorId do usuário autenticado é atribuído automaticamente.
- ✅ Validações retornam HTTP 400 com mensagens específicas.
- ✅ Auditoria registrada corretamente (UsuarioCriacaoId, DataCriacao).

---

### UC02 — Visualizar Custo Fixo

#### Objetivo

Permitir ao usuário visualizar detalhes completos de um custo fixo específico, incluindo lançamentos históricos e projeções.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.VIEW`.
- Custo fixo existe e pertence ao FornecedorId do usuário.

#### Pós-condições

- Detalhes do custo fixo exibidos.
- Histórico de lançamentos exibido (últimos 12 meses).
- Projeção de custos futuros exibida (próximos 3 meses).

#### Fluxo Principal

1. Usuário clica em custo fixo na listagem.
2. Sistema valida:
   - Custo fixo pertence ao FornecedorId do usuário (**RN-RF036-13**).
3. Sistema exibe:
   - **Dados principais**: Descrição, Tipo, Valor Orçado, Data Início, Data Fim, Fornecedor, Contrato, Status, Observações.
   - **Histórico de lançamentos**: Últimos 12 meses com Mês Referência, Valor Provisionado, Valor Realizado, Variação %, Status, Justificativa (se houver).
   - **Gráfico de evolução**: Comparação Valor Orçado x Valor Realizado (últimos 12 meses).
   - **Projeção futura**: Próximos 3 meses com valores estimados (baseado em histórico).
   - **Auditoria**: Criado por, em, Última alteração por, em.
4. Usuário visualiza informações.

#### Fluxos Alternativos

Nenhum.

#### Fluxos de Exceção

**FE-UC02-01: Custo fixo não encontrado ou de outro Fornecedor**
- Passo 2: Sistema retorna **HTTP 404** com mensagem "Custo fixo não encontrado".

#### Regras de Negócio Aplicadas

- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Detalhes completos exibidos corretamente.
- ✅ Histórico de lançamentos carregado.
- ✅ Gráfico de evolução renderizado.
- ✅ Tentativa de acesso a custo de outro Fornecedor retorna HTTP 404.

---

### UC03 — Editar Custo Fixo

#### Objetivo

Permitir ao usuário alterar informações de um custo fixo existente.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.UPDATE`.
- Custo fixo existe e pertence ao FornecedorId do usuário.

#### Pós-condições

- Custo fixo atualizado no banco de dados.
- Registro auditado (UsuarioAlteracaoId, DataAlteracao).
- Se status mudou para "Ativo" → custo elegível para provisionamento futuro.
- Se status mudou para "Inativo/Cancelado" → provisionamento automático para.

#### Fluxo Principal

1. Usuário acessa tela de visualização de custo fixo e clica em "Editar".
2. Sistema exibe formulário preenchido com dados atuais:
   - Descrição, Tipo, Valor Orçado, Data Início, Data Fim, Fornecedor, Contrato, Status, Observações.
3. Usuário altera campos desejados e clica em "Salvar".
4. Sistema valida:
   - Campos obrigatórios preenchidos (**RN-RF036-01**).
   - Descrição ≤ 500 caracteres (**RN-RF036-01**).
   - Valor Orçado > 0 (**RN-RF036-01**).
   - Data Início ≤ hoje (**RN-RF036-01**).
   - Data Fim > Data Início (se informada) (**RN-RF036-08**).
   - Fornecedor e Contrato pertencem ao mesmo FornecedorId (se informados) (**RN-RF036-09**).
5. Sistema atualiza custo fixo com:
   - UsuarioAlteracaoId = usuário autenticado.
   - DataAlteracao = agora.
6. Sistema exibe mensagem de sucesso.

#### Fluxos Alternativos

**FA-UC03-01: Usuário cancela edição**
- Passo 3: Usuário clica em "Cancelar".
- Sistema descarta alterações e volta para visualização.

#### Fluxos de Exceção

**FE-UC03-01: Campo obrigatório ausente**
- Passo 4: Sistema retorna **HTTP 400** com mensagem: "Campo [Nome do Campo] é obrigatório".

**FE-UC03-02: Validações diversas (mesmas de UC01)**
- Passo 4: Sistema retorna **HTTP 400** conforme violação.

**FE-UC03-03: Custo fixo não encontrado ou de outro Fornecedor**
- Passo 1: Sistema retorna **HTTP 404**.

#### Regras de Negócio Aplicadas

- **RN-RF036-01**: Campos obrigatórios.
- **RN-RF036-08**: Data Fim validada.
- **RN-RF036-09**: Vinculação a fornecedor/contrato.
- **RN-RF036-10**: Status do custo fixo.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Custo fixo atualizado com sucesso se validações passarem.
- ✅ Auditoria registrada (UsuarioAlteracaoId, DataAlteracao).
- ✅ Validações retornam HTTP 400 com mensagens específicas.

---

### UC04 — Inativar Custo Fixo

#### Objetivo

Permitir ao usuário inativar um custo fixo, interrompendo provisionamento automático futuro.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.UPDATE`.
- Custo fixo existe, pertence ao FornecedorId do usuário e tem status "Ativo".

#### Pós-condições

- Status do custo fixo = **Inativo**.
- Provisionamento automático NÃO cria mais lançamentos futuros para este custo.
- Lançamentos históricos permanecem inalterados.
- Registro auditado (UsuarioAlteracaoId, DataAlteracao).

#### Fluxo Principal

1. Usuário acessa tela de visualização de custo fixo e clica em "Inativar".
2. Sistema exibe confirmação: "Tem certeza que deseja inativar este custo fixo? Lançamentos futuros não serão mais provisionados automaticamente."
3. Usuário confirma.
4. Sistema atualiza:
   - Status = **Inativo** (**RN-RF036-10**).
   - UsuarioAlteracaoId = usuário autenticado.
   - DataAlteracao = agora.
5. Sistema exibe mensagem de sucesso: "Custo fixo inativado com sucesso".

#### Fluxos Alternativos

**FA-UC04-01: Usuário cancela inativação**
- Passo 3: Usuário clica em "Cancelar".
- Sistema descarta ação e mantém status atual.

#### Fluxos de Exceção

**FE-UC04-01: Custo fixo não encontrado ou de outro Fornecedor**
- Passo 1: Sistema retorna **HTTP 404**.

**FE-UC04-02: Custo fixo já está inativo**
- Passo 1: Sistema retorna **HTTP 400** com mensagem "Custo fixo já está inativo".

#### Regras de Negócio Aplicadas

- **RN-RF036-10**: Status do custo fixo (transição para Inativo).
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Status alterado para "Inativo" com sucesso.
- ✅ Provisionamento automático NÃO cria lançamentos futuros.
- ✅ Lançamentos históricos permanecem intactos.
- ✅ Auditoria registrada.

---

### UC05 — Provisionar Custos Fixos (Job Automático)

#### Objetivo

Executar job automático mensal que cria lançamentos de custos fixos ativos para o mês corrente.

#### Pré-condições

- Job configurado para executar no **1º dia útil do mês**.
- Existem custos fixos com Status = **Ativo**.

#### Pós-condições

- Lançamentos criados para todos os custos fixos elegíveis.
- Cada lançamento tem:
  - Status = **Provisionado**.
  - Valor Provisionado = Valor Realizado do mês anterior OU Valor Orçado (se primeiro lançamento).
  - FlProvisionamentoAutomatico = **true**.
- Notificações enviadas aos responsáveis.
- Log de execução do job registrado.

#### Fluxo Principal

1. Sistema inicia job no 1º dia útil do mês (ex: 01/01/2026).
2. Sistema consulta custos fixos com:
   - Status = **Ativo** (**RN-RF036-10**).
   - DataInicio ≤ data atual (**RN-RF036-02**).
   - (DataFim IS NULL OU DataFim ≥ data atual) (**RN-RF036-02**).
   - FornecedorId = todos os Fornecedores (processamento global).
3. Para cada custo fixo elegível:
   - Sistema verifica se já existe lançamento para o mês corrente:
     - Se SIM → pula (evita duplicatas - idempotência).
     - Se NÃO → continua.
   - Sistema busca lançamento do mês anterior (mesmo CustoFixoId):
     - Se encontrado → Valor Provisionado = Valor Realizado do mês anterior.
     - Se NÃO encontrado → Valor Provisionado = Valor Orçado do custo fixo.
   - Sistema cria lançamento com:
     - CustoFixoId.
     - MesReferencia = mês corrente (ex: 2026-01).
     - ValorProvisionado = calculado acima.
     - Status = **Provisionado**.
     - FlProvisionamentoAutomatico = **true**.
     - FornecedorId = mesmo do custo fixo (**RN-RF036-13**).
     - UsuarioCriacaoId = ID do sistema (job).
     - DataCriacao = agora.
4. Sistema envia notificação ao responsável de cada custo fixo: "Lançamento de [Descrição] provisionado para [Mês/Ano] no valor de R$ [Valor]".
5. Sistema registra log de execução: "Provisionamento mensal concluído: [N] lançamentos criados".

#### Fluxos Alternativos

**FA-UC05-01: Nenhum custo fixo elegível**
- Passo 2: Sistema não encontra custos fixos elegíveis.
- Sistema registra log: "Nenhum custo fixo elegível para provisionamento".
- Job finaliza com sucesso.

#### Fluxos de Exceção

**FE-UC05-01: Erro ao criar lançamento**
- Passo 3: Sistema encontra erro ao criar lançamento (ex: violação de constraint).
- Sistema registra erro no log.
- Sistema continua processando próximo custo fixo (não bloqueia job inteiro).

#### Regras de Negócio Aplicadas

- **RN-RF036-02**: Provisionamento automático mensal.
- **RN-RF036-10**: Apenas custos com Status = Ativo são provisionados.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Job executado no 1º dia útil do mês.
- ✅ Apenas custos Ativos são provisionados.
- ✅ Custos com DataInicio > hoje NÃO são provisionados.
- ✅ Custos com DataFim < hoje NÃO são provisionados.
- ✅ Valor provisionado = valor realizado mês anterior OU valor orçado.
- ✅ FlProvisionamentoAutomatico = true em todos os lançamentos criados.
- ✅ Job é idempotente (executar 2x não cria duplicatas).

---

### UC06 — Registrar Valor Realizado

#### Objetivo

Permitir ao usuário informar o valor efetivamente realizado de um lançamento provisionado, com validação automática de variação orçamentária e detecção de anomalias.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.UPDATE`.
- Lançamento existe, pertence ao FornecedorId do usuário e tem Status = **Provisionado**.

#### Pós-condições

- Valor Realizado registrado no lançamento.
- Variação orçamentária calculada automaticamente.
- Se variação ≥10% → Alerta emitido (**RN-RF036-03**).
- Se variação ≥20% → Justificativa obrigatória (**RN-RF036-04**).
- Se variação ≥30% → Status = **Aguardando Aprovação** (**RN-RF036-05**).
- Detecção de anomalias executada (**RN-RF036-07**).
- Registro auditado.

#### Fluxo Principal

1. Usuário acessa lançamento com Status = **Provisionado** e clica em "Registrar Valor Realizado".
2. Sistema exibe formulário:
   - **Valor Realizado*** (obrigatório, decimal > 0).
   - **Justificativa** (obrigatório SE variação >20%).
   - **Data Realização*** (obrigatório, data ≤ hoje).
3. Usuário preenche Valor Realizado e clica em "Salvar".
4. Sistema calcula:
   - **Variação %** = |ValorRealizado - ValorOrcado| / ValorOrcado × 100 (**RN-RF036-03**).
5. Sistema valida:
   - **SE variação ≥20%** E Justificativa ausente → **HTTP 400** (**RN-RF036-04**).
   - Justificativa (se presente) ≥ 10 caracteres (**RN-RF036-04**).
6. Sistema atualiza lançamento:
   - ValorRealizado = valor informado.
   - Justificativa = texto informado (se aplicável).
   - DataRealizacao = data informada.
   - UsuarioAlteracaoId = usuário autenticado.
   - DataAlteracao = agora.
7. Sistema determina novo Status:
   - **SE variação <30%** → Status = **Realizado**.
   - **SE variação ≥30%** → Status = **Aguardando Aprovação** + RequereAprovacaoGerencial = **true** (**RN-RF036-05**).
8. Sistema executa detecção de anomalias (**RN-RF036-07**):
   - Busca últimos 6 meses de lançamentos realizados do mesmo CustoFixoId.
   - **SE histórico < 3 meses** → pula detecção.
   - Calcula média e desvio padrão (σ).
   - **SE ValorRealizado > média + (2 × σ)**:
     - FlAnomalia = **true**.
     - DescricaoAnomalia = "Valor R$ [X] acima do padrão histórico (média R$ [Y], σ R$ [Z])".
     - Envia alerta: "Anomalia detectada em [Descrição] - Mês [Mês/Ano]".
9. Sistema emite alerta de variação orçamentária:
   - **SE variação ≥10% e <20%** → Alerta Informativo.
   - **SE variação ≥20% e <30%** → Alerta de Aviso (warning).
   - **SE variação ≥30%** → Alerta Crítico + notifica gestor para aprovação.
10. Sistema exibe mensagem de sucesso.

#### Fluxos Alternativos

**FA-UC06-01: Usuário cancela registro**
- Passo 3: Usuário clica em "Cancelar".
- Sistema descarta dados e volta para visualização.

#### Fluxos de Exceção

**FE-UC06-01: Variação >20% sem justificativa**
- Passo 5: Sistema retorna **HTTP 400** com mensagem: "Variação superior a 20% requer justificativa obrigatória".

**FE-UC06-02: Justificativa < 10 caracteres**
- Passo 5: Sistema retorna **HTTP 400** com mensagem: "Justificativa deve ter no mínimo 10 caracteres".

**FE-UC06-03: Lançamento já possui Status = Pago**
- Passo 1: Sistema retorna **HTTP 400** com mensagem: "Lançamentos com status Pago não podem ser editados" (**RN-RF036-12**).

**FE-UC06-04: Lançamento não encontrado ou de outro Fornecedor**
- Passo 1: Sistema retorna **HTTP 404**.

#### Regras de Negócio Aplicadas

- **RN-RF036-03**: Alertas de variação orçamentária (3 níveis).
- **RN-RF036-04**: Justificativa obrigatória para variações >20%.
- **RN-RF036-05**: Aprovação gerencial para variações >30%.
- **RN-RF036-07**: Detecção automática de anomalias.
- **RN-RF036-12**: Bloqueio de edição de lançamentos pagos.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Valor Realizado registrado com sucesso.
- ✅ Variação calculada automaticamente.
- ✅ Alerta emitido conforme nível de variação (10%, 20%, 30%).
- ✅ Justificativa obrigatória SE variação >20%.
- ✅ Status = "Aguardando Aprovação" SE variação >30%.
- ✅ Detecção de anomalias executada (SE histórico ≥3 meses).
- ✅ Lançamentos pagos NÃO podem ser editados.

---

### UC07 — Aprovar Lançamento

#### Objetivo

Permitir a um gestor aprovar ou reprovar lançamentos que ultrapassaram variação orçamentária de 30%.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.APROVAR`.
- Lançamento existe, pertence ao FornecedorId do usuário e tem Status = **Aguardando Aprovação**.

#### Pós-condições

- **SE aprovado**: Status = **Aprovado** + AprovadoPor = usuário autenticado.
- **SE reprovado**: Status = **Cancelado** + MotivoReprovacao registrado.
- Registro auditado.
- Notificação enviada ao responsável do custo fixo.

#### Fluxo Principal

1. Usuário acessa lançamento com Status = **Aguardando Aprovação**.
2. Sistema exibe:
   - Dados do lançamento: Custo Fixo, Mês Referência, Valor Orçado, Valor Realizado, Variação %, Justificativa.
   - Botões: **Aprovar** | **Reprovar**.
3. Usuário clica em "Aprovar".
4. Sistema confirma: "Tem certeza que deseja aprovar este lançamento?".
5. Usuário confirma.
6. Sistema atualiza:
   - Status = **Aprovado** (**RN-RF036-05**).
   - AprovadoPor = usuário autenticado.
   - DataAprovacao = agora.
   - UsuarioAlteracaoId = usuário autenticado.
   - DataAlteracao = agora.
7. Sistema envia notificação ao responsável do custo fixo: "Lançamento de [Descrição] - [Mês/Ano] aprovado por [Nome Gestor]".
8. Sistema exibe mensagem de sucesso: "Lançamento aprovado com sucesso".

#### Fluxos Alternativos

**FA-UC07-01: Usuário reprova lançamento**
- Passo 3: Usuário clica em "Reprovar".
- Sistema exibe campo: **Motivo da Reprovação*** (obrigatório, ≥10 caracteres).
- Usuário preenche motivo e confirma.
- Sistema atualiza:
  - Status = **Cancelado** (**RN-RF036-05**).
  - MotivoReprovacao = texto informado.
  - ReprovadoPor = usuário autenticado.
  - DataReprovacao = agora.
- Sistema envia notificação ao responsável: "Lançamento de [Descrição] - [Mês/Ano] reprovado por [Nome Gestor]. Motivo: [Texto]".
- Sistema exibe mensagem: "Lançamento reprovado com sucesso".

**FA-UC07-02: Usuário cancela ação**
- Passo 5: Usuário clica em "Cancelar".
- Sistema descarta ação e mantém status atual.

#### Fluxos de Exceção

**FE-UC07-01: Usuário sem permissão**
- Passo 1: Sistema retorna **HTTP 403** com mensagem "Acesso negado".

**FE-UC07-02: Lançamento não está aguardando aprovação**
- Passo 1: Sistema retorna **HTTP 400** com mensagem "Lançamento não está aguardando aprovação".

**FE-UC07-03: Motivo de reprovação < 10 caracteres**
- FA-UC07-01: Sistema retorna **HTTP 400** com mensagem "Motivo de reprovação deve ter no mínimo 10 caracteres".

**FE-UC07-04: Lançamento já está pago**
- Passo 1: Sistema retorna **HTTP 400** com mensagem "Lançamentos com status Pago não podem ser editados" (**RN-RF036-12**).

#### Regras de Negócio Aplicadas

- **RN-RF036-05**: Aprovação gerencial para variações >30%.
- **RN-RF036-12**: Bloqueio de edição de lançamentos pagos.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Apenas usuários com permissão `GES.CUSTOS_FIXOS.APROVAR` podem aprovar.
- ✅ Aprovação altera Status para "Aprovado".
- ✅ Reprovação altera Status para "Cancelado" com motivo obrigatório.
- ✅ Notificação enviada ao responsável do custo fixo.
- ✅ Lançamentos pagos NÃO podem ser aprovados/reprovados.

---

### UC08 — Configurar Rateio

#### Objetivo

Permitir ao usuário configurar distribuição percentual de um custo fixo entre múltiplos centros de custo.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.UPDATE`.
- Custo fixo existe e pertence ao FornecedorId do usuário.

#### Pós-condições

- Itens de rateio criados/atualizados.
- Soma dos percentuais = 100% (**RN-RF036-06**).
- Registro auditado.

#### Fluxo Principal

1. Usuário acessa tela de visualização de custo fixo e clica em "Configurar Rateio".
2. Sistema exibe formulário com grid de rateio:
   - Colunas: Centro de Custo, Percentual (%).
   - Botões: **Adicionar Linha** | **Remover Linha**.
3. Usuário adiciona linhas:
   - Seleciona Centro de Custo (dropdown - apenas do mesmo FornecedorId).
   - Informa Percentual (decimal, 0 < x ≤ 100).
4. Usuário clica em "Salvar".
5. Sistema valida:
   - Ao menos 1 item de rateio (**RN-RF036-06**).
   - Cada item tem Percentual > 0 e ≤ 100 (**RN-RF036-06**).
   - Soma dos percentuais = 100% (**RN-RF036-06**).
   - Cada Centro de Custo pertence ao mesmo FornecedorId (**RN-RF036-06**).
6. Sistema salva itens de rateio com:
   - CustoFixoId.
   - CentroCustoId.
   - Percentual.
   - FornecedorId = mesmo do custo fixo.
   - UsuarioCriacaoId = usuário autenticado.
   - DataCriacao = agora.
7. Sistema exibe mensagem de sucesso: "Rateio configurado com sucesso".

#### Fluxos Alternativos

**FA-UC08-01: Usuário remove rateio existente**
- Passo 1: Usuário acessa formulário e remove todas as linhas.
- Sistema permite salvar sem itens de rateio (rateio é opcional).

**FA-UC08-02: Usuário cancela configuração**
- Passo 4: Usuário clica em "Cancelar".
- Sistema descarta alterações.

#### Fluxos de Exceção

**FE-UC08-01: Soma dos percentuais ≠ 100%**
- Passo 5: Sistema retorna **HTTP 400** com mensagem: "A soma dos percentuais deve ser exatamente 100%".

**FE-UC08-02: Percentual ≤ 0 ou > 100**
- Passo 5: Sistema retorna **HTTP 400** com mensagem: "Percentual deve ser maior que 0 e no máximo 100".

**FE-UC08-03: Centro de Custo de outro Fornecedor**
- Passo 5: Sistema retorna **HTTP 400** com mensagem: "Centro de Custo não pertence ao seu Fornecedor".

#### Regras de Negócio Aplicadas

- **RN-RF036-06**: Rateio multi-dimensional com soma = 100%.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Rateio configurado com sucesso se soma = 100%.
- ✅ Validação bloqueia soma ≠ 100%.
- ✅ Apenas centros de custo do mesmo FornecedorId são permitidos.
- ✅ Rateio é opcional (pode ser removido completamente).

---

### UC09 — Dashboard de Custos Fixos

#### Objetivo

Exibir visão consolidada dos custos fixos com KPIs, gráficos e análises comparativas.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.VIEW`.
- Existem custos fixos e lançamentos no FornecedorId do usuário.

#### Pós-condições

- Dashboard exibido com dados atualizados.

#### Fluxo Principal

1. Usuário acessa menu "Custos Fixos > Dashboard".
2. Sistema exibe:
   - **KPIs**:
     - Total de Custos Fixos Ativos.
     - Total Orçado (mês corrente).
     - Total Realizado (mês corrente).
     - Variação % (Total Realizado vs Total Orçado).
   - **Top 10 Maiores Custos Fixos** (ordenado por Valor Orçado DESC).
   - **Gráfico de Evolução Mensal por Categoria** (últimos 12 meses):
     - Eixo X: Mês.
     - Eixo Y: Valor Total.
     - Séries: Aluguel, Suporte, Licença, Energia, Internet, Telefonia, Outros.
   - **Análise Year-over-Year (YoY)**:
     - Comparação do mês corrente com mesmo mês do ano anterior.
     - Ex: Janeiro/2026 vs Janeiro/2025.
     - Mostra variação absoluta (R$) e percentual (%).
   - **Ranking de Maiores Variações** (Top 5 custos com maior variação % no mês corrente).
   - **Alertas Ativos**:
     - Lançamentos com variação >30% aguardando aprovação.
     - Anomalias detectadas no mês corrente.
     - Vencimentos próximos (7, 3, 1 dia).
3. Usuário visualiza dashboard.

#### Fluxos Alternativos

**FA-UC09-01: Nenhum dado disponível**
- Passo 2: Sistema exibe mensagem: "Nenhum custo fixo encontrado para exibir no dashboard".

#### Fluxos de Exceção

Nenhum.

#### Regras de Negócio Aplicadas

- **RN-RF036-13**: Isolamento multi-tenant (apenas dados do FornecedorId do usuário).

#### Critérios de Aceite

- ✅ Dashboard carrega dados apenas do Fornecedor do usuário.
- ✅ KPIs calculados corretamente.
- ✅ Gráficos renderizados com dados dos últimos 12 meses.
- ✅ Análise YoY compara mês atual com mesmo mês do ano anterior.
- ✅ Alertas exibidos em tempo real.

---

### UC10 — Projeção de Custos

#### Objetivo

Projetar valores futuros de custos fixos para os próximos 3, 6 ou 12 meses, considerando recorrência e sazonalidade.

#### Pré-condições

- Usuário autenticado.
- Usuário possui permissão `GES.CUSTOS_FIXOS.VIEW`.
- Existem custos fixos ativos no FornecedorId do usuário.

#### Pós-condições

- Projeção de custos exibida em formato de tabela e gráfico.

#### Fluxo Principal

1. Usuário acessa menu "Custos Fixos > Projeção de Custos".
2. Sistema exibe filtros:
   - **Período de Projeção** (dropdown: 3 meses, 6 meses, 12 meses - padrão: 3 meses).
   - **Categoria** (dropdown: Todas, Aluguel, Suporte, etc.).
3. Usuário seleciona período e clica em "Gerar Projeção".
4. Sistema calcula projeção:
   - Para cada custo fixo ativo:
     - **SE DataFim < período projetado** → NÃO incluir meses após DataFim (**RN-RF036-08**).
     - **SE Status = Ativo** E DataInicio ≤ mês projetado:
       - Valor Projetado = média dos últimos 3 meses realizados OU Valor Orçado (se < 3 meses de histórico).
   - Agrupa por mês e categoria.
5. Sistema exibe:
   - **Tabela de Projeção**:
     - Colunas: Mês/Ano, Categoria, Valor Projetado, Quantidade de Custos.
   - **Gráfico de Barras**:
     - Eixo X: Mês/Ano.
     - Eixo Y: Valor Total Projetado.
     - Séries por categoria.
6. Usuário visualiza projeção.

#### Fluxos Alternativos

**FA-UC10-01: Usuário exporta projeção**
- Passo 6: Usuário clica em "Exportar para Excel".
- Sistema gera arquivo Excel com dados da projeção.
- Sistema inicia download.

#### Fluxos de Exceção

**FE-UC10-01: Nenhum custo fixo ativo**
- Passo 4: Sistema exibe mensagem: "Nenhum custo fixo ativo encontrado para projeção".

#### Regras de Negócio Aplicadas

- **RN-RF036-02**: Consideração de Status = Ativo para provisionamento futuro.
- **RN-RF036-08**: Data Fim limita projeção futura.
- **RN-RF036-13**: Isolamento multi-tenant.

#### Critérios de Aceite

- ✅ Projeção considera apenas custos ativos.
- ✅ Custos com DataFim < período projetado são excluídos após DataFim.
- ✅ Valor projetado = média dos últimos 3 meses OU Valor Orçado.
- ✅ Exportação para Excel funciona corretamente.

---

## 5. Matriz de Rastreabilidade

| Regra de Negócio | Casos de Uso Aplicados |
|------------------|-------------------------|
| RN-RF036-01 | UC01, UC03 |
| RN-RF036-02 | UC05, UC10 |
| RN-RF036-03 | UC06 |
| RN-RF036-04 | UC06 |
| RN-RF036-05 | UC06, UC07 |
| RN-RF036-06 | UC08 |
| RN-RF036-07 | UC06 |
| RN-RF036-08 | UC01, UC03, UC10 |
| RN-RF036-09 | UC01, UC03 |
| RN-RF036-10 | UC01, UC03, UC04, UC05 |
| RN-RF036-11 | (Dashboard - alertas automáticos) |
| RN-RF036-12 | UC06, UC07 |
| RN-RF036-13 | UC00, UC01, UC02, UC03, UC04, UC05, UC06, UC07, UC08, UC09, UC10 |

**Cobertura:** 13/13 regras de negócio cobertas (100%).

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-31 | Geração completa de UCs v2.0 conforme CONTRATO-GERACAO-DOCS-UC.md: 11 UCs cobrindo 13 RNs | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-18 | Versão inicial com 9 UCs em formato legado | Architect Agent |

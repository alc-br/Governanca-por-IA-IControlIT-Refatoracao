# UC-RF055 — Casos de Uso Canônicos

**RF:** RF055 — Gestão de Rateio de Custos
**Epic:** EPIC007-FIN - Financeiro Processos
**Fase:** Fase 4 - Financeiro II - Processos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## Índice

| UC | Nome | Tipo | Impacta Dados |
|----|------|------|---------------|
| [UC00](#uc00---listar-rateios) | Listar Rateios | Leitura | Não |
| [UC01](#uc01---criar-regra-de-rateio) | Criar Regra de Rateio | CRUD | Sim |
| [UC02](#uc02---visualizar-detalhes-de-rateio) | Visualizar Detalhes de Rateio | Leitura | Não |
| [UC03](#uc03---editar-regra-de-rateio) | Editar Regra de Rateio | CRUD | Sim |
| [UC04](#uc04---aprovar-rateio-processado) | Aprovar Rateio Processado | Ação | Sim |
| [UC05](#uc05---exportar-rateio-para-erp) | Exportar Rateio para ERP | Batch | Sim |
| [UC06](#uc06---simular-rateio) | Simular Rateio | Leitura | Não |
| [UC07](#uc07---dashboard-de-rateios) | Dashboard de Rateios | Leitura | Não |

---

## UC00 - Listar Rateios

### Objetivo
Permitir ao usuário visualizar e filtrar as regras de rateio cadastradas no sistema.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.view_any`

### Pós-condições
- Lista de rateios exibida conforme filtros aplicados
- Isolamento multi-tenant garantido (apenas rateios do Id_Conglomerado do usuário)

### Fluxo Principal

**FP-UC00-001**: Usuário acessa o menu "Financeiro > Rateio de Custos"

**FP-UC00-002**: Sistema valida permissão `rateio.view_any`

**FP-UC00-003**: Sistema carrega rateios do Id_Conglomerado do usuário logado

**FP-UC00-004**: Sistema aplica paginação (20 registros por página) e ordenação padrão (data de criação DESC)

**FP-UC00-005**: Sistema exibe grid com colunas:
- Nome da Regra
- Tipo (Fixo / Proporcional / Uso Real / Projeto)
- Critério (Centro de Custo / Departamento / Projeto)
- Status (Ativo / Inativo)
- Última Execução
- Ações (Visualizar, Editar, Inativar)

### Fluxos Alternativos

**FA-UC00-001**: Usuário aplica filtro por Nome
- Sistema recarrega lista filtrada por nome da regra (LIKE)

**FA-UC00-002**: Usuário aplica filtro por Tipo
- Sistema recarrega lista filtrada por tipo de rateio (Fixo / Proporcional / Uso Real / Projeto)

**FA-UC00-003**: Usuário aplica filtro por Status
- Sistema recarrega lista filtrada por status (Ativo / Inativo)

**FA-UC00-004**: Usuário ordena por coluna
- Sistema recarrega lista com nova ordenação

**FA-UC00-005**: Usuário navega entre páginas
- Sistema carrega próxima página mantendo filtros ativos

### Fluxos de Exceção

**FE-UC00-001**: Usuário sem permissão `rateio.view_any`
- Sistema exibe mensagem: "Acesso negado. Você não possui permissão para visualizar rateios."
- Sistema redireciona para página inicial

**FE-UC00-002**: Nenhum rateio cadastrado
- Sistema exibe estado vazio: "Nenhuma regra de rateio cadastrada. Clique em 'Nova Regra' para começar."

**FE-UC00-003**: Erro ao carregar dados
- Sistema exibe mensagem: "Erro ao carregar rateios. Tente novamente."
- Sistema registra erro em log estruturado

### Regras de Negócio

**RN-UC-00-001**: Apenas rateios do Id_Conglomerado do usuário podem ser exibidos (multi-tenant)

**RN-UC-00-002**: Paginação padrão: 20 registros por página

**RN-UC-00-003**: Ordenação padrão: Data de Criação DESC

### Critérios de Aceite

**CA-UC00-001**: Grid exibe apenas rateios do tenant do usuário

**CA-UC00-002**: Filtros por Nome, Tipo e Status funcionam corretamente

**CA-UC00-003**: Paginação funciona corretamente

**CA-UC00-004**: Estado vazio é exibido quando não há rateios cadastrados

**CA-UC00-005**: Mensagem de erro 403 é exibida para usuário sem permissão

---

## UC01 - Criar Regra de Rateio

### Objetivo
Permitir ao usuário criar uma nova regra de rateio de custos com validação de totalização 100%.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.create`

### Pós-condições
- Nova regra de rateio criada e salva no banco
- Auditoria registrada (usuário, data, IP)
- Regra disponível para execução mensal automática

### Fluxo Principal

**FP-UC01-001**: Usuário clica em "Nova Regra de Rateio"

**FP-UC01-002**: Sistema valida permissão `rateio.create`

**FP-UC01-003**: Sistema exibe formulário com campos:
- Nome da Regra* (texto, max 100 caracteres)
- Descrição (textarea, max 500 caracteres)
- Tipo de Rateio* (select: Fixo / Proporcional por Headcount / Uso Real / Projeto)
- Critério de Destino* (select: Centro de Custo / Departamento / Projeto)
- Regras de Distribuição* (grid dinâmico: Destino + Percentual/Quantidade)

**FP-UC01-004**: Usuário preenche campos obrigatórios

**FP-UC01-005**: Usuário adiciona regras de distribuição no grid (ex: TI 40%, RH 30%, Financeiro 30%)

**FP-UC01-006**: Usuário clica em "Salvar"

**FP-UC01-007**: Sistema valida dados (RN-UC-01-001 a RN-UC-01-005)

**FP-UC01-008**: Sistema cria registro na tabela `Rateio` com Status "Ativo"

**FP-UC01-009**: Sistema salva regras de distribuição na tabela `Rateio_Regra`

**FP-UC01-010**: Sistema registra auditoria (AuditLog)

**FP-UC01-011**: Sistema exibe mensagem: "Regra de rateio criada com sucesso!"

**FP-UC01-012**: Sistema redireciona para listagem

### Fluxos Alternativos

**FA-UC01-001**: Usuário clica em "Salvar e Criar Outro"
- Sistema salva regra e mantém formulário aberto (limpo)

**FA-UC01-002**: Usuário clica em "Cancelar"
- Sistema descarta alterações e retorna à listagem

**FA-UC01-003**: Usuário seleciona "Tipo: Proporcional por Headcount"
- Sistema exibe campo adicional: "Departamento Origem" (select)
- Sistema calcula automaticamente percentuais com base em número de colaboradores

**FA-UC01-004**: Usuário seleciona "Tipo: Uso Real"
- Sistema exibe campo adicional: "Métrica de Uso" (select: Horas Máquina / GB Armazenamento / Transações)

### Fluxos de Exceção

**FE-UC01-001**: Campos obrigatórios não preenchidos
- Sistema exibe mensagem: "Preencha todos os campos obrigatórios."
- Sistema destaca campos com erro

**FE-UC01-002**: Soma dos percentuais ≠ 100%
- Sistema exibe mensagem: "A soma dos percentuais deve ser exatamente 100%. Atual: {valor}%"
- Sistema impede salvamento

**FE-UC01-003**: Nome da regra duplicado (mesmo Id_Conglomerado)
- Sistema exibe mensagem: "Já existe uma regra com este nome."
- Sistema impede salvamento

**FE-UC01-004**: Destinos duplicados na distribuição
- Sistema exibe mensagem: "Destinos duplicados não são permitidos."
- Sistema impede salvamento

**FE-UC01-005**: Erro ao salvar no banco
- Sistema exibe mensagem: "Erro ao criar regra. Tente novamente."
- Sistema registra erro em log estruturado
- Sistema executa rollback da transação

### Regras de Negócio

**RN-UC-01-001**: Campo "Nome da Regra" é obrigatório e deve ser único no tenant

**RN-UC-01-002**: A soma dos percentuais de distribuição DEVE ser exatamente 100%

**RN-UC-01-003**: Tipo "Fixo": Usuário define percentuais manualmente

**RN-UC-01-004**: Tipo "Proporcional por Headcount": Sistema calcula percentuais automaticamente com base no número de colaboradores ativos

**RN-UC-01-005**: Tipo "Uso Real": Rateio baseado em métricas extraídas do sistema (horas máquina, GB armazenamento, transações)

**RN-UC-01-006**: Tipo "Projeto": Rateio vinculado a projetos específicos (requer integração com módulo de projetos)

**RN-UC-01-007**: Regras criadas ficam automaticamente com Status "Ativo"

**RN-UC-01-008**: Multi-tenant: Regra só pode referenciar destinos do mesmo Id_Conglomerado

### Critérios de Aceite

**CA-UC01-001**: Formulário exibe todos os campos obrigatórios com asterisco

**CA-UC01-002**: Validação de soma 100% impede salvamento se inválida

**CA-UC01-003**: Mensagem de sucesso é exibida após criação

**CA-UC01-004**: Auditoria registra corretamente usuário, data e IP

**CA-UC01-005**: Regra criada aparece na listagem (UC00)

**CA-UC01-006**: Destinos duplicados são bloqueados

**CA-UC01-007**: Nome duplicado é bloqueado

---

## UC02 - Visualizar Detalhes de Rateio

### Objetivo
Exibir informações detalhadas de uma regra de rateio, incluindo histórico de execuções e preview da distribuição.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.view`
- Rateio existe e pertence ao tenant do usuário

### Pós-condições
- Detalhes da regra exibidos
- Histórico de execuções exibido
- Preview de distribuição exibido

### Fluxo Principal

**FP-UC02-001**: Usuário clica em "Visualizar" em um rateio da listagem

**FP-UC02-002**: Sistema valida permissão `rateio.view`

**FP-UC02-003**: Sistema valida que o rateio pertence ao Id_Conglomerado do usuário

**FP-UC02-004**: Sistema exibe tela de detalhes com 3 seções:

**Seção 1: Informações da Regra**
- Nome da Regra
- Descrição
- Tipo de Rateio
- Critério de Destino
- Status (Ativo / Inativo)
- Data de Criação
- Criado por

**Seção 2: Regras de Distribuição**
- Grid com colunas: Destino | Percentual/Quantidade | Status

**Seção 3: Histórico de Execuções**
- Grid com colunas: Data Execução | Total Rateado | Status (Processado / Aprovado / Exportado / Erro) | Ações (Visualizar Detalhes)

**FP-UC02-005**: Sistema exibe botões de ação: "Editar", "Inativar", "Simular"

### Fluxos Alternativos

**FA-UC02-001**: Usuário clica em "Visualizar Detalhes" de uma execução
- Sistema exibe modal com detalhamento da execução: valores por destino, data/hora, usuário aprovador, arquivo de exportação (se exportado)

**FA-UC02-002**: Usuário clica em "Simular"
- Sistema redireciona para UC06 (Simular Rateio) com regra pré-selecionada

**FA-UC02-003**: Usuário clica em "Editar"
- Sistema redireciona para UC03 (Editar Regra de Rateio)

**FA-UC02-004**: Usuário clica em "Inativar"
- Sistema exibe confirmação: "Deseja realmente inativar esta regra?"
- Sistema altera Status para "Inativo" se confirmado
- Sistema registra auditoria

### Fluxos de Exceção

**FE-UC02-001**: Rateio não encontrado
- Sistema exibe mensagem: "Rateio não encontrado."
- Sistema redireciona para listagem

**FE-UC02-002**: Rateio pertence a outro tenant
- Sistema exibe mensagem: "Acesso negado."
- Sistema registra tentativa de acesso em log de segurança

**FE-UC02-003**: Usuário sem permissão `rateio.view`
- Sistema exibe mensagem: "Acesso negado."
- Sistema redireciona para página inicial

### Regras de Negócio

**RN-UC-02-001**: Apenas rateios do Id_Conglomerado do usuário podem ser visualizados

**RN-UC-02-002**: Histórico de execuções exibe últimas 12 execuções (1 ano)

**RN-UC-02-003**: Preview de distribuição calcula valores baseado no total do mês anterior

### Critérios de Aceite

**CA-UC02-001**: Todas as 3 seções são exibidas corretamente

**CA-UC02-002**: Histórico exibe execuções em ordem decrescente (mais recentes primeiro)

**CA-UC02-003**: Botões de ação estão habilitados/desabilitados conforme permissões

**CA-UC02-004**: Tentativa de acesso a rateio de outro tenant é bloqueada

---

## UC03 - Editar Regra de Rateio

### Objetivo
Permitir edição de regra de rateio com validação de não execução no mês corrente.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.update`
- Rateio existe e pertence ao tenant do usuário
- Rateio NÃO foi executado no mês corrente

### Pós-condições
- Regra de rateio atualizada
- Auditoria registrada
- Versão anterior preservada (histórico de alterações)

### Fluxo Principal

**FP-UC03-001**: Usuário clica em "Editar" na visualização de detalhes (UC02)

**FP-UC03-002**: Sistema valida permissões e pré-condições

**FP-UC03-003**: Sistema exibe formulário preenchido com dados atuais

**FP-UC03-004**: Usuário altera campos desejados (Nome, Descrição, Regras de Distribuição)

**FP-UC03-005**: Usuário clica em "Salvar"

**FP-UC03-006**: Sistema valida dados (mesmas validações do UC01)

**FP-UC03-007**: Sistema cria snapshot da versão anterior na tabela `Rateio_Historico`

**FP-UC03-008**: Sistema atualiza registro na tabela `Rateio`

**FP-UC03-009**: Sistema atualiza regras de distribuição na tabela `Rateio_Regra`

**FP-UC03-010**: Sistema registra auditoria

**FP-UC03-011**: Sistema exibe mensagem: "Regra de rateio atualizada com sucesso!"

**FP-UC03-012**: Sistema redireciona para visualização de detalhes

### Fluxos Alternativos

**FA-UC03-001**: Usuário clica em "Cancelar"
- Sistema descarta alterações e retorna à visualização

**FA-UC03-002**: Usuário clica em "Histórico de Alterações"
- Sistema exibe modal com snapshots anteriores (data, usuário, valores alterados)

### Fluxos de Exceção

**FE-UC03-001**: Rateio foi executado no mês corrente
- Sistema exibe mensagem: "Não é possível editar regras já executadas no mês corrente. Aguarde o próximo mês ou crie uma nova regra."
- Sistema desabilita edição

**FE-UC03-002**: Campos obrigatórios não preenchidos
- Sistema exibe mensagem de validação (mesma do UC01)

**FE-UC03-003**: Soma dos percentuais ≠ 100%
- Sistema exibe mensagem de validação (mesma do UC01)

**FE-UC03-004**: Erro ao salvar no banco
- Sistema exibe mensagem de erro
- Sistema executa rollback
- Sistema mantém versão anterior

### Regras de Negócio

**RN-UC-03-001**: **CRÍTICO**: Regra NÃO pode ser editada se foi executada no mês corrente (evita inconsistência)

**RN-UC-03-002**: Snapshot da versão anterior deve ser criado antes de atualizar

**RN-UC-03-003**: Histórico de alterações deve preservar: data, usuário, campos alterados (antes/depois)

**RN-UC-03-004**: Apenas Nome, Descrição e Regras de Distribuição podem ser editados

**RN-UC-03-005**: Tipo de Rateio NÃO pode ser alterado (criar nova regra se necessário)

**RN-UC-03-006**: Validações de UC01 (soma 100%, destinos únicos) se aplicam

### Critérios de Aceite

**CA-UC03-001**: Edição é bloqueada se regra foi executada no mês corrente

**CA-UC03-002**: Snapshot é criado corretamente antes da atualização

**CA-UC03-003**: Histórico de alterações exibe todas as versões anteriores

**CA-UC03-004**: Auditoria registra usuário que fez a edição

**CA-UC03-005**: Tipo de Rateio é somente leitura (campo desabilitado)

---

## UC04 - Aprovar Rateio Processado

### Objetivo
Permitir aprovação de rateio processado antes da exportação para ERP, com validação de variação acima de 10%.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.approve`
- Rateio executado com Status "PROCESSADO"
- Rateio pertence ao tenant do usuário

### Pós-condições
- Rateio aprovado com Status "APROVADO"
- Auditoria registrada (usuário aprovador, data, IP)
- Rateio liberado para exportação (UC05)

### Fluxo Principal

**FP-UC04-001**: Usuário acessa "Financeiro > Rateios Pendentes de Aprovação"

**FP-UC04-002**: Sistema valida permissão `rateio.approve`

**FP-UC04-003**: Sistema exibe grid com rateios PROCESSADOS:
- Data de Processamento
- Regra Aplicada
- Total Rateado
- Variação vs Mês Anterior
- Ações (Visualizar, Aprovar, Rejeitar)

**FP-UC04-004**: Usuário clica em "Visualizar" em um rateio

**FP-UC04-005**: Sistema exibe detalhes:
- Resumo: Total rateado, quantidade de destinos, data de processamento
- Grid de distribuição: Destino | Valor Rateado | Percentual | Variação vs Mês Anterior
- Comparativo mensal (gráfico)

**FP-UC04-006**: Usuário clica em "Aprovar"

**FP-UC04-007**: Sistema valida se variação > 10% em algum destino (RN-UC-04-001)

**FP-UC04-008**: Sistema atualiza Status para "APROVADO"

**FP-UC04-009**: Sistema registra usuário aprovador e data/hora de aprovação

**FP-UC04-010**: Sistema registra auditoria

**FP-UC04-011**: Sistema exibe mensagem: "Rateio aprovado com sucesso!"

**FP-UC04-012**: Sistema remove rateio da lista de pendentes

### Fluxos Alternativos

**FA-UC04-001**: Variação > 10% detectada
- Sistema exibe alerta: "ATENÇÃO: Variação superior a 10% detectada nos destinos: {lista}. Deseja continuar?"
- Se usuário confirmar: prossegue com aprovação (FP-UC04-008)
- Se usuário cancelar: retorna sem aprovar

**FA-UC04-002**: Usuário clica em "Rejeitar"
- Sistema exibe modal: "Motivo da Rejeição*" (textarea, obrigatório)
- Sistema atualiza Status para "REJEITADO"
- Sistema registra motivo e usuário que rejeitou
- Sistema exibe mensagem: "Rateio rejeitado. Será reprocessado no próximo ciclo."

**FA-UC04-003**: Usuário aprova múltiplos rateios em lote
- Sistema exibe checkbox de seleção múltipla
- Sistema exibe botão "Aprovar Selecionados"
- Sistema valida variações de todos os selecionados
- Sistema aprova em lote com confirmação única

### Fluxos de Exceção

**FE-UC04-001**: Usuário sem permissão `rateio.approve`
- Sistema exibe mensagem: "Acesso negado. Apenas Controllers podem aprovar rateios."
- Sistema redireciona para página inicial

**FE-UC04-002**: Rateio já foi aprovado por outro usuário
- Sistema exibe mensagem: "Este rateio já foi aprovado por {usuário} em {data}."
- Sistema atualiza listagem

**FE-UC04-003**: Erro ao salvar aprovação
- Sistema exibe mensagem: "Erro ao aprovar rateio. Tente novamente."
- Sistema executa rollback
- Sistema mantém Status "PROCESSADO"

### Regras de Negócio

**RN-UC-04-001**: **CRÍTICO**: Se variação > 10% em qualquer destino, sistema DEVE exibir alerta de confirmação obrigatório

**RN-UC-04-002**: Apenas usuários com permissão `rateio.approve` podem aprovar

**RN-UC-04-003**: Rateio só pode ser aprovado uma única vez (idempotência)

**RN-UC-04-004**: Rejeição exige motivo obrigatório (mínimo 10 caracteres)

**RN-UC-04-005**: Rateios rejeitados voltam para reprocessamento no próximo ciclo

**RN-UC-04-006**: Aprovação registra usuário aprovador, data/hora e IP

### Critérios de Aceite

**CA-UC04-001**: Alerta de variação > 10% é exibido corretamente

**CA-UC04-002**: Aprovação registra corretamente usuário e data/hora

**CA-UC04-003**: Rateio aprovado muda para Status "APROVADO"

**CA-UC04-004**: Rejeição exige motivo obrigatório

**CA-UC04-005**: Aprovação em lote funciona corretamente

**CA-UC04-006**: Apenas usuários com permissão `rateio.approve` acessam a tela

---

## UC05 - Exportar Rateio para ERP

### Objetivo
Exportar rateio aprovado para ERP externo (SAP, TOTVS, Conta Azul) em formato padronizado.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.export`
- Rateio com Status "APROVADO"
- Rateio pertence ao tenant do usuário
- Integração ERP configurada (credenciais, endpoint)

### Pós-condições
- Arquivo de exportação gerado (CSV ou XML)
- Rateio exportado com Status "EXPORTADO"
- Log de exportação registrado
- Auditoria registrada

### Fluxo Principal

**FP-UC05-001**: Usuário acessa "Financeiro > Rateios Aprovados"

**FP-UC05-002**: Sistema valida permissão `rateio.export`

**FP-UC05-003**: Sistema exibe grid com rateios APROVADOS:
- Data de Aprovação
- Regra Aplicada
- Total Rateado
- Ações (Visualizar, Exportar)

**FP-UC05-004**: Usuário seleciona um ou mais rateios

**FP-UC05-005**: Usuário clica em "Exportar"

**FP-UC05-006**: Sistema exibe modal de confirmação:
- Sistema ERP de destino (SAP / TOTVS / Conta Azul)
- Formato (CSV / XML)
- Data de Competência

**FP-UC05-007**: Usuário confirma exportação

**FP-UC05-008**: Sistema valida integração ERP configurada (RN-UC-05-001)

**FP-UC05-009**: Sistema gera arquivo de exportação conforme formato:

**Formato CSV:**
```
Centro Custo;Valor;Conta Contábil;Histórico
101;15000.00;4.01.001;Rateio TI - Dez/2025
102;10000.00;4.01.001;Rateio RH - Dez/2025
```

**Formato XML (SAP):**
```xml
<Rateio>
  <Item>
    <CentroCusto>101</CentroCusto>
    <Valor>15000.00</Valor>
    <ContaContabil>4.01.001</ContaContabil>
    <Historico>Rateio TI - Dez/2025</Historico>
  </Item>
</Rateio>
```

**FP-UC05-010**: Sistema envia arquivo via API REST para ERP (ou disponibiliza download se integração manual)

**FP-UC05-011**: Sistema atualiza Status para "EXPORTADO"

**FP-UC05-012**: Sistema registra log de exportação (data/hora, usuário, arquivo gerado, sistema destino)

**FP-UC05-013**: Sistema registra auditoria

**FP-UC05-014**: Sistema exibe mensagem: "Rateio exportado com sucesso! Arquivo: {nome_arquivo}"

### Fluxos Alternativos

**FA-UC05-001**: Integração ERP não configurada
- Sistema exibe mensagem: "Integração ERP não configurada. Configure em 'Configurações > Integrações'."
- Sistema disponibiliza download manual do arquivo CSV/XML

**FA-UC05-002**: Exportação manual (download de arquivo)
- Usuário clica em "Baixar Arquivo"
- Sistema gera arquivo CSV/XML
- Sistema inicia download no navegador
- Sistema marca Status como "EXPORTADO MANUALMENTE"

**FA-UC05-003**: Erro na API do ERP (timeout, credenciais inválidas)
- Sistema exibe mensagem: "Erro ao exportar para ERP: {mensagem_erro}"
- Sistema mantém Status "APROVADO"
- Sistema registra erro em log
- Sistema disponibiliza opção de "Tentar Novamente"

**FA-UC05-004**: Exportação em lote (múltiplos rateios)
- Sistema gera arquivo consolidado com todos os rateios selecionados
- Sistema envia via API ou disponibiliza download único

### Fluxos de Exceção

**FE-UC05-001**: Usuário sem permissão `rateio.export`
- Sistema exibe mensagem: "Acesso negado. Apenas Controllers podem exportar rateios."
- Sistema redireciona para página inicial

**FE-UC05-002**: Rateio já foi exportado
- Sistema exibe mensagem: "Este rateio já foi exportado em {data} por {usuário}."
- Sistema desabilita botão "Exportar"

**FE-UC05-003**: Erro ao gerar arquivo
- Sistema exibe mensagem: "Erro ao gerar arquivo de exportação. Tente novamente."
- Sistema registra erro em log

### Regras de Negócio

**RN-UC-05-001**: Integração ERP deve estar configurada (endpoint, credenciais, formato)

**RN-UC-05-002**: Arquivo CSV deve seguir layout padrão: Centro Custo; Valor; Conta Contábil; Histórico

**RN-UC-05-003**: Arquivo XML deve seguir schema XSD do ERP de destino

**RN-UC-05-004**: Histórico contábil deve conter: "Rateio {Regra} - {Mês/Ano}"

**RN-UC-05-005**: Exportação registra data/hora, usuário, arquivo gerado, sistema destino

**RN-UC-05-006**: Rateio só pode ser exportado uma única vez (evita duplicação contábil)

**RN-UC-05-007**: **CRÍTICO**: Arquivo exportado deve ser armazenado por 7 anos (compliance fiscal)

### Critérios de Aceite

**CA-UC05-001**: Arquivo CSV é gerado corretamente com todas as colunas

**CA-UC05-002**: Arquivo XML é gerado conforme schema do ERP

**CA-UC05-003**: Exportação via API funciona corretamente (SAP, TOTVS, Conta Azul)

**CA-UC05-004**: Download manual funciona quando integração não configurada

**CA-UC05-005**: Log de exportação registra todas as informações obrigatórias

**CA-UC05-006**: Arquivo exportado é armazenado no blob storage

**CA-UC05-007**: Exportação duplicada é bloqueada

---

## UC06 - Simular Rateio

### Objetivo
Simular execução de rateio antes do processamento real, exibindo preview da distribuição e impacto no orçamento.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.simulate`
- Regra de rateio existe e está ativa

### Pós-condições
- Preview de distribuição exibido
- Impacto no orçamento calculado
- NENHUMA alteração em dados reais (simulação é read-only)

### Fluxo Principal

**FP-UC06-001**: Usuário acessa "Financeiro > Simular Rateio"

**FP-UC06-002**: Sistema valida permissão `rateio.simulate`

**FP-UC06-003**: Sistema exibe formulário:
- Regra de Rateio* (select)
- Mês/Ano de Referência* (date picker, padrão: mês atual)
- Valor Total a Ratear* (number, padrão: valor do mês anterior)

**FP-UC06-004**: Usuário seleciona regra e define valor total

**FP-UC06-005**: Usuário clica em "Simular"

**FP-UC06-006**: Sistema calcula distribuição conforme tipo de rateio:
- **Fixo**: Aplica percentuais definidos
- **Proporcional**: Calcula baseado em headcount atual
- **Uso Real**: Busca métricas do período selecionado
- **Projeto**: Distribui conforme alocação de projetos

**FP-UC06-007**: Sistema exibe preview com 3 seções:

**Seção 1: Resumo**
- Total a Ratear
- Quantidade de Destinos
- Tipo de Rateio

**Seção 2: Distribuição Detalhada**
- Grid: Destino | Percentual | Valor | Variação vs Mês Anterior | Impacto Orçamento

**Seção 3: Gráficos**
- Gráfico pizza: Distribuição por destino
- Gráfico barras: Comparativo últimos 6 meses

**FP-UC06-008**: Sistema exibe botões: "Exportar PDF", "Exportar Excel", "Executar Rateio"

### Fluxos Alternativos

**FA-UC06-001**: Usuário clica em "Exportar PDF"
- Sistema gera PDF com preview de simulação
- Sistema inicia download

**FA-UC06-002**: Usuário clica em "Exportar Excel"
- Sistema gera planilha Excel com grid de distribuição
- Sistema inicia download

**FA-UC06-003**: Usuário clica em "Executar Rateio"
- Sistema exibe confirmação: "Confirma execução do rateio conforme simulado?"
- Se confirmado: Sistema executa rateio real (job mensal) e marca Status "PROCESSADO"
- Sistema exibe mensagem: "Rateio executado com sucesso!"

**FA-UC06-004**: Usuário altera valor total
- Sistema recalcula distribuição automaticamente
- Sistema atualiza preview

### Fluxos de Exceção

**FE-UC06-001**: Usuário sem permissão `rateio.simulate`
- Sistema exibe mensagem: "Acesso negado."
- Sistema redireciona para página inicial

**FE-UC06-002**: Regra de rateio inativa
- Sistema exibe mensagem: "Regra inativa não pode ser simulada."
- Sistema desabilita botão "Simular"

**FE-UC06-003**: Dados insuficientes para simulação (ex: métrica de uso não disponível)
- Sistema exibe mensagem: "Dados insuficientes para simular. Métricas do período não encontradas."
- Sistema sugere usar "Tipo: Fixo" ou aguardar dados

**FE-UC06-004**: Erro ao calcular distribuição
- Sistema exibe mensagem: "Erro ao simular rateio. Tente novamente."
- Sistema registra erro em log

### Regras de Negócio

**RN-UC-06-001**: **CRÍTICO**: Simulação é READ-ONLY (não altera dados reais)

**RN-UC-06-002**: Cálculo de variação usa último rateio APROVADO como base

**RN-UC-06-003**: Impacto no orçamento compara valor simulado vs valor orçado no período

**RN-UC-06-004**: Simulação de "Proporcional" usa headcount ATUAL (não do mês de referência)

**RN-UC-06-005**: Simulação de "Uso Real" busca métricas reais do período selecionado

**RN-UC-06-006**: Se não houver métricas, sistema usa média dos últimos 3 meses

### Critérios de Aceite

**CA-UC06-001**: Simulação NÃO altera dados reais (nenhum insert/update)

**CA-UC06-002**: Cálculos de distribuição estão corretos para todos os tipos de rateio

**CA-UC06-003**: Preview exibe variação vs mês anterior corretamente

**CA-UC06-004**: Impacto no orçamento é calculado corretamente

**CA-UC06-005**: Exportação PDF/Excel funciona corretamente

**CA-UC06-006**: Botão "Executar Rateio" só aparece se usuário tem permissão `rateio.execute`

---

## UC07 - Dashboard de Rateios

### Objetivo
Exibir visão consolidada de rateios aplicados, com análises de tendências, comparativos mensais e alertas de variação.

### Pré-condições
- Usuário autenticado
- Permissão: `rateio.view_dashboard`

### Pós-condições
- Dashboard exibido com dados do tenant do usuário
- Métricas calculadas em tempo real

### Fluxo Principal

**FP-UC07-001**: Usuário acessa "Financeiro > Dashboard de Rateios"

**FP-UC07-002**: Sistema valida permissão `rateio.view_dashboard`

**FP-UC07-003**: Sistema carrega dados do Id_Conglomerado do usuário

**FP-UC07-004**: Sistema exibe dashboard com 4 seções:

**Seção 1: Cards de Resumo (Mês Atual)**
- Total Rateado (R$)
- Quantidade de Rateios Executados
- Pendentes de Aprovação
- Exportados para ERP

**Seção 2: Gráficos**
- Gráfico Linha: Evolução Total Rateado (últimos 12 meses)
- Gráfico Pizza: Distribuição por Tipo de Rateio (Fixo, Proporcional, Uso Real, Projeto)
- Gráfico Barras: Top 10 Destinos (maiores valores rateados)

**Seção 3: Alertas**
- Lista de destinos com variação > 10% vs mês anterior (badge vermelho)
- Lista de rateios pendentes de aprovação > 5 dias (badge amarelo)
- Lista de rateios não exportados (badge laranja)

**Seção 4: Últimos Rateios Executados**
- Grid: Data | Regra | Total | Status | Ações (Visualizar)

**FP-UC07-005**: Sistema permite filtrar por período (mês/ano)

### Fluxos Alternativos

**FA-UC07-001**: Usuário aplica filtro de período
- Sistema recarrega dashboard com dados do período selecionado

**FA-UC07-002**: Usuário clica em um alerta
- Sistema redireciona para detalhes do rateio relacionado (UC02)

**FA-UC07-003**: Usuário clica em "Visualizar" em um rateio
- Sistema redireciona para UC02 (Visualizar Detalhes)

**FA-UC07-004**: Usuário exporta dashboard para PDF
- Sistema gera PDF com todos os gráficos e métricas
- Sistema inicia download

### Fluxos de Exceção

**FE-UC07-001**: Usuário sem permissão `rateio.view_dashboard`
- Sistema exibe mensagem: "Acesso negado."
- Sistema redireciona para página inicial

**FE-UC07-002**: Nenhum rateio executado no período
- Sistema exibe estado vazio: "Nenhum rateio executado neste período."

**FE-UC07-003**: Erro ao carregar dados
- Sistema exibe mensagem: "Erro ao carregar dashboard. Tente novamente."
- Sistema registra erro em log

### Regras de Negócio

**RN-UC-07-001**: Dashboard exibe apenas dados do Id_Conglomerado do usuário (multi-tenant)

**RN-UC-07-002**: Alertas de variação > 10% são exibidos em vermelho (prioridade alta)

**RN-UC-07-003**: Rateios pendentes de aprovação > 5 dias são exibidos em amarelo

**RN-UC-07-004**: Filtro de período padrão: Mês atual

**RN-UC-07-005**: Gráfico de evolução exibe últimos 12 meses completos

**RN-UC-07-006**: Top 10 destinos considera soma total dos últimos 12 meses

### Critérios de Aceite

**CA-UC07-001**: Cards de resumo exibem valores corretos do mês atual

**CA-UC07-002**: Gráficos são renderizados corretamente

**CA-UC07-003**: Alertas de variação > 10% são exibidos corretamente

**CA-UC07-004**: Filtro de período funciona corretamente

**CA-UC07-005**: Exportação PDF gera arquivo correto

**CA-UC07-006**: Dashboard é responsivo (funciona em mobile/tablet/desktop)

---

## Matriz de Rastreabilidade

| RF Item | Descrição | UCs que Cobrem |
|---------|-----------|----------------|
| RF-CRUD-01 | Criar regra de rateio | UC01 |
| RF-CRUD-02 | Listar regras de rateio | UC00 |
| RF-CRUD-03 | Visualizar detalhes de rateio | UC02 |
| RF-CRUD-04 | Editar regra de rateio | UC03 |
| RF-VAL-01 | Validar soma 100% | UC01, UC03 |
| RF-VAL-02 | Validar destinos únicos | UC01, UC03 |
| RF-VAL-03 | Validar não edição mês corrente | UC03 |
| RF-VAL-04 | Validar variação > 10% | UC04 |
| RF-SEC-01 | RBAC - view_any | UC00 |
| RF-SEC-02 | RBAC - create | UC01 |
| RF-SEC-03 | RBAC - update | UC03 |
| RF-SEC-04 | RBAC - approve | UC04 |
| RF-SEC-05 | RBAC - export | UC05 |
| RF-SEC-06 | RBAC - simulate | UC06 |
| RF-SEC-07 | RBAC - view_dashboard | UC07 |
| RF-INT-01 | Exportar para SAP | UC05 |
| RF-INT-02 | Exportar para TOTVS | UC05 |
| RF-INT-03 | Exportar para Conta Azul | UC05 |
| RF-PROC-01 | Job mensal automático | UC05, UC06 |
| RF-PROC-02 | Processamento em lote | UC05 |
| RF-REL-01 | Dashboard consolidado | UC07 |
| RF-REL-02 | Simulação de rateio | UC06 |

---

## Exclusões

### Itens do RF NÃO Cobertos por UCs

Não há itens funcionais do RF055.md que NÃO estejam cobertos pelos 8 Casos de Uso acima.

---

## Histórico de Versões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | Agência ALC | Versão inicial (formato resumido) |
| 2.0 | 2025-12-31 | Agência ALC | Migração para template v2.0 (detalhamento completo: FP/FA/FE, RN, CA, rastreabilidade) |

---

**Fim do Documento UC-RF055.md**

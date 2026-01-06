# UC-RF034 — Casos de Uso Canônicos

**RF:** RF034 — Gestão de Itens de Auditoria
**Epic:** EPIC010-AUD - Auditoria Avançada
**Fase:** Fase 6 - Ativos, Auditoria e Integrações
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF034 - Gestão de Itens de Auditoria**, cobrindo integralmente o comportamento funcional esperado para auditoria detalhada de bilhetes de telecomunicações.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF034.yaml)
- Massas de Teste (MT-RF034.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**Contexto de negócio:** Este RF trata da análise linha-a-linha de bilhetes de telecomunicações, comparando valores cobrados versus contratuais, identificando glosas (valores indevidos), classificando divergências por criticidade e preparando documentação para contestação formal junto às operadoras.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Itens de Auditoria | Auditor / Gestor Financeiro |
| UC01 | Criar Item de Auditoria | Auditor |
| UC02 | Visualizar Item de Auditoria | Auditor / Gestor Financeiro / Analista |
| UC03 | Editar Item de Auditoria | Auditor |
| UC04 | Excluir Item de Auditoria | Super Admin |
| UC05 | Aprovar/Contestar Item | Auditor / Gestor Financeiro |
| UC06 | Exportar para Contestação | Auditor / Gestor Financeiro |
| UC07 | Buscar e Filtrar Avançado | Auditor / Gestor Financeiro / Analista |
| UC08 | Gerar Relatórios Gerenciais | Gestor Financeiro |
| UC09 | Visualizar Dashboard de Glosas | Gestor Financeiro |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (FornecedorId)
- Todas as ações exigem **permissão explícita** conforme RBAC
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Todas as operações devem sincronizar automaticamente com Resumo de Auditoria (RF035)
- Cálculos de glosa devem respeitar precisão NUMERIC(13,8)
- Validações devem detectar inconsistências de unidade de consumo vs tipo de bilhete

---

## UC00 — Listar Itens de Auditoria

### Objetivo
Permitir que auditores e gestores visualizem itens auditados com filtros avançados por período, operadora, tipo de serviço, criticidade e status.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.VIEW`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Totalizadores exibidos (soma de glosas, quantidade de itens)

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa "Auditoria → Itens de Auditoria"
- **FP-UC00-002:** Sistema valida permissão AUD.ITENS.VIEW
- **FP-UC00-003:** Sistema carrega itens do tenant (Global Query Filter por FornecedorId)
- **FP-UC00-004:** Sistema aplica paginação (20 itens/página) e ordenação padrão (data DESC)
- **FP-UC00-005:** Sistema exibe grid com colunas: Lote, Bilhete, Ativo, Operadora, ValorCobrado, ValorCorreto, Glosa, Divergência%, Status
- **FP-UC00-006:** Sistema exibe totalizadores no rodapé: Total Glosa, Total Itens

### Fluxos Alternativos
- **FA-UC00-001:** Filtrar por Lote (AAAAMM)
  - Sistema valida formato do lote
  - Retorna itens do período
- **FA-UC00-002:** Filtrar por Operadora
  - Sistema lista operadoras ativas
  - Retorna itens da operadora selecionada
- **FA-UC00-003:** Filtrar por Criticidade (Crítica >10%, Alta 5-10%, Média 1-5%, Baixa <1%)
  - Sistema calcula percentual de divergência
  - Retorna itens na faixa selecionada
- **FA-UC00-004:** Ordenar por coluna (Glosa, Divergência, Data)
  - Sistema reordena resultados
- **FA-UC00-005:** Exportar lista filtrada para Excel/CSV
  - Sistema chama UC06

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 "Acesso negado"
- **FE-UC00-002:** Nenhum registro encontrado → Exibe estado vazio "Nenhum item auditado no período"
- **FE-UC00-003:** Filtro de lote inválido → HTTP 400 "Lote deve estar no formato AAAAMM"

### Regras de Negócio
- **RN-UC00-001:** Somente registros do tenant (FornecedorId = usuário logado)
- **RN-UC00-002:** Registros soft-deleted (FlExcluido=true) não aparecem
- **RN-UC00-003:** Paginação padrão: 20 registros/página
- **RN-UC00-004:** Divergência calculada como: ((ValorCobrado - ValorCorreto) / ValorCorreto) * 100
- **RN-UC00-005:** Destaque visual: Divergência >10% em vermelho, 5-10% em laranja, <5% em cinza

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado
- **CA-UC00-002:** Registros excluídos (FlExcluido=true) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (deep linking)
- **CA-UC00-006:** Totalizadores DEVEM refletir apenas registros filtrados (não total geral)
- **CA-UC00-007:** Performance: Lista de 10.000 itens DEVE carregar em <500ms

---

## UC01 — Criar Item de Auditoria

### Objetivo
Permitir criação de novo item de auditoria com validações automáticas de cálculo de glosa, classificação de divergência e sincronização com resumo.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.CREATE`
- Resumo de Auditoria (RF035) criado previamente
- Bilhete de telecomunicação existente

### Pós-condições
- Registro persistido
- Glosa calculada automaticamente
- Divergência classificada automaticamente
- Resumo sincronizado via Domain Event
- Auditoria registrada

### Fluxo Principal
- **FP-UC01-001:** Usuário solicita criação clicando em "Novo Item"
- **FP-UC01-002:** Sistema valida permissão AUD.ITENS.CREATE
- **FP-UC01-003:** Sistema exibe formulário com campos:
  - Resumo de Auditoria* (dropdown)
  - Bilhete* (lookup por número)
  - Ativo* (lookup por código)
  - Contrato* (dropdown)
  - Operadora* (dropdown)
  - Tipo de Bilhete* (dropdown)
  - Lote* (AAAAMM)
  - QuantidadeConsumo* (numeric)
  - UnidadeConsumo* (enum: Minutos, MegaBytes, SMS, Franquia)
  - ValorCobrado* (numeric 13,8)
  - ValorCorreto* (numeric 13,8)
  - Observações (text)
- **FP-UC01-004:** Usuário preenche campos obrigatórios
- **FP-UC01-005:** Sistema valida dados:
  - Resumo existe e ativo
  - Bilhete existe e ativo
  - Ativo existe e ativo
  - Lote no formato AAAAMM
  - QuantidadeConsumo > 0
  - ValorCobrado >= 0 e <= 8 casas decimais
  - ValorCorreto >= 0 e <= 8 casas decimais
  - UnidadeConsumo compatível com Tipo de Bilhete
- **FP-UC01-006:** Sistema calcula automaticamente:
  - ValorCobradoAMais = ValorCobrado - ValorCorreto
  - PercentualDivergencia = ((ValorCobrado - ValorCorreto) / ValorCorreto) * 100
- **FP-UC01-007:** Sistema classifica criticidade:
  - Divergência >10% → Crítica
  - Divergência 5-10% → Alta
  - Divergência 1-5% → Média
  - Divergência <1% → Baixa
- **FP-UC01-008:** Sistema cria registro com FornecedorId = usuário logado
- **FP-UC01-009:** Sistema dispara Domain Event: `AuditoriaItemCreated`
- **FP-UC01-010:** Handler sincroniza Resumo: incrementa TotalGlosa, QtdItens
- **FP-UC01-011:** Sistema registra auditoria (UsuarioCriacao, DataCriacao)
- **FP-UC01-012:** Sistema retorna HTTP 201 com ID do item criado
- **FP-UC01-013:** Sistema exibe mensagem: "Item de auditoria criado com sucesso. Glosa: R$ {valor}"

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro
  - Sistema mantém formulário aberto
  - Limpa campos (exceto Resumo e Lote)
- **FA-UC01-002:** Cancelar criação
  - Sistema descarta dados
  - Retorna para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Campo obrigatório ausente → HTTP 400 "Campo {nome} é obrigatório"
- **FE-UC01-002:** Resumo inexistente → HTTP 400 "Resumo de auditoria não encontrado"
- **FE-UC01-003:** Bilhete inexistente → HTTP 400 "Bilhete não encontrado"
- **FE-UC01-004:** Lote inválido → HTTP 400 "Lote deve estar no formato AAAAMM"
- **FE-UC01-005:** QuantidadeConsumo <= 0 → HTTP 400 "Quantidade deve ser maior que zero"
- **FE-UC01-006:** Valor com mais de 8 decimais → HTTP 400 "Máximo 8 casas decimais"
- **FE-UC01-007:** UnidadeConsumo incompatível com Tipo → HTTP 400 "Unidade incompatível com tipo de bilhete VOZ/DADOS/SMS"
- **FE-UC01-008:** Valor negativo → HTTP 400 "Valor não pode ser negativo"
- **FE-UC01-009:** Erro inesperado → HTTP 500 "Erro ao criar item de auditoria"

### Regras de Negócio
- **RN-UC01-001:** Campos obrigatórios: Resumo, Bilhete, Ativo, Contrato, Operadora, Tipo, Lote, Quantidade, Unidade, ValorCobrado, ValorCorreto
- **RN-UC01-002:** FornecedorId preenchido automaticamente com tenant do usuário
- **RN-UC01-003:** UsuarioCriacao e DataCriacao preenchidos automaticamente
- **RN-UC01-004:** Campo ValorCobradoAMais é somente leitura (calculado automaticamente)
- **RN-UC01-005:** Campo PercentualDivergencia é somente leitura (calculado automaticamente)
- **RN-UC01-006:** VOZ exige UnidadeConsumo=Minutos, DADOS exige MegaBytes, SMS exige SMS
- **RN-UC01-007:** Sincronização com Resumo via Domain Event (assíncrono)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** FornecedorId DEVE ser preenchido automaticamente com tenant do usuário autenticado
- **CA-UC01-003:** UsuarioCriacao DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC01-004:** DataCriacao DEVE ser preenchido automaticamente com timestamp UTC
- **CA-UC01-005:** ValorCobradoAMais DEVE ser calculado como (ValorCobrado - ValorCorreto) com precisão de 8 decimais
- **CA-UC01-006:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-007:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-008:** Resumo DEVE ser atualizado automaticamente via Domain Event
- **CA-UC01-009:** Notificação DEVE ser enviada se divergência >10% (crítica)

---

## UC02 — Visualizar Item de Auditoria

### Objetivo
Permitir visualização detalhada de um item auditado com histórico completo, relacionamentos e cálculos.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.VIEW`

### Pós-condições
- Dados exibidos corretamente com todos os relacionamentos

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona item na lista (clica em linha ou botão "Visualizar")
- **FP-UC02-002:** Sistema valida permissão AUD.ITENS.VIEW
- **FP-UC02-003:** Sistema valida tenant (item.FornecedorId == usuário logado)
- **FP-UC02-004:** Sistema carrega item com relacionamentos:
  - Resumo de Auditoria
  - Bilhete
  - Ativo
  - Contrato
  - Operadora
  - Tipo de Bilhete
- **FP-UC02-005:** Sistema exibe seções:
  - **Cabeçalho:** Lote, Status, Criticidade, Data Criação
  - **Identificação:** Resumo, Bilhete (número completo), Ativo (código + descrição)
  - **Valores:** ValorCobrado, ValorCorreto, Glosa (ValorCobradoAMais), Divergência%
  - **Consumo:** Quantidade, Unidade
  - **Relacionamentos:** Contrato, Operadora, Tipo de Bilhete
  - **Observações:** Texto livre
  - **Auditoria:** Criado por, Criado em, Alterado por, Alterado em
- **FP-UC02-006:** Sistema destaca visualmente:
  - Glosa positiva (cobrança a maior) em vermelho
  - Glosa negativa (cobrança a menor) em verde
  - Divergência crítica (>10%) com ícone de alerta

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar histórico de alterações
  - Sistema lista versões anteriores (se houver)
  - Exibe diff de valores
- **FA-UC02-002:** Exportar detalhes em PDF
  - Sistema gera PDF formatado
  - Inclui QR Code para rastreabilidade

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente → HTTP 404 "Item não encontrado"
- **FE-UC02-002:** Registro de outro tenant → HTTP 404 "Item não encontrado" (não vaza informação)
- **FE-UC02-003:** Resumo vinculado excluído → Exibe "(Resumo excluído)" mas mantém dados históricos

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant obrigatório
- **RN-UC02-002:** Informações de auditoria sempre visíveis
- **RN-UC02-003:** Relacionamentos excluídos exibem "(excluído)" mas mantêm histórico

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar registros do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (UsuarioCriacao, DataCriacao, UsuarioAlteracao, DataAlteracao)
- **CA-UC02-003:** Tentativa de acessar registro de outro tenant DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar registro inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Glosas DEVEM ser formatadas com 8 casas decimais
- **CA-UC02-007:** Divergências DEVEM ser formatadas como percentual com 2 casas decimais

---

## UC03 — Editar Item de Auditoria

### Objetivo
Permitir alteração controlada de item auditado com recálculo automático de glosa e sincronização com resumo.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.UPDATE`
- Item em status editável (não pode estar em "Recuperado")

### Pós-condições
- Registro atualizado
- Glosa recalculada
- Resumo sincronizado
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição clicando em "Editar"
- **FP-UC03-002:** Sistema valida permissão AUD.ITENS.UPDATE
- **FP-UC03-003:** Sistema valida que item não está em status "Recuperado"
- **FP-UC03-004:** Sistema carrega dados atuais em formulário
- **FP-UC03-005:** Usuário altera campos permitidos:
  - ValorCobrado
  - ValorCorreto
  - QuantidadeConsumo
  - UnidadeConsumo
  - Observações
- **FP-UC03-006:** Sistema valida alterações (mesmas regras de UC01)
- **FP-UC03-007:** Sistema recalcula:
  - ValorCobradoAMais = ValorCobrado - ValorCorreto
  - PercentualDivergencia = ((ValorCobrado - ValorCorreto) / ValorCorreto) * 100
- **FP-UC03-008:** Sistema reclassifica criticidade
- **FP-UC03-009:** Sistema persiste alterações
- **FP-UC03-010:** Sistema dispara Domain Event: `AuditoriaItemUpdated` com valores antes/depois
- **FP-UC03-011:** Handler recalcula totalizadores do Resumo
- **FP-UC03-012:** Sistema registra auditoria (UsuarioAlteracao, DataAlteracao, ValoresAntes, ValoresDepois)
- **FP-UC03-013:** Sistema retorna HTTP 200
- **FP-UC03-014:** Sistema exibe mensagem: "Item atualizado com sucesso. Nova glosa: R$ {valor}"

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição
  - Sistema descarta alterações
  - Retorna para visualização

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação (mesmas de UC01)
- **FE-UC03-002:** Item em status "Recuperado" → HTTP 400 "Item recuperado não pode ser editado"
- **FE-UC03-003:** Conflito de edição concorrente → HTTP 409 "Item foi modificado por outro usuário. Recarregue e tente novamente."
- **FE-UC03-004:** Registro de outro tenant → HTTP 404

### Regras de Negócio
- **RN-UC03-001:** UsuarioAlteracao e DataAlteracao preenchidos automaticamente
- **RN-UC03-002:** Campos não editáveis: FornecedorId, Resumo, Bilhete, Ativo, Contrato, Operadora, Tipo, Lote, DataCriacao, UsuarioCriacao
- **RN-UC03-003:** Recálculo de glosa automático ao alterar ValorCobrado ou ValorCorreto
- **RN-UC03-004:** Sincronização com Resumo via Domain Event (assíncrono)

### Critérios de Aceite
- **CA-UC03-001:** UsuarioAlteracao DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** DataAlteracao DEVE ser preenchida automaticamente com timestamp UTC
- **CA-UC03-003:** Apenas campos editáveis DEVEM ser permitidos para alteração
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (optimistic locking)
- **CA-UC03-005:** Tentativa de editar registro de outro tenant DEVE retornar HTTP 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior e novo estado (JSON)
- **CA-UC03-007:** Resumo DEVE ser sincronizado automaticamente

---

## UC04 — Excluir Item de Auditoria

### Objetivo
Permitir exclusão lógica de itens com sincronização automática de totalizadores.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.DELETE`

### Pós-condições
- Registro marcado como excluído (soft delete)
- Resumo sincronizado (totalizadores reduzidos)
- Auditoria registrada

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita exclusão clicando em "Excluir"
- **FP-UC04-002:** Sistema exibe confirmação: "Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita."
- **FP-UC04-003:** Usuário confirma
- **FP-UC04-004:** Sistema valida permissão AUD.ITENS.DELETE
- **FP-UC04-005:** Sistema valida que não há dependências bloqueantes (nenhuma neste caso)
- **FP-UC04-006:** Sistema executa soft delete: FlExcluido = true
- **FP-UC04-007:** Sistema registra: DataExclusao, UsuarioExclusao
- **FP-UC04-008:** Sistema dispara Domain Event: `AuditoriaItemDeleted`
- **FP-UC04-009:** Handler recalcula totalizadores do Resumo (reduz TotalGlosa, QtdItens)
- **FP-UC04-010:** Sistema registra auditoria
- **FP-UC04-011:** Sistema retorna HTTP 204
- **FP-UC04-012:** Sistema exibe mensagem: "Item excluído com sucesso"

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
  - Sistema fecha modal de confirmação
  - Nenhuma alteração é feita

### Fluxos de Exceção
- **FE-UC04-001:** Registro já excluído → HTTP 404 "Item não encontrado"
- **FE-UC04-002:** Registro de outro tenant → HTTP 404
- **FE-UC04-003:** Erro ao sincronizar resumo → HTTP 500 "Erro ao excluir item"

### Regras de Negócio
- **RN-UC04-001:** Exclusão sempre lógica (soft delete) via FlExcluido=true
- **RN-UC04-002:** Registro excluído não aparece em listagens (Global Query Filter)
- **RN-UC04-003:** Auditoria preserva dados completos do registro excluído

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via FlExcluido=true
- **CA-UC04-002:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-003:** DataExclusao DEVE ser preenchida com timestamp UTC
- **CA-UC04-004:** UsuarioExclusao DEVE ser preenchido com ID do usuário autenticado
- **CA-UC04-005:** Registro excluído NÃO deve aparecer em listagens padrão
- **CA-UC04-006:** Resumo DEVE ser sincronizado automaticamente (totais reduzidos)

---

## UC05 — Aprovar/Contestar Item

### Objetivo
Permitir transição de status do item conforme workflow de aprovação (pendente → análise → aprovado → contestado → recuperado).

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.UPDATE`

### Pós-condições
- Status atualizado
- Data e usuário da transição registrados
- Auditoria registrada

### Fluxo Principal
- **FP-UC05-001:** Usuário visualiza item (UC02)
- **FP-UC05-002:** Sistema exibe botões conforme status atual:
  - Pendente → [Aprovar] [Rejeitar]
  - Aprovado → [Contestar]
  - Contestado → [Marcar como Recuperado]
- **FP-UC05-003:** Usuário clica em botão de ação
- **FP-UC05-004:** Sistema valida permissão
- **FP-UC05-005:** Sistema valida transição permitida
- **FP-UC05-006:** Sistema solicita justificativa (obrigatória)
- **FP-UC05-007:** Usuário informa justificativa
- **FP-UC05-008:** Sistema atualiza:
  - Status → novo status
  - DataAprovacao / DataContestacao / DataRecuperacao
  - UsuarioAprovacao / UsuarioContestacao / UsuarioRecuperacao
  - Justificativa
- **FP-UC05-009:** Sistema registra auditoria
- **FP-UC05-010:** Sistema retorna HTTP 200
- **FP-UC05-011:** Sistema exibe mensagem: "Status atualizado para {status}"

### Fluxos Alternativos
- **FA-UC05-001:** Rejeitar item
  - Sistema marca status = Rejeitado
  - Item não entra em contestação
- **FA-UC05-002:** Cancelar ação
  - Sistema mantém status atual

### Fluxos de Exceção
- **FE-UC05-001:** Transição inválida → HTTP 400 "Transição de {statusAtual} para {statusNovo} não permitida"
- **FE-UC05-002:** Justificativa ausente → HTTP 400 "Justificativa é obrigatória"
- **FE-UC05-003:** Item em status final (Recuperado) → HTTP 400 "Item já está em status final"

### Regras de Negócio
- **RN-UC05-001:** Transições permitidas:
  - Pendente → Aprovado / Rejeitado
  - Aprovado → Contestado
  - Contestado → Recuperado
- **RN-UC05-002:** Justificativa obrigatória em todas as transições
- **RN-UC05-003:** Datas e usuários de transição registrados automaticamente

### Critérios de Aceite
- **CA-UC05-001:** Sistema DEVE validar transições permitidas
- **CA-UC05-002:** Justificativa DEVE ser obrigatória
- **CA-UC05-003:** Datas e usuários DEVEM ser preenchidos automaticamente
- **CA-UC05-004:** Auditoria DEVE registrar status anterior e novo

---

## UC06 — Exportar para Contestação

### Objetivo
Gerar documento estruturado (PDF, Excel, CSV) agrupado por operadora com itens aprovados para contestação formal.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.EXPORT`

### Pós-condições
- Arquivo gerado e disponibilizado para download
- Auditoria de exportação registrada

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa "Exportar para Contestação"
- **FP-UC06-002:** Sistema valida permissão AUD.ITENS.EXPORT
- **FP-UC06-003:** Sistema exibe filtros:
  - Lote
  - Operadora
  - Status (padrão: Aprovado)
  - Formato (PDF, Excel, CSV)
- **FP-UC06-004:** Usuário define filtros e formato
- **FP-UC06-005:** Sistema busca itens conforme filtros
- **FP-UC06-006:** Sistema agrupa por operadora
- **FP-UC06-007:** Sistema calcula subtotais por operadora
- **FP-UC06-008:** Sistema gera documento estruturado:
  - Cabeçalho: Data geração, Período, Empresa
  - Para cada Operadora:
    - Nome da operadora
    - Lista de itens (Bilhete, Ativo, ValorCobrado, ValorCorreto, Glosa, Justificativa)
    - Subtotal Glosa
  - Rodapé: Total Geral Glosa
- **FP-UC06-009:** Sistema registra auditoria (operação EXPORT)
- **FP-UC06-010:** Sistema retorna arquivo para download
- **FP-UC06-011:** Sistema exibe mensagem: "Exportação concluída. {qtd} itens exportados."

### Fluxos Alternativos
- **FA-UC06-001:** Exportação grande (>10.000 registros)
  - Sistema gera em background (Hangfire)
  - Notifica usuário por email quando concluir
- **FA-UC06-002:** Personalizar template
  - Sistema permite escolher modelo predefinido

### Fluxos de Exceção
- **FE-UC06-001:** Nenhum item encontrado → HTTP 400 "Nenhum item encontrado para exportação"
- **FE-UC06-002:** Erro ao gerar arquivo → HTTP 500 "Erro ao gerar exportação"
- **FE-UC06-003:** Timeout (>30s) → Sistema enfileira job background

### Regras de Negócio
- **RN-UC06-001:** Exportação agrupa por operadora
- **RN-UC06-002:** Documento inclui subtotais e total geral
- **RN-UC06-003:** Justificativas técnicas geradas automaticamente conforme criticidade
- **RN-UC06-004:** Formato Excel com formatação profissional (headers bold, zebra striping)

### Critérios de Aceite
- **CA-UC06-001:** Exportação DEVE agrupar itens por operadora
- **CA-UC06-002:** Cada grupo DEVE exibir subtotal de glosas
- **CA-UC06-003:** Documento DEVE incluir data de geração e total geral
- **CA-UC06-004:** Justificativas técnicas DEVEM ser geradas automaticamente
- **CA-UC06-005:** Excel DEVE ter formatação profissional

---

## UC07 — Buscar e Filtrar Avançado

### Objetivo
Permitir busca e filtragem avançada por múltiplos critérios combinados.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.VIEW`

### Pós-condições
- Resultados filtrados conforme critérios
- Filtros aplicados refletidos na URL

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa "Buscar Avançada"
- **FP-UC07-002:** Sistema exibe campos de filtro:
  - Lote (AAAAMM)
  - Resumo de Auditoria
  - Bilhete (número parcial)
  - Ativo (código parcial)
  - Operadora
  - Tipo de Bilhete
  - UnidadeConsumo
  - Faixa de Glosa (mín-máx)
  - Faixa de Divergência (mín-máx)
  - Status
  - Data Criação (intervalo)
- **FP-UC07-003:** Usuário define critérios
- **FP-UC07-004:** Sistema valida filtros
- **FP-UC07-005:** Sistema aplica filtros cumulativos (AND)
- **FP-UC07-006:** Sistema retorna resultados paginados
- **FP-UC07-007:** Sistema atualiza URL com query string

### Fluxos Alternativos
- **FA-UC07-001:** Limpar filtros
  - Sistema remove todos os filtros
  - Retorna para listagem padrão
- **FA-UC07-002:** Salvar filtro como favorito
  - Sistema armazena combinação de filtros
  - Usuário pode reaplicar rapidamente

### Fluxos de Exceção
- **FE-UC07-001:** Filtro inválido → HTTP 400 "Filtro {nome} inválido"
- **FE-UC07-002:** Nenhum resultado → Exibe estado vazio

### Regras de Negócio
- **RN-UC07-001:** Filtros são cumulativos (operador AND)
- **RN-UC07-002:** Buscas textuais são case-insensitive
- **RN-UC07-003:** Filtros refletem na URL (deep linking)

### Critérios de Aceite
- **CA-UC07-001:** Filtros DEVEM ser cumulativos
- **CA-UC07-002:** URL DEVE refletir filtros aplicados
- **CA-UC07-003:** Performance: Busca DEVE retornar em <500ms

---

## UC08 — Gerar Relatórios Gerenciais

### Objetivo
Gerar relatórios consolidados por operadora, tipo de serviço, período.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.VIEW`

### Pós-condições
- Relatório gerado e exibido
- Auditoria de acesso registrada

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa "Relatórios"
- **FP-UC08-002:** Sistema exibe opções:
  - Por Operadora
  - Por Tipo de Serviço
  - Por Período
  - Por Criticidade
- **FP-UC08-003:** Usuário seleciona tipo de relatório
- **FP-UC08-004:** Sistema solicita parâmetros (período, filtros)
- **FP-UC08-005:** Sistema gera relatório consolidado
- **FP-UC08-006:** Sistema exibe gráficos e tabelas
- **FP-UC08-007:** Sistema permite exportar em PDF/Excel

### Fluxos Alternativos
- **FA-UC08-001:** Agendar relatório recorrente
  - Sistema envia por email periodicamente

### Fluxos de Exceção
- **FE-UC08-001:** Dados insuficientes → HTTP 400 "Período selecionado sem dados"

### Regras de Negócio
- **RN-UC08-001:** Relatórios incluem totalizadores
- **RN-UC08-002:** Gráficos gerados automaticamente

### Critérios de Aceite
- **CA-UC08-001:** Relatório DEVE incluir totalizadores
- **CA-UC08-002:** Gráficos DEVEM ser gerados automaticamente
- **CA-UC08-003:** Performance: Relatório de 50.000 itens DEVE gerar em <5s

---

## UC09 — Visualizar Dashboard de Glosas

### Objetivo
Exibir dashboard em tempo real com KPIs de glosas.

### Pré-condições
- Usuário autenticado
- Permissão `AUD.ITENS.VIEW`

### Pós-condições
- Dashboard exibido com dados atualizados

### Fluxo Principal
- **FP-UC09-001:** Usuário acessa "Dashboard de Glosas"
- **FP-UC09-002:** Sistema carrega KPIs:
  - Total Glosa Pendente
  - Total Glosa Aprovada
  - Total Glosa Contestada
  - Total Glosa Recuperada
  - Taxa de Recuperação (%)
  - Economia Gerada (R$)
- **FP-UC09-003:** Sistema exibe gráficos:
  - Evolução de Glosas (linha temporal)
  - Distribuição por Operadora (pizza)
  - Top 10 Divergências (barras)
- **FP-UC09-004:** Sistema atualiza automaticamente via SignalR

### Fluxos Alternativos
- **FA-UC09-001:** Filtrar por período
  - Sistema recalcula KPIs

### Fluxos de Exceção
- **FE-UC09-001:** Erro ao carregar dados → Exibe cache anterior

### Regras de Negócio
- **RN-UC09-001:** Dashboard com cache de 15 minutos
- **RN-UC09-002:** Atualização em tempo real via SignalR

### Critérios de Aceite
- **CA-UC09-001:** KPIs DEVEM ser calculados em tempo real
- **CA-UC09-002:** Gráficos DEVEM ser interativos
- **CA-UC09-003:** Performance: Dashboard DEVE carregar em <2s

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Funcionalidades RF034 | Regras de Negócio |
|----|----------------------|-------------------|
| UC00 | F01, F10, F14 | RN-RF034-013, RN-RF034-014 |
| UC01 | F01, F02, F03, F05, F06, F11, F12 | RN-RF034-001, RN-RF034-002, RN-RF034-003, RN-RF034-004, RN-RF034-005, RN-RF034-006, RN-RF034-009, RN-RF034-011, RN-RF034-013 |
| UC02 | F01, F11, F14 | RN-RF034-009, RN-RF034-013 |
| UC03 | F01, F02, F03, F06, F11 | RN-RF034-002, RN-RF034-006, RN-RF034-009, RN-RF034-011, RN-RF034-013 |
| UC04 | F01, F06, F11 | RN-RF034-006, RN-RF034-009, RN-RF034-012, RN-RF034-013 |
| UC05 | F07, F11 | RN-RF034-009 |
| UC06 | F08, F11 | RN-RF034-008, RN-RF034-015 |
| UC07 | F10, F11 | RN-RF034-010, RN-RF034-014 |
| UC08 | F04, F09, F11 | RN-RF034-014 |
| UC09 | F04, F10, F11 | RN-RF034-014 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - Recriação completa alinhada ao RF034 (Auditoria de Telecom) |
| 1.0 | 2025-12-18 | Architect Agent | Versão inicial (INCORRETA - documentava RF003 em vez de RF034) |

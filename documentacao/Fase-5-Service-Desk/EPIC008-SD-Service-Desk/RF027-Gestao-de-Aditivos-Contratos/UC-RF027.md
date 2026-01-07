# UC-RF027 — Casos de Uso: Gestão de Aditivos de Contratos

**RF:** RF027 — Gestão de Aditivos de Contratos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC01 | Listar Aditivos | Exibir listagem paginada de aditivos contratuais |
| UC02 | Criar Aditivo | Criar novo aditivo usando wizard multi-step |
| UC03 | Visualizar Aditivo | Exibir detalhes completos de um aditivo específico |
| UC04 | Editar Aditivo | Alterar dados de aditivo em rascunho |
| UC05 | Inativar Aditivo | Inativar aditivo logicamente |
| UC06 | Calcular Impacto Financeiro | Calcular impacto financeiro automático do aditivo |
| UC07 | Comparar Versões | Comparar versões de contrato (diff visual) |
| UC08 | Aprovar Aditivo | Workflow de aprovação multi-nível (Gestor → Jurídico → Diretoria) |

---

## UC01 - Listar Aditivos

### Descrição
Exibir listagem paginada de aditivos contratuais com filtros avançados (contrato, tipo, status, período) e ordenação.

### Atores
- Usuário autenticado com permissão de visualização de aditivos
- Gestor de contratos
- Analista jurídico

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.LISTAR`
- Multi-tenancy: Usuário vinculado a Fornecedor

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Acessa menu "Contratos" → "Aditivos" | - |
| 2 | - | Carrega lista paginada (20 registros/página) |
| 3 | - | Exibe colunas: Número Aditivo, Contrato Base, Tipo, Data Criação, Impacto Financeiro, Status, Ações |
| 4 | Aplica filtros (contrato, tipo, status) | Recarrega lista com filtros aplicados |
| 5 | Pode ordenar por coluna | Reordena resultados |
| 6 | Pode buscar por número/descrição | Filtra resultados em tempo real |

### Filtros Disponíveis

| Filtro | Tipo | Descrição |
|--------|------|-----------|
| Contrato Base | Select | Filtra por contrato específico |
| Tipo Aditivo | Select Multiple | Acréscimo, Supressão, Alteração Tarifária, etc. |
| Status | Select | Rascunho, Aprovação, Assinatura, Vigente, Encerrado |
| Período | Date Range | Data criação início/fim |
| Impacto Financeiro | Range | Filtro por valor (mínimo/máximo) |

### Fluxos Alternativos

**FA01 - Lista Vazia**
- **Condição:** Não existem aditivos para os filtros aplicados
- **Ação:** Sistema exibe mensagem "Nenhum aditivo encontrado" + botão "Criar Novo Aditivo"

**FA02 - Visualizar Pipeline Kanban**
- **Condição:** Usuário clica em "Visualizar Pipeline"
- **Ação:** Sistema exibe Kanban com colunas: Rascunho → Aprovação → Assinatura → Vigente → Encerrado

### Exceções

**EX01 - Erro de Conexão**
- **Condição:** Falha na comunicação com servidor
- **Ação:** Sistema exibe mensagem de erro e botão "Tentar novamente"

### Pós-condições
- Lista exibida com dados atualizados
- Filtros persistidos na sessão do usuário

### Regras de Negócio Aplicáveis
- RN-ADT-027-15: Isolamento multi-tenancy
- RN-ADT-027-16: Auditoria de acesso

---

## UC02 - Criar Aditivo

### Descrição
Criar novo aditivo contratual usando wizard multi-step inteligente com 5 etapas (Tipo → Dados → Impacto → Documentos → Revisão).

### Atores
- Usuário autenticado com permissão de criação de aditivos
- Gestor de contratos

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.CRIAR`
- Contrato base existe e está vigente

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Novo Aditivo" | - |
| 2 | - | Exibe wizard (Passo 1/5: Seleção de Tipo) |
| 3 | Seleciona contrato base | Sistema carrega dados do contrato |
| 4 | Seleciona tipo aditivo (8 opções) | Sistema carrega wizard específico do tipo |
| 5 | - | Passo 2/5: Preenche dados específicos do tipo |
| 6 | Preenche campos obrigatórios | Sistema valida em tempo real |
| 7 | - | Passo 3/5: Sistema calcula impacto financeiro automaticamente |
| 8 | Revisa projeção financeira | - |
| 9 | - | Passo 4/5: Upload de documentos |
| 10 | Faz upload de PDFs/Word | Sistema valida formato e tamanho |
| 11 | - | Passo 5/5: Revisão final de todos os dados |
| 12 | Clica em "Salvar Aditivo" | Sistema cria aditivo e nova versão do contrato |

### Campos do Formulário (por Tipo)

**Tipo 1: Acréscimo de Linhas/Ativos**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Contrato Base | Select | Sim | Deve estar vigente |
| Quantidade Linhas | Number | Sim | > 0 |
| Valor Unitário | Currency | Sim | > 0 |
| Plano/Serviço | Select | Sim | - |
| Data Ativação | Date | Sim | ≥ Hoje |
| Justificativa | Textarea | Sim | Min 50 caracteres |

**Tipo 2: Supressão de Linhas/Ativos**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Linhas a Remover | Multi-select | Sim | Mínimo 1 linha |
| Motivo | Textarea | Sim | Min 50 caracteres |
| Data Desligamento | Date | Sim | ≥ Hoje |
| Calcular Multa | Checkbox | Não | Se sim, sistema calcula multa rescisória |

**Tipo 3: Alteração Tarifária**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Plano Original | Select | Sim | Deve existir no contrato |
| Plano Novo | Select | Sim | Deve ser diferente do original |
| % Desconto Negociado | Number | Não | 0-100% |
| Data Vigência | Date | Sim | ≥ Hoje |

**Tipo 4: Prorrogação de Prazo**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Nova Data Término | Date | Sim | ≥ Data término atual + 1 mês |
| Manter Condições Originais | Radio | Sim | Sim / Não |
| Período Prorrogado | Text (readonly) | - | Calculado automaticamente |

**Tipo 5: Mudança de SLA**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| SLA Atual | Select | Sim | Referência RF028 |
| SLA Novo | Select | Sim | Diferente do atual |
| Impacto Tarifário | Currency | Não | Pode ser positivo/negativo |

**Tipo 6: Inclusão de Novos Serviços**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Descrição Serviço | Text | Sim | Max 200 caracteres |
| Valor | Currency | Sim | > 0 |
| Forma Cobrança | Radio | Sim | Mensal / Única |

**Tipo 7: Reajuste Inflacionário**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Índice Econômico | Select | Sim | IPCA, IGP-M, IPC |
| % Reajuste | Number | Sim | 0-100% |
| Data Base | Date | Sim | - |

**Tipo 8: Troca de Garantias**

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Garantia Atual | Select | Sim | Caução, Fiança, Seguro-Garantia |
| Garantia Nova | Select | Sim | Diferente da atual |
| Valor Garantia | Currency | Sim | > 0 |

### Fluxos Alternativos

**FA01 - Salvar Rascunho**
- **Condição:** Usuário clica em "Salvar Rascunho" durante wizard
- **Ação:** Sistema salva progresso e permite retomar depois

**FA02 - Cancelar Criação**
- **Condição:** Usuário clica em "Cancelar" durante wizard
- **Ação:** Sistema descarta dados e retorna à listagem

**FA03 - Usar Template Cláusulas**
- **Condição:** Usuário clica em "Usar Template Jurídico" (Passo 4)
- **Ação:** Sistema exibe library com 50+ templates pré-aprovados

### Exceções

**EX01 - Validação Falhou**
- **Condição:** Campos inválidos
- **Ação:** Sistema destaca campos com erro e impede avançar no wizard

**EX02 - Contrato Não Vigente**
- **Condição:** Contrato base expirou
- **Ação:** Sistema bloqueia criação e exibe mensagem "Contrato expirado. Crie renovação."

**EX03 - Valor Acréscimo >25% Contrato Base**
- **Condição:** Tipo Acréscimo com valor >25%
- **Ação:** Sistema alerta "Requer aprovação diretoria" mas permite continuar

### Pós-condições
- Aditivo criado com status "Rascunho"
- Nova versão do contrato gerada
- Log de auditoria registrado
- Notificação enviada para aprovadores

### Regras de Negócio Aplicáveis
- RN-ADT-027-01: 8 tipos de aditivos suportados
- RN-ADT-027-02: Wizard multi-step inteligente
- RN-ADT-027-03: Cálculo automático impacto financeiro

---

## UC03 - Visualizar Aditivo

### Descrição
Exibir detalhes completos de um aditivo específico incluindo dados do aditivo, impacto financeiro, documentos e histórico.

### Atores
- Usuário autenticado com permissão de visualização

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.VISUALIZAR`
- Aditivo existe no sistema

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em aditivo na listagem | - |
| 2 | - | Carrega dados completos do aditivo |
| 3 | - | Exibe tela com abas: Resumo, Impacto Financeiro, Documentos, Histórico |
| 4 | Navega entre abas | Carrega conteúdo da aba selecionada |

### Informações Exibidas

**Aba Resumo:**

| Campo | Descrição |
|-------|-----------|
| Número Aditivo | Identificador único |
| Contrato Base | Número contrato + link para visualizar |
| Tipo Aditivo | Um dos 8 tipos |
| Data Criação | Data criação do aditivo |
| Status | Rascunho, Aprovação, Assinatura, Vigente, Encerrado |
| Criado Por | Usuário que criou |
| Dados Específicos | Campos do tipo (ex: Quantidade Linhas, Valor, etc.) |

**Aba Impacto Financeiro:**
- Valor Incremental Mensal
- Valor Incremental Anual
- Projeção 12 meses
- Gráfico Waterfall (comparação antes/depois)
- Valor Total Contrato Pré-Aditivo
- Valor Total Contrato Pós-Aditivo

**Aba Documentos:**
- Lista de PDFs/Word vinculados
- Download individual ou em lote (ZIP)
- Assinatura digital via DocuSign (se aplicável)

**Aba Histórico:**
- Timeline de eventos: Criação, Aprovações, Assinatura, Vigência, Encerramento
- Quem realizou cada ação + data/hora
- Observações de cada etapa

### Fluxos Alternativos

**FA01 - Editar Aditivo**
- **Condição:** Usuário com permissão `ADITIVOS.EDITAR` clica em "Editar" e aditivo está em "Rascunho"
- **Ação:** Sistema redireciona para UC04

**FA02 - Comparar Versões**
- **Condição:** Usuário clica em "Comparar com Versão Anterior"
- **Ação:** Sistema redireciona para UC07

**FA03 - Download Documentos**
- **Condição:** Usuário clica em "Download Todos"
- **Ação:** Sistema gera ZIP com todos os documentos

### Exceções

**EX01 - Aditivo Não Encontrado**
- **Condição:** Aditivo foi excluído por outro usuário
- **Ação:** Sistema exibe mensagem e redireciona para listagem

**EX02 - Documento Indisponível**
- **Condição:** Arquivo foi movido/deletado do storage
- **Ação:** Sistema exibe mensagem "Documento não disponível"

### Pós-condições
- Acesso ao aditivo registrado em log de auditoria
- Nenhuma alteração no sistema

### Regras de Negócio Aplicáveis
- RN-ADT-027-15: Multi-tenancy
- RN-ADT-027-16: Auditoria de acesso

---

## UC04 - Editar Aditivo

### Descrição
Alterar dados de aditivo em status "Rascunho". Aditivos em outros status não podem ser editados.

### Atores
- Usuário autenticado com permissão de edição

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.EDITAR`
- Aditivo existe e está em status "Rascunho"

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Editar" no aditivo | - |
| 2 | - | Carrega wizard com dados preenchidos |
| 3 | Altera campos desejados | Sistema valida em tempo real |
| 4 | Clica em "Salvar Alterações" | - |
| 5 | - | Valida dados |
| 6 | - | Atualiza aditivo |
| 7 | - | Exibe mensagem de sucesso |

### Fluxos Alternativos

**FA01 - Cancelar Edição**
- **Condição:** Usuário clica em "Cancelar"
- **Ação:** Sistema descarta alterações e retorna à visualização

**FA02 - Alterar Tipo Aditivo**
- **Condição:** Usuário tenta alterar tipo
- **Ação:** Sistema bloqueia e exibe "Tipo não pode ser alterado. Crie novo aditivo."

### Exceções

**EX01 - Aditivo Não Está em Rascunho**
- **Condição:** Status ≠ "Rascunho"
- **Ação:** Sistema bloqueia edição e exibe "Apenas aditivos em rascunho podem ser editados"

**EX02 - Conflito de Edição**
- **Condição:** Outro usuário está editando simultaneamente
- **Ação:** Sistema exibe mensagem de bloqueio

### Pós-condições
- Aditivo atualizado
- Nova versão do impacto financeiro calculada
- Log de auditoria registrado

### Regras de Negócio Aplicáveis
- RN-ADT-027-04: Versionamento completo
- RN-ADT-027-15: Multi-tenancy

---

## UC05 - Inativar Aditivo

### Descrição
Inativar aditivo logicamente (soft delete). Apenas aditivos em "Rascunho" podem ser inativados.

### Atores
- Usuário autenticado com permissão de exclusão

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.INATIVAR`
- Aditivo existe e está em status "Rascunho"

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Inativar" no aditivo | - |
| 2 | - | Exibe diálogo de confirmação "Deseja realmente inativar este aditivo?" |
| 3 | Confirma inativação | - |
| 4 | - | Marca aditivo como inativo (Fl_Excluido = true) |
| 5 | - | Exibe mensagem de sucesso |
| 6 | - | Remove aditivo da listagem |

### Fluxos Alternativos

**FA01 - Cancelar Inativação**
- **Condição:** Usuário cancela no diálogo
- **Ação:** Sistema fecha diálogo e mantém aditivo ativo

### Exceções

**EX01 - Aditivo Vigente**
- **Condição:** Status = "Vigente"
- **Ação:** Sistema bloqueia inativação e exibe "Aditivos vigentes não podem ser inativados. Encerre formalmente."

**EX02 - Aditivo Já Inativo**
- **Condição:** Aditivo já foi inativado
- **Ação:** Sistema exibe mensagem informativa

### Pós-condições
- Aditivo inativado (soft delete)
- Log de auditoria registrado
- Versão do contrato revertida (se aplicável)

### Regras de Negócio Aplicáveis
- RN-ADT-027-14: Soft delete
- RN-ADT-027-16: Auditoria

---

## UC06 - Calcular Impacto Financeiro

### Descrição
Calcular automaticamente o impacto financeiro do aditivo (valor incremental mensal/anual, projeção 12 meses).

### Atores
- Sistema (cálculo automático)
- Usuário (pode recalcular manualmente)

### Pré-condições
- Aditivo criado com dados completos
- Contrato base possui valores de referência

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Sistema detecta criação/edição de aditivo | - |
| 2 | - | Carrega dados do contrato base |
| 3 | - | Aplica fórmula de cálculo conforme tipo aditivo |
| 4 | - | Calcula valor incremental mensal |
| 5 | - | Calcula valor incremental anual (mensal × 12) |
| 6 | - | Gera projeção 12 meses |
| 7 | - | Cria gráfico waterfall (antes/depois) |
| 8 | - | Salva resultados na aba "Impacto Financeiro" |

### Fórmulas de Cálculo (por Tipo)

**Tipo 1: Acréscimo de Linhas**
- Valor Incremental Mensal = Quantidade × Valor Unitário

**Tipo 2: Supressão de Linhas**
- Valor Incremental Mensal = -(Quantidade × Valor Unitário) - Multa Rescisória

**Tipo 3: Alteração Tarifária**
- Valor Incremental Mensal = (Valor Novo - Valor Original) × Quantidade Linhas

**Tipo 4: Prorrogação de Prazo**
- Valor Incremental Anual = Valor Mensal Contrato × Meses Prorrogados

**Tipo 5: Mudança de SLA**
- Valor Incremental Mensal = Impacto Tarifário informado

**Tipo 6: Inclusão de Serviços**
- Valor Incremental Mensal = Valor Serviço (se mensal) ou Valor / 12 (se única)

**Tipo 7: Reajuste Inflacionário**
- Valor Incremental Mensal = Valor Contrato × (% Reajuste / 100)

**Tipo 8: Troca de Garantias**
- Valor Incremental Único = Valor Garantia Nova - Valor Garantia Atual

### Fluxos Alternativos

**FA01 - Recalcular Manualmente**
- **Condição:** Usuário altera dados do aditivo
- **Ação:** Sistema recalcula impacto automaticamente em tempo real

### Exceções

**EX01 - Dados Insuficientes**
- **Condição:** Contrato base sem valores de referência
- **Ação:** Sistema exibe "Impossível calcular impacto. Complete dados do contrato base."

### Pós-condições
- Impacto financeiro calculado e salvo
- Gráfico waterfall gerado
- Projeção 12 meses disponível

### Regras de Negócio Aplicáveis
- RN-ADT-027-03: Cálculo automático impacto financeiro

---

## UC07 - Comparar Versões

### Descrição
Comparar visualmente duas versões de contrato (antes/depois do aditivo) com diff highlighting.

### Atores
- Usuário autenticado
- Analista jurídico

### Pré-condições
- Usuário logado no sistema
- Aditivo gerou nova versão do contrato
- Versão anterior existe

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Clica em "Comparar Versões" no aditivo | - |
| 2 | - | Carrega versão anterior e versão atual do contrato |
| 3 | - | Executa diff engine (comparação texto/cláusulas) |
| 4 | - | Exibe interface split-screen (lado a lado) |
| 5 | - | Destaca mudanças com color coding (verde = adicionado, vermelho = removido, amarelo = modificado) |
| 6 | Navega entre diferenças | Sistema rola automaticamente para próxima mudança |

### Color Coding

| Cor | Significado |
|-----|-------------|
| Verde | Cláusula/texto adicionado |
| Vermelho | Cláusula/texto removido |
| Amarelo | Cláusula/texto modificado |
| Cinza | Sem alteração |

### Fluxos Alternativos

**FA01 - Exportar Comparação**
- **Condição:** Usuário clica em "Exportar Comparação"
- **Ação:** Sistema gera PDF com diff highlighting + track changes estilo Word

**FA02 - Comparar Versões Específicas**
- **Condição:** Usuário seleciona 2 versões específicas (não apenas anterior/atual)
- **Ação:** Sistema compara versões selecionadas

### Exceções

**EX01 - Apenas 1 Versão Disponível**
- **Condição:** Contrato sem versões anteriores
- **Ação:** Sistema exibe "Não há versão anterior para comparar"

### Pós-condições
- Comparação exibida
- Acesso registrado em log de auditoria

### Regras de Negócio Aplicáveis
- RN-ADT-027-04: Versionamento completo
- RN-ADT-027-10: Comparação de versões

---

## UC08 - Aprovar Aditivo

### Descrição
Workflow de aprovação multi-nível de aditivo (Gestor → Jurídico → Diretoria) com prazos SLA e escalação automática.

### Atores
- Gestor de contratos (1º nível)
- Analista jurídico (2º nível)
- Diretor financeiro (3º nível)

### Pré-condições
- Usuário logado no sistema
- Usuário com permissão `ADITIVOS.APROVAR`
- Aditivo em status "Aprovação"
- Workflow configurado

### Fluxo Principal

| Passo | Ator | Sistema |
|-------|------|---------|
| 1 | Gestor acessa "Aditivos Pendentes Aprovação" | - |
| 2 | - | Lista aditivos aguardando aprovação nível 1 |
| 3 | Clica em aditivo | Exibe resumo + impacto financeiro + documentos |
| 4 | Analisa dados | - |
| 5 | Clica em "Aprovar" | - |
| 6 | - | Envia para aprovação nível 2 (Jurídico) |
| 7 | Jurídico aprova | Envia para nível 3 (Diretoria) |
| 8 | Diretor aprova | Status atualizado para "Assinatura" |

### Campos do Formulário

| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Decisão | Radio | Sim | Aprovar / Rejeitar / Solicitar Ajustes |
| Observações | Textarea | Não (obrigatório se rejeitar/solicitar ajustes) | Max 1000 caracteres |

### Fluxos Alternativos

**FA01 - Rejeitar Aditivo**
- **Condição:** Aprovador clica em "Rejeitar"
- **Ação:** Sistema solicita justificativa e devolve para criador

**FA02 - Solicitar Ajustes**
- **Condição:** Aprovador clica em "Solicitar Ajustes"
- **Ação:** Sistema devolve para nível anterior com observações

**FA03 - Delegar Aprovação**
- **Condição:** Aprovador ausente (férias, afastamento)
- **Ação:** Sistema permite delegar para substituto pré-cadastrado

**FA04 - Aprovação Automática**
- **Condição:** Valor incremental < R$ 10.000 e tipo não é "Troca Garantias"
- **Ação:** Sistema aprova automaticamente níveis 1 e 2, requer apenas diretoria

### Exceções

**EX01 - Prazo SLA Expirado**
- **Condição:** Aprovador não decide em 72h
- **Ação:** Sistema escala automaticamente para nível superior

**EX02 - Aprovador Sem Alçada**
- **Condição:** Usuário não tem alçada para valor do aditivo
- **Ação:** Sistema bloqueia aprovação e escala para superior

### Pós-condições
- Aditivo aprovado ou rejeitado
- Histórico de aprovações registrado
- Notificação enviada para próximo nível ou criador (se rejeitado)
- Se totalmente aprovado, status muda para "Assinatura"

### Regras de Negócio Aplicáveis
- RN-ADT-027-05: Workflow aprovação multi-nível
- RN-ADT-027-06: Prazos SLA e escalação
- RN-ADT-027-07: Alçadas por valor

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 17/12/2025 | Architect Agent | Versão inicial com 8 casos de uso completos |

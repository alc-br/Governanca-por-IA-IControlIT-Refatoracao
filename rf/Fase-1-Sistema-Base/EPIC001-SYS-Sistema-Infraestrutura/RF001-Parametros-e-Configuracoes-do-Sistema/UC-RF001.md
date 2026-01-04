# UC-RF001 — Casos de Uso Canônicos

**RF:** RF001 — Sistema de Parâmetros e Configurações Centralizadas
**Versão:** 2.2
**Data:** 2026-01-03
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC001-SYS-Sistema-Infraestrutura
**Fase:** Fase-1-Sistema-Base

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF001 - Sistema de Parâmetros e Configurações Centralizadas**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF001.yaml)
- Massas de Teste (MT-RF001.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

**IMPORTANTE:** Este documento contém a documentação detalhada dos UCs UC00-UC04 (Sistema_Parametro). Os demais UCs (UC05-UC21) estão completamente especificados em **UC-RF001.yaml** e devem ser consultados lá para detalhes completos de fluxos, regras e validações.

---

## 2. SUMÁRIO DE CASOS DE USO

### Entidade 1: Sistema_Parametro (UC00-UC04)
| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Sistema_Parametro | Usuário Autenticado |
| UC01 | Criar Sistema_Parametro | Usuário Autenticado |
| UC02 | Visualizar Sistema_Parametro | Usuário Autenticado |
| UC03 | Editar Sistema_Parametro | Usuário Autenticado |
| UC04 | Excluir Sistema_Parametro | Usuário Autenticado |

### Entidade 2: Sistema_Feature_Flag (UC05-UC09)
| ID | Nome | Ator Principal |
|----|------|----------------|
| UC05 | Listar Sistema_Feature_Flag | Usuário Autenticado |
| UC06 | Criar Sistema_Feature_Flag | Usuário Autenticado |
| UC07 | Visualizar Sistema_Feature_Flag | Usuário Autenticado |
| UC08 | Editar Sistema_Feature_Flag | Usuário Autenticado |
| UC09 | Excluir Sistema_Feature_Flag | Usuário Autenticado |

### Entidade 3: Sistema_Configuracao_Email (UC10-UC14)
| ID | Nome | Ator Principal |
|----|------|----------------|
| UC10 | Listar Sistema_Configuracao_Email | Usuário Autenticado |
| UC11 | Criar Sistema_Configuracao_Email | Usuário Autenticado |
| UC12 | Visualizar Sistema_Configuracao_Email | Usuário Autenticado |
| UC13 | Editar Sistema_Configuracao_Email | Usuário Autenticado |
| UC14 | Excluir Sistema_Configuracao_Email | Usuário Autenticado |

### Entidade 4: Sistema_Limite_Uso (UC15-UC19)
| ID | Nome | Ator Principal |
|----|------|----------------|
| UC15 | Listar Sistema_Limite_Uso | Usuário Autenticado |
| UC16 | Criar Sistema_Limite_Uso | Usuário Autenticado |
| UC17 | Visualizar Sistema_Limite_Uso | Usuário Autenticado |
| UC18 | Editar Sistema_Limite_Uso | Usuário Autenticado |
| UC19 | Excluir Sistema_Limite_Uso | Usuário Autenticado |

### Funcionalidades Especiais (UC20-UC21)
| ID | Nome | Ator Principal | Tipo |
|----|------|----------------|------|
| UC20 | Job Background - Verificação de Limites de Uso | Sistema (Hangfire) | background_job |
| UC21 | Integração - Teste de Envio de E-mail SMTP | Sistema | integracao_externa |

**Total:** 22 Casos de Uso
**Cobertura:** 4 entidades (CRUD completo) + 2 funcionalidades especiais (jobs, integrações)

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Conglomerado)
- Todas as ações exigem **permissão explícita** conforme matriz RBAC
- Erros não devem vazar informações sensíveis (stack traces, senhas, tokens)
- Auditoria deve registrar **quem** (Id_Usuario), **quando** (timestamp), **de onde** (IP, User-Agent) e **qual ação** (CREATE, UPDATE, DELETE, ACCESS)
- Mensagens devem ser claras, previsíveis e rastreáveis
- Dados sensíveis devem ser criptografados em AES-256 antes de persistir
- Configurações dinâmicas devem invalidar cache automaticamente ao salvar

---

## UC00 — Listar Sistema_Parametro

### Objetivo
Permitir que o usuário visualize parâmetros do sistema disponíveis do seu próprio tenant, com suporte a filtros, paginação e ordenação.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.PARAMETROS.VIEW_ANY`

### Pós-condições
- Lista exibida conforme filtros e paginação aplicados
- Valores sensíveis (Fl_Sensivel = 1) são mascarados (`*****`) para usuários sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Parâmetros do Sistema" pelo menu
- **FP-UC00-002:** Sistema valida permissão `SYS.PARAMETROS.VIEW_ANY`
- **FP-UC00-003:** Sistema carrega registros do tenant (filtra por Id_Conglomerado do usuário autenticado)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros por página) e ordenação padrão (Cd_Parametro ASC)
- **FP-UC00-005:** Sistema máscaras valores sensíveis (Fl_Sensivel = 1) se usuário não tiver permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- **FP-UC00-006:** Sistema exibe a lista com colunas: Cd_Parametro, Nm_Parametro, Categoria, Tipo_Dado, Fl_Sistema, Fl_Sensivel, Ações

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por termo - Usuário digita termo de busca → Sistema filtra por Cd_Parametro, Nm_Parametro ou Ds_Parametro (case-insensitive)
- **FA-UC00-002:** Ordenar por coluna - Usuário clica em cabeçalho de coluna → Sistema alterna ordenação ASC/DESC
- **FA-UC00-003:** Filtrar por Categoria - Usuário seleciona categoria (Sistema, Segurança, Integração, Notificação, Relatório) → Sistema aplica filtro
- **FA-UC00-004:** Filtrar por Tipo_Dado - Usuário seleciona tipo (String, Integer, Decimal, Boolean, Date, JSON) → Sistema aplica filtro
- **FA-UC00-005:** Filtrar apenas parâmetros de sistema (Fl_Sistema = 1) - Usuário marca checkbox → Sistema aplica filtro
- **FA-UC00-006:** Exportar lista para CSV - Usuário clica em "Exportar" → Sistema gera CSV (exige permissão `SYS.PARAMETROS.EXPORT`)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão `SYS.PARAMETROS.VIEW_ANY` → Sistema retorna HTTP 403 com mensagem "Acesso negado. Você não tem permissão para visualizar parâmetros."
- **FE-UC00-002:** Nenhum registro encontrado → Sistema exibe estado vazio com mensagem "Nenhum parâmetro encontrado" e botão "Criar Novo Parâmetro"
- **FE-UC00-003:** Erro ao carregar registros → Sistema exibe mensagem "Erro ao carregar parâmetros. Tente novamente." e registra erro em log

### Regras de Negócio
- **RN-SYS-001-14:** Isolamento multi-tenant - Somente registros do tenant do usuário autenticado (Id_Conglomerado)
- **RN-SYS-001-04:** Valores sensíveis mascarados (`*****`) para usuários sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- Registros soft-deleted (Fl_Excluido = 1) não aparecem na listagem

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas registros do tenant do usuário autenticado (Id_Conglomerado)
- **CA-UC00-002:** Registros excluídos (Fl_Excluido = 1) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros por página
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível (Cd_Parametro, Nm_Parametro, Categoria, Tipo_Dado)
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis (busca + categoria + tipo) e refletir na URL para compartilhamento
- **CA-UC00-006:** Valores sensíveis DEVEM ser mascarados (`*****`) para usuários sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- **CA-UC00-007:** Parâmetros de sistema (Fl_Sistema = 1) DEVEM ter indicador visual (ícone de cadeado ou badge "Sistema")

---

## UC01 — Criar Sistema_Parametro

### Objetivo
Permitir a criação de um novo parâmetro do sistema com validação tipada, criptografia de dados sensíveis e auditoria completa.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.PARAMETROS.CREATE`

### Pós-condições
- Registro persistido no banco de dados
- Auditoria registrada em Sistema_Parametro_Historico (tipo CREATE)
- Cache invalidado para forçar reload de configurações
- Evento `parametro.criado` publicado

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Criar Novo Parâmetro"
- **FP-UC01-002:** Sistema valida permissão `SYS.PARAMETROS.CREATE`
- **FP-UC01-003:** Sistema exibe formulário de criação com campos: Cd_Parametro, Nm_Parametro, Ds_Parametro, Categoria, Tipo_Dado, Fl_Sensivel, Fl_Sistema, Fl_Obrigatorio, Regex_Validacao, Valor_Minimo, Valor_Maximo, Opcoes_Validas, Valor_Padrao
- **FP-UC01-004:** Usuário informa dados obrigatórios (Cd_Parametro, Nm_Parametro, Ds_Parametro, Categoria, Tipo_Dado)
- **FP-UC01-005:** Usuário seleciona valor conforme tipo de dado (String, Integer, Decimal, Boolean, Date, JSON)
- **FP-UC01-006:** Usuário clica em "Salvar"
- **FP-UC01-007:** Sistema valida campos obrigatórios (RN-SYS-001-06)
- **FP-UC01-008:** Sistema valida unicidade de Cd_Parametro no tenant (RN-SYS-001-01)
- **FP-UC01-009:** Sistema valida valor conforme tipo de dado (RN-SYS-001-02)
- **FP-UC01-010:** Sistema valida regex se Regex_Validacao especificado (RN-SYS-001-02)
- **FP-UC01-011:** Sistema valida valor dentro de min/max se especificado (RN-SYS-001-02)
- **FP-UC01-012:** Sistema valida valor dentro de Opcoes_Validas se especificado (RN-SYS-001-05)
- **FP-UC01-013:** Sistema criptografa valor se Fl_Sensivel = 1 (RN-SYS-001-04)
- **FP-UC01-014:** Sistema preenche automaticamente: Id_Conglomerado (do usuário autenticado), Id_Usuario_Criacao, Dt_Criacao, Fl_Excluido = 0
- **FP-UC01-015:** Sistema persiste registro no banco de dados
- **FP-UC01-016:** Sistema registra auditoria em Sistema_Parametro_Historico (tipo CREATE, valor anterior = NULL, valor novo = JSON completo)
- **FP-UC01-017:** Sistema invalida cache de configurações
- **FP-UC01-018:** Sistema publica evento `parametro.criado`
- **FP-UC01-019:** Sistema exibe mensagem de sucesso "Parâmetro '{Cd_Parametro}' criado com sucesso" e redireciona para tela de visualização

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro - Usuário clica em "Salvar e Criar Outro" → Sistema salva, exibe mensagem de sucesso e limpa formulário para nova criação
- **FA-UC01-002:** Cancelar criação - Usuário clica em "Cancelar" → Sistema descarta dados e retorna para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação de campos obrigatórios → Sistema retorna HTTP 400 com lista de erros: `"Campo '{campo}' é obrigatório"`
- **FE-UC01-002:** Código de parâmetro duplicado → Sistema retorna HTTP 409 com mensagem: `"Já existe um parâmetro com o código '{Cd_Parametro}' neste conglomerado"`
- **FE-UC01-003:** Valor inválido conforme tipo de dado → Sistema retorna HTTP 400 com mensagem específica: `"Valor inválido para tipo {Tipo_Dado}. Esperado: {formato}"`
- **FE-UC01-004:** Valor fora de min/max → Sistema retorna HTTP 400 com mensagem: `"Valor deve estar entre {Valor_Minimo} e {Valor_Maximo}"`
- **FE-UC01-005:** Valor fora de Opcoes_Validas → Sistema retorna HTTP 400 com mensagem: `"Valor '{valor}' inválido. Opções válidas: {Opcoes_Validas}"`
- **FE-UC01-006:** JSON inválido → Sistema retorna HTTP 400 com mensagem: `"JSON inválido. Erro: {erro de parsing}"`
- **FE-UC01-007:** Regex inválido → Sistema retorna HTTP 400 com mensagem: `"Valor não corresponde ao padrão esperado: {Regex_Validacao}"`
- **FE-UC01-008:** Erro inesperado ao salvar → Sistema retorna HTTP 500, registra erro em log e exibe mensagem: `"Erro ao criar parâmetro. Tente novamente."`

### Regras de Negócio
- **RN-SYS-001-01:** Código único de parâmetro (Cd_Parametro) por tenant
- **RN-SYS-001-02:** Validação por tipo de dado (String, Integer, Decimal, Boolean, Date, JSON)
- **RN-SYS-001-04:** Criptografia AES-256 para dados sensíveis (Fl_Sensivel = 1)
- **RN-SYS-001-05:** Validação de opções válidas (se Opcoes_Validas especificado)
- **RN-SYS-001-06:** Valores obrigatórios (se Fl_Obrigatorio = 1, usar Valor_Padrao se especificado)
- **RN-SYS-001-07:** Histórico completo de alterações
- **RN-SYS-001-14:** Isolamento multi-tenant (Id_Conglomerado automático)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios (Cd_Parametro, Nm_Parametro, Ds_Parametro, Categoria, Tipo_Dado) DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Conglomerado DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** Id_Usuario_Criacao DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** Dt_Criacao DEVE ser preenchido automaticamente com timestamp atual (UTC)
- **CA-UC01-005:** Sistema DEVE retornar erro claro (HTTP 400/409) se validação falhar, sem expor stack traces
- **CA-UC01-006:** Auditoria DEVE ser registrada em Sistema_Parametro_Historico APÓS sucesso da criação
- **CA-UC01-007:** Valores sensíveis (Fl_Sensivel = 1) DEVEM ser criptografados em AES-256 ANTES de persistir no banco
- **CA-UC01-008:** Cache de configurações DEVE ser invalidado após criação bem-sucedida
- **CA-UC01-009:** Evento `parametro.criado` DEVE ser publicado após sucesso
- **CA-UC01-010:** Tentativa de criar parâmetro com Cd_Parametro duplicado DEVE retornar HTTP 409

---

## UC02 — Visualizar Sistema_Parametro

### Objetivo
Permitir visualização detalhada de um parâmetro do sistema, incluindo metadados, histórico de alterações e valores descriptografados (para usuários autorizados).

### Pré-condições
- Usuário autenticado
- Permissão `SYS.PARAMETROS.VIEW`

### Pós-condições
- Dados exibidos corretamente conforme permissões do usuário
- Auditoria registrada em Sistema_Parametro_Historico (tipo ACCESS) se parâmetro for sensível (Fl_Sensivel = 1)

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona parâmetro na listagem ou acessa URL direta
- **FP-UC02-002:** Sistema valida permissão `SYS.PARAMETROS.VIEW`
- **FP-UC02-003:** Sistema valida que parâmetro pertence ao tenant do usuário autenticado (Id_Conglomerado)
- **FP-UC02-004:** Sistema carrega dados completos do parâmetro
- **FP-UC02-005:** Sistema verifica se parâmetro é sensível (Fl_Sensivel = 1)
- **FP-UC02-006:** Se parâmetro sensível E usuário NÃO tem permissão `SYS.PARAMETROS.VIEW_SENSITIVE` → Máscaras valor (`*****`)
- **FP-UC02-007:** Se parâmetro sensível E usuário tem permissão `SYS.PARAMETROS.VIEW_SENSITIVE` → Descriptografa valor e registra auditoria tipo ACCESS
- **FP-UC02-008:** Sistema exibe dados: Cd_Parametro, Nm_Parametro, Ds_Parametro, Categoria, Tipo_Dado, Valor (conforme tipo), Fl_Sensivel, Fl_Sistema, Fl_Obrigatorio, Regex_Validacao, Valor_Minimo, Valor_Maximo, Opcoes_Validas, Valor_Padrao
- **FP-UC02-009:** Sistema exibe metadados de auditoria: Id_Usuario_Criacao, Dt_Criacao, Id_Usuario_Atualizacao, Dt_Atualizacao
- **FP-UC02-010:** Sistema exibe botões de ação: "Editar" (se permissão `SYS.PARAMETROS.UPDATE`), "Excluir" (se permissão `SYS.PARAMETROS.DELETE` e Fl_Sistema = 0)

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar histórico de alterações - Usuário clica em "Histórico" → Sistema exibe lista de registros de Sistema_Parametro_Historico ordenados por Dt_Alteracao DESC

### Fluxos de Exceção
- **FE-UC02-001:** Registro inexistente → Sistema retorna HTTP 404 com mensagem: `"Parâmetro não encontrado"`
- **FE-UC02-002:** Registro de outro tenant → Sistema retorna HTTP 404 (não revela existência do registro em outro tenant)
- **FE-UC02-003:** Usuário sem permissão `SYS.PARAMETROS.VIEW` → Sistema retorna HTTP 403 com mensagem: `"Acesso negado. Você não tem permissão para visualizar parâmetros."`

### Regras de Negócio
- **RN-SYS-001-04:** Valores sensíveis descriptografados apenas para Super Admin com permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- **RN-SYS-001-07:** Acesso a parâmetro sensível gera registro de auditoria tipo ACCESS
- **RN-SYS-001-14:** Isolamento multi-tenant (usuário só visualiza parâmetros do próprio tenant)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar parâmetros do próprio tenant (Id_Conglomerado)
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (Id_Usuario_Criacao, Dt_Criacao, Id_Usuario_Atualizacao, Dt_Atualizacao)
- **CA-UC02-003:** Tentativa de acessar parâmetro de outro tenant DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar parâmetro inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco (não em cache)
- **CA-UC02-006:** Valores sensíveis DEVEM ser mascarados (`*****`) para usuários sem permissão `SYS.PARAMETROS.VIEW_SENSITIVE`
- **CA-UC02-007:** Visualização de parâmetro sensível com valor descriptografado DEVE registrar auditoria tipo ACCESS
- **CA-UC02-008:** Parâmetros de sistema (Fl_Sistema = 1) DEVEM ter botão "Excluir" desabilitado/oculto

---

## UC03 — Editar Sistema_Parametro

### Objetivo
Permitir alteração controlada de parâmetros do sistema, com validação, criptografia e auditoria de mudanças.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.PARAMETROS.UPDATE`
- Parâmetro não marcado como sistema (Fl_Sistema = 0) para edição completa; parâmetros de sistema permitem apenas edição de valor

### Pós-condições
- Registro atualizado no banco de dados
- Auditoria registrada em Sistema_Parametro_Historico (tipo UPDATE) com diff JSON (valor anterior vs. novo)
- Cache invalidado para forçar reload de configurações
- Evento `parametro.atualizado` publicado

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" na tela de visualização ou listagem
- **FP-UC03-002:** Sistema valida permissão `SYS.PARAMETROS.UPDATE`
- **FP-UC03-003:** Sistema valida que parâmetro pertence ao tenant do usuário autenticado (Id_Conglomerado)
- **FP-UC03-004:** Sistema verifica se parâmetro é de sistema (Fl_Sistema)
- **FP-UC03-005:** Se Fl_Sistema = 1 → Sistema permite editar apenas valor (campos metadados bloqueados)
- **FP-UC03-006:** Se Fl_Sistema = 0 → Sistema permite editar todos os campos exceto Cd_Parametro e Id_Conglomerado
- **FP-UC03-007:** Sistema carrega dados atuais no formulário
- **FP-UC03-008:** Usuário altera dados (valor, descrição, validações, flags)
- **FP-UC03-009:** Usuário clica em "Salvar"
- **FP-UC03-010:** Sistema valida campos obrigatórios (RN-SYS-001-06)
- **FP-UC03-011:** Sistema valida valor conforme tipo de dado (RN-SYS-001-02)
- **FP-UC03-012:** Sistema valida regex se Regex_Validacao especificado (RN-SYS-001-02)
- **FP-UC03-013:** Sistema valida valor dentro de min/max se especificado (RN-SYS-001-02)
- **FP-UC03-014:** Sistema valida valor dentro de Opcoes_Validas se especificado (RN-SYS-001-05)
- **FP-UC03-015:** Sistema criptografa valor se Fl_Sensivel = 1 (RN-SYS-001-04)
- **FP-UC03-016:** Sistema captura estado anterior do registro (JSON completo)
- **FP-UC03-017:** Sistema preenche automaticamente: Id_Usuario_Atualizacao, Dt_Atualizacao
- **FP-UC03-018:** Sistema persiste alterações no banco de dados
- **FP-UC03-019:** Sistema registra auditoria em Sistema_Parametro_Historico (tipo UPDATE, valor anterior = JSON antes, valor novo = JSON depois)
- **FP-UC03-020:** Sistema invalida cache de configurações
- **FP-UC03-021:** Sistema publica evento `parametro.atualizado`
- **FP-UC03-022:** Sistema exibe mensagem de sucesso "Parâmetro '{Cd_Parametro}' atualizado com sucesso" e redireciona para tela de visualização

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição - Usuário clica em "Cancelar" → Sistema descarta alterações e retorna para tela de visualização

### Fluxos de Exceção
- **FE-UC03-001:** Tentativa de editar parâmetro de sistema (Fl_Sistema = 1) com campos metadados alterados → Sistema retorna HTTP 403 com mensagem: `"Parâmetros de sistema não podem ser editados via interface. Apenas valores podem ser alterados."`
- **FE-UC03-002:** Erro de validação de campos obrigatórios → Sistema retorna HTTP 400 com lista de erros
- **FE-UC03-003:** Valor inválido conforme tipo de dado → Sistema retorna HTTP 400 com mensagem específica
- **FE-UC03-004:** Valor fora de min/max → Sistema retorna HTTP 400 com mensagem específica
- **FE-UC03-005:** Valor fora de Opcoes_Validas → Sistema retorna HTTP 400 com mensagem específica
- **FE-UC03-006:** JSON inválido → Sistema retorna HTTP 400 com mensagem de erro de parsing
- **FE-UC03-007:** Regex inválido → Sistema retorna HTTP 400 com mensagem específica
- **FE-UC03-008:** Conflito de edição concorrente (Optimistic Concurrency) → Sistema retorna HTTP 409 com mensagem: `"O registro foi alterado por outro usuário. Recarregue e tente novamente."`
- **FE-UC03-009:** Tentativa de editar parâmetro de outro tenant → Sistema retorna HTTP 404

### Regras de Negócio
- **RN-SYS-001-02:** Validação por tipo de dado
- **RN-SYS-001-03:** Parâmetros de sistema (Fl_Sistema = 1) não podem ter metadados editados via UI (apenas valores)
- **RN-SYS-001-04:** Criptografia AES-256 para dados sensíveis
- **RN-SYS-001-05:** Validação de opções válidas
- **RN-SYS-001-06:** Valores obrigatórios
- **RN-SYS-001-07:** Histórico completo com diff JSON (antes vs. depois)
- **RN-SYS-001-14:** Isolamento multi-tenant

### Critérios de Aceite
- **CA-UC03-001:** Id_Usuario_Atualizacao DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** Dt_Atualizacao DEVE ser preenchido automaticamente com timestamp atual (UTC)
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (Optimistic Concurrency Control via ETag ou timestamp)
- **CA-UC03-005:** Tentativa de editar parâmetro de outro tenant DEVE retornar HTTP 404
- **CA-UC03-006:** Auditoria DEVE registrar estado anterior e novo estado (diff JSON) em Sistema_Parametro_Historico
- **CA-UC03-007:** Cache DEVE ser invalidado após edição bem-sucedida
- **CA-UC03-008:** Parâmetros de sistema (Fl_Sistema = 1) SÓ permitem edição de valor, não de metadados
- **CA-UC03-009:** Tentativa de editar metadados de parâmetro de sistema DEVE retornar HTTP 403

---

## UC04 — Excluir Sistema_Parametro

### Objetivo
Permitir exclusão lógica (soft delete) de parâmetros do sistema, com proteção de parâmetros críticos e auditoria completa.

### Pré-condições
- Usuário autenticado
- Permissão `SYS.PARAMETROS.DELETE`
- Parâmetro não marcado como sistema (Fl_Sistema = 0) - parâmetros de sistema NÃO podem ser excluídos via UI

### Pós-condições
- Registro marcado como excluído (Fl_Excluido = 1, Dt_Exclusao = timestamp)
- Auditoria registrada em Sistema_Parametro_Historico (tipo DELETE)
- Cache invalidado para forçar reload de configurações
- Evento `parametro.excluido` publicado

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" na tela de visualização ou listagem
- **FP-UC04-002:** Sistema valida permissão `SYS.PARAMETROS.DELETE`
- **FP-UC04-003:** Sistema valida que parâmetro pertence ao tenant do usuário autenticado (Id_Conglomerado)
- **FP-UC04-004:** Sistema verifica se parâmetro é de sistema (Fl_Sistema)
- **FP-UC04-005:** Se Fl_Sistema = 1 → Sistema retorna HTTP 403 (parâmetros de sistema não podem ser excluídos)
- **FP-UC04-006:** Sistema exibe modal de confirmação: "Tem certeza que deseja excluir o parâmetro '{Cd_Parametro}'? Esta ação não pode ser desfeita."
- **FP-UC04-007:** Usuário confirma exclusão
- **FP-UC04-008:** Sistema executa soft delete: Fl_Excluido = 1, Dt_Exclusao = timestamp atual, Id_Usuario_Exclusao = ID do usuário autenticado
- **FP-UC04-009:** Sistema registra auditoria em Sistema_Parametro_Historico (tipo DELETE, valor anterior = JSON completo, valor novo = NULL)
- **FP-UC04-010:** Sistema invalida cache de configurações
- **FP-UC04-011:** Sistema publica evento `parametro.excluido`
- **FP-UC04-012:** Sistema exibe mensagem de sucesso "Parâmetro '{Cd_Parametro}' excluído com sucesso" e redireciona para listagem

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão - Usuário clica em "Cancelar" no modal → Sistema fecha modal sem executar exclusão

### Fluxos de Exceção
- **FE-UC04-001:** Tentativa de excluir parâmetro de sistema (Fl_Sistema = 1) → Sistema retorna HTTP 403 com mensagem: `"Parâmetros de sistema não podem ser excluídos via interface."`
- **FE-UC04-002:** Registro já excluído (Fl_Excluido = 1) → Sistema retorna HTTP 404 com mensagem: `"Parâmetro não encontrado ou já foi excluído"`
- **FE-UC04-003:** Tentativa de excluir parâmetro de outro tenant → Sistema retorna HTTP 404
- **FE-UC04-004:** Usuário sem permissão `SYS.PARAMETROS.DELETE` → Sistema retorna HTTP 403 com mensagem: `"Acesso negado. Você não tem permissão para excluir parâmetros."`

### Regras de Negócio
- **RN-SYS-001-03:** Parâmetros de sistema (Fl_Sistema = 1) não podem ser excluídos via interface
- **RN-SYS-001-07:** Histórico completo de alterações (registrar tipo DELETE)
- **RN-SYS-001-14:** Isolamento multi-tenant
- Exclusão sempre lógica (soft delete) via Fl_Excluido = 1
- Retenção de dados excluídos por 7 anos (LGPD)

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via Fl_Excluido = 1, NÃO física (DELETE do banco)
- **CA-UC04-002:** Parâmetros de sistema (Fl_Sistema = 1) NÃO podem ser excluídos via interface (retornar HTTP 403)
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário via modal
- **CA-UC04-004:** Dt_Exclusao DEVE ser preenchido com timestamp atual (UTC)
- **CA-UC04-005:** Id_Usuario_Exclusao DEVE ser preenchido com ID do usuário autenticado
- **CA-UC04-006:** Parâmetro excluído NÃO deve aparecer em listagens padrão (filtrar por Fl_Excluido = 0)
- **CA-UC04-007:** Auditoria DEVE ser registrada em Sistema_Parametro_Historico (tipo DELETE, valor anterior = JSON completo)
- **CA-UC04-008:** Cache DEVE ser invalidado após exclusão bem-sucedida
- **CA-UC04-009:** Tentativa de excluir parâmetro de outro tenant DEVE retornar HTTP 404

---

## 4. MATRIZ DE RASTREABILIDADE

### Cobertura de Regras de Negócio por Caso de Uso

| UC | Regras de Negócio Aplicadas |
|----|----------------------------|
| UC00 | RN-SYS-001-04, RN-SYS-001-14 |
| UC01 | RN-SYS-001-01, RN-SYS-001-02, RN-SYS-001-04, RN-SYS-001-05, RN-SYS-001-06, RN-SYS-001-07, RN-SYS-001-14 |
| UC02 | RN-SYS-001-04, RN-SYS-001-07, RN-SYS-001-14 |
| UC03 | RN-SYS-001-02, RN-SYS-001-03, RN-SYS-001-04, RN-SYS-001-05, RN-SYS-001-06, RN-SYS-001-07, RN-SYS-001-14 |
| UC04 | RN-SYS-001-03, RN-SYS-001-07, RN-SYS-001-14 |

### Cobertura de Itens do RF por Caso de Uso

| UC | Itens do RF (catalog) Cobertos |
|----|-------------------------------|
| UC00 | RF-CRUD-02, RF-SEC-01, RF-SEC-02, RF-SEC-04 |
| UC01 | RF-CRUD-01, RF-VAL-01, RF-VAL-02, RF-VAL-03, RF-VAL-04, RF-VAL-05, RF-VAL-06, RF-SEC-01, RF-SEC-02, RF-SEC-03 |
| UC02 | RF-CRUD-03, RF-SEC-01, RF-SEC-02, RF-SEC-04 |
| UC03 | RF-CRUD-04, RF-VAL-01, RF-VAL-03, RF-VAL-04, RF-VAL-05, RF-VAL-06, RF-SEC-01, RF-SEC-02, RF-SEC-03, RF-SEC-05 |
| UC04 | RF-CRUD-05, RF-SEC-01, RF-SEC-02, RF-SEC-05 |

### Cobertura de Permissões por Caso de Uso

| UC | Permissões Requeridas |
|----|----------------------|
| UC00 | SYS.PARAMETROS.VIEW_ANY, SYS.PARAMETROS.VIEW_SENSITIVE (opcional), SYS.PARAMETROS.EXPORT (opcional) |
| UC01 | SYS.PARAMETROS.CREATE |
| UC02 | SYS.PARAMETROS.VIEW, SYS.PARAMETROS.VIEW_SENSITIVE (opcional) |
| UC03 | SYS.PARAMETROS.UPDATE |
| UC04 | SYS.PARAMETROS.DELETE |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato, conformidade 100% com template oficial UC.md, cobertura completa de RF001 (15 regras de negócio, 5 UCs CRUD, permissões específicas, validações tipadas, criptografia, auditoria) |
| 1.0 | 2025-11-03 | Agência ALC - alc.dev.br | Versão inicial (não conforme ao template) |

# UC-RF019 — Casos de Uso Canônicos

**RF:** RF019 — Gestão de Tipos de Ativos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD-Cadastros-Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF019**, cobrindo integralmente o comportamento funcional esperado para a gestão de tipos de ativos de TI e Telecom.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF019.yaml)
- Massas de Teste (MT-RF019.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Tipos de Ativos | Usuário Autenticado |
| UC01 | Criar Tipo de Ativo | Usuário Autenticado |
| UC02 | Visualizar Tipo de Ativo | Usuário Autenticado |
| UC03 | Editar Tipo de Ativo | Usuário Autenticado |
| UC04 | Excluir Tipo de Ativo | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (Id_Fornecedor)
- Todas as ações exigem **permissão explícita** (RBAC policy-based)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Validações ocorrem tanto no backend (obrigatório) quanto no frontend (UX)
- Soft delete obrigatório (Fl_Ativo = 0) - NUNCA delete físico
- Multi-tenancy obrigatório em todas as queries

---

## UC00 — Listar Tipos de Ativos

### Objetivo
Permitir que o usuário visualize tipos de ativos disponíveis do seu próprio tenant, com filtros, paginação e visualização em árvore hierárquica.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.ATIVOS.TIPOS.READ_ANY`

### Pós-condições
- Lista ou árvore hierárquica exibida conforme filtros e paginação

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa o menu "Cadastros > Tipos de Ativos"
- **FP-UC00-002:** Sistema valida permissão `CAD.ATIVOS.TIPOS.READ_ANY`
- **FP-UC00-003:** Sistema carrega tipos do tenant do usuário autenticado (WHERE Id_Fornecedor = @TenantId AND Fl_Ativo = 1)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros por página)
- **FP-UC00-005:** Sistema ordena por Ordem_Exibicao ASC, Nm_Tipo ASC
- **FP-UC00-006:** Sistema calcula quantidade de ativos vinculados a cada tipo
- **FP-UC00-007:** Sistema exibe lista em formato tabela ou árvore hierárquica

### Fluxos Alternativos
- **FA-UC00-001:** Usuário aplica filtro por Categoria Principal (Hardware, Software, etc.)
  - Sistema refiltra lista mantendo apenas tipos da categoria selecionada
- **FA-UC00-002:** Usuário aplica filtro por texto (busca por código ou nome)
  - Sistema aplica LIKE %termo% em Cd_Tipo e Nm_Tipo
- **FA-UC00-003:** Usuário alterna visualização entre Tabela e Árvore Hierárquica
  - Sistema reorganiza exibição mantendo dados carregados
- **FA-UC00-004:** Usuário ordena por coluna clicável (Código, Nome, Categoria, Quantidade Ativos)
  - Sistema reordena lista mantendo filtros aplicados
- **FA-UC00-005:** Usuário expande/colapsa nós da árvore hierárquica
  - Sistema exibe/oculta subtipos filhos

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão `CAD.ATIVOS.TIPOS.READ_ANY`
  - Sistema retorna HTTP 403 Forbidden
  - Sistema exibe mensagem: "Você não tem permissão para visualizar tipos de ativos"
- **FE-UC00-002:** Nenhum tipo cadastrado no tenant
  - Sistema exibe estado vazio: "Nenhum tipo de ativo cadastrado. Clique em 'Novo Tipo' para começar"
- **FE-UC00-003:** Erro ao carregar dados do backend
  - Sistema exibe mensagem: "Erro ao carregar tipos de ativos. Tente novamente"
  - Sistema loga erro completo para troubleshooting

### Regras de Negócio
- **RN-UC-00-001:** Somente registros do tenant do usuário autenticado (isolamento multi-tenant)
- **RN-UC-00-002:** Registros com Fl_Ativo = 0 NÃO aparecem na listagem padrão
- **RN-UC-00-003:** Paginação padrão: 20 registros, máximo 100 registros por página
- **RN-UC-00-004:** Hierarquia exibida em formato visual (indentação ou árvore)
- **RN-UC-00-005:** Quantidade de ativos vinculados calculada via COUNT(Ativo WHERE Id_Ativo_Tipo = X)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas tipos de ativos do tenant do usuário autenticado
- **CA-UC00-002:** Tipos com Fl_Ativo = 0 NÃO devem aparecer na listagem padrão
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por Código, Nome, Categoria, Quantidade de Ativos
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis (categoria + busca de texto)
- **CA-UC00-006:** Visualização em árvore DEVE exibir hierarquia completa (até 5 níveis)
- **CA-UC00-007:** Quantidade de ativos vinculados DEVE ser exata e atualizada em tempo real

---

## UC01 — Criar Tipo de Ativo

### Objetivo
Permitir a criação de um novo tipo de ativo com código único, categoria, hierarquia, depreciação e campos customizados.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.ATIVOS.TIPOS.CREATE`

### Pós-condições
- Tipo de ativo criado e disponível para associação a ativos
- Registro de auditoria criado na tabela Ativo_Tipo_Auditoria
- Hierarquia recalculada se tipo tem pai

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em botão "Novo Tipo"
- **FP-UC01-002:** Sistema valida permissão `CAD.ATIVOS.TIPOS.CREATE`
- **FP-UC01-003:** Sistema exibe formulário com campos obrigatórios e opcionais
- **FP-UC01-004:** Usuário preenche campos:
  - Código (obrigatório, máx 20 caracteres, único no Fornecedor)
  - Nome (obrigatório, máx 200 caracteres)
  - Descrição (opcional, máx 1000 caracteres)
  - Categoria Principal (dropdown: Hardware, Software, LinhaMovel, LinhaFixa, Servico, Licenca, Acessorio, Outro)
  - Subcategoria (opcional)
  - Tipo Pai (dropdown com tipos existentes, opcional)
  - Flags: Inventariável, Depreciável, Rastreável, Faturável (checkboxes)
  - Taxa de Depreciação Anual (%, obrigatório se categoria = Hardware)
  - Vida Útil (anos, obrigatório se categoria = Hardware)
  - Método de Depreciação (dropdown: Linear, DeclinioAcelerado, SomaDigitos)
  - Ícone (seletor Font Awesome)
  - Cor (color picker hex)
- **FP-UC01-005:** Usuário clica em "Salvar"
- **FP-UC01-006:** Sistema valida dados:
  - Código único no Fornecedor ✓ (RN-RF019-001)
  - Categoria válida ✓ (RN-RF019-003)
  - Se categoria = Hardware, obrigatório Taxa e Vida Útil ✓ (RN-RF019-004)
  - Taxa entre 0-100% ✓ (RN-RF019-007)
  - Se tem tipo pai, calcular nível hierárquico ≤ 5 ✓ (RN-RF019-002)
  - Validar que não cria loop na hierarquia ✓ (RN-RF019-013)
- **FP-UC01-007:** Sistema calcula campos automáticos:
  - Id_Fornecedor: tenant do usuário autenticado
  - Nivel_Hierarquia: se tipo pai (nível do pai + 1), senão (1)
  - Caminho_Hierarquia: concatenação de nomes "/Pai/Filho"
  - Fl_Ativo: 1 (ativo por padrão)
  - Fl_Sistema: 0 (não é tipo de sistema)
  - Ordem_Exibicao: 100 (padrão)
- **FP-UC01-008:** Sistema cria registro na tabela Ativo_Tipo
- **FP-UC01-009:** Sistema registra auditoria:
  - Tabela: Ativo_Tipo_Auditoria
  - Tipo_Operacao: "INSERT"
  - Dados_Depois: JSON com todos os campos criados
  - Id_Usuario, Nm_Usuario, IP_Origem, Dt_Operacao
- **FP-UC01-010:** Sistema dispara evento de domínio `TipoAtivoCriado`
- **FP-UC01-011:** Sistema exibe mensagem: "Tipo de ativo criado com sucesso"
- **FP-UC01-012:** Sistema fecha formulário e atualiza lista/árvore com novo tipo

### Fluxos Alternativos
- **FA-UC01-001:** Usuário adiciona campos customizados
  - Após passo FP-UC01-004, usuário clica em aba "Campos Customizados"
  - Sistema exibe lista vazia + botão "Adicionar Campo"
  - Usuário clica em "Adicionar Campo"
  - Sistema exibe formulário: Código, Nome, Tipo de Dados, Obrigatório, Valor Padrão
  - Usuário preenche e confirma
  - Sistema adiciona campo à lista temporária
  - Ao salvar tipo (FP-UC01-008), sistema cria registros em Ativo_Tipo_Campo_Customizado
- **FA-UC01-002:** Usuário usa template pré-configurado
  - Após passo FP-UC01-003, usuário clica em "Usar Template"
  - Sistema exibe lista de templates (Desktop Padrão, Notebook Corporativo, Servidor Web)
  - Usuário seleciona template
  - Sistema pré-preenche formulário com dados do template
  - Usuário pode ajustar campos antes de salvar
- **FA-UC01-003:** Usuário cancela criação
  - Em qualquer passo antes de FP-UC01-005, usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, fecha formulário sem salvar

### Fluxos de Exceção
- **FE-UC01-001:** Código duplicado
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Já existe um tipo de ativo com o código '{Cd_Tipo}'"
  - Sistema destaca campo "Código" em vermelho
  - Retorna ao passo FP-UC01-004
- **FE-UC01-002:** Hardware sem depreciação (RN-RF019-004)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Tipos da categoria Hardware devem ter depreciação e vida útil definidas (compliance contábil)"
  - Sistema destaca campos obrigatórios em vermelho
  - Retorna ao passo FP-UC01-004
- **FE-UC01-003:** Hierarquia excede 5 níveis (RN-RF019-002)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Hierarquia não pode ter mais de 5 níveis. Tipo pai selecionado já está no nível 5"
  - Sistema desabilita campo "Tipo Pai" para seleção deste tipo
  - Retorna ao passo FP-UC01-004
- **FE-UC01-004:** Loop hierárquico detectado (RN-RF019-013)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Loop hierárquico detectado: {caminho}. Operação não permitida"
  - Sistema limpa campo "Tipo Pai"
  - Retorna ao passo FP-UC01-004
- **FE-UC01-005:** Taxa de depreciação inválida (RN-RF019-007)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Taxa de depreciação deve estar entre 0% e 100%"
  - Sistema destaca campo em vermelho
  - Retorna ao passo FP-UC01-004
- **FE-UC01-006:** Erro inesperado ao criar tipo
  - Sistema retorna HTTP 500 Internal Server Error
  - Mensagem: "Erro inesperado ao criar tipo. Tente novamente ou contate o suporte"
  - Sistema loga exceção completa para troubleshooting
  - Retorna ao passo FP-UC01-004

### Regras de Negócio
- **RN-UC-01-001:** Código obrigatório, único no Fornecedor, máx 20 caracteres
- **RN-UC-01-002:** Id_Fornecedor preenchido automaticamente com tenant do usuário autenticado
- **RN-UC-01-003:** Campos de auditoria (Dt_Criacao, Id_Usuario_Criacao) preenchidos automaticamente
- **RN-UC-01-004:** Fl_Ativo = 1 por padrão (tipo ativo)
- **RN-UC-01-005:** Fl_Sistema = 0 por padrão (não é tipo de sistema)
- **RN-UC-01-006:** Categoria Principal não pode ser alterada após criação (preservar histórico)

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** Id_Fornecedor DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** Dt_Criacao e Id_Usuario_Criacao DEVEM ser preenchidos automaticamente
- **CA-UC01-004:** Sistema DEVE retornar erro HTTP 400 se código duplicado (RN-RF019-001)
- **CA-UC01-005:** Sistema DEVE retornar erro HTTP 400 se Hardware sem depreciação (RN-RF019-004)
- **CA-UC01-006:** Sistema DEVE retornar erro HTTP 400 se hierarquia > 5 níveis (RN-RF019-002)
- **CA-UC01-007:** Sistema DEVE detectar e bloquear loops hierárquicos (RN-RF019-013)
- **CA-UC01-008:** Auditoria DEVE ser registrada com Tipo_Operacao="INSERT" e Dados_Depois JSON completo
- **CA-UC01-009:** Caminho_Hierarquia DEVE ser calculado automaticamente no formato "/Pai/Filho"
- **CA-UC01-010:** Campos customizados DEVEM ser salvos em Ativo_Tipo_Campo_Customizado

---

## UC02 — Visualizar Tipo de Ativo

### Objetivo
Permitir visualização detalhada de um tipo de ativo específico, incluindo hierarquia, campos customizados, quantidade de ativos e dados de auditoria.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.ATIVOS.TIPOS.READ`
- Tipo de ativo existe e pertence ao tenant do usuário

### Pós-condições
- Detalhes completos do tipo exibidos

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona um tipo na lista/árvore ou clica em ícone "Visualizar"
- **FP-UC02-002:** Sistema valida permissão `CAD.ATIVOS.TIPOS.READ`
- **FP-UC02-003:** Sistema valida que tipo pertence ao tenant do usuário autenticado
- **FP-UC02-004:** Sistema busca dados completos do tipo (incluindo tipo pai, subtipos, campos customizados)
- **FP-UC02-005:** Sistema calcula quantidade de ativos vinculados
- **FP-UC02-006:** Sistema exibe painel/modal com seções:
  - **Identificação:** Código, Nome, Descrição
  - **Classificação:** Categoria, Subcategoria, Tipo Pai (link clicável), Caminho Hierárquico Completo, Nível Hierárquico
  - **Características:** Flags (Inventariável, Depreciável, Rastreável, Faturável, Requer Serial, IMEI, MAC)
  - **Depreciação:** Taxa Anual %, Vida Útil (anos), Método de Depreciação
  - **Visual:** Ícone (preview), Cor (preview colorido)
  - **Hierarquia:** Quantidade de Subtipos, Lista de Subtipos (links clicáveis)
  - **Uso:** Quantidade de Ativos Vinculados (botão "Ver Ativos" que abre lista filtrada)
  - **Campos Customizados:** Lista de campos definidos (Código, Nome, Tipo, Obrigatório, Valor Padrão)
  - **Auditoria:** Data Criação, Usuário Criação, Data Última Alteração, Usuário Última Alteração
- **FP-UC02-007:** Usuário pode navegar para tipo pai, subtipos ou ver lista de ativos vinculados

### Fluxos Alternativos
- **FA-UC02-001:** Usuário navega para tipo pai
  - Usuário clica no link do tipo pai
  - Sistema carrega visualização do tipo pai (UC02 recursivo)
- **FA-UC02-002:** Usuário navega para subtipo
  - Usuário clica em um subtipo da lista
  - Sistema carrega visualização do subtipo (UC02 recursivo)
- **FA-UC02-003:** Usuário visualiza lista de ativos vinculados
  - Usuário clica em botão "Ver Ativos" (exibido se quantidade > 0)
  - Sistema abre tela de listagem de ativos filtrada por Id_Ativo_Tipo

### Fluxos de Exceção
- **FE-UC02-001:** Tipo inexistente
  - Sistema retorna HTTP 404 Not Found
  - Mensagem: "Tipo de ativo não encontrado"
  - Sistema redireciona para lista de tipos
- **FE-UC02-002:** Tipo pertence a outro tenant (violação multi-tenancy)
  - Sistema retorna HTTP 404 Not Found (não vazar informação de existência)
  - Mensagem: "Tipo de ativo não encontrado"
  - Sistema loga tentativa de acesso cross-tenant para auditoria de segurança

### Regras de Negócio
- **RN-UC-02-001:** Isolamento por tenant (WHERE Id_Fornecedor = @TenantId)
- **RN-UC-02-002:** Informações de auditoria DEVEM ser exibidas
- **RN-UC-02-003:** Quantidade de ativos calculada em tempo real via COUNT

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar tipos do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (datas e usuários)
- **CA-UC02-003:** Tentativa de acessar tipo de outro tenant DEVE retornar HTTP 404
- **CA-UC02-004:** Tentativa de acessar tipo inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Links para tipo pai e subtipos DEVEM ser clicáveis e funcionais
- **CA-UC02-007:** Quantidade de ativos vinculados DEVE ser exata

---

## UC03 — Editar Tipo de Ativo

### Objetivo
Permitir alteração controlada de um tipo de ativo existente, preservando integridade referencial e auditoria completa (antes/depois).

### Pré-condições
- Usuário autenticado
- Permissão `CAD.ATIVOS.TIPOS.UPDATE`
- Tipo de ativo existe e pertence ao tenant do usuário
- Tipo não é de sistema (Fl_Sistema = 0)

### Pós-condições
- Tipo atualizado com novos dados
- Registro de auditoria criado com Dados_Antes e Dados_Depois
- Hierarquia recalculada se tipo pai foi alterado

### Fluxo Principal
- **FP-UC03-001:** Usuário seleciona tipo na lista e clica em "Editar"
- **FP-UC03-002:** Sistema valida permissão `CAD.ATIVOS.TIPOS.UPDATE`
- **FP-UC03-003:** Sistema valida que tipo pertence ao tenant do usuário
- **FP-UC03-004:** Sistema valida que Fl_Sistema = 0 (não é tipo de sistema)
- **FP-UC03-005:** Sistema carrega formulário pré-preenchido com dados atuais
- **FP-UC03-006:** Sistema captura snapshot dos dados originais (para auditoria)
- **FP-UC03-007:** Usuário altera campos permitidos:
  - Nome, Descrição, Subcategoria
  - Tipo Pai (recalcula hierarquia)
  - Taxa de Depreciação, Vida Útil, Método de Depreciação
  - Flags (Inventariável, Depreciável, Rastreável, Faturável)
  - Ícone, Cor, Ordem de Exibição
- **FP-UC03-008:** Usuário clica em "Salvar"
- **FP-UC03-009:** Sistema valida alterações (mesmas validações de UC01)
- **FP-UC03-010:** Se tipo pai foi alterado, sistema recalcula hierarquia:
  - Recalcula Nivel_Hierarquia e Caminho_Hierarquia do tipo editado
  - Recalcula recursivamente todos os descendentes (RN-RF019-009)
  - Valida que hierarquia não excede 5 níveis (RN-RF019-002)
  - Valida que não cria loop (RN-RF019-013)
- **FP-UC03-011:** Sistema atualiza registro na tabela Ativo_Tipo
- **FP-UC03-012:** Sistema atualiza campos de auditoria:
  - Dt_Ult_Atualizacao: timestamp atual
  - Id_Usuario_Atualizacao: ID do usuário autenticado
- **FP-UC03-013:** Sistema registra auditoria:
  - Tabela: Ativo_Tipo_Auditoria
  - Tipo_Operacao: "UPDATE"
  - Dados_Antes: JSON com dados originais (snapshot do passo FP-UC03-006)
  - Dados_Depois: JSON com novos dados
  - Id_Usuario, Nm_Usuario, IP_Origem, Dt_Operacao
- **FP-UC03-014:** Sistema dispara evento de domínio `TipoAtivoAtualizado`
- **FP-UC03-015:** Sistema exibe mensagem: "Tipo de ativo atualizado com sucesso"
- **FP-UC03-016:** Sistema fecha formulário e atualiza lista/árvore

### Fluxos Alternativos
- **FA-UC03-001:** Usuário cancela edição
  - Em qualquer passo antes de FP-UC03-008, usuário clica em "Cancelar"
  - Sistema exibe confirmação: "Descartar alterações?"
  - Se confirmado, fecha formulário sem salvar

### Fluxos de Exceção
- **FE-UC03-001:** Tipo de sistema (Fl_Sistema = 1) (RN-RF019-008)
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Tipos de sistema não podem ser editados"
  - Sistema fecha formulário
- **FE-UC03-002:** Tentativa de alterar Código (campo imutável)
  - Sistema desabilita campo "Código" no formulário
  - Se tentativa de alterar via API: HTTP 400 "Código não pode ser alterado"
- **FE-UC03-003:** Tentativa de alterar Categoria Principal (campo imutável)
  - Sistema desabilita campo "Categoria Principal" no formulário
  - Se tentativa de alterar via API: HTTP 400 "Categoria Principal não pode ser alterada após criação"
- **FE-UC03-004:** Hierarquia excede 5 níveis após alteração de tipo pai
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Alteração de tipo pai causaria hierarquia > 5 níveis. Operação bloqueada"
  - Retorna ao passo FP-UC03-007
- **FE-UC03-005:** Loop hierárquico detectado após alteração de tipo pai
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Alteração de tipo pai criaria loop hierárquico: {caminho}"
  - Retorna ao passo FP-UC03-007

### Regras de Negócio
- **RN-UC-03-001:** Dt_Ult_Atualizacao e Id_Usuario_Atualizacao preenchidos automaticamente
- **RN-UC-03-002:** Campos imutáveis: Cd_Tipo, Categoria_Principal, Id_Fornecedor
- **RN-UC-03-003:** Tipos de sistema (Fl_Sistema = 1) NÃO são editáveis (RN-RF019-008)
- **RN-UC-03-004:** Se tipo pai mudou, recalcular hierarquia de descendentes (RN-RF019-009)
- **RN-UC-03-005:** Auditoria DEVE registrar estado anterior e novo estado (Dados_Antes/Dados_Depois)

### Critérios de Aceite
- **CA-UC03-001:** Dt_Ult_Atualizacao e Id_Usuario_Atualizacao DEVEM ser preenchidos automaticamente
- **CA-UC03-002:** Sistema DEVE impedir edição de tipos de sistema (Fl_Sistema = 1) com HTTP 403
- **CA-UC03-003:** Campos Código e Categoria Principal NÃO devem ser editáveis
- **CA-UC03-004:** Se tipo pai mudou, hierarquia DEVE ser recalculada recursivamente para descendentes
- **CA-UC03-005:** Auditoria DEVE registrar Dados_Antes e Dados_Depois em formato JSON
- **CA-UC03-006:** Sistema DEVE validar hierarquia máxima (5 níveis) após alteração de tipo pai
- **CA-UC03-007:** Sistema DEVE detectar e bloquear loops hierárquicos após alteração de tipo pai

---

## UC04 — Excluir Tipo de Ativo

### Objetivo
Permitir exclusão lógica (soft delete) de tipos de ativos que não estão em uso, preservando integridade referencial.

### Pré-condições
- Usuário autenticado
- Permissão `CAD.ATIVOS.TIPOS.DELETE`
- Tipo de ativo existe e pertence ao tenant do usuário
- Tipo não é de sistema (Fl_Sistema = 0)
- Tipo não possui ativos vinculados (COUNT(Ativo WHERE Id_Ativo_Tipo = X) = 0)
- Tipo não possui subtipos ativos (COUNT(Ativo_Tipo WHERE Id_Tipo_Pai = X AND Fl_Ativo = 1) = 0)

### Pós-condições
- Tipo marcado como inativo (Fl_Ativo = 0)
- Registro de auditoria criado
- Tipo removido de listagens padrão
- Possibilidade de restauração posterior (apenas Super Admin)

### Fluxo Principal
- **FP-UC04-001:** Usuário seleciona tipo na lista e clica em "Excluir"
- **FP-UC04-002:** Sistema valida permissão `CAD.ATIVOS.TIPOS.DELETE`
- **FP-UC04-003:** Sistema valida que tipo pertence ao tenant do usuário
- **FP-UC04-004:** Sistema valida pré-condições:
  - Fl_Sistema = 0 (não é tipo de sistema) ✓
  - Não tem ativos vinculados ✓ (RN-RF019-005)
  - Não tem subtipos ativos ✓ (RN-RF019-006)
- **FP-UC04-005:** Sistema exibe modal de confirmação:
  - Título: "Confirmar Exclusão"
  - Mensagem: "Deseja realmente inativar o tipo '{Nm_Tipo}'?"
  - Submensagem: "Esta ação pode ser revertida posteriormente (apenas por Super Admin)"
  - Botões: Cancelar (padrão), Confirmar Exclusão (destrutivo)
- **FP-UC04-006:** Usuário clica em "Confirmar Exclusão"
- **FP-UC04-007:** Sistema captura snapshot dos dados originais (para auditoria)
- **FP-UC04-008:** Sistema executa soft delete:
  - UPDATE Ativo_Tipo SET Fl_Ativo = 0 WHERE Id_Ativo_Tipo = X
  - Dt_Ult_Atualizacao = timestamp atual
  - Id_Usuario_Atualizacao = ID do usuário autenticado
- **FP-UC04-009:** Sistema registra auditoria:
  - Tabela: Ativo_Tipo_Auditoria
  - Tipo_Operacao: "DELETE"
  - Dados_Antes: JSON com dados antes da exclusão
  - Dados_Depois: NULL
  - Id_Usuario, Nm_Usuario, IP_Origem, Dt_Operacao
- **FP-UC04-010:** Sistema dispara evento de domínio `TipoAtivoExcluido`
- **FP-UC04-011:** Sistema exibe mensagem: "Tipo de ativo inativado com sucesso"
- **FP-UC04-012:** Sistema remove tipo da lista/árvore (atualiza UI)

### Fluxos Alternativos
- **FA-UC04-001:** Usuário cancela exclusão
  - Após passo FP-UC04-005, usuário clica em "Cancelar"
  - Sistema fecha modal sem executar exclusão

### Fluxos de Exceção
- **FE-UC04-001:** Tipo de sistema (Fl_Sistema = 1) (RN-RF019-008)
  - Sistema retorna HTTP 403 Forbidden
  - Mensagem: "Tipos de sistema não podem ser excluídos"
  - Modal não é exibido
- **FE-UC04-002:** Tipo com ativos vinculados (RN-RF019-005)
  - Sistema busca quantidade de ativos: COUNT(Ativo WHERE Id_Ativo_Tipo = X AND Fl_Ativo = 1)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Não é possível excluir este tipo pois existem {quantidade} ativos associados. Reclassifique os ativos primeiro"
  - Sistema exibe botão "Ver Ativos" que abre lista filtrada
  - Modal não é exibido
- **FE-UC04-003:** Tipo com subtipos ativos (RN-RF019-006)
  - Sistema busca quantidade de subtipos: COUNT(Ativo_Tipo WHERE Id_Tipo_Pai = X AND Fl_Ativo = 1)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Não é possível excluir este tipo pois existem {quantidade} subtipos ativos. Inactive os subtipos primeiro ou altere o tipo pai deles"
  - Sistema exibe lista de subtipos afetados
  - Modal não é exibido
- **FE-UC04-004:** Tipo já excluído (Fl_Ativo = 0)
  - Sistema retorna HTTP 400 Bad Request
  - Mensagem: "Tipo de ativo já está inativo"
  - Sistema atualiza lista/árvore

### Regras de Negócio
- **RN-UC-04-001:** Exclusão SEMPRE lógica (soft delete via Fl_Ativo = 0) - NUNCA delete físico
- **RN-UC-04-002:** Tipos com ativos vinculados NÃO podem ser excluídos (RN-RF019-005)
- **RN-UC-04-003:** Tipos com subtipos ativos NÃO podem ser excluídos (RN-RF019-006)
- **RN-UC-04-004:** Tipos de sistema (Fl_Sistema = 1) NÃO podem ser excluídos (RN-RF019-008)
- **RN-UC-04-005:** Confirmação explícita do usuário é obrigatória

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via Fl_Ativo = 0
- **CA-UC04-002:** Sistema DEVE verificar ativos vinculados ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE verificar subtipos ativos ANTES de permitir exclusão
- **CA-UC04-004:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-005:** Tentativa de excluir tipo com ativos DEVE retornar HTTP 400 com mensagem clara
- **CA-UC04-006:** Tentativa de excluir tipo com subtipos DEVE retornar HTTP 400 com lista de subtipos
- **CA-UC04-007:** Tentativa de excluir tipo de sistema DEVE retornar HTTP 403
- **CA-UC04-008:** Tipo excluído NÃO deve aparecer em listagens padrão
- **CA-UC04-009:** Auditoria DEVE ser registrada com Tipo_Operacao="DELETE" e Dados_Antes completo

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio RF019 |
|----|-------------------------|
| UC00 | RN-RF019-001, RN-RF019-012 |
| UC01 | RN-RF019-001, RN-RF019-002, RN-RF019-003, RN-RF019-004, RN-RF019-007, RN-RF019-010, RN-RF019-011, RN-RF019-013 |
| UC02 | RN-RF019-001, RN-RF019-002, RN-RF019-010 |
| UC03 | RN-RF019-002, RN-RF019-004, RN-RF019-007, RN-RF019-008, RN-RF019-009, RN-RF019-010, RN-RF019-013 |
| UC04 | RN-RF019-005, RN-RF019-006, RN-RF019-008, RN-RF019-010, RN-RF019-015 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Migração v1.0 → v2.0: template canônico, adição de UC00, cobertura total RF019 |
| 1.0 | 2025-12-17 | Sistema | Versão inicial consolidada (4 UCs) |

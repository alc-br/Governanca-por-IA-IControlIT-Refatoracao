# UC-RF063 — Casos de Uso Canônicos

**RF:** RF063 — Motor de Templates (Template Engine)
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC004-TPL-Templates
**Fase:** Fase-2-Cadastros-e-Servicos-Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF063 - Motor de Templates (Template Engine)**, cobrindo integralmente o comportamento funcional esperado do motor de processamento de templates dinâmicos.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF063.yaml)
- Massas de Teste (MT-RF063.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

O motor de templates permite criação e gerenciamento de templates dinâmicos com sintaxe Liquid para geração de e-mails, relatórios, documentos e notificações, com suporte a versionamento, preview em tempo real, herança, parciais, i18n, cache e validações de segurança.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Templates | Usuário Autenticado |
| UC01 | Criar Template | Usuário Autenticado |
| UC02 | Visualizar Template | Usuário Autenticado |
| UC03 | Editar Template | Usuário Autenticado |
| UC04 | Arquivar Template | Usuário Autenticado |
| UC05 | Renderizar Template | Sistema/Usuário Autenticado |
| UC06 | Gerar Preview de Template | Usuário Autenticado |
| UC07 | Criar Nova Versão | Usuário Autenticado |
| UC08 | Executar Rollback de Versão | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (EmpresaId)
- Todas as ações exigem **permissão explícita** (TPL.ENGINE.*)
- Validação de sintaxe Liquid é obrigatória antes de salvar (RN-RF063-006)
- Sanitização HTML automática contra XSS (RN-RF063-011)
- Versionamento obrigatório em toda alteração (RN-RF063-005)
- Cache Redis de templates compilados (RN-RF063-012)
- Auditoria completa de operações (RN-RF063-014)
- Mensagens de erro devem ser claras, localizadas e não vazar informações sensíveis
- Templates globais (sistema) são acessíveis por todos os tenants

---

## UC00 — Listar Templates

### Objetivo
Permitir que o usuário visualize templates disponíveis do seu tenant, com suporte a filtros por tipo, estado e busca textual.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.VIEW_ANY`

### Pós-condições
- Lista de templates exibida conforme filtros aplicados
- Paginação aplicada (padrão: 20 registros)

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade de templates
- **FP-UC00-002:** Sistema valida permissão `TPL.ENGINE.VIEW_ANY`
- **FP-UC00-003:** Sistema carrega templates do tenant do usuário
- **FP-UC00-004:** Sistema aplica paginação e ordenação padrão (data criação DESC)
- **FP-UC00-005:** Sistema exibe lista com: nome, tipo, estado, versão ativa, data última atualização

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por nome ou descrição do template
- **FA-UC00-002:** Filtrar por tipo (email, relatorio, documento, notificacao)
- **FA-UC00-003:** Filtrar por estado (draft, active, archived, testing)
- **FA-UC00-004:** Ordenar por nome, data criação ou data atualização
- **FA-UC00-005:** Incluir templates globais (sistema) na listagem

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 + mensagem "Acesso negado. Permissão TPL.ENGINE.VIEW_ANY necessária"
- **FE-UC00-002:** Nenhum template encontrado → estado vazio com mensagem "Nenhum template encontrado. Crie o primeiro template."

### Regras de Negócio
- **RN-UC-00-001:** Somente templates do tenant do usuário devem ser exibidos (exceto templates globais)
- **RN-UC-00-002:** Templates arquivados aparecem na listagem com indicador visual
- **RN-UC-00-003:** Paginação padrão de 20 registros por página
- **RN-UC-00-004:** Templates globais (EmpresaId = NULL) são visíveis para todos
- **RN-RF063-015:** Isolamento multi-tenant obrigatório

### Critérios de Aceite
- **CA-UC00-001:** Lista DEVE exibir apenas templates do tenant do usuário autenticado + templates globais
- **CA-UC00-002:** Templates arquivados DEVEM aparecer com indicador visual claro (ícone/badge)
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL (query parameters)
- **CA-UC00-006:** Busca textual DEVE pesquisar em nome e descrição simultaneamente

---

## UC01 — Criar Template

### Objetivo
Permitir criação de novo template dinâmico com sintaxe Liquid, definindo tipo, conteúdo, contexto de dados e configurações.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.CREATE`

### Pós-condições
- Template criado em estado `draft`
- Versão 1 gerada automaticamente
- Auditoria registrada (quem criou, quando)

### Fluxo Principal
- **FP-UC01-001:** Usuário solicita criação de novo template
- **FP-UC01-002:** Sistema valida permissão `TPL.ENGINE.CREATE`
- **FP-UC01-003:** Sistema exibe formulário com campos: nome, descrição, tipo, conteúdo Liquid, contexto de teste
- **FP-UC01-004:** Usuário preenche campos obrigatórios
- **FP-UC01-005:** Sistema valida sintaxe Liquid em tempo real (RN-RF063-006)
- **FP-UC01-006:** Usuário confirma criação
- **FP-UC01-007:** Sistema valida dados completos
- **FP-UC01-008:** Sistema cria template em estado `draft` com versão 1
- **FP-UC01-009:** Sistema registra auditoria (template.criado)
- **FP-UC01-010:** Sistema exibe mensagem de sucesso + botão "Visualizar Preview"

### Fluxos Alternativos
- **FA-UC01-001:** Salvar e criar outro template
- **FA-UC01-002:** Cancelar criação (confirmação se houver alterações)
- **FA-UC01-003:** Selecionar layout base para herança (RN-RF063-008)
- **FA-UC01-004:** Adicionar parciais reutilizáveis (RN-RF063-009)
- **FA-UC01-005:** Configurar filtros customizados disponíveis

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação de sintaxe Liquid → destacar linha/coluna com erro + mensagem descritiva
- **FE-UC01-002:** Nome duplicado no tenant → mensagem "Já existe template com este nome"
- **FE-UC01-003:** Variável não existente no contexto → warning (não bloqueante, permitir salvar)
- **FE-UC01-004:** Erro inesperado → rollback + log + mensagem genérica

### Regras de Negócio
- **RN-UC-01-001:** Campos obrigatórios: nome, tipo, conteúdo
- **RN-UC-01-002:** EmpresaId preenchido automaticamente com tenant do usuário
- **RN-UC-01-003:** created_by preenchido automaticamente com ID do usuário
- **RN-UC-01-004:** Estado inicial sempre `draft`
- **RN-UC-01-005:** Versão inicial sempre 1
- **RN-RF063-001:** Sintaxe Liquid obrigatória
- **RN-RF063-006:** Validação de sintaxe bloqueante

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** EmpresaId DEVE ser preenchido automaticamente com tenant do usuário
- **CA-UC01-003:** created_by DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC01-004:** created_at DEVE ser preenchido com timestamp UTC atual
- **CA-UC01-005:** Estado inicial DEVE ser `draft`
- **CA-UC01-006:** Versão inicial DEVE ser 1
- **CA-UC01-007:** Validação de sintaxe Liquid DEVE ocorrer antes de salvar
- **CA-UC01-008:** Erros de sintaxe DEVEM impedir salvamento e exibir mensagem clara
- **CA-UC01-009:** Auditoria DEVE ser registrada APÓS sucesso da criação

---

## UC02 — Visualizar Template

### Objetivo
Permitir visualização detalhada de um template, incluindo conteúdo, versões, histórico de uso e preview renderizado.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.VIEW`
- Template pertence ao tenant do usuário OU é template global

### Pós-condições
- Dados do template exibidos corretamente
- Histórico de versões acessível

### Fluxo Principal
- **FP-UC02-001:** Usuário seleciona template na listagem
- **FP-UC02-002:** Sistema valida permissão `TPL.ENGINE.VIEW`
- **FP-UC02-003:** Sistema valida que template pertence ao tenant OU é global
- **FP-UC02-004:** Sistema carrega dados do template + versão ativa
- **FP-UC02-005:** Sistema exibe: nome, descrição, tipo, estado, conteúdo Liquid, contexto, versão ativa, data criação/atualização, criado por/atualizado por
- **FP-UC02-006:** Sistema exibe histórico de versões (versão, data, usuário)
- **FP-UC02-007:** Sistema exibe botão "Gerar Preview"

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar versão específica (não ativa)
- **FA-UC02-002:** Comparar versão atual com versão anterior (diff)
- **FA-UC02-003:** Visualizar auditoria de uso (quando foi renderizado, por quem)
- **FA-UC02-004:** Copiar template como novo (duplicar)

### Fluxos de Exceção
- **FE-UC02-001:** Template inexistente → HTTP 404 + mensagem "Template não encontrado"
- **FE-UC02-002:** Template de outro tenant → HTTP 403 + mensagem "Acesso negado"
- **FE-UC02-003:** Versão específica inexistente → HTTP 404 + mensagem "Versão não encontrada"

### Regras de Negócio
- **RN-UC-02-001:** Usuário SÓ pode visualizar templates do próprio tenant OU templates globais
- **RN-UC-02-002:** Informações de auditoria DEVEM ser exibidas (created_by, created_at, updated_by, updated_at)
- **RN-UC-02-003:** Histórico de versões ordenado DESC (mais recente primeiro)
- **RN-RF063-015:** Isolamento multi-tenant obrigatório

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar templates do próprio tenant OU globais
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (created_by, created_at, updated_by, updated_at)
- **CA-UC02-003:** Tentativa de acessar template de outro tenant DEVE retornar HTTP 403
- **CA-UC02-004:** Tentativa de acessar template inexistente DEVE retornar HTTP 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Histórico de versões DEVE incluir: número, data, usuário, estado

---

## UC03 — Editar Template

### Objetivo
Permitir alteração de template existente, criando nova versão automaticamente e validando sintaxe Liquid.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.EDIT`
- Template em estado `draft` OU `active`
- Template pertence ao tenant do usuário

### Pós-condições
- Template atualizado
- Nova versão criada
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário solicita edição de template
- **FP-UC03-002:** Sistema valida permissão `TPL.ENGINE.EDIT`
- **FP-UC03-003:** Sistema valida que template pertence ao tenant
- **FP-UC03-004:** Sistema valida que template NÃO está arquivado
- **FP-UC03-005:** Sistema carrega dados do template em formulário editável
- **FP-UC03-006:** Usuário altera campos (nome, descrição, conteúdo, contexto)
- **FP-UC03-007:** Sistema valida sintaxe Liquid em tempo real
- **FP-UC03-008:** Usuário confirma salvamento
- **FP-UC03-009:** Sistema valida alterações
- **FP-UC03-010:** Sistema cria nova versão (versão anterior + 1)
- **FP-UC03-011:** Sistema atualiza campos de auditoria (updated_by, updated_at)
- **FP-UC03-012:** Sistema invalida cache Redis do template
- **FP-UC03-013:** Sistema registra auditoria (template.versionado)
- **FP-UC03-014:** Sistema exibe mensagem de sucesso + número da nova versão

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição (confirmação se houver alterações)
- **FA-UC03-002:** Publicar template após edição (mudar de `draft` para `active`)
- **FA-UC03-003:** Salvar como rascunho (manter em `draft`)
- **FA-UC03-004:** Comparar com versão anterior antes de salvar

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação de sintaxe Liquid → bloquear salvamento + destacar erro
- **FE-UC03-002:** Conflito de edição concorrente → detectar via ETag/timestamp + avisar usuário
- **FE-UC03-003:** Template arquivado → mensagem "Templates arquivados não podem ser editados"
- **FE-UC03-004:** Template de outro tenant → HTTP 403

### Regras de Negócio
- **RN-UC-03-001:** updated_by DEVE ser preenchido automaticamente com ID do usuário autenticado
- **RN-UC-03-002:** updated_at DEVE ser preenchido automaticamente com timestamp UTC atual
- **RN-UC-03-003:** Nova versão DEVE ser criada a cada salvamento
- **RN-UC-03-004:** Apenas versão mais recente pode ser editada
- **RN-UC-03-005:** Cache Redis DEVE ser invalidado ao salvar
- **RN-RF063-005:** Versionamento obrigatório
- **RN-RF063-006:** Validação de sintaxe bloqueante
- **RN-RF063-012:** Cache deve ser invalidado

### Critérios de Aceite
- **CA-UC03-001:** updated_by DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** updated_at DEVE ser preenchido automaticamente com timestamp UTC atual
- **CA-UC03-003:** Nova versão DEVE ser criada automaticamente
- **CA-UC03-004:** Sistema DEVE detectar conflitos de edição concorrente (via ETag ou version)
- **CA-UC03-005:** Tentativa de editar template de outro tenant DEVE retornar HTTP 403
- **CA-UC03-006:** Tentativa de editar template arquivado DEVE retornar erro claro
- **CA-UC03-007:** Cache Redis DEVE ser invalidado automaticamente
- **CA-UC03-008:** Auditoria DEVE registrar estado anterior e novo estado

---

## UC04 — Arquivar Template

### Objetivo
Permitir arquivamento lógico de template, removendo-o do uso ativo sem deletar dados.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.ARCHIVE`
- Template em estado `draft`, `active` ou `testing`

### Pós-condições
- Template movido para estado `archived`
- Template não aparece em listagens padrão
- Histórico preservado

### Fluxo Principal
- **FP-UC04-001:** Usuário solicita arquivamento de template
- **FP-UC04-002:** Sistema exibe confirmação: "Tem certeza que deseja arquivar este template?"
- **FP-UC04-003:** Sistema valida permissão `TPL.ENGINE.ARCHIVE`
- **FP-UC04-004:** Sistema verifica se template está em uso ativo (jobs agendados, fluxos críticos)
- **FP-UC04-005:** Sistema altera estado para `archived`
- **FP-UC04-006:** Sistema invalida cache Redis
- **FP-UC04-007:** Sistema registra auditoria (template.arquivado)
- **FP-UC04-008:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar arquivamento
- **FA-UC04-002:** Desarquivar template (mover de `archived` para `draft`)

### Fluxos de Exceção
- **FE-UC04-001:** Template em uso ativo → bloquear arquivamento + listar onde está sendo usado
- **FE-UC04-002:** Template já arquivado → mensagem "Template já está arquivado"
- **FE-UC04-003:** Template de outro tenant → HTTP 403

### Regras de Negócio
- **RN-UC-04-001:** Arquivamento é lógico (mudança de estado, não deleção)
- **RN-UC-04-002:** Templates em uso ativo NÃO podem ser arquivados
- **RN-UC-04-003:** Templates arquivados NÃO aparecem em listagens padrão (filtro necessário)
- **RN-UC-04-004:** Templates arquivados podem ser desarquivados
- **RN-UC-04-005:** Cache Redis DEVE ser invalidado

### Critérios de Aceite
- **CA-UC04-001:** Arquivamento DEVE ser lógico (mudança de estado para `archived`)
- **CA-UC04-002:** Sistema DEVE verificar uso ativo ANTES de permitir arquivamento
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** Estado alterado para `archived` com timestamp
- **CA-UC04-005:** Tentativa de arquivar template em uso DEVE retornar erro claro com lista de dependências
- **CA-UC04-006:** Template arquivado NÃO deve aparecer em listagens padrão
- **CA-UC04-007:** Cache Redis DEVE ser invalidado

---

## UC05 — Renderizar Template

### Objetivo
Processar template Liquid com contexto de dados fornecido, gerando HTML/texto final pronto para uso.

### Pré-condições
- Sistema/Usuário autenticado
- Permissão `TPL.ENGINE.RENDER` (quando chamado por usuário)
- Template em estado `active`
- Contexto de dados válido fornecido

### Pós-condições
- HTML/texto renderizado gerado
- Auditoria de uso registrada
- Cache atualizado (se aplicável)

### Fluxo Principal
- **FP-UC05-001:** Sistema/Usuário solicita renderização de template
- **FP-UC05-002:** Sistema valida permissão (se chamado por usuário)
- **FP-UC05-003:** Sistema valida que template está em estado `active`
- **FP-UC05-004:** Sistema verifica cache Redis para template compilado
- **FP-UC05-005:** Se cache miss → sistema compila template Liquid
- **FP-UC05-006:** Sistema armazena template compilado em cache Redis (TTL 1h)
- **FP-UC05-007:** Sistema aplica contexto de dados ao template
- **FP-UC05-008:** Sistema aplica filtros customizados (currency, formatarData, truncar)
- **FP-UC05-009:** Sistema processa condicionais, loops e includes
- **FP-UC05-010:** Sistema sanitiza HTML automaticamente (exceto se flag `raw`)
- **FP-UC05-011:** Sistema registra auditoria (template.renderizado)
- **FP-UC05-012:** Sistema retorna HTML/texto renderizado

### Fluxos Alternativos
- **FA-UC05-001:** Renderizar com dados de teste (preview)
- **FA-UC05-002:** Renderizar com flag `raw` para variável específica (desabilitar sanitização)
- **FA-UC05-003:** Renderizar template com herança (layout base + filho)
- **FA-UC05-004:** Renderizar template com parciais incluídas

### Fluxos de Exceção
- **FE-UC05-001:** Template inativo → erro "Template não está ativo para uso"
- **FE-UC05-002:** Erro de sintaxe em runtime → log + retornar placeholder ou template fallback
- **FE-UC05-003:** Variável não encontrada no contexto → exibir placeholder `[variavel.ausente]`
- **FE-UC05-004:** Timeout de renderização (>5s) → abortar + log + alerta
- **FE-UC05-005:** Cache Redis indisponível → compilar sem cache (performance degradada)

### Regras de Negócio
- **RN-UC-05-001:** Apenas templates em estado `active` podem ser renderizados
- **RN-UC-05-002:** Sanitização HTML automática (exceto flag `raw` explícita)
- **RN-UC-05-003:** Variáveis ausentes geram placeholder, não erro
- **RN-UC-05-004:** Cache Redis com TTL de 1 hora
- **RN-UC-05-005:** Timeout máximo de renderização: 5 segundos
- **RN-RF063-002:** Contexto de dados tipado
- **RN-RF063-003:** Filtros customizados obrigatórios
- **RN-RF063-011:** Sanitização HTML contra XSS
- **RN-RF063-012:** Cache de templates compilados

### Critérios de Aceite
- **CA-UC05-001:** Apenas templates `active` DEVEM ser renderizados
- **CA-UC05-002:** Cache Redis DEVE ser consultado antes de compilar
- **CA-UC05-003:** Template compilado DEVE ser armazenado em cache com TTL de 1 hora
- **CA-UC05-004:** Variáveis DEVEM ser sanitizadas automaticamente (exceto `raw`)
- **CA-UC05-005:** Variáveis ausentes DEVEM gerar placeholder `[variavel.ausente]` e não erro
- **CA-UC05-006:** Filtros `currency`, `formatarData`, `truncar` DEVEM funcionar corretamente
- **CA-UC05-007:** Herança de templates DEVE funcionar recursivamente
- **CA-UC05-008:** Parciais DEVEM ter acesso ao contexto global
- **CA-UC05-009:** Auditoria DEVE registrar: template ID, versão, contexto, data, usuário
- **CA-UC05-010:** Timeout DEVE abortar renderização após 5 segundos

---

## UC06 — Gerar Preview de Template

### Objetivo
Gerar preview em tempo real do template com dados de teste, permitindo validação visual antes de publicar.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.EDIT` ou `TPL.ENGINE.CREATE`
- Template com conteúdo Liquid válido

### Pós-condições
- Preview HTML renderizado exibido
- Erros de sintaxe destacados (se houver)

### Fluxo Principal
- **FP-UC06-001:** Usuário solicita preview de template (durante criação/edição)
- **FP-UC06-002:** Sistema valida sintaxe Liquid
- **FP-UC06-003:** Sistema carrega contexto de teste padrão OU contexto fornecido pelo usuário
- **FP-UC06-004:** Sistema renderiza template com contexto de teste
- **FP-UC06-005:** Sistema exibe lado a lado: código Liquid (esquerda) + preview renderizado (direita)
- **FP-UC06-006:** Sistema destaca variáveis não encontradas com placeholder `[variavel.ausente]`

### Fluxos Alternativos
- **FA-UC06-001:** Editar contexto de teste e re-gerar preview
- **FA-UC06-002:** Alternar entre modos: Desktop / Tablet / Mobile (responsividade)
- **FA-UC06-003:** Copiar HTML renderizado para área de transferência
- **FA-UC06-004:** Visualizar preview em idioma específico (i18n)

### Fluxos de Exceção
- **FE-UC06-001:** Erro de sintaxe Liquid → destacar linha/coluna com erro + mensagem descritiva
- **FE-UC06-002:** Contexto de teste inválido → mensagem "Contexto JSON inválido"
- **FE-UC06-003:** Timeout de renderização → mensagem "Preview demorou muito (>5s)"

### Regras de Negócio
- **RN-UC-06-001:** Preview NÃO cria versão (é apenas visualização)
- **RN-UC-06-002:** Contexto de teste DEVE ser JSON válido
- **RN-UC-06-003:** Erros de sintaxe DEVEM ser destacados visualmente
- **RN-UC-06-004:** Preview em tempo real (debounce de 500ms após parar de digitar)
- **RN-RF063-004:** Preview em tempo real obrigatório
- **RN-RF063-006:** Validação de sintaxe bloqueante

### Critérios de Aceite
- **CA-UC06-001:** Preview DEVE mostrar HTML renderizado lado a lado com código Liquid
- **CA-UC06-002:** Erros de sintaxe DEVEM ser destacados com linha/coluna
- **CA-UC06-003:** Variáveis não encontradas DEVEM exibir placeholder `[variavel.ausente]`
- **CA-UC06-004:** Preview DEVE atualizar automaticamente com debounce de 500ms
- **CA-UC06-005:** Contexto de teste DEVE ser editável pelo usuário
- **CA-UC06-006:** Preview DEVE funcionar mesmo com template incompleto (não bloquear digitação)

---

## UC07 — Criar Nova Versão

### Objetivo
Criar snapshot de versão atual do template, preservando estado exato para auditoria e possibilidade de rollback.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.VERSION`
- Template existente

### Pós-condições
- Nova versão criada
- Versão anterior preservada
- Histórico atualizado

### Fluxo Principal
- **FP-UC07-001:** Sistema detecta alteração em template (durante edição em UC03)
- **FP-UC07-002:** Sistema incrementa número de versão (versão anterior + 1)
- **FP-UC07-003:** Sistema cria snapshot com: número versão, conteúdo completo, contexto, data, usuário
- **FP-UC07-004:** Sistema marca nova versão como ativa
- **FP-UC07-005:** Sistema marca versão anterior como inativa
- **FP-UC07-006:** Sistema registra auditoria (template.versionado)

### Fluxos Alternativos
- **FA-UC07-001:** Adicionar nota de versão (changelog manual)
- **FA-UC07-002:** Marcar versão como "importante" (milestone)

### Fluxos de Exceção
- **FE-UC07-001:** Erro ao criar snapshot → rollback + log + alerta
- **FE-UC07-002:** Limite de versões atingido → arquivar versões antigas (>100 versões)

### Regras de Negócio
- **RN-UC-07-001:** Versões numeradas sequencialmente (1, 2, 3...)
- **RN-UC-07-002:** Apenas uma versão pode estar ativa por vez
- **RN-UC-07-003:** Versões preservam snapshot completo (conteúdo + contexto + metadados)
- **RN-UC-07-004:** Histórico preservado indefinidamente (compliance)
- **RN-RF063-005:** Versionamento obrigatório

### Critérios de Aceite
- **CA-UC07-001:** Versão DEVE ser numerada sequencialmente
- **CA-UC07-002:** Snapshot DEVE preservar conteúdo completo + contexto + metadados
- **CA-UC07-003:** Apenas UMA versão DEVE estar ativa por vez
- **CA-UC07-004:** Versão anterior DEVE ser marcada como inativa automaticamente
- **CA-UC07-005:** Auditoria DEVE registrar usuário, data e número da versão
- **CA-UC07-006:** Histórico DEVE preservar todas as versões indefinidamente

---

## UC08 — Executar Rollback de Versão

### Objetivo
Reverter template para versão anterior, criando nova versão com conteúdo da versão selecionada.

### Pré-condições
- Usuário autenticado
- Permissão `TPL.ENGINE.ROLLBACK`
- Template com pelo menos 2 versões

### Pós-condições
- Nova versão criada com conteúdo da versão selecionada
- Template volta ao estado da versão escolhida
- Cache invalidado

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa histórico de versões
- **FP-UC08-002:** Usuário seleciona versão anterior para rollback
- **FP-UC08-003:** Sistema exibe comparação (diff) entre versão atual e versão selecionada
- **FP-UC08-004:** Sistema exibe confirmação: "Confirma rollback para versão X?"
- **FP-UC08-005:** Sistema valida permissão `TPL.ENGINE.ROLLBACK`
- **FP-UC08-006:** Sistema cria nova versão (N+1) com conteúdo da versão selecionada
- **FP-UC08-007:** Sistema marca nova versão como ativa
- **FP-UC08-008:** Sistema invalida cache Redis
- **FP-UC08-009:** Sistema registra auditoria (template.rollback)
- **FP-UC08-010:** Sistema exibe mensagem: "Rollback concluído. Versão X restaurada como versão N+1"

### Fluxos Alternativos
- **FA-UC08-001:** Cancelar rollback antes de confirmar
- **FA-UC08-002:** Visualizar preview da versão antes de fazer rollback
- **FA-UC08-003:** Adicionar nota de rollback (motivo)

### Fluxos de Exceção
- **FE-UC08-001:** Versão inexistente → HTTP 404
- **FE-UC08-002:** Template com apenas 1 versão → mensagem "Rollback requer pelo menos 2 versões"
- **FE-UC08-003:** Erro ao criar nova versão → rollback + log + alerta

### Regras de Negócio
- **RN-UC-08-001:** Rollback NÃO deleta versões, cria nova versão com conteúdo antigo
- **RN-UC-08-002:** Rollback exige confirmação explícita
- **RN-UC-08-003:** Diff visual DEVE ser exibido antes de confirmar
- **RN-UC-08-004:** Cache Redis DEVE ser invalidado
- **RN-RF063-005:** Versionamento obrigatório preservado

### Critérios de Aceite
- **CA-UC08-001:** Rollback DEVE criar NOVA versão com conteúdo da versão selecionada (não deletar versões)
- **CA-UC08-002:** Sistema DEVE exibir diff visual antes de confirmar
- **CA-UC08-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC08-004:** Nova versão DEVE ser marcada como ativa
- **CA-UC08-005:** Cache Redis DEVE ser invalidado
- **CA-UC08-006:** Auditoria DEVE registrar: versão origem, versão destino, usuário, data
- **CA-UC08-007:** Tentativa de rollback com apenas 1 versão DEVE retornar erro claro

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Aplicadas |
|----|---------------------------|
| UC00 | RN-UC-00-001, RN-UC-00-002, RN-UC-00-003, RN-UC-00-004, RN-RF063-015 |
| UC01 | RN-UC-01-001, RN-UC-01-002, RN-UC-01-003, RN-UC-01-004, RN-UC-01-005, RN-RF063-001, RN-RF063-006 |
| UC02 | RN-UC-02-001, RN-UC-02-002, RN-UC-02-003, RN-RF063-015 |
| UC03 | RN-UC-03-001, RN-UC-03-002, RN-UC-03-003, RN-UC-03-004, RN-UC-03-005, RN-RF063-005, RN-RF063-006, RN-RF063-012 |
| UC04 | RN-UC-04-001, RN-UC-04-002, RN-UC-04-003, RN-UC-04-004, RN-UC-04-005 |
| UC05 | RN-UC-05-001, RN-UC-05-002, RN-UC-05-003, RN-UC-05-004, RN-UC-05-005, RN-RF063-002, RN-RF063-003, RN-RF063-011, RN-RF063-012 |
| UC06 | RN-UC-06-001, RN-UC-06-002, RN-UC-06-003, RN-UC-06-004, RN-RF063-004, RN-RF063-006 |
| UC07 | RN-UC-07-001, RN-UC-07-002, RN-UC-07-003, RN-UC-07-004, RN-RF063-005 |
| UC08 | RN-UC-08-001, RN-UC-08-002, RN-UC-08-003, RN-UC-08-004, RN-RF063-005 |

### Cobertura de Regras RF063

| Regra RF063 | UCs que cobrem |
|------------|---------------|
| RN-RF063-001 (Sintaxe Liquid) | UC01, UC05, UC06 |
| RN-RF063-002 (Contexto Tipado) | UC05 |
| RN-RF063-003 (Filtros Customizados) | UC05 |
| RN-RF063-004 (Preview Tempo Real) | UC06 |
| RN-RF063-005 (Versionamento) | UC03, UC07, UC08 |
| RN-RF063-006 (Validação Sintaxe) | UC01, UC03, UC06 |
| RN-RF063-007 (Testes A/B) | Não coberto explicitamente (caso de uso futuro) |
| RN-RF063-008 (Herança Templates) | UC01, UC05 (implícito em fluxos alternativos) |
| RN-RF063-009 (Parciais) | UC01, UC05 (implícito em fluxos alternativos) |
| RN-RF063-010 (i18n) | UC05, UC06 (implícito em fluxos alternativos) |
| RN-RF063-011 (Sanitização XSS) | UC05 |
| RN-RF063-012 (Cache Redis) | UC03, UC04, UC05, UC08 |
| RN-RF063-013 (Documentação Variáveis) | UC01, UC02 (implícito) |
| RN-RF063-014 (Auditoria Uso) | UC01, UC03, UC04, UC05, UC07, UC08 |
| RN-RF063-015 (Multi-tenant) | UC00, UC02 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica v2.0 - Reformatação completa para governança v2.0, 9 UCs canônicos (UC00-UC08), 100% aderência ao template oficial, cobertura completa do RF063 |
| 1.0 | 2025-12-17 | Agência ALC - alc.dev.br | Versão inicial (pré-governança v2.0, estrutura incompatível) |

# UC-RF021 — Casos de Uso Canônicos

**RF:** RF021 — Catálogo de Serviços e Portal Self-Service
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD-Service-Desk
**Fase:** Fase 5 - Service Desk

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF021 - Catálogo de Serviços e Portal Self-Service**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF021.yaml)
- Massas de Teste (MT-RF021.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

O RF021 implementa um **Catálogo de Serviços e Portal Self-Service** que permite aos usuários finais solicitar serviços de TI/Telecom de forma autônoma através de uma interface intuitiva estilo "carrinho de compras", com aprovação automatizada via workflow configurável, tracking visual de SLA e integração com sistemas de estoque e fornecedores.

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Serviços do Catálogo | Usuário Autenticado |
| UC01 | Criar Serviço no Catálogo | Administrador |
| UC02 | Visualizar Detalhes do Serviço | Usuário Autenticado |
| UC03 | Editar Serviço no Catálogo | Administrador |
| UC04 | Inativar Serviço no Catálogo | Administrador |
| UC05 | Adicionar Serviço ao Carrinho | Usuário Autenticado |
| UC06 | Finalizar Solicitação (Converter Carrinho) | Usuário Autenticado |
| UC07 | Aprovar Solicitação (Workflow) | Aprovador |
| UC08 | Atender Solicitação (Provisionamento) | Atendente |
| UC09 | Cancelar Solicitação | Usuário/Aprovador |
| UC10 | Avaliar Serviço | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (empresa)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- SLA deve ser calculado considerando **dias úteis** (segunda a sexta, 8h às 18h)
- Notificações devem ser enviadas em **tempo real** (latência máxima 30 segundos)
- Formulários dinâmicos devem validar **client-side** (UX) e **server-side** (segurança)

---

## UC00 — Listar Serviços do Catálogo

### Objetivo
Permitir que o usuário visualize o catálogo de serviços disponíveis para solicitação, com busca e filtros.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.CATALOGO.VIEW`

### Pós-condições
- Lista de serviços exibida conforme filtros aplicados
- Serviços inativos não aparecem na listagem

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade "Catálogo de Serviços"
- **FP-UC00-002:** Sistema valida permissão `SERVICO.CATALOGO.VIEW`
- **FP-UC00-003:** Sistema carrega serviços ativos do tenant
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros por página)
- **FP-UC00-005:** Sistema exibe lista com cards mostrando: nome, ícone, categoria, SLA, preço estimado, avaliação média, botão "Adicionar ao Carrinho"

### Fluxos Alternativos
- **FA-UC00-001:** Buscar serviço por nome (busca full-text)
- **FA-UC00-002:** Filtrar por categoria
- **FA-UC00-003:** Ordenar por: nome, SLA, preço, avaliação
- **FA-UC00-004:** Visualizar como grid ou lista

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → retornar HTTP 403 com mensagem "Acesso negado"
- **FE-UC00-002:** Nenhum serviço disponível → exibir estado vazio com mensagem "Nenhum serviço disponível no momento"
- **FE-UC00-003:** Erro de conexão → exibir mensagem "Erro ao carregar catálogo. Tente novamente."

### Regras de Negócio
- **RN-UC00-001:** Somente registros do tenant do usuário autenticado (multi-tenancy)
- **RN-UC00-002:** Serviços com `Ativo = 0` não aparecem na listagem
- **RN-UC00-003:** Paginação padrão de 20 registros
- **RN-UC00-004:** Avaliação média exibida como estrelas (1-5)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas serviços ativos do tenant do usuário autenticado
- **CA-UC00-002:** Serviços inativos (Ativo = 0) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL

---

## UC01 — Criar Serviço no Catálogo

### Objetivo
Permitir ao administrador cadastrar um novo serviço no catálogo.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.CATALOGO.MANAGE`

### Pós-condições
- Serviço criado e persistido
- Auditoria registrada
- Serviço disponível no catálogo (se Ativo = 1)

### Fluxo Principal
- **FP-UC01-001:** Administrador clica em "Novo Serviço"
- **FP-UC01-002:** Sistema valida permissão `SERVICO.CATALOGO.MANAGE`
- **FP-UC01-003:** Sistema exibe formulário de criação
- **FP-UC01-004:** Administrador preenche campos obrigatórios: Nome, Descrição, Categoria, SLA (horas), Preço Estimado, Ícone
- **FP-UC01-005:** Administrador define flags: Requer Aprovação, Verifica Estoque, Provisiona Automático, Requer Justificativa
- **FP-UC01-006:** Administrador define formulário dinâmico (JSON Schema) - opcional
- **FP-UC01-007:** Administrador define workflow de aprovação (níveis 1-4) - opcional
- **FP-UC01-008:** Sistema valida dados (campos obrigatórios, JSON Schema válido)
- **FP-UC01-009:** Sistema cria registro com `tenant_id` automático
- **FP-UC01-010:** Sistema registra auditoria (created_by, created_at)
- **FP-UC01-011:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Salvar como rascunho (Ativo = 0)
- **FA-UC01-002:** Copiar de template existente
- **FA-UC01-003:** Upload de ícone customizado

### Fluxos de Exceção
- **FE-UC01-001:** Nome duplicado → retornar HTTP 400 "Já existe um serviço com este nome"
- **FE-UC01-002:** JSON Schema inválido → retornar HTTP 400 "Formulário customizado inválido"
- **FE-UC01-003:** SLA < 1 hora → retornar HTTP 400 "SLA mínimo é de 1 hora"
- **FE-UC01-004:** Categoria inexistente → retornar HTTP 400 "Categoria inválida"

### Regras de Negócio
- **RN-UC01-001:** Nome único por empresa (tenant)
- **RN-UC01-002:** SLA mínimo de 1 hora
- **RN-UC01-003:** Preço 0 = serviço gratuito
- **RN-UC01-004:** Formulário customizado deve ser JSON Schema válido
- **RN-UC01-005:** `tenant_id` preenchido automaticamente com tenant do usuário
- **RN-UC01-006:** `created_by` preenchido automaticamente com ID do usuário

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** `tenant_id` DEVE ser preenchido automaticamente
- **CA-UC01-003:** `created_by` DEVE ser preenchido automaticamente
- **CA-UC01-004:** `created_at` DEVE ser preenchido automaticamente
- **CA-UC01-005:** Sistema DEVE validar JSON Schema se formulário customizado for fornecido
- **CA-UC01-006:** Auditoria DEVE ser registrada APÓS sucesso da criação

---

## UC02 — Visualizar Detalhes do Serviço

### Objetivo
Permitir visualização detalhada de um serviço do catálogo antes de adicionar ao carrinho.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.CATALOGO.VIEW`
- Serviço existe e está ativo

### Pós-condições
- Detalhes do serviço exibidos corretamente
- Usuário pode adicionar ao carrinho

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em um serviço no catálogo
- **FP-UC02-002:** Sistema valida permissão `SERVICO.CATALOGO.VIEW`
- **FP-UC02-003:** Sistema valida que serviço pertence ao tenant do usuário
- **FP-UC02-004:** Sistema exibe modal/página com: nome, descrição completa, categoria, SLA, preço estimado, formulário de solicitação, avaliação média, comentários de usuários
- **FP-UC02-005:** Sistema exibe botão "Adicionar ao Carrinho"

### Fluxos Alternativos
- **FA-UC02-001:** Ver avaliações de outros usuários (top 10 mais recentes)
- **FA-UC02-002:** Ver minhas solicitações anteriores deste serviço
- **FA-UC02-003:** Adicionar aos favoritos

### Fluxos de Exceção
- **FE-UC02-001:** Serviço não existe → retornar HTTP 404
- **FE-UC02-002:** Serviço inativo → retornar HTTP 404 (não expor existência)
- **FE-UC02-003:** Serviço de outro tenant → retornar HTTP 404

### Regras de Negócio
- **RN-UC02-001:** Isolamento por tenant (multi-tenancy)
- **RN-UC02-002:** Exibir avaliação média calculada (estrelas 1-5)
- **RN-UC02-003:** Auditoria de visualização (analytics)

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar serviços do próprio tenant
- **CA-UC02-002:** Avaliação média DEVE ser calculada a partir de todas as avaliações
- **CA-UC02-003:** Tentativa de acessar serviço de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar serviço inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco

---

## UC03 — Editar Serviço no Catálogo

### Objetivo
Permitir alteração controlada de um serviço no catálogo, mantendo histórico.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.CATALOGO.MANAGE`
- Serviço existe

### Pós-condições
- Serviço atualizado
- Auditoria registrada
- Usuários afetados notificados (se serviço tiver solicitações pendentes)

### Fluxo Principal
- **FP-UC03-001:** Administrador clica em "Editar" no serviço
- **FP-UC03-002:** Sistema valida permissão `SERVICO.CATALOGO.MANAGE`
- **FP-UC03-003:** Sistema carrega dados atuais do serviço
- **FP-UC03-004:** Administrador altera dados
- **FP-UC03-005:** Sistema valida alterações
- **FP-UC03-006:** Sistema persiste alterações
- **FP-UC03-007:** Sistema registra auditoria (updated_by, updated_at)
- **FP-UC03-008:** Sistema notifica usuários com solicitações pendentes deste serviço (se aplicável)

### Fluxos Alternativos
- **FA-UC03-001:** Editar apenas metadados (nome, descrição)
- **FA-UC03-002:** Alterar formulário customizado (JSON Schema)
- **FA-UC03-003:** Alterar workflow de aprovação

### Fluxos de Exceção
- **FE-UC03-001:** Nome duplicado → retornar HTTP 400 "Já existe um serviço com este nome"
- **FE-UC03-002:** JSON Schema inválido → retornar HTTP 400 "Formulário customizado inválido"
- **FE-UC03-003:** SLA < 1 hora → retornar HTTP 400 "SLA mínimo é de 1 hora"
- **FE-UC03-004:** Serviço tem solicitações em atendimento → exibir warning "Este serviço possui solicitações em atendimento"

### Regras de Negócio
- **RN-UC03-001:** `updated_by` preenchido automaticamente com ID do usuário
- **RN-UC03-002:** `updated_at` preenchido automaticamente com timestamp atual
- **RN-UC03-003:** Auditoria deve registrar estado anterior e novo estado
- **RN-UC03-004:** Notificar usuários afetados se serviço tiver solicitações pendentes

### Critérios de Aceite
- **CA-UC03-001:** `updated_by` DEVE ser preenchido automaticamente
- **CA-UC03-002:** `updated_at` DEVE ser preenchido automaticamente
- **CA-UC03-003:** Apenas campos alterados DEVEM ser validados
- **CA-UC03-004:** Tentativa de editar serviço de outro tenant DEVE retornar 404
- **CA-UC03-005:** Auditoria DEVE registrar estado anterior e novo estado

---

## UC04 — Inativar Serviço no Catálogo

### Objetivo
Permitir inativação lógica de um serviço (soft delete).

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.CATALOGO.MANAGE`
- Serviço existe

### Pós-condições
- Serviço marcado como inativo (`Ativo = 0`)
- Serviço removido do catálogo público
- Histórico de solicitações mantido

### Fluxo Principal
- **FP-UC04-001:** Administrador clica em "Inativar" no serviço
- **FP-UC04-002:** Sistema exibe modal de confirmação
- **FP-UC04-003:** Sistema valida permissão `SERVICO.CATALOGO.MANAGE`
- **FP-UC04-004:** Sistema verifica se existem solicitações pendentes deste serviço
- **FP-UC04-005:** Sistema marca `Ativo = 0`
- **FP-UC04-006:** Sistema registra auditoria
- **FP-UC04-007:** Sistema confirma sucesso

### Fluxos Alternativos
- **FA-UC04-001:** Reativar serviço inativo
- **FA-UC04-002:** Agendar inativação futura

### Fluxos de Exceção
- **FE-UC04-001:** Solicitações pendentes/em atendimento existem → retornar HTTP 400 "Não é possível inativar. Existem X solicitações pendentes/em atendimento"
- **FE-UC04-002:** Serviço já inativo → retornar HTTP 400 "Serviço já está inativo"
- **FE-UC04-003:** Serviço de outro tenant → retornar HTTP 404

### Regras de Negócio
- **RN-UC04-001:** Inativação é sempre lógica (`Ativo = 0`)
- **RN-UC04-002:** Bloquear se existem solicitações com status `Pendente`, `Aprovada`, `Em_Atendimento`, `Aguardando_Estoque`, `Aguardando_Usuario`, `Em_Provisionamento`
- **RN-UC04-003:** Serviço inativo não aparece em listagens mas histórico é mantido
- **RN-UC04-004:** Auditoria completa de inativação

### Critérios de Aceite
- **CA-UC04-001:** Inativação DEVE ser sempre lógica (`Ativo = 0`)
- **CA-UC04-002:** Sistema DEVE verificar solicitações ativas ANTES de permitir inativação
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do administrador
- **CA-UC04-004:** Serviço inativo NÃO deve aparecer em listagens públicas do catálogo
- **CA-UC04-005:** Histórico de solicitações DEVE ser mantido mesmo após inativação

---

## UC05 — Adicionar Serviço ao Carrinho

### Objetivo
Permitir que o usuário adicione múltiplos serviços a um carrinho temporário antes de finalizar a solicitação.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.SOLICITAR`
- Serviço ativo

### Pós-condições
- Item adicionado ao carrinho
- Carrinho persiste entre sessões

### Fluxo Principal
- **FP-UC05-001:** Usuário clica em "Adicionar ao Carrinho" em um serviço
- **FP-UC05-002:** Sistema valida permissão `SERVICO.SOLICITAR`
- **FP-UC05-003:** Sistema valida que serviço está ativo
- **FP-UC05-004:** Sistema verifica limite de 10 serviços por carrinho
- **FP-UC05-005:** Sistema adiciona item à tabela `Servico_Carrinho` com `tenant_id` e `usuario_id`
- **FP-UC05-006:** Sistema confirma adição com badge no ícone do carrinho

### Fluxos Alternativos
- **FA-UC05-001:** Remover item do carrinho
- **FA-UC05-002:** Limpar carrinho inteiro
- **FA-UC05-003:** Visualizar carrinho sem finalizar

### Fluxos de Exceção
- **FE-UC05-001:** Limite de 10 serviços atingido → retornar HTTP 400 "Carrinho cheio. Máximo de 10 serviços."
- **FE-UC05-002:** Serviço inativo → retornar HTTP 400 "Serviço não está disponível"
- **FE-UC05-003:** Serviço já está no carrinho → exibir mensagem "Serviço já está no carrinho"

### Regras de Negócio
- **RN-UC05-001:** Máximo de 10 serviços por carrinho (RN-RF021-003)
- **RN-UC05-002:** Carrinho persiste entre sessões
- **RN-UC05-003:** Itens não finalizados por 30 dias são removidos automaticamente via job noturno
- **RN-UC05-004:** Carrinho é limpo automaticamente após finalização da solicitação

### Critérios de Aceite
- **CA-UC05-001:** Usuário PODE adicionar até 10 serviços ao carrinho
- **CA-UC05-002:** Carrinho DEVE persistir entre sessões (salvo no banco)
- **CA-UC05-003:** Itens DEVEM ser removidos automaticamente após 30 dias sem finalização
- **CA-UC05-004:** Badge do carrinho DEVE atualizar em tempo real

---

## UC06 — Finalizar Solicitação (Converter Carrinho)

### Objetivo
Converter itens do carrinho em uma solicitação formal de serviço.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.SOLICITAR` ou `SERVICO.SOLICITAR_TERCEIROS`
- Carrinho contém pelo menos 1 serviço

### Pós-condições
- Solicitação criada com número único (formato `SRV-YYYY-NNNNN`)
- Carrinho limpo
- Workflow de aprovação iniciado (se serviço requer aprovação)
- Notificações enviadas

### Fluxo Principal
- **FP-UC06-001:** Usuário clica em "Finalizar Solicitação"
- **FP-UC06-002:** Sistema valida permissão
- **FP-UC06-003:** Sistema valida limite de solicitações simultâneas (máximo 5 para usuário comum, 20 para gestor/diretor) - RN-RF021-010
- **FP-UC06-004:** Sistema exibe formulário de finalização: beneficiário (se permissão `SOLICITAR_TERCEIROS`), justificativa (se serviço requer), prioridade
- **FP-UC06-005:** Sistema gera número único de solicitação (`SRV-YYYY-NNNNN`) - RN-RF021-013
- **FP-UC06-006:** Sistema cria registro em `Servico_Solicitacao` com status `Pendente`
- **FP-UC06-007:** Sistema limpa carrinho
- **FP-UC06-008:** Sistema inicia workflow de aprovação (se `Fl_Requer_Aprovacao = 1`)
- **FP-UC06-009:** Sistema envia notificação para solicitante e aprovador nível 1 (se aplicável)
- **FP-UC06-010:** Sistema registra auditoria
- **FP-UC06-011:** Sistema confirma sucesso e exibe número da solicitação

### Fluxos Alternativos
- **FA-UC06-001:** Solicitação para outro usuário (beneficiário diferente do solicitante) - RN-RF021-002
- **FA-UC06-002:** Auto-aprovação por regras (RN-RF021-008) - aprovação automática se colaborador veterano (>1 ano), valor baixo (<R$ 500), serviço não-crítico

### Fluxos de Exceção
- **FE-UC06-001:** Carrinho vazio → retornar HTTP 400 "Carrinho vazio"
- **FE-UC06-002:** Limite de solicitações simultâneas atingido → retornar HTTP 400 "Você possui 5 solicitações pendentes. Aguarde conclusão ou cancele uma para criar nova."
- **FE-UC06-003:** Justificativa obrigatória não fornecida → retornar HTTP 400 "Justificativa obrigatória (50-1000 caracteres)"
- **FE-UC06-004:** Beneficiário inválido → retornar HTTP 400 "Beneficiário não encontrado"

### Regras de Negócio
- **RN-UC06-001:** Gera número único no formato `SRV-YYYY-NNNNN` via sequence SQL Server (RN-RF021-013)
- **RN-UC06-002:** Limite de 5 solicitações pendentes/em atendimento para usuário comum, 20 para gestor/diretor (RN-RF021-010)
- **RN-UC06-003:** Justificativa obrigatória (50-1000 chars) se `Fl_Requer_Justificativa = 1` (RN-RF021-012)
- **RN-UC06-004:** Solicitação para terceiro requer permissão `SERVICO.SOLICITAR_TERCEIROS` (RN-RF021-002)
- **RN-UC06-005:** Auto-aprovação automática se regras forem atendidas (RN-RF021-008)
- **RN-UC06-006:** SLA inicia após aprovação final (ou imediatamente se auto-aprovada)

### Critérios de Aceite
- **CA-UC06-001:** Número de solicitação DEVE ser único e sequencial por ano
- **CA-UC06-002:** Carrinho DEVE ser limpo APÓS criação bem-sucedida da solicitação
- **CA-UC06-003:** Workflow DEVE iniciar automaticamente se serviço requer aprovação
- **CA-UC06-004:** Notificações DEVEM ser enviadas para solicitante e aprovador
- **CA-UC06-005:** Sistema DEVE validar limite de solicitações simultâneas

---

## UC07 — Aprovar Solicitação (Workflow)

### Objetivo
Permitir aprovação/rejeição de solicitações através de workflow configurável multi-nível.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.APROVAR`
- Solicitação com status `Pendente`
- Usuário é aprovador do nível atual

### Pós-condições
- Aprovação/rejeição registrada
- Solicitação avança para próximo nível ou status final
- Notificações enviadas
- Auditoria registrada

### Fluxo Principal
- **FP-UC07-001:** Aprovador acessa "Minhas Aprovações Pendentes"
- **FP-UC07-002:** Sistema lista solicitações onde aprovador é responsável pelo nível atual
- **FP-UC07-003:** Aprovador clica em uma solicitação
- **FP-UC07-004:** Sistema exibe detalhes: serviço, solicitante, beneficiário, justificativa, formulário preenchido, níveis de aprovação anteriores
- **FP-UC07-005:** Aprovador clica em "Aprovar" ou "Rejeitar"
- **FP-UC07-006:** Se rejeitar, sistema solicita motivo obrigatório (mínimo 20 caracteres)
- **FP-UC07-007:** Sistema registra aprovação/rejeição em `Servico_Aprovacao`
- **FP-UC07-008:** Se aprovado: sistema avança para próximo nível ou marca como `Aprovada` (se último nível)
- **FP-UC07-009:** Se rejeitado: sistema marca solicitação como `Rejeitada` e notifica solicitante
- **FP-UC07-010:** Sistema envia notificações (próximo aprovador ou solicitante)
- **FP-UC07-011:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC07-001:** Auto-aprovação por regras (RN-RF021-008) - sistema aprova automaticamente sem intervenção humana
- **FA-UC07-002:** Verificação de estoque antes de aprovar (RN-RF021-004) - se `Fl_Verifica_Estoque = 1`, exibir alerta se item indisponível

### Fluxos de Exceção
- **FE-UC07-001:** Solicitação já aprovada/rejeitada → retornar HTTP 400 "Solicitação já foi processada"
- **FE-UC07-002:** Usuário não é aprovador deste nível → retornar HTTP 403 "Você não é aprovador deste nível"
- **FE-UC07-003:** Motivo de rejeição < 20 caracteres → retornar HTTP 400 "Motivo de rejeição deve ter mínimo 20 caracteres"
- **FE-UC07-004:** Estoque indisponível → exibir warning "Item em falta no estoque. Solicitação aguardará reposição."

### Regras de Negócio
- **RN-UC07-001:** Aprovações são sequenciais - cada nível depende do anterior (RN-RF021-001)
- **RN-UC07-002:** Se uma aprovação for rejeitada, todo o fluxo é cancelado automaticamente
- **RN-UC07-003:** Níveis de aprovação: Nível 1 (Gestor), Nível 2 (TI/Telecom), Nível 3 (Financeiro >R$ 1.000), Nível 4 (Diretor >R$ 10.000)
- **RN-UC07-004:** Aprovador recebe notificação no momento que solicitação chega em sua fila
- **RN-UC07-005:** Histórico completo de aprovações deve ser auditado
- **RN-UC07-006:** Se `Fl_Verifica_Estoque = 1`, validar disponibilidade antes de aprovar (RN-RF021-004)
- **RN-UC07-007:** Auto-aprovação registrada com `Fl_Auto_Aprovacao = 1` e `Regra_Auto_Aprovacao` (RN-RF021-008)

### Critérios de Aceite
- **CA-UC07-001:** Aprovações DEVEM ser sequenciais (dependência entre níveis)
- **CA-UC07-002:** Rejeição DEVE cancelar todo o fluxo automaticamente
- **CA-UC07-003:** Aprovador DEVE receber notificação quando solicitação chegar em sua fila
- **CA-UC07-004:** Histórico completo DEVE ser auditado
- **CA-UC07-005:** Auto-aprovação DEVE registrar regra aplicada

---

## UC08 — Atender Solicitação (Provisionamento)

### Objetivo
Executar o provisionamento técnico do serviço solicitado após aprovação.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.ATENDER`
- Solicitação com status `Aprovada`

### Pós-condições
- Serviço provisionado
- Status atualizado para `Concluida`
- SLA finalizado
- Usuário notificado para avaliar serviço

### Fluxo Principal
- **FP-UC08-001:** Atendente acessa "Fila de Atendimento"
- **FP-UC08-002:** Sistema lista solicitações com status `Aprovada`
- **FP-UC08-003:** Atendente atribui solicitação a si e atualiza status para `Em_Atendimento`
- **FP-UC08-004:** Sistema registra `Dt_Inicio_Atendimento`
- **FP-UC08-005:** Atendente executa provisionamento (manual ou automático via API) - RN-RF021-007
- **FP-UC08-006:** Se `Fl_Provisiona_Automatico = 1`, sistema chama API do fornecedor e aguarda callback
- **FP-UC08-007:** Atendente registra evidências (fotos, logs, confirmações)
- **FP-UC08-008:** Atendente marca como `Concluida`
- **FP-UC08-009:** Sistema registra `Dt_Conclusao`
- **FP-UC08-010:** Sistema finaliza SLA
- **FP-UC08-011:** Sistema envia notificação para solicitante solicitando avaliação
- **FP-UC08-012:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC08-001:** Provisionamento automático via API (RN-RF021-007) - integrações com Vivo, Claro, TIM, Dell, HP, Lenovo, AWS, Azure
- **FA-UC08-002:** Solicitação aguarda estoque (status `Aguardando_Estoque`) - RN-RF021-004
- **FA-UC08-003:** Solicitação aguarda ação do usuário (status `Aguardando_Usuario`)
- **FA-UC08-004:** Provisionamento parcial (múltiplas etapas)

### Fluxos de Exceção
- **FE-UC08-001:** Erro de provisionamento → atualizar status para `Erro_Provisionamento` e notificar atendente
- **FE-UC08-002:** Timeout da API do fornecedor → retornar HTTP 500 "Timeout na integração com fornecedor"
- **FE-UC08-003:** Estoque indisponível → atualizar status para `Aguardando_Estoque` e aguardar reposição (máximo 15 dias, senão cancelar automaticamente)
- **FE-UC08-004:** SLA vencido → enviar alerta para atendente e gestor

### Regras de Negócio
- **RN-UC08-001:** Provisionamento pode ser manual ou automático (RN-RF021-007)
- **RN-UC08-002:** SLA tracking em tempo real com semáforo verde/amarelo/vermelho (RN-RF021-005)
- **RN-UC08-003:** SLA pausado em status `Aguardando_Estoque` ou `Aguardando_Usuario` (RN-RF021-005)
- **RN-UC08-004:** Job Hangfire verifica SLAs a cada 15 minutos (RN-RF021-005)
- **RN-UC08-005:** Alerta enviado ao atendente quando SLA entrar em "vermelho" (<20% do tempo restante)
- **RN-UC08-006:** Se estoque não for reposto em 15 dias, solicitação é cancelada automaticamente (RN-RF021-004)
- **RN-UC08-007:** Integração com fornecedores: Vivo, Claro, TIM (ativação de linhas), Dell, HP, Lenovo (pedidos via EDI), AWS, Azure (criação de recursos via SDK) - RN-RF021-007

### Critérios de Aceite
- **CA-UC08-001:** SLA DEVE ser calculado considerando apenas dias úteis (segunda a sexta, 8h às 18h)
- **CA-UC08-002:** SLA DEVE ser pausado em status `Aguardando_Estoque` ou `Aguardando_Usuario`
- **CA-UC08-003:** Alerta DEVE ser enviado quando SLA entrar em "vermelho"
- **CA-UC08-004:** Provisionamento automático DEVE atualizar status via callback do fornecedor
- **CA-UC08-005:** Se provisionamento falhar, status DEVE mudar para `Erro_Provisionamento`

---

## UC09 — Cancelar Solicitação

### Objetivo
Permitir cancelamento de solicitação pelo solicitante ou aprovador.

### Pré-condições
- Usuário autenticado
- Permissão `SERVICO.SOLICITAR` (para cancelamento próprio) ou `SERVICO.CANCELAR_FORCADO` (para cancelamento em atendimento)
- Solicitação existe

### Pós-condições
- Solicitação cancelada (`Status = 'Cancelada'`)
- Reserva de estoque liberada (se aplicável)
- Todos os envolvidos notificados

### Fluxo Principal
- **FP-UC09-001:** Usuário/Aprovador clica em "Cancelar Solicitação"
- **FP-UC09-002:** Sistema exibe modal solicitando justificativa obrigatória (mínimo 20 caracteres)
- **FP-UC09-003:** Sistema valida permissão e restrições de cancelamento
- **FP-UC09-004:** Sistema atualiza `Status = 'Cancelada'`
- **FP-UC09-005:** Sistema registra `Dt_Cancelamento`, `Id_Usuario_Cancelamento`, `Motivo_Cancelamento`
- **FP-UC09-006:** Sistema libera reserva de estoque (se `Fl_Verifica_Estoque = 1`)
- **FP-UC09-007:** Sistema envia notificação para todos os envolvidos (solicitante, beneficiário, aprovadores, atendentes)
- **FP-UC09-008:** Sistema registra auditoria

### Fluxos Alternativos
- **FA-UC09-001:** Cancelamento em lote (múltiplas solicitações)
- **FA-UC09-002:** Cancelamento automático por timeout (15 dias aguardando estoque - RN-RF021-004)

### Fluxos de Exceção
- **FE-UC09-001:** Solicitação já está `Em_Atendimento` e usuário não é aprovador → retornar HTTP 403 "Não é possível cancelar após início do atendimento"
- **FE-UC09-002:** Solicitação já concluída/cancelada/rejeitada → retornar HTTP 400 "Solicitação já foi finalizada"
- **FE-UC09-003:** Justificativa < 20 caracteres → retornar HTTP 400 "Justificativa deve ter mínimo 20 caracteres"
- **FE-UC09-004:** Usuário tentando cancelar solicitação de outro → retornar HTTP 403 "Você não pode cancelar esta solicitação"

### Regras de Negócio
- **RN-UC09-001:** Solicitante pode cancelar até início do atendimento (`Dt_Inicio_Atendimento`) - RN-RF021-011
- **RN-UC09-002:** Aprovador pode cancelar a qualquer momento (inclui solicitações em atendimento)
- **RN-UC09-003:** Cancelamento requer justificativa obrigatória (mínimo 20 caracteres)
- **RN-UC09-004:** Liberar reserva de estoque se `Fl_Verifica_Estoque = 1`
- **RN-UC09-005:** Notificar todos os aprovadores e atendentes envolvidos
- **RN-UC09-006:** Cancelamento automático se estoque não for reposto em 15 dias (RN-RF021-004)

### Critérios de Aceite
- **CA-UC09-001:** Solicitante PODE cancelar até início do atendimento
- **CA-UC09-002:** Aprovador PODE cancelar a qualquer momento
- **CA-UC09-003:** Justificativa DEVE ter mínimo 20 caracteres
- **CA-UC09-004:** Reserva de estoque DEVE ser liberada após cancelamento
- **CA-UC09-005:** Todos os envolvidos DEVEM ser notificados

---

## UC10 — Avaliar Serviço

### Objetivo
Permitir que o solicitante avalie o serviço prestado após conclusão.

### Pré-condições
- Usuário autenticado
- Solicitação concluída (`Status = 'Concluida'`)
- Usuário é o solicitante

### Pós-condições
- Avaliação registrada
- Média do serviço recalculada
- Atendente e gestor notificados

### Fluxo Principal
- **FP-UC10-001:** Solicitação concluída → sistema envia push notification "Avalie o serviço"
- **FP-UC10-002:** Usuário clica e sistema exibe modal de avaliação
- **FP-UC10-003:** Usuário seleciona estrelas (1-5) e adiciona comentário opcional (0-500 caracteres)
- **FP-UC10-004:** Sistema valida avaliação
- **FP-UC10-005:** Sistema registra avaliação em `Servico_Avaliacao`
- **FP-UC10-006:** Sistema recalcula `Avaliacao_Media` do serviço
- **FP-UC10-007:** Sistema notifica atendente e gestor do catálogo
- **FP-UC10-008:** Sistema registra auditoria
- **FP-UC10-009:** Se avaliação < 3.0, sistema gera ticket de melhoria automático

### Fluxos Alternativos
- **FA-UC10-001:** Avaliar depois - sistema envia lembrete após 3 dias
- **FA-UC10-002:** Editar avaliação (permitido uma única vez)
- **FA-UC10-003:** Atendente responde avaliação

### Fluxos de Exceção
- **FE-UC10-001:** Usuário não é o solicitante → retornar HTTP 403 "Apenas o solicitante pode avaliar"
- **FE-UC10-002:** Solicitação não concluída → retornar HTTP 400 "Solicitação ainda não foi concluída"
- **FE-UC10-003:** Comentário > 500 caracteres → retornar HTTP 400 "Comentário muito longo (máximo 500 caracteres)"

### Regras de Negócio
- **RN-UC10-001:** Apenas solicitante pode avaliar (RN-RF021-009)
- **RN-UC10-002:** Avaliação obrigatória - notificações progressivas (imediato, 24h, 48h)
- **RN-UC10-003:** Modal bloqueante após 48 horas (bloqueia navegação até avaliar)
- **RN-UC10-004:** `Avaliacao_Media` recalculada automaticamente após cada avaliação
- **RN-UC10-005:** Serviços com média < 3.0 por 3 meses consecutivos sinalizados ao gestor
- **RN-UC10-006:** Comentários negativos geram ticket de melhoria automático

### Critérios de Aceite
- **CA-UC10-001:** Apenas solicitante PODE avaliar
- **CA-UC10-002:** Estrelas DEVEM ser obrigatórias (1-5)
- **CA-UC10-003:** Comentário DEVE ser opcional (0-500 caracteres)
- **CA-UC10-004:** `Avaliacao_Media` DEVE ser recalculada automaticamente
- **CA-UC10-005:** Notificações progressivas DEVEM ser enviadas (imediato, 24h, 48h)
- **CA-UC10-006:** Modal bloqueante DEVE aparecer após 48 horas

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Aplicadas | Funcionalidades RF Cobertas |
|----|---------------------------|---------------------------|
| UC00 | RN-UC00-001, RN-UC00-002, RN-UC00-003, RN-UC00-004 | RF021-CRUD-02, RF021-SEC-01 |
| UC01 | RN-UC01-001, RN-UC01-002, RN-UC01-003, RN-UC01-004, RN-UC01-005, RN-UC01-006 | RF021-CRUD-01, RF021-VAL-01, RF021-SEC-02, RF021-SEC-03 |
| UC02 | RN-UC02-001, RN-UC02-002, RN-UC02-003 | RF021-CRUD-03, RF021-SEC-01 |
| UC03 | RN-UC03-001, RN-UC03-002, RN-UC03-003, RN-UC03-004 | RF021-CRUD-04, RF021-SEC-02, RF021-SEC-03 |
| UC04 | RN-UC04-001, RN-UC04-002, RN-UC04-003, RN-UC04-004 | RF021-CRUD-05, RF021-SEC-02, RF021-SEC-03 |
| UC05 | RN-UC05-001, RN-UC05-002, RN-UC05-003, RN-UC05-004 | RF021-CRUD-06, RN-RF021-003 |
| UC06 | RN-UC06-001, RN-UC06-002, RN-UC06-003, RN-UC06-004, RN-UC06-005, RN-UC06-006 | RF021-CRUD-07, RN-RF021-002, RN-RF021-008, RN-RF021-010, RN-RF021-012, RN-RF021-013 |
| UC07 | RN-UC07-001, RN-UC07-002, RN-UC07-003, RN-UC07-004, RN-UC07-005, RN-UC07-006, RN-UC07-007 | RF021-CRUD-08, RN-RF021-001, RN-RF021-004, RN-RF021-008 |
| UC08 | RN-UC08-001, RN-UC08-002, RN-UC08-003, RN-UC08-004, RN-UC08-005, RN-UC08-006, RN-UC08-007 | RF021-CRUD-09, RN-RF021-004, RN-RF021-005, RN-RF021-007, RN-RF021-014 |
| UC09 | RN-UC09-001, RN-UC09-002, RN-UC09-003, RN-UC09-004, RN-UC09-005, RN-UC09-006 | RF021-CRUD-10, RN-RF021-004, RN-RF021-011, RN-RF021-014 |
| UC10 | RN-UC10-001, RN-UC10-002, RN-UC10-003, RN-UC10-004, RN-UC10-005, RN-UC10-006 | RF021-CRUD-11, RN-RF021-009 |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - 11 UCs cobrindo 100% do RF021 |
| 1.0 | 2025-12-17 | Sistema | Consolidação inicial de 8 casos de uso (incompleto) |

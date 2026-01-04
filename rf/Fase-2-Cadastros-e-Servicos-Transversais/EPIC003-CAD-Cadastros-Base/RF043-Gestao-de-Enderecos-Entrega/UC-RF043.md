# UC-RF043 — Casos de Uso Canônicos

**RF:** RF043 — Gestão de Endereços de Entrega
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD-Cadastros-Base
**Fase:** Fase-2-Cadastros-e-Servicos-Transversais

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF043**, cobrindo integralmente o comportamento funcional esperado do sistema de gestão de endereços de entrega com validação automática de CEP, geocodificação, cálculo de frete, rastreamento em tempo real e histórico completo de entregas.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF043.yaml)
- Massas de Teste (MT-RF043.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Listar Endereços de Entrega | Usuário Autenticado |
| UC01 | Criar Endereço de Entrega | Usuário Autenticado |
| UC02 | Visualizar Endereço de Entrega | Usuário Autenticado |
| UC03 | Editar Endereço de Entrega | Usuário Autenticado |
| UC04 | Excluir Endereço de Entrega | Usuário Autenticado |
| UC05 | Definir Endereço Padrão | Usuário Autenticado |
| UC06 | Calcular Frete | Usuário Autenticado |
| UC07 | Rastrear Entrega | Usuário Autenticado |
| UC08 | Visualizar Mapa de Calor | Usuário Autenticado |
| UC09 | Exportar Relatório de Entregas | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (ClienteId)
- Todas as ações exigem **permissão explícita** (RBAC)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação**
- Mensagens devem ser claras, previsíveis e rastreáveis
- Validação automática de CEP via ViaCEP com fallback para PostMon
- Geocodificação automática com Google Maps API com fallback para OpenStreetMap

---

## UC00 — Listar Endereços de Entrega

### Objetivo
Permitir que o usuário visualize endereços de entrega disponíveis do seu próprio tenant com busca fuzzy e autocomplete.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW`

### Pós-condições
- Lista exibida conforme filtros e paginação
- Endereços mais usados aparecem primeiro

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa a funcionalidade Gestão de Endereços de Entrega
- **FP-UC00-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.VIEW`
- **FP-UC00-003:** Sistema carrega endereços do tenant (WHERE ClienteId = @currentUserId AND FlExcluido = 0)
- **FP-UC00-004:** Sistema aplica paginação padrão (20 registros) e ordenação (endereços mais usados primeiro via COUNT entregas DESC)
- **FP-UC00-005:** Sistema exibe a lista com colunas: Apelido, CEP, Logradouro, Número, Bairro, Cidade, UF, Categoria, Endereço Padrão

### Fluxos Alternativos
- **FA-UC00-001:** Buscar por termo (mínimo 3 caracteres) com autocomplete fuzzy (RN-RF043-008)
  - Sistema aplica debounce 300ms
  - Busca em: CEP, Logradouro, Bairro, Cidade, NomeFantasia, Referencia
  - Algoritmo Levenshtein (FuzzySharp) aceita erros de digitação
  - Máximo 10 resultados
  - Destaque do termo buscado em negrito
- **FA-UC00-002:** Ordenar por coluna (CEP, Cidade, Categoria)
- **FA-UC00-003:** Filtrar por Categoria (Matriz, Filial, Depósito, Home Office, Temporário)
- **FA-UC00-004:** Filtrar por UF
- **FA-UC00-005:** Visualizar apenas endereços padrão (FlEnderecoPadrao = 1)

### Fluxos de Exceção
- **FE-UC00-001:** Usuário sem permissão → HTTP 403 "Acesso negado"
- **FE-UC00-002:** Nenhum registro encontrado → Estado vazio "Nenhum endereço cadastrado. Clique em 'Novo' para criar."

### Regras de Negócio
- **RN-RF043-008:** Autocomplete ativa após 3 caracteres com debounce 300ms
- RN-UC-00-001: Somente endereços do tenant (isolamento por ClienteId)
- RN-UC-00-002: Endereços excluídos (FlExcluido = 1) não aparecem
- RN-UC-00-003: Paginação padrão 20 registros
- RN-UC-00-004: Ordenação padrão: endereços mais usados primeiro (COUNT entregas)

### Critérios de Aceite
- **CA-UC00-001:** A lista DEVE exibir apenas endereços do tenant do usuário autenticado
- **CA-UC00-002:** Endereços excluídos (soft delete) NÃO devem aparecer na listagem
- **CA-UC00-003:** Paginação DEVE ser aplicada com limite padrão de 20 registros
- **CA-UC00-004:** Sistema DEVE permitir ordenação por qualquer coluna visível
- **CA-UC00-005:** Filtros DEVEM ser acumuláveis e refletir na URL
- **CA-UC00-006:** Autocomplete DEVE ativar após 3 caracteres digitados
- **CA-UC00-007:** Busca fuzzy DEVE aceitar erros de digitação (algoritmo Levenshtein)
- **CA-UC00-008:** Debounce DEVE ser 300ms para evitar buscas excessivas

---

## UC01 — Criar Endereço de Entrega

### Objetivo
Permitir a criação de um novo endereço de entrega com validação automática de CEP, geocodificação e verificação de duplicatas.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.CREATE`

### Pós-condições
- Endereço persistido com coordenadas geográficas
- Auditoria registrada
- Histórico de entregas vazio criado

### Fluxo Principal
- **FP-UC01-001:** Usuário clica em "Novo Endereço"
- **FP-UC01-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.CREATE`
- **FP-UC01-003:** Sistema exibe formulário vazio
- **FP-UC01-004:** Usuário digita CEP (8 dígitos)
- **FP-UC01-005:** Sistema aplica formatação automática (12345678 → 12345-678)
- **FP-UC01-006:** Após 500ms (debounce), sistema dispara requisição para ViaCEP (RN-RF043-001)
- **FP-UC01-007:** API ViaCEP retorna logradouro, bairro, cidade, UF, código IBGE
- **FP-UC01-008:** Sistema preenche automaticamente os campos retornados
- **FP-UC01-009:** Usuário preenche: Número, Complemento, Categoria, Nome Fantasia, Referência
- **FP-UC01-010:** Usuário clica em "Salvar"
- **FP-UC01-011:** Sistema valida campos obrigatórios (CEP, Logradouro, Número, Bairro, Cidade, UF, Categoria)
- **FP-UC01-012:** Sistema verifica duplicatas (CEP + Número + ClienteId) via fuzzy match (RN-RF043-009)
- **FP-UC01-013:** Se não houver duplicatas, sistema envia requisição para Google Maps Geocoding API (RN-RF043-002)
- **FP-UC01-014:** API retorna Latitude, Longitude, Precisão (ROOFTOP/RANGE_INTERPOLATED), PlaceId
- **FP-UC01-015:** Sistema valida coordenadas (Latitude entre -90 e +90, Longitude entre -180 e +180)
- **FP-UC01-016:** Sistema persiste endereço com ClienteId automático
- **FP-UC01-017:** Sistema registra auditoria (CriadoPor, CriadoEm)
- **FP-UC01-018:** Sistema exibe mensagem "Endereço salvo com sucesso!" e redireciona para listagem

### Fluxos Alternativos
- **FA-UC01-001:** API ViaCEP falha (timeout ou erro)
  - Sistema tenta fallback para PostMon (http://api.postmon.com.br/v1/cep/{cep})
  - Se PostMon falhar também, sistema permite preenchimento manual com aviso "CEP não encontrado - verifique se está correto"
- **FA-UC01-002:** Google Maps Geocoding API falha
  - Sistema tenta fallback para OpenStreetMap Nominatim
  - Se ambos falharem, salva endereço sem coordenadas (Latitude/Longitude = NULL)
  - Exibe aviso "Geocodificação falhou - coordenadas não disponíveis"
- **FA-UC01-003:** Salvar e criar outro
  - Após salvar, sistema mantém no formulário e limpa campos
- **FA-UC01-004:** Cancelar criação
  - Sistema descarta dados e retorna para listagem

### Fluxos de Exceção
- **FE-UC01-001:** Erro de validação (campo obrigatório vazio)
  - Sistema exibe mensagens de erro por campo
  - HTTP 400 "Validação falhou: {campo} é obrigatório"
- **FE-UC01-002:** Endereço duplicado detectado (RN-RF043-009)
  - Sistema exibe modal "Endereço similar encontrado. Deseja reutilizar?"
  - Opções: Reutilizar Existente | Salvar Novo | Cancelar
  - HTTP 409 "Endereço similar já existe"
- **FE-UC01-003:** Erro inesperado (banco de dados, rede)
  - Sistema exibe mensagem genérica "Erro ao salvar endereço. Tente novamente."
  - Registra log detalhado
  - HTTP 500

### Regras de Negócio
- **RN-RF043-001:** Validação automática de CEP via ViaCEP com debounce 500ms e fallback para PostMon
- **RN-RF043-002:** Geocodificação automática via Google Maps API com fallback para OpenStreetMap
- **RN-RF043-009:** Validação de duplicatas via fuzzy match (≥90% similaridade) em CEP + Número + Logradouro + ClienteId
- RN-UC-01-001: Campos obrigatórios: CEP, Logradouro, Número, Bairro, Cidade, UF, Categoria
- RN-UC-01-002: ClienteId preenchido automaticamente com tenant do usuário autenticado
- RN-UC-01-003: CriadoPor preenchido automaticamente com ID do usuário
- RN-UC-01-004: CriadoEm preenchido automaticamente com timestamp atual
- RN-UC-01-005: Latitude entre -90 e +90, Longitude entre -180 e +180

### Critérios de Aceite
- **CA-UC01-001:** Todos os campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-002:** ClienteId DEVE ser preenchido automaticamente com o tenant do usuário autenticado
- **CA-UC01-003:** CriadoPor DEVE ser preenchido automaticamente com o ID do usuário autenticado
- **CA-UC01-004:** CriadoEm DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC01-005:** Sistema DEVE validar CEP via ViaCEP com debounce 500ms
- **CA-UC01-006:** Sistema DEVE geocodificar endereço automaticamente via Google Maps API
- **CA-UC01-007:** Sistema DEVE detectar duplicatas via fuzzy match antes de salvar
- **CA-UC01-008:** Auditoria DEVE ser registrada APÓS sucesso da criação
- **CA-UC01-009:** Coordenadas DEVEM estar dentro dos ranges válidos (lat: -90 a +90, long: -180 a +180)

---

## UC02 — Visualizar Endereço de Entrega

### Objetivo
Permitir visualização detalhada de um endereço com histórico completo de entregas realizadas.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW`

### Pós-condições
- Dados exibidos corretamente com histórico de entregas
- Mapa visual com marcador na localização

### Fluxo Principal
- **FP-UC02-001:** Usuário clica em um endereço na listagem
- **FP-UC02-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.VIEW`
- **FP-UC02-003:** Sistema valida tenant (WHERE Id = @id AND ClienteId = @currentUserId)
- **FP-UC02-004:** Sistema carrega dados completos do endereço
- **FP-UC02-005:** Sistema carrega histórico de entregas (RN-RF043-005) - últimas 10 entregas ordenadas por DataEnvio DESC
- **FP-UC02-006:** Sistema exibe mapa com marcador (Latitude/Longitude) usando Google Maps
- **FP-UC02-007:** Sistema calcula estatísticas:
  - Taxa de sucesso de entrega (% Entregue)
  - Tempo médio de entrega (dias úteis)
  - Custo médio de frete (R$)
  - Problemas recorrentes (contagem)
- **FP-UC02-008:** Sistema exibe dados completos + histórico + mapa + estatísticas

### Fluxos Alternativos
- **FA-UC02-001:** Visualizar histórico completo de entregas
  - Clique em "Ver Histórico Completo" abre modal com paginação
- **FA-UC02-002:** Ampliar mapa
  - Clique no mapa abre fullscreen com Google Maps

### Fluxos de Exceção
- **FE-UC02-001:** Endereço inexistente
  - HTTP 404 "Endereço não encontrado"
- **FE-UC02-002:** Endereço de outro tenant
  - HTTP 404 "Endereço não encontrado" (não vazar que existe)
- **FE-UC02-003:** Coordenadas geográficas ausentes
  - Mapa não exibido, mensagem "Geocodificação não disponível"

### Regras de Negócio
- **RN-RF043-005:** Histórico completo de entregas com status, evidências, problemas e avaliação
- RN-UC-02-001: Isolamento por tenant (ClienteId)
- RN-UC-02-002: Informações de auditoria visíveis (CriadoPor, CriadoEm, AlteradoPor, AlteradoEm)
- RN-UC-02-003: Últimas 10 entregas exibidas por padrão

### Critérios de Aceite
- **CA-UC02-001:** Usuário SÓ pode visualizar endereços do próprio tenant
- **CA-UC02-002:** Informações de auditoria DEVEM ser exibidas (CriadoPor, CriadoEm, AlteradoPor, AlteradoEm)
- **CA-UC02-003:** Tentativa de acessar endereço de outro tenant DEVE retornar 404
- **CA-UC02-004:** Tentativa de acessar endereço inexistente DEVE retornar 404
- **CA-UC02-005:** Dados exibidos DEVEM corresponder exatamente ao estado atual no banco
- **CA-UC02-006:** Histórico DEVE exibir últimas 10 entregas ordenadas por data de envio DESC
- **CA-UC02-007:** Estatísticas DEVEM ser calculadas corretamente a partir do histórico
- **CA-UC02-008:** Mapa DEVE exibir marcador na localização se coordenadas existirem

---

## UC03 — Editar Endereço de Entrega

### Objetivo
Permitir alteração controlada de um endereço com revalidação de CEP e regeocodificação.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.EDIT`

### Pós-condições
- Endereço atualizado com coordenadas atualizadas
- Auditoria registrada

### Fluxo Principal
- **FP-UC03-001:** Usuário clica em "Editar" em um endereço
- **FP-UC03-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.EDIT`
- **FP-UC03-003:** Sistema valida tenant
- **FP-UC03-004:** Sistema carrega dados atuais no formulário
- **FP-UC03-005:** Usuário altera campos desejados
- **FP-UC03-006:** Se CEP alterado, sistema revalida via ViaCEP (RN-RF043-001)
- **FP-UC03-007:** Usuário clica em "Salvar"
- **FP-UC03-008:** Sistema valida alterações
- **FP-UC03-009:** Se endereço alterado (Logradouro, Número, Bairro, Cidade, UF), sistema regeocodifica via Google Maps API (RN-RF043-002)
- **FP-UC03-010:** Sistema persiste alterações
- **FP-UC03-011:** Sistema registra auditoria (AlteradoPor, AlteradoEm, shadow properties antes/depois)
- **FP-UC03-012:** Sistema exibe mensagem "Endereço atualizado com sucesso!"

### Fluxos Alternativos
- **FA-UC03-001:** Cancelar edição
  - Sistema descarta alterações e retorna para visualização

### Fluxos de Exceção
- **FE-UC03-001:** Erro de validação
  - Sistema exibe mensagens de erro por campo
  - HTTP 400
- **FE-UC03-002:** Conflito de edição concorrente
  - Sistema detecta alteração desde carregamento inicial
  - HTTP 409 "Endereço foi modificado por outro usuário. Recarregue."
- **FE-UC03-003:** Tentativa de editar endereço de outro tenant
  - HTTP 404

### Regras de Negócio
- **RN-RF043-001:** Revalidação de CEP via ViaCEP se CEP alterado
- **RN-RF043-002:** Regeocodificação via Google Maps API se endereço alterado
- RN-UC-03-001: AlteradoPor preenchido automaticamente com ID do usuário autenticado
- RN-UC-03-002: AlteradoEm preenchido automaticamente com timestamp atual
- RN-UC-03-003: Apenas campos alterados são validados

### Critérios de Aceite
- **CA-UC03-001:** AlteradoPor DEVE ser preenchido automaticamente com ID do usuário autenticado
- **CA-UC03-002:** AlteradoEm DEVE ser preenchido automaticamente com timestamp atual
- **CA-UC03-003:** Sistema DEVE detectar conflitos de edição concorrente
- **CA-UC03-004:** Tentativa de editar endereço de outro tenant DEVE retornar 404
- **CA-UC03-005:** Auditoria DEVE registrar estado anterior e novo estado (shadow properties)
- **CA-UC03-006:** Sistema DEVE revalidar CEP via ViaCEP se CEP alterado
- **CA-UC03-007:** Sistema DEVE regeocodificar se endereço alterado

---

## UC04 — Excluir Endereço de Entrega

### Objetivo
Permitir exclusão lógica de endereços respeitando regra de endereço padrão.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.DELETE`

### Pós-condições
- Endereço marcado como excluído (FlExcluido = 1)

### Fluxo Principal
- **FP-UC04-001:** Usuário clica em "Excluir" em um endereço
- **FP-UC04-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.DELETE`
- **FP-UC04-003:** Sistema verifica se endereço é padrão (FlEnderecoPadrao = 1) (RN-RF043-004)
- **FP-UC04-004:** Sistema exibe modal de confirmação "Tem certeza que deseja excluir este endereço?"
- **FP-UC04-005:** Usuário confirma exclusão
- **FP-UC04-006:** Sistema valida tenant
- **FP-UC04-007:** Sistema verifica dependências (entregas pendentes, pedidos abertos)
- **FP-UC04-008:** Sistema executa soft delete (SET FlExcluido = 1, AlteradoPor = @userId, AlteradoEm = @now)
- **FP-UC04-009:** Sistema registra auditoria
- **FP-UC04-010:** Sistema exibe mensagem "Endereço excluído com sucesso!"

### Fluxos Alternativos
- **FA-UC04-001:** Cancelar exclusão
  - Sistema fecha modal e não executa exclusão
- **FA-UC04-002:** Exclusão em lote
  - Usuário seleciona múltiplos endereços (máximo 50)
  - Sistema executa soft delete em batch

### Fluxos de Exceção
- **FE-UC04-001:** Endereço é padrão (RN-RF043-004)
  - Sistema bloqueia exclusão
  - HTTP 400 "Endereço padrão não pode ser excluído. Defina outro como padrão primeiro."
- **FE-UC04-002:** Endereço possui entregas pendentes
  - Sistema bloqueia exclusão
  - HTTP 400 "Endereço possui entregas pendentes. Aguarde conclusão."
- **FE-UC04-003:** Endereço já excluído
  - HTTP 404 "Endereço não encontrado"

### Regras de Negócio
- **RN-RF043-004:** Endereço padrão (FlEnderecoPadrao = 1) não pode ser excluído
- RN-UC-04-001: Exclusão sempre lógica (soft delete) via FlExcluido = 1
- RN-UC-04-002: Dependências (entregas pendentes) bloqueiam exclusão

### Critérios de Aceite
- **CA-UC04-001:** Exclusão DEVE ser sempre lógica (soft delete) via FlExcluido = 1
- **CA-UC04-002:** Sistema DEVE verificar se endereço é padrão ANTES de permitir exclusão
- **CA-UC04-003:** Sistema DEVE exigir confirmação explícita do usuário
- **CA-UC04-004:** AlteradoEm DEVE ser preenchido com timestamp atual
- **CA-UC04-005:** Tentativa de excluir endereço padrão DEVE retornar erro 400
- **CA-UC04-006:** Endereço excluído NÃO deve aparecer em listagens padrão (WHERE FlExcluido = 0)

---

## UC05 — Definir Endereço Padrão

### Objetivo
Permitir marcar um endereço como padrão garantindo unicidade por tenant.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.SET_DEFAULT`

### Pós-condições
- Endereço marcado como padrão (FlEnderecoPadrao = 1)
- Endereço anteriormente padrão desmarcado (FlEnderecoPadrao = 0)

### Fluxo Principal
- **FP-UC05-001:** Usuário clica em ícone "Estrela" (Definir como Padrão) em um endereço
- **FP-UC05-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.SET_DEFAULT`
- **FP-UC05-003:** Sistema valida tenant
- **FP-UC05-004:** Sistema exibe modal de confirmação "Deseja definir este endereço como padrão?"
- **FP-UC05-005:** Usuário confirma
- **FP-UC05-006:** Sistema inicia transação de banco de dados
- **FP-UC05-007:** Sistema desmarca endereço anteriormente padrão (UPDATE SET FlEnderecoPadrao = 0 WHERE ClienteId = @clienteId AND FlEnderecoPadrao = 1)
- **FP-UC05-008:** Sistema marca novo endereço como padrão (UPDATE SET FlEnderecoPadrao = 1 WHERE Id = @id)
- **FP-UC05-009:** Sistema registra auditoria (AlteradoPor, AlteradoEm) para ambos endereços
- **FP-UC05-010:** Sistema confirma transação (COMMIT)
- **FP-UC05-011:** Sistema exibe mensagem "Endereço definido como padrão com sucesso!"

### Fluxos Alternativos
- **FA-UC05-001:** Cancelar definição
  - Sistema fecha modal sem executar alteração

### Fluxos de Exceção
- **FE-UC05-001:** Endereço já é padrão
  - Sistema exibe mensagem "Este endereço já é o padrão"
- **FE-UC05-002:** Erro em transação
  - Sistema executa ROLLBACK
  - HTTP 500 "Erro ao definir endereço padrão. Tente novamente."

### Regras de Negócio
- **RN-RF043-004:** Apenas 1 endereço padrão por ClienteId (garantido por transação)
- RN-UC-05-001: Operação atômica em transação (desmarcar anterior + marcar novo)
- RN-UC-05-002: Auditoria registrada para ambos endereços (anterior e novo)

### Critérios de Aceite
- **CA-UC05-001:** Operação DEVE ser atômica (transação com COMMIT/ROLLBACK)
- **CA-UC05-002:** Apenas 1 endereço DEVE ter FlEnderecoPadrao = 1 por ClienteId
- **CA-UC05-003:** Endereço anterior DEVE ser desmarcado automaticamente
- **CA-UC05-004:** Auditoria DEVE ser registrada para ambos endereços
- **CA-UC05-005:** Em caso de erro, ROLLBACK DEVE ser executado

---

## UC06 — Calcular Frete

### Objetivo
Permitir cálculo automático de frete consultando múltiplas transportadoras com ordenação por custo-benefício.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW`
- CEP origem e destino válidos

### Pós-condições
- Tabela comparativa exibida com prazo e valor de frete de cada transportadora

### Fluxo Principal
- **FP-UC06-001:** Usuário acessa página de cálculo de frete
- **FP-UC06-002:** Sistema valida permissão
- **FP-UC06-003:** Sistema exibe formulário com campos: CEP Destino, Peso (kg), Dimensões (altura × largura × profundidade em cm), Valor Declarado (R$)
- **FP-UC06-004:** Usuário preenche campos e clica em "Calcular Frete"
- **FP-UC06-005:** Sistema valida campos obrigatórios e ranges (RN-RF043-003):
  - CEP: 8 dígitos válidos
  - Peso: >0 e <100 kg
  - Dimensões: soma (altura + largura + profundidade) ≤200 cm
  - Valor Declarado: ≥0
- **FP-UC06-006:** Sistema verifica cache (6 horas) para mesmos parâmetros
- **FP-UC06-007:** Se não houver cache, sistema dispara consulta paralela (Task.WhenAll) para APIs:
  - Correios (PAC, SEDEX, SEDEX 10, SEDEX Hoje)
  - Jadlog (.Package, .Com, .Corporate)
  - Total Express (Convencional, Econômico, Rodoviário)
- **FP-UC06-008:** Sistema aguarda resposta de todas as APIs (timeout 10s cada)
- **FP-UC06-009:** Sistema agrega resultados e ordena por: mais barato → mais rápido → melhor custo-benefício
- **FP-UC06-010:** Sistema exibe tabela comparativa com colunas: Transportadora, Modalidade, Prazo (dias úteis), Frete (R$), Seguro (R$), Total (R$)

### Fluxos Alternativos
- **FA-UC06-001:** Cache hit
  - Sistema retorna resultados do cache sem consultar APIs
  - Exibe aviso "Valores em cache - consultados há X minutos"
- **FA-UC06-002:** Selecionar transportadora
  - Usuário clica em uma linha da tabela
  - Sistema pré-seleciona para uso em pedido/solicitação

### Fluxos de Exceção
- **FE-UC06-001:** Validação falha (peso >100 kg, dimensões >200 cm)
  - HTTP 400 "Peso deve ser >0 e <100 kg / Dimensões soma ≤200 cm"
- **FE-UC06-002:** Todas as APIs falharam
  - Sistema exibe aviso "Não foi possível calcular frete automaticamente. Digite o valor manualmente."
  - Permite entrada manual de frete
- **FE-UC06-003:** API parcialmente indisponível
  - Sistema exibe resultados das APIs que responderam
  - Exibe aviso "Correios indisponível - valores parciais"

### Regras de Negócio
- **RN-RF043-003:** Consulta paralela a múltiplas APIs com validação de peso, dimensões e cache 6h
- RN-UC-06-001: Peso >0 e <100 kg
- RN-UC-06-002: Dimensões soma ≤200 cm
- RN-UC-06-003: Cache 6 horas para mesmos parâmetros
- RN-UC-06-004: Timeout 10s por API
- RN-UC-06-005: Ordenação: mais barato → mais rápido → custo-benefício

### Critérios de Aceite
- **CA-UC06-001:** Sistema DEVE consultar APIs em paralelo (Task.WhenAll)
- **CA-UC06-002:** Cache DEVE ser aplicado para consultas repetidas (6 horas)
- **CA-UC06-003:** Validações DEVEM bloquear requisição inválida (peso >100 kg, dimensões >200 cm)
- **CA-UC06-004:** Timeout DEVE ser 10s por API
- **CA-UC06-005:** Resultados DEVEM ser ordenados por mais barato → mais rápido
- **CA-UC06-006:** Sistema DEVE permitir entrada manual se todas APIs falharem

---

## UC07 — Rastrear Entrega

### Objetivo
Permitir rastreamento em tempo real de entregas com notificações automáticas via SignalR.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW_HISTORY`
- Código de rastreio válido

### Pós-condições
- Timeline de eventos exibida com status atualizado em tempo real

### Fluxo Principal
- **FP-UC07-001:** Usuário acessa página de rastreamento (via histórico de entrega)
- **FP-UC07-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.VIEW_HISTORY`
- **FP-UC07-003:** Sistema carrega histórico de entrega (EntregaHistorico)
- **FP-UC07-004:** Sistema carrega eventos de rastreamento (RastreamentoEvento) ordenados por DataHora DESC
- **FP-UC07-005:** Sistema estabelece conexão SignalR para receber notificações em tempo real (RN-RF043-006)
- **FP-UC07-006:** Sistema exibe timeline visual com eventos: Postado → Em Trânsito → Saiu para Entrega → Entregue
- **FP-UC07-007:** Sistema exibe dados: Transportadora, Código Rastreio, Status Atual, Última Atualização, Local

### Fluxos Alternativos
- **FA-UC07-001:** Receber notificação de novo evento via webhook (RN-RF043-006)
  - Transportadora envia webhook para /api/webhooks/rastreamento/{transportadora}
  - Sistema valida signature HMAC-SHA256
  - Sistema verifica idempotência (timestamp duplicado)
  - Sistema persiste novo evento (INSERT INTO RastreamentoEvento)
  - Sistema envia notificação SignalR para frontend
  - Frontend atualiza timeline em tempo real
  - Sistema envia e-mail/SMS se evento crítico (SaiuParaEntrega, Entregue)
- **FA-UC07-002:** Polling manual (fallback)
  - Se webhook falhar, Hangfire executa polling a cada 1 hora
  - Sistema consulta API da transportadora via código de rastreio
  - Compara com eventos existentes e insere novos

### Fluxos de Exceção
- **FE-UC07-001:** Código de rastreio inválido
  - HTTP 404 "Rastreio não encontrado"
- **FE-UC07-002:** Webhook com signature inválida
  - HTTP 401 "Signature inválida (HMAC-SHA256)"
  - Log de tentativa de acesso não autorizado
- **FE-UC07-003:** Evento duplicado (idempotência)
  - Sistema ignora silenciosamente (não insere)

### Regras de Negócio
- **RN-RF043-006:** Notificações em tempo real via webhooks com validação HMAC-SHA256 e fallback polling
- RN-UC-07-001: Webhooks validam signature para segurança
- RN-UC-07-002: Idempotência: eventos duplicados são ignorados
- RN-UC-07-003: Notificações SignalR (push), e-mail (importantes), SMS (críticos)
- RN-UC-07-004: Fallback polling a cada 1 hora via Hangfire

### Critérios de Aceite
- **CA-UC07-001:** Sistema DEVE validar signature HMAC-SHA256 de webhooks
- **CA-UC07-002:** Sistema DEVE implementar idempotência (ignorar eventos duplicados)
- **CA-UC07-003:** Sistema DEVE enviar notificações SignalR em tempo real
- **CA-UC07-004:** Sistema DEVE enviar e-mail para eventos importantes
- **CA-UC07-005:** Sistema DEVE enviar SMS apenas para eventos críticos (SaiuParaEntrega, Entregue)
- **CA-UC07-006:** Sistema DEVE executar polling a cada 1 hora como fallback

---

## UC08 — Visualizar Mapa de Calor

### Objetivo
Permitir análise estratégica de entregas por região com visualização de concentração geográfica.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW`

### Pós-condições
- Mapa de calor exibido com concentração de entregas por região

### Fluxo Principal
- **FP-UC08-001:** Usuário acessa dashboard "Mapa de Calor de Entregas"
- **FP-UC08-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.VIEW`
- **FP-UC08-003:** Sistema agrega entregas por coordenadas geográficas (3 casas decimais ~100m de raio) (RN-RF043-007)
- **FP-UC08-004:** Sistema aplica filtro padrão: último mês, status Entregue
- **FP-UC08-005:** Sistema carrega dados agregados (máximo 10.000 pontos)
- **FP-UC08-006:** Sistema renderiza mapa de calor usando Google Maps Heatmap Layer
- **FP-UC08-007:** Sistema aplica cores:
  - Verde: <10 entregas/mês
  - Amarelo: 10-50 entregas/mês
  - Vermelho: >50 entregas/mês
- **FP-UC08-008:** Sistema exibe filtros: Período, Status, Transportadora

### Fluxos Alternativos
- **FA-UC08-001:** Aplicar filtros
  - Usuário seleciona período, status, transportadora
  - Sistema recarrega dados e atualiza mapa
- **FA-UC08-002:** Clique em região
  - Sistema exibe modal com lista de endereços e estatísticas da região
  - Estatísticas: total entregas, taxa sucesso, tempo médio, custo médio

### Fluxos de Exceção
- **FE-UC08-001:** Mais de 10.000 pontos (performance)
  - Sistema agrega por CEP em vez de coordenadas precisas
  - Exibe aviso "Dados agregados por CEP para melhor performance"
- **FE-UC08-002:** Nenhuma entrega no período
  - Sistema exibe mapa vazio com mensagem "Nenhuma entrega encontrada no período selecionado"

### Regras de Negócio
- **RN-RF043-007:** Mapa de calor com agregação por 3 casas decimais e máximo 10.000 pontos
- RN-UC-08-001: Agregação por 3 casas decimais (ROUND(Latitude, 3), ROUND(Longitude, 3))
- RN-UC-08-002: Cores: Verde (<10), Amarelo (10-50), Vermelho (>50)
- RN-UC-08-003: Performance: máximo 10.000 pontos (senão agregar por CEP)

### Critérios de Aceite
- **CA-UC08-001:** Sistema DEVE agregar entregas por coordenadas com 3 casas decimais
- **CA-UC08-002:** Sistema DEVE aplicar cores conforme concentração (Verde/Amarelo/Vermelho)
- **CA-UC08-003:** Sistema DEVE limitar a 10.000 pontos para performance
- **CA-UC08-004:** Se >10.000 pontos, sistema DEVE agregar por CEP
- **CA-UC08-005:** Clique em região DEVE exibir lista de endereços e estatísticas

---

## UC09 — Exportar Relatório de Entregas

### Objetivo
Permitir exportação de relatório completo de entregas em Excel/PDF com filtros personalizados.

### Pré-condições
- Usuário autenticado
- Permissão `GES.ENDERECOS_ENTREGA.VIEW`

### Pós-condições
- Arquivo Excel/PDF gerado e baixado

### Fluxo Principal
- **FP-UC09-001:** Usuário clica em "Exportar Relatório" na listagem de entregas
- **FP-UC09-002:** Sistema valida permissão `GES.ENDERECOS_ENTREGA.VIEW`
- **FP-UC09-003:** Sistema exibe modal com filtros:
  - Formato: Excel (.xlsx) | PDF (.pdf)
  - Período: Data Início - Data Fim (máximo 1 ano)
  - Status: Entregue | Em Trânsito | Devolvido | Extraviado
  - Endereço: Dropdown com autocomplete
  - Transportadora: Correios | Jadlog | Total Express
- **FP-UC09-004:** Usuário seleciona filtros e clica em "Gerar Relatório"
- **FP-UC09-005:** Sistema valida filtros (RN-RF043-010):
  - Período máximo 1 ano (365 dias)
  - Máximo 10.000 registros
- **FP-UC09-006:** Sistema executa query com filtros aplicados
- **FP-UC09-007:** Se Excel: sistema usa EPPlus para gerar .xlsx com formatação condicional (verde=entregue, vermelho=devolvido, amarelo=em trânsito)
- **FP-UC09-008:** Se PDF: sistema usa QuestPDF para gerar .pdf com tabela formatada
- **FP-UC09-009:** Sistema calcula totalizadores:
  - Total de entregas
  - Entregues (quantidade e %)
  - Devolvidas (quantidade e %)
  - Custo total de frete (R$)
  - Custo médio (R$)
  - Avaliação média (estrelas)
- **FP-UC09-010:** Sistema adiciona footer: "Gerado em: {DateTime.Now} | Usuário: {userName}"
- **FP-UC09-011:** Sistema retorna arquivo para download (Content-Disposition: attachment)

### Fluxos Alternativos
- **FA-UC09-001:** Cancelar exportação
  - Sistema fecha modal sem gerar arquivo

### Fluxos de Exceção
- **FE-UC09-001:** Período maior que 1 ano
  - HTTP 400 "Período máximo: 1 ano"
- **FE-UC09-002:** Mais de 10.000 registros
  - HTTP 400 "Máximo 10.000 registros. Filtre mais ou gere em lote."
- **FE-UC09-003:** Nenhum registro encontrado
  - HTTP 400 "Nenhuma entrega encontrada com os filtros selecionados"

### Regras de Negócio
- **RN-RF043-010:** Exportação em Excel/PDF com período máximo 1 ano e limite 10.000 registros
- RN-UC-09-001: Período máximo 1 ano (365 dias)
- RN-UC-09-002: Máximo 10.000 registros por exportação
- RN-UC-09-003: Excel: formatação condicional por status
- RN-UC-09-004: Totalizadores obrigatórios no rodapé

### Critérios de Aceite
- **CA-UC09-001:** Sistema DEVE validar período máximo 1 ano
- **CA-UC09-002:** Sistema DEVE validar máximo 10.000 registros
- **CA-UC09-003:** Excel DEVE ter formatação condicional (verde/vermelho/amarelo)
- **CA-UC09-004:** Totalizadores DEVEM ser calculados corretamente
- **CA-UC09-005:** Footer DEVE incluir data de geração e usuário
- **CA-UC09-006:** Arquivo DEVE ser retornado para download (Content-Disposition: attachment)

---

## 4. MATRIZ DE RASTREABILIDADE

| UC | Regras de Negócio Cobertas |
|----|---------------------------|
| UC00 | RN-RF043-008 (Autocomplete) |
| UC01 | RN-RF043-001 (Validação CEP), RN-RF043-002 (Geocodificação), RN-RF043-009 (Duplicatas) |
| UC02 | RN-RF043-005 (Histórico de Entregas) |
| UC03 | RN-RF043-001 (Revalidação CEP), RN-RF043-002 (Regeocodificação) |
| UC04 | RN-RF043-004 (Endereço Padrão não pode ser excluído) |
| UC05 | RN-RF043-004 (Apenas 1 endereço padrão) |
| UC06 | RN-RF043-003 (Cálculo de Frete) |
| UC07 | RN-RF043-006 (Rastreamento em Tempo Real) |
| UC08 | RN-RF043-007 (Mapa de Calor) |
| UC09 | RN-RF043-010 (Exportação de Relatório) |

**Cobertura:** 10/10 regras de negócio (100%)

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato com cobertura completa das 10 regras de negócio |

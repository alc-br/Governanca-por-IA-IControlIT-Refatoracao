# Casos de Uso - RF087

**Versão:** 1.0
**Data:** 2025-12-17
**RF Relacionado:** [RF087 - Integracoes-e-APIs-Externas](./RF087.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Integrações | Caso de uso |
| UC01 | UC01 - Criar Integração | Caso de uso |
| UC02 | UC02 - Editar Integração | Caso de uso |
| UC02 | Visualizar Detalhes de Integração | Caso de uso |
| UC03 | Editar Integração | Caso de uso |
| UC03 | UC03 - Visualizar Integração | Caso de uso |
| UC04 | UC04 - Ativar/Desativar Integração | Caso de uso |
| UC04 | Executar Integração Manualmente | Caso de uso |
| UC05 | UC05 - Executar Integração | Caso de uso |
| UC05 | Receber e Processar Webhook | Caso de uso |
| UC06 | UC06 - Executar Ações Diretas em Notificação | Caso de uso |

---

# UC00 - Listar Integrações

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC00
- **Nome:** Listar Integrações
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:** Usuário logado com permissão INTEGRACOES.VIEW

---

## 2. Fluxo Principal

1. Usuário acessa o menu "Integrações"
2. Sistema carrega lista paginada de integrações da empresa
3. Sistema exibe tabela com: Código, Nome, Tipo, Status, Circuit Breaker, Última Execução
4. Usuário pode:
   - Filtrar por tipo, status, busca textual
   - Ordenar por qualquer coluna
   - Paginar resultados
   - Clicar para ver detalhes

---

## 3. Fluxos Alternativos

### FA01 - Filtrar por Tipo
1. Usuário seleciona tipo no dropdown
2. Sistema filtra lista pelo tipo selecionado

### FA02 - Busca Textual
1. Usuário digita no campo de busca
2. Sistema filtra por código, nome ou tags

### FA03 - Lista Vazia
1. Sistema não encontra integrações
2. Sistema exibe mensagem "Nenhuma integração encontrada"

---

## 4. Exceções

### E01 - Sem Permissão
- Sistema redireciona para página de acesso negado

### E02 - Erro de Conexão
- Sistema exibe mensagem de erro e botão "Tentar novamente"

---

## 5. Regras de Negócio

- RN-NPV-002-02: Tipos de integração suportados
- RN-NPV-002-06: Estados do Circuit Breaker
- RN-NPV-002-12: Estatísticas de execução

---

## 6. Interface

### Campos da Listagem
| Campo | Tipo | Descrição |
|-------|------|-----------|
| Código | Texto | Código único |
| Nome | Texto | Nome descritivo |
| Tipo | Badge | Tipo da integração |
| Status | Toggle | Ativo/Inativo |
| Circuit Breaker | Indicador | CLOSED/OPEN/HALF_OPEN |
| Última Execução | Data | Data da última execução |
| Ações | Botões | Ver, Editar, Executar |

### Filtros
- Tipo (dropdown)
- Status (Todos/Ativos/Inativos)
- Busca (texto)

---

## 7. Chaves i18n

- integracoes.list.title
- integracoes.list.empty
- integracoes.filter.tipo
- integracoes.filter.status
- integracoes.table.codigo
- integracoes.table.nome
- integracoes.table.tipo
- integracoes.table.status
- integracoes.table.circuitBreaker
- integracoes.table.ultimaExecucao

---

# UC01 - Criar Integração

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC01
- **Nome:** Criar Integração
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:** Usuário logado com permissão INTEGRACOES.CREATE

---

## 2. Fluxo Principal

1. Usuário clica em "Nova Integração"
2. Sistema exibe formulário com abas: Básico, Autenticação, Avançado
3. Usuário preenche campos obrigatórios:
   - Código, Nome, Tipo, URL Base, Tipo de Autenticação
4. Usuário preenche credenciais conforme tipo de autenticação
5. Usuário clica em "Salvar"
6. Sistema valida dados
7. Sistema cria integração
8. Sistema exibe mensagem de sucesso
9. Sistema redireciona para lista

---

## 3. Fluxos Alternativos

### FA01 - Configurar Autenticação Basic
1. Usuário seleciona "BASIC"
2. Sistema exibe campos: Usuário, Senha

### FA02 - Configurar OAuth2
1. Usuário seleciona "OAUTH2"
2. Sistema exibe campos: Client ID, Client Secret, Token URL, Scopes

### FA03 - Habilitar Webhook
1. Usuário marca "Habilitar Webhook"
2. Sistema exibe campos: URL Webhook, Secret

### FA04 - Habilitar Fila
1. Usuário marca "Habilitar Fila"
2. Sistema exibe campo: Máximo Retentativas

### FA05 - Adicionar Endpoint
1. Usuário clica em "Adicionar Endpoint"
2. Sistema exibe modal com: Path, Método, Descrição

---

## 4. Exceções

### E01 - Código Duplicado
- Sistema exibe: "Já existe uma integração com este código"

### E02 - URL Inválida
- Sistema exibe: "URL base inválida"

### E03 - Credenciais Inválidas
- Sistema exibe: "Formato de credenciais inválido para o tipo de autenticação"

---

## 5. Regras de Negócio

- RN-NPV-002-01: Código único de integração
- RN-NPV-002-02: Tipos de integração suportados
- RN-NPV-002-03: Métodos de autenticação
- RN-NPV-002-04: Credenciais criptografadas
- RN-NPV-002-05: Timeout padrão
- RN-NPV-002-09: Validação de URL base

---

## 6. Interface

### Aba Básico
| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Código | Texto | Sim | Máx 50 caracteres, único |
| Nome | Texto | Sim | Máx 200 caracteres |
| Descrição | Textarea | Não | Máx 1000 caracteres |
| Tipo | Select | Sim | Valores do enum |
| URL Base | URL | Sim | URL válida |
| Tags | Chips | Não | Separadas por vírgula |

### Aba Autenticação
| Campo | Tipo | Obrigatório | Validação |
|-------|------|-------------|-----------|
| Tipo Autenticação | Select | Sim | Valores do enum |
| Credenciais | Dinâmico | Condicional | Depende do tipo |

### Aba Avançado
| Campo | Tipo | Obrigatório | Default |
|-------|------|-------------|---------|
| Timeout (s) | Número | Não | 30 |
| Retentativas | Número | Não | 3 |
| Delay Retry (ms) | Número | Não | 1000 |
| Circuit Breaker Threshold | Número | Não | 5 |
| Circuit Breaker Duração (s) | Número | Não | 60 |
| Rate Limit Requisições | Número | Não | - |
| Rate Limit Período (s) | Número | Não | - |
| Aceitar Certificado Inválido | Toggle | Não | false |

---

## 7. Chaves i18n

- integracoes.create.title
- integracoes.form.codigo
- integracoes.form.nome
- integracoes.form.descricao
- integracoes.form.tipo
- integracoes.form.baseUrl
- integracoes.form.autenticacao
- integracoes.form.timeout
- integracoes.form.retry
- integracoes.messages.created
- integracoes.errors.duplicateCode
- integracoes.errors.invalidUrl

---

# UC02 - Editar Integração

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC02
- **Nome:** Editar Integração
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:** Usuário logado com permissão INTEGRACOES.EDIT

---

## 2. Fluxo Principal

1. Usuário clica em "Editar" na integração desejada
2. Sistema carrega dados da integração
3. Sistema exibe formulário preenchido
4. Usuário altera campos desejados
5. Usuário clica em "Salvar"
6. Sistema valida dados
7. Sistema atualiza integração
8. Sistema exibe mensagem de sucesso
9. Sistema retorna para lista

---

## 3. Fluxos Alternativos

### FA01 - Alterar Credenciais
1. Usuário clica em "Alterar Credenciais"
2. Sistema exibe campos de credenciais vazios
3. Usuário preenche novas credenciais

### FA02 - Gerenciar Endpoints
1. Usuário pode adicionar, editar ou remover endpoints
2. Sistema atualiza lista de endpoints

### FA03 - Resetar Circuit Breaker
1. Usuário clica em "Resetar Circuit Breaker"
2. Sistema confirma ação
3. Sistema reseta estado para CLOSED

---

## 4. Exceções

### E01 - Integração Não Encontrada
- Sistema exibe erro 404

### E02 - Código Duplicado
- Sistema exibe: "Já existe outra integração com este código"

### E03 - Sem Permissão
- Sistema exibe erro 403

---

## 5. Regras de Negócio

- RN-NPV-002-01: Código único de integração
- RN-NPV-002-04: Credenciais criptografadas
- RN-NPV-002-06: Circuit Breaker
- RN-NPV-002-11: Endpoints configuráveis
- RN-NPV-002-15: Auditoria de execuções

---

## 6. Interface

Mesma estrutura do UC01 (Criar), com campos preenchidos e opção de alterar credenciais.

### Campos Adicionais
| Campo | Tipo | Descrição |
|-------|------|-----------|
| Alterar Credenciais | Botão | Exibe campos de credenciais |
| Resetar Circuit Breaker | Botão | Reseta para CLOSED |
| Estatísticas | Painel | Exibe métricas de uso |

---

## 7. Chaves i18n

- integracoes.edit.title
- integracoes.form.alterarCredenciais
- integracoes.form.resetarCircuitBreaker
- integracoes.messages.updated
- integracoes.errors.notFound

---

# UC02: Visualizar Detalhes de Integração

**Última Atualização**: 05/11/2025

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Administrador do Sistema
**Pré-condições**: Usuário autenticado com permissão `SYS.INTEGRACOES.READ`
**Pós-condições**: Detalhes completos da integração exibidos

---

## 🎯 OBJETIVO

Visualizar detalhes completos de uma integração, incluindo configuração, estatísticas, histórico de execuções e estado do circuit breaker.

---

## 📝 FLUXO PRINCIPAL

1. Usuário clica em ícone "👁️ Visualizar" na lista de integrações
2. Sistema carrega detalhes da integração
3. Sistema exibe tela com 5 tabs:
   - **Informações**: Configuração geral
   - **Execuções**: Histórico de execuções
   - **Estatísticas**: Métricas e gráficos
   - **Endpoints**: Lista de endpoints configurados
   - **Auditoria**: Histórico de alterações
4. Tab "Informações" exibida por padrão com:
   - Código, nome, descrição
   - Tipo, URL base
   - Status (ativo/inativo)
   - Tipo de autenticação (credenciais mascaradas)
   - Políticas de resiliência (timeout, retry, circuit breaker, rate limit)
   - Metadados customizados
5. Botões de ação disponíveis:
   - ✏️ Editar
   - ▶️ Executar Manualmente
   - 📊 Ver Estatísticas
   - 🔄 Testar Conexão

---

## 🔐 REGRAS DE NEGÓCIO

**RN-UC02-001**: Credenciais NUNCA devem ser exibidas em plain text (sempre mascaradas)
**RN-UC02-002**: Histórico de execuções exibe últimas 100 execuções por padrão
**RN-UC02-003**: Estatísticas calculadas sobre últimas 24h, 7 dias, 30 dias
**RN-UC02-004**: Multi-tenancy: usuário só vê integrações do seu conglomerado

---

## 📤 ENDPOINT API

```http
GET /api/integration/{id}
Authorization: Bearer {token}
```

### Response (200 OK)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "codigo": "SAP-001",
  "nome": "SAP ERP Integration",
  "descricao": "Integração com SAP...",
  "tipo": "REST_API",
  "baseUrl": "https://sap.empresa.com/api",
  "autenticacaoTipo": "BASIC",
  "credenciaisMascaradas": {
    "username": "api_user@example.com",
    "password": "********"
  },
  "timeoutSegundos": 30,
  "retryTentativas": 3,
  "circuitBreakerState": "CLOSED",
  "ultimasExecucoes": [...],
  "estatisticas": {
    "taxaSucesso24h": 98.5,
    "totalExecucoes24h": 145,
    "latenciaMedia": 234
  }
}
```

---

# UC03: Editar Integração

**Última Atualização**: 05/11/2025

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Administrador do Sistema
**Pré-condições**: Usuário autenticado com permissão `SYS.INTEGRACOES.UPDATE`
**Pós-condições**: Integração atualizada, histórico registrado

---

## 🎯 OBJETIVO

Permitir edição de configurações de uma integração existente, preservando histórico de alterações.

---

## 📝 FLUXO PRINCIPAL

1. Usuário clica em "✏️ Editar" nos detalhes da integração
2. Sistema carrega formulário pré-preenchido (mesmo wizard de criação)
3. Campos de credenciais aparecem mascarados (••••••)
4. Usuário altera campos desejados
5. Ao alterar credenciais, sistema solicita confirmação
6. Usuário clica "Salvar Alterações"
7. Sistema valida mudanças
8. Sistema compara valores anteriores vs novos
9. Sistema salva alterações
10. Sistema registra histórico de alterações (campo por campo)
11. Sistema invalida cache (se houver)
12. Sistema exibe mensagem: "Integração atualizada com sucesso!"

---

## 🔐 REGRAS DE NEGÓCIO

**RN-UC03-001**: Alteração de credenciais requer confirmação explícita
**RN-UC03-002**: Código não pode ser alterado após criação
**RN-UC03-003**: Histórico registra campo, valor anterior e novo
**RN-UC03-004**: Alterar de ativo→inativo fecha todas as execuções pendentes
**RN-UC03-005**: Alterações críticas (URL, autenticação) resetam circuit breaker

---

## 📤 ENDPOINT API

```http
PUT /api/integration/{id}
Authorization: Bearer {token}

{
  "nome": "SAP ERP Integration (Updated)",
  "timeoutSegundos": 45,
  "retryTentativas": 5
}
```

### Response (200 OK)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "message": "Integração atualizada com sucesso!",
  "camposAlterados": ["nome", "timeoutSegundos", "retryTentativas"]
}
```

---

# UC03 - Visualizar Integração

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC03
- **Nome:** Visualizar Integração
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:** Usuário logado com permissão INTEGRACOES.VIEW

---

## 2. Fluxo Principal

1. Usuário clica em integração na lista
2. Sistema carrega dados completos da integração
3. Sistema exibe página de detalhes com:
   - Informações básicas
   - Estatísticas de execução
   - Estado do Circuit Breaker
   - Lista de endpoints
   - Histórico de execuções

---

## 3. Fluxos Alternativos

### FA01 - Ver Histórico de Execuções
1. Usuário clica na aba "Histórico"
2. Sistema exibe lista paginada de execuções
3. Usuário pode filtrar por data, status, endpoint

### FA02 - Ver Detalhes de Execução
1. Usuário clica em uma execução
2. Sistema exibe modal com: Request, Response, Duração, Status

### FA03 - Exportar Estatísticas
1. Usuário clica em "Exportar"
2. Sistema gera relatório em CSV/PDF

---

## 4. Exceções

### E01 - Integração Não Encontrada
- Sistema exibe erro 404 e redireciona para lista

---

## 5. Regras de Negócio

- RN-NPV-002-06: Estados do Circuit Breaker
- RN-NPV-002-12: Estatísticas de execução
- RN-NPV-002-15: Auditoria de execuções

---

## 6. Interface

### Painel de Informações
| Campo | Descrição |
|-------|-----------|
| Código | Código da integração |
| Nome | Nome descritivo |
| Tipo | Tipo com badge |
| Status | Ativo/Inativo |
| URL Base | URL do serviço |
| Autenticação | Tipo de autenticação |
| Criado em | Data de criação |
| Modificado em | Data da última alteração |

### Painel de Estatísticas
| Métrica | Descrição |
|---------|-----------|
| Total Execuções | Quantidade total |
| Taxa de Sucesso | Percentual |
| Tempo Médio | Em milissegundos |
| Última Execução | Data/hora |

### Painel Circuit Breaker
| Campo | Descrição |
|-------|-----------|
| Estado | CLOSED/OPEN/HALF_OPEN |
| Falhas | Quantidade de falhas |
| Última Falha | Data/hora |
| Próxima Tentativa | Data/hora (se OPEN) |

### Lista de Endpoints
| Campo | Descrição |
|-------|-----------|
| Path | Caminho do endpoint |
| Método | GET/POST/PUT/DELETE |
| Status | Ativo/Inativo |
| Ações | Executar, Editar |

---

## 7. Chaves i18n

- integracoes.details.title
- integracoes.details.estatisticas
- integracoes.details.circuitBreaker
- integracoes.details.endpoints
- integracoes.details.historico
- integracoes.details.totalExecucoes
- integracoes.details.taxaSucesso
- integracoes.details.tempoMedio

---

# UC04 - Ativar/Desativar Integração

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC04
- **Nome:** Ativar/Desativar Integração
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:** Usuário logado com permissão INTEGRACOES.EDIT

---

## 2. Fluxo Principal - Desativar

1. Usuário clica no toggle de status (Ativo -> Inativo)
2. Sistema exibe confirmação: "Deseja desativar esta integração?"
3. Usuário confirma
4. Sistema desativa integração
5. Sistema exibe mensagem: "Integração desativada com sucesso"

---

## 3. Fluxo Principal - Ativar

1. Usuário clica no toggle de status (Inativo -> Ativo)
2. Sistema ativa integração
3. Sistema exibe mensagem: "Integração ativada com sucesso"

---

## 4. Fluxos Alternativos

### FA01 - Cancelar Desativação
1. Usuário clica em "Cancelar" na confirmação
2. Sistema mantém estado atual

### FA02 - Ativar com Circuit Breaker Aberto
1. Sistema detecta Circuit Breaker em estado OPEN
2. Sistema exibe aviso: "Atenção: Circuit Breaker está aberto"
3. Usuário pode prosseguir ou resetar Circuit Breaker primeiro

---

## 5. Exceções

### E01 - Integração Não Encontrada
- Sistema exibe erro 404

### E02 - Sem Permissão
- Sistema exibe erro 403

---

## 6. Regras de Negócio

- RN-NPV-002-06: Estados do Circuit Breaker
- RN-NPV-002-15: Auditoria de execuções

---

## 7. Interface

### Toggle na Lista
- Componente: mat-slide-toggle
- Estados: Ativo (verde), Inativo (cinza)

### Modal de Confirmação (Desativar)
- Título: "Desativar Integração"
- Mensagem: "Deseja desativar a integração {nome}? Ela não será mais executada automaticamente."
- Botões: "Cancelar", "Desativar"

---

## 8. Chaves i18n

- integracoes.status.ativo
- integracoes.status.inativo
- integracoes.confirm.desativar.title
- integracoes.confirm.desativar.message
- integracoes.messages.ativada
- integracoes.messages.desativada
- integracoes.warnings.circuitBreakerOpen

---

# UC04: Executar Integração Manualmente

**Última Atualização**: 05/11/2025

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Administrador do Sistema
**Pré-condições**: Usuário autenticado com permissão `SYS.INTEGRACOES.EXECUTE`
**Pós-condições**: Integração executada, resultado registrado

---

## 🎯 OBJETIVO

Permitir execução manual de uma integração para testes ou operações sob demanda.

---

## 📝 FLUXO PRINCIPAL

1. Usuário clica em "▶️ Executar" na integração
2. Sistema exibe modal com:
   - Seleção de endpoint (se houver múltiplos)
   - Parâmetros dinâmicos (JSON editor)
   - Checkbox "Executar síncrono" (padrão: assíncrono)
3. Usuário preenche parâmetros (opcional)
4. Usuário clica "Executar"
5. **Se assíncrono**:
   - Sistema enfileira mensagem no RabbitMQ
   - Sistema retorna: "Execução enfileirada! ID: {guid}"
   - Worker processa em background
   - Usuário recebe notificação quando concluir
6. **Se síncrono**:
   - Sistema exibe loading spinner
   - Sistema executa requisição HTTP
   - Sistema aplica políticas Polly (retry, circuit breaker)
   - Sistema exibe resultado em tempo real
7. Sistema registra execução em `IntegracaoExecucao`
8. Sistema atualiza estatísticas de circuit breaker

---

## 🔐 REGRAS DE NEGÓCIO

**RN-UC04-001**: Circuit breaker OPEN bloqueia execução manual com mensagem: "Circuit breaker aberto. Tente novamente em X segundos."
**RN-UC04-002**: Execução síncrona limitada a timeout máximo de 2 minutos
**RN-UC04-003**: Execução assíncrona sem limite de tempo
**RN-UC04-004**: Rate limiting aplicado mesmo em execuções manuais
**RN-UC04-005**: Logs de request/response obrigatórios em execuções manuais (ignorar flags)

---

## 📤 ENDPOINT API

```http
POST /api/integration/{id}/execute
Authorization: Bearer {token}

{
  "endpointId": "abc-123",
  "parametros": {
    "dataInicio": "2025-01-01",
    "dataFim": "2025-01-31"
  },
  "executarSincrono": false
}
```

### Response (202 Accepted) - Assíncrono

```json
{
  "execucaoId": "def-456",
  "message": "Execução enfileirada com sucesso!",
  "estimativaProcessamento": "30 segundos",
  "posicaoNaFila": 3
}
```

### Response (200 OK) - Síncrono

```json
{
  "execucaoId": "def-456",
  "status": "SUCESSO",
  "duracaoMs": 234,
  "resultado": {
    "totalImportados": 150,
    "totalErros": 2
  }
}
```

---

# UC05 - Executar Integração

**RF:** RF-NPV-002
**Versão:** 1.0
**Data:** 2025-01-19

---

## 1. Identificação

- **Código:** UC05
- **Nome:** Executar Integração
- **Ator Principal:** Usuário Autenticado
- **Pré-condições:**
  - Usuário logado com permissão INTEGRACOES.EXECUTE
  - Integração ativa
  - Circuit Breaker não em estado OPEN

---

## 2. Fluxo Principal

1. Usuário clica em "Executar" na integração ou endpoint
2. Sistema exibe modal de execução com:
   - Endpoint selecionado (ou opção para escolher)
   - Payload (se aplicável)
   - Opções de override
3. Usuário configura execução
4. Usuário clica em "Executar"
5. Sistema executa integração
6. Sistema exibe resultado:
   - Status HTTP
   - Tempo de resposta
   - Response Body
7. Sistema atualiza estatísticas

---

## 3. Fluxos Alternativos

### FA01 - Executar com Payload
1. Usuário seleciona método POST/PUT/PATCH
2. Sistema exibe editor de JSON para payload
3. Usuário preenche payload

### FA02 - Override de URL
1. Usuário marca "Override URL"
2. Sistema exibe campo para URL personalizada

### FA03 - Override de Método
1. Usuário marca "Override Método"
2. Sistema exibe select para escolher método

### FA04 - Execução com Erro
1. Sistema recebe erro do serviço
2. Sistema exibe mensagem de erro
3. Sistema registra falha nas estatísticas
4. Se threshold atingido, abre Circuit Breaker

### FA05 - Timeout
1. Sistema aguarda além do timeout configurado
2. Sistema cancela execução
3. Sistema registra timeout nas estatísticas

---

## 4. Exceções

### E01 - Circuit Breaker Aberto
- Sistema exibe: "Não é possível executar. Circuit Breaker está aberto."
- Sistema informa quando poderá tentar novamente

### E02 - Rate Limit Excedido
- Sistema exibe erro 429: "Limite de requisições excedido"
- Sistema informa tempo de espera

### E03 - Integração Inativa
- Sistema exibe: "Integração está inativa"

### E04 - Credenciais Inválidas
- Sistema exibe erro 401: "Falha na autenticação"

---

## 5. Regras de Negócio

- RN-NPV-002-05: Timeout padrão
- RN-NPV-002-06: Circuit Breaker
- RN-NPV-002-07: Rate Limiting
- RN-NPV-002-08: Retry com Backoff
- RN-NPV-002-12: Estatísticas de execução
- RN-NPV-002-15: Auditoria de execuções

---

## 6. Interface

### Modal de Execução
| Campo | Tipo | Descrição |
|-------|------|-----------|
| Endpoint | Select | Endpoint a executar |
| Método | Select | GET/POST/PUT/DELETE/PATCH |
| URL Override | Texto | URL personalizada (opcional) |
| Headers | JSON Editor | Headers adicionais |
| Payload | JSON Editor | Corpo da requisição |

### Resultado da Execução
| Campo | Descrição |
|-------|-----------|
| Status | Código HTTP com cor (verde/amarelo/vermelho) |
| Duração | Tempo em ms |
| Tentativa | Número da tentativa (retry) |
| Response | JSON formatado |
| Error | Mensagem de erro (se houver) |

---

## 7. Chaves i18n

- integracoes.execute.title
- integracoes.execute.endpoint
- integracoes.execute.metodo
- integracoes.execute.payload
- integracoes.execute.headers
- integracoes.execute.resultado
- integracoes.execute.duracao
- integracoes.execute.tentativa
- integracoes.messages.executed
- integracoes.errors.circuitBreakerOpen
- integracoes.errors.rateLimitExceeded
- integracoes.errors.timeout
- integracoes.errors.authFailed

---

# UC05: Receber e Processar Webhook

**Última Atualização**: 05/11/2025

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Sistema Externo
**Pré-condições**: Integração do tipo WEBHOOK_IN configurada com token
**Pós-condições**: Webhook recebido, validado e processado

---

## 🎯 OBJETIVO

Receber webhooks de sistemas externos, validar assinatura HMAC, enfileirar para processamento assíncrono.

---

## 📝 FLUXO PRINCIPAL

1. Sistema externo envia POST para `https://api.icontrolit.com/api/integration/webhook/{token}`
2. Sistema valida se token existe e integração está ativa
3. Sistema extrai header `X-Signature` (HMAC-SHA256)
4. Sistema recalcula HMAC usando webhook secret + payload
5. Sistema compara assinaturas (recebida vs calculada)
6. Se assinatura válida:
   - Sistema salva webhook em `IntegracaoWebhook` (status PENDENTE)
   - Sistema enfileira mensagem no RabbitMQ (prioridade 1=Crítico)
   - Sistema retorna HTTP 202 Accepted
7. Worker consome mensagem da fila
8. Worker processa payload (lógica customizada por integração)
9. Worker atualiza status para SUCESSO ou ERRO
10. Se erro, reagendar processamento (até 5 tentativas)

---

## 🔐 REGRAS DE NEGÓCIO

**RN-UC05-001**: Webhook sem assinatura HMAC é rejeitado com HTTP 401 Unauthorized
**RN-UC05-002**: Webhooks devem ser processados em até 5 minutos (SLA)
**RN-UC05-003**: Máximo 5 tentativas de reprocessamento (exponential backoff)
**RN-UC05-004**: Rate limiting por IP: 100 webhooks/minuto/IP
**RN-UC05-005**: Payload máximo: 10 MB

---

## 📤 ENDPOINT API

```http
POST /api/integration/webhook/{token}
X-Signature: sha256=abc123...
Content-Type: application/json

{
  "event": "user.created",
  "data": {
    "userId": 123,
    "email": "novo@example.com"
  }
}
```

### Response (202 Accepted)

```json
{
  "webhookId": "def-456",
  "message": "Webhook recebido e enfileirado para processamento",
  "estimativaProcessamento": "30 segundos"
}
```

### Response (401 Unauthorized)

```json
{
  "error": "Assinatura HMAC inválida"
}
```

---

# UC06 - Executar Ações Diretas em Notificação

**RF**: RF-021 - Notificações e Alertas
**Complexidade**: Alta
**Estimativa**: 6h Backend + 7h Frontend

---

## 📋 Objetivo

Permitir ações rápidas diretamente na notificação (aprovar, rejeitar, visualizar) sem navegar

---

## 📝 Fluxo Principal

1. Usuário recebe notificação: "Solicitação #123 aguarda sua aprovação"
2. Notificação exibe botões inline:
   - [✅ Aprovar] [❌ Rejeitar] [👁️ Visualizar]
3. **Ação 1: Aprovar**:
   - Usuário clica "Aprovar"
   - Sistema abre modal rápido: "Comentário (opcional): [____]"
   - Confirma → Executa `PUT /api/aprovacoes/123/aprovar`
   - Marca notificação como lida automaticamente
   - Feedback: "Solicitação #123 aprovada com sucesso"
4. **Ação 2: Rejeitar**:
   - Sistema exige justificativa: "Motivo*: [____]"
   - Confirma → Executa `PUT /api/aprovacoes/123/rejeitar`
   - Notificação marcada como lida
5. **Ação 3: Visualizar**:
   - Navega para tela de detalhes (`/aprovacoes/123`)
   - Marca como lida ao abrir

---

## ✅ Validações

Não há validações específicas além das ações executadas

---

## 📐 Regras de Negócio

- **RN-UC06-001**: Ações devem ser idempotentes (não duplicar ao clicar 2x)
- **RN-UC06-002**: Ações executadas marcam notificação como lida automaticamente
- **RN-UC06-003**: Links de ação relativos (`/aprovacoes/123`), não absolutos
- **RN-UC06-004**: Ações com `Fl_Requer_Confirmacao = 1` exigem modal de confirmação

---

## 🎨 Interface UI

**Tipos de Ação:**

| Tipo | Link Ação | Método HTTP | Comportamento |
|------|-----------|-------------|---------------|
| **Visualizar** | `/contratos/456` | GET (navegação) | Abre tela de detalhes |
| **Aprovar** | `/aprovacoes/123/aprovar` | PUT | Executa ação, modal opcional |
| **Rejeitar** | `/aprovacoes/123/rejeitar` | PUT | Executa ação, justificativa obrigatória |
| **Download** | `/documentos/789/download` | GET (arquivo) | Baixa arquivo, marca lida |

**Notificação com Ações:**

```
┌─────────────────────────────────────────────────────────┐
│ 📋 Solicitação #123 aguarda aprovação                   │
│ João solicitou compra de Notebook Dell Inspiron 15      │
│ Valor: R$ 4.500,00 | Centro de Custo: TI                │
│                                                          │
│      [✅ Aprovar] [❌ Rejeitar] [👁️ Visualizar]          │
└─────────────────────────────────────────────────────────┘
```

**Modal de Rejeição:**

```
┌──────────────────────────────────────────┐
│ Rejeitar Solicitação #123           [x] │
├──────────────────────────────────────────┤
│ Motivo da rejeição*:                     │
│ ┌──────────────────────────────────────┐ │
│ │Fora do budget aprovado para Q1.      │ │
│ │Aguardar próximo trimestre.           │ │
│ └──────────────────────────────────────┘ │
│                                          │
│      [Cancelar] [Confirmar Rejeição]    │
└──────────────────────────────────────────┘
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 11 casos de uso |

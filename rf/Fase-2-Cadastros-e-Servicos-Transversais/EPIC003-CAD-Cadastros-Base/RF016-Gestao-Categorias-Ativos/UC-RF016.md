# Casos de Uso - RF016

**RF:** RF016 — Gestão de Categorias de Ativos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD - Cadastros Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**RF Relacionado:** [RF016 - Gestao-Categorias-Ativos](./RF016.md)

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Categorias | Caso de uso |
| UC00 | Listar Integrações | Caso de uso |
| UC01 | UC01 - Criar Categoria | Caso de uso |
| UC01 | Criar Nova Integração | Caso de uso |
| UC02 | UC02 - Visualizar Categoria | Caso de uso |
| UC03 | UC03 - Editar Categoria | Caso de uso |
| UC04 | UC04 - Inativar Categoria | Caso de uso |

---

# UC00 - Listar Categorias

**RF:** RF-090 - Gestão de Categorias de Ativos
**Versão:** 1.0

## Descrição
Permitir listagem, filtro e visualização de categorias em estrutura hierárquica (árvore).

## Fluxo Principal
1. Usuário acessa tela de Categorias
2. Sistema exibe árvore hierárquica de categorias
3. Sistema permite expandir/colapsar níveis
4. Sistema exibe filtros: Nome, Tipo, Ativo/Inativo

## Regras de Negócio
**RN-UC00-001:** Multi-tenant - apenas categorias do conglomerado
**RN-UC00-002:** Exibir até 10 níveis de hierarquia (RN-CAD-012-01)

## Rastreabilidade
- **RF:** [RF-090-Gestao-Categorias-Ativos.md](../RF-090-Gestao-Categorias-Ativos.md)

---

# UC00: Listar Integrações

**Última Atualização**: 05/11/2025
**Status**: ✅ Documentado

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Administrador do Sistema
**Pré-condições**:
- Usuário autenticado
- Possui permissão `SYS.INTEGRACOES.READ`

**Pós-condições**:
- Lista de integrações exibida com filtros aplicados
- Estado de cada integração visível (ativa, inativa, erro)

---

## 🎯 OBJETIVO

Permitir que administradores visualizem todas as integrações configuradas no sistema, com informações de status, última execução e health check em tempo real.

---

## 📝 FLUXO PRINCIPAL

1. Usuário acessa o menu "Sistema > Integrações"
2. Sistema carrega lista de integrações com paginação (50 por página)
3. Para cada integração, sistema exibe:
   - Nome e código
   - Tipo (REST, SOAP, etc.)
   - Status (ativo/inativo)
   - Estado do circuit breaker (fechado/aberto/meio-aberto)
   - Última execução (data, status)
   - Taxa de sucesso (últimas 24h)
   - Badge de health status (online/offline/erro)
4. Usuário pode aplicar filtros e ordenação
5. Usuário pode clicar em uma integração para ver detalhes (UC02)

---

## 🔀 FLUXOS ALTERNATIVOS

### FA01: Filtrar Integrações

1. Usuário preenche campos de filtro:
   - Nome/código (busca parcial)
   - Tipo de integração (dropdown)
   - Status (ativo/inativo)
   - Estado circuit breaker
   - Status última execução
2. Sistema aplica filtros e recarrega lista
3. Sistema exibe contador de resultados

### FA02: Ordenar Lista

1. Usuário clica em cabeçalho de coluna
2. Sistema reordena lista (crescente/decrescente)
3. Opções de ordenação:
   - Nome
   - Código
   - Tipo
   - Última execução
   - Taxa de sucesso

### FA03: Exportar Lista

1. Usuário clica em "Exportar"
2. Sistema gera arquivo Excel/CSV com:
   - Todas as integrações (ignorando paginação)
   - Filtros aplicados mantidos
   - Colunas configuráveis
3. Download automático do arquivo

---

## ⚠️ FLUXOS DE EXCEÇÃO

### FE01: Sem Permissão

1. Usuário não possui permissão `SYS.INTEGRACOES.READ`
2. Sistema redireciona para tela de "Acesso Negado"
3. Sistema registra tentativa de acesso em audit log

### FE02: Erro ao Carregar

1. Erro ao consultar banco de dados
2. Sistema exibe mensagem: "Erro ao carregar integrações. Tente novamente."
3. Sistema loga erro com stack trace

---

## 🖼️ INTERFACE

### Tela: Lista de Integrações

**Componentes**:

#### Barra de Filtros

```
┌────────────────────────────────────────────────────────────┐
│ Buscar: [____________________]  Tipo: [Todos ▼]            │
│ Status: [Todos ▼]  Circuit Breaker: [Todos ▼]              │
│ [Limpar Filtros]  [Aplicar]                    [Exportar] │
└────────────────────────────────────────────────────────────┘
```

#### Tabela de Integrações

| Nome | Código | Tipo | Status | Circuit | Última Exec. | Taxa Sucesso | Ações |
|------|--------|------|--------|---------|--------------|--------------|-------|
| SAP ERP | SAP-001 | REST_API | ✅ Ativo | 🟢 Fechado | 05/11 14:30 ✅ | 98.5% | 👁️ ✏️ ▶️ |
| Vivo Telecom | VIVO-001 | REST_API | ✅ Ativo | 🟡 Meio-Aberto | 05/11 14:25 ⚠️ | 75.2% | 👁️ ✏️ ▶️ |
| Cisco PBX | CISCO-001 | SOAP | ❌ Inativo | 🔴 Aberto | 04/11 22:15 ❌ | 45.0% | 👁️ ✏️ |

**Legenda dos Ícones**:
- 👁️ Visualizar detalhes
- ✏️ Editar configuração
- ▶️ Executar manualmente
- 🗑️ Desativar

#### Paginação

```
┌────────────────────────────────────────────────────────────┐
│ Mostrando 1-50 de 127 integrações                          │
│ [◀️ Anterior]  [1] [2] [3] ... [6]  [Próximo ▶️]            │
│ Itens por página: [50 ▼]                                   │
└────────────────────────────────────────────────────────────┘
```

### Badges de Status

- **🟢 Online**: Última execução com sucesso < 1 hora atrás
- **🟡 Alerta**: Taxa de sucesso < 80% nas últimas 24h
- **🔴 Offline**: Circuit breaker aberto ou última execução falhou
- **⚪ Inativo**: Integração desativada manualmente

---

## 🔐 REGRAS DE NEGÓCIO

### RN-UC00-001: Paginação Obrigatória

- Lista DEVE ser paginada (50 itens por página)
- Usuário pode alterar para 25, 50, 100 itens
- Paginação server-side (não carregar todos os registros)

### RN-UC00-002: Filtros Persistentes

- Filtros aplicados devem ser salvos em sessão
- Ao retornar para tela, manter filtros anteriores
- Botão "Limpar Filtros" reseta para padrão

### RN-UC00-003: Health Check Visual

- Badge de status atualizado a cada 30 segundos (polling)
- Ícone de loading durante atualização
- Tooltip com detalhes ao passar mouse

### RN-UC00-004: Taxa de Sucesso

- Calculada sobre últimas 100 execuções OU últimas 24h
- Fórmula: `(execuções sucesso / total execuções) * 100`
- Exibir "N/A" se menos de 5 execuções

### RN-UC00-005: Circuit Breaker Visual

- 🟢 Fechado: Funcionamento normal
- 🟡 Meio-Aberto: Testando recuperação
- 🔴 Aberto: Falhas consecutivas, bloqueado

---

## 🎨 VALIDAÇÕES

### Front-end

- ✅ Campo de busca aceita no mínimo 3 caracteres
- ✅ Filtro de tipo exibe apenas tipos existentes
- ✅ Filtros múltiplos aplicados com AND lógico

### Back-end

- ✅ Validar permissão `SYS.INTEGRACOES.READ`
- ✅ Validar isolamento multi-tenant (filtrar por ConglomeradoId)
- ✅ Sanitizar entrada de busca (evitar SQL Injection)
- ✅ Limitar paginação a máximo 100 itens por página

---

## 📤 ENDPOINT API

### Request

```http
GET /api/integration?pageNumber=1&pageSize=50&search=SAP&tipo=REST_API&status=ATIVO
Authorization: Bearer {token}
```

**Query Parameters**:
- `pageNumber` (int, default: 1)
- `pageSize` (int, default: 50, max: 100)
- `search` (string, opcional): Busca parcial em nome/código
- `tipo` (enum, opcional): Filtro por tipo de integração
- `status` (bool, opcional): true=ativo, false=inativo
- `circuitBreakerState` (enum, opcional): CLOSED, OPEN, HALF_OPEN

### Response (200 OK)

```json
{
  "items": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "codigo": "SAP-001",
      "nome": "SAP ERP Integration",
      "tipo": "REST_API",
      "baseUrl": "https://sap.empresa.com/api",
      "flAtivo": true,
      "circuitBreakerState": "CLOSED",
      "ultimaExecucao": {
        "dataHora": "2025-11-05T14:30:00Z",
        "status": "SUCESSO",
        "duracaoMs": 234
      },
      "estatisticas": {
        "taxaSucesso": 98.5,
        "totalExecucoes24h": 145,
        "totalSucesso24h": 143,
        "totalErro24h": 2
      },
      "healthStatus": "ONLINE"
    }
  ],
  "pageNumber": 1,
  "pageSize": 50,
  "totalCount": 127,
  "totalPages": 3,
  "hasPreviousPage": false,
  "hasNextPage": true
}
```

---

## ✅ CRITÉRIOS DE ACEITE

- [ ] Lista carrega em menos de 2 segundos
- [ ] Filtros aplicados corretamente
- [ ] Paginação funciona corretamente
- [ ] Badges de status atualizados em tempo real
- [ ] Taxa de sucesso calculada corretamente
- [ ] Circuit breaker estado visível
- [ ] Exportação gera arquivo Excel válido
- [ ] Permissões validadas no backend
- [ ] Multi-tenancy isolado (usuário só vê integrações do seu conglomerado)
- [ ] Responsivo em mobile

---

**Documento atualizado em**: 05/11/2025
**Responsável**: Equipe IControlIT v2

---

# UC01 - Criar Categoria

**RF:** RF-090
**Versão:** 1.0

## Descrição
Cadastrar nova categoria com possibilidade de definir categoria pai, atributos customizados e taxa de depreciação.

## Fluxo Principal
1. Usuário clica em "Nova Categoria"
2. Sistema exibe formulário:
   - Nome
   - Tipo (Ativo, Serviço, Chamado, Contrato)
   - Categoria Pai (dropdown hierárquico)
   - Taxa de Depreciação (%)
   - Ícone/Cor
3. Usuário preenche e salva
4. Sistema valida hierarquia (sem loops)
5. Sistema salva categoria

## Regras de Negócio
**RN-UC01-001:** Validar loops na hierarquia (RN-CAD-012-02)
**RN-UC01-002:** Taxa depreciação 0-100% (RN-CAD-012-03)
**RN-UC01-003:** Máximo 10 níveis hierarquia

## Rastreabilidade
- **RF:** [RF-090-Gestao-Categorias-Ativos.md](../RF-090-Gestao-Categorias-Ativos.md)

---

# UC01: Criar Nova Integração

**Última Atualização**: 05/11/2025
**Status**: ✅ Documentado

---

## 📋 INFORMAÇÕES BÁSICAS

**Ator Principal**: Administrador do Sistema
**Pré-condições**:
- Usuário autenticado
- Possui permissão `SYS.INTEGRACOES.CREATE`

**Pós-condições**:
- Nova integração criada e ativa
- Credenciais armazenadas criptografadas
- Circuit breaker inicializado (estado CLOSED)
- Registro de auditoria criado

---

## 🎯 OBJETIVO

Permitir que administradores configurem novas integrações com sistemas externos, definindo URLs, autenticação, políticas de retry e circuit breaker.

---

## 📝 FLUXO PRINCIPAL

1. Usuário clica em "Nova Integração" na lista
2. Sistema exibe formulário wizard em 4 etapas:
   - **Etapa 1**: Informações Básicas
   - **Etapa 2**: Autenticação e Credenciais
   - **Etapa 3**: Políticas de Resiliência
   - **Etapa 4**: Configurações Avançadas
3. Usuário preenche **Etapa 1 - Informações Básicas**:
   - Código único (gerado automaticamente, editável)
   - Nome descritivo
   - Descrição
   - Tipo de integração (dropdown: REST, SOAP, GraphQL, etc.)
   - URL base da API
   - Conglomerado (dropdown, opcional - null = global)
4. Usuário clica em "Próximo"
5. Sistema exibe **Etapa 2 - Autenticação**:
   - Tipo de autenticação (dropdown: NONE, BASIC, BEARER, API_KEY, OAUTH2, MTLS)
   - Formulário dinâmico baseado no tipo escolhido
   - Checkbox "Testar Conexão" (executa health check)
6. Usuário preenche credenciais e clica "Próximo"
7. Sistema exibe **Etapa 3 - Políticas de Resiliência**:
   - Timeout global (segundos)
   - Número de tentativas de retry
   - Backoff exponencial (intervalo inicial)
   - Circuit breaker threshold (falhas para abrir)
   - Circuit breaker timeout (tempo aberto)
   - Rate limiting (requisições por período)
8. Usuário ajusta políticas e clica "Próximo"
9. Sistema exibe **Etapa 4 - Configurações Avançadas**:
   - Headers HTTP padrão (editor JSON)
   - Habilitar logs de request/response (checkboxes)
   - Webhook secret (para webhooks incoming)
   - Webhook callback URL (para webhooks outgoing)
   - Metadados customizados (editor JSON)
   - Status inicial (ativo/inativo)
10. Usuário revisa configurações e clica "Criar Integração"
11. Sistema valida todos os campos
12. Sistema criptografa credenciais com AES-256
13. Sistema salva integração no banco
14. Sistema inicializa circuit breaker (estado CLOSED)
15. Sistema registra criação no histórico de auditoria
16. Sistema exibe mensagem: "Integração criada com sucesso!"
17. Sistema redireciona para detalhes da integração (UC02)

---

## 🔀 FLUXOS ALTERNATIVOS

### FA01: Testar Conexão Durante Configuração

1. Na Etapa 2, usuário marca "Testar Conexão"
2. Sistema faz requisição de health check para a URL base
3. Se sucesso:
   - Badge verde "Conexão OK"
   - Permite avançar para próxima etapa
4. Se falha:
   - Badge vermelho "Falha na Conexão"
   - Exibe mensagem de erro detalhada
   - Permite avançar mesmo assim (warning apenas)

### FA02: Importar Configuração de Arquivo

1. Usuário clica em "Importar Configuração"
2. Sistema abre diálogo de upload
3. Usuário seleciona arquivo JSON
4. Sistema valida formato do arquivo
5. Sistema preenche formulário com dados importados
6. Usuário revisa e ajusta se necessário
7. Fluxo continua normalmente

### FA03: Duplicar Integração Existente

1. Usuário seleciona "Duplicar" em integração existente
2. Sistema copia configuração (exceto credenciais)
3. Sistema gera novo código (original + "-COPY")
4. Sistema abre formulário pré-preenchido
5. Usuário ajusta configurações
6. Fluxo continua normalmente

---

## ⚠️ FLUXOS DE EXCEÇÃO

### FE01: Código Duplicado

1. Código já existe no banco de dados
2. Sistema exibe erro no campo: "Código já em uso"
3. Sistema sugere código alternativo (+1, +2, etc.)
4. Usuário corrige e tenta novamente

### FE02: URL Base Inválida

1. URL não segue formato válido
2. Sistema exibe erro: "URL inválida. Use formato: https://api.example.com"
3. Usuário corrige e tenta novamente

### FE03: Credenciais Inválidas no Teste

1. Teste de conexão falha por erro de autenticação (401)
2. Sistema exibe: "Credenciais inválidas. Verifique usuário/senha."
3. Usuário corrige credenciais
4. Permite salvar mesmo assim (com warning)

### FE04: Erro ao Salvar

1. Erro ao salvar no banco de dados
2. Sistema exibe: "Erro ao salvar integração. Tente novamente."
3. Sistema mantém dados preenchidos (não perde informações)
4. Sistema loga erro com stack trace
5. Administrador pode tentar novamente

---

## 🖼️ INTERFACE

### Formulário Wizard - Etapa 1: Informações Básicas

```
┌─────────────────────────────────────────────────────────────┐
│ Nova Integração                                    [1][2][3][4] │
│─────────────────────────────────────────────────────────────│
│ Informações Básicas                                         │
│                                                              │
│ Código *                                                     │
│ [SAP-001_________________] 🔄 Gerar Automático              │
│                                                              │
│ Nome *                                                       │
│ [SAP ERP Integration_____________________]                  │
│                                                              │
│ Descrição                                                    │
│ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]           │
│ [━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━]           │
│                                                              │
│ Tipo de Integração *                                         │
│ [REST API ▼]                                                │
│ 🔹 REST API - APIs RESTful padrão                           │
│                                                              │
│ URL Base *                                                   │
│ [https://sap.empresa.com/api______________] 🧪 Testar       │
│                                                              │
│ Conglomerado                                                 │
│ [Global (Todas as empresas) ▼]                              │
│                                                              │
│ [Cancelar]                         [Próximo: Autenticação →]│
└─────────────────────────────────────────────────────────────┘
```

### Formulário Wizard - Etapa 2: Autenticação (Exemplo: BASIC)

```
┌─────────────────────────────────────────────────────────────┐
│ Nova Integração                                    [1][2][3][4] │
│─────────────────────────────────────────────────────────────│
│ Autenticação e Credenciais                                  │
│                                                              │
│ Tipo de Autenticação *                                       │
│ [Basic Authentication ▼]                                    │
│                                                              │
│ Usuário *                                                    │
│ [api_user@example.com_______________]                       │
│                                                              │
│ Senha *                                                      │
│ [••••••••••••••••] 👁️ Mostrar                              │
│                                                              │
│ ☑ Testar conexão ao avançar                                │
│                                                              │
│ 💡 Dica: As credenciais serão criptografadas com AES-256    │
│    e armazenadas de forma segura no Azure Key Vault.        │
│                                                              │
│ [← Voltar]                      [Próximo: Políticas →]      │
└─────────────────────────────────────────────────────────────┘
```

### Formulário Wizard - Etapa 3: Políticas de Resiliência

```
┌─────────────────────────────────────────────────────────────┐
│ Nova Integração                                    [1][2][3][4] │
│─────────────────────────────────────────────────────────────│
│ Políticas de Resiliência                                    │
│                                                              │
│ ⏱️ Timeout & Retry                                          │
│                                                              │
│ Timeout Global (segundos) *                                  │
│ [──🔘──────] 30s                                            │
│  5s              60s                                         │
│                                                              │
│ Tentativas de Retry *                                        │
│ [──🔘──] 3                                                  │
│  0       5                                                   │
│                                                              │
│ Backoff Inicial (segundos) *                                 │
│ [──🔘───] 5s                                                │
│  1s      10s                                                 │
│                                                              │
│ 🔌 Circuit Breaker                                          │
│                                                              │
│ Falhas para Abrir *                                          │
│ [──🔘───] 5                                                 │
│  2        10                                                 │
│                                                              │
│ Tempo Circuit Aberto (segundos) *                            │
│ [────🔘──] 60s                                              │
│  30s      120s                                               │
│                                                              │
│ 🚦 Rate Limiting (Opcional)                                 │
│                                                              │
│ Requisições por Período                                     │
│ [100___] requisições a cada [60___] segundos                │
│                                                              │
│ [← Voltar]                      [Próximo: Avançado →]       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 REGRAS DE NEGÓCIO

### RN-UC01-001: Código Único Obrigatório

- Código deve ser único no sistema
- Formato: Letras maiúsculas, números e hífen
- Regex: `^[A-Z0-9-]{3,50}$`
- Sugestão automática: `{TIPO}-{SEQUENCIAL}` (ex: REST-001)

### RN-UC01-002: Criptografia de Credenciais

- Todas as credenciais DEVEM ser criptografadas com AES-256
- Chave de criptografia armazenada em Azure Key Vault (produção)
- Nunca exibir senha em plain text após salvar
- Ao editar, campo senha vem mascarado (não exibe valor original)

### RN-UC01-003: Validação de URL

- URL base DEVE começar com `https://` (http:// apenas em dev)
- URL DEVE ser válida e acessível (teste de conexão recomendado)
- Portas customizadas permitidas (ex: `https://api.com:8443`)

### RN-UC01-004: Valores Padrão de Políticas

- Se usuário não preencher, usar:
  - Timeout: 30 segundos
  - Retry tentativas: 3
  - Backoff: 5 segundos
  - Circuit threshold: 5 falhas
  - Circuit timeout: 60 segundos
  - Rate limit: desabilitado (null)

### RN-UC01-005: Multi-Tenancy

- Se `ConglomeradoId` = NULL → Integração global (visível para todos)
- Se `ConglomeradoId` = {guid} → Integração específica de um conglomerado
- Usuário só pode criar integração para seu conglomerado
- Super-admin pode criar integrações globais

---

## 🎨 VALIDAÇÕES

### Front-end

- ✅ Código: obrigatório, 3-50 caracteres, alfanumérico + hífen
- ✅ Nome: obrigatório, máximo 200 caracteres
- ✅ URL: obrigatório, formato válido, HTTPS
- ✅ Tipo: obrigatório, uma das opções do enum
- ✅ Timeout: número, 5-300 segundos
- ✅ Retry: número, 0-10 tentativas
- ✅ Circuit threshold: número, 2-20 falhas

### Back-end

- ✅ Validar permissão `SYS.INTEGRACOES.CREATE`
- ✅ Validar isolamento multi-tenant (ConglomeradoId)
- ✅ Verificar unicidade do código
- ✅ Criptografar credenciais antes de salvar
- ✅ Validar formato de credenciais JSON
- ✅ Validar rate limit (se definido, ambos os campos obrigatórios)
- ✅ Sanitizar URL (remover espaços, trailing slashes)

---

## 📤 ENDPOINT API

### Request

```http
POST /api/integration
Authorization: Bearer {token}
Content-Type: application/json

{
  "codigo": "SAP-001",
  "nome": "SAP ERP Integration",
  "descricao": "Integração com SAP para importação de usuários e estrutura",
  "tipo": "REST_API",
  "baseUrl": "https://sap.empresa.com/api",
  "conglomeradoId": null,
  "autenticacaoTipo": "BASIC",
  "credenciais": {
    "username": "api_user@example.com",
    "password": "senhaSecreta123"
  },
  "headersPadrao": {
    "Accept": "application/json",
    "X-Custom-Header": "valor"
  },
  "timeoutSegundos": 30,
  "retryTentativas": 3,
  "retryBackoffSegundos": 5,
  "circuitBreakerThreshold": 5,
  "circuitBreakerTimeoutSegundos": 60,
  "rateLimitRequisicoes": 100,
  "rateLimitPeriodoSegundos": 60,
  "flAtivo": true,
  "flLogRequest": false,
  "flLogResponse": false,
  "webhookSecret": null,
  "webhookUrlCallback": null,
  "metadados": {}
}
```

### Response (201 Created)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "codigo": "SAP-001",
  "nome": "SAP ERP Integration",
  "message": "Integração criada com sucesso!",
  "webhookUrl": null,
  "circuitBreakerState": "CLOSED"
}
```

### Response (400 Bad Request) - Código Duplicado

```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title": "Validação falhou",
  "status": 400,
  "errors": {
    "Codigo": [
      "O código 'SAP-001' já está em uso. Sugestões: SAP-002, SAP-003"
    ]
  }
}
```

---

## ✅ CRITÉRIOS DE ACEITE

- [ ] Wizard com 4 etapas navegável
- [ ] Código gerado automaticamente se não preenchido
- [ ] Validações em tempo real em cada campo
- [ ] Teste de conexão funciona (health check)
- [ ] Credenciais criptografadas corretamente
- [ ] Circuit breaker inicializado (CLOSED)
- [ ] Registro de auditoria criado
- [ ] Mensagem de sucesso exibida
- [ ] Redirecionamento para detalhes após criar
- [ ] Importação de configuração JSON funciona
- [ ] Duplicação de integração existente funciona
- [ ] Permissões validadas no backend
- [ ] Multi-tenancy isolado

---

**Documento atualizado em**: 05/11/2025
**Responsável**: Equipe IControlIT v2

---

# UC02 - Visualizar Categoria

**RF:** RF-090
**Versão:** 1.0

## Descrição
Visualizar detalhes completos de categoria, incluindo atributos herdados e ativos associados.

## Fluxo Principal
1. Usuário clica em categoria na árvore
2. Sistema exibe detalhes, hierarquia, atributos customizados

## Rastreabilidade
- **RF:** [RF-090-Gestao-Categorias-Ativos.md](../RF-090-Gestao-Categorias-Ativos.md)

---

# UC03 - Editar Categoria

**RF:** RF-090
**Versão:** 1.0

## Descrição
Permitir edição de dados da categoria, incluindo mover para outra categoria pai.

## Fluxo Principal
1. Usuário clica em "Editar"
2. Sistema exibe formulário preenchido
3. Usuário altera campos
4. Sistema valida e salva

## Regras de Negócio
**RN-UC03-001:** Não pode mover para dentro de descendentes (loop)
**RN-UC03-002:** Categorias de sistema não editáveis (RN-CAD-012-07)

## Rastreabilidade
- **RF:** [RF-090-Gestao-Categorias-Ativos.md](../RF-090-Gestao-Categorias-Ativos.md)

---

# UC04 - Inativar Categoria

**RF:** RF-090
**Versão:** 1.0

## Descrição
Inativar categoria com opção de inativação em cascata de subcategorias.

## Fluxo Principal
1. Usuário clica em "Inativar"
2. Sistema pergunta se deseja inativar subcategorias
3. Usuário confirma
4. Sistema inativa (soft delete)

## Regras de Negócio
**RN-UC04-001:** Inativação cascata opcional (RN-CAD-012-08)
**RN-UC04-002:** Categorias sistema não podem ser inativadas

## Rastreabilidade
- **RF:** [RF-090-Gestao-Categorias-Ativos.md](../RF-090-Gestao-Categorias-Ativos.md)

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 7 casos de uso |

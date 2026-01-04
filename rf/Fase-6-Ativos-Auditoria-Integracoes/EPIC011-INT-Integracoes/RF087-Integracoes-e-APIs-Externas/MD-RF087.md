# MD-NPV-002 - Modelo de Dados - Gestão de Integrações

**Versão:** 1.0
**Data:** 2025-01-19
**RF Relacionado:** RF-NPV-002

---

## 1. Diagrama Entidade-Relacionamento

```
+------------------+       +----------------------+       +----------------------+
|    Integracao    |       | IntegracaoEndpoint   |       | IntegracaoExecucao   |
+------------------+       +----------------------+       +----------------------+
| Id (PK)          |<──┐   | Id (PK)              |       | Id (PK)              |
| EmpresaId (FK)   |   │   | IntegracaoId (FK)    |───┐   | IntegracaoId (FK)    |
| Codigo           |   │   | Path                 |   │   | EndpointId (FK)      |
| Nome             |   │   | Metodo               |   │   | DataExecucao         |
| Descricao        |   │   | Descricao            |   │   | DuracaoMs            |
| Tipo             |   │   | HeadersCustomizados  |   │   | HttpStatusCode       |
| BaseUrl          |   └───| Ativo                |   │   | Sucesso              |
| AutenticacaoTipo |       +----------------------+   │   | ErrorMessage         |
| CredenciaisJson  |                                 │   | RequestBody          |
| TimeoutSegundos  |<────────────────────────────────┘   | ResponseBody         |
| ...              |                                     +----------------------+
+------------------+
```

---

## 2. Entidades

### 2.1 Integracao

Entidade principal que representa uma integração com sistema externo.

| Campo | Tipo | Tamanho | Obrigatório | Descrição |
|-------|------|---------|-------------|-----------|
| Id | GUID | - | Sim | Identificador único |
| EmpresaId | GUID | - | Sim | FK para Empresa (multi-tenancy) |
| Codigo | VARCHAR | 50 | Sim | Código único da integração |
| Nome | VARCHAR | 200 | Sim | Nome descritivo |
| Descricao | VARCHAR | 1000 | Não | Descrição detalhada |
| Tipo | VARCHAR | 20 | Sim | Tipo de integração |
| BaseUrl | VARCHAR | 500 | Sim | URL base do serviço |
| AutenticacaoTipo | VARCHAR | 20 | Sim | Método de autenticação |
| CredenciaisJson | TEXT | - | Não | Credenciais em JSON (criptografado) |
| TimeoutSegundos | INT | - | Sim | Timeout de conexão (default: 30) |
| RetryTentativas | INT | - | Sim | Número de retentativas (default: 3) |
| RetryDelayMs | INT | - | Sim | Delay entre tentativas (default: 1000) |
| CircuitBreakerThreshold | INT | - | Sim | Falhas para abrir circuito (default: 5) |
| CircuitBreakerDuracaoSegundos | INT | - | Sim | Tempo com circuito aberto (default: 60) |
| RateLimitRequisicoes | INT | - | Não | Limite de requisições |
| RateLimitPeriodoSegundos | INT | - | Não | Período do rate limit |
| AceitarCertificadoInvalido | BIT | - | Sim | Aceitar certificados inválidos (default: false) |
| HeadersCustomizados | TEXT | - | Não | Headers adicionais em JSON |
| HabilitarWebhook | BIT | - | Sim | Habilitar webhooks (default: false) |
| WebhookUrl | VARCHAR | 500 | Não | URL do webhook |
| WebhookSecret | VARCHAR | 200 | Não | Secret para validação HMAC |
| HabilitarFila | BIT | - | Sim | Habilitar fila (default: false) |
| FilaMaxRetentativas | INT | - | Não | Máximo retentativas na fila |
| Tags | VARCHAR | 500 | Não | Tags para categorização |
| Ativo | BIT | - | Sim | Status ativo/inativo (default: true) |
| Created | DATETIME | - | Sim | Data de criação |
| CreatedBy | VARCHAR | 100 | Sim | Usuário que criou |
| LastModified | DATETIME | - | Não | Data da última modificação |
| LastModifiedBy | VARCHAR | 100 | Não | Usuário que modificou |

**Constraints:**
- PK: Id
- FK: EmpresaId -> Empresa.Id
- UNIQUE: (EmpresaId, Codigo)

---

### 2.2 IntegracaoEndpoint

Endpoints configurados para cada integração.

| Campo | Tipo | Tamanho | Obrigatório | Descrição |
|-------|------|---------|-------------|-----------|
| Id | GUID | - | Sim | Identificador único |
| IntegracaoId | GUID | - | Sim | FK para Integracao |
| Path | VARCHAR | 500 | Sim | Caminho relativo do endpoint |
| Metodo | VARCHAR | 10 | Sim | Método HTTP (GET, POST, etc.) |
| Descricao | VARCHAR | 500 | Não | Descrição do endpoint |
| HeadersCustomizados | TEXT | - | Não | Headers específicos em JSON |
| Ativo | BIT | - | Sim | Status ativo/inativo |

**Constraints:**
- PK: Id
- FK: IntegracaoId -> Integracao.Id (CASCADE DELETE)

---

### 2.3 IntegracaoExecucao

Log de execuções para auditoria e estatísticas.

| Campo | Tipo | Tamanho | Obrigatório | Descrição |
|-------|------|---------|-------------|-----------|
| Id | GUID | - | Sim | Identificador único |
| IntegracaoId | GUID | - | Sim | FK para Integracao |
| EndpointId | GUID | - | Não | FK para IntegracaoEndpoint |
| DataExecucao | DATETIME | - | Sim | Data/hora da execução |
| DuracaoMs | INT | - | Sim | Duração em milissegundos |
| HttpStatusCode | INT | - | Não | Código HTTP retornado |
| Sucesso | BIT | - | Sim | Execução bem sucedida |
| ErrorMessage | TEXT | - | Não | Mensagem de erro |
| RequestBody | TEXT | - | Não | Corpo da requisição |
| ResponseBody | TEXT | - | Não | Corpo da resposta |
| RetryTentativa | INT | - | Sim | Número da tentativa |

**Constraints:**
- PK: Id
- FK: IntegracaoId -> Integracao.Id
- FK: EndpointId -> IntegracaoEndpoint.Id

---

## 3. Enumerações

### 3.1 TipoIntegracao

| Valor | Descrição |
|-------|-----------|
| REST_API | API REST padrão |
| SOAP | Web Service SOAP |
| GRAPHQL | API GraphQL |
| WEBHOOK_IN | Webhook recebido |
| WEBHOOK_OUT | Webhook enviado |
| FTP | Transferência FTP |
| SFTP | Transferência SFTP segura |
| LDAP | Diretório LDAP |

### 3.2 TipoAutenticacao

| Valor | Descrição |
|-------|-----------|
| NONE | Sem autenticação |
| BASIC | Basic Auth (usuário/senha) |
| BEARER | Bearer Token |
| API_KEY | Chave de API |
| OAUTH2 | OAuth 2.0 |
| MTLS | Mutual TLS (certificado) |

### 3.3 MetodoHttp

| Valor | Descrição |
|-------|-----------|
| GET | Consulta |
| POST | Criação |
| PUT | Atualização completa |
| PATCH | Atualização parcial |
| DELETE | Exclusão |

### 3.4 CircuitBreakerEstado

| Valor | Descrição |
|-------|-----------|
| CLOSED | Normal - requisições permitidas |
| OPEN | Bloqueado - requisições rejeitadas |
| HALF_OPEN | Testando - permitindo algumas requisições |

---

## 4. DDL (SQLite)

```sql
-- Tabela principal de integrações
CREATE TABLE IF NOT EXISTS Integracao (
    Id TEXT PRIMARY KEY,
    EmpresaId TEXT NOT NULL,
    Codigo TEXT NOT NULL,
    Nome TEXT NOT NULL,
    Descricao TEXT,
    Tipo TEXT NOT NULL,
    BaseUrl TEXT NOT NULL,
    AutenticacaoTipo TEXT NOT NULL,
    CredenciaisJson TEXT,
    TimeoutSegundos INTEGER NOT NULL DEFAULT 30,
    RetryTentativas INTEGER NOT NULL DEFAULT 3,
    RetryDelayMs INTEGER NOT NULL DEFAULT 1000,
    CircuitBreakerThreshold INTEGER NOT NULL DEFAULT 5,
    CircuitBreakerDuracaoSegundos INTEGER NOT NULL DEFAULT 60,
    RateLimitRequisicoes INTEGER,
    RateLimitPeriodoSegundos INTEGER,
    AceitarCertificadoInvalido INTEGER NOT NULL DEFAULT 0,
    HeadersCustomizados TEXT,
    HabilitarWebhook INTEGER NOT NULL DEFAULT 0,
    WebhookUrl TEXT,
    WebhookSecret TEXT,
    HabilitarFila INTEGER NOT NULL DEFAULT 0,
    FilaMaxRetentativas INTEGER,
    Tags TEXT,
    Ativo INTEGER NOT NULL DEFAULT 1,
    Created TEXT NOT NULL,
    CreatedBy TEXT NOT NULL,
    LastModified TEXT,
    LastModifiedBy TEXT,
    FOREIGN KEY (EmpresaId) REFERENCES Empresa(Id),
    UNIQUE (EmpresaId, Codigo)
);

-- Índices
CREATE INDEX IF NOT EXISTS IX_Integracao_EmpresaId ON Integracao(EmpresaId);
CREATE INDEX IF NOT EXISTS IX_Integracao_Ativo ON Integracao(EmpresaId, Ativo);
CREATE INDEX IF NOT EXISTS IX_Integracao_Tipo ON Integracao(EmpresaId, Tipo);

-- Endpoints da integração
CREATE TABLE IF NOT EXISTS IntegracaoEndpoint (
    Id TEXT PRIMARY KEY,
    IntegracaoId TEXT NOT NULL,
    Path TEXT NOT NULL,
    Metodo TEXT NOT NULL,
    Descricao TEXT,
    HeadersCustomizados TEXT,
    Ativo INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (IntegracaoId) REFERENCES Integracao(Id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS IX_IntegracaoEndpoint_IntegracaoId ON IntegracaoEndpoint(IntegracaoId);

-- Log de execuções
CREATE TABLE IF NOT EXISTS IntegracaoExecucao (
    Id TEXT PRIMARY KEY,
    IntegracaoId TEXT NOT NULL,
    EndpointId TEXT,
    DataExecucao TEXT NOT NULL,
    DuracaoMs INTEGER NOT NULL,
    HttpStatusCode INTEGER,
    Sucesso INTEGER NOT NULL,
    ErrorMessage TEXT,
    RequestBody TEXT,
    ResponseBody TEXT,
    RetryTentativa INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (IntegracaoId) REFERENCES Integracao(Id),
    FOREIGN KEY (EndpointId) REFERENCES IntegracaoEndpoint(Id)
);

CREATE INDEX IF NOT EXISTS IX_IntegracaoExecucao_IntegracaoId ON IntegracaoExecucao(IntegracaoId);
CREATE INDEX IF NOT EXISTS IX_IntegracaoExecucao_DataExecucao ON IntegracaoExecucao(DataExecucao);
```

---

## 5. DTOs

### 5.1 IntegracaoDto (Listagem)

```typescript
interface IntegracaoDto {
    id: string;
    codigo: string;
    nome: string;
    descricao?: string;
    tipo: TipoIntegracao;
    baseUrl: string;
    autenticacaoTipo: TipoAutenticacao;
    ativo: boolean;
    habilitarWebhook: boolean;
    habilitarFila: boolean;
    tags?: string;
    circuitBreakerEstado?: string;
    quantidadeExecucoesTotal?: number;
    quantidadeExecucoesSucesso?: number;
    quantidadeExecucoesErro?: number;
    dataUltimaExecucao?: string;
    created: string;
    lastModified?: string;
}
```

### 5.2 IntegracaoDetalheDto (Visualização)

```typescript
interface IntegracaoDetalheDto extends IntegracaoDto {
    timeoutSegundos: number;
    retryTentativas: number;
    retryDelayMs: number;
    circuitBreakerThreshold: number;
    circuitBreakerDuracaoSegundos: number;
    rateLimitRequisicoes?: number;
    rateLimitPeriodoSegundos?: number;
    aceitarCertificadoInvalido: boolean;
    headersCustomizados?: string;
    webhookUrl?: string;
    filaMaxRetentativas?: number;
    endpoints: EndpointDto[];
    createdBy?: string;
    lastModifiedBy?: string;
}
```

### 5.3 CriarIntegracaoRequest

```typescript
interface CriarIntegracaoRequest {
    codigo: string;
    nome: string;
    descricao?: string;
    tipo: TipoIntegracao;
    baseUrl: string;
    autenticacaoTipo: TipoAutenticacao;
    credenciaisJson: string;
    timeoutSegundos?: number;
    retryTentativas?: number;
    retryDelayMs?: number;
    circuitBreakerThreshold?: number;
    circuitBreakerDuracaoSegundos?: number;
    rateLimitRequisicoes?: number;
    rateLimitPeriodoSegundos?: number;
    aceitarCertificadoInvalido?: boolean;
    headersCustomizados?: string;
    habilitarWebhook?: boolean;
    webhookSecret?: string;
    habilitarFila?: boolean;
    filaMaxRetentativas?: number;
    ativo?: boolean;
    tags?: string;
}
```

---

## 6. Relacionamentos

| Entidade Origem | Entidade Destino | Cardinalidade | Descrição |
|-----------------|------------------|---------------|-----------|
| Integracao | Empresa | N:1 | Cada integração pertence a uma empresa |
| Integracao | IntegracaoEndpoint | 1:N | Uma integração pode ter vários endpoints |
| Integracao | IntegracaoExecucao | 1:N | Uma integração pode ter várias execuções |
| IntegracaoEndpoint | IntegracaoExecucao | 1:N | Um endpoint pode ter várias execuções |

---

## Histórico de Versões

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-01-19 | Claude | Modelo de dados inicial |

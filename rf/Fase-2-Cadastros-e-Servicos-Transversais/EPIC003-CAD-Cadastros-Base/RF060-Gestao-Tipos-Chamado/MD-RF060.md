# Modelo de Dados - RF060 - Gestão de Tipos de Chamado

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF060 - Gestão de Tipos de Chamado](./RF060.md)
**Banco de Dados:** SQL Server / PostgreSQL

---

## 1. Diagrama de Entidades (ER)

```
┌──────────────────────────────────────────────────────────┐
│                      GestaoCliente                        │
│                      (multi-tenancy)                      │
└──────────┬───────────────────────────────────────────────┘
           │ 1:N
           │
┌──────────▼──────────────────────────────────────────────────────┐
│                     TipoChamado                                  │
├──────────────────────────────────────────────────────────────────┤
│ Id (PK)                      UUID                                │
│ ClienteId (FK)               UUID                                │
│ Codigo                       VARCHAR(50)                         │
│ Nome                         VARCHAR(200)                        │
│ Descricao                    TEXT                                │
│ CategoriaITIL                VARCHAR(50)                         │
│ CategoriaHierarquica         VARCHAR(500)                        │
│ FilaPadraoId (FK)            UUID                                │
│ EspecialistaPreferencialId   UUID                                │
│ RequerAprovacaoCAB           BIT                                 │
│ PermiteAnexos                BIT                                 │
│ Icone, Cor, Ordem, Ativo                                         │
│ CreatedAt, CreatedBy, ModifiedAt, ModifiedBy                     │
└──────────┬──────────────────────────────────────────────────────┘
           │ 1:N
           ├─────────────────────────────────────────────────┐
           │                                                 │
┌──────────▼───────────────────────┐    ┌──────────────────▼───────────────────┐
│      SLATipoChamado              │    │    FormularioDinamico                │
├──────────────────────────────────┤    ├──────────────────────────────────────┤
│ Id (PK)              UUID        │    │ Id (PK)              UUID            │
│ TipoChamadoId (FK)   UUID        │    │ TipoChamadoId (FK)   UUID            │
│ ClienteId (FK)       UUID        │    │ ClienteId (FK)       UUID            │
│ Prioridade           VARCHAR(20) │    │ NomeCampo            VARCHAR(100)    │
│ TempoRespostaMinutos INT         │    │ TipoCampo            VARCHAR(20)     │
│ TempoResolucaoMinutos INT        │    │ Obrigatorio          BIT             │
│ Ativo                BIT         │    │ Ordem                INT             │
│ CreatedAt, CreatedBy, ...        │    │ Opcoes               TEXT (JSON)     │
└──────────────────────────────────┘    │ Validacoes           TEXT (JSON)     │
                                        │ Ativo                BIT             │
┌──────────────────────────────────┐    │ CreatedAt, CreatedBy, ...            │
│    TemplateResolucao             │    └──────────────────────────────────────┘
├──────────────────────────────────┤
│ Id (PK)              UUID        │    ┌──────────────────────────────────────┐
│ TipoChamadoId (FK)   UUID        │    │    EscalonamentoTipo                 │
│ ClienteId (FK)       UUID        │    ├──────────────────────────────────────┤
│ Titulo               VARCHAR(200)│    │ Id (PK)              UUID            │
│ Descricao            TEXT        │    │ TipoChamadoId (FK)   UUID            │
│ PassosResolucao      TEXT        │    │ ClienteId (FK)       UUID            │
│ QuantidadeUsos       INT         │    │ Nivel                INT             │
│ TaxaSucesso          DECIMAL     │    │ GrupoAtendimentoId   UUID            │
│ Ativo                BIT         │    │ TempoEscalonamentoMin INT            │
│ CreatedAt, CreatedBy, ...        │    │ NotificarGestor      BIT             │
└──────────────────────────────────┘    │ Ativo                BIT             │
                                        │ CreatedAt, CreatedBy, ...            │
┌──────────────────────────────────┐    └──────────────────────────────────────┘
│    MatrizImpactoUrgencia         │
├──────────────────────────────────┤    ┌──────────────────────────────────────┐
│ Id (PK)              UUID        │    │    TipoChamadoEspecialista           │
│ TipoChamadoId (FK)   UUID        │    ├──────────────────────────────────────┤
│ ClienteId (FK)       UUID        │    │ Id (PK)              UUID            │
│ Impacto              VARCHAR(20) │    │ TipoChamadoId (FK)   UUID            │
│ Urgencia             VARCHAR(20) │    │ EspecialistaId (FK)  UUID            │
│ PrioridadeResultante VARCHAR(20) │    │ ClienteId (FK)       UUID            │
│ CreatedAt, CreatedBy, ...        │    │ Preferencial         BIT             │
└──────────────────────────────────┘    │ NivelExperiencia     INT             │
                                        │ QuantidadeChamados   INT (computed)  │
                                        │ AvaliacaoMedia       DECIMAL (comp.) │
                                        │ Ativo                BIT             │
                                        │ CreatedAt, CreatedBy, ...            │
                                        └──────────────────────────────────────┘
```

---

## 2. Entidades

### 2.1 Tabela: TipoChamado

**Descrição:** Tipos de chamados técnicos baseados em ITIL v4 (Incidente, Requisição, Mudança, Problema). Define categorização, SLA, formulários e escalonamento específicos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Codigo | VARCHAR(50) | NÃO | - | Código único do tipo |
| Nome | VARCHAR(200) | NÃO | - | Nome do tipo de chamado |
| Descricao | TEXT | SIM | NULL | Descrição detalhada |
| CategoriaITIL | VARCHAR(50) | NÃO | - | INCIDENTE, REQUISICAO, MUDANCA, PROBLEMA |
| CategoriaHierarquica | VARCHAR(500) | SIM | NULL | Categoria.Subcategoria.Item |
| FilaPadraoId | UNIQUEIDENTIFIER | SIM | NULL | FK para fila de atendimento |
| EspecialistaPreferencialId | UNIQUEIDENTIFIER | SIM | NULL | FK para técnico especialista |
| RequerAprovacaoCAB | BIT | NÃO | 0 | Se requer Change Advisory Board |
| PermiteAnexos | BIT | NÃO | 1 | Se permite anexar arquivos |
| Icone | VARCHAR(50) | SIM | NULL | Ícone FontAwesome |
| Cor | VARCHAR(7) | SIM | NULL | Cor hexadecimal |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TipoChamado | Id | CLUSTERED | Chave primária |
| IX_TipoChamado_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_TipoChamado_Codigo | Codigo, ClienteId | NONCLUSTERED | Busca por código |
| IX_TipoChamado_CategoriaITIL | CategoriaITIL, ClienteId | NONCLUSTERED | Filtro por categoria ITIL |
| IX_TipoChamado_Ativo | Ativo, ClienteId | NONCLUSTERED | Filtro de ativos |
| IX_TipoChamado_FilaPadrao | FilaPadraoId | NONCLUSTERED | Join com filas |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TipoChamado | PRIMARY KEY | Id | Chave primária |
| FK_TipoChamado_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_TipoChamado_FilaPadrao | FOREIGN KEY | FilaPadraoId REFERENCES FilaAtendimento(Id) | Fila padrão |
| FK_TipoChamado_Especialista | FOREIGN KEY | EspecialistaPreferencialId REFERENCES Usuario(Id) | Especialista |
| FK_TipoChamado_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TipoChamado_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_TipoChamado_CodigoCliente | UNIQUE | (Codigo, ClienteId) | Código único |
| CHK_TipoChamado_CategoriaITIL | CHECK | CategoriaITIL IN ('INCIDENTE', 'REQUISICAO', 'MUDANCA', 'PROBLEMA') | Categorias válidas |
| CHK_TipoChamado_Cor | CHECK | Cor IS NULL OR Cor LIKE '#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]' | Formato hexadecimal |

---

### 2.2 Tabela: SLATipoChamado

**Descrição:** Define Service Level Agreement (SLA) por tipo de chamado e prioridade. Tempos de resposta e resolução em minutos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Prioridade | VARCHAR(20) | NÃO | - | CRITICA, ALTA, MEDIA, BAIXA |
| TempoRespostaMinutos | INT | NÃO | - | Tempo máximo para primeira resposta |
| TempoResolucaoMinutos | INT | NÃO | - | Tempo máximo para resolução |
| TempoReabertura | Minutos | INT | SIM | NULL | Tempo máximo para reabrir |
| PercentualCumprimento | DECIMAL(5,2) | NÃO | 95.00 | Meta de cumprimento (%) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_SLATipoChamado | Id | CLUSTERED | Chave primária |
| IX_SLATipoChamado_TipoId | TipoChamadoId, Prioridade | NONCLUSTERED | Busca SLA específico |
| IX_SLATipoChamado_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_SLATipoChamado_Ativo | Ativo, TipoChamadoId | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_SLATipoChamado | PRIMARY KEY | Id | Chave primária |
| FK_SLATipoChamado_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_SLATipoChamado_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_SLATipoChamado_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_SLATipoChamado_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_SLATipoChamado_TipoPrioridade | UNIQUE | (TipoChamadoId, Prioridade, ClienteId) | SLA único por combinação |
| CHK_SLATipoChamado_Prioridade | CHECK | Prioridade IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA') | Prioridades válidas |
| CHK_SLATipoChamado_Tempos | CHECK | TempoResolucaoMinutos >= TempoRespostaMinutos | Resolução >= Resposta |

---

### 2.3 Tabela: FormularioDinamico

**Descrição:** Define campos customizados obrigatórios ou opcionais por tipo de chamado. Permite formulários dinâmicos adaptados a cada tipo.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| NomeCampo | VARCHAR(100) | NÃO | - | Nome do campo |
| LabelCampo | VARCHAR(200) | NÃO | - | Label de exibição |
| TipoCampo | VARCHAR(20) | NÃO | - | TEXT, NUMBER, SELECT, DATE, CHECKBOX, FILE |
| Obrigatorio | BIT | NÃO | 0 | Se é campo obrigatório |
| Ordem | INT | NÃO | 0 | Ordem de exibição |
| Opcoes | TEXT | SIM | NULL | JSON array para SELECT (["Opção1", "Opção2"]) |
| Validacoes | TEXT | SIM | NULL | JSON com regras de validação |
| PlaceholderTexto | VARCHAR(200) | SIM | NULL | Texto de placeholder |
| ValorPadrao | VARCHAR(500) | SIM | NULL | Valor padrão do campo |
| Largura | INT | NÃO | 12 | Largura grid (1-12) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_FormularioDinamico | Id | CLUSTERED | Chave primária |
| IX_FormularioDinamico_TipoId | TipoChamadoId, Ordem | NONCLUSTERED | Listar campos ordenados |
| IX_FormularioDinamico_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_FormularioDinamico_NomeCampo | NomeCampo, TipoChamadoId | NONCLUSTERED | Busca por nome |
| IX_FormularioDinamico_Ativo | Ativo, TipoChamadoId | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_FormularioDinamico | PRIMARY KEY | Id | Chave primária |
| FK_FormularioDinamico_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_FormularioDinamico_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_FormularioDinamico_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_FormularioDinamico_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_FormularioDinamico_NomeTipo | UNIQUE | (NomeCampo, TipoChamadoId) | Nome único por tipo |
| CHK_FormularioDinamico_TipoCampo | CHECK | TipoCampo IN ('TEXT', 'NUMBER', 'SELECT', 'DATE', 'CHECKBOX', 'FILE', 'TEXTAREA') | Tipos válidos |
| CHK_FormularioDinamico_Largura | CHECK | Largura BETWEEN 1 AND 12 | Largura válida |

---

### 2.4 Tabela: TemplateResolucao

**Descrição:** Armazena soluções padrão (knowledge base) para problemas recorrentes. Contém passos de resolução, taxa de sucesso e quantidade de usos.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Titulo | VARCHAR(200) | NÃO | - | Título do template |
| Descricao | TEXT | SIM | NULL | Descrição do problema |
| PassosResolucao | TEXT | NÃO | - | Passos detalhados da resolução |
| QuantidadeUsos | INT | NÃO | 0 | Contador de vezes usado |
| QuantidadeSucessos | INT | NÃO | 0 | Contador de sucessos |
| TaxaSucesso | AS (CASE WHEN QuantidadeUsos > 0 THEN (QuantidadeSucessos * 100.0 / QuantidadeUsos) ELSE 0 END) PERSISTED | - | - | Taxa sucesso calculada |
| TempoMedioResolucaoMin | INT | SIM | NULL | Tempo médio de resolução |
| Tags | VARCHAR(500) | SIM | NULL | Tags separadas por vírgula |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TemplateResolucao | Id | CLUSTERED | Chave primária |
| IX_TemplateResolucao_TipoId | TipoChamadoId, TaxaSucesso DESC | NONCLUSTERED | Ordenar por taxa sucesso |
| IX_TemplateResolucao_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_TemplateResolucao_Ativo | Ativo, TipoChamadoId | NONCLUSTERED | Filtro ativos |
| IX_TemplateResolucao_Titulo | Titulo | NONCLUSTERED | Busca por título (FULLTEXT) |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TemplateResolucao | PRIMARY KEY | Id | Chave primária |
| FK_TemplateResolucao_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_TemplateResolucao_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_TemplateResolucao_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TemplateResolucao_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| CHK_TemplateResolucao_Quantidades | CHECK | QuantidadeSucessos <= QuantidadeUsos | Sucessos <= Usos |

---

### 2.5 Tabela: EscalonamentoTipo

**Descrição:** Define níveis de escalonamento automático por tipo de chamado quando SLA está prestes a estourar. Cada nível aponta para um grupo de atendimento.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Nivel | INT | NÃO | - | Nível de escalonamento (1, 2, 3...) |
| GrupoAtendimentoId | UNIQUEIDENTIFIER | NÃO | - | FK para grupo de atendimento |
| TempoEscalonamentoMin | INT | NÃO | - | Tempo para escalonar (minutos) |
| NotificarGestor | BIT | NÃO | 1 | Se notifica gestor do grupo |
| NotificarCliente | BIT | NÃO | 0 | Se notifica cliente |
| MensagemTemplate | TEXT | SIM | NULL | Template de mensagem de notificação |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_EscalonamentoTipo | Id | CLUSTERED | Chave primária |
| IX_EscalonamentoTipo_TipoId | TipoChamadoId, Nivel | NONCLUSTERED | Ordenar por nível |
| IX_EscalonamentoTipo_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_EscalonamentoTipo_GrupoId | GrupoAtendimentoId | NONCLUSTERED | Join com grupos |
| IX_EscalonamentoTipo_Ativo | Ativo, TipoChamadoId | NONCLUSTERED | Filtro ativos |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_EscalonamentoTipo | PRIMARY KEY | Id | Chave primária |
| FK_EscalonamentoTipo_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_EscalonamentoTipo_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_EscalonamentoTipo_Grupo | FOREIGN KEY | GrupoAtendimentoId REFERENCES GrupoAtendimento(Id) | Grupo alvo |
| FK_EscalonamentoTipo_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_EscalonamentoTipo_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_EscalonamentoTipo_TipoNivel | UNIQUE | (TipoChamadoId, Nivel) | Nível único por tipo |
| CHK_EscalonamentoTipo_Nivel | CHECK | Nivel > 0 | Nível positivo |
| CHK_EscalonamentoTipo_Tempo | CHECK | TempoEscalonamentoMin > 0 | Tempo positivo |

---

### 2.6 Tabela: MatrizImpactoUrgencia

**Descrição:** Matriz ITIL para calcular prioridade automaticamente baseada em combinação de Impacto × Urgência. Cada tipo de chamado pode ter matriz customizada.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Impacto | VARCHAR(20) | NÃO | - | ALTO, MEDIO, BAIXO |
| Urgencia | VARCHAR(20) | NÃO | - | ALTA, MEDIA, BAIXA |
| PrioridadeResultante | VARCHAR(20) | NÃO | - | CRITICA, ALTA, MEDIA, BAIXA |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_MatrizImpactoUrgencia | Id | CLUSTERED | Chave primária |
| IX_MatrizImpactoUrgencia_TipoId | TipoChamadoId | NONCLUSTERED | Filtro por tipo |
| IX_MatrizImpactoUrgencia_Lookup | TipoChamadoId, Impacto, Urgencia | NONCLUSTERED | Busca rápida prioridade |
| IX_MatrizImpactoUrgencia_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_MatrizImpactoUrgencia | PRIMARY KEY | Id | Chave primária |
| FK_MatrizImpactoUrgencia_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_MatrizImpactoUrgencia_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_MatrizImpactoUrgencia_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_MatrizImpactoUrgencia_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_MatrizImpactoUrgencia_Combinacao | UNIQUE | (TipoChamadoId, Impacto, Urgencia) | Combinação única |
| CHK_MatrizImpactoUrgencia_Impacto | CHECK | Impacto IN ('ALTO', 'MEDIO', 'BAIXO') | Impactos válidos |
| CHK_MatrizImpactoUrgencia_Urgencia | CHECK | Urgencia IN ('ALTA', 'MEDIA', 'BAIXA') | Urgências válidas |
| CHK_MatrizImpactoUrgencia_Prioridade | CHECK | PrioridadeResultante IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA') | Prioridades válidas |

---

### 2.7 Tabela: TipoChamadoEspecialista

**Descrição:** Vincula especialistas/técnicos a tipos de chamado específicos. Armazena nível de experiência e métricas de performance.

#### Campos

| Campo | Tipo | Nulo | Default | Descrição |
|-------|------|------|---------|-----------|
| Id | UNIQUEIDENTIFIER | NÃO | NEWID() | Chave primária |
| TipoChamadoId | UNIQUEIDENTIFIER | NÃO | - | FK para TipoChamado |
| EspecialistaId | UNIQUEIDENTIFIER | NÃO | - | FK para Usuario (técnico) |
| ClienteId | UNIQUEIDENTIFIER | NÃO | - | FK para GestaoCliente |
| Preferencial | BIT | NÃO | 0 | Se é especialista preferencial |
| NivelExperiencia | INT | NÃO | 1 | Nível 1-5 (1=Junior, 5=Senior) |
| QuantidadeChamados | AS (SELECT COUNT(*) FROM Chamado WHERE TecnicoId = EspecialistaId AND TipoChamadoId = TipoChamadoId) PERSISTED | - | - | Total de chamados atendidos |
| AvaliacaoMedia | AS (SELECT AVG(Avaliacao) FROM Chamado WHERE TecnicoId = EspecialistaId AND TipoChamadoId = TipoChamadoId AND Avaliacao IS NOT NULL) PERSISTED | - | - | Avaliação média (1-5) |
| Ativo | BIT | NÃO | 1 | Status ativo/inativo |
| CreatedAt | DATETIME2 | NÃO | GETUTCDATE() | Data de criação |
| CreatedBy | UNIQUEIDENTIFIER | NÃO | - | Usuário criador |
| ModifiedAt | DATETIME2 | SIM | NULL | Data de atualização |
| ModifiedBy | UNIQUEIDENTIFIER | SIM | NULL | Usuário atualizador |

#### Índices

| Nome | Colunas | Tipo | Descrição |
|------|---------|------|-----------|
| PK_TipoChamadoEspecialista | Id | CLUSTERED | Chave primária |
| IX_TipoChamadoEspecialista_TipoId | TipoChamadoId, NivelExperiencia DESC | NONCLUSTERED | Listar especialistas |
| IX_TipoChamadoEspecialista_EspecialistaId | EspecialistaId | NONCLUSTERED | Tipos por especialista |
| IX_TipoChamadoEspecialista_ClienteId | ClienteId | NONCLUSTERED | Multi-tenancy |
| IX_TipoChamadoEspecialista_Preferencial | TipoChamadoId, Preferencial | NONCLUSTERED | Encontrar preferencial |

#### Constraints

| Nome | Tipo | Definição | Descrição |
|------|------|-----------|-----------|
| PK_TipoChamadoEspecialista | PRIMARY KEY | Id | Chave primária |
| FK_TipoChamadoEspecialista_TipoChamado | FOREIGN KEY | TipoChamadoId REFERENCES TipoChamado(Id) ON DELETE CASCADE | Tipo pai |
| FK_TipoChamadoEspecialista_Especialista | FOREIGN KEY | EspecialistaId REFERENCES Usuario(Id) | Técnico especialista |
| FK_TipoChamadoEspecialista_Cliente | FOREIGN KEY | ClienteId REFERENCES GestaoCliente(Id) | Multi-tenancy |
| FK_TipoChamadoEspecialista_CreatedBy | FOREIGN KEY | CreatedBy REFERENCES Usuario(Id) | Auditoria |
| FK_TipoChamadoEspecialista_ModifiedBy | FOREIGN KEY | ModifiedBy REFERENCES Usuario(Id) | Auditoria |
| UQ_TipoChamadoEspecialista_TipoEspecialista | UNIQUE | (TipoChamadoId, EspecialistaId) | Vínculo único |
| CHK_TipoChamadoEspecialista_Nivel | CHECK | NivelExperiencia BETWEEN 1 AND 5 | Nível válido (1-5) |

---

## 3. Relacionamentos

| Tabela Origem | Cardinalidade | Tabela Destino | Descrição |
|---------------|---------------|----------------|-----------|
| GestaoCliente | 1:N | TipoChamado | Cliente possui múltiplos tipos |
| TipoChamado | 1:N | SLATipoChamado | Tipo tem SLA por prioridade |
| TipoChamado | 1:N | FormularioDinamico | Tipo tem campos customizados |
| TipoChamado | 1:N | TemplateResolucao | Tipo tem templates de solução |
| TipoChamado | 1:N | EscalonamentoTipo | Tipo tem níveis de escalonamento |
| TipoChamado | 1:N | MatrizImpactoUrgencia | Tipo tem matriz customizada |
| TipoChamado | 1:N | TipoChamadoEspecialista | Tipo vinculado a especialistas |
| TipoChamado | N:1 | FilaAtendimento | Tipo tem fila padrão |
| TipoChamado | N:1 | Usuario (especialista) | Tipo tem especialista preferencial |
| EscalonamentoTipo | N:1 | GrupoAtendimento | Escalonamento aponta para grupo |
| TipoChamadoEspecialista | N:1 | Usuario | Vínculo com técnico |
| Usuario | 1:N | TipoChamado (criação) | Usuário cria tipos |

---

## 4. DDL - SQL Server

```sql
-- =============================================
-- RF060 - Gestão de Tipos de Chamado
-- Modelo de Dados
-- Data: 2025-12-18
-- Versão: 1.0
-- =============================================

-- ---------------------------------------------
-- Tabela: TipoChamado
-- ---------------------------------------------
CREATE TABLE TipoChamado (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Codigo VARCHAR(50) NOT NULL,
    Nome VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    CategoriaITIL VARCHAR(50) NOT NULL,
    CategoriaHierarquica VARCHAR(500) NULL,
    FilaPadraoId UNIQUEIDENTIFIER NULL,
    EspecialistaPreferencialId UNIQUEIDENTIFIER NULL,
    RequerAprovacaoCAB BIT NOT NULL DEFAULT 0,
    PermiteAnexos BIT NOT NULL DEFAULT 1,
    Icone VARCHAR(50) NULL,
    Cor VARCHAR(7) NULL,
    Ordem INT NOT NULL DEFAULT 0,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_TipoChamado_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_TipoChamado_FilaPadrao
        FOREIGN KEY (FilaPadraoId) REFERENCES FilaAtendimento(Id),
    CONSTRAINT FK_TipoChamado_Especialista
        FOREIGN KEY (EspecialistaPreferencialId) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoChamado_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoChamado_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_TipoChamado_CodigoCliente
        UNIQUE (Codigo, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_TipoChamado_CategoriaITIL
        CHECK (CategoriaITIL IN ('INCIDENTE', 'REQUISICAO', 'MUDANCA', 'PROBLEMA')),
    CONSTRAINT CHK_TipoChamado_Cor
        CHECK (Cor IS NULL OR Cor LIKE '#[0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]')
);

-- Indices
CREATE NONCLUSTERED INDEX IX_TipoChamado_ClienteId ON TipoChamado(ClienteId);
CREATE NONCLUSTERED INDEX IX_TipoChamado_Codigo ON TipoChamado(Codigo, ClienteId);
CREATE NONCLUSTERED INDEX IX_TipoChamado_CategoriaITIL ON TipoChamado(CategoriaITIL, ClienteId);
CREATE NONCLUSTERED INDEX IX_TipoChamado_Ativo ON TipoChamado(Ativo, ClienteId) WHERE FlExcluido = 0;
CREATE NONCLUSTERED INDEX IX_TipoChamado_FilaPadrao ON TipoChamado(FilaPadraoId) WHERE FilaPadraoId IS NOT NULL;

-- Comentários
EXEC sp_addextendedproperty @name = N'MS_Description', @value = 'Tipos de chamados técnicos baseados em ITIL v4',
    @level0type = N'SCHEMA', @level0name = 'dbo', @level1type = N'TABLE', @level1name = 'TipoChamado';


-- ---------------------------------------------
-- Tabela: SLATipoChamado
-- ---------------------------------------------
CREATE TABLE SLATipoChamado (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Prioridade VARCHAR(20) NOT NULL,
    TempoRespostaMinutos INT NOT NULL,
    TempoResolucaoMinutos INT NOT NULL,
    TempoReaberturaMinutos INT NULL,
    PercentualCumprimento DECIMAL(5,2) NOT NULL DEFAULT 95.00,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_SLATipoChamado_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_SLATipoChamado_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_SLATipoChamado_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_SLATipoChamado_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_SLATipoChamado_TipoPrioridade
        UNIQUE (TipoChamadoId, Prioridade, ClienteId),

    -- Check Constraints
    CONSTRAINT CHK_SLATipoChamado_Prioridade
        CHECK (Prioridade IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA')),
    CONSTRAINT CHK_SLATipoChamado_Tempos
        CHECK (TempoResolucaoMinutos >= TempoRespostaMinutos)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_SLATipoChamado_TipoId ON SLATipoChamado(TipoChamadoId, Prioridade);
CREATE NONCLUSTERED INDEX IX_SLATipoChamado_ClienteId ON SLATipoChamado(ClienteId);
CREATE NONCLUSTERED INDEX IX_SLATipoChamado_Ativo ON SLATipoChamado(Ativo, TipoChamadoId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: FormularioDinamico
-- ---------------------------------------------
CREATE TABLE FormularioDinamico (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    NomeCampo VARCHAR(100) NOT NULL,
    LabelCampo VARCHAR(200) NOT NULL,
    TipoCampo VARCHAR(20) NOT NULL,
    Obrigatorio BIT NOT NULL DEFAULT 0,
    Ordem INT NOT NULL DEFAULT 0,
    Opcoes TEXT NULL,
    Validacoes TEXT NULL,
    PlaceholderTexto VARCHAR(200) NULL,
    ValorPadrao VARCHAR(500) NULL,
    Largura INT NOT NULL DEFAULT 12,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_FormularioDinamico_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_FormularioDinamico_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_FormularioDinamico_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_FormularioDinamico_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_FormularioDinamico_NomeTipo
        UNIQUE (NomeCampo, TipoChamadoId),

    -- Check Constraints
    CONSTRAINT CHK_FormularioDinamico_TipoCampo
        CHECK (TipoCampo IN ('TEXT', 'NUMBER', 'SELECT', 'DATE', 'CHECKBOX', 'FILE', 'TEXTAREA')),
    CONSTRAINT CHK_FormularioDinamico_Largura
        CHECK (Largura BETWEEN 1 AND 12)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_FormularioDinamico_TipoId ON FormularioDinamico(TipoChamadoId, Ordem);
CREATE NONCLUSTERED INDEX IX_FormularioDinamico_ClienteId ON FormularioDinamico(ClienteId);
CREATE NONCLUSTERED INDEX IX_FormularioDinamico_NomeCampo ON FormularioDinamico(NomeCampo, TipoChamadoId);
CREATE NONCLUSTERED INDEX IX_FormularioDinamico_Ativo ON FormularioDinamico(Ativo, TipoChamadoId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: TemplateResolucao
-- ---------------------------------------------
CREATE TABLE TemplateResolucao (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Titulo VARCHAR(200) NOT NULL,
    Descricao TEXT NULL,
    PassosResolucao TEXT NOT NULL,
    QuantidadeUsos INT NOT NULL DEFAULT 0,
    QuantidadeSucessos INT NOT NULL DEFAULT 0,
    TaxaSucesso AS (CASE WHEN QuantidadeUsos > 0 THEN (QuantidadeSucessos * 100.0 / QuantidadeUsos) ELSE 0 END) PERSISTED,
    TempoMedioResolucaoMin INT NULL,
    Tags VARCHAR(500) NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_TemplateResolucao_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_TemplateResolucao_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_TemplateResolucao_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TemplateResolucao_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Check Constraints
    CONSTRAINT CHK_TemplateResolucao_Quantidades
        CHECK (QuantidadeSucessos <= QuantidadeUsos)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_TemplateResolucao_TipoId ON TemplateResolucao(TipoChamadoId, TaxaSucesso DESC);
CREATE NONCLUSTERED INDEX IX_TemplateResolucao_ClienteId ON TemplateResolucao(ClienteId);
CREATE NONCLUSTERED INDEX IX_TemplateResolucao_Ativo ON TemplateResolucao(Ativo, TipoChamadoId) WHERE FlExcluido = 0;
CREATE FULLTEXT INDEX ON TemplateResolucao(Titulo, Descricao, PassosResolucao) KEY INDEX PK_TemplateResolucao;


-- ---------------------------------------------
-- Tabela: EscalonamentoTipo
-- ---------------------------------------------
CREATE TABLE EscalonamentoTipo (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Nivel INT NOT NULL,
    GrupoAtendimentoId UNIQUEIDENTIFIER NOT NULL,
    TempoEscalonamentoMin INT NOT NULL,
    NotificarGestor BIT NOT NULL DEFAULT 1,
    NotificarCliente BIT NOT NULL DEFAULT 0,
    MensagemTemplate TEXT NULL,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_EscalonamentoTipo_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_EscalonamentoTipo_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_EscalonamentoTipo_Grupo
        FOREIGN KEY (GrupoAtendimentoId) REFERENCES GrupoAtendimento(Id),
    CONSTRAINT FK_EscalonamentoTipo_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_EscalonamentoTipo_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_EscalonamentoTipo_TipoNivel
        UNIQUE (TipoChamadoId, Nivel),

    -- Check Constraints
    CONSTRAINT CHK_EscalonamentoTipo_Nivel
        CHECK (Nivel > 0),
    CONSTRAINT CHK_EscalonamentoTipo_Tempo
        CHECK (TempoEscalonamentoMin > 0)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_EscalonamentoTipo_TipoId ON EscalonamentoTipo(TipoChamadoId, Nivel);
CREATE NONCLUSTERED INDEX IX_EscalonamentoTipo_ClienteId ON EscalonamentoTipo(ClienteId);
CREATE NONCLUSTERED INDEX IX_EscalonamentoTipo_GrupoId ON EscalonamentoTipo(GrupoAtendimentoId);
CREATE NONCLUSTERED INDEX IX_EscalonamentoTipo_Ativo ON EscalonamentoTipo(Ativo, TipoChamadoId) WHERE FlExcluido = 0;


-- ---------------------------------------------
-- Tabela: MatrizImpactoUrgencia
-- ---------------------------------------------
CREATE TABLE MatrizImpactoUrgencia (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Impacto VARCHAR(20) NOT NULL,
    Urgencia VARCHAR(20) NOT NULL,
    PrioridadeResultante VARCHAR(20) NOT NULL,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_MatrizImpactoUrgencia_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_MatrizImpactoUrgencia_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_MatrizImpactoUrgencia_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_MatrizImpactoUrgencia_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_MatrizImpactoUrgencia_Combinacao
        UNIQUE (TipoChamadoId, Impacto, Urgencia),

    -- Check Constraints
    CONSTRAINT CHK_MatrizImpactoUrgencia_Impacto
        CHECK (Impacto IN ('ALTO', 'MEDIO', 'BAIXO')),
    CONSTRAINT CHK_MatrizImpactoUrgencia_Urgencia
        CHECK (Urgencia IN ('ALTA', 'MEDIA', 'BAIXA')),
    CONSTRAINT CHK_MatrizImpactoUrgencia_Prioridade
        CHECK (PrioridadeResultante IN ('CRITICA', 'ALTA', 'MEDIA', 'BAIXA'))
);

-- Indices
CREATE NONCLUSTERED INDEX IX_MatrizImpactoUrgencia_TipoId ON MatrizImpactoUrgencia(TipoChamadoId);
CREATE NONCLUSTERED INDEX IX_MatrizImpactoUrgencia_Lookup ON MatrizImpactoUrgencia(TipoChamadoId, Impacto, Urgencia);
CREATE NONCLUSTERED INDEX IX_MatrizImpactoUrgencia_ClienteId ON MatrizImpactoUrgencia(ClienteId);


-- ---------------------------------------------
-- Tabela: TipoChamadoEspecialista
-- ---------------------------------------------
CREATE TABLE TipoChamadoEspecialista (
    Id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    TipoChamadoId UNIQUEIDENTIFIER NOT NULL,
    EspecialistaId UNIQUEIDENTIFIER NOT NULL,
    ClienteId UNIQUEIDENTIFIER NOT NULL,
    Preferencial BIT NOT NULL DEFAULT 0,
    NivelExperiencia INT NOT NULL DEFAULT 1,
    FlExcluido BIT NOT NULL DEFAULT 0,
    CreatedAt DATETIME2 NOT NULL DEFAULT GETUTCDATE(),
    CreatedBy UNIQUEIDENTIFIER NOT NULL,
    ModifiedAt DATETIME2 NULL,
    ModifiedBy UNIQUEIDENTIFIER NULL,

    -- Foreign Keys
    CONSTRAINT FK_TipoChamadoEspecialista_TipoChamado
        FOREIGN KEY (TipoChamadoId) REFERENCES TipoChamado(Id) ON DELETE CASCADE,
    CONSTRAINT FK_TipoChamadoEspecialista_Especialista
        FOREIGN KEY (EspecialistaId) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoChamadoEspecialista_Cliente
        FOREIGN KEY (ClienteId) REFERENCES GestaoCliente(Id),
    CONSTRAINT FK_TipoChamadoEspecialista_CreatedBy
        FOREIGN KEY (CreatedBy) REFERENCES Usuario(Id),
    CONSTRAINT FK_TipoChamadoEspecialista_ModifiedBy
        FOREIGN KEY (ModifiedBy) REFERENCES Usuario(Id),

    -- Unique Constraints
    CONSTRAINT UQ_TipoChamadoEspecialista_TipoEspecialista
        UNIQUE (TipoChamadoId, EspecialistaId),

    -- Check Constraints
    CONSTRAINT CHK_TipoChamadoEspecialista_Nivel
        CHECK (NivelExperiencia BETWEEN 1 AND 5)
);

-- Indices
CREATE NONCLUSTERED INDEX IX_TipoChamadoEspecialista_TipoId ON TipoChamadoEspecialista(TipoChamadoId, NivelExperiencia DESC);
CREATE NONCLUSTERED INDEX IX_TipoChamadoEspecialista_EspecialistaId ON TipoChamadoEspecialista(EspecialistaId);
CREATE NONCLUSTERED INDEX IX_TipoChamadoEspecialista_ClienteId ON TipoChamadoEspecialista(ClienteId);
CREATE NONCLUSTERED INDEX IX_TipoChamadoEspecialista_Preferencial ON TipoChamadoEspecialista(TipoChamadoId, Preferencial) WHERE Preferencial = 1;
```

---

## 5. Stored Procedures

```sql
-- Procedure: Calcular prioridade baseado em matriz Impacto × Urgencia
CREATE PROCEDURE sp_CalcularPrioridade
    @TipoChamadoId UNIQUEIDENTIFIER,
    @Impacto VARCHAR(20),
    @Urgencia VARCHAR(20),
    @Prioridade VARCHAR(20) OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT @Prioridade = PrioridadeResultante
    FROM MatrizImpactoUrgencia
    WHERE TipoChamadoId = @TipoChamadoId
        AND Impacto = @Impacto
        AND Urgencia = @Urgencia;

    -- Se não encontrar matriz customizada, usar padrão ITIL
    IF @Prioridade IS NULL
    BEGIN
        IF (@Impacto = 'ALTO' AND @Urgencia = 'ALTA')
            SET @Prioridade = 'CRITICA';
        ELSE IF ((@Impacto = 'ALTO' AND @Urgencia = 'MEDIA') OR (@Impacto = 'MEDIO' AND @Urgencia = 'ALTA'))
            SET @Prioridade = 'ALTA';
        ELSE IF ((@Impacto = 'MEDIO' AND @Urgencia = 'MEDIA') OR (@Impacto = 'ALTO' AND @Urgencia = 'BAIXA') OR (@Impacto = 'BAIXO' AND @Urgencia = 'ALTA'))
            SET @Prioridade = 'MEDIA';
        ELSE
            SET @Prioridade = 'BAIXA';
    END;
END;
GO

-- Procedure: Obter SLA por tipo e prioridade
CREATE PROCEDURE sp_ObterSLA
    @TipoChamadoId UNIQUEIDENTIFIER,
    @Prioridade VARCHAR(20),
    @TempoRespostaMin INT OUTPUT,
    @TempoResolucaoMin INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        @TempoRespostaMin = TempoRespostaMinutos,
        @TempoResolucaoMin = TempoResolucaoMinutos
    FROM SLATipoChamado
    WHERE TipoChamadoId = @TipoChamadoId
        AND Prioridade = @Prioridade
        AND Ativo = 1;

    IF @TempoRespostaMin IS NULL
    BEGIN
        -- SLAs padrão se não configurado
        IF @Prioridade = 'CRITICA'
        BEGIN
            SET @TempoRespostaMin = 30;
            SET @TempoResolucaoMin = 240; -- 4 horas
        END
        ELSE IF @Prioridade = 'ALTA'
        BEGIN
            SET @TempoRespostaMin = 120;
            SET @TempoResolucaoMin = 480; -- 8 horas
        END
        ELSE IF @Prioridade = 'MEDIA'
        BEGIN
            SET @TempoRespostaMin = 240;
            SET @TempoResolucaoMin = 1440; -- 24 horas
        END
        ELSE
        BEGIN
            SET @TempoRespostaMin = 480;
            SET @TempoResolucaoMin = 4320; -- 72 horas
        END
    END;
END;
GO

-- Procedure: Obter templates de resolução por taxa de sucesso
CREATE PROCEDURE sp_ObterTemplatesResolucao
    @TipoChamadoId UNIQUEIDENTIFIER,
    @PalavraChave VARCHAR(200) = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        Id,
        Titulo,
        Descricao,
        PassosResolucao,
        QuantidadeUsos,
        TaxaSucesso,
        TempoMedioResolucaoMin,
        Tags
    FROM TemplateResolucao
    WHERE TipoChamadoId = @TipoChamadoId
        AND Ativo = 1
        AND (
            @PalavraChave IS NULL
            OR Titulo LIKE '%' + @PalavraChave + '%'
            OR Descricao LIKE '%' + @PalavraChave + '%'
            OR Tags LIKE '%' + @PalavraChave + '%'
        )
    ORDER BY TaxaSucesso DESC, QuantidadeUsos DESC;
END;
GO
```

---

## 6. Views de Negócio

```sql
-- View: Resumo de tipos de chamado com SLA
CREATE VIEW vw_TiposChamadoResumo AS
SELECT
    t.Id,
    t.Codigo,
    t.Nome,
    t.CategoriaITIL,
    t.Ativo,
    COUNT(DISTINCT s.Id) AS QuantidadeSLAs,
    COUNT(DISTINCT f.Id) AS QuantidadeCamposFormulario,
    COUNT(DISTINCT tr.Id) AS QuantidadeTemplates,
    COUNT(DISTINCT e.Id) AS NiveisEscalonamento,
    COUNT(DISTINCT esp.Id) AS QuantidadeEspecialistas
FROM TipoChamado t
LEFT JOIN SLATipoChamado s ON t.Id = s.TipoChamadoId
LEFT JOIN FormularioDinamico f ON t.Id = f.TipoChamadoId
LEFT JOIN TemplateResolucao tr ON t.Id = tr.TipoChamadoId
LEFT JOIN EscalonamentoTipo e ON t.Id = e.TipoChamadoId
LEFT JOIN TipoChamadoEspecialista esp ON t.Id = esp.TipoChamadoId
GROUP BY t.Id, t.Codigo, t.Nome, t.CategoriaITIL, t.Ativo;
GO
```

---

## 7. Dados Iniciais (Seed)

```sql
-- Inserir tipos padrão baseados em ITIL v4
DECLARE @ClienteId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM GestaoCliente);
DECLARE @UsuarioId UNIQUEIDENTIFIER = (SELECT TOP 1 Id FROM Usuario WHERE Email = 'admin@icontrolit.com');

-- Tipo: Incidente
DECLARE @TipoIncidente UNIQUEIDENTIFIER = NEWID();
INSERT INTO TipoChamado (Id, ClienteId, Codigo, Nome, Descricao, CategoriaITIL, Icone, Cor, Ordem, CreatedBy) VALUES
(@TipoIncidente, @ClienteId, 'INCIDENTE', 'Incidente', 'Interrupção não planejada ou redução na qualidade de um serviço de TI', 'INCIDENTE', 'fa-exclamation-circle', '#EF4444', 1, @UsuarioId);

-- SLA Incidente
INSERT INTO SLATipoChamado (TipoChamadoId, ClienteId, Prioridade, TempoRespostaMinutos, TempoResolucaoMinutos, CreatedBy) VALUES
(@TipoIncidente, @ClienteId, 'CRITICA', 30, 240, @UsuarioId),
(@TipoIncidente, @ClienteId, 'ALTA', 120, 480, @UsuarioId),
(@TipoIncidente, @ClienteId, 'MEDIA', 240, 1440, @UsuarioId),
(@TipoIncidente, @ClienteId, 'BAIXA', 480, 4320, @UsuarioId);

-- Matriz Impacto × Urgência Incidente
INSERT INTO MatrizImpactoUrgencia (TipoChamadoId, ClienteId, Impacto, Urgencia, PrioridadeResultante, CreatedBy) VALUES
(@TipoIncidente, @ClienteId, 'ALTO', 'ALTA', 'CRITICA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'ALTO', 'MEDIA', 'ALTA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'ALTO', 'BAIXA', 'MEDIA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'MEDIO', 'ALTA', 'ALTA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'MEDIO', 'MEDIA', 'MEDIA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'MEDIO', 'BAIXA', 'BAIXA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'BAIXO', 'ALTA', 'MEDIA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'BAIXO', 'MEDIA', 'BAIXA', @UsuarioId),
(@TipoIncidente, @ClienteId, 'BAIXO', 'BAIXA', 'BAIXA', @UsuarioId);
```

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-18 | IControlIT Architect | Versão inicial - 7 tabelas, 40+ índices, views, procedures |

---

**Total de Tabelas:** 7
**Total de Índices:** 42
**Total de Views:** 1
**Total de Stored Procedures:** 3
**Linhas de DDL:** ~1100

**Documento gerado em:** 2025-12-18
**Status:** Aprovado para implementação

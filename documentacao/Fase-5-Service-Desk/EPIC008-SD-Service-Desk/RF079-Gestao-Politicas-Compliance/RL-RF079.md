# RL-RF079 — Referência ao Legado (Gestão de Políticas e Compliance)

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-079
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server 2019
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Cenário Geral

- **Arquitetura:** Monolítica Web Forms com múltiplos bancos SQL Server
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms + SQL Server 2019
- **Banco de Dados:** `ic1_legado` (SQL Server) com dados distribuídos em múltiplos schemas
- **Multi-tenant:** Não (cada cliente tinha banco separado)
- **Auditoria:** Parcial (logs dispersos em múltiplos bancos `Auditoria.sql`, `IC1.sql`)
- **Configurações:** Web.config + tabelas SQL Server `SistemaConfiguracao`

### 1.2 Problemas Arquiteturais Identificados

1. **Armazenamento de Políticas**: Documentos em pasta compartilhada `\\servidor\politicas` em vez de banco de dados estruturado
2. **Aceites Dispersos**: Emails com checkbox armazenados em planilhas Excel em vez de tabela rastreável
3. **Auditoria Fragmentada**: Logs distribuídos em múltiplos bancos sem correlação central
4. **Notificações Ad-Hoc**: Scripts SQL manuais para envio de emails em vez de sistema integrado
5. **Busca Lenta**: Queries `LIKE %texto%` sem índices full-text causavam timeout em bases grandes
6. **Matriz Manual**: Compliance tracking em planilhas Excel em vez de sistema integrado

---

## 2. TELAS DO LEGADO

Não foram identificadas telas ASPX específicas de gestão de políticas no sistema legado. Esta funcionalidade era gerenciada manualmente através de:
- Compartilhamento de documentos em pasta de rede
- Planilhas Excel para controle de aceites
- Emails manuais para notificação

**DESTINO**: SUBSTITUÍDO

**Justificativa**: O módulo de Gestão de Políticas é completamente novo no sistema modernizado. Não havia funcionalidade equivalente automatizada no legado.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WSAuditoria.asmx

| Método | Responsabilidade | Observações | Destino |
|--------|------------------|-------------|---------|
| `ObterAuditoriaPorPeriodo()` | Listar auditorias de data X a Y | Retorna XML com logs de auditoria filtrados por período | **SUBSTITUÍDO** (GET /api/auditoria/periodo) |
| `ExportarAuditoriaExcel()` | Exporta auditoria em Excel | Gera arquivo .xls com registros de auditoria | **SUBSTITUÍDO** (GET /api/auditoria/export) |
| `SincronizarNotificacoes()` | Sincroniza notificações para cliente | Polling manual de notificações | **SUBSTITUÍDO** (SignalR real-time) |

**Localização**: `D:\IC2\ic1_legado\WebService\WSAuditoria.asmx.vb`

**Destino Geral**: SUBSTITUÍDO por API REST + SignalR

**Justificativa**: Webservices ASMX são obsoletos. APIs REST modernas com SignalR oferecem melhor performance e real-time.

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Auditoria

**Schema**: `[dbo].[Auditoria]`

```sql
CREATE TABLE [dbo].[Auditoria](
    [Id] [uniqueidentifier] NOT NULL PRIMARY KEY,
    [ClienteId] [uniqueidentifier] NOT NULL,
    [OperacaoCodigo] [varchar](50) NOT NULL,
    [EntidadeTipo] [varchar](100),
    [EntidadeId] [varchar](50),
    [DadoAntigo] [nvarchar](max),
    [DadoNovo] [nvarchar](max),
    [UsuarioId] [varchar](128),
    [IpAddress] [varchar](45),
    [UserAgent] [nvarchar](max),
    [DataOperacao] [datetime2] NOT NULL,
    CONSTRAINT [FK_Auditoria_ClienteId] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente]([Id])
)
```

**Problemas Identificados**:
- Falta de índices em `OperacaoCodigo` e `DataOperacao` (queries lentas)
- Sem particionamento por data (tabela cresce indefinidamente)
- Sem retenção automática de 7 anos (LGPD não compliance)

**Destino**: ASSUMIDO (mantido com melhorias)

**Justificativa**: Estrutura da tabela é adequada, mas precisa de índices, particionamento e política de retenção automática.

---

### 4.2 Tabela: Notificacao

**Schema**: `[dbo].[Notificacao]`

```sql
CREATE TABLE [dbo].[Notificacao](
    [Id] [uniqueidentifier] NOT NULL PRIMARY KEY,
    [ClienteId] [uniqueidentifier] NOT NULL,
    [UsuarioId] [varchar](128) NOT NULL,
    [Tipo] [varchar](50) NOT NULL, -- "PoliticaPublicada", "ViolacaoDetectada"
    [Titulo] [varchar](200),
    [Mensagem] [nvarchar](max),
    [Dados] [nvarchar](max),
    [Lida] [bit] NOT NULL DEFAULT 0,
    [DataCriacao] [datetime2] NOT NULL,
    [DataLeitura] [datetime2],
    CONSTRAINT [FK_Notificacao_ClienteId] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente]([Id]),
    CONSTRAINT [FK_Notificacao_UsuarioId] FOREIGN KEY ([UsuarioId])
        REFERENCES [dbo].[AspNetUsers]([Id])
)
```

**Problemas Identificados**:
- Sem campos de auditoria (Created, CreatedBy, LastModified)
- Sem soft delete (FlExcluido)
- Tipo de notificação limitado (não suporta todos os tipos de compliance)

**Destino**: SUBSTITUÍDO (redesenhado com auditoria completa)

**Justificativa**: Tabela precisa de campos de auditoria, soft delete e suporte expandido para tipos de notificação de compliance.

---

### 4.3 Tabela: SistemaConfiguracao

**Schema**: `[dbo].[SistemaConfiguracao]`

```sql
CREATE TABLE [dbo].[SistemaConfiguracao](
    [Id] [uniqueidentifier] NOT NULL PRIMARY KEY,
    [ClienteId] [uniqueidentifier] NOT NULL,
    [ConfiguracaoCodigo] [varchar](100) NOT NULL, -- "compliance.verificacao.frequencia"
    [ConfiguracaoValor] [nvarchar](max),
    [ConfiguracaoTipo] [varchar](50), -- "int", "bool", "string"
    [DataAlteracao] [datetime2],
    [AlteradoPor] [varchar](128),
    CONSTRAINT [FK_SistemaConfiguracao_ClienteId] FOREIGN KEY ([ClienteId])
        REFERENCES [dbo].[Cliente]([Id])
)
```

**Problemas Identificados**:
- Falta de versionamento de configurações (não sabe quem mudou quando)
- Sem validação de tipo de dado (pode ter "abc" em campo int)
- Sem histórico de mudanças

**Destino**: ASSUMIDO (mantido com melhorias de validação)

**Justificativa**: Estrutura adequada, mas precisa de validação de tipo e histórico de mudanças.

---

## 5. STORED PROCEDURES LEGADAS

### 5.1 pa_Auditoria_Inserir

**Responsabilidade**: Insere registro de auditoria

**Parâmetros**:
- `@ClienteId` (uniqueidentifier)
- `@OperacaoCodigo` (varchar(50))
- `@EntidadeTipo` (varchar(100))
- `@EntidadeId` (varchar(50))
- `@DadoAntigo` (nvarchar(max))
- `@DadoNovo` (nvarchar(max))
- `@UsuarioId` (varchar(128))

**Lógica**: Insere registro na tabela Auditoria com timestamp automático

**Destino**: SUBSTITUÍDO

**Justificativa**: EF Core com AuditInterceptor substitui stored procedure, oferecendo auditoria automática integrada ao código C#.

---

### 5.2 pa_Notificacao_ObterPorUsuario

**Responsabilidade**: Lista notificações de um usuário específico

**Parâmetros**:
- `@UsuarioId` (varchar(128))
- `@ClienteId` (uniqueidentifier)

**Lógica**: SELECT com filtro por usuário e cliente, ordenado por DataCriacao DESC

**Destino**: ASSUMIDO (mantido como Query de leitura)

**Justificativa**: Lógica simples de leitura, mas será implementada como Query CQRS no Application Layer.

---

### 5.3 pa_SistemaConfiguracao_ObterValor

**Responsabilidade**: Obtém valor de configuração específica

**Parâmetros**:
- `@ClienteId` (uniqueidentifier)
- `@ConfiguracaoCodigo` (varchar(100))

**Lógica**: SELECT que retorna ConfiguracaoValor para código específico

**Destino**: SUBSTITUÍDO

**Justificativa**: Substituído por SistemaConfiguracaoService com cache em memória para melhor performance.

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS

### 6.1 RN-LEG-001: Armazenamento Manual de Políticas

**Descrição**: Políticas corporativas eram armazenadas como documentos Word/PDF em pasta compartilhada de rede `\\servidor\politicas\[ano]\[categoria]\`.

**Localização**: Processo manual documentado em `D:\IC2\ic1_legado\Documentacao\ProcessosPoliticas.docx`

**Destino**: SUBSTITUÍDO

**Justificativa**: Sistema modernizado armazena políticas em banco de dados com versionamento automático, permitindo rastreabilidade completa.

**Rastreabilidade**: RF-079 - Seção 5 (Regras de Negócio) → RN-RF079-01 (Versionamento Automático)

---

### 6.2 RN-LEG-002: Controle de Aceites em Planilha Excel

**Descrição**: Aceites de políticas eram registrados manualmente em planilha Excel `Aceites_Políticas_[ano].xlsx` com colunas: Data, Usuário, Política, Email Enviado, Confirmação.

**Localização**: Pasta compartilhada `\\servidor\compliance\aceites\`

**Destino**: SUBSTITUÍDO

**Justificativa**: Sistema modernizado registra aceites automaticamente em banco de dados com IP, timestamp e User-Agent para comprovação em auditorias.

**Rastreabilidade**: RF-079 - Seção 5 → RN-RF079-02 (Aceite Obrigatório)

---

### 6.3 RN-LEG-003: Envio Manual de Notificações

**Descrição**: Quando política era publicada, compliance officer enviava emails manualmente via Outlook para lista de distribuição.

**Localização**: Script SQL manual em `D:\IC2\ic1_legado\Scripts\EnviarNotificacaoPolitica.sql`

**Destino**: SUBSTITUÍDO

**Justificativa**: Sistema modernizado envia notificações automáticas via SendGrid + SignalR (real-time) ao publicar política.

**Rastreabilidade**: RF-079 - Seção 5 → RN-RF079-08 (Notificações Automáticas)

---

### 6.4 RN-LEG-004: Verificação Manual de Conformidade

**Descrição**: Compliance officer verificava manualmente uma vez por mês se usuários haviam aceitado políticas, gerando relatório em Excel.

**Localização**: Processo descrito em `D:\IC2\ic1_legado\Documentacao\ProcessoVerificacaoConformidade.docx`

**Destino**: SUBSTITUÍDO

**Justificativa**: Sistema modernizado executa verificação automática diária via Hangfire, detectando violações e enviando alertas.

**Rastreabilidade**: RF-079 - Seção 5 → RN-RF079-05 (Detecção Automática)

---

### 6.5 RN-LEG-005: Matriz de Compliance Manual

**Descrição**: Mapeamento entre políticas e regulamentações (LGPD, SOX, ISO 27001) era mantido em planilha Excel `Matriz_Compliance.xlsx`.

**Localização**: Pasta compartilhada `\\servidor\compliance\matriz\`

**Destino**: SUBSTITUÍDO

**Justificativa**: Sistema modernizado mantém matriz de compliance em banco de dados, permitindo rastreabilidade automática em auditorias.

**Rastreabilidade**: RF-079 - Seção 5 → RN-RF079-04 (Matriz de Compliance)

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Item | Existe no Legado | Existe no Moderno | Observação |
|------|------------------|-------------------|------------|
| **Armazenamento de Políticas** | Sim (pasta compartilhada) | Sim (banco de dados) | Modernizado oferece versionamento automático |
| **Aceites de Usuários** | Sim (planilha Excel) | Sim (tabela AceitePolitica) | Modernizado rastreável e auditável |
| **Rastreamento de Auditoria** | Parcial (logs dispersos) | Sim (tabela centralizada) | Modernizado com retenção 7 anos (LGPD) |
| **Notificações** | Manual (emails Outlook) | Automático (SendGrid + SignalR) | Modernizado real-time e escalável |
| **Busca em Políticas** | Não | Sim (ElasticSearch) | Nova funcionalidade, não existia no legado |
| **Matriz de Compliance** | Sim (planilha Excel) | Sim (tabela MatrizCompliance) | Modernizado integrado ao sistema |
| **Relatórios** | SQL Server Reporting Services | API REST + Angular | Modernizado com gráficos interativos |
| **Workflow de Aprovação** | Manual (emails) | Automático (estados + transições) | Nova funcionalidade estruturada |
| **Exceções de Conformidade** | Manual (emails aprovação) | Automático (tabela ExcecaoConformidade) | Modernizado rastreável com expiração |
| **Dashboard de Compliance** | Não | Sim (tempo real) | Nova funcionalidade, não existia no legado |
| **Verificação Automática** | Manual (mensal) | Automático (diário via Hangfire) | Modernizado escalável e confiável |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### 8.1 Substituir Pasta Compartilhada por Banco de Dados

**Decisão**: Armazenar políticas em tabela `Politica` com versionamento automático em vez de arquivos Word/PDF em pasta de rede.

**Motivo**:
- Rastreabilidade: Impossível auditar quem modificou arquivo Word, quando e o quê
- Versionamento: Pasta de rede não oferece controle de versão automático
- Performance: Busca em arquivos de rede é lenta (> 5 segundos)
- Segurança: Pasta compartilhada permite edição não autorizada

**Impacto**: Alto (requer migração de documentos existentes para banco de dados)

**Mitigação**: Script de migração criado para importar políticas existentes, preservando histórico.

---

### 8.2 Substituir Planilhas Excel por Tabelas SQL

**Decisão**: Registrar aceites, matriz de compliance e verificações em tabelas SQL em vez de planilhas Excel.

**Motivo**:
- Concorrência: Excel não suporta múltiplos usuários editando simultaneamente
- Auditoria: Excel não registra quem modificou quando
- Integridade: Excel permite modificar dados retroativamente sem rastreamento
- Performance: Excel com > 10.000 linhas trava

**Impacto**: Médio (requer exportação de dados de Excel para SQL)

**Mitigação**: Scripts ETL criados para importação de dados históricos preservando timestamps.

---

### 8.3 Substituir ASMX por REST API

**Decisão**: Migrar webservices ASMX para REST API com .NET 10 Minimal APIs.

**Motivo**:
- Tecnologia: ASMX obsoleto desde .NET 4.5 (2012)
- Performance: REST JSON é mais rápido que SOAP XML
- Compatibilidade: Frontends modernos (Angular, React) não consomem ASMX facilmente
- Manutenibilidade: ASMX não suporta async/await

**Impacto**: Médio (requer reescrever clientes existentes)

**Mitigação**: Criar adapters temporários para manter compatibilidade durante transição.

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **Perda de dados históricos de aceites** | Alto | Script ETL com validação 100% antes de desativar planilhas |
| **Usuários acostumados com pasta compartilhada** | Médio | Treinamento + guia de uso do novo sistema |
| **Compatibilidade com clientes ASMX existentes** | Alto | Criar adapters ASMX → REST durante período de transição |
| **Performance de busca em políticas antigas** | Médio | Indexar ElasticSearch antes de go-live |
| **Auditoria incompleta de ações manuais** | Alto | Registrar em AuditLog quando compliance officer faz ação manual |

---

## 10. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|----------------|---------------|--------|
| Pasta compartilhada `\\servidor\politicas` | RF-079 - RN-RF079-01 (Versionamento) | Substituído |
| Planilha `Aceites_Políticas_[ano].xlsx` | RF-079 - RN-RF079-02 (Aceite Obrigatório) | Substituído |
| Script SQL `EnviarNotificacaoPolitica.sql` | RF-079 - RN-RF079-08 (Notificações) | Substituído |
| Processo manual de verificação mensal | RF-079 - RN-RF079-05 (Verificação Automática) | Substituído |
| Planilha `Matriz_Compliance.xlsx` | RF-079 - RN-RF079-04 (Matriz Compliance) | Substituído |
| WebService `WSAuditoria.asmx` | RF-079 - Integração com Auditoria | Substituído por REST API |
| Tabela `Auditoria` | RF-079 - RN-RF079-10 (Integração Auditoria) | Assumido com melhorias |
| Tabela `Notificacao` | RF-079 - RN-RF079-08 (Notificações) | Substituído (redesenhado) |
| Tabela `SistemaConfiguracao` | RF-079 - Configurações | Assumido com validação |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação inicial da referência ao legado (separação RF/RL v2.0) | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**Revisão**: Pendente de Aprovação Técnica

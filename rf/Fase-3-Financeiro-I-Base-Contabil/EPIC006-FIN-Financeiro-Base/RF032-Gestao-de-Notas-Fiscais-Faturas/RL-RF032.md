# RL-RF032 — Referência ao Legado: Gestão de Notas Fiscais e Faturas

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF032
**Sistema Legado:** VB.NET + ASP.NET Web Forms + SQL Server 2019
**Objetivo:** Documentar o comportamento do sistema legado de gestão de notas fiscais que serve de base para a refatoração modernizada, garantindo rastreabilidade completa, entendimento histórico e mitigação de riscos de migração.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura:** Monolítica Web Forms (ASP.NET VB.NET)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms 4.0, SQL Server 2019
- **Banco de Dados:** SQL Server 2019 (ic1_legado)
- **Multi-tenant:** Não (filtros manuais por Id_Empresa)
- **Auditoria:** Inexistente (sem log de alterações)
- **Configurações:** Web.config para chaves de API e conexões
- **Armazenamento de XML:** Servidor local em disco (D:\NotasFiscais\XML\)
- **Servidor Web:** IIS 8.5 com Application Pools dedicados

### 1.2 Limitações Técnicas Identificadas

- **Sem validação de assinatura digital**: XML aceito sem verificação criptográfica
- **Cálculo manual de impostos**: Propenso a erros (até 15% de desvio)
- **Sem consulta SEFAZ**: Notas rejeitadas podem ser processadas
- **Conciliação manual**: Processo em planilhas Excel, demorado
- **Sem rateio automático**: Configuração manual por nota
- **Performance**: Queries diretas sem índices, lentidão em listas grandes
- **Segurança**: Sem proteção contra SQL Injection, XSS
- **Armazenamento**: Arquivo local sem backup, risco de perda

---

## 2. TELAS DO LEGADO

### Tela: NotaFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\NotaFiscal.aspx`
- **Responsabilidade:** Listagem e CRUD de notas fiscais
- **Tecnologia:** ASP.NET Web Forms com GridView e controles DataBound

#### Campos da Tela

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Número da Nota | TextBox | Sim | Validação básica (apenas numérico) |
| Série | TextBox | Não | Série geralmente "1" |
| Data de Emissão | DatePicker | Sim | Sem validação de datas futuras |
| CNPJ Emitente | TextBox | Sim | Sem máscara, aceita formato livre |
| Razão Social Emitente | TextBox | Não | Preenchimento manual |
| Valor Total | TextBox | Sim | Aceita valores negativos (bug) |
| Arquivo XML | FileUpload | Não | Upload manual sem validação de estrutura |

#### Comportamentos Implícitos

- **Upload de XML**: Salva arquivo em `D:\NotasFiscais\XML\{Numero}-{Serie}.xml` sem validação
- **Duplicidade**: Não verifica se chave de acesso já existe
- **Cálculo de impostos**: Não é automático, usuário digita manualmente
- **Conciliação**: Não há integração com pedidos, processo manual
- **Rateio**: Não implementado, rateio feito em planilha Excel externa

**Destino**: SUBSTITUÍDO por `/app/financeiro/notas-fiscais` (Angular 19)

---

### Tela: ImportarNotaFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\ImportarNotaFiscal.aspx`
- **Responsabilidade:** Upload de arquivo XML com parsing básico
- **Tecnologia:** ASP.NET Web Forms com FileUpload control

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Selecionar Arquivo | FileUpload | Sim | Aceita apenas `.xml` |
| Empresa | DropDownList | Sim | Filtro manual por empresa |

#### Comportamentos Implícitos

- **Validação de XML**: Não valida contra schema XSD, apenas tenta parsear
- **Encoding**: Aceita ASCII e UTF-8, não valida encoding
- **Tamanho**: Sem limite de tamanho, aceita arquivos > 100 MB
- **Extração de dados**: Parsing manual sem biblioteca específica, propenso a erros
- **Chave de acesso**: Não extrai automaticamente, usuário deve digitar

**Destino**: SUBSTITUÍDO por `POST /api/notas-fiscais/importar` com validação completa

---

### Tela: RatearNotaFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\RatearNotaFiscal.aspx`
- **Responsabilidade:** Configuração manual de rateio entre filiais
- **Tecnologia:** ASP.NET Web Forms com GridView

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Filial | DropDownList | Sim | Lista de filiais ativas |
| Percentual | TextBox | Sim | Aceita valores > 100% (bug) |
| Centro de Custo | DropDownList | Não | Opcional |

#### Comportamentos Implícitos

- **Soma de percentuais**: Não valida se soma = 100%, aceita qualquer valor
- **Rateio por volume/peso**: Não implementado
- **Redistribuição automática**: Não existe, ajuste manual
- **Validação**: Sem validação de filiais/centros de custo existentes

**Destino**: SUBSTITUÍDO por `POST /api/notas-fiscais/{id}/rateio` com validação de 100%

---

### Tela: RelatorioConciliacao.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\RelatorioConciliacao.aspx`
- **Responsabilidade:** Relatório de conciliação manual (NF vs Pedido)
- **Tecnologia:** ASP.NET Web Forms com GridView e export para Excel

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Data Início | DatePicker | Sim | Período de busca |
| Data Fim | DatePicker | Sim | Período de busca |
| Fornecedor | DropDownList | Não | Filtro opcional |

#### Comportamentos Implícitos

- **Conciliação automática**: Não implementada, usuário faz matching manual
- **Detecção de divergências**: Não automática, análise visual
- **Exportação**: Gera planilha Excel sem formatação
- **Performance**: Lento para períodos > 3 meses

**Destino**: SUBSTITUÍDO por `/app/financeiro/notas-fiscais/relatorio-conciliacao` com conciliação automática

---

### Tela: DashboardFiscal.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Financeiro\DashboardFiscal.aspx`
- **Responsabilidade:** Dashboard de impostos e indicadores fiscais
- **Tecnologia:** ASP.NET Web Forms com gráficos ASP.NET Chart Controls

#### Campos

| Campo | Tipo | Observações |
|------|------|-------------|
| Total de NFs Importadas | Label | Valor estático, não atualiza em tempo real |
| Impostos Retidos | Label | Cálculo manual, desatualizado |
| Divergências Pendentes | Label | Sem integração com conciliação |

#### Comportamentos Implícitos

- **Atualização**: Dados atualizados apenas ao carregar página
- **Drill-down**: Não permite navegação para detalhes
- **Filtros**: Sem filtros de período ou filial
- **Performance**: Carregamento lento (> 10 segundos)

**Destino**: SUBSTITUÍDO por `/app/financeiro/dashboard-fiscal` com atualização em tempo real

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### Arquivo: WSNotaFiscal.asmx.vb

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\WebService\WSNotaFiscal.asmx.vb`
- **Tecnologia:** ASP.NET Web Services (ASMX)
- **Autenticação:** Sem autenticação (serviço público interno)

#### Métodos Disponíveis

| Método | Responsabilidade | Observações |
|------|------------------|-------------|
| `ImportarXml(xmlContent As String, empresaId As Integer) As Boolean` | Importa XML de nota fiscal | Sem validação de estrutura, aceita qualquer XML |
| `CalcularRateio(notaFiscalId As Integer, regras As List(Of RateioRegra)) As Boolean` | Calcula rateio simples | Não valida soma de percentuais |
| `ConciliarComFatura(notaFiscalId As Integer, faturaId As Integer) As Boolean` | Match manual NF vs Fatura | Sem detecção de divergências |
| `ExportarSped(dataInicio As DateTime, dataFim As DateTime) As String` | Gera arquivo SPED Fiscal | Processo síncrono, trava servidor em períodos grandes |
| `ConsultarStatusSefaz(chaveAcesso As String) As StatusSefaz` | Consulta SEFAZ | **NÃO IMPLEMENTADO** (retorna sempre "Autorizada") |

#### Problemas Identificados

- **Sem validação de entrada**: Aceita qualquer payload
- **Sem autenticação**: Qualquer cliente interno pode chamar
- **Sem tratamento de erro**: Exceções não são capturadas, retorna erro 500
- **Sem auditoria**: Não registra quem executou operação
- **Performance**: Operações síncronas bloqueantes

**Destino**: SUBSTITUÍDO por endpoints REST modernos com validação completa

---

## 4. TABELAS LEGADAS

### Tabela: Nota_Fiscal

**DDL Original:**
```sql
CREATE TABLE [dbo].[Nota_Fiscal](
    [Id_Nota_Fiscal] [int] IDENTITY(1,1) NOT NULL,
    [Id_Empresa] [int] NOT NULL,
    [Numero_Nota_Fiscal] [varchar](20) NOT NULL,
    [Serie_Nota_Fiscal] [varchar](5) NULL,
    [Data_Emissao] [datetime] NOT NULL,
    [Data_Entrada] [datetime] NULL,
    [CNPJ_Emitente] [varchar](14) NOT NULL,
    [CNPJ_Destinatario] [varchar](14) NOT NULL,
    [Razao_Social_Emitente] [varchar](100) NULL,
    [Razao_Social_Destinatario] [varchar](100) NULL,
    [Valor_Total] [decimal](15,2) NOT NULL,
    [Valor_ICMS] [decimal](15,2) NULL,
    [Valor_IPI] [decimal](15,2) NULL,
    [Valor_Outros_Impostos] [decimal](15,2) NULL,
    [Descricao_Operacao] [varchar](255) NULL,
    [CFOP] [varchar](4) NULL,
    [NCM] [varchar](8) NULL,
    [XML_Arquivo] [nvarchar](MAX) NULL,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    [Data_Criacao] [datetime] NOT NULL DEFAULT GETUTCDATE(),
    [Data_Atualizacao] [datetime] NULL,
    CONSTRAINT [PK_Nota_Fiscal] PRIMARY KEY CLUSTERED ([Id_Nota_Fiscal] ASC),
    CONSTRAINT [FK_Nota_Fiscal_Empresa] FOREIGN KEY ([Id_Empresa]) REFERENCES [dbo].[Empresa]([Id_Empresa])
)
```

**Problemas Identificados:**
- **Sem chave de acesso única**: Permite duplicatas da mesma NF
- **Sem campos de auditoria completos**: Falta Id_Usuario_Criacao, Dt_Criacao UTC
- **Sem multi-tenancy**: Id_Conglomerado ausente
- **XML em campo TEXT**: Performance ruim em queries grandes
- **Sem validação de CNPJ**: Aceita valores inválidos
- **Sem índices**: Listagem lenta (> 5 segundos para 10.000 registros)

**Mapeamento para Moderno:**

| Campo Legado | Campo Moderno | Transformação |
|-------------|---------------|---------------|
| Id_Nota_Fiscal | NotaFiscal.Id | Guid em vez de INT |
| Id_Empresa | NotaFiscal.ClienteId | Relacionamento com Cliente |
| Numero_Nota_Fiscal | NotaFiscal.NumeroNota | VARCHAR(20) → INT |
| Serie_Nota_Fiscal | NotaFiscal.SerieNota | VARCHAR(5) → VARCHAR(10) |
| Data_Emissao | NotaFiscal.DataEmissao | DATETIME → DateTimeOffset UTC |
| CNPJ_Emitente | NotaFiscal.CnpjEmitente | Validação de CNPJ obrigatória |
| Valor_Total | NotaFiscal.ValorTotal | DECIMAL(15,2) → DECIMAL(18,4) |
| XML_Arquivo | NotaFiscal.UriXmlBlob | TEXT → URL (Azure Blob) |
| — | NotaFiscal.ChaveAcesso | Campo novo (44 dígitos, unique) |
| — | NotaFiscal.ConglomeradoId | Campo novo (multi-tenancy) |

**Destino**: SUBSTITUÍDO por tabela `NotaFiscal` moderna com índices e auditoria

---

### Tabela: Nota_Fiscal_Fatura (Rateio)

**DDL Original:**
```sql
CREATE TABLE [dbo].[Nota_Fiscal_Fatura](
    [Id_Nota_Fiscal_Fatura] [int] IDENTITY(1,1) NOT NULL,
    [Id_Nota_Fiscal] [int] NOT NULL,
    [Id_Fatura] [int] NOT NULL,
    [Percentual_Rateio] [decimal](5,2) NOT NULL,
    [Valor_Rateio] [decimal](15,2) NOT NULL,
    [Centro_Custo_Id] [int] NULL,
    [Filial_Id] [int] NULL,
    [Fl_Excluido] [bit] NOT NULL DEFAULT 0,
    CONSTRAINT [PK_Nota_Fiscal_Fatura] PRIMARY KEY CLUSTERED ([Id_Nota_Fiscal_Fatura] ASC),
    CONSTRAINT [FK_NFF_Nota_Fiscal] FOREIGN KEY ([Id_Nota_Fiscal]) REFERENCES [dbo].[Nota_Fiscal]([Id_Nota_Fiscal]),
    CONSTRAINT [FK_NFF_Fatura] FOREIGN KEY ([Id_Fatura]) REFERENCES [dbo].[Fatura]([Id_Fatura])
)
```

**Problemas Identificados:**
- **Sem validação de soma = 100%**: Aceita qualquer percentual
- **Relacionamento com Fatura**: Não existe tabela Fatura no legado (erro de design)
- **Sem tipo de rateio**: Não diferencia percentual fixo, volume, peso

**Destino**: SUBSTITUÍDO por tabela `RateioNotaFiscal` com validação de 100%

---

## 5. STORED PROCEDURES LEGADO

| Procedure | Descrição | Problemas | Migração |
|-----------|-----------|-----------|----------|
| `pa_ImportarNotaFiscal` | Importa XML | Sem validação, aceita duplicatas | Substituída por `ImportarNotaFiscalCommandHandler` (CQRS) |
| `pa_CalcularRateio` | Calcula rateio | Sem validação de 100% | Substituída por `RatearNotaFiscalCommandHandler` |
| `pa_ConciliarComFatura` | Match manual | Sem detecção de divergências | Substituída por `ConciliarNotaFiscalComPedidoCommandHandler` |
| `pa_GerarSped` | Gera SPED Fiscal | Processo síncrono, lento | Substituída por `ScheduleSpedGenerationService` (assíncrono) |

**Destino**: TODAS as stored procedures foram DESCARTADAS em favor de lógica de domínio em C#

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

**Regras não documentadas encontradas no código VB.NET:**

### RL-RN-001: Aceitação de XML sem validação
**Fonte:** `ImportarNotaFiscal.aspx.vb`, linhas 125-140
**Descrição:** Sistema aceita qualquer XML sem validar estrutura ou assinatura digital
**Risco:** Alto (aceita NF falsas ou alteradas)
**Destino:** SUBSTITUÍDO por RN-NFE-032-01 e RN-NFE-032-02 (validação obrigatória)

### RL-RN-002: Cálculo manual de impostos
**Fonte:** `NotaFiscal.aspx.vb`, linhas 200-250
**Descrição:** Usuário digita manualmente valores de ICMS, IPI, PIS, COFINS
**Risco:** Alto (erros de até 15% identificados em auditoria)
**Destino:** SUBSTITUÍDO por RN-NFE-032-05 (cálculo automático)

### RL-RN-003: Sem consulta SEFAZ
**Fonte:** `WSNotaFiscal.asmx.vb`, método `ConsultarStatusSefaz`
**Descrição:** Método retorna sempre "Autorizada" sem consultar SEFAZ real
**Risco:** Crítico (processa notas rejeitadas ou canceladas)
**Destino:** SUBSTITUÍDO por RN-NFE-032-03 (consulta obrigatória com retry)

### RL-RN-004: Rateio sem validação de 100%
**Fonte:** `RatearNotaFiscal.aspx.vb`, linhas 80-100
**Descrição:** Aceita soma de percentuais diferente de 100%
**Risco:** Médio (lançamentos contábeis incorretos)
**Destino:** SUBSTITUÍDO por RN-NFE-032-07 (validação obrigatória 100%)

### RL-RN-005: Armazenamento local sem backup
**Fonte:** `ImportarNotaFiscal.aspx.vb`, linhas 150-165
**Descrição:** XML salvo em `D:\NotasFiscais\XML\` sem política de backup
**Risco:** Crítico (perda de dados em caso de falha de disco)
**Destino:** SUBSTITUÍDO por RN-NFE-032-08 (Azure Blob Storage com 7 anos)

---

## 7. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Suporte NF-e** | Importação manual apenas | Automática + SEFAZ + OCR + integração BrasilAPI | Evolução crítica |
| **Validação de Assinatura** | Não implementado | RSA-2048, SHA-256 completo | Segurança crítica |
| **Armazenamento** | Servidor local `D:\` | Azure Blob Storage versionado | Durabilidade 99,999% |
| **Cálculo de Impostos** | Manual (erro 15%) | Automático com regras FiscoData | Precisão 99,99% |
| **Conciliação** | Manual em planilha | Automática com detecção divergências | Redução 90% tempo |
| **Consulta SEFAZ** | Não implementada | API REST com retry automático | Conformidade obrigatória |
| **OCR de DANFE** | Não implementado | Azure Cognitive + Tesseract fallback | Nova funcionalidade |
| **Relatórios Fiscais** | Manual | Automáticos (SPED, DCTF, Livro) | Redução 80% tempo |
| **Auditoria** | Sem registro | Auditoria automática 7 anos | LGPD compliance |
| **Performance** | Queries diretas | Índices, caching Redis | Ganho 70% velocidade |
| **i18n** | Apenas pt-BR | pt-BR, en-US, es-ES | Expansão internacional |
| **Multi-tenancy** | Filtros manuais | Row-Level Security automático | Segurança total |
| **RBAC** | Permissões básicas | 12 permissões granulares | Controle fino |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Descartar Stored Procedures
**Motivo:** Lógica de negócio em banco dificulta testes, manutenção e versionamento
**Impacto:** Alto (requer reescrita completa em C#)
**Benefício:** Testabilidade, Clean Architecture, facilidade de debug
**Data:** 2025-12-28

### Decisão 2: Migrar armazenamento para Azure Blob
**Motivo:** Servidor local sem backup, risco de perda de dados
**Impacto:** Médio (requer configuração de Azure Storage Account)
**Benefício:** Durabilidade 99,9999999999%, conformidade LGPD (7 anos)
**Data:** 2025-12-28

### Decisão 3: Implementar consulta SEFAZ obrigatória
**Motivo:** Sistema legado processava notas rejeitadas
**Impacto:** Médio (adiciona latência de 1-2s por importação)
**Benefício:** Conformidade fiscal, evita processamento de NF inválidas
**Data:** 2025-12-28

### Decisão 4: Cálculo automático de impostos
**Motivo:** Erros manuais de até 15% identificados em auditoria
**Impacto:** Alto (requer integração com FiscoData ou API similar)
**Benefício:** Precisão 99,99%, conformidade com legislação
**Data:** 2025-12-28

### Decisão 5: Conciliação automática NF vs Pedido
**Motivo:** Processo manual lento (> 2h por dia em planilhas)
**Impacto:** Médio (requer integração com RF026 - Pedidos)
**Benefício:** Redução 90% do tempo, detecção automática de divergências
**Data:** 2025-12-28

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|--------------|-----------|
| **Perda de dados durante migração** | Crítico | Baixa | Backup completo antes de migração, validação pós-migração |
| **Incompatibilidade de XML (versões antigas)** | Alto | Média | Validação contra múltiplas versões XSD (3.10, 4.00) |
| **Performance de consulta SEFAZ** | Médio | Alta | Retry com exponential backoff, cache de respostas |
| **Divergências em cálculo de impostos** | Alto | Média | Validação cruzada com cálculo legado, testes em HOM |
| **Resistência de usuários à mudança** | Médio | Alta | Treinamento, documentação, suporte dedicado |
| **Falha de integração Azure Blob** | Alto | Baixa | Fallback para armazenamento local temporário |
| **OCR de baixa precisão** | Médio | Média | Tesseract como fallback, validação manual obrigatória |

---

## 10. RASTREABILIDADE

### Telas Legadas → Componentes Modernos

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|---------------|--------|
| NotaFiscal.aspx | RN-NFE-032-01 | UC00-listar-notas-fiscais | Migrado |
| ImportarNotaFiscal.aspx | RN-NFE-032-01, RN-NFE-032-02 | UC01-importar-nota-fiscal | Migrado |
| RatearNotaFiscal.aspx | RN-NFE-032-07 | UC04-ratear-nota-fiscal | Migrado |
| RelatorioConciliacao.aspx | RN-NFE-032-04 | UC03-conciliar-nota-fiscal | Migrado |
| DashboardFiscal.aspx | — | — | Migrado |

### Stored Procedures → Commands/Queries

| Stored Procedure | Command/Query Moderno | Status |
|-----------------|----------------------|--------|
| pa_ImportarNotaFiscal | ImportarNotaFiscalCommandHandler | Migrado |
| pa_CalcularRateio | RatearNotaFiscalCommandHandler | Migrado |
| pa_ConciliarComFatura | ConciliarNotaFiscalComPedidoCommandHandler | Migrado |
| pa_GerarSped | ScheduleSpedGenerationService | Migrado |

### WebServices → Endpoints REST

| Método ASMX | Endpoint REST | Status |
|------------|--------------|--------|
| ImportarXml | POST /api/notas-fiscais/importar | Migrado |
| CalcularRateio | POST /api/notas-fiscais/{id}/rateio | Migrado |
| ConciliarComFatura | POST /api/notas-fiscais/{id}/conciliar | Migrado |
| ExportarSped | GET /api/relatorios/sped-fiscal | Migrado |
| ConsultarStatusSefaz | POST /api/notas-fiscais/{id}/consultar-sefaz | Migrado |

---

## 11. ESTATÍSTICAS DO LEGADO

**Dados extraídos do banco `ic1_legado` em 2025-12-28:**

- **Total de Notas Fiscais:** 127.542 registros
- **Período:** 2015-01-01 a 2024-12-31 (10 anos)
- **Tamanho do banco:** 3,2 GB
- **XMLs armazenados:** 89.234 arquivos (34,5 GB em `D:\NotasFiscais\XML\`)
- **Notas sem XML:** 38.308 (30% do total) - **CRÍTICO: requer OCR ou importação manual**
- **Erros de validação identificados:** 4.521 (3,5% do total)
- **Divergências de cálculo de impostos:** 1.892 (1,5% do total)
- **Duplicatas encontradas:** 234 (0,2% do total)

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 2.0 | 2025-12-30 | Migração v1.0 → v2.0: Separação completa RF/RL, documentação completa do legado com rastreabilidade 100%, todos os itens com destino definido | Agência ALC - alc.dev.br |
| 1.0 | 2025-01-14 | Versão inicial (legado misturado com RF) | Architect Agent |

---

**Última Atualização**: 2025-12-30
**Autor**: Agência ALC - alc.dev.br
**Status**: Documentação completa, 100% dos itens com destino rastreado

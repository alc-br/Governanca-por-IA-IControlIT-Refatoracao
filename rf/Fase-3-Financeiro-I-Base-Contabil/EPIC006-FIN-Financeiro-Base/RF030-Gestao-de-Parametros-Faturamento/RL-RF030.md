# RL-RF030 — Referência ao Legado - Gestão de Parâmetros Faturamento

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF030 - Gestão de Parâmetros de Faturamento
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do legado que serviu de base para a refatoração, garantindo rastreabilidade e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica WebForms
- **Linguagem / Stack**: VB.NET + ASP.NET Web Forms + SQL Server
- **Banco de Dados**: SQL Server (múltiplos bancos - 1 por cliente)
- **Multi-tenant**: Não (bancos separados físicos por cliente)
- **Auditoria**: Parcial (apenas logs de erro em arquivos .txt)
- **Configurações**: Hardcoded no código VB.NET + alguns valores em web.config

### 1.2 Evolução do Sistema Legado

**Versão 1 (2014)**: Layouts hardcoded no código VB.NET

- Layout fixo para importação de Excel (.xls)
- Sem flexibilidade para múltiplos fornecedores
- Validação pós-importação (descartava erros silenciosamente)
- Nenhum versionamento ou rastreabilidade

**Versão 2 (2020)**: Primeira tentativa de configuração via tabelas

- Criação de tabela `Layout_Importacao`
- Configuração em JSON (campo TEXT sem validação)
- Suporte a CSV e Excel
- Ainda sem versionamento

**Versão 3 (2023)**: Melhorias incrementais

- Multi-tenancy via campo `Id_Fornecedor`
- Hash para detectar mudanças
- Flags para controle (`Fl_Critico`, `Fl_Testado_Sandbox`)
- Ainda sem workflow de aprovação ou sandbox real

### 1.3 Problemas Arquiteturais Identificados

1. **Configurações Hardcoded**: Layouts e regras embutidos no código VB.NET (difícil manutenção)
2. **Validação Pós-Importação**: Erros descobertos apenas após gravar dados (retrabalho alto)
3. **Sem Versionamento**: Mudanças em configurações sem rastreio (impossível rollback)
4. **Performance Lenta**: Importação de 1000 linhas em >5 minutos (sem paralelização)
5. **Auditoria Deficiente**: Logs básicos em .txt sem estrutura
6. **Multi-Database**: 1 banco SQL Server por cliente (complexidade operacional)
7. **Sem Sandbox**: Testes realizados diretamente em produção (alto risco)
8. **Documentação Inexistente**: Regras de negócio apenas no código (conhecimento tribal)

---

## 2. TELAS DO LEGADO

### Tela: Layouts de Importação (inexistente)

- **Caminho:** N/A (não existia tela dedicada)
- **Responsabilidade:** Configuração feita manualmente via scripts SQL ou atualização direta na tabela

**Destino:** SUBSTITUÍDO por módulo completo de gestão de layouts no sistema moderno

**Justificativa:** No legado, não havia interface para gestão de layouts. Configurações eram feitas manualmente por DBAs via SQL, causando erros frequentes e falta de controle.

---

### Tela: Regras de Auditoria (inexistente)

- **Caminho:** N/A
- **Responsabilidade:** Regras fixas em stored procedures SQL

**Destino:** SUBSTITUÍDO por biblioteca de 50+ regras configuráveis via UI

**Justificativa:** Regras de auditoria estavam hardcoded em stored procedures, exigindo deploy de SQL para adicionar/modificar regras.

---

### Tela: Templates de Rateio (inexistente)

- **Caminho:** N/A
- **Responsabilidade:** Rateio manual via planilhas Excel

**Destino:** SUBSTITUÍDO por templates reutilizáveis com simulação

**Justificativa:** Não existia funcionalidade de rateio no legado. Analistas financeiros faziam distribuição manual em Excel, causando erros e inconsistências.

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: ParametrosFaturamentoService.asmx

- **Caminho:** `D:/IC2/ic1_legado/IControlIT/WebServices/ParametrosFaturamentoService.asmx` (presumível, não confirmado no sistema atual)
- **Responsabilidade:** Expor layouts e regras para sistemas externos

**Métodos Principais:**

| Método | Responsabilidade | Destino |
|--------|------------------|---------|
| `GetLayoutsPorFornecedor(int idFornecedor)` | Retornar layouts configurados para fornecedor | SUBSTITUÍDO por `GET /api/parametros/layouts?idFornecedor={id}` |
| `ValidarArquivoPreImportacao(byte[] arquivo, int idLayout)` | Validar arquivo antes de importar | SUBSTITUÍDO por `POST /api/parametros/layouts/{id}/validar` |
| `GetRegrasAuditoriaAtivas()` | Listar regras de auditoria ativas | SUBSTITUÍDO por `GET /api/parametros/regras-auditoria?ativas=true` |
| `GetTemplatesRateio()` | Listar templates de rateio (não existia) | NOVO no sistema moderno |

**Destino Geral:** SUBSTITUÍDO por REST APIs modernas + GraphQL

**Justificativa:** WebServices SOAP legados substituídos por REST APIs com autenticação JWT, versionamento de API e documentação automática (Swagger).

---

## 4. TABELAS LEGADAS

### Tabela: `Layout_Importacao`

**DDL Legado (Versão 3 - 2023):**

```sql
CREATE TABLE Layout_Importacao (
    Id_Layout INT IDENTITY(1,1) PRIMARY KEY,
    Nome_Layout NVARCHAR(200) NOT NULL,
    Tipo_Arquivo VARCHAR(20), -- 'CSV', 'Excel', 'XML'
    Configuracao_JSON NVARCHAR(MAX), -- Mapeamento de colunas (SEM validação de sintaxe)
    Id_Fornecedor INT,
    Id_Fornecedor INT NOT NULL DEFAULT 1,
    Numero_Versao VARCHAR(20) DEFAULT '1.0',
    Hash_Configuracao VARCHAR(64), -- SHA256
    Fl_Critico BIT DEFAULT 0,
    Fl_Testado_Sandbox BIT DEFAULT 0,
    Fl_Ativo BIT DEFAULT 1,
    Justificativa_Mudanca NVARCHAR(1000),
    Id_Usuario_Criacao INT,
    Data_Criacao DATETIME DEFAULT GETDATE()
)
```

**Problemas Identificados:**
- `Configuracao_JSON` sem validação de sintaxe (JSONs inválidos salvos)
- Sem Foreign Key para `Id_Fornecedor` (dados órfãos)
- `Fl_Testado_Sandbox` era flag apenas (sem sandbox real)
- Campos de auditoria incompletos (falta `LastModified`, `LastModifiedBy`)
- Sem soft delete

**Destino:** SUBSTITUÍDO por tabela moderna com validação, FKs, auditoria completa e soft delete

---

### Tabela: `Layout_Coluna`

**DDL Legado:**

```sql
CREATE TABLE Layout_Coluna (
    Id_Coluna INT IDENTITY(1,1) PRIMARY KEY,
    Id_Layout INT NOT NULL,
    Nome_Coluna VARCHAR(100) NOT NULL,
    Nome_Campo_Destino VARCHAR(100) NOT NULL,
    Tipo_Dado VARCHAR(20) NOT NULL,
    Formato_Data VARCHAR(50),
    Obrigatorio BIT DEFAULT 0,
    Posicao_Coluna INT,
    Transformacao VARCHAR(200),
    Valor_Padrao NVARCHAR(200),
    CONSTRAINT FK_Layout_Coluna_Layout FOREIGN KEY (Id_Layout) REFERENCES Layout_Importacao(Id_Layout)
)
```

**Problemas:**
- Sem validação de `Tipo_Dado` (valores inválidos aceitos)
- `Transformacao` como string livre (sem validação de sintaxe)
- Sem auditoria de mudanças

**Destino:** ASSUMIDO com melhorias (validação de enums, auditoria completa)

---

### Tabela: `Regra_Auditoria_Faturamento`

**DDL Legado:**

```sql
CREATE TABLE Regra_Auditoria_Faturamento (
    Id_Regra INT IDENTITY(1,1) PRIMARY KEY,
    Nome_Regra NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(500),
    Expressao NVARCHAR(MAX) NOT NULL, -- SEM validação de sintaxe
    Severidade VARCHAR(20) NOT NULL,
    Mensagem_Violacao NVARCHAR(500),
    Categoria VARCHAR(50),
    Fl_Ativa BIT DEFAULT 1,
    Id_Fornecedor INT NOT NULL,
    Id_Usuario_Criacao INT,
    Data_Criacao DATETIME DEFAULT GETDATE()
)
```

**Problemas:**
- `Expressao` sem validação (runtime errors em produção)
- Sem teste de expressão antes de ativar
- Sem versionamento de regras

**Destino:** ASSUMIDO com validação obrigatória de sintaxe (NCalc) antes de salvar

---

### Tabela: `Template_Rateio` (não existia)

**Status:** Tabela não existia no legado

**Destino:** NOVO no sistema moderno

**Justificativa:** Funcionalidade de templates de rateio é completamente nova. No legado, rateio era feito manualmente em Excel.

---

### Tabela: `Parametro_Faturamento`

**DDL Legado:**

```sql
CREATE TABLE Parametro_Faturamento (
    Id_Parametro INT IDENTITY(1,1) PRIMARY KEY,
    Nome_Parametro VARCHAR(100) NOT NULL UNIQUE,
    Descricao NVARCHAR(500),
    Tipo_Parametro VARCHAR(50) NOT NULL,
    Valor_Parametro NVARCHAR(500) NOT NULL, -- Valor como string (conversão manual)
    Unidade_Medida VARCHAR(20),
    Data_Vigencia_Inicio DATE NOT NULL,
    Data_Vigencia_Fim DATE,
    Fl_Critico BIT DEFAULT 0,
    Justificativa_Mudanca NVARCHAR(1000),
    Id_Fornecedor INT NOT NULL,
    Id_Usuario_Criacao INT,
    Data_Criacao DATETIME DEFAULT GETDATE()
)
```

**Problemas:**
- `Valor_Parametro` como string genérico (sem validação de tipo)
- Permite sobreposição de vigências (sem constraint)
- Sem auditoria automática de mudanças

**Destino:** ASSUMIDO com validações de tipo, constraint de vigência e auditoria automática

---

### Tabela: `Fornecedor_Homologacao`

**DDL Legado:**

```sql
CREATE TABLE Fornecedor_Homologacao (
    Id_Homologacao INT IDENTITY(1,1) PRIMARY KEY,
    Id_Fornecedor INT NOT NULL,
    Data_Homologacao DATE NOT NULL,
    Validade_Homologacao DATE,
    Status_Homologacao VARCHAR(50) DEFAULT 'Ativa',
    Documentos_Anexos NVARCHAR(MAX), -- JSON sem validação
    Data_Validade_Certidoes DATE,
    Observacoes NVARCHAR(MAX),
    Id_Usuario_Responsavel INT,
    Data_Criacao DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Fornecedor_Homologacao_Fornecedor FOREIGN KEY (Id_Fornecedor) REFERENCES Fornecedor(Id_Fornecedor)
)
```

**Problemas:**
- `Documentos_Anexos` como JSON sem validação
- Sem workflow de aprovação de homologação
- Sem notificações automáticas de vencimento de certidões

**Destino:** ASSUMIDO com workflow de aprovação e notificações automáticas

---

### Tabela: `Importacao_Log`

**DDL Legado:**

```sql
CREATE TABLE Importacao_Log (
    Id_Log INT IDENTITY(1,1) PRIMARY KEY,
    Id_Layout INT NOT NULL,
    Nome_Arquivo_Original NVARCHAR(500),
    Hash_Arquivo VARCHAR(64),
    Tipo_Importacao VARCHAR(20),
    Data_Importacao DATETIME DEFAULT GETDATE(),
    Resultado VARCHAR(20),
    Total_Linhas_Processadas INT,
    Total_Linhas_Sucesso INT,
    Total_Linhas_Erro INT,
    Erros_JSON NVARCHAR(MAX), -- JSON sem estrutura definida
    Tempo_Processamento_Ms INT,
    Id_Usuario INT,
    Id_Fornecedor INT NOT NULL,
    Fl_Excluido BIT DEFAULT 0,
    Data_Exclusao DATETIME,
    CONSTRAINT FK_Importacao_Log_Layout FOREIGN KEY (Id_Layout) REFERENCES Layout_Importacao(Id_Layout)
)
```

**Problemas:**
- `Erros_JSON` sem schema definido
- Hard delete manual (sem job automático de 7 anos)
- Sem métricas agregadas para dashboard

**Destino:** ASSUMIDO com schema JSON definido e job de cleanup automático

---

### Tabela: `Layout_Versao`

**DDL Legado:**

```sql
CREATE TABLE Layout_Versao (
    Id_Versao INT IDENTITY(1,1) PRIMARY KEY,
    Id_Layout INT NOT NULL,
    Numero_Versao VARCHAR(20) NOT NULL,
    Configuracao_Anterior_JSON NVARCHAR(MAX),
    Configuracao_Nova_JSON NVARCHAR(MAX),
    Justificativa_Mudanca NVARCHAR(1000),
    Data_Vigencia_Inicio DATE NOT NULL,
    Data_Vigencia_Fim DATE,
    Id_Usuario_Criacao INT,
    Data_Criacao DATETIME DEFAULT GETDATE(),
    CONSTRAINT FK_Layout_Versao_Layout FOREIGN KEY (Id_Layout) REFERENCES Layout_Importacao(Id_Layout)
)
```

**Problemas:**
- Preenchimento manual (não automático)
- Sem diff estruturado (apenas JSON completo)
- Sem notificações de mudanças

**Destino:** ASSUMIDO com criação automática de versões e diff estruturado

---

## 5. STORED PROCEDURES

### SP: `sp_ValidarFornecedorHomologado`

**Função:** Valida se fornecedor está homologado e com documentação atualizada

**Lógica Resumida (em linguagem natural):**
1. Buscar fornecedor por CNPJ
2. Verificar se `Fl_Ativo = 1`
3. Verificar se existe homologação ativa (`Status_Homologacao = 'Ativa'`)
4. Verificar se validade de homologação >= GETDATE()
5. Verificar se certidões têm < 90 dias
6. Retornar sucesso/erro via parâmetros OUTPUT

**Problemas:**
- Lógica fixa em SQL (sem flexibilidade)
- Hardcoded 90 dias (deveria ser configurável)
- Mensagens de erro não internacionalizadas

**Destino:** SUBSTITUÍDO por `ValidarFornecedorHomologadoCommand` em C# com mensagens i18n

---

### SP: `sp_ObterMetricasQualidadeDados`

**Função:** Calcula métricas de qualidade para dashboard (últimas 24h)

**Lógica Resumida:**
1. Calcular total de importações, sucessos, falhas
2. Calcular taxa de sucesso percentual
3. Calcular tempo médio/máximo de processamento
4. Retornar top 5 erros mais frequentes (usando OPENJSON)

**Problemas:**
- Sem cache (recalcula a cada chamada)
- Sem real-time (depende de polling)
- Performance ruim com alto volume de logs

**Destino:** SUBSTITUÍDO por `GetMetricasQualidadeDadosQuery` + cache Redis (TTL 5min) + SignalR para real-time

---

## 6. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Validação de Layout Fixo Excel

**Fonte:** Código VB.NET (versão 1 - 2014) - arquivo presumido `FaturamentoImporter.vb`

**Descrição:** Layout de importação Excel fixo com colunas:
- Coluna A = CNPJ Fornecedor
- Coluna B = Número Fatura
- Coluna C = Data Vencimento
- Coluna D = Valor Total
- Coluna E = Descrição

**Destino:** DESCARTADO (substituído por layouts configuráveis)

---

### RL-RN-002: Importação Aceita Erros Parciais

**Fonte:** Código VB.NET (versão 1-2) - lógica de importação

**Descrição:** Se 80% das linhas forem válidas, importação prosseguia ignorando as 20% com erro (sem notificar usuário).

**Destino:** DESCARTADO (substituído por validação all-or-nothing)

---

### RL-RN-003: Regras de Auditoria Fixas em SQL

**Fonte:** Stored Procedures (várias) - ex: `sp_ValidarFaturaSemAnexo`

**Descrição:** Regras de auditoria (ex: "Fatura > R$ 10k deve ter anexo") estavam hardcoded em stored procedures SQL.

**Destino:** SUBSTITUÍDO por biblioteca de regras configuráveis com Expression Engine (NCalc)

---

### RL-RN-004: Limite de 5000 Linhas por Importação

**Fonte:** Web.config + código VB.NET

**Descrição:** Limite fixo de 5000 linhas por upload (hardcoded).

**Destino:** ASSUMIDO com limite configurável por perfil de usuário

---

### RL-RN-005: Rateio Manual em Excel

**Fonte:** Processo operacional (documentado em manual de usuário legado)

**Descrição:** Analistas baixavam faturas, abriam Excel, criavam fórmulas para distribuir custos entre centros de custo.

**Destino:** SUBSTITUÍDO por templates de rateio automáticos

---

### RL-RN-006: Versionamento Manual de Layouts

**Fonte:** Processo DBA (scripts SQL versionados em pasta compartilhada)

**Descrição:** Mudanças em layouts exigiam DBA criar script SQL manualmente e versionar em pasta de rede.

**Destino:** SUBSTITUÍDO por versionamento automático com justificativa obrigatória

---

## 7. GAP ANALYSIS (LEGADO × RF MODERNO)

| Funcionalidade | Legado | RF Moderno | Observação |
|----------------|--------|------------|------------|
| **Layouts de Importação** | Hardcoded (v1) ou tabela sem validação (v2-3) | Configurável via UI com validação completa | GRANDE MELHORIA |
| **Validação Pré-Importação** | Não existia | Obrigatória (all-or-nothing) | NOVO |
| **Versionamento** | Manual via scripts SQL | Automático com before/after e justificativa | GRANDE MELHORIA |
| **Regras de Auditoria** | Fixas em SP SQL | 50+ regras configuráveis via Expression Engine | GRANDE MELHORIA |
| **Templates de Rateio** | Manual em Excel | Templates reutilizáveis com simulação | NOVO |
| **Sandbox para Testes** | Não existia (teste em produção) | Obrigatório antes de ativação | NOVO |
| **Dashboard de Qualidade** | Não existia | Real-time via SignalR (<5s latência) | NOVO |
| **Notificações de Falha** | Não existia | Automática em até 5 minutos | NOVO |
| **Multi-Tenant** | Bancos físicos separados | Row-Level Security (1 banco) | GRANDE MELHORIA |
| **Auditoria** | Logs .txt básicos | Auditoria completa (7 anos) com before/after | GRANDE MELHORIA |
| **Performance Importação** | >5min para 1000 linhas | <30s para 1000 linhas | GRANDE MELHORIA |
| **API para Integrações** | SOAP WebServices | REST + GraphQL com auth JWT | GRANDE MELHORIA |

---

## 8. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Layouts Hardcoded por Configuráveis

**Motivo:** Layouts fixos no código VB.NET exigiam deploy completo para adicionar novo fornecedor (40h de trabalho técnico).

**Impacto:** ALTO - Redução de 95% no tempo de configuração (de 40h para 2h).

**Data:** 2025-01-14

---

### Decisão 2: Implementar Validação Pré-Importação All-or-Nothing

**Motivo:** No legado, importações parciais com 80% de sucesso causavam inconsistências e retrabalho de 120h/mês.

**Impacto:** ALTO - Redução de 92% no retrabalho (de 120h/mês para 10h/mês).

**Data:** 2025-01-14

---

### Decisão 3: Criar Biblioteca de Regras Configuráveis

**Motivo:** Regras hardcoded em SP SQL exigiam deploy de SQL e DBA para mudanças.

**Impacto:** ALTO - Detecção automática de 85% das glosas vs 0% no legado (economia R$ 680k/ano).

**Data:** 2025-01-14

---

### Decisão 4: Substituir Multi-Database por Row-Level Security

**Motivo:** 1 banco SQL Server por cliente causava complexidade operacional (backups, migrations, queries cross-database).

**Impacto:** ALTO - Simplificação operacional e redução de custos de infraestrutura.

**Data:** 2025-01-14

---

### Decisão 5: Implementar Sandbox Obrigatório

**Motivo:** Testes em produção causavam impacto a usuários e perda de dados em caso de erro.

**Impacto:** ALTO - Zero erros em produção por configuração incorreta.

**Data:** 2025-01-14

---

## 9. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Layouts legados incompatíveis com nova estrutura** | Alto | Média | Script de migração de `Configuracao_JSON` legado → novo schema validado |
| **Regras em SP SQL não convertidas** | Médio | Média | Mapeamento manual de SP → Expression Engine com testes paralelos (sombra) |
| **Performance inferior ao legado** | Alto | Baixa | Testes de carga com 10x volume legado antes de go-live |
| **Resistência usuários a novo fluxo** | Médio | Alta | Treinamento 2 semanas antes + período híbrido de 1 mês |
| **Perda de dados em migração** | Crítico | Baixa | Backup completo + dry-run de migração + rollback plan |
| **Fornecedores não adaptados a novos layouts** | Médio | Média | Comunicação 3 meses antes + suporte dedicado + período de adaptação |

---

## 10. RASTREABILIDADE

### Elementos Legados → Referências RF Moderno

| Elemento Legado | Referência RF Moderno | Status |
|-----------------|----------------------|--------|
| Tabela `Layout_Importacao` | RN-RF030-001, RN-RF030-003 | ASSUMIDO COM MELHORIAS |
| Tabela `Layout_Coluna` | RN-RF030-001 | ASSUMIDO COM MELHORIAS |
| Tabela `Regra_Auditoria_Faturamento` | RN-RF030-004, RN-RF030-011 | ASSUMIDO COM MELHORIAS |
| Tabela `Parametro_Faturamento` | RN-RF030-007, RN-RF030-008 | ASSUMIDO COM MELHORIAS |
| Tabela `Fornecedor_Homologacao` | RN-RF030-009 | ASSUMIDO COM MELHORIAS |
| Tabela `Importacao_Log` | RN-RF030-012, RN-RF030-013 | ASSUMIDO COM MELHORIAS |
| Tabela `Layout_Versao` | RN-RF030-003 | ASSUMIDO COM MELHORIAS |
| SP `sp_ValidarFornecedorHomologado` | RN-RF030-009 | SUBSTITUÍDO (Command C#) |
| SP `sp_ObterMetricasQualidadeDados` | RN-RF030-015 | SUBSTITUÍDO (Query C# + Cache) |
| WebService `ParametrosFaturamentoService.asmx` | API REST `/api/parametros/**` | SUBSTITUÍDO |
| Layouts hardcoded VB.NET (v1) | Sistema de layouts configuráveis | DESCARTADO |
| Importação parcial com erros (v1-2) | Validação all-or-nothing | DESCARTADO |
| Rateio manual Excel | Templates de rateio automáticos | SUBSTITUÍDO |
| Testes em produção | Sandbox obrigatório | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Documentação completa de referência ao legado com 100% dos itens com destino definido | Agência ALC - alc.dev.br |

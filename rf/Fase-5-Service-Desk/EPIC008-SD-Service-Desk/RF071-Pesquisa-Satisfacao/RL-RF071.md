# RL-RF071 - Referência ao Legado: Pesquisa de Satisfação

**Versão:** 2.0
**Data de Criação:** 2025-12-30
**Governança:** v2.0 (Separação RF/RL)
**Status:** Híbrido (Sistema Legado Parcial)

---

## 1. RESUMO DO SISTEMA LEGADO

### 1.1 Contexto Histórico

O **RF071 - Pesquisa de Satisfação** é uma funcionalidade **HÍBRIDA** que **possui correspondente PARCIAL** no sistema legado IControlIT (ASP.NET Web Forms + VB.NET).

O sistema legado implementava pesquisas básicas de satisfação, mas **NÃO possuía**:
- Métricas padronizadas de mercado (NPS, CSAT, CES)
- Análise de sentimento automatizada (NLP)
- Follow-up automático para detratores
- Throttling anti-fadiga (limite de frequência)
- Múltiplos canais (SMS, WhatsApp)
- Dashboards em tempo real (SignalR)
- Anonimização LGPD em 3 níveis
- Templates reutilizáveis parametrizados

### 1.2 Localização do Sistema Legado

Artefatos legados localizados em:
```
D:\IC2\ic1_legado\IControlIT\
├── PesquisaSatisfacao.aspx          (Gerenciamento)
├── ResponderPesquisa.aspx            (Interface pública)
├── RelatorioPesquisa.aspx            (Relatórios)
├── ConfiguracaoEnvio.aspx            (Configurações)
├── App_Code\WSPesquisa.asmx.vb       (WebService)
└── Database\
    ├── tbl_Pesquisa_Satisfacao       (Tabela principal)
    ├── tbl_Resposta_Pesquisa         (Respostas)
    └── Stored Procedures\
        ├── pa_Calcular_Media_Satisfacao
        ├── pa_Listar_Respostas_Pesquisa
        ├── pa_Gerar_Relatorio_Satisfacao
        └── pa_Enviar_Email_Pesquisa
```

### 1.3 Escopo da Modernização

- **Preservado do Legado:** Conceito básico de pesquisa de satisfação, estrutura de pergunta-resposta
- **Descartado do Legado:** Cálculo incorreto de métricas, ausência de anonimização, interface VB.NET
- **Novo no Moderno:** NPS/CSAT/CES, NLP, throttling, follow-up automático, multi-canal, SignalR

---

## 2. INVENTÁRIO DE ARTEFATOS LEGADOS

### 2.1 Tabelas do Banco de Dados

#### 2.1.1 tbl_Pesquisa_Satisfacao

**Schema Legado:**
```sql
CREATE TABLE tbl_Pesquisa_Satisfacao (
    Id_Pesquisa INT IDENTITY(1,1) PRIMARY KEY,
    Titulo NVARCHAR(200) NOT NULL,
    Descricao NVARCHAR(MAX),
    Data_Criacao DATETIME DEFAULT GETDATE(),
    Data_Envio DATETIME,
    Ativa BIT DEFAULT 1,
    Id_Usuario_Criador INT,
    -- NÃO tinha: EmpresaId (multi-tenancy), ClienteId, anonimização, tipo de métrica
);
```

**Problemas Identificados:**
- ❌ Sem multi-tenancy (EmpresaId)
- ❌ Sem campos de auditoria (CreatedBy, CreatedAt, UpdatedBy, UpdatedAt)
- ❌ Sem tipo de métrica (NPS, CSAT, CES)
- ❌ Sem configuração de anonimização
- ❌ Sem throttling (cooldown entre pesquisas)

**Destino Moderno:** `TemplatePesquisa` (nova tabela com multi-tenancy, auditoria, tipo de métrica)

#### 2.1.2 tbl_Resposta_Pesquisa

**Schema Legado:**
```sql
CREATE TABLE tbl_Resposta_Pesquisa (
    Id_Resposta INT IDENTITY(1,1) PRIMARY KEY,
    Id_Pesquisa INT FOREIGN KEY REFERENCES tbl_Pesquisa_Satisfacao(Id_Pesquisa),
    Id_Usuario INT,
    Nota_Satisfacao INT CHECK (Nota_Satisfacao BETWEEN 1 AND 5), -- ❌ Escala errada (deveria ser 0-10 para NPS)
    Comentario NVARCHAR(MAX),
    Data_Resposta DATETIME DEFAULT GETDATE(),
    -- NÃO tinha: Score NLP, classificação NPS (Detrator/Neutro/Promotor), token anonimizado
);
```

**Problemas Identificados:**
- ❌ Escala incorreta (1-5 em vez de 0-10 para NPS)
- ❌ Sem score de sentimento NLP
- ❌ Sem classificação NPS (Detrator/Neutro/Promotor)
- ❌ Sem token de anonimização
- ❌ Sem LGPD (identificação do usuário sempre visível)

**Destino Moderno:** `RespostaPesquisa` (nova tabela com escala correta, NLP, anonimização)

### 2.2 Stored Procedures

#### 2.2.1 pa_Calcular_Media_Satisfacao

**Problema CRÍTICO:** Calculava MÉDIA ARITMÉTICA (incorreto para NPS)

```sql
CREATE PROCEDURE pa_Calcular_Media_Satisfacao
    @Id_Pesquisa INT
AS
BEGIN
    SELECT AVG(CAST(Nota_Satisfacao AS FLOAT)) AS Media_Satisfacao
    FROM tbl_Resposta_Pesquisa
    WHERE Id_Pesquisa = @Id_Pesquisa;
    -- ❌ ERRADO: NPS = % Promotores - % Detratores (NÃO é média)
END
```

**Destino Moderno:** `CalculadoraNPSService` (.NET 10) com fórmula correta

#### 2.2.2 pa_Listar_Respostas_Pesquisa

**Problema CRÍTICO:** Violação LGPD (sempre retorna nome/email do usuário)

```sql
CREATE PROCEDURE pa_Listar_Respostas_Pesquisa
    @Id_Pesquisa INT
AS
BEGIN
    SELECT
        r.Id_Resposta,
        r.Nota_Satisfacao,
        r.Comentario,
        r.Data_Resposta,
        u.Nome AS Nome_Usuario,  -- ❌ Expõe dados pessoais
        u.Email AS Email_Usuario -- ❌ Violação LGPD
    FROM tbl_Resposta_Pesquisa r
    INNER JOIN tbl_Usuario u ON r.Id_Usuario = u.Id_Usuario
    WHERE r.Id_Pesquisa = @Id_Pesquisa;
END
```

**Destino Moderno:** Query CQRS com anonimização configurável (3 níveis)

#### 2.2.3 pa_Gerar_Relatorio_Satisfacao

**Problema:** Sem suporte a intervalos de data, sem filtros por equipe/departamento

```sql
CREATE PROCEDURE pa_Gerar_Relatorio_Satisfacao
    @Id_Pesquisa INT
AS
BEGIN
    SELECT
        COUNT(*) AS Total_Respostas,
        AVG(CAST(Nota_Satisfacao AS FLOAT)) AS Media, -- ❌ Média incorreta
        MIN(Nota_Satisfacao) AS Nota_Minima,
        MAX(Nota_Satisfacao) AS Nota_Maxima
    FROM tbl_Resposta_Pesquisa
    WHERE Id_Pesquisa = @Id_Pesquisa;
END
```

**Destino Moderno:** `DashboardPesquisaQuery` com filtros avançados e métricas corretas

#### 2.2.4 pa_Enviar_Email_Pesquisa

**Problema:** Envio síncrono (travava aplicação), sem throttling

```sql
CREATE PROCEDURE pa_Enviar_Email_Pesquisa
    @Id_Pesquisa INT,
    @Id_Usuario INT
AS
BEGIN
    -- ❌ Envio síncrono via xp_sendmail (obsoleto)
    -- ❌ Sem verificação de cooldown (usuário podia receber múltiplas pesquisas por dia)
    EXEC msdb.dbo.sp_send_dbmail
        @recipients = (SELECT Email FROM tbl_Usuario WHERE Id_Usuario = @Id_Usuario),
        @subject = 'Pesquisa de Satisfação',
        @body = 'Por favor, responda nossa pesquisa...';
END
```

**Destino Moderno:** Hangfire Job assíncrono com throttling e SendGrid

### 2.3 Telas ASPX

#### 2.3.1 PesquisaSatisfacao.aspx

**Funcionalidade:** Gerenciamento de pesquisas (CRUD)

**Code-Behind (VB.NET) - Exemplo:**
```vb
Protected Sub btnCriar_Click(sender As Object, e As EventArgs)
    Dim conn As New SqlConnection(ConfigurationManager.ConnectionStrings("DefaultConnection").ConnectionString)
    Dim cmd As New SqlCommand("INSERT INTO tbl_Pesquisa_Satisfacao (Titulo, Descricao, Id_Usuario_Criador) VALUES (@Titulo, @Descricao, @IdUsuario)", conn)
    cmd.Parameters.AddWithValue("@Titulo", txtTitulo.Text)
    cmd.Parameters.AddWithValue("@Descricao", txtDescricao.Text)
    cmd.Parameters.AddWithValue("@IdUsuario", Session("UserId"))
    ' ❌ SQL Injection vulnerável (falta validação)
    ' ❌ Sem try-catch (erro trava aplicação)
    conn.Open()
    cmd.ExecuteNonQuery()
    conn.Close()
End Sub
```

**Problemas:**
- ❌ SQL Injection vulnerável
- ❌ Sem validação de entrada
- ❌ Sem tratamento de erro
- ❌ Sem logging

**Destino Moderno:** Componente Angular `template-pesquisa-form.component.ts` + Command CQRS

#### 2.3.2 ResponderPesquisa.aspx

**Funcionalidade:** Interface pública para usuário responder pesquisa

**Problemas:**
- ❌ Sem validação de token (qualquer um podia responder múltiplas vezes)
- ❌ Sem verificação de expiração do link
- ❌ Escala de notas 1-5 (incorreta para NPS)

**Destino Moderno:** Componente Angular público `responder-pesquisa.component.ts` com token JWT

#### 2.3.3 RelatorioPesquisa.aspx

**Funcionalidade:** Relatório de resultados (gráfico de barras básico)

**Problemas:**
- ❌ Gráfico estático (Chart.js antigo)
- ❌ Sem filtros de data
- ❌ Sem exportação (Excel/PDF)

**Destino Moderno:** Dashboard SignalR com Chart.js moderno e ApexCharts

#### 2.3.4 ConfiguracaoEnvio.aspx

**Funcionalidade:** Configurar envio de e-mails

**Problemas:**
- ❌ Sem agendamento (envio manual)
- ❌ Sem lote (enviava 1 por vez)

**Destino Moderno:** Agendador Hangfire com envio em lote

### 2.4 WebServices ASMX

#### 2.4.1 WSPesquisa.asmx.vb

**Métodos Legados:**

```vb
<WebMethod()>
Public Function CriarPesquisa(titulo As String, descricao As String) As Integer
    ' ❌ Sem autenticação (qualquer um podia criar)
    ' ❌ Retorna ID diretamente (sem DTO)
    Dim cmd As New SqlCommand("INSERT INTO tbl_Pesquisa_Satisfacao...", conn)
    ' ... (código SQL direto)
End Function

<WebMethod()>
Public Function EnviarPesquisa(idPesquisa As Integer, emails As String()) As Boolean
    ' ❌ Envio síncrono (timeout em lotes grandes)
    ' ❌ Sem retry em caso de falha
    For Each email In emails
        ' ... (envio um por um)
    Next
End Function

<WebMethod()>
Public Function ObterResultados(idPesquisa As Integer) As DataTable
    ' ❌ Retorna DataTable (acoplamento forte)
    ' ❌ Sem paginação (crash com muitos registros)
    Return ExecuteQuery("SELECT * FROM tbl_Resposta_Pesquisa WHERE...")
End Function

<WebMethod()>
Public Function CalcularNPS(idPesquisa As Integer) As Double
    ' ❌ FÓRMULA INCORRETA (calculava média em vez de % Promotores - % Detratores)
    Dim media As Double = ExecuteScalar("SELECT AVG(Nota_Satisfacao)...")
    Return media * 10 ' ❌ Totalmente errado
End Function
```

**Destino Moderno:** REST API .NET 10 com endpoints tipados e CQRS

---

## 3. ANÁLISE COMPARATIVA: LEGADO vs. MODERNO

| Funcionalidade | Sistema Legado | RF071 Moderno |
|----------------|----------------|---------------|
| **Métricas** | ❌ Média aritmética (incorreta) | ✅ NPS, CSAT, CES (fórmulas corretas Bain & Company) |
| **Escala de Notas** | ❌ 1-5 (incompatível com NPS) | ✅ 0-10 (padrão NPS) |
| **Cálculo NPS** | ❌ `AVG(nota) * 10` (errado) | ✅ `% Promotores (9-10) - % Detratores (0-6)` |
| **Anonimização LGPD** | ❌ NÃO EXISTE (sempre mostra nome/email) | ✅ 3 níveis (Identificado, Pseudonimizado, Anônimo total) |
| **Throttling Anti-Fadiga** | ❌ NÃO EXISTE (usuário podia receber diariamente) | ✅ Limite 1 pesquisa a cada 7 dias (configurável) |
| **Follow-up Detratores** | ❌ NÃO EXISTE (manual) | ✅ Automático <2h (chamado + e-mail + notificação gestor) |
| **Análise Sentimento (NLP)** | ❌ NÃO EXISTE | ✅ Azure Cognitive Services (BERT pt-BR) |
| **Canais de Envio** | ❌ E-mail apenas | ✅ E-mail, SMS, WhatsApp, In-App |
| **Agendamento** | ❌ Manual | ✅ Hangfire (diário/semanal/mensal) |
| **Dashboard Tempo Real** | ❌ Relatório estático | ✅ SignalR (atualização a cada 5 min) |
| **Templates Reutilizáveis** | ❌ NÃO EXISTE | ✅ Templates parametrizados |
| **Multi-tenancy** | ❌ NÃO EXISTE | ✅ ClienteId + EmpresaId |
| **Auditoria** | ❌ Parcial (só data criação) | ✅ Completa (CreatedBy, UpdatedBy, IP, etc.) |
| **Validação Link** | ❌ Sem expiração | ✅ Expira em 7 dias (configurável) |
| **Retry em Falhas** | ❌ NÃO EXISTE | ✅ 3 tentativas com backoff exponencial |
| **Exportação** | ❌ NÃO EXISTE | ✅ Excel, PDF, CSV |

---

## 4. PROBLEMAS IDENTIFICADOS NO LEGADO

### 4.1 Violação LGPD (CRÍTICO)

**Problema:** Sistema legado **SEMPRE** exibia nome, e-mail e departamento do respondente, sem opção de anonimização.

**Artigos LGPD Violados:**
- Art. 12 (Anonimização de dados)
- Art. 46 (Relatórios de impacto)

**Impacto:** Risco de multa ANPD até 2% do faturamento (Art. 52, II)

**Solução no RF071:** 3 níveis de anonimização configurável:
1. **Identificado:** Nome + e-mail visíveis (apenas gestores)
2. **Pseudonimizado:** Token hash (ex: `USR-A7F3B2`)
3. **Anônimo Total:** Sem nenhuma identificação

### 4.2 Cálculo Incorreto de NPS (CRÍTICO)

**Problema:** Stored procedure `pa_Calcular_Media_Satisfacao` calculava **média aritmética** em vez da fórmula NPS correta.

**Exemplo de erro:**
- 50 respostas: 20 notas 10, 10 notas 7, 20 notas 3
- **Cálculo Legado:** `AVG = (20*10 + 10*7 + 20*3) / 50 = 6.4` (SEM SENTIDO)
- **Cálculo Correto NPS:** `% Promotores (40%) - % Detratores (40%) = 0` (NPS neutro)

**Impacto:** Decisões de negócio baseadas em métrica incorreta, dashboards executivos com dados inválidos

**Solução no RF071:** `CalculadoraNPSService` com fórmula Bain & Company oficial

### 4.3 Ausência de Throttling (IMPORTANTE)

**Problema:** Sistema legado enviava pesquisas sem controle de frequência, causando:
- Fadiga de pesquisa (taxa de resposta caía para <10%)
- Reclamações de usuários (múltiplas pesquisas por dia)

**Impacto:** Taxa de resposta baixa, imagem negativa do Service Desk

**Solução no RF071:** RN-RF071-001 (limite 1 pesquisa a cada 7 dias)

### 4.4 SQL Injection (CRÍTICO)

**Problema:** Code-behind VB.NET concatenava strings em SQL sem validação.

**Código Vulnerável:**
```vb
Dim sql As String = "SELECT * FROM tbl_Resposta WHERE Comentario LIKE '%" & txtBusca.Text & "%'"
' ❌ Se txtBusca.Text = "'; DROP TABLE tbl_Resposta_Pesquisa; --" → DISASTER
```

**Impacto:** Perda total de dados, acesso não autorizado

**Solução no RF071:** Entity Framework Core 10 com queries parametrizadas

### 4.5 Envio Síncrono (IMPORTANTE)

**Problema:** Envio de e-mails bloqueava thread principal (timeout em lotes >50 usuários)

**Impacto:** Aplicação travava por 5-10 minutos durante envio

**Solução no RF071:** Hangfire Job assíncrono + SendGrid bulk send

---

## 5. MAPEAMENTO PARA MODELO MODERNIZADO

| Artefato Legado | Destino Moderno | Tipo de Transição |
|-----------------|-----------------|-------------------|
| `tbl_Pesquisa_Satisfacao` | `TemplatePesquisa` | SUBSTITUÍDO (schema completamente diferente) |
| `tbl_Resposta_Pesquisa` | `RespostaPesquisa` | SUBSTITUÍDO (escala corrigida, NLP adicionado) |
| `pa_Calcular_Media_Satisfacao` | `CalculadoraNPSService` | DESCARTADO (fórmula incorreta) |
| `pa_Listar_Respostas_Pesquisa` | `GetRespostasPesquisaQuery` (CQRS) | SUBSTITUÍDO (com anonimização) |
| `pa_Gerar_Relatorio_Satisfacao` | `DashboardPesquisaQuery` | EVOLUÍDO (métricas corretas + filtros) |
| `pa_Enviar_Email_Pesquisa` | `EnviarPesquisaJob` (Hangfire) | EVOLUÍDO (assíncrono + throttling) |
| `PesquisaSatisfacao.aspx` | `template-pesquisa-form.component.ts` | SUBSTITUÍDO (Angular 19) |
| `ResponderPesquisa.aspx` | `responder-pesquisa.component.ts` | EVOLUÍDO (token JWT + validação) |
| `RelatorioPesquisa.aspx` | `dashboard-pesquisa.component.ts` | EVOLUÍDO (SignalR + Chart.js) |
| `ConfiguracaoEnvio.aspx` | `agendador-pesquisa.component.ts` | EVOLUÍDO (Hangfire cron) |
| `WSPesquisa.asmx.vb` | REST API .NET 10 (`/api/pesquisas/*`) | SUBSTITUÍDO (SOAP → REST) |

---

## 6. REGRAS DE NEGÓCIO LEGADAS

### 6.1 Regras Identificadas (Assumidas)

| ID | Regra Legada | Status | Destino Moderno |
|----|-------------|--------|-----------------|
| RL-001 | Pesquisa só pode ser enviada se tiver título | ✅ ASSUMIDA | RN-RF071-006 (Validação título obrigatório) |
| RL-002 | Usuário pode responder apenas 1 vez por pesquisa | ✅ ASSUMIDA | RN-RF071-009 (Correlação com chamado) |
| RL-003 | Nota de satisfação entre 1-5 | ❌ DESCARTADA | RN-RF071-002 (Escala 0-10 NPS) |
| RL-004 | Comentário opcional | ✅ ASSUMIDA | RN-RF071-010 (10-2000 caracteres) |

### 6.2 Regras Descartadas

| ID | Regra Legada | Motivo Descarte |
|----|-------------|-----------------|
| RL-005 | Cálculo de média aritmética | Fórmula incorreta para NPS |
| RL-006 | Envio ilimitado por usuário | Causa fadiga de pesquisa |
| RL-007 | Exposição de dados pessoais | Violação LGPD |

---

## 7. DECISÕES DE TRANSIÇÃO

### 7.1 Estratégia de Corte

**Big Bang** (substituição total):
- Sistema legado será **desativado** ao go-live do RF071
- NÃO haverá período de coexistência
- Motivo: Métricas incorretas do legado causam confusão

### 7.2 Migração de Dados

**Dados históricos:**
- ✅ **MIGRAR:** Respostas antigas (recalcular NPS com fórmula correta)
- ❌ **NÃO MIGRAR:** Configurações de envio (obsoletas)

**Script de migração:**
```sql
-- Migrar respostas legadas (ajustar escala 1-5 → 0-10)
INSERT INTO RespostaPesquisa (TemplatePesquisaId, UsuarioId, NotaNPS, Comentario, DataResposta)
SELECT
    NEWID(), -- Novo template
    Id_Usuario,
    CASE
        WHEN Nota_Satisfacao = 1 THEN 0
        WHEN Nota_Satisfacao = 2 THEN 3
        WHEN Nota_Satisfacao = 3 THEN 5
        WHEN Nota_Satisfacao = 4 THEN 8
        WHEN Nota_Satisfacao = 5 THEN 10
    END AS NotaNPS, -- Conversão aproximada
    Comentario,
    Data_Resposta
FROM tbl_Resposta_Pesquisa;
```

### 7.3 Cronograma de Desativação

1. **Dia D-7:** Avisar usuários sobre novo sistema
2. **Dia D:** Go-live RF071 (sistema legado readonly)
3. **Dia D+7:** Desativar completamente sistema legado
4. **Dia D+30:** Remover tabelas legadas (após backup)

### 7.4 Plano de Rollback

Em caso de problemas críticos no RF071:

1. **Reativar sistema legado** (ASPX + stored procedures)
2. **Pausar envio de pesquisas** via novo sistema
3. **Investigar falha** (logs Azure Application Insights)
4. **Corrigir** e re-deploy
5. **Migrar respostas** coletadas no período de rollback

---

## 8. CONCLUSÃO

### 8.1 Situação Atual

- ✅ **RF071.md v2.0** criado (690 linhas - 11 seções canônicas)
- ✅ **RF071.yaml** criado (sincronizado com RF.md)
- ✅ **RL-RF071.md** criado (documenta sistema legado parcial)
- 🔄 **RL-RF071.yaml** será criado (mapeamento `referencias`)

### 8.2 Próximos Passos

1. Criar RL-RF071.yaml (estrutura com `referencias` mapeando legado → moderno)
2. Executar validator-rl.py RF071 (deve passar com exit code 0)
3. Atualizar STATUS.yaml (marcar v2.0 completo)
4. Commit Git de todos os artefatos

### 8.3 Status de Governança

- **Governança v2.0:** ✅ Aderente
- **Separação RF/RL:** ✅ Completa (RL documenta legado parcial)
- **Rastreabilidade:** ✅ Total (todos os artefatos legados mapeados)
- **Validação Pendente:** 🔄 Executar validator-rl.py

---

**Documento controlado pela Governança v2.0 - IControlIT**
**Última revisão:** 2025-12-30

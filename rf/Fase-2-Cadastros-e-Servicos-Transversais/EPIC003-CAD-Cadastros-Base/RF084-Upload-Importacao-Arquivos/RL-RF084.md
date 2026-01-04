# RL-RF084 — Referência ao Legado: Upload e Importação de Arquivos

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF084 - Upload e Importação de Arquivos
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de upload e importação, garantindo rastreabilidade e mitigação de riscos durante a modernização.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica WebForms
- **Linguagem / Stack**: VB.NET, ASP.NET Web Forms (.aspx)
- **Banco de Dados**: SQL Server 2019 (múltiplos bancos por cliente)
- **Multi-tenant**: Não (bancos separados por cliente)
- **Auditoria**: Parcial (apenas logs de importação concluída, sem detalhamento)
- **Configurações**: Web.config (limites de upload, timeouts)

### 1.2 Stack Tecnológica Legada

| Componente | Tecnologia | Versão |
|------------|-----------|--------|
| Frontend | ASP.NET Web Forms | 4.5 |
| Backend | VB.NET Code-Behind | .NET Framework 4.5 |
| Upload Control | FileUpload (ASPX) | Built-in |
| Validação | Manual no code-behind | N/A |
| Processamento | Síncrono (bloqueia thread) | N/A |
| Armazenamento | File System Local | Windows Server |
| Antivírus | Nenhum | N/A |
| Progresso | Nenhum (sem feedback) | N/A |

### 1.3 Problemas Arquiteturais Identificados

1. **Limite de Upload Baixo**: Máximo 100MB configurado no Web.config, impossível aumentar sem afetar IIS
2. **Upload Síncrono**: Bloqueia thread do IIS durante todo processamento, causa timeouts para arquivos grandes
3. **Sem Antivírus**: Arquivos maliciosos podem ser enviados sem detecção
4. **Sem Rollback**: Importação parcial pode deixar dados inconsistentes no banco
5. **Sem Preview**: Usuário não consegue validar dados antes de confirmar importação
6. **Auditoria Limitada**: Apenas log de sucesso/falha, sem detalhes de linhas processadas ou erros
7. **Armazenamento Local**: Arquivos salvos em C:\Uploads, sem backup automático ou replicação
8. **Sem Isolamento**: Arquivos de todos clientes misturados na mesma pasta

---

## 2. TELAS DO LEGADO

### 2.1 Tela: UploadArquivo.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Importacao\UploadArquivo.aspx`

**Responsabilidade:** Formulário simples de upload de arquivo para importação de dados

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `FileUpload1` | FileUpload (ASPX) | Sim | Limite 100MB (Web.config) |
| `ddlTipoImportacao` | DropDownList | Sim | Tipos: Ativo, Contrato, Fatura, Usuario |
| `btnUpload` | Button | N/A | Dispara upload síncrono |
| `lblMensagem` | Label | N/A | Mostra sucesso/erro após upload |

#### Comportamentos Implícitos

- **Validação de Tipo**: Apenas verificação de extensão (.xls, .xlsx, .csv) no code-behind, sem validação de MIME Type
- **Processamento Imediato**: Após upload, arquivo é processado imediatamente sem preview
- **Timeout**: Upload > 5 minutos causa timeout do IIS (configuração padrão)
- **Sem Feedback Visual**: Usuário fica sem informação de progresso, apenas spinner genérico
- **Erro Não Tratado**: Exceções causam página branca (YSOD - Yellow Screen of Death)

#### Code-Behind (VB.NET)

**Arquivo:** `UploadArquivo.aspx.vb`

**Regras Implícitas Identificadas:**
1. Validação de extensão case-sensitive (`.XLS` é rejeitado, apenas `.xls` aceito)
2. Nome do arquivo é sanitizado manualmente (remove caracteres especiais), mas não previne null byte injection
3. Arquivo é salvo em `C:\Uploads\{Id_Cliente}\{Timestamp}_{NomeArquivo}`
4. Se pasta não existir, é criada sem verificação de permissões
5. Importação executa em loop síncrono linha por linha (sem transação)

**Destino no Sistema Moderno:** SUBSTITUÍDO por componente Angular com drag-and-drop e upload em chunks

---

### 2.2 Tela: RelatorioImportacoes.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Importacao\RelatorioImportacoes.aspx`

**Responsabilidade:** Lista de importações realizadas com status (sucesso/erro)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvImportacoes` | GridView | N/A | Lista paginada (10 itens por página) |
| `txtDataInicio` | TextBox (Date) | Não | Filtro de data inicial |
| `txtDataFim` | TextBox (Date) | Não | Filtro de data final |
| `ddlStatus` | DropDownList | Não | Todos, Sucesso, Erro |
| `btnBuscar` | Button | N/A | Dispara busca com filtros |

#### Comportamentos Implícitos

- **Paginação Server-Side**: GridView com ViewState pesado (>500KB para 100 registros)
- **Sem Detalhamento de Erros**: Coluna "Erros" mostra apenas quantidade, sem detalhes
- **Download de Relatório Indisponível**: Não há opção de exportar erros para CSV
- **Sem Retry**: Importação com erro não pode ser reprocessada, apenas nova tentativa manual

**Destino no Sistema Moderno:** SUBSTITUÍDO por tela Angular com paginação client-side e download de relatórios

---

### 2.3 Tela: ValidarImportacao.aspx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Importacao\ValidarImportacao.aspx`

**Responsabilidade:** Preview de dados antes de confirmar importação (NOTA: Esta tela existe no legado, mas raramente é usada)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `gvPreview` | GridView | N/A | Mostra primeiras 50 linhas |
| `lblTotalLinhas` | Label | N/A | Total de linhas no arquivo |
| `lblErros` | Label | N/A | Total de linhas com erro |
| `btnConfirmar` | Button | N/A | Confirma importação |
| `btnCancelar` | Button | N/A | Descarta upload |

#### Comportamentos Implícitos

- **Limite de Preview**: Apenas 50 linhas (hardcoded), insuficiente para arquivos grandes
- **Validação Parcial**: Schema validado, mas Foreign Keys não são verificadas
- **Timeout em Arquivos Grandes**: Preview de arquivo > 50MB causa timeout
- **Sem Marcação de Erros**: Linhas com erro aparecem sem destaque visual

**Destino no Sistema Moderno:** ASSUMIDO (funcionalidade mantida) mas reimplementado com 100 linhas e erros mapeados visualmente

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### 3.1 WebService: WSImport.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\Services\WSImport.asmx`

**Responsabilidade:** Processamento de importações via SOAP (usado por integrações antigas)

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `UploadArquivo(arquivo As Byte(), tipo As String)` | Recebe arquivo base64, salva em disco | Sem validação de tamanho, risco de OutOfMemoryException |
| `ValidarArquivo(idUpload As Integer)` | Valida estrutura do arquivo | Apenas verifica colunas, não valida dados |
| `ProcessarImportacao(idUpload As Integer)` | Inicia importação síncrona | Timeout após 5 minutos |
| `ObterStatus(idUpload As Integer)` | Retorna status da importação | Polling manual (sem push) |

**Problemas Identificados:**
- **SOAP Legacy**: Protocolo pesado, substituído por REST
- **Base64 Transfer**: Ineficiente para arquivos grandes (overhead de 33%)
- **Sem Autenticação**: WebService público sem validação de token
- **Sem Rate Limiting**: Vulnerável a ataques de DoS

**Destino no Sistema Moderno:** SUBSTITUÍDO por REST API com JWT authentication e chunked upload

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Tb_Importacoes

**Banco:** `BDICSYSTEM` (SQL Server 2019)

**DDL Original:**
```sql
CREATE TABLE [dbo].[Tb_Importacoes](
    [Id_Importacao] [int] IDENTITY(1,1) NOT NULL,
    [Id_Usuario] [int] NOT NULL,
    [Nm_Arquivo] [varchar](255) NOT NULL,
    [Tp_Importacao] [varchar](50) NOT NULL,
    [Qt_Linhas_Importadas] [int] NOT NULL,
    [Qt_Linhas_Erros] [int] NOT NULL,
    [Dt_Importacao] [datetime] NOT NULL,
    [Status] [varchar](20) NOT NULL,
    [Ds_Erro] [text] NULL,
    CONSTRAINT [PK_Tb_Importacoes] PRIMARY KEY CLUSTERED ([Id_Importacao] ASC)
)
```

**Problemas Identificados:**

| Problema | Descrição | Impacto |
|----------|-----------|---------|
| Sem Foreign Key para Usuario | `Id_Usuario` não tem FK, permite orphan records | Médio |
| Tipo varchar em Status | Deveria ser enum ou tabela lookup | Baixo |
| Ds_Erro como TEXT | Tipo deprecated, sem limit, dificulta busca | Médio |
| Sem Auditoria | Falta Created, CreatedBy, Modified, ModifiedBy | Alto |
| Sem Multi-Tenancy | Falta Id_Cliente para isolamento | Crítico |
| Sem Soft Delete | Exclusão física perde histórico | Médio |

**Destino no Sistema Moderno:** SUBSTITUÍDO por tabela `Upload` com multi-tenancy, auditoria completa e relacionamentos via FK

---

### 4.2 Tabela: Tb_Erros_Importacao (Não existe no legado)

**Observação:** No legado, erros de importação são salvos apenas em campo TEXT (`Ds_Erro`) na tabela `Tb_Importacoes`, sem estrutura. Exemplo:

```
"Linha 10: CNPJ inválido | Linha 23: Empresa não encontrada | Linha 45: Data fora do range"
```

Isso impossibilita:
- Consultas estruturadas (ex: "Quantas linhas falharam por CNPJ inválido?")
- Exportação de relatório detalhado
- Reprocessamento de linhas específicas

**Destino no Sistema Moderno:** CRIADO tabela `ImportError` para rastreabilidade estruturada de erros (linha, coluna, mensagem, valor)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Limite de Upload Configurável mas Limitado

**Descrição:** Tamanho máximo de upload é configurado via Web.config, mas IIS impõe limite absoluto de 100MB (configuração maxRequestLength)

**Localização:** `Web.config` (linha 45)
```xml
<httpRuntime maxRequestLength="102400" executionTimeout="300" />
```

**Impacto:** Arquivos > 100MB não podem ser enviados, gerando erro HTTP 413 ou timeout

**Destino no Sistema Moderno:** SUBSTITUÍDO por chunked upload com limite de 500MB

---

### RL-RN-002: Extensão deve ser XLS, XLSX ou CSV (Case-Sensitive)

**Descrição:** Validação de extensão é case-sensitive, apenas minúsculas aceitas

**Localização:** `UploadArquivo.aspx.vb` (linha 120)
```vb
If Not (ext = ".xls" Or ext = ".xlsx" Or ext = ".csv") Then
    lblMensagem.Text = "Tipo de arquivo inválido"
    Return
End If
```

**Problema:** Arquivos com extensão `.XLS` (maiúscula) são rejeitados

**Destino no Sistema Moderno:** ASSUMIDO mas corrigido (validação case-insensitive)

---

### RL-RN-003: Importação Sem Transação (Risco de Dados Parciais)

**Descrição:** Importação processa linhas em loop síncrono sem transação. Se falhar na linha 500 de 1000, as primeiras 499 já foram inseridas.

**Localização:** `ImportacaoHelper.vb` (linha 250)
```vb
For Each row In dt.Rows
    Try
        InsertRow(row)
        successCount += 1
    Catch ex As Exception
        errorCount += 1
        errorLog.Append("Linha " & row.Index & ": " & ex.Message)
    End Try
Next
```

**Impacto:** Banco fica com dados parciais, exige limpeza manual

**Destino no Sistema Moderno:** SUBSTITUÍDO por importação transacional com rollback automático

---

### RL-RN-004: Nome do Arquivo Salvo com Timestamp Manual

**Descrição:** Arquivo é salvo com timestamp no formato `yyyyMMddHHmmss_{NomeOriginal}`

**Localização:** `UploadArquivo.aspx.vb` (linha 85)
```vb
Dim fileName As String = DateTime.Now.ToString("yyyyMMddHHmmss") & "_" & FileUpload1.FileName
Dim path As String = "C:\Uploads\" & Id_Cliente & "\" & fileName
FileUpload1.SaveAs(path)
```

**Problema:**
- Colisão de nomes se dois uploads ocorrem no mesmo segundo
- Sem hash de arquivo (integridade não verificada)
- Path hardcoded (`C:\Uploads`)

**Destino no Sistema Moderno:** SUBSTITUÍDO por GUID como identificador único + hash SHA256 para integridade

---

### RL-RN-005: Processamento Síncrono Bloqueia UI

**Descrição:** Importação é processada no mesmo request HTTP, travando UI até concluir ou timeout (5 min)

**Localização:** `UploadArquivo.aspx.vb` (linha 150)
```vb
Protected Sub btnUpload_Click(sender As Object, e As EventArgs)
    ' Upload do arquivo
    UploadFile()
    ' Processamento IMEDIATO (síncrono)
    ProcessImport()
    ' Exibe resultado (ou timeout)
    lblMensagem.Text = "Importação concluída!"
End Sub
```

**Impacto:** Usuário fica aguardando sem feedback, conexão pode cair

**Destino no Sistema Moderno:** SUBSTITUÍDO por processamento assíncrono com Hangfire + notificações SignalR

---

### RL-RN-006: Validação de Schema Incompleta

**Descrição:** Validação verifica apenas se colunas obrigatórias existem, mas não valida tipos de dados ou ranges

**Localização:** `ValidationHelper.vb` (linha 45)
```vb
Public Function ValidateSchema(dt As DataTable) As Boolean
    Dim requiredColumns As String() = {"CNPJ", "Nome", "Email"}
    For Each col In requiredColumns
        If Not dt.Columns.Contains(col) Then
            Return False
        End If
    Next
    Return True
End Function
```

**Problema:** Campo "CNPJ" pode conter texto inválido ("ABC123"), campo "Email" sem validação de formato

**Destino no Sistema Moderno:** ASSUMIDO mas expandido com validação de tipos, ranges, formatos e FK

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Limite de Upload** | 100MB (Web.config) | 500MB (chunked) | Modernizado: Chunks permitem arquivos maiores |
| **Antivírus** | Nenhum | ClamAV obrigatório | Novo: Segurança crítica adicionada |
| **Processamento** | Síncrono (timeout 5 min) | Assíncrono (Hangfire) | Modernizado: Não bloqueia UI |
| **Progresso** | Nenhum | SignalR em tempo real | Novo: Feedback ao usuário |
| **Armazenamento** | File System Local | Azure Blob Storage | Modernizado: Cloud, encriptado |
| **Rollback** | Nenhum (dados parciais) | Transação SQL única | Novo: Integridade garantida |
| **Preview** | 50 linhas (raramente usado) | 100 linhas obrigatório | Modernizado: Sempre exibido |
| **Relatório de Erros** | Text field concatenado | Tabela estruturada | Modernizado: Consultável e exportável |
| **Multi-Tenancy** | Bancos separados | Row-Level Security | Modernizado: Banco único isolado |
| **Auditoria** | Parcial (log básico) | Completa (7 anos) | Modernizado: Conformidade LGPD |
| **Validação de Dados** | Schema apenas | Schema + Tipos + FK | Modernizado: Validação completa |
| **Formatos Suportados** | XLS, XLSX, CSV | CSV, XLSX, XML, JSON | Modernizado: Mais formatos |

**Funcionalidades do Legado NÃO Migradas:**
- WebService SOAP (`WSImport.asmx`) → Descartado, substituído por REST API
- Validação case-sensitive de extensão → Corrigido no moderno
- Processamento síncrono → Substituído por assíncrono

**Funcionalidades Novas do Moderno (não existiam no legado):**
- Chunked upload retomável
- Scan antivírus obrigatório
- Progresso em tempo real (SignalR)
- Rollback transacional
- Azure Blob Storage encriptado
- Preview obrigatório antes de importar
- Relatórios estruturados de erros

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir WebService SOAP por REST API

**Motivo:**
- SOAP é protocolo legado, pesado e complexo
- REST é padrão moderno, leve e amplamente suportado
- JWT authentication é mais seguro que nenhuma autenticação

**Impacto:** Alto - Integrações antigas (ERPs) precisarão ser atualizadas

**Mitigação:** Manter WebService SOAP em paralelo por 6 meses (período de transição)

---

### Decisão 2: Implementar Chunked Upload (TUS Protocol)

**Motivo:**
- Permite uploads > 100MB sem esgotar memória
- Retomável em caso de falha de rede
- Feedback de progresso em tempo real

**Impacto:** Médio - Complexidade adicional no frontend e backend

**Mitigação:** Usar biblioteca TUS.IO (padrão de mercado)

---

### Decisão 3: Tornar Scan Antivírus Obrigatório

**Motivo:**
- Legado permite upload de arquivos maliciosos
- Conformidade com políticas de segurança corporativa
- Proteção contra ransomware e malware

**Impacto:** Médio - ClamAV adiciona latência (~2-5s por arquivo)

**Mitigação:** Executar scan em paralelo com validação de schema

---

### Decisão 4: Processamento Assíncrono Obrigatório para Arquivos > 10MB

**Motivo:**
- Evitar timeouts do IIS/Kestrel
- Liberar thread para outros requests
- Permitir cancelamento de importação

**Impacto:** Baixo - Usuário precisa aguardar job finalizar

**Mitigação:** Notificações em tempo real via SignalR + email ao concluir

---

### Decisão 5: Migrar de File System para Azure Blob Storage

**Motivo:**
- Armazenamento local não tem backup automático
- Azure Blob é replicado, encriptado e escalável
- Permite CDN para download de relatórios

**Impacto:** Médio - Custo adicional de storage

**Mitigação:** Lifecycle policy para deletar arquivos após 90 dias (exceto auditoria)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Integrações SOAP quebradas** | Alto | Alta | Manter SOAP em paralelo por 6 meses |
| **ClamAV indisponível causa bloqueio** | Alto | Média | Fallback para fila de "pending scan" + alerta admin |
| **Azure Blob Storage custo excede orçamento** | Médio | Baixa | Implementar lifecycle policy (90 dias) |
| **Chunked upload incompatível com proxy corporativo** | Médio | Média | Permitir upload direto (sem chunks) para arquivos < 10MB |
| **SignalR bloqueado por firewall** | Médio | Média | Fallback para polling a cada 5s |
| **Hangfire job queue estoura memória** | Alto | Baixa | Limitar concorrência (5 jobs paralelos) + monitoramento |
| **Usuários não entendem preview obrigatório** | Baixo | Média | Onboarding + tooltip explicativo |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF Moderno |
|----------------|----------------------|
| `UploadArquivo.aspx` | RF084 - Seção 4 (Funcionalidades) + UC01 (Iniciar Upload) |
| `RelatorioImportacoes.aspx` | RF084 - Seção 8 (API Endpoints) + UC00 (Listar Uploads) |
| `ValidarImportacao.aspx` | RF084 - RN-RF084-005 (Separação Upload e Importação) + UC02 (Preview) |
| `WSImport.asmx` | RF084 - Seção 8 (API Endpoints) - SUBSTITUÍDO por REST |
| `Tb_Importacoes` | RF084 - Seção 9 (Modelo de Dados) - Entidade `Upload` |
| Validação de Extensão | RF084 - RN-RF084-003 (Validação de Extensão Consistente) |
| Limite de 100MB | RF084 - RN-RF084-001 (Limite de 500MB) |
| Processamento Síncrono | RF084 - RN-RF084-008 (Processamento Assíncrono) |
| Sem Auditoria | RF084 - RN-RF084-012 (Auditoria Completa) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Documentação completa da referência ao legado (migração v1.0 → v2.0) | Agência ALC - alc.dev.br |

---

**Última Atualização**: 2025-12-31
**Status**: Pronto para rastreabilidade YAML (RL-RF084.yaml)

# RL-RF107 — Referência ao Legado

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-107
**Sistema Legado:** IControlIT Web Forms (VB.NET + ASP.NET)
**Objetivo:** Documentar o comportamento do legado de QR Codes que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica Web Forms
- **Linguagem / Stack**: VB.NET, ASP.NET Web Forms, SQL Server
- **Banco de Dados**: SQL Server (múltiplos bancos por cliente - IC1Legado_ClienteXX)
- **Multi-tenant**: Não suportado nativamente (bancos separados por cliente)
- **Auditoria**: Inexistente para operações de QR Code
- **Configurações**: Web.config + tabelas de configuração no banco

### 1.2 Stack Tecnológica

| Componente | Tecnologia Legada |
|------------|-------------------|
| Frontend | ASP.NET Web Forms (ASPX) + VB.NET Code-Behind |
| Backend | VB.NET + Web Services (ASMX) |
| Banco de Dados | SQL Server 2008/2012 |
| Geração de QR Code | Manual via Excel ou biblioteca antiga (sem validação) |
| Armazenamento de Imagens | Servidor local (sem backup) |
| Autenticação | Session-based (ASP.NET Membership) |
| Autorização | Hardcoded no code-behind (sem RBAC) |

### 1.3 Problemas Arquiteturais Identificados

1. **Ausência de validação de QR Code**: QR Codes gerados manualmente sem CheckDigit ou validação de unicidade
2. **Sem rastreamento GPS**: Localização registrada manualmente via campo de texto
3. **Sem auditoria**: Impossível rastrear quem leu, quando ou onde
4. **Multi-database sem isolamento**: Cada cliente tinha banco separado, sem tenant isolation
5. **Imagens sem backup**: QR Codes salvos em servidor local sem redundância
6. **Performance ruim**: Queries sem índices, sem paginação
7. **Sem retenção LGPD**: Dados mantidos indefinidamente sem política de anonimização

---

## 2. TELAS DO LEGADO

### Tela: Patrimonio_QRCode.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Patrimonio\Patrimonio_QRCode.aspx`
- **Responsabilidade:** Gerenciar QR Codes de patrimônios (CRUD manual)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| idPatrimonio | INT | Sim | ID do patrimônio (FK para Patrimonio) |
| CodigoQR | VARCHAR(255) | Sim | Código QR em texto plano (sem validação) |
| LocalAtual | VARCHAR(255) | Não | Localização manual (texto livre) |
| DataGeracao | DATETIME | Sim | Data de geração do QR Code |
| UsuarioGeracao | VARCHAR(50) | Sim | Login do usuário (sem FK, string livre) |
| Ativo | BIT | Sim | Flag de ativo/inativo |

#### Comportamentos Implícitos

- Geração de QR Code era manual via botão que chamava Excel/VBA
- Não havia validação de duplicação de código
- Campo `LocalAtual` era texto livre sem vínculo com tabela de localizações
- Não havia histórico de movimentações (apenas último local)
- Imagem do QR Code era salva em pasta do servidor (`\\servidor\qrcodes\`)

---

### Tela: Patrimonio_QRCode_Gerar.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Patrimonio\Patrimonio_QRCode_Gerar.aspx`
- **Responsabilidade:** Gerar novo QR Code para patrimônio

#### Comportamentos Implícitos

- Geração era feita via biblioteca antiga (sem código aberto)
- Não havia validação de unicidade
- Tamanho da imagem era fixo (não permitia customização)
- Imagem salva em BLOB no banco (campo `ImagemQRCode` tipo `IMAGE`)
- Não havia auditoria de quem gerou ou quando

---

### Tela: Patrimonio_QRCode_Impressao.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Patrimonio\Patrimonio_QRCode_Impressao.aspx`
- **Responsabilidade:** Imprimir etiquetas com QR Code

#### Comportamentos Implícitos

- Geração de PDF era via Crystal Reports (licença proprietária)
- Layout fixo sem customização
- Não incluía data de geração ou código patrimonial completo
- Impressão em lote não funcionava (travava após 50 etiquetas)

---

### Tela: Patrimonio_QRCode_Leitura.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Patrimonio\Patrimonio_QRCode_Leitura.aspx`
- **Responsabilidade:** Interface manual de leitura de QR Code (via scanner externo)

#### Comportamentos Implícitos

- Leitura era via scanner de código de barras externo (não câmera)
- Não capturava GPS (localização manual)
- Não havia registro de quem leu ou quando
- Campo `DataUltimaLeitura` era atualizado sem auditoria

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

### WebService: WSPatrimonioQRCode.asmx

**Caminho:** `D:\IC2\ic1_legado\IControlIT\WebService\WSPatrimonioQRCode.asmx.vb`

| Método | Responsabilidade | Observações |
|--------|------------------|-------------|
| `GerarQRCodePatrimonio(idPatrimonio)` | Gera código para patrimônio | Retorna string do QR Code sem validação |
| `LerQRCode(codigoQR)` | Lê QR Code e atualiza última leitura | Não registra histórico, apenas atualiza `DataUltimaLeitura` |
| `ObterHistoricoQRCode(idPatrimonio)` | Retorna histórico (vazio no legado) | Sempre retornava vazio pois não havia tabela de histórico |
| `ExportarInventario()` | Exporta relatório de inventário | Gerava CSV sem filtros ou paginação |

#### Comportamentos Implícitos em WSPatrimonioQRCode.asmx

- Método `GerarQRCodePatrimonio` não validava se patrimônio já tinha QR Code
- Método `LerQRCode` não validava se código existia (retornava sucesso mesmo para código inexistente)
- Não havia autenticação (web service público)
- Retorno era XML sem schema definido
- Timeouts frequentes em lotes grandes

---

## 4. TABELAS LEGADAS

### Tabela: Patrimonio_QRCode

**Finalidade:** Armazenar QR Codes de patrimônios

**DDL Legado:**
```sql
CREATE TABLE [dbo].[Patrimonio_QRCode](
    [idPatrimonio] [int] IDENTITY(1,1) NOT NULL,
    [idEmpresa] [int] NOT NULL,
    [idCliente] [int] NULL,
    [CodigoPatrimonial] [varchar](50) NOT NULL,
    [CodigoQR] [varchar](255) NULL,
    [ImagemQRCode] [image] NULL,
    [LocalAtual] [varchar](255) NULL,
    [DataGeracao] [datetime] NULL,
    [DataUltimaLeitura] [datetime] NULL,
    [UsuarioGeracao] [varchar](50) NULL,
    [UsuarioUltimaLeitura] [varchar](50) NULL,
    [Ativo] [bit] DEFAULT 1,
    CONSTRAINT [PK_Patrimonio_QRCode] PRIMARY KEY CLUSTERED ([idPatrimonio] ASC)
)
```

**Problemas Identificados:**
- Falta Foreign Key para validar `idEmpresa` ou `idCliente`
- Campo `ImagemQRCode` tipo `IMAGE` (deprecated no SQL Server)
- Campo `UsuarioGeracao` sem FK (string livre, dados inconsistentes)
- Sem índices em `CodigoQR` (queries lentas)
- Sem campos de auditoria (Created, Modified)
- Sem soft delete (flag `Ativo` era sobrescrita)

---

### Tabela: Patrimonio_QRCode_Historico

**Finalidade:** Armazenar histórico de leituras (NÃO IMPLEMENTADA NO LEGADO)

**DDL Legado:**
```sql
CREATE TABLE [dbo].[Patrimonio_QRCode_Historico](
    [idHistorico] [int] IDENTITY(1,1) NOT NULL,
    [idPatrimonioQRCode] [int] NOT NULL,
    [DataLeitura] [datetime] NOT NULL,
    [LocalLeitura] [varchar](255) NULL,
    [UsuarioLeitura] [varchar](50) NOT NULL,
    [Observacoes] [varchar](500) NULL,
    CONSTRAINT [PK_Patrimonio_QRCode_Historico] PRIMARY KEY CLUSTERED ([idHistorico] ASC),
    CONSTRAINT [FK_Historico_QRCode] FOREIGN KEY ([idPatrimonioQRCode])
        REFERENCES [dbo].[Patrimonio_QRCode]([idPatrimonio])
)
```

**Problemas Identificados:**
- Tabela criada mas **NUNCA POPULADA** no legado
- Sem dados históricos para migração
- Campo `LocalLeitura` texto livre (deveria ser FK)
- Sem campos de GPS (latitude, longitude)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: QR Code gerado manualmente sem validação

**Descrição:** No legado, QR Code era gerado manualmente via Excel/VBA ou biblioteca antiga sem validação de unicidade, formato ou checksum.

**Localização:** `Patrimonio_QRCode_Gerar.aspx.vb`, linhas 45-67

**Impacto:** Possibilidade de duplicação de códigos, falsificação e erros de leitura.

**Destino no Moderno:** SUBSTITUÍDO - Agora gera via ZXing.Net com validação Luhn obrigatória.

---

### RL-RN-002: Localização manual via campo de texto livre

**Descrição:** Usuário digitava manualmente o local do ativo (sem autocomplete, validação ou FK para tabela de locais).

**Localização:** `Patrimonio_QRCode_Leitura.aspx.vb`, linhas 89-102

**Impacto:** Dados inconsistentes, impossível agrupar por localização, sem GPS.

**Destino no Moderno:** SUBSTITUÍDO - Agora captura GPS automaticamente via Geolocation API.

---

### RL-RN-003: Sem histórico de movimentações

**Descrição:** Sistema atualizava apenas `DataUltimaLeitura` sem registrar histórico de quem leu, quando ou onde.

**Localização:** `WSPatrimonioQRCode.asmx.vb`, método `LerQRCode`, linhas 123-135

**Impacto:** Impossível rastrear trilha de movimentações, não atende LGPD.

**Destino no Moderno:** SUBSTITUÍDO - Tabela `QRCodeLeitura` com histórico completo.

---

### RL-RN-004: Imagens QR Code salvas em servidor local

**Descrição:** Imagens geradas eram salvas em pasta do servidor (`\\servidor\qrcodes\`) sem backup ou redundância.

**Localização:** `Patrimonio_QRCode_Gerar.aspx.vb`, linhas 78-84

**Impacto:** Perda de imagens em caso de falha de hardware.

**Destino no Moderno:** SUBSTITUÍDO - Azure Blob Storage com redundância geográfica.

---

### RL-RN-005: Sem autenticação em Web Service

**Descrição:** Web Service `WSPatrimonioQRCode.asmx` era público, sem autenticação ou validação de origem.

**Localização:** `WSPatrimonioQRCode.asmx.vb`, linhas 1-15

**Impacto:** Qualquer aplicação externa poderia chamar e modificar dados.

**Destino no Moderno:** SUBSTITUÍDO - REST API com JWT obrigatório.

---

### RL-RN-006: Retenção de dados indefinida

**Descrição:** Dados de QR Code eram mantidos indefinidamente sem política de retenção ou anonimização.

**Localização:** Sem implementação no legado

**Impacto:** Não conformidade com LGPD Art. 5º.

**Destino no Moderno:** ASSUMIDO - Job diário anonimiza dados > 24 meses.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Geração de QR Code** | Manual via Excel/VBA | Automática via ZXing.Net com Luhn | Legado sem validação |
| **Validação de Unicidade** | Inexistente | CheckDigit obrigatório | Legado permitia duplicação |
| **Rastreamento GPS** | Não | Sim (precisão 10m) | Legado usava texto livre |
| **Histórico de Leituras** | Inexistente | Tabela QRCodeLeitura com 24 meses | Legado sem auditoria |
| **Autenticação Web Service** | Não | JWT obrigatório | Legado era público |
| **Armazenamento de Imagens** | Servidor local | Azure Blob Storage | Legado sem backup |
| **Multi-tenancy** | Bancos separados | ClienteId em todas as tabelas | Legado sem isolamento eficiente |
| **Impressão de Etiquetas** | Crystal Reports | PDF via iTextSharp | Legado com licença proprietária |
| **Leitura de QR Code** | Scanner externo | PWA com câmera HTML5 | Legado sem mobile |
| **Inventário Bulk** | Não suportado | Até 1.000 QR Codes | Legado travava após 50 |
| **Retenção LGPD** | Indefinida | 24 meses com anonimização | Legado não conforme |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Validação Obrigatória de CheckDigit

**Descrição:** Implementar validação de CheckDigit via Algoritmo de Luhn em TODOS os QR Codes.

**Motivo:** Legado permitia QR Codes duplicados ou falsificados. Luhn é padrão ISO para validação.

**Impacto:** Alto - Requer re-geração de todos os QR Codes do legado (migração de dados).

**Mitigação:** Script de migração gera novo QR Code para cada patrimônio existente.

---

### Decisão 2: GPS Obrigatório em Leituras

**Descrição:** Leitura de QR Code sem GPS deve ser rejeitada ou marcada como "baixa confiabilidade".

**Motivo:** Legado usava texto livre, impossível rastrear movimentações reais.

**Impacto:** Médio - Usuários precisam conceder permissão de GPS no mobile.

**Mitigação:** Alerta educativo ao abrir PWA pela primeira vez.

---

### Decisão 3: Histórico Imutável por 24 Meses

**Descrição:** Criar tabela `QRCodeLeitura` com registro imutável de todas as leituras.

**Motivo:** LGPD Art. 5º exige rastreabilidade e propósito legítimo. 24 meses é padrão corporativo.

**Impacto:** Médio - Aumento de armazenamento (estimado 50MB/ano por cliente).

**Mitigação:** Job diário anonimiza dados expirados automaticamente.

---

### Decisão 4: Migração de Imagens para Azure Blob

**Descrição:** Migrar imagens QR Code de servidor local para Azure Blob Storage.

**Motivo:** Servidor local sem backup, risco de perda de dados.

**Impacto:** Baixo - Custo adicional de R$ 0,20/GB/mês no Azure.

**Mitigação:** Migração em lote via script PowerShell.

---

### Decisão 5: Descontinuar Crystal Reports

**Descrição:** Substituir geração de etiquetas por iTextSharp (biblioteca open-source).

**Motivo:** Crystal Reports tem licença proprietária cara e deprecated.

**Impacto:** Baixo - Layout de etiqueta será redesenhado (melhoria visual).

**Mitigação:** Template de etiqueta configurável via JSON.

---

### Decisão 6: Descartar Tabela `Patrimonio_QRCode_Historico`

**Descrição:** Tabela existia no legado mas **NUNCA FOI POPULADA**.

**Motivo:** Sem dados para migrar, estrutura inadequada (sem GPS, sem FK).

**Impacto:** Nenhum - Não há dados a perder.

**Mitigação:** Criar nova tabela `QRCodeLeitura` com estrutura moderna.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|-------|---------|-----------|
| **QR Codes legados sem CheckDigit** | Alto - Impossível validar autenticidade | Re-gerar todos os QR Codes com novo formato |
| **Imagens QR Code perdidas** | Médio - Servidor local pode ter falhas | Backup manual antes de migração + re-geração |
| **Usuários sem GPS no mobile** | Médio - Leituras podem falhar | Fallback para "baixa confiabilidade" + alerta |
| **Perda de histórico de leituras** | Baixo - Legado não tinha histórico | Sem impacto (não há dados a migrar) |
| **Dependência de Crystal Reports** | Baixo - Licença expirada | Substituir por iTextSharp |
| **Multi-database sem isolamento** | Alto - Dados misturados | Consolidar em banco único com ClienteId |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF-107 |
|-----------------|-------------------|
| `Patrimonio_QRCode.aspx` | RF-107 - Seção 4: Funcionalidades (Gerar/Listar QR Code) |
| `WSPatrimonioQRCode.asmx` | RF-107 - RN-RF107-001 a RN-RF107-012 |
| `Patrimonio_QRCode` (tabela) | MD-RF107 - Tabela `QRCode` |
| `Patrimonio_QRCode_Historico` (tabela) | MD-RF107 - Tabela `QRCodeLeitura` |
| `ImagemQRCode` (campo BLOB) | Azure Blob Storage (migração externa) |
| `CodigoQR` (campo string) | RF-107 - RN-RF107-001 (GUID + Base64URL) |
| `LocalAtual` (campo texto) | RF-107 - RN-RF107-005 (GPS + reverse geocoding) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-31 | Versão inicial - referência completa ao legado de QR Codes | Agência ALC - alc.dev.br |

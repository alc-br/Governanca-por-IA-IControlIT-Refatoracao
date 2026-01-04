# RL-RF081 — Referência ao Legado (Termos de Responsabilidade)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Claude Code

**RF Moderno Relacionado:** RF-081 - Termos de Responsabilidade por Ativos e Equipamentos
**Sistema Legado:** ASP.NET Web Forms + VB.NET + SQL Server
**Objetivo:** Documentar o comportamento do sistema legado que serve de base para a refatoração, garantindo rastreabilidade histórica e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### 1.1 Arquitetura Geral

- **Arquitetura**: Monolítica WebForms (ASP.NET)
- **Linguagem / Stack**: VB.NET + ASP.NET Web Forms
- **Banco de Dados**: SQL Server (múltiplos bancos - um por cliente)
- **Multi-tenant**: Não (banco separado por cliente)
- **Auditoria**: Inexistente (não rastreia quem/quando/onde aceita termo)
- **Configurações**: Web.config + tabelas no SQL Server

### 1.2 Problemas Arquiteturais Identificados

1. **Falta de Versionamento**: Quando termo é editado, versão anterior é sobrescrita (perde histórico)
2. **Ausência de Assinatura Digital**: Aceite é apenas checkbox simples (sem prova legal)
3. **Sem Geolocalização**: Não registra IP ou GPS do aceite (sem rastreabilidade forense)
4. **Timestamp Local**: Data/hora em fuso local do servidor (não auditável internacionalmente)
5. **Sem Auditoria LGPD**: Não rastreia quem aceitou qual versão, quando, com quais dados
6. **Notificações Manuais**: Gestores precisavam enviar emails manualmente antes vencimento
7. **Sem Comprovante**: Não gera PDF com QRCode (documentação física inexistente)
8. **Multi-database**: Cada cliente em banco separado (dificulta consolidação e relatórios)

---

## 2. TELAS DO LEGADO

### 2.1 Tela: [Não encontrada - Funcionalidade Inexistente no Legado]

**OBSERVAÇÃO IMPORTANTE**: O sistema legado NÃO possuía tela dedicada para "Termos de Responsabilidade por Ativos".

A funcionalidade era **genérica e limitada** ("Gerenciamento de Termos" básico), sem foco em ativos/equipamentos.

**Referência mais próxima**: Tela genérica de envio de termos (`ic1_legado/IControlIT/Sistema/Termos/`) que permitia apenas:
- Enviar texto de termo por email
- Marcar se usuário leu (`Flg_Lido`)
- Marcar se usuário aceitou (`Flg_Aceito`)

**Comportamentos Implícitos** (não documentados):
- Aceite era checkbox simples (sem assinatura)
- Não validava identidade do usuário
- Não capturava contexto (IP, GPS, dispositivo)
- Não gerava comprovante automático

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

**OBSERVAÇÃO**: Nenhum WebService (.asmx) dedicado foi encontrado para termos de responsabilidade no legado.

A lógica era integrada em telas ASPX via code-behind VB.NET (sem separação de camadas).

---

## 4. TABELAS LEGADAS

### 4.1 Tabela: Si_Texto_Termo

**Caminho**: `[ic1_legado].[dbo].[Si_Texto_Termo]`

**Finalidade**: Armazenar texto do termo de responsabilidade (genérico, não específico para ativos)

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[Si_Texto_Termo](
    [Id_Texto_Termo] [int] IDENTITY(1,1) NOT NULL,
    [Ds_Titulo] [varchar](255) NOT NULL,
    [Ds_Termo] [nvarchar](max) NOT NULL,
    [Dt_Criacao] [datetime] NOT NULL,
    [Ativo] [bit] NOT NULL DEFAULT 1,
    CONSTRAINT [PK_Si_Texto_Termo] PRIMARY KEY CLUSTERED ([Id_Texto_Termo] ASC)
);
```

**Problemas Identificados**:
- ❌ Sem versionamento (alteração sobrescreve versão anterior)
- ❌ Sem auditoria (não rastreia quem criou/editou)
- ❌ Sem campos de multi-tenancy (ClienteId/EmpresaId)
- ❌ Sem relacionamento com tipo de ativo (termo genérico)
- ❌ Sem campos de vigência (data início/fim)
- ❌ Sem campos de penalidade

---

### 4.2 Tabela: Usuario_Envio_TermoResponsabilidade

**Caminho**: `[ic1_legado].[dbo].[Usuario_Envio_TermoResponsabilidade]`

**Finalidade**: Registrar envio de termo para usuário e capturar aceite básico

**Estrutura Simplificada**:
```sql
CREATE TABLE [dbo].[Usuario_Envio_TermoResponsabilidade](
    [Id_Usuario_Envio_Termo] [int] IDENTITY(1,1) NOT NULL,
    [Id_Usuario] [int] NOT NULL,
    [Id_Texto_Termo] [int] NOT NULL,
    [Dt_Envio] [datetime] NOT NULL,
    [Flg_Lido] [bit] NOT NULL DEFAULT 0,
    [Dt_Leitura] [datetime] NULL,
    [Flg_Aceito] [bit] NOT NULL DEFAULT 0,
    [Dt_Aceito] [datetime] NULL,
    CONSTRAINT [PK_Usuario_Envio_TermoResponsabilidade] PRIMARY KEY CLUSTERED ([Id_Usuario_Envio_Termo] ASC)
);
```

**Problemas Identificados**:
- ❌ Aceite é apenas flag boolean (sem assinatura digital)
- ❌ Sem captura de IP ou geolocalização
- ❌ Sem captura de User-Agent (dispositivo)
- ❌ Timestamp em `datetime` local (não UTC)
- ❌ Sem campos de vigência (data vencimento)
- ❌ Sem relacionamento com ativo/equipamento específico
- ❌ Sem campos de revogação (data, motivo)
- ❌ Sem penalidade acumulada
- ❌ Sem hash de integridade (SHA-256)
- ❌ Sem armazenamento de comprovante (PDF)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Aceite Simples sem Validação de Identidade

**Descrição**: No legado, aceite era apenas marcar checkbox "Li e Aceito", sem validar CPF ou matrícula corporativa.

**Fonte**: Análise do comportamento das telas (`ic1_legado/IControlIT/Sistema/Termos/`)

**Destino no RF Moderno**: **SUBSTITUÍDO** por RN-TRM-081-02 (Validação de Identidade Obrigatória via BrasilAPI)

---

### RL-RN-002: Sem Notificações Automáticas de Vencimento

**Descrição**: No legado, não havia job automático para notificar usuários sobre vencimento de termos. Gestores precisavam enviar emails manualmente.

**Fonte**: Ausência de Hangfire Jobs ou Stored Procedures de notificação

**Destino no RF Moderno**: **SUBSTITUÍDO** por RN-TRM-081-06 (Notificações Inteligentes Automáticas 30/15/7 dias)

---

### RL-RN-003: Timestamp em Fuso Local (Não UTC)

**Descrição**: Data/hora de aceite era registrada em fuso local do servidor SQL Server, sem sincronização NTP.

**Fonte**: Campo `Dt_Aceito` do tipo `datetime` (sem timezone awareness)

**Destino no RF Moderno**: **SUBSTITUÍDO** por RN-TRM-081-03 (Timestamp UTC Sincronizado com NTP)

---

### RL-RN-004: Sem Cálculo Automático de Penalidades

**Descrição**: Quando equipamento não era devolvido no prazo, penalidade era calculada manualmente por planilha Excel.

**Fonte**: Ausência de campos de penalidade nas tabelas

**Destino no RF Moderno**: **SUBSTITUÍDO** por RN-TRM-081-07 (Cálculo Automático de Penalidades)

---

### RL-RN-005: Edição de Termo Sobrescreve Versão Anterior

**Descrição**: Quando gestor editava termo, versão anterior era perdida (sem histórico). Usuários que aceitaram versão antiga ficavam sem rastreabilidade.

**Fonte**: Tabela `Si_Texto_Termo` sem campos de versionamento

**Destino no RF Moderno**: **SUBSTITUÍDO** por RN-TRM-081-04 (Versionamento Automático com Histórico Imutável)

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item / Funcionalidade | Existe no Legado | Existe no RF-081 Moderno | Observação |
|----------------------|------------------|-------------------------|------------|
| **Criação de Termo Customizado por Tipo de Ativo** | ❌ Não | ✅ Sim | Legado tinha termo genérico (não específico por tipo de equipamento) |
| **Versionamento Automático** | ❌ Não | ✅ Sim | Legado sobrescrevia versão anterior |
| **Assinatura Digital (SignaturePad)** | ❌ Não | ✅ Sim | Legado tinha apenas checkbox simples |
| **Validação de CPF via BrasilAPI** | ❌ Não | ✅ Sim | Legado não validava identidade |
| **Captura de Geolocalização (IP + GPS)** | ❌ Não | ✅ Sim | Legado não capturava contexto do aceite |
| **Timestamp UTC Sincronizado (NTP)** | ❌ Não | ✅ Sim | Legado usava datetime local |
| **Notificações Automáticas de Vencimento** | ❌ Não | ✅ Sim | Legado exigia envio manual por gestor |
| **Cálculo Automático de Penalidades** | ❌ Não | ✅ Sim | Legado calculava manualmente em planilha |
| **Revogação Formal de Termo** | ❌ Não | ✅ Sim | Legado não tinha fluxo de devolução formal |
| **Comprovante PDF com QRCode** | ❌ Não | ✅ Sim | Legado não gerava documento de comprovação |
| **Dashboard de Aceites** | ❌ Não | ✅ Sim | Legado tinha apenas relatórios SSRS estáticos |
| **Integração com Movimentação de Ativos (RF-027)** | ❌ Não | ✅ Sim | Legado não integrava com workflows |
| **Auditoria LGPD Completa** | ❌ Não | ✅ Sim | Legado não rastreava contexto de aceites |
| **Multi-idioma (i18n)** | ❌ Não | ✅ Sim | Legado hardcoded em português |
| **Multi-tenancy (Row-Level Security)** | ❌ Parcial | ✅ Sim | Legado usava bancos separados |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Abandonar Tabelas Legadas e Criar Modelo Novo

**Motivo**: Tabelas legadas (`Si_Texto_Termo`, `Usuario_Envio_TermoResponsabilidade`) não suportam versionamento, auditoria ou campos obrigatórios para LGPD/SOX.

**Impacto**: **Alto** - Requer migração de dados históricos (se houver) ou abandono completo do legado.

**Data**: 2025-12-31

---

### Decisão 2: Implementar Versionamento Automático Imutável

**Motivo**: Conformidade LGPD/SOX exige rastreamento de qual versão cada usuário aceitou. Legado não suportava isso.

**Impacto**: **Médio** - Adiciona complexidade no modelo de dados (tabela `TermoVersao`), mas essencial para auditoria.

**Data**: 2025-12-31

---

### Decisão 3: Substituir Checkbox por Assinatura Digital

**Motivo**: Checkbox simples não tem valor legal. Assinatura digital (SignaturePad) cria prova forense de aceite.

**Impacto**: **Médio** - Exige integração com biblioteca JavaScript no frontend.

**Data**: 2025-12-31

---

### Decisão 4: Migrar de Multi-Database para Row-Level Security

**Motivo**: Legado tinha banco separado por cliente (dificulta consolidação). Moderno usa banco único com isolamento por `ClienteId`.

**Impacto**: **Alto** - Requer consolidação de bancos legados em banco único moderno.

**Data**: 2025-12-31

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de Dados Históricos** | Alto | Média | Script de migração ETL validado em ambiente de teste antes de produção |
| **Usuários Não Familiarizados com Assinatura Digital** | Médio | Alta | Vídeo tutorial + tooltip in-app explicando como assinar |
| **Notificações Excessivas (Spam)** | Médio | Média | Configuração de throttling (máximo 3 emails por dia) |
| **Falha na Integração com BrasilAPI** | Alto | Baixa | Fallback para validação offline (regex CPF + dígito verificador) |
| **Performance do Job de Notificações** | Médio | Baixa | Job executado em horário de baixo uso (madrugada) |
| **Resistência de Gestores ao Novo Fluxo** | Médio | Média | Workshop de capacitação + documentação passo-a-passo |

---

## 9. RASTREABILIDADE (LEGADO → MODERNO)

| Elemento Legado | Referência RF-081 Moderno | Status |
|----------------|--------------------------|--------|
| `Si_Texto_Termo` (tabela) | `TermoResponsabilidade` (entidade) | **SUBSTITUÍDO** |
| `Usuario_Envio_TermoResponsabilidade` (tabela) | `AceiteTermo` (entidade) | **SUBSTITUÍDO** |
| Aceite via checkbox | Aceite via SignaturePad (assinatura digital) | **SUBSTITUÍDO** |
| Envio manual de notificações | Job Hangfire automático | **SUBSTITUÍDO** |
| Cálculo manual de penalidades | Service `CalculadorPenuldadeService` | **SUBSTITUÍDO** |
| Relatório SSRS estático | Dashboard Angular com D3.js | **SUBSTITUÍDO** |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Criação do RL-RF081 com referências ao sistema legado | Claude Code |

---

**Última Atualização**: 2025-12-31
**Autor**: Claude Code

---

[← Voltar ao RF-081](./RF081.md)

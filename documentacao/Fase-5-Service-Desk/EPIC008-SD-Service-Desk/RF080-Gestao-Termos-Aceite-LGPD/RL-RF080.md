# RL-RF080 — Referência ao Legado (Gestão de Termos de Aceite e LGPD)

**Versão:** 1.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-080
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Arquitetura Geral

- **Arquitetura:** Monolítica WebForms (ASP.NET 4.x)
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms
- **Banco de Dados:** SQL Server 2012+ (`Ativvus_Login`)
- **Multi-tenant:** Não (dados compartilhados entre empresas)
- **Auditoria:** Inexistente (apenas logs de erro)
- **Configurações:** Web.config hardcoded

### Características Técnicas

- Sem versionamento de termos (apenas update direto)
- Tabela `Si_Texto_Termo` com chave composta `(Pagina, Caixa)`
- Tabela `Usuario_Envio_TermoResponsabilidade` com registro simples de envio
- Sem consentimentos granulares
- Sem revogação de consentimento
- Sem portabilidade de dados
- Sem anonimização
- Sem dashboard de conformidade
- Sem notificações automáticas

---

## 2. TELAS DO LEGADO

### Tela: Login.aspx

- **Caminho:** `ic1_legado/IControlIT/Login.aspx`
- **Responsabilidade:** Exibir termo de responsabilidade antes de login

#### Comportamento

1. Usuário acessa página de login
2. Antes de autenticar, sistema verifica se termo foi aceito
3. Se não aceito, exibe checkbox "Li e aceito o termo de responsabilidade"
4. Texto do termo carregado de `Si_Texto_Termo` onde `Pagina='Login'` e `Caixa='Aceite'`
5. Usuário obrigado a marcar checkbox para prosseguir
6. Após aceite, registro inserido em `Usuario_Envio_TermoResponsabilidade`
7. Login permitido

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| chkAceiteTermo | Checkbox | Sim | Checkbox de aceite |
| lblTermoTexto | Label | - | Texto do termo carregado do banco |
| txtLogin | TextBox | Sim | Login do usuário |
| txtSenha | TextBox | Sim | Senha do usuário |

#### Comportamentos Implícitos

- **Sem versionamento:** Termo pode ser alterado sem histórico
- **Sem re-aceite:** Usuário que já aceitou não vê termo novamente mesmo se conteúdo mudar
- **Sem IP ou User-Agent:** Registro não captura origem do aceite
- **Sem timestamp:** Apenas `DataCadastro` registrada
- **Sem auditoria:** Nenhum log de quem aceitou ou quando
- **Hardcoded:** Texto do termo fixo em `Pagina='Login'`, `Caixa='Aceite'`

---

### Tela: frmConfiguracao.aspx

- **Caminho:** `ic1_legado/IControlIT/Configuracao/frmConfiguracao.aspx`
- **Responsabilidade:** Administração manual de texto de termo

#### Comportamento

1. Administrador acessa tela de configuração
2. Seleciona combo de páginas (Login, Termo, etc.)
3. Seleciona combo de caixas (Aceite, Privacidade, etc.)
4. Sistema carrega texto atual de `Si_Texto_Termo`
5. Administrador edita texto em `TextBox` multiline
6. Clica "Salvar" → UPDATE direto no banco (sem versionamento)
7. Nenhuma notificação enviada aos usuários
8. Sem diff visual de mudanças

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| cmbPagina | ComboBox | Sim | Páginas disponíveis |
| cmbCaixa | ComboBox | Sim | Seções da página |
| txtTextoTermo | TextBox | Sim | Conteúdo do termo (max 8000 chars) |
| btnSalvar | Button | - | Salva alteração |

#### Comportamentos Implícitos

- **Sem validação de HTML:** Aceita qualquer HTML (risco XSS)
- **Sem versionamento:** Alteração sobrescreve texto anterior sem histórico
- **Sem notificação:** Usuários não são avisados de mudanças
- **Sem diff:** Administrador não vê o que mudou
- **Limite de 8000 caracteres:** Restrição do SQL Server `VARCHAR(8000)`

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `ObterTextoPagina(pagina, caixa)` | WSSeguranca.asmx.vb (inferido) | Retorna texto de termo do banco | SELECT simples, sem cache |
| `SalvarTextoTermoEdit(pagina, caixa, texto)` | WSSeguranca.asmx.vb (inferido) | Salva alteração de termo | UPDATE direto, sem versionamento |
| `VerificarAceiteUsuario(usuarioId)` | WSSeguranca.asmx.vb (inferido) | Verifica se usuário aceitou termo | SELECT em `Usuario_Envio_TermoResponsabilidade` |
| `RegistrarAceiteUsuario(usuarioId)` | WSSeguranca.asmx.vb (inferido) | Registra aceite de termo | INSERT simples sem auditoria |

**Nota:** WebServices não encontrados no código fornecido, mas inferidos a partir do comportamento descrito no RF v1.0.

---

## 4. TABELAS LEGADAS

### Tabela: Si_Texto_Termo

```sql
CREATE TABLE [dbo].[Si_Texto_Termo](
    [Pagina] [varchar](50) NOT NULL,
    [Caixa] [varchar](50) NOT NULL,
    [Texto] [varchar](8000) NOT NULL,
    CONSTRAINT [PK_Si_Texto_De_Acordo] PRIMARY KEY CLUSTERED
    (
        [Pagina] ASC,
        [Caixa] ASC
    )
)
```

**Finalidade:** Armazenar textos de termos por página e seção.

**Problemas Identificados:**

1. **Chave composta não semântica:** `(Pagina, Caixa)` dificulta rastreabilidade
2. **Sem versionamento:** Alteração sobrescreve dados anteriores
3. **Limite de 8000 caracteres:** Insuficiente para termos longos
4. **Sem multi-idioma:** Apenas um idioma por página/caixa
5. **Sem auditoria:** Nenhum campo de `DataCriacao`, `CriadoPor`, `DataAlteracao`, `AlteradoPor`
6. **Sem soft delete:** Exclusão é permanente
7. **Sem tenant:** Dados compartilhados entre empresas (risco LGPD)

---

### Tabela: Usuario_Envio_TermoResponsabilidade

```sql
CREATE TABLE [dbo].[Usuario_Envio_TermoResponsabilidade](
    [Id_Usuario] [int] NOT NULL,
    [Id_Ativo] [int] NOT NULL,
    [Empresa] [varchar](50) NOT NULL,
    [DataCadastro] [datetime] NOT NULL,
    [QtdEnvios] [int] NULL,
    [DataUltEnvio] [datetime] NULL,
    [Url_Termo] [varchar](200) NULL,
    [Token] [varchar](250) NULL,
    [Token_Validade] [datetime] NULL
)
```

**Finalidade:** Registrar aceite de termo de responsabilidade por usuário.

**Problemas Identificados:**

1. **Sem chave primária:** Tabela sem PK definida
2. **Sem versionamento:** Não registra qual versão do termo foi aceita
3. **Sem IP ou User-Agent:** Não captura origem do aceite (crítico para LGPD)
4. **Sem timestamp ISO 8601:** `DataCadastro` em formato SQL Server (não portável)
5. **Campos confusos:** `Id_Ativo`, `QtdEnvios`, `DataUltEnvio` sem semântica clara
6. **Token sem uso:** `Token` e `Token_Validade` nunca utilizados
7. **Empresa como VARCHAR:** Deveria ser FK para tabela de empresas
8. **Sem auditoria:** Nenhum campo de auditoria (quem criou, quando, de onde)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Aceite Único Sem Re-aceite

**Descrição:** Usuário que já aceitou termo não precisa aceitar novamente mesmo se conteúdo mudar.

**Fonte:** `Login.aspx.vb`, linha ~120 (inferido do RF v1.0)

**Impacto:** Violação LGPD Art. 5 (transparência). Usuário pode não estar ciente de mudanças importantes.

**Destino:** **SUBSTITUÍDO** por RN-RF080-002 (Versionamento Automático com re-aceite obrigatório).

---

### RL-RN-002: Texto de Termo Sem Sanitização

**Descrição:** Texto de termo aceita qualquer HTML sem validação (risco XSS).

**Fonte:** `frmConfiguracao.aspx.vb`, linha ~80 (inferido)

**Impacto:** Risco de segurança crítico. Administrador mal-intencionado pode injetar código JavaScript.

**Destino:** **SUBSTITUÍDO** por RN-RF080-015 (Proteção Contra XSS com HtmlSanitizer).

---

### RL-RN-003: Sem Consentimentos Granulares

**Descrição:** Sistema não diferencia consentimento para Marketing, Analytics, Cookies ou Compartilhamento. Aceite é "tudo ou nada".

**Fonte:** Ausência de tabela de consentimentos no legado

**Impacto:** Violação LGPD Art. 8 (consentimento deve ser específico e granular).

**Destino:** **SUBSTITUÍDO** por RN-RF080-003 (Consentimentos Granulares).

---

### RL-RN-004: Sem Revogação de Consentimento

**Descrição:** Usuário não pode revogar aceite de termo. Não há interface ou funcionalidade para isso.

**Fonte:** Ausência de funcionalidade no legado

**Impacto:** Violação LGPD Art. 18, IX (direito de revogar consentimento).

**Destino:** **SUBSTITUÍDO** por RN-RF080-004 (Revogação Imediata).

---

### RL-RN-005: Sem Portabilidade de Dados

**Descrição:** Usuário não pode exportar seus dados pessoais em formato estruturado.

**Fonte:** Ausência de funcionalidade no legado

**Impacto:** Violação LGPD Art. 18, V (direito de obter cópia dos dados).

**Destino:** **SUBSTITUÍDO** por RN-RF080-005 (Portabilidade de Dados).

---

### RL-RN-006: Sem Anonimização

**Descrição:** Sistema não implementa anonimização de dados após revogação ou exclusão.

**Fonte:** Ausência de funcionalidade no legado

**Impacto:** Violação LGPD Art. 16 (direito ao esquecimento).

**Destino:** **SUBSTITUÍDO** por RN-RF080-006 (Anonimização Irreversível).

---

### RL-RN-007: Auditoria Inexistente

**Descrição:** Sistema não registra IP, User-Agent, timestamp ISO 8601, hash do documento ou qualquer auditoria completa de aceites.

**Fonte:** Tabela `Usuario_Envio_TermoResponsabilidade` sem campos de auditoria

**Impacto:** Violação LGPD Art. 5 (responsabilização). Empresa não pode demonstrar conformidade.

**Destino:** **SUBSTITUÍDO** por RN-RF080-007 (Auditoria Completa com retenção de 5 anos).

---

### RL-RN-008: Sem Multi-idioma

**Descrição:** Termos armazenados em único idioma (português). Não há suporte a inglês ou espanhol.

**Fonte:** Tabela `Si_Texto_Termo` sem campo de idioma

**Impacto:** Violação LGPD Art. 5 (transparência). Usuário estrangeiro não compreende termo.

**Destino:** **SUBSTITUÍDO** por RN-RF080-010 (Multi-idioma pt-BR, en-US, es-ES).

---

### RL-RN-009: Sem Notificações de Atualização

**Descrição:** Quando termo é atualizado, usuários não são notificados por e-mail, SMS ou in-app.

**Fonte:** Ausência de funcionalidade no legado

**Impacto:** Violação LGPD Art. 5 (transparência). Usuário pode ser bloqueado sem saber por quê.

**Destino:** **SUBSTITUÍDO** por RN-RF080-009 (Notificações Multi-Canal).

---

### RL-RN-010: Sem Dashboard de Conformidade

**Descrição:** Não há visualização de métricas de aceites, revogações ou conformidade.

**Fonte:** Ausência de funcionalidade no legado

**Impacto:** Empresa não pode demonstrar aderência à LGPD em caso de fiscalização.

**Destino:** **SUBSTITUÍDO** por RN-RF080-011 (Dashboard de Conformidade).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Existe no Legado | Existe no RF Moderno | Observação |
|-----|----------------|---------------------|------------|
| Aceite de termo no login | ✅ Sim | ✅ Sim | Mantido, mas modernizado |
| Versionamento de termos | ❌ Não | ✅ Sim | **GAP CRÍTICO** |
| Re-aceite após atualização | ❌ Não | ✅ Sim | **GAP CRÍTICO** |
| Consentimentos granulares | ❌ Não | ✅ Sim | **GAP CRÍTICO** (LGPD Art. 8) |
| Revogação de consentimento | ❌ Não | ✅ Sim | **GAP CRÍTICO** (LGPD Art. 18, IX) |
| Portabilidade de dados | ❌ Não | ✅ Sim | **GAP CRÍTICO** (LGPD Art. 18, V) |
| Anonimização | ❌ Não | ✅ Sim | **GAP CRÍTICO** (LGPD Art. 16) |
| Auditoria completa | ❌ Não | ✅ Sim | **GAP CRÍTICO** (LGPD Art. 5) |
| Dashboard de conformidade | ❌ Não | ✅ Sim | **GAP CRÍTICO** |
| Notificações multi-canal | ❌ Não | ✅ Sim | **GAP IMPORTANTE** |
| Multi-idioma | ❌ Não | ✅ Sim | **GAP IMPORTANTE** |
| Assinatura digital A1/A3 | ❌ Não | ✅ Sim | **NOVO RECURSO** |
| Administração manual | ✅ Sim | ✅ Sim | Mantido com melhorias |
| Armazenamento em banco | ✅ Sim | ✅ Sim | Migrado para PostgreSQL |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Substituir Tabela `Si_Texto_Termo`

**Descrição:** Criar nova tabela `termos` com versionamento, multi-idioma e auditoria completa.

**Motivo:** Tabela legada não suporta versionamento, multi-idioma ou auditoria. Limite de 8000 caracteres insuficiente.

**Impacto:** **ALTO** - Migração de dados necessária. Termos atuais devem ser importados como versão 1.

**Rastreabilidade:**
- Legado: `Si_Texto_Termo`
- Moderno: `termos` + `termo_versoes`

---

### Decisão 2: Substituir Tabela `Usuario_Envio_TermoResponsabilidade`

**Descrição:** Criar nova tabela `termo_aceites` com auditoria completa (IP, User-Agent, hash, timestamp ISO 8601).

**Motivo:** Tabela legada não captura origem do aceite, não tem versionamento e não suporta auditoria LGPD.

**Impacto:** **ALTO** - Migração de dados necessária. Aceites atuais devem ser importados com `ip_origem = NULL` (desconhecido).

**Rastreabilidade:**
- Legado: `Usuario_Envio_TermoResponsabilidade`
- Moderno: `termo_aceites`

---

### Decisão 3: Criar Tabela de Consentimentos Granulares

**Descrição:** Criar tabela `consentimentos_usuario` com tipos: Marketing, Analytics, Cookies, Compartilhamento.

**Motivo:** Legado não tem consentimentos granulares (violação LGPD Art. 8).

**Impacto:** **ALTO** - Nova funcionalidade sem equivalente legado. Usuários existentes devem ser migrados com consentimento padrão (todos negados, exceto obrigatórios).

**Rastreabilidade:**
- Legado: **INEXISTENTE**
- Moderno: `consentimentos_usuario`

---

### Decisão 4: Implementar Versionamento Automático

**Descrição:** Criar tabela `termo_versoes` com histórico completo e diff visual.

**Motivo:** Legado não tem versionamento (violação LGPD Art. 5 - transparência).

**Impacto:** **MÉDIO** - Nova funcionalidade. Termos atuais serão versão 1.

**Rastreabilidade:**
- Legado: **INEXISTENTE**
- Moderno: `termo_versoes`

---

### Decisão 5: Migrar de SQL Server para PostgreSQL

**Descrição:** Migrar banco de dados de SQL Server (`Ativvus_Login`) para PostgreSQL.

**Motivo:** PostgreSQL é open-source, suporta TDE (Transparent Data Encryption), melhor suporte a JSON e compliance.

**Impacto:** **ALTO** - Migração de dados completa. Scripts de migração necessários.

**Rastreabilidade:**
- Legado: SQL Server 2012+ (`Ativvus_Login`)
- Moderno: PostgreSQL 15+ (novo banco)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Perda de dados de aceites antigos** | Crítico | Média | Migração com validação completa. Backup antes de migrar. |
| **Usuários bloqueados após migração** | Alto | Alta | Aceites legados serão importados. Notificação prévia aos usuários. |
| **Termos truncados (>8000 chars)** | Médio | Baixa | PostgreSQL suporta TEXT ilimitado. Validar tamanho antes de migrar. |
| **Charset incompatível (SQL Server → PostgreSQL)** | Médio | Média | Usar UTF-8 em PostgreSQL. Validar acentuação e caracteres especiais. |
| **Performance degradada em consultas** | Baixo | Baixa | Índices otimizados em PostgreSQL. Cache distribuído (Redis). |
| **Usuários não entendem novos consentimentos** | Médio | Alta | Tutorial e tooltips explicativos na interface. E-mail de orientação. |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|----------------|---------------|--------|
| `Si_Texto_Termo` | RN-RF080-002 (Versionamento) | SUBSTITUÍDO |
| `Usuario_Envio_TermoResponsabilidade` | RN-RF080-007 (Auditoria) | SUBSTITUÍDO |
| Login.aspx (aceite de termo) | RN-RF080-001 (Aceite Obrigatório) | ASSUMIDO |
| frmConfiguracao.aspx (administração) | RN-RF080-014 (Validação) | SUBSTITUÍDO |
| Stored Procedures (inferidas) | - | SUBSTITUÍDAS (lógica movida para CQRS) |
| RL-RN-003 (Sem consentimentos) | RN-RF080-003 (Consentimentos Granulares) | SUBSTITUÍDO |
| RL-RN-004 (Sem revogação) | RN-RF080-004 (Revogação Imediata) | SUBSTITUÍDO |
| RL-RN-005 (Sem portabilidade) | RN-RF080-005 (Portabilidade) | SUBSTITUÍDO |
| RL-RN-006 (Sem anonimização) | RN-RF080-006 (Anonimização) | SUBSTITUÍDO |
| RL-RN-007 (Sem auditoria) | RN-RF080-007 (Auditoria Completa) | SUBSTITUÍDO |
| RL-RN-008 (Sem multi-idioma) | RN-RF080-010 (Multi-idioma) | SUBSTITUÍDO |
| RL-RN-009 (Sem notificações) | RN-RF080-009 (Notificações Multi-Canal) | SUBSTITUÍDO |
| RL-RN-010 (Sem dashboard) | RN-RF080-011 (Dashboard de Conformidade) | SUBSTITUÍDO |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-31 | Referência completa ao legado do RF080 com 100% dos itens destinados | Agência ALC - alc.dev.br |

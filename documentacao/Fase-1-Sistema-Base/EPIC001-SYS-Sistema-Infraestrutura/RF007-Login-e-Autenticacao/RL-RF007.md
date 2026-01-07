# RL-RF007 — Referência ao Legado: Login e Autenticação

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-007
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do sistema legado de autenticação (Session-based) que serve de base para refatoração JWT moderna, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

O sistema IControlIT original implementava autenticação via **ASP.NET Session** com armazenamento de credenciais em banco SQL Server separado (`Ativvus_Login`).

### 1.1 Arquitetura

- **Tipo:** Monolítica WebForms (Cliente-Servidor)
- **Linguagem/Stack:** VB.NET + ASP.NET Web Forms (.NET Framework 4.x)
- **Servidor:** IIS (Internet Information Services)
- **Banco de Dados:** SQL Server (18 bases separadas por cliente)
- **Multi-tenant:** Não (1 base de dados por cliente físico)
- **Auditoria:** Parcial (logs manuais via stored procedures)
- **Configurações:** Web.config + Banco de dados (`Config_Geral`)

### 1.2 Bases de Dados Envolvidas

| Base | Propósito | Observação |
|------|-----------|------------|
| `Ativvus_Login` | Autenticação global (usuários de todos os clientes) | Base centralizada |
| `Cliente_XXXX` | Dados operacionais de cada cliente | 1 base por cliente (18 bases no total) |

**Problema identificado:** Gestão complexa de múltiplas bases, dificuldade de backup e migração.

---

## 2. TELAS DO LEGADO

### Tela: Login.aspx

- **Caminho:** `ic1_legado/IControlIT/Login.aspx`
- **Responsabilidade:** Tela principal de login do sistema

#### Campos

| Campo | Tipo | Obrigatório | Validação Legado | Observações |
|-------|------|-------------|------------------|-------------|
| `txtNmUsuario` | TextBox | Sim | Nenhuma (validação no code-behind) | Nome de usuário (não era email) |
| `txtSenha` | TextBox (PasswordChar) | Sim | Nenhuma | Senha criptografada via `Fu_Criptografa` |
| `ddlEmpresa` | DropDownList | Sim | Preenchido dinamicamente | Lista de clientes disponíveis |
| `chkLembrar` | CheckBox | Não | - | "Lembrar-me" (armazenava cookie não seguro) |

#### Comportamentos Implícitos

1. **Validação de campos vazia apenas no cliente** (JavaScript básico)
   - Backend aceitava campos vazios se JS fosse desabilitado
   - **Risco:** Vulnerabilidade a ataques automatizados

2. **Senha criptografada com função customizada** `Fu_Criptografa`
   - Usava chave fixa `'GUA@123'` (hard-coded)
   - Algoritmo proprietário baseado em manipulação ASCII
   - **Problema:** Não usa salt, vulnerável a rainbow tables

3. **Sessão ASP.NET com timeout configurável no IIS**
   - Padrão: 20 minutos de inatividade
   - Configuração global (não por usuário)
   - **Problema:** Não havia renovação automática

4. **Cookie "Lembrar-me" armazenava senha em texto plano**
   - Cookie: `IControlIT_User` e `IControlIT_Pass`
   - **Problema crítico:** Senha em texto plano no cookie

5. **Redirecionamento para tela inicial sem validação de primeiro acesso**
   - Usuários com senha temporária podiam usar indefinidamente
   - **Problema:** Senhas fracas geradas pelo admin ficavam permanentes

6. **Mensagem de erro específica revelava se email/senha estava errado**
   - "Usuário não encontrado" vs "Senha incorreta"
   - **Vulnerabilidade:** Enumeração de usuários

---

### Tela: EsqueciSenha.aspx

- **Caminho:** `ic1_legado/IControlIT/EsqueciSenha.aspx`
- **Responsabilidade:** Solicitação de recuperação de senha

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtEmail` | TextBox | Sim | Validação básica de @ |
| `btnEnviar` | Button | - | Envia email com nova senha |

#### Comportamentos Implícitos

1. **Gerava nova senha aleatória e enviava por email**
   - Senha: 8 caracteres alfanuméricos
   - **Problema:** Email com senha em texto plano (inseguro)

2. **Não havia confirmação de identidade**
   - Qualquer pessoa com email podia resetar senha de outro
   - **Vulnerabilidade:** Ataque de reset de senha

3. **Senha era alterada imediatamente no banco**
   - Mesmo sem confirmação do usuário
   - **Problema:** Usuário podia perder acesso se email estivesse incorreto

4. **Sem expiração de link/token**
   - Não havia conceito de token temporário
   - **Problema:** Recuperação não controlada

---

### Tela: NovaSenha.aspx

- **Caminho:** `ic1_legado/IControlIT/NovaSenha.aspx`
- **Responsabilidade:** Troca de senha (primeiro acesso ou manual)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| `txtSenhaAtual` | TextBox | Sim | Apenas se não for primeiro acesso |
| `txtNovaSenha` | TextBox | Sim | Sem validação de complexidade |
| `txtConfirmaSenha` | TextBox | Sim | Validação apenas de igualdade |

#### Comportamentos Implícitos

1. **Sem validação de requisitos mínimos de senha**
   - Aceitava senhas fracas como "123", "abc"
   - **Problema:** Política de segurança inexistente

2. **Sem histórico de senhas**
   - Usuário podia reutilizar mesma senha indefinidamente
   - **Problema:** Vulnerabilidade a ataques de replay

3. **Flag `Senha_Segura` não era utilizada corretamente**
   - Campo existia no banco mas não era verificado
   - **Problema:** Primeiro acesso não era forçado

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `Fu_Criptografa` | `dbo.Fu_Criptografa` (SQL Function) | Criptografia de senha | Chave fixa, algoritmo proprietário |
| `pa_si_Validacao_Global` | Stored Procedure | Validação de login | Retorna dados do usuário se válido |
| `Sd_SF_ValidaPrimeiroAcesso` | Package VB.NET | Verifica flag primeiro acesso | Lógica no code-behind |
| `Sd_SF_UpdateSenhaFortePrimeiroAcesso` | Package VB.NET | Atualiza senha forte | Marca flag `Senha_Segura = 1` |

---

## 4. TABELAS LEGADAS

### Tabela: Usuario_Global

**Banco:** `Ativvus_Login`
**Finalidade:** Armazenamento centralizado de usuários e credenciais

**DDL Original:**
```sql
CREATE TABLE [dbo].[Usuario_Global](
    [Id_Usuario] [int] IDENTITY(1,1) NOT NULL,
    [Nm_Usuario] [varchar](50) NOT NULL,
    [Senha] [varchar](50) NOT NULL,
    [Empresa] [varchar](50) NOT NULL,
    [EMail] [varchar](50) NULL,
    [Id_Facebook] [varchar](50) NULL,
    [Chave_Validacao] [varchar](50) NULL,
    [Chave_Validacao_App] [varchar](50) NULL,
    [Fl_Validacao_App] [int] NULL,
    [Fl_Validacao] [int] NOT NULL,
    [Token] [varchar](250) NULL,
    [Token_Validade] [datetime] NULL,
    [Senha_Segura] [smallint] NULL,
    CONSTRAINT [PK_Usuario_Global] PRIMARY KEY CLUSTERED ([Id_Usuario] ASC)
)

-- Índices
CREATE UNIQUE NONCLUSTERED INDEX [IX_Usuario_Global]
ON [dbo].[Usuario_Global] ([Nm_Usuario] ASC, [Senha] ASC)

CREATE NONCLUSTERED INDEX [ix_usuario_global_email]
ON [dbo].[Usuario_Global] ([EMail] ASC)

CREATE NONCLUSTERED INDEX [idx_Usuario_Global_Token]
ON [dbo].[Usuario_Global] ([Token] ASC, [Token_Validade] ASC)
```

**Problemas Identificados:**

1. **Senha em texto criptografado (não hash)**
   - Campo `Senha` armazena resultado de `Fu_Criptografa` (reversível)
   - **Impacto:** Se função for descoberta, todas as senhas são comprometidas

2. **Sem salt individual**
   - Mesma senha gera sempre o mesmo valor criptografado
   - **Impacto:** Vulnerável a rainbow tables

3. **Campo `Nm_Usuario` não é email**
   - Login com nome de usuário arbitrário (ex: "joao.silva")
   - **Problema:** Nomes duplicados entre clientes

4. **Campo `EMail` pode ser NULL**
   - Usuários sem email não podem recuperar senha
   - **Problema:** Recuperação inviável

5. **Campos `Token` e `Token_Validade` não eram usados**
   - Implementação incompleta de sistema de tokens
   - **Problema:** Funcionalidade não finalizada

6. **Campo `Senha_Segura` (flag) ignorada**
   - Não forçava troca de senha no primeiro acesso
   - **Problema:** Senhas temporárias permanentes

7. **Sem auditoria de tentativas de login**
   - Não registrava falhas ou sucessos
   - **Problema:** Impossível rastrear ataques

8. **Índice único em `[Nm_Usuario, Senha]`**
   - Permite mesma senha para múltiplos usuários
   - **Problema:** Vulnerabilidade se um usuário for comprometido

---

### Tabela: Config_Geral

**Banco:** Cada `Cliente_XXXX`
**Finalidade:** Configurações gerais do sistema por cliente

**Campos Relevantes:**

| Campo | Tipo | Descrição | Valor Legado |
|-------|------|-----------|--------------|
| `Tempo_Sessao` | int | Timeout de sessão (minutos) | 20 |
| `Senha_Minima` | int | Tamanho mínimo da senha | NULL (não validado) |
| `Validade_Senha` | int | Dias para expiração de senha | NULL (não implementado) |

**Problemas:**
- Configurações não eram aplicadas (existiam mas não eram lidas pelo código)
- Cada cliente tinha configuração independente (difícil padronizar)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras encontradas no código VB.NET que **não estavam documentadas** formalmente:

### RL-RN-001: Sessão Compartilhada Entre Abas
**Descrição:** Sistema permitia múltiplas sessões simultâneas do mesmo usuário em abas diferentes.
**Fonte:** `Login.aspx.vb` - Não havia validação de sessão única.
**Impacto:** Usuário podia logar em múltiplos dispositivos/abas sem restrição.
**Destino:** SUBSTITUÍDO - Sistema moderno permite sessões múltiplas mas rastreadas.

### RL-RN-002: Logout Não Invalidava Cookie "Lembrar-me"
**Descrição:** Fazer logout não removia cookie persistente, permitindo login automático.
**Fonte:** `Logout.aspx.vb` - Apenas `Session.Abandon()`, cookie não era deletado.
**Impacto:** Risco de acesso não autorizado em computadores compartilhados.
**Destino:** DESCARTADO - Cookie "Lembrar-me" não será implementado (inseguro).

### RL-RN-003: Criptografia Reversível de Senha
**Descrição:** Senha era criptografada (não hash), permitindo descriptografar.
**Fonte:** `dbo.Fu_Criptografa` - Função SQL customizada.
**Impacto:** Se chave `'GUA@123'` for descoberta, todas as senhas são comprometidas.
**Destino:** SUBSTITUÍDO - BCrypt hash irreversível com salt aleatório.

### RL-RN-004: Banco de Dados Separado Por Cliente
**Descrição:** Cada cliente tinha banco SQL Server físico separado.
**Fonte:** Arquitetura de infra (18 bases).
**Impacto:** Gestão complexa, backups separados, dificuldade de migração.
**Destino:** SUBSTITUÍDO - Row-Level Security (RLS) em banco único.

### RL-RN-005: Validação de Email Apenas Frontend
**Descrição:** Validação de formato de email apenas em JavaScript (client-side).
**Fonte:** `Login.aspx` - Validação via `RegularExpressionValidator`.
**Impacto:** Backend aceitava emails inválidos se JS fosse desabilitado.
**Destino:** SUBSTITUÍDO - Validação obrigatória no backend (.NET FluentValidation).

### RL-RN-006: Mensagens de Erro Específicas
**Descrição:** Sistema revelava se problema era no usuário ou senha.
**Fonte:** `pa_si_Validacao_Global` - Mensagens distintas.
**Impacto:** Ataque de enumeração de usuários (descobrir emails válidos).
**Destino:** SUBSTITUÍDO - Mensagem genérica "Email ou senha incorretos".

### RL-RN-007: Sem Bloqueio Por Tentativas Falhas
**Descrição:** Usuário podia tentar login infinitas vezes sem bloqueio.
**Fonte:** Ausência de lógica de bloqueio no código.
**Impacto:** Vulnerável a ataques de força bruta.
**Destino:** SUBSTITUÍDO - Bloqueio após 5 tentativas (30 minutos).

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Legado | RF-007 (Moderno) | Decisão |
|---------------|--------|------------------|---------|
| **Autenticação** | Session-based | JWT Bearer Token | SUBSTITUÍDO |
| **Login** | Nm_Usuario + Senha | Email + Senha | ASSUMIDO (conceito) |
| **Criptografia** | `Fu_Criptografa` (chave fixa) | BCrypt + SHA-256 | SUBSTITUÍDO |
| **Timeout** | 20 min (IIS global) | 8h JWT + 30 min inatividade | SUBSTITUÍDO |
| **Recuperação de Senha** | Email com senha nova | Link com token 24h | SUBSTITUÍDO |
| **Bloqueio por Tentativas** | NÃO EXISTE | 5 tentativas = 30 min bloqueio | NOVO |
| **Auditoria** | Log manual (parcial) | Automática via Middleware | SUBSTITUÍDO |
| **Primeiro Acesso** | Flag ignorada | Forçado obrigatoriamente | ASSUMIDO (conceito corrigido) |
| **Mensagem de Erro** | Específica (revela usuário) | Genérica | SUBSTITUÍDO |
| **Histórico de Senhas** | NÃO EXISTE | Últimas 5 senhas | NOVO |
| **Notificação Novo Dispositivo** | NÃO EXISTE | Email assíncrono | NOVO |
| **Multi-tenant** | 18 bases separadas | Row-Level Security (1 base) | SUBSTITUÍDO |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migrar de Session para JWT

**Descrição:** Substituir autenticação baseada em ASP.NET Session por tokens JWT.

**Motivo:**
- Session é stateful (requer armazenamento no servidor)
- JWT é stateless (escalável, permite microserviços)
- Suporte nativo a APIs RESTful (frontend Angular separado)

**Impacto:** ALTO
**Risco:** Usuários precisarão fazer login novamente após deploy (sessões antigas invalidadas)
**Mitigação:** Comunicação prévia, deploy em horário de baixa demanda

---

### Decisão 2: BCrypt Hash em Vez de Criptografia Customizada

**Descrição:** Substituir `Fu_Criptografa` por BCrypt hash com salt aleatório.

**Motivo:**
- BCrypt é padrão da indústria (OWASP recomendado)
- Salt aleatório por senha (impossível rainbow tables)
- Irreversível (mesmo DBA não consegue "ver" senha)

**Impacto:** ALTO
**Risco:** Senhas legadas não podem ser migradas diretamente (hash diferente)
**Mitigação:**
1. Forçar troca de senha no primeiro login após migração, OU
2. Script de migração one-time: descriptografar com `Fu_Criptografa` → Re-hash com BCrypt

---

### Decisão 3: Banco Único com Row-Level Security

**Descrição:** Consolidar 18 bases SQL Server em 1 banco único com isolamento por `EmpresaId`.

**Motivo:**
- Simplifica backup (1 base vs 18)
- Facilita queries cross-client (relatórios consolidados)
- Reduz custo de infra (licenças SQL Server)

**Impacto:** MUITO ALTO
**Risco:** Vazamento de dados entre clientes (bugs em RLS)
**Mitigação:**
- Testes exaustivos de isolamento de tenant
- Auditoria de todas as queries (garantir filtro por `EmpresaId`)
- Consultas padrão via repositórios (não permitir SQL direto)

---

### Decisão 4: Email como Login (em Vez de Nm_Usuario)

**Descrição:** Usar email como identificador único de login.

**Motivo:**
- Email é globalmente único (não precisa prefixo de cliente)
- Facilita recuperação de senha
- Padrão moderno (Gmail, Office 365, etc.)

**Impacto:** MÉDIO
**Risco:** Usuários antigos precisam ser migrados (Nm_Usuario → Email)
**Mitigação:**
- Script de migração: buscar email em `Usuario_Global.EMail`
- Usuários sem email: solicitar cadastro manual antes da migração
- Permitir login por `Nm_Usuario` (legacy) + email durante transição

---

### Decisão 5: Implementar Bloqueio Anti Brute-Force

**Descrição:** Bloquear usuário por 30 minutos após 5 tentativas falhas em 15 minutos.

**Motivo:**
- Sistema legado era vulnerável a ataques automatizados
- Conformidade com OWASP Top 10 (A07 - Identification and Authentication Failures)

**Impacto:** BAIXO
**Risco:** Usuários legítimos que erram senha podem ser bloqueados (UX negativa)
**Mitigação:**
- Mensagem clara com tempo restante
- Opção de admin desbloquear via painel
- Log de bloqueios para análise

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Vazamento de dados entre tenants (RLS)** | CRÍTICO | MÉDIA | Testes exaustivos, code review, queries via repositórios |
| **Senhas legadas incompatíveis com BCrypt** | ALTO | ALTA | Script de re-hash one-time, forçar troca de senha |
| **Usuários sem email cadastrado** | MÉDIO | ALTA | Levantamento prévio, cadastro manual antes da migração |
| **Sessões ativas perdidas no deploy** | MÉDIO | ALTA | Comunicação prévia, deploy em horário de baixa demanda |
| **Bloqueio indevido de usuários legítimos** | BAIXO | MÉDIA | Mensagem clara, admin pode desbloquear, logs de bloqueio |
| **Perda de histórico de logins antigos** | BAIXO | BAIXA | Exportar logs de `Usuario_Global` antes da migração |

---

## 9. ESTRATÉGIA DE MIGRAÇÃO DE DADOS

### 9.1 Migração de Usuários

**Fonte:** `Ativvus_Login.dbo.Usuario_Global`
**Destino:** `IControlIT.dbo.Usuario` (novo modelo)

**Script de Migração:**
```sql
-- Migração de usuários (pseudocódigo)
INSERT INTO IControlIT.dbo.Usuario
    (Id, Email, Nome, SenhaHash, EmpresaId, PrimeiroAcesso, DataCriacao)
SELECT
    Id_Usuario,
    COALESCE(EMail, Nm_Usuario + '@legado.local'), -- Fallback se sem email
    Nm_Usuario,
    NULL, -- Senha será rehashada ou forçar troca
    (SELECT Id FROM Empresa WHERE Codigo = Usuario_Global.Empresa),
    CASE WHEN Senha_Segura IS NULL OR Senha_Segura = 0 THEN 1 ELSE 0 END,
    GETDATE()
FROM Ativvus_Login.dbo.Usuario_Global
```

**Regras:**
1. Usuários **sem email válido**: criar email temporário `{Nm_Usuario}@legado.local`
2. **Senha**: opção A (forçar troca) ou opção B (re-hash com BCrypt)
3. **Flag Primeiro Acesso**: se `Senha_Segura` for NULL ou 0 → `PrimeiroAcesso = true`
4. **EmpresaId**: mapear campo `Empresa` (varchar) para FK da tabela `Empresa` (Guid)

### 9.2 Migração de Histórico de Logins

**Fonte:** Logs manuais dispersos (não estruturados)
**Destino:** `IControlIT.dbo.AuditLog`

**Decisão:** DESCARTADO
**Justificativa:** Logs antigos não seguem padrão estruturado, custo/benefício de migração é baixo

---

## 10. LIÇÕES APRENDIDAS

1. **Criptografia customizada é risco de segurança**
   - Sempre usar bibliotecas testadas (BCrypt, Argon2)
   - Nunca inventar algoritmo proprietário

2. **Validação apenas no cliente é vulnerabilidade**
   - Backend DEVE validar TUDO (não confiar no frontend)

3. **Mensagens de erro específicas facilitam ataques**
   - Mensagens genéricas protegem contra enumeração

4. **Múltiplas bases de dados dificultam gestão**
   - Multi-tenancy via Row-Level Security é mais escalável

5. **Auditoria manual é insuficiente**
   - Middleware automático garante rastreabilidade completa

6. **Senhas sem política de complexidade são fracas**
   - Requisitos mínimos DEVEM ser validados no backend

7. **Session-based não escala para APIs modernas**
   - JWT permite frontend/backend separados e microserviços

8. **Cookie "Lembrar-me" com senha em texto é crítico**
   - NUNCA armazenar credenciais em cookies

---

## 11. RASTREABILIDADE

| Elemento Legado | Referência RF-007 | Status |
|----------------|-------------------|--------|
| `Login.aspx` | RN-AUTH-001 (Login com email+senha) | MIGRADO |
| `EsqueciSenha.aspx` | RN-AUTH-006 (Token recuperação 24h) | MIGRADO |
| `NovaSenha.aspx` | RN-AUTH-004 (Requisitos mínimos), RN-AUTH-007 (Histórico) | MIGRADO |
| `Fu_Criptografa` | RN-AUTH-005 (BCrypt case-sensitive) | SUBSTITUÍDO |
| `Usuario_Global.Nm_Usuario` | RN-AUTH-001 (Email como login) | SUBSTITUÍDO |
| `Usuario_Global.Senha` | RN-AUTH-005 (BCrypt hash) | SUBSTITUÍDO |
| `Usuario_Global.Token` | RN-AUTH-002 (JWT Token) | SUBSTITUÍDO |
| `pa_si_Validacao_Global` | RN-AUTH-001 (LoginCommand handler) | SUBSTITUÍDO |
| ASP.NET Session | RN-AUTH-002 (JWT com 8h) | SUBSTITUÍDO |
| Sem bloqueio brute-force | RN-AUTH-003 (5 tentativas = 30 min) | NOVO |
| Sem histórico senhas | RN-AUTH-007 (Últimas 5 senhas) | NOVO |
| Sem auditoria estruturada | RN-AUTH-010 (AuditLog automático) | NOVO |

---

## 12. ANEXOS

### 12.1 Função Legada `Fu_Criptografa`

**Localização:** `Ativvus_Login.dbo.Fu_Criptografa`

**Lógica (extraída em linguagem natural):**
1. Recebe senha em texto plano
2. Concatena com chave fixa `'GUA@123'`
3. Percorre cada caractere aplicando operações ASCII:
   - Converte para código ASCII
   - Soma/subtrai valores baseados na posição
   - Inverte ordem de alguns caracteres
4. Retorna string criptografada (50 caracteres max)

**Problemas:**
- Chave fixa (não usa salt aleatório)
- Reversível (conhecendo algoritmo, descriptografa)
- Vulnerável a rainbow tables (mesma senha = mesmo resultado)

**Destino:** DESCARTADO - Substituído por BCrypt

---

### 12.2 Stored Procedure `pa_si_Validacao_Global`

**Localização:** `Ativvus_Login.dbo.pa_si_Validacao_Global`

**Lógica (extraída em linguagem natural):**
1. Recebe `@Nm_Usuario` e `@Senha` (já criptografada)
2. Busca registro em `Usuario_Global` com `Nm_Usuario = @Nm_Usuario`
3. Se não encontrar → retorna "Usuário não encontrado" (VULNERABILIDADE)
4. Se encontrar, compara `Senha = @Senha`
5. Se senha incorreta → retorna "Senha incorreta" (VULNERABILIDADE)
6. Se válido:
   - Atualiza campo `Token` com GUID aleatório
   - Atualiza `Token_Validade` (não usado)
   - Retorna dados do usuário (Id, Nome, Email, Empresa)

**Problemas:**
- Mensagens específicas revelam se email existe
- Campo `Token` gerado mas não utilizado pelo sistema

**Destino:** SUBSTITUÍDO - `LoginCommandHandler` com mensagem genérica

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 2.0 | 2025-12-30 | Criação do RL separado do RF - Memória técnica completa do legado VB.NET/ASP.NET | Agência ALC - alc.dev.br |
| 1.0 | 2025-11-19 | Conteúdo legado estava mesclado no RF-007.md v1.0 (seções 3 e 4) | Claude Code (Architect Agent) |

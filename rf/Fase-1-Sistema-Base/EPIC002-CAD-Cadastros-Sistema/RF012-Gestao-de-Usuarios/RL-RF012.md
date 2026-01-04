# RL-RF012 — Referência ao Legado: Gestão de Usuários

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-012 (Gestão de Usuários do Sistema)
**Sistema Legado:** VB.NET + ASP.NET Web Forms (IControlIT v1.0)
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

### Características Gerais

- **Arquitetura:** Monolítica ASP.NET Web Forms
- **Linguagem:** VB.NET (code-behind) + ASPX (markup)
- **Banco de Dados:** SQL Server
- **Multi-tenant:** Sim (campo `Id_Conglomerado` em tabela Usuario)
- **Auditoria:** Parcial (apenas `Dt_Ultimo_Acesso`, sem logs detalhados de alterações)
- **Configurações:** Web.config + stored procedures no banco
- **Autenticação:** Session cookies ASP.NET + MD5 para senhas
- **Sessões:** ASP.NET Session State (in-process ou SQL Server)
- **Validação:** Mix de server-side (ASP.NET validators) e client-side (JavaScript inline)

### Problemas Identificados

1. **Segurança de Senhas:** MD5 é inseguro (quebrado desde 2004), facilmente reversível com rainbow tables
2. **SQL Injection:** Uso de SQL dinâmico via `cls_DB` sem parametrização adequada
3. **Performance:** ViewState pesado (50-200KB por request), PostBacks constantes
4. **Auditoria Limitada:** Apenas última data de acesso, sem histórico de alterações de dados
5. **Permissões Simplificadas:** RadioButtonLists com apenas 2 valores (Revogar/Permitir), falta granularidade
6. **Falta MFA:** Nenhuma autenticação de dois fatores
7. **Falta Detecção de Login Suspeito:** Sem geolocalização, sem alertas
8. **Sem Histórico de Senhas:** Permite reutilização infinita de senhas
9. **Sem Integração Active Directory:** Cada usuário deve ser criado manualmente no IControlIT
10. **Sessões sem Limite:** Não há controle de múltiplas sessões simultâneas

---

## 2. TELAS DO LEGADO

### Tela: Usuario.aspx

- **Caminho:** `ic1_legado/IControlIT/IControlIT/Cadastro/Usuario.aspx`
- **Responsabilidade:** CRUD de usuários do sistema com gestão básica de permissões

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|-------|------|-------------|-------------|
| Login | TextBox (`txtDescricao`) | ✅ Sim | MaxLength=50, único por conglomerado |
| Senha | Botão "Reiniciar Senha" | N/A | Gera senha temporária com confirmação JS |
| Idioma | DropDownList (`cboIdioma`) | ✅ Sim | Lista de idiomas do sistema |
| Grupo | DropDownList (`cboUsuarioGrupo`) | ✅ Sim | Agrupamento lógico de usuários |
| Perfil | DropDownList (`cboUsuarioPerfil`) | ✅ Sim | Perfil RBAC, **AutoPostBack=true** (reload página) |
| Acesso | DropDownList (`cboUsuarioPerfilAcesso`) | ✅ Sim | Nível de acesso |
| Permissão de Incluir | RadioButtonList (`optIncluir`) | ❌ Não | 1=Revogar, 2=Permitir |
| Permissão de Alterar | RadioButtonList (`optAlterar`) | ❌ Não | 1=Revogar, 2=Permitir |
| Permissão de Excluir | RadioButtonList (`optExcluir`) | ❌ Não | 1=Revogar, 2=Permitir |
| Conta de outro usuário | RadioButtonList (`optDetalhamentoConta`) | ❌ Não | 1=Revogar, 2=Permitir (controla visibilidade) |
| Contatos de outro usuário | RadioButtonList (`optDetalhamentoContato`) | ❌ Não | 1=Revogar, 2=Permitir (controla visibilidade) |
| Status para acesso | RadioButtonList (`optStatusUsuario`) | ❌ Não | 1=Revogar, 3=Permitir (valor 3 específico legado) |
| Permissão para Requisição | ListBox Duplo | ❌ Não | Origem/Destino com botões de mover (UI antiga) |
| Nome | TextBox (`txtNmConsumidor`) | ❌ Não | Readonly, vinculação opcional com consumidor |
| Chave do banco | TextBox (`txtIdentificacao`) | ❌ Não | Readonly, exibe GUID do usuário |

#### Comportamentos Implícitos

- **AutoPostBack no Perfil:** Ao alterar perfil, página recarrega para atualizar permissões disponíveis (ruim para UX)
- **Senha Temporária:** Botão "Reiniciar Senha" gera senha aleatória e força `Fl_Primeiro_Acesso = 1`
- **Validação JavaScript:** Confirmação antes de reiniciar senha (`confirm("Tem certeza?")`)
- **ViewState Pesado:** Todos os DropDownLists e RadioButtonLists adicionam 50-100KB de ViewState
- **RequiredFieldValidator:** Validação server-side para campos obrigatórios (Login, Idioma, Grupo, Perfil, Acesso)
- **ValidatorCalloutExtender:** Usa AjaxControlToolkit para exibir erros em callouts (biblioteca depreciada)

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|--------|-------|------------------|-------------|
| `WSAuth.asmx.vb::Login()` | `ic1_legado/IControlIT/WS/WSAuth.asmx.vb` | Autenticar usuário e criar sessão | Wrapper para `WSUsuario.Autenticar`, retorna session cookie ASP.NET |
| `WSAuth.asmx.vb::Logout()` | `ic1_legado/IControlIT/WS/WSAuth.asmx.vb` | Invalidar sessão ASP.NET | Limpa session state e cookies |
| `WSUsuario.asmx.vb::Autenticar()` | `ic1_legado/IControlIT/WS/WSUsuario.asmx.vb` | Validar credenciais (login/senha MD5) | Incrementa tentativas falhas, bloqueia após 5 |
| `WSUsuario.asmx.vb::Listar_Usuarios()` | `ic1_legado/IControlIT/WS/WSUsuario.asmx.vb` | Listar usuários com filtros (perfil, status) | Retorna DataSet com campos: Id_Usuario, Nm_Usuario, Email, Login, Nm_Perfil, Fl_Ativo, Fl_Bloqueado |
| `WSUsuario.asmx.vb::Criar_Usuario()` | `ic1_legado/IControlIT/WS/WSUsuario.asmx.vb` | Criar novo usuário com senha temporária | Define `Fl_Primeiro_Acesso = 1`, valida unicidade login/email |
| `WSUsuario.asmx.vb::Alterar_Senha()` | `ic1_legado/IControlIT/WS/WSUsuario.asmx.vb` | Alterar senha do usuário | Valida senha atual, atualiza com MD5, registra histórico, define expiração 90 dias |
| `WSUsuario.asmx.vb::Desbloquear_Usuario()` | `ic1_legado/IControlIT/WS/WSUsuario.asmx.vb` | Desbloquear usuário bloqueado | Zera `Tentativas_Falhas`, define `Fl_Bloqueado = 2`, limpa `Dt_Bloqueio` |

### Detalhamento dos Métodos

#### `WSUsuario.asmx.vb::Autenticar()`

**Parâmetros:**
- `pLogin` (String): Login do usuário
- `pSenha` (String): Senha em plaintext (⚠️ não usa HTTPS obrigatório)
- `pId_Conglomerado` (GUID): Identificador do conglomerado (multi-tenant)

**Comportamento:**
1. Calcula hash MD5 da senha fornecida
2. Executa query SQL dinâmica (⚠️ SQL Injection) buscando usuário com login/senha/conglomerado
3. Se encontrado:
   - Atualiza `Dt_Ultimo_Acesso = GETDATE()`
   - Zera `Tentativas_Falhas`
   - Retorna DataSet com dados do usuário (Id, Nome, Email, Perfil, Permissões)
4. Se não encontrado:
   - Incrementa `Tentativas_Falhas`
   - Se `Tentativas_Falhas >= 5`: define `Fl_Bloqueado = 1`, `Dt_Bloqueio = GETDATE()`
   - Retorna DataSet vazio

**Problemas:**
- MD5 inseguro
- SQL dinâmico vulnerável a SQL Injection
- Senha trafegada em plaintext (sem HTTPS forçado)
- Não registra IP, geolocalização ou dispositivo

#### `WSUsuario.asmx.vb::Alterar_Senha()`

**Parâmetros:**
- `pPakage` (String): Token de autenticação do webservice
- `pId_Usuario` (GUID): Identificador do usuário
- `pSenha_Atual` (String): Senha atual em plaintext
- `pSenha_Nova` (String): Nova senha em plaintext

**Comportamento:**
1. Valida `pPakage` via `cls_Config.Validar_Pakage()`
2. Valida senha atual calculando MD5 e comparando com hash armazenado
3. Se válido:
   - Calcula MD5 da nova senha
   - Insere hash anterior em `Usuario_Historico_Senha` (⚠️ sem limite de registros históricos)
   - Atualiza `Password_Hash` com novo MD5
   - Define `Dt_Expiracao_Senha = GETDATE() + 90 dias`
   - Retorna sucesso
4. Se inválido: retorna erro "Senha atual incorreta"

**Problemas:**
- MD5 inseguro
- Não valida força da nova senha (pode ser "123")
- Histórico de senhas sem limite (cresce infinitamente)
- Não previne reutilização das últimas 12 senhas

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|--------|------------|-------------------------|
| `Usuario` | Armazenar dados de usuários do sistema | MD5 em `Password_Hash`, falta campos MFA, falta `Permissoes_Customizadas`, falta campos AD |
| `Usuario_Historico_Senha` | Histórico de senhas alteradas | Sem limite de registros (pode crescer infinitamente), não previne reutilização |
| - (inexistente) | Sessões JWT/tokens | **Não existe**: legado usa ASP.NET Session State (in-memory ou SQL Server) |
| - (inexistente) | Auditoria de acessos | **Não existe**: apenas `Dt_Ultimo_Acesso` na tabela Usuario |
| - (inexistente) | Reset de senha via e-mail | **Não existe**: reset feito manualmente por admin via botão "Reiniciar Senha" |

### Tabela Usuario (Legado)

**Campos Principais:**

| Campo | Tipo | Nullable | Descrição | Problema |
|-------|------|----------|-----------|----------|
| `Id_Usuario` | UNIQUEIDENTIFIER | NOT NULL | PK, identificador único | ✅ OK |
| `Id_Conglomerado` | UNIQUEIDENTIFIER | NOT NULL | FK multi-tenant | ✅ OK |
| `Nm_Usuario` | NVARCHAR(120) | NOT NULL | Nome completo | ✅ OK |
| `Email` | NVARCHAR(100) | NOT NULL | E-mail (único por conglomerado) | ✅ OK |
| `Login` | NVARCHAR(50) | NOT NULL | Login (único por conglomerado) | ✅ OK |
| `Password_Hash` | NVARCHAR(255) | NOT NULL | Hash MD5 da senha | ⚠️ MD5 inseguro |
| `Id_Perfil` | UNIQUEIDENTIFIER | NOT NULL | FK perfil RBAC | ✅ OK |
| `Fl_Ativo` | INT | NOT NULL | 1=Ativo, 2=Inativo | ⚠️ Valores confusos (esperado 0/1) |
| `Fl_Bloqueado` | INT | NOT NULL | 1=Bloqueado, 2=Desbloqueado | ⚠️ Valores confusos (esperado 0/1) |
| `Tentativas_Falhas` | INT | NOT NULL | Contador de tentativas falhas | ✅ OK |
| `Dt_Ultimo_Acesso` | DATETIME | NULL | Último login bem-sucedido | ⚠️ Único campo de auditoria |
| `Dt_Expiracao_Senha` | DATETIME | NULL | Data de expiração da senha (90 dias) | ✅ OK |
| `Detalhamento_Conta` | INT | NOT NULL | Nível de visibilidade de contas (1, 2, 3) | ⚠️ Sem validação CHECK |
| `Detalhamento_Contato` | INT | NOT NULL | Nível de visibilidade de contatos (1, 2, 3) | ⚠️ Sem validação CHECK |
| `Fl_Desativado` | INT | NOT NULL | 1=Ativo, 2=Inativo, 3=Desativado Permanente | ⚠️ Valores confusos (esperado 0/1/2) |
| `Fl_Primeiro_Acesso` | INT | NOT NULL | 1=Sim (senha temporária), 0=Não | ✅ OK |

**Campos Ausentes (Necessários no Moderno):**

| Campo Necessário | Tipo | Descrição |
|------------------|------|-----------|
| `MFA_Secret` | NVARCHAR(100) | Secret TOTP para MFA |
| `Fl_MFA_Habilitado` | BIT | Flag MFA ativo |
| `Telefone_MFA` | NVARCHAR(20) | Telefone para backup MFA via SMS |
| `AD_Object_GUID` | UNIQUEIDENTIFIER | GUID do usuário no Active Directory |
| `AD_Sam_Account_Name` | NVARCHAR(50) | Login do AD |
| `Fl_Usuario_AD` | BIT | Flag usuário gerenciado pelo AD |
| `Permissoes_Customizadas` | NVARCHAR(MAX) | JSON com permissões extras além do perfil |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

### RL-RN-001: Bloqueio após 5 tentativas falhas

**Fonte:** `WSUsuario.asmx.vb::Autenticar()` linhas 45-60

**Descrição:** Ao atingir 5 tentativas falhas de login, sistema define `Fl_Bloqueado = 1` e `Dt_Bloqueio = GETDATE()`. Não há desbloqueio automático por timeout (apenas manual via `Desbloquear_Usuario()`).

**Destino:** **SUBSTITUÍDO** no RF moderno com desbloqueio automático após 15 minutos.

---

### RL-RN-002: Senha MD5 sem validação de força

**Fonte:** `WSUsuario.asmx.vb::Alterar_Senha()` linhas 120-135

**Descrição:** Sistema aceita qualquer senha (inclusive "123", "senha", etc.) e armazena hash MD5. Não há validação de comprimento mínimo, caracteres especiais, ou complexidade.

**Destino:** **SUBSTITUÍDO** no RF moderno com política de senha forte (mínimo 8 caracteres, maiúscula, minúscula, número, especial).

---

### RL-RN-003: Expiração de senha 90 dias

**Fonte:** `WSUsuario.asmx.vb::Alterar_Senha()` linha 145

**Descrição:** Ao alterar senha, sistema calcula `Dt_Expiracao_Senha = GETDATE() + 90 dias`. Porém, não há notificação antecipada (apenas bloqueia no login se expirada).

**Destino:** **ASSUMIDO** no RF moderno com adição de notificação 7 dias antes da expiração.

---

### RL-RN-004: Detalhamento de Conta/Contato (valores 1, 2, 3)

**Fonte:** Stored procedure `pa_Usuario` linhas 78-92

**Descrição:** Campos `Detalhamento_Conta` e `Detalhamento_Contato` aceitam valores 1 (Básico), 2 (Intermediário), 3 (Completo) para controle de visibilidade de dados sensíveis. Não há validação CHECK no banco, apenas no código VB.NET.

**Destino:** **ASSUMIDO** no RF moderno com adição de constraint CHECK no banco (valores 1, 2 ou 3 apenas).

---

### RL-RN-005: Status Desativado (valores 1, 2, 3)

**Fonte:** Stored procedure `pa_Usuario` linhas 103-115

**Descrição:** Campo `Fl_Desativado` aceita valores: 1 = Ativo, 2 = Inativo (temporário), 3 = Desativado Permanente (ex: funcionário desligado). Valor 3 requer aprovação especial para reativação. Porém, não há validação de permissão no código legado (qualquer admin pode reativar).

**Destino:** **SUBSTITUÍDO** no RF moderno com permissão específica `usuarios:reativar_permanente` (apenas Super Admin).

---

### RL-RN-006: Permissões customizadas via RadioButtonList

**Fonte:** Tela `Usuario.aspx` controles `optIncluir`, `optAlterar`, `optExcluir`

**Descrição:** Tela permite revogar ou permitir permissões individuais (Incluir, Alterar, Excluir) via RadioButtonList com valores 1 (Revogar) ou 2 (Permitir). Porém, essas permissões são armazenadas em campos separados na tabela (não em JSON estruturado), dificultando extensibilidade.

**Destino:** **SUBSTITUÍDO** no RF moderno com campo `Permissoes_Customizadas` (JSON) que permite adicionar permissões granulares.

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|------|--------|------------|------------|
| **Hash de Senha** | MD5 (inseguro) | BCrypt work factor 12 | ⚠️ Migração obrigatória (forçar troca senha) |
| **MFA** | Inexistente | TOTP via Google Authenticator | 🆕 Nova funcionalidade |
| **Histórico de Senhas** | Sem limite de registros | Últimas 12 senhas (limite fixo) | ⚠️ Limpeza de histórico legado |
| **Prevenção Reutilização** | Não previne | Proíbe reutilização das últimas 12 | 🆕 Nova regra |
| **Active Directory** | Inexistente | Autenticação LDAP + sincronização | 🆕 Nova integração |
| **Detecção Login Suspeito** | Inexistente | IP/país/horário anômalo com notificação | 🆕 Nova funcionalidade |
| **Auditoria** | Apenas `Dt_Ultimo_Acesso` | Histórico completo (sucesso/falha, IP, geolocalização) | 🆕 Nova tabela `Usuario_Historico_Acesso` |
| **Sessões Múltiplas** | Sem limite | Máximo 5 sessões simultâneas | 🆕 Nova regra |
| **Reset Senha** | Manual (botão admin) | Automático via e-mail com token | 🆕 Nova tabela `Usuario_Reset_Senha` |
| **Tokens JWT** | Session cookies ASP.NET | Access token (8h) + Refresh token (30 dias) | ⚠️ Arquitetura completamente diferente |
| **Permissões Customizadas** | Campos separados | JSON estruturado | ⚠️ Migração de dados |
| **Desbloqueio Automático** | Inexistente (apenas manual) | Timeout 15 minutos | 🆕 Nova regra |
| **Notificação Senha Expirada** | Inexistente | E-mail 7 dias antes | 🆕 Nova funcionalidade |
| **Validação Força Senha** | Inexistente | Mínimo 8 chars, maiúscula, minúscula, número, especial | 🆕 Nova validação |
| **Permissão Reativar Permanente** | Qualquer admin | Apenas Super Admin (`usuarios:reativar_permanente`) | 🆕 Nova permissão granular |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Migração de Senhas MD5 → BCrypt

**Motivo:** MD5 é inseguro (quebrado desde 2004), facilmente reversível. BCrypt é padrão moderno com custo computacional ajustável (work factor).

**Estratégia:**
1. Criar coluna temporária `Password_Hash_MD5` (backup)
2. Marcar todos os usuários com `Fl_Primeiro_Acesso = 1` (forçar troca)
3. No primeiro login pós-migração: validar senha via MD5 legado, gerar novo hash BCrypt, limpar `Password_Hash_MD5`
4. Após 90 dias (expiração senha): deletar coluna `Password_Hash_MD5`

**Impacto:** **ALTO** — Todos os usuários precisarão trocar senha no próximo login.

---

### Decisão 2: Substituir Session Cookies por JWT

**Motivo:** Session State ASP.NET não escala (dependência de servidor específico). JWT permite stateless authentication e suporte a múltiplos dispositivos.

**Estratégia:**
1. Implementar endpoints `/api/auth/login` (emite JWT) e `/api/auth/refresh` (renova token)
2. Access token válido 8 horas, Refresh token válido 30 dias
3. Armazenar refresh tokens em tabela `Usuario_Sessao` (rastreabilidade)
4. Frontend armazena access token em memory, refresh token em httpOnly cookie

**Impacto:** **ALTO** — Mudança arquitetural completa. Testes paralelos necessários.

---

### Decisão 3: Criar Tabela Usuario_Historico_Acesso

**Motivo:** Legado não possui auditoria de acessos (apenas `Dt_Ultimo_Acesso`). Compliance e segurança exigem logs detalhados.

**Estratégia:**
1. Criar tabela com campos: Id_Usuario, Dt_Acesso, IP, User_Agent, Pais, Cidade, Fl_Sucesso, Motivo_Falha, Fl_Login_Suspeito
2. Registrar TODOS os acessos (sucesso/falha) via middleware
3. Integrar com API de geolocalização (ipapi.co) para detectar país/cidade
4. Enviar e-mail se login suspeito (IP/país/horário anômalo)

**Impacto:** **MÉDIO** — Nova tabela, pode crescer rapidamente (particionamento futuro).

---

### Decisão 4: Limite de 12 Senhas no Histórico

**Motivo:** Legado não limita histórico (pode crescer infinitamente). NIST recomenda 12-24 senhas anteriores.

**Estratégia:**
1. Ao alterar senha: deletar hash mais antigo se já existirem 12 registros
2. Trigger ou lógica aplicação para garantir limite
3. Migração: manter apenas últimas 12 senhas de cada usuário

**Impacto:** **BAIXO** — Simples de implementar.

---

### Decisão 5: Integração Active Directory (Opcional)

**Motivo:** Empresas grandes possuem AD corporativo. Duplicar usuários é retrabalho. Sincronização automática reduz overhead administrativo.

**Estratégia:**
1. Campo `Fl_Usuario_AD = 1` indica usuário gerenciado pelo AD
2. Autenticação via LDAP (PrincipalContext .NET ou Microsoft Graph API)
3. Sincronização diária (job): atualiza nome, email, grupos
4. Desligamento no AD → marca `Fl_Ativo = 0` no IControlIT

**Impacto:** **MÉDIO** — Funcionalidade opcional, não obrigatória para MVP.

---

### Decisão 6: MFA via TOTP (Opcional)

**Motivo:** Aumentar segurança para administradores. TOTP é padrão (RFC 6238), compatível com Google Authenticator, Authy, etc.

**Estratégia:**
1. Campo `Fl_MFA_Habilitado = 1` exige código TOTP após login com senha
2. Secret armazenado em `MFA_Secret` (Base32-encoded)
3. QR Code gerado via formato: `otpauth://totp/IControlIT:{email}?secret={secret}&issuer=IControlIT`
4. Janela de validação: ±1 período (90 segundos total)

**Impacto:** **BAIXO** — Funcionalidade opcional, não afeta usuários que não habilitarem.

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| **Usuários não conseguem logar após migração MD5→BCrypt** | ALTO | BAIXA | Testes paralelos, validação MD5 legado no 1º login, forçar troca senha |
| **Performance degradada (BCrypt mais lento que MD5)** | MÉDIO | MÉDIA | Work factor 12 balanceado, usar async/await, cache em memória para permissões |
| **Histórico de senhas legado corrompido** | MÉDIO | BAIXA | Validar integridade antes de migrar, manter backup por 90 dias |
| **API de Geolocalização indisponível** | BAIXO | MÉDIA | Fallback: registrar apenas IP sem geolocalização, retry com backoff exponencial |
| **Active Directory inacessível** | MÉDIO | BAIXA | Fallback: autenticação local (senha BCrypt), job de sincronização com retry |
| **JWT tokens roubados (XSS)** | ALTO | BAIXA | httpOnly cookies para refresh token, sanitização de outputs, CSP headers |
| **Crescimento rápido da tabela Usuario_Historico_Acesso** | MÉDIO | ALTA | Particionamento por mês, retenção de 12 meses, archive para cold storage |
| **Usuários não entendem MFA** | BAIXO | MÉDIA | Tutorial guiado (tooltips), suporte técnico, SMS como backup |
| **Sessões simultâneas não invalidadas corretamente** | MÉDIO | BAIXA | Testes E2E, validação de revogação de refresh tokens |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|-----------------|---------------|--------|
| `WSAuth.asmx.vb::Login()` | RN-RF012-02 (Política Senha Forte), RN-RF012-05 (JWT Tokens) | **SUBSTITUÍDO** por `POST /api/auth/login` |
| `WSAuth.asmx.vb::Logout()` | RN-RF012-12 (Sessões Múltiplas) | **SUBSTITUÍDO** por `POST /api/auth/logout` |
| `WSUsuario.asmx.vb::Autenticar()` | RN-RF012-03 (Bloqueio 5 Tentativas), RN-RF012-13 (Auditoria) | **SUBSTITUÍDO** por endpoint autenticação + middleware auditoria |
| `WSUsuario.asmx.vb::Listar_Usuarios()` | Funcionalidade CRUD (Seção 4 RF) | **SUBSTITUÍDO** por `GET /api/usuarios` |
| `WSUsuario.asmx.vb::Criar_Usuario()` | RN-RF012-01 (Login Único), RN-RF012-14 (Primeiro Acesso) | **SUBSTITUÍDO** por `POST /api/usuarios` |
| `WSUsuario.asmx.vb::Alterar_Senha()` | RN-RF012-07 (Histórico 12 Senhas), RN-RF012-04 (Expiração 90d) | **SUBSTITUÍDO** por `PUT /api/usuarios/{id}/senha` |
| `WSUsuario.asmx.vb::Desbloquear_Usuario()` | RN-RF012-03 (Bloqueio com timeout 15min) | **SUBSTITUÍDO** por `POST /api/usuarios/{id}/unlock` |
| Tela `Usuario.aspx` | Funcionalidade CRUD (Seção 4 RF) | **SUBSTITUÍDO** por telas Angular (WF-RF012.md) |
| Tabela `Usuario` (campos MD5, sem MFA) | RN-RF012-02 (BCrypt), RN-RF012-08 (MFA), RN-RF012-09 (AD) | **SUBSTITUÍDO** com novos campos (MFA, AD, Permissoes_Customizadas) |
| Stored procedure `sp_Validar_Usuario_Login` | RN-RF012-02 (Validação Senha) | **DESCARTADO** (lógica migrada para Application Layer) |
| Stored procedure `sp_Bloquear_Usuario_Automatico` | RN-RF012-03 (Bloqueio Automático) | **DESCARTADO** (lógica migrada para Application Layer) |

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|--------|------|-----------|-------|
| 1.0 | 2025-12-30 | Criação inicial do RL-RF012 com memória técnica completa do legado. Documentação de 6 RNs implícitas, 7 webservices, 1 tela ASPX, gap analysis e decisões de modernização. | Agência ALC - alc.dev.br |

---

[← Voltar ao Índice](./README.md)

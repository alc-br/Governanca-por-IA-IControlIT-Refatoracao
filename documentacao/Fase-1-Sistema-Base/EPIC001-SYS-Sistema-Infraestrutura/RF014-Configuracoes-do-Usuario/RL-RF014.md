# RL-RF014 — Referência ao Legado: Configurações do Usuário

**Versão:** 2.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-014 - Configurações do Usuário
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar a ausência de funcionalidade dedicada para configurações do usuário no sistema legado, servindo como memória técnica histórica e justificativa para a criação do zero no sistema moderno.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado relacionado a configurações de usuário.

- **Arquitetura:** Monolítica Cliente-Servidor com ASP.NET Web Forms
- **Linguagem / Stack:** VB.NET, ASP.NET Web Forms, JavaScript
- **Banco de Dados:** SQL Server
- **Multi-tenant:** Não (bancos separados por cliente)
- **Auditoria:** Parcial (apenas em alguns cadastros críticos)
- **Configurações:** Web.config + tabelas de parâmetros

**Característica Principal:** O sistema legado **NÃO possuía uma tela dedicada para configurações do usuário**. As funcionalidades relacionadas eram distribuídas e limitadas.

---

## 2. TELAS DO LEGADO

### 2.1 Funcionalidade: Alteração de Senha

- **Tela:** Usuario_Cad.aspx (Cadastro de Usuários)
- **Caminho:** ic1_legado/IControlIT/Admin/Usuario_Cad.aspx
- **Responsabilidade:** Gerenciamento de usuários (criação, edição, exclusão)
- **Acesso:** Apenas administradores

#### Comportamento Identificado

| Funcionalidade | Como funcionava | Limitação |
|----------------|-----------------|-----------|
| Alteração de senha | Apenas admin podia alterar senha de qualquer usuário | Usuário final não podia alterar sua própria senha |
| Validação de senha | Não havia regras de senha forte | Senhas fracas eram aceitas (ex: "123") |
| Dados pessoais | Nome, email, CPF editáveis apenas por admin | Usuário não podia atualizar seus próprios dados |

#### Campos da Tela (Editáveis por Admin)

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| Nome | TextBox | Sim | Editável apenas por admin |
| Email | TextBox | Sim | Editável apenas por admin |
| Senha | TextBox (password) | Sim | Sem validação de força |
| Perfil/Role | DropDownList | Sim | Define permissões |

#### Comportamentos Implícitos

- Senha armazenada com hash MD5 ou SHA1 (hash fraco)
- Sem validação de senha forte (mínimo caracteres, complexidade)
- Sem blacklist de senhas comuns
- Sem auditoria de alteração de senha
- Usuário final dependia de admin para qualquer alteração

---

### 2.2 Funcionalidade: Preferências de Idioma

**Status:** Não existia

- Sistema legado era **monolinguagem** (apenas Português do Brasil)
- Não havia suporte a i18n
- Não havia opção de seleção de idioma

---

### 2.3 Funcionalidade: Tema Visual

**Status:** Não existia

- Interface visual era **fixa** (sem opção de tema claro/escuro)
- Layout não permitia personalização
- Usuário não podia ajustar preferências visuais

---

### 2.4 Funcionalidade: Timezone

**Status:** Não existia

- Sistema usava timezone do servidor (fixo: America/Sao_Paulo)
- Usuários de outros fusos horários viam horários incorretos
- Não havia configuração de timezone por usuário

---

### 2.5 Funcionalidade: Navegação Responsiva

**Status:** Não existia

- Interface não era responsiva (desktop apenas)
- Não funcionava adequadamente em dispositivos móveis
- Menu lateral fixo sem adaptação para telas pequenas

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

Não havia WebServices específicos para configurações do usuário.

**Observação:** O sistema legado utilizava PostBack tradicional do ASP.NET Web Forms, sem arquitetura de APIs REST.

---

## 4. TABELAS LEGADAS

### Tabela: Usuario (SQL Server)

| Campo | Tipo | Observação | Problema Identificado |
|-------|------|------------|----------------------|
| Id | INT | PK | Não usava GUID |
| Nome | NVARCHAR(200) | Obrigatório | Editável apenas por admin |
| Email | NVARCHAR(200) | Obrigatório | Editável apenas por admin |
| Senha | NVARCHAR(500) | Hash fraco | MD5/SHA1 (não BCrypt) |
| CPF | NVARCHAR(14) | Opcional | Sem validação de formato |
| Telefone | NVARCHAR(20) | Opcional | Sem validação de formato |
| DataNascimento | DATE | Opcional | Sem uso efetivo |

**Campos que NÃO existiam no legado:**
- `Idioma` - Sistema era monolinguagem
- `Timezone` - Usava timezone do servidor
- `Tema` - Não havia personalização de tema
- `MustChangePassword` - Não havia controle de expiração de senha
- `DataUltimoAcesso` - Não rastreava acessos
- `DataExpiracaoSenha` - Senhas não expiravam

**Campos de Auditoria:**
- **NÃO existiam** campos de auditoria automática (Created, CreatedBy, LastModified, LastModifiedBy)

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Regras identificadas no código VB.NET que **não estavam documentadas formalmente**:

### RL-RN-001: Senha Mínima (Fraca)

**Descrição:** Sistema aceitava senhas com mínimo de 3 caracteres.

**Evidência:** Validação no Usuario_Cad.aspx.vb:
```vb
' Código legado (extraído em linguagem natural)
' Validação verificava apenas se senha tinha mais de 2 caracteres
' Não validava complexidade (maiúsculas, números, especiais)
```

**Impacto:** Senhas fracas eram aceitas (ex: "123", "abc"), comprometendo segurança.

**Destino no RF Moderno:** SUBSTITUÍDO por RN-RF014-04 (senha forte com 8+ caracteres, complexidade obrigatória)

---

### RL-RN-002: Hash MD5 de Senha

**Descrição:** Sistema armazenava senha com hash MD5 (algoritmo considerado inseguro desde 2004).

**Evidência:** Método de hash no código VB.NET:
```vb
' Código legado utilizava System.Security.Cryptography.MD5
' Hash MD5 é vulnerável a ataques de colisão
```

**Impacto:** Senhas vulneráveis a ataques de força bruta e rainbow tables.

**Destino no RF Moderno:** SUBSTITUÍDO - Sistema moderno usa BCrypt com salt aleatório

---

### RL-RN-003: Sem Self-Service

**Descrição:** Usuário final não podia alterar sua própria senha ou dados.

**Evidência:** Tela Usuario_Cad.aspx exigia perfil de administrador para acesso.

**Impacto:** Dependência de administrador para operações simples, sobrecarga de suporte.

**Destino no RF Moderno:** SUBSTITUÍDO - RF-014 permite self-service completo

---

### RL-RN-004: Sem Auditoria de Senha

**Descrição:** Alterações de senha não eram auditadas (não registrava quem alterou, quando, de onde).

**Evidência:** Tabela Usuario não tinha relacionamento com tabela de auditoria.

**Impacto:** Impossível rastrear alterações de senha para investigação de incidentes de segurança.

**Destino no RF Moderno:** SUBSTITUÍDO - RF-014 audita todas alterações de senha (evento usuario.senha_alterada)

---

### RL-RN-005: Idioma Fixo

**Descrição:** Sistema era monolinguagem (apenas pt-BR).

**Evidência:** Não havia arquivos de recursos de idioma (.resx para outros idiomas).

**Impacto:** Usuários internacionais tinham dificuldade de uso.

**Destino no RF Moderno:** SUBSTITUÍDO - RF-014 suporta pt-BR, en-US, es-ES com Transloco

---

### RL-RN-006: Timezone do Servidor

**Descrição:** Todas as datas/horas eram exibidas no timezone do servidor (America/Sao_Paulo).

**Evidência:** Não havia conversão de timezone no código.

**Impacto:** Usuários em outros países viam horários incorretos.

**Destino no RF Moderno:** SUBSTITUÍDO - RF-014 permite seleção de timezone por usuário

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Funcionalidade | Existe no Legado? | Existe no Moderno? | Observação |
|----------------|-------------------|-------------------|------------|
| **Tela dedicada para configurações** | ❌ Não | ✅ Sim | Funcionalidade criada do zero |
| **Alteração de senha por usuário** | ❌ Não | ✅ Sim | Antes apenas admin podia |
| **Validação de senha forte** | ❌ Não | ✅ Sim | Legado aceitava senhas fracas |
| **Blacklist de senhas comuns** | ❌ Não | ✅ Sim | Funcionalidade nova |
| **Senha não pode conter dados pessoais** | ❌ Não | ✅ Sim | Validação nova |
| **Hash seguro de senha (BCrypt)** | ❌ Não (MD5) | ✅ Sim | Migração de algoritmo |
| **Seleção de idioma** | ❌ Não | ✅ Sim | Sistema era monolinguagem |
| **Seleção de tema (claro/escuro)** | ❌ Não | ✅ Sim | Funcionalidade nova |
| **Seleção de timezone** | ❌ Não | ✅ Sim | Usava timezone do servidor |
| **Auditoria de alteração de senha** | ❌ Não | ✅ Sim | Funcionalidade nova |
| **Edição de telefone pelo usuário** | ❌ Não | ✅ Sim | Antes apenas admin podia |
| **Interface responsiva** | ❌ Não | ✅ Sim | Desktop apenas |

---

## 7. DECISÕES DE MODERNIZAÇÃO

### Decisão 1: Criar Funcionalidade do Zero

**Decisão:** Implementar tela de configurações do usuário do zero, sem tentar migrar código legado.

**Motivo:**
- Funcionalidade não existia de forma integrada no legado
- Arquitetura legada (Web Forms + VB.NET) incompatível com Angular 19
- Segurança do legado era inadequada (hash MD5, sem validações)

**Impacto:** Alto - Requer implementação completa backend + frontend

---

### Decisão 2: Migrar Hashes de Senha Existentes

**Decisão:** Não migrar hashes MD5 antigos diretamente. Forçar reset de senha na primeira migração.

**Motivo:**
- Hash MD5 é inseguro
- BCrypt requer re-hash de todas as senhas
- Não é possível converter MD5 → BCrypt sem senha em texto plano

**Impacto:** Médio - Usuários precisarão redefinir senha na primeira migração

**Mitigação:** Sistema pode enviar email automático com link de reset de senha

---

### Decisão 3: Implementar i18n desde o Início

**Decisão:** Sistema moderno nasce multilíngue (pt-BR, en-US, es-ES).

**Motivo:**
- Evitar refatoração futura
- Facilita expansão para novos mercados
- Melhor experiência para usuários internacionais

**Impacto:** Baixo - Transloco facilita implementação

---

### Decisão 4: Auditoria Obrigatória de Senha

**Decisão:** Todas as alterações de senha são auditadas (quem, quando, de onde).

**Motivo:**
- Compliance (LGPD, ISO 27001)
- Investigação de incidentes de segurança
- Rastreabilidade completa

**Impacto:** Baixo - Auditoria já implementada no sistema

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Probabilidade | Mitigação |
|------|---------|---------------|-----------|
| **Usuários resistentes a senhas fortes** | Médio | Alta | Mensagens educativas sobre segurança |
| **Perda de senhas antigas (MD5)** | Alto | Certo | Email automático de reset de senha |
| **Confusão com múltiplos idiomas** | Baixo | Baixa | Idioma padrão pt-BR, seleção clara |
| **Timezone incorreto causa erros** | Médio | Média | Validação de timezone na seleção |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Status |
|----------------|---------------|--------|
| Usuario_Cad.aspx (admin) | RN-RF014-03 a RN-RF014-08 | Substituído por self-service |
| Hash MD5 de senha | RN-RF014-04 | Substituído por BCrypt |
| Ausência de i18n | RN-RF014-10 | Substituído por Transloco (pt-BR, en-US, es-ES) |
| Ausência de tema | RN-RF014-11 | Substituído por seleção de tema (light/dark/auto) |
| Timezone fixo | RN-RF014-12 | Substituído por seleção de timezone IANA |
| Sem auditoria de senha | Evento usuario.senha_alterada | Substituído por auditoria automática |

---

## 10. LIÇÕES APRENDIDAS

1. **Segurança deve ser prioritária desde o início** - Legado aceitava senhas fracas, causando vulnerabilidades
2. **Self-service reduz sobrecarga de suporte** - Usuários devem gerenciar suas próprias configurações
3. **i18n deve ser nativo, não retroativo** - Adicionar i18n depois é muito mais trabalhoso
4. **Auditoria de operações críticas é obrigatória** - Rastreabilidade é essencial para compliance
5. **Responsividade não é opcional** - Interface deve funcionar em todos os dispositivos

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 2.0 | 2025-12-30 | Migração para formato v2.0 com destinos obrigatórios, análise completa de gap legado vs moderno | Agência ALC - alc.dev.br |
| 1.0 | 2025-12-27 | Extração inicial de referências ao legado do RF-014 v1.1 | Equipe IControlIT |

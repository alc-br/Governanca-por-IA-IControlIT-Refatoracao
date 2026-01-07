# UC-RF014 — Casos de Uso Canônicos

**RF:** RF014 — Configurações do Usuário
**Fase:** Fase 1 - Sistema Base
**Epic:** EPIC001-SYS
**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF014**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF014.yaml)
- Massas de Teste (MT-RF014.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Visualizar Configurações Pessoais | Usuário Autenticado |
| UC01 | Atualizar Dados Pessoais | Usuário Autenticado |
| UC02 | Alterar Senha | Usuário Autenticado |
| UC03 | Atualizar Preferências de Interface | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Usuário **SOMENTE** pode visualizar e editar suas **próprias** configurações
- Todas as ações exigem **autenticação JWT válida**
- Dados críticos (nome, email, CPF, empresa) são **somente leitura**
- Alteração de senha exige **auditoria obrigatória**
- Preferências devem **persistir entre sessões**
- Mensagens de erro devem ser claras e não vazar informações sensíveis

---

## UC00 — Visualizar Configurações Pessoais

### Objetivo
Permitir que o usuário autenticado visualize todas as suas configurações atuais (dados pessoais, preferências, informações de auditoria).

### Pré-condições
- Usuário autenticado via JWT
- Token JWT válido e não expirado

### Pós-condições
- Dados do usuário exibidos corretamente
- Campos somente leitura claramente identificados

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa menu "Configurações" ou "Meu Perfil"
- **FP-UC00-002:** Sistema valida token JWT
- **FP-UC00-003:** Sistema carrega dados do usuário autenticado (baseado no UserId do token)
- **FP-UC00-004:** Sistema exibe dados pessoais (nome, email, CPF, telefone, data nascimento)
- **FP-UC00-005:** Sistema exibe empresa vinculada (somente leitura)
- **FP-UC00-006:** Sistema exibe preferências atuais (idioma, tema, timezone)
- **FP-UC00-007:** Sistema exibe informações de auditoria (created_at, updated_at)

### Fluxos Alternativos
- **FA-UC00-001:** Usuário navega entre abas (Dados Pessoais, Segurança, Preferências)
- **FA-UC00-002:** Usuário visualiza em tela pequena (< 1024px) → menu lateral vira drawer overlay

### Fluxos de Exceção
- **FE-UC00-001:** Token JWT inválido ou expirado → redirecionar para login
- **FE-UC00-002:** Usuário não encontrado no banco → retornar erro 404
- **FE-UC00-003:** Erro ao carregar dados → exibir mensagem genérica "Erro ao carregar configurações"

### Regras de Negócio
- **RN-RF014-01:** Nome, email, CPF e empresa são exibidos como somente leitura
- **RN-RF014-15:** Tela de configurações só é acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode visualizar suas próprias configurações

### Critérios de Aceite
- **CA-UC00-001:** Sistema DEVE exibir TODOS os dados do usuário autenticado
- **CA-UC00-002:** Campos nome, email, CPF e empresa DEVEM estar desabilitados para edição
- **CA-UC00-003:** Preferências (idioma, tema, timezone) DEVEM refletir valores salvos no banco
- **CA-UC00-004:** Informações de auditoria (created_at, updated_at) DEVEM ser exibidas
- **CA-UC00-005:** Sistema DEVE validar que UserId do token corresponde ao usuário logado

---

## UC01 — Atualizar Dados Pessoais

### Objetivo
Permitir que o usuário autenticado atualize **apenas telefone e data de nascimento** (dados pessoais editáveis).

### Pré-condições
- Usuário autenticado via JWT
- Permissão `self.update_profile` (ou autenticação suficiente)

### Pós-condições
- Telefone e/ou data de nascimento atualizados no banco
- Evento `usuario.dados_pessoais_atualizados` emitido
- Campos de auditoria atualizados (updated_at, updated_by)

### Fluxo Principal
- **FP-UC01-001:** Usuário acessa seção "Dados Pessoais"
- **FP-UC01-002:** Sistema exibe formulário com telefone e data nascimento editáveis
- **FP-UC01-003:** Usuário altera telefone e/ou data de nascimento
- **FP-UC01-004:** Usuário clica em "Salvar"
- **FP-UC01-005:** Sistema valida formato do telefone (se informado)
- **FP-UC01-006:** Sistema valida data de nascimento (não pode ser futura)
- **FP-UC01-007:** Sistema persiste alterações no banco
- **FP-UC01-008:** Sistema atualiza `updated_at` e `updated_by` automaticamente
- **FP-UC01-009:** Sistema emite evento `usuario.dados_pessoais_atualizados`
- **FP-UC01-010:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC01-001:** Usuário cancela edição → dados não são salvos

### Fluxos de Exceção
- **FE-UC01-001:** Telefone em formato inválido → exibir erro "Telefone deve seguir formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"
- **FE-UC01-002:** Data de nascimento futura → exibir erro "Data de nascimento não pode ser futura"
- **FE-UC01-003:** Erro ao salvar no banco → exibir mensagem "Erro ao atualizar dados pessoais"

### Regras de Negócio
- **RN-RF014-01:** Nome, email, CPF e empresa NÃO podem ser alterados
- **RN-RF014-02:** Telefone deve seguir formato brasileiro (XX) XXXXX-XXXX ou (XX) XXXX-XXXX

### Critérios de Aceite
- **CA-UC01-001:** Sistema DEVE permitir edição APENAS de telefone e data de nascimento
- **CA-UC01-002:** Telefone DEVE ser validado conforme regex brasileiro
- **CA-UC01-003:** Data de nascimento DEVE ser validada (não pode ser futura)
- **CA-UC01-004:** Sistema DEVE preencher `updated_at` e `updated_by` automaticamente
- **CA-UC01-005:** Evento `usuario.dados_pessoais_atualizados` DEVE conter UserId e campos alterados
- **CA-UC01-006:** Tentativa de alterar nome, email, CPF ou empresa DEVE ser rejeitada

---

## UC02 — Alterar Senha

### Objetivo
Permitir que o usuário autenticado altere sua senha de acesso, garantindo validações de segurança rigorosas.

### Pré-condições
- Usuário autenticado via JWT
- Permissão `self.change_password` (ou autenticação suficiente)

### Pós-condições
- Senha atualizada no banco (hash seguro)
- Auditoria obrigatória registrada
- Evento `usuario.senha_alterada` emitido
- Campos de auditoria atualizados (updated_at, updated_by)

### Fluxo Principal
- **FP-UC02-001:** Usuário acessa seção "Segurança" ou "Alterar Senha"
- **FP-UC02-002:** Sistema exibe formulário com 3 campos: senha atual, nova senha, confirmar nova senha
- **FP-UC02-003:** Usuário preenche os 3 campos
- **FP-UC02-004:** Usuário clica em "Alterar Senha"
- **FP-UC02-005:** Sistema valida que senha atual está correta
- **FP-UC02-006:** Sistema valida que nova senha tem mínimo 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial
- **FP-UC02-007:** Sistema valida que nova senha é diferente da senha atual
- **FP-UC02-008:** Sistema valida que nova senha NÃO está na blacklist (123456, password, senha123, admin123, qwerty, etc)
- **FP-UC02-009:** Sistema valida que nova senha NÃO contém nome do usuário ou parte do email
- **FP-UC02-010:** Sistema valida que confirmação de senha é idêntica à nova senha
- **FP-UC02-011:** Sistema gera hash seguro da nova senha (BCrypt/PBKDF2)
- **FP-UC02-012:** Sistema persiste novo hash no banco
- **FP-UC02-013:** Sistema atualiza `updated_at` e `updated_by` automaticamente
- **FP-UC02-014:** Sistema registra auditoria obrigatória (quem, quando, IP)
- **FP-UC02-015:** Sistema emite evento `usuario.senha_alterada`
- **FP-UC02-016:** Sistema exibe mensagem de sucesso "Senha alterada com sucesso"

### Fluxos Alternativos
- **FA-UC02-001:** Usuário cancela alteração → senha não é alterada

### Fluxos de Exceção
- **FE-UC02-001:** Senha atual incorreta → exibir erro "Senha atual incorreta"
- **FE-UC02-002:** Nova senha não atende requisitos de complexidade → exibir erro detalhado
- **FE-UC02-003:** Nova senha igual à atual → exibir erro "Nova senha deve ser diferente da senha atual"
- **FE-UC02-004:** Nova senha está na blacklist → exibir erro "Senha muito comum, escolha outra"
- **FE-UC02-005:** Nova senha contém nome ou email → exibir erro "Senha não pode conter seu nome ou email"
- **FE-UC02-006:** Confirmação de senha não coincide → exibir erro "Senhas não coincidem"
- **FE-UC02-007:** Rate limiting atingido → exibir erro "Muitas tentativas, aguarde X minutos"
- **FE-UC02-008:** Erro ao salvar no banco → exibir mensagem genérica "Erro ao alterar senha"

### Regras de Negócio
- **RN-RF014-03:** Para alterar senha, usuário deve informar senha atual corretamente
- **RN-RF014-04:** Nova senha deve ter mínimo 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial
- **RN-RF014-05:** Nova senha não pode ser igual à senha atual
- **RN-RF014-06:** Senhas comuns são bloqueadas (123456, password, senha123, admin123, qwerty, etc)
- **RN-RF014-07:** Senha não pode conter nome do usuário ou parte do email
- **RN-RF014-08:** Campo de confirmação deve ser idêntico ao campo de nova senha

### Critérios de Aceite
- **CA-UC02-001:** Sistema DEVE validar senha atual antes de permitir alteração
- **CA-UC02-002:** Sistema DEVE aplicar TODAS as validações de segurança (RN-RF014-04 a RN-RF014-08)
- **CA-UC02-003:** Sistema DEVE usar BCrypt ou PBKDF2 para gerar hash de senha
- **CA-UC02-004:** Auditoria DEVE registrar UserId, IP e timestamp da alteração
- **CA-UC02-005:** Evento `usuario.senha_alterada` DEVE conter UserId, IP e Timestamp
- **CA-UC02-006:** Sistema DEVE aplicar rate limiting (ex: máximo 5 tentativas em 15 minutos)
- **CA-UC02-007:** Mensagens de erro DEVEM ser específicas mas não vazar informações sensíveis

---

## UC03 — Atualizar Preferências de Interface

### Objetivo
Permitir que o usuário autenticado atualize suas preferências de interface (idioma, tema visual, timezone).

### Pré-condições
- Usuário autenticado via JWT
- Permissão `self.update_preferences` (ou autenticação suficiente)

### Pós-condições
- Idioma, tema e/ou timezone atualizados no banco
- Preferências aplicadas **imediatamente** na interface
- Evento `usuario.preferencias_atualizadas` emitido
- Campos de auditoria atualizados (updated_at, updated_by)

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa seção "Preferências" ou "Interface"
- **FP-UC03-002:** Sistema exibe formulário com dropdowns para idioma, tema e timezone
- **FP-UC03-003:** Sistema carrega opções disponíveis:
  - Idioma: pt-BR (padrão), en-US, es-ES
  - Tema: light, dark, auto
  - Timezone: lista de timezones IANA comuns (América, Europa, Ásia)
- **FP-UC03-004:** Usuário altera idioma, tema e/ou timezone
- **FP-UC03-005:** Usuário clica em "Salvar"
- **FP-UC03-006:** Sistema valida que valores selecionados são válidos
- **FP-UC03-007:** Sistema persiste alterações no banco
- **FP-UC03-008:** Sistema atualiza `updated_at` e `updated_by` automaticamente
- **FP-UC03-009:** Sistema emite evento `usuario.preferencias_atualizadas` (com preferências antigas e novas)
- **FP-UC03-010:** Sistema aplica novo idioma imediatamente (recarrega traduções via Transloco)
- **FP-UC03-011:** Sistema aplica novo tema imediatamente (troca classe CSS)
- **FP-UC03-012:** Sistema aplica novo timezone (ajusta exibição de datas/horas)
- **FP-UC03-013:** Sistema exibe mensagem de sucesso

### Fluxos Alternativos
- **FA-UC03-001:** Usuário altera idioma de qualquer tela → sistema reflete alteração na tela de configurações
- **FA-UC03-002:** Usuário cancela edição → preferências não são salvas

### Fluxos de Exceção
- **FE-UC03-001:** Idioma selecionado inválido → exibir erro "Idioma inválido"
- **FE-UC03-002:** Tema selecionado inválido → exibir erro "Tema inválido"
- **FE-UC03-003:** Timezone selecionado inválido → exibir erro "Timezone inválido"
- **FE-UC03-004:** Erro ao salvar no banco → exibir mensagem "Erro ao atualizar preferências"

### Regras de Negócio
- **RN-RF014-09:** Idioma selecionado é salvo no perfil do usuário e aplicado imediatamente
- **RN-RF014-10:** Sistema suporta 3 idiomas: pt-BR (padrão), en-US, es-ES
- **RN-RF014-11:** Usuário pode escolher entre temas: light, dark, auto
- **RN-RF014-12:** Sistema oferece lista de timezones IANA comuns (América, Europa, Ásia)
- **RN-RF014-14:** Alteração de idioma em qualquer parte do sistema reflete na tela de configurações

### Critérios de Aceite
- **CA-UC03-001:** Sistema DEVE permitir seleção de idioma (pt-BR, en-US, es-ES)
- **CA-UC03-002:** Sistema DEVE permitir seleção de tema (light, dark, auto)
- **CA-UC03-003:** Sistema DEVE permitir seleção de timezone (lista IANA)
- **CA-UC03-004:** Sistema DEVE aplicar idioma imediatamente após salvar (sem reload)
- **CA-UC03-005:** Sistema DEVE aplicar tema imediatamente após salvar
- **CA-UC03-006:** Preferências DEVEM persistir entre sessões (salvas no banco)
- **CA-UC03-007:** Evento `usuario.preferencias_atualizadas` DEVE conter preferências antigas e novas
- **CA-UC03-008:** Sistema DEVE validar que valores selecionados estão na lista de opções válidas
- **CA-UC03-009:** Alteração de idioma via seletor de idioma DEVE refletir na tela de configurações

---

## 4. MATRIZ DE RASTREABILIDADE

### UC00 — Visualizar Configurações Pessoais

| Regra de Negócio | Descrição |
|------------------|-----------|
| RN-RF014-01 | Nome, email, CPF e empresa exibidos como somente leitura |
| RN-RF014-15 | Tela de configurações só acessível por usuários autenticados |
| RN-RF014-16 | Usuário só visualiza suas próprias configurações |

| Item do Catálogo | Descrição |
|------------------|-----------|
| RF014-CRUD-01 | Visualizar dados pessoais |
| RF014-SEC-01 | Isolamento de dados |
| RF014-SEC-02 | Autenticação JWT obrigatória |

### UC01 — Atualizar Dados Pessoais

| Regra de Negócio | Descrição |
|------------------|-----------|
| RN-RF014-01 | Nome, email, CPF e empresa são somente leitura |
| RN-RF014-02 | Telefone deve seguir formato brasileiro |

| Item do Catálogo | Descrição |
|------------------|-----------|
| RF014-CRUD-02 | Atualizar telefone e data nascimento |
| RF014-VAL-01 | Validar formato de telefone brasileiro |
| RF014-SEC-01 | Isolamento de dados |

### UC02 — Alterar Senha

| Regra de Negócio | Descrição |
|------------------|-----------|
| RN-RF014-03 | Informar senha atual corretamente |
| RN-RF014-04 | Senha forte (8+ caracteres, maiúscula, minúscula, número, especial) |
| RN-RF014-05 | Nova senha diferente da atual |
| RN-RF014-06 | Senhas comuns bloqueadas |
| RN-RF014-07 | Senha não pode conter nome/email |
| RN-RF014-08 | Confirmação deve ser idêntica |

| Item do Catálogo | Descrição |
|------------------|-----------|
| RF014-CRUD-03 | Alterar senha |
| RF014-VAL-02 | Validar requisitos de senha forte |
| RF014-VAL-03 | Validar senha atual |
| RF014-VAL-04 | Validar nova senha diferente da atual |
| RF014-VAL-05 | Validar senha não está na blacklist |
| RF014-VAL-06 | Validar senha não contém dados pessoais |
| RF014-VAL-07 | Validar confirmação de senha |
| RF014-SEC-03 | Auditoria de alteração de senha |
| RF014-SEC-04 | Hash seguro de senha |
| RF014-SEC-05 | Rate limiting |

### UC03 — Atualizar Preferências de Interface

| Regra de Negócio | Descrição |
|------------------|-----------|
| RN-RF014-09 | Idioma salvo e aplicado imediatamente |
| RN-RF014-10 | Sistema suporta pt-BR, en-US, es-ES |
| RN-RF014-11 | Temas: light, dark, auto |
| RN-RF014-12 | Lista de timezones IANA |
| RN-RF014-14 | Alteração de idioma reflete na tela de configurações |

| Item do Catálogo | Descrição |
|------------------|-----------|
| RF014-CRUD-04 | Atualizar preferências (idioma, tema, timezone) |

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 2.0 | 2026-01-04 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - 4 casos de uso específicos para configurações de usuário |

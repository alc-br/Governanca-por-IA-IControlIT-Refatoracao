# UC-RF014 — Casos de Uso Canônicos

**RF:** RF014 — Configurações do Usuário
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC001-SYS - Sistema Infraestrutura
**Fase:** Fase 1 - Sistema Base

---

## 1. OBJETIVO DO DOCUMENTO

Este documento descreve **todos os Casos de Uso (UC)** derivados do **RF014 - Configurações do Usuário**, cobrindo integralmente o comportamento funcional esperado.

Os UCs aqui definidos servem como **contrato comportamental**, sendo a **fonte primária** para geração de:
- Casos de Teste (TC-RF014.yaml)
- Massas de Teste (MT-RF014.yaml)
- Evidências de auditoria e validação funcional
- Execução por agentes de IA (tester, QA, E2E)

---

## 2. SUMÁRIO DE CASOS DE USO

| ID | Nome | Ator Principal |
|----|------|----------------|
| UC00 | Visualizar Dados da Conta | Usuário Autenticado |
| UC01 | Editar Dados Pessoais | Usuário Autenticado |
| UC02 | Alterar Senha | Usuário Autenticado |
| UC03 | Configurar Idioma | Usuário Autenticado |
| UC04 | Configurar Tema Visual | Usuário Autenticado |
| UC05 | Configurar Timezone | Usuário Autenticado |

---

## 3. PADRÕES GERAIS APLICÁVEIS A TODOS OS UCs

- Todos os acessos respeitam **isolamento por tenant** (usuário só acessa seus próprios dados)
- Todas as ações exigem **autenticação JWT válida**
- Usuário só pode modificar suas próprias configurações (RN-RF014-16)
- Erros não devem vazar informações sensíveis
- Auditoria deve registrar **quem**, **quando** e **qual ação** (especialmente alteração de senha)
- Mensagens devem ser claras, previsíveis e rastreáveis
- Preferências devem persistir entre sessões
- Alterações de idioma devem ser aplicadas imediatamente

---

## UC00 — Visualizar Dados da Conta

### Objetivo
Permitir que o usuário autenticado visualize seus dados pessoais (nome, email, CPF, empresa) de forma somente leitura.

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Dados pessoais exibidos corretamente
- Nenhuma alteração nos dados

### Fluxo Principal
- **FP-UC00-001:** Usuário acessa /user-settings
- **FP-UC00-002:** Sistema valida autenticação JWT
- **FP-UC00-003:** Sistema carrega dados do usuário atual via Query GetCurrentUser
- **FP-UC00-004:** Sistema exibe campos somente leitura: Nome, Email, CPF, Empresa
- **FP-UC00-005:** Sistema indica visualmente que campos são não-editáveis (ícone de cadeado)
- **FP-UC00-006:** Sistema exibe dados editáveis: Telefone, Data de Nascimento

### Fluxos Alternativos
- **FA-UC00-001:** Tela responsiva em mobile (< 1024px) - Menu lateral vira drawer overlay
- **FA-UC00-002:** Usuário acessa via navegação por teclado (acessibilidade)

### Fluxos de Exceção
- **FE-UC00-001:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC00-002:** Usuário inativo ou bloqueado → Sistema retorna HTTP 403 → Mensagem "Usuário sem acesso"
- **FE-UC00-003:** Erro ao carregar dados → Sistema exibe mensagem "Erro ao carregar dados. Tente novamente"

### Regras de Negócio
- **RN-RF014-01:** Nome, Email, CPF e Empresa são somente leitura
- **RN-RF014-13:** Em telas menores (< 1024px), menu lateral vira drawer overlay
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode visualizar suas próprias configurações

### Critérios de Aceite
- **CA-UC00-001:** Campos somente leitura DEVEM ser visualmente distintos (ícone de cadeado)
- **CA-UC00-002:** Tentativa de editar campos somente leitura via API DEVE retornar HTTP 400
- **CA-UC00-003:** Dados exibidos DEVEM corresponder ao usuário autenticado
- **CA-UC00-004:** Em mobile, menu DEVE ser exibido como drawer overlay
- **CA-UC00-005:** Token inválido DEVE redirecionar para login

---

## UC01 — Editar Dados Pessoais

### Objetivo
Permitir que o usuário autenticado edite seus dados pessoais editáveis (telefone e data de nascimento).

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Dados editáveis atualizados no banco de dados
- Evento `usuario.dados_pessoais_atualizados` disparado
- Auditoria registrada com campos alterados

### Fluxo Principal
- **FP-UC01-001:** Usuário acessa aba "Conta" em /user-settings
- **FP-UC01-002:** Sistema valida autenticação JWT
- **FP-UC01-003:** Sistema carrega dados atuais do usuário
- **FP-UC01-004:** Usuário edita campo Telefone
- **FP-UC01-005:** Sistema valida formato em tempo real (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
- **FP-UC01-006:** Usuário edita campo Data de Nascimento via datepicker
- **FP-UC01-007:** Usuário clica em "Salvar"
- **FP-UC01-008:** Sistema valida formulário completo
- **FP-UC01-009:** Sistema envia dados ao backend via PUT /api/usuarios/{id}/profile
- **FP-UC01-010:** Backend valida dados
- **FP-UC01-011:** Backend atualiza registro no banco
- **FP-UC01-012:** Backend registra auditoria (campos alterados, valores antigos/novos, IP, timestamp)
- **FP-UC01-013:** Sistema exibe mensagem de sucesso
- **FP-UC01-014:** Interface atualiza com novos dados

### Fluxos Alternativos
- **FA-UC01-001:** Formulário sem alterações - Sistema exibe aviso "Nenhuma alteração detectada"
- **FA-UC01-002:** Usuário cancela edição - Dados não são salvos

### Fluxos de Exceção
- **FE-UC01-001:** Telefone com formato inválido → Sistema exibe erro "Formato inválido. Use (XX) XXXXX-XXXX"
- **FE-UC01-002:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC01-003:** Erro de conexão → Sistema exibe mensagem "Erro de conexão. Tente novamente"
- **FE-UC01-004:** Data de nascimento futura → Sistema exibe erro "Data de nascimento inválida"

### Regras de Negócio
- **RN-RF014-01:** Nome, Email, CPF e Empresa não podem ser editados (somente leitura)
- **RN-RF014-02:** Telefone deve seguir formato brasileiro (XX) XXXXX-XXXX ou (XX) XXXX-XXXX
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode editar suas próprias configurações

### Critérios de Aceite
- **CA-UC01-001:** Validação de telefone DEVE ocorrer em tempo real no frontend
- **CA-UC01-002:** Validação de telefone DEVE ser reforçada no backend
- **CA-UC01-003:** Campos obrigatórios DEVEM ser validados antes de persistir
- **CA-UC01-004:** Auditoria DEVE registrar campos alterados, valores antigos e novos
- **CA-UC01-005:** Sistema DEVE retornar erro claro se validação falhar
- **CA-UC01-006:** Tentativa de editar campos somente leitura DEVE retornar HTTP 400

---

## UC02 — Alterar Senha

### Objetivo
Permitir que o usuário autenticado altere sua própria senha, fornecendo a senha atual e uma nova senha que atenda aos requisitos de segurança.

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário conhece sua senha atual
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Senha do usuário atualizada no banco de dados (hash BCrypt/PBKDF2)
- Flag MustChangePassword definida como false
- Evento `usuario.senha_alterada` disparado
- Auditoria registrada com UserId, IP, Timestamp, UserAgent
- Mensagem de confirmação exibida

### Fluxo Principal
- **FP-UC02-001:** Usuário acessa aba "Segurança" em /user-settings
- **FP-UC02-002:** Sistema valida autenticação JWT
- **FP-UC02-003:** Sistema exibe formulário de alteração de senha
- **FP-UC02-004:** Usuário digita senha atual (campo com toggle de visibilidade)
- **FP-UC02-005:** Usuário digita nova senha
- **FP-UC02-006:** Sistema valida requisitos em tempo real: mínimo 8 caracteres, maiúscula, minúscula, número, especial
- **FP-UC02-007:** Usuário digita confirmação de senha
- **FP-UC02-008:** Sistema valida se senhas coincidem em tempo real
- **FP-UC02-009:** Usuário clica em "Alterar Senha"
- **FP-UC02-010:** Sistema valida formulário completo
- **FP-UC02-011:** Sistema envia dados ao backend via POST /api/usuarios/change-password
- **FP-UC02-012:** Backend busca usuário no banco
- **FP-UC02-013:** Backend valida hash da senha atual
- **FP-UC02-014:** Backend valida nova senha (requisitos, blacklist, dados pessoais)
- **FP-UC02-015:** Backend valida que nova senha é diferente da atual
- **FP-UC02-016:** Backend gera hash da nova senha
- **FP-UC02-017:** Backend salva nova senha
- **FP-UC02-018:** Backend registra auditoria (UserId, IP, Timestamp, UserAgent)
- **FP-UC02-019:** Sistema retorna HTTP 200 OK
- **FP-UC02-020:** Frontend exibe mensagem de sucesso
- **FP-UC02-021:** Formulário é limpo

### Fluxos Alternativos
- **FA-UC02-001:** Usuário clica em ícone de olho - Sistema alterna tipo do input entre password/text
- **FA-UC02-002:** Usuário cancela operação - Dados não são salvos

### Fluxos de Exceção
- **FE-UC02-001:** Senha atual incorreta → Backend retorna HTTP 400 "Senha atual incorreta" → Frontend exibe erro no campo
- **FE-UC02-002:** Nova senha igual à atual → Backend retorna HTTP 400 "Nova senha deve ser diferente da senha atual"
- **FE-UC02-003:** Senha muito fraca → Frontend valida em tempo real → Exibe erros: "Mínimo 8 caracteres", "Deve conter maiúscula, minúscula, número e especial"
- **FE-UC02-004:** Senha na blacklist → Backend retorna HTTP 400 "Esta senha é muito comum. Escolha uma senha mais segura"
- **FE-UC02-005:** Senha contém dados pessoais → Backend retorna HTTP 400 "Senha não pode conter seu nome ou email"
- **FE-UC02-006:** Senhas não coincidem → Frontend valida em tempo real → Exibe erro "As senhas não coincidem" → Botão desabilitado
- **FE-UC02-007:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC02-008:** Erro inesperado → Sistema exibe mensagem "Erro ao alterar senha. Tente novamente"

### Regras de Negócio
- **RN-RF014-03:** Para alterar senha, usuário deve informar senha atual corretamente
- **RN-RF014-04:** Nova senha deve ter mínimo 8 caracteres, maiúscula, minúscula, número e especial
- **RN-RF014-05:** Nova senha não pode ser igual à senha atual
- **RN-RF014-06:** Senhas comuns são bloqueadas (blacklist: 123456, password, senha123, admin123, qwerty, etc)
- **RN-RF014-07:** Senha não pode conter nome do usuário ou parte do email
- **RN-RF014-08:** Campo de confirmação deve ser idêntico ao campo de nova senha
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode alterar sua própria senha

### Critérios de Aceite
- **CA-UC02-001:** Senha atual DEVE ser validada comparando hash no backend
- **CA-UC02-002:** Nova senha DEVE atender todos os requisitos (8+ chars, maiúscula, minúscula, número, especial)
- **CA-UC02-003:** Nova senha DEVE ser diferente da senha atual
- **CA-UC02-004:** Senhas na blacklist DEVEM ser rejeitadas
- **CA-UC02-005:** Senhas contendo nome ou email do usuário DEVEM ser rejeitadas
- **CA-UC02-006:** Confirmação de senha DEVE ser idêntica à nova senha
- **CA-UC02-007:** Hash DEVE ser gerado usando BCrypt ou PBKDF2
- **CA-UC02-008:** Auditoria DEVE registrar UserId, IP, Timestamp, UserAgent
- **CA-UC02-009:** Senha NUNCA deve trafegar ou ser armazenada em texto plano
- **CA-UC02-010:** Rate limiting DEVE limitar tentativas de alteração (5 tentativas/hora)

---

## UC03 — Configurar Idioma

### Objetivo
Permitir que o usuário autenticado selecione o idioma da interface (pt-BR, en-US, es-ES).

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Idioma selecionado salvo no localStorage
- Idioma aplicado imediatamente na interface
- Evento `usuario.preferencias_atualizadas` disparado
- Interface traduzida via Transloco

### Fluxo Principal
- **FP-UC03-001:** Usuário acessa aba "Preferências" em /user-settings
- **FP-UC03-002:** Sistema valida autenticação JWT
- **FP-UC03-003:** Sistema exibe formulário de preferências
- **FP-UC03-004:** Sistema carrega idioma atual do localStorage
- **FP-UC03-005:** Usuário seleciona idioma no dropdown (pt-BR, en-US, es-ES)
- **FP-UC03-006:** Usuário clica em "Salvar"
- **FP-UC03-007:** Sistema aplica idioma via TranslocoService.setActiveLang()
- **FP-UC03-008:** Sistema salva preferência no localStorage ('preferredLang')
- **FP-UC03-009:** Sistema atualiza toda interface imediatamente
- **FP-UC03-010:** Sistema exibe mensagem de confirmação no novo idioma
- **FP-UC03-011:** Dropdown de idioma no header sincroniza automaticamente

### Fluxos Alternativos
- **FA-UC03-001:** Idioma alterado pelo header - Sistema detecta via langChanges$ - Dropdown atualiza automaticamente
- **FA-UC03-002:** Usuário cancela operação - Idioma não é alterado

### Fluxos de Exceção
- **FE-UC03-001:** Idioma não suportado informado → Sistema faz fallback para pt-BR (padrão)
- **FE-UC03-002:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC03-003:** Erro ao salvar no localStorage → Sistema exibe aviso mas idioma é aplicado na sessão atual

### Regras de Negócio
- **RN-RF014-09:** Idioma selecionado é salvo no perfil do usuário e aplicado imediatamente
- **RN-RF014-10:** Sistema suporta 3 idiomas: pt-BR (padrão), en-US, es-ES
- **RN-RF014-14:** Alteração de idioma em qualquer parte do sistema reflete na tela de configurações
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode alterar suas próprias configurações

### Critérios de Aceite
- **CA-UC03-001:** Idioma DEVE ser aplicado imediatamente sem necessidade de logout/login
- **CA-UC03-002:** Idioma DEVE persistir no localStorage entre sessões
- **CA-UC03-003:** Sistema DEVE suportar apenas pt-BR, en-US, es-ES
- **CA-UC03-004:** Idioma não suportado DEVE fazer fallback para pt-BR
- **CA-UC03-005:** Alteração de idioma DEVE sincronizar entre header e tela de configurações
- **CA-UC03-006:** Toda interface DEVE ser traduzida via Transloco (chaves i18n)

---

## UC04 — Configurar Tema Visual

### Objetivo
Permitir que o usuário autenticado escolha o tema visual da interface (light, dark, auto).

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Tema selecionado salvo no localStorage
- Tema aplicado imediatamente na interface
- Evento `usuario.preferencias_atualizadas` disparado

### Fluxo Principal
- **FP-UC04-001:** Usuário acessa aba "Preferências" em /user-settings
- **FP-UC04-002:** Sistema valida autenticação JWT
- **FP-UC04-003:** Sistema exibe formulário de preferências
- **FP-UC04-004:** Sistema carrega tema atual do localStorage
- **FP-UC04-005:** Usuário seleciona tema no dropdown (light, dark, auto)
- **FP-UC04-006:** Usuário clica em "Salvar"
- **FP-UC04-007:** Sistema aplica tema visual (CSS variables, dark mode)
- **FP-UC04-008:** Sistema salva preferência no localStorage
- **FP-UC04-009:** Sistema atualiza interface imediatamente
- **FP-UC04-010:** Sistema exibe mensagem de confirmação

### Fluxos Alternativos
- **FA-UC04-001:** Tema "auto" selecionado - Sistema detecta preferência do sistema operacional - Aplica tema correspondente
- **FA-UC04-002:** Usuário cancela operação - Tema não é alterado

### Fluxos de Exceção
- **FE-UC04-001:** Tema inválido informado → Sistema faz fallback para "light" (padrão)
- **FE-UC04-002:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC04-003:** Erro ao salvar no localStorage → Sistema exibe aviso mas tema é aplicado na sessão atual

### Regras de Negócio
- **RN-RF014-11:** Usuário pode escolher entre temas: light, dark, auto
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode alterar suas próprias configurações

### Critérios de Aceite
- **CA-UC04-001:** Tema DEVE ser aplicado imediatamente sem necessidade de recarregar página
- **CA-UC04-002:** Tema DEVE persistir no localStorage entre sessões
- **CA-UC04-003:** Tema "auto" DEVE seguir preferência do sistema operacional
- **CA-UC04-004:** Mudança de tema DEVE aplicar CSS variables correspondentes
- **CA-UC04-005:** Sistema DEVE suportar apenas light, dark, auto

---

## UC05 — Configurar Timezone

### Objetivo
Permitir que o usuário autenticado defina seu fuso horário (timezone IANA).

### Pré-condições
- Usuário autenticado com token JWT válido
- Usuário deve estar ativo (não inativo ou bloqueado)

### Pós-condições
- Timezone selecionado salvo no localStorage
- Todas as datas/horas exibidas no fuso horário correto
- Evento `usuario.preferencias_atualizadas` disparado

### Fluxo Principal
- **FP-UC05-001:** Usuário acessa aba "Preferências" em /user-settings
- **FP-UC05-002:** Sistema valida autenticação JWT
- **FP-UC05-003:** Sistema exibe formulário de preferências
- **FP-UC05-004:** Sistema carrega timezone atual do localStorage
- **FP-UC05-005:** Usuário seleciona timezone no dropdown (lista IANA: America/Sao_Paulo, America/New_York, Europe/London, etc)
- **FP-UC05-006:** Usuário clica em "Salvar"
- **FP-UC05-007:** Sistema aplica timezone em todas as datas/horas exibidas
- **FP-UC05-008:** Sistema salva preferência no localStorage
- **FP-UC05-009:** Sistema atualiza interface imediatamente
- **FP-UC05-010:** Sistema exibe mensagem de confirmação

### Fluxos Alternativos
- **FA-UC05-001:** Usuário cancela operação - Timezone não é alterado

### Fluxos de Exceção
- **FE-UC05-001:** Timezone inválido informado → Sistema faz fallback para America/Sao_Paulo (padrão)
- **FE-UC05-002:** Token JWT expirado → Sistema retorna HTTP 401 → Redirecionamento para login
- **FE-UC05-003:** Erro ao salvar no localStorage → Sistema exibe aviso mas timezone é aplicado na sessão atual

### Regras de Negócio
- **RN-RF014-12:** Sistema oferece lista de timezones IANA comuns (América, Europa, Ásia)
- **RN-RF014-15:** Tela de configurações só acessível por usuários autenticados
- **RN-RF014-16:** Usuário só pode alterar suas próprias configurações

### Critérios de Aceite
- **CA-UC05-001:** Timezone DEVE ser aplicado em todas as datas/horas exibidas
- **CA-UC05-002:** Timezone DEVE persistir no localStorage entre sessões
- **CA-UC05-003:** Lista de timezones DEVE incluir América, Europa, Ásia
- **CA-UC05-004:** Timezone inválido DEVE fazer fallback para America/Sao_Paulo
- **CA-UC05-005:** Formato DEVE seguir padrão IANA (ex: America/Sao_Paulo)

---

## 4. MATRIZ DE RASTREABILIDADE

### Cobertura de Regras de Negócio

| Regra de Negócio | UC Responsável | Descrição |
|------------------|----------------|-----------|
| RN-RF014-01 | UC00, UC01 | Campos somente leitura (Nome, Email, CPF, Empresa) |
| RN-RF014-02 | UC01 | Validação de telefone brasileiro |
| RN-RF014-03 | UC02 | Senha atual obrigatória para alteração |
| RN-RF014-04 | UC02 | Requisitos de nova senha (8+ chars, maiúscula, minúscula, número, especial) |
| RN-RF014-05 | UC02 | Nova senha diferente da atual |
| RN-RF014-06 | UC02 | Blacklist de senhas comuns |
| RN-RF014-07 | UC02 | Senha não pode conter dados pessoais |
| RN-RF014-08 | UC02 | Confirmação de senha |
| RN-RF014-09 | UC03 | Persistência de idioma |
| RN-RF014-10 | UC03 | Idiomas suportados (pt-BR, en-US, es-ES) |
| RN-RF014-11 | UC04 | Temas disponíveis (light, dark, auto) |
| RN-RF014-12 | UC05 | Timezones suportados (IANA) |
| RN-RF014-13 | UC00 | Navegação responsiva (< 1024px drawer) |
| RN-RF014-14 | UC03 | Sincronização de idioma entre componentes |
| RN-RF014-15 | UC00, UC01, UC02, UC03, UC04, UC05 | Usuário logado obrigatório |
| RN-RF014-16 | UC00, UC01, UC02, UC03, UC04, UC05 | Isolamento de dados (usuário só edita suas configurações) |

### Cobertura de Funcionalidades do RF

| Funcionalidade do RF | UC Responsável |
|----------------------|----------------|
| Visualizar Conta | UC00 |
| Editar Dados Pessoais (telefone, data nascimento) | UC01 |
| Alterar Senha | UC02 |
| Configurar Idioma | UC03 |
| Configurar Tema | UC04 |
| Configurar Timezone | UC05 |

**Cobertura Total:** 16/16 Regras de Negócio = **100%**

---

## CHANGELOG

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2025-12-31 | Agência ALC - alc.dev.br | Versão canônica orientada a contrato - Recriação total seguindo template UC.md com cobertura 100% das 16 RNs |
| 1.0 | 2025-12-17 | Sistema | Consolidação de 3 casos de uso (versão antiga) |

# WF-RF007 — Wireframes Canônicos Login e Autenticação (UI Contract)

**Versão:** 1.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF007 - Login e Autenticação
**UC Relacionado:** UC-RF007 (UC00, UC01, UC02, UC03, UC04, UC05, UC06, UC09)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF007 - Login e Autenticação.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional**
- Servir como **fonte de verdade para IA, QA e Desenvolvimento**
- Permitir derivação direta de **TCs E2E e testes de usabilidade**
- Evitar dependência de ferramentas específicas (ex: Filament, React, Vue)

> ⚠️ Este documento descreve **o que a tela deve permitir e comunicar**, não **como será implementado tecnicamente**.

---

## 2. PRINCÍPIOS DE DESIGN (OBRIGATÓRIOS)

### 2.1 Princípios Gerais

- Clareza acima de estética
- Feedback imediato a toda ação do usuário
- Estados explícitos (loading, vazio, erro)
- Não ocultar erros críticos
- Comportamento previsível
- Segurança em primeiro lugar (mensagens genéricas para erros de autenticação)

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis (sem revelar informações sensíveis) |
| Responsividade | Obrigatória |
| Acessibilidade | WCAG 2.1 AA |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Login | UC00, UC09 | Autenticação inicial do usuário |
| WF-02 | Esqueci Minha Senha | UC01 | Solicitação de recuperação de senha |
| WF-03 | Redefinir Senha | UC02 | Criação de nova senha via token |
| WF-04 | Alterar Senha (Primeiro Acesso) | UC03 | Troca obrigatória de senha temporária |
| WF-05 | Conta Bloqueada | UC06 | Informação de bloqueio e desbloqueio |

---

## 4. WF-01 — TELA DE LOGIN

### 4.1 Intenção da Tela
Permitir ao usuário **autenticar-se no sistema** de forma segura, exibindo **logo corporativa do tenant** quando disponível.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Logo Corporativa/Padrão | Image | Logo do Cliente (tenant) ou logo padrão IControlIT |
| CMP-WF01-002 | Campo Email | Input (email) | Campo obrigatório para email do usuário |
| CMP-WF01-003 | Campo Senha | Input (password) | Campo obrigatório para senha |
| CMP-WF01-004 | Checkbox Lembrar-me | Checkbox | Opção para estender validade do refresh token |
| CMP-WF01-005 | Botão Entrar | Button | Ação primária para submeter credenciais |
| CMP-WF01-006 | Link Esqueci Senha | Link | Navegação para recuperação de senha |
| CMP-WF01-007 | Mensagem de Erro | Alert | Exibe erros de validação ou autenticação |
| CMP-WF01-008 | Indicador de Loading | Spinner | Feedback visual durante autenticação |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Carregamento da Tela | Usuário acessa /sign-in | UC00, UC09 | FP-UC00-001, FP-UC09-001 |
| EVT-WF01-002 | Preenchimento Email | Usuário digita no CMP-WF01-002 | UC09 | FP-UC09-002, FP-UC09-003 |
| EVT-WF01-003 | Carregamento de Logo | Sistema identifica ClienteId | UC09 | FP-UC09-004, FP-UC09-005 |
| EVT-WF01-004 | Submissão Formulário | Usuário clica em CMP-WF01-005 | UC00 | FP-UC00-005 |
| EVT-WF01-005 | Erro de Validação | Email vazio ou inválido | UC00 | FE-UC00-001, FE-UC00-002 |
| EVT-WF01-006 | Erro de Autenticação | Credenciais inválidas | UC00 | FA-UC00-001, FE-UC00-004, FE-UC00-005 |
| EVT-WF01-007 | Conta Bloqueada | 5 tentativas falhas | UC00, UC06 | FA-UC00-002, FP-UC06-005 |
| EVT-WF01-008 | Primeiro Acesso | Fl_Primeiro_Acesso = true | UC00, UC03 | FA-UC00-004, FP-UC03-001 |
| EVT-WF01-009 | Navegação Esqueci Senha | Usuário clica em CMP-WF01-006 | UC01 | FP-UC01-001 |

### 4.4 Ações Permitidas
- Preencher email e senha
- Marcar/desmarcar "Lembrar-me"
- Submeter formulário (Enter ou clique no botão)
- Acessar tela de recuperação de senha
- Visualizar mensagens de erro

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está validando credenciais ou carregando logo corporativa

**Exibir:**
- Spinner no botão "Entrar"
- Botão desabilitado
- Mensagem: "Carregando..." (para logo) ou "Autenticando..." (para login)

#### Estado 2: Inicial (Vazio)
**Quando:** Usuário acessa a tela pela primeira vez

**Exibir:**
- Logo padrão IControlIT (ou logo corporativa após identificar ClienteId)
- Formulário limpo
- Campos habilitados
- Botão "Entrar" habilitado

#### Estado 3: Erro de Validação
**Quando:** Campos obrigatórios vazios ou formato inválido

**Exibir:**
- CMP-WF01-007 com mensagem de erro específica:
  - "E-mail é obrigatório"
  - "Formato de e-mail inválido"
  - "Senha é obrigatória"
- Campo com erro destacado (borda vermelha)
- Ícone de erro ao lado do campo

#### Estado 4: Erro de Autenticação
**Quando:** Credenciais inválidas, usuário bloqueado, empresa inativa

**Exibir:**
- CMP-WF01-007 com mensagem **genérica** (segurança):
  - "E-mail ou senha incorretos" (RN-AUTH-011)
  - "Conta bloqueada. Tente novamente em X minutos" (com contador)
  - "Sua empresa está temporariamente inativa. Contate o administrador."
- Incremento invisível do contador de tentativas (backend)

#### Estado 5: Sucesso
**Quando:** Autenticação bem-sucedida

**Exibir:**
- Redirecionamento imediato para /dashboard
- Mensagem de toast (opcional): "Bem-vindo, [Nome]!"

#### Estado 6: Primeiro Acesso
**Quando:** Fl_Primeiro_Acesso = true (UC03)

**Exibir:**
- Redirecionamento para /change-password
- Mensagem: "Primeiro acesso detectado. Por favor, altere sua senha."

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário centralizado, logo reduzida, campos empilhados
- **Tablet:** Formulário centralizado com largura máxima 400px
- **Desktop:** Formulário centralizado com largura máxima 480px, logo em tamanho padrão

#### Acessibilidade (WCAG AA)
- Labels em português claro:
  - "E-mail" (não "Email" ou "Login")
  - "Senha" (com indicador de visibilidade - ícone olho)
- Navegação por teclado:
  - Tab: email → senha → lembrar-me → entrar → esqueci senha
  - Enter: submete formulário
- Contraste mínimo 4.5:1 entre texto e fundo
- Screen readers: aria-label em todos os componentes

#### Feedback ao Usuário
- Validação em tempo real (onBlur) para formato de email
- Loading spinner durante autenticação (não permitir múltiplos cliques)
- Mensagens de erro claras e **genéricas** para segurança
- Toast de sucesso (opcional)

#### Segurança
- Mensagem genérica "E-mail ou senha incorretos" (RN-AUTH-011)
- **NÃO revelar** se usuário existe ou não
- **NÃO revelar** se erro foi no email ou na senha
- Contador de tentativas invisível (backend)
- Rate limiting visual (após 10 tentativas): "Muitas tentativas. Aguarde 1 minuto."

#### Logo Corporativa (UC09)
- Logo carregada após identificação de ClienteId pelo domínio do email
- Fallback para logo padrão IControlIT se:
  - LogoUrl não existe
  - LogoUrl inacessível (404, timeout)
- Logo **NÃO bloqueia** autenticação (falha silenciosa)
- Logo armazenada em localStorage (`cliente_logo_url`) após login

---

## 5. WF-02 — ESQUECI MINHA SENHA

### 5.1 Intenção da Tela
Permitir que o usuário **solicite recuperação de senha** via email de forma segura.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Título | Heading | "Recuperar Senha" |
| CMP-WF02-002 | Descrição | Text | "Digite seu e-mail para receber instruções de recuperação" |
| CMP-WF02-003 | Campo Email | Input (email) | Campo obrigatório para email |
| CMP-WF02-004 | Botão Enviar | Button | Ação primária para solicitar recuperação |
| CMP-WF02-005 | Link Voltar ao Login | Link | Navegação de volta para /sign-in |
| CMP-WF02-006 | Mensagem de Sucesso | Alert (success) | "Se o e-mail estiver cadastrado, você receberá as instruções" |
| CMP-WF02-007 | Mensagem de Erro | Alert (error) | Erros de validação |
| CMP-WF02-008 | Indicador de Loading | Spinner | Feedback visual durante envio |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Carregamento da Tela | Usuário acessa /forgot-password | UC01 | FP-UC01-001, FP-UC01-002 |
| EVT-WF02-002 | Submissão Formulário | Usuário clica em CMP-WF02-004 | UC01 | FP-UC01-005 |
| EVT-WF02-003 | Erro de Validação | Email vazio ou inválido | UC01 | FE-UC01-001, FE-UC01-002 |
| EVT-WF02-004 | Sucesso | Sistema envia email ou não (genérico) | UC01 | FP-UC01-008 |
| EVT-WF02-005 | Navegação Voltar | Usuário clica em CMP-WF02-005 | UC01 | Retorna para WF-01 |

### 5.4 Estados Obrigatórios

#### Estado 1: Loading
**Quando:** Sistema está processando solicitação

**Exibir:**
- Spinner no botão "Enviar"
- Botão desabilitado
- Mensagem: "Enviando..."

#### Estado 2: Inicial
**Quando:** Usuário acessa a tela

**Exibir:**
- Formulário limpo
- Campos habilitados
- Descrição clara

#### Estado 3: Erro de Validação
**Quando:** Email vazio ou formato inválido

**Exibir:**
- CMP-WF02-007 com mensagem:
  - "E-mail é obrigatório"
  - "Formato de e-mail inválido"

#### Estado 4: Sucesso
**Quando:** Sistema processa solicitação (independente de email existir)

**Exibir:**
- CMP-WF02-006 com mensagem **genérica** (RN-AUTH-011):
  - "Se o e-mail estiver cadastrado, você receberá as instruções"
- **NÃO revelar** se email existe ou não

### 5.5 Contratos de Comportamento

#### Responsividade
- **Mobile/Tablet/Desktop:** Formulário centralizado, largura máxima 480px

#### Acessibilidade
- Labels claras
- Navegação por teclado
- Contraste WCAG AA

#### Segurança
- Mensagem genérica (RN-AUTH-011)
- **NÃO revelar** se email existe
- Rate limiting (3 solicitações por minuto por IP)

---

## 6. WF-03 — REDEFINIR SENHA

### 6.1 Intenção da Tela
Permitir que o usuário **crie uma nova senha** usando token de recuperação válido.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Título | Heading | "Redefinir Senha" |
| CMP-WF03-002 | Campo Nova Senha | Input (password) | Campo obrigatório para nova senha |
| CMP-WF03-003 | Campo Confirmar Senha | Input (password) | Campo obrigatório para confirmação |
| CMP-WF03-004 | Indicador Requisitos | Component | Checklist visual de requisitos de senha |
| CMP-WF03-005 | Botão Salvar | Button | Ação primária para salvar nova senha |
| CMP-WF03-006 | Mensagem de Erro | Alert (error) | Erros de validação ou token |
| CMP-WF03-007 | Mensagem de Sucesso | Alert (success) | "Senha alterada com sucesso!" |
| CMP-WF03-008 | Indicador de Loading | Spinner | Feedback visual durante salvamento |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Carregamento da Tela | Usuário acessa /reset-password?token=xxx | UC02 | FP-UC02-002, FP-UC02-003 |
| EVT-WF03-002 | Validação Token | Sistema valida token com backend | UC02 | FP-UC02-003 |
| EVT-WF03-003 | Digitação Senha | Usuário digita em CMP-WF03-002 | UC02 | FP-UC02-006 |
| EVT-WF03-004 | Submissão Formulário | Usuário clica em CMP-WF03-005 | UC02 | FP-UC02-007 |
| EVT-WF03-005 | Erro Token Expirado | Token expirou (> 24h) | UC02 | FE-UC02-001 |
| EVT-WF03-006 | Erro Senha Reutilizada | Senha já usada antes | UC02 | FE-UC02-006 |
| EVT-WF03-007 | Sucesso | Senha alterada com sucesso | UC02 | FP-UC02-011 |

### 6.4 Estados Obrigatórios

#### Estado 1: Loading (Validando Token)
**Quando:** Sistema está validando token ao carregar tela

**Exibir:**
- Spinner de página inteira
- Mensagem: "Validando link de recuperação..."

#### Estado 2: Token Inválido/Expirado
**Quando:** Token não existe, expirou ou já foi usado

**Exibir:**
- CMP-WF03-006 com mensagem:
  - "Link expirado. Solicite nova recuperação."
  - "Link já utilizado. Solicite nova recuperação."
  - "Link inválido."
- Botão "Solicitar Nova Recuperação" (navega para WF-02)

#### Estado 3: Formulário Ativo
**Quando:** Token válido, usuário preenchendo senha

**Exibir:**
- CMP-WF03-004 com requisitos em tempo real:
  - ✅ Mínimo 8 caracteres (verde se atendido, cinza se não)
  - ✅ Letra maiúscula
  - ✅ Letra minúscula
  - ✅ Número
  - ✅ Caractere especial (!@#$%^&*)
  - ✅ Confirmação igual

#### Estado 4: Erro de Validação
**Quando:** Requisitos não atendidos ou senhas diferentes

**Exibir:**
- CMP-WF03-006 com mensagem:
  - "Requisitos de senha não atendidos"
  - "Senhas não coincidem"
  - "Senha já utilizada anteriormente" (últimas 5)

#### Estado 5: Sucesso
**Quando:** Senha alterada com sucesso

**Exibir:**
- CMP-WF03-007: "Senha alterada com sucesso!"
- Redirecionamento automático para /sign-in em 3 segundos
- Mensagem: "Redirecionando para login..."

### 6.5 Contratos de Comportamento

#### Validação em Tempo Real
- Indicador de requisitos atualiza a cada caractere digitado
- Feedback visual imediato (verde/cinza)

#### Responsividade
- **Mobile/Tablet/Desktop:** Formulário centralizado, largura máxima 480px

#### Acessibilidade
- Labels claras
- Indicador de visibilidade de senha (ícone olho)
- Navegação por teclado

#### Segurança (RN-AUTH-004, RN-AUTH-006, RN-AUTH-007)
- Validação requisitos mínimos de senha
- Token válido por 24 horas
- Não reutilizar últimas 5 senhas

---

## 7. WF-04 — ALTERAR SENHA (PRIMEIRO ACESSO)

### 7.1 Intenção da Tela
Forçar troca de **senha temporária** no primeiro acesso.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Título | Heading | "Alterar Senha" |
| CMP-WF04-002 | Mensagem Instrução | Alert (info) | "Primeiro acesso detectado. Crie uma nova senha segura." |
| CMP-WF04-003 | Campo Senha Atual | Input (password) | Campo obrigatório para senha temporária |
| CMP-WF04-004 | Campo Nova Senha | Input (password) | Campo obrigatório para nova senha |
| CMP-WF04-005 | Campo Confirmar Senha | Input (password) | Campo obrigatório para confirmação |
| CMP-WF04-006 | Indicador Requisitos | Component | Checklist visual de requisitos de senha |
| CMP-WF04-007 | Botão Salvar | Button | Ação primária para salvar nova senha |
| CMP-WF04-008 | Mensagem de Erro | Alert (error) | Erros de validação |
| CMP-WF04-009 | Indicador de Loading | Spinner | Feedback visual |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Carregamento da Tela | Sistema detecta Fl_Primeiro_Acesso = true | UC03 | FP-UC03-004, FP-UC03-005 |
| EVT-WF04-002 | Submissão Formulário | Usuário clica em CMP-WF04-007 | UC03 | FP-UC03-007 |
| EVT-WF04-003 | Erro Senha Atual Incorreta | Senha temporária errada | UC03 | FE-UC03-001 |
| EVT-WF04-004 | Erro Nova Igual Atual | Nova senha igual à temporária | UC03 | FE-UC03-002 |
| EVT-WF04-005 | Sucesso | Senha alterada, Fl_Primeiro_Acesso = false | UC03 | FP-UC03-010 |

### 7.4 Estados Obrigatórios

#### Estado 1: Formulário Ativo
**Quando:** Usuário preenchendo campos

**Exibir:**
- CMP-WF04-002: "Primeiro acesso detectado. Crie uma nova senha segura."
- CMP-WF04-006: Indicador de requisitos em tempo real
- Todos os campos habilitados

#### Estado 2: Erro de Validação
**Quando:** Requisitos não atendidos

**Exibir:**
- CMP-WF04-008 com mensagem:
  - "Senha atual incorreta"
  - "Nova senha deve ser diferente da atual"
  - "Requisitos de senha não atendidos"

#### Estado 3: Sucesso
**Quando:** Senha alterada com sucesso

**Exibir:**
- Alert de sucesso: "Senha alterada com sucesso! Faça login novamente."
- Redirecionamento para /sign-in

### 7.5 Contratos de Comportamento

#### Responsividade
- **Mobile/Tablet/Desktop:** Formulário centralizado, largura máxima 480px

#### Acessibilidade
- Labels claras
- Navegação por teclado

#### Segurança (RN-AUTH-008)
- Obriga troca no primeiro acesso
- **NÃO permitir** pular ou cancelar

---

## 8. WF-05 — CONTA BLOQUEADA

### 8.1 Intenção da Tela
Informar o usuário sobre **bloqueio temporário** e **tempo restante**.

### 8.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF05-001 | Ícone Bloqueio | Icon | Ícone visual de cadeado/bloqueio |
| CMP-WF05-002 | Título | Heading | "Conta Bloqueada" |
| CMP-WF05-003 | Mensagem Principal | Alert (warning) | "Sua conta foi bloqueada devido a múltiplas tentativas de acesso" |
| CMP-WF05-004 | Contador Tempo | Text | "Tempo restante: X minutos" (atualizado a cada segundo) |
| CMP-WF05-005 | Botão Voltar ao Login | Button | Navegação de volta para /sign-in |
| CMP-WF05-006 | Link Ajuda | Link | "Precisa de ajuda? Contate o administrador" |

### 8.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF05-001 | Exibição de Bloqueio | Sistema retorna erro 423 (Locked) | UC06 | FP-UC06-005 |
| EVT-WF05-002 | Atualização Contador | A cada segundo | UC06 | FP-UC06-005 |
| EVT-WF05-003 | Desbloqueio Automático | 30 minutos se passam | UC06 | FP-UC06-008 |
| EVT-WF05-004 | Navegação Voltar | Usuário clica em CMP-WF05-005 | UC06 | Retorna para WF-01 |

### 8.4 Estados Obrigatórios

#### Estado 1: Bloqueado
**Quando:** Conta bloqueada por 5 tentativas falhas

**Exibir:**
- CMP-WF05-001: Ícone de cadeado vermelho
- CMP-WF05-002: "Conta Bloqueada"
- CMP-WF05-003: "Sua conta foi bloqueada devido a múltiplas tentativas de acesso"
- CMP-WF05-004: Contador regressivo (ex: "Tempo restante: 25 minutos")

#### Estado 2: Desbloqueado
**Quando:** 30 minutos se passam ou admin desbloqueia

**Exibir:**
- Redirecionamento automático para /sign-in
- Toast: "Sua conta foi desbloqueada. Você já pode fazer login."

### 8.5 Contratos de Comportamento

#### Contador Regressivo
- Atualiza a cada segundo
- Formato: "X minutos" ou "X minutos e Y segundos"
- Quando chegar a zero: redireciona para /sign-in

#### Responsividade
- **Mobile/Tablet/Desktop:** Mensagem centralizada, largura máxima 480px

#### Acessibilidade
- Mensagem clara e descritiva
- Navegação por teclado

#### Segurança (RN-AUTH-003)
- Bloqueio após 5 tentativas falhas em 15 minutos
- Desbloqueio automático após 30 minutos

---

## 9. NOTIFICAÇÕES

### 9.1 Tipos Padronizados

| Tipo | Uso | Exemplo |
|----|----|----|
| Sucesso | Operação concluída | "Login realizado com sucesso!" |
| Erro | Falha bloqueante | "E-mail ou senha incorretos" |
| Aviso | Atenção necessária | "Conta bloqueada. Tente novamente em X minutos" |
| Info | Feedback neutro | "Se o e-mail estiver cadastrado, você receberá as instruções" |

---

## 10. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| Mobile (< 768px) | Formulário em coluna, logo reduzida, campos empilhados |
| Tablet (768px - 1024px) | Formulário centralizado, largura máxima 400px |
| Desktop (> 1024px) | Formulário centralizado, largura máxima 480px, logo em tamanho padrão |

---

## 11. ACESSIBILIDADE (OBRIGATÓRIO)

- **Navegação por teclado:** Tab, Enter, Esc
- **Leitura por screen readers:** aria-label, role, alt text
- **Contraste mínimo WCAG AA:** 4.5:1 entre texto e fundo
- **Labels e descrições claras:** Em português, sem ambiguidade
- **Feedback de erro acessível:** Mensagens lidas por screen readers
- **Indicador de visibilidade de senha:** Ícone olho (toggle)

---

## 12. RASTREABILIDADE

| Wireframe | UC(s) | RF |
|---------|----|----|
| WF-01 | UC00, UC09 | RF007 |
| WF-02 | UC01 | RF007 |
| WF-03 | UC02 | RF007 |
| WF-04 | UC03 | RF007 |
| WF-05 | UC06 | RF007 |

**Cobertura:** 100% dos UCs do RF007 (6/7 UCs mapeados em wireframes)

**Observação:** UC04 (Logout) e UC05 (Renovar Sessão) não requerem wireframes dedicados (são ações em outras telas).

---

## 13. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, tipografia, espaçamentos específicos)
- Escolha de framework (React, Vue, Angular)
- Design gráfico definitivo
- Animações avançadas (transições, micro-interações)
- Implementação técnica (código)

---

## 14. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 1.0 | 2026-01-04 | Agência ALC - alc.dev.br | Criação do WF-RF007 com cobertura 100% dos UCs |

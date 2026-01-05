# WF-RF014 — Wireframes Canônicos (UI Contract)

**Versão:** 2.0
**Data:** 2026-01-04
**Autor:** Agência ALC - alc.dev.br

**RF Relacionado:** RF014 - Configurações do Usuário
**UC Relacionado:** UC-RF014 (UC00, UC01, UC02, UC03)
**Plataforma:** Web (Responsivo)

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RF014 - Configurações do Usuário.

Ele **não é um layout final**, nem um guia de framework específico.
Seu objetivo é:

- Garantir **consistência visual e funcional** na tela de configurações pessoais
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
- Segurança visível (campos somente leitura claramente identificados)

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória (Mobile, Tablet, Desktop) |
| Campos somente leitura | Visualmente distintos (desabilitados ou bloqueados) |
| Validações de senha | Requisitos exibidos explicitamente |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Configurações - Visualização Geral | UC00 | Exibir dados pessoais, preferências e informações de auditoria |
| WF-02 | Dados Pessoais - Edição | UC01 | Editar telefone e data de nascimento |
| WF-03 | Segurança - Alterar Senha | UC02 | Permitir alteração segura de senha |
| WF-04 | Preferências - Edição | UC03 | Configurar idioma, tema e timezone |

---

## 4. WF-01 — CONFIGURAÇÕES - VISUALIZAÇÃO GERAL

### 4.1 Intenção da Tela
Permitir ao usuário autenticado **visualizar todas as suas configurações atuais** (dados pessoais, empresa, preferências, auditoria) e navegar entre seções editáveis.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Abas de Navegação | Tabs | Navegação entre Dados Pessoais, Segurança, Preferências |
| CMP-WF01-002 | Campo Nome | Input (readonly) | Exibe nome completo do usuário (somente leitura) |
| CMP-WF01-003 | Campo Email | Input (readonly) | Exibe email do usuário (somente leitura) |
| CMP-WF01-004 | Campo CPF | Input (readonly) | Exibe CPF do usuário (somente leitura) |
| CMP-WF01-005 | Campo Telefone | Input (readonly) | Exibe telefone do usuário (somente leitura) |
| CMP-WF01-006 | Campo Data Nascimento | Input (readonly) | Exibe data de nascimento (somente leitura) |
| CMP-WF01-007 | Campo Empresa | Input (readonly) | Exibe empresa vinculada (somente leitura) |
| CMP-WF01-008 | Campo Idioma | Input (readonly) | Exibe idioma atual (somente leitura) |
| CMP-WF01-009 | Campo Tema | Input (readonly) | Exibe tema atual (somente leitura) |
| CMP-WF01-010 | Campo Timezone | Input (readonly) | Exibe timezone atual (somente leitura) |
| CMP-WF01-011 | Info Criado em | Text | Exibe data/hora de criação (created_at) |
| CMP-WF01-012 | Info Atualizado em | Text | Exibe data/hora última atualização (updated_at) |
| CMP-WF01-013 | Botão Editar Dados Pessoais | Button | Navega para WF-02 (edição de telefone/data nascimento) |
| CMP-WF01-014 | Botão Alterar Senha | Button | Navega para WF-03 (alteração de senha) |
| CMP-WF01-015 | Botão Editar Preferências | Button | Navega para WF-04 (edição de preferências) |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Carregamento da Tela | Usuário acessa menu Configurações | UC00 | FP-UC00-001 |
| EVT-WF01-002 | Validação de Token | Sistema valida JWT ao carregar tela | UC00 | FP-UC00-002 |
| EVT-WF01-003 | Navegação entre Abas | Usuário clica em aba (Dados Pessoais, Segurança, Preferências) | UC00 | FA-UC00-001 |
| EVT-WF01-004 | Clique em Editar Dados Pessoais | Usuário clica em CMP-WF01-013 | UC01 | Navega para WF-02 |
| EVT-WF01-005 | Clique em Alterar Senha | Usuário clica em CMP-WF01-014 | UC02 | Navega para WF-03 |
| EVT-WF01-006 | Clique em Editar Preferências | Usuário clica em CMP-WF01-015 | UC03 | Navega para WF-04 |

### 4.4 Ações Permitidas
- Visualizar dados pessoais (nome, email, CPF, telefone, data nascimento)
- Visualizar empresa vinculada
- Visualizar preferências atuais (idioma, tema, timezone)
- Visualizar informações de auditoria (created_at, updated_at)
- Navegar entre abas (Dados Pessoais, Segurança, Preferências)
- Navegar para tela de edição de dados pessoais
- Navegar para tela de alteração de senha
- Navegar para tela de edição de preferências

### 4.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados do usuário autenticado
**Exibir:**
- Skeleton loader (formulário)
- Mensagem: "Carregando configurações..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Usuário não encontrado no banco (cenário improvável)
**Exibir:**
- Ícone de erro
- Mensagem: "Usuário não encontrado"
- Botão "Voltar para Dashboard"

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, etc.) ou token inválido
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar configurações. Tente novamente."
- Botão "Recarregar"
- Se token inválido: redirecionar para login

#### Estado 4: Dados (Configurações Exibidas)
**Quando:** Dados do usuário carregados com sucesso
**Exibir:**
- Todas as seções (Dados Pessoais, Segurança, Preferências) conforme aba selecionada
- Campos somente leitura (nome, email, CPF, empresa) visualmente distintos (desabilitados)
- Campos editáveis (telefone, data nascimento) destacados se aplicável
- Botões de ação (Editar Dados Pessoais, Alterar Senha, Editar Preferências)
- Informações de auditoria (created_at, updated_at)

### 4.6 Contratos de Comportamento

#### Responsividade
- **Mobile (< 768px):** Abas viram drawer overlay ou accordion; campos empilhados
- **Tablet (768px - 1024px):** Abas horizontais; formulário em 2 colunas
- **Desktop (> 1024px):** Layout completo com abas horizontais; formulário em 3 colunas

#### Acessibilidade (WCAG AA)
- Labels em português claro ("Nome Completo", "Email", "CPF", "Telefone", etc.)
- Campos somente leitura com aria-readonly="true"
- Navegação por teclado (Tab, Enter, Setas)
- Contraste mínimo 4.5:1
- Screen reader: anunciar "Campo somente leitura" para campos bloqueados

#### Feedback ao Usuário
- Loading spinner durante carregamento inicial
- Token inválido → redirecionar para login automaticamente
- Erro ao carregar → exibir mensagem clara com botão "Recarregar"

#### Segurança
- Dados do usuário carregados **SOMENTE** baseados no UserId do token JWT
- Campos somente leitura (nome, email, CPF, empresa) devem estar **visualmente bloqueados**
- Nenhuma tentativa de editar campos bloqueados via UI deve ser possível

---

## 5. WF-02 — DADOS PESSOAIS - EDIÇÃO

### 5.1 Intenção da Tela
Permitir ao usuário autenticado **editar telefone e data de nascimento** (únicos campos editáveis de dados pessoais).

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo Nome | Input (readonly) | Exibe nome completo (somente leitura) |
| CMP-WF02-002 | Campo Email | Input (readonly) | Exibe email (somente leitura) |
| CMP-WF02-003 | Campo CPF | Input (readonly) | Exibe CPF (somente leitura) |
| CMP-WF02-004 | Campo Telefone | Input (editable) | Permite editar telefone (formato brasileiro) |
| CMP-WF02-005 | Campo Data Nascimento | DatePicker (editable) | Permite editar data de nascimento |
| CMP-WF02-006 | Botão Salvar | Button | Salva alterações (ação primária) |
| CMP-WF02-007 | Botão Cancelar | Button | Cancela edição e volta para WF-01 |
| CMP-WF02-008 | Mensagem de Erro | Alert | Exibe erros de validação (telefone inválido, data futura) |
| CMP-WF02-009 | Mensagem de Sucesso | Toast | Exibe confirmação de sucesso após salvar |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Carregamento da Tela | Usuário acessa edição de dados pessoais | UC01 | FP-UC01-001 |
| EVT-WF02-002 | Alteração de Telefone | Usuário altera campo CMP-WF02-004 | UC01 | FP-UC01-003 |
| EVT-WF02-003 | Alteração de Data Nascimento | Usuário altera campo CMP-WF02-005 | UC01 | FP-UC01-003 |
| EVT-WF02-004 | Submissão de Formulário | Usuário clica em CMP-WF02-006 (Salvar) | UC01 | FP-UC01-004 |
| EVT-WF02-005 | Cancelamento | Usuário clica em CMP-WF02-007 (Cancelar) | UC01 | FA-UC01-001 |
| EVT-WF02-006 | Validação de Telefone | Sistema valida formato após blur ou submissão | UC01 | FP-UC01-005 |
| EVT-WF02-007 | Validação de Data | Sistema valida data não futura após blur ou submissão | UC01 | FP-UC01-006 |
| EVT-WF02-008 | Exibição de Erro | Sistema retorna erro de validação | UC01 | FE-UC01-001, FE-UC01-002 |
| EVT-WF02-009 | Exibição de Sucesso | Sistema retorna sucesso após salvar | UC01 | FP-UC01-010 |

### 5.4 Ações Permitidas
- Editar telefone (formato brasileiro: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX)
- Editar data de nascimento (não pode ser futura)
- Salvar alterações
- Cancelar edição

### 5.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está carregando dados do usuário
**Exibir:**
- Skeleton loader (formulário)
- Mensagem: "Carregando dados..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** N/A (usuário sempre existe se autenticado)

#### Estado 3: Erro (Falha ao Carregar ou Salvar)
**Quando:** API retorna erro ao carregar ou salvar
**Exibir:**
- Mensagem de erro clara em CMP-WF02-008
- Telefone inválido: "Telefone deve seguir formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"
- Data futura: "Data de nascimento não pode ser futura"
- Erro ao salvar: "Erro ao atualizar dados pessoais. Tente novamente."

#### Estado 4: Dados (Formulário Exibido)
**Quando:** Dados carregados com sucesso
**Exibir:**
- Formulário com campos nome, email, CPF (somente leitura) e telefone, data nascimento (editáveis)
- Botões Salvar e Cancelar
- Validações em tempo real (telefone, data nascimento)

#### Estado 5: Sucesso (Salvamento Confirmado)
**Quando:** Dados salvos com sucesso
**Exibir:**
- Toast de sucesso: "Dados pessoais atualizados com sucesso"
- Voltar automaticamente para WF-01 após 2 segundos (ou permitir fechar toast)

### 5.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em 1 coluna; botões empilhados
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 2 colunas

#### Acessibilidade (WCAG AA)
- Labels claros ("Telefone", "Data de Nascimento")
- Campos somente leitura com aria-readonly="true"
- Campos editáveis com aria-required="true" se obrigatórios
- Erros de validação associados aos campos (aria-describedby)
- Navegação por teclado (Tab, Enter para salvar, Esc para cancelar)
- Contraste mínimo 4.5:1

#### Feedback ao Usuário
- Validação de telefone em tempo real (blur) com regex brasileiro
- Validação de data nascimento em tempo real (blur) para evitar data futura
- Loading spinner durante salvamento
- Toast de sucesso após salvamento
- Mensagem de erro clara e acionável

#### Segurança
- Campos nome, email, CPF e empresa **DEVEM** estar bloqueados (readonly)
- Validação de formato de telefone no backend (não confiar apenas no frontend)
- Validação de data nascimento no backend (não confiar apenas no frontend)

---

## 6. WF-03 — SEGURANÇA - ALTERAR SENHA

### 6.1 Intenção da Tela
Permitir ao usuário autenticado **alterar sua senha de acesso** com validações de segurança rigorosas.

### 6.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF03-001 | Campo Senha Atual | Input (password) | Senha atual do usuário (obrigatório) |
| CMP-WF03-002 | Campo Nova Senha | Input (password) | Nova senha (obrigatório, validações de segurança) |
| CMP-WF03-003 | Campo Confirmar Nova Senha | Input (password) | Confirmação da nova senha (obrigatório) |
| CMP-WF03-004 | Requisitos de Senha | Info Box | Exibe requisitos de senha forte (8+ caracteres, maiúscula, minúscula, número, especial) |
| CMP-WF03-005 | Indicador de Força | Progress Bar | Exibe força da senha (fraca, média, forte) |
| CMP-WF03-006 | Botão Alterar Senha | Button | Submete formulário (ação primária) |
| CMP-WF03-007 | Botão Cancelar | Button | Cancela alteração e volta para WF-01 |
| CMP-WF03-008 | Mensagem de Erro | Alert | Exibe erros de validação (senha atual incorreta, requisitos não atendidos, etc.) |
| CMP-WF03-009 | Mensagem de Sucesso | Toast | Exibe confirmação de sucesso após alteração |

### 6.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF03-001 | Carregamento da Tela | Usuário acessa alterar senha | UC02 | FP-UC02-001 |
| EVT-WF03-002 | Digitação de Nova Senha | Usuário digita em CMP-WF03-002 | UC02 | FP-UC02-003 |
| EVT-WF03-003 | Submissão de Formulário | Usuário clica em CMP-WF03-006 | UC02 | FP-UC02-004 |
| EVT-WF03-004 | Cancelamento | Usuário clica em CMP-WF03-007 | UC02 | FA-UC02-001 |
| EVT-WF03-005 | Validação de Senha Atual | Sistema valida senha atual após blur ou submissão | UC02 | FP-UC02-005 |
| EVT-WF03-006 | Validação de Senha Forte | Sistema valida requisitos de senha após blur ou submissão | UC02 | FP-UC02-006 |
| EVT-WF03-007 | Validação de Senha Diferente | Sistema valida que nova senha é diferente da atual | UC02 | FP-UC02-007 |
| EVT-WF03-008 | Validação de Blacklist | Sistema valida que senha não está na blacklist | UC02 | FP-UC02-008 |
| EVT-WF03-009 | Validação de Dados Pessoais | Sistema valida que senha não contém nome/email | UC02 | FP-UC02-009 |
| EVT-WF03-010 | Validação de Confirmação | Sistema valida que confirmação é idêntica | UC02 | FP-UC02-010 |
| EVT-WF03-011 | Exibição de Erro | Sistema retorna erro de validação | UC02 | FE-UC02-001 a FE-UC02-008 |
| EVT-WF03-012 | Exibição de Sucesso | Sistema retorna sucesso após alterar | UC02 | FP-UC02-016 |

### 6.4 Ações Permitidas
- Digitar senha atual
- Digitar nova senha (com validações de segurança)
- Digitar confirmação de nova senha
- Visualizar requisitos de senha forte em tempo real
- Visualizar indicador de força de senha
- Alterar senha
- Cancelar alteração

### 6.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está processando alteração de senha
**Exibir:**
- Loading spinner no botão "Alterar Senha"
- Mensagem: "Alterando senha..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** N/A (formulário sempre disponível)

#### Estado 3: Erro (Validação Falhada)
**Quando:** Alguma validação falha
**Exibir:**
- Mensagens de erro específicas em CMP-WF03-008:
  - Senha atual incorreta: "Senha atual incorreta"
  - Requisitos não atendidos: "Senha deve ter mínimo 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial"
  - Senha igual à atual: "Nova senha deve ser diferente da senha atual"
  - Senha na blacklist: "Senha muito comum, escolha outra"
  - Senha contém dados pessoais: "Senha não pode conter seu nome ou email"
  - Confirmação não coincide: "Senhas não coincidem"
  - Rate limiting: "Muitas tentativas, aguarde X minutos"
  - Erro ao salvar: "Erro ao alterar senha. Tente novamente."

#### Estado 4: Dados (Formulário Exibido)
**Quando:** Formulário carregado e pronto para entrada
**Exibir:**
- Formulário com 3 campos (senha atual, nova senha, confirmar nova senha)
- Requisitos de senha forte em CMP-WF03-004
- Indicador de força de senha em CMP-WF03-005
- Botões Alterar Senha e Cancelar
- Validações em tempo real (força de senha, confirmação)

#### Estado 5: Sucesso (Senha Alterada)
**Quando:** Senha alterada com sucesso
**Exibir:**
- Toast de sucesso: "Senha alterada com sucesso"
- Voltar automaticamente para WF-01 após 2 segundos (ou permitir fechar toast)

### 6.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em 1 coluna; botões empilhados
- **Tablet:** Formulário em 1 coluna
- **Desktop:** Formulário em 1 coluna (centralizado)

#### Acessibilidade (WCAG AA)
- Labels claros ("Senha Atual", "Nova Senha", "Confirmar Nova Senha")
- Campos de senha com type="password"
- Opção de "Mostrar Senha" (toggle) para acessibilidade
- Requisitos de senha lidos por screen reader
- Erros de validação associados aos campos (aria-describedby)
- Navegação por teclado (Tab, Enter para submeter, Esc para cancelar)
- Contraste mínimo 4.5:1

#### Feedback ao Usuário
- Indicador de força de senha em tempo real (fraca, média, forte)
- Requisitos de senha exibidos claramente acima do campo
- Validação de confirmação em tempo real (blur)
- Loading spinner durante alteração
- Toast de sucesso após alteração
- Mensagens de erro claras e específicas

#### Segurança
- **NUNCA** exibir senha atual em texto plano
- Validação de senha atual no backend (não confiar apenas no frontend)
- Validação de requisitos de senha forte no backend
- Validação de blacklist no backend
- Validação de dados pessoais no backend
- Rate limiting aplicado no backend (ex: máximo 5 tentativas em 15 minutos)
- Auditoria obrigatória registrada no backend (UserId, IP, Timestamp)
- Hash seguro (BCrypt/PBKDF2) gerado no backend

---

## 7. WF-04 — PREFERÊNCIAS - EDIÇÃO

### 7.1 Intenção da Tela
Permitir ao usuário autenticado **atualizar preferências de interface** (idioma, tema visual, timezone) com aplicação imediata.

### 7.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF04-001 | Dropdown Idioma | Select | Seleção de idioma (pt-BR, en-US, es-ES) |
| CMP-WF04-002 | Dropdown Tema | Select | Seleção de tema (light, dark, auto) |
| CMP-WF04-003 | Dropdown Timezone | Select | Seleção de timezone (lista IANA) |
| CMP-WF04-004 | Preview de Tema | Visual Box | Prévia do tema selecionado (opcional) |
| CMP-WF04-005 | Botão Salvar | Button | Salva preferências (ação primária) |
| CMP-WF04-006 | Botão Cancelar | Button | Cancela edição e volta para WF-01 |
| CMP-WF04-007 | Mensagem de Erro | Alert | Exibe erros de validação (idioma inválido, etc.) |
| CMP-WF04-008 | Mensagem de Sucesso | Toast | Exibe confirmação de sucesso após salvar |

### 7.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF04-001 | Carregamento da Tela | Usuário acessa edição de preferências | UC03 | FP-UC03-001 |
| EVT-WF04-002 | Seleção de Idioma | Usuário seleciona idioma em CMP-WF04-001 | UC03 | FP-UC03-004 |
| EVT-WF04-003 | Seleção de Tema | Usuário seleciona tema em CMP-WF04-002 | UC03 | FP-UC03-004 |
| EVT-WF04-004 | Seleção de Timezone | Usuário seleciona timezone em CMP-WF04-003 | UC03 | FP-UC03-004 |
| EVT-WF04-005 | Submissão de Formulário | Usuário clica em CMP-WF04-005 (Salvar) | UC03 | FP-UC03-005 |
| EVT-WF04-006 | Cancelamento | Usuário clica em CMP-WF04-006 (Cancelar) | UC03 | FA-UC03-002 |
| EVT-WF04-007 | Validação de Valores | Sistema valida que valores selecionados são válidos | UC03 | FP-UC03-006 |
| EVT-WF04-008 | Aplicação de Idioma | Sistema aplica idioma imediatamente após salvar | UC03 | FP-UC03-010 |
| EVT-WF04-009 | Aplicação de Tema | Sistema aplica tema imediatamente após salvar | UC03 | FP-UC03-011 |
| EVT-WF04-010 | Aplicação de Timezone | Sistema ajusta datas/horas após salvar | UC03 | FP-UC03-012 |
| EVT-WF04-011 | Exibição de Erro | Sistema retorna erro de validação | UC03 | FE-UC03-001 a FE-UC03-004 |
| EVT-WF04-012 | Exibição de Sucesso | Sistema retorna sucesso após salvar | UC03 | FP-UC03-013 |

### 7.4 Ações Permitidas
- Selecionar idioma (pt-BR, en-US, es-ES)
- Selecionar tema (light, dark, auto)
- Selecionar timezone (lista IANA)
- Visualizar prévia de tema (opcional)
- Salvar preferências
- Cancelar edição

### 7.5 Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está carregando opções disponíveis ou salvando preferências
**Exibir:**
- Skeleton loader (formulário)
- Mensagem: "Carregando preferências..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** N/A (usuário sempre tem preferências, mesmo que padrão)

#### Estado 3: Erro (Falha ao Carregar ou Salvar)
**Quando:** API retorna erro ao carregar ou salvar
**Exibir:**
- Mensagem de erro clara em CMP-WF04-007:
  - Idioma inválido: "Idioma inválido"
  - Tema inválido: "Tema inválido"
  - Timezone inválido: "Timezone inválido"
  - Erro ao salvar: "Erro ao atualizar preferências. Tente novamente."

#### Estado 4: Dados (Formulário Exibido)
**Quando:** Opções carregadas com sucesso
**Exibir:**
- Formulário com 3 dropdowns (idioma, tema, timezone)
- Opções disponíveis em cada dropdown
- Prévia de tema (opcional)
- Botões Salvar e Cancelar
- Validações em tempo real (valores válidos)

#### Estado 5: Sucesso (Preferências Salvas)
**Quando:** Preferências salvas com sucesso
**Exibir:**
- Toast de sucesso: "Preferências atualizadas com sucesso"
- Aplicar idioma imediatamente (recarregar traduções via Transloco)
- Aplicar tema imediatamente (trocar classe CSS)
- Aplicar timezone (ajustar exibição de datas/horas)
- Voltar automaticamente para WF-01 após 2 segundos (ou permitir fechar toast)

### 7.6 Contratos de Comportamento

#### Responsividade
- **Mobile:** Formulário em 1 coluna; dropdowns full-width
- **Tablet:** Formulário em 2 colunas
- **Desktop:** Formulário em 2 colunas

#### Acessibilidade (WCAG AA)
- Labels claros ("Idioma", "Tema", "Timezone")
- Dropdowns com aria-label
- Navegação por teclado (Tab, Enter, Setas para navegar em dropdown)
- Contraste mínimo 4.5:1
- Screen reader: anunciar opções disponíveis em cada dropdown

#### Feedback ao Usuário
- Prévia de tema em tempo real (opcional)
- Loading spinner durante salvamento
- Toast de sucesso após salvamento
- Aplicação imediata de preferências (idioma, tema, timezone)
- Mensagem de erro clara e acionável

#### Segurança
- Validação de valores selecionados no backend (não confiar apenas no frontend)
- Lista de opções válidas deve vir do backend (idioma: pt-BR, en-US, es-ES; tema: light, dark, auto; timezone: lista IANA)

#### Aplicação Imediata
- **Idioma:** Sistema deve recarregar traduções via Transloco **sem reload da página**
- **Tema:** Sistema deve trocar classe CSS **imediatamente** (ex: `<body class="theme-dark">`)
- **Timezone:** Sistema deve ajustar exibição de datas/horas **imediatamente**

---

## 8. NOTIFICAÇÕES

### 8.1 Tipos Padronizados

| Tipo | Uso | Exemplo |
|----|----|---------|
| Sucesso | Operação concluída | "Dados pessoais atualizados com sucesso" |
| Erro | Falha bloqueante | "Senha atual incorreta" |
| Aviso | Atenção necessária | "Nova senha deve ser diferente da senha atual" |
| Info | Feedback neutro | "Carregando configurações..." |

---

## 9. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| Mobile (< 768px) | Layout em 1 coluna; abas viram drawer/accordion; botões empilhados |
| Tablet (768px - 1024px) | Layout em 2 colunas; abas horizontais |
| Desktop (> 1024px) | Layout completo; formulário em 2-3 colunas; abas horizontais |

---

## 10. ACESSIBILIDADE (OBRIGATÓRIO)

- Navegação por teclado (Tab, Enter, Esc, Setas)
- Leitura por screen readers (labels claros, aria-labels, aria-readonly)
- Contraste mínimo WCAG AA (4.5:1)
- Labels e descrições claras em português
- Campos somente leitura identificados visualmente e por aria-readonly
- Erros de validação associados aos campos (aria-describedby)
- Botões com aria-label quando ícone apenas

---

## 11. RASTREABILIDADE

| Wireframe | UC | RF | Descrição |
|---------|----|----|-----------|
| WF-01 | UC00 | RF014 | Visualizar Configurações Pessoais |
| WF-02 | UC01 | RF014 | Atualizar Dados Pessoais (telefone, data nascimento) |
| WF-03 | UC02 | RF014 | Alterar Senha |
| WF-04 | UC03 | RF014 | Atualizar Preferências de Interface (idioma, tema, timezone) |

---

## 12. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final (cores, fontes, ícones específicos)
- Escolha de framework (Angular Material, Filament, React, Vue)
- Design gráfico definitivo
- Animações avançadas
- Alteração de nome, email, CPF ou empresa (campos somente leitura)
- Criação de novos usuários (fora do escopo deste RF)
- Gestão de permissões (fora do escopo deste RF)

---

## 13. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | 2026-01-04 | Agência ALC - alc.dev.br | Wireframes canônicos para RF014 - Configurações do Usuário (cobertura 100% dos UCs: UC00, UC01, UC02, UC03) |

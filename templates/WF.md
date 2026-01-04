# WF-RFXXX — Wireframes Canônicos (UI Contract)

**Versão:** 2.0
**Data:** YYYY-MM-DD  
**Autor:** Agência ALC - alc.dev.br  

**RF Relacionado:** RFXXX - [Nome do Requisito Funcional]  
**UC Relacionado:** UC-RFXXX (todos os UCs)  
**Plataforma:** Web (Responsivo)  

---

## 1. OBJETIVO DO DOCUMENTO

Este documento define os **contratos visuais e comportamentais de interface** do RFXXX.

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

### 2.2 Padrões Globais

| Item | Regra |
|----|----|
| Ações primárias | Sempre visíveis |
| Ações destrutivas | Sempre confirmadas |
| Estados vazios | Devem orientar o usuário |
| Erros | Devem ser claros e acionáveis |
| Responsividade | Obrigatória |

---

## 3. MAPA DE TELAS (COBERTURA TOTAL DO RF)

| ID | Tela | UC(s) Relacionado(s) | Finalidade |
|----|----|----------------------|------------|
| WF-01 | Listagem | UC00 | Descoberta e acesso |
| WF-02 | Criar | UC01 | Entrada de dados |
| WF-03 | Editar | UC03 | Alteração de dados |
| WF-04 | Visualizar | UC02 | Consulta |
| WF-05 | Confirmação | UC04 | Ação destrutiva |

---

## 4. WF-01 — LISTAGEM

### 4.1 Intenção da Tela
Permitir ao usuário **localizar, filtrar e acessar registros**.

### 4.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF01-001 | Botão "Criar" | Button | Ação primária para criar novo registro |
| CMP-WF01-002 | Campo de Busca | Input | Busca textual nos registros |
| CMP-WF01-003 | Filtro de Status | Dropdown | Filtrar por status ativo/inativo |
| CMP-WF01-004 | Tabela de Registros | DataTable | Exibição dos registros com paginação |
| CMP-WF01-005 | Botão Editar | IconButton | Ação para editar registro (cada linha) |
| CMP-WF01-006 | Botão Excluir | IconButton | Ação para excluir registro (cada linha) |
| CMP-WF01-007 | Paginação | Pagination | Controles de navegação entre páginas |

### 4.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF01-001 | Clique em "Criar" | Usuário clica no botão CMP-WF01-001 | UC01 | FP-UC01-001 |
| EVT-WF01-002 | Busca textual | Usuário digita no campo CMP-WF01-002 | UC00 | FA-UC00-001 |
| EVT-WF01-003 | Filtro por status | Usuário seleciona no dropdown CMP-WF01-003 | UC00 | FA-UC00-003 |
| EVT-WF01-004 | Clique em linha | Usuário clica em registro na tabela CMP-WF01-004 | UC02 | FP-UC02-001 |
| EVT-WF01-005 | Clique em Editar | Usuário clica em CMP-WF01-005 | UC03 | FP-UC03-001 |
| EVT-WF01-006 | Clique em Excluir | Usuário clica em CMP-WF01-006 | UC04 | FP-UC04-001 |
| EVT-WF01-007 | Mudança de página | Usuário interage com CMP-WF01-007 | UC00 | FP-UC00-004 |

### 4.4 Ações Permitidas
- Buscar registros
- Filtrar por atributos relevantes
- Ordenar resultados
- Acessar detalhes
- Iniciar criação

### 4.5 Estados Obrigatórios

| Estado | Comportamento |
|------|---------------|
| Loading | Indicador visual |
| Vazio | Mensagem + CTA |
| Erro | Mensagem + retry |
| Dados | Lista paginada |

### 4.6 Contratos de Comportamento

- Apenas dados do tenant atual são exibidos
- Registros excluídos não aparecem por padrão
- Paginação consistente
- Filtros acumuláveis

---

## 5. WF-02 — CRIAÇÃO

### 5.1 Intenção da Tela
Permitir **criação segura e validada** de um novo registro.

### 5.2 Componentes de Interface

| ID | Componente | Tipo | Descrição |
|----|-----------|------|-----------|
| CMP-WF02-001 | Campo Nome | Input | Campo obrigatório para nome do registro |
| CMP-WF02-002 | Campo Descrição | Textarea | Campo opcional para descrição |
| CMP-WF02-003 | Campo Status | Dropdown | Seleção de status (ativo/inativo) |
| CMP-WF02-004 | Botão Salvar | Button | Ação primária para salvar registro |
| CMP-WF02-005 | Botão Cancelar | Button | Ação secundária para cancelar criação |
| CMP-WF02-006 | Mensagem de Erro | Alert | Exibe erros de validação |

### 5.3 Eventos de UI

| ID | Evento | Gatilho | UC Relacionado | Fluxo |
|----|--------|---------|----------------|-------|
| EVT-WF02-001 | Submissão de Formulário | Usuário clica em CMP-WF02-004 | UC01 | FP-UC01-005 |
| EVT-WF02-002 | Cancelamento | Usuário clica em CMP-WF02-005 | UC01 | FA-UC01-002 |
| EVT-WF02-003 | Validação de Campo | Usuário sai de campo obrigatório vazio | UC01 | FE-UC01-001 |
| EVT-WF02-004 | Exibição de Erro | Sistema retorna erro de validação | UC01 | FE-UC01-001 |

### 5.4 Comportamentos Obrigatórios

- Campos obrigatórios destacados
- Validação antes do envio
- Feedback imediato
- Opção de cancelar

### 5.5 Estados

| Estado | Comportamento |
|------|---------------|
| Inicial | Formulário limpo |
| Erro | Campos destacados |
| Sucesso | Confirmação clara |
| Cancelamento | Confirmação se houver dados |

---

## 6. WF-03 — EDIÇÃO

### 6.1 Intenção da Tela
Permitir **alteração controlada** de dados existentes.

### 6.2 Regras Visuais

- Dados atuais pré-carregados
- Diferença entre valor original e alterado
- Feedback de salvamento

### 6.3 Restrições

- Campos bloqueados devem ser visíveis
- Conflitos devem ser comunicados

---

## 7. WF-04 — VISUALIZAÇÃO

### 7.1 Intenção da Tela
Permitir **consulta completa e segura** do registro.

### 7.2 Conteúdos Obrigatórios

- Dados principais
- Status atual
- Informações de auditoria
- Ações disponíveis conforme permissão

---

## 8. WF-05 — CONFIRMAÇÃO DE EXCLUSÃO

### 8.1 Intenção
Evitar exclusões acidentais.

### 8.2 Regras

- Sempre exigir confirmação explícita
- Informar consequências
- Bloquear se houver dependências

---

## 9. NOTIFICAÇÕES

### 9.1 Tipos Padronizados

| Tipo | Uso |
|----|----|
| Sucesso | Operação concluída |
| Erro | Falha bloqueante |
| Aviso | Atenção necessária |
| Info | Feedback neutro |

---

## 10. RESPONSIVIDADE (OBRIGATÓRIO)

| Contexto | Comportamento |
|-------|---------------|
| Mobile | Layout em coluna |
| Tablet | Componentes empilháveis |
| Desktop | Layout completo |

---

## 11. ACESSIBILIDADE (OBRIGATÓRIO)

- Navegação por teclado
- Leitura por screen readers
- Contraste mínimo WCAG AA
- Labels e descrições claras

---

## 12. RASTREABILIDADE

| Wireframe | UC | RF |
|---------|----|----|
| WF-01 | UC00 | RFXXX |
| WF-02 | UC01 | RFXXX |
| WF-03 | UC03 | RFXXX |
| WF-04 | UC02 | RFXXX |
| WF-05 | UC04 | RFXXX |

---

## 13. NÃO-OBJETIVOS (OUT OF SCOPE)

- Estilo visual final
- Escolha de framework
- Design gráfico definitivo
- Animações avançadas

---

## 14. HISTÓRICO DE ALTERAÇÕES

| Versão | Data | Autor | Descrição |
|------|------|-------|-----------|
| 2.0 | YYYY-MM-DD | Agência ALC - alc.dev.br | Template canônico orientado a contrato |
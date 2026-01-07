# CONTRATO DE GERAÇÃO WF (WIREFRAMES)

**Versão:** 1.0
**Data:** 2025-12-31
**Status:** Ativo

---

## 📋 SUMÁRIO EXECUTIVO

### ⚡ O que este contrato faz

Este contrato gera **documentação completa de Wireframes (WF)** com base nos **Casos de Uso (UC)** já criados, garantindo:

- ✅ **Cobertura Total (100%)**: WF cobre 100% dos UCs
- ✅ **Rastreabilidade Completa**: RF → UC → WF
- ✅ **Design Consistente**: Estados, responsividade e acessibilidade
- ✅ **Sem Criação de Código**: APENAS documentação

### 📁 Arquivos Gerados

1. **WF-RFXXX.md** - Wireframes narrativo (derivado dos UCs) - **OBRIGATÓRIO**
2. **STATUS.yaml** - Atualização de governança

✅ **UC deve estar criado e validado** (pré-requisito)
⚠️ **Commit e push:** Responsabilidade do usuário (não automatizado)

**⚠️ IMPORTANTE:** Apenas WF.md é obrigatório (formato narrativo). NÃO criar WF.yaml.

### 🎯 Princípios Fundamentais

1. **Derivação dos UCs**: WF deriva EXCLUSIVAMENTE dos UCs criados
2. **Cobertura Total**: WF cobre 100% dos UCs
3. **Estados Obrigatórios**: Loading, Vazio, Erro, Dados
4. **Responsividade**: Mobile, Tablet, Desktop
5. **Acessibilidade**: WCAG AA
6. **Sem Código**: Este contrato NÃO cria implementação

### ⚠️ REGRA CRÍTICA

**Se QUALQUER UC não estiver coberto por WF, a execução é considerada FALHADA.**

---

## 1. Identificação do Agente

| Campo | Valor |
|-------|-------|
| **Papel** | Agente Gerador de Wireframes |
| **Escopo** | Criação completa de WF-RFXXX.md |
| **Modo** | Documentação (sem alteração de código) |

---

## 2. Ativação do Contrato

Este contrato é ativado quando a solicitação mencionar explicitamente:

> **"Conforme CONTRATO-GERACAO-DOCS-WF para RFXXX"**

Exemplo:
```
Conforme CONTRATO-GERACAO-DOCS-WF para RF060.
Seguir D:\IC2\CLAUDE.md.
```

---

## 3. Objetivo do Contrato

Gerar **1 arquivo fundamental** que complementa os Casos de Uso (UC) com **wireframes**:

1. **WF-RFXXX.md** - Wireframes (contrato visual)

Além disso, atualizar:

2. **STATUS.yaml** - Controle de governança e progresso do RF

### 3.1 Princípio da Cobertura Total (100%)

**REGRA CRÍTICA:** Os WFs DEVEM cobrir **100% ABSOLUTO** dos UCs.

- ✅ TODO UC DEVE estar representado em pelo menos um WF
- ✅ Nenhum WF pode introduzir telas NÃO previstas nos UCs
- ✅ Telas fora de escopo nos UCs NÃO geram WFs

**Se houver dúvida sobre alguma tela:**
- ❌ NÃO assumir que pode ser ignorada
- ❌ NÃO deixar de documentar
- ✅ Criar WF correspondente ao UC

### 3.2 Estados Obrigatórios

**REGRA CRÍTICA:** Cada WF DEVE documentar TODOS os estados da tela.

Estados obrigatórios:
- ✅ **Loading**: Enquanto carrega dados
- ✅ **Vazio**: Quando não há dados
- ✅ **Erro**: Quando falha ao carregar
- ✅ **Dados**: Quando há dados exibidos

**IMPORTANTE:** Este contrato NÃO inclui commit/push. O usuário é responsável por commitar os arquivos gerados.

---

## 4. Configuração de Ambiente

### 4.1 Paths do Projeto

| Variável | Caminho |
|----------|---------|
| **PROJECT_ROOT** | `D:\IC2\` |
| **RF_BASE_PATH** | ` D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\` |
| **TEMPLATES_PATH** | `D:\IC2\docs\templates\` |

### 4.2 Permissões de Escrita

O agente PODE escrever **APENAS** em:
```
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\WF-RFXXX.md
 D:\IC2\documentacao\Fase-*\EPIC*\RFXXX\STATUS.yaml
```

**PROIBIDO** escrever em:
- `D:\IC2\backend\**`
- `D:\IC2\frontend\**`
- `contracts/**`
- `templates/**`
- Qualquer arquivo que não seja os 2 listados acima

---

## 5. Pré-requisitos (BLOQUEANTES)

O contrato TRAVA se qualquer condição falhar:

| Pré-requisito | Descrição | Bloqueante |
|---------------|-----------|------------|
| Pasta do RF | Pasta já criada em `rf/[Fase]/[EPIC]/RFXXX/` | Sim |
| UC-RFXXX.md | UC criado e completo | Sim |
| UC-RFXXX.yaml | UC estruturado e sincronizado | Sim |
| Template WF.md | Template WF.md disponível | Sim |
| STATUS.yaml | Arquivo presente na pasta do RF | Sim |
| UC Validado | STATUS.yaml com `documentacao.uc = true` | Sim |

**PARAR se qualquer item falhar.**

---

## 6. Workflow Obrigatório de Geração

### Fase 1: Leitura dos UCs (OBRIGATÓRIA)

Antes de criar qualquer wireframe, o agente DEVE:

#### 1.1 Ler UC-RFXXX.md Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\UC-RFXXX.md`
- Entender TODOS os casos de uso
- Identificar TODAS as telas necessárias
- Mapear fluxos principais, alternativos e de exceção

#### 1.2 Ler UC-RFXXX.yaml Completamente
- Localização: ` D:\IC2\documentacao\[Fase]\[EPIC]\RFXXX\UC-RFXXX.yaml`
- Extrair ações permitidas por UC
- Mapear estados esperados
- Identificar gatilhos e resultados finais

**Critério de completude:**
- ✅ UC.md lido integralmente
- ✅ UC.yaml lido integralmente
- ✅ Telas necessárias mapeadas
- ✅ Fluxos identificados

---

### Fase 2: Criação WF-RFXXX.md (Wireframes)

#### 2.1 Criar WF-RFXXX.md

**Baseado em:** `D:\IC2\docs\templates\WF.md`

**Estrutura obrigatória:**

1. **Seção 1: Objetivo do Documento**
   - Propósito dos wireframes
   - Referência ao RF e UC

2. **Seção 2: Princípios de Design**
   - Princípios gerais (clareza, feedback, estados explícitos)
   - Padrões globais

3. **Seção 3: Mapa de Telas**
   - Tabela com todas as telas (ID, Tela, UCs Relacionados, Finalidade)

4. **Seções 4+: Wireframes Detalhados**
   - WF-01: Listagem (UC00)
   - WF-02: Criação (UC01)
   - WF-03: Edição (UC03)
   - WF-04: Visualização (UC02)
   - WF-05: Confirmação de Exclusão (UC04)

**Cada Wireframe DEVE conter:**
- **Intenção da Tela:** Propósito
- **Ações Permitidas:** Lista de ações do usuário
- **Estados Obrigatórios:** Loading, Vazio, Erro, Dados
- **Contratos de Comportamento:** Regras visuais e funcionais

**Estrutura de Estado Obrigatória:**

```markdown
## WF-01: Listagem de [Entidade] (UC00)

### 1. Intenção da Tela
Permitir ao usuário visualizar todos os registros de [Entidade] do seu tenant.

### 2. Ações Permitidas
- Visualizar lista de [entidade]s
- Filtrar por status/nome
- Ordenar por colunas
- Criar novo [entidade] (se tiver permissão)
- Editar [entidade] (se tiver permissão)
- Excluir [entidade] (se tiver permissão)

### 3. Estados Obrigatórios

#### Estado 1: Loading (Carregando)
**Quando:** Sistema está buscando dados
**Exibir:**
- Skeleton loader (tabela)
- Mensagem: "Carregando [entidade]s..."

#### Estado 2: Vazio (Sem Dados)
**Quando:** Não há registros no tenant
**Exibir:**
- Ícone ilustrativo
- Mensagem: "Nenhum(a) [entidade] cadastrado(a)"
- Botão "Criar [Entidade]" (se tiver permissão)

#### Estado 3: Erro (Falha ao Carregar)
**Quando:** API retorna erro (500, 403, etc.)
**Exibir:**
- Ícone de erro
- Mensagem: "Erro ao carregar [entidade]s. Tente novamente."
- Botão "Recarregar"

#### Estado 4: Dados (Lista Exibida)
**Quando:** Há registros disponíveis
**Exibir:**
- Tabela com colunas: [listar colunas]
- Ações por linha: Visualizar, Editar, Excluir
- Paginação (se > 10 registros)
- Filtros e busca

### 4. Contratos de Comportamento

#### Responsividade
- **Mobile:** Lista empilhada (cards)
- **Tablet:** Tabela simplificada (4 colunas)
- **Desktop:** Tabela completa (todas colunas)

#### Acessibilidade (WCAG AA)
- Labels em português claro
- Botões com aria-label
- Navegação por teclado (Tab, Enter, Esc)
- Contraste mínimo 4.5:1

#### Feedback ao Usuário
- Loading spinner durante requisições
- Toast de sucesso/erro após ações
- Confirmação antes de exclusão
```

**OBRIGATÓRIO em WF-RFXXX.md:**
- ✅ Cobertura de 100% dos UCs
- ✅ Estados obrigatórios (Loading, Vazio, Erro, Dados) em TODOS os WFs
- ✅ Responsividade (Mobile, Tablet, Desktop)
- ✅ Acessibilidade (WCAG AA)
- ✅ Ações permitidas mapeadas dos UCs

**PROIBIDO em WF-RFXXX.md:**
- ❌ Criar telas não previstas nos UCs
- ❌ Omitir estados obrigatórios
- ❌ Ignorar responsividade ou acessibilidade

---

### Fase 3: Validação Estrutural

**⚠️ IMPORTANTE:** WF NÃO possui validador automático de código (como `validator-rf-uc.py` no UC).

A validação de WF é **estrutural**, realizada via **checklist** ([wf.yaml](../../../checklists/documentacao/geracao/wf.yaml)):

- ✅ Cobertura de 100% dos UCs
- ✅ Estados obrigatórios (Loading, Vazio, Erro, Dados) presentes
- ✅ Responsividade documentada (Mobile, Tablet, Desktop)
- ✅ Acessibilidade WCAG AA aplicada

A validação é **manual/estrutural**, não automatizada.

---

### Fase 4: Atualização STATUS.yaml

#### 4.1 Atualizar STATUS.yaml

**Baseado em:** `D:\IC2\docs\templates\STATUS.yaml`

**Campos a atualizar:**

```yaml
documentacao:
  wf: true           # WF-RFXXX.md criado
```

**REGRA CRÍTICA:** Só marcar como `true` após criação completa do WF e validação estrutural via checklist.

---

### Fase 5: Finalização

Após atualizar STATUS.yaml, a geração de WFs está concluída.

**Arquivos gerados:**
- WF-RFXXX.md
- STATUS.yaml (atualizado)

⚠️ **IMPORTANTE:** Commit e push são responsabilidade do usuário. O agente NÃO deve realizar essas operações.

---

## 7. Regras de Qualidade (OBRIGATÓRIAS)

### 7.1 WF deve cobrir 100% dos UCs

**OBRIGATÓRIO em WF-RFXXX.md:**
- ✅ Cobertura de 100% dos UCs
- ✅ Estados obrigatórios (Loading, Vazio, Erro, Dados) em TODOS os wireframes
- ✅ Responsividade (Mobile, Tablet, Desktop)
- ✅ Acessibilidade (WCAG AA)
- ✅ Ações permitidas mapeadas dos UCs

**PROIBIDO em WF-RFXXX.md:**
- ❌ Criar telas não previstas nos UCs
- ❌ Omitir estados obrigatórios
- ❌ Ignorar responsividade ou acessibilidade

### 7.2 Coerência Estrutural Obrigatória

**Coerência UC → WF:**
- Todo UC deve ter WF correspondente
- Todo WF deve derivar de UC existente
- Ações permitidas devem estar nos UCs

---

## 8. Bloqueios de Execução

O agente DEVE PARAR se:

1. **UC-RFXXX.md não existe**: UCs não foram criados
2. **UC-RFXXX.yaml não existe**: UCs estruturados não disponíveis
3. **Cobertura incompleta**: WF não cobre 100% dos UCs
4. **Estados faltando**: Algum WF não tem todos os 4 estados obrigatórios

---

## 9. Critério de Pronto

O contrato só é considerado CONCLUÍDO quando:

### 9.1 Checklist de Arquivos Gerados

- [ ] WF-RFXXX.md criado (wireframes cobrindo 100% dos UCs)
- [ ] STATUS.yaml atualizado

### 9.2 Checklist de Qualidade Final

- [ ] **Cobertura:** WF cobre 100% dos UCs
- [ ] **Estados:** Todos os WFs têm Loading, Vazio, Erro, Dados
- [ ] **Responsividade:** Mobile, Tablet, Desktop documentados
- [ ] **Acessibilidade:** WCAG AA aplicado
- [ ] **Rastreabilidade:** UC → WF completa
- [ ] **Arquivos prontos** (2 arquivos gerados: WF.md, STATUS.yaml)

**REGRA DE BLOQUEIO:** Se QUALQUER item desta lista estiver incompleto, a execução DEVE ser considerada FALHADA.

---

## 10. Próximo Contrato

Após conclusão deste contrato, o próximo passo é:

> **CONTRATO-GERACAO-DOCS-MD** (para criar MD)
>
> ```
> Conforme CONTRATO-GERACAO-DOCS-MD para RFXXX.
> Seguir D:\IC2\CLAUDE.md.
> ```

Este contrato gerará o arquivo MD-RFXXX.yaml (Modelo de Dados).

---

## 11. Arquivos Relacionados

| Arquivo | Descrição |
|---------|-----------|
| `contracts/documentacao/execucao/wf-criacao.md` | Este contrato |
| `checklists/documentacao/geracao/wf.yaml` | Checklist YAML |
| `templates/WF.yaml` | Template do WF |
| `templates/STATUS.yaml` | Template STATUS estruturado |

---

## 12. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-31 | Criação do contrato separado (WF apenas) |

---

## 13. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- não estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTÃO:

- A execução DEVE ser NEGADA
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

---

**FIM DO CONTRATO**

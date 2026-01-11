# D:\IC2\CLAUDE.md
# Contrato de Governança de Documentação

**Versão:** 4.1
**Data:** 2026-01-09
**Status:** Vigente

Este arquivo define **COMO** o Claude Code deve se comportar ao trabalhar com **documentação** neste repositório.
Ele é um **contrato de governança**, não documentação técnica.

O D:\IC2\CLAUDE.md funciona como a **camada de governança superior** para documentação.
Contratos específicos complementam este arquivo e **NUNCA o substituem**.

---

**ATENÇÃO:**

Aqui D:\IC2_Governanca\ é onde fica nossa estrutura de governança por contratos e os documentos do sistema. Se você estiver rodando a partir dessa pasta raiz nunca altere o branch.

Aqui D:\IC2\ é onde fica nossa estrutura de código. Quando estivermos falando em código, deve-se pesquisar nessa estrutura. 

Se você estiver rodando a partir da raiz D:\IC2_Governanca\ nunca altere nada em D:\IC2\.

Se você estiver rodando a partir da raiz D:\IC2\ nunca altere nada em D:\IC2_Governanca\.

---

## 1. Idioma e Comunicação

- **SEMPRE responda em Português do Brasil**
- Utilize linguagem técnica clara, objetiva e formal
- Não use gírias, informalidades ou emojis

---

## 2. Fonte da Verdade (Hierarquia de Documentos)

Este projeto segue **EXCLUSIVAMENTE** os documentos abaixo na ordem hierárquica:

| Nível | Documento | Propósito |
|-------|-----------|-----------|
| **1** | `CLAUDE.md` (este arquivo) | Governança superior de documentação |
| **2** | `COMPLIANCE.md` | Regras de validação e conformidade de documentos |
| **3** | `CONVENTIONS.md` | Nomenclatura e padrões de documentação |
| **4** | `contracts/` | Contratos formais de documentação |
| **5** | `prompts/` | Prompts para ativar contratos |
| **6** | `checklists/` | Checklists de validação de documentação |

**Regra de Conflito:**
➡️ Em caso de conflito, a documentação de nível superior vence.

---

## 3. MODO DE EXECUÇÃO RÍGIDO (OBRIGATÓRIO)

Este projeto opera em **MODO DE GOVERNANÇA RÍGIDA**.

### Regras Fundamentais

- O agente **NÃO** pode negociar escopo
- O agente **NÃO** pode sugerir ações fora do contrato ativo
- O agente **NÃO** pode executar tarefas não explicitamente solicitadas
- O agente **NÃO** pode "ajudar" fora do contrato
- O agente **NÃO** pode perguntar "se pode" fazer algo fora do contrato

### Se Solicitação Estiver Fora do Contrato

- O agente **DEVE NEGAR**
- O agente **DEVE** explicar o motivo
- O agente **DEVE** solicitar ajuste formal de contrato

**Qualquer tentativa de execução fora do contrato invalida a tarefa.**

➡️ **Ver detalhes completos em:** `COMPLIANCE.md` (seção 17)

---

## 4. REGRA DE NEGAÇÃO ZERO

Se uma solicitação:
- Não estiver explicitamente prevista no contrato ativo, **OU**
- Conflitar com qualquer regra do contrato

**ENTÃO:**
- A execução **DEVE** ser **NEGADA**
- Nenhuma ação parcial pode ser realizada
- Nenhum "adiantamento" é permitido

➡️ **Ver detalhes completos em:** `COMPLIANCE.md` (seção 15)

---

## 5. REGRA OBRIGATÓRIA — Arquivos Temporários da IA

**PROIBIDO criar arquivos na raiz do projeto (`D:\IC2_Governanca\`) sem solicitação explícita do usuário.**

### Regra

Qualquer arquivo criado pela IA que **NÃO** seja documentação oficial solicitada explicitamente **DEVE** ser criado em:

```
D:\IC2\.temp_ia\
```

### Exceções Permitidas (fora de `.temp_ia\`)

- Relatórios de auditoria em `D:\IC2\relatorios\`
- Documentação oficial de governança em `D:\IC2_Governanca\`
- Documentação de contratos em `D:\IC2_Governanca\contracts\`
- Documentação de prompts em `D:\IC2_Governanca\prompts\`
- Documentação de checklists em `D:\IC2_Governanca\checklists\`

### Exemplos

**✅ CORRETO:**
```
D:\IC2\.temp_ia\RELATORIO-ANALISE-DOC.md
D:\IC2\.temp_ia\analise-gap-documentacao.md
D:\IC2\.temp_ia\validacao-temporaria.md
```

**❌ INCORRETO:**
```
D:\IC2_Governanca\RELATORIO-ANALISE-DOC.md          # ❌ NA RAIZ (proibido)
D:\IC2\analise-gap-documentacao.md                   # ❌ NA RAIZ (proibido)
```

**VIOLAÇÃO:** Criar arquivos fora de `.temp_ia\` sem solicitação explícita é considerado **execução inválida**.

➡️ **Ver detalhes completos em:** `COMPLIANCE.md` (seção 16)

---

## 6. Hierarquia de Governança de Documentação

```
CLAUDE.md (este arquivo)
    ↓
COMPLIANCE.md (regras de validação de documentos)
    ↓
contracts/ (contratos de documentação)
    ↓
prompts/ (prompts para ativar contratos)
    ↓
checklists/ (checklists de validação)
```

---

## 7. Sistema de Contratos de Documentação

### Estrutura de Contratos

Os contratos estão organizados por categoria em `contracts/`:

```
contracts/
├── documentacao/        ← Geração e validação de documentação
├── auditoria/           ← Auditoria de conformidade documental
├── fluxos/              ← Documentação de fluxos
└── deprecated/          ← Contratos obsoletos (não usar)
```

➡️ **Ver estrutura completa em:** `contracts/README.md`

### Regras de Ativação

- Um contrato **só é aplicado** se for **explicitamente citado** no prompt
- Contratos **não se misturam**
- Se houver conflito entre contratos, o **mais restritivo** prevalece

---

## 8. Ativação de Contratos (Tabela de Referência Rápida)

| Prompt | Contrato Ativado | Caminho Completo |
|--------|------------------|------------------|
| "Conforme CONTRATO DE DOCUMENTAÇÃO ESSENCIAL" | Documentação Essencial | `contracts/documentacao/CONTRATO-DE-ADEQUACAO-DE-DOCUMENTOS.md` |
| "Conforme CONTRATO DE AUDITORIA" | Auditoria de Conformidade | `contracts/auditoria/conformidade.md` |

➡️ **Ver lista completa de contratos em:** `contracts/README.md`

---

## 9. AUTO-VALIDAÇÃO OBRIGATÓRIA DO AGENTE

Sempre que o agente criar ou modificar qualquer um dos arquivos de documentação:
- `RFXXX.yaml`
- `UC-RFXXX.yaml`
- `TC-RFXXX.yaml`
- `CN-RFXXX.yaml`
- `MD-RFXXX.yaml`
- Arquivos `.md` em `D:\IC2_Governanca\`

O agente **DEVE, OBRIGATORIAMENTE**:

1. Verificar conformidade com os templates estabelecidos
2. Validar estrutura obrigatória dos documentos
3. Verificar referências cruzadas (RF → UC → TC → CN)
4. Garantir integridade das seções obrigatórias

### Proibições

É **PROIBIDO**:
- Criar documentação sem seguir templates
- Modificar estrutura de documentos sem autorização
- Criar seções fora do padrão estabelecido
- Omitir seções obrigatórias

➡️ **Ver detalhes completos em:** `COMPLIANCE.md` (seção 3)

---

## 10. COMANDOS DE VALIDAÇÃO DE DOCUMENTAÇÃO

### Comandos Principais

| Categoria | Comando | Descrição |
|-----------|---------|-----------|
| **Validação** | `python tools/docs/validator-rf-uc.py RFXXX` | Validar RF → UC |
| **Validação** | `python tools/docs/validator-coverage.py RFXXX` | Validar cobertura completa |
| **Auditoria** | `/audit-rf RFXXX` | Auditoria de conformidade documental |

➡️ **Ver todos os comandos em:** `COMMANDS.md`

---

## 11. REGRAS DE CONFORMIDADE DOCUMENTAL (Resumo)

### Obrigações Principais

| Regra | Descrição | Referência |
|-------|-----------|------------|
| **Separação RF / RL** | RF e RL devem estar separados | `COMPLIANCE.md` seção 1 |
| **User Stories** | Obrigatórias para todo RF | `COMPLIANCE.md` seção 2 |
| **Templates** | Seguir templates estabelecidos | `COMPLIANCE.md` seção 4 |
| **Seções Obrigatórias** | RF deve ter 5 seções | `COMPLIANCE.md` seção 10 |
| **Referências Cruzadas** | RF → UC → TC → CN | `COMPLIANCE.md` seção 11 |

➡️ **Ver todas as regras em:** `COMPLIANCE.md`

---

## 12. Escopo de Responsabilidade do Agente

### Você É Responsável Por

- ✅ Criar documentação conforme templates
- ✅ Aplicar padrões estabelecidos
- ✅ Validar conformidade documental
- ✅ Seguir contratos ativados
- ✅ Manter integridade das referências

### Você NÃO É Responsável Por

- ❌ Criar novos templates
- ❌ Definir novos padrões
- ❌ Criar contratos
- ❌ Alterar estrutura de governança
- ❌ Executar tarefas fora do contrato

**Seu papel é EXCLUSIVAMENTE criação e validação de documentação.**

---

## 13. Consciência de Decisões (DECISIONS.md)

Durante a criação de documentação, você deve identificar **decisões estruturais implícitas**.

Você **DEVE PARAR e ALERTAR** quando ocorrer:
- Necessidade de criar nova seção não prevista
- Desvio de template estabelecido
- Conflito entre regras de documentação
- Decisões sobre estrutura documental
- Ambiguidade em requisitos

**Nesses casos:**
- **NÃO** prossiga silenciosamente
- Informe a decisão estrutural
- Sugira ajuste formal
- Aguarde confirmação

---

## 14. Antes de Qualquer Criação de Documentação

Antes de criar qualquer documento, você **DEVE**:

1. Ler o template aplicável em `templates/`
2. Ler `CONVENTIONS.md` (nomenclatura)
3. Ler `COMPLIANCE.md` (regras aplicáveis)
4. Confirmar entendimento das regras
5. Identificar se há **contrato específico ativado**
6. Somente então iniciar a criação

**Se algo estiver ambíguo, inconsistente ou inviável:**
➡️ **PARE e AVISE antes de continuar.**

---

## 15. Regras Invioláveis

Você **NUNCA** deve:

1. Criar documentos fora dos templates estabelecidos
2. Modificar estrutura de governança sem autorização
3. Inferir regras não documentadas
4. "Melhorar" templates silenciosamente
5. Alterar arquivos em `D:\IC2_Governanca\` sem solicitação explícita
6. Criar documentação sem validação
7. Omitir seções obrigatórias
8. Criar arquivos fora de `.temp_ia/` sem solicitação
9. Negociar escopo fora do contrato
10. Prosseguir com decisões ambíguas sem avisar

---

## 16. Regra Final

**Contratos:**
- Definem limites claros
- Não são negociáveis
- Não são interpretáveis

**Se algo violar um contrato:**
➡️ **PARE. AVISE. AGUARDE.**

Este comportamento é **obrigatório**.

---

## 17. Documentação de Referência Completa

| Documento | Propósito | Quando Consultar |
|-----------|-----------|------------------|
| **COMPLIANCE.md** | Regras de validação e conformidade | Antes de toda execução |
| **CONVENTIONS.md** | Nomenclatura, padrões de documentação | Durante criação de documentos |
| **contracts/README.md** | Lista completa de contratos | Para ativar contrato específico |
| **templates/** | Templates de documentação | Antes de criar documentos |
| **tools/README.md** | Ferramentas de validação | Para executar validadores |

---

## 18. ALINHAMENTO OBRIGATÓRIO COM TESTES (NOVO)

**Versão:** 1.0
**Data:** 2026-01-09
**Contexto:** Criado após análise do RF006 onde desalinhamento resultou em 12 execuções e apenas 74% E2E

### 18.1. Regra Fundamental

**Documentação e código DEVEM considerar testes desde o início.**

Este não é um princípio aspiracional. É uma **regra obrigatória** com **bloqueios automáticos**.

---

### 18.2. Princípios Test-First Documentation

#### 18.2.1. Test-First Documentation

- **RF** já identifica elementos testáveis (botões, campos, estados)
- **UC** já especifica data-test attributes, URLs, timeouts, estados UI
- **TC** já especifica seletores E2E e código Playwright
- **MT** já está sincronizado com backend seeds, frontend routing e UC

**Problema que resolve:**
- RF006 Problema 1/6: Credenciais MT desatualizadas → 100% falhas E2E
- RF006 Problema 2/6: URLs não documentadas → 32 falhas E2E por 404
- RF006 Problema 3/6: Data-test não especificados → 32 falhas E2E por seletores ausentes
- RF006 Problema 4/6: Estados UI não documentados → Validações incompletas
- RF006 Problema 5/6: Timeouts não especificados → 15 falhas E2E por timeout

---

#### 18.2.2. Bloqueios Obrigatórios

**REGRA INVIOLÁVEL:** Sem alinhamento = BLOQUEIO automático

| Bloqueio | Condição | Ação |
|----------|----------|------|
| **UC sem especificações de teste** | UC não possui: navegacao, credenciais, data-test, estados_ui, timeouts | ❌ BLOQUEIO: Não prosseguir para WF/MD/Backend/Frontend |
| **Backend sem testes unitários** | Commands/Queries sem testes ou taxa < 100% | ❌ BLOQUEIO: Não marcar como concluído |
| **Frontend sem data-test** | Auditoria `npm run audit-data-test RFXXX` retorna exit code 1 | ❌ BLOQUEIO: Não marcar como concluído |
| **MT desatualizada** | Validações de sincronização falharam | ❌ BLOQUEIO: Não executar testes E2E |

**Consequência de violar bloqueio:**
- Execução é **INVALIDADA**
- Status.yaml é marcado como **REPROVADO**
- Necessária correção completa antes de prosseguir

---

#### 18.2.3. Validação Automática

**Scripts obrigatórios ANTES de executar testes E2E:**

```bash
# Validar credenciais MT vs backend seeds
npm run validate-credentials RFXXX
# Exit code 0: PASS | Exit code 1: FAIL (credenciais desatualizadas)

# Validar URLs MT vs frontend routing
npm run validate-routes
# Exit code 0: PASS | Exit code 1: FAIL (URLs 404)

# Validar data-test MT vs UC
npm run audit-data-test RFXXX
# Exit code 0: PASS | Exit code 1: FAIL (seletores ausentes/inconsistentes)

# Validar timeouts MT vs UC (se script existir)
python tools/validate-timeouts.py RFXXX
# Exit code 0: PASS | Exit code 1: FAIL (timeouts divergentes)

# Validar especificações de teste em UC (se script existir)
python tools/validate-uc-test-specs.py RFXXX
# Exit code 0: PASS | Exit code 1: FAIL (UC incompleto)
```

**SE qualquer validação FALHAR:**
- ❌ Testes E2E **NÃO podem** ser executados
- ❌ Corrigir gaps e re-executar validações
- ❌ Somente prosseguir quando **TODOS** retornarem exit code 0

**Referência:** Checklist pré-execução de testes (seção sincronizacao_mt)

---

### 18.3. Critério de Sucesso

**Taxa inicial E2E: ≥ 80%**

Se primeira execução E2E < 80%:
- ❌ Alinhamento FALHOU
- ❌ RETORNAR à documentação (UC/TC/MT) ou implementação (Backend/Frontend)
- ❌ Corrigir gaps e re-executar até ≥ 80%

**Baseline (RF006):**
- Taxa inicial: 0%
- Execuções necessárias: 12
- Tempo desperdiçado: ~10 horas

**Meta (com alinhamento):**
- Taxa inicial: 80-90%
- Execuções necessárias: 2-3
- Tempo economizado: ~8 horas por RF

**ROI:**
- Investimento: 90 horas (atualização governança - 7 sprints)
- Break-even: 10-12 RFs (~3-4 sprints)
- Economia anual: ~120-160 horas (estimativa 20 RFs/ano)

---

### 18.4. Rastreabilidade Completa

**Cadeia obrigatória:** RF → UC → TC → MT → Backend → Frontend → E2E

```
RF-RFXXX.yaml
    ↓ (identifica elementos testáveis)
UC-RFXXX.yaml
    ↓ (especifica data-test, URLs, timeouts, estados UI)
TC-RFXXX.yaml
    ↓ (especifica seletores E2E, código Playwright)
MT-RFXXX.data.ts
    ↓ (sincroniza credenciais, URLs, data-test, timeouts)
Backend (Commands/Queries)
    ↓ (testes unitários 100%)
Frontend (Components)
    ↓ (data-test attributes 100%)
Testes E2E
    ↓ (taxa inicial ≥ 80%)
```

**Quebra de rastreabilidade = BLOQUEIO**

---

### 18.5. Responsabilidades por Fase

#### FASE DOCUMENTAÇÃO

**Agente de RF (rf-criacao.md):**
- ✅ Identificar elementos testáveis (botões, campos, tabelas)
- ✅ Documentar nomenclatura esperada de data-test
- ✅ Identificar URLs de navegação
- ✅ Identificar timeouts esperados

**Agente de UC (uc-criacao.md):**
- ✅ Criar seções obrigatórias: navegacao, credenciais, estados_ui, performance, timeouts_e2e
- ✅ Especificar data-test para TODOS os passos interativos
- ✅ Documentar estados UI (loading, vazio, erro)
- ✅ BLOQUEIO: UC incompleto = não prosseguir

**Agente de TC (tc-criacao.md):**
- ✅ Especificar seletores E2E para TODOS os passos
- ✅ Especificar código Playwright (acao_e2e)
- ✅ Validar sincronização com UC
- ✅ BLOQUEIO: Seletores ausentes = não aprovar TC

**Agente de MT (mt-criacao.md):**
- ✅ Sincronizar credenciais com backend seeds
- ✅ Sincronizar URLs com frontend routing
- ✅ Sincronizar data-test com UC
- ✅ Sincronizar timeouts com UC
- ✅ BLOQUEIO: Validações falharam = não aprovar MT

---

#### FASE DESENVOLVIMENTO

**Agente de Backend (backend-criacao.md):**
- ✅ Criar testes unitários para TODOS os Commands/Queries
- ✅ Executar testes: `dotnet test` → Taxa 100%
- ✅ BLOQUEIO: Cobertura < 100% = não marcar como concluído

**Agente de Frontend (frontend-criacao.md):**
- ✅ Implementar data-test attributes conforme UC
- ✅ Executar auditoria: `npm run audit-data-test RFXXX` → Exit code 0
- ✅ BLOQUEIO: Auditoria FAIL = não marcar como concluído

---

#### FASE TESTES

**Agente de Testes (execucao-completa.md):**
- ✅ Executar checklist pré-execução (sincronizacao_mt)
- ✅ Validar TODAS as sincronizações (exit code 0)
- ✅ Executar testes E2E
- ✅ Validar taxa inicial ≥ 80%
- ✅ BLOQUEIO: Taxa < 80% = RETORNAR à documentação/implementação

---

### 18.6. Exceções

**Nenhuma. Esta é uma regra INVIOLÁVEL.**

Não existem exceções para:
- "RF simples demais para precisar de testes"
- "Só um botão, não precisa data-test"
- "Vamos adicionar testes depois"
- "Credenciais são as mesmas, não precisa validar"

**TODO RF, independente de tamanho ou complexidade, DEVE seguir alinhamento obrigatório.**

---

### 18.7. Documentação de Apoio

| Documento | Propósito |
|-----------|-----------|
| `checklists/testes/CHECKLIST-IMPLEMENTACAO-E2E.md` | Checklist completo 3 fases (pré, durante, pós) |
| `processos/SINCRONIZACAO-MT-SEEDS.md` | Processo detalhado de sincronização MT |
| `checklists/documentacao/geracao/uc.yaml` | Checklist com seção especificacoes_teste |
| `checklists/documentacao/geracao/tc.yaml` | Checklist com seção seletores_e2e |
| `checklists/desenvolvimento/validacao/frontend.yaml` | Checklist com seção data_test_attributes |
| `checklists/testes/pre-execucao.yaml` | Checklist com seção sincronizacao_mt |

---

### 18.8. Versão e Histórico

**v1.0 (2026-01-09):**
- Criação da seção após análise do RF006
- Definição de bloqueios obrigatórios
- Critério de sucesso: taxa inicial E2E ≥ 80%
- Rastreabilidade completa: RF → UC → TC → MT → Código → Testes
- Scripts de validação automática
- Processo de sincronização MT documentado

---

## Changelog

### v4.1 (2026-01-09)
- **Adicionada seção 18: ALINHAMENTO OBRIGATÓRIO COM TESTES**
- Criado após análise do RF006 (12 execuções, 74% E2E, 5/6 problemas evitáveis)
- Regra fundamental: Documentação e código DEVEM considerar testes desde o início
- Bloqueios obrigatórios: UC incompleto, Backend sem testes, Frontend sem data-test, MT desatualizada
- Scripts de validação automática: validate-credentials, validate-routes, audit-data-test
- Critério de sucesso: Taxa inicial E2E ≥ 80%
- Rastreabilidade completa: RF → UC → TC → MT → Backend → Frontend → E2E
- Responsabilidades por fase (Documentação, Desenvolvimento, Testes)
- Documentação de apoio: 6 checklists atualizados + 2 processos novos

### v4.0 (2026-01-04)
- **Foco exclusivo em governança de documentação**
- Remoção de todas as seções relacionadas a codificação
- Remoção de referências a build, deploy, testes de código
- Remoção de referências a backend/frontend
- Foco em validação, criação e auditoria de documentos
- Mantida hierarquia de governança
- Mantidas regras de contratos e validação

### v3.0 (2026-01-01)
- Redistribuição cirúrgica: Redução de 2456 → ~350 linhas (85%)
- Versão com foco misto (código + documentação)

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-09
**Versão:** 4.1 - Governança de Documentação

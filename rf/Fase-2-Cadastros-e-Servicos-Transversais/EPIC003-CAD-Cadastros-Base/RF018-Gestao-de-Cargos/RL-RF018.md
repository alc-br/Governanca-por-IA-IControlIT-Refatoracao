# RL-RF018 — Referência ao Legado - Gestão de Cargos

**Versão:** 1.0
**Data:** 2025-12-30
**Autor:** Agência ALC - alc.dev.br

**RF Moderno Relacionado:** RF-018
**Sistema Legado:** VB.NET + ASP.NET Web Forms
**Objetivo:** Documentar o comportamento do legado que serve de base para a refatoração, garantindo rastreabilidade, entendimento histórico e mitigação de riscos.

---

## 1. CONTEXTO DO LEGADO

Descreve o cenário geral do sistema legado.

- **Arquitetura:** Monolítica WebForms
- **Linguagem / Stack:** VB.NET + ASP.NET Web Forms + SQL Server
- **Banco de Dados:** SQL Server (tabelas `Cargo`, `Rl_Cargo_Competencia`)
- **Multi-tenant:** Não (campo `Id_Conglomerado` ausente)
- **Auditoria:** Parcial (apenas criação e última atualização)
- **Configurações:** Web.config, stored procedures no banco

---

## 2. TELAS DO LEGADO

### Tela: TelaCargos.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\TelaCargos.aspx`
- **Responsabilidade:** CRUD básico de cargos (Create, Read, Update, Delete)

#### Campos

| Campo | Tipo | Obrigatório | Observações |
|------|------|-------------|-------------|
| `Cd_Cargo` | TextBox | Sim | Código único, 20 caracteres, sem validação de formato |
| `Nm_Cargo` | TextBox | Sim | Nome do cargo, 150 caracteres |
| `Ds_Cargo` | TextArea | Não | Descrição livre, 500 caracteres |
| `Id_Cargo_Superior` | DropDownList | Não | Supervisor, sem validação de ciclo |
| `Vl_Alcada` | TextBox | Não | Valor numérico, sem validação de alçada crescente |
| `Fl_Ativo` | CheckBox | Sim | Ativo/Inativo |

#### Comportamentos Implícitos

- **Código duplicado:** Sistema permite salvar código duplicado (bug conhecido)
- **Ciclo em hierarquia:** Não valida ciclo ao atribuir supervisor
- **Alçada inconsistente:** Permite subordinado com alçada maior que supervisor
- **Deleção física:** Delete remove registro do banco (não é soft delete)

---

### Tela: TelaCargos_Editar.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\TelaCargos_Editar.aspx`
- **Responsabilidade:** Formulário de edição de cargo existente

#### Comportamentos Implícitos

- **Validação fraca:** Aceita código vazio se não for alterado
- **Sem auditoria antes/depois:** Não registra valores antigos
- **Permite editar código:** Código pode ser alterado após criação (risco de quebra de integridade)

---

### Tela: TelaCargos_Hierarquia.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\TelaCargos_Hierarquia.aspx`
- **Responsabilidade:** Visualização de árvore organizacional

#### Comportamentos Implícitos

- **Árvore lenta:** Stored procedure recursiva sem otimização (timeout em hierarquias grandes)
- **Sem limite de profundidade:** Permite hierarquias infinitas
- **Exibição apenas:** Não permite editar hierarquia nesta tela

---

### Tela: TelaCargos_Competencia.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\TelaCargos_Competencia.aspx`
- **Responsabilidade:** Matriz de competências por cargo

#### Comportamentos Implícitos

- **Sem validação de nível:** Aceita nível 0 ou > 5 (inválido)
- **Duplicação permitida:** Permite adicionar mesma competência múltiplas vezes
- **Sem obrigatoriedade:** Não diferencia competências obrigatórias de desejáveis

---

### Tela: TelaCargos_FaixaSalarial.aspx

- **Caminho:** `D:\IC2\ic1_legado\IControlIT\Cadastros\TelaCargos_FaixaSalarial.aspx`
- **Responsabilidade:** Gerenciamento de salários (piso/teto)

#### Comportamentos Implícitos

- **Sem validação de ordem:** Permite Piso > Teto (bug conhecido)
- **Sem salário mínimo legal:** Não valida contra legislação trabalhista
- **Histórico limitado:** Não mantém histórico completo de faixas

---

## 3. WEBSERVICES / MÉTODOS LEGADOS

| Método | Local | Responsabilidade | Observações |
|------|-------|------------------|-------------|
| `ListarCargos()` | `WSCargo.asmx.vb` | Retorna lista de cargos | Sem paginação, retorna todos os registros |
| `ObterCargo(id)` | `WSCargo.asmx.vb` | Retorna cargo por ID | Sem validação de multi-tenancy |
| `InserirCargo(...)` | `WSCargo.asmx.vb` | Cria novo cargo | Não valida código único |
| `AtualizarCargo(...)` | `WSCargo.asmx.vb` | Edita cargo existente | Permite alterar código |
| `DeletarCargo(id)` | `WSCargo.asmx.vb` | Deleta cargo (físico) | Não verifica ocupantes |
| `ObterHierarquia()` | `WSCargo.asmx.vb` | Retorna árvore organizacional | Usa stored procedure `pa_Cargo_Montar_Arvore` |
| `ValidarCiclo(idCargo, idSuperior)` | `WSCargo.asmx.vb` | Valida ciclo | Implementação incompleta (não detecta todos os casos) |
| `SincronizarAD()` | `WSCargo.asmx.vb` | Sincroniza com Active Directory | Sincronização manual, não automática |

---

## 4. TABELAS LEGADAS

| Tabela | Finalidade | Problemas Identificados |
|-------|------------|-------------------------|
| `Cargo` | Armazenamento principal | Falta campo `Id_Conglomerado` (multi-tenancy), constraint de unicidade fraca |
| `Rl_Cargo_Competencia` | Competências por cargo | Permite duplicação, sem FK constraint adequada |
| `Cargo_FaixaSalarial` | Histórico de salários | Tabela não existe (dados em `Cargo.Vl_Salario_Piso` e `Cargo.Vl_Salario_Teto`) |

---

## 5. REGRAS DE NEGÓCIO IMPLÍCITAS NO LEGADO

Liste regras que não estavam documentadas formalmente.

- **RL-RN-001:** Código de cargo deveria ser único, mas sistema não valida adequadamente (permite duplicados)
- **RL-RN-002:** Hierarquia deveria ser acíclica, mas sistema não valida ciclos (permite A→B→C→A)
- **RL-RN-003:** Alçada de supervisor deveria ser >= alçada de subordinado, mas sistema não valida
- **RL-RN-004:** Cargo com ocupantes não deveria ser deletado, mas sistema permite (delete físico)
- **RL-RN-005:** Faixa salarial deveria ter Piso < Teto, mas sistema não valida
- **RL-RN-006:** Competências deveriam ter nível 1-5, mas sistema aceita qualquer valor
- **RL-RN-007:** Auditoria deveria registrar antes/depois, mas sistema só registra criação e última atualização

---

## 6. GAP ANALYSIS (LEGADO x RF MODERNO)

| Item | Legado | RF Moderno | Observação |
|-----|--------|------------|------------|
| **Multi-tenancy** | Não existe | Campo `ClienteId` obrigatório | CRÍTICO: Legado permite acesso cruzado |
| **Soft Delete** | Delete físico | Soft delete com `FlExcluido` | CRÍTICO: Legado perde dados históricos |
| **Validação de código único** | Fraca (permite duplicados) | Forte (constraint UNIQUE + validação) | Corrigido |
| **Validação de ciclo** | Ausente | Graph validation completa | Corrigido |
| **Validação de alçada** | Ausente | Alçada monotônica crescente | Corrigido |
| **Auditoria** | Parcial (apenas criação) | Completa (antes/depois, 7 anos) | Compliance LGPD |
| **Paginação** | Sem paginação | Paginação obrigatória (20/página) | Performance |
| **Faixa salarial histórico** | Não existe | Histórico completo com vigência | Rastreabilidade |
| **Competências obrigatórias** | Não diferencia | Campo `FlObrigatoria` | Controle melhor |
| **Perfil sugerido** | Não existe | Campo `IdPerfilSugerido` | Facilita onboarding |

---

## 7. DECISÕES DE MODERNIZAÇÃO

Explique decisões tomadas durante a refatoração.

### Decisão 1: Multi-tenancy obrigatório

- **Descrição:** Adicionar campo `ClienteId` em todas as tabelas
- **Motivo:** Sistema legado não possui isolamento de dados, risco de acesso cruzado
- **Impacto:** Alto (altera schema, requer migração de dados)

### Decisão 2: Soft Delete obrigatório

- **Descrição:** Substituir delete físico por `FlExcluido = true`
- **Motivo:** Compliance LGPD (retenção de dados por 7 anos), rastreabilidade
- **Impacto:** Médio (altera comportamento de deleção, requer query filter)

### Decisão 3: Validação de ciclo em hierarquia

- **Descrição:** Implementar validação de grafo antes de alterar supervisor
- **Motivo:** Legado permite ciclos (A→B→C→A), causa problemas em relatórios
- **Impacto:** Médio (lógica de validação complexa)

### Decisão 4: Alçada monotônica crescente

- **Descrição:** Supervisor deve ter alçada >= subordinado
- **Motivo:** Evita inconsistência lógica (gerente não pode aprovar o que seu subordinado pode)
- **Impacto:** Médio (validação adicional ao alterar alçada ou hierarquia)

### Decisão 5: Histórico de faixa salarial

- **Descrição:** Criar tabela `FaixaSalarialCargo` com histórico completo
- **Motivo:** Legado não mantém histórico, dificulta análise temporal
- **Impacto:** Baixo (nova tabela, não afeta código existente)

### Decisão 6: Competências obrigatórias vs desejáveis

- **Descrição:** Campo `FlObrigatoria` em `CompetenciaCargo`
- **Motivo:** Diferenciar competências essenciais de desejáveis
- **Impacto:** Baixo (novo campo, melhora controle)

---

## 8. RISCOS DE MIGRAÇÃO

| Risco | Impacto | Mitigação |
|------|---------|-----------|
| **Dados sem `ClienteId`** | Alto | Script de migração para atribuir `ClienteId` baseado em contexto |
| **Registros deletados fisicamente** | Médio | Perda irreversível, aceitar como dado perdido |
| **Códigos duplicados** | Médio | Identificar duplicados, solicitar decisão ao cliente antes de migrar |
| **Ciclos em hierarquia** | Alto | Script de detecção de ciclos, quebrar ciclos manualmente antes de migrar |
| **Alçadas inconsistentes** | Médio | Ajustar alçadas manualmente para respeitar monotonicidade |
| **Competências com nível inválido** | Baixo | Normalizar para 1-5, nível 0 vira 1, nível > 5 vira 5 |
| **Faixas com Piso > Teto** | Médio | Trocar valores (Piso ↔ Teto) automaticamente |

---

## 9. RASTREABILIDADE

| Elemento Legado | Referência RF | Referência UC | Status |
|----------------|---------------|---------------|--------|
| `TelaCargos.aspx` | RN-RF018-001 a RN-RF018-005 | UC01-criar-cargo, UC03-editar-cargo | Migrado |
| `TelaCargos_Hierarquia.aspx` | RN-RF018-003, RN-RF018-004 | UC-hierarquia | Migrado |
| `TelaCargos_Competencia.aspx` | RN-RF018-007 | UC-competencias | Migrado |
| `TelaCargos_FaixaSalarial.aspx` | RN-RF018-008 | UC-faixas | Migrado |
| `pa_Cargo_Listar` | GET /api/v1/cargos | UC00-listar-cargos | Migrado |
| `pa_Cargo_Montar_Arvore` | GET /api/v1/cargos/hierarquia/arvore | UC-hierarquia | Migrado |
| `pa_Cargo_Validar_Ciclo` | Validação inline | RN-RF018-003 | Migrado |
| `WSCargo.asmx.vb` | Endpoints REST API | Todos os UCs | Migrado |
| Tabela `Cargo` | Entidade Cargo | MD-RF018 | Migrado |
| Tabela `Rl_Cargo_Competencia` | Entidade CompetenciaCargo | MD-RF018 | Migrado |

---

## PROBLEMAS CONHECIDOS DO LEGADO

### 1. Código Duplicado (Bug Crítico)

**Descrição:** Sistema permite salvar cargo com código duplicado no mesmo conglomerado.

**Causa:** Constraint UNIQUE ausente, validação de código apenas no frontend (pode ser contornada).

**Impacto:** Relatórios quebram, integrações falham ao buscar por código.

**Solução Moderna:** Constraint UNIQUE (`Codigo`, `ClienteId`) + validação FluentValidation + tratamento HTTP 409.

---

### 2. Ciclo em Hierarquia (Bug Crítico)

**Descrição:** Sistema permite criar ciclo (A→B→C→A) na hierarquia organizacional.

**Causa:** Stored procedure `pa_Cargo_Validar_Ciclo` incompleta, não detecta todos os casos.

**Impacto:** Relatórios de hierarquia entram em loop infinito (timeout), aprovações quebram.

**Solução Moderna:** Validação de grafo com algoritmo DFS (Depth-First Search), rejeita qualquer tentativa de criar ciclo.

---

### 3. Alçada Inconsistente (Bug Grave)

**Descrição:** Subordinado pode ter alçada maior que supervisor.

**Causa:** Sem validação de alçada crescente.

**Impacto:** Lógica de aprovação quebra (subordinado aprova mais que chefe).

**Solução Moderna:** Validação de alçada monotônica crescente ao alterar alçada ou hierarquia.

---

### 4. Delete Físico (Violação LGPD)

**Descrição:** Sistema deleta registros fisicamente do banco.

**Causa:** Comando SQL `DELETE FROM Cargo WHERE Id_Cargo = @Id`.

**Impacto:** Perda irreversível de dados, violação LGPD (retenção 7 anos).

**Solução Moderna:** Soft delete com `FlExcluido = true`, retenção de auditoria 7 anos.

---

### 5. Sem Multi-Tenancy (Segurança Crítica)

**Descrição:** Sistema não possui isolamento de dados por cliente/conglomerado.

**Causa:** Tabela sem campo `Id_Conglomerado`.

**Impacto:** Risco de acesso cruzado (Cliente A vê dados do Cliente B).

**Solução Moderna:** Campo `ClienteId` obrigatório em todas as tabelas + global query filter.

---

## CHANGELOG

| Versão | Data | Descrição | Autor |
|------|------|----------|------|
| 1.0 | 2025-12-30 | Criação do documento de referência ao legado (separação RF/RL) | Agência ALC - alc.dev.br |

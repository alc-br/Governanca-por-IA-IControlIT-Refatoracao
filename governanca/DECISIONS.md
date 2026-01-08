# Registro de Decisoes Tecnicas (ADR)

Este arquivo documenta decisoes arquiteturais e tecnicas do projeto IControlIT 2.0.

Cada decisao segue o formato ADR (Architecture Decision Record).

---

## Template

Para registrar uma nova decisao, copie o template abaixo:

```
### ADR-XXX: [Titulo da Decisao]

**Data:** YYYY-MM-DD
**Status:** Proposta | Aceita | Depreciada | Substituida por ADR-XXX

**Contexto:**
[Descreva o problema ou situacao que motivou a decisao]

**Decisao:**
[Descreva a decisao tomada]

**Alternativas Consideradas:**
- [Alternativa 1]: [Motivo de rejeicao]
- [Alternativa 2]: [Motivo de rejeicao]

**Consequencias:**
- Positivas: [Impactos positivos]
- Negativas: [Impactos negativos ou trade-offs]

**Responsavel:** [Nome ou papel]
```

---

## Decisoes Registradas

### ADR-001: Sistema de Contratos para Governanca de Agentes AI

**Data:** 2024-12-23
**Status:** Aceita

**Contexto:**
O projeto utiliza agentes AI (Claude Code) para desenvolvimento. Era necessario
garantir que o agente atuasse dentro de limites definidos, sem autonomia excessiva.

**Decisao:**
Implementar sistema de contratos formais que definem:
- Escopo permitido por tipo de atividade
- Proibicoes explicitas
- Checklists obrigatorios
- Transicoes validas entre contratos

**Alternativas Consideradas:**
- Prompts longos: Dificil manter consistencia
- Regras informais: Sem rastreabilidade

**Consequencias:**
- Positivas: Rastreabilidade total, governanca auditavel
- Negativas: Overhead inicial de configuracao

**Responsavel:** Tech Lead

---

### ADR-002: STATUS.yaml por Requisito Funcional

**Data:** 2024-12-23
**Status:** Aceita

**Contexto:**
Necessidade de rastrear o progresso de cada RF de forma estruturada e
integravel com Azure DevOps.

**Decisao:**
Cada RF possui um arquivo STATUS.yaml que registra:
- Status de documentacao
- Status de desenvolvimento (backend/frontend)
- Status de testes
- Integracao com work items do DevOps

**Alternativas Consideradas:**
- Planilha Excel: Nao versionavel
- Banco de dados: Complexidade desnecessaria

**Consequencias:**
- Positivas: Versionamento Git, automacao possivel
- Negativas: Requer sincronizacao manual ou script

**Responsavel:** Tech Lead

---

### ADR-003: Modelo Multi-Tenant com Cliente como Raiz

**Data:** 2025-12-25
**Status:** Aceita

**Contexto:**
O sistema IControlIT 2.0 possui uma hierarquia multi-tenant complexa com 4 níveis:
- Cliente (tenant raiz - quem paga pelo sistema)
- Fornecedor (agrupamento lógico de empresas dentro do Cliente)
- Empresa (empresa individual dentro do Fornecedor)
- Filial (filial da empresa)

Os Modelos de Dados (MDs) foram inicialmente gerados assumindo `Fornecedor` como
entidade raiz de multi-tenancy, mas a implementação do backend já estava usando
`Cliente` como raiz.

Auditoria de conformidade (2025-12-25) identificou divergência sistemática entre
MDs (usam FornecedorId) e código backend (usa ClienteId/EmpresaId) em 100%
dos 49 RFs da Fase 2.

**Decisao:**
- **Cliente é a entidade raiz de multi-tenancy** (não Fornecedor)
- Todas as entidades devem ter FK `ClienteId` como campo obrigatório de isolamento multi-tenant
- Entidades podem ter FK adicional `EmpresaId` quando precisam de escopo por empresa específica
- TODOS os Modelos de Dados (MD-RFXXX.md) serão atualizados para refletir esta hierarquia

**Alternativas Consideradas:**
- **Alternativa 1 (Rejeitada):** Usar `Fornecedor` como raiz
  - Motivo: Não reflete modelo de negócio real (Cliente é quem paga)
  - Motivo: Exigiria refatoração massiva de ~250 entidades já implementadas
  - Motivo: Risco alto de regressões e quebra de dados existentes

- **Alternativa 2 (Rejeitada):** Manter divergência entre MDs e código
  - Motivo: Inviabiliza manutenção e auditoria
  - Motivo: Confunde novos desenvolvedores

**Consequencias:**
- **Positivas:**
  - Documentação sincronizada com código implementado
  - Hierarquia multi-tenant alinhada com modelo de negócio
  - Maior flexibilidade de isolamento (Cliente > Fornecedor > Empresa > Filial)
  - Zero risco técnico (código já está correto)

- **Negativas:**
  - Trabalho de atualização de 49 arquivos MD-RFXXX.md
  - Necessidade de documentar hierarquia completa em ARCHITECTURE.md

**Impacto:**
- 49 arquivos MD-RFXXX.md precisam ser atualizados (substituir `FornecedorId` por `ClienteId`)
- Seção de multi-tenancy será adicionada em `/docs/ARCHITECTURE.md`
- Seeds e migrations já estão corretos (usam ClienteId)

**Responsavel:** Tech Lead / Architect

---

### ADR-004: Soft Delete com Campo FlExcluido (Separação Semântica)

**Data:** 2025-12-25
**Status:** Aceita

**Contexto:**
O sistema utiliza soft delete para preservar histórico e integridade referencial.

Auditoria de conformidade (2025-12-25) identificou **inconsistência interna** no backend:
- ~60% das entidades usam campo `Ativo` (bool) para múltiplos propósitos (soft delete + flag funcional)
- ~40% das entidades usam campo `FlExcluido` (bool) exclusivamente para soft delete
- Algumas entidades têm AMBOS campos (`Ativo` + `FlExcluido`) com semânticas diferentes:
  - `Ativo`: Flag funcional (habilitado/desabilitado, ativo/inativo)
  - `FlExcluido`: Soft delete (deletado/não deletado)

Modelos de Dados (MDs) especificam `FlExcluido` (padrão SQL tradicional).

**Decisao:**
- **Padronizar soft delete usando campo `FlExcluido`** (semântica negativa)
- `FlExcluido = false` → Registro não deletado (ativo)
- `FlExcluido = true` → Registro deletado (soft delete)
- **Campo `Ativo` é OPCIONAL** e usado para flag funcional quando necessário
- Entidades podem ter:
  - **Apenas `FlExcluido`**: Soft delete simples (maioria dos casos)
  - **`FlExcluido` + `Ativo`**: Soft delete + flag funcional (casos especiais)
- TODOS os Modelos de Dados (MD-RFXXX.md) especificam `FlExcluido`

**Alternativas Consideradas:**
- **Alternativa 1 (Rejeitada):** Usar `Ativo` para soft delete
  - Motivo: Conflito semântico (desabilitado ≠ deletado)
  - Motivo: Entidade `Ativo.cs` tem conflito de nome (propriedade não pode ter mesmo nome da classe)
  - Motivo: Entidades com ambos campos (`Ativo` + `FlExcluido`) perderiam distinção semântica

- **Alternativa 2 (Rejeitada):** Manter ambos padrões
  - Motivo: Confusão constante sobre qual usar
  - Motivo: Queries inconsistentes no código

**Consequencias:**
- **Positivas:**
  - Semântica clara e separada: `Ativo` (funcional) vs `FlExcluido` (soft delete)
  - Zero conflitos de nome (entidade `Ativo.cs` pode ter propriedade `FlExcluido`)
  - Padrão SQL tradicional (convenção amplamente usada)
  - ~40% das entidades JÁ estão corretas (usam `FlExcluido`)
  - Permite desabilitar temporariamente (`Ativo=false`) sem deletar (`FlExcluido=false`)

- **Negativas:**
  - Semântica negativa menos intuitiva: `WHERE FlExcluido = false` vs `WHERE Ativo = true`
  - ~60% das entidades precisam adicionar `FlExcluido` (se usam `Ativo` para soft delete)

**Impacto:**
- Entidades que SÓ TÊM `Ativo` (usando para soft delete) precisam:
  - Adicionar propriedade `FlExcluido`
  - Migrar lógica de soft delete de `Ativo` para `FlExcluido`
  - Manter `Ativo` se necessário como flag funcional
- Entidades que JÁ TÊM `FlExcluido`: nenhuma mudança necessária
- MDs JÁ especificam `FlExcluido`: nenhuma mudança necessária
- Migration para adicionar coluna `FlExcluido` onde necessário
- Queries, validators, DTOs precisam usar `FlExcluido` para soft delete
- Convenção será documentada em `/docs/CONVENTIONS.md`

**Plano de Execução:**
1. Identificar entidades que usam `Ativo` para soft delete (sem `FlExcluido`)
2. Adicionar propriedade `FlExcluido` nessas entidades
3. Criar migration: `ALTER TABLE ... ADD FlExcluido BIT NOT NULL DEFAULT 0`
4. Atualizar queries: usar `FlExcluido` para soft delete
5. Atualizar validators e DTOs
6. Executar testes de regressão
7. MDs já estão corretos (não requer atualização)

**Responsavel:** Tech Lead / Architect

---

### ADR-005: Schema-First Testing (Temporário)

**Data:** 2026-01-07
**Status:** Aceito (temporário)
**RF Relacionado:** Infraestrutura (todos os RFs)

**Contexto:**
- EF Core Migrations com FK cycles impedem criação de banco de testes
- Azure SQL DEV (212 tabelas) funciona perfeitamente
- Testcontainers usa `EnsureCreatedAsync()` que falha devido a FK cycles
- Sistema está em desenvolvimento ativo, schema muda frequentemente
- Corrigir FK cycles agora = 2-8h + retrabalho futuro

**Decisão:**
Testcontainers usará `schema.sql` exportado do Azure SQL DEV em vez de `EnsureCreatedAsync()`.

**Implementação:**
1. Exportar schema do Azure SQL DEV via SqlPackage ou SSMS
2. Salvar em `D:\IC2\backend\IControlIT.API\tests\schema.sql`
3. Modificar `SqlTestcontainersTestDatabase.cs` linha 47
4. Executar script SQL em vez de `EnsureCreatedAsync()`

**Alternativas Consideradas:**
- **Corrigir FK cycles no EF Core**: Rejeitada (retrabalho, schema muda frequentemente)
- **Usar migrations em testes**: Rejeitada (migrations têm FK cycles)
- **Usar backup .bacpac**: Rejeitada (mais lento, arquivo grande)
- **SQL Server persistente**: Rejeitada (perde isolamento de testes)

**Consequências:**
- ✅ Testes funcionam imediatamente
- ✅ Schema de testes = Schema de produção (100% fidelidade)
- ✅ Sem dependência de migrations em testes
- ⚠️ schema.sql precisa ser atualizado manualmente quando schema mudar
- ⚠️ Duas fontes de verdade (schema.sql vs migrations)

**Trade-off Aceito:**
- Sincronização manual de schema.sql quando schema mudar
- Em troca: testes funcionam, desenvolvimento não trava

**Critério de Revisão Futura:**
- Quando schema estabilizar (após EPIC-001 concluído)
- Avaliar se vale corrigir FK cycles ou manter schema.sql permanentemente

**Responsável:** Equipe de Arquitetura IControlIT

---

(Novas decisoes devem ser adicionadas acima desta linha)

# CHECKLIST - CONTRATO DE MANUTENÇÃO COMPLETA

**Contrato:** `contracts/desenvolvimento/manutencao/manutencao-completa.md`
**Versão:** 1.0
**Data:** 2026-01-06

---

## ✅ PRÉ-REQUISITOS

- [ ] Problema exige alterações em **múltiplos arquivos** (10+ arquivos)
- [ ] Problema exige alterações em **múltiplas camadas** (cross-layer)
- [ ] Refatoração é **necessária** para correção
- [ ] **OU** Contrato de Manutenção Controlada **BLOQUEOU** por ultrapassar escopo

---

## 📋 FASE 1: ANÁLISE DE IMPACTO

- [ ] **1.1** Identificar todos os arquivos afetados
  - [ ] Domain layer
  - [ ] Application layer
  - [ ] Infrastructure layer
  - [ ] Web layer

- [ ] **1.2** Criar análise de impacto (`.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`)
  - [ ] Listar arquivos por camada
  - [ ] Estimar impacto (quantidade de arquivos/camadas)
  - [ ] Identificar decisões técnicas necessárias

- [ ] **1.3** Validar que escopo exige Manutenção Completa
  - [ ] Impacto > 3 arquivos OU > 1 camada → ✅ Manutenção Completa
  - [ ] Impacto <= 3 arquivos E 1 camada → ⚠️ Considerar Manutenção Controlada

---

## 📋 FASE 2: PLANEJAMENTO

- [ ] **2.1** Definir ordem de correção (Domain → Application → Infrastructure → Web)

- [ ] **2.2** Criar checklist de correção em `.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`
  - [ ] FASE 1 - Domain Layer (tarefas específicas)
  - [ ] FASE 2 - Application Layer (tarefas específicas)
  - [ ] FASE 3 - Infrastructure Layer (tarefas específicas)
  - [ ] FASE 4 - Web Layer (tarefas específicas)

---

## 📋 FASE 3: EXECUÇÃO DA CORREÇÃO

### FASE 3.1 - Domain Layer

- [ ] **3.1.1** Aplicar correções em Domain layer
  - [ ] Corrigir entidades
  - [ ] Corrigir enums/constants
  - [ ] Remover duplicações

- [ ] **3.1.2** Compilar: `dotnet build`
  - [ ] Exit code 0 (SUCESSO) → Prosseguir
  - [ ] Exit code != 0 (FALHA) → Corrigir antes de prosseguir

- [ ] **3.1.3** Marcar fase como concluída no checklist

### FASE 3.2 - Application Layer

- [ ] **3.2.1** Aplicar correções em Application layer
  - [ ] Corrigir commands
  - [ ] Corrigir queries
  - [ ] Corrigir handlers
  - [ ] Corrigir validators
  - [ ] Corrigir DTOs
  - [ ] Corrigir mapeamentos (AutoMapper)

- [ ] **3.2.2** Compilar: `dotnet build`
  - [ ] Exit code 0 (SUCESSO) → Prosseguir
  - [ ] Exit code != 0 (FALHA) → Corrigir antes de prosseguir

- [ ] **3.2.3** Marcar fase como concluída no checklist

### FASE 3.3 - Infrastructure Layer

- [ ] **3.3.1** Aplicar correções em Infrastructure layer
  - [ ] Corrigir DbContext
  - [ ] Corrigir configurations (EF Core)
  - [ ] Corrigir repositories
  - [ ] Corrigir migrations (se necessário)

- [ ] **3.3.2** Compilar: `dotnet build`
  - [ ] Exit code 0 (SUCESSO) → Prosseguir
  - [ ] Exit code != 0 (FALHA) → Corrigir antes de prosseguir

- [ ] **3.3.3** Marcar fase como concluída no checklist

### FASE 3.4 - Web Layer

- [ ] **3.4.1** Aplicar correções em Web layer
  - [ ] Corrigir endpoints
  - [ ] Corrigir middlewares (se necessário)
  - [ ] Corrigir filters (se necessário)

- [ ] **3.4.2** Compilar: `dotnet build`
  - [ ] Exit code 0 (SUCESSO) → Prosseguir
  - [ ] Exit code != 0 (FALHA) → Corrigir antes de prosseguir

- [ ] **3.4.3** Marcar fase como concluída no checklist

---

## 📋 FASE 4: VALIDAÇÃO FINAL

- [ ] **4.1** Executar testes unitários
  - [ ] `dotnet test`
  - [ ] Resultado: 100% passando

- [ ] **4.2** Executar testes de integração (se aplicável)
  - [ ] `dotnet test --filter "Category=Integration"`
  - [ ] Resultado: 100% passando

- [ ] **4.3** Validar build completo
  - [ ] Backend: `dotnet build --no-incremental` → SUCESSO
  - [ ] Frontend (se afetado): `npm run build` → SUCESSO

---

## 📋 FASE 5: COMMIT E DOCUMENTAÇÃO

- [ ] **5.1** Criar branch dedicado
  - [ ] `git checkout dev`
  - [ ] `git pull origin dev`
  - [ ] `git checkout -b manutencao/correcao-[PROBLEMA]-[DATA]`

- [ ] **5.2** Commit estruturado
  - [ ] Mensagem segue template:
    ```
    fix(camadas): título curto

    PROBLEMA IDENTIFICADO:
    - [descrição]

    CORREÇÕES APLICADAS:
    - Domain Layer: [lista]
    - Application Layer: [lista]
    - Infrastructure Layer: [lista]

    IMPACTO:
    - Arquivos alterados: X
    - Camadas afetadas: Y
    - Builds: SUCESSO
    - Testes: SUCESSO

    TIPO DE MANUTENÇÃO: Completa (cross-layer)
    CONTRATO: contracts/desenvolvimento/manutencao/manutencao-completa.md
    ```

- [ ] **5.3** Atualizar DECISIONS.md (SE decisões técnicas tomadas)
  - [ ] Contexto do problema
  - [ ] Decisões tomadas (com justificativa)
  - [ ] Alternativas consideradas
  - [ ] Impacto das decisões
  - [ ] Tipo de manutenção (Completa)

---

## 📋 CRITÉRIO DE PRONTO

### Correção Aplicada

- [ ] Análise de impacto criada (`.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md`)
- [ ] Checklist de correção definido
- [ ] Correções aplicadas por fase (Domain → Application → Infrastructure → Web)
- [ ] Compilação validada após CADA fase

### Validação Técnica

- [ ] Build backend: **SUCESSO**
- [ ] Build frontend: **SUCESSO** (se aplicável)
- [ ] Testes unitários: **100% passando**
- [ ] Testes de integração: **100% passando** (se aplicável)

### Documentação

- [ ] Branch criado: `manutencao/correcao-[PROBLEMA]-[DATA]`
- [ ] Commit estruturado com contexto completo
- [ ] **SE decisões tomadas:** DECISIONS.md atualizado
- [ ] Análise de impacto salva em `.temp_ia/`

### Entrega

- [ ] Branch pronto para PR contra `dev`
- [ ] Nenhuma violação de contrato
- [ ] Nenhum breaking change não justificado
- [ ] Código compilando sem warnings relacionados

---

## ❌ VALIDAÇÕES DE PROIBIÇÕES

### Proibições Absolutas

- [ ] ✅ ZERO features novas adicionadas
- [ ] ✅ ZERO alterações de arquitetura
- [ ] ✅ ZERO breaking changes em APIs públicas (sem justificativa)
- [ ] ✅ ZERO refatorações não relacionadas ao problema

### Proibições de Git/Commits

- [ ] ✅ ZERO commits em `dev` diretamente (sempre em branch)
- [ ] ✅ ZERO commits sem mensagem estruturada
- [ ] ✅ ZERO commits sem validar builds/testes

---

**FIM DO CHECKLIST**

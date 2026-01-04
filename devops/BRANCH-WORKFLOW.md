# Workflow de Branches - IControlIT 2.0

Este documento define o fluxo de trabalho de branches para o projeto.

---

## Branches Principais

| Branch | Proposito | Protegida |
|--------|-----------|-----------|
| **main** | Producao estavel | SIM |
| **dev** | Desenvolvimento ativo | SIM |

---

## Regra Fundamental

> **Todas as feature branches DEVEM ser derivadas de `dev`**
> **Ao concluir cada etapa, DEVE fazer merge de volta para `dev`**

---

## Fluxo de Trabalho

### 1. Criar Feature Branch

```bash
# Sempre partir de dev atualizado
git checkout dev
git pull origin dev

# Criar branch da feature
git checkout -b feature/RFXXX-descricao
```

### 2. Durante o Desenvolvimento

```bash
# Commits frequentes
git add .
git commit -m "feat(RFXXX): descricao da alteracao"

# Manter sincronizado com dev
git fetch origin dev
git rebase origin/dev
```

### 3. Ao Concluir Etapa (Backend/Frontend/Testes)

```bash
# Garantir que esta atualizado
git fetch origin dev
git rebase origin/dev

# Push da branch
git push origin feature/RFXXX-descricao

# Criar PR para dev
# OU merge direto (se permitido)
git checkout dev
git pull origin dev
git merge feature/RFXXX-descricao
git push origin dev
```

---

## Nomenclatura de Branches

| Tipo | Padrao | Exemplo |
|------|--------|---------|
| Feature | `feature/RFXXX-descricao` | `feature/RF027-aditivos-contratos` |
| Bugfix | `bugfix/RFXXX-descricao` | `bugfix/RF015-validacao-endereco` |
| Hotfix | `hotfix/descricao` | `hotfix/correcao-login` |

---

## Fluxo por Contrato

### CONTRATO-EXECUCAO-BACKEND

```
dev -> feature/RFXXX-backend -> (commit) -> merge dev
```

### CONTRATO-EXECUCAO-FRONTEND

```
dev -> feature/RFXXX-frontend -> (commit) -> merge dev
```

### CONTRATO-EXECUCAO-TESTES

```
dev -> feature/RFXXX-testes -> (commit) -> merge dev
```

---

## Regras Inviolaveis

1. **NUNCA** criar branch a partir de `main` para features
2. **NUNCA** fazer push direto para `main`
3. **SEMPRE** manter `dev` atualizado apos cada etapa
4. **SEMPRE** resolver conflitos antes de merge
5. **SEMPRE** executar testes antes de merge

---

## STATUS.yaml - Campo branch

O campo `branch` no STATUS.yaml deve registrar a branch ativa:

```yaml
desenvolvimento:
  backend:
    status: in_progress
    branch: feature/RF027-backend  # Branch atual
  frontend:
    status: not_started
    branch: null
```

Ao concluir e fazer merge:

```yaml
desenvolvimento:
  backend:
    status: done
    branch: null  # Limpar apos merge em dev
  frontend:
    status: in_progress
    branch: feature/RF027-frontend
```

---

## Merge para Main (Release)

Somente apos aprovacao completa do QA:

```bash
git checkout main
git pull origin main
git merge dev
git push origin main
git tag -a vX.Y.Z -m "Release X.Y.Z"
git push origin --tags
```

---

## Comandos Uteis

```bash
# Ver branches locais
git branch

# Ver todas as branches
git branch -a

# Deletar branch local apos merge
git branch -d feature/RFXXX-descricao

# Deletar branch remota
git push origin --delete feature/RFXXX-descricao
```

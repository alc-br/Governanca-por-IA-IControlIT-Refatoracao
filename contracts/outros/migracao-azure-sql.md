# CONTRATO DE MIGRAÇÃO AZURE SQL

**Versão:** 1.0
**Data:** 2026-01-06
**Status:** Ativo
**Branch Obrigatório:** `migration/azure-sql-complete`
**Base Técnica:** D:\IC2\PLANO-MIGRACAO-AZURE-SQL.md
**Prompt:** D:\IC2_Governanca\prompts\outros\migracao-azure-sql.md
**Checklist:** D:\IC2_Governanca\checklists\outros\migracao-azure-sql.md

---

## 📋 SUMÁRIO EXECUTIVO

Este contrato executa migração completa de SQLite (DEV) para Azure SQL Database em todos os ambientes.

**Responsabilidades:**
- **USUÁRIO:** Executar `az login` antes de ativar o contrato
- **AGENTE:** Criar infraestrutura DEV, atualizar código, aplicar migrations, validar

---

## 1. PRÉ-REQUISITOS OBRIGATÓRIOS (BLOQUEANTES)

| Pré-requisito | Validação | Responsável |
|---------------|-----------|-------------|
| RF006 merged | Commit 5fc9cf91 em `dev` | AGENTE |
| Migrations corrigidas | ZERO tipos SQLite | AGENTE |
| Docker rodando | `docker ps` OK | AGENTE |
| **Azure autenticado** | `az account show` OK | **USUÁRIO** |
| dotnet-ef tool | `dotnet ef --version` OK | AGENTE |

**⚠️ USUÁRIO DEVE EXECUTAR `az login` ANTES DE ATIVAR ESTE CONTRATO**

---

## 2. BRANCH OBRIGATÓRIO: `migration/azure-sql-complete`

```bash
git checkout dev && git pull
git checkout -b migration/azure-sql-complete
git push -u origin migration/azure-sql-complete
```

**Validação:**
```bash
git branch --show-current
# Esperado: migration/azure-sql-complete
```

**Se falhar:** BLOQUEIO TOTAL

---

## 3. ESCOPO PERMITIDO E PROIBIDO

### ✅ PERMITIDO
- Alterar `appsettings.Development.json`
- Alterar `Program.cs` (remover SQLite)
- Criar resource group DEV
- Criar Azure SQL Server/Database DEV
- Atualizar `.gitignore`
- Atualizar `DECISIONS.md` (D:\IC2)
- Criar `AZURE-SQL-MIGRATION.md` (D:\IC2_Governanca)

### ❌ PROIBIDO
- Alterar migrations (já corrigidas RF006)
- Criar resource groups HOM/PRD (já existem)
- Executar fora do branch `migration/azure-sql-complete`

---

## 4. WORKFLOW (7 FASES - 7 COMMITS)

### FASE 0: VALIDAR AUTENTICAÇÃO AZURE

```bash
az account show
```

**Se FALHAR:**
```
❌ BLOQUEIO - Azure não autenticado

AÇÃO USUÁRIO:
1. Execute: az login
2. Faça login no navegador
3. Re-execute contrato

O agente NÃO pode executar az login (requer navegador).
```

---

### FASE 1: PREPARAÇÃO

1. Validar branch `migration/azure-sql-complete`
2. Backup SQLite: `.temp_ia/backup-sqlite/IControlIT-*.db`
3. Validar migrations (ZERO tipos SQLite)
4. **Commit:** `chore(infra): preparar ambiente para migração Azure SQL`

---

### FASE 2: CRIAR INFRAESTRUTURA AZURE SQL DEV

#### 2.1. Obter Padrão de Resource Groups Existentes

```bash
# Obter configuração de HOM (referência)
az group show --name rg-icontrolit-hom --query "{location:location, tags:tags}"
```

#### 2.2. Criar Resource Group DEV (seguindo padrão)

```bash
az group create \
  --name rg-icontrolit-dev \
  --location brazilsouth \
  --tags Environment=Development Project=IControlIT
```

#### 2.3. Criar SQL Server DEV

```bash
$suffix = Get-Random -Minimum 1000 -Maximum 9999
az sql server create \
  --name "sql-icontrolit-dev-$suffix" \
  --resource-group rg-icontrolit-dev \
  --location brazilsouth \
  --admin-user sqladmin \
  --admin-password "YourStrong@Passw0rd123"
```

#### 2.4. Configurar Firewall

```bash
# Azure Services
az sql server firewall-rule create \
  --resource-group rg-icontrolit-dev \
  --server "sql-icontrolit-dev-$suffix" \
  --name AllowAzureServices \
  --start-ip 0.0.0.0 --end-ip 0.0.0.0

# IP Local
$myIp = (Invoke-WebRequest -Uri "https://api.ipify.org").Content.Trim()
az sql server firewall-rule create \
  --resource-group rg-icontrolit-dev \
  --server "sql-icontrolit-dev-$suffix" \
  --name AllowDeveloperIP \
  --start-ip $myIp --end-ip $myIp
```

#### 2.5. Criar Database (Basic Tier - ~$5/mês)

```bash
az sql db create \
  --resource-group rg-icontrolit-dev \
  --server "sql-icontrolit-dev-$suffix" \
  --name IControlIT_DEV \
  --service-objective Basic \
  --backup-storage-redundancy Local
```

#### 2.6. Validar e Documentar

```bash
# Validar
az sql db show \
  --resource-group rg-icontrolit-dev \
  --server "sql-icontrolit-dev-$suffix" \
  --name IControlIT_DEV

# Documentar em .temp_ia/INFRA-AZURE-SQL-DEV.md
```

**Commit:** `feat(infra): criar infraestrutura Azure SQL DEV`

---

### FASE 3: ATUALIZAR CÓDIGO

#### 3.1. appsettings.Development.json

**ANTES:**
```json
"ConnectionStrings": {
  "IControlIT.APIDb": "Data Source=IControlIT.db"
}
```

**DEPOIS:**
```json
"ConnectionStrings": {
  "IControlIT.APIDb": "Server=tcp:sql-icontrolit-dev-XXXX.database.windows.net,1433;Initial Catalog=IControlIT_DEV;User ID=sqladmin;Password=YourStrong@Passw0rd123;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"
}
```

#### 3.2. Program.cs (remover SQLite)

**Caminho:** `D:\IC2\backend\IControlIT.API\src\Web\Program.cs` (~linhas 160-191)

Remover bloco `if (builder.Environment.IsDevelopment())` e usar SEMPRE `UseSqlServer`.

#### 3.3. .gitignore

```bash
echo "*.db" >> D:\IC2\.gitignore
echo "*.db-shm" >> D:\IC2\.gitignore
echo "*.db-wal" >> D:\IC2\.gitignore
```

**Commit:** `refactor(infra): remover lógica SQLite de Program.cs`

---

### FASE 4: APLICAR MIGRATIONS

```bash
cd D:\IC2\backend\IControlIT.API
dotnet ef database update --connection "[CONNECTION_STRING_DEV]"

# Validar
dotnet ef migrations list --connection "[CONNECTION_STRING_DEV]"
# Esperado: 62 migrations aplicadas
```

**Commit:** `feat(infra): aplicar migrations em Azure SQL`

---

### FASE 5: MIGRAR DADOS (OPCIONAL)

Verificar se SQLite tem dados:
- Se < 100KB: Pular (apenas schema)
- Se > 100KB: Executar migração manual ou repovoar via seeds

**Commit:** `chore(data): migrar dados SQLite → Azure SQL` (se executado)

---

### FASE 6: VALIDAÇÃO COMPLETA

```bash
# Build
dotnet build --no-incremental

# Testes
dotnet test tests/Domain.UnitTests/          # 5/5
dotnet test tests/Application.UnitTests/     # 26/26
dotnet test tests/Application.FunctionalTests/ # 23/23

# Aplicação
cd src/Web && dotnet run
curl https://localhost:5001/health  # 200 OK
```

**Commit:** `test(infra): validar aplicação em Azure SQL`

---

### FASE 7: DOCUMENTAÇÃO

#### 7.1. Atualizar DECISIONS.md

**Caminho:** `D:\IC2\DECISIONS.md`

Adicionar decisão arquitetural sobre migração.

#### 7.2. Criar AZURE-SQL-MIGRATION.md

**Caminho:** `D:\IC2_Governanca\AZURE-SQL-MIGRATION.md`

Relatório executivo completo da migração.

#### 7.3. Mover SQLite

```bash
Move-Item "D:\IC2\backend\IControlIT.API\src\Web\IControlIT.db" "D:\IC2\.temp_ia\backup-sqlite\"
```

**Commit:** `docs(infra): documentar migração completa Azure SQL`

---

## 5. ROLLBACK (SE FALHAR)

| Fase | Rollback |
|------|----------|
| FASE 0 | Instruir usuário: `az login` |
| FASE 1 | Abortar (sem mudanças) |
| FASE 2 | `az group delete --name rg-icontrolit-dev --yes` |
| FASE 3 | `git reset --hard HEAD~1` |
| FASE 4 | Reverter FASE 3 + deletar database |
| FASE 6 | `git reset --hard HEAD~2` |
| FASE 7 | `git reset --hard HEAD~1` |

**Rollback Completo:**
```bash
git checkout dev
git branch -D migration/azure-sql-complete
git push origin --delete migration/azure-sql-complete
az group delete --name rg-icontrolit-dev --yes
# Restaurar SQLite do backup
```

---

## 6. CRITÉRIO DE PRONTO

- [ ] Azure autenticado (az account show OK)
- [ ] Resource Group DEV criado
- [ ] Azure SQL Server DEV criado
- [ ] Azure SQL Database DEV criado (Basic)
- [ ] Firewall configurado
- [ ] appsettings.Development.json atualizado
- [ ] Program.cs refatorado (sem SQLite)
- [ ] 62 migrations aplicadas em DEV
- [ ] Build: 0 erros
- [ ] Testes: 54/54 passando
- [ ] Aplicação funcional
- [ ] DECISIONS.md atualizado
- [ ] AZURE-SQL-MIGRATION.md criado
- [ ] 7 commits atômicos
- [ ] SQLite em backup

---

## 7. PRÓXIMOS PASSOS

1. Merge `migration/azure-sql-complete` → `dev`
2. Monitorar custos Azure DEV (30 dias)
3. Deletar SQLite (após 7 dias validação)

---

## 8. PROIBIÇÕES

❌ **NUNCA:**
- Executar sem `az login` prévio
- Executar fora do branch `migration/azure-sql-complete`
- Alterar migrations existentes
- Criar resource groups HOM/PRD (já existem)
- Deletar SQLite antes de 7 dias

---

**FIM DO CONTRATO**

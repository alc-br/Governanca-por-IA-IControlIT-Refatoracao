# PROMPT: Migração Azure SQL

**Contrato:** D:\IC2_Governanca\contracts\outros\migracao-azure-sql.md
**Checklist:** D:\IC2_Governanca\checklists\outros\migracao-azure-sql.md
**Plano Técnico:** D:\IC2\PLANO-MIGRACAO-AZURE-SQL.md

---

## 🚨 PRÉ-REQUISITO OBRIGATÓRIO (USUÁRIO)

**ANTES de ativar este prompt, você DEVE:**

```bash
az login
```

1. Aguarde o navegador abrir
2. Faça login com suas credenciais Azure
3. Aguarde confirmação: "You have logged in"
4. **SÓ ENTÃO** execute o prompt abaixo

**O agente validará que `az account show` funciona, mas NÃO executará `az login` (requer navegador).**

---

## PROMPT DE ATIVAÇÃO

Execute migração completa para Azure SQL conforme contrato de Migração Azure SQL.

**Contrato:** D:\IC2_Governanca\contracts\outros\migracao-azure-sql.md

Modo governança rígida. Não negociar escopo. Não extrapolar.
Seguir D:\IC2\CLAUDE.md.

---

## CONTEXTO

**Motivação:**
- Sistema usa SQLite em DEV e SQL Server em HOM/PRD
- Inconsistência causa bugs
- Migrations já corrigidas para SQL Server (commit 5fc9cf91 - RF006)

**Objetivo:**
- Migrar DEV para Azure SQL Database (Basic Tier - ~$5/mês)
- Garantir consistência entre todos os ambientes

**Infraestrutura Existente:**
- ✅ HOM: rg-icontrolit-hom (já existe)
- ✅ PRD: rg-icontrolit-prd (já existe)
- ❌ DEV: rg-icontrolit-dev (CRIAR seguindo padrão HOM/PRD)

---

## MODO DE EXECUÇÃO

### AUTONOMIA TOTAL (APÓS VALIDAÇÃO AZURE)

- ❌ NÃO perguntar permissões ao usuário
- ❌ NÃO esperar confirmação para cada passo
- ✅ EXECUTAR automaticamente todas as 7 fases
- ✅ PARAR imediatamente se qualquer fase falhar
- ✅ GERAR rollback se necessário

### EXCEÇÃO: APROVAÇÃO USUÁRIO

**Apenas 1 momento requer aprovação:**
- **FASE 4 - Aplicar migrations em PRD** (opcional - pode pular)

---

## BRANCH OBRIGATÓRIO

**SEMPRE executar em:** `migration/azure-sql-complete`

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

**Se NÃO estiver neste branch: BLOQUEIO TOTAL**

---

## WORKFLOW (7 FASES - 7 COMMITS)

### FASE 0: VALIDAR AUTENTICAÇÃO AZURE

```bash
az account show
```

**Se FALHAR:**
```
❌ BLOQUEIO TOTAL - Azure não autenticado

AÇÃO USUÁRIO:
1. Execute: az login
2. Faça login no navegador
3. Re-execute este prompt

O agente NÃO pode executar az login.
```

---

### FASE 1: PREPARAÇÃO

1. Validar branch: `migration/azure-sql-complete`
2. Validar RF006 merged (commit 5fc9cf91)
3. Validar migrations (ZERO tipos SQLite)
4. Backup SQLite: `.temp_ia/backup-sqlite/IControlIT-*.db`
5. Commit: `chore(infra): preparar ambiente para migração Azure SQL`

---

### FASE 2: CRIAR INFRAESTRUTURA AZURE SQL DEV

**Passos:**

1. **Obter padrão de HOM/PRD:**
   ```bash
   az group show --name rg-icontrolit-hom --query "{location:location, tags:tags}"
   ```

2. **Criar Resource Group DEV** (seguindo padrão):
   ```bash
   az group create \
     --name rg-icontrolit-dev \
     --location brazilsouth \
     --tags Environment=Development Project=IControlIT
   ```

3. **Criar SQL Server DEV:**
   ```bash
   az sql server create \
     --name sql-icontrolit-dev-[RANDOM] \
     --resource-group rg-icontrolit-dev \
     --location brazilsouth \
     --admin-user sqladmin \
     --admin-password "YourStrong@Passw0rd123"
   ```

4. **Configurar Firewall:**
   - Azure Services: 0.0.0.0
   - IP Local: (obter via https://api.ipify.org)

5. **Criar Database (Basic Tier - ~$5/mês):**
   ```bash
   az sql db create \
     --resource-group rg-icontrolit-dev \
     --server sql-icontrolit-dev-[RANDOM] \
     --name IControlIT_DEV \
     --service-objective Basic
   ```

6. **Validar:**
   ```bash
   az sql db show --resource-group rg-icontrolit-dev --server [...] --name IControlIT_DEV
   # Esperado: status = "Online", tier = "Basic"
   ```

7. **Documentar:** `.temp_ia/INFRA-AZURE-SQL-DEV.md`

8. **Commit:** `feat(infra): criar infraestrutura Azure SQL DEV`

---

### FASE 3: ATUALIZAR CÓDIGO

1. **Atualizar appsettings.Development.json:**
   - ANTES: `"Data Source=IControlIT.db"`
   - DEPOIS: Connection string Azure SQL DEV

2. **Atualizar Program.cs:**
   - Remover bloco `if (builder.Environment.IsDevelopment())`
   - Usar SEMPRE `UseSqlServer` (linhas ~160-191)

3. **Atualizar .gitignore:**
   - Adicionar: `*.db`, `*.db-shm`, `*.db-wal`

4. **Commit:** `refactor(infra): remover lógica SQLite de Program.cs`

---

### FASE 4: APLICAR MIGRATIONS

1. **Validar build:**
   ```bash
   dotnet build --no-incremental
   # Esperado: 0 erros
   ```

2. **Aplicar migrations em DEV:**
   ```bash
   dotnet ef database update --connection "[CONNECTION_STRING_DEV]"
   ```

3. **Validar:**
   ```bash
   dotnet ef migrations list --connection "[CONNECTION_STRING_DEV]"
   # Esperado: 62 migrations aplicadas
   ```

4. **Commit:** `feat(infra): aplicar migrations em Azure SQL`

---

### FASE 5: MIGRAR DADOS (OPCIONAL)

1. **Verificar se SQLite tem dados:**
   - Se < 100KB: Pular (apenas schema)
   - Se > 100KB: Executar migração OU repovoar via seeds

2. **Commit (se executado):** `chore(data): migrar dados SQLite → Azure SQL`

---

### FASE 6: VALIDAÇÃO COMPLETA

1. **Build:**
   ```bash
   dotnet build --no-incremental
   # Esperado: 0 erros
   ```

2. **Testes:**
   ```bash
   dotnet test tests/Domain.UnitTests/          # 5/5
   dotnet test tests/Application.UnitTests/     # 26/26
   dotnet test tests/Application.FunctionalTests/ # 23/23
   ```

3. **Aplicação:**
   ```bash
   dotnet run --project src/Web
   curl https://localhost:5001/health  # 200 OK
   ```

4. **Commit:** `test(infra): validar aplicação em Azure SQL`

---

### FASE 7: DOCUMENTAÇÃO

1. **Atualizar DECISIONS.md** (D:\IC2):
   - Adicionar decisão arquitetural sobre migração

2. **Criar AZURE-SQL-MIGRATION.md** (D:\IC2_Governanca):
   - Relatório executivo completo

3. **Mover SQLite para backup:**
   ```bash
   Move-Item src/Web/IControlIT.db .temp_ia/backup-sqlite/
   ```

4. **Commit:** `docs(infra): documentar migração completa Azure SQL`

---

## ROLLBACK (SE FALHAR)

**Rollback Completo:**

```bash
# 1. Voltar para dev
git checkout dev

# 2. Deletar branch
git branch -D migration/azure-sql-complete
git push origin --delete migration/azure-sql-complete

# 3. Deletar resource group Azure
az group delete --name rg-icontrolit-dev --yes

# 4. Restaurar SQLite do backup
Copy-Item .temp_ia/backup-sqlite/IControlIT-*.db backend/IControlIT.API/src/Web/IControlIT.db
```

---

## CRITÉRIO DE SUCESSO

- [ ] Azure autenticado (az account show OK)
- [ ] Resource Group DEV criado (rg-icontrolit-dev)
- [ ] SQL Server DEV criado (sql-icontrolit-dev-XXXX)
- [ ] Database DEV criado (IControlIT_DEV - Basic)
- [ ] Firewall configurado
- [ ] appsettings.Development.json atualizado
- [ ] Program.cs sem lógica SQLite
- [ ] 62 migrations aplicadas em DEV
- [ ] Build: 0 erros
- [ ] Testes: 54/54 passando
- [ ] Aplicação funcional
- [ ] DECISIONS.md atualizado
- [ ] AZURE-SQL-MIGRATION.md criado
- [ ] 7 commits atômicos
- [ ] SQLite em backup (.temp_ia/backup-sqlite/)
- [ ] Branch pronto para merge

---

## PRÓXIMOS PASSOS (PÓS-MIGRAÇÃO)

1. Merge `migration/azure-sql-complete` → `dev`
2. Validar em HOM (via pipeline)
3. Monitorar custos Azure DEV (30 dias)
4. Deletar SQLite definitivamente (após 7 dias)

---

## PROIBIÇÕES

❌ **NUNCA:**
- Executar sem `az login` prévio do usuário
- Executar fora do branch `migration/azure-sql-complete`
- Alterar migrations existentes
- Criar resource groups HOM/PRD (já existem)
- Deletar SQLite antes de 7 dias de validação

---

## EVIDÊNCIAS OBRIGATÓRIAS

Ao final, gerar em `.temp_ia/`:
- `INFRA-AZURE-SQL-DEV.md` (documentação infraestrutura)
- `backup-sqlite/IControlIT-*.db` (backup SQLite)

E em `D:\IC2_Governanca/`:
- `AZURE-SQL-MIGRATION.md` (relatório executivo)

---

**LEMBRE-SE:** Execute `az login` ANTES de ativar este prompt!

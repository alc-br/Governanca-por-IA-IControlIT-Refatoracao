# GUIA-BD.md - Guia de Banco de Dados

**Projeto:** Modernização IControlIT
**Versão:** 1.0
**Data:** 2025-01-14
**Audiência:** Desenvolvedores (Backend/Full-Stack)

---

## 🎯 Objetivo

Este guia documenta **tudo** sobre gerenciamento de banco de dados no projeto IControlIT, incluindo:
- Como migrations funcionam
- Comandos essenciais
- Padrões e convenções
- O que commitar e o que NÃO commitar
- Troubleshooting comum

---

## 📚 Documentação Relacionada

**Leia também:**
- [IMPORTANTE-BANCO-DE-DADOS.md](../IMPORTANTE-BANCO-DE-DADOS.md) - Explicação completa com FAQ
- [RESUMO-BANCO-DE-DADOS-GIT.md](../RESUMO-BANCO-DE-DADOS-GIT.md) - Resumo executivo
- [PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md) - Padrões de código backend

---

## 🏗️ Arquitetura do Banco de Dados

### Tecnologias

| Ambiente | Banco de Dados | ORM | Provedor |
|----------|---------------|-----|----------|
| **Desenvolvimento** | SQLite 3 | Entity Framework Core 10 | Microsoft.EntityFrameworkCore.Sqlite |
| **Produção** | SQL Server | Entity Framework Core 10 | Microsoft.EntityFrameworkCore.SqlServer |

### Estrutura de Código

```
backend/IControlIT.API/src/
├── Domain/
│   └── Entities/                    # Entidades do domínio
├── Application/
│   └── Common/
│       └── Interfaces/
│           └── IApplicationDbContext.cs  # Interface do contexto
├── Infrastructure/
│   └── Data/
│       ├── ApplicationDbContext.cs       # DbContext principal
│       ├── Configurations/               # Configurações EF (Fluent API)
│       ├── Interceptors/
│       │   ├── AuditInterceptor.cs      # Auditoria automática
│       │   └── SoftDeleteInterceptor.cs # Soft delete automático
│       └── Migrations/                   # ⭐ MIGRATIONS (vão no Git)
│           ├── 20251106012228_AddRF021Notificacoes.cs
│           ├── 20251106013036_AddRF017TemplateEngineBase.cs
│           ├── ... (18 migrations no total)
│           └── ApplicationDbContextModelSnapshot.cs
└── Web/
    └── IControlIT.db                     # ⚠️ Banco SQLite (NÃO vai no Git)
```

---

## ✅ O que VAI para o Git

**SEMPRE commitar:**

1. **Migrations (`.cs` files)**
   - Localização: `src/Infrastructure/Data/Migrations/*.cs`
   - Exemplo: `20251114120000_AdicionarColunaEmail.cs`
   - Função: Scripts que CRIAM/MODIFICAM o schema do banco

2. **ApplicationDbContextModelSnapshot.cs**
   - Localização: `src/Infrastructure/Data/Migrations/ApplicationDbContextModelSnapshot.cs`
   - Função: Snapshot do estado atual do schema (usado pelo EF Core)

3. **Configurações EF Core**
   - Localização: `src/Infrastructure/Data/Configurations/*.cs`
   - Exemplo: `UsuarioConfiguration.cs`
   - Função: Fluent API para configurar entidades

4. **DbContext e Interceptors**
   - `ApplicationDbContext.cs`
   - `AuditInterceptor.cs`
   - `SoftDeleteInterceptor.cs`

---

## ❌ O que NÃO VAI para o Git

**NUNCA commitar:**

1. **Banco de dados SQLite**
   - ❌ `IControlIT.db`
   - ❌ `IControlIT.db-shm` (arquivo temporário SQLite)
   - ❌ `IControlIT.db-wal` (Write-Ahead Log SQLite)

2. **Por quê?**
   - Repositório fica pesado (banco pode ter dezenas de MB)
   - Conflitos entre desenvolvedores
   - Dados sensíveis podem vazar
   - Git não versiona bem arquivos binários
   - Clone/push/pull ficam lentos

**Verificação no `.gitignore` (linha 41):**
```gitignore
# --- Database ---
*.db          # ← Ignora TODOS os arquivos .db
*.db-shm      # ← Ignora arquivos temporários do SQLite
*.db-wal      # ← Ignora Write-Ahead Log do SQLite
```

---

## 🔧 Comandos Essenciais

### 1. Restaurar Ferramentas .NET

**Sempre executar ANTES de usar `dotnet ef` pela primeira vez:**

```bash
cd backend/IControlIT.API
dotnet tool restore
```

**O que faz:**
- Instala `dotnet-ef` versão 9.0.10
- Instala `nswag.consolecore` versão 14.0.8

---

### 2. Criar o Banco de Dados (Nova Máquina)

```bash
cd backend/IControlIT.API

# Aplicar TODAS as migrations (criar banco do zero)
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Resultado:**
- ✅ Banco criado: `src/Web/IControlIT.db`
- ✅ 18 migrations aplicadas automaticamente
- ✅ Estrutura idêntica à de outros desenvolvedores

---

### 3. Criar uma Nova Migration

**Quando você modifica entidades ou adiciona novas tabelas:**

```bash
cd backend/IControlIT.API

# 1. Criar migration
dotnet ef migrations add NomeDaMigration \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# 2. Aplicar migration localmente
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Exemplo real:**
```bash
# Adicionando coluna Email à tabela Usuario
dotnet ef migrations add AdicionarColunaEmailUsuario \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Arquivo criado:**
```
src/Infrastructure/Data/Migrations/20251114120000_AdicionarColunaEmailUsuario.cs
```

---

### 4. Listar Migrations

**Ver todas as migrations e seu status (Applied/Pending):**

```bash
cd backend/IControlIT.API

dotnet ef migrations list \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Saída esperada:**
```
20251106012228_AddRF021Notificacoes (Applied)
20251106013036_AddRF017TemplateEngineBase (Applied)
20251106112924_AddRF007EnhancedRoleManagement (Applied)
...
20251114120000_AdicionarColunaEmailUsuario (Pending)
```

---

### 5. Ver SQL Gerado por Migrations

**Útil para revisar antes de aplicar em produção:**

```bash
cd backend/IControlIT.API

# Gerar script SQL de TODAS as migrations
dotnet ef migrations script \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext \
  --output migration.sql
```

**Script SQL gerado:** `migration.sql` (pode ser executado manualmente no SQL Server)

---

### 6. Remover Última Migration (Não Aplicada)

**Se você criou uma migration errada e NÃO aplicou ainda:**

```bash
cd backend/IControlIT.API

dotnet ef migrations remove \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**⚠️ ATENÇÃO:**
- Só funciona se a migration NÃO foi aplicada (`dotnet ef database update`)
- Se já aplicou, precisa reverter primeiro

---

### 7. Reverter Migration Aplicada

**Voltar para uma migration específica:**

```bash
cd backend/IControlIT.API

# Reverter para migration específica (nome ou 0 para tudo)
dotnet ef database update NomeDaMigrationAnterior \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# Exemplo: Reverter TODAS (banco vazio)
dotnet ef database update 0 \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

---

## 📋 Padrões e Convenções

### 1. Nomenclatura de Migrations

**Padrão:** `<Verbo><Descrição>` ou `<RF>_<Descrição>`

✅ **CORRETO:**
- `AddRF021Notificacoes`
- `AddEmpresasTable`
- `UpdateUsuarioAddEmail`
- `RF008_AddEmpresasFiliais`

❌ **ERRADO:**
- `Migration1` (não descritivo)
- `Fix` (vago)
- `Teste` (não usar em produção)

### 2. Nomenclatura de Tabelas

**Padrão:** PascalCase, singular

✅ **CORRETO:**
- `Usuario`
- `Empresa`
- `SistemaIdioma`
- `SistemaConfiguracaoGeral`

❌ **ERRADO:**
- `Usuarios` (plural)
- `usuario` (minúscula)
- `tbl_usuario` (prefixo desnecessário)

### 3. Nomenclatura de Colunas

**Padrão:** PascalCase

✅ **CORRETO:**
- `Id`
- `Nome`
- `Email`
- `DataCriacao`
- `UsuarioId` (FK)
- `EmpresaId` (FK para multi-tenancy)

❌ **ERRADO:**
- `id` (minúscula)
- `data_criacao` (snake_case)
- `usuario_id` (snake_case)

### 4. Campos Obrigatórios em TODAS as Entidades

**Auditoria automática (AuditInterceptor):**
```csharp
public class MinhaEntidade : BaseAuditableEntity
{
    public Guid Id { get; set; }

    // ✅ Herdados de BaseAuditableEntity (OBRIGATÓRIOS):
    // public DateTime Created { get; set; }
    // public string? CreatedBy { get; set; }
    // public DateTime? LastModified { get; set; }
    // public string? LastModifiedBy { get; set; }
}
```

**Multi-tenancy (OBRIGATÓRIO em entidades de negócio):**
```csharp
public class MinhaEntidade : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public Guid EmpresaId { get; set; }  // ✅ OBRIGATÓRIO para multi-tenancy

    // Propriedades de negócio
    public string Nome { get; set; }
}
```

**Soft Delete (para entidades que podem ser "apagadas"):**
```csharp
public class MinhaEntidade : BaseAuditableEntity
{
    public Guid Id { get; set; }
    public bool IsDeleted { get; set; }       // ✅ Flag de soft delete
    public DateTime? DeletedAt { get; set; }  // ✅ Data de exclusão
}
```

### 5. Configuração Fluent API

**Sempre criar arquivo de configuração para cada entidade:**

```csharp
// src/Infrastructure/Data/Configurations/MinhaEntidadeConfiguration.cs
public class MinhaEntidadeConfiguration : IEntityTypeConfiguration<MinhaEntidade>
{
    public void Configure(EntityTypeBuilder<MinhaEntidade> builder)
    {
        builder.ToTable("MinhaEntidade");

        builder.HasKey(e => e.Id);

        builder.Property(e => e.Nome)
            .IsRequired()
            .HasMaxLength(200);

        // Multi-tenancy: índice + filtro global
        builder.HasIndex(e => e.EmpresaId);

        // Soft Delete: filtro global
        builder.HasQueryFilter(e => !e.IsDeleted);
    }
}
```

**Registrar no ApplicationDbContext:**
```csharp
protected override void OnModelCreating(ModelBuilder modelBuilder)
{
    modelBuilder.ApplyConfiguration(new MinhaEntidadeConfiguration());
    // ... outras configurações
}
```

---

## 🔄 Fluxo de Trabalho: Dev A → Dev B

### Desenvolvedor A (cria feature)

```bash
# 1. Modifica entidade Usuario
# src/Domain/Entities/Usuario.cs
public class Usuario
{
    public Guid Id { get; set; }
    public string Nome { get; set; }
    public string Email { get; set; }  // ← NOVA PROPRIEDADE
}

# 2. Cria migration
cd backend/IControlIT.API
dotnet ef migrations add AdicionarColunaEmailUsuario \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# 3. Aplica localmente
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# 4. Testa localmente
# (backend roda, testes passam, etc.)

# 5. Commita APENAS a migration
git add src/Infrastructure/Data/Migrations/
git commit -m "feat(RF-XXX): adicionar coluna Email à tabela Usuario"
git push origin dev
```

### Desenvolvedor B (sincroniza)

```bash
# 1. Pull do código
git pull origin dev

# 2. Aplica migrations pendentes
cd backend/IControlIT.API
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext

# 3. Pronto! Banco sincronizado
# (coluna Email agora existe na tabela Usuario)
```

---

## 🚨 Checklist Antes de Commitar

**SEMPRE verificar antes de `git push`:**

- [ ] Migration foi criada com nome descritivo
- [ ] Migration aplica sem erros localmente (`dotnet ef database update`)
- [ ] Backend roda sem erros após aplicar migration
- [ ] `ApplicationDbContextModelSnapshot.cs` foi atualizado automaticamente
- [ ] `IControlIT.db` NÃO está no staging area (`git status` não mostra .db)
- [ ] Apenas arquivos `.cs` de migrations estão sendo commitados

**Comando de verificação:**
```bash
cd backend/IControlIT.API
git status

# ✅ DEVE aparecer:
# new file:   src/Infrastructure/Data/Migrations/20251114_MinhaFeature.cs
# modified:   src/Infrastructure/Data/Migrations/ApplicationDbContextModelSnapshot.cs

# ❌ NÃO DEVE aparecer:
# modified:   src/Web/IControlIT.db
```

**Se aparecer `.db` no staging:**
```bash
# Remover do staging (não commitar!)
git restore src/Web/IControlIT.db
```

---

## 🐛 Troubleshooting Comum

### Erro: "dotnet-ef: command not found"

**Causa:** Ferramentas .NET não foram restauradas

**Solução:**
```bash
cd backend/IControlIT.API
dotnet tool restore
```

---

### Erro: "More than one DbContext was found"

**Causa:** Há múltiplos DbContext no projeto (ApplicationDbContext + outros)

**Solução:** Sempre especificar `--context ApplicationDbContext`
```bash
dotnet ef migrations add MinhaFeature \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

---

### Erro: "SQLite Error 1: 'table X already exists'"

**Causa:** Banco tem estrutura mas migrations não foram registradas em `__EFMigrationsHistory`

**Solução 1: Recriar banco (DESENVOLVIMENTO apenas)**
```bash
cd backend/IControlIT.API/src/Web

# 1. Backup do banco atual
cp IControlIT.db IControlIT.db.backup-$(date +%Y%m%d-%H%M%S)

# 2. Remover banco
rm IControlIT.db

# 3. Recriar com migrations
cd ../..
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Solução 2: Marcar migrations como aplicadas (PRODUÇÃO)**
```bash
# Gerar script SQL que marca migrations como aplicadas SEM executar DDL
dotnet ef migrations script \
  --idempotent \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext \
  --output fix-migrations.sql

# Executar manualmente no banco (remove DDL, deixa só INSERT em __EFMigrationsHistory)
```

---

### Erro: "Cannot find module 'express'" (ao rodar backend)

**Causa:** Erro de comando (backend é .NET, não Node.js)

**Solução:** Comandos corretos para backend:
```bash
cd backend/IControlIT.API/src/Web
dotnet run
```

---

### Migration aplicada mas mudanças não aparecem no banco

**Causa:** Banco não foi atualizado ou está usando banco antigo

**Verificação:**
```bash
# Ver qual banco está sendo usado
cat backend/IControlIT.API/src/Web/appsettings.json | grep ConnectionString

# Listar migrations aplicadas
dotnet ef migrations list \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

**Solução:**
```bash
# Forçar atualização
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Web \
  --context ApplicationDbContext
```

---

## 📊 Estado Atual do Projeto

**Atualizado em:** 2025-01-14

### Migrations Aplicadas

**Total:** 18 migrations

```
1.  20251106012228_AddRF021Notificacoes
2.  20251106013036_AddRF017TemplateEngineBase
3.  20251106112924_AddRF007EnhancedRoleManagement
4.  20251106132940_AddRF017EngineAndJsonSchemaFields
5.  20251106184236_AddSoftDeleteToRoles
6.  20251106212520_AddRF008EmpresasFiliais
7.  20251106212936_AddRF013LocaisEnderecos
8.  20251106214522_AddRF014CategoriaManagement
9.  20251107000606_RF009_HierarquiaCorporativa
10. 20251107013315_RF015_GestaoTiposAtivos
11. 20251107124014_RF010_AddBudgetMensalToHierarquiaEntities
12. 20251107130449_RF016_GestaoMarcasModelos
13. 20251107131537_RF001_FeatureFlagsPorEmpresa_Config
14. 20251107133948_AddRF011GestaoDeCargos
15. 20251107135509_AddFlOcultaParaSistemaToFeatureFlags
16. 20251107152405_AddUC08FieldsToFeatureFlags
17. 20251107164924_AddFeatureFlagEnhancedFields
18. 20251114005812_AddEmpresasTable
```

### Estatísticas

- **Tamanho do banco:** ~3 MB (local, não commitado)
- **Tamanho das migrations:** ~200 KB (commitadas no Git)
- **Total de tabelas:** ~50 (inclui ASP.NET Identity + entidades de negócio)

---

## 🎓 Regra de Ouro

**Analogia Simples:**

| Item | Analogia | Onde fica? | Vai no Git? |
|------|----------|------------|-------------|
| **Migrations (.cs)** | Receita do bolo 📐 | `src/Infrastructure/Data/Migrations/` | ✅ SIM |
| **Banco de dados (.db)** | Bolo pronto 🎂 | `src/Web/IControlIT.db` | ❌ NÃO |

**Regra:**
- ✅ Commitar a RECEITA (migrations)
- ❌ NÃO commitar o BOLO (banco)
- ✅ Cada dev constrói seu próprio bolo seguindo a receita

---

## 📚 Links Úteis

**Documentação Oficial:**
- [Entity Framework Core Migrations](https://learn.microsoft.com/ef/core/managing-schemas/migrations/)
- [EF Core DbContext](https://learn.microsoft.com/ef/core/dbcontext-configuration/)
- [SQLite with EF Core](https://learn.microsoft.com/ef/core/providers/sqlite/)

**Documentação do Projeto:**
- [IMPORTANTE-BANCO-DE-DADOS.md](../IMPORTANTE-BANCO-DE-DADOS.md)
- [RESUMO-BANCO-DE-DADOS-GIT.md](../RESUMO-BANCO-DE-DADOS-GIT.md)
- [PADROES-CODIFICACAO-BACKEND.md](./PADROES-CODIFICACAO-BACKEND.md)
- [GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)

---

## 🆘 Suporte

**Problemas não cobertos neste guia?**

1. Consultar [IMPORTANTE-BANCO-DE-DADOS.md](../IMPORTANTE-BANCO-DE-DADOS.md) (FAQ completo)
2. Verificar [ERROS-A-EVITAR.md](../ERROS-A-EVITAR.md) (erros conhecidos)
3. Perguntar ao usuário com contexto detalhado

---

**Última Atualização:** 2025-01-14
**Versão:** 1.0
**Autor:** Claude Code (com revisão humana)

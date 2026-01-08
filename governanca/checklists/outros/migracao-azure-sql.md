# CHECKLIST: Migração Azure SQL

**Contrato:** D:\IC2_Governanca\contracts\outros\migracao-azure-sql.md
**Prompt:** D:\IC2_Governanca\prompts\outros\migracao-azure-sql.md

---

## PRÉ-EXECUÇÃO (USUÁRIO)

- [ ] **Executar `az login`** (OBRIGATÓRIO)
- [ ] Aguardar navegador abrir
- [ ] Fazer login com credenciais Azure
- [ ] Confirmar: "You have logged in"
- [ ] Validar: `az account show` funciona

**SEM ESTE PASSO, O AGENTE NÃO PODE PROSSEGUIR.**

---

## FASE 0: VALIDAÇÃO DE AUTENTICAÇÃO AZURE

- [ ] Comando `az account show` executado
- [ ] Resultado: subscription ativa exibida
- [ ] **Se falhar:** Instruir usuário a executar `az login`

---

## FASE 1: PREPARAÇÃO

### Validação de Branch

- [ ] Branch atual: `migration/azure-sql-complete`
- [ ] **Se falhar:** BLOQUEIO TOTAL

### Validação de Pré-Requisitos

- [ ] RF006 merged em dev (commit 5fc9cf91 presente)
- [ ] Migrations validadas (ZERO tipos SQLite: TEXT, INTEGER, REAL)
- [ ] Docker rodando (`docker ps` OK)
- [ ] dotnet-ef tool instalado (`dotnet ef --version`)
- [ ] Plano lido (D:\IC2\PLANO-MIGRACAO-AZURE-SQL.md)

### Backup SQLite

- [ ] Diretório criado: `.temp_ia/backup-sqlite/`
- [ ] SQLite copiado (se existe): `IControlIT-[TIMESTAMP].db`
- [ ] Validar backup criado

### Commit Inicial

- [ ] Commit realizado: `chore(infra): preparar ambiente para migração Azure SQL`
- [ ] Mensagem contém: validações, backup, próximo passo

**Se qualquer item falhar:** BLOQUEIO TOTAL

---

## FASE 2: CRIAR INFRAESTRUTURA AZURE SQL DEV

### Obter Padrão de Resource Groups

- [ ] Comando executado: `az group show --name rg-icontrolit-hom`
- [ ] Location capturada: `brazilsouth`
- [ ] Tags capturadas (se houver)

### Criar Resource Group DEV

- [ ] Comando executado: `az group create --name rg-icontrolit-dev`
- [ ] Location: `brazilsouth` (igual HOM/PRD)
- [ ] Tags aplicadas: `Environment=Development Project=IControlIT`
- [ ] Validação: `provisioningState = "Succeeded"`

**Se falhar:** BLOQUEIO - gerar relatório de falha

### Criar SQL Server DEV

- [ ] Nome gerado: `sql-icontrolit-dev-[RANDOM]` (sufixo 4 dígitos)
- [ ] Resource Group: `rg-icontrolit-dev`
- [ ] Location: `brazilsouth`
- [ ] Admin user: `sqladmin`
- [ ] Admin password definida
- [ ] Validação: `state = "Ready"`

### Configurar Firewall

- [ ] Regra criada: `AllowAzureServices` (0.0.0.0)
- [ ] IP local obtido (https://api.ipify.org)
- [ ] Regra criada: `AllowDeveloperIP` (IP obtido)
- [ ] Validação: 2 regras criadas

### Criar Database (Basic Tier)

- [ ] Nome: `IControlIT_DEV`
- [ ] Service Objective: `Basic` (5 DTUs)
- [ ] Backup Redundancy: `Local`
- [ ] Validação: `status = "Online"`
- [ ] Validação: `currentServiceObjectiveName = "Basic"`
- [ ] Validação: `maxSizeBytes = 2147483648` (2 GB)

### Gerar Connection String

- [ ] Connection string gerada
- [ ] Exibida para referência futura
- [ ] Salva em `.temp_ia/INFRA-AZURE-SQL-DEV.md`

### Documentação

- [ ] Arquivo criado: `.temp_ia/INFRA-AZURE-SQL-DEV.md`
- [ ] Contém: SQL Server name, database name, connection string
- [ ] Contém: Custo estimado (~$5/mês)

### Commit

- [ ] Commit realizado: `feat(infra): criar infraestrutura Azure SQL DEV`
- [ ] Arquivo incluído: `.temp_ia/INFRA-AZURE-SQL-DEV.md`

**Se qualquer item falhar:** ROLLBACK (deletar resource group criado)

---

## FASE 3: ATUALIZAR CÓDIGO

### appsettings.Development.json

- [ ] Arquivo lido: `D:\IC2\backend\IControlIT.API\src\Web\appsettings.Development.json`
- [ ] Connection string ANTES capturada (SQLite)
- [ ] Connection string DEPOIS aplicada (Azure SQL DEV)
- [ ] Validação: contém `sql-icontrolit-dev-XXXX.database.windows.net`

### Program.cs

- [ ] Arquivo lido: `D:\IC2\backend\IControlIT.API\src\Web\Program.cs`
- [ ] Bloco `if (builder.Environment.IsDevelopment())` identificado
- [ ] Lógica SQLite removida (linhas ~160-191)
- [ ] UseSqlServer aplicado em TODOS os ambientes
- [ ] Retry policy configurada (5 tentativas, 30s delay)
- [ ] Interceptors mantidos (auditableEntityInterceptor, etc.)

### .gitignore

- [ ] Arquivo lido: `D:\IC2\.gitignore`
- [ ] Verificar se `*.db` já existe
- [ ] Se NÃO: adicionar `*.db`, `*.db-shm`, `*.db-wal`
- [ ] Se SIM: nenhuma alteração necessária

### Commit

- [ ] Arquivos staged: appsettings.Development.json, Program.cs, .gitignore
- [ ] Commit realizado: `refactor(infra): remover lógica SQLite de Program.cs`
- [ ] Mensagem contém: mudanças, motivação

**Se qualquer item falhar:** ROLLBACK (git reset --hard HEAD~1)

---

## FASE 4: APLICAR MIGRATIONS

### Validar Build

- [ ] Comando executado: `dotnet build --no-incremental`
- [ ] Resultado: 0 erros, 0 warnings

**Se falhar:** BLOQUEIO TOTAL - reverter FASE 3

### Aplicar Migrations em DEV

- [ ] Connection string DEV preparada
- [ ] Comando executado: `dotnet ef database update --connection "[...]"`
- [ ] Resultado: migrations aplicadas sem erro

### Validar Migrations Aplicadas

- [ ] Comando executado: `dotnet ef migrations list --connection "[...]"`
- [ ] Resultado: 62 migrations com `[X] applied`
- [ ] ZERO migrations pendentes

**Se falhar:** BLOQUEIO TOTAL - reverter FASE 3 + deletar database

### Aplicar Migrations em HOM (Opcional)

- [ ] Verificar se HOM já tem migrations aplicadas
- [ ] Se SIM: pular este passo
- [ ] Se NÃO: aplicar migrations em HOM

### Aplicar Migrations em PRD (Requer Aprovação)

**Solicitar aprovação do usuário:**
- [ ] Exibir mensagem de aprovação
- [ ] Aguardar resposta: SIM/NÃO

**Se SIM:**
- [ ] Criar backup BACPAC
- [ ] Aplicar migrations em PRD
- [ ] Validar migrations aplicadas

**Se NÃO:**
- [ ] Documentar que PRD será aplicado manualmente

### Commit

- [ ] Commit realizado: `feat(infra): aplicar migrations em Azure SQL`
- [ ] Mensagem contém: resultados DEV, HOM, PRD

**Se qualquer item falhar:** ROLLBACK da fase

---

## FASE 5: MIGRAR DADOS (OPCIONAL)

### Verificar se SQLite tem Dados

- [ ] Backup SQLite localizado: `.temp_ia/backup-sqlite/IControlIT-*.db`
- [ ] Tamanho verificado (em KB)

**Se < 100KB:**
- [ ] SQLite vazio ou apenas schema
- [ ] Pular FASE 5 completamente

**Se > 100KB:**
- [ ] SQLite tem dados
- [ ] Executar migração OU repovoar via seeds

### Migração de Dados (se necessário)

- [ ] Opção escolhida: [Seeds automáticos | Migração manual]
- [ ] Se Seeds: nenhuma ação (seeds aplicam automaticamente)
- [ ] Se Manual: executar script de migração

### Commit (se executado)

- [ ] Commit realizado: `chore(data): migrar dados SQLite → Azure SQL`
- [ ] Mensagem contém: método usado, resultado

---

## FASE 6: VALIDAÇÃO COMPLETA

### Build

- [ ] Comando executado: `dotnet build --no-incremental`
- [ ] Resultado: 0 erros
- [ ] Resultado: 0 warnings

**Se falhar:** BLOQUEIO TOTAL

### Testes Unitários

- [ ] Domain.UnitTests executados
- [ ] Resultado: 5/5 passando
- [ ] Application.UnitTests executados
- [ ] Resultado: 26/26 passando

**Se qualquer teste falhar:** BLOQUEIO TOTAL

### Testes Funcionais

- [ ] Docker rodando (validado)
- [ ] Application.FunctionalTests executados
- [ ] Resultado: 23/23 passando

**Se qualquer teste falhar:** BLOQUEIO TOTAL

### Aplicação Funcional

- [ ] Aplicação iniciada: `dotnet run --project src/Web`
- [ ] Endpoint /health testado
- [ ] Resultado: 200 OK
- [ ] Endpoint /api/clientes testado (ou similar)
- [ ] Resultado: 200 OK ou 401 (auth)

**Se qualquer endpoint falhar:** BLOQUEIO TOTAL

### Commit

- [ ] Commit realizado: `test(infra): validar aplicação em Azure SQL`
- [ ] Mensagem contém: build OK, testes OK, aplicação OK

**Se qualquer validação falhar:** ROLLBACK completo

---

## FASE 7: DOCUMENTAÇÃO E LIMPEZA

### Atualizar DECISIONS.md

- [ ] Arquivo lido: `D:\IC2\DECISIONS.md`
- [ ] Seção adicionada: `[2026-01-06] Migração Completa para Azure SQL`
- [ ] Contém: Contexto, Decisão, Alternativas Rejeitadas, Resultado
- [ ] Contém: Custo estimado (~$5/mês DEV)

### Criar AZURE-SQL-MIGRATION.md

- [ ] Arquivo criado: `D:\IC2_Governanca\AZURE-SQL-MIGRATION.md`
- [ ] Contém: Resumo executivo
- [ ] Contém: Infraestrutura criada (tabela)
- [ ] Contém: Mudanças de código
- [ ] Contém: Migrations aplicadas
- [ ] Contém: Validações
- [ ] Contém: Evidências
- [ ] Contém: Próximos passos

### Mover SQLite para Backup

- [ ] Verificar se SQLite ainda está em: `src/Web/IControlIT.db`
- [ ] Se SIM: mover para `.temp_ia/backup-sqlite/`
- [ ] Se NÃO: já foi movido anteriormente

### Commit Final

- [ ] Arquivos staged: DECISIONS.md, AZURE-SQL-MIGRATION.md
- [ ] Commit realizado: `docs(infra): documentar migração completa Azure SQL`
- [ ] Mensagem contém: documentação, limpeza, evidências, próximo passo

---

## CRITÉRIO DE APROVAÇÃO FINAL

### Infraestrutura

- [ ] Resource Group DEV criado (rg-icontrolit-dev)
- [ ] SQL Server DEV criado (sql-icontrolit-dev-XXXX)
- [ ] Database DEV criado (IControlIT_DEV - Basic Tier)
- [ ] Firewall configurado (Azure Services + IP local)
- [ ] Connection string documentada

### Código

- [ ] appsettings.Development.json atualizado (Azure SQL)
- [ ] Program.cs refatorado (sem lógica SQLite)
- [ ] .gitignore atualizado (*.db)

### Migrations

- [ ] 62 migrations aplicadas em DEV (100%)
- [ ] HOM: aplicado OU já estava OU pulado
- [ ] PRD: aplicado OU documentado que será manual

### Validação

- [ ] Build: 0 erros
- [ ] Testes unitários: 31/31 passando
- [ ] Testes funcionais: 23/23 passando
- [ ] Aplicação: funcional (/health 200 OK)

### Documentação

- [ ] DECISIONS.md atualizado (D:\IC2)
- [ ] AZURE-SQL-MIGRATION.md criado (D:\IC2_Governanca)
- [ ] Infraestrutura documentada (.temp_ia/INFRA-AZURE-SQL-DEV.md)

### Commits

- [ ] FASE 1: `chore(infra): preparar ambiente`
- [ ] FASE 2: `feat(infra): criar infraestrutura`
- [ ] FASE 3: `refactor(infra): remover SQLite`
- [ ] FASE 4: `feat(infra): aplicar migrations`
- [ ] FASE 5: `chore(data): migrar dados` (opcional)
- [ ] FASE 6: `test(infra): validar aplicação`
- [ ] FASE 7: `docs(infra): documentar migração`
- [ ] **Total:** 7 commits atômicos (ou 6 se FASE 5 pulada)

### Limpeza

- [ ] SQLite em backup (.temp_ia/backup-sqlite/)
- [ ] Branch pronto para merge (migration/azure-sql-complete)

---

## APROVAÇÃO OU REPROVAÇÃO

### ✅ APROVADO

**TODOS os itens abaixo DEVEM ser verdadeiros:**

- [ ] Azure autenticado (az account show OK)
- [ ] 7 commits atômicos realizados
- [ ] Infraestrutura DEV criada (Basic Tier)
- [ ] 62 migrations aplicadas em DEV
- [ ] Build: 0 erros
- [ ] Testes: 54/54 passando (100%)
- [ ] Aplicação funcional
- [ ] Documentação completa
- [ ] SQLite em backup

### ❌ REPROVADO

**Se QUALQUER condição abaixo ocorrer:**

- [ ] Azure não autenticado (usuário não executou az login)
- [ ] Branch incorreto (não é migration/azure-sql-complete)
- [ ] Infraestrutura DEV falhou ao criar
- [ ] Migrations falharam ao aplicar
- [ ] Build com erros
- [ ] Testes falhando (< 54/54)
- [ ] Aplicação não funciona
- [ ] Documentação incompleta

**Em caso de REPROVAÇÃO:**
- PARAR imediatamente
- EXECUTAR rollback apropriado
- GERAR relatório de falha: `.temp_ia/RELATORIO-FALHA-MIGRACAO-AZURE-SQL.md`

---

## ROLLBACK (SE NECESSÁRIO)

- [ ] Branch deletado: `git branch -D migration/azure-sql-complete`
- [ ] Remote branch deletado: `git push origin --delete migration/azure-sql-complete`
- [ ] Resource Group DEV deletado: `az group delete --name rg-icontrolit-dev --yes`
- [ ] SQLite restaurado do backup (se havia)
- [ ] Relatório de rollback gerado

---

## PRÓXIMOS PASSOS (PÓS-APROVAÇÃO)

- [ ] Merge `migration/azure-sql-complete` → `dev`
- [ ] Validar em HOM (via pipeline)
- [ ] Monitorar custos Azure DEV (30 dias)
- [ ] Deletar SQLite definitivamente (após 7 dias validação)
- [ ] Configurar Managed Identity para PRD (se aplicável)

---

**LEMBRETE FINAL:** Sem `az login` prévio do usuário, NADA pode ser executado.

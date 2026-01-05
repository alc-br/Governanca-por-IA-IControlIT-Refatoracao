# COMMANDS.md
# Comandos e Scripts - Projeto IControlIT

**Versão:** 2.0.0
**Data:** 2026-01-01

Este documento centraliza todos os comandos essenciais do projeto IControlIT, incluindo comandos de desenvolvimento, testes, deploy, validação e scripts utilitários.

---

## Comandos Backend (.NET 10)

### Build e Execução

```bash
# Navegar para o projeto backend
cd D:\IC2\backend\IControlIT.API

# Build do projeto
dotnet build

# Rodar API (porta 5000/5001)
cd src\Web
dotnet run

# Build em modo Release
dotnet build -c Release

# Limpar outputs de build
dotnet clean
```

### Migrations e Banco de Dados

```bash
# Criar nova migration
dotnet ef migrations add NomeDaMigration --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Aplicar migrations (criar/atualizar banco)
dotnet ef database update --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Reverter última migration
dotnet ef database update NomeMigrationAnterior --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Remover última migration (se não aplicada)
dotnet ef migrations remove --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Gerar script SQL de migration
dotnet ef migrations script --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext --output migration.sql

# Listar migrations aplicadas
dotnet ef migrations list --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Restaurar ferramentas .NET (necessário em nova máquina)
dotnet tool restore
```

### Testes

```bash
# Rodar todos os testes
dotnet test

# Rodar testes com cobertura
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=opencover

# Rodar testes de projeto específico
dotnet test tests\Application.UnitTests\Application.UnitTests.csproj

# Rodar testes com filtro
dotnet test --filter "FullyQualifiedName~CreateEmpresa"
```

### Linting e Formatação

```bash
# Formatar código
dotnet format

# Analisar código (Roslyn analyzers)
dotnet build /p:TreatWarningsAsErrors=true
```

---

## Comandos Frontend (Angular 19)

### Build e Execução

```bash
# Navegar para o projeto frontend
cd D:\IC2\frontend\icontrolit-app

# Instalar dependências
npm install

# Rodar dev server (porta 4200)
npm start

# Build para produção
npm run build

# Build com AOT (Ahead-of-Time compilation)
npm run build -- --aot

# Servir build de produção
npm run serve:dist
```

### Testes

```bash
# Testes unitários (Jest)
npm run test

# Testes unitários em watch mode
npm run test:watch

# Testes unitários com cobertura
npm run test:coverage

# Testes E2E (Playwright)
npm run e2e

# Testes E2E em modo headless
npm run e2e:headless

# Testes E2E em modo debug
npm run e2e:debug

# Testes E2E em browser específico
npm run e2e -- --project=chromium
```

### Linting e Formatação

```bash
# Lint do código
npm run lint

# Lint com correção automática
npm run lint:fix

# Prettier format
npm run format

# Prettier check
npm run format:check
```

### i18n (Internacionalização)

```bash
# Validar traduções (verifica chaves faltando)
npm run i18n:validate

# Corrigir traduções automaticamente
npm run i18n:fix

# Extrair chaves de tradução
npm run i18n:extract

# Gerar relatório de traduções faltando
npm run i18n:report
```

---

## Comandos Git (Workflow Padrão)

### Branch Management

```bash
# Criar branch para RF
git checkout dev
git pull origin dev
git checkout -b feature/RFXXX-backend

# Criar branch para frontend
git checkout -b feature/RFXXX-frontend

# Criar branch para hotfix
git checkout main
git pull origin main
git checkout -b hotfix/RFXXX
```

### Commit e Push

```bash
# Stage arquivos
git add .

# Commit com mensagem
git commit -m "feat(RFXXX): Implementação completa backend

- Criação de entidades e DTOs
- Commands e Queries com MediatR
- Validators com FluentValidation
- Testes unitários com 80% cobertura
- Seeds e permissões RBAC

Refs: RFXXX"

# Push para origin
git push origin feature/RFXXX-backend

# Push com upstream (primeira vez)
git push -u origin feature/RFXXX-backend
```

### Merge e Cleanup

```bash
# Merge para dev (após aprovação PR)
git checkout dev
git pull origin dev
git merge feature/RFXXX-backend
git push origin dev

# Deletar branch local
git branch -d feature/RFXXX-backend

# Deletar branch remoto
git push origin --delete feature/RFXXX-backend
```

---

## Comandos de Validação de Documentação

### Validadores Python

```bash
# Validar cobertura RF → UC → TC
python D:\IC2_Governanca\tools\docs\validator-rf-uc.py RFXXX

# Validar separação RF / RL
python D:\IC2_Governanca\tools\docs\validator-rl.py RFXXX

# Validar governança completa
python D:\IC2_Governanca\tools\docs\validator-governance.py RFXXX

# Validar user stories
python D:\IC2_Governanca\tools\docs\validator-user-stories.py RFXXX

# Validar STATUS.yaml
python D:\IC2_Governanca\tools\docs\validator-status.py RFXXX
```

### Exit Codes Obrigatórios

Todos os validadores retornam exit codes:
- `0` - Validação APROVADA (pode prosseguir)
- `1` - Validação REPROVADA (bloqueio de execução)

**REGRA CRÍTICA:** Código de saída ≠ 0 BLOQUEIA execução do próximo contrato.

---

## Comandos de Sincronização DevOps

```bash
# Sincronizar RF com Azure DevOps
python D:\IC2_Governanca\tools\devops-sync\sync-rf.py RFXXX

# Sincronizar User Stories
python D:\IC2_Governanca\tools\devops-sync\sync-user-stories.py RFXXX

# Sincronizar STATUS.yaml → Board
python D:\IC2_Governanca\tools\devops-sync\sync-status.py RFXXX

# Criar Feature no Azure DevOps
python D:\IC2_Governanca\tools\devops-sync\create-feature.py RFXXX

# Mover work item de coluna
python D:\IC2_Governanca\tools\devops-sync\move-workitem.py RFXXX "In Progress"
```

---

## Comandos de Deploy

### Azure CLI

```bash
# Login no Azure
az login

# Selecionar subscription
az account set --subscription "IControlIT-Production"

# Listar app services
az webapp list --resource-group IControlIT-RG --output table

# Deploy backend
az webapp deployment source config-zip --resource-group IControlIT-RG --name icontrolit-api --src backend.zip

# Deploy frontend
az webapp deployment source config-zip --resource-group IControlIT-RG --name icontrolit-app --src frontend.zip

# Ver logs de aplicação
az webapp log tail --resource-group IControlIT-RG --name icontrolit-api

# Restart aplicação
az webapp restart --resource-group IControlIT-RG --name icontrolit-api
```

### Rollback

```bash
# Listar deployments
az webapp deployment list --resource-group IControlIT-RG --name icontrolit-api --output table

# Rollback para deployment anterior
az webapp deployment slot swap --resource-group IControlIT-RG --name icontrolit-api --slot staging --target-slot production
```

---

## Comandos de Debugging

### Backend (.NET)

```bash
# Rodar com logging detalhado
cd D:\IC2\backend\IControlIT.API\src\Web
dotnet run --verbosity detailed

# Rodar com debugger anexado
dotnet run --launch-profile "IControlIT.Web (Debug)"

# Ver logs em tempo real
tail -f D:\IC2\backend\IControlIT.API\logs\app.log

# Verificar endpoints disponíveis
curl http://localhost:5000/api/health
curl http://localhost:5000/api/swagger/index.html
```

### Frontend (Angular)

```bash
# Rodar com sourcemaps detalhados
npm start -- --source-map

# Build de desenvolvimento com sourcemaps
npm run build -- --source-map

# Analisar bundle size
npm run build -- --stats-json
npx webpack-bundle-analyzer dist/icontrolit-app/stats.json

# Verificar erros de linting sem parar build
npm run lint -- --force

# Debug de testes E2E
npm run e2e:debug
```

### Database Debugging

```bash
# Conectar ao SQLite (dev)
sqlite3 D:\IC2\backend\IControlIT.API\src\Web\IControlIT.db

# Queries úteis
.tables                          # Listar tabelas
.schema Usuario                  # Ver schema de tabela
SELECT * FROM Usuario LIMIT 10;  # Query básica

# Exportar dados
.output usuarios.sql
.dump Usuario
.output stdout

# Sair
.quit
```

---

## Scripts Utilitários

### Setup Inicial

```bash
# Setup completo do ambiente
powershell -ExecutionPolicy Bypass -File D:\IC2\setup-ambiente.ps1

# Verificar ambiente
powershell -ExecutionPolicy Bypass -File D:\IC2\verify-environment.ps1

# Exportar configuração do ambiente
powershell -ExecutionPolicy Bypass -File D:\IC2\export-ambiente.ps1

# Importar configuração do ambiente
powershell -ExecutionPolicy Bypass -File D:\IC2\import-ambiente.ps1
```

### Limpeza e Manutenção

```bash
# Limpar node_modules e reinstalar
cd D:\IC2\frontend\icontrolit-app
rmdir /s /q node_modules
npm install

# Limpar bin/obj do backend
cd D:\IC2\backend\IControlIT.API
dotnet clean
rmdir /s /q src\Web\bin
rmdir /s /q src\Web\obj

# Limpar arquivos temporários do projeto
rmdir /s /q D:\IC2\.temp_ia
mkdir D:\IC2\.temp_ia
```

### Geração de Relatórios

```bash
# Relatório de cobertura de testes (backend)
cd D:\IC2\backend\IControlIT.API
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=html /p:CoverletOutput=./coverage/
start coverage\index.html

# Relatório de cobertura de testes (frontend)
cd D:\IC2\frontend\icontrolit-app
npm run test:coverage
start coverage\index.html

# Relatório de auditoria de conformidade
python D:\IC2_Governanca\tools\docs\audit-rf.py RFXXX --output D:\IC2\relatorios\
```

---

## Comandos de Skills do Claude Code

Estes comandos são executados via Skill tool do Claude Code:

### /start-rf
**Descrição:** Iniciar trabalho em um Requisito Funcional
**Uso:** `/start-rf`
**Resultado:** Valida documentação, cria branch, verifica portas, cria checklist

### /validate-rf
**Descrição:** Validar build, testes e documentação completos de um RF
**Uso:** `/validate-rf`
**Resultado:** Executa builds, testes, valida STATUS.yaml, gera relatório

### /deploy-rf
**Descrição:** Deploy de RF para HOM ou PRD
**Uso:** `/deploy-rf`
**Resultado:** Valida pré-requisitos, executa deploy, atualiza STATUS.yaml

### /audit-rf
**Descrição:** Executar auditoria de conformidade de um RF
**Uso:** `/audit-rf`
**Resultado:** Analisa código vs especificação, gera relatório de gaps

### /fix-build
**Descrição:** Corrigir erros de compilação automaticamente
**Uso:** `/fix-build`
**Resultado:** Detecta erros, adiciona imports, instala dependências

### /sync-devops
**Descrição:** Sincronizar STATUS.yaml com Azure DevOps
**Uso:** `/sync-devops`
**Resultado:** Move work items, cria user stories, atualiza board

### /sync-todos
**Descrição:** Sincronizar Lista de Tarefas
**Uso:** `/sync-todos`
**Resultado:** Atualiza TodoWrite com work items do Azure DevOps

---

## Ordem de Execução Recomendada

### Workflow Completo de RF

```bash
# 1. Iniciar trabalho no RF
/start-rf

# 2. Implementar backend
cd backend/IControlIT.API
dotnet build
dotnet test

# 3. Implementar frontend
cd frontend/icontrolit-app
npm start
npm run test
npm run e2e

# 4. Validar RF completo
/validate-rf

# 5. Auditar conformidade (opcional)
/audit-rf

# 6. Deploy para HOM
/deploy-rf

# 7. Sincronizar DevOps
/sync-devops

# 8. Após aprovação, deploy para PRD
/deploy-rf
```

---

## Troubleshooting Comum

### Erro: "dotnet ef not found"
```bash
dotnet tool restore
```

### Erro: "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Verificar portas em uso
netstat -ano | findstr :5000
netstat -ano | findstr :4200
```

### Erro: "npm ERR! EINTEGRITY"
```bash
npm cache clean --force
rmdir /s /q node_modules
rmdir /s /q package-lock.json
npm install
```

### Erro: "Migration already applied"
```bash
# Reverter migration
dotnet ef database update MigracaoAnterior --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext

# Remover migration
dotnet ef migrations remove --project src\Infrastructure --startup-project src\Web --context ApplicationDbContext
```

---

## Referências

- **ARCHITECTURE.md** - Stack tecnológico, padrões arquiteturais
- **CONVENTIONS.md** - Convenções de nomenclatura e código
- **COMPLIANCE.md** - Regras de validação e conformidade
- **DECISIONS.md** - Decisões arquiteturais tomadas
- **tools/README.md** - Documentação completa de ferramentas

---

**Última Atualização:** 2026-01-01
**Versão:** 2.0.0 - Redistribuição cirúrgica do D:\IC2\CLAUDE.md

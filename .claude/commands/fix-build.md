---
description: Corrigir erros de compilação automaticamente
allowed-tools: Read, Grep, Bash, Edit, TodoWrite
---

# Corrigir Build

Corrige erros de compilação de backend e frontend automaticamente.

## Instruções

1. **Detectar Erros de Build**

   **Backend:**
   ```bash
   cd backend/IControlIT.Api
   dotnet build 2>&1 | tee build-errors.txt
   ```

   **Frontend:**
   ```bash
   cd frontend/icontrolit-app
   npm run build 2>&1 | tee build-errors.txt
   ```

2. **Analisar Erros**

   Ler `build-errors.txt` e identificar:
   - Erros de sintaxe
   - Imports faltantes
   - Dependências ausentes
   - Conflitos de versão

3. **Correções Automáticas**

   **Missing imports (C#):**
   ```csharp
   // Se erro: 'DbContext' not found
   // Adicionar: using Microsoft.EntityFrameworkCore;
   ```

   **Missing dependencies (npm):**
   ```bash
   npm install <pacote-faltante>
   ```

   **Version conflicts:**
   ```bash
   # Backend
   dotnet clean
   dotnet restore
   dotnet build

   # Frontend
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

4. **Re-buildar**

   Após correções, executar build novamente:
   ```bash
   # Backend
   dotnet build --no-restore

   # Frontend
   npm run build
   ```

5. **Criar Checklist**

   - [ ] Erros identificados
   - [ ] Correções aplicadas
   - [ ] Build executado novamente
   - [ ] Build OK (0 erros)

6. **Informar Resultado**

   **Se build OK:**
   ```
   ✅ Build corrigido com sucesso

   🔧 Correções aplicadas:
   - Adicionado using Microsoft.EntityFrameworkCore
   - Instalado @angular/common@19.0.0

   ✅ Build:
   - Backend: 0 errors, 0 warnings
   - Frontend: 0 errors, 0 warnings
   ```

   **Se build ainda falha:**
   ```
   ❌ Build ainda com erros

   ❌ Erros restantes:
   - error CS0246: Type 'IActionResult' not found

   🔍 Análise:
   [Explicar causa do erro]

   💡 Solução Manual Necessária:
   [Descrever o que fazer]
   ```

## Erros Comuns

### Backend (.NET)

| Erro | Causa | Solução |
|------|-------|---------|
| CS0246: Type not found | Using faltando | Adicionar using correto |
| CS0103: Name does not exist | Variável não declarada | Declarar variável |
| CS1061: Does not contain definition | Método inexistente | Verificar nome do método |

### Frontend (Angular)

| Erro | Causa | Solução |
|------|-------|---------|
| Cannot find module | Pacote não instalado | npm install |
| NG8001: Unknown element | Componente não importado | Adicionar em imports |
| NG2003: No provider for | Serviço não fornecido | Adicionar em providers |

## Notas

- Fix-build corrige erros **triviais** automaticamente
- Erros **complexos** requerem análise manual
- Sempre re-buildar após correções

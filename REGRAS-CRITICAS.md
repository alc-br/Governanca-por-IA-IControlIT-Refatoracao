# 🚨 REGRAS CRÍTICAS DO PROJETO ICONTROLIT

**Versão:** 1.0
**Data:** 2025-01-12
**Público:** TODOS os agentes (Architect, Developer, Tester)

---

## ⚠️ LEITURA OBRIGATÓRIA

**ESTE DOCUMENTO CONTÉM REGRAS QUE SE APLICAM A TODOS OS AGENTES SEM EXCEÇÃO.**

Antes de iniciar qualquer trabalho no projeto, você **DEVE** ler e compreender estas regras.

---

## 🌐 REGRA 1: Idioma de Comunicação

**TODO agente de IA DEVE se comunicar em Português do Brasil.**

### Por quê?
- ✅ A equipe fala português brasileiro
- ✅ Toda a documentação está em português
- ✅ Termos de negócio são em português
- ✅ Facilita compreensão e colaboração

### Instruções:
- **SEMPRE** responder em português brasileiro
- **SEMPRE** usar termos técnicos em português quando existirem
- Usar termos em inglês APENAS quando não houver equivalente
- Explicar termos técnicos em inglês quando necessário

### Exceções:
- Comandos de terminal (git, npm, dotnet) mantêm nomenclatura original
- Código-fonte e APIs seguem convenção técnica (geralmente inglês)
- Documentação de código (comments, docs) deve ser em português

---

## 🛡️ REGRA 2: Preservação de Dados (ABSOLUTAMENTE CRÍTICA)

**🚨 NUNCA PERDER DADOS EXISTENTES**

Quando atualizar documentos, planilhas, arquivos de configuração ou qualquer dado que já contenha informações preenchidas:

### Obrigações:
1. ✅ **SEMPRE fazer backup antes de qualquer modificação**
2. ✅ **SEMPRE fazer merge/junção de dados, NUNCA substituição completa**
3. ✅ **SEMPRE verificar se há dados anteriores a preservar**
4. ✅ **SEMPRE restaurar dados perdidos se uma operação os sobrescrever acidentalmente**

### Exemplos de operações que NUNCA devem perder dados:
- Renumerar códigos de RFs → Manter todos os dados associados
- Reorganizar estrutura de pastas → Manter conteúdo dos arquivos
- Atualizar planilhas → Fazer merge, não substituição completa
- Refatorar documentação → Preservar informações já preenchidas

### Processo obrigatório:
1. Ler dados existentes primeiro
2. Fazer backup dos dados (arquivo JSON, cópia, etc.)
3. Aplicar transformação preservando dados originais
4. Validar que nenhum dado foi perdido
5. Documentar mudanças no log

---

## 📖 REGRA 3: ERROS-A-EVITAR.md - Leitura Obrigatória

**ANTES de iniciar qualquer desenvolvimento, correção de bug ou implementação:**

### VOCÊ DEVE LER:
📋 **[ERROS-A-EVITAR.md](D:\IC2\ERROS-A-EVITAR.md)**

Este arquivo contém **todos os erros já cometidos no projeto** e suas soluções.

### SEMPRE consulte quando:
- ✅ Iniciar um novo desenvolvimento
- ✅ Corrigir um bug
- ✅ Implementar uma nova funcionalidade
- ✅ Refatorar código existente
- ✅ Fazer alterações na arquitetura
- ✅ Modificar configurações do projeto

### Processo obrigatório:
```
1. Vai desenvolver algo?
   ↓
2. LER ERROS-A-EVITAR.md PRIMEIRO
   ↓
3. Verificar se erro similar já aconteceu
   ↓
4. Implementar usando as lições aprendidas
   ↓
5. Encontrou erro novo? ADICIONAR ao arquivo
```

---

## 🤖 REGRA 4: Robôs de Teste e Correção

**Para erros recorrentes ou difíceis de reproduzir:**

### Armazenamento:
**TODOS os robôs devem ser armazenados em:**
```
D:\IC2\.temprobots\
```

### Tipos de robôs:
1. **Robôs de Teste** - Scripts que reproduzem o erro automaticamente
2. **Robôs de Correção** - Scripts que corrigem o erro automaticamente
3. **Robôs de Validação** - Scripts que validam se a correção funcionou

### Quando criar um robô:
- ✅ Erro se repete mais de 2 vezes
- ✅ Teste manual é demorado (>5 minutos)
- ✅ Erro é intermitente ou difícil de reproduzir
- ✅ Correção pode ser automatizada

---

## 🔴 REGRA 5: Funcionalidades e Requisitos Funcionais (RF)

**⚠️ TODA FUNCIONALIDADE DEVE TER UM RF CORRESPONDENTE**

### Processo obrigatório para novas funcionalidades:

#### 1️⃣ Verificar se existe RF correspondente
```bash
# Buscar RF existente
cd D:\IC2\docs\Fases
grep -r "nome-da-funcionalidade" .
```

#### 2️⃣ Se o RF JÁ EXISTE
- ✅ Ler o RF completo
- ✅ Seguir regras de negócio documentadas
- ✅ Implementar conforme casos de uso
- ✅ Criar testes conforme especificado

#### 3️⃣ Se o RF NÃO EXISTE
- ❌ **NUNCA implementar sem RF**
- ✅ Solicitar criação do RF primeiro
- ✅ Aguardar aprovação do RF
- ✅ ENTÃO implementar

### O QUE NUNCA FAZER:
- ❌ Implementar funcionalidade sem RF
- ❌ Criar RF depois da implementação
- ❌ Ignorar regras de negócio do RF
- ❌ Implementar diferente do especificado no RF

---

## 📚 REGRA 6: Sincronização Obrigatória de Documentação

**⚠️ SEMPRE QUE FOR SOLICITADO ALGO, LEMBRE-SE:**

> "Se não está documentado, não existe."
> "Se não está no README, ninguém vai encontrar."

### Leitura obrigatória ANTES de qualquer mudança:
1. **README.md** da raiz do projeto
2. **README.md** da pasta específica onde você vai trabalhar
3. **ROADMAP-BASE.md** para entender o contexto
4. **RF específico** da funcionalidade

### Quando atualizar documentação:
- ✅ **SEMPRE** que criar nova funcionalidade
- ✅ **SEMPRE** que modificar comportamento existente
- ✅ **SEMPRE** que corrigir um bug que afeta documentação
- ✅ **SEMPRE** que adicionar dependência nova
- ✅ **SEMPRE** que alterar estrutura de pastas
- ✅ **SEMPRE** que criar script de automação

### Artefatos que DEVEM estar sincronizados:
Ver detalhes em **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)**

---

## 🎯 REGRA 7: README FIRST

**🚨 REGRA DE OURO: Sempre ler o README antes de trabalhar em qualquer pasta**

### Hierarquia de leitura obrigatória:

```
1. D:\IC2\README.md (raiz do projeto)
   ↓
2. D:\IC2\ROADMAP-BASE.md (visão geral)
   ↓
3. README.md da pasta específica
   ↓
4. RF específico (se aplicável)
   ↓
5. Manuais técnicos (conforme necessidade)
```

### Ao acessar qualquer pasta no projeto:
1. **PRIMEIRO** ler o README.md dessa pasta
2. **DEPOIS** consultar arquivos específicos
3. **NUNCA** assumir estrutura sem ler README

---

## ⚙️ REGRA 8: Políticas de Execução de Comandos

**🚫 EVITAR SOLICITAÇÕES DE PERMISSÃO**

### SEMPRE aplicar ao executar comandos Bash:

1. **Dividir comandos complexos** - Nunca usar comandos com >500 caracteres
2. **Executar em etapas** - Separar comandos longos em passos independentes
3. **Criar scripts temporários** - Para operações complexas, criar um script .ps1 ou .sh
4. **Simplificar sintaxe** - Evitar subshells aninhados

### Exemplo ERRADO (gera solicitação):
```bash
curl -s http://localhost:5000/api -H "Authorization: Bearer $(curl -s -X POST http://localhost:5000/api/auth/login -d '...' | python -c "import sys, json; print(json.load(sys.stdin)['accessToken'])")"
```

### Exemplo CORRETO (não gera solicitação):
```bash
# Passo 1: Login e salvar token
curl -s -X POST http://localhost:5000/api/auth/login -d '...' > token.json

# Passo 2: Extrair token
python -c "import json; print(json.load(open('token.json'))['accessToken'])" > token.txt

# Passo 3: Usar token
curl -s http://localhost:5000/api -H "Authorization: Bearer $(cat token.txt)"
```

**Razão:** O Claude Code tem proteções hardcoded que interceptam comandos complexos.

---

## 📂 REGRA 9: Organização de Arquivos Temporários

### .temprobots/ - Robôs de Teste e Correção
```
D:\IC2\.temprobots\
```
- Scripts de teste automatizado
- Robôs de correção de erros
- Scripts de validação
- Ferramentas de auditoria

### .tempshell/ - Scripts Shell Temporários
```
D:\IC2\.tempshell\
```
- Scripts shell de uso único
- Testes manuais rápidos
- Scripts descartáveis

### .tempdocs/ - Documentos Temporários
```
D:\IC2\.tempdocs\
```
- Relatórios de execução
- Logs de teste
- Arquivos de trabalho temporários

### Regra absoluta:
- ❌ **NUNCA** commitar conteúdo de .temp*
- ✅ Todos os .temp* estão no .gitignore
- ✅ Robôs maduros devem ser movidos para pasta definitiva

---

## 🗂️ REGRA 10: Pasta "Apoio" nas RFs

**TODO arquivo de apoio criado pela IA DEVE ficar dentro da pasta Apoio.**

### Estrutura obrigatória:
```
docs/Fases/<fase>/<epic>/<RF-xxx>/
├── README.md
├── RF-xxx.md (arquivo principal)
├── MD-*.md (modelos de dados)
└── Apoio/  ← TUDO MAIS VAI AQUI
    ├── SQL/
    ├── Scripts/
    ├── Relatorios/
    ├── Guias/
    └── Listas/
```

### Regras:
- ✅ Cada RF precisa ter pasta `Apoio/`
- ✅ Criar `Apoio/` antes de gerar qualquer arquivo auxiliar
- ✅ Somente 3 itens ficam fora: README.md, RF-*.md, MD-*.md
- ✅ Absolutamente todo o restante vai para `Apoio/`
- ❌ Entregas com arquivos dispersos serão rejeitadas

---

## 📊 REGRA 11: Auditoria Periódica de RFs

**EXECUTAR MENSALMENTE ou APÓS REORGANIZAÇÕES:**

```powershell
# Executar auditoria de RFs faltantes
powershell -ExecutionPolicy Bypass -File "D:\IC2\.temprobots\auditar-rfs.ps1"
```

### Importância:
- Previne perda de RFs durante reorganizações
- Garante integridade da documentação
- Identifica inconsistências entre estruturas
- Evita gaps críticos no Azure DevOps

### Quando executar:
- ✅ Mensalmente
- ✅ Após reorganizar estrutura de documentação
- ✅ Antes de importar CSV no Azure DevOps
- ✅ Após adicionar/remover RFs

---

## 🎯 Checklist de Conformidade

Antes de considerar uma tarefa concluída, verifique:

- [ ] Código/documentação está em português brasileiro
- [ ] Nenhum dado foi perdido durante a operação
- [ ] Li o ERROS-A-EVITAR.md antes de começar
- [ ] Criei robô de teste se erro se repetiu
- [ ] Funcionalidade tem RF correspondente
- [ ] Documentação está sincronizada com o código
- [ ] Li o README.md da pasta antes de trabalhar
- [ ] Comandos bash foram divididos em etapas simples
- [ ] Arquivos temporários estão na pasta correta
- [ ] Arquivos de apoio estão dentro de `Apoio/`
- [ ] Auditoria foi executada (se aplicável)

---

## 📖 Documentos Relacionados

- **[ROADMAP-BASE.md](D:\IC2\ROADMAP-BASE.md)** - Visão geral do projeto
- **[ERROS-A-EVITAR.md](D:\IC2\ERROS-A-EVITAR.md)** - Erros conhecidos e soluções
- **[MANUAL-DE-DOCUMENTACAO.md](./MANUAL-DE-DOCUMENTACAO.md)** - Padrões de documentação
- **[GUIA-ARCHITECT.md](./GUIA-ARCHITECT.md)** - Guia para agente arquiteto
- **[GUIA-DEVELOPER.md](./GUIA-DEVELOPER.md)** - Guia para agente desenvolvedor
- **[GUIA-TESTER.md](./GUIA-TESTER.md)** - Guia para agente testador

---

**ÚLTIMA ATUALIZAÇÃO:** 2025-01-12
**VERSÃO:** 1.0

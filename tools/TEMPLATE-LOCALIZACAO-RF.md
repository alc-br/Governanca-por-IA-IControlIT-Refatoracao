# TEMPLATE: Seção de Localização de Arquivos RF

**Versão:** 1.0
**Data:** 2026-01-13
**Uso:** Copiar esta seção para contratos/prompts que trabalham com RFs

---

## 📁 LOCALIZAÇÃO DOS ARQUIVOS

### IMPORTANTE: Localizar Arquivos ANTES de Ler

**REGRA OBRIGATÓRIA:** SEMPRE localizar o diretório do RF usando `find` ANTES de tentar ler arquivos.

**NUNCA use:**
- ❌ Glob com padrão genérico (`**/RFXXX.md`)
- ❌ Tentativas de adivinhar caminho

**SEMPRE use:**
- ✅ `find` com caminho base completo
- ✅ Validar que diretório existe antes de prosseguir

### Estrutura de Diretórios

**Todos os RFs seguem a estrutura:**
```
D:\IC2_Governanca\documentacao\
  └── Fase-{N}-{Nome-Fase}/
      └── EPIC{NNN}-{Categoria}-{Nome-Epic}/
          └── RF{NNN}-{Nome-RF}/
              ├── RF{NNN}.md       ← Requisito Funcional (Markdown)
              ├── RF{NNN}.yaml     ← Requisito Funcional (YAML)
              ├── UC-RF{NNN}.yaml  ← Casos de Uso
              ├── RL-RF{NNN}.yaml  ← Regras de Negócio
              ├── WF-RF{NNN}.md    ← Wireframes
              ├── MD-RF{NNN}.yaml  ← Modelo de Dados
              ├── TC-RF{NNN}.yaml  ← Casos de Teste
              ├── MT-RF{NNN}.yaml  ← Massa de Teste
              ├── CN-RF{NNN}.yaml  ← Cenários de Teste
              └── STATUS.yaml      ← Status da Execução
```

**Exemplo RF007:**
```
D:\IC2_Governanca\documentacao\Fase-1-Sistema-Base\EPIC001-SYS-Sistema-Infraestrutura\RF007-Login-e-Autenticacao\RF007.md
```

### Comando de Localização Rápida (OBRIGATÓRIO)

**Passo 0: Localizar diretório do RF (SEMPRE PRIMEIRO)**

```bash
# Localizar diretório do RF
RF_DIR=$(find D:/IC2_Governanca/documentacao/ -type d -name "RFXXX*" | head -1)

# Validar que diretório foi encontrado
if [ -z "$RF_DIR" ]; then
    echo "ERRO: RF não encontrado"
    exit 1
fi

echo "Diretório encontrado: $RF_DIR"

# Listar arquivos disponíveis
ls -1 "$RF_DIR"
```

**Exemplo para RF007:**
```bash
RF_DIR=$(find D:/IC2_Governanca/documentacao/ -type d -name "RF007*" | head -1)
echo "Diretório: $RF_DIR"
ls -1 "$RF_DIR"
```

**Output esperado:**
```
Diretório: D:/IC2_Governanca/documentacao/Fase-1-Sistema-Base/EPIC001-SYS-Sistema-Infraestrutura/RF007-Login-e-Autenticacao
MD-RF007.yaml
RF007.md
RF007.yaml
RL-RF007.md
RL-RF007.yaml
STATUS.yaml
UC-RF007.md
UC-RF007.yaml
WF-RF007.md
```

### Utilitário de Localização (RECOMENDADO)

**Use o script de localização rápida:**

```bash
# Localizar RF007 usando utilitário
bash D:/IC2_Governanca/tools/find-rf.sh RF007
```

**Output esperado:**
```
✅ RF localizado com sucesso!

📁 Diretório: .../RF007-Login-e-Autenticacao

📄 Arquivos disponíveis:
MD-RF007.yaml
RF007.md
RF007.yaml
RL-RF007.md
UC-RF007.md
WF-RF007.md
STATUS.yaml

📌 Caminhos completos:
  RF.md   : .../RF007.md
  RF.yaml : .../RF007.yaml
  UC.yaml : .../UC-RF007.yaml
  RL.yaml : .../RL-RF007.yaml
```

---

## ONDE INSERIR ESTE TEMPLATE

**Inserir APÓS:**
- Seção de título/descrição do contrato/prompt
- Instruções iniciais

**Inserir ANTES:**
- Seções de validação/execução
- Checklists
- Passos do contrato

**Exemplo:**

```markdown
# Contrato de Criação de RF

## Objetivo
...

## 📁 LOCALIZAÇÃO DOS ARQUIVOS
[INSERIR TEMPLATE AQUI]

## Passos de Execução
...
```

---

**Mantido por:** Time de Arquitetura IControlIT
**Última Atualização:** 2026-01-13
**Versão:** 1.0

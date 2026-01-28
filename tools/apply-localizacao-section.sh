#!/bin/bash

# apply-localizacao-section.sh - Aplicar seção de localização em contratos/prompts
# Versão: 1.0
# Data: 2026-01-13

# ==================================================
# CONFIGURAÇÃO
# ==================================================

BASE_DIR="D:/IC2_Governanca/governanca"
TEMPLATE_FILE="D:/IC2_Governanca/tools/TEMPLATE-LOCALIZACAO-RF.md"
BACKUP_DIR="D:/IC2/.temp_ia/backup-localizacao-$(date +%Y%m%d-%H%M%S)"

# Criar backup
mkdir -p "$BACKUP_DIR"

# ==================================================
# ARQUIVOS A PROCESSAR
# ==================================================

ARQUIVOS=(
    # Contratos de execução
    "contracts/documentacao/execucao/rf-criacao.md"
    "contracts/documentacao/execucao/uc-criacao.md"
    "contracts/documentacao/execucao/uc-adequacao.md"
    "contracts/documentacao/execucao/tc-criacao.md"
    "contracts/documentacao/execucao/mt-criacao.md"
    "contracts/documentacao/execucao/mt-tc-criacao.md"
    "contracts/documentacao/execucao/wf-criacao.md"
    "contracts/documentacao/execucao/md-criacao.md"
    "contracts/documentacao/execucao/aditivo.md"

    # Contratos de validação
    "contracts/documentacao/validacao/rf.md"
    "contracts/documentacao/validacao/uc.md"
    "contracts/documentacao/validacao/wf.md"
    "contracts/documentacao/validacao/wf-md.md"
    "contracts/documentacao/validacao/md.md"
    "contracts/documentacao/validacao/mt-tc.md"
    "contracts/documentacao/validacao/aditivo.md"

    # Prompts de execução
    "prompts/documentacao/execucao/rf-criacao.md"
    "prompts/documentacao/execucao/uc-criacao.md"
    "prompts/documentacao/execucao/uc-adequacao.md"
    "prompts/documentacao/execucao/tc-criacao.md"
    "prompts/documentacao/execucao/mt-tc-criacao.md"
    "prompts/documentacao/execucao/wf-criacao.md"
    "prompts/documentacao/execucao/md-criacao.md"
    "prompts/documentacao/execucao/aditivo.md"

    # Prompts de validação
    # prompts/documentacao/validacao/rf.md (já atualizado manualmente)
    "prompts/documentacao/validacao/uc.md"
    "prompts/documentacao/validacao/wf.md"
    "prompts/documentacao/validacao/wf-md.md"
    "prompts/documentacao/validacao/md.md"
    "prompts/documentacao/validacao/mt-tc.md"
    "prompts/documentacao/validacao/aditivo.md"
)

# ==================================================
# SEÇÃO DE LOCALIZAÇÃO (extraída do template)
# ==================================================

read -r -d '' SECAO_LOCALIZACAO << 'EOF'

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
EOF

# ==================================================
# FUNÇÃO: APLICAR SEÇÃO
# ==================================================

aplicar_secao() {
    local arquivo="$1"
    local caminho_completo="$BASE_DIR/$arquivo"

    # Verificar se arquivo existe
    if [ ! -f "$caminho_completo" ]; then
        echo "⚠️  SKIP: $arquivo (não existe)"
        return
    fi

    # Verificar se já possui a seção
    if grep -q "LOCALIZAÇÃO DOS ARQUIVOS" "$caminho_completo"; then
        echo "⏭️  SKIP: $arquivo (já possui seção)"
        return
    fi

    # Fazer backup
    cp "$caminho_completo" "$BACKUP_DIR/$(basename $arquivo)"

    # Inserir seção após a primeira linha de separador "---"
    # Procurar primeira linha "---" (ignorando as primeiras 5 linhas de cabeçalho)
    linha_separador=$(tail -n +6 "$caminho_completo" | grep -n "^---$" | head -1 | cut -d: -f1)

    if [ -z "$linha_separador" ]; then
        # Se não encontrar "---", inserir após linha 10 (cabeçalho típico)
        echo "⚠️  WARN: $arquivo (sem separador ---, inserindo após linha 10)"
        linha_separador=5
    fi

    # Ajustar linha (compensar tail -n +6)
    linha_insercao=$((linha_separador + 5))

    # Inserir seção
    {
        head -n "$linha_insercao" "$caminho_completo"
        echo "$SECAO_LOCALIZACAO"
        tail -n +"$((linha_insercao + 1))" "$caminho_completo"
    } > "${caminho_completo}.tmp"

    mv "${caminho_completo}.tmp" "$caminho_completo"

    echo "✅ APLICADO: $arquivo"
}

# ==================================================
# PROCESSAR ARQUIVOS
# ==================================================

echo "=========================================="
echo "APLICAÇÃO DE SEÇÃO DE LOCALIZAÇÃO"
echo "=========================================="
echo ""
echo "Backup em: $BACKUP_DIR"
echo ""

total=0
aplicados=0
skip=0

for arquivo in "${ARQUIVOS[@]}"; do
    total=$((total + 1))
    aplicar_secao "$arquivo"
    if [[ $? -eq 0 ]]; then
        if grep -q "LOCALIZAÇÃO DOS ARQUIVOS" "$BASE_DIR/$arquivo"; then
            aplicados=$((aplicados + 1))
        else
            skip=$((skip + 1))
        fi
    fi
done

echo ""
echo "=========================================="
echo "RESUMO"
echo "=========================================="
echo "Total de arquivos: $total"
echo "Aplicados: $aplicados"
echo "Ignorados (já possuem): $skip"
echo ""
echo "Backup: $BACKUP_DIR"
echo "=========================================="

exit 0

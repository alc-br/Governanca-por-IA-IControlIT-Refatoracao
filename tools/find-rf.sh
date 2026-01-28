#!/bin/bash

# find-rf.sh - Utilitário para localizar arquivos de RF
# Versão: 1.0
# Data: 2026-01-13
# Uso: bash find-rf.sh RFXXX

# ==================================================
# CONFIGURAÇÃO
# ==================================================

BASE_DIR="D:/IC2_Governanca/documentacao"
RF_ID=$1

# ==================================================
# VALIDAÇÃO DE ENTRADA
# ==================================================

if [ -z "$RF_ID" ]; then
    echo "❌ ERRO: RF não especificado"
    echo ""
    echo "Uso: bash find-rf.sh RFXXX"
    echo ""
    echo "Exemplos:"
    echo "  bash find-rf.sh RF001"
    echo "  bash find-rf.sh RF007"
    echo "  bash find-rf.sh RF025"
    exit 1
fi

# ==================================================
# LOCALIZAR DIRETÓRIO DO RF
# ==================================================

RF_DIR=$(find "$BASE_DIR" -type d -name "${RF_ID}*" 2>/dev/null | head -1)

if [ -z "$RF_DIR" ]; then
    echo "❌ ERRO: RF $RF_ID não encontrado"
    echo ""
    echo "Estrutura esperada:"
    echo "  $BASE_DIR/Fase-X/EPICXXX/RFXXX/"
    echo ""
    echo "Verifique se o RF existe na estrutura de documentação."
    exit 1
fi

# ==================================================
# EXIBIR INFORMAÇÕES DO RF
# ==================================================

echo "✅ RF localizado com sucesso!"
echo ""
echo "📁 Diretório: $RF_DIR"
echo ""
echo "📄 Arquivos disponíveis:"
ls -1 "$RF_DIR" 2>/dev/null | grep -E "^(RF|UC|RL|WF|MD|TC|MT|CN|STATUS)" | sort

echo ""
echo "📌 Caminhos completos:"
echo "  RF.md   : $RF_DIR/${RF_ID}.md"
echo "  RF.yaml : $RF_DIR/${RF_ID}.yaml"

# Verificar arquivos opcionais
if [ -f "$RF_DIR/UC-${RF_ID}.yaml" ]; then
    echo "  UC.yaml : $RF_DIR/UC-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/RL-${RF_ID}.yaml" ]; then
    echo "  RL.yaml : $RF_DIR/RL-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/WF-${RF_ID}.md" ]; then
    echo "  WF.md   : $RF_DIR/WF-${RF_ID}.md"
fi

if [ -f "$RF_DIR/MD-${RF_ID}.yaml" ]; then
    echo "  MD.yaml : $RF_DIR/MD-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/TC-${RF_ID}.yaml" ]; then
    echo "  TC.yaml : $RF_DIR/TC-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/MT-${RF_ID}.yaml" ]; then
    echo "  MT.yaml : $RF_DIR/MT-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/CN-${RF_ID}.yaml" ]; then
    echo "  CN.yaml : $RF_DIR/CN-${RF_ID}.yaml"
fi

if [ -f "$RF_DIR/STATUS.yaml" ]; then
    echo "  STATUS.yaml : $RF_DIR/STATUS.yaml"
fi

echo ""
echo "💡 Para usar em scripts Bash:"
echo "  RF_DIR=\$(bash find-rf.sh $RF_ID | grep 'Diretório:' | cut -d' ' -f3)"
echo "  cat \"\$RF_DIR/${RF_ID}.md\""

exit 0

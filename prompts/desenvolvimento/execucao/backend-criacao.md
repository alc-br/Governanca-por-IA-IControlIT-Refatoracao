Executar backend do RFXXX conforme CONTRATO DE EXECUCAO – BACKEND.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
Antes de QUALQUER acao, validar:

1. UC-RFXXX.md DEVE existir
2. STATUS.yaml DEVE ter documentacao.uc = true
3. MD-RFXXX.md DEVE existir OU STATUS.yaml ter md: false com justificativa valida
4. WF-RFXXX.md DEVE existir OU STATUS.yaml ter wf: false com justificativa valida

VALIDACAO DE PRE-REQUISITOS:
1. Verificar se MD-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo md
     * Se md = false, validar se ha justificativa
     * Justificativas validas: "tabela unica sem complexidade", "CRUD simples sem relacionamentos", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

2. Verificar se WF-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo wf
     * Se wf = false, validar se ha justificativa
     * Justificativas validas: "gestao administrativa backend-only", "CRUD simples", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

3. Se QUALQUER pre-requisito falhar:
   - PARAR imediatamente
   - REPROVAR com mensagem clara
   - NAO prosseguir com backend

Execute apenas os testes previstos neste contrato
(smoke tests e caminho feliz).
NAO validar violacoes de contrato.
NAO assumir comportamento implicito.
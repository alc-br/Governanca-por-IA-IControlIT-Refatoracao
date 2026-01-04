Executar frontend do RFXXX conforme CONTRATO DE EXECUÇÃO – FRONTEND.
Seguir CLAUDE.md.

PRE-REQUISITOS OBRIGATORIOS (BLOQUEANTES):
Antes de QUALQUER acao, validar:

1. UC-RFXXX.md DEVE existir
2. STATUS.yaml DEVE ter documentacao.uc = true
3. Backend DEVE estar aprovado 100% (desenvolvimento.backend.conformidade = "100%")
4. MD-RFXXX.md DEVE existir OU STATUS.yaml ter md: false com justificativa valida
5. WF-RFXXX.md DEVE existir OU STATUS.yaml ter wf: false com justificativa valida

VALIDACAO DE PRE-REQUISITOS:
1. Verificar se backend foi aprovado:
   - STATUS.yaml desenvolvimento.backend.conformidade DEVE ser "100%"
   - Se < 100%: BLOQUEAR execucao frontend
   - Motivo: Frontend depende de contratos de API prontos

2. Verificar se MD-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo md
     * Se md = false, validar se ha justificativa
     * Justificativas validas: "tabela unica sem complexidade", "CRUD simples sem relacionamentos", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

3. Verificar se WF-RFXXX.md existe
   - Se NAO existir:
     * Verificar STATUS.yaml campo wf
     * Se wf = false, validar se ha justificativa
     * Justificativas validas: "gestao administrativa backend-only", "CRUD simples", "nao aplicavel"
     * Se justificativa ausente ou invalida: BLOQUEAR execucao
   - Se existir: prosseguir

4. Se QUALQUER pre-requisito falhar:
   - PARAR imediatamente
   - REPROVAR com mensagem clara
   - NAO prosseguir com frontend

Antes de qualquer coisa, analise se tudo está implementado no backend e caso falte algo me avise imediatamente.

Preste MUITA atenção ao checklist obrigatório, pois é essencial que voce o siga.

Ao final me diga em qual menu eu posso acessar a funcionalidade desenvolvida.

Fique atento para que o layout siga nosso padrão já existente utilizado em http://localhost:4200/admin/management/sla-operacoes, http://localhost:4200/management/users, http://localhost:4200/management/roles etc.

Lembre de adicionar esse item ao menu.
Executar adequacao de frontend do RFXXX conforme D:/IC2_Governanca/contracts/desenvolvimento/execucao/frontend-adequacao.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

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

VALIDACAO DATA-TEST ATTRIBUTES (BLOQUEANTE):
Antes de considerar frontend concluido, o agente DEVE validar:

1. TODOS elementos interativos TEM data-test attributes
2. Nomenclatura segue padrao: data-test="<contexto>-<elemento>-<acao>"
3. Executar validacao:
   ```bash
   grep -r "data-test=" frontend/src/app/modules/RFXXX/
   ```
4. Se resultado vazio ou insuficiente → BLOQUEAR conclusao do frontend
5. Elementos que DEVEM ter data-test:
   - Botoes (salvar, cancelar, excluir, etc.)
   - Campos de formulario (input, select, textarea)
   - Links de navegacao
   - Grids/tabelas (headers, rows, acoes)
   - Modals/dialogs
6. Elementos que NAO precisam de data-test:
   - Texto estatico
   - Icones decorativos
   - Divs estruturais

Ver padrao completo em: docs/CONVENTIONS.md (secao 5.6 - Data-test Attributes)

RAZAO: Testes E2E dependem de data-test. Sem eles, 100% dos testes FALHAM.

VALIDACAO INICIAL OBRIGATORIA:
1. Antes de QUALQUER acao, execute:
   - dotnet build (backend)
   - npm run build (frontend)
2. Se QUALQUER build quebrar: PARAR, CORRIGIR e re-validar
3. Somente prosseguir com adequacao se AMBOS os builds passarem

AUTONOMIA TOTAL:
- NAO perguntar se pode buildar/rodar
- NAO esperar usuario executar comandos
- O agente DEVE deixar sistema BUILDADO e RODANDO
- Garantir que TUDO funcione sem intervencao manual

Execute apenas os testes previstos neste contrato
(testes E2E Playwright para validar adequacao).
NAO validar violacoes de contrato backend.
NAO assumir comportamento implicito.

RESPONSABILIDADE DO AGENTE:
- Buildar backend (dotnet build)
- Buildar frontend (npm run build)
- Rodar backend (dotnet run)
- Rodar frontend (npm start)
- Executar testes E2E (npm run e2e)
- Deixar sistema funcional ao final

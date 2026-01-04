Validar frontend do RFXXX conforme CONTRATO DE VALIDACAO DE FRONTEND.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

VALIDACAO INICIAL OBRIGATORIA:
1. Antes de QUALQUER acao, execute:
   - dotnet build (backend)
   - npm run build (frontend)
2. Se QUALQUER build quebrar: PARAR, REPORTAR gap critico
3. Sistema quebrado BLOQUEIA validacao

AUTONOMIA TOTAL:
- NAO perguntar se pode buildar/rodar
- NAO esperar usuario executar comandos
- O agente DEVE deixar sistema BUILDADO e RODANDO
- Garantir que TUDO funcione sem intervencao manual

1. Analisar documentacao oficial (RF, UC, WF)
2. Criar matriz de cobertura UC
3. Implementar testes E2E Playwright
4. Executar testes E2E
5. Validar conformidade visual (checklist)
6. Validar integracao (i18n, diagnosticos, permissoes)
7. Documentar gaps criticos

Se qualquer gap critico for encontrado:
- REPROVAR
- NAO sugerir correcoes
- NAO ajustar codigo
- NAO continuar execucao

RESPONSABILIDADE DO AGENTE:
- Buildar backend (dotnet build)
- Buildar frontend (npm run build)
- Rodar backend (dotnet run)
- Rodar frontend (npm start)
- Executar testes E2E (npm run e2e)
- Gerar relatorios de conformidade
- Deixar sistema funcional ao final

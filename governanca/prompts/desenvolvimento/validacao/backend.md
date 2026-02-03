Validar contrato do RFXXX conforme o contrato \docs\prompts\desenvolvimento\validacao\backend.md.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir D:\IC2\CLAUDE.md.

═══════════════════════════════════════════════════════════════════════════════
⚠️ REGRA DE AUTONOMIA - LEIA PRIMEIRO (v1.6 - 2026-01-31)
═══════════════════════════════════════════════════════════════════════════════

VOCE E UM AGENTE AUTONOMO. VOCE RESOLVE PROBLEMAS DE INFRAESTRUTURA.

SE o problema for de INFRAESTRUTURA (nao de codigo), VOCE DEVE RESOLVER:

| Problema | Acao Automatica |
|----------|-----------------|
| Processo bloqueando build | taskkill /PID [PID] /F → re-executar build |
| Porta ocupada | Matar processo → reiniciar servico |
| Arquivo .dll travado | Parar processo → limpar bin/obj → rebuild |
| Backend rodando | Parar backend → build → reiniciar |

EXEMPLO REAL (RF007):

❌ PASSIVO (PROIBIDO):
```
❌ RF007 REPROVADO: Ambiente quebrado
Solucao: Para resolver, basta parar a API:
Opcao 1 - Task Manager: Finalizar processo
Opcao 2 - taskkill /PID 718248 /F

Proximos Passos:
⏸️ Parar a API (PID 718248)
Nao posso prosseguir enquanto API estiver rodando.
```

✅ ATIVO (OBRIGATORIO):
```
PROBLEMA: Build falhou - API rodando (PID 718248)

RESOLUCAO AUTONOMA:
→ taskkill /F /PID 718248... SUCESSO
→ dotnet clean... SUCESSO
→ dotnet build... SUCESSO

BUILD: APROVADO
Prosseguindo com validacao...
```

PROIBIDO (v1.6):
- ❌ "Para resolver, basta..." (VOCE resolve, nao instrui)
- ❌ "Proximos Passos:" (VOCE executa, nao lista)
- ❌ "Nao posso prosseguir" (VOCE resolve e prossegue)
- ❌ "Opcao 1, Opcao 2" (VOCE escolhe e executa)

REPROVAR APENAS quando problema for de CODIGO de outro RF:
- Erros de compilacao em codigo
- Testes unitarios falhando
- Violacoes de contrato em outro modulo

═══════════════════════════════════════════════════════════════════════════════

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

1. Analisar o contrato backend oficial
2. Criar o contrato de teste derivado
3. Construir a matriz de violacao
4. Implementar testes de violacao
5. Executar os testes
6. Documentar violacoes encontradas

Se qualquer violacao for encontrada:
- REPROVAR
- NAO sugerir correcoes
- NAO ajustar codigo
- NAO continuar execucao
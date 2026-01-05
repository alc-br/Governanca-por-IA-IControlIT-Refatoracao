# Fluxo: ADEQUAÇÃO (Backend legado → modernizado)

Use esta sequência de prompts quando estiver adaptando backend legado aos padrões atuais.

## Quando usar

- Backend existe mas foi criado antes da governança
- Código legado precisa ser regularizado
- Frontend já existe e depende do backend
- Comportamento atual não pode ser quebrado

## Ordem de Execução

1. **01-regularizar-backend.md** - Auditar e adequar backend legado
2. **02-validar-contrato.md** - Validar backend adequado (testes de violação)
3. **03-frontend.md** - Ajustar/criar frontend se necessário
4. **04-testes.md** - Executar testes (Backend, E2E, Segurança)

## Contratos Ativados

- CONTRATO-DE-REGULARIZACAO-DE-BACKEND
- CONTRATO-EXECUCAO-TESTER-BACKEND
- CONTRATO-EXECUCAO-FRONTEND (se necessário)
- CONTRATO-EXECUCAO-TESTES

## Resultado Esperado

- Backend legado normalizado
- Backend validado por Tester-Backend
- Compatibilidade preservada
- Testes 100% pass
- STATUS.yaml atualizado

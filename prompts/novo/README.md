# Fluxo: NOVO RF (Backend não existe)

Use esta sequência de prompts quando estiver criando um RF completamente novo.

## Quando usar

- Backend não existe para este RF
- Funcionalidade nova (não há equivalente no legado)
- Primeiro desenvolvimento

## Ordem de Execução

1. **01-documentacao-essencial.md** - Criar RF, UC, MD, WF, user-stories.yaml
2. **02-backend.md** - Implementar backend (.NET 10 + CQRS)
3. **03-validar-contrato.md** - Validar backend (testes de violação)
4. **04-frontend.md** - Implementar frontend (Angular 19)
5. **05-testes.md** - Executar testes (Backend, E2E, Segurança)

## Contratos Ativados

- CONTRATO-DOCUMENTACAO-ESSENCIAL
- CONTRATO-EXECUCAO-BACKEND
- CONTRATO-EXECUCAO-TESTER-BACKEND
- CONTRATO-EXECUCAO-FRONTEND
- CONTRATO-EXECUCAO-TESTES

## Resultado Esperado

- RF 100% documentado e implementado
- Backend validado por Tester-Backend
- Frontend integrado
- Testes 100% pass
- STATUS.yaml atualizado

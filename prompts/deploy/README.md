# Fluxo: DEPLOY (HOM/PRD)

Use esta sequência de prompts para deploy em ambientes.

## Quando usar

- Deploy para Homologação (HOM)
- Deploy para Produção (PRD)
- Rollback de deploy

## Ordem de Execução

1. **01-deploy-hom.md** - Deploy HOM com validação completa
2. **02-deploy-hom-sem-validacao.md** - Deploy HOM para apresentação inicial (EXCEPCIONAL)
3. **03-deploy-prd.md** - Deploy PRD (requer aprovação Tester-Backend)

## Contratos Ativados

- CONTRATO-DEPLOY-AZURE
- CONTRATO-DEPLOY-HOM-SEM-VALIDACAO (exceção)

## Resultado Esperado

- Deploy executado com sucesso
- EXECUTION-MANIFEST atualizado
- Rollback disponível em caso de falha
- Ambiente validado

## Importante

- Deploy PRD requer 100% aprovação Tester-Backend
- Deploy sem validação só para HOM (apresentações)
- Rollback obrigatório em caso de falha
- Alterações fora do pipeline são proibidas

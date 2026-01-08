# Contratos Depreciados

**Data de criação:** 2026-01-01
**Motivo:** Organização da estrutura de contratos

---

## Contratos Depreciados

Esta pasta contém contratos que foram substituídos por versões melhoradas ou movidos para estrutura organizada.

| Arquivo | Data Depreciação | Razão | Substituído por |
|---------|------------------|-------|-----------------|
| `CONTRATO-GERACAO-RF-RL.md.deprecated-20260101` | 2026-01-01 | Commit automático perigoso | `documentacao/geracao/rf-rl.md` (commit manual) |
| `CONTRATO-DOCUMENTACAO-UC.md.deprecated-20260101` | 2026-01-01 | Versão antiga sem autocorreção | `documentacao/execucao/uc-criacao.md` |

---

## Regras de Depreciação

1. **Formato de nomenclatura**: `NOME-ORIGINAL.md.deprecated-AAAAMMDD`
2. **Nunca deletar**: Arquivos depreciados são mantidos para rastreabilidade histórica
3. **Não usar em produção**: Contratos depreciados NÃO devem ser executados
4. **Consulta permitida**: Podem ser consultados para entender decisões históricas

---

## Por que depreciar em vez de deletar?

- **Rastreabilidade**: Histórico de decisões técnicas
- **Referências**: Outros documentos podem mencionar versões antigas
- **Auditoria**: Compliance e governança
- **Recuperação**: Em caso de necessidade de rollback

---

## Quando um contrato é depreciado?

- Quando há duplicação confirmada
- Quando versão melhorada substitui a antiga
- Quando contrato se torna obsoleto por mudança de arquitetura
- Quando há reorganização estrutural do projeto

---

**Atenção**: Esta pasta é gerenciada por contratos de governança. Não mover ou deletar arquivos sem aprovação formal.

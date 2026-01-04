# UC-RF042 — Casos de Uso: Gestão de Notas Fiscais de Estoque

**RF:** RF042 — Gestão de Notas Fiscais de Estoque
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC007-FIN - Financeiro Processos
**Fase:** Fase 4 - Financeiro II - Processos

---

## Índice de Casos de Uso
| UC | Nome | Complexidade |
|----|------|--------------|
| UC00 | Listar Notas Fiscais Estoque | Média |
| UC01 | Criar Nota Fiscal Estoque | Média |
| UC02 | Visualizar Nota Fiscal Estoque | Baixa |
| UC03 | Editar Nota Fiscal Estoque | Média |
| UC04 | Cancelar Nota Fiscal Estoque | Baixa |
| UC05 | Vincular Itens ao Estoque | Média |
| UC06 | Validar XML NF-e | Alta |
| UC07 | Relatório de Entradas | Média |

## Resumo dos UCs

**UC00:** Listagem com filtros por fornecedor, período, status. Grid: Número NF, Fornecedor, Data Emissão, Valor Total, Qtd Itens, Status.
**RN-042-001:** Multi-tenancy por empresa.

**UC01:** Registro de NF entrada. Campos: Número*, Série*, Chave_Acesso (44 dígitos), Fornecedor*, Dt_Emissao*, Valor_Total*, Anexo_XML (upload). Valida chave acesso formato. Job cria itens estoque automaticamente se vinculação configurada.
**RN-042-002:** Chave acesso única no sistema.

**UC02:** Detalhes NF + lista itens vinculados + histórico recebimentos. Exibe XML parseado, DANFE preview, movimentações estoque geradas.

**UC03:** Editar valor, data ou fornecedor. RN: Apenas se status = "Pendente". NF com itens recebidos não pode ser editada.

**UC04:** Cancelar NF com justificativa. RN: Estorna movimentações estoque se já processadas.

**UC05:** Vincular itens da NF a produtos no estoque. Seleciona NF → Lista itens XML → Mapeia para produtos cadastrados → Gera entradas estoque.
**RN-042-003:** Validação de quantidade (XML vs estoque físico).

**UC06:** Upload XML NF-e → Parse automático → Valida assinatura digital → Extrai dados (fornecedor, itens, valores) → Pré-preenche formulário.
**RN-042-004:** Suporta NF-e modelo 55 (padrão SEFAZ).

**UC07:** Relatório de entradas por período: Total NFs, Valor Total, Qtd Itens, Por Fornecedor, Por Categoria. Formatos: PDF, Excel.

## Integrações
- Central: Feature "NF Estoque" | i18n: `nf_estoque.*` | Auditoria: CREATE, UPDATE, CANCEL | RBAC: Estoquista (criar), Controller (cancelar)

## Histórico
| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-18 | Criação inicial - 8 UCs |

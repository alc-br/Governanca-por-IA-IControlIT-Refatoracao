# Casos de Uso - RF041 - Gestão de Estoque de Aparelhos

**RF:** RF-041 — Gestão de Estoque de Aparelhos
**Epic:** EPIC009-AST - Ativos e Inventário
**Fase:** Fase 6 - Ativos, Auditoria e Integrações
**Versão:** 1.0
**Data:** 2025-12-18
**Autor:** Agência ALC - alc.dev.br

## Índice | 11 UCs
UC00: Listar | UC01: Criar Item | UC02: Visualizar | UC03: Editar | UC04: Dar Baixa | UC05: Entrada Estoque (NF) | UC06: Saída Estoque (Alocação) | UC07: Transferência entre Locais | UC08: Inventário Físico | UC09: Alertar Estoque Mínimo | UC10: Relatório Movimentações

## Resumo
**UC00:** Grid: Produto, Marca/Modelo, Localização, Qtd_Disponível, Qtd_Alocada, Qtd_Total, Valor_Unitário, Status.
**UC01:** Form: Produto* (FK Catálogo), Marca*, Modelo*, IMEI/Serial, Localização*, Qtd*, Valor_Unit*, Dt_Entrada, Fornecedor, NF_Entrada. RN: IMEI único se informado.
**UC02:** Detalhes + histórico movimentações (entradas, saídas, transferências) + timeline.
**UC03:** Editar localização, valor, observações. RN: Qtd não editável diretamente (usar UC05/UC06).
**UC04:** Dar baixa (perda, roubo, obsolescência). Motivo* obrigatório. Soft delete. Atualiza qtd disponível.
**UC05:** Entrada via NF (integra RF042). Valida NF → Cria itens estoque → Atualiza qtd. Job automático.
**UC06:** Saída para alocação consumidor/ativo. Valida disponibilidade → Decrementa qtd → Registra histórico.
**UC07:** Transferência entre locais (filiais, almoxarifados). Origem, Destino, Qtd, Responsável_Recebimento.
**UC08:** Inventário físico: Leitura QR/barcode via app mobile → Compara físico vs sistema → Gera relatório divergências.
**UC09:** Job diário verifica estoque < mínimo configurado → Notifica compras → Sugere pedido automático.
**UC10:** Relatório movimentações: Entradas/Saídas/Saldo por período, produto, localização. Curva ABC. Giro estoque.

## Integrações
Central: Estoque Aparelhos | i18n: `estoque_aparelhos.*` | Auditoria: ALL | RBAC: Estoquista (full), Compras (visualizar)

## Histórico
| 1.0 | 2025-12-18 | 11 UCs |

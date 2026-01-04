# Casos de Uso - RF037 - Gestão de Custos por Ativo

**Versão:** 1.0
**Data:** 2025-12-18
**RF Relacionado:** [RF037 - Gestão de Custos por Ativo](./RF037.md)

## Índice de Casos de Uso

| UC | Nome | Complexidade |
|----|------|--------------|
| UC00 | Listar Custos por Ativo | Média |
| UC01 | Criar Custo de Ativo | Média |
| UC02 | Visualizar Custo de Ativo | Baixa |
| UC03 | Editar Custo de Ativo | Média |
| UC04 | Excluir Custo de Ativo | Baixa |
| UC05 | Calcular TCO (Custo Total Propriedade) | Alta |
| UC06 | Comparar Custos entre Ativos | Média |
| UC07 | Alertar Custos Excessivos | Média |
| UC08 | Histórico de Custos do Ativo | Média |

## UC00 - Listar Custos por Ativo
**Objetivo:** Listagem de todos os custos associados a ativos com filtros por tipo, período, ativo.
**Fluxo:** Grid com Ativo, Tipo Custo (Aquisição, Manutenção, Licença, Depreciação), Valor, Data, Fornecedor.
**RN-037-001:** Exibir apenas custos de ativos da empresa atual.

## UC01 - Criar Custo de Ativo
**Objetivo:** Registrar custo específico de um ativo (compra, manutenção, upgrade, licença).
**Fluxo:** Seleciona Ativo*, Tipo Custo*, Valor*, Data*, Fornecedor (opcional), Descrição, Anexos (NF, recibos).
**RN-037-002:** Custo tipo "Aquisição" pode ser registrado apenas 1x por ativo.
**RN-037-003:** Custo tipo "Depreciação" calculado automaticamente (vida útil 5 anos).

## UC02 - Visualizar Custo de Ativo
**Objetivo:** Detalhes do custo + anexos + impacto no TCO do ativo.
**Fluxo:** Exibe dados do custo, links para NF, histórico de pagamentos, impacto percentual no TCO total.

## UC03 - Editar Custo de Ativo
**Objetivo:** Corrigir valor, data, tipo ou fornecedor do custo.
**RN-037-004:** Alteração de custo tipo "Aquisição" requer aprovação do gestor.

## UC04 - Excluir Custo de Ativo
**Objetivo:** Remover custo lançado incorretamente (soft delete).
**RN-037-005:** Exclusão requer justificativa obrigatória. Custo tipo "Aquisição" não pode ser excluído.

## UC05 - Calcular TCO (Custo Total de Propriedade)
**Objetivo:** Calcular TCO completo do ativo: Aquisição + Manutenção + Licenças + Depreciação + Custos operacionais.
**Fluxo:** Dashboard TCO exibe breakdown por categoria, gráfico de pizza, comparação com média da categoria.
**RN-037-006:** TCO inclui custos indiretos (suporte, energia) rateados por tempo de uso.

## UC06 - Comparar Custos entre Ativos
**Objetivo:** Comparar TCO de múltiplos ativos da mesma categoria para identificar outliers.
**Fluxo:** Seleciona ativos → Gera tabela comparativa com TCO, custo por mês, custo por usuário.
**RN-037-007:** Comparação limitada a ativos da mesma categoria/tipo.

## UC07 - Alertar Custos Excessivos
**Objetivo:** Notificar gestor quando custo de ativo excede 120% da média da categoria.
**Fluxo:** Job diário analisa custos vs baseline. Gera alerta se > threshold.
**RN-037-008:** Threshold configurável por categoria (padrão: 120%).

## UC08 - Histórico de Custos do Ativo
**Objetivo:** Timeline completa de todos os custos do ativo desde aquisição.
**Fluxo:** Exibe linha do tempo: Aquisição → Manutenções → Upgrades → Depreciação acumulada.
**RN-037-009:** Histórico inclui custos excluídos (marcados como "Cancelado").

## Integrações
- Central de Funcionalidades: Feature "Custos por Ativo"
- i18n: `custos_ativo.titulo`, `custos_ativo.tipo.aquisicao`
- Auditoria: CREATE, UPDATE, DELETE, TCO_CALC
- RBAC: Visualizar (Gestor), Criar/Editar (Financeiro), Aprovar (Diretor)

## Histórico
| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-18 | Criação inicial - 9 UCs |

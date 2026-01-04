# Casos de Uso - RF050 - Gestão de Linhas e Chips SIM

**Versão:** 1.0 | **Data:** 2025-12-18
**RF Relacionado:** [RF050](./RF050.md)

## Índice de Casos de Uso
| UC | Nome | Complexidade |
|----|------|--------------|
| UC00 | Listar Linhas/Chips | Média |
| UC01 | Criar Linha/Chip | Média |
| UC02 | Visualizar Linha/Chip | Baixa |
| UC03 | Editar Linha/Chip | Média |
| UC04 | Bloquear/Desbloquear Linha | Média |
| UC05 | Vincular Linha a Consumidor | Média |
| UC06 | Trocar Chip (mesma linha) | Média |
| UC07 | Portabilidade de Linha | Alta |
| UC08 | Relatório de Consumo por Linha | Média |
| UC09 | Dashboard de Linhas Ativas | Média |

## Resumo dos UCs

**UC00:** Listagem com filtros por operadora, status, consumidor. Grid: Número, ICCID, Operadora, Consumidor, Status, Plano, Valor.

**UC01:** Cadastro. Campos: Número*, ICCID* (19-20 dígitos), Operadora*, Plano, DDD, Tipo* (Móvel/Fixa/Dados), Status* (Ativo/Bloqueado/Cancelado), Dt_Ativacao, Contrato.
**RN-050-001:** ICCID único no sistema.

**UC02:** Detalhes + histórico consumo + consumidor atual. Timeline: ativação, trocas chip, bloqueios, vinculações.

**UC03:** Editar operadora, plano ou status. RN: Número não pode ser alterado (apenas portabilidade).

**UC04:** Bloquear/desbloquear via API operadora. Registra motivo (perda, roubo, inadimplência). Job sincroniza status com operadora.
**RN-050-002:** Bloqueio imediato via API + email confirmação consumidor.

**UC05:** Vincular linha disponível a consumidor. Valida: linha disponível, consumidor ativo. Gera termo responsabilidade se configurado.

**UC06:** Substituir chip físico (perda/defeito). ICCID antigo → Novo ICCID. Mantém histórico.
**RN-050-003:** Chip antigo marcado como "Substituído".

**UC07:** Portabilidade numérica. Workflow: Solicitação → Operadora Origem → Operadora Destino → Confirmação (até 3 dias úteis). Atualiza operadora no sistema.

**UC08:** Relatório consumo: Chamadas, SMS, Dados (MB), Valor total. Período configurável. Drill-down bilhetes.

**UC09:** Dashboard: Total linhas ativas, por operadora, por status, alertas (bloqueios, vencimentos plano). KPIs em tempo real.

## Integrações
- Central: Feature "Linhas/Chips" | i18n: `linhas_chips.*` | Auditoria: CREATE, UPDATE, BLOQUEIO, PORTABILIDADE | RBAC: Telecom (full), Gestor (visualizar)

## Histórico
| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-18 | Criação inicial - 10 UCs |

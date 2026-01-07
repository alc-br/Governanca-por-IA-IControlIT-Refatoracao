# Casos de Uso - RF059 - Gestão de Status e Tipos Genéricos

**RF:** RF059 — Gestão de Status e Tipos Genéricos
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD - Cadastros Base
**Fase:** Fase 2 - Cadastros e Serviços Transversais
**RF Relacionado:** [RF059](./RF059.md)

## Índice | 6 UCs
UC00: Listar | UC01: Criar | UC02: Visualizar | UC03: Editar | UC04: Inativar | UC05: Reordenar

## Resumo
**UC00:** Grid: Categoria (Ativos/Contratos/Chamados), Nome, Cor, Ordem, Qtd Uso, Status.
**UC01:** Form: Categoria*, Nome*, Descrição, Cor_Badge, Icone, Ordem, Permite_Transicao_De (multi-select), Fl_Ativo. RN: Nome único por categoria.
**UC02:** Detalhes + registros usando este status + fluxo transições permitidas.
**UC03:** Editar nome, cor, transições. RN: Alteração transições valida ciclos.
**UC04:** Inativar. RN: Status em uso não pode ser inativado (migrar registros primeiro).
**UC05:** Drag-and-drop para reordenar exibição. Salva nova ordem.

## Integrações
Central: Status Genéricos | i18n: `status_genericos.*` | Auditoria: CREATE, UPDATE | RBAC: Admin (full)

## Histórico
| 1.0 | 2025-12-18 | 6 UCs |

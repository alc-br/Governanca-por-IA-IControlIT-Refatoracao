# Casos de Uso - RF045 - Gestão de Volumetria

**RF:** RF045 — Gestão de Volumetria
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC008-SD - Service Desk
**Fase:** Fase 5 - Service Desk
**RF Relacionado:** [RF045](./RF045.md)

## Índice de Casos de Uso
| UC | Nome | Complexidade |
|----|------|--------------|
| UC00 | Listar Registros Volumetria | Média |
| UC01 | Capturar Volumetria Automática | Alta |
| UC02 | Visualizar Volumetria | Média |
| UC03 | Dashboard de Crescimento | Alta |
| UC04 | Projetar Capacidade Futura | Alta |
| UC05 | Alertar Limite de Capacidade | Média |
| UC06 | Relatório de Uso por Módulo | Média |
| UC07 | Comparar Volumetria entre Períodos | Média |
| UC08 | Configurar Quota de Fornecedor | Alta |
| UC09 | Atualizar Limites e Quotas | Média |
| UC10 | Exportar Dados de Volumetria | Média |
| UC11 | Aplicar Throttling Progressivo | Alta |

## Resumo dos UCs

**UC00:** Listagem de snapshots volumétricos por data. Grid: Data Captura, Total Ativos, Total Usuários, Total Contratos, Total Faturas, Crescimento (%).

**UC01:** Job diário (02:00) executa queries de contagem:
```sql
SELECT COUNT(*) FROM Ativos WHERE Fl_Excluido = 0;
SELECT COUNT(*) FROM Usuarios WHERE Fl_Ativo = 1;
SELECT COUNT(*) FROM Contratos WHERE Status = 'Ativo';
...
```
Registra em tabela `Volumetria_Snapshot` com timestamp.
**RN-045-001:** Captura 20+ métricas principais (tabelas core do sistema).

**UC02:** Detalhes snapshot com breakdown por módulo. Exibe comparação com snapshot anterior (delta absoluto e %).

**UC03:** Dashboard com gráficos evolução:
- Linha: Total registros por dia (últimos 90 dias)
- Barras empilhadas: Distribuição por módulo
- KPI: Crescimento médio diário, projeção próximos 30 dias
**RN-045-002:** Cache 1h para performance.

**UC04:** Análise preditiva baseada em regressão linear. Calcula crescimento médio últimos 6 meses → Projeta 12 meses futuros.
Alertas: "Banco atingirá 1 milhão registros em 4 meses - considerar otimização".
**RN-045-003:** Thresholds configuráveis por tabela.

**UC05:** Job semanal verifica volumetria vs limites definidos. Se > 80% capacidade → Notifica admin.
**RN-045-004:** Limites exemplo: Ativos (100k), Usuários (10k), Contratos (5k).

**UC06:** Relatório comparativo uso entre módulos: Ativos (35%), Faturas (25%), Contratos (20%), etc. Identifica módulos subutilizados ou com crescimento acelerado.

**UC07:** Comparação mês a mês ou ano a ano. Tabela: Métrica, Jan 2024, Jan 2025, Δ absoluto, Δ %.

## Integrações
- Central: Feature "Volumetria" | i18n: `volumetria.*` | Auditoria: SNAPSHOT_CREATE | RBAC: Apenas Admin/DBA

## Histórico

**UC08:** Configuração de quotas mensais por fornecedor (GB tráfego + número requests). Validação: quota = 0 apenas para Super Admin (ilimitado). RBAC: `VOL.QUOTAS.CREATE`.
**RN-045-002:** Todo fornecedor deve ter quota configurada.

**UC09:** Atualização de quotas com versionamento automático. Validação: nova quota não pode ser menor que consumo atual do mês. RBAC: `VOL.QUOTAS.UPDATE`.
**RN-045-004:** Throttling progressivo ao atingir limites (95% → 50%, 99% → 80%, 100% → bloqueio POST/PUT/DELETE).

**UC10:** Exportação de dados de volumetria (CSV/Excel) com isolamento multi-tenant. Validação: tamanho máximo 1 GB. RBAC: `VOL.EXPORT`.
**RN-045-005:** Volumetria de um fornecedor não pode afetar outro.

**UC11:** Sistema automático de throttling progressivo ao atingir limites de quota:
- 95% → Rate limit 50% (delay 1s entre requests)
- 99% → Rate limit 80% (delay 5s entre requests)
- 100% → Bloqueia POST/PUT/DELETE (GET ainda permitido)
**RN-045-004:** Throttling aplica isolamento perfeito (fornecedor A não afeta B).
| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0 | 2025-12-18 | Criação inicial - 8 UCs |
| 2.0 | 2025-12-31 | Adicionados UC08-UC11 (Quotas, Throttling, Export) - Cobertura 100% |

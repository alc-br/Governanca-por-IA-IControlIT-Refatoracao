Para o RFXXX...

Executar validação completa de WF-RFXXX.yaml e MD-RFXXX.yaml conforme contracts/documentacao/validacao/wf-md.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.

Seguir D:\IC2\CLAUDE.md.

PRÉ-REQUISITOS BLOQUEANTES:
- WF-RFXXX.yaml DEVE existir
- MD-RFXXX.yaml DEVE existir
- UC-RFXXX.yaml DEVE existir e estar validado
- RF-RFXXX.yaml DEVE existir
- STATUS.yaml DEVE ter documentacao.wf = true
- STATUS.yaml DEVE ter documentacao.md = true

IMPORTANTE:
Este é um validador READ-ONLY. NÃO corrija problemas, apenas IDENTIFIQUE e REPORTE.

VALIDAÇÕES OBRIGATÓRIAS:

PARTE 1: WIREFRAMES (WF) - 9 validações
1. Cobertura UC → WF = 100% (ZERO gaps)
2. Estados obrigatórios (Loading, Vazio, Erro, Dados) em TODOS os WFs
3. Responsividade (Mobile, Tablet, Desktop) documentada em TODOS os WFs
4. Acessibilidade WCAG AA documentada em TODOS os WFs
5. Componentes de interface documentados (formulários, botões, tabelas, modais, navegação, feedback)
6. Eventos de interação documentados (onClick, onSubmit, onChange, onNavigate, onOpen/onClose)
7. Seções obrigatórias presentes (objetivo, principios_design, mapa_telas, componentes, eventos, estados, responsividade, acessibilidade, contratos_comportamento)
8. Contratos de comportamento completos (validações, transições de estado, regras de negócio, mensagens erro/sucesso, confirmações)
9. WF.yaml aderente ao template v2.0

PARTE 2: MODELO DE DADOS (MD)
1. Derivação RF/UC/WF = 100%
2. Multi-tenancy (cliente_id ou empresa_id) em TODAS as tabelas
3. Auditoria completa (5 campos) em TODAS as tabelas
4. Soft delete (deleted_at) em TODAS as tabelas
5. Constraints obrigatórias (PK, FK, UNIQUE) em TODAS as tabelas
6. Índices obrigatórios (PK, multi-tenancy, performance) em TODAS as tabelas
7. MD.yaml aderente ao template v2.0

PARTE 3: STATUS - 1 validação
1. STATUS.yaml com documentacao.wf = true E documentacao.md = true

CRITÉRIO DE APROVAÇÃO:
- ✅ APROVADO = 17/17 validações PASS + ZERO gaps (9 WF + 7 MD + 1 STATUS)
- ❌ REPROVADO = Qualquer validação FAIL OU qualquer gap

RELATÓRIO OBRIGATÓRIO:
Gere relatório detalhado em .temp_ia/validacao-wf-md-RFXXX-relatorio.md contendo:
- Resumo executivo (tabela de validações)
- Gaps identificados (se houver) classificados por severidade
- Recomendações de ação corretiva
- Veredicto final: APROVADO ou REPROVADO

MODO AUTONOMIA TOTAL:
- NÃO perguntar permissões ao usuário
- NÃO esperar confirmação
- EXECUTAR IMEDIATAMENTE todas as 17 validações
- Gerar relatório automaticamente
- Declarar veredicto final

Se REPROVADO:
- Listar TODOS os gaps encontrados
- Classificar por severidade (CRÍTICO, IMPORTANTE, MENOR)
- Recomendar ações corretivas específicas
- NÃO prosseguir para próximo passo

Se APROVADO:
- Confirmar ZERO gaps
- Declarar: "WF-RFXXX e MD-RFXXX estão 100% conformes. Pode prosseguir para criação de TC/MT."

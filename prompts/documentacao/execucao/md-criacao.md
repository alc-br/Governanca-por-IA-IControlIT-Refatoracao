Para o RFXXX...

Crie os documentos de Modelo de Dados (MD) conforme docs\contracts\documentacao\execucao\md-criacao.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.

Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

PRÉ-REQUISITOS BLOQUEANTES:
- RFXXX.yaml DEVE estar criado
- UC-RFXXX.yaml DEVE estar criado e validado
- WF-RFXXX.yaml DEVE estar criado
- STATUS.yaml DEVE ter documentacao.uc = true
- STATUS.yaml DEVE ter documentacao.wf = true

IMPORTANTE:
1. Leia o template em docs/templates/:
   - MD.yaml

2. Analise RFXXX.yaml, UC-RFXXX.yaml e WF-RFXXX.yaml para extrair tudo o que for necessário para o Modelo de Dados:
   - RF: Entidades principais e relacionamentos
   - UC: Operações CRUD e validações
   - WF: Campos visíveis e filtros (índices necessários)

3. O modelo de dados é derivado da análise COMPLETA de RF, UC e WF. Cada tabela deve ter campos obrigatórios de governança.

4. Este documento é único, então não pode automatizar de nenhuma forma, tudo deve ser criado de forma personalizada.

NAO invente entidades ou campos. Tudo deve derivar de RF/UC/WF.

CAMPOS OBRIGATÓRIOS EM TODAS AS TABELAS:
1. id (GUID, PK)
2. cliente_id OU empresa_id (multi-tenancy)
3. created_at (auditoria)
4. created_by (auditoria)
5. updated_at (auditoria)
6. updated_by (auditoria)
7. deleted_at (soft delete)

CONSTRAINTS OBRIGATÓRIAS:
- PK constraint (id)
- FK multi-tenancy (CASCADE)
- FKs auditoria (SET NULL)
- UNIQUE por tenant (quando aplicável)

ÍNDICES OBRIGATÓRIOS:
- Índice PK
- Índice multi-tenancy
- Índices de performance (conforme filtros do WF)

Após criar MD-RFXXX.yaml:
- Atualize STATUS.yaml com documentacao.md = true

PROXIMOS PASSOS:
Após a conclusão bem-sucedida deste contrato, a documentação funcional completa (RF, UC, WF, MD) está finalizada.

O próximo passo é criar os casos de teste:

> Conforme CONTRATO-DOCUMENTACAO-GOVERNADA-TESTES para RFXXX.
> Seguir CLAUDE.md.

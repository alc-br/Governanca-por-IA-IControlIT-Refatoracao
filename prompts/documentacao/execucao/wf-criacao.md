Para o RFXXX...

Crie os documentos de Wireframes (WF) conforme docs/contracts/documentacao/execucao/wf-criacao.md.

Modo governanca rigida. Nao negociar escopo. Nao extrapolar.

Seguir CLAUDE.md.

Preste MUITA atencao ao checklist obrigatorio, pois e essencial que voce o siga.

PRÉ-REQUISITOS BLOQUEANTES:
- UC-RFXXX.yaml DEVE estar criado e validado
- STATUS.yaml DEVE ter documentacao.uc = true

IMPORTANTE:
1. Leia o template em docs/templates/:
   - WF.yaml

2. Analise o UC-RFXXX.yaml para extrair tudo o que for necessário para os Wireframes.

3. Os wireframes são derivados EXCLUSIVAMENTE dos Casos de Uso. Cada UC deve ter representação visual correspondente.

4. Esses documentos são únicos, então não pode automatizar de nenhuma forma, tudo deve ser criado de forma personalizada garantindo a cobertura total dos UCs.

NAO invente telas ou funcionalidades. Tudo deve derivar dos UCs criados.

ESTADOS OBRIGATÓRIOS em TODOS os wireframes:
- Loading (Carregando)
- Vazio (Sem Dados)
- Erro (Falha ao Carregar)
- Dados (Lista/Formulário Exibido)

RESPONSIVIDADE OBRIGATÓRIA:
- Mobile
- Tablet
- Desktop

ACESSIBILIDADE OBRIGATÓRIA:
- Labels em português claro
- Navegação por teclado
- Contraste WCAG AA

Após criar WF-RFXXX.yaml:
- Atualize STATUS.yaml com documentacao.wf = true

PROXIMOS PASSOS:
Após a conclusão bem-sucedida deste contrato, o próximo passo é:

> Conforme docs/contracts/documentacao/execucao/md-criacao.md para RFXXX.
> Seguir CLAUDE.md.

IMPORTANTE:

Se o WF já estiver criado, valide se ele está dentro dos padrões do template docs/templates/WF.yaml. Se não estiver, ajuste-o para que entre nos padrões. Se ele está no padrão, pare e peça para que avance para o próximo passo que é "Gerar o MD de acordo com o contrato de geração de MD."
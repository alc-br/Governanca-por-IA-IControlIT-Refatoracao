Regularizar backend do RFXXX conforme CONTRATO DE REGULARIZACAO DE BACKEND.
Modo governanca rigida. Nao negociar escopo. Nao extrapolar.
Seguir CLAUDE.md.

Contexto:
Este backend foi desenvolvido antes da governanca atual.
Existem frontends ja implementados que dependem dele.

Objetivo:
Alinhar o backend existente com:
- RFXXX
- UC-RFXXX
- MD-RFXXX
- WF-RFXXX

SEM:
- criar novas funcionalidades
- redefinir regras de negocio
- quebrar contratos existentes com o frontend

Tarefas obrigatorias:
1. Auditar o backend atual contra RF/UC/MD
2. Listar divergencias encontradas
3. Classificar cada divergencia:
   - Falta de validacao
   - Regra nao implementada
   - Comportamento permissivo
   - Inconsistencia de dados
4. Corrigir APENAS o necessario para aderir ao RF
5. Manter compatibilidade com frontend existente
6. Atualizar testes basicos (smoke / caminho feliz)
7. Documentar o que foi ajustado

Proibicoes:
- Nao endurecer validacoes que quebrem frontend
- Nao alterar payloads publicos
- Nao mudar contratos externos
- Nao executar testes de violacao

Resultado esperado:
Backend aderente ao RF e pronto para validacao
pelo CONTRATO DE TESTER-BACKEND.

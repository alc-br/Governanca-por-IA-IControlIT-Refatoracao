Execute D:\IC2_Governanca\contracts\desenvolvimento\manutencao\manutencao-completa.md para corrigir o seguinte problema:

## CONTEXTO

[Descrever o problema que exige manutenção completa]

Exemplo:
```
PROBLEMA: Duplicação de Id_Fornecedor e erros cross-layer

ERROS IDENTIFICADOS:
- CS0101: Duplicação de Id_Fornecedor em Fornecedor.cs (linha 17)
- CS0618 (13 ocorrências): Uso de propriedade obsoleta Id_Fornecedor
- Refatoração parcial "Conglomerado → Fornecedor" mal resolvida

IMPACTO ESTIMADO:
- Arquivos afetados: 20
- Camadas afetadas: 3 (Domain, Application, Infrastructure)
- Tipo: Cross-layer
```

## JUSTIFICATIVA PARA MANUTENÇÃO COMPLETA

[Por que este problema exige Manutenção Completa em vez de Controlada]

Exemplo:
```
RAZÃO: Correção exige alterações em múltiplas camadas

- Domain: Remover duplicações (Fornecedor.cs, Ativo.cs)
- Application: Substituir Id_Fornecedor→ClienteId (15 arquivos)
- Infrastructure: Atualizar DbContext e configurations

ESCOPO: 20 arquivos, 3 camadas (cross-layer)
DECISÕES: Renomeações, remoções, escolhas técnicas necessárias

Manutenção Controlada BLOQUEARIA por ultrapassar escopo (3 arquivos, 1 camada).
```

## ARQUIVOS AFETADOS

[Listar arquivos que precisam ser alterados, agrupados por camada]

Exemplo:
```
Domain Layer:
- D:\IC2\backend\IControlIT.API/src/Domain/Entities/Fornecedor.cs
- D:\IC2\backend\IControlIT.API/src/Domain/Entities/Ativo.cs
- D:\IC2\backend\IControlIT.API/src/Domain/Entities/Conglomerado.cs (REMOVER)

Application Layer (15 arquivos):
- D:\IC2\backend\IControlIT.API/src/Application/Commands/Ativos/CreateAtivoCommand.cs
- D:\IC2\backend\IControlIT.API/src/Application/Commands/Ativos/UpdateAtivoCommand.cs
- D:\IC2\backend\IControlIT.API/src/Application/Queries/Fornecedores/GetFornecedoresQuery.cs
- (continuar listagem...)

Infrastructure Layer:
- D:\IC2\backend\IControlIT.API/src/Infrastructure/Persistence/IApplicationDbContext.cs
- D:\IC2\backend\IControlIT.API/src/Infrastructure/Persistence/Configurations/FornecedorConfiguration.cs
```

## DECISÕES TÉCNICAS NECESSÁRIAS

[Listar decisões que o agente precisará tomar, com alternativas]

Exemplo:
```
DECISÃO 1: Renomear Id_Fornecedor → ClienteId
- Razão: Id_Fornecedor está obsoleto (CS0618)
- Alternativas: Manter Id_Fornecedor (não recomendado - deprecado)
- Escolha recomendada: Migrar para ClienteId (padrão multi-tenancy)

DECISÃO 2: Renomear IdFornecedor → IdFornecedorAquisicao em Ativo.cs
- Razão: Esclarecer contexto (aquisição vs manutenção)
- Alternativas: Manter IdFornecedor genérico
- Escolha recomendada: Renomear para clareza

DECISÃO 3: Remover Conglomerado.cs
- Razão: Arquivo duplicado, refatoração incompleta
- Alternativas: Manter e resolver conflitos
- Escolha recomendada: Remover (mais limpo)
```

## CRITÉRIO DE SUCESSO

[Como validar que a correção foi bem-sucedida]

Exemplo:
```
- ✅ ZERO erros de compilação
- ✅ Build backend: SUCESSO
- ✅ Testes unitários: 100% passando
- ✅ Propriedade obsoleta Id_Fornecedor não usada
- ✅ Duplicações removidas
- ✅ DECISIONS.md atualizado (se decisões tomadas)
- ✅ Branch criado: manutencao/correcao-[PROBLEMA]-[DATA]
```

## RESPONSABILIDADE

[Camada/módulo responsável pelo problema]

Exemplo:
```
RESPONSABILIDADE: DOMAIN + APPLICATION (cross-layer)

- Domain: Duplicação de propriedades
- Application: Uso de propriedades obsoletas
- Causa raiz: Refatoração "Conglomerado → Fornecedor" incompleta
```

---

Modo governança rígida. Não negociar escopo. Não extrapolar.
Seguir D:\IC2\CLAUDE.md e contracts/desenvolvimento/manutencao/manutencao-completa.md.

IMPORTANTE:
- Criar análise de impacto ANTES de iniciar (.temp_ia/ANALISE-IMPACTO-[PROBLEMA].md)
- Corrigir por fases (Domain → Application → Infrastructure → Web)
- Validar build APÓS cada fase
- Documentar decisões em DECISIONS.md
- Criar branch dedicado: manutencao/correcao-[PROBLEMA]-[DATA]
- Commit estruturado com contexto completo

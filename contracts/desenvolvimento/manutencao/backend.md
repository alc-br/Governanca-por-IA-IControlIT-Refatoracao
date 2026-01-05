# CONTRATO DE MANUTENÇÃO – BACKEND

**Projeto:** IControlIT 2.0
**RF relacionado:** RF-027 – Gestão de Aditivos de Contratos
**Tipo de contrato:** Manutenção corretiva (retroativa)
**Status:** Ativo (regularização formal)

---

## 1. Contexto e Justificativa

Durante a execução do **CONTRATO DE EXECUÇÃO – FRONTEND** do RF-027, foi identificado um bloqueio crítico no backend que impediu:

* Inicialização correta da aplicação
* Execução da Prova de Acesso
* Execução dos testes E2E

O erro observado foi:

* **SQLite Error 19 – FOREIGN KEY constraint failed** durante o seed
* Erro adicional de **DateTimeOffset em ORDER BY** incompatível com SQLite

Esses problemas **não pertencem ao escopo de frontend** e caracterizam **falhas estruturais pré‑existentes ou de compatibilidade**, exigindo correção técnica mínima para restabelecer o funcionamento do sistema.

Portanto, esta intervenção é formalmente classificada como **MANUTENÇÃO BACKEND**, aplicada de forma retroativa para preservar a governança do processo.

---

## 2. Objetivo do Contrato

Autorizar **exclusivamente** a correção mínima necessária no backend para:

* Restabelecer a inicialização do sistema
* Garantir consistência do seed de permissões e roles
* Permitir execução da Prova de Acesso
* Habilitar testes E2E do frontend

Este contrato **não autoriza evolução funcional**, refatorações amplas ou mudanças de comportamento além do estritamente necessário.

---

## 3. Escopo Permitido

Estão **explicitamente autorizadas** apenas as seguintes ações:

### 3.1 Seed e Inicialização

* Reset controlado do banco SQLite local (`icontrolit.db`)
* Correção de inconsistências de seed de permissões e roles
* Garantia de integridade referencial entre `Permissions`, `Roles` e `RolePermissions`

### 3.2 Compatibilidade Técnica

* Ajustes mínimos em queries incompatíveis com SQLite (ex.: `DateTimeOffset` em `ORDER BY`)
* Correções necessárias para permitir execução local e testes

### 3.3 Infraestrutura Local

* Reinicialização do backend
* Validação de health check
* Prova de acesso via autenticação como usuário `Developer`

---

## 4. Itens Explicitamente Proibidos

Sob este contrato, é **terminantemente proibido**:

* Alterar ou criar funcionalidades novas
* Modificar regras de negócio
* Alterar contratos de frontend
* Ajustar UI, componentes, rotas ou i18n
* Executar ou declarar conclusão de frontend
* Atualizar status funcional do RF-027

Qualquer violação invalida este contrato.

---

## 5. Critérios de Conclusão (DoD)

Este contrato é considerado **CONCLUÍDO** somente quando **TODOS** os itens abaixo forem atendidos:

* Backend inicializa sem erro
* Seed executa com sucesso (FKs válidas)
* Health check retorna **Healthy**
* Login como usuário `Developer` retorna **HTTP 200**
* Endpoint crítico do RF-027 responde sem erro estrutural
* Commit isolado contendo **APENAS backend** é criado
* Merge do backend no branch `dev` é realizado

---

## 6. Regras de Versionamento e Commit

* O commit deve conter **somente arquivos backend**
* Nenhum arquivo de frontend ou documentação fora deste contrato é permitido

**Padrão obrigatório de commit:**

```
feat(backend-maintenance): corrigir seed e compatibilidade SQLite – RF-027
```

---

## 7. Encerramento do Contrato

Após o merge bem-sucedido no branch `dev`:

* Este contrato é automaticamente encerrado
* A execução do RF-027 retorna ao **CONTRATO DE EXECUÇÃO – FRONTEND**
* Testes E2E e validação funcional podem ser retomados

---

## 8. Cláusula de Governança

Este contrato existe para **preservar a integridade do processo**, evitar mistura de responsabilidades e garantir rastreabilidade total entre causa, correção e execução.

Nenhuma ação fora do escopo aqui definido é considerada válida.

---

**Contrato criado para regularização formal de execução.**

---

## REGRA DE NEGACAO ZERO

Se uma solicitacao:
- nao estiver explicitamente prevista no contrato ativo, ou
- conflitar com qualquer regra do contrato

ENTAO:

- A execucao DEVE ser NEGADA
- Nenhuma acao parcial pode ser realizada
- Nenhum "adiantamento" e permitido

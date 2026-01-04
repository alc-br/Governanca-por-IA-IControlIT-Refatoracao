# UC-RF015 — Casos de Uso Canônicos

**RF:** RF015 — Gestão de Locais e Endereços
**Versão:** 2.0
**Data:** 2025-12-31
**Autor:** Agência ALC - alc.dev.br
**Epic:** EPIC003-CAD-Cadastros-Base
**Fase:** Fase-2-Cadastros-e-Servicos-Transversais

---

## Índice de Casos de Uso

| UC | Nome | Descrição |
|----|------|-----------|
| UC00 | UC00 - Listar Endereços | Caso de uso |
| UC01 | UC01 - Criar Endereço | Caso de uso |
| UC02 | UC02 - Visualizar Endereço | Caso de uso |
| UC03 | UC03 - Editar Endereço | Caso de uso |
| UC04 | UC04 - Inativar Endereço | Caso de uso |

---

# UC00 - Listar Endereços

**RF:** RF-063 - Gestão de Locais e Endereços
**Versão:** 1.0
**Data:** 04/11/2025

---

## Descrição

Permitir que usuários autorizados listem, filtrem e visualizem endereços cadastrados no sistema.

---

## Atores

- **Ator Principal:** Usuário com permissão `CAD.LOCAIS.VISUALIZAR`
- **Atores Secundários:** Sistema de auditoria

---

## Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `CAD.LOCAIS.VISUALIZAR`

---

## Fluxo Principal

1. Usuário acessa a tela de Locais e Endereços
2. Sistema exibe listagem de endereços do conglomerado do usuário
3. Sistema exibe filtros: CEP, Logradouro, Cidade, Estado, Tipo (Principal/Secundário)
4. Sistema exibe grid com colunas:
   - CEP
   - Logradouro completo (Tipo + Nome + Número)
   - Bairro
   - Cidade/UF
   - Tipo (Principal/Secundário)
   - Ações (Visualizar, Editar, Excluir)
5. Sistema implementa paginação (10 registros por página)

---

## Fluxos Alternativos

### FA01 - Filtrar por CEP
1. Usuário digita CEP no filtro
2. Sistema filtra endereços que contenham o CEP informado
3. Sistema atualiza grid

### FA02 - Filtrar por Cidade/Estado
1. Usuário seleciona Estado no dropdown
2. Sistema habilita dropdown de Cidades daquele Estado
3. Usuário seleciona Cidade
4. Sistema filtra endereços
5. Sistema atualiza grid

### FA03 - Ordenar por coluna
1. Usuário clica no header da coluna
2. Sistema ordena crescente/decrescente
3. Sistema atualiza grid

### FA04 - Exportar para Excel
1. Usuário clica em "Exportar"
2. Sistema gera arquivo Excel com todos os registros filtrados
3. Sistema inicia download

---

## Fluxos de Exceção

### FE01 - Sem permissão
1. Sistema detecta que usuário não possui permissão
2. Sistema exibe mensagem: "Acesso negado. Você não possui permissão para visualizar endereços"
3. Sistema redireciona para dashboard

### FE02 - Nenhum resultado encontrado
1. Sistema não encontra endereços com os filtros aplicados
2. Sistema exibe mensagem: "Nenhum endereço encontrado"
3. Sistema sugere limpar filtros

---

## Pós-condições

- Lista de endereços exibida conforme filtros aplicados
- Operação registrada em log de auditoria

---

## Regras de Negócio

**RN-UC00-001:** Isolamento Multi-tenant
- Usuário só visualiza endereços do seu conglomerado
- Filtro `Id_Conglomerado = @Id_Conglomerado_Usuario` aplicado automaticamente

**RN-UC00-002:** Paginação obrigatória
- Máximo 100 registros por página
- Padrão: 10 registros

---

## Rastreabilidade

- **RF:** [RF-063-Gestao-Locais-Enderecos.md](../RF-063-Gestao-Locais-Enderecos.md)
- **Testes Backend:** [TC-UC00-listar-enderecos.md](../Testes/Backend/TC-UC00-listar-enderecos.md)
- **Testes Sistema:** [TC-UC00-listar-enderecos.md](../Testes/Sistema/TC-UC00-listar-enderecos.md)

---

# UC01 - Criar Endereço

**RF:** RF-063 - Gestão de Locais e Endereços
**Versão:** 1.0
**Data:** 04/11/2025

---

## Descrição

Permitir que usuários autorizados cadastrem novos endereços no sistema, com validação de CEP e integração com API ViaCEP para autocompletar dados.

---

## Atores

- **Ator Principal:** Usuário com permissão `CAD.LOCAIS.CRIAR`
- **Atores Secundários:** API ViaCEP, Sistema de auditoria

---

## Pré-condições

- Usuário autenticado no sistema
- Usuário possui permissão `CAD.LOCAIS.CRIAR`

---

## Fluxo Principal

1. Usuário acessa tela de Locais e clica em "Novo Endereço"
2. Sistema exibe formulário com campos:
   - CEP (com máscara 00000-000)
   - Tipo de Logradouro (Rua, Avenida, Travessa, etc.)
   - Logradouro
   - Número
   - Complemento
   - Bairro
   - Cidade
   - Estado (UF)
   - País (padrão: Brasil)
   - Latitude (opcional)
   - Longitude (opcional)
   - Tipo: Principal/Secundário
3. Usuário preenche CEP
4. Sistema consulta API ViaCEP
5. Sistema preenche automaticamente: Logradouro, Bairro, Cidade, UF
6. Usuário preenche campos restantes (Número, Complemento)
7. Usuário clica em "Salvar"
8. Sistema valida dados (ver Regras de Negócio)
9. Sistema salva endereço no banco
10. Sistema exibe mensagem: "Endereço cadastrado com sucesso"
11. Sistema redireciona para visualização do endereço

---

## Fluxos Alternativos

### FA01 - CEP não encontrado na ViaCEP
1. Sistema não encontra CEP na API
2. Sistema exibe mensagem: "CEP não encontrado. Preencha manualmente"
3. Sistema habilita todos os campos para preenchimento manual
4. Usuário preenche dados
5. Retorna ao passo 7 do fluxo principal

### FA02 - Marcar como endereço principal
1. Usuário marca checkbox "Endereço Principal"
2. Sistema valida se já existe endereço principal para esta empresa
3. Sistema exibe modal de confirmação: "Já existe um endereço principal. Deseja substituir?"
4. Usuário confirma
5. Sistema desmarca endereço principal anterior
6. Sistema marca novo endereço como principal
7. Retorna ao fluxo principal

### FA03 - Geocodificar endereço
1. Usuário clica em "Geocodificar"
2. Sistema monta endereço completo
3. Sistema consulta API de geocodificação (Google Maps)
4. Sistema preenche Latitude e Longitude
5. Sistema exibe pin no mapa
6. Retorna ao fluxo principal

---

## Fluxos de Exceção

### FE01 - CEP inválido
1. Sistema detecta CEP com formato inválido (não tem 8 dígitos)
2. Sistema exibe mensagem: "CEP inválido. Deve conter 8 dígitos"
3. Sistema mantém foco no campo CEP

### FE02 - Endereço duplicado
1. Sistema detecta endereço idêntico já cadastrado
2. Sistema exibe mensagem: "Endereço já cadastrado"
3. Sistema oferece opção de visualizar endereço existente

### FE03 - Campos obrigatórios não preenchidos
1. Sistema detecta campos obrigatórios vazios
2. Sistema exibe mensagens de validação nos campos
3. Sistema impede salvamento

### FE04 - Sem permissão
1. Sistema detecta falta de permissão
2. Sistema exibe mensagem: "Acesso negado"
3. Sistema redireciona para dashboard

---

## Pós-condições

- Endereço criado no banco de dados
- Operação registrada em auditoria
- Se marcado como principal, endereço anterior desmarcado

---

## Regras de Negócio

**RN-UC01-001:** Validação de CEP (RN-CAD-011-01)
- CEP deve ter 8 dígitos numéricos
- Formato: 00000-000
- CEP é opcional mas se informado deve ser válido

**RN-UC01-002:** Endereço principal único (RN-CAD-011-02)
- Apenas um endereço principal por empresa
- Ao marcar novo como principal, desmarcar anterior

**RN-UC01-003:** Validação de UF (RN-CAD-011-09)
- Estado deve ser sigla de 2 caracteres
- Validar contra lista de UFs brasileiras
- Converter automaticamente para uppercase

**RN-UC01-004:** Campos obrigatórios
- CEP (se Brasil)
- Logradouro
- Número
- Bairro
- Cidade
- UF
- País

**RN-UC01-005:** Geocodificação opcional (RN-CAD-011-07)
- Se geocodificação falhar, não bloquear cadastro
- Apenas registrar erro em log

---

## Rastreabilidade

- **RF:** [RF-063-Gestao-Locais-Enderecos.md](../RF-063-Gestao-Locais-Enderecos.md)
- **MD:** [MD-013-Gestao-Locais-Enderecos.md](../MD-013-Gestao-Locais-Enderecos.md)
- **Testes Backend:** [TC-UC01-criar-endereco.md](../Testes/Backend/TC-UC01-criar-endereco.md)
- **Testes Sistema:** [TC-UC01-criar-endereco.md](../Testes/Sistema/TC-UC01-criar-endereco.md)

---

# UC02 - Visualizar Endereço

**RF:** RF-063 - Gestão de Locais e Endereços
**Versão:** 1.0

---

## Descrição

Visualizar detalhes completos de um endereço, incluindo hierarquia de locais associados (edifícios, andares, salas).

---

## Fluxo Principal

1. Usuário clica em "Visualizar" na listagem
2. Sistema exibe detalhes do endereço
3. Sistema exibe mapa com pin de localização (se geocodificado)
4. Sistema exibe hierarquia de locais:
   - Edifícios neste endereço
   - Andares por edifício
   - Salas por andar
   - Racks por sala

---

## Regras de Negócio

**RN-UC02-001:** Multi-tenant
- Usuário só visualiza endereços do seu conglomerado

---

## Rastreabilidade

- **RF:** [RF-063-Gestao-Locais-Enderecos.md](../RF-063-Gestao-Locais-Enderecos.md)

---

# UC03 - Editar Endereço

**RF:** RF-063 - Gestão de Locais e Endereços
**Versão:** 1.0

---

## Descrição

Permitir edição de dados de endereço existente.

---

## Fluxo Principal

1. Usuário acessa detalhes do endereço
2. Usuário clica em "Editar"
3. Sistema exibe formulário preenchido
4. Usuário altera campos
5. Usuário clica em "Salvar"
6. Sistema valida e atualiza
7. Sistema registra em histórico de auditoria

---

## Regras de Negócio

**RN-UC03-001:** Não pode alterar endereço de outro conglomerado

---

## Rastreabilidade

- **RF:** [RF-063-Gestao-Locais-Enderecos.md](../RF-063-Gestao-Locais-Enderecos.md)

---

# UC04 - Inativar Endereço

**RF:** RF-063 - Gestão de Locais e Endereços
**Versão:** 1.0

---

## Descrição

Inativar endereço usando soft delete, com inativação em cascata de locais dependentes.

---

## Fluxo Principal

1. Usuário clica em "Inativar"
2. Sistema exibe modal de confirmação
3. Sistema alerta sobre impactos (edifícios, andares, salas que serão inativados)
4. Usuário confirma
5. Sistema ativa soft delete (Fl_Excluido = 1)
6. Sistema inativa em cascata locais dependentes
7. Sistema registra em auditoria

---

## Regras de Negócio

**RN-UC04-001:** Inativação em cascata (RN-CAD-011-12)
- Inativa todos edifícios, andares, salas e racks associados

**RN-UC04-002:** Validar ativos
- Não permite inativar se houver ativos ativos nos locais

---

## Rastreabilidade

- **RF:** [RF-063-Gestao-Locais-Enderecos.md](../RF-063-Gestao-Locais-Enderecos.md)

---

## Histórico de Alterações

| Versão | Data | Autor | Descrição |
|--------|------|-------|-----------|
| 1.0 | 2025-12-17 | Sistema | Consolidação de 5 casos de uso |

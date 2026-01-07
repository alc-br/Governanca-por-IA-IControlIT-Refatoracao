# Script para atualizar UC-RF064.yaml com cobertura 100%
import os

# Caminho do novo arquivo
output_file = r"UC-RF064.yaml.new"

# Conteúdo completo do novo YAML
yaml_content = """uc:
  documentacao: "RF064"
  titulo: "Templates de E-mail"
  fase: "Fase 2 - Cadastros e Serviços Transversais"
  epic: "EPIC004-TPL-Templates"
  versao: "2.1"
  data: "2025-12-31"
  autor: "Agência ALC - alc.dev.br"

exclusions:
  uc_items: []

casos_de_uso:
  # UCs base (CRUD)
  - id: "UC00"
    nome: "Listar Templates de E-mail"
    tipo: "leitura"
    regras_negocio:
      - "RN-RF064-005"
      - "RN-RF064-016"
    endpoint: "GET /api/templates-email"

  - id: "UC01"
    nome: "Criar Template de E-mail"
    tipo: "escrita"
    regras_negocio:
      - "RN-RF064-001"
      - "RN-RF064-008"
      - "RN-RF064-009"
      - "RN-RF064-012"
      - "RN-RF064-016"
      - "RN-RF064-018"
    endpoint: "POST /api/templates-email"

  - id: "UC02"
    nome: "Visualizar Template de E-mail"
    tipo: "leitura"
    regras_negocio:
      - "RN-RF064-013"
      - "RN-RF064-014"
    endpoint: "GET /api/templates-email/{id}"

  - id: "UC03"
    nome: "Editar Template de E-mail"
    tipo: "escrita"
    regras_negocio:
      - "RN-RF064-009"
      - "RN-RF064-012"
    endpoint: "PUT /api/templates-email/{id}"

  - id: "UC04"
    nome: "Inativar Template de E-mail"
    tipo: "escrita"
    regras_negocio: []
    endpoint: "DELETE /api/templates-email/{id}"

  # UCs adicionais (funcionalidades específicas)
  - id: "UC05"
    nome: "Compilar Template MJML → HTML"
    tipo: "processamento"
    regras_negocio:
      - "RN-RF064-001"
      - "RN-RF064-008"
      - "RN-RF064-009"
      - "RN-RF064-018"
    endpoint: "Sistema (job)"

  - id: "UC06"
    nome: "Testar Compatibilidade Multi-Cliente"
    tipo: "validacao"
    regras_negocio:
      - "RN-RF064-002"
    endpoint: "POST /api/templates-email/{id}/test-compatibility"

  - id: "UC07"
    nome: "Configurar Branding por Empresa"
    tipo: "configuracao"
    regras_negocio:
      - "RN-RF064-005"
    endpoint: "GET/PUT /api/branding-email"

  - id: "UC08"
    nome: "Configurar e Executar Teste A/B"
    tipo: "teste"
    regras_negocio:
      - "RN-RF064-006"
    endpoint: "POST /api/ab-tests"

  - id: "UC09"
    nome: "Rastrear Abertura de E-mail"
    tipo: "rastreamento"
    regras_negocio:
      - "RN-RF064-003"
    endpoint: "GET /api/track/open/{id_envio}"

  - id: "UC10"
    nome: "Rastrear Cliques em Links"
    tipo: "rastreamento"
    regras_negocio:
      - "RN-RF064-004"
    endpoint: "GET /api/track/click/{id_envio}"

  - id: "UC11"
    nome: "Calcular Anti-Spam Score"
    tipo: "validacao"
    regras_negocio:
      - "RN-RF064-010"
    endpoint: "POST /api/templates-email/{id}/spam-score"

  - id: "UC12"
    nome: "Clonar Template da Biblioteca Padrão"
    tipo: "escrita"
    regras_negocio:
      - "RN-RF064-011"
    endpoint: "POST /api/templates-email/{id}/clone"

  - id: "UC13"
    nome: "Agendar Envio de E-mail"
    tipo: "escrita"
    regras_negocio:
      - "RN-RF064-015"
      - "RN-RF064-018"
    endpoint: "POST /api/envios-email/schedule"

  - id: "UC14"
    nome: "Visualizar Métricas Consolidadas"
    tipo: "leitura"
    regras_negocio:
      - "RN-RF064-014"
    endpoint: "GET /api/templates-email/metrics"

  - id: "UC15"
    nome: "Gerenciar Descadastramento (Unsubscribe)"
    tipo: "escrita"
    regras_negocio:
      - "RN-RF064-007"
    endpoint: "GET/POST /api/unsubscribe/{id_envio}"

  - id: "UC16"
    nome: "Configurar e Validar SMTP"
    tipo: "configuracao"
    regras_negocio:
      - "RN-RF064-017"
    endpoint: "GET/PUT/POST /api/smtp-config"

matriz_rastreabilidade:
  cobertura_rn:
    total_rns: 18
    rns_cobertas: 18
    percentual: "100%"
    mapeamento:
      - rn: "RN-RF064-001"
        ucs: ["UC01", "UC05"]
      - rn: "RN-RF064-002"
        ucs: ["UC06"]
      - rn: "RN-RF064-003"
        ucs: ["UC09"]
      - rn: "RN-RF064-004"
        ucs: ["UC10"]
      - rn: "RN-RF064-005"
        ucs: ["UC00", "UC07"]
      - rn: "RN-RF064-006"
        ucs: ["UC08"]
      - rn: "RN-RF064-007"
        ucs: ["UC15"]
      - rn: "RN-RF064-008"
        ucs: ["UC01", "UC05"]
      - rn: "RN-RF064-009"
        ucs: ["UC01", "UC03", "UC05"]
      - rn: "RN-RF064-010"
        ucs: ["UC11"]
      - rn: "RN-RF064-011"
        ucs: ["UC12"]
      - rn: "RN-RF064-012"
        ucs: ["UC01", "UC03"]
      - rn: "RN-RF064-013"
        ucs: ["UC02"]
      - rn: "RN-RF064-014"
        ucs: ["UC02", "UC14"]
      - rn: "RN-RF064-015"
        ucs: ["UC13"]
      - rn: "RN-RF064-016"
        ucs: ["UC00", "UC01"]
      - rn: "RN-RF064-017"
        ucs: ["UC16"]
      - rn: "RN-RF064-018"
        ucs: ["UC01", "UC05", "UC13"]

historico:
  - versao: "2.1"
    data: "2025-12-31"
    descricao: "Expansão para 100% de cobertura de RNs (UC05-UC16)"
"""

# Escrever novo arquivo
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(yaml_content)

print(f"Arquivo criado: {output_file}")
print(f"Tamanho: {len(yaml_content)} bytes")

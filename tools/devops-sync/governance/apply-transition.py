# tools/devops-sync/apply-transition.py

import yaml
import sys

rf = sys.argv[1]

manifest = load_manifest(rf)

if manifest["resultado_final"] != "APROVADO":
    raise Exception("Transição negada: backend não aprovado")

status = load_status_yaml(rf)

status["governanca"]["contrato_ativo"] = "CONTRATO-EXECUCAO-TESTES"
status["governanca"]["ultimo_manifesto"] = manifest["id"]
status["testes"]["backend"] = "pending"
status["devops"]["board_column"] = "Pronto para Testes"

save_status_yaml(rf, status)

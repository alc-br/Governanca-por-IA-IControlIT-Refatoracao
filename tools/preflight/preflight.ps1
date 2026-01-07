param (
  [Parameter(Mandatory)]
  [string]$RF,

  [Parameter(Mandatory)]
  [ValidateSet("FRONTEND","BACKEND","MANUTENCAO","DEBUG","TESTES")]
  [string]$Contrato
)

$branch = "feature/$RF-$($Contrato.ToLower())"

Write-Host "📌 Preparando ambiente para $RF ($Contrato)"

git checkout dev
git pull origin dev
git checkout -b $branch

Write-Host "✅ Branch criado: $branch"

$manifest = "docs/contracts/EXECUTION-MANIFEST.md"

(Get-Content $manifest) `
  -replace "CONTRATO: .*", "CONTRATO: $Contrato" `
  -replace "Requisito Funcional .*", "Requisito Funcional: $RF" |
Set-Content $manifest

Write-Host "✅ EXECUTION-MANIFEST.md atualizado"

$statusPath = "docs/documentacao/$RF/STATUS.yaml"

if (!(Test-Path $statusPath)) {
  Write-Host "🆕 Criando STATUS.yaml"
  New-Item -ItemType Directory -Force -Path "docs/documentacao/$RF" | Out-Null
  @"
rf: $RF
status:
  documentation:
    documentacao: false
    uc: false
    md: false
    wf: false
    tc_backend: false
    tc_frontend: false
    tc_seguranca: false
    tc_e2e: false
  development:
    backend: not_started
    frontend: not_started
  tests:
    backend: not_run
    e2e: not_run
    security: not_run
devops:
  work_item_id: null
"@ | Set-Content $statusPath
}

Write-Host "🚀 Pre-flight concluído"

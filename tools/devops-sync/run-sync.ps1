$env:AZDO_ORG_URL = "https://dev.azure.com/IControlIT-v2"
$env:AZDO_PROJECT = "iControlIT 2.0"

# Tentar ler PAT de arquivo
$patFile = "D:\IC2\.azdo-pat"
if (Test-Path $patFile) {
    $env:AZDO_PAT = Get-Content $patFile -Raw
    $env:AZDO_PAT = $env:AZDO_PAT.Trim()
}

if (-not $env:AZDO_PAT) {
    Write-Host "ERRO: PAT nao configurado. Configure em D:\IC2\.azdo-pat ou defina a variavel AZDO_PAT"
    exit 1
}

Write-Host "PAT configurado. Executando sync..."
python D:\IC2\tools\devops-sync\sync-all-rfs.py

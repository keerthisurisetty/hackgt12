# Requires: PowerShell 5+, Python 3 in PATH
param(
    [int]$Port = 8080
)

$ErrorActionPreference = 'Stop'

function Start-Server {
    param([int]$Port)
    $cmd = "python -m http.server $Port"
    Write-Host "Starting server on http://localhost:$Port ..." -ForegroundColor Green
    Start-Process powershell -ArgumentList "-NoProfile","-Command",$cmd | Out-Null
}

function Open-Browser {
    param([int]$Port)
    $url = "http://localhost:$Port/login.html"
    Write-Host "Opening $url" -ForegroundColor Green
    Start-Process $url | Out-Null
}

try {
    # Prefer py if available
    $python = (Get-Command py -ErrorAction SilentlyContinue)
    if ($python) { $env:PY_PYTHON = '3'; $global:alias:python = 'py' }
} catch {}

try {
    Start-Server -Port $Port
    Start-Sleep -Seconds 1
    Open-Browser -Port $Port
} catch {
    Write-Error $_
    exit 1
}



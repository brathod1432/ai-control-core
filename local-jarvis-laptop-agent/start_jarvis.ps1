param(
    [switch]$StartOllama,
    [string]$Config = "config\jarvis.local.example.json"
)

$ErrorActionPreference = "Stop"

$ScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ConfigPath = if ([System.IO.Path]::IsPathRooted($Config)) {
    $Config
}
else {
    Join-Path $ScriptRoot $Config
}

$BaseUrl = "http://127.0.0.1:11434"
$Model = "qwen2.5:3b"
$TagsUrl = "$BaseUrl/api/tags"

function Test-Ollama {
    try {
        Invoke-RestMethod -Uri $TagsUrl -Method Get -TimeoutSec 3 | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

Write-Host "Jarvis local start"
Write-Host "Ollama endpoint: $BaseUrl"
Write-Host "Required model: $Model"
Write-Host "Project path: $ScriptRoot"

if (-not (Test-Ollama)) {
    if ($StartOllama) {
        Write-Host "Ollama is not responding. Starting 'ollama serve' in a hidden local process..."
        Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 2
    }
}

if (-not (Test-Ollama)) {
    Write-Host "Ollama is not responding on $BaseUrl."
    Write-Host "Start Ollama locally, then rerun this script. If needed, run:"
    Write-Host "  ollama serve"
    Write-Host "or rerun:"
    Write-Host "  .\start_jarvis.ps1 -StartOllama"
    exit 1
}

$Tags = Invoke-RestMethod -Uri $TagsUrl -Method Get -TimeoutSec 5
$Models = @($Tags.models | ForEach-Object { $_.name })
if ($Models -notcontains $Model) {
    Write-Host "Ollama is running, but model '$Model' was not found."
    Write-Host "Available models:"
    $Models | ForEach-Object { Write-Host "  $_" }
    Write-Host "No model download was attempted. Install the model only if you explicitly choose to."
    exit 2
}

$env:PYTHONPATH = Join-Path $ScriptRoot "src"
Write-Host "Starting Jarvis. Logs and transcripts stay local."
Push-Location $ScriptRoot
try {
    python -m jarvis --config $ConfigPath
}
finally {
    Pop-Location
}

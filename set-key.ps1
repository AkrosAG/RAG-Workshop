# Sets LLM_API_KEY for the CURRENT PowerShell session — nothing is written to disk.
# PowerShell scripts run in-process, so a plain call is enough:
#   .\set-key.ps1
# Every python/poetry command started from this shell inherits the key.

if ($env:LLM_API_KEY) {
    Write-Host "LLM_API_KEY is already set for this session (overwriting)."
}

$env:LLM_API_KEY = Read-Host "LLM API key (input hidden)" -MaskInput

if ($env:LLM_API_KEY) {
    Write-Host "LLM_API_KEY set for this session. It vanishes when the shell closes."
} else {
    Write-Warning "Empty input - LLM_API_KEY not set."
}

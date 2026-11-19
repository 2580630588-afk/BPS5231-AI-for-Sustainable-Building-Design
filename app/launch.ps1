$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$env:OPENBLAS_NUM_THREADS = '1'
$env:OMP_NUM_THREADS = '1'
$env:PYTHONIOENCODING = 'utf-8'
$candidates = @()
if ($env:WINDOW_TRANSFER_PYTHON) { $candidates += $env:WINDOW_TRANSFER_PYTHON }
$candidates += (Join-Path $projectRoot '.venv\Scripts\python.exe')
# Optional authoring-machine fallback; other machines use their own installed Python.
$runtime = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$candidates += $runtime
$installed = Get-Command python -ErrorAction SilentlyContinue
if ($installed -and $installed.Source -notlike '*\WindowsApps\*') { $candidates += $installed.Source }
foreach ($candidate in $candidates) {
    if (-not (Test-Path -LiteralPath $candidate)) { continue }
    $oldPath = $env:PYTHONPATH
    $extras = Join-Path (Split-Path -Parent (Split-Path -Parent $projectRoot)) 'work\pydeps'
    if ($candidate -eq $runtime -and (Test-Path -LiteralPath $extras)) { $env:PYTHONPATH = $extras }
    & $candidate -c 'import numpy, scipy, sklearn' 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host 'Starting http://127.0.0.1:8765/ ; keep this window open.'
        & $candidate (Join-Path $PSScriptRoot 'serve.py') --open-browser
        exit $LASTEXITCODE
    }
    $env:PYTHONPATH = $oldPath
}
Write-Host 'No usable Python environment found. Install Python and run:'
Write-Host '  python -m venv .venv'
Write-Host '  .venv\Scripts\python -m pip install -r requirements.txt'
Write-Host 'Then double-click launch_interface.bat again.'
exit 1

$projectRoot = (Get-Item $PSScriptRoot).Parent.FullName
$env:PYTHONPATH = $projectRoot
Write-Host "PYTHONPATH has been set to: $env:PYTHONPATH"
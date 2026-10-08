# Forward arguments to the shared manager; preview is the default.
$ErrorActionPreference = 'Stop'
$manager = Join-Path (Split-Path -Parent $PSScriptRoot) 'tools/manage.py'
& python $manager @args
exit $LASTEXITCODE

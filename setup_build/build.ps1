# GraceOS Setup Builder - build.ps1
# Usage: powershell -ExecutionPolicy Bypass -File build.ps1

Set-Location (Split-Path $MyInvocation.MyCommand.Path)

$PythonVersion = '3.13.13'
$PythonDownload = 'https://www.python.org/ftp/python/' + $PythonVersion + '/python-' + $PythonVersion + '-embed-amd64.zip'

Write-Host '=== GraceOS Setup Builder ===' -ForegroundColor Cyan

# Step 1: Download Python embeddable
Write-Host '[1/5] Downloading Python embeddable...' -ForegroundColor Yellow
$buildDir = Join-Path $PSScriptRoot 'build'
New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
Invoke-WebRequest -Uri $PythonDownload -OutFile 'python-embed.zip'

# Step 2: Extract
Write-Host '[2/5] Extracting Python...' -ForegroundColor Yellow
Expand-Archive -Path 'python-embed.zip' -DestinationPath $buildDir -Force
Remove-Item 'python-embed.zip'

# Step 3: Config python313._pth
Write-Host '[3/5] Configuring site-packages...' -ForegroundColor Yellow
Copy-Item 'python313._pth.template' (Join-Path $buildDir 'python313._pth') -Force

# Step 4: Install pip packages
Write-Host '[4/5] Installing Python packages...' -ForegroundColor Yellow
$pythonExe = Join-Path $buildDir 'python.exe'
& $pythonExe -m pip install streamlit pandas pywin32 GitPython -q --target (Join-Path $buildDir 'Lib\site-packages')

# Step 5: Copy app files
Write-Host '[5/5] Copying app files...' -ForegroundColor Yellow
Copy-Item (Join-Path $PSScriptRoot 'app\*') (Join-Path $buildDir 'app\') -Recurse -Force

Write-Host '=== Build preparation complete ===' -ForegroundColor Green
Write-Host ''
Write-Host 'Next: makensis setup.nsi'
Write-Host 'Install NSIS: winget install NSIS.NSIS'

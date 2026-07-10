@echo off
setlocal EnableDelayedExpansion
title Instalador do WhisperEdge
cd /d "%~dp0"

echo ================================================
echo    WhisperEdge - instalador (v0.1.0)
echo ================================================
echo.

rem ---- 1) localizar Python 3.11+ -------------------------------------------
set "PY="
py -3.11 -c "print()" >nul 2>&1 && set "PY=py -3.11"
if not defined PY py -3.12 -c "print()" >nul 2>&1 && set "PY=py -3.12"
if not defined PY python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1 && set "PY=python"

if not defined PY (
    echo [ERRO] Python 3.11 nao encontrado.
    echo.
    echo Instale em https://www.python.org/downloads/  e marque a opcao
    echo "Add python.exe to PATH". Depois rode este instalador de novo.
    echo.
    pause
    exit /b 1
)
echo [1/4] Python encontrado: %PY%

rem ---- 2) criar ambiente virtual -------------------------------------------
if not exist ".venv\Scripts\python.exe" (
    echo [2/4] Criando ambiente virtual...
    %PY% -m venv --copies .venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar o ambiente virtual.
        pause
        exit /b 1
    )
) else (
    echo [2/4] Ambiente virtual ja existe.
)

rem ---- 3) instalar dependencias --------------------------------------------
echo [3/4] Instalando dependencias (pode levar alguns minutos)...
".venv\Scripts\python.exe" -m pip install --upgrade pip -q
".venv\Scripts\python.exe" -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo [ERRO] Falha ao instalar as dependencias.
    pause
    exit /b 1
)

rem ---- 4) atalhos -----------------------------------------------------------
echo [4/4] Criando atalho na Area de Trabalho...
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$lnk = $ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\WhisperEdge.lnk');" ^
  "$lnk.TargetPath = 'C:\Windows\System32\wscript.exe';" ^
  "$lnk.Arguments = '\"%~dp0WhisperEdge.vbs\"';" ^
  "$lnk.WorkingDirectory = '%~dp0';" ^
  "$lnk.IconLocation = '%~dp0assets\ww-logo.ico,0';" ^
  "$lnk.Save()"

choice /C SN /M "Deseja iniciar o WhisperEdge junto com o Windows"
if !errorlevel! EQU 1 (
    powershell -NoProfile -Command ^
      "$ws = New-Object -ComObject WScript.Shell;" ^
      "$lnk = $ws.CreateShortcut([Environment]::GetFolderPath('Startup') + '\WhisperEdge.lnk');" ^
      "$lnk.TargetPath = 'C:\Windows\System32\wscript.exe';" ^
      "$lnk.Arguments = '\"%~dp0WhisperEdge.vbs\"';" ^
      "$lnk.WorkingDirectory = '%~dp0';" ^
      "$lnk.IconLocation = '%~dp0assets\ww-logo.ico,0';" ^
      "$lnk.Save()"
    echo Atalho de inicializacao criado.
)

echo.
echo ================================================
echo  Instalacao concluida!
echo.
echo  - Atalho de ditado: Ctrl + Espaco
echo  - Na primeira execucao o modelo de voz (~460 MB)
echo    sera baixado uma unica vez.
echo  - O icone fica na bandeja, perto do relogio.
echo ================================================
echo.
choice /C SN /M "Abrir o WhisperEdge agora"
if !errorlevel! EQU 1 start "" wscript.exe "%~dp0WhisperEdge.vbs"
endlocal

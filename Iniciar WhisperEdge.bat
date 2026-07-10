@echo off
title WhisperEdge
cd /d "%~dp0"
echo ============================================
echo   WhisperEdge - ditado por voz (Whisper local)
echo ============================================
echo.
echo Atalho de ditado (padrao): Ctrl + Espaco
echo (Na primeira vez, aguarde o download do modelo.)
echo Para fechar: feche esta janela ou o icone da bandeja.
echo.
".venv\Scripts\python.exe" run.py
echo.
echo WhisperEdge encerrou. Pressione uma tecla para fechar.
pause >nul

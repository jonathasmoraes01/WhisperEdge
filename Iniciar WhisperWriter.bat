@echo off
title WhisperWriter
cd /d "%~dp0"
echo ============================================
echo   WhisperWriter - ditado por voz (Whisper)
echo ============================================
echo.
echo Atalho para ditar:  Ctrl + Shift + Espaco
echo (Na primeira vez, aguarde o download do modelo.)
echo Para fechar: feche esta janela ou o icone da bandeja.
echo.
".venv\Scripts\python.exe" run.py
echo.
echo WhisperWriter encerrou. Pressione uma tecla para fechar.
pause >nul

# WiprFlow — Estado do Loop

**Última atualização:** 2026-07-10 — **CONCLUÍDO**
**Diretório:** `C:\Users\Administrator\Tools\whisper-writer` (venv `.venv` Python 3.11).

## Baseline
- [x] Repo / venv / deps
- [x] `python run.py` roda (com correções Windows)

## Checklist — TUDO ✅

### Rebrand
- [x] Textos WhisperWriter → WiprFlow (UI, classe `WiprFlowApp`, bandeja, run.py, README, CHANGELOG)
- [x] Logo/ícone WiprFlow original (`assets/ww-logo.png/.ico` — quadrado roxo + waveform)

### UI
- [x] Tema QSS escuro centralizado (`assets/theme.qss` + `src/theme.py`, accent configurável)
- [x] Pílula flutuante + waveform animada (`src/ui/status_window.py`, não rouba foco)
- [x] Settings redesenhada com 9 abas (config via schema + editores + histórico/stats/sobre)
- [x] i18n EN/PT (`src/i18n.py`, `ui.language`)

### Features
- [x] LLM clean-up (toggle + prompt; openai-compat/ollama/anthropic; fallback seguro)
- [x] Command Mode (2ª hotkey com prioridade; seleção/clipboard → LLM)
- [x] Dicionário pessoal (`text_processing`, word-boundary, editor em tabela)
- [x] Snippets por voz (idem)
- [x] Histórico persistente (SQLite `data/history.db` + captura de janela ativa + UI)
- [x] Estatísticas / dashboard (palavras, WPM, streak — `data/stats.json`)
- [x] 4 modos de gravação preservados (continuous/VAD/toggle/hold)

### Docs
- [x] README reescrito (features, instalação, config, i18n, créditos)
- [x] CHANGELOG atualizado (entrada WiprFlow 1.0)
- [x] requirements.txt reescrito (UTF-8, conjunto testado 3.11)

### Verificação final
- [x] `python run.py` sobe limpo (exit 124 nos testes, sem traceback)
- [x] Cada feature testada por script (imports, i18n, tema, dict+snippets, histórico, stats/WPM, command fallback, 4 modos)
- [x] Nenhum import quebrado / nenhum crash; pílula e Settings renderizadas e conferidas

## Notas / decisões
- Validação por iteração: `timeout 15 .venv/Scripts/python.exe -u src/main.py` (exit 124 = rodando OK) + testes de funções puras + render de UI para PNG.
- LLM/nuvem 100% opcional; sem chave hardcoded (config/.env/env). GPL-3.0 e créditos preservados.
- Novas deps: `pyperclip` (clipboard/command), `httpx` (anthropic; já vinha via openai). `pillow` só p/ gerar o logo (não runtime).
- Command Mode: recomendado atalho que não seja superset do de ditado (registrado no README).
- Dados locais em `data/` (gitignored): history.db, stats.json, dictionary.json, snippets.json.

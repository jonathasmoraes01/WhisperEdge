# WiprFlow — Estado do Loop

**Última atualização:** 2026-07-10 (iteração inicial)
**Iteração nº:** 1
**Diretório de trabalho:** `C:\Users\Administrator\Tools\whisper-writer` (repo git existente, venv `.venv` Python 3.11, deps instaladas).

> Decisão (registrada): o repo WhisperWriter já estava clonado e funcionando aqui, com venv/deps e correções de execução no Windows. Trabalhamos NESTE repo em vez de clonar dentro do repo do Neural Edge OS (que é outro produto). Baseline = este estado.

## Baseline
- [x] Repo clonado / venv / deps instaladas
- [x] `python run.py` roda (com correções de Windows: `import ctranslate2` antes do PyQt5 p/ evitar segfault; guarda de `sys.stdout` None; auto-listen na bandeja; launcher oculto). Modelo `small` pt CPU int8 já em cache.
- Estrutura real:
  - `run.py`, `requirements.txt`, `README.md`, `CHANGELOG.md`, `LICENSE` (GPL-3.0)
  - `src/main.py` (app, tray, hotkey, orquestra tudo)
  - `src/config_schema.yaml` (defaults) + `src/config.yaml` (user)
  - `src/transcription.py` (create_local_model, transcribe_local/api, post_process, `transcribe()`)
  - `src/result_thread.py` (QThread: grava áudio + VAD + chama `transcribe`)
  - `src/key_listener.py` (hotkeys), `src/input_simulation.py` (digitação)
  - `src/utils.py` (ConfigManager singleton)
  - `src/ui/{base_window,main_window,settings_window,status_window}.py`
  - `assets/` (ww-logo.png/ico, microphone.png, pencil.png, beep.wav)

## Checklist

### Rebrand
- [ ] Textos WhisperWriter → WiprFlow (janelas, README, CHANGELOG, UI, about)
- [ ] Logo/ícone WiprFlow original

### UI
- [ ] Tema QSS escuro centralizado (`assets/theme.qss` + loader)
- [ ] Pílula flutuante + waveform animada (status_window)
- [ ] Settings redesenhada (abas)
- [ ] i18n EN/PT (`src/i18n.py`, config `ui_language`)

### Features
- [ ] LLM clean-up (toggle + prompt editável; OpenAI-compat/Anthropic/Ollama)
- [ ] Command Mode (hotkey separada)
- [ ] Dicionário pessoal (mapa de correção)
- [ ] Snippets por voz (gatilho → expansão)
- [ ] Histórico de dictados (persistente SQLite/JSON + UI)
- [ ] Estatísticas / dashboard (palavras, WPM, streak)
- [ ] 4 modos de gravação preservados (continuous/VAD/toggle/hold)

### Docs
- [ ] README reescrito
- [ ] CHANGELOG atualizado

### Verificação final
- [ ] `python run.py` sobe limpo
- [ ] Cada feature testada
- [ ] Nenhum import quebrado / nenhum crash

## Notas / decisões / bloqueios
- Validação por iteração: `timeout 15 .venv/Scripts/python.exe -u src/main.py` → exit 124 (segue rodando, sem traceback) = OK. GUI bloqueia + sandbox mata processos, então uso timeout + smoke-test de imports + testes de funções puras.
- LLM/nuvem: 100% opcional e desligável; nada de chave hardcoded (usa env/.env/config).
- Licença GPL-3.0 e créditos originais preservados (obrigatório).
- Módulos novos planejados: `i18n.py`, `theme.py`/`theme.qss`, `text_processing.py` (dicionário+snippets), `llm_cleanup.py`, `command_processor.py`, `history.py`, `stats.py`.

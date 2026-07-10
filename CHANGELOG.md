# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.1.0] - 2026-07-10

Primeira versão pública do **WhisperEdge** — ditado por voz local e privado,
evolução do projeto open-source WhisperWriter (GPL-3.0, créditos preservados).

### Added
- **Indicador flutuante**: bolinha discreta e arrastável que mostra o app aberto;
  expande no hover com controles (gravar / configurações / janela); **waveform
  reativa à voz real** (parada no silêncio, viva quando você fala); não rouba o
  foco da janela-alvo.
- **Tema escuro central** (`assets/theme.qss` + `src/theme.py`) com cor de
  destaque configurável; ícones desenhados em código (`src/ui/widgets.py`).
- **Configurações redesenhadas**: sidebar de navegação, linhas com título +
  descrição amigáveis (PT/EN), toggles estilo switch, cards por seção.
- **i18n EN/PT** (`src/i18n.py`, `ui.language: auto|en|pt`).
- **Limpeza por IA opcional** (`src/llm_cleanup.py`): OpenAI-compat, Ollama
  local ou Anthropic; prompt editável; fallback seguro; 100% desligável.
- **Command Mode**: segunda hotkey — a fala vira instrução sobre a seleção ou
  o clipboard, processada por LLM.
- **Perfis por app** (`data/app_profiles.json` + página própria): adapta o tom
  pelo app ativo (chat casual, prompt técnico em IDEs, e-mail formal).
- **Dicionário pessoal** e **Snippets por voz** com editores em tabela.
- **Histórico persistente** (SQLite) com app de origem, e **Estatísticas**
  (palavras, WPM, streak diário).
- **Fallback de clipboard**: cada transcrição fica pronta para colar.
- **Aplicação a quente das configurações** (sem reiniciar; modelo recarrega em
  segundo plano só se necessário) e **som de conclusão suave**.
- Launchers Windows: `WhisperEdge.vbs` (invisível, via `pythonw`) e
  `Iniciar WhisperEdge.bat` (com console, para depuração).

### Fixed
- Atalho disparava com Ctrl+QUALQUER tecla (teclas desconhecidas eram tratadas
  como ESPAÇO no backend pynput).
- Nenhuma janela de console pisca na barra de tarefas ao abrir (venv com
  executáveis reais + `pythonw` + execução em processo único).
- Segfault na inicialização no Windows (`import ctranslate2` antes do PyQt5).

### Preserved
- Os 4 modos de gravação (continuous, VAD, press-to-toggle, hold-to-record) e o
  pipeline faster-whisper/API do WhisperWriter original.
- Licença GPL-3.0 e créditos ao projeto WhisperWriter.

## [Unreleased]
### Added
- New settings window to configure WhisperWriter.
- New main window to either start the keyboard listener or open the settings window.
- New continuous recording mode ([Issue #40](https://github.com/savbell/whisper-writer/issues/40)).
- New option to play a sound when transcription finishes ([Issue #40](https://github.com/savbell/whisper-writer/issues/40)).

### Changed
- Migrated status window from using `tkinter` to `PyQt5`.
- Migrated from using JSON to using YAML to store configuration settings.
- Upgraded to latest versions of `openai` and `faster-whisper`, including support for local API ([Issue #32](https://github.com/savbell/whisper-writer/issues/32)).

### Removed
- No longer using `keyboard` package to listen for key presses.

## [1.0.1] - 2024-01-28
### Added
- New message to identify whether Whisper was being called using the API or running locally.
- Additional hold-to-talk ([PR #28](https://github.com/savbell/whisper-writer/pull/28)) and press-to-toggle recording methods ([Issue #21](https://github.com/savbell/whisper-writer/issues/21)).
- New configuration options to:
  - Choose recording method (defaulting to voice activity detection).
  - Choose which sound device and sample rate to use.
  - Hide the status window ([PR #28](https://github.com/savbell/whisper-writer/pull/28)).

### Changed
- Migrated from `whisper` to `faster-whisper` ([Issue #11](https://github.com/savbell/whisper-writer/issues/11)).
- Migrated from `pyautogui` to `pynput` ([PR #10](https://github.com/savbell/whisper-writer/pull/10)).
- Migrated from `webrtcvad` to `webrtcvad-wheels` ([PR #17](https://github.com/savbell/whisper-writer/pull/17)).
- Changed default activation key combo from `ctrl+alt+space` to `ctrl+shift+space`.
- Changed to using a local model rather than the API by default.
- Revamped README.md, including new Roadmap, Contributing, and Credits sections.

### Fixed
- Local model is now only loaded once at start-up, rather than every time the activation key combo was pressed.
- Default configuration now auto-chooses compute type for the local model to avoid warnings.
- Graceful degradation to CPU if CUDA isn't available ([PR #30](https://github.com/savbell/whisper-writer/pull/30)).
- Removed long prefix of spaces in transcription ([PR #19](https://github.com/savbell/whisper-writer/pull/19)).

## [1.0.0] - 2023-05-29
### Added
- Initial release of WhisperWriter.
- Added CHANGELOG.md.
- Added Versioning and Known Issues to README.md.

### Changed
- Updated Whisper Python package; the local model is now compatible with Python 3.11.

[Unreleased]: https://github.com/savbell/whisper-writer/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/savbell/whisper-writer/releases/tag/v1.0.0...v1.0.1
[1.0.0]: https://github.com/savbell/whisper-writer/releases/tag/v1.0.0

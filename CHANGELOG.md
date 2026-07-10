# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [WhisperEdge 1.1] - 2026-07-10
### UI overhaul
- Redesign completo do front-end, **sem emojis**: rótulos e descrições amigáveis
  PT/EN para todas as configurações (`i18n.FIELD_META`), toggles estilo switch,
  cards por seção com divisórias, sidebar com barra de destaque no item ativo,
  ícones desenhados em código (`ui/widgets.py`), janela principal com marca e
  chip de atalho, paleta mais profunda e QSS refinado.

### Fixed
- Atalho disparava com Ctrl+QUALQUER tecla: o backend pynput mapeava teclas
  desconhecidas para `SPACE` por padrão; agora eventos fora do mapa são ignorados.

### Added
- **Indicador flutuante persistente**: pílula discreta que mostra o app aberto e
  **expande no hover** com mini-controles (gravar / configurações / janela).
- **Waveform reativa à voz real**: o `ResultThread` emite o nível de áudio (RMS)
  e a waveform fica parada no silêncio e se mexe quando você fala.
- **Fallback de clipboard** (`post_processing.copy_to_clipboard`): cada
  transcrição também vai para a área de transferência.
- **Configurações com sidebar** de navegação (estilo SuperWhisper), no lugar das
  abas no topo.

### Changed
- Produto renomeado de WiprFlow para **WhisperEdge**.
- Launchers portáveis `Iniciar WhisperEdge.bat` e `WhisperEdge.vbs`.
- Higiene do repositório: `config.yaml`/`data/` fora do versionamento; `.env`
  garantidamente ignorado.

## [WhisperEdge 1.0] - 2026-07-10
Rebrand e evolução do WhisperWriter para **WhisperEdge** — ditado por voz local,
inspirado no Wispr Flow, mantendo a licença GPL-3.0 e os créditos originais.

### Added
- **Pílula flutuante com waveform animada** (`src/ui/status_window.py`) que não
  rouba o foco da janela-alvo; estados ocioso/gravando/transcrevendo.
- **Tema escuro central** via `assets/theme.qss` + `src/theme.py` (cor de destaque
  configurável) aplicado a toda a UI.
- **i18n EN/PT** (`src/i18n.py`, config `ui.language`).
- **Limpeza por LLM opcional** (`src/llm_cleanup.py`): OpenAI-compat, Ollama local
  ou Anthropic, com prompt de sistema editável e fallback seguro. Desligável.
- **Command Mode** (`src/command_processor.py` + segunda hotkey no `key_listener`):
  a fala vira instrução sobre a seleção/clipboard, processada por LLM.
- **Dicionário pessoal** e **Snippets por voz** (`src/text_processing.py`), com
  editores em tabela nas Configurações.
- **Histórico de dictados** persistente em SQLite (`src/history.py`) e
  **Estatísticas** de uso — palavras, WPM, streak (`src/stats.py`) — com telas na UI.
- **Configurações redesenhadas** com abas (Geral, Gravação, Modelo, Aprimorar,
  Dicionário, Snippets, Histórico, Estatísticas, Sobre).
- Novo **logo original** (`assets/ww-logo.png/.ico`).
- Correções de execução no Windows: `import ctranslate2` antes do PyQt5 (evita
  segfault), guarda de `sys.stdout` None (rodar oculto), auto-listen na bandeja.

### Changed
- Rebrand de todas as strings de usuário e da classe principal (`WhisperEdgeApp`).
- `requirements.txt` reescrito (UTF-8) para o conjunto testado em Python 3.11.
- `transcribe()` agora aplica o pipeline de aprimoramento (LLM → dicionário →
  snippets) antes da formatação final.

### Preserved
- Os 4 modos de gravação e o pipeline faster-whisper/API originais.
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

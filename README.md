# <img src="./assets/ww-logo.png" alt="WhisperEdge" width="26" height="26"> WhisperEdge

**Ditado por voz fluido, local e privado.** WhisperEdge escuta um atalho global,
transcreve sua fala com [faster-whisper](https://github.com/SYSTRAN/faster-whisper)
rodando **no seu computador** e digita o texto onde estiver o cursor — em qualquer
aplicativo. Inspirado no Wispr Flow, com uma pílula flutuante e waveform animada,
tema escuro e recursos de produtividade — **sem depender de nuvem**.

> WhisperEdge é um rebrand/evolução do excelente projeto open-source
> [WhisperWriter](https://github.com/savbell/whisper-writer) (GPL-3.0).

---

## ✨ Recursos

- 🎙️ **Ditado local** com faster-whisper (offline, privado). 4 modos de gravação:
  `continuous`, `voice_activity_detection`, `press_to_toggle`, `hold_to_record`.
- 🌊 **Pílula flutuante com waveform animada** — feedback visual discreto de
  ocioso / gravando / transcrevendo, sem roubar o foco da janela onde você digita.
- 🎨 **Tema escuro** central (QSS) com cor de destaque configurável.
- 🌐 **Bilíngue (EN/PT)** — interface em inglês ou português (auto pelo sistema).
- 🧹 **Limpeza por IA (opcional)** — envia a transcrição a um LLM para corrigir
  pontuação e remover hesitações ("um", "tipo", "né"). Provedores: OpenAI-compat,
  **Ollama local**, ou Anthropic. Prompt de sistema editável. **Desligável.**
- ⌨️ **Command Mode** — uma segunda hotkey trata sua fala como uma **instrução**
  sobre o texto selecionado/clipboard (ex.: "deixe mais formal", "vire em bullets",
  "resuma"). Requer um LLM configurado.
- 📖 **Dicionário pessoal** — força correções de nomes/jargões na saída.
- ⚡ **Snippets por voz** — gatilhos falados que expandem em textos maiores
  (ex.: "meu email" → seu endereço completo).
- 🕘 **Histórico de dictados** — cada transcrição salva localmente (SQLite) com
  horário e app ativo; navegável e copiável na UI.
- 📊 **Estatísticas** — palavras ditadas, velocidade média (WPM) e streak diário.

Tudo que é IA/nuvem é **opcional e desligável**; nada de chaves de API no código.

---

## 🚀 Instalação

Pré-requisitos: **Python 3.11** (recomendado) e um microfone.

```bash
git clone <este-repo> whisper-edge
cd whisper-edge
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Na primeira execução, o modelo de transcrição é baixado (uma vez) e fica em cache.

### Windows — notas
- O app já vem com a correção do **segfault** de inicialização (o `ctranslate2`
  é importado antes do PyQt5 em `src/main.py`) e roda oculto sem console.
- Para iniciar **sem janela de console** ou **junto com o Windows**, use um
  atalho apontando para `pythonw`/wscript (veja `Iniciar WhisperWriter.bat` e o
  lançador `.vbs` de exemplo no repositório).

---

## 🎧 Uso

1. Rode `python run.py`. O ícone aparece na **bandeja** e a escuta começa
   automaticamente.
2. Posicione o cursor onde quer escrever, pressione o **atalho de ditado**
   (padrão `ctrl+shift+space`), fale e faça uma pausa — o texto é digitado.
3. Abra **Configurações** pelo ícone da bandeja para ajustar tudo.

### Command Mode
Selecione um texto, pressione o **atalho de comando** (padrão `ctrl+alt+space`),
e fale uma instrução (ex.: "resuma isto"). O texto selecionado é substituído pelo
resultado. Requer `llm_post_processing` configurado.

> Dica: escolha um atalho de comando que **não seja um superset** do atalho de
> ditado, para evitar disparar os dois juntos.

---

## ⚙️ Configuração

As opções ficam em `src/config.yaml` (geradas do `src/config_schema.yaml`) e são
editáveis pela UI de **Configurações**. Principais seções novas do WhisperEdge:

| Seção | Chaves | O que faz |
|------|--------|-----------|
| `ui` | `language` (auto/en/pt), `theme` (dark/light), `accent_color` | Aparência e idioma. |
| `llm_post_processing` | `enabled`, `provider` (openai/ollama/anthropic), `base_url`, `model`, `api_key`, `timeout`, `system_prompt` | Limpeza opcional por LLM. |
| `command_mode` | `enabled`, `activation_key`, `source` (selection/clipboard), `system_prompt` | Segunda hotkey de comando. |
| `dictionary` | `enabled` | Correções (dados em `data/dictionary.json`, editáveis na UI). |
| `snippets` | `enabled` | Expansões (dados em `data/snippets.json`). |
| `history` | `enabled`, `max_entries` | Histórico local (`data/history.db`). |
| `stats` | `enabled` | Estatísticas (`data/stats.json`). |

As seções originais (`model_options`, `recording_options`, `post_processing`,
`misc`) continuam válidas.

### Chaves de API / privacidade
- A chave da OpenAI vai para o `.env` (`OPENAI_API_KEY`), **nunca** para o config.
- Para Ollama local: `provider: ollama`, `base_url: http://localhost:11434/v1`.
- Sem LLM configurado, o clean-up e o Command Mode simplesmente devolvem o texto
  original — o ditado local continua funcionando 100% offline.

### Idiomas (i18n)
A interface tem strings em inglês e português em `src/i18n.py`. `ui.language: auto`
segue o idioma do sistema; force com `en` ou `pt`.

---

## 🗂️ Estrutura

```
src/
  main.py            app, bandeja, hotkeys, orquestracao
  transcription.py   faster-whisper + pipeline de aprimoramento
  result_thread.py   gravacao de audio + VAD
  key_listener.py    hotkeys (ditado + command mode)
  text_processing.py dicionario + snippets
  llm_cleanup.py     LLM opcional (clean-up / chat)
  command_processor.py  Command Mode
  history.py, stats.py  persistencia local
  i18n.py, theme.py, paths.py  fundacao (idioma/tema/caminhos)
  ui/  base_window, main_window, settings_window, status_window (pilula+waveform)
assets/  theme.qss, ww-logo.png/.ico, sons e icones
```

---

## 📜 Licença e créditos

GNU **GPL-3.0** (preservada do projeto original). WhisperEdge é baseado em
[WhisperWriter](https://github.com/savbell/whisper-writer) de sav (savbell) e
contribuidores. Veja `LICENSE`.

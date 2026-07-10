<div align="center">

<img src="assets/ww-logo.png" alt="WhisperEdge" width="96" height="96">

# WhisperEdge

**Ditado por voz local, privado e fluido para Windows.**

Fale em qualquer aplicativo — o texto aparece onde estiver o cursor.
Transcrição 100% no seu computador, sem nuvem.

[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D6?logo=windows&logoColor=white)](#-instalação)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](#-instalação)
[![Licença](https://img.shields.io/badge/Licen%C3%A7a-GPL--3.0-blue)](LICENSE)
[![Offline](https://img.shields.io/badge/Transcri%C3%A7%C3%A3o-100%25%20local-6C5CE7)](#-privacidade)

[Instalação](#-instalação) •
[Como usar](#-como-usar) •
[Recursos](#-recursos) •
[Configuração](#%EF%B8%8F-configuração) •
[English](README.en.md)

<img src="docs/screenshots/settings-general.png" alt="Configurações do WhisperEdge" width="720">

</div>

---

## O que é

O WhisperEdge fica invisível na bandeja do sistema escutando um atalho global
(padrão `Ctrl + Espaço`). Você pressiona, fala, pausa — e o que você disse é
**digitado automaticamente** no campo em que você estava, seja no navegador,
no editor de código, no chat ou no e-mail. A transcrição roda **localmente**
com [faster-whisper](https://github.com/SYSTRAN/faster-whisper): seu áudio
nunca sai da sua máquina.

Um indicador flutuante minimalista mostra o estado do app:

| Ocioso | Hover (controles) | Gravando |
|:---:|:---:|:---:|
| <img src="docs/screenshots/indicator-idle.png" alt="ocioso"> | <img src="docs/screenshots/indicator-hover.png" alt="controles"> | <img src="docs/screenshots/indicator-recording.png" alt="gravando"> |

A bolinha é **arrastável** (lembra a posição) e a waveform **reage à sua voz
de verdade** — parada no silêncio, viva quando você fala.

## ✨ Recursos

- 🎙️ **Ditado local e offline** — modelos Whisper de `tiny` a `large-v3`;
  4 modos de gravação (parada por silêncio, contínuo, apertar p/ alternar,
  segurar p/ gravar).
- 🌊 **Indicador flutuante** com waveform reativa, que nunca rouba o foco da
  janela onde você digita.
- 📋 **Sempre no clipboard** — cada transcrição também fica pronta para colar
  (`Ctrl+V`), mesmo se nenhum campo estava focado.
- 🧹 **Limpeza por IA** *(opcional)* — um LLM corrige pontuação e remove
  hesitações ("ééé", "tipo"). Funciona com OpenAI, qualquer endpoint
  compatível ou **Ollama local**. Totalmente desligável.
- 🎯 **Perfis por app** — o tom se adapta ao aplicativo ativo: casual no
  Discord/WhatsApp, prompt técnico bem estruturado em IDEs, formal no e-mail.
- ⌨️ **Command Mode** — segunda hotkey: fale uma **instrução** sobre o texto
  selecionado ("resuma isto", "deixe mais formal") e ele é reescrito.
- 📖 **Dicionário pessoal** — força a grafia certa de nomes e jargões.
- ⚡ **Snippets por voz** — "meu email" → `voce@dominio.com`.
- 🕘 **Histórico local** (SQLite) com app de origem, e 📊 **estatísticas**
  (palavras, velocidade WPM, sequência diária).
- 🌐 **Interface em português e inglês**, tema escuro com cor de destaque
  configurável, e configurações aplicadas **sem reiniciar**.

## 🚀 Instalação

**Pré-requisitos:** Windows 10/11, [Python 3.11](https://www.python.org/downloads/)
(marque *"Add python.exe to PATH"* na instalação) e um microfone.

### Opção A — instalador automático

1. Baixe o projeto ([ZIP da última versão](../../releases/latest) ou `git clone`).
2. Dê dois cliques em **`install.bat`**.
3. Pronto — o instalador cria o ambiente, baixa as dependências, cria os
   atalhos e abre o app.

### Opção B — manual

```bash
git clone https://github.com/jonathasmoraes01/WhisperEdge.git
cd WhisperEdge
python -m venv --copies .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python run.py
```

> Na primeira execução, o modelo de transcrição (~460 MB no padrão `small`) é
> baixado uma única vez e fica em cache.

Para abrir **sem nenhuma janela**, use `WhisperEdge.vbs`. Para iniciar junto
com o Windows, coloque um atalho desse arquivo na pasta Inicializar
(`Win+R` → `shell:startup`).

## 🎧 Como usar

1. Abra o WhisperEdge — a bolinha aparece na parte inferior da tela e o ícone
   na bandeja.
2. Clique no campo onde quer escrever.
3. Pressione **`Ctrl + Espaço`**, fale e faça uma pausa.
4. O texto é digitado no lugar (e copiado para o clipboard).

Passe o mouse na bolinha para acessar **gravar / configurações / janela**.
Tudo é configurável pelo ícone de engrenagem.

## ⚙️ Configuração

Tudo editável pela interface (bandeja → Configurações). Principais opções:

| Seção | O que controla |
|---|---|
| **Geral** | Idioma da interface, tema, cor de destaque, som de conclusão |
| **Gravação** | Atalho, modo de gravação, microfone, sensibilidade de silêncio |
| **Modelo** | Modelo Whisper (`tiny`→`large-v3`), CPU/GPU, idioma falado |
| **Aprimorar** | Limpeza por IA (provedor/modelo/prompt), Command Mode |
| **Dicionário / Snippets / Perfis** | Correções, expansões e tom por app |
| **Histórico / Estatísticas** | Seus dictados e números de uso |

Os arquivos ficam em `src/config.yaml` (configurações) e `data/` (seus dados
locais) — nenhum dos dois é versionado.

## 🔒 Privacidade

- A transcrição é **100% local** — o áudio nunca sai da sua máquina.
- Histórico, estatísticas, dicionário e perfis ficam apenas em `data/`.
- Os recursos de IA (limpeza e Command Mode) são **opcionais e desligados por
  padrão**; ao ativá-los com um provedor de nuvem, apenas o **texto** ditado é
  enviado ao provedor escolhido. Com **Ollama**, até isso fica local.
- Chaves de API são guardadas no `.env`, nunca no código ou na configuração.

## 🗺️ Roadmap

- [ ] Instalador `.exe` (sem precisar de Python)
- [ ] Suporte a GPU NVIDIA out-of-the-box (CUDA)
- [ ] Mais idiomas de interface
- [ ] Modo de pontuação por comando de voz ("vírgula", "nova linha")

## 🤝 Contribuindo

Issues e PRs são bem-vindos! O código é Python (PyQt5) direto ao ponto:
`src/main.py` orquestra, `src/ui/` é a interface, `src/transcription.py` é o
pipeline de voz. Rode `python run.py` e edite com hot-apply de configurações.

## 📜 Créditos e licença

O WhisperEdge é uma evolução do excelente
[**WhisperWriter**](https://github.com/savbell/whisper-writer) de
[sav](https://github.com/savbell) e contribuidores — obrigado! ❤️

Transcrição por [faster-whisper](https://github.com/SYSTRAN/faster-whisper) /
[CTranslate2](https://github.com/OpenNMT/CTranslate2).

Licenciado sob **GNU GPL-3.0** — veja [LICENSE](LICENSE).

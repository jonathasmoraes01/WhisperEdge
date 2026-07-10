"""
i18n minimo do WhisperEdge. Dicionario de strings EN/PT + funcao tr().

O idioma vem de ConfigManager (ui.language). 'auto' segue o locale do sistema.
Uso: from i18n import tr;  tr('start')  ->  'Iniciar' / 'Start'
"""
import locale

STRINGS = {
    'en': {
        'app_name': 'WhisperEdge',
        'app_tagline': 'Fluid voice dictation',
        'main_menu': 'WhisperEdge — Main Menu',
        'start': 'Start',
        'stop': 'Stop',
        'settings': 'Settings',
        'exit': 'Exit',
        'open_main': 'Open WhisperEdge',
        'open_settings': 'Open Settings',
        'history': 'History',
        'stats': 'Stats',
        # status
        'status_idle': 'Ready',
        'status_recording': 'Listening…',
        'status_transcribing': 'Transcribing…',
        'status_thinking': 'Cleaning up…',
        'status_command': 'Running command…',
        'status_done': 'Done',
        'status_error': 'Error',
        # settings tabs
        'tab_general': 'General',
        'tab_recording': 'Recording',
        'tab_model': 'Model',
        'tab_enhance': 'Enhance',
        'tab_dictionary': 'Dictionary',
        'tab_snippets': 'Snippets',
        'tab_history': 'History',
        'tab_stats': 'Stats',
        'tab_about': 'About',
        'save': 'Save',
        'reset': 'Reset to defaults',
        'saved': 'Settings saved. Restarting…',
        # enhance
        'llm_cleanup': 'AI clean-up',
        'llm_cleanup_desc': 'Send the transcript to an LLM to fix punctuation and remove filler words.',
        'command_mode': 'Command Mode',
        # dictionary / snippets
        'dict_desc': 'Force corrections of specific words/names in the output.',
        'snip_desc': 'Spoken triggers that expand into longer text.',
        'add': 'Add',
        'remove': 'Remove',
        'trigger': 'Trigger (spoken)',
        'replacement': 'Replacement',
        'wrong': 'Heard as',
        'right': 'Correct to',
        # stats
        'words_total': 'Words dictated',
        'words_today': 'Words today',
        'avg_wpm': 'Avg. speed (WPM)',
        'streak': 'Daily streak',
        'sessions': 'Dictations',
        'no_history': 'No dictations yet. Press your hotkey and speak!',
        'copy': 'Copy',
        'clear_history': 'Clear history',
    },
    'pt': {
        'app_name': 'WhisperEdge',
        'app_tagline': 'Ditado por voz fluido',
        'main_menu': 'WhisperEdge — Menu Principal',
        'start': 'Iniciar',
        'stop': 'Parar',
        'settings': 'Configurações',
        'exit': 'Sair',
        'open_main': 'Abrir WhisperEdge',
        'open_settings': 'Abrir Configurações',
        'history': 'Histórico',
        'stats': 'Estatísticas',
        # status
        'status_idle': 'Pronto',
        'status_recording': 'Ouvindo…',
        'status_transcribing': 'Transcrevendo…',
        'status_thinking': 'Limpando texto…',
        'status_command': 'Executando comando…',
        'status_done': 'Concluído',
        'status_error': 'Erro',
        # settings tabs
        'tab_general': 'Geral',
        'tab_recording': 'Gravação',
        'tab_model': 'Modelo',
        'tab_enhance': 'Aprimorar',
        'tab_dictionary': 'Dicionário',
        'tab_snippets': 'Snippets',
        'tab_history': 'Histórico',
        'tab_stats': 'Estatísticas',
        'tab_about': 'Sobre',
        'save': 'Salvar',
        'reset': 'Restaurar padrões',
        'saved': 'Configurações salvas. Reiniciando…',
        # enhance
        'llm_cleanup': 'Limpeza por IA',
        'llm_cleanup_desc': 'Envia a transcrição a um LLM para corrigir pontuação e remover hesitações.',
        'command_mode': 'Modo Comando',
        # dictionary / snippets
        'dict_desc': 'Força correções de palavras/nomes específicos na saída.',
        'snip_desc': 'Gatilhos falados que expandem em textos maiores.',
        'add': 'Adicionar',
        'remove': 'Remover',
        'trigger': 'Gatilho (falado)',
        'replacement': 'Expansão',
        'wrong': 'Ouvido como',
        'right': 'Corrigir para',
        # stats
        'words_total': 'Palavras ditadas',
        'words_today': 'Palavras hoje',
        'avg_wpm': 'Velocidade média (PPM)',
        'streak': 'Sequência diária',
        'sessions': 'Dictados',
        'no_history': 'Nenhum dictado ainda. Aperte o atalho e fale!',
        'copy': 'Copiar',
        'clear_history': 'Limpar histórico',
    },
}


def _system_language():
    try:
        loc = locale.getdefaultlocale()[0] or ''
    except Exception:
        loc = ''
    return 'pt' if loc.lower().startswith('pt') else 'en'


def current_language():
    """Idioma efetivo da UI, resolvendo 'auto' pelo locale do sistema."""
    try:
        from utils import ConfigManager
        lang = ConfigManager.get_config_value('ui', 'language') or 'auto'
    except Exception:
        lang = 'auto'
    if lang == 'auto':
        lang = _system_language()
    return lang if lang in STRINGS else 'en'


def tr(key, lang=None):
    """Traduz uma chave para o idioma atual (fallback: en, depois a propria chave)."""
    lang = lang or current_language()
    return STRINGS.get(lang, {}).get(key) or STRINGS['en'].get(key) or key


# ---------------------------------------------------------------------------
# Rotulos amigaveis das configuracoes (path -> (titulo, descricao curta)).
# Paths: "categoria.chave" ou "categoria.sub.chave".
# ---------------------------------------------------------------------------

SECTION_TITLES = {
    'en': {
        'misc': 'General', 'ui': 'Appearance',
        'recording_options': 'Recording', 'post_processing': 'Text output',
        'model_options': 'Transcription', 'model_options.common': 'Transcription',
        'model_options.api': 'Cloud API (optional)', 'model_options.local': 'Local model',
        'llm_post_processing': 'AI clean-up', 'command_mode': 'Command Mode',
        'dictionary': 'Dictionary', 'snippets': 'Snippets',
        'history': 'History', 'stats': 'Statistics',
    },
    'pt': {
        'misc': 'Geral', 'ui': 'Aparência',
        'recording_options': 'Gravação', 'post_processing': 'Saída de texto',
        'model_options': 'Transcrição', 'model_options.common': 'Transcrição',
        'model_options.api': 'API na nuvem (opcional)', 'model_options.local': 'Modelo local',
        'llm_post_processing': 'Limpeza por IA', 'command_mode': 'Modo Comando',
        'dictionary': 'Dicionário', 'snippets': 'Snippets',
        'history': 'Histórico', 'stats': 'Estatísticas',
    },
}

FIELD_META = {
    'en': {
        'misc.print_to_terminal': ('Log to terminal', 'Print status and transcripts to the console.'),
        'misc.hide_status_window': ('Hide floating indicator', 'Do not show the on-screen pill/dot.'),
        'misc.noise_on_completion': ('Sound on completion', 'Play a beep after the text is typed.'),
        'ui.language': ('Interface language', '"auto" follows your system language.'),
        'ui.theme': ('Theme', ''),
        'ui.accent_color': ('Accent color', 'Hex color used for highlights and the waveform.'),
        'recording_options.activation_key': ('Dictation hotkey', 'Keys separated by "+", e.g. ctrl+space.'),
        'recording_options.input_backend': ('Input backend', 'Leave on "auto" unless keys are not detected.'),
        'recording_options.recording_mode': ('Recording mode', 'How recording starts and stops.'),
        'recording_options.sound_device': ('Microphone (device #)', 'Empty = system default.'),
        'recording_options.sample_rate': ('Sample rate (Hz)', ''),
        'recording_options.silence_duration': ('Silence to stop (ms)', 'Pause length that ends the recording.'),
        'recording_options.min_duration': ('Minimum duration (ms)', 'Shorter recordings are discarded.'),
        'post_processing.writing_key_press_delay': ('Typing delay (s)', 'Delay between simulated key presses.'),
        'post_processing.remove_trailing_period': ('Remove trailing period', ''),
        'post_processing.add_trailing_space': ('Add trailing space', ''),
        'post_processing.remove_capitalization': ('Lowercase everything', ''),
        'post_processing.copy_to_clipboard': ('Copy to clipboard', 'Also keep each transcript ready to paste.'),
        'post_processing.input_method': ('Typing method', ''),
        'model_options.use_api': ('Use cloud API', 'Off = transcribe locally (private, offline).'),
        'model_options.common.language': ('Spoken language', 'ISO code, e.g. pt, en. Empty = auto-detect.'),
        'model_options.common.temperature': ('Temperature', 'Lower = more deterministic.'),
        'model_options.common.initial_prompt': ('Initial prompt', 'Optional text to bias the transcription.'),
        'model_options.api.model': ('API model', ''),
        'model_options.api.base_url': ('API base URL', ''),
        'model_options.api.api_key': ('API key', 'Stored in .env, never in the config file.'),
        'model_options.local.model': ('Whisper model', 'Bigger = more accurate, slower.'),
        'model_options.local.device': ('Device', 'cuda = NVIDIA GPU; cpu = processor.'),
        'model_options.local.compute_type': ('Compute type', 'int8 is fastest on CPU.'),
        'model_options.local.condition_on_previous_text': ('Use previous context', ''),
        'model_options.local.vad_filter': ('VAD filter', 'Trim silence inside the recording.'),
        'model_options.local.model_path': ('Custom model path', 'Empty = download automatically.'),
        'llm_post_processing.enabled': ('Enable AI clean-up', 'Fix punctuation and remove filler words via LLM.'),
        'llm_post_processing.provider': ('Provider', 'openai = any OpenAI-compatible; ollama = local.'),
        'llm_post_processing.base_url': ('Base URL', 'e.g. http://localhost:11434/v1 for Ollama.'),
        'llm_post_processing.model': ('Model', ''),
        'llm_post_processing.api_key': ('API key', 'Empty = use environment variable.'),
        'llm_post_processing.timeout': ('Timeout (s)', 'On timeout the raw text is used.'),
        'llm_post_processing.system_prompt': ('System prompt', ''),
        'command_mode.enabled': ('Enable Command Mode', 'Speak an instruction about the selected text.'),
        'command_mode.activation_key': ('Command hotkey', ''),
        'command_mode.source': ('Target text', 'selection = copy current selection; clipboard = as is.'),
        'command_mode.system_prompt': ('System prompt', ''),
        'dictionary.enabled': ('Enable dictionary', 'Apply your word corrections to every transcript.'),
        'snippets.enabled': ('Enable snippets', 'Expand spoken triggers into full text.'),
        'history.enabled': ('Save history', 'Keep transcripts locally (SQLite).'),
        'history.max_entries': ('Max entries', ''),
        'stats.enabled': ('Collect statistics', 'Words, WPM and daily streak.'),
    },
    'pt': {
        'misc.print_to_terminal': ('Log no terminal', 'Imprime status e transcrições no console.'),
        'misc.hide_status_window': ('Ocultar indicador flutuante', 'Não mostra a bolinha/pílula na tela.'),
        'misc.noise_on_completion': ('Som ao concluir', 'Toca um bipe após digitar o texto.'),
        'ui.language': ('Idioma da interface', '"auto" segue o idioma do sistema.'),
        'ui.theme': ('Tema', ''),
        'ui.accent_color': ('Cor de destaque', 'Cor hex usada em realces e na waveform.'),
        'recording_options.activation_key': ('Atalho de ditado', 'Teclas separadas por "+", ex.: ctrl+space.'),
        'recording_options.input_backend': ('Backend de teclado', 'Deixe em "auto", salvo se teclas não forem detectadas.'),
        'recording_options.recording_mode': ('Modo de gravação', 'Como a gravação inicia e termina.'),
        'recording_options.sound_device': ('Microfone (nº do dispositivo)', 'Vazio = padrão do sistema.'),
        'recording_options.sample_rate': ('Taxa de amostragem (Hz)', ''),
        'recording_options.silence_duration': ('Silêncio para parar (ms)', 'Duração da pausa que encerra a gravação.'),
        'recording_options.min_duration': ('Duração mínima (ms)', 'Gravações mais curtas são descartadas.'),
        'post_processing.writing_key_press_delay': ('Atraso de digitação (s)', 'Intervalo entre teclas simuladas.'),
        'post_processing.remove_trailing_period': ('Remover ponto final', ''),
        'post_processing.add_trailing_space': ('Adicionar espaço ao final', ''),
        'post_processing.remove_capitalization': ('Tudo em minúsculas', ''),
        'post_processing.copy_to_clipboard': ('Copiar para a área de transferência', 'Deixa cada transcrição pronta para colar.'),
        'post_processing.input_method': ('Método de digitação', ''),
        'model_options.use_api': ('Usar API na nuvem', 'Desligado = transcreve localmente (privado, offline).'),
        'model_options.common.language': ('Idioma falado', 'Código ISO, ex.: pt, en. Vazio = detectar.'),
        'model_options.common.temperature': ('Temperatura', 'Menor = mais determinístico.'),
        'model_options.common.initial_prompt': ('Prompt inicial', 'Texto opcional para orientar a transcrição.'),
        'model_options.api.model': ('Modelo da API', ''),
        'model_options.api.base_url': ('URL base da API', ''),
        'model_options.api.api_key': ('Chave de API', 'Guardada no .env, nunca no arquivo de config.'),
        'model_options.local.model': ('Modelo Whisper', 'Maior = mais preciso, porém mais lento.'),
        'model_options.local.device': ('Dispositivo', 'cuda = GPU NVIDIA; cpu = processador.'),
        'model_options.local.compute_type': ('Tipo de computação', 'int8 é o mais rápido em CPU.'),
        'model_options.local.condition_on_previous_text': ('Usar contexto anterior', ''),
        'model_options.local.vad_filter': ('Filtro VAD', 'Remove silêncios dentro da gravação.'),
        'model_options.local.model_path': ('Caminho de modelo próprio', 'Vazio = baixar automaticamente.'),
        'llm_post_processing.enabled': ('Ativar limpeza por IA', 'Corrige pontuação e remove hesitações via LLM.'),
        'llm_post_processing.provider': ('Provedor', 'openai = qualquer OpenAI-compat; ollama = local.'),
        'llm_post_processing.base_url': ('URL base', 'ex.: http://localhost:11434/v1 para Ollama.'),
        'llm_post_processing.model': ('Modelo', ''),
        'llm_post_processing.api_key': ('Chave de API', 'Vazio = usar variável de ambiente.'),
        'llm_post_processing.timeout': ('Timeout (s)', 'Se estourar, usa o texto sem limpeza.'),
        'llm_post_processing.system_prompt': ('Prompt de sistema', ''),
        'command_mode.enabled': ('Ativar Modo Comando', 'Fale uma instrução sobre o texto selecionado.'),
        'command_mode.activation_key': ('Atalho de comando', ''),
        'command_mode.source': ('Texto-alvo', 'selection = copia a seleção atual; clipboard = como está.'),
        'command_mode.system_prompt': ('Prompt de sistema', ''),
        'dictionary.enabled': ('Ativar dicionário', 'Aplica suas correções em toda transcrição.'),
        'snippets.enabled': ('Ativar snippets', 'Expande gatilhos falados em textos completos.'),
        'history.enabled': ('Salvar histórico', 'Guarda as transcrições localmente (SQLite).'),
        'history.max_entries': ('Máximo de entradas', ''),
        'stats.enabled': ('Coletar estatísticas', 'Palavras, PPM e sequência diária.'),
    },
}


def _path(category, sub, key):
    return f"{category}.{sub}.{key}" if sub else f"{category}.{key}"


def field_label(category, sub, key, lang=None):
    """Titulo amigavel de um campo de configuracao (fallback: chave capitalizada)."""
    lang = lang or current_language()
    meta = FIELD_META.get(lang, {}).get(_path(category, sub, key)) \
        or FIELD_META['en'].get(_path(category, sub, key))
    if meta:
        return meta[0]
    return key.replace('_', ' ').capitalize()


def field_desc(category, sub, key, lang=None):
    """Descricao curta de um campo (pode ser vazia)."""
    lang = lang or current_language()
    meta = FIELD_META.get(lang, {}).get(_path(category, sub, key)) \
        or FIELD_META['en'].get(_path(category, sub, key))
    return meta[1] if meta else ''


def section_title(category, sub=None, lang=None):
    """Titulo amigavel de uma secao do schema."""
    lang = lang or current_language()
    path = f"{category}.{sub}" if sub else category
    table = SECTION_TITLES.get(lang, {})
    return table.get(path) or table.get(category) \
        or SECTION_TITLES['en'].get(path) or category.replace('_', ' ').title()

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

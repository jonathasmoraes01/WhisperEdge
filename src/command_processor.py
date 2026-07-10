"""
Command Mode do WiprFlow: a fala vira uma INSTRUCAO sobre um texto-alvo
(selecao atual ou clipboard), processada por LLM. Ex.: "deixe mais formal",
"vire em bullets", "resuma".

Requer o LLM configurado em llm_post_processing (provider/base_url/model/chave).
Sem LLM configurado, devolve o texto-alvo sem alteracao.
"""
import time

from utils import ConfigManager


def get_target_text():
    """Obtem o texto-alvo: a selecao atual (via Ctrl+C) ou o clipboard."""
    import pyperclip
    source = ConfigManager.get_config_value('command_mode', 'source') or 'selection'

    if source == 'selection':
        try:
            from pynput.keyboard import Controller, Key
            keyboard = Controller()
            with keyboard.pressed(Key.ctrl):
                keyboard.press('c')
                keyboard.release('c')
            time.sleep(0.15)  # espera o SO atualizar o clipboard
        except Exception as e:
            ConfigManager.console_print(f'[command] copia da selecao falhou: {e}')

    try:
        return import_pyperclip_paste()
    except Exception:
        return ''


def import_pyperclip_paste():
    import pyperclip
    return pyperclip.paste() or ''


def run_command(target_text, instruction):
    """Aplica a instrucao falada ao texto-alvo via LLM. Em falha, devolve o alvo."""
    instruction = (instruction or '').strip()
    if not instruction:
        return target_text
    system_prompt = (ConfigManager.get_config_value('command_mode', 'system_prompt')
                     or 'Edite o texto conforme a instrucao e devolva apenas o resultado.')
    user_content = f"TEXTO:\n{target_text or ''}\n\nINSTRUCAO:\n{instruction}"
    try:
        from llm_cleanup import chat
        result = chat(system_prompt, user_content)
        return result or (target_text or '')
    except Exception as e:
        ConfigManager.console_print(f'[command] LLM falhou: {e}')
        return target_text or ''

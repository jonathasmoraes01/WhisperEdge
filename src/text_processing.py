"""
Pos-processamento de texto do WhisperEdge:
- Dicionario pessoal: forca correcoes de palavras/nomes/jargoes na saida.
- Snippets por voz: gatilhos falados que expandem em textos maiores.

Os dados ficam em data/dictionary.json e data/snippets.json (listas de pares),
editaveis pela UI de Settings.
"""
import json
import re

from paths import data_path
from utils import ConfigManager

DICT_FILE = 'dictionary.json'
SNIP_FILE = 'snippets.json'


def _load(name, default):
    try:
        with open(data_path(name), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default


def _save(name, data):
    try:
        with open(data_path(name), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


# --- Dicionario: [{"from": "ouvido como", "to": "correto"}] ---
def get_dictionary():
    entries = _load(DICT_FILE, [])
    return entries if isinstance(entries, list) else []


def set_dictionary(entries):
    _save(DICT_FILE, entries)


# --- Snippets: [{"trigger": "meu email", "expansion": "fulano@dominio.com"}] ---
def get_snippets():
    entries = _load(SNIP_FILE, [])
    return entries if isinstance(entries, list) else []


def set_snippets(entries):
    _save(SNIP_FILE, entries)


# --- Perfis por app: [{"match": "discord", "style": "tom casual"}] -----------
# Adapta o ESTILO da limpeza por IA conforme a janela ativa (so age quando a
# Limpeza por IA esta ligada — sem LLM nao ha como reescrever o texto).
PROFILES_FILE = 'app_profiles.json'

DEFAULT_PROFILES = [
    {'match': 'discord',
     'style': 'Tom casual e direto, como mensagem de chat entre amigos. Pode ser informal.'},
    {'match': 'whatsapp',
     'style': 'Tom casual de mensagem. Frases curtas.'},
    {'match': 'telegram',
     'style': 'Tom casual de mensagem. Frases curtas.'},
    {'match': 'antigravity',
     'style': 'O texto e um PROMPT para uma IA de programacao: estruture com clareza, '
              'objetivo primeiro e detalhes depois, remova redundancias e ambiguidades.'},
    {'match': 'cursor',
     'style': 'O texto e um PROMPT para uma IA de programacao: claro, estruturado e sem ambiguidade.'},
    {'match': 'visual studio code',
     'style': 'O texto e um PROMPT/instrucao tecnica: claro, estruturado e preciso.'},
    {'match': 'claude',
     'style': 'O texto e um PROMPT para uma IA: organize bem o pedido, contexto e criterios.'},
    {'match': 'gmail',
     'style': 'Tom profissional e cordial de e-mail.'},
    {'match': 'outlook',
     'style': 'Tom profissional e cordial de e-mail.'},
]


def get_app_profiles():
    entries = _load(PROFILES_FILE, None)
    if entries is None:
        _save(PROFILES_FILE, DEFAULT_PROFILES)
        return [dict(e) for e in DEFAULT_PROFILES]
    return entries if isinstance(entries, list) else []


def set_app_profiles(entries):
    _save(PROFILES_FILE, entries)


def style_for_window(title):
    """Instrucao de estilo para a janela ativa (substring, case-insensitive)."""
    t = (title or '').lower()
    if not t:
        return ''
    for entry in get_app_profiles():
        m = (entry.get('match') or '').lower().strip()
        if m and m in t:
            return entry.get('style') or ''
    return ''


def _replace_whole(text, needle, replacement):
    """Substitui 'needle' por 'replacement' respeitando limites de palavra,
    ignorando maiusculas/minusculas. Usa funcao no replacement para nao
    interpretar barras/grupos."""
    if not needle:
        return text
    pattern = re.compile(r'(?<!\w)' + re.escape(needle) + r'(?!\w)', re.IGNORECASE | re.UNICODE)
    return pattern.sub(lambda _m: replacement, text)


def apply_dictionary(text):
    for entry in get_dictionary():
        frm = (entry.get('from') or '').strip()
        to = entry.get('to') or ''
        if frm:
            text = _replace_whole(text, frm, to)
    return text


def apply_snippets(text):
    for entry in get_snippets():
        trigger = (entry.get('trigger') or '').strip()
        expansion = entry.get('expansion') or ''
        if trigger:
            text = _replace_whole(text, trigger, expansion)
    return text


def enhance_text(text):
    """Pipeline de aprimoramento aplicado apos a transcricao bruta.
    Ordem: LLM clean-up (opcional) -> dicionario -> snippets.
    Tudo protegido: se algo falhar, retorna o melhor texto disponivel."""
    if not text:
        return text

    # 1) Limpeza opcional por LLM (nao obrigatoria; desligavel).
    try:
        if ConfigManager.get_config_value('llm_post_processing', 'enabled'):
            from llm_cleanup import clean_up
            text = clean_up(text)
    except Exception as e:
        ConfigManager.console_print(f'[enhance] LLM clean-up ignorado: {e}')

    # 2) Dicionario pessoal.
    try:
        if ConfigManager.get_config_value('dictionary', 'enabled'):
            text = apply_dictionary(text)
    except Exception as e:
        ConfigManager.console_print(f'[enhance] dicionario ignorado: {e}')

    # 3) Snippets por voz.
    try:
        if ConfigManager.get_config_value('snippets', 'enabled'):
            text = apply_snippets(text)
    except Exception as e:
        ConfigManager.console_print(f'[enhance] snippets ignorado: {e}')

    return text

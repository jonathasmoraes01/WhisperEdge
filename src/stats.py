"""
Estatisticas de uso do WiprFlow — persistentes em data/stats.json.
Rastreia palavras ditadas, tempo de fala (para WPM), sessoes e streak diario.
"""
import json
import time
from datetime import date, timedelta

from paths import data_path
from utils import ConfigManager

_FILE = 'stats.json'
_DEFAULT = {
    'total_words': 0,
    'total_speech_seconds': 0.0,
    'sessions': 0,
    'by_day': {},          # 'YYYY-MM-DD' -> palavras
    'last_day': None,
    'streak': 0,
}


def _load():
    try:
        with open(data_path(_FILE), 'r', encoding='utf-8') as f:
            data = json.load(f)
        merged = dict(_DEFAULT)
        merged.update(data or {})
        return merged
    except Exception:
        return dict(_DEFAULT)


def _save(data):
    try:
        with open(data_path(_FILE), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def record(word_count, speech_seconds=0.0):
    """Registra um dictado nas estatisticas."""
    if not ConfigManager.get_config_value('stats', 'enabled'):
        return
    if not word_count:
        return
    data = _load()
    today = date.today().isoformat()

    # Streak diario
    if data['last_day'] != today:
        if data['last_day'] == (date.today() - timedelta(days=1)).isoformat():
            data['streak'] = (data.get('streak') or 0) + 1
        else:
            data['streak'] = 1
        data['last_day'] = today

    data['total_words'] += int(word_count)
    data['total_speech_seconds'] = float(data.get('total_speech_seconds') or 0.0) + float(speech_seconds or 0.0)
    data['sessions'] = int(data.get('sessions') or 0) + 1
    data['by_day'][today] = int(data['by_day'].get(today, 0)) + int(word_count)
    _save(data)


def get_summary():
    """Resumo pronto para a UI."""
    data = _load()
    today = date.today().isoformat()
    secs = data.get('total_speech_seconds') or 0.0
    avg_wpm = (data['total_words'] / (secs / 60.0)) if secs > 0 else 0
    return {
        'total_words': data.get('total_words', 0),
        'words_today': data.get('by_day', {}).get(today, 0),
        'avg_wpm': round(avg_wpm),
        'streak': data.get('streak', 0),
        'sessions': data.get('sessions', 0),
    }

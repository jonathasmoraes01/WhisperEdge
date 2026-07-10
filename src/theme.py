"""
Tema central do WhisperEdge. Le assets/theme.qss (template com @VAR@) e substitui
pelas cores do tema (dark/light) e a cor de destaque escolhida na config.
"""
from paths import asset_path


def _clamp(v):
    return max(0, min(255, v))


def _lighten(hex_color, amount=30):
    """Clareia uma cor hex por 'amount' (0-255)."""
    try:
        h = hex_color.lstrip('#')
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return '#%02x%02x%02x' % (_clamp(r + amount), _clamp(g + amount), _clamp(b + amount))
    except Exception:
        return hex_color


DARK = {
    'BG': '#141419',
    'PANEL': '#1e1e27',
    'PANEL2': '#282833',
    'TEXT': '#e9e9f1',
    'MUTED': '#9a9ab2',
    'BORDER': '#33333f',
}

LIGHT = {
    'BG': '#f3f3f7',
    'PANEL': '#ffffff',
    'PANEL2': '#eceef4',
    'TEXT': '#1b1b26',
    'MUTED': '#6b6b7c',
    'BORDER': '#dcdce6',
}


def get_palette():
    """Retorna o dicionario de cores efetivo (tema + accent da config)."""
    try:
        from utils import ConfigManager
        theme = ConfigManager.get_config_value('ui', 'theme') or 'dark'
        accent = ConfigManager.get_config_value('ui', 'accent_color') or '#6C5CE7'
    except Exception:
        theme, accent = 'dark', '#6C5CE7'
    palette = dict(LIGHT if theme == 'light' else DARK)
    palette['ACCENT'] = accent
    palette['ACCENT_HOVER'] = _lighten(accent, 25)
    return palette


def load_qss():
    """Le o template QSS e substitui os placeholders pelas cores efetivas."""
    palette = get_palette()
    try:
        with open(asset_path('theme.qss'), 'r', encoding='utf-8') as f:
            qss = f.read()
    except Exception:
        return ''
    for key, value in palette.items():
        qss = qss.replace('@' + key + '@', value)
    return qss


def apply_theme(app):
    """Aplica o tema a uma QApplication."""
    try:
        app.setStyleSheet(load_qss())
    except Exception:
        pass

"""
Historico de dictados do WhisperEdge — persistente em SQLite (data/history.db).
Cada entrada: timestamp, texto, app/janela ativa (quando possivel), nº de palavras.
"""
import sqlite3
import time

from paths import data_path
from utils import ConfigManager

_DB = None


def _db():
    global _DB
    if _DB is None:
        _DB = sqlite3.connect(data_path('history.db'), check_same_thread=False)
        _DB.execute(
            """CREATE TABLE IF NOT EXISTS dictations (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   ts REAL NOT NULL,
                   text TEXT NOT NULL,
                   app TEXT,
                   word_count INTEGER DEFAULT 0
               )"""
        )
        _DB.commit()
    return _DB


def get_active_window_title():
    """Titulo da janela em primeiro plano (Windows, via ctypes). Fallback: ''."""
    try:
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value or ''
    except Exception:
        return ''


def add_entry(text, app='', word_count=None):
    """Salva um dictado no historico (respeitando o toggle e o limite)."""
    if not ConfigManager.get_config_value('history', 'enabled'):
        return
    text = (text or '').strip()
    if not text:
        return
    if word_count is None:
        word_count = len(text.split())
    try:
        db = _db()
        db.execute(
            'INSERT INTO dictations (ts, text, app, word_count) VALUES (?, ?, ?, ?)',
            (time.time(), text, app or '', word_count),
        )
        db.commit()
        _prune()
    except Exception as e:
        ConfigManager.console_print(f'[history] falha ao salvar: {e}')


def _prune():
    max_entries = ConfigManager.get_config_value('history', 'max_entries') or 2000
    try:
        db = _db()
        db.execute(
            """DELETE FROM dictations WHERE id NOT IN (
                   SELECT id FROM dictations ORDER BY id DESC LIMIT ?
               )""",
            (max_entries,),
        )
        db.commit()
    except Exception:
        pass


def get_entries(limit=200):
    """Lista as entradas mais recentes: [{id, ts, text, app, word_count}]."""
    try:
        db = _db()
        rows = db.execute(
            'SELECT id, ts, text, app, word_count FROM dictations ORDER BY id DESC LIMIT ?',
            (limit,),
        ).fetchall()
        return [
            {'id': r[0], 'ts': r[1], 'text': r[2], 'app': r[3], 'word_count': r[4]}
            for r in rows
        ]
    except Exception:
        return []


def clear():
    try:
        db = _db()
        db.execute('DELETE FROM dictations')
        db.commit()
    except Exception:
        pass

"""
WhisperEdge — janela de Configuracoes redesenhada, com abas limpas:
Geral, Gravacao, Modelo, Aprimorar (LLM/Command), Dicionario, Snippets,
Historico, Estatisticas e Sobre. Tema escuro central (QSS) + i18n EN/PT.

As abas de config sao geradas a partir do schema (fonte unica da verdade);
Dicionario/Snippets tem editores em tabela; Historico e Estatisticas tem vistas
proprias. Mantem o contrato usado pelo app: sinais settings_closed/settings_saved.
"""
import os
import sys
import time

from dotenv import set_key, load_dotenv
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QSpinBox, QPlainTextEdit, QTabWidget, QScrollArea,
    QFrame, QTableWidget, QTableWidgetItem, QListWidget, QListWidgetItem, QHeaderView,
    QSizePolicy, QMessageBox, QFileDialog,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.base_window import BaseWindow
from utils import ConfigManager
from i18n import tr
import text_processing
import history as history_mod
import stats as stats_mod

load_dotenv()

# Agrupamento das secoes do schema em abas logicas.
CONFIG_TABS = [
    ('tab_general', ['misc', 'ui']),
    ('tab_recording', ['recording_options', 'post_processing']),
    ('tab_model', ['model_options']),
    ('tab_enhance', ['llm_post_processing', 'command_mode', 'dictionary', 'snippets', 'history', 'stats']),
]


class SettingsWindow(BaseWindow):
    settings_closed = pyqtSignal()
    settings_saved = pyqtSignal()

    def __init__(self):
        super().__init__(tr('settings'), 780, 660)
        self.schema = ConfigManager.get_schema()
        self.widgets = {}  # (category, sub, key) -> widget
        self._build()

    # ------------------------------------------------------------------ build
    def _build(self):
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        for tab_key, categories in CONFIG_TABS:
            self.tabs.addTab(self._config_tab(categories), tr(tab_key))

        self.tabs.addTab(self._table_tab('dictionary'), tr('tab_dictionary'))
        self.tabs.addTab(self._table_tab('snippets'), tr('tab_snippets'))
        self.tabs.addTab(self._history_tab(), tr('tab_history'))
        self.tabs.addTab(self._stats_tab(), tr('tab_stats'))
        self.tabs.addTab(self._about_tab(), tr('tab_about'))

        footer = QHBoxLayout()
        reset_btn = QPushButton(tr('reset'))
        reset_btn.setProperty('role', 'ghost')
        reset_btn.clicked.connect(self.reset_settings)
        save_btn = QPushButton(tr('save'))
        save_btn.setProperty('role', 'primary')
        save_btn.clicked.connect(self.save_settings)
        footer.addWidget(reset_btn)
        footer.addStretch(1)
        footer.addWidget(save_btn)
        self.main_layout.addLayout(footer)

    def _scroll(self, inner):
        area = QScrollArea()
        area.setWidgetResizable(True)
        area.setWidget(inner)
        area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        return area

    def _config_tab(self, categories):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)
        for category in categories:
            settings = self.schema.get(category, {})
            if not settings:
                continue
            card = QFrame()
            card.setProperty('role', 'card')
            grid = QGridLayout(card)
            grid.setContentsMargins(16, 14, 16, 14)
            grid.setVerticalSpacing(10)
            grid.setHorizontalSpacing(12)

            title = QLabel(category.replace('_', ' ').title())
            title.setProperty('role', 'subtitle')
            grid.addWidget(title, 0, 0, 1, 2)

            row = 1
            for sub, meta in settings.items():
                if isinstance(meta, dict) and 'value' in meta:
                    row = self._add_row(grid, row, category, None, sub, meta)
                else:
                    for key, leaf in meta.items():
                        row = self._add_row(grid, row, category, sub, key, leaf)
            layout.addWidget(card)
        layout.addStretch(1)
        return self._scroll(inner)

    def _add_row(self, grid, row, category, sub, key, meta):
        label = QLabel(key.replace('_', ' ').capitalize())
        label.setToolTip(meta.get('description', ''))
        widget = self._make_widget(category, sub, key, meta)
        if widget is None:
            return row
        self.widgets[(category, sub, key)] = widget
        grid.addWidget(label, row, 0)
        grid.addWidget(widget, row, 1)
        return row + 1

    def _make_widget(self, category, sub, key, meta):
        mtype = meta.get('type')
        value = self._current_value(category, sub, key, meta)

        if mtype == 'bool':
            w = QCheckBox()
            w.setChecked(bool(value))
            return w
        if mtype == 'str' and 'options' in meta:
            w = QComboBox()
            w.addItems([str(o) for o in meta['options']])
            w.setCurrentText(str(value))
            return w
        if mtype == 'int':
            w = QSpinBox()
            w.setRange(0, 100000)
            try:
                w.setValue(int(value))
            except (TypeError, ValueError):
                w.setValue(0)
            return w
        if 'prompt' in key:  # textos longos -> multi-linha
            w = QPlainTextEdit()
            w.setPlainText('' if value is None else str(value))
            w.setFixedHeight(90)
            return w
        w = QLineEdit('' if value is None else str(value))
        if key == 'api_key':
            w.setEchoMode(QLineEdit.Password)
            w.setText(os.getenv('OPENAI_API_KEY') or ('' if value is None else str(value)))
            w.setPlaceholderText('sk-…  (ou deixe vazio p/ usar variavel de ambiente)')
        return w

    def _current_value(self, category, sub, key, meta):
        if sub:
            v = ConfigManager.get_config_value(category, sub, key)
        else:
            v = ConfigManager.get_config_value(category, key)
        return meta['value'] if v is None else v

    # -------------------------------------------------------- table editors
    def _table_tab(self, kind):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        desc = QLabel(tr('dict_desc') if kind == 'dictionary' else tr('snip_desc'))
        desc.setProperty('role', 'muted')
        desc.setWordWrap(True)
        layout.addWidget(desc)

        table = QTableWidget(0, 2)
        headers = ([tr('wrong'), tr('right')] if kind == 'dictionary'
                   else [tr('trigger'), tr('replacement')])
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        layout.addWidget(table, 1)

        entries = (text_processing.get_dictionary() if kind == 'dictionary'
                   else text_processing.get_snippets())
        for e in entries:
            if kind == 'dictionary':
                self._table_add(table, e.get('from', ''), e.get('to', ''))
            else:
                self._table_add(table, e.get('trigger', ''), e.get('expansion', ''))

        buttons = QHBoxLayout()
        add_btn = QPushButton('+ ' + tr('add'))
        add_btn.clicked.connect(lambda: self._table_add(table, '', ''))
        rm_btn = QPushButton(tr('remove'))
        rm_btn.setProperty('role', 'danger')
        rm_btn.clicked.connect(lambda: table.removeRow(table.currentRow()) if table.currentRow() >= 0 else None)
        buttons.addWidget(add_btn)
        buttons.addWidget(rm_btn)
        buttons.addStretch(1)
        layout.addLayout(buttons)

        if kind == 'dictionary':
            self._dict_table = table
        else:
            self._snip_table = table
        return inner

    def _table_add(self, table, a, b):
        r = table.rowCount()
        table.insertRow(r)
        table.setItem(r, 0, QTableWidgetItem(a))
        table.setItem(r, 1, QTableWidgetItem(b))

    def _read_table(self, table, keys):
        out = []
        for r in range(table.rowCount()):
            a = table.item(r, 0).text().strip() if table.item(r, 0) else ''
            b = table.item(r, 1).text() if table.item(r, 1) else ''
            if a:
                out.append({keys[0]: a, keys[1]: b})
        return out

    # ---------------------------------------------------------- history/stats
    def _history_tab(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        self.history_list = QListWidget()
        layout.addWidget(self.history_list, 1)
        self._reload_history()

        buttons = QHBoxLayout()
        copy_btn = QPushButton(tr('copy'))
        copy_btn.clicked.connect(self._copy_history)
        clear_btn = QPushButton(tr('clear_history'))
        clear_btn.setProperty('role', 'danger')
        clear_btn.clicked.connect(self._clear_history)
        buttons.addWidget(copy_btn)
        buttons.addWidget(clear_btn)
        buttons.addStretch(1)
        layout.addLayout(buttons)
        return inner

    def _reload_history(self):
        self.history_list.clear()
        entries = history_mod.get_entries(200)
        if not entries:
            self.history_list.addItem(tr('no_history'))
            return
        for e in entries:
            when = time.strftime('%d/%m %H:%M', time.localtime(e['ts']))
            app = (e.get('app') or '')[:28]
            preview = ' '.join((e['text'] or '').split())
            item = QListWidgetItem(f"[{when}] {app}\n{preview}")
            item.setData(Qt.UserRole, e['text'])
            self.history_list.addItem(item)

    def _copy_history(self):
        item = self.history_list.currentItem()
        if item and item.data(Qt.UserRole):
            QApplication.clipboard().setText(item.data(Qt.UserRole))

    def _clear_history(self):
        history_mod.clear()
        self._reload_history()

    def _stats_tab(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        s = stats_mod.get_summary()
        cards = QGridLayout()
        cards.setSpacing(12)
        data = [
            (tr('words_total'), s['total_words']),
            (tr('words_today'), s['words_today']),
            (tr('avg_wpm'), s['avg_wpm']),
            (tr('streak'), f"{s['streak']} 🔥"),
            (tr('sessions'), s['sessions']),
        ]
        for i, (title, value) in enumerate(data):
            card = QFrame()
            card.setProperty('role', 'card')
            v = QVBoxLayout(card)
            v.setContentsMargins(18, 16, 18, 16)
            num = QLabel(str(value))
            num.setProperty('role', 'stat')
            cap = QLabel(title)
            cap.setProperty('role', 'muted')
            v.addWidget(num)
            v.addWidget(cap)
            cards.addWidget(card, i // 2, i % 2)
        layout.addLayout(cards)
        layout.addStretch(1)
        return inner

    def _about_tab(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(10)
        name = QLabel('WhisperEdge')
        name.setProperty('role', 'title')
        tagline = QLabel(tr('app_tagline'))
        tagline.setProperty('role', 'subtitle')
        info = QLabel(
            'Ditado por voz local com faster-whisper.\n\n'
            'Baseado no projeto open-source WhisperWriter (savbell/whisper-writer).\n'
            'Licenca: GNU GPL-3.0. Recursos de LLM/nuvem sao opcionais e desligaveis.'
        )
        info.setWordWrap(True)
        info.setProperty('role', 'muted')
        layout.addWidget(name)
        layout.addWidget(tagline)
        layout.addSpacing(8)
        layout.addWidget(info)
        layout.addStretch(1)
        return inner

    # ------------------------------------------------------------- save/reset
    def save_settings(self):
        for (category, sub, key), widget in self.widgets.items():
            meta = self._meta_for(category, sub, key)
            value = self._widget_value(widget, meta.get('type'), key)
            if sub:
                ConfigManager.set_config_value(value, category, sub, key)
            else:
                ConfigManager.set_config_value(value, category, key)

        # Chave de API vai para o .env (nunca para o config).
        api_key = ConfigManager.get_config_value('model_options', 'api', 'api_key') or ''
        try:
            set_key('.env', 'OPENAI_API_KEY', api_key)
            os.environ['OPENAI_API_KEY'] = api_key
        except Exception:
            pass
        ConfigManager.set_config_value(None, 'model_options', 'api', 'api_key')

        # Dicionario e snippets (tabelas).
        try:
            text_processing.set_dictionary(self._read_table(self._dict_table, ('from', 'to')))
            text_processing.set_snippets(self._read_table(self._snip_table, ('trigger', 'expansion')))
        except Exception:
            pass

        ConfigManager.save_config()
        QMessageBox.information(self, 'WhisperEdge', tr('saved'))
        self.settings_saved.emit()
        self.close()

    def _meta_for(self, category, sub, key):
        node = self.schema.get(category, {})
        if sub:
            return node.get(sub, {}).get(key, {})
        return node.get(key, {})

    def _widget_value(self, widget, mtype, key):
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        if isinstance(widget, QComboBox):
            return widget.currentText() or None
        if isinstance(widget, QSpinBox):
            return widget.value()
        if isinstance(widget, QPlainTextEdit):
            return widget.toPlainText() or None
        if isinstance(widget, QLineEdit):
            text = widget.text()
            if mtype == 'int':
                return int(text) if text else None
            if mtype == 'float':
                return float(text) if text else None
            return text or None
        return None

    def reset_settings(self):
        ConfigManager.reload_config()
        for (category, sub, key), widget in self.widgets.items():
            meta = self._meta_for(category, sub, key)
            value = self._current_value(category, sub, key, meta)
            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                widget.setCurrentText(str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(int(value) if value else 0)
            elif isinstance(widget, QPlainTextEdit):
                widget.setPlainText('' if value is None else str(value))
            elif isinstance(widget, QLineEdit):
                widget.setText('' if value is None else str(value))

    def closeEvent(self, event):
        ConfigManager.reload_config()  # descarta alteracoes nao salvas
        self.settings_closed.emit()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ConfigManager.initialize()
    from theme import apply_theme
    apply_theme(app)
    w = SettingsWindow()
    w.show()
    sys.exit(app.exec_())

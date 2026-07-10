"""
WhisperEdge — janela de Configurações.

Layout estilo SuperWhisper: sidebar de navegação à esquerda (texto, sem emojis,
com barra de destaque no item ativo) e páginas à direita. Cada configuração é
uma linha com título + descrição à esquerda e o controle à direita (switch para
booleanos). Rótulos amigáveis PT/EN vêm de i18n.FIELD_META — o schema segue
sendo a fonte da verdade dos campos.
"""
import os
import sys
import time

from dotenv import set_key, load_dotenv
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QCheckBox, QSpinBox, QPlainTextEdit, QStackedWidget,
    QScrollArea, QFrame, QTableWidget, QTableWidgetItem, QListWidget,
    QListWidgetItem, QHeaderView, QGridLayout, QMessageBox,
)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.base_window import BaseWindow
from ui.widgets import Switch
from utils import ConfigManager
from i18n import tr, field_label, field_desc, section_title
import text_processing
import history as history_mod
import stats as stats_mod

load_dotenv()

APP_VERSION = '1.1'

# Páginas de configuração: (chave i18n, categorias do schema)
CONFIG_PAGES = [
    ('tab_general', ['misc', 'ui']),
    ('tab_recording', ['recording_options', 'post_processing']),
    ('tab_model', ['model_options']),
    ('tab_enhance', ['llm_post_processing', 'command_mode', 'dictionary',
                     'snippets', 'history', 'stats']),
]

CONTROL_WIDTH = 230  # largura padrão dos controles à direita


class SettingsWindow(BaseWindow):
    settings_closed = pyqtSignal()
    settings_saved = pyqtSignal()

    def __init__(self):
        super().__init__(tr('settings'), 860, 640)
        self.schema = ConfigManager.get_schema()
        self.widgets = {}  # (category, sub, key) -> widget
        self._build()

    # ------------------------------------------------------------------ build
    def _build(self):
        body = QHBoxLayout()
        body.setContentsMargins(4, 4, 4, 0)
        body.setSpacing(16)

        # ---- Sidebar
        side = QVBoxLayout()
        side.setSpacing(2)
        brand = QLabel('WhisperEdge')
        brand.setProperty('role', 'title')
        tagline = QLabel(tr('app_tagline'))
        tagline.setProperty('role', 'subtitle')
        side.addWidget(brand)
        side.addWidget(tagline)
        side.addSpacing(14)

        self.nav = QListWidget()
        self.nav.setObjectName('nav')
        self.nav.setFixedWidth(180)
        side.addWidget(self.nav, 1)

        version = QLabel(f'v{APP_VERSION}')
        version.setProperty('role', 'muted')
        side.addWidget(version)
        body.addLayout(side)

        # ---- Páginas
        self.stack = QStackedWidget()
        nav_items = [tr(k) for k, _ in CONFIG_PAGES] + [
            tr('tab_dictionary'), tr('tab_snippets'),
            tr('tab_history'), tr('tab_stats'), tr('tab_about'),
        ]
        pages = [self._config_page(cats) for _, cats in CONFIG_PAGES] + [
            self._table_page('dictionary'), self._table_page('snippets'),
            self._history_page(), self._stats_page(), self._about_page(),
        ]
        for text, page in zip(nav_items, pages):
            QListWidgetItem(text, self.nav)
            self.stack.addWidget(page)
        self.nav.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.nav.setCurrentRow(0)
        body.addWidget(self.stack, 1)

        self.main_layout.addLayout(body, 1)

        # ---- Rodapé
        footer = QHBoxLayout()
        footer.setContentsMargins(4, 8, 4, 4)
        reset_btn = QPushButton(tr('reset'))
        reset_btn.setProperty('role', 'ghost')
        reset_btn.clicked.connect(self.reset_settings)
        save_btn = QPushButton(tr('save'))
        save_btn.setProperty('role', 'primary')
        save_btn.setMinimumWidth(120)
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

    # ----------------------------------------------------------- config pages
    def _config_page(self, categories):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(4, 4, 12, 12)
        layout.setSpacing(14)

        for category in categories:
            settings = self.schema.get(category, {})
            if not settings:
                continue
            # separa folhas (sem sub) de subgrupos
            leafs = [(k, m) for k, m in settings.items()
                     if isinstance(m, dict) and 'value' in m]
            groups = [(k, m) for k, m in settings.items()
                      if not (isinstance(m, dict) and 'value' in m)]

            if leafs:
                layout.addWidget(self._card(section_title(category),
                                            [(category, None, k, m) for k, m in leafs]))
            for sub, submeta in groups:
                layout.addWidget(self._card(section_title(category, sub),
                                            [(category, sub, k, m) for k, m in submeta.items()]))
        layout.addStretch(1)
        return self._scroll(inner)

    def _card(self, title, fields):
        card = QFrame()
        card.setProperty('role', 'card')
        v = QVBoxLayout(card)
        v.setContentsMargins(18, 14, 18, 14)
        v.setSpacing(0)

        head = QLabel(title.upper())
        head.setProperty('role', 'section')
        v.addWidget(head)
        v.addSpacing(6)

        for i, (category, sub, key, meta) in enumerate(fields):
            if i > 0:
                line = QFrame()
                line.setProperty('role', 'hline')
                line.setFixedHeight(1)
                v.addWidget(line)
            v.addWidget(self._row(category, sub, key, meta))
        return card

    def _row(self, category, sub, key, meta):
        """Linha de configuração: título+descrição à esquerda, controle à direita.
        Prompts (textos longos) ocupam a largura toda, abaixo do título."""
        roww = QWidget()
        control = self._make_widget(category, sub, key, meta)
        self.widgets[(category, sub, key)] = control

        name = QLabel(field_label(category, sub, key))
        name.setProperty('role', 'fieldname')
        desc_text = field_desc(category, sub, key) or meta.get('description', '')
        desc = QLabel(desc_text)
        desc.setProperty('role', 'fielddesc')
        desc.setWordWrap(True)
        desc.setVisible(bool(desc_text))

        left = QVBoxLayout()
        left.setSpacing(2)
        left.addWidget(name)
        left.addWidget(desc)

        if isinstance(control, QPlainTextEdit):
            v = QVBoxLayout(roww)
            v.setContentsMargins(0, 10, 0, 10)
            v.setSpacing(6)
            v.addLayout(left)
            v.addWidget(control)
        else:
            h = QHBoxLayout(roww)
            h.setContentsMargins(0, 10, 0, 10)
            h.setSpacing(16)
            h.addLayout(left, 1)
            if not isinstance(control, Switch):
                control.setFixedWidth(CONTROL_WIDTH)
            h.addWidget(control, 0, Qt.AlignRight | Qt.AlignVCenter)
        return roww

    def _make_widget(self, category, sub, key, meta):
        mtype = meta.get('type')
        value = self._current_value(category, sub, key, meta)

        if mtype == 'bool':
            w = Switch()
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
        if 'prompt' in key:
            w = QPlainTextEdit()
            w.setPlainText('' if value is None else str(value))
            w.setFixedHeight(84)
            return w
        w = QLineEdit('' if value is None else str(value))
        if key == 'api_key':
            w.setEchoMode(QLineEdit.Password)
            w.setText(os.getenv('OPENAI_API_KEY') or ('' if value is None else str(value)))
            w.setPlaceholderText('sk-…')
        return w

    def _current_value(self, category, sub, key, meta):
        if sub:
            v = ConfigManager.get_config_value(category, sub, key)
        else:
            v = ConfigManager.get_config_value(category, key)
        return meta['value'] if v is None else v

    # ----------------------------------------------------------- table pages
    def _table_page(self, kind):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(4, 4, 12, 12)
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
        table.setShowGrid(False)
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
        rm_btn.clicked.connect(
            lambda: table.removeRow(table.currentRow()) if table.currentRow() >= 0 else None)
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

    # --------------------------------------------------------- history/stats
    def _history_page(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(4, 4, 12, 12)
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
            app = (e.get('app') or '')[:34]
            preview = ' '.join((e['text'] or '').split())
            if len(preview) > 120:
                preview = preview[:117] + '…'
            item = QListWidgetItem(f"{when}   {app}\n{preview}")
            item.setData(Qt.UserRole, e['text'])
            self.history_list.addItem(item)

    def _copy_history(self):
        item = self.history_list.currentItem()
        if item and item.data(Qt.UserRole):
            QApplication.clipboard().setText(item.data(Qt.UserRole))

    def _clear_history(self):
        history_mod.clear()
        self._reload_history()

    def _stats_page(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(4, 4, 12, 12)
        layout.setSpacing(14)

        s = stats_mod.get_summary()
        cards = QGridLayout()
        cards.setSpacing(12)
        data = [
            (tr('words_total'), f"{s['total_words']:,}".replace(',', '.')),
            (tr('words_today'), f"{s['words_today']:,}".replace(',', '.')),
            (tr('avg_wpm'), s['avg_wpm']),
            (tr('streak'), s['streak']),
            (tr('sessions'), f"{s['sessions']:,}".replace(',', '.')),
        ]
        for i, (title, value) in enumerate(data):
            card = QFrame()
            card.setProperty('role', 'card')
            v = QVBoxLayout(card)
            v.setContentsMargins(18, 16, 18, 16)
            v.setSpacing(4)
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

    def _about_page(self):
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(8)
        name = QLabel('WhisperEdge')
        name.setProperty('role', 'title')
        tagline = QLabel(tr('app_tagline'))
        tagline.setProperty('role', 'subtitle')
        info = QLabel(
            f'v{APP_VERSION} — ditado por voz local com faster-whisper.\n\n'
            'Baseado no projeto open-source WhisperWriter (savbell/whisper-writer).\n'
            'Licença: GNU GPL-3.0. Recursos de LLM/nuvem são opcionais e desligáveis.'
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
            value = self._widget_value(widget, meta.get('type'))
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

    def _widget_value(self, widget, mtype):
        if isinstance(widget, QCheckBox):  # inclui Switch
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
        ConfigManager.reload_config()  # descarta alterações não salvas
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

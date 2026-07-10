import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.base_window import BaseWindow
from i18n import tr
from utils import ConfigManager


class MainWindow(BaseWindow):
    openSettings = pyqtSignal()
    startListening = pyqtSignal()
    closeApp = pyqtSignal()

    def __init__(self):
        """Initialize the main window (acessivel pelo icone da bandeja)."""
        super().__init__('WiprFlow', 360, 210)
        self.initMainUI()

    def initMainUI(self):
        """Cabecalho da marca + atalho atual + botao de configuracoes."""
        title = QLabel('WiprFlow')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignCenter)

        tagline = QLabel(tr('app_tagline'))
        tagline.setProperty('role', 'subtitle')
        tagline.setAlignment(Qt.AlignCenter)

        hotkey = ConfigManager.get_config_value('recording_options', 'activation_key') or ''
        hint = QLabel(f"⌨  {hotkey}")
        hint.setProperty('role', 'muted')
        hint.setAlignment(Qt.AlignCenter)

        settings_btn = QPushButton(tr('settings'))
        settings_btn.setProperty('role', 'primary')
        settings_btn.setFont(QFont('Segoe UI', 10))
        settings_btn.setFixedHeight(40)
        settings_btn.clicked.connect(self.openSettings.emit)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(settings_btn)
        button_layout.addStretch(1)

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(tagline)
        self.main_layout.addWidget(hint)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch(1)

    def closeEvent(self, event):
        """Fechar a janela apenas a esconde — sair de vez e pela bandeja (Exit)."""
        event.ignore()
        self.hide()

    def startPressed(self):
        """Emit the startListening signal when start is requested."""
        self.startListening.emit()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ConfigManager.initialize()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

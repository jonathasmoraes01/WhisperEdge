import os
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.base_window import BaseWindow
from ui.widgets import icon_pixmap
from i18n import tr
from utils import ConfigManager


class MainWindow(BaseWindow):
    openSettings = pyqtSignal()
    startListening = pyqtSignal()
    closeApp = pyqtSignal()

    def __init__(self):
        """Janela principal (acessivel pelo icone da bandeja)."""
        super().__init__('WhisperEdge', 380, 240)
        self.initMainUI()

    def initMainUI(self):
        """Marca + atalho atual (chip) + botao de configuracoes."""
        logo = QLabel()
        logo.setPixmap(icon_pixmap('logo', 52))
        logo.setAlignment(Qt.AlignCenter)

        title = QLabel('WhisperEdge')
        title.setProperty('role', 'title')
        title.setAlignment(Qt.AlignCenter)

        tagline = QLabel(tr('app_tagline'))
        tagline.setProperty('role', 'subtitle')
        tagline.setAlignment(Qt.AlignCenter)

        hotkey = ConfigManager.get_config_value('recording_options', 'activation_key') or ''
        chip = QLabel(hotkey.replace('+', ' + '))
        chip.setProperty('role', 'kbd')
        chip.setAlignment(Qt.AlignCenter)
        chip_row = QHBoxLayout()
        chip_row.addStretch(1)
        chip_row.addWidget(chip)
        chip_row.addStretch(1)

        settings_btn = QPushButton(tr('settings'))
        settings_btn.setProperty('role', 'primary')
        settings_btn.setFont(QFont('Segoe UI', 10))
        settings_btn.setFixedHeight(38)
        settings_btn.setMinimumWidth(160)
        settings_btn.clicked.connect(self.openSettings.emit)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(settings_btn)
        button_layout.addStretch(1)

        self.main_layout.addStretch(1)
        self.main_layout.addWidget(logo)
        self.main_layout.addSpacing(6)
        self.main_layout.addWidget(title)
        self.main_layout.addWidget(tagline)
        self.main_layout.addSpacing(10)
        self.main_layout.addLayout(chip_row)
        self.main_layout.addSpacing(14)
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

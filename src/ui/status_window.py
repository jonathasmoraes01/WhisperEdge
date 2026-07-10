"""
WhisperEdge — indicador flutuante persistente ("orb") com waveform reativa.

- Ocioso: uma pílula pequena e discreta na parte inferior-central, mostrando que
  o app está aberto. A waveform fica praticamente plana.
- Hover: expande e mostra mini-controles (gravar / configurações / janela).
- Gravando: a waveform reage à VOZ REAL (níveis vindos do ResultThread) — parada
  no silêncio, animada quando você fala.
- Transcrevendo: pulso indeterminado suave.

Não rouba o foco da janela-alvo (WA_ShowWithoutActivating).
"""
import os
import sys
import math
from collections import deque

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QToolButton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from i18n import tr
from theme import get_palette


class Waveform(QWidget):
    """Forma de onda. Modos: 'flat' (plana), 'live' (reage a push_level da voz),
    'pulse' (transcrevendo)."""

    def __init__(self, bars=30, width=132, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, 26)
        self.n = bars
        self.levels = deque([0.06] * self.n, maxlen=self.n)
        self.mode = 'flat'
        self.phase = 0.0
        self.accent = QColor(get_palette().get('ACCENT', '#6C5CE7'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(55)

    def set_mode(self, mode):
        self.mode = mode
        self.accent = QColor(get_palette().get('ACCENT', '#6C5CE7'))

    def push_level(self, level):
        """Recebe o nível de áudio real (0..1) durante a gravação."""
        if self.mode == 'live':
            self.levels.append(max(0.06, min(1.0, level)))
            self.update()

    def _tick(self):
        if self.mode == 'flat':
            last = self.levels[-1] if self.levels else 0.06
            self.levels.append(max(0.06, last * 0.6))  # relaxa suave até a base
            self.update()
        elif self.mode == 'pulse':
            self.phase += 0.28
            self.levels.append(0.5 + 0.4 * math.sin(self.phase))
            self.update()
        # 'live' é atualizado por push_level

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        w, h = self.width(), self.height()
        gap = 2
        bar_w = (w - gap * (self.n - 1)) / self.n
        levels = list(self.levels)
        for i, lv in enumerate(levels):
            bh = max(2.0, lv * h)
            x = i * (bar_w + gap)
            y = (h - bh) / 2
            color = QColor(self.accent)
            color.setAlpha(120 + int(135 * lv))
            p.setBrush(QBrush(color))
            p.drawRoundedRect(QRectF(x, y, bar_w, bh), bar_w / 2, bar_w / 2)


class StatusWindow(QWidget):
    """Indicador flutuante persistente. Interface p/ o app:
    updateStatus(str), setLevel(float), show(); sinais de controle."""

    statusSignal = pyqtSignal(str)
    closeSignal = pyqtSignal()          # compat (não usado no modo persistente)
    recordClicked = pyqtSignal()
    settingsClicked = pyqtSignal()
    expandClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.state = 'idle'      # idle | recording | transcribing
        self.hovered = False
        self._build()
        self.statusSignal.connect(self.updateStatus)

    def _build(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(14, 7, 14, 7)
        self.layout.setSpacing(10)

        self.wave = Waveform()

        self.label = QLabel(tr('status_recording'))
        self.label.setFont(QFont('Segoe UI', 9, QFont.DemiBold))

        # Mini-controles (aparecem no hover, quando ocioso)
        self.controls = QWidget()
        cl = QHBoxLayout(self.controls)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(6)
        self.btn_record = self._icon_button('●', tr('status_recording'), self.recordClicked)
        self.btn_settings = self._icon_button('⚙', tr('settings'), self.settingsClicked)
        self.btn_expand = self._icon_button('⤢', tr('open_main'), self.expandClicked)
        cl.addWidget(self.btn_record)
        cl.addWidget(self.btn_settings)
        cl.addWidget(self.btn_expand)

        self.layout.addWidget(self.wave)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.controls)

        self._apply_colors()
        self._relayout()

    def _icon_button(self, glyph, tip, signal):
        b = QToolButton()
        b.setText(glyph)
        b.setToolTip(tip)
        b.setCursor(Qt.PointingHandCursor)
        b.setFixedSize(26, 26)
        b.clicked.connect(signal.emit)
        pal = get_palette()
        b.setStyleSheet(
            f"QToolButton {{ background: {pal.get('PANEL2', '#282833')}; color: {pal.get('TEXT', '#e9e9f1')};"
            f" border: none; border-radius: 13px; font-size: 12px; }}"
            f"QToolButton:hover {{ background: {pal.get('ACCENT', '#6C5CE7')}; color: white; }}"
        )
        return b

    def _apply_colors(self):
        pal = get_palette()
        self._bg = QColor(pal.get('PANEL', '#1e1e27'))
        self._bg.setAlpha(240)
        self.label.setStyleSheet(f"color: {pal.get('TEXT', '#e9e9f1')}; background: transparent;")

    def _relayout(self):
        """Ajusta o que aparece e o tamanho conforme estado/hover, mantendo a
        base centralizada na parte inferior da tela."""
        recording = self.state in ('recording', 'transcribing')
        show_controls = (self.state == 'idle' and self.hovered)
        show_wave = not show_controls
        show_label = recording

        self.wave.setVisible(show_wave)
        self.label.setVisible(show_label)
        self.controls.setVisible(show_controls)

        if show_controls:
            self.wave.setFixedWidth(0)
            width = 132
        elif recording:
            self.wave.setFixedWidth(132)
            width = 250
        elif self.hovered:
            self.wave.setFixedWidth(96)
            width = 128
        else:
            # ocioso e sem hover: pílula compacta e discreta
            self.wave.setFixedWidth(64)
            width = 92

        self.setFixedSize(width, 40)
        self._center_bottom()
        self.update()

    def _center_bottom(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() - self.height() - 90
        self.move(x, y)

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        r = self.height() / 2
        path.addRoundedRect(QRectF(self.rect()), r, r)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawPath(path)

    # ------------------------------------------------------------- interacoes
    def enterEvent(self, _event):
        self.hovered = True
        self._relayout()

    def leaveEvent(self, _event):
        self.hovered = False
        self._relayout()

    def show(self):
        self._apply_colors()
        self._relayout()
        super().show()
        self.raise_()

    @pyqtSlot(float)
    def setLevel(self, level):
        self.wave.push_level(level)

    @pyqtSlot(str)
    def updateStatus(self, status):
        if status == 'recording':
            self.state = 'recording'
            self.label.setText(tr('status_recording'))
            self.wave.set_mode('live')
        elif status == 'transcribing':
            self.state = 'transcribing'
            self.label.setText(tr('status_transcribing'))
            self.wave.set_mode('pulse')
        elif status in ('idle', 'error', 'cancel'):
            self.state = 'idle'
            self.wave.set_mode('flat')
        self._apply_colors()
        self._relayout()


if __name__ == '__main__':
    import random
    app = QApplication(sys.argv)
    w = StatusWindow()
    w.show()
    w.statusSignal.emit('recording')
    t = QTimer()
    t.timeout.connect(lambda: w.setLevel(random.random()))
    t.start(60)
    QTimer.singleShot(4000, lambda: w.statusSignal.emit('transcribing'))
    QTimer.singleShot(7000, lambda: w.statusSignal.emit('idle'))
    sys.exit(app.exec_())

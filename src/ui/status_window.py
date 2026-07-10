"""
WhisperEdge — pilula de status flutuante com waveform animada.

Aparece discretamente na parte inferior-central da tela durante a gravacao e a
transcricao. Nao rouba o foco da janela-alvo (WA_ShowWithoutActivating), para que
o texto seja digitado no lugar certo. Visual escuro, cantos arredondados, com uma
forma de onda animada — a assinatura visual do WhisperEdge.
"""
import os
import sys
import math

from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QTimer, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from i18n import tr
from theme import get_palette


class Waveform(QWidget):
    """Pequena forma de onda animada (barras). Modo 'recording' = viva;
    'transcribing'/'thinking' = onda viajante suave; parada = plana."""

    def __init__(self, bars=22, parent=None):
        super().__init__(parent)
        self.setFixedSize(120, 28)
        self.n = bars
        self.phase = 0.0
        self.mode = 'idle'
        self.levels = [0.12] * self.n
        self.accent = QColor(get_palette().get('ACCENT', '#6C5CE7'))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)

    def start(self, mode='recording'):
        self.mode = mode
        self.accent = QColor(get_palette().get('ACCENT', '#6C5CE7'))
        if not self.timer.isActive():
            self.timer.start(45)

    def stop(self):
        self.mode = 'idle'
        self.timer.stop()
        self.levels = [0.12] * self.n
        self.update()

    def _tick(self):
        self.phase += 0.35
        new = []
        for i in range(self.n):
            if self.mode == 'recording':
                # Onda viva com leve variacao por barra.
                base = 0.5 + 0.42 * math.sin(self.phase + i * 0.55)
                jitter = 0.12 * math.sin(self.phase * 2.3 + i)
                val = max(0.08, min(1.0, abs(base) + jitter))
            elif self.mode in ('transcribing', 'thinking'):
                # Pulso viajante suave (indeterminado).
                d = abs(((i / max(1, self.n - 1)) - ((self.phase * 0.08) % 1.0)))
                val = max(0.12, 0.9 * math.exp(-((d * 3.0) ** 2)))
            else:
                val = 0.12
            new.append(val)
        self.levels = new
        self.update()

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        w, h = self.width(), self.height()
        gap = 3
        bar_w = (w - gap * (self.n - 1)) / self.n
        for i, lv in enumerate(self.levels):
            bh = max(3.0, lv * h)
            x = i * (bar_w + gap)
            y = (h - bh) / 2
            color = QColor(self.accent)
            color.setAlpha(150 + int(105 * lv))
            p.setBrush(QBrush(color))
            p.drawRoundedRect(QRectF(x, y, bar_w, bh), bar_w / 2, bar_w / 2)


class StatusWindow(QWidget):
    """Pilula flutuante de status. Interface compativel com o app:
    updateStatus(str), sinal closeSignal, show()."""

    statusSignal = pyqtSignal(str)
    closeSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build()
        self.statusSignal.connect(self.updateStatus)

    def _build(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # Nao roubar foco da janela-alvo:
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setFixedSize(260, 56)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(18, 8, 18, 8)
        layout.setSpacing(12)

        self.dot = QLabel('●')
        self.dot.setFont(QFont('Segoe UI', 11))

        self.waveform = Waveform()

        self.label = QLabel(tr('status_recording'))
        self.label.setFont(QFont('Segoe UI', 10, QFont.DemiBold))

        layout.addWidget(self.dot)
        layout.addWidget(self.waveform, 1)
        layout.addWidget(self.label)

        self._apply_colors()

    def _apply_colors(self):
        pal = get_palette()
        self._bg = QColor(pal.get('PANEL', '#1e1e27'))
        self._bg.setAlpha(238)
        self._accent = pal.get('ACCENT', '#6C5CE7')
        self.label.setStyleSheet(f"color: {pal.get('TEXT', '#e9e9f1')}; background: transparent;")
        self.dot.setStyleSheet(f"color: {self._accent}; background: transparent;")

    def paintEvent(self, _event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 28, 28)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(self._bg))
        p.drawPath(path)

    def _center_bottom(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = screen.height() - self.height() - 110
        self.move(x, y)

    def show(self):
        self._apply_colors()
        self._center_bottom()
        super().show()
        self.raise_()

    @pyqtSlot(str)
    def updateStatus(self, status):
        if status == 'recording':
            self.label.setText(tr('status_recording'))
            self.waveform.start('recording')
            self.show()
        elif status == 'transcribing':
            self.label.setText(tr('status_transcribing'))
            self.waveform.start('transcribing')
        elif status == 'thinking':
            self.label.setText(tr('status_thinking'))
            self.waveform.start('thinking')
        elif status in ('idle', 'error', 'cancel'):
            self.waveform.stop()
            self.hide()

    def closeEvent(self, event):
        self.closeSignal.emit()
        super().closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = StatusWindow()
    w.statusSignal.emit('recording')
    QTimer.singleShot(3000, lambda: w.statusSignal.emit('transcribing'))
    QTimer.singleShot(6000, lambda: w.statusSignal.emit('idle'))
    sys.exit(app.exec_())

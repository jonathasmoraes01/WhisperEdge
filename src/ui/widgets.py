"""
WhisperEdge — widgets e ícones desenhados em código (sem emojis/imagens externas).

- Switch: toggle iOS-like (subclasse de QCheckBox — compatível com isChecked()).
- icon_pixmap(kind): ícones minimalistas desenhados com QPainter
  ('record', 'settings', 'expand', 'logo').
"""
import os
import sys

from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QPixmap, QIcon
from PyQt5.QtWidgets import QCheckBox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from theme import get_palette


class Switch(QCheckBox):
    """Toggle estilo interruptor. Herda QCheckBox, então isChecked()/setChecked()
    continuam funcionando no fluxo de salvar/restaurar das Configurações."""

    W, H = 40, 22

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(self.W, self.H)
        self.setCursor(Qt.PointingHandCursor)

    def hitButton(self, pos):
        return self.rect().contains(pos)

    def paintEvent(self, _event):
        pal = get_palette()
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)

        # trilho
        if self.isChecked():
            track = QColor(pal.get('ACCENT', '#6C5CE7'))
        else:
            track = QColor(pal.get('PANEL2', '#20202a'))
            p.setPen(QPen(QColor(pal.get('BORDER', '#2a2a36')), 1))
        p.setBrush(QBrush(track))
        p.drawRoundedRect(QRectF(0.5, 0.5, self.W - 1, self.H - 1),
                          (self.H - 1) / 2, (self.H - 1) / 2)

        # botao (knob)
        p.setPen(Qt.NoPen)
        knob_d = self.H - 6
        x = self.W - knob_d - 3 if self.isChecked() else 3
        p.setBrush(QBrush(QColor('#ffffff')))
        p.drawEllipse(QRectF(x, 3, knob_d, knob_d))


def icon_pixmap(kind, size=16, color=None):
    """Desenha um ícone minimalista e devolve um QPixmap transparente."""
    pal = get_palette()
    color = QColor(color or pal.get('TEXT', '#ececf4'))
    accent = QColor(pal.get('ACCENT', '#6C5CE7'))

    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    s = float(size)

    if kind == 'record':
        # circulo preenchido (gravar)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(accent))
        r = s * 0.30
        p.drawEllipse(QPointF(s / 2, s / 2), r, r)

    elif kind == 'settings':
        # dois "sliders" horizontais com knobs (estilo ajustes moderno)
        pen = QPen(color, max(1.6, s * 0.11), Qt.SolidLine, Qt.RoundCap)
        p.setPen(pen)
        y1, y2 = s * 0.34, s * 0.66
        p.drawLine(QPointF(s * 0.15, y1), QPointF(s * 0.85, y1))
        p.drawLine(QPointF(s * 0.15, y2), QPointF(s * 0.85, y2))
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(color))
        r = s * 0.12
        p.drawEllipse(QPointF(s * 0.62, y1), r, r)
        p.drawEllipse(QPointF(s * 0.38, y2), r, r)

    elif kind == 'expand':
        # duas setas diagonais (expandir)
        pen = QPen(color, max(1.6, s * 0.11), Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        p.setPen(pen)
        m, a = s * 0.20, s * 0.26   # margem e tamanho da ponta
        # canto superior-direito
        p.drawLine(QPointF(s - m, m), QPointF(s * 0.56, s * 0.44))
        p.drawLine(QPointF(s - m, m), QPointF(s - m - a, m))
        p.drawLine(QPointF(s - m, m), QPointF(s - m, m + a))
        # canto inferior-esquerdo
        p.drawLine(QPointF(m, s - m), QPointF(s * 0.44, s * 0.56))
        p.drawLine(QPointF(m, s - m), QPointF(m + a, s - m))
        p.drawLine(QPointF(m, s - m), QPointF(m, s - m - a))

    elif kind == 'logo':
        # marca: quadrado arredondado accent + 3 barras brancas (waveform)
        p.setPen(Qt.NoPen)
        p.setBrush(QBrush(accent))
        p.drawRoundedRect(QRectF(0, 0, s, s), s * 0.24, s * 0.24)
        p.setBrush(QBrush(QColor(255, 255, 255, 235)))
        bw = s * 0.10
        for i, h in enumerate((0.34, 0.58, 0.40)):
            x = s * (0.28 + i * 0.22) - bw / 2
            bh = s * h
            p.drawRoundedRect(QRectF(x, (s - bh) / 2, bw, bh), bw / 2, bw / 2)

    p.end()
    return pm


def icon(kind, size=16, color=None):
    return QIcon(icon_pixmap(kind, size, color))

"""Caminhos centrais do WhisperEdge (raiz do app, pasta de dados, assets)."""
import os

# Raiz do repositorio (um nivel acima de src/)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(APP_ROOT, 'data')
ASSETS_DIR = os.path.join(APP_ROOT, 'assets')


def data_path(name):
    """Retorna um caminho dentro de data/, garantindo que a pasta exista."""
    os.makedirs(DATA_DIR, exist_ok=True)
    return os.path.join(DATA_DIR, name)


def asset_path(name):
    """Retorna um caminho dentro de assets/."""
    return os.path.join(ASSETS_DIR, name)

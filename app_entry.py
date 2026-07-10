"""
Entry point para o executavel (PyInstaller). Nao usado no modo fonte
(use run.py). Define CWD na pasta do exe para os caminhos relativos
(assets/, src/config.yaml, data/) funcionarem.
"""
import os
import sys

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

from dotenv import load_dotenv
load_dotenv()

import main  # noqa: E402  (importa o app; ordem ctranslate2->PyQt5 e interna)

app = main.WhisperEdgeApp()
app.run()

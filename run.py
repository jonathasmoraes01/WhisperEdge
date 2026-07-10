import os
import sys
import subprocess
from dotenv import load_dotenv

# Sob pythonw.exe (sem console) sys.stdout/stderr sao None e qualquer print() crasha.
# Redireciona para devnull para o app rodar oculto sem console.
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

print('Starting WiprFlow...')
load_dotenv()
subprocess.run([sys.executable, os.path.join('src', 'main.py')])

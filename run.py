import os
import sys
import runpy
from dotenv import load_dotenv

# Sob pythonw.exe (sem console) sys.stdout/stderr sao None e qualquer print() crasha.
# Redireciona para devnull para o app rodar oculto sem console.
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# Garante caminhos relativos corretos (assets/, src/config.yaml) de onde quer
# que o launcher tenha sido chamado.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('Starting WhisperEdge...')
load_dotenv()

# Executa o app NO MESMO processo (sem subprocess): um unico processo no
# Gerenciador de Tarefas e nenhuma chance de console extra piscar.
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
runpy.run_path(os.path.join('src', 'main.py'), run_name='__main__')

' Inicia o WhisperWriter com a janela de console ESCONDIDA (estilo 0 = oculto).
' Usa python.exe (que funciona certinho); a janela do console fica invisivel.
Dim sh, cmd
Set sh = CreateObject("WScript.Shell")
sh.CurrentDirectory = "C:\Users\Administrator\Tools\whisper-writer"
cmd = """C:\Users\Administrator\Tools\whisper-writer\.venv\Scripts\python.exe"" ""C:\Users\Administrator\Tools\whisper-writer\run.py"""
sh.Run cmd, 0, False

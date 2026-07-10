' Inicia o WhisperEdge sem NENHUMA janela (pythonw = subsistema GUI, sem console).
' Portavel: usa a propria pasta do script, entao funciona onde o repo estiver.
Dim sh, fso, here, cmd
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
here = fso.GetParentFolderName(WScript.ScriptFullName)
sh.CurrentDirectory = here
cmd = """" & here & "\.venv\Scripts\pythonw.exe"" """ & here & "\run.py"""
sh.Run cmd, 0, False

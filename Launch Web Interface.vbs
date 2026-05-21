Dim sh, dir
Set sh  = CreateObject("WScript.Shell")
dir     = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\") - 1)
sh.Run "cmd /c cd /d """ & dir & """ && streamlit run app_streamlit.py", 0, False

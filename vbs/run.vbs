'=======================================================

' ARG[0]: str  = Script To Run
' ARG[1]: bool = Show Terminal Window (Default=True)
' ARG[2]: bool = Verbose (Default=False)

' EX: wscript run.vbs Interval.Startup True False

'=======================================================

' Get Method Name from first arguement
CMD = "python.exe -m Scripts." & WScript.Arguments(0)

'=======================================================
' VISIBLE [POSITIONAL ARG]

if WScript.Arguments.Count = 2 then
    Visible = CBool(WScript.Arguments(1))
else
    Visible = True
end if

'=======================================================
' VERBOSE [POSITIONAL ARG]

If WScript.Arguments.Count > 2 Then
    For i = 2 To WScript.Arguments.Count - 1
        CMD = CMD & " " & Chr(34) & WScript.Arguments(i) & Chr(34)
    Next
end if

'=======================================================

' Create a new Shell Object
Set Shell = CreateObject("WScript.Shell")

Shell.CurrentDirectory = "C:\"

Shell.Run CMD, Visible, 0

'=======================================================
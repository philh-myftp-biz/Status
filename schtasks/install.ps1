
$Credential = Get-Credential `
    -UserName "$env:USERDOMAIN\$env:USERNAME" `
    -Message "Enter the Windows account credentials to run the Server tasks."

# Unpack the username and plain text password
[String] $Username = $Credential.UserName

[String] $Password = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($Credential.Password)
)

@("Startup", "Hour", "Week") | ForEach-Object {

    $Task = "\Server\$_"

    Write-Host "Registering task: $_"

    # Force delete existing task to prevent schema conflict errors
    schtasks.exe /delete /f /tn $Task 2>$null

    # Create the task using native schtasks.exe matching your batch arguments
    schtasks.exe /create `
        /xml "$PSScriptRoot\$_.xml" `
        /tn $Task `
        /ru $Username `
        /rp $Password `
        /it

}

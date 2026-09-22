
$profileData = @{
    profiles = @(
        [PSCustomObject]@{
            commandline       = "python -m Scripts.run.Console"
            elevate           = $false
            guid              = "{43e925b0-daa4-4138-ab4a-fc706c9b2a50}"
            hidden            = $false
            icon              = [char]0xE770 
            name              = "Phil's Console"
            startingDirectory = "C:\"
        }
    )
}

$fragDir = "$env:LOCALAPPDATA\Microsoft\Windows Terminal\Fragments\PhilsConsole"

New-Item $fragDir `
    -ItemType Directory `
    -ErrorAction SilentlyContinue

Write-Host "Compiling profile.json fragment..."
Set-Content `
    -Path "$fragDir\profile.json" `
    -Value ($profileData | ConvertTo-Json -Depth 10) `
    -Encoding UTF8

Write-Host "Refreshing Windows Terminal..." -ForegroundColor Gray
Add-Content `
    -Path "$env:LOCALAPPDATA\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json" `
    -Value " "

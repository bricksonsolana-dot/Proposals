## Creates a desktop shortcut for the Lead Finder

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$batPath = Join-Path $root "LeadFinder.bat"
$iconPath = Join-Path (Split-Path $root) "crm\static\logo.ico"

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Devox Lead Finder.lnk"

$wshell = New-Object -ComObject WScript.Shell
$shortcut = $wshell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $batPath
$shortcut.WorkingDirectory = $root
$shortcut.WindowStyle = 7
if (Test-Path $iconPath) { $shortcut.IconLocation = $iconPath }
$shortcut.Description = "Devox Lead Finder"
$shortcut.Save()

Write-Host "Shortcut created: $shortcutPath"
Write-Host "Double-click 'Devox Lead Finder' on your desktop to launch."

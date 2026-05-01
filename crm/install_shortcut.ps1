## Creates a desktop shortcut to launch the Devox Sales CRM
## Run with: powershell -ExecutionPolicy Bypass -File install_shortcut.ps1

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
# Prefer cloud client launcher if it exists, fall back to local launcher
$batPath = Join-Path $root "DevoxSalesClient.bat"
if (-not (Test-Path $batPath)) {
    $batPath = Join-Path $root "DevoxSales.bat"
}
$logoPath = Join-Path $root "static\logo.png"
$iconPath = Join-Path $root "static\logo.ico"

# Convert logo.png -> logo.ico if it doesn't exist yet (best-effort)
if (-not (Test-Path $iconPath) -and (Test-Path $logoPath)) {
    try {
        Add-Type -AssemblyName System.Drawing
        $bitmap = [System.Drawing.Bitmap]::FromFile($logoPath)
        $iconHandle = $bitmap.GetHicon()
        $icon = [System.Drawing.Icon]::FromHandle($iconHandle)
        $stream = [System.IO.File]::Create($iconPath)
        $icon.Save($stream)
        $stream.Close()
        $bitmap.Dispose()
        Write-Host "Created icon at $iconPath"
    } catch {
        Write-Host "Could not create .ico (not critical): $_"
    }
}

$desktop = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktop "Devox Sales.lnk"

$wshell = New-Object -ComObject WScript.Shell
$shortcut = $wshell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $batPath
$shortcut.WorkingDirectory = $root
$shortcut.WindowStyle = 7  # minimized
if (Test-Path $iconPath) { $shortcut.IconLocation = $iconPath }
$shortcut.Description = "Devox Sales CRM"
$shortcut.Save()

Write-Host "Shortcut created: $shortcutPath"
Write-Host "Double-click 'Devox Sales' on your desktop to launch."

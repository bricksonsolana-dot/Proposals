; Inno Setup script for Devox Sales
; Builds DevoxSales-Setup.exe — a one-click Windows installer
; that installs DevoxSales.exe + crm_url.txt to Program Files,
; creates Start Menu / Desktop shortcuts, and registers an uninstaller.

#define MyAppName "Devox Sales"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Devox"
#define MyAppExeName "DevoxSales.exe"
#define MyAppId "{{8E1B5F77-4C3D-4D6A-9F4B-DEA0AABBCC01}"

[Setup]
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL=https://devox.gr
AppSupportURL=https://devox.gr
AppUpdatesURL=https://devox.gr
DefaultDirName={autopf}\Devox Sales
DefaultGroupName=Devox Sales
DisableDirPage=yes
DisableProgramGroupPage=yes
ArchitecturesInstallIn64BitMode=x64compatible
ArchitecturesAllowed=x64compatible
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog commandline
OutputDir=..\dist
OutputBaseFilename=DevoxSales-Setup
SetupIconFile=..\static\logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
Compression=lzma2/ultra
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=auto
CloseApplications=yes
RestartApplications=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkedonce

[Files]
Source: "..\dist\DevoxSales.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\crm_url.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,Devox Sales}"; Flags: nowait postinstall skipifsilent

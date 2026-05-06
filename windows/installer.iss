[Setup]
AppName=Tacty
AppVersion=1.0
AppPublisher=TactileLibrary
DefaultDirName={autopf}\tacty
DefaultGroupName=tacty
OutputDir=..\Output
OutputBaseFilename=tacty-windows-installer
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=..\src\tacty\resources\icons\tl.ico

[Files]
Source: "..\dist\tacty.dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Tacty"; Filename: "{app}\Tacty.exe"
Name: "{autodesktop}\Tacty"; Filename: "{app}\Tacty.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"

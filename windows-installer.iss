#ifndef AppSource
 #define AppSource "app"
#endif
#ifndef PackageSource
 #define PackageSource "package"
#endif
#ifndef OutputRoot
 #define OutputRoot "dist"
#endif
[Setup]
AppId=OrcaSlicerAutoSlicePreview
AppName=OrcaSlicer AutoSlice
AppVersion=0.2.0
AppVerName=OrcaSlicer AutoSlice 0.2.0 preview
AppPublisher=OrcaSlicer AutoSlice community
AppPublisherURL=https://github.com/Moffy97/OrcaSlicer-AutoSlice
DefaultDirName={localappdata}\Programs\OrcaSlicer-AutoSlice
DefaultGroupName=OrcaSlicer AutoSlice
DisableProgramGroupPage=yes
DisableDirPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#OutputRoot}
OutputBaseFilename=OrcaSlicer-AutoSlice-0.2.0-preview-Setup-x64
Compression=lzma2/fast
SolidCompression=yes
LZMANumBlockThreads=2
WizardStyle=modern
SetupIconFile={#AppSource}\resources\images\OrcaSlicer.ico
UninstallDisplayIcon={app}\app\orca-slicer.exe
CloseApplications=no
RestartApplications=no
AllowNoIcons=yes
SetupLogging=yes
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
[Dirs]
Name: "{app}\dati"; Flags: uninsneveruninstall
[Files]
Source: "{#AppSource}\*"; DestDir: "{app}\app"; Excludes: "*.pdb,*.log,__pycache__\*,.git\*,logs\*"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#PackageSource}\*"; DestDir: "{app}\source"; Flags: ignoreversion recursesubdirs createallsubdirs
[Icons]
Name: "{group}\OrcaSlicer AutoSlice"; Filename: "{app}\app\orca-slicer.exe"; Parameters: "--datadir ""{app}\dati"""; WorkingDir: "{app}"
Name: "{group}\Uninstall OrcaSlicer AutoSlice"; Filename: "{uninstallexe}"
Name: "{autodesktop}\OrcaSlicer AutoSlice"; Filename: "{app}\app\orca-slicer.exe"; Parameters: "--datadir ""{app}\dati"""; WorkingDir: "{app}"; Tasks: desktopicon

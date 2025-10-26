; AI Corrector - Inno Setup Installer Script
; BLACK & WHITE MINIMAL THEME
; Build command: iscc.exe config\AICorrector_Installer.iss

#define MyAppName "AI Corrector"
#define MyAppVersion "2.3.0"
#define MyAppPublisher "Jampani Komal"
#define MyAppURL "https://github.com/JAMPANIKOMAL/AI_Corrector_Project"
#define MyAppExeName "AICorrector.exe"

[Setup]
AppId={{7A31F16B-71A1-44EB-BD16-94BCCED9F827}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright © 2024-2025 {#MyAppPublisher}

DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

OutputDir=..\dist
OutputBaseFilename=AICorrector-Setup-v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=4

WizardStyle=modern
SetupIconFile=..\assets\app_logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
DisableWelcomePage=no

PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright=Copyright © 2024-2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

AllowNoIcons=yes
ShowLanguageDialog=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\app_logo.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "..\assets\app_logo.png"; DestDir: "{app}\assets"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_logo.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{app}\assets\app_logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}\models"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure InitializeWizard();
begin
  WizardForm.WizardBitmapImage.Visible := False;
  WizardForm.WizardBitmapImage2.Visible := False;
  
  WizardForm.WelcomeLabel2.Caption := 
    'This wizard will guide you through the installation of AI Corrector.' + #13#10 + #13#10 +
    'AI Corrector is an intelligent text correction application that uses ' +
    'advanced T5 Transformer models to provide contextual grammar corrections.' + #13#10 + #13#10 +
    'Click Next to continue, or Cancel to exit Setup.';
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    CreateDir(ExpandConstant('{app}\models'));
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
end;

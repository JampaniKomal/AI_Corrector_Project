; AI Corrector - Inno Setup Installer Script with VCL Styles
; Modern black & white themed installer
; Build command: iscc.exe config\AICorrector_Installer.iss

#define MyAppName "AI Corrector"
#define MyAppVersion "2.3.0"
#define MyAppPublisher "Jampani Komal"
#define MyAppURL "https://github.com/JAMPANIKOMAL/AI_Corrector_Project"
#define MyAppExeName "AICorrector.exe"
#define VCLStyle "Carbon.vsf"

[Setup]
; App Information
AppId={{7A31F16B-71A1-44EB-BD16-94BCCED9F827}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright © 2024-2025 {#MyAppPublisher}

; Installation Directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output Configuration
OutputDir=..\dist
OutputBaseFilename=AICorrector-Setup-v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes
LZMANumBlockThreads=4

; Appearance
WizardStyle=modern
SetupIconFile=..\assets\app_logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

; Privileges & Architecture
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

; Version Info
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoDescription={#MyAppName} Installer
VersionInfoCopyright=Copyright © 2024-2025 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}

; Misc
AllowNoIcons=yes
ShowLanguageDialog=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main Application
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Assets
Source: "..\assets\app_logo.ico"; DestDir: "{app}\assets"; Flags: ignoreversion
Source: "..\assets\app_logo.png"; DestDir: "{app}\assets"; Flags: ignoreversion

; VCL Styles Plugin (will be added if available)
; Source: "VclStylesInno.dll"; DestDir: "{app}"; Flags: dontcopy
; Source: "styles\{#VCLStyle}"; DestDir: "{app}"; Flags: dontcopy

[Icons]
; Start Menu
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_logo.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; IconFilename: "{app}\assets\app_logo.ico"

; Desktop Icon (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\app_logo.ico"; Tasks: desktopicon

[Run]
; Option to launch app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up any user-created files (optional)
Type: filesandordirs; Name: "{app}\models"

[Code]
// VCL Styles functions (commented out for now - will be enabled if plugin is available)
(*
procedure LoadVCLStyle(VClStyleFile: String); external 'LoadVCLStyleW@files:VclStylesInno.dll stdcall';
procedure UnLoadVCLStyles; external 'UnLoadVCLStyles@files:VclStylesInno.dll stdcall';

function InitializeSetup(): Boolean;
begin
  ExtractTemporaryFile('{#VCLStyle}');
  LoadVCLStyle(ExpandConstant('{tmp}\{#VCLStyle}'));
  Result := True;
end;

procedure DeinitializeSetup();
begin
  UnLoadVCLStyles;
end;
*)

function InitializeSetup(): Boolean;
begin
  Result := True;
end;

// Custom messages and functions
procedure CurPageChanged(CurPageID: Integer);
begin
  if CurPageID = wpWelcome then
  begin
    WizardForm.WelcomeLabel2.Caption := 
      'This wizard will guide you through the installation of AI Corrector.' + #13#10 + #13#10 +
      'AI Corrector is an intelligent text correction application that uses ' +
      'advanced T5 Transformer models to provide contextual grammar corrections ' +
      'and spelling translations.' + #13#10 + #13#10 +
      'Click Next to continue, or Cancel to exit Setup.';
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create models directory for user downloads
    CreateDir(ExpandConstant('{app}\models'));
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  // Add any pre-installation checks here if needed
end;

; AI Corrector - NSIS Installer Script
; Modern UI installer for AI Corrector application
; CLI: makensis.exe config/installer.nsi

!include "MUI2.nsh"
!include "x64.nsh"

; ============================================================================
; Define Constants
; ============================================================================

!define APP_NAME "AI Corrector"
!define APP_VERSION "2.3.0"
!define APP_PUBLISHER "Jampani Komal"
!define APP_EXE "AICorrector.exe"
!define INSTALL_DIR "$PROGRAMFILES\AI Corrector"

; ============================================================================
; Installer Configuration
; ============================================================================

Name "${APP_NAME} ${APP_VERSION}"
OutFile "..\dist\AICorrector-Setup-v${APP_VERSION}.exe"
InstallDir "${INSTALL_DIR}"
InstallDirRegKey HKCU "Software\${APP_NAME}" "InstallDir"
ShowInstDetails show
ShowUninstDetails show

; Request admin privileges for Windows Vista+
RequestExecutionLevel admin

; ============================================================================
; MUI Settings - Black and White Theme
; ============================================================================

!define MUI_ICON "..\assets\app_logo.ico"
!define MUI_UNICON "..\assets\app_logo.ico"

; Color scheme - Black and White only
!define MUI_BGCOLOR FFFFFF
!define MUI_TEXTCOLOR 000000

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ============================================================================
; Installation Sections
; ============================================================================

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Copy application executable
  File "..\dist\${APP_EXE}"
  
  ; Copy assets
  SetOutPath "$INSTDIR\assets"
  File "..\assets\app_logo.ico"
  File "..\assets\app_logo.png"
  
  ; Create uninstaller (NSIS generates this automatically)
  SetOutPath "$INSTDIR"
  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
  WriteRegStr HKCU "Software\${APP_NAME}" "Version" "${APP_VERSION}"
  
  ; Create Start Menu shortcuts
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\assets\app_logo.ico"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\assets\app_logo.ico"
  
  ; Create Desktop shortcut
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\assets\app_logo.ico"
  
  ; Add to Add/Remove Programs
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME} ${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\assets\app_logo.ico"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
  
  DetailPrint "Installation complete!"
SectionEnd

; ============================================================================
; Uninstaller Section
; ============================================================================

Section "Uninstall"
  ; Remove application files
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\Uninstall.exe"
  Delete "$INSTDIR\assets\app_logo.ico"
  Delete "$INSTDIR\assets\app_logo.png"
  
  RMDir "$INSTDIR\assets"
  RMDir "$INSTDIR"
  
  ; Remove shortcuts
  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  
  Delete "$DESKTOP\${APP_NAME}.lnk"
  
  ; Remove registry entries
  DeleteRegKey HKCU "Software\${APP_NAME}"
  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
  
  DetailPrint "Uninstallation complete!"
SectionEnd

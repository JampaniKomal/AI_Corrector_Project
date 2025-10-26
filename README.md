# AI Corrector

![Version](https://img.shields.io/badge/version-2.3.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

A powerful AI-powered contextual grammar and spelling correction application built with T5 Transformer models and a modern GUI interface.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Building Executable](#building-executable)
- [Team](#team)

## About

AI Corrector is an intelligent text correction application developed as part of the **Artificial Intelligence (G5AD24ARI)** course at **Rashtriya Raksha University**. The application leverages pre-trained T5 Transformer models to provide contextual grammar corrections and spelling translations with high accuracy.

### Supported Languages

- **English (US/Global)** - Full grammar correction support
- **English (UK)** - Spelling translation from US to UK English
- **English (IN)** - Coming soon

## Features

- **AI-Powered Corrections** - Uses state-of-the-art T5 transformer models
- **Modern UI** - Built with CustomTkinter for a beautiful, responsive interface
- **Theme Support** - Dark mode, Light mode, and System-adaptive themes
- **Model Management** - Easy download and management of language models
- **Multi-Language** - Support for multiple English variants
- **Fast Processing** - Efficient model loading and inference
- **Local Processing** - All corrections run locally for privacy

## Project Structure

```
AI_Corrector_Project/
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── ui/                       # User interface modules
│   │   ├── __init__.py
│   │   └── main_window.py        # Main application window
│   └── utils/                    # Utility modules
│       ├── __init__.py
│       └── grammar_correction.py # Core correction logic
│
├── installer/                    # Custom installer & uninstaller
│   ├── installer_ui.py           # Professional themed installer
│   ├── uninstaller_ui.py         # Matching themed uninstaller
│   ├── requirements.txt          # Installer dependencies
│   └── GUIDE.md                  # Installation guide
│
├── scripts/                      # Utility scripts
│   ├── download_model.py         # Model download utility
│   └── setup.py                  # Build automation script
│
├── config/                       # Configuration files
│   ├── AICorrector.spec          # PyInstaller spec file
│   └── AICorrector_Installer.iss # Inno Setup script (alternative)
│
├── assets/                       # Application assets
│   ├── app_logo.ico              # Application icon
│   └── app_logo.png              # Application logo
│
├── models/                       # Downloaded AI models (gitignored)
├── dist/                         # Build output (gitignored)
│
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # Project license
└── .gitignore                   # Git ignore rules
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB+ RAM recommended for model inference

### Step 1: Clone the Repository

```bash
git clone https://github.com/JAMPANIKOMAL/AI_Corrector_Project.git
cd AI_Corrector_Project
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Download Language Models [Optional]

Run the application and navigate to **Settings** → **Language Models** to download your desired language model, or use the download script:

```bash
python scripts/download_model.py
```

## Usage

### Running the Application

```bash
python main.py
```

### Using the Corrector

1. **Select Language Model**: Go to Settings and select your preferred language model
2. **Download Model**: Click the download button if the model isn't already downloaded
3. **Correct Text**: 
   - Navigate to the Corrector page
   - Enter your text in the left text box
   - Click the ">>" button
   - View corrected text in the right text box

### Changing Themes

1. Go to **Settings** → **Appearance Mode**
2. Choose from:
   - Light Mode
   - Dark Mode
   - Adapt to Device (System)

## Building Executable & Installer

### Complete Build Process

**Step 1: Build the Main Application**

Build the executable using PyInstaller:

```powershell
pyinstaller config\AICorrector.spec
```

This creates `dist/AICorrector.exe` (~204 MB) - the standalone application.

---

### Step 2: Create Custom Installer (Recommended)

**Our custom installer perfectly matches the application's black/white minimalist theme.**

**Install installer dependencies:**
```powershell
cd installer
pip install -r requirements.txt
cd ..
```

**Run the installer (for testing):**
```powershell
python installer\installer_ui.py
```

**Build standalone installer executable:**
```powershell
cd installer
pyinstaller --onefile --windowed --name "AICorrector-Setup" --icon ..\assets\app_logo.ico installer_ui.py
cd ..
```

This creates `installer\dist\AICorrector-Setup.exe` - a professional themed installer.

**Custom Installer Features:**
- **Perfect Theme Match** - Identical black/white design as main app
- **Minimal Design** - No decorative symbols, clean typography
- **Smart Installation** - User-selectable location (default: AppData)
- **Progress Tracking** - Real-time installation progress
- **Shortcuts** - Desktop and Start Menu shortcuts with custom icon
- **Matching Uninstaller** - Same themed uninstaller included
- **Registry Integration** - Appears in Add/Remove Programs
- **Launch Option** - Launch app immediately after installation
- **No Admin Required** - Installs to user directory

**Window Specifications:**
- Size: 450x450 (compact 1:1 ratio)
- Theme: Black background, white text/buttons
- Font sizes: 18-22px titles, 12px body text
- Consistent with main application design

---

### Alternative: Inno Setup Installer

**For traditional Windows installer experience:**

1. Download Inno Setup from [jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
2. Build the installer:

```powershell
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" config\AICorrector_Installer.iss
```

Creates `dist\AICorrector-Setup-v2.3.0.exe` (~203 MB)

**Inno Setup Features:**
- Standard Windows wizard
- Minimal theme (limited customization)
- Professional appearance
- Built-in uninstaller

---

### Distribution

**Recommended Distribution Method:**

Distribute `AICorrector-Setup.exe` (the custom installer):
- Users get beautiful themed installation experience
- Matches application design perfectly
- Professional and user-friendly
- Single executable, no dependencies

**What the installer does:**
1. Welcome screen with app description
2. User selects installation location
3. User chooses shortcuts (desktop/start menu)
4. Installs application files
5. Creates shortcuts with custom icon
6. Registers in Add/Remove Programs
7. Option to launch app immediately

**What users get:**
- `C:\Users\[username]\AppData\Local\AI Corrector\` - Application files
- Desktop shortcut (optional)
- Start Menu folder with app and uninstaller shortcuts
- Add/Remove Programs entry for easy uninstallation

---

## Packaging for Distribution

### Create Final Release Package

**Step 1: Build all components**
```powershell
# Build main application
pyinstaller config\AICorrector.spec

# Build custom installer
cd installer
pip install -r requirements.txt
pyinstaller --onefile --windowed --name "AICorrector-Setup-v2.3.0" --icon ..\assets\app_logo.ico installer_ui.py
cd ..
```

**Step 2: Prepare distribution folder**
```powershell
# Create release folder
New-Item -ItemType Directory -Force -Path "release"

# Copy installer
Copy-Item "installer\dist\AICorrector-Setup-v2.3.0.exe" -Destination "release\"

# Optional: Copy README for context
Copy-Item "README.md" -Destination "release\README.txt"
```

**Step 3: Test the installer**
```powershell
# Run installer to verify it works
.\release\AICorrector-Setup-v2.3.0.exe
```

---

### Release Checklist

Before distributing:

- [ ] Main app executable built (`dist/AICorrector.exe`)
- [ ] Installer executable built (`installer/dist/AICorrector-Setup-v2.3.0.exe`)
- [ ] Test installer on clean machine
- [ ] Verify shortcuts work correctly
- [ ] Test uninstaller removes all files
- [ ] Check Add/Remove Programs entry
- [ ] Verify app launches after installation
- [ ] Test app functionality (grammar correction)
- [ ] Ensure all assets (icon, logo) display correctly

---

### Distribution Files

**For End Users:**
- `AICorrector-Setup-v2.3.0.exe` - Single file, ~5-10 MB
- User runs installer, gets complete themed installation experience
- No Python or dependencies required

**For Developers:**
- Full repository with source code
- Build instructions in README
- Custom installer source code in `installer/`

---

## Team

**Project Team:**
- **Jampani Komal** - Lead Developer

**Course:** Artificial Intelligence (G5AD24ARI)  
**University:** Rashtriya Raksha University  
**Academic Year:** 2024-2025

## Technologies Used

- **Python 3.8+**
- **Transformers** - Hugging Face Transformers library
- **PyTorch** - Deep learning framework
- **CustomTkinter** - Modern GUI framework (app & installers)
- **PySpellChecker** - Spell checking library
- **PyInstaller** - Executable builder

## Acknowledgments

- Hugging Face for providing pre-trained models
- The Transformers library team
- CustomTkinter developers
- Gemini

---

**Note:** This is an academic project developed for educational purposes.

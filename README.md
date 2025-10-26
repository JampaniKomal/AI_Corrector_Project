# AI Corrector

A powerful AI-powered contextual grammar and spelling correction application built with T5 Transformer models and a modern GUI interface.

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Building & Distribution](#building--distribution)
- [Team](#team)

## About

AI Corrector is an intelligent text correction application developed as part of the **Artificial Intelligence (G5AD24ARI)** course at **Rashtriya Raksha University**. The application leverages pre-trained T5 Transformer models to provide contextual grammar corrections and spelling translations with high accuracy.

### Supported Languages

- **English (US/Global)** - Full grammar correction support
- **English (UK)** - Spelling translation from US to UK English
- **English (IN)** - Coming soon

## Features

- AI-Powered Corrections - Uses state-of-the-art T5 transformer models
- Modern UI - Built with CustomTkinter for a beautiful, responsive interface
- Theme Support - Dark mode, Light mode, and System-adaptive themes
- Model Management - Easy download and management of language models
- Multi-Language - Support for multiple English variants
- Fast Processing - Efficient model loading and inference
- Local Processing - All corrections run locally for privacy

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
│   └── AICorrector_Complete_Setup.spec  # Complete installer build spec
│
├── scripts/                      # Utility scripts
│   └── download_model.py         # Model download utility
│
├── config/                       # Configuration files
│   └── AICorrector.spec          # PyInstaller spec file
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

### For End Users

Download and run `AICorrector-Setup-v2.3.0.exe` (240 MB)
- Self-contained installer with everything included
- No Python or dependencies required
- Themed black/white installer matching the app
- Creates desktop and start menu shortcuts

### For Developers

```powershell
git clone https://github.com/JAMPANIKOMAL/AI_Corrector_Project.git
cd AI_Corrector_Project
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Building & Distribution

### Build Complete Installer (One Command)

```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Step 1: Build main application
pyinstaller config\AICorrector.spec

# Step 2: Install installer dependencies
cd installer
pip install -r requirements.txt

# Step 3: Build complete self-contained installer
pyinstaller AICorrector_Complete_Setup.spec
cd ..
```

Output: `installer\dist\AICorrector-Setup-v2.3.0.exe` (240 MB)

This single executable contains:
- Themed installer UI (black/white design)
- Main application (204 MB)
- Themed uninstaller UI
- All assets and icons

### What Users Get

The installer provides:
- Installation location selection (default: AppData/Local/AI Corrector)
- Desktop shortcut (optional)
- Start Menu shortcuts
- Add/Remove Programs registry entry
- Themed uninstaller matching the app design
- Option to launch app after installation

No admin rights required. No Python needed.

---

## Team

Project Team: Jampani Komal - Lead Developer

Course: Artificial Intelligence (G5AD24ARI)
University: Rashtriya Raksha University
Academic Year: 2024-2025

## Technologies

- Python 3.8+
- Transformers - Hugging Face Transformers library
- PyTorch - Deep learning framework
- CustomTkinter - Modern GUI framework
- PyInstaller - Executable builder

## Acknowledgments

- Hugging Face for providing pre-trained models
- The Transformers library team
- CustomTkinter developers
- Gemini

This is an academic project developed for educational purposes.

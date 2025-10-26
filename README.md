# AI Corrector v2

A sophisticated, universal AI-powered grammar and spelling correction application. Unlike browser-limited extensions, this desktop application uses T5 Transformer models to provide contextual correction across any application on your machine, delivered through a modern, persistent GUI.

## Table of Contents

- [Project Evolution](#project-evolution-from-browser-goal-to-universal-corrector)
- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Building & Distribution](#building--distribution)
- [Team](#team)

## Project Evolution: From Browser Goal to Universal Corrector

Our primary objective was initially to create a real-time, AI-powered type corrector delivered via a Chrome/Browser Extension. This journey required us to explore various architectures, ultimately leading us to pivot toward a standalone desktop application that could achieve our correction goals across all applications on a user's machine.

### Phase 1: The Basic Extension (Invisible-Autocorrect-Extension)

Repository: https://github.com/JAMPANIKOMAL/invisible-autocorrect-extension

Architecture: Rule-based/Dictionary-based correction implemented as a minimalist Chrome Extension.

What it Lacked: This prototype successfully achieved the extension deployment but lacked the sophistication required for the project. It could only perform simple spelling lookups, falling short of the required AI functionality—specifically, contextual and grammatical correction provided by neural networks.

### Phase 2: The AI Integration Challenge (Ghost-Type-Corrector)

Repository: https://github.com/JAMPANIKOMAL/Ghost-Type-Corrector

Architecture: Attempted to integrate a heavy AI component (TensorFlow/Keras model) directly into the browser extension's sandbox environment.

What it Lacked: Integrating a full-scale AI model proved immensely complex and performance-intensive within the constraints of the browser's architecture. The technical complexity and performance degradation forced us to seek an alternative deployment method that could support our robust neural network.

### Phase 3: AI Model Validation (Type-Correcter-Ai)

Repository: https://github.com/JAMPANIKOMAL/Type-Correcter-Ai

Architecture: A pivot to a Flask Web Application to isolate and validate the performance of the core Sequence-to-Sequence Neural Network.

What it Lacked: While proving the AI model was effective, the web interface limited the solution to one tab/browser. It failed to address our expanded vision: universal correction in every selected app—not just Chrome.

### Final Solution: AI Corrector Project (The Universal Solution)

We settled on a standalone desktop application using Python and CustomTkinter. This architecture was the logical conclusion because it successfully addressed the limitations of all prototypes:

1. AI Power: It allows the robust, resource-intensive T5 Transformer model to run natively, unconstrained by a browser sandbox.
2. Universal Reach: By operating as a desktop application, it can process text input from any application (text editor, IDE, messaging app), fulfilling our ultimate goal of a truly universal AI corrector.
3. Meets Project Requirements: It provides a professional, dedicated Graphical User Interface (GUI) for control and demonstration with modern theming support.

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

Clone and run from source:

```powershell
git clone https://github.com/JAMPANIKOMAL/AI_Corrector_Project.git
cd AI_Corrector_Project
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Run the application:

```powershell
python main.py
```

First-time setup:
1. Navigate to Settings and select your preferred language model
2. Click download if the model is not already installed
3. Navigate to Corrector page and start correcting text

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

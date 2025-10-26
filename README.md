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
├── scripts/                      # Utility scripts
│   └── download_model.py         # Model download utility
│
├── config/                       # Configuration files
│   ├── app.spec                  # PyInstaller configuration
│   └── installer_script.iss      # Inno Setup installer script
│
├── docs/                         # Documentation
│
├── models/                       # Downloaded AI models (gitignored)
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

## Building Executable

### Using PyInstaller

```bash
pyinstaller -F --noconsole --name AICorrector --paths src --collect-all torch --collect-all transformers --collect-all customtkinter --collect-all spellchecker --add-data "..\\assets\\app_logo.ico;assets" --add-data "..\\assets\\app_logo.png;assets" --icon "..\\assets\\app_logo.ico" main.py --specpath config
```

The executable will be created in the `dist/` folder.

### Creating Windows Installer

1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Open `config/installer_script.iss` in Inno Setup
3. Click **Build** → **Compile**

The installer will be created in the project root directory.

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
- **CustomTkinter** - Modern GUI framework
- **PySpellChecker** - Spell checking library
- **PyInstaller** - Executable builder
- **Inno Setup** - Windows installer creator

## Acknowledgments

- Hugging Face for providing pre-trained models
- The Transformers library team
- CustomTkinter developers
- Gemini

---

**Note:** This is an academic project developed for educational purposes.

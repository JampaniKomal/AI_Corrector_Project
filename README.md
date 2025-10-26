# AI Corrector

A sophisticated, universal AI-powered grammar and spelling correction application. Unlike browser-limited extensions, this desktop application uses T5 Transformer models to provide contextual correction across any application on your machine, delivered through a modern, persistent GUI.

## Table of Contents

- [Project Evolution](#project-evolution-from-browser-goal-to-universal-corrector)
- [About](#about)
- [Features](#features)
- [AI Methodology](#ai-methodology-focus)
- [Visual Demonstration](#visual-demonstration)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Building & Distribution](#building--distribution)
- [Future Scope](#future-scope-and-enhancements)
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

Architecture: A pivot to a Flask Web Application to isolate and validate the performance of the core Sequence-to-Sequence (Seq2Seq) model.

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

## AI Methodology Focus

The core of the AI Corrector project is built upon the T5 (Text-to-Text Transfer Transformer) model, an advanced neural network architecture explicitly linked to the Neural Networks and NLP and Text Analytics units of our Artificial Intelligence syllabus (G5AD24ARI).

- Technique: We utilize a fine-tuned T5 model specifically trained for Grammatical Error Correction (GEC). The GEC task is treated as a sequence-to-sequence translation problem, where the input sequence (erroneous text) is directly translated into the output sequence (corrected text).
- Model Advantage: The T5 architecture's attention mechanisms allow it to understand the deep context of a sentence, enabling it to correct complex grammatical errors and syntactical mistakes that simple dictionary or rule-based methods (like those explored in Prototype 1) could not handle.
- Deployment: The integration of the large T5 model locally is what necessitated the pivot to a universal desktop application, providing sufficient resources for low-latency inference.

## Visual Demonstration

To showcase the application's modern UI and core functionality, screenshots of the CustomTkinter interface are included below. These visuals directly support the Implementation Details and Results & Discussion sections required for the Project Report and PowerPoint Presentation.

(Screenshots will be added here demonstrating the application interface, correction workflow, and settings management)

## Project Structure

This directory structure is organized to cleanly separate the application logic (the Source Code deliverable) from the deployment assets and configuration.

Key Deliverables Location:
- GUI Code: Located in src/ui/main_window.py (demonstrating CustomTkinter implementation)
- AI Logic: Core T5 model loading and inference is encapsulated in src/utils/grammar_correction.py (demonstrating the AI/search/logic techniques required by the syllabus)
- Deployment Assets: The installer/ directory contains all necessary files for the professional, end-user deployment package

```
AI_Corrector_Project/
│
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
│
├── src/                          # Core application code
│   ├── ui/
│   │   └── main_window.py        # GUI implementation (CustomTkinter)
│   └── utils/
│       └── grammar_correction.py # AI correction logic (T5 model)
│
├── assets/                       # Application resources
│   ├── app_logo.ico              # Application icon
│   └── app_logo.png              # Application logo
│
├── scripts/                      # Utility scripts
│   └── download_model.py         # T5 model download utility
│
├── config/                       # Build configuration
│   └── AICorrector.spec          # Main app build specification
│
├── installer/                    # Installer package
│   ├── installer_ui.py           # Themed installer interface
│   ├── uninstaller_ui.py         # Themed uninstaller interface
│   ├── requirements.txt          # Installer dependencies
│   └── AICorrector_Complete_Setup.spec  # Complete installer build spec
│
├── models/                       # T5 model weights (downloaded, gitignored)
└── dist/                         # Built executables (gitignored)
```

## Installation

### For End Users

Download and run [AICorrector-Setup-v2.3.0.exe](installer/dist/AICorrector-Setup-v2.3.0.exe) (240 MB)
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

# First-time setup: Download the required T5 model weights
python scripts\download_model.py

# Run the application
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

Output: `installer\dist\AICorrector-Setup.exe`

This single executable contains:
- Themed installer UI (black/white design)
- Main application
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

## Future Scope and Enhancements

This project serves as a robust proof-of-concept for universal, local, AI-powered correction. For future development, we plan the following enhancements:

- Custom Model Fine-Tuning: Currently relying on a pre-trained T5 model, future work will involve fine-tuning the model on a domain-specific dataset (e.g., technical or legal texts) to improve accuracy in specialized writing.
- Real-Time API Service: Develop a lightweight, local API endpoint for the correction model, allowing other local applications (like word processors or IDEs) to integrate correction functionality directly without relying on screen/keyboard hooks.
- Expanded Language Support: Implement and manage T5 models for other regional English variants (e.g., IN) and completely new languages, managed easily through the current GUI's Model Management feature.
- Hardware Acceleration: Integrate explicit support for different hardware backends (e.g., CUDA for NVIDIA GPUs) within the Python environment to further reduce inference latency, which is critical for real-time universal correction.

---

## Team

This project was developed for the Artificial Intelligence (G5AD24ARI) course at Rashtriya Raksha University.

Primary Developer: Jampani Komal

Project Team Structure (For Academic Submission):

The following roles cover the required project scope and deliverables, demonstrating understanding of necessary division of labor:

- AI/Model Specialist: Led the research on Transformer models (T5), managed the model training pipeline, and implemented the core correction logic in grammar_correction.py.
- Application & Integration Engineer: Designed the CustomTkinter GUI (main_window.py), developed the universal background service architecture, and handled the PyInstaller packaging and installer scripts.
- Documentation & Testing Lead: Authored the Project Report and Presentation, created the Demo Video, and ensured the project adhered to all formatting and documentation guidelines (e.g., the README, code comments).

Academic Year: 2024-2025

## Technologies

- Python
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

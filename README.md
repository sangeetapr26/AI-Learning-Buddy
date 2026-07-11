# AI Learning Buddy

An AI-powered educational web application that transforms lecture audio into complete, structured, and downloadable study materials.

The application helps students save time by automatically converting lecture recordings into transcripts, summaries, organized notes, keywords, quizzes, and flashcards.

---

## Features

The application automatically generates:

- **Complete Transcript** — Converts lecture audio into readable text
- **Concise Summary** — Summarizes the main ideas of the lecture
- **Organized Study Notes** — Creates structured notes for revision
- **Important Keywords** — Extracts important terms and concepts
- **Practice Quiz** — Generates multiple-choice questions with answers and explanations
- **Revision Flashcards** — Creates question-and-answer flashcards
- **PDF Export** — Download complete study material as a PDF
- **DOCX Export** — Download editable Microsoft Word notes
- **TXT Export** — Download complete study material as a text file

---

## Project Objective

Students often miss important concepts while trying to listen to lectures and write notes at the same time.

The **AI Learning Buddy** solves this problem by automatically processing lecture audio and generating structured learning materials.

The main objective of the project is to improve learning efficiency by allowing students to focus on understanding the lecture instead of manually writing every point.

---

## Target Users

This application is designed for:

- Students
- Teachers
- Online learners
- Competitive exam aspirants
- Self-learners

---

## Technologies Used

- **Python** — Core programming language
- **Streamlit** — Interactive web application interface
- **Groq API** — AI inference platform
- **Whisper Large V3 Turbo** — Speech-to-text transcription
- **Llama 3.3 70B Versatile** — AI-powered study material generation
- **ReportLab** — PDF document generation
- **python-docx** — Microsoft Word document generation
- **python-dotenv** — Secure local environment variable management

---

## AI Models Used

### Speech-to-Text

```text
whisper-large-v3-turbo
```

Used to convert uploaded lecture audio into a complete transcript.

### Text Generation

```text
llama-3.3-70b-versatile
```

Used to generate:

- Summary
- Study Notes
- Important Keywords
- Quiz Questions
- Flashcards

---

## Project Workflow

```text
 Lecture Audio
        │
        ▼
 Upload Audio File
        │
        ▼
 Groq Whisper Speech-to-Text
        │
        ▼
 Complete Transcript
        │
        ▼
 Groq Llama AI
        │
        ├────────► Concise Summary
        │
        ├────────► Organized Study Notes
        │
        ├────────► Important Keywords
        │
        ├────────► Practice Quiz
        │
        └────────► Revision Flashcards
        │
        ▼
Document Generation
        │
        ├────────► TXT
        ├────────► PDF
        └────────► DOCX
```

---

## Supported Audio Formats

The application supports:

- MP3
- WAV
- M4A
- AAC
- FLAC
- OGG

---

## Project Structure

```text
AI Learning Buddy/
│
├── app.py
├── test.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── assets/
│   └── style.css
│
├── uploads/
│   └── .gitkeep
│
├── outputs/
│   └── .gitkeep
│
└── utils/
    ├── __init__.py
    ├── prompts.py
    ├── pdf_generator.py
    ├── docx_generator.py
    └── helpers.py
```

## File and Folder Description

### `app.py`

The main Streamlit application.

It handles:

- Audio file upload
- Audio playback
- Speech-to-text transcription
- AI-generated summaries
- Study note generation
- Keyword extraction
- Quiz generation
- Flashcard generation
- Result display
- PDF, DOCX, and TXT downloads

---

### `test.py`

A simple testing file used during development to verify that the Groq API connection is working correctly.

This file is not required for normal application usage.

---

### `.env`

Stores the Groq API key securely for local development.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

### `.gitignore`

Prevents sensitive and unnecessary files from being uploaded to GitHub.

Examples include:

```text
.env
.venv/
__pycache__/
uploads/*
outputs/*
```

---

### `requirements.txt`

Contains all Python dependencies required to run the project.

```text
streamlit
groq
python-dotenv
python-docx
reportlab
```

---

### `assets/`

Contains the visual resources used by the application.

```text
assets/
└── style.css
```

- `style.css` — Custom styling for the Streamlit user interface

---

### `uploads/`

Temporarily stores lecture audio files uploaded by users.

Example:

```text
uploads/
├── lecture1.mp3
└── lecture2.m4a
```

---

### `outputs/`

Stores generated study materials and downloadable documents.

Example:

```text
outputs/
├── transcript.txt
├── summary.txt
├── notes.txt
├── keywords.txt
├── quiz.txt
├── flashcards.txt
├── complete_lecture_notes.txt
├── lecture_notes.pdf
└── lecture_notes.docx
```

---

### `utils/`

Contains reusable helper modules used by the main application.

```text
utils/
├── __init__.py
├── prompts.py
├── pdf_generator.py
├── docx_generator.py
└── helpers.py
```

#### `prompts.py`

Stores reusable AI prompt templates for:

- Summary generation
- Study note generation
- Keyword extraction
- Quiz generation
- Flashcard generation

#### `pdf_generator.py`

Generates the complete study material as a PDF document.

#### `docx_generator.py`

Generates the complete study material as an editable DOCX document.

#### `helpers.py`

Contains common utility functions for:

- Creating project folders
- Sanitizing filenames
- Saving uploaded audio files
- Saving generated text files
- Combining generated study materials

---

## Installation and Setup

## 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd AI Learning Buddy
```

---

## 2. Create a Virtual Environment

```bash
python -m venv .venv
```

---

## 3. Activate the Virtual Environment

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

---

## 4. Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## 5. Create a `.env` File

Create a file named:

```text
.env
```

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 6. Run the Application

```bash
python -m streamlit run app.py
```

The application will open in your browser.

---

## Security

The application follows basic API-key security practices:

- API keys are stored in environment variables.
- The `.env` file is excluded from GitHub using `.gitignore`.
- API keys are never hardcoded into the application.
- Deployment secrets should be stored using the hosting platform's secret-management system.

---

## Limitations

- Transcription quality depends on audio clarity and background noise.
- AI-generated content may occasionally contain inaccuracies.
- Very large audio files may take longer to process or exceed API limits.
- API usage is subject to the limits of the selected service and account.
- Generated study materials should be reviewed by the learner for accuracy.
- Temporary uploaded and generated files may not persist permanently on cloud deployment platforms.

---

## Future Improvements

Future versions of the project may include:

- Multi-language lecture support
- Speaker identification
- Timestamped transcripts
- Interactive quizzes
- Interactive flashcard mode
- User editing of generated notes
- Search within lecture transcripts
- Cloud storage integration
- User authentication
- Lecture history and dashboard
- Multiple AI model options

---

## Use Cases

The application can be used for:

- College lectures
- Online classes
- Educational podcasts
- Recorded seminars
- Workshops
- Self-learning sessions

---

## Author

### Sangeeta Prasad

B.Tech Computer Science and Engineering Student
Chaibasa Engineering College

---

## Disclaimer

This application uses artificial intelligence to generate educational content. AI-generated transcripts, summaries, notes, quizzes, and flashcards may occasionally contain errors or incomplete information.

Users should verify important academic information from reliable sources.

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

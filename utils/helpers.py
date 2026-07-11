import os
import re
from pathlib import Path


UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"


def create_project_folders():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def safe_filename(filename):
    filename = Path(filename).name
    return re.sub(
        r"[^A-Za-z0-9._-]",
        "_",
        filename
    )


def save_uploaded_file(uploaded_file):
    create_project_folders()

    filename = safe_filename(uploaded_file.name)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


def save_text(filename, content):
    create_project_folders()

    file_path = os.path.join(
        OUTPUT_FOLDER,
        filename
    )

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(content)

    return file_path


def create_complete_text(
    transcript,
    summary,
    notes,
    keywords,
    quiz,
    flashcards
):
    return f"""
LECTURE VOICE-TO-NOTES GENERATOR
================================

1. COMPLETE TRANSCRIPT
----------------------
{transcript}


2. CONCISE SUMMARY
------------------
{summary}


3. ORGANIZED STUDY NOTES
------------------------
{notes}


4. IMPORTANT KEYWORDS
---------------------
{keywords}


5. QUIZ
-------
{quiz}


6. FLASHCARDS
-------------
{flashcards}
""".strip()
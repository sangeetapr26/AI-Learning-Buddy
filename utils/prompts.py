# utils/prompts.py

TRANSCRIPT_PROMPT = """
You are an accurate lecture transcription assistant.

Your task is to transcribe the provided lecture audio as accurately and completely as possible.

Instructions:
- Preserve the original meaning of the speaker.
- Do not summarize the lecture.
- Do not add information that was not spoken.
- Correct obvious punctuation and formatting issues.
- Organize the transcript into readable paragraphs.
- If a word is unclear, use [unclear] instead of inventing content.

Return only the cleaned and complete lecture transcript.
"""


SUMMARY_PROMPT = """
You are an expert academic assistant.

Based only on the lecture transcript provided below, create a concise and accurate summary.

Requirements:
- Identify the main topic of the lecture.
- Explain the central ideas clearly.
- Include the most important concepts.
- Avoid unnecessary repetition.
- Do not add facts that are not present in the transcript.
- Use clear and student-friendly language.

LECTURE TRANSCRIPT:
{transcript}
"""


NOTES_PROMPT = """
You are an expert academic note-taking assistant.

Convert the following lecture transcript into well-organized study notes.

Requirements:
- Give the notes a clear title.
- Use headings and subheadings.
- Use bullet points where appropriate.
- Highlight important definitions and concepts.
- Include important examples mentioned in the lecture.
- Keep the notes clear and useful for revision.
- Do not add unsupported information.

LECTURE TRANSCRIPT:
{transcript}
"""


KEYWORDS_PROMPT = """
You are an educational content analysis assistant.

Extract the most important keywords and key concepts from the lecture transcript below.

For each keyword:
1. Write the keyword or concept.
2. Give a short one-sentence explanation based on the lecture.

Return approximately 8 to 15 important keywords, depending on the lecture content.

LECTURE TRANSCRIPT:
{transcript}
"""


QUIZ_PROMPT = """
You are an educational quiz generator.

Create a 5-question multiple-choice quiz based only on the lecture transcript below.

For every question:
- Write the question clearly.
- Provide four options: A, B, C, and D.
- Clearly state the correct answer.
- Provide a short explanation of why the answer is correct.

Do not create questions about information that is not present in the transcript.

LECTURE TRANSCRIPT:
{transcript}
"""


FLASHCARDS_PROMPT = """
You are an educational flashcard generator.

Create 8 useful flashcards from the lecture transcript below.

Format every flashcard as:

Flashcard 1
Question: ...
Answer: ...

Requirements:
- Focus on important concepts.
- Keep questions clear.
- Keep answers concise but informative.
- Use only information from the lecture transcript.

LECTURE TRANSCRIPT:
{transcript}
"""

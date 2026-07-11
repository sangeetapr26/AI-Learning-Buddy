import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

from utils.prompts import (
    TRANSCRIPT_PROMPT,
    SUMMARY_PROMPT,
    NOTES_PROMPT,
    KEYWORDS_PROMPT,
    QUIZ_PROMPT,
    FLASHCARDS_PROMPT,
)

from utils.helpers import (
    create_project_folders,
    save_uploaded_file,
    save_text,
    create_complete_text,
)

from utils.pdf_generator import generate_pdf
from utils.docx_generator import generate_docx


# 1. PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Learning Buddy",
    page_icon="🎙️",
    layout="wide",
)


# 2. LOAD CUSTOM CSS

css_path = os.path.join(
    "assets",
    "style.css"
)

if os.path.exists(css_path):

    with open(
        css_path,
        "r",
        encoding="utf-8"
    ) as css_file:

        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


# 3. CREATE REQUIRED FOLDERS

create_project_folders()


# 4. LOAD GROQ API KEY

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:

    st.error(
        "GROQ_API_KEY was not found in the .env file."
    )

    st.info(
        "Add your Groq API key to the .env file and restart the app."
    )

    st.stop()


# 5. INITIALIZE GROQ CLIENT

client = Groq(
    api_key=api_key
)


# Text generation model
TEXT_MODEL = "llama-3.3-70b-versatile"


# Speech-to-text model
TRANSCRIPTION_MODEL = "whisper-large-v3-turbo"


# 6. SESSION STATE

state_defaults = {

    "transcript": "",
    "summary": "",
    "notes": "",
    "keywords": "",
    "quiz": "",
    "flashcards": "",

    "txt_path": "",
    "pdf_path": "",
    "docx_path": ""
}


for key, default_value in state_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = default_value


# 7. GROQ TEXT GENERATION FUNCTION

def generate_text(prompt):
    """
    Generate text using the Groq LLM.
    """

    response = client.chat.completions.create(

        model=TEXT_MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert academic learning assistant. "
                    "Follow the user's instructions carefully. "
                    "Use only the information provided in the lecture "
                    "transcript and do not invent unsupported facts."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )


    content = response.choices[0].message.content


    if not content:

        raise ValueError(
            "Groq returned an empty response."
        )


    return content.strip()


# 8. GROQ AUDIO TRANSCRIPTION FUNCTION

def transcribe_audio(audio_path):
    """
    Convert lecture audio into text using
    Groq Whisper speech-to-text.
    """

    with open(
        audio_path,
        "rb"
    ) as audio_file:

        transcription = (
            client.audio.transcriptions.create(

                file=audio_file,

                model=TRANSCRIPTION_MODEL,

                prompt=(
                    "Transcribe this lecture accurately and completely. "
                    "Preserve the original meaning. "
                    "Do not summarize the lecture. "
                    "Add appropriate punctuation for readability."
                ),

                response_format="text",

                temperature=0.0
            )
        )


    if not transcription:

        raise ValueError(
            "Groq did not generate a transcript."
        )


    # Groq may return plain text
    if isinstance(
        transcription,
        str
    ):

        return transcription.strip()


    # Handle response object if returned
    if hasattr(
        transcription,
        "text"
    ):

        return transcription.text.strip()


    return str(
        transcription
    ).strip()


# 9. HEADER

st.title(
    "Lecture Voice-to-Notes Generator"
)


st.markdown(
    """
    <p class="app-subtitle">
        Transform lecture recordings into complete transcripts,
        concise summaries, organized study notes, important keywords,
        quizzes and flashcards.
    </p>
    """,
    unsafe_allow_html=True
)


# 10. FEATURE CARDS

feature1, feature2, feature3 = st.columns(3)


with feature1:

    st.markdown(
        """
        <div class="feature-card">
            <h3>Transcript</h3>
            <p>
                Convert lecture audio into accurate
                and readable text.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature2:

    st.markdown(
        """
        <div class="feature-card">
            <h3>Smart Notes</h3>
            <p>
                Generate summaries, organized notes
                and important keywords.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


with feature3:

    st.markdown(
        """
        <div class="feature-card">
            <h3>Revision</h3>
            <p>
                Create quizzes and flashcards
                for effective revision.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# 11. AUDIO UPLOAD

st.header(
    "Upload Lecture Audio"
)


audio_file = st.file_uploader(

    "Choose an audio file",

    type=[
        "mp3",
        "wav",
        "m4a",
        "aac",
        "flac",
        "ogg"
    ],

    help=(
        "Supported formats: "
        "MP3, WAV, M4A, AAC, FLAC and OGG"
    )
)


# 12. PROCESS UPLOADED AUDIO

if audio_file is not None:

    # Upload confirmation

    st.success(
        f"{audio_file.name} uploaded successfully!"
    )


    # Audio player

    st.audio(
        audio_file
    )


    # File information

    file_size_mb = (
        audio_file.size
        / (1024 * 1024)
    )


    info1, info2 = st.columns(2)


    with info1:

        st.info(
            f"File: {audio_file.name}"
        )


    with info2:

        st.info(
            f"Size: {file_size_mb:.2f} MB"
        )


    # Generate button

    if st.button(
        "Generate Complete Study Material",
        type="primary",
        use_container_width=True
    ):

        try:

            progress = st.progress(0)

            status = st.empty()


            # =================================================
            # STEP 1: SAVE AUDIO
            # =================================================

            status.info(
                "Saving uploaded audio..."
            )


            audio_path = save_uploaded_file(
                audio_file
            )


            progress.progress(10)


            # =================================================
            # STEP 2: GENERATE TRANSCRIPT
            # =================================================

            status.info(
                "🎧 Generating complete transcript..."
            )


            transcript = transcribe_audio(
                audio_path
            )


            st.session_state.transcript = (
                transcript
            )


            save_text(
                "transcript.txt",
                transcript
            )


            progress.progress(35)


            # =================================================
            # STEP 3: GENERATE SUMMARY
            # =================================================

            status.info(
                "Generating concise summary..."
            )


            summary = generate_text(

                SUMMARY_PROMPT.format(
                    transcript=transcript
                )
            )


            st.session_state.summary = (
                summary
            )


            save_text(
                "summary.txt",
                summary
            )


            progress.progress(50)


            # =================================================
            # STEP 4: GENERATE STUDY NOTES
            # =================================================

            status.info(
                "Creating organized study notes..."
            )


            notes = generate_text(

                NOTES_PROMPT.format(
                    transcript=transcript
                )
            )


            st.session_state.notes = (
                notes
            )


            save_text(
                "notes.txt",
                notes
            )


            progress.progress(65)


            # =================================================
            # STEP 5: GENERATE KEYWORDS
            # =================================================

            status.info(
                "Extracting important keywords..."
            )


            keywords = generate_text(

                KEYWORDS_PROMPT.format(
                    transcript=transcript
                )
            )


            st.session_state.keywords = (
                keywords
            )


            save_text(
                "keywords.txt",
                keywords
            )


            progress.progress(75)


            # =================================================
            # STEP 6: GENERATE QUIZ
            # =================================================

            status.info(
                "Generating practice quiz..."
            )


            quiz = generate_text(

                QUIZ_PROMPT.format(
                    transcript=transcript
                )
            )


            st.session_state.quiz = (
                quiz
            )


            save_text(
                "quiz.txt",
                quiz
            )


            progress.progress(85)


            # =================================================
            # STEP 7: GENERATE FLASHCARDS
            # =================================================

            status.info(
                "Generating revision flashcards..."
            )


            flashcards = generate_text(

                FLASHCARDS_PROMPT.format(
                    transcript=transcript
                )
            )


            st.session_state.flashcards = (
                flashcards
            )


            save_text(
                "flashcards.txt",
                flashcards
            )


            progress.progress(92)


            # =================================================
            # STEP 8: CREATE COMPLETE TXT
            # =================================================

            status.info(
                "Creating downloadable documents..."
            )


            complete_text = create_complete_text(

                transcript,
                summary,
                notes,
                keywords,
                quiz,
                flashcards
            )


            txt_path = save_text(

                "complete_lecture_notes.txt",

                complete_text
            )


            # =================================================
            # STEP 9: CREATE PDF
            # =================================================

            pdf_path = generate_pdf(

                transcript,
                summary,
                notes,
                keywords,
                quiz,
                flashcards
            )


            # =================================================
            # STEP 10: CREATE DOCX
            # =================================================

            docx_path = generate_docx(

                transcript,
                summary,
                notes,
                keywords,
                quiz,
                flashcards
            )


            # =================================================
            # SAVE DOWNLOAD PATHS
            # =================================================

            st.session_state.txt_path = (
                txt_path
            )

            st.session_state.pdf_path = (
                pdf_path
            )

            st.session_state.docx_path = (
                docx_path
            )


            # =================================================
            # COMPLETE
            # =================================================

            progress.progress(100)


            status.success(
                "All study materials generated successfully!"
            )


            st.balloons()


        # =====================================================
        # ERROR HANDLING
        # =====================================================

        except Exception as error:

            error_message = str(
                error
            )


            # Rate limit error
            if (
                "429" in error_message
                or "rate_limit" in error_message.lower()
                or "rate limit" in error_message.lower()
            ):

                st.error(
                    """
                    Groq API rate limit reached.

                    Please wait for a short time
                    and try again.
                    """
                )


            # Authentication error
            elif (
                "401" in error_message
                or "invalid api key" in error_message.lower()
                or "authentication" in error_message.lower()
            ):

                st.error(
                    """
                    Groq API authentication failed.

                    Please check your GROQ_API_KEY
                    in the .env file.
                    """
                )


            # File size error
            elif (
                "file size" in error_message.lower()
                or "too large" in error_message.lower()
            ):

                st.error(
                    """
                    The audio file is too large.

                    Please try a shorter or smaller
                    lecture recording.
                    """
                )


            # Other errors
            else:

                st.error(
                    "Processing failed."
                )

                st.error(
                    error_message
                )


# 13. DISPLAY GENERATED RESULTS

if st.session_state.transcript:

    st.divider()


    st.header(
        "Generated Study Material"
    )


    tabs = st.tabs(
        [
            "Transcript",
            "Summary",
            "Notes",
            "Keywords",
            "Quiz",
            "Flashcards",
            "Downloads"
        ]
    )


    # TRANSCRIPT TAB

    with tabs[0]:

        st.subheader(
            "Complete Transcript"
        )


        st.write(
            st.session_state.transcript
        )


    # SUMMARY TAB

    with tabs[1]:

        st.subheader(
            "Concise Summary"
        )


        if st.session_state.summary:

            st.markdown(
                st.session_state.summary
            )

        else:

            st.info(
                "Summary has not been generated yet."
            )


    # NOTES TAB

    with tabs[2]:

        st.subheader(
            "Organized Study Notes"
        )


        if st.session_state.notes:

            st.markdown(
                st.session_state.notes
            )

        else:

            st.info(
                "Study notes have not been generated yet."
            )


    # KEYWORDS TAB

    with tabs[3]:

        st.subheader(
            "Important Keywords"
        )


        if st.session_state.keywords:

            st.markdown(
                st.session_state.keywords
            )

        else:

            st.info(
                "Keywords have not been generated yet."
            )


    # QUIZ TAB

    with tabs[4]:

        st.subheader(
            "Practice Quiz"
        )


        if st.session_state.quiz:

            st.markdown(
                st.session_state.quiz
            )

        else:

            st.info(
                "Quiz has not been generated yet."
            )


    # FLASHCARDS TAB

    with tabs[5]:

        st.subheader(
            "Revision Flashcards"
        )


        if st.session_state.flashcards:

            st.markdown(
                st.session_state.flashcards
            )

        else:

            st.info(
                "Flashcards have not been generated yet."
            )


    # DOWNLOADS TAB

    with tabs[6]:

        st.subheader(
            "Download Study Material"
        )


        st.write(
            """
            Download the complete generated study material
            for offline learning and revision.
            """
        )


        download1, download2, download3 = (
            st.columns(3)
        )


        # ====================================================
        # TXT DOWNLOAD
        # ====================================================

        with download1:

            if (
                st.session_state.txt_path
                and
                os.path.exists(
                    st.session_state.txt_path
                )
            ):

                with open(
                    st.session_state.txt_path,
                    "rb"
                ) as file:

                    txt_data = file.read()


                st.download_button(

                    label="Download TXT",

                    data=txt_data,

                    file_name=(
                        "complete_lecture_notes.txt"
                    ),

                    mime="text/plain",

                    use_container_width=True
                )


        # ====================================================
        # PDF DOWNLOAD
        # ====================================================

        with download2:

            if (
                st.session_state.pdf_path
                and
                os.path.exists(
                    st.session_state.pdf_path
                )
            ):

                with open(
                    st.session_state.pdf_path,
                    "rb"
                ) as file:

                    pdf_data = file.read()


                st.download_button(

                    label="Download PDF",

                    data=pdf_data,

                    file_name=(
                        "lecture_notes.pdf"
                    ),

                    mime="application/pdf",

                    use_container_width=True
                )


        # ====================================================
        # DOCX DOWNLOAD
        # ====================================================

        with download3:

            if (
                st.session_state.docx_path
                and
                os.path.exists(
                    st.session_state.docx_path
                )
            ):

                with open(
                    st.session_state.docx_path,
                    "rb"
                ) as file:

                    docx_data = file.read()


                st.download_button(

                    label="Download DOCX",

                    data=docx_data,

                    file_name=(
                        "lecture_notes.docx"
                    ),

                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),

                    use_container_width=True
                )


# 14. FOOTER

st.divider()


st.caption(
    "Lecture Voice-to-Notes Generator • "
    "Built with Streamlit, Groq AI and Whisper • "
    "With ❤️ by Sangeeta"
)
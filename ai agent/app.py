import streamlit as st
import ollama
import json
import os
import pyttsx3

# Web search
try:
    from ddgs import DDGS
except:
    DDGS = None

# PDF
try:
    from pypdf import PdfReader
except:
    PdfReader = None

# Voice input
try:
    from streamlit_mic_recorder import speech_to_text
except:
    speech_to_text = None


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="My Personal AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# FILES
# =========================================================

MEMORY_FILE = "memory.json"
CHAT_FILE = "chat_history.json"
NOTES_FILE = "notes.txt"


# =========================================================
# MEMORY FUNCTIONS
# =========================================================

def load_memory():

    if os.path.exists(MEMORY_FILE):

        try:

            with open(MEMORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except:
            return []

    return []


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# CHAT HISTORY FUNCTIONS
# =========================================================

def load_chat():

    if os.path.exists(CHAT_FILE):

        try:

            with open(CHAT_FILE, "r", encoding="utf-8") as file:
                return json.load(file)

        except:
            return []

    return []


def save_chat(messages):

    with open(CHAT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            messages,
            file,
            indent=4,
            ensure_ascii=False
        )


# =========================================================
# NOTES
# =========================================================

def save_note(note):

    with open(
        NOTES_FILE,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(note + "\n")


# =========================================================
# LOAD DATA
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = load_chat()


if "memory" not in st.session_state:

    st.session_state.memory = load_memory()


if "pdf_text" not in st.session_state:

    st.session_state.pdf_text = ""


if "pdf_name" not in st.session_state:

    st.session_state.pdf_name = ""


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
"""
<style>

.stApp {
    background: #0f1117;
}

section[data-testid="stSidebar"] {

    background: #151821;

    border-right:
    1px solid #292d38;
}

.main-title {

    text-align: center;

    font-size: 44px;

    font-weight: 700;

    color: white;

    margin-top: 20px;

    margin-bottom: 5px;
}

.subtitle {

    text-align: center;

    color: #9ca3af;

    font-size: 16px;

    margin-bottom: 30px;
}

.welcome-card {

    background:
    linear-gradient(
        135deg,
        #1d2330,
        #171b25
    );

    border:
    1px solid #303644;

    border-radius: 20px;

    padding: 35px;

    text-align: center;

    margin: 20px auto 35px auto;

    max-width: 850px;

    box-shadow:
    0 10px 35px
    rgba(0,0,0,0.25);
}

.robot {

    font-size: 65px;

    margin-bottom: 10px;
}

.welcome-title {

    font-size: 28px;

    font-weight: 600;

    color: white;

    margin-bottom: 10px;
}

.welcome-text {

    color: #a7afbd;

    font-size: 16px;
}

.feature-card {

    background: #171b25;

    border:
    1px solid #292e3a;

    border-radius: 15px;

    padding: 18px;

    margin-bottom: 10px;
}

.footer {

    text-align: center;

    color: #626a78;

    font-size: 12px;

    margin-top: 30px;
}

</style>
""",
unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        "## 🤖 My Personal AI"
    )

    st.caption(
        "Your private AI assistant"
    )

    st.divider()


    # =====================================================
    # NEW CHAT
    # =====================================================

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        save_chat([])

        st.rerun()


    # =====================================================
    # CLEAR CHAT
    # =====================================================

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        save_chat([])

        st.rerun()


    st.divider()


    # =====================================================
    # SETTINGS
    # =====================================================

    st.markdown("### ⚙️ Settings")


    web_search = st.toggle(
        "🌐 Web Search",
        value=False
    )


    voice_output = st.toggle(
        "🔊 Voice Output",
        value=False
    )


    st.divider()


    # =====================================================
    # MEMORY
    # =====================================================

    st.markdown("### 🧠 My Memory")

    memory_text = st.text_input(
        "Tell AI something to remember",
        placeholder="Example: I love fashion"
    )


    if st.button(
        "💾 Save Memory",
        use_container_width=True
    ):

        if memory_text.strip():

            st.session_state.memory.append(
                memory_text.strip()
            )

            save_memory(
                st.session_state.memory
            )

            st.success(
                "Memory saved!"
            )


    if st.session_state.memory:

        st.caption("Saved memories:")

        for item in st.session_state.memory:

            st.write(
                "• " + item
            )


    st.divider()


    # =====================================================
    # PDF UPLOAD
    # =====================================================

    st.markdown("### 📄 PDF Reader")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"]
    )


    if uploaded_pdf is not None:

        if PdfReader is not None:

            try:

                reader = PdfReader(
                    uploaded_pdf
                )

                text = ""

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:

                        text += page_text + "\n"


                st.session_state.pdf_text = text

                st.session_state.pdf_name = (
                    uploaded_pdf.name
                )

                st.success(
                    "PDF loaded successfully!"
                )

            except Exception as error:

                st.error(
                    "Could not read PDF: "
                    + str(error)
                )


    if st.session_state.pdf_name:

        st.caption(
            "📄 Loaded: "
            + st.session_state.pdf_name
        )


    st.divider()


    # =====================================================
    # NOTES
    # =====================================================

    st.markdown("### 📝 Quick Note")

    note = st.text_area(
        "Write a note",
        placeholder="Type something you want to save..."
    )


    if st.button(
        "💾 Save Note",
        use_container_width=True
    ):

        if note.strip():

            save_note(
                note.strip()
            )

            st.success(
                "Note saved!"
            )


    if os.path.exists(NOTES_FILE):

        if st.button(
            "📖 Show Notes",
            use_container_width=True
        ):

            with open(
                NOTES_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                notes = file.read()

            st.text_area(
                "Your Notes",
                notes,
                height=200
            )


    st.divider()


    # =====================================================
    # AI INFORMATION
    # =====================================================

    st.markdown("### 🤖 AI Information")

    st.markdown(
        """
**Model**

`qwen2.5:0.5b`

**Engine**

Ollama

**Type**

Local AI

**Cost**

Free 🆓

**Memory**

Enabled 🧠

**PDF**

Supported 📄

**Voice**

Supported 🎤

**Web**

Optional 🌐
"""
    )


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    '<div class="main-title">'
    '🤖 My Personal AI'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    '<div class="subtitle">'
    'Your private AI assistant running on your computer'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# WELCOME SCREEN
# =========================================================

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="welcome-card">'
        '<div class="robot">🤖</div>'
        '<div class="welcome-title">'
        'Hello! I\'m your Personal AI'
        '</div>'
        '<div class="welcome-text">'
        'Ask questions, learn something new, '
        'upload PDFs, search the web, '
        'or talk using your voice.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# VOICE INPUT
# =========================================================

voice_text = None

if speech_to_text is not None:

    try:

        voice_text = speech_to_text(
            language="en",
            start_prompt="🎤 Start Speaking",
            stop_prompt="⏹️ Stop",
            just_once=True,
            use_container_width=True,
            key="voice_input"
        )

    except:

        voice_text = None


# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for message in st.session_state.messages:

    if message["role"] == "user":

        with st.chat_message(
            "user",
            avatar="👤"
        ):

            st.markdown(
                message["content"]
            )

    elif message["role"] == "assistant":

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            st.markdown(
                message["content"]
            )


# =========================================================
# CHAT INPUT
# =========================================================

typed_message = st.chat_input(
    "💬 Ask your AI anything..."
)


# =========================================================
# GET USER MESSAGE
# =========================================================

user_message = None


if typed_message:

    user_message = typed_message


elif voice_text:

    user_message = voice_text


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_message:

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message(
        "user",
        avatar="👤"
    ):

        st.markdown(
            user_message
        )


    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # =====================================================
    # BUILD AI CONTEXT
    # =====================================================

    context = ""


    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    if st.session_state.memory:

        context += "\n\nUSER MEMORY:\n"

        for item in st.session_state.memory:

            context += (
                "- "
                + item
                + "\n"
            )


    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    if st.session_state.pdf_text:

        # Limit PDF text to avoid making the tiny model
        # extremely slow.

        pdf_context = (
            st.session_state.pdf_text[:12000]
        )

        context += (
            "\n\nPDF CONTENT:\n"
            + pdf_context
        )


    # -----------------------------------------------------
    # WEB SEARCH
    # -----------------------------------------------------

    if web_search:

        if DDGS is not None:

            try:

                with st.spinner(
                    "🌐 Searching the web..."
                ):

                    search_results = (
                        DDGS().text(
                            user_message,
                            max_results=5
                        )
                    )


                context += (
                    "\n\nWEB SEARCH RESULTS:\n"
                )


                for result in search_results:

                    title = result.get(
                        "title",
                        ""
                    )

                    body = result.get(
                        "body",
                        ""
                    )

                    url = result.get(
                        "href",
                        ""
                    )

                    context += (
                        "\nTitle: "
                        + title
                        + "\n"
                    )

                    context += (
                        "Information: "
                        + body
                        + "\n"
                    )

                    context += (
                        "Source: "
                        + url
                        + "\n"
                    )


            except Exception as error:

                context += (
                    "\nWeb search failed: "
                    + str(error)
                )


    # =====================================================
    # SYSTEM INSTRUCTIONS
    # =====================================================

    system_message = """
You are My Personal AI.

You are helpful, friendly and concise.

Explain difficult topics in simple language.

If the user asks about their uploaded PDF,
use the PDF content provided.

If web search information is provided,
use it carefully and mention that it came
from web search.

Remember the user's saved preferences
when relevant.

Do not pretend you performed an action
if you did not actually perform it.

If you don't know something, say so.
"""


    if context:

        system_message += (
            "\n\nAdditional context:"
            + context
        )


    # =====================================================
    # AI RESPONSE
    # =====================================================

    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):

        response_placeholder = st.empty()

        full_response = ""

        try:

            # Keep conversation smaller to improve speed.
            recent_messages = (
                st.session_state.messages[-10:]
            )


            messages_for_ai = [
                {
                    "role": "system",
                    "content": system_message
                }
            ]


            messages_for_ai.extend(
                recent_messages
            )


            stream = ollama.chat(

                model="qwen2.5:0.5b",

                messages=messages_for_ai,

                stream=True,

                options={
                    "temperature": 0.5,
                    "num_predict": 300
                }
            )


            # -------------------------------------------------
            # STREAM RESPONSE
            # -------------------------------------------------

            for chunk in stream:

                text = (
                    chunk["message"]["content"]
                )

                full_response += text

                response_placeholder.markdown(
                    full_response + "▌"
                )


            response_placeholder.markdown(
                full_response
            )


        except Exception as error:

            full_response = (
                "❌ Something went wrong.\n\n"
                + str(error)
            )

            response_placeholder.error(
                full_response
            )


    # =====================================================
    # SAVE AI RESPONSE
    # =====================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )


    save_chat(
        st.session_state.messages
    )


    # =====================================================
    # VOICE OUTPUT
    # =====================================================

    if voice_output and full_response:

        try:

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                175
            )

            engine.say(
                full_response
            )

            engine.runAndWait()

            engine.stop()

        except Exception as error:

            st.warning(
                "Voice output could not be started."
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🤖 Local AI • 🧠 Memory • 🎤 Voice • '
    '📄 PDF • 🌐 Web Search • Free'
    '</div>',
    unsafe_allow_html=True
)
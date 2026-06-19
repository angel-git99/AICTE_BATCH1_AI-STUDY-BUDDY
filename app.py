import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. Initialize and secure the Gemini Client
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

try:
    client = get_gemini_client()
except Exception as e:
    st.error("🔑 API Key Missing! Please configure your secrets.toml file locally.")
    st.stop()

# 2. Page Configuration Layout
st.set_page_config(page_title="AI Study Buddy", page_icon="📚", layout="centered")
st.title("📚 AI-Powered Study Buddy")
st.caption("Transform dense lecture material into clear summaries, flashcards, or interactive quizzes.")

# 3. Material Input Source (Text Input or PDF Upload)
st.subheader("📋 Step 1: Provide Your Study Material")
input_method = st.radio("Choose input method:", ["✏️ Paste Text", "📂 Upload Lecture PDF"], horizontal=True)

study_material = ""

if input_method == "✏️ Paste Text":
    study_material = st.text_area(
        "Paste textbook chapters, paragraphs, or lecture slides here:",
        placeholder="Type or paste study content here...",
        height=200
    )
else:
    uploaded_file = st.file_uploader("Upload your lecture notes (.pdf format only)", type=["pdf"])
    if uploaded_file is not None:
        try:
            with st.spinner("Extracting text from PDF..."):
                reader = PdfReader(uploaded_file)
                extracted_text = ""
                for page in reader.pages:
                    text_content = page.extract_text()
                    if text_content:
                        extracted_text += text_content + "\n"
                study_material = extracted_text
                st.success(f"Successfully extracted content from '{uploaded_file.name}'!")
        except Exception as e:
            st.error(f"Error reading PDF file: {e}")

# 4. Selecting the AI Tool Configuration
st.subheader("⚙️ Step 2: Choose Your AI Study Tool")
tool_option = st.radio(
    "What would you like the AI engine to generate?",
    ["⚡ Quick Summary", "🗂️ Interactive Concept Flashcards", "📝 Instant Interactive Quiz"],
    horizontal=True
)

# 5. Core Execution Pipeline
if st.button("Generate AI Study Assets", type="primary"):
    if not study_material.strip():
        st.warning("Please provide study material by pasting text or uploading a valid PDF file first.")
    else:
        with st.spinner("AI is processing your materials..."):
            try:
                # Tailor instructions conditionally based on selected menu options
                if tool_option == "⚡ Quick Summary":
                    system_instruction = (
                        "You are an elite academic tutor. Summarize the provided text into clear, "
                        "high-level bullet points. Highlight key technical concepts in bold markdown text. "
                        "Include a 2-sentence 'TL;DR Summary' at the very top."
                    )
                elif tool_option == "🗂️ Interactive Concept Flashcards":
                    system_instruction = (
                        "You are an academic coach. Break down the provided text into critical concepts. "
                        "Format your response strictly as a series of flashcards. "
                        "Each card must contain 'FRONT: [Concept or Question]' followed immediately by "
                        "'BACK: [Definition or Answer]'. Do not combine them on the same line."
                    )
                else:  # Interactive Quiz
                    system_instruction = (
                        "You are a university professor. Generate a 3-question Multiple Choice Quiz based "
                        "strictly on the provided text. Provide the questions, marked options (A, B, C, D), "
                        "and hide the answers at the very bottom inside a clearly separated 'Answer Key' section."
                    )

                # Send content to the Gemini API
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[study_material],
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.3,
                    )
                )

                output_text = response.text

                # 6. Streamlit User Interface Rendering Logic
                st.subheader(f"✨ Your Generated {tool_option}")
                
                # Custom rendering block for visual Flashcard Expanders
                if tool_option == "🗂️ Interactive Concept Flashcards":
                    cards = output_text.split("FRONT:")
                    card_count = 1
                    for card in cards:
                        if "BACK:" in card:
                            parts = card.split("BACK:")
                            front_side = parts[0].strip()
                            back_side = parts[1].strip()
                            
                            with st.expander(f"🎴 Flashcard {card_count}: {front_side}"):
                                st.markdown(f"**Answer:** {back_side}")
                            card_count += 1
                
                # Custom rendering block for collapsible Quiz Dropdowns
                elif tool_option == "📝 Instant Interactive Quiz":
                    if "Answer Key" in output_text:
                        quiz_part, answer_part = output_text.split("Answer Key")
                        st.markdown(quiz_part)
                        with st.expander("👁️ Reveal Quiz Answer Key"):
                            st.markdown(answer_part)
                    else:
                        st.markdown(output_text)
                
                # Standard markdown print layout for Summary
                else:
                    st.markdown(output_text)

            except Exception as e:
                st.error(f"Error communicating with Gemini: {e}")

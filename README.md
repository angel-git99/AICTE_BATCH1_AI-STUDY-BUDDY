# 📚 AI-Powered Study Buddy

A high-performance, generative AI web application built to streamline and democratize academic learning pipelines. This platform takes dense text or multi-page lecture PDFs and instantly synthesizes them into actionable, active-recall study assets.

## 🚀 Core Features

- **⚡ Abstractive TL;DR Summarizer:** Condenses expansive textbook chapters or lecture notes into high-yield bullet points with bold key concepts.
- **🗂️ Interactive Concept Flashcards:** Leverages structural string-parsing to dynamically map complex definitions into digital, clickable expandable cards.
- **📝 Automated Quiz Engine:** Dynamically generates professor-style multiple-choice questions matching input text parameters, complete with a collapsible answer key.
- **📂 Multi-Format Ingestion:** Equipped with a backend file stream processing tracker to decode and clean unstructured text straight from uploaded `.pdf` documents.

## 🛠️ Tech Stack & System Architecture

- **Frontend Interface:** Streamlit (UI state management and responsive web forms)
- **AI Core Framework:** Google Gemini 2.5 Flash Engine (Connected via the modern `google-genai` SDK)
- **Document Preprocessing:** PyPDF File Parser (Dynamic binary text-stream extraction)
- **Language Environment:** Python 3.12+

## 🛡️ Setup & Installation for Reviewers

To run this repository locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd AICTE_BATCH1_AI-STUDY-BUDDY
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Local Credentials:**
   - Create a hidden folder named `.streamlit/` in the root directory.
   - Inside that folder, create a file named `secrets.toml`.
   - Add your personal Google AI Studio API key:
     ```toml
     GEMINI_API_KEY = "your_actual_gemini_api_key_here"
     ```

4. **Launch the application server:**
   ```bash
   streamlit run app.py
   ```

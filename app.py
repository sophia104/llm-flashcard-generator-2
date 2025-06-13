import streamlit as st
import openai
from flashcard_generator import generate_flashcards
from utils import read_pdf, read_text, export_to_csv, export_to_json

st.set_page_config(page_title="Flashcard Generator", layout="wide")

st.title("📚 LLM Flashcard Generator")

#openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter OpenAI API Key:", type="password")
api_key = st.text_input("🔑 Enter OpenAI API Key:", type="password")
openai.api_key = api_key

subject = st.selectbox("Select Subject (optional)", ["General", "Biology", "History", "Computer Science", "Physics"])

uploaded_file = st.file_uploader("Upload a .txt or .pdf file", type=["pdf", "txt"])
raw_text = st.text_area("Or paste text here")

if st.button("Generate Flashcards"):
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            content = read_pdf(uploaded_file)
        else:
            content = read_text(uploaded_file)
    elif raw_text:
        content = raw_text
    else:
        st.error("Please provide input via file or text.")
        st.stop()

    with st.spinner("Generating flashcards..."):
        flashcards = generate_flashcards(content, subject=subject, api_key=api_key)
    
    if flashcards:
        st.success(f"Generated {len(flashcards)} flashcards!")
        for card in flashcards:
            st.markdown(f"**Q:** {card['question']}\n\n**A:** {card['answer']}")
            if 'topic' in card:
                st.caption(f"Topic: {card['topic']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Export as CSV"):
                export_to_csv(flashcards, "output/flashcards.csv")
                st.success("Saved as flashcards.csv in output/")
        with col2:
            if st.button("Export as JSON"):
                export_to_json(flashcards, "output/flashcards.json")
                st.success("Saved as flashcards.json in output/")
    else:
        st.error("No flashcards generated. Try again with more content.")

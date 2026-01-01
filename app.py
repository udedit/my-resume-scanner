import streamlit as st
import PyPDF2
import spacy

# Page Setup
st.set_page_config(page_title="Resume Scanner", page_icon="📄")
st.title("📄 Resume Keyword Matcher")

# Model Loading (Simple method for cloud)
@st.cache_resource
def load_nlp():
    # Hum model download karne ka command direct code mein chala rahe hain
    try:
        return spacy.load("en_core_web_sm")
    except:
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_nlp()

# Function to read PDF
def extract_text_from_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# UI Layout
st.write("Apna Resume aur Job Description daalein, hum match check karenge.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
jd = st.text_area("Job Description Paste karein")

if st.button("Check Match"):
    if uploaded_file and jd:
        # Processing
        resume_text = extract_text_from_pdf(uploaded_file)
        
        doc_resume = nlp(resume_text)
        doc_jd = nlp(jd)
        
        # Keywords nikaalna (Sirf Nouns)
        res_words = set([token.text.lower() for token in doc_resume if token.pos_ in ["NOUN", "PROPN"]])
        jd_words = set([token.text.lower() for token in doc_jd if token.pos_ in ["NOUN", "PROPN"]])
        
        # Match calculation
        common = res_words.intersection(jd_words)
        missing = jd_words - res_words
        score = len(common) / len(jd_words) * 100 if len(jd_words) > 0 else 0
        
        st.subheader(f"Match Score: {score:.0f}%")
        st.write("Ye words missing hain:")
        st.error(", ".join(missing))
    else:
        st.warning("Dono cheezein fill karein!")
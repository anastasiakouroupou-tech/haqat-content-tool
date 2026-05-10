import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mystic Blog Content Studio", layout="wide")
st.title("🌙 Mystic Blog Content Studio")

# Αρχικοποίηση ιστορικού στη μνήμη
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Σύνδεση με το κλειδί
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Πρόβλημα σύνδεσης")

tab1, tab2, tab3 = st.tabs(["✨ Δημιουργία", "🔍 SEO Keywords", "📜 Ιστορικό"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        c_type = st.selectbox("Τύπος", ["Άρθρο blog", "Social post", "Newsletter"])
        topic = st.text_input("Θέμα / Keyword", key="main_topic")
        category = st.selectbox("Θεματική", ["Witchcraft", "Αστρολογία", "Tarot", "Ελληνική λαϊκή μαγεία"])
        if st.button("Επίκληση Περιεχομένου", type="primary"):
            with st.spinner("Η Gemini υφαίνει το κείμενο..."):
                prompt = f"Δημιούργησε {c_type} για {category}. Θέμα {topic}"
                response = model.generate_content(prompt)
                st.session_state['last_output'] = response.text
                st.session_state['history'].append({"type": c_type, "topic": topic, "content": response.text})

    with col2:
        if 'last_output' in st.session_state:
            st.markdown(st.session_state['last_output'])

with tab2:
    st.header("Στρατηγική SEO")
    seo_topic = st.text_input("Θέμα για ανάλυση Keywords")
    if st.button("Ανάλυση"):
        with st.spinner("Αναζήτηση μαγικών λέξεων..."):
            seo_prompt = f"Πρότεινε 10 LSI keywords και SEO τίτλους για το θέμα {seo_topic}"
            seo_res = model.generate_content(seo_prompt)
            st.write(seo_res.text)

with tab3:
    st.header("Αρχείο Δημιουργιών")
    for item in reversed(st.session_state['history']):
        with st.expander(f"{item['type']} - {item['topic']}"):
            st.write(item['content']) 
import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Mystic Blog Content Studio", layout="wide")
st.title("🌙 Mystic Blog Content Studio")

# Σύνδεση με το κλειδί από τα secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Πρόβλημα με το κλειδί στο secrets.toml: {e}")

tab1, tab2, tab3 = st.tabs(["✨ Δημιουργία", "🔍 SEO Keywords", "📜 Ιστορικό"])

with tab1:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        c_type = st.selectbox("Τύπος", ["Άρθρο blog", "Social post", "Newsletter", "Τίτλοι ×5"])
        topic = st.text_input("Θέμα / Keyword")
        category = st.selectbox("Θεματική", ["Witchcraft", "Αστρολογία", "Tarot", "Ελληνική λαϊκή μαγεία"])
        lang = st.radio("Γλώσσα", ["Ελληνικά", "English"], horizontal=True)
        tone = st.select_slider("Ύφος", options=["Μυστηριακό", "Εκπαιδευτικό", "Προσιτό"])
        
        if st.button("Επίκληση Περιεχομένου", type="primary"):
            if not topic:
                st.warning("Συμπλήρωσε ένα θέμα.")
            else:
                with st.spinner("Η Gemini υφαίνει το κείμενο..."):
                    try:
                        # Χρήση του gemini-2.5-flash που είναι διαθέσιμο σε εσάς
                        model = genai.GenerativeModel('gemini-2.5-flash')
                        prompt = f"Δημιούργησε {c_type} για {category}. Θέμα: {topic}. Γλώσσα: {lang}. Ύφος: {tone}. Εστίασε στην ποιότητα και την αυθεντικότητα."
                        response = model.generate_content(prompt)
                        st.session_state['last_output'] = response.text
                    except Exception as e:
                        st.error(f"Σφάλμα κατά την παραγωγή: {e}")

    with col2:
        st.markdown("### Output")
        if 'last_output' in st.session_state:
            st.markdown(st.session_state['last_output'])
            st.divider()
            if st.button("📋 Αντιγραφή"):
                st.info("Το κείμενο είναι έτοιμο για αντιγραφή (Ctrl+C από την οθόνη).")
        else:
            st.info("Το κείμενο θα εμφανιστεί εδώ μόλις πατήσεις τη Δημιουργία.")
            
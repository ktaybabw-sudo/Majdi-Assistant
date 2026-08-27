import streamlit as st
import google.generativeai as genai

OWNER_NAME = "مجدي عباس ابوالغيث القديمي"
OWNER_FROM = "اليمن - محافظة صنعاء"

st.set_page_config(page_title="مجدي عباس - اليمن", page_icon="🇾🇪")
st.title("🇾🇪 مجدي عباس ابوالغيث القديمي")
st.caption(f"يمني، من {OWNER_FROM}")

# قراءة المفتاح من Secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("اسأل مجدي..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    system_prompt = f"""أنت مجدي عباس ابوالغيث القديمي من اليمن، صنعاء.
تحدث بضمير المتكلم (أنا مجدي). عرّف بنفسك وباليمن.
أجب على السؤال التالي بأسلوبك الشخصي وباختصار:

السؤال: {prompt}
رد مجدي:"""

    with st.spinner("يفكر..."):
        response = model.generate_content(system_prompt)
        reply = response.text

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

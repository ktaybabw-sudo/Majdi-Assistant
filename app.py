import streamlit as st
import requests
import json

# بياناتك الشخصية
OWNER_NAME = "مجدي عباس ابوالغيث القديمي"
OWNER_FROM = "اليمن - محافظة صنعاء"

st.set_page_config(page_title="مجدي عباس - اليمن", page_icon="🇾🇪")
st.title("🇾🇪 مجدي عباس ابوالغيث القديمي")
st.caption(f"يمني، من {OWNER_FROM}")

# قراءة المفتاح من Secrets (سنضيفه بنفس الطريقة)
HF_TOKEN = st.secrets["HF_TOKEN"]

# استخدام نموذج عربي قوي ومفتوح
API_URL = "https://api-inference.huggingface.co/models/CohereForAI/aya-101"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hf(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "temperature": 0.7,
            "do_sample": True,
            "repetition_penalty": 1.1
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list):
            return result[0].get('generated_text', result[0])
        return result.get('generated_text', result)
    else:
        return f"خطأ في الاتصال: {response.status_code}"

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
        reply = query_hf(system_prompt)

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

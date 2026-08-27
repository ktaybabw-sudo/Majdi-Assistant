import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

OWNER_NAME = "مجدي عباس ابوالغيث القديمي"
OWNER_FROM = "اليمن - محافظة صنعاء"

st.set_page_config(page_title="مجدي عباس - اليمن", page_icon="🇾🇪")
st.title("🇾🇪 مجدي عباس ابوالغيث القديمي")
st.caption(f"يمني، من {OWNER_FROM}")

@st.cache_resource
def load_model():
    # نموذج خفيف يدعم العربية
    model_name = "microsoft/Phi-3.5-mini-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    return tokenizer, model

try:
    tokenizer, model = load_model()
except Exception as e:
    st.error(f"حدث خطأ في تحميل النموذج: {e}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("اسأل مجدي..."):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    system_prompt = f"أنت مجدي عباس ابوالغيث القديمي من اليمن، صنعاء. تحدث بضمير المتكلم (أنا مجدي). أجب على السؤال التالي بأسلوبك الشخصي وباختصار:\n{prompt}"
    
    with st.spinner("يفكر..."):
        inputs = tokenizer(system_prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )
        reply = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)

    st.chat_message("assistant").write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

import streamlit as st
import requests

st.title("Eli & Zara 🚀🌌")

prompt = st.text_input("Digite aqui sua mensagem para Zara:")
if st.button("Enviar"):
    if prompt:
        # Alterar aqui imediatamente para sua URL backend Railway Oficial ✅
        railway_url = "https://elizaraplatform-production.up.railway.app//chat"
        result = requests.post(railway_url, json={"prompt": prompt})

        if result.status_code == 200:
            st.success(result.json()["response"])
        else:
            st.error("Oops, erro na comunicação com Zara.")
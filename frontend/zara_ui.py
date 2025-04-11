import streamlit as st
import requests

st.title("Eli & Zara")

prompt = st.text_input("Digite a mensagem para Zara")
if st.button("Enviar"):
    backend_url = "https://elizaraplatform-production.up.railway.app/chat"
    if prompt:
        resposta = requests.post(backend_url, json={"prompt": prompt})
        if resposta.status_code == 200:
            st.write(resposta.json()['response'])
        else:
            st.error("Erro de comunicação com o backend.")
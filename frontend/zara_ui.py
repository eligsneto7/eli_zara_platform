import streamlit as st
import requests

# título interface Eli & Zara claramente definido
st.title("Eli & Zara 🚀🌌")

# campo mensagem usuário envia para Zara
prompt = st.text_input("Digite aqui sua mensagem para Zara:")

# botão claro de envio & ação API backend railway imediatamente configurada
if st.button("Enviar"):
    if prompt:
        # ⚠️ COLOQUE claramente ABAIXO EXATAMENTE sua URL pública completa Railway backend Flask atual já funcionando comprovadamente:
        railway_url = "https://elizaraplatform-production.up.railway.app/chat"
        
        # envia claramente request para backend Railway Flask API
        result = requests.post(railway_url, json={"prompt": prompt})

        # tratamento imediato resposta railway backend API rapidamente
        if result.status_code == 200:
            st.success(result.json()["response"])
        else:
            st.error("Oops, erro na comunicação com Zara.")
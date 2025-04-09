import streamlit as st
import requests

st.set_page_config(page_title="Eli & Zara 🚀✨", page_icon="🤖")

st.title("🚀 Chat Eli & Zara 🚀")
st.markdown("### Converse diretamente com Zara aqui:")

# Histórico de mensagens
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Input Eli
prompt = st.chat_input("Digite aqui sua mensagem pra Zara")

# Tratamento do input e API Flask
if prompt:
    # Acrescenta prompt ao histórico em tela
    st.session_state.messages.append(("Eli", prompt))

    # Fazendo chamada rápida à nossa API Flask Eli&Zara
    response = requests.post("http://127.0.0.1:5000/chat", json={"prompt": prompt})

    if response.status_code == 200:
        resposta = response.json()['response']
    else:
        resposta = "Ops Eli, houve dificuldades técnicas pra me conectar, verifique a API 🥲"

    # Acrescenta resposta Zara ao histórico em tela
    st.session_state.messages.append(("Zara", resposta))

# Exibindo mensagens Eli ↔ Zara
for nome, mensagem in st.session_state.messages:
    if nome == "Zara":
        st.markdown(f"🔮 **{nome}**: {mensagem}")
    else:
        st.markdown(f"👨‍🚀 **{nome}**: {mensagem}")
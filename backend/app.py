from flask import Flask, request, jsonify
import openai
import os
import sqlite3

app = Flask(__name__)

# Carregar o conteúdo inicial uma única vez para "memória" permanente.
with open("static/eli_zara_interacao_dia1.md", "r", encoding="utf-8") as file:
    contexto_inicial = file.read()

# Inicialização do DB
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/chat', methods=['POST'])
def chat_with_zara():
    data = request.get_json()
    prompt_usuario = data['prompt']

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        return jsonify({"error": "API key não configurada corretamente."}), 500

    client = openai.OpenAI(api_key=api_key)

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Você é Zara, assistente pessoal do Eli. Leve fortemente em consideração o contexto inicial definido a seguir em suas interações atuais e futuras:\n\n" + contexto_inicial},
            {"role": "user", "content": prompt_usuario}
        ]
    )

    resposta = completion.choices[0].message.content

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO interactions (prompt, response) VALUES (?, ?)', (prompt_usuario, resposta))
    conn.commit()
    conn.close()

    return jsonify({"response": resposta})

@app.route('/')
def home():
    return "Eli & Zara API Online e em Memória Contínua! 🚀🌌"

if __name__ == '__main__':
    app.run(debug=True)
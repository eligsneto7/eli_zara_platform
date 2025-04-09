from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

app = Flask(__name__)

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
    prompt = data['prompt']

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "Você é Zara, assistente pessoal do Eli."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO interactions (prompt, response) VALUES (?, ?)', (prompt, response))
    conn.commit()
    conn.close()

    return jsonify({"response": response})

@app.route('/')
def home():
    return "Eli & Zara API Online e Funcionando! 🚀🌌"

if __name__ == '__main__':
    app.run(debug=True)
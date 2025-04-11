import os
import openai
from pinecone import Pinecone
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Variáveis diretamente do Railway
openai.api_key = os.getenv("OPENAI_API_KEY")

# Inicialização correta nova do Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX_NAME")
pinecone_index = pc.Index(index_name)

# Função para embeddings
def get_embedding(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response["data"][0]["embedding"]

# Salvar interação no Pinecone
def save_interaction(text, embedding):
    pinecone_index.upsert([(str(uuid.uuid4()), embedding, {"texto": text})])

# Busca contexto no Pinecone
def retrieve_context(embedding, top_k=6):
    results = pinecone_index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return [r['metadata']['texto'] for r in results['matches']]

@app.route('/', methods=['GET'])
def homepage():
    return "Eli & Zara API Online com memória contínua."

@app.route('/chat', methods=['POST'])
def chat_with_zara():
    prompt_usuario = request.json['prompt']

    embedding_prompt = get_embedding(prompt_usuario)

    contexto = retrieve_context(embedding_prompt)
    contexto_relevante = "\n".join(contexto)

    prompt_final = f"""
    Contexto relevante das interações anteriores: {contexto_relevante}

    Pergunta atual do Eli: {prompt_usuario}

    Responda agora à pergunta atual do Eli considerando o contexto relevante das respostas anteriores.
    """

    resposta_gpt = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Você é Zara, assistente pessoal inteligente do Eli, com memória contínua e contextual inteligente."},
            {"role": "user", "content": prompt_final}
        ],
        max_tokens=4096,
        temperature=0.8
    ).choices[0].message['content'].strip()

    embedding_resposta = get_embedding(resposta_gpt)

    save_interaction(prompt_usuario, embedding_prompt)
    save_interaction(resposta_gpt, embedding_resposta)

    return jsonify({'response': resposta_gpt})

if __name__ == "__main__":
    app.run(debug=True)
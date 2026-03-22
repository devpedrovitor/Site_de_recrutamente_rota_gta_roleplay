import time
import asyncio
import threading
import os
from flask import Flask, render_template, request, session
from pymongo.errors import ConnectionFailure
from modules.mongodb_conncetion import MongoDBConnectionHandler
from bot import bot, enviar_discord
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='template')
app.secret_key = 'b9fc4281510749bb582f6bd995cc4bc5aa45f1a09c7f6a3c07e61ff9c27240ae'

connection = MongoDBConnectionHandler().valid_connection()

if connection is None:
    raise RuntimeError("Não foi possível conectar ao MongoDB")

db = connection['result_forms']
colecao = db['result_users']

@app.route("/")
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        documento = {
            "name":       request.form.get("f-nome"),
            "age":        request.form.get("f-idade"),
            "nick":       request.form.get("f-nick"),
            "discord":    request.form.get("f-discord"),
            "server_id":  request.form.get("f-id"),
            "exp":        request.form.get("exp"),
            "hist":       request.form.get("f-hist"),
            "rdm":        request.form.get("f-rdm"),
            "vdm":        request.form.get("f-vdm"),
            "pg":         request.form.get("f-pg"),
            "meta":       request.form.get("f-meta"),
            "car_jacking":request.form.get("f-cj"),
            "surf":       request.form.get("f-surf"),
            "disp":       request.form.get("disp"),
            "status":     "pendente",   # campo para controle de aprovação
        }

        result = colecao.insert_one(documento)
        session['id'] = str(result.inserted_id)
        return render_template('tatico.html')

    return render_template('formulario.html')


@app.route('/tatico', methods=['GET', 'POST'])
def tatico():
    user_id = session.get('id')

    if request.method == 'POST':
        if not user_id:
            return render_template('index.html')  # sessão perdida, volta ao início

        tatico_doc = {
            'q1': request.form.get("q1"),
            'q2': request.form.get("q2"),
            'q3': request.form.get("q3"),
            'q4': request.form.get("q4"),
            'q5': request.form.get("q5"),
            'q6': request.form.get("q6"),
        }

        # Atualiza o documento 
        colecao.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": tatico_doc}
        )

        # Busca o documento completo (pessoal + tático)
        documento_completo = colecao.find_one({"_id": ObjectId(user_id)})

        # ✅ Dispara a embed no Discord com tudo preenchido
        if documento_completo:
            asyncio.run_coroutine_threadsafe(
                enviar_discord(documento_completo),
                bot.loop
            )

        time.sleep(1.5)
        return render_template("index.html")

    return render_template('tatico.html')
def iniciar_flask():
    print("🌐 Flask iniciando na porta 5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=iniciar_flask, daemon=True)
    flask_thread.start()

    print("🤖 Bot do Discord iniciando...")
    bot.run(os.getenv("TOKEN_DISCORD"))  # ← token 

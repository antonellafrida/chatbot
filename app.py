from flask import Flask, render_template, request, jsonify
import spacy


app = Flask(__name__, template_folder='templates', static_folder='static')


try:
    nlp = spacy.load("es_core_news_md")
except:
    
    print("Error: Modelo es_core_news_md no encontrado.")


conocimiento = {
    "conexion": {
        "respuesta": "Para problemas de conexión: Asegúrate de que el cable esté conectado, reinicia el router y verifica el Wi-Fi.",
        "keywords": "conexion internet red wifi router cable navegacion lento error conexion caida datos"
    },
    "password": {
        "respuesta": "Para contraseñas: Visita 'soporte.empresa.com/recuperar' para restablecerla usando tu correo institucional.",
        "keywords": "contraseña clave password acceso ingresar login olvide cuenta recuperar restablecer"
    },
    "impresora": {
        "respuesta": "Para impresoras: Revisa los niveles de tinta, verifica que esté encendida y comprueba la conexión USB o Wi-Fi.",
        "keywords": "impresora papel tinta atasco escaner imprimir toner"
    },
    "humano": {
        "respuesta": "Para hablar con un humano, por favor llama a soporte técnico al +58 04247552171.",
        "keywords": "humano persona soporte tecnico ayuda hablar agente representante"
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chat():
    user_input_raw = request.form["msg"]
    user_doc = nlp(user_input_raw.lower())
    
    mejor_respuesta = "Lo siento, no logré interpretar tu solicitud. ¿Podrías ser más específico?"
    mayor_similitud = 0
    umbral_minimo = 0.3  # Ajustado a 0.3 para mayor flexibilidad

    
    for categoria, datos in conocimiento.items():
        keyword_doc = nlp(datos["keywords"])
        similitud = user_doc.similarity(keyword_doc)
        
        
        print(f"Input: {user_input_raw} | Categoría: {categoria} | Similitud: {similitud:.2f}")
        
        if similitud > mayor_similitud and similitud > umbral_minimo:
            mayor_similitud = similitud
            mejor_respuesta = datos["respuesta"]
            
    return jsonify({"response": mejor_respuesta})

if __name__ == "__main__":
    app.run(debug=True)
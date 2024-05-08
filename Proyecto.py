from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

uri = "..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultados', methods=['POST'])
def resultados():
    barrio = request.form['...']
    dia = request.form['DIA']  

    cliente = MongoClient(uri)
    db = cliente.get_database("Contaminacion")
    coleccion = db.get_collection("...")
    datos_contaminacion = coleccion.find_one({"...": barrio, "DIA": dia})  
    cliente.close()

    return render_template('resultados.html', datos_contaminacion=datos_contaminacion)

if __name__ == '__main__':
    app.run(debug=True)

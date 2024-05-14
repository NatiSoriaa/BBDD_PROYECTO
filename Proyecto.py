<<<<<<< Updated upstream
from flask import Flask, render_template, request
from pymongo import MongoClient
=======
import pymongo
from pymongo import MongoClient


MONGO_URI = 'mongodb+srv://natgsarabia:Fsu6t4y5jUfhYQxI@contaminacionbcn.xbosddo.mongodb.net/'

myClient = pymongo.MongoClient(MONGO_URI)

myDB = myClient['contaminacionBCN']

collection=myDB['CalidadAire']
user=57

for items in collection.find({'Estacio':user}):
    print(items)

# print(myDB.list_collection_names())

# def InsertData():
#     myTask = {"Estación":"ETP Xavier", "Barrio":"Ciutat Vella"}
#     result = myCollection.insert_one (myTask)
#     print(result)

# #InsertData()

# # #Leer un dato
# def ReadOne():

#     result = myCollection.find_one()
#     print(result)

# #ReadOne()

# #Leer todos los datos
# def ReadAll():
#     result = myCollection.find()    #nos devuelve un cursor
#     for documento in result:
#         print(documento)

>>>>>>> Stashed changes

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

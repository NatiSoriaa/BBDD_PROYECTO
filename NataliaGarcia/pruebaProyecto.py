import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


def iniciarMongoDB():
    MONGO_URI = 'mongodb+srv://natgsarabia:Fsu6t4y5jUfhYQxI@contaminacionbcn.xbosddo.mongodb.net/'

    myClient = pymongo.MongoClient(MONGO_URI)

    myDB = myClient['contaminacionBCN']
    return myDB


# FUNCIÓN EXTRAER NOMBRES BARRIOS
def encontrarBarrios(myDB):
    collection=myDB['Estaciones']
    listaBarrios=collection.distinct('Nom_barri')
    return listaBarrios

# FUNCIÓN EXTRAER UBICACION ESTACIONES
def informacionEstacion(myDB,barrio):
    estaciones=myDB['Estaciones']

    query={'Codi_barri': barrio}
    informacionEstacion=[]
  
    iter=estaciones.find(query,{'_id':0, 'nom_cabina':1,'ubicacio':1})
    i=0
    for doc in iter:
        doc=dict(doc)
        valoresDoc=doc.items()
        listaDatos=list(valoresDoc)
        informacionEstacion.insert(i,listaDatos[0][1])
        informacionEstacion.insert(i,listaDatos[1][1])
        i+=1

    
    return informacionEstacion


# FUNCIÓN BUSQUEDA RESULTADO
def find(myDB,codigoEstacion, diaMes):
    collection=myDB['CalidadAire']
    query={'ESTACIO': codigoEstacion, 'DIA':diaMes}
  
    codigosContaminantesActivos=[]
    
    iter=collection.find(query,{'CODI_CONTAMINANT':1})
    i=0
    for doc in iter:
        doc=dict(doc)
        valoresDoc=doc.items()
        listaDatos=list(valoresDoc)
        codigosContaminantesActivos.insert(i,listaDatos[1][1])
        i+=1

    return(codigosContaminantesActivos)

# ENCONTRAR NOMBRE BARRIO
def checkCodigoBarrio(barrioHTML):
    barrios = {
        "el Poblenou":4,
        "Sants":42,
        "la Nova Esquerra de l'Eixample" : 43,
        "la Vila de Gracia" : 44,
        "Sant Pere, Santa Caterina i la Ribera" : 50,
        "la Vall d'Hebron" : 54,
        "Pedralbes":57,
        "Vallvidrera-el Tibidabo-les Planes":58
    }

    return barrios.get(barrioHTML)


# FUNCIÓN BUSQUEDA CONTAMINANTES 
def buscarContaminantes(myDB,listaContaminantes):
    nombresContamimantes=[]
    collection=myDB['Contaminantes']

    i=0

    for contaminante in listaContaminantes:
        query={'Codi_Contaminant': contaminante}
        iter=collection.find(query,{'Desc_Contaminant':1})
        for item in iter:
            contaminantes=dict(item)
            nombreContamimante=contaminantes.items()
            listaNombrescontaminantes=list(nombreContamimante)
            nombresContamimantes.insert(i,listaNombrescontaminantes[1][1])
            i+=1     
            
    return(nombresContamimantes)




@app.route('/paginaInicio', methods=["GET","POST"])

def index():
    myDB=iniciarMongoDB()
    if request.method=="GET":
        listaBarrios=encontrarBarrios(myDB)
        return render_template("paginaInicio.html",listaBarrios=listaBarrios)

    elif request.method=="POST":
        barrioHTML=request.form.get("barrioHTML")
        barrio=checkCodigoBarrio(barrioHTML)

        diaMes=request.form.get("diaHTML")

        codigosContaminantes=find(myDB, int(barrio), int(diaMes))
        nombresContaminantes=buscarContaminantes(myDB,codigosContaminantes)
        ubicacionEstacion=informacionEstacion(myDB,int(barrio))
        print(codigosContaminantes)
        print(nombresContaminantes)
        print(ubicacionEstacion)
        
    
        return render_template("resultados.html",nombresContaminantes=nombresContaminantes,diaMes=diaMes,barrioHTML=barrioHTML,ubicacionEstacion=ubicacionEstacion)

if __name__=='__main__':
    app.run(debug=True)









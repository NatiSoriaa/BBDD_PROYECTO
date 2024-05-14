import pymongo
from pymongo import MongoClient
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates')


def iniciarMongoDB():
    url = 'mongodb+srv://natgsarabia:Fsu6t4y5jUfhYQxI@contaminacionbcn.xbosddo.mongodb.net/'

    myClient = pymongo.MongoClient(url)

    myDB = myClient['contaminacionBCN']
    return myDB


#1  FUNCIÓN EXTRAER NOMBRES BARRIOS
def encontrarBarrios(myDB):
    collection=myDB['Estaciones']
    listaBarrios=collection.distinct('Nom_barri')
    return listaBarrios

#2  FUNCIÓN EXTRAER UBICACION ESTACIONES
def informacionEstacion(myDB,barrio): 
    collection=myDB['Estaciones']
    query={'Codi_barri': barrio}

    informacionEstacion=[]
  
    iter=collection.find(query,{'_id':0, 'nom_cabina':1,'ubicacio':1})
    i=0
    for doc in iter:
        doc=dict(doc)
        valoresDoc=doc.items()
        listaDatos=list(valoresDoc)
        informacionEstacion.insert(i,listaDatos[0][1],listaDatos[1][1])
        i+=1

    
    return informacionEstacion


#3 FUNCIÓN BUSQUEDA RESULTADO
def find(myDB,codigoEstacion, diaMes):
    collection=myDB['CalidadAire']
    query={'ESTACIO': codigoEstacion, 'DIA':diaMes}
  
    codigosContaminantesActivos=[]
    
    iter=collection.find(query,{'_id':0,'CODI_CONTAMINANT':1,'H12':1})
    i=0
    for doc in iter:
        doc=dict(doc)
        valoresDoc=doc.items()
        listaDatos=list(valoresDoc)
        codigosContaminantesActivos.insert(i,(listaDatos[0][1],listaDatos[1][1]))
        i+=1

    return codigosContaminantesActivos 

#4 ENCONTRAR NOMBRE BARRIO
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


#5 FUNCIÓN BUSQUEDA CONTAMINANTES 
def buscarContaminantes(myDB,listaContaminantes):
    nombresContamimantes=[]
    collection=myDB['Contaminantes']

    i=0
    for contaminante in listaContaminantes:
        query={'Codi_Contaminant': contaminante}
        iter=collection.find(query,{'_id':0,'Desc_Contaminant':1,'Unitats':1})
        for item in iter:
            contaminantes=dict(item)
            nombreContamimante=contaminantes.items()
            listaNombrescontaminantes=list(nombreContamimante)
            print(listaContaminantes[i])
            nombresContamimantes.insert(i,(listaNombrescontaminantes[0][1],listaNombrescontaminantes[1][1]))
            i+=1     
            
    return(nombresContamimantes)

# COMPROBACION FUNCIONES:


myDB=iniciarMongoDB()


#1 FUNCIÓN EXTRAER NOMBRES BARRIOS
barrios=encontrarBarrios(myDB)
print(barrios)
##################################################    OK


#4 ENCONTRAR CODIGO BARRIO
codigoBarrio=checkCodigoBarrio("Sant Pere, Santa Caterina i la Ribera")
print(codigoBarrio)
##################################################     OK  


#2  FUNCIÓN EXTRAER UBICACION ESTACIONES
informacionEstacion(myDB,codigoBarrio)
print(informacionEstacion)
##################################################  FALLO


#3 FUNCIÓN BUSQUEDA RESULTADO

diaMes=7
codigosContaminantes=find(myDB, codigoBarrio, diaMes)
print(codigosContaminantes)

##################################################       OK

#5 FUNCIÓN BUSQUEDA CONTAMINANTES 
# informacionContaminantes=buscarContaminantes(myDB,codigosContaminantes)
# print(informacionContaminantes)



# @app.route('/paginaInicio', methods=["GET","POST"])

# def index():
#     myDB=iniciarMongoDB()
#     if request.method=="GET":
#         listaBarrios=encontrarBarrios(myDB)
#         print(listaBarrios)
#         print("___________________________________")
#         return render_template("paginaInicio.html",listaBarrios=listaBarrios)

#     elif request.method=="POST":
#         barrioHTML=request.form.get("barrioHTML")
#         barrio=checkCodigoBarrio(barrioHTML)
#         print('Nombre barrio '+barrioHTML+"     Codigo: "+str(barrio))
#         print("___________________________________")

#         diaMes=request.form.get("diaHTML")
#         print('Dia mes escogido: '+str(diaMes))
#         print("___________________________________")

#         codigosContaminantes=find(myDB, int(barrio), int(diaMes))
#         print(codigosContaminantes)
#         # for item in codigosContaminantes:
#         #     print('Codigos contaminante y cantidad: '+item[0])
#         # print("___________________________________")

#         nombresContaminantes=buscarContaminantes(myDB,codigosContaminantes)
#         print(nombresContaminantes)

#         ubicacionEstacion=informacionEstacion(myDB,barrio)
#         print(ubicacionEstacion)
        
    
#         return render_template("resultados.html",nombresContaminantes=nombresContaminantes,diaMes=diaMes,barrioHTML=barrioHTML,ubicacionEstacion=ubicacionEstacion)

# if __name__=='__main__':
#     app.run(debug=True)









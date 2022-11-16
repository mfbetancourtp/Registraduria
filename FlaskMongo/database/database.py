from pymongo import MongoClient
import json
import certifi


ca = certifi.where()

######
##Carga el archivo de configuracion 
######

def loadConfigFile():
    with open('database/config.json') as f:
        data= json.load(f)
        return data


#####
##Funcion de conexion 
#####c


######################################
#       Función de conexión          #
######################################
def dbConnection():
    dataConfig = loadConfigFile()
    try:
            #conexión atlas
            client = MongoClient(dataConfig['MONGO_URI_SERVER'], tlsCAFile = ca)
            #Conexión local
           # client = MongoClient(dataConfig['MONGO_URI_LOCAL'], dataConfig['LOCAL_PORT'])
            db = client["ciclo4_votaciones_domingo"]
    except ConnectionError:
            print("Error de conexión con la db")
    return db
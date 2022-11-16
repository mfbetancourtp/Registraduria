from pymongo import MongoClient
import json
import certifi


ca = certifi.where()

######
##Carga el archivo de configuracion 
######

def loadConfigFile():
    with open('database/config.jeson') as f:
        data= json.load(f)
        return data


#####
##Funcion de conexion 
#####

def dbconnecion():
    dataconfig= loadConfigFile()
    try:    
        ##Conexion atlas
        client = MongoClient(dataconfig['MONGO_URI_SERVER'], tlsCAFile= ca)
        ##Conexion local 
       # client = MongoClient(dataconfig['MONGO_URI_LOCAL'], dataconfig['LOCAL_PORT'])
        db = client["Cliclo4_Votaciones_domingo"]

    except ConnectionError:
        print("Error de conexion con la db")
        return db


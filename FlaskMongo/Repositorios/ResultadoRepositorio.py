from Repositorios.InterfazRepositorio import InterfazRerpositorio
from Modelos.Resultado import Resultado
from bson import ObjectId

class ReultadoRepositorio(InterfazRerpositorio[Resultado]):
    
    def getListadoCandidatosInscritosMesa(self,id_mesa):
        theQuery = {"mesa.$id":ObjectId(id_mesa)}
        return self.query(theQuery)

    def getListadoMesasCandidatoInscrito(self,id_candidato):
        theQuery = {"candidato.$id": ObjectId(id_candidato)}
        return self.query(theQuery)

    def getNumeroCedulaMayorCandidato(self):
        query={
                "$group":{
                        "_id":"$candidato",
                        "max":{
                            "$max": "$cedula"
                        },
                        "doc":{
                            "$first": "$$ROOT"
                        }
                    }
                }
        pipeline = [query]
        return  self.queryAggregation(pipeline)

  

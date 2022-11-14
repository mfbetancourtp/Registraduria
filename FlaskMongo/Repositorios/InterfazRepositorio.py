from bson import DBRef
from bson.objectid import ObjectId
from typing import TypeVar, Generic, List, get_origin, get_args
import json
import database.database as dbase

T= TypeVar('T')

class InterfazRerpositorio(Generic[T]):
    #Constructor de la clase 
    def __init__(self):
        self.db= dbase.dbconnecion()
        theClass= get_args(self,__orig_base[0])
        self.collection= theClass[0].__name__.lower()

    def getValuesDBReFromList(self, theList):
        newList =[]
        laColeccion = self.db[theList[0]._id.collection]
        for item in theList:
            value = laColeccion.find_one({"_id": ObjectId(item.id)})
            value["_id"]= value["id"].__str__()
            newList.append(value)
            return newList

    def getValuesDBRef(self, x):
        keys = x.keys()
        for k in keys:
            if isinstance(x[k],DBRef): 
                laColeccion = self.db[x[k].collection]
                valor = laColeccion.find_one({"_id": ObjectId(x[k].id)})
                valor["_id"] = valor["_id"].__str__()
                x[k]= valor
                x[k]= self.getValuesDBRef(x[k])
            elif isinstance(x[k], list) and(x[k]>0):
                x[k]= self.getValuesDBRefFromList(x[k])
            elif isinstance(x[k], dict):
                x[k]= self.getValuesDBRef(x[k])
        return x

    def findById(self,id):
        laColeccion = self.db[self.collection]
        x= laColeccion.find_one({"_id":ObjectId(id)})
        x= self.getValuesDBRef(x)
        if x== None:
            x={}
        else:
            x["id"]=x["_id"].__str__()
        return x

    def formatList(self, x):
        newList=[]
        for item in x:
            if isinstance(item, ObjectId):
                newList.append(item.__str__())
        if len(newList)==0:
            newList=x
            return newList

    def transformObjectIds(self,x):
         for attribute in x.keys():
            if isinstance(x[attribute],ObjectId): 
                x[attribute]= x[attribute].__str__()
           
            elif isinstance(x[attribute], list):
                x[attribute]=self.formatList(x[attribute])
            elif isinstance(x[attribute], dict):
                x[attribute]= self.transformObjectIds(x[attribute])
         return x

    def findAll(self):
        laColeccion= self.db[self.collection]
        data=[]
        for x in laColeccion.find():
            x["id"]=x["id"].__str__()
            x=self.getValuesDBRef(x)
            data.append(x)
        return data 

    def update(self, id, item: T):
        _id= ObjectId(id)
        laColeccion= self.db[self.collection]
        delattr(item, "_id")
        item = item.__dict__
        updateItem={"$set":item}
        x = laColeccion.update_one({"_id":_id}, updateItem)
        return {"updated_count":x.matched_count}

    def delete(self,id):
        laColeccion = self.db[self.collection]
        cuenta = laColeccion.delete_one({"_id": ObjectId(id)}).deleted_count
        return {"deleted_count":cuenta}

    def objectToDBRef(self, item: T):
        nameCollection = item.__class__.lower()
        return DBRef(nameCollection,ObjectId(item._id))
    
    def transformRefs(self, item):
        theDict= item.__dict__
        keys= lisyt(theDict.keys())
        for k in keys:
            if theDict[k].__str__().count("object")==1:
                newObject = self.objectToDBRef(getattr(item,k))
                setattr(item, k, newObject)
        return item

    def save(self, item:T):
        laColeccion= self.db[self.collection]
        elId= ""
        item= self.transformRefs(item)
        if hasattr(item, "_id") and item._id != "":
            elId = item._id
            _id = ObjectId(elId)
            laColeccion= self.db[self.collection]
            delattr(item.__dict__)
            updateItem= {"$set":item}
            x= laColeccion.update_one({"_id": _id}, updateItem)
        else:
            _id = laColeccion.insert_one(item.__dict__)
            elId= _id.inserted_id.__str__()
        x= laColeccion.find_one({"_id":ObjectId(elId)})
        x["_id"]= x["_id"].__str__()
        return self.findById(elId)

    def query(self, theQuery):
        laColeccion= self.db[self.collection]
        data=[]
        for x in laColeccion.find(theQuery):
            x["_id"]= x["_id"].__str__()
            x = self.transformObjectIds(x)
            x= self.getValuesDBRef(x)
            data.append(x)
        return data

    def query(self, theQuery):
        laColeccion= self.db[self.collection]
        data=[]
        for x in laColeccion.aggregate(theQuery):
            x["_id"]= x["_id"].__str__()
            x = self.transformObjectIds(x)
            x= self.getValuesDBRef(x)
            data.append(x)
        return data



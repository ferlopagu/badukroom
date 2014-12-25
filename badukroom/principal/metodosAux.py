
'''
Created on 25/12/2014

@author: fla2727
'''
import os
import re

"""METODO PARA AVERIGUAR PATH DE CADA FICHERO """
def pathFile(path): #example--> path="Correos",    dir="Correos/"
    ficheros=[]
    pathFile=""
    for e in os.listdir(path):
        if re.match(".*.sgf", e):
            pathFile=path+"/"+e
            #print pathFile
            ficheros.append(pathFile)
    for e in ficheros:
        print e
    return ficheros

#pathFile("sgf")

def recorrer_sgfs():
    lista_diccionarios_res=[]
    dict_game={}
    ficheros = pathFile("sgf")
    for path in ficheros:
        #print path
        contador=0
        """ LEEMOS EL FICHERO"""
        fileobj = open(path, "rb")
        lines = fileobj.readlines()
        fileobj.close()
        pw=""
        pb=""
        date=""
        result=""
        """Recorremos las lineas para rellenar la informacion de cada partida"""
        for line in lines:
            #print line
            if pw=="" or pw==None:
                mo = re.search("PW\[(\w*[\s]?\w)\]", line)
                if mo:
                    for e in mo.groups():
                        pw=e
                #print "pw: "+str(pw)+"\n"+line
            if pb=="" or pb==None:
                #mo = re.search("PB\[(\w*)\]", line)
                mo = re.search("PB\[(\w*[\s]?\w)\]", line)
                if mo:
                    for e in mo.groups():
                        pb=e
            if date=="" or date==None:
                mo = re.search("DT\[(\d+-\d+-\d+)]", line)
                if mo:
                    for e in mo.groups():
                        date=e
            if result=="" or result==None:
                mo = re.search("RE\[(\w\+.*)\]", line)
                if mo:
                    for e in mo.groups():
                        result=e
        dict_game={}
        dict_game["blanco"]=pw
        dict_game["black"]=pb
        dict_game["fecha"]=date
        dict_game["result"]=result
        dict_game["path"]=path
        lista_diccionarios_res.append(dict_game)
    for e in lista_diccionarios_res:
        print e
     
recorrer_sgfs()

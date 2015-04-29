
'''
Created on 25/12/2014
datetime.date.today()

@author: fla2727
'''
import os
import re
from principal.models import Jugador, Partida
#from login.models import Perfil
import datetime
from datetime import date
import time
import locale
from django.conf.urls import url
from redsocial.models import Grupo
from django.shortcuts import get_object_or_404
from login.models import Perfil
from django.contrib.auth.models import User
from django.db.models import Q
from badukroom.settings import BASE_DIR
from django.core.files import File

import django
django.setup()

#from datetime import datetime
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


#pathFile("../static/sgf")
def recorrer_sgfs():
    lista_diccionarios_res=[]
    dict_game={}
    #ficheros = pathFile("../static/sgf")
    ficheros=pathFile("../principal/gokifu.com")
    #ficheros=pathFile("../gokifu.com")
    for path in ficheros:
        #print path
        #nombre_fichero=path
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
                mo = re.search("PW\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        pw=e
                #print "pw: "+str(pw)+"\n"+line
            if pb=="" or pb==None:
                #mo = re.search("PB\[(\w*)\]", line)
                mo = re.search("PB\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        pb=e
            if date=="" or date==None:
                mo = re.search("DT\[(\d+-\d+-\d+)]", line)
                if mo:
                    for e in mo.groups():
                        date=e
            if result=="" or result==None:
                #mo = re.search("RE\[(\w\+.*)\]", line)
                mo = re.search("RE\[(\w*\+\w*\W?\w*?)\]", line)
                if mo:
                    for e in mo.groups():
                        result=e
        dict_game={}
        dict_game["blanco"]=pw
        dict_game["black"]=pb
        dict_game["fecha"]=date
        dict_game["result"]=result
        dict_game["path"]=path
        
        """Creamos los jugadores y la Partida"""
        #path_fichero=BASE_DIR+"/static/sgf/"+path
        #print path_fichero
        jugador_negro, created = Jugador.objects.get_or_create(nombre=dict_game['black'])
        print jugador_negro.__unicode__()
        #jugador_negro=Jugador()
        #jugador_negro.save()
        print 'jugador negro guardado con exito'
        #jugador_blanco=Jugador(nombre=dict_game['blanco'])
        jugador_blanco, created = Jugador.objects.get_or_create(nombre=dict_game['blanco'])
        #jugador_blanco.save()
        
        cadenas=path.split("/")
        nombre_fichero=cadenas[len(cadenas)-1]
        path_fichero="sgf/"+nombre_fichero
        print "Path fichero"+path_fichero
        
        partida = Partida(fecha=dict_game['fecha'], jugador_negro=jugador_negro, jugador_blanco=jugador_blanco, resultado=dict_game['result'], fichero=File(open(path, 'r')), path=path_fichero)
        partida.save()
        """ Fin crear Partida """
        
        lista_diccionarios_res.append(dict_game)
    for e in lista_diccionarios_res:
        print e     
#recorrer_sgfs()

profesionales=['Yoshiteru Abe','Akaboshi Intetsu','Jiro Akiyama','Nobuo Amayake','Akio Ando','Takeo Ando','Toshiyuki Ando','Nobuaki Anzai','Kaori Aoba','Kikuyo Aoki','Shinichi Aoki','Takeshi Aragaki','Shuzo Awaji','Shigeru Baba','Kaori Chinen','Hideyuki Fujisawa','Hosai Fujisawa','Susumu Fukui','Go Seigen','Dogen Handa','Naoki Hane','Yasumasa Hane','Shoji Hashimoto','Utaro Hashimoto','Naoto Hikosaka','Hirose Heijiro','Kunihisa Honda','Honinbo Chihaku','Honinbo Doetsu','Honinbo Shuhaku','Honinbo Shusai','Honinbo Dochi','Honinbo Dosaku','Honinbo Doteki',
       'Honinbo Genjo','Honinbo Hakugen','Honinbo Jowa','Honinbo Retsugen','Honinbo Sansa','Honinbo Satsugen','Honinbo Shuei','Honinbo Shuetsu','Honinbo Shugen','Honinbo Shuho','Honinbo Shusaku','Honinbo Shuwa','Masaki Hoshino''Inoue Genan Inseki','Akira Ishida','Yoshio Ishida','Kunio Ishii','Kaoru Iwamoto','Tatsuaki Iwata','Yuta Iyama','Honinbo Josaku','Toshiro Kageyama','Takeo Kajiwara','Masaaki Kanagawa','Karigane Junichi','Satoshi Kataoka','Atsushi Kato','Masao Kato','Shin Kato','Kazumi Akedo','Yasuro Kikuchi','Minoru Kitani','Tetsuya Kiyonari',
       'Ko Iso','Ko Reibun','Izumi Kobayashi','Koichi Kobayashi','Satoru Kobayashi','Hideki Komatsu','Rin Kono','Yasuo Koyama','Katsukiyo Kubomatsu','Shuchi Kubouchi','Norio Kudo','Nobuaki Maeda','Kana Mannami','Takehisa Matsumoto','Hideki Matsuoka','Tomoyasu Mimura','Naoki Miyamoto','Hidehiro Miyashita','Goro Miyazawa','Tomochika Mizokami','Yoshika Mizuno','Michihiro Morita','Daisuke Murakawa','Nakamura Doseki','Shinya Nakamura','Yusuke Oeda','Masaki Ogata','Shuzo Ohira','Yumiko Okada','Chiyotaro Onoda','Ota Yuzo','Hideo Otake','Hideyuki Sakai',
       'Toshio Sakai','Eio Sakata','Honinbo Sanetsu','Sunao Sato','Kensaku Segoe','Riichi Sekiyama','Taiki Seto','Toshihiro Shimamura','So Yokoku','Masao Sugiuchi','Keizo Suzuki','Tamejiro Suzuki','Dohei Takabe','Kaku Takagawa','Shinji Takao','Masaki Takemiya','Hiroaki Tono','Masamitsu Tsuchida','Atsushi Tsuruyama','Tsuzuki Yoneko','Shuhei Uchida','Yoshio Ueki','Toshiro Yamabe','Kimio Yamada','Takuji Yamada','Hiroshi Yamashiro','Keigo Yamashita','Katsunori Yanaka','Yasui Sanchi','Hajime Yasunaga','Norimoto Yoda','Shigeaki Yokota','Yukari Yoshihara','Satoshi Yuki',]
def guardar_profesionales(lista):
    for e in lista:
        jugador = Jugador(nombre=e)
        jugador.save()
    print "Jugadores deberian haber sido guardados"
        
#guardar_profesionales(profesionales)
""" Ejecutar en shell with Django enviroment
introducir primero 
import django
django.setup()
from login.models import Perfil
cadena="Pris"
lista_perfiles=Perfil.objects.filter(user__username__iregex=cadena) #cambiar username por el campo que queramos filtrar con la expresion regular por ejemplo first name
print lista_perfiles

Perfil.objects.values('user').filter(Q(user__first_name__regex=cadena) | Q(user__last_name__regex=cadena))
"""
def buscador():
    cadena=raw_input("Introduce un nombre: ")
    print cadena
    #antes usaba iregex
    if cadena!="":
        lista_perfiles=list(Perfil.objects.values('user__first_name', 'user__last_name', 'user__username').filter(Q(user__first_name__regex=cadena) | Q(user__last_name__regex=cadena))) #cambiar username por first_name o last_name
        print lista_perfiles
        #for p in lista_perfiles:
            #lista_user=list(User.objects.values('first_name', 'last_name', 'username').filter(id=p['user']))
        #print lista_user
    else:
        print "La cadena es ''"
def informacion_partida(path):
#fichero = pathFile("../static/sgf")
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
            mo = re.search("PW\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    pw=e
            #print "pw: "+str(pw)+"\n"+line
        if pb=="" or pb==None:
            #mo = re.search("PB\[(\w*)\]", line)
            mo = re.search("PB\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    pb=e
        if date=="" or date==None:
            mo = re.search("DT\[(\d+-\d+-\d+)]", line)
            if mo:
                for e in mo.groups():
                    date=e
        if result=="" or result==None:
            #mo = re.search("RE\[(\w\+.*)\]", line)
            mo = re.search("RE\[(\w*\+\w*\W?\w*?)\]", line)
            if mo:
                for e in mo.groups():
                    result=e
    dict_game={}
    dict_game["blanco"]=pw
    dict_game["black"]=pb
    dict_game["fecha"]=date
    dict_game["result"]=result
    dict_game["path"]=path
    print dict_game
    return dict_game

def informacion_partida2(lineas, path):
    """Recorremos las lineas para rellenar la informacion de cada partida"""
    pw=""
    rw=""
    pb=""
    rb=""
    date=""
    result=""
    for line in lineas:
        #print line
        if pw=="" or pw==None:
            mo = re.search("PW\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    pw=e
            #print "pw: "+str(pw)+"\n"+line
        if rw=="" or rw==None:
            mo = re.search("WR\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    rw=e
        if pb=="" or pb==None:
            #mo = re.search("PB\[(\w*)\]", line)
            mo = re.search("PB\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    pb=e
        if rb=="" or rb==None:
            mo = re.search("BR\[(\w*\s?\w*)\]", line)
            if mo:
                for e in mo.groups():
                    rb=e
        if date=="" or date==None:
            mo = re.search("DT\[(\d+-\d+-\d+)]", line)
            if mo:
                for e in mo.groups():
                    date=e
        if result=="" or result==None:
            #mo = re.search("RE\[(\w\+.*)\]", line)
            mo = re.search("RE\[(\w*\+\w*\W?\w*?)\]", line)
            if mo:
                for e in mo.groups():
                    result=e
    dict_game={}
    dict_game["blanco"]=pw
    dict_game["rango_blanco"]=rw
    dict_game["black"]=pb
    dict_game["rango_negro"]=rb
    dict_game["fecha"]=date
    dict_game["result"]=result
    dict_game["path"]=path
    print dict_game
    return dict_game


#informacion_partida("../static/sgf/gresko-ersev.sgf")
#informacion_partida('../static/sgf/wilwal6re-ersev2.sgf')


#print datetime.date.today( )
#print datetime.datetime.now()

def fue_comentado(fecha):
    locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
    #diccionario_meses={"01":"enero", "02":"febrero", "03":"marzo", "04":"abril", "05":"mayo", "06":"junio", "07":"julio", "08":"agosto","09":"septiembre", "10":"octubre", "11":"noviembre", "12":"diciembre"}
    res=""
    ahora= datetime.datetime.now()
    ahora_cadena=datetime.datetime.now().strftime("%d de %B a la(s) %H:%M")
    diferencia= ahora -fecha
    #creamos tupla (horas, segundos)
    tupla=divmod(diferencia.total_seconds(), 3600)
    #comprobamos que el numero de horas es mayor que 24
    if tupla[0] > 24:
        res=ahora_cadena
    else:
        if tupla[0]>=0:
            res= "hace "+str(int(tupla[0]))+" hora(s)"
        else:
            #al ser igual que cero, tupla[1] almacena los segundos que dividido entre 60 nos devuelve los minutos y segundos restantes
            minutos_segundos=divmod(tupla[1], 60)
            if minutos_segundos[0]>0:
                res = "hace "+str(int(minutos_segundos[0]))+ " minutos"
            else: 
                res= "hace "+str(int(minutos_segundos[1]))+ "segundos"
    print "RES: "+res
    return res
            #almacena
        
        #tupla=divmod(tupla[0], )

#fecha=datetime.datetime(2015, 2, 8, 21, 57, 42)
#fue_comentado(fecha)

#locale.setlocale(locale.LC_TIME, "es_ES.UTF-8") 
#diccionario_meses={"01":"enero", "02":"febrero", "03":"marzo", "04":"abril", "05":"mayo", "06":"junio", "07":"julio", "08":"agosto"
#                    ,"09":"septiembre", "10":"octubre", "11":"noviembre", "12":"diciembre"}
#print datetime.datetime.now().strftime("%d de %B a la(s) %H:%M")
#print datetime.datetime.now().strftime("%m")
ahora = datetime.datetime.now().strftime("%y-%m-%d-%H:%M:%S")
#print "ahora: "+str(ahora)
dia1= datetime.datetime(2015, 2, 8, 18, 17, 42)
dia2= datetime.datetime(2015, 2, 8, 18, 57, 42)
elapsedTime = dia2 - dia1
#print divmod(elapsedTime.total_seconds(), 86400)
#print divmod(elapsedTime.total_seconds(), 3600)
#print divmod(elapsedTime.total_seconds(), 60)
#tupla=divmod(elapsedTime.total_seconds(), 3600)
#print tupla[0]
#print tupla[1]
#print dia1
#print dia2
#segundos_ahora=datetime.datetime.now().strftime("%s")
#meses_ahora=datetime.datetime.now().strftime("%s")
#print "fecha en meses: "+str(meses_ahora)
#segundos_dia1= dia1.strftime("%s")
#segundos_dia= dia2.strftime("%s")
#print "Diferencia: "+str(int(segundos_dia) - int(segundos_dia1))
#print dia2.strftime("%s")
#print "dia: "+str(dia2)

#print "RES: "+str(  int(segundos_ahora)- int(segundos_dia)  )
#ayer = hoy - datetime.timedelta(hours=1)
#res= hoy-dia2
"""
print res
print "el comentario se realizo hace "+str(res)


print "Time in seconds since the epoch: %s" %time.time()
print "Current date and time: " , datetime.datetime.now()
print "Or like this: " ,datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
print "Current year: ", datetime.date.today().strftime("%Y")
print "Month of year: ", datetime.date.today().strftime("%B")
print "Week number of the year: ", datetime.date.today().strftime("%W")
print "Weekday of the week: ", datetime.date.today().strftime("%w")
print "Day of year: ", datetime.date.today().strftime("%j")
print "Day of the month : ", datetime.date.today().strftime("%d")
print "Day of week: ", datetime.date.today().strftime("%A")
"""


#/redsocial/grupo/1/
"""
def estamos_en_grupo1(url):
    print url
    res_url=[]
    print res_url
    mo = re.search("/redsocial/grupo/(.+)", url)
    if mo:
        res_url.append(True)
        res_url.append(mo.group(1))
    else:
        res_url.append(False)
    #print res_url
    return res_url

#estamos_en_grupo("/redsocial/grupo/1")

def devuelve_grupo(g_id):
    g = get_object_or_404(Grupo, pk=g_id)
    #int g.__unicode__()
    return g
#devuelve_grupo(1)

def devuelve_grupo2(url):
    g_id=int(estamos_en_grupo1(url))
    g=devuelve_grupo(g_id)
    #print g
    return g
"""
def estamos_en_grupo(url):
    mo = re.search("/redsocial/grupo/(.+)/", url)
    resultado=[]
    if mo:
        g_id=int(mo.group(1))
        g = get_object_or_404(Grupo, pk=g_id)
        resultado.append(True)
        resultado.append(g)
        print resultado[0]
        print resultado[1]
    else:
        resultado.append(False)
        print resultado[0]
    return resultado
        
#estamos_en_grupo("/redsocial/grupo/1/")
#estamos_en_grupo("/redsocial/fla2727/")



#names_urls = zip(names, urls)

#for name, url in names_urls:
def descarga_sgf():
    url="http://gokifu.com/es/?p=2"
    print('Downloading %s' % url)
    #wget -A pdf,jpg -m -p -E -k -K -np http://site/path/
    os.system('wget -A sgf,SGF -r -l 1  %s' % url)
#descarga_sgf()

#recibimos una cadena 'dd/mm/yyyy' retorna 'yyyy-mm-dd'
def formatoFecha(cadena):
    array=cadena.split("/")
    fecha=array[2]+"-"+array[1]+"-"+array[0]
    return fecha

def recorrer_sgfs_gokifu():
    lista_diccionarios_res=[]
    dict_game={}
    #ficheros = pathFile("../static/sgf")
    ficheros=pathFile("../principal/gokifu.com")
    #ficheros=pathFile("../gokifu.com")
    for path in ficheros:
        #print path
        #nombre_fichero=path
        #print path
        contador=0
        """ LEEMOS EL FICHERO"""
        fileobj = open(path, "rb")
        lines = fileobj.readlines()
        fileobj.close()
        pw=""
        rw=""
        pb=""
        rb=""
        date=""
        result=""
        """Recorremos las lineas para rellenar la informacion de cada partida"""
        for line in lines:
            #print line
            if pw=="" or pw==None:
                mo = re.search("PW\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        pw=e
                #print "pw: "+str(pw)+"\n"+line
            if rw=="" or rw==None:
                mo = re.search("WR\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        rw=e
            if pb=="" or pb==None:
                #mo = re.search("PB\[(\w*)\]", line)
                mo = re.search("PB\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        pb=e
            if rb=="" or rb==None:
                mo = re.search("BR\[(\w*\s?\w*)\]", line)
                if mo:
                    for e in mo.groups():
                        rb=e
            if date=="" or date==None:
                mo = re.search("DT\[(\d+-\d+-\d+)]", line)
                if mo:
                    for e in mo.groups():
                        date=e
            if result=="" or result==None:
                #mo = re.search("RE\[(\w\+.*)\]", line)
                mo = re.search("RE\[(\w*\+\w*\W?\w*?)\]", line)
                if mo:
                    for e in mo.groups():
                        result=e
        dict_game={}
        dict_game["blanco"]=pw
        dict_game["rango_blanco"]=rw
        dict_game["black"]=pb
        dict_game["rango_negro"]=rb
        dict_game["fecha"]=date
        dict_game["result"]=result
        dict_game["path"]=path
        
        """Creamos los jugadores y la Partida"""
        #path_fichero=BASE_DIR+"/static/sgf/"+path
        #print path_fichero
        jugador_negro, created = Jugador.objects.get_or_create(nombre=dict_game['black'])
        print jugador_negro.__unicode__()
        #jugador_negro=Jugador()
        #jugador_negro.save()
        print 'jugador negro guardado con exito'
        #jugador_blanco=Jugador(nombre=dict_game['blanco'])
        jugador_blanco, created = Jugador.objects.get_or_create(nombre=dict_game['blanco'])
        #jugador_blanco.save()
        
        cadenas=path.split("/")
        nombre_fichero=cadenas[len(cadenas)-1]
        path_fichero="sgf/"+nombre_fichero
        print "Path fichero"+path_fichero
        
        partida = Partida(fecha=dict_game['fecha'], jugador_negro=jugador_negro, rango_negro=dict_game['rango_negro'], jugador_blanco=jugador_blanco, rango_blanco=dict_game['rango_blanco'], resultado=dict_game['result'], fichero=File(open(path, 'r')))
        partida.save()
        """ Fin crear Partida """
        
        lista_diccionarios_res.append(dict_game)
    for e in lista_diccionarios_res:
        print e     
#recorrer_sgfs_gokifu()

    
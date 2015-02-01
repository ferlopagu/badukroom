
'''
Created on 25/12/2014

@author: fla2727
'''
import os
import re
from principal.models import Jugador
from login.models import Perfil

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
    ficheros = pathFile("../static/sgf")
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
"""

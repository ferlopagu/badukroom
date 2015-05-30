'''
Created on 4/3/2015

@author: fla2727
'''
from login.models import Perfil
from principal.models import Jugador
from django.db.models import Q


def sim_distance(prefs, person1, person2):
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    if len(si)==0: return 0
    
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                        for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squares)

""" Recomendar perfiles segun los gustos en comun """
def perfiles_gustos():
    dic_gustos={}
    for p in Perfil.objects.all():
        dic_jugadores={}
        for j in p.jugadores_favoritos.all():
            dic_jugadores[j]=1.0
        dic_gustos[p]=dic_jugadores
    return dic_gustos

def similitud_gustos(dic_gustos, person1, person2): #funciona pero en funcion de los distintos parece que el maximo alcanzable es en funcion de cuantos tengan diferentes salvo que tengan los mismos ambos. Usamos la distancia euclidea
    si={}
    for j in Jugador.objects.all(): #el siguiente bucle add los jugadores que no tienen en comun entre ambos usuarios para hacer la comparacion entre ellos
        if j in dic_gustos[person1]:
            if j in dic_gustos[person2]:
                si[j]=1.0
            else:
                dic_gustos[person2][j]=0.0
        else:
            if j in dic_gustos[person2]:
                dic_gustos[person1][j]=0.0
    if len(si)==0:
        return 0
    sum_of_squares=sum([pow(dic_gustos[person1][item]-dic_gustos[person2][item],2)
                        for item in dic_gustos[person1] if item in dic_gustos[person2]])
    return 1/(1+sum_of_squares)

def topMatches_gustos(diccionario_gustos, person, n=4, similarity=similitud_gustos):
    scores=[(similarity(diccionario_gustos, person, other), other) for other in diccionario_gustos if other != person and other not in person.amigos.all()] #and other not in person.amigos.all()
    scores.sort()
    scores.reverse()
    return scores[0:n] 

""" Fin recomendar perfiles segun los gustos en comun """

""" Recomendar jugadores basado en los gustos en comun """ 
def getRecommendations_jugadores(person, dic_gustos , similarity=similitud_gustos): #ESTE METODO AL FINAL NO LO ESTAMOS USANDO EN LA WEB
    totals={}
    simSums={}
    for other in dic_gustos:
        #don't compare me to myself
        if other==person: continue
        sim=similarity(dic_gustos, person, other)
        #ignore scores of zero or lower
        if sim<=0: continue
        for item in dic_gustos[other]:
            #only score players i don't like yet:
            if item not in dic_gustos[person] or dic_gustos[person][item]==0.0:
                #similarity * score
                totals.setdefault(item,0)
                totals[item]+=dic_gustos[other][item]*sim
                #Sum of similarities
                simSums.setdefault(item,0)
                simSums[item]+=sim
    #Create the normalized list
    rankings=[(total/simSums[item],item) for item, total in totals.items()]
    #return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings
""" Fin recomendar jugadores basado en los gustos en comun"""


""" Recomendar perfiles segun amigos en comun """    
def perfiles_amigos():
    diccionario_amigos={}
    for p in Perfil.objects.all(): 
        diccionario_amigos[p]=list(p.amigos.all())
    return diccionario_amigos

def similitud_amigos_comun_2(diccionario_amigos, person1, person2):
    contador=0
    for p in diccionario_amigos[person1]:
        if p in diccionario_amigos[person2]:
            contador+=1
    return contador

def topMatches_amigos_comun(diccionario_amigos, person, n=4, similarity=similitud_amigos_comun_2):
    scores=[(similarity(diccionario_amigos, person, other), other) for other in diccionario_amigos if other != person and other not in diccionario_amigos[person]] #Quizas Comprobar que no existe other en los amigos de person Menos Probable probar primero modificar diccionario
    scores.sort()
    scores.reverse()
    return scores[0:n] #Con esto podriamos recomendar personas con mayor similitud contigo en los ghustos por los jugadores
""" Fin recomendar perfiles segun amigos en comun """

if __name__ == '__main__':
    #""" PRUEBAS BASE DE DATOS
    import django
    django.setup()
    perfil1=Perfil.objects.get(user__username='priscilacb')
    perfil2=Perfil.objects.get(user__username='fran')
    
    dic_gustos=perfiles_gustos()
    diccionario_amigos=perfiles_amigos()

    print "==========DICCIONARIO DE LOS GUSTOS DE JUGADORES PARA CADA PERFIL============\n"
    print dic_gustos
    print "\n===========PERFIL DE ESTUDIO: "+perfil1.user.first_name+" "+perfil1.user.last_name+" ==============="
    #print "\n=========LISTA PONDERADA DE PERFILES RECOMENDADOS POR GUSTOS EN COMUN========="
    print topMatches_gustos(dic_gustos, perfil1)
    print topMatches_amigos_comun(diccionario_amigos, perfil1)
    #print "===========RESULTADOS DE LA PONDERACION DE LOS GUSTOS============="
    #print(getRecommendations_jugadores(perfil1, dic_gustos))
    print "\n===========PERFIL DE ESTUDIO: "+perfil2.user.first_name+" "+perfil2.user.last_name+" ==============="
    #print "\n=========LISTA PONDERADA DE PERFILES RECOMENDADOS POR GUSTOS EN COMUN========="
    print topMatches_gustos(dic_gustos, perfil2)
    print topMatches_amigos_comun(diccionario_amigos, perfil2)
    #print "\n===========RESULTADOS DE LA PONDERACION DE LOS GUSTOS============="
    #print(getRecommendations_jugadores(perfil2, dic_gustos))
    
    #print "\n==========DICCIONARIO DE LOS AMIGOS PARA CADA PERFIL============\n"
    #print diccionario_amigos
    #print "===========PERFIL DE ESTUDIO: "+perfil1.user.first_name+" "+perfil1.user.last_name+" ==============="
    #print "=========LISTA PONDERADA DE PERFILES RECOMENDADOS POR AMIGOS EN COMUN=========\n"
    #print topMatches_amigos_comun(diccionario_amigos, perfil1) #Devuelve perfiles con quien tenemos mas amigos en comun
    #print "\n===========PERFIL DE ESTUDIO: "+perfil2.user.first_name+" "+perfil2.user.last_name+" ==============="
    #print "=========LISTA PONDERADA DE PERFILES RECOMENDADOS POR AMIGOS EN COMUN========="
    #print topMatches_amigos_comun(diccionario_amigos, perfil2) #Devuelve perfiles con quien tenemos mas amigos en comun

    """
    print critics
    #print(sim_distance(critics, 'Fla', 'Priscila'))
    similitud(jugadores, critics, 'Fla', 'Priscila')
    print topMatches(critics, 'Antonio')
    print getRecommendations('Priscila')
    
    similitud_amigos_comun(lista_amigos,amigos, 'Fla', 'Antonio')
    print topMatches(amigos, 'Fla',4, similitud_amigos_comun, lista_amigos)
    """
    
    
    """
    diccionario_amigos=perfiles_amigos()
    perfil2=Perfil.objects.get(user__username='lolo')
    print(similitud_amigos_comun_2(diccionario_amigos, perfil1, perfil2))
    lista=topMatches_amigos_comun(diccionario_amigos, perfil1)
    for e in lista:
        print e
    print dic_gustos
    #similitud_gustos(dic_gustos, perfil1, perfil2)
    print topMatches_gustos(dic_gustos, perfil1) #devuelve los perfiles mas afines segun jugadores en comun
    print(getRecommendations_jugadores(perfil1, dic_gustos)) #Nos devuleve Los jugadores recomendados por los perfiles mas afines
    print topMatches_amigos_comun(diccionario_amigos, perfil1) #Devuelve perfiles con quien tenemos mas amigos en comun
    """


""" PRIMERAS VARIABLES PARA PRUEBAS CON LOS METODOS POSTERIORES
critics={'Fla': {'Gu Li':1.0, 'Lee Sedol':1.0, 'Iyama Yuuta':1.0},
         'Priscila':{'Gu Li':1.0, 'Ishida Yoshio':1.0, 'Iyama Yuuta':1.0},
         'Lolo':{'Lee Sedol':1.0, 'Ishida Yoshio':1.0, 'Hane Naoki':1.0},
         'Manu':{'Hane Naoki':1.0, 'Cho Chikun':1.0, 'Ishida Yoshio':1.0, 'Iyama Yuuta':1.0},
         'Antonio':{'Iyama Yuuta':1.0, 'Lee Sedol':1.0, 'Cho Chikun':1.0, 'Gu Li':1.0, 'Go Seigen':1.0}
         }
jugadores=['Gu Li', 'Lee Sedol', 'Iyama Yuuta', 'Ishida Yoshio', 'Hane Naoki', 'Cho Chikun', 'Go Seigen']

amigos={'Fla': {'Priscila':1.0, 'Lolo':1.0, 'Antonio':1.0},
         'Priscila':{'Lolo':1.0, 'Manu':1.0, 'Fla':1.0},
         'Lolo':{'Fla':1.0, 'Priscila':1.0, 'Manu':1.0},
         'Manu':{'Lolo':1.0, 'Priscila':1.0},
         'Antonio':{'Fla':1.0}
        }

lista_amigos={'Fla', 'Priscila', 'Lolo', 'Manu', 'Antonio'}

#<Perfil: fla2727>: {<Jugador: Ida Athushi>: 1.0, <Jugador: Hane Naoki>: 1.0, <Jugador: Lee Youngjoo>: 1.0, <Jugador: Kim Miri>: 1.0}, 
#<Perfil: priscilacb>: {<Jugador: Ida Athushi>: 1.0, <Jugador: Hane Naoki>: 1.0, <Jugador: Choi Jeong>: 1.0}, 
#<Perfil: lolo>: {<Jugador: Oh Jeonga>: 1.0, <Jugador: Hane Naoki>: 1.0, <Jugador: Yamashiro Hiroshi>: 1.0, <Jugador: Lee Youngjoo>: 1.0, <Jugador: Lee Sedol>: 1.0}, 
#<Perfil: manu>: {<Jugador: Lee Taehyun>: 1.0, <Jugador: Park Jungwhan>: 1.0, <Jugador: Lee Youngjoo>: 1.0, <Jugador: Kim Miri>: 1.0}, 
#<Perfil: fran>: {<Jugador: Ida Athushi>: 1.0, <Jugador: Lee Sedol>: 1.0, <Jugador: Jiang Qirun>: 1.0, <Jugador: Zhao Chenyu>: 1.0}

"""

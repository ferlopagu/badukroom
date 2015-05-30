'''
Created on 27/4/2015

@author: fla2727

'''
import random
import string
import datetime
from login.models import Perfil
from redsocial.models import Comentario, Respuesta
from django.contrib.auth.models import User

date = datetime.date(1992,3, 13)  #year, month, day

def cargaComentariosRelleno():
    i=0
    print "=====EMPEZANDO CARGA======"
    while i < 20:
        texto="Comentario "+str(i)+'  '.join(random.choice(string.ascii_lowercase) for x in range(350))
        fecha=datetime.datetime.now()
        #total = Perfil.objects.all().count()
        #id=random.randrange(0,total-1)
        perfil = Perfil.objects.get(user__username='priscilacb')
        comentario = Comentario(fecha=fecha, perfil=perfil, texto=texto)
        comentario.save()
        print comentario.__unicode__()
        j=0
        while j<3:
            perfil2 = Perfil.objects.get(user__username='fla2727')
            texto2="Respuesta a comentario "+str(i)+' - '+str(j)+'   '.join(random.choice(string.ascii_lowercase) for x in range(350))
            respuesta=Respuesta(fecha=fecha, perfil=perfil2, texto=texto2, comentario=comentario)
            respuesta.save()
            j+=1
            print "Respuesta: "+str(j)
        i+=1
    print "=======CARGA FINALIZADA====="

def creaUser(n_username, n_password, n_email, n_first_name, n_last_name):
    user = User.objects.create_user(
    username = n_username,
    password = n_password,
    email = n_email,
    first_name= n_first_name,
    last_name = n_last_name
    )
    user.save()
    return user
    
def creaPerfil(user, rango="18k", ciudad="Sevilla", fecha_nacimiento=date):
    p=Perfil(user=user, rango=rango, ciudad=ciudad, fecha_nacimiento=fecha_nacimiento)
    p.save()
    return p

def addAmigos(perfil, amigos):
    for amigo in amigos:
        perfil.amigos.add(amigo)
        perfil.save()

if __name__ == '__main__':
    import django
    django.setup()
    
    
    a=creaUser("lolo", "lolo", "lolo@hotmail.com", "Lolo", "Amador")
    b=creaUser("fran", "fran", "fran@hotmail.com", "Fran", "Hernandez")
    c=creaUser("campa", "campa", "campa@hotmail.com", "Carlos", "Campanario")
    d=creaUser("maria", "maria", "maria@hotmail.com", "Maria", "Del Campo")
    f=creaUser("libe", "libe", "libe@hotmail.com", "Libertad", "Bordallo")
    g=creaUser("dani", "dani", "dani@hotmail.com", "Dani", "Romero")
    h=creaUser("samu", "samu", "samu@hotmail.com", "Samuel", "Gomez")
    i=creaUser("sandra", "sandra", "sandra@hotmail.com", "Sandra", "Menos")
    j=creaUser("soto", "soto", "soto@hotmail.com", "Jose Manuel", "Soto")
    k=creaUser("manu", "manu", "manu@hotmail.com", "Manuel", "Serrano")
    l=creaUser("isaac", "isaac", "isaac@hotmail.com", "Isaac", "Cobacho")
    m=creaUser("mar", "mar", "mar@hotmail.com", "Mar", "Tukutu")
    n=creaUser("mejias", "mejias", "mejias@hotmail.com", "Jose Antonio", "Mejias")
    o=creaUser("monica", "monica", "monica@hotmail.com", "Monica", "Rueda")
    p=creaUser("marta", "marta", "marta@hotmail.com", "Marta", "Magdaleno")
    q=creaUser("joaquin", "joaquin", "joaquin@hotmail.com", "Joaquin", "Pineda")
    r=creaUser("segura", "segura", "segura@hotmail.com", "Antonio", "Segura")
    s=creaUser("advani", "advani", "advani@hotmail.com", "Javier", "Advani")
    t=creaUser("lucia", "lucia", "lucia@hotmail.com", "Lucia", "Garcia")
    u=creaUser("yolanda", "yolanda", "yolanda@hotmail.com", "Yolanda", "Cabrera")
    v=creaUser("luis", "luis", "luis@hotmail.com", "Luis", "Garrido")
    
    pa=creaPerfil(a)
    pb=creaPerfil(b)
    pc=creaPerfil(c)
    pd=creaPerfil(d)
    pf=creaPerfil(f)
    pg=creaPerfil(g)
    ph=creaPerfil(h)
    pi=creaPerfil(i)
    pj=creaPerfil(j)
    pk=creaPerfil(k)
    pl=creaPerfil(l)
    pm=creaPerfil(m)
    pn=creaPerfil(n)
    po=creaPerfil(o)
    pp=creaPerfil(p)
    pq=creaPerfil(q)
    pr=creaPerfil(r)
    ps=creaPerfil(s)
    pt=creaPerfil(t)
    pu=creaPerfil(u)
    pv=creaPerfil(v)
    
    addAmigos(pa, amigos=[pb,pc,pd,pf,pg,ph,pi,pj,pk,pl,pt,pu])
    addAmigos(pb, amigos=[pa,pc,pd,pf,ph,pi,pj,pk,pl,pm,pt,pu])
    addAmigos(pc, amigos=[pa,pb,pd,pf,ph,pi,pj,pk,pl,pt,pu])
    addAmigos(pd, amigos=[pa,pb,pc,pf,ph,pi,pj,pk,pl])
    addAmigos(pf, amigos=[pa,pb,pc,pd,ph,pi,pj,pk,pl])
    addAmigos(pg, amigos=[pa])
    
    #cargaComentariosRelleno()
    
    print "Carga completada de perfiles y relaciones"
    
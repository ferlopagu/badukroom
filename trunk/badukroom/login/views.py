from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from login.forms import UserForm, PerfilForm
from django.http import HttpResponseRedirect

#ultimos add
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
#add necesarios para la confirmacion de la web
import random
import string
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Perfil

def login_view(request):
    login_incorrecto=""
    formulario_login=AuthenticationForm()
    user_form = UserForm()
    perfil_form=PerfilForm()
    error_en_registro=False
    exito=False
    if request.method=='POST':
        formulario_login=AuthenticationForm(request.POST)
        user_form=UserForm(request.POST)
        perfil_form=PerfilForm(request.POST, request.FILES)
        if 'entrar' in request.POST:
            if formulario_login.is_valid:
                usuario=request.POST['username']
                clave=request.POST['password']
                acceso=authenticate(username=usuario, password=clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request, acceso)
                        return HttpResponseRedirect('/redsocial')
                    else:
                        return render_to_response('noactivo.html', context_instance=RequestContext(request))
                else:
                    error_login=True
                    login_incorrecto="El nick o password no son validos."
                    formulario_login=AuthenticationForm()
                    user_form = UserForm()
                    perfil_form=PerfilForm()
                    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error':error_login} ,context_instance=RequestContext(request) )
        elif 'registrar' in request.POST:
            #AQUI TENEMOS QUE COMPROBAR SI EL FORMULARIO ES VALIDO
            #if messageform.is_valid():   <-- INCLUIR EL PARENTESIS http://stackoverflow.com/questions/5358566/saving-modelform-erroruser-message-could-not-be-created-because-the-data-didnt
            if user_form.is_valid():
                user = user_form.save()
                user.is_active = False
                user.save()
                confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
                if perfil_form.is_valid():
                    perfil=perfil_form.save(commit=False) #tenemos que add el usuario
                    perfil.user=user #add el usuario al perfil 
                    perfil.confirmation_code=confirmation_code #ADD confirmation code to perfil
                    perfil.save() #guardamos el perfil
                    send_registration_confirmation(user)
                    print "REDIRECCIONAMOS A INICIO"
                    exito=True
                    #VOLVEMOS A CARGAR LOS FORMULARIOS VACIOS
                    formulario_login=AuthenticationForm()
                    user_form = UserForm()
                    perfil_form=PerfilForm()
                    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error':error_en_registro, 'exito':exito}, context_instance=RequestContext(request))
                else:
                    print "EL PERFIL_FORM NO ES VALID"
                    user.delete()
            else:
                print "EL USERFORM NO ES VALID"
        else:
            return HttpResponseRedirect('/quedise')          
    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error':error_en_registro, 'exito':exito}, context_instance=RequestContext(request))

def send_registration_confirmation(user):
    p = Perfil.objects.get(user = user)
    email = user.email
    title = "BadukRoom confirmacion"
    parrafo1 = "Bienvenido a Badukroom \n\n Debe ingresar al siguiente enlace para activar su cuenta: \n\n"
    content = "http://127.0.0.1:8000/confirm/" + str(p.confirmation_code) + "/" + user.username
    parrafo2 = "\n\n Saludos, \n BadukRoom Team."
    mensaje=parrafo1+content+parrafo2
    send_mail(title, mensaje, 'no-reply@badukroom.com', [email], fail_silently=False)

def confirm(request, confirmation_code, username):
    try:
        user = User.objects.get(username=username)
        profile = Perfil.objects.get(user = user)
        if profile.confirmation_code == confirmation_code:
            print "LOS CODIGOS SON IGUALES"
        if profile.confirmation_code == confirmation_code: #and user.date_joined > (datetime.datetime.now()-datetime.timedelta(days=1)):
            user.is_active = True
            user.save()
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request,user) #estaba en auth_login
            return HttpResponseRedirect('/redsocial/'+user.username)
        return HttpResponseRedirect('../../../../../') #Mandar a pagina de error en la confirmacion
    except:
        return HttpResponseRedirect('../../../../../') #Mandar a pagina de error en la confirmacion

@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
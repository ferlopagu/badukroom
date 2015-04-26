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
import datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Perfil

def holaMundo(request):
    return render_to_response('mundo.html', locals())

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
            print "Entro en entrar"
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
                    print "el formulario es valido pero acceso es not"
                    login_incorrecto="El nick o password no son validos."
                    formulario_login=AuthenticationForm()
                    user_form = UserForm()
                    perfil_form=PerfilForm()
                    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto} ,context_instance=RequestContext(request) )
                    #return render_to_response('nousuario.html', context_instance=RequestContext(request))
        elif 'registrar' in request.POST:
            """
            print "Entro en registrar"
            if user_form.is_valid() and perfil_form.is_valid():
                print "userform y perfilform son validos"
                print request.FILES
                user=user_form.save() #guardamos el usuario
                perfil=perfil_form.save(commit=False) #tenemos que add el usuario
                perfil.user=user #add el usuario al perfil 
                perfil.save() #guardamos el perfil
                return HttpResponseRedirect('/')
            """
            if error_register(request):
                error_en_registro=True
                return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error': error_en_registro}, context_instance=RequestContext(request))
            else:
                #AQUI TENEMOS QUE COMPROBAR SI EL FORMULARIO ES VALIDO
                #AUN POR HACER 
                #if messageform.is_valid():   <-- INCLUIR EL PARENTESIS http://stackoverflow.com/questions/5358566/saving-modelform-erroruser-message-could-not-be-created-because-the-data-didnt
                user = user_form.save()
                user.is_active = False
                user.save()
                confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
                perfil=perfil_form.save(commit=False) #tenemos que add el usuario
                perfil.user=user #add el usuario al perfil 
                perfil.confirmation_code=confirmation_code #ADD confirmation code to perfil
                perfil.save() #guardamos el perfil
                send_registration_confirmation(user)
                print "REDIRECCIONAMOS A INICIO"
                #return HttpResponseRedirect('/')
                exito=True
                #VOLVEMOS A CARGAR LOS FORMULARIOS VACIOS
                formulario_login=AuthenticationForm()
                user_form = UserForm()
                perfil_form=PerfilForm()
                return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error':error_en_registro, 'exito':exito}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect('/quedise')          
    #else:
        #formulario_login=AuthenticationForm()
        #user_form = UserForm()
        #perfil_form=PerfilForm()
    return render_to_response('login.html', {'formulario_login':formulario_login, 'user_form':user_form, 'perfil_form':perfil_form, 'login_incorrecto':login_incorrecto, 'error':error_en_registro, 'exito':exito}, context_instance=RequestContext(request))

#INTENTO DE HACER EL REGISTRO Y LOGIN CON EMAIL DE CONFIRMACION

"""
def register(request):
    if request.method == 'POST':
        captcha_error = ""
        captcha_response = captcha.submit(
        request.POST.get("recaptcha_challenge_field", None),
        request.POST.get("recaptcha_response_field", None),
        settings.RECAPTCHA_PRIVATE_KEY,
        request.META.get("REMOTE_ADDR", None))
        if not captcha_response.is_valid:
            captcha_error = "&error=%s" % captcha_response.error_code
            c = {}
            c.update(csrf(request))
            c['repetir'] = True
            c['header'] = "register"
            return render_to_response('register.html', c, context_instance=RequestContext(request))
        else:
            if error_register(request):
                c = {}
                c.update(csrf(request))
                c['repetir'] = True
                c['header'] = "register"
                return render_to_response('register.html', c, context_instance=RequestContext(request))
            else:
                username = clean_username(request.POST['user'])
                password = request.POST['password']
                email = request.POST['email']
                user = User.objects.create_user(username, email, password)
                user.is_active = False
                user.save()
                confirmation_code = ''.join(tehrandom.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
                p = Profile(user=user, confirmation_code=confirmation_code)
                p.save()
                send_registration_confirmation(user)
                return HttpResponseRedirect('../../../../../')
    else:
        c = create_c(request)
        c['header'] = "register"
        return render_to_response('register.html', c, context_instance=RequestContext(request))
"""

def send_registration_confirmation(user):
    print "ENTRAMOS EN send_registration"
    p = Perfil.objects.get(user = user)
    email = user.email
    title = "BadukRoom confirmacion"
    parrafo1 = "Bienvenido a Badukroom \n\n Debe ingresar al siguiente enlace para activar su cuenta: \n\n"
    content = "http://127.0.0.1:8000/confirm/" + str(p.confirmation_code) + "/" + user.username
    parrafo2 = "\n\n Saludos, \n BadukRoom Team."
    mensaje=parrafo1+content+parrafo2
    send_mail(title, mensaje, 'no-reply@badukroom.com', [email], fail_silently=False)
    print "DEBERIAMOS HABER ENVIADO EL EMAIL"

def confirm(request, confirmation_code, username):
    print "ENTRAMOS EN confirm"
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
        print "NO EXISTE USUARIO O PERFIL EN METODO CONFIRM"
        return HttpResponseRedirect('../../../../../') #Mandar a pagina de error en la confirmacion

def error_register(request):
    username = request.POST['username']
    password = request.POST['password1'] 
    email = request.POST['email'] 
    #if not clean_username(username):
    #    return True
    
    
    
    
    print "ENTRAMOS EN error_register"
    if username.replace(" ", "") == "" or password.replace(" ", "") == "":
        return True
    if len(username) > 15 or len(password) > 50:
        return True
    if not "@" in email:
        return True
    try:
        if User.objects.get(username=username):
            return True
    except:
        pass

from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import authenticate, login,logout 
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

def home(request): 
    return render(request, 'home.html')

def registroUsuario(request):
    if request.method == 'POST':
        form = FormularioUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado exitosamente, ya puedes iniciar sesion')
    else:
        form = FormularioUser()

    return render(request, 'registro.html', {
        'form': form
    })
    
def inicioSesion(request):
    if request.method == "GET":
        return render(request, "inicioSesion.html", {"form": AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            usuario = authenticate(
                request,
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password"),
            )
            if usuario is not None:
                login(request, usuario)
                return redirect("crear_alerta")
        return render(
            request,
            "inicioSesion.html",
            {"form": form, "error": "Usuario o contraseña incorrecta"},
        )
        

def crear_alerta(request):
    if request.method == 'POST':
        form = AlertaForm(request.POST, request.FILES)  # Maneja archivos
        if form.is_valid():
            alerta = form.save(commit=False)
            alerta.usuario = request.user  # Asigna el usuario actual
            alerta.save()
            # Enviar notificación a todas las autoridades
            autoridades = Autoridad.objects.all()
            for autoridad in autoridades:
                Notificacion.objects.create(
                    alerta=alerta,
                    autoridad=autoridad
                )
                # Agregar mensaje de éxito
            messages.success(request, 'Alerta creada y notificación enviada a la autoridad correspondiente.')
            return redirect('ver_alertas')  # Redirige a la vista de lista de alertas
    else:
        form = AlertaForm()
    
    return render(request, 'crear_alerta.html', {'form': form})


def ver_alertas(request):
    alertas = Alerta.objects.all().order_by('-fecha_creacion')
    return render(request, 'ver_alertas.html', {'alertas': alertas})

def alerta_detalle(request, pk):
    alerta = get_object_or_404(Alerta, pk=pk)
    notificada = Notificacion.objects.filter(alerta=alerta).exists()
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.usuario = request.user
            comentario.alerta_id = request.POST.get('alerta_id')  # Obtiene el id de la alerta desde el formulario
            comentario.save()
            return redirect('alerta_detalle', pk=pk)
    else:
        form = ComentarioForm()

    return render(request, 'alerta_detalle.html', {'alerta': alerta, 'notificada': notificada, 'form':form})


def cerrarSesion(request):
    logout(request)
    return redirect("home")
    
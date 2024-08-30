from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.forms import ModelForm

class FormularioUser(UserCreationForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'identificacion', 'rol', 'telefono', 'ciudad')
        
    
class AlertaForm(ModelForm):
    class Meta:
        model = Alerta
        fields = ['titulo', 'descripcion', 'ubicacion', 'gravedad', 'imagen_multimedia']

class ComentarioForm(ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
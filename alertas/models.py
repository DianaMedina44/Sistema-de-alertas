from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    identificacion = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    telefono = models.BigIntegerField(null=True, blank=True) 
    ciudad = models.CharField(max_length=100, null=True, blank=True)  

    def __str__(self):
        return self.username
    
class Alerta(models.Model):
    TITULO_OPCIONES = [
        ('INUNDACION', 'Inundación'),
        ('INCENDIO', 'Incendio'),
        ('DESLIZAMIENTO', 'Deslizamiento'),
        ('VENDAVAL', 'Vendaval'),
        # Agrega más opciones aquí
    ]
    GRAVEDAD_OPCIONES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
        # Agrega más opciones aquí
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, choices=TITULO_OPCIONES)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ubicacion = models.CharField(max_length=250, blank=False)  # Campo obligatorio

    # ubicacion_latitud = models.FloatField()  # Descomentarlo si decides usar latitud
    # ubicacion_longitud = models.FloatField()  # Descomentarlo si decides usar longitud
    gravedad = models.CharField(max_length=50, choices=GRAVEDAD_OPCIONES)
    validada = models.BooleanField(default=False)
    imagen_multimedia = models.ImageField(upload_to='alertas/')
   
    
    def __str__(self):
        return f'{self.get_titulo_display()} - {self.descripcion}'


class Comentario(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'comentario de alerta {self.alerta.titulo}'

class Autoridad(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)

class Notificacion(models.Model):
    alerta = models.ForeignKey(Alerta, on_delete=models.CASCADE)
    autoridad = models.ForeignKey(Autoridad, on_delete=models.CASCADE)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Notificación para {self.autoridad.nombre} sobre {self.alerta.titulo}"

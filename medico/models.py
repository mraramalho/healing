from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime as dt

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
        return self.especialidade


class DadosMedico(models.Model):
    crm = models.CharField(max_length=30, unique=True)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to=os.path.join("medico", "rgs"), unique=True)
    cedula_identidade_medica = models.ImageField(upload_to=os.path.join("medico", "cim"))
    foto = models.ImageField(upload_to=os.path.join("medico", "fotos_perfil"))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True, blank=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)
    valor_consulta = models.FloatField(default=100)

    def __str__(self):
        return self.user.username
    
    @property
    def proxima_data(self):
        return CadastroAgenda.objects.filter(user=self.user).filter(data__gt=dt.now()).filter(agendado=False).order_by('data').first()
    
class CadastroAgenda(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)
    
    
    def __str__(self):
        return str(self.data)
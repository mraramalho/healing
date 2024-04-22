from django.contrib import admin
from .models import Especialidades, DadosMedico, CadastroAgenda

# Register your models here.
admin.site.register(DadosMedico)
admin.site.register(Especialidades)
admin.site.register(CadastroAgenda)

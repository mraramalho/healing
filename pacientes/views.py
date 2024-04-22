from django.shortcuts import render
from medico.models import DadosMedico, Especialidades, CadastroAgenda
from .models import Consulta
from django.contrib.messages import add_message, constants
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime as dt
from django.contrib.auth.decorators import login_required
from medico.views import is_medico


# Create your views here.
@login_required
def home(request):
    especialidades = Especialidades.objects.all()
    dados_medico = DadosMedico.objects.all()
    
    if request.method=='GET':
            
        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')
        proxima_consulta = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=dt.now()).order_by('data_aberta').first()

        if proxima_consulta:
            medico = dados_medico.get(user=proxima_consulta.data_aberta.user.id)
            lembrete =  f'Consulta com {medico.nome} dia {proxima_consulta.data_aberta.data}'
        else:
            lembrete = None
            
        if medico_filtrar:
            dados_medico = dados_medico.filter(nome__icontains = medico_filtrar)

        if especialidades_filtrar:
            dados_medico = dados_medico.filter(especialidade_id__in=especialidades_filtrar)
        
        return render(request, 'pacientes/home.html', context={'dados_medico':dados_medico, 
                                                            'especialidades': especialidades,
                                                            'is_medico': is_medico(request.user),
                                                            'lembrete': lembrete,})
        
@login_required       
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = CadastroAgenda.objects.filter(user=medico.user).filter(data__gte=dt.now()).filter(agendado=False)
        return render(request, 'pacientes/escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas, 'is_medico': is_medico(request.user)})

@login_required
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = CadastroAgenda.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        horario_agendado.save()

        # TODO: Sugestão Tornar atomico

        data_aberta.agendado = True
        data_aberta.save()

        add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')

        return redirect(reverse('minhas_consultas'), context = {'is_medico': is_medico(request.user)})
    
@login_required    
def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=dt.now())
        return render(request, 'pacientes/minhas_consultas.html', {'minhas_consultas': minhas_consultas, 'is_medico': is_medico(request.user)})

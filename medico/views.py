from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Especialidades, DadosMedico, CadastroAgenda
from django.contrib.messages import constants, add_message
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime as dt
from pacientes.models import Consulta, Documento
from datetime import timedelta

def is_medico(user):
    return DadosMedico.objects.filter(user=user).exists()

@login_required
def cadastro_medico(request):
    if request.method == "GET":
        especialidades = Especialidades.objects.all()
        return render(request, 'medico/cadastro_medico.html', {'especialidades': especialidades, 'is_medico': is_medico(request.user)})
    elif request.method == "POST":
        crm = request.POST.get('crm')
        nome = request.POST.get('nome')
        cep = request.POST.get('cep')
        rua = request.POST.get('rua')
        bairro = request.POST.get('bairro')
        numero = request.POST.get('numero')
        cim = request.FILES.get('cim')
        rg = request.FILES.get('rg')
        foto = request.FILES.get('foto')
        especialidade = request.POST.get('especialidade')
        descricao = request.POST.get('descricao')
        valor_consulta = request.POST.get('valor_consulta')

        #TODO: Validar todos os campos
        
        if is_medico(request.user):
            add_message(request, constants.WARNING, 'Você já está cadastrado como médico.')
            return redirect(reverse('cadastro_medico'))

        dados_medico = DadosMedico(
            crm=crm,
            nome=nome,
            cep=cep,
            rua=rua,
            bairro=bairro,
            numero=numero,
            rg=rg,
            cedula_identidade_medica=cim,
            foto=foto,
            user=request.user,
            descricao=descricao,
            especialidade_id=especialidade,
            valor_consulta=valor_consulta
        )
        dados_medico.save()

        add_message(request, constants.SUCCESS, 'Cadastro médico realizado com sucesso.')

        return redirect('/medicos/abrir_horario')

@login_required
def cadastro_agenda(request):
    
    if not is_medico(request.user):
        return redirect(reverse(cadastro_medico))
    
    if request.method == 'GET':
        agenda = CadastroAgenda.objects.filter(user=request.user)
        dados_medico = DadosMedico.objects.get(user=request.user)
        return render(request, 'medico/cadastro_agenda.html', context = {'dados_medico': dados_medico, 'agenda': agenda, 'is_medico': is_medico(request.user)})
    
    elif request.method == 'POST':
        data = request.POST.get('data')
        data_formatada = dt.strptime(data, "%Y-%m-%dT%H:%M")
        
        if data_formatada <= dt.now():
            add_message(request, constants.WARNING, 'A data deve ser maior ou igual a data atual.')
            return redirect(reverse('cadastro_agenda'))
        
        CadastroAgenda(
            data=data,
            user=request.user
        ).save()
        
        add_message(request, constants.SUCCESS, "Horário cadastrado com sucesso!")
        return redirect(reverse('cadastro_agenda'))

@login_required
def consultas_medico(request):
    if not is_medico(request.user):
        return redirect(reverse('cadastro_agenda'))
    
    hoje = dt.now().date()

    consultas_hoje = Consulta.objects.filter(data_aberta__user=request.user).filter(data_aberta__data__gte=hoje).filter(data_aberta__data__lt=hoje + timedelta(days=1))
    consultas_restantes = Consulta.objects.exclude(id__in=consultas_hoje.values('id'))

    return render(request, 'medico/consultas_medico.html', {'consultas_hoje': consultas_hoje, 'consultas_restantes': consultas_restantes, 'is_medico': is_medico(request.user)})

@login_required
def consulta_area_medico(request, id_consulta):
    if not is_medico(request.user):
        return redirect(reverse('home'))

    if request.method == "GET":
        consulta = Consulta.objects.get(id=id_consulta)
        documentos = Documento.objects.filter(consulta=consulta)
        return render(request, 'medico/consulta_area_medico.html', {'consulta': consulta, 'documentos': documentos,'is_medico': is_medico(request.user)})
    
    elif request.method == "POST":
        # Inicializa a consulta + link da chamada
        consulta = Consulta.objects.get(id=id_consulta)
        link = request.POST.get('link')

        if consulta.status == 'C':
            add_message(request, constants.WARNING, 'Essa consulta já foi cancelada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        elif consulta.status == "F":
            add_message(request, constants.WARNING, 'Essa consulta já foi finalizada, você não pode inicia-la')
            return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
        
        consulta.link = link
        consulta.status = 'I'
        consulta.save()

        add_message(request, constants.SUCCESS, 'Consulta inicializada com sucesso.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
def finalizar_consulta(request, id_consulta):
    if not is_medico(request.user):
        return redirect(reverse('home'))
    
    consulta = Consulta.objects.get(id=id_consulta)
    if request.user != consulta.data_aberta.user:
        add_message(request, constants.WARNING, "Essa consulta não é sua!")
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    consulta.status = 'F'
    consulta.save()
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

def add_documento(request, id_consulta):
    if not is_medico(request.user):
        return redirect(reverse('home'))
    
    consulta = Consulta.objects.get(id=id_consulta)
    
    if consulta.data_aberta.user != request.user:
        add_message(request, constants.ERROR, 'Essa consulta não é sua!')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    
    
    titulo = request.POST.get('titulo')
    documento = request.FILES.get('documento')

    if not documento:
        add_message(request, constants.WARNING, 'Adicione o documento.')
        return redirect(f'/medicos/consulta_area_medico/{id_consulta}')

    documento = Documento(
        consulta=consulta,
        titulo=titulo,
        documento=documento

    )

    documento.save()

    add_message(request, constants.SUCCESS, 'Documento enviado com sucesso!')
    return redirect(f'/medicos/consulta_area_medico/{id_consulta}')
    

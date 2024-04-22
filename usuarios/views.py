from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages

def exibir_mensagem_de_erro(request, mensagem: str):
    messages.add_message(request, messages.constants.ERROR, mensagem)
    
def cadastrar(request):
    if request.method == 'GET':
        return render(request, 'usuarios/cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        cadastro_webpage = redirect(reverse('cadastro'))
        login_webpage = redirect(reverse('login'))
        
        if senha != confirmar_senha:
            exibir_mensagem_de_erro(request, mensagem="Senha e Confirmar senha devem ser iguais.")
            return cadastro_webpage
        
        if len(senha) < 6:
            exibir_mensagem_de_erro(request, mensagem= "Sua senha deve ter ao menos 6 caracteres.")
            return cadastro_webpage
        
        if len(username) <= 3:
            exibir_mensagem_de_erro(request, mensagem= "Usuário precisa ter mais de 3 caracteres.")
            return cadastro_webpage
        
        users = User.objects.filter(username=username)
        emails = User.objects.filter(email=email)
               
        if users.exists():
            exibir_mensagem_de_erro(request, mensagem= "Username já existe. Escolha outro.")
            return cadastro_webpage
        if emails.exists():
            exibir_mensagem_de_erro(request, mensagem= "Já existe um usuário cadastrado com esse endereço de e-mail. Tente recuperar a senha ou cadastre outro e-mail.")
            return cadastro_webpage
        
        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            ).save()
            return login_webpage
        except:
            exibir_mensagem_de_erro(request, mensagem= "Erro ao salvar o usuário. Tente novamente mais tarde!")
            return cadastro_webpage
        
def login(request):
    if request.method == 'GET':
        print(request.user)
        return render(request, 'usuarios/login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request,
                                 username=username, 
                                 password=senha)
        if user:
            auth.login(request=request, user=user)
            return redirect('home')
        
        exibir_mensagem_de_erro(request=request,
                                mensagem="Usuário e/ou senha incorretos")
        return redirect(reverse('login'))
    
def sair(request):
    auth.logout(request)
    return redirect(reverse('login'))       
    
def home(request):
    if request.method == 'GET':
        return render(request, 'pacientes/home.html')
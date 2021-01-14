from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContato


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login feito com sucesso')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')


def cadastro(request):
    if request.method != 'POST':
        messages.info(request, 'Nada Postado')
        return render(request, 'accounts/register.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha_confirma = request.POST.get('senha_confirma')
    
    if not nome or not sobrenome or not email or not usuario or not senha or not senha_confirma:
        messages.error(request, 'Todos os campos devem estar preenchidos')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')

    if len(senha) < 6:
        messages.error(request, 'A senha deve possuir mais de 6 caracteres')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'O nome de usuário deve possuir mais de 6 caracteres')
        return render(request, 'accounts/register.html')

    if senha != senha_confirma:
        messages.error(request, 'O campo da senha deve ser igual ao da confirmação')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já cadastrado')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Email já cadastrado')
        return render(request, 'accounts/register.html')

    messages.success(request, 'Cadastrado com sucesso')
    user = User.objects.create_user(username=usuario, email=email, password=senha, first_name=nome, last_name=sobrenome)
    user.save()
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContato()
        return render(request, 'accounts/dashboard.html', {'form': form})
    form = FormContato(request.POST, request.FILES)

    if form.is_valid():
        form.save()
        messages.success(request, f'Contato {request.POST.get("nome")} salvo com sucesso')
        return render(request, 'accounts/dashboard.html', {'form:'})
    else:
        messages.error(request, 'Erro ao enviar formulário')
        form = FormContato(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

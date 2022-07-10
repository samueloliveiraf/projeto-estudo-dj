from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.contrib.auth.models import User


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')
    

def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    
    nome = request.POST.get('nome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Há campo vazio')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/register.html')

    if len(senha) < 8:
        messages.error(request, 'Senha precisa ter 8 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if len(usuario) < 6:
        messages.error(request, 'Usuário precisa ter 6 caracteres ou mais')
        return render(request, 'accounts/register.html')

    if senha != senha2:
        messages.error(request, 'A senhas não são iguais')
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuário já existe')
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Usuário com esse email já existe')
        return render(request, 'accounts/register.html')

    User.objects.create(
        username=usuario,
        email=email,
        first_name=nome,
        password=senha
    )

    messages.success(request, 'Usuário cadastrado!')

    return redirect('login')

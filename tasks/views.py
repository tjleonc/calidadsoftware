from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)  # Inicia sesión automáticamente después del registro
                return redirect('tasks')  # Redirige a la página de tareas
            except IntegrityError:
                # Manejo de error si el usuario ya existe
                return render(request, 'signup.html', {'form': form, 'error': 'El usuario ya existe'})
        else:
            # Muestra el formulario con errores si no es válido
            return render(request, 'signup.html', {'form': form})
        
# def signup(request):
    # if request.method == 'POST':
    #     form = CustomUserCreationForm(request.POST)
    #     if form.is_valid():
    #         user = form.save()
    #         login(request, user)  # Inicia sesión automáticamente después del registro
    #         return redirect('home')  # Redirige a la página de inicio u otra URL definida en tu proyecto
    #     else:
    #         # Retorna la misma página con los errores del formulario si no es válido
    #         return render(request, 'signup.html', {'form': form})
    # else:
    #     form = CustomUserCreationForm()
    #     # Retorna el formulario vacío si la petición no es POST
    #     return render(request, 'signup.html', {'form': form})



@login_required
def tasks(request):
    return render(request, 'tasks.html')

@login_required
def cerrarSesion(request):
    logout(request)
    return redirect('home')

def entrar(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'form': AuthenticationForm(), 'error': 'Usuario o contraseña incorrectos'})
        else:
            login(request, user)
            return redirect('tasks')
        
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import Review, Item
from .forms import ReviewForm
from django.shortcuts import get_object_or_404



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
                return redirect('home')  # Redirige a la página de tareas
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
def reseñas(request):
    return render(request, 'reseñas.html')

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
            return redirect('home')
        
def eliminarUsuario(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    usuario.delete()
    return redirect('home')

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
    else:
        validlink = False

    if request.method == 'POST' and validlink:
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 and password2 and password1 == password2:
            user.password = make_password(password1)
            user.save()
            messages.success(request, 'Tu contraseña ha sido restablecida con éxito.')
            return redirect('login')  # Cambia 'login' por el nombre de tu vista de inicio de sesión
        else:
            messages.error(request, 'Las contraseñas no coinciden o son inválidas.')

    context = {
        'validlink': validlink
    }
    return render(request, 'password_reset_confirm.html', context)  # Cambia 'tu_template.html' por el nombre de tu archivo de template




def add_review(request, pk):
    item = get_object_or_404(Item, pk=pk)  # Obtener el item basado en el ID
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)  # No guardamos aún
            review.item = item  # Establecer la relación con el item
            review.author = request.user  # Asume que el usuario está autenticado
            review.save()  # Ahora guardamos la reseña
            return redirect('item_detail', pk=item.pk)  # Redirigir al detalle del item
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'item': item, 'form': form})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

# Vista para ver los detalles de un producto específico
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    reviews = item.reviews.all()  # Ahora esto debería funcionar
    return render(request, 'item_detail.html', {'item': item, 'reviews': reviews})


# Vista para añadir una reseña a un producto
def add_review(request, pk):
    item = get_object_or_404(Item, pk=pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.item = item
            review.author = request.user
            review.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'item': item, 'form': form})
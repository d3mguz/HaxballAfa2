from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


User = get_user_model()


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    first_name = forms.CharField(max_length=150, required=True, label="Nombre")
    last_name = forms.CharField(max_length=150, required=True, label="Apellido")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "last_name", "email")
        labels = {"username": "Nombre de usuario"}

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta registrada con ese correo.")
        return email


def inicio(request):
    return render(request, 'app1/index.html')


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu cuenta fue creada correctamente. Ya podés iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'app1/registro.html', {'form': form})


def iniciar_sesion(request):
    # Si ya hay una sesión activa, mostramos el panel de cuenta.
    # El enlace a usuarios registrados se renderiza únicamente para superusuarios.
    if request.user.is_authenticated:
        return render(request, 'app1/login.html', {'error': None})

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        error = 'Usuario o contraseña incorrectos.'
    return render(request, 'app1/login.html', {'error': error})


@login_required
@require_POST
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


def es_superusuario(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(es_superusuario, login_url='inicio')
def usuarios_registrados(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'app1/usuarios.html', {'usuarios': usuarios})

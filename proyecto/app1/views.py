from django.shortcuts import render, redirect
from django.http import HttpResponse

def inicio(request):
    return render(request, 'app1/index.html')


# {% extends 'app1/base.html'  %} para heredar de base.html, ej creamos una carpeta componentes y los metemos en todos lados

# {% block content %} para que se pueda cambiar el contenido de la pagina, ej en index.html ponemos un h1 y en base.html ponemos otro h1, al final se mostrara el h1 de index.html LE METEMOS CONTENIDO AL OTRO HTML
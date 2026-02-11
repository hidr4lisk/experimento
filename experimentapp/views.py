from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def home(request):
    return HttpResponse("Página de inicio")

# Create your views here.
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse("Login OK")
        return HttpResponse("Credenciales inválidas", status=401)
    return render(request, "experimentapp/login.html")  
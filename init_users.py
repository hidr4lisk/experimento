#!/usr/bin/env python
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'experimento.settings')
django.setup()

from django.contrib.auth.models import User

# Crear usuarios si no existen
users_to_create = [
    {'username': 'admin', 'email': 'admin@example.com', 'password': 'admin', 'is_superuser': True},
    {'username': 'emma', 'email': 'emma@example.com', 'password': 'emma', 'is_superuser': False},
    {'username': 'pipo', 'email': 'pipo@example.com', 'password': 'pipo', 'is_superuser': False},
]

for user_data in users_to_create:
    username = user_data['username']
    email = user_data['email']
    password = user_data['password']
    is_superuser = user_data['is_superuser']
    
    if not User.objects.filter(username=username).exists():
        if is_superuser:
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"✓ Superusuario '{username}' creado")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            print(f"✓ Usuario '{username}' creado")
    else:
        print(f"• Usuario '{username}' ya existe")

print("\n✓ Inicialización completada")

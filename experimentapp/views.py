from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Agent, Record
from datetime import datetime, timedelta
import holidays
from django.core.management import call_command

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'experimentapp/home_not_logged.html')
    
    records = Record.objects.all().order_by('-fecha_inicio')
    
    # Filtros
    agent_filter = request.GET.get('agent')
    record_type_filter = request.GET.get('type')
    
    if agent_filter:
        records = records.filter(agent_id=agent_filter)
    if record_type_filter:
        records = records.filter(record_type=record_type_filter)
    
    # Ordenamiento
    sort_by = request.GET.get('sort', '-fecha_inicio')
    records = records.order_by(sort_by)
    
    agents = Agent.objects.all()
    is_admin = request.user.is_superuser
    
    context = {
        'records': records,
        'agents': agents,
        'is_admin': is_admin,
        'record_types': Record.RECORD_TYPES,
    }
    return render(request, 'experimentapp/home.html', context)

@login_required(login_url='login')
def agent_calendar(request, agent_id):
    agent = get_object_or_404(Agent, id=agent_id)
    records = Record.objects.filter(agent=agent)
    
    context = {
        'agent': agent,
        'records': records,
    }
    return render(request, 'experimentapp/agent_calendar.html', context)

@login_required(login_url='login')
def agent_calendar_data(request, agent_id):
    """API que devuelve los eventos del calendario en formato JSON"""
    agent = get_object_or_404(Agent, id=agent_id)
    records = Record.objects.filter(agent=agent)
    
    # Mapeo de colores por tipo de registro
    color_map = {
        'vacaciones': '#ffc107',      # Amarillo
        'franquicia': '#6f42c1',      # Morado
        'razon_particular': '#fd7e14', # Naranja
        'comision': '#dc3545',        # Rojo
    }
    
    events = []
    
    # Obtener el rango de fechas para los feriados
    all_dates = [r.fecha_inicio for r in records] + [r.fecha_fin for r in records]
    if all_dates:
        min_year = min(d.year for d in all_dates)
        max_year = max(d.year for d in all_dates)
    else:
        min_year = datetime.now().year
        max_year = datetime.now().year
    
    # Cargar feriados de Argentina para los años relevantes
    ar_holidays = holidays.AR(years=range(min_year, max_year + 1))
    
    # Agregar feriados al calendario
    for date, name in ar_holidays.items():
        if date.weekday() < 5:  # Solo feriados en días hábiles (opcional, pero consistente con el resto)
            events.append({
                'title': f'Feriado: {name}',
                'start': date.strftime('%Y-%m-%d'),
                'backgroundColor': '#e2e8f0',
                'borderColor': '#cbd5e0',
                'textColor': '#4a5568',
                'allDay': True,
                'display': 'background', # Opcional: mostrar como fondo
            })
        else:
            # Si es fin de semana, igual lo agregamos pero quizás con otro estilo o solo el título
            events.append({
                'title': f'Feriado: {name}',
                'start': date.strftime('%Y-%m-%d'),
                'backgroundColor': '#e2e8f0',
                'borderColor': '#cbd5e0',
                'textColor': '#4a5568',
                'allDay': True,
            })

    # Agregar eventos de los registros (días que no vino)
    for record in records:
        current_date = record.fecha_inicio
        color = color_map.get(record.record_type, '#667eea')  # Color default
        
        while current_date <= record.fecha_fin:
            # Solo marcamos días de lunes a viernes (weekday 0-4)
            if current_date.weekday() < 5:  # 0=lunes, 4=viernes
                events.append({
                    'title': f'{record.get_record_type_display()}',
                    'start': current_date.strftime('%Y-%m-%d'),
                    'backgroundColor': color,
                    'borderColor': color,
                    'textColor': 'white',
                    'allDay': True,
                })
            current_date += timedelta(days=1)
    
    return JsonResponse(events, safe=False)

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        context = {'error': 'Credenciales inválidas'}
        return render(request, "experimentapp/login.html", context)
    return render(request, "experimentapp/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def add_agent(request):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    if request.method == "POST":
        name = request.POST.get('name')
        location = request.POST.get('location')
        Agent.objects.create(name=name, location=location)
        return redirect('home')
    
    return render(request, 'experimentapp/add_agent.html')

@login_required(login_url='login')
def edit_agent(request, agent_id):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    agent = get_object_or_404(Agent, id=agent_id)
    
    if request.method == "POST":
        agent.name = request.POST.get('name')
        agent.location = request.POST.get('location')
        agent.save()
        return redirect('home')
    
    context = {'agent': agent}
    return render(request, 'experimentapp/edit_agent.html', context)

@login_required(login_url='login')
def add_record(request):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    if request.method == "POST":
        agent_id = request.POST.get('agent')
        record_type = request.POST.get('record_type')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        notes = request.POST.get('notes', '')
        
        agent = get_object_or_404(Agent, id=agent_id)
        Record.objects.create(
            agent=agent,
            record_type=record_type,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            notes=notes
        )
        return redirect('home')
    
    agents = Agent.objects.all()
    context = {
        'agents': agents,
        'record_types': Record.RECORD_TYPES
    }
    return render(request, 'experimentapp/add_record.html', context)

@login_required(login_url='login')
def edit_record(request, record_id):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    record = get_object_or_404(Record, id=record_id)
    
    if request.method == "POST":
        record.agent_id = request.POST.get('agent')
        record.record_type = request.POST.get('record_type')
        record.fecha_inicio = request.POST.get('fecha_inicio')
        record.fecha_fin = request.POST.get('fecha_fin')
        record.notes = request.POST.get('notes', '')
        record.save()
        return redirect('home')
    
    agents = Agent.objects.all()
    context = {
        'record': record,
        'agents': agents,
        'record_types': Record.RECORD_TYPES
    }
    return render(request, 'experimentapp/edit_record.html', context)  

@login_required(login_url='login')
def delete_record(request, record_id):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    record = get_object_or_404(Record, id=record_id)
    record.delete()
    return redirect('home')

@login_required(login_url='login')
def delete_agent(request, agent_id):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    agent = get_object_or_404(Agent, id=agent_id)
    agent.delete()
    return redirect('home')

def debug_db(request):
    """View para diagnosticar problemas de base de datos"""
    # No verificamos autenticación aquí para poder acceder aun cuando el login falla
    # Pero usamos un secreto o algo simple si es necesario, por ahora acceso libre
    # para debug rápido (solo habilitar temporalmente)
    try:
        from django.db import connection
        from django.core.management import call_command
        
        # Si pasan ?migrate=true, forzamos las migraciones
        if request.GET.get('migrate') == 'true':
            call_command('migrate', no_input=True)
            # El script init_users.py no es un comando de Django, se corre por separado
            import subprocess
            res = subprocess.run(["python", "init_users.py"], capture_output=True, text=True)
            return JsonResponse({
                'status': 'Migrations and users initialization attempted',
                'migration_output': 'OK',
                'user_init_output': res.stdout or res.stderr
            })

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
        
        from django.contrib.auth.models import User
        from .models import Agent, Record
        
        db_info = {
            'connection': 'OK' if row else 'Failed',
            'engine': connection.settings_dict['ENGINE'],
            'host': connection.settings_dict['HOST'],
            'user_count': User.objects.count(),
            'agent_count': Agent.objects.count(),
            'record_count': Record.objects.count(),
        }
        return JsonResponse(db_info)
    except Exception as e:
        import traceback
        return JsonResponse({
            'error': str(e),
            'traceback': traceback.format_exc()
        }, status=500)
@login_required(login_url='login')
def trigger_population(request):
    if not request.user.is_superuser:
        return HttpResponse("No autorizado", status=403)
    
    try:
        from django.core.management import call_command
        call_command('populate_agents')
        return HttpResponse("¡Éxito! La base de datos ha sido poblada con la lista definitiva.")
    except Exception as e:
        return HttpResponse(f"Error al poblar la base de datos: {str(e)}", status=500)

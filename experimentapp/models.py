from django.db import models
from django.contrib.auth.models import User

class Agent(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ubicación")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Record(models.Model):
    RECORD_TYPES = (
        ('vacaciones', 'Vacaciones'),
        ('franquicia', 'Franquicia'),
        ('razon_particular', 'Razón Particular'),
        ('comision', 'Comisión'),
    )
    
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_inicio']
    
    def __str__(self):
        return f"{self.agent.name} - {self.record_type} ({self.fecha_inicio} to {self.fecha_fin})"

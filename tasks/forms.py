from django.forms import ModelForm
from .models import Task
from django import forms
from .models import Producto

class Taskform(ModelForm):
    class Meta:
        model = Task
        fields = ['titulo', 'descripcion', 'importante']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un titulo'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen_url']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un nombre'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribe un precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Escribe una descripcion'}),
            'imagen_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Escribe una URL de imagen'}),
        }
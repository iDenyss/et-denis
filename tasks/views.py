from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import Taskform
from .forms import ProductoForm
from .models import Task
from .models import Producto
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'home.html')

def compra_realizada(request):
    return render(request, 'compra_realizada.html')

def anime(request):
    return render(request, 'anime.html')

def formulario(request):
    return render(request, 'formulario.html')

def carrito(request):
    query = request.GET.get("search")
    productos = Producto.objects.all()

    # Filtrado si hay búsqueda
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    # Vista diferente si es admin o usuario
    if request.user.is_authenticated:
        return render(request, 'carrito_admin.html', {"productos": productos, "query": query})
    else:
        return render(request, 'carrito.html', {"productos": productos, "query": query})

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
    })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            #registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'usuario ya existe'
                })
        return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'contrasenas no hacen match'
                })
    
@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, fechaterminado__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, fechaterminado__isnull=False).order_by
    ('-fechaterminado')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': Taskform
        })
    else:
        try:
            form = Taskform(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save() 
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': Taskform,
            'error': 'please coloca datos validos'
        })

@login_required
def create_producto(request):
    if request.method == 'GET':
        return render(request, 'create_producto.html', {
            'form': ProductoForm()
        })
    else:
        try:
            form = ProductoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('carrito')  # Cambia por la URL que corresponda
            else:
                return render(request, 'create_producto.html', {
                    'form': form,
                    'error': 'Por favor coloca datos válidos'
                })
        except ValueError:
            return render(request, 'create_producto.html', {
                'form': ProductoForm(),
                'error': 'Ocurrió un error al guardar el producto'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk= task_id, user=request.user)
        form = Taskform(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk= task_id, user=request.user)
            form = Taskform(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form,
            'error': "Error al actualizar la tarea"})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.fechaterminado = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    

@login_required
def update_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'GET':
        form = ProductoForm(instance=producto)
        return render(request, 'update_producto.html', {'form': form, 'producto': producto})
    else:
        try:
            form = ProductoForm(request.POST, instance=producto)
            if form.is_valid():
                form.save()
                return redirect('carrito_admin')  # Cambia por la URL que corresponda
            else:
                return render(request, 'update_producto.html', {
                    'form': form,
                    'producto': producto,
                    'error': 'Por favor coloca datos válidos'
                })
        except ValueError:
            return render(request, 'update_producto.html', {
                'form': ProductoForm(instance=producto),
                'producto': producto,
                'error': 'Ocurrió un error al actualizar el producto'
            })

@login_required
def delete_producto(request, codigo):
    producto = get_object_or_404(Producto, codigo=codigo)
    if request.method == 'POST':
        producto.delete()
        return redirect('carrito_admin')  # Cambia por la URL que corresponda
    return render(request, 'delete_producto_confirm.html', {'producto': producto})

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
          'form': AuthenticationForm
        }) 
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
             return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username o password es incorrecto'
            }) 
        else:
            login(request, user)
            return redirect('tasks')
        
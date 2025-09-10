from django.contrib import admin
from .models import Task
from .models import Producto

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("creado", )

class ProductoAdmin(admin.ModelAdmin):  
    list_display = ("nombre", "precio", "descripcion")  # Display these fields in the admin list view
    search_fields = ("nombre", )  # Add a search box for the 'nombre' field

# Register your models here.
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Task, TaskAdmin)

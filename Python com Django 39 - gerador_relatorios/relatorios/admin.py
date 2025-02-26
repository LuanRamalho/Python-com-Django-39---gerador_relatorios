from django.contrib import admin
from .models import Servico

# Administrador do modelo Servico
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'data_servico')  # Exibe nome, categoria, preço e data de serviço
    list_filter = ('categoria', 'data_servico')  # Filtro de categorias e data
    search_fields = ('nome', 'categoria')  # Permite a pesquisa por nome e categoria
    ordering = ('-data_servico',)  # Ordena por data de serviço de forma decrescente
    
    # Exibe os campos para edição no form de administração
    fieldsets = (
        (None, {
            'fields': ('nome', 'categoria', 'preco', 'data_servico')
        }),
    )

# Registra o modelo e o admin
admin.site.register(Servico, ServicoAdmin)

from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'categoria', 'preco', 'data_servico']
        widgets = {
            'data_servico': forms.DateInput(attrs={'type': 'date'})
        }

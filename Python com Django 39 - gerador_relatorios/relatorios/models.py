from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    data_servico = models.DateField()

    def __str__(self):
        return f"{self.nome} - {self.categoria}"

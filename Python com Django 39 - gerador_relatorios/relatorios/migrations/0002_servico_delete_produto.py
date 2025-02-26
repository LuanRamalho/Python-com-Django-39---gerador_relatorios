# Generated by Django 5.1.2 on 2025-02-26 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('relatorios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_servico', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='Produto',
        ),
    ]

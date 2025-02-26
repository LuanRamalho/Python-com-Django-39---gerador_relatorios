from django.shortcuts import render, redirect
from .models import Servico
from .forms import ServicoForm
from django.http import HttpResponse
import csv
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Página inicial com o formulário
def formulario(request):
    if request.method == "POST":
        form = ServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('relatorio')
    else:
        form = ServicoForm()
    return render(request, 'relatorios/formulario.html', {'form': form})

# Página do relatório
def relatorio(request):
    servicos = Servico.objects.all()
    return render(request, 'relatorios/relatorio.html', {'servicos': servicos})

# Função para exportar para Excel
def exportar_excel(request):
    # Obtém os dados dos serviços
    servicos = Servico.objects.all()
    
    # Criando um buffer em memória
    buffer = BytesIO()

    # Criando a tabela com os dados dos serviços
    data = []
    for servico in servicos:
        data.append([
            servico.nome,
            servico.categoria,
            f'{servico.preco:.2f}',  # Formatando o preço com duas casas decimais
            servico.data_servico.strftime('%d/%m/%Y')  # Convertendo a data para string formatada
        ])

    # Criando um DataFrame com os dados formatados
    df = pd.DataFrame(data, columns=['Nome', 'Categoria', 'Preço', 'Data do Serviço'])
    
    # Usando o ExcelWriter para salvar o arquivo no buffer
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Escreve os dados no Excel
        df.to_excel(writer, index=False, sheet_name='Relatório de Serviços')

        # Acessa o workbook e o worksheet
        workbook  = writer.book
        worksheet = writer.sheets['Relatório de Serviços']
        
        # Cria um formato de data
        date_format = workbook.add_format({'num_format': 'DD/MM/YYYY'})
        
        # Aplica o formato de data para a coluna de datas (a coluna 'Data do Serviço' é a última)
        data_column_index = df.columns.get_loc('Data do Serviço')
        
        # Aplica o formato para a coluna de data
        for row_num in range(1, len(df) + 1):
            # Convertendo a data para string antes de escrever
            date_value = df.iloc[row_num - 1]['Data do Serviço']
            worksheet.write_string(row_num, data_column_index, date_value, date_format)
        
        # Ajustando a largura das colunas para facilitar a visualização
        for i, col in enumerate(df.columns):
            max_length = max(df[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, max_length)

    buffer.seek(0)  # Volta para o início do buffer para leitura

    # Criando a resposta para download
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio_servicos.xlsx'
    
    return response
# Função para exportar para CSV
def exportar_csv(request):
    # Obtém os dados dos serviços
    servicos = Servico.objects.all()
    
    # Criando a resposta HTTP para o CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=relatorio.csv'
    
    # Criando o escritor CSV
    writer = csv.writer(response, delimiter=';')
    
    # Escrevendo o cabeçalho do CSV com a formatação correta
    writer.writerow(['Nome', 'Categoria', 'Preço', 'Data do Serviço'])
    
    # Iterando pelos serviços e escrevendo os dados formatados
    for servico in servicos:
        # Formatando a data para o formato 'DD/MM/YYYY'
        data_formatada = servico.data_servico.strftime('%d/%m/%Y')
        
        # Escrevendo os dados de cada serviço no CSV
        writer.writerow([servico.nome, servico.categoria, f'{servico.preco:.2f}', data_formatada])
    
    return response

# Função para exportar para PDF
def exportar_pdf(request):
    servicos = Servico.objects.all()
    
    # Preparando a resposta HTTP para o PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'

    # Criando o buffer em memória
    buffer = BytesIO()

    # Inicializando o canvas do reportlab
    p = canvas.Canvas(buffer, pagesize=letter)
    
    # Definindo a posição inicial no eixo Y
    y_position = 750

    # Título do relatório
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y_position, "Relatório de Serviços")
    y_position -= 20

    # Desenhando as colunas
    p.setFont("Helvetica-Bold", 10)
    p.drawString(100, y_position, "Nome")
    p.drawString(250, y_position, "Categoria")
    p.drawString(400, y_position, "Preço")
    p.drawString(500, y_position, "Data de Serviço")
    y_position -= 20

    # Preenchendo os dados dos serviços
    p.setFont("Helvetica", 10)
    for servico in servicos:
        p.drawString(100, y_position, servico.nome)
        p.drawString(250, y_position, servico.categoria)
        p.drawString(400, y_position, f"R$ {servico.preco:.2f}")  # Formatando o preço com duas casas decimais
        p.drawString(500, y_position, servico.data_servico.strftime("%d/%m/%Y"))  # Formatando a data
        y_position -= 20

        # Verifica se o espaço acabou na página e adiciona uma nova página
        if y_position < 50:
            p.showPage()
            y_position = 750
            p.setFont("Helvetica-Bold", 10)
            p.drawString(100, y_position, "Nome")
            p.drawString(250, y_position, "Categoria")
            p.drawString(400, y_position, "Preço")
            p.drawString(500, y_position, "Data de Serviço")
            y_position -= 20

    # Finalizando a página
    p.showPage()
    p.save()

    # Enviar o conteúdo PDF como resposta
    buffer.seek(0)
    response.write(buffer.read())
    return response

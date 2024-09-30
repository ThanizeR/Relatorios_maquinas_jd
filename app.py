import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly._subplots as sp
from streamlit_option_menu import option_menu
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import plotly.graph_objects as go
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly.io as pio
from reportlab.lib.colors import black
import textwrap

st.set_page_config("📊Análise de Trabalho", page_icon="", layout="wide")

# Função para carregar o arquivo por tipo de máquina
@st.cache_data
def load_data(file, file_type, encoding='utf-8'):
    try:
        if file_type == "CSV":
            df = pd.read_excel(file, engine='openpyxl')
        return df
    except UnicodeDecodeError:
        st.error(f"Erro: Não foi possível decodificar o arquivo usando o encoding '{encoding}'. "
                 "Verifique o formato do arquivo ou tente novamente com um encoding diferente.")
        
# Lógica para página de Tratores
#st.sidebar.title('Selecione a página:')
#pagina_selecionada = st.sidebar.radio("Selecione a página:", ("Tratores", "Pulverizadores", "Colheitadeira"))

# Função para quebrar linhas dos nomes das máquinas
def wrap_labels(labels, width):
    return ['\n'.join(textwrap.wrap(label, width)) for label in labels]

def generate_pdf_tratores(df_tractors, figures, background_image_first_page_tratores=None, background_image_other_pages=None):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))

    page_width, page_height = landscape(A4)
    x_margin = 60  # Margem lateral
    y_margin = 40  # Margem vertical ajustada para subir o gráfico
    header_space_other_pages = 70  # Espaço para a organização e datas

    # Tamanho do gráfico
    graph_width = page_width - 2 * x_margin  # Largura do gráfico
    graph_height = page_height - header_space_other_pages - 2 * y_margin  # Altura do gráfico

    def set_background(page_num):
        if page_num == 0 and background_image_first_page_tratores:
            background = ImageReader(background_image_first_page_tratores)
        elif background_image_other_pages:
            background = ImageReader(background_image_other_pages)
        else:
            return
        c.drawImage(background, 0, 0, width=page_width, height=page_height)

    # Primeira página (capa)
    set_background(0)
    c.showPage()

    # Segunda página com organização, datas e gráficos
    set_background(1)

    # Adicionando informações da organização e datas na segunda página
    if 'Data de Início' in df_tractors.columns and 'Data Final' in df_tractors.columns and 'Organização' in df_tractors.columns:
        data_inicio = pd.to_datetime(df_tractors['Data de Início'].iloc[0])
        data_final = pd.to_datetime(df_tractors['Data Final'].iloc[0])
        organizacao = df_tractors['Organização'].iloc[0]

        # Texto à esquerda com espaçamento como dois Tabs
        c.setFont("Helvetica", 10)
        c.drawString(x_margin - 20, page_height - 40, f"Organização: {organizacao}")
        c.drawString(x_margin - 20, page_height - 55, f"Data de Início: {data_inicio.strftime('%d/%m/%Y')}")
        c.drawString(x_margin - 20, page_height - 70, f"Data Final: {data_final.strftime('%d/%m/%Y')}")

    page_num = 1
    graph_index = 0

    while graph_index < len(figures):
        fig = figures[graph_index]

        if not isinstance(fig, plt.Figure):
            print(f"Skipping non-Matplotlib figure: {type(fig)}")
            continue

        # Salvar gráfico como imagem
        img_data = BytesIO()
        fig.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)

        # Centralizar o gráfico e movê-lo um pouco mais para cima
        c.drawImage(ImageReader(img_data), x_margin, y_margin + 20, width=graph_width, height=graph_height)  # Aumentar para subir
        graph_index += 1

        if graph_index < len(figures):
            c.showPage()
            page_num += 1
            set_background(page_num)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Caminho para as imagens de fundo
background_image_first_page_tratores = 'background_pdf_first_page_tratores.jpg'
background_image_other_pages = 'background_pdf_other_pages.jpg'

def generate_pdf_pulverizador(df_sprayers, figures, background_image_first_page_pulverizador=None, background_image_other_pages=None):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))

    page_width, page_height = landscape(A4)
    x_margin = 60  # Margem lateral
    y_margin = 40  # Margem vertical ajustada para subir o gráfico
    header_space_other_pages = 70  # Espaço para a organização e datas

    # Tamanho do gráfico
    graph_width = page_width - 2 * x_margin  # Largura do gráfico
    graph_height = page_height - header_space_other_pages - 2 * y_margin  # Altura do gráfico

    def set_background(page_num):
        if page_num == 0 and background_image_first_page_pulverizador:
            background = ImageReader(background_image_first_page_pulverizador)
        elif background_image_other_pages:
            background = ImageReader(background_image_other_pages)
        else:
            return
        c.drawImage(background, 0, 0, width=page_width, height=page_height)

    # Primeira página (capa)
    set_background(0)
    c.showPage()

    # Segunda página com organização, datas e gráficos
    set_background(1)

    # Adicionando informações da organização e datas na segunda página
    if 'Data de Início' in df_sprayers.columns and 'Data Final' in df_sprayers.columns and 'Organização' in df_sprayers.columns:
        data_inicio = pd.to_datetime(df_sprayers['Data de Início'].iloc[0])
        data_final = pd.to_datetime(df_sprayers['Data Final'].iloc[0])
        organizacao = df_sprayers['Organização'].iloc[0]

        # Texto à esquerda com espaçamento como dois Tabs
        c.setFont("Helvetica", 10)
        c.drawString(x_margin - 20, page_height - 40, f"Organização: {organizacao}")
        c.drawString(x_margin - 20, page_height - 55, f"Data de Início: {data_inicio.strftime('%d/%m/%Y')}")
        c.drawString(x_margin - 20, page_height - 70, f"Data Final: {data_final.strftime('%d/%m/%Y')}")

    page_num = 1
    graph_index = 0

    while graph_index < len(figures):
        fig = figures[graph_index]

        if not isinstance(fig, plt.Figure):
            print(f"Skipping non-Matplotlib figure: {type(fig)}")
            continue

        # Salvar gráfico como imagem
        img_data = BytesIO()
        fig.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)

        # Centralizar o gráfico e movê-lo um pouco mais para cima
        c.drawImage(ImageReader(img_data), x_margin, y_margin + 20, width=graph_width, height=graph_height)  # Aumentar para subir
        graph_index += 1

        if graph_index < len(figures):
            c.showPage()
            page_num += 1
            set_background(page_num)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Caminho para as imagens de fundo
background_image_first_page_pulverizador = 'background_pdf_first_page_pulverizador.jpg'

def generate_pdf_colheitadeira(df_colheitadeira, figures, background_image_first_page_colheitadeira=None, background_image_other_pages=None):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))

    page_width, page_height = landscape(A4)
    x_margin = 60  # Margem lateral
    y_margin = 40  # Margem vertical ajustada para subir o gráfico
    header_space_other_pages = 70  # Espaço para a organização e datas

    # Tamanho do gráfico
    graph_width = page_width - 2 * x_margin  # Largura do gráfico
    graph_height = page_height - header_space_other_pages - 2 * y_margin  # Altura do gráfico

    def set_background(page_num):
        if page_num == 0 and background_image_first_page_colheitadeira:
            background = ImageReader(background_image_first_page_colheitadeira)
        elif background_image_other_pages:
            background = ImageReader(background_image_other_pages)
        else:
            return
        c.drawImage(background, 0, 0, width=page_width, height=page_height)

    # Primeira página (capa)
    set_background(0)
    c.showPage()

    # Segunda página com organização, datas e gráficos
    set_background(1)

    # Adicionando informações da organização e datas na segunda página
    if 'Data de Início' in df_colheitadeira.columns and 'Data Final' in df_colheitadeira.columns and 'Organização' in df_colheitadeira.columns:
        data_inicio = pd.to_datetime(df_colheitadeira['Data de Início'].iloc[0])
        data_final = pd.to_datetime(df_colheitadeira['Data Final'].iloc[0])
        organizacao = df_colheitadeira['Organização'].iloc[0]

        # Texto à esquerda com espaçamento como dois Tabs
        c.setFont("Helvetica", 10)
        c.drawString(x_margin - 20, page_height - 40, f"Organização: {organizacao}")
        c.drawString(x_margin - 20, page_height - 55, f"Data de Início: {data_inicio.strftime('%d/%m/%Y')}")
        c.drawString(x_margin - 20, page_height - 70, f"Data Final: {data_final.strftime('%d/%m/%Y')}")

    page_num = 1
    graph_index = 0

    while graph_index < len(figures):
        fig = figures[graph_index]

        if not isinstance(fig, plt.Figure):
            print(f"Skipping non-Matplotlib figure: {type(fig)}")
            continue

        # Salvar gráfico como imagem
        img_data = BytesIO()
        fig.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)

        # Centralizar o gráfico e movê-lo um pouco mais para cima
        c.drawImage(ImageReader(img_data), x_margin, y_margin + 20, width=graph_width, height=graph_height)  # Aumentar para subir
        graph_index += 1

        if graph_index < len(figures):
            c.showPage()
            page_num += 1
            set_background(page_num)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Caminho para as imagens de fundo
background_image_first_page_colheitadeira = 'background_pdf_first_page_colheitadeira.jpg'


# Menu dropdown na barra superior
selected = option_menu(
    menu_title=None,  # Título do menu, None para esconder
    options=["🌱Tratores", "🌱Pulverizadores", "🌱Colheitadeira"],  # Opções do menu
    icons=['tractor', 'spray-can', 'a'],  # Ícones para cada opção
    menu_icon="cast",  # Ícone do menu
    default_index=0,  # Índice padrão
    orientation="horizontal",  # Orientação horizontal
)

# Lógica para exibir o conteúdo com base na opção selecionada
if selected == "🌱Tratores":
    pass
elif selected == "🌱Pulverizadores":
    pass
elif selected == "🌱Colheitadeira":
    pass

if selected == "🌱Tratores":
    st.subheader("Tratores")
    col1,col2,col3=st.columns(3)
    # Seleção do tipo de arquivo e upload
    file_type_tractors = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_tractors = st.file_uploader(f"Escolha um arquivo {file_type_tractors} para Tratores", type=["csv", "xlsx"])

    if uploaded_file_tractors is not None:
        df_tractors = load_data(uploaded_file_tractors, file_type_tractors)

        if df_tractors is not None:
            st.subheader('Dados do Arquivo Carregado para Tratores')
            # Exibir data de início e data final
            if 'Data de Início' in df_tractors.columns and 'Data Final' in df_tractors.columns and 'Organização' in df_tractors.columns:
                    data_inicio = pd.to_datetime(df_tractors['Data de Início'].iloc[0])
                    data_final = pd.to_datetime(df_tractors['Data Final'].iloc[0])
                    organização = df_tractors['Organização'].iloc[0]

                    col1, col2, col3 = st.columns(3)
                    col1.write(f"Organização: {organização}")
                    col2.write(f"Data de Início: {data_inicio}")
                    col3.write(f"Data Final: {data_final}")
                    

                    # Exibir logo
                    #st.image(Image.open('C:\Users\ThanizeRodrigues-Alv\OneDrive - Alvorada Sistemas Agrícolas Ltda\Área de Trabalho\Thanize\códigos\logo.jpg'), width=200)

                    # Criar lista de datas
                    dates = pd.date_range(start=data_inicio, end=data_final)

                    # Criar dicionário para cores
                    colors = {
                        'Event': 'rgb(31, 119, 180)',
                        'Other Event': 'rgb(255, 127, 14)'
                    }

            # Definir os dados
            selected_columns_hrmotor = ["Máquina", "Horas de Operação do Motor Período (h)"]
            df_selected_tractors_hrmotor = df_tractors[selected_columns_hrmotor].copy()

            # Ordenar o DataFrame com base nas horas de operação do motor usando sort_values
            df_selected_tractors_hrmotor = df_selected_tractors_hrmotor.sort_values(by="Horas de Operação do Motor Período (h)", ascending=False)

            # Configurar o gráfico
            fig_hrmotor, ax_hrmotor = plt.subplots(figsize=(12, 8))

            # Extrair dados para plotagem
            maquinas_tractors_hrmotor = df_selected_tractors_hrmotor["Máquina"]
            horas_operacao_hrmotor = df_selected_tractors_hrmotor["Horas de Operação do Motor Período (h)"]
            wrapped_labels = wrap_labels(maquinas_tractors_hrmotor, width=10)  # Ajuste a largura conforme necessário

            # Ajustar a altura das barras dinamicamente
            bar_height_hrmotor = 0.4
            if len(maquinas_tractors_hrmotor) == 1:
                bar_height_hrmotor = 0.2  # Barra mais fina

            # Plotar barras horizontais com cor verde musgo claro
            bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=bar_height_hrmotor, color='green')
            labels_hrmotor = ['Hr de operação']

            # Adicionar os números de horas formatados no final de cada barra
            for bar, hora in zip(bars, horas_operacao_hrmotor):
                ax_hrmotor.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                va='center', ha='left', fontsize=10, fontweight='bold')

            # Configurar os eixos e título
            ax_hrmotor.set_xlabel('')
            ax_hrmotor.set_ylabel('')
            ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')
            ax_hrmotor.set_yticklabels(wrapped_labels)

            # Centralizar a barra única
            if len(maquinas_tractors_hrmotor) == 1:
                ax_hrmotor.set_ylim(-0.5, 0.5)  # Centralizar a barra no meio do gráfico

            # Adicionar legenda única para Horas de Operação
            ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

            # Mostrar o gráfico
            col8, col9 = st.columns(2)
            col8.pyplot(fig_hrmotor)
            #######################################################################################
            # Definir as colunas principais e opcionais para análise de utilização
            selected_columns_utilizacao = ["Máquina"]

            # Verificar se as colunas opcionais existem e adicioná-las
            if "Utilização (Agricultura) Trabalho (%)" in df_tractors.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Trabalho (%)")

            if "Utilização (Agricultura) Transporte (%)" in df_tractors.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Transporte (%)")

            if "Utilização (Agricultura) Marcha Lenta (%)" in df_tractors.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Marcha Lenta (%)")

            if "Utilização (Agricultura) Ocioso (%)" in df_tractors.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Ocioso (%)")

            # Selecionar os dados com as colunas presentes
            df_selected_tractors_utilizacao = df_tractors[selected_columns_utilizacao].copy()

            # Nomes das máquinas e porcentagens de utilização
            maquinas_tractors = df_selected_tractors_utilizacao["Máquina"]
            velocidades_total_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].sum(axis=1)
            velocidades_percentual_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].div(velocidades_total_tractors, axis=0) * 100
            wrapped_labels = wrap_labels(maquinas_tractors, width=10)  # Ajuste a largura conforme necessário

            # Ajustar a altura das barras dinamicamente
            bar_height_utilizacao = 0.6
            if len(maquinas_tractors) == 1:
                bar_height_utilizacao = 0.2  # Barra mais fina

            bar_positions_tractors_utilizacao = np.arange(len(maquinas_tractors))

            # Plotar gráfico de barras horizontais para % de Utilização
            fig_utilizacao, ax_utilizacao = plt.subplots(figsize=(12, 8))

            # Definir as cores e labels dinamicamente com base nas colunas disponíveis
            colors_utilizacao = []
            labels_utilizacao = []

            if "Utilização (Agricultura) Trabalho (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:green')
                labels_utilizacao.append('Trabalhando')

            if "Utilização (Agricultura) Transporte (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:gray')
                labels_utilizacao.append('Transporte')

            if "Utilização (Agricultura) Marcha Lenta (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:orange')
                labels_utilizacao.append('Marcha Lenta')

            if "Utilização (Agricultura) Ocioso (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:orange')
                labels_utilizacao.append('Ocioso')

            # Plotar as barras horizontais combinadas para cada máquina (utilização)
            for i, (maquina, row) in enumerate(zip(maquinas_tractors, velocidades_percentual_tractors.values)):
                left = 0
                for j, (percent, color) in enumerate(zip(row, colors_utilizacao)):
                    ax_utilizacao.barh(bar_positions_tractors_utilizacao[i], percent, height=bar_height_utilizacao, 
                                    left=left, label=labels_utilizacao[j] if i == 0 else "", color=color)
                    ax_utilizacao.text(left + percent / 2, bar_positions_tractors_utilizacao[i], 
                                    f'{percent:.1f}%', ha='center', va='center', color='black', fontsize=10, fontweight='bold')
                    left += percent

            # Configurar os eixos e título
            ax_utilizacao.set_xlabel('')
            ax_utilizacao.set_yticks(bar_positions_tractors_utilizacao)
            ax_utilizacao.set_yticklabels(wrapped_labels)
            ax_utilizacao.set_xticks([])  
            ax_utilizacao.set_title('% de Utilização por Máquina - Tratores')

            # Centralizar a barra única
            if len(maquinas_tractors) == 1:
                ax_utilizacao.set_ylim(-0.5, 0.5)  # Centralizar a barra no meio do gráfico

            # Adicionar legenda única para Utilização
            ax_utilizacao.legend(labels_utilizacao, loc='upper right', bbox_to_anchor=(1.21, 1.0))

            # Mostrar o gráfico de Utilização
            col4, col5 = st.columns(2)
            col4.pyplot(fig_utilizacao)


            #############################################################
           # Verificar se as colunas existem no DataFrame antes de selecioná-las
            colunas_disponiveis = ["Máquina", 
                                "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                                "Fator de Carga Média do Motor (Ag) Transporte (%)"]

            # Adicionar colunas opcionais apenas se existirem
            if "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)" in df_tractors.columns:
                colunas_disponiveis.append("Fator de Carga Média do Motor (Ag) Marcha Lenta (%)")
            if "Fator de Carga Média do Motor (Ag) Ocioso (%)" in df_tractors.columns:
                colunas_disponiveis.append("Fator de Carga Média do Motor (Ag) Ocioso (%)")

            # Filtrar o DataFrame para as colunas de fator de carga disponíveis
            df_selected_tractors_fator = df_tractors[colunas_disponiveis].copy()

            # Identificar linhas onde os valores são todos zero
            zeros_mask = (df_selected_tractors_fator.iloc[:, 1:] == 0).all(axis=1)

            # Separar máquinas com todos os valores zero e as que têm valores diferentes de zero
            df_non_zeros = df_selected_tractors_fator[~zeros_mask]
            df_zeros = df_selected_tractors_fator[zeros_mask]

            # Concatenar os DataFrames, primeiro os não-zero, depois os zero
            df_selected_tractors_fator = pd.concat([df_non_zeros, df_zeros])

            # Nomes das máquinas e porcentagens de fator de carga
            maquinas_tractors_fator = df_selected_tractors_fator["Máquina"]
            fatores_percentual_tractors = df_selected_tractors_fator.iloc[:, 1:] * 100

            # Plotar gráfico de barras horizontais para % de Fator de Carga
            fig_fator, ax_fator = plt.subplots(figsize=(12, 8))

            # Definir as cores e labels dinamicamente
            colors_fator = []
            labels_fator = []

            if "Fator de Carga Média do Motor (Ag) Trabalho (%)" in df_selected_tractors_fator.columns:
                colors_fator.append('tab:green')
                labels_fator.append('Trabalhando')

            if "Fator de Carga Média do Motor (Ag) Transporte (%)" in df_selected_tractors_fator.columns:
                colors_fator.append('tab:gray')
                labels_fator.append('Transporte')

            if "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)" in df_selected_tractors_fator.columns:
                colors_fator.append('tab:orange')
                labels_fator.append('Marcha Lenta')

            if "Fator de Carga Média do Motor (Ag) Ocioso (%)" in df_selected_tractors_fator.columns:
                colors_fator.append('tab:orange')
                labels_fator.append('Ocioso')

            bar_height_fator = 0.32  # Altura das barras de Fator de Carga
            bar_positions_tractors_fator = np.arange(len(maquinas_tractors_fator)) * 1.5  # Aumentar o espaçamento
            offset = 0.35  # Espaçamento entre as categorias dentro de cada máquina

            # Iterar sobre as categorias para criar as barras
            for j in range(len(labels_fator)):
                # Desenhar barras apenas para as máquinas que não têm todos os valores zerados
                ax_fator.barh(bar_positions_tractors_fator[:len(df_non_zeros)] + j * offset, 
                            fatores_percentual_tractors.iloc[:len(df_non_zeros), j], 
                            height=bar_height_fator, 
                            label=labels_fator[j], 
                            color=colors_fator[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_tractors_fator[:len(df_non_zeros)])):
                    percent = fatores_percentual_tractors.iloc[i, j]
                    ax_fator.text(fatores_percentual_tractors.iloc[i, j] + 2,  
                                bar_positions_tractors_fator[i] + j * offset, 
                                f'{percent:.1f}%', 
                                ha='left', 
                                va='center', 
                                color='black', 
                                fontsize=10, 
                                fontweight='bold')

            # Configurar os eixos e título
            ax_fator.set_xlabel('% de Fator de Carga')
            ax_fator.set_yticks(bar_positions_tractors_fator + offset)
            ax_fator.set_yticklabels(maquinas_tractors_fator)  # Nomes das máquinas
            ax_fator.set_title('% de Fator de Carga por Máquina - Tratores')

            # Definir os limites e marcas do eixo x
            ax_fator.set_xlim([0, 100])
            ax_fator.set_xticks([0, 50, 100])
            ax_fator.set_xticklabels(['0%', '50%', '100%'])  # Valores do eixo x

            # Adicionar legenda única para Fator de Carga
            ax_fator.legend(labels_fator, loc='upper right', bbox_to_anchor=(1.23, 1.0))

            # Mostrar o gráfico de Fator de Carga
            col5.pyplot(fig_fator)


            ################################################################################################
            # Definir colunas para análise de taxa média de combustível
            selected_columns_combust = [
                "Máquina",
                "Taxa Média de Combustível (Ag) Trabalhando (l/h)",
                "Taxa Média de Combustível (Ag) Transporte (l/h)",
                "Taxa Média de Combustível (Ag) Ocioso (l/h)"
            ]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_tractors_combust = df_tractors[selected_columns_combust].copy()

            # Nomes das máquinas e porcentagens
            maquinas_tractors_combust = df_selected_tractors_combust["Máquina"]
            percentual_tractors_combust = df_selected_tractors_combust.iloc[:, 1:]
            wrapped_labels = wrap_labels(maquinas_tractors_combust, width=10)

            # Plotar gráfico de barras verticais
            fig_combust, ax_combust = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_combust = ['tab:green', 'tab:gray', 'tab:orange']
            labels_combust = ['Trabalhando (l/h)', 'Transporte (l/h)', 'Ocioso (l/h)']
            bar_width_combust = 0.2  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_tractors_combust = np.arange(len(maquinas_tractors_combust))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_tractors_combust, percentual_tractors_combust.values)):
                for j, (percent, color) in enumerate(zip(row, colors_combust)):
                    ax_combust.bar(bar_positions_tractors_combust[i] + j * bar_width_combust, percent, width=bar_width_combust,
                                label=labels_combust[j] if i == 0 else "", color=color)
                    ax_combust.text(bar_positions_tractors_combust[i] + j * bar_width_combust, percent + 1,
                                    f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

            # Configurar rótulos e título
            ax_combust.set_xlabel('')  # Eixo X em negrito
            ax_combust.set_ylabel('')  # Eixo Y em negrito
            ax_combust.set_xticks(bar_positions_tractors_combust + bar_width_combust)
            ax_combust.set_xticklabels(wrapped_labels)  # Rótulos em negrito
            ax_combust.set_title('Consumo de Combustível')  # Título em negrito

            # Definir os limites do eixo Y de forma adaptativa
            max_value_combust = percentual_tractors_combust.max().max()  # Obtém o valor máximo dos dados
            if max_value_combust <= 15:
                y_limit_combust = 15
            elif max_value_combust <= 25:
                y_limit_combust = 25
            elif max_value_combust <= 50:
                y_limit_combust = 50
            elif max_value_combust <= 75:
                y_limit_combust = 75
            else:
                y_limit_combust = 100

            ax_combust.set_ylim(0, y_limit_combust)  # Define o limite do eixo Y

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, y_limit_combust + 1, 10)  # Ajusta conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_combust.set_yticks(yticks_values)
            ax_combust.set_yticklabels(yticks_labels)  # Rótulos do eixo Y em negrito

            # Adicionar legenda única
            ax_combust.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))  # Legenda em negrito

            # Mostrar o gráfico
            col6, col7 = st.columns(2)
            col6.pyplot(fig_combust)

        ###################################################################################################

            # Definir colunas para análise de rotação média do motor
            selected_columns_rotacao = ["Máquina", 
                                        "Rotação Média do Motor Trabalhando (rpm)",
                                        "Rotação Média do Motor Transporte (rpm)",
                                        "Rotação Média do Motor Ocioso (rpm)"]

            # Filtrar o DataFrame para as colunas de rotação selecionadas
            df_selected_tractors_rotacao = df_tractors[selected_columns_rotacao].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e rotação média
            maquinas_tractors_rotacao = df_selected_tractors_rotacao["Máquina"]
            rotacoes_tractors = df_selected_tractors_rotacao.iloc[:, 1:]
            wrapped_labels = wrap_labels(maquinas_tractors_rotacao, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras horizontais para rotação média
            fig_rotacao, ax_rotacao = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

            # Cores e labels para as barras de rotação média
            colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_rotacao = ['Trabalhando', 'Transporte', 'Ocioso']
            bar_height_rotacao = 0.32  # Altura das barras de rotação média
            bar_positions_rotacao = np.arange(len(maquinas_tractors_rotacao)) * 1.5  # Aumentar o fator de multiplicação para espaçamento maior
            offset = 0.35  # Espaçamento entre as categorias dentro de cada máquina

            # Iterar sobre as categorias para criar as barras
            for j in range(len(labels_rotacao)):
                # Desenhar barras apenas para as máquinas que não têm todos os valores zerados
                ax_rotacao.barh(bar_positions_rotacao[:len(df_selected_tractors_rotacao)] + j * offset, 
                                rotacoes_tractors.iloc[:, j].fillna(np.nan), 
                                height=bar_height_rotacao, 
                                label=labels_rotacao[j], 
                                color=colors_rotacao[j])

                # Adicionar rótulos às barras na ponta
                for i in range(len(bar_positions_rotacao[:len(df_selected_tractors_rotacao)])):
                    rotacao = rotacoes_tractors.iloc[i, j]
                    if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                        ax_rotacao.text(rotacao + 2,  # Posição na ponta da barra
                                        bar_positions_rotacao[i] + j * offset, 
                                        f'{rotacao:.0f}', 
                                        ha='left', 
                                        va='center', 
                                        color='black', 
                                        fontsize=10, 
                                        fontweight='bold')  # Texto em negrito

            # Configurar os eixos e título
            ax_rotacao.set_xlabel('')
            ax_rotacao.set_yticks(bar_positions_rotacao + offset)
            ax_rotacao.set_yticklabels(wrapped_labels)  # Nomes das máquinas em negrito
            ax_rotacao.set_title('Rotação Média do Motor por Máquina - Tratores')  # Título em negrito

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = rotacoes_tractors.stack().max() if not rotacoes_tractors.empty else 0
            ax_rotacao.set_xlim([0, max_value * 1.1])

            # Adicionar legenda única para rotação média
            ax_rotacao.legend(labels_rotacao, loc='upper right', bbox_to_anchor=(1.2, 1.0))

            # Mostrar o gráfico de rotação média
            col7.pyplot(fig_rotacao)

            ########################################################################################
            # Definir colunas para análise de velocidade média de deslocamento
            selected_columns_desloc = [
                "Máquina", 
                "Velocidade Média de Deslocamento Trabalhando (km/h)",
                "Velocidade Média de Deslocamento (km/h)"
            ]
            df_selected_tractors_desloc = df_tractors[selected_columns_desloc].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_desloc.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e velocidade média de deslocamento
            maquinas_tractors_desloc = df_selected_tractors_desloc["Máquina"]
            desloc_tractors = df_selected_tractors_desloc.iloc[:, 1:]
            wrapped_labels = wrap_labels(maquinas_tractors_desloc, width=10)  # Ajuste a largura conforme necessário
            # Plotar gráfico de barras verticais para velocidade média de deslocamento
            fig_desloc, ax_desloc = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

            # Cores e labels para as barras de velocidade média de deslocamento
            colors_desloc = ['tab:green', 'tab:gray']
            labels_desloc = ['Trabalhando', 'Transporte']
            bar_width = 0.2  # Largura das barras
            bar_positions_desloc = np.arange(len(maquinas_tractors_desloc))

            # Ajustar as posições das barras para que fiquem lado a lado
            for j in range(min(len(labels_desloc), desloc_tractors.shape[1])):  # Verificação para evitar índice fora dos limites
                # Usar np.nan para valores NaN para que apareçam em branco
                ax_desloc.bar(
                    bar_positions_desloc + j * bar_width - bar_width/2, 
                    desloc_tractors.iloc[:, j].fillna(np.nan), 
                    width=bar_width, 
                    label=labels_desloc[j], 
                    color=colors_desloc[j]
                )

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_desloc)):
                    desloc = desloc_tractors.iloc[i, j]
                    if pd.notna(desloc):  # Apenas adicionar texto se não for NaN
                        ax_desloc.text(
                            bar_positions_desloc[i] + j * bar_width - bar_width/2, 
                            desloc + 0.5,  # Ajuste para mover o texto acima da barra
                            f'{desloc:.1f}', 
                            ha='center', 
                            va='bottom', 
                            color='black', 
                            fontsize=10,
                            fontweight='bold'
                        )

           # Configurar os eixos e título
            ax_desloc.set_ylabel('km/h')  # Remover rótulo do eixo Y
            ax_desloc.set_yticks([])  # Remover marcações do eixo Y
            ax_desloc.set_xticks(bar_positions_desloc)
            ax_desloc.set_xticklabels(maquinas_tractors_desloc)
            ax_desloc.set_xticklabels(wrapped_labels)
            ax_desloc.set_title('Velocidade Média de Deslocamento por Máquina - Tratores')

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = desloc_tractors.stack().max() if not desloc_tractors.empty else 0
            ax_desloc.set_ylim([0, max_value * 1.1])

            # Adicionar legenda
            ax_desloc.legend(labels_desloc, loc='upper right', bbox_to_anchor=(1.2, 1.0))

            col9.pyplot(fig_desloc)

            ################################################################

            # Seleciona as colunas de patinagem na ordem exata da planilha
            selected_columns_patinagem = [
                "Máquina", 
                "Tempo de Patinagem das Rodas no Nível 0,00–2,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 2,01–4,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 4,01–6,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 6,01–8,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 8,01-10,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 10,01–12,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 12,01–14,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 14,01–16,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 16,01–18,00% (h)",
                "Tempo de Patinagem das Rodas no Nível 18,01–100,00% (h)"
            ]

            # Copia o DataFrame mantendo a ordem das colunas
            df_selected_patinagem = df_tractors[selected_columns_patinagem].copy()

            # Substitui valores infinitos por NaN
            df_selected_patinagem.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Define máquinas e valores de patinagem
            maquinas = df_selected_patinagem["Máquina"]
            patinagem_values = df_selected_patinagem.iloc[:, 1:]

            # Ajusta os rótulos das máquinas para caberem no gráfico
            wrapped_labels = wrap_labels(maquinas, width=10)

            # Configura o gráfico de barras
            fig_patinagem, ax_patinagem = plt.subplots(figsize=(12, 8))

            # Cores e labels correspondentes
            colors = ['tab:blue', 'tab:red', 'tab:green', 'tab:pink', 'tab:cyan', 'tab:orange', 'tab:brown', 'tab:gray', 'tab:olive', 'tab:purple']
            labels = [
                '0,00–2,00', '2,01–4,00', '4,01–6,00', '6,01–8,00', '8,01–10,00',
                '10,01–12,00', '12,01–14,00', '14,01–16,00', '16,01–18,00', '18,01–100,00'
            ]

            bar_width = 4  # Largura das barras
            space_between_bars = 2  # Espaço entre as barras coloridas
            machine_offset = 4  # Espaço entre cada máquina

            # Gera as barras sem alterar a ordem dos dados
            for i, (maquina, row) in enumerate(zip(maquinas, patinagem_values.values)):
                base_position = i * (len(colors) * (bar_width + space_between_bars) + machine_offset)
                
                for j, (value, color, label) in enumerate(zip(row, colors, labels)):
                    # Arredonda o valor para duas casas decimais
                    value_arredondado = round(value, 2)
                    
                    # Verifica se o valor arredondado é maior ou igual a 0.01 ou igual a 0
                    if value_arredondado >= 0.01 or value_arredondado == 0:
                        bar_position = base_position + j * (bar_width + space_between_bars)
                        ax_patinagem.bar(bar_position, value_arredondado, width=bar_width, label=label if i == 0 else "", color=color)

            # Ajuste da escala do eixo Y para acomodar os valores
            max_value = patinagem_values.max().max()  # Obtém o valor máximo dos dados

            # Definir o limite superior do eixo Y de forma adaptativa
            if max_value <= 20:
                y_limit = 20
            elif max_value <= 30:
                y_limit = 30
            elif max_value <= 50:
                y_limit = 50
            elif max_value <= 75:
                y_limit = 75
            else:
                y_limit = 100

            # Define o limite do eixo Y
            ax_patinagem.set_ylim(0, y_limit)

            # Adicionar linhas horizontais de referência para os valores de y
            y_ticks = np.arange(0, y_limit + 10, 10)  # Gera ticks de 10 em 10 unidades até o máximo
            ax_patinagem.set_yticks(y_ticks)

            for y in y_ticks:
                ax_patinagem.axhline(y, color='gray', linestyle='--', linewidth=0.5)

            # Configurar os eixos e título
            ax_patinagem.set_ylabel('Tempo de Patinagem (h)')
            ax_patinagem.set_xticks([i * (len(colors) * (bar_width + space_between_bars) + machine_offset) + (len(colors) * (bar_width + space_between_bars) - space_between_bars) / 2 for i in range(len(maquinas))])
            ax_patinagem.set_xticklabels(maquinas, rotation=45, ha='right')
            ax_patinagem.set_title('Tempo de Patinagem das Rodas por Máquina - Tratores')
            ax_patinagem.set_xticklabels(wrapped_labels)

            # Adicionar legenda única para Patinagem na ordem correta
            handles, labels = zip(*sorted(zip(ax_patinagem.get_legend_handles_labels()[0], labels), key=lambda x: labels.index(x[1])))
            ax_patinagem.legend(handles, labels, loc='upper right', bbox_to_anchor=(1.25, 1.0))

            # Exibe o gráfico no Streamlit
            st.pyplot(fig_patinagem)


            #########################################################################################################

            if st.button('Gerar PDF para Tratores'):
                        figures = [fig_hrmotor, fig_utilizacao, fig_fator, fig_combust, fig_rotacao,fig_desloc, fig_patinagem]  
                        pdf_buffer = generate_pdf_tratores( df_tractors, figures, background_image_first_page_tratores, background_image_other_pages)
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_buffer,
                            file_name="relatorio_tratores.pdf",
                            mime="application/pdf"
                        )
# Lógica para Pulverizadores
elif selected == "🌱Pulverizadores":
    st.subheader("Pulverizadores")
    file_type_sprayers = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_sprayers = st.file_uploader(f"Escolha um arquivo {file_type_sprayers} para Pulverizadores", type=["csv", "xlsx"])

    if uploaded_file_sprayers is not None:
        df_sprayers = load_data(uploaded_file_sprayers, file_type_sprayers)

        if df_sprayers is not None:
            st.subheader('Dados do Arquivo Carregado para Pulverizadores')
           # st.write(df_sprayers)
            # Exibir data de início e data final
            if 'Data de Início' in df_sprayers.columns and 'Data Final' in df_sprayers.columns and 'Organização' in df_sprayers.columns:
                    data_inicio = pd.to_datetime(df_sprayers['Data de Início'].iloc[0])
                    data_final = pd.to_datetime(df_sprayers['Data Final'].iloc[0])
                    organização = df_sprayers['Organização'].iloc[0]

                    col1, col2, col3 = st.columns(3)
                    col1.write(f"Organização: {organização}")
                    col2.write(f"Data de Início: {data_inicio}")
                    col3.write(f"Data Final: {data_final}")
                    

                    # Exibir logo
                    #st.image(Image.open('C:\Users\ThanizeRodrigues-Alv\OneDrive - Alvorada Sistemas Agrícolas Ltda\Área de Trabalho\Thanize\códigos\logo.jpg'), width=200)

                    # Criar lista de datas
                    dates = pd.date_range(start=data_inicio, end=data_final)

                    # Criar dicionário para cores
                    colors = {
                        'Event': 'rgb(31, 119, 180)',
                        'Other Event': 'rgb(255, 127, 14)'
                    }
                    #####################################################################################################
                    #FAZER DO COMBUSTIVEL
                    # Mostrar o gráfico
                    col4, col5 = st.columns(2)
                    #combustivel
                    selected_columns_colheitadeira_combus = ["Máquina", 
                                    "Taxa Média de Combustível (Ag) Ocioso (l/h)",
                                    "Taxa Média de Combustível (Ag) Trabalhando (l/h)",
                                    "Taxa Média de Combustível (Ag) Transporte (l/h)"
                                    ]

                    # Filtrar o DataFrame para as colunas selecionadas
                    df_selected_colheitadeira_combus = df_sprayers[selected_columns_colheitadeira_combus].copy()

                    # Nomes das máquinas e porcentagens
                    maquinas_colheitadeira_combus = df_selected_colheitadeira_combus["Máquina"]
                    percentual_colheitadeira_combus = df_selected_colheitadeira_combus.iloc[:, 1:] 

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_colheitadeira_combus, width=10)  # Ajuste a largura conforme necessário

                    # Plotar gráfico de barras verticais
                    fig_pulverizador_combus, ax_colheitadeira_combus = plt.subplots(figsize=(12, 8))

                    # Cores e labels para as barras
                    colors_colheitadeira_combus = ['tab:orange', 'tab:green', 'tab:gray']
                    labels_colheitadeira_combus = ['Ocioso l/h', 'Trabalhando l/h', 'Transporte l/h']
                    bar_width_colheitadeira_combus = 0.1  # Largura das barras

                    # Definir posições das barras para cada grupo de dados
                    bar_positions_colheitadeira_combus = np.arange(len(maquinas_colheitadeira_combus))

                    # Plotar as barras verticais combinadas para cada máquina
                    for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_combus, percentual_colheitadeira_combus.values)):
                        for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_combus)):
                            ax_colheitadeira_combus.bar(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent, width=bar_width_colheitadeira_combus, label=labels_colheitadeira_combus[j] if i == 0 else "", color=color)
                            ax_colheitadeira_combus.text(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

                    # Configurar rótulos e título
                    ax_colheitadeira_combus.set_xlabel('Máquinas')  # Texto do eixo x
                    ax_colheitadeira_combus.set_ylabel('(l/h)')  # Texto do eixo y
                    ax_colheitadeira_combus.set_xticks(bar_positions_colheitadeira_combus + bar_width_colheitadeira_combus)
                    ax_colheitadeira_combus.set_xticklabels(maquinas_colheitadeira_combus)
                    ax_colheitadeira_combus.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_colheitadeira_combus.set_title('Combustivel (l/h)')

                    # Definir as numerações do eixo y
                    yticks_values = np.arange(0, 51, 10)  # Ajuste conforme necessário
                    yticks_labels = [f'{val:.1f}' for val in yticks_values]
                    ax_colheitadeira_combus.set_yticks(yticks_values)
                    ax_colheitadeira_combus.set_yticklabels(yticks_labels)

                    # Adicionar legenda única
                    ax_colheitadeira_combus.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
                    col4.pyplot(fig_pulverizador_combus)
                    #####################################################################################################
                    
                    # Definir colunas para análise de fator de carga média do pulverizador
                    selected_columns_pulverizador_factor = ["Máquina", 
                                                            "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)",
                                                            "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                                                            "Fator de Carga Média do Motor (Ag) Transporte (%)"]

                    # Filtrar o DataFrame para as colunas selecionadas
                    df_selected_pulverizador_factor = df_sprayers[selected_columns_pulverizador_factor].copy()

                    # Identificar linhas onde os valores são todos zero
                    zeros_mask = (df_selected_pulverizador_factor.iloc[:, 1:] == 0).all(axis=1)

                    # Separar máquinas com todos os valores zero e as que têm valores diferentes de zero
                    df_non_zeros = df_selected_pulverizador_factor[~zeros_mask]
                    df_zeros = df_selected_pulverizador_factor[zeros_mask]

                    # Concatenar os DataFrames, primeiro os não-zero, depois os zero
                    df_selected_pulverizador_factor = pd.concat([df_non_zeros, df_zeros])

                    # Nomes das máquinas e porcentagens de fator de carga
                    maquinas_pulverizador_factor = df_selected_pulverizador_factor["Máquina"]
                    percentual_pulverizador_factor = df_selected_pulverizador_factor.iloc[:, 1:] * 100

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_pulverizador_factor, width=10)  # Ajuste a largura conforme necessário

                    # Plotar gráfico de barras horizontais para % de Fator de Carga
                    fig_pulverizador_factor, ax_pulverizador_factor = plt.subplots(figsize=(12, 8))

                    # Cores e labels para as barras de Fator de Carga
                    colors_pulverizador_factor = ['tab:green', 'tab:blue', 'tab:red']
                    labels_pulverizador_factor = ['Marcha Lenta (%)', 'Trabalho (%)', 'Transporte (%)']
                    bar_height_pulverizador_factor = 0.32  # Altura das barras de Fator de Carga
                    bar_positions_pulverizador_factor = np.arange(len(maquinas_pulverizador_factor)) * 1.5  # Aumentar o fator de multiplicação para espaçamento maior
                    offset = 0.35  # Espaçamento entre as categorias dentro de cada máquina

                    # Iterar sobre as categorias para criar as barras
                    for j in range(len(labels_pulverizador_factor)):
                        # Desenhar barras apenas para as máquinas que não têm todos os valores zerados
                        ax_pulverizador_factor.barh(bar_positions_pulverizador_factor[:len(df_non_zeros)] + j * offset, 
                                                    percentual_pulverizador_factor.iloc[:len(df_non_zeros), j], 
                                                    height=bar_height_pulverizador_factor, 
                                                    label=labels_pulverizador_factor[j], 
                                                    color=colors_pulverizador_factor[j])

                        # Adicionar rótulos às barras na ponta
                        for i in range(len(bar_positions_pulverizador_factor[:len(df_non_zeros)])):
                            percent = percentual_pulverizador_factor.iloc[i, j]
                            
                            # Verificar se o valor é zero e ajustar a posição do texto
                            if percent == 0:
                                ax_pulverizador_factor.text(2,  # Posição no início da barra se for zero
                                                            bar_positions_pulverizador_factor[i] + j * offset, 
                                                            f'{percent:.1f}%', 
                                                            ha='left', 
                                                            va='center', 
                                                            color='black', 
                                                            fontsize=10, 
                                                            fontweight='bold')
                            else:
                                ax_pulverizador_factor.text(percent + 2,  # Posição na ponta da barra
                                                            bar_positions_pulverizador_factor[i] + j * offset, 
                                                            f'{percent:.1f}%', 
                                                            ha='left', 
                                                            va='center', 
                                                            color='black', 
                                                            fontsize=10, 
                                                            fontweight='bold')

                    # Configurar os eixos e título
                    ax_pulverizador_factor.set_xlabel('')
                    ax_pulverizador_factor.set_yticks(bar_positions_pulverizador_factor + offset)
                    ax_pulverizador_factor.set_yticklabels(wrapped_labels)  # Nomes das máquinas em negrito
                    ax_pulverizador_factor.set_title('Fator de Carga % por Máquina - Pulverizadores')  # Título em negrito

                    # Definir os limites e marcas do eixo x
                    ax_pulverizador_factor.set_xlim([0, 100])
                    ax_pulverizador_factor.set_xticks([0, 50, 100])
                    ax_pulverizador_factor.set_xticklabels(['0%', '50%', '100%'])  # Valores do eixo x em negrito

                    # Adicionar legenda única para Fator de Carga
                    ax_pulverizador_factor.legend(loc='upper right', bbox_to_anchor=(1.23, 1.0))

                    # Mostrar o gráfico de Fator de Carga
                    col5.pyplot(fig_pulverizador_factor)


                    ############################################################################################################
                    # Definir colunas para análise de rotação média do motor
                    selected_columns_rotacao = ["Máquina", 
                                                "Rotação Média do Motor Trabalhando (rpm)",
                                                "Rotação Média do Motor Transporte (rpm)",
                                                "Rotação Média do Motor Ocioso (rpm)"]

                    # Filtrar o DataFrame para as colunas de rotação selecionadas
                    df_selected_rotacao = df_sprayers[selected_columns_rotacao].copy()

                    # Manter linhas com NaN para visualização em branco
                    df_selected_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

                    # Nomes das máquinas e rotação média
                    maquinas_rotacao = df_selected_rotacao["Máquina"]
                    rotacoes = df_selected_rotacao.iloc[:, 1:]

                    # Plotar gráfico de barras horizontais para rotação média
                    fig_pulverizador_rotacao, ax_rotacao = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_rotacao, width=10)  # Ajuste a largura conforme necessário

                    # Cores e labels para as barras de rotação média
                    colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
                    labels_rotacao = ['Trabalhando', 'Transporte', 'Ocioso']
                    bar_height_rotacao = 0.32  # Altura das barras de rotação média
                    bar_positions_rotacao = np.arange(len(maquinas_rotacao)) * 2  # Aumentar o fator de multiplicação para espaçamento maior
                    offset = 0.35  # Espaçamento entre as categorias dentro de cada máquina

                    # Iterar sobre as categorias para criar as barras
                    for j in range(len(labels_rotacao)):
                        # Desenhar barras e garantir que valores NaN sejam visualizados como em branco
                        ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                        rotacoes.iloc[:, j].fillna(np.nan), 
                                        height=bar_height_rotacao, 
                                        label=labels_rotacao[j], 
                                        color=colors_rotacao[j])

                        # Adicionar rótulos às barras
                        for i in range(len(bar_positions_rotacao)):
                            rotacao = rotacoes.iloc[i, j]
                            if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                                ax_rotacao.text(rotacao + 2,  # Ajuste para mover o texto mais para a direita
                                                bar_positions_rotacao[i] + j * offset, 
                                                f'{rotacao:.0f}', 
                                                ha='left', 
                                                va='center', 
                                                color='black', 
                                                fontsize=10,
                                                fontweight='bold')

                    # Configurar os eixos e título
                    ax_rotacao.set_xlabel('')
                    ax_rotacao.set_yticks(bar_positions_rotacao + offset)
                    ax_rotacao.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_rotacao.set_title('Rotação Média do Motor RPM')

                    # Definir os limites e marcas do eixo x
                    max_value = rotacoes.stack().max() if not rotacoes.empty else 0
                    ax_rotacao.set_xlim([0, max_value * 1.1])
                    ax_rotacao.set_xticks([0, max_value * 0.5, max_value])
                    ax_rotacao.set_xticklabels(['0', f'{int(max_value * 0.5)}', f'{int(max_value)}'])

                    # Adicionar legenda única para rotação média
                    ax_rotacao.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))

                    # Mostrar o gráfico de rotação média
                    col6, col7 = st.columns(2)
                    col6.pyplot(fig_pulverizador_rotacao)

                    ##########################################################################################################
                    selected_columns_colheitadeira_autotrac = ["Máquina", 
                               'AutoTrac™ Ativo (%)'
                               ]

                    # Filtrar o DataFrame para as colunas selecionadas
                    df_selected_colheitadeira_autotrac = df_sprayers[selected_columns_colheitadeira_autotrac].copy()

                    # Nomes das máquinas e porcentagens
                    maquinas_colheitadeira_autotrac = df_selected_colheitadeira_autotrac["Máquina"]
                    percentual_colheitadeira_autotrac = df_selected_colheitadeira_autotrac.iloc[:, 1:] *100

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_colheitadeira_autotrac, width=10)  # Ajuste a largura conforme necessário

                    # Plotar gráfico de barras verticais
                    fig_pulverizador_autotrac, ax_colheitadeira_autotrac = plt.subplots(figsize=(12, 8))

                    # Cores e labels para as barras
                    colors_colheitadeira_autotrac = ['tab:blue']
                    labels_colheitadeira_autotrac = [ 'AutoTrac™ Ativo (%)']
                    bar_width_colheitadeira_autotrac = 0.2  # Largura das barras

                    # Definir posições das barras para cada grupo de dados
                    bar_positions_colheitadeira_autotrac = np.arange(len(maquinas_colheitadeira_autotrac))

                    # Plotar as barras verticais combinadas para cada máquina
                    for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_autotrac, percentual_colheitadeira_autotrac.values)):
                        for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_autotrac)):
                            ax_colheitadeira_autotrac.bar(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent, width=bar_width_colheitadeira_autotrac, label=labels_colheitadeira_autotrac[j] if i == 0 else "", color=color)
                            ax_colheitadeira_autotrac.text(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

                    # Configurar rótulos e título
                    ax_colheitadeira_autotrac.set_xlabel('Máquinas')  # Texto do eixo x
                    ax_colheitadeira_autotrac.set_ylabel('')  # Texto do eixo y
                    ax_colheitadeira_autotrac.set_xticks(bar_positions_colheitadeira_autotrac + bar_width_colheitadeira_autotrac)
                    ax_colheitadeira_autotrac.set_xticklabels(maquinas_colheitadeira_autotrac)
                    ax_colheitadeira_autotrac.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_colheitadeira_autotrac.set_title('Uso do Autotrac %')

                    # Definir as numerações do eixo y
                    yticks_values = np.arange(0, 201, 10)  # Ajuste conforme necessário
                    yticks_labels = [f'{val:.1f}' for val in yticks_values]
                    ax_colheitadeira_autotrac.set_yticks(yticks_values)
                    ax_colheitadeira_autotrac.set_yticklabels(yticks_labels)

                    # Adicionar legenda única
                    ax_colheitadeira_autotrac.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
                    col7.pyplot(fig_pulverizador_autotrac)

                    ##############################################################################################################################
                    selected_columns_colheitadeira_desloc = ["Máquina", 
                               "Velocidade Média de Deslocamento Trabalhando (km/h)",
                               "Velocidade Média de Deslocamento Transporte (km/h)"	
                               ]

                    # Filtrar o DataFrame para as colunas selecionadas
                    df_selected_colheitadeira_desloc = df_sprayers[selected_columns_colheitadeira_desloc].copy()

                    # Nomes das máquinas e porcentagens
                    maquinas_colheitadeira_desloc = df_selected_colheitadeira_desloc["Máquina"]
                    percentual_colheitadeira_desloc = df_selected_colheitadeira_desloc.iloc[:, 1:] 

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_colheitadeira_desloc, width=10)  # Ajuste a largura conforme necessário

                    # Plotar gráfico de barras verticais
                    fig_pulverizador_desloc, ax_colheitadeira_desloc = plt.subplots(figsize=(12, 8))

                    # Cores e labels para as barras
                    colors_colheitadeira_desloc = ['tab:green', 'tab:gray']
                    labels_colheitadeira_desloc = [ 'Trabalhando (km/h)','Transporte (km/h)']
                    bar_width_colheitadeira_desloc = 0.1  # Largura das barras

                    # Definir posições das barras para cada grupo de dados
                    bar_positions_colheitadeira_desloc = np.arange(len(maquinas_colheitadeira_desloc))

                    # Plotar as barras verticais combinadas para cada máquina
                    for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_desloc, percentual_colheitadeira_desloc.values)):
                        for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_desloc)):
                            ax_colheitadeira_desloc.bar(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent, width=bar_width_colheitadeira_desloc, label=labels_colheitadeira_desloc[j] if i == 0 else "", color=color)
                            ax_colheitadeira_desloc.text(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

                    # Configurar rótulos e título
                    ax_colheitadeira_desloc.set_xlabel('Máquinas')  # Texto do eixo x
                    ax_colheitadeira_desloc.set_ylabel('')  # Texto do eixo y
                    ax_colheitadeira_desloc.set_xticks(bar_positions_colheitadeira_desloc + bar_width_colheitadeira_desloc)
                    ax_colheitadeira_desloc.set_xticklabels(maquinas_colheitadeira_desloc)
                    ax_colheitadeira_desloc.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_colheitadeira_desloc.set_title('Velocidade de Deslocamento km/h')

                    # Definir as numerações do eixo y
                    yticks_values = np.arange(0, 26, 2)  # Ajuste conforme necessário
                    yticks_labels = [f'{val:.1f}' for val in yticks_values]
                    ax_colheitadeira_desloc.set_yticks(yticks_values)
                    ax_colheitadeira_desloc.set_yticklabels(yticks_labels)

                    # Adicionar legenda única
                    ax_colheitadeira_desloc.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
                    col8, col9 = st.columns(2)
                    col8.pyplot(fig_pulverizador_desloc)

                    #########################################################################################################################

                    selected_columns_hrmotor = ["Máquina", "Horas de Operação do Motor Período (h)"]
                    df_selected_tractors_hrmotor = df_sprayers[selected_columns_hrmotor].copy()

                    # Ordenar o DataFrame com base nas horas de operação do motor usando sort_values
                    df_selected_tractors_hrmotor = df_selected_tractors_hrmotor.sort_values(by="Horas de Operação do Motor Período (h)", ascending=False)

                    # Configurar o gráfico
                    fig_pulverizador_hrmotor, ax_hrmotor = plt.subplots(figsize=(12, 8))

                    # Extrair dados para plotagem
                    maquinas_tractors_hrmotor = df_selected_tractors_hrmotor["Máquina"]
                    horas_operacao_hrmotor = df_selected_tractors_hrmotor["Horas de Operação do Motor Período (h)"]
                    wrapped_labels = wrap_labels(maquinas_tractors_hrmotor, width=10)  # Ajuste a largura conforme necessário

                    # Ajustar a altura das barras dinamicamente
                    bar_height_hrmotor = 0.3
                    if len(maquinas_tractors_hrmotor) == 1:
                        bar_height_hrmotor = 0.2  # Barra mais fina

                    # Plotar barras horizontais com cor verde musgo claro
                    bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=bar_height_hrmotor, color='green')
                    labels_hrmotor = ['Hr de operação']

                    # Adicionar os números de horas formatados no final de cada barra
                    for bar, hora in zip(bars, horas_operacao_hrmotor):
                        ax_hrmotor.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                        va='center', ha='left', fontsize=10, fontweight='bold')

                    # Configurar os eixos e título
                    ax_hrmotor.set_xlabel('')
                    ax_hrmotor.set_ylabel('')
                    ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')
                    ax_hrmotor.set_yticklabels(wrapped_labels)

                    # Centralizar a barra única
                    if len(maquinas_tractors_hrmotor) == 1:
                        ax_hrmotor.set_ylim(-0.5, 0.5)  # Centralizar a barra no meio do gráfico

                    # Adicionar legenda única para Horas de Operação
                    ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

                    col9.pyplot(fig_pulverizador_hrmotor)
                    #############################################################################################################
                    
                    if st.button('Gerar PDF para Pulverizador'):
                        figures = [fig_pulverizador_combus, fig_pulverizador_factor,  fig_pulverizador_rotacao, fig_pulverizador_autotrac, fig_pulverizador_desloc,fig_pulverizador_hrmotor ]  
                        pdf_buffer = generate_pdf_pulverizador( df_sprayers, figures, background_image_first_page_pulverizador, background_image_other_pages)
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_buffer,
                            file_name="relatorio_pulverizador.pdf",
                            mime="application/pdf"
                        )

# Lógica para Colheitadeira
elif selected == "🌱Colheitadeira":
    
    st.subheader("Colheitadeira")

    col1,col2,col3=st.columns(3)
    # Seleção do tipo de arquivo e upload
    file_type_colheitadeira = st.radio("Selecione o tipo de arquivo:", ("CSV", "Excel"))
    uploaded_file_colheitadeira = st.file_uploader(f"Escolha um arquivo {file_type_colheitadeira} para Tratores", type=["csv", "xlsx"])

    if uploaded_file_colheitadeira is not None:
        df_colheitadeira = load_data(uploaded_file_colheitadeira, file_type_colheitadeira)

        if df_colheitadeira is not None:
            st.subheader('Dados do Arquivo Carregado para Colheitadeira')
            # Exibir data de início e data final
            if 'Data de Início' in df_colheitadeira.columns and 'Data Final' in df_colheitadeira.columns and 'Organização' in df_colheitadeira.columns:
                    data_inicio = pd.to_datetime(df_colheitadeira['Data de Início'].iloc[0])
                    data_final = pd.to_datetime(df_colheitadeira['Data Final'].iloc[0])
                    organização = df_colheitadeira['Organização'].iloc[0]

                    col1, col2, col3 = st.columns(3)
                    col1.write(f"Organização: {organização}")
                    col2.write(f"Data de Início: {data_inicio}")
                    col3.write(f"Data Final: {data_final}")
                    

                    # Exibir logo
                    #st.image(Image.open('C:\Users\ThanizeRodrigues-Alv\OneDrive - Alvorada Sistemas Agrícolas Ltda\Área de Trabalho\Thanize\códigos\logo.jpg'), width=200)

                    # Criar lista de datas
                    dates = pd.date_range(start=data_inicio, end=data_final)

                    # Criar dicionário para cores
                    colors = {
                        'Event': 'rgb(31, 119, 180)',
                        'Other Event': 'rgb(255, 127, 14)'
                    }
    ##############################################################################################################################################################################
    # Definir colunas para análise de utilização da colheitadeira
    # Definir as colunas principais e opcionais para análise de utilização
            selected_columns_utilizacao = ["Máquina"]

            # Verificar se as colunas opcionais existem e adicioná-las
            if "Utilização (Agricultura) Trabalho (%)" in df_colheitadeira.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Trabalho (%)")

            if "Utilização (Agricultura) Transporte (%)" in df_colheitadeira.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Transporte (%)")

            if "Utilização (Agricultura) Marcha Lenta (%)" in df_colheitadeira.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Marcha Lenta (%)")

            if "Utilização (Agricultura) Ocioso (%)" in df_colheitadeira.columns:
                selected_columns_utilizacao.append("Utilização (Agricultura) Ocioso (%)")

            # Selecionar os dados com as colunas presentes
            df_selected_tractors_utilizacao = df_colheitadeira[selected_columns_utilizacao].copy()

            # Nomes das máquinas e porcentagens de utilização
            maquinas_tractors = df_selected_tractors_utilizacao["Máquina"]
            velocidades_total_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].sum(axis=1)
            velocidades_percentual_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].div(velocidades_total_tractors, axis=0) * 100
            wrapped_labels = wrap_labels(maquinas_tractors, width=10)  # Ajuste a largura conforme necessário

            # Ajustar a altura das barras dinamicamente
            bar_height_utilizacao = 0.6
            if len(maquinas_tractors) == 1:
                bar_height_utilizacao = 0.2  # Barra mais fina

            bar_positions_tractors_utilizacao = np.arange(len(maquinas_tractors))

            # Plotar gráfico de barras horizontais para % de Utilização
            fig_colheitadeira_util, ax_utilizacao = plt.subplots(figsize=(12, 8))

            # Definir as cores e labels dinamicamente com base nas colunas disponíveis
            colors_utilizacao = []
            labels_utilizacao = []

            if "Utilização (Agricultura) Trabalho (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:green')
                labels_utilizacao.append('Trabalhando')

            if "Utilização (Agricultura) Transporte (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:gray')
                labels_utilizacao.append('Transporte')

            if "Utilização (Agricultura) Marcha Lenta (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:orange')
                labels_utilizacao.append('Marcha Lenta')

            if "Utilização (Agricultura) Ocioso (%)" in df_selected_tractors_utilizacao.columns:
                colors_utilizacao.append('tab:orange')
                labels_utilizacao.append('Ocioso')

            # Plotar as barras horizontais combinadas para cada máquina (utilização)
            for i, (maquina, row) in enumerate(zip(maquinas_tractors, velocidades_percentual_tractors.values)):
                left = 0
                for j, (percent, color) in enumerate(zip(row, colors_utilizacao)):
                    ax_utilizacao.barh(bar_positions_tractors_utilizacao[i], percent, height=bar_height_utilizacao, 
                                    left=left, label=labels_utilizacao[j] if i == 0 else "", color=color)
                    ax_utilizacao.text(left + percent / 2, bar_positions_tractors_utilizacao[i], 
                                    f'{percent:.1f}%', ha='center', va='center', color='black', fontsize=10, fontweight='bold')
                    left += percent

            # Configurar os eixos e título
            ax_utilizacao.set_xlabel('')
            ax_utilizacao.set_yticks(bar_positions_tractors_utilizacao)
            ax_utilizacao.set_yticklabels(wrapped_labels)
            ax_utilizacao.set_xticks([])  
            ax_utilizacao.set_title('% de Utilização por Máquina - Tratores')

            # Centralizar a barra única
            if len(maquinas_tractors) == 1:
                ax_utilizacao.set_ylim(-0.5, 0.5)  # Centralizar a barra no meio do gráfico

            # Adicionar legenda única para Utilização
            ax_utilizacao.legend(labels_utilizacao, loc='upper right', bbox_to_anchor=(1.21, 1.0))

            # Mostrar o gráfico
            col4, col5 = st.columns(2)
            col4.pyplot(fig_colheitadeira_util)

            ##############################################################################################################################################################################
            #fator de carga média
            selected_columns_colheitadeira_factor = ["Máquina", 
                               "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)",
                               "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                               "Fator de Carga Média do Motor (Ag) Transporte (%)"
                               ]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_colheitadeira_factor = df_colheitadeira[selected_columns_colheitadeira_factor].copy()

            # Nomes das máquinas e porcentagens
            maquinas_colheitadeira_factor = df_selected_colheitadeira_factor["Máquina"]
            percentual_colheitadeira_factor = df_selected_colheitadeira_factor.iloc[:, 1:] *100

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_colheitadeira_factor, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais
            fig_colheitadeira_factor, ax_colheitadeira_factor = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_colheitadeira_factor = ['tab:orange', 'tab:green', 'tab:gray']
            labels_colheitadeira_factor = ['Marcha Lenta (%)', 'Trabalho (%)', 'Transporte (%)']
            bar_width_colheitadeira_factor = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_factor = np.arange(len(maquinas_colheitadeira_factor))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_factor, percentual_colheitadeira_factor.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_util)):
                    ax_colheitadeira_factor.bar(bar_positions_colheitadeira_factor[i] + j * bar_width_colheitadeira_factor, percent, width=bar_width_colheitadeira_factor, label=labels_colheitadeira_factor[j] if i == 0 else "", color=color)
                    ax_colheitadeira_factor.text(bar_positions_colheitadeira_factor[i] + j * bar_width_colheitadeira_factor, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10,fontweight='bold')

            # Configurar rótulos e título
            ax_colheitadeira_factor.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_factor.set_ylabel('Percentual de Utilização (%)')  # Texto do eixo y
            ax_colheitadeira_factor.set_xticks(bar_positions_colheitadeira_factor + bar_width_colheitadeira_factor)
            ax_colheitadeira_factor.set_xticklabels(maquinas_colheitadeira_factor)
            ax_colheitadeira_factor.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_factor.set_title('Fator de caga %')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_factor.set_yticks(yticks_values)
            ax_colheitadeira_factor.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_factor.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))

            col5.pyplot(fig_colheitadeira_factor)
            ###################################################################################################################################################
            #combustivel
            selected_columns_colheitadeira_combus = ["Máquina", 
                               "Taxa Média de Combustível (Ag) Ocioso (l/h)",
                               "Taxa Média de Combustível (Ag) Trabalhando (l/h)",
                               "Taxa Média de Combustível (Ag) Transporte (l/h)"
                               ]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_colheitadeira_combus = df_colheitadeira[selected_columns_colheitadeira_combus].copy()

            # Nomes das máquinas e porcentagens
            maquinas_colheitadeira_combus = df_selected_colheitadeira_combus["Máquina"]
            percentual_colheitadeira_combus = df_selected_colheitadeira_combus.iloc[:, 1:] 

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_colheitadeira_combus, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais
            fig_colheitadeira_combus, ax_colheitadeira_combus = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_colheitadeira_combus = ['tab:orange', 'tab:green', 'tab:gray']
            labels_colheitadeira_combus = ['Ocioso l/h', 'Trabalhando l/h', 'Transporte l/h']
            bar_width_colheitadeira_combus = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_combus = np.arange(len(maquinas_colheitadeira_combus))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_combus, percentual_colheitadeira_combus.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_util)):
                    ax_colheitadeira_combus.bar(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent, width=bar_width_colheitadeira_combus, label=labels_colheitadeira_combus[j] if i == 0 else "", color=color)
                    ax_colheitadeira_combus.text(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

            # Configurar rótulos e título
            ax_colheitadeira_combus.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_combus.set_ylabel('(l/h)')  # Texto do eixo y
            ax_colheitadeira_combus.set_xticks(bar_positions_colheitadeira_combus + bar_width_colheitadeira_combus)
            ax_colheitadeira_combus.set_xticklabels(maquinas_colheitadeira_combus)
            ax_colheitadeira_combus.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_combus.set_title('Combustivel (l/h)')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_combus.set_yticks(yticks_values)
            ax_colheitadeira_combus.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_combus.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
            col6, col7 = st.columns(2)
            col6.pyplot(fig_colheitadeira_combus)
            ###################################################################################################################################################
           # Definir colunas para análise de rotação média do motor
            selected_columns_rotacao = ["Máquina", 
                                        "Rotação Média do Motor Ocioso (rpm)",
                                        "Rotação Média do Motor Trabalhando (rpm)",
                                        "Rotação Média do Motor Transporte (rpm)"]

            # Filtrar o DataFrame para as colunas de rotação selecionadas
            df_selected_rotacao = df_colheitadeira[selected_columns_rotacao].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e rotação média
            maquinas_rotacao = df_selected_rotacao["Máquina"]
            rotacoes = df_selected_rotacao.iloc[:, 1:]

            # Plotar gráfico de barras horizontais para rotação média
            fig_rotacao, ax_rotacao = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_rotacao, width=10)  # Ajuste a largura conforme necessário

            # Cores e labels para as barras de rotação média
            colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_rotacao = ['Ocioso', 'Trabalhando', 'Transporte']
            bar_height_rotacao = 0.32  # Altura das barras de rotação média
            bar_positions_rotacao = np.arange(len(maquinas_rotacao)) * 2  # Aumentar o fator de multiplicação para espaçamento maior
            offset = 0.35  # Espaçamento entre as categorias dentro de cada máquina

            # Iterar sobre as categorias para criar as barras
            for j in range(len(labels_rotacao)):
                # Desenhar barras e garantir que valores NaN sejam visualizados como em branco
                ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                rotacoes.iloc[:, j].fillna(np.nan), 
                                height=bar_height_rotacao, 
                                label=labels_rotacao[j], 
                                color=colors_rotacao[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_rotacao)):
                    rotacao = rotacoes.iloc[i, j]
                    if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                        ax_rotacao.text(rotacao + 2,  # Ajuste para mover o texto mais para a direita
                                        bar_positions_rotacao[i] + j * offset, 
                                        f'{rotacao:.0f}', 
                                        ha='left', 
                                        va='center', 
                                        color='black', 
                                        fontsize=10,
                                        fontweight='bold')

            # Configurar os eixos e título
            ax_rotacao.set_xlabel('')
            ax_rotacao.set_yticks(bar_positions_rotacao + offset)
            ax_rotacao.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_rotacao.set_title('Rotação Média do Motor RPM')

            # Definir os limites e marcas do eixo x
            max_value = rotacoes.stack().max() if not rotacoes.empty else 0
            ax_rotacao.set_xlim([0, max_value * 1.1])
            ax_rotacao.set_xticks([0, max_value * 0.5, max_value])
            ax_rotacao.set_xticklabels(['0', f'{int(max_value * 0.5)}', f'{int(max_value)}'])

            # Adicionar legenda única para rotação média
            ax_rotacao.legend(loc='upper right', bbox_to_anchor=(1.2, 1.0))

            # Mostrar o gráfico de rotação média
            col7.pyplot(fig_rotacao)


            #####################################################################################################################
            # Definir colunas para análise de velocidade de deslocamento
            selected_columns_colheitadeira_desloc = ["Máquina", 
                                        "Velocidade Média de Deslocamento (km/h)",
                                        "Velocidade Média de Deslocamento Trabalhando (km/h)"]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_colheitadeira_desloc = df_colheitadeira[selected_columns_colheitadeira_desloc].copy()

            # Nomes das máquinas e porcentagens
            maquinas_colheitadeira_desloc = df_selected_colheitadeira_desloc["Máquina"]
            percentual_colheitadeira_desloc = df_selected_colheitadeira_desloc.iloc[:, 1:]

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_colheitadeira_desloc, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais
            fig_colheitadeira_desloc, ax_colheitadeira_desloc = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_colheitadeira_desloc = ['tab:green', 'tab:orange']
            labels_colheitadeira_desloc = ['Trabalhando (km/h)', 'Deslocamento (km/h)']
            bar_width_colheitadeira_desloc = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_desloc = np.arange(len(maquinas_colheitadeira_desloc))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_desloc, percentual_colheitadeira_desloc.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_desloc)):
                    ax_colheitadeira_desloc.bar(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent, width=bar_width_colheitadeira_desloc, label=labels_colheitadeira_desloc[j] if i == 0 else "", color=color)
                    ax_colheitadeira_desloc.text(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent + 0.5, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')  # Ajuste para o número mais próximo da barra

            # Configurar rótulos e título
            ax_colheitadeira_desloc.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_desloc.set_ylabel('')  # Texto do eixo y
            ax_colheitadeira_desloc.set_xticks(bar_positions_colheitadeira_desloc + bar_width_colheitadeira_desloc / 2)
            ax_colheitadeira_desloc.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_desloc.set_title('Velocidade de Deslocamento km/h')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 13, 2)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_desloc.set_yticks(yticks_values)
            ax_colheitadeira_desloc.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_desloc.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))

            # Mostrar o gráfico
            col8, col9 = st.columns(2)
            col9.pyplot(fig_colheitadeira_desloc)

            ######################################################################################################################################################################################

            selected_columns_colheitadeira_autotrac = ["Máquina", 
                               'AutoTrac™ Ativo (%)'
                               ]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_colheitadeira_autotrac = df_colheitadeira[selected_columns_colheitadeira_autotrac].copy()

            # Nomes das máquinas e porcentagens
            maquinas_colheitadeira_autotrac = df_selected_colheitadeira_autotrac["Máquina"]
            percentual_colheitadeira_autotrac = df_selected_colheitadeira_autotrac.iloc[:, 1:] *100

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_colheitadeira_autotrac, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais
            fig_colheitadeira_autotrac, ax_colheitadeira_autotrac = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_colheitadeira_autotrac = ['tab:blue']
            labels_colheitadeira_autotrac = [ 'AutoTrac™ Ativo (%)']
            bar_width_colheitadeira_autotrac = 0.2  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_autotrac = np.arange(len(maquinas_colheitadeira_autotrac))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_autotrac, percentual_colheitadeira_autotrac.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_autotrac)):
                    ax_colheitadeira_autotrac.bar(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent, width=bar_width_colheitadeira_autotrac, label=labels_colheitadeira_autotrac[j] if i == 0 else "", color=color)
                    ax_colheitadeira_autotrac.text(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold')

            # Configurar rótulos e título
            ax_colheitadeira_autotrac.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_autotrac.set_ylabel('')  # Texto do eixo y
            ax_colheitadeira_autotrac.set_xticks(bar_positions_colheitadeira_desloc + bar_width_colheitadeira_desloc)
            ax_colheitadeira_autotrac.set_xticklabels(maquinas_colheitadeira_desloc)
            ax_colheitadeira_autotrac.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_autotrac.set_title('Uso de Autotrac %')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_autotrac.set_yticks(yticks_values)
            ax_colheitadeira_autotrac.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_autotrac.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
            col8.pyplot(fig_colheitadeira_autotrac)

            ######################################################################################################################################################
            ## Definir os dados
            selected_columns_hrmotor = ["Máquina", "Horas de Operação do Motor Período (h)"]
            df_selected_tractors_hrmotor = df_colheitadeira[selected_columns_hrmotor].copy()

            # Ordenar o DataFrame com base nas horas de operação do motor usando sort_values
            df_selected_tractors_hrmotor = df_selected_tractors_hrmotor.sort_values(by="Horas de Operação do Motor Período (h)", ascending=False)

            # Configurar o gráfico
            fig_hrmotor, ax_hrmotor = plt.subplots(figsize=(12, 8))

            # Extrair dados para plotagem
            maquinas_tractors_hrmotor = df_selected_tractors_hrmotor["Máquina"]
            horas_operacao_hrmotor = df_selected_tractors_hrmotor["Horas de Operação do Motor Período (h)"]

             # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_tractors_hrmotor, width=10)  # Ajuste a largura conforme necessário
            # Plotar barras horizontais com cor verde musgo claro
            bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=0.2, color='green')
            labels_hrmotor = ['Hr de operação']

            # Adicionar os números de horas formatados no final de cada barra
            for bar, hora in zip(bars, horas_operacao_hrmotor):
                ax_hrmotor.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                va='center', ha='left', fontsize=10, fontweight='bold')

            # Configurar os eixos e título
            ax_hrmotor.set_xlabel('')
            ax_hrmotor.set_ylabel('')
            ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')
            ax_hrmotor.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha

            # Adicionar legenda única para Fator de Carga
            ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

            # Mostrar o gráfico
            col10, col11 = st.columns(2)
            # Mostrar o gráfico de barras horizontais
            col10.pyplot(fig_hrmotor)

            if st.button('Gerar PDF para Colheitadeira'):
                        figures = [ fig_colheitadeira_util, fig_colheitadeira_factor, fig_colheitadeira_combus, fig_rotacao, fig_colheitadeira_autotrac, fig_colheitadeira_desloc, fig_hrmotor]  
                        pdf_buffer = generate_pdf_colheitadeira( df_colheitadeira, figures, background_image_first_page_colheitadeira, background_image_other_pages)
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_buffer,
                            file_name="relatorio_colheitadeira.pdf",
                            mime="application/pdf"
                        )
else:
    st.error("Página não encontrada.")
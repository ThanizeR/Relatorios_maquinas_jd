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

def generate_pdf(df_tractors, figures, background_image_first_page=None, background_image_other_pages=None):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    page_width, page_height = A4
    x_margin = 35
    y_margin = 20
    header_space_first_page = 100
    header_space_other_pages = 25

    # Diminuir um pouco mais a largura e altura dos gráficos
    graph_width = page_width - 2 * x_margin - 10
    graph_height_first_page = (page_height - 2 * y_margin - header_space_first_page) / 2 - 12
    graph_height_other_pages = (page_height - 2 * y_margin - header_space_other_pages) / 2 - 12

    def set_background(page_num):
        if page_num == 0 and background_image_first_page:
            background = ImageReader(background_image_first_page)
        elif background_image_other_pages:
            background = ImageReader(background_image_other_pages)
        else:
            return
        c.drawImage(background, 0, 0, width=A4[0], height=A4[1])

    page_num = 0
    set_background(page_num)

    if 'Data de Início' in df_tractors.columns and 'Data Final' in df_tractors.columns and 'Organização' in df_tractors.columns:
        data_inicio = pd.to_datetime(df_tractors['Data de Início'].iloc[0])
        data_final = pd.to_datetime(df_tractors['Data Final'].iloc[0])
        organizacao = df_tractors['Organização'].iloc[0]

        c.setFont("Helvetica-Bold", 10)  # Definir texto em negrito e tamanho 12
        c.setFillColorRGB(1, 1, 1)  # Definir a cor do texto como branca
        y_position = page_height - y_margin - 2  # Ajustar a posição do texto no cabeçalho

        # Desenhar organização e datas em três linhas
        c.drawString(x_margin, y_position, f"Organização: {organizacao}")
        y_position -= 15  # Espaçamento entre linhas
        c.drawString(x_margin, y_position, f"Data de Início: {data_inicio.strftime('%d/%m/%Y')}")
        y_position -= 15  # Espaçamento entre linhas
        c.drawString(x_margin, y_position, f"Data Final: {data_final.strftime('%d/%m/%Y')}")

    for i, fig in enumerate(figures):
        if not isinstance(fig, plt.Figure):
            print(f"Skipping non-Matplotlib figure: {type(fig)}")
            continue

        if i % 2 == 0 and i != 0:
            c.showPage()
            page_num += 1
            set_background(page_num)
            y_position = page_height - y_margin - header_space_other_pages
            graph_height = graph_height_other_pages
        else:
            if i == 0:
                y_position = page_height - y_margin - header_space_first_page
                graph_height = graph_height_first_page
            else:
                y_position -= graph_height + y_margin / 2

        img_data = BytesIO()
        fig.savefig(img_data, format='png', bbox_inches='tight')
        img_data.seek(0)

        x_position = x_margin
        c.drawImage(ImageReader(img_data), x_position, y_position - graph_height, width=graph_width, height=graph_height)

    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Caminho para as imagens de fundo
background_image_first_page = 'background_pdf_first_page.jpg'
background_image_other_pages = 'background_pdf_other_pages.jpg'

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
            #######################################################################################

            # Definir colunas para análise de utilização
            selected_columns_utilizacao = ["Máquina", 
                                           "Utilização (Agricultura) Trabalho (%)",
                                           "Utilização (Agricultura) Transporte (%)",
                                           "Utilização (Agricultura) Marcha Lenta (%)"]

            df_selected_tractors_utilizacao = df_tractors[selected_columns_utilizacao].copy()

            # Nomes das máquinas e porcentagens de utilização
            maquinas_tractors = df_selected_tractors_utilizacao["Máquina"]
            velocidades_total_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].sum(axis=1)
            velocidades_percentual_tractors = df_selected_tractors_utilizacao.iloc[:, 1:].div(velocidades_total_tractors, axis=0) * 100
            wrapped_labels = wrap_labels(maquinas_tractors, width=10)  # Ajuste a largura conforme necessário
            # Plotar gráfico de barras horizontais para % de Utilização
            fig_utilizacao, ax_utilizacao = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras de Utilização
            colors_utilizacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_utilizacao = ['Trabalhando', 'Transporte', 'Marcha Lenta']
            bar_height_utilizacao = 0.6  # Altura das barras de Utilização
            bar_positions_tractors_utilizacao = np.arange(len(maquinas_tractors))

            # Plotar as barras horizontais combinadas para cada máquina (utilização)
            for i, (maquina, row) in enumerate(zip(maquinas_tractors, velocidades_percentual_tractors.values)):
                left = 0
                for j, (percent, color) in enumerate(zip(row, colors_utilizacao)):
                    ax_utilizacao.barh(bar_positions_tractors_utilizacao[i], percent, height=bar_height_utilizacao, left=left, label=labels_utilizacao[j] if i == 0 else "", color=color)
                    ax_utilizacao.text(left + percent / 2, bar_positions_tractors_utilizacao[i], f'{percent:.1f}%', ha='center', va='center', color='black', fontsize=10)
                    left += percent

            # Configurar os eixos e título
            ax_utilizacao.set_xlabel('')
            ax_utilizacao.set_yticks(bar_positions_tractors_utilizacao)  # Manter os ticks do eixo y
            ax_utilizacao.set_yticklabels(maquinas_tractors)  # Manter os rótulos do eixo y
            ax_utilizacao.set_xticks([])  # Remover os ticks do eixo x
            ax_utilizacao.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_utilizacao.set_title('% de Utilização por Máquina - Tratores')

            # Adicionar legenda única para Utilização
            ax_utilizacao.legend(labels_utilizacao, loc='upper right', bbox_to_anchor=(1.21, 1.0))

            # Mostrar o gráfico de Utilização
            col4, col5 = st.columns(2)
            col4.pyplot(fig_utilizacao)
            #############################################################

            # Definir colunas para análise de fator de carga média do motor
            selected_columns_fator = ["Máquina", 
                                    "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                                    "Fator de Carga Média do Motor (Ag) Transporte (%)",
                                    "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)"]

            # Filtrar o DataFrame para as colunas de fator de carga selecionadas
            df_selected_tractors_fator = df_tractors[selected_columns_fator].copy()

            # Nomes das máquinas e porcentagens de fator de carga
            maquinas_tractors_fator = df_selected_tractors_fator["Máquina"]
            fatores_percentual_tractors = df_selected_tractors_fator.iloc[:, 1:] * 100
            wrapped_labels = wrap_labels(maquinas_tractors_fator, width=10)
            # Plotar gráfico de barras horizontais para % de Fator de Carga
            fig_fator, ax_fator = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras de Fator de Carga
            colors_fator = ['tab:green', 'tab:gray', 'tab:orange']
            labels_fator = ['Trabalhando', 'Transporte', 'Marcha Lenta']
            bar_height_fator = 0.33  # Altura das barras de Fator de Carga
            bar_positions_tractors_fator = np.arange(len(maquinas_tractors_fator))

            # Ajustar as posições das barras para que fiquem separadas
            offset = 0.35
            for j in range(len(labels_fator)):
                ax_fator.barh(bar_positions_tractors_fator + j * offset, 
                            fatores_percentual_tractors.iloc[:, j], 
                            height=bar_height_fator, 
                            label=labels_fator[j], 
                            color=colors_fator[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_tractors_fator)):
                    percent = fatores_percentual_tractors.iloc[i, j]
                    ax_fator.text((percent / 2) + 2,  # Ajuste para mover o texto mais para a direita
                                bar_positions_tractors_fator[i] + j * offset, 
                                f'{percent:.1f}%', 
                                ha='center', 
                                va='center', 
                                color='black', 
                                fontsize=10)

            # Configurar os eixos e título
            ax_fator.set_xlabel('')
            ax_fator.set_yticks(bar_positions_tractors_fator + offset)
            ax_fator.set_yticklabels(maquinas_tractors_fator)
            ax_fator.set_title('% de Fator de Carga por Máquina - Tratores')
            ax_fator.set_xticklabels(wrapped_labels)
            # Definir os limites e marcas do eixo x
            ax_fator.set_xlim([0, 100])
            ax_fator.set_xticks([0, 50, 100])
            ax_fator.set_xticklabels(['0%', '50%', '100%'])

            # Adicionar legenda única para Fator de Carga
            ax_fator.legend(labels_fator, loc='upper right', bbox_to_anchor=(1.23, 1.0))

            # Mostrar o gráfico de Fator de Carga
            col5.pyplot(fig_fator)


            ################################################################################################

            # Definir colunas para análise de taxa média de combustível
            selected_columns_combust = ["Máquina",
                                        "Taxa Média de Combustível (Ag) Trabalhando (l/h)",
                                        "Taxa Média de Combustível (Ag) Transporte (l/h)",
                                        "Taxa Média de Combustível (Ag) Ocioso (l/h)"]

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
                    ax_combust.bar(bar_positions_tractors_combust[i] + j * bar_width_combust, percent, width=bar_width_combust, label=labels_combust[j] if i == 0 else "", color=color)
                    ax_combust.text(bar_positions_tractors_combust[i] + j * bar_width_combust, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10)

            # Configurar rótulos e título
            ax_combust.set_xlabel('')  # Texto do eixo x
            ax_combust.set_ylabel('')  # Texto do eixo y
            ax_combust.set_xticks(bar_positions_tractors_combust + bar_width_combust)
            ax_combust.set_xticklabels(maquinas_tractors_combust)
            ax_combust.set_yticklabels(wrapped_labels)
            ax_combust.set_title('Consumo de Combustível')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 51, 5)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_combust.set_yticks(yticks_values)
            ax_combust.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_combust.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))

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
            labels_rotacao = ['Trabalhando', 'Transporte','Ocioso']
            bar_height_rotacao = 0.3  # Altura das barras de rotação média
            bar_positions_rotacao = np.arange(len(maquinas_tractors_rotacao))

            # Ajustar as posições das barras para que fiquem separadas
            offset = 0.32
            for j in range(len(labels_rotacao)):
                # Usar np.nan para valores NaN para que apareçam em branco
                ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                rotacoes_tractors.iloc[:, j].fillna(np.nan), 
                                height=bar_height_rotacao, 
                                label=labels_rotacao[j] if j == 0 else "", 
                                color=colors_rotacao[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_rotacao)):
                    rotacao = rotacoes_tractors.iloc[i, j]
                    if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                        ax_rotacao.text((rotacao / 2) + 3,  # Ajuste para mover o texto mais para a direita
                                        bar_positions_rotacao[i] + j * offset, 
                                        f'{rotacao:.0f}', 
                                        ha='center', 
                                        va='center', 
                                        color='black', 
                                        fontsize=10)

            # Configurar os eixos e título
            ax_rotacao.set_xlabel('')
            ax_rotacao.set_yticks(bar_positions_rotacao + offset)
            ax_rotacao.set_yticklabels(maquinas_tractors_rotacao)
            ax_rotacao.set_title('Rotação Média do Motor por Máquina - Tratores')
            ax_rotacao.set_yticklabels(wrapped_labels)

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = rotacoes_tractors.stack().max() if not rotacoes_tractors.empty else 0
            ax_rotacao.set_xlim([0, max_value * 1.1])

            # Adicionar legenda única para rotação média
            ax_rotacao.legend(labels_rotacao, loc='upper right', bbox_to_anchor=(1.2, 1.0))


            # Mostrar o gráfico de rotação média
            col7.pyplot(fig_rotacao)

        ###################################################################################################

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
            # Plotar barras horizontais com cor verde musgo claro
            bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=0.6, color='green')
            labels_hrmotor = ['Hr de operação']

            # Adicionar os números de horas formatados no final de cada barra
            for bar, hora in zip(bars, horas_operacao_hrmotor):
                ax_hrmotor.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                va='center', ha='left', fontsize=10)

            # Configurar os eixos e título
            ax_hrmotor.set_xlabel('')
            ax_hrmotor.set_ylabel('')
            ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')
            ax_hrmotor.set_yticklabels(wrapped_labels)

            # Adicionar legenda única para Fator de Carga
            ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

            # Mostrar o gráfico
            col8, col9 = st.columns(2)
            # Mostrar o gráfico de barras horizontais
            col8.pyplot(fig_hrmotor)


            ########################################################################################
            # Definir colunas para análise de velocidade média de deslocamento
            selected_columns_desloc = [
                "Máquina", 
                "Velocidade Média de Deslocamento Trabalhando (km/h)",
                "Velocidade Média de Deslocamento Transporte (km/h)"
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
                            fontsize=10
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
            selected_columns_patinagem3 = [
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

            df_selected_tractors_patinagem3 = df_tractors[selected_columns_patinagem3].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_patinagem3.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e tempo de patinagem
            maquinas_tractors_patinagem3 = df_selected_tractors_patinagem3["Máquina"]
            patinagem_tractors3 = df_selected_tractors_patinagem3.iloc[:, 1:]
            wrapped_labels = wrap_labels(maquinas_tractors_patinagem3, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais para tempo de patinagem
            fig_patinagem4, ax_patinagem3 = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras de Patinagem
            colors_patinagem3 = ['tab:blue', 'tab:red', 'tab:green', 'tab:pink', 'tab:cyan',
                                'tab:orange', 'tab:brown', 'tab:gray', 'tab:olive', 'tab:purple']
            labels_patinagem3 = [
                '0,00–2,00% (h)', '2,01–4,00% (h)', '4,01–6,00% (h)', '6,01–8,00% (h)', '8,01–10,00% (h)',
                '10,01–12,00% (h)', '12,01–14,00% (h)', '14,01–16,00% (h)', '16,01–18,00% (h)', '18,01–100,00% (h)'
            ]

            bar_width = 4  # Largura das barras
            space_between_bars = 2  # Espaço entre as barras coloridas
            machine_offset = 2  # Espaço entre cada máquina

            for i, (maquina, row) in enumerate(zip(maquinas_tractors_patinagem3, patinagem_tractors3.values)):
                base_position = i * (len(colors_patinagem3) * (bar_width + space_between_bars) + machine_offset)
                sorted_row = sorted(zip(row, colors_patinagem3, labels_patinagem3), key=lambda x: x[0])
                for j, (value, color, label) in enumerate(sorted_row):
                    if value >= 0.1 or value == 0:  # Exibe valores maiores ou iguais a 0.1, ou valores zero
                        bar_position = base_position + j * (bar_width + space_between_bars)
                        ax_patinagem3.bar(bar_position, value, width=bar_width, label=label if i == 0 else "", color=color)

            # Adicionar linhas horizontais de referência para todos os valores de y
            max_y_value = patinagem_tractors3.values.max()
            max_y = min(max_y_value + 5, 25) if not np.isnan(max_y_value) and not np.isinf(max_y_value) else 25  # Garantir valor máximo de 25
            ax_patinagem3.set_ylim(0, max_y)

            y_ticks = np.arange(0, max_y + 1, 1)  # Gera ticks de 1 em 1 hora
            ax_patinagem3.set_yticks(y_ticks)

            for y in y_ticks:
                ax_patinagem3.axhline(y, color='gray', linestyle='--', linewidth=0.5)

            # Configurar os eixos e título
            ax_patinagem3.set_ylabel('Tempo de Patinagem (h)')
            ax_patinagem3.set_xticks([i * (len(colors_patinagem3) * (bar_width + space_between_bars) + machine_offset) + (len(colors_patinagem3) * (bar_width + space_between_bars) - space_between_bars) / 2 for i in range(len(maquinas_tractors_patinagem3))])
            ax_patinagem3.set_xticklabels(maquinas_tractors_patinagem3, rotation=45, ha='right')
            ax_patinagem3.set_title('Tempo de Patinagem das Rodas por Máquina - Tratores')
            ax_patinagem3.set_xticklabels(wrapped_labels)

            # Adicionar legenda única para Patinagem na ordem correta
            handles3, labels3 = zip(*sorted(zip(ax_patinagem3.get_legend_handles_labels()[0], labels_patinagem3), key=lambda x: labels_patinagem3.index(x[1])))
            ax_patinagem3.legend(handles3, labels_patinagem3, loc='upper right', bbox_to_anchor=(1.25, 1.0))

            st.pyplot(fig_patinagem4)
            #########################################################################################################

            if st.button('Gerar PDF para Tratores'):
                        figures = [ fig_utilizacao, fig_fator, fig_combust, fig_rotacao, fig_hrmotor,fig_desloc, fig_patinagem4]  
                        pdf_buffer = generate_pdf( df_tractors, figures, background_image_first_page, background_image_other_pages)
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_buffer,
                            file_name="relatorio.pdf",
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
                            ax_colheitadeira_combus.text(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10)

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
                    
                     #fator de carga média
                    selected_columns_pulverizador_factor = ["Máquina", 
                                    "Fator de Carga Média do Motor (Ag) Marcha Lenta (%)",
                                    "Fator de Carga Média do Motor (Ag) Trabalho (%)",
                                    "Fator de Carga Média do Motor (Ag) Transporte (%)"
                                    ]

                    # Filtrar o DataFrame para as colunas selecionadas
                    df_selected_pulverizador_factor = df_sprayers[selected_columns_pulverizador_factor].copy()

                    # Nomes das máquinas e porcentagens
                    maquinas_pulverizador_factor = df_selected_pulverizador_factor["Máquina"]
                    percentual_pulverizador_factor = df_selected_pulverizador_factor.iloc[:, 1:] *100

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_pulverizador_factor, width=10)  # Ajuste a largura conforme necessário

                    # Plotar gráfico de barras verticais
                    fig_pulverizador_factor, ax_pulverizador_factor = plt.subplots(figsize=(12, 8))

                    # Cores e labels para as barras
                    colors_pulverizador_factor = ['tab:green', 'tab:blue', 'tab:red']
                    labels_pulverizador_factor = ['Marcha Lenta (%)', 'Trabalho (%)', 'Transporte (%)']
                    bar_width_pulverizador_factor = 0.1  # Largura das barras

                    # Definir posições das barras para cada grupo de dados
                    bar_positions_pulverizador_factor = np.arange(len(maquinas_pulverizador_factor))

                    # Plotar as barras verticais combinadas para cada máquina
                    for i, (maquina, row) in enumerate(zip(maquinas_pulverizador_factor, percentual_pulverizador_factor.values)):
                        for j, (percent, color) in enumerate(zip(row, colors_pulverizador_factor)):
                            ax_pulverizador_factor.bar(bar_positions_pulverizador_factor[i] + j * bar_width_pulverizador_factor, percent, width=bar_width_pulverizador_factor, label=labels_pulverizador_factor[j] if i == 0 else "", color=color)
                            ax_pulverizador_factor.text(bar_positions_pulverizador_factor[i] + j * bar_width_pulverizador_factor, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

                    # Configurar rótulos e título
                    ax_pulverizador_factor.set_xlabel('Máquinas')  # Texto do eixo x
                    ax_pulverizador_factor.set_ylabel('Percentual de Utilização (%)')  # Texto do eixo y
                    ax_pulverizador_factor.set_xticks(bar_positions_pulverizador_factor + bar_width_pulverizador_factor)
                    ax_pulverizador_factor.set_xticklabels(maquinas_pulverizador_factor)
                    ax_pulverizador_factor.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_pulverizador_factor.set_title('Fator de caga %')

                    # Definir as numerações do eixo y
                    yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
                    yticks_labels = [f'{val:.1f}' for val in yticks_values]
                    ax_pulverizador_factor.set_yticks(yticks_values)
                    ax_pulverizador_factor.set_yticklabels(yticks_labels)

                    # Adicionar legenda única
                    ax_pulverizador_factor.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))

                    col5.pyplot(fig_pulverizador_factor)

                    ############################################################################################################
                    # Definir colunas para análise de rotação média do motor
                    selected_columns_rotacao = ["Máquina", 
                                                "Rotação Média do Motor Trabalhando (rpm)",
                                                "Rotação Média do Motor Transporte (rpm)",
                                                "Rotação Média do Motor Ocioso (rpm)"]

                    # Filtrar o DataFrame para as colunas de rotação selecionadas
                    df_selected_tractors_rotacao = df_sprayers[selected_columns_rotacao].copy()

                    # Manter linhas com NaN para visualização em branco
                    df_selected_tractors_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

                    # Nomes das máquinas e rotação média
                    maquinas_tractors_rotacao = df_selected_tractors_rotacao["Máquina"]
                    rotacoes_tractors = df_selected_tractors_rotacao.iloc[:, 1:]

                    # Plotar gráfico de barras horizontais para rotação média
                    fig_pulverizador_rotacao, ax_rotacao = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_tractors_rotacao, width=10)  # Ajuste a largura conforme necessário
                    # Cores e labels para as barras de rotação média
                    colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
                    labels_rotacao = ['Trabalhando', 'Transporte','Ocioso']
                    bar_height_rotacao = 0.2  # Altura das barras de rotação média
                    bar_positions_rotacao = np.arange(len(maquinas_tractors_rotacao))

                    # Ajustar as posições das barras para que fiquem separadas
                    offset = 0.32
                    for j in range(len(labels_rotacao)):
                        # Usar np.nan para valores NaN para que apareçam em branco
                        ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                        rotacoes_tractors.iloc[:, j].fillna(np.nan), 
                                        height=bar_height_rotacao, 
                                        label=labels_rotacao[j] if j == 0 else "", 
                                        color=colors_rotacao[j])

                        # Adicionar rótulos às barras
                        for i in range(len(bar_positions_rotacao)):
                            rotacao = rotacoes_tractors.iloc[i, j]
                            if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                                ax_rotacao.text((rotacao / 2) + 3,  # Ajuste para mover o texto mais para a direita
                                                bar_positions_rotacao[i] + j * offset, 
                                                f'{rotacao:.0f}', 
                                                ha='center', 
                                                va='center', 
                                                color='black', 
                                                fontsize=10)

                    # Configurar os eixos e título
                    ax_rotacao.set_xlabel('')
                    ax_rotacao.set_yticks(bar_positions_rotacao + offset)
                    ax_rotacao.set_yticklabels(maquinas_tractors_rotacao)
                    ax_rotacao.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    ax_rotacao.set_title('Rotação Média do Motor RPM')

                    # Verificar se os valores para definir os limites do eixo são válidos
                    max_value = rotacoes_tractors.stack().max() if not rotacoes_tractors.empty else 0
                    ax_rotacao.set_xlim([0, max_value * 1.1])

                    # Adicionar legenda única para rotação média
                    ax_rotacao.legend(labels_rotacao, loc='upper right', bbox_to_anchor=(1.2, 1.0))
                    col6, col7 = st.columns(2)
                    # Mostrar o gráfico de rotação média
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
                            ax_colheitadeira_autotrac.text(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

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
                            ax_colheitadeira_desloc.text(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10)

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
                    # Definir os dados
                    selected_columns_hrmotor = ["Máquina", "Horas de Operação do Motor Período (h)"]
                    df_selected_tractors_hrmotor = df_sprayers[selected_columns_hrmotor].copy()

                    # Ordenar o DataFrame com base nas horas de operação do motor usando sort_values
                    df_selected_tractors_hrmotor = df_selected_tractors_hrmotor.sort_values(by="Horas de Operação do Motor Período (h)", ascending=False)

                    # Configurar o gráfico
                    fig_pulverizador_hrmotor, ax_hrmotor = plt.subplots(figsize=(12, 8))

                    # Extrair dados para plotagem
                    maquinas_tractors_hrmotor = df_selected_tractors_hrmotor["Máquina"]
                    horas_operacao_hrmotor = df_selected_tractors_hrmotor["Horas de Operação do Motor Período (h)"]

                    # Aplicar quebra de linha nos nomes das máquinas
                    wrapped_labels = wrap_labels(maquinas_tractors_hrmotor, width=10)  # Ajuste a largura conforme necessário
                    # Plotar barras horizontais com cor verde musgo claro
                    bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=0.4, color='green')
                    labels_hrmotor = ['Hr de operação']

                    # Adicionar os números de horas formatados no final de cada barra
                    for bar, hora in zip(bars, horas_operacao_hrmotor):
                        ax_hrmotor.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                        va='center', ha='left', fontsize=10)

                    # Configurar os eixos e título
                    ax_hrmotor.set_xlabel('')
                    ax_hrmotor.set_ylabel('')
                    ax_hrmotor.set_title('Horas de Operação do Motor por Máquina')
                    ax_hrmotor.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
                    xticks_values = np.arange(0, 120, 20)  # Ajuste conforme necessário
                    ax_hrmotor.set_xticks(xticks_values)
                    # Adicionar legenda única para Fator de Carga
                    ax_hrmotor.legend(labels_hrmotor, loc='upper right', bbox_to_anchor=(1.22, 1.0))

                    # Mostrar o gráfico de barras horizontais
                    col9.pyplot(fig_pulverizador_hrmotor)
                    #############################################################################################################
                    
                    if st.button('Gerar PDF para Tratores'):
                        figures = [fig_pulverizador_combus, fig_pulverizador_factor,  fig_pulverizador_rotacao, fig_pulverizador_autotrac, fig_pulverizador_desloc,fig_pulverizador_hrmotor ]  
                        pdf_buffer = generate_pdf( df_sprayers, figures, background_image_first_page, background_image_other_pages)
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
            selected_columns_utilização = ["Máquina", 
                               "Utilização (Agricultura) Marcha Lenta (%)",
                               "Utilização (Agricultura) Trabalho (%)",
                               "Utilização (Agricultura) Transporte (%)"]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_colheitadeira_utilizacao = df_colheitadeira[selected_columns_utilização].copy()

            # Nomes das máquinas e porcentagens
            maquinas_colheitadeira_util = df_selected_colheitadeira_utilizacao["Máquina"]
            percentual_colheitadeira_util = df_selected_colheitadeira_utilizacao.iloc[:, 1:] * 100

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_colheitadeira_util, width=10)  # Ajuste a largura conforme necessário

            # Plotar gráfico de barras verticais
            fig_colheitadeira_util, ax_colheitadeira_util = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_colheitadeira_util = ['tab:orange', 'tab:green', 'tab:gray']
            labels_colheitadeira_util = ['Marcha Lenta (%)', 'Trabalho (%)', 'Transporte (%)']
            bar_width_colheitadeira_util = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_util = np.arange(len(maquinas_colheitadeira_util))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_util, percentual_colheitadeira_util.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_util)):
                    ax_colheitadeira_util.bar(bar_positions_colheitadeira_util[i] + j * bar_width_colheitadeira_util, percent, width=bar_width_colheitadeira_util, label=labels_colheitadeira_util[j] if i == 0 else "", color=color)
                    ax_colheitadeira_util.text(bar_positions_colheitadeira_util[i] + j * bar_width_colheitadeira_util, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

            # Configurar rótulos e título
            ax_colheitadeira_util.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_util.set_ylabel('Percentual de Utilização (%)')  # Texto do eixo y
            ax_colheitadeira_util.set_xticks(bar_positions_colheitadeira_util + bar_width_colheitadeira_util)
            ax_colheitadeira_util.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_util.set_title('Utilização das Colheitadeiras')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_util.set_yticks(yticks_values)
            ax_colheitadeira_util.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_util.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))


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
                    ax_colheitadeira_factor.text(bar_positions_colheitadeira_factor[i] + j * bar_width_colheitadeira_factor, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

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
                    ax_colheitadeira_combus.text(bar_positions_colheitadeira_combus[i] + j * bar_width_colheitadeira_combus, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10)

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
            df_selected_tractors_rotacao = df_colheitadeira[selected_columns_rotacao].copy()

            # Manter linhas com NaN para visualização em branco
            df_selected_tractors_rotacao.replace([np.inf, -np.inf], np.nan, inplace=True)

            # Nomes das máquinas e rotação média
            maquinas_tractors_rotacao = df_selected_tractors_rotacao["Máquina"]
            rotacoes_tractors = df_selected_tractors_rotacao.iloc[:, 1:]

            # Plotar gráfico de barras horizontais para rotação média
            fig_rotacao, ax_rotacao = plt.subplots(figsize=(12, 8))  # Ajustar o tamanho da figura para evitar erro

            # Aplicar quebra de linha nos nomes das máquinas
            wrapped_labels = wrap_labels(maquinas_tractors_rotacao, width=10)  # Ajuste a largura conforme necessário
            # Cores e labels para as barras de rotação média
            colors_rotacao = ['tab:green', 'tab:gray', 'tab:orange']
            labels_rotacao = ['Trabalhando', 'Transporte','Ocioso']
            bar_height_rotacao = 0.2  # Altura das barras de rotação média
            bar_positions_rotacao = np.arange(len(maquinas_tractors_rotacao))

            # Ajustar as posições das barras para que fiquem separadas
            offset = 0.32
            for j in range(len(labels_rotacao)):
                # Usar np.nan para valores NaN para que apareçam em branco
                ax_rotacao.barh(bar_positions_rotacao + j * offset, 
                                rotacoes_tractors.iloc[:, j].fillna(np.nan), 
                                height=bar_height_rotacao, 
                                label=labels_rotacao[j] if j == 0 else "", 
                                color=colors_rotacao[j])

                # Adicionar rótulos às barras
                for i in range(len(bar_positions_rotacao)):
                    rotacao = rotacoes_tractors.iloc[i, j]
                    if pd.notna(rotacao):  # Apenas adicionar texto se não for NaN
                        ax_rotacao.text((rotacao / 2) + 3,  # Ajuste para mover o texto mais para a direita
                                        bar_positions_rotacao[i] + j * offset, 
                                        f'{rotacao:.0f}', 
                                        ha='center', 
                                        va='center', 
                                        color='black', 
                                        fontsize=10)

            # Configurar os eixos e título
            ax_rotacao.set_xlabel('')
            ax_rotacao.set_yticks(bar_positions_rotacao + offset)
            ax_rotacao.set_yticklabels(maquinas_tractors_rotacao)
            ax_rotacao.set_yticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_rotacao.set_title('Rotação Média do Motor RPM')

            # Verificar se os valores para definir os limites do eixo são válidos
            max_value = rotacoes_tractors.stack().max() if not rotacoes_tractors.empty else 0
            ax_rotacao.set_xlim([0, max_value * 1.1])

            # Adicionar legenda única para rotação média
            ax_rotacao.legend(labels_rotacao, loc='upper right', bbox_to_anchor=(1.2, 1.0))

            # Mostrar o gráfico de rotação média
            col7.pyplot(fig_rotacao)

            #####################################################################################################################
            selected_columns_colheitadeira_desloc = ["Máquina", 
                               "Velocidade Média de Deslocamento (km/h)",
                               "Velocidade Média de Deslocamento Trabalhando (km/h)"
                               ]

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
            labels_colheitadeira_desloc = [ 'Trabalhando (km/h)','Deslocamento (km/h)']
            bar_width_colheitadeira_desloc = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_colheitadeira_desloc = np.arange(len(maquinas_colheitadeira_desloc))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_colheitadeira_desloc, percentual_colheitadeira_desloc.values)):
                for j, (percent, color) in enumerate(zip(row, colors_colheitadeira_desloc)):
                    ax_colheitadeira_desloc.bar(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent, width=bar_width_colheitadeira_desloc, label=labels_colheitadeira_desloc[j] if i == 0 else "", color=color)
                    ax_colheitadeira_desloc.text(bar_positions_colheitadeira_desloc[i] + j * bar_width_colheitadeira_desloc, percent + 1, f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10)

            # Configurar rótulos e título
            ax_colheitadeira_desloc.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_desloc.set_ylabel('')  # Texto do eixo y
            ax_colheitadeira_desloc.set_xticks(bar_positions_colheitadeira_desloc + bar_width_colheitadeira_desloc)
            ax_colheitadeira_desloc.set_xticklabels(maquinas_colheitadeira_desloc)
            ax_colheitadeira_desloc.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_desloc.set_title('Velocidade de Deslocamento km/h')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 13, 2)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_desloc.set_yticks(yticks_values)
            ax_colheitadeira_desloc.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_desloc.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
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
                    ax_colheitadeira_autotrac.text(bar_positions_colheitadeira_autotrac[i] + j * bar_width_colheitadeira_autotrac, percent + 1, f'{percent:.1f}%', ha='center', va='bottom', color='black', fontsize=10)

            # Configurar rótulos e título
            ax_colheitadeira_autotrac.set_xlabel('Máquinas')  # Texto do eixo x
            ax_colheitadeira_autotrac.set_ylabel('')  # Texto do eixo y
            ax_colheitadeira_autotrac.set_xticks(bar_positions_colheitadeira_desloc + bar_width_colheitadeira_desloc)
            ax_colheitadeira_autotrac.set_xticklabels(maquinas_colheitadeira_desloc)
            ax_colheitadeira_autotrac.set_xticklabels(wrapped_labels)  # Usar labels com quebra de linha
            ax_colheitadeira_autotrac.set_title('Velocidade de Deslocamento km/h')

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, 101, 10)  # Ajuste conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_colheitadeira_autotrac.set_yticks(yticks_values)
            ax_colheitadeira_autotrac.set_yticklabels(yticks_labels)

            # Adicionar legenda única
            ax_colheitadeira_autotrac.legend(loc='upper right', bbox_to_anchor=(1.24, 1.0))
            col8.pyplot(fig_colheitadeira_autotrac)

            ######################################################################################################################################################
            # Definir os dados
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
            bars = ax_hrmotor.barh(maquinas_tractors_hrmotor, horas_operacao_hrmotor, height=0.4, color='green')
            labels_hrmotor = ['Hr de operação']

            # Adicionar os números de horas formatados no final de cada barra
            for bar, hora in zip(bars, horas_operacao_hrmotor):
                ax_hrmotor.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height() / 2, f'{hora:.2f} h',
                                va='center', ha='left', fontsize=10)

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

            if st.button('Gerar PDF para Tratores'):
                        figures = [ fig_colheitadeira_util, fig_colheitadeira_factor, fig_colheitadeira_combus, fig_rotacao, fig_colheitadeira_autotrac, fig_colheitadeira_desloc, fig_hrmotor]  
                        pdf_buffer = generate_pdf( df_colheitadeira, figures, background_image_first_page, background_image_other_pages)
                        st.download_button(
                            label="Baixar PDF",
                            data=pdf_buffer,
                            file_name="relatorio_colheitadeira.pdf",
                            mime="application/pdf"
                        )
else:
    st.error("Página não encontrada.")
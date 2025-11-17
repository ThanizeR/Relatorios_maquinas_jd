selected_columns_media_oleo = [
                "Máquina",
                "Temperatura Máx. do Líq. de Arrefecimento Período (°C)",
                "Temp. Média do Líq. de Arref. Período (°C)",
                "Temperatura Máx. do Óleo da Transm. Período (°C)",
                "Temp. Média do Óleo da Transm. Período (°C)",
                "Temp. Máx. do Óleo Hidráulico Período (°C)",
                "Temp. Média do Óleo Hidráulico Período (°C)"
            ]

            # Filtrar o DataFrame para as colunas selecionadas
            df_selected_tractors_media_oleo = df_tractors[selected_columns_media_oleo].copy()

            # Ordenar o DataFrame de forma decrescente baseado 
            df_selected_tractors_media_oleo = df_selected_tractors_media_oleo.sort_values(by="Temperatura Máx. do Líq. de Arrefecimento Período (°C)", ascending=False)

            # Nomes das máquinas e porcentagens
            maquinas_tractors_media_oleo = df_selected_tractors_media_oleo["Máquina"]
            percentual_tractors_media_oleo = df_selected_tractors_media_oleo.iloc[:, 1:]
            wrapped_labels = wrap_labels(maquinas_tractors_media_oleo, width=10)

            # Plotar gráfico de barras verticais
            fig_media_oleo, ax_media_oleo = plt.subplots(figsize=(12, 8))

            # Cores e labels para as barras
            colors_media_oleo = ["#026e02", "#00ff2a", "#d1a700", "#fff674", "#000e8d", "#5cc3ff"]
            labels_media_oleo = ['Máxima Líq. de Arref. Período (°C)','Média Líq. de Arref. Período (°C)', 'Máxima Óleo da Transm. Período (°C)', 'Média Óleo da Transm. Período (°C)', 'Máxima Óleo Hidráulico Período (°C)', 'Média Óleo Hidráulico Período (°C)']
            bar_width_media_oleo = 0.1  # Largura das barras

            # Definir posições das barras para cada grupo de dados
            bar_positions_tractors_media_oleo = np.arange(len(maquinas_tractors_media_oleo))

            # Plotar as barras verticais combinadas para cada máquina
            for i, (maquina, row) in enumerate(zip(maquinas_tractors_media_oleo, percentual_tractors_media_oleo.values)):
                for j, (percent, color) in enumerate(zip(row, colors_media_oleo)):
                    ax_media_oleo.bar(
                        bar_positions_tractors_media_oleo[i] + j * bar_width_media_oleo,
                        percent,
                        width=bar_width_media_oleo,
                        label=labels_media_oleo[j] if i == 0 else "",
                        color=color
                    )
                    ax_media_oleo.text(
                        bar_positions_tractors_media_oleo[i] + j * bar_width_media_oleo,
                        percent + 1,
                        f'{percent:.1f}', ha='center', va='bottom', color='black', fontsize=10, fontweight='bold'
                    )

            # Configurar rótulos e título
            ax_media_oleo.set_xlabel('')  # Eixo X em negrito
            ax_media_oleo.set_ylabel('')  # Eixo Y em negrito
            ax_media_oleo.set_xticks(bar_positions_tractors_media_oleo + bar_width_media_oleo)
            ax_media_oleo.set_xticklabels(wrapped_labels)  # Rótulos em negrito
            ax_media_oleo.set_title('Temparatura máxima e média do motor')  # Título em negrito

            # Definir os limites do eixo Y de forma adaptativa
            max_value_media_oleo = percentual_tractors_media_oleo.max().max()  # Obtém o valor máximo dos dados
            if max_value_media_oleo <= 15:
                y_limit_media_oleo = 15
            elif max_value_media_oleo <= 25:
                y_limit_media_oleo = 25
            elif max_value_media_oleo <= 50:
                y_limit_media_oleo = 50
            elif max_value_media_oleo <= 75:
                y_limit_media_oleo = 75
            else:
                y_limit_media_oleo = 100

            ax_media_oleo.set_ylim(0, y_limit_media_oleo)  # Define o limite do eixo Y

            # Definir as numerações do eixo y
            yticks_values = np.arange(0, y_limit_media_oleo + 1, 10)  # Ajusta conforme necessário
            yticks_labels = [f'{val:.1f}' for val in yticks_values]
            ax_media_oleo.set_yticks(yticks_values)
            ax_media_oleo.set_yticklabels(yticks_labels)  # Rótulos do eixo Y em negrito

            # Adicionar legenda única
            ax_media_oleo.legend(loc='upper right', bbox_to_anchor=(1.37, 1.0))  # Legenda em negrito
            col10, col12 = st.columns(2)
            col10.pyplot(fig_media_oleo)

            ##################################################################

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

            # Verifica se há dados, caso contrário, cria DataFrame vazio com colunas definidas
            # Verifica se o DataFrame existe e contém dados
            try:
                df_selected_patinagem = df_tractors[selected_columns_patinagem].copy()
            except NameError:
                df_selected_patinagem = pd.DataFrame(columns=selected_columns_patinagem)

            # Substitui valores infinitos por NaN e preenche NaNs com zero para não quebrar o gráfico
            df_selected_patinagem.replace([np.inf, -np.inf], np.nan, inplace=True)
            df_selected_patinagem.fillna(0, inplace=True)

            # Define máquinas e valores de patinagem com dados padrão, caso não haja dados válidos
            if df_selected_patinagem.empty or df_selected_patinagem.isnull().all().all():
                maquinas = ["Máquina 1", "Máquina 2", "Máquina 3"]
                patinagem_values = pd.DataFrame(0, index=range(len(maquinas)), columns=selected_columns_patinagem[1:])
            else:
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

            # Configurações das barras
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

            # Define limites do eixo Y com base em `max_value`, ou define padrão se `max_value` for inválido
            if pd.notna(max_value) and max_value != 0:
                if max_value <= 5:
                    y_limit = 5
                    y_ticks = [0, 5]
                elif max_value <= 10:
                    y_limit = 10
                    y_ticks = [0, 5, 10]
                elif max_value <= 20:
                    y_limit = 20
                    y_ticks = np.arange(0, 21, 5)
                elif max_value <= 30:
                    y_limit = 30
                    y_ticks = np.arange(0, 31, 5)
                elif max_value <= 50:
                    y_limit = 50
                    y_ticks = np.arange(0, 51, 10)
                elif max_value <= 75:
                    y_limit = 75
                    y_ticks = np.arange(0, 76, 15)
                else:
                    y_limit = 100
                    y_ticks = np.arange(0, 101, 20)
            else:
                y_limit = 5
                y_ticks = [0, 5]  # Define limite padrão se `max_value` for NaN ou zero

            # Define o limite do eixo Y
            ax_patinagem.set_ylim(0, y_limit)
            ax_patinagem.set_yticks(y_ticks)
            for y in y_ticks:
                ax_patinagem.axhline(y, color='gray', linestyle='--', linewidth=0.5)

            # Configuração dos eixos e título
            ax_patinagem.set_ylabel('Tempo de Patinagem (h)')
            ax_patinagem.set_xticks([i * (len(colors) * (bar_width + space_between_bars) + machine_offset) + (len(colors) * (bar_width + space_between_bars) - space_between_bars) / 2 for i in range(len(maquinas))])
            ax_patinagem.set_xticklabels(wrapped_labels, rotation=45, ha='right')
            ax_patinagem.set_title('Tempo de Patinagem das Rodas por Máquina - Tratores')

            # Adicionar legenda única para Patinagem na ordem correta
            handles, legend_labels = ax_patinagem.get_legend_handles_labels()
            if handles and legend_labels:
                sorted_handles_labels = sorted(zip(handles, labels), key=lambda x: labels.index(x[1]))
                handles, legend_labels = zip(*sorted_handles_labels)
                ax_patinagem.legend(handles, legend_labels, loc='upper right', bbox_to_anchor=(1.25, 1.0))

            # Exibe o gráfico no Streamlit
            st.pyplot(fig_patinagem)

 # -----------------------------------------
    # 3️⃣ Terceira página – 2 gráficos lado a lado
    # (média do motor e patinagem)
    # -----------------------------------------
        # Página 1 - Gráfico de Média do Motor
    set_background(2)

    # Dimensões para gráfico centralizado e grande
    graph_width = page_width - 2 * x_margin - 100
    graph_height = graph_width * 0.65
    y_pos = (page_height - graph_height) / 2

    # Renderizar gráfico de média do motor
    fig_media_motor = figures[6]
    img_media_motor = BytesIO()
    fig_media_motor.savefig(img_media_motor, format='png', bbox_inches='tight')
    img_media_motor.seek(0)
    c.drawImage(ImageReader(img_media_motor),
                x_margin + 50, y_pos,
                width=graph_width, height=graph_height)
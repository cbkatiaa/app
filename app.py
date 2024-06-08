# -*- coding: utf-8 -*-

import pandas as pd
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib.colors import LinearSegmentedColormap

# Configurar el alcance y credenciales para la API de Google Sheets
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Conectar a Google Sheets usando la clave del archivo
file_key = '13hOEzyecNB-3SdKE3qnIHKRPRWtkTqdz66VHEhqdtWA'
sheet = client.open_by_key(file_key).sheet1

# Obtener datos de la hoja y convertirlos a un DataFrame
df = pd.DataFrame(sheet.get_all_records())

# Filtrar las temporadas y posiciones disponibles
temporadas = df['Season'].unique()
posiciones = df['Primary Position'].unique()

# Crear selectores en Streamlit
temporada_seleccionada = st.selectbox("Selecciona la temporada", temporadas)
posicion_seleccionada = st.selectbox("Selecciona la posición", posiciones)

# Filtrar el DataFrame basado en la selección de temporada y posición
df_filtrado = df[(df['Season'] == temporada_seleccionada) & (df['Primary Position'] == posicion_seleccionada)]
jugadores = df_filtrado['Name'].unique()
jugador_seleccionado = st.selectbox("Seleccione al jugador", jugadores)

# Función para generar el análisis de porteros
def iqindportero(df, j1):
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.3)

    bar1 = ['Despejes', 'Despejes exitosos']
    bar2 = ['Salidas (centros)', 'Despejes p90']
    bar3 = ['Duelos aéreos ganados', 'Éxito duelos aéreos']
    bar4 = ['Pases', '% pases bajo presión', 'Éxito pases', 'Distancia de pases bajo presión', 'Éxito pases largos', 'Distancia conducciones']
    bar5 = ['PS xG vs xG', 'PS xG', 'Goles encajados', 'Portería a 0']

    ti1 = 'Acciones aéreas'
    ti2 = 'Despejes'
    ti3 = 'Juego aéreo'
    ti4 = 'Distribución'
    ti5 = 'Rendimiento en portería'

    c1 = 'white'
    y1 = -3
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))

    plt.rcParams["font.family"] = "Century Gothic"

    # Crear métricas específicas para porteros
    df['PS xG vs xG'] = df['PSxG'] / df['xG']
    df['Calidad definición'] = df['PS xG vs xG'].rank(pct=True)
    df['PS xG'] = df['PSxG'].rank(pct=True)
    df['Salidas (centros)'] = df['Crosses Stopped'].rank(pct=True)
    df['Goles encajados'] = df['GA'].rank(pct=True)
    df['Portería a 0'] = df['Clean Sheets'].rank(pct=True)
    df['Paradas'] = df['Saves'].rank(pct=True)
    df['% paradas'] = df['Save%'].rank(pct=True)
    df['Pases al área'] = df['OP Passes Into Box'].rank(pct=True)
    df['Despejes'] = df['PAdj Clearances'].rank(pct=True)
    df['Éxito duelos aéreos'] = df['Aerial Duel%'].rank(pct=True)
    df['Duelos aéreos ganados'] = df['Aerial Duels Won'].rank(pct=True)
    df['Distancia de pases bajo presión'] = df['Avg Pr. Pass Distance'].rank(pct=True)
    df['Éxito pases largos'] = df['Long Pass %'].rank(pct=True)
    df['Distancia conducciones'] = df['Dribble Distance'].rank(pct=True)

    df = df.loc[df['Name'] == j1]
    df = df.set_index('Name').transpose()

     def plot_bar(ax, bar_data, title):
        ax.set_facecolor(c1)
        ax.set_xlim(0, 1)
        ax.set_ylim(-1, len(bar_data))
        ax.set_xticklabels([])
        ax.yaxis.set_ticks_position('none')
        df1 = df.reindex(bar_data)
        df1 = df1.reindex(index=df1.index[::-1])
        df1 = df1.reset_index()
        x = df1['index']
        y = df1[j1]
        data_color = y
        normmin = 0
        normmax = 1
        data_color = [(x - normmin) / (normmax - normmin) for x in data_color]
        cmap = LinearSegmentedColormap.from_list('rg', ["darkred", "red", "salmon", "yellowgreen", "green", "darkgreen"], N=256)
        cmap_invertida = LinearSegmentedColormap.from_list('rg', ["darkgreen", "green", "yellowgreen", "salmon", "red", "darkred"], N=256)
        for data in bar_data:
            if bar_data == 'Pases hacia peligro %' or bar_data == 'Pass into Danger%':
                colors = cmap_invertida(data_color)
            else:
                colors = cmap(data_color)
        ax.barh(x, y, color=colors, zorder=2, edgecolor='none')
        for c in ax.containers:
            labels = [(y * 100).astype(int) if y > .05 else "" for y in c.datavalues]
            ax.bar_label(c, labels=labels, label_type='edge', color='w', size=txs, fontweight='bold', padding=padr)
        for s in ['top', 'bottom', 'left', 'right']:
            ax.spines[s].set_visible(False)
        ax.set_yticklabels(df1['index'], color='black', size=20, fontname='Century Gothic', va='center')
        ax.yaxis.set_tick_params(pad=15)
        ax.set_title(title, color='black', size=22, x=0, y=0.93, ha='left', fontname='Century Gothic', fontweight='semibold')
        ax.set_xticks([0.5])
        ax.grid(color='grey', axis='x', which='major')

    plot_bar(ax1, bar1, ti1)
    plot_bar(ax2, bar2, ti2)

    ax6.set_title(ti6, color='black', size=22, x=0.05, y=0.9, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax6.axis('off')
    ax7.set_title(ti7, color='black', size=22, x=0.05, y=1, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax7.axis('off')

    return fig


# Función para generar el análisis de centrales
def iqindcentral(df, j1):
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.3)

    bar1 = ['Intercepciones', 'Entradas', 'Presiones', 'Altura de presiones', 'Entradas e Intercepciones p90']
    bar2 = ['Bloqueos de pases', 'Bloqueos de tiros', 'Duelos defensivos', 'Éxito duelos defensivos']
    bar3 = ['Duelos aéreos defensivos', 'Duelos aéreos ofensivos', 'Duelos aéreos totales']
    bar4 = ['Pases', 'Pases al área', 'Pases largos sin presión', 'Pérdidas', 'Pases progresivos']
    bar5 = ['Goles', 'Asistencias', 'xG', 'xA']

    ti1 = 'Acciones defensivas activas'
    ti2 = 'Acciones defensivas en la última línea'
    ti3 = 'Juego aéreo'
    ti4 = 'Distribución'
    ti5 = 'Contribuciones ofensivas'

    c1 = 'white'
    y1 = -3
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))

    plt.rcParams["font.family"] = "Century Gothic"

    # Crear métricas específicas para centrales
    df['Press %']=df['Pressure Regains']/df['Pressures']
    df['Éxito duelos aéreos']=df['Aerial Win%'].rank(pct=True)
    df['Duelos aéreos ganados']=df['Aerial Wins'].rank(pct=True)
    df['Acciones agresivas']=df['Aggressive Actions'].rank(pct=True)
    df['Asistencias Torneo']=df['Assists'].rank(pct=True)
    df['Asistencias Jugada Abierta p90']=df['OP Assists'].rank(pct=True)
    df['Promedio minutos jugados por partido']=df['Minutes'].rank(pct=True)
    df['Pases hacia atrás %']=df['Pass Backward%'].rank(pct=True)
    df['Pases hacia adelante %']=df['Pass Forward%'].rank(pct=True)
    df['Balones recuperados']=df['Ball Recoveries'].rank(pct=True)
    df['Tiros bloqueados']=df['Blocks/Shot'].rank(pct=True)
    #df['Éxito de centros']=df['player_season_box_cross_ratio'].rank(pct=True)
    df['Acarreos']=df['Carries'].rank(pct=True)
    df['Distancia de conducciones']=df['Carry Length'].rank(pct=True)
    df['Acarreos exitosos']=df['Carry%'].rank(pct=True)
    df['Éxito 1vs1 defensivo']=df['Tack/DP%'].rank(pct=True)
    df['Dif éxito pases BP']=df['Pr. Pass% Dif.'].rank(pct=True)
    #df['Salidas de portero (centros)']=df['player_season_clcaa'].rank(pct=True)
    df['Despejes p90']=df['Clearances'].rank(pct=True)
    df['Tiros convertidos en gol %']=df['Shooting%'].rank(pct=True)
    df['Balones disputados ganados p90']=df['Counterpress Regains'].rank(pct=True)
    df['Contrapresiones']=df['Counterpressures'].rank(pct=True)
    df['Centros']=df['Successful Crosses'].rank(pct=True)
    df['Éxito centros']=df['Crossing%'].rank(pct=True)
    df['Pases en profundidad exitosos']=df['Deep Completions'].rank(pct=True)
    df['Progresiones al último tercio']=df['Deep Progressions'].rank(pct=True)
    df['Balones perdidos en disputa']=df['Dispossessed'].rank(pct=True)
    df['Éxito de regates']=df['Dribble%'].rank(pct=True)
    df['Regates']=df['Successful Dribbles'].rank(pct=True)
    df['Pases hacia atrás 3/3 %']=df['F3 Pass Backward%'].rank(pct=True)
    df['Pases hacia adelante 3/3 %']=df['F3 Pass Forward%'].rank(pct=True)
    df['Pases último tercio']=df['OP F3 Passes'].rank(pct=True)
    df['Balones recuperados campo rival']=df['Ball Recov. F2'].rank(pct=True)
    df['Faltas cometidas']=df['Fouls'].rank(pct=True)
    df['Faltas recibidas']=df['Fouls Won'].rank(pct=True)
    df['Intercepciones p90']=df['Interceptions'].rank(pct=True)
    df['% pases con zurdo']=df['L/R Footedness%'].rank(pct=True)
    df['Éxito pases largos']=df['Long Ball%'].rank(pct=True)
    df['Pases largos']=df['Long Balls'].rank(pct=True)
    df['Tiros']=df['Shots'].rank(pct=True)
    df['xG']=df['xG'].rank(pct=True)
    df['xG por tiro']=df['xG/Shot'].rank(pct=True)
    df['Goles (sin penales)']=df['NP Goals'].rank(pct=True)
    df['Contribución de gol']=df['xG & xG Assisted'].rank(pct=True)
    df['xG post-tiro']=df['PSxG'].rank(pct=True)
    df['OBV total']=df['OBV'].rank(pct=True)
    df['OBV pases']=df['Pass OBV'].rank(pct=True)
    df['OBV tiros']=df['Shot OBV'].rank(pct=True)
    df['OBV acciones defensivas']=df['DA OBV'].rank(pct=True)
    df['OBV conducciones y regates']=df['D&C OBV'].rank(pct=True)
    df['OBV portero']=df['Goalkeeper OBV'].rank(pct=True)
    df['Distancia de pases bajo presión']=df['Pr. Pass Length Dif.'].rank(pct=True)
    df['Despejes']=df['PAdj Clearances'].rank(pct=True)
    df['Intercepciones']=df['PAdj Interceptions'].rank(pct=True)
    df['Presiones']=df['PAdj Pressures'].rank(pct=True)
    df['Altura de presiones']=df['Average Pressure X'].rank(pct=True)
    df['Entradas']=df['Tackles'].rank(pct=True)
    df['Entradas e Intercepciones p90']=df['Tack&Int'].rank(pct=True)
    df['Pases']=df['OP Passes'].rank(pct=True)
    df['Pases dentro del área']=df['Passes Inside Box'].rank(pct=True)
    df['Pases al área']=df['OP Passes Into Box'].rank(pct=True)
    df['% pases bajo presión']=df['Passes Pressured%'].rank(pct=True)
    df['Éxito pases']=df['Passing%'].rank(pct=True)
    df['xA']=df['xG Assisted'].rank(pct=True)
    df['Pases largos sin presión']=df['UPr. Long Balls'].rank(pct=True)
    df['Pérdidas']=df['Turnovers'].rank(pct=True)
    df['Toques en el área']=df['Touches In Box'].rank(pct=True)
    df['Pases filtrados']=df['Throughballs'].rank(pct=True)
    df['% tiros a puerta']=df['Shot Touch%'].rank(pct=True)
    df['Presiones p90']=df['Pressures'].rank(pct=True)
    df['Éxito pases bajo presión']=df['Pr. Pass%'].rank(pct=True)
    df['Pases largos bajo presión']=df['Pr. Long Balls'].rank(pct=True)
    df['Dif. distancia de pases bajo presión']=df['Pr. Pass% Dif.'].rank(pct=True)
    df['Recuperación tras presión']=df['Pressure Regains'].rank(pct=True)
    df['Recuperación tras presión %']=df['Press %'].rank(pct=True)
    df['Presiones cancha rival']=df['Pressures F2'].rank(pct=True)
    df['PS xG vs xG']=df['PSxG']/df['xG']
    df['Calidad definición']=df['PS xG vs xG'].rank(pct=True)
    df['Carry length total']=df['Carries']*df['Carry Length']
    df['Distancia conducciones']=df['Carry length total'].rank(pct=True)
    df['Long balls total']=(df['Long Balls']/df['Long Ball%'])*100
    df['Long balls per pass']=df['Long balls total']/df['OP Passes']
    df['Pases largos por pases']=df['Long balls per pass'].rank(pct=True)
    df['% pases con zurdo']=df['L/R Footedness%']/100

    df = df.loc[df['Name'] == j1]
    df = df.set_index('Name').transpose()

    def plot_bar(ax, bar_data, title):
        ax.set_facecolor(c1)
        ax.set_xlim(0, 1)
        ax.set_ylim(-1, len(bar_data))
        ax.set_xticklabels([])
        ax.yaxis.set_ticks_position('none')

        df1 = df.reindex(bar_data).reindex(index=bar_data[::-1]).reset_index()
        x = df1['index']
        y = df1[j1]

        data_color = [(x - 0) / (1 - 0) for x in y]
        cmap = LinearSegmentedColormap.from_list('rg', ["darkred", "red", "salmon", "yellowgreen", "green", "darkgreen"], N=256)
        
        colors = [cmap(val) for val in data_color]
        ax.barh(x, y, color=colors, zorder=2, edgecolor='none')
        
        for container in ax.containers:
            labels = [(val * 100).astype(int) if val > .05 else "" for val in container.datavalues]
            ax.bar_label(container, labels=labels, label_type='edge', color='w', size=txs, fontweight='bold', padding=padr)

        for spine in ['top', 'bottom', 'left', 'right']:
            ax.spines[spine].set_visible(False)

        ax.set_yticklabels(df1['index'], color='black', size=20, fontname='Century Gothic', va='center')
        ax.yaxis.set_tick_params(pad=15)
        ax.set_title(title, color='black', size=22, x=0, y=0.93, ha='left', fontname='Century Gothic', fontweight='semibold')
        ax.set_xticks([0.5])
        ax.grid(color='grey', axis='x', which='major')

    # Generar gráficos para cada categoría
    plot_bar(axs[0, 0], bar1, ti1)
    plot_bar(axs[0, 1], bar2, ti2)
    plot_bar(axs[0, 2], bar3, ti3)
    plot_bar(axs[1, 0], bar4, ti4)
    plot_bar(axs[1, 1], bar5, ti5)

    axs[1, 2].axis('off')

    return fig

# Generar el análisis cuando se presiona el botón
if st.button("Generar Análisis"):
    if posicion_seleccionada == "Portero":
        fig = iqindportero(df_filtrado, jugador_seleccionado)
    else:
        fig = iqindcentral(df_filtrado, jugador_seleccionado)
    st.pyplot(fig)


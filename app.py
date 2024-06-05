# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mp
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def iqindportero(df, j1):
    c = 'white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh = 16
    ax0 = plt.subplot2grid(shape=(sh, 7), loc=(0, 0), colspan=4, rowspan=3)
    ax1 = plt.subplot2grid(shape=(sh, 7), loc=(3, 0), colspan=4, rowspan=5)
    ax2 = plt.subplot2grid(shape=(sh, 7), loc=(8, 0), colspan=4, rowspan=8)
    ax6 = plt.subplot2grid(shape=(sh, 7), loc=(0, 4), colspan=3, rowspan=7)
    ax7 = plt.subplot2grid(shape=(sh, 7), loc=(9, 4), colspan=3, rowspan=7)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.3)

    bar1 = ['Goles parados', 'Calidad de posicionamiento', 'Salidas de portero (centros)', 'Salidas de libero del portero']
    bar2 = ['Pases', '% pases con zurdo', 'Éxito pases', '% pases son largos', 'Éxito pases largos', 'Éxito pases bajo presión', 'Pases hacia peligro %']

    ti1 = 'Acciones del portero'
    ti2 = 'Posesión'
    ti6 = 'Tiros en contra'
    ti7 = 'Penales en contra'

    c1 = 'white'
    txs = 22
    padr = -45

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.76, 0.76], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))

    plt.rcParams["font.family"] = "Century Gothic"

    df['Long balls total'] = (df['Long Balls'] / df['Long Ball%']) * 100
    df['Long balls per pass'] = df['Long balls total'] / df['OP Passes']
    df['% pases son largos'] = df['Long balls per pass'].rank(pct=True)
    df['Goles parados'] = df['GSAA'].rank(pct=True)
    df['OBV portero'] = df['Goalkeeper OBV'].rank(pct=True)
    df['Salidas de libero del portero'] = df['GK Aggressive Dist.'].rank(pct=True)
    df['Salidas de portero (centros)'] = df['Claims%'].rank(pct=True)
    df['Pases hacia peligro %'] = df['Pass into Danger%'].rank(pct=True)
    df['Calidad de posicionamiento'] = 1 - (df['Positioning Error'].rank(pct=True))
    df['Pases'] = df['OP Passes'].rank(pct=True)
    df['Éxito pases largos'] = df['Long Ball%'].rank(pct=True)
    df['Éxito pases'] = df['Passing%'].rank(pct=True)
    df['Éxito pases bajo presión'] = df['Pr. Pass%'].rank(pct=True)
    df['% pases con zurdo'] = df['L/R Footedness%'] / 100

    df = df.loc[df['Name'] == j1]
    df = df.set_index('Name')
    df = df.transpose()

    ax0.axis('off')

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

def iqindcentral(df, j1):
    c = 'white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh = 33
    ax0 = plt.subplot2grid(shape=(sh, 7), loc=(0, 0), colspan=4, rowspan=6)
    ax1 = plt.subplot2grid(shape=(sh, 7), loc=(6, 0), colspan=4, rowspan=9)
    ax2 = plt.subplot2grid(shape=(sh, 7), loc=(15, 0), colspan=4, rowspan=3)
    ax3 = plt.subplot2grid(shape=(sh, 7), loc=(18, 0), colspan=4, rowspan=3)
    ax4 = plt.subplot2grid(shape=(sh, 7), loc=(21, 0), colspan=4, rowspan=9)
    ax5 = plt.subplot2grid(shape=(sh, 7), loc=(30, 0), colspan=4, rowspan=3)
    ax6 = plt.subplot2grid(shape=(sh, 7), loc=(2, 4), colspan=3, rowspan=1)
    ax7 = plt.subplot2grid(shape=(sh, 7), loc=(3, 4), colspan=3, rowspan=12)
    ax8 = plt.subplot2grid(shape=(sh, 7), loc=(18, 4), colspan=3, rowspan=1)
    ax9 = plt.subplot2grid(shape=(sh, 7), loc=(19, 4), colspan=3, rowspan=12)
    fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.05, hspace=0.3)

    bar1 = ['Presiones', 'Altura de presiones', 'Acciones agresivas', 'Recuperación tras presión %', 'Contrapresiones', 'Entradas', 'Éxito 1vs1 defensivo', 'Intercepciones']
    bar2 = ['Despejes', 'Calidad despejes', 'Duelos aéreos defensivos', 'Duelos aéreos ofensivos']
    bar3 = ['Goles', 'xG', 'Remates', 'Asistencias', 'xA', 'Acciones Generación de Disparo', 'Tiros al área', 'Pases al área', 'Conducciones al área']
    bar4 = ['% acierto pases', 'Pases', 'Distancia pases', 'Pases largos %', 'Pases Peligro %', 'Pases entre líneas', 'Distancia progresiva', 'Distancia progresiva/90']
    bar5 = ['Faltas cometidas', 'Penales cometidos', 'Errores']

    ti1 = 'Presión'
    ti2 = 'Defensa'
    ti3 = 'Ataque'
    ti4 = 'Posesión'
    ti5 = 'Disciplina'
    ti6 = 'Tiros en contra'
    ti7 = 'Penales en contra'

    c1 = 'white'
    txs = 22
    padr = -45

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.91, 0.91], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))

    plt.rcParams["font.family"] = "Century Gothic"

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
    df = df.set_index('Name')
    df = df.transpose()

    ax0.axis('off')

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
            if bar_data == 'Pases Peligro %':
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
    plot_bar(ax4, bar3, ti3)
    plot_bar(ax5, bar5, ti5)
    plot_bar(ax3, bar4, ti4)

    ax6.set_title(ti6, color='black', size=22, x=0.05, y=0.9, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax6.axis('off')
    ax7.set_title(ti7, color='black', size=22, x=0.05, y=1, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax7.axis('off')

    return fig


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)


file_key = '13hOEzyecNB-3SdKE3qnIHKRPRWtkTqdz66VHEhqdtWA'


sheet = client.open_by_key(file_key).sheet1


df = pd.DataFrame(sheet.get_all_records())


temporadas = df['Season'].unique()
posiciones = df['Primary Position'].unique()

temporada_seleccionada = st.selectbox("Selecciona la temporada", temporadas)
posicion_seleccionada = st.selectbox("Selecciona la posición", posiciones)

df_filtrado = df[(df['Season'] == temporada_seleccionada) & (df['Primary Position'] == posicion_seleccionada)]
jugadores = df_filtrado['Name'].unique()
jugador_seleccionado = st.selectbox("Seleccione al jugador", jugadores)


if st.button("Generar Análisis"):
    if posicion_seleccionada == "Goalkeeper":
        fig = iqindportero(df_filtrado, jugador_seleccionado)
    else:
        fig = iqindcentral(df_filtrado, jugador_seleccionado)
    st.pyplot(fig)

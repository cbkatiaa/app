# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:36:22 2024

@author: katia
"""

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

    df['Presiones'] = df['Pressures'].rank(pct=True)
    df['Altura de presiones'] = df['Height Pressures'].rank(pct=True)
    df['Acciones agresivas'] = df['Aggressive Actions'].rank(pct=True)
    df['Recuperación tras presión %'] = df['Pressures Recovery %'].rank(pct=True)
    df['Contrapresiones'] = df['Counter Pressures'].rank(pct=True)
    df['Entradas'] = df['Tackles'].rank(pct=True)
    df['Éxito 1vs1 defensivo'] = df['Defensive 1vs1 Success %'].rank(pct=True)
    df['Intercepciones'] = df['Interceptions'].rank(pct=True)
    df['Despejes'] = df['Clearances'].rank(pct=True)
    df['Calidad despejes'] = 1 - df['Clearance Errors'].rank(pct=True)
    df['Duelos aéreos defensivos'] = df['Aerial Duels Defensive'].rank(pct=True)
    df['Duelos aéreos ofensivos'] = df['Aerial Duels Offensive'].rank(pct=True)
    df['Goles'] = df['Goals'].rank(pct=True)
    df['xG'] = df['xG'].rank(pct=True)
    df['Remates'] = df['Shots'].rank(pct=True)
    df['Asistencias'] = df['Assists'].rank(pct=True)
    df['xA'] = df['xA'].rank(pct=True)
    df['Acciones Generación de Disparo'] = df['Shot Creating Actions'].rank(pct=True)
    df['Tiros al área'] = df['Shots to Box'].rank(pct=True)
    df['Pases al área'] = df['Passes to Box'].rank(pct=True)
    df['Conducciones al área'] = df['Carries to Box'].rank(pct=True)
    df['% acierto pases'] = df['Passing %'].rank(pct=True)
    df['Pases'] = df['Passes'].rank(pct=True)
    df['Distancia pases'] = df['Passing Distance'].rank(pct=True)
    df['Pases largos %'] = df['Long Pass %'].rank(pct=True)
    df['Pases Peligro %'] = df['Danger Passes %'].rank(pct=True)
    df['Pases entre líneas'] = df['Passes Between Lines'].rank(pct=True)
    df['Distancia progresiva'] = df['Progressive Distance'].rank(pct=True)
    df['Distancia progresiva/90'] = df['Progressive Distance per 90'].rank(pct=True)
    df['Faltas cometidas'] = df['Fouls Committed'].rank(pct=True)
    df['Penales cometidos'] = df['Penalties Committed'].rank(pct=True)
    df['Errores'] = df['Errors'].rank(pct=True)

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

# Google Sheets authentication
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Google Sheets file key
file_key = '13hOEzyecNB-3SdKE3qnIHKRPRWtkTqdz66VHEhqdtWA'

# Open the Google Sheets file and select the worksheet
sheet = client.open_by_key(file_key).sheet1

# Convert worksheet data into DataFrame
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

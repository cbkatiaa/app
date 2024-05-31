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
        inverted_bars = {'Pases hacia peligro %', 'Pass into Danger%'}
        colors = cmap_invertida(data_color) if any(item in bar_data for item in inverted_bars) else cmap(data_color)
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

# Streamlit app
st.title('Análisis de Porteros')

# URL del archivo CSV en GitHub
file_url = 'https://raw.githubusercontent.com/cbkatiaa/app/main/porteros.csv'

# Leer el archivo CSV desde GitHub
df = pd.read_csv(file_url)

# Seleccionar temporada, posición y nombre de portera
temporadas = df['Season'].unique()
posiciones = df['Primary Position'].unique()

temporada_seleccionada = st.selectbox("Selecciona la temporada", temporadas)
posicion_seleccionada = st.selectbox("Selecciona la posición", posiciones)

df_filtrado = df[(df['Season'] == temporada_seleccionada) & (df['Primary Position'] == posicion_seleccionada)]
porteras = df_filtrado['Name'].unique()
portera_seleccionada = st.selectbox("Seleccione al portero", porteras)

if st.button("Generar Análisis"):
    fig = iqindportero(df_filtrado, portera_seleccionada)
    st.pyplot(fig)

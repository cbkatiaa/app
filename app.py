# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import lines
from matplotlib.colors import LinearSegmentedColormap
import matplotlib as mp
import matplotlib.image as mpimg
import os
#from google.colab import drive
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def iqindportero(df, j1, pos):
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

    df_porteros['Long balls total'] = (df_porteros['Long Balls'] / df_porteros['Long Ball%']) * 100
    df_porteros['Long balls per pass'] = df_porteros['Long balls total'] / df_porteros['OP Passes']
    df_porteros['% pases son largos'] = df_porteros['Long balls per pass'].rank(pct=True)
    df_porteros['Goles parados'] = df_porteros['GSAA'].rank(pct=True)
    df_porteros['OBV portero'] = df_porteros['Goalkeeper OBV'].rank(pct=True)
    df_porteros['Salidas de libero del portero'] = df_porteros['GK Aggressive Dist.'].rank(pct=True)
    df_porteros['Salidas de portero (centros)'] = df_porteros['Claims%'].rank(pct=True)
    df_porteros['Pases hacia peligro %'] = df_porteros['Pass into Danger%'].rank(pct=True)
    df_porteros['Calidad de posicionamiento'] = 1 - (df_porteros['Positioning Error'].rank(pct=True))
    df_porteros['Pases'] = df_porteros['OP Passes'].rank(pct=True)
    df_porteros['Éxito pases largos'] = df_porteros['Long Ball%'].rank(pct=True)
    df_porteros['Éxito pases'] = df_porteros['Passing%'].rank(pct=True)
    df_porteros['Éxito pases bajo presión'] = df_porteros['Pr. Pass%'].rank(pct=True)
    df_porteros['% pases con zurdo'] = df_porteros['L/R Footedness%'] / 100

    df_porteros = df_porteros.loc[df_porteros['Name'] == j1]
    df_porteros = df_porteros.set_index('Name')
    df_porteros = df_porteros.transpose()

    ax0.axis('off')

    def plot_bar_portero(ax, bar_data, title):
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
        colors = []
        for i, label in enumerate(df1['index']):
            if label == 'Pases hacia peligro %':
                colors.append(cmap_invertida(data_color[i]))
            else:
                colors.append(cmap(data_color[i]))

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

    plot_bar_portero(ax1, bar1, ti1)
    plot_bar_portero(ax2, bar2, ti2)

    ax6.set_title(ti6, color='black', size=22, x=0.05, y=0.9, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax6.axis('off')
    ax7.set_title(ti7, color='black', size=22, x=0.05, y=1, ha='left', fontname='Century Gothic', fontweight='semibold')
    ax7.axis('off')

    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')

    return fig


def iqindcentral(df, j1, pos):
    c='white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh=33
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
    fig.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.05,
                        hspace=0.3)

    bar1=['Presiones', 'Recuperación tras presión %','Entradas','Éxito 1vs1 defensivo','Intercepciones']
    bar2=['Despejes','Tiros bloqueados','Balones recuperados']
    bar3=['Duelos aéreos ganados', 'Éxito duelos aéreos']
    bar4=['Pases','% pases con zurdo','Éxito pases','Pases largos por pases','Progresiones al último tercio','Éxito pases largos','Éxito pases bajo presión','Distancia conducciones']
    bar5=['xG','Toques en el área']

    t2='Pases'
    t3='Presiones'
    t4='xA'
    t5='Pases progresivos'

    ti1='Defensivo- activo'
    ti2='Defensivo- última línea'
    ti3='Juego aéreo'
    ti4='Posesión'
    ti5='Ofensivo'

    c1 = 'white'
    y1 = -3
    vmax = 4
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))
    #fig.add_artist(lines.Line2D([.6, .91], [.37, 0.37], color='#293A4A', lw=5))

    plt.rcParams["font.family"] = "Century Gothic"


    df['Press %']=df['Pressure Regains']/df['Pressures']
    df['Éxito duelos aéreos'] = df.groupby('Primary Position')['Aerial Win%'].rank(pct=True)
    df['Duelos aéreos ganados']=df.groupby('Primary Position')['Aerial Wins'].rank(pct=True)
    df['Acciones agresivas']=df.groupby('Primary Position')['Aggressive Actions'].rank(pct=True)
    df['Asistencias Torneo']=df.groupby('Primary Position')['Assists'].rank(pct=True)
    df['Asistencias Jugada Abierta p90']=df.groupby('Primary Position')['OP Assists'].rank(pct=True)
    df['Promedio minutos jugados por partido']=df.groupby('Primary Position')['Minutes'].rank(pct=True)
    df['Pases hacia atrás %']=df.groupby('Primary Position')['Pass Backward%'].rank(pct=True)
    df['Pases hacia adelante %']=df.groupby('Primary Position')['Pass Forward%'].rank(pct=True)
    df['Balones recuperados']=df.groupby('Primary Position')['Ball Recoveries'].rank(pct=True)
    df['Tiros bloqueados']=df.groupby('Primary Position')['Blocks/Shot'].rank(pct=True)
    #df['Éxito de centros']=df.groupby('Primary Position')['player_season_box_cross_ratio'].rank(pct=True)
    df['Acarreos']=df.groupby('Primary Position')['Carries'].rank(pct=True)
    df['Distancia de conducciones']=df.groupby('Primary Position')['Carry Length'].rank(pct=True)
    df['Acarreos exitosos']=df.groupby('Primary Position')['Carry%'].rank(pct=True)
    df['Éxito 1vs1 defensivo']=df.groupby('Primary Position')['Tack/DP%'].rank(pct=True)
    df['Dif éxito pases BP']=df.groupby('Primary Position')['Pr. Pass% Dif.'].rank(pct=True)
    #df['Salidas de portero (centros)']=df.groupby('Primary Position')['player_season_clcaa'].rank(pct=True)
    df['Despejes p90']=df.groupby('Primary Position')['Clearances'].rank(pct=True)
    df['Tiros convertidos en gol %']=df.groupby('Primary Position')['Shooting%'].rank(pct=True)
    df['Balones disputados ganados p90']=df.groupby('Primary Position')['Counterpress Regains'].rank(pct=True)
    df['Contrapresiones']=df.groupby('Primary Position')['Counterpressures'].rank(pct=True)
    df['Centros']=df.groupby('Primary Position')['Successful Crosses'].rank(pct=True)
    df['Éxito centros']=df.groupby('Primary Position')['Crossing%'].rank(pct=True)
    df['Pases en profundidad exitosos']=df.groupby('Primary Position')['Deep Completions'].rank(pct=True)
    df['Progresiones al último tercio']=df.groupby('Primary Position')['Deep Progressions'].rank(pct=True)
    df['Balones perdidos en disputa']=df.groupby('Primary Position')['Dispossessed'].rank(pct=True)
    df['Éxito de regates']=df.groupby('Primary Position')['Dribble%'].rank(pct=True)
    df['Regates']=df.groupby('Primary Position')['Successful Dribbles'].rank(pct=True)
    df['Pases hacia atrás 3/3 %']=df.groupby('Primary Position')['F3 Pass Backward%'].rank(pct=True)
    df['Pases hacia adelante 3/3 %']=df.groupby('Primary Position')['F3 Pass Forward%'].rank(pct=True)
    df['Pases último tercio']=df.groupby('Primary Position')['OP F3 Passes'].rank(pct=True)
    df['Balones recuperados campo rival']=df.groupby('Primary Position')['Ball Recov. F2'].rank(pct=True)
    df['Faltas cometidas']=df.groupby('Primary Position')['Fouls'].rank(pct=True)
    df['Faltas recibidas']=df.groupby('Primary Position')['Fouls Won'].rank(pct=True)
    df['Intercepciones p90']=df.groupby('Primary Position')['Interceptions'].rank(pct=True)
    df['% pases con zurdo']=df.groupby('Primary Position')['L/R Footedness%'].rank(pct=True)
    df['Éxito pases largos']=df.groupby('Primary Position')['Long Ball%'].rank(pct=True)
    df['Pases largos']=df.groupby('Primary Position')['Long Balls'].rank(pct=True)
    df['Tiros']=df.groupby('Primary Position')['Shots'].rank(pct=True)
    df['xG']=df.groupby('Primary Position')['xG'].rank(pct=True)
    df['xG por tiro']=df.groupby('Primary Position')['xG/Shot'].rank(pct=True)
    df['Goles (sin penales)']=df.groupby('Primary Position')['NP Goals'].rank(pct=True)
    df['Contribución de gol']=df.groupby('Primary Position')['xG & xG Assisted'].rank(pct=True)
    df['xG post-tiro']=df.groupby('Primary Position')['PSxG'].rank(pct=True)
    df['OBV total']=df.groupby('Primary Position')['OBV'].rank(pct=True)
    df['OBV pases']=df.groupby('Primary Position')['Pass OBV'].rank(pct=True)
    df['OBV tiros']=df.groupby('Primary Position')['Shot OBV'].rank(pct=True)
    df['OBV acciones defensivas']=df.groupby('Primary Position')['DA OBV'].rank(pct=True)
    df['OBV conducciones y regates']=df.groupby('Primary Position')['D&C OBV'].rank(pct=True)
    df['OBV portero']=df.groupby('Primary Position')['Goalkeeper OBV'].rank(pct=True)
    df['Distancia de pases bajo presión']=df.groupby('Primary Position')['Pr. Pass Length Dif.'].rank(pct=True)
    df['Despejes']=df.groupby('Primary Position')['PAdj Clearances'].rank(pct=True)
    df['Intercepciones']=df.groupby('Primary Position')['PAdj Interceptions'].rank(pct=True)
    df['Presiones']=df.groupby('Primary Position')['PAdj Pressures'].rank(pct=True)
    #df['Altura de presiones']=df.groupby('Primary Position')['Average Pressure X'].rank(pct=True)
    df['Entradas']=df.groupby('Primary Position')['Tackles'].rank(pct=True)
    df['Entradas e Intercepciones p90']=df.groupby('Primary Position')['Tack&Int'].rank(pct=True)
    df['Pases']=df.groupby('Primary Position')['OP Passes'].rank(pct=True)
    df['Pases dentro del área']=df.groupby('Primary Position')['Passes Inside Box'].rank(pct=True)
    df['Pases al área']=df.groupby('Primary Position')['OP Passes Into Box'].rank(pct=True)
    df['% pases bajo presión']=df.groupby('Primary Position')['Passes Pressured%'].rank(pct=True)
    df['Éxito pases']=df.groupby('Primary Position')['Passing%'].rank(pct=True)
    df['xA']=df.groupby('Primary Position')['xG Assisted'].rank(pct=True)
    df['Pases largos sin presión']=df.groupby('Primary Position')['UPr. Long Balls'].rank(pct=True)
    df['Pérdidas']=df.groupby('Primary Position')['Turnovers'].rank(pct=True)
    df['Toques en el área']=df.groupby('Primary Position')['Touches In Box'].rank(pct=True)
    df['Pases filtrados']=df.groupby('Primary Position')['Throughballs'].rank(pct=True)
    df['% tiros a puerta']=df.groupby('Primary Position')['Shot Touch%'].rank(pct=True)
    df['Presiones p90']=df.groupby('Primary Position')['Pressures'].rank(pct=True)
    df['Éxito pases bajo presión']=df.groupby('Primary Position')['Pr. Pass%'].rank(pct=True)
    df['Pases largos bajo presión']=df.groupby('Primary Position')['Pr. Long Balls'].rank(pct=True)
    df['Dif. distancia de pases bajo presión']=df.groupby('Primary Position')['Pr. Pass% Dif.'].rank(pct=True)
    df['Recuperación tras presión']=df.groupby('Primary Position')['Pressure Regains'].rank(pct=True)
    df['Recuperación tras presión %']=df.groupby('Primary Position')['Press %'].rank(pct=True)
    df['Presiones cancha rival']=df.groupby('Primary Position')['Pressures F2'].rank(pct=True)
    df['PS xG vs xG']=df.groupby('Primary Position')['PSxG']/df.groupby('Primary Position')['xG']
    df['Calidad definición']=df.groupby('Primary Position')['PS xG vs xG'].rank(pct=True)
    df['Carry length total']=df.groupby('Primary Position')['Carries']*df.groupby('Primary Position')['Carry Length']
    df['Distancia conducciones']=df.groupby('Primary Position')['Carry length total'].rank(pct=True)
    df['Long balls total']=(df.groupby('Primary Position')['Long Balls']/df.groupby('Primary Position')['Long Ball%'])*100
    df['Long balls per pass']=df.groupby('Primary Position')['Long balls total']/df.groupby('Primary Position')['OP Passes']
    df['Pases largos por pases']=df.groupby('Primary Position')['Long balls per pass'].rank(pct=True)
    df['% pases con zurdo']=df.groupby('Primary Position')['L/R Footedness%']/100


    df = df.loc[df['Name'] == j1]
    df = df.set_index('Name').transpose()

    ax0.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')

    def plot_bar_central(ax, bar_data, title):
        #ax=ax.axis('off')
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


    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, ti1, size=txs1, c='black', fontweight='semibold') 

    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, t3, size=txs1, c='black', fontweight='semibold')


    plot_bar_central(ax1, bar1, ti1)
    plot_bar_central(ax2, bar2, ti2)
    plot_bar_central(ax3, bar3, ti3)
    plot_bar_central(ax4, bar4, ti4)
    plot_bar_central(ax5, bar5, ti5)



    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')


    return fig

def iqindlateral(df, j1, pos):
    c='white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh=36
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
    fig.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.05,
                        hspace=0.3)

    bar1=['Pases','% pases con zurdo','Éxito pases','Pases largos por pases','Progresiones al último tercio','Éxito pases largos','Éxito pases bajo presión']
    bar2=['Presiones','Recuperación tras presión %', 'Contrapresiones', 'Entradas','Éxito 1vs1 defensivo','Intercepciones','Despejes']
    bar3=['Duelos aéreos ganados', 'Éxito duelos aéreos']
    bar4=['Distancia conducciones','Regates','Éxito de regates','Faltas recibidas']
    bar5=['xA','Centros','Éxito centros','Pases al área','Toques en el área']


    t2='Pases'
    t3='Presiones'
    t4='xA'
    t5='Pases progresivos'

    ti1='Posesión'
    ti2='Defensivo'
    ti3='Juego aéreo'
    ti4='Conducción'
    ti5='Ofensivo'

    c1 = 'white'
    y1 = -3
    vmax = 4
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))
    #fig.add_artist(lines.Line2D([.6, .91], [.37, 0.37], color='#293A4A', lw=5))

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
    #df['Altura de presiones']=df['Average Pressure X'].rank(pct=True)
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

    ax0.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')

    def plot_bar_lateral(ax, bar_data, title):
        #ax=ax.axis('off')
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


    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, ti1, size=txs1, c='black', fontweight='semibold') 

    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, t3, size=txs1, c='black', fontweight='semibold')


    plot_bar_lateral(ax1, bar1, ti1)
    plot_bar_lateral(ax2, bar2, ti2)
    plot_bar_lateral(ax3, bar3, ti3)
    plot_bar_lateral(ax4, bar4, ti4)
    plot_bar_lateral(ax5, bar5, ti5)



    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')


    return fig

def iqindcontencion(df, j1, pos):
    c='white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh=36
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
    fig.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.05,
                        hspace=0.3)

    bar1=['Pases','% pases con zurdo','Éxito pases','Pases largos por pases','Progresiones al último tercio','Éxito pases largos','Éxito pases bajo presión']
    bar2=['Presiones', 'Recuperación tras presión %','Contrapresiones', 'Entradas','Éxito 1vs1 defensivo','Intercepciones','Balones recuperados']
    bar3=['Duelos aéreos ganados', 'Éxito duelos aéreos']
    bar4=['Distancia conducciones','Regates','Éxito de regates','Faltas recibidas']
    bar5=['xA','Centros','Pases al área','Tiros','Toques en el área']

    t2='Pases'
    t3='Presiones'
    t4='xA'
    t5='Pases progresivos'

    ti1='Posesión'
    ti2='Defensivo'
    ti3='Juego aéreo'
    ti4='Conducción'
    ti5='Ofensivo'

    c1 = 'white'
    y1 = -3
    vmax = 4
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))
    #fig.add_artist(lines.Line2D([.6, .91], [.37, 0.37], color='#293A4A', lw=5))

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
    #df['Altura de presiones']=df['Average Pressure X'].rank(pct=True)
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

    ax0.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')

    def plot_bar_contencion(ax, bar_data, title):
        #ax=ax.axis('off')
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


    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, ti1, size=txs1, c='black', fontweight='semibold') 

    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, t3, size=txs1, c='black', fontweight='semibold')


    plot_bar_contencion(ax1, bar1, ti1)
    plot_bar_contencion(ax2, bar2, ti2)
    plot_bar_contencion(ax3, bar3, ti3)
    plot_bar_contencion(ax4, bar4, ti4)
    plot_bar_contencion(ax5, bar5, ti5)



    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')


    return fig


def iqindvolante(df, j1, pos):
    c='white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh=36
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
    fig.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.05,
                        hspace=0.3)

    bar1=['xA','Pases al área','Centros','Éxito centros','Pases filtrados']    
    bar2=['xG','Calidad definición','Tiros','Toques en el área']
    bar3=['Distancia conducciones', 'Regates', 'Éxito regates', 'Faltas recibidas','Retención del balón']
    bar4=['Pases','% pases con zurdo','Éxito pases','Progresiones al último tercio']
    bar5=['Presiones', 'Recuperación tras presión %','Contrapresiones', 'Entradas e Intercepciones']

    t2='Pases'
    t3='Presiones'
    t4='xA'
    t5='Pases progresivos'

    ti1='Creación'
    ti2='Llegadas'
    ti3='Conducción'
    ti4='Posesión'
    ti5='Defensivo'

    c1 = 'white'
    y1 = -3
    vmax = 4
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))
    #fig.add_artist(lines.Line2D([.6, .91], [.37, 0.37], color='#293A4A', lw=5))

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
    #df['Altura de presiones']=df['Average Pressure X'].rank(pct=True)
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

    ax0.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')

    def plot_bar_volante(ax, bar_data, title):
        #ax=ax.axis('off')
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


    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, ti1, size=txs1, c='black', fontweight='semibold') 

    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, t3, size=txs1, c='black', fontweight='semibold')


    plot_bar_volante(ax1, bar1, ti1)
    plot_bar_volante(ax2, bar2, ti2)
    plot_bar_volante(ax3, bar3, ti3)
    plot_bar_volante(ax4, bar4, ti4)
    plot_bar_volante(ax5, bar5, ti5)



    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')


    return fig

def iqinddelantero(df, j1, pos):
    c='white'
    fig = plt.figure(frameon=False, edgecolor='#293A4A')
    fig.set_figheight(18)
    fig.set_figwidth(31)
    sh=36
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
    fig.subplots_adjust(left=0.1,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.05,
                        hspace=0.3)

    bar1=['xG','Calidad definición','Tiros','xG por tiro','Toques en el área','xA','Pases al área','Centros']
    bar2=['OBV conducciones y regates','Distancia conducciones','Regates','Éxito de regates','Faltas recibidas']
    bar3=['Pases','Éxito pases','Éxito pases bajo presión','OBV pases','Progresiones al último tercio','Pases hacia adelante %']
    bar4=['Duelos aéreos ganados','Éxito duelos aéreos']
    bar5=['Presiones','Recuperación tras presión %','Contrapresiones']

    t2='Pases'
    t3='Presiones'
    t4='xA'
    t5='Pases progresivos'

    ti1='Ofensivo'
    ti2='Conducción'
    ti3='Posesión'
    ti4='Juego aéreo'
    ti5='Defensivo'

    c1 = 'white'
    y1 = -3
    vmax = 4
    txs = 18
    txs1 = 22
    padr = -40

    fig.add_artist(lines.Line2D([.57, .57], [1, 0.1], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([-.04, .57], [.78, 0.78], color='#293A4A', lw=5))
    fig.add_artist(lines.Line2D([.57, .91], [.5, 0.5], color='#293A4A', lw=5))
    #fig.add_artist(lines.Line2D([.6, .91], [.37, 0.37], color='#293A4A', lw=5))

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
    #df['Altura de presiones']=df['Average Pressure X'].rank(pct=True)
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

    ax0.axis('off')
    ax6.axis('off')
    ax7.axis('off')
    ax8.axis('off')
    ax9.axis('off')

    def plot_bar_delantero(ax, bar_data, title):
        #ax=ax.axis('off')
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


    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, ti1, size=txs1, c='black', fontweight='semibold') 

    ax1.set_yticklabels('', color='black', size=20, fontname='Century Gothic', va='center')
    ax1.yaxis.set_tick_params(pad=15)
    ax1.set_xticks([])
    ax1.grid(color='grey', axis='x', which='major', zorder=3)
    ax1.text(0, y1, t3, size=txs1, c='black', fontweight='semibold')


    plot_bar_delantero(ax1, bar1, ti1)
    plot_bar_delantero(ax2, bar2, ti2)
    plot_bar_delantero(ax3, bar3, ti3)
    plot_bar_delantero(ax4, bar4, ti4)
    plot_bar_delantero(ax5, bar5, ti5)



    j1 = j1.upper()
    pos = pos.upper()
    plt.figtext(0.05, 0.98, j1, c='#151616', fontsize=56, fontweight='bold', fontname='arial')
    plt.figtext(0.05, 0.94, pos, c='#151616', fontsize=40, fontweight='bold', fontname='arial')


    return fig


st.title('Análisis de Jugadores')

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)


file_key = '13hOEzyecNB-3SdKE3qnIHKRPRWtkTqdz66VHEhqdtWA'


sheet = client.open_by_key(file_key).sheet1


# Convierte los datos de la hoja de cálculo en un DataFrame
df = pd.DataFrame(sheet.get_all_records())


temporadas = df['Season'].unique()
posiciones = df['Primary Position'].unique()
#equipos = df['Team'].unique()

# Selección de temporada y posición
temporada_seleccionada = st.selectbox("Selecciona la temporada", temporadas)
posicion_seleccionada = st.selectbox("Selecciona la posición", posiciones)
#equipo_seleccionado = st.selectbox("Selecciona el equipo", equipos)

# Filtrado de datos según la temporada y posición seleccionadas (& (df['Team'] == equipo_seleccionado))
df_filtrado = df[(df['Season'] == temporada_seleccionada) & (df['Primary Position'] == posicion_seleccionada)]
jugadores = df_filtrado['Name'].unique()
jugador_seleccionado = st.selectbox("Seleccione al jugador", jugadores)


posicion_funciones = {
    "Portero": iqindportero,
    "Right Centre Back": iqindcentral,
    "Left Centre Back": iqindcentral,
    "Centre Back": iqindcentral,
    "Left Back": iqindlateral,
    "Left Wing Back": iqindlateral,
    "Right Back": iqindlateral,
    "Right Wing Back": iqindlateral,
    "Left Defensive Midfielder": iqindcontencion,
    "Centre Defensive Midfielder": iqindcontencion,
    "Right Defensive Midfielder": iqindcontencion,
    "Left Centre Midfielder": iqindcontencion,
    "Centre Midfielder": iqindcontencion,
    "Right Centre Midfielder": iqindcontencion,
    "Left Midfielder": iqindvolante,
    "Left Wing": iqindvolante,
    "Right Midfielder": iqindvolante,
    "Right Wing": iqindvolante,
    "Left Attacking Midfielder": iqindvolante,
    "Centre Attacking Midfielder": iqindvolante,
    "Right Attacking Midfielder": iqindvolante,
    "Secondary Striker": iqindvolante,
    "Left Centre Forward": iqinddelantero,
    "Centre Forward": iqinddelantero,
    "Right Centre Forward": iqinddelantero
}

if st.button("Generar Análisis"):
    funcion_grafico = posicion_funciones.get(posicion_seleccionada)
    
    if funcion_grafico:
        fig = funcion_grafico(df_filtrado, jugador_seleccionado, posicion_seleccionada)
        st.pyplot(fig)
    else:
        st.error(f"No hay una función de gráficos definida para la posición: {posicion_seleccionada}")


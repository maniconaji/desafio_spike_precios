import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
import math
import pandas as pd

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def round_down(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

def k_bins(s):
    """
    Función para determinar número de bins en un histograma
    
    s (series.dataframe): Serie de la que se desea enconrar en número de bins para realizar un histograma.
    """
    if s.count() >= 100:
        return np.round(1+ 3.322*np.log10(s.count())).astype(int)
    else:
        return np.round(np.sqrt(s.count())).astype(int)

def plot_distribution(df, col_name, vlabel, name_file, close_file = True):

    s = df[col_name].dropna().sort_index()
    vmin  = round_down(s.min(), -1)
    if s.max() < 10:
        vmax  = round_up(s.max(), -1)
    else:
        vmax  = round_up(s.max()*1.1, -1)
    vstep = (vmax - vmin) * 10 ** -1
    fig = plt.figure(constrained_layout=True, figsize=(8,6), facecolor="lightgray")
    fig.suptitle(col_name.upper(), fontweight='bold')
    
    gs = GridSpec(
        2, 2, figure=fig, 
        left = 0.1, right = 0.85, top = 0.950, bottom = 0.1, 
        hspace = 0.0125, height_ratios=[2,1], 
        wspace = 0.005, width_ratios=[1,2] )
    ax_histogram  = fig.add_subplot(gs[0, 1])
    ax_boxplot    = fig.add_subplot(gs[0, 0])
    ax_timeseries = fig.add_subplot(gs[1, :])

    #boxplot
    sns.boxplot(
        data = s,  whis=[0, 100], orient="v", 
        color='lightblue', linewidth=1, saturation=1, 
        zorder=3, ax=ax_boxplot)
    sns.stripplot(
        data=s, size=2.5, orient="v",
        color=".3", linewidth=0, ax=ax_boxplot)
    ax_boxplot.set_ylim(vmin-vstep, vmax+vstep)
    ax_boxplot.set_xticklabels("")
    ax_boxplot.set_ylabel(vlabel)#, fontweight='bold')
    ax_boxplot.grid(axis="y", ls="--", lw=0.75, zorder=2)
    ax_boxplot.set_axisbelow(True)
    ax_boxplot.set_title("Boxplot")#, fontweight='bold')
    ax_boxplot.xaxis.set_ticks_position('none')
    #histogram
    if s.count() >= 100:
        kbins = np.round(1+ 3.322*np.log10(s.count())).astype(int)
    else:
        kbins = np.round(np.sqrt(s.count())).astype(int)
    sns.histplot(
        s, stat="probability", color='lightblue',
        bins=kbins, binrange=(vmin, vmax),
        zorder=3, ax=ax_histogram
        )
    ax_histogram.set_xlim(vmin-vstep, vmax+vstep)
    ax_histogram.set_ylim(0,1)
    ax_histogram.grid(ls="--", lw=0.75, zorder=1)
    ax_histogram.set_ylabel("Probabilidad (%)")#, fontweight='bold')
    ax_histogram.set_xlabel(vlabel)#, fontweight='bold')
    ax_histogram.set_axisbelow(True)
    ax_histogram.yaxis.set_major_locator(mticker.FixedLocator(ax_histogram.get_yticks()))
    ax_histogram.set_yticklabels(mticker.FormatStrFormatter('%.0f').format_ticks(ax_histogram.get_yticks()*100))
    ax_histogram.set_title("Histograma")#, fontweight='bold')
    # #time series
    ax_timeseries.plot(s, label="Datos", c='k', lw=1)
    ax_timeseries.set_xlim(s.index.min(), s.index.max())
    ax_timeseries.set_ylim(vmin, vmax)
    ax_timeseries.grid(axis="both", ls="--", lw=0.75, zorder=2)
    ax_timeseries.set_ylabel(vlabel)#, fontweight='bold')
    ax_timeseries.set_xlabel("Tiempo [años]")#, fontweight='bold')
    ax_timeseries.set_title("Serie de Tiempo")#, fontweight='bold')
    ax_timeseries.legend(loc=0, ncol=2)
    fig.savefig("Output/Plot/"+name_file)
    if close_file == True:
        plt.close(fig)
    return

def plot_allboxplot(df, vmin, vmax, vstep, vlabel, name_file):
    gridspec_kw = {"left": 0.3, "right": 0.975, "top": 0.975, "bottom": 0.1}
    fig, ax = plt.subplots(figsize=(10, 6), facecolor="lightgray", gridspec_kw=gridspec_kw)
    sns.boxplot(
        data = df,  whis=[0, 100], orient="h", 
        palette="tab10", linewidth=1, saturation=1, 
        zorder=3, ax=ax)
    ax.set_xlim(vmin-vstep, vmax+vstep)
    ax.set_xlabel(vlabel, fontweight='bold')
    ax.grid(axis="x", ls="--", lw=1, zorder=2)
    ax.set_axisbelow(True)
    fig.savefig("Output/Plot/"+name_file)
    return 

def plotSTPrecipitación(df, region_name, fecha_min, fecha_max):
    """
    Función para serie de tiempo de cada región en cierto intervalo de tiempo.
    
    df           (DataFrame): Corresponde al dataframe sin outliers, duplicados, o caracteres que puedan ocasionar un error.
    region_name        (str): strings que corresponde al nombre de una región. 
    fecha_min          (str): String con la fecha de inicio
    fecha_max          (str): String con la fecha de termino
    """
    def values(df, col_name, fecha_min, fecha_max):
        #eliminar NaN values y ordenar el índice
        df = df.dropna().sort_index()
        estacion = {
            12: "Verano", 1: "Verano", 2: "Verano", 
            3: "Otoño", 4: "Otoño", 5: "Otoño",
            6: "Invierno", 7: "Invierno", 8: "Invierno",
            9: "Primavera", 10: "Primavera", 11: "Primavera"}
        df['estacion'] = df.index.month.map(estacion)
        #establecer una condición para filtrar por fechas
        condicion = (df.index >= fecha_min) & (df.index <= fecha_max)
        s = df.loc[condicion, col_name]
        #valor mínimo, máximo
        vmin  = round_down(s.min(), -1)
        if s.max() < 10:
            vmax  = round_up(s.max(), -1)
        elif s.max() > 200:
            vmax  = round_up(s.max(), -2)
        else:
            vmax  = round_up(s.max()*1.1, -1)
        return vmin, vmax, df[condicion].reset_index()

    #combrobar que region_name se encuentra en el dataframe, o que esta está correctamente digitada
    if (any(df.index == fecha_min) == True) & (any(df.index == fecha_max) == True):
        boolean_list = [region_name in nregion for nregion in df.columns]
        if any(boolean_list) == True:
            #creación de figura
            left, right, top, bottom = [0.075, 0.975, 0.9, 0.125]
            gridspec_kw = {'left' : left, 'right' : right, 'top' : top, 'bottom' : bottom, "wspace":0.05, "width_ratios":[5, 1]}
            fig, (ax, ay) = plt.subplots(
                ncols=2, figsize=(12.5,5), gridspec_kw=gridspec_kw, facecolor='lightgrey', edgecolor='w')
            fig.suptitle("Series históricas de precipitaciones".upper(), fontweight="bold")
            col_name = df.columns[np.where(boolean_list)[0]][0]
            vmin, vmax, df = values(df, col_name, fecha_min, fecha_max)
            #serie de tiempo de precipítación}
            sns.lineplot(data=df, x="date", y=col_name, label="Datos", ax=ax)
            titulo_rangotemporal = "Rango: ".upper()+fecha_min.replace("-","/")+' a '+fecha_max.replace("-","/")
            titulo_region        = 'Región: '.upper()+col_name.replace("_"," ")
            ax.set_axisbelow(True)
            ax.set(xlim = (df['date'].min(), df['date'].max()), ylim = (vmin, vmax), title= titulo_rangotemporal+" - "+titulo_region)
            ax.set_xlabel("Tiempo [años]", fontweight='bold', fontsize=12, labelpad=5)
            ax.set_ylabel("Precipitación (mm)", fontweight='bold', fontsize=12, labelpad=5)
            ax.legend(fontsize=12, facecolor='lightgrey', edgecolor='k')
            ax.grid(ls="--", lw=1.5, zorder = 2)
            #table
            index = ["n° datos", "promedio", "std", "min", "P25", "P50", "P75", "max"]
            table_data = [ [index, "{:.2f}".format(value)] for index, value in zip(index, df[col_name].describe().values)]
            table = ay.table(cellText=table_data, loc='center left', cellLoc="center")
            table.scale(1,1.5)
            ay.axis('off')
            #guardar imagen 
            fig.savefig('Output/Plot/Precipitaciones_ST-'+col_name+'.png', facecolor='lightgrey', edgecolor='w')
        else:
            print("Error: No se encuentra la región: "+region_name+" dentro del archivo.")
    else:
        print("Error: El rango de fechas entre "+fecha_min+' a '+fecha_max+' no se encuentra en el archivo.')
    return

def plotSTbyYearPrecipitación(df, region_name, list_years):
    """
    Función para gráficar histogramas y series de tiempo de cada región.
    
    df           (DataFrame): Corresponde al dataframe sin outliers, duplicados, o caracteres que puedan ocasionar un error.
    region_name        (str): strings que corresponde al nombre de una región. 
    list_year         (list): Lista con años a considerar en el gráfico.
    """
    
    #eliminar NaN values y ordenar el índice
    df    = df.dropna().sort_index()
    Meses = {n+1: mes for n, mes in enumerate(["Ene",'Feb', "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"])}
    boolean_year_list = []
    for year in list_years:
        condicion = any(df.index.year.isin([year]))
        boolean_year_list.append(condicion)
        if condicion == False:
            print("Error: El año "+str(year)+' no se encuentra en el archivo.')
            break
    if all(boolean_year_list) == True:

        boolean_list = [region_name in nregion for nregion in df.columns]
        if any(boolean_list) == True:
            fig, ax = plt.subplots(ncols=1, figsize=(10,5), gridspec_kw={'left'  :0.05, 'right' :0.975, 'top'   :0.900, 'bottom':0.15},
                                facecolor='lightgrey', edgecolor='w')
            col_name = df.columns[np.where(boolean_list)[0]][0]
            df['Años']         = df.index.year
            df['Meses']        = df.index.month
            df["Nombre_meses"] = df.Meses.map(Meses)
            df          = df.loc[df['Años'].isin(list_years)]
            #serie de tiempo
            sns.lineplot(data=df, x="Meses", y=col_name, ci=None, hue="Años", ax=ax, lw=2, palette="tab10")
            
            #definición de limites
            if df[col_name].max() < 10:
                vmax  = round_up(df[col_name].max(), -1)
            elif df[col_name].max() > 200:
                vmax  = round_up(df[col_name].max(), -2)
            else:
                vmax  = round_up(df[col_name].max()*1.1, -1)
            ax.set_xlim(1, 12)
            ax.set_ylim(0,vmax)
            #definición de etiquetas del eje x e y
            ax.set_ylabel("Precipitación (mm)", fontweight='bold', fontsize=12, labelpad=10)
            ax.set_xlabel("Tiempo [meses]", fontweight='bold', fontsize=12, labelpad=10)
            #aumento de tamaño en xticks e yticks
            ax.set_xticks(df.Meses.unique().tolist())
            ax.set_xticklabels(df.Nombre_meses.unique().tolist())
            ax.tick_params(labelsize = 10, pad=5)
            #incorpora la legenda
            ax.legend(fontsize=10, facecolor='lightgrey', edgecolor='k')
            #difine forma de lineas que representan a la grilla
            ax.grid(ls="--", lw=1, zorder = 1)
            #definición de titulo
            ax.set_title("Series históricas de precipitaciones para la región: "+col_name, fontsize=14, fontweight='bold', pad = 10)
            #guardar imagen 
            fig.savefig('Output/Plot/Precipitaciones_byYear_'+col_name+'.png', facecolor='lightgrey', edgecolor='w')
        else:
            print("No se encuentra la región: "+region_name+" dentro del archivo.")
            
    return

def plotSTBancoCentral(df, col_name, fecha_min, fecha_max):
    """
    Función para graficar serie de tiempo de cada variable económica en cierto intervalo de tiempo.
    
    df           (DataFrame): Corresponde al dataframe sin outliers, duplicados, o caracteres que puedan ocasionar un error.
    col_name           (str): String con el nombre de la variable económica a gráficar.
    fecha_min          (str): String con la fecha de inicio
    fecha_max          (str): String con la fecha de termino
    """
    
    if (any(df.index == fecha_min) == True) & (any(df.index == fecha_max) == True):
        condicion = (df.index >= fecha_min) & (df.index <= fecha_max)
        s = df[condicion].sort_index()

        boolean_list = [col_name in ncol for ncol in df.columns]
        if any(boolean_list) == True:
            gridspec_kw={'left'  :0.05, 'right' :0.975, 'top'   :0.900, 'bottom':0.125, "wspace":0.05, "width_ratios":[5, 1]}
            fig, (ax, ay) = plt.subplots(
                ncols=2, figsize=(12.5,5), gridspec_kw=gridspec_kw,
                facecolor='lightgrey', edgecolor='w')
            nombre_columna = df.columns[np.where(boolean_list)[0]][0]
            #serie de tiempo            
            ax.plot(s[nombre_columna].dropna(), zorder=2, lw=2, label="Datos", ls="-")
            
            #definición de limite
            vmin  = round_down(s[nombre_columna].dropna().min(), -1)
            if s[nombre_columna].dropna().max() < 10:
                vmax  = round_up(s[nombre_columna].dropna().max(), -1)
            elif s[nombre_columna].dropna().max() > 200:
                vmax  = round_up(s[nombre_columna].dropna().max(), -2)
            else:
                vmax  = round_up(s[nombre_columna].dropna().max()*1.1, -1)
            ax.set_xlim(s[nombre_columna].dropna().index.min(), s[nombre_columna].dropna().index.max())
            ax.set_ylim(vmin, vmax)
            
            #definición de etiquetas del eje x e y
            ax.set_ylabel(col_name, fontweight='bold', fontsize=12, labelpad=10)
            ax.set_xlabel("Tiempo", fontweight='bold', fontsize=12, labelpad=10)
            
            #aumento de tamaño en xticks e yticks
            ax.tick_params(labelsize = 10, pad=5)
            
            #incorpora la legenda
            ax.legend(fontsize=14, facecolor='lightgrey', edgecolor='k')
            
            #difine forma de lineas que representan a la grilla
            ax.grid(ls="--", lw=1, zorder = 1)
            
            #definición de titulo
            ax.set_title('Series históricas para el rango: '+fecha_min+' a '+fecha_max+'.', 
                         fontsize=14, fontweight='bold', pad = 10)
            
            #table
            index = ["n° datos", "promedio", "std", "min", "P25", "P50", "P75", "max"]
            table_data = [ [index, "{:.2f}".format(value)] for index, value in zip(index, s[nombre_columna].dropna().describe().values)]
            table = ay.table(cellText=table_data, loc='center left', cellLoc="center")
            table.scale(1,1.5)
            ay.axis('off')

            #guardar imagen 
            fig.savefig('Output/Plot/BancoCentral_ST-'+nombre_columna+'.png', facecolor='lightgrey', edgecolor='w')
        else:
            print("Error: No se encuentra la región: "+col_name+" dentro del archivo.")
    else:
        print("Error: El rango de fechas entre "+fecha_min+' a '+fecha_max+' no se encuentra en el archivo.')
    return

def plot_variablesrelevantes(df_relevante, ncols, nrows):
    fig, axes = plt.subplots(
        figsize = (5*ncols, 5*nrows),
        ncols= ncols, nrows = nrows, 
        gridspec_kw={'wspace':0.25, 'hspace':0.25, 'left'  :0.075, 'right' :0.95,'top' :0.950, 'bottom':0.1},
        facecolor='lightgrey', edgecolor='w'
        )
    i=0
    for n, ax in enumerate(axes.flatten()):
        col_name = df_relevante.columns[1:][i]
        if n%2 == 0:
            s = df_relevante[col_name].dropna().sort_index()
            hist, bins = np.histogram(s, bins = k_bins(s))
            hist = hist / s.count()
            width = 1 * (bins[1] - bins[0])
            bins = (bins[:-1] + bins[1:]) / 2
            ax.bar(bins, hist, width, color='tab:blue', edgecolor='k', zorder=2)
            ax.set_ylim(0,0.3)
            ax.set_xlabel(col_name)
            ax.set_ylabel("Probabilidad (-)")
            ax.grid()
            ax.set_axisbelow(True)
        elif n%2 == 1:
            pd.plotting.autocorrelation_plot(s, ax=ax, label=col_name)
            ax.set_ylim(-1, 1)
            ax.set_xlim(0,)
            ax.set_title("Autocorrelación: {:.3f}".format(s.autocorr()))
            ax.set_axisbelow(True)
            i+=1
    return

########################################### Otras ################################################################

def plothistBancoCentral(df, col_name, variable, unidad, trimestral=True):
    """
    Función para gráficar histogramas y series de tiempo de cada región.
    
    df          (DataFrame): Corresponde al dataframe sin outliers, duplicados, o caracteres que puedan ocasionar un error.
    col_name    (str)      : String que corresponde al nombre de cada variable. 
    variable    (str)      : String con nombre global que debe tener abajo el histograma.
    unidad      (str)      : String que corresponde a la unidad de cada variable.
    list_string (list)     : Lista con valores unicos correspondiente a cual es el largo de cada string en esa variable.
    max_hist    (float)    : Máximo a considerar para histograma, este va de 0 a 1.
    """
    if (col_name in df.columns) == True:        
        fig, (ax, ay) = plt.subplots(ncols=2, figsize=(20,5), 
                                     gridspec_kw={'wspace':0.175, 'hspace':0.25, 'left'  :0.075, 'right' :0.95,
                                                  'top'   :0.900, 'bottom':0.1, 'width_ratios': [1,4]},
                                     facecolor='lightgrey', edgecolor='w')
                                     
        s = df[col_name].dropna().sort_index()
        hist, bins = np.histogram(s, bins = k_bins(s))
        hist = 100 * hist / s.count()
        width = 1 * (bins[1] - bins[0])
        bins = (bins[:-1] + bins[1:]) / 2
        ax.bar(bins, hist, width, color='tab:blue', edgecolor='k', zorder=2)
        ax.set_xlim(s.min(), s.max())
        ax.set_ylim(0,100)
        ax.grid(ls="--", lw=0.75, zorder=1)
        ax.set_xlabel(variable+' '+unidad, fontweight='bold')
        ax.set_ylabel("Probabilidad (%)", fontweight='bold')
        #serie de tiempo
        ay.plot(s, zorder=2, label='Datos', ls="--", c='tab:blue', marker='.', ms=3, lw=0.5)
        if trimestral == True:
            ay.plot(s.resample("Q", convention="end").median(), label="Promedio Trimestral", ls='-', lw=1, c='tab:red')
        ay.set_xlim(s.index.min(), s.index.max())
        ay.set_ylabel(variable+' '+unidad, fontweight='bold')
        ay.set_xlabel("Tiempo", fontweight='bold')
        ay.legend(fontsize=10)
        ay.grid(ls="--", lw=0.75, zorder = 1)
        ay.set_title(col_name, fontsize=12, fontweight='bold', pad = 10)
        fig.savefig('Output/Plot/BancoCentral_Hist_'+col_name+'.png')
        plt.close(fig)
    else:
        print("La variable ..."+col_name+'... no se encuentra en el archivo banco_central.csv')

def plothistBancoCentralPIB(df, col_name, variable, unidad):
    """
    Función para gráficar histogramas y series de tiempo de cada región.
    
    df          (DataFrame): Corresponde al dataframe sin outliers, duplicados, o caracteres que puedan ocasionar un error.
    col_name    (str)      : String que corresponde al nombre de cada variable. 
    variable    (str)      : String con nombre global que debe tener abajo el histograma.
    unidad      (str)      : String que corresponde a la unidad de cada variable.
    max_hist    (float)    : Máximo a considerar para histograma, este va de 0 a 1.
    """
    if (col_name in df.columns) == True:        
        fig, (ax, ay, az) = plt.subplots(ncols=3, figsize=(20,5), 
                                         gridspec_kw={'wspace':0.175, 'hspace':0.25, 'left'  :0.075, 'right' :0.95,
                                                      'top'   :0.900, 'bottom':0.1, 'width_ratios': [1,2,2]},
                                        facecolor='lightgrey', edgecolor='w')
        s = df[col_name].dropna().sort_index()
        hist, bins = np.histogram(s, bins = k_bins(s))
        hist = 100 * hist / s.count()
        width = 1 * (bins[1] - bins[0])
        bins = (bins[:-1] + bins[1:]) / 2
        ax.bar(bins, hist, width, color='tab:blue', edgecolor='k', zorder=2)
        ax.set_xlim(s.min(), s.max())
        ax.set_ylim(0,100)
        ax.grid(ls="--", lw=0.75, zorder=1)
        ax.set_xlabel(variable+' '+unidad, fontweight='bold')
        ax.set_ylabel("Probabilidad (%)", fontweight='bold')
        ax.set_title(col_name, fontsize=12, fontweight='bold', pad = 10)
        #serie de tiempo
        ay.plot(s, zorder=2, label='Datos', ls="--", c='tab:blue', marker='.', ms=3, lw=0.5)
        ay.plot(s.resample("Q", convention="end").median(), label="Promedio Trimestral", ls='-', lw=1, c='tab:red')
        ay.set_xlim(s.index.min(), s.index.max())
        ay.set_ylabel(variable+' '+unidad, fontweight='bold')
        ay.set_xlabel("Tiempo", fontweight='bold')
        ay.legend(fontsize=10)
        ay.grid(ls="--", lw=0.75, zorder = 1)
        ay.set_title('Serie de Tiempo', fontsize=10, fontweight='bold', pad = 10)
        #serie de tiempo trimestral
        s_resample = s.resample("Q", convention="end").sum()
        az.plot(s_resample, label="Suma Trimestral", ls='-', lw=1, c='tab:blue')
        az.set_xlim(s_resample.index.min(), s_resample.index.max())
        az.set_ylabel(variable+' '+unidad, fontweight='bold')
        az.set_xlabel("Tiempo", fontweight='bold')
        az.legend(fontsize=10)
        az.grid(ls="--", lw=0.75, zorder = 1)
        az.set_title("Suma trimestral", fontsize=12, fontweight='bold', pad = 10)
        fig.savefig('Output/Plot/BancoCentral_Hist_'+col_name+'.png')
        plt.close(fig)
    else:
        print("La variable ..."+col_name+'... no se encuentra en el archivo banco_central.csv')
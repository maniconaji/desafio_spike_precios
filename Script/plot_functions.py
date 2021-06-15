import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker

def k_bins(s):
    """
    Función para determinar número de bins en un histograma
    
    s (series.dataframe): Serie de la que se desea enconrar en número de bins para realizar un histograma.
    """
    if s.count() >= 100:
        return np.round(1+ 3.322*np.log10(s.count())).astype(int)
    else:
        return np.round(np.sqrt(s.count())).astype(int)

def plot_distribution(df, col_name, vmin, vmax, vstep, vlabel, name_file):
    fig = plt.figure(constrained_layout=True, figsize=(10, 6), facecolor="lightgray")
    fig.suptitle(col_name.upper(), fontweight='bold', fontsize=15)
    
    gs = GridSpec(
        2, 2, figure=fig, 
        left = 0.1, right = 0.94, top = 0.950, bottom = 0.1, hspace = 0.025, wspace = 0.025, 
        height_ratios=[2,1], width_ratios=[2,1] )
    ax_histogram  = fig.add_subplot(gs[0, 0])
    ax_boxplot    = fig.add_subplot(gs[0, 1])
    ax_timeseries = fig.add_subplot(gs[1, :])

    s = df[col_name].dropna().sort_index()
    #boxplot
    sns.boxplot(
        data = s,  whis=[0, 100], orient="v", 
        color='tab:blue', linewidth=1, saturation=1, 
        zorder=3, ax=ax_boxplot)
    sns.stripplot(
        data=s, size=2, orient="v",
        color=".3", linewidth=0, ax=ax_boxplot)
    ax_boxplot.set_ylim(vmin-vstep, vmax+vstep)
    ax_boxplot.set_xticklabels("")
    ax_boxplot.set_ylabel(vlabel, fontweight='bold')
    ax_boxplot.grid(axis="y", ls="--", lw=0.75, zorder=2)
    ax_boxplot.set_axisbelow(True)
    ax_boxplot.set_title("Boxplot", fontweight='bold')
    ax_boxplot.xaxis.set_ticks_position('none')
    #histogram
    if s.count() >= 100:
        kbins = np.round(1+ 3.322*np.log10(s.count())).astype(int)
    else:
        kbins = np.round(np.sqrt(s.count())).astype(int)
    sns.histplot(
        s, stat="probability", color='tab:blue',
        bins=kbins, binrange=(vmin, vmax),
        zorder=3, ax=ax_histogram
        )
    ax_histogram.set_xlim(vmin-vstep, vmax+vstep)
    ax_histogram.set_ylim(0,1)
    ax_histogram.grid(ls="--", lw=0.75, zorder=1)
    ax_histogram.set_ylabel("Probabilidad (%)", fontweight='bold')
    ax_histogram.set_xlabel(vlabel, fontweight='bold')
    ax_histogram.set_axisbelow(True)
    ax_histogram.yaxis.set_major_locator(mticker.FixedLocator(ax_histogram.get_yticks()))
    ax_histogram.set_yticklabels(mticker.FormatStrFormatter('%.1f').format_ticks(ax_histogram.get_yticks()*100))
    ax_histogram.set_title("Histograma", fontweight='bold')
    # #time series
    ax_timeseries.plot(s)
    ax_timeseries.set_xlim(s.index.min(), s.index.max())
    ax_timeseries.set_ylim(vmin, vmax)
    ax_timeseries.grid(axis="both", ls="--", lw=0.75, zorder=2)
    ax_timeseries.set_ylabel(vlabel, fontweight='bold')
    ax_timeseries.set_xlabel("Tiempo [años]", fontweight='bold')
    ax_timeseries.set_title("Serie de Tiempo", fontweight='bold')
    fig.savefig("Output/Plot/"+name_file)
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
#definición de función para 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from plot_functions import plot_distribution

def stringtofloat_BancoCentral(df, col_name, Ncorrecion, replace_dot, nmsk, nmskcorrecion, Nyear = False, nYcorrection = 10):
    """
    df (dataframe)      : dataframe correspondiente a los datos del banco central.
    col_name (str)      : nombre de variable.
    Ncorrecion (list)   : lista con valores para corregir cada string que paso a ser float32. Esta debe contener 10 elementos.
    replace_dot(list)   : lista de bool con:
                          -True: se debe reemplazar punto con "". 
                          -False: no es necesario reemplazar los puntos contenidos en cada string.
    nmsk (float or int) : valor que establecerá un límite para conocer que valores no logran ser corregidos.
    nmskcorrecion 
        (int or float)  : valor para corregir los valores.
    Nyear (list)        : lista de strings con fechas que no puedan corregirse previamente.
    nYcorrection        : valor para corregir el o los valores.
    """
    list_string = np.sort(df[col_name].dropna().str.len().unique())
    for n, i in enumerate([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
        if any(list_string == i) == True:
            if (replace_dot[n] == True):
                #confección de boolean para corregir valores
                msk = df[col_name].str.len() == i
                #reemplazo de punto para juntar string
                df.loc[msk, col_name] = df.loc[msk, col_name].replace('\.','', regex=True)
                #convertir a float y corrección de valores
                df.loc[msk, col_name] = pd.to_numeric(df.loc[msk, col_name], errors = "coerce", downcast='float')/(10**Ncorrecion[n])
            else:
                #convertir a float y corrección de valores
                msk = df[col_name].str.len() == i
                df.loc[msk, col_name] = pd.to_numeric(df.loc[msk, col_name], errors = "coerce", downcast='float')/(10**Ncorrecion[n])
    # convertir de float64 a float32 por uso de memoria
    df[col_name] = df[col_name].astype(np.float32)
    if (isinstance(nmsk, float) or isinstance(nmsk, int)) == True:
        #confección de boolean para corregir valores
        mskN = df[col_name] < nmsk
        df.loc[mskN, col_name] = df.loc[mskN, col_name]*nmskcorrecion
    if isinstance(Nyear, list) == True:
        mskN = df[col_name].index.isin(Nyear)
        df.loc[mskN, col_name] = df.loc[mskN, col_name]*nYcorrection
    # convertir de float64 a float32 por uso de memoria
    df[col_name] = df[col_name].astype(np.float32)
    return df


####################################### Arreglo Series ###########################################

def SeriesBC_IMACEC(bc2):
    replace_dot = [True for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    columnas_objetivo = [name_col for name_col in bc2.columns if "Imacec" in name_col] 
    for n, col_name in enumerate(columnas_objetivo):
        if bc2[col_name].dtypes == object:
            Ncorrecion = [0, 0, 0, 0, 0, 4, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 20, 10)
            plot_distribution(bc2, col_name, "IMACEC (%)", "BancoCentral_distribuciones_"+col_name)       
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=bc2[columnas_objetivo], orient="h", ax=ax, whis=[0,100])
    fig.savefig("Output/Plot/BancoCentral_boxplot_MACEC")
    return bc2

def SeriesBC_PIB(bc2):
    replace_dot = [True for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    #PIB, IVA y derechos de importación
    columnas_objetivo = [name_col for name_col in bc2.columns if "PIB" in name_col]
    # 'PIB_Agropecuario_silvicola'
    n = 0
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # 'PIB_Pesca'
    n = 1
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 20, 10)
    # 'PIB_Mineria'
    n = 2
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 3, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # 'PIB_Mineria_del_cobre'
    n = 3
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 250, 10)
    # 'PIB_Otras_actividades_mineras'
    n = 4
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 20, 10)
    # 'PIB_Industria_Manufacturera'
    n = 5
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 2, 0, 0, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Alimentos'
    n = 6
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 20, 10)
    #  'PIB_Bebidas_y_tabaco'
    n = 7
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Textil'
    n = 8
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Maderas_y_muebles'
    n = 9
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Celulosa'
    n = 10
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 3, 0, 4, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 50, 10)
    #  'PIB_Refinacion_de_petroleo'
    n = 11
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 15, 10)
    #  'PIB_Quimica'
    n = 12
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Minerales_no_metalicos_y_metalica_basica'
    n = 13
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Productos_metalicos'
    n = 14
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Electricidad'
    n = 15
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Construccion'
    n = 16
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 200, 10)
    #  'PIB_Comercio'
    n = 17
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 3, 0, 5, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 500, 10)
    #  'PIB_Restaurantes_y_hoteles'
    n = 18
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 4, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 500, 10)
    #  'PIB_Transporte'
    n = 19
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 3, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Comunicaciones'
    n = 20
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Servicios_financieros'
    n = 21
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Servicios_empresariales'
    n = 22
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Servicios_de_vivienda'
    n = 23
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    #  'PIB_Servicios_personales'
    n = 24
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 500, 10)
    #  'PIB_Administracion_publica'
    n = 25
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 500, 10)
    #  'PIB_a_costo_de_factores'
    n = 26
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 2, 3, 0, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 5000, 10)
    #  'PIB'
    n = 27
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 5000, 10)
    #  'Impuesto_al_valor_agregado'
    n = 28
    col_name = bc2.columns[36]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 500, 10)
        plot_distribution(bc2, col_name, "IVA (MM$)", "BancoCentral_distribuciones_"+col_name)
    #  'Derechos_de_Importacion'
    n = 29
    col_name = bc2.columns[37]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
        plot_distribution(bc2, col_name, col_name, "BancoCentral_distribuciones_"+col_name)

    for col_name in columnas_objetivo:
        plot_distribution(bc2, col_name, "PIB (MM$)", "BancoCentral_distribuciones_"+col_name)

    columnas_objetivo.append(bc2.columns[36])
    columnas_objetivo.append(bc2.columns[37])
    fig, (ax, ay) = plt.subplots(ncols=2, figsize=(16, 8))
    sns.boxplot(data=bc2[[i for i in columnas_objetivo if (i not in ["PIB_a_costo_de_factores", "PIB"])]], orient="h", ax=ax, whis=[0,100])
    sns.boxplot(data=bc2[["PIB_a_costo_de_factores", "PIB"]], orient="v", ax=ay, whis=[0,100])
    fig.savefig("Output/Plot/BancoCentral_boxplot_PIB")
    return bc2

def SeriesBC_Precio(bc2):
    # Precios y Tasa de cambio
    columnas_objetivo = [name_col for name_col in bc2.columns if "Precio" in name_col]

    # Precio_de_la_gasolina_en_EEUU_dolaresm3
    n = 0
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [1, 1, 2, 2, 2, 3, 3, 4, 5, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 28, 10, ["1979-06-01"], 10)
    # Precio_de_la_onza_troy_de_oro_dolaresoz
    n = 1
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_de_la_onza_troy_de_plata_dolaresoz
    n = 2
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 4, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [7]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_del_cobre_refinado_BML_dolareslibra
    n = 3
    col_name = columnas_objetivo[n]
    #display(bc2[col_name])
    fechasconproblemas = ['1984-12-01', '1986-10-01', '1986-12-01', '1987-12-01', '1988-09-01', '1988-11-01','1989-02-01', '1989-10-01', 
                        '1989-12-01', '1992-09-01', '1995-07-01', '1996-07-01', '1997-01-01', '1997-03-01',
                        '1997-12-01', '1999-12-01', '2006-01-01', '2006-04-01', '2011-02-01', '2016-11-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 3, 2, 3, 3, 6, 0, 8, 8, 8] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 0.4, 10, fechasconproblemas, 10)
    # Precio_del_diesel_centavos_de_dolargalon
    n = 4
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_del_gas_natural_dolaresmillon_de_unidades_termicas_britanicas
    n = 5
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 4, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [7]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_del_petroleo_Brent_dolaresbarril
    n = 6
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_del_kerosene_dolaresm3
    n = 7
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 1, 0, 2, 3, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 10**5, 10**-2)
    # Precio_del_petroleo_WTI_dolaresbarril
    n = 8
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # Precio_del_propano_centavos_de_dolargalon_DTN
    n = 9
    col_name = columnas_objetivo[n]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
    # "Tipo_de_cambio_del_dolar_observado_diario"
    col_name = "Tipo_de_cambio_del_dolar_observado_diario"
    fechasproblemas = ['1982-08-01', '1982-09-01', '1982-10-01', '1982-11-01', '1982-12-01', '1983-01-01', '1983-02-01', '1983-03-01',
                    '1983-04-01', '1983-05-01', '1983-06-01', '1983-07-01', '1983-08-01', '1983-09-01', '1983-10-01', '1983-11-01',
                    '1983-12-01', '1984-01-01', '1984-02-01', '1984-03-01', '1984-04-01', '1984-05-01', '1984-06-01', '1984-07-01', '1984-08-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 100, 10, fechasproblemas, 10**-1)
        plot_distribution(bc2, col_name, "Precio ($/dolares)", "BancoCentral_distribuciones_"+col_name)
    #Resumen descriptivo

    vlabel = {
        0: "Precio (dolares/m3)",
        1: "Precio (dolares/oz)",
        2: "Precio (dolares/oz)",
        3: "Precio (dolares/libra)",
        4: "Precio (dolares/galon)",
        5: "Precio (dolares/Munidades termicas)",
        6: "Precio (dolares/barril)",
        7: "Precio (dolares/m3)",
        8: "Precio (dolares/barril)",
        9: "Precio (dolares/galon)"
        }
    for n, col_name in enumerate(columnas_objetivo):
        plot_distribution(bc2, col_name, vlabel[n], "BancoCentral_distribuciones_"+col_name)

    columnas_objetivo.append("Tipo_de_cambio_del_dolar_observado_diario")
    fig, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=bc2[columnas_objetivo],  orient="h", ax=ax, whis=[0,100])
    fig.savefig("Output/Plot/BancoCentral_boxplot_Precios")
    return bc2

def SeriesBC_Ocupacion(bc2):
    columnas_objetivo = [name_col for name_col in bc2.columns if "Ocupa" in name_col]
    columnas_objetivo.append(bc2.columns[72])
    lista_A = [columnas_objetivo[i] for i in [1, 2, 3, 12, 11, 10, 9, 8, 6, 5, 15, 16, 17, 19, 20]]
    lista_B = [columnas_objetivo[i] for i in [0, 13]]
    lista_C = [columnas_objetivo[i] for i in [4, 14, 7]]
    lista_D = columnas_objetivo[18]
    lista_E = columnas_objetivo[21]
    lista_F = columnas_objetivo[22]

    for col_name in lista_A:
        if bc2[col_name].dtypes == object:
            Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
            bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")

    for col_name in lista_B:
        if bc2[col_name].dtypes == object:
            Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 3, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
            bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")

    for col_name in lista_C:
        if bc2[col_name].dtypes == object:
            Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
            bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")


    col_name = lista_D
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, 40, 10)

    col_name = lista_E
    fechasproblemas = ["2013-05-01", "2013-06-01", "2016-08-01", "2016-10-01", "2016-11-01", "2018-09-01", "2018-10-01", "2018-11-01", "2016-09-01",
                    "2014-04-01", "2014-05-01"]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 4, 0, 0, 0, 7, 8] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [6, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)

    col_name = lista_F
    fechasproblemas = ["2020-06-01", "2020-05-01"]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)

    #Resumen descriptivo

    for col_name in columnas_objetivo:
        plot_distribution(bc2, col_name, "Ocupados (miles de personas)", "BancoCentral_distribuciones_"+col_name)

    fig, (ax, ay) = plt.subplots(ncols=2, figsize=(16, 8))
    sns.boxplot(data=bc2[columnas_objetivo[1:]], orient="h", ax=ax, whis=[0,100])
    sns.boxplot(data=bc2[columnas_objetivo[0]], orient="v", ax=ay, whis=[0,100])
    ay.set_xticklabels("")
    ay.set_xlabel(columnas_objetivo[0])
    fig.savefig("Output/Plot/BancoCentral_boxplot_Ocupación")
    return bc2

def SeriesBC_TCMTCR(bc2):
    columnas_objetivo = [name_col for name_col in bc2.columns if ("ipo_de_cambio" in name_col) and ("dolar" not in name_col)]
    # Tipo_de_cambio_nominal_multilateral___TCM
    n = 0
    col_name = columnas_objetivo[n]
    fechasproblemas = ['1997-04-01', '1997-07-01', '1997-09-01', '2005-12-01','2006-04-01', '2008-02-01', '2008-04-01', '2010-11-01',
                    '2011-01-01', '2011-03-01', '2011-05-01', '2011-07-01','2011-08-01', '2011-09-01', '2012-02-01', '2012-03-01',
                    '2012-05-01', '2012-06-01', '2012-08-01', '2012-09-01','2012-10-01', '2012-12-01', '2013-01-01', '2013-04-01',
                    '2013-05-01', '2013-07-01', '2013-08-01', '2013-09-01','2013-10-01', '2010-12-01', '2011-06-01','1997-03-01', 
                    '2012-04-01', '2013-02-01', '2013-06-01', '1997-08-01','2008-03-01', '2010-09-01', '2010-10-01','2011-02-01',
                    '2011-04-01', '2012-07-01', '2012-11-01','2013-03-01', '1997-10-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 1, 2, 3, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [5, 6, 7, 9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)
        plot_distribution(bc2, col_name, "TCM (-)", "BancoCentral_distribuciones_"+col_name)

    # Indice_de_tipo_de_cambio_real___TCR_promedio_1986_100
    n = 1
    col_name = columnas_objetivo[n]
    fechasproblemas = [
        '1986-02-01', '1986-03-01', '1986-08-01', '1986-09-01', '1986-10-01', '1986-11-01', '1986-12-01', '1987-01-01', '1987-02-01',
        '1987-03-01', '1987-04-01', '1987-05-01', '1987-06-01', '1987-07-01', '1987-08-01', '1987-09-01', '1987-10-01', '1987-11-01',
        '1988-01-01', '1988-02-01', '1988-03-01', '1988-04-01', '1988-06-01', '1988-07-01', '1988-09-01', '1988-10-01', '1988-11-01',
        '1988-12-01', '1989-01-01', '1989-02-01', '1989-03-01', '1989-04-01', '1989-05-01', '1989-06-01', '1989-07-01', '1989-08-01',
        '1989-09-01', '1989-10-01', '1989-11-01', '1989-12-01', '1990-01-01', '1990-02-01', '1990-03-01', '1990-04-01', '1990-05-01',
        '1990-07-01', '1990-08-01', '1990-09-01', '1990-10-01', '1990-11-01', '1990-12-01', '1991-01-01', '1991-02-01', '1991-03-01',
        '1991-04-01', '1991-05-01', '1991-06-01', '1991-07-01', '1991-08-01', '1991-10-01', '1991-11-01', '1991-12-01', '1992-01-01',
        '1992-08-01', '1992-09-01', '1993-04-01', '1993-05-01', '2001-08-01', '2001-09-01', '2001-10-01', '2001-11-01', '2002-09-01',
        '2002-10-01', '2002-12-01', '2003-01-01', '2003-02-01', '2003-03-01', '2003-04-01', '2003-05-01', '2003-06-01', '2003-07-01',
        '2003-08-01', '2003-09-01', '2003-10-01', '2004-05-01', '2004-06-01', '2004-07-01', '2004-08-01', '2004-09-01', '2004-10-01',
        '2004-11-01', '2008-10-01', '2008-12-01', '2009-01-01', '2014-08-01', '2014-09-01', '2019-11-01', '2019-12-01', '2020-01-01',
        '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01', '2020-09-01', '2020-10-01', '1987-12-01', 
        '1988-08-01', '1991-09-01', '2005-03-01', '2008-11-01', '2015-08-01', '2020-08-01', '1988-05-01', '1990-06-01'
        ]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10)
        plot_distribution(bc2, col_name, "TCR (-)", "BancoCentral_distribuciones_"+col_name)
    #Resumen descriptivo

    fig, ax = plt.subplots(figsize=(8, 8))
    sns.boxplot(data=bc2[columnas_objetivo], orient="h", ax=ax, whis=[0,100])
    fig.savefig("Output/Plot/BancoCentral_boxplot_TCMTCR")
    return bc2

def SeriesBC_Produccion(bc2):
    columnas_objetivo = [name_col for name_col in bc2.columns if ("Indice_de_produccion" in name_col)]
    # Indice_de_produccion_industrial
    n = 0
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2011-12-01', '2012-03-01', '2012-10-01', '2012-11-01', '2012-12-01', '2013-03-01', '2013-07-01', '2013-08-01',
                    '2013-10-01', '2013-11-01', '2013-12-01', '2014-03-01', '2014-04-01', '2014-05-01', '2014-10-01', '2014-11-01', 
                    '2014-12-01', '2015-01-01', '2015-03-01', '2015-05-01', '2015-06-01', '2015-10-01', '2015-11-01', '2015-12-01', 
                    '2016-03-01', '2016-05-01', '2016-11-01', '2016-12-01', '2017-05-01', '2017-08-01', '2017-10-01', '2017-11-01', 
                    '2017-12-01', '2018-03-01', '2018-05-01', '2018-06-01', '2018-08-01', '2018-10-01', '2018-11-01', '2018-12-01',
                    '2019-03-01', '2019-05-01', '2019-07-01', '2019-08-01', '2019-10-01', '2019-11-01', '2019-12-01', '2020-01-01', 
                    '2020-03-01', '2020-10-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10)
    # Indice_de_produccion_industrial__mineria
    n = 1
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2004-12-01', '2005-12-01', '2006-12-01', '2007-03-01', '2007-12-01', '2011-12-01', '2012-12-01', '2013-08-01',
                    '2013-10-01', '2013-11-01', '2013-12-01', '2014-05-01', '2014-06-01', '2014-10-01', '2014-11-01', '2014-12-01',
                    '2015-01-01', '2015-05-01', '2015-06-01', '2015-09-01', '2015-10-01', '2015-12-01', '2016-03-01', '2016-05-01',
                    '2016-11-01', '2016-12-01', '2017-08-01', '2017-09-01', '2017-10-01', '2017-11-01', '2017-12-01', '2018-03-01',
                    '2018-07-01', '2018-09-01', '2018-10-01', '2018-11-01', '2018-12-01', '2019-08-01', '2019-10-01', '2019-11-01',
                    '2019-12-01', '2020-05-01', '2020-08-01', '2020-10-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 4, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [7, 9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10)
    # Indice_de_produccion_industrial_electricidad__gas_y_agua
    n = 2
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2014-02-01', '2014-04-01', '2014-06-01', '2014-08-01',
                    '2014-09-01', '2014-10-01', '2014-11-01', '2015-02-01',
                    '2015-09-01', '2015-11-01', '2016-09-01', '2020-09-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)
    # Indice_de_produccion_industrial__manufacturera
    n = 3
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2007-03-01', '2008-03-01', '2008-04-01', '2011-03-01', '2011-11-01', '2011-12-01', '2012-03-01', '2012-04-01',
                    '2012-05-01', '2012-08-01', '2012-10-01', '2012-11-01', '2012-12-01', '2013-01-01', '2013-03-01', '2013-04-01',
                    '2013-07-01', '2013-08-01', '2013-10-01', '2013-11-01', '2013-12-01', '2014-01-01', '2014-03-01', '2014-04-01',
                    '2014-05-01', '2014-10-01', '2014-12-01', '2015-03-01', '2015-04-01', '2015-05-01', '2015-07-01', '2015-10-01',
                    '2015-11-01', '2015-12-01', '2016-03-01', '2016-04-01', '2016-05-01', '2016-08-01', '2016-11-01', '2016-12-01',
                    '2017-03-01', '2017-05-01', '2017-08-01', '2017-11-01', '2017-12-01', '2018-03-01', '2018-04-01', '2018-05-01',
                    '2018-06-01', '2018-08-01', '2018-10-01', '2018-11-01', '2018-12-01', '2019-01-01', '2019-03-01', '2019-04-01',
                    '2019-05-01', '2019-07-01', '2019-08-01', '2019-10-01', '2019-11-01', '2019-12-01', '2020-01-01', '2020-02-01',
                    '2020-03-01', '2020-10-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 4, 0, 5, 6, 7] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [7, 9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10)
    # "Generación eléctrica"
    col_name = bc2.columns[79]
    fechasproblemas = ['2015-12-01', '2016-12-01', '2019-01-01', '2019-02-01', 
                    '2019-03-01', '2019-04-01', '2019-05-01', '2019-06-01',
                    '2019-07-01', '2019-10-01', '2019-12-01', '2020-01-01',
                    '2020-02-01', '2020-03-01', '2020-04-01', '2020-05-01',
                    '2020-06-01', '2020-07-01', '2020-09-01', '2020-10-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 2, 0, 0, 3, 4, 5] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [4, 6, 9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10)
        plot_distribution(bc2, col_name, "Generación eléctrica (GWh)", "BancoCentral_distribuciones_"+col_name)
    #Resumen descriptivo

    for col_name in columnas_objetivo:
        plot_distribution(bc2, col_name, "Índice de producción (%)", "BancoCentral_distribuciones_"+col_name)

    fig, (ax, ay) = plt.subplots(ncols=2, figsize=(16, 8))
    sns.boxplot(data=bc2[columnas_objetivo], orient="h", ax=ax, whis=[0,100])
    sns.boxplot(data=bc2[bc2.columns[79]], orient="v", ax=ay, whis=[0,100])
    ay.set_xticklabels("")
    ay.set_xlabel(col_name)
    fig.savefig("Output/Plot/BancoCentral_boxplot_Produccion")
    return bc2

def SeriesBc_Ventas(bc2):
    columnas_objetivo = [name_col for name_col in bc2.columns if ("Indice_de_ventas_comercio_real" in name_col)]
    # Indice_de_ventas_comercio_real_IVCM [ 9 10 11]
    n = 0
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2014-01-01', '2014-02-01', '2014-04-01', '2014-05-01', '2014-06-01', '2014-07-01', '2014-08-01', '2014-09-01',
                    '2014-10-01', '2014-11-01', '2015-01-01', '2015-02-01', '2015-04-01', '2015-06-01', '2015-07-01', '2015-09-01',
                    '2016-02-01', '2016-06-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 4, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [9, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)
    # Indice_de_ventas_comercio_real_no_durables_IVCM [ 7 10 11]
    n = 1
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2014-01-01', '2014-02-01', '2014-04-01', '2014-05-01', '2014-06-01', '2014-07-01', '2014-08-01', '2014-09-01',
                    '2014-11-01', '2015-01-01', '2015-02-01', '2015-04-01', '2015-06-01', '2015-07-01', '2015-09-01', '2016-06-01',
                    '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01', '2015-08-01', '2016-08-01', '2017-02-01', '2019-10-01', '2019-11-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 3, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [7, 10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)
        
    # Indice_de_ventas_comercio_real_durables_IVCM [10 11]
    n = 2
    col_name = columnas_objetivo[n]
    fechasproblemas = ['2014-01-01', '2014-02-01', '2014-04-01', '2014-05-01', '2014-06-01', '2014-07-01', '2014-09-01', '2014-10-01',
                    '2014-11-01', '2015-01-01', '2015-02-01', '2015-03-01', '2015-04-01', '2015-05-01', '2015-06-01', '2015-07-01',
                    '2015-10-01', '2016-01-01', '2016-02-01', '2020-04-01', '2020-05-01', '2020-06-01', '2020-07-01']
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 5, 6] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [True if (n_bool in [10, 11]) else False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "", fechasproblemas, 10**-1)
        
    # Ventas_autos_nuevos [4 5]
    n = 3
    col_name = bc2.columns[-1]
    if bc2[col_name].dtypes == object:
        Ncorrecion  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #[2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        replace_dot = [False for n_bool in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
        bc2 = stringtofloat_BancoCentral(bc2, col_name, Ncorrecion, replace_dot, "", "")
        plot_distribution(bc2, col_name, "Ventas de autos nuevos (unidades)", "BancoCentral_distribuciones_"+col_name)

    for col_name in columnas_objetivo:
        plot_distribution(bc2, col_name, "Índice_de_ventas (%)", "BancoCentral_distribuciones_"+col_name)

    fig, (ax, ay) = plt.subplots(ncols=2, figsize=(16, 8))
    sns.boxplot(data=bc2[columnas_objetivo], orient="h", ax=ax, whis=[0,100])
    sns.boxplot(data=bc2[bc2.columns[-1]], orient="v", ax=ay, whis=[0,100])
    ay.set_xticklabels("")
    ay.set_xlabel(col_name)
    fig.savefig("Output/Plot/BancoCentral_boxplot_Ventas")
    return bc2
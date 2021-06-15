#definición de función para 
import pandas as pd
import numpy as np

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
        if any(list_string == i) == True and (replace_dot[n] == True):
            #confección de boolean para corregir valores
            msk = df[col_name].str.len() == i
            #reemplazo de punto para juntar string
            df.loc[msk, col_name] = df.loc[msk, col_name].replace('\.','', regex=True)
            #convertir a float y corrección de valores
            df.loc[msk, col_name] = pd.to_numeric(df.loc[msk, col_name], errors = "coerce", downcast='float')/(10**Ncorrecion[n])
        elif any(list_string == i) == True and (replace_dot[n] == False):
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
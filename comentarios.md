## 2.3 Análisis y comentarios de ambos archivos: 

De acuerdo a lo observado anteriormente:
* Respecto a los registros duplicados y nulos en cada archivo:
    1. No hay registros de precipitación duplicados y ni datos anómalos, teniendo 496 observaciones para cada región en el archivo "precipitaciones.csv".
    2. En el archivo "banco_central.csv" existen dos fechas con archivos duplicados: "2018-08-01" y "2019-08-01". También existen registros con letra "a", lo que no es considerado como un valor nulo, por lo tanto se hace una limpieza de los datos duplicados y aquellos con valores como "a" son pasados a un valor NaN.
    3. Además, las diferentes variables económicas presentan registros en periodos, lo que genera datos nulos.
* Respecto al análisis descriptivo, histogramas y boxplot para el archivo "precipitaciones" se tiene:
    1. Desde la región más al norte (Coquimbo) hasta la región más al sur (Los Rios), se observa en los percentiles 25, 50 y 75, junto a la media un aumento en intensidad de la precipitación registrada. Misma tendencia no es compartida en los valores máximos.
    2. 
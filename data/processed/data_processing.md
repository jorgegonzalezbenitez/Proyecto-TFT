# Procesamiento y preparación de datos

En esta parte del proyecto he trabajado en la **limpieza, validación y transformación de los datos originales** del sistema de reservas del grupo hotelero.

El objetivo de esta fase es construir **datasets limpios y consistentes** que posteriormente se utilizarán en el análisis exploratorio y en los modelos de predicción de la tasa de ocupación.

Todo este proceso se realiza dentro del directorio `data/processed`, utilizando dos notebooks principales que forman el pipeline de preparación de datos.

---

# 1. Conversión del dataset original a parquet

El dataset original se encuentra en formato **CSV** dentro del directorio `data/raw`.

Dado que el archivo es relativamente grande, el primer paso consiste en convertirlo a formato **parquet**, que permite una lectura mucho más rápida y eficiente en los pasos posteriores del análisis.

Este proceso lo realizo en el notebook:
`raw_to_parquet.ipynb`

En este notebook aplico varias transformaciones iniciales para normalizar y limpiar los datos.

---

## Normalización de variables

Primero convierto las variables al formato adecuado:

- `date` y `fechaimport` → formato fecha (`datetime`)
- `codigo_hotel` y `codigo_ttoo` → texto en mayúsculas
- variables numéricas (`roomnights`, `bednights`, `stock`, `neto`) → formato numérico

Esto evita problemas posteriores derivados de formatos inconsistentes en los datos.

---

## Eliminación de agregados duplicados

En algunos casos el dataset contiene **líneas agregadas** que representan la suma de varios registros del mismo día.

Por ejemplo, pueden aparecer:

- varias filas por turoperador
- y otra fila adicional con la suma total

Para evitar duplicaciones en los cálculos, detecto estas filas comparando los valores de `roomnights` y `bednights` con la suma del grupo y elimino las líneas agregadas.

---

## Reglas de consistencia del stock

El dataset incluye una variable `stock` que representa el número de habitaciones disponibles.

Sin embargo, en los datos originales aparecen valores inconsistentes que no coinciden con la capacidad real del hotel.

Por ello defino el stock real de cada establecimiento:

- Hotel 1 → 94 habitaciones  
- Hotel 2 → 138 habitaciones  
- Hotel 3 → 251 habitaciones  

A partir de ahí aplico dos reglas:

- si el stock es **menor que el real**, se elimina el registro
- si el stock es **mayor que el real**, se ajusta al valor correcto

Esto asegura que la ocupación calculada posteriormente sea coherente.

---

## Procesamiento por bloques (chunks)

Como el dataset es grande, realizo la lectura del CSV **por bloques de filas** utilizando `chunksize`.

Esto permite procesar el archivo sin cargarlo completamente en memoria.

Cada bloque limpio se guarda como un parquet intermedio, y al final todos los bloques se combinan en un único dataset:
`livvo_clean_all_v2.parquet`

---

# 2. Limpieza final y agregaciones

El segundo notebook del pipeline es:
`final_cleaning_and_aggregates.ipynb`

Aquí realizo la limpieza final y genero los datasets que se utilizarán en el análisis y el modelado.

---

## Consistencia temporal

En esta fase analizo la relación entre la fecha de la estancia (`date`) y la fecha de importación del registro (`fechaimport`).

Detecté que una parte importante de los registros presentaba la situación:
`fechaimport < date`

Es decir, el sistema indicaba que el registro se había importado antes de la fecha real de la estancia, lo que supone una inconsistencia temporal en los datos.

Para evitar introducir errores en el análisis posterior, decidí **eliminar estos registros durante la fase de limpieza**, manteniendo únicamente observaciones con una relación temporal coherente entre ambas variables.

Aunque `fechaimport` se utiliza en esta fase para asegurar la calidad del dataset y seleccionar la versión más reciente de cada registro, **la variable principal utilizada en el análisis y en los modelos de predicción es `date`**, que representa la fecha real de la estancia.

---

## Eliminación de duplicados

Después verifico que no existan registros duplicados para la combinación:
`hotel + fecha + turoperador`

En caso de existir duplicados, se conserva únicamente una observación para evitar distorsiones en las agregaciones posteriores.

---

## Selección de la última fecha de importación

En el sistema de reservas, una misma fecha puede aparecer varias veces porque los datos se actualizan con el tiempo.

Para cada combinación de:
`hotel + turoperador + fecha`

conservo únicamente el registro con **la última fecha de importación**, que representa la información más actualizada disponible.

---

## Agregación diaria

Una vez limpiados los datos, realizo dos niveles de agregación.

### Agregación por turoperador

Primero agrupo por:
`date + hotel + ttoo`

y calculo:

- suma de `roomnights`
- suma de `bednights`
- suma de `neto`
- máximo de `stock`

Esto genera el dataset:
`livvo_day_ttoo_final.parquet`

---

### Agregación por hotel

Después agrego a nivel de hotel agrupando por:
`date + hotel`

y calculo nuevamente:

- `roomnights`
- `bednights`
- `neto`
- `stock`

---

## Cálculo de indicadores hoteleros

A partir de estas variables calculo dos indicadores clave:

**Ocupación**: `ocup_total = roomnights / stock`

**ADR (Average Daily Rate)**: `ADR = neto / roomnights`

Estos indicadores serán fundamentales para el análisis exploratorio.

---

# Resultado final

Al final de este proceso obtengo dos datasets limpios y listos para el análisis:

- `livvo_day_ttoo_final.parquet`
- `livvo_day_hotel_final.parquet`
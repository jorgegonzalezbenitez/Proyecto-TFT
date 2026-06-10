# Análisis Exploratorio de Canales de Distribución por Hotel

En esta fase del proyecto he analizado cómo contribuyen los distintos canales de distribución a la ocupación diaria de los hoteles.  
El objetivo es entender:

- Qué canales son más relevantes para cada hotel,  
- Cómo evoluciona su peso a lo largo del tiempo,  
- Si existen dependencias fuertes de un canal,  
- Cómo cambia la mezcla comercial en distintos periodos,  
- Y qué implicaciones tiene todo esto para los modelos de predicción de ocupación.

Este análisis lo he realizado sobre la base `livvo_day_ttoo_final.parquet`, que contiene la información diaria de *roomnights* por hotel y canal.


## 1. Tabla comparativa hotel × canal (roomnights totales)

La primera tabla que he generado resume los **roomnights totales** aportados por cada canal a cada hotel.

Algunas observaciones claras:

- **Hotel 1** tiene una fuerte concentración en los canales WEL y B, que juntos suman una parte muy significativa del total.  
- **Hotel 2** presenta un mix algo más equilibrado, pero con dos actores dominantes: T y J.  
- **Hotel 3** destaca por la aportación masiva del canal J, que supera con diferencia a cualquier otro canal.

Esta primera vista confirma que los tres hoteles tienen **mezclas comerciales completamente diferentes**.


## 2. Peso relativo de cada canal dentro del hotel

A partir de la matriz anterior calculé el **share** (porcentaje del total del hotel que representa cada canal). Esta tabla y su correspondiente heatmap permiten ver qué canales son realmente estratégicos.

### Principales conclusiones

### Hotel 1
- WEL es el canal dominante (37%).
- B (23%) es el segundo pilar.
- El resto de canales tiene un papel mucho más marginal.

### Hotel 2
- T domina con un 37%.
- Le sigue J con un 18%.
- WEL y B mantienen un papel intermedio.
- Mix bastante equilibrado, pero con dos dependencias claras.

### Hotel 3
- Dominancia del canal J (29%).
- WEL, TH y T forman un segundo bloque más equilibrado.
- Más diversificación que el Hotel 1 pero menos que el Hotel 2.

El heatmap refuerza visualmente estas diferencias entre hoteles y confirma dónde hay **dependencia comercial alta**, algo importante para los modelos y para la interpretación estratégica.


## 3. Top 5 canales por hotel

A través de un ranking de roomnights por hotel, identifiqué los cinco canales principales en cada uno.

### Hotel 1
1. WEL  
2. B  
3. H  
4. K  
5. T  

### Hotel 2
1. T  
2. J  
3. WEL  
4. B  
5. L  

### Hotel 3
1. J  
2. T  
3. WEL  
4. TH  
5. AV  

Esta lista ayuda a centrar los análisis temporales únicamente en los canales realmente relevantes para cada hotel.


## 4. Evolución temporal de los principales canales (global)

Analicé la evolución de los canales más importantes a nivel global (sumados para todos los hoteles).

### Insights relevantes

- **WEL, T y J** son los que muestran series más voluminosas y estables.  
- Se aprecian **patrones estacionales claros**, con máximos entre invierno y primavera, y descensos en algunos veranos.  
- A partir de 2026 todas las series caen abruptamente, reflejando el efecto estructural observado previamente en el Hotel 3 y en parte del Hotel 2.

Este análisis global sirve de referencia antes de entrar al detalle por hotel.


## 5. Evolución temporal por hotel (roomnights por canal)

### Hotel 1
- Muy alta volatilidad diaria, sin patrones estacionales marcados.  
- WEL y K parecen alternarse como principales fuentes.  
- Curvas irregulares: ocupación muy distribuida entre múltiples canales pequeños.

### Hotel 2
- TU es el canal estrella durante todo el horizonte temporal.  
- J aporta un bloque relevante pero menor.  
- WEL y B aparecen como complementarios.  
- Se aprecia una estacionalidad clara, similar a la serie de ocupación del hotel.

### Hotel 3
- J domina claramente todo el periodo.  
- Durante 2024–2025 el volumen de J es muy alto y constante.  
- A finales de 2026 todas las series caen, igual que ocurría con la ocupación total del hotel.

En los tres casos la evolución temporal de los canales refleja fielmente los patrones generales de ocupación detectados en el EDA previo de hoteles.


## 6. Peso temporal (share diario)

Después analicé **cómo varía el peso diario** de los canales dentro de cada hotel.

### Hotel 1
- El peso diario es extremadamente variable.  
- WEL llega algunos días al 80–90% del total.  
- No existe un mix estable: alta fragmentación y picos constantes.

### Hotel 2
- T muestra continuamente shares entre 30% y 50%.  
- J mantiene un peso más modesto pero estable.  
- El hotel presenta un mix más equilibrado a lo largo del tiempo comparado con los hoteles 1 y 3.

### Hotel 3
- La serie es mucho más estable, dominada por J.  
- A partir de 2026 el share de J llega incluso a valores cercanos al 100% en días específicos.  
- El resto de canales se mantiene siempre en valores pequeños.

Este análisis es clave: **los modelos no solo deben captar la estacionalidad de la ocupación, sino también la heterogeneidad en la dependencia del hotel respecto a cada canal**.


## 7. Mix temporal de canales (gráficos de área)

Estos gráficos permiten ver de forma clara **qué canales ocupan el "espacio" comercial del hotel** a lo largo del tiempo.

### Hotel 1
- Mezcla muy fragmentada, sin claro patrón estacional.  
- WEL y H se alternan como los canales más voluminosos.

### Hotel 2
- T ocupa una franja muy amplia casi todo el tiempo.  
- WEL y B aportan un volumen secundario pero constante.  
- Visualmente es el hotel con el mix más equilibrado y legible.

### Hotel 3
- J llena la mayor parte del área prácticamente todo el tiempo.  
- El mix es visualmente un bloque dominante con tres capas secundarias muy estables.  
- La caída post-2026 es muy evidente.

Estos gráficos muestran la "firma comercial" de cada hotel.


## Conclusiones generales del análisis de canales

### 1. Cada hotel tiene un perfil comercial completamente distinto  
- Hotel 1 → muy fragmentado, mix inestable.  
- Hotel 2 → mix equilibrado pero con dos actores dominantes.  
- Hotel 3 → dependencia muy alta del canal J.  

Esto significa que los modelos de predicción deberán **tratar cada hotel por separado**.

### 2. Existen dependencias críticas  
En algunos hoteles un único canal puede representar **más del 30–40%** del volumen total.

### 3. Hay estacionalidad clara en los canales más importantes  
Especialmente en **T**, **J** y **WEL**, que reflejan directamente los patrones estacionales de ocupación.

### 4. Se observan cambios estructurales  
Particularmente en el Hotel 3 y parcialmente en el Hotel 2 con la caída drástica a partir de 2026. Esto indica que habrá que:

- segmentar periodos,  
- usar modelos robustos a cambios de régimen,  
- o introducir variables que representen estos cambios.

### 5. El análisis de canales aporta valor directo al modelado  
Estos resultados permiten:

- entender qué canales son predictores fuertes,  
- adaptar el modelo a la estructura comercial de cada hotel.
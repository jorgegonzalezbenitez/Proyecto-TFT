# Análisis Exploratorio de Datos (EDA)

En esta fase he analizado los datos de los tres hoteles para los que quiero estimar y predecir la tasa de ocupación. Antes de entrar en modelos de predicción o series temporales, me parecía importante entender bien cómo se comporta cada establecimiento a lo largo del tiempo: su ocupación, demanda, ingresos y posibles anomalías.

---
---

# Análisis Exploratorio del Hotel 1 (EDA)

Aplico el mismo enfoque al Hotel 1, para contrastar su dinámica de ocupación con los hoteles 2 y 3.

## 1. Evolución de roomnights

La serie de roomnights en el Hotel 1 muestra:

- Mayor variabilidad diaria que en los otros dos hoteles.
- Menor estacionalidad identificable a simple vista.
- Descensos bruscos puntuales, probablemente por baja demanda o incidencias.

## 2. Ocupación del hotel

La ocupación diaria (`ocup_total`) en el Hotel 1:

- Es más irregular y con ocupación media más baja.
- Presenta subidas y bajadas abruptas entre semanas.
- Sugiere un mix de demanda más heterogéneo y sensible a eventos.

## 3. ADR (precio medio por habitación vendida)

El ADR en el Hotel 1:

- También es variable, pero menos extremo que en el Hotel 3.
- Muestra picos coincidentes con semanas de alta demanda.
- Mantiene una estacionalidad moderada.

## 4. Distribuciones (roomnights, ocup_total y ADR)

- Roomnights: concentrados en valores medios.
- `ocup_total`: distribución relativamente uniforme, con colas inferiores.
- ADR: comportamiento irregular con varios modos.

## 5. Estacionalidad mensual y semanal

### Mensual

Estacionalidad débil comparada con el Hotel 2; meses con mezcla de días altos y bajos.

### Semanal

Patrón plano: pocas diferencias sistemáticas entre días, lo que sugiere que la demanda no depende tanto del día de la semana.

## 6. Correlaciones entre variables

- `ocup_total` correlaciona bien con `roomnights` (consistente con la lógica de ocupación).
- ADR muestra correlación más débil con la demanda (precio y cantidad no siempre se alinean).

## 7. Detección de outliers (ocupación)

Outliers detectados con IQR sobre `ocup_total`:

- Varios outliers inferiores (días de ocupación muy baja).
- Aparecen en periodos concretos, compatibles con baja actividad o incidencias operativas.

Para el modelado:

- Considerar suavizados (ventana de 7/28 días) para reducir ruido en la señal objetivo.
- Probar modelos robustos a variabilidad y outliers (Random Forest, XGBoost).

## 8. Heatmap tipo calendario (ocupación diaria)

El calendario del Hotel 1:

- Muestra meses heterogéneos con alternancia de semanas fuertes y débiles.
- Refuerza la menor estacionalidad y la irregularidad intra-mensual.
- Facilita localizar rachas y valles que los promedios ocultan.

## Conclusión del EDA del Hotel 1

- Menor estacionalidad y mayor ruido que en los hoteles 2 y 3.
- Ocupación media más baja e irregular.
- Recomendable usar enfoques que toleren alta variabilidad y capturen no linealidades (Random Forest, XGBoost), además de features temporales y estadísticos de ventana móvil.

---
# Análisis Exploratorio del Hotel 2 (EDA)

He comenzado con el Hotel 2, que presenta el perfil vacacional más marcado de los tres. A continuación resumo lo que he hecho y lo que he observado.

## 1. Evolución de roomnights

Lo primero que he hecho ha sido representar los roomnights diarios del hotel.
La gráfica muestra bastante variabilidad, pero se aprecia un patrón claro:

- Hay picos de ocupación alta en invierno y principios de año.
- En cambio, hay una caída pronunciada en los meses alrededor del verano del primer año (2023).
- A partir de ahí, la demanda se recupera bastante bien y vuelve a estabilizarse.

Esta curva temporal ya me da pistas sobre la estacionalidad, algo que luego será clave en los modelos predictivos.

## 2. Ocupación del hotel

Luego he representado la ocupación diaria (`ocup_total`).
La forma general coincide bastante con la serie de roomnights, pero es interesante ver:

- Una ocupación alta durante buena parte del año.
- Bajadas puntuales que se repiten en ciertas épocas, lo que refuerza la idea de estacionalidad.
- Algunos "dientes de sierra", típicos de la variación día a día (sobre todo entre semanas y fines de semana).

Esta es la variable principal que quiero predecir en el TFG, así que es importante ir viéndole el comportamiento desde el principio.

## 3. ADR (precio medio por habitación vendida)

La representación del ADR diario ha sido especialmente útil porque muestra:

- Grandes fluctuaciones en determinados días, con picos muy altos.
- Periodos con ADR bajo (probablemente promociones o baja demanda).
- Picos que podrían corresponder a eventos, festivos o aumentos de precio en temporada alta.

Más adelante, el ADR puede ser una variable explicativa útil para los modelos de ML.

## 4. Distribuciones (roomnights, ocup_total y ADR)

He analizado las distribuciones para entender su forma:

- Roomnights tiende hacia valores altos, con pocos días de demanda muy baja.
- La ocupación tiene un sesgo hacia la parte alta (70–85%).
- El ADR tiene una distribución más irregular, con varios grupos de valores, lo que sugiere cambios de estrategia de precios según temporada.

Estas distribuciones ayudan a detectar comportamientos normales y días atípicos.

## 5. Estacionalidad mensual y semanal

### Estacionalidad mensual

- Meses como enero, febrero y marzo tienen ocupaciones más altas.
- Junio y julio muestran ocupaciones más bajas.
- Octubre, noviembre y diciembre parecen estables en torno a niveles altos.

### Estacionalidad semanal

- No hay grandes diferencias entre días de la semana, pero sí aparecen outliers hacia abajo los lunes, martes y miércoles.

Esto me servirá para crear variables temporales en los modelos de ML.

## 6. Correlaciones entre variables

La matriz de correlaciones confirma cosas esperadas:

- `roomnights` ↔ `ocup_total` → correlación altísima (lógico).
- `ADR` ↔ `neto` → correlación muy fuerte (precio × demanda).
- `roomnights` ↔ `ADR` → relación algo más débil (habitaciones vendidas y precio no siempre suben juntos).

Esto me ayuda a decidir qué variables añadir en los modelos futuros.

## 7. Detección de outliers (ocupación)

Finalmente, he detectado **outliers en la ocupación diaria (`ocup_total`)** usando el método **IQR** y los he resaltado en un gráfico de dispersión. Para cada día, calculo los cuartiles Q1 y Q3 de la ocupación, el rango intercuartílico (IQR = Q3 − Q1) y marco como outlier cualquier valor **< Q1 − 1.5×IQR** o **> Q3 + 1.5×IQR**. En la figura, los **puntos rojos** son días atípicos y los **azules** días normales. Las líneas grises indican los umbrales de referencia.

Esto me sirve para:

- identificar días anómalos en la ocupación,
- decidir si conviene eliminarlos, imputarlos o justificarlos antes del modelado,
- y evitar que distorsionen los resultados de los modelos de predicción.

En el Hotel 2, los outliers se concentran en un tramo específico, lo que puede deberse a **baja actividad temporal**, **cambios operativos**, **cierres parciales** o incidencias de datos.

## Conclusión general del EDA del Hotel 2

Tras este análisis, entiendo mucho mejor el comportamiento del Hotel 2:

- Tiene una estacionalidad clara tanto mensual como anual.
- La ocupación es alta la mayor parte del tiempo, salvo en algunos periodos concretos.
- El ADR muestra variaciones muy fuertes que habrá que tener en cuenta.
- Existen outliers que tendré que tratar antes de modelar.
- La serie temporal tiene potencial para modelos tanto SARIMA/Prophet como ML.

---

# Análisis Exploratorio del Hotel 3 (EDA)

Tras finalizar el análisis del Hotel 2, he replicado el mismo proceso para el Hotel 3 con el objetivo de comparar comportamientos y preparar el terreno para el modelado de la tasa de ocupación.

## 1. Evolución de roomnights

La serie temporal de roomnights en el Hotel 3 muestra:

- Un nivel alto y estable en el primer tramo.
- Una caída progresiva y consistente en el último periodo (2026), que sugiere un cambio estructural (p. ej., reducción de inventario, cambios operativos o cierre parcial).
- Mayor volatilidad al final de la serie.

## 2. Ocupación del hotel

La ocupación diaria (`ocup_total`) del Hotel 3:

- Mantiene valores altos inicialmente, con patrón relativamente estable.
- Presenta un descenso sostenido desde 2026 y dispersión creciente.
- Confirma la necesidad de considerar segmentación temporal (antes/después de 2026) en el modelado.

## 3. ADR (precio medio por habitación vendida)

El ADR en el Hotel 3:

- Es elevado en promedio, comparable o superior al Hotel 2.
- Tiene picos intensos en fechas concretas.
- Muestra una estacionalidad suave pero apreciable.

## 4. Distribuciones (roomnights, ocup_total y ADR)

Las distribuciones ayudan a entender la forma de los datos:

- `ocup_total`: sesgo a valores altos al inicio; más dispersión tras 2026.
- ADR: colas largas y multimodalidad por cambios de estrategia de precios.
- Roomnights: se aprecian dos regímenes (pre/post 2026).

## 5. Estacionalidad mensual y semanal

### Mensual

- Meses fríos y primavera con ocupación más alta.
- Tras 2026 aparecen meses completos con niveles más bajos y mayor variabilidad.

### Semanal

- Patrón menos marcado que el Hotel 2; la caída estructural enmascara diferencias entre días.

## 6. Correlaciones entre variables

La matriz de correlaciones en el Hotel 3:

- Refuerza la relación esperable entre `roomnights`, `bednights`, `neto` y ocupación.
- Muestra que la relación ADR ↔ demanda no siempre es directa (elasticidad variable).

## 7. Detección de outliers (ocupación)

He aplicado IQR sobre `ocup_total`. Hallazgos:

- Concentración de outliers al final de la serie, coherente con el cambio de régimen observado.
- Posible reflejo de la nueva operativa más que errores de datos.

## 8. Heatmap tipo calendario (ocupación diaria)

El heatmap de calendario permite ver semanas completas de alta/baja ocupación:

- En los primeros años predominan tonos rojos (alta ocupación) uniformes.
- A partir de 2026 aparecen más amarillos/naranjas, revelando baja ocupación y heterogeneidad entre semanas.

## Conclusión del EDA del Hotel 3

- Cambio estructural claro en 2026 → segmentar periodos en el modelado.
- ADR volátil con picos intensos.
- Outliers mayormente coherentes con el nuevo régimen.


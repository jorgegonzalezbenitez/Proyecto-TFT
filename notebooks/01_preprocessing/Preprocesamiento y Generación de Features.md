# Preprocesamiento y Feature Engineering

En esta fase se preparan los datasets que alimentan la fase de **modelado**.

El objetivo principal es generar datos:

- limpios
- causales
- sin fuga de información
- sin sobreajuste
- totalmente coherentes con el negocio hotelero

---

## Objetivo del pipeline

Transformar los datos originales en un dataset **listo para modelar ocupación**,
siguiendo un flujo claro y controlado:

**carga → generación de features → validación → exportación**

Este flujo permite mantener trazabilidad completa desde los datos originales
hasta los modelos finales.

---

## Cambio clave en el enfoque

Tras una revisión metodológica del proyecto, se realizó una depuración del
pipeline inicial para eliminar complejidad innecesaria y riesgos de sobreajuste.

### Variables eliminadas

El pipeline final **no incluye** durante el modelado:

- lags del target (`ocup_total_lag*`)
- medias móviles (`mm*`)
- variables temporales de alta cardinalidad:
  - `dayofyear`
  - `weekofyear`
  - `dow`
- shares de canales
- lags y medias móviles de canales
- agregados como `rn_total_canal`
- variables derivadas del target:
  - `roomnights`
  - `neto`
  - `stock`
  - `adr`
- variable artificial `post_2026` (no causal)

**Motivo:**
todas estas variables introducían **sobreajuste estructural**, redundancia o
filtrado indirecto de información del objetivo (`ocup_total`).

Estas variables se preservan únicamente en fases de **EDA**, nunca en el
pipeline de modelado.

---

## Nuevo enfoque

El pipeline final se apoya exclusivamente en variables simples, observables
y causales.

### Calendario básico

- `is_weekend`

Variable binaria que toma el valor 1 si el día es sábado o domingo y 0 en
caso contrario. Es conocida con antelación y representa un comportamiento
recurrente de demanda.

---

### Estacionalidad categórica

- `season` ∈ {`winter`, `spring`, `summer`, `autumn`}

Asigna a cada fecha una de las cuatro estaciones en función del mes al que
pertenece. Representa ciclos estacionales amplios y estables, reduciendo
ruido frente a enfoques continuos como `dayofyear`.

---

### Volumen real diario por canal (formato *wide*)

- `rn_WEL`
- `rn_TU`
- `rn_J`
- `rn_B`
- …

Cada variable `rn_*` representa el **número de habitaciones ocupadas ese día
que provienen de un canal de venta concreto**.

Estas variables describen el **mix de demanda diario del hotel**, permitiendo
saber no solo cuánta ocupación existe, sino **qué canales están impulsando
esa ocupación**.

El formato *wide* (una columna por canal) se utiliza porque:

- cada canal tiene dinámicas temporales distintas,
- permite capturar el impacto diferencial de cada fuente de demanda,
- evita mezclar comportamientos heterogéneos,
- facilita interpretación posterior mediante SHAP.

No se incluyen shares por canal, agregados ni variables derivadas del target
para preservar causalidad y evitar redundancia.

---

### Variable objetivo

- `ocup_total`

Tasa de ocupación diaria, utilizada exclusivamente como **target**, nunca
derivada ni anticipada mediante features.

---

## Estructura del preprocesamiento

- **Notebooks** → orquestan y validan el proceso
- **`src/`** → implementa la lógica reutilizable
- **`data/features`** → dataset final por hotel

---

## Features generadas

### Variables incluidas

- `date`
- `ocup_total`
- `is_weekend`
- `season`
- `rn_{canal}` por cada canal activo en el hotel

### Variables eliminadas

- ADR, stock, roomnights, neto
- lags y medias móviles
- `dayofyear`, `weekofyear`, `dow`
- variables no causales

---

## Output

Un único dataset final por hotel:

`data/features/hotel_ttoo/{HOTEL_1|HOTEL_2|HOTEL_3}.parquet`

Este dataset integra la fecha, las variables de calendario, estacionalidad
y volumen diario por canal de distribución, junto con la tasa de ocupación
como variable objetivo.

---

## Validación

Se comprueba:

- estructura homogénea entre hoteles
- ausencia de valores nulos
- coherencia temporal

---

## Conclusión

Este pipeline de preprocesamiento:

- simplifica drásticamente los datos
- elimina ruido y colinealidad
- reduce el riesgo de sobreajuste
- mejora la calidad del modelado
- facilita interpretabilidad y validación

El resultado es un dataset menos complejo en entrenamiento, pero **más
robusto, realista y defendible en un proyecto aplicado real**.
# Hotel Occupancy Forecasting — TFG Data Science & Engineering

Trabajo de Fin de Grado · Grado en Ciencia e Ingeniería de Datos · ULPGC  
Colaboración con grupo hotelero en Gran Canaria · Metodología CRISP-DM

---

## Privacidad de datos

Este proyecto se ha desarrollado en colaboración con un grupo hotelero real. Para proteger la identidad de la empresa y la confidencialidad de sus datos operativos, se han aplicado las siguientes medidas de anonimización:

- Los hoteles se identifican como **Hotel 1**, **Hotel 2** y **Hotel 3** a lo largo de todo el código, la documentación y el dashboard.
- Los canales de distribución y turoperadores se identifican mediante **alias de una o dos letras** (por ejemplo, `B`, `WEL`, `J`, `TU`), sin ninguna referencia a sus nombres reales.
- Los datasets originales no se incluyen en este repositorio. Todos los archivos de datos utilizados en el pipeline han sido previamente anonimizados.
- Las rutas, variables y nombres de archivos en el código no contienen ningún identificador real del grupo hotelero.

---

## Descripción del proyecto

Este proyecto aborda la predicción diaria de la tasa de ocupación hotelera en tres establecimientos con perfiles distintos: un hotel urbano, un hotel vacacional hiperestable y un hotel vacacional de perfil mixto. El objetivo es construir un sistema de inteligencia predictiva que combine modelos de Machine Learning, análisis de explicabilidad y simulación de escenarios estratégicos, integrado en un dashboard interactivo.

El desarrollo sigue la metodología **CRISP-DM** y está estructurado en seis fases.

---

## Fases del proyecto

### 1. Limpieza y preparación de datos

El punto de partida es un CSV con el histórico de reservas diarias por hotel y canal de distribución. Esta fase construye el pipeline de limpieza mediante procesamiento por bloques (`chunksize`) para manejar el volumen del dataset sin cargarlo completo en memoria.

Las transformaciones aplicadas incluyen la normalización de tipos, la eliminación de líneas agregadas duplicadas, la aplicación de reglas de consistencia sobre la variable `stock` (eliminación de registros con stock inferior al real y ajuste de los que lo superan), y la selección del registro más reciente por combinación hotel-canal-fecha.

El resultado son dos datasets agregados a nivel diario: uno por hotel y otro por hotel y canal, que sirven como base para todas las fases posteriores.

---

### 2. Análisis exploratorio (EDA)

El objetivo de esta fase fue comprender en profundidad el comportamiento de cada hotel antes de entrar en el modelado. El análisis se desarrolló en tres partes complementarias.

La primera estudió el comportamiento individual de cada hotel: evolución temporal de la ocupación, distribuciones, estacionalidad mensual y semanal, correlaciones entre variables y detección de outliers mediante IQR.

La segunda profundizó en el papel de los canales de distribución, identificando qué canales concentran la mayor parte de la demanda en cada hotel, cómo evoluciona su peso a lo largo del tiempo y qué dependencias estructurales existen.

La tercera llevó a cabo un análisis específico de picos y patrones estacionales. Para el hotel urbano se desarrolló un sistema de **Peak Intelligence** que identifica los picos máximos de ocupación, los contrasta con eventos reales ocurridos en la ciudad y evalúa si se repiten al año siguiente. Para los hoteles vacacionales se desarrolló un sistema de **Season Intelligence** basado en suavizado de serie y detección de regímenes de subida y bajada estructural por año.

---

### 3. Preprocesamiento y feature engineering

Esta fase construye el dataset final que alimenta los modelos, siguiendo un principio estricto de **causalidad**: no se incluye ninguna variable que implique fuga de información hacia el futuro.

Las variables eliminadas del pipeline de modelado incluyen lags y medias móviles del target, variables temporales de alta cardinalidad (`dayofyear`, `dow`), shares y derivados de canales, y variables derivadas del target como `roomnights`, `stock` o `ADR`.

Las variables finales utilizadas son exclusivamente tres tipos: el volumen diario real por canal en formato wide (`rn_*`), el indicador de fin de semana (`is_weekend`) y la estacionalidad categórica (`season`). El pipeline está implementado de forma modular en el directorio `src/` con funciones de carga, feature engineering y ensamblado separadas.

---

### 4. Modelado

La fase de modelado evalúa cinco familias de modelos con el mismo split temporal: entrenamiento hasta finales de 2024 y test desde 2025.

Se comienza con tres **baselines** (Naive, Seasonal Naive y Moving Average de 7 días) como referencia mínima. A continuación se evalúan modelos clásicos de series temporales: **ARIMA**, **SARIMA** y **SARIMAX** con variables exógenas causales. Finalmente se entrenan los modelos de Machine Learning: **Random Forest** y **XGBoost**, ambos con las mismas features causales.

Para todos los modelos se calculan MAE, RMSE y MAPE, y se generan gráficas de predicción, calibración y análisis de residuales. Los modelos de ML incorporan análisis de explicabilidad mediante **SHAP**, tanto en su versión global (peso medio y signo por variable) como en su versión temporal (evolución del impacto de cada canal a lo largo del año histórico). Las gráficas SHAP se exportan en PDF para su inclusión en la memoria.

XGBoost resulta el modelo ganador en los tres hoteles.

---

### 5. Evaluación e integración

Esta fase consolida todos los resultados del proyecto en datasets limpios y coherentes listos para el dashboard. Se ejecuta a través de siete notebooks especializados:

- **Dataset histórico unificado** — combina los tres hoteles en un único dataset multianual con todas las variables relevantes.
- **Comparación de modelos** — unifica métricas de todos los modelos, calcula deltas frente al baseline y determina el modelo ganador por hotel.
- **Dataset de predicciones** — concatena todas las predicciones en test con atributos temporales añadidos.
- **Importancias y explicabilidad** — unifica los coeficientes SARIMAX y los valores SHAP de RF y XGBoost en un único dataset normalizado.
- **Resumen EDA** — transforma el análisis exploratorio en estadísticas ejecutivas por hotel incluyendo canal dominante y shares.
- **Resumen de forecast** — unifica los forecast multiescenario de los tres hoteles en un único dataset.
- **SHAP temporal** — prepara el dataset de SHAP dinámico para su visualización en el dashboard.

---

### 6. Dashboard (Power BI)

El dashboard está construido en Power BI y estructurado en seis páginas navegables desde una portada de presentación. Por tema de confidencialidad con la empresa, no está subido a este repositorio.

La página de **Overview** muestra los KPIs principales (ocupación media, máxima, volatilidad, estacionalidad y canal dominante) junto con la evolución histórica diaria, filtrable por hotel y año.

La página de **EDA & Peak Intelligence** combina boxplots de estacionalidad mensual y semanal con el gráfico principal de Season Intelligence (serie suavizada con franjas de régimen y marcadores de máximos y mínimos anuales), el mix de canales por roomnights y la evolución temporal apilada por canal.

La página de **Model Performance** compara todos los modelos mediante gráficas de real vs predicción, scatter de calibración y barras comparativas de MAE, RMSE y MAPE.

La página de **Drivers & Explicabilidad** incluye el gráfico SHAP global con signo, el donut de peso por familia de canal, la influencia temporal SHAP dinámica filtrable por canal, y heatmaps de efecto estacional y efecto de calendario.

La página de **Forecast 2026** presenta los KPIs del escenario seleccionado y un gráfico HTML interactivo construido en DAX que superpone la línea del histórico real 2025 con la línea del escenario forecast, con banda de área coloreada dinámica y tooltip con delta en puntos porcentuales.

---

## Stack tecnológico

| Área | Tecnologías |
|------|-------------|
| Lenguaje | Python 3.11 |
| Procesamiento | pandas, numpy, pyarrow |
| Modelado | scikit-learn, xgboost, statsmodels |
| Explicabilidad | shap |
| Visualización Python | matplotlib, seaborn |
| Dashboard | Power BI (DAX, Deneb/Vega-Lite, HTML visual) |
| Pipeline modular | módulos propios en `src/` |

---

## Resultados resumidos (modelo XGBoost — conjunto test)

| Hotel | MAPE |
|-------|------|
| Hotel 1 (urbano) | 9.4% |
| Hotel 2 (vacacional) | 6.4% |
| Hotel 3 (mixto) | 5.9% |

---

## Autor

Jorge González Benítez  
Grado en Ciencia e Ingeniería de Datos · ULPGC  
Curso 2024–2025

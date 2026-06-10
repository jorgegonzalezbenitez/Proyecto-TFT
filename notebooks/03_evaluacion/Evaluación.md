# Fase de Evaluación del Proyecto
Integración final de métricas, predicciones, forecast y season intelligence

La fase de **Evaluación** constituye el puente final entre el proceso de modelado
y el dashboard del proyecto.
Mientras que el modelado produce métricas, predicciones y modelos entrenados,
en esta fase:

1. consolido todos los resultados cuantitativos (métricas, predicciones,
   importancias, EDA),
2. unifico el **forecast multiescenario** generado en la fase de modelado,
3. incorporo el **Peak/Season Intelligence** derivado de la fase de exploración
   avanzada,
4. preparo **todos los datasets finales que alimentan el dashboard**.

Es la fase donde las distintas piezas del pipeline convergen en un único
repositorio de información coherente, completo y listo para visualización.

La fase está organizada en **seis notebooks**, cada uno con un objetivo muy
específico.

---

# 0. `00_historical_dataset.ipynb`

## Objetivo

Crear un dataset histórico unificado, multianual y granular (día a día), con toda
la información real utilizada durante el EDA previo al modelado. Este dataset se
convierte en la tabla de hechos (fact table) del dashboard en Power BI y es la
base para:

- KPIs filtrables por año
- Tendencias reales multianuales
- Mix de touroperadores anual
- Estacionalidad histórica
- Peak Analysis basado en datos reales
- Volatilidad y comportamiento temporal por hotel

## ¿Por qué es necesario?

Hasta este punto del proyecto, todos los datasets generados estaban orientados a:

- comparar modelos,
- analizar predicciones,
- construir forecast,
- estudiar peaks y estacionalidad global.

Sin embargo, ninguno contenía el histórico completo multianual día a día,
indispensable para:

- filtrar por año en Power BI,
- mostrar tendencias reales (no solo predicciones del test),
- calcular KPIs dinámicos por año,
- reconstruir el comportamiento temporal de cada hotel,
- analizar el mix real de canales a lo largo del tiempo.

Por ello, se genera un dataset completo y depurado, unificado para los tres hoteles.

## ¿Qué hace este notebook?

Carga los históricos reales procesados previamente:

- `data/features/hotel_ttoo/HOTEL_1.parquet`
- `data/features/hotel_ttoo/HOTEL_2.parquet`
- `data/features/hotel_ttoo/HOTEL_3.parquet`

Estandariza columnas:

- `fecha` (como datetime)
- `hotel`
- `ocup_total`
- `season`
- `is_weekend`
- todos los `rn_*` de cada touroperador

Unifica los tres hoteles en un único DataFrame, ordena por fecha y hotel, y exporta:

- `historical_dataset.parquet`

---

# 1. `01_model_comparison.ipynb`

## Objetivo
Unificar y comparar todas las métricas de todos los modelos desarrollados (MAE,
RMSE, MAPE), por hotel y por técnica.

## ¿Qué hace?
Carga métricas de:

- Baselines (Naive, MA7, Seasonal Naive)
- ARIMA, SARIMA, SARIMAX
- Random Forest
- XGBoost (modelo ganador)

Calcula delta absoluto y porcentual frente al baseline, genera ranking por hotel
y selecciona el **mejor modelo real** (excluyendo baselines).

Exporta:

- `model_comparison.parquet`
- `best_models.parquet`

## ¿Para qué sirve?
Comparación profesional entre técnicas, elección del modelo óptimo para
forecasting y base de la sección "Comparación de modelos" del dashboard.

---

# 2. `02_predictions_dataset.ipynb`

## Objetivo
Unificar **todas las predicciones históricas** de todos los modelos en un único
dataset granular.

## ¿Qué hace?
Carga:

- `arima_predictions.parquet`
- `sarima_predictions.parquet`
- `sarimax_predictions.parquet`
- `random_forest_predictions.parquet`
- `xgb_predictions.parquet`

Concatena en estructura:

| fecha | hotel | modelo | y_real | y_pred | error_abs | error_pct |

Añade atributos temporales (año, mes, semana, día de la semana) y exporta:

- `predictions_dataset.parquet`

## ¿Para qué sirve?
Análisis fino de error, gráficas real vs predicción, identificación de sesgos
temporales y base para varias visualizaciones del dashboard.

---

# 3. `03_feature_importance.ipynb`

## Objetivo
Unificar toda la explicabilidad del proyecto: coeficientes SARIMAX, SHAP de
Random Forest y SHAP de XGBoost.

## ¿Qué hace?
Carga:

- `sarimax_importance_features.csv`
- `random_forest_importance_features.csv`
- `xgb_importance_features.csv`

Normaliza weight (magnitud), sign, sign_value, rank y family, y exporta:

- `feature_importance.parquet`

## ¿Para qué sirve?
Comparaciones RF vs XGB vs SARIMAX, identificación de drivers reales por hotel
y visualizaciones explicativas en el dashboard.

---

# 4. `04_eda_summary.ipynb`

## Objetivo
Transformar el EDA inicial (hotel y touroperadores) en un **resumen ejecutivo**
claro y utilizable en el dashboard.

## ¿Qué hace?
Carga:

- `hotel_day_hotel_final.parquet`
- `hotel_day_ttoo_final.parquet`

Calcula resumen por hotel: estadísticas temporales, estacionalidad,
correlaciones, touroperador dominante y shares, y diversidad del mix.

Exporta:

- `eda_summary.parquet`

## ¿Para qué sirve?
Página "Hotel Overview" y narrativa comercial del TFG.

---

# 5. `05_forecast_summary.ipynb`

## Objetivo
Unificar todos los forecast multiescenario (Hotel 1, Hotel 2, Hotel 3) en un
único dataset.

## ¿Qué hace?
Carga:

- `forecast_HOTEL_1.parquet`
- `forecast_HOTEL_2.parquet`
- `forecast_HOTEL_3.parquet`

Normaliza las diferentes estructuras, reconstruye fecha si es necesario y añade:

- `year`, `month`, `week`, `dow`, `dayofyear`
- `season_winter`, `season_spring`, `season_summer`, `season_autumn`

Exporta:

- `forecast_summary.parquet`

## ¿Para qué sirve?
Visualización multiescenario por hotel, comparación entre escenarios, filtrado
por temporada y base de la página "Forecast 2026" del dashboard.

---

# 6. `06_peak_summary.ipynb`

## Objetivo
Unificar los análisis avanzados de **Peak/Season Intelligence** de los tres
hoteles en un dataset estandarizado para el dashboard.

## ¿Qué hace?
Carga:

- `peak_HOTEL_1.parquet`
- `peak_HOTEL_2.parquet`
- `peak_HOTEL_3.parquet`

Normaliza estructuras distintas según el tipo de hotel:

- Hotel 1 → eventos puntuales
- Hotel 2 / Hotel 3 → segmentos estacionales PEAK/VALLEY

Añade season reconstruida y atributos temporales, y exporta:

- `peak_summary.parquet`

## ¿Para qué sirve?
Página "Peaks & Season Intelligence", comparativa pico–real +1año/+2año,
riesgos y oportunidades futuras, e inteligencia temporal avanzada por hotel.

---

# 7. `07_shap_temporal_summary.ipynb`

## Objetivo
Unificar y preparar la **explicabilidad temporal (SHAP dinámico)** del modelo
**XGBoost** en un dataset estandarizado, listo para su uso en el dashboard final.

Este notebook complementa la explicabilidad global del proyecto, permitiendo
analizar **cuándo** cada canal (`rn_*`) influye realmente sobre la ocupación y
conectando de forma directa el modelado con los escenarios de forecast definidos
en la fase anterior.

## ¿Qué hace este notebook?

Carga el dataset generado en la fase de modelado:

- `models/importances/xgb_shap_temporal.csv`

Limpia y valida la estructura (fechas, hoteles, canales `rn_*`, valores SHAP),
añade atributos temporales clave (año, mes, semana, día de la semana, día del
año) y exporta:

- `xgb_shap_temporal.parquet`

## ¿Para qué sirve?

Este dataset permite incorporar una capa avanzada de explicabilidad en el
dashboard, haciendo posible:

- Visualizar la **influencia SHAP alineada con la serie temporal de ocupación**.
- Identificar **regímenes temporales**, valles, picos y transiciones.
- Validar empíricamente los escenarios de forecast multiescenario.
- Diferenciar entre canales estructurales, palancas tácticas y efectos puntuales.

Gracias a este notebook, el dashboard incorpora una página específica de
**"SHAP Temporal por Canal"**, que transforma la interpretabilidad del modelo
de una lectura estática a una **visión dinámica y operativa**.

---

# Conclusión de la Fase de Evaluación

Esta fase consolida **todos** los resultados del proyecto en **datasets limpios,
coherentes y listos para dashboard**, integrando modelado, forecast, exploración,
peak analysis, explicabilidad y análisis temporal avanzado.

Gracias a esta fase, el dashboard final puede construirse sobre una base
**sólida, completa y profesional**, donde cada pieza del pipeline queda unificada
de forma clara, trazable y coherente con la lógica del TFG.
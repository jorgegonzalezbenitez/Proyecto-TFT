# 📘 Modelado

Este capítulo recoge TODA la fase de modelado del proyecto:  
desde los baselines iniciales hasta la comparativa final entre modelos clásicos de series temporales y modelos avanzados de Machine Learning.  
Tras depurar completamente el pipeline para evitar fuga de información, solo se utilizan **variables completamente causales**:

- `rn_*` → roomnights por turoperador del mismo día  
- `season` → estacionalidad categórica (OHE)  
- `is_weekend` → indicador estructural semanal  
- nunca `dow` (ordinal), nunca lags ni medias móviles del target

Esto garantiza un escenario realista y defendible de forecasting.

---

# 1. Modelado Baseline

## 1.1 Objetivo
Establecer una referencia mínima de rendimiento predictivo mediante modelos simples:

- Naive (persistencia)
- Seasonal Naive (replica semana previa)
- Media Móvil MA(7)

Estas líneas base permiten medir el valor añadido de modelos más avanzados.

## 1.2 Resultados
Los baselines muestran un patrón claro:

- **HOTEL_2 y HOTEL_3** → Naive es extremadamente fuerte (MAPE ≈ 5–10%).  
  → Hoteles hiperestables.

- **HOTEL_1** → mayor variabilidad → MA(7) funciona mejor que Naive.  

Conclusión baseline:
> En hoteles vacacionales, la persistencia explica prácticamente toda la ocupación; en hoteles urbanos, la variabilidad diaria dificulta modelos simples.

---

# 2. Modelado ARIMA

ARIMA modela exclusivamente la estructura temporal histórica.

## 2.1 Resultados
| Hotel | MAE |
|-------|------|
| HOTEL_1 | 0.1158 |
| HOTEL_2 | 0.1819 |
| HOTEL_3 | 0.1757 |

Conclusión ARIMA:
> ARIMA no mejora a los baselines.  
> Las series requieren estacionalidad o variables externas.

---

# 3. Modelado SARIMA

Se introduce estacionalidad semanal (s=7).

## 3.1 Resultados
| Hotel | MAE |
|-------|------|
| HOTEL_1 | 0.1160 |
| HOTEL_2 | 0.1848 |
| HOTEL_3 | 0.1799 |

Conclusión SARIMA:
> La estacionalidad semanal aporta muy poco.  
> Las curvas siguen demasiado planas y no captan picos.

---

# 4. Modelado SARIMAX  
Pipeline causal definitivo — **sin fuga**

Tras eliminar:

❌ lags  
❌ medias móviles  
❌ dow  
❌ features temporales artificiales  
❌ season_* ordinal  
✅ solo `rn_*`, `is_weekend`, `season_*` OHE

SARIMAX se vuelve **estable y realista**.

## 4.1 Resultados finales
| Hotel | MAE |
|-------|------|
| HOTEL_1 | 0.1076 |
| HOTEL_2 | 0.0934 |
| HOTEL_3 | 0.1357 |

Conclusión SARIMAX:
> Útil, interpretable y estable, pero limitado:  
> sigue siendo un modelo lineal y no capta interacciones o no linealidades entre TTOO.

## 4.2 Influencia por hotel (coeficientes + IC95%)

### 🏨 HOTEL_1 — Urbano
- `rn_B` (+)  
- `rn_WEL` (+)  
- `rn_J` (+ leve)  
- `is_weekend` no significativo  

### 🏨 HOTEL_2 — Vacacional hiperestable
- `rn_T` (+, muy significativo)  
- `rn_J` (+)  

### 🏨 HOTEL_3 — Vacacional moderado
- `rn_J` (+ dominante)  
- `rn_T` (+ complementario)

SARIMAX confirma:  
**OTA domina HOTEL_1**, **T domina HOTEL_2**, **J domina HOTEL_3**.

---

# 5. Random Forest (pipeline causal final)

Se usa **EXCLUSIVAMENTE**:

- `rn_*`
- `is_weekend`
- `season_*` (one-hot)

## 5.1 Resultados finales
| Hotel | MAE | MAPE |
|-------|---------|---------|
| HOTEL_1 | 0.0692 | 13.1% |
| HOTEL_2 | 0.0675 | 9.86% |
| HOTEL_3 | 0.0366 | 6.26% |

RF supera claramente a SARIMAX y a todos los modelos temporales.

## 5.2 SHAP (peso + signo)

### HOTEL_1
- `rn_B` (+)  
- `rn_WEL` (+)  

### HOTEL_2
- `rn_T` (peso alto, **signo negativo medio**)  
- `rn_J` (+)  

> **Explicación clave del TFG**:  
> El signo negativo de `rn_T` no indica que "T baje la ocupación",  
> sino que **XGBoost/RF detectan que los días con más T coinciden con periodos estructuralmente menos altos** (valles, rotaciones, inicios/fin de temporada).

### HOTEL_3
- `rn_J` (+ dominante)  
- `rn_T` (peso secundario, signo negativo leve)

---

# 6. XGBoost (modelo final del proyecto)

## 6.1 Resultados finales
| Hotel | MAE | MAPE |
|-------|----------|----------|
| **HOTEL_1** | **0.0520** | **9.44%** |
| **HOTEL_2** | **0.0449** | **6.43%** |
| **HOTEL_3** | **0.0357** | **5.93%** |

✅ Mejor modelo en los tres hoteles  
✅ Captura interacciones complejas  
✅ Estable y bien calibrado  
✅ Explicabilidad con SHAP muy clara

## 6.2 Drivers según SHAP

### HOTEL_1  
`rn_B`, `rn_WEL` → motores principales  

### HOTEL_2  
`rn_T` → régimen temporal  
`rn_J` → picos  

### HOTEL_3  
`rn_J` → driver dominante  

---

# 7. Comparativa final entre todos los modelos

## 7.1 Mejor modelo por hotel (sin baselines)
**XGBoost gana en HOTEL_1, HOTEL_2 y HOTEL_3.**

## 7.2 Conclusiones por tipo de hotel

### 🏨 HOTEL_1 (urbano - OTA)
- ML > SARIMAX > SARIMA > ARIMA > baselines  
- XGB mejora un **38%** vs baseline  
- Drivers: `rn_B`, `rn_WEL`

### 🏨 HOTEL_2 (vacacional hiperestable)
- Naive baseline casi imbatible  
- Mejor modelo real → **XGBoost**  
- Drivers: `rn_T` (régimen), `rn_J` (picos)

### 🏨 HOTEL_3 (vacacional moderado)
- XGB logra MAPE < 6%  
- Driver: `rn_J`  

---

# ✅ 8. Conclusión general del capítulo de modelado

> En un pipeline causal y sin fuga,  
> **XGBoost es el modelo dominante**, superando a SARIMAX y Random Forest en los tres hoteles y capturando interacciones no lineales críticas entre TTOO, estacionalidad y ocupación.  
>  
> La estructura de demanda varía significativamente entre hoteles:  
> - **HOTEL_1** depende de canales online (`rn_B`, `rn_WEL`).  
> - **HOTEL_2** depende del mix turoperado donde **`rn_T` marca el régimen temporal**.  
> - **HOTEL_3** depende de **`rn_J`** casi en exclusiva.  
>  
> La coherencia entre SARIMAX (coeficientes) y ML (SHAP) valida la metodología completa y confirma que el modelo XGBoost es la mejor elección para forecasting y análisis operativo.
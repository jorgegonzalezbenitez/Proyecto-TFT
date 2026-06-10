# Fase de Dashboard — Visualización e Inteligencia Operativa
Construcción del cuadro de mando interactivo en Power BI sobre el análisis predictivo de la ocupación hotelera

Esta fase representa el cierre del ciclo **CRISP-DM** del proyecto.
Todo el trabajo previo — exploración, modelado, evaluación y forecast — converge
aquí en un dashboard profesional e interactivo, construido en **Power BI**, que
permite explorar los resultados de forma visual, dinámica y accesible.

El dashboard está estructurado en **seis páginas**, cada una con un propósito
claro y diferenciado, navegables desde una portada de presentación.

---

# 0. Portada — Presentación

## Objetivo

Ofrecer una entrada profesional al dashboard, contextualizando el proyecto antes
de entrar al análisis.

## ¿Qué contiene?

- **Título principal:** *Análisis predictivo de la ocupación hotelera*
- **Subtítulo:** *Inteligencia de datos aplicada a la gestión y predicción de la
  ocupación vacacional*
- Datos académicos: Trabajo de Fin de Grado, Grado en Ciencia e Ingeniería de
  Datos, Escuela de Ingeniería Informática — ULPGC, autor y curso académico
- **Botón de navegación** *"Explorar dashboard →"* que lleva directamente a la
  primera página de análisis

## Decisiones de diseño

El fondo es **azul marino oscuro (`#1E2A3A`)**, lo que diferencia la portada del
resto de páginas y genera un efecto de entrada profesional. El texto usa jerarquía
tipográfica clara: título en blanco puro, subtítulo en gris azulado claro, y datos
académicos en un tono más suave. Una línea separadora en verde conecta visualmente
con la identidad del proyecto.

---

# 1. Overview — Panorama Operativo del Hotel

## Objetivo

Ofrecer una visión global del comportamiento histórico de la ocupación por hotel
y año, con las métricas clave en un vistazo.

## ¿Qué contiene?

- **KPIs principales** filtrables dinámicamente:
  - Ocupación Media
  - Ocupación Máxima
  - Volatilidad (σ) — variabilidad diaria
  - Estacionalidad — perfil anual
  - Canal Dominante — touroperador con mayor peso

- **Gráfico de evolución histórica de la ocupación** — línea temporal diaria con
  área rellena, filtrable por hotel y año

- **Panel de filtros** con slicer de Hotel (Hotel 1, Hotel 2, Hotel 3) y Año
  (2023, 2024, 2025), con formato de panel lateral estilizado

## Decisiones de diseño

El título del gráfico es dinámico — se actualiza automáticamente mostrando el
hotel y año seleccionados. Los slicers siguen el estilo corporativo del dashboard:
fondo gris claro (`#F4F6F8`), borde suave, acento lateral verde, agrupados dentro
de un contenedor con título *"Filtros de análisis"*.

---

# 2. EDA & Peak Intelligence — Inteligencia Operativa y de Demanda

## Objetivo

Profundizar en los patrones de ocupación, estacionalidad y contribución de
touroperadores, combinando análisis exploratorio con inteligencia de picos y
valles estacionales.

## ¿Qué contiene?

- **Distribución mensual de la ocupación** — gráfico de cajas (boxplot) por mes,
  mostrando la variabilidad intra-mensual
- **Día laboral vs. Fin de semana** — boxplot comparativo del comportamiento según
  tipo de día
- **Season Intelligence** — gráfico principal de la página con:
  - Serie suavizada (EMA span=14) de la ocupación histórica multianual
  - Franjas coloreadas de fases estacionales (valles en azul, picos en rojo)
  - Puntos de máximo y mínimo anual con etiquetas de fecha y valor
  - Los máximos se posicionan sobre la serie suavizada; los mínimos sobre el valor real
  - Botones Hotel 1 / Hotel 2 / Hotel 3 para cambiar de hotel directamente en el
    gráfico mediante marcadores
- **Mix de touroperadores por roomnights acumulados** — gráfico de barras con el
  peso de cada canal (`rn_*`)
- **Evolución de Roomnights por canal** — área apilada temporal mostrando la
  contribución dinámica de cada touroperador

## Decisiones de diseño

El gráfico de Season Intelligence fue uno de los más trabajados del proyecto. La
decisión de usar la serie suavizada como protagonista visual, con los valores reales
en los tooltips y los marcadores anuales posicionados estratégicamente, permite leer
la estacionalidad de forma intuitiva sin sacrificar precisión. Los máximos y mínimos
coinciden exactamente con los KPIs de la página Overview, garantizando coherencia
entre páginas.

---

# 3. Model Performance & Validación — Evaluación de Modelos Predictivos

## Objetivo

Comparar el rendimiento de todos los modelos entrenados y validar visualmente la
calidad de las predicciones.

## ¿Qué contiene?

- **Esquema de validación temporal** — diagrama visual que explica la división
  TRAIN / TEST con la frontera en 2025
- **Ocupación real vs predicción** — gráfico de líneas con la serie real (azul
  sólida) y la predicción (verde discontinua), filtrable por hotel y modelo
- **Precisión del modelo** — scatter plot de valores reales vs predichos en el
  conjunto de test, con línea diagonal de referencia perfecta
- **Comparativa de modelos (MAE)** — gráfico de barras comparando el Error Absoluto
  Medio de todos los modelos, con línea de baseline y colores diferenciados (azul
  para los mejores, rojo para los peores)
- **Validación de modelos (RMSE y MAPE)** — gráfico de barras agrupadas con ambas
  métricas normalizadas por modelo

## Decisiones de diseño

El modelo ganador es **XGBoost** de forma consistente en los tres hoteles, quedando
visualmente claro en los gráficos de comparativa. El esquema de validación temporal
se diseñó como un visual nativo de Power BI (formas y cuadros de texto) para
explicar de forma intuitiva la metodología de evaluación sin necesidad de texto
adicional.

---

# 4. Drivers & Explicabilidad — Drivers de Ocupación y Dinámicas de Influencia

## Objetivo

Explicar qué variables y canales impulsan o frenan la ocupación hotelera, con qué
peso y en qué momentos del año.

## ¿Qué contiene?

- **Impacto de variables sobre la ocupación** — gráfico de barras horizontales con
  valores SHAP positivos (verde) y negativos (rojo), ordenados por importancia global
- **Peso relativo por familia de canal** — gráfico de donut mostrando la distribución
  de influencia entre grupos de canales (OTAs, touroperadores, estación, calendario)
- **Influencia temporal del canal** — gráfico de línea temporal con el efecto SHAP
  dinámico del canal seleccionado sobre la ocupación diaria, filtrable por touroperador
- **Efecto estacional de los canales** — heatmap matricial (canal × estación) con
  intensidad de color que refleja el impacto SHAP por estación
- **Efecto del calendario** — heatmap similar (canal × tipo de día: laboral vs fin
  de semana)

## Decisiones de diseño

Los heatmaps usan un degradado de color desde beige claro hasta rojo fuerte
(`#C0392B`), evitando que los valores máximos caigan en colores casi negros que
dificultan la lectura. Las etiquetas de valor y los indicadores de dirección (▲/▼)
dentro de cada celda permiten leer el heatmap sin necesidad de leyenda adicional.
El texto blanco se activa automáticamente cuando el fondo supera cierto umbral de
intensidad, garantizando legibilidad en toda la escala.

---

# 5. Forecast 2026 & Estrategia — Forecast y Simulación de Escenarios

## Objetivo

Proyectar la ocupación para 2026 bajo distintos escenarios estratégicos y evaluar
su impacto frente al histórico real del año anterior.

## ¿Qué contiene?

- **KPIs del escenario seleccionado:**
  - Ocupación Real 2025
  - Ocupación Estimada 2026
  - Mejora Estimada (Δ vs Histórico)
  - Volatilidad (σ) del escenario
  - Días con mayor ocupación vs histórico 2025
  - Evaluación del escenario (Escenario estable / Riesgo / Mejora)

- **Gráfico HTML interactivo** — visualización personalizada construida en DAX +
  SVG/JavaScript con:
  - Línea suavizada del histórico real (azul grisáceo, EMA span=3)
  - Línea suavizada del escenario forecast (verde `#2BB673`, EMA span=3, animada
    segmento a segmento)
  - Banda de área entre ambas curvas (verde semitransparente cuando el escenario
    supera al histórico, roja cuando lo empeora)
  - Tooltip interactivo con fecha, valor histórico, valor del escenario y delta en
    puntos porcentuales
  - Leyenda interna dentro del área del gráfico
  - Título dinámico: *Escenario seleccionado — Hotel*
  - Subtítulo: *Comparativa de la ocupación proyectada frente al comportamiento
    real del año anterior*

- **Panel de filtros** con slicer de Hotel (Hotel 1, Hotel 2, Hotel 3) y Escenario
  Estratégico (opciones específicas por hotel)

## Decisiones de diseño

El gráfico principal de esta página fue el más complejo del proyecto — construido
íntegramente como medida DAX que genera HTML/SVG dinámico. La animación segmento
a segmento de la línea del escenario, el suavizado EMA aplicado en JavaScript antes
del renderizado, y la banda de área coloreada dinámicamente hacen de esta
visualización el elemento más diferencial del dashboard. El cruce entre el histórico
real (tabla `historico`) y el forecast (tabla `forecast_summary`) se resuelve en DAX
puro mediante join por fecha, garantizando que los valores mostrados en el tooltip
coincidan exactamente con los KPIs de la página.

---

# Conclusión de la Fase de Dashboard

El dashboard final integra de forma coherente y navegable todos los resultados del
proyecto:

- el histórico real multianual de los tres hoteles,
- el análisis exploratorio y de estacionalidad avanzado,
- la evaluación comparativa de cinco modelos predictivos,
- la explicabilidad de variables mediante SHAP,
- y la simulación de escenarios estratégicos para 2026.

Cada página tiene un propósito diferenciado pero complementario, y juntas cuentan
la historia completa del proyecto: **de los datos históricos a la inteligencia
accionable**.

El resultado es un cuadro de mando que no solo presenta resultados, sino que permite
al usuario explorarlos, filtrarlos y comprenderlos en tiempo real — cumpliendo el
objetivo final de la metodología CRISP-DM: transformar el conocimiento extraído en
valor operativo real.
# Fase de Forecast del Proyecto

La fase de **Forecast** representa el punto donde el proyecto deja de analizar el
pasado para comenzar a **predecir el futuro**.  
Después de seleccionar el mejor modelo para cada hotel en la fase de modelado, en
esta fase utilizo dichos modelos para generar **proyecciones multiescenario**,
simulando decisiones comerciales realistas y respondiendo preguntas del tipo:

- "¿Qué pasaría si refuerzo un canal en una temporada concreta?"
- "¿Qué ocurre si reduzco cupo en mi canal dominante?"
- "¿Puedo suavizar los valles de ocupación?"
- "¿Quién aporta valor en cada temporada?"

Todos los forecast respetan el **pipeline causal**, usando únicamente las variables:

- `rn_*` (actividad por canal del día)
- `season_*` (winter, spring, summer, autumn)
- `is_weekend`

**Nunca se manipula la demanda**, solo se simulan **acciones reales del hotel**
sobre su *oferta/cupo*, lo cual los hace plenamente defendibles a nivel académico
y empresarial.

Cada hotel requiere escenarios distintos y específicos, ya que su comportamiento,
estacionalidad y drivers comerciales son diferentes.

---

## Aportación del análisis SHAP al diseño de escenarios de Forecast

Además de los escenarios basados en calendario y reglas de negocio, en esta fase
se incorpora la información derivada del **análisis SHAP temporal**, que permite:

- identificar **cuándo** un canal tiene impacto real sobre la ocupación,
- diferenciar entre **palancas estructurales** y **acciones tácticas**,
- y evolucionar desde escenarios puramente calendarizados hacia escenarios
  **guiados por el comportamiento observado del modelo**.

Este enfoque es especialmente relevante en los hoteles vacacionales (**Hotel 2 y
Hotel 3**), donde el SHAP temporal permite afinar los escenarios y jerarquizarlos
según su impacto real.

---

# 1. `forecast_HOTEL_1.ipynb` — Hotel 1 (urbano, OTA–driven)

## Objetivo
Predecir la ocupación 2026 de Hotel 1 mediante **XGBoost**, el modelo ganador, y
simular escenarios basados en su realidad digital. Hotel 1 es un hotel **poco
estacional y muy dependiente de canales OTA**, especialmente B (B) y WEL
(Weblivvo).

## Qué se hace en este notebook

- Carga del dataset Hotel 1 con pipeline causal (`rn_*`, `season_*`, `is_weekend`)
- One-hot encoding de `season`
- Entrenamiento del modelo **XGBoost**
- Construcción de futuros para 2026
- Diseño de escenarios WHAT‑IF **100% realistas**:

#### BAU (Business-as-usual)
Proyección sin cambios estratégicos.

#### ESTACIONAL
Replica el patrón día‑mes del histórico mediante `season_*`.

#### OTA_INVIERNO
Aumento de cupo/visibilidad en B y WEL en invierno
(acción realista para aumentar ocupación en temporada baja).

#### T_VERANO
Prueba realista de apertura de cupo a T en verano
(conclusión: impacto mínimo → Hotel 1 no es un hotel turoperado).

#### OTA_SEMANA_SANTA
Reducción temporal de OTA para evaluar resiliencia del hotel.

#### LOW_DEMAND_PROTECTION
Refuerzo selectivo de OTA únicamente en días históricamente débiles.

## Utilidad

- Confirma que Hotel 1 es **muy estable** y **resiliente**.
- El hotel opera casi exclusivamente con OTA, pero su demanda es poco elástica.
- Las decisiones comerciales tienen impacto moderado.
- El SHAP temporal confirma que **no existen palancas estructurales sostenidas**,
  sino oportunidades puntuales y tácticas, coherentes con un hotel urbano.

## Exportación

`forecast/outputs/forecast_HOTEL_1.parquet`

---

# 2. `forecast_HOTEL_2.ipynb` — Hotel 2 (vacacional hiperestable, T dominante)

## Objetivo
Realizar un forecast multiescenario con XGBoost para un hotel **vacacional muy
estable**, dominado por **T** y con valles y picos claramente definidos.

## Qué se hace en este notebook

- Carga del dataset Hotel 2 (pipeline causal)
- One-hot de `season`
- Entrenamiento XGBoost
- Creación del futuro 2026
- Escenarios WHAT‑IF adaptados a su estructura:

#### BAU
Proyección base, extremadamente estable.

#### ESTACIONAL
Reproducción de valles (spring/autumn) y picos (summer).

#### T_VERANO
Mayor cupo en T en verano → impacto moderado.

#### J_SHOULDER
Reforzar J en spring y autumn → **escenario más potente**.
Reduce valles y suaviza la temporada.

#### DIVERSIFICACION_T
Reducción de cupo T en agosto–septiembre.
Mide dependencia del canal.

#### OTA_INVIERNO
Reforzar OTA en invierno para ver si abren temporada baja (impacto débil).

#### J_SMART_VALLEY ⭐
Refuerzo **dinámico** de J únicamente en aquellos días futuros que coinciden
con patrones históricos de baja ocupación, identificados a partir del análisis
SHAP temporal.

## Utilidad

- Hotel 2 es **hiperestable** (su propia estructura domina).
- J muestra capacidad de mejorar valles.
- T define el régimen, no los picos.
- El SHAP temporal permite identificar **cuándo actuar con J**, no solo dónde,
  jerarquizando los escenarios.

## Exportación

`forecast/outputs/forecast_HOTEL_2.parquet`

---

# 3. `forecast_HOTEL_3.ipynb` — Hotel 3 (vacacional moderado, J dominante)

## Objetivo
Simular escenarios sobre un hotel vacacional donde **J es el canal decisivo**,
con gran estacionalidad y valles profundos.

## Qué se hace en este notebook

- Carga de Hotel 3 con pipeline causal
- One-hot de `season`
- Entrenamiento XGBoost
- Forecast day-by-day 2026
- Escenarios realistas:

#### BAU
Patrón natural del hotel.

#### ESTACIONAL
Reproducción de picos y valles reales.

#### J_VERANO
Refuerzo del canal dominante J en verano → mejora notable.

#### J_SHOULDER
Reforzar J en spring y autumn → escenario muy útil, reduce valles.

#### T_OTOÑO
Probar si T puede alargar temporada → impacto leve.

#### OTA_INVIERNO
Reforzar OTA en invierno → impacto bajo.

#### DIVERSIFICACION_J
Reducir cupo del canal dominante J a final de verano → caída suave.

#### J_SMART_GLOBAL ⭐
Refuerzo **estructural** de J durante la mayor parte del año, excluyendo
únicamente aquellos periodos históricamente asociados a valles extremos,
según el SHAP temporal.

## Utilidad

- Hotel 3 es el hotel más **sensible** a sus escenarios:
  - J mueve la aguja de forma clara
  - OTA y T tienen efecto bajo o compensatorio
- El SHAP temporal explica por qué reducir J empeora el forecast y justifica
  escenarios de refuerzo estructural.

## Exportación

`forecast/outputs/forecast_HOTEL_3.parquet`

---

# Conclusión global de la Fase de Forecast

La fase de forecast transforma la modelización en una herramienta estratégica de
negocio. Gracias a los modelos XGBoost entrenados por hotel y los escenarios WHAT‑IF:

- **Hotel 1** → hotel urbano muy estable, resiliente y OTA‑driven
- **Hotel 2** → hotel hiperestable; J suaviza valles; T define régimen
- **Hotel 3** → hotel vacacional sensible a J; fuerte estacionalidad

La incorporación del **SHAP temporal** permite:

- diseñar escenarios **más precisos y jerarquizados**,
- diferenciar palancas estructurales de acciones tácticas,
- y conectar directamente interpretabilidad y forecast.

Los forecast permiten:

- Evaluar decisiones comerciales **antes** de implementarlas.
- Medir sensibilidad por canal.
- Anticipar riesgos operativos.
- Identificar oportunidades para alargar temporada o elevar valles.
- Preparar estrategias diferenciales por tipo de hotel.

Los archivos generados (`forecast_HOTEL_*.parquet`) están listos para el dashboard
final, que visualiza:

- predicciones
- escenarios
- ocupación futura
- periodos críticos
- sensibilidad por canal
- estacionalidad futura

Esta fase completa la parte predictiva del TFG y conecta de forma directa el modelo
con la toma de decisiones en un entorno real de Revenue Management hotelero.

> En los escenarios WHAT‑IF del forecast no se altera la demanda real del mercado.
> Los valores modificados (`rn_*`) representan decisiones de **oferta controladas
> por el hotel**, como la asignación de cupos, la priorización de canales o
> estrategias estacionales. Estas acciones son habituales en Revenue Management y
> permiten estimar cómo podría variar la ocupación ante cambios realistas en la
> distribución, sin violar la causalidad ni inventar información futura. Por tanto,
> los escenarios utilizados son **válidos, realistas y defendibles**, ya que modelan
> decisiones estratégicas que el hotel sí puede tomar, y no suposiciones arbitrarias
> sobre el comportamiento de la demanda.
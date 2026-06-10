# Fase de Peak/Season Intelligence del Proyecto

En esta fase realizo un análisis complementario al forecasting cuyo objetivo es entender por qué un hotel alcanza sus picos máximos de ocupación, qué eventos o temporadas los explican, y qué ocurre en la fecha equivalente del año siguiente, tanto en forecast como en datos reales.

Mientras que la fase de forecasting me permitió proyectar el futuro, esta fase tiene una intención diferente:

> explicar, contextualizar y comparar los máximos y mínimos históricos de cada hotel, para saber si son estructurales, estacionales o provocados por eventos puntuales.

Este análisis es clave para negocio porque responde a preguntas como:

- "¿Este pico tan alto del año pasado volverá a repetirse?"
- "¿Qué causó realmente esta subida de ocupación?"
- "¿Es un pico estructural o un evento puntual?"
- "¿Qué riesgo tengo de caída en la misma fecha del año siguiente?"
- "¿Qué temporadas son realmente las más importantes para cada hotel?"

Para ello he desarrollado tres notebooks, uno por hotel, ya que cada establecimiento tiene una lógica completamente distinta, especialmente entre el hotel urbano (Hotel 1) y los hoteles vacacionales (Hotel 2 y Hotel 3).

---

## 1. Notebook Peak Intelligence – Hotel 1

### Objetivo

Identificar y explicar los 10 picos reales más altos del Hotel 1, un hotel urbano cuyo comportamiento no es estacional, sino evento-dependiente.

### ¿Qué hago en este notebook?

- Cargo la serie histórica del Hotel 1.
- Detecto los 10 picos más altos de ocupación.
- Para cada pico:
  - investigo qué evento ocurrió ese día en la ciudad,
  - documento la evidencia,
  - clasifico el tipo de evento (festival, carnaval, cine, navidad, etc.).
- Calculo la fecha equivalente +1 año y +2 años.
- Recupero el dato real observado para esas fechas cuando el histórico lo permite.
- Comparo pico histórico, real +1 año y real +2 años.
- Mido deltas y clasifico persistencia del pico (consolidado, debilitado, pendiente).
- Genero una gráfica final donde se ve claramente cómo desaparecen los picos si no se repite el evento.

### ¿Qué demuestro?

- El Hotel 1 no tiene estacionalidad anual, sino dependencias de eventos.
- Todos los picos desaparecen el año siguiente si no hay evento equivalente.
- Esto confirma que el Hotel 1 es un hotel urbano, sensible a shocks culturales y festivos, no a la estacionalidad turística.

---

## 2. Notebook Season Intelligence – Hotel 2

### Objetivo

Identificar temporadas completas de picos y valles en el Hotel 2, un hotel vacacional fuertemente estacional, y entender cómo esas temporadas se proyectan en el año siguiente.

A diferencia del Hotel 1, aquí no analizo días concretos, sino periodos homogéneos.

### ¿Qué hago en este notebook?

- Analizo la serie temporal del Hotel 2: descomposición estacional y curvas YOY.
- Detecto patrones repetitivos cada año.
- Suavizo la serie y calculo la tendencia para segmentarla en periodos (regímenes).
- Clasifico cada periodo como subida pronunciada (**PEAK_BUILDUP**) o bajada pronunciada (**VALLEY_DROP**).
- Calculo la fecha representativa (`mid_date`) de cada temporada.
- Identifico el máximo y mínimo anual sobre la serie suavizada.
- Genero la gráfica final de Season Intelligence, donde se visualizan los tramos de subida y bajada estructural junto a los máximos y mínimos anuales.

### ¿Qué demuestro?

- El Hotel 2 es un hotel vacacional puro con patrones hiperrepetitivos.
- Picos recurrentes en temporada alta (invierno, primavera) y valles en mayo–junio.
- Los máximos anuales se sitúan de forma consistente en niveles muy elevados (~82–85%).
- Este hotel es extremadamente estable y predecible en su comportamiento estacional.

---

## 3. Notebook Season Intelligence – Hotel 3

### Objetivo

Realizar el mismo análisis estacional que en el Hotel 2, pero adaptado al perfil propio del Hotel 3, que presenta un comportamiento vacacional/mixto con mayor variabilidad interanual.

### ¿Qué hago en este notebook?

- Analizo estacionalidad mediante descomposición, curvas YOY, suavizado y segmentación.
- Detecto periodos **PEAK_BUILDUP** y **VALLEY_DROP** mediante cuantiles.
- Identifico máximos y mínimos anuales sobre la serie suavizada.
- Construyo la gráfica final con la serie histórica suavizada, los tramos estructurales y los puntos de inflexión anuales.

### ¿Qué demuestro?

- El Hotel 3 es vacacional pero con mayor volatilidad que el Hotel 2:
  - sus picos son más moderados,
  - sus valles menos profundos,
  - y sus recuperaciones más fragmentadas y graduales.
- La estacionalidad existe, pero con menor amplitud y mayor variabilidad entre ejercicios.
- Las fases de recuperación aparecen en múltiples tramos consecutivos, especialmente en 2025.

---

## Conclusión de la Fase de Peak/Season Intelligence

En esta fase no solo identifico dónde están los picos y valles de ocupación de cada hotel, sino por qué suceden y qué ocurre al año siguiente, lo cual añade una capa de inteligencia temporal esencial para la toma de decisiones.

Gracias a estos notebooks he demostrado que:

### Hotel 1 → Peak Intelligence por eventos

- No es estacional.
- Sus picos dependen de eventos locales verificables.
- Riesgo alto de caída si no se repiten los eventos.
- La planificación comercial debe apoyarse en inteligencia contextual, no en patrones históricos asumidos.

### Hotel 2 → Season Intelligence vacacional profundo

- Patrones hiperrepetitivos y altamente predecibles.
- Picos estacionales muy marcados; valles muy profundos en mayo–junio.
- Máximos anuales consistentemente por encima del 80%.
- Comportamiento ideal para modelos de forecasting basados en estacionalidad.

### Hotel 3 → Season Intelligence vacacional moderado

- Picos más suaves y valles menos pronunciados que el Hotel 2.
- Estacionalidad firme pero con mayor variabilidad interanual.
- Recuperaciones más fragmentadas y graduales.
- Requiere una gestión comercial más flexible que un hotel puramente vacacional.

---

## ¿Para qué sirve esta fase del proyecto?

- Para entender la verdadera dinámica temporal de cada hotel.
- Para saber si un pico es estructural o un accidente por evento.
- Para anticipar en qué periodos se espera crecimiento, caída, estabilidad u oportunidad comercial.
- Para integrar esta información en dashboards y en decisiones de pricing, staffing, revenue, marketing y operaciones.
# Pipeline de Preprocesamiento – Directorio `src`

Este directorio contiene toda la lógica de preprocesamiento del proyecto,
separada de los notebooks exploratorios.

El objetivo es construir un pipeline **simple, causal y sin sobreajuste**,
que genere un dataset fiable para modelar la tasa de ocupación hotelera.

- **Notebooks:** orquestan, validan y visualizan
- **`src/`:** implementa la lógica reutilizable

---

## Filosofía del pipeline

El pipeline se define con un objetivo claro:

- evitar cualquier variable que introduzca **fuga de información**
- eliminar estructuras que inducían **sobreajuste**
- utilizar únicamente señales **causales**, **observables en tiempo real**
  y **coherentes con el negocio hotelero**

Este enfoque prioriza **robustez y explicabilidad** frente a complejidad
innecesaria.

---

## Variables eliminadas

El pipeline final **no incluye** las siguientes variables durante el modelado:

- variables temporales de alta cardinalidad:
  - `dayofyear`, `weekofyear`, `dow`
- lags y medias móviles del target:
  - `ocup_total_lag*`, `mm*`
- lags, shares y medias de canales:
  - `rn_*_lag*`, `rn_*_mm*`, `share_*`
- agregados artificiales:
  - `rn_total_canal`
- variables derivadas del target:
  - `roomnights`, `neto`, `stock`, `adr`
- dummies no causales:
  - `post_2026`

Estas variables se mantienen únicamente en fases de **EDA**, **nunca durante
el entrenamiento del modelo**.

---

## Variables priorizadas

### 1. Calendario básico

- `is_weekend`

Variable binaria: 1 si el día es sábado o domingo, 0 en caso contrario.
Observable con antelación e interpretación directa en demanda turística.

---

### 2. Estacionalidad categórica

- `season` ∈ {`winter`, `spring`, `summer`, `autumn`}

Estacionalidad estable y alineada con el negocio. Se evita el uso de
estacionales continuas para reducir sobreajuste.

---

### 3. Volumen real diario por canal (formato *wide*)

- `rn_WEL`, `rn_B`, `rn_J`, `rn_T`, ...

Cada variable `rn_*` representa el número de habitaciones ocupadas ese día
procedentes de un canal concreto. Describen el **mix de demanda diario del
hotel**: no solo cuánta ocupación hay, sino **de dónde proviene**.

No se utilizan shares, lags ni derivados del target para preservar causalidad.

---

## Módulos del directorio `src`

### `loaders.py` — Carga de datos

**read_parquet_hotel**
- normaliza columnas, convierte fecha, ordena por hotel y fecha.
- Salida: `fecha`, `hotel`, `ocup_total`

**read_parquet_ttoo**
- limpia columnas, convierte tipos, ordena temporalmente.
- Salida: `fecha`, `hotel`, `canal`, `roomnights`

---

### `features_time.py` — Features temporales

**add_calendar_features**
- genera `is_weekend`.
- No genera `dayofyear`, `weekofyear`, `dow` ni `post_2026`.

**add_season_feature**
- genera `season` ∈ {winter, spring, summer, autumn}.

---

### `features_hotel.py` — Features del hotel

**build_hotel_features**
- genera el dataset base con `ocup_total`, `is_weekend` y `season`.
- No incluye ADR, roomnights, stock, lags ni medias móviles.

---

### `features_ttoo.py` — Features de canales

**pivot_ttoo_volumes_all**
- convierte el dataset de canales a formato *wide*: `rn_{canal}`.
- No incluye shares, lags, medias ni agregados artificiales.

---

### `assemble.py` — Ensamblado final

**make_hotel_ttoo_datasets**
- ensambla el dataset final por hotel integrando:
  - `fecha`
  - `ocup_total`
  - `is_weekend`
  - `season`
  - `rn_{canal}` por cada canal activo

- Output: `data/features/hotel_ttoo/{HOTEL_1|HOTEL_2|HOTEL_3}.parquet`

---

## Qué garantiza este pipeline

### Causalidad real
No se utiliza información futura ni derivada de la variable objetivo.

### Robustez del modelado
Menor número de variables → menor riesgo de sobreajuste.

### Interpretación clara
Cada variable tiene una interpretación directa en el negocio.

### Coherencia con el dominio hotelero
La ocupación se explica únicamente por calendario, estacionalidad y
volumen real por canal.

---

## Conclusión

El pipeline genera un único dataset por hotel, simple, causal, robusto e
interpretable, que constituye la base para un modelado fiable y un forecast
realista con verdadero valor aplicado.
# Mapa GIS - Delimitación de Veredas y Corredor del Cacao (Tumaco, Nariño)

Sistema de Información Geográfica (GIS) web e interactivo para la delimitación, medición y visualización de las veredas y sectores rurales del corredor cacaotero en el municipio de **San Andrés de Tumaco**, Nariño, Colombia.

El visor funciona directamente en cualquier navegador web moderno sin requerir software instalado (como ArcGIS o QGIS) y permite exportar todas las capas en formatos estándar (**GeoJSON**, **KML / Google Earth**, y **CSV / Excel**).

---

## Veredas y Sectores Delimitados

Las veredas se encuentran ordenadas consecutivamente a lo largo de la **Vía Nacional 10 (Vía al Mar)** y la cuenca del **Río Caunapí**, cotejadas con la cartografía oficial del **Instituto Geográfico Agustín Codazzi (IGAC)** y el **DANE**:

1. **La Ñupa / Porvenir (Km 52):** Consejo Comunitario La Ñupa - Río Caunapí, cuenca media y quebradas Yepes/Yuyero.
2. **Pulgande (Km 54):** Caserío Pulgande, contiguo a La Ñupa y La Variante.
3. **Kilómetro 58 (Km 58):** Caserío Km 58, sector Gualtal e I.E. San José de Caunapí (Sede Cristo Rey).
4. **Caunapí (Km 60):** Centro Poblado Caunapí y puente sobre el Río Caunapí.
5. **El Carmen (Km 63):** Sede Educativa El Carmen Km 63 y sector Vuelta del Carmen.
6. **Chinguirito:** Cuenca de la Quebrada Chinguirito y Quebrada Pianulpí hacia el Río Mira (Resguardo Indígena Awá Chinguirito Mira).

---

## Características de la Herramienta GIS

- **Capas Base Satelitales:**
  - Esri World Imagery (Imágenes de satélite de alta resolución con etiquetas de vías y centros poblados).
  - OpenStreetMap (Red vial e hidrografía detallada).
  - OpenTopoMap (Relieve y curvas de nivel).
- **Capa Oficial de Referencia:**
  - Capa oficial descargada del servidor **IGAC** (código DIVIPOLA `52835`), mostrando los límites de los Corregimientos y Corredores territoriales oficiales (*Corredor Espriella*, *Corredor Llorente*, *Pueblo Awá*).
- **Herramientas de Dibujo y Edición (Leaflet-Geoman):**
  - Trazado de polígonos libres, rectángulos, líneas y marcadores de puntos.
  - Edición en caliente de vértices, corte y reubicación de linderos.
- **Cálculos Geodésicos Automáticos (Turf.js):**
  - Cálculo instantáneo de **Área en Hectáreas (ha)**, **km²** y **m²**.
  - Cálculo de **Perímetro en Kilómetros (km)** y **metros (m)**.
- **Exportación Estándar:**
  - **GeoJSON:** 100% compatible con ArcGIS Pro, ArcGIS Online y QGIS.
  - **KML:** Para visualización tridimensional en Google Earth (Web y Desktop).
  - **CSV / Excel:** Tabla con nombres, hectáreas, perímetros y atributos.

---

## ¿Cómo ejecutar el proyecto?

1. **Visualización Directa:**  
   Haz doble clic sobre `index.html` o sobre `abrir_mapa.bat`. Se abrirá al instante en tu navegador predeterminado.
2. **Servidor Local (Python):**  
   Haz doble clic en `iniciar_servidor_python.bat` o ejecuta:
   ```bash
   python servidor_local.py
   ```
   Y abre `http://localhost:8000/index.html` en tu navegador.

---

## Estructura de Archivos

- `index.html`: Aplicación web GIS interactiva completa.
- `zonas_tumaco_veredas.geojson`: Capa vectorial con las 6 veredas delimitadas y el límite municipal de Tumaco.
- `igac_tumaco_simplificado.geojson`: Capa oficial de referencia territorial del IGAC (código 52835).
- `veredas_tumaco_oficiales_igac.geojson`: Dataset completo oficial del IGAC.
- `tumaco_municipio.geojson`: Límite perimetral completo del Distrito de San Andrés de Tumaco.
- `abrir_mapa.bat`: Lanzador rápido para Windows.
- `servidor_local.py`: Servidor HTTP ligero en Python.

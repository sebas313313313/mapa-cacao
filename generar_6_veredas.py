import json

# Cargar el límite oficial de Tumaco
with open('tumaco_municipio.geojson', encoding='utf-8') as f:
    tumaco_raw = json.load(f)

tumaco_geom = tumaco_raw['geojson']

# Definición de polígonos contiguos según la toponimia y cartografía IGAC del corredor vial y cuencas:

# 1. La Ñupa / Porvenir (Km 50 a Km 53)
# Centro: 1.4444, -78.6333
poly_la_nupa = [
    [-78.6550, 1.4650],
    [-78.6350, 1.4720],
    [-78.6240, 1.4620],
    [-78.6250, 1.4470],
    [-78.6290, 1.4380], # Límite compartido con Pulgande
    [-78.6410, 1.4320], # Límite sur sobre el río Caunapí
    [-78.6580, 1.4420],
    [-78.6550, 1.4650]
]

# 2. Pulgande (Km 53 a Km 56)
# Centro: 1.4361, -78.6249
poly_pulgande = [
    [-78.6240, 1.4620],
    [-78.6100, 1.4550],
    [-78.6050, 1.4350],
    [-78.6080, 1.4230], # Límite compartido con Km 58
    [-78.6240, 1.4210],
    [-78.6410, 1.4320], # Límite sur
    [-78.6290, 1.4380], # Límite compartido con La Ñupa
    [-78.6250, 1.4470],
    [-78.6240, 1.4620]
]

# 3. Kilómetro 58 (Km 56 a Km 59, incluye Gualtal)
# Centro: 1.4123, -78.5870
poly_km58 = [
    [-78.6100, 1.4550],
    [-78.5880, 1.4450],
    [-78.5780, 1.4250],
    [-78.5810, 1.4080], # Límite compartido con Caunapí
    [-78.5950, 1.4020],
    [-78.6080, 1.4230], # Límite compartido con Pulgande
    [-78.6050, 1.4350],
    [-78.6100, 1.4550]
]

# 4. Caunapí - Km 60 (Km 59 a Km 61)
# Centro: 1.4024, -78.5703
poly_caunapi = [
    [-78.5880, 1.4450],
    [-78.5620, 1.4380],
    [-78.5520, 1.4150],
    [-78.5540, 1.3960], # Límite compartido con El Carmen Km 63
    [-78.5700, 1.3920],
    [-78.5810, 1.4080], # Límite compartido con Km 58
    [-78.5780, 1.4250],
    [-78.5880, 1.4450]
]

# 5. El Carmen - Km 63 (Km 61 a Km 64)
# Centro: 1.3889, -78.5367
poly_el_carmen = [
    [-78.5620, 1.4380],
    [-78.5380, 1.4250],
    [-78.5220, 1.4080],
    [-78.5250, 1.3850], # Límite hacia Llorente
    [-78.5420, 1.3820],
    [-78.5540, 1.3960], # Límite compartido con Caunapí
    [-78.5520, 1.4150],
    [-78.5620, 1.4380]
]

# 6. Chinguirito (Resguardo Chinguirito Mira - Quebrada Chinguirito hacia Río Mira)
# Centro: 1.3812, -78.5450
poly_chinguirito = [
    [-78.5700, 1.3920], # Límite norte con Caunapí
    [-78.5540, 1.3960],
    [-78.5420, 1.3820], # Límite con El Carmen
    [-78.5250, 1.3850],
    [-78.5320, 1.3650], # Hacia el Río Mira
    [-78.5600, 1.3600],
    [-78.5850, 1.3680],
    [-78.5800, 1.3850],
    [-78.5700, 1.3920]
]

features = [
    # Límite general de Tumaco
    {
        "type": "Feature",
        "properties": {
            "id": "zona_municipio_tumaco",
            "nombre": "Distrito de Tumaco (Límite Municipal)",
            "categoria": "Límite Municipal",
            "color": "#e11d48",
            "weight": 2.5,
            "dashArray": "6, 6",
            "fillOpacity": 0.03,
            "municipio": "San Andrés de Tumaco",
            "departamento": "Nariño",
            "divipola": "52835",
            "notas": "Límite oficial del Distrito de San Andrés de Tumaco (IGAC / DANE)."
        },
        "geometry": tumaco_geom
    },

    # Vereda 1: La Ñupa / Porvenir
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_la_nupa_porvenir",
            "nombre": "Vereda La Ñupa / Porvenir (Km 52)",
            "categoria": "Vereda / Consejo Comunitario",
            "color": "#ea580c", # Naranja intenso
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Corredor vía al mar Km 50-53. Sector La Ñupa y caserío El Porvenir. Consejo Comunitario La Ñupa - Río Caunapí."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_la_nupa] }
    },

    # Vereda 2: Pulgande
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_pulgande",
            "nombre": "Vereda Pulgande",
            "categoria": "Vereda",
            "color": "#9333ea", # Morado
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Corredor vía al mar Km 53-56. Caserío Pulgande, colindante con La Ñupa y La Variante."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_pulgande] }
    },

    # Vereda 3: Kilómetro 58
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_km58",
            "nombre": "Vereda Kilómetro 58",
            "categoria": "Vereda",
            "color": "#0284c7", # Azul celeste
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Corredor vial Km 56-59. Incluye caserío Kilómetro 58, sector Gualtal e I.E. San José de Caunapí Sede Cristo Rey."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_km58] }
    },

    # Vereda 4: Caunapí - Km 60
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_caunapi_km60",
            "nombre": "Vereda Caunapí - Km 60",
            "categoria": "Vereda / Centro Poblado",
            "color": "#2563eb", # Azul real
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Centro Poblado Caunapí y puente sobre el Río Caunapí. Corredor vial Km 59-61."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_caunapi] }
    },

    # Vereda 5: El Carmen - Km 63
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_el_carmen_km63",
            "nombre": "Vereda El Carmen - Km 63",
            "categoria": "Vereda",
            "color": "#0d9488", # Verde azulado / Teal
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Corredor vial Km 62-64. Sede Educativa El Carmen Km 63, Vuelta del Carmen y cuenca media del Río Caunapí."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_el_carmen] }
    },

    # Vereda 6: Chinguirito
    {
        "type": "Feature",
        "properties": {
            "id": "vereda_chinguirito",
            "nombre": "Vereda / Resguardo Chinguirito",
            "categoria": "Resguardo Indígena / Vereda",
            "color": "#16a34a", # Verde bosque
            "weight": 2.5,
            "fillOpacity": 0.35,
            "municipio": "Tumaco",
            "notas": "Sector Quebrada Chinguirito y Quebrada Pianulpí hacia el Río Mira. Resguardo Awá Chinguirito Mira."
        },
        "geometry": { "type": "Polygon", "coordinates": [poly_chinguirito] }
    }
]

# Marcadores de hitos oficiales (puntos IGAC/DANE)
hitos = [
    {
        "nombre": "La Ñupa / Porvenir (Km 52)",
        "coords": [-78.6333434, 1.4443899],
        "color": "#ea580c",
        "categoria": "Punto de Referencia",
        "notas": "Caserío La Ñupa / Porvenir - Km 52"
    },
    {
        "nombre": "Caserío Pulgande",
        "coords": [-78.6248715, 1.4360607],
        "color": "#9333ea",
        "categoria": "Punto de Referencia",
        "notas": "Caserío Pulgande - Km 54"
    },
    {
        "nombre": "Caserío Kilómetro 58",
        "coords": [-78.5870283, 1.4122997],
        "color": "#0284c7",
        "categoria": "Punto de Referencia",
        "notas": "Hito Km 58 / Gualtal"
    },
    {
        "nombre": "Centro Poblado Caunapí (Km 60)",
        "coords": [-78.5703372, 1.4023856],
        "color": "#2563eb",
        "categoria": "Punto de Referencia",
        "notas": "Centro Poblado Caunapí - Puente Río Caunapí"
    },
    {
        "nombre": "El Carmen - Km 63",
        "coords": [-78.5366670, 1.3888890],
        "color": "#0d9488",
        "categoria": "Punto de Referencia",
        "notas": "Sede Escolar El Carmen Km 63"
    },
    {
        "nombre": "Quebrada Chinguirito",
        "coords": [-78.5324317, 1.3811667],
        "color": "#16a34a",
        "categoria": "Punto de Referencia",
        "notas": "Desembocadura Quebrada Chinguirito"
    }
]

for h in hitos:
    features.append({
        "type": "Feature",
        "properties": {
            "id": "hito_" + h["nombre"].lower().replace(" ", "_").replace("/", "_").replace("-", "_"),
            "nombre": h["nombre"],
            "categoria": h["categoria"],
            "color": h["color"],
            "notas": h["notas"]
        },
        "geometry": {
            "type": "Point",
            "coordinates": h["coords"]
        }
    })

geojson_collection = {
    "type": "FeatureCollection",
    "name": "Tumaco_6_Veredas_Corredor",
    "features": features
}

with open("zonas_tumaco_veredas.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson_collection, f, ensure_ascii=False, indent=2)

print("zonas_tumaco_veredas.geojson regenerado con las 6 veredas ordenadas contiguas y sus hitos!")


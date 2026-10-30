import json
import math

def point_line_distance(point, start, end):
    if start == end:
        return math.hypot(point[0] - start[0], point[1] - start[1])
    n = abs((end[1] - start[1]) * point[0] - (end[0] - start[0]) * point[1] + end[0] * start[1] - end[1] * start[0])
    d = math.hypot(end[1] - start[1], end[0] - start[0])
    return n / d

def douglas_peucker(points, tolerance):
    if len(points) <= 2:
        return points
    dmax = 0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax > tolerance:
        left = douglas_peucker(points[:index + 1], tolerance)
        right = douglas_peucker(points[index:], tolerance)
        return left[:-1] + right
    else:
        return [points[0], points[-1]]

def simplify_geom(geom, tolerance=0.001):
    gtype = geom['type']
    coords = geom['coordinates']
    if gtype == 'Polygon':
        new_coords = [douglas_peucker(ring, tolerance) for ring in coords]
        return {'type': 'Polygon', 'coordinates': new_coords}
    elif gtype == 'MultiPolygon':
        new_coords = [[douglas_peucker(ring, tolerance) for ring in poly] for poly in coords]
        return {'type': 'MultiPolygon', 'coordinates': new_coords}
    return geom

with open('veredas_tumaco_oficiales_igac.geojson', encoding='utf-8') as f:
    data = json.load(f)

simplified_features = []
for feat in data['features']:
    props = feat['properties']
    geom = simplify_geom(feat['geometry'], tolerance=0.0006)
    simplified_features.append({
        'type': 'Feature',
        'properties': {
            'nombre': props.get('NOMBRE_VER'),
            'codigo': props.get('CODIGO_VER'),
            'fuente': props.get('FUENTE'),
            'area_ha': props.get('AREA_HA'),
            'tipo': 'Corregimiento / Sector Oficial IGAC'
        },
        'geometry': geom
    })

simplified_data = {
    'type': 'FeatureCollection',
    'name': 'Corregimientos_Oficiales_IGAC_Tumaco',
    'features': simplified_features
}

with open('igac_tumaco_simplificado.geojson', 'w', encoding='utf-8') as f:
    json.dump(simplified_data, f, ensure_ascii=False)

print("Archivo simplificado con éxito!")


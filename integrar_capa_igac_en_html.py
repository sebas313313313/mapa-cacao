import json

with open("zonas_tumaco_veredas.geojson", encoding="utf-8") as f:
    veredas_data = json.load(f)

with open("igac_tumaco_simplificado.geojson", encoding="utf-8") as f:
    igac_data = json.load(f)

veredas_str = json.dumps(veredas_data)
igac_str = json.dumps(igac_data)

html_template = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>GIS Tumaco - Verificación Oficial Agustín Codazzi (IGAC)</title>
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
  <!-- Leaflet-Geoman CSS -->
  <link rel="stylesheet" href="https://unpkg.com/@geoman-io/leaflet-geoman-free@2.14.2/dist/leaflet-geoman.css" />
  <!-- FontAwesome Icons -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  
  <style>
    :root {
      --primary: #1e40af;
      --primary-hover: #1d4ed8;
      --accent: #10b981;
      --accent-hover: #059669;
      --dark: #0f172a;
      --panel-bg: rgba(255, 255, 255, 0.96);
      --border-color: #e2e8f0;
      --text-main: #1e293b;
      --text-muted: #64748b;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body, html {
      height: 100%;
      width: 100%;
      overflow: hidden;
      color: var(--text-main);
    }

    #app-container {
      display: flex;
      height: 100%;
      width: 100%;
      position: relative;
    }

    #map {
      flex: 1;
      height: 100%;
      width: 100%;
      z-index: 1;
      background-color: #cad2d3;
    }

    /* Barra Superior */
    #top-bar {
      position: absolute;
      top: 10px;
      left: 60px;
      z-index: 1000;
      background: var(--panel-bg);
      backdrop-filter: blur(8px);
      padding: 7px 12px;
      border-radius: 10px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.18);
      display: flex;
      align-items: center;
      gap: 6px;
      border: 1px solid var(--border-color);
      max-width: calc(100vw - 420px);
      flex-wrap: wrap;
    }

    .app-title {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 700;
      font-size: 13px;
      color: var(--dark);
      margin-right: 4px;
    }

    .badge-tumaco {
      background: #eff6ff;
      color: #1d4ed8;
      font-size: 10px;
      font-weight: 700;
      padding: 1px 6px;
      border-radius: 9999px;
      border: 1px solid #bfdbfe;
    }

    .nav-btn {
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      padding: 3px 8px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      color: var(--text-main);
      transition: all 0.15s;
      white-space: nowrap;
    }
    .nav-btn:hover {
      background: #f1f5f9;
      border-color: #94a3b8;
    }
    .nav-btn.primary {
      background: var(--primary);
      color: white;
      border-color: var(--primary);
    }
    .nav-btn.primary:hover {
      background: var(--primary-hover);
    }

    .btn-igac-toggle {
      background: #fefce8;
      border: 1.5px solid #eab308;
      color: #854d0e;
      font-weight: 700;
      font-size: 11px;
      padding: 3px 9px;
      border-radius: 6px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
    }
    .btn-igac-toggle.active {
      background: #ca8a04;
      color: white;
      border-color: #a16207;
    }

    /* Panel Lateral */
    #sidebar {
      position: absolute;
      top: 10px;
      right: 10px;
      bottom: 10px;
      width: 380px;
      z-index: 1000;
      background: var(--panel-bg);
      backdrop-filter: blur(10px);
      border-radius: 12px;
      box-shadow: 0 8px 30px rgba(0,0,0,0.18);
      border: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: transform 0.3s ease;
    }

    #sidebar.collapsed {
      transform: translateX(400px);
    }

    .sidebar-toggle-btn {
      position: absolute;
      top: 10px;
      right: 400px;
      z-index: 1000;
      background: white;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.12);
      transition: all 0.2s;
    }
    .sidebar-toggle-btn:hover { background: #f8fafc; }

    .sidebar-header {
      padding: 12px 14px;
      background: white;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .sidebar-header h2 {
      font-size: 14px;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .zones-count {
      background: #dbeafe;
      color: var(--primary);
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 9999px;
    }

    .sidebar-content {
      flex: 1;
      overflow-y: auto;
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }
    .metric-card {
      background: #f8fafc;
      border: 1px solid var(--border-color);
      padding: 7px 9px;
      border-radius: 8px;
    }
    .metric-label {
      font-size: 9.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .metric-value {
      font-size: 13px;
      font-weight: 700;
      color: var(--dark);
      margin-top: 1px;
    }

    .zones-list {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .zone-item {
      background: white;
      border: 1px solid var(--border-color);
      border-left: 5px solid var(--primary);
      border-radius: 7px;
      padding: 8px 10px;
      transition: all 0.15s;
    }
    .zone-item:hover {
      box-shadow: 0 3px 8px rgba(0,0,0,0.06);
      border-color: #94a3b8;
    }

    .zone-item-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 3px;
    }
    .zone-name {
      font-weight: 600;
      font-size: 12.5px;
      color: var(--dark);
    }
    .zone-type {
      font-size: 9px;
      font-weight: 600;
      padding: 1px 5px;
      border-radius: 4px;
      background: #f1f5f9;
      color: #475569;
    }

    .zone-metrics {
      display: flex;
      gap: 10px;
      font-size: 11px;
      color: var(--text-muted);
      margin: 3px 0;
    }

    .zone-actions {
      display: flex;
      gap: 5px;
      margin-top: 5px;
      border-top: 1px solid #f1f5f9;
      padding-top: 5px;
    }
    .action-btn {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 4px;
      padding: 2px 6px;
      font-size: 10.5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 4px;
      color: #334155;
    }
    .action-btn:hover { background: #e2e8f0; }

    .sidebar-footer {
      padding: 10px 12px;
      background: white;
      border-top: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .footer-btn-group {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
    }

    .btn-gis {
      background: white;
      border: 1px solid #cbd5e1;
      padding: 6px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-gis:hover { background: #f8fafc; border-color: #94a3b8; }
    .btn-gis.primary { background: var(--accent); color: white; border-color: var(--accent); }
    .btn-gis.primary:hover { background: var(--accent-hover); }

    #coordinates-bar {
      position: absolute;
      bottom: 10px;
      left: 10px;
      z-index: 1000;
      background: rgba(15, 23, 42, 0.85);
      color: #f8fafc;
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 11px;
      font-family: monospace;
      backdrop-filter: blur(4px);
    }

    /* Modal */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0,0,0,0.5);
      backdrop-filter: blur(2px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
    }
    .modal-overlay.active { display: flex; }

    .modal-content {
      background: white;
      border-radius: 12px;
      width: 420px;
      max-width: 90vw;
      box-shadow: 0 10px 40px rgba(0,0,0,0.25);
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .modal-header {
      padding: 12px 16px;
      background: #f8fafc;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .modal-header h3 { font-size: 14px; font-weight: 700; }
    .close-modal { background: none; border: none; font-size: 16px; cursor: pointer; color: var(--text-muted); }

    .modal-body {
      padding: 14px 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .form-group { display: flex; flex-direction: column; gap: 3px; }
    .form-group label { font-size: 11px; font-weight: 600; color: #475569; }
    .form-group input, .form-group select, .form-group textarea {
      padding: 6px 9px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 12.5px;
      outline: none;
    }
    .modal-footer {
      padding: 10px 16px;
      background: #f8fafc;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: flex-end;
      gap: 6px;
    }
  </style>
</head>
<body>

  <div id="app-container">
    
    <!-- Barra Superior -->
    <div id="top-bar">
      <div class="app-title">
        <i class="fa-solid fa-map-location-dot"></i>
        <span>GIS Tumaco</span>
        <span class="badge-tumaco">IGAC Oficial</span>
      </div>

      <button class="nav-btn primary" id="btnGoCorredor" title="Ver todo el corredor de las 6 veredas juntas">
        <i class="fa-solid fa-route"></i> Todo el Corredor
      </button>

      <!-- Botón especial de Verificación IGAC -->
      <button class="btn-igac-toggle active" id="btnToggleIGAC" title="Activar/Desactivar capa oficial descargada de Agustín Codazzi">
        <i class="fa-solid fa-landmark"></i> Capa Oficial IGAC
      </button>

      <!-- Veredas en orden -->
      <button class="nav-btn" id="btnGoLaNupa" style="border-left: 3px solid #ea580c;">1. La Ñupa/Porvenir</button>
      <button class="nav-btn" id="btnGoPulgande" style="border-left: 3px solid #9333ea;">2. Pulgande</button>
      <button class="nav-btn" id="btnGoKm58" style="border-left: 3px solid #0284c7;">3. Km 58</button>
      <button class="nav-btn" id="btnGoCaunapi" style="border-left: 3px solid #2563eb;">4. Caunapí (Km 60)</button>
      <button class="nav-btn" id="btnGoElCarmen" style="border-left: 3px solid #0d9488;">5. El Carmen (Km 63)</button>
      <button class="nav-btn" id="btnGoChinguirito" style="border-left: 3px solid #16a34a;">6. Chinguirito</button>
    </div>

    <!-- Toggle Sidebar -->
    <button class="sidebar-toggle-btn" id="sidebarToggleBtn" title="Mostrar/Ocultar Panel">
      <i class="fa-solid fa-bars"></i>
    </button>

    <!-- Panel Lateral -->
    <div id="sidebar">
      <div class="sidebar-header">
        <h2><i class="fa-solid fa-layer-group text-primary"></i> Veredas Delimitadas</h2>
        <span class="zones-count" id="zonesCounter">6 veredas</span>
      </div>

      <div class="sidebar-content">
        <div class="summary-grid">
          <div class="metric-card">
            <div class="metric-label">Veredas Delimitadas</div>
            <div class="metric-value">6 sectores</div>
          </div>
          <div class="metric-card">
            <div class="metric-label">Área del Corredor</div>
            <div class="metric-value" id="totalVeredasAreaVal">0 ha</div>
          </div>
        </div>

        <div class="zones-list" id="zonesList"></div>
      </div>

      <!-- Pie de página con Exportar / Importar GIS -->
      <div class="sidebar-footer">
        <div class="footer-btn-group">
          <button class="btn-gis primary" id="btnExportGeoJSON" title="Descargar GeoJSON para ArcGIS y QGIS">
            <i class="fa-solid fa-download"></i> GeoJSON
          </button>
          <button class="btn-gis" id="btnExportKML" title="Descargar KML para Google Earth">
            <i class="fa-solid fa-globe"></i> KML Earth
          </button>
        </div>

        <div class="footer-btn-group">
          <button class="btn-gis" id="btnExportCSV" title="Exportar tabla a Excel">
            <i class="fa-solid fa-file-csv"></i> Tabla CSV
          </button>
          <label class="btn-gis" style="cursor: pointer;" title="Cargar archivo GeoJSON">
            <i class="fa-solid fa-upload"></i> Importar
            <input type="file" id="importFileInput" accept=".geojson,.json,.kml" style="display:none;" />
          </label>
        </div>
      </div>
    </div>

    <!-- Mapa -->
    <div id="map"></div>

    <div id="coordinates-bar">
      Lat: <span id="mouseLat">1.4000</span> | Lon: <span id="mouseLng">-78.5800</span>
    </div>

  </div>

  <!-- Modal de Edición -->
  <div class="modal-overlay" id="zoneModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modalTitle"><i class="fa-solid fa-pen-to-square"></i> Detalle de Vereda</h3>
        <button class="close-modal" id="modalCloseBtn">&times;</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="zoneNameInput">Nombre:</label>
          <input type="text" id="zoneNameInput" />
        </div>
        <div class="form-group">
          <label for="zoneNotesInput">Notas / Linderos:</label>
          <textarea id="zoneNotesInput" rows="2"></textarea>
        </div>
        <div class="summary-grid" style="background: #f1f5f9; padding: 7px; border-radius: 7px;">
          <div>
            <span style="font-size: 10px; color: #64748b; font-weight: 600;">ÁREA CALCULADA:</span>
            <div id="modalAreaDisplay" style="font-size: 12.5px; font-weight: 700; color: #1e293b;">0 ha</div>
          </div>
          <div>
            <span style="font-size: 10px; color: #64748b; font-weight: 600;">PERÍMETRO:</span>
            <div id="modalPerimeterDisplay" style="font-size: 12.5px; font-weight: 700; color: #1e293b;">0 km</div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="nav-btn" id="modalCancelBtn">Cancelar</button>
        <button class="nav-btn primary" id="modalSaveBtn"><i class="fa-solid fa-check"></i> Guardar</button>
      </div>
    </div>
  </div>

  <!-- Leaflet & GIS Scripts -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  <script src="https://unpkg.com/@geoman-io/leaflet-geoman-free@2.14.2/dist/leaflet-geoman.min.js"></script>
  <script src="https://unpkg.com/@turf/turf@6.5.0/turf.min.js"></script>

  <script>
    // DATOS DE LAS 6 VEREDAS Y CAPA OFICIAL IGAC
    const INITIAL_VEREDAS_DATA = __INITIAL_VEREDAS_DATA__;
    const INITIAL_IGAC_DATA = __INITIAL_IGAC_DATA__;

    // CAPAS BASE
    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Esri Satellite'
    });
    const esriLabels = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Esri Labels'
    });
    const esriHybrid = L.layerGroup([esriSatellite, esriLabels]);

    const osmStandard = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19, attribution: '&copy; OpenStreetMap'
    });
    const openTopo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
      maxZoom: 17, attribution: 'OpenTopoMap'
    });

    const map = L.map('map', {
      center: [1.415, -78.580],
      zoom: 12,
      layers: [esriHybrid]
    });

    // GRUPOS DE CAPAS
    let igacLayerGroup = L.layerGroup().addTo(map);
    let veredasLayerGroup = L.layerGroup().addTo(map);

    const baseLayers = {
      "Satélite Esri (Híbrido)": esriHybrid,
      "Satélite Esri (Puro)": esriSatellite,
      "OpenStreetMap (Vías)": osmStandard,
      "Topografía (Curvas)": openTopo
    };

    const overlayLayers = {
      "<span style='color:#ca8a04; font-weight:bold;'>🏛️ Capa Oficial IGAC</span>": igacLayerGroup,
      "<span style='color:#2563eb; font-weight:bold;'>📍 Nuestras 6 Veredas</span>": veredasLayerGroup
    };

    L.control.layers(baseLayers, overlayLayers, { position: 'topright' }).addTo(map);
    L.control.scale({ imperial: false, metric: true, position: 'bottomleft' }).addTo(map);

    // DIBUJO GEOMAN
    map.pm.addControls({
      position: 'topleft',
      drawCircleMarker: false,
      drawCircle: false,
      drawPolyline: true,
      drawRectangle: true,
      drawPolygon: true,
      drawMarker: true,
      editMode: true,
      dragMode: true,
      cutPolygon: true,
      removalMode: true
    });
    map.pm.setLang('es');

    let zones = [];
    let currentEditingLayer = null;

    // 1. Cargar Capa Oficial Agustín Codazzi (IGAC)
    function loadIGACLayer() {
      L.geoJSON(INITIAL_IGAC_DATA, {
        style: function(feature) {
          return {
            color: '#eab308', // Dorado / Amarillo IGAC
            weight: 2,
            dashArray: '5, 5',
            fillColor: '#fef08a',
            fillOpacity: 0.12
          };
        },
        onEachFeature: function(feature, layer) {
          const props = feature.properties || {};
          layer.bindTooltip(`<b>🏛️ LÍMITE OFICIAL IGAC</b><br><b>${props.nombre}</b><br>Área: ${Math.round(props.area_ha || 0).toLocaleString()} ha`, { sticky: true });
        }
      }).addTo(igacLayerGroup);
    }

    // 2. Cargar Nuestras 6 Veredas
    function loadVeredasLayer() {
      L.geoJSON(INITIAL_VEREDAS_DATA, {
        style: function(feature) {
          const p = feature.properties || {};
          return {
            color: p.color || '#2563eb',
            weight: p.weight || 2.5,
            fillColor: p.color || '#2563eb',
            fillOpacity: p.fillOpacity !== undefined ? p.fillOpacity : 0.35,
            dashArray: p.dashArray || null
          };
        },
        pointToLayer: function(feature, latlng) {
          const p = feature.properties || {};
          return L.circleMarker(latlng, {
            radius: 5,
            fillColor: p.color || '#2563eb',
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillOpacity: 0.95
          });
        },
        onEachFeature: function(feature, layer) {
          const props = feature.properties || {};
          const id = props.id || 'zona_' + Date.now();
          layer._zoneId = id;
          layer.addTo(veredasLayerGroup);

          const measures = calculateLayerMeasurements(layer);
          const zoneObj = {
            id: id,
            name: props.nombre || 'Zona',
            category: props.categoria || 'Vereda',
            notes: props.notas || '',
            color: props.color || '#2563eb',
            layer: layer,
            areaHa: measures.areaHa,
            perimeterKm: measures.perimeterKm
          };

          zones.push(zoneObj);
          updateLayerTooltip(layer, zoneObj);

          layer.on('click', () => openEditZoneModal(zoneObj));
          layer.on('pm:edit', () => {
            const updated = calculateLayerMeasurements(layer);
            zoneObj.areaHa = updated.areaHa;
            zoneObj.perimeterKm = updated.perimeterKm;
            updateSidebar();
            updateLayerTooltip(layer, zoneObj);
          });
        }
      });

      updateSidebar();
      zoomToCorredor();
    }

    function calculateLayerMeasurements(layer) {
      try {
        const geojson = layer.toGeoJSON();
        let areaHa = 0;
        let perimeterKm = 0;

        if (geojson.geometry.type === 'Polygon' || geojson.geometry.type === 'MultiPolygon') {
          const areaSqMeters = turf.area(geojson);
          areaHa = areaSqMeters / 10000;
          perimeterKm = turf.length(geojson, { units: 'kilometers' });
        } else if (geojson.geometry.type === 'LineString') {
          perimeterKm = turf.length(geojson, { units: 'kilometers' });
        }

        let areaFormatted = areaHa >= 100 
          ? (areaHa / 100).toFixed(2) + ' km² (' + areaHa.toFixed(1) + ' ha)'
          : areaHa.toFixed(2) + ' ha';

        let perimeterFormatted = perimeterKm.toFixed(2) + ' km';
        return { areaHa, perimeterKm, areaFormatted, perimeterFormatted };
      } catch (e) {
        return { areaHa: 0, perimeterKm: 0, areaFormatted: 'N/A', perimeterFormatted: 'N/A' };
      }
    }

    function updateLayerTooltip(layer, zoneData) {
      let content = `<b>${zoneData.name}</b><br><span style="color:#64748b;">${zoneData.category}</span>`;
      if (zoneData.areaHa > 0) {
        content += `<br><b>Área:</b> ${zoneData.areaHa.toFixed(1)} ha`;
      }
      if (zoneData.perimeterKm > 0) {
        content += `<br><b>Perímetro:</b> ${zoneData.perimeterKm.toFixed(1)} km`;
      }
      layer.bindTooltip(content, { sticky: true });
    }

    function updateSidebar() {
      const container = document.getElementById('zonesList');
      const counter = document.getElementById('zonesCounter');
      const totalAreaElem = document.getElementById('totalVeredasAreaVal');

      const veredasOnly = zones.filter(z => z.id.startsWith('vereda_'));
      counter.innerText = veredasOnly.length + ' veredas';

      let veredasArea = 0;
      container.innerHTML = '';

      veredasOnly.forEach((zone, idx) => {
        veredasArea += zone.areaHa || 0;

        const item = document.createElement('div');
        item.className = 'zone-item';
        item.style.borderLeftColor = zone.color;

        item.innerHTML = `
          <div class="zone-item-header">
            <span class="zone-name">${idx + 1}. ${zone.name}</span>
            <span class="zone-type">${zone.category}</span>
          </div>
          <div class="zone-metrics">
            <span><i class="fa-solid fa-chart-area"></i> ${zone.areaHa.toFixed(1)} ha</span>
            <span><i class="fa-solid fa-ruler"></i> ${zone.perimeterKm.toFixed(1)} km</span>
          </div>
          <div class="zone-actions">
            <button class="action-btn" onclick="zoomToZone('${zone.id}')"><i class="fa-solid fa-location-crosshairs"></i> Ver</button>
            <button class="action-btn" onclick="editZoneById('${zone.id}')"><i class="fa-solid fa-pen"></i> Editar</button>
          </div>
        `;
        container.appendChild(item);
      });

      totalAreaElem.innerText = veredasArea.toFixed(1) + ' ha';
    }

    function zoomToCorredor() {
      map.fitBounds([
        [1.355, -78.665],
        [1.475, -78.515]
      ], { padding: [30, 30] });
    }

    document.getElementById('btnGoCorredor').onclick = zoomToCorredor;

    // Toggle Capa Oficial IGAC
    let igacVisible = true;
    const btnToggleIGAC = document.getElementById('btnToggleIGAC');
    btnToggleIGAC.onclick = () => {
      if (igacVisible) {
        map.removeLayer(igacLayerGroup);
        igacVisible = false;
        btnToggleIGAC.classList.remove('active');
        btnToggleIGAC.innerHTML = '<i class="fa-solid fa-landmark"></i> Ver Capa IGAC (Off)';
      } else {
        map.addLayer(igacLayerGroup);
        igacVisible = true;
        btnToggleIGAC.classList.add('active');
        btnToggleIGAC.innerHTML = '<i class="fa-solid fa-landmark"></i> Capa Oficial IGAC (On)';
      }
    };

    document.getElementById('btnGoLaNupa').onclick = () => zoomToZone('vereda_la_nupa_porvenir');
    document.getElementById('btnGoPulgande').onclick = () => zoomToZone('vereda_pulgande');
    document.getElementById('btnGoKm58').onclick = () => zoomToZone('vereda_km58');
    document.getElementById('btnGoCaunapi').onclick = () => zoomToZone('vereda_caunapi_km60');
    document.getElementById('btnGoElCarmen').onclick = () => zoomToZone('vereda_el_carmen_km63');
    document.getElementById('btnGoChinguirito').onclick = () => zoomToZone('vereda_chinguirito');

    window.zoomToZone = function(id) {
      const zone = zones.find(z => z.id === id);
      if (zone && zone.layer) {
        if (zone.layer.getBounds) {
          map.fitBounds(zone.layer.getBounds(), { padding: [40, 40], maxZoom: 15 });
        } else if (zone.layer.getLatLng) {
          map.setView(zone.layer.getLatLng(), 15);
        }
      }
    };

    window.editZoneById = function(id) {
      const zone = zones.find(z => z.id === id);
      if (zone) openEditZoneModal(zone);
    };

    function openEditZoneModal(zone) {
      currentEditingLayer = zone.layer;
      document.getElementById('modalTitle').innerHTML = '<i class="fa-solid fa-pen-to-square"></i> ' + zone.name;
      document.getElementById('zoneNameInput').value = zone.name;
      document.getElementById('zoneNotesInput').value = zone.notes;

      const measures = calculateLayerMeasurements(zone.layer);
      document.getElementById('modalAreaDisplay').innerText = measures.areaFormatted;
      document.getElementById('modalPerimeterDisplay').innerText = measures.perimeterFormatted;

      document.getElementById('zoneModal').classList.add('active');
    }

    document.getElementById('modalCloseBtn').onclick = () => document.getElementById('zoneModal').classList.remove('active');
    document.getElementById('modalCancelBtn').onclick = () => document.getElementById('zoneModal').classList.remove('active');

    document.getElementById('modalSaveBtn').onclick = () => {
      if (!currentEditingLayer) return;
      const found = zones.find(z => z.id === currentEditingLayer._zoneId);
      if (found) {
        found.name = document.getElementById('zoneNameInput').value.trim() || 'Sin Nombre';
        found.notes = document.getElementById('zoneNotesInput').value.trim();
        updateLayerTooltip(currentEditingLayer, found);
        updateSidebar();
      }
      document.getElementById('zoneModal').classList.remove('active');
    };

    map.on('mousemove', (e) => {
      document.getElementById('mouseLat').innerText = e.latlng.lat.toFixed(5);
      document.getElementById('mouseLng').innerText = e.latlng.lng.toFixed(5);
    });

    // Toggle Sidebar
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('sidebarToggleBtn');
    toggleBtn.onclick = () => {
      sidebar.classList.toggle('collapsed');
      toggleBtn.style.right = sidebar.classList.contains('collapsed') ? '10px' : '400px';
    };

    // Exportar GeoJSON
    document.getElementById('btnExportGeoJSON').onclick = () => {
      const fc = {
        type: "FeatureCollection",
        name: "Delimitacion_Corredor_Tumaco_6_Veredas",
        features: zones.map(z => {
          const feat = z.layer.toGeoJSON();
          feat.properties = {
            id: z.id,
            nombre: z.name,
            categoria: z.category,
            area_ha: parseFloat(z.areaHa.toFixed(2)),
            perimetro_km: parseFloat(z.perimeterKm.toFixed(2)),
            color: z.color,
            notas: z.notes,
            municipio: "Tumaco"
          };
          return feat;
        })
      };
      downloadFile(JSON.stringify(fc, null, 2), 'delimitacion_corredor_tumaco_6_veredas.geojson', 'application/geo+json');
    };

    // Exportar KML
    document.getElementById('btnExportKML').onclick = () => {
      let kml = `<?xml version="1.0" encoding="UTF-8"?>\\n<kml xmlns="http://www.opengis.net/kml/2.2">\\n<Document>\\n<name>Corredor Tumaco - 6 Veredas</name>\\n`;
      zones.forEach(z => {
        const gj = z.layer.toGeoJSON();
        kml += `<Placemark><name><![CDATA[${z.name}]]></name><description><![CDATA[${z.category} - Área: ${z.areaHa.toFixed(1)} ha]]></description>`;
        if (gj.geometry.type === 'Polygon') {
          kml += `<Polygon><outerBoundaryIs><LinearRing><coordinates>\\n`;
          kml += gj.geometry.coordinates[0].map(c => `${c[0]},${c[1]},0`).join(' ') + `\\n</coordinates></LinearRing></outerBoundaryIs></Polygon>`;
        }
        kml += `</Placemark>\\n`;
      });
      kml += `</Document>\\n</kml>`;
      downloadFile(kml, 'delimitacion_corredor_tumaco_6_veredas.kml', 'application/vnd.google-earth.kml+xml');
    };

    // Exportar CSV
    document.getElementById('btnExportCSV').onclick = () => {
      let csv = "Numero,ID,Nombre,Categoria,Area_Hectareas,Perimetro_Km,Color,Notas\\n";
      const veredas = zones.filter(z => z.id.startsWith('vereda_'));
      veredas.forEach((z, idx) => {
        csv += `${idx + 1},"${z.id}","${z.name}","${z.category}",${z.areaHa.toFixed(2)},${z.perimeterKm.toFixed(2)},"${z.color}","${(z.notes||'').replace(/"/g, '""')}"\\n`;
      });
      downloadFile(csv, 'tabla_veredas_corredor_tumaco.csv', 'text/csv;charset=utf-8;');
    };

    function downloadFile(content, fileName, contentType) {
      const blob = new Blob([content], { type: contentType });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(a.href);
    }

    // Inicializar ambas capas
    loadIGACLayer();
    loadVeredasLayer();
  </script>
</body>
</html>
"""

final_html = html_template.replace("__INITIAL_VEREDAS_DATA__", veredas_str).replace("__INITIAL_IGAC_DATA__", igac_str)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("index.html actualizado exitosamente con la Capa Oficial IGAC integrada!")


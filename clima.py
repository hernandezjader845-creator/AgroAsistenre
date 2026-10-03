import requests
import logging
import time
import os
import json
import re

logger = logging.getLogger(__name__)

RUTA_MUNICIPIOS = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "Biblioteca_Agronomica", "municipios_nicaragua.json")
if not os.path.exists(RUTA_MUNICIPIOS):
    RUTA_MUNICIPIOS = "C:/antigravity 1/Biblioteca_Agronomica/municipios_nicaragua.json"

def normalizar_texto(texto: str) -> str:
    """Remueve tildes y caracteres especiales para búsqueda tolerante."""
    if not texto:
        return ""
    texto = texto.lower()
    for a, b in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
        texto = texto.replace(a, b)
    return texto

def cargar_catalogo_municipios():
    if os.path.exists(RUTA_MUNICIPIOS):
        try:
            with open(RUTA_MUNICIPIOS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error cargando municipios_nicaragua.json: {e}")
    return {}

CATALOGO_MUNICIPIOS = cargar_catalogo_municipios()

def obtener_departamentos() -> list:
    """Retorna la lista ordenada de los 17 departamentos y regiones autónomas."""
    return sorted(list(CATALOGO_MUNICIPIOS.keys())) if CATALOGO_MUNICIPIOS else ["Managua", "Matagalpa", "Chinandega", "León", "Rivas"]

def obtener_municipios(departamento: str) -> list:
    """Retorna la lista de municipios de un departamento dado."""
    if not CATALOGO_MUNICIPIOS or departamento not in CATALOGO_MUNICIPIOS:
        return [departamento]
    return sorted(list(CATALOGO_MUNICIPIOS[departamento].keys()))

# Generar índice plano de búsqueda de todos los 152 municipios
MAPA_BUSQUEDA_MUNICIPIOS = {}
PALABRAS_VACIAS_MUN = {'san', 'santa', 'del', 'los', 'las', 'rio', 'villa', 'puerto', 'ciudad', 'maria', 'francisco', 'jose', 'juan', 'pedro', 'de', 'la', 'el'}

for dep, muns in CATALOGO_MUNICIPIOS.items():
    for mun, coords in muns.items():
        nom_completo = f"{mun}, {dep}"
        val = (coords['lat'], coords['lon'], nom_completo)
        
        # Clave exacta normalizada
        MAPA_BUSQUEDA_MUNICIPIOS[normalizar_texto(mun)] = val
        
        # Claves de partes significativas (ej: 'pantasma', 'dalia', 'malpaisillo', 'ometepe', 'bilwi', 'cuapa')
        partes = mun.replace('(', ' ').replace(')', ' ').replace('-', ' ').replace('/', ' ').split()
        for p in partes:
            pn = normalizar_texto(p)
            if len(pn) >= 4 and pn not in PALABRAS_VACIAS_MUN:
                # No sobreescribir si ya existe una clave más específica
                if pn not in MAPA_BUSQUEDA_MUNICIPIOS:
                    MAPA_BUSQUEDA_MUNICIPIOS[pn] = val

# Diccionario de departamentos para respaldo
DEPARTAMENTOS_CENTROIDES = {
    "managua": {"lat": 12.1364, "lon": -86.2514, "nombre": "Managua"},
    "leon": {"lat": 12.4379, "lon": -86.8780, "nombre": "León"},
    "chinandega": {"lat": 12.6294, "lon": -87.1311, "nombre": "Chinandega"},
    "matagalpa": {"lat": 12.9256, "lon": -85.9175, "nombre": "Matagalpa"},
    "jinotega": {"lat": 13.0919, "lon": -86.0022, "nombre": "Jinotega"},
    "esteli": {"lat": 13.0918, "lon": -86.3538, "nombre": "Estelí"},
    "madriz": {"lat": 13.4808, "lon": -86.5821, "nombre": "Somoto, Madriz"},
    "nueva segovia": {"lat": 13.6321, "lon": -86.4752, "nombre": "Ocotal, Nueva Segovia"},
    "rivas": {"lat": 11.4372, "lon": -85.8263, "nombre": "Rivas"},
    "carazo": {"lat": 11.8500, "lon": -86.2000, "nombre": "Jinotepe, Carazo"},
    "masaya": {"lat": 11.9744, "lon": -86.0942, "nombre": "Masaya"},
    "granada": {"lat": 11.9299, "lon": -85.9560, "nombre": "Granada"},
    "boaco": {"lat": 12.4722, "lon": -85.6586, "nombre": "Boaco"},
    "chontales": {"lat": 12.1063, "lon": -85.3645, "nombre": "Juigalpa, Chontales"},
    "rio san juan": {"lat": 11.1333, "lon": -84.7833, "nombre": "San Carlos, Río San Juan"},
    "costa caribe sur": {"lat": 12.0137, "lon": -83.7635, "nombre": "Bluefields, RACCS"},
    "costa caribe norte": {"lat": 14.0351, "lon": -83.3888, "nombre": "Bilwi, RACCN"},
    "raccs": {"lat": 12.0137, "lon": -83.7635, "nombre": "Bluefields, RACCS"},
    "raccn": {"lat": 14.0351, "lon": -83.3888, "nombre": "Bilwi, RACCN"}
}

def resolver_coordenadas(texto_o_lugar: str, departamento_hint: str = None) -> tuple:
    """
    Resuelve con máxima precisión las coordenadas de cualquier municipio o departamento
    de Nicaragua a partir de una selección UI o de texto libre en el chat.
    Retorna (latitud, longitud, nombre_descriptivo).
    """
    if not texto_o_lugar:
        loc = DEPARTAMENTOS_CENTROIDES["managua"]
        return loc["lat"], loc["lon"], loc["nombre"]
        
    txt_norm = normalizar_texto(texto_o_lugar)
    
    # 1. Búsqueda directa en catálogo si se proporcionó departamento y municipio exactos
    if departamento_hint and departamento_hint in CATALOGO_MUNICIPIOS:
        muns_dep = CATALOGO_MUNICIPIOS[departamento_hint]
        if texto_o_lugar in muns_dep:
            c = muns_dep[texto_o_lugar]
            return c["lat"], c["lon"], f"{texto_o_lugar}, {departamento_hint}"
            
    # 2. Búsqueda en los 152 municipios (por longitud descendente para evitar ambigüedades)
    for k in sorted(MAPA_BUSQUEDA_MUNICIPIOS.keys(), key=len, reverse=True):
        patron = r'\b' + re.escape(k) + r'\b'
        if re.search(patron, txt_norm):
            lat, lon, nom = MAPA_BUSQUEDA_MUNICIPIOS[k]
            return lat, lon, nom

    # 3. Búsqueda por departamentos
    for dep_k, coords in DEPARTAMENTOS_CENTROIDES.items():
        if dep_k in txt_norm:
            return coords["lat"], coords["lon"], coords["nombre"]
            
    # 4. Regiones amplias
    if "costa" in txt_norm or "caribe" in txt_norm or "atlantico" in txt_norm:
        if "norte" in txt_norm:
            c = DEPARTAMENTOS_CENTROIDES["costa caribe norte"]
            return c["lat"], c["lon"], c["nombre"]
        c = DEPARTAMENTOS_CENTROIDES["costa caribe sur"]
        return c["lat"], c["lon"], c["nombre"]

    # Predeterminado: Managua
    loc = DEPARTAMENTOS_CENTROIDES["managua"]
    return loc["lat"], loc["lon"], loc["nombre"]

# Caché georreferenciada de 30 minutos (1800 s) por par de coordenadas
_cache_clima_multizona = {}

class RadarClimatico:
    def __init__(self, lat=12.1364, lon=-86.2514, nombre_lugar="Managua"):
        self.lat = lat
        self.lon = lon
        self.nombre_lugar = nombre_lugar
        
    def obtener_pronostico(self, lat=None, lon=None):
        global _cache_clima_multizona
        target_lat = lat if lat is not None else self.lat
        target_lon = lon if lon is not None else self.lon
        
        clave_cache = (round(float(target_lat), 2), round(float(target_lon), 2))
        ahora = time.time()
        
        # Verificar caché para este par de coordenadas
        if clave_cache in _cache_clima_multizona:
            cached = _cache_clima_multizona[clave_cache]
            if ahora - cached["timestamp"] < 1800:
                return cached["datos"]

        try:
            url = f"https://api.open-meteo.com/v1/forecast?latitude={target_lat}&longitude={target_lon}&hourly=precipitation_probability,precipitation,wind_speed_10m&forecast_days=1&timezone=America%2FManagua"
            response = requests.get(url, timeout=3.5)
            response.raise_for_status()
            data = response.json()
            
            probabilidades = data.get('hourly', {}).get('precipitation_probability', [])[:12]
            lluvias = data.get('hourly', {}).get('precipitation', [])[:12]
            vientos = data.get('hourly', {}).get('wind_speed_10m', [])[:12]
            
            max_prob = max(probabilidades) if probabilidades else 0
            total_lluvia = sum(lluvias) if lluvias else 0
            max_viento = max(vientos) if vientos else 0
            
            resumen = {
                "riesgo_lluvia": "ALTO" if max_prob > 60 or total_lluvia > 5 else "MEDIO" if max_prob > 30 else "BAJO",
                "probabilidad_maxima_pct": max_prob,
                "lluvia_acumulada_mm": round(total_lluvia, 1),
                "riesgo_deriva_viento": "ALTO (Peligroso para rociar)" if max_viento > 20 else "MODERADO" if max_viento > 10 else "BAJO",
                "viento_maximo_kmh": round(max_viento, 1)
            }
            
            _cache_clima_multizona[clave_cache] = {
                "datos": resumen,
                "timestamp": ahora
            }
            return resumen
        except Exception as e:
            logger.warning(f"Error obteniendo clima para ({target_lat}, {target_lon}): {e}")
            if clave_cache in _cache_clima_multizona:
                return _cache_clima_multizona[clave_cache]["datos"]
            return None

    def generar_advertencia_agronomica(self, lat=None, lon=None, nombre_lugar=None):
        target_lat = lat if lat is not None else self.lat
        target_lon = lon if lon is not None else self.lon
        lugar = nombre_lugar or self.nombre_lugar
        
        datos = self.obtener_pronostico(target_lat, target_lon)
        if not datos:
            return f"🌤️ Clima en {lugar}: Condiciones estables estimadas. Verifique el cielo local antes de aplicar."
            
        advertencia = f"📍 **{lugar}** (Pronóstico a 12h):\nLluvia esperada: **{datos['lluvia_acumulada_mm']} mm** ({datos['probabilidad_maxima_pct']}% prob). Viento máx: **{datos['viento_maximo_kmh']} km/h**.\n"
        
        recomendaciones = []
        if datos["riesgo_lluvia"] == "ALTO":
            recomendaciones.append("⚠️ RIESGO DE LAVADO: Lluvia inminente. Use productos SISTÉMICOS o aplique con adherente/surfactante siliconado.")
        elif datos["riesgo_lluvia"] == "MEDIO":
            recomendaciones.append("🌦️ RIESGO MODERADO: Asegure al menos 2-3 horas de ventana seca tras la aspersión.")
            
        if datos["riesgo_deriva_viento"] == "ALTO (Peligroso para rociar)":
            recomendaciones.append("🌬️ RIESGO DE DERIVA: Viento superior a 20 km/h. Suspenda aspersiones foliares o use boquilla antideriva con gota gruesa.")
        elif datos["riesgo_deriva_viento"] == "MODERADO":
            recomendaciones.append("🍃 Viento moderado: Aspersión recomendada en horas tempranas de la mañana.")
            
        if recomendaciones:
            advertencia += "\n" + "\n".join(recomendaciones)
        else:
            advertencia += "✅ Ventana favorable para aspersión fitosanitaria y fertilización foliar."
            
        return advertencia

if __name__ == "__main__":
    for m in ["Sébaco", "Pantasma", "Tola", "Nandaime", "Jalapa", "Nueva Guinea"]:
        la, lo, no = resolver_coordenadas(m)
        rad = RadarClimatico(la, lo, no)
        res = rad.generar_advertencia_agronomica()
        try:
            print(res)
        except UnicodeEncodeError:
            print(res.encode('ascii', errors='replace').decode('ascii'))
        print("-" * 50)

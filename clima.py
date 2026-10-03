import requests
import logging
import time
import os
import json
import re

logger = logging.getLogger(__name__)

def normalizar_texto(texto: str) -> str:
    """Remueve tildes y caracteres especiales para búsqueda tolerante."""
    if not texto:
        return ""
    texto = texto.lower()
    for a, b in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
        texto = texto.replace(a, b)
    return texto

# Catálogo completo embebido de todos los departamentos y municipios de Nicaragua
CATALOGO_MUNICIPIOS = {
  "Chinandega": {
    "Chinandega": {
      "lat": 12.6294,
      "lon": -87.1311
    },
    "El Viejo": {
      "lat": 12.6633,
      "lon": -87.1689
    },
    "Chichigalpa": {
      "lat": 12.5714,
      "lon": -87.0264
    },
    "Posoltega": {
      "lat": 12.5444,
      "lon": -86.9797
    },
    "Corinto": {
      "lat": 12.4819,
      "lon": -87.1733
    },
    "Puerto Morazan": {
      "lat": 12.85,
      "lon": -87.1833
    },
    "Somotillo": {
      "lat": 13.0442,
      "lon": -86.9042
    },
    "Villa Nueva": {
      "lat": 12.9667,
      "lon": -86.8167
    },
    "Santo Tomas del Norte": {
      "lat": 13.1833,
      "lon": -86.9167
    },
    "Cinco Pinos": {
      "lat": 13.2333,
      "lon": -86.8667
    },
    "San Pedro del Norte": {
      "lat": 13.2833,
      "lon": -86.8667
    },
    "San Francisco del Norte": {
      "lat": 13.2,
      "lon": -86.7667
    },
    "El Realejo": {
      "lat": 12.5333,
      "lon": -87.1667
    }
  },
  "Leon": {
    "Leon": {
      "lat": 12.4379,
      "lon": -86.878
    },
    "Telica": {
      "lat": 12.52,
      "lon": -86.8589
    },
    "Quezalguaque": {
      "lat": 12.5083,
      "lon": -86.9042
    },
    "Larreynaga (Malpaisillo)": {
      "lat": 12.6744,
      "lon": -86.5756
    },
    "El Sauce": {
      "lat": 12.9833,
      "lon": -86.5333
    },
    "Achuapa": {
      "lat": 13.0536,
      "lon": -86.5892
    },
    "Santa Rosa del Penon": {
      "lat": 12.8014,
      "lon": -86.3689
    },
    "El Jicaral": {
      "lat": 12.7275,
      "lon": -86.3806
    },
    "La Paz Centro": {
      "lat": 12.3397,
      "lon": -86.6747
    },
    "Nagarote": {
      "lat": 12.2667,
      "lon": -86.6156
    }
  },
  "Managua": {
    "Managua": {
      "lat": 12.1364,
      "lon": -86.2514
    },
    "Tipitapa": {
      "lat": 12.1978,
      "lon": -86.0967
    },
    "Ciudad Sandino": {
      "lat": 12.1583,
      "lon": -86.3444
    },
    "Mateare": {
      "lat": 12.2389,
      "lon": -86.4278
    },
    "Villa El Carmen": {
      "lat": 11.9806,
      "lon": -86.5056
    },
    "San Rafael del Sur": {
      "lat": 11.8475,
      "lon": -86.4386
    },
    "El Crucero": {
      "lat": 11.9889,
      "lon": -86.3117
    },
    "Ticuantepe": {
      "lat": 12.0231,
      "lon": -86.205
    },
    "San Francisco Libre": {
      "lat": 12.5,
      "lon": -86.3
    }
  },
  "Masaya": {
    "Masaya": {
      "lat": 11.9744,
      "lon": -86.0942
    },
    "Nindiri": {
      "lat": 12.0053,
      "lon": -86.1219
    },
    "Tisma": {
      "lat": 12.0819,
      "lon": -86.0189
    },
    "Masatepe": {
      "lat": 11.9167,
      "lon": -86.15
    },
    "Niquinohomo": {
      "lat": 11.9039,
      "lon": -86.095
    },
    "Catarina": {
      "lat": 11.9114,
      "lon": -86.0747
    },
    "San Juan de Oriente": {
      "lat": 11.9056,
      "lon": -86.0736
    },
    "Nandasmo": {
      "lat": 11.9231,
      "lon": -86.1206
    },
    "La Concepcion": {
      "lat": 11.9367,
      "lon": -86.1894
    }
  },
  "Granada": {
    "Granada": {
      "lat": 11.9299,
      "lon": -85.956
    },
    "Nandaime": {
      "lat": 11.7567,
      "lon": -86.0528
    },
    "Diriomo": {
      "lat": 11.8764,
      "lon": -86.0517
    },
    "Diria": {
      "lat": 11.8847,
      "lon": -86.0569
    },
    "Malacatoya": {
      "lat": 12.1833,
      "lon": -85.8667
    }
  },
  "Carazo": {
    "Jinotepe": {
      "lat": 11.85,
      "lon": -86.2
    },
    "Diriamba": {
      "lat": 11.8581,
      "lon": -86.2392
    },
    "San Marcos": {
      "lat": 11.9094,
      "lon": -86.2036
    },
    "Dolores": {
      "lat": 11.8569,
      "lon": -86.2167
    },
    "El Rosario": {
      "lat": 11.8417,
      "lon": -86.1833
    },
    "La Paz de Carazo": {
      "lat": 11.8228,
      "lon": -86.1278
    },
    "Santa Teresa": {
      "lat": 11.8028,
      "lon": -86.2139
    },
    "La Conquista": {
      "lat": 11.7333,
      "lon": -86.1931
    }
  },
  "Rivas": {
    "Rivas": {
      "lat": 11.4372,
      "lon": -85.8263
    },
    "San Jorge": {
      "lat": 11.4556,
      "lon": -85.8031
    },
    "Buenos Aires": {
      "lat": 11.4697,
      "lon": -85.8164
    },
    "Potosi": {
      "lat": 11.4942,
      "lon": -85.8564
    },
    "Belen": {
      "lat": 11.5039,
      "lon": -85.8889
    },
    "Tola": {
      "lat": 11.3853,
      "lon": -85.9389
    },
    "San Juan del Sur": {
      "lat": 11.2528,
      "lon": -85.8706
    },
    "Cardenas": {
      "lat": 11.1964,
      "lon": -85.5089
    },
    "Moyogalpa (Ometepe)": {
      "lat": 11.54,
      "lon": -85.6983
    },
    "Altagracia (Ometepe)": {
      "lat": 11.5667,
      "lon": -85.58
    }
  },
  "Matagalpa": {
    "Matagalpa": {
      "lat": 12.9256,
      "lon": -85.9175
    },
    "Sebaco": {
      "lat": 12.855,
      "lon": -86.0967
    },
    "San Isidro": {
      "lat": 12.9292,
      "lon": -86.1953
    },
    "Ciudad Dario": {
      "lat": 12.7314,
      "lon": -86.1239
    },
    "San Ramon": {
      "lat": 12.9236,
      "lon": -85.8389
    },
    "Matiguas": {
      "lat": 12.8361,
      "lon": -85.4622
    },
    "Muy Muy": {
      "lat": 12.7631,
      "lon": -85.6297
    },
    "Esquipulas": {
      "lat": 12.6653,
      "lon": -85.7897
    },
    "Rio Blanco": {
      "lat": 12.9344,
      "lon": -85.2236
    },
    "Rancho Grande": {
      "lat": 13.25,
      "lon": -85.55
    },
    "El Tuma - La Dalia": {
      "lat": 13.12,
      "lon": -85.75
    },
    "Terrabona": {
      "lat": 12.7303,
      "lon": -85.9647
    },
    "San Dionisio": {
      "lat": 12.7606,
      "lon": -85.8503
    }
  },
  "Jinotega": {
    "Jinotega": {
      "lat": 13.0919,
      "lon": -86.0022
    },
    "Santa Maria de Pantasma": {
      "lat": 13.35,
      "lon": -85.9333
    },
    "Wiwili de Jinotega": {
      "lat": 13.6167,
      "lon": -85.8333
    },
    "El Cua": {
      "lat": 13.3667,
      "lon": -85.6667
    },
    "San Jose de Bocay": {
      "lat": 13.5417,
      "lon": -85.5389
    },
    "San Rafael del Norte": {
      "lat": 13.2128,
      "lon": -86.1108
    },
    "San Sebastian de Yali": {
      "lat": 13.3056,
      "lon": -86.1861
    },
    "La Concordia": {
      "lat": 13.1956,
      "lon": -86.1667
    }
  },
  "Esteli": {
    "Esteli": {
      "lat": 13.0918,
      "lon": -86.3538
    },
    "Condega": {
      "lat": 13.35,
      "lon": -86.3989
    },
    "Pueblo Nuevo": {
      "lat": 13.3814,
      "lon": -86.4808
    },
    "San Juan de Limay": {
      "lat": 13.1764,
      "lon": -86.6128
    },
    "La Trinidad": {
      "lat": 12.9686,
      "lon": -86.2367
    },
    "San Nicolas": {
      "lat": 12.9333,
      "lon": -86.35
    }
  },
  "Madriz": {
    "Somoto": {
      "lat": 13.4808,
      "lon": -86.5821
    },
    "San Lucas": {
      "lat": 13.4139,
      "lon": -86.6111
    },
    "Las Sabanas": {
      "lat": 13.3486,
      "lon": -86.6214
    },
    "San Jose de Cusmapa": {
      "lat": 13.2889,
      "lon": -86.6556
    },
    "Totogalpa": {
      "lat": 13.5636,
      "lon": -86.4925
    },
    "Telpaneca": {
      "lat": 13.5333,
      "lon": -86.2833
    },
    "Palacaguina": {
      "lat": 13.4556,
      "lon": -86.4069
    },
    "Yalaguina": {
      "lat": 13.4833,
      "lon": -86.4944
    },
    "San Juan de Rio Coco": {
      "lat": 13.5444,
      "lon": -86.1639
    }
  },
  "Nueva Segovia": {
    "Ocotal": {
      "lat": 13.6321,
      "lon": -86.4752
    },
    "Jalapa": {
      "lat": 13.9211,
      "lon": -86.1264
    },
    "El Jicaro": {
      "lat": 13.7208,
      "lon": -86.1408
    },
    "Murra": {
      "lat": 13.7597,
      "lon": -86.0194
    },
    "Quilali": {
      "lat": 13.5667,
      "lon": -86.0333
    },
    "San Fernando": {
      "lat": 13.6789,
      "lon": -86.315
    },
    "Santa Maria": {
      "lat": 13.7483,
      "lon": -86.7117
    },
    "Macuelizo": {
      "lat": 13.6528,
      "lon": -86.6139
    },
    "Dipilto": {
      "lat": 13.7194,
      "lon": -86.5117
    },
    "Ciudad Antigua": {
      "lat": 13.6406,
      "lon": -86.3072
    },
    "Wiwili de Nueva Segovia": {
      "lat": 13.6264,
      "lon": -85.8264
    },
    "Mozonte": {
      "lat": 13.6583,
      "lon": -86.4528
    }
  },
  "Boaco": {
    "Boaco": {
      "lat": 12.4722,
      "lon": -85.6586
    },
    "Camoapa": {
      "lat": 12.3833,
      "lon": -85.5167
    },
    "San Lorenzo": {
      "lat": 12.3789,
      "lon": -85.6661
    },
    "Teustepe": {
      "lat": 12.4217,
      "lon": -85.7983
    },
    "San Jose de los Remates": {
      "lat": 12.5978,
      "lon": -85.7608
    },
    "Santa Lucia": {
      "lat": 12.5317,
      "lon": -85.7103
    }
  },
  "Chontales": {
    "Juigalpa": {
      "lat": 12.1063,
      "lon": -85.3645
    },
    "Acoyapa": {
      "lat": 11.9703,
      "lon": -85.1714
    },
    "Santo Tomas": {
      "lat": 12.0694,
      "lon": -85.0906
    },
    "Comalapa": {
      "lat": 12.2833,
      "lon": -85.5103
    },
    "San Pedro de Lovago": {
      "lat": 12.1286,
      "lon": -85.1158
    },
    "La Libertad": {
      "lat": 12.2164,
      "lon": -85.1661
    },
    "Santo Domingo": {
      "lat": 12.2611,
      "lon": -85.0806
    },
    "El Coral": {
      "lat": 11.9167,
      "lon": -84.5167
    },
    "San Francisco de Cuapa": {
      "lat": 12.2694,
      "lon": -85.3819
    }
  },
  "Rio San Juan": {
    "San Carlos": {
      "lat": 11.1333,
      "lon": -84.7833
    },
    "El Castillo": {
      "lat": 11.0181,
      "lon": -84.3986
    },
    "San Miguelito": {
      "lat": 11.4028,
      "lon": -84.8989
    },
    "Morrito": {
      "lat": 11.6214,
      "lon": -85.0806
    },
    "El Almendro": {
      "lat": 11.6786,
      "lon": -84.7028
    },
    "San Juan de Nicaragua": {
      "lat": 10.9231,
      "lon": -83.7056
    }
  },
  "Costa Caribe Sur (RACCS)": {
    "Bluefields": {
      "lat": 12.0137,
      "lon": -83.7635
    },
    "Nueva Guinea": {
      "lat": 11.6876,
      "lon": -84.4562
    },
    "El Rama": {
      "lat": 12.1594,
      "lon": -84.2194
    },
    "Muelle de los Bueyes": {
      "lat": 12.0667,
      "lon": -84.5333
    },
    "Kukra Hill": {
      "lat": 12.2417,
      "lon": -83.75
    },
    "Corn Island": {
      "lat": 12.17,
      "lon": -83.06
    },
    "La Cruz de Rio Grande": {
      "lat": 13.1128,
      "lon": -84.1856
    },
    "Desembocadura de Rio Grande": {
      "lat": 12.9961,
      "lon": -83.5608
    },
    "Laguna de Perlas": {
      "lat": 12.3428,
      "lon": -83.6711
    },
    "El Tortuguero": {
      "lat": 12.82,
      "lon": -84.195
    },
    "Bocana de Paiwas": {
      "lat": 12.7878,
      "lon": -85.1239
    }
  },
  "Costa Caribe Norte (RACCN)": {
    "Puerto Cabezas (Bilwi)": {
      "lat": 14.0351,
      "lon": -83.3888
    },
    "Waspam": {
      "lat": 14.7419,
      "lon": -83.9739
    },
    "Siuna": {
      "lat": 13.7332,
      "lon": -84.7773
    },
    "Bonanza": {
      "lat": 14.0289,
      "lon": -84.5847
    },
    "Rosita": {
      "lat": 13.9267,
      "lon": -84.4039
    },
    "Prinzapolka": {
      "lat": 13.4072,
      "lon": -83.5642
    },
    "Mulukuku": {
      "lat": 13.1492,
      "lon": -84.9706
    },
    "Waslala": {
      "lat": 13.2333,
      "lon": -85.3833
    }
  }
}

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

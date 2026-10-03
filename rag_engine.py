import os
import json
import logging
import re
import time
from google import genai

logger = logging.getLogger(__name__)

STOP_WORDS = {
    "que", "cual", "cuales", "como", "cuando", "donde", "quien", "por", "para", "con", "sin",
    "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella",
    "tiene", "tengo", "tener", "esta", "estan", "cultivo", "cultivos", "planta",
    "plantas", "hoja", "hojas", "mira", "foto", "imagen", "ayuda", "saber", "hola", "buenos",
    "dias", "tardes", "noches", "saludos", "favor", "gracias", "muchas", "algo", "nada",
    "todo", "bien", "mal", "hacer", "hago", "puedo", "debo", "deberia", "sera", "seria",
    "recomiendas", "recomendar", "producto", "productos", "quimico", "remedio", "aplicar",
    "sobre", "desde", "hasta", "entre", "hacia", "contra"
}

def _extraer_extracto_relevante(texto: str, palabras_clave: list, max_chars: int = 1200) -> str:
    """Extrae quirúrgicamente la sección de dosis o el fragmento donde aparecen las palabras clave."""
    if not texto:
        return ""
    if len(texto) <= max_chars:
        return texto
        
    keywords_busqueda = list(palabras_clave) + ["dosis", "l/ha", "g/ha", "kg/ha", "ml/bomba", "litros"]
    pos_min = -1
    texto_lower = texto.lower()
    for kw in keywords_busqueda:
        p = texto_lower.find(kw)
        if p != -1 and (pos_min == -1 or p < pos_min):
            pos_min = p
            
    if pos_min == -1:
        return texto[:max_chars] + "..."
        
    inicio = max(0, pos_min - 150)
    fin = min(len(texto), inicio + max_chars)
    return ("..." if inicio > 0 else "") + texto[inicio:fin] + ("..." if fin < len(texto) else "")

def _sanitizar_salida(texto: str) -> str:
    """Elimina estrictamente cualquier mención de 'Doctor', 'Doctorado', instituciones o autores."""
    if not texto:
        return texto
        
    reemplazos = [
        (r"Doctor(?:ado)?\s+en\s+Entomolog[ií]a\s+y\s+Fitopatolog[ií]a(?:\s*\([^)]*\))?", ""),
        (r"Doctor(?:ado)?\s+en\s+Entomolog[ií]a", ""),
        (r"Doctor(?:ado)?\s+en\s+Fitopatolog[ií]a", ""),
        (r"Doctor(?:ado)?\s+en\s+Sanidad\s+Vegetal", ""),
        (r"\bDoctor(?:ado)?\b", ""),
        (r"\bUNA\b", ""),
        (r"\bINTA\b", ""),
        (r"\bINATEC\b", ""),
        (r"\bIPSA\b", ""),
        (r"\bMAG\b", ""),
        (r"\bUNAN\b", ""),
        (r"\(\s*UNA\s*\)", ""),
        (r"\(\s*INTA\s*\)", ""),
        (r"\(\s*INATEC\s*\)", ""),
        (r"\(\s*UNA\s*/\s*INTA\s*\)", ""),
        (r"Dr\.\s*Edgardo\s*Jim[eé]nez\s*Mart[ií]nez", "el manual técnico"),
        (r"Dr\.\s*Edgardo\s*Jim[eé]nez", "el manual técnico"),
        (r"Edgardo\s*Jim[eé]nez", "el manual técnico"),
        (r"George\s*N\.\s*Agrios", "la literatura fitopatológica"),
        (r"Agrios", "la literatura técnica"),
        (r"Floria\s*Bertsch", "la literatura técnica"),
        (r"Bertsch", "la literatura técnica"),
        (r"Oswaldo\s*Rodr[ií]guez", "la literatura técnica")
    ]
    for pat, repl in reemplazos:
        texto = re.sub(pat, repl, texto, flags=re.IGNORECASE)
        
    # Limpiar posibles saludos que digan 'Como...'
    texto = re.sub(r"^(?:Hola[!,.\s]*)?como\s*[,:]?\s*", "", texto, flags=re.IGNORECASE)
    texto = re.sub(r"\(\s*\)", "", texto)
    texto = re.sub(r"\(\s*/\s*\)", "", texto)
    texto = re.sub(r"[ \t]{2,}", " ", texto)
    return texto.strip()

class AsistenteFitosanitario:
    def __init__(self, api_key: str = None, base_agroquimicos: dict = None, base_libros: dict = None, base_entomologia: dict = None, base_cultivos: dict = None, base_nutricion: dict = None):
        key_to_use = api_key or os.getenv("GEMINI_API_KEY")
        if key_to_use:
            self.client = genai.Client(api_key=key_to_use)
        else:
            self.client = None
            logger.warning("Inicialización fallida: No se proporcionó API key para Gemini.")
        
        # Cargar bases de conocimiento enriquecidas (usando caché si se proporcionan)
        self.base_agroquimicos = base_agroquimicos if base_agroquimicos is not None else self._cargar_db("base_conocimiento_agroquimicos.json")
        self.base_libros = base_libros if base_libros is not None else self._cargar_db("base_libros.json")
        self.base_entomologia = base_entomologia if base_entomologia is not None else self._cargar_db("base_entomologia_nicaragua.json")
        self.base_cultivos = base_cultivos if base_cultivos is not None else self._cargar_db("base_cultivos_nicaragua.json")
        self.base_nutricion = base_nutricion if base_nutricion is not None else self._cargar_db("base_nutricion_cultivos.json")
        
        # Cargar Catálogo Comercial Maestro Completo de Nicaragua (99 productos)
        self.base_catalogo_completo = self._cargar_db("catalogo_comercial_completo.json")
        if self.base_catalogo_completo:
            for prod_nom, info in self.base_catalogo_completo.items():
                if prod_nom not in self.base_agroquimicos:
                    self.base_agroquimicos[prod_nom] = {
                        "nombre_comercial": prod_nom,
                        "i_a": info.get("i_a", ""),
                        "tipo": info.get("categoria", ""),
                        "grupo_frac_irac": info.get("grupo", ""),
                        "espectro": info.get("uso_principal", ""),
                        "dosis_recomendada": f"{info.get('dosis_ha', '')} {info.get('unidad', '')} ({info.get('dosis_bomba', '')} por bomba 20L)",
                        "texto_ficha": f"Producto Comercial: {prod_nom}. Ingrediente activo: {info.get('i_a', '')}. Grupo: {info.get('grupo', '')}. Categoría: {info.get('categoria', '')}. Dosis por hectárea: {info.get('dosis_ha', '')} {info.get('unidad', '')}. Dosis por bomba de 20L: {info.get('dosis_bomba', '')}. Usos y plagas: {info.get('uso_principal', '')}"
                    }

    def _cargar_db(self, nombre_archivo):
        ruta = os.path.join("data", nombre_archivo)
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Error decodificando {nombre_archivo}: {e}")
        return {}

    def buscar_conocimiento_relevante(self, query: str, max_productos: int = 4, max_fragmentos_libros: int = 2):
        """Busca productos, plagas, cultivos, curvas de nutrición y fragmentos de libros de forma compacta."""
        query_lower = query.lower()
        palabras_brutas = [re.sub(r'[^a-záéíóúñ]', '', p) for p in query_lower.split()]
        palabras_clave = [p for p in palabras_brutas if len(p) > 3 and p not in STOP_WORDS]
        
        # Si no hay palabras clave específicas (ej. solo dice "que es lo que tiene mi cultivo" con una foto)
        if not palabras_clave:
            # Enviamos un catálogo estructurado por marcas comerciales y su principio activo
            fungicidas = []
            insecticidas = []
            for k, v in self.base_agroquimicos.items():
                nom = v.get("nombre_comercial") or k.replace('_', ' ').title()
                ia = v.get("i_a") or v.get("ingrediente_activo", "")
                tipo = v.get("tipo", "").lower()
                g = v.get("grupo_frac_irac") or v.get("grupo_frac") or v.get("grupo_irac") or ""
                
                if ia and ia != "N/A":
                    item = f"**{nom}** (IA: {ia} | Grupo: {g})"
                    if "fungicida" in tipo or "frac" in g.lower():
                        fungicidas.append(item)
                    elif "insecticida" in tipo or "irac" in g.lower():
                        insecticidas.append(item)
                        
            resumen_catalogo = {
                "Fungicidas_Comerciales_Foliares": fungicidas[:12],
                "Insecticidas_Comerciales_Foliares": insecticidas[:12],
                "Tratamientos_Radiculares_y_Suelo_Drench": [
                    "**Ridomil Gold MZ** (Fungicida Drench para Pythium, Phytophthora y pudrición de raíz - Mefenoxam + Mancozeb | FRAC 4 + M3)",
                    "**Mertect 500 SC** (Fungicida Drench para Fusarium y Rhizoctonia radicular - Thiabendazol | FRAC 1)",
                    "**Infinito** (Fungicida de suelo/drench para Oomicetos radiculares - Propamocarb + Fluopicolide | FRAC 28 + 43)",
                    "**Solvigo** (Nematicida e insecticida radicular - Abamectina + Tiametoxam | IRAC 6 + 4A)",
                    "**Actara 25 WG** (Insecticida al cuello/drench para plagas de suelo y raíz - Thiamethoxam | IRAC 4A)"
                ]
            }
            # Retorno consistente de 5 elementos para evitar ValueError al desempaquetar
            return resumen_catalogo, {}, {}, {}, {}

        # 1. Puntuar y extraer productos relevantes (SOLO datos agronómicos esenciales)
        raiz_keywords = {"raiz", "radicular", "radiculares", "cuello", "drench", "suelo", "pudricion", "marchitez", "nematodo", "nematodos", "agallas", "fusarium", "pythium", "phytophthora", "rhizoctonia", "secadera"}
        es_consulta_radicular = any(k in palabras_clave for k in raiz_keywords)

        puntuaciones_agro = {}
        for producto, datos in self.base_agroquimicos.items():
            score = 0
            nombre_comercial = (datos.get("nombre_comercial") or producto.replace("_", " ")).lower()
            espectro = datos.get("espectro", "").lower()
            tipo = datos.get("tipo", "").lower()
            ingrediente = (datos.get("i_a") or datos.get("ingrediente_activo", "")).lower()
            texto_ficha = datos.get("texto_ficha", "").lower()
            
            for p in palabras_clave:
                if p in nombre_comercial: score += 20
                if p in ingrediente: score += 15
                if p in espectro: score += 10
                if p in tipo: score += 5
                if p in texto_ficha: score += 1
                
            if es_consulta_radicular:
                if any(x in producto.lower() for x in ["ridomil", "mertect", "infinito", "solvigo", "actara"]):
                    score += 25
                if "drench" in texto_ficha or "suelo" in texto_ficha or "fusarium" in texto_ficha or "pythium" in texto_ficha:
                    score += 15
                
            if score > 0:
                puntuaciones_agro[producto] = score
                
        top_agro = sorted(puntuaciones_agro.items(), key=lambda x: x[1], reverse=True)[:max_productos]
        
        catalogo_relevante = {}
        for prod, score in top_agro:
            datos_orig = self.base_agroquimicos[prod]
            nom = datos_orig.get("nombre_comercial") or prod.replace("_", " ").title()
            ia = datos_orig.get("i_a") or datos_orig.get("ingrediente_activo", "")
            grupo = datos_orig.get("grupo_frac_irac") or datos_orig.get("grupo_frac") or datos_orig.get("grupo_irac") or ""
            
            catalogo_relevante[nom] = {
                "producto_comercial": nom,
                "ingrediente_activo": ia,
                "tipo": datos_orig.get("tipo", ""),
                "grupo_frac_irac": grupo,
                "espectro": datos_orig.get("espectro", ""),
                "dosis_registrada": datos_orig.get("dosis_recomendada", ""),
                "extracto_etiqueta_dosis": _extraer_extracto_relevante(datos_orig.get("texto_ficha", ""), palabras_clave, max_chars=1200)
            }

        # 2. Búsqueda y rescate en Base Entomológica de Nicaragua con Ranking Top-3
        entomologia_relevante = {}
        if self.base_entomologia:
            puntuaciones_ins = {}
            for insect_id, datos_ins in self.base_entomologia.items():
                score_ins = 0
                nom_c = datos_ins.get("nombre_comun", "").lower()
                nom_s = datos_ins.get("nombre_cientifico", "").lower()
                orden = datos_ins.get("orden", "").lower()
                familia = datos_ins.get("familia", "").lower()
                hospedantes = " ".join(datos_ins.get("cultivos_hospedantes", [])).lower()
                daño = datos_ins.get("daño", "").lower()
                
                for p in palabras_clave:
                    if p in nom_c: score_ins += 25
                    if p in nom_s: score_ins += 30
                    if p in orden or p in familia: score_ins += 15
                    if p in daño: score_ins += 8
                    if p in hospedantes: score_ins += 5

                # Detectar palabras de plagas genéricas
                if any(x in palabras_clave for x in ["gusano", "larva", "plaga", "insecto", "bicho", "oruga", "cogollero", "barrenador", "minador", "trozador", "mosca", "trips", "salivazo", "broca", "palomilla"]):
                    if score_ins > 0:
                        score_ins += 10

                if score_ins >= 10:
                    puntuaciones_ins[insect_id] = score_ins

            # Ordenar por relevancia y limitar a los 3 más pertinentes
            top_ins = sorted(puntuaciones_ins.items(), key=lambda x: x[1], reverse=True)[:3]
            for insect_id, _ in top_ins:
                datos_ins = self.base_entomologia[insect_id]
                entomologia_relevante[datos_ins.get("nombre_comun")] = {
                    "taxonomia": f"{datos_ins.get('orden')} : {datos_ins.get('familia')} - {datos_ins.get('nombre_cientifico')}",
                    "cultivos_afectados": datos_ins.get("cultivos_hospedantes"),
                    "biologia_y_ciclo": datos_ins.get("biologia_y_ciclo"),
                    "daño_caracteristico": datos_ins.get("daño"),
                    "umbral_economico_nicaragua": datos_ins.get("umbral_economico_nicaragua"),
                    "control_biologico": datos_ins.get("control_biologico"),
                    "control_cultural": datos_ins.get("control_cultural"),
                    "control_quimico_recomendado": datos_ins.get("control_quimico_sugerido")
                }

        # 3. Búsqueda en Base de Cultivos Agroindustriales - Inmune a tildes
        cultivos_relevantes = {}
        if self.base_cultivos:
            # Función auxiliar para remover tildes
            def desacentuar(s):
                for a, b in [('á','a'), ('é','e'), ('í','i'), ('ó','o'), ('ú','u'), ('ñ','n')]:
                    s = s.replace(a, b)
                return s

            for cult_id, datos_c in self.base_cultivos.items():
                nom_cult = datos_c.get("nombre_cultivo", "").lower()
                nom_cient = datos_c.get("nombre_cientifico", "").lower()
                nom_clean = desacentuar(nom_cult)
                id_clean = cult_id.replace("_", " ")

                coincide = any(
                    p in nom_cult or p in nom_clean or p in cult_id or cult_id in p or p in id_clean
                    for p in palabras_clave
                ) or (nom_clean in desacentuar(query_lower))
                
                if coincide:
                    cultivos_relevantes[datos_c.get("nombre_cultivo")] = {
                        "variedades_nicaragua": datos_c.get("variedades_nicaragua"),
                        "requerimientos": datos_c.get("requerimientos_edafoclimaticos"),
                        "manejo_agronomico": datos_c.get("manejo_agronomico")
                    }

        # 4. Búsqueda y rescate en Base Nutricional y Curvas de Absorción (44 Cultivos)
        nutricion_relevante = {}
        if self.base_nutricion:
            nutri_keywords = {
                "fertilizante", "fertilizantes", "fertilizacion", "abono", "abonos", "abonar",
                "nutricion", "nutrimentos", "nutrientes", "dosis", "kg/ha", "npk", "n-p-k",
                "nitrogeno", "fosforo", "potasio", "calcio", "magnesio", "boro", "zinc",
                "curva", "absorcion", "extraccion", "rendimiento", "tonelada", "fertirriego",
                "urea", "dap", "kcl", "mop", "requerimiento"
            }
            es_consulta_nutricional = any(k in palabras_clave for k in nutri_keywords)
            
            puntuaciones_nutri = {}
            for cult_id, datos_n in self.base_nutricion.items():
                score_n = 0
                nom_c = datos_n.get("nombre_comun", "").lower()
                grupo = datos_n.get("grupo_agronomico", "").lower()
                
                for p in palabras_clave:
                    if p in nom_c: score_n += 30
                    if p in cult_id: score_n += 30
                    if p in grupo: score_n += 10
                    
                if es_consulta_nutricional and score_n > 0:
                    score_n += 25
                    
                if score_n >= 20:
                    puntuaciones_nutri[cult_id] = score_n
                    
            top_nutri = sorted(puntuaciones_nutri.items(), key=lambda x: x[1], reverse=True)[:2]
            for cult_id, _ in top_nutri:
                datos_n = self.base_nutricion[cult_id]
                din = datos_n.get("dinamica_nutricional", {})
                nutricion_relevante[datos_n.get("nombre_comun")] = {
                    "grupo_agronomico": datos_n.get("grupo_agronomico"),
                    "extraccion_total_kg_t": datos_n.get("extraccion_nutrimentos_kg_por_t", {}).get("extraccion_total"),
                    "extraccion_cosecha_kg_t": datos_n.get("extraccion_nutrimentos_kg_por_t", {}).get("extraccion_cosecha"),
                    "relacion_nk_cosecha": datos_n.get("balance_nutricional", {}).get("relacion_nk_cosecha"),
                    "demanda_potasio": datos_n.get("balance_nutricional", {}).get("categoria_demanda_k"),
                    "curva_tipo": din.get("curva_tipo"),
                    "fraccionamiento_por_etapas": din.get("fraccionamiento_por_etapas"),
                    "secundarios_kg_t": din.get("extraccion_secundarios_estimada_kg_t"),
                    "micronutrientes_criticos": din.get("micronutrientes_criticos"),
                    "formula_dosis": din.get("formula_calculo_dosis")
                }

        # 5. Puntuar y extraer fragmentos de libros generales
        puntuaciones_libros = {}
        for fragmento, datos in self.base_libros.items():
            score = 0
            texto_libro = datos.get("texto", "").lower()
            for p in palabras_clave:
                if p in texto_libro: score += texto_libro.count(p)
            if score >= 3:
                puntuaciones_libros[fragmento] = score
                
        top_libros = sorted(puntuaciones_libros.items(), key=lambda x: x[1], reverse=True)[:max_fragmentos_libros]
        
        libros_relevantes = {}
        for frag, score in top_libros:
            datos_frag = self.base_libros[frag]
            libros_relevantes[frag] = {
                "origen": datos_frag.get("origen", ""),
                "extracto": _extraer_extracto_relevante(datos_frag.get("texto", ""), palabras_clave, max_chars=1000)
            }

        return catalogo_relevante, entomologia_relevante, cultivos_relevantes, nutricion_relevante, libros_relevantes

    def generar_respuesta(self, historial_chat: list, mensaje_usuario: str, imagen=None, ubicacion_usuario: str = None) -> str:
        if not self.client:
            return "⚠️ Necesitas configurar tu API Key gratuita de Gemini (Google AI Studio) para habilitar la Inteligencia Artificial."
            
        # Extraer el contexto relevante compacto
        catalogo_relevante, entomologia_relevante, cultivos_relevantes, nutricion_relevante, libros_relevantes = self.buscar_conocimiento_relevante(mensaje_usuario)
        
        info_catalogo = json.dumps(catalogo_relevante, ensure_ascii=False) if catalogo_relevante else "Catálogo disponible general."
        info_entomologia = json.dumps(entomologia_relevante, ensure_ascii=False) if entomologia_relevante else "No se detectaron especies entomológicas específicas."
        info_cultivos = json.dumps(cultivos_relevantes, ensure_ascii=False) if cultivos_relevantes else "Manejo agronómico estándar."
        info_nutricion = json.dumps(nutricion_relevante, ensure_ascii=False) if nutricion_relevante else "Extracción estándar por curvas sigmoideas."
        info_libros = json.dumps(libros_relevantes, ensure_ascii=False) if libros_relevantes else "No se requieren citas bibliográficas específicas."

        # Obtener clima en tiempo real dinámico según la ubicación del usuario o mención en el chat
        nombre_zona = "Managua"
        try:
            from clima import RadarClimatico, resolver_coordenadas
            
            # Priorizar la ubicación explícita de la interfaz
            if ubicacion_usuario:
                lat_c, lon_c, nombre_zona = resolver_coordenadas(ubicacion_usuario)
            else:
                lat_c, lon_c, nombre_zona = resolver_coordenadas(mensaje_usuario)
                
            radar = RadarClimatico(lat_c, lon_c, nombre_zona)
            clima_actual = radar.generar_advertencia_agronomica()
        except Exception as e:
            clima_actual = f"Clima en {nombre_zona}: Condiciones normales de aplicación."

        # Preparar contexto sintético, ligero y con REGLA ESTRICTA DE NOMBRE COMERCIAL Y ENTOMOLOGÍA
        contexto_sistema = (
            "Eres el Asistente Agronómico y Fitosanitario Inteligente de Nicaragua.\n"
            "Tu misión es realizar diagnósticos de máxima precisión científica y prescribir los PRODUCTOS COMERCIALES EXACTOS de tu catálogo local.\n\n"
            "REGLAS OBLIGATORIAS:\n\n"
            "1. PROTOCOLO ENTOMOLÓGICO DE NICARAGUA (CUANDO HAYA INSECTOS O PLAGAS):\n"
            "   - Basado en la entomología agrícola y fitosanitaria de los cultivos en Nicaragua:\n"
            "   - Si se detecta un insecto o daño por plaga (o en la foto se aprecia un insecto/oruga/larva/chinche/mosca/escarabajo):\n"
            "     * 🔬 **Identificación Taxonómica:** Orden, Familia, Género y Especie exacta.\n"
            "     * 🐛 **Nombre Común en Nicaragua:** (ej. Gusano cogollero, Mosca blanca, Barrenador del fruto de sandía, Broca del café, Gallina ciega, Salivazo, etc.).\n"
            "     * 🔄 **Biología y Estadío Dañino:** Huevo, larva/ninfa, pupa, adulto. Explica qué estadío causa el daño económico y cómo reconocerlo.\n"
            "     * 🎯 **Síntomas y Daño en el Cultivo:** Perforación de frutos, raspado foliar, daño al cogollo, agallas o transmisión de virus.\n"
            "     * 🛑 **Umbral Económico de Decisión (Nicaragua):** Indica el porcentaje de infestación o número de insectos por planta que justifica la aplicación técnica.\n"
            "     * 🐞 **Control Biológico y Cultural:** Enemigos naturales nativos (Trichogramma, Bacillus thuringiensis, Beauveria bassiana, Metarhizium, crisopas) y prácticas culturales.\n\n"
            "2. OBLIGATORIO - PRESCRIPCIÓN FITOSANITARIA 360° (NUNCA OMITIR PLAGUICIDAS EN AFECCIONES RADICULARES):\n"
            "   - Si el problema involucra RAÍCES o SUELO (pudrición radicular, marchitez vascular, damping-off, nematodos, Pythium, Phytophthora, Fusarium, Rhizoctonia, Gallina ciega):\n"
            "   - ESTÁ TOTALMENTE PROHIBIDO limitarse a dar solo consejos nutricionales o enraizadores.\n"
            "   - DEBES PRESCRIBIR OBLIGATORIAMENTE en la misma respuesta el TRATAMIENTO AL DRENCH/CUELLO con las marcas comerciales de tu catálogo (ejemplo: **Ridomil Gold MZ** o **Infinito** para Oomicetos; **Mertect 500 SC** para Fusarium/Rhizoctonia; **Solvigo** para nematodos; **Actara 25 WG** / **Lorsban** para plagas de suelo).\n\n"
            "3. OBLIGATORIO - NOMBRAR LA MARCA / PRODUCTO COMERCIAL:\n"
            "   - El agricultor no compra ingredientes activos puros, compra MARCAS COMERCIALES en la agropecuaria local.\n"
            "   - En CADA recomendación, DEBES DAR EL NOMBRE COMERCIAL EXACTO del catálogo local (ejemplo: **Match 050 EC**, **Proclaim 05 SG**, **Actara 25 WG**, **Amistar Top**, **Score 250 EC**, **Nativo 75 WG**, **Bravo 72 SC**, **Ridomil Gold MZ**, **Mertect 500 SC**, etc.).\n"
            "   - Estructura obligatoria por cada producto que recetes:\n"
            "     * 🌿 **Producto Comercial:** [Nombre Comercial de Marca]\n"
            "     * 🧪 **Ingrediente Activo:** [I.A.]\n"
            "     * 🏷️ **Grupo FRAC / IRAC:** [Grupo]\n"
            "     * 🔬 **Modo de Acción & Mecanismo de Muerte:** [Familia química (ej. Organofosforados, Diamidas antranílicas, Neonicotinoides, Triazoles, Estrobirulinas, etc.) y CÓMO MATA al insecto o patógeno (ejemplo: 'Inhibe la acetilcolinesterasa bloqueando la transmisión del impulso nervioso y provocando hiperexcitación, parálisis y muerte', 'Modula los receptores de rianodina liberando calcio intracelular descontroladamente lo que causa parálisis muscular letal', 'Inhibe la biosíntesis de ergosterol destruyendo la pared y membrana celular del hongo', o 'Inhibe la respiración mitocondrial en el complejo III impidiendo la producción de energía y la germinación de esporas')]\n"
            "     * ⚖️ **Dosis por Hectárea:** [Dosis/ha]\n"
            "     * 🎒 **Dosis por Bomba de 20L:** [Dosis/bomba de 20 litros (dosis/ha dividido entre 10)]\n"
            "     * 💧 **Forma de Aplicación:** [Foliar al follaje / Al drench dirigido a la base o cuello de la planta / En fertirriego]\n\n"
            "4. ROTACIÓN QUÍMICA: Siempre sugiere al menos 2 opciones de DIFERENTE grupo FRAC o IRAC para que el productor pueda rotar y no generar resistencia.\n"
            "5. CLIMA LOCAL Y VENTANA DE APLICACIÓN:\n"
            f"   - Zona geográfica actual del lote: {nombre_zona}.\n"
            "   - Considera las condiciones específicas de lluvia y viento indicadas en el pronóstico meteorológico local.\n"
            "   - Si hay lluvia inminente o viento fuerte en esa zona, advierte de inmediato sobre lavado de producto o deriva.\n\n"
            "6. PROHIBICIÓN TOTAL Y ESTRICTA (REGLA FUNDAMENTAL E INQUEBRANTABLE):\n"
            "   - ESTÁ TOTALMENTE PROHIBIDO usar, escribir o mencionar las palabras o frases:\n"
            "     * 'Doctor' o 'Doctorado'\n"
            "     * 'Entomología y Fitopatología (UNA / INTA)'\n"
            "     * 'UNA', 'INTA', 'INATEC', 'IPSA', 'MAG', 'UNAN', ni ninguna institución pública o privada.\n"
            "     * Nombres de autores de libros o manuales (ej. Jiménez, Agrios, Rodríguez, etc.).\n"
            "   - NUNCA te presentes diciendo 'Como doctor...' ni menciones títulos de doctorado ni instituciones.\n"
            "   - Responde DIRECTAMENTE al productor con el diagnóstico agronómico, taxonomía y productos comerciales con sus dosis.\n\n"
            "7. PROTOCOLO NUTRICIONAL Y CURVAS DE ABSORCIÓN (44 CULTIVOS DISPONIBLES):\n"
            "   - Si la consulta involucra fertilización, abonado, dosis por hectárea, nutrición vegetal o rendimiento meta:\n"
            "   - UNIDAD OBLIGATORIA: Basa OBLIGATORIAMENTE tu cálculo y unidades de rendimiento en QUINTALES POR HECTÁREA O POR MANZANA (qq/ha o qq/mz). NUNCA uses toneladas por hectárea (t/ha), ya que los productores nicaragüenses cuantifican sus cosechas exclusivamente en Quintales (1 quintal = 100 lb = 45.36 kg; 1 t = 22.046 qq):\n"
            "     * 📊 **Extracción Total por Quintal (qq):** Kg de N, P2O5, K2O requeridos por cada quintal cosechado (calculado convirtiendo los datos de absorción: kg/t dividido entre 22.046).\n"
            "     * 🌾 **Exportación Neta en Cosecha:** Proporción de nutrientes removidos del lote por quintal cosechado vs rastrojo reincorporado.\n"
            "     * ⚖️ **Relación N:K y Exigencia Potásica:** Destaca si el cultivo tiene alta demanda de Potasio (ej. Sandía, Tomate, Banano, Papa) o si predomina el Nitrógeno (Maíz, Frijol, Soya).\n"
            "     * 🦠 **FIJACIÓN BIOLÓGICA DE NITRÓGENO (FBN) EN LEGUMINOSAS (FRIJOL, SOYA, MANÍ, ARVEJA):**\n"
            "       - Para cultivos leguminosos como el frijol, NUNCA prescribas la demanda total bruta de nitrógeno con urea química.\n"
            "       - OBLIGATORIO: Descuenta el nitrógeno que la propia planta aporta mediante simbiosis con bacterias fijadoras (Rhizobium spp.).\n"
            "       - Utiliza un valor medio representativo para cepas nativas en suelos agrícolas de Nicaragua de **40.0 kg N/ha** fijados biológicamente por el frijol.\n"
            "       - DEJA TOTALMENTE CLARO y explícito al productor que realizas esta resta: indica que se descuentan 40 kg N/ha aportados gratuitamente por los nódulos nativos y que esto equivale a un ahorro de **~2.5 a 3.0 sacos de Urea (50 kg) por hectárea**.\n"
            "       - Por tanto, la fertilización química en frijol se limita al fósforo y nitrógeno inicial/starter (cubierto usualmente por el DAP 18-46-0 o 12-24-12) y únicamente un complemento mínimo si la meta de quintales es muy alta.\n"
            "     * 🔬 **DESCUENTO POR ANÁLISIS DE SUELO (OPCIONAL):**\n"
            "       - Si el productor menciona o ingresa datos de análisis químico de suelo (ppm de fósforo, potasio intercambiable, materia orgánica / N disponible, pH), resta los nutrientes que ya aporta el suelo para dar la dosis neta final.\n"
            "       - Si el productor NO cuenta con análisis de suelo, formula con las eficiencias agronómicas estándar sin exigirle obligatoriamente el examen.\n"
            "     * 📈 **Dinámica Sigmoidea y Fraccionamiento:** Divide la dosis en las fases fenológicas (Establecimiento, Crecimiento/Floración, Llenado/Maduración) indicando el rol fisiológico de cada elemento.\n"
            "     * 🧪 **Dosis Recomendada por Hectárea:** Aplica eficiencias de suelo estándar (N 60%, P2O5 25%, K2O 70%) y desglosa en fertilizantes comerciales comunes (Urea 46-0-0, DAP 18-46-0, MOP 0-0-60, Nitrato de Potasio, etc.).\n"
            "     * 🔬 **Nutrientes Secundarios y Micronutrientes:** Recomienda Ca, Mg, S y micronutrientes críticos (Boro, Zinc, etc.).\n\n"
            "8. MONEDA OFICIAL Y COSTOS:\n"
            "   - Si se mencionan precios, costos de tratamiento, agroquímicos o fertilizantes, utiliza EXCLUSIVAMENTE Córdobas nicaragüenses (C$), NUNCA uses dólares estadounidenses (USD) ni el signo $ aislado sin especificar Córdobas.\n\n"
            f"CLIMA EN TIEMPO REAL ({nombre_zona}):\n{clima_actual}\n\n"
            f"BASE ENTOMOLÓGICA DE NICARAGUA:\n{info_entomologia}\n\n"
            f"GUÍA AGRONÓMICA DE CULTIVOS:\n{info_cultivos}\n\n"
            f"BASE DE ABSORCIÓN Y CURVAS NUTRICIONALES (44 CULTIVOS):\n{info_nutricion}\n\n"
            f"CATÁLOGO DE PRODUCTOS COMERCIALES LOCALES:\n{info_catalogo}\n\n"
            f"REFERENCIAS TEÓRICAS Y FITOPATOLOGÍA:\n{info_libros}\n"
        )
        
        # Redimensionar / preparar imagen si existe
        contenido_final = [imagen, mensaje_usuario] if imagen else mensaje_usuario

        config = genai.types.GenerateContentConfig(
            system_instruction=contexto_sistema,
            temperature=0.2
        )
        
        # Cascada multi-pase con backoff progresivo para resistir picos globales de saturación
        secuencia_intentos = [
            ('gemini-3.8-flash', 4),
            ('gemini-3.5-flash-lite', 5),
            ('gemini-3.1-flash-lite', 6),
            ('gemini-3.8-flash', 7),  # Segunda pasada después de esperar
            ('gemini-3.5-flash-lite', 8)
        ]
        
        ultimo_error = None
        for i, (modelo, espera) in enumerate(secuencia_intentos):
            try:
                response = self.client.models.generate_content(
                    model=modelo,
                    contents=contenido_final,
                    config=config
                )
                if response.text:
                    return _sanitizar_salida(response.text)
            except Exception as e:
                error_str = str(e).upper()
                ultimo_error = e
                logger.warning(f"Intento {i+1}/5 en {modelo} saturado ({error_str[:60]}...). Esperando {espera}s...")
                
                # Si es un error 400 por la imagen, intentar enviar solo el texto
                if "400" in error_str and imagen:
                    try:
                        resp_txt = self.client.models.generate_content(
                            model=modelo,
                            contents=mensaje_usuario,
                            config=config
                        )
                        return _sanitizar_salida("*(Nota: La imagen no pudo ser transmitida por límites de conexión, pero aquí está el análisis)*\n\n" + resp_txt.text)
                    except Exception:
                        pass
                
                time.sleep(espera)
                continue
                
        # Si después de 5 intentos (más de 30 segundos de espera) Google sigue caído:
        logger.error(f"Saturación total tras 5 intentos: {ultimo_error}")
        return (
            "⚠️ **Los servidores de Google AI Studio están experimentando una congestión temporal de tráfico global (Error 503).**\n\n"
            "El sistema intentó 5 veces de forma automática durante 30 segundos pero los servidores aún no liberan cupo. "
            "Por favor, **espera unos 20 segundos y vuelve a enviar tu pregunta** para recibir el diagnóstico y las marcas comerciales."
        )

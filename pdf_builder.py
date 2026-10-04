import os
import re
from fpdf import FPDF
from datetime import datetime

class RecetaAgronomicaPDF(FPDF):
    def __init__(self, ubicacion="Nicaragua", lote="Lote General"):
        super().__init__()
        self.ubicacion = ubicacion
        self.lote = lote

    def header(self):
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        logo_path = os.path.join(assets_dir, "logo_calabaza_glassmorphism.png")
        
        # 1. Asegurar que el logo exista en disco; si no, recrearlo desde assets_bundle
        if not os.path.exists(logo_path):
            logo_alt = os.path.join(os.path.dirname(__file__), "logo_calabaza_glassmorphism.png")
            if os.path.exists(logo_alt):
                logo_path = logo_alt
            else:
                try:
                    import assets_bundle
                    import base64
                    logo_b64 = getattr(assets_bundle, "LOGO_B64", "")
                    if logo_b64:
                        os.makedirs(assets_dir, exist_ok=True)
                        with open(logo_path, "wb") as f_img:
                            f_img.write(base64.b64decode(logo_b64))
                except Exception:
                    pass

        # 2. Marca de agua traslúcida centrada en cada hoja del PDF (logo tenue)
        wm_path = os.path.join(assets_dir, "logo_watermark.png")
        if os.path.exists(wm_path):
            try:
                self.image(wm_path, x=55, y=98, w=100, h=100)
            except Exception:
                pass
            
        # 3. Logo oficial en el encabezado de cada hoja (esquina superior izquierda)
        logo_loaded = False
        if os.path.exists(logo_path):
            try:
                self.image(logo_path, x=14, y=8, w=15, h=15)
                logo_loaded = True
            except Exception:
                pass

        if not logo_loaded:
            try:
                import assets_bundle
                import io
                import base64
                from PIL import Image
                logo_b64 = getattr(assets_bundle, "LOGO_B64", "")
                if logo_b64:
                    img = Image.open(io.BytesIO(base64.b64decode(logo_b64)))
                    self.image(img, x=14, y=8, w=15, h=15)
                    logo_loaded = True
            except Exception:
                pass
        
        # Encabezado institucional elegante
        title_x = 32 if logo_loaded else 14
        self.set_xy(title_x, 9)
        self.set_font('times', 'B', 14)
        self.set_text_color(21, 62, 32) # Verde bosque institucional #153E20
        self.cell(196 - title_x, 7, 'RECETA TÉCNICA AGRONÓMICA', align='L', new_x="LMARGIN", new_y="NEXT")
        
        self.set_xy(title_x, 16)
        self.set_font('times', 'I', 9.5)
        self.set_text_color(52, 91, 60)
        self.cell(196 - title_x, 5, 'Sistema Experto Fitosanitario & Nutrición | Nicaragua', align='L', new_x="LMARGIN", new_y="NEXT")
        
        self.set_draw_color(21, 62, 32)
        self.set_line_width(0.6)
        self.line(14, 26, 196, 26)
        self.set_y(29)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(180, 200, 180)
        self.set_line_width(0.3)
        self.line(14, self.get_y(), 196, self.get_y())
        self.set_font('times', 'I', 9)
        self.set_text_color(110, 110, 110)
        self.cell(0, 8, f'AgroAsistente Nicaragua | Documento Técnico Oficial | Página {self.page_no()}', align='C')

def limpiar_caracteres_conflictivos(texto: str) -> str:
    """Elimina emojis, signos de interrogación parásitos y normaliza caracteres a Latin-1 estricto."""
    if not texto:
        return ""

    reemplazos = {
        '₂': '2', '₃': '3', '₄': '4', '₅': '5', '₆': '6', '₁': '1', '₀': '0',
        '²': '2', '³': '3', 'º': 'o', 'ª': 'a', '°': ' grados ',
        '“': '"', '”': '"', '‘': "'", '’': "'", '–': '-', '—': '-',
        '•': '', '·': '', '…': '...', '±': '+/-', 'µ': 'u',
        '🩺': '', '🐛': '', '🌾': '', '🌱': '', '🧪': '', '☁️': '', '🌧️': '',
        '⚠️': '', '📦': '', '🎯': '', '💰': '', '💧': '', '⚖️': '', '🌿': '',
        '🎒': '', '📊': '', '📈': '', '📍': '', '✅': '', '❌': '', '✨': '',
        '🔍': '', '💡': '', '🚨': '', '🗓️': '', '⏱️': '', '☕': '', '🦗': ''
    }
    for orig, rep in reemplazos.items():
        texto = texto.replace(orig, rep)

    # Filtrar estrictamente solo caracteres en rango Latin-1 (0 a 255)
    texto_seguro = "".join(c for c in texto if ord(c) < 256 and c != '•')
    
    # Remover signos de interrogación aislados o repetidos
    texto_seguro = re.sub(r'(\?{1,4})\s*', '', texto_seguro)
    return texto_seguro

def generar_receta_pdf(diagnostico, receta_texto, lote="Lote Finca", ubicacion="Nicaragua", **kwargs):
    pdf = RecetaAgronomicaPDF(ubicacion=ubicacion, lote=lote)
    pdf.set_margins(14, 18, 14)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    
    # ── METADATOS TÉCNICOS DE LA RECETA ──────────────────────────────────────────
    fecha = datetime.now().strftime("%d/%m/%Y - %I:%M %p")
    pdf.set_fill_color(240, 245, 238) # Fondo salvia suave
    pdf.set_draw_color(176, 195, 165)
    pdf.set_line_width(0.3)
    pdf.rect(14, pdf.get_y(), 182, 18, 'DF')
    
    pdf.set_xy(18, pdf.get_y() + 2)
    pdf.set_font('times', 'B', 10)
    pdf.set_text_color(21, 62, 32)
    pdf.cell(90, 6, f"FECHA DE EMISIÓN: {fecha}", new_x="RIGHT")
    pdf.cell(90, 6, f"UBICACIÓN: {limpiar_caracteres_conflictivos(ubicacion)}", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_x(18)
    pdf.cell(90, 6, f"LOTE / ÁREA: {limpiar_caracteres_conflictivos(lote)}", new_x="RIGHT")
    pdf.cell(90, 6, "VALIDEZ TÉCNICA: Aplicación inmediata recomendada", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)

    # ── PROCESAMIENTO LIMPIO LÍNEA POR LÍNEA ─────────────────────────────────────
    lineas = receta_texto.split('\n')
    
    for raw_line in lineas:
        line = raw_line.strip()
        if not line:
            pdf.ln(2)
            continue
            
        # 1. Separadores horizontales (--- o ___) -> Línea gráfica limpia
        if re.match(r'^[-*_]{3,}$', line):
            pdf.ln(2)
            pdf.set_draw_color(176, 195, 165)
            pdf.set_line_width(0.4)
            pdf.line(14, pdf.get_y(), 196, pdf.get_y())
            pdf.ln(3)
            continue
            
        # 2. Títulos y Encabezados (líneas que empiezan con # o números como "1. DIAGNÓSTICO" o están en negrita completa)
        es_encabezado_hash = bool(re.match(r'^#{1,6}\s*', line))
        es_linea_negrita_completa = bool(re.match(r'^\*\*(.*?)\*\*$', line))
        es_seccion_numerada = bool(re.match(r'^\d+\.\s+[A-ZÁÉÍÓÚÑ\s]{4,}$', line))
        
        if es_encabezado_hash or es_linea_negrita_completa or es_seccion_numerada:
            # Limpiar marcas de formato markdown (#, *, ?, -)
            titulo_limpio = re.sub(r'^#{1,6}\s*', '', line)
            titulo_limpio = re.sub(r'^\d+\.\s*', '', titulo_limpio)
            titulo_limpio = re.sub(r'\*+', '', titulo_limpio)
            titulo_limpio = re.sub(r'^\?+\s*', '', titulo_limpio).strip()
            titulo_limpio = limpiar_caracteres_conflictivos(titulo_limpio)
            
            if titulo_limpio:
                pdf.ln(3)
                # TÍTULO: Times New Roman, tamaño 13, negrita
                pdf.set_font('times', 'B', 13)
                pdf.set_text_color(21, 62, 32)
                pdf.set_x(14)
                pdf.multi_cell(0, 6.5, titulo_limpio.upper(), new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            continue
            
        # 3. Elementos de lista / Viñetas (líneas que empiezan con *, -, o números)
        es_lista = bool(re.match(r'^[-*+]\s+', line))
        es_item_numerado = bool(re.match(r'^\d+[\.\)]\s+', line))
        
        if es_lista or es_item_numerado:
            # Limpiar viñeta inicial (* o -) y asteriscos de negrita
            item_limpio = re.sub(r'^[-*+]\s+', '', line)
            item_limpio = re.sub(r'^\d+[\.\)]\s+', '', item_limpio)
            item_limpio = re.sub(r'\*\*(.*?)\*\*', r'\1', item_limpio)
            item_limpio = re.sub(r'\*(.*?)\*', r'\1', item_limpio)
            item_limpio = re.sub(r'^\?+\s*', '', item_limpio).strip()
            item_limpio = limpiar_caracteres_conflictivos(item_limpio)
            
            if item_limpio:
                # PÁRRAFO: Times New Roman, tamaño 12, regular con sangría limpia (sin * ni -)
                pdf.set_font('times', '', 12)
                pdf.set_text_color(20, 20, 20)
                pdf.set_x(20)
                pdf.multi_cell(176, 5.8, item_limpio, new_x="LMARGIN", new_y="NEXT")
                pdf.ln(1)
            continue
            
        # 4. Párrafos normales de texto
        parrafo_limpio = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        parrafo_limpio = re.sub(r'\*(.*?)\*', r'\1', parrafo_limpio)
        parrafo_limpio = re.sub(r'^\?+\s*', '', parrafo_limpio).strip()
        parrafo_limpio = limpiar_caracteres_conflictivos(parrafo_limpio)
        
        if parrafo_limpio:
            # PÁRRAFO: Times New Roman, tamaño 12, regular
            pdf.set_font('times', '', 12)
            pdf.set_text_color(20, 20, 20)
            pdf.set_x(14)
            pdf.multi_cell(182, 5.8, parrafo_limpio, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1.5)

    # ── GUARDAR PDF TÉCNICO OFICIAL ─────────────────────────────────────────────
    ruta_salida = os.path.join(os.path.dirname(__file__), "Receta_Agronomica_Generada.pdf")
    pdf.output(ruta_salida)
    
    return ruta_salida

# Alias para compatibilidad
generar_pdf_receta = generar_receta_pdf


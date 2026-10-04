import streamlit as st
import json
import os
import base64
from PIL import Image
from rag_engine import AsistenteFitosanitario


# Cargar icono de pestaña y logo de vidrio esmerilado translúcido
import io

dir_actual = os.path.dirname(__file__)
icon_img = "🎃"
try:
    import assets_bundle
    icon_b64 = getattr(assets_bundle, "ICON_B64", "")
    if icon_b64:
        icon_img = Image.open(io.BytesIO(base64.b64decode(icon_b64)))
except Exception:
    pass

if icon_img == "🎃":
    for p in ["logo_calabaza_icon.png", os.path.join(dir_actual, "logo_calabaza_icon.png"), os.path.join(dir_actual, "assets", "logo_calabaza_icon.png")]:
        if os.path.exists(p):
            try:
                icon_img = Image.open(p)
                break
            except Exception:
                pass

# Configuración de página
st.set_page_config(
    page_title="AgroAsistente • Inteligencia Agronómica",
    page_icon=icon_img,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Blindaje contra extensiones de traducción de navegadores que rompen React DOM (removeChild)
import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    function protectDOM() {
        try {
            const p = window.parent.document;
            if (!p) return;
            p.documentElement.setAttribute('translate', 'no');
            p.documentElement.classList.add('notranslate');
            p.documentElement.setAttribute('data-theme', 'light');
            p.documentElement.style.colorScheme = 'light';
            if (p.body) {
                p.body.setAttribute('translate', 'no');
                p.body.classList.add('notranslate');
                p.body.style.colorScheme = 'light';
            }
            if (!p.querySelector('meta[name="google"][content="notranslate"]')) {
                const meta = p.createElement('meta');
                meta.name = 'google';
                meta.content = 'notranslate';
                p.head.appendChild(meta);
            }
            let st = p.getElementById('agro-universal-light');
            if (!st) {
                st = p.createElement('style');
                st.id = 'agro-universal-light';
                p.head.appendChild(st);
            }
            st.textContent = `
                :root, html, body, .stApp, section[data-testid="stSidebar"], [data-testid="stSidebar"] {
                    color-scheme: light !important;
                    --background-color: #EEF4EB !important;
                    --secondary-background-color: #FFFFFF !important;
                    --text-color: #0A2211 !important;
                    --primary-color: #153E20 !important;
                }
                /* Selectbox: sin contenedor exterior con borde, solo el control box interno */
                [data-testid="stSelectbox"],
                [data-testid="stSelectbox"] > div {
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }
                [data-testid="stSelectbox"] [class*="e1fp86qc0"],
                [data-testid="stSelectbox"] > div:last-child > div,
                [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
                    background-color: #FFFFFF !important;
                    background: #FFFFFF !important;
                    border: 1.5px solid rgba(21, 62, 32, 0.32) !important;
                    border-radius: 14px !important;
                    box-shadow: 0 2px 6px rgba(20, 50, 30, 0.05) !important;
                    min-height: 44px !important;
                    color: #0A2211 !important;
                }
                /* Interior del selectbox: plano, sin cajas secundarias ni bordes anidados */
                [data-testid="stSelectbox"] input,
                [data-testid="stSelectbox"] button,
                [data-testid="stSelectbox"] [class*="e1fp86qc1"],
                [data-testid="stSelectbox"] [class*="e1fp86qc2"],
                [data-testid="stSelectbox"] [class*="e1fp86qc3"],
                [data-testid="stSelectbox"] span,
                [data-testid="stSelectbox"] div[role="combobox"],
                [data-testid="stSelectbox"] svg {
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                    outline: none !important;
                    color: #0A2211 !important;
                    -webkit-text-fill-color: #0A2211 !important;
                }
                [data-testid="stSelectbox"] svg {
                    fill: #153E20 !important;
                    stroke: #153E20 !important;
                    color: #153E20 !important;
                }
                /* TextInput: caja unica tipo píldora */
                [data-testid="stTextInput"],
                [data-testid="stTextInput"] > div {
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                }
                [data-testid="stTextInputRootElement"],
                div[data-baseweb="input"] {
                    background-color: #FFFFFF !important;
                    background: #FFFFFF !important;
                    border: 1.5px solid rgba(21, 62, 32, 0.32) !important;
                    border-radius: 9999px !important;
                    box-shadow: 0 2px 6px rgba(20, 50, 30, 0.05) !important;
                }
                [data-testid="stTextInputField"],
                [data-testid="stTextInputRootElement"] input {
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                    color: #0A2211 !important;
                    -webkit-text-fill-color: #0A2211 !important;
                }
                [data-testid="stTextInputRootElement"] button,
                button[aria-label*="password"],
                button[aria-label*="Password"] {
                    background-color: #DCEDDA !important;
                    background: #DCEDDA !important;
                    color: #153E20 !important;
                    border: none !important;
                    border-radius: 9999px !important;
                }
                [data-testid="stTextInputRootElement"] button svg,
                button[aria-label*="password"] svg,
                button[aria-label*="Password"] svg {
                    fill: #153E20 !important;
                    stroke: #153E20 !important;
                    color: #153E20 !important;
                    border: none !important;
                }
                [data-testid="stSelectboxVirtualDropdown"],
                [data-testid="stSelectboxVirtualDropdown"] > div,
                [data-testid="stSelectboxVirtualDropdown"] [class*="e1fp86qc4"],
                div[data-baseweb="popover"],
                div[data-baseweb="menu"] {
                    background-color: #FFFFFF !important;
                    background: #FFFFFF !important;
                    border: 1.5px solid rgba(21, 62, 32, 0.28) !important;
                    border-radius: 16px !important;
                    box-shadow: 0 16px 40px rgba(20, 50, 30, 0.16) !important;
                    color: #0A2211 !important;
                }
            `;
        } catch (e) {}
    }
    protectDOM();
    setInterval(protectDOM, 500);
})();
</script>
""", height=0, width=0)

# Helper para cargar archivos en base64 con invalidación por mtime
def get_base64_file(filename_or_path):
    if os.path.isabs(filename_or_path) and os.path.exists(filename_or_path):
        path = filename_or_path
    else:
        path = os.path.join(os.path.dirname(__file__), "assets", filename_or_path)
    if os.path.exists(path):
        mtime = os.path.getmtime(path)
        return _get_base64_file_cached(path, mtime)
    return ""

@st.cache_data
def _get_base64_file_cached(path, mtime):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

# Sincronización y respaldo de fondos
assets_harvest_bg = os.path.join(dir_actual, "assets", "background_harvest.png")
assets_backup_bg = os.path.join(dir_actual, "assets", "background_harvest_backup.png")
assets_campo_bg = os.path.join(dir_actual, "assets", "background_campo_maiz.jpg")

try:
    import assets_bundle
    logo_glass_b64 = getattr(assets_bundle, "LOGO_B64", "")
    bg_campo_b64 = getattr(assets_bundle, "BG_B64", "")
except Exception:
    logo_glass_b64 = ""
    bg_campo_b64 = ""

if not logo_glass_b64:
    logo_glass_b64 = get_base64_file("logo_calabaza_glassmorphism.png")

if not bg_campo_b64:
    bg_campo_b64 = get_base64_file("background_campo_maiz.jpg")
    if not bg_campo_b64:
        bg_campo_b64 = get_base64_file("background_harvest.png")

# ── CSS PREMIUM: APPLE GLASSMORPHISM TRANSLÚCIDO & ESTÉTICA BOTÁNICA #B0C3A5 ──
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..800;1,400..800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {{
        --color-theme: #B0C3A5;
        --color-theme-dark: #92AA86;
        --color-theme-soft: #DDE7D7;
        --color-theme-light: #EEF4EB;
        --text-primary: #0A2211;
        --text-secondary: #183C21;
        --text-muted: #345B3C;
        --accent-emerald: #153E20;
        --glass-card-bg: rgba(255, 255, 255, 0.80);
        --glass-card-border: rgba(255, 255, 255, 0.94);
        --glass-card-shadow: 0 16px 40px rgba(20, 48, 26, 0.10);
    }}

    *, *::before, *::after {{
        box-sizing: border-box !important;
        overflow-wrap: break-word;
        word-wrap: break-word;
    }}

    /* Fondo global con fotografía de maizal y velo orgánico armonizado en tono #B0C3A5 */
    .stApp {{
        background: 
            linear-gradient(180deg, rgba(235, 243, 230, 0.46) 0%, rgba(176, 195, 165, 0.38) 50%, rgba(195, 212, 185, 0.48) 100%),
            url('data:image/jpeg;base64,{bg_campo_b64}') center center / cover no-repeat fixed !important;
        color: #0A2211 !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        translate: no !important;
    }}

    /* Contenedor principal con efecto de difusión óptica (blur) para máxima legibilidad */
    .block-container {{
        backdrop-filter: blur(8px) saturate(135%);
        -webkit-backdrop-filter: blur(8px) saturate(135%);
        padding-top: 2rem !important;
        padding-bottom: 8rem !important;
    }}

    /* Ocultar barra superior nativa */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Tipografía editorial de alto contraste con sombreado de relieve */
    h1, h2, h3, h4, h5, h6, .serif-font {{
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #0A2211 !important;
        letter-spacing: 0.2px;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9), 0 3px 10px rgba(10, 34, 17, 0.20) !important;
    }}

    p, li, label, span {{
        color: #0E2916;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.7);
    }}

    /* Subtítulos y captions con nitidez garantizada */
    .stCaption, [data-testid="stCaptionContainer"] p {{
        color: #1B4D27 !important;
        font-size: 0.94rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9) !important;
    }}

    /* Sombreado y tipografía específica para la barra lateral #DCEDDA */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] li, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {{
        color: #0A2211 !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}

    [data-testid="stSidebar"] strong {{
        color: #051A0B !important;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9) !important;
    }}

    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {{
        color: #0A2211 !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9), 0 2px 8px rgba(10, 34, 17, 0.20) !important;
    }}

    /* Tarjeta cabecera de sección con cristal esmerilado translúcido */
    .section-header-card {{
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-top: 2px solid #FFFFFF;
        border-radius: 26px;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        padding: 20px 28px;
        margin-bottom: 20px;
        box-shadow: 0 14px 35px rgba(20, 50, 30, 0.10), inset 0 1px 2px rgba(255, 255, 255, 1);
    }}

    /* Títulos de sección con corchetes botánicos */
    .section-bracket {{
        display: inline-flex;
        align-items: center;
        gap: 12px;
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #0A2211 !important;
        margin: 0 0 6px 0;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9), 0 3px 10px rgba(10, 34, 17, 0.22) !important;
    }}
    .section-bracket .bracket {{
        color: #1B4D27 !important;
        font-size: 1.85rem;
        font-weight: 400;
        text-shadow: 0 1px 3px rgba(255, 255, 255, 0.9);
    }}

    /* Hero Banner: Glassmorphism translúcido con navbar integrada */
    .plantfashion-hero {{
        background: rgba(255, 255, 255, 0.78);
        backdrop-filter: blur(35px) saturate(180%);
        -webkit-backdrop-filter: blur(35px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-top: 2px solid #FFFFFF;
        border-radius: 36px;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        padding: 30px 40px;
        margin-bottom: 26px;
        box-shadow: 0 20px 50px rgba(20, 50, 30, 0.16), inset 0 1px 2px rgba(255, 255, 255, 1);
        position: relative;
        overflow: hidden;
    }}
    .plantfashion-hero::after {{
        content: '';
        position: absolute;
        top: 0;
        left: 40px;
        right: 40px;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.95), transparent);
    }}
    .pf-navbar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        margin-bottom: 24px;
        padding-bottom: 16px;
        border-bottom: 1px solid rgba(46, 84, 56, 0.14);
    }}
    .pf-brand {{
        display: flex;
        align-items: center;
        gap: 14px;
        flex-shrink: 0;
        margin-right: auto;
    }}
    .pf-logo-img {{
        width: 52px;
        height: 52px;
        flex-shrink: 0;
        filter: drop-shadow(0 6px 14px rgba(16, 45, 25, 0.28)) drop-shadow(0 2px 4px rgba(16, 45, 25, 0.15));
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), filter 0.35s ease;
    }}
    .pf-logo-img:hover {{
        transform: scale(1.10) rotate(2deg);
        filter: drop-shadow(0 10px 22px rgba(16, 45, 25, 0.38)) drop-shadow(0 4px 8px rgba(16, 45, 25, 0.20));
    }}
    .pf-title {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #102B19 !important;
        letter-spacing: 0.6px;
        white-space: nowrap;
        text-shadow: 0 3px 10px rgba(16, 45, 25, 0.35), 0 1px 3px rgba(0, 0, 0, 0.20) !important;
    }}
    .pf-links {{
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        align-items: center;
        justify-content: flex-end;
    }}
    .pf-pill-link {{
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1.5px solid rgba(255, 255, 255, 0.95);
        padding: 6px 14px;
        border-radius: 9999px;
        font-size: 0.80rem;
        color: #153E20 !important;
        font-weight: 600;
        white-space: nowrap;
        box-shadow: 0 4px 14px rgba(20, 50, 30, 0.10);
        text-shadow: 0 1px 4px rgba(16, 45, 25, 0.22);
    }}
    .pf-headline {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2.85rem;
        font-weight: 700;
        color: #0E2916 !important;
        line-height: 1.15;
        margin: 0 0 12px 0;
        max-width: 740px;
        text-shadow: 0 4px 16px rgba(16, 45, 25, 0.38), 0 1px 4px rgba(0, 0, 0, 0.22) !important;
    }}
    .pf-subhead {{
        font-size: 1.05rem;
        color: #2D5837 !important;
        line-height: 1.55;
        max-width: 660px;
        margin-bottom: 20px;
        text-shadow: 0 2px 8px rgba(16, 45, 25, 0.25) !important;
    }}
    .pf-btn-badge {{
        display: inline-block;
        background: #153E20;
        color: #EEF4EB !important;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 9px 24px;
        border-radius: 9999px;
        box-shadow: 0 8px 24px rgba(21, 62, 32, 0.30);
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.45) !important;
    }}

    /* Tarjetas Glassmorphism translúcidas */
    .agro-card {{
        background: rgba(255, 255, 255, 0.82);
        backdrop-filter: blur(32px) saturate(180%);
        -webkit-backdrop-filter: blur(32px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-top: 2px solid #FFFFFF;
        border-radius: 26px;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        padding: 22px 26px !important;
        margin-bottom: 20px;
        box-shadow: 0 16px 40px rgba(20, 50, 30, 0.12), inset 0 1px 2px rgba(255, 255, 255, 1);
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
    }}
    .agro-card:hover {{
        background: rgba(255, 255, 255, 0.92);
        border-color: #FFFFFF;
        transform: translateY(-2px);
        box-shadow: 0 22px 50px rgba(20, 50, 30, 0.18), inset 0 1px 2px rgba(255, 255, 255, 1);
    }}
    .agro-card h1, .agro-card h2, .agro-card h3, .agro-card h4, .agro-card h5, .agro-card h6 {{
        color: #102B19 !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 8px rgba(16, 45, 25, 0.30), 0 1px 2px rgba(0, 0, 0, 0.15) !important;
    }}
    .agro-card p, .agro-card li {{
        color: #15381F !important;
        text-shadow: 0 1px 4px rgba(16, 45, 25, 0.20) !important;
    }}
    .agro-card strong {{
        color: #0E2916 !important;
        text-shadow: 0 2px 6px rgba(16, 45, 25, 0.28) !important;
    }}

    /* Barra lateral translúcida en tono #B0C3A5 con vidrio esmerilado */
    [data-testid="stSidebar"] {{
        background-color: rgba(176, 195, 165, 0.90) !important;
        background: linear-gradient(180deg, rgba(186, 204, 175, 0.92) 0%, rgba(166, 187, 154, 0.94) 100%) !important;
        backdrop-filter: blur(40px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(40px) saturate(180%) !important;
        border-right: 1.5px solid rgba(255, 255, 255, 0.80) !important;
        box-shadow: 6px 0 25px rgba(20, 50, 30, 0.12) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #0A2211 !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label, 
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {{
        color: #0A2211 !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] hr {{
        border-color: rgba(21, 62, 32, 0.20) !important;
    }}

    /* Blindaje limpio y estilizado para controles en la barra lateral (sin dobles bordes) */
    [data-testid="stSidebar"] [data-testid="stSelectbox"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div,
    [data-testid="stSidebar"] [data-testid="stTextInput"],
    [data-testid="stSidebar"] [data-testid="stTextInput"] > div {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="e1fp86qc0"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] > div:last-child > div,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.32) !important;
        border-radius: 14px !important;
        padding: 6px 14px !important;
        min-height: 44px !important;
        box-shadow: 0 2px 6px rgba(20, 50, 30, 0.05) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSelectbox"] input,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] button,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="e1fp86qc1"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="e1fp86qc2"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] [class*="e1fp86qc3"],
    [data-testid="stSidebar"] [data-testid="stSelectbox"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[role="combobox"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSelectbox"] svg,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] button svg {{
        fill: #153E20 !important;
        stroke: #153E20 !important;
        color: #153E20 !important;
        border: none !important;
    }}
    [data-testid="stSidebar"] [data-testid="stTextInputRootElement"],
    [data-testid="stSidebar"] div[data-baseweb="input"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.32) !important;
        border-radius: 9999px !important;
        padding: 2px 14px !important;
        box-shadow: 0 2px 6px rgba(20, 50, 30, 0.05) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stTextInputField"],
    [data-testid="stSidebar"] [data-testid="stTextInputRootElement"] input {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stTextInputRootElement"] button,
    [data-testid="stSidebar"] button[aria-label*="password"],
    [data-testid="stSidebar"] button[aria-label*="Password"] {{
        background-color: #DCEDDA !important;
        background: #DCEDDA !important;
        color: #153E20 !important;
        border: none !important;
        border-radius: 9999px !important;
    }}
    [data-testid="stSidebar"] [data-testid="stTextInputRootElement"] button svg,
    [data-testid="stSidebar"] button[aria-label*="password"] svg,
    [data-testid="stSidebar"] button[aria-label*="Password"] svg {{
        fill: #153E20 !important;
        stroke: #153E20 !important;
        color: #153E20 !important;
        border: none !important;
    }}

    /* Pestañas estilo Dock Apple Glass Pills:
       Ultra redondeadas (capsule/pill 9999px), sin bordes rectangulares al activarse */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(36px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(36px) saturate(180%) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.95) !important;
        border-top: 2px solid #FFFFFF !important;
        border-radius: 9999px !important;
        padding: 8px 14px !important;
        gap: 10px !important;
        box-shadow: 0 12px 36px rgba(20, 50, 30, 0.12), inset 0 1px 2px rgba(255, 255, 255, 1) !important;
        margin-bottom: 24px !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        flex-wrap: nowrap !important;
        scrollbar-width: thin !important;
        max-width: 100% !important;
    }}
    .stTabs [data-baseweb="tab"],
    .stTabs button[role="tab"] {{
        background: rgba(176, 195, 165, 0.40) !important;
        border-radius: 9999px !important;
        color: #0E2E16 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 10px 24px !important;
        border: 1.5px solid rgba(21, 62, 32, 0.22) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.9) !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }}
    .stTabs [data-baseweb="tab"]:hover,
    .stTabs button[role="tab"]:hover {{
        background: rgba(255, 255, 255, 0.98) !important;
        color: #061A0C !important;
        border-color: #153E20 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(21, 62, 32, 0.16) !important;
        border-radius: 9999px !important;
    }}
    .stTabs [aria-selected="true"],
    .stTabs button[role="tab"][aria-selected="true"] {{
        background: #FFFFFF !important;
        color: #061A0C !important;
        font-weight: 700 !important;
        border: 2.5px solid #153E20 !important;
        border-radius: 9999px !important;
        box-shadow: 0 6px 22px rgba(21, 62, 32, 0.22), inset 0 1px 2px #FFFFFF !important;
        transform: translateY(-1px) !important;
    }}
    .stTabs [data-baseweb="tab"] > div,
    .stTabs button[role="tab"] > div {{
        border-radius: 9999px !important;
    }}
    .stTabs [data-baseweb="tab-border"],
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none !important;
    }}

    /* Botones de vidrio translúcido con armonía cromática y forma redondeada pill */
    .stButton>button {{
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        color: #0B2914 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        border-radius: 9999px !important;
        border: 1.5px solid rgba(21, 62, 32, 0.28) !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 14px rgba(20, 50, 30, 0.08), inset 0 1px 2px rgba(255, 255, 255, 1) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}
    .stButton>button:hover {{
        background: #FFFFFF !important;
        border-color: #153E20 !important;
        border-radius: 9999px !important;
        box-shadow: 0 8px 24px rgba(21, 62, 32, 0.22), inset 0 1px 2px rgba(255, 255, 255, 1) !important;
        transform: translateY(-2px) scale(1.02) !important;
        color: #031407 !important;
    }}

    /* Botón de descarga de receta en PDF: Tono Botánico #B0C3A5 */
    .stDownloadButton > button {{
        background-color: #B0C3A5 !important;
        background: linear-gradient(135deg, #B8CCA9 0%, #9EB593 100%) !important;
        color: #0A2211 !important;
        border-radius: 9999px !important;
        padding: 12px 32px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        border: 1.5px solid rgba(21, 62, 32, 0.30) !important;
        border-top: 2px solid rgba(255, 255, 255, 0.85) !important;
        box-shadow: 0 8px 24px rgba(20, 50, 30, 0.14), inset 0 1px 2px rgba(255, 255, 255, 0.80) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        white-space: nowrap !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.85) !important;
        cursor: pointer !important;
    }}
    .stDownloadButton > button:hover {{
        background-color: #C2D6B3 !important;
        background: linear-gradient(135deg, #C5D9B6 0%, #B0C3A5 100%) !important;
        color: #051A0B !important;
        transform: translateY(-2px) scale(1.02) !important;
        border-color: #153E20 !important;
        box-shadow: 0 14px 32px rgba(21, 62, 32, 0.22), inset 0 1px 2px #FFFFFF !important;
    }}
    .stDownloadButton > button:active {{
        transform: translateY(0px) scale(0.99) !important;
        box-shadow: 0 4px 14px rgba(21, 62, 32, 0.16) !important;
    }}

    /* Mensajes del chat con forma de burbuja redondeada */
    .stChatMessage, [data-testid="stChatMessage"] {{
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        border-radius: 28px !important;
        padding: 18px 24px !important;
        margin-bottom: 16px !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        box-shadow: 0 12px 30px rgba(30, 65, 40, 0.08), inset 0 1px 1px rgba(255, 255, 255, 1) !important;
    }}
    .stChatMessage p, [data-testid="stChatMessage"] p,
    .stChatMessage div, [data-testid="stChatMessage"] div {{
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}
    .stChatMessage[data-testid="chat-message-user"],
    [data-testid="stChatMessage"][data-testid="chat-message-user"] {{
        background: rgba(255, 255, 255, 0.95) !important;
        border: 1.5px solid rgba(21, 62, 32, 0.28) !important;
        color: #0A2211 !important;
        border-radius: 28px 28px 10px 28px !important;
    }}
    .stChatMessage[data-testid="chat-message-assistant"],
    [data-testid="stChatMessage"][data-testid="chat-message-assistant"] {{
        background: rgba(255, 255, 255, 0.90) !important;
        border: 1.5px solid rgba(255, 255, 255, 0.96) !important;
        color: #0A2211 !important;
        border-radius: 28px 28px 28px 10px !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════════
       BURBUJAS DE TEXTO Y CONTROLES ULTRA-REDONDEADOS (CAPSULE / PILL SHAPE)
       ═══════════════════════════════════════════════════════════════════════════ */

    /* 1. Chat Input: Cápsula continua ultra redondeada */
    [data-testid="stChatInput"] {{
        background: transparent !important;
    }}
    [data-testid="stChatInput"] > div {{
        background: rgba(255, 255, 255, 0.96) !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1.5px solid rgba(21, 62, 32, 0.35) !important;
        border-radius: 9999px !important;
        padding: 4px 16px !important;
        box-shadow: 0 10px 30px rgba(20, 50, 30, 0.12), inset 0 1px 2px #FFFFFF !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stChatInput"] > div:focus-within {{
        border-color: #153E20 !important;
        border-radius: 9999px !important;
        box-shadow: 0 12px 36px rgba(21, 62, 32, 0.24), inset 0 1px 2px #FFFFFF !important;
    }}
    [data-testid="stChatInput"] textarea {{
        background: transparent !important;
        color: #0A2211 !important;
        font-size: 0.96rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: #2D5837 !important;
        opacity: 0.85 !important;
    }}
    [data-testid="stChatInput"] button {{
        background: #153E20 !important;
        color: #EEF4EB !important;
        border-radius: 50% !important;
        border: none !important;
        transition: transform 0.2s ease, background 0.2s ease !important;
    }}
    [data-testid="stChatInput"] button:hover {{
        background: #0B2513 !important;
        transform: scale(1.08) !important;
    }}
    [data-testid="stChatInput"] button svg {{
        fill: #EEF4EB !important;
    }}
    [data-testid="stBottom"] {{
        background: linear-gradient(180deg, rgba(235, 243, 230, 0) 0%, rgba(235, 243, 230, 0.88) 32%, rgba(235, 243, 230, 0.98) 100%) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding-bottom: 14px !important;
        padding-top: 10px !important;
    }}
    [data-testid="stBottom"] > div {{
        background: transparent !important;
    }}

    /* 2. Subida de Archivos (File Uploader): Panel blanco cristal con bordes redondeados */
    [data-testid="stFileUploader"] {{
        background: transparent !important;
    }}
    [data-testid="stFileUploader"] section {{
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border: 1.5px dashed rgba(21, 62, 32, 0.40) !important;
        border-radius: 26px !important;
        padding: 16px 20px !important;
        box-shadow: 0 8px 24px rgba(20, 50, 30, 0.08), inset 0 1px 2px #FFFFFF !important;
        transition: all 0.3s ease !important;
    }}
    [data-testid="stFileUploader"] section:hover {{
        border-color: #153E20 !important;
        background: #FFFFFF !important;
        box-shadow: 0 12px 30px rgba(21, 62, 32, 0.16) !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: #0E2916 !important;
    }}
    /* Botón de subida estilizado con cristal esmeralda luminoso (Apple Glass Pill) */
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"],
    [data-testid="stFileUploader"] button {{
        background: linear-gradient(180deg, #FFFFFF 0%, #EEF5EC 100%) !important;
        color: #153E20 !important;
        border: 1.5px solid rgba(21, 62, 32, 0.40) !important;
        border-radius: 9999px !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        padding: 9px 24px !important;
        box-shadow: 0 4px 14px rgba(20, 50, 30, 0.08), inset 0 1px 2px #FFFFFF !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        text-shadow: none !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
    }}
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"] *,
    [data-testid="stFileUploader"] button * {{
        color: #153E20 !important;
        fill: #153E20 !important;
        stroke: #153E20 !important;
        text-shadow: none !important;
        font-weight: 700 !important;
    }}
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"]:hover,
    [data-testid="stFileUploader"] button:hover {{
        background: linear-gradient(135deg, #1E5128 0%, #153E20 100%) !important;
        color: #FFFFFF !important;
        border-color: #153E20 !important;
        transform: translateY(-2px) scale(1.03) !important;
        box-shadow: 0 8px 24px rgba(21, 62, 32, 0.28), inset 0 1px 1px rgba(255, 255, 255, 0.3) !important;
    }}
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"]:hover *,
    [data-testid="stFileUploader"] button:hover * {{
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
        text-shadow: none !important;
    }}
    [data-testid="stFileUploader"] small, 
    [data-testid="stFileUploaderDropzoneInstructions"] {{
        color: #244C2E !important;
        font-size: 0.84rem !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}

    /* 3. Inputs de Texto, Contraseñas (API Key) y Búsqueda */
    [data-testid="stTextInput"],
    .stTextInput {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-bottom: 12px !important;
    }}
    [data-testid="stTextInput"] label,
    .stTextInput label,
    [data-testid="stTextInput"] [data-testid="stWidgetLabel"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #0A2211 !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        margin-bottom: 6px !important;
        padding: 0 !important;
        display: inline-block !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}
    [data-testid="stTextInputRootElement"],
    div[data-baseweb="input"],
    div[data-baseweb="base-input"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border: 1.5px solid rgba(21, 62, 32, 0.35) !important;
        border-radius: 9999px !important;
        padding: 2px 14px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04), 0 3px 10px rgba(30, 65, 40, 0.06) !important;
        box-sizing: border-box !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}
    [data-testid="stTextInputRootElement"]:focus-within,
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within {{
        border-color: #153E20 !important;
        border-radius: 9999px !important;
        box-shadow: 0 0 16px rgba(21, 62, 32, 0.28), inset 0 1px 2px #FFFFFF !important;
    }}
    [data-testid="stTextInputRootElement"] input,
    [data-testid="stTextInputField"],
    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    .stTextInput input {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        padding: 8px 6px !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       BLINDAJE PERMANENTE CONTRA MODO OSCURO (BOTÁNICO ELEGANTE #B0C3A5)
       ═══════════════════════════════════════════════════════════════════════ */
    :root, html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stHeader"] {{
        color-scheme: light !important;
    }}

    @media (prefers-color-scheme: dark) {{
        :root, html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], [data-testid="stHeader"] {{
            color-scheme: light !important;
        }}
    }}

    [data-theme="dark"],
    .dark,
    [data-testid="stAppViewContainer"][data-theme="dark"] {{
        color-scheme: light !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       DESPLEGABLES / SELECTBOXES (AUDITORÍA UI/UX CORREGIDA)
       ═══════════════════════════════════════════════════════════════════════ */

    /* 1. Contenedor padre de Selectbox: 100% transparente y limpio, sin recuadros exteriores */
    [data-testid="stSelectbox"],
    [data-testid="stSelectbox"] > div,
    [data-testid="stSelectbox"] > div:first-child,
    [data-testid="stSelectbox"] > div:last-child,
    .stSelectbox,
    .stSelectbox > div {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 0 !important;
    }}

    /* 2. Etiqueta / Label del Selectbox: Texto limpio botánico sin píldora ni fondo */
    [data-testid="stSelectbox"] label,
    [data-testid="stSelectbox"] [data-testid="stWidgetLabel"],
    [data-testid="stSelectbox"] label p,
    .stSelectbox label,
    .stSelectbox [data-testid="stWidgetLabel"],
    .stSelectbox label p {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        margin-bottom: 6px !important;
        padding: 0 !important;
        display: inline-block !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}

    /* 3. Contenedor del selector: UNA SOLA CAJA ELEGANTE, sin bordes dobles ni anidaciones */
    [data-testid="stSelectbox"] [class*="e1fp86qc0"],
    [data-testid="stSelectbox"] > div:last-child > div,
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.32) !important;
        border-radius: 14px !important;
        padding: 6px 14px !important;
        min-height: 44px !important;
        color: #0A2211 !important;
        box-shadow: 0 2px 6px rgba(20, 50, 30, 0.05) !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease, background 0.25s ease !important;
        cursor: pointer !important;
        box-sizing: border-box !important;
    }}

    [data-testid="stSelectbox"] [class*="e1fp86qc0"]:hover,
    [data-testid="stSelectbox"] > div:last-child > div:hover,
    div[data-baseweb="select"] > div:hover {{
        border-color: #153E20 !important;
        background: #FDFEFC !important;
        box-shadow: 0 4px 14px rgba(21, 62, 32, 0.14) !important;
    }}

    [data-testid="stSelectbox"]:focus-within [class*="e1fp86qc0"],
    [data-testid="stSelectbox"]:focus-within > div:last-child > div,
    div[data-baseweb="select"]:focus-within > div {{
        border-color: #153E20 !important;
        border-radius: 14px !important;
        box-shadow: 0 0 0 2px rgba(21, 62, 32, 0.20), 0 4px 16px rgba(21, 62, 32, 0.12) !important;
        background: #FFFFFF !important;
    }}

    /* 4. Elementos internos del selector: 100% transparentes y sin bordes */
    [data-testid="stSelectbox"] input,
    [data-testid="stSelectbox"] button,
    [data-testid="stSelectbox"] [class*="e1fp86qc1"],
    [data-testid="stSelectbox"] [class*="e1fp86qc2"],
    [data-testid="stSelectbox"] [class*="e1fp86qc3"],
    [data-testid="stSelectbox"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSelectbox"] span,
    [data-testid="stSelectbox"] div[aria-selected],
    [data-testid="stSelectbox"] div[role="combobox"],
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div[role="combobox"] {{
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        white-space: nowrap !important;
        background: transparent !important;
        background-color: transparent !important;
        box-sizing: border-box !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }}

    /* 5. Flecha / Icono SVG del desplegable (limpio, sin caja alrededor) */
    [data-testid="stSelectbox"] svg,
    [data-testid="stSelectbox"] button svg,
    div[data-baseweb="select"] svg {{
        fill: #153E20 !important;
        stroke: #153E20 !important;
        color: #153E20 !important;
        border: none !important;
        box-shadow: none !important;
        background: transparent !important;
        flex-shrink: 0 !important;
        transition: transform 0.2s ease !important;
    }}

    /* Soporte MultiSelect */
    [data-testid="stMultiSelect"] {{
        background: transparent !important;
        border: none !important;
    }}
    [data-testid="stMultiSelect"] label {{
        background: transparent !important;
        margin-bottom: 6px !important;
        color: #0A2211 !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMultiSelect"] div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.35) !important;
        border-radius: 14px !important;
        padding: 6px 14px !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       CAMPOS NUMÉRICOS (NUMBER INPUT) Y BOTONES + / -
       ═══════════════════════════════════════════════════════════════════════ */
    [data-testid="stNumberInput"],
    .stNumberInput {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-bottom: 10px !important;
    }}
    [data-testid="stNumberInput"] label,
    .stNumberInput label {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #0A2211 !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        margin-bottom: 6px !important;
        padding: 0 !important;
        display: inline-block !important;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8) !important;
    }}
    [data-testid="stNumberInputContainer"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.35) !important;
        border-radius: 9999px !important;
        padding: 2px 4px 2px 14px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04), 0 3px 10px rgba(30, 65, 40, 0.06) !important;
        box-sizing: border-box !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}
    [data-testid="stNumberInputContainer"]:focus-within {{
        border-color: #153E20 !important;
        border-radius: 9999px !important;
        box-shadow: 0 0 16px rgba(21, 62, 32, 0.28), inset 0 1px 2px #FFFFFF !important;
    }}
    [data-testid="stNumberInputContainer"] > div,
    [data-testid="stNumberInputContainer"] div[data-baseweb="input"],
    [data-testid="stNumberInputContainer"] div[data-baseweb="base-input"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    [data-testid="stNumberInputContainer"] input {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: #0A2211 !important;
        font-weight: 700 !important;
        font-size: 0.94rem !important;
        padding: 6px 4px !important;
    }}
    [data-testid="stNumberInputContainer"] button,
    [data-testid="stNumberInput"] button,
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"],
    div[data-baseweb="spinbutton"] button,
    [data-testid="stNumberInputContainer"] [data-baseweb="button"] {{
        background-color: #DCEDDA !important;
        background: #DCEDDA !important;
        color: #153E20 !important;
        border: none !important;
        border-radius: 9999px !important;
        margin: 2px 3px !important;
        width: 30px !important;
        height: 30px !important;
        min-width: 30px !important;
        min-height: 30px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }}
    [data-testid="stNumberInputContainer"] button:hover,
    [data-testid="stNumberInput"] button:hover,
    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover,
    div[data-baseweb="spinbutton"] button:hover,
    [data-testid="stNumberInputContainer"] [data-baseweb="button"]:hover {{
        background-color: #B0C3A5 !important;
        background: #B0C3A5 !important;
        color: #051A0B !important;
        transform: scale(1.08) !important;
    }}
    [data-testid="stNumberInputContainer"] button svg,
    [data-testid="stNumberInput"] button svg,
    button[data-testid="stNumberInputStepDown"] svg,
    button[data-testid="stNumberInputStepUp"] svg,
    div[data-baseweb="spinbutton"] button svg {{
        fill: #153E20 !important;
        stroke: #153E20 !important;
        color: #153E20 !important;
        width: 14px !important;
        height: 14px !important;
    }}
    [data-testid="stNumberInputContainer"] button:hover svg,
    [data-testid="stNumberInput"] button:hover svg,
    button[data-testid="stNumberInputStepDown"]:hover svg,
    button[data-testid="stNumberInputStepUp"]:hover svg {{
        fill: #051A0B !important;
        stroke: #051A0B !important;
        color: #051A0B !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       BOTÓN DEL OJITO (VER/OCULTAR CONTRASEÑA O API KEY)
       ═══════════════════════════════════════════════════════════════════════ */
    div[data-baseweb="input"] button,
    div[data-baseweb="base-input"] button,
    .stTextInput button,
    [data-testid="stTextInputRootElement"] button,
    button[aria-label="Show password text"],
    button[aria-label="Hide password text"] {{
        background-color: #DCEDDA !important;
        background: #DCEDDA !important;
        color: #153E20 !important;
        border-radius: 9999px !important;
        border: none !important;
        margin-right: 4px !important;
        width: 32px !important;
        height: 32px !important;
        min-width: 32px !important;
        min-height: 32px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }}
    div[data-baseweb="input"] button:hover,
    div[data-baseweb="base-input"] button:hover,
    .stTextInput button:hover,
    [data-testid="stTextInputRootElement"] button:hover,
    button[aria-label="Show password text"]:hover,
    button[aria-label="Hide password text"]:hover {{
        background-color: #B0C3A5 !important;
        background: #B0C3A5 !important;
        color: #051A0B !important;
        transform: scale(1.08) !important;
    }}
    div[data-baseweb="input"] button svg,
    div[data-baseweb="base-input"] button svg,
    .stTextInput button svg,
    [data-testid="stTextInputRootElement"] button svg,
    button[aria-label="Show password text"] svg,
    button[aria-label="Hide password text"] svg {{
        fill: #153E20 !important;
        stroke: #153E20 !important;
        color: #153E20 !important;
        width: 16px !important;
        height: 16px !important;
    }}
    div[data-baseweb="input"] button:hover svg,
    div[data-baseweb="base-input"] button:hover svg,
    .stTextInput button:hover svg,
    [data-testid="stTextInputRootElement"] button:hover svg,
    button[aria-label="Show password text"]:hover svg,
    button[aria-label="Hide password text"]:hover svg {{
        fill: #051A0B !important;
        stroke: #051A0B !important;
        color: #051A0B !important;
    }}

    /* Área de texto multilínea */
    .stTextArea textarea {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        background: rgba(255, 255, 255, 0.95) !important;
        backdrop-filter: blur(20px) !important;
        border: 1.5px solid rgba(21, 62, 32, 0.35) !important;
        border-radius: 26px !important;
        color: #0A2211 !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        padding: 14px 22px !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04), 0 3px 10px rgba(30, 65, 40, 0.06) !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}
    .stTextArea textarea:focus {{
        border-color: #153E20 !important;
        border-radius: 26px !important;
        box-shadow: 0 0 16px rgba(21, 62, 32, 0.28), inset 0 1px 2px #FFFFFF !important;
    }}

    /* ═══════════════════════════════════════════════════════════════════════
       POPOVERS Y MENÚS DE OPCIONES BASEWEB (DESPLEGABLES ACTIVOS)
       ═══════════════════════════════════════════════════════════════════════ */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    [data-baseweb="popover"],
    [data-baseweb="menu"],
    ul[data-baseweb="menu"],
    [data-testid="stSelectboxVirtualDropdown"],
    [data-testid="stSelectboxVirtualDropdown"] > div,
    [data-testid="stSelectboxVirtualDropdown"] [class*="e1fp86qc4"],
    ul[role="listbox"],
    div[role="listbox"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        border: 1.5px solid rgba(21, 62, 32, 0.30) !important;
        border-radius: 16px !important;
        box-shadow: 0 16px 40px rgba(20, 50, 30, 0.20) !important;
        padding: 8px !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}
    [data-baseweb="menu"] li,
    div[data-baseweb="popover"] li,
    [data-testid="stSelectboxVirtualDropdown"] li,
    [data-testid="stSelectboxVirtualDropdown"] div[role="option"],
    li[role="option"],
    div[role="option"] {{
        background-color: #FFFFFF !important;
        background: #FFFFFF !important;
        color: #0A2211 !important;
        -webkit-text-fill-color: #0A2211 !important;
        font-weight: 600 !important;
        font-size: 0.90rem !important;
        border-radius: 10px !important;
        margin: 3px 4px !important;
        padding: 9px 14px !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
        transition: background 0.15s ease, color 0.15s ease !important;
        cursor: pointer !important;
    }}
    [data-baseweb="menu"] li:hover,
    div[data-baseweb="popover"] li:hover,
    [data-testid="stSelectboxVirtualDropdown"] li:hover,
    [data-testid="stSelectboxVirtualDropdown"] div[role="option"]:hover,
    li[role="option"]:hover,
    div[role="option"]:hover,
    [data-baseweb="menu"] li[aria-selected="true"],
    div[data-baseweb="popover"] li[aria-selected="true"],
    [data-testid="stSelectboxVirtualDropdown"] li[aria-selected="true"],
    [data-testid="stSelectboxVirtualDropdown"] div[role="option"][aria-selected="true"],
    li[role="option"][aria-selected="true"],
    div[role="option"][aria-selected="true"] {{
        background: #DCEDDA !important;
        background-color: #DCEDDA !important;
        color: #051A0B !important;
        -webkit-text-fill-color: #051A0B !important;
    }}
    [data-baseweb="menu"] li *,
    div[data-baseweb="popover"] li *,
    [data-testid="stSelectboxVirtualDropdown"] li *,
    [data-testid="stSelectboxVirtualDropdown"] div[role="option"] * {{
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
        background: transparent !important;
        background-color: transparent !important;
    }}

    /* Desplegables stExpander */
    [data-testid="stExpander"] {{
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(28px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(28px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.90) !important;
        border-radius: 24px !important;
        box-shadow: 0 12px 30px rgba(30, 65, 40, 0.05), inset 0 1px 1px rgba(255, 255, 255, 1) !important;
        margin-bottom: 16px !important;
        color: #102B19 !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}
    [data-testid="stExpander"]:hover {{
        background: rgba(255, 255, 255, 0.80) !important;
    }}
    [data-testid="stExpander"] summary {{
        color: #102B19 !important;
        font-weight: 700 !important;
    }}

    /* Alertas stAlert */
    .stAlert {{
        background: rgba(255, 255, 255, 0.85) !important;
        border: 1px solid rgba(46, 84, 56, 0.25) !important;
        border-radius: 22px !important;
        color: #102B19 !important;
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}

    /* Badges */
    .badge-order {{
        background: rgba(45, 106, 79, 0.15);
        border: 1px solid rgba(45, 106, 79, 0.35);
        color: #123B1D;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.80em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    .badge-family {{
        background: rgba(2, 136, 209, 0.15);
        border: 1px solid rgba(2, 136, 209, 0.35);
        color: #074B83;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.80em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    /* Glass Tile para métricas */
    .glass-tile {{
        background: rgba(255, 255, 255, 0.70);
        backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 14px 18px;
        box-shadow: 0 10px 25px rgba(30, 65, 40, 0.06), inset 0 1px 1px rgba(255, 255, 255, 1);
        box-sizing: border-box !important;
        overflow-wrap: break-word !important;
        word-wrap: break-word !important;
    }}

    /* Métricas Streamlit nativas */
    [data-testid="stMetricValue"] {{
        color: #102B19 !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #244C2E !important;
        font-weight: 600 !important;
    }}
    [data-testid="stMetricDelta"] {{
        color: #426B4D !important;
    }}

    /* ── DISEÑO RESPONSIVO AVANZADO PARA SMARTPHONES Y TABLETS ─────────────── */
    @media (max-width: 992px) {{
        .pf-navbar {{
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 12px !important;
        }}
        .pf-links {{
            justify-content: flex-start !important;
            width: 100% !important;
        }}
    }}

    @media (max-width: 768px) {{
        /* Contenedor principal ajustado para pantallas móviles */
        .block-container {{
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
            padding-top: 1rem !important;
            padding-bottom: 3rem !important;
        }}

        /* Banner Hero Móvil */
        .plantfashion-hero {{
            padding: 20px 18px !important;
            border-radius: 22px !important;
            margin-bottom: 18px !important;
            box-sizing: border-box !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }}
        .pf-navbar {{
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 12px !important;
            margin-bottom: 16px !important;
            padding-bottom: 12px !important;
        }}
        .pf-brand {{
            width: 100% !important;
            gap: 10px !important;
        }}
        .pf-logo-img {{
            width: 38px !important;
            height: 38px !important;
        }}
        .pf-title {{
            font-size: 1.35rem !important;
            letter-spacing: 0.2px !important;
            white-space: nowrap !important;
        }}
        .pf-links {{
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 6px !important;
            width: 100% !important;
            justify-content: flex-start !important;
        }}
        .pf-pill-link {{
            font-size: 0.74rem !important;
            padding: 5px 11px !important;
            white-space: nowrap !important;
        }}
        .pf-headline {{
            font-size: 1.60rem !important;
            line-height: 1.25 !important;
            margin-bottom: 8px !important;
        }}
        .pf-subhead {{
            font-size: 0.86rem !important;
            line-height: 1.45 !important;
            margin-bottom: 14px !important;
        }}
        .pf-btn-badge {{
            font-size: 0.76rem !important;
            padding: 7px 16px !important;
        }}

        /* Barra de pestañas móvil con deslizamiento táctil horizontal nativo */
        .stTabs [data-baseweb="tab-list"] {{
            border-radius: 18px !important;
            padding: 6px 8px !important;
            gap: 6px !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            flex-wrap: nowrap !important;
            scrollbar-width: none !important;
        }}
        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
            display: none !important;
        }}
        .stTabs [data-baseweb="tab"],
        .stTabs button[role="tab"] {{
            font-size: 0.78rem !important;
            padding: 7px 14px !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }}

        /* Tarjetas de información y análisis en móvil */
        .agro-card {{
            padding: 16px 18px !important;
            border-radius: 18px !important;
            margin-bottom: 12px !important;
            box-sizing: border-box !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }}
        .agro-card h4, .agro-card h5 {{
            font-size: 1.05rem !important;
        }}
        .agro-card ul, .agro-card p, .agro-card li {{
            font-size: 0.86rem !important;
            line-height: 1.65 !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }}
        .section-header-card {{
            padding: 14px 16px !important;
            border-radius: 18px !important;
            margin-bottom: 16px !important;
            box-sizing: border-box !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
        }}
        .section-bracket {{
            font-size: 1.02rem !important;
        }}

        /* Selectboxes en móvil */
        div[data-baseweb="select"] > div {{
            border-radius: 14px !important;
            padding: 6px 12px !important;
        }}

        /* Botones y controles táctiles cómodos para dedos */
        .stButton>button {{
            padding: 10px 16px !important;
            font-size: 0.85rem !important;
            min-height: 42px !important;
        }}
        input, select, textarea {{
            font-size: 16px !important; /* Previene el zoom automático de Safari iOS */
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Inicializar sesión
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")
if "suelo_params" not in st.session_state:
    st.session_state.suelo_params = {
        "activo": False,
        "profundidad_cm": 20.0,
        "da_g_cm3": 1.20,
        "mo_pct": 2.5,
        "n_disp_kg_ha": 25.0,
        "p_ppm": 15.0,
        "p_metodo": "Bray II (Suelos ácidos/neutros)",
        "p2o5_disp_kg_ha": 20.6,
        "k_unidad": "cmol(+)/kg (o meq/100g)",
        "k_val": 0.45,
        "k_disp_kg_ha": 50.8,
        "ca_cmol": 6.5,
        "mg_cmol": 2.2,
        "ph": 6.2,
        "textura": "Franco"
    }

# Función para cargar las bases de datos de conocimiento
def cargar_base_datos(nombre):
    for ruta in [os.path.join("data", nombre), nombre]:
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return {}

db_agro = cargar_base_datos("base_conocimiento_agroquimicos.json")
db_libros = cargar_base_datos("base_libros.json")
db_entomologia = cargar_base_datos("base_entomologia_nicaragua.json")
db_cultivos = cargar_base_datos("base_cultivos_nicaragua.json")
db_nutricion = cargar_base_datos("base_nutricion_cultivos.json")
db_catalogo_completo = cargar_base_datos("catalogo_comercial_completo.json")

# ── HERO HEADER PRINCIPAL (APPLE GLASSMORPHISM & LOGO TRANSLÚCIDO) ───────────
logo_glass_tag = f'<img src="data:image/png;base64,{logo_glass_b64}" class="pf-logo-img" alt="Logo Calabaza Translúcida" />' if logo_glass_b64 else '🎃'

st.markdown(f"""
<div class="plantfashion-hero">
    <div class="pf-navbar">
        <div class="pf-brand">
            {logo_glass_tag}
            <span class="pf-title">AgroAsistente</span>
        </div>
        <div class="pf-links">
            <span class="pf-pill-link">🌱 44 Cultivos</span>
            <span class="pf-pill-link">📦 {len(db_catalogo_completo)} Insumos</span>
            <span class="pf-pill-link">🐛 Entomología</span>
            <span class="pf-pill-link">☁️ Radar Clima</span>
        </div>
    </div>
    <div class="pf-content">
        <div class="pf-text-col">
            <h1 class="pf-headline">Diagnóstico y Nutrición de Precisión</h1>
            <p class="pf-subhead">
                Sanidad vegetal avanzada, identificación entomológica, curvas sigmoideas de absorción y formulación cuantitativa por quintal de cosecha.
            </p>
            <div class="pf-action-row">
                <span class="pf-btn-badge">✨ Inteligencia Agronómica de Precisión</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── BARRA LATERAL (CONFIGURACIÓN & CEREBRO CON LOGO TRANSLÚCIDO) ──────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 14px 0 20px 0;">
        <img src="data:image/png;base64,{logo_glass_b64}" style="width: 88px; height: 86px; filter: drop-shadow(0 8px 20px rgba(16, 45, 25, 0.22)) drop-shadow(0 2px 5px rgba(255, 255, 255, 0.8)); transition: transform 0.3s ease;" />
        <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.45rem; color: #102B19; margin-top: 10px; font-weight: 700; letter-spacing: 0.5px;">
            AgroAsistente
        </div>
        <span style="font-size: 0.72rem; color: #153E20; letter-spacing: 1.8px; text-transform: uppercase; font-weight: 700; background: rgba(255, 255, 255, 0.85); padding: 5px 16px; border-radius: 9999px; border: 1.5px solid rgba(21, 62, 32, 0.25); display: inline-block; margin-top: 5px;">Edición Glassmorphism</span>
    </div>
    """, unsafe_allow_html=True)

    # ── 1. UBICACIÓN DEL CULTIVO (OBLIGATORIA & EN LA CIMA) ───────────────────
    st.markdown("### 📍 Ubicación del Cultivo")
    st.markdown("<p style='font-size:0.82rem; color:#153E20; font-weight:700; margin-top:-6px; margin-bottom:8px;'>⚠️ Selección obligatoria para activar el diagnóstico:</p>", unsafe_allow_html=True)
    from clima import obtener_departamentos, obtener_municipios, resolver_coordenadas, RadarClimatico
    
    lista_departamentos = ["-- Selecciona un Departamento --"] + obtener_departamentos()
    dep_default_idx = 0
    if "dep_guardado" in st.session_state and st.session_state.dep_guardado in lista_departamentos:
        dep_default_idx = lista_departamentos.index(st.session_state.dep_guardado)

    dep_seleccionado = st.selectbox(
        "1. Departamento / Región:",
        lista_departamentos,
        index=dep_default_idx,
        key="selector_dep_principal"
    )
    st.session_state.dep_guardado = dep_seleccionado

    es_dep_valido = bool(dep_seleccionado and dep_seleccionado != "-- Selecciona un Departamento --")
    if es_dep_valido:
        lista_muns = ["-- Selecciona un Municipio --"] + obtener_municipios(dep_seleccionado)
        esta_deshabilitado = False
    else:
        lista_muns = ["-- Primero selecciona Departamento --"]
        esta_deshabilitado = True

    if "prev_dep_sync" not in st.session_state:
        st.session_state.prev_dep_sync = dep_seleccionado

    if st.session_state.prev_dep_sync != dep_seleccionado:
        st.session_state.prev_dep_sync = dep_seleccionado
        st.session_state.selector_mun_estable = lista_muns[0]

    val_mun_actual = st.session_state.get("selector_mun_estable", lista_muns[0])
    mun_default_idx = lista_muns.index(val_mun_actual) if val_mun_actual in lista_muns else 0

    mun_seleccionado = st.selectbox(
        "2. Municipio:",
        options=lista_muns,
        index=mun_default_idx,
        disabled=esta_deshabilitado,
        key="selector_mun_estable"
    )

    if es_dep_valido and mun_seleccionado and mun_seleccionado not in ("-- Selecciona un Municipio --", "-- Primero selecciona Departamento --"):
        ubicacion_valida = True
        ubicacion_activa = f"{mun_seleccionado}, {dep_seleccionado}"
    else:
        ubicacion_valida = False
        ubicacion_activa = ""

    if ubicacion_valida:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.92); padding: 8px 14px; border-radius: 9999px; border: 1.5px solid #153E20; text-align: center; margin: 8px 0 14px 0; box-shadow: 0 4px 12px rgba(21, 62, 32, 0.10);">
            <span style="color: #153E20; font-weight: 700; font-size: 0.84rem;">✅ Sincronizado: {ubicacion_activa}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ☁️ Radar Meteorológico Local")
        try:
            lat_z, lon_z, nom_z = resolver_coordenadas(mun_seleccionado, departamento_hint=dep_seleccionado)
            radar = RadarClimatico(lat_z, lon_z, nom_z)
            resumen_clima = radar.generar_advertencia_agronomica()
            st.info(resumen_clima)
        except Exception:
            st.info(f"Radar activo para {ubicacion_activa}: Monitoreo en tiempo real.")
    else:
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.90); padding: 10px 14px; border-radius: 20px; border: 1.5px dashed #C0392B; margin: 8px 0 14px 0;">
            <span style="color: #C0392B; font-weight: 700; font-size: 0.83rem;">🔴 Requisito Obligatorio:</span><br>
            <span style="color: #78281F; font-size: 0.80rem;">Debes elegir tu departamento y municipio para habilitar las consultas y el radar.</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ── 2. CONFIGURACIÓN IA ───────────────────────────────────────────────────
    st.subheader("⚙️ Configuración IA")
    api_key_input = st.text_input("Gemini API Key:", type="password", value=st.session_state.api_key)
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.toast("API Key guardada.", icon="🔑")
    elif api_key_input and "GEMINI_API_KEY" not in os.environ:
        os.environ["GEMINI_API_KEY"] = api_key_input

    st.markdown("---")

    # ── 3. CEREBRO DEL ASISTENTE ──────────────────────────────────────────────
    with st.expander("🧠 Cerebro & Base del Asistente", expanded=False):
        st.markdown(f"""
        - 🧪 **{len(db_agro)}** Agroquímicos comerciales locales
        - 🐛 **{len(db_entomologia)}** Plagas entomológicas completas
        - 🌾 **{len(db_cultivos)}** Cultivos agronómicos e industriales
        - 🌱 **{len(db_nutricion)}** Cultivos con Curvas de Absorción Nutricional
        - 📚 **{len(db_libros)}** Fragmentos de literatura científica
        """)

# Pestañas principales
tab_diagnostico, tab_entomologia, tab_cultivos, tab_nutricion, tab_suelo, tab_costos = st.tabs([
    "🩺 Diagnóstico Clínico",
    "🐛 Catálogo Entomológico",
    "🌾 Guía de Cultivos",
    "🌱 Nutrición & Curvas",
    "🔬 Análisis de Suelo (Opcional)",
    "💲 Costos de Aplicación"
])

# ── PESTAÑA 1: DIAGNÓSTICO FITOSANITARIO ──────────────────────────────────────
with tab_diagnostico:
    st.markdown("""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Consultorio Clínico Agronómico <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            Escribe los síntomas, el cultivo o sube una fotografía del daño foliar, fruto, tallo o raíz para diagnóstico y prescripción técnica.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Banner de estado de ubicación obligatoria
    if not ubicacion_valida:
        st.markdown("""
        <div style="background: rgba(255, 235, 238, 0.94); border: 2px solid #E53935; border-radius: 9999px; padding: 10px 24px; margin-bottom: 20px; box-shadow: 0 4px 16px rgba(229, 57, 53, 0.12); display: flex; align-items: center; justify-content: space-between;">
            <span style="color: #B71C1C; font-weight: 700; font-size: 0.90rem;">
                📍 <strong>Requisito Obligatorio:</strong> Debes seleccionar tu <strong>Departamento y Municipio</strong> en el panel lateral para habilitar las respuestas del asistente.
            </span>
            <span style="background: #E53935; color: white; padding: 3px 12px; border-radius: 9999px; font-size: 0.76rem; font-weight: 700;">PENDIENTE</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.92); border: 1.5px solid #153E20; border-radius: 9999px; padding: 8px 24px; margin-bottom: 20px; box-shadow: 0 4px 14px rgba(21, 62, 32, 0.08); display: flex; align-items: center; justify-content: space-between;">
            <span style="color: #102B19; font-weight: 700; font-size: 0.88rem;">
                📍 Ubicación Activa: <strong>{ubicacion_activa}</strong>
            </span>
            <span style="background: rgba(176, 195, 165, 0.60); color: #153E20; padding: 3px 14px; border-radius: 9999px; font-size: 0.78rem; font-weight: 700; border: 1px solid rgba(21, 62, 32, 0.25);">📡 Radar Meteorológico Sincronizado</span>
        </div>
        """, unsafe_allow_html=True)

    # Preguntas rápidas de 1-clic estilo Apple Glass Pills
    col_q1, col_q2, col_q3, col_q4, col_q5 = st.columns(5)
    pregunta_rapida = None
    if col_q1.button("🐛 Barrenador Sandía", key="btn_quick_barrenador"):
        pregunta_rapida = "¿Cómo identificar y controlar el gusano barrenador del fruto en sandía y qué productos aplicar?"
    if col_q2.button("🦗 Salivazo Caña", key="btn_quick_salivazo"):
        pregunta_rapida = "¿Cuáles son los umbrales de acción para salivazo en caña de azúcar y qué insecticida rotar?"
    if col_q3.button("☕ Broca Café", key="btn_quick_broca"):
        pregunta_rapida = "¿Cómo controlar la broca del café en posición AB y qué manejo integrado se recomienda?"
    if col_q4.button("🌱 Pudrición Raíz (Drench)", key="btn_quick_pudricion"):
        pregunta_rapida = "Tengo pudrición radicular y marchitez en mi cultivo, ¿qué fungicida al drench debo aplicar?"
    if col_q5.button("🧪 Plan NPK Sandía", key="btn_quick_npk"):
        pregunta_rapida = "¿Cuál es el plan nutricional y extracción de N-P-K por quintal para sandía según su curva sigmoidea de absorción?"

    # Subida de imagen opcional para diagnóstico fotográfico
    with st.expander("📷 Adjuntar Fotografía de Campo para Diagnóstico Visual (Opcional)", expanded=False):
        foto_subida = st.file_uploader(
            "Sube una foto clara del cultivo, follaje, tallo o fruto con síntomas:",
            type=["jpg", "jpeg", "png"],
            key="foto_campo"
        )
        if foto_subida:
            st.image(foto_subida, width=240, caption="Foto lista para diagnóstico multimodal")

    # Historial de conversación
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("has_image") and "image_bytes" in msg:
                st.image(msg["image_bytes"], width=220, caption="Foto adjunta por el productor")

    # Barra de entrada fija permanentemente en la parte inferior de la pantalla (Sticky Bottom)
    consulta_texto = st.chat_input("Escribe tu consulta agronómica aquí...")
    consulta_activa = pregunta_rapida or consulta_texto

    if consulta_activa:
        if not ubicacion_valida:
            st.error("🛑 **Ubicación Requerida Obligatoria:** No se puede emitir diagnóstico fitosanitario sin conocer la zona agroclimática. Por favor, selecciona primero tu **Departamento y Municipio** en el panel lateral.")
        else:
            imagen_pil = None
            imagen_bytes = None
            if foto_subida:
                try:
                    imagen_bytes = foto_subida.getvalue()
                    imagen_pil = Image.open(foto_subida)
                    imagen_pil.thumbnail((800, 800))
                except Exception:
                    imagen_pil = None

            user_msg = {"role": "user", "content": consulta_activa}
            if imagen_bytes:
                user_msg["has_image"] = True
                user_msg["image_bytes"] = imagen_bytes

            st.session_state.chat_history.append(user_msg)
            with st.chat_message("user"):
                st.markdown(consulta_activa)
                if imagen_bytes:
                    st.image(imagen_bytes, width=220, caption="Foto adjunta por el productor")

            with st.chat_message("assistant"):
                with st.spinner("Analizando base entomológica, guías agronómicas, catálogo de agroquímicos y clima local..."):
                    if not st.session_state.api_key:
                        st.warning("⚠️ Ingresa tu API Key de Gemini en la barra lateral para activar el diagnóstico.")
                    else:
                        try:
                            asistente = AsistenteFitosanitario(
                                api_key=st.session_state.api_key,
                                base_agroquimicos=db_agro,
                                base_libros=db_libros,
                                base_entomologia=db_entomologia,
                                base_cultivos=db_cultivos,
                                base_nutricion=db_nutricion
                            )
                            respuesta = asistente.generar_respuesta(
                                st.session_state.chat_history,
                                consulta_activa,
                                imagen=imagen_pil,
                                ubicacion_usuario=ubicacion_activa
                            )
                            st.markdown(respuesta)
                            st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                            st.session_state.ultima_receta = respuesta
                            st.session_state.ultima_ubicacion = ubicacion_activa
                        except Exception as e:
                            st.error(f"Error procesando la consulta: {e}")

    # Descarga directa de Receta Agronómica en PDF
    if "ultima_receta" in st.session_state and st.session_state.ultima_receta:
        st.markdown("---")
        col_pdf_btn, _ = st.columns([2.5, 1])
        with col_pdf_btn:
            try:
                import importlib
                import pdf_builder
                importlib.reload(pdf_builder)
                loc_pdf = st.session_state.get("ultima_ubicacion", ubicacion_activa if ubicacion_valida else "Nicaragua")
                pdf_path = pdf_builder.generar_receta_pdf("Diagnóstico Fitosanitario", st.session_state.ultima_receta, lote="Lote de Producción", ubicacion=loc_pdf)
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f_pdf:
                        st.download_button(
                            label="📥 Descargar Receta Agronómica Oficial (PDF)",
                            data=f_pdf.read(),
                            file_name="Receta_Fitosanitaria_Nicaragua.pdf",
                            mime="application/pdf"
                        )
                    st.caption("✨ Documento técnico formal con membrete institucional y marcas de agua oficiales.")
            except Exception as ex:
                st.caption(f"Generador PDF disponible al procesar consulta ({ex})")

# ── PESTAÑA 2: CATÁLOGO ENTOMOLÓGICO ─────────────────────────────────────────
with tab_entomologia:
    st.markdown("""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Catálogo Entomológico Especializado <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            Fichas técnicas completas de taxonomía, ciclo biológico, daños característicos, umbrales económicos y manejo integrado.
        </p>
    </div>
    """, unsafe_allow_html=True)

    filtro_insecto = st.text_input("🔍 Buscar por insecto, cultivo o nombre científico:", placeholder="Ej: Spodoptera, Sandía, Salivazo, Broca, Picudo...")

    for key, p in db_entomologia.items():
        nom_c = p.get("nombre_comun", "")
        nom_s = p.get("nombre_cientifico", "")
        hospedantes = ", ".join(p.get("cultivos_hospedantes", []))
        
        # Filtro de búsqueda
        if filtro_insecto:
            termino = filtro_insecto.lower()
            if termino not in nom_c.lower() and termino not in nom_s.lower() and termino not in hospedantes.lower():
                continue

        with st.expander(f"🐜 {nom_c} (*{nom_s}*)"):
            col_tax, col_bio = st.columns([1, 2])
            with col_tax:
                st.markdown(f"**Orden:** <span class='badge-order'>{p.get('orden')}</span>", unsafe_allow_html=True)
                st.markdown(f"**Familia:** <span class='badge-family'>{p.get('familia')}</span>", unsafe_allow_html=True)
                st.markdown(f"**Cultivos Hospedantes:**\n{hospedantes}")
                umbral = p.get('umbral_economico') or p.get('umbral_economico_nicaragua', 'Consultar técnico')
                st.markdown(f"**🛑 Umbral Económico:**\n*{umbral}*")
            with col_bio:
                st.markdown(f"**🔬 Biología y Ciclo:**\n{p.get('biologia_y_ciclo')}")
                st.markdown(f"**🎯 Daño Característico:**\n{p.get('daño')}")
                st.markdown(f"**🐞 Control Biológico:**\n{p.get('control_biologico')}")
                st.markdown(f"**🧪 Manejo Químico & Rotación IRAC:**\n`{p.get('control_quimico_sugerido')}`")

# ── PESTAÑA 3: GUÍA TÉCNICA DE CULTIVOS ───────────────────────────────────────
with tab_cultivos:
    st.markdown("""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Guía Técnica de Manejo de Cultivos <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            Fichas agronómicas completas de variedades, requerimientos edafoclimáticos, fertilización por etapas y rendimientos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    for k_c, c in db_cultivos.items():
        with st.expander(f"🌱 Cultivo: {c.get('nombre_cultivo')} (*{c.get('nombre_cientifico')}*)"):
            col_gen, col_man = st.columns([1, 2])
            with col_gen:
                st.markdown(f"**Familia:** {c.get('familia')}")
                zonas = c.get('zonas_principales') or c.get('zonas_principales_nicaragua', [])
                st.markdown(f"**Zonas Principales:**\n{', '.join(zonas)}")
                vars_c = c.get('variedades') or c.get('variedades_nicaragua', [])
                st.markdown(f"**Variedades recomendadas:**\n{', '.join(vars_c)}")
                req = c.get('requerimientos_edafoclimaticos', {})
                st.markdown(f"**🌡️ Temperatura:** {req.get('temperatura_optima', 'N/A')}")
                st.markdown(f"**🌧️ Suelos:** {req.get('suelos', 'N/A')}")
            with col_man:
                man = c.get('manejo_agronomico', {})
                if 'fertilizacion_nutricion' in man:
                    st.markdown("**🧪 Programa de Fertilización:**")
                    for etapa, desc in man['fertilizacion_nutricion'].items():
                        st.markdown(f"- *{etapa.replace('_', ' ').title()}:* {desc}")
                st.markdown(f"**🐛 Plagas Clave:** {', '.join(man.get('plagas_clave', []))}")
                st.markdown(f"**🍄 Enfermedades Clave:** {', '.join(man.get('enfermedades_clave', []))}")
                st.markdown(f"**🚜 Cosecha & Rendimiento:** {man.get('cosecha_y_rendimiento') or man.get('cosecha', 'N/A')}")

# ── PESTAÑA 4: CURVAS DE ABSORCIÓN & PLANES NUTRICIONALES ─────────────────────
with tab_nutricion:
    st.markdown("""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Fisiología Nutricional & Curvas de Absorción (44 Cultivos) <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            Cálculo cuantitativo de extracción total (kg/t), remoción por cosecha, balance N:K y fraccionamiento fenológico por curva sigmoidea.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Filtro por grupo agronómico y selección de cultivo
    grupos_disponibles = ["Todos los Grupos", "Granos", "Industriales", "Hortalizas", "Raíces y Tubérculos", "Frutales"]
    col_g, col_c = st.columns([1, 2])
    with col_g:
        grupo_sel = st.selectbox("Filtrar por Grupo Agronómico:", grupos_disponibles)
    
    # Filtrar cultivos según grupo
    cultivos_filtrados = {}
    for cid, cdata in sorted(db_nutricion.items(), key=lambda x: x[1].get("nombre_comun", "")):
        if grupo_sel == "Todos los Grupos" or cdata.get("grupo_agronomico", "").lower() == grupo_sel.lower():
            cultivos_filtrados[cdata.get("nombre_comun", cid.title())] = (cid, cdata)

    nombres_cultivos = list(cultivos_filtrados.keys())
    with col_c:
        cultivo_seleccionado_nom = st.selectbox("Selecciona el Cultivo a Analizar:", nombres_cultivos, index=0 if nombres_cultivos else 0)

    if cultivo_seleccionado_nom and cultivo_seleccionado_nom in cultivos_filtrados:
        cid_actual, c_info = cultivos_filtrados[cultivo_seleccionado_nom]
        ext_tot = c_info.get("extraccion_nutrimentos_kg_por_t", {}).get("extraccion_total", {})
        ext_cos = c_info.get("extraccion_nutrimentos_kg_por_t", {}).get("extraccion_cosecha", {})
        pct_exp = c_info.get("extraccion_nutrimentos_kg_por_t", {}).get("porcentaje_exportado_en_cosecha", {})
        bal = c_info.get("balance_nutricional", {})
        din = c_info.get("dinamica_nutricional", {})

        # Tarjetas Métricas Principales de Extracción en Quintales (qq)
        st.markdown(f"#### 📊 Métricas de Extracción por Quintal (qq) de Cosecha ({c_info.get('nombre_comun')} - *{c_info.get('grupo_agronomico')}*)")
        
        # 1 Quintal (qq) = 100 lb = 45.3592 kg = 0.0453592 t
        F_QQ = 0.0453592

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric(
                label="Nitrógeno (N)",
                value=f"{round(ext_tot.get('N', 0) * F_QQ, 2)} kg/qq",
                delta=f"Cosecha: {round(ext_cos.get('N', 0) * F_QQ, 2)} kg/qq ({pct_exp.get('N_pct', 0)}% exportado)",
                delta_color="off"
            )
        with m2:
            st.metric(
                label="Fósforo (P₂O₅)",
                value=f"{round(ext_tot.get('P2O5', 0) * F_QQ, 2)} kg/qq",
                delta=f"Cosecha: {round(ext_cos.get('P2O5', 0) * F_QQ, 2)} kg/qq ({pct_exp.get('P_pct', 0)}% exportado)",
                delta_color="off"
            )
        with m3:
            st.metric(
                label="Potasio (K₂O)",
                value=f"{round(ext_tot.get('K2O', 0) * F_QQ, 2)} kg/qq",
                delta=f"Cosecha: {round(ext_cos.get('K2O', 0) * F_QQ, 2)} kg/qq ({pct_exp.get('K_pct', 0)}% exportado)",
                delta_color="off"
            )
        with m4:
            nk = bal.get("relacion_nk_cosecha", "1:1")
            dem_k = bal.get("categoria_demanda_k", "Similar")
            badge_color = "#E53935" if dem_k == "Alto" else "#43A047" if dem_k == "Similar" else "#FB8C00"
            st.markdown(f"""
            <div class="glass-tile" style="text-align:center; padding:12px;">
                <span style="font-size:0.85em; color:#244C2E; font-weight:600;">Relación N:K en Cosecha</span><br>
                <span style="font-size:1.45em; font-weight:700; color:#102B19;">{nk}</span><br>
                <span style="background-color:{badge_color}; color:white; padding:3px 12px; border-radius:20px; font-size:0.75em; font-weight:600; display:inline-block; margin-top:4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">Demanda K: {dem_k}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Calculadora Dinámica de Fertilización
        st.markdown("#### 🧮 Calculadora de Fertilización de Precisión")
        
        # Rendimiento por defecto en Quintales por hectárea (qq/ha)
        rend_default = 770.0
        nom_c = c_info.get("nombre_comun", "").lower()
        if c_info.get("grupo_agronomico") == "Granos":
            if "frijol" in nom_c: rend_default = 35.0
            elif "maiz" in nom_c or "maíz" in nom_c: rend_default = 90.0
            elif "arroz" in nom_c: rend_default = 120.0
            else: rend_default = 80.0
        elif c_info.get("grupo_agronomico") == "Industriales":
            rend_default = 1750.0 if "caña" in nom_c else 65.0
        elif c_info.get("grupo_agronomico") == "Raíces y Tubérculos":
            rend_default = 550.0
        elif c_info.get("grupo_agronomico") == "Frutales":
            rend_default = 650.0

        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            rend_meta = st.number_input(
                "Rendimiento Meta Esperado (qq/ha):",
                min_value=1.0,
                max_value=10000.0,
                value=float(rend_default),
                step=5.0,
                help="Rendimiento agronómico meta medido en quintales por hectárea (1 qq = 100 lb = 45.36 kg)."
            )
        with col_calc2:
            tipo_suelo = st.selectbox(
                "Tipo de Suelo y Retención:",
                ["Franco / Neutro Estándar (Eficiencias: N 60%, P 25%, K 70%)",
                 "Arcilloso / Pesado / Fijador (Eficiencias: N 55%, P 20%, K 65%)",
                 "Arenoso / Ligero / Lixiviable (Eficiencias: N 50%, P 30%, K 60%)"]
            )

        # Determinar factores de eficiencia
        if "Arcilloso" in tipo_suelo:
            ef_n, ef_p, ef_k = 0.55, 0.20, 0.65
        elif "Arenoso" in tipo_suelo:
            ef_n, ef_p, ef_k = 0.50, 0.30, 0.60
        else:
            ef_n, ef_p, ef_k = 0.60, 0.25, 0.70

        # Detección de leguminosas (Frijol, Soya, Maní, Arveja, etc.)
        nom_c_lower = c_info.get("nombre_comun", "").lower()
        id_c_lower = str(cid_actual).lower()
        es_leguminosa = any(x in nom_c_lower or x in id_c_lower for x in ["frijol", "soya", "soja", "mani", "maní", "arveja", "habas", "garbanzo", "caupi"])

        descuento_fbn = 0.0
        if es_leguminosa:
            col_fbn_sel, col_fbn_info = st.columns([1.6, 1.4])
            with col_fbn_sel:
                fbn_opcion = st.selectbox(
                    "🦠 Simbiosis Bacteriana (Fijación Biológica de N - Rhizobium):",
                    [
                        "Cepas Nativas en Suelos Agrícolas (Promedio: 40.0 kg N/ha)",
                        "Inoculación Seleccionada / Comercial (65.0 kg N/ha)",
                        "Sin Nódulos / Suelo Degradado o Quema (0.0 kg N/ha)",
                        "Personalizado (Digitar kg N/ha manualmente)"
                    ],
                    index=0,
                    key=f"fbn_opcion_{cid_actual}",
                    help="En Nicaragua, los suelos agrícolas cuentan con poblaciones nativas de Rhizobium en nódulos radiculares que fijan en promedio 40 kg N/ha en frijol."
                )
            with col_fbn_info:
                if "Nativas" in fbn_opcion:
                    descuento_fbn = 40.0
                    st.markdown("<p style='font-size:0.86rem; color:#1B5E20; padding-top:28px;'>🌱 <strong>40.0 kg N/ha</strong> aportados gratuitamente por cepas nativas de <em>Rhizobium</em>.</p>", unsafe_allow_html=True)
                elif "Inoculación" in fbn_opcion:
                    descuento_fbn = 65.0
                    st.markdown("<p style='font-size:0.86rem; color:#1B5E20; padding-top:28px;'>🚀 <strong>65.0 kg N/ha</strong> fijados con cepas comerciales de alta eficiencia.</p>", unsafe_allow_html=True)
                elif "Sin Nódulos" in fbn_opcion:
                    descuento_fbn = 0.0
                    st.markdown("<p style='font-size:0.86rem; color:#B71C1C; padding-top:28px;'>⚠️ <strong>0.0 kg N/ha</strong> (Sin fijación biológica activa).</p>", unsafe_allow_html=True)
                else:
                    descuento_fbn = st.number_input("Digita el Aporte FBN (kg N/ha):", min_value=0.0, max_value=250.0, value=40.0, step=5.0, key=f"fbn_custom_{cid_actual}")

        # Comprobar si hay análisis de suelo activo (Pestaña 5)
        suelo_p = st.session_state.get("suelo_params", {})
        suelo_activo = suelo_p.get("activo", False)
        if suelo_activo:
            descuento_suelo_n = float(suelo_p.get("n_disp_kg_ha", 0.0))
            descuento_suelo_p = float(suelo_p.get("p2o5_disp_kg_ha", 0.0))
            descuento_suelo_k = float(suelo_p.get("k_disp_kg_ha", 0.0))
        else:
            descuento_suelo_n = 0.0
            descuento_suelo_p = 0.0
            descuento_suelo_k = 0.0

        # Cálculo de extracciones brutas (rend_meta en qq/ha convertido a toneladas)
        rend_meta_t = rend_meta * F_QQ
        req_n_bruto = round(ext_tot.get("N", 0) * rend_meta_t, 1)
        req_p_bruto = round(ext_tot.get("P2O5", 0) * rend_meta_t, 1)
        req_k_bruto = round(ext_tot.get("K2O", 0) * rend_meta_t, 1)

        # Demanda Neta a cubrir mediante fertilizantes químicos
        req_n_neto = max(0.0, round(req_n_bruto - descuento_fbn - descuento_suelo_n, 1))
        req_p_neto = max(0.0, round(req_p_bruto - descuento_suelo_p, 1))
        req_k_neto = max(0.0, round(req_k_bruto - descuento_suelo_k, 1))

        # Dosis bruta con fertilizante al suelo considerando eficiencias de absorción
        dosis_n_ha = round(req_n_neto / ef_n, 1)
        dosis_p_ha = round(req_p_neto / ef_p, 1)
        dosis_k_ha = round(req_k_neto / ef_k, 1)

        # Conversión a fertilizantes comerciales (Sacos de 50 kg)
        # 1. DAP (18-46-0) cubre primero P2O5
        kg_dap = round(dosis_p_ha / 0.46, 1) if dosis_p_ha > 0 else 0.0
        sacos_dap = round(kg_dap / 50.0, 1)
        n_aportado_dap = round(kg_dap * 0.18, 1)

        # 2. Urea (46-0-0) cubre el N restante
        n_restante = max(0.0, round(dosis_n_ha - n_aportado_dap, 1))
        kg_urea = round(n_restante / 0.46, 1) if n_restante > 0 else 0.0
        sacos_urea = round(kg_urea / 50.0, 1)

        # 3. MOP (0-0-60) Cloruro de Potasio cubre K2O
        kg_mop = round(dosis_k_ha / 0.60, 1) if dosis_k_ha > 0 else 0.0
        sacos_mop = round(kg_mop / 50.0, 1)

        # Banner explicativo de Resta por Fijación Biológica de Nitrógeno (FBN)
        if es_leguminosa and descuento_fbn > 0:
            n_ahorrado_bruto = round(descuento_fbn / ef_n, 1)
            sacos_urea_ahorrados = round((n_ahorrado_bruto) / 0.46 / 50.0, 1)
            suelo_txt_fbn = f" - Suelo ({descuento_suelo_n:.1f} kg N)" if descuento_suelo_n > 0 else ""
            st.markdown(f"""
            <div class="agro-card" style="background: rgba(232, 245, 233, 0.92); border-left: 6px solid #2E7D32; margin: 10px 0 16px 0; padding: 16px 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                    <h5 style="color:#1B5E20; font-family:'Playfair Display', Georgia, serif; font-weight:700; margin:0;">
                        🦠 Crédito Biológico por Simbiosis (FBN - <em>Rhizobium spp.</em>):
                    </h5>
                    <span style="background:#2E7D32; color:white; padding:4px 14px; border-radius:9999px; font-size:0.82rem; font-weight:700; box-shadow:0 2px 6px rgba(46,125,50,0.3);">
                        RESTA APLICADA: -{descuento_fbn:.1f} kg N/ha
                    </span>
                </div>
                <div style="margin-top:10px; font-size:0.92rem; color:#143E19; line-height:1.7;">
                    El cultivo de <strong>{c_info.get('nombre_comun')}</strong> fija nitrógeno atmosférico a través de sus nódulos radiculares en simbiosis con bacterias del género <em>Rhizobium</em> (cepas nativas abundantes en los suelos agrícolas de Nicaragua).
                    <ul style="margin: 8px 0 4px 18px; padding-left:0; line-height:1.9;">
                        <li>🌱 <strong>Aporte natural descontado:</strong> Se restan <strong>{descuento_fbn:.1f} kg N/ha</strong> directamente de la demanda total del cultivo.</li>
                        <li>📉 <strong>Equivalencia en Fertilizante Ahorrado:</strong> Esta fijación biológica evita aplicar <strong>{n_ahorrado_bruto} kg N/ha de fertilización sintética</strong> (a eficiencia del {int(ef_n*100)}%), lo que equivale a un ahorro directo de <strong>~{sacos_urea_ahorrados} sacos de Urea (50 kg) por hectárea</strong>.</li>
                        <li>📐 <strong>Ajuste de Demanda Neta:</strong> Demanda Bruta ({req_n_bruto} kg N) - Aporte Nódulo ({descuento_fbn:.1f} kg N){suelo_txt_fbn} = <strong>{req_n_neto} kg N netos a suministrar</strong>.</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Banner explicativo de Análisis de Suelo (Activo vs Inactivo)
        if suelo_activo:
            st.markdown(f"""
            <div class="agro-card" style="background: rgba(227, 242, 253, 0.92); border-left: 6px solid #1565C0; margin: 10px 0 16px 0; padding: 16px 20px;">
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
                    <h5 style="color:#0D47A1; font-family:'Playfair Display', Georgia, serif; font-weight:700; margin:0;">
                        🔬 Descuento por Análisis de Suelo de Laboratorio Aplicado:
                    </h5>
                    <span style="background:#1565C0; color:white; padding:4px 14px; border-radius:9999px; font-size:0.82rem; font-weight:700; box-shadow:0 2px 6px rgba(21,101,192,0.3);">
                        CALIBRACIÓN QUÍMICA ACTIVA
                    </span>
                </div>
                <div style="margin-top:10px; font-size:0.92rem; color:#0A2540; line-height:1.7;">
                    Se descuentan los nutrientes que tu suelo ya tiene disponibles según el análisis químico ingresado en la pestaña <em>🔬 Análisis de Suelo</em>:
                    <ul style="margin: 8px 0 4px 18px; padding-left:0; line-height:1.9;">
                        <li>🌿 <strong>Nitrógeno Aportado por Suelo (MO):</strong> -{descuento_suelo_n:.1f} kg N/ha</li>
                        <li>🌾 <strong>Fósforo Asimilable del Lote:</strong> -{descuento_suelo_p:.1f} kg P₂O₅/ha (Ahorro de ~{round(descuento_suelo_p / 0.46 / 50.0, 1)} sacos de DAP)</li>
                        <li>🍌 <strong>Potasio Asimilable del Lote:</strong> -{descuento_suelo_k:.1f} kg K₂O/ha (Ahorro de ~{round(descuento_suelo_k / 0.60 / 50.0, 1)} sacos de MOP)</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.78); border: 1.5px dashed rgba(21, 62, 32, 0.30); border-radius: 9999px; padding: 10px 22px; margin-bottom: 16px; font-size: 0.88rem; color: #153E20; display:flex; justify-content:space-between; align-items:center;">
                <span>💡 <strong>¿Tienes análisis químico de suelo?</strong> Es <em>opcional</em>. Si cuentas con los resultados de laboratorio de tu lote, ve a la pestaña <strong>🔬 Análisis de Suelo (Opcional)</strong> para descontar los nutrientes de tu tierra.</span>
                <span style="background: rgba(176, 195, 165, 0.6); padding: 3px 12px; border-radius: 9999px; font-weight: 700; font-size: 0.78rem;">MODO ESTÁNDAR</span>
            </div>
            """, unsafe_allow_html=True)

        # Mostrar resultados de la calculadora
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            linea_fbn_res = f"<li>🦠 <strong>Crédito Simbiosis (Rhizobium FBN):</strong> <span style='color:#1B5E20; font-weight:bold;'>-{descuento_fbn:.1f} kg N/ha</span></li>" if (es_leguminosa and descuento_fbn > 0) else ""
            linea_suelo_res = f"<li>🔬 <strong>Aporte Análisis de Suelo:</strong> <span style='color:#1565C0; font-weight:bold;'>-{descuento_suelo_n:.1f} N | -{descuento_suelo_p:.1f} P₂O₅ | -{descuento_suelo_k:.1f} K₂O kg/ha</span></li>" if suelo_activo else ""

            st.markdown(f"""<div class="agro-card">
<h5 style="color:#102B19; font-weight:700; margin-bottom:12px;">🎯 Requerimiento Elemental del Lote ({rend_meta} qq/ha):</h5>
<ul style="line-height:1.9; padding-left:18px; margin:0;">
<li><strong>Extracción Total Bruta del Cultivo:</strong> {req_n_bruto} kg N | {req_p_bruto} kg P₂O₅ | {req_k_bruto} kg K₂O / ha</li>
{linea_fbn_res}
{linea_suelo_res}
<li><strong>Demanda Neta a Cubrir con Fertilizante:</strong><br><span style="color:#102B19; font-weight:bold;">N: {req_n_neto} kg/ha | P₂O₅: {req_p_neto} kg/ha | K₂O: {req_k_neto} kg/ha</span></li>
<li><strong>Dosis Bruta a Aplicar al Suelo:</strong><br><span style="color:#1B4D27; font-weight:bold;">N: {dosis_n_ha} kg/ha</span> (Eficiencia {int(ef_n*100)}%)<br><span style="color:#1B4D27; font-weight:bold;">P₂O₅: {dosis_p_ha} kg/ha</span> (Eficiencia {int(ef_p*100)}%)<br><span style="color:#1B4D27; font-weight:bold;">K₂O: {dosis_k_ha} kg/ha</span> (Eficiencia {int(ef_k*100)}%)</li>
</ul>
</div>""", unsafe_allow_html=True)

        with col_res2:
            st.markdown(f"""<div class="agro-card">
<h5 style="color:#102B19; font-weight:700; margin-bottom:12px;">📦 Equivalencia en Fertilizantes Comerciales (Sacos 50 kg):</h5>
<ul style="line-height:1.9; padding-left:18px; margin:0;">
<li><strong>DAP 18-46-0 (Fósforo + N inicial):</strong> <span style="font-weight:bold; color:#102B19;">{kg_dap} kg/ha</span> → <span style="color:#1B4D27; font-weight:bold;">{sacos_dap} sacos/ha</span><br><small style="color:#2D5837;">(Aporta {n_aportado_dap} kg N como starter para desarrollo radicular inicial)</small></li>
<li><strong>Urea 46-0-0 (Nitrógeno de balance):</strong> <span style="font-weight:bold; color:#102B19;">{kg_urea} kg/ha</span> → <span style="color:#1B4D27; font-weight:bold;">{sacos_urea} sacos/ha</span><br><small style="color:#2D5837;">(Cubre los {n_restante} kg N netos de balance no cubiertos por DAP ni FBN)</small></li>
<li><strong>MOP 0-0-60 (Cloruro de Potasio):</strong> <span style="font-weight:bold; color:#102B19;">{kg_mop} kg/ha</span> → <span style="color:#1B4D27; font-weight:bold;">{sacos_mop} sacos/ha</span></li>
</ul>
<div style="margin-top:10px; font-size:0.82rem; color:#2D5837;">*En fertirriego o cultivos sensibles a cloro (tabaco/papa), sustituir MOP por Sulfato de Potasio (SOP 0-0-50) o Nitrato de Potasio.</div>
</div>""", unsafe_allow_html=True)

        # Fraccionamiento Fenológico (Curva Sigmoidea)
        st.markdown("#### 📈 Fraccionamiento Fenológico según la Curva Sigmoidea de Absorción")
        etapas = din.get("fraccionamiento_por_etapas", [])
        if etapas:
            cols_etapas = st.columns(len(etapas))
            for idx, etapa_info in enumerate(etapas):
                with cols_etapas[idx]:
                    pct_n = etapa_info.get("N_pct", 0)
                    pct_p = etapa_info.get("P2O5_pct", 0)
                    pct_k = etapa_info.get("K2O_pct", 0)
                    kg_etapa_n = round(dosis_n_ha * (pct_n / 100.0), 1)
                    kg_etapa_p = round(dosis_p_ha * (pct_p / 100.0), 1)
                    kg_etapa_k = round(dosis_k_ha * (pct_k / 100.0), 1)
                    
                    st.markdown(f"""
                    <div class="agro-card" style="min-height: 220px;">
                        <h6 style="color:#102B19; font-weight:700; margin-bottom:5px;">{etapa_info.get('etapa')}</h6>
                        <p style="font-size:0.85em; color:#356041;"><em>{etapa_info.get('rol', '')}</em></p>
                        <hr style="border-color: rgba(46, 84, 56, 0.15); margin:8px 0;">
                        <p style="font-size:0.85em; margin:2px 0;"><strong>N ({pct_n}%):</strong> {kg_etapa_n} kg/ha</p>
                        <p style="font-size:0.85em; margin:2px 0;"><strong>P₂O₅ ({pct_p}%):</strong> {kg_etapa_p} kg/ha</p>
                        <p style="font-size:0.85em; margin:2px 0;"><strong>K₂O ({pct_k}%):</strong> {kg_etapa_k} kg/ha</p>
                    </div>
                    """, unsafe_allow_html=True)

        # Nutrientes Secundarios y Micronutrientes
        sec = din.get("extraccion_secundarios_estimada_kg_t", {})
        mic = din.get("micronutrientes_criticos", "Consultar análisis foliar.")
        st.markdown(f"""
        <div class="agro-card">
            <h5 style="color:#102B19; font-weight:700;">🧪 Nutrientes Secundarios & Micronutrientes Esenciales:</h5>
            <p><strong>Extracción de Secundarios por Quintal (qq):</strong> Calcio (CaO): {round(sec.get('Ca_kg_t', 0)*F_QQ, 3)} kg/qq | Magnesio (MgO): {round(sec.get('Mg_kg_t', 0)*F_QQ, 3)} kg/qq | Azufre (S): {round(sec.get('S_kg_t', 0)*F_QQ, 3)} kg/qq</p>
            <p><strong>Demanda Total para {rend_meta} qq/ha:</strong> {round(sec.get('Ca_kg_t', 0)*rend_meta_t, 1)} kg Ca | {round(sec.get('Mg_kg_t', 0)*rend_meta_t, 1)} kg Mg | {round(sec.get('S_kg_t', 0)*rend_meta_t, 1)} kg S por hectárea.</p>
            <p><strong>Micronutrientes Críticos:</strong> {mic}</p>
        </div>
        """, unsafe_allow_html=True)

# ── PESTAÑA 5: ANÁLISIS DE SUELO (OPCIONAL) ───────────────────────────────────
with tab_suelo:
    st.markdown("""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Análisis Químico de Suelo & Descuento Nutricional <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            <strong>Pestaña 100% Opcional:</strong> Si dispones de un análisis químico de suelo emitido por laboratorio para tu finca, introduce aquí los resultados para descontar los nutrientes que ya posee tu tierra. Si no cuentas con análisis de suelo, <strong>no es obligatorio rellenar esta sección</strong>; la calculadora formulará las dosis estándar por eficiencias agronómicas.
        </p>
    </div>
    """, unsafe_allow_html=True)

    sp = st.session_state.suelo_params

    # Toggle de activación del análisis
    col_t1, col_t2 = st.columns([2.2, 1.2])
    with col_t1:
        activar_suelo = st.toggle(
            "🧪 Activar Descuento de Nutrientes del Análisis de Suelo en la Calculadora",
            value=sp.get("activo", False),
            key="toggle_analisis_suelo_activo",
            help="Al activar este interruptor, el N, P₂O₅ y K₂O disponibles calculados abajo se restarán automáticamente de las dosis en la Pestaña 4."
        )
        sp["activo"] = activar_suelo
    with col_t2:
        if activar_suelo:
            st.markdown('<div style="text-align:right; padding-top:6px;"><span style="background:#1565C0; color:white; padding:6px 18px; border-radius:9999px; font-size:0.82rem; font-weight:700; box-shadow:0 2px 8px rgba(21,101,192,0.3);">🟢 DESCUENTO ACTIVADO</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:right; padding-top:6px;"><span style="background:rgba(21,62,32,0.15); color:#153E20; padding:6px 18px; border-radius:9999px; font-size:0.82rem; font-weight:700;">⚪ MODO ESTÁNDAR (INACTIVO)</span></div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("##### 🌍 1. Características Físicas y Capa Arable del Lote:")
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        profundidad = st.number_input(
            "Profundidad Muestreada (cm):",
            min_value=10.0, max_value=60.0, value=float(sp.get("profundidad_cm", 20.0)), step=5.0,
            key="suelo_profundidad"
        )
        sp["profundidad_cm"] = profundidad
    with col_f2:
        da = st.number_input(
            "Densidad Aparente (g/cm³):",
            min_value=0.70, max_value=1.80, value=float(sp.get("da_g_cm3", 1.20)), step=0.05,
            key="suelo_da",
            help="Suelos francos suelen tener 1.20-1.30 g/cm³, arcillosos 1.10-1.25, volcánicos andisoles 0.80-1.0."
        )
        sp["da_g_cm3"] = da
    with col_f3:
        ph_val = st.number_input(
            "pH del Suelo (1:2.5 en agua):",
            min_value=3.5, max_value=9.5, value=float(sp.get("ph", 6.2)), step=0.1,
            key="suelo_ph"
        )
        sp["ph"] = ph_val
    with col_f4:
        texturas_disponibles = ["Franco", "Franco-Arcilloso", "Franco-Arenoso", "Arcilloso Pesado", "Arenoso"]
        tex_idx = texturas_disponibles.index(sp.get("textura", "Franco")) if sp.get("textura", "Franco") in texturas_disponibles else 0
        textura_sel = st.selectbox(
            "Textura Predominante:",
            texturas_disponibles,
            index=tex_idx,
            key="suelo_textura"
        )
        sp["textura"] = textura_sel

    # Cálculo de masa de capa arable
    masa_suelo_t = (profundidad / 100.0) * 10000.0 * da
    factor_kg_ppm = masa_suelo_t / 1000.0

    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.7); border: 1px solid rgba(21,62,32,0.18); border-radius: 12px; padding: 8px 16px; margin: 6px 0 16px 0; font-size: 0.88rem; color: #102B19;">
        ⚖️ <strong>Masa de la Capa Arable Calculada:</strong> <span style="font-weight:700;">{masa_suelo_t:,.0f} toneladas de suelo/ha</span> (Factor de conversión analítico: 1 ppm = {factor_kg_ppm:.2f} kg/ha).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##### 🧪 2. Fertilidad Química del Suelo (Valores de Laboratorio):")
    col_q1, col_q2, col_q3 = st.columns(3)
    
    with col_q1:
        st.markdown("**🌿 Nitrógeno y Materia Orgánica:**")
        mo_val = st.number_input(
            "Materia Orgánica (% MO):",
            min_value=0.1, max_value=15.0, value=float(sp.get("mo_pct", 2.5)), step=0.2,
            key="suelo_mo"
        )
        sp["mo_pct"] = mo_val
        n_calc_mo = round(mo_val * 10.0 * (da / 1.20), 1)
        n_disp_in = st.number_input(
            "Aporte Neto de N del Suelo (kg N/ha):",
            min_value=0.0, max_value=300.0, value=float(sp.get("n_disp_kg_ha", n_calc_mo)), step=2.0,
            key="suelo_n_disp",
            help="Calculado a partir de la tasa de mineralización de la Materia Orgánica durante el ciclo del cultivo."
        )
        sp["n_disp_kg_ha"] = n_disp_in

    with col_q2:
        st.markdown("**🌾 Fósforo Disponible (P):**")
        p_ppm_val = st.number_input(
            "Fósforo en Análisis (ppm o mg/kg P):",
            min_value=0.0, max_value=300.0, value=float(sp.get("p_ppm", 15.0)), step=1.0,
            key="suelo_p_ppm"
        )
        sp["p_ppm"] = p_ppm_val
        
        factor_disp_p = 0.25 if (5.8 <= ph_val <= 7.2) else 0.18
        p2o5_calc_asimilable = round(p_ppm_val * factor_kg_ppm * 2.29 * factor_disp_p, 1)
        
        p2o5_disp_in = st.number_input(
            "Fósforo Asimilable del Suelo (kg P₂O₅/ha):",
            min_value=0.0, max_value=300.0, value=float(sp.get("p2o5_disp_kg_ha", p2o5_calc_asimilable)), step=2.0,
            key="suelo_p2o5_disp",
            help="Fracción de P₂O₅ que la raíz puede interceptar y absorber efectivamente en el ciclo."
        )
        sp["p2o5_disp_kg_ha"] = p2o5_disp_in

    with col_q3:
        st.markdown("**🍌 Potasio Intercambiable (K):**")
        k_val_in = st.number_input(
            "Potasio en Análisis (cmol(+)/kg o meq/100g):",
            min_value=0.0, max_value=5.0, value=float(sp.get("k_val", 0.45)), step=0.05,
            key="suelo_k_val",
            help="Valores óptimos suelen oscilar entre 0.35 y 0.80 cmol(+)/kg."
        )
        sp["k_val"] = k_val_in
        
        k2o_calc_asimilable = round(k_val_in * 390.0 * factor_kg_ppm * 1.205 * 0.10, 1)
        
        k2o_disp_in = st.number_input(
            "Potasio Asimilable del Suelo (kg K₂O/ha):",
            min_value=0.0, max_value=400.0, value=float(sp.get("k_disp_kg_ha", k2o_calc_asimilable)), step=5.0,
            key="suelo_k2o_disp",
            help="Fracción de K₂O en solución y fácilmente intercambiable absorbida en el ciclo."
        )
        sp["k_disp_kg_ha"] = k2o_disp_in

    st.markdown("##### ⚖️ 3. Bases Secundarias y Balance Catiónico:")
    col_b1, col_b2, col_b3, col_b4 = st.columns(4)
    with col_b1:
        ca_in = st.number_input("Calcio Ca (cmol/kg):", min_value=0.0, max_value=35.0, value=float(sp.get("ca_cmol", 6.5)), step=0.5, key="suelo_ca")
        sp["ca_cmol"] = ca_in
    with col_b2:
        mg_in = st.number_input("Magnesio Mg (cmol/kg):", min_value=0.0, max_value=15.0, value=float(sp.get("mg_cmol", 2.2)), step=0.2, key="suelo_mg")
        sp["mg_cmol"] = mg_in
    with col_b3:
        rel_ca_mg = round(ca_in / mg_in, 2) if mg_in > 0 else 0.0
        estado_ca_mg = "Óptimo (3 a 5)" if 3.0 <= rel_ca_mg <= 5.0 else ("Bajo (<3)" if rel_ca_mg < 3.0 else "Alto (>5)")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.7); border-radius:12px; padding:10px 14px; border:1px solid rgba(21,62,32,0.18);">
            <div style="font-size:0.80rem; color:#244C2E; font-weight:600;">Relación Ca:Mg</div>
            <div style="font-size:1.25rem; font-weight:700; color:#102B19;">{rel_ca_mg}</div>
            <div style="font-size:0.75rem; color:#1B5E20; font-weight:600;">{estado_ca_mg}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_b4:
        rel_mg_k = round(mg_in / k_val_in, 2) if k_val_in > 0 else 0.0
        estado_mg_k = "Equilibrado (2 a 5)" if 2.0 <= rel_mg_k <= 5.0 else ("Bajo (<2)" if rel_mg_k < 2.0 else "Antagonismo Mg/K (>5)")
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.7); border-radius:12px; padding:10px 14px; border:1px solid rgba(21,62,32,0.18);">
            <div style="font-size:0.80rem; color:#244C2E; font-weight:600;">Relación Mg:K</div>
            <div style="font-size:1.25rem; font-weight:700; color:#102B19;">{rel_mg_k}</div>
            <div style="font-size:0.75rem; color:#1B5E20; font-weight:600;">{estado_mg_k}</div>
        </div>
        """, unsafe_allow_html=True)

    # Tarjeta de Resumen y Estado
    if activar_suelo:
        sacos_dap_ahor = round(p2o5_disp_in / 0.46 / 50.0, 1)
        sacos_mop_ahor = round(k2o_disp_in / 0.60 / 50.0, 1)
        sacos_urea_ahor = round(n_disp_in / 0.46 / 50.0, 1)
        st.markdown(f"""
        <div class="agro-card" style="background: rgba(227, 242, 253, 0.94); border-left: 6px solid #1565C0; margin-top: 18px;">
            <h4 style="color:#0D47A1; font-family:'Playfair Display', Georgia, serif; font-weight:700; margin-bottom:10px;">
                📋 Nutrientes Asimilables del Suelo que se Descontarán:
            </h4>
            <p style="color:#0A2540; font-size:0.92rem; margin-bottom:10px;">
                Al tener activado el análisis de suelo, estos valores se restarán directamente de la dosis en la pestaña <strong>🌱 Nutrición & Curvas</strong>:
            </p>
            <ul style="line-height:2.0; font-size:0.92rem; color:#0A2540;">
                <li>🌿 <strong>Nitrógeno del Suelo (N):</strong> <span style="font-weight:700; color:#0D47A1;">-{n_disp_in} kg N/ha</span> (~{sacos_urea_ahor} sacos de Urea ahorrados)</li>
                <li>🌾 <strong>Fósforo Asimilable (P₂O₅):</strong> <span style="font-weight:700; color:#0D47A1;">-{p2o5_disp_in} kg P₂O₅/ha</span> (~{sacos_dap_ahor} sacos de DAP ahorrados)</li>
                <li>🍌 <strong>Potasio Asimilable (K₂O):</strong> <span style="font-weight:700; color:#0D47A1;">-{k2o_disp_in} kg K₂O/ha</span> (~{sacos_mop_ahor} sacos de MOP ahorrados)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="agro-card" style="background: rgba(255, 255, 255, 0.85); border-left: 6px solid #555; margin-top: 18px;">
            <h5 style="color:#333; font-weight:700;">⚪ Modo Estándar Activo (Sin descuento de análisis de suelo)</h5>
            <p style="color:#555; font-size:0.90rem; margin:0;">
                El interruptor superior está apagado. La calculadora formulará la fertilización asumiendo las eficiencias convencionales de absorción sin restar aportes analíticos de suelo. Actívalo si deseas calibrar las dosis exactas con tu informe de laboratorio.
            </p>
        </div>
        """, unsafe_allow_html=True)

# ── PESTAÑA 6: CALCULADORA DE COSTOS & INVENTARIO ─────────────────────────────
with tab_costos:
    # Cargar productos
    catalogo_dict = db_catalogo_completo if db_catalogo_completo else {}
    total_insumos = len(catalogo_dict)

    st.markdown(f"""
    <div class="section-header-card">
        <div class="section-bracket">
            <span class="bracket">[</span> Calculadora de Inversión & Catálogo Comercial Completo ({total_insumos} Insumos) <span class="bracket">]</span>
        </div>
        <p style="margin: 0; color: #153E20; font-size: 0.94rem; font-weight: 500;">
            Catálogo agronómico integral con <strong>{total_insumos} insumos comerciales</strong> extraídos e indexados directamente desde tus fichas técnicas oficiales (insecticidas, fungicidas, herbicidas, biológicos y fertilizantes). Calcula presupuesto por hectárea, por quintal y por bomba de 20L en Córdobas (C$).
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Definición de categorías para filtrado dinámico
    categorias_map = {
        f"🌿 Todos los Insumos ({total_insumos} disponibles)": None,
        "🐛 Insecticidas y Acaricidas": ["Insecticida", "Insecticida/Acaricida", "Insecticida / Acaricida", "Insecticida/Nematicida", "Insecticida / Nematicida", "Insecticida (Tratamiento Semilla)"],
        "🍄 Fungicidas y Bactericidas": ["Fungicida", "Bactericida / Fungicida", "Fungicida / Insecticida", "Fungicida (Tratamiento Semilla)"],
        "🌾 Herbicidas": ["Herbicida", "Herbicida / Desecante"],
        "🦠 Biológicos y Nematicidas": ["Biológico / Biofungicida", "Biológico / Bioinsecticida", "Biológico / Fungicida Acaricida", "Nematicida", "Insecticida/Nematicida", "Insecticida / Nematicida"],
        "🧪 Fertilizantes Edáficos (Suelo)": ["Fertilizante Edáfico"],
        "🍃 Fertilizantes Foliares y Nutrición": ["Fertilizante Foliar"]
    }
    if not catalogo_dict:
        # Fallback de emergencia
        catalogo_dict = {
            "Match 050 EC": {"categoria": "Insecticida", "i_a": "Lufenuron (50 g/L)", "grupo": "IRAC 15", "dosis_ha": 0.4, "dosis_bomba": 40.0, "unidad": "L/ha", "uso_principal": "Gusano cogollero"},
            "Proclaim 05 SG": {"categoria": "Insecticida", "i_a": "Benzoato de Emamectina (50 g/kg)", "grupo": "IRAC 6", "dosis_ha": 0.25, "dosis_bomba": 25.0, "unidad": "Kg/ha", "uso_principal": "Lepidópteros difíciles"},
            "Actara 25 WG": {"categoria": "Insecticida", "i_a": "Tiametoxam (250 g/kg)", "grupo": "IRAC 4A", "dosis_ha": 0.2, "dosis_bomba": 20.0, "unidad": "Kg/ha", "uso_principal": "Mosca blanca y chupadores"},
            "Ridomil Gold MZ": {"categoria": "Fungicida", "i_a": "Mefenoxam + Mancozeb (40 + 640 g/kg)", "grupo": "FRAC 4 + M3", "dosis_ha": 2.5, "dosis_bomba": 60.0, "unidad": "Kg/ha", "uso_principal": "Tizón tardío, Pythium"},
            "Amistar Top": {"categoria": "Fungicida", "i_a": "Azoxistrobina + Difenoconazol (200 + 125 g/L)", "grupo": "FRAC 11 + 3", "dosis_ha": 0.5, "dosis_bomba": 35.0, "unidad": "L/ha", "uso_principal": "Roya, Antracnosis"},
            "Score 250 EC": {"categoria": "Fungicida", "i_a": "Difenoconazol (250 g/L)", "grupo": "FRAC 3", "dosis_ha": 0.35, "dosis_bomba": 25.0, "unidad": "L/ha", "uso_principal": "Manchas foliares"},
            "Mertect 500 SC": {"categoria": "Fungicida", "i_a": "Tiabendazol (500 g/L)", "grupo": "FRAC 1", "dosis_ha": 1.0, "dosis_bomba": 50.0, "unidad": "L/ha", "uso_principal": "Fusarium, pudriciones"},
            "Solvigo": {"categoria": "Insecticida/Nematicida", "i_a": "Abamectina + Tiametoxam", "grupo": "IRAC 6 + 4A", "dosis_ha": 1.5, "dosis_bomba": 80.0, "unidad": "L/ha", "uso_principal": "Nematodos y chupadores"}
        }

    col_cat, col_prod = st.columns([1.1, 1.9])
    with col_cat:
        cat_seleccionada = st.selectbox(
            "📂 Filtrar por Categoría:",
            list(categorias_map.keys()),
            key="filtro_cat_costos"
        )
    
    # Filtrar productos disponibles
    grupos_filtro = categorias_map[cat_seleccionada]
    if grupos_filtro is None:
        prods_filtrados = sorted(list(catalogo_dict.keys()))
    else:
        prods_filtrados = sorted([
            k for k, v in catalogo_dict.items()
            if v.get("categoria") in grupos_filtro
        ])
    
    if not prods_filtrados:
        prods_filtrados = sorted(list(catalogo_dict.keys()))

    with col_prod:
        producto_sel = st.selectbox(
            f"Selecciona el Producto Comercial ({len(prods_filtrados)} insumos en lista):",
            prods_filtrados,
            key="selector_producto_comercial_completo"
        )

    prod_info = catalogo_dict.get(producto_sel, {})
    categoria_prod = prod_info.get("categoria", "Insumo Agrícola")
    ia_prod = prod_info.get("i_a", "Ingrediente Activo registrado")
    grupo_prod = prod_info.get("grupo", "No especificado")
    dosis_defecto = float(prod_info.get("dosis_ha", 0.5))
    dosis_bomba_defecto = prod_info.get("dosis_bomba", 35.0)
    unidad_tecnica = prod_info.get("unidad", "L/ha")
    espectro_prod = prod_info.get("uso_principal", "Control fitosanitario o nutrición vegetal.")
    es_edafico = "edáfico" in categoria_prod.lower() or "suelo" in categoria_prod.lower()

    # Tarjeta de Especificación Técnica del Insumo Seleccionado
    bomba_badge = f"{dosis_bomba_defecto} cc o g / bomba 20L" if not es_edafico and dosis_bomba_defecto else "Aplicación al suelo (edáfico / voleo)"
    
    st.markdown(f"""
    <div class="agro-card" style="background: rgba(255, 255, 255, 0.88); border-left: 6px solid #1E5128; margin: 12px 0 20px 0; padding: 18px 22px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px;">
            <div style="font-family:'Playfair Display', Georgia, serif; font-size:1.35rem; color:#0A2211; font-weight:700;">
                🏷️ {producto_sel}
            </div>
            <span style="background: linear-gradient(135deg, #1E5128 0%, #153E20 100%); color: #FFFFFF; font-size: 0.84rem; font-weight: 600; padding: 5px 16px; border-radius: 9999px; box-shadow: 0 2px 8px rgba(21, 62, 32, 0.25);">
                {categoria_prod}
            </span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 10px; font-size: 0.92rem; line-height: 1.6;">
            <div>🔬 <strong>Ingrediente Activo:</strong> <br/><span style="color:#102B19; font-weight:600;">{ia_prod}</span></div>
            <div>🧬 <strong>Modo de Acción / Grupo:</strong> <br/><span style="color:#102B19; font-weight:600;">{grupo_prod}</span></div>
            <div>⚖️ <strong>Dosis Técnica Recomendada:</strong> <br/><span style="color:#153E20; font-weight:700;">{dosis_defecto} {unidad_tecnica}</span></div>
            <div>🎒 <strong>Dosis por Bomba (20 L):</strong> <br/><span style="color:#153E20; font-weight:700;">{bomba_badge}</span></div>
        </div>
        <div style="margin-top: 12px; padding-top: 10px; border-top: 1px dashed rgba(21, 62, 32, 0.20); font-size: 0.88rem; color: #1B4D27;">
            🎯 <strong>Espectro y Plagas / Funciones:</strong> {espectro_prod}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_vol, col_dosis, col_costo = st.columns(3)
    with col_vol:
        hectareas = st.number_input("Número de Hectáreas a tratar:", min_value=0.1, max_value=1000.0, value=1.0, step=0.5, key="num_hectareas_costos")
    with col_dosis:
        dosis_ha = st.number_input(
            f"Dosis a aplicar ({unidad_tecnica}):",
            min_value=0.01,
            max_value=2500.0,
            value=float(dosis_defecto),
            step=0.1 if dosis_defecto < 10 else 5.0,
            key=f"dosis_ha_{producto_sel}",
            help="Puedes calibrar o ajustar la dosis según la necesidad del lote"
        )
    with col_costo:
        unidad_precio = "litro o kg" if not es_edafico else "saco o quintal o kg"
        precio_unitario = st.number_input(
            f"Precio en Tienda (C$ por {unidad_precio}):",
            min_value=0.0,
            max_value=35000.0,
            value=0.0,
            step=50.0,
            key=f"precio_{producto_sel}",
            help="Ingresa el precio de cotización con tu distribuidor local en Córdobas (C$)"
        )

    # Cálculos agronómicos y financieros
    total_producto = dosis_ha * hectareas
    costo_total = total_producto * precio_unitario
    bombas_20l = hectareas * 10
    costo_por_bomba = costo_total / bombas_20l if bombas_20l > 0 else 0

    st.markdown("---")
    
    if precio_unitario == 0:
        costo_bomba_display = '<span style="color:#527358; font-size:1.05em; font-weight:600;">C$ 0.00 <em style="font-size:0.82em; font-weight:normal;">(Ingresa el precio cotizado en tienda)</em></span>'
        costo_total_display = '<span style="color:#102B19; font-size:1.3em; font-weight:700; background: rgba(176, 195, 165, 0.55); padding: 5px 18px; border-radius: 9999px; border: 1.5px dashed rgba(21, 62, 32, 0.35); display: inline-block;">C$ 0.00 <em style="font-size:0.75em; font-weight:normal; color:#244C2E;">(Ingresa el precio en tienda)</em></span>'
    else:
        costo_bomba_display = f'<span style="color:#153E20; font-size:1.3em; font-weight:bold;">C$ {costo_por_bomba:,.2f}</span>'
        costo_total_display = f'<span style="color:#0E2916; font-size:1.55em; font-weight:bold; background: rgba(176, 195, 165, 0.65); padding: 5px 20px; border-radius: 9999px; border: 1.5px solid rgba(21, 62, 32, 0.35); display: inline-block;">C$ {costo_total:,.2f}</span>'

    # Detalle especial para fertilizantes granulados edáficos
    equivalencia_qq = ""
    if es_edafico:
        sacos_46 = total_producto / 46.0 if total_producto > 0 else 0
        qq_totales = total_producto / 45.36 if total_producto > 0 else 0
        equivalencia_qq = f"<li>🌾 <strong>Equivalencia en Quintales (qq):</strong> <span style=\"color:#102B19; font-weight:600;\">{qq_totales:.2f} qq</span> (aprox. {sacos_46:.1f} sacos de 46 kg / 100 lb)</li>"

    detalle_bomba_line = f"<li>🎒 <strong>Equivalente en Bombas de 20L (10 bombas/ha):</strong> <span style=\"color:#102B19;\">{bombas_20l:.0f} bombas de espalda</span></li>\n<li>💧 <strong>Costo por Bomba de 20L:</strong> {costo_bomba_display}</li>" if not es_edafico else f"<li>🚜 <strong>Tipo de Aplicación:</strong> <span style=\"color:#102B19; font-weight:600;\">Fertilización Edáfica al Voleo / Incorporada al suelo</span></li>"

    st.markdown(f"""<div class="agro-card">
<h4 style="color:#102B19; font-family:'Playfair Display', Georgia, serif; margin-bottom:14px; font-weight:700;">📊 Presupuesto del Insumo Seleccionado:</h4>
<ul style="list-style-type: none; padding-left: 5px; line-height: 2.2;">
<li>🌿 <strong>Producto Comercial:</strong> <span style="color:#102B19; font-weight:700;">{producto_sel}</span> <span style="color:#244C2E; font-size:0.9em;">({categoria_prod})</span></li>
<li>⚖️ <strong>Dosis formulada:</strong> <span style="color:#102B19;">{dosis_ha:.2f} {unidad_tecnica}</span></li>
<li>📦 <strong>Volumen Total Requerido para {hectareas} ha:</strong> <span style="color:#102B19; font-weight:700;">{total_producto:,.2f} {unidad_tecnica.replace('/ha', '')}</span></li>
{equivalencia_qq}
{detalle_bomba_line}
<li>💰 <strong>Inversión Total Estimada:</strong> {costo_total_display}</li>
</ul>
<div style="margin-top:14px; font-size:0.85rem; color:#2D5837; border-top: 1px solid rgba(46, 84, 56, 0.15); padding-top:10px;">
ℹ️ <em>Valores calculados en Córdobas nicaragüenses (C$). El catálogo completo incluye {total_insumos} insumos comerciales disponibles en agroservicios del país y extraídos de las fichas técnicas locales. El precio unitario inicia en C$ 0 para que digites la cotización de tu proveedor local.</em>
</div>
</div>""", unsafe_allow_html=True)

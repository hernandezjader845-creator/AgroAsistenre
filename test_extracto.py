import re

STOP_WORDS = {
    "que", "cual", "cuales", "como", "cuando", "donde", "quien", "por", "para", "con", "sin",
    "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas", "aquel", "aquella",
    "tiene", "tengo", "tener", "esta", "estan", "cultivo", "cultivos", "planta",
    "plantas", "hoja", "hojas", "mira", "foto", "imagen", "ayuda", "saber", "hola", "buenos",
    "dias", "tardes", "noches", "saludos", "favor", "gracias", "muchas", "algo", "nada",
    "todo", "bien", "mal", "hacer", "hago", "puedo", "debo", "deberia", "sera", "seria",
    "recomiendas", "recomendar", "producto", "productos", "quimico", "remedio"
}

def extraer_extracto(texto, palabras_clave, max_chars=1200):
    if not texto:
        return ""
    if len(texto) <= max_chars:
        return texto
        
    # Buscar la primera ocurrencia de dosis o de alguna palabra clave
    keywords_busqueda = list(palabras_clave) + ["dosis", "litros", "l/ha", "g/ha", "kg/ha", "ml/"]
    pos_min = -1
    texto_lower = texto.lower()
    for kw in keywords_busqueda:
        p = texto_lower.find(kw)
        if p != -1 and (pos_min == -1 or p < pos_min):
            pos_min = p
            
    if pos_min == -1:
        return texto[:max_chars]
        
    inicio = max(0, pos_min - 200)
    fin = min(len(texto), inicio + max_chars)
    return ("..." if inicio > 0 else "") + texto[inicio:fin] + ("..." if fin < len(texto) else "")

print("Script de prueba OK")

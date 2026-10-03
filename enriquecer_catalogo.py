import json
import re

with open("C:/antigravity 1/Biblioteca_Agronomica/base_conocimiento_agroquimicos.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# Diccionario maestro de nombres comerciales conocidos y sus I.A. comunes
catalogo_maestro = {
    "alto_10_sl": ("Alto 10 SL", "Fungicida", "Cyproconazole", "FRAC 3"),
    "amistar_50_wg": ("Amistar 50 WG", "Fungicida", "Azoxystrobin", "FRAC 11"),
    "amistar_full": ("Amistar Full", "Fungicida", "Azoxystrobin + Difenoconazol", "FRAC 11 + 3"),
    "amistar_ztra": ("Amistar Xtra", "Fungicida", "Azoxystrobin + Cyproconazole", "FRAC 11 + 3"),
    "amistaropti": ("Amistar Opti", "Fungicida", "Azoxystrobin + Clorotalonil", "FRAC 11 + M5"),
    "antracol_70_wp": ("Antracol 70 WP", "Fungicida", "Propineb", "FRAC M3"),
    "arko_80_wp": ("Arko 80 WP", "Fungicida", "Mancozeb", "FRAC M3"),
    "avante_72_wp": ("Avante 72 WP", "Fungicida", "Mancozeb + Metalaxil", "FRAC M3 + 4"),
    "bankitr_25sc": ("Bankit 25 SC", "Fungicida", "Azoxystrobin", "FRAC 11"),
    "bravo_gold": ("Bravo Gold", "Fungicida", "Clorotalonil + Mefenoxam", "FRAC M5 + 4"),
    "pa_bravo_72_sc": ("Bravo 72 SC", "Fungicida", "Clorotalonil", "FRAC M5"),
    "bravonil": ("Bravonil 720 SC", "Fungicida", "Clorotalonil", "FRAC M5"),
    "daconil": ("Daconil 720 SC", "Fungicida", "Clorotalonil", "FRAC M5"),
    "cydome_30_sc": ("Cydome 30 SC", "Fungicida", "Cyproconazole", "FRAC 3"),
    "folio_gold": ("Folio Gold 440 SC", "Fungicida", "Mefenoxam + Clorotalonil", "FRAC 4 + M5"),
    "kasumin_2_sl": ("Kasumin 2 SL", "Bactericida/Fungicida", "Kasugamicina", "FRAC 24"),
    "mertect_500_sc": ("Mertect 500 SC", "Fungicida", "Thiabendazol", "FRAC 1"),
    "miravis_duo": ("Miravis Duo", "Fungicida", "Adepidyn + Difenoconazol", "FRAC 7 + 3"),
    "orondisr_opti": ("Orondis Opti", "Fungicida", "Oxathiapiprolin + Clorotalonil", "FRAC 49 + M5"),
    "prix_72_sc": ("Prix 72 SC", "Fungicida", "Clorotalonil", "FRAC M5"),
    "reflect_125_ec": ("Reflect 125 EC", "Fungicida", "Isopyrazam", "FRAC 7"),
    "revus_250_sc": ("Revus 250 SC", "Fungicida", "Mandipropamid", "FRAC 40"),
    "revus_opti": ("Revus Opti", "Fungicida", "Mandipropamid + Clorotalonil", "FRAC 40 + M5"),
    "sico_250_ec": ("Sico 250 EC", "Fungicida", "Difenoconazol", "FRAC 3"),
    "sphere_max": ("Sphere Max", "Fungicida", "Trifloxystrobin + Cyproconazole", "FRAC 11 + 3"),
    "taspa_500_ec": ("Taspa 500 EC", "Fungicida", "Difenoconazol + Propiconazol", "FRAC 3 + 3"),
    "tranca_72_wp": ("Tranca 72 WP", "Fungicida", "Mancozeb + Cymoxanil", "FRAC M3 + 27"),
    "verdadero_600_wg": ("Verdadero 600 WG", "Fungicida/Insecticida", "Thiamethoxam + Difenoconazol", "IRAC 4A + FRAC 3"),
    "vibrance": ("Vibrance", "Fungicida", "Sedaxane", "FRAC 7"),
    "infinito": ("Infinito", "Fungicida", "Propamocarb + Fluopicolide", "FRAC 28 + 43"),
    "nativo": ("Nativo 75 WG", "Fungicida", "Tebuconazol + Trifloxystrobin", "FRAC 3 + 11"),
    "score": ("Score 250 EC", "Fungicida", "Difenoconazol", "FRAC 3"),
    "ridomil_gold": ("Ridomil Gold MZ", "Fungicida", "Mefenoxam + Mancozeb", "FRAC 4 + M3"),
    
    # Insecticidas
    "actellic": ("Actellic 50 EC", "Insecticida", "Pirimiphos-methyl", "IRAC 1B"),
    "armero_35_sc": ("Armero 35 SC", "Insecticida", "Imidacloprid", "IRAC 4A"),
    "cepadik_57_sg": ("Cepadik 57 SG", "Insecticida", "Emamectina benzoato", "IRAC 6"),
    "curbix_plus": ("Curbix Plus", "Insecticida", "Etioprole + Acetamiprid", "IRAC 2B + 4A"),
    "curacron": ("Curacron 500 EC", "Insecticida", "Profenofos", "IRAC 1B"),
    "curyom": ("Curyom 550 EC", "Insecticida", "Profenofos + Lufenuron", "IRAC 1B + 15"),
    "decis": ("Decis 2.5 EC", "Insecticida", "Deltametrina", "IRAC 3A"),
    "dismetrina": ("Dismetrina 25 EC", "Insecticida", "Permetrina", "IRAC 3A"),
    "kloister_10_sc": ("Kloister 10 SC", "Insecticida", "Bifentrina", "IRAC 3A"),
    "oberonspeed": ("Oberon Speed", "Insecticida/Acaricida", "Spiromesifen + Abamectina", "IRAC 23 + 6"),
    "raptan": ("Raptan 44 EC", "Insecticida", "Clorpirifos + Cipermetrina", "IRAC 1B + 3A"),
    "salvate_20_sp": ("Salvate 20 SP", "Insecticida", "Acetamiprid", "IRAC 4A"),
    "task_25_wg": ("Task 25 WG", "Insecticida", "Thiamethoxam", "IRAC 4A"),
    "volpix": ("Volpix 30 OD", "Insecticida", "Spirotetramat + Imidacloprid", "IRAC 23 + 4A"),
    "solvigo": ("Solvigo", "Insecticida/Nematicida", "Abamectina + Tiametoxam", "IRAC 6 + 4A"),
    "actara": ("Actara 25 WG", "Insecticida", "Thiamethoxam", "IRAC 4A"),
    "vertimec": ("Vertimec 018 EC", "Insecticida/Acaricida", "Abamectina", "IRAC 6"),
    "match": ("Match 50 EC", "Insecticida", "Lufenuron", "IRAC 15"),
    "movento": ("Movento 150 SC", "Insecticida", "Spirotetramat", "IRAC 23"),
    "muralla": ("Muralla Delta", "Insecticida", "Imidacloprid + Deltametrina", "IRAC 4A + 3A"),
    "karate_zeon": ("Karate Zeon 2.5 CS", "Insecticida", "Lambda-cihalotrina", "IRAC 3A"),
    "sivanto_prime": ("Sivanto Prime", "Insecticida", "Flupyradifurone", "IRAC 4D"),
    "voliam_flexi": ("Voliam Flexi", "Insecticida", "Thiamethoxam + Chlorantraniliprole", "IRAC 4A + 28"),
    
    # Herbicidas
    "fusilade": ("Fusilade 12.5 EC", "Herbicida", "Fluazifop-P-butil", "HRAC 1"),
    "flex": ("Flex 25 SL", "Herbicida", "Fomesafen", "HRAC 14"),
    "gesapax": ("Gesapax 500 SC", "Herbicida", "Ametrina", "HRAC 5"),
    "gesaprim": ("Gesaprim 90 WG", "Herbicida", "Atrazina", "HRAC 5"),
    "gramuron": ("Gramuron", "Herbicida", "Paraquat + Diuron", "HRAC 22 + 7"),
    "touchdown": ("Touchdown Forte", "Herbicida", "Glifosato", "HRAC 9")
}

actualizados = 0
for k, v in db.items():
    nombre_limpio = k.lower()
    
    # 1. Buscar en catálogo maestro
    encontrado = False
    for patron, datos_m in catalogo_maestro.items():
        if patron in nombre_limpio:
            v["nombre_comercial"] = datos_m[0]
            v["tipo"] = datos_m[1]
            v["i_a"] = datos_m[2]
            v["grupo_frac_irac"] = datos_m[3]
            encontrado = True
            actualizados += 1
            break
            
    if not encontrado:
        # Generar nombre comercial limpio basado en el archivo
        v["nombre_comercial"] = k.replace("_", " ").title()
        texto = v.get("texto_ficha", "").lower()
        if "fungicida" in texto:
            v["tipo"] = "Fungicida"
        elif "insecticida" in texto:
            v["tipo"] = "Insecticida"
        elif "herbicida" in texto:
            v["tipo"] = "Herbicida"
        elif "fertilizante" in texto or "foliar" in texto:
            v["tipo"] = "Nutrición/Foliar"

with open("C:/antigravity 1/Biblioteca_Agronomica/base_conocimiento_agroquimicos.json", "w", encoding="utf-8") as f:
    json.dump(db, f, indent=4, ensure_ascii=False)

print(f"✅ Catálogo enriquecido con éxito. {actualizados} marcas comerciales líderes vinculadas directamente a ingredientes activos y grupos FRAC/IRAC.")

import json

with open("C:/antigravity 1/Biblioteca_Agronomica/base_conocimiento_agroquimicos.json", "r", encoding="utf-8") as f:
    db = json.load(f)

fungicidas = []
insecticidas = []
herbicidas = []

for k, v in db.items():
    nombre_comercial = k.replace("_", " ").title()
    ia = v.get("ingrediente_activo", "")
    tipo = v.get("tipo", "").lower()
    grupo = v.get("grupo_frac_irac", "")
    
    if "fungicida" in tipo or "frac" in grupo.lower():
        fungicidas.append(f"{nombre_comercial} (IA: {ia} | {grupo})")
    elif "insecticida" in tipo or "irac" in grupo.lower():
        insecticidas.append(f"{nombre_comercial} (IA: {ia} | {grupo})")
    elif "herbicida" in tipo or "hrac" in grupo.lower():
        herbicidas.append(f"{nombre_comercial} (IA: {ia} | {grupo})")

print(f"Total Fungicidas: {len(fungicidas)}")
print("Ejemplos Fungicidas:", fungicidas[:10])
print(f"\nTotal Insecticidas: {len(insecticidas)}")
print("Ejemplos Insecticidas:", insecticidas[:10])
print(f"\nTotal Herbicidas: {len(herbicidas)}")
print("Ejemplos Herbicidas:", herbicidas[:10])

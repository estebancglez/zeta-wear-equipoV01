import csv
import os

POLITICAS = {
    "AX": "Revisión continua y automatizada. Colchón de seguridad mínimo debido a la alta estabilidad de la demanda. Automatización alta mediante punto de pedido automático (JIT/VMI).",
    "AY": "Revisión semanal periódica. Colchón de seguridad moderado para cubrir la variabilidad en ventas. Automatización media con supervisión de alertas.",
    "AZ": "Revisión continua por especialista. Colchón de seguridad alto o gestión bajo pedido dada la alta variabilidad y alto impacto financiero.",
    "BX": "Revisión quincenal automatizada. Colchón de seguridad bajo ante demanda predecible. Automatización mediante regla fija de punto de pedido (ROP).",
    "BY": "Revisión mensual estándar. Colchón de seguridad moderado. Automatización parcial con revisiones periódicas de niveles de stock.",
    "BZ": "Revisión quincenal/mensual estrecha. Colchón de seguridad alto o compra contra pedido para mitigar el riesgo de sobrestock en artículos de demanda errática.",
    "CX": "Revisión trimestral automatizada sin intervención. Colchón de seguridad mínimo. Automatización total mediante lote económico de compra (EOQ).",
    "CY": "Revisión trimestral periódica. Colchón de seguridad bajo/moderado. Reaprovisionamiento automatizado por lote con supervisión mínima.",
    "CZ": "Revisión bajo demanda o por excepción. Colchón de seguridad mínimo o nulo; priorizar compra bajo pedido o evaluar descatalogación para reducir costes de almacenamiento."
}

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abc_path = os.path.join(base_dir, "resultados", "abc.csv")
    xyz_path = os.path.join(base_dir, "resultados", "xyz.csv")
    clasificacion_path = os.path.join(base_dir, "resultados", "clasificacion.csv")
    politicas_path = os.path.join(base_dir, "resultados", "politicas.md")

    with open(abc_path, mode="r", encoding="utf-8") as f:
        abc_data = {row["sku"]: row for row in csv.DictReader(f)}

    with open(xyz_path, mode="r", encoding="utf-8") as f:
        xyz_data = {row["sku"]: row for row in csv.DictReader(f)}

    clasificacion = []
    celdas_ocupadas = set()

    for sku, abc_info in abc_data.items():
        xyz_info = xyz_data.get(sku, {})
        clase_abc = abc_info.get("clase_abc", "")
        clase_xyz = xyz_info.get("clase_xyz", "")
        cv = xyz_info.get("cv", "")
        celda = f"{clase_abc}{clase_xyz}"
        celdas_ocupadas.add(celda)

        clasificacion.append({
            "sku": sku,
            "clase_abc": clase_abc,
            "cv": cv,
            "clase_xyz": clase_xyz,
            "celda": celda
        })

    os.makedirs(os.path.dirname(clasificacion_path), exist_ok=True)
    fieldnames = ["sku", "clase_abc", "cv", "clase_xyz", "celda"]

    with open(clasificacion_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in clasificacion:
            writer.writerow(r)

    # Ordenar celdas ocupadas en orden matriz (A..C, X..Z)
    orden_matriz = [f"{a}{x}" for a in ["A", "B", "C"] for x in ["X", "Y", "Z"]]
    celdas_ordenadas = [c for c in orden_matriz if c in celdas_ocupadas]

    with open(politicas_path, mode="w", encoding="utf-8") as f:
        f.write("# Políticas de Gestión del Inventario (Matriz ABC×XYZ)\n\n")
        for celda in celdas_ordenadas:
            politica = POLITICAS.get(celda, "Política no definida.")
            f.write(f"- **Celda {celda}**: {politica}\n")

if __name__ == "__main__":
    main()

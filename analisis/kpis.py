import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    master_path = os.path.join(base_dir, "datos", "ex2_sku_master.csv")
    monthly_path = os.path.join(base_dir, "datos", "ex2_monthly_sales.csv")
    daily_path = os.path.join(base_dir, "datos", "ex1_demand_daily.csv")
    output_path = os.path.join(base_dir, "resultados", "kpis.csv")

    # Leer maestro de SKUs
    with open(master_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        skus = list(reader)

    # Verificación de fuentes de datos disponibles en el repositorio:
    # 1. Rotación anual = demanda anual / stock medio
    #    - demanda_anual existe en ex2_sku_master.csv.
    #    - stock_medio NO existe en ningún fichero del repositorio.
    # 2. Días con rotura de stock en 2026 por SKU:
    #    - ex1_demand_daily.csv contiene una serie diaria agregada de 120 días (sin desglose por SKU ni cobertura de todo 2026).
    #    - NO existe una serie diaria de rotura de stock por SKU para el año 2026.

    rows = []
    for row in skus:
        sku = row["sku"]
        rotacion_anual = "N/A (Sin dato de stock medio)"
        dias_rotura_stock_2026 = "N/A (Sin serie diaria por SKU)"
        rows.append({
            "sku": sku,
            "rotacion_anual": rotacion_anual,
            "dias_rotura_stock_2026": dias_rotura_stock_2026
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["sku", "rotacion_anual", "dias_rotura_stock_2026"]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Archivo generado exitosamente en: {output_path}")
    print("Auditoría de datos realizada:")
    print(" - Rotación Anual: No se puede calcular sin inventar datos. El 'stock medio' no está disponible en el catálogo ni en las ventas.")
    print(" - Días con rotura de stock 2026: No se puede calcular por SKU. 'ex1_demand_daily.csv' solo contiene 120 días de datos agregados sin campo SKU.")

if __name__ == "__main__":
    main()

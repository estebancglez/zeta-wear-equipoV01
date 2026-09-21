import csv
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "datos", "ex2_sku_master.csv")
    output_path = os.path.join(base_dir, "resultados", "abc.csv")

    with open(input_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        skus = list(reader)

    # Calcular margen_anual para cada SKU
    for row in skus:
        price = float(row["price"])
        cost = float(row["cost"])
        annual_demand = float(row["annual_demand"])
        row["margen_anual"] = round(annual_demand * (price - cost), 2)

    # Ordenar de mayor a menor margen anual
    skus.sort(key=lambda x: x["margen_anual"], reverse=True)

    # Calcular total_margen
    total_margen = sum(row["margen_anual"] for row in skus)

    # Calcular pct_acumulado y clase_abc
    acumulado = 0.0
    for row in skus:
        acumulado += row["margen_anual"]
        pct_acumulado = round((acumulado / total_margen) * 100, 2)
        row["pct_acumulado"] = pct_acumulado

        if pct_acumulado <= 80.0:
            row["clase_abc"] = "A"
        elif pct_acumulado <= 95.0:
            row["clase_abc"] = "B"
        else:
            row["clase_abc"] = "C"

    # Escribir en resultados/abc.csv
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["sku", "margen_anual", "pct_acumulado", "clase_abc"]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in skus:
            writer.writerow({k: row[k] for k in fieldnames})

if __name__ == "__main__":
    main()

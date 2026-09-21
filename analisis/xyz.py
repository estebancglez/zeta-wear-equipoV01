import csv
import os
import statistics

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "datos", "ex2_monthly_sales.csv")
    output_path = os.path.join(base_dir, "resultados", "xyz.csv")

    with open(input_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    results = []
    for row in rows:
        sku = row["sku"]
        sales = [float(row[k]) for k in row if k != "sku"]

        media_mensual = statistics.mean(sales)
        # Usamos desviación típica muestral (stdev, n-1)
        desv_tipica = statistics.stdev(sales)
        cv = desv_tipica / media_mensual if media_mensual != 0 else 0.0

        if cv <= 0.25:
            clase_xyz = "X"
        elif cv <= 0.50:
            clase_xyz = "Y"
        else:
            clase_xyz = "Z"

        results.append({
            "sku": sku,
            "media_mensual": round(media_mensual, 2),
            "desv_tipica": round(desv_tipica, 2),
            "cv": round(cv, 4),
            "clase_xyz": clase_xyz
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = ["sku", "media_mensual", "desv_tipica", "cv", "clase_xyz"]

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

if __name__ == "__main__":
    main()

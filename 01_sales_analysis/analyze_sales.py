from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "sales.csv"
OUTPUT_DIR = BASE_DIR / "output"


def load_sales(path: Path) -> pd.DataFrame:
    """Load sales data and validate required fields."""
    df = pd.read_csv(path, parse_dates=["order_date"])
    required = {
        "order_id", "order_date", "product", "category",
        "region", "quantity", "unit_price"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"В CSV отсутствуют столбцы: {sorted(missing)}")

    if df[list(required)].isna().any().any():
        raise ValueError("В обязательных полях найдены пустые значения.")
    if (df["quantity"] <= 0).any():
        raise ValueError("Количество должно быть положительным.")
    if (df["unit_price"] < 0).any():
        raise ValueError("Цена не может быть отрицательной.")

    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    return df


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    df = load_sales(DATA_PATH)

    monthly = df.groupby("month", as_index=False)["revenue"].sum()
    categories = (
        df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )
    regions = (
        df.groupby("region", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    total_revenue = float(df["revenue"].sum())
    average_order_revenue = float(df.groupby("order_id")["revenue"].sum().mean())
    top_product = (
        df.groupby("product")["revenue"].sum().sort_values(ascending=False).index[0]
    )
    revenue_values = df["revenue"].to_numpy(dtype=float)
    median_line = np.median(revenue_values)

    monthly.to_csv(OUTPUT_DIR / "monthly_revenue.csv", index=False)
    categories.to_csv(OUTPUT_DIR / "revenue_by_category.csv", index=False)
    regions.to_csv(OUTPUT_DIR / "revenue_by_region.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly["month"], monthly["revenue"], marker="o")
    ax.set_title("Revenue by month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(categories["category"], categories["revenue"])
    ax.set_title("Revenue by category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Revenue")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "revenue_by_category.png", dpi=150)
    plt.close(fig)

    print(f"Количество записей: {len(df)}")
    print(f"Общая выручка: {total_revenue:,.2f}")
    print(f"Средняя выручка на заказ: {average_order_revenue:,.2f}")
    print(f"Медиана выручки по строкам: {median_line:,.2f}")
    print(f"Товар с наибольшей выручкой: {top_product}")
    print("\nВыручка по категориям:")
    print(categories.to_string(index=False))
    print(f"\nРезультаты сохранены в: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

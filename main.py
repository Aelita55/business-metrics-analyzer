import pandas as pd


def calculate_profitability(revenue: float, cost: float) -> float:
    """Возвращает рентабельность в процентах."""
    if revenue == 0:
        return 0.0
    return (revenue - cost) / revenue * 100


def main():
    data = {
        "Месяц": ["Январь", "Февраль", "Март"],
        "Выручка": [120000, 150000, 135000],
        "Затраты": [80000, 90000, 85000],
    }
    df = pd.DataFrame(data)
    print(df)
    print("Средняя выручка:", df["Выручка"].mean())

    # Вызываем функцию расчёта KPI
    total_revenue = df["Выручка"].sum()
    total_cost = df["Затраты"].sum()
    profitability = calculate_profitability(total_revenue, total_cost)
    print(f"Общая рентабельность за период: {profitability:.2f}%")


if __name__ == "__main__":
    main()
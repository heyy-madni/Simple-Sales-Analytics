from metric_exporter import get_metrics


# CORE

def classify(value, thresholds):
    if value < thresholds["low"]:
        return "Low"
    elif value < thresholds["medium"]:
        return "Medium"
    return "High"


def impact_score(value, thresholds):
    target = (
        thresholds["low"] if value < thresholds["low"]
        else thresholds["medium"] if value < thresholds["medium"]
        else thresholds["high"]
    )
    return round(abs(value - target) / target * 100, 2) if target else 0


def build_metric(name, value, thresholds, prefix=""):
    if not isinstance(value, (int, float)):
        raise TypeError(f"Expected numeric value for '{name}', got {type(value).__name__}")
    return {
        "type": name,
        "value": f"{prefix}{value:,}",
        "level": classify(value, thresholds),
        "impact": impact_score(value, thresholds)
    }


# METRIC CONFIG

METRICS = [
    ("Total Revenue", "total revenue", {"low": 1e8, "medium": 5e8, "high": 1e9}, "₹"),
    ("Total Orders", "total orders", {"low": 500, "medium": 2000, "high": 5000}, ""),
    ("Total Units Sold", "total units sold", {"low": 1000, "medium": 5000, "high": 10000}, ""),
    ("Customers Count", "customers count", {"low": 100, "medium": 500, "high": 1000}, ""),
    ("Average Order Value", "average_order_value", {"low": 10000, "medium": 25000, "high": 50000}, "₹"),
    ("Average Sale Price", "average sale price", {"low": 5000, "medium": 15000, "high": 30000}, "₹"),
]


# SPECIAL INSIGHTS

def price_gap_insight(metrics):
    value = metrics.get("price_to_value_gap", 0)

    if value < 0:
        insight = "Bulk buying behavior detected"
        level = "Negative"
    elif value > 0:
        insight = "Premium single-unit purchases"
        level = "Positive"
    else:
        insight = "Mostly single-unit orders"
        level = "Neutral"

    return {
        "type": "Price to Value Gap",
        "value": f"₹{value:,}",
        "level": level,
        "insight": insight
    }


def top_products(metrics):
    total = metrics.get("total revenue", 0)
    products = metrics.get("top_5_products") or []
    result = []

    for name, rev in products:
        share = round((rev / total) * 100, 2) if total else 0
        result.append({
            "product": name,
            "share": f"{share}%",
            "tag": "Dominant" if share > 20 else "Strong" if share > 10 else "Minor"
        })

    return {"type": "Top Products", "data": result}


# PIPELINE

def generate_insights(metrics):
    output = []

    for name, key, thresholds, prefix in METRICS:
        value = metrics.get(key)
        if value is None:
            print(f"Warning: missing key '{key}' in metrics, skipping.")
            continue
        output.append(build_metric(name, value, thresholds, prefix))

    output.append(price_gap_insight(metrics))
    output.append(top_products(metrics))

    return output


if __name__ == "__main__":
    import pprint
    try:
        metrics = get_metrics()
        pprint.pprint(generate_insights(metrics))
    except Exception as e:
        print(f"Failed to generate insights: {e}")



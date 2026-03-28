"""
presentation.py
Prints a formatted metric table with insights and recommendations
in the terminal. Uses intelligent.py for rule-based analysis.

Usage:
    python presentation.py
"""

from metric_exporter import get_metrics
from intelligence_engine import generate_insights
# from intelligent import get_intelligence


# ─── ANSI ────────────────────────────────────────────────────────────────────

R     = "\033[0m"        # reset
BOLD  = "\033[1m"
DIM   = "\033[2m"
ITAL  = "\033[3m"

WHITE  = "\033[97m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
BLUE   = "\033[94m"
GRAY   = "\033[90m"

BG_DARK = "\033[48;5;235m"
BG_ROW  = "\033[48;5;237m"


# ─── HELPERS ─────────────────────────────────────────────────────────────────

def level_color(level: str) -> str:
    if level in ("High", "Positive", "Dominant", "Strong"):
        return GREEN
    elif level in ("Medium", "Neutral", "Stable"):
        return YELLOW
    else:
        return RED


def clip(text: str, width: int) -> str:
    """Truncate with ellipsis if too long."""
    if len(text) > width:
        return text[:width - 1] + "…"
    return text


def col(text: str, width: int, align: str = "left", color: str = "") -> str:
    """Fixed-width colored column cell."""
    text = clip(str(text), width)
    padded = text.ljust(width) if align == "left" else text.rjust(width)
    return f"{color}{padded}{R}"


def rule(char: str = "─", width: int = 116) -> str:
    return f"{DIM}{char * width}{R}"


def header_rule(width: int = 116) -> str:
    return f"{CYAN}{'━' * width}{R}"


# ─── SECTIONS ────────────────────────────────────────────────────────────────

def print_health(health: str) -> None:
    color = GREEN if "STRONG" in health else YELLOW if "STABLE" in health or "AVERAGE" in health else RED
    print()
    print(f"  {BOLD}{color}● OVERALL HEALTH:{R}  {color}{health}{R}")
    print()


def print_table(insights: list[dict], intelligence: dict) -> None:
    llm = {m["type"]: m for m in intelligence["metrics"]}

    # Column widths
    W = {"metric": 22, "value": 14, "level": 8, "impact": 8, "insight": 36, "recommendation": 36}

    # Header
    print(header_rule())
    print(
        f"  "
        f"{col('METRIC',         W['metric'],  color=BOLD+CYAN)}"
        f"  {col('VALUE',        W['value'],   align='right', color=BOLD+CYAN)}"
        f"  {col('LEVEL',        W['level'],   color=BOLD+CYAN)}"
        f"  {col('IMPACT',       W['impact'],  align='right', color=BOLD+CYAN)}"
        f"  {col('INSIGHT',      W['insight'],  color=BOLD+CYAN)}"
        f"  {col('RECOMMENDATION', W['recommendation'], color=BOLD+CYAN)}"
    )
    print(header_rule())

    for i, metric in enumerate(insights):
        name   = metric["type"]
        value  = metric.get("value", "—")
        level  = metric.get("level", "—")
        impact = f"{metric['impact']}%" if "impact" in metric else "—"
        lc     = level_color(level)

        llm_data  = llm.get(name, {})
        insight   = llm_data.get("insight", "—")
        rec       = llm_data.get("recommendation", "—")

        row_bg = BG_ROW if i % 2 == 0 else ""

        print(
            f"  "
            f"{col(name,    W['metric'],              color=BOLD+WHITE)}"
            f"  {col(value, W['value'],  align='right', color=CYAN)}"
            f"  {col(level, W['level'],               color=lc+BOLD)}"
            f"  {col(impact,W['impact'], align='right', color=lc)}"
            f"  {col(insight, W['insight'],            color=WHITE)}"
            f"  {col(rec,   W['recommendation'],       color=GRAY+ITAL)}"
        )
        print(f"  {rule()}")


def print_top_products(insights: list[dict]) -> None:
    top = next((m for m in insights if m["type"] == "Top Products"), None)
    if not top:
        return

    print(f"\n  {BOLD}{CYAN}TOP PRODUCTS{R}")
    print(f"  {rule('─', 60)}")

    for p in top.get("data", []):
        tc    = level_color(p["tag"])
        bar_w = int(float(p["share"].strip("%")) * 1.5)
        bar   = f"{tc}{'█' * bar_w}{R}{GRAY}{'░' * (30 - bar_w)}{R}"
        print(
            f"  {col(p['product'], 22, color=WHITE+BOLD)}"
            f"  {bar}"
            f"  {tc}{p['share']:>5}{R}"
            f"  {DIM}{p['tag']}{R}"
        )

    print()


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{BOLD}{CYAN}  ╔══════════════════════════════════════╗")
    print(f"  ║   METRIC INTELLIGENCE REPORT         ║")
    print(f"  ╚══════════════════════════════════════╝{R}\n")

    print(f"  {DIM}Fetching metrics...{R}")
    metrics     = get_metrics()

    print(f"  {DIM}Generating insights...{R}")
    insights    = generate_insights(metrics)
    intelligence = (insights)

    print_health(intelligence["health"])

    # Filter out Top Products for main table (it has no level/impact)
    table_rows = [m for m in insights if m["type"] != "Top Products"]
    print_table(table_rows, intelligence)

    print_top_products(insights)


if __name__ == "__main__":
    main()
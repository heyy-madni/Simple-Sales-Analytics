# presentation.py

from utils.common_utils import click_pause,clear_console # type: ignore

from data_compute.metric_exporter import get_metrics # type: ignore
from data_compute.intelligence_engine import generate_insights # type: ignore

R     = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
ITAL  = "\033[3m"

WHITE  = "\033[97m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
GRAY   = "\033[90m"

BG_ROW = "\033[48;5;237m"


def level_color(level: str) -> str:
    if level in ("High", "Positive", "Dominant", "Strong"):
        return GREEN
    elif level in ("Medium", "Neutral", "Stable"):
        return YELLOW
    else:
        return RED


def clip(text: str, width: int) -> str:
    if len(text) > width:
        return text[:width - 1] + "…"
    return text


def col(text: str, width: int, align: str = "left", color: str = "") -> str:
    text = clip(str(text), width)
    padded = text.ljust(width) if align == "left" else text.rjust(width)
    return f"{color}{padded}{R}"


def rule(char: str = "─", width: int = 86) -> str:
    return f"{DIM}{char * width}{R}"


def header_rule(width: int = 86) -> str:
    return f"{CYAN}{'━' * width}{R}"



def derive_health(insights: list[dict]) -> tuple[str, str]:
    """Derive overall health label and color from insight levels."""
    scored = [m for m in insights if "level" in m and m["type"] != "Top Products"]
    high_count = sum(1 for m in scored if m["level"] in ("High", "Positive"))
    ratio = high_count / len(scored) if scored else 0

    if ratio >= 0.6:
        return "STRONG", GREEN
    elif ratio >= 0.3:
        return "STABLE", YELLOW
    else:
        return "NEEDS ATTENTION", RED



def print_health(insights: list[dict]) -> None:
    label, color = derive_health(insights)
    print()
    print(f"  {BOLD}{color}● OVERALL HEALTH:  {label}{R}")
    print()


def print_table(insights: list[dict]) -> None:
    W = {"metric": 22, "value": 14, "level": 10, "impact": 8}

    print(header_rule())
    print(
        f"  "
        f"{col('METRIC',  W['metric'],             color=BOLD+CYAN)}"
        f"  {col('VALUE', W['value'], align='right', color=BOLD+CYAN)}"
        f"  {col('LEVEL', W['level'],               color=BOLD+CYAN)}"
        f"  {col('IMPACT',W['impact'], align='right', color=BOLD+CYAN)}"
    )
    print(header_rule())

    for metric in insights:
        name   = metric["type"]
        value  = metric.get("value", "—")
        level  = metric.get("level", "—")
        impact = f"{metric['impact']}%" if metric.get("impact") is not None else "✓"
        lc     = level_color(level)

        print(
            f"  "
            f"{col(name,    W['metric'],               color=BOLD+WHITE)}"
            f"  {col(value, W['value'],  align='right', color=CYAN)}"
            f"  {col(level, W['level'],                color=lc+BOLD)}"
            f"  {col(impact,W['impact'], align='right', color=lc)}"
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



def show_report() -> None:
    clear_console()
    """Entry point for menu_manager to call."""
    print(f"\n{BOLD}{CYAN}  ╔══════════════════════════════════════╗")
    print(f"  ║   METRIC INTELLIGENCE REPORT         ║")
    print(f"  ╚══════════════════════════════════════╝{R}\n")

    print(f"  {DIM}Fetching metrics...{R}")
    metrics  = get_metrics()

    print(f"  {DIM}Generating insights...{R}")
    insights = generate_insights(metrics)

    print_health(insights)

    table_rows = [m for m in insights if m["type"] != "Top Products"]
    print_table(table_rows)

    print_top_products(insights)
    click_pause()


if __name__ == "__main__":
    show_report()
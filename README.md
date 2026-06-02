# Simple Sales Analytics

A terminal-based business analytics system built with Python and SQLite. Load your sales data into the database and get an instant breakdown of revenue, product performance, and business health — with a colored intelligence report, all without any external APIs or dashboards.

---

## What It Does

Connect it to your SQLite database and navigate through three views:

- **Executive Snapshot** — top-line numbers at a glance: revenue, orders, customers, average order value
- **Product Performance** — revenue by category, units sold by category, top 5 products by revenue
- **Insights & Recommendations** — a full intelligence report with metric classification (High / Medium / Low), impact scores showing how far each metric is from the next threshold, buying behavior detection, top product revenue share breakdown, and an overall business health label

---

## Project Structure

```
Simple-Sales-Analytics/
├── database/
│   └── database.db          # SQLite database (auto-created on first run)
├── src/
│   ├── main.py              # Entry point
│   ├── data_compute/
│   │   ├── database_manager.py    # SQLite connection, table creation
│   │   ├── metric_exporter.py     # All SQL queries, metric aggregation
│   │   └── intelligence_engine.py # Classification, scoring, insight generation
│   ├── presentation_manager/
│   │   ├── menu_manager.py        # Main menu and submenus
│   │   └── presentation.py        # Colored terminal report renderer
│   └── utils/
│       └── common_utils.py        # Console utilities (clear, pause)
└── README.md
```

---

## Getting Started

### Requirements

- Python 3.10+
- No external packages required — uses only the standard library

### Run

```bash
cd src
python main.py
```

The database file is auto-created at `database/database.db` on first run. Populate it with your data before running analysis (see Database Schema below).

---

## Database Schema

Three tables are expected:

**customers**
| Column | Type | Notes |
|--------|------|-------|
| customer_id | INTEGER | Primary key, auto-increment |
| name | TEXT | Customer name |
| city | TEXT | Customer city |

**products**
| Column | Type | Notes |
|--------|------|-------|
| product_id | INTEGER | Primary key, auto-increment |
| name | TEXT | Product name |
| category | TEXT | Product category |
| price | REAL | Unit price |

**orders**
| Column | Type | Notes |
|--------|------|-------|
| order_id | INTEGER | Primary key, auto-increment |
| customer_id | INTEGER | Foreign key → customers |
| product_id | INTEGER | Foreign key → products |
| quantity | INTEGER | Units ordered |
| order_date | TEXT | Date string (YYYY-MM-DD recommended) |

You can insert data using DB Browser for SQLite, a seed script, or any SQLite client.

---

## Menu Structure

```
BUSINESS ANALYTICS SYSTEM
├── 1. Executive Snapshot
├── 2. Product Performance
│   ├── 1. Revenue by Category
│   ├── 2. Units Sold by Category
│   └── 3. Top 5 Products by Revenue
├── 3. Insights & Recommendations
└── 4. Exit
```

---

## How the Intelligence Report Works

The Insights & Recommendations view runs every metric through a classification and scoring system:

**Metrics analyzed:**

| Metric | Low | Medium | High |
|--------|-----|--------|------|
| Total Revenue | < ₹1 Cr | < ₹5 Cr | ₹10 Cr+ |
| Total Orders | < 500 | < 2,000 | 5,000+ |
| Total Units Sold | < 1,000 | < 5,000 | 10,000+ |
| Customer Count | < 100 | < 500 | 1,000+ |
| Average Order Value | < ₹10,000 | < ₹25,000 | ₹50,000+ |
| Average Sale Price | < ₹5,000 | < ₹15,000 | ₹30,000+ |

**Impact score** — shown as a percentage gap between the current value and the next threshold. A metric already at High shows ✓.

**Price-to-Value Gap** — difference between average sale price and average order value. A negative gap means bulk buying behaviour; positive means premium single-unit purchases.

**Top Products** — each product's share of total revenue is tagged as Dominant (>20%), Strong (>10%), or Minor.

**Overall Health** — derived from the ratio of High/Positive metrics to total metrics:
- 60%+ High → **STRONG**
- 30–60% → **STABLE**
- Below 30% → **NEEDS ATTENTION**

---

## Author

**Madni Abid Khan**
Email: madnikhan.work@gmail.com
WhatsApp: +91 90997 16001
GitHub: [github.com/heyy-madni](https://github.com/heyy-madni)
from metric_exporter import executive_snapshot #type: ignore
from common_utils import clear_console, click_pause #type: ignore


def executive_snapshot():
    clear_console()
    print("\n===== EXECUTIVE SNAPSHOT =====")
    snapshot = executive_snapshot()
    print(f"Total Revenue: {snapshot['Total Revenue']}")
    print(f"Total Orders: {snapshot['Total Orders']}")
    print(f"Unique Customers: {snapshot['Unique Customers']}")
    print(f"Average Order Value: {snapshot['Average Order Value']}")
    print(f"Average Units / Order: {snapshot['Average Units / Order']}")
    print(f"Revenue per Unit: {snapshot['Revenue per Unit']}")

    click_pause()

def submenu_product_performance():
    clear_console()
    print("\n===== PRODUCT PERFORMANCE =====")
    print("2.1 Revenue by Category")
    print("2.2 Units Sold by Category")
    print("2.3 Top 5 Products by Revenue")
    print("2.4 Bottom 5 Products by Revenue")
    print("2.5 Product Revenue Concentration")
    print("2.6 Back")
    choice = input("Select option: ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        return

def submenu_customer_intelligence():

    clear_console()
    print("\n===== CUSTOMER INTELLIGENCE =====")
    print("3.1 Top 10 Customers by Revenue")
    print("3.2 Top 10 Customers by Units Purchased")
    print("3.3 Customer Distribution by City")
    print("3.4 Repeat vs One-Time Customers")
    print("3.5 Average Revenue per Customer")
    print("3.6 Back")
    choice = input("Select option: ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        return

def submenu_time_trend_analysis():
    clear_console()
    print("\n===== TIME & TREND ANALYSIS =====")
    print("4.1 Monthly Revenue Trend")
    print("4.2 Monthly Order Volume")
    print("4.3 Growth Rate Month-over-Month")
    print("4.4 Best Performing Month")
    print("4.5 Worst Performing Month")
    print("4.6 Back")
    choice = input("Select option: ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        pass
    elif choice == "6":
        return

def submenu_risk_distribution_analysis():
    clear_console()
    print("\n===== RISK & DISTRIBUTION ANALYSIS =====")
    print("5.1 Revenue Concentration (Top 5 Customers Share %)")
    print("5.2 Revenue Concentration (Top 3 Products Share %) ")
    print("5.3 Customer Revenue Spread (Low / Mid / High) ")
    print("5.4 Order Size Distribution ")
    print("5.5 Dependency Risk Simulation")
    print("5.6 Back")
    choice = input("Select option: ")
    if choice == "1":
        pass
    elif choice == "2":
        pass
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        return

def main_menu():

    while True:
        clear_console()
        print("\n===== BUSINESS ANALYTICS SYSTEM =====")
        print("1. Executive Snapshot")
        print("2. Product Performance")
        print("3. Customer Intelligence")
        print("4. Time & Trend Analysis")
        print("5. Risk & Distribution Analysis")
        print("6. Exit")
        choice = input("Select option: ")

        if choice == "1":
            executive_snapshot()

        elif choice == "2":
            submenu_product_performance()
        
        elif choice == "3":
            submenu_customer_intelligence()

        elif choice == "4":
            submenu_time_trend_analysis()

        elif choice == "5":
            submenu_risk_distribution_analysis()

        elif choice == "6":
            break
        else:
            print("Invalid option")
from metric_exporter import executive_snapshot as get_snapshot ,get_metrics
from common_utils import clear_console, click_pause 



# opt 1 EXECUTIVE SNAPSHOT

def show_executive_snapshot():
    clear_console()
    print("\n===== EXECUTIVE SNAPSHOT =====")

    snapshot = get_snapshot()

    print(f"Total Revenue: {snapshot['Total Revenue']}")
    print(f"Total Orders: {snapshot['Total Orders']}")
    print(f"Unique Customers: {snapshot['Unique Customers']}")
    print(f"Average Order Value: {snapshot['Average Order Value']}")
    print(f"Average Units / Order: {snapshot['Average Units / Order']}")
    print(f"Revenue per Unit: {snapshot['Revenue per Unit']}")

    click_pause()



# opt 2 PRODUCT PERFORMANCE

def submenu_product_performance():
    while True:
        clear_console()
        print("\n===== PRODUCT PERFORMANCE =====")
        print("1. Revenue by category")
        print("2. Units Sold by Category")
        print("3. Top 5 Products by Revenue")
        print("4. Back")

        choice = input("Select option: ").strip()

        if choice == "1":

            clear_console()
            for product, revenue in get_metrics()["revenue by category"]:
                 print(f"{product}: ₹{revenue:,.2f}")
            click_pause()

        elif choice == "2":
            clear_console()
            for product, units in get_metrics()["unit_sold_by_category"]:
                 print(f"{product}: ₹{units:,}")
                 click_pause()

        elif choice == "3":
            clear_console()
            for product, revenue in get_metrics()["top_5_products_by_revenue"]:
                 print(f"{product}: ₹{revenue:,.2f}")
                 click_pause()

        elif choice == "4":
            break
        else:
            print("Invalid option")
            click_pause()










# MAIN MENU

def main_menu():

    while True:
        clear_console()
        print("\n===== BUSINESS ANALYTICS SYSTEM =====")
        print("1. Executive Snapshot")
        print("2. Product Performance")
        print("3. Insights & Recommendations")
        print("4. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            show_executive_snapshot()
        elif choice == "2":
            submenu_product_performance()


        elif choice == "3":
            #submenu_insights_recommendations()
            pass
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid option")
            click_pause()









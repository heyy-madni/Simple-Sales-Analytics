from metric_exporter import executive_snapshot #type: ignore
from common_utils import clear_console #type: ignore


def executive_snapshot_print():

    snapshot = executive_snapshot()
    print(f"Total Revenue: {snapshot['Total Revenue']}")
    print(f"Total Orders: {snapshot['Total Orders']}")
    print(f"Unique Customers: {snapshot['Unique Customers']}")
    print(f"Average Order Value: {snapshot['Average Order Value']}")
    print(f"Average Units / Order: {snapshot['Average Units / Order']}")
    print(f"Revenue per Unit: {snapshot['Revenue per Unit']}")

def submenu_product_performance():
    clear_console()
    print("\n===== PRODUCT PERFORMANCE =====")
    print("1. Revenue by Category")
    print("2. Units Sold by Category")
    print("3. Top 5 Products by Revenue")
    print("4. Bottom 5 Products by Revenue")
    print("5. Product Revenue Concentration")
    print("6. Back")
    choice = input("Select option: ")
 

def main_menu():
    clear_console()
    while True:
        print("\n===== BUSINESS ANALYTICS SYSTEM =====")
        print("1. Executive Snapshot")
        print("2. Product Performance")
        print("3. Customer Intelligence")
        print("4. Time & Trend Analysis")
        print("5. Risk & Distribution Analysis")
        print("6. Exit")
        choice = input("Select option: ")

        if choice == "1":
            executive_snapshot_print()

        elif choice == "2":
            submenu_product_performance()
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
                break
                
        
        elif choice == "3":
            pass
        elif choice == "4":
            pass
        elif choice == "5":
            pass
        elif choice == "6":
            break
        else:
            print("Invalid option")

from metric_exporter import executive_snapshot 

def main():
    Welcome_message = """
    Welcome to the Simple Sales Analytics App!

    This application allows you to analyze sales data and gain insights into customer behavior, product performance, and overall sales trends.

    You can use this app to:
    - View sales reports and analytics
    - Analyze customer purchasing patterns
    - Track product performance and inventory levels
    - Generate visualizations to better understand your sales data

    Let's get started!"""


def main_menu():
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
            snapshot = executive_snapshot()
            print(f"Total Revenue: {snapshot['Total Revenue']}")
            print(f"Total Orders: {snapshot['Total Orders']}")
            print(f"Unique Customers: {snapshot['Unique Customers']}")
            print(f"Average Order Value: {snapshot['Average Order Value']}")
            print(f"Average Units / Order: {snapshot['Average Units / Order']}")
            print(f"Revenue per Unit: {snapshot['Revenue per Unit']}")

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
        else:
            print("Invalid option")

        choice = input("Select option: ")

        if choice == "1":

            pass
        elif choice == "2":
           pass# inventory_menu()
        elif choice == "3":
            pass#customer_menu()
        elif choice == "4":
            pass#report_menu()
        elif choice == "5":
            break
        else:
            print("Invalid option")



    


main()









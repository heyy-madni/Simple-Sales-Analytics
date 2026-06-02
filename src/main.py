#imports
from presentation_manager.menu_manager import  main_menu  


def main():
    try:
        main_menu()
    except Exception as e :
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()





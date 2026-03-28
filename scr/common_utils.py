#import 

import os




#wlcome message



#  CLEAR CONSOLE FUNCTION 
def clear_console():
    """Clears the console screen."""
    
    os.system('cls' if os.name == 'nt' else 'clear')

# click pause function
def click_pause():

    input("\nPress Enter to continue...")


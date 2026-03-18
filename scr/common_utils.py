#import 

import os



#wlcome message
Welcome_message = """

    Welcome to the Simple Sales Analytics App!

    This application allows you to analyze sales data and gain insights into customer behavior, product performance, and overall sales trends.

    You can use this app to:
    - View sales reports and analytics
    - Analyze customer purchasing patterns
    - Track product performance and inventory levels
    - Generate visualizations to better understand your sales data

    Let's get started!"""


#! ---------- CLEAR CONSOLE FUNCTION ----------
def clear_console():
    """Clears the console screen."""
    
    os.system('cls' if os.name == 'nt' else 'clear')


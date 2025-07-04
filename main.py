
from models.product_model import add_product, view_all_products, update_product, delete_product
from models.order_model import add_to_cart, get_cart_items, place_order, view_orders
from tkinter import Tk
from gui.app_window import GroceryAppGUI

if __name__ == "__main__":
    root = Tk()
    app = GroceryAppGUI(root)
    root.mainloop()







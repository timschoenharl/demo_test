import time
import random
import tkinter as tk
from tkinter import ttk

#Backpack management game
#Provided by Claude

class Item:
    def __init__(self, weight, type, uses):
        self.weight = weight
        self.type = type
        self.uses = uses
        
    def get_usage_message(self, uses_left):
        if self.uses == float('inf'):
            return "It has unlimited uses!"
        elif uses_left == 0:
            return "It's now gone!"
        else:
            return f"{uses_left} uses remaining!"

    def __eq__(self, other):
        return self.weight == other.weight and self.type == other.type and self.uses == other.uses


# Create Item objects and store them in the ITEMS dictionary
ITEMS = {
    'sandwich': Item(1, 'food', 2),
    'water bottle': Item(2, 'drink', 3),
    'flashlight': Item(2, 'tool', 5),
    'map': Item(1, 'tool', float('inf')),
    'compass': Item(1, 'tool', float('inf')),
    'first aid kit': Item(3, 'medical', 3),
    'rope': Item(4, 'tool', float('inf')),
    'matches': Item(1, 'tool', 5),
    'bag of poop': Item(2, 'food', 3),
    'rations': Item(1, 'food', 5)
}

class Backpack:
    def __init__(self, max_weight=10):
        self.items = {}  # Dictionary to store items and their remaining uses
        self.max_weight = max_weight

    def current_weight(self):
        return sum(self.items[key].weight for key in self.items)

    def add_item(self, item_name):
        if item_name not in ITEMS:
            return False, "That item doesn't exist!"

        item = ITEMS[item_name]
        new_weight = self.current_weight() + item.weight
        if new_weight > self.max_weight:
            return False, "Too heavy! Cannot add this item."
        if item_name in self.items:
            return False, "You already have this item!"
        self.items[item_name] = Item(item.weight, item.type, item.uses) #add a copy of the item
        return True, f"Added {item_name} to your backpack!"
    
    def use_item(self, item_name):
        if item_name not in self.items:
            return False, "You don't have this item!"
        item = self.items[item_name]
        if item.uses == 0:
            return False, f"Your {item_name} has no uses left!"
        if item.uses != float('inf'):
            item.uses -= 1
            if item.uses == 0:
                del self.items[item_name]
                return True, f"Used {item_name}. {item.get_usage_message(item.uses)}"
            return True, f"Used {item_name}. {item.get_usage_message(item.uses)}"
        return True, f"Used {item_name}. {item.get_usage_message(item.uses)}"
        
    def list_items(self):
        if not self.items:
            return "Your backpack is empty!"
        result = "\nYour Backpack Contents:"
        for item_name in self.items:
            item = self.items[item_name]
            uses = "∞" if item.uses == float('inf') else item.uses
            result += f"\n- {item_name} (Uses left: {uses})"
        result += f"\nTotal Weight: {self.current_weight()}/{self.max_weight}"
        return result

def display_backpack(backpack):
    # Clear existing labels
    for widget in backpack_frame.winfo_children():
        widget.destroy()
    backpack_label = tk.Label(backpack_frame, text="Backpack Contents:", font=("Arial", 12))
    backpack_label.pack()
    
    # Display items in the backpack
    for item in backpack.items:
        item_label = tk.Label(backpack_frame, text=f"- {item} (Uses left: {backpack.items[item].uses})", font=("Arial", 10))
        item_label.pack()
    # Display weight
    weight_label = tk.Label(backpack_frame, text=f"Total Weight: {backpack.current_weight()}/{backpack.max_weight}")
    weight_label.pack()
    
def display_available_items():
    # Clear existing labels
    for widget in items_frame.winfo_children():
        widget.destroy()
    items_label = tk.Label(items_frame, text="Available Items:", font=("Arial", 12))
    items_label.pack()
    # Display available items
    for item, properties in ITEMS.items():
        item_label = tk.Label(items_frame, text=f"- {item} (Weight: {properties.weight})")
        item_label.pack()

        
def add_item(backpack):
    item = item_entry.get().lower()
    success, message = backpack.add_item(item)
    status_label.config(text=message)
    item_entry.delete(0, tk.END)
    display_backpack(backpack)
    display_available_items()
    
def use_item(backpack):
    item = item_usage.get().lower()
    success, message = backpack.use_item(item)
    status_label.config(text=message)
    #status_label.config(text=item)
    item_usage.delete(0, tk.END)
    display_backpack(backpack)

def main():
    global backpack, window, item_entry, item_usage, status_label, backpack_frame, items_frame
    backpack = Backpack()
    window = tk.Tk()
    window.title("Adventure Backpack")

    # Status Label
    status_label = tk.Label(window, text="", font=("Arial", 10))
    status_label.pack()
   
    # Add Item Section
    add_item_frame = tk.Frame(window)
    add_item_frame.pack(pady=10)
    add_item_label = tk.Label(add_item_frame, text="Add Item:", font=("Arial", 12))
    add_item_label.pack()
    item_entry = tk.Entry(add_item_frame, width=20)
    item_entry.pack()
    
    add_item_button = tk.Button(add_item_frame, text="Add", command=lambda: add_item(backpack))
    add_item_button.pack()
    
        # Use Item Section
    use_item_frame = tk.Frame(window)
    use_item_frame.pack(pady=10)
    use_item_label = tk.Label(use_item_frame, text="Use Item:", font=("Arial", 12))
    use_item_label.pack()
    item_usage = tk.Entry(use_item_frame, width=20)
    item_usage.pack()
    use_item_button = tk.Button(use_item_frame, text="Use", command=lambda: use_item(backpack))
    use_item_button.pack()

    # Display Backpack Section
    backpack_frame = tk.Frame(window)
    backpack_frame.pack(pady=10)
    display_backpack(backpack)
    
    # Display Available Items Section
    items_frame = tk.Frame(window)
    items_frame.pack(pady=10)
    display_available_items()

    
    window.mainloop()

if __name__ == "__main__":
    main()
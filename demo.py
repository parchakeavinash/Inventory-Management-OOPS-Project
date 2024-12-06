import streamlit as st
import uuid
import csv
import pandas as pd


# Inventory Items class
class InventoryItems:
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sku = str(uuid.uuid4())


# Inventory Manager class
class InventoryManager:
    def __init__(self, file):
        self.file = file
        self.inventory = []
        self.next_item_id = 0
        self.load_inventory()

    def load_inventory(self):
        try:
            with open(self.file, "r") as file:
                reader = csv.DictReader(file)
                self.inventory = [
                    InventoryItems(
                        int(row["itemsID"]),
                        row["Name"],
                        int(row["Quantity"]),
                        float(row["Price"]),
                    )
                    for row in reader
                ]
                self.next_item_id = len(self.inventory)
        except FileNotFoundError:
            st.warning("Inventory file not found. Starting with an empty inventory.")

    def save_inventory(self):
        with open(self.file, "w", newline="") as file:
            fieldnames = ["itemsID", "Name", "Quantity", "Price", "sku"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.inventory:
                writer.writerow(
                    {
                        "itemsID": item.item_id,
                        "Name": item.name,
                        "Quantity": item.quantity,
                        "Price": item.price,
                        "sku": item.sku,
                    }
                )

    def add_item(self, name, quantity, price):
        item = InventoryItems(self.next_item_id, name, quantity, price)
        self.inventory.append(item)
        self.next_item_id += 1
        st.success(f"Item '{name}' added successfully!")


    def delete_items_by_id(self, item_id):
        self.inventory = [item for item in self.inventory if item.item_id != item_id]
        st.success(f"Item with ID {item_id} deleted successfully!")

    def filter_items(self, max_price):
        return [item for item in self.inventory if item.price <= max_price]


# Streamlit UI
def main():
    st.title("Inventory Management System")
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio(
        "Select an option:",
        ["Add Item", "View Inventory", "Filter by Price", "Delete Item", "Save Inventory"],
    )

    # Load inventory manager
    manager = InventoryManager("inventory.csv")

    # Add Item
    if choice == "Add Item":
        st.header("Add a New Item")
        name = st.text_input("Item Name")
        quantity = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.01)

        if st.button("Add Item"):
            manager.add_item(name, quantity, price)
            manager.save_inventory()


    # View Inventory
    elif choice == "View Inventory":
        st.header("Inventory List")
        if manager.inventory:
            data = {
                "Item ID": [item.item_id for item in manager.inventory],
                "Name": [item.name for item in manager.inventory],
                "Quantity": [item.quantity for item in manager.inventory],
                "Price": [item.price for item in manager.inventory],
                "SKU": [item.sku for item in manager.inventory],
            }
            st.table(pd.DataFrame(data))
        else:
            st.warning("The inventory is currently empty.")

    # Filter by Price
    elif choice == "Filter by Price":
        st.header("Filter Items by Price")
        max_price = st.slider("Select Maximum Price", 0.0, 100000.0, 5000.0, step=100.0)
        filtered_items = manager.filter_items(max_price)

        if filtered_items:
            data = {
                "Item ID": [item.item_id for item in filtered_items],
                "Name": [item.name for item in filtered_items],
                "Quantity": [item.quantity for item in filtered_items],
                "Price": [item.price for item in filtered_items],
                "SKU": [item.sku for item in filtered_items],
            }
            st.table(pd.DataFrame(data))
        else:
            st.warning("No items found below the specified price.")

    # Delete Item
    elif choice == "Delete Item":
        st.header("Delete an Item")
        if manager.inventory:
            item_ids = [item.item_id for item in manager.inventory]
            selected_id = st.selectbox("Select Item ID to Delete", item_ids)

            if st.button("Delete Item"):
                manager.delete_items_by_id(selected_id)
                manager.save_inventory()
        else:
            st.warning("The inventory is empty. No items to delete.")

    # Save Inventory
    elif choice == "Save Inventory":
        if st.button("Save Inventory"):
            manager.save_inventory()
            st.success("Inventory saved successfully!")


if __name__ == "__main__":
    main()
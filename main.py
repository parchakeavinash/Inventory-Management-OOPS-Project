# create inventory class
import uuid
import csv


class InventoryItems:
    def __init__(self, item_id, name, quantity, price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sku = str(uuid.uuid4())  # basic version to generate numbers

    def display_info(self):
        print(f"item ID: {self.item_id}, Name: {self.name}, Quantity: {self.quantity}, price: {self.price:.2f}")


class InventoryManager:
    def __init__(self, file):
        self.file = file
        self.inventory = []  # create an inventory in list format
        self.next_item_id = 0

    def load_inventory(self):
        try:
            with open('self.file', "r") as file:
                reader = csv.DictReader(file)
                self.inventory = [InventoryItems(
                    int(row["itemsID"]),
                    row["Name"],
                    int(row["Quantity"]),
                    float(row["Price"]),
                )
                    for row in reader]
                self.next_item_id = len(self.inventory) + 1
        except FileNotFoundError:
            print("No File....")

    def save_inventory(self):
        with open("self.file", "w", newline="") as file:
            fieldnames = ["itemsID", "Name", "Quantity", "Price", "sku"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.inventory:
                writer.writerow({
                    "itemsID": item.item_id,
                    "Name": item.name,
                    "Quantity": item.quantity,
                    "Price": item.price,
                    "sku": item.sku
                })

    def add_item(self, name, quantity, price):
        item = InventoryItems(self.next_item_id, name, quantity, price)
        self.inventory.append(item)
        self.next_item_id += 1
        # save to csv file
        self.save_inventory()

    def display_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
        else:
            for item in self.inventory:
                item.display_info()

    def delete_items_by_id(self, item_id):
        self.inventory = [item for item in self.inventory if item.item_id != item_id]
        self.save_inventory()

    def filter_items(self, max_price):
        if not self.inventory:
            print("Inventory is empty.")
            return []

        return [item for item in self.inventory if item.price <= max_price]


def main():

    store = InventoryManager("inventory.csv")
    store.load_inventory()
    while True:
        print("\n====== E-Commerce System =====")
        print("1. Add an Item")
        print("2. Display Inventory")
        print("3. Filter items by price")
        print("4. Delete an items by ID")
        print("5. Save Inventory")
        print("6. Exit")

        option = input("Enter your choice (1-6): ")

        if option == "1":
            name = input("Enter name: ")
            quantity = int(input("Enter amount of items : "))
            price = float(input("Enter a price: "))
            # add items
            store.add_item(name, quantity, price)

        elif option == "2":
            store.display_inventory()

        elif option == "3":
            search = float(input("Enter a max price: "))
            filter_items = store.filter_items(search)
            print(f"Items less than {search}:")
            for item in filter_items:
                item.display_info()

        elif option == "4":
            id_num = int(input("Enter the Id of the items to delete: "))
            store.delete_items_by_id(id_num)

        elif option == "5":
            store.save_inventory()
            print("save to csv.")

        elif option == "6":
            print("Goodbye...")
            break

        else:
            print("invalid option. please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()

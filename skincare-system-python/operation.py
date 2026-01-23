import datetime
from write import writemessage, update_products_file, generate_sales_invoice, generate_restock_invoice

def displayproduct(item):
    print("\n\t\t\t\t--- WeCare Beauty Products --- \n")
    print("------------------------------------------------------------------------------------------------------------")
    print("Product Name\t | Brand\t | Quantity\t | Cost Price\t | Selling Price\t | Country\t |")
    print("------------------------------------------------------------------------------------------------------------")
    for p in item:
        sp = p["cost"] * 2  # 200% markup
        print(f"{p['name']}\t | {p['brand']}\t | {p['quantity']}\t\t | Rs.{p['cost']:.2f}\t | Rs.{sp:.2f}\t\t | {p['country']}\t |")
        print("------------------------------------------------------------------------------------------------------------")

def process_sale(items):
    """Process a customer sale with the 'buy three get one free' policy"""
    # Display available products for the user to choose
    print("\n\t\t\t\t--- Available Products --- \n")
    print("------------------------------------------------------------------------------------------------------------")
    print("ID | Product Name\t | Brand\t | Quantity\t | Selling Price\t | Country\t |")
    print("------------------------------------------------------------------------------------------------------------")
    
    # Display products with IDs for selection
    for i, p in enumerate(items):
        selling_price = p["cost"] * 2  # 200% markup
        print(f"{i+1} | {p['name']}\t | {p['brand']}\t | {p['quantity']}\t\t | Rs.{selling_price:.2f}\t\t | {p['country']}\t |")
        print("------------------------------------------------------------------------------------------------------------")
    
    # Get customer name
    customer_name = input("\nEnter customer name: ")
    
    cart = []
    quantities = []
    total_amount = 0
    
    # Let the user add products to cart
    while True:
        try:
            choice = input("\nEnter product ID to add to cart (0 to finish): ")
            if choice == '0':
                break
            
            product_id = int(choice) - 1
            if product_id < 0 or product_id >= len(items):
                print("Invalid product ID. Please try again.")
                continue
            
            # Check if product is in stock
            if items[product_id]["quantity"] <= 0:
                print(f"Sorry, {items[product_id]['name']} is out of stock.")
                continue
            
            quantity = int(input(f"Enter quantity for {items[product_id]['name']}: "))
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue
            
            if quantity > items[product_id]["quantity"]:
                print(f"Sorry, only {items[product_id]['quantity']} units of {items[product_id]['name']} are available.")
                continue
            
            # Calculate free items based on "buy three get one free" policy
            free_items = quantity // 3
            paid_items = quantity - free_items
            
            # Calculate amount for this product
            selling_price = items[product_id]["cost"] * 2  # 200% markup
            subtotal = paid_items * selling_price
            
            print(f"\nAdded {quantity} units of {items[product_id]['name']} to cart.")
            print(f"Regular: {paid_items} units + Free: {free_items} units")
            print(f"Subtotal: Rs.{subtotal:.2f}")
            
            # Add to cart
            cart.append(product_id)
            quantities.append(quantity)
            total_amount += subtotal
            
        except ValueError:
            print("Please enter a valid number.")
    
    # If cart is empty, cancel the sale
    if not cart:
        print("\nNo products selected. Sale cancelled.")
        return items
    
    # Display cart summary
    print("\n\t\t\t\t--- Cart Summary --- \n")
    print("------------------------------------------------------------------------------------------------------------")
    print("Product Name\t | Quantity\t | Free Items\t | Price\t\t | Subtotal\t |")
    print("------------------------------------------------------------------------------------------------------------")
    
    for i, product_id in enumerate(cart):
        quantity = quantities[i]
        free_items = quantity // 3
        paid_items = quantity - free_items
        selling_price = items[product_id]["cost"] * 2
        subtotal = paid_items * selling_price
        
        print(f"{items[product_id]['name']}\t | {quantity}\t\t | {free_items}\t\t | Rs.{selling_price:.2f}\t | Rs.{subtotal:.2f}\t |")
    
    print("------------------------------------------------------------------------------------------------------------")
    print(f"Total Amount: Rs.{total_amount:.2f}")
    
    # Confirm sale
    confirm = input("\nConfirm sale? (y/n): ")
    if confirm.lower() != 'y':
        print("\nSale cancelled.")
        return items
    
    # Update quantities
    updated_items = items.copy()
    for i, product_id in enumerate(cart):
        updated_items[product_id]["quantity"] -= quantities[i]
    
    # Update products.txt
    update_products_file(updated_items)
    
    # Generate invoice
    generate_sales_invoice(customer_name, updated_items, cart, quantities, total_amount)
    
    print("\nSale completed successfully!")
    return updated_items

def restock_products(items):
    """Restock products from suppliers"""
    # Display current inventory
    print("\n\t\t\t\t--- Current Inventory --- \n")
    print("------------------------------------------------------------------------------------------------------------")
    print("ID | Product Name\t | Brand\t | Quantity\t | Cost Price\t | Country\t |")
    print("------------------------------------------------------------------------------------------------------------")
    
    # Display products with IDs for selection
    for i, p in enumerate(items):
        print(f"{i+1} | {p['name']}\t | {p['brand']}\t | {p['quantity']}\t\t | Rs.{p['cost']:.2f}\t\t | {p['country']}\t |")
        print("------------------------------------------------------------------------------------------------------------")
    
    # Get supplier name
    supplier_name = input("\nEnter supplier name: ")
    
    restock_cart = []
    restock_quantities = []
    new_costs = []
    total_cost = 0
    
    # Let the user add products to restock
    while True:
        try:
            choice = input("\nEnter product ID to restock (0 to finish): ")
            if choice == '0':
                break
            
            product_id = int(choice) - 1
            if product_id < 0 or product_id >= len(items):
                print("Invalid product ID. Please try again.")
                continue
            
            quantity = int(input(f"Enter quantity to restock for {items[product_id]['name']}: "))
            if quantity <= 0:
                print("Quantity must be greater than 0.")
                continue
            
            # Ask if cost price has changed
            cost_update = input(f"Current cost price is Rs.{items[product_id]['cost']:.2f}. Has the cost changed? (y/n): ")
            
            if cost_update.lower() == 'y':
                try:
                    new_cost = float(input("Enter new cost price: "))
                    if new_cost <= 0:
                        print("Cost must be greater than 0. Using current cost.")
                        new_cost = items[product_id]["cost"]
                except ValueError:
                    print("Invalid cost. Using current cost.")
                    new_cost = items[product_id]["cost"]
            else:
                new_cost = items[product_id]["cost"]
            
            # Calculate amount for this product
            subtotal = quantity * new_cost
            
            print(f"\nAdding {quantity} units of {items[product_id]['name']} to restock.")
            print(f"Cost: Rs.{new_cost:.2f} per unit")
            print(f"Subtotal: Rs.{subtotal:.2f}")
            
            # Add to restock cart
            restock_cart.append(product_id)
            restock_quantities.append(quantity)
            new_costs.append(new_cost)
            total_cost += subtotal
            
        except ValueError:
            print("Please enter a valid number.")
    
    # If restock cart is empty, cancel the restock
    if not restock_cart:
        print("\nNo products selected. Restock cancelled.")
        return items
    
    # Display restock summary
    print("\n\t\t\t\t--- Restock Summary --- \n")
    print("------------------------------------------------------------------------------------------------------------")
    print("Product Name\t | Quantity\t | Cost Price\t | Subtotal\t |")
    print("------------------------------------------------------------------------------------------------------------")
    
    for i, product_id in enumerate(restock_cart):
        quantity = restock_quantities[i]
        cost = new_costs[i]
        subtotal = quantity * cost
        
        print(f"{items[product_id]['name']}\t | {quantity}\t\t | Rs.{cost:.2f}\t | Rs.{subtotal:.2f}\t |")
    
    print("------------------------------------------------------------------------------------------------------------")
    print(f"Total Cost: Rs.{total_cost:.2f}")
    
    # Confirm restock
    confirm = input("\nConfirm restock? (y/n): ")
    if confirm.lower() != 'y':
        print("\nRestock cancelled.")
        return items
    
    # Update quantities and costs
    updated_items = items.copy()
    for i, product_id in enumerate(restock_cart):
        updated_items[product_id]["quantity"] += restock_quantities[i]
        updated_items[product_id]["cost"] = new_costs[i]
    
    # Update products.txt
    update_products_file(updated_items)
    
    # Generate restock invoice
    generate_restock_invoice(supplier_name, updated_items, restock_cart, restock_quantities, new_costs)
    
    print("\nRestock completed successfully!")
    return updated_items
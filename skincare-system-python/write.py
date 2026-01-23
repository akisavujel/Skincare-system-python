import datetime

def writemessage(filename, message):
    try:
        with open(filename, 'w') as file:
            file.write(message)
        return True
    except Exception as e:
        print(f"Write operation failed for {filename}: {e}")
        return False

def update_products_file(products):
    """
    Update the products.txt file with the latest inventory data
    """
    try:
        lines = []
        for product in products:
            line = f"{product['name']}, {product['brand']}, {product['quantity']}, {product['cost']}, {product['country']}\n"
            lines.append(line)
        
        with open("products.txt", 'w') as file:
            file.writelines(lines)
        print("Product inventory successfully updated in products.txt")
        return True
    except Exception as e:
        print(f"Failed to update product inventory in products.txt: {e}")
        return False

def generate_sales_invoice(customer_name, products, cart_indices, quantities, total_amount):
    """
    Generate a sales invoice for a customer and save it to a file
    """
    # Generate a unique filename with timestamp
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"invoice_sale_{current_date}_{timestamp}.txt"
    
    # Create invoice content
    invoice_content = f"""
        WeCare Beauty Products
        Sales Invoice
        --------------------------------------
        Date: {current_date}
        Customer Name: {customer_name}
        --------------------------------------
        Products Purchased:
        """
    
    # Add each product to the invoice
    for i, product_id in enumerate(cart_indices):
        quantity = quantities[i]
        free_items = quantity // 3
        paid_items = quantity - free_items
        selling_price = products[product_id]["cost"] * 2
        subtotal = paid_items * selling_price
        
        invoice_content += f"""
        {products[product_id]['name']} ({products[product_id]['brand']})
        Quantity: {paid_items} (Paid) + {free_items} (Free) = {quantity}
        Price: Rs.{selling_price:.2f} each
        Subtotal: Rs.{subtotal:.2f}
            """
    
    # Add total amount
    invoice_content += f"""
        --------------------------------------
        Total Amount: Rs.{total_amount:.2f}
        --------------------------------------
        
        Thank you for shopping with WeCare!
        Visit again for more exciting offers.
        """
    
    # Write invoice to file
    if writemessage(filename, invoice_content):
        print(f"Sales invoice generated successfully: {filename}")
        return True
    else:
        print("Failed to generate sales invoice")
        return False

def generate_restock_invoice(supplier_name, products, restock_indices, restock_quantities, costs):
    """
    Generate a restock invoice for supplier purchases
    """
    # Generate a unique filename with timestamp
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.datetime.now().strftime("%H%M%S")
    filename = f"invoice_restock_{current_date}_{timestamp}.txt"
    
    # Calculate total cost
    total_cost = sum(restock_quantities[i] * costs[i] for i in range(len(restock_indices)))
    
    # Create invoice content
    invoice_content = f"""
        WeCare Beauty Products
        Restock Invoice
        --------------------------------------
        Date: {current_date}
        Supplier Name: {supplier_name}
        --------------------------------------
        Products Restocked:
        """
    
    # Add each product to the invoice
    for i, product_id in enumerate(restock_indices):
        quantity = restock_quantities[i]
        cost_price = costs[i]
        subtotal = quantity * cost_price
        
        invoice_content += f"""
        {products[product_id]['name']} ({products[product_id]['brand']})
        Quantity: {quantity}
        Cost Price: Rs.{cost_price:.2f} each
        Subtotal: Rs.{subtotal:.2f}
            """
    
    # Add total cost
    invoice_content += f"""
        --------------------------------------
        Total Cost: Rs.{total_cost:.2f}
        --------------------------------------
        
        Restock completed successfully.
        """
    
    # Write invoice to file
    if writemessage(filename, invoice_content):
        print(f"Restock invoice generated successfully: {filename}")
        return True
    else:
        print("Failed to generate restock invoice")
        return False
from read import readproducts
from operation import displayproduct, process_sale, restock_products

def main():
    filename = "products.txt"
    item = readproducts(filename)
    
    if not item:
        print("Cannot load products. Please check if products.txt exists.")
        return
    
    # Main program loop
    while True:
        print("\n===== WeCare Beauty Products Management System =====")
        print("1. View Available Products")
        print("2. Process Customer Sale")
        print("3. Restock Products")
        print("4. Exit")
        
        # Get user choice
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            # Display products
            displayproduct(item)
            input("\nPress Enter to continue...")
            
        elif choice == '2':
            # Process customer sale
            item = process_sale(item)
            input("\nPress Enter to continue...")
            
        elif choice == '3':
            # Restock products
            item = restock_products(item)
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            # Exit the program
            print("\nThank you for using WeCare Beauty Products Management System. See you soon!")
            break
            
        else:
            # Handle invalid input
            print("\nInvalid choice. Please try again.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
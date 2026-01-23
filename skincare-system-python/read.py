def readproducts(filename):
    item = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                part = line.strip().split(',')
                items = {
                    "name": part[0].strip(),
                    "brand": part[1].strip(), 
                    "quantity": int(part[2].strip()),
                    "cost": float(part[3].strip()),
                    "country": part[4].strip()
                }
                item.append(items)
        return item
    except FileNotFoundError:
        print("The file was not found")
        return None
import pandas as pd
from datetime import datetime

def generate_receipt():
    products = []
    barcodes = load_barcodes()
    total_price = 0
    
    while True:
        name = input("Enter the product name (q to quit): ")
        if name.lower() == 'q':
            break
        price = float(input("Enter the product price: "))
        total_price += price
        
        barcode = generate_barcode(name, price, barcodes)
        product = {'barcode': barcode, 'name': name, 'price': price, 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        products.append(product)
        
    save_to_csv(products)
    save_barcodes(barcodes)
    print(f"Total price of products in this session: {total_price}")

def generate_barcode(name, price, barcodes):
    key = name + str(price)
    if key in barcodes:
        return barcodes[key]
    else:
        barcode = str(len(barcodes) + 1).zfill(4)
        barcodes[key] = barcode
        return barcode

def load_barcodes():
    try:
        with open('barcodes.csv', 'r') as csvfile:
            df = pd.read_csv(csvfile)
            return df.set_index('name')['barcode'].to_dict()
    except FileNotFoundError:
        return {}

def save_barcodes(barcodes):
    df = pd.DataFrame(list(barcodes.items()), columns=['name', 'barcode'])
    df.to_csv('barcodes.csv', index=False)

def save_to_csv(products):
    df = pd.DataFrame(products)
    
    with open('receipts.csv', 'a', newline='') as csvfile:
        df.to_csv(csvfile, index=False, header=csvfile.tell()==0)

generate_receipt()


from subprocess import check_output

def get_motherboard():
    product = check_output('wmic baseboard get product').decode()
    product = product[7:len(product)]
    product = product.strip()
    return product

def get_manufacturer():
    manufacturer = check_output('wmic baseboard get Manufacturer').decode()
    manufacturer = manufacturer[13:len(manufacturer)]
    manufacturer = manufacturer.strip()
    return manufacturer
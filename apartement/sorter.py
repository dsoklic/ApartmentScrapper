import json
from collections import OrderedDict

def loadApartments(filename):
    with open(filename, 'r') as apartments_file:
        if filename.split('.')[-1] == 'json':
            apartments = json.loads(apartments_file.read())
    return apartments

def sortApartments(apartments, sortKey='ppsm'):
    sort_order = ['ppsm', 'location', 'year', 'link', 'price', 'size']
    orderedApartments = [OrderedDict(sorted(item.items(), key = lambda k: sort_order.index(k[0]))) for item in apartments]
    return sorted(orderedApartments, key=lambda apartment : apartment[sortKey])

def writeApartments(filename, apartments):
    if filename.split('.')[-1] == 'json':
        values = json.dumps(apartments, ensure_ascii=False)
        values = values.replace("},", "},\n")
    with open(filename, 'w') as f:
        if filename.split('.')[-1] == 'csv':
            f.write("price per square meter, location, year, link, price, size\n")
        # for apartment in self.apartments:
        #     yield apartment
        #     line = "{:.4f}, {:}, {:}, {:}, {:}, {:}\n".format(apartment['price per square meter'], apartment['location'], apartment['year'], apartment['link'], apartment['price'], apartment['size'])
        f.write(values)


def modifyApartments(inputFile, outputFile, sortKey='ppsm'):
    apartments = loadApartments(inputFile)
    apartments = sortApartments(apartments, sortKey)
    writeApartments(outputFile, apartments)
    return apartments

if __name__ == "__main__":
    apartments = modifyApartments('apartments.json', 'orderedApartments.json')

#memasukan kordinat dengan geoalchemy akan tersimpan sebagai WKT format
#maka convert WKT tersebut ke WKB format untuk mengambil latitude dan longtitude


from shapely import wkb, wkt
from binascii import unhexlify
#
# binnary = unhexlify(b'0101000000F7FFFFCE85285940B5E14C39A1A6CCBF')
# print(binnary)
#
# point = wkb.loads(binnary)
#
# print(point.x, point.y)
#
# print(wkt.dumps(point))


data = '01010000001100008890285940FF55ED493B85CCBF'
binnary = unhexlify(data)
print(binnary)


point = wkb.loads(binnary)
print(point.x)
print(point.y)

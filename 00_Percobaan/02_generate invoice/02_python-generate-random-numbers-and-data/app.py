# import random
#
# words = ['Kucing','Kambing','Harimau','Gajah','Jerapah']
#
# # numbers =
#
# value1 = random.randint(1,20)
# value2 = random.uniform(1,20)
# value3 = random.random()
#
# print(value1)
# print(value2)
# print(value3)
# print(value1 + value2)


import string
import random

def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

generate = 'HR' + generator_random() + 'INV'

print(generate)
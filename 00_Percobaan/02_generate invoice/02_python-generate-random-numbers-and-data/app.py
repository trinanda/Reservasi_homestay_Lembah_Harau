import string
import random

def generator_random(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

generate = 'HR' + generator_random() + 'INV'

print(generate)
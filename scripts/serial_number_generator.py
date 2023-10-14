import random
import string


def generate_serial_number(length):
    characters = string.ascii_uppercase + string.digits
    serial_number = ''.join(random.choice(characters) for _ in range(length))
    return serial_number


serial_numbers = []

for i in range(1000):
    product_serial_number = generate_serial_number(8)
    serial_numbers.append(f'"{product_serial_number}"')


print(f"[{', '.join(serial_numbers)}]")

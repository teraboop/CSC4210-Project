import numpy as np

def ensure_decimal_in_range(value):
    val_32_bit_max = (2**31) - 1
    val_32_bit_min = -(2**31)

    if (value >= val_32_bit_min and value <= val_32_bit_max):
        return True
    else:
        print(f"Value {value} is out of range. Please enter a value between {val_32_bit_min} and {val_32_bit_max}.")
        return False

def decimal_input():
    while True:
        try:
            value = input("Enter a decimal value: ")
            if ensure_decimal_in_range(value) and value.is_integer():
                return value
        except ValueError: 
            print("Invalid input. Please enter a valid decimal number.")

def twos_complement_helper(binary):
    

def decimal_to_binary(value):
    if value == 0:
        return "0"
    
    corrected_value = abs(value)
    binary = ""


    while corrected_value > 0:
        remainder = corrected_value % 2
        binary = str(remainder) + binary
        corrected_value //= 2

    if value < 0:
        binary = twos_complement_helper(binary)

    return binary

def decimal_to_hexadecimal(value):
    if value == 0:
        return "0"
    
    hexadecimal = ""
    hex_digits = "0123456789ABCDEF"
    
    while value > 0:
        remainder = value % 16
        hexadecimal = hex_digits[remainder] + hexadecimal
        value //= 16

    return hexadecimal

def binary_to_hexadecimal(binary):
    hex_digits = "0123456789ABCDEF"
    arr = np.empty((8, 4))
    for each in binary:
        
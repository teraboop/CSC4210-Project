#Edward Lippel

import numpy as np
global overflowFlag, saturatedFlag, val_32_bit_min, val_32_bit_max
val_32_bit_max = 2147483647
val_32_bit_min = -2147483648
overflowFlag = 0
saturatedFlag = 0

# This function checks if the input decimal value is within the range of a 32-bit signed integer.
# If the value is outside this range, it sets the overflow and saturated flags.
#input: integer value (decimal number)
#output: boolean (True if in range, False otherwise. If false internally throws flags and prints messages if overflow is detected)
def ensure_decimal_in_range(value):


    if (value >= val_32_bit_min and value <= val_32_bit_max):
        return True
    else:
        global overflowFlag, saturatedFlag
        overflowFlag = 1

        print(f"OVERFLOW DETECTED: Value '{value}' is outside 32-bit signed integer range. Clamped to the nearest limit.")
        saturatedFlag = 1
        return False

# This function prompts the user to enter a decimal value, then validates that input is within a valid range.
#output: integer value (decimal number that is guaranteed to be within the range of a 32-bit signed integer)
def decimal_input():
    while True:
        try:
            value = int(input("Enter a decimal value: "))
            if ensure_decimal_in_range(value):
                return value
            else:
                if value > 0:
                    value = val_32_bit_max
                else:
                    value = val_32_bit_min
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# This helper function computes the two's complement of a binary string.
#input: binary string (32-bit representation of a number)
#output: binary string (two's complement of the input binary string)
def twos_complement_helper(binary):
    if binary == '11111111111111111111111111111111':
        return binary
    flipped = ''
    for bit in binary:
        if bit == '1':
            flipped += '0'
        else:
            flipped += '1'
    flipped = flipped.zfill(32)
    carry = 1
    result = ''
    for bit in flipped[::-1]:
        if bit == '1' and carry == 1:
            result = '0' + result
        elif bit == '0' and carry == 1:
            result = '1' + result
            carry = 0
        else:
            result = bit + result
    return result

    
# This function converts a decimal integer to its binary representation as a 32-bit string.
# If the input value is negative, it computes the two's complement to represent it in binary.
#input: integer value (decimal number)
#output: string (32-bit binary representation of the input decimal number)
def decimal_to_binary(value: int):
    if value == 0:
        return "".zfill(32)
    if ensure_decimal_in_range(value) == False:
        if value > 0:
            value = val_32_bit_max
        else:
            value = val_32_bit_min
    if value == val_32_bit_min:
        return '11111111111111111111111111111111'
    
    corrected_value = abs(value)
    binary = ""


    while corrected_value > 0:
        remainder = corrected_value % 2
        binary = str(remainder) + binary
        corrected_value //= 2

    binary = binary.zfill(32)
    if value < 0:
        binary = twos_complement_helper(binary)

    return binary

# This function converts a binary string to its hexadecimal representation.
# It processes the binary string in groups of 4 bits, calculates the corresponding hexadecimal digit for
# each group, and concatenates these digits to form the final hexadecimal string.
#input: string (32-bit binary representation of a number)
#output: string (hexadecimal representation of the input binary string)
def binary_to_hexadecimal(binary):
    hex_digits = "0123456789ABCDEF"
    binary = binary.zfill(32)
    arr = np.zeros((8, 4))

    for i in range(8):
        for j in range(4):
            arr[i][j] = binary[i*4 + j]
    hexadecimal = ""
    for i in range(8):
        value = 0
        for j in range(4):
            value += int(arr[i][j]) * (2 ** (3 - j))
        hexadecimal += hex_digits[value]
    
    return hexadecimal

# This function converts a binary string to its decimal integer representation.
# It iterates through each bit in the binary string, calculating its contribution to the total decimal
# value based on its position and the base (2) raised to the appropriate power.
#input: string (32-bit binary representation of a number)
#output: integer value (decimal representation of the input binary string)
def binary_to_decimal(binary):
    if binary == '11111111111111111111111111111111':
        return val_32_bit_min
    decimal = 0
    MSB = binary[0]
    if MSB == '1':
        binary = twos_complement_helper(binary)
        for i in range(len(binary)):
            decimal += int(binary[len(binary) - 1 - i]) * (2 ** i)
        decimal = -decimal
    else:
        for i in range(len(binary)):
            decimal += int(binary[len(binary) - 1 - i]) * (2 ** i)
    return decimal

def main():
    while True:
        decimal_value = decimal_input()
        selected_output = input(f"Enter output type (DEC/BIN/HEX): ").upper()
        if selected_output == "DEC":
            print(f"Decimal: {decimal_value}")
            print(f"Overflow Flag: {overflowFlag}")
            print(f"Saturated Flag: {saturatedFlag}")
        elif selected_output == "BIN":
            binary_value = decimal_to_binary(decimal_value)
            print(f"Binary: {binary_value}")
            print(f"Overflow Flag: {overflowFlag}")
            print(f"Saturated Flag: {saturatedFlag}")
        elif selected_output == "HEX":
            hexadecimal_value = decimal_to_hexadecimal(decimal_value)
            print(f"Hexadecimal: {hexadecimal_value}")
            print(f"Overflow Flag: {overflowFlag}")
            print(f"Saturated Flag: {saturatedFlag}")
        else:
            print("Invalid output type selected. Please choose DEC, BIN, or HEX.")
        if input("Do you want to continue? (Y/N): ").upper() != "Y":
            break

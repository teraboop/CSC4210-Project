import numpy as np

def readTruthTableFile(boolean_file, variable_count):
    boolean_values = np.zeros((2 ** variable_count, variable_count + 1), dtype=int)
    with open(boolean_file, 'r') as f:
        row_index = 0
        for line in f:
            if row_index >= boolean_values.shape[0]:
                raise ValueError(f"More rows in the file than expected for {variable_count} variables.")
            line = line.strip()
            col_index = 0
            for char in line:
                if col_index >= boolean_values.shape[1]:
                    raise ValueError(f"More columns in the file than expected for {variable_count} variables.")
                if char == '1':
                    boolean_values[row_index, col_index] = 1
                elif char == '0':
                    boolean_values[row_index, col_index] = 0
                else:
                    raise ValueError(f"Invalid boolean value '{char}' in file '{boolean_file}.txt'.")
                col_index += 1
            row_index += 1
    return boolean_values

def takeNumberOfVariables():
    while True:
        try:
            variable_count = int(input("How many variables are in the truth table? (Enter a positive integer): "))
            if variable_count > 0:
                return variable_count
            else:
                raise ValueError("Number of variables must be a positive integer.")
        except ValueError as e:
            print(f"Invalid input. Error: {e}")
        finally:
            return variable_count
        
def getTruthTableFileName():
    while True:
        boolean_file = input("Enter the name of the file containing the boolean values (no file extension): ")
        boolean_file += ".txt"
        return boolean_file
    
def validateTruthTable(boolean_values, variable_count):
    expected_length = (2 ** variable_count) * (variable_count + 1)
    actual_length = boolean_values.size
    if actual_length != expected_length:
        raise ValueError(f"Expected {expected_length} boolean values for {variable_count} variables, but got {actual_length}.")
    return True
        


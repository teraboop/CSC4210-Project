def readTruthTableFile(boolean_file):
    boolean_values = []
    with open(boolean_file, 'r') as f:
        for line in f:
            line = line.strip()
            for char in line:
                if char == '1':
                    boolean_values.append(1)
                elif char == '0':
                    boolean_values.append(0)
                else:
                    print(f"Invalid boolean value '{char}' in file. Skipping.")
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
        
def takeTruthTableFileName(variable_count):
    while True:
        boolean_file = input("Enter the name of the file containing the boolean values (no file extension): ")
        boolean_file += ".txt"
        return boolean_file
    
def validateTruthTable(boolean_values, variable_count):
    expected_length = 2 ** variable_count
    if len(boolean_values) != expected_length:
        print(f"Error: The number of boolean values ({len(boolean_values)}) does not match the expected length ({expected_length}) for {variable_count} variables.")
        return False
    return True


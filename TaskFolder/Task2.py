import numpy as np

def readTruthTableFile(boolean_file, variable_count):
    boolean_values = np.zeros((2 ** variable_count, variable_count + 1), dtype=int)
    with open(boolean_file, 'r') as f:
        row_index = 0
        for line in f:
            if row_index >= boolean_values.shape[0]:
                raise ValueError(f"More rows in the file than expected for {variable_count} variables.")
            line = ''.join(line.split())
            col_index = 0
            for char in line:
                if col_index >= boolean_values.shape[1]:
                    raise ValueError(f"More columns in the file than expected for {variable_count} variables.")
                if char == '1':
                    boolean_values[row_index, col_index] = 1
                elif char == '0':
                    boolean_values[row_index, col_index] = 0
                else:
                    print(f"Invalid character '{char}' in the file. Skipping.")
                col_index += 1
            row_index += 1
    return boolean_values

def getNumberOfVariables():
    while True:
        try:
            variable_count = int(input("How many variables are in the truth table? (Enter a positive integer): "))
            if variable_count >= 2:
                return variable_count
            else:
                raise ValueError("Number of variables must be a positive integer 2 or greater.")
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
        
def getOutputFormat():
    while True:
        output_format = input("Would you like the equation to be in Sum of Products (SOP) or Product of Sums (POS) form? (Enter 'SOP' or 'POS'): ").strip().upper()
        if output_format in ['SOP', 'POS']:
            return output_format
        else:
            print("Invalid input. Please enter 'SOP' or 'POS'.")

def getOutputColumn(boolean_values):
    outputColumn = []
    for row in boolean_values:
        outputColumn.append(row[-1])
    return outputColumn

def generateSumOfProducts(boolean_values, variable_count):

    sop_terms = []
    for i in range(boolean_values.shape[0]):
        if boolean_values[i, -1] == 1:
            term = []
            for j in range(variable_count):
                if boolean_values[i, j] == 1:
                    term.append(f"x{j + 1}")
                else:
                    term.append(f"x{j + 1}'")
            sop_terms.append('*'.join(term))
    return ' + '.join(sop_terms)

def generateProductOfSums(boolean_values, variable_count):
    pos_terms = []
    for i in range(boolean_values.shape[0]):
        if boolean_values[i, -1] == 0:
            term = []
            for j in range(variable_count):
                if boolean_values[i, j] == 1:
                    term.append(f"x{j + 1}'")
                else:
                    term.append(f"x{j + 1}")
            pos_terms.append(' (' + ' + '.join(term) + ') *')
    return ''.join(pos_terms)

def validateSimplifiedEquation(simplified_equation, boolean_values, variable_count):
    for i in range(boolean_values.shape[0]):
        expected_output = boolean_values[i, -1]
        variable_values = boolean_values[i, :variable_count]
        eval_equation = simplified_equation
        for j in range(variable_count):
            eval_equation = eval_equation.replace(f"x{j + 1}'", str(1 - variable_values[j]))
            eval_equation = eval_equation.replace(f"x{j + 1}", str(variable_values[j]))
        try:
            actual_output = int(eval(eval_equation) > 0)
            if actual_output != expected_output:
                print(f"FAIL for input {variable_values}. Expected: {expected_output}, Got: {actual_output}")
                return False
        except Exception as e:
            print(f"FAIL for input {variable_values}. Error: {e}")
            return False
    print("PASS")
    return True

def printMintermMaxtermList(POS, SOP, variable_count):
    POS_terms = POS.split('*')
    SOP_terms = SOP.split('+')
    print("Minterm List:")
    for term in SOP_terms:
        print(f"  {term}")
    print("Maxterm List:")
    for term in POS_terms:
        print(f"  {term}")

def kmap_simplify(boolean_values, variable_count):
    if variable_count < 2 or variable_count > 4:
        raise ValueError("K-map grouping supports 2-4 variables only.")

    def gray_code(n):
        return [i ^ (i >> 1) for i in range(2 ** n)]

    row_vars = variable_count // 2
    col_vars = variable_count - row_vars

    rows = 2 ** row_vars
    cols = 2 ** col_vars

    row_codes = gray_code(row_vars)
    col_codes = gray_code(col_vars)

    kmap = [[0] * cols for _ in range(rows)]

    for i in range(boolean_values.shape[0]):
        if boolean_values[i, -1] == 1:
            bits = boolean_values[i, :variable_count]

            row_bits = bits[:row_vars]
            col_bits = bits[row_vars:]

            r = row_codes.index(int(''.join(map(str, row_bits)), 2)) if row_vars else 0
            c = col_codes.index(int(''.join(map(str, col_bits)), 2)) if col_vars else 0

            kmap[r][c] = 1

    def get_cells(sr, sc, h, w):
        cells = []
        for dr in range(h):
            for dc in range(w):
                r = (sr + dr) % rows
                c = (sc + dc) % cols
                cells.append((r, c))
        return cells

    def valid_group(cells):
        return all(kmap[r][c] == 1 for r, c in cells)

    def extract_term(cells):
        term = []

        for bit in range(row_vars):
            vals = set()
            for r, _ in cells:
                g = row_codes[r]
                vals.add((g >> (row_vars - 1 - bit)) & 1)

            if len(vals) == 1:
                v = vals.pop()
                term.append(f"x{bit+1}" if v else f"x{bit+1}'")

        for bit in range(col_vars):
            vals = set()
            for _, c in cells:
                g = col_codes[c]
                vals.add((g >> (col_vars - 1 - bit)) & 1)

            if len(vals) == 1:
                idx = row_vars + bit + 1
                v = vals.pop()
                term.append(f"x{idx}" if v else f"x{idx}'")

        return '*'.join(term) if term else '1'

    groups = []

    for size in [8, 4, 2, 1]:
        for h in [1, 2, 4]:
            for w in [1, 2, 4]:
                if h * w != size or h > rows or w > cols:
                    continue

                for r in range(rows):
                    for c in range(cols):
                        cells = get_cells(r, c, h, w)
                        if valid_group(cells):
                            groups.append({
                                "cells": set(cells),
                                "term": extract_term(cells),
                                "size": size
                            })

    unique = []
    seen = set()

    for g in groups:
        key = tuple(sorted(g["cells"]))
        if key not in seen:
            seen.add(key)
            unique.append(g)

    groups = unique

    def literal_count(term):
        if term == '1':
            return 0
        return term.count('x')
    
    groups.sort(key=lambda g: (-g["size"], literal_count(g["term"])))


    ones = {(r, c) for r in range(rows) for c in range(cols) if kmap[r][c] == 1}

    cover_map = {cell: [] for cell in ones}

    for i, g in enumerate(groups):
        for cell in g["cells"]:
            if cell in cover_map:
                cover_map[cell].append(i)

    selected = set()
    covered = set()

    for cell, g_list in cover_map.items():
        if len(g_list) == 1:
            idx = g_list[0]
            selected.add(idx)

    for idx in selected:
        covered |= groups[idx]["cells"]

    while covered != ones:
        best_idx = None
        best_score = -1

        for i, g in enumerate(groups):
            new_cover = g["cells"] - covered
            if not new_cover:
                continue

            term_len = literal_count(g["term"])
            score = len(new_cover) * 10 - term_len

            if best_idx is None or score > best_score:
                best_score = score
                best_idx = i

        if best_idx is None:
            break

        selected.add(best_idx)
        covered |= groups[best_idx]["cells"]
    
    print("Selected groups:")
    for i in selected:
        print(f"{groups[i]['term']} -> {groups[i]['cells']}")

    print()
    terms = [groups[i]["term"] for i in selected]

    return ' + '.join(sorted(set(terms)))

def main():
    variable_count = getNumberOfVariables()
    boolean_file = getTruthTableFileName()
    boolean_values = readTruthTableFile(boolean_file, variable_count)
    validateTruthTable(boolean_values, variable_count)
    output_format = getOutputFormat()
    simplified = kmap_simplify(boolean_values, variable_count)
    print(f"Boolean Values:\n{boolean_values}")

    match output_format:
        case "SOP":
            equation = generateSumOfProducts(boolean_values, variable_count)
        case "POS":
            equation = generateProductOfSums(boolean_values, variable_count)
    
    print(f"{output_format}: {equation}")
    printMintermMaxtermList(generateProductOfSums(boolean_values, variable_count), generateSumOfProducts(boolean_values, variable_count), variable_count)
    print(f"The {output_format} form of the equation is: {equation}")
    print(f"\nSimplified {output_format}: {simplified}")
    validateSimplifiedEquation(simplified, boolean_values, variable_count)

main()
'''
Steps to go from a CFG to a Chomsky Normal Form (CNF) grammar:
1. Remove epsilon productions
2. Remove unit productions
3. Remove useless symbols
4. Remove terminals from right-hand sides of productions
5. Remove productions with more than two non-terminals on the right-hand side
6. Convert remaining productions to CNF
'''

from helper import read_input_file

file_name = "input.txt"

# Step 1: Remove epsilon productions
def remove_epsilon_productions(grammar):
    epsilon_vars = {var for var, prods in grammar.items() if 'ε' in prods}
    print("Epsilon variables:", epsilon_vars)
    for var in epsilon_vars:
        grammar[var].remove('ε')
        # Replace all productions of the form A -> αBβ with A -> αβ for all B -> ε
        for v, prods in grammar.items():
            for prod in prods:
                if var in prod:
                    new_prods = [prod.replace(var, '')]
                    grammar[v] += new_prods
    return grammar

grammar = read_input_file(file_name)
grammar = remove_epsilon_productions(grammar)
print(grammar)

# Step 2: Remove unit productions
def remove_unit_productions(grammar):

    # Remove productions of the form A -> A
    for var, prods in grammar.items():
        grammar[var] = [prod for prod in prods if prod != var]

    unit_prods = {}
    for var, prods in grammar.items():
        unit_prods[var] = [prod for prod in prods if len(prod) == 1 and prod.isupper()]
        print("Unit productions for", var, ":", unit_prods[var])
    
    for var, prods in unit_prods.items():
        # If prod is not empty, replace
        if prods:
            print("Replacing unit productions for", var, ":", grammar[var])
            for element in list(grammar[var]):  # Create a copy of the list before iterating
                if element in prods:
                    grammar[var].remove(element)
                    grammar[var] += grammar[element]
            grammar[var] = list(set(grammar[var]))
            print("After replacing unit productions for", var, ":", grammar[var])
    return grammar

grammar = remove_unit_productions(grammar)
print(grammar)
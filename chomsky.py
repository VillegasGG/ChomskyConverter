'''
Steps to go from a CFG to a Chomsky Normal Form (CNF) grammar:
1. Remove epsilon productions
2. Remove unit productions
3. Remove useless symbols
4. Remove terminals 
5. Remove productions with more than two non-terminals on the right-hand side
6. Convert remaining productions to CNF
'''

from helper import read_input_file

file_name = "input.txt"

# Step 1: Remove epsilon productions
def remove_epsilon_productions(grammar):
    epsilon_vars = {var for var, prods in grammar.items() if 'ε' in prods}
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
    
    for var, prods in unit_prods.items():
        # If prod is not empty, replace
        if prods:
            for element in list(grammar[var]):  # Create a copy of the list before iterating
                if element in prods:
                    grammar[var].remove(element)
                    grammar[var] += grammar[element]
            grammar[var] = list(set(grammar[var]))
    return grammar

grammar = remove_unit_productions(grammar)
print(grammar)

# Step 3: Remove useless symbols
def remove_useless_symbols(grammar):
    start_symbol = 'S'
    reachable = set()
    reachable.add(start_symbol)
    old_len = 0
    while len(reachable) != old_len:
        old_len = len(reachable)
        for var, prods in grammar.items():
            for prod in prods:
                if all([p in reachable or p.islower() for p in prod]):
                    reachable.add(var)
    for var in list(grammar.keys()):
        if var not in reachable:
            del grammar[var]
    return grammar

grammar = remove_useless_symbols(grammar)
print(grammar)

# Step 4: Remove terminals 
def remove_terminals(grammar):
    terminals = []
    for var, prods in grammar.items():
        for prod in prods:
            terminals += [p for p in prod if p.islower()]
    terminals = set(terminals)
    new_varibles = {}
    for terminal in terminals:
        new_varibles[terminal] = 'X_' + terminal
    
    # Replace terminals with new variables
    for production in grammar.values():
        for element in list(production):
            if element in terminals:
                production.remove(element)
                production.append(new_varibles[element])

    # Add new productions
    for terminal, new_var in new_varibles.items():
        grammar[new_var] = [terminal]

    return grammar

grammar = remove_terminals(grammar)
print(grammar)
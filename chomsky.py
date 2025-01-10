'''
Steps to go from a CFG to a Chomsky Normal Form (CNF) grammar:
1. Remove epsilon productions
2. Remove unit productions
3. Remove useless symbols
4. Remove terminals 
5. Remove productions with more than two non-terminals on the right-hand side
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

# Step 5: Remove productions with more than two non-terminals on the right-hand side
def remove_more_than_two_non_terminals(grammar):
    productions_to_remove = []
    for var, prods in grammar.items():
        for prod in prods:
            if len([p for p in prod if p.isupper()]) > 2:
                productions_to_remove.append((var, prod))
    
    for var, prod in productions_to_remove:
        grammar[var].remove(prod)
        # Divide the production into productions with two non-terminals
        new_vars = []
        for i in range(1, len(prod) - 1):
            new_var = 'X_' + var + str(i)
            new_vars.append(new_var)
            grammar[new_var] = prod[i] + prod[i+1]

        grammar[var].append(prod[0] + new_vars[0])

    return grammar

grammar = remove_more_than_two_non_terminals(grammar)
print(grammar)

def is_cnf(grammar):
    for key, prods in grammar.items():
        for prod in prods:
            # Check if is a terminal
            if len(prod) == 1 and prod.islower() and not 'X_' in key:
                print("Terminal found: ", key, '->', prod)
                return False
            # Check if is a unit production
            if len(prod) == 1 and prod.isupper() and not 'X_' in key:
                print("Unit production found: ", key, '->', prod)
                return False
            # Check if is a production with more than two non-terminals
            if len([p for p in prod if p.isupper()]) > 2 and not 'X_' in prod:
                print("Production with more than two non-terminals found: ", key, '->', prod)
                return False
            
    return True

# Check if the grammar is in CNF
result = is_cnf(grammar)
print(result)

# Save the CNF grammar to a file
def save_cnf_grammar(grammar, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        for var, prods in grammar.items():
            file.write(var + ' -> ' + ' | '.join(prods) + '\n')

save_cnf_grammar(grammar, "cnf_grammar.txt")

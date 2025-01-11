'''
Steps to go from a CFG to a Chomsky Normal Form (CNF) grammar:
0. Eliminate start symbol from right-hand side of productions
1. Remove epsilon productions
2. Remove unit productions
3. Remove useless symbols
4. Remove terminals 
5. Remove productions with more than two non-terminals on the right-hand side
'''

from helper import read_input_file, save_grammar
from itertools import combinations

file_name = "input.txt"

# Step 0: Eliminate start symbol from right-hand side of productions
def eliminate_start_symbol(grammar):
    start_symbol = 'S'
    new_start_symbol = 'S_0'
    # Add new start symbol at the beginning of the grammar
    grammar = {new_start_symbol: [start_symbol], **grammar}
    return grammar

grammar = read_input_file(file_name)
grammar = eliminate_start_symbol(grammar)
print("Step 0: Eliminate start symbol from right-hand side of productions")
print(grammar)
save_grammar(grammar, "after_step_0.txt")

# Step 1: Remove epsilon productions
def find_nullable_variables(grammar):
    """
    Find nullable variables in the grammar.
    """
    nullable = set()
    for var, prods in grammar.items():
        if 'ε' in prods:
            nullable.add(var)
    # Find nullable variables produced by nullable variables
    def find_nullable(grammar, nullable):
        new_nullable = set(nullable)
        for var, prods in grammar.items():
            for prod in prods:
                if all([p in nullable or p.islower() for p in prod]):
                    new_nullable.add(var)
        if new_nullable == nullable:
            return new_nullable
        else:
            return find_nullable(grammar, new_nullable)

    return find_nullable(grammar, nullable)

def remove_epsilon_productions(grammar):
    """
    - Generate new rule R by removing nullable variables
    - Remove epsilon productions except for the start symbol
    """
    nullable = find_nullable_variables(grammar)
    print("Nullable variables: ", nullable)

    # Generate new rule R by removing nullable variables from its right side
    new_productions = {}

    # If nullable variable is in the right side of a production:
    # - The number of  new rules is 2^(number of nullable variables)-1
    # - Generate new rule is added if it is not already among the rules

    for var, prods in grammar.items():
        for prod in prods:
            nullable_positions = [i for i, p in enumerate(prod) if p in nullable]
            for i in range(1, len(nullable_positions) + 1):
                for comb in combinations(nullable_positions, i):
                    new_prod = list(prod)
                    for pos in comb:
                        new_prod[pos] = ''
                    new_prod = ''.join(new_prod)
                    if new_prod and new_prod not in grammar[var]:
                        new_productions[var] = new_productions.get(var, []) + [new_prod]

    # Add new rules to the grammar
    for var, prods in new_productions.items():
        grammar[var] += prods

    # Add epsilon to the nullable variables
    for var in nullable:
        grammar[var].append('ε')

    # Remove epsilon productions except for the start symbol
    for var, prods in grammar.items():
        for prod in prods:
            if 'ε' in prod and var != 'S_0':
                grammar[var].remove(prod)
    
    # Remove repeated productions
    for var, prods in grammar.items():
        grammar[var] = list(set(prods))

    return grammar

grammar = remove_epsilon_productions(grammar)
print("Step 1: Remove epsilon productions")
print(grammar)
save_grammar(grammar, "after_step_1.txt")

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
print("Step 2: Remove unit productions")
print(grammar)
save_grammar(grammar, "after_step_2.txt")

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
print("Step 3: Remove useless symbols")
print(grammar)
save_grammar(grammar, "after_step_3.txt")

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

    # Remove terminals ex A->aa and add new productions
    for var, prods in grammar.items():
        for prod in prods:
            if len(prod) > 1:
                new_prods = []
                for p in prod:
                    if p in terminals:
                        new_prods.append(new_varibles[p])
                    else:
                        new_prods.append(p)
                grammar[var].remove(prod)
                grammar[var].append(''.join(new_prods))

    return grammar

grammar = remove_terminals(grammar)
print("Step 4: Remove terminals")
print(grammar)
save_grammar(grammar, "after_step_4.txt")

# Step 5: Remove productions with more than two non-terminals on the right-hand side
def remove_more_than_two_non_terminals(grammar):
    new_productions = {}
    counter = 1  # Contador para nombres únicos

    for var, prods in grammar.items():
        updated_prods = []
        for prod in prods:
            # Divide las producciones con más de dos no terminales
            if len([p for p in prod if p.isupper()]) > 2:
                current_prod = list(prod)  # Asegúrate de trabajar con una lista de caracteres
                while len([p for p in current_prod if p.isupper()]) > 2:
                    # Crea una nueva variable para los dos primeros no terminales
                    new_var = f"X_{counter}"
                    counter += 1
                    
                    # Reemplaza los dos primeros no terminales con la nueva variable
                    new_productions[new_var] = [''.join(current_prod[:2])]
                    current_prod = [new_var] + current_prod[2:]  # Actualiza la producción restante

                updated_prods.append(''.join(current_prod))
            else:
                updated_prods.append(prod)

        grammar[var] = updated_prods

    # Añadir las nuevas producciones a la gramática
    grammar.update(new_productions)
    return grammar


grammar = remove_more_than_two_non_terminals(grammar)
print(grammar)
save_grammar(grammar, "after_step_5.txt")

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


save_grammar(grammar, "cnf_grammar.txt")

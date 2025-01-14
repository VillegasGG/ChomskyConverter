'''
Testing chomsy.py step by step
'''
from chomsky import eliminate_start_symbol, remove_epsilon_productions, remove_unit_productions, remove_useless_symbols, remove_terminals
from helper import read_input_file


file_name = "input.txt"

# Is there any epsilon production in the grammar?
def test_epsilon_productions(grammar):
    for key in grammar:
        for production in grammar[key]:
            if production == 'e':
                print("Epsilon production found")
                return True
    print("No epsilon production found")
    return False

# Testing step 1: Remove epsilon productions
def test_remove_epsilon_productions():
    print("\nTesting step 1: Remove epsilon productions")
    grammar = read_input_file(file_name)
    grammar = eliminate_start_symbol(grammar)
    grammar = remove_epsilon_productions(grammar)
    isEpsilon = test_epsilon_productions(grammar)
    if isEpsilon:
        print("Step 1: Remove epsilon productions failed")
    else:
        print("Step 1: Remove epsilon productions passed")
    print('\n')

test_remove_epsilon_productions()

# Is there any unit production in the grammar?
def test_unit_productions(grammar):
    for key in grammar:
        for production in grammar[key]:
            if len(production) == 1 and production.isupper():
                print("Unit production found")
                return True
    print("No unit production found")
    return False

# Testing step 2: Remove unit productions
def test_remove_unit_productions():
    print("Testing step 2: Remove unit productions")
    grammar = read_input_file(file_name)
    grammar = eliminate_start_symbol(grammar)
    grammar = remove_epsilon_productions(grammar)
    grammar = remove_unit_productions(grammar)
    isUnit = test_unit_productions(grammar)
    if isUnit:
        print("Step 2: Remove unit productions failed")
    else:
        print("Step 2: Remove unit productions passed")
    print('\n')

test_remove_unit_productions()

# is there any unreachable symbols in the grammar?
def test_unreachable_symbols(grammar):
    start_symbol = 'S_0'
    reachable = set()
    reachable.add(start_symbol)
    old_len = 0
    while len(reachable) != old_len:
        old_len = len(reachable)
        for var, prods in grammar.items():
            for prod in prods:
                if all([p in reachable or p.islower() for p in prod]):
                    reachable.add(var)
    for key in grammar:
        if key not in reachable:
            print("Unreachable symbol found")
            return True
    print("No unreachable symbol found")
    return False

# Testing step 3: Remove useless symbols
def test_remove_useless_symbols():
    print("Testing step 3: Remove useless symbols")
    grammar = read_input_file(file_name)
    grammar = eliminate_start_symbol(grammar)
    grammar = remove_epsilon_productions(grammar)
    grammar = remove_unit_productions(grammar)
    grammar = remove_useless_symbols(grammar)
    isUnreachable = test_unreachable_symbols(grammar)
    if isUnreachable:
        print("Step 3: Remove useless symbols failed")
    else:
        print("Step 3: Remove useless symbols passed")
    print('\n')

test_remove_useless_symbols()
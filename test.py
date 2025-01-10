'''
Testing chomsy.py step by step
'''
from chomsky import remove_epsilon_productions
from helper import read_input_file


file_name = "input.txt"

# Testing step 1: Remove epsilon productions
def test_remove_epsilon_productions():
    grammar = read_input_file(file_name)
    grammar = remove_epsilon_productions(grammar)
    print(grammar)
    assert grammar == {'S': ['AB', 'BC', 'a', 'B'], 'A': ['aA', 'a'], 'B': ['b', 'AB', 'B'], 'C': ['c']}
    print("Step 1: Remove epsilon productions passed")

test_remove_epsilon_productions()
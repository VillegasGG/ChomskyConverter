file_name = "input.txt"

def read_input_file(input_file_name):
    """Reads a context-free grammar from a file and returns it as a dictionary."""
    grammar = {}
    with open(input_file_name, 'r', encoding='utf-8') as file:
        print("Reading input file...")
        for line in file:
            line = line.strip()
            if line:
                non_terminal, productions = line.split('->')
                grammar[non_terminal.strip()] = [production.strip() for production in productions.split('|')]
    return grammar

print(read_input_file(file_name))
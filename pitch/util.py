
def print_line(line_char: str, edge_char: str, line_len: int = 80):
    padding_len = line_len - 2
    padding = line_char* padding_len
    print(f'{edge_char}{padding}{edge_char}')

def print_form(line: str):
    line_len = len(line)
    padding_len = 80 - (line_len + 4)
    padding = ' ' * padding_len
    print(f'| {line}{padding} |')


DEFAULT_LINE_LENGTH = 100


import logging
import socket

def get_line_ln(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    return get_line(line_char, edge_char, line_len) + "\n"


def get_line(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    padding_len = line_len - 2
    padding = line_char * padding_len
    return f"{edge_char}{padding}{edge_char}"


def print_line(line_char: str, edge_char: str, line_len: int = DEFAULT_LINE_LENGTH):
    print(get_line(line_char, edge_char, line_len))


def get_form_ln(line: str) -> str:
    return get_form(line) + "\n"


def get_form(line: str) -> str:
    line_len = len(line)
    padding_len = DEFAULT_LINE_LENGTH - (line_len + 4)
    padding = " " * padding_len
    return f"| {line}{padding} |"


def print_form(line: str):
    print(get_form(line))

def set_up_logging(verbose: bool, debug: bool) -> None:
    logger = logging.getLogger()

    # Create handlers
    stream_handler = logging.StreamHandler()
    if verbose:
        print(f"verbose: {verbose}")
        stream_handler.setLevel(logging.INFO)
    else:
        stream_handler.setLevel(logging.WARN)

    stream_format = logging.Formatter("%(message)s")
    stream_handler.setFormatter(stream_format)
    logger.addHandler(stream_handler)

    logger.setLevel(logging.DEBUG)

def send_over_udp(seq, mac, ip, port):
    """
    """
    #(d_mac, addr, port) = (addr_port_tup[0], addr_port_tup[1], addr_port_tup[2])
    #addr_port_tup = (d_mac, config.publish_host(), config.publish_port())
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((ip, port))

    sock.send(seq_unit_hdr.get_bytes())
    sock.close()

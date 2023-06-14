import argparse
from datetime import datetime
from pitch.generator import Generator, WatchListItem
import sys
from typing import Any
from .util import print_line, print_form

def parse_args(parser) ->  Any:
    return parser.parse_args()

def main():
    parser = argparse.ArgumentParser(
            prog='PITCH.Generator',
            description='PITCH Message Generator and Parser',
            epilog='Bottom of help text'
            )
    parser.add_argument(
            '-v',
            '--verbose',
            default=False,
            action='store_true',
            help='Verbose')
    parser.add_argument(
            '-n',
            '--num-of-msgs',
            default=10,
            help='Number of Messages to Generate')
    parser.add_argument(
            '-o',
            '--output-file',
            default='pitch24.dat',
            help='Specify output file')
    args = parse_args(parser)

    # Set these variables from argument
    ticker = 'MSFT'
    weight = 0.50
    num_of_msgs = 10
    book_size_range = (1, 3)
    msg_rate_p_sec = 5
    verbose = args.verbose

    start_time = datetime.now()

    #print(f'Start time: {start_time}')

    watch_list = [
            WatchListItem(ticker=ticker,
                          weight=weight,
                          book_size_range=book_size_range,
                          price_range=(50.00, 65.00),
                          size_range=(25, 200)
                          )
            ]
    generator = Generator(watch_list=watch_list,
                          msg_rate_p_sec=msg_rate_p_sec,
                          start_time=start_time,
                          )
    sep_len = 100
    if verbose:
        print_line('=', '=', sep_len)
        print_line('=', '=', sep_len)
        print('Initial Order Book\n')
        generator._orderbook.print_order_book(ticker)

    f_ascii = open('orders.log', 'w')
    f_bin = open('orders.dat', 'wb')

    for i in range(num_of_msgs):
        if verbose:
            print_line(' ', ' ')
            print_line(' ', ' ')
        new_msg = generator.getNextMsg()

        if verbose:
            print_line('=', '=', sep_len)
        print_line('=', '=', sep_len)
        print(f'Message #{i+1}:    {new_msg}')
        new_msg_bytes = new_msg.get_bytes()
        new_msg_bytes_str = ', '.join(['0x' + str(x) for x in new_msg_bytes])
        if verbose:
            print(f'bytes:\n\t{new_msg_bytes_str}')

        f_ascii.write(f'{str(new_msg)}\n')
        f_bin.write(new_msg.get_bytes())

        if verbose:
            print_line(' ', ' ')
            generator._orderbook.print_order_book(ticker)

    f_ascii.close()
    f_bin.close()

    print_line(' ', ' ')
    print_line(' ', ' ')
    print_line('=', '=', sep_len)
    print('Final OrderBook')
    print_line('=', '=', sep_len)
    print_line(' ', ' ')
    print_line(' ', ' ')
    generator._orderbook.print_order_book(ticker)
    print_line(' ', ' ')
    print_line(' ', ' ')
    print_line('=', '=', sep_len)


if __file__ == "__main__":
    main()


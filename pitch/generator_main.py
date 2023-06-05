import argparse
from datetime import datetime
from pitch.generator import Generator, WatchListItem
import sys
from typing import Any

def parse_args(parser) ->  Any:
    return parser.parse_args()

def main():
    print('Hello World')

    parser = argparse.ArgumentParser(
            prog='PITCH.Generator', 
            description='PITCH Message Generator and Parser',
            epilog='Bottom of help text'
            )
    parser.add_argument(
            '-o',
            '--output-file',
            default='pitch24.dat',
            help='Specify output file')
    args = parse_args(parser)

    # Set these variables from argument
    ticker = 'MSFT'
    weight = 0.50
    num_of_msgs = 5
    book_size_range = (2, 4)

    start_time = datetime.now()

    print(f'Start time: {start_time}')

    watch_list = [
            WatchListItem(ticker=ticker,
                          weight=weight,
                          book_size_range=book_size_range,
                          price_range=(50.00, 65.00),
                          size_range=(25, 200)
                          )
            ]
    generator = Generator(watch_list=watch_list,
                          msg_rate_p_sec=1,
                          start_time=start_time,
                          )
    generator.print_OrderBook(ticker)
    for i in range(num_of_msgs):
        new_msg = generator.getNextMsg()
        print('-'*80)
        print(f'new_msg: {new_msg} ({type(new_msg)})')
        print('-'*10)
        generator.print_OrderBook(ticker)

if __file__ == "__main__":
    main()


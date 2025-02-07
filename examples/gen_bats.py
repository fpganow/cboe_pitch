#!/usr/bin/env python3.11


from datetime import datetime


from cboe_pitch.seq_unit_header import SequencedUnitHeader



def main():
    """
    """

    print('Generate Messages\n')

    watch_list = []
    watch_list.append(
        WatchListItem(
            ticker="MSFT",
            weight=1.0,
            book_size_range=[10, 20],
            price_range=[400.0, 450.0],
            size_range=[5, 50],
        )
    )

    generator = Generator(
        watch_list=watch_list,
        msg_rate_p_sec=2,
        start_time=datetime.now().replace(microsecond=0),
        seed=1_000,
    )

    num_of_msgs = 10
    seq_unit_hdr_len = 500

    seq_unit_hdr = SequencedUnitHeader(hdr_sequence=1)

    new_msg = generator.getNextMsg()
    if (seq_unit_hdr.getLength() + new_msg.length()) <= seq_unit_hdr_len:
        seq_unit_hdr.addMessage(new_msg)
    else:
        seq_unit_array.append(seq_unit_hdr)
        seq_unit_hdr = SequencedUnitHeader(
            hdr_sequence=seq_unit_hdr.getNextSequence()
        )
        seq_unit_hdr.addMessage(new_msg)



if __file__ == "__main__":
    main()

from pathlib import Path
from typing import List

from pitch.seq_unit_header import SequencedUnitHeader


class FileParser:
    @staticmethod
    def parse_file(file_path: str) -> List[SequencedUnitHeader]:
        f_in = Path(file_path)
        if f_in.exists() is False:
            raise Exception(f"File {file_path} does not exist")

        rem_bytes = Path(file_path).read_bytes()

        out_arr = []

        more_seq = True
        while more_seq:
            [seq_unit_hdr, rem_bytes] = SequencedUnitHeader.from_bytestream(
                msg_bytes=rem_bytes
            )
            out_arr.append(seq_unit_hdr)

            if rem_bytes is None:
                break

        return out_arr

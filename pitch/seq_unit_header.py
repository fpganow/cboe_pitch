import collections
from typing import ByteString, List, OrderedDict

from pitch.message_factory import MessageFactory
from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class SequencedUnitHeader(MessageBase):
    """
    Field          Offset   Length   Value/Type   Description
    Hdr Length       0        2        Binary     Length of entire block of messages.
                                                  Includes this and header and Hdr Count
                                                  messages to follow.
    Hdr Count        2        1        Binary     Number of messages to follow this header.
    Hdr Unit         3        1        Binary     Unit that applies to messages included
                                                  in this header.
    Hdr Sequence     4        4        Binary     Sequence of first message to follow this
                                                  header.
    """

    def __init__(self, hdr_sequence: int = 1):
        self._field_specs: OrderedDict[FieldName, FieldSpec] = collections.OrderedDict()
        self._field_specs[FieldName.HdrLength] = FieldSpec(
            field_name=FieldName.HdrLength,
            offset=0,
            length=2,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.HdrCount] = FieldSpec(
            field_name=FieldName.HdrCount,
            offset=2,
            length=1,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.HdrUnit] = FieldSpec(
            field_name=FieldName.HdrUnit,
            offset=3,
            length=1,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.HdrSequence] = FieldSpec(
            field_name=FieldName.HdrSequence,
            offset=4,
            length=4,
            field_type=FieldType.Binary,
        )

        self._field_specs[FieldName.HdrLength].value(8)
        self._field_specs[FieldName.HdrCount].value(0)
        self._field_specs[FieldName.HdrUnit].value(1)
        self._field_specs[FieldName.HdrSequence].value(hdr_sequence)

        self._messages = []

    @staticmethod
    def from_bytestream(msg_bytes: ByteString) -> 'SequencedUnitHeader':
        # Read in Sequenced Unit Header
        seq_unit_hdr_bytes = msg_bytes[:8]

        seq_unit_hdr = SequencedUnitHeader()
        for idx, field_spec in enumerate(seq_unit_hdr._field_specs.values()):
            field_spec.fill_value(seq_unit_hdr_bytes)

        # Save Header Values
        old_hdr_count = seq_unit_hdr.hdr_count()
        old_hdr_length = seq_unit_hdr.hdr_length()
        seq_unit_hdr.hdr_count(0)
        seq_unit_hdr.hdr_length(8)

        # Remaining Bytes
        rem_bytes = msg_bytes[8:]

        while True:
            # Chop off a single message
            next_msg_len = rem_bytes[0]
            next_msg_bytes = rem_bytes[:next_msg_len]
            next_msg = MessageFactory.from_bytes(next_msg_bytes)
            seq_unit_hdr.addMessage(next_msg)

            # Is final message?
            if len(next_msg_bytes) == len(rem_bytes) or old_hdr_length == seq_unit_hdr.hdr_length():
                break
            else:
                # Chop off message that was just parsed
                rem_bytes = rem_bytes[next_msg_len:]

        rem_data = None
        if seq_unit_hdr.hdr_length() < len(msg_bytes):
            rem_data = msg_bytes[seq_unit_hdr.hdr_length():]

        return [seq_unit_hdr, rem_data]

    def hdr_length(self, hdr_length: int = None) -> int:
        if hdr_length is not None:
            self._field_specs[FieldName.HdrLength].value(hdr_length)
        return self._field_specs[FieldName.HdrLength].value()

    def hdr_count(self, hdr_count: int = None) -> int:
        if hdr_count is not None:
            self._field_specs[FieldName.HdrCount].value(hdr_count)
        return self._field_specs[FieldName.HdrCount].value()

    def hdr_unit(self, hdr_unit: int = None) -> int:
        if hdr_unit is not None:
            self._field_specs[FieldName.HdrUnit].value(hdr_unit)
        return self._field_specs[FieldName.HdrUnit].value()

    def hdr_sequence(self, hdr_sequence: int = None) -> int:
        if hdr_sequence is not None:
            self._field_specs[FieldName.HdrSequence].value(hdr_sequence)
        return self._field_specs[FieldName.HdrSequence].value()

    def getNextSequence(self) -> int:
        return self._field_specs[FieldName.HdrSequence].value() + len(self._messages)

    def addMessage(self, new_msg: MessageBase) -> None:
        self._messages.append(new_msg)
        self.hdr_length(hdr_length=self.hdr_length() + new_msg.length())
        self.hdr_count(hdr_count=self.hdr_count() + 1)

    def getMessages(self) -> List[MessageBase]:
        return self._messages

    def getLength(self) -> int:
        total_length = 8
        for msg in self._messages:
            total_length += msg.length()
        return total_length

    def __str__(self) -> str:
        pretty_msg_type = str(type(self)).split(".")[-1][:-2]
        msg_str = f"({pretty_msg_type}, "
        msg_str += f'HdrLength={self.hdr_length()}, '
        msg_str += f'HdrCount={self.hdr_count()}'
        msg_str += ")"
        return msg_str

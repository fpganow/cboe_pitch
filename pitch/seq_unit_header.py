import collections
from typing import OrderedDict

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
            offset=3,
            length=4,
            field_type=FieldType.Binary,
        )

        self._field_specs[FieldName.HdrLength].value(8)
        self._field_specs[FieldName.HdrCount].value(0)
        self._field_specs[FieldName.HdrUnit].value(1)
        self._field_specs[FieldName.HdrSequence].value(hdr_sequence)

        self._messages = []

    def hdr_length(self, hdr_length: int = None) -> int:
        if hdr_length is not None:
            self._field_specs[FieldName.HdrLength].value(hdr_length)
        return self._field_specs[FieldName.HdrLength].value()

    def hdr_count(self, hdr_count: int = None) -> int:
        if hdr_count is not None:
            self._field_specs[FieldName.HdrCount].value(hdr_count)
        return self._field_specs[FieldName.HdrCount].value()

    def getNextSequence(self) -> int:
        return self._field_specs[FieldName.HdrSequence].value() + len(self._messages)

    def addMessage(self, new_msg: MessageBase) -> None:
        self._messages.append(new_msg)
        self.hdr_length(hdr_length=self.hdr_length() + new_msg.length())
        self.hdr_count(hdr_count=self.hdr_count() + 1)

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

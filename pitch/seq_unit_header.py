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

    def __init__(self, hdr_count: int = 0, hdr_unit: int = 1, hdr_sequence: int = 1):
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
        self._field_specs[FieldName.HdrCount].value(hdr_count)
        self._field_specs[FieldName.HdrUnit].value(hdr_unit)
        self._field_specs[FieldName.HdrSequence].value(hdr_sequence)

import collections
from typing import Any, ByteString, OrderedDict, Union
from enum import Enum

import logging

logger = logging.getLogger(__name__)


class FieldName(Enum):
    HdrLength = 'Hdr Length'
    HdrCount = 'Hdr Count'
    HdrUnit = 'Hdr Unit'
    HdrSequence = 'Hdr Sequence'

    ModifyFlags = 'Modify Flags'
    AddFlags = 'Flags'
    Length = 'Length'
    CanceledQuantity = 'Canceled Quantity'
    ExecutedQuantity = 'Executed Quantity'
    ExecutionId = 'Execution Id'
    MessageType = 'Message Type'
    OrderId = 'Order Id'
    Price = 'Price'
    Quantity = 'Quantity'
    RemainingQuantity = 'Remaining Quantity'
    SideIndicator = 'Side Indicator'
    Symbol = 'Symbol'
    Time = 'Time'
    TimeOffset = 'Time Offset'

    ParticipantId = 'Participant Id'
    CustomerIndicator = 'Customer Indicator'


class FieldType(Enum):
    Alphanumeric = 0
    Binary = 1
    BinaryLongPrice = 2
    BinaryShortPrice = 3
    BitField = 4
    PrintableAscii = 5
    Value = 6


class FieldSpec:
    def __init__(self,
                 field_name: FieldName,
                 offset: int,
                 length: int,
                 field_type: FieldType,
                 value: Any = None):
        self._name = field_name
        self._offset = offset
        self._length = length
        self._field_type = field_type
        self._value = value

    def offset(self, offset: int = None) -> int:
        if offset is not None:
            self._offset = offset
        return self._offset

    def length(self, length: int = None) -> int:
        if length is not None:
            self._length = length
        return self._length

    def field_type(self, field_type: FieldType = None) -> Any:
        if field_type is not None:
            self._field_type = field_type
        return self._field_type

    def value(self, value: Any = None) -> Any:
        if value is not None:
            self._value = value
        return self._value

    def get_bytes(self) -> ByteString:
        if self._field_type == FieldType.Alphanumeric:
            return self._value.encode()
        elif self._field_type == FieldType.Binary:
            if type(self._value) is str:
                return self._value.encode()
            return self._value.to_bytes(self._length, byteorder='little')
        elif self._field_type == FieldType.BinaryLongPrice:
            tmp_val = int(self._value * 10_000)
            return tmp_val.to_bytes(self._length, byteorder='little')
        elif self._field_type == FieldType.BinaryShortPrice:
            tmp_val = int(self._value * 100)
            return tmp_val.to_bytes(self._length, byteorder='little')
        elif self._field_type == FieldType.BitField:
            return self._value.to_bytes(self._length, byteorder='little')
        elif self._field_type == FieldType.PrintableAscii:
            tmp_val = self._value + (self.length() - len(self._value)) * ' '
            return tmp_val.encode()
        elif self._field_type == FieldType.Value:
            return self._value.to_bytes(self._length, byteorder='little')
        return bytearray([])

    def fill_value(self, msg_bytes: ByteString) -> None:
        start_idx = self.offset()
        length = self.length()
        if self._field_type == FieldType.Alphanumeric:
            value = msg_bytes[start_idx:start_idx + length].decode()
            # print(f'Alphanumeric - value: {value}')
            self.value(value)
        elif self._field_type == FieldType.Binary:
            subset = msg_bytes[self.offset():
                               self.offset() + self.length()]
            value = int.from_bytes(subset, 'little')
            self.value(value)
            print(f'value: {value} ({hex(value)})')
        elif self._field_type == FieldType.BinaryLongPrice:
            subset = msg_bytes[self.offset():
                               self.offset() + self.length()]
            value = int.from_bytes(subset, 'little')
            value = value / 10_000
            self.value(value)
        elif self._field_type == FieldType.BinaryShortPrice:
            subset = msg_bytes[self.offset():
                               self.offset() + self.length()]
            value = int.from_bytes(subset, 'little')
            value = value / 100
            self.value(value)
        elif self._field_type == FieldType.BitField:
            subset = msg_bytes[self.offset(): self.offset() + 1]
            self.value(subset[0])
        elif self._field_type == FieldType.PrintableAscii:
            value = msg_bytes[start_idx:start_idx + length].decode()
            self.value(value)
        elif self._field_type == FieldType.Value:
            pass


class MessageBase(object):
    _messageType = None
    _field_specs: OrderedDict[FieldName, FieldSpec] = None

    def __init__(self):
        self._field_specs: OrderedDict[FieldName, FieldSpec] = collections.OrderedDict()

    def get_bytes(self):
        final_msg = bytearray()

        ordered_field_specs: OrderedDict[FieldName, FieldSpec] = OrderedDict(
            sorted(self._field_specs.items(), key=lambda x: x[1].offset()))
        for field_name, field_spec in ordered_field_specs.items():
            logger.debug(f'{field_name}')

            if field_spec.value() is not None:
                tmp_val = field_spec.get_bytes()
                tmp_val_str = [f'0x{format(x, "02x")}' for x in tmp_val]
                logger.debug(f'\tAppending: {list(tmp_val_str)}')

                final_msg.extend(tmp_val)
        return final_msg

    def from_bytes(self, msg_bytes: ByteString):
        if msg_bytes[0] != len(msg_bytes):
            raise Exception('Invalid message length in ByteString')
        if msg_bytes[1] != self._messageType:
            raise Exception('Invalid message type in ByteString')

        for idx, field_spec in enumerate(self._field_specs.values()):
            if idx == 0:
                if field_spec.value() != len(msg_bytes):
                    raise Exception('Invalid message length')
            elif idx == 1:
                if field_spec.value() != self._messageType:
                    raise Exception('Invalid message type')
            else:
                field_spec.fill_value(msg_bytes)

    def length(self) -> int:
        return self._field_specs[FieldName.Length].value()

    def messageType(self) -> int:
        return self._field_specs[FieldName.MessageType].value()

    def time(self) -> int:
        return self._field_specs[FieldName.Time].value()

    def time_offset(self, time_offset: int = None) -> int:
        if time_offset is not None:
            self._field_specs[FieldName.TimeOffset].value(time_offset)
        return self._field_specs[FieldName.TimeOffset].value()

    def order_id(self, order_id: str = None) -> str:
        if order_id is not None:
            self._field_specs[FieldName.OrderId].value(int.from_bytes(order_id.encode(), 'little'))
        order_id_ba = self._field_specs[FieldName.OrderId].value().to_bytes(8, 'little')
        return order_id_ba.decode('utf-8')

    def side(self, side: str = None) -> str:
        if side is not None:
            self._field_specs[FieldName.SideIndicator].value(side)
        return self._field_specs[FieldName.SideIndicator].value()

    def quantity(self, quantity: int = None) -> int:
        if quantity is not None:
            self._field_specs[FieldName.Quantity].value(quantity)
        return self._field_specs[FieldName.Quantity].value()

    def symbol(self, symbol: str = None) -> str:
        if symbol is not None:
            self._field_specs[FieldName.Symbol].value(symbol)
        return self._field_specs[FieldName.Symbol].value().strip()

    def price(self, price: float = None) -> float:
        if price is not None:
            self._field_specs[FieldName.Price].value(price)
        return self._field_specs[FieldName.Price].value()

    def displayed(self, displayed: bool = None) -> bool:
        if displayed is not None:
            self._field_specs[FieldName.AddFlags].value(1 if displayed is True else 0)
        return True if self._field_specs[FieldName.AddFlags].value() == 0x1 else False

    def executed_quantity(self, executed_quantity: int = None) -> int:
        if executed_quantity is not None:
            self._field_specs[FieldName.ExecutedQuantity].value(executed_quantity)
        return self._field_specs[FieldName.ExecutedQuantity].value()

    def remaining_quantity(self, remaining_quantity: int = None) -> int:
        if remaining_quantity is not None:
            self._field_specs[FieldName.RemainingQuantity].value(remaining_quantity)
        return self._field_specs[FieldName.RemainingQuantity].value()

    def execution_id(self, execution_id: str = None) -> str:
        if execution_id is not None:
            self._field_specs[FieldName.ExecutionId].value(int.from_bytes(execution_id.encode(), 'little'))
        execution_id_ba = self._field_specs[FieldName.ExecutionId].value().to_bytes(8, 'little')
        return execution_id_ba.decode('utf-8')


class Heartbeat:
    """
       A Sequenced Unit Header with a count field set to '0' will be used for
       heartbeat messages.
       During trading hours, heartbeat messages will be sent from the GRP and
       all multicast addresses if no data has been delivered within 1 second.
       Heartbeat messages never increments the sequence number.
       Heartbeats have a Hdr Sequence Value equal to the sequence of
       the next sequenced message.
    """

    def __init__(self):
        pass

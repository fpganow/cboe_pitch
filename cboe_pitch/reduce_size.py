from .pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class ReduceSizeBase(MessageBase):
    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length] = FieldSpec(
            field_name=FieldName.Length, offset=0, length=1, field_type=FieldType.Binary
        )
        self._field_specs[FieldName.MessageType] = FieldSpec(
            field_name=FieldName.MessageType,
            offset=1,
            length=1,
            field_type=FieldType.Value,
        )
        self._field_specs[FieldName.TimeOffset] = FieldSpec(
            field_name=FieldName.TimeOffset,
            offset=2,
            length=4,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.OrderId] = FieldSpec(
            field_name=FieldName.OrderId,
            offset=6,
            length=8,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.CanceledQuantity] = FieldSpec(
            field_name=FieldName.CanceledQuantity,
            offset=14,
            length=4,
            field_type=FieldType.Binary,
        )

    def set_fields(self, time_offset: int, order_id: str, canceled_quantity: int):
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)
        self._field_specs[FieldName.CanceledQuantity].value(canceled_quantity)

    def canceled_quantity(self, canceled_quantity: int = None) -> int:
        if canceled_quantity is not None:
            self._field_specs[FieldName.CanceledQuantity].value(canceled_quantity)
        return self._field_specs[FieldName.CanceledQuantity].value()


class ReduceSizeLong(ReduceSizeBase):
    _messageType = 0x25

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(18)
        self._field_specs[FieldName.MessageType].value(self._messageType)

    @staticmethod
    def from_parms(
        time_offset: int, order_id: str, canceled_quantity: int
    ) -> "ReduceSizeLong":
        reduce_size_long = ReduceSizeLong()
        reduce_size_long.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            canceled_quantity=canceled_quantity,
        )
        return reduce_size_long


class ReduceSizeShort(ReduceSizeBase):
    _messageType = 0x26

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(16)
        self._field_specs[FieldName.MessageType].value(self._messageType)
        self._field_specs[FieldName.CanceledQuantity].length(2)

    @staticmethod
    def from_parms(
        time_offset: int, order_id: str, canceled_quantity: int
    ) -> "ReduceSizeShort":
        reduce_size_short = ReduceSizeShort()
        reduce_size_short.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            canceled_quantity=canceled_quantity,
        )
        return reduce_size_short

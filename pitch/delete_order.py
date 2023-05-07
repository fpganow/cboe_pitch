from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class DeleteOrder(MessageBase):
    _messageType = 0x29

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

    def set_fields(self, time_offset: int, order_id: str):
        self._field_specs[FieldName.Length].value(14)
        self._field_specs[FieldName.MessageType].value(self._messageType)
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)

    @staticmethod
    def from_parms(time_offset: int, order_id: str) -> "DeleteOrder":
        delete_order = DeleteOrder()
        delete_order.set_fields(time_offset=time_offset, order_id=order_id)
        return delete_order

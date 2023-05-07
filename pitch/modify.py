from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class ModifyBase(MessageBase):
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
        self._field_specs[FieldName.Quantity] = FieldSpec(
            field_name=FieldName.Quantity,
            offset=14,
            length=4,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.Price] = FieldSpec(
            field_name=FieldName.Price,
            offset=18,
            length=8,
            field_type=FieldType.BinaryLongPrice,
        )
        self._field_specs[FieldName.ModifyFlags] = FieldSpec(
            field_name=FieldName.ModifyFlags,
            offset=26,
            length=1,
            field_type=FieldType.BitField,
        )

    def set_fields(
        self,
        time_offset: int,
        order_id: str,
        quantity: int,
        price: float,
        displayed: bool = True,
    ):
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)
        self._field_specs[FieldName.Quantity].value(quantity)
        self._field_specs[FieldName.Price].value(price)
        self._field_specs[FieldName.ModifyFlags].value(1 if displayed is True else 0)


class ModifyOrderLong(ModifyBase):
    _messageType = 0x27

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(27)
        self._field_specs[FieldName.MessageType].value(self._messageType)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        quantity: int,
        price: float,
        displayed: bool = True,
    ) -> "ModifyOrderLong":
        modify_long = ModifyOrderLong()
        modify_long.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            quantity=quantity,
            price=price,
            displayed=displayed,
        )
        return modify_long


class ModifyOrderShort(ModifyBase):
    _messageType = 0x28

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(19)
        self._field_specs[FieldName.MessageType].value(self._messageType)
        self._field_specs[FieldName.Quantity].length(2)
        self._field_specs[FieldName.Price].offset(16)
        self._field_specs[FieldName.Price].length(2)
        self._field_specs[FieldName.Price].field_type(FieldType.BinaryShortPrice)
        self._field_specs[FieldName.ModifyFlags].offset(18)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        quantity: int,
        price: float,
        displayed: bool = True,
    ) -> "ModifyOrderShort":
        modify_short = ModifyOrderShort()
        modify_short.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            quantity=quantity,
            price=price,
            displayed=displayed,
        )
        return modify_short

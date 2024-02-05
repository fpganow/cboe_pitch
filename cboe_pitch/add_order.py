from .pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class AddOrderBase(MessageBase):
    """
    Represents a newly accepted visible order on the Cboe book.
    """

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
        self._field_specs[FieldName.SideIndicator] = FieldSpec(
            field_name=FieldName.SideIndicator,
            offset=14,
            length=1,
            field_type=FieldType.Alphanumeric,
        )
        self._field_specs[FieldName.Quantity] = FieldSpec(
            field_name=FieldName.Quantity,
            offset=15,
            length=4,
            field_type=FieldType.Binary,
        )
        self._field_specs[FieldName.Symbol] = FieldSpec(
            field_name=FieldName.Symbol,
            offset=19,
            length=6,
            field_type=FieldType.PrintableAscii,
        )
        self._field_specs[FieldName.Price] = FieldSpec(
            field_name=FieldName.Price,
            offset=25,
            length=8,
            field_type=FieldType.BinaryLongPrice,
        )
        self._field_specs[FieldName.AddFlags] = FieldSpec(
            field_name=FieldName.AddFlags,
            offset=33,
            length=1,
            field_type=FieldType.BitField,
        )

    def set_fields(
        self,
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        displayed: bool = True,
    ):
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)
        self._field_specs[FieldName.SideIndicator].value(side)
        self._field_specs[FieldName.Quantity].value(quantity)
        self._field_specs[FieldName.Symbol].value(symbol)
        self._field_specs[FieldName.Price].value(price)
        self._field_specs[FieldName.AddFlags].value(1 if displayed is True else 0)


class AddOrderLong(AddOrderBase):
    _messageType = 0x21

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(34)
        self._field_specs[FieldName.MessageType].value(self._messageType)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        displayed: bool = True,
    ) -> "AddOrderLong":
        add_order_long = AddOrderLong()
        add_order_long.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            displayed=displayed,
        )

        return add_order_long


class AddOrderShort(AddOrderBase):
    _messageType = 0x22

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(26)
        self._field_specs[FieldName.MessageType].value(AddOrderShort._messageType)

        self._field_specs[FieldName.Quantity].offset(15)
        self._field_specs[FieldName.Quantity].length(2)
        self._field_specs[FieldName.Symbol].offset(17)
        self._field_specs[FieldName.Symbol].length(6)
        self._field_specs[FieldName.Price].offset(23)
        self._field_specs[FieldName.Price].length(2)
        self._field_specs[FieldName.Price].field_type(FieldType.BinaryShortPrice)
        self._field_specs[FieldName.AddFlags].offset(25)
        self._field_specs[FieldName.AddFlags].length(1)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        displayed: bool = True,
    ) -> "AddOrderShort":
        add_order_short = AddOrderShort()
        add_order_short.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            displayed=displayed,
        )
        return add_order_short


class AddOrderExpanded(AddOrderBase):
    _messageType = 0x2F

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(41)
        self._field_specs[FieldName.MessageType].value(AddOrderExpanded._messageType)

        self._field_specs[FieldName.Symbol].offset(19)
        self._field_specs[FieldName.Symbol].length(8)
        self._field_specs[FieldName.Price].offset(27)
        self._field_specs[FieldName.Price].length(8)
        self._field_specs[FieldName.AddFlags].offset(35)
        self._field_specs[FieldName.AddFlags].length(1)

        self._field_specs[FieldName.ParticipantId] = FieldSpec(
            field_name=FieldName.ParticipantId,
            offset=36,
            length=4,
            field_type=FieldType.Alphanumeric,
        )
        self._field_specs[FieldName.CustomerIndicator] = FieldSpec(
            field_name=FieldName.CustomerIndicator,
            offset=40,
            length=1,
            field_type=FieldType.Alphanumeric,
        )

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        displayed: bool = True,
        participant_id: str = "0001",
        customer_indicator: str = "C",
    ) -> "AddOrderExpanded":
        add_order_expanded = AddOrderExpanded()
        add_order_expanded.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            displayed=displayed,
        )
        add_order_expanded._field_specs[FieldName.ParticipantId] = FieldSpec(
            field_name=FieldName.ParticipantId,
            offset=36,
            length=4,
            field_type=FieldType.Alphanumeric,
            value=participant_id,
        )
        add_order_expanded._field_specs[FieldName.CustomerIndicator] = FieldSpec(
            field_name=FieldName.CustomerIndicator,
            offset=40,
            length=1,
            field_type=FieldType.Alphanumeric,
            value=customer_indicator,
        )

        return add_order_expanded

    def participant_id(self, participant_id: str = None) -> str:
        if participant_id is not None:
            self._field_specs[FieldName.ParticipantId].value(participant_id)
        return self._field_specs[FieldName.ParticipantId].value()

    def customer_indicator(self, customer_indicator: str = None) -> str:
        if customer_indicator is not None:
            self._field_specs[FieldName.CustomerIndicator].value(customer_indicator)
        return self._field_specs[FieldName.CustomerIndicator].value()

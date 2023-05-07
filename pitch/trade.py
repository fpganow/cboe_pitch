from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class TradeBase(MessageBase):
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
        self._field_specs[FieldName.ExecutionId] = FieldSpec(
            field_name=FieldName.ExecutionId,
            offset=33,
            length=8,
            field_type=FieldType.PrintableAscii,
        )

    def set_fields(
        self,
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        execution_id: str,
    ):
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)
        self._field_specs[FieldName.SideIndicator].value(side)
        self._field_specs[FieldName.Quantity].value(quantity)
        self._field_specs[FieldName.Symbol].value(symbol)
        self._field_specs[FieldName.Price].value(price)
        self._field_specs[FieldName.ExecutionId].value(execution_id)


class TradeLong(TradeBase):
    _messageType = 0x2A

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(41)
        self._field_specs[FieldName.MessageType].value(self._messageType)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        execution_id: str,
    ) -> "TradeLong":
        trade_long = TradeLong()
        trade_long.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            execution_id=execution_id,
        )
        return trade_long


class TradeShort(TradeBase):
    _messageType = 0x2B

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(33)
        self._field_specs[FieldName.MessageType].value(self._messageType)

        self._field_specs[FieldName.Quantity].offset(15)
        self._field_specs[FieldName.Quantity].length(2)
        self._field_specs[FieldName.Symbol].offset(17)

        self._field_specs[FieldName.Price].offset(23)
        self._field_specs[FieldName.Price].length(2)
        self._field_specs[FieldName.Price].field_type(FieldType.BinaryShortPrice)
        self._field_specs[FieldName.ExecutionId].offset(25)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        execution_id: str,
    ):
        trade_short = TradeShort()
        trade_short.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            execution_id=execution_id,
        )
        return trade_short


class TradeExpanded(TradeBase):
    _messageType = 0x30

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(43)
        self._field_specs[FieldName.MessageType].value(self._messageType)

        self._field_specs[FieldName.Symbol].length(8)
        self._field_specs[FieldName.Price].offset(27)
        self._field_specs[FieldName.Price].length(8)
        self._field_specs[FieldName.ExecutionId].offset(35)
        self._field_specs[FieldName.ExecutionId].length(8)

    @staticmethod
    def from_parms(
        time_offset: int,
        order_id: str,
        side: str,
        quantity: int,
        symbol: str,
        price: float,
        execution_id: str,
    ) -> "TradeExpanded":
        trade_expanded = TradeExpanded()
        trade_expanded.set_fields(
            time_offset=time_offset,
            order_id=order_id,
            side=side,
            quantity=quantity,
            symbol=symbol,
            price=price,
            execution_id=execution_id,
        )
        return trade_expanded

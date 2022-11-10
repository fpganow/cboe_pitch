from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class OrderExecutedBase(MessageBase):
    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length] = FieldSpec(field_name=FieldName.Length,
                                                        offset=0, length=1,
                                                        field_type=FieldType.Binary)
        self._field_specs[FieldName.MessageType] = FieldSpec(field_name=FieldName.MessageType,
                                                             offset=1, length=1,
                                                             field_type=FieldType.Value)
        self._field_specs[FieldName.TimeOffset] = FieldSpec(field_name=FieldName.TimeOffset,
                                                            offset=2, length=4,
                                                            field_type=FieldType.Binary)
        self._field_specs[FieldName.OrderId] = FieldSpec(field_name=FieldName.OrderId,
                                                         offset=6, length=8,
                                                         field_type=FieldType.Binary)
        self._field_specs[FieldName.ExecutedQuantity] = FieldSpec(field_name=FieldName.ExecutedQuantity,
                                                                  offset=14, length=4,
                                                                  field_type=FieldType.Binary)
        self._field_specs[FieldName.ExecutionId] = FieldSpec(field_name=FieldName.ExecutionId,
                                                             offset=18, length=8,
                                                             field_type=FieldType.Binary)

    def set_fields(self,
                   time_offset: int,
                   order_id: str,
                   executed_quantity: int,
                   execution_id: str):
        self._field_specs[FieldName.TimeOffset].value(time_offset)
        self.order_id(order_id)
        self._field_specs[FieldName.ExecutedQuantity].value(executed_quantity)
        self.execution_id(execution_id)


class OrderExecuted(OrderExecutedBase):
    _messageType = 0x23

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(26)
        self._field_specs[FieldName.MessageType].value(self._messageType)

    @staticmethod
    def from_parms(
            time_offset: int,
            order_id: str,
            executed_quantity: int,
            execution_id: str) -> 'OrderExecuted':
        order_executed = OrderExecuted()
        order_executed.set_fields(time_offset=time_offset,
                                  order_id=order_id,
                                  executed_quantity=executed_quantity,
                                  execution_id=execution_id)
        return order_executed


class OrderExecutedAtPriceSize(OrderExecutedBase):
    _messageType = 0x24

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length].value(38)
        self._field_specs[FieldName.MessageType].value(self._messageType)

        self._field_specs[FieldName.RemainingQuantity] = FieldSpec(field_name=FieldName.RemainingQuantity,
                                                                   offset=18, length=4,
                                                                   field_type=FieldType.Binary)
        self._field_specs[FieldName.ExecutionId].offset(22)
        self._field_specs[FieldName.ExecutionId].length(8)
        self._field_specs[FieldName.Price] = FieldSpec(field_name=FieldName.Price,
                                                       offset=30, length=8,
                                                       field_type=FieldType.BinaryLongPrice)

    @staticmethod
    def from_parms(
            time_offset: int,
            order_id: str,
            executed_quantity: int,
            remaining_quantity: int,
            execution_id: str,
            price: float) -> 'OrderExecutedAtPriceSize':
        order_executed = OrderExecutedAtPriceSize()
        order_executed.set_fields(time_offset=time_offset,
                                  order_id=order_id,
                                  executed_quantity=executed_quantity,
                                  execution_id=execution_id)
        order_executed._field_specs[FieldName.RemainingQuantity].value(remaining_quantity)
        order_executed._field_specs[FieldName.Price].value(price)
        return order_executed

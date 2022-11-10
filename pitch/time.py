from datetime import datetime

from pitch.pitch24 import MessageBase, FieldName, FieldSpec, FieldType


class Time(MessageBase):
    """
        A Time message is immediately generated and sent when there is a PITCH
        event for a given clock second.
    """
    _messageType = 0x20

    def __init__(self):
        super().__init__()
        self._field_specs[FieldName.Length] = FieldSpec(field_name=FieldName.Length,
                                                        offset=0, length=1,
                                                        field_type=FieldType.Binary,
                                                        value=6)
        self._field_specs[FieldName.MessageType] = FieldSpec(field_name=FieldName.MessageType,
                                                             offset=1, length=1,
                                                             field_type=FieldType.Value,
                                                             value=self._messageType)
        self._field_specs[FieldName.Time] = FieldSpec(field_name=FieldName.Time,
                                                      offset=2, length=4,
                                                      field_type=FieldType.Binary)

    def set_fields(self, time: int = None):
        seconds_since_midnight = time
        if time is None:
            now = datetime.now()
            seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
        self._field_specs[FieldName.Time].value(seconds_since_midnight)

    @staticmethod
    def from_parms(time: int) -> 'Time':
        time_message = Time()
        time_message.set_fields(time=time)
        return time_message

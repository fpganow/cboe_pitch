from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description


def compare_bytes(good_msg):
    return CompareBytes(good_msg)


class CompareBytes(BaseMatcher):
    def __init__(self, good_msg):
        self._good_msg = good_msg
        self._reason = ""

    def _matches(self, item):
        if not isinstance(item, bytearray):
            self._reason += "Expected value is not a bytearray"
            return False
        elif not isinstance(self._good_msg, bytearray):
            self._reason += "Actual value is not a bytearray"
            return False
        if len(self._good_msg) != len(item):
            return False
        for idx, good_item in enumerate(self._good_msg):
            if good_item != item[idx]:
                self._reason += f'Values at index {idx} do not match\n'
                self._reason += f'\t\t    {good_item}  !=   {item[idx]}\n'
                self._reason += f'\t\t  {hex(good_item)}  !=  {hex(item[idx])}'
                return False
        return True

    def describe_mismatch(self, item: bytearray, mismatch_description: Description) -> None:
        mismatch_description.append_text(self._reason)

    def describe_to(self, description):
        description.append_text('Compare bytearray')

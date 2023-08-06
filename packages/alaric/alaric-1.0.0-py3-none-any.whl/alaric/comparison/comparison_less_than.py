from typing import Dict, Union


class LT:
    """
    Asserts the provided field is less to the provided value.

    Parameters
    ----------
    field: str
        The field to check in.
    value: Union[int, str, float, bytes, dict]
        The value the field should be less than.
    """

    def __init__(self, field: str, value: Union[int, str, float, bytes]):
        self.field: str = field
        assert not isinstance(value, (list, tuple, set))
        self.value: Union[int, str, float, bytes] = value

    def __repr__(self):
        return f"LT(field='{self.field}', value={self.value})"

    def build(self) -> Dict[str, Dict[str, Union[int, str, float, bytes]]]:
        """Return this instance as a usable Mongo filter."""
        return {self.field: {"$lt": self.value}}

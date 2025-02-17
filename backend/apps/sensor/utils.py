from decimal import InvalidOperation
from typing import Optional, Union


def validate_float(value) -> Optional[Union[float, None]]:
    try:
        return float(value)
    except (InvalidOperation, ValueError, TypeError):
        return None

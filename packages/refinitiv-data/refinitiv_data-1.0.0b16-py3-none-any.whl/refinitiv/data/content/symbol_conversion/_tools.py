def _normalize(some: str, symbols_type: dict) -> str:
    some_lower = some.lower()
    symbol_type = symbols_type.get(some_lower)
    result = ""
    if symbol_type:
        result = symbol_type.value
    return result

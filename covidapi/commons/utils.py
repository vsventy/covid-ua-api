def safe_int(input: str) -> int:
    return int(input.replace('\xa0', '').strip())
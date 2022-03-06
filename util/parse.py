def parse_color(color_name: str):
    if color_name.startswith("#"):
        color_name = color_name[1:]
    color_name = color_name.lower()
    assert_alphabet(color_name, "0123456789abcdef")
    if len(color_name) in (3, 4):
        return tuple(16 * int(char, 16) for char in color_name)
    if len(color_name) in (6, 8):
        return tuple(int(color_name[i:i+2], 16) for i in range(0, len(color_name), 2))
    raise ValueError(f"unknown color length: {len(color_name)}")


def assert_alphabet(string: str, alphabet: str):
    for char in string:
        if char not in alphabet:
            raise ValueError(f"character {char} not allowed, not in {alphabet}")

def to_snake_case(string: str) -> str:
    index = 0
    while index < len(string):
        char = string[index]
        if index == 0:
            string = char.lower() + string[index + 1 :]

        elif char.isupper():
            string = string[:index] + f"_{char.lower()}" + string[index + 1 :]
            index += 1

        index += 1

    return string

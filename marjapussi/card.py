class Card:
    COLOR_NAMES = {
        "r": "Rot",
        "s": "Schell",
        "e": "Eichel",
        "g": "Grün"
    }

    def __init__(self, color, value):
        if color not in COLORS:
            raise ValueError(f"Invalid color: {color}")
        if value not in VALUES:
            raise ValueError(f"Invalid value: {value}")

        self.color = color
        self.value = value

    def __str__(self):
        return f"{self.color}-{self.value}"

    def __eq__(self, other):
        return self.color == other.color and self.value == other.value

    def __hash__(self):
        return hash((self.color, self.value))

    def is_higher_than(self, other):
        return VALUES.index(self.value) > VALUES.index(other.value)
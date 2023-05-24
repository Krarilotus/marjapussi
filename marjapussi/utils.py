from card import Card

COLORS = ["r", "s", "e", "g"]
VALUES = ["A", "Z", "K", "O", "U", "9", "8", "7", "6"]

CARDS = [Card(c, v) for c in COLORS for v in VALUES]

text_format = {"r": "\033[91m", "s": "\033[93m", "e": "\033[96m", "g": "\033[92m",
               "end": "\033[0m", "bold": "\033[1m", "uline": "\033[4m"}


def allowed_first(cards) -> list:
    """First player has to play an ace, green or any card."""
    allowed = [c for c in cards if c.value == 'A']
    if not allowed:
        allowed = [c for c in cards if c.color == 'g']
    if not allowed:
        allowed = cards[:]
    return allowed


def high_card(cards, trump="") -> Card | None:
    """Finds the highest card in single trick."""
    if not cards:
        return None
    col = cards[0].color
    base_col_cards = [card for card in cards if card.color == col]
    trump_cards = [card for card in cards if card.color == trump]
    return max(trump_cards, default=max(base_col_cards, default=None), key=lambda card: card.VALUES.index(card.value))


def allowed_general(trick, cards, trump=None, first=False) -> list:
    if len(trick) == 0 and first:
        return allowed_first(cards)
    if not trick:
        return cards

    trick_col = trick[0].color
    if first:
        # check for ace
        ace = next((card for card in cards if card.color == trick_col and card.value == 'A'), None)
        if ace:
            return [ace]

    allowed = [card for card in cards if card.color == trick_col]
    if not allowed:
        allowed = [card for card in cards if card.color == trump]
    high = high_card(trick + allowed, trump=trump)
    if high in allowed:
        allowed = [high]

    return allowed if allowed else cards


def higher_value(base, card) -> bool:
    """Returns True if card has higher value than base."""
    return card.is_higher_than(base)


def higher_cards(base, trump='', pool=None) -> list:
    """Returns all cards out of the pool that would win a trick over base as high card."""
    if pool is None:
        pool = CARDS
    if not trump:
        return [card for card in pool if card.is_higher_than(base) and base.color == card.color]
    return [card for card in pool if (card.is_higher_than(base) and base.color == card.color) or (card.color == trump)]


def contains_pair(cards, col) -> bool:
    return any(card.color == col and card.value == "K" for card in cards) and any(
        card.color == col and card.value == "O" for card in cards)


def contains_half(cards, col) -> bool:
    return any(card.color == col and (card.value == "K" or card.value == "O") for card in cards)


def sorted_cards(cards) -> list:
    return sorted(cards, key=lambda card: (COLORS.index(card.color), VALUES.index(card.value)))


def all_color_cards(col):
    """Returns all cards with given color."""
    return [Card(col, v) for v in VALUES]


def all_value_cards(value):
    """Returns all cards with given type."""
    return [Card(c, value) for c in COLORS]


def card_str(card, fancy=True) -> str:
    return text_format[card.color] + str(card) + text_format["end"] if fancy else str(card)


def cards_str(cards, fancy=True) -> str:
    return " ".join([card_str(card, fancy=fancy) for card in cards])


def color_str(col, fancy=True) -> str:
    return text_format[col] + Card.COLOR_NAMES[col] + text_format["end"] if fancy else Card.COLOR_NAMES[col]


def bold_str(s, fancy=True) -> str:
    return text_format["bold"] + s + text_format["end"] if fancy else s

# COLORS = [c for c in "rseg"]
# VALUES = [v for v in "AZKOU9876"]
# CARDS = [c + "-" + v for c in COLORS for v in VALUES]
#
#
# COLOR_NAMES = {c: name for c, name in zip(
#     "rseg", ["Rot", "Schell", "Eichel", "Grün"])}
#
#
#
#
# def allowed_general(trick, cards, trump=None, first=False) -> list:
#     if len(trick) == 0 and first:
#         return allowed_first(cards)
#     if not trick:
#         return cards
#     trick_col = trick[0][0]
#     if first:
#         # check for ace
#         if (ace := f"{trick_col}-A") in cards:
#             return [ace]
#
#     if not (allowed:=[c for c in cards if c[0] == trick_col]):
#         allowed = [c for c in cards if c[0] == trump]
#     if (b:=list(filter(lambda card: card == high_card(trick+[card], trump=trump), allowed))):
#         allowed = b
#     return allowed if allowed else cards
#
#
# def high_card(cards, trump="") -> str:
#     """Finds highest card in single trick."""
#     if not cards:
#         return None
#     col = cards[0][0]
#     base_col_cards = [card for card in cards if card[0] == col]
#     trump_cards = [card for card in cards if card[0] == trump]
#     return trump_cards[-1] if trump_cards else base_col_cards[-1]
#     """#!! also not really nice, there has to be a cleaner way but
#     for c in cards:
#         if c[0] == col and higher_value(high, c):
#             high = c
#     sup_high = high_card([c for c in cards if c[0] == trump]
#                          ) if trump != "" and trump != col else None
#     return sup_high if not sup_high is None else high"""
#
#
# def higher_value(base, card) -> bool:
#     """Returns True if card has higher value than base."""
#     for val in VALUES:
#         if base[2] == val:
#             return False
#         if card[2] == val:
#             return True
#
#
# def higher_cards(base, trump='', pool=CARDS) -> list:
#     """Returns all cards out of the pool that would win a trick over base as high card."""
#     if not trump:
#         return [card for card in pool if higher_value(base, card) and base[0] == card[0]]
#     return [card for card in pool if (higher_value(base, card) and base[0] == card[0]) or (card[0] == trump)]
#
#
# def contains_pair(cards, col) -> bool:
#     return f"{col}-K" in cards and f"{col}-O" in cards
#
#
# def contains_half(cards, col) -> bool:
#     return f"{col}-K" in cards or f"{col}-O" in cards
#
#
# def sorted_cards(cards) -> list:
#     return [card for card in CARDS if card in set(cards)]
#     return cards
#
#
# def all_color_cards(col):
#     """Returns all cards with given color."""
#     return [f"{col}-{v}" for v in VALUES]
#
#
# def all_value_cards(value):
#     """Returns all cards with given type."""
#     return [f"{c}-{value}" for c in COLORS]
#
#
# def card_str(card, fancy=True) -> str:
#     return text_format[card[0]] + card + text_format["end"] if fancy else card
#
#
# def cards_str(cards, fancy=True) -> str:
#     return " ".join([card_str(card, fancy=fancy) for card in cards])
#
#
# def color_str(col, fancy=True) -> str:
#     return text_format[col] + COLOR_NAMES[col] + text_format["end"] if fancy else COLOR_NAMES[col]
#
#
# def bold_str(s, fancy=True) -> str:
#     return text_format["bold"] + s + text_format["end"] if fancy else s

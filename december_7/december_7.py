import functools
from collections import Counter

def get_hand_type(hand, joker=False):
    """ we get the type of the card hand """

    result = Counter(hand)

    cards = sorted(result.values(), reverse=True)

    n_jokers = 0
    if joker:
        n_jokers = result['J']

    if cards == [5]:
        return 7  # five of a kind
    elif cards == [4, 1]:
        if n_jokers > 0:
            return 7
        return 6  # four of a kind
    elif cards == [3, 2]:
        if n_jokers > 0:
            return 7  # five of a kind
        return 5 # full house
    elif cards == [3, 1, 1]:
        if n_jokers > 0:
            return 6  # four of a kind
        return 4  # three of a kind
    elif cards == [2, 2, 1]:
        if n_jokers == 2:
            return 6 # four of a kind
        if n_jokers == 1:
            return 5  # full house 
        return 3  # two pair
    elif cards == [2, 1, 1, 1]:
        if n_jokers > 0:
            return 4 # three of a kind
        return 2  # one pair
    else:
        if n_jokers > 0:
            return 2  # one pair
        return 1  # high card
    

converter_part_1 = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

converter_part_2 = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 1,
    'Q': 12,
    'K': 13,
    'A': 14
}

def compare_hands(hand1, hand2):
    hand1 = hand1[0]
    hand2 = hand2[0]

    hand1_type = get_hand_type(hand1)
    hand2_type = get_hand_type(hand2)

    if hand1_type > hand2_type:
        return 1
    elif hand1_type < hand2_type:
        return -1
    else:
        for card1, card2 in zip(hand1, hand2):
            value_1 = converter_part_1[card1]
            value_2 = converter_part_1[card2]
            if value_1 > value_2:
                return 1
            elif value_1 < value_2:
                return -1
        return 0  #hands are equal

def compare_hands_2(hand1, hand2):
    hand1 = hand1[0]
    hand2 = hand2[0]

    hand1_type = get_hand_type(hand1, joker=True)
    hand2_type = get_hand_type(hand2, joker=True)

    if hand1_type > hand2_type:
        return 1
    elif hand1_type < hand2_type:
        return -1
    else:
        for card1, card2 in zip(hand1, hand2):
            value_1 = converter_part_2[card1]
            value_2 = converter_part_2[card2]
            if value_1 > value_2:
                return 1
            elif value_1 < value_2:
                return -1
        return 0  #hands are equal


def main():
    with open('./december_7/input.txt') as f:
        lines = f.readlines()

    hands = []
    for line in lines:
        line = line.strip()
        line_split = line.split(' ')
        hand = line_split[0]
        bid = int(line_split[1])
        hands.append((hand, bid))


    """ part 1 """
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands))

    sum_ = 0
    for i, hand in enumerate(sorted_hands):
        sum_ += hand[1] * (i+1)

    print(f"Total sum is {sum_}")

    """ part 2 """
    sorted_hands = sorted(hands, key=functools.cmp_to_key(compare_hands_2))

    sum_ = 0
    for i, hand in enumerate(sorted_hands):
        sum_ += hand[1] * (i+1)

    print(f"Total sum is {sum_}")


if __name__ == "__main__":
    main()